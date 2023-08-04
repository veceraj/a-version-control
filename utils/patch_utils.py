"""Utility module for patch"""

import config


def add(data: list, line: int, payload):
    """Add line to data"""
    return data.insert(line, payload)


def remove(data: list, line: int):
    """Remove line from data"""
    return data.pop(line)


def patch(original: list, log: list) -> list:
    """Patch original with log"""
    data = original.copy()

    for operation, line, payload in log:
        if operation == config.REMOVE:
            remove(data, line)
        elif operation == config.ADD:
            add(data, line, payload)

    return data
