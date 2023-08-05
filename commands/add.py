"""Add module"""

import uuid
import os
from datetime import datetime
from pathlib import Path
import config
from commands import base_command, version, diff
from utils import path_utils, parsing_utils


class AddCommand(base_command.IRunnable):
    """Add command"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser("add", help="Add file to stage")
        self.parser.add_argument(
            "-p", "--path", nargs="+", required=True, help="Path of files or dirs"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        add(args.path)


def get_file_changes(file: str):
    """makes diff between argument file and a built file from logs"""
    with open(config.path_meta, "r", encoding=config.ENCODING) as meta_file:
        metadata = config.deserialize_metadata(meta_file)

        logs = version.get_file_version_logs(
            file=file, version_name=metadata.current_version, metadata=metadata
        )

        list_first = parsing_utils.list_from_logs(logs)

        return diff.diff(list_first=list_first, name_second=file)


def handle_staged_file(file: str, metadata: config.dataobjects.Metadata) -> None:
    """updates existing file in stage"""
    updated_stage = []

    for log in metadata.stage:
        if log.source == file:
            if os.path.isfile(log.path):
                os.remove(log.path)
        else:
            updated_stage.append(log)

    metadata.stage = updated_stage


def add(paths: list[str]):
    """Add new file or directory to stage"""

    files = path_utils.get_files_from_paths(paths)

    if not files:
        return

    with open(config.path_meta, "r+", encoding=config.ENCODING) as meta_file:
        metadata = config.deserialize_metadata(meta_file)

        is_changed = False

        for file in files:
            changes = get_file_changes(file)

            if not changes:
                continue

            is_changed = True

            handle_staged_file(file=file, metadata=metadata)

            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            target = Path(f".vc/logs/{timestamp}_{file}.{config.LOG_EXTENSION}")

            target.parent.mkdir(exist_ok=True, parents=True)
            target.write_text(str(changes), encoding=config.ENCODING)

            metadata.stage.append(
                config.dataobjects.Log(
                    uuid=str(uuid.uuid4()),
                    operation=add.__name__,
                    source=str(file),
                    path=str(target),
                    created_at=timestamp,
                )
            )

        if not is_changed:
            return

        meta_file.seek(0)
        meta_file.write(config.serialize_metadata(metadata))
        meta_file.truncate()
