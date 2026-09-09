#!/usr/bin/env python3
# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Shrink the downloaded pictures so the attachment XML stays reviewable.

The attachments are inlined as base64 in ``data/ir_attachment_pre.xml``, so a
three megabyte hero image turns into tens of thousands of unreadable diff
lines. Illustrations exported as PNG are the worst offenders: re-encoding them
as WebP keeps the alpha channel and cuts an order of magnitude.

Files already under the byte budget are left untouched, so vector assets and
the logo keep their original format.

Pillow is optional: without it the script reports and exits cleanly.

Usage: tools/optimize_asset.py [directory] [--max-width 1600] [--budget 220000]
"""

# A command line tool run by a developer, never imported by Odoo, so its report
# belongs on stdout rather than in the server log.
# pylint: disable=print-used

import argparse
import sys
from pathlib import Path

MAX_WIDTH = 1600
BYTE_BUDGET = 220_000
QUALITY_STEPS = (82, 72, 62)
RASTER_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def optimize(path, max_width, budget):
    """Return a human readable summary, or None when nothing was needed."""
    from PIL import Image

    original_size = path.stat().st_size
    with Image.open(path) as opened:
        source_dimensions = opened.size
        if opened.width > max_width:
            height = round(opened.height * max_width / opened.width)
            image = opened.resize((max_width, height), Image.LANCZOS)
        else:
            image = opened.copy()

    needs_resize = source_dimensions != image.size
    if not needs_resize and original_size <= budget:
        return None

    target = path.with_suffix(".webp")
    for quality in QUALITY_STEPS:
        image.save(target, "WEBP", quality=quality, method=6)
        if target.stat().st_size <= budget:
            break

    if target != path:
        path.unlink()
    return (
        f"{path.name} -> {target.name}: "
        f"{source_dimensions[0]}x{source_dimensions[1]} "
        f"{original_size // 1024} KB -> "
        f"{image.size[0]}x{image.size[1]} {target.stat().st_size // 1024} KB"
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(
            Path(__file__).resolve().parent.parent / "static/src/binary/ir_attachment"
        ),
    )
    parser.add_argument("--max-width", type=int, default=MAX_WIDTH)
    parser.add_argument("--budget", type=int, default=BYTE_BUDGET)
    args = parser.parse_args(argv)

    directory = Path(args.directory)
    if not directory.is_dir():
        parser.error(f"{directory} is not a directory")

    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Pillow is not installed, skipping image optimisation", file=sys.stderr)
        return 0

    total = 0
    for path in sorted(directory.iterdir()):
        if path.suffix.lower() not in RASTER_SUFFIXES:
            continue
        summary = optimize(path, args.max_width, args.budget)
        if summary:
            print(summary)
            total += 1
    print(f"optimised {total} images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
