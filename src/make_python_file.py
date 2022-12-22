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


def main():
    settings = get_config("machine_learning.json", get_project_root() / "conf")

    print(settings)


if __name__ == "__main__":
    main()
