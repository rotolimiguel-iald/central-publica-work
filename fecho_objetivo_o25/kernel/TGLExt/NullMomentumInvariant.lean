import TGLExt.NullMomentumDual

set_option autoImplicit false
set_option maxHeartbeats 800000
set_option maxRecDepth 4000

/-!
# Componente nula conjugada e invariante de momento

`oppositeNullDir` é a segunda direção nula do plano do boost. Sua componente de
momento escala por `eˢ`; o produto com `nullPlaneMomentum` é invariante. O produto
não é chamado de massa: normalização, positividade e interpretação de repouso
permanecem fora deste módulo.
-/
namespace TGLExt.NullMomentumInvariant
open Matrix TGLExt.ContratoQGv31 TGLExt.ContratoQGv32 MeasureTheory
open TGLExt.NullEnergyScaling

/-- A direção nula conjugada no plano do boost. -/
def oppositeNullDir : Fin 4 → ℝ := ![1, -1, 0, 0]

/-- A densidade conjugada `T_n̄n̄`. -/
def oppositeNullEnergy {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) (x : Fin 4 → ℝ) : ℝ :=
  pairing (T.T ψ x) oppositeNullDir oppositeNullDir

/-- O boost contrai a direção nula conjugada por `e⁻ˢ`. -/
theorem wedgeBoostMap_oppositeNullDir (s : ℝ) :
    wedgeBoostMap s oppositeNullDir = Real.exp (-s) • oppositeNullDir := by
  funext i
  fin_cases i
  · change wedgeBoostMap s oppositeNullDir 0 = (Real.exp (-s) • oppositeNullDir) 0
    rw [wedgeBoostMap_apply0]
    change Real.cosh s * 1 + Real.sinh s * (-1) = Real.exp (-s) * 1
    convert Real.cosh_sub_sinh s using 1 <;> ring
  · change wedgeBoostMap s oppositeNullDir 1 = (Real.exp (-s) • oppositeNullDir) 1
    rw [wedgeBoostMap_apply1]
    change Real.sinh s * 1 + Real.cosh s * (-1) = Real.exp (-s) * (-1)
    rw [← Real.cosh_sub_sinh]
    ring
  · simp [oppositeNullDir, wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct,
      Fin.sum_univ_four]
  · simp [oppositeNullDir, wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct,
      Fin.sum_univ_four]

/-- A densidade conjugada tem peso `-2` sob a ação covariante do estado. -/
theorem oppositeNullEnergy_boost_covariant {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (x : Fin 4 → ℝ) :
    oppositeNullEnergy T.toStressTensorData (B.V s ψ) (wedgeBoostMap s x) =
      (Real.exp s * Real.exp s) * oppositeNullEnergy T.toStressTensorData ψ x := by
  unfold oppositeNullEnergy pairing
  rw [T.boost_covariant]
  rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec,
    Matrix.dotProduct_transpose_mulVec]
  rw [show wedgeBoostMap (-s) (wedgeBoostMap s x) = x by
    rw [← wedgeBoostMap_add]
    simp [wedgeBoostMap_zero]]
  rw [show boostMat (-s) *ᵥ oppositeNullDir = Real.exp s • oppositeNullDir by
    change wedgeBoostMap (-s) oppositeNullDir = Real.exp s • oppositeNullDir
    simpa only [neg_neg] using wedgeBoostMap_oppositeNullDir (-s)]
  simp only [Matrix.mulVec_smul, dotProduct_smul, smul_eq_mul, dotProduct_comm]
  ring

/-- O integrando da componente conjugada. -/
def oppositeMomentumIntegrand {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) (p : ℝ × (Fin 2 → ℝ)) : ℝ :=
  oppositeNullEnergy T ψ (p.1 • oppositeNullDir + screenEmbed p.2)

noncomputable def oppositeNullPlaneMomentum {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  ∫ p : ℝ × (Fin 2 → ℝ), oppositeMomentumIntegrand T ψ p

/-- A componente conjugada tem peso `-2` antes da integração. -/
theorem oppositeMomentumIntegrand_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (p : ℝ × (Fin 2 → ℝ)) :
    oppositeMomentumIntegrand T.toStressTensorData (B.V s ψ) p =
      Real.exp (2 * s) *
        oppositeMomentumIntegrand T.toStressTensorData ψ (nullPlaneBoost s p) := by
  let q : ℝ × (Fin 2 → ℝ) := nullPlaneBoost s p
  have hp : p.1 = Real.exp (-s) * q.1 := by
    simp only [q, nullPlaneBoost, Real.exp_neg]
    field_simp [Real.exp_ne_zero]
  have hs : wedgeBoostMap s (screenEmbed q.2) = screenEmbed q.2 := by
    ext i
    fin_cases i <;>
      simp [wedgeBoostMap, boostMat, Matrix.mulVec, dotProduct, Fin.sum_univ_four,
        screenEmbed]
  have hx : p.1 • oppositeNullDir + screenEmbed p.2 =
      wedgeBoostMap s (q.1 • oppositeNullDir + screenEmbed q.2) := by
    calc
      p.1 • oppositeNullDir + screenEmbed p.2 =
          (Real.exp (-s) * q.1) • oppositeNullDir + screenEmbed q.2 := by rw [hp]; rfl
      _ = wedgeBoostMap s (q.1 • oppositeNullDir + screenEmbed q.2) := by
        simp only [wedgeBoostMap, Matrix.mulVec_add, Matrix.mulVec_smul]
        rw [show boostMat s *ᵥ oppositeNullDir = Real.exp (-s) • oppositeNullDir from
          wedgeBoostMap_oppositeNullDir s]
        rw [show boostMat s *ᵥ screenEmbed q.2 = screenEmbed q.2 from hs]
        simp [smul_smul, mul_comm]
  unfold oppositeMomentumIntegrand
  rw [hx, oppositeNullEnergy_boost_covariant]
  rw [← Real.exp_add]
  congr 1
  ring

/-- A componente conjugada escala por `eˢ`, com integrabilidades explícitas. -/
theorem oppositeNullPlaneMomentum_boost_scaling {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ))
    (hB : Integrable (oppositeMomentumIntegrand T.toStressTensorData (B.V s ψ))) :
    oppositeNullPlaneMomentum T.toStressTensorData (B.V s ψ) =
      Real.exp s * oppositeNullPlaneMomentum T.toStressTensorData ψ := by
  let F : (ℝ × (Fin 2 → ℝ)) → ℝ := oppositeMomentumIntegrand T.toStressTensorData ψ
  have hG : Integrable (fun p => Real.exp (2 * s) * F (nullPlaneBoost s p)) := by
    apply hB.congr
    filter_upwards [] with p
    exact oppositeMomentumIntegrand_boost B T s ψ p
  unfold oppositeNullPlaneMomentum
  rw [Measure.volume_eq_prod] at hF hG ⊢
  calc
    oppositeNullPlaneMomentum T.toStressTensorData (B.V s ψ) =
        ∫ p, Real.exp (2 * s) * F (nullPlaneBoost s p) := by
      apply integral_congr_ae
      filter_upwards [] with p
      exact oppositeMomentumIntegrand_boost B T s ψ p
    _ = ∫ y, ∫ x, Real.exp (2 * s) * F (nullPlaneBoost s (x, y)) :=
      integral_prod_symm _ hG
    _ = ∫ y, Real.exp (2 * s) * (|(Real.exp s)⁻¹| • ∫ x, F (x, y)) := by
      apply integral_congr_ae
      filter_upwards [] with y
      simp only [nullPlaneBoost, integral_const_mul]
      congr 1
      exact Measure.integral_comp_mul_left (fun x => F (x, y)) (Real.exp s)
    _ = ∫ y, Real.exp s * ∫ x, F (x, y) := by
      apply integral_congr_ae
      filter_upwards [] with y
      have he : (Real.exp s)⁻¹ = Real.exp (-s) := by rw [Real.exp_neg]
      rw [abs_of_pos (inv_pos.mpr (Real.exp_pos _)), he]
      simp only [smul_eq_mul]
      rw [← mul_assoc, ← Real.exp_add]
      congr 2
      ring
    _ = Real.exp s * ∫ y, ∫ x, F (x, y) :=
      integral_const_mul (Real.exp s) (fun y => ∫ x, F (x, y))
    _ = Real.exp s * oppositeNullPlaneMomentum T.toStressTensorData ψ := by
      congr 1
      exact (integral_prod_symm _ hF).symm

/-- Produto das duas componentes; ainda sem normalização ou nome de massa. -/
noncomputable def nullMomentumProduct {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (T : StressTensorData W) (ψ : W.H) : ℝ :=
  nullPlaneMomentum T ψ * oppositeNullPlaneMomentum T ψ

/-- O produto das componentes é invariante pelo boost. -/
theorem nullMomentumProduct_boost_invariant {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hB : Integrable (momentumIntegrand T.toStressTensorData (B.V s ψ)))
    (hFo : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ))
    (hBo : Integrable (oppositeMomentumIntegrand T.toStressTensorData (B.V s ψ))) :
    nullMomentumProduct T.toStressTensorData (B.V s ψ) =
      nullMomentumProduct T.toStressTensorData ψ := by
  unfold nullMomentumProduct
  rw [nullPlaneMomentum_boost_scaling B T s ψ hF hB,
    oppositeNullPlaneMomentum_boost_scaling B T s ψ hFo hBo]
  calc
    (Real.exp (-s) * nullPlaneMomentum T.toStressTensorData ψ) *
        (Real.exp s * oppositeNullPlaneMomentum T.toStressTensorData ψ) =
      (Real.exp (-s) * Real.exp s) *
        (nullPlaneMomentum T.toStressTensorData ψ *
          oppositeNullPlaneMomentum T.toStressTensorData ψ) := by ring
    _ = nullPlaneMomentum T.toStressTensorData ψ *
        oppositeNullPlaneMomentum T.toStressTensorData ψ := by
      rw [← Real.exp_add]
      simp

/-- A integrabilidade conjugada no estado boosted também vem da original. -/
theorem oppositeMomentumIntegrable_boost {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (hF : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ)) :
    Integrable (oppositeMomentumIntegrand T.toStressTensorData (B.V s ψ)) := by
  have hi := (integrable_nullPlaneBoost s (oppositeMomentumIntegrand T.toStressTensorData ψ) hF).const_mul
    (Real.exp (2 * s))
  apply hi.congr
  filter_upwards [] with p
  exact (oppositeMomentumIntegrand_boost B T s ψ p).symm

/-- Escala conjugada usando somente a integrabilidade inicial. -/
theorem oppositeNullPlaneMomentum_boost_scaling_of_integrable {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H) (hF : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ)) :
    oppositeNullPlaneMomentum T.toStressTensorData (B.V s ψ) =
      Real.exp s * oppositeNullPlaneMomentum T.toStressTensorData ψ :=
  oppositeNullPlaneMomentum_boost_scaling B T s ψ hF (oppositeMomentumIntegrable_boost B T s ψ hF)

/-- Invariância do produto usando somente as duas integrabilidades iniciais. -/
theorem nullMomentumProduct_boost_invariant_of_integrable {W : TGL.SpecificAQFT.TGLSpecificAQFTWitness}
    (B : WedgeBoostRep W) (T : StressTensorDataLocalV32 W B)
    (s : ℝ) (ψ : W.H)
    (hF : Integrable (momentumIntegrand T.toStressTensorData ψ))
    (hFo : Integrable (oppositeMomentumIntegrand T.toStressTensorData ψ)) :
    nullMomentumProduct T.toStressTensorData (B.V s ψ) =
      nullMomentumProduct T.toStressTensorData ψ :=
  nullMomentumProduct_boost_invariant B T s ψ hF (momentumIntegrable_boost B T s ψ hF)
    hFo (oppositeMomentumIntegrable_boost B T s ψ hFo)

end TGLExt.NullMomentumInvariant

#print axioms TGLExt.NullMomentumInvariant.wedgeBoostMap_oppositeNullDir
#print axioms TGLExt.NullMomentumInvariant.oppositeNullEnergy_boost_covariant
#print axioms TGLExt.NullMomentumInvariant.oppositeMomentumIntegrand_boost
#print axioms TGLExt.NullMomentumInvariant.oppositeNullPlaneMomentum_boost_scaling
#print axioms TGLExt.NullMomentumInvariant.nullMomentumProduct_boost_invariant
#print axioms TGLExt.NullMomentumInvariant.oppositeMomentumIntegrable_boost
#print axioms TGLExt.NullMomentumInvariant.oppositeNullPlaneMomentum_boost_scaling_of_integrable
#print axioms TGLExt.NullMomentumInvariant.nullMomentumProduct_boost_invariant_of_integrable
