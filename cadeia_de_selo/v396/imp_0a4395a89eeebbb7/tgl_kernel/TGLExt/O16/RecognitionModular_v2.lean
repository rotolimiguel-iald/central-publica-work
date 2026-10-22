-- predecessor_sha256: 4b6b64fedab87145e04385e9f7c3415aca3004742ad982e96601a57770b667f0
import Lean
import TGLExt.O16.RecognitionSquare
import TGLExt.V351ResolventImaginaryIntertwining
import TGLExt.V350BoundedInjectivePolar

set_option autoImplicit false
set_option maxHeartbeats 1500000
namespace ORDEM016.D6
noncomputable section
open Set Topology TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- Analytic realizations of one closed Tomita graph, supplied independently.
No equation relating two pairs or two modular operators is a field. -/
structure ModularGraphRealization (G : Set (H × H)) where
  R : H →L[ℂ] H
  nonneg : 0 ≤ R
  le_one : R ≤ 1
  injective : Function.Injective R
  complement_injective : Function.Injective (1-R : H →L[ℂ] H)
  resolvent_mem : ∀ x : H, (R x,x-R x) ∈ antilinearSquareGraph G
  resolvent_inverse : ∀ x y : H, (x,y) ∈ antilinearSquareGraph G → R (x+y)=x
  graph_functional : ∀ x y z : H, (x,y) ∈ G → (x,z) ∈ G → y=z
  J : H ≃ₛₗᵢ[starRingEnd ℂ] H
  polar_regularized : ∀ x : H,
    (R x,J (CFC.sqrt (resolventDampingOperator R) x)) ∈ G

variable {G G' : Set (H × H)}

theorem recognizes_resolvent (U : H ≃ₗᵢ[ℂ] H)
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) (B : ModularGraphRealization G') (x : H) :
    U (A.R x)=B.R (U x) :=
  unitary_recognizes_square_resolvent U G G' hg A.R B.R A.resolvent_mem B.resolvent_inverse x

theorem recognizes_resolvent_operator (U : H ≃ₗᵢ[ℂ] H)
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) (B : ModularGraphRealization G') :
    B.R * U.toContinuousLinearEquiv.toContinuousLinearMap =
      U.toContinuousLinearEquiv.toContinuousLinearMap * A.R := by
  ext x
  exact (recognizes_resolvent U hg A B x).symm

theorem recognizes_imaginary_powers (U : H ≃ₗᵢ[ℂ] H)
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) (B : ModularGraphRealization G') (t : ℝ) (x : H) :
    U (resolventImaginaryPower A.R A.nonneg A.le_one A.injective A.complement_injective t x) =
      resolventImaginaryPower B.R B.nonneg B.le_one B.injective B.complement_injective t (U x) := by
  exact (resolventImaginaryPower_intertwines B.R A.R
    U.toContinuousLinearEquiv.toContinuousLinearMap
    B.nonneg B.le_one B.injective B.complement_injective
    A.nonneg A.le_one A.injective A.complement_injective
    (recognizes_resolvent_operator U hg A B) t x).symm

theorem regularized_root_dense (A : ModularGraphRealization G) :
    DenseRange (CFC.sqrt (resolventDampingOperator A.R) : H →L[ℂ] H) :=
  ChatgptAudit.Continuous049.bounded_graph_domain_dense _ 0
    (positive_sqrt_injective _ (resolventDampingOperator_nonneg A.R A.nonneg A.le_one)
      (resolventDampingOperator_injective A.R A.injective A.complement_injective))
    (IsSelfAdjoint.of_nonneg (CFC.sqrt_nonneg _))

theorem recognizes_regularized_root (U : H ≃ₗᵢ[ℂ] H)
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) (B : ModularGraphRealization G') (x : H) :
    CFC.sqrt (resolventDampingOperator B.R) (U x) =
      U (CFC.sqrt (resolventDampingOperator A.R) x) := by
  exact congrArg (fun F : H →L[ℂ] H => F x)
    (positive_sqrt_intertwines _ _ U.toContinuousLinearEquiv.toContinuousLinearMap
      (resolventDampingOperator_nonneg B.R B.nonneg B.le_one)
      (resolventDampingOperator_nonneg A.R A.nonneg A.le_one)
      (resolventDampingOperator_intertwines B.R A.R _ (recognizes_resolvent_operator U hg A B)))

theorem recognizes_polar_factor (U : H ≃ₗᵢ[ℂ] H)
    (hg : (U.toHomeomorph.prodCongr U.toHomeomorph) '' G = G')
    (A : ModularGraphRealization G) (B : ModularGraphRealization G') (x : H) :
    U (A.J x)=B.J (U x) := by
  refine (regularized_root_dense A).induction ?_ (isClosed_eq (by fun_prop) (by fun_prop)) x
  rintro _ ⟨y,rfl⟩
  have hsource : (U (A.R y),U (A.J (CFC.sqrt (resolventDampingOperator A.R) y))) ∈ G' := by
    rw [← hg]
    exact ⟨(A.R y,A.J (CFC.sqrt (resolventDampingOperator A.R) y)),A.polar_regularized y,rfl⟩
  rw [recognizes_resolvent U hg A B y] at hsource
  have he := B.graph_functional _ _ _ hsource (B.polar_regularized (U y))
  rw [recognizes_regularized_root U hg A B y] at he
  exact he

/-- Conditional bridge for independently realized pairs on the same Hilbert space.
Instantiation of each analytic realization is a separate obligation. -/
theorem same_horizon_by_content
    {M N : StarSubalgebra ℂ (H →L[ℂ] H)} {omega omega' : H}
    (C : ReconhecimentoPeloConteudo M N omega omega')
    (A : ModularGraphRealization (closure (pairTomitaGraph M omega)))
    (B : ModularGraphRealization (closure (pairTomitaGraph N omega'))) :
    (∀ x, C.U (A.J x)=B.J (C.U x)) ∧
    (∀ t x, C.U (resolventImaginaryPower A.R A.nonneg A.le_one A.injective A.complement_injective t x) =
      resolventImaginaryPower B.R B.nonneg B.le_one B.injective B.complement_injective t (C.U x)) :=
  ⟨recognizes_polar_factor C.U (recognition_closed_tomita_graph C) A B,
   recognizes_imaginary_powers C.U (recognition_closed_tomita_graph C) A B⟩

#print axioms recognizes_resolvent
#print axioms recognizes_resolvent_operator
#print axioms recognizes_imaginary_powers
#print axioms regularized_root_dense
#print axioms recognizes_regularized_root
#print axioms recognizes_polar_factor
#print axioms same_horizon_by_content
end
end ORDEM016.D6


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
