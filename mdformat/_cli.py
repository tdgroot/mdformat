import argparse
from pathlib import Path
import sys
from typing import Sequence

from markdown_it import MarkdownIt

from mdformat._renderer import RendererCmark
from mdformat._util import is_md_equal


def run(cli_args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        description="CommonMark compliant Markdown formatter"
    )
    parser.add_argument("paths", type=Path, nargs="*", help="Files to format")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(cli_args)

    if not args.paths:
        sys.stderr.write("No files have been passed in. Doing nothing.\n")
        return 0

    for path in args.paths:
        if not path.is_file():
            sys.stderr.write(f'Error: File "{path}" does not exist.\n')
            return 1

    for path in args.paths:
        original_str = path.read_text()
        formatted_str = MarkdownIt(renderer_cls=RendererCmark).render(original_str)

        if args.check:
            if formatted_str != original_str:
                sys.stderr.write(f'Error: File "{path}" is not formatted.\n')
                return 1
        else:
            if not is_md_equal(original_str, formatted_str):
                sys.stderr.write(
                    f'Error: Could not format "{path}"\n'
                    "\n"
                    "The formatted Markdown renders to different HTML than the input Markdown.\n"  # noqa: E501
                    "This is likely a bug in mdformat. Please create an issue report here:\n"  # noqa: E501
                    "https://github.com/hukkinj1/mdformat/issues\n"
                )
                return 1
            with path.open(mode="w") as f:
                f.write(formatted_str)
    return 0