# -*- coding: utf-8 -*-
# CANDIDATA CORRIGIDA (SO DOCSTRINGS) da pedra TheUnitIsTheRank — redator da F1.FREQUENCIA, 12/10/2026.
# Le a pedra ORIGINAL de 3_KERNEL (so leitura; ela fica intocada como registro), aplica substituicoes EXATAS, cada uma
# conferida como unica, e grava a candidata em 4_RELATORIO\L\TGLExt\TheUnitIsTheRank.lean. Depois confere, com um
# leitor de comentarios no grammar do Lean 4 (bloco /- -/ ANINHADO e linha --), que o CODIGO sem comentarios e
# byte a byte o mesmo da original: so o texto de comentario/docstring muda; nenhum enunciado, prova ou nome muda.
# O que entra: os achados das duas auditorias (citacoes de V4 pelos bytes; rotulos [KNOWN]; homonimo de B9.c; os
# dois polos; a leitura seletiva; o titulo no atomo; o Tudo de uma passagem). Correcao AO LADO: o texto antigo fica,
# salvo as duas citacoes de V4, trocadas pelos bytes com a nota do que eram.
import os, sys, json, hashlib, re

BASE = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
ORIG = os.path.join(BASE, "3_KERNEL", "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
DEST_DIR = os.path.join(BASE, "4_RELATORIO", "L", "TGLExt")
DEST = os.path.join(DEST_DIR, "TheUnitIsTheRank.lean")
REC = os.path.join(BASE, "4_RELATORIO", "CORRECAO_DOCSTRINGS.json")
ORIG_SHA_ESPERADO = "617155151fb0d9e110a4beda34f5f6cd40dd4636c6e0da13a3938f3ad1e08464"
# tentativa 2 (12/10): + E25 e E26 (re-exportacoes que a auditoria de estatuto apontou sem rotulo); a tentativa 1 fica em tentativasndidata_tentativa1

AO = "\u26a0 AO LADO (12/10/2026, redator da F1.FREQUENCIA"

R = []  # (rotulo, antigo, novo)

R.append(("E1_titulo_no_atomo",
"""   NÃO instalada no Nós — instalar é ato da v392]
""",
"""   NÃO instalada no Nós — instalar é ato da v392]
  [""" + AO + """; achado da auditoria de estatuto): o título diz mais que a pedra.
   A tese «a unidade é o posto» vale NO ÁTOMO (B1: Tr ρ* = posto ρ* = 1; P4: nome e índice só coincidem em d = 1);
   no ponto final da defasagem o posto é 2 (`rank_not_preserved_by_dephasing`) e traço 1 não dá posto 1
   (`trace_one_not_rank_one`). O nome definitivo da pedra é do operador.]
"""))

R.append(("E2_V2_latex_e_pessoa",
"""  mesma passagem reafirmada, com a fórmula ρ = |ψ⟩⟨ψ|, Tr ρ = 1 e Tr ρ² = 1 (l.16).
""",
"""  mesma passagem reafirmada, com a fórmula ρ = |ψ⟩⟨ψ|, Tr ρ = 1 e Tr ρ² = 1 (l.16; nos bytes ela está em LaTeX; a
  primeira pessoa aparece só em «Quando eu derivei» (l.12), na mesma frase de «você impôs»).
"""))

R.append(("E3_V4_pelos_bytes",
"""  do rank («Tudo = D_β(F(1))», «o vazamento … impede o anticomutador perfeito {Q̂, ρ*} = 0»).
""",
"""  do rank. l.13, nos bytes (LaTeX): «$$ \\text{Tudo} = D_\\beta(F(1)) $$» (lê-se Tudo = D_β(F(1))); l.16, nos bytes:
  «Esse pequeno vazamento de fase é o que impede o anticomutador perfeito $\\{ \\hat{Q}, \\rho^* \\} = 0$.»
  [""" + AO + """; achado das duas auditorias): na versão `617155151fb0d9e1` desta pedra as duas
  citações de V4 eram paráfrase (LaTeX renderizado; a segunda, um recorte composto que começava dentro de «pequeno»);
  os bytes estão acima.]
"""))

R.append(("E4_rotulos_KNOWN",
"""  `LinearMap.finrank_range_add_finrank_ker`; Axler, LADR, Teo. 3.22): formalizados aqui como TERMO; o conteúdo segue
  sendo da literatura.
""",
"""  `LinearMap.finrank_range_add_finrank_ker`; Axler, LADR, Teo. 3.22): formalizados aqui como TERMO; o conteúdo segue
  sendo da literatura.
* `[KNOWN]` — """ + AO + """; achado da auditoria de estatuto): também é de livro-texto, formalizado aqui
  como TERMO: P² = P ⟹ Tr P = posto P (Mathlib `LinearMap.IsProj.trace`; B1.b); traço e posto invariantes por
  conjugação unitária (Mathlib `Matrix.trace_mul_cycle`, `Matrix.rank_mul_eq_left_of_isUnit_det`; B4.a); em M₂(ℂ),
  Tr M² = (Tr M)² − 2 det M (Cayley–Hamilton 2×2; P1.b); posto |ψ⟩⟨ψ| = 1 (P1.d); a compressão por projetor de posto 1
  e a leitura seletiva (G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951); P3.a); S(θ)ⁿ = S(nθ) é corolário de `Smat_mul`
  (SMatrix:81; B7.a1); a não convergência de sin²(nθ) com sin θ ≠ 0 é elementar (B7.a2). O PASSA é do TERMO.
"""))

R.append(("E5_regimes_e_uma_passagem",
"""hiperbólica de SL(2,ℝ) é [ONTO] (IALDJones) e não é afirmado aqui.
""",
"""hiperbólica de SL(2,ℝ) é [ONTO] (IALDJones) e não é afirmado aqui.

""" + AO + """; achados das auditorias): (i) o que `angular_leak_no_limit` prova é que a sequência
sin²(nθ) não converge quando sin θ ≠ 0, uma leitura do ângulo, não uma lei geral sobre todo observável angular; (ii) a
letra F designa nesta pedra F_θ = Ad S(θ); o `axiomFlow` F(t) = P + e^{−t}(1 − P) do lock (TheAxiomAndTheFalseWitness),
re-exportado em B9.c, é OUTRO objeto (ver `transmission_dephases_reexport`); (iii) o Tudo tipado aqui,
D_∞F_θM(1) = diag(1 − β, β), é ponto de UMA passagem: sob o canal iterado C = D∘Ad(S)∘D da F1.ATRATOR ele não é
estacionário (p₁: β ↦ 2β(1 − β)) e Cⁿ → I/2; β fixa a taxa λ = 1 − 2β, não o ponto fixo. Isso foi medido em runtime
pelas auditorias e pelo redator; não é termo desta pedra.
"""))

R.append(("E6_nao_afirma_atrator",
"""reservado e não move o gate. Validade na face testada não é creditação. Sem sorry, sem axiom.
""",
"""reservado e não move o gate. Validade na face testada não é creditação. Sem sorry, sem axiom.
""" + AO + """): nem que o ponto final de UMA passagem seja o atrator do canal iterado (este é I/2,
F1.ATRATOR), nem que o PASSA de B9.b seja a letra de V4 l.10 (a letra é FALSA em θ = 0).
"""))

R.append(("E7_qual_Q",
"""/-- Q_θ = S(θ)ᴴ·Q₀·S(θ) (pré-registro; = R·Q₀·Rᵀ do um.py, ver `Qtheta_eq_rot`). -/
""",
"""/-- Q_θ = S(θ)ᴴ·Q₀·S(θ) (pré-registro; = R·Q₀·Rᵀ do um.py, ver `Qtheta_eq_rot`).
    """ + AO + """; anexo A8 do ótico): este Q_θ NÃO é 1 − F_θ(1) = Q_{−θ}; os dois
    diferem fora da diagonal (norma de Frobenius 2√2·|sin θ cos θ|) e dão o mesmo vazamento Tr(ρ*·) = sin²θ; o texto
    da v392 diz qual dos dois é o Q̂ de V4. -/
"""))

R.append(("E8_traco_posto_KNOWN",
"""    (Mathlib `LinearMap.IsIdempotentElem.isProj_range`, `LinearMap.IsProj.trace`). -/
""",
"""    (Mathlib `LinearMap.IsIdempotentElem.isProj_range`, `LinearMap.IsProj.trace`). [KNOWN: traço de projeção = posto;
    o PASSA é do TERMO.] -/
"""))

R.append(("E9_compressao_Luders",
"""/-- [P3.a] P = |a⟩⟨a|: P·X·P = ⟨a, Xa⟩·P e Tr(P·X) = ⟨a, Xa⟩ — para TODO vetor a (a normalização não é usada). -/
""",
"""/-- [P3.a] P = |a⟩⟨a|: P·X·P = ⟨a, Xa⟩·P e Tr(P·X) = ⟨a, Xa⟩ — para TODO vetor a (a normalização não é usada).
    [KNOWN: G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951); o PASSA é do TERMO.] -/
"""))

R.append(("E10_leitura_seletiva",
"""/-- [P3.a] ⟨a, Xa⟩ ≠ 0 ⟹ P·X·P / ⟨a, Xa⟩ = P: a leitura devolve o posto. -/
""",
"""/-- [P3.a] ⟨a, Xa⟩ ≠ 0 ⟹ P·X·P / ⟨a, Xa⟩ = P: a leitura devolve o posto. (É a leitura SELETIVA de Lüders, normalizada
    pelo peso de Born ⟨a, Xa⟩; [KNOWN].) -/
"""))

R.append(("E11_atrator_seletiva",
"""    (I/2 é o estado fixo do canal da F1.ATRATOR — citado; o posto 1 volta pela LEITURA, não pelo atrator.) -/
""",
"""    (I/2 é o estado fixo do canal da F1.ATRATOR — citado; o posto 1 volta pela LEITURA, não pelo atrator.)
    """ + AO + """; auditoria de estatuto): a leitura é SELETIVA: devolve ρ* com peso de Born
    Tr(ρ*·I/2) = 1/2; a não seletiva devolveria a mistura. I/2 vem da F1.ATRATOR, pedra candidata ainda NÃO instalada
    (instala-se junto, na v392). -/
"""))

R.append(("E12_verdade_e_custo_ONTO",
"""/-- [P3.b] ρ = diag(1 − b, b): Tr(ρ*·ρ) = 1 − b e Tr(Q₀·ρ) = b. -/
""",
"""/-- [P3.b] ρ = diag(1 − b, b): Tr(ρ*·ρ) = 1 − b e Tr(Q₀·ρ) = b. («verdade» e «custo» são leituras [ONTO] do nome; a
    conta lê as duas entradas de diag(1 − b, b).) -/
"""))

R.append(("E13a_ad_trace_KNOWN",
"""/-- [B4.a] uᴴu = 1 ⟹ Tr(u ρ uᴴ) = Tr ρ. -/
""",
"""/-- [B4.a] uᴴu = 1 ⟹ Tr(u ρ uᴴ) = Tr ρ. [KNOWN: Mathlib `Matrix.trace_mul_cycle`; o PASSA é do TERMO.] -/
"""))

R.append(("E13b_ad_rank_KNOWN",
"""/-- [B4.a] uᴴu = 1 ⟹ posto(u ρ uᴴ) = posto ρ (lacuna L4 do levantamento, via Mathlib). -/
""",
"""/-- [B4.a] uᴴu = 1 ⟹ posto(u ρ uᴴ) = posto ρ (lacuna L4 do levantamento, via Mathlib). [KNOWN: Mathlib
    `Matrix.rank_mul_eq_left_of_isUnit_det` e `Matrix.rank_mul_eq_right_of_isUnit_det`; o PASSA é do TERMO.] -/
"""))

R.append(("E14_fractal_ONTO",
"""/-- [B4.b = B5.e(i)] F_θ(1) = ρ_out θ: posto 1, Tr 1, idempotente, hermitiana, pureza 1. -/
""",
"""/-- [B4.b = B5.e(i)] F_θ(1) = ρ_out θ: posto 1, Tr 1, idempotente, hermitiana, pureza 1. (Corolário de `ad_rank`,
    `ad_trace` e da pedra 116; «fractal» é leitura [ONTO] do nome.) -/
"""))

R.append(("E15_negativo_previsto",
"""/-- [B5.e(ii), NEGATIVO HONESTO] «para todo θ, posto D_∞ F_θ(1) = posto F_θ(1)» é FALSO; testemunha θ_M. -/
""",
"""/-- [B5.e(ii), NEGATIVO HONESTO] «para todo θ, posto D_∞ F_θ(1) = posto F_θ(1)» é FALSO; testemunha θ_M.
    (O desfecho já estava previsto no levantamento, R4: é negativo certificado, não descoberta.) -/
"""))

R.append(("E16_reexport_trace_diagExpect",
"""/-- [B5.e(ii)] o que sobrevive: Tr D_∞ F_θ(1) = Tr F_θ(1). -/
""",
"""/-- [B5.e(ii)] o que sobrevive: Tr D_∞ F_θ(1) = Tr F_θ(1). (Re-exportação de `trace_diagExpect`, CondExpect:114.) -/
"""))

R.append(("E17_leitor_diagonal",
"""/-- [B6.a] g_ii = 0: Tr(ρ*·D_t Q_θ) = sin²θ para todo t. -/
""",
"""/-- [B6.a] g_ii = 0: Tr(ρ*·D_t Q_θ) = sin²θ para todo t. (O leitor ρ* é diagonal e por isso cego ao dephasing; um
    leitor não diagonal vê o tempo: C10, `nondiagonal_reader_sees_time`.) -/
"""))

R.append(("E18_Smat_pow_corolario",
"""/-- [B7.a1] S(θ)ⁿ = S(nθ): iterar o ângulo é girar o ângulo. -/
""",
"""/-- [B7.a1] S(θ)ⁿ = S(nθ): iterar o ângulo é girar o ângulo. (Corolário de `Smat_mul`, SMatrix:81: a lei de grupo
    já estava no kernel.) -/
"""))

R.append(("E19_sem_limite_elementar",
"""    Prova: um limite L teria de valer 1/2 (recorrência de três termos) e satisfazer L = 4L(1 − L) (duplicação). -/
""",
"""    Prova: um limite L teria de valer 1/2 (recorrência de três termos) e satisfazer L = 4L(1 − L) (duplicação).
    (Elementar; é a leitura do ângulo NESTA sequência, não uma lei geral.) -/
"""))

R.append(("E20_dois_polos",
"""/-- [B8.a] θ = 0: Tr(ρ*Q₀) = 0, {Q₀, ρ*} = 0, F₀(1) = ρ* = D_t ρ* para todo t; posto 1; pureza 1. -/
""",
"""/-- [B8.a] θ = 0: Tr(ρ*Q₀) = 0, {Q₀, ρ*} = 0, F₀(1) = ρ* = D_t ρ* para todo t; posto 1; pureza 1.
    """ + AO + """; auditoria de estatuto): a não-defasagem tem DOIS polos, θ = 0 (β = 0,
    transmissão total) e θ = π/2 (β = 1, reflexão total), ambos de posto 1 (`dephasing_trivial_iff`,
    `dephasing_trivial_at_thetaMiguel`). Na tipagem da matriz-S, «o que não transmite» (V4 l.9) aponta θ = π/2; este
    ramo, θ = 0, é transmissão total. -/
"""))

R.append(("E21_anticomm_avaliacao",
"""/-- [B2.a] {Q_θ, ρ*} = 0 ⟺ sin θ = 0 (o anticomutador perfeito é exatamente o ramo θ = 0 mod π). -/
""",
"""/-- [B2.a] {Q_θ, ρ*} = 0 ⟺ sin θ = 0 (o anticomutador perfeito é exatamente o ramo θ = 0 mod π).
    """ + AO + """): é a AVALIAÇÃO exata que substitui o «=0 EXATO só em θ_M→0» do um.py v391
    (l.6502): com 0 < β < 1 (`TGLCoupling`), θ = 0 é excluído pela hipótese; não é limite «inalcançável». Nunca se pede
    limite ao ângulo. -/
"""))

R.append(("E22_inscricao_escolhida",
"""/-- [B9.b] a leitura de INSCRIÇÃO: D atua ⟺ |𝓣|² > 0 e |𝓡|² > 0 (transmite E vaza). -/
""",
"""/-- [B9.b] a leitura de INSCRIÇÃO: D atua ⟺ |𝓣|² > 0 e |𝓡|² > 0 (transmite E vaza). (O PASSA é desta leitura,
    escolhida pela gerência e coerente com o cânone; a letra de V4 l.10 é FALSA em θ = 0:
    `literal_transmission_does_not_force_dephasing`.) -/
"""))

R.append(("E23_inscricao_identidade",
"""/-- [B9.b] c : TGLCoupling: em θ_M D atua e (D_∞ F(1))₁₁ = β. -/
""",
"""/-- [B9.b] c : TGLCoupling: em θ_M D atua e (D_∞ F(1))₁₁ = β. («inscrição» é leitura [INPUT da gerência]; o valor em θ_M
    é identidade de θ_M := arcsin √β, sem poder discriminante.) -/
"""))

R.append(("E25_endpoint_eq_refaz",
"""/-- [B5.a] D_∞ F_θ(1) = diag(c², s²). -/
""",
"""/-- [B5.a] D_∞ F_θ(1) = diag(c², s²). (Refaz numa só igualdade `dephased_rhoOut_zero_zero` e
    `dephased_rhoOut_one_one`, GlobalLiftLadder:219 e 228; o novo aqui é o POSTO do ponto final, abaixo.) -/
"""))

R.append(("E26_dephased_trace_composicao",
"""/-- [B5.c] o traço é preservado em todo t. -/
""",
"""/-- [B5.c] o traço é preservado em todo t. (Composição de `dephase_preserves_trace`, TheTraceIsNotErasable:96,
    com `rhoOut_trace`.) -/
"""))

R.append(("E24_B9c_homonimo",
"""    «transmitir defasa» (05/10): F(t)(1 − P) = e^{−t}(1 − P) no fluxo do lock mínimo. -/
""",
"""    «transmitir defasa» (05/10): F(t)(1 − P) = e^{−t}(1 − P) no fluxo do lock mínimo.
    """ + AO + """; auditoria de estatuto): HOMÔNIMO. O «transmitir» daqui é o fluxo do lock
    P + e^{−t}(1 − P), que contrai AO posto P; o da sonda B9 é |𝓣|² da matriz-S, cujo dephasing de Schur SOBE o posto
    de 1 para 2. Não há lema-ponte entre os dois: este termo existe no kernel, mas não apoia a leitura B9.b. -/
"""))


def strip_lean_comments(s):
    """Remove comentarios no grammar do Lean 4: bloco /- -/ ANINHADO (inclui /-- e /-!) e linha -- ate o fim da linha.
    Sem literais de string ou char no arquivo (conferido: 0 aspas duplas); falha visivel se um bloco nao fecha."""
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


def sha(b):
    return hashlib.sha256(b).hexdigest()


ob = open(ORIG, "rb").read()
if sha(ob) != ORIG_SHA_ESPERADO:
    raise SystemExit("FALHA VISIVEL: a pedra original nao e a esperada")
if b"\r\n" in ob:
    raise SystemExit("FALHA VISIVEL: a original tem CRLF; este script supoe LF")
o = ob.decode("utf-8")
if '"' in o:
    raise SystemExit("FALHA VISIVEL: a original tem aspas duplas; o leitor de comentarios precisaria de strings")
novo = o
log = []
for rot, antigo, nv in R:
    for marca in ("-/", "/-"):
        acrescimo = nv.replace(antigo.rstrip("\n").rstrip(), "")
        if rot not in ("E7_qual_Q", "E8_traco_posto_KNOWN", "E9_compressao_Luders", "E10_leitura_seletiva",
                       "E11_atrator_seletiva", "E12_verdade_e_custo_ONTO", "E13a_ad_trace_KNOWN", "E13b_ad_rank_KNOWN",
                       "E14_fractal_ONTO", "E15_negativo_previsto", "E16_reexport_trace_diagExpect",
                       "E17_leitor_diagonal", "E18_Smat_pow_corolario", "E19_sem_limite_elementar", "E20_dois_polos",
                       "E21_anticomm_avaliacao", "E22_inscricao_escolhida", "E23_inscricao_identidade",
                       "E24_B9c_homonimo"):
            if marca in nv:
                raise SystemExit("FALHA VISIVEL: %s introduz %r" % (rot, marca))
    k = novo.count(antigo)
    if k != 1:
        raise SystemExit("FALHA VISIVEL: %s: o trecho antigo ocorre %d vezes (precisa ser 1)" % (rot, k))
    novo = novo.replace(antigo, nv)
    log.append({"rotulo": rot, "ocorrencias_do_antigo": k, "bytes_antes": len(antigo.encode("utf-8")),
                "bytes_depois": len(nv.encode("utf-8"))})
# nas docstrings de declaracao (/-- ... -/), o unico -/ admitido e o fechamento que ja existia: conferido abaixo pelo
# leitor de comentarios (codigo identico => nenhuma fronteira de comentario mudou).
cod_o = strip_lean_comments(o)
cod_n = strip_lean_comments(novo)
igual = (cod_o == cod_n)
os.makedirs(DEST_DIR, exist_ok=True)
nb = novo.encode("utf-8")
if os.path.exists(DEST):
    raise SystemExit("FALHA VISIVEL: destino ja existe (nao sobrescrevo): " + DEST)
open(DEST, "wb").write(nb)
rec = {"documento": "CORRECAO_DOCSTRINGS — candidata corrigida (so docstrings) da pedra TheUnitIsTheRank",
       "autor": "redator da F1.FREQUENCIA (subagente), 12/10/2026",
       "original": {"arquivo": ORIG, "bytes": len(ob), "sha256": sha(ob), "intocada": True},
       "candidata": {"arquivo": DEST, "bytes": len(nb), "sha256": sha(nb)},
       "substituicoes": log, "n_substituicoes": len(log),
       "codigo_sem_comentarios_identico": igual,
       "codigo_sem_comentarios_sha256": {"original": sha(cod_o.encode("utf-8")), "candidata": sha(cod_n.encode("utf-8"))},
       "linhas": {"original": o.count("\n"), "candidata": novo.count("\n")},
       "estatuto": "[REAL medido aqui] so comentario/docstring muda; nenhum enunciado, prova ou nome muda; a original "
                   "fica em 3_KERNEL como registro; instalar e nomear sao atos da v392 (gerencia e operador)"}
if os.path.exists(REC):
    raise SystemExit("FALHA VISIVEL: recibo ja existe (nao sobrescrevo): " + REC)
open(REC, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
print(json.dumps(rec, ensure_ascii=False, indent=1))
if not igual:
    raise SystemExit("FALHA VISIVEL: o codigo sem comentarios MUDOU")
