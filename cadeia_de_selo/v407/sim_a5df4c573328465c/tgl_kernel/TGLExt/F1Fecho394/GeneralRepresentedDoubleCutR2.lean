import TGLExt.F1Fecho394.GeneralRepresentedRegularResolventR4
import TGLExt.F1Fecho394.GeneralRegularDomainCutR1
/-! Existing v393 cut-balance proof generalized to a representation of the
same regular core. The base modular balance, injectivities, flip and one
commutant relation remain explicit; concrete consumers must discharge them. -/
set_option autoImplicit false
set_option maxHeartbeats 2400000
noncomputable section
namespace F1Fecho.RepresentedDoubleCut
open TGLV350.Regular MeasureTheory Filter
open F1Fecho.RegularPositiveFlow F1Fecho.RegularCovariantCore
open scoped Topology
variable {H K : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]
local instance : NormedSpace ℂ (K →L[ℂ] K) := inferInstance
local instance : Module ℂ (K →L[ℂ] K) := ContinuousLinearMap.module
local instance : ContinuousFunctionalCalculus ℂ (K →L[ℂ] K) IsStarNormal :=
  IsStarNormal.instContinuousFunctionalCalculus (A := K →L[ℂ] K)
local instance : IsometricContinuousFunctionalCalculus ℂ (K →L[ℂ] K) IsStarNormal :=
  IsStarNormal.instIsometricContinuousFunctionalCalculus (A := K →L[ℂ] K)
local instance : SMulCommClass ℂ (K →L[ℂ] K) (K →L[ℂ] K) := ⟨by
  intro c a b
  ext1 x
  change c • a (b x) = a (c • b x)
  exact (a.map_smul c (b x)).symm⟩
local instance : IsScalarTower ℂ (K →L[ℂ] K) (K →L[ℂ] K) := ⟨by
  intro c a b
  ext1 x
  rfl⟩

open F1Fecho.RepresentedRegularResolvent
variable (Q : UnitaryFlow H) (M : VonNeumannAlgebra H)
variable (π : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra →⋆ₐ[ℂ] (K →L[ℂ] K))
def cutElement (δ : ℝ) : (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra :=
  ⟨F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff Q δ,F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_mem Q M δ⟩
theorem balance (T : K →L[ℂ] K) (J : K ≃ₛₗᵢ[starRingEnd ℂ] K)
    (hTA : Commute T (π (resolventElement Q M)))
    (hTB : Commute T (antiunitaryConjugate (H := K) J (π (resolventElement Q M))))
    (hiA : Function.Injective (π (resolventElement Q M)))
    (hiB : Function.Injective (antiunitaryConjugate (H := K) J (π (resolventElement Q M))))
    (hbase : (1-T)*π (resolventElement Q M)*
        (1-antiunitaryConjugate (H := K) J (π (resolventElement Q M))) =
      T*(1-π (resolventElement Q M))*antiunitaryConjugate (H := K) J (π (resolventElement Q M)))
    (hflip : antiunitaryConjugate (H := K) J T=1-T)
    (hcross : ∀ a, Commute (antiunitaryConjugate (H := K) J
      (π (resolventElement Q M))) (π a))
    (ε η : ℝ) (hε : 0<ε) (hη : 0<η) :
    let C := π (cutElement Q M ε)
    let D := antiunitaryConjugate (H := K) J (π (cutElement Q M η))
    Commute T C ∧ Commute T D ∧
      (1-T)*C*antiunitaryConjugate (H := K) J (π (F1Fecho.RegularPositiveFlow.regularDomainCut Q M η)) =
        T*π (F1Fecho.RegularPositiveFlow.regularDomainCut Q M ε)*D := by
  let N := (F1Fecho.RegularCovariantCore.core Q M).toStarSubalgebra
  let r : N := resolventElement Q M
  let A := π r
  let B := antiunitaryConjugate (H := K) J A
  let c (δ : ℝ) : N := cutElement Q M δ
  let C := π (c ε)
  let D := antiunitaryConjugate (H := K) J (π (c η))
  let p := π (F1Fecho.RegularPositiveFlow.regularDomainCut Q M ε)
  let q := antiunitaryConjugate (H := K) J (π (F1Fecho.RegularPositiveFlow.regularDomainCut Q M η))
  change Commute T C ∧ Commute T D ∧ (1-T)*C*q=T*p*D
  haveI : IsClosed (N : Set (RegularHilbert H →L[ℂ] RegularHilbert H)) := by
    change IsClosed (F1Fecho.RegularCovariantCore.core Q M : Set (RegularHilbert H →L[ℂ] RegularHilbert H))
    rw [← VonNeumannAlgebra.centralizer_centralizer (F1Fecho.RegularCovariantCore.core Q M)]
    exact Set.isClosed_centralizer _
  have hTC (δ : ℝ) (hδ : 0<δ) : Commute T (π (c δ)) := by
    let f := inverseCutoffFunction δ
    have hr : IsSelfAdjoint r.val := IsSelfAdjoint.of_nonneg (F1Fecho.RegularPositiveFlow.regularSpectralResolvent_nonneg Q)
    obtain ⟨hm,_,hc⟩ := F1Fecho.ModularCutBalance.closed_representation_cfc
      (H := RegularHilbert H) (K := K) N π r hr f (inverseCutoffFunction_continuous δ hδ)
    have he : (⟨cfc f r.val,hm⟩ : N)=c δ :=
      Subtype.ext (F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_cfc Q δ hδ).symm
    rw [he] at hc
    exact hc T hTA
  have hTD : Commute T D := by
    have hh := (hTC η hη).map (antiunitaryConjugateRealHom J)
    change Commute (antiunitaryConjugate (H := K) J T) D at hh
    rw [hflip] at hh
    simpa only [sub_sub_cancel] using (Commute.one_left D).sub_left hh
  have hp (δ : ℝ) (hδ : 0<δ) : A*π (F1Fecho.RegularPositiveFlow.regularDomainCut Q M δ)=(1-A)*π (c δ) := by
    have he : r*F1Fecho.RegularPositiveFlow.regularDomainCut Q M δ=(1-r)*c δ := by
      apply Subtype.ext
      have hh := F1Fecho.RegularPositiveFlow.regularDomainCut_inverse_product Q M 1 δ zero_lt_one hδ
      simp only [F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_one,Complex.ofReal_one,one_smul] at hh
      have hc := (F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_commutes Q 1 δ zero_lt_one hδ).eq
      rw [F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff_one] at hc
      change F1Fecho.RegularPositiveFlow.regularSpectralResolvent Q*(F1Fecho.RegularPositiveFlow.regularDomainCut Q M δ).val =
        (1-F1Fecho.RegularPositiveFlow.regularSpectralResolvent Q)*F1Fecho.RegularPositiveFlow.regularInverseGeneratorCutoff Q δ
      rw [hh,sub_mul,one_mul,hc]
    have hh := congrArg (fun a : N => π a) he
    simpa only [map_mul,map_sub,map_one] using hh
  have hq : B*q=(1-B)*D := by
    have hh := congrArg (antiunitaryConjugateRealHom J) (hp η hη)
    simp only [map_mul,map_sub,map_one] at hh
    exact hh
  have hBC : Commute B C := hcross (c ε)
  have hBp : Commute B p := hcross (F1Fecho.RegularPositiveFlow.regularDomainCut Q M ε)
  have he := F1Fecho.ModularCutBalance.cut_balance_after_multiplication T A B C D p q
    hbase hTA hTB hBC hBp (hp ε hε) hq
  refine ⟨hTC ε hε,hTD,?_⟩
  ext1 x
  apply hiA.comp hiB
  exact congrArg (fun W : K →L[ℂ] K => W x) he
end F1Fecho.RepresentedDoubleCut
#print axioms F1Fecho.RepresentedDoubleCut.cutElement
#print axioms F1Fecho.RepresentedDoubleCut.balance
