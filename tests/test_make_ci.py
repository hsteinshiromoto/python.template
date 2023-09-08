import sys
from pathlib import Path

import pytest
from cartorio import log, make_logger
from git import Repo

PROJECT_ROOT = Path(__file__).parents[1].resolve()

sys.path.append(str(PROJECT_ROOT / "{{cookiecutter.project_slug}}"))

import bin.make_ci as mc


def test_get_file(tmp_path):
    for file in ["ci.yml", "new_release.yml"]:
        url = f"https://raw.githubusercontent.com/hsteinshiromoto/python.template/dev/files/{file}"
        mc.get_file(url, path=tmp_path)
        assert (tmp_path / file).exists()


def test_get_repository_name():
    assert mc.get_repository_name() == "template.py"


def test_main(tmp_path):

    local_repo = Repo(PROJECT_ROOT)
    local_branch = local_repo.active_branch.name
    mc.main(git_branch_name=local_branch, path=tmp_path)

    with open(str(tmp_path / "ci.yml"), mode="r", encoding="utf-8") as file:
        content = file.read()
        assert "python.template" in content
        assert "[[cookiecutter.project_slug]]" not in content
