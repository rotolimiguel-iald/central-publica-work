import TheUnitIsTheRank

/-!
# SONDA S1 (auditor REPRO r2) — PROVAR O CONTRÁRIO: tentativas que TÊM de falhar.
Cada `example` abaixo enuncia o CONTRÁRIO de um teorema da pedra e tenta fechá-lo com automação ampla.
Esperado: 6 exemplos, cada um com erro (a pedra está no trio de axiomas; um sucesso aqui seria inconsistência).
-/

open TGLExt TGLExt.TheUnitIsTheRank Matrix Filter Topology

-- S1.1 contrário de B1.a: posto ρ* = 2
example : rhoStar.rank = 2 := by
  rw [rhoStar_eq]
  simp

-- S1.2 contrário de B5.e(ii): o posto sobrevive à defasagem para todo θ
example : ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro θ
  simp [diagExpect, rhoOut_eq]

-- S1.3 contrário de B9.a: a leitura literal (transmitir ⟹ D atua) vale
example : ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 0) → dephasingActs unitRates θ := by
  intro θ h
  simp [dephasingActs, dephase, rhoOut_eq, unitRates] at *

-- S1.4 contrário de B3.b: o vazamento em θ_M NÃO é β
example (c : TGLCoupling) : (rhoStar * Qtheta (thetaMiguel c.beta)).trace ≠ (c.beta : ℂ) := by
  simp [leak_eq]

-- S1.5 contrário de B2.a em θ = π/4: o anticomutador se anula
example : anticomm (Qtheta (Real.pi / 4)) rhoStar = 0 := by
  rw [anticomm_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

-- S1.6 contrário de B7.a2 em θ = 1: sin²(k) converge (a 1/2)
example : ∃ L : ℝ, Tendsto (fun k : ℕ => Real.sin (k * 1) ^ 2) atTop (𝓝 L) := by
  refine ⟨1 / 2, ?_⟩
  simp
