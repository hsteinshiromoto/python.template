import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parents[1].resolve()

sys.path.append(str(PROJECT_ROOT))

mrs = __import__(r"{{cookiecutter.project_slug}}")


def test_error_on_invalid_repository_type():
    with pytest.raises(ValueError):
        mrs.main("invalid_repository_type")
