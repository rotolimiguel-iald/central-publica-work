import ModularEigenRecognition

set_option autoImplicit false
set_option maxHeartbeats 1800000

namespace ChatgptAudit.Commutation032
open TGLExt ChatgptAudit
noncomputable section

theorem bounded_selfadjoint_inner (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsSelfAdjoint B)
    (x y : TowerHilbert P) :
    inner ℂ (B x) y=inner ℂ x (B y) := by
  have hs : ContinuousLinearMap.adjoint B=B := hB.star_eq
  rw [←ContinuousLinearMap.adjoint_inner_right,hs]

theorem modular_fixed_commutes_with_flow (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hfixed : ∀ s : ℝ, modularConjugation P s B=B)
    (s : ℝ) (x : TowerHilbert P) :
    modularFlow P s (B x)=B (modularFlow P s x) := by
  have h := congrArg (fun A : TowerHilbert P →L[ℂ] TowerHilbert P =>
    A (modularFlow P s x)) (hfixed s)
  change modularFlow P s (B (modularFlow P (-s) (modularFlow P s x)))=
    B (modularFlow P s x) at h
  rw [modularFlow_inverse] at h
  exact h

theorem flow_commuting_modular_fixed (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hcomm : ∀ (s : ℝ) (x : TowerHilbert P),
      modularFlow P s (B x)=B (modularFlow P s x))
    (s : ℝ) : modularConjugation P s B=B := by
  ext x
  change modularFlow P s (B (modularFlow P (-s) x))=B x
  rw [hcomm,modularFlow_group,add_neg_cancel,modularFlow_zero_time]

theorem commuting_operator_delta_eigen_graph (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hcomm : ∀ (s : ℝ) (x : TowerHilbert P),
      modularFlow P s (B x)=B (modularFlow P s x))
    (N : ℕ) (i j : chainIdx N) :
    (B (localEigenvector P N i j),
      (localEigenvalue P N i j : ℂ) • B (localEigenvector P N i j))∈
        (towerDeltaClosed P).graph := by
  have hx (s : ℝ) :
      modularFlow P s (B (localEigenvector P N i j))=
        modularPhase s (Real.log (localEigenvalue P N i j)) •
          B (localEigenvector P N i j) := by
    rw [hcomm,modularFlow_eigenvector,map_smul]
  have h := flow_eigen_implies_delta_graph P (Real.log (localEigenvalue P N i j))
    (B (localEigenvector P N i j)) hx
  simpa only [Real.exp_log (localEigenvalue_pos (P := P) N i j)] using h

theorem commuting_operator_delta_graph (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsSelfAdjoint B)
    (hcomm : ∀ (s : ℝ) (x : TowerHilbert P),
      modularFlow P s (B x)=B (modularFlow P s x))
    (x : (towerDeltaClosed P).domain) :
    (B (x : TowerHilbert P),B (towerDeltaClosed P x))∈(towerDeltaClosed P).graph := by
  apply weak_delta_mem_graph
  apply weak_delta_of_eigen_tests (P := P)
  intro N i j
  let v := localEigenvector P N i j
  let w := localEigenvalue P N i j
  have hg := commuting_operator_delta_eigen_graph P B hcomm N i j
  rw [LinearPMap.mem_graph_iff] at hg
  obtain ⟨z,hz,hy⟩ := hg
  change (z : TowerHilbert P)=B v at hz
  change towerDeltaClosed P z=(w : ℂ) • B v at hy
  change inner ℂ v (B (towerDeltaClosed P x))=
    inner ℂ ((w : ℂ) • v) (B (x : TowerHilbert P))
  calc
    _=inner ℂ (B v) (towerDeltaClosed P x) :=
      (bounded_selfadjoint_inner P B hB v (towerDeltaClosed P x)).symm
    _=inner ℂ (z : TowerHilbert P) (towerDeltaClosed P x) := by rw [hz]
    _=inner ℂ (towerDeltaClosed P z) (x : TowerHilbert P) :=
      (delta_is_symmetric (P := P) z x).symm
    _=inner ℂ ((w : ℂ) • B v) (x : TowerHilbert P) := by rw [hy]
    _=inner ℂ (B ((w : ℂ) • v)) (x : TowerHilbert P) := by rw [map_smul]
    _=_ := bounded_selfadjoint_inner P B hB ((w : ℂ) • v) (x : TowerHilbert P)

theorem commuting_operator_preserves_delta_domain (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsSelfAdjoint B)
    (hcomm : ∀ (s : ℝ) (x : TowerHilbert P),
      modularFlow P s (B x)=B (modularFlow P s x))
    (x : TowerHilbert P) (hx : x∈(towerDeltaClosed P).domain) :
    B x∈(towerDeltaClosed P).domain :=
  LinearPMap.mem_domain_of_mem_graph (commuting_operator_delta_graph P B hB hcomm ⟨x,hx⟩)

theorem commuting_operator_delta_apply (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsSelfAdjoint B)
    (hcomm : ∀ (s : ℝ) (x : TowerHilbert P),
      modularFlow P s (B x)=B (modularFlow P s x))
    (x : (towerDeltaClosed P).domain) :
    towerDeltaClosed P
      ⟨B (x : TowerHilbert P),
        commuting_operator_preserves_delta_domain P B hB hcomm (x : TowerHilbert P) x.property⟩=
      B (towerDeltaClosed P x) := by
  have hg := commuting_operator_delta_graph P B hB hcomm x
  rw [LinearPMap.mem_graph_iff] at hg
  obtain ⟨z,hz,hy⟩ := hg
  have he : z=
      (⟨B (x : TowerHilbert P),
        commuting_operator_preserves_delta_domain P B hB hcomm (x : TowerHilbert P) x.property⟩ :
          (towerDeltaClosed P).domain) := Subtype.ext hz
  rw [←he]
  exact hy

theorem modular_fixed_delta_graph (P : SiteProfile)
    (B : TowerHilbert P →L[ℂ] TowerHilbert P) (hB : IsSelfAdjoint B)
    (hfixed : ∀ s : ℝ, modularConjugation P s B=B)
    (x : (towerDeltaClosed P).domain) :
    (B (x : TowerHilbert P),B (towerDeltaClosed P x))∈(towerDeltaClosed P).graph :=
  commuting_operator_delta_graph P B hB (modular_fixed_commutes_with_flow P B hfixed) x

#print axioms bounded_selfadjoint_inner
#print axioms modular_fixed_commutes_with_flow
#print axioms flow_commuting_modular_fixed
#print axioms commuting_operator_delta_eigen_graph
#print axioms commuting_operator_delta_graph
#print axioms commuting_operator_preserves_delta_domain
#print axioms commuting_operator_delta_apply
#print axioms modular_fixed_delta_graph

end
end ChatgptAudit.Commutation032
