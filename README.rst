=================
GEOMETOR poincare
=================

Synchronized 4-track bilingual **Book Codex** (*English · French (1902) · Summary · Notes*) of **Henri Poincaré's** *La Science et l'Hypothèse* (*Science and Hypothesis*, 1902 / 1905) paired with **100% exact symbolic constructions** of the **Poincaré Conformal Hyperbolic Disk Model** in ``SymPy`` and ``geometor.model``.

Overview
--------

1. **4-Track Bilingual Digital Scriptorium Codex (``docsrc/science_and_hypothesis/``)**:
   - Verbatim 1902 French original (*Ernest Flammarion*, including *Les Géométries de Hilbert*) collated paragraph-for-paragraph with W. J. Greenstreet's 1905 London translation (with Sir Joseph Larmor's Preface) and G. B. Halsted's 1905 New York translation (with Poincaré's Special American Preface).
   - Four thematic units covering **Part I (*Number and Magnitude*: Chs. I–II)**, **Part II (*Space*: Chs. III–V)**, and an unabridged epistemological bridge to **Parts III–IV (Chs. VI, VII, IX)**.
   - Eight calibrated ``.euclid-graphic`` SVG figures wired for bidirectional ``:g:`` hover highlighting, plus a machine-compiled **Translation Dictionary & Cross-Corpus Concordance** (``PC.01``–``PC.12``), **Bibliography**, **Prosopographical Index**, and **Bilingual Glossary**.

2. **Exact Symbolic Hyperbolic Disk Engine (``geometor.poincare``)**:
   - **Zero ``float`` / ``sp.Float`` Coordinates**: Every point, line, orthogonal circle, horizon inversion, and intersection is constructed over $\mathbb{Q}$ and closed-form quadratic radicals inside ``geometor.model.Model(..., auto_intersect=False)``.
   - **Poincaré's Translation Dictionary & Rational Trigonometry**: Connects Poincaré's 4-point circle cross-ratio $\chi(P, Q; U, V)$ with Norman Wildberger's transcendental-free **Rational Hyperbolic Quadrance** $q_{\mathrm{UHG}}(P, Q) = -\sinh^2 d_{\mathbb{H}}(P, Q) \in \mathbb{Q}$ and the Beltrami–Klein straightedge radial projection $K(P) = \frac{2P}{1 + \|P\|^2}$.

Development & Verification
--------------------------

.. code-block:: bash

   # Verify SHA-256 archival witnesses, 4-track parity, and exact symbolic invariants
   /home/phi/PROJECTS/geometor/.venv/bin/python scripts/verify_codex.py

   # Export all 8 calibrated .euclid-graphic SVGs
   /home/phi/PROJECTS/geometor/.venv/bin/python scripts/export_figures.py

   # Run runnable symbolic demonstrations
   /home/phi/PROJECTS/geometor/.venv/bin/python demos/inversion_and_geodesics.py
   /home/phi/PROJECTS/geometor/.venv/bin/python demos/ultraparallels_and_fifth_postulate.py
   /home/phi/PROJECTS/geometor/.venv/bin/python demos/ideal_and_saccheri_triangles.py
   /home/phi/PROJECTS/geometor/.venv/bin/python demos/cayley_klein_and_heated_disk.py

   # Test, lint, and compile the Book Codex
   pytest
   ruff check src demos scripts tests
   publish build

License
-------

MIT License (code, SVG figures, and scholarly apparatus). Primary source texts (1902 / 1905) are in the worldwide Public Domain.
