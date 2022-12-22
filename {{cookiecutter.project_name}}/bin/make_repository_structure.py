import contextlib
import json
from pathlib import Path

import git
from cartorio import make_logger, log


@log
def get_project_root() -> Path:
    return Path(git.Repo(".", search_parent_directories=True).working_tree_dir)


@log
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


@log
def make_directory_structure(file: dict, path: Path = get_project_root()):
    """Make directory structure from JSON file.

    Args:
        file (dict): JSON file containing the directory structure to create.
        path (Path, optional): Path where to create the directory. Defaults to get_project_root().
    """
    if file["type"] == "directory":
        # Create the directory
        logger.info(f"Creating directory {path / file['name']}")
        (path / file["name"]).mkdir(parents=True, exist_ok=True)

        # Recursively process the children of the directory
        with contextlib.suppress(KeyError):
            for child in file["children"]:
                make_directory_structure(child, path / file["name"])
    else:
        # Create the file
        logger.info(f"Creating file {path / file['name']}")
        with (path / file["name"]).open("w", encoding="utf-8") as f:
            f.write(" ")


@log
def main(repository_type: str):

    try:
        settings = get_config(f"{repository_type}.json", get_project_root() / "conf")

    except IOError as e:
        p = (get_project_root() / "conf").glob("*.json")
        msg = f"Expected repository_type to be either {[x.stem for x in p if x.is_file()]}. Got {repository_type}"
        raise ValueError(msg) from e

    make_directory_structure(settings)


if __name__ == "__main__":
    logger, _ = make_logger(__file__, get_project_root() / "logs")
    main("python")
