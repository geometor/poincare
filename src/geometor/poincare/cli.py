"""Command-line interface for ``geometor-poincare``."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import sympy as sp
import sympy.geometry as spg
from geometor.model import Model, zero_test

from geometor.poincare.concordance import (
    audit_codex_repository,
    compile_apparatus_rst,
    default_repo_root,
)
from geometor.poincare.disk import (
    construct_hyperbolic_geodesic,
    construct_ideal_hyperbolic_triangle,
    construct_saccheri_triangleDefect,
    construct_ultraparallels_through_point,
    hyperbolic_cross_ratio_and_quadrance,
)
from geometor.poincare.render import export_all_codex_figures


def _run_symbolic_smoke_checks() -> str:
    """Execute fast exact symbolic assertions across ``geometor.poincare.disk``."""
    model = Model("cli_smoke", logger=False, auto_intersect=False)
    p_pt = model.set_point(sp.Rational(1, 2), sp.Integer(0))
    q_pt = model.set_point(sp.Integer(0), sp.Rational(1, 2))
    geo = construct_hyperbolic_geodesic(model, p_pt, q_pt)
    metrics = hyperbolic_cross_ratio_and_quadrance(p_pt, q_pt, geo.U, geo.V)
    if not zero_test(metrics.conformal_quadrance - sp.Rational(8, 17)):
        raise AssertionError(f"Expected conformal quadrance 8/17, got {metrics.conformal_quadrance}")

    ideal = construct_ideal_hyperbolic_triangle()
    sac = construct_saccheri_triangleDefect()
    ultra = construct_ultraparallels_through_point()
    _ = (spg, ideal, sac, ultra)
    return (
        f"Symbolic engine OK: tau(P,Q)={metrics.conformal_quadrance}, "
        f"q_UHG(P,Q)={metrics.wildberger_uhg_quadrance}, "
        f"ideal_radii={ideal.radii}, saccheri_summit_spread={sac.saccheri_summit_spreads[0]}"
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser for ``geometor-poincare``."""
    parser = argparse.ArgumentParser(
        prog="geometor-poincare",
        description="GEOMETOR • Poincaré: Bilingual Science & Hypothesis Codex and Exact Hyperbolic Disk Engine.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=default_repo_root(),
        help="Path to the geometor/poincare repository root.",
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status", help="Display codex, apparatus, and figure counts.")
    sub.add_parser("verify", help="Verify witness SHA-256 checksums, 4-track parity, and symbolic invariants.")
    sub.add_parser("figures", help="Export all 8 .euclid-graphic SVGs into docsrc/_static/figures/.")
    sub.add_parser("compile-apparatus", help="Compile concordance, bibliography, persons, and glossary RST pages.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ``geometor-poincare`` command-line tool.

    Args:
        argv: Optional list of CLI arguments.

    Returns:
        Process exit status (``0`` on success).
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    root: Path = args.repo_root.resolve()
    cmd = args.command or "status"

    if cmd == "figures":
        out = export_all_codex_figures(root / "docsrc" / "_static" / "figures")
        print(f"Exported {len(out)} .euclid-graphic SVGs to {root / 'docsrc' / '_static' / 'figures'}")
        return 0

    if cmd == "compile-apparatus":
        written = compile_apparatus_rst(root)
        print(f"Compiled {len(written)} apparatus RST files in {root / 'docsrc' / 'science_and_hypothesis'}")
        return 0

    if cmd in ("status", "verify"):
        report = audit_codex_repository(root)
        print(
            f"Codex OK: {report.witness_count} archival witnesses | "
            f"{report.unit_track_files} synchronized track files | "
            f"{report.figure_count} SVGs | "
            f"{report.concordance_entries} concordance entries ({report.dictionary_rows} dictionary rows) | "
            f"{report.persons_count} persons | {report.citations_count} citations | "
            f"{report.glossary_count} glossary terms"
        )
        if cmd == "verify":
            print(_run_symbolic_smoke_checks())
        return 0

    parser.print_help()
    return 1
