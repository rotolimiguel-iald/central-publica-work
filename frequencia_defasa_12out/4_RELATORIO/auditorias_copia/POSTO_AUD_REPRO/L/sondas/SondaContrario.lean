/- SONDA ADVERSARIAL do auditor REPRO (sandbox): tentar PROVAR O CONTRARIO das afirmacoes centrais da pedra.
   ESPERADO: cada `example` abaixo FALHA (erro do Lean). Um `example` que compile seria contradicao com a pedra.
   (A refutacao positiva de cada contrario esta em SondaContraexemplos.lean, secao II.) -/
import TheUnitIsTheRank

set_option autoImplicit false

open Matrix Filter Topology

namespace TGLExt.TheUnitIsTheRank

namespace SondaContrario

noncomputable section

-- K1 (contra B5.a): o ponto final em π/4 teria posto 1
example : (diagExpect (rhoOut (Real.pi / 4))).rank = 1 := by
  rw [endpoint_rank_one_iff]
  simp

-- K2 (contra B2.b): o anticomutador em θ_M seria nulo
example (c : TGLCoupling) : anticomm (Qtheta (thetaMiguel c.beta)) rhoStar = 0 := by
  rw [anticomm_zero_iff]
  simp [thetaMiguel]

-- K3 (contra B5.e(ii)): D preservaria o posto para todo θ
example : ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro θ
  rw [(fractal_one_is_rank_one θ).1, endpoint_rank_one_iff]
  simp

-- K4 (contra B9.a): transmitir bastaria para defasar
example (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) :
    ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 0) → dephasingActs g θ := by
  intro θ _
  exact ⟨1, by simp [dephase, rhoOut_eq, hg0]⟩

-- K5 (contra B3.b): o vazamento em θ_M seria zero
example (c : TGLCoupling) : (rhoStar * Qtheta (thetaMiguel c.beta)).trace = 0 := by
  rw [leak_at_thetaMiguel]
  simp

-- K6 (contra B7.a2): o angulo teria limite
example : ∃ L : ℝ, Tendsto (fun k : ℕ => Real.sin (k * 1) ^ 2) atTop (𝓝 L) := by
  refine ⟨1 / 2, ?_⟩
  simp

-- K7 (contra P1.a): pureza sem posto 1 (I/2 seria pura)
example : (halfId ^ 2).trace = 1 := by
  simp [halfId, sq]

-- K8 (contra B6.a): o vazamento lido por ρ* dependeria do tempo
example (θ : ℝ) : (rhoStar * dephase unitRates 1 (Qtheta θ)).trace ≠ (Real.sin θ : ℂ) ^ 2 := by
  intro h
  simp [leak_survives_dephasing θ unitRates unitRates_spec.1 1] at h

end

end SondaContrario

end TGLExt.TheUnitIsTheRank
