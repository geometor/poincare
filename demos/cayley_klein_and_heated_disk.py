r"""Demo 4: Poincaré's Heated Disk, Beltrami–Klein Projection, & Stellar Parallax.

Synthesizes the physical and projective models of *La Science et l'Hypothèse*
(Part II, Chs. IV–V, 1902):

1. **Poincaré's Heated-Disk Parable (Ch. IV)**:
   - Temperature :math:`T(r) \propto R^2 - r^2` and refractive index :math:`n(r) \propto (R^2 - r^2)^{-1}`
     bend optical Fermat geodesics and thermally contracted rulers along orthogonal circles,
     making the finite disk physically indistinguishable from an infinite Lobachevskian plane.
2. **Beltrami–Klein Projective Chord Bridge**:
   - Radial straightedge projection from :math:`O` onto the straight chord :math:`UV`
     realizes the exact Weierstrass map :math:`K(P) = \frac{2P}{1 + \|P\|^2}`, turning
     Poincaré's conformal arcs into Beltrami–Klein projective segments while preserving
     :math:`q_{\text{CK}}(P_1, P_2) = \tanh^2 d_{\mathbb{H}}(P_1, P_2)`.
3. **Stellar Parallax & Geometric Conventionalism (Ch. V § 3)**:
   - Any astronomical triangle :math:`\triangle S_1 S_2 S_3` with angular sum differing
     from :math:`\pi` admits two empirically equivalent descriptions: Lobachevskian space
     with straight rays vs. Euclidean space with refracted rays.
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
    BeltramiKleinBridgeResult,
    HeatedDiskResult,
    StellarParallaxResult,
    construct_beltrami_klein_bridge,
    construct_heated_disk_optical_rays,
    construct_stellar_parallax_conventionalism,
    hyperbolic_cross_ratio_and_quadrance,
    render_figure_svg,
)


def _klein_hilbert_quadrance(
    k1: sp.geometry.Point2D,
    k2: sp.geometry.Point2D,
) -> sp.Expr:
    r"""Compute the Beltrami–Klein metric invariant directly from Klein coordinates.

    For interior Klein points :math:`K_1, K_2`, the Cayley–Klein quadrance satisfies
    :math:`1 - q_{\text{CK}}(K_1, K_2) = \frac{(1 - \|K_1\|^2)(1 - \|K_2\|^2)}{(1 - K_1 \cdot K_2)^2}`.
    """
    n1 = k1.x**2 + k1.y**2
    n2 = k2.x**2 + k2.y**2
    dot = k1.x * k2.x + k1.y * k2.y
    return sp.simplify(1 - ((1 - n1) * (1 - n2)) / (1 - dot) ** 2)


def run_demo(
    svg_dir: Path | None = None,
) -> tuple[HeatedDiskResult, BeltramiKleinBridgeResult, StellarParallaxResult]:
    """Construct and verify the Heated Disk, Beltrami–Klein bridge, and Parallax models."""
    heated = construct_heated_disk_optical_rays()
    bridge = construct_beltrami_klein_bridge()
    parallax = construct_stellar_parallax_conventionalism()

    for m in (heated.model, bridge.model, parallax.model):
        for el in m:
            if el.has(sp.Float):
                raise AssertionError(f"Floating-point atom detected in {el!r}")

    p1, p2 = bridge.poincare_points
    k1, k2 = bridge.klein_points
    poincare_metrics = hyperbolic_cross_ratio_and_quadrance(
        p1, p2, bridge.poincare_geodesic.U, bridge.poincare_geodesic.V
    )
    q_ck_from_klein = _klein_hilbert_quadrance(k1, k2)
    assert zero_test(poincare_metrics.cayley_klein_quadrance - q_ck_from_klein)

    if svg_dir is not None:
        svg_dir.mkdir(parents=True, exist_ok=True)
        for fname in (
            "fig6_heated_disk_refraction.svg",
            "fig7_cayley_klein_beltrami_bridge.svg",
            "fig8_stellar_parallax_conventionalism.svg",
        ):
            (svg_dir / fname).write_text(render_figure_svg(fname), encoding="utf-8")

    return heated, bridge, parallax


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for Demo 4."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--svg-dir",
        type=Path,
        default=None,
        help="Optional directory to write fig6, fig7, and fig8 SVGs.",
    )
    args = parser.parse_args(argv)

    heated, bridge, parallax = run_demo(svg_dir=args.svg_dir)
    p1, p2 = bridge.poincare_points
    k1, k2 = bridge.klein_points
    metrics = hyperbolic_cross_ratio_and_quadrance(
        p1, p2, bridge.poincare_geodesic.U, bridge.poincare_geodesic.V
    )

    print("=== Demo 4: Heated Disk, Beltrami–Klein Bridge, & Stellar Parallax ===")
    print(
        f"Heated disk source S = ({heated.source.x}, {heated.source.y}) with "
        f"{len(heated.isothermals)} isothermals and {len(heated.light_rays)} Fermat rays"
    )
    print(f"Poincaré points      : P1 = ({p1.x}, {p1.y}), P2 = ({p2.x}, {p2.y})")
    print(f"Klein chord images   : K1 = ({k1.x}, {k1.y}), K2 = ({k2.x}, {k2.y})")
    print(
        f"Invariant match      : q_CK(Poincaré) = {metrics.cayley_klein_quadrance} == "
        f"q_CK(Beltrami–Klein) = {_klein_hilbert_quadrance(k1, k2)}"
    )
    print(
        f"Parallax triangle    : {len(parallax.stars)} stars, "
        f"{len(parallax.lobachevsky_rays)} hyperbolic arcs vs. "
        f"{len(parallax.euclidean_chords)} Euclidean refracted chords"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
