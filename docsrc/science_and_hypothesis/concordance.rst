:layout: book

.. _concordance:

Poincaré Translation Dictionary & Cross-Corpus Concordance
==========================================================

.. rubric:: Mapping *La Science et l'Hypothèse* (1902 / 1905) across the GEOMETOR Digital Scriptorium & Symbolic Engine

Maps Henri Poincaré's La Science et l'Hypothèse (1902 / 1905)—specifically his synthetic a priori arithmetic induction, Dedekind vs. perceptual continua, Non-Euclidean Translation Dictionary, Heated-Disk conformal metric, Lie displacement groups, and geometric conventionalism—directly onto exact SymPy + geometor.model constructions and eleven sister GEOMETOR repositories.

----

I. Poincaré's Hyperbolic Translation Dictionary (*Ch. III, pp. 56–58*)
----------------------------------------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 24 30 46

   * - Lobachevskian Term
     - Euclidean Disk Model Translation (:math:`\mathbb{D} \subset \mathbb{R}^2`)
     - Exact ``geometor.poincare`` Algebraic Realization
   * - **Space / Hyperbolic Plane** (*L'espace / Le plan de Lobatchefsky*)
     - Open interior D = {(x, y) : x^2 + y^2 < 1} above/within the fundamental circle Ω: x^2 + y^2 = 1
     - construct_unit_horizon(model) -> (O, Ex, Omega) with interior predicate exact_sign(x^2 + y^2 - 1) < 0
   * - **Ideal Horizon / Infinity** (*Le plan fondamental / L'infini*)
     - Euclidean unit boundary circle ∂Ω: x^2 + y^2 = 1 where hyperbolic rulers shrink to zero
     - Boundary locus quadrance(O, U) == 1; rational Pythagorean points U = ((1-t^2)/(1+t^2), 2t/(1+t^2))
   * - **Hyperbolic Reflection in Ω** (*Inversion par rapport au cercle fondamental*)
     - Euclidean circle inversion ``P <-> P* = P / ||P||^2`` satisfying ``OP · OP* = 1 = R_Ω^2``
     - ``construct_inversion_in_horizon(model, P)`` via Euclid VI.8 chord-and-tangent construction
   * - **Hyperbolic Straight Line** (*La droite non-euclidienne*)
     - Euclidean diameter through ``O`` or unique Euclidean circle through ``(P, Q, P*)`` cutting Ω orthogonally (``||OC||^2 - r^2 = 1``)
     - ``construct_hyperbolic_geodesic(model, P, Q) -> HyperbolicGeodesic(carrier, U, V)``
   * - **Hyperbolic Angle** (*L'angle de deux droites*)
     - True Euclidean angle between the intersecting circles/diameters (100% conformal preservation)
     - ``line_spread(tan_1, tan_2)`` via ``euclidean_tangent_at_circle_point(model, circle, vertex)``
   * - **Hyperbolic Distance** (*La distance de deux points*)
     - Logarithm of the 4-point chord cross-ratio :math:`\chi(P, Q; U, V) = \frac{|PV|\cdot|QU|}{|PU|\cdot|QV|}` along the orthogonal circle
     - ``hyperbolic_cross_ratio_and_quadrance(P, Q, U, V)`` -> :math:`\ln\chi` paired with rational :math:`\tau(P,Q)` and Wildberger :math:`q_{\mathrm{UHG}}(P,Q)`
   * - **Rigid Hyperbolic Displacement** (*Le mouvement d'une figure invariable*)
     - Group ``PSU(1, 1)`` of Möbius inversions/homographies mapping Ω onto itself and preserving angles + cross-ratios
     - Compositions of orthogonal circle inversions preserving ``conformal_quadrance`` and ``wildberger_uhg_quadrance``
   * - **Beltrami–Klein Straight Chord** (*La corde rectiligne de Beltrami–Klein*)
     - Straight chord ``UV`` inside Ω connected to Poincaré arc ``UV`` by radial Weierstrass map ``K(P) = 2P / (1 + ||P||^2)``
     - ``construct_beltrami_klein_bridge(model)``: radial line ``OP`` meets straight chord ``UV`` at exact ``K(P)``

----

II. Cross-Repository Philosophical & Geometric Concordance
----------------------------------------------------------

PC.01 — Reasoning by Recurrence vs. Logicism and Formalism
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Introduction & Part I, Ch. I (FR pp. 9–28 / EN pp. 1–17) (:ref:`Unit I (Ch. I) <science-and-hypothesis-unit-1-en>`)
* **GEOMETOR Canon Links:** ``geometor/bertrand-russell``, ``geometor/hilbert``, ``geometor/aquinas``, ``geometor/hoenen``
* **Exact Symbolic Construction:** ``construct_dedekind_continuum_cut``

Poincaré defends complete mathematical induction (raisonnement par récurrence) as an irreducible synthetic a priori intuition condensing an infinite cascade of syllogisms into a single formula—challenging both Bertrand Russell's logicist reduction in Principles of Mathematics (1903) and David Hilbert's purely formal consistency program.

PC.02 — Dedekind's Irrational Cuts vs. Fechner's Perceptual Continuum
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part I, Ch. II (FR pp. 29–48 / EN pp. 18–34) (:ref:`Unit I (Ch. II) <science-and-hypothesis-unit-1-en>`)
* **GEOMETOR Canon Links:** ``geometor/euclid``, ``geometor/elements``, ``geometor/aristotle``, ``geometor/hilbert``
* **Exact Symbolic Construction:** ``construct_dedekind_continuum_cut``

Contrasts the physical continuum governed by Fechner's threshold paradox (A = B, B = C, A < C) against the mathematical continuum created via Dedekind cuts (such as √2/2 bisecting the unit square diagonal on x^2 + y^2 = 1), culminating in multidimensional cuts and Analysis Situs.

PC.03 — Independence of Euclid's Fifth Postulate: Lobachevsky Horoparallels & Ultraparallels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III §§ 1–2 (FR pp. 49–53 / EN pp. 35–39) (:ref:`Unit II (Ch. III) <science-and-hypothesis-unit-2-en>`)
* **GEOMETOR Canon Links:** ``geometor/euclid``, ``geometor/elements``, ``geometor/proclus``, ``geometor/hilbert``
* **Exact Symbolic Construction:** ``construct_ultraparallels_through_point``

Resolves two millennia of attempts (from Posidonius and Proclus to Saccheri and Legendre) to deduce Euclid's Postulate V from Postulates I–IV: in the Poincaré disk, through P ∉ L_hyp pass two asymptotic horoparallels and infinitely many disjoint ultraparallels.

PC.04 — Poincaré's Translation Dictionary & Relative Consistency via Circle Inversion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III §§ 5–6 (FR pp. 55–58 / EN pp. 41–43) (:ref:`Unit II (Ch. III) <science-and-hypothesis-unit-2-en>`)
* **GEOMETOR Canon Links:** ``geometor/casey``, ``geometor/lemoine``, ``geometor/pappus``, ``geometor/hilbert``
* **Exact Symbolic Construction:** ``construct_inversion_in_horizon / construct_hyperbolic_geodesic``

Applies Casey's theory of orthogonal circles and Lemoine/Adler horizon inversion (OP · OP* = 1) to translate every theorem of Lobachevsky into an ordinary Euclidean theorem about circles orthogonal to Ω—establishing the model-theoretic proof of relative consistency alongside Hilbert (1899).

PC.05 — Cross-Ratio Logarithmic Metric & Wildberger's Rational Hyperbolic Quadrance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III § 5 (FR p. 57 / EN p. 42) (:ref:`Unit II (Ch. III) <science-and-hypothesis-unit-2-en>`)
* **GEOMETOR Canon Links:** ``geometor/pappus``, ``geometor/wildberger``, ``geometor/klein``, ``geometor/codes``
* **Exact Symbolic Construction:** ``hyperbolic_cross_ratio_and_quadrance``

Unites Pappus's projective cross-ratio χ(P, Q; U, V) and Poincaré's logarithmic metric d_H = ln(χ) with Norman Wildberger's transcendental-free Universal Hyperbolic Quadrance q_UHG(P, Q) = -4τ/(1-τ)^2 over Q, proven algebraically equivalent via (1-τ)^2(χ^2+1)^2 = 4(1+τ)^2 χ^2.

PC.06 — Ideal Hyperbolic Triangles & Saccheri's Acute Angle Hypothesis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III §§ 1, 5 (FR pp. 50, 57 / EN pp. 36, 42) (:ref:`Unit II (Ch. III) <science-and-hypothesis-unit-2-en>`)
* **GEOMETOR Canon Links:** ``geometor/euclid``, ``geometor/elements``, ``geometor/wildberger``
* **Exact Symbolic Construction:** ``construct_ideal_hyperbolic_triangle / construct_saccheri_triangleDefect``

Demonstrates over pure Q that Pythagorean ideal vertices U_1=(1,0), U_2=(-3/5,4/5), U_3=(-3/5,-4/5) bound an orthogonal-circle triangle with rational centers (1,2), (1,-2), (-5/3,0) and 0° interior spreads (defect π), while Saccheri quadrilateral A_1 A_2 B_2 B_1 exhibits acute summit spread 64/145 < 1.

PC.07 — The Fourth Indefinite Geometry & Chromogeometric Red Metric
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III § 8 (FR pp. 60–61 / EN pp. 46–47) (:ref:`Unit II (Ch. III) <science-and-hypothesis-unit-2-en>`)
* **GEOMETOR Canon Links:** ``geometor/wildberger``, ``geometor/klein``, ``geometor/hilbert``
* **Exact Symbolic Construction:** ``hyperbolic_cross_ratio_and_quadrance``

Poincaré's little-noticed 'Fourth Geometry'—generated by reflections across the exterior of the fundamental circle where a real line can be perpendicular to itself (isotropic null line)—anticipates both Minkowski spacetime (1905–1908) and Wildberger's Red relativistic metric in Chromogeometry.

PC.08 — Veronese & Hilbert's Non-Archimedean Geometries (1899 Grundlagen Restoration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III § 10 & Ch. IV § 7 (FR pp. 63–64, 90) (:ref:`Unit II (Ch. III) <science-and-hypothesis-unit-2-en>`)
* **GEOMETOR Canon Links:** ``geometor/hilbert``, ``geometor/euclid``
* **Exact Symbolic Construction:** ``construct_dedekind_continuum_cut``

Critical philological restoration: the Flammarion French text contains Poincaré's explicit analysis of David Hilbert's 1899 Grundlagen der Geometrie non-Archimedean field Ω(t) (omitted in 1905 English printings derived from Poincaré's 1891 essay), linking Ch. II's third-order continuum directly to geometor/hilbert.

PC.09 — Poincaré's Heated-Disk World & Conformal Optical Geodesics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. IV §§ 5–6 (FR pp. 82–88 / EN pp. 64–69) (:ref:`Unit III (Ch. IV) <science-and-hypothesis-unit-3-en>`)
* **GEOMETOR Canon Links:** ``geometor/klein``, ``geometor/casey``, ``geometor/walter-russell``
* **Exact Symbolic Construction:** ``construct_heated_disk_optical_rays``

Models sentient observers inside a disk of radius R with temperature T ∝ R^2 - r^2, thermal dilation proportional to R^2 - r^2, and refractive index n ∝ (R^2 - r^2)^(-1): Fermat's principle forces light rays along orthogonal circular geodesics, making the world intrinsically infinite and Lobachevskian.

PC.10 — Lie Groups, Erlanger Programm & the Beltrami–Klein Radial Bridge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. III § 9 & Ch. IV §§ 4, 7 (FR pp. 61–63, 77–91 / EN pp. 47–48, 59–71) (:ref:`Unit III (Ch. IV) <science-and-hypothesis-unit-3-en>`)
* **GEOMETOR Canon Links:** ``geometor/klein``, ``geometor/pappus``, ``geometor/wildberger``, ``geometor/codes``
* **Exact Symbolic Construction:** ``construct_beltrami_klein_bridge``

Bridges Felix Klein's Erlanger Programm (geometor/klein) and interactive CindyJS Cayley–Klein models (geometor/codes) to Poincaré's conformal disk via the exact straightedge radial theorem: ray OP meets straight Beltrami–Klein chord UV at K(P) = 2P / (1 + ||P||^2).

PC.11 — Stellar Parallax, Crucial Experiments & Geometric Conventionalism
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Ch. V (FR pp. 92–109 / EN pp. 72–88) (:ref:`Unit IV (Ch. V) <science-and-hypothesis-unit-4-en>`)
* **GEOMETOR Canon Links:** ``geometor/bertrand-russell``, ``geometor/hoenen``, ``geometor/hilbert``
* **Exact Symbolic Construction:** ``construct_stellar_parallax_conventionalism``

Demonstrates why even an astronomical parallax measurement α + β + γ < π could never empirically falsify Euclidean geometry, since physics always tests the joint bundle (Geometry + Optics), and Euclidean geometry remains privileged by group-theoretic simplicity.

PC.12 — The Poincaré–Russell Debate (1898–1900) & Hoenen's Intelligible Matter Critique (1954)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Locus in Poincaré:** Part II, Chs. III–V & Bridge to Parts III–IV (Chs. VI, VII, IX) (:ref:`Unit IV (Notes) <science-and-hypothesis-unit-4-notes>`)
* **GEOMETOR Canon Links:** ``geometor/bertrand-russell``, ``geometor/hoenen``, ``geometor/aquinas``, ``geometor/aristotle``
* **Exact Symbolic Construction:** ``construct_stellar_parallax_conventionalism``

Synthesizes the three-cornered epistemological dialogue across GEOMETOR: Poincaré's conventionalism ('disguised definitions'), Bertrand Russell's defense of metric apriority and absolute relations (Mind 1898, RMM 1899–1900), and P. H. J. Hoenen's Thomistic resolution via abstraction in materia intelligibilis (De Noetica Geometriae, 1954).
