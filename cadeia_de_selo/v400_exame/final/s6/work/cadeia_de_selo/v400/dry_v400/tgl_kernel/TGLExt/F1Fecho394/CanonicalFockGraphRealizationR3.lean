import TGLExt.F1Fecho394.CanonicalFockDeltaR4
import TGLExt.F1Fecho394.PositiveRegularizedRootR3
import TGLExt.O16.RecognitionModular_v2
/-! Analytic modular graph of the actual Weyl/vacuum pair, constructed from its
positive selfadjoint Fock lift. The spectral readout by the prescribed boost
flow is NOT assumed or proved in this module. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 200000
noncomputable section
open scoped InnerProductSpace
namespace F1Fecho.CanonicalFockPolar
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Rede.CanonicalWedge
open F1Fecho.ExponentialLift F1Fecho.ExponentialTomita F1Fecho.Antilinear
open F1Fecho.ExponentialTomitaEquality F1Fecho.ExponentialTomitaInclusion
open F1Fecho.WedgePairTomita ChatgptAudit.Continuous050
open TGLV350.Regular ChatgptAudit.UnboundedTransform016 ORDEM016.D6

local instance operatorRealModule : Module ℝ (F →L[ℂ] F) :=
  Module.restrictScalars ℝ ℂ (F →L[ℂ] F)

abbrev actualGraph := closure (pairTomitaGraph (algebra KWR) vacuum)

theorem actualGraph_eq : actualGraph =
    Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) :=
  (graph_eq KWR).symm.trans tomita_graph_eq

theorem partialSquare_eq : partialOperatorSquare canonicalLift = Delta := by
  apply LinearPMap.eq_of_eq_graph
  ext p
  rcases p with ⟨x,y⟩
  change (x,y) ∈ (partialOperatorSquare canonicalLift).graph ↔
    (x,y) ∈ (PartialSquare.square canonicalLift).graph
  rw [partialOperatorSquare_graph_iff,PartialSquare.square_graph_iff_two]

theorem actual_square_relation : antilinearSquareGraph actualGraph = Delta.graph := by
  ext p
  rcases p with ⟨x,z⟩
  constructor
  · rintro ⟨sx,hsx,hp⟩
    rw [actualGraph_eq] at hsx
    obtain ⟨u,hu⟩ := hsx
    have hx : (u:F)=x := congrArg Prod.fst hu
    have hv : Sexp u=sx := congrArg Prod.snd hu
    obtain ⟨ha,hav⟩ := generic_adjoint_maximal canonicalLift canonicalLift_selfadjoint JF
      canonicalFockJ_involutive (y:=Sexp u) (z:=z) (fun v => by
        change inner ℂ (Sexp v) (Sexp u) = inner ℂ z (v:F)
        rw [hv]
        exact (hp v (Sexp v) (actualGraph_eq ▸ ⟨v,rfl⟩)).symm)
    apply (delta_graph_iff_tomita_comp x z).mpr
    subst x
    exact ⟨u.property,ha,hav⟩
  · intro hp
    obtain ⟨hx,ha,hv⟩ := (delta_graph_iff_tomita_comp x z).mp hp
    refine ⟨Sexp ⟨x,hx⟩,actualGraph_eq ▸ ⟨⟨x,hx⟩,rfl⟩,?_⟩
    intro y sy hy
    rw [actualGraph_eq] at hy
    obtain ⟨v,hv'⟩ := hy
    have hy' : (v:F)=y := congrArg Prod.fst hv'
    have hs' : Sexp v=sy := congrArg Prod.snd hv'
    rw [← hy',← hs',← hv]
    exact (generic_adjoint_pairing canonicalLift canonicalLift_selfadjoint JF
      canonicalFockJ_involutive v ⟨Sexp ⟨x,hx⟩,ha⟩).symm

theorem canonicalLift_kernel_zero (x : canonicalLift.domain) (hx : canonicalLift x=0) : (x:F)=0 := by
  have hS : Sexp x=0 := by
    change JF (canonicalLift x)=0
    rw [hx,map_zero]
  have hi := Sexp_involutive x
  have he : (⟨Sexp x,Sexp_maps_domain x⟩ : canonicalLift.domain)=0 := Subtype.ext hS
  rw [he,map_zero] at hi
  exact hi.symm

def modularR : F →L[ℂ] F := selfadjointSquareResolvent canonicalLift canonicalLift_selfadjoint

theorem modularR_nonneg : 0 ≤ modularR := selfadjoint_square_resolvent_nonneg _ _
theorem modularR_le_one : modularR ≤ 1 := selfadjoint_square_resolvent_le_one _ _
theorem modularR_injective : Function.Injective modularR := selfadjoint_square_resolvent_injective _ _

theorem modularR_complement_kernel (x : F) (hx : (1-modularR : F→L[ℂ]F) x=0) : x=0 := by
  have hr : modularR x=x := by
    change x-modularR x=0 at hx
    exact (sub_eq_zero.mp hx).symm
  obtain ⟨u,hu,he⟩ := selfadjoint_square_resolvent_equation canonicalLift canonicalLift_selfadjoint x
  change (u:F)=modularR x at hu
  have hux : (u:F)=x := hu.trans hr
  have hz : partialOperatorSquare canonicalLift u=0 := by
    rw [hux] at he
    exact add_left_cancel (he.trans (add_zero x).symm)
  obtain ⟨v,hv,hn⟩ := partialSquare_energy canonicalLift (partialOperatorSquare canonicalLift)
    (selfadjoint_formal _ canonicalLift_selfadjoint) rfl u
  rw [hz,inner_zero_right,Complex.zero_re] at hn
  have hv0 : canonicalLift v=0 := norm_eq_zero.mp (sq_eq_zero_iff.mp hn)
  exact hux.symm.trans (hv.symm.trans (canonicalLift_kernel_zero v hv0))

theorem modularR_complement_injective : Function.Injective (1-modularR : F→L[ℂ]F) := by
  intro x y h
  apply sub_eq_zero.mp
  apply modularR_complement_kernel
  rw [map_sub,h,sub_self]

theorem modularR_mem (x : F) : (modularR x,x-modularR x) ∈ antilinearSquareGraph actualGraph := by
  rw [actual_square_relation,← partialSquare_eq]
  obtain ⟨u,hu,he⟩ := selfadjoint_square_resolvent_equation canonicalLift canonicalLift_selfadjoint x
  apply (LinearPMap.mem_graph_iff _).mpr
  refine ⟨u,hu,?_⟩
  change (u:F)=modularR x at hu
  rw [hu] at he
  exact eq_sub_of_add_eq' he

theorem modularR_inverse (x y : F) (h : (x,y) ∈ antilinearSquareGraph actualGraph) : modularR (x+y)=x := by
  rw [actual_square_relation,← partialSquare_eq] at h
  obtain ⟨u,hu,hv⟩ := (LinearPMap.mem_graph_iff _).mp h
  have hr := partialPositiveResolvent_inverse (partialOperatorSquare canonicalLift)
    (selfadjoint_square_positive _ canonicalLift_selfadjoint)
    (selfadjoint_one_add_square_onto _ canonicalLift_selfadjoint) u
  change modularR ((u:F)+partialOperatorSquare canonicalLift u)=(u:F) at hr
  change (u:F)=x at hu
  change partialOperatorSquare canonicalLift u=y at hv
  rwa [hu,hv] at hr

theorem modular_polar_regularized (x : F) :
    (modularR x,JF (CFC.sqrt (resolventDampingOperator modularR) x)) ∈ actualGraph := by
  have h := PositiveRegularized.regularized_graph canonicalLift canonicalLift_selfadjoint
    ExponentialLiftPositive.canonicalLift_positive x
  obtain ⟨u,hu,hv⟩ := (LinearPMap.mem_graph_iff canonicalLift).mp h
  rw [actualGraph_eq]
  refine ⟨u,?_⟩
  apply Prod.ext
  · exact hu
  · change JF (canonicalLift u)=_
    exact congrArg JF hv

/-- Every field is paid by the actual Weyl graph and the constructed Fock root. -/
def actualGraphRealization : ModularGraphRealization actualGraph where
  R := modularR
  nonneg := modularR_nonneg
  le_one := modularR_le_one
  injective := modularR_injective
  complement_injective := modularR_complement_injective
  resolvent_mem := modularR_mem
  resolvent_inverse := modularR_inverse
  graph_functional := graph_functional KWR
  J := JF
  polar_regularized := modular_polar_regularized

end F1Fecho.CanonicalFockPolar
#print axioms F1Fecho.CanonicalFockPolar.partialSquare_eq
#print axioms F1Fecho.CanonicalFockPolar.actual_square_relation
#print axioms F1Fecho.CanonicalFockPolar.canonicalLift_kernel_zero
#print axioms F1Fecho.CanonicalFockPolar.modularR_complement_injective
#print axioms F1Fecho.CanonicalFockPolar.modularR_mem
#print axioms F1Fecho.CanonicalFockPolar.modularR_inverse
#print axioms F1Fecho.CanonicalFockPolar.modular_polar_regularized
#print axioms F1Fecho.CanonicalFockPolar.actualGraphRealization
