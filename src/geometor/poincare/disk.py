r"""Exact symbolic constructions in the Poincaré Conformal Hyperbolic Disk Model.

Implements Henri Poincaré's *Translation Dictionary* (*La Science et l'Hypothèse*,
Part II, Chs. III–V, 1902) inside ``geometor.model`` using 100% exact SymPy symbolic
algebra over :math:`\mathbb{Q}` and closed-form quadratic extensions—with zero
floating-point coordinates.

Because every hyperbolic geodesic in the unit disk
:math:`\mathbb{D} = \{(x, y) : x^2 + y^2 < 1\}` is either a Euclidean diameter through
the center :math:`O = (0, 0)` or a Euclidean circle cutting the horizon circle
:math:`\Omega: x^2 + y^2 = 1` orthogonally, ``geometor.model``'s straightedge-and-compass
kernel constructs hyperbolic lines, circle inversions, limiting horoparallels,
ultraparallels, ideal triangles, Saccheri quadrilaterals, Weierstrass–Beltrami–Klein
projections, and Wildberger's Rational Hyperbolic Quadrances with complete algebraic
exactness.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

import sympy as sp
import sympy.geometry as spg
from geometor.model import (
    Model,
    exact_sign,
    intersect_2d,
    line_spread,
    orientation,
    quadrance,
    zero_test,
)

__all__ = [
    "BeltramiKleinBridgeResult",
    "DedekindCutResult",
    "HeatedDiskResult",
    "HyperbolicGeodesic",
    "HyperbolicMetricReport",
    "IdealTriangleResult",
    "SaccheriDefectResult",
    "StellarParallaxResult",
    "UltraparallelPencil",
    "construct_beltrami_klein_bridge",
    "construct_dedekind_continuum_cut",
    "construct_heated_disk_optical_rays",
    "construct_hyperbolic_geodesic",
    "construct_ideal_hyperbolic_triangle",
    "construct_inversion_in_horizon",
    "construct_saccheri_triangleDefect",
    "construct_saccheri_triangle_defect",
    "construct_stellar_parallax_conventionalism",
    "construct_ultraparallels_through_point",
    "construct_unit_horizon",
    "euclidean_tangent_at_circle_point",
    "hyperbolic_cross_ratio_and_quadrance",
]


def _new_model(name: str) -> Model:
    """Create a quiet, targeted-DAG ``geometor.model.Model`` instance."""
    return Model(name, logger=False, auto_intersect=False)


def _assert_exact_point(pt: spg.Point2D) -> None:
    """Raise ``TypeError`` if ``pt`` contains any floating-point atoms.

    Args:
        pt: Point to validate.

    Raises:
        TypeError: If ``pt`` is not a ``spg.Point`` or contains ``sp.Float``.
    """
    if not isinstance(pt, spg.Point):
        raise TypeError(f"Expected sympy.geometry.Point2D, got {type(pt)!r}")
    if pt.x.has(sp.Float) or pt.y.has(sp.Float):
        raise TypeError(f"Floating-point coordinates are forbidden in geometor.poincare: {pt!r}")


def _simplify_rational_or_radical(expr: sp.Expr) -> sp.Expr:
    """Canonicalize an exact SymPy scalar over Q or simple radical extensions.

    Args:
        expr: Exact SymPy expression.

    Returns:
        Simplified exact SymPy expression with zero ``sp.Float`` atoms.
    """
    if expr.is_Rational:
        return expr
    num, den = sp.fraction(sp.together(expr))
    num_e = sp.expand(num)
    if zero_test(num_e):
        return sp.Integer(0)
    den_e = sp.expand(den)
    if den_e == 1:
        return sp.radsimp(num_e)
    return sp.simplify(sp.radsimp(num_e / den_e))


def _find_point_by_coords(model: Model, x: sp.Expr | int, y: sp.Expr | int) -> spg.Point2D | None:
    """Locate an existing point in ``model`` with exact coordinates ``(x, y)``."""
    sx = sp.sympify(x)
    sy = sp.sympify(y)
    for el in model:
        if isinstance(el, spg.Point2D) and zero_test(el.x - sx) and zero_test(el.y - sy):
            return el
    return None


def _find_unit_circle(model: Model, origin: spg.Point2D) -> spg.Circle | None:
    """Locate the unit horizon circle centered at ``origin`` with radius ``1`` if present."""
    for el in model:
        if (
            isinstance(el, spg.Circle)
            and zero_test(el.center.x - origin.x)
            and zero_test(el.center.y - origin.y)
            and zero_test(sp.sympify(el.radius) ** 2 - 1)
        ):
            return el
    return None


def construct_unit_horizon(
    model: Model,
) -> tuple[spg.Point2D, spg.Point2D, spg.Circle]:
    r"""Ensure the unit horizon circle :math:`\Omega: x^2 + y^2 = 1` exists in ``model``.

    Args:
        model: Active ``geometor.model.Model`` (recommended ``auto_intersect=False``).

    Returns:
        Tuple ``(O, Ex, Omega)`` consisting of center ``O = (0, 0)``, horizon unit point
        ``Ex = (1, 0)``, and Euclidean unit circle ``Omega``.
    """
    origin = _find_point_by_coords(model, 0, 0)
    if origin is None:
        origin = model.set_point(0, 0, classes=["given", "origin"], ID="O", label="O")

    ex_pt = _find_point_by_coords(model, 1, 0)
    if ex_pt is None:
        ex_pt = model.set_point(1, 0, classes=["given", "ideal"], ID="Ex", label="Ex")

    omega = _find_unit_circle(model, origin)
    if omega is None:
        omega = model.construct_circle(origin, ex_pt, classes=["horizon"], ID="Omega")
    return origin, ex_pt, omega


def _compass_perpendicular_bisector(
    model: Model, a: spg.Point2D, b: spg.Point2D
) -> spg.Line2D:
    """Construct the Euclidean perpendicular bisector of segment ``AB`` by equilateral lenses."""
    c_ab = model.construct_circle(a, b, guide=True)
    c_ba = model.construct_circle(b, a, guide=True)
    poles = model.intersect_all(c_ab, c_ba, guide=True)
    return model.construct_line(poles[0], poles[1], guide=True)


def _compass_perpendicular_at(
    model: Model, line: spg.Line2D, foot: spg.Point2D, ref_pt: spg.Point2D
) -> spg.Line2D:
    """Erect the Euclidean perpendicular to ``line`` at ``foot`` using ``ref_pt`` on ``line``."""
    c_step = model.construct_circle(foot, ref_pt, guide=True)
    sym_pt = model.intersect(line, c_step, other_than=ref_pt, guide=True)
    return _compass_perpendicular_bisector(model, ref_pt, sym_pt)


def _compass_circumcenter(
    model: Model, a: spg.Point2D, b: spg.Point2D, c: spg.Point2D
) -> spg.Point2D:
    """Construct the Euclidean circumcenter of non-collinear triangle ``ABC``."""
    bis_ab = _compass_perpendicular_bisector(model, a, b)
    bis_ac = _compass_perpendicular_bisector(model, a, c)
    return model.intersect(bis_ab, bis_ac, guide=True)


def euclidean_tangent_at_circle_point(
    model: Model, circle: spg.Circle, pt_on_circle: spg.Point2D
) -> spg.Line2D:
    """Construct the Euclidean tangent line to ``circle`` at boundary point ``pt_on_circle``.

    Args:
        model: Active ``geometor.model.Model``.
        circle: Circle element whose center is registered or constructible in ``model``.
        pt_on_circle: Point lying on ``circle``.

    Returns:
        Exact ``spg.Line2D`` tangent to ``circle`` at ``pt_on_circle``.
    """
    center = _find_point_by_coords(model, circle.center.x, circle.center.y)
    if center is None:
        center = model.set_point(circle.center.x, circle.center.y, guide=True)
    rad_line = model.construct_line(center, pt_on_circle, guide=True)
    return _compass_perpendicular_at(model, rad_line, pt_on_circle, center)


def construct_inversion_in_horizon(
    model: Model,
    P: spg.Point2D,
    *,
    label: str | None = None,
) -> spg.Point2D:
    r"""Construct the exact Euclidean inverse :math:`P^* = P / \|P\|^2` in :math:`\Omega: x^2+y^2=1`.

    Uses pure straightedge-and-compass geometry inside ``model``:

    - If :math:`P \in \partial\Omega` (:math:`\|P\|^2 = 1`), returns :math:`P` itself.
    - If :math:`0 < \|P\|^2 < 1` (:math:`P \in \mathbb{D} \setminus \{O\}`), erects the chord
      perpendicular to :math:`OP` at :math:`P` meeting :math:`\Omega` at :math:`T_1`, then
      intersects the horizon tangent at :math:`T_1` with ray :math:`OP` (Euclid VI.8:
      :math:`|OP|\cdot|OP^*| = |OT_1|^2 = 1`).
    - If :math:`\|P\|^2 > 1`, constructs the Thales circle on diameter :math:`OP` meeting
      :math:`\Omega` at :math:`T_1, T_2` and intersects polar chord :math:`T_1 T_2` with :math:`OP`.

    Args:
        model: Active ``geometor.model.Model``.
        P: Exact non-origin point ``spg.Point2D``.
        label: Optional label for the constructed inverse point ``P*``.

    Returns:
        Exact inverse point :math:`P^*` satisfying :math:`Q(O, P) \cdot Q(O, P^*) = 1`.

    Raises:
        TypeError: If ``P`` contains floating-point coordinates.
        ValueError: If ``P`` coincides with the horizon center ``O = (0, 0)``.
    """
    _assert_exact_point(P)
    origin, _ex, omega = construct_unit_horizon(model)
    q_op = quadrance(origin, P)
    if zero_test(q_op):
        raise ValueError("Origin O = (0, 0) maps to the point at infinity under horizon inversion.")
    if zero_test(q_op - 1):
        if P not in model:
            P = model.set_point(P.x, P.y, classes=["given", "ideal"])
        return P

    existing = _find_point_by_coords(model, P.x, P.y)
    P = existing if existing is not None else model.set_point(P.x, P.y, classes=["given"])

    ray_op = model.construct_line(origin, P, classes=["guide", "inversion-ray"], guide=True)

    with model.subconstruction("horizon_inversion") as scope:
        if exact_sign(q_op - 1) < 0:
            chord_perp = _compass_perpendicular_at(model, ray_op, P, origin)
            t1 = model.intersect(chord_perp, omega, index=0, guide=True)
            rad_ot1 = model.construct_line(origin, t1, guide=True)
            polar_rel = _compass_perpendicular_at(model, rad_ot1, t1, origin)
        else:
            bis_op = _compass_perpendicular_bisector(model, origin, P)
            mid_op = model.intersect(bis_op, ray_op, guide=True)
            thales = model.construct_circle(mid_op, origin, guide=True)
            tangency_pts = model.intersect_all(thales, omega, guide=True)
            polar_rel = model.construct_line(tangency_pts[0], tangency_pts[1], guide=True)

        p_star = model.intersect(
            polar_rel,
            ray_op,
            classes=["inverse", "result"],
            label=label or "",
        )
        scope.keep(p_star)

    if not zero_test(quadrance(origin, P) * quadrance(origin, p_star) - 1):
        raise AssertionError("Horizon inversion failed exactness check Q(O,P)*Q(O,P*) == 1.")
    return p_star


@dataclass(frozen=True)
class HyperbolicGeodesic:
    r"""Exact hyperbolic geodesic in the Poincaré Conformal Disk :math:`\mathbb{D}`.

    Supports both named attribute inspection (``.carrier``, ``.U``, ``.V``,
    ``.ideal_points``) and 3-tuple unpacking ``carrier, U, V = geodesic``.
    Stores the underlying ``spg.Line2D`` diameter or orthogonal ``spg.Circle``
    carrier, ordered ideal horizon endpoints ``(U, V)``, optional inverse point
    :math:`P^*`, Euclidean circle center, squared radius :math:`r^2 = |OC|^2 - 1`,
    and exact orthogonality residual :math:`|OC|^2 - r^2 - 1 = 0`.
    """

    carrier: spg.Line2D | spg.Circle
    U: spg.Point2D
    V: spg.Point2D
    inverse_point: spg.Point2D | None = None
    is_diameter: bool = False
    center: spg.Point2D | None = None
    radius_squared: sp.Expr | None = None
    orthogonality_residual: sp.Expr = sp.Integer(0)

    @property
    def ideal_points(self) -> tuple[spg.Point2D, spg.Point2D]:
        r"""Return ordered ideal boundary endpoints ``(U, V)`` on :math:`\partial\Omega`."""
        return (self.U, self.V)

    def __iter__(self) -> Iterator[spg.Line2D | spg.Circle | spg.Point2D]:
        """Yield ``(carrier, U, V)`` for ergonomic tuple unpacking."""
        yield self.carrier
        yield self.U
        yield self.V


def _order_ideal_endpoints(
    P: spg.Point2D,
    Q: spg.Point2D,
    u_raw: spg.Point2D,
    v_raw: spg.Point2D,
) -> tuple[spg.Point2D, spg.Point2D]:
    """Order ideal endpoints ``(U, V)`` along the geodesic so ``U -> P -> Q -> V``."""
    if (zero_test(P.x - u_raw.x) and zero_test(P.y - u_raw.y)) or (
        zero_test(Q.x - v_raw.x) and zero_test(Q.y - v_raw.y)
    ):
        return (u_raw, v_raw)
    if (zero_test(P.x - v_raw.x) and zero_test(P.y - v_raw.y)) or (
        zero_test(Q.x - u_raw.x) and zero_test(Q.y - u_raw.y)
    ):
        return (v_raw, u_raw)

    lhs = quadrance(P, v_raw) * quadrance(Q, u_raw)
    rhs = quadrance(P, u_raw) * quadrance(Q, v_raw)
    if exact_sign(lhs - rhs) < 0:
        return (v_raw, u_raw)
    return (u_raw, v_raw)


def construct_hyperbolic_geodesic(
    model: Model,
    P: spg.Point2D,
    Q: spg.Point2D,
    *,
    classes: list[str] | None = None,
    label: str | None = None,
) -> HyperbolicGeodesic:
    r"""Construct the unique hyperbolic geodesic through :math:`P, Q \in \overline{\mathbb{D}}`.

    Implements Poincaré's Translation Dictionary (*La Science et l'Hypothèse*, Ch. III):

    - When :math:`O, P, Q` are collinear, constructs the Euclidean diameter line :math:`PQ`
      and intersects it with :math:`\Omega` to obtain antipodal ideal points :math:`U, V`.
    - When :math:`O, P, Q` are non-collinear and at least one point lies strictly inside
      :math:`\mathbb{D}`, constructs its horizon inverse :math:`P^* = P / \|P\|^2` and
      circumscribes the unique Euclidean circle through :math:`(P, Q, P^*)`. By power-of-a-point
      (:math:`|OP|\cdot|OP^*| = 1 = R_\Omega^2`), this circle cuts :math:`\Omega` orthogonally
      at two exact ideal points :math:`U, V \in \partial\Omega`.
    - When both :math:`P` and :math:`Q` lie on :math:`\partial\Omega` (ideal geodesic),
      intersects the Euclidean horizon tangents at :math:`P` and :math:`Q` to locate the
      exact orthogonal circle center :math:`C`.

    Args:
        model: Active ``geometor.model.Model``.
        P: First point in :math:`\overline{\mathbb{D}}`.
        Q: Second distinct point in :math:`\overline{\mathbb{D}}`.
        classes: Optional CSS/semantic class tags for the constructed geodesic element.
        label: Optional identifier for the constructed geodesic element.

    Returns:
        Populated :class:`HyperbolicGeodesic` dataclass (unpackable as ``(carrier, U, V)``).

    Raises:
        TypeError: If ``P`` or ``Q`` contains floating-point coordinates.
        ValueError: If ``P == Q`` or either point lies outside :math:`\overline{\mathbb{D}}`.
    """
    _assert_exact_point(P)
    _assert_exact_point(Q)
    if zero_test(P.x - Q.x) and zero_test(P.y - Q.y):
        raise ValueError("Two distinct points are required to determine a hyperbolic geodesic.")

    origin, _ex, omega = construct_unit_horizon(model)
    q_op = quadrance(origin, P)
    q_oq = quadrance(origin, Q)
    if exact_sign(q_op - 1) > 0 or exact_sign(q_oq - 1) > 0:
        raise ValueError("Geodesic points P and Q must lie in the closed unit disk x^2 + y^2 <= 1.")

    p_found = _find_point_by_coords(model, P.x, P.y)
    P = p_found if p_found is not None else model.set_point(P.x, P.y, classes=["given"])
    q_found = _find_point_by_coords(model, Q.x, Q.y)
    Q = q_found if q_found is not None else model.set_point(Q.x, Q.y, classes=["given"])

    geo_classes = list(classes) if classes is not None else ["geodesic"]

    if orientation(origin, P, Q) == 0:
        diam = model.construct_line(P, Q, classes=geo_classes + ["diameter"], ID=label or "")
        ideal_hits = model.intersect_all(diam, omega, classes=["ideal"])
        u_pt, v_pt = _order_ideal_endpoints(P, Q, ideal_hits[0], ideal_hits[1])
        return HyperbolicGeodesic(
            carrier=diam,
            U=u_pt,
            V=v_pt,
            inverse_point=None,
            is_diameter=True,
            center=None,
            radius_squared=None,
            orthogonality_residual=sp.Integer(0),
        )

    p_on_bdry = zero_test(q_op - 1)
    q_on_bdry = zero_test(q_oq - 1)

    if p_on_bdry and q_on_bdry:
        with model.subconstruction("ideal_geodesic_center") as scope:
            tan_p = euclidean_tangent_at_circle_point(model, omega, P)
            tan_q = euclidean_tangent_at_circle_point(model, omega, Q)
            center_pt = model.intersect(tan_p, tan_q, classes=["aux-center"])
            scope.keep(center_pt)
        c_geo = model.construct_circle(center_pt, P, classes=geo_classes, ID=label or "")
        model.assert_incident(Q, c_geo)
        r_sq = quadrance(center_pt, P)
        orth_res = _simplify_rational_or_radical(quadrance(origin, center_pt) - r_sq - 1)
        if not zero_test(orth_res):
            raise AssertionError(f"Ideal geodesic circle failed orthogonality check: {orth_res}")
        return HyperbolicGeodesic(
            carrier=c_geo,
            U=P,
            V=Q,
            inverse_point=None,
            is_diameter=False,
            center=center_pt,
            radius_squared=r_sq,
            orthogonality_residual=orth_res,
        )

    pivot = Q if p_on_bdry else P
    other = P if p_on_bdry else Q
    pivot_star = construct_inversion_in_horizon(model, pivot)

    with model.subconstruction("orthogonal_circumcenter") as scope:
        center_pt = _compass_circumcenter(model, pivot, other, pivot_star)
        scope.keep(center_pt)

    c_geo = model.construct_circle(center_pt, pivot, classes=geo_classes, ID=label or "")
    model.assert_incident(other, c_geo)
    model.assert_incident(pivot_star, c_geo)

    r_sq = quadrance(center_pt, pivot)
    orth_res = _simplify_rational_or_radical(quadrance(origin, center_pt) - r_sq - 1)
    if not zero_test(orth_res):
        raise AssertionError(f"Geodesic circle failed orthogonality to horizon: {orth_res}")

    ideal_hits = model.intersect_all(c_geo, omega, classes=["ideal"])
    u_pt, v_pt = _order_ideal_endpoints(P, Q, ideal_hits[0], ideal_hits[1])
    return HyperbolicGeodesic(
        carrier=c_geo,
        U=u_pt,
        V=v_pt,
        inverse_point=pivot_star,
        is_diameter=False,
        center=center_pt,
        radius_squared=r_sq,
        orthogonality_residual=orth_res,
    )


@dataclass(frozen=True)
class HyperbolicMetricReport:
    r"""Exact cross-ratio and Rational Hyperbolic Quadrance invariants for :math:`P, Q \in \mathbb{D}`.

    Unites Poincaré's cross-ratio logarithmic distance with Norman Wildberger's
    transcendental-free Universal Hyperbolic Geometry (UHG) and Cayley–Klein quadrances:

    - ``cross_ratio``: :math:`\chi(P, Q; U, V) = \frac{|PV|\cdot|QU|}{|PU|\cdot|QV|} \ge 1`
    - ``cross_ratio_squared``: :math:`\chi^2(P, Q; U, V) = \frac{Q(P,V)\,Q(Q,U)}{Q(P,U)\,Q(Q,V)}`
    - ``poincare_distance``: :math:`d_{\mathbb{H}}(P, Q) = \ln \chi(P, Q; U, V)`
    - ``conformal_quadrance``: :math:`\tau(P, Q) = \frac{\|P-Q\|^2}{\|1 - \bar{P}Q\|^2} = \left(\frac{\chi-1}{\chi+1}\right)^2 \in [0, 1)`
    - ``wildberger_uhg_quadrance``: :math:`q_{\text{UHG}}(P, Q) = -\frac{4\tau}{(1-\tau)^2} = -\sinh^2 d_{\mathbb{H}}(P, Q) \in \mathbb{Q}(P, Q)`
    - ``cayley_klein_quadrance``: :math:`q_{\text{CK}}(P, Q) = \frac{4\tau}{(1+\tau)^2} = \tanh^2 d_{\mathbb{H}}(P, Q) \in [0, 1)`
    - ``isometric_delta``: :math:`\delta(P, Q) = \frac{2\|P-Q\|^2}{(1-\|P\|^2)(1-\|Q\|^2)} = \cosh d_{\mathbb{H}}(P, Q) - 1`
    """

    cross_ratio: sp.Expr
    cross_ratio_squared: sp.Expr
    poincare_distance: sp.Expr
    conformal_quadrance: sp.Expr
    wildberger_uhg_quadrance: sp.Expr
    cayley_klein_quadrance: sp.Expr
    isometric_delta: sp.Expr


def hyperbolic_cross_ratio_and_quadrance(
    P: spg.Point2D,
    Q: spg.Point2D,
    U: spg.Point2D | None = None,
    V: spg.Point2D | None = None,
) -> HyperbolicMetricReport:
    r"""Compute the exact algebraic cross-ratio and Wildberger's Rational Hyperbolic Quadrance.

    Eliminates transcendental logarithms for algebraic comparison while verifying the
    exact polynomial bridge :math:`(1 - \tau)^2 (\chi^2 + 1)^2 = 4 (1 + \tau)^2 \chi^2`
    between the 4-point circle chord cross-ratio :math:`\chi(P, Q; U, V)` and the
    purely rational conformal/UHG quadrances over :math:`\mathbb{Q}`.

    Args:
        P: First interior point :math:`P \in \mathbb{D}`.
        Q: Second interior point :math:`Q \in \mathbb{D}`.
        U: First ideal endpoint on :math:`\partial\Omega` (constructed automatically if ``None``).
        V: Second ideal endpoint on :math:`\partial\Omega` (constructed automatically if ``None``).

    Returns:
        Populated :class:`HyperbolicMetricReport` with 100% exact SymPy invariants.

    Raises:
        TypeError: If any point contains ``sp.Float`` coordinates.
        ValueError: If ``P`` or ``Q`` does not lie strictly inside :math:`\mathbb{D}`.
    """
    _assert_exact_point(P)
    _assert_exact_point(Q)

    x1, y1 = sp.sympify(P.x), sp.sympify(P.y)
    x2, y2 = sp.sympify(Q.x), sp.sympify(Q.y)
    norm_p = x1**2 + y1**2
    norm_q = x2**2 + y2**2
    if not (exact_sign(norm_p - 1) < 0 and exact_sign(norm_q - 1) < 0):
        raise ValueError("Points P and Q must lie strictly inside the unit disk x^2 + y^2 < 1.")

    q_euc = (x2 - x1) ** 2 + (y2 - y1) ** 2
    if zero_test(q_euc):
        return HyperbolicMetricReport(
            cross_ratio=sp.Integer(1),
            cross_ratio_squared=sp.Integer(1),
            poincare_distance=sp.Integer(0),
            conformal_quadrance=sp.Integer(0),
            wildberger_uhg_quadrance=sp.Integer(0),
            cayley_klein_quadrance=sp.Integer(0),
            isometric_delta=sp.Integer(0),
        )

    denom_conf = (1 - x1 * x2 - y1 * y2) ** 2 + (x1 * y2 - x2 * y1) ** 2
    tau = _simplify_rational_or_radical(q_euc / denom_conf)
    delta = _simplify_rational_or_radical((2 * q_euc) / ((1 - norm_p) * (1 - norm_q)))
    q_uhg = _simplify_rational_or_radical((-4 * tau) / (1 - tau) ** 2)
    q_ck = _simplify_rational_or_radical((4 * tau) / (1 + tau) ** 2)

    if U is None or V is None:
        aux_model = _new_model("metric_probe")
        geo = construct_hyperbolic_geodesic(aux_model, P, Q)
        U, V = geo.U, geo.V
    else:
        _assert_exact_point(U)
        _assert_exact_point(V)
        U, V = _order_ideal_endpoints(P, Q, U, V)

    chi_sq_num = quadrance(P, V) * quadrance(Q, U)
    chi_sq_den = quadrance(P, U) * quadrance(Q, V)
    chi_sq = _simplify_rational_or_radical(chi_sq_num / chi_sq_den)
    chi = _simplify_rational_or_radical(sp.sqrt(chi_sq))

    bridge_poly = (1 - tau) ** 2 * (chi_sq + 1) ** 2 - 4 * (1 + tau) ** 2 * chi_sq
    if not zero_test(bridge_poly):
        raise AssertionError(
            "Ideal points (U, V) do not lie on the hyperbolic geodesic through P and Q."
        )

    return HyperbolicMetricReport(
        cross_ratio=chi,
        cross_ratio_squared=chi_sq,
        poincare_distance=sp.log(chi),
        conformal_quadrance=tau,
        wildberger_uhg_quadrance=q_uhg,
        cayley_klein_quadrance=q_ck,
        isometric_delta=delta,
    )


@dataclass(frozen=True)
class UltraparallelPencil:
    """Hyperbolic parallel & ultraparallel pencil demonstrating Postulate V independence."""

    model: Model
    base_geodesic: HyperbolicGeodesic
    point: spg.Point2D
    limiting_parallels: tuple[HyperbolicGeodesic, HyperbolicGeodesic]
    ultraparallels: tuple[HyperbolicGeodesic, HyperbolicGeodesic]


def _geodesics_disjoint_in_closed_disk(
    g1: HyperbolicGeodesic, g2: HyperbolicGeodesic
) -> bool:
    """Verify exact algebraic disjointness of two geodesics on the closed unit disk."""
    pts = intersect_2d(g1.carrier, g2.carrier)
    for pt in pts:
        if isinstance(pt, spg.Point2D):
            q_norm = pt.x**2 + pt.y**2
            if exact_sign(q_norm - 1) <= 0:
                return False
    return True


def construct_ultraparallels_through_point(
    model: Model | None = None,
    L_hyp: HyperbolicGeodesic | spg.Circle | spg.Line2D | None = None,
    P: spg.Point2D | None = None,
) -> UltraparallelPencil:
    r"""Construct two limiting horoparallels and two ultraparallels to ``L_hyp`` through ``P``.

    Demonstrates inside ``geometor.model`` that Euclid's Fifth Postulate fails in the
    Poincaré disk while Postulates I–IV (in Poincaré's dictionary) hold identically:
    through a single point :math:`P \notin L_{\text{hyp}}`, infinitely many hyperbolic
    lines fail to meet :math:`L_{\text{hyp}}`.

    Args:
        model: Optional ``geometor.model.Model`` (created if ``None``).
        L_hyp: Reference hyperbolic geodesic (or its ``Circle``/``Line2D`` carrier). If
            omitted, constructs the rational geodesic with ideal endpoints
            :math:`(\frac{4}{5}, -\frac{3}{5})` and :math:`(-\frac{4}{5}, -\frac{3}{5})`.
        P: Exterior point in :math:`\mathbb{D} \setminus L_{\text{hyp}}`. Defaults to
            :math:`(\frac{1}{6}, \frac{2}{5})`.

    Returns:
        Verified :class:`UltraparallelPencil` with exact disjointness over :math:`\overline{\mathbb{D}}`.
    """
    if model is None:
        model = _new_model("lobachevsky_ultraparallels")
    origin, _ex, omega = construct_unit_horizon(model)

    if L_hyp is None:
        u_base = model.set_point(sp.Rational(4, 5), sp.Rational(-3, 5), classes=["ideal"], label="UL")
        v_base = model.set_point(sp.Rational(-4, 5), sp.Rational(-3, 5), classes=["ideal"], label="VL")
        base_geo = construct_hyperbolic_geodesic(
            model, u_base, v_base, classes=["geodesic", "base-geodesic"], label="L_hyp"
        )
    elif isinstance(L_hyp, HyperbolicGeodesic):
        base_geo = L_hyp
    else:
        hits = model.intersect_all(L_hyp, omega, classes=["ideal"])
        base_geo = HyperbolicGeodesic(
            carrier=L_hyp,
            U=hits[0],
            V=hits[1],
            is_diameter=isinstance(L_hyp, spg.Line2D),
        )

    if P is None:
        P = model.set_point(sp.Rational(1, 6), sp.Rational(2, 5), classes=["given"], label="P")
    else:
        _assert_exact_point(P)
        found_p = _find_point_by_coords(model, P.x, P.y)
        P = found_p if found_p is not None else model.set_point(P.x, P.y, classes=["given"], label="P")

    if base_geo.carrier.contains(P):
        raise ValueError("Point P must not lie on the base hyperbolic geodesic L_hyp.")

    lim_1 = construct_hyperbolic_geodesic(
        model, P, base_geo.U, classes=["geodesic", "horoparallel"], label="l1"
    )
    lim_2 = construct_hyperbolic_geodesic(
        model, P, base_geo.V, classes=["geodesic", "horoparallel"], label="l2"
    )

    candidate_ideals = [
        spg.Point2D(sp.Integer(-1), sp.Integer(0)),
        spg.Point2D(sp.Integer(1), sp.Integer(0)),
        spg.Point2D(sp.Rational(-4, 5), sp.Rational(3, 5)),
        spg.Point2D(sp.Rational(4, 5), sp.Rational(3, 5)),
        spg.Point2D(sp.Rational(-3, 5), sp.Rational(4, 5)),
        spg.Point2D(sp.Rational(3, 5), sp.Rational(4, 5)),
        spg.Point2D(sp.Integer(0), sp.Integer(1)),
        spg.Point2D(sp.Rational(5, 13), sp.Rational(12, 13)),
        spg.Point2D(sp.Rational(-5, 13), sp.Rational(12, 13)),
        spg.Point2D(sp.Rational(12, 13), sp.Rational(5, 13)),
        spg.Point2D(sp.Rational(-12, 13), sp.Rational(5, 13)),
    ]

    found_ultras: list[HyperbolicGeodesic] = []
    for cand in candidate_ideals:
        if (zero_test(cand.x - base_geo.U.x) and zero_test(cand.y - base_geo.U.y)) or (
            zero_test(cand.x - base_geo.V.x) and zero_test(cand.y - base_geo.V.y)
        ):
            continue
        probe = _new_model("ultra_probe")
        probe_geo = construct_hyperbolic_geodesic(probe, P, cand)
        if _geodesics_disjoint_in_closed_disk(base_geo, probe_geo):
            if all(not probe_geo.carrier.equals(prev.carrier) for prev in found_ultras):
                idx = len(found_ultras) + 1
                cand_pt = _find_point_by_coords(model, cand.x, cand.y)
                if cand_pt is None:
                    cand_pt = model.set_point(cand.x, cand.y, classes=["ideal"], label=f"W{idx}")
                real_geo = construct_hyperbolic_geodesic(
                    model,
                    P,
                    cand_pt,
                    classes=["geodesic", "ultraparallel"],
                    label=f"m{idx}",
                )
                found_ultras.append(real_geo)
                if len(found_ultras) == 2:
                    break

    if len(found_ultras) < 2:
        raise RuntimeError("Could not find two rational ultraparallels for the supplied (L_hyp, P).")

    _ = origin
    return UltraparallelPencil(
        model=model,
        base_geodesic=base_geo,
        point=P,
        limiting_parallels=(lim_1, lim_2),
        ultraparallels=(found_ultras[0], found_ultras[1]),
    )


@dataclass(frozen=True)
class IdealTriangleResult:
    r"""Exact Pythagorean ideal hyperbolic triangle on :math:`\partial\Omega` with :math:`0^\circ` angles."""

    model: Model
    vertices: tuple[spg.Point2D, spg.Point2D, spg.Point2D]
    sides: tuple[HyperbolicGeodesic, HyperbolicGeodesic, HyperbolicGeodesic]
    centers: tuple[spg.Point2D, spg.Point2D, spg.Point2D]
    radii: tuple[sp.Rational, sp.Rational, sp.Rational]
    vertex_spreads: tuple[sp.Expr, sp.Expr, sp.Expr]
    angular_defect: sp.Expr


def construct_ideal_hyperbolic_triangle(model: Model | None = None) -> IdealTriangleResult:
    r"""Construct the exact rational ideal hyperbolic triangle on :math:`U_1, U_2, U_3 \in \partial\Omega`.

    Uses Pythagorean horizon points :math:`U_1 = (1, 0)`,
    :math:`U_2 = (-\frac{3}{5}, \frac{4}{5})`, and
    :math:`U_3 = (-\frac{3}{5}, -\frac{4}{5})`. Every side is an orthogonal Euclidean
    circle with 100% rational center and rational radius:

    - :math:`C_{12} = (1, 2),\; r_{12} = 2`
    - :math:`C_{13} = (1, -2),\; r_{13} = 2`
    - :math:`C_{23} = (-\frac{5}{3}, 0),\; r_{23} = \frac{4}{3}`

    Meeting tangentially along radii :math:`OU_1, OU_2, OU_3` with interior spreads ``(0, 0, 0)``
    (:math:`0^\circ` angle sum, maximal Gauss–Bonnet defect :math:`\pi`).

    Args:
        model: Optional ``geometor.model.Model`` (created if ``None``).

    Returns:
        Verified :class:`IdealTriangleResult`.
    """
    if model is None:
        model = _new_model("ideal_hyperbolic_triangle")
    origin, u1, omega = construct_unit_horizon(model)
    u2 = model.set_point(sp.Rational(-3, 5), sp.Rational(4, 5), classes=["given", "ideal"], label="U2")
    u3 = model.set_point(sp.Rational(-3, 5), sp.Rational(-4, 5), classes=["given", "ideal"], label="U3")

    g12 = construct_hyperbolic_geodesic(
        model, u1, u2, classes=["geodesic", "ideal-side"], label="g12"
    )
    g13 = construct_hyperbolic_geodesic(
        model, u1, u3, classes=["geodesic", "ideal-side"], label="g13"
    )
    g23 = construct_hyperbolic_geodesic(
        model, u2, u3, classes=["geodesic", "ideal-side"], label="g23"
    )

    assert isinstance(g12.carrier, spg.Circle) and g12.center is not None
    assert isinstance(g13.carrier, spg.Circle) and g13.center is not None
    assert isinstance(g23.carrier, spg.Circle) and g23.center is not None

    with model.subconstruction("ideal_tangents"):
        t1_a = euclidean_tangent_at_circle_point(model, g12.carrier, u1)
        t1_b = euclidean_tangent_at_circle_point(model, g13.carrier, u1)
        t2_a = euclidean_tangent_at_circle_point(model, g12.carrier, u2)
        t2_b = euclidean_tangent_at_circle_point(model, g23.carrier, u2)
        t3_a = euclidean_tangent_at_circle_point(model, g13.carrier, u3)
        t3_b = euclidean_tangent_at_circle_point(model, g23.carrier, u3)

    s1 = line_spread(t1_a, t1_b)
    s2 = line_spread(t2_a, t2_b)
    s3 = line_spread(t3_a, t3_b)
    if not (zero_test(s1) and zero_test(s2) and zero_test(s3)):
        raise AssertionError(f"Ideal triangle spreads must vanish identically: {(s1, s2, s3)}")

    _ = (origin, omega)
    return IdealTriangleResult(
        model=model,
        vertices=(u1, u2, u3),
        sides=(g12, g13, g23),
        centers=(g12.center, g13.center, g23.center),
        radii=(
            sp.Rational(g12.carrier.radius),
            sp.Rational(g13.carrier.radius),
            sp.Rational(g23.carrier.radius),
        ),
        vertex_spreads=(s1, s2, s3),
        angular_defect=sp.pi,
    )


@dataclass(frozen=True)
class SaccheriDefectResult:
    """Exact rational hyperbolic right-triangle & Saccheri quadrilateral defect proof."""

    model: Model
    triangle_vertices: tuple[spg.Point2D, spg.Point2D, spg.Point2D]
    triangle_hypotenuse: HyperbolicGeodesic
    triangle_spreads: tuple[sp.Expr, sp.Expr, sp.Expr]
    triangle_defect: sp.Expr
    saccheri_vertices: tuple[spg.Point2D, spg.Point2D, spg.Point2D, spg.Point2D]
    saccheri_base: HyperbolicGeodesic
    saccheri_legs: tuple[HyperbolicGeodesic, HyperbolicGeodesic]
    saccheri_summit: HyperbolicGeodesic
    saccheri_base_spreads: tuple[sp.Expr, sp.Expr]
    saccheri_summit_spreads: tuple[sp.Expr, sp.Expr]
    saccheri_leg_uhg_quadrances: tuple[sp.Expr, sp.Expr]
    saccheri_defect: sp.Expr


def construct_saccheri_triangleDefect(model: Model | None = None) -> SaccheriDefectResult:
    """Construct an exact hyperbolic right triangle & Saccheri quadrilateral proving defect > 0.

    Args:
        model: Optional ``geometor.model.Model`` (created if ``None``).

    Returns:
        Verified :class:`SaccheriDefectResult` with 100% rational spreads and quadrances.
    """
    if model is None:
        model = _new_model("saccheri_triangle_defect")
    origin, _ex, _omega = construct_unit_horizon(model)

    # 1. Exact rational hyperbolic right triangle OAB
    pt_a = model.set_point(sp.Rational(1, 2), 0, classes=["given"], label="A")
    pt_b = model.set_point(0, sp.Rational(1, 2), classes=["given"], label="B")
    geo_oa = construct_hyperbolic_geodesic(model, origin, pt_a, classes=["geodesic"], label="gOA")
    geo_ob = construct_hyperbolic_geodesic(model, origin, pt_b, classes=["geodesic"], label="gOB")
    geo_ab = construct_hyperbolic_geodesic(
        model, pt_a, pt_b, classes=["geodesic", "featured"], label="gAB"
    )
    assert isinstance(geo_oa.carrier, spg.Line2D)
    assert isinstance(geo_ob.carrier, spg.Line2D)
    assert isinstance(geo_ab.carrier, spg.Circle)

    with model.subconstruction("triangle_tangents"):
        tan_ab_at_a = euclidean_tangent_at_circle_point(model, geo_ab.carrier, pt_a)
        tan_ab_at_b = euclidean_tangent_at_circle_point(model, geo_ab.carrier, pt_b)

    s_o = line_spread(geo_oa.carrier, geo_ob.carrier)
    s_a = line_spread(geo_oa.carrier, tan_ab_at_a)
    s_b = line_spread(geo_ob.carrier, tan_ab_at_b)
    if not (
        zero_test(s_o - 1)
        and zero_test(s_a - sp.Rational(9, 34))
        and zero_test(s_b - sp.Rational(9, 34))
    ):
        raise AssertionError(f"Unexpected triangle tangent spreads: {(s_o, s_a, s_b)}")

    tri_defect = sp.pi / 2 - 2 * sp.atan(sp.Rational(3, 5))

    # 2. Exact rational Saccheri quadrilateral A1 A2 B2 B1
    a1 = model.set_point(sp.Rational(-1, 3), 0, classes=["given", "saccheri"], label="A1")
    a2 = model.set_point(sp.Rational(1, 3), 0, classes=["given", "saccheri"], label="A2")
    b1 = model.set_point(
        sp.Rational(-17, 39), sp.Rational(20, 39), classes=["given", "saccheri"], label="B1"
    )
    b2 = model.set_point(
        sp.Rational(17, 39), sp.Rational(20, 39), classes=["given", "saccheri"], label="B2"
    )

    sac_base = geo_oa
    sac_leg1 = construct_hyperbolic_geodesic(
        model, a1, b1, classes=["geodesic", "saccheri-leg"], label="leg1"
    )
    sac_leg2 = construct_hyperbolic_geodesic(
        model, a2, b2, classes=["geodesic", "saccheri-leg"], label="leg2"
    )
    sac_summit = construct_hyperbolic_geodesic(
        model, b1, b2, classes=["geodesic", "saccheri-summit"], label="summit"
    )
    assert isinstance(sac_leg1.carrier, spg.Circle)
    assert isinstance(sac_leg2.carrier, spg.Circle)
    assert isinstance(sac_summit.carrier, spg.Circle)

    with model.subconstruction("saccheri_tangents"):
        tan_leg1_base = euclidean_tangent_at_circle_point(model, sac_leg1.carrier, a1)
        tan_leg2_base = euclidean_tangent_at_circle_point(model, sac_leg2.carrier, a2)
        tan_leg1_top = euclidean_tangent_at_circle_point(model, sac_leg1.carrier, b1)
        tan_leg2_top = euclidean_tangent_at_circle_point(model, sac_leg2.carrier, b2)
        tan_sum_b1 = euclidean_tangent_at_circle_point(model, sac_summit.carrier, b1)
        tan_sum_b2 = euclidean_tangent_at_circle_point(model, sac_summit.carrier, b2)

    sb1 = line_spread(sac_base.carrier, tan_leg1_base)
    sb2 = line_spread(sac_base.carrier, tan_leg2_base)
    ss1 = line_spread(tan_leg1_top, tan_sum_b1)
    ss2 = line_spread(tan_leg2_top, tan_sum_b2)

    m_leg1 = hyperbolic_cross_ratio_and_quadrance(a1, b1, sac_leg1.U, sac_leg1.V)
    m_leg2 = hyperbolic_cross_ratio_and_quadrance(a2, b2, sac_leg2.U, sac_leg2.V)
    if not (
        zero_test(sb1 - 1)
        and zero_test(sb2 - 1)
        and zero_test(ss1 - sp.Rational(64, 145))
        and zero_test(ss2 - sp.Rational(64, 145))
        and zero_test(m_leg1.wildberger_uhg_quadrance - m_leg2.wildberger_uhg_quadrance)
    ):
        raise AssertionError("Saccheri quadrilateral exactness check failed.")

    sac_defect = sp.pi - 2 * sp.atan(sp.Rational(8, 9))

    return SaccheriDefectResult(
        model=model,
        triangle_vertices=(origin, pt_a, pt_b),
        triangle_hypotenuse=geo_ab,
        triangle_spreads=(s_o, s_a, s_b),
        triangle_defect=tri_defect,
        saccheri_vertices=(a1, a2, b2, b1),
        saccheri_base=sac_base,
        saccheri_legs=(sac_leg1, sac_leg2),
        saccheri_summit=sac_summit,
        saccheri_base_spreads=(sb1, sb2),
        saccheri_summit_spreads=(ss1, ss2),
        saccheri_leg_uhg_quadrances=(
            m_leg1.wildberger_uhg_quadrance,
            m_leg2.wildberger_uhg_quadrance,
        ),
        saccheri_defect=sac_defect,
    )


construct_saccheri_triangle_defect = construct_saccheri_triangleDefect


@dataclass(frozen=True)
class DedekindCutResult:
    r"""Exact model for Unit 1: Dedekind continuum cut (:math:`\sqrt{2}/2`) & rational thresholds."""

    model: Model
    cut_point: spg.Point2D
    lower_rational: spg.Point2D
    upper_rational: spg.Point2D


def construct_dedekind_continuum_cut(model: Model | None = None) -> DedekindCutResult:
    """Construct the incommensurable diagonal-circle Dedekind cut for Chs. I–II."""
    if model is None:
        model = _new_model("dedekind_continuum_cut")
    origin, ex_pt, omega = construct_unit_horizon(model)
    ey_pt = model.set_point(0, 1, classes=["given", "ideal"], label="Ey")
    sq_corner = model.set_point(1, 1, classes=["given"], label="S")
    x_axis = model.construct_line(origin, ex_pt, classes=["guide"], ID="x_axis")
    _ = model.construct_line(origin, ey_pt, classes=["guide"], ID="y_axis")
    diag = model.construct_line(origin, sq_corner, classes=["geodesic", "diameter"], ID="diag")
    diag_hits = model.intersect_all(diag, omega, classes=["result"])
    d_cut = next(pt for pt in diag_hits if exact_sign(pt.x) > 0)

    with model.subconstruction("dedekind_projection") as scope:
        c_do = model.construct_circle(d_cut, origin, guide=True)
        far_x = model.intersect(x_axis, c_do, other_than=origin, guide=True)
        drop = _compass_perpendicular_bisector(model, origin, far_x)
        dx_pt = model.intersect(drop, x_axis, classes=["result"], label="Dx")
        scope.keep(dx_pt)

    low_pt = model.set_point(sp.Rational(2, 3), 0, classes=["given", "rational-low"], label="Q1")
    high_pt = model.set_point(sp.Rational(3, 4), 0, classes=["given", "rational-high"], label="Q2")
    _ = dx_pt
    return DedekindCutResult(
        model=model,
        cut_point=d_cut,
        lower_rational=low_pt,
        upper_rational=high_pt,
    )


@dataclass(frozen=True)
class HeatedDiskResult:
    """Exact model for Unit 3: Poincaré's Heated Disk optical rays & isothermals (Ch. IV)."""

    model: Model
    source: spg.Point2D
    isothermals: tuple[spg.Circle, spg.Circle, spg.Circle]
    light_rays: tuple[HyperbolicGeodesic, HyperbolicGeodesic, HyperbolicGeodesic, HyperbolicGeodesic]


def construct_heated_disk_optical_rays(model: Model | None = None) -> HeatedDiskResult:
    r"""Construct Poincaré's Heated-Disk optical world (:math:`T \propto 1 - r^2,\; n \propto (1-r^2)^{-1}`)."""
    if model is None:
        model = _new_model("poincare_heated_disk")
    origin, _ex, _omega = construct_unit_horizon(model)

    r1_pt = model.set_point(sp.Rational(2, 5), 0, classes=["aux-iso"], guide=True)
    r2_pt = model.set_point(sp.Rational(7, 10), 0, classes=["aux-iso"], guide=True)
    r3_pt = model.set_point(sp.Rational(9, 10), 0, classes=["aux-iso"], guide=True)
    iso1 = model.construct_circle(origin, r1_pt, classes=["isothermal"], ID="iso1")
    iso2 = model.construct_circle(origin, r2_pt, classes=["isothermal"], ID="iso2")
    iso3 = model.construct_circle(origin, r3_pt, classes=["isothermal"], ID="iso3")

    src = model.set_point(0, sp.Rational(-2, 5), classes=["given", "source"], label="S")
    p_left = model.set_point(sp.Rational(-2, 5), sp.Rational(1, 5), classes=["given"], label="R1")
    p_mid_l = model.set_point(sp.Rational(-1, 5), sp.Rational(2, 5), classes=["given"], label="R2")
    p_mid_r = model.set_point(sp.Rational(1, 5), sp.Rational(2, 5), classes=["given"], label="R3")
    p_right = model.set_point(sp.Rational(2, 5), sp.Rational(1, 5), classes=["given"], label="R4")

    ray1 = construct_hyperbolic_geodesic(model, src, p_left, classes=["geodesic", "light-ray"])
    ray2 = construct_hyperbolic_geodesic(model, src, p_mid_l, classes=["geodesic", "light-ray"])
    ray3 = construct_hyperbolic_geodesic(model, src, p_mid_r, classes=["geodesic", "light-ray"])
    ray4 = construct_hyperbolic_geodesic(model, src, p_right, classes=["geodesic", "light-ray"])

    return HeatedDiskResult(
        model=model,
        source=src,
        isothermals=(iso1, iso2, iso3),
        light_rays=(ray1, ray2, ray3, ray4),
    )


@dataclass(frozen=True)
class BeltramiKleinBridgeResult:
    """Exact straightedge correspondence between Poincaré conformal arcs & Beltrami–Klein chords."""

    model: Model
    poincare_geodesic: HyperbolicGeodesic
    beltrami_klein_chord: spg.Line2D
    poincare_points: tuple[spg.Point2D, spg.Point2D]
    klein_points: tuple[spg.Point2D, spg.Point2D]


def construct_beltrami_klein_bridge(model: Model | None = None) -> BeltramiKleinBridgeResult:
    r"""Construct the exact Weierstrass radial projection :math:`K(P) = \frac{2P}{1 + \|P\|^2}`."""
    if model is None:
        model = _new_model("beltrami_klein_bridge")
    origin, u_pt, _omega = construct_unit_horizon(model)
    v_pt = model.set_point(0, 1, classes=["given", "ideal"], label="V")

    p1 = model.set_point(sp.Rational(2, 5), sp.Rational(1, 5), classes=["given"], label="P1")
    p2 = model.set_point(sp.Rational(1, 5), sp.Rational(2, 5), classes=["given"], label="P2")
    p_geo = construct_hyperbolic_geodesic(
        model, p1, p2, classes=["geodesic", "featured"], label="g_poincare"
    )
    bk_chord = model.construct_line(u_pt, v_pt, classes=["klein-chord"], ID="L_klein")

    ray_1 = model.construct_line(origin, p1, classes=["guide", "radial-proj"], guide=True)
    ray_2 = model.construct_line(origin, p2, classes=["guide", "radial-proj"], guide=True)
    k1 = model.intersect(ray_1, bk_chord, classes=["klein-point"], label="K1")
    k2 = model.intersect(ray_2, bk_chord, classes=["klein-point"], label="K2")

    for p_pt, k_pt in ((p1, k1), (p2, k2)):
        denom = 1 + p_pt.x**2 + p_pt.y**2
        if not (
            zero_test(k_pt.x - (2 * p_pt.x) / denom)
            and zero_test(k_pt.y - (2 * p_pt.y) / denom)
        ):
            raise AssertionError("Radial intersection with UV did not match Weierstrass map K(P).")

    return BeltramiKleinBridgeResult(
        model=model,
        poincare_geodesic=p_geo,
        beltrami_klein_chord=bk_chord,
        poincare_points=(p1, p2),
        klein_points=(k1, k2),
    )


@dataclass(frozen=True)
class StellarParallaxResult:
    """Exact model for Unit 4: Stellar parallax triangle & Poincaré conventionalism (Ch. V § 3)."""

    model: Model
    stars: tuple[spg.Point2D, spg.Point2D, spg.Point2D]
    lobachevsky_rays: tuple[HyperbolicGeodesic, HyperbolicGeodesic, HyperbolicGeodesic]
    euclidean_chords: tuple[spg.Line2D, spg.Line2D, spg.Line2D]


def construct_stellar_parallax_conventionalism(
    model: Model | None = None,
) -> StellarParallaxResult:
    """Construct Poincaré's astronomical parallax triangle (Ch. V, *Experience and Geometry*)."""
    if model is None:
        model = _new_model("stellar_parallax_conventionalism")
    _origin, _ex, _omega = construct_unit_horizon(model)

    s1 = model.set_point(sp.Rational(-3, 5), sp.Rational(-2, 5), classes=["given", "star"], label="S1")
    s2 = model.set_point(sp.Rational(3, 5), sp.Rational(-2, 5), classes=["given", "star"], label="S2")
    s3 = model.set_point(0, sp.Rational(3, 4), classes=["given", "star"], label="S3")

    g12 = construct_hyperbolic_geodesic(model, s1, s2, classes=["geodesic", "parallax-arc"])
    g23 = construct_hyperbolic_geodesic(model, s2, s3, classes=["geodesic", "parallax-arc"])
    g31 = construct_hyperbolic_geodesic(model, s3, s1, classes=["geodesic", "parallax-arc"])

    c12 = model.construct_line(s1, s2, classes=["euclidean-chord"])
    c23 = model.construct_line(s2, s3, classes=["euclidean-chord"])
    c31 = model.construct_line(s3, s1, classes=["euclidean-chord"])

    return StellarParallaxResult(
        model=model,
        stars=(s1, s2, s3),
        lobachevsky_rays=(g12, g23, g31),
        euclidean_chords=(c12, c23, c31),
    )
