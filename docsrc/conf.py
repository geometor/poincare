"""Sphinx configuration for GEOMETOR • poincare."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE_ROOT = _REPO_ROOT.parent
for _src_path in (_REPO_ROOT / "src", _WORKSPACE_ROOT / "model" / "src"):
    if str(_src_path) not in sys.path:
        sys.path.insert(0, str(_src_path))

from photon_platform.publish.global_conf import *  # noqa: E402, F403

import geometor.poincare as module  # noqa: E402
from geometor.poincare.sphinx_ext import (  # noqa: E402
    configure_local_intersphinx,
    register_french_book_track,
)

register_french_book_track()
if "geometor.poincare.sphinx_ext" not in extensions:  # noqa: F405
    extensions.append("geometor.poincare.sphinx_ext")  # noqa: F405

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "poincare"
repo_name = "poincare"

setup_globals(org, org_name, repo, repo_name)  # noqa: F405

project = "GEOMETOR • poincare"
author = "Henri Poincaré"
copyright = (
    "1902 Ernest Flammarion · 1905 Walter Scott / Science Press · Digital Codex GEOMETOR"
)

html_static_path = ["_static"]

# Restrict AutoAPI strictly to `src/geometor` and avoid duplicate root index with modules/index.rst
autoapi_dirs = [str(_REPO_ROOT / "src" / "geometor")]
autoapi_add_toctree_entry = False
if "modules/api/geometor/poincare/index.rst" not in exclude_patterns:  # noqa: F405
    exclude_patterns.append("modules/api/geometor/poincare/index.rst")  # noqa: F405

# Bind offline-first local intersphinx inventories across the GEOMETOR canon
configure_local_intersphinx(intersphinx_mapping, _REPO_ROOT)  # noqa: F405
