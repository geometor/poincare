:layout: book

.. _science-and-hypothesis-unit-3-notes:

Unit III: Space and Geometry — Scholarly Notes
==============================================

.. rubric:: Variational Optics of the Heated Disk, Erlanger Programm & Beltrami–Klein Bridge

.. contents:: In These Notes
   :local:
   :depth: 2
   :backlinks: none

1. Fermat's Principle in the Heated Disk ($n \propto (R^2 - r^2)^{-1}$)
------------------------------------------------------------------------

In Chapter IV (FR pp. 84–87 / EN pp. 65–68; ``Fig. 6``, :ref:`Concordance PC.09 <concordance>`), :person:`Poincaré <poincare>` endows the open disk $r < R$ (normalized to $R = 1$) with two coupled physical laws:

1. **Thermal Ruler Law**: A ruler of nominal length $ds_H$ placed at Euclidean radius $r = \sqrt{x^2 + y^2}$ contracts to Euclidean length $ds_E \propto (1 - r^2)\,ds_H$, inducing the **Poincaré conformal metric**:

   .. math::

      ds_H = \frac{2\,\sqrt{dx^2 + dy^2}}{1 - (x^2 + y^2)} \quad (K = -1).

2. **Optical Refraction Law**: With refractive index $n(x, y) = \frac{2}{1 - (x^2 + y^2)}$, Fermat's principle of least optical time $\delta \int n(x, y)\,ds_E = 0$ minimizes the exact same hyperbolic arc-length functional $\int ds_H$! Hence **every optical ray in Poincaré's heated enclosure is an exact circular arc orthogonal to $\partial\Omega$**, constructed symbolically over $\mathbb{Q}$ in :func:`geometor.poincare.disk.construct_heated_disk_optical_rays`.

2. Klein's *Erlanger Programm* & the Straightedge Beltrami–Klein Bridge (``Fig. 7``)
------------------------------------------------------------------------------------

Chapter IV's thesis—that *"the object of geometry is the study of a particular group"*—is Poincaré's epistemological synthesis of :person:`Felix Klein <klein>`'s 1872 *Erlanger Programm* (:cite:`Klein 1872 <klein-1872>`, digitized in ``geometor/klein``) and :person:`Sophus Lie <lie>`'s classification of Riemann–Helmholtz–Lie mobility groups (cf. :person:`Helmholtz <helmholtz>` 1868).

How does Klein and :person:`Beltrami <beltrami>`'s **projective disk model** (:cite:`Beltrami 1868 <beltrami-1868>`, interactive CindyJS applets in ``geometor/codes``), where hyperbolic lines are **straight Euclidean chords** $UV$, relate to Poincaré's **conformal disk model**, where hyperbolic lines are **orthogonal circular arcs** $\overset{\frown}{UV}$?

In :func:`geometor.poincare.disk.construct_beltrami_klein_bridge` (``Fig. 7``, :ref:`Concordance PC.10 <concordance>`), we prove a remarkable **purely algebraic straightedge theorem** over $\mathbb{Q}$:

* Let $U, V \in \partial\Omega$ be the shared ideal endpoints of a hyperbolic line, so the orthogonal Poincaré circle satisfies $x^2 + y^2 - 2(c_x x + c_y y) + 1 = 0$ and the radical axis (straight Beltrami–Klein chord $UV$) satisfies $c_x X + c_y Y = 1$.
* For *any* point $P = (x, y)$ on the Poincaré circular arc $\overset{\frown}{UV}$, $c_x x + c_y y = \frac{1 + x^2 + y^2}{2}$.
* Therefore, projecting $P$ **radially from the disk center $O(0, 0)$** via the Weierstrass map

  .. math::

     K(P) = \frac{2P}{1 + \|P\|^2} = \left(\frac{2x}{1 + x^2 + y^2},\; \frac{2y}{1 + x^2 + y^2}\right)

  satisfies $c_x K_x + c_y K_y = \frac{2(c_x x + c_y y)}{1 + x^2 + y^2} = 1$, proving that **the Euclidean straight line $OP$ meets the straight chord $UV$ at the exact Beltrami–Klein image $K(P)$**! Furthermore, the conformal quadrance $\tau(P_1, P_2)$ induces the exact Cayley–Klein chordal quadrance $q_{\mathrm{CK}}(K_1, K_2) = \frac{4\tau}{(1 + \tau)^2}$ on the projective model.
