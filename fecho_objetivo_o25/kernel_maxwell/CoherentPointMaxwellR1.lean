import RealProfileMaxwellStressR4

/-! The off-diagonal coherent Maxwell kernel on the SAME regular H1.
Its diagonal is the already constructed real Maxwell wave. Multiplication by
the coherent overlap and extension to the regular Fock domain are separate. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory Filter
open TGLExt.ImportedSQ ChatgptAudit.WignerRapidityMeasure016

def coherentProfileWave (h k : H1) (μ ν : Fin 4) (x : Spacetime) : ℂ :=
  (Real.sqrt 2:ℂ)⁻¹*((starRingEnd ℂ) (lowerProfileWave h μ ν x)+lowerProfileWave k μ ν x)

def coherentProfileJet (h k : H1) (ρ μ ν : Fin 4) (x : Spacetime) : ℂ :=
  (Real.sqrt 2:ℂ)⁻¹*((starRingEnd ℂ) (lowerProfileJet h ρ μ ν x)+lowerProfileJet k ρ μ ν x)

theorem coherentProfileWave_line_hasDerivAt (h k : H1)
    (hh : RegularProfile h) (hk : RegularProfile k) (ρ μ ν : Fin 4)
    (x : Spacetime) (t : ℝ) :
    HasDerivAt (fun u : ℝ=>coherentProfileWave h k μ ν (x+u • spacetimeBasis ρ))
      (coherentProfileJet h k ρ μ ν (x+t • spacetimeBasis ρ)) t :=
  ((Complex.conjCLE.hasFDerivAt.comp_hasDerivAt t
    (lowerProfileWave_line_hasDerivAt h hh ρ μ ν x t)).add
    (lowerProfileWave_line_hasDerivAt k hk ρ μ ν x t)).const_mul _

theorem coherentProfileWave_antisymmetric (h k : H1) (μ ν : Fin 4) (x : Spacetime) :
    coherentProfileWave h k ν μ x= -coherentProfileWave h k μ ν x := by
  unfold coherentProfileWave
  rw [lowerProfileWave_antisymmetric h μ ν x,lowerProfileWave_antisymmetric k μ ν x,map_neg]
  ring

theorem coherentProfileJet_antisymmetric (h k : H1) (ρ μ ν : Fin 4) (x : Spacetime) :
    coherentProfileJet h k ρ ν μ x= -coherentProfileJet h k ρ μ ν x := by
  unfold coherentProfileJet
  rw [lowerProfileJet_antisymmetric h ρ μ ν x,lowerProfileJet_antisymmetric k ρ μ ν x,map_neg]
  ring

theorem coherentProfileJet_bianchi (h k : H1) (hh : RegularProfile h) (hk : RegularProfile k)
    (ρ μ ν : Fin 4) (x : Spacetime) :
    coherentProfileJet h k ρ μ ν x+coherentProfileJet h k μ ν ρ x+
      coherentProfileJet h k ν ρ μ x=0 := by
  have h1:=congrArg (starRingEnd ℂ) (lowerProfileJet_bianchi h hh ρ μ ν x)
  simp only [map_add,map_zero] at h1
  have h2:=lowerProfileJet_bianchi k hk ρ μ ν x
  unfold coherentProfileJet
  linear_combination (Real.sqrt 2:ℂ)⁻¹*h1+(Real.sqrt 2:ℂ)⁻¹*h2

theorem metricSignC_conj (μ : Fin 4) : (starRingEnd ℂ) (metricSignC μ)=metricSignC μ := by
  unfold metricSignC
  split_ifs <;> simp

theorem coherentProfileJet_divergence (h k : H1) (hh : RegularProfile h) (hk : RegularProfile k)
    (ν : Fin 4) (x : Spacetime) :
    (∑μ : Fin 4,metricSignC μ*coherentProfileJet h k μ μ ν x)=0 := by
  calc
    _ = (Real.sqrt 2:ℂ)⁻¹*
        ((starRingEnd ℂ) (∑μ : Fin 4,metricSignC μ*lowerProfileJet h μ μ ν x)+
        ∑μ : Fin 4,metricSignC μ*lowerProfileJet k μ μ ν x) := by
      rw [map_sum,mul_add,Finset.mul_sum,Finset.mul_sum,← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro μ _
      rw [map_mul,metricSignC_conj]
      unfold coherentProfileJet
      ring
    _ = 0 := by rw [lowerProfileJet_divergence h hh,lowerProfileJet_divergence k hk,map_zero,add_zero,mul_zero]

theorem coherentProfileWave_diagonal (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    coherentProfileWave h h μ ν x=realProfileWave h μ ν x := by
  unfold coherentProfileWave realProfileWave
  rw [realWaveProjection_apply]
  have ha : (starRingEnd ℂ) (lowerProfileWave h μ ν x)+lowerProfileWave h μ ν x=
      (2*(lowerProfileWave h μ ν x).re:ℝ) := by
    simpa only [add_comm] using Complex.add_conj (lowerProfileWave h μ ν x)
  rw [ha]
  have hs : (Real.sqrt 2:ℂ)^2=2 := by exact_mod_cast Real.sq_sqrt (by norm_num : (0:ℝ)≤2)
  have hn : (Real.sqrt 2:ℂ)≠0 := Complex.ofReal_ne_zero.mpr (Real.sqrt_ne_zero'.mpr (by norm_num))
  push_cast
  field_simp [hn]
  linear_combination -(lowerProfileWave h μ ν x).re*hs

theorem coherentProfileWave_hermitian (h k : H1) (μ ν : Fin 4) (x : Spacetime) :
    (starRingEnd ℂ) (coherentProfileWave h k μ ν x)=coherentProfileWave k h μ ν x := by
  simp only [coherentProfileWave,map_mul,map_add,map_inv₀,Complex.conj_ofReal,starRingEnd_self_apply]
  ring

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.coherentProfileWave_line_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.coherentProfileWave_antisymmetric
#print axioms F1Fecho.MaxwellGlobal.coherentProfileJet_bianchi
#print axioms F1Fecho.MaxwellGlobal.coherentProfileJet_divergence
#print axioms F1Fecho.MaxwellGlobal.coherentProfileWave_diagonal
#print axioms F1Fecho.MaxwellGlobal.coherentProfileWave_hermitian
