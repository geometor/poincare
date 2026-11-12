:layout: book

.. _science-and-hypothesis-unit-1-notes:

Unit I: Number and Magnitude — Scholarly Notes
==============================================

.. rubric:: Philological Collation, Symbolic Realization & Cross-Repository Commentary

.. contents:: In These Notes
   :local:
   :depth: 2
   :backlinks: none

1. Philological Collation: The *Kronecker* vs. *Dedekind* Textual Variant
-------------------------------------------------------------------------

Collating the 1902 Flammarion French text (:cite:`Poincaré 1902 <poincare-1902>`, pp. 31–40) against :person:`Greenstreet <greenstreet>`'s 1905 English translation (:cite:`Greenstreet 1905 <poincare-1905-greenstreet>`, pp. 19–27) uncovers one of the most instructive textual strata in *La Science et l'Hypothèse*:

* In Poincaré's original January 1893 essay *"Le continu mathématique"* (*Revue de Métaphysique et de Morale*, Vol. 1, pp. 26–34), Poincaré inadvertently wrote **Kronecker** where he described :person:`Richard Dedekind <dedekind>`'s 1872 *Stetigkeit und irrationale Zahlen* definition of irrational numbers by cuts (*Schnitte* / *coupures*) of $\mathbb{Q}$.
* When revising the essay for Ernest Flammarion, Poincaré corrected the attribution on French pp. 32–33 to **M. Dedekind** (*« Voyons donc quelle est la définition de M. Dedekind »* and *« au point de vue de M. Dedekind, le nombre incommensurable $\sqrt{2}$... »*), while overlooking a single residual occurrence on p. 40 (*« Nous reconnaissons là la conception de Kronecker »*).
* :person:`Greenstreet <greenstreet>`'s 1905 translation—working from an early impression retaining the 1893 reading—prints *"Kronecker"* at all three places (EN pp. 20, 21, 26), whereas :person:`Halsted <halsted>`'s 1905 American edition (:cite:`Halsted 1905 <poincare-1905-halsted>`) follows the corrected Flammarion text (*Dedekind* on pp. 32–33). Both witnesses are preserved *verbatim* in their respective tracks here so the editorial evolution remains transparent.

2. Poincaré's Synthetic *A Priori* Recurrence vs. Russell & Hilbert
-------------------------------------------------------------------

Chapter I forms the opening salvo in Poincaré's two-front foundational debate documented across the GEOMETOR Scriptorium (:ref:`Concordance PC.01 <concordance>`):

* **Against Logicism (``geometor/bertrand-russell``)**: In *The Principles of Mathematics* (1903; cf. :cite:`Russell 1897 <russell-1897>` and :cite:`Russell 1899 <russell-1899-reponse>`), :person:`Bertrand Russell <russell>` (following Frege and Peano) defined the natural numbers as the intersection of all inductive classes, claiming to reduce mathematical induction to an analytic definition. Poincaré countered (later expanded in *Science et Méthode*, 1908) that verifying the consistency and non-emptiness of that impredicative definition covertly presupposes the very synthetic *a priori* intuition of finite iteration it purports to eliminate (**petitio principii**).
* **Against Pure Formalism (``geometor/hilbert`` & ``geometor/hoenen``)**: In his Special Preface to Halsted's translation above, Poincaré remarks on :person:`Hilbert <hilbert>`'s *Grundlagen der Geometrie* (:cite:`Hilbert 1899 <hilbert-1899>`) that teaching geometry purely axiomatically *"is surely this time to burn all bridges of reliance upon sensory intuition."* Crucially, Hilbert's own metamathematical consistency proofs rely at every step on finite combinatorial induction—confirming Poincaré's thesis (echoed from a Thomistic standpoint by :person:`P. H. J. Hoenen <hoenen>` in :cite:`*De Noetica Geometriae* <hoenen-1954>`, Caput I § 6) that formal axiomatics presupposes intuitive arithmetic recurrence.

3. Exact Symbolic Realization in ``geometor.poincare`` (``Fig. 1``)
-------------------------------------------------------------------

In :func:`geometor.poincare.disk.construct_dedekind_continuum_cut`, Chapter II's crucial example (FR p. 39 / EN p. 26)—that over the first-order continuum $\mathbb{Q}^2$ a circle and a square's diagonal miss one another without :term:`Dedekind cuts <coupure-de-dedekind>`—is modeled with **zero floating-point approximations**:

* Over $\mathbb{Q}$, the perceptual threshold points $Q_1 = (2/3, 0)$ and $Q_2 = (3/4, 0)$ satisfy $Q(O, Q_1) = 4/9 < 1/2 < 9/16 = Q(O, Q_2)$, illustrating :person:`Fechner <fechner>`'s indistinguishability band around the cut.
* In ``geometor.model``, intersecting the exact diagonal line $x - y = 0$ through $O(0,0)$ and $S(1,1)$ with the unit horizon circle $\Omega: x^2 + y^2 = 1$ creates the quadratic extension $\mathbb{Q}(\sqrt{2})$ and yields the exact cut point $D = (\frac{\sqrt{2}}{2}, \frac{\sqrt{2}}{2})$ with rational quadrance $Q(O, D_x) = \frac{1}{2}$ verified symbolically via ``sp.simplify``.
