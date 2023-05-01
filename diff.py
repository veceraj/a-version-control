import config
import json
from _diff import diff as _diff
from _patch import patch
from join import build_from_logs
from version import file_version_logs


class DiffCommand:
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
        # print(patched == second)
        print("".join(patched))

    return log


def diff_versions(nameFirst: str, nameSecond: str, file: str):
    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        logsFirst = file_version_logs(file=file, version_name=nameFirst, data=data)
        logsSecond = file_version_logs(file=file, version_name=nameSecond, data=data)

        old = build_from_logs(logsFirst)
        new = build_from_logs(logsSecond)
        log = _diff(old, new, is_print=True)

    return log
