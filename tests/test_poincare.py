"""Comprehensive test suite for ``geometor-poincare``."""

from __future__ import annotations

import importlib.util
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import sympy as sp
import sympy.geometry as spg
from geometor.model import Model, exact_sign, intersect_2d, quadrance, zero_test

from geometor.poincare import (
    FIGURE_SPECS,
    audit_codex_repository,
    construct_beltrami_klein_bridge,
    construct_dedekind_continuum_cut,
    construct_heated_disk_optical_rays,
    construct_hyperbolic_geodesic,
    construct_ideal_hyperbolic_triangle,
    construct_inversion_in_horizon,
    construct_saccheri_triangle_defect,
    construct_saccheri_triangleDefect,
    construct_stellar_parallax_conventionalism,
    construct_ultraparallels_through_point,
    construct_unit_horizon,
    default_repo_root,
    hyperbolic_cross_ratio_and_quadrance,
    render_figure_svg,
    verify_sources_manifest,
)
from geometor.poincare.cli import main as cli_main

REPO_ROOT = Path(__file__).resolve().parents[1]


def _assert_model_zero_floats(model: Model) -> None:
    """Assert that no element in ``model`` contains ``sp.Float``."""
    assert len(model) > 0
    for el in model:
        assert not el.has(sp.Float), f"sp.Float detected in {el!r}"


def test_repo_root_and_sources_manifest() -> None:
    """Verify repository root discovery and SHA-256 archival witness checksums."""
    assert default_repo_root() == REPO_ROOT
    verified = verify_sources_manifest(REPO_ROOT)
    assert len(verified) == 3
    ids = {w["id"] for w in verified}
    assert ids == {"flammarion-1902-fr", "greenstreet-1905-en", "halsted-1905-en"}


def test_horizon_inversion_exactness_and_involution() -> None:
    """Verify straightedge-and-compass horizon inversion over Q and Q(sqrt(2))."""
    model = Model("test_inversion", logger=False, auto_intersect=False)
    origin, _ex, _omega = construct_unit_horizon(model)

    # 1. Rational interior point P = (1/3, 1/4), ||P||^2 = 25/144 -> P* = (48/25, 36/25)
    p_rat = spg.Point2D(sp.Rational(1, 3), sp.Rational(1, 4))
    p_star = construct_inversion_in_horizon(model, p_rat, label="P*")
    assert zero_test(p_star.x - sp.Rational(48, 25))
    assert zero_test(p_star.y - sp.Rational(36, 25))
    assert zero_test(quadrance(origin, p_rat) * quadrance(origin, p_star) - 1)

    # 2. Exterior-to-interior involution (P*)* == P
    p_back = construct_inversion_in_horizon(model, p_star, label="P**")
    assert zero_test(p_back.x - p_rat.x)
    assert zero_test(p_back.y - p_rat.y)

    # 3. Quadratic irrational interior point Q = (sqrt(2)/3, 1/3), ||Q||^2 = 1/3 -> Q* = 3Q
    q_rad = spg.Point2D(sp.sqrt(2) / 3, sp.Rational(1, 3))
    q_star = construct_inversion_in_horizon(model, q_rad)
    assert zero_test(q_star.x - sp.sqrt(2))
    assert zero_test(q_star.y - 1)
    assert zero_test(quadrance(origin, q_rad) * quadrance(origin, q_star) - 1)

    # 4. Horizon boundary point is fixed
    b_pt = spg.Point2D(sp.Rational(3, 5), sp.Rational(4, 5))
    b_star = construct_inversion_in_horizon(model, b_pt)
    assert zero_test(b_star.x - b_pt.x) and zero_test(b_star.y - b_pt.y)

    _assert_model_zero_floats(model)

    with pytest.raises(ValueError, match="Origin"):
        construct_inversion_in_horizon(model, spg.Point2D(0, 0))

    with pytest.raises(TypeError, match="Floating-point"):
        construct_inversion_in_horizon(model, spg.Point2D(sp.Float("0.5"), 0, evaluate=False))


def test_hyperbolic_geodesic_diameter_chord_and_ideal() -> None:
    """Verify diameter, interior orthogonal circle, and ideal-to-ideal geodesics."""
    model = Model("test_geodesics", logger=False, auto_intersect=False)
    origin, _ex, _omega = construct_unit_horizon(model)

    # 1. Diameter case (collinear with O)
    d1 = spg.Point2D(sp.Rational(-1, 3), sp.Rational(-1, 4))
    d2 = spg.Point2D(sp.Rational(2, 3), sp.Rational(1, 2))
    diam_geo = construct_hyperbolic_geodesic(model, d1, d2)
    assert diam_geo.is_diameter
    assert isinstance(diam_geo.carrier, spg.Line2D)
    assert zero_test(diam_geo.U.x - sp.Rational(-4, 5))
    assert zero_test(diam_geo.U.y - sp.Rational(-3, 5))
    assert zero_test(diam_geo.V.x - sp.Rational(4, 5))
    assert zero_test(diam_geo.V.y - sp.Rational(3, 5))

    # 2. Non-diametral interior chord P=(1/2, 0), Q=(0, 1/2) -> center (5/4, 5/4), r^2 = 17/8
    p_pt = spg.Point2D(sp.Rational(1, 2), 0)
    q_pt = spg.Point2D(0, sp.Rational(1, 2))
    arc_geo = construct_hyperbolic_geodesic(model, p_pt, q_pt)
    carrier, u_pt, v_pt = arc_geo
    assert not arc_geo.is_diameter
    assert isinstance(carrier, spg.Circle)
    assert arc_geo.center is not None
    assert zero_test(arc_geo.center.x - sp.Rational(5, 4))
    assert zero_test(arc_geo.center.y - sp.Rational(5, 4))
    assert zero_test(arc_geo.radius_squared - sp.Rational(17, 8))
    assert zero_test(arc_geo.orthogonality_residual)
    assert zero_test(quadrance(origin, u_pt) - 1)
    assert zero_test(quadrance(origin, v_pt) - 1)

    # 3. Ideal-to-ideal geodesic (1, 0) to (0, 1) -> center (1, 1), r^2 = 1
    id1 = spg.Point2D(1, 0)
    id2 = spg.Point2D(0, 1)
    ideal_geo = construct_hyperbolic_geodesic(model, id1, id2)
    assert ideal_geo.center is not None
    assert zero_test(ideal_geo.center.x - 1) and zero_test(ideal_geo.center.y - 1)
    assert zero_test(ideal_geo.radius_squared - 1)

    _assert_model_zero_floats(model)

    with pytest.raises(ValueError, match="distinct"):
        construct_hyperbolic_geodesic(model, p_pt, p_pt)
    with pytest.raises(ValueError, match="closed unit disk"):
        construct_hyperbolic_geodesic(model, p_pt, spg.Point2D(2, 0))


def test_hyperbolic_cross_ratio_and_wildberger_quadrances() -> None:
    """Verify exact cross-ratio and Rational Hyperbolic Quadrance identities."""
    origin = spg.Point2D(0, 0)
    half_x = spg.Point2D(sp.Rational(1, 2), 0)
    half_y = spg.Point2D(0, sp.Rational(1, 2))

    # Zero-distance identity
    same = hyperbolic_cross_ratio_and_quadrance(half_x, half_x)
    assert same.cross_ratio == 1
    assert same.poincare_distance == 0
    assert same.wildberger_uhg_quadrance == 0

    # Radial segment O -> (1/2, 0): chi = (1 + 1/2)/(1 - 1/2) = 3
    rad_m = hyperbolic_cross_ratio_and_quadrance(origin, half_x)
    assert rad_m.cross_ratio == sp.Integer(3)
    assert rad_m.poincare_distance == sp.log(3)
    assert rad_m.conformal_quadrance == sp.Rational(1, 4)
    assert rad_m.wildberger_uhg_quadrance == sp.Rational(-16, 9)
    assert rad_m.cayley_klein_quadrance == sp.Rational(16, 25)

    # Non-diametral chord (1/2, 0) -> (0, 1/2): tau = 8/17, q_UHG = -544/81, q_CK = 544/625
    chord_m = hyperbolic_cross_ratio_and_quadrance(half_x, half_y)
    assert chord_m.conformal_quadrance == sp.Rational(8, 17)
    assert chord_m.wildberger_uhg_quadrance == sp.Rational(-544, 81)
    assert chord_m.cayley_klein_quadrance == sp.Rational(544, 625)
    assert not chord_m.cross_ratio.has(sp.Float)
    assert exact_sign(chord_m.cross_ratio - 1) > 0


def test_ultraparallels_and_fifth_postulate_independence() -> None:
    """Verify two limiting horoparallels and two disjoint ultraparallels through P."""
    pencil = construct_ultraparallels_through_point()
    _assert_model_zero_floats(pencil.model)
    assert len(pencil.limiting_parallels) == 2
    assert len(pencil.ultraparallels) == 2

    base = pencil.base_geodesic.carrier
    for lim in pencil.limiting_parallels:
        hits = [pt for pt in intersect_2d(base, lim.carrier) if isinstance(pt, spg.Point2D)]
        assert any(zero_test(pt.x**2 + pt.y**2 - 1) for pt in hits)
        assert not any(exact_sign(pt.x**2 + pt.y**2 - 1) < 0 for pt in hits)

    for ultra in pencil.ultraparallels:
        hits = [pt for pt in intersect_2d(base, ultra.carrier) if isinstance(pt, spg.Point2D)]
        assert not any(exact_sign(pt.x**2 + pt.y**2 - 1) <= 0 for pt in hits)


def test_ideal_triangle_and_saccheri_defect() -> None:
    """Verify rational ideal triangle (0 spreads) and Saccheri acute summit spreads."""
    ideal = construct_ideal_hyperbolic_triangle()
    _assert_model_zero_floats(ideal.model)
    assert ideal.radii == (sp.Integer(2), sp.Integer(2), sp.Rational(4, 3))
    assert ideal.vertex_spreads == (sp.Integer(0), sp.Integer(0), sp.Integer(0))
    assert ideal.angular_defect == sp.pi

    sac = construct_saccheri_triangleDefect()
    assert construct_saccheri_triangle_defect is construct_saccheri_triangleDefect
    _assert_model_zero_floats(sac.model)
    assert sac.triangle_spreads == (sp.Integer(1), sp.Rational(9, 34), sp.Rational(9, 34))
    assert sac.saccheri_base_spreads == (sp.Integer(1), sp.Integer(1))
    assert sac.saccheri_summit_spreads == (sp.Rational(64, 145), sp.Rational(64, 145))
    assert sac.saccheri_leg_uhg_quadrances == (
        sp.Rational(-225, 64),
        sp.Rational(-225, 64),
    )


def test_dedekind_heated_disk_beltrami_klein_and_parallax() -> None:
    """Verify Units 1, 3, and 4 exact symbolic models."""
    ded = construct_dedekind_continuum_cut()
    _assert_model_zero_floats(ded.model)
    assert zero_test(ded.cut_point.x**2 - sp.Rational(1, 2))
    assert exact_sign(ded.lower_rational.x**2 - ded.cut_point.x**2) < 0
    assert exact_sign(ded.upper_rational.x**2 - ded.cut_point.x**2) > 0

    heated = construct_heated_disk_optical_rays()
    _assert_model_zero_floats(heated.model)
    assert len(heated.isothermals) == 3
    assert len(heated.light_rays) == 4

    bridge = construct_beltrami_klein_bridge()
    _assert_model_zero_floats(bridge.model)
    k1, k2 = bridge.klein_points
    assert zero_test(k1.x - sp.Rational(2, 3)) and zero_test(k1.y - sp.Rational(1, 3))
    assert zero_test(k2.x - sp.Rational(1, 3)) and zero_test(k2.y - sp.Rational(2, 3))

    parallax = construct_stellar_parallax_conventionalism()
    _assert_model_zero_floats(parallax.model)
    assert len(parallax.stars) == 3
    assert len(parallax.lobachevsky_rays) == 3
    assert len(parallax.euclidean_chords) == 3


def test_exported_svgs_codex_integrity_and_g_role_wiring() -> None:
    """Verify all 8 SVGs parse cleanly, match :g: targets, and book pages embed zero py_file."""
    report = audit_codex_repository(REPO_ROOT)
    assert report.witness_count == 3
    assert report.unit_track_files == 16
    assert report.figure_count == 8
    assert report.dictionary_rows == 8
    assert report.concordance_entries == 12

    fig_dir = REPO_ROOT / "docsrc" / "_static" / "figures"
    svg_refs: dict[str, set[str]] = {}
    for fname in FIGURE_SPECS:
        fig_id = fname.removesuffix(".svg")
        svg_path = fig_dir / fname
        assert svg_path.is_file()
        raw = svg_path.read_text(encoding="utf-8")
        assert render_figure_svg(fname) == raw
        root = ET.fromstring(raw)
        assert root.attrib.get("class") == "euclid-graphic"
        assert root.attrib.get("id") == fig_id
        assert root.attrib.get("data-graphic-id") == fig_id
        refs = {
            el.attrib["data-ref"]
            for el in root.iter()
            if "data-ref" in el.attrib and el.attrib["data-ref"]
        }
        assert len(refs) >= 4
        svg_refs[fig_id] = refs

    # Check every codex RST file for zero py_file and valid :g:`... <fig_id:ref>` references
    g_role_re = re.compile(r":g:`[^`]*<([^:>]+):([^>]+)>`")
    codex_dir = REPO_ROOT / "docsrc" / "science_and_hypothesis"
    matched_g_roles = 0
    for rst_file in sorted(codex_dir.rglob("*.rst")):
        text = rst_file.read_text(encoding="utf-8")
        assert ".. py_file::" not in text, f"Forbidden py_file in {rst_file}"
        for m in g_role_re.finditer(text):
            fig_target, ref_target = m.group(1).strip(), m.group(2).strip()
            assert fig_target in svg_refs, f"Unknown SVG id {fig_target} in {rst_file}"
            assert ref_target in svg_refs[fig_target], (
                f"Missing data-ref={ref_target!r} on {fig_target}.svg (referenced in {rst_file.name})"
            )
            matched_g_roles += 1
    assert matched_g_roles >= 20


def test_cli_and_demo_scripts() -> None:
    """Verify CLI status subcommand and all 4 standalone demo scripts."""
    assert cli_main(["--repo-root", str(REPO_ROOT), "status"]) == 0

    demo_names = (
        "inversion_and_geodesics.py",
        "ultraparallels_and_fifth_postulate.py",
        "ideal_and_saccheri_triangles.py",
        "cayley_klein_and_heated_disk.py",
    )
    for demo_name in demo_names:
        demo_path = REPO_ROOT / "demos" / demo_name
        spec = importlib.util.spec_from_file_location(demo_path.stem, demo_path)
        assert spec is not None and spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert mod.main([]) == 0
