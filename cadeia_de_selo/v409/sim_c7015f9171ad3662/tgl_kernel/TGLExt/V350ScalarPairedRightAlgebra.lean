import TGLExt.V350ScalarCommutantSandwich

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1500000

namespace TGLV350.Regular
open TGLExt Filter
open scoped Topology
noncomputable section

private theorem pairedStarZero {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] :
    star (0 : H →L[ℂ] H) = 0 := map_zero ContinuousLinearMap.adjoint

private theorem pairedStarAdd {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (R S : H →L[ℂ] H) :
    star (R+S) = star R + star S := map_add ContinuousLinearMap.adjoint R S

private theorem pairedStarMul {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (R S : H →L[ℂ] H) :
    star (R*S) = star S * star R := ContinuousLinearMap.adjoint_comp R S

private theorem pairedStarInvolutive {H : Type*} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (R : H →L[ℂ] H) :
    star (star R) = R := ContinuousLinearMap.adjoint_adjoint R

def scalarRightAdjointPair_zero (P : SiteProfile) : ScalarRightAdjointPair P 0 where
  vector := 0
  adjointVector := 0
  right := by intro a; simp only [zero_apply,map_zero]
  adjoint := by
    intro a
    rw [pairedStarZero (H := ScalarGNSHilbert P)]
    simp only [zero_apply,map_zero]

def scalarRightAdjointPair_add {P : SiteProfile}
    {R S : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P}
    (d : ScalarRightAdjointPair P R) (e : ScalarRightAdjointPair P S) :
    ScalarRightAdjointPair P (R+S) where
  vector := d.vector+e.vector
  adjointVector := d.adjointVector+e.adjointVector
  right := by
    intro a
    change R (scalarWeightGNSEmbedding P a)+S (scalarWeightGNSEmbedding P a) = _
    exact (congrArg₂ (fun x y : ScalarGNSHilbert P => x+y) (d.right a) (e.right a)).trans
      ((scalarGNSRepresentation P a.val).map_add _ _).symm
  adjoint := by
    intro a
    rw [pairedStarAdd R S]
    change star R (scalarWeightGNSEmbedding P a)+star S (scalarWeightGNSEmbedding P a) = _
    exact (congrArg₂ (fun x y : ScalarGNSHilbert P => x+y) (d.adjoint a) (e.adjoint a)).trans
      ((scalarGNSRepresentation P a.val).map_add _ _).symm

def scalarRightAdjointPair_smul {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P}
    (d : ScalarRightAdjointPair P R) (c : ℂ) : ScalarRightAdjointPair P (c • R) where
  vector := c • d.vector
  adjointVector := star c • d.adjointVector
  right := by
    intro a
    change c • R (scalarWeightGNSEmbedding P a) = _
    exact (congrArg (fun x : ScalarGNSHilbert P => c • x) (d.right a)).trans
      ((scalarGNSRepresentation P a.val).map_smul c d.vector).symm
  adjoint := by
    intro a
    rw [StarModule.star_smul]
    change star c • star R (scalarWeightGNSEmbedding P a) = _
    exact (congrArg (fun x : ScalarGNSHilbert P => star c • x) (d.adjoint a)).trans
      ((scalarGNSRepresentation P a.val).map_smul (star c) d.adjointVector).symm

def scalarRightAdjointPair_mul {P : SiteProfile}
    {R S : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P}
    (d : ScalarRightAdjointPair P R) (e : ScalarRightAdjointPair P S) :
    ScalarRightAdjointPair P (R*S) where
  vector := R e.vector
  adjointVector := star S d.adjointVector
  right := by
    intro a
    change R (S (scalarWeightGNSEmbedding P a)) = _
    have hc := scalarRightBounded_commutes P R (scalarRightAdjointPair_rightBounded d) a.val
    exact (congrArg R (e.right a)).trans
      (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => B e.vector) hc.eq)
  adjoint := by
    intro a
    rw [pairedStarMul R S]
    change star S (star R (scalarWeightGNSEmbedding P a)) = _
    have hc := scalarRightBounded_commutes P (star S)
      (scalarRightAdjointPair_adjoint_rightBounded e) a.val
    exact (congrArg (fun x : ScalarGNSHilbert P => star S x) (d.adjoint a)).trans
      (congrArg (fun B : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P => B d.adjointVector) hc.eq)

def scalarRightAdjointPair_star {P : SiteProfile}
    {R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P}
    (d : ScalarRightAdjointPair P R) : ScalarRightAdjointPair P (star R) where
  vector := d.adjointVector
  adjointVector := d.vector
  right := d.adjoint
  adjoint := by intro a; rw [pairedStarInvolutive R]; exact d.right a

/-- An actual nonunital star algebra of bounded OPERATORS with right pairs.
No claim of a full left Hilbert algebra or of graph-core density for F. -/
def scalarPairedRightAlgebra (P : SiteProfile) :
    NonUnitalStarSubalgebra ℂ (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) where
  carrier := {R | Nonempty (ScalarRightAdjointPair P R)}
  zero_mem' := ⟨scalarRightAdjointPair_zero P⟩
  add_mem' := by rintro _ _ ⟨d⟩ ⟨e⟩; exact ⟨scalarRightAdjointPair_add d e⟩
  mul_mem' := by rintro _ _ ⟨d⟩ ⟨e⟩; exact ⟨scalarRightAdjointPair_mul d e⟩
  smul_mem' := by rintro c _ ⟨d⟩; exact ⟨scalarRightAdjointPair_smul d c⟩
  star_mem' := by rintro _ ⟨d⟩; exact ⟨scalarRightAdjointPair_star d⟩

def scalarGNSCommutant (P : SiteProfile) : VonNeumannAlgebra (ScalarGNSHilbert P) where
  toStarSubalgebra := StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P))
  centralizer_centralizer' := by simp

theorem scalarPairedRightAlgebra_mem_commutant (P : SiteProfile)
    (R : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P) (hR : R ∈ scalarPairedRightAlgebra P) :
    R ∈ scalarGNSCommutant P := by
  obtain ⟨d⟩ := hR
  exact scalarRightBounded_commutant_mem P R (scalarRightAdjointPair_rightBounded d)

/-- The operator star algebra of genuine right pairs generates the ENTIRE
commutant in the same representation. It is not yet identified with J*pi(N)*J. -/
theorem scalarPairedRightAlgebra_generated_eq_commutant (P : SiteProfile) :
    generatedAlgebra (scalarPairedRightAlgebra P : Set _) = scalarGNSCommutant P := by
  apply le_antisymm
  · exact generated_minimal _ _ (fun R hR => scalarPairedRightAlgebra_mem_commutant P R hR)
  · intro T hT
    obtain ⟨ha,_,ht,_⟩ := scalarCommutant_paired_right_approximation P T hT
    apply vonNeumann_mem_of_strong_limit (generatedAlgebra (scalarPairedRightAlgebra P : Set _))
      (fun h : ℝ => scalarCommutantSandwich P T h) T _ ht
    exact ha.mono (fun h hh => generator_mem hh)

#print axioms scalarRightAdjointPair_zero
#print axioms scalarRightAdjointPair_add
#print axioms scalarRightAdjointPair_smul
#print axioms scalarRightAdjointPair_mul
#print axioms scalarRightAdjointPair_star
#print axioms scalarPairedRightAlgebra
#print axioms scalarGNSCommutant
#print axioms scalarPairedRightAlgebra_mem_commutant
#print axioms scalarPairedRightAlgebra_generated_eq_commutant
end
end TGLV350.Regular
