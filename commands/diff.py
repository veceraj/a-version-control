"""Diff module"""

import config
from commands import base_command, version
from utils import diff_utils, patch_utils, parsing_utils


class DiffCommand(base_command.IRunnable):
    """Diff command"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "diff", help="Diff between two version for specified file"
        )
        self.parser.add_argument(
            "-f", "--from-version", required=True, help="Name of from version"
        )
        self.parser.add_argument(
            "-t", "--to-version", required=True, help="Name of to version"
        )
        self.parser.add_argument("-p", "--path", help="The path of the file")
        self.parser.add_argument(
            "--files",
            action="store_true",
            help="Whether to run diff on two files with -f and -t arguments. Ignores the -p attribute. \nExample: diff --files -f file1 -t file2",
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if not args.files and not args.path:
            print(
                "The -p/--path argument is required unless argument --files is present"
            )
            return

        if args.files:
            log = diff(
                name_first=args.from_version,
                name_second=args.to_version,
                print_patch=True,
            )
            print(log)
            return

        diff_versions(args.from_version, args.to_version, args.path)


def diff(
    name_first=None,
    name_second=None,
    list_first: list = None,
    list_second: list = None,
    print_patch: bool = False,
):
    """Diff function that hadnles multiple scenarios"""

    if list_first is None:
        list_first = []

    if list_second is None:
        list_second = []

    if name_first:
        with open(name_first, "r", encoding=config.ENCODING) as f:
            first = f.readlines()
    else:
        first = list_first

    if name_second:
        with open(name_second, "r", encoding=config.ENCODING) as f:
            second = f.readlines()
    else:
        second = list_second

    log = diff_utils.diff(first, second)

    if print_patch:
        patched = patch_utils.patch(first, log)
        print("".join(patched))

    return log


def diff_versions(name_first: str, name_second: str, source: str):
    """Print diff between two versions"""
    with open(config.path_meta, "r+", encoding=config.ENCODING) as file:
        metadata = config.deserialize_metadata(file)

        logs_first = version.get_file_version_logs(
            file=source, version_name=name_first, metadata=metadata
        )
        logs_second = version.get_file_version_logs(
            file=source, version_name=name_second, metadata=metadata
        )

        print_diff_from_logs(logs_first, logs_second)


def print_diff_from_logs(
    logs_first: list[config.dataobjects.Log], logs_second: list[config.dataobjects.Log]
) -> None:
    """Print changes from list of logs"""
    list_first = parsing_utils.list_from_logs(logs_first)
    list_second = parsing_utils.list_from_logs(logs_second)

    diff_utils.diff(list_first, list_second, is_print=True)
