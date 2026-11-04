import Lean
import TGLExt.O16.SelfadjointSquareResolvent
import TGLExt.V350GraphCoreNormTransfer

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace ChatgptAudit.UnboundedTransform016
open TGLV350.Regular
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem selfadjoint_graph_range_closed (D : H →ₗ.[ℂ] H) (hs : IsSelfAdjoint D) :
    IsClosed (Set.range (fun x : D.domain => ((x : H),D x))) := by
  have he : Set.range (fun x : D.domain => ((x : H),D x)) = (D.graph : Set (H × H)) := by
    ext p
    constructor
    · rintro ⟨u,rfl⟩
      exact D.mem_graph u
    · intro hp
      obtain ⟨u,hu,hDu⟩ := (LinearPMap.mem_graph_iff D).mp hp
      exact ⟨u,Prod.ext hu hDu⟩
  rw [he]
  exact hs.isClosed

theorem sameSquare_norm_core (D E Q : H →ₗ.[ℂ] H)
    (hd : IsSelfAdjoint D) (he : IsSelfAdjoint E)
    (hdq : partialOperatorSquare D=Q) (heq : partialOperatorSquare E=Q)
    (x : Q.domain) :
    ‖D (Submodule.inclusion (partialSquare_domain_le D Q hdq) x)‖ =
      ‖E (Submodule.inclusion (partialSquare_domain_le E Q heq) x)‖ := by
  obtain ⟨u,hu,hn⟩ := partialSquare_energy D Q (selfadjoint_formal D hd) hdq x
  obtain ⟨v,hv,hm⟩ := partialSquare_energy E Q (selfadjoint_formal E he) heq x
  have hu' : Submodule.inclusion (partialSquare_domain_le D Q hdq) x=u := Subtype.ext hu.symm
  have hv' : Submodule.inclusion (partialSquare_domain_le E Q heq) x=v := Subtype.ext hv.symm
  rw [hu',hv']
  nlinarith only [hn,hm,norm_nonneg (D u),norm_nonneg (E v)]

theorem sameSquare_domain_le (D E Q : H →ₗ.[ℂ] H)
    (hd : IsSelfAdjoint D) (he : IsSelfAdjoint E)
    (hdq : partialOperatorSquare D=Q) (heq : partialOperatorSquare E=Q) :
    D.domain ≤ E.domain := by
  have hr : ∀ z : H, ∃ u : Q.domain, (u : H)+Q u=z := by
    rw [← hdq]
    exact selfadjoint_one_add_square_onto D hd
  exact graphCore_norm_domain_transfer D.domain E.domain Q.domain
    (D.toFun.restrictScalars ℝ) (E.toFun.restrictScalars ℝ)
    (partialSquare_domain_le D Q hdq) (partialSquare_domain_le E Q heq)
    (partialSquare_graph_core D Q hdq (selfadjoint_formal D hd)
      (selfadjoint_graph_range_closed D hd) hr)
    (selfadjoint_graph_range_closed E he) (sameSquare_norm_core D E Q hd he hdq heq)

theorem sameSquare_domain_eq (D E Q : H →ₗ.[ℂ] H)
    (hd : IsSelfAdjoint D) (he : IsSelfAdjoint E)
    (hdq : partialOperatorSquare D=Q) (heq : partialOperatorSquare E=Q) :
    D.domain=E.domain :=
  le_antisymm (sameSquare_domain_le D E Q hd he hdq heq)
    (sameSquare_domain_le E D Q he hd heq hdq)

theorem sameSquare_norm_full (D E Q : H →ₗ.[ℂ] H)
    (hd : IsSelfAdjoint D) (he : IsSelfAdjoint E)
    (hdq : partialOperatorSquare D=Q) (heq : partialOperatorSquare E=Q)
    (x : D.domain) :
    ‖D x‖ = ‖E (Submodule.inclusion (sameSquare_domain_le D E Q hd he hdq heq) x)‖ := by
  have hr : ∀ z : H, ∃ u : Q.domain, (u : H)+Q u=z := by
    rw [← hdq]
    exact selfadjoint_one_add_square_onto D hd
  obtain ⟨y,hy,hn⟩ := graphCore_norm_extension D.domain E.domain Q.domain
    (D.toFun.restrictScalars ℝ) (E.toFun.restrictScalars ℝ)
    (partialSquare_domain_le D Q hdq) (partialSquare_domain_le E Q heq)
    (partialSquare_graph_core D Q hdq (selfadjoint_formal D hd)
      (selfadjoint_graph_range_closed D hd) hr)
    (selfadjoint_graph_range_closed E he) (sameSquare_norm_core D E Q hd he hdq heq) x
  have he' : Submodule.inclusion (sameSquare_domain_le D E Q hd he hdq heq) x=y :=
    Subtype.ext hy.symm
  rw [he']
  exact hn

#print axioms selfadjoint_graph_range_closed
#print axioms sameSquare_norm_core
#print axioms sameSquare_domain_le
#print axioms sameSquare_domain_eq
#print axioms sameSquare_norm_full
end ChatgptAudit.UnboundedTransform016


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
