import TGLExt.TheWitnessLinearOnWH
import TGLExt.TheConjugationMapsCommutants
import TGLExt.TheBoundaryDuality
import TGLExt.TheFactorObject

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A MONTAGEM — a conjugação como mapa dos operadores, e a cláusula instanciada
  [BANCADA — 26/08/2026 · marco M4 · o último elo construtivo]

## O passo

A v242 provou o teorema abstrato: **bijeção multiplicativa involutiva leva comutante em
comutante**, e daí **geradores no comutante ⟹ bicomutante inteiro no comutante**. A
v243 provou o que faltava para exibir a hipótese: a testemunha é **aditiva, antilinear
e contínua** em `WH`.

Esta pedra **monta**: define `Φ(T) = J∘T∘J` como **operador contínuo** de `WH` —
**linear**, porque duas antilineares compõem em linear — e prova que Φ é
**multiplicativa** e **involutiva**. Com isso, o teorema da v242 se **instancia**.

## O que se prova

* ★★★ **`conjByJ`** — `Φ(T) = J∘T∘J` **existe como operador contínuo** de `WH`;
* ★★★ **`conjByJ_mul`** — **multiplicativa**: `Φ(T·U) = Φ(T)·Φ(U)` (o `J²=1` cancela);
* ★★★ **`conjByJ_involutive`** — **involutiva**: `Φ(Φ(T)) = T`;
* ★★★ **`conjByJ_commutant`** — logo **leva comutante em comutante** (instância da v242);
* ★★★ **`conjByJ_bicommutant_in_commutant`** — **A CLÁUSULA, INSTANCIADA**: se Φ leva
  os geradores no comutante, leva o **BICOMUTANTE INTEIRO** no comutante.

## O QUE FALTA
Ligar a hipótese `Φ(geradores) ⊆ comutante` ao que a v241 provou pontualmente
(`J·π(a)·J = ρ(J a)`) — isto é, mostrar que `Φ(towerPi a) = rTowerPi (J a)` **como
operadores** e que a imagem direita está no comutante da imagem esquerda. β jamais
entra; nada move o gate.
-/

namespace TGLExt

variable {P : SiteProfile}

/-- ★★★ **A CONJUGAÇÃO COMO OPERADOR CONTÍNUO**: `Φ(T) = J∘T∘J`, linear porque duas
    antilineares compõem em linear. -/
noncomputable def conjByJ (P : SiteProfile)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) :
    TowerHilbert P →L[ℂ] TowerHilbert P where
  toFun := fun z => towerJ P (T (towerJ P z))
  map_add' := by
    intro z w
    rw [towerJ_add, map_add, towerJ_add]
  map_smul' := by
    intro c z
    rw [towerJ_conj_smul, map_smul, towerJ_conj_smul]
    simp
  cont := by
    exact (towerJ_continuous P).comp (T.continuous.comp (towerJ_continuous P))

theorem conjByJ_apply (P : SiteProfile)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) (z : TowerHilbert P) :
    conjByJ P T z = towerJ P (T (towerJ P z)) := rfl

/-- ★★★ **MULTIPLICATIVA**: o `J² = 1` cancela no meio. -/
theorem conjByJ_mul (P : SiteProfile)
    (T U : TowerHilbert P →L[ℂ] TowerHilbert P) :
    conjByJ P (T * U) = conjByJ P T * conjByJ P U := by
  ext z
  simp only [conjByJ_apply, ContinuousLinearMap.mul_apply, conjByJ_apply]
  rw [towerJ_involutive]

/-- ★★★ **INVOLUTIVA**. -/
theorem conjByJ_involutive (P : SiteProfile)
    (T : TowerHilbert P →L[ℂ] TowerHilbert P) :
    conjByJ P (conjByJ P T) = T := by
  ext z
  simp only [conjByJ_apply]
  rw [towerJ_involutive, towerJ_involutive]

/-- ★★★ **LEVA COMUTANTE EM COMUTANTE** — instância do teorema da v242. -/
theorem conjByJ_commutant (P : SiteProfile)
    (S : Set (TowerHilbert P →L[ℂ] TowerHilbert P)) :
    conjByJ P '' (commutantSet S) = commutantSet (conjByJ P '' S) :=
  conj_commutant (conjByJ P) (conjByJ_mul P) (conjByJ_involutive P) S

/-- ★★★ **A CLÁUSULA, INSTANCIADA**: geradores no comutante ⟹ BICOMUTANTE INTEIRO
    no comutante. É `J M J ⊆ M′` reduzido a uma hipótese sobre GERADORES. -/
theorem conjByJ_bicommutant_in_commutant (P : SiteProfile)
    (S : Set (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hgen : conjByJ P '' S ⊆ commutantSet S) :
    conjByJ P '' (commutantSet (commutantSet S)) ⊆ commutantSet S :=
  conj_bicommutant_in_commutant (conjByJ P) (conjByJ_mul P)
    (conjByJ_involutive P) S hgen


/-- ★★ **A CONJUGADA DE UMA AÇÃO É A AÇÃO DIREITA CONJUGADA**, como OPERADORES. -/
theorem conjByJ_towerPi (P : SiteProfile) {N : ℕ}
    (x : Matrix (chainIdx N) (chainIdx N) ℂ) :
    conjByJ P (towerPi P x) = rTowerPi P (profileJlevel P N x) := by
  ext z
  exact boundaryDuality P x z

/-- ★★★ **A HIPÓTESE FECHA**: a conjugada da imagem da torre está no comutante dela. -/
theorem conjByJ_towerImage_in_commutant (P : SiteProfile) :
    conjByJ P '' (towerImage P) ⊆ commutantSet (towerImage P) := by
  rintro _ ⟨T, ⟨N, x, rfl⟩, rfl⟩ _ ⟨M, y, rfl⟩
  rw [conjByJ_towerPi]
  ext z
  simp only [ContinuousLinearMap.mul_apply]
  exact (rTowerPi_comm_towerPi P (profileJlevel P N x) y z).symm

/-- ★★★★ **`J M J ⊆ M′` --- A PRIMEIRA CLÁUSULA DE COMUTANTE, no nível do
    BICOMUTANTE.** Sem o teorema de von Neumann: a rota é algébrica. -/
theorem J_M_J_in_commutant (P : SiteProfile) :
    conjByJ P '' (commutantSet (commutantSet (towerImage P)))
      ⊆ commutantSet (towerImage P) :=
  conjByJ_bicommutant_in_commutant P (towerImage P)
    (conjByJ_towerImage_in_commutant P)

end TGLExt
