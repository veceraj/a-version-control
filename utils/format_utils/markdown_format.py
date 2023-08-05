"""Markdown utility module"""

import os
import re
import config
import dataobjects
from commands import version
from utils import parsing_utils


def output_file(path: str) -> str:
    """Save Markdown file to publishing output directory and return path to the file"""

    content = parse_file(path)

    output_path = config.path_publish.joinpath(path)

    with open(output_path, "w", encoding=config.ENCODING) as file:
        file.write(content)

    return output_path


def parse_file(path: str) -> str:
    """Find by patter and replace it"""

    with open(path, "r", encoding=config.ENCODING) as file:
        content = file.read()

    pattern_snippet = (
        r'<snippet path="(?P<path>[^"]+)" start="(?P<start>\d+)" end="(?P<end>\d+)"/>'
    )

    pattern_snippet_link = (
        r'<snippet-link path="(?P<path>[^"]+)" line="(?P<line>\d+)"/>'
    )

    if config.path_meta.exists():
        with open(config.path_meta, "r", encoding=config.ENCODING) as meta_file:
            metadata = config.deserialize_metadata(meta_file)

        last_version = version.get_version_of_last_update_until_version(
            file_path=path, version_name=metadata.current_version, metadata=metadata
        )
    else:
        metadata = None
        last_version = None

    # replace using the pattern and replace_tag function
    content = re.sub(
        pattern_snippet,
        lambda match: replace_tag(match, last_version, metadata),
        content,
    )

    content = re.sub(
        pattern_snippet_link,
        lambda match: replace_link(match, last_version, metadata),
        content,
    )

    return content


def replace_link(
    match,
    last_version_document: dataobjects.Version | None,
    metadata: dataobjects.Metadata | None,
):
    """Get data using match and return line number"""
    path = match.group("path")
    line = int(match.group("line"))

    _, line, _ = generate_code_snippet(
        path, line, line, last_version_document, metadata
    )

    return str(line)


def replace_tag(
    match,
    last_version_document: dataobjects.Version | None,
    metadata: dataobjects.Metadata | None,
):
    """Get data using match and return sniped with code"""
    path = match.group("path")
    line_start = int(match.group("start"))
    line_end = int(match.group("end"))

    snippet_lines, _, _ = generate_code_snippet(
        path, line_start, line_end, last_version_document, metadata
    )

    numbered_snippet = []
    for i, line in enumerate(snippet_lines, start=line_start):
        stripped_line = line.rstrip("\n")
        numbered_snippet.append(f"{i}: {stripped_line}")

    string_lines = "\n".join(numbered_snippet)

    # determine the language for syntax highlights
    language = get_programming_language(path)

    return f"``` {language}\n{string_lines}\n```"


def generate_code_snippet(
    path,
    line_start,
    line_end,
    last_version_document: dataobjects.Version | None,
    metadata: dataobjects.Metadata | None,
):
    """Read lines from path"""
    if last_version_document is not None:
        logs = version.get_file_version_logs(
            file=path,
            version_name=metadata.current_version,
            metadata=metadata,
            start_version_name=last_version_document.name,
        )

    with open(path, "r", encoding=config.ENCODING) as file:
        lines = file.readlines()

    snippet_lines = lines[line_start - 1 : line_end]

    return (snippet_lines, line_start, line_end)


def get_programming_language(file_path):
    """Get programing language by file path or empty string"""
    extension_mapping = {
        ".py": "python",
        ".c": "c",
        ".cpp": "cpp",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
    }

    _, extension = os.path.splitext(file_path)
    return extension_mapping.get(extension, "")
