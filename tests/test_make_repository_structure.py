import contextlib
import sys
from pathlib import Path

import pytest
from cartorio import log, make_logger

PROJECT_ROOT = Path(__file__).parents[1].resolve()

sys.path.append(str(PROJECT_ROOT / "{{cookiecutter.project_slug}}"))

import bin.make_repository_structure as mrs


def read_directory_structure(file: dict, path: Path):
    """Make directory structure from JSON file.

    Args:
        file (dict): JSON file containing the directory structure to create.
        path (Path, optional): Path where to create the directory. Defaults to get_project_root().
    """
    if file["type"] == "directory":
        # test directory
        (path / file["name"]).exists()

        # Recursively process the children of the directory
        with contextlib.suppress(KeyError):
            for child in file["children"]:
                read_directory_structure(child, path / file["name"])
    else:
        # Test file
        (path / file["name"]).exists()


def test_error_on_invalid_repository_type():
    with pytest.raises(ValueError):
        mrs.main("invalid_repository_type")


# @pytest.fixture(scope="session")
def test_repository_structure_creation(tmp_path):
    path = tmp_path / "tests"
    settings = mrs.get_config(
        "machine_learning", PROJECT_ROOT / "{{cookiecutter.project_slug}}" / "conf"
    )
    mrs.main(settings, path)
    read_directory_structure(settings, path)
