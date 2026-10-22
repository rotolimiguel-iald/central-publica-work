import Mathlib
import TGLExt.GlobalLiftLadder
import TGLExt.TheSingularExpectation
import TGLExt.TheTraceIsNotErasable
import TGLExt.PageInformation
import TGLExt.FractalUnitarity
import TGLExt.TheWeightIsNotTheRank
import TGLExt.TheVerbalCoupling
import TGLExt.TheSameBetaReadsThreeFaces
import TGLExt.IALDJones
import TGLExt.TheVerbSelectsTheAction
import TGLExt.TheAxiomAndTheFalseWitness

set_option autoImplicit false
set_option maxHeartbeats 800000
set_option linter.unusedSectionVars false

/-!
# A UNIDADE É O POSTO — pedra CANDIDATA da F1.FREQUENCIA (trilha POSTO)
  [SANDBOX da gerência c1, 12/10/2026; nome PROVISÓRIO (o operador pode renomear);
   NÃO instalada no Nós — instalar é ato da v392]

## Os textos do operador (por sha16 dos bytes; lidos e conferidos por script no 3_KERNEL)

* V1 `OPERADOR_10out_posto_rank_texto_verbatim.txt` — sha16 `8d252f24e2806ff3` (10/10): «a transição entre uma
  hipótese difusa e um formalismo fechado é precisamente uma questão de posto (rank)»; «um estado puro … é descrito
  por um operador densidade de posto 1»; «Ao colapsar a superposição, a matriz deixa de ter um núcleo vazio
  (nullity) … e ganha posto definido».
* V2 `OPERADOR_12out_rank_e_tempo_santo_verbatim.txt` — sha16 `2c8b7b712aa9ad7f` (12/10; l.1–33 na trilha): a
  mesma passagem reafirmada, com a fórmula ρ = |ψ⟩⟨ψ|, Tr ρ = 1 e Tr ρ² = 1 (l.16).
* V3 `OPERADOR_10out_posto_rank_verbatim.txt` — sha16 `5b9afcc691a0e1e4` (10/10): «POSTO=RANK».
* V4 `OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt` — sha16 `b365591ceb346cdf` (11/10): a dinâmica
  do rank («Tudo = D_β(F(1))», «o vazamento … impede o anticomutador perfeito {Q̂, ρ*} = 0»).

O pré-registro congelado (`1_PREREGISTRO\PREREGISTRO.json`, sha256 `0c20d7c196a4c7ef…`) fixa as afirmações
P1–P4, B1–B9, os controles C1–C14 e as sondas. Esta pedra contém os termos da face K: as provas das partes com PASSA
esperado, as NEGAÇÕES das leituras que o pré-registro esperava falsas (B5.e(ii), B9.a, B9.a' — negativos honestos), os
controles C1–C14, as sondas de vacuidade e as re-exportações TRIVIAIS (B7.b, B7.c, B9.c).

## Estatutos (sem véu)

* `[REAL no sandbox]` — cada teorema desta pedra, compilado com o toolchain v4.31.0 e o `.lake` do Nós só-leitura;
  axiomas medidos por `#print axioms` em arquivo de auditoria separado.
* `[KNOWN]` — «estado puro ⟺ posto 1» (Nielsen & Chuang, Ex. 2.71) e posto–nulidade (Mathlib
  `LinearMap.finrank_range_add_finrank_ker`; Axler, LADR, Teo. 3.22): formalizados aqui como TERMO; o conteúdo segue
  sendo da literatura.
* `[INPUT da gerência]` — os mapeamentos frase → objeto (pré-registro, seção b).
* `[ONTO]` — «posição ⟷ rank», «Tudo», «Nada», «matéria», «verbo», «consciência», «existência»: NÃO são termos aqui.
* `[CONJECTURE ontológica]` (um.py l.6488) — «Tudo = D_β(F(1))»: aqui só o PONTO FINAL diag(cos²θ, sin²θ) e o seu posto.

## Os dois regimes (a regra matriz)

A matriz-S `Smat θ` é o ÂNGULO (unitária, só lê): `Smat_pow` mostra que iterá-la gira o ângulo e
`angular_leak_no_limit` / `angular_reflected_weight_no_limit` mostram que sin²(nθ), o peso refletido após n passagens,
NÃO converge quando sin θ ≠ 0 — o limite nunca é pedido ao ângulo (aqui se prova que ele não existe). O semigrupo `dephase` é a FACE (dissipativa, tem limite `diagExpect`). Ler o decaimento como direção
hiperbólica de SL(2,ℝ) é [ONTO] (IALDJones) e não é afirmado aqui.

## O que fica provado (resumo; o detalhe por parte está em RESULTADO_KERNEL.json)

* o posto, a nulidade e as suas faces: `rank_add_nullity` (re-exportação, KNOWN), `pure_iff_rank_one`,
  `pure_iff_idempotent`, `trace_eq_rank_of_projection`, `name_meets_rank_only_at_the_atom`;
* a unidade: `rhoStar_trace`, `rhoStar_rank`, `range_rhoStar` — Tr ρ* = posto ρ* = 1;
* a leitura de posto 1: `compression_by_rank_one`, `reading_returns_the_post`, `reading_of_the_attractor_state`;
* o anticomutador e o vazamento: `anticomm_zero_iff` ({Q_θ, ρ*} = 0 ⟺ sin θ = 0), `leak_eq`, `leak_at_thetaMiguel`
  (identidade de θ_M: sem poder discriminante);
* F preserva o Um (`ad_trace`, `ad_rank`, `fractal_one_is_rank_one`) e D NÃO preserva o posto
  (`rank_not_preserved_by_dephasing`, negativo honesto): o traço sobrevive, o posto não;
* a sonda honesta: `literal_transmission_does_not_force_dephasing` (negativo honesto) e
  `dephasing_acts_iff_transmits_and_leaks` (a leitura de inscrição).

## O que esta pedra NÃO afirma

β no Lean (θ é genérico ou `thetaMiguel c.beta` com `c : TGLCoupling`; o número de β é do runtime); ρ* = firstAtom,
PFmic, post Ω, bellProjector, P_F ou R; os dois «1» encadeados fora do átomo; que D preserve o posto ou devolva o
posto 1; que I/2 tenha posto 1; limite no ângulo; D como direção hiperbólica; colapso físico, seleção na natureza,
espaço latente; Tudo, Nada, matéria, verbo ou consciência como termos; que o vazamento discrimine β. Não cunha nome
reservado e não move o gate. Validade na face testada não é creditação. Sem sorry, sem axiom.
-/

namespace TGLExt.TheUnitIsTheRank

open Matrix Filter Topology
open scoped ComplexOrder

noncomputable section

/-! ## 0. Posto e nulidade em dimensão geral -/

section RankGeneral

variable {n : Type} [Fintype n] [DecidableEq n]

/-- A NULIDADE (pré-registro, objetos): `nulidade A := finrank (ker A.mulVecLin)`. -/
def nullity (A : Matrix n n ℂ) : ℕ := Module.finrank ℂ (LinearMap.ker A.mulVecLin)

/-- [KNOWN — Mathlib `LinearMap.finrank_range_add_finrank_ker`; Axler, LADR, Teo. 3.22] P2.lit, re-exportação para
    matrizes: posto + nulidade = n. O PASSA é do TERMO; o conteúdo é da literatura. -/
theorem rank_add_nullity (A : Matrix n n ℂ) : A.rank + nullity A = Fintype.card n := by
  have h := LinearMap.finrank_range_add_finrank_ker A.mulVecLin
  rw [Module.finrank_fintype_fun_eq_card] at h
  exact h

/-- Posto zero é a matriz nula (auxiliar; nome distinto do `rank_eq_zero_iff` de módulos da Mathlib). -/
theorem matrix_rank_eq_zero_iff (A : Matrix n n ℂ) : A.rank = 0 ↔ A = 0 := by
  constructor
  · intro h
    have h1 : LinearMap.range A.mulVecLin = ⊥ := Submodule.finrank_eq_zero.mp h
    have h2 : A.mulVecLin = 0 := LinearMap.range_eq_bot.mp h1
    have h3 : Matrix.toLin' A = 0 := by rw [Matrix.toLin'_apply']; exact h2
    exact (LinearEquiv.map_eq_zero_iff Matrix.toLin').mp h3
  · rintro rfl
    exact Matrix.rank_zero

/-- Nulidade positiva ⟺ determinante nulo (auxiliar). -/
theorem nullity_pos_iff_det_eq_zero (A : Matrix n n ℂ) : 0 < nullity A ↔ A.det = 0 := by
  rw [← Matrix.exists_mulVec_eq_zero_iff, nullity, Module.finrank_pos_iff_exists_ne_zero]
  constructor
  · rintro ⟨⟨v, hv⟩, hne⟩
    refine ⟨v, fun h0 => hne ?_, ?_⟩
    · subst h0
      rfl
    · have h := LinearMap.mem_ker.mp hv
      rwa [Matrix.mulVecLin_apply] at h
  · rintro ⟨v, hv0, hv⟩
    refine ⟨⟨v, LinearMap.mem_ker.mpr (by rwa [Matrix.mulVecLin_apply])⟩, fun h => hv0 ?_⟩
    simpa using congrArg Subtype.val h

/-- Posto cheio ⟺ determinante não nulo (auxiliar). -/
theorem rank_eq_card_iff_det_ne_zero (A : Matrix n n ℂ) :
    A.rank = Fintype.card n ↔ A.det ≠ 0 := by
  constructor
  · intro hr hdet
    have h1 := rank_add_nullity A
    have h2 := (nullity_pos_iff_det_eq_zero A).mpr hdet
    omega
  · intro hdet
    exact Matrix.rank_of_isUnit A ((Matrix.isUnit_iff_isUnit_det A).mpr (isUnit_iff_ne_zero.mpr hdet))

/-- Traço não nulo ⟹ matriz não nula (auxiliar). -/
theorem ne_zero_of_trace_ne_zero {A : Matrix n n ℂ} (h : A.trace ≠ 0) : A ≠ 0 := by
  rintro rfl
  simp at h

/-- Traço não nulo ⟹ posto ≥ 1 (auxiliar). -/
theorem rank_pos_of_trace_ne_zero {A : Matrix n n ℂ} (h : A.trace ≠ 0) : 1 ≤ A.rank := by
  rcases Nat.eq_zero_or_pos A.rank with h0 | h0
  · exact absurd ((matrix_rank_eq_zero_iff A).mp h0) (ne_zero_of_trace_ne_zero h)
  · exact h0

end RankGeneral

/-! ## 0'. Posto em M₂(ℂ) -/

section RankFinTwo

/-- Em M₂(ℂ): posto 2 ⟺ det ≠ 0. -/
theorem rank_two_iff (A : Matrix (Fin 2) (Fin 2) ℂ) : A.rank = 2 ↔ A.det ≠ 0 := by
  have h := rank_eq_card_iff_det_ne_zero A
  rwa [Fintype.card_fin] at h

/-- Em M₂(ℂ): posto 1 ⟺ A ≠ 0 ∧ det A = 0. -/
theorem rank_one_iff_fin_two (A : Matrix (Fin 2) (Fin 2) ℂ) : A.rank = 1 ↔ A ≠ 0 ∧ A.det = 0 := by
  have hle : A.rank ≤ 2 := by
    have h := Matrix.rank_le_card_width A
    rwa [Fintype.card_fin] at h
  constructor
  · intro h
    refine ⟨fun h0 => ?_, ?_⟩
    · rw [h0, Matrix.rank_zero] at h
      exact absurd h (by norm_num)
    · by_contra hd
      have h2 := (rank_two_iff A).mpr hd
      omega
  · rintro ⟨hne, hdet⟩
    have h0 : A.rank ≠ 0 := fun h => hne ((matrix_rank_eq_zero_iff A).mp h)
    have h2 : A.rank ≠ 2 := fun h => ((rank_two_iff A).mp h) hdet
    omega

/-- Em M₂(ℂ): nulidade = 2 − posto. -/
theorem nullity_fin_two (A : Matrix (Fin 2) (Fin 2) ℂ) : nullity A = 2 - A.rank := by
  have h := rank_add_nullity A
  rw [Fintype.card_fin] at h
  omega

end RankFinTwo

/-! ## 1. P1.a — estado puro ⟺ posto 1 (dimensão geral) -/

section Pure

variable {n : Type} [Fintype n] [DecidableEq n]

/-- Lema real: f ≥ 0, Σ f = 1 ⟹ (Σ f² = 1 ⟺ ∀ i, f i² = f i). -/
theorem sum_sq_eq_one_iff_idem (f : n → ℝ) (hf : ∀ i, 0 ≤ f i) (hs : ∑ i, f i = 1) :
    ∑ i, f i ^ 2 = 1 ↔ ∀ i, f i ^ 2 = f i := by
  have hle : ∀ i, f i ≤ 1 := fun i => by
    have h := Finset.single_le_sum (fun j _ => hf j) (Finset.mem_univ i)
    rwa [hs] at h
  have hterm : ∀ i, 0 ≤ f i - f i ^ 2 := fun i => by nlinarith [hf i, hle i]
  constructor
  · intro h
    have hsum : ∑ i, (f i - f i ^ 2) = 0 := by
      rw [Finset.sum_sub_distrib, hs, h, sub_self]
    have h0 := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => hterm i)).mp hsum
    intro i
    have h1 := h0 i (Finset.mem_univ i)
    linarith
  · intro h
    rw [← hs]
    exact Finset.sum_congr rfl (fun i _ => h i)

/-- Lema real: Σ f = 1 ⟹ ((∀ i, f i² = f i) ⟺ exatamente um f i é não nulo). -/
theorem idem_iff_card_support_one (f : n → ℝ) (hs : ∑ i, f i = 1) :
    (∀ i, f i ^ 2 = f i) ↔ (Finset.univ.filter (fun i => f i ≠ 0)).card = 1 := by
  constructor
  · intro h
    have h01 : ∀ i, f i = 0 ∨ f i = 1 := fun i => by
      have h2 : f i * (f i - 1) = 0 := by linear_combination h i
      rcases mul_eq_zero.mp h2 with h0 | h1
      · exact Or.inl h0
      · exact Or.inr (by linarith)
    have hc : ∑ i, f i = ((Finset.univ.filter (fun i => f i ≠ 0)).card : ℝ) := by
      rw [← Finset.sum_filter_ne_zero, Finset.card_eq_sum_ones, Nat.cast_sum]
      refine Finset.sum_congr rfl (fun i hi => ?_)
      have hne : f i ≠ 0 := (Finset.mem_filter.mp hi).2
      rcases h01 i with h0 | h1
      · exact absurd h0 hne
      · rw [h1]
        norm_num
    rw [hs] at hc
    exact_mod_cast hc.symm
  · intro hc i
    obtain ⟨k, hk⟩ := Finset.card_eq_one.mp hc
    have hzero : ∀ j, j ≠ k → f j = 0 := fun j hj => by
      by_contra hne
      have hmem : j ∈ Finset.univ.filter (fun i => f i ≠ 0) :=
        Finset.mem_filter.mpr ⟨Finset.mem_univ j, hne⟩
      rw [hk] at hmem
      exact hj (Finset.mem_singleton.mp hmem)
    have hfk : f k = 1 := by
      rw [← hs, Finset.sum_eq_single k (fun j _ hj => hzero j hj)
        (fun h => absurd (Finset.mem_univ k) h)]
    by_cases hik : i = k
    · rw [hik, hfk]
      norm_num
    · rw [hzero i hik]
      norm_num

/-- O teorema espectral da Mathlib, em forma de conjugação explícita. -/
theorem hermitian_spectral (ρ : Matrix n n ℂ) (hH : ρ.IsHermitian) :
    ∃ U : Matrix n n ℂ, star U * U = 1 ∧ U * star U = 1 ∧
      ρ = U * diagonal (fun i => ((hH.eigenvalues i : ℝ) : ℂ)) * star U := by
  refine ⟨(hH.eigenvectorUnitary : Matrix n n ℂ), Unitary.coe_star_mul_self _,
    Unitary.coe_mul_star_self _, ?_⟩
  have h := hH.spectral_theorem
  rw [Unitary.conjStarAlgAut_apply] at h
  exact h

/-- A conjugação unitária preserva o traço (auxiliar). -/
theorem conj_trace (U : Matrix n n ℂ) (hU : star U * U = 1) (X : Matrix n n ℂ) :
    (U * X * star U).trace = X.trace := by
  rw [Matrix.trace_mul_cycle, hU, one_mul]

/-- O quadrado de U·diag(d)·U* (auxiliar). -/
theorem conj_diag_sq (U : Matrix n n ℂ) (hU : star U * U = 1) (d : n → ℂ) :
    (U * diagonal d * star U) ^ 2 = U * diagonal (fun i => d i ^ 2) * star U := by
  rw [sq]
  calc U * diagonal d * star U * (U * diagonal d * star U)
      = U * diagonal d * (star U * U) * diagonal d * star U := by simp only [mul_assoc]
    _ = U * (diagonal d * diagonal d) * star U := by rw [hU, mul_one]; simp only [mul_assoc]
    _ = U * diagonal (fun i => d i ^ 2) * star U := by rw [diagonal_mul_diagonal]; simp only [sq]

/-- A conjugação unitária é injetiva nas diagonais (auxiliar). -/
theorem conj_diag_eq_iff (U : Matrix n n ℂ) (hU : star U * U = 1) (d e : n → ℂ) :
    U * diagonal d * star U = U * diagonal e * star U ↔ d = e := by
  constructor
  · intro h
    have key : ∀ f : n → ℂ, star U * (U * diagonal f * star U) * U = diagonal f := fun f => by
      calc star U * (U * diagonal f * star U) * U = (star U * U) * diagonal f * (star U * U) := by
            simp only [mul_assoc]
        _ = diagonal f := by rw [hU, one_mul, mul_one]
    have h2 : star U * (U * diagonal d * star U) * U = star U * (U * diagonal e * star U) * U := by rw [h]
    rw [key, key] at h2
    exact diagonal_injective h2
  · rintro rfl
    rfl

/-- Tr ρ = Σ λᵢ (auxiliar). -/
theorem trace_eq_sum_eig (ρ : Matrix n n ℂ) (hH : ρ.IsHermitian) :
    ρ.trace = ((∑ i, hH.eigenvalues i : ℝ) : ℂ) := by
  rw [hH.trace_eq_sum_eigenvalues, Complex.ofReal_sum]
  rfl

/-- Tr ρ² = Σ λᵢ² e ρ² = ρ ⟺ λᵢ² = λᵢ (auxiliar). -/
theorem pure_spectral_facts (ρ : Matrix n n ℂ) (hH : ρ.IsHermitian) :
    (ρ ^ 2).trace = ((∑ i, hH.eigenvalues i ^ 2 : ℝ) : ℂ)
    ∧ (ρ ^ 2 = ρ ↔ ∀ i, hH.eigenvalues i ^ 2 = hH.eigenvalues i) := by
  obtain ⟨U, hU1, -, hρ⟩ := hermitian_spectral ρ hH
  have hsq : ρ ^ 2 = U * diagonal (fun i => ((hH.eigenvalues i : ℝ) : ℂ) ^ 2) * star U := by
    conv_lhs => rw [hρ]
    exact conj_diag_sq U hU1 _
  refine ⟨?_, ?_⟩
  · rw [hsq, conj_trace U hU1, trace_diagonal, Complex.ofReal_sum]
    push_cast
    rfl
  · constructor
    · intro h
      have h2 : U * diagonal (fun i => ((hH.eigenvalues i : ℝ) : ℂ) ^ 2) * star U
          = U * diagonal (fun i => ((hH.eigenvalues i : ℝ) : ℂ)) * star U := by
        rw [← hsq, ← hρ]
        exact h
      have h3 := (conj_diag_eq_iff U hU1 _ _).mp h2
      intro i
      have h4 := congrFun h3 i
      exact_mod_cast h4
    · intro h
      rw [hsq]
      conv_rhs => rw [hρ]
      exact (conj_diag_eq_iff U hU1 _ _).mpr (funext fun i => by exact_mod_cast h i)

/-- posto ρ = #{i : λᵢ ≠ 0} (auxiliar). -/
theorem rank_eq_card_eig (ρ : Matrix n n ℂ) (hH : ρ.IsHermitian) :
    ρ.rank = (Finset.univ.filter (fun i => hH.eigenvalues i ≠ 0)).card := by
  rw [hH.rank_eq_card_non_zero_eigs]
  convert Fintype.card_subtype (fun i => hH.eigenvalues i ≠ 0)

/-- O núcleo de P1.a: sob ρ ⪰ 0 e Tr ρ = 1, as três condições equivalem a «todo autovalor é 0 ou 1». -/
theorem pure_core {ρ : Matrix n n ℂ} (hρ : ρ.PosSemidef) (htr : ρ.trace = 1) :
    ((ρ ^ 2).trace = 1 ↔ ∀ i, hρ.isHermitian.eigenvalues i ^ 2 = hρ.isHermitian.eigenvalues i)
    ∧ (ρ.rank = 1 ↔ ∀ i, hρ.isHermitian.eigenvalues i ^ 2 = hρ.isHermitian.eigenvalues i)
    ∧ (ρ ^ 2 = ρ ↔ ∀ i, hρ.isHermitian.eigenvalues i ^ 2 = hρ.isHermitian.eigenvalues i) := by
  have hnn : ∀ i, 0 ≤ hρ.isHermitian.eigenvalues i := hρ.eigenvalues_nonneg
  have hs : ∑ i, hρ.isHermitian.eigenvalues i = 1 := by
    have h := trace_eq_sum_eig ρ hρ.isHermitian
    rw [htr] at h
    exact_mod_cast h.symm
  obtain ⟨htr2, hidem⟩ := pure_spectral_facts ρ hρ.isHermitian
  refine ⟨?_, ?_, hidem⟩
  · rw [htr2, ← sum_sq_eq_one_iff_idem _ hnn hs]
    exact Complex.ofReal_eq_one
  · rw [rank_eq_card_eig ρ hρ.isHermitian]
    exact (idem_iff_card_support_one _ hs).symm

/-- [P1.a; KNOWN — Nielsen & Chuang, Ex. 2.71; TERMO novo] ρ ⪰ 0, Tr ρ = 1: Tr ρ² = 1 ⟺ posto ρ = 1. -/
theorem pure_iff_rank_one {ρ : Matrix n n ℂ} (hρ : ρ.PosSemidef) (htr : ρ.trace = 1) :
    (ρ ^ 2).trace = 1 ↔ ρ.rank = 1 := by
  obtain ⟨h1, h2, -⟩ := pure_core hρ htr
  rw [h1, h2]

/-- [P1.a; KNOWN — Nielsen & Chuang, Ex. 2.71; TERMO novo] ρ ⪰ 0, Tr ρ = 1: Tr ρ² = 1 ⟺ ρ² = ρ. -/
theorem pure_iff_idempotent {ρ : Matrix n n ℂ} (hρ : ρ.PosSemidef) (htr : ρ.trace = 1) :
    (ρ ^ 2).trace = 1 ↔ ρ ^ 2 = ρ := by
  obtain ⟨h1, -, h3⟩ := pure_core hρ htr
  rw [h1, h3]

end Pure

/-! ## 2. P1.b — em M₂(ℂ) a positividade não é necessária -/

/-- [P1.b] Tr M² = (Tr M)² − 2·det M em M₂(ℂ). -/
theorem trace_sq_fin_two (M : Matrix (Fin 2) (Fin 2) ℂ) :
    (M ^ 2).trace = M.trace ^ 2 - 2 * M.det := by
  rw [sq, sq, Matrix.trace_fin_two, Matrix.trace_fin_two, Matrix.det_fin_two]
  simp only [Matrix.mul_apply, Fin.sum_univ_two]
  ring

/-- [P1.b] Em M₂(ℂ), com Tr M = 1 e SEM positividade: Tr M² = 1 ⟺ posto M = 1. -/
theorem pure_iff_rank_one_fin_two (M : Matrix (Fin 2) (Fin 2) ℂ) (htr : M.trace = 1) :
    (M ^ 2).trace = 1 ↔ M.rank = 1 := by
  rw [trace_sq_fin_two, htr, rank_one_iff_fin_two]
  have hne : M ≠ 0 := ne_zero_of_trace_ne_zero (by rw [htr]; exact one_ne_zero)
  constructor
  · intro h
    exact ⟨hne, by linear_combination (-1 / 2 : ℂ) * h⟩
  · rintro ⟨-, hd⟩
    rw [hd]
    ring

/-- [P1.b, forma literal] Tr M = Tr M² = 1 ⟹ det M = 0 ∧ posto M = 1 (sem positividade). -/
theorem trace_and_purity_one_fin_two (M : Matrix (Fin 2) (Fin 2) ℂ) (h1 : M.trace = 1)
    (h2 : (M ^ 2).trace = 1) : M.det = 0 ∧ M.rank = 1 := by
  have hr := (pure_iff_rank_one_fin_two M h1).mp h2
  exact ⟨((rank_one_iff_fin_two M).mp hr).2, hr⟩

/-! ## 3. P1.d — |ψ⟩⟨ψ| tem posto 1 -/

section RankOne

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [P1.d] ψ ≠ 0 ⟹ posto |ψ⟩⟨ψ| = 1. -/
theorem rankOne_density (ψ : n → ℂ) (hψ : ψ ≠ 0) : (vecMulVec ψ (star ψ)).rank = 1 := by
  have hle := Matrix.rank_vecMulVec_le ψ (star ψ)
  obtain ⟨i, hi⟩ : ∃ i, ψ i ≠ 0 := by
    by_contra hc
    exact hψ (funext fun j => by by_contra hj; exact hc ⟨j, hj⟩)
  have hne : vecMulVec ψ (star ψ) ≠ 0 := by
    intro h
    have h2 := congrFun (congrFun h i) i
    rw [vecMulVec_apply, Pi.star_apply, Complex.star_def, Complex.mul_conj, Matrix.zero_apply] at h2
    have h3 : Complex.normSq (ψ i) = 0 := by exact_mod_cast h2
    exact hi (Complex.normSq_eq_zero.mp h3)
  have h0 : (vecMulVec ψ (star ψ)).rank ≠ 0 := fun h => hne ((matrix_rank_eq_zero_iff _).mp h)
  omega

/-- [P1.d] ⟨ψ, ψ⟩ = 1 ⟹ Tr |ψ⟩⟨ψ| = 1, |ψ⟩⟨ψ|² = |ψ⟩⟨ψ|, Tr (|ψ⟩⟨ψ|)² = 1 (e posto 1). A norma de Hilbert
    é codificada por ⟨ψ, ψ⟩ = star ψ ⬝ᵥ ψ = 1 (em `n → ℂ` a norma da Mathlib é a do sup). -/
theorem rankOne_density_normalized (ψ : n → ℂ) (hψ : star ψ ⬝ᵥ ψ = 1) :
    (vecMulVec ψ (star ψ)).trace = 1 ∧ vecMulVec ψ (star ψ) ^ 2 = vecMulVec ψ (star ψ)
    ∧ (vecMulVec ψ (star ψ) ^ 2).trace = 1 ∧ (vecMulVec ψ (star ψ)).rank = 1 := by
  have htr : (vecMulVec ψ (star ψ)).trace = 1 := by
    rw [trace_vecMulVec, dotProduct_comm, hψ]
  have hidem : vecMulVec ψ (star ψ) ^ 2 = vecMulVec ψ (star ψ) := by
    rw [sq, vecMulVec_mul_vecMulVec, hψ, one_smul]
  have hne : ψ ≠ 0 := by
    rintro rfl
    simp at hψ
  exact ⟨htr, hidem, by rw [hidem, htr], rankOne_density ψ hne⟩

end RankOne

/-! ## 4. Os objetos da trilha (pré-registro, seção «objetos») -/

/-- ρ* = |0⟩⟨0| = diag(1, 0): o termo de `rhoOut` (`Matrix.single 0 0 1`); um.py l.6512. -/
def rhoStar : Matrix (Fin 2) (Fin 2) ℂ := Matrix.single 0 0 1

/-- Q₀ = 1 − ρ* (um.py l.6514). -/
def Q0 : Matrix (Fin 2) (Fin 2) ℂ := 1 - rhoStar

/-- A matriz R do um.py (l.6518): `[[c, −s], [s, c]]`. -/
def Rot (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![(Real.cos θ : ℂ), -(Real.sin θ : ℂ); (Real.sin θ : ℂ), (Real.cos θ : ℂ)]

/-- Q_θ = S(θ)ᴴ·Q₀·S(θ) (pré-registro; = R·Q₀·Rᵀ do um.py, ver `Qtheta_eq_rot`). -/
def Qtheta (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℂ := (Smat θ)ᴴ * Q0 * Smat θ

/-- O anticomutador {A, B} = AB + BA. -/
def anticomm (A B : Matrix (Fin 2) (Fin 2) ℂ) : Matrix (Fin 2) (Fin 2) ℂ := A * B + B * A

/-- I/2. -/
def halfId : Matrix (Fin 2) (Fin 2) ℂ := (2⁻¹ : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)

/-- «D atua» (pré-registro): ∃ t, D_t F_θ(1) ≠ F_θ(1). -/
def dephasingActs (g : Fin 2 → Fin 2 → ℝ) (θ : ℝ) : Prop :=
  ∃ t : ℝ, dephase g t (rhoOut θ) ≠ rhoOut θ

theorem rhoStar_eq : rhoStar = !![1, 0; 0, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rhoStar]

theorem Q0_eq : Q0 = !![0, 0; 0, 1] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Q0, rhoStar]

theorem rhoOut_eq_ad (θ : ℝ) : rhoOut θ = Smat θ * rhoStar * (Smat θ)ᴴ := rfl

/-- ρ* = |e₁⟩⟨e₁| com e₁ = ![1, 0] (o `e1` da matriz-S; o «e0» do pré-registro). -/
theorem rhoStar_eq_vecMulVec : rhoStar = vecMulVec e1 (star e1) := by
  rw [rhoStar_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [vecMulVec_apply, e1]

/-! ## 5. B1 — a unidade: Tr ρ* = posto ρ* = 1 (POSTO = RANK) -/

/-- [B1.a] Tr ρ* = 1 (= ω(I) no runtime, um.py l.6513). -/
theorem rhoStar_trace : rhoStar.trace = 1 := by
  rw [rhoStar_eq, Matrix.trace_fin_two]
  simp

/-- [B1.a] ρ*² = ρ*. -/
theorem rhoStar_idem : rhoStar * rhoStar = rhoStar := by
  rw [rhoStar_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- [B1.a] ρ*ᴴ = ρ*. -/
theorem rhoStar_herm : rhoStarᴴ = rhoStar := by
  rw [rhoStar_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.conjTranspose_apply]

theorem rhoStar_det : rhoStar.det = 0 := by
  rw [rhoStar_eq, Matrix.det_fin_two]
  simp

theorem rhoStar_ne_zero : rhoStar ≠ 0 :=
  ne_zero_of_trace_ne_zero (by rw [rhoStar_trace]; exact one_ne_zero)

/-- [B1.a] posto ρ* = 1. -/
theorem rhoStar_rank : rhoStar.rank = 1 :=
  (rank_one_iff_fin_two _).mpr ⟨rhoStar_ne_zero, rhoStar_det⟩

/-- [B1.a, conjunção] Tr ρ* = 1, posto ρ* = 1, ρ*² = ρ* = ρ*ᴴ. -/
theorem rhoStar_unit : rhoStar.trace = 1 ∧ rhoStar.rank = 1 ∧ rhoStar * rhoStar = rhoStar
    ∧ rhoStarᴴ = rhoStar :=
  ⟨rhoStar_trace, rhoStar_rank, rhoStar_idem, rhoStar_herm⟩

/-- [B1.c] imagem ρ* = span{e₁}; posto ρ* = finrank(span{e₁}) = 1 (o mesmo espaço `Fin 2 → ℂ`). -/
theorem range_rhoStar : LinearMap.range rhoStar.mulVecLin = ℂ ∙ e1
    ∧ rhoStar.rank = Module.finrank ℂ (ℂ ∙ e1) ∧ Module.finrank ℂ (ℂ ∙ e1) = 1 := by
  have hrange : LinearMap.range rhoStar.mulVecLin = ℂ ∙ e1 := by
    apply le_antisymm
    · rintro _ ⟨v, rfl⟩
      rw [Submodule.mem_span_singleton]
      refine ⟨v 0, ?_⟩
      ext i
      fin_cases i <;> simp [rhoStar_eq, Matrix.mulVec, dotProduct, e1,
        Fin.sum_univ_two]
    · rw [Submodule.span_le, Set.singleton_subset_iff, SetLike.mem_coe]
      refine LinearMap.mem_range.mpr ⟨e1, ?_⟩
      ext i
      fin_cases i <;> simp [rhoStar_eq, Matrix.mulVec, dotProduct, e1,
        Fin.sum_univ_two]
  have he1 : e1 ≠ 0 := by
    intro h
    have h0 := congrFun h 0
    simp [e1] at h0
  refine ⟨hrange, ?_, finrank_span_singleton he1⟩
  show Module.finrank ℂ (LinearMap.range rhoStar.mulVecLin) = _
  rw [hrange]

section Projection

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [B1.b] P² = P ⟹ Tr P = posto P (sobre ℂ, sem hipótese hermitiana). Rota: `IsProj` sobre a imagem
    (Mathlib `LinearMap.IsIdempotentElem.isProj_range`, `LinearMap.IsProj.trace`). -/
theorem trace_eq_rank_of_projection (P : Matrix n n ℂ) (hP : P * P = P) :
    P.trace = (P.rank : ℂ) := by
  have hidem : IsIdempotentElem P.mulVecLin := by
    show P.mulVecLin * P.mulVecLin = P.mulVecLin
    rw [Module.End.mul_eq_comp, ← Matrix.mulVecLin_mul, hP]
  have hproj := LinearMap.IsIdempotentElem.isProj_range P.mulVecLin hidem
  have h1 : P.trace = LinearMap.trace ℂ (n → ℂ) P.mulVecLin := by
    rw [← Matrix.toLin'_apply', Matrix.trace_toLin'_eq]
  rw [h1, hproj.trace]
  rfl

/-! ## 6. P4 — o nome e o índice na densidade -/

/-- [P4] ρ = P/d com d = posto P ≥ 1: Tr ρ = 1 (o NOME, cego ao posto). -/
theorem normalized_projection_name (P : Matrix n n ℂ) (hP : P * P = P) (hd : 1 ≤ P.rank) :
    (((P.rank : ℂ))⁻¹ • P).trace = 1 := by
  rw [Matrix.trace_smul, trace_eq_rank_of_projection P hP, smul_eq_mul]
  have h : (P.rank : ℂ) ≠ 0 := by exact_mod_cast (by omega : P.rank ≠ 0)
  field_simp

/-- [P4] Tr ρ² = 1/d (o ÍNDICE, que vê o posto). -/
theorem normalized_projection_index (P : Matrix n n ℂ) (hP : P * P = P) (hd : 1 ≤ P.rank) :
    ((((P.rank : ℂ))⁻¹ • P) ^ 2).trace = ((P.rank : ℂ))⁻¹ := by
  rw [sq, smul_mul_smul_comm, hP, Matrix.trace_smul, trace_eq_rank_of_projection P hP, smul_eq_mul]
  have h : (P.rank : ℂ) ≠ 0 := by exact_mod_cast (by omega : P.rank ≠ 0)
  field_simp

/-- [P4] Tr ρ² = Tr ρ ⟺ d = 1: o nome encontra o posto SÓ no átomo (face de densidade de
    `the_two_indices_agree_only_at_the_atom`; distinção, não ponte). -/
theorem name_meets_rank_only_at_the_atom (P : Matrix n n ℂ) (hP : P * P = P) (hd : 1 ≤ P.rank) :
    ((((P.rank : ℂ))⁻¹ • P) ^ 2).trace = (((P.rank : ℂ))⁻¹ • P).trace ↔ P.rank = 1 := by
  rw [normalized_projection_index P hP hd, normalized_projection_name P hP hd]
  constructor
  · intro h
    have h2 : (P.rank : ℂ) = 1 := by
      have h3 := congrArg (fun z : ℂ => z⁻¹) h
      simpa using h3
    exact_mod_cast h2
  · intro h
    rw [h]
    simp

/-- [P4, forma literal do pré-registro: P² = P = Pᴴ] A hipótese `Pᴴ = P` é SEM PESO (não usada): a identidade vale para
    todo idempotente sobre ℂ — por isso o nome `_hH`. -/
theorem normalized_projection_literal (P : Matrix n n ℂ) (hP : P * P = P) (_hH : Pᴴ = P)
    (hd : 1 ≤ P.rank) :
    P.trace = (P.rank : ℂ) ∧ (((P.rank : ℂ))⁻¹ • P).trace = 1
    ∧ ((((P.rank : ℂ))⁻¹ • P) ^ 2).trace = ((P.rank : ℂ))⁻¹
    ∧ (((((P.rank : ℂ))⁻¹ • P) ^ 2).trace = (((P.rank : ℂ))⁻¹ • P).trace ↔ P.rank = 1) :=
  ⟨trace_eq_rank_of_projection P hP, normalized_projection_name P hP hd,
    normalized_projection_index P hP hd, name_meets_rank_only_at_the_atom P hP hd⟩

end Projection

/-! ## 7. P2 — posto e nulidade -/

/-- [P2.a] (posto, nulidade) de ρ* = (1, 1). -/
theorem rhoStar_rank_nullity : rhoStar.rank = 1 ∧ nullity rhoStar = 1 := by
  refine ⟨rhoStar_rank, ?_⟩
  rw [nullity_fin_two, rhoStar_rank]

theorem halfId_det : halfId.det = 4⁻¹ := by
  rw [halfId, Matrix.det_fin_two]
  simp
  norm_num

theorem halfId_rank : halfId.rank = 2 :=
  (rank_two_iff _).mpr (by rw [halfId_det]; norm_num)

/-- [P2.a] (posto, nulidade) de I/2 = (2, 0). -/
theorem half_identity_rank_nullity : halfId.rank = 2 ∧ nullity halfId = 0 := by
  refine ⟨halfId_rank, ?_⟩
  rw [nullity_fin_two, halfId_rank]

/-- [P2.a] (posto, nulidade) de 0 = (0, 2). -/
theorem zero_rank_nullity :
    (0 : Matrix (Fin 2) (Fin 2) ℂ).rank = 0 ∧ nullity (0 : Matrix (Fin 2) (Fin 2) ℂ) = 2 := by
  refine ⟨Matrix.rank_zero, ?_⟩
  rw [nullity_fin_two, Matrix.rank_zero]

section NullityGeneral

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [P2.b] Tr ρ = 1 ⟹ posto ρ ≥ 1. -/
theorem trace_one_rank_pos {ρ : Matrix n n ℂ} (htr : ρ.trace = 1) : 1 ≤ ρ.rank :=
  rank_pos_of_trace_ne_zero (by rw [htr]; exact one_ne_zero)

/-- [P2.b, forma sem subtração e sem hipótese] posto ρ = 1 ⟺ nulidade ρ + 1 = n. -/
theorem rank_one_iff_nullity_succ (ρ : Matrix n n ℂ) :
    ρ.rank = 1 ↔ nullity ρ + 1 = Fintype.card n := by
  have h := rank_add_nullity ρ
  constructor <;> intro h2 <;> omega

/-- [P2.b, forma literal] Tr ρ = 1 ⟹ (posto ρ = 1 ⟺ nulidade ρ = n − 1). -/
theorem rank_one_iff_nullity {ρ : Matrix n n ℂ} (htr : ρ.trace = 1) :
    ρ.rank = 1 ↔ nullity ρ = Fintype.card n - 1 := by
  have h1 := rank_add_nullity ρ
  have h2 := trace_one_rank_pos htr
  constructor <;> intro h3 <;> omega

end NullityGeneral

/-! ## 8. P3 — a leitura de posto 1 -/

section Reading

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [P3.a] P = |a⟩⟨a|: P·X·P = ⟨a, Xa⟩·P e Tr(P·X) = ⟨a, Xa⟩ — para TODO vetor a (a normalização não é usada). -/
theorem compression_by_rank_one (a : n → ℂ) (X : Matrix n n ℂ) :
    vecMulVec a (star a) * X * vecMulVec a (star a) = (star a ⬝ᵥ (X *ᵥ a)) • vecMulVec a (star a)
    ∧ (vecMulVec a (star a) * X).trace = star a ⬝ᵥ (X *ᵥ a) := by
  constructor
  · rw [vecMulVec_mul, vecMulVec_mul_vecMulVec, vecMulVec_smul, dotProduct_mulVec]
  · rw [vecMulVec_mul, trace_vecMulVec, dotProduct_comm a (star a ᵥ* X), dotProduct_mulVec]

/-- [P3.a] ⟨a, Xa⟩ ≠ 0 ⟹ P·X·P / ⟨a, Xa⟩ = P: a leitura devolve o posto. -/
theorem reading_returns_the_post (a : n → ℂ) (X : Matrix n n ℂ) (h : star a ⬝ᵥ (X *ᵥ a) ≠ 0) :
    (star a ⬝ᵥ (X *ᵥ a))⁻¹ • (vecMulVec a (star a) * X * vecMulVec a (star a))
      = vecMulVec a (star a) := by
  rw [(compression_by_rank_one a X).1, smul_smul, inv_mul_cancel₀ h, one_smul]

/-- [P3.a, forma literal do pré-registro: ⟨a, a⟩ = 1] A normalização `⟨a, a⟩ = 1` é SEM PESO para estas conclusões
    (por isso `_ha`); ela só é necessária para P ser projeção (P² = P), o que não faz parte do enunciado P3.a. -/
theorem compression_by_rank_one_literal (a : n → ℂ) (_ha : star a ⬝ᵥ a = 1) (X : Matrix n n ℂ) :
    (vecMulVec a (star a) * X * vecMulVec a (star a) = (star a ⬝ᵥ (X *ᵥ a)) • vecMulVec a (star a)
      ∧ (vecMulVec a (star a) * X).trace = star a ⬝ᵥ (X *ᵥ a))
    ∧ (star a ⬝ᵥ (X *ᵥ a) ≠ 0 →
      (star a ⬝ᵥ (X *ᵥ a))⁻¹ • (vecMulVec a (star a) * X * vecMulVec a (star a))
        = vecMulVec a (star a)) :=
  ⟨compression_by_rank_one a X, reading_returns_the_post a X⟩

end Reading

/-- [P3.b] A leitura ρ* aplicada ao estado atrator I/2 devolve ρ*: ρ*(I/2)ρ*/Tr(ρ*·I/2) = ρ*, com Tr = 1/2.
    (I/2 é o estado fixo do canal da F1.ATRATOR — citado; o posto 1 volta pela LEITURA, não pelo atrator.) -/
theorem reading_of_the_attractor_state :
    (rhoStar * halfId).trace = 2⁻¹
    ∧ ((rhoStar * halfId).trace)⁻¹ • (rhoStar * halfId * rhoStar) = rhoStar := by
  have h1 : rhoStar * halfId = (2⁻¹ : ℂ) • rhoStar := by
    rw [halfId, mul_smul_comm, mul_one]
  have h2 : (rhoStar * halfId).trace = 2⁻¹ := by
    rw [h1, Matrix.trace_smul, rhoStar_trace, smul_eq_mul, mul_one]
  refine ⟨h2, ?_⟩
  rw [h2, h1, smul_mul_assoc, rhoStar_idem, smul_smul]
  norm_num

/-- [P3.b] ρ = diag(1 − b, b): Tr(ρ*·ρ) = 1 − b e Tr(Q₀·ρ) = b. -/
theorem reading_weights_are_truth_and_cost (b : ℂ) :
    (rhoStar * diagonal ![1 - b, b]).trace = 1 - b ∧ (Q0 * diagonal ![1 - b, b]).trace = b := by
  constructor
  · rw [rhoStar_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]
  · rw [Q0_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]

/-! ## 9. B2, B3 — o anticomutador e o vazamento -/

theorem Rot_eq_conjTranspose (θ : ℝ) : Rot θ = (Smat θ)ᴴ := by
  rw [Smat_conjTranspose, Smat_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Rot, Real.cos_neg, Real.sin_neg]

theorem Rot_transpose (θ : ℝ) : (Rot θ)ᵀ = Smat θ := by
  rw [Smat_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Rot]

/-- A receita do um.py (l.6518): Q_θ = R·Q₀·Rᵀ é o mesmo objeto que S(θ)ᴴ·Q₀·S(θ). -/
theorem Qtheta_eq_rot (θ : ℝ) : Qtheta θ = Rot θ * Q0 * (Rot θ)ᵀ := by
  rw [Qtheta, Rot_transpose, Rot_eq_conjTranspose]

/-- [B2.a] Q_θ = [[s², −sc], [−cs, c²]]. -/
theorem Qtheta_eq (θ : ℝ) :
    Qtheta θ = !![(Real.sin θ : ℂ) ^ 2, -((Real.sin θ : ℂ) * (Real.cos θ : ℂ));
      -((Real.cos θ : ℂ) * (Real.sin θ : ℂ)), (Real.cos θ : ℂ) ^ 2] := by
  rw [Qtheta, Smat_conjTranspose, Smat_eq θ, Smat_eq (-θ), Q0_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Real.cos_neg, Real.sin_neg] <;> ring

theorem Qtheta_zero : Qtheta 0 = Q0 := by
  simp [Qtheta]

/-- [B2.a] {Q_θ, ρ*} = [[2s², −sc], [−cs, 0]]. -/
theorem anticomm_eq (θ : ℝ) :
    anticomm (Qtheta θ) rhoStar = !![2 * (Real.sin θ : ℂ) ^ 2, -((Real.sin θ : ℂ) * (Real.cos θ : ℂ));
      -((Real.cos θ : ℂ) * (Real.sin θ : ℂ)), 0] := by
  rw [anticomm, Qtheta_eq, rhoStar_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp
  all_goals ring

/-- [B2.a] {Q_θ, ρ*} = 0 ⟺ sin θ = 0 (o anticomutador perfeito é exatamente o ramo θ = 0 mod π). -/
theorem anticomm_zero_iff (θ : ℝ) : anticomm (Qtheta θ) rhoStar = 0 ↔ Real.sin θ = 0 := by
  rw [anticomm_eq]
  constructor
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    simp only [Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.empty_val',
      Matrix.cons_val_fin_one, Matrix.zero_apply] at h00
    have h2 : (Real.sin θ : ℂ) ^ 2 = 0 := by
      rcases mul_eq_zero.mp h00 with h3 | h3
      · norm_num at h3
      · exact h3
    exact Complex.ofReal_eq_zero.mp ((pow_eq_zero_iff two_ne_zero).mp h2)
  · intro h
    ext i j
    fin_cases i <;> fin_cases j <;> simp [h]

/-- [B2.a] Tr {Q_θ, ρ*} = 2 sin²θ. -/
theorem anticomm_trace (θ : ℝ) : (anticomm (Qtheta θ) rhoStar).trace = 2 * (Real.sin θ : ℂ) ^ 2 := by
  rw [anticomm_eq, Matrix.trace_fin_two]
  simp

/-- [B2.a] Σ|{Q_θ, ρ*}ᵢⱼ|² = 2 sin²θ (1 + sin²θ) (a `purityR` de `PageInformation`). -/
theorem anticomm_frob (θ : ℝ) :
    purityR (anticomm (Qtheta θ) rhoStar) = 2 * Real.sin θ ^ 2 * (1 + Real.sin θ ^ 2) := by
  rw [anticomm_eq]
  unfold purityR
  simp only [Fin.sum_univ_two, Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero,
    Matrix.cons_val_one, Matrix.empty_val', Matrix.cons_val_fin_one]
  have e1 : (2 * (Real.sin θ : ℂ) ^ 2) = ((2 * Real.sin θ ^ 2 : ℝ) : ℂ) := by push_cast; ring
  have e2 : -((Real.sin θ : ℂ) * (Real.cos θ : ℂ)) = ((-(Real.sin θ * Real.cos θ) : ℝ) : ℂ) := by
    push_cast; ring
  have e3 : -((Real.cos θ : ℂ) * (Real.sin θ : ℂ)) = ((-(Real.cos θ * Real.sin θ) : ℝ) : ℂ) := by
    push_cast; ring
  rw [e1, e2, e3, Complex.normSq_ofReal, Complex.normSq_ofReal, Complex.normSq_ofReal, map_zero]
  have hc := Real.sin_sq_add_cos_sq θ
  nlinarith [hc]

/-! ### os valores em θ_M (identidades; sem poder discriminante) -/

theorem sin_sq_thetaMiguel (c : TGLCoupling) : Real.sin (thetaMiguel c.beta) ^ 2 = c.beta := by
  rw [sin_thetaMiguel c.beta_pos.le c.beta_lt_one.le, Real.sq_sqrt c.beta_pos.le]

theorem cos_sq_thetaMiguel (c : TGLCoupling) : Real.cos (thetaMiguel c.beta) ^ 2 = 1 - c.beta := by
  have h := Real.sin_sq_add_cos_sq (thetaMiguel c.beta)
  rw [sin_sq_thetaMiguel] at h
  linarith

theorem sin_mul_cos_thetaMiguel_ne_zero (c : TGLCoupling) :
    Real.sin (thetaMiguel c.beta) * Real.cos (thetaMiguel c.beta) ≠ 0 := by
  intro h
  have h2 : (Real.sin (thetaMiguel c.beta) * Real.cos (thetaMiguel c.beta)) ^ 2 = 0 := by
    rw [h]
    ring
  rw [mul_pow, sin_sq_thetaMiguel, cos_sq_thetaMiguel] at h2
  have h3 : 0 < c.beta * (1 - c.beta) := mul_pos c.beta_pos (by linarith [c.beta_lt_one])
  linarith

/-- [B2.b] c : TGLCoupling: {Q_θM, ρ*} ≠ 0, Tr = 2β, Σ|·|² = 2β(1 + β). -/
theorem anticomm_at_thetaMiguel (c : TGLCoupling) :
    anticomm (Qtheta (thetaMiguel c.beta)) rhoStar ≠ 0
    ∧ (anticomm (Qtheta (thetaMiguel c.beta)) rhoStar).trace = 2 * (c.beta : ℂ)
    ∧ purityR (anticomm (Qtheta (thetaMiguel c.beta)) rhoStar) = 2 * c.beta * (1 + c.beta) := by
  have hs : Real.sin (thetaMiguel c.beta) ≠ 0 := by
    intro h
    have h2 := sin_sq_thetaMiguel c
    rw [h] at h2
    have := c.beta_pos
    norm_num at h2
    linarith
  refine ⟨fun h => hs ((anticomm_zero_iff _).mp h), ?_, ?_⟩
  · rw [anticomm_trace, ← Complex.ofReal_pow, sin_sq_thetaMiguel]
  · rw [anticomm_frob, sin_sq_thetaMiguel]

/-- [B3.a] Tr(ρ*·Q_θ) = sin²θ. -/
theorem leak_eq (θ : ℝ) : (rhoStar * Qtheta θ).trace = (Real.sin θ : ℂ) ^ 2 := by
  rw [rhoStar_eq, Qtheta_eq, Matrix.trace_fin_two]
  simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- [B3.a] Tr(ρ*·Q_θ) = Tr(F_θ(1)·Q₀) = (ρ_out θ)₁₁. -/
theorem leak_eq_rhoOut (θ : ℝ) :
    (rhoStar * Qtheta θ).trace = (rhoOut θ * Q0).trace ∧ (rhoOut θ * Q0).trace = rhoOut θ 1 1 := by
  have h2 : (rhoOut θ * Q0).trace = rhoOut θ 1 1 := by
    rw [Q0_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]
  refine ⟨?_, h2⟩
  rw [h2, leak_eq, rhoOut_one_one]

/-- [B3.a] Tr(ρ*·Q_θ) = |𝓡(θ)|² (o peso refletido da matriz-S). -/
theorem leak_eq_reflected_weight (θ : ℝ) :
    (rhoStar * Qtheta θ).trace = (Complex.normSq ((Smat θ).mulVec e1 1) : ℂ) := by
  rw [leak_eq, normSq_reflection]
  push_cast
  ring

/-- [B3.b] c : TGLCoupling: Tr(ρ*·Q_θM) = β (identidade de θ_M := arcsin √β; validade algébrica). -/
theorem leak_at_thetaMiguel (c : TGLCoupling) :
    (rhoStar * Qtheta (thetaMiguel c.beta)).trace = (c.beta : ℂ) := by
  rw [leak_eq, ← Complex.ofReal_pow, sin_sq_thetaMiguel]

/-! ## 10. B4 — F preserva o Um (regime angular: só lê) -/

section Ad

variable {n : Type} [Fintype n] [DecidableEq n]

/-- [B4.a] uᴴu = 1 ⟹ Tr(u ρ uᴴ) = Tr ρ. -/
theorem ad_trace (u ρ : Matrix n n ℂ) (hu : uᴴ * u = 1) : (u * ρ * uᴴ).trace = ρ.trace := by
  rw [Matrix.trace_mul_cycle, hu, one_mul]

/-- [B4.a] uᴴu = 1 ⟹ posto(u ρ uᴴ) = posto ρ (lacuna L4 do levantamento, via Mathlib). -/
theorem ad_rank (u ρ : Matrix n n ℂ) (hu : uᴴ * u = 1) : (u * ρ * uᴴ).rank = ρ.rank := by
  have hu1 : IsUnit u.det := Matrix.isUnit_det_of_left_inverse hu
  have hu2 : IsUnit uᴴ.det := Matrix.isUnit_det_of_right_inverse hu
  rw [Matrix.rank_mul_eq_left_of_isUnit_det uᴴ (u * ρ) hu2,
    Matrix.rank_mul_eq_right_of_isUnit_det u ρ hu1]

/-- [B4.a] u P uᴴ é projeção quando P é (re-uso de `ad_preserves_projection` e `ad_preserves_star_projection`,
    pedra 116). -/
theorem ad_projection (u P : Matrix n n ℂ) (hu : uᴴ * u = 1) (hP : P * P = P) (hH : Pᴴ = P) :
    (u * P * uᴴ) * (u * P * uᴴ) = u * P * uᴴ ∧ (u * P * uᴴ)ᴴ = u * P * uᴴ := by
  refine ⟨ad_preserves_projection hu hP, ?_⟩
  have h := ad_preserves_star_projection (u := u) (p := P) (by rw [Matrix.star_eq_conjTranspose]; exact hH)
  rw [Matrix.star_eq_conjTranspose, Matrix.star_eq_conjTranspose] at h
  exact h

end Ad

/-- [B4.a] em ρ*: Tr(u ρ* uᴴ) = posto(u ρ* uᴴ) = 1. -/
theorem ad_rhoStar (u : Matrix (Fin 2) (Fin 2) ℂ) (hu : uᴴ * u = 1) :
    (u * rhoStar * uᴴ).trace = 1 ∧ (u * rhoStar * uᴴ).rank = 1 := by
  rw [ad_trace u rhoStar hu, ad_rank u rhoStar hu]
  exact ⟨rhoStar_trace, rhoStar_rank⟩

/-- [B4.b = B5.e(i)] F_θ(1) = ρ_out θ: posto 1, Tr 1, idempotente, hermitiana, pureza 1. -/
theorem fractal_one_is_rank_one (θ : ℝ) :
    (rhoOut θ).rank = 1 ∧ (rhoOut θ).trace = 1 ∧ rhoOut θ * rhoOut θ = rhoOut θ
    ∧ (rhoOut θ)ᴴ = rhoOut θ ∧ (rhoOut θ ^ 2).trace = 1 := by
  have hu : (Smat θ)ᴴ * Smat θ = 1 := Smat_conjTranspose_mul θ
  obtain ⟨htr, hrk⟩ : (rhoOut θ).trace = 1 ∧ (rhoOut θ).rank = 1 := ad_rhoStar (Smat θ) hu
  obtain ⟨hidem, hherm⟩ : rhoOut θ * rhoOut θ = rhoOut θ ∧ (rhoOut θ)ᴴ = rhoOut θ :=
    ad_projection (Smat θ) rhoStar hu rhoStar_idem rhoStar_herm
  exact ⟨hrk, htr, hidem, hherm, by rw [sq, hidem, htr]⟩

/-! ## 11. B5 — o ponto final D_∞ F_θ(1) e o seu posto (a FACE tem limite) -/

/-- sin 2θ = 0 ⟺ sin θ = 0 ∨ cos θ = 0 (auxiliar). -/
theorem sin_two_mul_eq_zero_iff (θ : ℝ) : Real.sin (2 * θ) = 0 ↔ Real.sin θ = 0 ∨ Real.cos θ = 0 := by
  rw [Real.sin_two_mul, mul_assoc, mul_eq_zero, mul_eq_zero]
  simp

/-- c²s² = 0 ⟺ sin θ = 0 ∨ cos θ = 0 (auxiliar, em ℂ). -/
theorem cs_sq_eq_zero_iff (θ : ℝ) :
    (Real.cos θ : ℂ) ^ 2 * (Real.sin θ : ℂ) ^ 2 = 0 ↔ Real.sin θ = 0 ∨ Real.cos θ = 0 := by
  rw [mul_eq_zero, pow_eq_zero_iff two_ne_zero, pow_eq_zero_iff two_ne_zero,
    Complex.ofReal_eq_zero, Complex.ofReal_eq_zero]
  tauto

/-- [B5.a] D_∞ F_θ(1) = diag(c², s²). -/
theorem endpoint_eq (θ : ℝ) :
    diagExpect (rhoOut θ) = diagonal ![(Real.cos θ : ℂ) ^ 2, (Real.sin θ : ℂ) ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagExpect, rhoOut_eq]

theorem endpoint_det (θ : ℝ) :
    (diagExpect (rhoOut θ)).det = (Real.cos θ : ℂ) ^ 2 * (Real.sin θ : ℂ) ^ 2 := by
  rw [endpoint_eq, det_diagonal, Fin.prod_univ_two]
  simp

/-- [B5.a] Tr D_∞ F_θ(1) = 1. -/
theorem endpoint_trace (θ : ℝ) : (diagExpect (rhoOut θ)).trace = 1 := by
  rw [trace_diagExpect, rhoOut_trace]

/-- [B5.a] posto D_∞ F_θ(1) = 2 ⟺ sin 2θ ≠ 0. -/
theorem endpoint_rank_two_iff (θ : ℝ) :
    (diagExpect (rhoOut θ)).rank = 2 ↔ Real.sin (2 * θ) ≠ 0 := by
  rw [rank_two_iff, endpoint_det]
  exact not_congr ((cs_sq_eq_zero_iff θ).trans (sin_two_mul_eq_zero_iff θ).symm)

/-- [B5.a] posto D_∞ F_θ(1) = 1 ⟺ sin 2θ = 0. -/
theorem endpoint_rank_one_iff (θ : ℝ) :
    (diagExpect (rhoOut θ)).rank = 1 ↔ Real.sin (2 * θ) = 0 := by
  rw [rank_one_iff_fin_two, endpoint_det, cs_sq_eq_zero_iff, ← sin_two_mul_eq_zero_iff]
  have hne : diagExpect (rhoOut θ) ≠ 0 :=
    ne_zero_of_trace_ne_zero (by rw [endpoint_trace]; exact one_ne_zero)
  exact ⟨fun h => h.2, fun h => ⟨hne, h⟩⟩

/-- [B5.a] pureza D_∞ F_θ(1) = 1 − 2s²c², e < 1 ⟺ sin 2θ ≠ 0. -/
theorem endpoint_purity (θ : ℝ) :
    ((diagExpect (rhoOut θ)) ^ 2).trace = ((1 - 2 * Real.sin θ ^ 2 * Real.cos θ ^ 2 : ℝ) : ℂ)
    ∧ (1 - 2 * Real.sin θ ^ 2 * Real.cos θ ^ 2 < 1 ↔ Real.sin (2 * θ) ≠ 0) := by
  constructor
  · rw [endpoint_eq, sq, diagonal_mul_diagonal, trace_diagonal, Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
    have hR : ((1 - 2 * Real.sin θ ^ 2 * Real.cos θ ^ 2 : ℝ) : ℂ)
        = 1 - 2 * (Real.sin θ : ℂ) ^ 2 * (Real.cos θ : ℂ) ^ 2 := by
      norm_cast
    have hC : (Real.sin θ : ℂ) ^ 2 + (Real.cos θ : ℂ) ^ 2 = 1 := by
      exact_mod_cast Real.sin_sq_add_cos_sq θ
    rw [hR]
    linear_combination ((Real.sin θ : ℂ) ^ 2 + (Real.cos θ : ℂ) ^ 2 + 1) * hC
  · rw [ne_eq, sin_two_mul_eq_zero_iff]
    constructor
    · intro h hsc
      rcases hsc with hs | hc
      · rw [hs] at h
        simp at h
      · rw [hc] at h
        simp at h
    · intro h
      have hs : Real.sin θ ≠ 0 := (not_or.mp h).1
      have hc : Real.cos θ ≠ 0 := (not_or.mp h).2
      have h2 : 0 < Real.sin θ ^ 2 * Real.cos θ ^ 2 := by positivity
      linarith

/-- [B5.b] b ∈ [0, 1]: posto diag(1 − b, b) = 2 ⟺ 0 < b < 1. -/
theorem rank_diag_two_iff (b : ℝ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    (diagonal ![((1 - b : ℝ) : ℂ), (b : ℂ)]).rank = 2 ↔ (0 < b ∧ b < 1) := by
  rw [rank_two_iff, det_diagonal, Fin.prod_univ_two]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  constructor
  · intro h
    refine ⟨lt_of_le_of_ne hb0 (fun e => h (by rw [← e]; simp)),
      lt_of_le_of_ne hb1 (fun e => h (by rw [e]; simp))⟩
  · rintro ⟨h0, h1⟩ hdet
    have h2 : ((1 - b) * b : ℝ) = 0 := by exact_mod_cast hdet
    rcases mul_eq_zero.mp h2 with h3 | h3 <;> linarith

/-- [B5.b] posto diag(1 − b, b) = 1 em b = 0 e em b = 1. -/
theorem rank_diag_one_at_ends (b : ℝ) (hb : b = 0 ∨ b = 1) :
    (diagonal ![((1 - b : ℝ) : ℂ), (b : ℂ)]).rank = 1 := by
  rw [rank_one_iff_fin_two, det_diagonal, Fin.prod_univ_two]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
  refine ⟨fun h => ?_, ?_⟩
  · have h00 := congrFun (congrFun h 0) 0
    have h11 := congrFun (congrFun h 1) 1
    simp at h00 h11
    rcases hb with hb | hb
    · rw [hb] at h00
      norm_num at h00
    · rw [hb] at h11
      norm_num at h11
  · rcases hb with hb | hb <;> rw [hb] <;> simp

/-- [B5.b] c : TGLCoupling: D_∞ F_θM(1) = diag(1 − β, β), posto 2, pureza 1 − 2β(1 − β) < 1. -/
theorem endpoint_at_thetaMiguel (c : TGLCoupling) :
    diagExpect (rhoOut (thetaMiguel c.beta)) = diagonal ![((1 - c.beta : ℝ) : ℂ), (c.beta : ℂ)]
    ∧ (diagExpect (rhoOut (thetaMiguel c.beta))).rank = 2
    ∧ ((diagExpect (rhoOut (thetaMiguel c.beta))) ^ 2).trace
        = ((1 - 2 * c.beta * (1 - c.beta) : ℝ) : ℂ)
    ∧ 1 - 2 * c.beta * (1 - c.beta) < 1 := by
  have hs' : (Real.sin (thetaMiguel c.beta) : ℂ) ^ 2 = ((c.beta : ℝ) : ℂ) := by
    rw [← Complex.ofReal_pow, sin_sq_thetaMiguel]
  have hc' : (Real.cos (thetaMiguel c.beta) : ℂ) ^ 2 = ((1 - c.beta : ℝ) : ℂ) := by
    rw [← Complex.ofReal_pow, cos_sq_thetaMiguel]
  have heq : diagExpect (rhoOut (thetaMiguel c.beta))
      = diagonal ![((1 - c.beta : ℝ) : ℂ), (c.beta : ℂ)] := by
    rw [endpoint_eq, hs', hc']
  have hpos : 0 < c.beta * (1 - c.beta) := mul_pos c.beta_pos (by linarith [c.beta_lt_one])
  refine ⟨heq, ?_, ?_, by nlinarith⟩
  · rw [heq]
    exact (rank_diag_two_iff c.beta c.beta_pos.le c.beta_lt_one.le).mpr ⟨c.beta_pos, c.beta_lt_one⟩
  · have h := (endpoint_purity (thetaMiguel c.beta)).1
    rw [sin_sq_thetaMiguel, cos_sq_thetaMiguel] at h
    exact h

/-- [P3.b] os pesos da leitura no ponto final: Tr(ρ*·D_∞F_θ(1)) = |𝓣(θ)|² e Tr(Q₀·D_∞F_θ(1)) = |𝓡(θ)|². -/
theorem reading_weights_at_theta (θ : ℝ) :
    (rhoStar * diagExpect (rhoOut θ)).trace = (Complex.normSq ((Smat θ).mulVec e1 0) : ℂ)
    ∧ (Q0 * diagExpect (rhoOut θ)).trace = (Complex.normSq ((Smat θ).mulVec e1 1) : ℂ) := by
  rw [normSq_transmission, normSq_reflection, endpoint_eq]
  constructor
  · rw [rhoStar_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]
  · rw [Q0_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- [P3.b] em θ_M (b = β): Tr(ρ*·diag(1 − β, β)) = |𝓣(θ_M)|² = 1 − β e Tr(Q₀·diag(1 − β, β)) = |𝓡(θ_M)|² = β
    (identidades de θ_M := arcsin √β; validade algébrica, sem poder discriminante). -/
theorem reading_weights_at_thetaMiguel (c : TGLCoupling) :
    (rhoStar * diagonal ![((1 - c.beta : ℝ) : ℂ), (c.beta : ℂ)]).trace
        = (Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 0) : ℂ)
    ∧ (Q0 * diagonal ![((1 - c.beta : ℝ) : ℂ), (c.beta : ℂ)]).trace
        = (Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) : ℂ)
    ∧ Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 0) = 1 - c.beta
    ∧ Complex.normSq ((Smat (thetaMiguel c.beta)).mulVec e1 1) = c.beta := by
  refine ⟨?_, ?_, by rw [normSq_transmission, cos_sq_thetaMiguel], c.reflection_weight⟩
  · rw [← (endpoint_at_thetaMiguel c).1]
    exact (reading_weights_at_theta (thetaMiguel c.beta)).1
  · rw [← (endpoint_at_thetaMiguel c).1]
    exact (reading_weights_at_theta (thetaMiguel c.beta)).2

/-! ### B5.c — o semigrupo em tempo finito -/

/-- D_t F_θ(1), entrada a entrada (g_ii = 0). -/
theorem dephased_rhoOut_eq (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    dephase g t (rhoOut θ)
      = !![(Real.cos θ : ℂ) ^ 2, (Real.exp (-(t * g 0 1)) : ℂ) * -((Real.cos θ : ℂ) * (Real.sin θ : ℂ));
          (Real.exp (-(t * g 1 0)) : ℂ) * -((Real.sin θ : ℂ) * (Real.cos θ : ℂ)), (Real.sin θ : ℂ) ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [dephase, rhoOut_eq, hg0]

/-- [B5.c] det D_t F_θ(1) = c² s² (1 − e^{−t(g₀₁ + g₁₀)}). -/
theorem dephased_det (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    (dephase g t (rhoOut θ)).det
      = (((Real.cos θ ^ 2 * Real.sin θ ^ 2) * (1 - Real.exp (-(t * (g 0 1 + g 1 0)))) : ℝ) : ℂ) := by
  rw [dephased_rhoOut_eq θ g hg0 t, Matrix.det_fin_two_of]
  have hexp : Real.exp (-(t * g 0 1)) * Real.exp (-(t * g 1 0))
      = Real.exp (-(t * (g 0 1 + g 1 0))) := by
    rw [← Real.exp_add]
    congr 1
    ring
  have hreal : Real.cos θ ^ 2 * Real.sin θ ^ 2
        - (Real.exp (-(t * g 0 1)) * -(Real.cos θ * Real.sin θ))
          * (Real.exp (-(t * g 1 0)) * -(Real.sin θ * Real.cos θ))
      = (Real.cos θ ^ 2 * Real.sin θ ^ 2) * (1 - Real.exp (-(t * (g 0 1 + g 1 0)))) := by
    rw [← hexp]
    ring
  rw [← hreal]
  push_cast
  ring

/-- [B5.c] g_ii = 0, g₀₁, g₁₀ > 0, t > 0: posto D_t F_θ(1) = 2 ⟺ sin 2θ ≠ 0. -/
theorem dephased_rank_two_iff (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (h01 : 0 < g 0 1) (h10 : 0 < g 1 0) {t : ℝ} (ht : 0 < t) :
    (dephase g t (rhoOut θ)).rank = 2 ↔ Real.sin (2 * θ) ≠ 0 := by
  rw [rank_two_iff, dephased_det θ g hg0 t]
  have hpos : 0 < 1 - Real.exp (-(t * (g 0 1 + g 1 0))) := by
    have h1 : 0 < t * (g 0 1 + g 1 0) := mul_pos ht (by linarith)
    have h2 : Real.exp (-(t * (g 0 1 + g 1 0))) < 1 := Real.exp_lt_one_iff.mpr (by linarith)
    linarith
  have hX : Real.cos θ ^ 2 * Real.sin θ ^ 2 = 0 ↔ Real.sin θ = 0 ∨ Real.cos θ = 0 := by
    rw [mul_eq_zero, pow_eq_zero_iff two_ne_zero, pow_eq_zero_iff two_ne_zero]
    tauto
  rw [ne_eq, ne_eq, Complex.ofReal_eq_zero, mul_eq_zero, hX, ← sin_two_mul_eq_zero_iff]
  constructor
  · intro h h2
    exact h (Or.inl h2)
  · intro h h2
    rcases h2 with h2 | h2
    · exact h h2
    · exact (ne_of_gt hpos) h2

/-- [B5.c] t = 0: posto 1. -/
theorem dephased_rank_at_zero (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) :
    (dephase g 0 (rhoOut θ)).rank = 1 := by
  rw [dephase_zero]
  exact (fractal_one_is_rank_one θ).1

/-- [B5.c] o traço é preservado em todo t. -/
theorem dephased_trace (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    (dephase g t (rhoOut θ)).trace = 1 := by
  rw [dephase_preserves_trace g hg0 t, rhoOut_trace]

/-! ### B5.e — sobrevive o traço, não o posto -/

/-- [B5.e(ii), NEGATIVO HONESTO] «para todo θ, posto D_∞ F_θ(1) = posto F_θ(1)» é FALSO; testemunha θ_M. -/
theorem rank_not_preserved_by_dephasing (c : TGLCoupling) :
    ¬ ∀ θ : ℝ, (diagExpect (rhoOut θ)).rank = (rhoOut θ).rank := by
  intro h
  have h1 := h (thetaMiguel c.beta)
  rw [(endpoint_at_thetaMiguel c).2.1, (fractal_one_is_rank_one _).1] at h1
  exact absurd h1 (by norm_num)

/-- [B5.e(ii)] o que sobrevive: Tr D_∞ F_θ(1) = Tr F_θ(1). -/
theorem trace_survives_dephasing (θ : ℝ) : (diagExpect (rhoOut θ)).trace = (rhoOut θ).trace :=
  trace_diagExpect _

/-! ## 12. B6 — o vazamento sobrevive à defasagem -/

/-- [B6.a] g_ii = 0: Tr(ρ*·D_t Q_θ) = sin²θ para todo t. -/
theorem leak_survives_dephasing (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    (rhoStar * dephase g t (Qtheta θ)).trace = (Real.sin θ : ℂ) ^ 2 := by
  rw [rhoStar_eq, Matrix.trace_fin_two]
  simp [Matrix.mul_apply, Fin.sum_univ_two, dephase, hg0, Qtheta_eq]

/-- D_t Q_θ, entrada a entrada (taxas quaisquer). -/
theorem dephased_Qtheta_eq (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (t : ℝ) :
    dephase g t (Qtheta θ)
      = !![(Real.exp (-(t * g 0 0)) : ℂ) * (Real.sin θ : ℂ) ^ 2,
          (Real.exp (-(t * g 0 1)) : ℂ) * -((Real.sin θ : ℂ) * (Real.cos θ : ℂ));
          (Real.exp (-(t * g 1 0)) : ℂ) * -((Real.cos θ : ℂ) * (Real.sin θ : ℂ)),
          (Real.exp (-(t * g 1 1)) : ℂ) * (Real.cos θ : ℂ) ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [dephase, Qtheta_eq]

/-- [B6.b] {D_t Q_θ, ρ*} = [[2s², −e^{−t g₀₁} sc], [−e^{−t g₁₀} cs, 0]] (g_ii = 0). -/
theorem anticomm_dephased_eq (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    anticomm (dephase g t (Qtheta θ)) rhoStar
      = !![2 * (Real.sin θ : ℂ) ^ 2,
          (Real.exp (-(t * g 0 1)) : ℂ) * -((Real.sin θ : ℂ) * (Real.cos θ : ℂ));
          (Real.exp (-(t * g 1 0)) : ℂ) * -((Real.cos θ : ℂ) * (Real.sin θ : ℂ)), 0] := by
  rw [anticomm, dephased_Qtheta_eq, rhoStar_eq, hg0 0, hg0 1]
  ext i j
  fin_cases i <;> fin_cases j <;> simp
  all_goals ring

/-- A entrada (0,0) de {D_t Q_θ, ρ*} para taxas quaisquer: 2·e^{−t g₀₀}·s². -/
theorem anticomm_dephased_entry00 (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (t : ℝ) :
    (anticomm (dephase g t (Qtheta θ)) rhoStar) 0 0
      = 2 * ((Real.exp (-(t * g 0 0)) : ℂ) * (Real.sin θ : ℂ) ^ 2) := by
  rw [anticomm, dephased_Qtheta_eq, rhoStar_eq]
  simp
  all_goals ring

/-- [B6.b] {D_t Q_θ, ρ*} = 0 ⟺ sin θ = 0 (vale para quaisquer taxas; g_ii = 0 não é necessária). -/
theorem anticomm_dephased_zero_iff (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (t : ℝ) :
    anticomm (dephase g t (Qtheta θ)) rhoStar = 0 ↔ Real.sin θ = 0 := by
  constructor
  · intro h
    have h00 := anticomm_dephased_entry00 θ g t
    rw [h, Matrix.zero_apply] at h00
    have hE : (Real.exp (-(t * g 0 0)) : ℂ) ≠ 0 := by exact_mod_cast (Real.exp_pos _).ne'
    have h2 : (Real.sin θ : ℂ) ^ 2 = 0 := by
      rcases mul_eq_zero.mp h00.symm with h3 | h3
      · norm_num at h3
      · rcases mul_eq_zero.mp h3 with h4 | h4
        · exact absurd h4 hE
        · exact h4
    exact Complex.ofReal_eq_zero.mp ((pow_eq_zero_iff two_ne_zero).mp h2)
  · intro h
    rw [anticomm, dephased_Qtheta_eq, rhoStar_eq, h]
    ext i j
    fin_cases i <;> fin_cases j <;> simp

/-- D_∞ Q_θ = diag(s², c²). -/
theorem diagExpect_Qtheta (θ : ℝ) :
    diagExpect (Qtheta θ) = !![(Real.sin θ : ℂ) ^ 2, 0; 0, (Real.cos θ : ℂ) ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [diagExpect, Qtheta_eq]

/-- [B6.b] {D_∞ Q_θ, ρ*} = diag(2 s², 0). -/
theorem anticomm_limit (θ : ℝ) :
    anticomm (diagExpect (Qtheta θ)) rhoStar = diagonal ![2 * (Real.sin θ : ℂ) ^ 2, 0] := by
  rw [anticomm, diagExpect_Qtheta, rhoStar_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp
  all_goals ring

/-- [B6.b, complemento fora do pré-registro: o LIMITE da face] com taxas positivas, {D_t Q_θ, ρ*} → diag(2 s², 0). -/
theorem anticomm_dephased_tendsto (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (hgpos : ∀ i j, i ≠ j → 0 < g i j) :
    Tendsto (fun t => anticomm (dephase g t (Qtheta θ)) rhoStar) atTop
      (𝓝 (diagonal ![2 * (Real.sin θ : ℂ) ^ 2, 0])) := by
  rw [← anticomm_limit]
  have h := dephase_tendsto_expectation g hg0 hgpos (Qtheta θ)
  have hcont : Continuous fun y : Matrix (Fin 2) (Fin 2) ℂ => anticomm y rhoStar := by
    unfold anticomm
    exact (continuous_id.matrix_mul continuous_const).add (continuous_const.matrix_mul continuous_id)
  exact (hcont.tendsto _).comp h

/-! ## 13. B7 — os dois regimes: o ângulo não tem limite; a face tem -/

/-- [B7.a1] S(θ)ⁿ = S(nθ): iterar o ângulo é girar o ângulo. -/
theorem Smat_pow (θ : ℝ) (k : ℕ) : Smat θ ^ k = Smat (k * θ) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ih, Smat_mul]
    congr 1
    push_cast
    ring

/-- [B7.a1] o peso refletido após n passagens é sin²(nθ). -/
theorem leak_after_n_passes (θ : ℝ) (k : ℕ) :
    Complex.normSq ((Smat θ ^ k).mulVec e1 1) = Real.sin (k * θ) ^ 2 := by
  rw [Smat_pow, normSq_reflection]

theorem sin_sq_shift_identity (x θ : ℝ) :
    Real.sin (x + θ) ^ 2 + Real.sin (x - θ) ^ 2
      = 2 * Real.sin x ^ 2 * Real.cos θ ^ 2 + 2 * Real.cos x ^ 2 * Real.sin θ ^ 2 := by
  rw [Real.sin_add, Real.sin_sub]
  ring

theorem sin_sq_double (x : ℝ) : Real.sin (2 * x) ^ 2 = 4 * Real.sin x ^ 2 * (1 - Real.sin x ^ 2) := by
  rw [Real.sin_two_mul, ← Real.cos_sq' x]
  ring

/-- [B7.a2] sin θ ≠ 0 ⟹ sin²(nθ) NÃO tem limite (o ângulo só lê; o limite nunca é pedido a ele).
    Prova: um limite L teria de valer 1/2 (recorrência de três termos) e satisfazer L = 4L(1 − L) (duplicação). -/
theorem angular_leak_no_limit (θ : ℝ) (h : Real.sin θ ≠ 0) :
    ¬ ∃ L : ℝ, Tendsto (fun k : ℕ => Real.sin (k * θ) ^ 2) atTop (𝓝 L) := by
  rintro ⟨L, hL⟩
  have h1 : Tendsto (fun k : ℕ => Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2) atTop (𝓝 L) :=
    hL.comp (tendsto_add_atTop_nat 1)
  have h2 : Tendsto (fun k : ℕ => Real.sin (((k + 2 : ℕ) : ℝ) * θ) ^ 2) atTop (𝓝 L) :=
    hL.comp (tendsto_add_atTop_nat 2)
  have hdbl : Tendsto (fun k : ℕ => Real.sin (((2 * k : ℕ) : ℝ) * θ) ^ 2) atTop (𝓝 L) :=
    hL.comp (tendsto_atTop_mono (fun k => show k ≤ 2 * k by omega) tendsto_id)
  have hid : ∀ k : ℕ, Real.sin (((k + 2 : ℕ) : ℝ) * θ) ^ 2 + Real.sin ((k : ℝ) * θ) ^ 2
      = 2 * Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2 * Real.cos θ ^ 2
        + 2 * (1 - Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2) * Real.sin θ ^ 2 := by
    intro k
    have e1 : ((k + 2 : ℕ) : ℝ) * θ = ((k + 1 : ℕ) : ℝ) * θ + θ := by push_cast; ring
    have e2 : (k : ℝ) * θ = ((k + 1 : ℕ) : ℝ) * θ - θ := by push_cast; ring
    rw [e1, e2, sin_sq_shift_identity, Real.cos_sq' (((k + 1 : ℕ) : ℝ) * θ)]
  have hlim1 : Tendsto (fun k : ℕ => Real.sin (((k + 2 : ℕ) : ℝ) * θ) ^ 2
      + Real.sin ((k : ℝ) * θ) ^ 2) atTop (𝓝 (L + L)) := h2.add hL
  have hlim2 : Tendsto (fun k : ℕ => 2 * Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2 * Real.cos θ ^ 2
      + 2 * (1 - Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2) * Real.sin θ ^ 2) atTop
      (𝓝 (2 * L * Real.cos θ ^ 2 + 2 * (1 - L) * Real.sin θ ^ 2)) :=
    ((h1.const_mul 2).mul_const _).add (((tendsto_const_nhds.sub h1).const_mul 2).mul_const _)
  have hEq : L + L = 2 * L * Real.cos θ ^ 2 + 2 * (1 - L) * Real.sin θ ^ 2 := by
    have hfun : (fun k : ℕ => Real.sin (((k + 2 : ℕ) : ℝ) * θ) ^ 2 + Real.sin ((k : ℝ) * θ) ^ 2)
        = (fun k : ℕ => 2 * Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2 * Real.cos θ ^ 2
          + 2 * (1 - Real.sin (((k + 1 : ℕ) : ℝ) * θ) ^ 2) * Real.sin θ ^ 2) := funext hid
    rw [hfun] at hlim1
    exact tendsto_nhds_unique hlim1 hlim2
  have hs2 : 0 < Real.sin θ ^ 2 := by positivity
  have hL12 : L = 1 / 2 := by
    rw [Real.cos_sq' θ] at hEq
    have h3 : Real.sin θ ^ 2 * (2 - 4 * L) = 0 := by linear_combination (-1 : ℝ) * hEq
    rcases mul_eq_zero.mp h3 with h4 | h4
    · linarith
    · linarith
  have hdbl_id : ∀ k : ℕ, Real.sin (((2 * k : ℕ) : ℝ) * θ) ^ 2
      = 4 * Real.sin ((k : ℝ) * θ) ^ 2 * (1 - Real.sin ((k : ℝ) * θ) ^ 2) := by
    intro k
    rw [show ((2 * k : ℕ) : ℝ) * θ = 2 * ((k : ℝ) * θ) by push_cast; ring, sin_sq_double]
  have hlim3 : Tendsto (fun k : ℕ => 4 * Real.sin ((k : ℝ) * θ) ^ 2 * (1 - Real.sin ((k : ℝ) * θ) ^ 2))
      atTop (𝓝 (4 * L * (1 - L))) := (hL.const_mul 4).mul (tendsto_const_nhds.sub hL)
  have hEq2 : L = 4 * L * (1 - L) := by
    have hfun : (fun k : ℕ => Real.sin (((2 * k : ℕ) : ℝ) * θ) ^ 2)
        = (fun k : ℕ => 4 * Real.sin ((k : ℝ) * θ) ^ 2 * (1 - Real.sin ((k : ℝ) * θ) ^ 2)) :=
      funext hdbl_id
    rw [hfun] at hdbl
    exact tendsto_nhds_unique hdbl hlim3
  rw [hL12] at hEq2
  norm_num at hEq2

/-- [B7.a2] a mesma ausência de limite, lida no peso refletido da matriz-S iterada. -/
theorem angular_reflected_weight_no_limit (θ : ℝ) (h : Real.sin θ ≠ 0) :
    ¬ ∃ L : ℝ, Tendsto (fun k : ℕ => Complex.normSq ((Smat θ ^ k).mulVec e1 1)) atTop (𝓝 L) := by
  simp_rw [leak_after_n_passes]
  exact angular_leak_no_limit θ h

/-- [B7.a2] sin θ = 0 ⟹ sin²(nθ) = 0 para todo n (constante; converge a 0). -/
theorem angular_leak_zero_converges (θ : ℝ) (h : Real.sin θ = 0) :
    (∀ k : ℕ, Real.sin (k * θ) ^ 2 = 0)
    ∧ Tendsto (fun k : ℕ => Real.sin (k * θ) ^ 2) atTop (𝓝 0) := by
  obtain ⟨m, hm⟩ := Real.sin_eq_zero_iff.mp h
  have hall : ∀ k : ℕ, Real.sin (k * θ) ^ 2 = 0 := by
    intro k
    rw [← hm, show (k : ℝ) * ((m : ℝ) * Real.pi) = (((k : ℤ) * m : ℤ) : ℝ) * Real.pi by push_cast; ring,
      Real.sin_int_mul_pi]
    ring
  refine ⟨hall, ?_⟩
  simp_rw [hall]
  exact tendsto_const_nhds

/-- [B7.b, CITADO_REAL — re-exportação TRIVIAL de `dephase_tendsto_expectation`] taxas > 0 ⟹ D_t x → D_∞ x. -/
theorem dephasing_has_limit {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ)
    (hg0 : ∀ i, g i i = 0) (hgpos : ∀ i j, i ≠ j → 0 < g i j) (x : Matrix n n ℂ) :
    Tendsto (fun t => dephase g t x) atTop (𝓝 (diagExpect x)) :=
  dephase_tendsto_expectation g hg0 hgpos x

/-- [B7.c, CITADO_REAL — re-exportação TRIVIAL de `IALDJones.orbit_tendsto_center`] r > 0 ⟹ a órbita converge ao centro. -/
theorem spiral_with_rate_converges {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) {r : ℝ} (hr : 0 < r) (ω : ℝ) (v : V) :
    Tendsto (fun s => IALDJones.orbit P r ω s v) atTop (𝓝 (P v)) :=
  IALDJones.orbit_tendsto_center P hr ω v

/-- [B7.c, CITADO_REAL — re-exportação TRIVIAL de `IALDJones.angular_orbit_no_limit`] r = 0: sem limite no centro. -/
theorem spiral_without_rate_has_no_limit {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) (ω : ℝ) (v : V) (hv : v ≠ P v) :
    ¬ Tendsto (fun s => IALDJones.orbit P 0 ω s v) atTop (𝓝 (P v)) :=
  IALDJones.angular_orbit_no_limit P ω v hv

/-- [B7.c, CITADO_REAL — re-exportação TRIVIAL de `IALDJones.angular_orbit_periodic`] r = 0, ω ≠ 0: periódica. -/
theorem spiral_without_rate_is_periodic {V : Type} [NormedAddCommGroup V] [NormedSpace ℂ V]
    (P : V →ₗ[ℂ] V) {ω : ℝ} (hω : ω ≠ 0) (s : ℝ) (v : V) :
    IALDJones.orbit P 0 ω (s + 2 * Real.pi / ω) v = IALDJones.orbit P 0 ω s v :=
  IALDJones.angular_orbit_periodic P hω s v

/-! ## 14. B8 — o ramo do nada (álgebra; «nada» não é termo) -/

theorem rhoOut_zero : rhoOut 0 = rhoStar := by
  simp [rhoOut, rhoStar]

theorem dephase_rhoStar (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    dephase g t rhoStar = rhoStar := by
  rw [rhoStar_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [dephase, hg0]

/-- [B8.a] θ = 0: Tr(ρ*Q₀) = 0, {Q₀, ρ*} = 0, F₀(1) = ρ* = D_t ρ* para todo t; posto 1; pureza 1. -/
theorem nothing_branch :
    (rhoStar * Q0).trace = 0 ∧ anticomm Q0 rhoStar = 0 ∧ rhoOut 0 = rhoStar
    ∧ (∀ g : Fin 2 → Fin 2 → ℝ, (∀ i, g i i = 0) → ∀ t, dephase g t (rhoOut 0) = rhoOut 0)
    ∧ rhoStar.rank = 1 ∧ (rhoStar ^ 2).trace = 1 := by
  refine ⟨?_, ?_, rhoOut_zero, ?_, rhoStar_rank, ?_⟩
  · rw [rhoStar_eq, Q0_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]
  · rw [← Qtheta_zero]
    exact (anticomm_zero_iff 0).mpr Real.sin_zero
  · intro g hg0 t
    rw [rhoOut_zero]
    exact dephase_rhoStar g hg0 t
  · rw [sq, rhoStar_idem, rhoStar_trace]

/-- ρ_out θ é diagonal ⟺ sin 2θ = 0 (auxiliar). -/
theorem rhoOut_eq_diag_iff (θ : ℝ) : rhoOut θ = diagExpect (rhoOut θ) ↔ Real.sin (2 * θ) = 0 := by
  rw [sin_two_mul_eq_zero_iff]
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    have h01' : rhoOut θ 0 1 = 0 := by
      rw [h01]
      simp [diagExpect]
    rw [rhoOut_eq] at h01'
    simp only [Matrix.of_apply, Matrix.cons_val', Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.empty_val', Matrix.cons_val_fin_one, neg_eq_zero, mul_eq_zero,
      Complex.ofReal_eq_zero] at h01'
    tauto
  · intro h
    ext i j
    rcases h with h | h <;> fin_cases i <;> fin_cases j <;> simp [diagExpect, rhoOut_eq, h]

/-- [B8.b] (∀ t, D_t F_θ(1) = F_θ(1)) ⟺ sin 2θ = 0. -/
theorem dephasing_trivial_iff (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (h01 : 0 < g 0 1) (h10 : 0 < g 1 0) :
    (∀ t, dephase g t (rhoOut θ) = rhoOut θ) ↔ Real.sin (2 * θ) = 0 := by
  have hgpos : ∀ i j, i ≠ j → 0 < g i j := by
    intro i j hij
    fin_cases i <;> fin_cases j
    · exact absurd rfl hij
    · exact h01
    · exact h10
    · exact absurd rfl hij
  rw [dephase_fixed_iff_diagonal g hg0 hgpos, rhoOut_eq_diag_iff]

theorem cos_thetaMiguel {b : ℝ} (hb0 : 0 ≤ b) : Real.cos (thetaMiguel b) = Real.sqrt (1 - b) := by
  unfold thetaMiguel
  rw [Real.cos_arcsin, Real.sq_sqrt hb0]

/-- [B8.b] em θ = θ_M(b), b ∈ [0, 1]: sin 2θ = 0 ⟺ b = 0 ∨ b = 1. -/
theorem sin_two_thetaMiguel_eq_zero_iff (b : ℝ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    Real.sin (2 * thetaMiguel b) = 0 ↔ b = 0 ∨ b = 1 := by
  rw [sin_two_mul_eq_zero_iff, sin_thetaMiguel hb0 hb1, cos_thetaMiguel hb0,
    Real.sqrt_eq_zero hb0, Real.sqrt_eq_zero (by linarith)]
  constructor
  · rintro (h | h)
    · exact Or.inl h
    · exact Or.inr (by linarith)
  · rintro (h | h)
    · exact Or.inl h
    · exact Or.inr (by linarith)

/-- [B8.b, forma literal] D trivial em θ_M(b) ⟺ b = 0 ∨ b = 1; e o posto é 1 nos dois ramos. -/
theorem dephasing_trivial_at_thetaMiguel (b : ℝ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1)
    (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (h01 : 0 < g 0 1) (h10 : 0 < g 1 0) :
    ((∀ t, dephase g t (rhoOut (thetaMiguel b)) = rhoOut (thetaMiguel b)) ↔ (b = 0 ∨ b = 1))
    ∧ (rhoOut (thetaMiguel b)).rank = 1 := by
  refine ⟨?_, (fractal_one_is_rank_one _).1⟩
  rw [dephasing_trivial_iff _ g hg0 h01 h10, sin_two_thetaMiguel_eq_zero_iff b hb0 hb1]

/-! ## 15. B9 — a sonda honesta: o que transmite defasa? -/

theorem dephasingActs_iff (g : Fin 2 → Fin 2 → ℝ) (θ : ℝ) :
    dephasingActs g θ ↔ ¬ ∀ t, dephase g t (rhoOut θ) = rhoOut θ :=
  not_forall.symm

/-- [B9.a, NEGATIVO HONESTO = C12] a leitura LITERAL (transmitir = |𝓣|² > 0 ⟹ D atua) é FALSA; testemunha θ = 0. -/
theorem literal_transmission_does_not_force_dephasing (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) :
    ¬ ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 0) → dephasingActs g θ := by
  intro h
  obtain ⟨t, ht⟩ := h 0 (by rw [normSq_transmission, Real.cos_zero]; norm_num)
  apply ht
  rw [rhoOut_zero]
  exact dephase_rhoStar g hg0 t

theorem rhoOut_pi_div_two : rhoOut (Real.pi / 2) = Q0 := by
  rw [rhoOut_eq, Q0_eq, Real.cos_pi_div_two, Real.sin_pi_div_two]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

theorem dephase_Q0 (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) (t : ℝ) :
    dephase g t Q0 = Q0 := by
  rw [Q0_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [dephase, hg0]

/-- [B9.a', CONTROLE = C13] a leitura simétrica (vazar = |𝓡|² > 0 ⟹ D atua) é FALSA; testemunha θ = π/2. -/
theorem literal_leak_does_not_force_dephasing (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) :
    ¬ ∀ θ : ℝ, 0 < Complex.normSq ((Smat θ).mulVec e1 1) → dephasingActs g θ := by
  intro h
  obtain ⟨t, ht⟩ := h (Real.pi / 2) (by rw [normSq_reflection, Real.sin_pi_div_two]; norm_num)
  apply ht
  rw [rhoOut_pi_div_two]
  exact dephase_Q0 g hg0 t

/-- [B9.b] a leitura de INSCRIÇÃO: D atua ⟺ |𝓣|² > 0 e |𝓡|² > 0 (transmite E vaza). -/
theorem dephasing_acts_iff_transmits_and_leaks (θ : ℝ) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (h01 : 0 < g 0 1) (h10 : 0 < g 1 0) :
    dephasingActs g θ
      ↔ (0 < Complex.normSq ((Smat θ).mulVec e1 0) ∧ 0 < Complex.normSq ((Smat θ).mulVec e1 1)) := by
  rw [dephasingActs_iff, dephasing_trivial_iff θ g hg0 h01 h10, sin_two_mul_eq_zero_iff,
    normSq_transmission, normSq_reflection]
  constructor
  · intro h
    have hs : Real.sin θ ≠ 0 := fun hs => h (Or.inl hs)
    have hc : Real.cos θ ≠ 0 := fun hc => h (Or.inr hc)
    exact ⟨by positivity, by positivity⟩
  · rintro ⟨hc, hs⟩ h
    rcases h with h | h
    · rw [h] at hs
      norm_num at hs
    · rw [h] at hc
      norm_num at hc

/-- [B9.b] c : TGLCoupling: em θ_M D atua e (D_∞ F(1))₁₁ = β. -/
theorem inscription_at_thetaMiguel (c : TGLCoupling) (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0)
    (h01 : 0 < g 0 1) (h10 : 0 < g 1 0) :
    dephasingActs g (thetaMiguel c.beta) ∧ diagExpect (rhoOut (thetaMiguel c.beta)) 1 1 = (c.beta : ℂ) := by
  refine ⟨?_, ?_⟩
  · rw [dephasing_acts_iff_transmits_and_leaks _ g hg0 h01 h10, normSq_transmission, normSq_reflection,
      sin_sq_thetaMiguel, cos_sq_thetaMiguel]
    exact ⟨by linarith [c.beta_lt_one], c.beta_pos⟩
  · rw [dephased_rhoOut_one_one, ← Complex.ofReal_pow, sin_sq_thetaMiguel]

/-- [B9.c, CITADO_REAL — re-exportação TRIVIAL de `TheVerbSelectsTheAction.transmission_dephases`]
    «transmitir defasa» (05/10): F(t)(1 − P) = e^{−t}(1 − P) no fluxo do lock mínimo. -/
theorem transmission_dephases_reexport {A : Type*} [Ring A] [Algebra ℂ A] {P : A}
    (hP : IsIdempotentElem P) (t : ℝ) :
    TheAxiomAndTheFalseWitness.axiomFlow P t * (1 - P) = ((Real.exp (-t) : ℝ) : ℂ) • (1 - P) :=
  TheVerbSelectsTheAction.transmission_dephases hP t

/-! ## 16. Os CONTROLES C1–C14 (esperado: FALHA_SEM_HIPOTESE) -/

/-- C1: diag(2/3, 2/3, −1/3) em M₃(ℂ). -/
def C1mat : Matrix (Fin 3) (Fin 3) ℂ := diagonal ![2 / 3, 2 / 3, -1 / 3]

/-- [C1 — P1.a] sem positividade: Tr = 1, Tr(·²) = 1, posto 3, não ⪰ 0. -/
theorem psd_is_necessary :
    C1mat.trace = 1 ∧ (C1mat ^ 2).trace = 1 ∧ C1mat.rank = 3 ∧ ¬ C1mat.PosSemidef := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [C1mat, trace_diagonal, Fin.sum_univ_three]
    simp
    norm_num
  · rw [C1mat, sq, diagonal_mul_diagonal, trace_diagonal, Fin.sum_univ_three]
    simp
    norm_num
  · have h := rank_eq_card_iff_det_ne_zero C1mat
    rw [Fintype.card_fin] at h
    refine h.mpr ?_
    rw [C1mat, det_diagonal, Fin.prod_univ_three]
    simp
  · intro h
    have h2 := (Matrix.posSemidef_diagonal_iff.mp h) 2
    simp [Complex.nonneg_iff] at h2
    norm_num at h2

/-- [C1, forma «a hipótese é necessária»] sem ⪰ 0, «Tr = Tr² = 1 ⟹ posto 1» falha em M₃(ℂ). -/
theorem psd_is_necessary' :
    ¬ ∀ ρ : Matrix (Fin 3) (Fin 3) ℂ, ρ.trace = 1 → (ρ ^ 2).trace = 1 → ρ.rank = 1 := by
  intro h
  obtain ⟨h1, h2, h3, -⟩ := psd_is_necessary
  have := h C1mat h1 h2
  rw [h3] at this
  norm_num at this

/-- [C2 — P1.a] ρ*/2: ⪰ 0, posto 1, Tr(·²) = 1/4 (a normalização é necessária). -/
theorem normalization_is_necessary :
    ((2⁻¹ : ℂ) • rhoStar).PosSemidef ∧ ((2⁻¹ : ℂ) • rhoStar).rank = 1
    ∧ (((2⁻¹ : ℂ) • rhoStar) ^ 2).trace = 4⁻¹ := by
  have hdiag : (2⁻¹ : ℂ) • rhoStar = diagonal ![(2⁻¹ : ℂ), 0] := by
    rw [rhoStar_eq]
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  refine ⟨?_, ?_, ?_⟩
  · rw [hdiag]
    refine Matrix.posSemidef_diagonal_iff.mpr ?_
    intro i
    fin_cases i <;> simp
  · rw [rank_one_iff_fin_two, hdiag, det_diagonal, Fin.prod_univ_two]
    refine ⟨fun h => ?_, by simp⟩
    have h00 := congrFun (congrFun h 0) 0
    simp at h00
  · rw [hdiag, sq, diagonal_mul_diagonal, trace_diagonal, Fin.sum_univ_two]
    simp
    norm_num

/-- [C2, forma «a hipótese é necessária»] sem Tr = 1, «⪰ 0 ∧ posto 1 ⟹ Tr ρ² = 1» falha. -/
theorem normalization_is_necessary' :
    ¬ ∀ ρ : Matrix (Fin 2) (Fin 2) ℂ, ρ.PosSemidef → ρ.rank = 1 → (ρ ^ 2).trace = 1 := by
  intro h
  obtain ⟨h1, h2, h3⟩ := normalization_is_necessary
  have := h _ h1 h2
  rw [h3] at this
  norm_num at this

/-- [C3 — B1, P4] I/2: Tr 1, posto 2, ⪰ 0 (traço 1 não é posto 1 fora de projeções). -/
theorem trace_one_not_rank_one : halfId.trace = 1 ∧ halfId.rank = 2 ∧ halfId.PosSemidef := by
  refine ⟨?_, halfId_rank, ?_⟩
  · rw [halfId, Matrix.trace_smul, Matrix.trace_one, Fintype.card_fin]
    norm_num
  · rw [halfId]
    have h2 : (0 : ℂ) ≤ 2⁻¹ := by
      rw [show (2⁻¹ : ℂ) = ((2⁻¹ : ℝ) : ℂ) by push_cast; rfl]
      exact Complex.zero_le_real.mpr (by norm_num)
    exact Matrix.PosSemidef.one.smul h2

theorem trace_one_not_rank_one' : ¬ ∀ ρ : Matrix (Fin 2) (Fin 2) ℂ, ρ.trace = 1 → ρ.rank = 1 := by
  intro h
  have h1 := h halfId trace_one_not_rank_one.1
  rw [halfId_rank] at h1
  norm_num at h1

/-- [C4 — P3] P = ρ*, ρ = Q₀: Tr(Pρ) = 0 e PρP = 0 (sem peso, a leitura não devolve o posto). -/
theorem reading_needs_weight :
    (rhoStar * Q0).trace = 0 ∧ rhoStar * Q0 * rhoStar = 0
    ∧ ((rhoStar * Q0).trace)⁻¹ • (rhoStar * Q0 * rhoStar) ≠ rhoStar := by
  have h1 : rhoStar * Q0 = 0 := by
    rw [rhoStar_eq, Q0_eq]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]
  refine ⟨by rw [h1, Matrix.trace_zero], by rw [h1, zero_mul], ?_⟩
  rw [h1, zero_mul, smul_zero]
  exact rhoStar_ne_zero.symm

/-- [C5 — P3] P = 1 (posto 2), ρ = I/2: a saída I/2 tem posto 2 (sem posto 1, a leitura não escalariza). -/
theorem reading_needs_rank_one :
    ((1 * halfId).trace)⁻¹ • (1 * halfId * 1) = halfId ∧ halfId.rank = 2
    ∧ (1 : Matrix (Fin 2) (Fin 2) ℂ).rank = 2 := by
  refine ⟨?_, halfId_rank, ?_⟩
  · rw [one_mul, mul_one, trace_one_not_rank_one.1, inv_one, one_smul]
  · rw [Matrix.rank_one, Fintype.card_fin]

/-- C6: diag(2, 1). -/
def C6mat : Matrix (Fin 2) (Fin 2) ℂ := diagonal ![2, 1]

/-- [C6 — B4] A = diag(2, 1) não unitária: Tr(Aρ*Aᴴ) = 4 ≠ 1. -/
theorem nonunitary_changes_trace : (C6mat * rhoStar * C6matᴴ).trace = 4 ∧ C6matᴴ * C6mat ≠ 1 := by
  constructor
  · rw [C6mat, rhoStar_eq, Matrix.trace_fin_two]
    simp [Matrix.mul_apply, Fin.sum_univ_two]
    norm_num
  · intro h
    have h00 := congrFun (congrFun h 0) 0
    simp [C6mat, Matrix.mul_apply, Fin.sum_univ_two] at h00
    norm_num at h00

/-- [C7 — B4] A = Q₀ singular: Aρ*Aᴴ = 0, posto 0. -/
theorem singular_kills_rank : Q0 * rhoStar * Q0ᴴ = 0 ∧ (Q0 * rhoStar * Q0ᴴ).rank = 0 := by
  have h : Q0 * rhoStar * Q0ᴴ = 0 := by
    rw [Q0_eq, rhoStar_eq]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.conjTranspose_apply]
  exact ⟨h, by rw [h, Matrix.rank_zero]⟩

/-- [C8 — B5] θ ∈ {0, π/2}: D_∞ F_θ(1) = F_θ(1), posto 1. -/
theorem endpoint_rank_one_at_poles :
    (diagExpect (rhoOut 0) = rhoOut 0 ∧ (diagExpect (rhoOut 0)).rank = 1)
    ∧ (diagExpect (rhoOut (Real.pi / 2)) = rhoOut (Real.pi / 2)
      ∧ (diagExpect (rhoOut (Real.pi / 2))).rank = 1) := by
  have h0 : Real.sin (2 * 0) = 0 := by simp
  have h1 : Real.sin (2 * (Real.pi / 2)) = 0 := by
    rw [show 2 * (Real.pi / 2) = Real.pi by ring, Real.sin_pi]
  exact ⟨⟨((rhoOut_eq_diag_iff 0).mpr h0).symm, (endpoint_rank_one_iff 0).mpr h0⟩,
    ⟨((rhoOut_eq_diag_iff _).mpr h1).symm, (endpoint_rank_one_iff _).mpr h1⟩⟩

/-- [C9 — B5, B7.b] g = 0: D_t = id e NÃO há convergência a D_∞ (para um estado não diagonal). -/
theorem zero_rate_no_dephasing :
    (∀ (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ), dephase (fun _ _ => (0 : ℝ)) t x = x)
    ∧ ¬ Tendsto (fun t => dephase (fun _ _ => (0 : ℝ)) t (rhoOut (Real.pi / 4))) atTop
        (𝓝 (diagExpect (rhoOut (Real.pi / 4)))) := by
  have hid : ∀ (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ), dephase (fun _ _ => (0 : ℝ)) t x = x := by
    intro t x
    ext i j
    simp [dephase]
  refine ⟨hid, ?_⟩
  intro h
  simp only [hid] at h
  have h2 := tendsto_nhds_unique tendsto_const_nhds h
  have h3 := (rhoOut_eq_diag_iff (Real.pi / 4)).mp h2
  rw [show 2 * (Real.pi / 4) = Real.pi / 2 by ring, Real.sin_pi_div_two] at h3
  norm_num at h3

/-- O leitor |+⟩⟨+|. -/
def plusReader : Matrix (Fin 2) (Fin 2) ℂ := !![2⁻¹, 2⁻¹; 2⁻¹, 2⁻¹]

/-- As taxas unitárias g_ii = 0, g_ij = 1 (sonda das hipóteses de defasagem). -/
def unitRates : Fin 2 → Fin 2 → ℝ := fun i j => if i = j then 0 else 1

/-- [sonda] as taxas unitárias satisfazem as hipóteses de D: g_ii = 0, g₀₁ > 0, g₁₀ > 0. -/
theorem unitRates_spec : (∀ i, unitRates i i = 0) ∧ 0 < unitRates 0 1 ∧ 0 < unitRates 1 0 := by
  refine ⟨fun i => by simp [unitRates], by simp [unitRates], by simp [unitRates]⟩

theorem plus_reader_value (θ t : ℝ) :
    (plusReader * dephase unitRates t (Qtheta θ)).trace
      = 2⁻¹ - (Real.exp (-t) : ℂ) * ((Real.sin θ : ℂ) * (Real.cos θ : ℂ)) := by
  rw [Matrix.trace_fin_two, dephased_Qtheta_eq]
  simp [plusReader, Matrix.mul_apply, Fin.sum_univ_two, unitRates]
  linear_combination (2⁻¹ : ℂ) * Complex.sin_sq_add_cos_sq (θ : ℂ)

/-- [C10 — B6] o leitor NÃO diagonal |+⟩⟨+| vê o tempo em θ_M (γ = 1): o valor em t = 0 difere do valor em t = 1. -/
theorem nondiagonal_reader_sees_time (c : TGLCoupling) :
    (plusReader * dephase unitRates 0 (Qtheta (thetaMiguel c.beta))).trace
      ≠ (plusReader * dephase unitRates 1 (Qtheta (thetaMiguel c.beta))).trace := by
  rw [plus_reader_value, plus_reader_value]
  intro h
  have hsc : (Real.sin (thetaMiguel c.beta) : ℂ) * (Real.cos (thetaMiguel c.beta) : ℂ) ≠ 0 := by
    exact_mod_cast sin_mul_cos_thetaMiguel_ne_zero c
  have hE : (Real.exp (-1) : ℂ) ≠ 1 := by
    intro h1
    have h2 : Real.exp (-1) = 1 := by exact_mod_cast h1
    rw [Real.exp_eq_one_iff] at h2
    norm_num at h2
  have h0 : (Real.exp (-(0 : ℝ)) : ℂ) = 1 := by simp
  rw [h0] at h
  have h2 : (1 - (Real.exp (-1) : ℂ))
      * ((Real.sin (thetaMiguel c.beta) : ℂ) * (Real.cos (thetaMiguel c.beta) : ℂ)) = 0 := by
    linear_combination (-1 : ℂ) * h
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact hE (by linear_combination (-1 : ℂ) * h3)
  · exact hsc h3

/-- [C11 — B7.a2] θ = π: sin²(nπ) = 0 para todo n. -/
theorem angular_leak_zero_at_pi : ∀ k : ℕ, Real.sin (k * Real.pi) ^ 2 = 0 :=
  (angular_leak_zero_converges Real.pi Real.sin_pi).1

/-- [C12 — B9.a] θ = 0: |𝓣|² = 1 e D não atua. -/
theorem transmission_without_dephasing_at_zero (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) :
    Complex.normSq ((Smat 0).mulVec e1 0) = 1 ∧ ¬ dephasingActs g 0 := by
  refine ⟨by rw [normSq_transmission, Real.cos_zero]; norm_num, ?_⟩
  rw [dephasingActs_iff, not_not]
  intro t
  rw [rhoOut_zero]
  exact dephase_rhoStar g hg0 t

/-- [C13 — B9.a'] θ = π/2: |𝓡|² = 1 e D não atua. -/
theorem leak_without_dephasing_at_half_pi (g : Fin 2 → Fin 2 → ℝ) (hg0 : ∀ i, g i i = 0) :
    Complex.normSq ((Smat (Real.pi / 2)).mulVec e1 1) = 1 ∧ ¬ dephasingActs g (Real.pi / 2) := by
  refine ⟨by rw [normSq_reflection, Real.sin_pi_div_two]; norm_num, ?_⟩
  rw [dephasingActs_iff, not_not]
  intro t
  rw [rhoOut_pi_div_two]
  exact dephase_Q0 g hg0 t

/-- [C14 — B2] θ = 0: {Q₀, ρ*} = 0. -/
theorem anticomm_zero_at_zero : anticomm (Qtheta 0) rhoStar = 0 :=
  (anticomm_zero_iff 0).mpr Real.sin_zero

/-! ## 17. SONDAS DE VACUIDADE (hipóteses habitadas; os dois lados de cada ⟺ realizados) -/

/-- [sonda] as hipóteses de estado são habitadas: ρ* e I/2 são ⪰ 0 com traço 1. -/
theorem probe_states : rhoStar.PosSemidef ∧ rhoStar.trace = 1 ∧ halfId.PosSemidef ∧ halfId.trace = 1 := by
  refine ⟨?_, rhoStar_trace, trace_one_not_rank_one.2.2, trace_one_not_rank_one.1⟩
  rw [rhoStar_eq_vecMulVec]
  exact Matrix.posSemidef_vecMulVec_self_star e1

/-- [sonda] e₁ ≠ 0 e ⟨e₁, e₁⟩ = 1 (as hipóteses de P1.d são habitadas). -/
theorem probe_e1 : e1 ≠ 0 ∧ star e1 ⬝ᵥ e1 = 1 := by
  refine ⟨fun h => ?_, ?_⟩
  · have h0 := congrFun h 0
    simp [e1] at h0
  · simp [e1, dotProduct, Fin.sum_univ_two]

/-- [sonda] `TGLCoupling` é habitada (β = 1/2 SÓ para mostrar que 0 < β < 1 é satisfatível; esse 1/2 não substitui
    β, cujo número é do runtime). -/
theorem probe_coupling : ∃ c : TGLCoupling, c.beta = 1 / 2 :=
  ⟨⟨1 / 2, by norm_num, by norm_num⟩, rfl⟩

/-- [sonda] os ângulos das sondas: sin(2·π/4) ≠ 0, sin(2·0) = 0, sin 1 ≠ 0, sin π = 0. -/
theorem probe_angles :
    Real.sin (2 * (Real.pi / 4)) ≠ 0 ∧ Real.sin (2 * 0) = 0 ∧ Real.sin 1 ≠ 0 ∧ Real.sin Real.pi = 0 := by
  refine ⟨?_, by simp, ?_, Real.sin_pi⟩
  · rw [show 2 * (Real.pi / 4) = Real.pi / 2 by ring, Real.sin_pi_div_two]
    norm_num
  · exact (Real.sin_pos_of_pos_of_lt_pi one_pos (by linarith [Real.pi_gt_three])).ne'

/-- [sonda P1.a] os dois lados: ρ* (puro, posto 1, idempotente) e I/2 (não puro, posto 2, não idempotente). -/
theorem probe_pure_both_sides :
    ((rhoStar ^ 2).trace = 1 ∧ rhoStar.rank = 1 ∧ rhoStar ^ 2 = rhoStar)
    ∧ ((halfId ^ 2).trace ≠ 1 ∧ halfId.rank ≠ 1 ∧ halfId ^ 2 ≠ halfId) := by
  have hρ := probe_states
  have hiff1 := pure_iff_rank_one hρ.2.2.1 hρ.2.2.2
  have hiff2 := pure_iff_idempotent hρ.2.2.1 hρ.2.2.2
  have hr : halfId.rank ≠ 1 := by rw [halfId_rank]; norm_num
  refine ⟨⟨?_, rhoStar_rank, ?_⟩, ⟨fun h => hr (hiff1.mp h), hr, fun h => hr (hiff1.mp (hiff2.mpr h))⟩⟩
  · rw [sq, rhoStar_idem, rhoStar_trace]
  · rw [sq, rhoStar_idem]

/-- [sonda P2.b] os dois lados de «posto 1 ⟺ nulidade + 1 = n». -/
theorem probe_rank_nullity_both_sides :
    (rhoStar.rank = 1 ∧ nullity rhoStar + 1 = 2) ∧ (halfId.rank ≠ 1 ∧ nullity halfId + 1 ≠ 2) := by
  refine ⟨⟨rhoStar_rank, by rw [rhoStar_rank_nullity.2]⟩, ⟨by rw [halfId_rank]; norm_num, ?_⟩⟩
  rw [half_identity_rank_nullity.2]
  norm_num

/-- [sonda P4] os dois lados: ρ* (d = 1, o nome encontra o posto) e a projeção 1 em M₂ (d = 2, não encontra). -/
theorem probe_name_rank_both_sides :
    ((((rhoStar.rank : ℂ))⁻¹ • rhoStar) ^ 2).trace = (((rhoStar.rank : ℂ))⁻¹ • rhoStar).trace
    ∧ ((((1 : Matrix (Fin 2) (Fin 2) ℂ).rank : ℂ)⁻¹ • (1 : Matrix (Fin 2) (Fin 2) ℂ)) ^ 2).trace
        ≠ ((((1 : Matrix (Fin 2) (Fin 2) ℂ).rank : ℂ)⁻¹ • (1 : Matrix (Fin 2) (Fin 2) ℂ))).trace := by
  have hr1 : (1 : Matrix (Fin 2) (Fin 2) ℂ).rank = 2 := by rw [Matrix.rank_one, Fintype.card_fin]
  refine ⟨(name_meets_rank_only_at_the_atom rhoStar rhoStar_idem (by rw [rhoStar_rank])).mpr rhoStar_rank,
    fun h => ?_⟩
  have h2 := (name_meets_rank_only_at_the_atom (1 : Matrix (Fin 2) (Fin 2) ℂ) (mul_one 1)
    (by rw [hr1]; norm_num)).mp h
  rw [hr1] at h2
  norm_num at h2

/-- A projeção de posto 2 do pré-registro: diag(1, 1, 0, 0) em M₄(ℂ) (objeto de sonda). -/
def P2diag : Matrix (Fin 4) (Fin 4) ℂ := diagonal ![1, 1, 0, 0]

/-- [sonda P4] diag(1, 1, 0, 0): idempotente, hermitiana, posto 2 — e o lado FALSO de
    `name_meets_rank_only_at_the_atom` (Tr ρ² ≠ Tr ρ em d = 2). -/
theorem probe_rank_two_projection :
    P2diag * P2diag = P2diag ∧ P2diagᴴ = P2diag ∧ P2diag.rank = 2
    ∧ ((((P2diag.rank : ℂ))⁻¹ • P2diag) ^ 2).trace ≠ (((P2diag.rank : ℂ))⁻¹ • P2diag).trace := by
  have hidem : P2diag * P2diag = P2diag := by
    simp only [P2diag, diagonal_mul_diagonal]
    congr 1
    funext i
    fin_cases i <;> simp
  have hrank : P2diag.rank = 2 := by
    have htr : P2diag.trace = 2 := by
      rw [P2diag, trace_diagonal, Fin.sum_univ_four]
      simp
      norm_num
    have h := trace_eq_rank_of_projection P2diag hidem
    rw [htr] at h
    exact_mod_cast h.symm
  refine ⟨hidem, ?_, hrank, fun h => ?_⟩
  · simp only [P2diag, diagonal_conjTranspose]
    congr 1
    funext i
    fin_cases i <;> simp
  · have h2 := (name_meets_rank_only_at_the_atom P2diag hidem (by rw [hrank]; norm_num)).mp h
    rw [hrank] at h2
    norm_num at h2

/-- [sonda B2.a, B6.b, C14] os dois lados de «{·, ρ*} = 0 ⟺ sin θ = 0». -/
theorem probe_anticomm_both_sides :
    anticomm (Qtheta 0) rhoStar = 0 ∧ anticomm (Qtheta (Real.pi / 4)) rhoStar ≠ 0
    ∧ anticomm (dephase unitRates 1 (Qtheta 0)) rhoStar = 0
    ∧ anticomm (dephase unitRates 1 (Qtheta (Real.pi / 4))) rhoStar ≠ 0 := by
  have hs : Real.sin (Real.pi / 4) ≠ 0 := by
    rw [Real.sin_pi_div_four]
    positivity
  exact ⟨anticomm_zero_at_zero, fun h => hs ((anticomm_zero_iff _).mp h),
    (anticomm_dephased_zero_iff 0 unitRates 1).mpr Real.sin_zero,
    fun h => hs ((anticomm_dephased_zero_iff _ unitRates 1).mp h)⟩

/-- [sonda B5.a, B5.c, B8.b, B9.b] os dois lados: θ = π/4 (posto 2, D atua) e θ = 0 (posto 1, D não atua). -/
theorem probe_endpoint_both_sides :
    (diagExpect (rhoOut (Real.pi / 4))).rank = 2 ∧ (diagExpect (rhoOut 0)).rank = 1
    ∧ (dephase unitRates 1 (rhoOut (Real.pi / 4))).rank = 2 ∧ (dephase unitRates 1 (rhoOut 0)).rank = 1
    ∧ dephasingActs unitRates (Real.pi / 4) ∧ ¬ dephasingActs unitRates 0 := by
  obtain ⟨hg0, h01, h10⟩ := unitRates_spec
  have hq : Real.sin (2 * (Real.pi / 4)) ≠ 0 := probe_angles.1
  have hz : Real.sin (2 * 0) = 0 := by simp
  refine ⟨(endpoint_rank_two_iff _).mpr hq, (endpoint_rank_one_iff 0).mpr hz,
    (dephased_rank_two_iff _ unitRates hg0 h01 h10 one_pos).mpr hq, ?_, ?_,
    (transmission_without_dephasing_at_zero unitRates hg0).2⟩
  · have h := (dephasing_trivial_iff 0 unitRates hg0 h01 h10).mpr hz
    rw [h 1]
    exact (fractal_one_is_rank_one 0).1
  · rw [dephasingActs_iff, dephasing_trivial_iff _ unitRates hg0 h01 h10]
    exact hq

/-- [sonda B5.a, pureza] os dois lados de «pureza < 1 ⟺ sin 2θ ≠ 0». -/
theorem probe_purity_both_sides :
    1 - 2 * Real.sin (Real.pi / 4) ^ 2 * Real.cos (Real.pi / 4) ^ 2 < 1
    ∧ ¬ (1 - 2 * Real.sin 0 ^ 2 * Real.cos 0 ^ 2 < 1) := by
  refine ⟨(endpoint_purity _).2.mpr probe_angles.1, ?_⟩
  simp

/-- [sonda B5.b, B8.b] os dois lados: b = 1/2 (posto 2; sin 2θ_M(b) ≠ 0) e b = 0 (posto 1; sin 2θ_M(b) = 0). -/
theorem probe_diag_both_sides :
    (diagonal ![((1 - 1 / 2 : ℝ) : ℂ), ((1 / 2 : ℝ) : ℂ)]).rank = 2
    ∧ (diagonal ![((1 - 0 : ℝ) : ℂ), ((0 : ℝ) : ℂ)]).rank = 1
    ∧ Real.sin (2 * thetaMiguel 0) = 0 ∧ Real.sin (2 * thetaMiguel (1 / 2)) ≠ 0 := by
  refine ⟨(rank_diag_two_iff (1 / 2) (by norm_num) (by norm_num)).mpr ⟨by norm_num, by norm_num⟩,
    rank_diag_one_at_ends 0 (Or.inl rfl),
    (sin_two_thetaMiguel_eq_zero_iff 0 le_rfl zero_le_one).mpr (Or.inl rfl), ?_⟩
  intro h
  rcases (sin_two_thetaMiguel_eq_zero_iff (1 / 2) (by norm_num) (by norm_num)).mp h with h2 | h2 <;>
    norm_num at h2

/-- [sonda B7.a2] θ = 1 (sin 1 ≠ 0: sem limite) e θ = π (converge). -/
theorem probe_angular_both_sides :
    (¬ ∃ L : ℝ, Tendsto (fun k : ℕ => Real.sin (k * 1) ^ 2) atTop (𝓝 L))
    ∧ Tendsto (fun k : ℕ => Real.sin (k * Real.pi) ^ 2) atTop (𝓝 0) :=
  ⟨angular_leak_no_limit 1 probe_angles.2.2.1, (angular_leak_zero_converges Real.pi Real.sin_pi).2⟩

/-- [sonda P1.b] os dois lados em M₂ sem positividade: ρ* (Tr² = 1, posto 1) e I/2 (Tr² ≠ 1, posto ≠ 1). -/
theorem probe_fin_two_both_sides :
    ((rhoStar ^ 2).trace = 1 ∧ rhoStar.rank = 1) ∧ ((halfId ^ 2).trace ≠ 1 ∧ halfId.rank ≠ 1) := by
  have h1 := pure_iff_rank_one_fin_two rhoStar rhoStar_trace
  have h2 := pure_iff_rank_one_fin_two halfId trace_one_not_rank_one.1
  have hr : halfId.rank ≠ 1 := by rw [halfId_rank]; norm_num
  exact ⟨⟨h1.mpr rhoStar_rank, rhoStar_rank⟩, ⟨fun h => hr (h2.mp h), hr⟩⟩

end

end TGLExt.TheUnitIsTheRank
