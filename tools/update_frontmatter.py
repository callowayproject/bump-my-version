#!/usr/bin/env python
"""Update frontmatter of markdown files."""

import argparse
from pathlib import Path
from typing import Any, Dict, Optional

import frontmatter


def extract_main_heading(markdown_content: str) -> Optional[str]:
    """
    Extracts the first level 1 heading from the provided Markdown content.

    Args:
        markdown_content: A string containing Markdown text.

    Returns:
        The text of the first level 1 heading, or None if no such heading is found.
    """
    lines = markdown_content.split("\n")

    return next((line[2:] for line in lines if line.startswith("# ")), None)


def calc_title(post: frontmatter.Post) -> str:
    """Calculate the title of the post."""
    return extract_main_heading(post.content) or post.get("title", "")


def calc_comment(post: frontmatter.Post) -> bool:
    """Calculate if the post has comments."""
    return bool(post.get("comments", True))


def calculate_update(post: frontmatter.Post) -> dict:
    """Calculate if the frontmatter needs to be updated."""
    expected_title = calc_title(post)
    expected_comment = calc_comment(post)
    update: Dict[str, Any] = {}
    if expected_title and expected_title != post.get("title"):
        update["title"] = expected_title
    if expected_comment != post.get("comments"):
        update["comments"] = expected_comment
    return update


def process_file(markdown_path: Path) -> None:
    """Process a single file."""
    if not (markdown_path.is_file() and markdown_path.suffix == ".md"):
        return
    raw_text = markdown_path.read_text()
    post = frontmatter.loads(raw_text)

    update = calculate_update(post)
    if update:
        for key, value in update.items():
            post[key] = value
        new_text = frontmatter.dumps(post)
        print(f"Updating {markdown_path}")
        markdown_path.write_text(new_text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Update frontmatter of markdown files")
    parser.add_argument("markdown_path", type=str, nargs="+", help="Path or glob to markdown files")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    documents = args.markdown_path
    for document in documents:
        for path in Path().glob(document):
            process_file(path)
