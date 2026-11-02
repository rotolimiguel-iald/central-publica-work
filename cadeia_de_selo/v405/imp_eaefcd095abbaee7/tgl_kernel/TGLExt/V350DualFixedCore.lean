import TGLExt.V350DualResolventFixed

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1800000

namespace TGLV350.Regular
open Filter
open scoped Topology ENNReal
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The star commutant of an arbitrary set is a concrete von Neumann algebra. -/
def starCommutantAlgebra (S : Set (H →L[ℂ] H)) : VonNeumannAlgebra H where
  toStarSubalgebra := StarSubalgebra.centralizer ℂ S
  centralizer_centralizer' := by simp

theorem dualAmbient_fixed_iff_commutes (s : ℝ)
    (R : RegularHilbert H →L[ℂ] RegularHilbert H) :
    dualAmbient s R = R ↔ characterMultiplier s * R = R * characterMultiplier s := by
  constructor
  · intro h
    have hh := congrArg (fun B => B * characterMultiplier (H := H) s) h
    rw [dualAmbient_apply] at hh
    simpa only [mul_assoc,(characterMultiplier_unitary s).1,mul_one] using hh
  · intro h
    rw [dualAmbient_apply,h,mul_assoc,(characterMultiplier_unitary s).2,mul_one]

/-- N intersected with the commutant of the dual implementers, constructed
as one star commutant. This does not identify it with the original base. -/
def dualFixedCore (P : TGLExt.SiteProfile) :
    VonNeumannAlgebra (RegularHilbert (TGLExt.TowerHilbert P)) :=
  starCommutantAlgebra
    (((regularCoreAlgebra P).commutant : Set
        (RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))) ∪
      Set.range (characterMultiplier (H := TGLExt.TowerHilbert P)))

theorem dualFixedCore_mem_iff (P : TGLExt.SiteProfile)
    (R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P)) :
    R ∈ dualFixedCore P ↔ R ∈ regularCoreAlgebra P ∧ ∀ s : ℝ, dualAmbient s R = R := by
  change R ∈ StarSubalgebra.centralizer ℂ _ ↔ _
  rw [StarSubalgebra.mem_centralizer_iff]
  constructor
  · intro h
    constructor
    · rw [← VonNeumannAlgebra.commutant_commutant (regularCoreAlgebra P),
        VonNeumannAlgebra.mem_commutant_iff]
      intro B hB
      exact (h B (Or.inl hB)).1
    · intro s
      exact (dualAmbient_fixed_iff_commutes s R).mpr (h _ (Or.inr ⟨s,rfl⟩)).1
  · rintro ⟨hR,hfixed⟩ B hB
    rcases hB with hB | ⟨s,rfl⟩
    · have hRc : R ∈ (regularCoreAlgebra P).commutant.commutant := by
        rwa [VonNeumannAlgebra.commutant_commutant]
      have hc := VonNeumannAlgebra.mem_commutant_iff.mp hRc
      exact ⟨hc B hB,hc (star B) (star_mem hB)⟩
    · refine ⟨(dualAmbient_fixed_iff_commutes s R).mp (hfixed s), ?_⟩
      rw [characterMultiplier_star]
      exact (dualAmbient_fixed_iff_commutes (-s) R).mp (hfixed (-s))

theorem amplified_factor_mem_dualFixedCore (P : TGLExt.SiteProfile)
    (B : TGLExt.TowerHilbert P →L[ℂ] TGLExt.TowerHilbert P)
    (hB : B ∈ TGLExt.theFactorObject P) : fibre B ∈ dualFixedCore P :=
  (dualFixedCore_mem_iff P (fibre B)).mpr
    ⟨amplified_factor_mem P B hB,fun s => dualAmbient_fibre s B⟩

theorem dualResolvent_mem_dualFixedCore (P : TGLExt.SiteProfile)
    (A R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hA : 0 ≤ A) (hmR : R ∈ regularCoreAlgebra P)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) :
    R ∈ dualFixedCore P :=
  (dualFixedCore_mem_iff P R).mpr ⟨hmR,dualResolvent_limit_dual_fixed A R hA hlim⟩

/-- The fixed resolvent and the full form representation share the same
R,T,S. The output is not a pairing of unrelated existence statements. -/
theorem exists_dualFixedFormRepresentation (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P))
    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ] RegularHilbert (TGLExt.TowerHilbert P),
    ∃ T S : dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA,
      R ∈ dualFixedCore P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      T.IsClosed ∧ Dense (T.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint T ∧
      S.IsClosed ∧ Dense (S.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint S ∧
      (∀ x : S.domain, 0 ≤ (inner ℂ (x : dualFormSupport A hA) (S x)).re) ∧
      partialOperatorSquare S = T ∧
      (∀ w : RegularHilbert (TGLExt.TowerHilbert P), dualQuadraticIntegral A w < ⊤ ↔
        ∃ x : S.domain, ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = w) ∧
      (∀ x : S.domain, dualQuadraticIntegral A (x : dualFormSupport A hA) =
        ENNReal.ofReal (‖S x‖^2)) ∧
      (∀ u : dualFormSupport A hA, ∃ x : T.domain,
        ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = R u ∧
        (x : dualFormSupport A hA) + T x = u) := by
  obtain ⟨R,T,S,hmR,hR,hone,hlim,hrest⟩ := exists_dualFormRepresentation P A hmem hA
  exact ⟨R,T,S,dualResolvent_mem_dualFixedCore P A R hA hmR hlim,hR,hone,hlim,hrest⟩

#print axioms starCommutantAlgebra
#print axioms dualAmbient_fixed_iff_commutes
#print axioms dualFixedCore
#print axioms dualFixedCore_mem_iff
#print axioms amplified_factor_mem_dualFixedCore
#print axioms dualResolvent_mem_dualFixedCore
#print axioms exists_dualFixedFormRepresentation
end
end TGLV350.Regular
