import Lean
import TGLExt.O16.LightRayBoundaryBalance_v3
import Mathlib.Analysis.Fourier.FourierTransform

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter Complex
open scoped FourierTransform

namespace ChatgptAudit.LightRayCore016

theorem fourier_explicit (f : ℝ → ℂ) (p : ℝ) :
    𝓕 f p = ∫ x : ℝ, exp (-2*(Real.pi : ℂ)*I*(p : ℂ)*(x : ℂ)) * f x := by
  rw [Real.fourier_real_eq_integral_exp_smul]
  apply integral_congr_ae
  apply Eventually.of_forall
  intro x
  simp only [smul_eq_mul]
  congr 1
  congr 1
  push_cast
  ring

theorem fourier_star_reverse (f : ℝ → ℂ) (p : ℝ) :
    𝓕 (fun x => star (f x)) p = star (𝓕 f (-p)) := by
  rw [fourier_explicit, fourier_explicit, Complex.star_def, ← integral_conj]
  apply integral_congr_ae
  apply Eventually.of_forall
  intro x
  simp only [map_mul, ← exp_conj, map_neg, map_ofNat, Complex.conj_ofReal, conj_I,
    Complex.star_def, ofReal_neg]
  congr 1
  congr 1
  ring

theorem product_fourier_modular_balance (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) (r p : ℝ) :
    𝓕 (fun x : ℝ => multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ)) p =
      (Real.exp ((2*Real.pi^2)*p) : ℂ) *
        star (𝓕 (fun x : ℝ => multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ)) (-p)) := by
  rw [← fourier_star_reverse, fourier_explicit, fourier_explicit]
  exact spectral_boundary_balance a b ha hb r p

#print axioms fourier_explicit
#print axioms fourier_star_reverse
#print axioms product_fourier_modular_balance

end ChatgptAudit.LightRayCore016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
