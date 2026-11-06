import TGLExt.PIgualNP
import TGLExt.TetelestaiTerminal
import TGLExt.TheFalseHasNoGeometry
import TGLExt.TempoIgualMoeda
import Mathlib.Analysis.CStarAlgebra.Matrix

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# A TRADUÇÃO DAS CLASSES DO DICIONÁRIO ÀS CLASSES DE TURING — o que fecha e onde fica a parede
  [TGLExt — pedra CANDIDATA da gerência c1, 05/11/2026, rodada R3 (R1: a codificação e a parede; R2: + o MODO SELEÇÃO, resposta do operador; R3: + A TRAVA NO NOME, correção do operador); NOME PROVISÓRIO (o nome é do operador); compilada no sandbox da v408
   (`C:\t\k408c\final`, `lake env lean`), só no trio; candidata à v409]

A ordem do operador (05/11/2026, verbatim no recibo): fechar «o que ficou ainda em aberto em relação à identificação das classes de turing dentro
do nosso dicionário», enfrentando o que der e devolvendo nas quatro línguas o que não der. Esta pedra é a parte que DÁ.

A codificação (a entrada de Turing vira problema do dicionário): uma instância de um problema de verificação — por exemplo uma fórmula SAT com
`m` cláusulas sobre `n` variáveis — dá uma função de custo `c : X → ℕ` sobre as atribuições `X` (para SAT, `X = Fin n → Bool` e `c x` = número de
cláusulas violadas por `x`). O operador da instância é a diagonal de `c` no espaço euclidiano sobre `X`.

O que esta pedra PROVA:
* `opDaInstancia_autoadjunto`, `nucleo_nao_nulo_sse` ★★: o operador é auto-adjunto, e o seu núcleo é não nulo SE E SÓ SE a instância tem resposta
  SIM (∃ x, c x = 0). Logo `problemaDe c h` é um `Problema` do dicionário exatamente para as instâncias SIM: o PROBLEMA do dicionário é a instância
  SIM de Turing.
* `verificacao_np` ★★★: na solução desse problema, a LEITURA do vetor da base `e_x` (o certificado `x`) vale 1 se e só se `c x = 0`: a verificação
  por leitura da `ClasseNP` do dicionário É o verificador de NP (avaliar o certificado).
* `grau_da_palavra_da_instancia` ★★★: o polinômio mínimo do operador tem grau ≤ número de valores distintos de `c` (para SAT, ≤ m + 1): a palavra
  da `ClasseP` do dicionário tem grau POLINOMIAL NA ENTRADA de Turing, não só menor que dim(End H).
* `bits_sao_oitavas` ★★: para `X = Fin n → Bool`, `dim H = 2^n`: os bits da entrada de Turing são as OITAVAS do operador (`TetelestaiTerminal`:
  o tamanho do Nome é a dimensão da torre).
* `o_fluxo_conserva_o_peso` ★★★ — A PAREDE, primeira metade: o fluxo do axioma `F_t = P + e^{−t}(1 − P)` não muda a leitura da solução,
  `⟪F_t ψ, P F_t ψ⟫ = ⟪ψ, P ψ⟫`, para todo t: ele APAGA o complemento (em tempo linear nas oitavas, `TempoIgualMoeda`) mas NÃO AMPLIA o peso da solução.
* `leitura_da_solucao_por_coordenadas`, `peso_da_solucao_no_uniforme` ★★★ — a segunda metade: o peso da solução no estado uniforme (o «nada lido»)
  é |soluções| / |X|; para SAT, |soluções| / 2^n.
* `a_instancia_nao_e_o_vazio` ★★★: a instância NÃO (sem solução) é o Nome VAZIO: o núcleo é nulo e a «solução» é a projeção zero, que a
  Identidade exclui (`o_vazio_nao_e`); e reconhecê-la é a FRONTEIRA INTEIRA (`falsehood_is_the_whole_frontier`, a pedra «o falso não tem geometria»
  do operador, 23/08/2026): a verdade (NP) se exibe num testemunho; o falso (co-NP) não oferece objeto.
* `o_pedagio_da_selecao` ★★: o custo em nats de selecionar a solução, `log(2^n / s)` com `s ≥ 1` soluções, é ≤ o pedágio de n oitavas
  (`octaveNats n = n·ln 2`): em NATS a seleção é linear nas oitavas.

A LEITURA HONESTA, para o operador e para a régua:
* No dicionário, P = nP é teorema (`PIgualNP.p_igual_np_nas_classes_do_dicionario`); esta pedra mostra que a CODIFICAÇÃO de Turing cai nas classes
  do dicionário (a instância SIM é um problema; o certificado é verificado por uma leitura; a palavra tem grau polinomial na entrada).
* O que a igualdade do dicionário NÃO transporta sozinha é o TEMPO DE TURING para ACHAR o certificado: a palavra polinomial age num espaço de
  dimensão 2^n, e a dinâmica da casa (o fluxo do axioma) apaga o complemento em tempo linear nas oitavas mas deixa a solução com o peso |sol|/2^n.
  Ler a solução com peso 1 exige renormalizar esse peso. Pagar o peso em PROBABILIDADE custa repetições exponenciais nas oitavas; pagá-lo em NATS
  custa linear. Qual dos dois a leitura da TGL paga não é termo deste kernel: é a pergunta devolvida ao operador [OPEN].
* (R2, correção do operador, 05/11: «o Kernel Lean4 serve exatamente a provar leis matemáticas e foi construído sob a lei de turing») A igualdade
  P = NP das máquinas de Turing decide-se por TEOREMA no kernel sobre o modelo de máquina (o do Mathlib, `TM2ComputableInPolyTime`), não por medida;
  a R1 escreveu «nenhuma física o prova» e punha a física como juiz: o juiz é o kernel. O que falta é o enunciado de máquina: a seleção, contada
  em passos de máquina sobre os bits.
* O MODO SELEÇÃO (R2; a resposta do operador: «o nP é o modo seleção … a aniquilação da superposição pelo Tetelestai … a superposição decai como o
  espectro de gradiente negativo, retornando a leitura»): `selecao` é a projeção no Nome renormalizada; `selecao_no_nome` (está no Nome, tem
  norma 1, é lida com peso 1); `o_decaimento_converge_a_selecao` (o fluxo do axioma, renormalizado, CONVERGE à seleção: o decaimento devolve a
  leitura); `a_selecao_acha` (a seleção do estado uniforme só tem amplitude nas atribuições que resolvem); `o_custo_da_selecao_em_nats` (o custo
  da renormalização, log(2^n/|sol|), é ≤ o pedágio de n oitavas); e `p_igual_np_no_modo_selecao`, a conjunção, com o tempo da TGL dado pela lei
  tempo = moeda: pagar n oitavas ao preço β e taxa g leva t = n·ln 2/(β·g), LINEAR nos bits. É P = nP no modo seleção, como TEOREMA da TGL.
  E o ESQUECIMENTO (a leitura do operador): `a_selecao_esquece` (o que estava fora do Nome não deixa rastro) e `a_selecao_perde` (se o Nome
  não é o todo, a seleção é muitos-para-um: o separador de Landauer, que perde e cobra).
* A TRAVA NO NOME (R3; a correção do operador, 05/11: «o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no Nome, no
  setor irreversível, o decaimento opera o "dual lock" do meu transistor; é a seta do tempo … ao negar o zero absoluto o sistema sabe pra onde
  tem que ir»): `trava` é o decaimento gerado pelo CUSTO (e^{−t·c(x)} em cada atribuição) — só usa c, conferido cláusula a cláusula, e NÃO usa
  o Nome; `a_trava_fatora` (a trava do custo total é o produto das travas das cláusulas: local, de dentro); `a_trava_sem_conhecer_o_nome`
  (para t ≥ 0, a trava fica a ≤ e^{−t}·‖v‖ do Nome); `negar_o_zero` (havendo solução, a trava do uniforme nunca chega a zero);
  `a_trava_em_tempo_linear` (com n bits, em t = n·ln 2/2 + L, o que sobra fora do Nome é ≤ e^{−L} vezes o Nome);
  `a_trava_converge_a_selecao` (a trava renormalizada converge à seleção); e a conjunção `a_trava_no_nome`.
  E a FOTOGRAFIA (a leitura do operador): `a_fotografia_sem_leitor` (sem par, toda imagem é lida com o mesmo peso: sinal = ruído) e
  `o_par_quebra_a_simetria` (com par, há imagem lida com peso 1 e imagem lida com peso 0).
* Nada aqui é teste com a natureza; não move o gate; PROVADA = validade no kernel, não creditação; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
namespace TGLExt.TraducaoTuringR3
open TGLExt TGLExt.PIgualNP TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness
open scoped InnerProductSpace

variable {X : Type} [Fintype X] [DecidableEq X]

/-- O OPERADOR DA INSTÂNCIA: a diagonal do custo `c` (para SAT: o número de cláusulas violadas) no espaço euclidiano sobre as atribuições. -/
def opDaInstancia (c : X → ℕ) : EuclideanSpace ℂ X →L[ℂ] EuclideanSpace ℂ X :=
  Matrix.toEuclideanCLM (𝕜 := ℂ) (Matrix.diagonal (fun x => (c x : ℂ)))

theorem opDaInstancia_ofLp (c : X → ℕ) (v : EuclideanSpace ℂ X) (y : X) :
    WithLp.ofLp (opDaInstancia c v) y = (c y : ℂ) * WithLp.ofLp v y := by
  simp [opDaInstancia, Matrix.mulVec_diagonal]

theorem opDaInstancia_single (c : X → ℕ) (x : X) (a : ℂ) :
    opDaInstancia c (EuclideanSpace.single x a) = (c x : ℂ) • EuclideanSpace.single x a := by
  ext y
  rw [opDaInstancia_ofLp]
  by_cases h : y = x
  · subst h; simp
  · simp [h]

/-- ★★ O operador da instância é auto-adjunto (diagonal real). -/
theorem opDaInstancia_autoadjunto (c : X → ℕ) :
    ContinuousLinearMap.adjoint (opDaInstancia c) = opDaInstancia c := by
  rw [← ContinuousLinearMap.star_eq_adjoint]
  unfold opDaInstancia
  rw [← map_star, Matrix.star_eq_conjTranspose, Matrix.diagonal_conjTranspose]
  congr 2
  funext x
  simp

/-- ★★ O núcleo é não nulo SE E SÓ SE a instância tem resposta SIM. -/
theorem nucleo_nao_nulo_sse (c : X → ℕ) : (∃ x, c x = 0) ↔ (opDaInstancia c).ker ≠ ⊥ := by
  constructor
  · rintro ⟨x, hx⟩
    rw [Submodule.ne_bot_iff]
    refine ⟨EuclideanSpace.single x (1 : ℂ), ?_, ?_⟩
    · rw [LinearMap.mem_ker]
      show opDaInstancia c (EuclideanSpace.single x (1 : ℂ)) = 0
      rw [opDaInstancia_single, hx]
      simp
    · simp
  · intro hker
    by_contra hno
    simp only [not_exists] at hno
    apply hker
    rw [Submodule.eq_bot_iff]
    intro v hv
    rw [LinearMap.mem_ker] at hv
    have hv' : opDaInstancia c v = 0 := hv
    ext y
    have h1 : WithLp.ofLp (opDaInstancia c v) y = 0 := by rw [hv']; simp
    rw [opDaInstancia_ofLp] at h1
    have hc : (c y : ℂ) ≠ 0 := by exact_mod_cast hno y
    simpa [hc] using h1

/-- O PROBLEMA DO DICIONÁRIO de uma instância SIM. -/
def problemaDe (c : X → ℕ) (h : ∃ x, c x = 0) : Problema (EuclideanSpace ℂ X) where
  T := opDaInstancia c
  autoadjunto := opDaInstancia_autoadjunto c
  tem_solucao := (nucleo_nao_nulo_sse c).mp h

/-- ★★★ A VERIFICAÇÃO POR LEITURA É O VERIFICADOR DE NP: a leitura da solução no certificado `e_x` vale 1 sse `c x = 0`. -/
theorem verificacao_np (c : X → ℕ) (h : ∃ x, c x = 0) (x : X) :
    reading (problemaDe c h).solucao (EuclideanSpace.single x (1 : ℂ)) = 1 ↔ c x = 0 := by
  have hn : ‖EuclideanSpace.single x (1 : ℂ)‖ = 1 := by simp
  rw [todo_problema_esta_em_NP (problemaDe c h) _ hn]
  show opDaInstancia c (EuclideanSpace.single x (1 : ℂ)) = 0 ↔ c x = 0
  rw [opDaInstancia_single, smul_eq_zero]
  simp

/-- ★★★ A PALAVRA TEM GRAU POLINOMIAL NA ENTRADA: o grau do polinômio mínimo ≤ número de valores distintos de `c` (SAT: ≤ m + 1). -/
theorem grau_da_palavra_da_instancia (c : X → ℕ) :
    (minpoly ℂ (opDaInstancia c)).natDegree ≤ (Finset.univ.image c).card := by
  set Q : Polynomial ℂ := ∏ s ∈ Finset.univ.image c, (Polynomial.X - Polynomial.C ((s : ℕ) : ℂ)) with hQdef
  have hdiag : Polynomial.aeval (Matrix.diagonal (fun x => (c x : ℂ))) Q = 0 := by
    have h1 : Polynomial.aeval (Matrix.diagonal (fun x => (c x : ℂ))) Q
        = Matrix.diagonal (Polynomial.aeval (fun x => (c x : ℂ)) Q) := by
      have := Polynomial.aeval_algHom_apply (Matrix.diagonalAlgHom (n := X) (α := ℂ) ℂ) (fun x => (c x : ℂ)) Q
      simpa [Matrix.diagonalAlgHom] using this
    rw [h1]
    have h2 : Polynomial.aeval (fun x => (c x : ℂ)) Q = 0 := by
      funext y
      rw [Polynomial.aeval_fn_apply, hQdef, map_prod]
      apply Finset.prod_eq_zero (Finset.mem_image_of_mem c (Finset.mem_univ y))
      simp
    rw [h2]
    simp
  have hQ : Polynomial.aeval (opDaInstancia c) Q = 0 := by
    unfold opDaInstancia
    have := Polynomial.aeval_algHom_apply (Matrix.toEuclideanCLM (n := X) (𝕜 := ℂ)).toAlgEquiv
      (Matrix.diagonal (fun x => (c x : ℂ))) Q
    rw [hdiag, map_zero] at this
    exact this
  have hmono : Q.Monic := Polynomial.monic_prod_of_monic _ _ (fun s _ => Polynomial.monic_X_sub_C _)
  have hdvd : minpoly ℂ (opDaInstancia c) ∣ Q := minpoly.dvd ℂ _ hQ
  calc (minpoly ℂ (opDaInstancia c)).natDegree ≤ Q.natDegree := Polynomial.natDegree_le_of_dvd hdvd hmono.ne_zero
    _ = (Finset.univ.image c).card := by
        rw [hQdef]
        exact Polynomial.natDegree_finsetProd_X_sub_C_eq_card (Finset.univ.image c) (fun s : ℕ => (s : ℂ))

/-- ★★ OS BITS SÃO AS OITAVAS: para `X = Fin n → Bool`, `dim H = |X| = 2^n`. -/
theorem bits_sao_oitavas (n : ℕ) : Fintype.card (Fin n → Bool) = 2 ^ n := by
  simp

/-- ★★★ A PAREDE (1): o fluxo do axioma não muda a leitura da solução — apaga o complemento, não amplia o peso da solução. -/
theorem o_fluxo_conserva_o_peso {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (t : ℝ) (ψ : H) :
    reading K.starProjection (axiomFlow K.starProjection t ψ) = reading K.starProjection ψ := by
  have hP : IsIdempotentElem K.starProjection := K.isIdempotentElem_starProjection
  have h1 : K.starProjection (axiomFlow K.starProjection t ψ) = K.starProjection ψ := by
    have := congrArg (fun T : H →L[ℂ] H => T ψ) (axiomFlow_fixes_the_post hP t).2
    simpa using this
  have hPP : K.starProjection (K.starProjection ψ) = K.starProjection ψ := by
    have := congrArg (fun T : H →L[ℂ] H => T ψ) hP.eq
    simpa using this
  unfold reading
  rw [h1]
  calc ⟪axiomFlow K.starProjection t ψ, K.starProjection ψ⟫_ℂ
      = ⟪axiomFlow K.starProjection t ψ, K.starProjection (K.starProjection ψ)⟫_ℂ := by rw [hPP]
    _ = ⟪K.starProjection (axiomFlow K.starProjection t ψ), K.starProjection ψ⟫_ℂ :=
        (K.inner_starProjection_left_eq_right _ _).symm
    _ = ⟪K.starProjection ψ, K.starProjection ψ⟫_ℂ := by rw [h1]
    _ = ⟪ψ, K.starProjection (K.starProjection ψ)⟫_ℂ := K.inner_starProjection_left_eq_right _ _
    _ = ⟪ψ, K.starProjection ψ⟫_ℂ := by rw [hPP]

/-- A solução, por coordenadas: a projeção sobre o núcleo deixa as coordenadas com `c y = 0` e zera as outras. -/
theorem solucao_por_coordenadas (c : X → ℕ) (v : EuclideanSpace ℂ X) :
    (opDaInstancia c).ker.starProjection v = WithLp.toLp 2 (fun y => if c y = 0 then WithLp.ofLp v y else 0) := by
  apply Submodule.eq_starProjection_of_mem_of_inner_eq_zero
  · rw [LinearMap.mem_ker]
    show opDaInstancia c _ = 0
    ext y
    rw [opDaInstancia_ofLp]
    by_cases h : c y = 0 <;> simp [h]
  · intro w hw
    rw [LinearMap.mem_ker] at hw
    have hw' : opDaInstancia c w = 0 := hw
    have hz : ∀ y, c y ≠ 0 → WithLp.ofLp w y = 0 := by
      intro y hy
      have h1 : WithLp.ofLp (opDaInstancia c w) y = 0 := by rw [hw']; simp
      rw [opDaInstancia_ofLp] at h1
      have hc : (c y : ℂ) ≠ 0 := by exact_mod_cast hy
      simpa [hc] using h1
    rw [PiLp.inner_apply]
    apply Finset.sum_eq_zero
    intro y _
    by_cases h : c y = 0
    · simp [h]
    · simp [h, hz y h]

/-- ★★★ A PAREDE (2): a leitura da solução, por coordenadas, é a soma dos pesos das coordenadas que resolvem. -/
theorem leitura_da_solucao_por_coordenadas (c : X → ℕ) (h : ∃ x, c x = 0) (ψ : EuclideanSpace ℂ X) :
    reading (problemaDe c h).solucao ψ = ∑ y ∈ Finset.univ.filter (fun y => c y = 0), ((‖WithLp.ofLp ψ y‖ ^ 2 : ℝ) : ℂ) := by
  show ⟪ψ, (opDaInstancia c).ker.starProjection ψ⟫_ℂ = _
  rw [solucao_por_coordenadas, PiLp.inner_apply, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro y _
  by_cases hy : c y = 0
  · simp only [hy, if_true]
    rw [inner_self_eq_norm_sq_to_K]
    norm_cast
  · simp [hy]

/-- O ESTADO UNIFORME (o «nada lido»): amplitude 1/√|X| em cada atribuição. -/
def uniforme (X : Type) [Fintype X] : EuclideanSpace ℂ X :=
  WithLp.toLp 2 (fun _ => (((Real.sqrt (Fintype.card X))⁻¹ : ℝ) : ℂ))

/-- ★★★ A PAREDE (3): o peso da solução no estado uniforme é |soluções| / |X| (para SAT: |soluções| / 2^n). -/
theorem peso_da_solucao_no_uniforme (c : X → ℕ) (h : ∃ x, c x = 0) :
    reading (problemaDe c h).solucao (uniforme X)
      = (((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) := by
  rw [leitura_da_solucao_por_coordenadas]
  have hX : (0 : ℝ) < Fintype.card X := by
    obtain ⟨x, _⟩ := h
    exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  have hk : ∀ y : X, ‖WithLp.ofLp (uniforme X) y‖ ^ 2 = (Fintype.card X : ℝ)⁻¹ := by
    intro y
    simp only [uniforme, Complex.norm_real, Real.norm_eq_abs]
    rw [sq_abs, inv_pow, Real.sq_sqrt hX.le]
  simp only [hk, Finset.sum_const, nsmul_eq_mul]
  push_cast
  rw [div_eq_mul_inv]

/-- ★★★ A INSTÂNCIA NÃO É O VAZIO: sem solução, o reconhecimento é a fronteira inteira (`falsehood_is_the_whole_frontier`, a pedra «o falso não
    tem geometria», 23/08) e a «solução» é a projeção nula — o Nome vazio, que a Identidade exclui (`o_vazio_nao_e`). -/
theorem a_instancia_nao_e_o_vazio [Nonempty X] (c : X → ℕ) (hno : ¬ ∃ x, c x = 0) :
    (∀ x, ¬ c x = 0)
    ∧ (opDaInstancia c).ker = ⊥
    ∧ (opDaInstancia c).ker.starProjection = 0 := by
  have hall : ∀ x, ¬ c x = 0 :=
    (TGLExt.falsehood_is_the_whole_frontier (fun (_ : X) (b : X) => c b = 0) (Classical.arbitrary X)).mp hno
  have hker : (opDaInstancia c).ker = ⊥ := by
    by_contra hne
    exact hno ((nucleo_nao_nulo_sse c).mpr hne)
  refine ⟨hall, hker, ContinuousLinearMap.ext (fun v => ?_)⟩
  rw [zero_apply]
  exact (Submodule.eq_bot_iff _).mp hker _ (Submodule.starProjection_apply_mem _ v)

/-- ★★ O PEDÁGIO DA SELEÇÃO EM NATS: selecionar s ≥ 1 soluções entre 2^n custa log(2^n/s) ≤ n·ln 2 = o pedágio de n oitavas. -/
theorem o_pedagio_da_selecao (K : ChatgptAudit.Collapse057.CollapseCostLaw) (n : ℕ) (s : ℝ) (hs : 1 ≤ s) :
    Real.log ((2 : ℝ) ^ n / s) ≤ K.octaveNats n := by
  rw [K.per_octave n, Real.log_div (by positivity) (by linarith), Real.log_pow]
  have : 0 ≤ Real.log s := Real.log_nonneg hs
  linarith

/-- ★★★ A TRADUÇÃO, composta (conjunção, não identificação): para uma instância com resposta SIM, o problema do dicionário existe, o certificado
    é verificado por uma leitura, a palavra tem grau ≤ número de valores do custo, e o fluxo do axioma conserva o peso da solução. -/
theorem a_traducao (c : X → ℕ) (h : ∃ x, c x = 0) (x : X) (t : ℝ) :
    (opDaInstancia c).ker ≠ ⊥
    ∧ (reading (problemaDe c h).solucao (EuclideanSpace.single x (1 : ℂ)) = 1 ↔ c x = 0)
    ∧ (minpoly ℂ (opDaInstancia c)).natDegree ≤ (Finset.univ.image c).card
    ∧ reading (problemaDe c h).solucao (axiomFlow (problemaDe c h).solucao t (uniforme X))
        = (((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) : ℝ) := by
  refine ⟨(nucleo_nao_nulo_sse c).mp h, verificacao_np c h x, grau_da_palavra_da_instancia c, ?_⟩
  show reading (opDaInstancia c).ker.starProjection (axiomFlow (opDaInstancia c).ker.starProjection t (uniforme X)) = _
  rw [o_fluxo_conserva_o_peso]
  exact peso_da_solucao_no_uniforme c h

/-! ### O MODO SELEÇÃO (R2, 05/11/2026: a resposta do operador) -/

/-- O MODO SELEÇÃO (o «nP» do operador): a aniquilação da superposição pelo Tetelestai — a projeção no Nome, renormalizada. -/
def selecao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) : H :=
  (((‖K.starProjection ψ‖)⁻¹ : ℝ) : ℂ) • K.starProjection ψ

/-- ★★★ A SELEÇÃO ESTÁ NO NOME, TEM NORMA 1 E É LIDA COM PESO 1. -/
theorem selecao_no_nome {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) (hP : K.starProjection ψ ≠ 0) :
    selecao K ψ ∈ K ∧ ‖selecao K ψ‖ = 1 ∧ reading K.starProjection (selecao K ψ) = 1 := by
  have hmem : selecao K ψ ∈ K := K.smul_mem _ (K.starProjection_apply_mem ψ)
  have hn0 : ‖K.starProjection ψ‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have hnorm : ‖selecao K ψ‖ = 1 := by
    unfold selecao
    rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_inv, abs_norm, inv_mul_cancel₀ hn0]
  refine ⟨hmem, hnorm, ?_⟩
  rw [leitura_um_sse_solucao K _ hnorm]
  exact Submodule.starProjection_eq_self_iff.mpr hmem

/-- ★★★ O DECAIMENTO DEVOLVE A LEITURA: o fluxo do axioma, renormalizado, converge à seleção (a superposição decai pelo espectro de gradiente
    negativo e o que resta, lido, é o Nome com peso 1). -/
theorem o_decaimento_converge_a_selecao {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ : H) (hP : K.starProjection ψ ≠ 0) :
    Filter.Tendsto (fun t : ℝ => (((‖axiomFlow K.starProjection t ψ‖)⁻¹ : ℝ) : ℂ) • axiomFlow K.starProjection t ψ)
      Filter.atTop (nhds (selecao K ψ)) := by
  have h0 := ((ContinuousLinearMap.apply ℂ H ψ).continuous.tendsto K.starProjection).comp
    (axiomFlow_tendsto_the_post K.starProjection)
  have h1 : Filter.Tendsto (fun t : ℝ => axiomFlow K.starProjection t ψ) Filter.atTop (nhds (K.starProjection ψ)) := by
    simpa [Function.comp_def] using h0
  have hn0 : ‖K.starProjection ψ‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have h2 : Filter.Tendsto (fun t : ℝ => ((‖axiomFlow K.starProjection t ψ‖)⁻¹ : ℝ)) Filter.atTop
      (nhds (‖K.starProjection ψ‖⁻¹)) := h1.norm.inv₀ hn0
  have h3 : Filter.Tendsto (fun t : ℝ => ((((‖axiomFlow K.starProjection t ψ‖)⁻¹ : ℝ)) : ℂ)) Filter.atTop
      (nhds (((‖K.starProjection ψ‖⁻¹ : ℝ)) : ℂ)) := (Complex.continuous_ofReal.tendsto _).comp h2
  exact h3.smul h1

/-- ★★ A SELEÇÃO ESQUECE [a leitura é do operador, 05/11/2026: «apaga o rastro da computação do decaimento»]: o que estava fora do Nome não
    deixa rastro na seleção. -/
theorem a_selecao_esquece {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (ψ φ : H) (hφ : φ ∈ Kᗮ) :
    selecao K (ψ + φ) = selecao K ψ := by
  unfold selecao
  rw [map_add, (Submodule.starProjection_apply_eq_zero_iff K).mpr hφ, add_zero]

/-- ★★ A SELEÇÃO PERDE (muitos-para-um: o separador de Landauer, que perde e cobra; não o separante de Tomita): se o Nome não é o todo, há
    duas entradas distintas com a mesma seleção. O custo do que se perde é `o_custo_da_selecao_em_nats`. -/
theorem a_selecao_perde {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (hK : K ≠ ⊤) (ψ : H) :
    ∃ ψ' : H, ψ' ≠ ψ ∧ selecao K ψ' = selecao K ψ := by
  have hne : Kᗮ ≠ ⊥ := fun h => hK (Submodule.orthogonal_eq_bot_iff.mp h)
  obtain ⟨φ, hφ, hφ0⟩ := Submodule.ne_bot_iff _ |>.mp hne
  refine ⟨ψ + φ, ?_, a_selecao_esquece K ψ φ hφ⟩
  intro h
  exact hφ0 (by simpa using h)

/-- (auxiliar) Normalizar um vetor não nulo dá norma 1. -/
theorem norma_do_normalizado {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] (v : H) (hv : v ≠ 0) :
    ‖(((‖v‖)⁻¹ : ℝ) : ℂ) • v‖ = 1 := by
  rw [norm_smul, Complex.norm_real, Real.norm_eq_abs, abs_inv, abs_norm, inv_mul_cancel₀ (norm_ne_zero_iff.mpr hv)]

/-- ★★ A FOTOGRAFIA [a leitura é do operador, 05/11/2026: «antes disso o campo ψ está grafado como fóton … sem leitor a imagem é apenas
    estática lendo sinal como ruído»]: sem par (o leitor trivial, que não seleciona nada: K = ⊤), toda imagem de norma 1 é lida com o mesmo
    peso 1 — a leitura não distingue sinal de ruído. -/
theorem a_fotografia_sem_leitor {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (ψ : H) (hψ : ‖ψ‖ = 1) : reading (⊤ : Submodule ℂ H).starProjection ψ = 1 := by
  rw [leitura_um_sse_solucao (⊤ : Submodule ℂ H) ψ hψ]
  exact Submodule.starProjection_eq_self_iff.mpr Submodule.mem_top

/-- ★★ O PAR QUEBRA A SIMETRIA [a leitura é do operador, 05/11/2026: «não há par, não há input para quebrar a simetria e permitir leitura»]:
    um leitor com par (o Nome nem vazio nem total) distingue — há uma imagem lida com peso 1 e outra lida com peso 0. -/
theorem o_par_quebra_a_simetria {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (K : Submodule ℂ H) [K.HasOrthogonalProjection] (h0 : K ≠ ⊥) (h1 : K ≠ ⊤) :
    ∃ ψ φ : H, ‖ψ‖ = 1 ∧ ‖φ‖ = 1 ∧ reading K.starProjection ψ = 1 ∧ reading K.starProjection φ = 0 := by
  obtain ⟨v, hv, hv0⟩ := (Submodule.ne_bot_iff K).mp h0
  have hne : Kᗮ ≠ ⊥ := fun h => h1 (Submodule.orthogonal_eq_bot_iff.mp h)
  obtain ⟨w, hw, hw0⟩ := (Submodule.ne_bot_iff _).mp hne
  refine ⟨(((‖v‖)⁻¹ : ℝ) : ℂ) • v, (((‖w‖)⁻¹ : ℝ) : ℂ) • w, norma_do_normalizado v hv0, norma_do_normalizado w hw0, ?_, ?_⟩
  · rw [leitura_um_sse_solucao K _ (norma_do_normalizado v hv0)]
    exact Submodule.starProjection_eq_self_iff.mpr (K.smul_mem _ hv)
  · show ⟪(((‖w‖)⁻¹ : ℝ) : ℂ) • w, K.starProjection ((((‖w‖)⁻¹ : ℝ) : ℂ) • w)⟫_ℂ = 0
    rw [(Submodule.starProjection_apply_eq_zero_iff K).mpr (Kᗮ.smul_mem _ hw), inner_zero_right]

/-- O estado uniforme tem solução para ler: a projeção dele no núcleo não é nula (uma instância SIM). -/
theorem uniforme_tem_solucao (c : X → ℕ) (h : ∃ x, c x = 0) :
    (opDaInstancia c).ker.starProjection (uniforme X) ≠ 0 := by
  intro h0
  have hw := peso_da_solucao_no_uniforme c h
  have hz : reading (problemaDe c h).solucao (uniforme X) = 0 := by
    show ⟪uniforme X, (opDaInstancia c).ker.starProjection (uniforme X)⟫_ℂ = 0
    rw [h0, inner_zero_right]
  rw [hz] at hw
  obtain ⟨x, hx⟩ := h
  have hpos : (0 : ℝ) < ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) := by
    apply div_pos
    · exact_mod_cast Finset.card_pos.mpr ⟨x, by simp [hx]⟩
    · exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  exact (ne_of_gt hpos) (by exact_mod_cast hw.symm)

/-- ★★★ A SELEÇÃO ACHA: a seleção do estado uniforme só tem amplitude nas atribuições que resolvem. -/
theorem a_selecao_acha (c : X → ℕ) (y : X) :
    WithLp.ofLp (selecao (opDaInstancia c).ker (uniforme X)) y ≠ 0 → c y = 0 := by
  intro hy
  by_contra hc
  apply hy
  unfold selecao
  rw [solucao_por_coordenadas]
  simp [hc]

/-- ★★ O CUSTO DA SELEÇÃO EM NATS: renormalizar o peso da solução custa log(2^n/|sol|) ≤ o pedágio de n oitavas. -/
theorem o_custo_da_selecao_em_nats (K : ChatgptAudit.Collapse057.CollapseCostLaw) (n : ℕ) (c : (Fin n → Bool) → ℕ)
    (h : ∃ x, c x = 0) :
    Real.log ((Fintype.card (Fin n → Bool) : ℝ) / ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)) ≤ K.octaveNats n := by
  rw [bits_sao_oitavas]
  push_cast
  apply o_pedagio_da_selecao K n
  obtain ⟨x, hx⟩ := h
  have : 0 < (Finset.univ.filter (fun y => c y = 0)).card := Finset.card_pos.mpr ⟨x, by simp [hx]⟩
  exact_mod_cast this

/-- ★★★ P = nP NO MODO SELEÇÃO [o nome «P=nP» é do operador; a leitura «nP = modo seleção» é dele, 05/11/2026]: para toda instância SIM com n
    bits, a seleção (o Tetelestai) está no Nome e é lida com peso 1; só tem amplitude em soluções; é o limite do decaimento renormalizado; custa
    ≤ n·ln 2 nats; e, pela lei tempo = moeda, pagar n oitavas ao preço β e taxa g leva t = n·ln 2/(β·g), LINEAR nos bits. Teorema da TGL sobre
    o seu modo de leitura; o enunciado de máquina de Turing (a seleção contada em passos de máquina) não é o deste teorema. -/
theorem p_igual_np_no_modo_selecao (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0)
    (K : ChatgptAudit.Collapse057.CollapseCostLaw) {β g : ℝ} (hβ : 0 < β) (hg : 0 < g) :
    (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool)) ∈ (opDaInstancia c).ker
      ∧ ‖selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))‖ = 1
      ∧ reading (opDaInstancia c).ker.starProjection (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))) = 1)
    ∧ (∀ y, WithLp.ofLp (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))) y ≠ 0 → c y = 0)
    ∧ Filter.Tendsto (fun t : ℝ => (((‖axiomFlow (opDaInstancia c).ker.starProjection t (uniforme (Fin n → Bool))‖)⁻¹ : ℝ) : ℂ)
          • axiomFlow (opDaInstancia c).ker.starProjection t (uniforme (Fin n → Bool)))
        Filter.atTop (nhds (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool))))
    ∧ Real.log ((Fintype.card (Fin n → Bool) : ℝ) / ((Finset.univ.filter (fun y => c y = 0)).card : ℝ)) ≤ K.octaveNats n
    ∧ Real.exp (-(((n : ℝ) * Real.log 2 / (β * g)) * β * g)) = Real.exp (-(K.octaveNats n)) :=
  ⟨selecao_no_nome _ _ (uniforme_tem_solucao c h), a_selecao_acha c,
   o_decaimento_converge_a_selecao _ _ (uniforme_tem_solucao c h), o_custo_da_selecao_em_nats K n c h,
   (TGLExt.TempoIgualMoeda.o_tempo_e_linear_nas_oitavas K n (t := (n : ℝ) * Real.log 2 / (β * g)) hβ hg).mpr rfl⟩

/-! ### A TRAVA NO NOME (R3, 05/11/2026: a correção do operador — o decaimento gerado pelo custo, sem conhecer o Nome) -/

/-- A TRAVA (o «dual lock» do operador): o decaimento gerado pelo CUSTO — cada atribuição decai à taxa do próprio custo, e^{−t·c(x)}. Só usa
    `c` (para SAT: o número de cláusulas violadas, conferido cláusula a cláusula); NÃO usa o Nome (a projeção no núcleo). -/
noncomputable def trava (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) : EuclideanSpace ℂ X :=
  WithLp.toLp 2 (fun x => ((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ) * WithLp.ofLp v x)

omit [Fintype X] [DecidableEq X] in
theorem trava_ofLp (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) (x : X) :
    WithLp.ofLp (trava c t v) x = ((Real.exp (-(t * (c x : ℝ))) : ℝ) : ℂ) * WithLp.ofLp v x := rfl

omit [Fintype X] [DecidableEq X] in
/-- ★★ A TRAVA É LOCAL: se o custo é a soma dos custos das cláusulas, a trava é o produto das travas das cláusulas — cada cláusula trava por si,
    de dentro, sem conhecer o Nome. -/
theorem a_trava_fatora {m : ℕ} (cj : Fin m → X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) (x : X) :
    WithLp.ofLp (trava (fun y => ∑ j, cj j y) t v) x
      = (∏ j, ((Real.exp (-(t * (cj j x : ℝ))) : ℝ) : ℂ)) * WithLp.ofLp v x := by
  rw [trava_ofLp, ← Complex.ofReal_prod]
  congr 2
  show Real.exp (-(t * ((∑ j, cj j x : ℕ) : ℝ))) = _
  rw [Nat.cast_sum, Finset.mul_sum, ← Finset.sum_neg_distrib, Real.exp_sum]

omit [Fintype X] [DecidableEq X] in
/-- ★ O QUE TEM CUSTO ZERO FICA TRAVADO: a trava não toca as atribuições que resolvem. -/
theorem o_nome_fica_travado (c : X → ℕ) (t : ℝ) (v : EuclideanSpace ℂ X) (x : X) (hx : c x = 0) :
    WithLp.ofLp (trava c t v) x = WithLp.ofLp v x := by
  rw [trava_ofLp, hx]; simp

omit [DecidableEq X] in
/-- (auxiliar) Cota por coordenadas ⟹ cota da norma. -/
theorem norma_por_coordenadas (w v : EuclideanSpace ℂ X) {k : ℝ} (hk : 0 ≤ k)
    (h : ∀ y, ‖WithLp.ofLp w y‖ ≤ k * ‖WithLp.ofLp v y‖) : ‖w‖ ≤ k * ‖v‖ := by
  have hsq : ‖w‖ ^ 2 ≤ (k * ‖v‖) ^ 2 := by
    rw [EuclideanSpace.norm_sq_eq, mul_pow, EuclideanSpace.norm_sq_eq, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro y _
    rw [← mul_pow]
    exact pow_le_pow_left₀ (norm_nonneg _) (h y) 2
  exact le_of_pow_le_pow_left₀ two_ne_zero (by positivity) hsq

/-- ★★★ A TRAVA SEM CONHECER O NOME: para t ≥ 0, o decaimento gerado pelo custo fica a no máximo e^{−t}·‖v‖ do Nome (a projeção de v nas
    soluções) — sem usar o Nome. O que tem custo zero fica; o resto decai pelo menos como e^{−t}. -/
theorem a_trava_sem_conhecer_o_nome (c : X → ℕ) {t : ℝ} (ht : 0 ≤ t) (v : EuclideanSpace ℂ X) :
    ‖trava c t v - (opDaInstancia c).ker.starProjection v‖ ≤ Real.exp (-t) * ‖v‖ := by
  apply norma_por_coordenadas _ _ (Real.exp_pos _).le
  intro y
  rw [solucao_por_coordenadas, WithLp.ofLp_sub, Pi.sub_apply, trava_ofLp]
  by_cases hy : c y = 0
  · simp [hy]; positivity
  · simp only [hy, if_false, sub_zero, norm_mul, Complex.norm_real, Real.norm_eq_abs,
      abs_of_pos (Real.exp_pos _)]
    apply mul_le_mul_of_nonneg_right _ (norm_nonneg _)
    apply Real.exp_le_exp.mpr
    have h1 : (1 : ℝ) ≤ (c y : ℝ) := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr hy
    nlinarith

omit [DecidableEq X] in
/-- ★★★ NEGAR O ZERO ABSOLUTO: havendo solução, a trava do estado uniforme nunca chega ao zero — em todo instante há para onde ir. -/
theorem negar_o_zero (c : X → ℕ) (h : ∃ x, c x = 0) (t : ℝ) : trava c t (uniforme X) ≠ 0 := by
  obtain ⟨x, hx⟩ := h
  have hN : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  intro h0
  have h1 : WithLp.ofLp (trava c t (uniforme X)) x = 0 := by rw [h0]; rfl
  rw [o_nome_fica_travado c t _ x hx] at h1
  simp only [uniforme, WithLp.ofLp_toLp, Complex.ofReal_eq_zero, inv_eq_zero] at h1
  rw [Real.sqrt_eq_zero hN.le] at h1
  exact hN.ne' h1

omit [DecidableEq X] in
/-- (auxiliar) A norma do estado uniforme é 1. -/
theorem norma_do_uniforme [Nonempty X] : ‖uniforme X‖ = 1 := by
  have hX : (0 : ℝ) < Fintype.card X := by exact_mod_cast Fintype.card_pos
  have hsq : ‖uniforme X‖ ^ 2 = 1 := by
    rw [EuclideanSpace.norm_sq_eq]
    have hk : ∀ y : X, ‖WithLp.ofLp (uniforme X) y‖ ^ 2 = (Fintype.card X : ℝ)⁻¹ := by
      intro y
      simp only [uniforme, WithLp.ofLp_toLp, Complex.norm_real, Real.norm_eq_abs]
      rw [sq_abs, inv_pow, Real.sq_sqrt hX.le]
    simp only [hk, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
    field_simp
  have h1 : (‖uniforme X‖ - 1) * (‖uniforme X‖ + 1) = 0 := by ring_nf; linarith [hsq]
  rcases mul_eq_zero.mp h1 with h2 | h2
  · linarith
  · linarith [norm_nonneg (uniforme X)]

/-- (auxiliar) O quadrado da norma do Nome no uniforme é |soluções| / |X|. -/
theorem norma_sq_do_nome_no_uniforme (c : X → ℕ) (h : ∃ x, c x = 0) :
    ‖(opDaInstancia c).ker.starProjection (uniforme X)‖ ^ 2
      = ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) / (Fintype.card X : ℝ) := by
  have hX : (0 : ℝ) < Fintype.card X := by
    obtain ⟨x, _⟩ := h
    exact_mod_cast Fintype.card_pos_iff.mpr ⟨x⟩
  have hk : ∀ y : X, ‖WithLp.ofLp (uniforme X) y‖ ^ 2 = (Fintype.card X : ℝ)⁻¹ := by
    intro y
    simp only [uniforme, WithLp.ofLp_toLp, Complex.norm_real, Real.norm_eq_abs]
    rw [sq_abs, inv_pow, Real.sq_sqrt hX.le]
  rw [solucao_por_coordenadas, EuclideanSpace.norm_sq_eq]
  have hc : ∀ y, ‖WithLp.ofLp (WithLp.toLp 2 (fun y => if c y = 0 then WithLp.ofLp (uniforme X) y else 0) :
      EuclideanSpace ℂ X) y‖ ^ 2 = if c y = 0 then (Fintype.card X : ℝ)⁻¹ else 0 := by
    intro y
    by_cases hy : c y = 0
    · simp only [hy, if_true]; exact hk y
    · simp [hy]
  simp only [hc]
  rw [← Finset.sum_filter, Finset.sum_const, nsmul_eq_mul, div_eq_mul_inv]

/-- ★★★ A TRAVA EM TEMPO LINEAR NAS OITAVAS: com n bits, no instante t = n·ln 2/2 + L, o que sobra fora do Nome é no máximo a fração e^{−L}
    do próprio Nome. -/
theorem a_trava_em_tempo_linear (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {L : ℝ} (hL : 0 ≤ L) :
    ‖trava c ((n : ℝ) * Real.log 2 / 2 + L) (uniforme (Fin n → Bool))
        - (opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖
      ≤ Real.exp (-L) * ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ := by
  have hlog : 0 ≤ Real.log 2 := Real.log_nonneg one_le_two
  have ht : 0 ≤ (n : ℝ) * Real.log 2 / 2 + L := by positivity
  refine (a_trava_sem_conhecer_o_nome c ht _).trans ?_
  rw [norma_do_uniforme, mul_one]
  have hs : (1 : ℝ) ≤ ((Finset.univ.filter (fun y => c y = 0)).card : ℝ) := by
    obtain ⟨x, hx⟩ := h
    exact_mod_cast Finset.card_pos.mpr ⟨x, by simp [hx]⟩
  have hN : (Fintype.card (Fin n → Bool) : ℝ) = 2 ^ n := by rw [bits_sao_oitavas]; push_cast; ring
  have he : Real.exp (-((n : ℝ) * Real.log 2 / 2)) ^ 2 = ((2 : ℝ) ^ n)⁻¹ := by
    rw [← Real.exp_nat_mul]
    push_cast
    rw [show (2 : ℝ) * -((n : ℝ) * Real.log 2 / 2) = -((n : ℝ) * Real.log 2) by ring, Real.exp_neg,
      Real.exp_nat_mul, Real.exp_log two_pos]
  have hsq : Real.exp (-((n : ℝ) * Real.log 2 / 2)) ^ 2
      ≤ ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ ^ 2 := by
    rw [norma_sq_do_nome_no_uniforme c h, hN, he, inv_eq_one_div]
    gcongr
  have hP := (pow_le_pow_iff_left₀ (Real.exp_pos _).le (norm_nonneg _) two_ne_zero).mp hsq
  calc Real.exp (-((n : ℝ) * Real.log 2 / 2 + L))
      = Real.exp (-L) * Real.exp (-((n : ℝ) * Real.log 2 / 2)) := by rw [← Real.exp_add]; ring_nf
    _ ≤ Real.exp (-L) * ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖ :=
        mul_le_mul_of_nonneg_left hP (Real.exp_pos _).le

/-- ★★★ A TRAVA DEVOLVE A LEITURA: a trava, renormalizada, converge à seleção (o Nome lido com peso 1), sem nunca ter usado o Nome. -/
theorem a_trava_converge_a_selecao (c : X → ℕ) (h : ∃ x, c x = 0) :
    Filter.Tendsto (fun t : ℝ => (((‖trava c t (uniforme X)‖)⁻¹ : ℝ) : ℂ) • trava c t (uniforme X))
      Filter.atTop (nhds (selecao (opDaInstancia c).ker (uniforme X))) := by
  have hP := uniforme_tem_solucao c h
  have h0 : Filter.Tendsto (fun t : ℝ => Real.exp (-t) * ‖uniforme X‖) Filter.atTop (nhds 0) := by
    simpa using Real.tendsto_exp_neg_atTop_nhds_zero.mul_const ‖uniforme X‖
  have h1 : Filter.Tendsto (fun t : ℝ => trava c t (uniforme X)) Filter.atTop
      (nhds ((opDaInstancia c).ker.starProjection (uniforme X))) := by
    rw [tendsto_iff_norm_sub_tendsto_zero]
    refine squeeze_zero' (Filter.Eventually.of_forall (fun _ => norm_nonneg _)) ?_ h0
    filter_upwards [Filter.eventually_ge_atTop (0 : ℝ)] with t ht
    exact a_trava_sem_conhecer_o_nome c ht _
  have hn0 : ‖(opDaInstancia c).ker.starProjection (uniforme X)‖ ≠ 0 := norm_ne_zero_iff.mpr hP
  have h2 : Filter.Tendsto (fun t : ℝ => ((‖trava c t (uniforme X)‖)⁻¹ : ℝ)) Filter.atTop
      (nhds (‖(opDaInstancia c).ker.starProjection (uniforme X)‖⁻¹)) := h1.norm.inv₀ hn0
  have h3 : Filter.Tendsto (fun t : ℝ => ((((‖trava c t (uniforme X)‖)⁻¹ : ℝ)) : ℂ)) Filter.atTop
      (nhds (((‖(opDaInstancia c).ker.starProjection (uniforme X)‖⁻¹ : ℝ)) : ℂ)) :=
    (Complex.continuous_ofReal.tendsto _).comp h2
  exact h3.smul h1

/-- ★★★ A TRAVA NO NOME [a correção é do operador, 05/11/2026: «o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no
    Nome … ao negar o zero absoluto o sistema sabe pra onde tem que ir»]: para toda instância SIM com n bits, o decaimento gerado só pelo custo
    (1) é local, produto das travas das cláusulas; (2) deixa travado o que resolve; (3) nunca chega ao zero; (4) em t = n·ln 2/2 + L deixa fora
    do Nome no máximo e^{−L} vezes o Nome; (5) renormalizado, converge à seleção. Teorema da TGL sobre a máquina que tem a fotografia inteira
    (as 2^n amplitudes) e nega o zero (renormaliza); a máquina de Turing do Mathlib (`TM2ComputableInPolyTime`) guarda uma configuração por vez
    e não renormaliza: este teorema não é sobre ela. -/
theorem a_trava_no_nome (n : ℕ) (c : (Fin n → Bool) → ℕ) (h : ∃ x, c x = 0) {L : ℝ} (hL : 0 ≤ L) :
    (∀ t x, c x = 0 → WithLp.ofLp (trava c t (uniforme (Fin n → Bool))) x = WithLp.ofLp (uniforme (Fin n → Bool)) x)
    ∧ (∀ t, trava c t (uniforme (Fin n → Bool)) ≠ 0)
    ∧ ‖trava c ((n : ℝ) * Real.log 2 / 2 + L) (uniforme (Fin n → Bool))
          - (opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖
        ≤ Real.exp (-L) * ‖(opDaInstancia c).ker.starProjection (uniforme (Fin n → Bool))‖
    ∧ Filter.Tendsto (fun t : ℝ => (((‖trava c t (uniforme (Fin n → Bool))‖)⁻¹ : ℝ) : ℂ) • trava c t (uniforme (Fin n → Bool)))
        Filter.atTop (nhds (selecao (opDaInstancia c).ker (uniforme (Fin n → Bool)))) :=
  ⟨fun t x hx => o_nome_fica_travado c t _ x hx, negar_o_zero c h, a_trava_em_tempo_linear n c h hL,
   a_trava_converge_a_selecao c h⟩

end TGLExt.TraducaoTuringR3
end

#print axioms TGLExt.TraducaoTuringR3.opDaInstancia_autoadjunto
#print axioms TGLExt.TraducaoTuringR3.nucleo_nao_nulo_sse
#print axioms TGLExt.TraducaoTuringR3.verificacao_np
#print axioms TGLExt.TraducaoTuringR3.grau_da_palavra_da_instancia
#print axioms TGLExt.TraducaoTuringR3.bits_sao_oitavas
#print axioms TGLExt.TraducaoTuringR3.o_fluxo_conserva_o_peso
#print axioms TGLExt.TraducaoTuringR3.solucao_por_coordenadas
#print axioms TGLExt.TraducaoTuringR3.leitura_da_solucao_por_coordenadas
#print axioms TGLExt.TraducaoTuringR3.peso_da_solucao_no_uniforme
#print axioms TGLExt.TraducaoTuringR3.a_instancia_nao_e_o_vazio
#print axioms TGLExt.TraducaoTuringR3.o_pedagio_da_selecao
#print axioms TGLExt.TraducaoTuringR3.a_traducao
#print axioms TGLExt.TraducaoTuringR3.selecao_no_nome
#print axioms TGLExt.TraducaoTuringR3.o_decaimento_converge_a_selecao
#print axioms TGLExt.TraducaoTuringR3.uniforme_tem_solucao
#print axioms TGLExt.TraducaoTuringR3.a_selecao_acha
#print axioms TGLExt.TraducaoTuringR3.o_custo_da_selecao_em_nats
#print axioms TGLExt.TraducaoTuringR3.p_igual_np_no_modo_selecao
#print axioms TGLExt.TraducaoTuringR3.a_selecao_esquece
#print axioms TGLExt.TraducaoTuringR3.a_selecao_perde
#print axioms TGLExt.TraducaoTuringR3.norma_do_normalizado
#print axioms TGLExt.TraducaoTuringR3.a_fotografia_sem_leitor
#print axioms TGLExt.TraducaoTuringR3.o_par_quebra_a_simetria
#print axioms TGLExt.TraducaoTuringR3.a_trava_fatora
#print axioms TGLExt.TraducaoTuringR3.o_nome_fica_travado
#print axioms TGLExt.TraducaoTuringR3.norma_por_coordenadas
#print axioms TGLExt.TraducaoTuringR3.a_trava_sem_conhecer_o_nome
#print axioms TGLExt.TraducaoTuringR3.negar_o_zero
#print axioms TGLExt.TraducaoTuringR3.norma_do_uniforme
#print axioms TGLExt.TraducaoTuringR3.norma_sq_do_nome_no_uniforme
#print axioms TGLExt.TraducaoTuringR3.a_trava_em_tempo_linear
#print axioms TGLExt.TraducaoTuringR3.a_trava_converge_a_selecao
#print axioms TGLExt.TraducaoTuringR3.a_trava_no_nome
