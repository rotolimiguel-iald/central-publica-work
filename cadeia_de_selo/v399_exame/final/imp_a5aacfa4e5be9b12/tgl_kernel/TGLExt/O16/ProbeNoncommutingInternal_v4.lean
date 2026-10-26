import Lean
import TGLExt.O16.ContratoQG_v31_Minimal

set_option autoImplicit false
set_option maxHeartbeats 2000000
namespace ChatgptAudit.NoncommutingInternal
open Matrix Complex TGL.SpecificAQFT TGL.ModularRealization
open TGLExt.ContratoQGv31
noncomputable section

/-! Finite CONTROL, not an AQFT witness. Both matrix groups fix e0.
Their actions do not commute. Translations only read a0 and therefore
cannot satisfy the actual faithful-translation field of ContratoH2.
No identification of D with the genuine modular flow is assumed. -/
abbrev V := Fin 3 → ℂ
def vacuum : V := ![1,0,0]
def probe : V := ![0,1,0]
def phase (t : ℝ) : ℂ := Complex.exp ((t : ℂ) * Complex.I)
def U (a : Fin 4 → ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![1,0,0; 0,phase (a 0),0; 0,0,1]
def D (t : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![1,0,0; 0,Real.cos t,-Real.sin t; 0,Real.sin t,Real.cos t]
def spatialShift : Fin 4 → ℝ := ![0,1,0,0]
def halfTurn : Fin 4 → ℝ := ![Real.pi,0,0,0]

theorem U_zero : U 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [U,phase]
theorem U_add (a b : Fin 4 → ℝ) : U (a+b) = U a * U b := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [U,phase,Matrix.mul_apply,Fin.sum_univ_three,add_mul,Complex.exp_add]
theorem D_zero : D 0 = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [D]
theorem D_add (s t : ℝ) : D (s+t) = D s * D t := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [D,Matrix.mul_apply,Fin.sum_univ_three,Real.cos_add,Real.sin_add] <;> ring
theorem U_fixes_vacuum (a : Fin 4 → ℝ) : (U a).mulVec vacuum = vacuum := by
  ext i
  fin_cases i <;> simp [U,vacuum,Matrix.mulVec,dotProduct,Fin.sum_univ_three]
theorem D_fixes_vacuum (t : ℝ) : (D t).mulVec vacuum = vacuum := by
  ext i
  fin_cases i <;> simp [D,vacuum,Matrix.mulVec,dotProduct,Fin.sum_univ_three]

theorem noncommuting_on_probe :
    (D (Real.pi/2)).mulVec ((U halfTurn).mulVec probe) ≠
    (U halfTurn).mulVec ((D (Real.pi/2)).mulVec probe) := by
  intro h
  have he := congrFun h 2
  norm_num [D,U,halfTurn,probe,phase,Matrix.mulVec,dotProduct,Fin.sum_univ_three,
    Complex.exp_pi_mul_I,Matrix.cons_val_two,Matrix.vecHead,Matrix.vecTail] at he

theorem spatialShift_nonzero : spatialShift ≠ 0 := by
  intro h
  have he := congrFun h 1
  norm_num [spatialShift] at he
theorem U_spatialShift : U spatialShift = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [U,phase,spatialShift]

/-- Conditional comparison to the ACTUAL contract, not an invented finite witness. -/
theorem contract_rejects_this_translation_action
    {W : TGLSpecificAQFTWitness} {R : TGLModularRealization W}
    {N : KillingNormalization} (C : ContratoH2 W R N)
    (read : W.H → V) (faithful_read : Function.Injective read)
    (reads_action : ∀ a ψ, read (W.U a ψ) = (U a).mulVec (read ψ)) : False := by
  have hu : W.U spatialShift = 1 := by
    ext ψ
    apply faithful_read
    simpa only [U_spatialShift,Matrix.one_mulVec,ContinuousLinearMap.one_apply] using reads_action spatialShift ψ
  exact spatialShift_nonzero (C.translations_faithful spatialShift hu)

theorem U_adjoint (a : Fin 4 → ℝ) : (U a).conjTranspose = U (-a) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [U,phase,Matrix.conjTranspose_apply, ← Complex.exp_conj]
theorem D_adjoint (t : ℝ) : (D t).conjTranspose = D (-t) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [D,Matrix.conjTranspose_apply, ← Complex.cos_conj, ← Complex.sin_conj]
theorem U_unitary (a : Fin 4 → ℝ) : (U a).conjTranspose * U a = 1 := by
  rw [U_adjoint, ← U_add,neg_add_cancel,U_zero]
theorem D_unitary (t : ℝ) : (D t).conjTranspose * D t = 1 := by
  rw [D_adjoint, ← D_add,neg_add_cancel,D_zero]
theorem U_continuous : Continuous U := by
  unfold U phase
  fun_prop
theorem D_continuous : Continuous D := by
  unfold D
  fun_prop

#print axioms U_adjoint
#print axioms D_adjoint
#print axioms U_unitary
#print axioms D_unitary
#print axioms U_continuous
#print axioms D_continuous
#print axioms U_zero
#print axioms U_add
#print axioms D_zero
#print axioms D_add
#print axioms U_fixes_vacuum
#print axioms D_fixes_vacuum
#print axioms noncommuting_on_probe
#print axioms spatialShift_nonzero
#print axioms U_spatialShift
#print axioms contract_rejects_this_translation_action
end
end ChatgptAudit.NoncommutingInternal


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
