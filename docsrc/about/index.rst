:navigation: header
:order: 20
:nav_title: About

.. _about:
.. _about-index:

About
=====

.. rubric:: Extracting Historical Semantic Knowledge & Repurposing It for Exact Symbolic Reasoning

About This Edition
------------------

``geometor.poincare`` reconstructs the foundational geometrical, epistemological, and physical investigations of :person:`Henri Poincaré <poincare>` (1854–1912) centered on his seminal masterwork, *La Science et l'Hypothèse* (*Science and Hypothesis*, Paris: Ernest Flammarion, 1902; authorized translations 1905). At the turn of the twentieth century, Poincaré shattered the rigid dichotomy between synthetic *a priori* intuition and raw empirical inductivism by establishing the doctrine of geometric **conventionalism**: geometric axioms are neither self-evident metaphysical necessities nor experimental facts subject to empirical refutation, but free conventions—guided by experience, yet chosen for their supreme mathematical convenience (*les axiomes ne sont que des définitions déguisées*).

The codex extracts the implicit argumentative and mathematical architecture of the work across four core units: *Number and Magnitude* (mathematical induction and the continuous magnitude), *Non-Euclidean Geometries* (Lobachevsky, Riemann, and the Euclidean–Hyperbolic Translation Dictionary), *Space and Geometry* (visual, tactile, and motor space, the heated-disk world, and transformation groups), and *Experience and Geometry* (stellar parallax and physical hypotheses). Powered by ``photon-platform/publish``, every section is presented across four synchronized tracks: verbatim public-domain English translations, verbatim 1902 French text (including *Les Géométries de Hilbert*), deductive structural summaries, and critical notes featuring calibrated ``.euclid-graphic`` SVG reconstructions and exact symbolic demonstrations.

This edition anchors Poincaré's revolutionary geometric vision directly within the GEOMETOR ecosystem. Poincaré's insight that non-Euclidean geometries can be faithfully modeled through Euclidean circle inversion and orthogonal circular arcs bridges the axiomatic classical tradition of :person:`Euclid's <euclid>` *Elements* (``geometor/euclid``) and :person:`Proclus's <proclus>` commentary (``geometor/proclus``) with the rigorous axiomatic modernism of :person:`David Hilbert's <hilbert>` *Grundlagen der Geometrie*, the epistemological debates of :person:`Bertrand Russell <russell>`, the scholastic noetics of :person:`Fr. Peter Hoenen S.J. <hoenen>` (*De Noetica Geometriae*), the projective cross-ratio invariants of :person:`Pappus of Alexandria <pappus>` (``geometor/pappus``), and Norman J. Wildberger's Rational Hyperbolic Geometry in ``geometor.model``.

The GEOMETOR Mission
--------------------

The GEOMETOR project, initiated and directed by **phi ARCHITECT**, is dedicated to the complete digital renaissance and computational re-grounding of classical geometry and axiomatic thought. The mission advances across three foundational pillars:

1. **Extracting Historical Semantic Knowledge**: Moving beyond passive page scans, static PDFs, and raw OCR to recover the living deductive structure of 2,300+ years of geometric, axiomatic, and philosophical treatises. GEOMETOR elevates historical prose, marginal scholia, primary-source folios (via ``publish folio`` directives), and calibrated Ink-to-Vector ``.euclid-graphic`` diagrams into structured, machine-addressable semantic graphs. Each proposition, enunciation, step, hypothesis, and proof is rendered uniquely identifiable, computationally navigable, and interoperable across the entire historical canon.
2. **Exact Symbolic Grounding (``geometor.model``)**: Anchoring geometric constructions and spatial relations in 100% exact symbolic algebra via `SymPy` and Norman J. Wildberger's Rational Trigonometry invariants (quadrance, spread, cross-ratio). By operating strictly over exact algebraic number fields rather than floating-point approximations, GEOMETOR eliminates rounding degradation, preserves absolute mathematical truth, and guarantees that every geometric demonstration is provably exact.
3. **Repurposing Knowledge Across Mediums**: Re-deploying extracted semantic and algebraic structures across synchronized multi-track **Book Codices** and accessible EPUB 3 editions (powered by ``photon-platform/publish``), computable deductive canons (``geometor.elements``, ``geometor.etc``, ``geometor.pappus``, ``geometor.divine``), interactive SVG exploratory laboratories (``geometor.explorer``), ultra-high-definition visual broadcasts, and neuro-symbolic program synthesis (``geometor.seer``) across `geometor.com <https://geometor.com>`_.

Sources, Provenance & Methodology
---------------------------------

All primary textual witnesses archived in ``resources/science_and_hypothesis/sources/`` are **100% Public Domain** worldwide (Henri Poincaré died 17 July 1912; William John Greenstreet died 28 June 1930; George Bruce Halsted died 16 March 1922; Sir Joseph Larmor died 19 May 1942; all editions published 1902–1905) and are verified by SHA-256 checksums in ``resources/science_and_hypothesis/sources_manifest.json``:

* **1902 French Original (Paris: Ernest Flammarion)**: *La Science et l'Hypothèse*, Bibliothèque de Philosophie scientifique, 1902. Preserves Poincaré's Author Introduction, Parts I–IV (Chapters I–XIII), and the section *Les Géométries de Hilbert* in Chapter III (pp. 63–64).
* **1905 British English Translation (London: Walter Scott Publishing Co.)**: *Science and Hypothesis*, translated by **W. J. Greenstreet** with an extensive Prefatory Essay by **Sir Joseph Larmor**, Lucasian Professor of Mathematics at Cambridge.
* **1905 American English Translation (New York: The Science Press)**: *Science and Hypothesis*, authorized translation by **George Bruce Halsted**, containing **Henri Poincaré's Special Preface to the English Edition** and Halsted's English translation of *Hilbert's Geometries* (*Science*, 16 December 1904 / 1905 codex).

Editorial Collation Note
~~~~~~~~~~~~~~~~~~~~~~~~

Where Walter Scott's 1905 London edition compressed the conclusion of Chapter III (omitting *Les Géométries de Hilbert*) and trimmed technical sentences at the close of Chapters IV and V, the English track of this codex supplies Halsted's 1905 authorized English translation with explicit apparatus banners so every paragraph of Poincaré's 1902 French text has a complete, faithful English counterpart.
