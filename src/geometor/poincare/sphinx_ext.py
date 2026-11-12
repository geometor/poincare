"""Runtime Sphinx & photon-platform/publish integration for GEOMETOR Poincaré.

Registers the ``fr`` ("French (1902)") companion track in ``photon_platform.publish.book``
at build time (without modifying ``photon-platform/publish``) and configures
offline-safe local intersphinx inventories across the GEOMETOR ecosystem.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any


def register_french_book_track() -> None:
    """Extend ``photon_platform.publish.book`` to recognize ``<stem>-fr`` French tracks."""
    try:
        from photon_platform.publish import book
    except ImportError:
        return

    fr_pattern = (r"^(.+)[._-]fr$", "fr", "French (1902)")
    if not any(key == "fr" for _pat, key, _lbl in book._TRACK_SUFFIX_PATTERNS):
        book._TRACK_SUFFIX_PATTERNS.append(fr_pattern)

    book._AUX_TRACK_BASENAMES.add("fr")
    fr_aux_re = re.compile(r"^.+[._-]fr$")
    if not any(p.pattern == fr_aux_re.pattern for p in book._AUX_TRACK_PATTERNS):
        book._AUX_TRACK_PATTERNS.append(fr_aux_re)

    if getattr(book.detect_companion_tracks, "_poincare_fr_patched", False):
        return

    orig_detect = book.detect_companion_tracks

    def _detect_with_french(env: object, pagename: str) -> list[dict[str, Any]]:
        found_docs: set[str] = set(getattr(env, "found_docs", set()))
        if not found_docs:
            return []

        doc_dir = os.path.dirname(pagename)
        basename = os.path.basename(pagename)
        stem = book._extract_unit_stem(basename, doc_dir)
        if basename == "fr" and doc_dir:
            stem = os.path.basename(doc_dir)

        def _qual(local_name: str) -> str:
            return f"{doc_dir}/{local_name}" if doc_dir else local_name

        probe_page = pagename
        fr_candidates = [
            _qual(f"{stem}.fr"),
            _qual(f"{stem}_fr"),
            _qual(f"{stem}-fr"),
            _qual("fr"),
        ]
        fr_doc = next((c for c in fr_candidates if c in found_docs), None)
        if fr_doc and pagename == fr_doc:
            en_cand = next(
                (
                    c
                    for c in (
                        _qual(f"{stem}-en"),
                        _qual(f"{stem}_en"),
                        _qual(f"{stem}.en"),
                    )
                    if c in found_docs
                ),
                None,
            )
            if en_cand:
                probe_page = en_cand

        tracks = orig_detect(env, probe_page)
        if not fr_doc:
            return tracks

        updated: list[dict[str, Any]] = []
        inserted_fr = False
        fr_entry = {
            "key": "fr",
            "label": "French (1902)",
            "docname": fr_doc,
            "active": fr_doc == pagename,
        }
        for tr in tracks:
            if tr.get("docname") == fr_doc:
                continue
            item = dict(tr)
            item["active"] = item.get("docname") == pagename
            updated.append(item)
            if item.get("key") == "en" and not inserted_fr:
                updated.append(fr_entry)
                inserted_fr = True

        if not inserted_fr:
            updated.insert(0, fr_entry)

        return updated if len(updated) >= 2 else []

    _detect_with_french._poincare_fr_patched = True  # type: ignore[attr-defined]
    book.detect_companion_tracks = _detect_with_french


def configure_local_intersphinx(
    intersphinx_mapping: dict[str, Any], project_root: Path
) -> None:
    """Bind local ``objects.inv`` files across GEOMETOR sister repos and prune offline-unreachable URLs.

    Args:
        intersphinx_mapping: Mutable Sphinx ``intersphinx_mapping`` dictionary.
        project_root: Root directory of the ``geometor/poincare`` repository.
    """
    geometor_dir = project_root.parent
    sister_repos = (
        "euclid",
        "elements",
        "hilbert",
        "bertrand-russell",
        "hoenen",
        "klein",
        "pappus",
        "casey",
        "lemoine",
        "wildberger",
        "codes",
        "etc",
        "proclus",
        "aristotle",
        "model",
    )
    for sister in sister_repos:
        inv = geometor_dir / sister / "docs" / "objects.inv"
        if inv.is_file():
            intersphinx_mapping[sister] = (
                f"https://geometor.github.io/{sister}",
                str(inv.resolve()),
            )
    for key in list(intersphinx_mapping.keys()):
        _uri, inv_target = intersphinx_mapping[key]
        if inv_target is None:
            intersphinx_mapping.pop(key, None)


def setup(app: object) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app: Active Sphinx application instance.

    Returns:
        Extension metadata dictionary.
    """
    _ = app
    register_french_book_track()
    return {
        "version": "0.1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
