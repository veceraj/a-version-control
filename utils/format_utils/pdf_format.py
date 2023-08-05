"""Pdf utility module"""

import os
import subprocess
import config
from utils.format_utils import markdown_format


def output_file(path: str, template: str | None = None) -> str:
    """Save PDF file to publishing output directory"""

    markdown_output_path = markdown_format.output_file(path)

    path_without_extension, _ = os.path.splitext(path)

    output_path = config.path_publish.joinpath(path_without_extension + ".pdf")

    command = [
        "pandoc",
        "--number-sections",
        "--filter",
        "pandoc-crossref",
        "--no-highlight",
    ]

    # pandoc, pandoc-crossref, pdflatex

    original_directory = os.getcwd()

    if template:
        new_directory = os.path.dirname(template)
        os.chdir(new_directory)

        # paths relative to the new directory
        relative_output_path = os.path.normpath(os.path.join("..", str(output_path)))
        relative_markdown_output_path = os.path.normpath(
            os.path.join("..", str(markdown_output_path))
        )

        command.extend(
            [
                "-o",
                relative_output_path,
                relative_markdown_output_path,
                "--template",
                os.path.basename(template),
            ]
        )
    else:
        command.extend(["-o", str(output_path), str(markdown_output_path)])

    subprocess.run(" ".join(command), shell=True, check=False)

    os.chdir(original_directory)

    return output_path
