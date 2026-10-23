import TGLExt.F1Fecho394.BoundedTensorMapR2
import TGLExt.F1Fecho394.ExponentialTotalityR4
import Mathlib.Analysis.Normed.Operator.Extend
/-! Bounded second quantization of contractions on the SAME canonical sectors.
The algebraic tensor action is extended by continuity, restricted to the
constructed symmetric sectors, and then summed in the existing Fock space. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section
open UniformSpace
open scoped TensorProduct InnerProductSpace ENNReal
namespace F1Fecho.BoundedGamma
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Fecho.Exponential

def algebraic (A : H1 →L[ℂ] H1) : (n : ℕ) → Algebraic n →L[ℂ] Algebraic n
  | 0 => ContinuousLinearMap.id ℂ ℂ
  | n+1 => BoundedTensor.mapCLM A (algebraic A n)

theorem algebraic_bound (A : H1 →L[ℂ] H1) (n : ℕ) (x : Algebraic n) :
    ‖algebraic A n x‖ ≤ ‖A‖^n * ‖x‖ := by
  induction n with
  | zero => change ‖(x : ℂ)‖ ≤ ‖A‖^0 * ‖x‖; simp
  | succ n ih =>
    change ‖BoundedTensor.mapCLM A (algebraic A n) x‖ ≤ _
    have hn : ‖algebraic A n‖ ≤ ‖A‖^n :=
      (algebraic A n).opNorm_le_bound (pow_nonneg (norm_nonneg _) _) ih
    calc
      _ ≤ (‖A‖ * ‖algebraic A n‖) * ‖x‖ := BoundedTensor.norm_map_le A (algebraic A n) x
      _ ≤ (‖A‖ * ‖A‖^n) * ‖x‖ := by gcongr
      _ = _ := by rw [pow_succ]; ring

theorem algebraic_pure (A : H1 →L[ℂ] H1) (n : ℕ) (x : H1) :
    algebraic A n (pureAlgebraic x n) = pureAlgebraic (A x) n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change BoundedTensor.mapCLM A (algebraic A n) (x ⊗ₜ[ℂ] pureAlgebraic x n) = _
    rw [BoundedTensor.mapCLM_tmul,ih]
    rfl

def tensor (A : H1 →L[ℂ] H1) (n : ℕ) : TensorHilbert n →L[ℂ] TensorHilbert n :=
  ((Completion.toComplL : Algebraic n →L[ℂ] TensorHilbert n).comp (algebraic A n)).extend
    (Completion.toComplL : Algebraic n →L[ℂ] TensorHilbert n)

@[simp] theorem tensor_coe (A : H1 →L[ℂ] H1) (n : ℕ) (x : Algebraic n) :
    tensor A n (x : TensorHilbert n) = (algebraic A n x : TensorHilbert n) := by
  exact ContinuousLinearMap.extend_eq _ Completion.denseRange_coe
    (Completion.isUniformInducing_coe _) x

theorem tensor_bound (A : H1 →L[ℂ] H1) (n : ℕ) (x : TensorHilbert n) :
    ‖tensor A n x‖ ≤ ‖A‖^n * ‖x‖ := by
  refine Completion.induction_on x (isClosed_le (tensor A n).continuous.norm
    (continuous_const.mul continuous_norm)) ?_
  intro y
  simpa only [tensor_coe,Completion.norm_coe] using algebraic_bound A n y

theorem tensor_pure (A : H1 →L[ℂ] H1) (n : ℕ) (x : H1) :
    tensor A n (pureCompleted n x) = pureCompleted n (A x) := by
  simp only [pureCompleted,tensor_coe,algebraic_pure]

theorem tensor_mem (A : H1 →L[ℂ] H1) (n : ℕ) {x : TensorHilbert n}
    (hx : x ∈ symmetricSpace n) : tensor A n x ∈ symmetricSpace n := by
  let S := symmetricSpace n
  have hb : algebraicSymmetricSpan n ≤ S.comap (tensor A n).toLinearMap := by
    apply Submodule.span_le.mpr
    rintro _ ⟨y,rfl⟩
    change tensor A n (pureCompleted n y) ∈ S
    rw [tensor_pure]
    exact pureCompleted_mem n (A y)
  have hc : IsClosed (S.comap (tensor A n).toLinearMap : Set (TensorHilbert n)) :=
    (algebraicSymmetricSpan n).isClosed_topologicalClosure.preimage (tensor A n).continuous
  exact (algebraicSymmetricSpan n).topologicalClosure_minimal hb hc hx

def sector (A : H1 →L[ℂ] H1) (n : ℕ) : Sector n →L[ℂ] Sector n :=
  ((tensor A n).comp (symmetricSpace n).subtypeL).codRestrict
    (symmetricSpace n) (fun x => tensor_mem A n x.property)

@[simp] theorem sector_pure (A : H1 →L[ℂ] H1) (n : ℕ) (x : H1) :
    sector A n (pureTensor n x) = pureTensor n (A x) := by
  apply Subtype.ext
  exact tensor_pure A n x

theorem sector_bound (A : H1 →L[ℂ] H1) (n : ℕ) (x : Sector n) :
    ‖sector A n x‖ ≤ ‖A‖^n * ‖x‖ := tensor_bound A n x

theorem sector_contraction (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) (n : ℕ) (x : Sector n) :
    ‖sector A n x‖ ≤ ‖x‖ := by
  have hpow : ‖A‖^n ≤ 1 := pow_le_one₀ (norm_nonneg _) hA
  exact (sector_bound A n x).trans (by nlinarith [norm_nonneg x])

def gammaFun (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) (x : F) : F :=
  ⟨fun n => sector A n (x n), Memℓp.mono (lp.memℓp x).norm
    (fun n => by simpa using sector_contraction A hA n (x n))⟩

def gamma (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) : F →L[ℂ] F :=
  ({ toFun := gammaFun A hA
     map_add' x y := by apply lp.ext; funext n; exact (sector A n).map_add (x n) (y n)
     map_smul' c x := by apply lp.ext; funext n; exact (sector A n).map_smul c (x n) } : F →ₗ[ℂ] F).mkContinuous
    1 (fun x => by simpa using (lp.norm_mono (by norm_num : (2:ℝ≥0∞) ≠ 0)
      (fun n => sector_contraction A hA n (x n))))

@[simp] theorem gamma_apply (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) (x : F) (n : ℕ) :
    gamma A hA x n = sector A n (x n) := rfl

theorem gamma_norm_le (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) : ‖gamma A hA‖ ≤ 1 :=
  (gamma A hA).opNorm_le_bound (by norm_num) (fun x => by
    simpa using lp.norm_mono (by norm_num : (2:ℝ≥0∞) ≠ 0)
      (fun n => sector_contraction A hA n (x n)))

theorem gamma_exponential (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) (x : H1) :
    gamma A hA (exponential x) = exponential (A x) := by
  apply lp.ext
  funext n
  change sector A n ((weight n : ℂ) • pureTensor n x) =
    (weight n : ℂ) • pureTensor n (A x)
  rw [map_smul,sector_pure]

theorem gamma_vacuum (A : H1 →L[ℂ] H1) (hA : ‖A‖ ≤ 1) : gamma A hA vacuum = vacuum := by
  rw [← exponential_zero,gamma_exponential,map_zero]

end F1Fecho.BoundedGamma
#print axioms F1Fecho.BoundedGamma.algebraic_bound
#print axioms F1Fecho.BoundedGamma.tensor_bound
#print axioms F1Fecho.BoundedGamma.sector_contraction
#print axioms F1Fecho.BoundedGamma.gamma_norm_le
#print axioms F1Fecho.BoundedGamma.gamma_exponential
#print axioms F1Fecho.BoundedGamma.gamma_vacuum
