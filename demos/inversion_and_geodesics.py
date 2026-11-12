r"""Demo 1: Horizon Inversion, Orthogonal Geodesic Circles, and Rational Quadrances.

Constructs Henri Poincaré's conformal disk dictionary (*La Science et l'Hypothèse*,
Part II, Ch. III, 1902) inside ``geometor.model`` with 100% exact SymPy algebra:

1. Horizon circle :math:`\Omega: x^2 + y^2 = 1` centered at :math:`O = (0, 0)`.
2. Pure straightedge-and-compass Euclidean inversion :math:`P \mapsto P^* = P / \|P\|^2`
   satisfying :math:`Q(O, P) \cdot Q(O, P^*) = 1` and involution :math:`(P^*)^* = P`.
3. Unique orthogonal hyperbolic geodesic circle through :math:`(P, Q, P^*)` cutting
   :math:`\Omega` orthogonally (:math:`|OC|^2 - r^2 = 1`) at ideal boundary points :math:`U, V`.
4. Exact equivalence between Poincaré's 4-point cross-ratio distance
   :math:`d_{\mathbb{H}}(P, Q) = \ln \chi(P, Q; U, V)` and Norman Wildberger's
   transcendental-free Rational Hyperbolic Quadrance :math:`q_{\text{UHG}}(P, Q) \in \mathbb{Q}`.
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
from geometor.model import Model, quadrance, zero_test  # noqa: E402

from geometor.poincare import (  # noqa: E402
    construct_hyperbolic_geodesic,
    construct_inversion_in_horizon,
    construct_unit_horizon,
    hyperbolic_cross_ratio_and_quadrance,
    render_figure_svg,
)


def assert_zero_floats(model: Model) -> None:
    """Verify that every element in ``model`` is 100% free of ``sp.Float``."""
    for el in model:
        if el.has(sp.Float):
            raise AssertionError(f"Floating-point contamination detected in {el!r}")


def run_demo(svg_out: Path | None = None) -> dict[str, sp.Expr]:
    """Execute the exact horizon-inversion and geodesic construction."""
    model = Model("demo_inversion_and_geodesics", logger=False, auto_intersect=False)
    origin, _ex, _omega = construct_unit_horizon(model)

    # Interior rational points P and Q
    p_pt = model.set_point(sp.Rational(1, 3), sp.Rational(1, 4), classes=["given"], label="P")
    q_pt = model.set_point(sp.Rational(-2, 5), sp.Rational(1, 5), classes=["given"], label="Q")

    # 1. Exact compass-and-straightedge inversion in the unit horizon
    p_star = construct_inversion_in_horizon(model, p_pt, label="P*")
    p_roundtrip = construct_inversion_in_horizon(model, p_star, label="P**")
    assert zero_test(quadrance(origin, p_pt) * quadrance(origin, p_star) - 1)
    assert zero_test(p_roundtrip.x - p_pt.x) and zero_test(p_roundtrip.y - p_pt.y)

    # 2. Orthogonal hyperbolic geodesic circle through P and Q
    geo = construct_hyperbolic_geodesic(model, p_pt, q_pt, label="g_PQ")
    carrier, u_ideal, v_ideal = geo
    assert not geo.is_diameter
    assert geo.center is not None and geo.radius_squared is not None
    assert zero_test(geo.orthogonality_residual)
    assert zero_test(quadrance(origin, u_ideal) - 1)
    assert zero_test(quadrance(origin, v_ideal) - 1)

    # 3. Diameter case when collinear with origin O
    r_pt = model.set_point(sp.Rational(2, 3), sp.Rational(1, 2), classes=["given"], label="R")
    diam_geo = construct_hyperbolic_geodesic(model, p_pt, r_pt, label="diam_PR")
    assert diam_geo.is_diameter

    # 4. Cross-ratio and Rational Hyperbolic Quadrance invariants
    metrics = hyperbolic_cross_ratio_and_quadrance(p_pt, q_pt, u_ideal, v_ideal)
    assert_zero_floats(model)

    svg_markup = render_figure_svg("fig2_poincare_dictionary_inversion.svg")
    if svg_out is not None:
        svg_out.parent.mkdir(parents=True, exist_ok=True)
        svg_out.write_text(svg_markup, encoding="utf-8")

    _ = carrier
    return {
        "P_star_x": p_star.x,
        "P_star_y": p_star.y,
        "center_x": geo.center.x,
        "center_y": geo.center.y,
        "radius_squared": geo.radius_squared,
        "conformal_quadrance": metrics.conformal_quadrance,
        "wildberger_uhg_quadrance": metrics.wildberger_uhg_quadrance,
        "cayley_klein_quadrance": metrics.cayley_klein_quadrance,
        "cross_ratio": metrics.cross_ratio,
        "poincare_distance": metrics.poincare_distance,
    }


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for Demo 1."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg", type=Path, default=None, help="Optional output SVG path.")
    args = parser.parse_args(argv)

    summary = run_demo(svg_out=args.svg)
    print("=== Demo 1: Horizon Inversion & Hyperbolic Geodesic Dictionary ===")
    print(f"P         = (1/3, 1/4)  ->  P* = ({summary['P_star_x']}, {summary['P_star_y']})")
    print(
        f"Geodesic  : center C = ({summary['center_x']}, {summary['center_y']}), "
        f"r^2 = {summary['radius_squared']} (|OC|^2 - r^2 = 1)"
    )
    print(f"tau(P, Q) = {summary['conformal_quadrance']}")
    print(f"q_UHG     = {summary['wildberger_uhg_quadrance']}")
    print(f"q_CK      = {summary['cayley_klein_quadrance']}")
    print(f"chi       = {summary['cross_ratio']}")
    print(f"d_H(P, Q) = {summary['poincare_distance']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
