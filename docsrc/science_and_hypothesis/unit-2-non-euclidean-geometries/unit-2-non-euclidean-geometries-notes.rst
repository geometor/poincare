:layout: book

.. _science-and-hypothesis-unit-2-notes:

Unit II: Non-Euclidean Geometries — Scholarly Notes
===================================================

.. rubric:: Exact Symbolic Geometry, Rational Trigonometry & Cross-Repository Commentary

.. contents:: In These Notes
   :local:
   :depth: 2
   :backlinks: none

1. Circle Inversion & Orthogonal Circles (``geometor/casey`` & ``geometor/lemoine``)
------------------------------------------------------------------------------------

Poincaré's :term:`Translation Dictionary <dictionnaire-poincare>` (``Fig. 2``, :ref:`Concordance PC.04 <concordance>`) rests synthetically on two classical pillars digitized in the GEOMETOR canon:

* **Casey's Orthogonal Circle Criterion (``geometor/casey``)**: In :person:`John Casey <casey>`'s *Sequel to Euclid* (:cite:`Casey 1888 <casey-1888>`, Book III & Book VI Section V), a circle $\mathcal{C}(C, r)$ cuts the unit horizon $\Omega: x^2 + y^2 = 1$ orthogonally if and only if the power of $O$ with respect to $\mathcal{C}$ equals $R_\Omega^2 = 1$, i.e. $|OC|^2 - r^2 = 1$, which holds if and only if $\mathcal{C}$ passes through the :term:`horizon inverse <inversion-orthogonale>` $P^* = P / \|P\|^2$ of every point $P \in \mathcal{C}$.
* **Lemoine's 1902 *Géométrographie* (``geometor/lemoine``)**: Published in Paris in 1902—the exact year of *La Science et l'Hypothèse*—:person:`Émile Lemoine <lemoine>`'s :cite:`*Géométrographie* <lemoine-1902>` analyzes ruler-and-compass inversion via **Euclid VI.8** (:cite:`Heath 1908 <euclid-heath-1908>`): erecting the perpendicular chord $T_1 T_2 \perp OP$ inside $\Omega$ and taking the pole where the tangents at $T_1, T_2$ meet ray $OP$ constructs $P^*$ over the exact base field $\mathbb{Q}(P)$ without introducing a single extraneous radical! In :func:`geometor.poincare.disk.construct_hyperbolic_geodesic`, for $P=(1/2, 1/4)$ and $Q=(-2/5, 2/5)$, this yields exact rational $P^*=(8/5, 4/5)$ and circumcenter $C=(9/16, 33/16)$ with $|OC|^2 - r^2 = \frac{1170}{256} - \frac{914}{256} = 1$.

2. Cross-Ratio Metric & Wildberger's Rational Hyperbolic Quadrance (``geometor/pappus`` & ``geometor/wildberger``)
------------------------------------------------------------------------------------------------------------------

Poincaré defines the distance between $P, Q \in \mathbb{D}$ via :person:`Pappus <pappus>`'s anharmonic ratio $\chi(P, Q; U, V) = \frac{|PV|\cdot|QU|}{|PU|\cdot|QV|}$. In :func:`geometor.poincare.disk.hyperbolic_cross_ratio_and_quadrance` (:ref:`Concordance PC.05 <concordance>`), this classical logarithmic formula is united with :person:`Norman Wildberger <wildberger>`'s transcendental-free **Universal Hyperbolic Geometry** (:cite:`Wildberger 2005/2013 <wildberger-2005>`, ``geometor/wildberger``):

.. math::

   \tau(P, Q) = \frac{\|P - Q\|^2}{\|1 - \overline{P}Q\|^2} \in \mathbb{Q}, \qquad
   q_{\mathrm{UHG}}(P, Q) = -\frac{4\tau(P, Q)}{\bigl(1 - \tau(P, Q)\bigr)^2} = -\frac{(\chi^2 - 1)^2}{4\chi^2}.

Whenever $P, Q \in \mathbb{Q}^2 \cap \mathbb{D}$, both the conformal quadrance $\tau(P, Q) = \tanh^2(d_H/2)$ and Wildberger's hyperbolic quadrance $q_{\mathrm{UHG}}(P, Q) = -\sinh^2(d_H)$ remain **100% rational numbers** even when the ideal endpoints $U, V$ lie in a quadratic field $\mathbb{Q}(\sqrt{d})$!

3. Postulate V, Ideal Triangles & Saccheri's Acute Summit (``geometor/euclid``, ``geometor/elements``)
------------------------------------------------------------------------------------------------------

Figures 3–5 realize in exact rational arithmetic the classic counterexamples to Euclid's Fifth Postulate (`G.1`–`G.28` neutral core in ``geometor/elements``):

* **Horoparallels & Ultraparallels (``Fig. 3``)**: Over base line $L_{\mathrm{hyp}}$ with Pythagorean endpoints $U_L(4/5, -3/5), V_L(-4/5, -3/5)$, point $P(1/6, 2/5)$ admits two limiting :term:`horoparallels <horoparallele>` sharing $U_L$ or $V_L$ on $\partial\Omega$ and infinitely many :term:`ultraparallels <ultraparallele>` strictly disjoint in $\overline{\mathbb{D}}$.
* **Rational Ideal Triangle (``Fig. 4``)**: Vertices $U_1(1,0), U_2(-3/5,4/5), U_3(-3/5,-4/5)$ produce orthogonal side circles with pure rational centers $(1,2), (1,-2), (-5/3,0)$, radii $(2, 2, 4/3)$, and exact tangent spreads $(0,0,0)$—realizing Gauss and Lobachevsky's maximum finite area $\pi$ at angle sum $0$.
* **Saccheri Quadrilateral (``Fig. 5``)**: Over $A_1(-1/3,0), A_2(1/3,0)$, erecting equal hyperbolic legs ($q_{\mathrm{UHG}} = -225/64$) to $B_1(-17/39, 20/39)$ and $B_2(17/39, 20/39)$ refutes :person:`Saccheri <saccheri>`'s Right Angle Hypothesis by an exact rational inequality: the summit spread at $B_1, B_2$ is $s = \frac{64}{145} < 1$.

4. Poincaré's Fourth Geometry & Chromogeometry's Red Metric
-----------------------------------------------------------

Poincaré's little-known **Fourth Geometry** (FR pp. 60–61 / EN p. 46; :ref:`Concordance PC.07 <concordance>`) corresponds geometrically to the **exterior** $x^2 + y^2 > 1$ of the fundamental horizon (de Sitter / single-sheeted hyperboloid plane of signature $(+, -)$), where lines tangent to $\Omega$ are **null (isotropic) lines perpendicular to themselves** ($Q_{\mathrm{red}}(v, v) = 0$)—directly anticipating Minkowski spacetime (1905–1908) and Wildberger's **Red relativistic metric** in Chromogeometry (``geometor/wildberger``).
