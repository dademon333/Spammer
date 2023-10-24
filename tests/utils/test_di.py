from unittest.mock import Mock

import pytest
from fastapi import Depends

from application.utils.di import DependencySolver


def func_without_args_1():
    return 123


def func_without_args_2():
    return 456


def func_with_one_kwarg(result: int = 1000):
    return result


def func_with_one_dep_arg(result: int = Depends(func_without_args_1)):
    return result


async def async_func_with_one_dep_arg(
    result: int = Depends(func_without_args_1),
):
    return result


def func_with_mixed_args(
    result: int = Depends(func_without_args_1),
    kwarg: int = 2000,
):
    return [result, kwarg]


def func_with_two_dep_args(
    result_1: int = Depends(func_without_args_1),
    result_2: int = Depends(func_without_args_2),
):
    return [result_1, result_2]


def func_with_nested_args(
    result_1: int = Depends(func_with_one_dep_arg),
    result_2: int = 456,
):
    return [result_1, result_2]


async def test_without_args():
    async with DependencySolver() as solver:
        result = await solver.solve(func_without_args_1)
    assert result == 123


async def test_with_one_kwarg():
    async with DependencySolver() as solver:
        result = await solver.solve(func_with_one_kwarg)
    assert result == 1000


async def test_with_one_dep_arg():
    async with DependencySolver() as solver:
        result = await solver.solve(func_with_one_dep_arg)
    assert result == 123


async def test_async_func_with_one_dep_arg():
    async with DependencySolver() as solver:
        result = await solver.solve(async_func_with_one_dep_arg)
    assert result == 123


async def test_func_with_mixed_args():
    async with DependencySolver() as solver:
        result = await solver.solve(func_with_mixed_args)
    assert result == [123, 2000]


async def test_func_with_two_dep_args():
    async with DependencySolver() as solver:
        result = await solver.solve(func_with_two_dep_args)
    assert result == [123, 456]


async def test_func_with_nested_args():
    async with DependencySolver() as solver:
        result = await solver.solve(func_with_nested_args)
    assert result == [123, 456]


async def test_with_cache():
    async with DependencySolver() as solver:
        mock = Mock(side_effect=[1, 2])
        result_1 = await solver.solve(mock)
        result_2 = await solver.solve(mock)
    assert result_1 is result_2
    assert mock.call_count == 1


async def test_without_cache():
    async with DependencySolver(use_cache=False) as solver:
        mock = Mock(side_effect=[1, 2])
        result_1 = await solver.solve(mock)
        result_2 = await solver.solve(mock)
    assert result_1 == 1
    assert result_2 == 2
    assert mock.call_count == 2


async def test_cache_with_subdeps():
    foo_calls = 0
    bar_calls = 0

    def foo() -> int:
        nonlocal foo_calls
        foo_calls += 1
        return 123

    def bar(value: int = Depends(foo)) -> int:
        nonlocal bar_calls
        bar_calls += 1
        return value + 100

    async with DependencySolver() as solver:
        await solver.solve(bar)
        await solver.solve(bar)
        await solver.solve(foo)

    assert foo_calls == 1
    assert bar_calls == 1


async def test_closes_generator_dependencies():
    is_closed = False

    def get_db():
        nonlocal is_closed
        yield 123
        is_closed = True

    async with DependencySolver() as solver:
        result = await solver.solve(get_db)
        assert result == 123
        assert not is_closed

    assert is_closed


async def test_closes_async_generator_dependencies():
    is_closed = False

    async def get_db():
        nonlocal is_closed
        yield 123
        is_closed = True

    async with DependencySolver() as solver:
        result = await solver.solve(get_db)
        assert result == 123
        assert not is_closed

    assert is_closed


async def test_closes_dependencies_on_exception():
    is_closed = False

    async def get_db():
        nonlocal is_closed
        yield 123
        is_closed = True

    with pytest.raises(ValueError):
        async with DependencySolver() as solver:
            await solver.solve(get_db)
            assert not is_closed
            raise ValueError("Some exception")

    assert is_closed
