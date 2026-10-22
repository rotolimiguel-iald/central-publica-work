import TGLExt.V350ScalarPairedMultiplicationGraph
import TGLExt.V350HilbertProjectionOrder
import TGLExt.V350ScalarGNSVonNeumann

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000
set_option synthInstance.maxHeartbeats 200000

namespace TGLV350.Regular
open TGLExt WithLp
noncomputable section

private theorem centralizerGeneratedRightAlgebra {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) :
    Set.centralizer (generatedAlgebra (E : Set (H →L[ℂ] H)) : Set (H →L[ℂ] H)) = Set.centralizer (E : Set (H →L[ℂ] H)) := by
  change Set.centralizer (StarSubalgebra.centralizer ℂ
    (StarSubalgebra.centralizer ℂ (E : Set (H →L[ℂ] H)) : Set (H →L[ℂ] H)) : Set (H →L[ℂ] H)) = _
  rw [StarSubalgebra.coe_centralizer_centralizer,StarMemClass.star_coe_eq,
    Set.union_self,Set.centralizer_centralizer_centralizer]

private theorem centralizerOfRange {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (M : VonNeumannAlgebra H) (r : Set (H →L[ℂ] H)) (hr : r=(M : Set (H →L[ℂ] H))) :
    Set.centralizer (StarSubalgebra.centralizer ℂ r : Set (H →L[ℂ] H)) = (M : Set (H →L[ℂ] H)) := by
  rw [hr,StarSubalgebra.coe_centralizer,StarMemClass.star_coe_eq,
    Set.union_self,VonNeumannAlgebra.centralizer_centralizer]

theorem scalarPairedRightAlgebra_centralizer (P : SiteProfile) :
    Set.centralizer (scalarPairedRightAlgebra P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) =
      (scalarGNSVonNeumann P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) := by
  have hc : Set.centralizer (scalarGNSCommutant P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) = (scalarGNSVonNeumann P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) := by
    change Set.centralizer (StarSubalgebra.centralizer ℂ (Set.range (scalarGNSRepresentation P)) : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) = _
    exact centralizerOfRange (scalarGNSVonNeumann P) (Set.range (scalarGNSRepresentation P))
      (scalarGNSVonNeumann_coe P).symm
  calc
    _ = Set.centralizer (generatedAlgebra (scalarPairedRightAlgebra P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) :=
      (centralizerGeneratedRightAlgebra (scalarPairedRightAlgebra P)).symm
    _ = Set.centralizer (scalarGNSCommutant P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) :=
      congrArg (fun N : VonNeumannAlgebra (ScalarGNSHilbert P) => Set.centralizer (N : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)))
        (scalarPairedRightAlgebra_generated_eq_commutant P)
    _ = _ := hc

theorem scalarPairedCommutant_mem_GNS (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ a : scalarPairedRightAlgebra P, Commute T a.val) : T ∈ scalarGNSVonNeumann P := by
  have hm : T ∈ Set.centralizer (scalarPairedRightAlgebra P : Set (ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)) := by
    intro a ha
    exact (hT ⟨a,ha⟩).eq.symm
  exact (scalarPairedRightAlgebra_centralizer P).subset hm

theorem scalarPairedProjection_A_mem (P : SiteProfile) (η : ScalarGNSHilbert P) :
    hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection ∈ scalarGNSVonNeumann P := by
  apply scalarPairedCommutant_mem_GNS
  intro a
  exact hilbertBlockA_commutes _ a.val (scalarPairedMultiplicationGraph_projection_commutes P η a)

theorem scalarPairedProjection_B_mem (P : SiteProfile) (η : ScalarGNSHilbert P) :
    hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection ∈ scalarGNSVonNeumann P := by
  apply scalarPairedCommutant_mem_GNS
  intro a
  exact hilbertBlockB_commutes _ a.val (scalarPairedMultiplicationGraph_projection_commutes P η a)

theorem scalarPairedProjection_D_mem (P : SiteProfile) (η : ScalarGNSHilbert P) :
    hilbertBlockD (scalarPairedMultiplicationGraph P η).starProjection ∈ scalarGNSVonNeumann P := by
  apply scalarPairedCommutant_mem_GNS
  intro a
  exact hilbertBlockD_commutes _ a.val (scalarPairedMultiplicationGraph_projection_commutes P η a)

theorem scalarPairedProjection_A_positive_contraction (P : SiteProfile) (η : ScalarGNSHilbert P) :
    0 ≤ hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection ∧
      hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection ≤ 1 :=
  ⟨hilbertBlockA_nonneg _,hilbertBlockA_le_one _⟩

private theorem subalgebraGraphBlockInjective {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (E : NonUnitalStarSubalgebra ℂ (H →L[ℂ] H)) (j f : E →ₗ[ℂ] H) (hj : DenseRange j) :
    Function.Injective (hilbertBlockA (complexGraphClosure j f).starProjection) :=
  complexGraph_blockA_injective j f hj

theorem scalarPairedProjection_A_injective (P : SiteProfile) (η : ScalarGNSHilbert P) :
    Function.Injective (hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection) := by
  refine subalgebraGraphBlockInjective (scalarPairedRightAlgebra P)
    (scalarRightPairVector P) (scalarPairedMultiplicationVector P η) ?_
  exact scalarRightPairVector_denseRange P

theorem scalarPairedProjection_BBstar (P : SiteProfile) (η : ScalarGNSHilbert P) :
    let S := scalarPairedMultiplicationGraph P η
    hilbertBlockB S.starProjection * star (hilbertBlockB S.starProjection) =
      hilbertBlockA S.starProjection * (1-hilbertBlockA S.starProjection) :=
  hilbertBlockB_mul_adjoint _

theorem scalarPairedProjection_BD (P : SiteProfile) (η : ScalarGNSHilbert P) :
    let S := scalarPairedMultiplicationGraph P η
    hilbertBlockB S.starProjection * hilbertBlockD S.starProjection =
      (1-hilbertBlockA S.starProjection) * hilbertBlockB S.starProjection :=
  hilbertBlockB_mul_D _

private theorem blockBFromFixed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (x y : H)
    (hp : S.starProjection (toLp 2 (x,y))=toLp 2 (x,y)) :
    hilbertBlockB S.starProjection y = (1-hilbertBlockA S.starProjection) x := by
  have he : toLp 2 (x,y)=hilbertPairInl x+hilbertPairInr y := by
    change toLp 2 (x,y)=toLp 2 (x+0,0+y)
    rw [add_zero,zero_add]
  have hj : (hilbertPairInl (H:=H)).adjoint (S.starProjection (toLp 2 (x,y))) =
      hilbertBlockA S.starProjection x + hilbertBlockB S.starProjection y := by
    rw [he,map_add,map_add]
    rfl
  have hx : (hilbertPairInl (H:=H)).adjoint (toLp 2 (x,y))=x := by
    rw [hilbertPairInl_adjoint_apply]
  exact eq_sub_of_add_eq' (hj.symm.trans ((congrArg (hilbertPairInl (H:=H)).adjoint hp).trans hx))

private theorem blockBadjointFromRotated {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    (S : Submodule ℂ (WithLp 2 (H × H))) [CompleteSpace S] (x y : H)
    (hp : S.starProjection (toLp 2 (y,-x))=0) :
    (hilbertBlockB S.starProjection).adjoint y = hilbertBlockD S.starProjection x := by
  have he : toLp 2 (y,-x)=hilbertPairInl y-hilbertPairInr x := by
    change toLp 2 (y,-x)=toLp 2 (y-0,0-x)
    rw [sub_zero,zero_sub]
  have hj : (hilbertPairInr (H:=H)).adjoint (S.starProjection (toLp 2 (y,-x))) =
      (hilbertBlockB S.starProjection).adjoint y-hilbertBlockD S.starProjection x := by
    rw [he,map_sub,map_sub,hilbertBlockB_adjoint]
    rfl
  exact sub_eq_zero.mp (hj.symm.trans
    ((congrArg (hilbertPairInr (H:=H)).adjoint hp).trans (map_zero _)))

theorem scalarPairedProjection_B_left (P : SiteProfile) (η : scalarClosedTomitaDomain P)
    (hη : scalarClosedTomita P η=(η:ScalarGNSHilbert P)) (a : scalarPairedRightAlgebra P) :
    hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection (scalarRightPairVector P a) =
      hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection (a.val η) :=
  hilbertBlockB_from_rotated _ _ _ (scalarPairedMultiplicationGraph_rotated_zero P η hη a)

theorem scalarPairedProjection_B_right (P : SiteProfile) (η : ScalarGNSHilbert P)
    (a : scalarPairedRightAlgebra P) :
    hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection (a.val η) =
      (1-hilbertBlockA (scalarPairedMultiplicationGraph P η).starProjection) (scalarRightPairVector P a) :=
  blockBFromFixed _ _ _ (scalarPairedMultiplicationGraph_projection_fixed P η a)

theorem scalarPairedProjection_Badjoint_right (P : SiteProfile) (η : scalarClosedTomitaDomain P)
    (hη : scalarClosedTomita P η=(η:ScalarGNSHilbert P)) (a : scalarPairedRightAlgebra P) :
    star (hilbertBlockB (scalarPairedMultiplicationGraph P η).starProjection) (a.val η) =
      hilbertBlockD (scalarPairedMultiplicationGraph P η).starProjection (scalarRightPairVector P a) :=
  blockBadjointFromRotated _ _ _ (scalarPairedMultiplicationGraph_rotated_zero P η hη a)

#print axioms scalarPairedRightAlgebra_centralizer
#print axioms scalarPairedCommutant_mem_GNS
#print axioms scalarPairedProjection_A_mem
#print axioms scalarPairedProjection_B_mem
#print axioms scalarPairedProjection_D_mem
#print axioms scalarPairedProjection_A_positive_contraction
#print axioms scalarPairedProjection_A_injective
#print axioms scalarPairedProjection_BBstar
#print axioms scalarPairedProjection_BD
#print axioms scalarPairedProjection_B_left
#print axioms scalarPairedProjection_B_right
#print axioms scalarPairedProjection_Badjoint_right
end
end TGLV350.Regular
