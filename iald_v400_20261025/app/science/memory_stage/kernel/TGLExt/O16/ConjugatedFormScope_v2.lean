-- predecessor_sha256: a4393e81d9c7ea83280f63e16894aed692d063563271a97bfe60a5b6b981b0b3
import Lean
import TGLExt.TheGravitonIsTheConjugatedPhase

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open Matrix TGLExt
namespace ORDEM016.D3prime

/-- The finite stationary face selected in the supplied light tower.
It is not asserted to be the center of the full matrix algebra. -/
def finiteCenter : Matrix (Fin 2) (Fin 2) ℂ := (1/4 : ℂ) • (rootPlus*rootMinus)

theorem finite_center_is_projection : finiteCenter=projPlus := by
  unfold finiteCenter
  rw [the_ladder_factors_the_projections.1,smul_smul]
  norm_num

theorem finite_center_commutes_angular (θ : ℝ) :
    angFamily θ*finiteCenter=finiteCenter*angFamily θ := by
  rw [finite_center_is_projection]
  faces

/-- Negative control in the finite angular face, not a wedge boost. -/
theorem light_vector_is_not_fixed : (angFamily (Real.pi/2)).mulVec lightPlus ≠ lightPlus := by
  rw [at_the_right_angle_the_family_is_the_generator,the_generator_reads_the_light_at_half_weight.1]
  intro h
  have h0 := congrArg Complex.im (congrFun h 0)
  norm_num [lightPlus] at h0

def fixedReadout : Matrix (Fin 3) (Fin 3) ℂ := !![0,0,0;1,0,0;0,0,0]
def differentGenerator : Matrix (Fin 3) (Fin 3) ℂ := !![0,0,0;0,1,0;0,0,0]
def phaseFlow (t : ℝ) : Matrix (Fin 3) (Fin 3) ℂ :=
  !![1,0,0;0,1,0;0,0,Complex.exp ((t : ℂ)*Complex.I)]

theorem phase_flow_inverse (t : ℝ) : phaseFlow t*phaseFlow (-t)=1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [phaseFlow,Matrix.mul_apply,Fin.sum_univ_three,←Complex.exp_add,←add_mul]

theorem fixed_for_one_flow (t : ℝ) :
    phaseFlow t*fixedReadout*phaseFlow (-t)=fixedReadout := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [phaseFlow,fixedReadout,Matrix.mul_apply,Fin.sum_univ_three]

theorem fixed_does_not_mean_zero_other_weight :
    differentGenerator*fixedReadout-fixedReadout*differentGenerator=fixedReadout ∧
      fixedReadout ≠ 0 := by
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [differentGenerator,fixedReadout,Matrix.mul_apply,Fin.sum_univ_three]
  · intro h
    have he := congrArg (fun M : Matrix (Fin 3) (Fin 3) ℂ => M 1 0) h
    norm_num [fixedReadout] at he

/-- The additional translation content that actually eliminates a nonzero
translation character; it is not supplied by angular or modular fixedness. -/
theorem translation_fixed_readout {H : Type*} [AddCommGroup H] [Module ℂ H]
    (U A : H →ₗ[ℂ] H) (omega : H)
    (hU : U omega=omega) (hA : U.comp A=A.comp U) : U (A omega)=A omega := by
  have h := LinearMap.congr_fun hA omega
  simpa [hU] using h

theorem nontrivial_character_refused {H : Type*} [AddCommGroup H] [Module ℂ H]
    (U : H →ₗ[ℂ] H) (v : H) (z : ℂ) (hz : z≠1)
    (hfix : U v=v) (hweight : U v=z • v) : v=0 := by
  have h : (z-1) • v=0 := by rw [sub_smul,one_smul,←hweight,hfix,sub_self]
  exact (smul_eq_zero.mp h).resolve_left (sub_ne_zero.mpr hz)

#print axioms TGLExt.the_light_squares_to_the_graviton
#print axioms TGLExt.the_conjugation_crosses_the_squaring
#print axioms TGLExt.the_conjugated_light_squares_to_the_minus_graviton
#print axioms finite_center_is_projection
#print axioms finite_center_commutes_angular
#print axioms light_vector_is_not_fixed
#print axioms phase_flow_inverse
#print axioms fixed_for_one_flow
#print axioms fixed_does_not_mean_zero_other_weight
#print axioms translation_fixed_readout
#print axioms nontrivial_character_refused
end ORDEM016.D3prime


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
