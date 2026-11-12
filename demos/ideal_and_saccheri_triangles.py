r"""Demo 3: Ideal Hyperbolic Triangle & Saccheri Quadrilateral Angular Defect.

Proves two celebrated theorems of Bolyai–Lobachevsky–Saccheri geometry using 100%
rational points, rational circle centers, and Rational Trigonometry spreads inside
``geometor.model``:

1. **Pythagorean Ideal Triangle** :math:`\triangle U_1 U_2 U_3` on
   :math:`U_1 = (1, 0),\; U_2 = (-\frac{3}{5}, \frac{4}{5}),\; U_3 = (-\frac{3}{5}, -\frac{4}{5})`:
   - Orthogonal side circles centered at :math:`(1, 2),\; (1, -2),\; (-\frac{5}{3}, 0)`
     with exact rational radii :math:`2,\; 2,\; \frac{4}{3}`.
   - Interior tangent spreads :math:`(0, 0, 0)` and maximal Gauss–Bonnet defect :math:`\pi`.
2. **Hyperbolic Right Triangle** :math:`\triangle OAB` & **Saccheri Quadrilateral**
   :math:`A_1 A_2 B_2 B_1`:
   - Right triangle on :math:`O(0,0),\; A(\frac{1}{2},0),\; B(0,\frac{1}{2})` has base spread
     :math:`1` and acute vertex spreads :math:`\frac{9}{34} < \frac{1}{2}`.
   - Saccheri quadrilateral with base :math:`A_1(-\frac{1}{3}, 0),\; A_2(\frac{1}{3}, 0)` and
     summit :math:`B_1(-\frac{17}{39}, \frac{20}{39}),\; B_2(\frac{17}{39}, \frac{20}{39})` has
     equal leg UHG quadrances :math:`-\frac{225}{64}`, right base spreads :math:`(1, 1)`,
     and strictly acute summit spreads :math:`\frac{64}{145} < 1` (refuting Saccheri's
     Euclidean right-angle hypothesis).
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
from geometor.model import zero_test  # noqa: E402

from geometor.poincare import (  # noqa: E402
    IdealTriangleResult,
    SaccheriDefectResult,
    construct_ideal_hyperbolic_triangle,
    construct_saccheri_triangleDefect,
    render_figure_svg,
)


def run_demo(svg_dir: Path | None = None) -> tuple[IdealTriangleResult, SaccheriDefectResult]:
    """Construct and verify the ideal hyperbolic triangle and Saccheri quadrilateral."""
    ideal = construct_ideal_hyperbolic_triangle()
    sac = construct_saccheri_triangleDefect()

    for m in (ideal.model, sac.model):
        for el in m:
            if el.has(sp.Float):
                raise AssertionError(f"Floating-point atom detected in {el!r}")

    assert ideal.radii == (sp.Integer(2), sp.Integer(2), sp.Rational(4, 3))
    assert all(zero_test(s) for s in ideal.vertex_spreads)

    assert sac.triangle_spreads == (sp.Integer(1), sp.Rational(9, 34), sp.Rational(9, 34))
    assert sac.saccheri_base_spreads == (sp.Integer(1), sp.Integer(1))
    assert sac.saccheri_summit_spreads == (sp.Rational(64, 145), sp.Rational(64, 145))
    assert sac.saccheri_leg_uhg_quadrances == (
        sp.Rational(-225, 64),
        sp.Rational(-225, 64),
    )

    if svg_dir is not None:
        svg_dir.mkdir(parents=True, exist_ok=True)
        (svg_dir / "fig4_ideal_hyperbolic_triangle.svg").write_text(
            render_figure_svg("fig4_ideal_hyperbolic_triangle.svg"), encoding="utf-8"
        )
        (svg_dir / "fig5_saccheri_angular_defect.svg").write_text(
            render_figure_svg("fig5_saccheri_angular_defect.svg"), encoding="utf-8"
        )

    return ideal, sac


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for Demo 3."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--svg-dir",
        type=Path,
        default=None,
        help="Optional directory to write fig4 and fig5 SVGs.",
    )
    args = parser.parse_args(argv)

    ideal, sac = run_demo(svg_dir=args.svg_dir)
    print("=== Demo 3: Ideal Hyperbolic Triangle & Saccheri Angular Defect ===")
    print(f"Ideal vertices       : {ideal.vertices}")
    print(f"Ideal circle centers : {ideal.centers}")
    print(f"Ideal circle radii   : {ideal.radii}")
    print(f"Ideal vertex spreads : {ideal.vertex_spreads}  ->  defect = {ideal.angular_defect}")
    print("-" * 68)
    print(
        f"Right triangle OAB   : spreads = {sac.triangle_spreads} (< (1, 1/2, 1/2)), "
        f"defect = {sac.triangle_defect}"
    )
    print(f"Saccheri leg q_UHG   : {sac.saccheri_leg_uhg_quadrances}")
    print(f"Saccheri base spreads: {sac.saccheri_base_spreads}")
    print(
        f"Saccheri summit      : spreads = {sac.saccheri_summit_spreads} (< 1), "
        f"defect = {sac.saccheri_defect}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
