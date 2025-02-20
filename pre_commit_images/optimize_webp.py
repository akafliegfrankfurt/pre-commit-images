#!/usr/bin/env python3
import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import IO

from PIL import Image

from .optimizer import _optimize_images


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to optimize.")
    parser.add_argument(
        "-t",
        "--threshold",
        dest="threshold",
        default=1024,
        type=int,
        help="Minimum improvement to replace file in bytes (default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--lossless",
        action="store_true",
        help="Use lossless compression",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default=80,
        type=int,
        help="Quality of lossy images or effort to compress lossless images (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    def optimize(source: Path, target: IO[bytes]) -> None:
        im = Image.open(source)
        im.save(
            target,
            format=im.format,
            lossless=args.lossless,
            method=6,
            quality=args.quality,
        )

    success = _optimize_images(args.filenames, optimize, args.threshold)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
