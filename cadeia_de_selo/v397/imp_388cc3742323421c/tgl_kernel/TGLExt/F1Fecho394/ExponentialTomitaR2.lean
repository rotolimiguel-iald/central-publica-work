import TGLExt.F1Fecho394.ExponentialLiftR2

/-! Closed, densely-defined involution obtained from the exponential lift and
concrete Gamma(J). This is an actual operator on the same Fock space, with a
proved graph invariance. Equality with the Tomita operator of the Weyl algebra
and vacuum is NOT asserted here. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open Filter Topology
namespace F1Fecho.ExponentialTomita
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.ExponentialLift F1Fecho.Antilinear F1Rede.CanonicalWedge
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050 AuditF13v31

abbrev JF := canonicalFockJ

theorem JF_exponential (f : H1) : JF (exponential f) = exponential (Jcandidate f) :=
  gammaJ_exponential _ _ f

theorem TW_SW (f : TW.domain) : TW ⟨SW TW Jcandidate f,SW_maps f⟩ = Jcandidate f := by
  have h := congrArg Jcandidate (SW_involutive f)
  change Jcandidate (Jcandidate (TW ⟨SW TW Jcandidate f,SW_maps f⟩)) = Jcandidate f at h
  exact (Jcandidate_involutive _).symm.trans h

def flipJ (p : F × F) : F × F := (JF p.2,JF p.1)

theorem flipJ_continuous : Continuous flipJ :=
  (JF.continuous.comp continuous_snd).prodMk (JF.continuous.comp continuous_fst)

theorem flipJ_involutive (p : F × F) : flipJ (flipJ p) = p := by
  exact Prod.ext (canonicalFockJ_involutive p.1) (canonicalFockJ_involutive p.2)

theorem coreGraph_flipJ (p : F × F) (hp : p ∈ coreGraph TW) : flipJ p ∈ coreGraph TW := by
  induction hp using Submodule.span_induction with
  | mem p hp =>
    obtain ⟨f,rfl⟩ := hp
    have hg : (exponential (SW TW Jcandidate f),
        exponential (TW ⟨SW TW Jcandidate f,SW_maps f⟩)) ∈ coreGraph TW :=
      Submodule.subset_span ⟨⟨SW TW Jcandidate f,SW_maps f⟩,rfl⟩
    rw [TW_SW] at hg
    change (JF (exponential (TW f)),JF (exponential f)) ∈ coreGraph TW
    rw [JF_exponential,JF_exponential]
    exact hg
  | zero =>
    change (JF 0,JF 0) ∈ coreGraph TW
    rw [map_zero]
    exact (coreGraph TW).zero_mem
  | add p q hp hq ihp ihq =>
    have he : flipJ (p+q) = flipJ p + flipJ q := by
      apply Prod.ext <;> simp only [flipJ,Prod.fst_add,Prod.snd_add,map_add]
    rw [he]
    exact (coreGraph TW).add_mem ihp ihq
  | smul c p hp ih =>
    have he : flipJ (c • p) = star c • flipJ p := by
      apply Prod.ext <;> exact JF.map_smulₛₗ c _
    rw [he]
    exact (coreGraph TW).smul_mem (star c) ih

theorem closedGraph_flipJ (p : F × F) (hp : p ∈ closedGraph TW) :
    flipJ p ∈ closedGraph TW := by
  have hc : IsClosed {q : F × F | flipJ q ∈ closedGraph TW} :=
    (coreGraph TW).isClosed_topologicalClosure.preimage flipJ_continuous
  have hi : closure (coreGraph TW : Set (F × F)) ⊆ {q : F × F | flipJ q ∈ closedGraph TW} :=
    closure_minimal (fun q hq => (coreGraph TW).le_topologicalClosure (coreGraph_flipJ q hq)) hc
  apply hi
  rw [← Submodule.topologicalClosure_coe]
  exact hp

/-- Constructed exponential Tomita candidate, without algebra identification. -/
def Sexp : canonicalLift.domain →ₛₗ[starRingEnd ℂ] F :=
  (genericTomita canonicalLift JF).toFun

theorem Sexp_maps_domain (x : canonicalLift.domain) : Sexp x ∈ canonicalLift.domain :=
  ⟨JF x,closedGraph_flipJ ((x:F),canonicalLift x) (closedValue_graph TW x)⟩

theorem Sexp_involutive (x : canonicalLift.domain) :
    Sexp ⟨Sexp x,Sexp_maps_domain x⟩ = x := by
  have h : canonicalLift ⟨Sexp x,Sexp_maps_domain x⟩ = JF x :=
    closedGraph_functional TW TW_selfadjoint (Sexp x) _ _
      (closedValue_graph TW ⟨Sexp x,Sexp_maps_domain x⟩)
      (closedGraph_flipJ ((x:F),canonicalLift x) (closedValue_graph TW x))
  change JF (canonicalLift ⟨Sexp x,Sexp_maps_domain x⟩) = (x:F)
  rw [h]
  exact canonicalFockJ_involutive x

theorem Sexp_graph_iff (p : F × F) :
    p ∈ Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) ↔
      (p.1,JF p.2) ∈ closedGraph TW := by
  constructor
  · rintro ⟨x,rfl⟩
    change ((x:F),JF (JF (canonicalLift x))) ∈ closedGraph TW
    rw [canonicalFockJ_involutive]
    exact closedValue_graph TW x
  · intro hp
    let x : canonicalLift.domain := ⟨p.1,JF p.2,hp⟩
    have h : canonicalLift x = JF p.2 :=
      closedGraph_functional TW TW_selfadjoint p.1 _ _ (closedValue_graph TW x) hp
    refine ⟨x,?_⟩
    apply Prod.ext
    · rfl
    · change JF (canonicalLift x) = p.2
      rw [h]
      exact canonicalFockJ_involutive p.2

theorem Sexp_closed :
    IsClosed (Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x))) := by
  have he : Set.range (fun x : canonicalLift.domain => ((x:F),Sexp x)) =
      (fun p : F × F => (p.1,JF p.2)) ⁻¹' (closedGraph TW : Set (F × F)) := by
    ext p
    exact Sexp_graph_iff p
  rw [he]
  exact (coreGraph TW).isClosed_topologicalClosure.preimage
    (continuous_fst.prodMk (JF.continuous.comp continuous_snd))

theorem Sexp_dense : Dense (canonicalLift.domain : Set F) := canonicalLift_dense

theorem Sexp_exponential (f : TW.domain) :
    Sexp ⟨exponential f,exponential_mem_domain TW f⟩ = exponential (SW TW Jcandidate f) := by
  change JF (canonicalLift ⟨exponential f,exponential_mem_domain TW f⟩) = _
  rw [canonicalLift_exponential,JF_exponential]
  rfl

end F1Fecho.ExponentialTomita
#print axioms F1Fecho.ExponentialTomita.TW_SW
#print axioms F1Fecho.ExponentialTomita.coreGraph_flipJ
#print axioms F1Fecho.ExponentialTomita.closedGraph_flipJ
#print axioms F1Fecho.ExponentialTomita.Sexp_maps_domain
#print axioms F1Fecho.ExponentialTomita.Sexp_involutive
#print axioms F1Fecho.ExponentialTomita.Sexp_graph_iff
#print axioms F1Fecho.ExponentialTomita.Sexp_closed
#print axioms F1Fecho.ExponentialTomita.Sexp_dense
#print axioms F1Fecho.ExponentialTomita.Sexp_exponential
