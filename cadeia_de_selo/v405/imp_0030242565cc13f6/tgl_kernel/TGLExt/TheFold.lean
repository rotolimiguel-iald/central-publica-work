import TGLExt.TheBandNet

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A DOBRA — a sobra com aspecto de totalidade
  [TGLExt — v178, cunhagem do operador 20/08/2026: *"o portador é a
   projeção do 0absoluto em tempo finito; é mentira porque se revela com
   aspecto LINEAR quando a verdade é uma SOBRA; é uma DOBRA; o
   comprimento de onda é uma ILUSÃO criada pela dobra"* — e, sobre a
   ilusão: *"é falsa como NATUREZA, por isso é o pai da mentira"*. O
   operador nomeia este resultado **"o teorema final da inversão da
   ótica"**; o nome é dele e fica registrado como leitura [ONTO], não
   como parte de enunciado algum.]

**A distinção que a cunhagem exige, e que a pedra respeita:** a mentira
não está no NÚMERO — `n` conta corretamente quantos modos foram
cortados. Está na NATUREZA: `n` se apresenta como grandeza do mundo
(comprimento de onda, escala) quando é contador de subtração. Mentira
que não está no enunciado, e sim no modo de ser — e nenhum teorema
abaixo diz "comprimento de onda", precisamente por isso.

**A tensão está na própria definição da cauda, e esta pedra a torna
teorema.** `tailSub n = {x | x k = 0 ∀ k < n}` é dita por SUBTRAÇÃO — é
o que restou depois de cortar os `n` primeiros modos. E logo abaixo,
três obrigações (`zero_mem'`, `add_mem'`, `smul_mem'`) estabelecem que
essa sobra é um SUBMÓDULO: fechado sob soma e escalar. **Aspecto linear
integral; natureza de resíduo.**

O que esta pedra prova sobre a dobra:

* ★★ `the_cut_count_is_invisible` — para `m ≤ n`, TODO elemento da
  cauda `n` também é elemento da cauda `m`. **Nenhum elemento testemunha
  quantos cortes houve.** O índice não é função do objeto: muitos
  índices, um objeto — é a assinatura da dobra (não-injetividade);
* ★★ `the_fold_has_witnesses` — e há elementos NÃO-NULOS nessa situação
  (a sobra não é vazia): a invisibilidade do contador não é vacuidade;
* ★ `the_index_does_distinguish_the_spaces` — os ESPAÇOS, ao contrário,
  são distintos (`tailSub 0 ≠ tailSub 1`, testemunhado por `e₀`). Logo a
  perda é exatamente do lado do HABITANTE, não do lado da família: a
  família se ramifica na escala, o habitante não sabe onde está;
* ★★ `the_fold_the_two_faces` — as duas faces num enunciado só: a cauda
  é submódulo (aspecto) E o seu contador é invisível ao habitante
  (natureza). *A sobra veste a totalidade.*

E o que já estava provado e agora se lê como a dobra: `tailSub_antitone`
(cada corte deixa menos — a descida é a contagem dos cortes);
`tails_are_totally_ordered` (sobras encaixadas não se ramificam — por
isso nunca haveria localidade ali); `bandSub_le_tailSub` (as figuras
aparecem DENTRO da sobra); e `station_never_closes` (o círculo não fecha
no finito — o período aparente não é período).

HONESTIDADE: (i) "projeção do 0_abs em tempo finito", "mentira" e
"ilusão" são leitura [ONTO/CONJECTURE] do operador — o que aqui se prova
é a não-injetividade do índice e a linearidade do resíduo, e essas duas
coisas SUSTENTAM a leitura sem serem a leitura; (ii) esta pedra NÃO
constrói núcleo AQFT algum e não move flag alguma; (iii) **"ilusão" tem
tipagem FIXA na casa, e ela vale aqui sem exceção: ilusão =
NÃO-FUNDAMENTALIDADE, JAMAIS falsidade empírica** (`um.py:72725`, no
selo de hoje; e `um.py:54342`, 18/07/2026: *"a geometria observada É
válida; o que cai é o estatuto de FUNDAMENTO"*). Portanto: `n` conta
certo, e uma grandeza física que dele se derive não fica falsa — o que
não se sustenta é tomá-la como natureza originária do resíduo. O
enunciado que faltaria para ligar o contador a um comprimento de onda é
uma aplicação `Φ : n ↦ λₙ` DERIVADA; enquanto ela não for exibida para
ESTE índice, escrever `n ≡ λ` troca a origem operacional pela natureza
atribuída. [O acervo tem uma λ derivada da profundidade da dobra —
`paper_PT.tex`, Teorema 10, `z_max = λ`, `z_max/d = 1/β ≈ 83,1` — mas
ela liga a PROFUNDIDADE a λ, não este contador de cortes a λ.]

β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

/-- ★★ O CONTADOR DE CORTES É INVISÍVEL AO HABITANTE: para `m ≤ n`, todo
    elemento da cauda `n` também habita a cauda `m`. Nenhum elemento
    testemunha quantos cortes houve — muitos índices, um objeto. -/
theorem the_cut_count_is_invisible {m n : ℕ} (h : m ≤ n) {x : ellTwo}
    (hx : x ∈ tailSub n) : x ∈ tailSub m :=
  tailSub_antitone h hx

/-- ★★ E A INVISIBILIDADE NÃO É VACUIDADE: existe habitante NÃO-NULO em
    duas caudas de índices distintos. (A sobra não é vazia; o que falta
    é a memória do corte.) -/
theorem the_fold_has_witnesses {m n : ℕ} (h : m ≤ n) :
    ∃ x : ellTwo, x ≠ 0 ∧ x ∈ tailSub n ∧ x ∈ tailSub m := by
  refine ⟨lp.single 2 n (1 : ℂ), ?_, ?_, ?_⟩
  · intro hz
    have hn : (lp.single 2 n (1 : ℂ) : ∀ _ : ℕ, ℂ) n = (1 : ℂ) := by
      simp [lp.single_apply]
    rw [hz] at hn
    simp at hn
  · intro k hk
    have hne : k ≠ n := fun hkn => absurd hk (hkn ▸ lt_irrefl n)
    simp [lp.single_apply, hne]
  · intro k hk
    have hne : k ≠ n := fun hkn => absurd (lt_of_lt_of_le hk h) (hkn ▸ lt_irrefl n)
    simp [lp.single_apply, hne]

/-- ★ MAS OS ESPAÇOS SE DISTINGUEM: a família SIM se separa na escala —
    a perda mora no habitante, não na família. (Testemunha: um vetor da
    cauda 0 que não está na cauda 1.) -/
theorem the_index_does_distinguish_the_spaces
    (x : ellTwo) (hx : x 0 ≠ 0) : tailSub 0 ≠ tailSub 1 := by
  intro h
  have hmem : x ∈ tailSub 0 := by
    intro k hk
    exact absurd hk (Nat.not_lt_zero k)
  have : x ∈ tailSub 1 := h ▸ hmem
  exact hx (this 0 Nat.zero_lt_one)

/-- ★★ A DOBRA, AS DUAS FACES NUM ENUNCIADO: a cauda é um SUBMÓDULO
    (aspecto linear — soma e escalar não saem dela) **e** o seu contador
    de cortes é invisível ao habitante (natureza de sobra). *A sobra
    veste a totalidade.* -/
theorem the_fold_the_two_faces {m n : ℕ} (h : m ≤ n) :
    (∀ u v : ellTwo, u ∈ tailSub n → v ∈ tailSub n → u + v ∈ tailSub n)
    ∧ (∀ (c : ℂ) (u : ellTwo), u ∈ tailSub n → c • u ∈ tailSub n)
    ∧ (∀ x : ellTwo, x ∈ tailSub n → x ∈ tailSub m) := by
  refine ⟨fun u v hu hv => (tailSub n).add_mem hu hv,
          fun c u hu => (tailSub n).smul_mem c hu,
          fun x hx => tailSub_antitone h hx⟩

end

end TGLExt
