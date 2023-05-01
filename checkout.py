import config
import json

from join import build_from_logs
from version import get_version, version_logs, new_version
from stash import stash


class CheckoutCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "checkout", help="Checkout to new or existing version"
        )
        self.parser.add_argument(
            "-v", "--version", required=True, help="Name of the version"
        )
        self.parser.add_argument(
            "-f",
            "--from-version",
            help="Name of the version from which is being created, is ignored if branch already exists. If provided non existent, creates empty. If not provided creates from current.",
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        checkout(version=args.version, from_version=args.from_version)


def update_files(version_name: str, data: dict):
    for file, logs in version_logs(version_name, data).items():
        if not len(logs):
            continue
        else:
            with open(file, "w") as f:
                for line in build_from_logs(logs):
                    f.write(line)


def checkout(version: str, from_version: str = None):
    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        is_version = get_version(version, data)

        if is_version == None:
            id = new_version(version, from_version, data)

            if id == None:
                print("error while creaing new version")
                return

        if not is_version == None and not version == data["current_version"]:
            stash(data)
            update_files(version, data)

        data["current_version"] = version

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
