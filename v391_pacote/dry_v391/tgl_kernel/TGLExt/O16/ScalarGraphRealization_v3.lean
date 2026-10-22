-- predecessor_sha256: 21e1d590d7bdfaf950030d214fd06aa813fe10be6b4f49d2251e718cc4aaf4db
-- predecessor_sha256: 6e947b19e661c02b809cd5ad9b8860c69853455fa6084dd118bbd6da0bc6d8a2
import Lean
import TGLExt.O16.RecognitionReadout
import TGLExt.V351ScalarTomitaImaginaryPowers

set_option autoImplicit false
set_option maxHeartbeats 1800000
set_option synthInstance.maxHeartbeats 200000
namespace ORDEM016.D6
noncomputable section
open Set Topology TGLExt TGLV350.Regular ChatgptAudit.Continuous049

variable (P : SiteProfile)

/-- Identify our adjoint-pairing relation with the existing maximal composition.
This is the scalar GNS construction, not a photon-net identification. -/
theorem scalar_square_relation :
    antilinearSquareGraph (closure (scalarTomitaGraph P)) = (scalarTomitaSquare P).graph := by
  ext p
  constructor
  · rintro ⟨sx,hsx,hpair⟩
    let x : scalarClosedTomitaDomain P := ⟨p.1,⟨sx,hsx⟩⟩
    have hval : scalarClosedTomita P x=sx :=
      scalarTomitaGraph_closure_single_valued P p.1 _ _ (scalarClosedTomita_graph x) hsx
    obtain ⟨ha,hav⟩ := scalarTomitaAdjoint_maximal P (y := scalarClosedTomita P x) (z := p.2)
      (fun y => by
        rw [hval]
        exact (hpair y (scalarClosedTomita P y) (scalarClosedTomita_graph y)).symm)
    let q : scalarTomitaSquareDomain P := ⟨p.1,⟨x.property,ha⟩⟩
    apply (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mpr
    refine ⟨q,rfl,?_⟩
    exact hav
  · intro hp
    obtain ⟨q,hx,hz⟩ := (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mp hp
    change scalarTomitaSquareDomain P at q
    refine ⟨scalarClosedTomita P (scalarTomitaSquareInput P q),?_,?_⟩
    · simpa only [scalarTomitaSquareInput_coe,hx] using scalarClosedTomita_graph (scalarTomitaSquareInput P q)
    · intro y sy hy
      rw [← scalarClosedTomita_graph_eq (P := P)] at hy
      obtain ⟨t,ht⟩ := hy
      have hty : (t : ScalarGNSHilbert P)=y := congrArg Prod.fst ht
      have hts : scalarClosedTomita P t=sy := congrArg Prod.snd ht
      rw [← hty,← hts,← hz]
      exact scalarTomitaSquare_pairing P q t

theorem scalar_resolvent_in_relation (z : ScalarGNSHilbert P) :
    (scalarTomitaResolvent P z,z-scalarTomitaResolvent P z) ∈
      antilinearSquareGraph (closure (scalarTomitaGraph P)) := by
  rw [scalar_square_relation]
  obtain ⟨q,hq,he⟩ := scalarTomitaResolvent_equation P z
  apply (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mpr
  refine ⟨q,hq,?_⟩
  rw [hq] at he
  exact eq_sub_of_add_eq' he

theorem scalar_resolvent_inverse_relation (x y : ScalarGNSHilbert P)
    (h : (x,y) ∈ antilinearSquareGraph (closure (scalarTomitaGraph P))) :
    scalarTomitaResolvent P (x+y)=x := by
  rw [scalar_square_relation] at h
  obtain ⟨q,hx,hy⟩ := (LinearPMap.mem_graph_iff (scalarTomitaSquare P)).mp h
  change (q : ScalarGNSHilbert P)=x at hx
  change scalarTomitaSquare P q=y at hy
  rw [← hx,← hy]
  exact scalarTomitaResolvent_inverse P q

theorem sqrt_damping_factorization {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R : H →L[ℂ] H) (hR : 0 ≤ R) (h1 : R ≤ 1) :
    CFC.sqrt (resolventDampingOperator R)=CFC.sqrt R*CFC.sqrt (1-R) := by
  have hc := resolvent_sqrt_pair_commute R
  apply CFC.sqrt_unique
  · calc
      _ = CFC.sqrt R * (CFC.sqrt (1-R) * CFC.sqrt R) * CFC.sqrt (1-R) := by simp only [mul_assoc]
      _ = CFC.sqrt R * (CFC.sqrt R * CFC.sqrt (1-R)) * CFC.sqrt (1-R) := by rw [← hc]
      _ = (CFC.sqrt R * CFC.sqrt R) * (CFC.sqrt (1-R) * CFC.sqrt (1-R)) := by simp only [mul_assoc]
      _ = resolventDampingOperator R := by
        rw [CFC.sqrt_mul_sqrt_self R hR,CFC.sqrt_mul_sqrt_self (1-R) (sub_nonneg.mpr h1)]
        rfl
  · exact Commute.mul_nonneg (CFC.sqrt_nonneg R) (CFC.sqrt_nonneg (1-R)) hc

def dampingRoot {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R : H →L[ℂ] H) : H →L[ℂ] H := CFC.sqrt (resolventDampingOperator R)

theorem damping_root_in_partial_graph {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R : H →L[ℂ] H) (hR : 0 ≤ R) (hi : Function.Injective R) (h1 : R ≤ 1) (z : H) :
    (R z,dampingRoot R z) ∈ (resolventSquareRoot R hR hi).graph := by
  apply (bounded_graph_param_iff (CFC.sqrt R) (CFC.sqrt (1-R))
    (positive_sqrt_injective R hR hi) _ _).mpr
  refine ⟨CFC.sqrt R z,?_,?_⟩
  · exact congrArg (fun T : H →L[ℂ] H => T z) (CFC.sqrt_mul_sqrt_self R hR)
  · have he := sqrt_damping_factorization R hR h1
    rw [resolvent_sqrt_pair_commute R] at he
    exact (congrArg (fun T : H →L[ℂ] H => T z) he).symm

theorem scalar_polar_regularized (z : ScalarGNSHilbert P) :
    (scalarTomitaResolvent P z,scalarTomitaPolarFactor P (dampingRoot (scalarTomitaResolvent P) z)) ∈
      closure (scalarTomitaGraph P) := by
  have hroot := damping_root_in_partial_graph (scalarTomitaResolvent P)
    (scalarTomitaResolvent_nonneg P) (scalarTomitaResolvent_injective P) (scalarTomitaResolvent_le_one P) z
  change (_,_) ∈ (scalarTomitaPositiveRoot P).graph at hroot
  obtain ⟨u,hu,hv⟩ := (LinearPMap.mem_graph_iff (scalarTomitaPositiveRoot P)).mp hroot
  have hs := scalarClosedTomita_graph (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) u)
  have hf := scalarTomitaPolarFactor_root P u
  change scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P u)=
    scalarClosedTomita P (Submodule.inclusion (scalarTomitaRootDomain_le_closed P) u) at hf
  rw [← hf] at hs
  change ((u : ScalarGNSHilbert P),scalarTomitaPolarFactor P (scalarTomitaPositiveRoot P u)) ∈ _ at hs
  simpa only [hu,hv] using hs

/-- A concrete analytic realization already present in the scalar GNS tower.
It does not identify this graph with the physical photon wedge graph. -/
def scalarGraphRealization : ModularGraphRealization (closure (scalarTomitaGraph P)) where
  R := scalarTomitaResolvent P
  nonneg := scalarTomitaResolvent_nonneg P
  le_one := scalarTomitaResolvent_le_one P
  injective := scalarTomitaResolvent_injective P
  complement_injective := scalarTomitaResolvent_complement_injective P
  resolvent_mem := scalar_resolvent_in_relation P
  resolvent_inverse := scalar_resolvent_inverse_relation P
  graph_functional := scalarTomitaGraph_closure_single_valued P
  J := scalarTomitaPolarFactor P
  polar_regularized := scalar_polar_regularized P

def scalarGraphReadout : ModularReadout (scalarGraphRealization P) where
  flow := scalarTomitaImaginaryPower P
  spectral_readout := scalarTomitaImaginaryPower_damping P

#print axioms scalar_square_relation
#print axioms scalar_resolvent_in_relation
#print axioms scalar_resolvent_inverse_relation
#print axioms sqrt_damping_factorization
#print axioms dampingRoot
#print axioms damping_root_in_partial_graph
#print axioms scalar_polar_regularized
#print axioms scalarGraphRealization
#print axioms scalarGraphReadout
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
