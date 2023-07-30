"""Markdown utility module"""

import os
import re
import config


def parse_file(path: str) -> str:
    """Find by patter and replace it"""

    with open(path, "r", encoding=config.ENCODING) as file:
        content = file.read()

    pattern = (
        r'<snippet path="(?P<path>[^"]+)" start="(?P<start>\d+)" end="(?P<end>\d+)"/>'
    )

    # replace using the pattern and replace_tag function
    content = re.sub(pattern, replace_tag, content)

    return content


def replace_tag(match):
    """Get data using match and return sniped with code"""
    path = match.group("path")
    line_start = int(match.group("start"))
    line_end = int(match.group("end"))

    snippet_lines = generate_code_snippet(path, line_start, line_end)

    numbered_snippet = []
    for i, line in enumerate(snippet_lines, start=line_start):
        stripped_line = line.rstrip("\n")
        numbered_snippet.append(f"{i}: {stripped_line}")

    string_lines = "\n".join(numbered_snippet)

    # determine the language for syntax highlights
    language = get_programming_language(path)

    return f"``` {language}\n{string_lines}\n```"


def generate_code_snippet(path, line_start, line_end):
    """Read lines from path"""

    with open(path, "r", encoding=config.ENCODING) as file:
        lines = file.readlines()

    snippet_lines = lines[line_start - 1 : line_end]

    return snippet_lines


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
