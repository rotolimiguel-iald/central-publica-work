import TGLExt.F1Fecho394.RegularCoreFixedR3
import TGLExt.F1Fecho394.RegularCoreResolventR2
import TGLExt.F1Fecho394.CanonicalFockDualWeightR3
import TGLExt.F1Fecho394.WedgeCyclicR3
/-! Faithfulness of the actual scalar dual weight on the SAME Fock regular
core. The proof reuses the fixed-core identification and canonical variational
resolvent, then applies the already derived separating Fock vacuum. No trace,
semifiniteness or modular-group identification is assumed or concluded. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockFaithfulWeight
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open scoped Topology ENNReal

theorem boost_normalizes (t : ℝ) (A : F →L[ℂ] F) :
    F1Fecho.RegularCovariantCore.automorphism fockFlow t A ∈ M ↔ A ∈ M := by
  rw [automorphism_is_concrete_boost]
  exact (F1Fecho.CanonicalWedgeFlow.boostAd_preserves t A).symm

theorem fixed_core_is_base (A : RegularHilbert F →L[ℂ] RegularHilbert F) :
    (A ∈ core ∧ ∀ s : ℝ, dualAmbient s A = A) ↔ ∃ C ∈ M, A = fibre C :=
  F1Fecho.RegularCoreFixed.dualFixed_eq_amplified_base fockFlow M boost_normalizes A

theorem fixed_core_vacuum_separating
    (A : RegularHilbert F →L[ℂ] RegularHilbert F)
    (hA : A ∈ core) (hfix : ∀ s : ℝ, dualAmbient s A = A)
    (hz : A regularFockVacuum = 0) : A = 0 := by
  obtain ⟨C,hC,he⟩ := (fixed_core_is_base A).mp ⟨hA,hfix⟩
  subst A
  change fibre C (testVector vacuum) = 0 at hz
  rw [fibre_testVector] at hz
  have hc0 : C vacuum = 0 := by
    apply norm_eq_zero.mp
    rw [← testVector_norm,hz,norm_zero]
  have hc : C = 0 := F1Fecho.WedgeCyclic.canonical_wedge_separating C hC hc0
  rw [hc]
  exact map_zero fibreRepresentation

theorem weight_faithful (A : PositiveInput) : weight A = 0 ↔ A.val = 0 := by
  constructor
  · intro hv
    obtain ⟨R,hmR,hR,hone,hlim,hfix⟩ :=
      F1Fecho.RegularCoreResolvent.exists_dualResolvent_fixed fockFlow M A.val A.property.1 A.property.2
    have hz : (R-1) regularFockVacuum = 0 := by
      change R regularFockVacuum - regularFockVacuum = 0
      exact sub_eq_zero.mpr (dualResolvent_fixes_zero_form_vector A.val R A.property.2 hlim _ hv)
    have hfixsub : ∀ s : ℝ, dualAmbient s (R-1) = R-1 := by
      intro s
      rw [map_sub,hfix,map_one]
    have hRone : R = 1 := sub_eq_zero.mp
      (fixed_core_vacuum_separating (R-1) (core.sub_mem hmR core.one_mem) hfixsub hz)
    apply (dualQuadraticIntegral_faithful A.val A.property.2).mp
    intro v
    have hfinite := dualResolvent_limit_range_finite A.val R A.property.2 hlim v
    have hid := dualResolvent_limit_energy_identity A.val R A.property.2 hlim v
    rw [hRone] at hfinite hid
    change dualQuadraticIntegral A.val v < ⊤ at hfinite
    change (dualQuadraticIntegral A.val v).toReal = (inner ℂ v (v-v)).re at hid
    simp only [sub_self,inner_zero_right,Complex.zero_re] at hid
    calc
      dualQuadraticIntegral A.val v = ENNReal.ofReal (dualQuadraticIntegral A.val v).toReal :=
        (ENNReal.ofReal_toReal (ne_of_lt hfinite)).symm
      _ = 0 := by rw [hid,ENNReal.ofReal_zero]
  · intro h
    change dualQuadraticIntegral A.val regularFockVacuum = 0
    rw [h]
    exact dualQuadraticIntegral_zero regularFockVacuum

end F1Fecho.CanonicalFockFaithfulWeight
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockFaithfulWeight).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
