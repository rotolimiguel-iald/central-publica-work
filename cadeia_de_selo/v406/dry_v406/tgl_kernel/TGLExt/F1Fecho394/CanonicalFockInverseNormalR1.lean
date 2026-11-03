import TGLExt.F1Fecho394.GeneralInverseAdditivityR3
import TGLExt.F1Fecho394.CanonicalFockInverseSupremumR2
/-! Internal order normality and the infinite identity of the SAME inverse
weight on the Fock core. The latter follows from proved scaling and
faithfulness, not from a zero surrogate or a finiteness assumption. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.CanonicalFockInverseSupremum
open TGLExt TGLV350.Regular
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.RegularInverseWeight
open scoped ENNReal

theorem value_mono (X Y:PositiveInput) (h:X.val≤Y.val) : value X≤value Y :=
  inverseSupremum_mono fockFlow regularFockVacuum X.val Y.val h

theorem value_internal_normal {ι:Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A:ι→core.toStarSubalgebra) (S:core.toStarSubalgebra)
    (hpos:∀i,0≤A i) (hmono:Monotone A) (hS:IsLUB (Set.range A) S) (hSpos:0≤S) :
    value ⟨S.val,S.property,hSpos⟩=⨆i,value ⟨(A i).val,(A i).property,hpos i⟩ :=
  inverseSupremum_preserves_internal_isLUB fockFlow regularFockVacuum core A S hpos hmono hS

theorem positiveDual_one (s:ℝ) : positiveDual s one=one := by
  apply Subtype.ext
  change (dualAction s (1:core.toStarSubalgebra)).val=(1:core.toStarSubalgebra).val
  exact congrArg Subtype.val (map_one (dualAction s))

theorem value_one : value one=⊤ := by
  have hn:value one≠0:=by
    intro hz
    have he:one.val=(0:TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F→L[ℂ]
        TGLV350.Regular.RegularHilbert F1Rede.BosonicFock.F):=(value_faithful one).mp hz
    exact positive_cone_nontrivial (Subtype.ext he)
  by_contra ht
  have he:=value_dual 1 one
  rw [positiveDual_one] at he
  have hc:ENNReal.ofReal (Real.exp (-1))=1:=(ENNReal.mul_eq_right hn ht).mp he.symm
  have hl:ENNReal.ofReal (Real.exp (-1))<1:=
    ENNReal.ofReal_lt_one.mpr (Real.exp_lt_one_iff.mpr (by norm_num))
  exact (ne_of_lt hl) hc

end F1Fecho.CanonicalFockInverseSupremum
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_mono
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_internal_normal
#print axioms F1Fecho.CanonicalFockInverseSupremum.positiveDual_one
#print axioms F1Fecho.CanonicalFockInverseSupremum.value_one
