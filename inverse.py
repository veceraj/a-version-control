"""Inverse module with helper inverse function"""

import uuid
from datetime import datetime
from copy import deepcopy
from pathlib import Path
import ast
import config
import dataobjects
import version


def handle_inverse(
    message: str, version_names: list[str], metadata: dataobjects.Metadata
) -> None:
    """Handle inversion of commit by determinig which versions need to be inversed and which not"""

    # Inverse
    (versions_to_inverse, versions_to_reinverse) = get_versions_to_inverse(
        version_names, metadata
    )

    if versions_to_inverse:
        for version_name in versions_to_inverse:
            commit_inverse(message, version_name, metadata)

    if versions_to_reinverse:
        for version_name in versions_to_reinverse:
            commit_reinverse(message, version_name, metadata)


def get_versions_to_inverse(
    selected_versions: list, metadata: dataobjects.Metadata
) -> tuple[list[str], list[str]]:
    """Get version names that need to be inversed and re-inversed."""

    to_inverse = set()
    to_re_inverse = set()

    for version_name in selected_versions:
        following = version.get_following_version_names(version_name, metadata)
        inverse_found = False
        for follow_version in following:
            if follow_version not in selected_versions and not inverse_found:
                to_inverse.add(follow_version)
                inverse_found = True
            elif follow_version in selected_versions and inverse_found:
                to_re_inverse.add(follow_version)

    return list(to_inverse), list(to_re_inverse)


def commit_reinverse(
    message: str, version_name: str, metadata: dataobjects.Metadata
) -> None:
    """Make reinverse commit for version"""
    version_to_reinverse = version.get_version(
        version_name=version_name, metadata=metadata
    )

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    new_commit = dataobjects.Commit(
        message="Reinverse: " + message,
        uuid=str(uuid.uuid4()),
        logs=metadata.stage,
        created_at=timestamp,
    )

    version_to_reinverse.commits = [new_commit] + version_to_reinverse.commits


def commit_inverse(
    message: str, version_name: str, metadata: dataobjects.Metadata
) -> None:
    """Make inverse commit for version"""
    version_to_inverse = version.get_version(
        version_name=version_name, metadata=metadata
    )

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    new_commit = dataobjects.Commit(
        message="Inverse: " + message,
        uuid=str(uuid.uuid4()),
        logs=get_inversed_logs(metadata, version_name),
        created_at=timestamp,
    )

    version_to_inverse.commits = [new_commit] + version_to_inverse.commits


def get_inversed_logs(
    metadata: dataobjects.Metadata, version_name: str
) -> list[dataobjects.Log]:
    """Return list of inversed logs"""
    inverse_stage = deepcopy(metadata.stage)

    for log in inverse_stage:
        inverse_log(log, version_name)

    return inverse_stage


def inverse_log(log: dataobjects.Log, version_name: str) -> None:
    """Inverse log by mutating it"""

    with open(log.path, "r", encoding=config.ENCODING) as file:
        difflog = ast.literal_eval(file.read())
        inversed = inverse_difflog(log=difflog)

    path = log.path.removesuffix(f".{config.LOG_EXTENSION}")
    target = Path(f"{path}_inverse_{version_name}.{config.LOG_EXTENSION}")

    target.parent.mkdir(exist_ok=True, parents=True)
    target.write_text(str(inversed), encoding=config.ENCODING)

    log.uuid = str(uuid.uuid4())
    log.operation = "inverse"
    log.source = log.source
    log.path = str(target)


def inverse_difflog(log: list) -> list:
    """Inverese diff log opperations and order"""
    inversed = log.copy()
    inversed.reverse()
    for i, item in enumerate(inversed):
        (operation, position_old, position_new) = item
        if operation == config.REMOVE:
            inversed[i] = (config.ADD, position_old, position_new)
        elif operation == config.ADD:
            inversed[i] = (config.REMOVE, position_old, position_new)

    return inversed
