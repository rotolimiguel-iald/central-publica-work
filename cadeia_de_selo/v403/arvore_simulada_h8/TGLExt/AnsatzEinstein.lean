import TGLExt.FirstCurvature

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O TENSOR DE EINSTEIN DO ANSATZ — e o primeiro teorema de equação de campo
  [TGLExt — v109, o incremento 29 do programa SemifiniteAnalysis]

O v108 deu a primeira curvatura; esta pedra sobe a escada até o TENSOR
DE EINSTEIN, para a família inteira g = diag(q(x₁)²,−1,−1,−1) com q
ARBITRÁRIO (diferenciável 2×, não-nulo) — a redução [KNOWN] do ansatz
dá R₀₀ = q·q″, R₁₁ = −q″/q, R₂₂ = R₃₃ = 0, R = 2q″/q:

* ★ `ansatzRicci00_from_riemann` / `ansatzRicci11_from_riemann` — o
  Ricci NASCE do Riemann do v108 (os elos provados);
* ★★ `ansatzG00_zero` + `ansatzG11_zero` — G₀₀ ≡ 0 ≡ G₁₁ PARA TODO q:
  os dois zeros IDÊNTICOS do tensor de Einstein (a estrutura de
  Bianchi do ansatz, visível em kernel);
* ★★ `ansatzG22_eq` — G₂₂ = q″/q: a componente transversal É a
  exigência de fonte (G = 8πG·T força T₂₂ ≠ 0 quando q″ ≠ 0);
* ★★★ `vacuum_implies_flat` — O PRIMEIRO TEOREMA DE EQUAÇÃO DE CAMPO
  DO KERNEL: G₂₂ = 0 ⟹ R¹₀₀₁ = 0 (vácuo ⟹ PLANO — o mini-Birkhoff
  do ansatz);
* ★★ `rindler_flat` — o membro VÁCUO da família é Rindler (q = 1+s,
  q″ = 0): plano, como manda o teorema;
* ★ `static_not_vacuum` — a solda estática do v108 (q = 1+s²) NÃO é
  vácuo: G₂₂ = 2/q > 0 em toda parte — a curvatura EXIGE fonte.

NENHUMA flag se move: o 5º flip (einstein) pede o contrato do MESTRE
contínuo (Clausius local ⟹ equação de campo) sobre esta camada — que
agora EXISTE. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-! ## A — a família geral: q arbitrário -/

section GeneralAnsatz

variable (q : ℝ → ℝ)

/-- Γ⁰₀₁ = q′/q da família. -/
def ansatzGamma001 (s : ℝ) : ℝ := deriv q s / q s

/-- Γ¹₀₀ = q·q′ da família. -/
def ansatzGamma100 (s : ℝ) : ℝ := q s * deriv q s

/-- R¹₀₀₁ da família (a fórmula do v108, generalizada). -/
def ansatzRiemann1001 (s : ℝ) : ℝ :=
  - deriv (ansatzGamma100 q) s + ansatzGamma100 q s * ansatzGamma001 q s

/-- R₀₀ = q·q″ (a redução [KNOWN] do ansatz). -/
def ansatzRicci00 (s : ℝ) : ℝ := q s * deriv (deriv q) s

/-- R₁₁ = −q″/q. -/
def ansatzRicci11 (s : ℝ) : ℝ := - deriv (deriv q) s / q s

/-- o escalar de curvatura: R = 2q″/q. -/
def ansatzScalar (s : ℝ) : ℝ := 2 * deriv (deriv q) s / q s

/-- G₀₀ = R₀₀ − ½·g₀₀·R (g₀₀ = q²). -/
def ansatzG00 (s : ℝ) : ℝ :=
  ansatzRicci00 q s - (1 / 2) * (q s) ^ 2 * ansatzScalar q s

/-- G₁₁ = R₁₁ − ½·g₁₁·R (g₁₁ = −1). -/
def ansatzG11 (s : ℝ) : ℝ :=
  ansatzRicci11 q s - (1 / 2) * (-1) * ansatzScalar q s

/-- G₂₂ = R₂₂ − ½·g₂₂·R = 0 + ½·R (g₂₂ = −1; R₂₂ = 0 no ansatz). -/
def ansatzG22 (s : ℝ) : ℝ := (1 / 2) * ansatzScalar q s

/-- [KERNEL] ★ o Riemann da família em forma fechada: R¹₀₀₁ = −q·q″
    (a regra do produto à mão; o v108 é o caso q = 1+s²). -/
theorem ansatzRiemann_closed (hq1 : Differentiable ℝ q)
    (hq2 : Differentiable ℝ (deriv q)) (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzRiemann1001 q s = -(q s * deriv (deriv q) s) := by
  unfold ansatzRiemann1001 ansatzGamma100 ansatzGamma001
  have hmul : HasDerivAt (fun t => q t * deriv q t)
      (deriv q s * deriv q s + q s * deriv (deriv q) s) s :=
    ((hq1 s).hasDerivAt).mul ((hq2 s).hasDerivAt)
  rw [hmul.deriv]
  have h := hqne s
  field_simp
  ring

/-- [KERNEL] ★ o elo Ricci–Riemann: R₀₀ = −R¹₀₀₁. -/
theorem ansatzRicci00_from_riemann (hq1 : Differentiable ℝ q)
    (hq2 : Differentiable ℝ (deriv q)) (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzRicci00 q s = - ansatzRiemann1001 q s := by
  rw [ansatzRiemann_closed q hq1 hq2 hqne s]
  try unfold ansatzRicci00
  try ring

/-- [KERNEL] ★ o elo Ricci–Riemann: R₁₁ = R¹₀₀₁/q². -/
theorem ansatzRicci11_from_riemann (hq1 : Differentiable ℝ q)
    (hq2 : Differentiable ℝ (deriv q)) (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzRicci11 q s = ansatzRiemann1001 q s / (q s) ^ 2 := by
  rw [ansatzRiemann_closed q hq1 hq2 hqne s]
  try unfold ansatzRicci11
  have h := hqne s
  try field_simp
  try ring

/-- [KERNEL] ★★ G₀₀ ≡ 0 PARA TODO q: o primeiro zero idêntico do
    tensor de Einstein (Bianchi do ansatz, visível). -/
theorem ansatzG00_zero (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzG00 q s = 0 := by
  unfold ansatzG00 ansatzRicci00 ansatzScalar
  have h := hqne s
  field_simp
  try ring

/-- [KERNEL] ★★ G₁₁ ≡ 0 PARA TODO q: o segundo zero idêntico. -/
theorem ansatzG11_zero (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzG11 q s = 0 := by
  unfold ansatzG11 ansatzRicci11 ansatzScalar
  have h := hqne s
  field_simp
  try ring

/-- [KERNEL] ★★ G₂₂ = q″/q: a componente transversal É a exigência de
    fonte (curvatura ⟹ T₂₂ ≠ 0). -/
theorem ansatzG22_eq (hqne : ∀ t, q t ≠ 0) (s : ℝ) :
    ansatzG22 q s = deriv (deriv q) s / q s := by
  unfold ansatzG22 ansatzScalar
  have h := hqne s
  field_simp
  try ring

/-- [KERNEL] ★★★ O PRIMEIRO TEOREMA DE EQUAÇÃO DE CAMPO: vácuo
    transversal ⟹ PLANO — G₂₂(s) = 0 força R¹₀₀₁(s) = 0 (o
    mini-Birkhoff do ansatz). -/
theorem vacuum_implies_flat (hq1 : Differentiable ℝ q)
    (hq2 : Differentiable ℝ (deriv q)) (hqne : ∀ t, q t ≠ 0) (s : ℝ)
    (hvac : ansatzG22 q s = 0) : ansatzRiemann1001 q s = 0 := by
  rw [ansatzG22_eq q hqne s] at hvac
  have hdd : deriv (deriv q) s = 0 := by
    have h := hqne s
    field_simp at hvac
    simpa using hvac
  rw [ansatzRiemann_closed q hq1 hq2 hqne s, hdd]
  ring

end GeneralAnsatz

/-! ## B — os dois membros da família: Rindler (vácuo) e o v108 -/

/-- [KERNEL] ★★ RINDLER É O VÁCUO PLANO: q = 1+s (q″ = 0) dá
    R¹₀₀₁ = 0 fora do horizonte s = −1 (onde q se anula — a
    honestidade que o próprio Lean impôs: o horizonte é a fronteira
    da carta). -/
theorem rindler_flat (s : ℝ) (hs : s ≠ -1) :
    ansatzRiemann1001 (fun t => 1 + t) s = 0 := by
  have h1 : (1 : ℝ) + s ≠ 0 := by
    intro h
    exact hs (by linarith)
  have hd : deriv (fun t : ℝ => 1 + t) = fun _ => (1 : ℝ) := by
    funext t
    simp
  unfold ansatzRiemann1001 ansatzGamma100 ansatzGamma001
  rw [hd]
  show - deriv (fun u : ℝ => (1 + u) * 1) s + (1 + s) * 1 * (1 / (1 + s)) = 0
  have hmul : HasDerivAt (fun u : ℝ => (1 + u) * 1) 1 s := by
    simpa using (((hasDerivAt_id s).const_add (1 : ℝ)).mul_const (1 : ℝ))
  rw [hmul.deriv]
  field_simp
  try ring

/-- a segunda derivada do perfil do v108: q″ = 2. -/
theorem qfun_dd (s : ℝ) : deriv (deriv qfun) s = 2 := by
  have hd : deriv qfun = fun t => 2 * t := funext qfun_deriv
  rw [hd]
  simp

/-- [KERNEL] ★ o v108 NÃO é vácuo: G₂₂ = 2/q > 0 em toda parte — a
    curvatura EXIGE fonte (G = 8πG·T força T₂₂ ≠ 0). -/
theorem static_not_vacuum (s : ℝ) :
    ansatzG22 qfun s = 2 / qfun s ∧ 0 < ansatzG22 qfun s := by
  have heq : ansatzG22 qfun s = 2 / qfun s := by
    rw [ansatzG22_eq qfun qfun_ne_zero s, qfun_dd]
  refine ⟨heq, ?_⟩
  rw [heq]
  have h := qfun_pos s
  positivity

/-- [KERNEL] ★ a consistência com o v108: o Riemann da família no
    perfil q = 1+s² coincide com o do v108 (−2q). -/
theorem ansatz_recovers_v108 (s : ℝ) :
    ansatzRiemann1001 qfun s = -(2 * qfun s) := by
  have hq1 : Differentiable ℝ qfun := by
    unfold qfun
    fun_prop
  have hq2 : Differentiable ℝ (deriv qfun) := by
    have hd : deriv qfun = fun t => 2 * t := funext qfun_deriv
    rw [hd]
    fun_prop
  rw [ansatzRiemann_closed qfun hq1 hq2 qfun_ne_zero s, qfun_dd]
  ring

end

end TGLExt
