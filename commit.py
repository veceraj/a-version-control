import config
import helper
import json
import uuid
from datetime import datetime
from pathlib import Path
from version import get_version, get_version_name
from _diff import diff


class CommitCommand:
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
        self.parser.add_argument(
            "-v",
            "--versions",
            nargs="+",
            required=True,
            help="Versions to apply the commits to",
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        commit(message=args.message, versions=args.versions, dry_run=args.dry_run)


# TODO: refactor this function into smaller parts after deciding reusability of functions
def commit_to_version(version_name: str, data: dict, message: str, dry_run: bool):
    version = get_version(version_name, data)

    if version == None:
        print(f"\nVersion {version_name} does not exist.")
        return

    target_commit_ids = version["logs"]

    if dry_run:
        print(f"\nVersion: {version_name}")
        target_commit_logs = helper.commit_logs_from_commit_ids(target_commit_ids, data)
        grouped_target = helper.group_by_key(target_commit_logs, "source")

    current_version = get_version(get_version_name(), data)
    current_commit_ids = current_version["logs"]

    invert_commit_ids = [id for id in current_commit_ids if id not in target_commit_ids]
    add_commit_ids = [id for id in target_commit_ids if id not in current_commit_ids]

    # TODO: check if it should be reversed
    invert_commit_logs = helper.commit_logs_from_commit_ids(invert_commit_ids, data)
    invert_commit_logs.reverse()

    add_commit_logs = helper.commit_logs_from_commit_ids(add_commit_ids, data)

    grouped_invert = helper.group_by_key(invert_commit_logs, "source")
    grouped_add = helper.group_by_key(add_commit_logs, "source")

    grouped_stage = helper.group_by_key(data["stage"], "source")

    calculated_commit_logs = []

    for source, stage_commit_logs in grouped_stage.items():
        diff_logs = helper.diff_logs_from_commit_logs(stage_commit_logs)

        invert_diff_logs = helper.diff_logs_from_commit_logs(grouped_invert[source])
        add_diff_logs = helper.diff_logs_from_commit_logs(grouped_add[source])

        recalculated_logs = []

        for operation, line, payload in diff_logs:
            # TODO: check if it should handle index increase - example in freeform
            invert_before_line = [log for log in invert_diff_logs if log[1] < line]

            count = 0

            for operation_invert, _, _ in invert_before_line:
                if operation_invert == config.ADD:
                    count -= 1
                elif operation_invert == config.REMOVE:
                    count += 1

            increment = 0

            # TODO: the algorithm actualy goes step by step but can be as below (same for invert)
            # for add_commit_log_by_source in grouped_add[source]:
            #     add_diff_logs = helper.diff_logs_from_commit_log(
            #         add_commit_log_by_source
            #     )

            # for operation_add, line_add, _ in add_diff_logs:
            #     print(operation_add, line_add, line)

            for operation_add, line_add, _ in add_diff_logs:
                if line_add <= line + increment:
                    increment += 1
                    if operation_add == config.ADD:
                        count += 1
                    elif operation_add == config.REMOVE:
                        count -= 1

            recalculated_logs.append((operation, line + count, payload))

        if dry_run:
            print(f"Source: {source}:")

            old = helper.diff_logs_from_commit_logs(grouped_target[source])

            diff(
                helper.build_from_diff_logs(old),
                helper.build_from_diff_logs([*old, *recalculated_logs]),
                is_print=True,
            )
            print("")

            continue

        # no need to create new file for current version
        if get_version_name() == version_name:
            calculated_commit_logs = data["stage"]
            continue

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        target = Path(f".vc/logs/{timestamp}_{version_name}_{source}.diff_log")
        target.parent.mkdir(exist_ok=True, parents=True)
        target.write_text(str(recalculated_logs))

        calculated_commit_logs.append(
            {
                "uuid": str(uuid.uuid4()),
                "operation": commit.__name__,
                "source": str(source),
                "path": str(target),
            }
        )

    id = str(uuid.uuid4())

    calculated_commit = {
        "id": id,
        "version": version_name,
        "message": message,
        "logs": calculated_commit_logs,
    }

    data["commits"][id] = calculated_commit
    version["logs"].append(id)


def commit(message: str, versions: list, dry_run: bool):
    if not len(versions):
        print("specify at least one version")
        return

    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        if not len(data["stage"]):
            print("nothing to commit")
            return

        for version_name in versions:
            commit_to_version(
                version_name=version_name, data=data, message=message, dry_run=dry_run
            )

        data["stage"] = []

        if not dry_run:
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
