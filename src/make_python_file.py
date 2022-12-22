import contextlib
from pathlib import Path
import json

import git


def get_project_root() -> Path:
    return Path(git.Repo(".", search_parent_directories=True).working_tree_dir)


def get_config(filename: str | Path, path: Path) -> dict:
    """Get configuration from YAML file.

    Params:
        filename (str | Path): Name of YAML file.
        path (Path): Path to YAML file.

    Returns:
        dict: Configuration dictionary.
    """

    with open(str(path / filename), "r") as f:
        config = json.load(f)

    return config


def make_directory_structure(file: dict, path: Path = get_project_root()):
    """Make directory structure from JSON file.

    Args:
        file (dict): JSON file containing the directory structure to create.
        path (Path, optional): Path where to create the directory. Defaults to get_project_root().
    """
    if file["type"] == "directory":
        # Create the directory
        print(f"Creating directory {path / file['name']}")
        (path / file["name"]).mkdir(parents=True, exist_ok=True)

        # Recursively process the children of the directory
        with contextlib.suppress(KeyError):
            for child in file["children"]:
                make_directory_structure(child, path / file["name"])
    else:
        # Create the file
        print(f"Creating file {path / file['name']}")
        with (path / file["name"]).open("w", encoding="utf-8") as f:
            f.write(" ")


def main():
    settings = get_config("machine_learning.json", get_project_root() / "conf")

    make_directory_structure(settings, Path("/workspaces/tmp"))


if __name__ == "__main__":
    main()
