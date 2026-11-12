"""Publication-grade interactive ``.euclid-graphic`` SVG renderer for ``geometor.poincare``.

Generates theme-adaptive SVGs directly from exact :mod:`geometor.poincare.disk` symbolic
constructions while preserving canonical ``data-ref`` attributes, ``<defs>`` midpoint
tick markers (``#geom-tick-1..3``), 3-vertex midpoint ``<path>`` arcs and segments, and
``#highlights`` overlay groups consumed by PHOTON Publish's ``geometor_interactive.js``
and ``.. picture::`` directive.
"""

from __future__ import annotations

import html
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import sympy as sp
import sympy.geometry as spg
from geometor.model import Model

from geometor.poincare.disk import (
    HyperbolicGeodesic,
    construct_beltrami_klein_bridge,
    construct_dedekind_continuum_cut,
    construct_heated_disk_optical_rays,
    construct_hyperbolic_geodesic,
    construct_ideal_hyperbolic_triangle,
    construct_saccheri_triangle_defect,
    construct_stellar_parallax_conventionalism,
    construct_ultraparallels_through_point,
    construct_unit_horizon,
)

__all__ = [
    "EMBEDDED_SVG_STYLE",
    "FIGURE_SPECS",
    "export_all_codex_figures",
    "render_codex_figure",
    "render_figure_svg",
]

EMBEDDED_SVG_CSS2_FALLBACK: str = """
  .euclid-graphic { font-family: "Inter", "Fira Sans", "Segoe UI", sans-serif; }
  .euclid-graphic .svg-bg { fill: #fafaf9; }
  .euclid-graphic .disk-interior { fill: #0ea5e9; fill-opacity: 0.055; stroke: none; }
  .euclid-graphic .horizon-circle { fill: none; stroke: #0f172a; stroke-width: 2.35; }
  .euclid-graphic .carrier-ghost { fill: none; stroke: #64748b; stroke-width: 1.15; stroke-dasharray: 4 3.5; opacity: 0.55; }
  .euclid-graphic .isothermal-circle { fill: none; stroke: #0284c7; stroke-width: 1.25; stroke-dasharray: 3 3; opacity: 0.62; }
  .euclid-graphic .guide-line { fill: none; stroke: #64748b; stroke-width: 1.35; stroke-dasharray: 5 3.5; opacity: 0.78; }
  .euclid-graphic .geodesic-arc { fill: none; stroke: #0369a1; stroke-width: 2.35; stroke-linecap: round; }
  .euclid-graphic .featured-arc { fill: none; stroke: #b45309; stroke-width: 2.75; stroke-linecap: round; }
  .euclid-graphic .horoparallel-arc { fill: none; stroke: #059669; stroke-width: 2.3; stroke-linecap: round; }
  .euclid-graphic .ultraparallel-arc { fill: none; stroke: #7c3aed; stroke-width: 2.25; stroke-dasharray: 7 3.5; stroke-linecap: round; }
  .euclid-graphic .klein-chord { fill: none; stroke: #dc2626; stroke-width: 2.25; stroke-dasharray: 6 3; stroke-linecap: round; }
  .euclid-graphic .region-fill { fill: #b45309; fill-opacity: 0.09; stroke: none; }
  .euclid-graphic .ideal-region { fill: #7c3aed; fill-opacity: 0.08; stroke: none; }
  .euclid-graphic .pt-interior { fill: #0369a1; stroke: #fafaf9; stroke-width: 1.6; }
  .euclid-graphic .pt-featured { fill: #b45309; stroke: #fafaf9; stroke-width: 1.75; }
  .euclid-graphic .pt-ideal { fill: #fafaf9; stroke: #0f172a; stroke-width: 2.0; }
  .euclid-graphic .pt-inverse { fill: #7c3aed; stroke: #fafaf9; stroke-width: 1.7; }
  .euclid-graphic .pt-klein { fill: #dc2626; stroke: #fafaf9; stroke-width: 1.7; }
  .euclid-graphic .geom-label { fill: #1c1917; font-size: 13px; font-weight: 600; }
  .euclid-graphic .geom-caption { fill: #64748b; font-size: 11.5px; font-weight: 500; }
""".strip()

EMBEDDED_SVG_STYLE: str = """
  .euclid-graphic {
    --svg-bg: #fafaf9;
    --disk-fill: rgba(14, 165, 233, 0.055);
    --ink: #1c1917;
    --muted: #64748b;
    --label-halo: rgba(250, 250, 249, 0.94);
    --horizon: #0f172a;
    --geodesic: #0369a1;
    --featured: #b45309;
    --horoparallel: #059669;
    --ultraparallel: #7c3aed;
    --klein: #dc2626;
    --isothermal: #0284c7;
    --guide: #64748b;
    --poly-fill: rgba(180, 83, 9, 0.09);
    --ideal-fill: rgba(124, 58, 237, 0.08);
    --geom-assert: #16a34a;
  }
  @media (prefers-color-scheme: dark) {
    .euclid-graphic {
      --svg-bg: #141417;
      --disk-fill: rgba(56, 189, 248, 0.075);
      --ink: #f4f4f5;
      --muted: #94a3b8;
      --label-halo: rgba(20, 20, 23, 0.94);
      --horizon: #e2e8f0;
      --geodesic: #38bdf8;
      --featured: #fbbf24;
      --horoparallel: #34d399;
      --ultraparallel: #c084fc;
      --klein: #f87171;
      --isothermal: #38bdf8;
      --guide: #94a3b8;
      --poly-fill: rgba(251, 191, 36, 0.11);
      --ideal-fill: rgba(192, 132, 252, 0.11);
      --geom-assert: #4ade80;
    }
  }
  .euclid-graphic .svg-bg { fill: var(--svg-bg); }
  .euclid-graphic .disk-interior { fill: var(--disk-fill); fill-opacity: 1; }
  .euclid-graphic .horizon-circle { stroke: var(--horizon); }
  .euclid-graphic .carrier-ghost { stroke: var(--guide); }
  .euclid-graphic .isothermal-circle { stroke: var(--isothermal); }
  .euclid-graphic .guide-line { stroke: var(--guide); }
  .euclid-graphic .geodesic-arc { stroke: var(--geodesic); }
  .euclid-graphic .featured-arc { stroke: var(--featured); }
  .euclid-graphic .horoparallel-arc { stroke: var(--horoparallel); }
  .euclid-graphic .ultraparallel-arc { stroke: var(--ultraparallel); }
  .euclid-graphic .klein-chord { stroke: var(--klein); }
  .euclid-graphic .region-fill { fill: var(--poly-fill); fill-opacity: 1; }
  .euclid-graphic .ideal-region { fill: var(--ideal-fill); fill-opacity: 1; }
  .euclid-graphic .pt-interior { fill: var(--geodesic); stroke: var(--svg-bg); }
  .euclid-graphic .pt-featured { fill: var(--featured); stroke: var(--svg-bg); }
  .euclid-graphic .pt-ideal { fill: var(--svg-bg); stroke: var(--horizon); }
  .euclid-graphic .pt-inverse { fill: var(--ultraparallel); stroke: var(--svg-bg); }
  .euclid-graphic .pt-klein { fill: var(--klein); stroke: var(--svg-bg); }
  .euclid-graphic .geom-label {
    fill: var(--ink);
    paint-order: stroke fill;
    stroke: var(--label-halo);
    stroke-width: 3.6px;
    stroke-linejoin: round;
    user-select: none;
  }
  .euclid-graphic .geom-caption { fill: var(--muted); user-select: none; }
""".strip()


def _fmt(val: float) -> str:
    """Format a floating-point SVG coordinate compactly to 2 decimal places."""
    if abs(val - round(val)) < 1e-5:
        return str(int(round(val)))
    return f"{val:.2f}".rstrip("0").rstrip(".")


@dataclass(frozen=True)
class _Viewport:
    """Affine math-to-SVG viewport transform."""

    width: int
    height: int
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    pad: float = 34.0

    @property
    def scale(self) -> float:
        """Compute uniform pixels-per-unit scale factor."""
        sx = (self.width - 2 * self.pad) / (self.xmax - self.xmin)
        sy = (self.height - 2 * self.pad) / (self.ymax - self.ymin)
        return min(sx, sy)

    def to_px(self, x: sp.Expr | float, y: sp.Expr | float) -> tuple[float, float]:
        """Map exact or numeric math coordinates ``(x, y)`` to SVG pixels ``(px, py)``."""
        xf = float(sp.sympify(x).evalf()) if not isinstance(x, float) else x
        yf = float(sp.sympify(y).evalf()) if not isinstance(y, float) else y
        s = self.scale
        cx_math = 0.5 * (self.xmin + self.xmax)
        cy_math = 0.5 * (self.ymin + self.ymax)
        px = 0.5 * self.width + (xf - cx_math) * s
        py = 0.5 * self.height - (yf - cy_math) * s
        return (px, py)


def _svg_defs() -> str:
    """Return ``<defs>`` block with ``#geom-tick-1..3`` midpoint equality markers."""
    return """  <defs>
    <marker id="geom-tick-1" viewBox="-4 -7 8 14" refX="0" refY="0" markerWidth="8" markerHeight="14" orient="auto">
      <line x1="0" y1="-5.5" x2="0" y2="5.5" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/>
    </marker>
    <marker id="geom-tick-2" viewBox="-6 -7 12 14" refX="0" refY="0" markerWidth="12" markerHeight="14" orient="auto">
      <line x1="-2.2" y1="-5.5" x2="-2.2" y2="5.5" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="2.2" y1="-5.5" x2="2.2" y2="5.5" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/>
    </marker>
    <marker id="geom-tick-3" viewBox="-8 -7 16 14" refX="0" refY="0" markerWidth="16" markerHeight="14" orient="auto">
      <line x1="-4.2" y1="-5.5" x2="-4.2" y2="5.5" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="0" y1="-5.5" x2="0" y2="5.5" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/>
      <line x1="4.2" y1="-5.5" x2="4.2" y2="5.5" stroke="#16a34a" stroke-width="1.8" stroke-linecap="round"/>
    </marker>
  </defs>"""


def _segment_path(
    vp: _Viewport,
    p1: tuple[sp.Expr | float, sp.Expr | float],
    p2: tuple[sp.Expr | float, sp.Expr | float],
    *,
    cls: str,
    ref: str | None = None,
    title: str | None = None,
) -> str:
    """Render a 3-vertex midpoint ``<path>`` segment compatible with ``#geom-tick-*``."""
    x1, y1 = vp.to_px(p1[0], p1[1])
    x2, y2 = vp.to_px(p2[0], p2[1])
    mx, my = 0.5 * (x1 + x2), 0.5 * (y1 + y2)
    ref_attr = f' data-ref="{html.escape(ref)}"' if ref else ""
    d_str = f"M {_fmt(x1)} {_fmt(y1)} L {_fmt(mx)} {_fmt(my)} L {_fmt(x2)} {_fmt(y2)}"
    if title:
        return f'    <path class="{cls}"{ref_attr} d="{d_str}"><title>{html.escape(title)}</title></path>'
    return f'    <path class="{cls}"{ref_attr} d="{d_str}"/>'


def _minor_arc_mid_math(
    cx: float, cy: float, r: float, ax: float, ay: float, bx: float, by: float
) -> tuple[float, float]:
    """Compute the exact math midpoint along the minor circular arc between ``A`` and ``B``."""
    th_a = math.atan2(ay - cy, ax - cx)
    th_b = math.atan2(by - cy, bx - cx)
    delta = th_b - th_a
    while delta <= -math.pi:
        delta += 2 * math.pi
    while delta > math.pi:
        delta -= 2 * math.pi
    th_mid = th_a + 0.5 * delta
    return (cx + r * math.cos(th_mid), cy + r * math.sin(th_mid))


def _arc_path_between(
    vp: _Viewport,
    center: tuple[sp.Expr | float, sp.Expr | float],
    radius: sp.Expr | float,
    a_pt: tuple[sp.Expr | float, sp.Expr | float],
    b_pt: tuple[sp.Expr | float, sp.Expr | float],
    *,
    cls: str,
    ref: str | None = None,
    title: str | None = None,
) -> str:
    """Render a minor circular arc between ``a_pt`` and ``b_pt`` as a 3-vertex SVG ``<path>``."""
    cx = float(sp.sympify(center[0]).evalf())
    cy = float(sp.sympify(center[1]).evalf())
    rf = float(sp.sympify(radius).evalf())
    ax = float(sp.sympify(a_pt[0]).evalf())
    ay = float(sp.sympify(a_pt[1]).evalf())
    bx = float(sp.sympify(b_pt[0]).evalf())
    by = float(sp.sympify(b_pt[1]).evalf())

    mx_m, my_m = _minor_arc_mid_math(cx, cy, rf, ax, ay, bx, by)
    px_c, py_c = vp.to_px(cx, cy)
    px_a, py_a = vp.to_px(ax, ay)
    px_m, py_m = vp.to_px(mx_m, my_m)
    px_b, py_b = vp.to_px(bx, by)
    r_px = rf * vp.scale

    cross1 = (px_a - px_c) * (py_m - py_c) - (py_a - py_c) * (px_m - px_c)
    sweep1 = 1 if cross1 > 0 else 0
    cross2 = (px_m - px_c) * (py_b - py_c) - (py_m - py_c) * (px_b - px_c)
    sweep2 = 1 if cross2 > 0 else 0

    d_str = (
        f"M {_fmt(px_a)} {_fmt(py_a)} "
        f"A {_fmt(r_px)} {_fmt(r_px)} 0 0 {sweep1} {_fmt(px_m)} {_fmt(py_m)} "
        f"A {_fmt(r_px)} {_fmt(r_px)} 0 0 {sweep2} {_fmt(px_b)} {_fmt(py_b)}"
    )
    ref_attr = f' data-ref="{html.escape(ref)}"' if ref else ""
    if title:
        return f'    <path class="{cls}"{ref_attr} d="{d_str}"><title>{html.escape(title)}</title></path>'
    return f'    <path class="{cls}"{ref_attr} d="{d_str}"/>'


def _geodesic_path(
    vp: _Viewport,
    geo: HyperbolicGeodesic,
    *,
    cls: str = "geodesic-arc",
    ref: str | None = None,
    title: str | None = None,
    start_pt: spg.Point2D | None = None,
    end_pt: spg.Point2D | None = None,
) -> str:
    """Render a full ideal-to-ideal (or finite sub-arc) hyperbolic geodesic."""
    p_a = start_pt if start_pt is not None else geo.U
    p_b = end_pt if end_pt is not None else geo.V
    if geo.is_diameter or isinstance(geo.carrier, spg.Line2D):
        return _segment_path(vp, (p_a.x, p_a.y), (p_b.x, p_b.y), cls=cls, ref=ref, title=title)
    assert isinstance(geo.carrier, spg.Circle)
    return _arc_path_between(
        vp,
        (geo.carrier.center.x, geo.carrier.center.y),
        geo.carrier.radius,
        (p_a.x, p_a.y),
        (p_b.x, p_b.y),
        cls=cls,
        ref=ref,
        title=title,
    )


def _circle_el(
    vp: _Viewport,
    center: tuple[sp.Expr | float, sp.Expr | float],
    radius: sp.Expr | float,
    *,
    cls: str,
    ref: str | None = None,
    title: str | None = None,
) -> str:
    """Render an SVG ``<circle>`` element."""
    cx, cy = vp.to_px(center[0], center[1])
    r_px = float(sp.sympify(radius).evalf()) * vp.scale
    ref_attr = f' data-ref="{html.escape(ref)}"' if ref else ""
    if title:
        return (
            f'    <circle class="{cls}"{ref_attr} cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r_px)}">'
            f"<title>{html.escape(title)}</title></circle>"
        )
    return f'    <circle class="{cls}"{ref_attr} cx="{_fmt(cx)}" cy="{_fmt(cy)}" r="{_fmt(r_px)}"/>'


def _point_and_label(
    vp: _Viewport,
    pt: spg.Point2D | tuple[sp.Expr | float, sp.Expr | float],
    label: str,
    *,
    cls: str = "pt-interior",
    ref: str | None = None,
    dx: float = 8.0,
    dy: float = -8.0,
    r_px: float = 4.3,
) -> tuple[str, str]:
    """Render a point marker ``<circle>`` and haloed ``<text>`` label."""
    if isinstance(pt, spg.Point2D):
        x_val, y_val = pt.x, pt.y
        title_str = f"{label} = ({sp.sstr(pt.x)}, {sp.sstr(pt.y)})"
    else:
        x_val, y_val = pt[0], pt[1]
        title_str = label
    px, py = vp.to_px(x_val, y_val)
    ref_val = ref if ref is not None else label
    pt_svg = (
        f'    <circle class="{cls}" data-ref="{html.escape(ref_val)}" '
        f'cx="{_fmt(px)}" cy="{_fmt(py)}" r="{_fmt(r_px)}">'
        f"<title>{html.escape(title_str)}</title></circle>"
    )
    anchor = "middle" if abs(dx) < 3.0 else ("start" if dx > 0 else "end")
    lbl_svg = (
        f'    <text class="geom-label" data-ref="{html.escape(ref_val)}" '
        f'x="{_fmt(px + dx)}" y="{_fmt(py + dy)}" text-anchor="{anchor}">'
        f"{html.escape(label)}</text>"
    )
    return pt_svg, lbl_svg


def _wrap_svg(
    vp: _Viewport,
    fig_id: str,
    aria_label: str,
    geom_lines: Sequence[str],
    point_lines: Sequence[str],
    label_lines: Sequence[str],
    caption: str,
) -> str:
    """Assemble a complete interactive ``svg.euclid-graphic`` document."""
    cap_y = vp.height - 10
    cap_x = 0.5 * vp.width
    body = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" class="euclid-graphic" id="{html.escape(fig_id)}" '
            f'data-graphic-id="{html.escape(fig_id)}" '
            f'viewBox="0 0 {vp.width} {vp.height}" role="img" aria-label="{html.escape(aria_label)}">',
            f"  <style>\n{EMBEDDED_SVG_CSS2_FALLBACK}\n  </style>",
            f"  <style>\n{EMBEDDED_SVG_STYLE}\n  </style>",
            _svg_defs(),
            f'  <rect class="svg-bg" fill="#fafaf9" x="0" y="0" width="{vp.width}" height="{vp.height}" rx="8"/>',
            '  <g class="geometry-layer" fill="none">',
            *geom_lines,
            "  </g>",
            '  <g id="highlights"></g>',
            '  <g class="points-layer">',
            *point_lines,
            "  </g>",
            '  <g class="labels-layer">',
            *label_lines,
            f'    <text class="geom-caption" x="{_fmt(cap_x)}" y="{_fmt(cap_y)}" text-anchor="middle">{html.escape(caption)}</text>',
            "  </g>",
            "</svg>",
            "",
        ]
    )
    return body


def _render_fig1() -> str:
    """Unit 1: Dedekind cut (sqrt(2)/2) vs perceptual continuum threshold."""
    res = construct_dedekind_continuum_cut()
    vp = _Viewport(width=660, height=480, xmin=-0.22, xmax=1.28, ymin=-0.28, ymax=1.18)
    geom: list[str] = [
        _arc_path_between(
            vp, (0, 0), 1, (1, 0), (0, 1), cls="horizon-circle", ref="( Ex Ey )", title="Quarter unit circle x^2 + y^2 = 1"
        ),
        _segment_path(vp, (0, 0), (1.12, 0), cls="guide-line", ref="/ O Ex /", title="Real axis"),
        _segment_path(vp, (0, 0), (0, 1.08), cls="guide-line", ref="/ O Ey /", title="Imaginary/vertical axis"),
        _segment_path(vp, (0, 1), (1, 1), cls="guide-line", ref="/ Ey S /"),
        _segment_path(vp, (1, 0), (1, 1), cls="guide-line", ref="/ Ex S /"),
        _segment_path(
            vp, (0, 0), (1, 1), cls="geodesic-arc", ref="/ O S /", title="Unit-square diagonal y = x"
        ),
        _segment_path(
            vp,
            (res.cut_point.x, res.cut_point.y),
            (res.cut_point.x, 0),
            cls="featured-arc",
            ref="/ D Dx /",
            title="Exact Dedekind cut x = sqrt(2)/2",
        ),
        _segment_path(
            vp,
            (res.lower_rational.x, -0.05),
            (res.upper_rational.x, -0.05),
            cls="horoparallel-arc",
            ref="/ Q1 Q2 /",
            title="Perceptual threshold band [2/3, 3/4] (A = B, B = C, A < C)",
        ),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (spg.Point2D(0, 0), "O (0, 0)", "O", "pt-interior", -10, 18),
        (spg.Point2D(1, 0), "Eₓ (1, 0)", "Ex", "pt-ideal", 8, 18),
        (spg.Point2D(0, 1), "Eᵧ (0, 1)", "Ey", "pt-ideal", -10, -8),
        (spg.Point2D(1, 1), "S (1, 1)", "S", "pt-interior", 10, -8),
        (res.cut_point, "D (√2/2, √2/2)", "D", "pt-featured", 10, 16),
        (spg.Point2D(res.cut_point.x, 0), "Dₓ = √2/2", "Dx", "pt-featured", 0, -14),
        (res.lower_rational, "Q₁ = 2/3", "Q1", "pt-inverse", -14, 22),
        (res.upper_rational, "Q₂ = 3/4", "Q2", "pt-inverse", 16, 22),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig1_recurrence_continuum_cuts",
        "Dedekind continuum cut at sqrt(2)/2 versus perceptual continuum bounds",
        geom,
        pts,
        lbls,
        "Fig. 1 — Part I (Chs. I–II): Dedekind Cut Dₓ = √2/2 Splitting the Rational Continuum vs. Perceptual Threshold [Q₁, Q₂]",
    )


def _render_fig2() -> str:
    """Unit 2: Poincaré's Translation Dictionary & Horizon Inversion P <-> P*."""
    model = Model("fig2_dictionary", logger=False, auto_intersect=False)
    origin, _ex, _omega = construct_unit_horizon(model)
    p_pt = model.set_point(sp.Rational(1, 2), sp.Rational(1, 4), classes=["given"], label="P")
    q_pt = model.set_point(sp.Rational(-2, 5), sp.Rational(2, 5), classes=["given"], label="Q")
    geo = construct_hyperbolic_geodesic(model, p_pt, q_pt)
    assert geo.inverse_point is not None and geo.center is not None
    assert isinstance(geo.carrier, spg.Circle)

    vp = _Viewport(width=680, height=500, xmin=-1.38, xmax=2.42, ymin=-1.26, ymax=2.42)
    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega", title="Fundamental horizon Ω: x^2 + y^2 = 1"),
        _circle_el(
            vp,
            (geo.center.x, geo.center.y),
            geo.carrier.radius,
            cls="carrier-ghost",
            ref="( P Q Pstar )",
            title="Full orthogonal Euclidean circle through P, Q, P*",
        ),
        _segment_path(
            vp,
            (0, 0),
            (geo.inverse_point.x, geo.inverse_point.y),
            cls="guide-line",
            ref="/ O Pstar /",
            title="Inversion ray OP·OP* = 1",
        ),
        _segment_path(vp, (0, 0), (geo.U.x, geo.U.y), cls="guide-line", ref="/ O U /"),
        _segment_path(vp, (geo.center.x, geo.center.y), (geo.U.x, geo.U.y), cls="guide-line", ref="/ C U /"),
        _geodesic_path(
            vp,
            geo,
            cls="featured-arc",
            ref="( U V )",
            title="Hyperbolic geodesic arc UV orthogonal to Ω",
        ),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (origin, "O", "O", "pt-interior", -10, 16),
        (p_pt, "P (1/2, 1/4)", "P", "pt-featured", 0, 18),
        (q_pt, "Q (-2/5, 2/5)", "Q", "pt-featured", -6, 18),
        (geo.inverse_point, "P* (8/5, 4/5)", "Pstar", "pt-inverse", 10, -8),
        (geo.center, "C (9/16, 33/16)", "C", "pt-interior", 10, 4),
        (geo.U, "U", "U", "pt-ideal", 10, 6),
        (geo.V, "V", "V", "pt-ideal", -10, -8),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig2_poincare_dictionary_inversion",
        "Poincaré's Translation Dictionary and horizon circle inversion P to P*",
        geom,
        pts,
        lbls,
        "Fig. 2 — Ch. III: Poincaré's Dictionary — Horizon Inversion OP·OP* = 1 & Orthogonal Geodesic Circle (P, Q, P*)",
    )


def _render_fig3() -> str:
    """Unit 2: Lobachevsky limiting horoparallels & ultraparallels through P."""
    pencil = construct_ultraparallels_through_point()
    vp = _Viewport(width=660, height=520, xmin=-1.28, xmax=1.28, ymin=-1.26, ymax=1.24)
    l1, l2 = pencil.limiting_parallels
    m1, m2 = pencil.ultraparallels
    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega", title="Horizon Ω: x^2 + y^2 = 1"),
        _geodesic_path(vp, pencil.base_geodesic, cls="featured-arc", ref="L_hyp", title="Base hyperbolic line L_hyp"),
        _geodesic_path(vp, l1, cls="horoparallel-arc", ref="l1", title="First limiting horoparallel l1"),
        _geodesic_path(vp, l2, cls="horoparallel-arc", ref="l2", title="Second limiting horoparallel l2"),
        _geodesic_path(vp, m1, cls="ultraparallel-arc", ref="m1", title="First ultraparallel m1"),
        _geodesic_path(vp, m2, cls="ultraparallel-arc", ref="m2", title="Second ultraparallel m2"),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (pencil.point, "P (1/6, 2/5)", "P", "pt-featured", 16, 4),
        (pencil.base_geodesic.U, "U_L (4/5, -3/5)", "UL", "pt-ideal", 10, 14),
        (pencil.base_geodesic.V, "V_L (-4/5, -3/5)", "VL", "pt-ideal", -10, 14),
        (m1.U, "m₁", "m1_end", "pt-ideal", 10, -6),
        (m2.V, "m₂", "m2_end", "pt-ideal", 12, -4),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig3_lobachevsky_parallels",
        "Lobachevsky limiting horoparallels and ultraparallels violating Euclid Postulate V",
        geom,
        pts,
        lbls,
        "Fig. 3 — Ch. III: Independence of Euclid Postulate V — Base Line L_hyp, Horoparallels (l₁, l₂) & Ultraparallels (m₁, m₂)",
    )


def _render_fig4() -> str:
    """Unit 2: Exact Pythagorean Ideal Hyperbolic Triangle on partial Omega."""
    ideal = construct_ideal_hyperbolic_triangle()
    u1, u2, u3 = ideal.vertices
    g12, g13, g23 = ideal.sides
    c12, c13, c23 = ideal.centers
    r12, r13, r23 = ideal.radii
    vp = _Viewport(width=680, height=520, xmin=-2.05, xmax=2.05, ymin=-1.65, ymax=1.65)

    # Build interior shaded ideal triangle path
    px_u1, py_u1 = vp.to_px(u1.x, u1.y)
    px_u2, py_u2 = vp.to_px(u2.x, u2.y)
    px_u3, py_u3 = vp.to_px(u3.x, u3.y)
    r12_px = float(r12) * vp.scale
    r13_px = float(r13) * vp.scale
    r23_px = float(r23) * vp.scale
    c12_px = vp.to_px(c12.x, c12.y)
    c23_px = vp.to_px(c23.x, c23.y)
    c13_px = vp.to_px(c13.x, c13.y)
    sw12 = 1 if (px_u1 - c12_px[0]) * (py_u2 - c12_px[1]) - (py_u1 - c12_px[1]) * (px_u2 - c12_px[0]) > 0 else 0
    sw23 = 1 if (px_u2 - c23_px[0]) * (py_u3 - c23_px[1]) - (py_u2 - c23_px[1]) * (px_u3 - c23_px[0]) > 0 else 0
    sw31 = 1 if (px_u3 - c13_px[0]) * (py_u1 - c13_px[1]) - (py_u3 - c13_px[1]) * (px_u1 - c13_px[0]) > 0 else 0
    fill_path = (
        f'    <path class="ideal-region" data-ref="{html.escape("< U1 U2 U3 >")}" d="'
        f"M {_fmt(px_u1)} {_fmt(py_u1)} "
        f"A {_fmt(r12_px)} {_fmt(r12_px)} 0 0 {sw12} {_fmt(px_u2)} {_fmt(py_u2)} "
        f"A {_fmt(r23_px)} {_fmt(r23_px)} 0 0 {sw23} {_fmt(px_u3)} {_fmt(py_u3)} "
        f'A {_fmt(r13_px)} {_fmt(r13_px)} 0 0 {sw31} {_fmt(px_u1)} {_fmt(py_u1)} Z"/>'
    )

    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        fill_path,
        _circle_el(vp, (c12.x, c12.y), r12, cls="carrier-ghost", ref="C12_circle"),
        _circle_el(vp, (c13.x, c13.y), r13, cls="carrier-ghost", ref="C13_circle"),
        _circle_el(vp, (c23.x, c23.y), r23, cls="carrier-ghost", ref="C23_circle"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega"),
        _segment_path(vp, (0, 0), (u1.x, u1.y), cls="guide-line", ref="/ O U1 /"),
        _segment_path(vp, (0, 0), (u2.x, u2.y), cls="guide-line", ref="/ O U2 /"),
        _segment_path(vp, (0, 0), (u3.x, u3.y), cls="guide-line", ref="/ O U3 /"),
        _geodesic_path(vp, g12, cls="featured-arc", ref="( U1 U2 )", title="Side U1U2: center (1, 2), r = 2"),
        _geodesic_path(vp, g23, cls="featured-arc", ref="( U2 U3 )", title="Side U2U3: center (-5/3, 0), r = 4/3"),
        _geodesic_path(vp, g13, cls="featured-arc", ref="( U1 U3 )", title="Side U1U3: center (1, -2), r = 2"),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (spg.Point2D(0, 0), "O", "O", "pt-interior", -10, 15),
        (u1, "U₁ (1, 0)", "U1", "pt-ideal", 10, -10),
        (u2, "U₂ (-3/5, 4/5)", "U2", "pt-ideal", -12, -10),
        (u3, "U₃ (-3/5, -4/5)", "U3", "pt-ideal", -12, 18),
        (c23, "C₂₃ (-5/3, 0)", "C23", "pt-inverse", 0, -12),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig4_ideal_hyperbolic_triangle",
        "Rational Pythagorean ideal hyperbolic triangle with zero interior angles and defect pi",
        geom,
        pts,
        lbls,
        "Fig. 4 — Ch. III: Rational Ideal Triangle U₁U₂U₃ — Orthogonal Circles C₁₂=(1,2), C₁₃=(1,-2), C₂₃=(-5/3,0), Angle Sum 0°",
    )


def _render_fig5() -> str:
    """Unit 2/3: Hyperbolic right triangle & Saccheri quadrilateral angular defect."""
    sac = construct_saccheri_triangle_defect()
    a1, a2, b2, b1 = sac.saccheri_vertices
    leg1, leg2 = sac.saccheri_legs
    summit = sac.saccheri_summit
    _o, pt_a, pt_b = sac.triangle_vertices
    vp = _Viewport(width=660, height=520, xmin=-1.24, xmax=1.24, ymin=-1.18, ymax=1.24)

    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega"),
        _segment_path(vp, (-1, 0), (1, 0), cls="guide-line", ref="x_diam"),
        _segment_path(vp, (0, -1), (0, 1), cls="guide-line", ref="y_diam"),
        _segment_path(vp, (a1.x, a1.y), (a2.x, a2.y), cls="geodesic-arc", ref="/ A1 A2 /", title="Saccheri base A1A2"),
        _geodesic_path(
            vp, leg1, start_pt=a1, end_pt=b1, cls="horoparallel-arc", ref="( A1 B1 )", title="Left leg A1B1 (q_UHG = -225/64)"
        ),
        _geodesic_path(
            vp, leg2, start_pt=a2, end_pt=b2, cls="horoparallel-arc", ref="( A2 B2 )", title="Right leg A2B2 (q_UHG = -225/64)"
        ),
        _geodesic_path(
            vp, summit, start_pt=b1, end_pt=b2, cls="featured-arc", ref="( B1 B2 )", title="Saccheri summit B1B2 (acute spread 64/145 < 1)"
        ),
        _geodesic_path(
            vp,
            sac.triangle_hypotenuse,
            start_pt=pt_a,
            end_pt=pt_b,
            cls="ultraparallel-arc",
            ref="( A B )",
            title="Right triangle hypotenuse AB (spread at A, B = 9/34 < 1/2)",
        ),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (spg.Point2D(0, 0), "O", "O", "pt-interior", -10, 16),
        (a1, "A₁ (-1/3, 0)", "A1", "pt-interior", -10, 18),
        (a2, "A₂ (1/3, 0)", "A2", "pt-interior", -2, 18),
        (b1, "B₁ (-17/39, 20/39)", "B1", "pt-featured", -6, -12),
        (b2, "B₂ (17/39, 20/39)", "B2", "pt-featured", 6, -12),
        (pt_a, "A (1/2, 0)", "A", "pt-inverse", 18, -6),
        (pt_b, "B (0, 1/2)", "B", "pt-inverse", 0, -14),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig5_saccheri_angular_defect",
        "Saccheri quadrilateral A1A2B2B1 and right hyperbolic triangle OAB proving acute summit angles",
        geom,
        pts,
        lbls,
        "Fig. 5 — Ch. III: Acute Summit Spread s = 64/145 < 1 in Saccheri A₁A₂B₂B₁ & Right Triangle OAB (s_A = 9/34 < 1/2)",
    )


def _render_fig6() -> str:
    """Unit 3: Poincaré's Heated-Disk Thought Experiment (T ~ R^2 - r^2)."""
    heated = construct_heated_disk_optical_rays()
    vp = _Viewport(width=660, height=520, xmin=-1.25, xmax=1.25, ymin=-1.22, ymax=1.22)
    iso1, iso2, iso3 = heated.isothermals
    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        _circle_el(vp, (0, 0), iso1.radius, cls="isothermal-circle", ref="iso1", title="Isothermal r = 2/5 (T = 21/25 T0)"),
        _circle_el(vp, (0, 0), iso2.radius, cls="isothermal-circle", ref="iso2", title="Isothermal r = 7/10 (T = 51/100 T0)"),
        _circle_el(vp, (0, 0), iso3.radius, cls="isothermal-circle", ref="iso3", title="Isothermal r = 9/10 (T = 19/100 T0)"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega", title="Absolute Zero Boundary T = 0 at r = R"),
    ]
    for idx, ray in enumerate(heated.light_rays, start=1):
        cls = "featured-arc" if idx in (2, 3) else "geodesic-arc"
        geom.append(_geodesic_path(vp, ray, cls=cls, ref=f"ray{idx}", title=f"Refracted optical ray {idx}: n ~ 1/(R^2 - r^2)"))

    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (spg.Point2D(0, 0), "O (T = T₀)", "O", "pt-interior", 0, -12),
        (heated.source, "S (0, -2/5)", "S", "pt-featured", 14, 15),
        (heated.light_rays[0].V, "U₁", "U1", "pt-ideal", -12, -6),
        (heated.light_rays[1].V, "U₂", "U2", "pt-ideal", -10, -10),
        (heated.light_rays[2].V, "U₃", "U3", "pt-ideal", 10, -10),
        (heated.light_rays[3].V, "U₄", "U4", "pt-ideal", 12, -6),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig6_heated_disk_refraction",
        "Poincaré's Heated Disk world with thermal gradient T proportional to R^2 - r^2 and circular light rays",
        geom,
        pts,
        lbls,
        "Fig. 6 — Ch. IV: Poincaré's Heated Disk (T ∝ R² − r², n ∝ (R² − r²)⁻¹) — Circular Light Rays Orthogonal to ∂Ω",
    )


def _render_fig7() -> str:
    """Unit 3/4: Beltrami–Klein projective chord vs Poincaré conformal arc bridge."""
    bridge = construct_beltrami_klein_bridge()
    p1, p2 = bridge.poincare_points
    k1, k2 = bridge.klein_points
    u_pt, v_pt = bridge.poincare_geodesic.U, bridge.poincare_geodesic.V
    vp = _Viewport(width=660, height=520, xmin=-1.18, xmax=1.28, ymin=-1.15, ymax=1.26)
    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega"),
        _segment_path(vp, (0, 0), (k1.x, k1.y), cls="guide-line", ref="/ O K1 /", title="Radial Weierstrass ray OP1 -> K1"),
        _segment_path(vp, (0, 0), (k2.x, k2.y), cls="guide-line", ref="/ O K2 /", title="Radial Weierstrass ray OP2 -> K2"),
        _segment_path(
            vp,
            (u_pt.x, u_pt.y),
            (v_pt.x, v_pt.y),
            cls="klein-chord",
            ref="/ U V /",
            title="Beltrami–Klein projective chord UV (X + Y = 1)",
        ),
        _geodesic_path(
            vp,
            bridge.poincare_geodesic,
            cls="featured-arc",
            ref="( U V )",
            title="Poincaré conformal orthogonal arc UV",
        ),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (spg.Point2D(0, 0), "O (0, 0)", "O", "pt-interior", -10, 16),
        (u_pt, "U (1, 0)", "U", "pt-ideal", 10, 16),
        (v_pt, "V (0, 1)", "V", "pt-ideal", -10, -10),
        (p1, "P₁ (2/5, 1/5)", "P1", "pt-featured", 0, 20),
        (p2, "P₂ (1/5, 2/5)", "P2", "pt-featured", -14, -6),
        (k1, "K₁ (2/3, 1/3)", "K1", "pt-klein", 8, -4),
        (k2, "K₂ (1/3, 2/3)", "K2", "pt-klein", 8, -8),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig7_cayley_klein_beltrami_bridge",
        "Exact radial projection K(P) = 2P/(1+|P|^2) mapping Poincaré arcs to Beltrami-Klein chords",
        geom,
        pts,
        lbls,
        "Fig. 7 — Cayley–Klein / Poincaré Bridge: Radial Ray OP Meets Straight Chord UV at Exact K(P) = 2P / (1 + ‖P‖²)",
    )


def _render_fig8() -> str:
    """Unit 4: Stellar parallax triangle & conventionalist equivalence (Ch. V § 3)."""
    par = construct_stellar_parallax_conventionalism()
    s1, s2, s3 = par.stars
    g12, g23, g31 = par.lobachevsky_rays
    vp = _Viewport(width=660, height=520, xmin=-1.24, xmax=1.24, ymin=-1.18, ymax=1.22)
    geom: list[str] = [
        _circle_el(vp, (0, 0), 1, cls="disk-interior"),
        _circle_el(vp, (0, 0), 1, cls="horizon-circle", ref="Omega"),
        _segment_path(vp, (s1.x, s1.y), (s2.x, s2.y), cls="klein-chord", ref="/ S1 S2 /", title="Euclidean chord S1S2"),
        _segment_path(vp, (s2.x, s2.y), (s3.x, s3.y), cls="klein-chord", ref="/ S2 S3 /", title="Euclidean chord S2S3"),
        _segment_path(vp, (s3.x, s3.y), (s1.x, s1.y), cls="klein-chord", ref="/ S3 S1 /", title="Euclidean chord S3S1"),
        _geodesic_path(
            vp, g12, start_pt=s1, end_pt=s2, cls="featured-arc", ref="( S1 S2 )", title="Lobachevsky geodesic / curved ray S1S2"
        ),
        _geodesic_path(
            vp, g23, start_pt=s2, end_pt=s3, cls="featured-arc", ref="( S2 S3 )", title="Lobachevsky geodesic / curved ray S2S3"
        ),
        _geodesic_path(
            vp, g31, start_pt=s3, end_pt=s1, cls="featured-arc", ref="( S3 S1 )", title="Lobachevsky geodesic / curved ray S3S1"
        ),
    ]
    pts: list[str] = []
    lbls: list[str] = []
    for pt_obj, lbl, ref, p_cls, dx, dy in (
        (s1, "S₁ (-3/5, -2/5)", "S1", "pt-featured", 0, 20),
        (s2, "S₂ (3/5, -2/5)", "S2", "pt-featured", 0, 20),
        (s3, "S₃ (0, 3/4)", "S3", "pt-featured", 0, -12),
    ):
        p_el, l_el = _point_and_label(vp, pt_obj, lbl, cls=p_cls, ref=ref, dx=dx, dy=dy)
        pts.append(p_el)
        lbls.append(l_el)
    return _wrap_svg(
        vp,
        "fig8_stellar_parallax_conventionalism",
        "Stellar parallax triangle comparing Lobachevskian straight geodesics and Euclidean curved light rays",
        geom,
        pts,
        lbls,
        "Fig. 8 — Ch. V: Astronomical Parallax — Lobachevskian Geodesics (α+β+γ < π) vs. Euclidean Space + Curved Optical Rays",
    )


FIGURE_SPECS: dict[str, str] = {
    "fig1_recurrence_continuum_cuts.svg": "Unit 1 — Dedekind Cut & Perceptual Continuum",
    "fig2_poincare_dictionary_inversion.svg": "Unit 2 — Poincaré's Dictionary & Horizon Inversion",
    "fig3_lobachevsky_parallels.svg": "Unit 2 — Lobachevsky Horoparallels & Ultraparallels",
    "fig4_ideal_hyperbolic_triangle.svg": "Unit 2 — Rational Pythagorean Ideal Hyperbolic Triangle",
    "fig5_saccheri_angular_defect.svg": "Unit 2/3 — Saccheri Quadrilateral & Triangle Defect",
    "fig6_heated_disk_refraction.svg": "Unit 3 — Poincaré's Heated-Disk Optical World",
    "fig7_cayley_klein_beltrami_bridge.svg": "Unit 3/4 — Beltrami–Klein / Poincaré Radial Bridge",
    "fig8_stellar_parallax_conventionalism.svg": "Unit 4 — Stellar Parallax & Conventionalism",
}


def render_codex_figure(filename: str) -> str:
    """Render one of the 8 canonical ``.euclid-graphic`` codex figures by filename.

    Args:
        filename: Key in :data:`FIGURE_SPECS` (with or without ``.svg`` suffix).

    Returns:
        Complete UTF-8 SVG document string.

    Raises:
        KeyError: If ``filename`` is not a recognized codex figure.
    """
    key = filename if filename.endswith(".svg") else f"{filename}.svg"
    dispatch = {
        "fig1_recurrence_continuum_cuts.svg": _render_fig1,
        "fig2_poincare_dictionary_inversion.svg": _render_fig2,
        "fig3_lobachevsky_parallels.svg": _render_fig3,
        "fig4_ideal_hyperbolic_triangle.svg": _render_fig4,
        "fig5_saccheri_angular_defect.svg": _render_fig5,
        "fig6_heated_disk_refraction.svg": _render_fig6,
        "fig7_cayley_klein_beltrami_bridge.svg": _render_fig7,
        "fig8_stellar_parallax_conventionalism.svg": _render_fig8,
    }
    if key not in dispatch:
        raise KeyError(f"Unknown figure {filename!r}; expected one of {sorted(dispatch)}")
    return dispatch[key]()


def export_all_codex_figures(output_dir: Path) -> list[Path]:
    """Generate and write all 8 standalone ``.euclid-graphic`` SVGs into ``output_dir``.

    Args:
        output_dir: Target directory (e.g. ``docsrc/_static/figures``).

    Returns:
        Sorted list of written SVG file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for fname in FIGURE_SPECS:
        target = output_dir / fname
        target.write_text(render_codex_figure(fname), encoding="utf-8")
        written.append(target)
    return written


render_figure_svg = render_codex_figure
