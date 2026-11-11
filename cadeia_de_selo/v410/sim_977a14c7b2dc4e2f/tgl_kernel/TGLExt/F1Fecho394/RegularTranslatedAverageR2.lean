import TGLExt.F1Fecho394.RegularFibreAverageStarR3
/-! Translated finite adjunction pairs for arbitrary coefficient intervals. -/
set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.RegularTranslatedAverage
open TGLV350.Regular F1Fecho.RegularCovariantCore
variable {H:Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
theorem average_commutes (B:UnitaryFlow H) (a h:ℝ) :
    RegularCoreAverage.regularAverage B h*regularUnitary B a=
      regularUnitary B a*RegularCoreAverage.regularAverage B h := by
  have he := TGLV350.StrongIntegral.operatorIntegral_commutes
    (RegularCoreAverage.regularIntegralFamily B) 0 h (regularUnitary B a) (fun t=>by
      change regularUnitary B a*regularUnitary B t=regularUnitary B t*regularUnitary B a
      rw [F1Fecho.RegularCovariantCore.regular_mul,F1Fecho.RegularCovariantCore.regular_mul,add_comm])
  unfold RegularCoreAverage.regularAverage
  rw [smul_mul_assoc,mul_smul_comm,he]

theorem translated_star (B:UnitaryFlow H) (A:H→L[ℂ]H) (a h:ℝ) :
    star (fibre A*(regularUnitary B a*RegularCoreAverage.regularAverage B h))=
      regularUnitary B (-(a+h))*(RegularCoreAverage.regularAverage B h*fibre (star A)) := by
  rw [star_mul,star_mul,RegularAverageAdjoint.regularAverage_star,F1Fecho.RegularCovariantCore.regular_star,←fibre_star]
  calc
    _ = regularUnitary B (-h)*(RegularCoreAverage.regularAverage B h*regularUnitary B (-a))*fibre (star A) := by
      simp only [mul_assoc]
    _ = _ := by
      rw [average_commutes,←mul_assoc,F1Fecho.RegularCovariantCore.regular_mul]
      have he : -h + -a=-(a+h) := by ring
      rw [he]
      simp only [mul_assoc]

theorem translated_finite (B:UnitaryFlow H) (A:H→L[ℂ]H) (a h:ℝ) (hh:0<h) :
    HasFiniteDualSquare (fibre A*(regularUnitary B a*RegularCoreAverage.regularAverage B h)) ∧
    HasFiniteDualSquare (star (fibre A*(regularUnitary B a*RegularCoreAverage.regularAverage B h))) := by
  constructor
  · exact HasFiniteDualSquare.left_mul _ _ (HasFiniteDualSquare.left_mul _ _
      (RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare B h hh))
  · rw [translated_star]
    exact HasFiniteDualSquare.left_mul _ _ (RegularFiniteFibreRight.right_fibre _
      (RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare B h hh) (star A))
end F1Fecho.RegularTranslatedAverage
#print axioms F1Fecho.RegularTranslatedAverage.average_commutes
#print axioms F1Fecho.RegularTranslatedAverage.translated_star
#print axioms F1Fecho.RegularTranslatedAverage.translated_finite
