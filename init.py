import json
import config
from checkout import checkout


class InitCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser("init", help="Initialize the repository")
        self.parser.add_argument(
            "-v", "--version-name", required=True, help="Name of the version"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        init(args.version_name)


def init(versionName: str) -> None:
    if config.path_meta.is_file():
        print("Version Control already initialized.")
        return

    metadata = {
        "current_version": versionName,
        "commits": {},
        "stage": [],
        "stash": [],
        "versions": [],
    }

    config.path_meta.parent.mkdir(exist_ok=True, parents=True)
    config.path_meta.write_text(json.dumps(metadata, indent=4))

    checkout(version=versionName)
