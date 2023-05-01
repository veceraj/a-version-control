import config
import ast
import os
from _join import join as _join
from _patch import patch
from _diff import diff
from pathlib import Path


class JoinCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "join", help="Internal: Join multiple logs. Provide specific log files."
        )
        self.parser.add_argument(
            "-l",
            "--logs",
            nargs="+",
            required=True,
            help="Logs to join",
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        join_files(args=args.logs)


def join_files(args: list):
    basenames = []
    joined = []

    for arg in args:
        with open(arg, "r") as f:
            dir = os.path.dirname(f.name)
            basenames.append(os.path.basename(f.name))
            log_str = f.read()
            log = ast.literal_eval(log_str)
            joined = _join(joined, log)

    path = f"{dir}/join_{'_'.join(basenames)}.diff_log"

    output_file = Path(path)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(str(joined))


def build_from_logs(logs: list):
    finalLog = []

    for log in logs:
        path = Path(log["path"])
        difflog = ast.literal_eval(path.open().read())
        finalLog = _join(finalLog, difflog)

    return patch([], finalLog)
