from pathlib import Path


def collect_fixtures() -> tuple:
    """Автоматически собирает все файлы с фикстурами из папки fixtures"""

    fixtures = []
    project_root = Path(__file__).parent
    fixtures_dir = project_root / "fixtures"

    for path in fixtures_dir.rglob("*.py"):
        if path.is_file() and not path.name.startswith("_"):
            # Пример: fixtures/models/calls.py
            relative_path = str(path.relative_to(project_root))
            # К формату fixtures.models.calls
            relative_path = relative_path.replace(".py", "").replace("/", ".")
            fixtures.append(relative_path)

    return tuple(fixtures)


pytest_plugins = collect_fixtures()
