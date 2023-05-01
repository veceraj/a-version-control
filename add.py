import config
import json
import uuid
from diff import diff
from join import build_from_logs
from datetime import datetime
from pathlib import Path
from version import file_version_logs, get_version_name


class AddCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser("add", help="Add new file to stage")
        self.parser.add_argument("-p", "--path", required=True, help="Path of the file")
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        add(args.path)


def get_file_changes(file: str):
    with open(config.path_meta, "r") as f:
        data = json.load(f)
        logs = file_version_logs(file=file, version_name=get_version_name(), data=data)

        logs_with_stage = [*logs, *data["stage"]]

        listFirst = build_from_logs(logs_with_stage)

        changes = diff(listFirst=listFirst, nameSecond=file)

        return changes


def add_log(log):
    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        data["stage"].append(log)

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


# TODO: handle add same file - with and without changes in same commit
# TODO: handle multiple files and directories
def add(file: str):
    changes = get_file_changes(file)

    if not changes:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    target = Path(f".vc/logs/{timestamp}_{file}.diff_log")

    target.parent.mkdir(exist_ok=True, parents=True)
    target.write_text(str(changes))

    add_log(
        {
            "uuid": str(uuid.uuid4()),
            "operation": add.__name__,
            "source": str(file),
            "path": str(target),
        }
    )
