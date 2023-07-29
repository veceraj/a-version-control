"Dataobjects module"
from dataclasses import dataclass
from typing import Self


@dataclass
class Log:
    """Class for representation of each log."""

    uuid: str
    operation: str
    source: str
    path: str
    created_at: str

    @staticmethod
    def map(data: dict) -> Self:
        """Log mapper"""
        return Log(**data)


@dataclass
class Commit:
    """Class for representation of each commit. Also used for stash."""

    message: str
    uuid: str
    created_at: str
    logs: list[Log]

    @staticmethod
    def map(data: dict) -> Self:
        """Commit mapper"""
        return Commit(
            message=data["message"],
            uuid=data["uuid"],
            logs=[Log.map(log) for log in data["logs"]],
            created_at=data["created_at"],
        )


@dataclass
class Version:
    """Class for representation of each version."""

    name: str
    uuid: str
    created_at: str
    commits: list[Commit]

    @staticmethod
    def map(data: dict) -> Self:
        """Version mapper"""
        return Version(
            name=data["name"],
            uuid=data["uuid"],
            created_at=data["created_at"],
            commits=[Commit.map(commit) for commit in data["commits"]],
        )


@dataclass
class Metadata:
    """Class for representation of all versions."""

    current_version: str
    stage: list[Log]
    stash: list[Commit]
    versions: list[Version]

    @staticmethod
    def map(data: dict) -> Self:
        """Metadata mapper"""
        return Metadata(
            current_version=data["current_version"],
            stage=[Log.map(log) for log in data["stage"]],
            stash=[Commit.map(stash) for stash in data["stash"]],
            versions=[Version.map(version) for version in data["versions"]],
        )
