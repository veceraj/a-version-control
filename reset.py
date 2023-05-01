import config
import json
import os
from version import get_version_name, file_version_logs
from join import build_from_logs
from pathlib import Path


class ResetCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "reset", help="Reset currently staged files"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        reset()


def reset():
    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        stage = data["stage"]

        if not len(stage):
            print("nothing to reset")
            return

        for log in stage:
            logs = file_version_logs(
                file=log["source"], version_name=get_version_name(), data=data
            )
            source = Path(log["source"])
            with open(source, "w") as file:
                file.writelines(build_from_logs(logs))

        for log in stage:
            if os.path.isfile(log["path"]):
                os.remove(log["path"])

        data["stage"] = []

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
