"""Utility module for path handling"""

import os
import config


def get_files_from_paths(paths: list[str]) -> list[str]:
    """Gets unique file paths from multiple paths"""
    files = []

    for path in paths:
        files.extend(get_files_from_path(path))

    return list(set(files))


def get_files_from_path(path: str) -> list[str]:
    """Get files paths from path and determine it it exists, is file or directory"""

    files = []

    if not os.path.exists(path):
        config.print_red(f"No such file or directory: '{path}'")
        return []

    if os.path.isfile(path):
        files.append(path)

    if os.path.isdir(path):
        files.extend(get_files_from_dir(path))

    return files


def get_files_from_dir(path: str) -> list[str]:
    """Walk path and return files relative to initial path"""
    all_files = []
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files
