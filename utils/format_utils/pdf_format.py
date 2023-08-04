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
        "-o",
        str(output_path),
        str(markdown_output_path),
        "--no-highlight",
    ]

    # pandoc, pandoc-crossref, pdflatex

    if template:
        command.extend(["--template", template])

    subprocess.run(" ".join(command), shell=True, check=False)

    return output_path
