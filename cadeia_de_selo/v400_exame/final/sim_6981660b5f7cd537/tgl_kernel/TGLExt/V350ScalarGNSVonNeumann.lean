import TGLExt.V350SeparatingRestrictionVonNeumann
import TGLExt.V350ScalarGaussianUnitary
import TGLExt.V350ScalarGaussianClosureTransport

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt
noncomputable section

private theorem rangePreimageEquivalence {A B C : Type} (f : A → C) (g : B → C)
    (he : Set.range f = Set.range g) (z : C) :
    (∃ a, z = f a) ↔ ∃ b, z = g b := by
  constructor
  · rintro ⟨a,ha⟩
    have hz : z ∈ Set.range g := he ▸ ⟨a,ha.symm⟩
    obtain ⟨b,hb⟩ := hz
    exact ⟨b,hb.symm⟩
  · rintro ⟨b,hb⟩
    have hz : z ∈ Set.range f := he.symm ▸ ⟨b,hb.symm⟩
    obtain ⟨a,ha⟩ := hz
    exact ⟨a,ha.symm⟩

private theorem conjugatedRange {A X Y : Type} (e : X → Y) (f : A → X) (g : A → Y)
    (he : ∀ a, e (f a) = g a) : e '' Set.range f = Set.range g := by
  ext y
  constructor
  · rintro ⟨_,⟨a,rfl⟩,rfl⟩
    exact ⟨a,(he a).symm⟩
  · rintro ⟨a,rfl⟩
    exact ⟨f a,Set.mem_range_self a,he a⟩

private theorem transportedGeneratedPreimage {H K A : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
    (e : (H →L[ℂ] H) ≃⋆ₐ[ℂ] (K →L[ℂ] K))
    (f : A → (H →L[ℂ] H)) (g : A → (K →L[ℂ] K))
    (he : ∀ a, e (f a) = g a)
    (hg : ∀ B, B ∈ generatedAlgebra (Set.range g) ↔ ∃ a, B = g a)
    (B : H →L[ℂ] H) :
    B ∈ generatedAlgebra (Set.range f) ↔ ∃ a, B = f a := by
  constructor
  · intro hB
    have ht := (starEquiv_generated_transport e (Set.range f) B).mpr hB
    rw [conjugatedRange e f g he] at ht
    obtain ⟨a,ha⟩ := (hg _).mp ht
    exact ⟨a,e.injective (ha.trans (he a).symm)⟩
  · rintro ⟨a,rfl⟩
    exact generator_mem (Set.mem_range_self a)

private theorem actualImageEquality {A B : Type} (s : Set B) (f : A → B)
    (h : ∀ b, b ∈ s ↔ ∃ a, b = f a) : s = Set.range f := by
  ext b
  exact (h b).trans ⟨fun ⟨a,ha⟩ => ⟨a,ha.symm⟩,fun ⟨a,ha⟩ => ⟨a,ha.symm⟩⟩

theorem scalarGaussianImage_ambient_invariant (P : SiteProfile)
    (a : (dualOrbitVonNeumann (regularCoreAlgebra P)).toStarSubalgebra)
    (v : RegularHilbert (RegularHilbert (TowerHilbert P)))
    (hv : v ∈ scalarGaussianImage P) : a.val v ∈ scalarGaussianImage P := by
  obtain ⟨A,hA,he⟩ := (mem_dualOrbitVonNeumann_iff (regularCoreAlgebra P) a.val).mp a.property
  rw [he]
  exact scalarGaussianImage_invariant P ⟨A,hA⟩ v hv

def scalarGaussianRestrictedAmbientRepresentation (P : SiteProfile) :
    (dualOrbitVonNeumann (regularCoreAlgebra P)).toStarSubalgebra →⋆ₐ[ℂ]
      (scalarGaussianImage P →L[ℂ] scalarGaussianImage P) :=
  reducingStarRepresentation
    (dualOrbitVonNeumann (regularCoreAlgebra P)).toStarSubalgebra.subtype
    (scalarGaussianImage P) (scalarGaussianImage_ambient_invariant P)

theorem scalarGaussianRestrictedAmbient_dual (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) :
    scalarGaussianRestrictedAmbientRepresentation P
      ⟨dualOrbitRepresentation a.val,
        (mem_dualOrbitVonNeumann_iff (regularCoreAlgebra P) _).mpr ⟨a.val,a.property,rfl⟩⟩ =
      scalarGaussianImageRepresentation P a := by
  ext1 v
  rfl

theorem scalarGaussianRestrictedAmbient_range (P : SiteProfile) :
    Set.range (scalarGaussianRestrictedAmbientRepresentation P) =
      Set.range (scalarGaussianImageRepresentation P) := by
  ext B
  constructor
  · rintro ⟨a,rfl⟩
    obtain ⟨A,hA,he⟩ := (mem_dualOrbitVonNeumann_iff (regularCoreAlgebra P) a.val).mp a.property
    refine ⟨⟨A,hA⟩,?_⟩
    ext1 v
    apply Subtype.ext
    exact (congrArg (fun T : RegularHilbert (RegularHilbert (TowerHilbert P)) →L[ℂ]
      RegularHilbert (RegularHilbert (TowerHilbert P)) => T v.val) he).symm
  · rintro ⟨a,rfl⟩
    exact ⟨_,scalarGaussianRestrictedAmbient_dual P a⟩

/-- The auxiliary Gaussian image is bicommutant closed, with every ambient
membership hypothesis discharged for the actual regular core. -/
theorem scalarGaussianImage_generated_iff (P : SiteProfile)
    (B : scalarGaussianImage P →L[ℂ] scalarGaussianImage P) :
    B ∈ generatedAlgebra (Set.range (scalarGaussianImageRepresentation P)) ↔
      ∃ a : (regularCoreAlgebra P).toStarSubalgebra,
        B = scalarGaussianImageRepresentation P a := by
  rw [← scalarGaussianRestrictedAmbient_range P]
  have ht := mem_generated_restriction_iff
    (dualOrbitVonNeumann (regularCoreAlgebra P)) (scalarGaussianImage P)
    (scalarGaussianImage_ambient_invariant P)
    ⟨scalarGaussianVacuum P,scalarGaussianVacuum_mem_image P⟩
    (scalarGaussianImage_separating P) B
  change B ∈ generatedAlgebra (Set.range (scalarGaussianRestrictedAmbientRepresentation P)) ↔
    ∃ a, B = scalarGaussianRestrictedAmbientRepresentation P a at ht
  rw [ht]
  exact rangePreimageEquivalence
    (scalarGaussianRestrictedAmbientRepresentation P) (scalarGaussianImageRepresentation P)
    (scalarGaussianRestrictedAmbient_range P) B

theorem scalarGaussianUnitary_conjugates_representation (P : SiteProfile)
    (a : (regularCoreAlgebra P).toStarSubalgebra) :
    (scalarGaussianUnitary P).conjStarAlgEquiv (scalarGNSRepresentation P a) =
      scalarGaussianImageRepresentation P a := by
  ext1 v
  change scalarGaussianUnitary P
    (scalarGNSRepresentation P a ((scalarGaussianUnitary P).symm v)) = _
  rw [scalarGaussianUnitary_intertwines,(scalarGaussianUnitary P).apply_symm_apply]

theorem scalarGaussianUnitary_representation_image (P : SiteProfile) :
    (scalarGaussianUnitary P).conjStarAlgEquiv '' Set.range (scalarGNSRepresentation P) =
      Set.range (scalarGaussianImageRepresentation P) := by
  exact conjugatedRange (scalarGaussianUnitary P).conjStarAlgEquiv
    (scalarGNSRepresentation P) (scalarGaussianImageRepresentation P)
    (scalarGaussianUnitary_conjugates_representation P)

/-- The algebra is now proved to equal the actual scalar representation image.
This definition alone does not assert that fact; see mem_scalarGNSVonNeumann_iff. -/
def scalarGNSVonNeumann (P : SiteProfile) : VonNeumannAlgebra (ScalarGNSHilbert P) :=
  generatedAlgebra (Set.range (scalarGNSRepresentation P))

theorem mem_scalarGNSVonNeumann_iff (P : SiteProfile)
    (B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) :
    B ∈ scalarGNSVonNeumann P ↔
      ∃ a : (regularCoreAlgebra P).toStarSubalgebra, B = scalarGNSRepresentation P a := by
  exact transportedGeneratedPreimage (scalarGaussianUnitary P).conjStarAlgEquiv
    (scalarGNSRepresentation P) (scalarGaussianImageRepresentation P)
    (scalarGaussianUnitary_conjugates_representation P)
    (scalarGaussianImage_generated_iff P) B

theorem scalarGNSVonNeumann_coe (P : SiteProfile) :
    (scalarGNSVonNeumann P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) =
      Set.range (scalarGNSRepresentation P) := by
  exact actualImageEquality
    (scalarGNSVonNeumann P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P))
    (scalarGNSRepresentation P) (mem_scalarGNSVonNeumann_iff P)

#print axioms scalarGaussianImage_ambient_invariant
#print axioms scalarGaussianRestrictedAmbientRepresentation
#print axioms scalarGaussianRestrictedAmbient_dual
#print axioms scalarGaussianRestrictedAmbient_range
#print axioms scalarGaussianImage_generated_iff
#print axioms scalarGaussianUnitary_conjugates_representation
#print axioms scalarGaussianUnitary_representation_image
#print axioms scalarGNSVonNeumann
#print axioms mem_scalarGNSVonNeumann_iff
#print axioms scalarGNSVonNeumann_coe
end
end TGLV350.Regular
