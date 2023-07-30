"""Commit module"""

import uuid
from copy import deepcopy
from datetime import datetime
import config
import command
import dataobjects
import diff
import inverse
import version


class CommitCommand(command.IRunnable):
    """Commit command"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "commit", help="Commit stage with message to specified versions"
        )
        self.parser.add_argument(
            "-d",
            "--dry-run",
            action="store_true",
            help="Whether to run in dry-run mode",
        )
        self.parser.add_argument(
            "-m", "--message", required=True, help="Message for the commit"
        )

        group = self.parser.add_mutually_exclusive_group(required=True)

        group.add_argument(
            "-v",
            "--versions",
            nargs="+",
            help="Versions to apply the commits to",
        )
        group.add_argument(
            "-all",
            "--all-versions",
            action="store_true",
            help="Apply to current version and all following",
        )

        self.parser.set_defaults(func=self.run)

    def run(self, args):
        make_commit(
            message=args.message, version_names=args.versions, dry_run=args.dry_run
        )


def make_commit(message: str, version_names: list[str] | None, dry_run: bool):
    """Make a new commit from stage. Cannot be applied to previous versions.
    In order to make a commit - needs to be checked out in specific version"""

    with open(config.path_meta, "r+", encoding=config.ENCODING) as file:
        metadata = config.deserialize_metadata(file)

        if not metadata.stage:
            print("Nothing to commit")
            return

        if version_names is None:
            version_names = [
                metadata.current_version,
                *version.get_following_version_names(
                    metadata.current_version, metadata
                ),
            ]

        if metadata.current_version not in version_names:
            print("Current version needs to be present")
            return

        if contains_previous_versions(version_names, metadata):
            print("It is not possible to commit to previous versions")
            return

        if contains_nonexisting_versions(version_names, metadata):
            print("Non existing version provided")
            return

        current_version = version.get_version(
            version_name=metadata.current_version, metadata=metadata
        )

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        new_commit = dataobjects.Commit(
            message=message,
            uuid=str(uuid.uuid4()),
            logs=metadata.stage,
            created_at=timestamp,
        )

        if dry_run:
            commit_dry_run(
                metadata=metadata,
                new_commit=new_commit,
                current_version=current_version,
                version_names=version_names,
            )
            return

        current_version.commits.append(new_commit)

        inverse.handle_inverse(message, version_names, metadata)

        metadata.stage = []

        file.seek(0)
        file.write(config.serialize_metadata(metadata))
        file.truncate()


def contains_previous_versions(
    version_names: list, metadata: dataobjects.Metadata
) -> bool:
    """Check if version names are present in previous versions"""
    first = set(version_names)
    second = set(version.get_previous_version_names(metadata))
    return bool(len(first.intersection(second)))


def contains_nonexisting_versions(
    version_names: list, metadata: dataobjects.Metadata
) -> bool:
    """Check if version names exist"""
    first = set(version_names)
    second = set(version.get_all_version_names(metadata))

    return bool(len(first.difference(second)))


def commit_dry_run(
    metadata: dataobjects.Metadata,
    new_commit: dataobjects.Commit,
    current_version: dataobjects.Version,
    version_names: list,
) -> None:
    """Handle dry run for commit by making duplicit metadata object
    that does not contain the new commit"""
    duplicate_metadata = deepcopy(metadata)
    current_version.commits.append(new_commit)

    for version_name in version_names:
        print(f"Version: {version_name}:")

        old_logs = version.get_version_logs(
            version_name=version_name, metadata=duplicate_metadata
        )
        new_logs = version.get_version_logs(
            version_name=version_name, metadata=metadata
        )

        for stage_log in metadata.stage:
            print(f"--- Source: {stage_log.source}: ---")

            diff.print_diff_from_logs(
                logs_first=old_logs[stage_log.source],
                logs_second=new_logs[stage_log.source],
            )

            print("\n--- End of source ---")
        print("")
