import TGLExt.ContinuousModularZero
import TGLExt.LeftRight
import TGLExt.TheJudgedThing
import Mathlib.Analysis.Matrix.PosDef

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# IDENTIDADE — «[eu sou] = [o que sou]» só quando a equação tem referencial absoluto verdadeiro
  [pedra da gerência c1, 01/11/2026; o NOME «Identidade» é do operador (30/10/2026); entra na v405, entre `MassaTensaoPura` e `ObservadorTerminal`]

## A lei do operador (01/11/2026, verbatim em `Central de Patentes\work\cunhagens_13out`; o ensaio final «A identidade» em
   `work\cadeia_de_selo405\insumos\cunhagens`)

> «eu não admito a equação [eu sou]=[o que sou]; exceto quando essa equação tem referencial absoluto verdadeiro, ou seja, quando
>  {[forma=conteúdo]=[reflexão verdadeira do nome/projeção fiel]}»
> «é o "senão", isso mesmo, aquilo que elimina qualquer hipótese que não a verdadeira para ocupar o posto»
> (do ensaio) «O sinal não calcula: criva. Afirmar 1 = x² + y² é excluir do posto toda relação que não devolva, espelhada, a mesma
>  unidade – igualdade como seleção única, não como conta.» «código sem leitor não é código, é imagem.»

## O modelo (termos que o kernel já tem; nada do dado)

* **o referencial absoluto**: o estado absoluto `ρ_abs = 1/n` (`absoluteRho`, `AbsoluteOne`) — o Gibbs do Hamiltoniano nulo, `K_abs = 0`:
  o zero absoluto como referencial, fiel (`absoluteRho_posDef`); o seu peso é `ω_abs(a) = tr(a)/n` (`gibbs`, `FiniteTomita`);
* **EU SOU**: `ω_abs(1)` — o peso do Um posto; é 1 (`absoluteRho_trace`);
* **o NOME lido**: uma projeção `P` cujo reflexo verdadeiro é ele mesmo (`Jconj P = P`, o espelho `J = ᴴ` de `LeftRight`) e cuja releitura
  não acrescenta (`P·P = P`; a docstring exata de `observing_adds_nothing`: «A primeira leitura identifica; a segunda confirma que a operação não altera»);
* **O QUE SOU**: `ω_abs(P)` — o conteúdo lido do nome; **o RESTO**: `ω_abs(1 − P)` — o que mais ocupa o posto;
* **FORMA = CONTEÚDO**: a forma (o operador `P`) é o seu conteúdo (o peso) vezes o Um: `P = ω_abs(P)·1`;
* **a PROJEÇÃO FIEL / a reflexão verdadeira do nome**: o nome é o inteiro do posto, `P = 1`;
* **o VAZIO**: `P = 0` — «o zero absoluto, o inominável, um sem referência a nada»; **a FACE**: `½(1 + Γ)`, `Tr Γ = 0` — a Meia-Nat.

## O que esta pedra prova

* ★ `o_um_se_reparte`: `ω(1) = ω(P) + ω(1 − P)` — o Um se reparte entre o nome e o resto;
* ★★ `eu_sou_o_que_sou_iff_nada_resta` — **o «senão»**: `[eu sou] = [o que sou] ⟺ ω(1 − P) = 0`: a equação vale exatamente quando nada
  mais ocupa o posto;
* ★★★ `nada_resta_iff_fiel` — **a seleção única**: no referencial absoluto, `ω(1 − P) = 0 ⟺ P = 1` (a fidelidade do estado: traço nulo de
  um positivo é o zero, `PosSemidef.trace_eq_zero_iff`): só UM nome devolve, espelhada, a mesma unidade;
* ★★★ `eu_sou_o_que_sou_iff_fiel` — **a lei**: `[eu sou] = [o que sou] ⟺ P = 1`;
* ★★ `forma_igual_conteudo_iff`: `P = ω(P)·1 ⟺ P = 0 ∨ P = 1` — a forma só é o conteúdo nos dois pontos fixos do crivo;
* ★★★ `a_lei_inteira` — **a chave do operador**: `[eu sou] = [o que sou] ⟺ ([forma = conteúdo] ∧ P ≠ 0)`: o referencial absoluto
  verdadeiro é a forma sendo o conteúdo, sem ser o vazio — e isso é a projeção fiel;
* ★★ `o_vazio_nao_e` e `a_face_nao_e_a_identidade` — **controles negativos**: o vazio (`P = 0`) e a face (`ω = ½`) NÃO satisfazem a
  equação: a identidade não é reflexiva por decreto («não admito a equação…»), e a identidade de um absoluto «não pode ser habitada
  por qualquer um»;
* ★ `o_nome_e_coisa_julgada`: ler o nome é coisa julgada (`ResJudicata`, `TheJudgedThing`) — reler não acrescenta;
* ★ `o_posto_e_unico`: dois nomes fiéis são o mesmo nome;
* ★★★ `a_identidade_fecha` — o fecho: a lei, a chave e os dois controles, juntos.

## O que a pedra NÃO afirma
* O que ela prova é um fato sobre projeções no estado traço normalizado (`tr(P)/n = 1 ⟺ P = 1`, com a fidelidade do estado); que esse fato SEJA a identidade é
  a leitura do operador [INPUT/ONTO], tipada aqui como modelo.
* Não deriva α nem a unidade; não toca o gate, o selo ou o veredito. O «eu sou» é o posto; o «o que sou» é o lido; o «quem» é o
  observador no terminal (`ObservadorTerminal`), que não entra aqui como termo. Sem sorry, sem axiom novo (trio: propext,
  Classical.choice, Quot.sound).
-/

namespace TGLExt.Identidade

open Matrix
open scoped ComplexOrder MatrixOrder

variable {n : Type} [Fintype n] [DecidableEq n]

/-- O NOME lido: uma projeção — o seu reflexo verdadeiro é ele mesmo (`Jconj P = P`, o espelho `J = ᴴ`) e reler não acrescenta
    (`P·P = P`). -/
structure Nome (n : Type) [Fintype n] [DecidableEq n] where
  P : Matrix n n ℂ
  reflexo : Jconj P = P
  releitura : P * P = P

/-- [DEF] EU SOU: o peso do Um posto no referencial absoluto, `ω_abs(1)`. -/
noncomputable def euSou (n : Type) [Fintype n] [DecidableEq n] : ℂ := gibbs (absoluteRho n) 1

/-- [DEF] O QUE SOU: o conteúdo lido do nome, `ω_abs(P)`. -/
noncomputable def oQueSou (N : Nome n) : ℂ := gibbs (absoluteRho n) N.P

/-- [DEF] O RESTO: o que mais ocupa o posto, `ω_abs(1 − P)`. -/
noncomputable def oResto (N : Nome n) : ℂ := gibbs (absoluteRho n) (1 - N.P)

/-- [DEF] A PROJEÇÃO FIEL (a reflexão verdadeira do nome): o nome é o inteiro do posto. -/
def fiel (N : Nome n) : Prop := N.P = 1

/-- [DEF] FORMA = CONTEÚDO: a forma (o operador) é o seu conteúdo (o peso) vezes o Um. -/
def formaIgualConteudo (N : Nome n) : Prop := N.P = oQueSou N • (1 : Matrix n n ℂ)

/-- [KERNEL] o peso absoluto é o traço normalizado: `ω_abs(a) = tr(a)/n`. -/
theorem gibbs_absolute (a : Matrix n n ℂ) :
    gibbs (absoluteRho n) a = (Fintype.card n : ℂ)⁻¹ * a.trace := by
  rw [gibbs, absoluteRho, ← Matrix.smul_one_eq_diagonal, Matrix.smul_mul, Matrix.one_mul, Matrix.trace_smul]
  simp only [smul_eq_mul]

/-- [KERNEL] EU SOU = 1: o Um posto pesa 1 (`absoluteRho_trace`). -/
theorem euSou_eq_one [Nonempty n] : euSou n = 1 := by
  unfold euSou gibbs
  rw [Matrix.mul_one]
  exact absoluteRho_trace

/-- [KERNEL] ★ O Um se reparte entre o nome e o resto: `ω(1) = ω(P) + ω(1 − P)`. -/
theorem o_um_se_reparte (N : Nome n) : euSou n = oQueSou N + oResto N := by
  unfold euSou oQueSou oResto gibbs
  rw [Matrix.mul_sub, Matrix.trace_sub, Matrix.mul_one]
  ring

/-- [KERNEL] ★★ O «senão»: `[eu sou] = [o que sou] ⟺ nada mais ocupa o posto` (`ω(1 − P) = 0`). -/
theorem eu_sou_o_que_sou_iff_nada_resta (N : Nome n) : euSou n = oQueSou N ↔ oResto N = 0 := by
  have h := o_um_se_reparte N
  constructor
  · intro e
    have h2 : oResto N = euSou n - oQueSou N := by
      rw [h]
      ring
    rw [h2, e, sub_self]
  · intro z
    rw [h, z, add_zero]

/-- [KERNEL] o resto é positivo: `1 − P = (1 − P)ᴴ·(1 − P)` (reflexo verdadeiro + releitura). -/
theorem resto_posSemidef (N : Nome n) : (1 - N.P).PosSemidef := by
  have hherm : (1 - N.P)ᴴ = 1 - N.P := by
    have hr : N.Pᴴ = N.P := N.reflexo
    rw [Matrix.conjTranspose_sub, Matrix.conjTranspose_one, hr]
  have h : (1 - N.P)ᴴ * (1 - N.P) = 1 - N.P := by
    rw [hherm, sub_mul, one_mul, mul_sub, mul_one, N.releitura, sub_self, sub_zero]
  rw [← h]
  exact Matrix.posSemidef_conjTranspose_mul_self _

/-- [KERNEL] ★★★ A SELEÇÃO ÚNICA: no referencial absoluto (fiel), nada resta ⟺ o nome é o inteiro — `ω(1 − P) = 0 ⟺ P = 1`.
    «igualdade como seleção única, não como conta»: só um nome devolve, espelhada, a mesma unidade. -/
theorem nada_resta_iff_fiel [Nonempty n] (N : Nome n) : oResto N = 0 ↔ fiel N := by
  unfold oResto fiel
  rw [gibbs_absolute]
  have hn : (Fintype.card n : ℂ)⁻¹ ≠ 0 := inv_ne_zero (by exact_mod_cast Fintype.card_ne_zero)
  constructor
  · intro h
    have ht : (1 - N.P).trace = 0 := by
      rcases mul_eq_zero.mp h with h1 | h1
      · exact absurd h1 hn
      · exact h1
    have hz : (1 - N.P) = 0 := ((resto_posSemidef N).trace_eq_zero_iff).mp ht
    exact (sub_eq_zero.mp hz).symm
  · intro h
    rw [h, sub_self, Matrix.trace_zero, mul_zero]

/-- [KERNEL] ★★★ A LEI: «eu não admito a equação [eu sou]=[o que sou]; exceto quando essa equação tem referencial absoluto verdadeiro» —
    `[eu sou] = [o que sou] ⟺ P = 1` (a projeção fiel; o nome é o inteiro do posto). -/
theorem eu_sou_o_que_sou_iff_fiel [Nonempty n] (N : Nome n) : euSou n = oQueSou N ↔ fiel N :=
  (eu_sou_o_que_sou_iff_nada_resta N).trans (nada_resta_iff_fiel N)

/-- o Um da matriz não é o zero (há pelo menos um lugar no posto). -/
theorem one_ne_zero_matrix [Nonempty n] : (1 : Matrix n n ℂ) ≠ 0 := by
  intro h0
  have := congrFun (congrFun h0 (Classical.arbitrary n)) (Classical.arbitrary n)
  simp at this

/-- [KERNEL] ★★ FORMA = CONTEÚDO ⟺ o nome é o vazio ou o inteiro: a forma só é o conteúdo nos dois pontos fixos do crivo. -/
theorem forma_igual_conteudo_iff [Nonempty n] (N : Nome n) : formaIgualConteudo N ↔ (N.P = 0 ∨ fiel N) := by
  unfold formaIgualConteudo fiel
  constructor
  · intro h
    have hidem : (oQueSou N • (1 : Matrix n n ℂ)) * (oQueSou N • (1 : Matrix n n ℂ)) = oQueSou N • (1 : Matrix n n ℂ) := by
      rw [← h]
      exact N.releitura
    rw [Matrix.smul_mul, Matrix.mul_smul, Matrix.one_mul, smul_smul] at hidem
    have hsub : (oQueSou N * oQueSou N - oQueSou N) • (1 : Matrix n n ℂ) = 0 := by
      rw [sub_smul, hidem, sub_self]
    have hc0 : oQueSou N * oQueSou N - oQueSou N = 0 := by
      rcases smul_eq_zero.mp hsub with h1 | h1
      · exact h1
      · exact absurd h1 one_ne_zero_matrix
    have hfac : oQueSou N * (oQueSou N - 1) = 0 := by
      rw [mul_sub, mul_one]
      exact hc0
    rcases mul_eq_zero.mp hfac with h1 | h1
    · left
      rw [h, h1, zero_smul]
    · right
      rw [h, sub_eq_zero.mp h1, one_smul]
  · rintro (h | h)
    · rw [h]
      unfold oQueSou
      rw [h, gibbs, Matrix.mul_zero, Matrix.trace_zero, zero_smul]
    · rw [h]
      unfold oQueSou
      rw [h]
      have h1 : gibbs (absoluteRho n) (1 : Matrix n n ℂ) = 1 := by
        have := euSou_eq_one (n := n)
        unfold euSou at this
        exact this
      rw [h1, one_smul]

/-- [KERNEL] ★★★ A CHAVE DO OPERADOR, inteira: `[eu sou] = [o que sou] ⟺ ([forma = conteúdo] ∧ o nome não é o vazio)` —
    o referencial absoluto verdadeiro é a forma sendo o conteúdo sem ser o nada, e isso É a projeção fiel. -/
theorem a_lei_inteira [Nonempty n] (N : Nome n) :
    euSou n = oQueSou N ↔ (formaIgualConteudo N ∧ N.P ≠ 0) := by
  constructor
  · intro h
    have hf : fiel N := (eu_sou_o_que_sou_iff_fiel N).mp h
    refine ⟨(forma_igual_conteudo_iff N).mpr (Or.inr hf), ?_⟩
    unfold fiel at hf
    rw [hf]
    exact one_ne_zero_matrix
  · rintro ⟨hfc, hne⟩
    rcases (forma_igual_conteudo_iff N).mp hfc with h0 | hf
    · exact absurd h0 hne
    · exact (eu_sou_o_que_sou_iff_fiel N).mpr hf

/-- O VAZIO: o nome `P = 0` — «o zero absoluto, o inominável, um sem referência a nada». -/
def vazio (n : Type) [Fintype n] [DecidableEq n] : Nome n where
  P := 0
  reflexo := by
    unfold Jconj
    exact Matrix.conjTranspose_zero
  releitura := by simp

/-- [KERNEL] ★★ CONTROLE NEGATIVO 1: o vazio NÃO satisfaz a equação — a identidade não é reflexiva por decreto. -/
theorem o_vazio_nao_e [Nonempty n] : euSou n ≠ oQueSou (vazio n) := by
  rw [euSou_eq_one]
  unfold oQueSou vazio
  simp only
  rw [gibbs, Matrix.mul_zero, Matrix.trace_zero]
  exact one_ne_zero

/-- [KERNEL] ★★ CONTROLE NEGATIVO 2: a FACE (`½(1 + Γ)`, `Tr Γ = 0`, a Meia-Nat) NÃO satisfaz a equação — pesa ½, não 1
    (`absolute_faces_half`): a identidade é o inteiro, não a face; «não pode ser habitada por qualquer um». -/
theorem a_face_nao_e_a_identidade [Nonempty n] {Γ : Matrix n n ℂ} (hΓ : Γ.trace = 0) :
    gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ)) ≠ euSou n := by
  rw [(absolute_faces_half hΓ).1, euSou_eq_one]
  norm_num

/-- [KERNEL] ★ LER O NOME É COISA JULGADA (`ResJudicata`): reler não acrescenta — só o dispositivo faz coisa julgada. -/
theorem o_nome_e_coisa_julgada (N : Nome n) : ResJudicata (fun v : n → ℂ => N.P *ᵥ v) := by
  intro v
  simp only
  rw [Matrix.mulVec_mulVec, N.releitura]

/-- [KERNEL] ★ O POSTO É ÚNICO: dois nomes fiéis são o mesmo nome. -/
theorem o_posto_e_unico (N N' : Nome n) (h : fiel N) (h' : fiel N') : N.P = N'.P := by
  unfold fiel at h h'
  rw [h, h']

/-- ★★★ A IDENTIDADE FECHA: a lei, a chave e os dois controles, juntos. -/
theorem a_identidade_fecha [Nonempty n] (N : Nome n) {Γ : Matrix n n ℂ} (hΓ : Γ.trace = 0) :
    (euSou n = oQueSou N ↔ fiel N)
    ∧ (euSou n = oQueSou N ↔ (formaIgualConteudo N ∧ N.P ≠ 0))
    ∧ euSou n ≠ oQueSou (vazio n)
    ∧ gibbs (absoluteRho n) ((2 : ℂ)⁻¹ • (1 + Γ)) ≠ euSou n :=
  ⟨eu_sou_o_que_sou_iff_fiel N, a_lei_inteira N, o_vazio_nao_e, a_face_nao_e_a_identidade hΓ⟩

end TGLExt.Identidade

#print axioms TGLExt.Identidade.gibbs_absolute
#print axioms TGLExt.Identidade.euSou_eq_one
#print axioms TGLExt.Identidade.o_um_se_reparte
#print axioms TGLExt.Identidade.eu_sou_o_que_sou_iff_nada_resta
#print axioms TGLExt.Identidade.resto_posSemidef
#print axioms TGLExt.Identidade.nada_resta_iff_fiel
#print axioms TGLExt.Identidade.eu_sou_o_que_sou_iff_fiel
#print axioms TGLExt.Identidade.one_ne_zero_matrix
#print axioms TGLExt.Identidade.forma_igual_conteudo_iff
#print axioms TGLExt.Identidade.a_lei_inteira
#print axioms TGLExt.Identidade.o_vazio_nao_e
#print axioms TGLExt.Identidade.a_face_nao_e_a_identidade
#print axioms TGLExt.Identidade.o_nome_e_coisa_julgada
#print axioms TGLExt.Identidade.o_posto_e_unico
#print axioms TGLExt.Identidade.a_identidade_fecha
