# GEOMETOR • poincare

Bilingual Digital Scriptorium Book Codex of **Henri Poincaré's** *La Science et l'Hypothèse* (*Science and Hypothesis*, 1902 / 1905) paired with **100% exact symbolic constructions** of the **Poincaré Conformal Hyperbolic Disk Model** in `SymPy` and `geometor.model`.

---

## 1. Architectural Mandates

1. **100% Exact Symbolic Precision (`src/geometor/poincare/disk.py`)**:
   - Every element inside `geometor.model.Model(..., auto_intersect=False)` is constructed over $\mathbb{Q}$ or exact quadratic radicals—**zero `float` or `sp.Float` coordinates**.
   - Hyperbolic geodesics in $\mathbb{D} = \{(x, y) : x^2 + y^2 < 1\}$ are constructed via straightedge-and-compass horizon inversion $P^* = P / \|P\|^2$ in $\Omega: x^2 + y^2 = 1$ and orthogonal circle circumscription $|OC|^2 - r^2 = 1$.
   - Metric invariants pair Poincaré's cross-ratio $d_{\mathbb{H}}(P, Q) = \ln \chi(P, Q; U, V)$ with conformal quadrance $\tau(P, Q)$, Cayley–Klein quadrance $q_{\mathrm{CK}}(P, Q)$, and Norman Wildberger's Rational Hyperbolic Quadrance $q_{\mathrm{UHG}}(P, Q) = -\frac{4\tau}{(1-\tau)^2}$.
2. **Strict Content / Code Separation (`:layout: book`)**:
   - Historical and commentary tracks under `docsrc/science_and_hypothesis/` contain **zero embedded `py_file` directives**.
   - Eight calibrated `.euclid-graphic` SVGs are generated offline by `scripts/export_figures.py` into `docsrc/_static/figures/` with CSS2 presentation fallbacks (for Inkscape/rsvg) + CSS3 dark-mode theme variables and bidirectional `data-graphic-id` / `data-ref` `:g:` highlighting.
   - Runnable Python demonstrations live in `demos/` and are showcased in `docsrc/demos/index.rst`.
3. **Runtime 4-Track Book Codex (`src/geometor/poincare/sphinx_ext.py`)**:
   - Registers the `fr` (*"French (1902)"*) companion track dynamically in `photon_platform.publish.book` at Sphinx build time without modifying `photon-platform/publish`.
   - Binds local `objects.inv` files across sister GEOMETOR repositories so `publish build` succeeds 100% offline.

---

## 2. Repository Structure

- `src/geometor/poincare/`
  - `disk.py` — Exact symbolic hyperbolic disk constructions & Rational Hyperbolic Quadrances.
  - `render.py` — Exact-model `.euclid-graphic` SVG renderer for Figures 1–8.
  - `concordance.py` — SHA-256 archival witness verifier, 4-track parity auditor, and RST apparatus compiler.
  - `sphinx_ext.py` — Runtime `fr` track registration and offline local intersphinx configuration.
  - `cli.py` — `geometor-poincare` CLI (`status`, `verify`, `figures`, `compile-apparatus`).
- `demos/` — Four standalone runnable demonstrations (`inversion_and_geodesics.py`, `ultraparallels_and_fifth_postulate.py`, `ideal_and_saccheri_triangles.py`, `cayley_klein_and_heated_disk.py`).
- `resources/science_and_hypothesis/` — Verbatim 1902/1905 public-domain witnesses (`sources/`), `sources_manifest.json`, `concordance.json`, `persons.json`, `citations.json`, and `glossary.json` (mirrored to `resources/` for `:cite:`, `:person:`, and `:term:` resolution).
- `docsrc/science_and_hypothesis/` — 4-track synchronized Book Codex (`unit-1` through `unit-4`) + compiled apparatus pages.
- `tests/test_poincare.py` — Comprehensive pytest suite verifying zero-float algebra, geometric theorems, SVG XML validity, CLI, and codex parity.

---

## 3. Offline Sandbox Verification Commands

```bash
/home/phi/PROJECTS/geometor/.venv/bin/python scripts/export_figures.py
/home/phi/PROJECTS/geometor/.venv/bin/python scripts/verify_codex.py
/home/phi/PROJECTS/geometor/.venv/bin/pytest
ruff check src demos scripts tests
publish build
```
