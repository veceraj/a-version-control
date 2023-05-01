import config
import ast
from pathlib import Path
from collections import defaultdict

from _join import join
from _patch import patch


def diff_logs_from_commit_logs(logs: list) -> list:
    """For each commit's log read file in path and join them.

    Note: commits should be previously grouped by source.
    """

    joined_logs = []

    for log in logs:
        path = Path(log["path"])
        diff_logs = ast.literal_eval(path.open().read())
        joined_logs = join(joined_logs, diff_logs)

    return joined_logs


def diff_logs_from_commit_log(log: dict) -> list:
    path = Path(log["path"])
    diff_logs = ast.literal_eval(path.open().read())
    return diff_logs


def build_from_diff_logs(logs: list) -> list:
    """Build a list of string that represent lines of code."""
    return patch([], logs)


def commit_logs_from_commit_ids(commit_ids: list, data):
    logs = []

    for commit_id in commit_ids:
        logs.extend(data["commits"][commit_id]["logs"])

    return logs


def group_by_key(data: dict, key: str) -> defaultdict:
    group = defaultdict(list)

    for item in data:
        group[item[key]].append(item)

    return group
