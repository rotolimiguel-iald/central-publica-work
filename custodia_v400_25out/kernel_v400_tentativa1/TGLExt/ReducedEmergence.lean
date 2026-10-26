import TGLExt.SolvedEquation

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A EMERGÊNCIA REDUZIDA: Clausius nulo ⟹ equação de campo, na família
  [TGLExt — v112, o incremento 32 do programa SemifiniteAnalysis]

A parede do 5º flip é a EMERGÊNCIA termodinâmica contínua (Jacobson).
Esta pedra a ENCOLHE, provando a versão redutível na família do
ansatz — e o mecanismo é a estrutura de BIANCHI do v109:

* ★★ `null_contraction_reads_source` — a contração nula TRANSVERSAL
  do tensor de Einstein, G_kk = G₀₀/q² + G₂₂, é IDÊNTICA a G₂₂
  (porque G₀₀ ≡ 0, o zero de Bianchi): a contabilidade de Clausius em
  QUALQUER congruência nula transversal lê EXATAMENTE a exigência de
  fonte;
* `ReducedEmergenceData` — o insumo TERMODINÂMICO em forma nula:
  Clausius lido como G_kk = T_kk (com η = 1/4G e o coeficiente 8πG
  vindos da face finita do MESTRE v74 [KERNEL]);
* ★★★ `emergence_forces_field_equation` — CLAUSIUS NULO ⟹ A EQUAÇÃO
  DE CAMPO (G₂₂ = T) — a emergência de Jacobson REDUZIDA à família,
  provada;
* ★★ `emergence_zero_flat` — Clausius com fonte nula ⟹ PLANO (a
  emergência devolve o vácuo ⟹ plano do v109);
* ★★ `theReducedEmergence` — habitante: a fonte κ² emerge na solução
  global cosh (o elo com o v111).

O QUE AINDA FALTA (a parede, encolhida e nomeada): a emergência PLENA
pede métricas GERAIS e Raychaudhuri contínuo — fora da mathlib de
hoje; o 5º flip segue reservado. β jamais literal. Sem sorry, sem
axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a contração nula transversal -/

/-- a contração nula transversal do tensor de Einstein do ansatz:
    G_kk = G₀₀·(k⁰)² + G₂₂·(k²)² com k = (1/q, 0, 1, 0). -/
def ansatzNullG (q : ℝ → ℝ) (s : ℝ) : ℝ :=
  ansatzG00 q s / (q s) ^ 2 + ansatzG22 q s

/-- [KERNEL] ★★ O ZERO DE BIANCHI FAZ CLAUSIUS LER A FONTE: a
    contração nula transversal é IDÊNTICA a G₂₂ (G₀₀ ≡ 0, v109) —
    a contabilidade nula não vê nada além da exigência de fonte. -/
theorem null_contraction_reads_source (q : ℝ → ℝ)
    (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzNullG q s = ansatzG22 q s := by
  unfold ansatzNullG
  rw [ansatzG00_zero q hqne s]
  simp

/-! ## B — o insumo termodinâmico e a emergência -/

/-- [DATA] o insumo TERMODINÂMICO em forma nula: a lei de Clausius
    δQ = TδS com S = ηA (η = 1/4G, do MESTRE v74 na face finita
    [KERNEL]) lida em toda congruência nula transversal:
    G_kk(s) = T(s). -/
structure ReducedEmergenceData where
  q : ℝ → ℝ
  q_ne : ∀ s, q s ≠ 0
  T : ℝ → ℝ
  clausius : ∀ s, ansatzNullG q s = T s

/-- [KERNEL] ★★★ A EMERGÊNCIA REDUZIDA: Clausius nulo FORÇA a equação
    de campo na família — G₂₂ = T em toda parte (Jacobson reduzido,
    provado). -/
theorem emergence_forces_field_equation (E : ReducedEmergenceData)
    (s : ℝ) : ansatzG22 E.q s = E.T s := by
  rw [← null_contraction_reads_source E.q E.q_ne s]
  exact E.clausius s

/-- [KERNEL] ★★ A EMERGÊNCIA DEVOLVE O VÁCUO ⟹ PLANO: fonte
    termodinâmica nula ⟹ curvatura nula (com as hipóteses de
    diferenciabilidade da família). -/
theorem emergence_zero_flat (E : ReducedEmergenceData)
    (hq1 : Differentiable ℝ E.q) (hq2 : Differentiable ℝ (deriv E.q))
    (hT : ∀ s, E.T s = 0) (s : ℝ) :
    ansatzRiemann1001 E.q s = 0 := by
  apply vacuum_implies_flat E.q hq1 hq2 E.q_ne s
  rw [emergence_forces_field_equation E s]
  exact hT s

/-- [KERNEL] ★★ o habitante: a fonte constante κ² EMERGE na solução
    global cosh — o elo termodinâmica → equação → solução (v111). -/
def theReducedEmergence (kappa : ℝ) : ReducedEmergenceData where
  q := coshProfile kappa
  q_ne := coshProfile_ne_zero kappa
  T := fun _ => kappa ^ 2
  clausius := fun s => by
    rw [null_contraction_reads_source (coshProfile kappa)
      (coshProfile_ne_zero kappa) s]
    exact cosh_solves_field_equation kappa s

/-- [KERNEL] ★ a coerência do habitante: a emergência entrega G₂₂ = κ²
    (a mesma equação resolvida do v111, agora vinda do insumo
    termodinâmico). -/
theorem reduced_emergence_delivers (kappa s : ℝ) :
    ansatzG22 (theReducedEmergence kappa).q s = kappa ^ 2 :=
  emergence_forces_field_equation (theReducedEmergence kappa) s

end

end TGLExt
