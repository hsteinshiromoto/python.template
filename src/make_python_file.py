from pathlib import Path

import git

def get_project_root() -> Path:
    return Path(git.Repo('.', search_parent_directories=True).working_tree_dir)

print(get_project_root())