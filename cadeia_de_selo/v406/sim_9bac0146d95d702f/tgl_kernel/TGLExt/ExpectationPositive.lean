-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_001 (05/09/2026), transposta em 05/09/2026
-- A ESPERANCA CONDICIONAL DOS ANDARES: constructedLevelExpectations e o TERMO
--   (todos os campos por prova); expectation_not_imported_contract mede a
--   distancia ao contrato importado (obstrucao morre exatamente em w(0)=1/2).
-- Auditoria da gerencia (sessao d554e796): hashes 11/11; recompilacao
--   independente 8/8 exit 0; axiomas = [propext, Classical.choice, Quot.sound].
-- Transposicao MECANICA: este cabecalho + prefixo TGLExt. nos imports da
--   bancada; nada mais. Namespace ChatgptAudit = procedencia.
-- NAO move gate; nao e fisica. NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ExpectationBimodule
import Mathlib.Analysis.InnerProductSpace.Positive
import Mathlib.Analysis.Matrix.Order

set_option autoImplicit false
set_option maxHeartbeats 1000000
namespace ChatgptAudit
open TGLExt Matrix UniformSpace
open scoped ComplexOrder MatrixOrder
noncomputable section
variable {P : SiteProfile}

theorem towerPi_injective (P : SiteProfile) (N : ℕ) :
    Function.Injective (fun a : Matrix (chainIdx N) (chainIdx N) ℂ => towerPi P a) := by
  intro a b h
  apply levelEmbedding_injective P N
  have ho := congrArg (fun T : TowerHilbert P →L[ℂ] TowerHilbert P => T (hOmega P)) h
  rw [towerPi_omega, towerPi_omega] at ho
  exact ho

theorem expectation_star (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) :
    towerExpectation P N (star x) = star (towerExpectation P N x) := by
  apply factor_eq_of_omega (expectation_mem_factor _ _)
    (star_mem (expectation_mem_factor _ _))
  have hright : star (towerExpectation P N x) (hOmega P) ∈ levelSpace P N := by
    change star (towerPi P (expectationMatrix P N x)) (hOmega P) ∈ _
    rw [ContinuousLinearMap.star_eq_adjoint, ← towerPi_star, towerPi_omega]
    exact ⟨_,rfl⟩
  rw [expectation_omega]
  apply level_inner_ext (levelProject_mem _ _) hright
  intro b hb
  rw [levelProject_inner hb]
  simp only [ContinuousLinearMap.star_eq_adjoint]
  rw [ContinuousLinearMap.adjoint_inner_right, ContinuousLinearMap.adjoint_inner_right,
    expectation_compression N x hx hb]
  have ht := congrArg (starRingEnd ℂ) (levelProject_inner (omega_mem_level N) (x b))
  simpa only [inner_conj_symm] using ht.symm

theorem expectationMatrix_hermitian (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) (hsa : IsSelfAdjoint x) :
    (expectationMatrix P N x).IsHermitian := by
  apply towerPi_injective P N
  change towerPi P (expectationMatrix P N x)ᴴ = towerPi P (expectationMatrix P N x)
  rw [towerPi_star, ← ContinuousLinearMap.star_eq_adjoint]
  change star (towerExpectation P N x) = towerExpectation P N x
  rw [← expectation_star N x hx, hsa.star_eq]

theorem expectation_local_nonneg (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) (hpos : x.IsPositive)
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    0 ≤ tInner P N b (expectationMatrix P N x * b) := by
  have hi := hpos.inner_nonneg_right (levelEmbedding P N b)
  have he : inner ℂ (levelEmbedding P N b) (towerExpectation P N x (levelEmbedding P N b)) =
      inner ℂ (levelEmbedding P N b) (x (levelEmbedding P N b)) := by
    rw [expectation_compression N x hx ⟨b,rfl⟩, levelProject_inner ⟨b,rfl⟩]
  rw [← he] at hi
  change 0 ≤ inner ℂ ((tof P N b : TowerPre P) : TowerHilbert P)
    (towerPi P (expectationMatrix P N x) ((tof P N b : TowerPre P) : TowerHilbert P)) at hi
  rw [towerPi_coe, lmulPre_tof_at (le_refl N) (le_refl N), tPush_self, tPush_self,
    Completion.inner_coe] at hi
  change 0 ≤ innerPre P (tof P N b) (tof P N (expectationMatrix P N x * b)) at hi
  rwa [innerPre_tof_same] at hi

def repeatedColumn (N : ℕ) (v : chainIdx N → ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  fun i _ => v i

theorem repeated_column_inner (N : ℕ) (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (v : chainIdx N → ℂ) :
    tInner P N (repeatedColumn N v) (a * repeatedColumn N v) = star v ⬝ᵥ (a *ᵥ v) := by
  rw [tInner_apply]
  simp only [Matrix.mul_apply, Matrix.mulVec, dotProduct, Pi.star_apply, repeatedColumn]
  rw [← Finset.sum_mul]
  have hw : ∑ k, (towerW P N k : ℂ) = 1 := by
    exact_mod_cast towerW_sum P N
  rw [hw, one_mul]
  rfl

theorem expectationMatrix_positive (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) (hpos : x.IsPositive) :
    (expectationMatrix P N x).PosSemidef := by
  apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
    (expectationMatrix_hermitian N x hx hpos.isSelfAdjoint)
  intro v
  rw [← repeated_column_inner (P := P) N (expectationMatrix P N x) v]
  exact expectation_local_nonneg N x hx hpos _

theorem expectation_positive (N : ℕ) (x : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hx : x ∈ theFactorObject P) (hpos : 0 ≤ x) : 0 ≤ towerExpectation P N x := by
  have hp := expectationMatrix_positive N x hx ((ContinuousLinearMap.nonneg_iff_isPositive x).mp hpos)
  obtain ⟨b,hb⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hp.nonneg
  change 0 ≤ towerPi P (expectationMatrix P N x)
  rw [hb, show star b = bᴴ from rfl, towerPi_mul, towerPi_star,
    ← ContinuousLinearMap.star_eq_adjoint]
  exact star_mul_self_nonneg _

#print axioms expectation_star
#print axioms expectation_positive
end
end ChatgptAudit
