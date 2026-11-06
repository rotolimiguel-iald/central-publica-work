import TGLExt.F1Fecho394.BosonicFock
import TGLExt.F1Fecho394.CanonicalOutput
import TGLExt.GenericAntilinearAdjoint
/-! Local implementation of the already registered Gamma(J) target; no external
job is executed, repeated, cancelled or changed. These adapters act on the
existing algebraic tensor products and their existing completions. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open scoped TensorProduct InnerProductSpace
open UniformSpace
namespace F1Fecho.Antilinear
open ChatgptAudit.Continuous050
variable {E F : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F]

theorem tensor_inner (j : E ≃ₛₗᵢ[starRingEnd ℂ] E)
    (k : F ≃ₛₗᵢ[starRingEnd ℂ] F) (x y : E ⊗[ℂ] F) :
    inner ℂ (TensorProduct.congr j.toLinearEquiv k.toLinearEquiv x)
      (TensorProduct.congr j.toLinearEquiv k.toLinearEquiv y) = star (inner ℂ x y) := by
  induction x using TensorProduct.induction_on with
  | zero => simp
  | tmul a b =>
    induction y using TensorProduct.induction_on with
    | zero => simp
    | tmul c d => simp [antiunitary_inner_conj, star_mul, mul_comm]
    | add y z hy hz => simp only [map_add, inner_add_right, star_add, hy, hz]
  | add x z hx hz => simp only [map_add, inner_add_left, star_add, hx, hz]

def tensorAnti (j : E ≃ₛₗᵢ[starRingEnd ℂ] E)
    (k : F ≃ₛₗᵢ[starRingEnd ℂ] F) : E ⊗[ℂ] F ≃ₛₗᵢ[starRingEnd ℂ] E ⊗[ℂ] F where
  toLinearEquiv := TensorProduct.congr j.toLinearEquiv k.toLinearEquiv
  norm_map' x := by
    have h := congrArg Complex.re (tensor_inner j k x x)
    rw [norm_eq_sqrt_re_inner (𝕜 := ℂ), norm_eq_sqrt_re_inner (𝕜 := ℂ)]
    apply congrArg Real.sqrt
    simpa only [Complex.star_def, Complex.conj_re, RCLike.re_to_complex] using h


@[simp] theorem tensorAnti_tmul (j : E ≃ₛₗᵢ[starRingEnd ℂ] E)
    (k : F ≃ₛₗᵢ[starRingEnd ℂ] F) (x : E) (y : F) :
    tensorAnti j k (x ⊗ₜ[ℂ] y) = j x ⊗ₜ[ℂ] k y := by
  exact TensorProduct.congr_tmul _ _ _ _

theorem tensorAnti_involutive (j : E ≃ₛₗᵢ[starRingEnd ℂ] E)
    (k : F ≃ₛₗᵢ[starRingEnd ℂ] F) (hj : Function.Involutive j)
    (hk : Function.Involutive k) : Function.Involutive (tensorAnti j k) := by
  intro x
  induction x using TensorProduct.induction_on with
  | zero => simp
  | tmul x y => simp [hj x, hk y]
  | add x y hx hy => simp only [map_add, hx, hy]

def completionAnti (j : E ≃ₛₗᵢ[starRingEnd ℂ] E) :
    Completion E ≃ₛₗᵢ[starRingEnd ℂ] Completion E :=
  j.toLinearEquiv.extendOfIsometry
    (Completion.toComplₗᵢ (𝕜 := ℂ) (E := E)).toLinearMap
    (Completion.toComplₗᵢ (𝕜 := ℂ) (E := E)).toLinearMap
    Completion.denseRange_coe Completion.denseRange_coe (fun x => by simp)

@[simp] theorem completionAnti_coe (j : E ≃ₛₗᵢ[starRingEnd ℂ] E) (x : E) :
    completionAnti j (x : Completion E) = (j x : Completion E) :=
  LinearEquiv.extendOfIsometry_eq _ _ _ _ _ _ x

theorem completionAnti_involutive (j : E ≃ₛₗᵢ[starRingEnd ℂ] E)
    (hj : Function.Involutive j) : Function.Involutive (completionAnti j) := by
  intro x
  refine Completion.induction_on x (isClosed_eq
    ((completionAnti j).continuous.comp (completionAnti j).continuous) continuous_id) ?_
  intro a
  simp [hj a]

def scalarConj : ℂ ≃ₛₗᵢ[starRingEnd ℂ] ℂ where
  toFun := star
  invFun := star
  left_inv := star_star
  right_inv := star_star
  map_add' := star_add
  map_smul' := by intro c x; simp [smul_eq_mul]
  norm_map' := norm_star

@[simp] theorem scalarConj_one : scalarConj 1 = 1 := by simp [scalarConj]
theorem scalarConj_involutive : Function.Involutive scalarConj := star_star

end F1Fecho.Antilinear

#print axioms F1Fecho.Antilinear.tensor_inner
#print axioms F1Fecho.Antilinear.tensorAnti
#print axioms F1Fecho.Antilinear.tensorAnti_involutive
#print axioms F1Fecho.Antilinear.completionAnti
#print axioms F1Fecho.Antilinear.completionAnti_involutive
#print axioms F1Fecho.Antilinear.scalarConj_involutive
