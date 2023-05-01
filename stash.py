import config
import json
import uuid
from join import build_from_logs
from version import get_version_name, version_logs
from datetime import datetime
from pathlib import Path


class StashCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "stash", help="Stash files or apply stash and list stashes"
        )
        self.parser.add_argument("-a", "--apply", help="Apply stash id")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all stashes"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if args.list == True:
            print(stash_list())
            return

        if args.apply:
            apply_stash(args.apply)
            return

        # with open(config.path_meta, "r+") as f:
        #     data = json.load(f)

        #     stash(data)

        #     f.seek(0)
        #     json.dump(data, f, indent=4)
        #     f.truncate()
        #     return


def ignored():
    if not config.path_ignore.is_file():
        return []

    with config.path_ignore.open() as f:
        return f.read().splitlines()


def get_stash(stash_name: str, data: dict):
    return next(
        (stash for stash in data["stash"] if stash["name"] == stash_name),
        None,
    )


def apply_stash(stash_name: str):
    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        stash = get_stash(stash_name=stash_name, data=data)

        for stash in stash["logs"]:
            stashed_file = Path(stash["path"])
            target = Path(stash["source"])
            target.write_text(stashed_file.read_text())

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def add_stash(data, stash_name: str, log):
    stash = get_stash(stash_name=stash_name, data=data)

    if stash == None:
        data["stash"].append(
            {"name": stash_name, "uuid": str(uuid.uuid4()), "logs": [log]}
        )
    else:
        stash["log"].append(log)


def stash_file(data, stash_name, file, logs):
    if not len(logs):
        return

    with open(file, "r") as f:
        old_file = f.read()
        new_file = "".join(build_from_logs(logs))

        if old_file == new_file:
            return

        target = Path(f".vc/stash/{stash_name}/{file}.stash")

        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_text(old_file)

        add_stash(
            data=data,
            stash_name=stash_name,
            log={
                "uuid": str(uuid.uuid4()),
                "operation": stash.__name__,
                "source": str(file),
                "path": str(target),
            },
        )


# TODO: on checkout fail if not specified that it should stash
def stash(data):
    current_version = get_version_name()

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    stash_name = f"{current_version}_{timestamp}"

    for file, logs in version_logs(version_name=current_version, data=data).items():
        stash_file(data, stash_name, file, logs)


def stash_list():
    with config.path_meta.resolve().open() as f:
        data = json.load(f)
        return list(map(lambda stash: stash["name"], data["stash"]))
