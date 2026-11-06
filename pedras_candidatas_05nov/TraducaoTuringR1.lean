import TGLExt.PIgualNP
import TGLExt.TetelestaiTerminal
import TGLExt.TheFalseHasNoGeometry
import Mathlib.Analysis.CStarAlgebra.Matrix

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# A TRADUÇÃO DAS CLASSES DO DICIONÁRIO ÀS CLASSES DE TURING — o que fecha e onde fica a parede
  [TGLExt — pedra CANDIDATA da gerência c1, 05/11/2026, rodada R1; NOME PROVISÓRIO (o nome é do operador); compilada no sandbox da v408
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
* A igualdade P = NP das máquinas de Turing é um enunciado MATEMÁTICO sobre máquinas de Turing; nenhuma física o prova ou refuta por si. Uma lei
  física da leitura só decidiria o que um DISPOSITIVO da TGL resolve em tempo polinomial (a tese física de Church–Turing), não a igualdade de Turing.
* Nada aqui é teste com a natureza; não move o gate; PROVADA = validade no kernel, não creditação; NOT_FALSIFIED nunca é CONFIRMED.
Sem sorry, sem axiom; trio `{propext, Classical.choice, Quot.sound}`.
-/

noncomputable section
namespace TGLExt.TraducaoTuringR1
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

end TGLExt.TraducaoTuringR1
end

#print axioms TGLExt.TraducaoTuringR1.opDaInstancia_autoadjunto
#print axioms TGLExt.TraducaoTuringR1.nucleo_nao_nulo_sse
#print axioms TGLExt.TraducaoTuringR1.verificacao_np
#print axioms TGLExt.TraducaoTuringR1.grau_da_palavra_da_instancia
#print axioms TGLExt.TraducaoTuringR1.bits_sao_oitavas
#print axioms TGLExt.TraducaoTuringR1.o_fluxo_conserva_o_peso
#print axioms TGLExt.TraducaoTuringR1.solucao_por_coordenadas
#print axioms TGLExt.TraducaoTuringR1.leitura_da_solucao_por_coordenadas
#print axioms TGLExt.TraducaoTuringR1.peso_da_solucao_no_uniforme
#print axioms TGLExt.TraducaoTuringR1.a_instancia_nao_e_o_vazio
#print axioms TGLExt.TraducaoTuringR1.o_pedagio_da_selecao
#print axioms TGLExt.TraducaoTuringR1.a_traducao
