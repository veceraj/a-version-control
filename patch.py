import ast
from _patch import patch as _patch
from pathlib import Path


class PatchCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "patch", help="Internal: Patch file by log and place it in output"
        )
        self.parser.add_argument(
            "-p", "--path-original", required=True, help="Path of the version"
        )
        self.parser.add_argument(
            "-l", "--path-log", required=True, help="Path of the version"
        )
        self.parser.add_argument(
            "-o", "--path-output", required=True, help="Path of the version"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        patch(args.path_original, args.path_log, args.path_output)


def patch(nameOriginal, nameLog, nameOutput):
    with open(nameOriginal, "r") as f:
        original = f.readlines()

    with open(nameLog, "r") as f:
        log_str = f.read()

    # covnert to list
    log = ast.literal_eval(log_str)

    patched = _patch(original, log)

    output_file = Path(nameOutput)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    with open(nameOutput, "w") as f:
        f.writelines(patched)
