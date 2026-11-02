import Mathlib

set_option autoImplicit false
set_option linter.unusedVariables false

/-!
# NENHUMA PROJEÇÃO LINEAR LEVA O SETOR NEUTRO DE SPIN INTEIRO AO SETOR ESPINORIAL CARREGADO
  [TGLExt — v368; a obstrução escrita pela bancada, TIPADA]

Pergunta do operador (18/09/2026): «O elétron seria a manifestação do gráviton no Bulk?».
A bancada respondeu com uma obstrução: a volta de 2π age como `+1` no setor de spin inteiro e como
`−1` no setor de spin ½; um mapa linear que entrelace as duas ações tem de ser ZERO. O mesmo vale
para a carga: uma fase que age trivialmente na fonte e por um fator `c ≠ 1` no alvo mata o mapa.

Esta pedra põe esse argumento no kernel, em vez de prosa. O enunciado geral é um só:

* `zero_of_scalar_mismatch` — se a fonte é fixada pela ação e o alvo é multiplicado por `c ≠ 1`,
  qualquer mapa linear que entrelace as duas ações é nulo;
* `no_linear_map_integer_to_half_spin` — o caso `c = −1`: a volta de 2π (spin inteiro → spin ½);
* `no_linear_map_neutral_to_charged` — o caso da carga, com a fase `c ≠ 1`;
* `hypothesis_does_work` — a hipótese do entrelaçamento não é decorativa: sem ela existe mapa
  não nulo (exemplo explícito).

**ESCOPO, dito sem véu:** isto proíbe uma PROJEÇÃO LINEAR QUE ENTRELACE as ações — nada mais.
NÃO proíbe emergência fermiônica por construção coletiva, topológica ou não linear; NÃO diz o que
o elétron é; NÃO constrói setor eletrônico algum (espinor, carga, estatística e massa seguem
[OPEN]); e NÃO move gate. Nenhuma lacuna de prova e nenhum axioma novo.
-/

namespace TGLExt.SpinorObstruction

variable {V W : Type*} [AddCommGroup V] [AddCommGroup W] [Module ℝ V] [Module ℝ W]

/-- [KERNEL] ★★★ A OBSTRUÇÃO: se a ação fixa a fonte (`Ug = id`) e multiplica o alvo por `c ≠ 1`
    (`Ue = c • id`), então todo mapa linear que entrelaça as duas ações é nulo. -/
theorem zero_of_scalar_mismatch (proj : V →ₗ[ℝ] W) (Ug : V →ₗ[ℝ] V) (Ue : W →ₗ[ℝ] W) (c : ℝ)
    (hg : Ug = LinearMap.id) (he : Ue = c • LinearMap.id) (hc : c ≠ 1)
    (hint : Ue.comp proj = proj.comp Ug) : proj = 0 := by
  ext v
  have h : Ue (proj v) = proj (Ug v) := congrArg (fun f : V →ₗ[ℝ] W => f v) hint
  rw [hg, he] at h
  simp only [LinearMap.smul_apply, LinearMap.id_apply, LinearMap.id_coe, id_eq] at h
  have h0 : (c - 1) • proj v = 0 := by
    rw [sub_smul, one_smul, h, sub_self]
  rcases smul_eq_zero.mp h0 with hcz | hz
  · exact absurd (sub_eq_zero.mp hcz) hc
  · exact hz

/-- [KERNEL] ★★ O CASO DO SPIN: a volta de 2π vale `+1` no setor de spin inteiro e `−1` no setor
    espinorial; logo não há projeção linear entrelaçante não nula de um para o outro. -/
theorem no_linear_map_integer_to_half_spin (proj : V →ₗ[ℝ] W) (Ug : V →ₗ[ℝ] V) (Ue : W →ₗ[ℝ] W)
    (hg : Ug = LinearMap.id) (he : Ue = (-1 : ℝ) • LinearMap.id)
    (hint : Ue.comp proj = proj.comp Ug) : proj = 0 :=
  zero_of_scalar_mismatch proj Ug Ue (-1) hg he (by norm_num) hint

/-- [KERNEL] ★★ O CASO DA CARGA: se a fase da carga fixa a fonte (neutra) e multiplica o alvo por
    `c ≠ 1` (carregado), o mapa linear entrelaçante é nulo. -/
theorem no_linear_map_neutral_to_charged (proj : V →ₗ[ℝ] W) (Ug : V →ₗ[ℝ] V) (Ue : W →ₗ[ℝ] W) (c : ℝ)
    (hg : Ug = LinearMap.id) (he : Ue = c • LinearMap.id) (hc : c ≠ 1)
    (hint : Ue.comp proj = proj.comp Ug) : proj = 0 :=
  zero_of_scalar_mismatch proj Ug Ue c hg he hc hint

/-- [KERNEL] a hipótese do entrelaçamento faz trabalho: SEM ela existe mapa linear não nulo entre
    os mesmos setores (a identidade de ℝ), de modo que a obstrução não é vacuidade de tipo. -/
theorem hypothesis_does_work :
    ∃ (proj : ℝ →ₗ[ℝ] ℝ) (Ug : ℝ →ₗ[ℝ] ℝ) (Ue : ℝ →ₗ[ℝ] ℝ),
      Ug = LinearMap.id ∧ Ue = (-1 : ℝ) • LinearMap.id ∧ proj ≠ 0 := by
  refine ⟨LinearMap.id, LinearMap.id, (-1 : ℝ) • LinearMap.id, rfl, rfl, ?_⟩
  intro h
  have : (LinearMap.id : ℝ →ₗ[ℝ] ℝ) 1 = (0 : ℝ →ₗ[ℝ] ℝ) 1 := by rw [h]
  simpa using this

end TGLExt.SpinorObstruction
