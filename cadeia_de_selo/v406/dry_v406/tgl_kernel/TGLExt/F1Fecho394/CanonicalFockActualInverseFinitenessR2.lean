import TGLExt.F1Fecho394.CanonicalFockActualInverseAdditivityR2
import TGLExt.F1Fecho394.CanonicalFockActualTracialExtensionR1
import TGLExt.F1Fecho394.GeneralInverseFiniteApproximationR1

/-! DECLARADO / UNCOMPILED CANDIDATE, R50, 2026-10-16.
Concrete domain bound and finite-positive-minorants identity on the SAME Fock
core and inverseSupremum. The argument of the older candidate
CanonicalFockInverseFinitenessR3 is reused, preserving that file. No compiled
receipt for R3 was found in the OUT search; this file does not import it.
Actual right membership and perturbed order are supplied by compiled concrete
lemmas. The old hreg parameter disappears. CFC/product/scalar rewrites are
performed generically before specialization with native dictionaries.
The finite-minorants theorem in GeneralInverseFiniteApproximationR1 consumes
the proved domain bound and R49 traciality. It already contains the bodies of
GeneralInverseFiniteMinorantsR3 and GeneralInverseFiniteContractionsR3, so
those overlapping standalone modules are not imported a second time.
No total trace extension or PF is defined here. Four axiom reports required. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
set_option maxErrors 10
noncomputable section
namespace F1Fecho.CanonicalFockActualInverseFinitenessR2
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockRegular (core fockFlow M)
open F1Fecho.CanonicalFockWeight (PositiveInput regularFockVacuum)
open F1Fecho.CanonicalFockWeightDomain (scalarWeightLeftIdeal)
open F1Fecho.CanonicalFockGNS (GNSHilbert GNSSubspace)
open F1Fecho.CanonicalFockPolarRight (scalarPolarRightAlgebra)
open F1Fecho.CanonicalFockWeightPolar (scalarTomitaPolarFactor)
open F1Fecho.CanonicalFockActualRightCutoffs
open F1Fecho.RegularPositiveFlow
open F1Fecho.RegularInverseWeight
open scoped ENNReal

private abbrev nativeNormedAddCommGroup : NormedAddCommGroup GNSHilbert := inferInstance
private abbrev nativeInnerProductSpace : InnerProductSpace ℂ GNSHilbert := inferInstance
private abbrev nativeNormedSpace : NormedSpace ℂ GNSHilbert := inferInstance
private abbrev nativeModule : Module ℂ GNSHilbert := inferInstance
private abbrev nativeTopologicalSpace : TopologicalSpace GNSHilbert := inferInstance
private abbrev nativeUniformSpace : UniformSpace GNSHilbert := inferInstance
private abbrev nativeCompleteSpace : CompleteSpace GNSHilbert :=
  F1Fecho.CanonicalFockGNS.gnsCompleteSpace
private abbrev nativeStar : Star (GNSHilbert →L[ℂ] GNSHilbert) :=
  F1Fecho.ClosedSubmoduleRestriction.endomorphismStar GNSSubspace
attribute [local instance] nativeNormedAddCommGroup nativeInnerProductSpace
  nativeNormedSpace nativeModule nativeTopologicalSpace nativeUniformSpace
  nativeCompleteSpace nativeStar

private abbrev AmbientHilbert := RegularHilbert F1Rede.BosonicFock.F
private abbrev ambientNormedAddCommGroup : NormedAddCommGroup AmbientHilbert := inferInstance
private abbrev ambientInnerProductSpace : InnerProductSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientNormedSpace : NormedSpace ℂ AmbientHilbert := inferInstance
private abbrev ambientModule : Module ℂ AmbientHilbert := inferInstance
private abbrev ambientTopologicalSpace : TopologicalSpace AmbientHilbert := inferInstance
private abbrev ambientUniformSpace : UniformSpace AmbientHilbert := inferInstance
private abbrev ambientCompleteSpace : CompleteSpace AmbientHilbert := inferInstance
private abbrev ambientStar : Star (AmbientHilbert →L[ℂ] AmbientHilbert) := inferInstance
private abbrev ambientOrder : PartialOrder (AmbientHilbert →L[ℂ] AmbientHilbert) :=
  ContinuousLinearMap.instLoewnerPartialOrder (𝕜 := ℂ) (E := AmbientHilbert)
attribute [local instance] ambientNormedAddCommGroup ambientInnerProductSpace
  ambientNormedSpace ambientModule ambientTopologicalSpace ambientUniformSpace
  ambientCompleteSpace ambientStar ambientOrder
private abbrev fockNormedAddCommGroup : NormedAddCommGroup F1Rede.BosonicFock.F := inferInstance
private abbrev fockInnerProductSpace : InnerProductSpace ℂ F1Rede.BosonicFock.F := inferInstance
private abbrev fockCompleteSpace : CompleteSpace F1Rede.BosonicFock.F := inferInstance

private theorem hilbert_sqrt_mul_star {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (R : H →L[ℂ] H) (hR : 0 ≤ R) :
    hilbertPositiveSqrt R * star (hilbertPositiveSqrt R) = R := by
  change CFC.sqrt R * star (CFC.sqrt R) = R
  rw [(CFC.sqrt_nonneg R).isSelfAdjoint.star_eq,CFC.sqrt_mul_sqrt_self R hR]

private theorem scalar_root_unit_square {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (r : ℝ) (hr : 0 ≤ r) :
    ((Real.sqrt r : ℂ) • (1 : H →L[ℂ] H)) *
      star ((Real.sqrt r : ℂ) • (1 : H →L[ℂ] H)) = (r : ℂ) • 1 := by
  have hc : (Real.sqrt r : ℂ)*(Real.sqrt r : ℂ) = (r : ℂ) := by
    exact_mod_cast Real.mul_self_sqrt hr
  simp only [star_smul,Complex.star_def,Complex.conj_ofReal,star_one,
    smul_mul_assoc,mul_smul_comm,smul_smul,hc,one_mul]

private theorem scalar_root_sandwich {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (r : ℝ) (hr : 0 ≤ r) (A : H →L[ℂ] H) :
    star ((Real.sqrt r : ℂ) • (1 : H →L[ℂ] H)) * A *
      ((Real.sqrt r : ℂ) • (1 : H →L[ℂ] H)) = (r : ℂ) • A := by
  have hc : (Real.sqrt r : ℂ)*(Real.sqrt r : ℂ) = (r : ℂ) := by
    exact_mod_cast Real.mul_self_sqrt hr
  simp only [star_smul,Complex.star_def,Complex.conj_ofReal,star_one,
    smul_mul_assoc,mul_smul_comm,smul_smul,hc,one_mul,mul_one]

private theorem core_cut_product_order {H : Type}
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (N : StarSubalgebra ℂ (H →L[ℂ] H)) (q s c : N) (R : H →L[ℂ] H) (r : ℂ)
    (hq : star q.val = q.val) (hs : s.val*star s.val = R)
    (hc : c.val*star c.val = r • 1) (hcomm : Commute R q.val)
    (hbound : R*q.val*q.val ≤ r • 1) :
    (q*s)*star (q*s) ≤ c*star c := by
  change (q.val*s.val)*star (q.val*s.val) ≤ c.val*star c.val
  rw [hc]
  calc
    _ = q.val*(s.val*star s.val)*q.val := by simp only [star_mul,hq,mul_assoc]
    _ = q.val*R*q.val := by rw [hs]
    _ = R*q.val*q.val := by rw [← hcomm.eq]
    _ ≤ _ := hbound

private theorem sandwich_reassociate {A : Type*} [Ring A] [StarRing A] (a q s : A) :
    star s*(star (a*q)*(a*q))*s = star (q*s)*(star a*a)*(q*s) := by
  simp only [star_mul,mul_assoc]

theorem domainCut_right (d : ℝ) (hd : 0 < d) :
    regularDomainCut fockFlow M d ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor :=
  (scalarPolarRightAlgebra scalarTomitaPolarFactor).sub_mem
    (scalarPolarRightAlgebra scalarTomitaPolarFactor).one_mem
    ((scalarPolarRightAlgebra scalarTomitaPolarFactor).smul_mem
      (actualInverseCutoff_right d hd) _)
#print axioms domainCut_right

theorem domainCut_bound (d : ℝ) (hd : 0 < d) (a : scalarWeightLeftIdeal) :
    inverseSupremum fockFlow regularFockVacuum
      (star (a.val.val*(regularDomainCut fockFlow M d).val)*
        (a.val.val*(regularDomainCut fockFlow M d).val)) ≤
      ENNReal.ofReal d⁻¹ * dualQuadraticIntegral (star a.val.val*a.val.val) regularFockVacuum := by
  let q := regularDomainCut fockFlow M d
  have hq := domainCut_right d hd
  have hqstar : star q.val = q.val :=
    (regularDomainCut_bounds fockFlow M d hd).1.isSelfAdjoint.star_eq
  let c : core.toStarSubalgebra := (Real.sqrt d⁻¹ : ℂ) • 1
  have hc : c ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor :=
    (scalarPolarRightAlgebra scalarTomitaPolarFactor).smul_mem
      (scalarPolarRightAlgebra scalarTomitaPolarFactor).one_mem _
  have hcc : c.val*star c.val = ((d⁻¹ : ℝ) : ℂ) • 1 :=
    @scalar_root_unit_square AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace d⁻¹ (inv_nonneg.mpr hd.le)
  apply iSup_le
  intro e
  let hs := actualInverseCutoff_root_right e.val e.property
  let s : core.toStarSubalgebra :=
    ⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff fockFlow e.val),hs.choose⟩
  have hrs : s ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor := hs.choose_spec
  let b := q*s
  have hb : b ∈ scalarPolarRightAlgebra scalarTomitaPolarFactor :=
    (scalarPolarRightAlgebra scalarTomitaPolarFactor).mul_mem hq hrs
  have hss : s.val*star s.val = regularInverseGeneratorCutoff fockFlow e.val :=
    @hilbert_sqrt_mul_star AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace _
      (regularInverseGeneratorCutoff_nonneg fockFlow e.val e.property)
  have hproduct : regularInverseGeneratorCutoff fockFlow e.val*q.val*q.val ≤
      ((d⁻¹ : ℝ) : ℂ) • 1 := by
    simpa only [Complex.ofReal_inv] using
      (regularDomainCut_product_bound fockFlow M e.val d e.property hd)
  have hbc : b*star b ≤ c*star c :=
    @core_cut_product_order AmbientHilbert ambientNormedAddCommGroup
      ambientInnerProductSpace ambientCompleteSpace core.toStarSubalgebra q s c
      (regularInverseGeneratorCutoff fockFlow e.val) ((d⁻¹ : ℝ) : ℂ) hqstar hss hcc
      (regularDomainCut_commutes fockFlow M e.val d e.property hd) hproduct
  have hm := F1Fecho.CanonicalFockActualInverseAdditivityR2.scalarWeight_right_perturbed_mono
    scalarTomitaPolarFactor b c hb hc hbc a
  calc
    cutoffWeight fockFlow regularFockVacuum e.val (star (a.val.val*q.val)*(a.val.val*q.val)) =
        dualQuadraticIntegral (star b.val*(star a.val.val*a.val.val)*b.val) regularFockVacuum := by
      apply congrArg (fun V => dualQuadraticIntegral V regularFockVacuum)
      exact sandwich_reassociate a.val.val q.val s.val
    _ ≤ dualQuadraticIntegral (star c.val*(star a.val.val*a.val.val)*c.val) regularFockVacuum := hm
    _ = ENNReal.ofReal d⁻¹ * dualQuadraticIntegral (star a.val.val*a.val.val) regularFockVacuum := by
      have he : star c.val*(star a.val.val*a.val.val)*c.val =
          ((d⁻¹ : ℝ) : ℂ) • (star a.val.val*a.val.val) :=
        @scalar_root_sandwich AmbientHilbert ambientNormedAddCommGroup
          ambientInnerProductSpace ambientCompleteSpace d⁻¹ (inv_nonneg.mpr hd.le) _
      exact (congrArg (fun V => dualQuadraticIntegral V regularFockVacuum) he).trans
        (dualQuadraticIntegral_smul_operator d⁻¹ (inv_nonneg.mpr hd.le) _ regularFockVacuum)
#print axioms domainCut_bound

theorem domainCut_bound_all (a : core.toStarSubalgebra) (d : ℝ) (hd : 0 < d) :
    inverseSupremum fockFlow regularFockVacuum
      (star (a.val*(regularDomainCut fockFlow M d).val)*
        (a.val*(regularDomainCut fockFlow M d).val)) ≤
      ENNReal.ofReal d⁻¹ * dualQuadraticIntegral (star a.val*a.val) regularFockVacuum := by
  by_cases hf : dualQuadraticIntegral (star a.val*a.val) regularFockVacuum < ⊤
  · exact domainCut_bound d hd ⟨a,hf⟩
  · have ht : dualQuadraticIntegral (star a.val*a.val) regularFockVacuum = ⊤ := top_le_iff.mp (le_of_not_gt hf)
    have hc : ENNReal.ofReal d⁻¹ ≠ 0 := ne_of_gt (ENNReal.ofReal_pos.mpr (inv_pos.mpr hd))
    simp only [ht,ENNReal.mul_top hc,le_top]
#print axioms domainCut_bound_all

theorem value_finite_minorants (X : PositiveInput) :
    F1Fecho.CanonicalFockInverseSupremum.value X =
      ⨆ (Y : PositiveInput) (_ : Y.val ≤ X.val)
        (_ : F1Fecho.CanonicalFockInverseSupremum.value Y < ⊤),
        F1Fecho.CanonicalFockInverseSupremum.value Y := by
  have hmain := @inverseSupremum_finite_minorants_of_domain_bound
    F1Rede.BosonicFock.F fockNormedAddCommGroup fockInnerProductSpace fockCompleteSpace
    fockFlow M regularFockVacuum domainCut_bound_all
    F1Fecho.CanonicalFockActualTracialExtensionR1.inverseSupremum_tracial
    ⟨X.val,X.property.1⟩ X.property.2
  apply le_antisymm
  · calc
      F1Fecho.CanonicalFockInverseSupremum.value X =
          ⨆ (Y : core.toStarSubalgebra) (_ : 0 ≤ Y.val) (_ : Y.val ≤ X.val)
            (_ : inverseSupremum fockFlow regularFockVacuum Y.val < ⊤),
            inverseSupremum fockFlow regularFockVacuum Y.val := hmain
      _ ≤ _ := by
        apply iSup_le
        intro Y
        apply iSup_le
        intro hp
        apply iSup_le
        intro hYX
        apply iSup_le
        intro hf
        let Z : PositiveInput := ⟨Y.val,Y.property,hp⟩
        exact le_iSup_of_le Z (le_iSup_of_le hYX (le_iSup_of_le hf le_rfl))
  · apply iSup_le
    intro Y
    apply iSup_le
    intro hYX
    apply iSup_le
    intro _
    exact inverseSupremum_mono fockFlow regularFockVacuum Y.val X.val hYX
#print axioms value_finite_minorants

end F1Fecho.CanonicalFockActualInverseFinitenessR2
