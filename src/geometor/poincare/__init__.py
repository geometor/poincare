"""GEOMETOR • Poincaré: Bilingual *La Science et l'Hypothèse* Codex & Exact Hyperbolic Disk Engine.

Combines a synchronized 4-track Digital Scriptorium Book Codex (*English · French (1902) ·
Summary · Notes*) of Henri Poincaré's *La Science et l'Hypothèse* (1902 / 1905) with
100% exact SymPy + ``geometor.model`` straightedge-and-compass constructions in the
Poincaré Conformal Hyperbolic Disk Model.
"""

from __future__ import annotations

from geometor.poincare.concordance import (
    CODEX_UNITS,
    CodexAuditReport,
    audit_codex_repository,
    compile_apparatus_rst,
    default_repo_root,
    load_concordance,
    load_sources_manifest,
    verify_sources_manifest,
)
from geometor.poincare.disk import (
    BeltramiKleinBridgeResult,
    DedekindCutResult,
    HeatedDiskResult,
    HyperbolicGeodesic,
    HyperbolicMetricReport,
    IdealTriangleResult,
    SaccheriDefectResult,
    StellarParallaxResult,
    UltraparallelPencil,
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
    euclidean_tangent_at_circle_point,
    hyperbolic_cross_ratio_and_quadrance,
)
from geometor.poincare.render import (
    FIGURE_SPECS,
    export_all_codex_figures,
    render_codex_figure,
    render_figure_svg,
)

__version__ = "0.1.0"

__all__ = [
    "BeltramiKleinBridgeResult",
    "CODEX_UNITS",
    "CodexAuditReport",
    "DedekindCutResult",
    "FIGURE_SPECS",
    "HeatedDiskResult",
    "HyperbolicGeodesic",
    "HyperbolicMetricReport",
    "IdealTriangleResult",
    "SaccheriDefectResult",
    "StellarParallaxResult",
    "UltraparallelPencil",
    "__version__",
    "audit_codex_repository",
    "compile_apparatus_rst",
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
    "default_repo_root",
    "euclidean_tangent_at_circle_point",
    "export_all_codex_figures",
    "hyperbolic_cross_ratio_and_quadrance",
    "load_concordance",
    "load_sources_manifest",
    "render_codex_figure",
    "render_figure_svg",
    "verify_sources_manifest",
]
