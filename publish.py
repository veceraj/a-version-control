"""Publisher module"""

import command
import config
from utils import path_utils, markdown_utils


class PublishCommand(command.IRunnable):
    """Publish command"""

    def __init__(self, subparsers) -> None:
        self.parser = subparsers.add_parser(
            "publish", help="Command for publishing documents"
        )
        self.parser.add_argument(
            "-p", "--path", nargs="+", required=True, help="Path of files or dirs"
        )

        self.parser.set_defaults(func=self.run)

    def run(self, args):
        publish(args.path)


def publish(paths: list[str]):
    """Publish markdown files to output location"""

    files = path_utils.get_files_from_paths_by_extension(paths, ".md")

    if not files:
        print("No files to publish")
        return

    config.path_publish.mkdir(exist_ok=True, parents=True)

    for file_path in files:
        content = markdown_utils.parse_file(path=file_path)

        with open(
            config.path_publish.joinpath(file_path), "w", encoding=config.ENCODING
        ) as file:
            file.write(content)
