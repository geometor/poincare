"""Export all 8 standalone .euclid-graphic SVGs into docsrc/_static/figures/."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
for _p in (_REPO_ROOT / "src", _REPO_ROOT.parent / "model" / "src"):
    if _p.is_dir() and str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from geometor.poincare.cli import main  # noqa: E402


def run() -> int:
    """Export all codex figures via the CLI."""
    return main(["--repo-root", str(_REPO_ROOT), "figures"])


if __name__ == "__main__":
    raise SystemExit(run())
