import TGLExt.F1Fecho394.CanonicalFockRegularCoreR2
import TGLExt.V350DualWeightForm
import TGLExt.V350DualQuadraticLaws
import TGLExt.V350DualFormFaithfulness
import TGLExt.V350DualFormNormality
/-!
The actual dual integral on the positive cone of the newly constructed regular
core of R(KWR), on L2(R; Fock), evaluated at the SAME concrete Fock vacuum.
This is a constructed nonzero scalar dual weight, not the exp(-s)-scaling trace.
Its additivity, nonnegative homogeneity, monotonicity, dual invariance and
preservation of positive monotone strong limits reuse the generic integral
lemmas. The unit has infinite weight, so the construction is nonzero.
No faithfulness, semifiniteness, tracial law, inverse-generator perturbation,
full modular implementation or Fock-to-tower equivalence is asserted here.
-/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
open Filter Topology
open scoped ENNReal NNReal
namespace F1Fecho.CanonicalFockWeight
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular
open F1Fecho.CanonicalFockRegular

def PositiveInput :=
  {A : RegularHilbert F →L[ℂ] RegularHilbert F // A ∈ core ∧ 0 ≤ A}

def zero : PositiveInput := ⟨0,core.zero_mem,le_rfl⟩

def one : PositiveInput := ⟨1,core.one_mem,zero_le_one⟩

def add (A B : PositiveInput) : PositiveInput :=
  ⟨A.val+B.val,core.add_mem A.property.1 B.property.1,
    add_nonneg A.property.2 B.property.2⟩

def scale (r : ℝ≥0) (A : PositiveInput) : PositiveInput :=
  ⟨((r : ℝ) : ℂ) • A.val, by
    change ((r : ℝ) : ℂ) • A.val ∈ core
    exact core.toStarSubalgebra.smul_mem A.property.1 _, by
    change 0 ≤ ((r : ℝ) : ℂ) • A.val
    apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
    exact ((ContinuousLinearMap.nonneg_iff_isPositive _).mp A.property.2).smul_of_nonneg
      (by exact_mod_cast r.property)⟩

def positiveDual (s : ℝ) (A : PositiveInput) : PositiveInput :=
  ⟨(dualAction s ⟨A.val,A.property.1⟩).val,
    (dualAction s ⟨A.val,A.property.1⟩).property,
    dualAmbient_nonneg s A.val A.property.2⟩

def regularFockVacuum : RegularHilbert F := testVector vacuum

theorem regularFockVacuum_norm : ‖regularFockVacuum‖ = 1 := by
  rw [regularFockVacuum,testVector_norm,vacuum_norm]

theorem regularFockVacuum_ne_zero : regularFockVacuum ≠ 0 := by
  intro h
  have hn := regularFockVacuum_norm
  rw [h,norm_zero] at hn
  norm_num at hn

def weight (A : PositiveInput) : ℝ≥0∞ :=
  dualQuadraticIntegral A.val regularFockVacuum

theorem weight_zero : weight zero = 0 := dualQuadraticIntegral_zero regularFockVacuum

theorem weight_add (A B : PositiveInput) : weight (add A B) = weight A + weight B :=
  dualQuadraticIntegral_add A.val B.val A.property.2 B.property.2 regularFockVacuum

theorem weight_scale (r : ℝ≥0) (A : PositiveInput) :
    weight (scale r A) = (r : ℝ≥0∞) * weight A := by
  have h := dualQuadraticIntegral_smul_operator (r : ℝ) r.property A.val regularFockVacuum
  change dualQuadraticIntegral (((r : ℝ) : ℂ) • A.val) regularFockVacuum =
    ENNReal.ofReal (r : ℝ) * dualQuadraticIntegral A.val regularFockVacuum at h
  change dualQuadraticIntegral (((r : ℝ) : ℂ) • A.val) regularFockVacuum = _
  simpa only [weight,ENNReal.ofReal_coe_nnreal] using h

theorem weight_mono (A B : PositiveInput) (h : A.val ≤ B.val) : weight A ≤ weight B :=
  dualQuadraticIntegral_mono A.val B.val h regularFockVacuum

theorem weight_dual_invariant (s : ℝ) (A : PositiveInput) :
    weight (positiveDual s A) = weight A :=
  dualQuadraticIntegral_dual_invariant s A.val regularFockVacuum

theorem weight_one : weight one = ⊤ :=
  dualQuadraticIntegral_one regularFockVacuum regularFockVacuum_ne_zero

theorem weight_nonzero : weight ≠ fun _ => 0 := by
  intro h
  have he := congrFun h one
  rw [weight_one] at he
  exact ENNReal.top_ne_zero he

theorem positive_cone_nontrivial : one ≠ zero := by
  intro h
  have he := congrArg weight h
  rw [weight_one,weight_zero] at he
  exact ENNReal.top_ne_zero he

theorem weight_monotone_strong_limit
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → PositiveInput) (S : PositiveInput)
    (hmono : Monotone (fun i => (A i).val))
    (hlim : ∀ v, Tendsto (fun i => (A i).val v) atTop (𝓝 (S.val v))) :
    weight S = ⨆ i, weight (A i) :=
  dualQuadraticIntegral_of_monotone_strong_limit (fun i => (A i).val) S.val
    (fun i => (A i).property.2) hmono hlim regularFockVacuum

end F1Fecho.CanonicalFockWeight
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockWeight).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
