import Lean
import TGLExt.SMatrix
import TGLExt.BisognanoWichmann
import Mathlib.Analysis.Complex.Trigonometric

set_option autoImplicit false
noncomputable section
open Matrix NormedSpace
namespace ChatgptAudit.Wick016

def complexBoost (z : ℂ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![Complex.cosh z, Complex.sinh z; Complex.sinh z, Complex.cosh z]

def wickW : Matrix (Fin 2) (Fin 2) ℂ := !![1,0;0,-Complex.I]
def wickWinv : Matrix (Fin 2) (Fin 2) ℂ := !![1,0;0,Complex.I]

theorem complexBoost_real (s : ℝ) :
    complexBoost (s : ℂ) = (TGLExt.boost s).map Complex.ofReal := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [complexBoost,TGLExt.boost,Complex.ofReal_cosh,Complex.ofReal_sinh]

theorem wickW_mul_inverse : wickW * wickWinv = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [wickW,wickWinv,Matrix.mul_apply,Fin.sum_univ_two]

theorem wickW_inverse : wickW⁻¹ = wickWinv :=
  Matrix.inv_eq_right_inv wickW_mul_inverse

/-- Exact matrix continuation; this does not assert a KMS state. -/
theorem wick_boost_rotation (phi : ℝ) :
    wickW⁻¹ * complexBoost ((phi : ℂ)*Complex.I) * wickW = TGLExt.Smat phi := by
  rw [wickW_inverse, TGLExt.Smat_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [wickW,wickWinv,complexBoost,Matrix.mul_apply,Fin.sum_univ_two,
      Complex.cosh_mul_I,Complex.sinh_mul_I,← Complex.ofReal_cos,← Complex.ofReal_sin,
      mul_assoc] <;> ring_nf <;> simp [Complex.I_sq]

theorem wick_boost_exponential (phi : ℝ) :
    wickW⁻¹ * complexBoost (Complex.I*(phi : ℂ)) * wickW =
      exp ((phi : ℂ) • TGLExt.Grot) := by
  rw [mul_comm Complex.I, wick_boost_rotation, TGLExt.exp_smul_Grot]

theorem rotation_two_pi : TGLExt.Smat (2*Real.pi) = 1 := by
  simp [TGLExt.Smat,Real.cos_two_pi,Real.sin_two_pi]

theorem wick_boost_two_pi :
    wickW⁻¹ * complexBoost (Complex.I*((2*Real.pi : ℝ) : ℂ)) * wickW = 1 := by
  rw [mul_comm Complex.I, wick_boost_rotation, rotation_two_pi]

#print axioms complexBoost_real
#print axioms wickW_mul_inverse
#print axioms wickW_inverse
#print axioms wick_boost_rotation
#print axioms wick_boost_exponential
#print axioms rotation_two_pi
#print axioms wick_boost_two_pi
end ChatgptAudit.Wick016


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
