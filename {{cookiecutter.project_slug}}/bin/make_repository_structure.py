#!/usr/bin/env python3

import argparse
import contextlib
import json
from pathlib import Path

import git
from cartorio import log, make_logger


@log
def get_project_root() -> Path:
    return Path(git.Repo(".", search_parent_directories=True).working_tree_dir)  # type: ignore


@log
def get_config(repository_type: Path | str, path: Path | str = "") -> dict:
    """Get configuration from YAML file.

    Params:
        repository_type (Path | str): Name of YAML file.
        path (Path | str): Path to YAML file.

    Returns:
        dict: Configuration dictionary.
    """
    path = Path(path) if path else get_project_root()

    try:
        with open(str(path / f"{repository_type}.json"), "r") as f:
            config = json.load(f)

    except IOError as e:
        p = (path / "conf").glob("*.json")
        msg = f"Expected repository_type to be either {[x.stem for x in p if x.is_file()]}. Got {repository_type}"
        raise ValueError(msg) from e

    return config


@log
def make_directory_structure(file: dict, path: Path = get_project_root()):
    """Make directory structure from JSON file.

    Args:
        file (dict): JSON file containing the directory structure to create.
        path (Path, optional): Path where to create the directory. Defaults to get_project_root().
    """
    if file["type"] == "directory":
        # Create the directory
        # logger.info(f"Creating directory {path / file['name']}")
        (path / file["name"]).mkdir(parents=True, exist_ok=True)

        # Recursively process the children of the directory
        with contextlib.suppress(KeyError):
            for child in file["children"]:
                make_directory_structure(child, path / file["name"])
    else:
        # Create the file
        # logger.info(f"Creating file {path / file['name']}")
        with (path / file["name"]).open("w", encoding="utf-8") as f:
            f.write(" ")


@log
def main(settings: dict, path: Path | str = ""):

    path = Path(path) if path else get_project_root()

    make_directory_structure(settings, path)


if __name__ == "__main__":
    logger, _ = make_logger(__file__, get_project_root() / "logs")

    args = argparse.ArgumentParser()
    args.add_argument(
        "-p",
        "--path",
        type=str,
        default="",
        help="Path to create the repository structure.",
    )
    args.add_argument(
        "-r", "--repository_type", type=str, help="Type of repository to create."
    )
    inputs = args.parse_args()

    settings = get_config(inputs.repository_type, inputs.path)
    main(settings, inputs.path)
