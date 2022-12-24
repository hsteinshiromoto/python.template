import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parents[1].resolve()

sys.path.append(str(PROJECT_ROOT / "{{cookiecutter.project_slug}}"))

import bin.make_repository_structure as mrs


def test_error_on_invalid_repository_type():
    with pytest.raises(ValueError):
        mrs.main("invalid_repository_type")
