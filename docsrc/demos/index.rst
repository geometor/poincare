:navigation: header
:order: 25

.. _poincare-demos:

demos
=====

.. rubric:: Exact Symbolic Poincaré Conformal Hyperbolic Disk Demonstrations (``SymPy`` + ``geometor.model``)

In strict accordance with **GEOMETOR's Content / Code Separation**, executable Python constructions live outside the historical ``:layout: book`` pages of *La Science et l'Hypothèse* and operate in ``geometor.poincare.disk`` and ``demos/`` with **zero ``float`` or ``sp.Float`` coordinates**.

Because Poincaré's conformal dictionary represents the hyperbolic plane inside the Euclidean unit disk $\mathbb{D} = \{(x, y) : x^2 + y^2 < 1\}$ bounded by the ideal horizon $\Omega: x^2 + y^2 = 1$, every hyperbolic geodesic is either a Euclidean diameter through $O(0,0)$ or a Euclidean circle cutting $\Omega$ orthogonally ($|OC|^2 - r^2 = 1$). Straightedge-and-compass constructions in ``geometor.model`` therefore execute **100% exact hyperbolic geometry** over $\mathbb{Q}$ and quadratic radical extensions.

----

1. Horizon Inversion, Orthogonal Geodesic Circles & Rational Quadrances
-----------------------------------------------------------------------

Constructs Euclidean inversion $P \mapsto P^* = P / \|P\|^2$ in $\Omega$, circumscribes the unique orthogonal geodesic circle through $(P, Q, P^*)$, and verifies the exact polynomial bridge between Poincaré's 4-point cross-ratio $\chi(P, Q; U, V)$ and Norman Wildberger's Rational Hyperbolic Quadrance $q_{\mathrm{UHG}}(P, Q) \in \mathbb{Q}$:

.. math::

   (1 - \tau)^2 (\chi^2 + 1)^2 = 4 (1 + \tau)^2 \chi^2,
   \qquad
   q_{\mathrm{UHG}}(P, Q) = -\frac{4\tau}{(1 - \tau)^2} = -\sinh^2 d_{\mathbb{H}}(P, Q).

.. literalinclude:: ../../demos/inversion_and_geodesics.py
   :language: python
   :linenos:

----

2. Limiting Horoparallels, Ultraparallels & Independence of Postulate V
-----------------------------------------------------------------------

Constructs two asymptotic horoparallels $\ell_1, \ell_2$ and two ultraparallels $m_1, m_2$ through $P(\frac{1}{6}, \frac{2}{5})$ relative to the rational geodesic $L_{\mathrm{hyp}}$ joining $(\frac{4}{5}, -\frac{3}{5})$ and $(-\frac{4}{5}, -\frac{3}{5})$, proving algebraically via ``intersect_2d`` that Euclid's Fifth Postulate fails inside $\mathbb{D}$ while Postulates I–IV hold identically.

.. literalinclude:: ../../demos/ultraparallels_and_fifth_postulate.py
   :language: python
   :linenos:

----

3. Pythagorean Ideal Triangle & Saccheri Quadrilateral Angular Defect
---------------------------------------------------------------------

Constructs the ideal triangle $\triangle U_1 U_2 U_3$ on $U_1(1,0), U_2(-\frac{3}{5},\frac{4}{5}), U_3(-\frac{3}{5},-\frac{4}{5})$ with rational side centers $(1,2), (1,-2), (-\frac{5}{3},0)$, rational radii $2, 2, \frac{4}{3}$, and interior spreads $(0, 0, 0)$, alongside the rational Saccheri quadrilateral $A_1 A_2 B_2 B_1$ with equal leg UHG quadrances $-\frac{225}{64}$ and strictly acute summit spreads $\frac{64}{145} < 1$.

.. literalinclude:: ../../demos/ideal_and_saccheri_triangles.py
   :language: python
   :linenos:

----

4. Heated-Disk Optical Rays, Beltrami–Klein Bridge & Stellar Parallax
---------------------------------------------------------------------

Realizes Poincaré's physical thermal parable ($T \propto 1 - r^2$, $n \propto (1 - r^2)^{-1}$), proves by pure straightedge radial projection $K(P) = \frac{2P}{1 + \|P\|^2}$ that Poincaré conformal arcs map onto Beltrami–Klein straight chords with identical Cayley–Klein quadrance $q_{\mathrm{CK}}$, and models Poincaré's astronomical parallax argument for geometric conventionalism.

.. literalinclude:: ../../demos/cayley_klein_and_heated_disk.py
   :language: python
   :linenos:
