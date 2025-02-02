#!/usr/bin/env python3

import argparse
import wget
from pathlib import Path

import git
from cartorio import log, make_logger

PROJECT_ROOT = Path(git.Repo(".", search_parent_directories=True).working_tree_dir)  # type: ignore


@log
def get_file(url: str, path: Path):
    """Gets a file from a URL and saves it in a given path.

    Args:
        url (str): URL to download the file from.
        path (Path, optional): Path to save the file to.

    Returns:
        None: Not used.

    Example:
        >>> path = PROJECT_ROOT / ".github" / "workflows"
        >>> get_file("https://raw.githubusercontent.com/hsteinshiromoto/template.py/dev/files/ci.yml", path=path)
        >>> (path / "ci.yml").exists()
        True
    """
    wget.download(url, out=str(path))


def get_repository_name(path: Path = PROJECT_ROOT) -> str:
    """Get the name of the repository.

    Args:
        path (Path, optional): Path to project root folder. Defaults to PROJECT_ROOT.

    Returns:
        str: Name of the repository.

    Example:
        >>> get_repository_name(PROJECT_ROOT)
        'template.py'
    """
    repo = git.Repo(path)
    return repo.remotes.origin.url.split(".git")[0].split("/")[-1]


@log
def main(
    git_branch_name: str = "main", path: Path = PROJECT_ROOT / ".github" / "workflows"
):

    # Get the repository name

    files_list = ["ci.yml", "new_release.yml"]
    repository_name = get_repository_name()

    for filename in files_list:
        base_url_map = f"https://raw.githubusercontent.com/hsteinshiromoto/template.py/{git_branch_name}/files/{filename}"
        get_file(base_url_map, path=path)

        if filename == "ci.yml":
            with open(str(path / filename), mode="r", encoding="utf-8") as file:
                content = file.read()

            content = content.replace("[[cookiecutter.project_slug]]", repository_name)

            with open(str(path / filename), mode="w", encoding="utf-8") as file:
                file.write(content)


if __name__ == "__main__":
    logger, _ = make_logger(__file__, PROJECT_ROOT / "logs")

    args = argparse.ArgumentParser()
    args.add_argument(
        "-b",
        "--git_branch_name",
        type=str,
        default="",
        help="Project Slug.",
    )

    inputs = args.parse_args()

    main(git_branch_name=inputs.git_branch_name)
