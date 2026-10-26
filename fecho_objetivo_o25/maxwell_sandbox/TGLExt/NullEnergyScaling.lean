import TGLExt.ContratoQG_v32
import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
import Mathlib.MeasureTheory.Measure.Prod

set_option autoImplicit false
set_option maxHeartbeats 800000

/-!
# Transformação da densidade de energia nula sob o boost

Este módulo não postula uma dinâmica nem identifica a densidade com `pPlus`.
Ele mede o que a covariância do tensor já obriga: a densidade `T_nn` escala
quadraticamente. A carga de Killing é calculada com o seu jacobiano, sem
presumir que ela satisfaça a lei dual de expoente um.
-/
namespace TGLExt.NullEnergyScaling
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory

/-- A densidade nula transforma com quadrado do fator do vetor nulo. -/
theorem nullEnergy_boost_covariant {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (x : Fin 4 → ℝ) :
    nullEnergy T.toStressTensorData (B.V s ψ) (wedgeBoostMap s x) =
      (Real.exp (-s) * Real.exp (-s)) * nullEnergy T.toStressTensorData ψ x := by
  unfold nullEnergy pairing
  rw [T.boost_covariant]
  rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec,
    Matrix.dotProduct_transpose_mulVec]
  rw [show wedgeBoostMap (-s) (wedgeBoostMap s x) = x by
    rw [← wedgeBoostMap_add]
    simp [wedgeBoostMap_zero]]
  rw [show boostMat (-s) *ᵥ nullDir = Real.exp (-s) • nullDir by
    exact wedgeBoostMap_nullDir (-s)]
  simp only [Matrix.mulVec_smul, dotProduct_smul, smul_dotProduct, smul_eq_mul,
    dotProduct_comm]
  ring

/-- A forma exponencial usada na auditoria da lei dual. -/
theorem nullEnergy_boost_exp_neg_two {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (x : Fin 4 → ℝ) :
    nullEnergy T.toStressTensorData (B.V s ψ) (wedgeBoostMap s x) =
      Real.exp (-(2 * s)) * nullEnergy T.toStressTensorData ψ x := by
  rw [nullEnergy_boost_covariant]
  congr 1
  rw [← Real.exp_add]
  congr 1
  ring

/-- O integrando bilateral da carga nula, mantido explícito para a mudança de escala. -/
def chargeIntegrand {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) (p : ℝ × (Fin 2 → ℝ)) : ℝ :=
  p.1 * nullEnergy T ψ (p.1 • nullDir + screenEmbed p.2)

/-- O boost induzido no plano nulo: só a coordenada da geratriz escala. -/
noncomputable def nullPlaneBoost (s : ℝ) (p : ℝ × (Fin 2 → ℝ)) : ℝ × (Fin 2 → ℝ) :=
  (Real.exp s * p.1, p.2)

/-- A dilatação anisotrópica preserva integrabilidade; nenhuma segunda hipótese
    no estado transformado é necessária. -/
theorem integrable_nullPlaneBoost (s : ℝ) (F : (ℝ × (Fin 2 → ℝ)) → ℝ)
    (hF : Integrable F) : Integrable (fun p => F (nullPlaneBoost s p)) := by
  rw [Measure.volume_eq_prod] at hF ⊢
  have hm : Measure.QuasiMeasurePreserving (nullPlaneBoost s) (volume.prod volume) (volume.prod volume) := by
    have hs : Measure.QuasiMeasurePreserving (Real.exp s • ·) (volume : Measure ℝ) volume :=
      Measure.quasiMeasurePreserving_smul (volume : Measure ℝ) (Real.exp_ne_zero s)
    change Measure.QuasiMeasurePreserving (Prod.map (Real.exp s • ·) id)
      (volume.prod volume) (volume.prod volume)
    exact MeasureTheory.QuasiMeasurePreserving.prodMap hs
      (Measure.QuasiMeasurePreserving.id (volume : Measure (Fin 2 → ℝ)))
  have hmeas : AEStronglyMeasurable (fun p => F (nullPlaneBoost s p))
      (volume.prod volume) := hF.aestronglyMeasurable.comp_quasiMeasurePreserving hm
  rw [integrable_prod_iff' hmeas]
  constructor
  · filter_upwards [hF.prod_left_ae] with y hy
    simp only [nullPlaneBoost]
    exact hy.comp_mul_left' (Real.exp_ne_zero s)
  · have hnorm := hF.integral_norm_prod_right
    have heq : (fun y => ∫ x, ‖F (nullPlaneBoost s (x, y))‖) =
        (fun y => |(Real.exp s)⁻¹| * ∫ x, ‖F (x, y)‖) := by
      funext y
      simp only [nullPlaneBoost]
      simpa only [smul_eq_mul] using
        (Measure.integral_comp_mul_left (fun x => ‖F (x, y)‖) (Real.exp s))
    rw [heq]
    exact hnorm.const_mul _

/-- O integrando transformado ganha `e⁻ˢ`; a tela transversal não escala. -/
theorem chargeIntegrand_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (p : ℝ × (Fin 2 → ℝ)) :
    chargeIntegrand T.toStressTensorData (B.V s ψ) p =
      Real.exp (-s) * chargeIntegrand T.toStressTensorData ψ (nullPlaneBoost (-s) p) := by
  let q : ℝ × (Fin 2 → ℝ) := nullPlaneBoost (-s) p
  have hp : p.1 = Real.exp s * q.1 := by
    simp only [q, nullPlaneBoost, Real.exp_neg]
    field_simp [Real.exp_ne_zero]
  have hs : wedgeBoostMap s (screenEmbed q.2) = screenEmbed q.2 := by
    ext i
    fin_cases i <;>
      simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
        screenEmbed]
  have hx : p.1 • nullDir + screenEmbed p.2 =
      wedgeBoostMap s (q.1 • nullDir + screenEmbed q.2) := by
    calc
      p.1 • nullDir + screenEmbed p.2 =
          (Real.exp s * q.1) • nullDir + screenEmbed q.2 := by rw [hp]; rfl
      _ = wedgeBoostMap s (q.1 • nullDir + screenEmbed q.2) := by
        simp only [wedgeBoostMap, Matrix.mulVec_add, Matrix.mulVec_smul]
        rw [show boostMat s *ᵥ nullDir = Real.exp s • nullDir from wedgeBoostMap_nullDir s]
        rw [show boostMat s *ᵥ screenEmbed q.2 = screenEmbed q.2 from hs]
        simp [smul_smul, mul_comm]
  unfold chargeIntegrand
  rw [hx, nullEnergy_boost_covariant]
  simp only [q, nullPlaneBoost]
  rw [hp]
  simp only [Real.exp_neg]
  field_simp [Real.exp_ne_zero]
  <;> ring

/-- A carga bilateral é invariante: o fator `e⁻ˢ` do integrando e o
    jacobiano `eˢ` da única coordenada nula se cancelam exatamente.
    Portanto uma carga não nula não satisfaz a lei dual de expoente um.
    As duas integrabilidades permanecem hipóteses explícitas. -/
theorem nullPlaneCharge_boost_invariant {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (chargeIntegrand T.toStressTensorData ψ))
    (hB : Integrable (chargeIntegrand T.toStressTensorData (B.V s ψ))) :
    nullPlaneCharge T.toStressTensorData (B.V s ψ) =
      nullPlaneCharge T.toStressTensorData ψ := by
  let F : (ℝ × (Fin 2 → ℝ)) → ℝ := chargeIntegrand T.toStressTensorData ψ
  have hG : Integrable (fun p => Real.exp (-s) * F (nullPlaneBoost (-s) p)) := by
    apply hB.congr
    filter_upwards [] with p
    exact chargeIntegrand_boost B T s ψ p
  unfold nullPlaneCharge
  rw [Measure.volume_eq_prod] at hF hG ⊢
  calc
    nullPlaneCharge T.toStressTensorData (B.V s ψ) =
        ∫ p, Real.exp (-s) * F (nullPlaneBoost (-s) p) := by
      apply integral_congr_ae
      filter_upwards [] with p
      exact chargeIntegrand_boost B T s ψ p
    _ = ∫ y, ∫ x, Real.exp (-s) * F (nullPlaneBoost (-s) (x, y)) := integral_prod_symm _ hG
    _ = ∫ y, Real.exp (-s) * (|(Real.exp (-s))⁻¹| • ∫ x, F (x, y)) := by
      apply integral_congr_ae
      filter_upwards [] with y
      simp only [nullPlaneBoost, integral_const_mul]
      congr 1
      exact Measure.integral_comp_mul_left (fun x => F (x, y)) (Real.exp (-s))
    _ = ∫ y, ∫ x, F (x, y) := by
      simp only [Real.exp_neg, abs_of_pos (Real.exp_pos s), smul_eq_mul, inv_inv]
      field_simp [Real.exp_ne_zero]
    _ = nullPlaneCharge T.toStressTensorData ψ := (integral_prod_symm _ hF).symm

/-- Uma carga não nula não pode ser o `τ` da lei dual: `s = 1` já a refuta. -/
theorem nullPlaneCharge_not_dual_scaling {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (ψ : W.H)
    (hF : Integrable (chargeIntegrand T.toStressTensorData ψ))
    (hB : Integrable (chargeIntegrand T.toStressTensorData (B.V 1 ψ)))
    (hQ : nullPlaneCharge T.toStressTensorData ψ ≠ 0) :
    nullPlaneCharge T.toStressTensorData (B.V 1 ψ) ≠
      Real.exp (-(1 : ℝ)) * nullPlaneCharge T.toStressTensorData ψ := by
  rw [nullPlaneCharge_boost_invariant B T 1 ψ hF hB]
  intro h
  have he : Real.exp (-(1 : ℝ)) < 1 := Real.exp_lt_one_iff.mpr (by norm_num)
  rcases lt_or_gt_of_ne hQ with hneg | hpos
  · nlinarith
  · nlinarith

/-- A carga nula sem peso de Killing: uma componente de momento, não massa. -/
def momentumIntegrand {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) (p : ℝ × (Fin 2 → ℝ)) : ℝ :=
  nullEnergy T ψ (p.1 • nullDir + screenEmbed p.2)

noncomputable def nullPlaneMomentum {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  ∫ p : ℝ × (Fin 2 → ℝ), momentumIntegrand T ψ p

/-- A componente de momento tem peso dois antes da integração. -/
theorem momentumIntegrand_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (p : ℝ × (Fin 2 → ℝ)) :
    momentumIntegrand T.toStressTensorData (B.V s ψ) p =
      Real.exp (-(2 * s)) *
        momentumIntegrand T.toStressTensorData ψ (nullPlaneBoost (-s) p) := by
  let q : ℝ × (Fin 2 → ℝ) := nullPlaneBoost (-s) p
  have hp : p.1 = Real.exp s * q.1 := by
    simp only [q, nullPlaneBoost, Real.exp_neg]
    field_simp [Real.exp_ne_zero]
  have hs : wedgeBoostMap s (screenEmbed q.2) = screenEmbed q.2 := by
    ext i
    fin_cases i <;>
      simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
        screenEmbed]
  have hx : p.1 • nullDir + screenEmbed p.2 =
      wedgeBoostMap s (q.1 • nullDir + screenEmbed q.2) := by
    calc
      p.1 • nullDir + screenEmbed p.2 =
          (Real.exp s * q.1) • nullDir + screenEmbed q.2 := by rw [hp]; rfl
      _ = wedgeBoostMap s (q.1 • nullDir + screenEmbed q.2) := by
        simp only [wedgeBoostMap, Matrix.mulVec_add, Matrix.mulVec_smul]
        rw [show boostMat s *ᵥ nullDir = Real.exp s • nullDir from wedgeBoostMap_nullDir s]
        rw [show boostMat s *ᵥ screenEmbed q.2 = screenEmbed q.2 from hs]
        simp [smul_smul, mul_comm]
  unfold momentumIntegrand
  rw [hx, nullEnergy_boost_covariant]
  rw [← Real.exp_add]
  congr 1
  ring

/-- O momento nulo tem exatamente a lei de escala exigida de `τ`. -/
theorem nullPlaneMomentum_boost_scaling {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hB : Integrable (momentumIntegrand T.toStressTensorData (B.V s ψ))) :
    nullPlaneMomentum T.toStressTensorData (B.V s ψ) =
      Real.exp (-s) * nullPlaneMomentum T.toStressTensorData ψ := by
  let F : (ℝ × (Fin 2 → ℝ)) → ℝ := momentumIntegrand T.toStressTensorData ψ
  have hG : Integrable (fun p => Real.exp (-(2 * s)) * F (nullPlaneBoost (-s) p)) := by
    apply hB.congr
    filter_upwards [] with p
    exact momentumIntegrand_boost B T s ψ p
  unfold nullPlaneMomentum
  rw [Measure.volume_eq_prod] at hF hG ⊢
  calc
    nullPlaneMomentum T.toStressTensorData (B.V s ψ) =
        ∫ p, Real.exp (-(2 * s)) * F (nullPlaneBoost (-s) p) := by
      apply integral_congr_ae
      filter_upwards [] with p
      exact momentumIntegrand_boost B T s ψ p
    _ = ∫ y, ∫ x, Real.exp (-(2 * s)) * F (nullPlaneBoost (-s) (x, y)) :=
      integral_prod_symm _ hG
    _ = ∫ y, Real.exp (-(2 * s)) * (|(Real.exp (-s))⁻¹| • ∫ x, F (x, y)) := by
      apply integral_congr_ae
      filter_upwards [] with y
      simp only [nullPlaneBoost, integral_const_mul]
      congr 1
      exact Measure.integral_comp_mul_left (fun x => F (x, y)) (Real.exp (-s))
    _ = ∫ y, Real.exp (-s) * ∫ x, F (x, y) := by
      apply integral_congr_ae
      filter_upwards [] with y
      have he : (Real.exp (-s))⁻¹ = Real.exp s := by rw [Real.exp_neg, inv_inv]
      rw [abs_of_pos (inv_pos.mpr (Real.exp_pos _)), he]
      simp only [smul_eq_mul]
      rw [← mul_assoc, ← Real.exp_add]
      congr 2
      ring
    _ = Real.exp (-s) * ∫ y, ∫ x, F (x, y) :=
      integral_const_mul (Real.exp (-s)) (fun y => ∫ x, F (x, y))
    _ = Real.exp (-s) * nullPlaneMomentum T.toStressTensorData ψ := by
      congr 1
      exact (integral_prod_symm _ hF).symm

/-- A integrabilidade da carga no estado boosted é derivada da original. -/
theorem chargeIntegrable_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (hF : Integrable (chargeIntegrand T.toStressTensorData ψ)) :
    Integrable (chargeIntegrand T.toStressTensorData (B.V s ψ)) := by
  have hi := (integrable_nullPlaneBoost (-s) (chargeIntegrand T.toStressTensorData ψ) hF).const_mul
    (Real.exp (-s))
  apply hi.congr
  filter_upwards [] with p
  exact (chargeIntegrand_boost B T s ψ p).symm

/-- Invariância da carga usando somente a integrabilidade no estado inicial. -/
theorem nullPlaneCharge_boost_invariant_of_integrable {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (hF : Integrable (chargeIntegrand T.toStressTensorData ψ)) :
    nullPlaneCharge T.toStressTensorData (B.V s ψ) = nullPlaneCharge T.toStressTensorData ψ :=
  nullPlaneCharge_boost_invariant B T s ψ hF (chargeIntegrable_boost B T s ψ hF)

/-- A integrabilidade do momento no estado boosted é derivada da original. -/
theorem momentumIntegrable_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (hF : Integrable (momentumIntegrand T.toStressTensorData ψ)) :
    Integrable (momentumIntegrand T.toStressTensorData (B.V s ψ)) := by
  have hi := (integrable_nullPlaneBoost (-s) (momentumIntegrand T.toStressTensorData ψ) hF).const_mul
    (Real.exp (-(2 * s)))
  apply hi.congr
  filter_upwards [] with p
  exact (momentumIntegrand_boost B T s ψ p).symm

/-- Escala do momento usando somente a integrabilidade no estado inicial. -/
theorem nullPlaneMomentum_boost_scaling_of_integrable {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (hF : Integrable (momentumIntegrand T.toStressTensorData ψ)) :
    nullPlaneMomentum T.toStressTensorData (B.V s ψ) =
      Real.exp (-s) * nullPlaneMomentum T.toStressTensorData ψ :=
  nullPlaneMomentum_boost_scaling B T s ψ hF (momentumIntegrable_boost B T s ψ hF)

end TGLExt.NullEnergyScaling

#print axioms TGLExt.NullEnergyScaling.nullEnergy_boost_covariant
#print axioms TGLExt.NullEnergyScaling.nullEnergy_boost_exp_neg_two
#print axioms TGLExt.NullEnergyScaling.integrable_nullPlaneBoost
#print axioms TGLExt.NullEnergyScaling.chargeIntegrand_boost
#print axioms TGLExt.NullEnergyScaling.nullPlaneCharge_boost_invariant
#print axioms TGLExt.NullEnergyScaling.nullPlaneCharge_not_dual_scaling
#print axioms TGLExt.NullEnergyScaling.momentumIntegrand_boost
#print axioms TGLExt.NullEnergyScaling.nullPlaneMomentum_boost_scaling
#print axioms TGLExt.NullEnergyScaling.chargeIntegrable_boost
#print axioms TGLExt.NullEnergyScaling.nullPlaneCharge_boost_invariant_of_integrable
#print axioms TGLExt.NullEnergyScaling.momentumIntegrable_boost
#print axioms TGLExt.NullEnergyScaling.nullPlaneMomentum_boost_scaling_of_integrable
