"""Diff module"""

import config
import command
import parsing
import version
from _diff import diff as _diff
from _patch import patch


class DiffCommand(command.IRunnable):
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
                nameFirst=args.from_version,
                nameSecond=args.to_version,
                printPatch=True,
            )
            print(log)
            return

        diff_versions(args.from_version, args.to_version, args.path)


def diff(
    nameFirst=None,
    nameSecond=None,
    listFirst: list = [],
    listSecond: list = [],
    printPatch: bool = False,
):
    if nameFirst:
        with open(nameFirst, "r") as f:
            first = f.readlines()
    else:
        first = listFirst

    if nameSecond:
        with open(nameSecond, "r") as f:
            second = f.readlines()
    else:
        second = listSecond

    log = _diff(first, second)

    if printPatch:
        patched = patch(first, log)
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
    list_first = parsing.list_from_logs(logs_first)
    list_second = parsing.list_from_logs(logs_second)

    _diff(list_first, list_second, is_print=True)
