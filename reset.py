"""Reset module"""

import os
import config
import command
import checkout


class ResetCommand(command.IRunnable):
    """Reset command"""

    def __init__(self, subparsers):
        self.parser = subparsers.add_parser(
            "reset", help="Reset currently staged files based on current version"
        )
        self.parser.add_argument(
            "-p",
            "--preserve",
            action="store_true",
            help="Whether to preserve changes to files",
        )
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        reset(args.preserve)


def reset(preserve: bool):
    """Reset the stage"""
    with open(config.path_meta, "r+", encoding=config.ENCODING) as meta_file:
        metadata = config.deserialize_metadata(meta_file)

        if not metadata.stage:
            print("Nothing to reset")
            return

        if not preserve:
            checkout.checkout(
                version_name=metadata.current_version, ignore_current_version=True
            )

        for log in metadata.stage:
            if os.path.isfile(log.path):
                os.remove(log.path)

        metadata.stage = []

        meta_file.seek(0)
        meta_file.write(config.serialize_metadata(metadata))
        meta_file.truncate()
