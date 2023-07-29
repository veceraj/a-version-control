"""Config module"""

import json
from pathlib import Path
from io import TextIOWrapper
from dataclasses import asdict
import dataobjects


path_meta = Path(".vc/metadata.json")
path_ignore = Path(".vcignore")

LOG_EXTENSION = "diff_log"
ADD = "add"
REMOVE = "remove"

ENCODING = "utf-8"


def serialize_metadata(metadata: dataobjects.Metadata) -> str:
    """Serialize metadata into json"""
    return json.dumps(asdict(metadata), indent=4)


def deserialize_metadata(file: TextIOWrapper) -> dataobjects.Metadata:
    """Read file and returned deserialized metadata"""
    return dataobjects.Metadata.map(json.load(file))


# colors
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"


def print_red(data: str, end="\n"):
    """Print in red color"""
    print(f"{COLOR_RED}{data}\033[0;0m", end=end)


def print_equal(data):
    """Print format when equal"""
    print("  " + data, end="")


def print_remove(data):
    """Print format when removing"""
    print_red(f"- {data}", end="")


def print_add(data):
    """Print format when adding"""
    print(f"{COLOR_GREEN}+ {data}\033[0;0m", end="")
