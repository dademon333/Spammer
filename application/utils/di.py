from contextlib import AsyncExitStack
from typing import Any, Callable, Awaitable

from fastapi import Request
from fastapi.dependencies.utils import (
    get_dependant,
    solve_dependencies,
    is_gen_callable,
    is_async_gen_callable,
    solve_generator,
    is_coroutine_callable,
)
from starlette.concurrency import run_in_threadpool


class DependencyInjector[T]:
    """FastAPI add-on over solve_dependencies,
    which can be used outside request scope.

    Example usage:
    ```
    async with DependencyInjector() as injector:
        foo_use_case = await injector.solve(get_foo_use_case)
        bar_repository = await injector.solve(get_bar_repository)
        await use_case.execute(...)
    # commits and closes db connection/etc
    some_next_login()
    ```
    `DependencyInjector.solve` adds a dependency to AsyncExitStack
    (inside FastAPI's `solve_dependencies`), then
    `DependencyInjector.__aexit__` calls `AsyncExitStack.aclose`,
    which gracefully shuts down yield-dependencies
    via `__anext__` (e.g. db transactions, connections).
    """

    def __init__(self, use_cache: bool = True):
        self.use_cache = use_cache
        self.exit_stack = AsyncExitStack()
        self.cache: dict[tuple, Any] = {}

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()

    async def solve(
        self, get_dependency: Callable[..., T | Awaitable[T]]
    ) -> T:
        if self.use_cache:
            cache_key = (get_dependency, ())
            if cache_key in self.cache:
                return self.cache[cache_key]

        dependant = get_dependant(path="/", call=get_dependency)
        request = Request(
            scope={
                "type": "http",
                "query_string": "",
                "headers": [],
                "fastapi_astack": self.exit_stack,
            }
        )
        kwargs, *_, self.cache = await solve_dependencies(
            request=request, dependant=dependant, dependency_cache=self.cache
        )

        if is_gen_callable(get_dependency) or is_async_gen_callable(
            get_dependency
        ):
            solved = await solve_generator(
                call=get_dependency, stack=self.exit_stack, sub_values=kwargs
            )
        elif is_coroutine_callable(get_dependency):
            solved = await get_dependency(**kwargs)  # type: ignore
        else:
            solved = await run_in_threadpool(get_dependency, **kwargs)

        if self.use_cache:
            self.cache[(get_dependency, ())] = solved

        return solved
