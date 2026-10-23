import TGLExt.F1Fecho394.AntilinearTensorR4
/-! Gamma(J) on the very same sectors and direct sum already constructed by
F1.REDE. No Weyl, modular Tomita or KMS claim is supplied by these identities. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open scoped TensorProduct InnerProductSpace ENNReal
open UniformSpace
namespace F1Fecho.Antilinear
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock F1Rede.SectorDirectSum

def algebraicJ (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) :
    (n : ℕ) → Algebraic n ≃ₛₗᵢ[starRingEnd ℂ] Algebraic n
  | 0 => scalarConj
  | n+1 => tensorAnti j (algebraicJ j n)

theorem algebraicJ_pure (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (n : ℕ) (x : H1) :
    algebraicJ j n (pureAlgebraic x n) = pureAlgebraic (j x) n := by
  induction n with
  | zero => exact scalarConj_one
  | succ n ih =>
    change tensorAnti j (algebraicJ j n) (x ⊗ₜ[ℂ] pureAlgebraic x n) = _
    rw [tensorAnti_tmul, ih]
    rfl

theorem algebraicJ_involutive (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (hj : Function.Involutive j) (n : ℕ) : Function.Involutive (algebraicJ j n) := by
  induction n with
  | zero => exact scalarConj_involutive
  | succ n ih => exact tensorAnti_involutive j (algebraicJ j n) hj ih

def tensorJ (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (n : ℕ) :
    TensorHilbert n ≃ₛₗᵢ[starRingEnd ℂ] TensorHilbert n := completionAnti (algebraicJ j n)

@[simp] theorem tensorJ_coe (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (n : ℕ) (x : Algebraic n) :
    tensorJ j n (x : TensorHilbert n) = (algebraicJ j n x : TensorHilbert n) :=
  completionAnti_coe _ _

theorem tensorJ_pure (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (n : ℕ) (x : H1) :
    tensorJ j n (pureCompleted n x) = pureCompleted n (j x) := by
  simp only [pureCompleted, tensorJ_coe, algebraicJ_pure]

theorem tensorJ_mem (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (n : ℕ) {x : TensorHilbert n}
    (hx : x ∈ symmetricSpace n) : tensorJ j n x ∈ symmetricSpace n := by
  let S := symmetricSpace n
  have hbase : algebraicSymmetricSpan n ≤ S.comap (tensorJ j n).toLinearMap := by
    apply Submodule.span_le.mpr
    rintro _ ⟨y,rfl⟩
    change tensorJ j n (pureCompleted n y) ∈ S
    rw [tensorJ_pure]
    exact pureCompleted_mem n (j y)
  have hclosed : IsClosed (S.comap (tensorJ j n).toLinearMap : Set (TensorHilbert n)) :=
    (algebraicSymmetricSpan n).isClosed_topologicalClosure.preimage (tensorJ j n).continuous
  exact (algebraicSymmetricSpan n).topologicalClosure_minimal hbase hclosed hx

theorem tensorJ_involutive (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (hj : Function.Involutive j) (n : ℕ) : Function.Involutive (tensorJ j n) :=
  completionAnti_involutive _ (algebraicJ_involutive j hj n)

def sectorJ (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (hj : Function.Involutive j)
    (n : ℕ) : Sector n ≃ₛₗᵢ[starRingEnd ℂ] Sector n where
  toFun x := ⟨tensorJ j n x,tensorJ_mem j n x.property⟩
  invFun x := ⟨tensorJ j n x,tensorJ_mem j n x.property⟩
  left_inv x := by apply Subtype.ext; exact tensorJ_involutive j hj n x
  right_inv x := by apply Subtype.ext; exact tensorJ_involutive j hj n x
  map_add' x y := by apply Subtype.ext; exact (tensorJ j n).map_add x y
  map_smul' c x := by apply Subtype.ext; exact (tensorJ j n).map_smulₛₗ c x
  norm_map' x := (tensorJ j n).norm_map x

@[simp] theorem sectorJ_pure (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (hj : Function.Involutive j) (n : ℕ) (x : H1) :
    sectorJ j hj n (pureTensor n x) = pureTensor n (j x) := by
  apply Subtype.ext
  exact tensorJ_pure j n x

theorem sectorJ_involutive (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (hj : Function.Involutive j) (n : ℕ) : Function.Involutive (sectorJ j hj n) := by
  intro x; apply Subtype.ext; exact tensorJ_involutive j hj n x

section Sum
variable {E : ℕ → Type*} [∀ n, NormedAddCommGroup (E n)]
  [∀ n, InnerProductSpace ℂ (E n)] [∀ n, CompleteSpace (E n)]

def diagonalAntiFun (j : ∀ n, E n ≃ₛₗᵢ[starRingEnd ℂ] E n) (f : SumSpace E) : SumSpace E :=
  ⟨fun n => j n (f n), Memℓp.mono (lp.memℓp f).norm (fun n => by simp)⟩

@[simp] theorem diagonalAntiFun_apply (j : ∀ n, E n ≃ₛₗᵢ[starRingEnd ℂ] E n)
    (f : SumSpace E) (n : ℕ) : diagonalAntiFun j f n = j n (f n) := rfl

def diagonalAnti (j : ∀ n, E n ≃ₛₗᵢ[starRingEnd ℂ] E n) :
    SumSpace E ≃ₛₗᵢ[starRingEnd ℂ] SumSpace E where
  toFun := diagonalAntiFun j
  invFun := diagonalAntiFun (fun n => (j n).symm)
  left_inv f := by ext n; simp
  right_inv f := by ext n; simp
  map_add' f g := by ext n; simp [diagonalAntiFun]
  map_smul' c f := by ext n; exact (j n).map_smulₛₗ c (f n)
  norm_map' f := by
    rw [lp.norm_eq_tsum_rpow (by norm_num : 0 < (2 : ℝ≥0∞).toReal),
      lp.norm_eq_tsum_rpow (by norm_num : 0 < (2 : ℝ≥0∞).toReal)]
    simp

@[simp] theorem diagonalAnti_apply (j : ∀ n, E n ≃ₛₗᵢ[starRingEnd ℂ] E n)
    (f : SumSpace E) (n : ℕ) : diagonalAnti j f n = j n (f n) := rfl

theorem diagonalAnti_single (j : ∀ n, E n ≃ₛₗᵢ[starRingEnd ℂ] E n) (n : ℕ) (x : E n) :
    diagonalAnti j (sectorEmbedding n x) = sectorEmbedding n (j n x) := by
  ext k
  by_cases h : k = n
  · subst k; simp
  · simp [lp.single_apply_ne, h]

theorem diagonalAnti_involutive (j : ∀ n, E n ≃ₛₗᵢ[starRingEnd ℂ] E n)
    (hj : ∀ n, Function.Involutive (j n)) : Function.Involutive (diagonalAnti j) := by
  intro f; ext n; exact hj n (f n)
end Sum

def gammaJ (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (hj : Function.Involutive j) :
    F ≃ₛₗᵢ[starRingEnd ℂ] F := diagonalAnti (sectorJ j hj)

theorem gammaJ_involutive (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (hj : Function.Involutive j) :
    Function.Involutive (gammaJ j hj) := diagonalAnti_involutive _ (sectorJ_involutive j hj)

theorem gammaJ_vacuum (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1) (hj : Function.Involutive j) :
    gammaJ j hj vacuum = vacuum := by
  change diagonalAnti (sectorJ j hj) (sectorEmbedding 0 vacuumSector) = _
  rw [diagonalAnti_single]
  simp only [vacuumSector, sectorJ_pure, map_zero]
  rfl

theorem gammaJ_oneParticle (j : H1 ≃ₛₗᵢ[starRingEnd ℂ] H1)
    (hj : Function.Involutive j) (x : H1) :
    gammaJ j hj (oneParticle x) = oneParticle (j x) := by
  change diagonalAnti (sectorJ j hj) (sectorEmbedding 1 (pureTensor 1 x)) = _
  rw [diagonalAnti_single,sectorJ_pure]
  rfl

def canonicalFockJ : F ≃ₛₗᵢ[starRingEnd ℂ] F :=
  gammaJ F1Rede.CanonicalWedge.Jcandidate F1Rede.CanonicalWedge.Jcandidate_involutive
theorem canonicalFockJ_involutive : Function.Involutive canonicalFockJ :=
  gammaJ_involutive _ _
theorem canonicalFockJ_vacuum : canonicalFockJ vacuum = vacuum := gammaJ_vacuum _ _
theorem canonicalFockJ_oneParticle (x : H1) :
    canonicalFockJ (oneParticle x) = oneParticle (F1Rede.CanonicalWedge.Jcandidate x) :=
  gammaJ_oneParticle _ _ x

end F1Fecho.Antilinear

#print axioms F1Fecho.Antilinear.gammaJ
#print axioms F1Fecho.Antilinear.gammaJ_involutive
#print axioms F1Fecho.Antilinear.gammaJ_vacuum
#print axioms F1Fecho.Antilinear.gammaJ_oneParticle
#print axioms F1Fecho.Antilinear.canonicalFockJ
#print axioms F1Fecho.Antilinear.canonicalFockJ_involutive
#print axioms F1Fecho.Antilinear.canonicalFockJ_vacuum
#print axioms F1Fecho.Antilinear.canonicalFockJ_oneParticle
