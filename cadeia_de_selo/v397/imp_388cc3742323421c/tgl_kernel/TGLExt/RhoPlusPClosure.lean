import TGLExt.LightIsJ

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# O FECHAMENTO ρ+p: a identidade de fundo da TGL como fluido
  [TGLExt — v154, a derivação do operador (08/08/2026)]

O operador: "δρ_TGL = β(δρ + δp) — a resposta da TGL é LOCAL, acoplada à
soma ρ+p do setor que a produz, não um δw." A consequência algébrica,
verificada numericamente na sessão de 08/08 (resíduo 2,2e-16): com
p_r = ρ_r/3 (radiação), p_m = 0 (matéria) e p_Λ = −ρ_Λ (vácuo),

  ρ_TGL = β(ρ+p) = β[(4/3)ρ_r + ρ_m]   —   ρ_Λ CANCELA EXATO.

E o fundo total: H² ∝ (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ — a TGL no fundo não é
modelo novo; é um ponto no plano (N_eff, ω_c) que todo pipeline de CMB já
sabe percorrer. [Crédito: a forma ρ+p é derivação do operador, 08/08/2026.]

* ★★ `lambda_drops_out` — O VÁCUO NÃO PAGA: ρ_Λ + p_Λ = 0 — o setor w=−1
  é invisível ao acoplamento ρ+p;
* ★★★ `closure_identity` — A IDENTIDADE DO FECHAMENTO: β·Σ(ρ_i+p_i) =
  β[(4/3)ρ_r + ρ_m] — exata, para quaisquer densidades;
* ★★ `hubble_form` — A FORMA DO FUNDO: ρ_total + ρ_TGL =
  (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ — o reescalonamento que o CMB já mede;
* `w_bounds` — a face algébrica da equação de estado efetiva: com
  p_T = (β/3)(4/3)ρ_r, w_T = p_T/ρ_T ∈ [0, 1/3]; w_T = 1/3 no domínio da
  radiação (ρ_m=0) e w_T = 0 no da matéria (ρ_r=0) — a conservação FORÇA
  a interpolação (versão dinâmica verificada no módulo);
* ★★★ `the_background_closure` — a síntese em um teorema.

Honestidades: esta é a face ALGÉBRICA [REAL]; a versão dinâmica
(p_T = −β·ṗ/3H; w=0,3325→0,0014) e a validação em CAMB são do módulo
[VERIFICADO 08/08]; a hipótese declarada é a não-troca de energia entre
setores; o fechamento PERTURBATIVO segue INDETERMINADO — e é o próprio
Lema 3 visto do lado do fluido. β jamais literal. O gate NÃO se move.
-/

namespace TGLExt

noncomputable section

/-- [KERNEL] ★★ O VÁCUO NÃO PAGA: para w = −1, ρ + p = 0 — o setor Λ é
    invisível ao acoplamento ρ+p. -/
theorem lambda_drops_out (ρΛ : ℝ) : ρΛ + (-ρΛ) = 0 := by ring

/-- [KERNEL] ★★★ A IDENTIDADE DO FECHAMENTO: com p_r = ρ_r/3, p_m = 0 e
    p_Λ = −ρ_Λ, a soma β·Σ(ρ_i+p_i) fecha EXATA em β[(4/3)ρ_r + ρ_m] —
    ρ_Λ cancela, para quaisquer densidades. -/
theorem closure_identity (β ρr ρm ρΛ : ℝ) :
    β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
      = β * ((4 / 3) * ρr + ρm) := by ring

/-- [KERNEL] ★★ A FORMA DO FUNDO: somar ρ_TGL ao total reescalona
    radiação e matéria e deixa Λ intacta — o ponto no plano (N_eff, ω_c). -/
theorem hubble_form (β ρr ρm ρΛ : ℝ) :
    (ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
      = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ := by ring

/-- [KERNEL] a equação de estado efetiva (face algébrica): w_T ∈ [0, 1/3],
    com os dois limites exatos — radiação pura dá 1/3, matéria pura dá 0. -/
theorem w_bounds (β ρr ρm : ℝ) (hβ : 0 < β) (hr : 0 ≤ ρr) (hm : 0 ≤ ρm)
    (hpos : 0 < (4 / 3) * ρr + ρm) :
    (0 ≤ (β / 3) * ((4 / 3) * ρr) / (β * ((4 / 3) * ρr + ρm))
      ∧ (β / 3) * ((4 / 3) * ρr) / (β * ((4 / 3) * ρr + ρm)) ≤ 1 / 3)
    ∧ (ρm = 0 → 0 < ρr →
        (β / 3) * ((4 / 3) * ρr) / (β * ((4 / 3) * ρr + ρm)) = 1 / 3)
    ∧ (ρr = 0 →
        (β / 3) * ((4 / 3) * ρr) / (β * ((4 / 3) * ρr + ρm)) = 0) := by
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · apply div_nonneg
    · positivity
    · positivity
  · rw [div_le_iff₀ (by positivity)]
    nlinarith [mul_pos hβ hpos, mul_nonneg (le_of_lt hβ) hm]
  · intro h0 hrpos
    subst h0
    field_simp
    ring
  · intro h0
    subst h0
    simp

/-- [KERNEL] ★★★ O FECHAMENTO DE FUNDO, síntese: o vácuo não paga ∧ a
    identidade fecha exata ∧ o fundo é o reescalonamento (N_eff, ω_c).
    "A TGL no fundo não é modelo novo — é um ponto que todo pipeline de
    CMB já sabe percorrer." -/
theorem the_background_closure (β ρr ρm ρΛ : ℝ) :
    (ρΛ + (-ρΛ) = 0)
    ∧ (β * ((ρr + ρr / 3) + (ρm + 0) + (ρΛ + (-ρΛ)))
        = β * ((4 / 3) * ρr + ρm))
    ∧ ((ρr + ρm + ρΛ) + β * ((4 / 3) * ρr + ρm)
        = (1 + 4 * β / 3) * ρr + (1 + β) * ρm + ρΛ) :=
  ⟨lambda_drops_out ρΛ, closure_identity β ρr ρm ρΛ, hubble_form β ρr ρm ρΛ⟩

end

end TGLExt
