import config
import json
import uuid
from os import rename
from version import get_version_name, get_version


def mv(source: str, target: str, message: str) -> None:
    rename(source, target)

    with open(config.path_meta, "r+") as f:
        data = json.load(f)

        current_version = get_version(version_name=get_version_name(), data=data)

        # TODO: update to new strucutre
        current_version["logs"].append(
            {
                "uuid": str(uuid.uuid4()),
                "operation": mv.__name__,
                "source": source,
                "target": target,
                "message": message,
            }
        )

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
