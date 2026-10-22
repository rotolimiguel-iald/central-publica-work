import TGLV350.ScaledPositiveResolvent
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.PosPart.Basic

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 200000

namespace TGLV350.Regular
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def projectionGapPart (A : H →L[ℂ] H) (c : ℝ) : H →L[ℂ] H := (1-c • A)⁺

theorem projectionGapPart_nonneg (A : H →L[ℂ] H) (c : ℝ) :
    0 ≤ projectionGapPart A c := CFC.posPart_nonneg _

theorem projectionGapPart_commutes (A T : H →L[ℂ] H) (c : ℝ) (hAT : Commute A T) :
    Commute (projectionGapPart A c) T := by
  have hX : Commute (1-c • A) T := by
    change (1-c • A)*T=T*(1-c • A)
    simp only [sub_mul,mul_sub,one_mul,mul_one,smul_mul_assoc,mul_smul_comm,hAT.eq]
  exact hX.cfcₙ_real (·⁺ : ℝ → ℝ)

theorem projectionGapPart_square (A : H →L[ℂ] H) (c : ℝ) (hA : star A=A) :
    projectionGapPart A c * projectionGapPart A c = projectionGapPart A c * (1-c • A) := by
  let X : H →L[ℂ] H := 1-c • A
  have hX : IsSelfAdjoint X := by
    change star (1-c • A)=1-c • A
    simp only [star_sub,star_one,star_smul,star_trivial,hA]
  have hd : X=X⁺-X⁻ := (CFC.posPart_sub_negPart X hX).symm
  change X⁺*X⁺=X⁺*X
  calc
    X⁺*X⁺ = X⁺*(X⁺-X⁻) := by rw [mul_sub,CFC.posPart_mul_negPart,sub_zero]
    _ = X⁺*X := congrArg (fun Y => X⁺*Y) hd.symm

theorem injectiveBlock_complement_zero (A B e : H →L[ℂ] H)
    (hinj : Function.Injective A) (hBB : B*star B=A*(1-A))
    (heA : Commute e A) (heB : e*B=0) : e*(1-A)=0 := by
  have hAz : A*(e*(1-A))=0 := by
    calc
      _ = (A*e)*(1-A) := (mul_assoc _ _ _).symm
      _ = (e*A)*(1-A) := congrArg (fun T => T*(1-A)) heA.eq.symm
      _ = e*(B*star B) := by rw [mul_assoc,hBB]
      _ = (e*B)*star B := (mul_assoc _ _ _).symm
      _ = 0 := by rw [heB,zero_mul]
  ext v
  apply hinj
  have hv := congrArg (fun T : H →L[ℂ] H => T v) hAz
  simpa using hv

theorem projectionGapPart_eq_zero_of_block_zero (A B : H →L[ℂ] H) (c : ℝ)
    (hc : 1 ≤ c) (hA : star A=A) (hinj : Function.Injective A)
    (hBB : B*star B=A*(1-A)) (heB : projectionGapPart A c*B=0) :
    projectionGapPart A c=0 := by
  let e := projectionGapPart A c
  have he : 0 ≤ e := projectionGapPart_nonneg A c
  have hs : star e=e := (IsSelfAdjoint.of_nonneg he).star_eq
  have heA : Commute e A := projectionGapPart_commutes A A c (Commute.refl A)
  have hcomp := injectiveBlock_complement_zero A B e hinj hBB heA heB
  have heq : e*A=e := by
    rw [mul_sub,mul_one,sub_eq_zero] at hcomp
    exact hcomp.symm
  have hsq : e*e=(1-c) • e := by
    calc
      _ = e*(1-c • A) := projectionGapPart_square A c hA
      _ = (1-c) • e := by rw [mul_sub,mul_one,mul_smul_comm,heq,sub_smul,one_smul]
  have hp : 0 ≤ e*e := by simpa only [hs] using (star_mul_self_nonneg e)
  have hn : e*e ≤ 0 := by
    rw [hsq]
    exact smul_nonpos_of_nonpos_of_nonneg (sub_nonpos.mpr hc) he
  exact (CStarRing.star_mul_self_eq_zero_iff e).mp (by simpa only [hs] using le_antisymm hn hp)

theorem projectionBlock_lower_bound_of_gap_zero (A : H →L[ℂ] H) (c : ℝ)
    (hc : 0 < c) (hA : star A=A) (he : projectionGapPart A c=0) :
    c⁻¹ • (1 : H →L[ℂ] H) ≤ A := by
  have hX : IsSelfAdjoint (1-c • A) := by
    change star (1-c • A)=1-c • A
    simp only [star_sub,star_one,star_smul,star_trivial,hA]
  have hle : (1 : H →L[ℂ] H) ≤ c • A :=
    sub_nonpos.mp ((CFC.posPart_eq_zero_iff _ hX).mp he)
  have hh := smul_nonneg (inv_pos.mpr hc).le (sub_nonneg.mpr hle)
  simp only [smul_sub,smul_smul,inv_mul_cancel₀ hc.ne',one_smul] at hh
  exact sub_nonneg.mp hh

theorem projectionBlock_strictPositive_of_lower_bound (A : H →L[ℂ] H) (c : ℝ)
    (hc : 0 < c) (hbound : c⁻¹ • (1 : H →L[ℂ] H) ≤ A) : IsStrictlyPositive A := by
  have hbase : IsStrictlyPositive (c⁻¹ • (1 : H →L[ℂ] H)) := by
    rw [IsStrictlyPositive.iff_of_unital]
    refine ⟨smul_nonneg (inv_pos.mpr hc).le zero_le_one,?_⟩
    rw [← Algebra.algebraMap_eq_smul_one]
    exact (isUnit_iff_ne_zero.mpr (inv_pos.mpr hc).ne').map (algebraMap ℝ (H →L[ℂ] H))
  exact hbase.of_le hbound

#print axioms projectionGapPart_nonneg
#print axioms projectionGapPart_commutes
#print axioms projectionGapPart_square
#print axioms injectiveBlock_complement_zero
#print axioms projectionGapPart_eq_zero_of_block_zero
#print axioms projectionBlock_lower_bound_of_gap_zero
#print axioms projectionBlock_strictPositive_of_lower_bound
end
end TGLV350.Regular
