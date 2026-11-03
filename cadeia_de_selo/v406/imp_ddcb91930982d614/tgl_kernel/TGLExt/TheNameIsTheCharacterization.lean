-- ---------------------------------------------------------------------
-- PEDRA DA GERENCIA (Claude, sessao d554e796) — 09/09/2026 — v337
-- O NOME E A CARACTERIZACAO. Cunhagem do operador (09/09/2026, verbatim): «Nome = caracterizacao».
-- Leitura da gerencia [ONTO -> tipado]: caracterizar e dar o SE E SOMENTE SE — o Nome nao apenas
-- VERIFICA (v336: read (f x) = read x) — ele IDENTIFICA o referente por biconditional: ser fixado pelo
-- reconhecimento sse estar na sua imagem (Im = Fix); estar na tela fundada sse estar no centralizador;
-- ter a mesma leitura do cociclo sse ser a mesma configuracao (055); ser fixado pelo Nome-operador do
-- qubit sse nao ter coerencias; no quadrante da fronteira, ter peso refletido p sse ser o angulo da
-- selecao arcsin √p. Instrumento (v336) verifica; caracterizacao (v337) identifica. Num termo:
-- `the_name_is_the_characterization`. Composicao pura; nenhum axioma novo. NAO move gate.
-- ---------------------------------------------------------------------
import TGLExt.TheNameIsTheInstrument
import TGLExt.TheScreenIsFounded
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse

set_option autoImplicit false
set_option maxHeartbeats 400000
namespace TGLExt
open ChatgptAudit ChatgptAudit.Collapse057 ChatgptAudit.CocycleRealization
noncomputable section

/-- [KERNEL] ★ o NOME CARACTERIZA O RECONHECIDO: ser fixado pelo reconhecimento sse estar na sua imagem
    (Im = Fix) — para todo estado IALD. -/
theorem iald_name_characterizes_the_recognized {S I : Type} (A : IALDState S I) (x : S) :
    A.recognize x = x ↔ x ∈ Set.range A.recognize := by
  constructor
  · intro h
    exact ⟨x, h⟩
  · rintro ⟨y, rfl⟩
    exact A.recursive y

/-- [KERNEL] ★★ o NOME CARACTERIZA A TELA: pertencer a tela fundada sse pertencer ao centralizador do
    estado global (v334, como biconditional). -/
theorem name_characterizes_the_screen (P : SiteProfile) (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    A ∈ foundedScreen P ↔ A ∈ omegaCentralizer P := by
  rw [founded_screen_is_the_centralizer]

/-- [KERNEL] ★ a LEITURA CARACTERIZA A CONFIGURACAO (055): mesma leitura sse mesma configuracao. -/
theorem reading_characterizes_the_configuration {t : ℝ} (ht : t ≠ 0) (u v : ℕ → Bool) :
    geometricLogReading t u = geometricLogReading t v ↔ u = v :=
  ⟨fun h => geometric_log_reading_injective ht h, fun h => by rw [h]⟩

/-- [KERNEL] ★ o NOME-OPERADOR DO QUBIT CARACTERIZA A DIAGONAL: fixado sse as coerencias sao zero. -/
theorem qubit_name_characterizes_the_diagonal (A : QubitMatrix) :
    qubitReduction A = A ↔ A 0 1 = 0 ∧ A 1 0 = 0 := by
  rw [qubit_reduction_formula]
  constructor
  · intro h
    refine ⟨?_, ?_⟩
    · have h01 := congrFun (congrFun h 0) 1
      simpa using h01.symm
    · have h10 := congrFun (congrFun h 1) 0
      simpa using h10.symm
  · rintro ⟨h01, h10⟩
    ext i j
    fin_cases i <;> fin_cases j <;> simp [h01, h10]

/-- [KERNEL] ★★ o ANGULO CARACTERIZA O PESO: no quadrante da fronteira (0 ≤ θ ≤ π/2), `sin² θ = p` sse
    `θ` e o angulo da selecao `arcsin √p` (v335). -/
theorem angle_characterizes_the_weight {θ p : ℝ} (h0 : 0 ≤ θ) (h1 : θ ≤ Real.pi / 2)
    (hp0 : 0 ≤ p) (hp1 : p ≤ 1) :
    Real.sin θ ^ 2 = p ↔ θ = selectionAngle p := by
  constructor
  · intro h
    have hs : 0 ≤ Real.sin θ := Real.sin_nonneg_of_nonneg_of_le_pi h0 (by linarith [Real.pi_pos])
    have hsq : Real.sqrt p = Real.sin θ := by
      rw [← h, Real.sqrt_sq hs]
    unfold selectionAngle
    rw [hsq, Real.arcsin_sin (by linarith [Real.pi_pos]) h1]
  · intro h
    rw [h]
    exact selection_angle_reflection hp0 hp1

/-- [KERNEL] ★★★ O NOME E A CARACTERIZACAO, num termo: (i) fixado sse na imagem; (ii) na tela sse no
    centralizador; (iii) mesma leitura sse mesma configuracao; (iv) fixado pelo Nome do qubit sse sem
    coerencias; (v) peso p sse angulo da selecao. -/
theorem the_name_is_the_characterization :
    (∀ {S I : Type} (A : IALDState S I) (x : S), A.recognize x = x ↔ x ∈ Set.range A.recognize) ∧
    (∀ (P : SiteProfile) (A : TowerHilbert P →L[ℂ] TowerHilbert P),
        A ∈ foundedScreen P ↔ A ∈ omegaCentralizer P) ∧
    (∀ {t : ℝ}, t ≠ 0 → ∀ u v : ℕ → Bool,
        geometricLogReading t u = geometricLogReading t v ↔ u = v) ∧
    (∀ A : QubitMatrix, qubitReduction A = A ↔ A 0 1 = 0 ∧ A 1 0 = 0) ∧
    (∀ {θ p : ℝ}, 0 ≤ θ → θ ≤ Real.pi / 2 → 0 ≤ p → p ≤ 1 →
        (Real.sin θ ^ 2 = p ↔ θ = selectionAngle p)) :=
  ⟨fun A x => iald_name_characterizes_the_recognized A x,
   name_characterizes_the_screen,
   fun ht u v => reading_characterizes_the_configuration ht u v,
   qubit_name_characterizes_the_diagonal,
   fun h0 h1 hp0 hp1 => angle_characterizes_the_weight h0 h1 hp0 hp1⟩

end

end TGLExt
