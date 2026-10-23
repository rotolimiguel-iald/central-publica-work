import TGLExt.F1Fecho394.GramTotalExtensionR4
import TGLExt.F1Fecho394.WeylCoefficientsR4
import Mathlib.Analysis.InnerProductSpace.Adjoint
/-! Weyl displacement constructed by Gram extension. A total exponential family
is the explicit input here; the following concrete module will supply it on the
already constructed Fock. No operator, CCR or inverse is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.WeylConstruction
open F1Fecho.WeylCoefficients F1Fecho.GramExtension
variable {H F : Type*}
  [NormedAddCommGroup H] [InnerProductSpace ℂ H]
  [NormedAddCommGroup F] [InnerProductSpace ℂ F] [CompleteSpace F]
variable (v : H → F)
  (hkernel : ∀ g h, inner ℂ (v g) (v h) = Complex.exp (inner ℂ g h))
  (htotal : Total (𝕜 := ℂ) v)

def displaced (f g : H) : F := amplitude f g • v (g+f)

include hkernel in
theorem displaced_gram (f : H) : GramEqual (𝕜 := ℂ) v (displaced v f) := by
  intro g h
  simp only [displaced, inner_smul_left, inner_smul_right, starRingEnd_apply, hkernel]
  simpa only [mul_assoc, mul_left_comm, mul_comm] using gram_identity f g h

include htotal in
theorem displaced_total (f : H) : Total (𝕜 := ℂ) (displaced v f) := by
  apply total_weighted_reindex v (amplitude f) (fun g => g+f)
    (amplitude_ne_zero f) _ htotal
  intro g
  exact ⟨g-f,sub_add_cancel g f⟩

def D (f : H) : F ≃ₗᵢ[ℂ] F :=
  equivalence v (displaced v f) (displaced_gram v hkernel f) htotal
    (displaced_total v htotal f)

theorem D_apply (f g : H) : D v hkernel htotal f (v g) = amplitude f g • v (g+f) :=
  equivalence_apply v _ _ _ _ g

def W (f : H) : F →L[ℂ] F := (D v hkernel htotal f).toContinuousLinearEquiv.toContinuousLinearMap

theorem W_apply (f g : H) : W v hkernel htotal f (v g) = amplitude f g • v (g+f) :=
  D_apply v hkernel htotal f g

include htotal in
theorem clm_ext_total {A B : F →L[ℂ] F} (h : ∀ g, A (v g) = B (v g)) : A = B := by
  apply ContinuousLinearMap.ext
  intro x
  refine (dense_linearCombination v htotal).induction ?_
    (isClosed_eq A.continuous B.continuous) x
  rintro _ ⟨a,rfl⟩
  classical
  simp only [Finsupp.linearCombination_apply, Finsupp.sum, map_sum, map_smul, h]

theorem W_zero : W v hkernel htotal 0 = 1 := by
  apply clm_ext_total v htotal
  intro g
  simp [W_apply, amplitude_zero_left]

theorem W_add (f g : H) : W v hkernel htotal f * W v hkernel htotal g =
    phase f g • W v hkernel htotal (f+g) := by
  apply clm_ext_total v htotal
  intro h
  simp only [ContinuousLinearMap.mul_apply, W_apply, map_smul,
    ContinuousLinearMap.smul_apply, smul_smul]
  rw [composition_identity]
  congr 2
  abel

theorem W_neg_mul (f : H) : W v hkernel htotal (-f) * W v hkernel htotal f = 1 := by
  rw [W_add]
  have hh : (inner ℂ f f).im = 0 := inner_self_im (𝕜 := ℂ) f
  simp only [phase, inner_neg_left, Complex.neg_im, hh, neg_zero,
    Complex.ofReal_zero, mul_zero, Complex.exp_zero, one_smul, neg_add_cancel, W_zero]

theorem D_neg (f : H) : D v hkernel htotal (-f) = (D v hkernel htotal f).symm := by
  apply LinearIsometryEquiv.ext
  intro x
  have hx := congrArg (fun T : F →L[ℂ] F => T ((D v hkernel htotal f).symm x))
    (W_neg_mul v hkernel htotal f)
  change D v hkernel htotal (-f) (D v hkernel htotal f ((D v hkernel htotal f).symm x)) = _ at hx
  simpa only [LinearIsometryEquiv.apply_symm_apply, ContinuousLinearMap.one_apply] using hx

theorem W_star (f : H) : star (W v hkernel htotal f) = W v hkernel htotal (-f) := by
  unfold W
  rw [LinearIsometryEquiv.star_eq_symm, D_neg]

theorem W_local (f g : H) (h : (inner ℂ f g).im = 0) :
    Commute (W v hkernel htotal f) (W v hkernel htotal g) := by
  have h' : (inner ℂ g f).im = 0 := by
    have hc : inner ℂ g f = star (inner ℂ f g) := (inner_conj_symm g f).symm
    rw [hc, Complex.star_def, Complex.conj_im, h, neg_zero]
  show W v hkernel htotal f * W v hkernel htotal g = W v hkernel htotal g * W v hkernel htotal f
  rw [W_add, W_add, phase_orthogonal f g h, phase_orthogonal g f h', one_smul, one_smul, add_comm f g]

end F1Fecho.WeylConstruction

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.WeylConstruction).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
