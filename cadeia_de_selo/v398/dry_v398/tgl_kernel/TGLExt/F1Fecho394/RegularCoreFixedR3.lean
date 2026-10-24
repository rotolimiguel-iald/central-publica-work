import TGLExt.F1Fecho394.RegularCovariantCoreR3
import TGLExt.V350TwistedCommutantField
import TGLExt.V350ConstantFibreIdentification
/-! Generic fixed-core identification using existing V350 analytic lemmas.
The named normalizer condition is about the supplied actual unitary flow and
base algebra, not a trace or modular-state identification. Its Fock instance
is supplied separately by the already constructed wedge-invariant boost. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularCoreFixed
open MeasureTheory Filter TGLExt ChatgptAudit TGLV350 TGLV350.Regular
open F1Fecho.RegularCovariantCore
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (B : UnitaryFlow H) (M : VonNeumannAlgebra H)
variable (hM : ∀ (t : ℝ) (A : H →L[ℂ] H), automorphism B t A ∈ M ↔ A ∈ M)

theorem automorphism_symm (t : ℝ) : (automorphism B t).symm = automorphism B (-t) := by
  unfold automorphism
  rw [boostIso_neg]
  rfl

theorem boostCLM_apply (t : ℝ) (v : H) : boostCLM B t v = boostIso B t v := rfl

include hM in
theorem modularConjugation_preserves_commutant (t : ℝ)
    (D : H →L[ℂ] H) (hD : D ∈ (M).commutant) :
    automorphism B t D ∈ (M).commutant := by
  rw [VonNeumannAlgebra.mem_commutant_iff] at hD ⊢
  intro A hA
  have hpre : (automorphism B t).symm A ∈ M := by
    rw [automorphism_symm]
    exact (hM (-t) A).mpr hA
  have he := congrArg (automorphism B t) (hD _ hpre)
  simpa only [map_mul, StarAlgEquiv.apply_symm_apply] using he

theorem modularFlow_jointly_continuous :
    Continuous (fun p : H × ℝ => boostIso B p.2 p.1) :=
  continuous_prod_of_continuous_lipschitzWith _ 1
    (fun v => boostIso_strong B v)
    (fun t => (boostIso B t).lipschitz)

theorem modularConjugation_strongly_continuous (D : H →L[ℂ] H) (v : H) :
    Continuous (fun x : ℝ => automorphism B x D v) := by
  have hn : Continuous (fun x : ℝ => boostIso B (-x) v) :=
    (boostIso_strong B v).comp continuous_neg
  have hd : Continuous (fun x : ℝ => D (boostIso B (-x) v)) := D.continuous.comp hn
  have hp : Continuous (fun x : ℝ => (D (boostIso B (-x) v), x)) :=
    hd.prodMk continuous_id
  have hc := (modularFlow_jointly_continuous B).comp hp
  simp only [Function.comp_def] at hc
  simpa only [boostAd_sandwich B, boostCLM_star B,
    mul_apply_eq_comp, boostCLM_apply] using hc

/-- The continuous field x ↦ Δ^(ix) D Δ^(-ix), using the same tower flow.
Its bounded lift will lie in the regular commutant when D lies in M'. -/
def twistedCommutantField (D : H →L[ℂ] H) :
    StrongIntegral.Family (H := H) where
  op := fun x => automorphism B x D
  continuous_apply := modularConjugation_strongly_continuous B D
  bound := ‖D‖
  bound_nonneg := norm_nonneg D
  norm_bound := fun x => le_of_eq (StarAlgEquiv.norm_map (automorphism B x) D)

theorem twistedCommutantField_zero (D : H →L[ℂ] H) : (twistedCommutantField B D).op 0 = D := by
  change automorphism B 0 D = D
  rw [boostAd_sandwich B, boostCLM_zero B]
  simp only [star_one, one_mul, mul_one]

theorem twistedCommutantField_intertwines (D : H →L[ℂ] H) (x t : ℝ) :
    (twistedCommutantField B D).op x * boostCLM B t =
      boostCLM B t * (twistedCommutantField B D).op (x-t) := by
  change automorphism B x D * boostCLM B t =
    boostCLM B t * automorphism B (x-t) D
  rw [boostAd_sandwich B, boostAd_sandwich B,
    boostCLM_star B, boostCLM_star B]
  calc
    _ = (boostCLM B x * D) * (boostCLM B (-x) * boostCLM B t) := by
      simp only [mul_assoc]
    _ = (boostCLM B x * D) * boostCLM B (t-x) := by
      rw [boostCLM_mul B, neg_add_eq_sub]
    _ = ((boostCLM B t * boostCLM B (x-t)) * D) * boostCLM B (-(x-t)) := by
      rw [boostCLM_mul B]
      congr 2 <;> congr 1 <;> ring
    _ = _ := by simp only [mul_assoc]

theorem operatorFieldLift_commutes_regular_of_intertwining (F : StrongIntegral.Family (H := H))
    (hF : ∀ x t : ℝ, F.op x * boostCLM B t = boostCLM B t * F.op (x-t))
    (t : ℝ) :
    operatorFieldLift F * regularUnitary B t = regularUnitary B t * operatorFieldLift F := by
  ext1 f
  apply Lp.ext
  filter_upwards [operatorFieldLift_ae F (regularUnitary B t f),
    fibre_ae (boostCLM B t) (shift t f), shift_ae t f,
    fibre_ae (boostCLM B t) (shift t (operatorFieldLift F f)),
    shift_ae t (operatorFieldLift F f),
    (measurePreserving_sub_right volume t).quasiMeasurePreserving.ae (operatorFieldLift_ae F f)]
    with x h1 h2 h3 h4 h5 h6
  change operatorFieldLift F (regularUnitary B t f) x = regularUnitary B t (operatorFieldLift F f) x
  rw [h1]
  change F.op x (fibre (boostCLM B t) (shift t f) x) =
    fibre (boostCLM B t) (shift t (operatorFieldLift F f)) x
  rw [h2,h3,h4,h5,h6]
  exact congrArg (fun T : H →L[ℂ] H => T (f (x-t))) (hF x t)

theorem mem_regularCommutant_of_generators (T : RegularHilbert (H) →L[ℂ] RegularHilbert (H))
    (hM : ∀ A ∈ M, T * fibre A = fibre A * T)
    (hU : ∀ t : ℝ, T * regularUnitary B t = regularUnitary B t * T) :
    T ∈ (core B M).commutant := by
  have hN : core B M ≤ starCommutantAlgebra {T} := by
    apply core_minimal B M
    · intro A hA
      change fibre A ∈ StarSubalgebra.centralizer ℂ {T}
      rw [StarSubalgebra.mem_centralizer_iff]
      intro B hB
      have he : B = T := Set.mem_singleton_iff.mp hB
      subst B
      refine ⟨hM A hA, ?_⟩
      have hs := congrArg star (hM (star A) (star_mem hA))
      rw [fibre_star] at hs
      simpa only [star_mul, star_star] using hs.symm
    · intro t
      change regularUnitary B t ∈ StarSubalgebra.centralizer ℂ {T}
      rw [StarSubalgebra.mem_centralizer_iff]
      intro B hB
      have he : B = T := Set.mem_singleton_iff.mp hB
      subst B
      refine ⟨hU t, ?_⟩
      have hs := congrArg star (hU (-t))
      simpa only [star_mul, regular_star B, neg_neg] using hs.symm
  rw [VonNeumannAlgebra.mem_commutant_iff]
  intro A hA
  have hm := hN hA
  change A ∈ StarSubalgebra.centralizer ℂ {T} at hm
  rw [StarSubalgebra.mem_centralizer_iff] at hm
  exact (hm T (Set.mem_singleton T)).1.symm

include hM in
theorem twistedCommutantLift_mem (D : H →L[ℂ] H)
    (hD : D ∈ (M).commutant) :
    operatorFieldLift (twistedCommutantField B D) ∈ (core B M).commutant := by
  apply mem_regularCommutant_of_generators B M
  · intro A hA
    apply operatorFieldLift_commutes_fibre
    intro x
    exact ((VonNeumannAlgebra.mem_commutant_iff.mp
      (modularConjugation_preserves_commutant B M hM x D hD)) A hA).symm
  · exact operatorFieldLift_commutes_regular_of_intertwining B _
      (twistedCommutantField_intertwines B D)

/- A constant fibre in the regular core comes from the original base M.
The test against every D in M' is made with a strongly continuous twisted
field; equality in L² is reflected before evaluation at zero. -/
include hM in
theorem fibre_mem_regularCore_iff (C : H →L[ℂ] H) :
    fibre C ∈ core B M ↔ C ∈ M := by
  constructor
  · intro hC
    rw [← VonNeumannAlgebra.commutant_commutant (M),
      VonNeumannAlgebra.mem_commutant_iff]
    intro D hD
    have he := (VonNeumannAlgebra.mem_commutant_iff.mp
      (twistedCommutantLift_mem B M hM D hD)) (fibre C) hC
    have hzero := operatorFieldLift_commutation_reflects
      (twistedCommutantField B D) C he.symm 0
    rwa [twistedCommutantField_zero B] at hzero
  · exact fibre_mem B M C

theorem shift_commutes_regularUnitary (s t : ℝ) :
    shift s * regularUnitary B t = regularUnitary B t * shift s := by
  unfold F1Fecho.RegularCovariantCore.regularUnitary
  calc
    _ = (shift s * fibre (boostCLM B t)) * shift t := by rw [mul_assoc]
    _ = fibre (boostCLM B t) * (shift s * shift t) := by
      rw [shift_commutes_fibre, mul_assoc]
    _ = fibre (boostCLM B t) * (shift t * shift s) := by
      rw [shift_mul, shift_mul, add_comm s t]
    _ = _ := by rw [mul_assoc]

/-- Every member of N commutes with ordinary translations. This follows from
its generators and bicommutant closure, not a decomposition theorem. -/
theorem regularCore_le_shiftCommutant :
    core B M ≤
      starCommutantAlgebra (Set.range (shift (H := H))) := by
  apply core_minimal B M
  · intro A _
    change fibre A ∈ StarSubalgebra.centralizer ℂ _
    rw [StarSubalgebra.mem_centralizer_iff]
    rintro _ ⟨s,rfl⟩
    refine ⟨shift_commutes_fibre s A, ?_⟩
    rw [shift_star]
    exact shift_commutes_fibre (-s) A
  · intro t
    change regularUnitary B t ∈ StarSubalgebra.centralizer ℂ _
    rw [StarSubalgebra.mem_centralizer_iff]
    rintro _ ⟨s,rfl⟩
    refine ⟨shift_commutes_regularUnitary B s t, ?_⟩
    rw [shift_star]
    exact shift_commutes_regularUnitary B (-s) t

theorem shift_mem_regularCommutant (s : ℝ) :
    shift s ∈ (core B M).commutant := by
  rw [VonNeumannAlgebra.mem_commutant_iff]
  intro X hX
  have h := regularCore_le_shiftCommutant B M hX
  change X ∈ StarSubalgebra.centralizer ℂ _ at h
  rw [StarSubalgebra.mem_centralizer_iff] at h
  exact (h _ ⟨s,rfl⟩).1.symm

theorem dualFixed_eq_fibre_candidate
    (A : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hA : A ∈ core B M) (hfix : ∀ s : ℝ, dualAmbient s A = A) :
    A = fibre (fibreCandidate A) := by
  apply eq_fibre_of_shift_character_commutation A
  · intro t
    exact ((VonNeumannAlgebra.mem_commutant_iff.mp (shift_mem_regularCommutant B M t)) A hA).symm
  · intro t
    exact (dualAmbient_fixed_iff_commutes t A).mp (hfix t)

include hM in
theorem dualFixed_eq_amplified_base
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) :
    (A ∈ core B M ∧ ∀ s : ℝ, dualAmbient s A = A) ↔ ∃ C ∈ M, A = fibre C := by
  constructor
  · rintro ⟨hA,hfix⟩
    have he := dualFixed_eq_fibre_candidate B M A hA hfix
    refine ⟨fibreCandidate A,?_,he⟩
    apply (fibre_mem_regularCore_iff B M hM _).mp
    rwa [← he]
  · rintro ⟨C,hC,rfl⟩
    exact ⟨fibre_mem B M C hC,fun s => dualAmbient_fibre s C⟩

end F1Fecho.RegularCoreFixed
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.RegularCoreFixed).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
