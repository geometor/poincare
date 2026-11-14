:navigation: header
:order: 20
:nav_title: Usage

.. _poincare-usage:

==================
Using This Edition
==================

.. rubric:: Interactive Reader's Guide to the Digital Scriptorium Edition of Poincaré's Science and Hypothesis

Welcome to the GEOMETOR critical edition of **Science and Hypothesis** (*La Science et l'Hypothèse*). This digital edition is designed for deep philosophical reading, bilingual French-English comparative philology, and exact symbolic synthesis across Henri Poincaré's foundational work on arithmetic recurrence, non-Euclidean geometries, and geometric conventionalism. Below are the key interactive features available throughout the site.

1. Synchronized Reading Tracks
------------------------------

Every unit in the Book Codex provides up to four synchronized reading tracks accessible directly from the chapter header navigation bar:

* **English (Primary Translation)**: Public-domain translation based on W. J. Greenstreet's authorized 1905 London edition (Walter Scott) with Joseph Larmor's preface, collated with George Bruce Halsted's 1905 New York edition (The Science Press) and enhanced with calibrated vector figures.
* **French (Original 1902, ``-fr``)**: Verbatim French text from Ernest Flammarion's 1902 Paris first edition (*Bibliothèque de Philosophie scientifique*), including the crucial section *Les Géométries de Hilbert* (pp. 63–64).
* **Summary (Epistemological Synopsis)**: Chapter theses, argumentative progression, translation dictionary mappings, and conventionalist foundations.
* **Notes (Scholarly Commentary)**: Exact symbolic SymPy models of the conformal hyperbolic disk, French and German philology, and cross-corpus links across Euclid, Hilbert, Russell, Hoenen, Klein, and Wildberger.

Use the track switcher in the chapter header bar to toggle seamlessly between perspectives while preserving your reading position.

2. Primary-Source Folio Milestones
----------------------------------

Every passage is calibrated to primary archival witnesses:

* **Marginal Folio Badges**: Marginal milestone pills mark page transitions in the 1902 Flammarion French edition and 1905 British/American translations.
* **Header Folio Indicator**: The top metadata bar identifies the active unit, chapter locus, and corresponding Flammarion pagination.
* **Cross-Reference Anchors**: Explicit anchors enable direct deep linking across the GEOMETOR ecosystem.

3. Interactive Diagrams & Deductive Links
-----------------------------------------

The edition features eight calibrated, theme-adaptive ``.euclid-graphic`` SVG vector plates:

* **Geometric Hover Cards (``:g:``)**: Hovering over or clicking a geometric symbol (e.g., points, lines, circles, or geodesic arcs in the conformal disk) highlights the corresponding element in the vector plate with coordinate and invariant tooltips.
* **Mathematical Equations (``:eq:``)**: Display formatted LaTeX typography with interactive term explanations.
* **Deductive Justifications (``:just:``)**: Citations to Euclidean postulates, Hilbert axioms, or Poincaré lemmas provide direct cross-references.

4. Full-Text Search with In-Page Highlighting
---------------------------------------------

The global search box in the sidebar provides instantaneous full-text search across all four units, apparatus tables, and commentary:

* Search queries automatically append `?highlight=` parameters to destination URLs.
* Matched terms are highlighted directly within the chapter body, French original, and scholia for immediate discovery.

5. Categories, Tags & Collection Views
--------------------------------------

Document collections throughout the site (such as the :doc:`Development Log <../log/index>`) support rich viewing modes:

* **Cards View**: Grid of entry cards with metadata badges and timestamps.
* **Banners View**: Wide banner layout for extended narrative overviews.
* **List View**: Dense tabular listing for fast scanning.
* **Taxonomy Facets**: Filter by topic tags (e.g., `conventionalism`, `hyperbolic`, `conformal-disk`, `induction`, `non-euclidean`).

6. People, Bibliography & Glossary Tooltips
-------------------------------------------

* **People (``:person:``)**: Historical figures (such as :person:`Henri Poincaré <poincare>`, :person:`W. J. Greenstreet <greenstreet>`, :person:`Sir Joseph Larmor <larmor>`, :person:`Nikolai Lobachevsky <lobachevsky>`, :person:`Bernhard Riemann <riemann>`, and :person:`David Hilbert <hilbert>`) display rich biographical hover cards linking to the :doc:`People Register <../science_and_hypothesis/persons>`.
* **Citations (``:cite:``)**: Inline citations link to authoritative editions in the :doc:`Bibliography <../science_and_hypothesis/bibliography>`.
* **Technical Terms (``:term:``)**: Classical and modern geometric terms (such as *convention*, *dedekind-cut*, *heated-disk*, and *circle-inversion*) link directly to entries in the :doc:`Technical Glossary <../science_and_hypothesis/glossary>`.
* **Theme Switching**: Toggle between Light and Dark themes via the header button to suit your reading environment.

7. Command-Line & Python API
----------------------------

The ``geometor-poincare`` CLI and Python package provide tools for exact symbolic conformal disk modeling, Rational Trigonometry verification, and apparatus management.

CLI Usage:

.. code-block:: bash

   # Verify witness SHA-256 checksums, 4-track parity, and symbolic invariants
   geometor-poincare verify

   # Display summary of all 4 units, apparatus registries, and figures
   geometor-poincare status

   # Export all 8 .euclid-graphic SVGs into docsrc/_static/figures/
   geometor-poincare figures

   # Compile concordance, bibliography, persons, and glossary RST pages
   geometor-poincare compile-apparatus

Python API Example:

.. code-block:: python

   import sympy as sp
   from geometor.model import Model
   from geometor.poincare.disk import (
       construct_hyperbolic_geodesic,
       hyperbolic_cross_ratio_and_quadrance,
   )

   # Create an exact symbolic model of the Poincaré conformal unit disk
   model = Model("poincare_demo", auto_intersect=False)
   p = model.set_point(sp.Rational(1, 2), sp.Integer(0))
   q = model.set_point(sp.Integer(0), sp.Rational(1, 2))

   # Construct the unique orthogonal circle (hyperbolic geodesic) through P and Q
   geodesic = construct_hyperbolic_geodesic(model, p, q)
   metrics = hyperbolic_cross_ratio_and_quadrance(p, q, geodesic.U, geodesic.V)
   print("Conformal quadrance tau(P, Q):", metrics.conformal_quadrance)
