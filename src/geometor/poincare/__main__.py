"""Module execution entry point (`python -m geometor.poincare`)."""

from __future__ import annotations

import sys

from geometor.poincare.cli import main

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
