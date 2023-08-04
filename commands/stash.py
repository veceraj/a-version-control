import config
from commands import base_command
from pathlib import Path


class StashCommand(base_command.IRunnable):
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "stash", help="Stash files or apply stash and list stashes"
        )
        self.parser.add_argument("-a", "--apply", help="Apply stash by name")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all stashes"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if args.list == True:
            stash_list()
            return

        if args.apply:
            apply_stash(args.apply)
            return

        stash()
        return


def stash_list() -> None:
    with open(config.path_meta, "r") as f:
        metadata = config.deserialize_metadata(f)
        names = list(map(lambda stash: stash.name, metadata.stash))

        if len(names):
            print(names)
        else:
            print("Stash is empty")


def get_stash(
    stash_name: str, metadata: config.dataobjects.Metadata
) -> config.dataobjects.Version | None:
    return next((stash for stash in metadata.stash if stash.name == stash_name), None)


def apply_stash(stash_name) -> None:
    with open(config.path_meta, "r+") as f:
        metadata = config.deserialize_metadata(f)

        found_stash = get_stash(stash_name=stash_name, metadata=metadata)

        if found_stash == None:
            print("Stash not found")
            return

        for item in found_stash.logs:
            stashed_file = Path(item.path)
            target = Path(item.source)
            target.write_text(stashed_file.read_text())


def stash() -> None:
    # get version
    # generate name
    # stash all files
    # clear logs
    print("stash")
