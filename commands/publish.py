"""Publisher module"""

import config
from commands import base_command
from utils import path_utils
from utils.format_utils import markdown_format, pdf_format


class PublishCommand(base_command.IRunnable):
    """Publish command"""

    def __init__(self, subparsers) -> None:
        self.parser = subparsers.add_parser(
            "publish", help="Command for publishing documents"
        )
        self.parser.add_argument(
            "-p", "--path", nargs="+", required=True, help="Path of files or dirs"
        )
        self.parser.add_argument(
            "-f", "--format", required=True, help="Format of the file"
        )
        self.parser.add_argument("-t", "--template", help="Path to template file")

        self.parser.set_defaults(func=self.run)

    def run(self, args):
        publish(args.path, args.format, args.template)


def publish(paths: list[str], format_type: str, template: str | None):
    """Publish markdown files to output location"""

    files = path_utils.get_files_from_paths_by_extension(paths, ".md")

    if not files:
        print("No files to publish")
        return

    config.path_publish.mkdir(exist_ok=True, parents=True)

    for file_path in files:
        parse_file(path=file_path, format_type=format_type, template=template)


def parse_file(path: str, format_type: str, template: str | None) -> str:
    """Parse file by determining format and return path to ouput file"""

    if format_type == "md":
        return markdown_format.output_file(path=path)
    elif format_type == "pdf":
        return pdf_format.output_file(path=path, template=template)

    raise ValueError(f"Unknown format type: {format_type}")
