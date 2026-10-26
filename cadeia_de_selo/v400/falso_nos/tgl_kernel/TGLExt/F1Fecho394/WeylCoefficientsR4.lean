import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic
/-!
Displacement convention: D(f)e(g)=a(f,g)e(g+f), where
a(f,g)=exp(-inner(f,f)/2-inner(f,g)). The exponential-vector normalization
is inner(e(g),e(h))=exp(inner(g,h)). This is not an operator construction;
it proves the scalar Gram and cocycle identities consumed by that construction.
-/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.WeylCoefficients
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

def amplitude (f g : H) : ℂ :=
  Complex.exp (-inner ℂ f f / 2 - inner ℂ f g)

def phase (f g : H) : ℂ :=
  Complex.exp (-Complex.I * (inner ℂ f g).im)

theorem amplitude_ne_zero (f g : H) : amplitude f g ≠ 0 := Complex.exp_ne_zero _

theorem amplitude_zero_left (g : H) : amplitude (0:H) g = 1 := by
  simp [amplitude]

theorem amplitude_norm_form (f g : H) :
    amplitude f g = Complex.exp (-((‖f‖ : ℂ)^2)/2 - inner ℂ f g) := by
  simp [amplitude, inner_self_eq_norm_sq_to_K]

theorem gram_identity (f g h : H) :
    star (amplitude f g) * amplitude f h * Complex.exp (inner ℂ (g+f) (h+f)) =
      Complex.exp (inner ℂ g h) := by
  simp only [amplitude, Complex.star_def, ← Complex.exp_conj, map_sub, map_div₀,
    map_neg, map_ofNat, inner_conj_symm, ← Complex.exp_add,
    inner_add_left, inner_add_right]
  congr 1
  ring

theorem imag_difference (z : ℂ) :
    -Complex.I * z.im = (star z - z)/2 := by
  apply Complex.ext <;> simp [Complex.ext_iff] <;> ring

theorem composition_identity (f g h : H) :
    amplitude g h * amplitude f (h+g) = phase f g * amplitude (f+g) h := by
  simp only [amplitude, phase, ← Complex.exp_add, inner_add_left, inner_add_right]
  rw [imag_difference, Complex.star_def, inner_conj_symm]
  congr 1
  ring

theorem phase_self_neg (f : H) : phase f (-f) = 1 := by
  have hh : (inner ℂ f f).im = 0 := inner_self_im (𝕜 := ℂ) f
  simp only [phase, inner_neg_right, Complex.neg_im, hh, neg_zero, Complex.ofReal_zero, mul_zero, Complex.exp_zero]

theorem inverse_identity (f g : H) :
    amplitude f g * amplitude (-f) (g+f) = 1 := by
  rw [composition_identity]
  have hh : (inner ℂ f f).im = 0 := inner_self_im (𝕜 := ℂ) f
  simp only [phase, inner_neg_left, Complex.neg_im, hh, neg_zero, Complex.ofReal_zero, mul_zero, Complex.exp_zero, neg_add_cancel, amplitude_zero_left, mul_one]

theorem amplitude_isometry (u : H ≃ₗᵢ[ℂ] H) (f g : H) :
    amplitude (u f) (u g) = amplitude f g := by
  simp only [amplitude, u.inner_map_map]

theorem phase_orthogonal (f g : H) (h : (inner ℂ f g).im = 0) :
    phase f g = 1 := by simp [phase,h]

end F1Fecho.WeylCoefficients

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.WeylCoefficients).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
