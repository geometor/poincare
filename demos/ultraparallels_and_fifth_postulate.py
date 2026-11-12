r"""Demo 2: Limiting Horoparallels, Ultraparallels, and Independence of Postulate V.

Constructs Henri Poincaré's relative consistency proof for Lobachevskian geometry
(*La Science et l'Hypothèse*, Part II, Ch. III, 1902):

Given a hyperbolic geodesic :math:`L_{\text{hyp}}` with rational ideal endpoints
:math:`U_L = (\frac{4}{5}, -\frac{3}{5})` and :math:`V_L = (-\frac{4}{5}, -\frac{3}{5})`
and an exterior point :math:`P = (\frac{1}{6}, \frac{2}{5}) \in \mathbb{D} \setminus L_{\text{hyp}}`:

- Constructs the two limiting horoparallels :math:`\ell_1 = PU_L` and :math:`\ell_2 = PV_L`
  sharing ideal boundary vertices with :math:`L_{\text{hyp}}` on :math:`\partial\Omega`
  while remaining disjoint inside the open disk :math:`\mathbb{D}`.
- Constructs two distinct ultraparallel geodesics :math:`m_1, m_2` through :math:`P`
  whose closures in :math:`\overline{\mathbb{D}}` are 100% disjoint from :math:`L_{\text{hyp}}`.
- Demonstrates that any contradiction in Lobachevsky's geometry would translate via
  Poincaré's Dictionary into a contradiction in Euclidean circle geometry.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

_REPO_ROOT = Path(__file__).resolve().parents[1]
for _candidate in (_REPO_ROOT / "src", _REPO_ROOT.parent / "model" / "src"):
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

import sympy as sp  # noqa: E402
import sympy.geometry as spg  # noqa: E402
from geometor.model import exact_sign, intersect_2d, zero_test  # noqa: E402

from geometor.poincare import (  # noqa: E402
    UltraparallelPencil,
    construct_ultraparallels_through_point,
    render_figure_svg,
)


def run_demo(svg_out: Path | None = None) -> UltraparallelPencil:
    """Construct and verify the Lobachevskian parallel pencil through P."""
    pencil = construct_ultraparallels_through_point()
    for el in pencil.model:
        if el.has(sp.Float):
            raise AssertionError(f"Floating-point atom found in {el!r}")

    base_carrier = pencil.base_geodesic.carrier
    # Verify limiting horoparallels meet base_geodesic ONLY on the ideal horizon x^2 + y^2 == 1
    for lim in pencil.limiting_parallels:
        hits = intersect_2d(base_carrier, lim.carrier)
        interior_hits = [
            pt
            for pt in hits
            if isinstance(pt, spg.Point2D) and exact_sign(pt.x**2 + pt.y**2 - 1) < 0
        ]
        bdry_hits = [
            pt
            for pt in hits
            if isinstance(pt, spg.Point2D) and zero_test(pt.x**2 + pt.y**2 - 1)
        ]
        assert len(interior_hits) == 0
        assert len(bdry_hits) == 1

    # Verify ultraparallels have ZERO intersections in the closed unit disk x^2 + y^2 <= 1
    for ultra in pencil.ultraparallels:
        hits = intersect_2d(base_carrier, ultra.carrier)
        closed_disk_hits = [
            pt
            for pt in hits
            if isinstance(pt, spg.Point2D) and exact_sign(pt.x**2 + pt.y**2 - 1) <= 0
        ]
        assert len(closed_disk_hits) == 0

    svg_markup = render_figure_svg("fig3_lobachevsky_parallels.svg")
    if svg_out is not None:
        svg_out.parent.mkdir(parents=True, exist_ok=True)
        svg_out.write_text(svg_markup, encoding="utf-8")

    return pencil


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for Demo 2."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg", type=Path, default=None, help="Optional output SVG path.")
    args = parser.parse_args(argv)

    pencil = run_demo(svg_out=args.svg)
    print("=== Demo 2: Lobachevskian Horoparallels & Ultraparallels (Postulate V) ===")
    print(f"Base geodesic L_hyp ideal endpoints : {pencil.base_geodesic.ideal_points}")
    print(f"Exterior point P                    : ({pencil.point.x}, {pencil.point.y})")
    for idx, lim in enumerate(pencil.limiting_parallels, start=1):
        print(f"Horoparallel l_{idx} center & r^2       : {lim.center}, r^2 = {lim.radius_squared}")
    for idx, ultra in enumerate(pencil.ultraparallels, start=1):
        print(
            f"Ultraparallel m_{idx} center & r^2      : {ultra.center}, r^2 = {ultra.radius_squared} "
            "(0 intersections in closed disk)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
