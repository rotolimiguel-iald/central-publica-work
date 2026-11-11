import TGLExt.F1Fecho394.BosonicSectors
import Mathlib.Analysis.Normed.Operator.Bilinear
import Mathlib.Topology.UniformSpace.UniformApproximation
import Mathlib.Topology.MetricSpace.UniformConvergence
import Mathlib.Topology.Sequences
/-!
Strong continuity of concrete bosonic sectors, derived from strong continuity
on H1. Tensor bilinearity proves continuity on diagonal powers; their linear
span and closure are handled by a closed subspace of continuous orbits.
Uniform convergence in that last step follows from the isometry estimate,
without assuming the desired sector continuity as an extra field.
-/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 100000
noncomputable section
open UniformSpace Filter
open scoped TensorProduct Topology
namespace F1Rede.BosonicSectorContinuity
open TGLExt.ImportedSQ F1Rede.BosonicSectors

section OrbitClosure
variable {A E : Type*} [TopologicalSpace A] [NormedAddCommGroup E] [NormedSpace ℂ E]

def continuousOrbitSpace (u : A → E ≃ₗᵢ[ℂ] E) : Submodule ℂ E where
  carrier := {x | Continuous (fun t => u t x)}
  zero_mem' := by
    change Continuous (fun t => u t 0)
    simpa only [map_zero] using (continuous_const : Continuous (fun _ : A => (0 : E)))
  add_mem' := by
    intro x y hx hy
    change Continuous (fun t => u t (x+y))
    simp only [map_add]
    exact continuous_add.comp (hx.prodMk hy)
  smul_mem' := by
    intro c x hx
    change Continuous (fun t => u t (c • x))
    simpa only [map_smul] using hx.const_smul c

theorem continuousOrbitSpace_closed (u : A → E ≃ₗᵢ[ℂ] E) :
    IsClosed (continuousOrbitSpace u : Set E) := by
  refine IsSeqClosed.isClosed fun x y hx hxy => ?_
  have hunif : TendstoUniformly (fun n t => u t (x n)) (fun t => u t y) atTop := by
    apply Metric.tendstoUniformly_iff.mpr
    intro ε hε
    filter_upwards [Metric.tendsto_nhds.mp hxy ε hε] with n hn
    intro t
    simpa only [(u t).isometry.dist_eq, dist_comm] using hn
  exact hunif.continuous (Filter.Eventually.of_forall hx).frequently
end OrbitClosure

def tensorBilinear (n : ℕ) : H1 →L[ℂ] Algebraic n →L[ℂ] (H1 ⊗[ℂ] Algebraic n) :=
  (TensorProduct.mk ℂ H1 (Algebraic n)).mkContinuous₂ 1 (by
    intro x y
    simp only [TensorProduct.mk_apply, TensorProduct.norm_tmul, one_mul, le_refl])

variable {A : Type*} [TopologicalSpace A]

theorem continuous_pureAlgebraic (f : A → H1) (hf : Continuous f) (n : ℕ) :
    Continuous (fun t => pureAlgebraic (f t) n) := by
  induction n with
  | zero => exact continuous_const
  | succ n ih =>
    change Continuous (fun t => tensorBilinear n (f t) (pureAlgebraic (f t) n))
    exact ((tensorBilinear n).continuous.comp hf).clm_apply ih

theorem continuous_pureCompleted (f : A → H1) (hf : Continuous f) (n : ℕ) :
    Continuous (fun t => pureCompleted n (f t)) :=
  (Completion.toComplₗᵢ (𝕜 := ℂ) (E := Algebraic n)).continuous.comp (continuous_pureAlgebraic f hf n)

theorem tensorGamma_strong_on_sector (u : A → H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀ x : H1, Continuous (fun t => u t x)) (n : ℕ) (x : Sector n) :
    Continuous (fun t => tensorGamma (u t) n (x : TensorHilbert n)) := by
  let O := continuousOrbitSpace (fun t => tensorGamma (u t) n)
  have hspan : algebraicSymmetricSpan n ≤ O := by
    apply Submodule.span_le.mpr
    rintro _ ⟨y, rfl⟩
    change Continuous (fun t => tensorGamma (u t) n (pureCompleted n y))
    simp only [tensorGamma_pure]
    exact continuous_pureCompleted (fun t => u t y) (hu y) n
  exact (algebraicSymmetricSpan n).topologicalClosure_minimal hspan
    (continuousOrbitSpace_closed (fun t => tensorGamma (u t) n)) x.property

/-- Applies to arbitrary parameter spaces, including real time and R^4
translations; the only continuity input lives on the original H1. -/
theorem gammaSector_strong (u : A → H1 ≃ₗᵢ[ℂ] H1)
    (hu : ∀ x : H1, Continuous (fun t => u t x)) (n : ℕ) (x : Sector n) :
    Continuous (fun t => gammaSector (u t) n x) :=
  (tensorGamma_strong_on_sector u hu n x).subtype_mk _

end F1Rede.BosonicSectorContinuity
#print axioms F1Rede.BosonicSectorContinuity.continuousOrbitSpace_closed
#print axioms F1Rede.BosonicSectorContinuity.gammaSector_strong
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
    | _ => pure ()
