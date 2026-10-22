# -*- coding: utf-8 -*-
r"""RODADA 2 da pedra candidata TheUnitIsTheRank (construtor do kernel, reinvocado pela gerencia c1, 12/10/2026 noite).
Le a pedra da RODADA 1 (3_KERNEL\sandbox\TGLExt\TheUnitIsTheRank.lean, SO LEITURA; ela fica intocada como registro) e:
 (1) acrescenta NOTAS AO LADO em comentarios/docstrings (achados das auditorias da rodada 1, conferidos aqui), trocando
     so as duas citacoes de V4 que estavam em «» como parafrase pelos BYTES, com a nota do que eram -> texto r2a;
     confere que o CODIGO sem comentarios de r2a e byte a byte o da rodada 1 (nenhum enunciado, prova ou nome muda);
 (2) acrescenta a secao 15' (termos fora do pre-registro) antes da secao 16 e as sondas 17' antes do fim -> texto r2;
     confere que retirar exatamente esses dois blocos devolve r2a.
Grava a pedra r2 em 3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean (uma pedra anterior desta rodada, se houver,
e preservada como .tentativaNN) e o recibo MONTAGEM_PEDRA_R2_tNN.json. Falha visivel em qualquer divergencia."""
import hashlib, json, os, sys, re

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.dirname(R2)
ORIG = os.path.join(K, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
ORIG_SHA = "617155151fb0d9e110a4beda34f5f6cd40dd4636c6e0da13a3938f3ad1e08464"
DEST_DIR = os.path.join(R2, "sandbox", "TGLExt")
DEST = os.path.join(DEST_DIR, "TheUnitIsTheRank.lean")

AO = "⚠ AO LADO"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def strip_lean_comments(s):
    """Comentarios no grammar do Lean 4: bloco /- -/ ANINHADO (inclui /-- e /-!) e linha -- ate o fim da linha.
    Sem literais de string no arquivo (conferido abaixo: zero aspas duplas). Falha visivel se um bloco nao fecha."""
    out, i, n, depth = [], 0, len(s), 0
    while i < n:
        if depth == 0:
            if s.startswith("/-", i):
                depth, i = 1, i + 2
            elif s.startswith("--", i):
                j = s.find("\n", i)
                i = n if j < 0 else j
            else:
                out.append(s[i]); i += 1
        else:
            if s.startswith("/-", i):
                depth, i = depth + 1, i + 2
            elif s.startswith("-/", i):
                depth, i = depth - 1, i + 2
            else:
                i += 1
    if depth != 0:
        raise SystemExit("FALHA VISIVEL: comentario de bloco nao fechado")
    return "".join(out)


ob = open(ORIG, "rb").read()
if sha(ob) != ORIG_SHA:
    raise SystemExit("FALHA VISIVEL: a pedra da rodada 1 nao e a esperada")
if b"\r\n" in ob or b'"' in ob:
    raise SystemExit("FALHA VISIVEL: a rodada 1 tem CRLF ou aspas duplas; este script supoe LF e nenhuma string")
o = ob.decode("utf-8")
L = o.split("\n")

# ---------------------------------------------------------------- (1a) cabecalho (linhas da rodada 1, de baixo para cima)
H1 = r"""  [⚠ AO LADO (12/10/2026, noite — construtor do kernel, RODADA 2, em nome próprio; achado da auditoria de estatuto
   da rodada 1, conferido aqui por termo): o título diz mais que a pedra. «A unidade é o posto» vale NO ÁTOMO
   (B1: Tr ρ* = posto ρ* = 1; P4: o nome encontra o posto só em d = 1, `name_meets_rank_only_at_the_atom`); traço 1
   não dá posto 1 (`trace_one_not_rank_one`) e no ponto final da defasagem o posto é 2 (`endpoint_at_thetaMiguel`,
   `rank_not_preserved_by_dephasing`). O nome definitivo da pedra é do operador. A rodada 1 (`617155151fb0d9e1`) fica
   intacta em `3_KERNEL\sandbox` como registro; a rodada 2 muda só comentários e ACRESCENTA a seção 15' (termos fora
   do pré-registro) e as sondas 17'; nenhum enunciado nem prova da rodada 1 muda (conferido por script).]"""

H2 = r"""  [⚠ AO LADO (rodada 2, conferido nos bytes): nos bytes a fórmula está em LaTeX, l.16:
  «$$\rho = \vert{}\psi\rangle\langle\psi\vert{}, \quad \text{com } \text{Tr}(\rho) = 1 \text{ e } \text{Tr}(\rho^2) = 1$$»;
  ela NÃO está nos bytes de V1 (V1 l.6 termina em «posto 1:»). A primeira pessoa aparece só em «Quando eu derivei»
  (l.12), na mesma frase de «você impôs operadores de projeção rígidos».]"""

H3 = r"""* V4 `OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt` — sha16 `b365591ceb346cdf` (11/10): a dinâmica
  do rank. Nos bytes (LaTeX), l.13: «$$ \text{Tudo} = D_\beta(F(1)) $$» (lê-se Tudo = D_β(F(1))); l.16:
  «Esse pequeno vazamento de fase é o que impede o anticomutador perfeito $\{ \hat{Q}, \rho^* \} = 0$.»
  [⚠ AO LADO (rodada 2; achado das duas auditorias da rodada 1, conferido aqui nos bytes): na rodada 1
  (`617155151fb0d9e1`) as duas citações de V4 estavam em «» como paráfrase — LaTeX renderizado e, na segunda, um
  recorte que começava dentro de «pequeno»; as citações acima são os bytes.]"""

H4 = r"""* `[KNOWN]` — [⚠ AO LADO (rodada 2; achado da auditoria de estatuto da rodada 1)]: também são de livro-texto,
  formalizados aqui como TERMO: P² = P ⟹ Tr P = posto P (Mathlib `LinearMap.IsProj.trace`; B1.b); traço e posto
  invariantes por conjugação unitária (Mathlib `Matrix.trace_mul_cycle`, `Matrix.rank_mul_eq_left_of_isUnit_det`;
  B4.a); em M₂(ℂ), Tr M² = (Tr M)² − 2 det M (Cayley–Hamilton 2×2; P1.b); posto |ψ⟩⟨ψ| = 1 (P1.d); a compressão por
  projetor de posto 1 e a leitura seletiva (G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951); P3.a); S(θ)ⁿ = S(nθ),
  corolário de `Smat_mul` (SMatrix:81; B7.a1); a não convergência de sin²(nθ) com sin θ ≠ 0, elementar (B7.a2).
  O PASSA é do TERMO; o conteúdo segue sendo da literatura."""

H5 = r"""
[⚠ AO LADO (rodada 2; achados das auditorias da rodada 1, conferidos aqui)]: (i) `angular_leak_no_limit` prova que a
sequência sin²(nθ) não converge quando sin θ ≠ 0 — a leitura do ângulo NESTA sequência, não uma lei sobre todo
observável angular; (ii) a letra F designa nesta pedra F_θ = Ad S(θ) (F_θ(1) = `rhoOut θ`); o fluxo do lock
F(t) = P + e^{−t}(1 − P) (`TheAxiomAndTheFalseWitness.axiomFlow`), re-exportado em B9.c, é OUTRO objeto: nenhum lema do
kernel do Nós liga `axiomFlow` a `Smat`, `rhoOut` ou `dephase` (consulta por texto de 12/10, rodada 2: os dois só
coexistem em `TheVerbSelectsTheAction`, sem enunciado que os ligue); (iii) «D atua» é lido no semigrupo PARA A FRENTE:
∃ t ∈ ℝ equivale a ∃ t > 0 para quaisquer taxas (`dephasingActs_iff_forward`, seção 15')."""

H8 = r"""  [⚠ AO LADO (rodada 2, conferido nos bytes): «Tudo = D_β(F(1))» acima é o rótulo renderizado da conjectura, não
  citação de bytes; no um.py a forma é ASCII, l.6526: «Tudo = D_beta(F(1)) = VERDADE»; a de V4 está acima, em LaTeX.]"""

H6 = r"""* [rodada 2, fora do pré-registro; seção 15'] `dephase_fixed_iff_neg` e `dephasingActs_iff_forward` (o semigrupo
  para a frente basta); `one_sub_rhoOut_eq_Qtheta_neg`, `leak_of_complement`, `anticomm_complement_zero_iff` e
  `Qtheta_eq_one_sub_rhoOut_iff` (as duas leituras de Q̂ — S(θ)ᴴQ₀S(θ) e 1 − F_θ(1) = Q_{−θ} — dão o mesmo vazamento e o
  mesmo «{·, ρ*} = 0 ⟺ sin θ = 0», e coincidem só onde sin 2θ = 0); as sondas dos dois lados na seção 17'."""

H7 = r"""[⚠ AO LADO (rodada 2)]: também NÃO afirma que o ponto final de UMA passagem, D_∞F_θM(1) = diag(1 − β, β), seja ponto
fixo de canal iterado (o estado fixo do canal da F1.ATRATOR, citado em P3.b, é I/2; as pedras da F1.ATRATOR não estão
no kernel do Nós — consulta por nome, 12/10); nem que o PASSA de B9.b seja a letra de V4 l.10 (a letra é FALSA em
θ = 0: `literal_transmission_does_not_force_dephasing`); nem qual das duas leituras de Q̂ é a de V4 (decisão do texto
da v392)."""


def esperar(idx1, prefixo):
    if not L[idx1 - 1].startswith(prefixo):
        raise SystemExit("FALHA VISIVEL: linha %d nao comeca com %r: %r" % (idx1, prefixo, L[idx1 - 1]))


esperar(21, "   NÃO instalada no Nós — instalar é ato da v392]")
esperar(29, "* V2 `OPERADOR_12out_rank_e_tempo_santo_verbatim.txt`")
esperar(30, "  mesma passagem reafirmada, com a fórmula ρ = |ψ⟩⟨ψ|, Tr ρ = 1 e Tr ρ² = 1 (l.16).")
esperar(32, "* V4 `OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt`")
esperar(33, "  do rank («Tudo = D_β(F(1))», «o vazamento … impede o anticomutador perfeito {Q̂, ρ*} = 0»).")
esperar(44, "* `[KNOWN]` — «estado puro ⟺ posto 1»")
esperar(46, "  sendo da literatura.")
esperar(49, "* `[CONJECTURE ontológica]` (um.py l.6488) — «Tudo = D_β(F(1))»: aqui só o PONTO FINAL")
esperar(56,"hiperbólica de SL(2,ℝ) é [ONTO] (IALDJones) e não é afirmado aqui.")
esperar(69, "  `dephasing_acts_iff_transmits_and_leaks` (a leitura de inscrição).")
esperar(77, "reservado e não move o gate. Validade na face testada não é creditação. Sem sorry, sem axiom.")
esperar(78, "-/")
v4_antigo = L[31:33]
# de baixo para cima: inserir DEPOIS da linha k (1-based) = L.insert(k, ...)
L[77:77] = H7.split("\n")
L[69:69] = H6.split("\n")
L[56:56] = H5.split("\n")
L[49:49] = H8.split("\n")
L[46:46] = H4.split("\n")
L[31:33] = H3.split("\n")
L[30:30] = H2.split("\n")
L[21:21] = H1.split("\n")
r2a = "\n".join(L)

# ---------------------------------------------------------------- (1b) notas nas docstrings das declaracoes
NOTAS = [
    ("def Qtheta ", r"""[⚠ AO LADO (rodada 2; anexo A8 do ótico da rodada 1, conferido aqui por termo)]: este Q_θ NÃO é
    1 − F_θ(1); a outra leitura é 1 − F_θ(1) = Q_{−θ} (`one_sub_rhoOut_eq_Qtheta_neg`). As duas diferem fora da
    diagonal e coincidem só onde sin 2θ = 0 (`Qtheta_eq_one_sub_rhoOut_iff`); dão o mesmo vazamento
    (`leak_of_complement`) e o mesmo B2.a (`anticomm_complement_zero_iff`). Qual delas é o Q̂ de V4 l.16 é decisão do
    texto da v392."""),
    ("def dephasingActs ", r"""(Para quaisquer taxas, ∃ t ∈ ℝ equivale a ∃ t > 0: `dephasingActs_iff_forward`, rodada 2.)"""),
    ("theorem trace_eq_rank_of_projection ", r"""[KNOWN: traço de projeção = posto; o PASSA é do TERMO.]"""),
    ("theorem compression_by_rank_one ", r"""[KNOWN: G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951); o PASSA é do TERMO.]"""),
    ("theorem reading_returns_the_post ", r"""(É a leitura SELETIVA de Lüders, normalizada pelo peso de Born ⟨a, Xa⟩;
    [KNOWN].)"""),
    ("theorem reading_of_the_attractor_state", r"""[⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1)]: a leitura é
    SELETIVA: devolve ρ* com peso de Born Tr(ρ*·I/2) = 1/2; a não seletiva devolveria a mistura. I/2 vem da F1.ATRATOR,
    cujas pedras candidatas NÃO estão no kernel do Nós (consulta por nome, 12/10)."""),
    ("theorem reading_weights_are_truth_and_cost ", r"""(«verdade» e «custo» são leituras [ONTO] do nome; a conta lê as
    duas entradas de diag(1 − b, b).)"""),
    ("theorem anticomm_zero_iff ", r"""[⚠ AO LADO (rodada 2)]: é a AVALIAÇÃO exata que substitui o
    «{Q,rho*}=0 EXATO so' em theta_M->0» do um.py v391 (l.6502): com 0 < β < 1 (`TGLCoupling`) θ = 0 fica excluído pela
    hipótese; não é «limite inalcancavel» (um.py l.6515) — nunca se pede limite ao ângulo."""),
    ("theorem ad_trace ", r"""[KNOWN: Mathlib `Matrix.trace_mul_cycle`; o PASSA é do TERMO.]"""),
    ("theorem ad_rank ", r"""[KNOWN: Mathlib `Matrix.rank_mul_eq_left_of_isUnit_det` e
    `Matrix.rank_mul_eq_right_of_isUnit_det`; o PASSA é do TERMO.]"""),
    ("theorem fractal_one_is_rank_one ", r"""(Corolário de `ad_rank`, `ad_trace` e da pedra 116; «fractal» é leitura
    [ONTO] do nome.)"""),
    ("theorem endpoint_eq ", r"""(Refaz numa só igualdade `dephased_rhoOut_zero_zero` e `dephased_rhoOut_one_one`,
    GlobalLiftLadder:219 e 228; o novo aqui é o POSTO do ponto final, abaixo.)"""),
    ("theorem dephased_trace ", r"""(Composição de `dephase_preserves_trace`, TheTraceIsNotErasable:96, com
    `rhoOut_trace`.)"""),
    ("theorem rank_not_preserved_by_dephasing ", r"""(O desfecho estava previsto no levantamento, R4: é negativo
    certificado, não descoberta.)"""),
    ("theorem trace_survives_dephasing ", r"""(Re-exportação de `trace_diagExpect`, CondExpect:114.)"""),
    ("theorem leak_survives_dephasing ", r"""(O leitor ρ* é diagonal e por isso cego à defasagem; um leitor não
    diagonal vê o tempo: C10, `nondiagonal_reader_sees_time`.)"""),
    ("theorem Smat_pow ", r"""(Corolário de `Smat_mul`, SMatrix:81: a lei de grupo já estava no kernel.)"""),
    ("theorem angular_leak_no_limit ", r"""(Elementar; é a leitura do ângulo NESTA sequência, não uma lei geral.)"""),
    ("theorem nothing_branch ", r"""[⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1)]: a não-defasagem tem
    DOIS polos, θ = 0 (β = 0, transmissão total) e θ = π/2 (β = 1, reflexão total), ambos de posto 1
    (`dephasing_trivial_iff`, `dephasing_trivial_at_thetaMiguel`, `endpoint_rank_one_at_poles`). Na tipagem da
    matriz-S, «O que **não** transmite (o que não defasa)» (V4 l.9) aponta θ = π/2; este ramo, θ = 0, é transmissão
    total."""),
    ("theorem dephasing_acts_iff_transmits_and_leaks ", r"""(O PASSA é desta leitura, escolhida pela gerência [INPUT] e
    sustentada pelo cânone; a letra de V4 l.10 é FALSA em θ = 0: `literal_transmission_does_not_force_dephasing`.
    «D atua» vale já num t > 0: `dephasingActs_iff_forward`.)"""),
    ("theorem inscription_at_thetaMiguel ", r"""(«inscrição» é leitura [INPUT da gerência]; o valor em θ_M é identidade
    de θ_M := arcsin √β, sem poder discriminante.)"""),
    ("theorem transmission_dephases_reexport ", r"""[⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1, conferido
    aqui)]: HOMÔNIMO. O «transmitir» daqui é o fluxo do lock P + e^{−t}(1 − P), que contrai AO posto P; o da sonda B9
    é |𝓣|² da matriz-S, cuja defasagem SOBE o posto de 1 para 2 (`endpoint_at_thetaMiguel`). Nenhum lema do kernel
    liga os dois (consulta por texto, 12/10): este termo existe no kernel, mas não apoia a leitura B9.b."""),
]

for ancora, nota in NOTAS:
    for proib in ("/-", "-/", '"'):
        if proib in nota:
            raise SystemExit("FALHA VISIVEL: a nota de %s contem %r" % (ancora, proib))
for bloco in (H1, H2, H3, H4, H5, H6, H7, H8):
    for proib in ("/-", "-/", '"'):
        if proib in bloco:
            raise SystemExit("FALHA VISIVEL: nota de cabecalho contem %r" % proib)

log_notas = []
s = r2a
for ancora, nota in NOTAS:
    k = s.count("\n" + ancora)
    if k != 1:
        raise SystemExit("FALHA VISIVEL: ancora %r ocorre %d vezes" % (ancora, k))
    pos = s.index("\n" + ancora)
    fim = s.rfind("-/", 0, pos)
    entre = s[fim + 2:pos]
    if entre.strip() != "":
        raise SystemExit("FALHA VISIVEL: a docstring nao precede imediatamente %r: %r" % (ancora, entre))
    ini = s.rfind("/--", 0, fim)
    if ini < 0 or s.rfind("-/", 0, fim) > ini:
        raise SystemExit("FALHA VISIVEL: docstring de %r nao encontrada" % ancora)
    antes = s[:fim].rstrip(" ")
    s = antes + "\n    " + nota + " " + s[fim:]
    log_notas.append({"declaracao": ancora.strip(), "bytes_nota": len(nota.encode("utf-8"))})
r2a = s

cod_o = strip_lean_comments(o)
cod_a = strip_lean_comments(r2a)
if cod_o != cod_a:
    raise SystemExit("FALHA VISIVEL: o codigo sem comentarios mudou em r2a")

# ---------------------------------------------------------------- (2) blocos de codigo acrescentados
SEC15 = r"""/-! ## 15'. Rodada 2 — termos fora do pré-registro

[⚠ AO LADO (12/10/2026, noite — construtor do kernel, rodada 2, em nome próprio)]: achados das auditorias da rodada 1,
conferidos aqui por termo. Não mudam nenhuma parte pré-registrada (enunciado, tolerância ou esperado); entram no anexo
«achados fora do pré-registro» do RESULTADO_KERNEL.json da rodada 2. -/

/-- [rodada 2, auxiliar] D_t x = x ⟺ D_{−t} x = x, para QUAISQUER taxas e qualquer matriz (entrada a entrada:
    e^{−t·g}·x = x ⟺ t·g = 0 ∨ x = 0). -/
theorem dephase_fixed_iff_neg {n : Type} [Fintype n] [DecidableEq n] (g : n → n → ℝ) (t : ℝ)
    (x : Matrix n n ℂ) : dephase g t x = x ↔ dephase g (-t) x = x := by
  have key : ∀ (s : ℝ) (i j : n),
      (Real.exp (-(s * g i j)) : ℂ) * x i j = x i j ↔ (s * g i j = 0 ∨ x i j = 0) := by
    intro s i j
    constructor
    · intro h
      by_cases hx : x i j = 0
      · exact Or.inr hx
      · left
        have h1 : (Real.exp (-(s * g i j)) : ℂ) = 1 :=
          mul_right_cancel₀ hx (h.trans (one_mul (x i j)).symm)
        have h2 : Real.exp (-(s * g i j)) = 1 := by exact_mod_cast h1
        rw [Real.exp_eq_one_iff, neg_eq_zero] at h2
        exact h2
    · rintro (h | h)
      · rw [h, neg_zero, Real.exp_zero, Complex.ofReal_one, one_mul]
      · rw [h, mul_zero]
  constructor
  · intro h
    ext i j
    have hij := congrFun (congrFun h i) j
    simp only [dephase, Matrix.of_apply] at hij ⊢
    rcases (key t i j).mp hij with h1 | h1
    · exact (key (-t) i j).mpr (Or.inl (by rw [neg_mul, h1, neg_zero]))
    · exact (key (-t) i j).mpr (Or.inr h1)
  · intro h
    ext i j
    have hij := congrFun (congrFun h i) j
    simp only [dephase, Matrix.of_apply] at hij ⊢
    rcases (key (-t) i j).mp hij with h1 | h1
    · exact (key t i j).mpr (Or.inl (by rw [neg_mul, neg_eq_zero] at h1; exact h1))
    · exact (key t i j).mpr (Or.inr h1)

/-- [rodada 2, fora do pré-registro] «D atua» é lido no semigrupo PARA A FRENTE: ∃ t ∈ ℝ (a definição `dephasingActs`)
    equivale a ∃ t > 0, para QUAISQUER taxas — t = 0 é a identidade (`dephase_zero`) e um tempo negativo troca-se pelo
    simétrico (`dephase_fixed_iff_neg`). O inverso de D_t (fora do semigrupo) não é usado em B9. -/
theorem dephasingActs_iff_forward (g : Fin 2 → Fin 2 → ℝ) (θ : ℝ) :
    dephasingActs g θ ↔ ∃ t : ℝ, 0 < t ∧ dephase g t (rhoOut θ) ≠ rhoOut θ := by
  constructor
  · rintro ⟨t, ht⟩
    rcases lt_trichotomy t 0 with h | h | h
    · refine ⟨-t, by linarith, fun he => ht ?_⟩
      have h2 := (dephase_fixed_iff_neg g (-t) (rhoOut θ)).mp he
      rwa [neg_neg] at h2
    · rw [h, dephase_zero] at ht
      exact absurd rfl ht
    · exact ⟨t, h, ht⟩
  · rintro ⟨t, -, ht⟩
    exact ⟨t, ht⟩

/-- [rodada 2, auxiliar] a entrada (0, 1) de Q_θ. -/
theorem Qtheta_entry01 (θ : ℝ) : Qtheta θ 0 1 = -((Real.sin θ : ℂ) * (Real.cos θ : ℂ)) := by
  rw [Qtheta_eq]
  simp

/-- [rodada 2, fora do pré-registro] a OUTRA leitura de Q̂: 1 − F_θ(1) = Q_{−θ} (não Q_θ). -/
theorem one_sub_rhoOut_eq_Qtheta_neg (θ : ℝ) : 1 - rhoOut θ = Qtheta (-θ) := by
  have hC := Complex.sin_sq_add_cos_sq (θ : ℂ)
  rw [Qtheta_eq, rhoOut_eq, Real.sin_neg, Real.cos_neg]
  ext i j
  fin_cases i <;> fin_cases j <;> simp
  all_goals first | ring1 | linear_combination (-1 : ℂ) * hC

/-- [rodada 2, fora do pré-registro] o vazamento lido na outra leitura é o mesmo: Tr(ρ*·(1 − F_θ(1))) = sin²θ. -/
theorem leak_of_complement (θ : ℝ) : (rhoStar * (1 - rhoOut θ)).trace = (Real.sin θ : ℂ) ^ 2 := by
  rw [one_sub_rhoOut_eq_Qtheta_neg, leak_eq, Real.sin_neg, Complex.ofReal_neg, neg_sq]

/-- [rodada 2, fora do pré-registro] e o anticomutador também: {1 − F_θ(1), ρ*} = 0 ⟺ sin θ = 0 — B2.a não depende
    de qual das duas leituras de Q̂ se escolhe. -/
theorem anticomm_complement_zero_iff (θ : ℝ) :
    anticomm (1 - rhoOut θ) rhoStar = 0 ↔ Real.sin θ = 0 := by
  rw [one_sub_rhoOut_eq_Qtheta_neg, anticomm_zero_iff, Real.sin_neg, neg_eq_zero]

/-- [rodada 2, fora do pré-registro] as duas leituras de Q̂ coincidem ⟺ sin 2θ = 0 (só nos dois polos); fora deles
    diferem na entrada (0, 1): −sin θ·cos θ contra +sin θ·cos θ. -/
theorem Qtheta_eq_one_sub_rhoOut_iff (θ : ℝ) : Qtheta θ = 1 - rhoOut θ ↔ Real.sin (2 * θ) = 0 := by
  rw [one_sub_rhoOut_eq_Qtheta_neg, sin_two_mul_eq_zero_iff]
  constructor
  · intro h
    have h01 := congrFun (congrFun h 0) 1
    rw [Qtheta_entry01, Qtheta_entry01, Real.sin_neg, Real.cos_neg, Complex.ofReal_neg] at h01
    have h2 : (Real.sin θ : ℂ) * (Real.cos θ : ℂ) = 0 := by
      linear_combination (-(1 : ℂ) / 2) * h01
    have h3 : Real.sin θ * Real.cos θ = 0 := by exact_mod_cast h2
    exact mul_eq_zero.mp h3
  · rintro (h | h)
    · rw [Qtheta_eq, Qtheta_eq, Real.sin_neg, Real.cos_neg, h]
      ext i j
      fin_cases i <;> fin_cases j <;> simp
    · rw [Qtheta_eq, Qtheta_eq, Real.sin_neg, Real.cos_neg, h]
      ext i j
      fin_cases i <;> fin_cases j <;> simp

"""

PROBES = r"""
/-! ## 17'. Rodada 2 — sondas dos termos da seção 15' (os dois lados de cada ⟺) -/

/-- [sonda, rodada 2] `dephase_fixed_iff_neg`: os dois lados VERDADEIROS (ρ*, t = ±1) e os dois FALSOS
    (F_{π/4}(1), t = ±1), com as taxas unitárias. -/
theorem probe_fixed_neg_both_sides :
    (dephase unitRates 1 rhoStar = rhoStar ∧ dephase unitRates (-1) rhoStar = rhoStar)
    ∧ (dephase unitRates 1 (rhoOut (Real.pi / 4)) ≠ rhoOut (Real.pi / 4)
      ∧ dephase unitRates (-1) (rhoOut (Real.pi / 4)) ≠ rhoOut (Real.pi / 4)) := by
  obtain ⟨hg0, h01, h10⟩ := unitRates_spec
  have hA : dephase unitRates 1 (rhoOut (Real.pi / 4)) ≠ rhoOut (Real.pi / 4) := by
    intro he
    have hr := (dephased_rank_two_iff (Real.pi / 4) unitRates hg0 h01 h10 one_pos).mpr probe_angles.1
    rw [he, (fractal_one_is_rank_one _).1] at hr
    exact absurd hr (by norm_num)
  refine ⟨⟨dephase_rhoStar unitRates hg0 1, dephase_rhoStar unitRates hg0 (-1)⟩, hA, fun he => hA ?_⟩
  have h2 := (dephase_fixed_iff_neg unitRates (-1) (rhoOut (Real.pi / 4))).mp he
  rwa [neg_neg] at h2

/-- [sonda, rodada 2] `dephasingActs_iff_forward`: θ = π/4 (atua num t > 0) e θ = 0 (nenhum t > 0 atua). -/
theorem probe_forward_both_sides :
    (∃ t : ℝ, 0 < t ∧ dephase unitRates t (rhoOut (Real.pi / 4)) ≠ rhoOut (Real.pi / 4))
    ∧ ¬ ∃ t : ℝ, 0 < t ∧ dephase unitRates t (rhoOut 0) ≠ rhoOut 0 := by
  obtain ⟨-, -, -, -, h1, h2⟩ := probe_endpoint_both_sides
  exact ⟨(dephasingActs_iff_forward unitRates _).mp h1,
    fun h => h2 ((dephasingActs_iff_forward unitRates 0).mpr h)⟩

/-- [sonda, rodada 2] `anticomm_complement_zero_iff`: os dois lados (θ = 0 nulo; θ = π/4 não nulo). -/
theorem probe_complement_anticomm_both_sides :
    anticomm (1 - rhoOut 0) rhoStar = 0 ∧ anticomm (1 - rhoOut (Real.pi / 4)) rhoStar ≠ 0 := by
  have hs : Real.sin (Real.pi / 4) ≠ 0 := by
    rw [Real.sin_pi_div_four]
    positivity
  exact ⟨(anticomm_complement_zero_iff 0).mpr Real.sin_zero,
    fun h => hs ((anticomm_complement_zero_iff _).mp h)⟩

/-- [sonda, rodada 2] `Qtheta_eq_one_sub_rhoOut_iff`: em θ = 0 as duas leituras de Q̂ coincidem; em θ_M
    (c : TGLCoupling, habitada por `probe_coupling`) diferem. -/
theorem probe_two_readings_of_Q (c : TGLCoupling) :
    Qtheta 0 = 1 - rhoOut 0 ∧ Qtheta (thetaMiguel c.beta) ≠ 1 - rhoOut (thetaMiguel c.beta) := by
  refine ⟨(Qtheta_eq_one_sub_rhoOut_iff 0).mpr (by simp), fun h => ?_⟩
  rcases (sin_two_mul_eq_zero_iff _).mp ((Qtheta_eq_one_sub_rhoOut_iff _).mp h) with h3 | h3
  · exact sin_mul_cos_thetaMiguel_ne_zero c (by rw [h3, zero_mul])
  · exact sin_mul_cos_thetaMiguel_ne_zero c (by rw [h3, mul_zero])
"""

for bloco in (SEC15, PROBES):
    if '"' in bloco:
        raise SystemExit("FALHA VISIVEL: bloco de codigo com aspas duplas")
ANC16 = "/-! ## 16. Os CONTROLES C1–C14"
if r2a.count(ANC16) != 1:
    raise SystemExit("FALHA VISIVEL: ancora da secao 16 nao unica")
FIM = "\nend\n\nend TGLExt.TheUnitIsTheRank\n"
if not r2a.endswith(FIM) or r2a.count(FIM) != 1:
    raise SystemExit("FALHA VISIVEL: o fim do arquivo nao e o esperado")
r2 = r2a.replace(ANC16, SEC15 + ANC16, 1)
r2 = r2[: len(r2) - len(FIM)] + PROBES + FIM
# conferencia: retirar exatamente os dois blocos devolve r2a
volta = r2.replace(SEC15, "", 1)
volta = volta[: len(volta) - len(FIM) - len(PROBES)] + FIM
if volta != r2a:
    raise SystemExit("FALHA VISIVEL: retirar os blocos acrescentados nao devolve r2a")
if '"' in r2:
    raise SystemExit("FALHA VISIVEL: a pedra r2 tem aspas duplas")
strip_lean_comments(r2)  # falha se algum bloco de comentario nao fecha

os.makedirs(DEST_DIR, exist_ok=True)
nb = r2.encode("utf-8")
tent = None
if os.path.exists(DEST):
    k = 1
    while os.path.exists(DEST + ".tentativa%02d" % k):
        k += 1
    tent = DEST + ".tentativa%02d" % k
    os.replace(DEST, tent)
with open(DEST + ".tmp", "wb") as f:
    f.write(nb)
os.replace(DEST + ".tmp", DEST)
if open(DEST, "rb").read() != nb:
    raise SystemExit("FALHA VISIVEL: a pedra gravada difere do texto montado")
decl_re = re.compile(r"^(theorem|def)\s+([A-Za-z_][A-Za-z0-9_'.]*)", re.M)
novas = [m.group(2) for m in decl_re.finditer(SEC15 + PROBES)]
rec = {
    "documento": "MONTAGEM da pedra candidata TheUnitIsTheRank, RODADA 2",
    "autor": "construtor do kernel (subagente), rodada 2 (reinvocacao da gerencia c1, 12/10/2026 noite)",
    "rodada1": {"arquivo": ORIG, "bytes": len(ob), "sha256": sha(ob), "intocada": True},
    "r2a_so_comentarios": {"bytes": len(r2a.encode("utf-8")), "sha256": sha(r2a.encode("utf-8")),
                           "codigo_sem_comentarios_identico_a_rodada1": cod_o == cod_a,
                           "codigo_sem_comentarios_sha256": sha(cod_o.encode("utf-8"))},
    "r2": {"arquivo": DEST, "bytes": len(nb), "sha256": sha(nb), "linhas": r2.count("\n"),
           "retirar_blocos_devolve_r2a": volta == r2a,
           "codigo_sem_comentarios_sha256": sha(strip_lean_comments(r2).encode("utf-8"))},
    "notas_cabecalho": 8, "notas_docstrings": log_notas,
    "v4_citacao_antiga_rodada1": v4_antigo,
    "declaracoes_acrescentadas": novas,
    "tentativa_anterior_preservada_em": tent,
    "estatuto": "[REAL medido aqui] so comentarios mudam em r2a; r2 = r2a + secao 15' + sondas 17'; a rodada 1 fica "
                "intacta em 3_KERNEL como registro; instalar e nomear sao atos da v392 (gerencia e operador)",
}
k = 1
while os.path.exists(os.path.join(R2, "MONTAGEM_PEDRA_R2_t%02d.json" % k)):
    k += 1
with open(os.path.join(R2, "MONTAGEM_PEDRA_R2_t%02d.json" % k), "w", encoding="utf-8") as f:
    f.write(json.dumps(rec, ensure_ascii=False, indent=1))
print(json.dumps(rec, ensure_ascii=False, indent=1))
