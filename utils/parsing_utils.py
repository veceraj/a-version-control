"""Module for handling parsing between structures"""

import ast
import config
from utils import patch_utils


def list_from_logs(logs: list[config.dataobjects.Log]) -> list:
    """build file as a list from tuple list of tuples (version_name, log)"""
    final = []

    timestamp_difflogs = []

    for i, log in enumerate(logs):
        with open(log.path, "r", encoding=config.ENCODING) as file:
            timestamp_difflogs.append((log.created_at, ast.literal_eval(file.read())))

    offset = 0

    # change line if determined that it needs to be changed
    for i, (created_at, difflog) in enumerate(timestamp_difflogs):
        # difflogs that have been created after the current one but are from previous versions
        difflogs_after = []
        for j, (compared_created_at, compared_log) in enumerate(timestamp_difflogs[:i]):
            if j < i and compared_created_at > created_at:
                # currently iterated j is before i but its log is created later
                difflogs_after.extend(compared_log)  # extend/append

        updated_difflog = []

        for operation, line, payload in difflog:
            current_offset = 0

            for compared_operation, compared_line, _ in difflogs_after:
                if compared_line <= line:
                    if compared_operation == config.ADD:
                        current_offset += 1
                        line += 1
                        # line += 1 + offset
                    elif compared_operation == config.REMOVE:
                        current_offset -= 1
                        line -= 1
                        # line -= 1 + offset

            updated_difflog.append((operation, line, payload))

        offset += current_offset

        # for each iteration apply difflog to update the file
        final = patch_utils.patch(final, updated_difflog)

    return final
