from pathlib import Path

path_meta = Path(".vc/metadata.json")
path_ignore = Path(".vcignore")

ADD = "add"
REMOVE = "remove"

commands = {
    "init": "InitCommand",
    "add": "AddCommand",
    "checkout": "CheckoutCommand",
    "commit": "CommitCommand",
    "diff": "DiffCommand",
    "version": "VersionCommand",
    "reset": "ResetCommand",
    "stash": "StashCommand",
    # "mv": "MvCommand",
    # internal
    "join": "JoinCommand",
    "patch": "PatchCommand",
}

# colors
color_red = "\033[31m"
color_green = "\033[32m"
color_orange = "\033[33m"


def printEqual(data):
    print("  " + data, end="")


def printRemove(data):
    print(f"\033[31m- {data}\033[0;0m", end="")


def printAdd(data):
    print(f"\033[32m+ {data}\033[0;0m", end="")
