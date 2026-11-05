import TGLExt.V350RegularDualAction
/-! Generic regular covariant representation, faithful generated-algebra embedding
and dual action for an actual strongly continuous unitary flow. No trace or
modular-state identification is assumed or asserted. The concrete Fock flow is
an instance supplied in the separate consumer, not a claimed hypothetical one. -/
set_option autoImplicit false
set_option maxHeartbeats 400000
noncomputable section
namespace F1Fecho.RegularCovariantCore
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
structure UnitaryFlow (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] where
  U : ℝ → H ≃ₗᵢ[ℂ] H
  zero : U 0 = .refl ℂ H
  add : ∀ s t, U (s+t) = (U t).trans (U s)
  strong : ∀ v, Continuous (fun t => U t v)
variable (B : UnitaryFlow H)

def boostIso (t : ℝ) : H ≃ₗᵢ[ℂ] H := B.U t
def boostCLM (t : ℝ) : H →L[ℂ] H := (boostIso B t).toLinearIsometry.toContinuousLinearMap

theorem boostIso_zero : boostIso B 0 = .refl ℂ H := B.zero

theorem boostIso_add (s t : ℝ) : boostIso B (s+t) = (boostIso B t).trans (boostIso B s) := B.add s t

theorem boostIso_neg (t : ℝ) : boostIso B (-t) = (boostIso B t).symm := by
  apply LinearIsometryEquiv.ext
  intro v
  apply (boostIso B t).injective
  rw [LinearIsometryEquiv.apply_symm_apply]
  have h := congrArg (fun u : H ≃ₗᵢ[ℂ] H => u v) (boostIso_add B t (-t))
  have hz := h.symm
  simp only [add_neg_cancel,boostIso_zero B,LinearIsometryEquiv.trans_apply] at hz
  exact hz

theorem boostCLM_zero : boostCLM B 0 = 1 := by rw [boostCLM,boostIso_zero B]; rfl

theorem boostCLM_mul (s t : ℝ) : boostCLM B s * boostCLM B t = boostCLM B (s+t) := by
  apply ContinuousLinearMap.ext
  intro v
  change boostIso B s (boostIso B t v) = boostIso B (s+t) v
  rw [boostIso_add B]
  rfl

theorem boostCLM_eq_coe (t : ℝ) :
    boostCLM B t = (boostIso B t : H →L[ℂ] H) := by
  apply ContinuousLinearMap.ext
  intro v
  rfl

theorem boostCLM_star (t : ℝ) : star (boostCLM B t) = boostCLM B (-t) := by
  rw [boostCLM_eq_coe B,LinearIsometryEquiv.star_eq_symm,boostCLM_eq_coe B,boostIso_neg B]

theorem boostIso_strong (v : H) : Continuous (fun t : ℝ => boostIso B t v) := by
  exact B.strong v

def automorphism (t : ℝ) : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (H →L[ℂ] H) := (boostIso B t).conjStarAlgEquiv

theorem boostAd_sandwich (t : ℝ) (A : H →L[ℂ] H) :
    automorphism B t A = boostCLM B t * A * star (boostCLM B t) := by
  rw [boostCLM_eq_coe B,LinearIsometryEquiv.star_eq_symm]
  rfl

def regularUnitary (t : ℝ) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  fibre (boostCLM B t) * shift t

theorem regular_zero : regularUnitary B 0 = 1 := by
  simp only [regularUnitary,boostCLM_zero B,fibre_one,shift_zero,mul_one]

theorem regular_mul (s t : ℝ) : regularUnitary B s * regularUnitary B t = regularUnitary B (s+t) := by
  unfold regularUnitary
  calc
    (fibre (boostCLM B s) * shift s) * (fibre (boostCLM B t) * shift t)
      = fibre (boostCLM B s) * (shift s * fibre (boostCLM B t)) * shift t := by simp only [mul_assoc]
    _ = fibre (boostCLM B s) * (fibre (boostCLM B t) * shift s) * shift t := by rw [shift_commutes_fibre]
    _ = (fibre (boostCLM B s) * fibre (boostCLM B t)) * (shift s * shift t) := by simp only [mul_assoc]
    _ = fibre (boostCLM B (s+t)) * shift (s+t) := by rw [← fibre_mul,boostCLM_mul B,shift_mul]

theorem regular_star (t : ℝ) : star (regularUnitary B t) = regularUnitary B (-t) := by
  unfold regularUnitary
  rw [star_mul,shift_star,← fibre_star,boostCLM_star B,shift_commutes_fibre]

theorem regular_unitary (t : ℝ) : star (regularUnitary B t) * regularUnitary B t = 1 ∧
    regularUnitary B t * star (regularUnitary B t) = 1 := by
  constructor
  · rw [regular_star B,regular_mul B,neg_add_cancel,regular_zero B]
  · rw [regular_star B,regular_mul B,add_neg_cancel,regular_zero B]

theorem regular_covariance (t : ℝ) (A : H →L[ℂ] H) :
    regularUnitary B t * fibre A * star (regularUnitary B t) =
      fibre (automorphism B t A) := by
  rw [boostAd_sandwich B,fibre_mul,fibre_mul,fibre_star]
  unfold regularUnitary
  calc
    _ = fibre (boostCLM B t) * (shift t * fibre A * star (shift (H := H) t)) *
      star (fibre (boostCLM B t)) := by simp only [star_mul,mul_assoc]
    _ = _ := by rw [shift_star,shift_fibre_sandwich]

theorem regular_strongly_continuous (f : RegularHilbert H) :
    Continuous (fun t : ℝ => regularUnitary B t f) := by
  have h := fibre_jointly_continuous (H := H) (Z := ℝ)
    (fun t => (boostIso B t).toLinearIsometry) (boostIso_strong B)
  have hp : Continuous (fun t : ℝ => (shift (H := H) t f,t)) :=
    (shift_strongly_continuous f).prodMk continuous_id
  refine (h.comp hp).congr ?_
  intro t
  change fibre (boostIso B t).toLinearIsometry.toContinuousLinearMap (shift t f) = regularUnitary B t f
  rfl

def generators (M : VonNeumannAlgebra H) : Set (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  (fibre '' (M : Set (H →L[ℂ] H))) ∪ Set.range (regularUnitary B)

def core (M : VonNeumannAlgebra H) : VonNeumannAlgebra (RegularHilbert H) :=
  generatedAlgebra (generators B M)

theorem fibre_mem (M : VonNeumannAlgebra H) (A : H →L[ℂ] H) (hA : A ∈ M) : fibre A ∈ core B M :=
  generator_mem (Or.inl ⟨A,hA,rfl⟩)

theorem regular_mem (M : VonNeumannAlgebra H) (t : ℝ) : regularUnitary B t ∈ core B M :=
  generator_mem (Or.inr ⟨t,rfl⟩)

def amplification (M : VonNeumannAlgebra H) : M.toStarSubalgebra →⋆ₐ[ℂ]
    (RegularHilbert H →L[ℂ] RegularHilbert H) :=
  fibreRepresentation.comp M.toStarSubalgebra.subtype

def embedding (M : VonNeumannAlgebra H) : M.toStarSubalgebra →⋆ₐ[ℂ] (core B M).toStarSubalgebra :=
  (amplification M).codRestrict (core B M).toStarSubalgebra (fun A => fibre_mem B M A A.property)

theorem embedding_injective (M : VonNeumannAlgebra H) : Function.Injective (embedding B M) := by
  intro A B h
  apply Subtype.ext
  apply fibre_injective
  exact congrArg Subtype.val h

theorem core_minimal (M : VonNeumannAlgebra H) (N : VonNeumannAlgebra (RegularHilbert H))
    (hM : ∀ A ∈ M, fibre A ∈ N) (hU : ∀ t : ℝ, regularUnitary B t ∈ N) : core B M ≤ N := by
  apply generated_minimal (generators B M) N
  intro A hA
  rcases hA with ⟨A0,hA0,rfl⟩ | ⟨t,rfl⟩
  · exact hM A0 hA0
  · exact hU t

theorem dual_on_regular (s t : ℝ) :
    dualAmbient s (regularUnitary B t) = characterPhase s t • regularUnitary B t := by
  rw [dualAmbient_apply]
  unfold regularUnitary
  calc
    _ = fibre (boostCLM B t) * (characterMultiplier s * shift t *
      star (characterMultiplier (H := H) s)) := by
      rw [← mul_assoc (characterMultiplier s),characterMultiplier_commutes_fibre]
      simp only [mul_assoc]
    _ = _ := by rw [characterMultiplier_weyl,mul_smul_comm]; rfl

theorem dual_preserves_generators (M : VonNeumannAlgebra H) (s : ℝ) :
    ∀ A ∈ generators B M, dualAmbient s A ∈ core B M := by
  intro A hA
  rcases hA with ⟨A0,hA0,rfl⟩ | ⟨t,rfl⟩
  · rw [dualAmbient_fibre]
    exact fibre_mem B M A0 hA0
  · rw [dual_on_regular B]
    exact (core B M).toStarSubalgebra.smul_mem (regular_mem B M t) _

def dualAction (M : VonNeumannAlgebra H) (s : ℝ) :
    (core B M).toStarSubalgebra ≃⋆ₐ[ℂ] (core B M).toStarSubalgebra :=
  generatedAutomorphism (dualAmbient s) (generators B M) (dual_preserves_generators B M s) (by
    rw [dualAmbient_symm (H := H)]
    exact dual_preserves_generators B M (-s))

theorem dualAction_zero (M : VonNeumannAlgebra H) : dualAction B M 0 = StarAlgEquiv.refl := by
  apply StarAlgEquiv.ext
  intro A
  apply Subtype.ext
  change dualAmbient (H := H) 0 (A : RegularHilbert H →L[ℂ] RegularHilbert H) = A
  rw [dualAmbient_zero (H := H)]
  rfl

theorem dualAction_add (M : VonNeumannAlgebra H) (s t : ℝ) :
    dualAction B M (s+t) = (dualAction B M s).trans (dualAction B M t) := by
  apply StarAlgEquiv.ext
  intro A
  apply Subtype.ext
  change dualAmbient (H := H) (s+t) (A : RegularHilbert H →L[ℂ] RegularHilbert H) =
    dualAmbient t (dualAmbient s A)
  rw [dualAmbient_add (H := H)]
  rfl

theorem dual_fixes_embedding (M : VonNeumannAlgebra H) (s : ℝ) (A : M.toStarSubalgebra) :
    dualAction B M s (embedding B M A) = embedding B M A := by
  apply Subtype.ext
  exact dualAmbient_fibre (H := H) s (A : H →L[ℂ] H)

theorem dual_strongly_continuous (M : VonNeumannAlgebra H)
    (A : (core B M).toStarSubalgebra) (f : RegularHilbert H) :
    Continuous (fun s : ℝ => (dualAction B M s A).val f) :=
  dualAmbient_strongly_continuous (H := H) (A : RegularHilbert H →L[ℂ] RegularHilbert H) f

end F1Fecho.RegularCovariantCore
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.RegularCovariantCore).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
