"""Checkout module"""

import config
import command
import parsing
from version import get_version, create_version, get_version_logs


class CheckoutCommand(command.IRunnable):
    """Checkout command"""

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
            help="""
                Name of the version from which is being created.
                Is ignored if branch already exists.
                If provided non existent, creates empty. If not provided creates from current.
            """,
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        checkout(version_name=args.version, from_version_name=args.from_version)


def checkout(
    version_name: str,
    from_version_name: str = None,
    ignore_current_version: bool = False,
):
    """Checkout to new branch or create new branch

    Can specify from which version is being creating by placing it as following"""
    with open(config.path_meta, "r+", encoding=config.ENCODING) as file:
        metadata = config.deserialize_metadata(file)

        if version_name == metadata.current_version and not ignore_current_version:
            print(f"Already on version {version_name}")
            return

        version = get_version(version_name, metadata)

        if version is None:
            version = create_version(version_name)

            if from_version_name is None:
                metadata.versions.append(version)
            else:
                index = next(
                    (
                        index
                        for (index, version) in enumerate(metadata.versions)
                        if version.name == from_version_name
                    ),
                    None,
                )

                if index is None:
                    print(f"Version {from_version_name} does not exist")
                    return

                metadata.versions.insert(index + 1, version)

        else:
            # stash(metadata)
            update_files(version_name, metadata)

        metadata.current_version = version_name

        file.seek(0)
        file.write(config.serialize_metadata(metadata))
        file.truncate()


def update_files(version_name: str, metadata: config.dataobjects.Metadata):
    """Update files conent based on checked out version"""
    version_logs = get_version_logs(version_name=version_name, metadata=metadata)

    for str_file, logs in version_logs.items():
        if logs:
            with open(str_file, "w", encoding=config.ENCODING) as file:
                for line in parsing.list_from_logs(logs):
                    file.write(line)
