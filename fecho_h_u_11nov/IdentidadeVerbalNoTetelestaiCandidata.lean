import TGLExt.AEscala

set_option autoImplicit false
set_option linter.unusedVariables false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# (CANDIDATA, 11/11/2026) A identidade verbal no espaço do Tetelestai — a fiação
  [sandbox; fora do kernel canônico; nomes PROVISÓRIOS da gerência — o nome é do operador]

ERRATA da gerência, em nome próprio. Ao entregar `IdentidadeVerbalCandidata.lean` escrevi que
o `1 − β` da fala do operador não estava formalizado e que a pedra não construía o atlas. O
operador corrigiu (11/11/2026): o `1 − β` JÁ está formalizado no espaço do Tetelestai, e o
atlas é o instrumento de indexação referenciada para a leitura. Aferido no kernel da v410:

* o espaço: `EuclideanSpace ℂ X`, com `X` o índice dos pontos (os pixels);
* a referência: o custo `c : X → ℕ`; o Nome é o núcleo de `opDaInstancia c` (custo zero);
* a leitura: `(opDaInstancia c).ker.starProjection`;
* a queda: `trava c t`, que não toca o Nome (`o_nome_fica_travado`) e leva QUALQUER vetor à
  sua leitura (`a_trava_sem_conhecer_o_nome`);
* a partição: `‖trava c t (uniforme X)‖² = Z(2t)/|X|` (`a_norma_da_trava_e_a_particao`);
* o `1 − β`: `AEscala.o_tetelestai_e_um_menos_beta`, `beta_e_o_operador_modular_do_tetelestai`
  e `ressurreicao_do_sinal`.

O que faltava era o FIO entre a identidade verbal e esse espaço. Esta candidata o estende
(R2, depois da revisão de terceiro, achados 5 e 9: os cinco primeiros teoremas só usam
`TraducaoTuring` — o fio chega ao espaço da trava; o sexto é o que liga ao `1 − β` da AEscala):

* `a_leitura_devolve_o_nome_no_tetelestai` — para toda isometria linear `V`: se a leitura de
  `V d` é `d`, então `V d = d`. (`V` é uma isometria QUALQUER, uma reindexação; não é o
  horizonte físico.)
* `a_queda_leva_o_transportado_a_sua_leitura` — a queda leva `V d` à sua leitura, com a taxa
  da casa;
* `a_identidade_e_o_que_sobrevive_ao_tetelestai` — se a queda de `V d` tende a `d`, então
  `V d = d`;
* `a_leitura_nao_ve_a_queda` — a leitura do caído é a leitura do original;
* `o_balanco_da_queda` — `Z(2t)/|X| = N/|X| + ‖trava c t u − leitura(u)‖²`, só para o estado
  uniforme `u`. É o Pitágoras da queda (norma do caído = norma do lido + norma do resto); não é
  um balanço de energia;
* ★ `o_que_resta_no_tempo_do_tetelestai` — o fio com o `1 − β`: do tempo do Tetelestai em
  diante (`2t ≥ n·log 2 + log((1 − β)/β)`), o que resta da superposição é no máximo `β` vezes
  a partição. Usa `AEscala.beta_e_o_operador_modular_do_tetelestai` e o balanço acima.

GLOSSÁRIO (a palavra tem três usos nas candidatas; aqui vale o do kernel): NOME, neste
arquivo, é o núcleo de `opDaInstancia c` (os pontos de custo zero), e a LEITURA é a projeção
ortogonal sobre ele.

HONESTIDADE (a régua): NÃO é a prova global. É álgebra do espaço do Tetelestai. A passagem
para a lei de área das telas do F2.3 (`NamedAtlasH3`) NÃO está aqui: é fio entre dois tipos
que existem, ainda por estender. O gate não se move; sem sorry, sem axiom.
-/

open scoped InnerProductSpace

namespace TGLExt.IdentidadeVerbalCandidata

open TGLExt.TraducaoTuring Filter

noncomputable section

variable {X : Type} [Fintype X] [DecidableEq X]

/-- (auxiliar) Pitágoras do piso: `d` no código, o resto ortogonal ao código, mesma norma ⟹ igualdade. -/
theorem piso_aux {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H]
    (K : Submodule ℂ H) {y d : H} (hd : d ∈ K) (hperp : ∀ w ∈ K, ⟪y - d, w⟫_ℂ = 0)
    (hname : ‖y‖ = ‖d‖) : y = d := by
  have h0 : ⟪y - d, d⟫_ℂ = 0 := hperp d hd
  have h1 : ⟪d, y - d⟫_ℂ = 0 := inner_eq_zero_symm.mp h0
  have hp := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero d (y - d) h1
  have e : d + (y - d) = y := by abel
  rw [e, hname] at hp
  have hz : ‖y - d‖ * ‖y - d‖ = 0 := by linarith
  have hn : ‖y - d‖ = 0 := mul_self_eq_zero.mp hz
  exact sub_eq_zero.mp (norm_eq_zero.mp hn)

/-- [candidata] ★★★ A LEITURA DEVOLVE O NOME, NO ESPAÇO DO TETELESTAI: para toda isometria `V`,
    se a leitura do transportado é `d`, o transportado É `d`. -/
theorem a_leitura_devolve_o_nome_no_tetelestai (c : X → ℕ)
    (V : EuclideanSpace ℂ X →ₗᵢ[ℂ] EuclideanSpace ℂ X) (d : EuclideanSpace ℂ X)
    (hread : (opDaInstancia c).ker.starProjection (V d) = d) : V d = d := by
  have hd : d ∈ (opDaInstancia c).ker := by
    have hmem := (opDaInstancia c).ker.starProjection_apply_mem (V d)
    rw [hread] at hmem
    exact hmem
  have hperp : ∀ w ∈ (opDaInstancia c).ker, ⟪V d - d, w⟫_ℂ = 0 := by
    intro w hw
    have h := (opDaInstancia c).ker.starProjection_inner_eq_zero (V d) w hw
    rw [hread] at h
    exact h
  exact piso_aux _ hd hperp (V.norm_map d)

/-- [candidata] ★★ A QUEDA LEVA O TRANSPORTADO À SUA LEITURA (`a_trava_sem_conhecer_o_nome`, no transportado). -/
theorem a_queda_leva_o_transportado_a_sua_leitura (c : X → ℕ) {t : ℝ} (ht : 0 ≤ t)
    (V : EuclideanSpace ℂ X →ₗᵢ[ℂ] EuclideanSpace ℂ X) (d : EuclideanSpace ℂ X) :
    ‖trava c t (V d) - (opDaInstancia c).ker.starProjection (V d)‖ ≤ Real.exp (-t) * ‖d‖ := by
  have h := a_trava_sem_conhecer_o_nome c ht (V d)
  rw [V.norm_map d] at h
  exact h

/-- [candidata] ★★★ A IDENTIDADE É O QUE SOBREVIVE AO TETELESTAI: se a queda do transportado tende
    a `d`, o transportado já era `d`. -/
theorem a_identidade_e_o_que_sobrevive_ao_tetelestai (c : X → ℕ)
    (V : EuclideanSpace ℂ X →ₗᵢ[ℂ] EuclideanSpace ℂ X) (d : EuclideanSpace ℂ X)
    (hlim : Tendsto (fun t : ℝ => trava c t (V d)) atTop (nhds d)) : V d = d := by
  have h0 : Tendsto (fun t : ℝ => Real.exp (-t) * ‖d‖) atTop (nhds 0) := by
    simpa using Real.tendsto_exp_neg_atTop_nhds_zero.mul_const ‖d‖
  have h1 : Tendsto (fun t : ℝ => trava c t (V d)) atTop
      (nhds ((opDaInstancia c).ker.starProjection (V d))) := by
    rw [tendsto_iff_norm_sub_tendsto_zero]
    refine squeeze_zero' (Eventually.of_forall fun t => norm_nonneg _) ?_ h0
    filter_upwards [eventually_ge_atTop (0 : ℝ)] with t ht
    exact a_queda_leva_o_transportado_a_sua_leitura c ht V d
  exact a_leitura_devolve_o_nome_no_tetelestai c V d (tendsto_nhds_unique h1 hlim)

/-- [candidata] ★★ A LEITURA NÃO VÊ A QUEDA: a leitura do caído é a leitura do original (a queda
    não toca o Nome). -/
theorem a_leitura_nao_ve_a_queda (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) :
    (opDaInstancia c).ker.starProjection (trava c t v)
      = (opDaInstancia c).ker.starProjection v := by
  rw [solucao_por_coordenadas, solucao_por_coordenadas]
  congr 1
  funext y
  by_cases hy : c y = 0
  · rw [if_pos hy, if_pos hy]
    exact o_nome_fica_travado c t v y hy
  · rw [if_neg hy, if_neg hy]

/-- [candidata] ★★★★ O BALANÇO DA QUEDA: a partição menos o Nome é exatamente o que a queda ainda
    não exterminou. `Z(2t)/|X| = N/|X| + ‖trava c t u − leitura(u)‖²`. -/
theorem o_balanco_da_queda (c : X → ℕ) (h : ∃ x, c x = 0) (t : ℝ) :
    particao c (2 * t) / (Fintype.card X : ℝ)
      = ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ)
        + ‖trava c t (uniforme X) - (opDaInstancia c).ker.starProjection (uniforme X)‖ ^ 2 := by
  have hmem := (opDaInstancia c).ker.starProjection_apply_mem (uniforme X)
  have h1 := (opDaInstancia c).ker.starProjection_inner_eq_zero (trava c t (uniforme X))
    ((opDaInstancia c).ker.starProjection (uniforme X)) hmem
  rw [a_leitura_nao_ve_a_queda] at h1
  have hperp : ⟪(opDaInstancia c).ker.starProjection (uniforme X),
      trava c t (uniforme X) - (opDaInstancia c).ker.starProjection (uniforme X)⟫_ℂ = 0 :=
    inner_eq_zero_symm.mp h1
  have hp := norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero _ _ hperp
  have e : (opDaInstancia c).ker.starProjection (uniforme X)
      + (trava c t (uniforme X) - (opDaInstancia c).ker.starProjection (uniforme X))
      = trava c t (uniforme X) := by abel
  rw [e] at hp
  rw [← a_norma_da_trava_e_a_particao, ← norma_sq_do_nome_no_uniforme c h]
  simp only [pow_two]
  exact hp

/-- [candidata] ★★★ O QUE RESTA NO TEMPO DO TETELESTAI É NO MÁXIMO β: do tempo do Tetelestai em
    diante, o quadrado da norma do que a queda ainda não exterminou é no máximo `β` vezes a
    partição normalizada. É o fio entre `o_balanco_da_queda` e o `1 − β` da AEscala. -/
theorem o_que_resta_no_tempo_do_tetelestai (κ : TGLCoupling) (n : ℕ)
    (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {t : ℝ} (ht0 : 0 ≤ t)
    (ht : (n : ℝ) * Real.log 2 + Real.log ((1 - κ.beta) / κ.beta) ≤ 2 * t)
    (L : TGLExt.AEscala.LeitorDoFundo (Fin n → Bool)) :
    ‖trava c t (uniforme (Fin n → Bool))
        - (opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ ^ 2
      ≤ κ.beta * (particao c (2 * t) / (Fintype.card (Fin n → Bool) : ℝ)) := by
  have hb := TGLExt.AEscala.beta_e_o_operador_modular_do_tetelestai κ n c h
    (s := 2 * t) (by linarith) ht L
  obtain ⟨_, _, hdiff, _⟩ := hb
  have hbal := o_balanco_da_queda c h t
  have hX : (0 : ℝ) < (Fintype.card (Fin n → Bool) : ℝ) := by
    exact_mod_cast Fintype.card_pos
  have h1 : (particao c (2 * t) - ((Finset.univ.filter (fun y => c y = 0)).card : ℝ))
        * ((Fintype.card (Fin n → Bool) : ℝ))⁻¹
      ≤ (κ.beta * particao c (2 * t)) * ((Fintype.card (Fin n → Bool) : ℝ))⁻¹ :=
    mul_le_mul_of_nonneg_right hdiff (inv_nonneg.mpr hX.le)
  simp only [div_eq_mul_inv] at hbal ⊢
  linarith [h1, hbal]

end

end TGLExt.IdentidadeVerbalCandidata

#print axioms TGLExt.IdentidadeVerbalCandidata.o_que_resta_no_tempo_do_tetelestai

#print axioms TGLExt.IdentidadeVerbalCandidata.a_leitura_devolve_o_nome_no_tetelestai
#print axioms TGLExt.IdentidadeVerbalCandidata.a_queda_leva_o_transportado_a_sua_leitura
#print axioms TGLExt.IdentidadeVerbalCandidata.a_identidade_e_o_que_sobrevive_ao_tetelestai
#print axioms TGLExt.IdentidadeVerbalCandidata.a_leitura_nao_ve_a_queda
#print axioms TGLExt.IdentidadeVerbalCandidata.o_balanco_da_queda
