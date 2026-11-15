=========
changelog
=========

0.1.4 (2026-11-15)
------------------

- Rebuilt codex documentation with ``photon-platform/publish`` ``v0.4.6`` so every inline ``.euclid-graphic`` SVG carries explicit ``viewBox`` pixel dimensions, per-diagram scoped ``<style>`` rules, and Nocturnal Codex dark/light theme parity.

0.1.3 (2026-11-15)
------------------

- Ensure canonical GEOMETOR ``logo.png`` and ``favicon.ico`` brand assets are provisioned in ``docsrc/_static/`` and rendered in site headers and browser tabs.

0.1.2 (2026-11-14)
------------------

- Standardized top-level ``About`` page (``docsrc/about/index.rst`` promoted to top header ``:order: 10``) with the three-pillar GEOMETOR semantic-extraction mission and archival provenance; retired ``docsrc/mission/`` stubs cleanly into Home and ``About``.

0.1.1 (2026-11-14)
------------------

* Standardized Book Title Page with publication metadata, reading instructions, and structured navigation.
* Added top-level Header Navigation (``Book``, ``People``, ``Bibliography``, ``Usage``) and dedicated Reader's Guide (``docsrc/usage/``).
* Enhanced ``People`` directory with featured Author and Translator biographical profiles.
* Standardized structural section headings and terminology in English across codex indices.

0.1.0 (2026-11-12)
------------------

* **Synchronized 4-Track Bilingual Book Codex (``docsrc/science_and_hypothesis/``)**:
  * Complete verbatim public-domain editions of Henri Poincaré's *La Science et l'Hypothèse* (Paris: Ernest Flammarion, 1902) paired with the 1905 authorized English translations by W. J. Greenstreet (with Sir Joseph Larmor's Preface) and G. B. Halsted (with Poincaré's Special American Preface and *Hilbert's Geometries*).
  * Runtime ``fr`` (*French (1902)*) companion track registered via ``geometor.poincare.sphinx_ext`` alongside *English*, *Summary*, and *Notes* across all four thematic units.
* **Exact Symbolic Conformal Hyperbolic Disk Engine (``geometor.poincare.disk``)**:
  * Zero-float ``SymPy`` + ``geometor.model`` straightedge-and-compass horizon circle inversion, orthogonal geodesic circles, cross-ratio & Wildberger Rational Hyperbolic Quadrance invariants, Lobachevskian horoparallels/ultraparallels, Pythagorean ideal triangle, Saccheri quadrilateral angular defect, Heated-Disk optical rays, Beltrami–Klein radial bridge, Dedekind cut, and stellar parallax conventionalism.
* **Interactive ``.euclid-graphic`` Figures & Cross-Corpus Apparatus**:
  * Eight exact-model SVG figures with bidirectional ``:g:`` hover highlighting and CSS2/CSS3 Inkscape + dark-mode support.
  * Compiled Translation Dictionary & Cross-Repository Concordance (``PC.01``–``PC.12``), Systematic Bibliography (23 citations), Prosopographical Index (28 persons), and Bilingual Glossary (18 entries).
