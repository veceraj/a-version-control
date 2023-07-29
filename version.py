"""Version module"""
from collections import defaultdict
from datetime import datetime
import uuid
import config
import command
import dataobjects


class VersionCommand(command.IRunnable):
    """Version Command"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser("version", help="Get current version")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all versions"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        with open(config.path_meta, "r", encoding="utf-8") as file:
            metadata = config.deserialize_metadata(file)

            if args.list:
                print(get_all_version_names(metadata))
                return

            print(metadata.current_version)


def get_all_version_names(metadata: dataobjects.Metadata) -> list[str]:
    """Get all version names in order"""
    return list(map(lambda v: v.name, metadata.versions))


def get_previous_version_names(metadata: dataobjects.Metadata) -> list[str]:
    """Get list of presious version names"""
    version_list = get_all_version_names(metadata)
    current_index = version_list.index(metadata.current_version)
    return version_list[:current_index]


def get_following_version_names(
    version_name: str, metadata: dataobjects.Metadata
) -> list[str]:
    """Get list of following version names"""
    version_list = get_all_version_names(metadata)

    current_index = version_list.index(version_name)
    return version_list[current_index + 1 :]


def get_version(
    version_name: str, metadata: dataobjects.Metadata
) -> dataobjects.Version | None:
    """Get Version by name"""
    return next(
        (version for version in metadata.versions if version.name == version_name), None
    )


def create_version(
    version_name: str, commits: list[dataobjects.Commit] = None
) -> dataobjects.Version:
    """Make new instance of Version"""

    if commits is None:
        commits = []

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    return dataobjects.Version(
        name=version_name, uuid=str(uuid.uuid4()), commits=commits, created_at=timestamp
    )


def get_version_index(version_name: str, metadata: dataobjects.Metadata):
    """Get index of version in version list"""
    return next(
        (
            index
            for (index, version) in enumerate(metadata.versions)
            if version.name == version_name
        ),
        None,
    )


# TODO: can be refactored to parent_id structure
def get_version_logs(version_name: str, metadata: dataobjects.Metadata):
    """Get logs for a version"""
    files = defaultdict(list)

    index = get_version_index(version_name, metadata)

    if index is None:
        return files

    for version in metadata.versions[: index + 1]:
        for commit in version.commits:
            for log in commit.logs:
                files[log.source].append(log)

    # sort_version_logs_by_timestamp(files)

    return files


def sort_version_logs_by_timestamp(files):
    """Sort logs by timestamp in path"""
    for _, logs in files.items():
        # timestamp is on first position
        logs.sort(key=lambda x: x.path)


def get_file_version_logs(
    file: str, version_name: str, metadata: dataobjects.Metadata
) -> list[dataobjects.Log]:
    """ "Get version log by file"""
    return get_version_logs(version_name, metadata)[file]
