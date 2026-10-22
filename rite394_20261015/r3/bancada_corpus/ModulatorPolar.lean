import ModulatorPositive

set_option autoImplicit false
set_option maxHeartbeats 2000000

namespace ChatgptAudit
open TGLExt
noncomputable section
variable {P : SiteProfile}

theorem closedTomita_injective : Function.Injective (closedTomita P) := by
  intro x y h
  have heq : (⟨closedTomita P x, closedTomita_maps_domain x⟩ : closedTomitaDomain P) =
      ⟨closedTomita P y, closedTomita_maps_domain y⟩ := Subtype.ext h
  have hi := congrArg (closedTomita P) heq
  rw [closedTomita_involutive, closedTomita_involutive] at hi
  exact Subtype.ext hi

theorem modulatorCandidate_injective :
    Function.Injective (fun x : closedTomitaDomain P => closedModulatorCandidate P x) := by
  intro x y h
  apply closedTomita_injective
  have hi := congrArg (towerJ P) h
  simpa only [candidate_factorization] using hi

theorem modulatorCandidate_denseRange :
    DenseRange (fun x : closedTomitaDomain P => closedModulatorCandidate P x) := by
  apply Dense.mono ?_ (towerPre_denseRange (P := P))
  rintro _ ⟨v, rfl⟩
  obtain ⟨N, a, rfl⟩ := exists_tof v
  let z : closedTomitaDomain P :=
    ⟨((tof P N (profileJlevel P N a) : TowerPre P) : TowerHilbert P),
      local_vector_mem_domain (profileJlevel P N a)⟩
  refine ⟨⟨closedTomita P z, closedTomita_maps_domain z⟩, ?_⟩
  change towerJ P (closedTomita P ⟨closedTomita P z, closedTomita_maps_domain z⟩) = _
  rw [closedTomita_involutive]
  change towerJ P ((tof P N (profileJlevel P N a) : TowerPre P) : TowerHilbert P) = _
  rw [← profileJpre_tof, ← towerJ_coe, towerJ_involutive]

/-- A parte positiva fechada da fatoração polar, agora com positividade e adjunto provados.
    A construção tipada do quadrado Δ e do cálculo espectral é uma obrigação separada. -/
abbrev towerDeltaHalfClosed (P : SiteProfile) := closedModulatorCandidate P

theorem tower_polar_decomposition (P : SiteProfile) :
    IsSelfAdjoint (towerDeltaHalfClosed P) ∧
    (∀ x : closedTomitaDomain P,
      0 ≤ (inner ℂ (x : TowerHilbert P) (towerDeltaHalfClosed P x)).re) ∧
    Function.Injective (fun x : closedTomitaDomain P => towerDeltaHalfClosed P x) ∧
    DenseRange (fun x : closedTomitaDomain P => towerDeltaHalfClosed P x) ∧
    (∀ x : closedTomitaDomain P,
      closedTomita P x = towerJ P (towerDeltaHalfClosed P x)) :=
  ⟨modulatorCandidate_selfadjoint, modulatorCandidate_positive,
    modulatorCandidate_injective, modulatorCandidate_denseRange,
    fun x => (candidate_factorization x).symm⟩

#print axioms modulatorCandidate_injective
#print axioms modulatorCandidate_denseRange
#print axioms tower_polar_decomposition
end
end ChatgptAudit
