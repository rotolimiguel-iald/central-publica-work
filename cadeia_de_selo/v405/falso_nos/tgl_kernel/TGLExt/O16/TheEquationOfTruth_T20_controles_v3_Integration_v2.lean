import Lean
import TGLExt.O16.OperatorContourBridge_v2_Integration_v2
import Mathlib.Analysis.Normed.Algebra.MatrixExponential

set_option autoImplicit false
set_option maxHeartbeats 1200000
namespace ORDEM016.EquationOfTruth.NegativeControls
open Matrix Filter Topology
noncomputable section

def diagonalFlow (a b s : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  NormedSpace.exp ((-s) • diagonal ![a,b])

theorem diagonalFlow_eq (a b s : ℝ) :
    diagonalFlow a b s = diagonal ![Real.exp (-(s*a)),Real.exp (-(s*b))] := by
  unfold diagonalFlow
  rw [← Matrix.diagonal_smul, Matrix.exp_diagonal]
  congr 1
  ext i
  fin_cases i <;> simp [Pi.coe_exp, ← Real.exp_eq_exp_ℝ, neg_mul]

theorem diagonalFlow_mulVec (a b s : ℝ) (x : Fin 2 → ℝ) :
    (diagonalFlow a b s).mulVec x =
      ![Real.exp (-(s*a))*x 0, Real.exp (-(s*b))*x 1] := by
  rw [diagonalFlow_eq]
  ext i
  fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_two]

def oblique : Matrix (Fin 2) (Fin 2) ℝ := !![1,-1;0,0]
def splitH : Matrix (Fin 2) (Fin 2) ℝ := diagonal ![0,1]
def fixedP : Matrix (Fin 2) (Fin 2) ℝ := diagonal ![1,0]

theorem C1_1_oblique_algebra :
    oblique*oblique=oblique ∧ splitH*oblique=0 ∧ oblique*splitH ≠ 0 := by
  refine ⟨?_,?_,?_⟩
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [oblique,Matrix.mul_apply,Fin.sum_univ_two]
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [oblique,splitH,Matrix.mul_apply,Fin.sum_univ_two]
  · intro h
    have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    norm_num [oblique,splitH,Matrix.mul_apply,Fin.sum_univ_two] at he

theorem C1_1_oblique_flow_fails (s : ℝ) (hs : 0 < s) :
    oblique*diagonalFlow 0 1 s ≠ oblique := by
  intro he
  have h := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) he
  simp [oblique,diagonalFlow_eq,Matrix.mul_apply,Fin.sum_univ_two] at h
  have he1 : Real.exp (-s)=1 := by linarith
  have hz : -s=0 := Real.exp_injective (by simpa using he1)
  linarith

def nilpotentH : Matrix (Fin 2) (Fin 2) ℝ := !![0,1;0,0]

theorem C1_2_nonsymmetric :
    nilpotentH.transpose ≠ nilpotentH ∧ fixedP.transpose=fixedP ∧ fixedP*nilpotentH ≠ 0 := by
  refine ⟨?_,?_,?_⟩
  · intro h
    have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    norm_num [nilpotentH] at he
  · ext i j
    fin_cases i <;> fin_cases j <;> norm_num [fixedP]
  · intro h
    have he := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) h
    norm_num [fixedP,nilpotentH,Matrix.mul_apply,Fin.sum_univ_two] at he

theorem C1_2_kernel_selected (x : Fin 2 → ℝ) :
    nilpotentH.mulVec x=0 ↔ x 1=0 := by
  simp [nilpotentH,Matrix.mulVec,dotProduct,Fin.sum_univ_two,funext_iff,Fin.forall_fin_two]

theorem negative_unit_flow (s x : ℝ) :
    T (-1 : ℝ →L[ℝ] ℝ) s x = Real.exp s*x := by
  simpa using T_apply_eigen (-1 : ℝ →L[ℝ] ℝ) (-1) x (by simp) s

theorem C1_3a_indefinite_no_limit (x : ℝ) (hx : x ≠ 0) :
    ¬ Tendsto (fun s : ℝ => T (-1 : ℝ →L[ℝ] ℝ) s x) atTop (𝓝 0) := by
  intro h
  have hn := continuous_abs.continuousAt.tendsto.comp h
  have ht : Tendsto (fun s : ℝ => Real.exp s*|x|) atTop atTop :=
    Real.tendsto_exp_atTop.atTop_mul_const (abs_pos.mpr hx)
  have hn0 : Tendsto (fun s : ℝ => Real.exp s*|x|) atTop (𝓝 0) := by
    simpa [Function.comp_def,negative_unit_flow,abs_mul,abs_of_pos (Real.exp_pos _)] using hn
  exact not_tendsto_atTop_of_tendsto_nhds hn0 ht

def productReader (x : Fin 2 → ℝ) : ℝ := x 0*x 1

theorem C1_3b_product_conserved (s : ℝ) (x : Fin 2 → ℝ) :
    productReader ((diagonalFlow 3 (-3) s).mulVec x)=productReader x := by
  rw [diagonalFlow_mulVec]
  simp only [productReader,Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.head_cons]
  have he : Real.exp (-(s*3))*Real.exp (-(s*(-3)))=1 := by
    rw [← Real.exp_add]
    convert Real.exp_zero using 1 <;> ring
  calc
    Real.exp (-(s*3))*x 0*(Real.exp (-(s*(-3)))*x 1) =
      (Real.exp (-(s*3))*Real.exp (-(s*(-3))))*(x 0*x 1) := by ring
    _ = x 0*x 1 := by rw [he,one_mul]

theorem C1_3b_reader_continuous : Continuous productReader := by
  unfold productReader
  fun_prop

theorem C1_3b_reader_not_factor : productReader (![1,1] : Fin 2 → ℝ) ≠ productReader 0 := by
  norm_num [productReader]

def discontinuousReader (x : Fin 2 → ℝ) : ℝ := if x 1=0 then 0 else 1

theorem C1_4_reader_conserved (s : ℝ) (x : Fin 2 → ℝ) :
    discontinuousReader ((diagonalFlow 0 1 s).mulVec x)=discontinuousReader x := by
  rw [diagonalFlow_mulVec]
  simp [discontinuousReader,mul_eq_zero,Real.exp_ne_zero]

theorem C1_4_reader_not_factor :
    discontinuousReader (fixedP.mulVec (![0,1] : Fin 2 → ℝ)) ≠ discontinuousReader ![0,1] := by
  norm_num [discontinuousReader,fixedP,Matrix.mulVec,dotProduct,Fin.sum_univ_two]

theorem C1_5_constant_false_positive :
    ∃ x y : Fin 2 → ℝ, fixedP.mulVec x ≠ fixedP.mulVec y ∧
      (fun _ : Fin 2 → ℝ => (1:ℝ)) x = (fun _ : Fin 2 → ℝ => (1:ℝ)) y := by
  refine ⟨![0,0],![1,0],?_,rfl⟩
  intro h
  have he := congrFun h 0
  norm_num [fixedP,Matrix.mulVec,dotProduct,Fin.sum_univ_two] at he

theorem C1_6_outside_bits : truthValue 2 0 = -3 ∧ truthValue 2 0 ≠ 0 ∧ truthValue 2 0 ≠ 1 := by
  norm_num [truthValue]

theorem C1_7_bad_pruning (s x : ℝ) (hs : 0 < s) (hx : x ≠ 0) :
    reading (0 : ℝ →L[ℝ] ℝ) (T (1 : ℝ →L[ℝ] ℝ) s x) ≠ reading (0 : ℝ →L[ℝ] ℝ) x :=
  equation_criterion_can_fail s x hs hx

theorem C1_8_signed_penalty :
    ((ContinuousLinearMap.adjoint (1 : ℝ →L[ℝ] ℝ)*1 -
       ContinuousLinearMap.adjoint (1 : ℝ →L[ℝ] ℝ)*1) : ℝ →L[ℝ] ℝ).ker = ⊤ ∧
    (1 : ℝ →L[ℝ] ℝ).ker ⊓ (1 : ℝ →L[ℝ] ℝ).ker = ⊥ ∧
    (⊤ : Submodule ℝ ℝ) ≠ ⊥ := by
  have hk : (1 : ℝ →L[ℝ] ℝ).ker = ⊥ := by
    ext x
    change (x=0) ↔ (x=0)
    rfl
  refine ⟨by simp, ?_, top_ne_bot⟩
  rw [hk]
  simp

theorem C1_9_invalid_qubit : (1/2:ℝ)*(1-1/2)-(3/5)^2 < 0 := by norm_num


theorem fixedP_idempotent : fixedP*fixedP=fixedP := by
  ext i j
  fin_cases i <;> fin_cases j <;> norm_num [fixedP,Matrix.mul_apply,Fin.sum_univ_two]

theorem fixedP_selects_kernel (x : Fin 2 → ℝ) : fixedP.mulVec x=x ↔ x 1=0 := by
  simp [fixedP,Matrix.mulVec,dotProduct,Fin.sum_univ_two,funext_iff,Fin.forall_fin_two,eq_comm]

theorem indefinite_kernel_zero (x : Fin 2 → ℝ) :
    (diagonal ![3,-3] : Matrix (Fin 2) (Fin 2) ℝ).mulVec x=0 ↔ x=0 := by
  simp [Matrix.mulVec,dotProduct,Fin.sum_univ_two,funext_iff,Fin.forall_fin_two]

theorem negative_unit_kernel : (-1 : ℝ →L[ℝ] ℝ).ker = ⊥ := by
  ext x
  change (-x=0) ↔ (x=0)
  simp

theorem C1_4_not_continuous : ¬ Continuous discontinuousReader := by
  intro h
  have hv : Tendsto (fun t : ℝ => (![0,Real.exp (-t)] : Fin 2 → ℝ)) atTop (𝓝 0) := by
    apply tendsto_pi_nhds.mpr
    intro i
    fin_cases i
    · simpa using (tendsto_const_nhds : Tendsto (fun _ : ℝ => (0:ℝ)) atTop (𝓝 0))
    · simpa using Real.tendsto_exp_neg_atTop_nhds_zero
  have hh := h.continuousAt.tendsto.comp hv
  have h10 : Tendsto (fun _ : ℝ => (1:ℝ)) atTop (𝓝 0) := by
    simpa [Function.comp_def,discontinuousReader,Real.exp_ne_zero] using hh
  have he : (1:ℝ)=0 := tendsto_nhds_unique tendsto_const_nhds h10
  norm_num at he

#print axioms fixedP_idempotent
#print axioms fixedP_selects_kernel
#print axioms indefinite_kernel_zero
#print axioms negative_unit_kernel
#print axioms C1_4_not_continuous

#print axioms diagonalFlow_eq
#print axioms diagonalFlow_mulVec
#print axioms C1_1_oblique_algebra
#print axioms C1_1_oblique_flow_fails
#print axioms C1_2_nonsymmetric
#print axioms C1_2_kernel_selected
#print axioms negative_unit_flow
#print axioms C1_3a_indefinite_no_limit
#print axioms C1_3b_product_conserved
#print axioms C1_3b_reader_continuous
#print axioms C1_3b_reader_not_factor
#print axioms C1_4_reader_conserved
#print axioms C1_4_reader_not_factor
#print axioms C1_5_constant_false_positive
#print axioms C1_6_outside_bits
#print axioms C1_7_bad_pruning
#print axioms C1_8_signed_penalty
#print axioms C1_9_invalid_qubit
end
end ORDEM016.EquationOfTruth.NegativeControls


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
