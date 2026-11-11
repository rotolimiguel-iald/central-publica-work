import TGLExt.F1Fecho394.GeneralInverseSupremumR3
import TGLExt.F1Fecho394.GeneralPositiveSandwichFaithfulR1
import TGLExt.F1Fecho394.CanonicalFockFaithfulWeightR2
/-! Actual inverse-generator perturbation on the SAME Fock represented core.
The supremum is homogeneous, normal, faithful, and dual-scaled. Its positive
additivity and tracial law are not claimed until regulator order is proved.
This is not a total cyclic ENNReal-valued extension to arbitrary operators. -/
set_option autoImplicit false
set_option maxHeartbeats 1500000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.CanonicalFockInverseSupremum
open TGLExt TGLV350.Regular F1Rede.BosonicFock
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.CanonicalFockFaithfulWeight F1Fecho.RegularInverseWeight
open Filter
open scoped ENNReal NNReal Topology

def cut (e:ℝ) (X:PositiveInput):ℝ≥0∞:=cutoffWeight fockFlow regularFockVacuum e X.val
def value (X:PositiveInput):ℝ≥0∞:=inverseSupremum fockFlow regularFockVacuum X.val

theorem value_zero:value zero=0:=inverseSupremum_zero fockFlow regularFockVacuum

theorem value_scale (r:ℝ≥0) (X:PositiveInput):
    value (scale r X)=(r:ℝ≥0∞)*value X:=
  inverseSupremum_scale fockFlow regularFockVacuum r X.val

theorem value_dual (s:ℝ) (X:PositiveInput):
    value (positiveDual s X)=ENNReal.ofReal (Real.exp (-s))*value X:=
  inverseSupremum_dual fockFlow regularFockVacuum s X.val

theorem cut_one_faithful (X:PositiveInput):cut 1 X=0 ↔ X.val=0 := by
  constructor
  · intro hz
    let R:=RegularPositiveFlow.regularInverseGeneratorCutoff fockFlow 1
    let b:=hilbertPositiveSqrt R
    have hR:R∈core:=RegularPositiveFlow.regularInverseGeneratorCutoff_mem fockFlow M 1
    have hb:b∈core:=sqrt_mem_core core R hR
      (RegularPositiveFlow.regularInverseGeneratorCutoff_nonneg fockFlow 1 zero_lt_one)
    have hm:star b*X.val*b∈core:=core.mul_mem
      (core.mul_mem (core.toStarSubalgebra.star_mem' hb) X.property.1) hb
    have he:star b*X.val*b=0:=
      (weight_faithful ⟨star b*X.val*b,hm,star_left_conjugate_nonneg X.property.2 b⟩).mp hz
    change star (hilbertPositiveSqrt R)*X.val*hilbertPositiveSqrt R=0 at he
    have hr:R=RegularPositiveFlow.regularSpectralResolvent fockFlow:=
      RegularPositiveFlow.regularInverseGeneratorCutoff_one fockFlow
    rw [hr] at he
    exact sqrt_conjugation_faithful _ X.val
      (RegularPositiveFlow.regularSpectralResolvent_nonneg fockFlow)
      (RegularPositiveFlow.regularSpectralResolvent_injective fockFlow) he
  · intro hx
    change cutoffWeight fockFlow regularFockVacuum 1 X.val=0
    rw [hx,cutoffWeight_zero]

theorem value_faithful (X:PositiveInput):value X=0 ↔ X.val=0 := by
  constructor
  · intro hz
    have hh:=cutoffWeight_le_supremum fockFlow regularFockVacuum
      (⟨1,zero_lt_one⟩:PositiveRegulator) X.val
    change cut 1 X ≤ value X at hh
    rw [hz] at hh
    exact (cut_one_faithful X).mp (le_antisymm hh bot_le)
  · intro hx
    change inverseSupremum fockFlow regularFockVacuum X.val=0
    rw [hx,inverseSupremum_zero]

theorem value_normal {i:Type*} [Preorder i] [IsDirectedOrder i] [Nonempty i]
    (A:i→PositiveInput) (S:PositiveInput)
    (hmono:Monotone (fun j=>(A j).val))
    (hlim:∀v,Tendsto (fun j=>(A j).val v) atTop (𝓝 (S.val v))) :
    value S=⨆j,value (A j) :=
  inverseSupremum_normal fockFlow regularFockVacuum (fun j=>(A j).val) S.val
    (fun j=>(A j).property.2) hmono hlim

theorem value_subadditive (X Y:PositiveInput):value (add X Y) ≤ value X+value Y :=
  inverseSupremum_subadditive fockFlow regularFockVacuum X.val Y.val X.property.2 Y.property.2

end F1Fecho.CanonicalFockInverseSupremum
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_zero
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_scale
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_dual
#print axioms F1Fecho.CanonicalFockInverseSupremum.cut_one_faithful
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_faithful

#print axioms F1Fecho.CanonicalFockInverseSupremum.value_normal
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_subadditive
