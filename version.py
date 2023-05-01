import config
import json
import uuid
from collections import defaultdict


class VersionCommand:
    def __init__(self, subparsers):
        self.parser = subparsers.add_parser("version", help="Get current version")
        self.parser.add_argument(
            "-l", "--list", action="store_true", help="List all versions"
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if args.list == True:
            print(all_versions())
            return

        print(get_version_name())


def get_version_name() -> str:
    with config.path_meta.resolve().open() as f:
        data = json.load(f)
        f.close
        return data["current_version"]


def all_versions() -> list:
    with config.path_meta.resolve().open() as f:
        data = json.load(f)
        f.close
        return list(map(lambda v: v["name"], data["versions"]))


def get_version(version_name: str, data: dict) -> dict | None:
    return next(
        (version for version in data["versions"] if version["name"] == version_name),
        None,
    )


def new_version(version_name: str, from_version_name: str, data: dict) -> str | None:
    logs = []

    if from_version_name == None:
        from_version = get_version(get_version_name(), data)
    else:
        from_version = get_version(from_version_name, data)

    if not from_version == None:
        logs = from_version["logs"]

    id = str(uuid.uuid4())

    data["versions"].append({"name": version_name, "uuid": id, "logs": logs})

    return id


def version_logs(version_name: str, data: dict, ignored_commits: list = []):
    version = get_version(version_name=version_name, data=data)

    files = defaultdict(list)

    for commit_id in version["logs"]:
        if commit_id in ignored_commits:
            continue

        for log in data["commits"][commit_id]["logs"]:
            source = log["source"]
            files[source].append(log)

    return files


def file_version_logs(
    file: str, version_name: str, data: dict, ignored_commits: list = []
):
    return version_logs(version_name, data, ignored_commits)[file]
