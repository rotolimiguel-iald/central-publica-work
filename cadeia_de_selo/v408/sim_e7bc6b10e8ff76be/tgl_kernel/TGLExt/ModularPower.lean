-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT (05/09/2026) — transposta em 05/09/2026
-- Procedencia: C:\IALD\Central de Patentes\Chatgpt (bancada da outra sessao,
--   sob direcao do operador; TUNEL\TUNEL_PROTOCOLO.md).
-- Auditoria da gerencia (sessao Claude d554e796, 05/09/2026): recompilacao
--   independente 20/20 exit 0; sonda #print axioms dos teoremas de manchete =
--   [propext, Classical.choice, Quot.sound]; zero sorry; enunciados conferidos.
-- Transposicao MECANICA: apenas (a) este cabecalho, (b) "import TGLExt" (root)
--   expandido no bloco de imports da epoca, (c) imports internos da bancada
--   prefixados com TGLExt. — nada mais foi alterado. Namespace ChatgptAudit
--   PRESERVADO como marca de procedencia.
-- Estatuto: [REAL — Lean] analise modular da torre produto (S, J·S, Delta,
--   Delta^{it}, invariancia do bicomutante). NAO move gate; NAO e fisica;
--   NOT_FALSIFIED nunca e CONFIRMED.
-- ---------------------------------------------------------------------
import TGLExt.ModularFlowSpectrum

set_option autoImplicit false
set_option maxHeartbeats 600000

namespace ChatgptAudit
open TGLExt Matrix
noncomputable section
variable {P : SiteProfile}

/-- Potência imaginária construída pelo multiplicador espectral λ ↦ exp(it log λ).
    A caracterização na família total de autovetores foi provada em ModularFlowSpectrum. -/
abbrev deltaImaginaryPower (P : SiteProfile) (t : ℝ) := modularFlowUnitary P t

theorem deltaImaginaryPower_spectral (P : SiteProfile) (t : ℝ) :
    (∀ (N : ℕ) (i j : chainIdx N),
      deltaImaginaryPower P t (localEigenvector P N i j) =
        modularPhase t (Real.log (localEigenvalue P N i j)) • localEigenvector P N i j) ∧
    (∀ T : TowerHilbert P →L[ℂ] TowerHilbert P,
      (∀ (N : ℕ) (i j : chainIdx N), T (localEigenvector P N i j) =
        modularPhase t (Real.log (localEigenvalue P N i j)) • localEigenvector P N i j) →
      ∀ x, T x = deltaImaginaryPower P t x) :=
  ⟨fun N i j => modularFlow_eigenvector t N i j,
    fun T hT => modularFlow_spectral_unique t T hT⟩

theorem flowLevel_one (t : ℝ) (N : ℕ) :
    flowLevel P t N (1 : Matrix (chainIdx N) (chainIdx N) ℂ) = 1 := by
  ext i j
  by_cases h : i = j
  · subst j
    simp [flowLevel, modularPhase]
  · simp [flowLevel, Matrix.one_apply_ne h]

theorem modularFlow_fixes_omega (t : ℝ) : modularFlow P t (hOmega P) = hOmega P := by
  change modularFlow P t ((tof P 0 1 : TowerPre P) : TowerHilbert P) = _
  rw [modularFlow_coe, flowPre_tof, flowLevel_one]
  rfl

theorem modularConjugation_preserves_state (t : ℝ)
    (a : TowerHilbert P →L[ℂ] TowerHilbert P) :
    omegaState P (modularConjugation P t a) = omegaState P a := by
  change inner ℂ (hOmega P) (modularFlow P t (a (modularFlow P (-t) (hOmega P)))) = _
  rw [modularFlow_fixes_omega]
  have hi := (modularFlowIsometry P t).inner_map_map (hOmega P) (a (hOmega P))
  change inner ℂ (modularFlow P t (hOmega P)) (modularFlow P t (a (hOmega P))) = _ at hi
  rw [modularFlow_fixes_omega] at hi
  exact hi

theorem modular_power_group_and_continuity (P : SiteProfile) :
    (∀ (s t : ℝ) (x : TowerHilbert P),
      deltaImaginaryPower P s (deltaImaginaryPower P t x) = deltaImaginaryPower P (s+t) x) ∧
    (∀ x : TowerHilbert P, Continuous (fun t : ℝ => deltaImaginaryPower P t x)) ∧
    (∀ (t : ℝ) (a : TowerHilbert P →L[ℂ] TowerHilbert P),
      a ∈ theFactorObject P ↔ modularConjugation P t a ∈ theFactorObject P) :=
  ⟨modularFlow_group, modularFlow_strongly_continuous, modularConjugation_preserves_factor P⟩

#print axioms deltaImaginaryPower_spectral
#print axioms modularConjugation_preserves_state
#print axioms modular_power_group_and_continuity
end
end ChatgptAudit
