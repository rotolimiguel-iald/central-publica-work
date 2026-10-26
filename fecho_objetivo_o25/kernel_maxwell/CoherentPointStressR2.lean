import CoherentPointMaxwellR1

/-! The pointwise coherent stress kernel built from actual regular profiles.
This kernel already satisfies Maxwell conservation and Hermitian swap. Its
extension to a Fock form and equality with the smeared Wick form need consumers. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open F1Fecho.MaxwellStress TGLExt.ImportedSQ

def coherentProfileStress (h k : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  Complex.exp (inner ℂ h k)*stress metricSignC (fun α β=>coherentProfileWave h k α β x) μ ν

theorem coherentProfileStress_line_hasDerivAt (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (ρ μ ν : Fin 4) (x : Spacetime) :
    HasDerivAt (fun t : ℝ=>coherentProfileStress h k μ ν (x+t • spacetimeBasis ρ))
      (Complex.exp (inner ℂ h k)*stressJet metricSignC
        (fun α β=>coherentProfileWave h k α β x)
        (fun ρ α β=>coherentProfileJet h k ρ α β x) ρ μ ν) 0 := by
  have hd (α β : Fin 4) :=coherentProfileWave_line_hasDerivAt h k hh hk ρ α β x 0
  have hr:=stress_hasDerivAt metricSignC
    (fun t α β=>coherentProfileWave h k α β (x+t • spacetimeBasis ρ))
    (fun α β=>coherentProfileJet h k ρ α β x) 0
    (fun α β=>by simpa only [zero_smul,add_zero] using hd α β) μ ν
  simpa only [coherentProfileStress,stressJet,zero_smul,add_zero] using
    hr.const_mul (Complex.exp (inner ℂ h k))

theorem coherentProfileStress_conserved (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (ν : Fin 4) (x : Spacetime) :
    (∑μ : Fin 4,metricSignC μ*
      deriv (fun t : ℝ=>coherentProfileStress h k μ ν (x+t • spacetimeBasis μ)) 0)=0 := by
  simp only [(coherentProfileStress_line_hasDerivAt h k hh hk _ _ _ x).deriv]
  have hs:=stressJet_conserved metricSignC metricSignC_square
    (fun α β=>coherentProfileWave h k α β x) (fun ρ α β=>coherentProfileJet h k ρ α β x)
    (fun μ ν=>coherentProfileWave_antisymmetric h k μ ν x)
    (fun ρ μ ν=>coherentProfileJet_antisymmetric h k ρ μ ν x)
    (fun ρ μ ν=>coherentProfileJet_bianchi h k hh hk ρ μ ν x)
    (fun ν=>coherentProfileJet_divergence h k hh hk ν x) ν
  calc
    _ = Complex.exp (inner ℂ h k)*
      (∑μ : Fin 4,metricSignC μ*stressJet metricSignC
        (fun α β=>coherentProfileWave h k α β x)
        (fun ρ α β=>coherentProfileJet h k ρ α β x) μ μ ν) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro μ _
      ring
    _ = 0 := by rw [hs,mul_zero]

theorem coherentProfileStress_symmetric (h k : H1) (μ ν : Fin 4) (x : Spacetime) :
    coherentProfileStress h k μ ν x=coherentProfileStress h k ν μ x := by
  unfold coherentProfileStress
  rw [stress_symmetric _ _ μ ν]

theorem stress_conj (F : Fin 4→Fin 4→ℂ) (μ ν : Fin 4) :
    (starRingEnd ℂ) (stress metricSignC F μ ν)=
      stress metricSignC (fun α β=>(starRingEnd ℂ) (F α β)) μ ν := by
  by_cases h : μ=ν <;> simp [stress,h,map_sum,metricSignC_conj,map_ofNat]

theorem coherentProfileStress_hermitian (h k : H1) (μ ν : Fin 4) (x : Spacetime) :
    (starRingEnd ℂ) (coherentProfileStress h k μ ν x)=coherentProfileStress k h μ ν x := by
  simp only [coherentProfileStress,map_mul,← Complex.exp_conj,inner_conj_symm,
    stress_conj,coherentProfileWave_hermitian]

theorem coherentProfileStress_diagonal (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    coherentProfileStress h h μ ν x=Complex.exp (inner ℂ h h)*realProfileStress h μ ν x := by
  simp only [coherentProfileStress,coherentProfileWave_diagonal,realProfileStress]

theorem coherentProfileStress_translate (a : Fin 4→ℝ) (h k : H1)
    (μ ν : Fin 4) (x : Spacetime) :
    coherentProfileStress (U1 a h) (U1 a k) μ ν x=
      coherentProfileStress h k μ ν (x-WithLp.toLp 2 a) := by
  simp only [coherentProfileStress,coherentProfileWave,lowerProfileWave,
    profileWave_U1,LinearIsometryEquiv.inner_map_map]

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_conserved
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_symmetric
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_hermitian
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_diagonal
#print axioms F1Fecho.MaxwellGlobal.coherentProfileStress_translate
