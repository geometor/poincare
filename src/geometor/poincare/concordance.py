"""Scholarly concordance, archival witness verification, and RST apparatus compiler.

Manages the JSON registries in ``resources/science_and_hypothesis/`` (mirrored to
``resources/`` for PHOTON Publish hover-card resolution), verifies SHA-256 digests of
the public-domain 1902 French and 1905 English primary witnesses, checks 4-track Book
Codex synchronization, and compiles ``concordance.rst``, ``bibliography.rst``,
``persons.rst``, and ``glossary.rst``.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "CODEX_UNITS",
    "CodexAuditReport",
    "audit_codex_repository",
    "compile_apparatus_rst",
    "default_repo_root",
    "load_concordance",
    "load_sources_manifest",
    "sync_root_apparatus_json",
    "verify_sources_manifest",
]

CODEX_UNITS: tuple[str, ...] = (
    "unit-1-number-and-magnitude",
    "unit-2-non-euclidean-geometries",
    "unit-3-space-and-geometry",
    "unit-4-experience-and-geometry",
)

TRACK_SUFFIXES: tuple[str, ...] = ("en", "fr", "summary", "notes")


def default_repo_root() -> Path:
    """Return the root directory of ``geometor/poincare``."""
    return Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> dict[str, Any]:
    """Read and parse a UTF-8 JSON object file."""
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return data


def load_sources_manifest(repo_root: Path | None = None) -> dict[str, Any]:
    """Load ``resources/science_and_hypothesis/sources_manifest.json``."""
    root = repo_root or default_repo_root()
    return _read_json(root / "resources" / "science_and_hypothesis" / "sources_manifest.json")


def load_concordance(repo_root: Path | None = None) -> dict[str, Any]:
    """Load ``resources/science_and_hypothesis/concordance.json``."""
    root = repo_root or default_repo_root()
    return _read_json(root / "resources" / "science_and_hypothesis" / "concordance.json")


def verify_sources_manifest(repo_root: Path | None = None) -> list[dict[str, Any]]:
    """Verify SHA-256 digests and byte counts of all archival witness files.

    Args:
        repo_root: Optional repository root path.

    Returns:
        List of verified witness records.

    Raises:
        FileNotFoundError: If any witness file is missing.
        ValueError: If a SHA-256 digest or byte count mismatches ``sources_manifest.json``.
    """
    root = repo_root or default_repo_root()
    manifest = load_sources_manifest(root)
    verified: list[dict[str, Any]] = []
    for item in manifest.get("witnesses", []):
        rel_path = item["path"]
        target = root / rel_path
        if not target.is_file():
            raise FileNotFoundError(f"Missing archival witness file: {target}")
        raw = target.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != item["sha256"]:
            raise ValueError(
                f"SHA-256 mismatch for {rel_path}: expected {item['sha256']}, got {digest}"
            )
        if len(raw) != int(item["bytes"]):
            raise ValueError(
                f"Byte size mismatch for {rel_path}: expected {item['bytes']}, got {len(raw)}"
            )
        verified.append(item)
    return verified


def sync_root_apparatus_json(repo_root: Path | None = None) -> list[Path]:
    """Mirror ``persons.json``, ``citations.json``, and ``glossary.json`` into ``resources/``.

    Args:
        repo_root: Optional repository root path.

    Returns:
        List of destination paths written in ``resources/``.
    """
    root = repo_root or default_repo_root()
    src_dir = root / "resources" / "science_and_hypothesis"
    dst_dir = root / "resources"
    copied: list[Path] = []
    for name in ("persons.json", "citations.json", "glossary.json"):
        src = src_dir / name
        dst = dst_dir / name
        shutil.copyfile(src, dst)
        copied.append(dst)
    return copied


def compile_apparatus_rst(repo_root: Path | None = None) -> list[Path]:
    """Compile ``concordance.rst``, ``bibliography.rst``, ``persons.rst``, and ``glossary.rst``.

    Args:
        repo_root: Optional repository root path.

    Returns:
        List of generated ``.rst`` paths under ``docsrc/science_and_hypothesis/``.
    """
    root = repo_root or default_repo_root()
    sync_root_apparatus_json(root)
    res_dir = root / "resources" / "science_and_hypothesis"
    out_dir = root / "docsrc" / "science_and_hypothesis"
    out_dir.mkdir(parents=True, exist_ok=True)

    concordance = _read_json(res_dir / "concordance.json")
    persons: dict[str, dict[str, str]] = _read_json(res_dir / "persons.json")
    citations: dict[str, dict[str, str]] = _read_json(res_dir / "citations.json")
    glossary: dict[str, dict[str, str]] = _read_json(res_dir / "glossary.json")

    written: list[Path] = []

    # 1. concordance.rst
    conc_lines = [
        ":layout: book",
        "",
        ".. _concordance:",
        "",
        "Poincaré Translation Dictionary & Cross-Corpus Concordance",
        "==========================================================",
        "",
        ".. rubric:: Mapping *La Science et l'Hypothèse* (1902 / 1905) across the GEOMETOR Digital Scriptorium & Symbolic Engine",
        "",
        concordance["description"],
        "",
        "----",
        "",
        "I. Poincaré's Hyperbolic Translation Dictionary (*Ch. III, pp. 56–58*)",
        "----------------------------------------------------------------------",
        "",
        ".. list-table::",
        "   :header-rows: 1",
        "   :widths: 24 30 46",
        "",
        "   * - Lobachevskian Term",
        "     - Euclidean Disk Model Translation (:math:`\\mathbb{D} \\subset \\mathbb{R}^2`)",
        "     - Exact ``geometor.poincare`` Algebraic Realization",
    ]
    for row in concordance["dictionary_mappings"]:
        conc_lines.extend(
            [
                f"   * - **{row['hyperbolic_term']}** (*{row['french_term']}*)",
                f"     - {row['euclidean_translation']}",
                f"     - {row['symbolic_realization']}",
            ]
        )

    conc_lines.extend(
        [
            "",
            "----",
            "",
            "II. Cross-Repository Philosophical & Geometric Concordance",
            "----------------------------------------------------------",
            "",
        ]
    )
    for entry in concordance["entries"]:
        hdr = f"{entry['id']} — {entry['title']}"
        conc_lines.extend(
            [
                hdr,
                "~" * len(hdr),
                "",
                f"* **Locus in Poincaré:** {entry['poincare_locus']} (:ref:`{entry['unit_ref_label']} <{entry['unit_ref']}>`)",
                f"* **GEOMETOR Canon Links:** {', '.join(f'``geometor/{r}``' for r in entry['sister_repos'])}",
                f"* **Exact Symbolic Construction:** ``{entry['symbolic_function']}``",
                "",
                entry["synthesis"],
                "",
            ]
        )

    conc_path = out_dir / "concordance.rst"
    conc_path.write_text("\n".join(conc_lines).rstrip() + "\n", encoding="utf-8")
    written.append(conc_path)

    # 2. bibliography.rst
    bib_lines = [
        ":layout: book",
        "",
        ".. _bibliography:",
        "",
        "Systematic Bibliography",
        "=======================",
        "",
        ".. rubric:: Primary Public-Domain Editions, Historical Treatises, and Philosophical Debates",
        "",
    ]
    for key, item in citations.items():
        title_line = f"``[{key}]`` — {item['author']} ({item['year']})"
        bib_lines.extend(
            [
                title_line,
                "-" * len(title_line),
                "",
                f"*{item['work']}*. {item['locus']}. {item['publisher']}.",
                "",
                item["note"],
                "",
            ]
        )
    bib_path = out_dir / "bibliography.rst"
    bib_path.write_text("\n".join(bib_lines).rstrip() + "\n", encoding="utf-8")
    written.append(bib_path)

    # 3. persons.rst
    pers_lines = [
        ":layout: book",
        "",
        ".. _persons:",
        "",
        "Index of Persons",
        "================",
        "",
        ".. rubric:: Prosopographical Registry of Geometers, Physicists, and Philosophers",
        "",
    ]
    for key, p in persons.items():
        hdr = f"{p['name']} ({p['dates']})"
        pers_lines.extend(
            [
                f".. _person-{key}:",
                "",
                hdr,
                "-" * len(hdr),
                "",
                f"**Role:** {p['role']}",
                "",
                p["bio"],
                "",
            ]
        )
    pers_path = out_dir / "persons.rst"
    pers_path.write_text("\n".join(pers_lines).rstrip() + "\n", encoding="utf-8")
    written.append(pers_path)

    # 4. glossary.rst
    gloss_lines = [
        ":layout: book",
        "",
        ".. _glossary:",
        "",
        "Bilingual Technical Glossary",
        "============================",
        "",
        ".. rubric:: French (1902), German, Latin, and English Terminology of Conventionalism & Non-Euclidean Geometry",
        "",
    ]
    for key, g in glossary.items():
        hdr = f"{g['headword']} — *{g['translation']}* ``[{g['language']}]``"
        gloss_lines.extend(
            [
                f".. _term-{key}:",
                "",
                hdr,
                "-" * len(hdr),
                "",
                g["definition"],
                "",
            ]
        )
    gloss_path = out_dir / "glossary.rst"
    gloss_path.write_text("\n".join(gloss_lines).rstrip() + "\n", encoding="utf-8")
    written.append(gloss_path)

    return written


@dataclass(frozen=True)
class CodexAuditReport:
    """Summary of verified codex witnesses, apparatus registries, figures, and 4-track units."""

    witness_count: int
    concordance_entries: int
    dictionary_rows: int
    persons_count: int
    citations_count: int
    glossary_count: int
    figure_count: int
    unit_track_files: int


def audit_codex_repository(repo_root: Path | None = None) -> CodexAuditReport:
    """Audit all primary witnesses, apparatus JSONs, 8 SVGs, and 16 4-track unit RST files.

    Args:
        repo_root: Optional repository root path.

    Returns:
        Verified :class:`CodexAuditReport`.

    Raises:
        FileNotFoundError: If any expected codex track or SVG figure is missing.
        ValueError: If any ``:layout: book`` file embeds a ``.. py_file::`` script.
    """
    root = repo_root or default_repo_root()
    witnesses = verify_sources_manifest(root)
    conc = load_concordance(root)
    res_dir = root / "resources" / "science_and_hypothesis"
    persons = _read_json(res_dir / "persons.json")
    citations = _read_json(res_dir / "citations.json")
    glossary = _read_json(res_dir / "glossary.json")

    fig_dir = root / "docsrc" / "_static" / "figures"
    svg_files = sorted(fig_dir.glob("*.svg")) if fig_dir.is_dir() else []
    if len(svg_files) < 8:
        raise FileNotFoundError(f"Expected >= 8 .euclid-graphic SVGs in {fig_dir}, found {len(svg_files)}")

    codex_dir = root / "docsrc" / "science_and_hypothesis"
    track_count = 0
    for unit in CODEX_UNITS:
        for suf in TRACK_SUFFIXES:
            rst_file = codex_dir / unit / f"{unit}-{suf}.rst"
            if not rst_file.is_file():
                raise FileNotFoundError(f"Missing synchronized track file: {rst_file}")
            txt = rst_file.read_text(encoding="utf-8")
            if ":layout: book" not in txt:
                raise ValueError(f"Track file missing ':layout: book' header: {rst_file}")
            if "py_file" in txt:
                raise ValueError(f"Forbidden embedded py_file directive in book codex: {rst_file}")
            track_count += 1

    return CodexAuditReport(
        witness_count=len(witnesses),
        concordance_entries=len(conc.get("entries", [])),
        dictionary_rows=len(conc.get("dictionary_mappings", [])),
        persons_count=len(persons),
        citations_count=len(citations),
        glossary_count=len(glossary),
        figure_count=len(svg_files),
        unit_track_files=track_count,
    )
