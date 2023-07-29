"""Init module"""
import config
import command
from version import create_version


class InitCommand(command.IRunnable):
    """Init command"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser("init", help="Initialize the repository")
        self.parser.add_argument(
            "-v", "--version-name", required=True, help="Name of the version"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if config.path_meta.is_file():
            print("Version Control already initialized.")
            return

        metadata = config.dataobjects.Metadata(
            current_version=args.version_name,
            stage=[],
            stash=[],
            versions=[create_version(args.version_name)],
        )

        config.path_meta.parent.mkdir(exist_ok=True, parents=True)
        config.path_meta.write_text(
            config.serialize_metadata(metadata), encoding="utf-8"
        )
