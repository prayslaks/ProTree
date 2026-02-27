"""
protree — Print a directory tree in markdown/README style.

Usage:
    protree [root_dir] [--depth N]

Examples:
    protree
    protree . --depth 3
    protree Source
"""

import contextlib
import fnmatch
import os
import sys
import argparse

VERSION = "1.0.0"

# Always skip regardless of .gitignore
ALWAYS_SKIP = {".git", "__pycache__", "node_modules"}


class PatternMatcher:
    """Parse a gitignore-style pattern file and test whether a path matches."""

    def __init__(self, root: str, filename: str):
        self.root = os.path.abspath(root)
        # patterns: list of (pattern_str, dir_only, anchored)
        self.patterns: list[tuple[str, bool, bool]] = []
        self._load(os.path.join(self.root, filename))

    def _load(self, path: str) -> None:
        if not os.path.isfile(path):
            return
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n").rstrip()
                if not line or line.startswith("#") or line.startswith("!"):
                    continue
                dir_only = line.endswith("/")
                pattern = line.rstrip("/")
                # Anchored = contains "/" (after stripping trailing slash)
                anchored = "/" in pattern
                self.patterns.append((pattern, dir_only, anchored))

    def matches(self, abs_path: str, is_dir: bool) -> bool:
        rel = os.path.relpath(abs_path, self.root).replace("\\", "/")
        name = os.path.basename(rel)

        for pattern, dir_only, anchored in self.patterns:
            if dir_only and not is_dir:
                continue
            if anchored:
                if fnmatch.fnmatch(rel, pattern):
                    return True
            else:
                if fnmatch.fnmatch(name, pattern):
                    return True
        return False


def print_tree(root: str, max_depth: int = -1) -> None:
    root = os.path.abspath(root)
    ignore = PatternMatcher(root, ".gitignore")
    collapse = PatternMatcher(root, ".ptignore")
    print(os.path.basename(root) + "/")
    _walk(root, prefix="", depth=0, max_depth=max_depth, ignore=ignore, collapse=collapse)


def _walk(
    path: str,
    prefix: str,
    depth: int,
    max_depth: int,
    ignore: PatternMatcher,
    collapse: PatternMatcher,
) -> None:
    if max_depth != -1 and depth >= max_depth:
        return

    try:
        entries = sorted(os.scandir(path), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        return

    entries = [
        e for e in entries
        if e.name not in ALWAYS_SKIP
        and not ignore.matches(e.path, e.is_dir())
    ]

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        suffix = "/" if entry.is_dir() else ""
        print(f"{prefix}{connector}{entry.name}{suffix}")

        if entry.is_dir() and not collapse.matches(entry.path, is_dir=True):
            extension = "    " if is_last else "│   "
            _walk(entry.path, prefix + extension, depth + 1, max_depth, ignore, collapse)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a directory tree in markdown style.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  protree .\n"
            "  protree C:/MyProject --depth 3\n"
            "  protree C:/MyProject --output tree.txt\n"
            "\n"
            "per-project config files (placed in <root>):\n"
            "  .gitignore   entries are hidden entirely\n"
            "  .ptignore    directories are shown but not expanded"
        ),
    )
    parser.add_argument("root", nargs="?", default=".", help="Target directory (default: .)")
    parser.add_argument("--depth", "-d", type=int, default=-1, help="Max depth (-1 = unlimited)")
    parser.add_argument("--output", "-o", default=None, help="Write output to this file instead of stdout")
    parser.add_argument("--version", "-v", action="version", version=f"protree {VERSION}")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"Error: '{args.root}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f, contextlib.redirect_stdout(f):
            print_tree(args.root, args.depth)
        print(f"Written to: {args.output}", file=sys.stderr)
    else:
        print_tree(args.root, args.depth)


if __name__ == "__main__":
    main()
