import TGLExt.TheFactorObject
import TGLExt.Commutant

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A PONTE DOS PORTADORES — o certificado e o comutante falam a mesma língua
  [BANCADA — 27/08/2026 · marco M4 · tarefa (a) rumo ao 4/4]

O certificado enuncia as suas cláusulas sobre os **portadores** dos objetos de álgebra;
as provas das ondas recentes vivem em `commutantSet`. Faltava a ponte — e ela **fecha**,
porque a mathlib dá `coe_centralizer_centralizer` e porque **`towerImage` já era
fechada por estrela nesta árvore** (`towerImage_star_closed`, que estava lá esperando).

* ★★ `towerImage_star_eq` — a imagem da torre é IGUAL à sua estrelada;
* ★★★ **`theFactorObject_carrier`** — o portador do FATOR **É** o bicomutante da
  imagem da torre: as duas línguas são a mesma.

β jamais entra; nada move o gate.
-/

namespace TGLExt

variable {P : SiteProfile}

/-- ★★ **A IMAGEM DA TORRE É FECHADA POR ESTRELA**, e portanto igual à sua estrelada. -/
theorem towerImage_star_eq (P : SiteProfile) :
    star (towerImage P) = towerImage P := by
  ext T
  rw [Set.mem_star]
  constructor
  · intro h
    have h2 := towerImage_star_closed h
    rwa [star_star] at h2
  · intro h
    exact towerImage_star_closed h

/-- ★★★ **O PORTADOR DO FATOR É O BICOMUTANTE DA IMAGEM DA TORRE**. -/
theorem theFactorObject_carrier (P : SiteProfile) :
    (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))
      = commutantSet (commutantSet (towerImage P)) := by
  have h : (theFactorObject P : Set (TowerHilbert P →L[ℂ] TowerHilbert P))
      = ((StarSubalgebra.centralizer ℂ
          ((StarSubalgebra.centralizer ℂ (towerImage P) :
            StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) :
              Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :
        StarSubalgebra ℂ (TowerHilbert P →L[ℂ] TowerHilbert P)) :
          Set (TowerHilbert P →L[ℂ] TowerHilbert P)) := rfl
  rw [h, StarSubalgebra.coe_centralizer_centralizer, towerImage_star_eq,
      Set.union_self]
  rfl

end TGLExt
