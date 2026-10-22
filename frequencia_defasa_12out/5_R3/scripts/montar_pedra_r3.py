# -*- coding: utf-8 -*-
r"""RODADA 3 da pedra candidata TheUnitIsTheRank (redator da gerencia c1, 13/10/2026) — SO nomes, comentarios e rotulos.
Le a pedra da RODADA 2 (3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean, SO LEITURA, sha256 3195ef8f...) e aplica
uma lista de EDICOES EXATAS (cada trecho antigo tem de ocorrer exatamente UMA vez). Depois confere, por script:
 (a) o codigo SEM comentarios de r3 e, byte a byte, o codigo sem comentarios de r2 apos as TRES renomeacoes
     (nothing_branch -> zero_angle_pole; reading_of_the_attractor_state -> selective_reading_of_half_identity;
      transmission_dephases_reexport -> axiomFlow_complement_decay_reexport) — logo nenhum enunciado nem prova muda;
 (b) nenhuma aspa dupla no arquivo; todo bloco de comentario fecha;
 (c) toda ocorrencia de um.py vem na forma «um.py v391 (`8e7b9927ceae64b8`) l.NNNN» (ou com intervalo l.NNNN–NNNN);
 (d) os nomes antigos nao sobrevivem em CODIGO (podem sobreviver em comentario, como registro da renomeacao).
Grava 5_R3\sandbox\TGLExt\TheUnitIsTheRank.lean e o recibo 5_R3\MONTAGEM_PEDRA_R3.json. Falha visivel em qualquer divergencia.
Nao escreve fora de 5_R3."""
import hashlib, json, os, re, sys, datetime

R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UNID = os.path.dirname(R3)
ORIG = os.path.join(UNID, "3_KERNEL", "rodada2", "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
ORIG_SHA = "3195ef8f0766384ca7d4d1ab2ddd7a9c3cdd28872957e4b8d0e72fa9f028a063"
DEST_DIR = os.path.join(R3, "sandbox", "TGLExt")
DEST = os.path.join(DEST_DIR, "TheUnitIsTheRank.lean")
UMPY = "um.py v391 (`8e7b9927ceae64b8`)"

RENOMEACOES = [
    ("nothing_branch", "zero_angle_pole"),
    ("reading_of_the_attractor_state", "selective_reading_of_half_identity"),
    ("transmission_dephases_reexport", "axiomFlow_complement_decay_reexport"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def strip_lean_comments(s):
    """Comentarios do Lean 4: bloco /- -/ ANINHADO (inclui /-- e /-!) e linha -- ate o fim da linha. Sem literais de
    string no arquivo (conferido: zero aspas duplas). Falha visivel se um bloco nao fecha."""
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
    raise SystemExit("FALHA VISIVEL: a pedra da rodada 2 nao e a esperada: " + sha(ob))
if b"\r\n" in ob or b'"' in ob:
    raise SystemExit("FALHA VISIVEL: a rodada 2 tem CRLF ou aspas duplas")
o = ob.decode("utf-8")

# ------------------------------------------------------------------------------------------------------ as edicoes
# Cada par (antigo, novo): o antigo ocorre EXATAMENTE uma vez em r2. Tudo o que muda esta em comentario/docstring,
# salvo os TRES identificadores renomeados (na linha de declaracao), conferidos em (a).
E = []

# (8) cabecalho: o titulo vale so no atomo; nome provisorio mantido; a nota da rodada 3
E.append((
r"""/-!
# A UNIDADE É O POSTO — pedra CANDIDATA da F1.FREQUENCIA (trilha POSTO)
  [SANDBOX da gerência c1, 12/10/2026; nome PROVISÓRIO (o operador pode renomear);
   NÃO instalada no Nós — instalar é ato da v392]
""",
r"""/-!
# A UNIDADE É O POSTO — pedra CANDIDATA da F1.FREQUENCIA (trilha POSTO)

**O título vale só no átomo; o traço sobrevive à defasagem, o posto não.**

  [SANDBOX da gerência c1, 12/10/2026; nome PROVISÓRIO `TheUnitIsTheRank`, MANTIDO na rodada 3 — o nome FINAL da pedra
   é do operador (relatório final da unidade, §10, item 1); NÃO instalada no Nós — instalar é ato da v392, por ordem do
   operador de 12/10 (`OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt`, sha16 `78ef70e6f9868281`,
   l.3: «as pedras do rank e do tempo entram na v392»), DEPOIS desta rodada]
  [⚠ AO LADO (13/10/2026 — RODADA 3, redator da gerência c1, em nome próprio; rodada pedida pela auditoria de estatuto
   da rodada 2): esta rodada muda SÓ nomes, comentários e rótulos — nenhum enunciado nem prova muda (conferido por
   script: o código sem comentários de r3 é o de r2 (`3195ef8f0766384c`) após as três renomeações, byte a byte; e os
   tipos das 190 declarações, impressos e hasheados no kernel, são os mesmos). Renomeações: `nothing_branch` →
   `zero_angle_pole` (o estado do polo θ = 0 é ρ*, o mesmo objeto de `rhoStar_unit`; o polo θ = π/2 é Q₀; os dois têm
   traço 1 e posto 1 — seção 14); `reading_of_the_attractor_state` → `selective_reading_of_half_identity` (o peso
   emprestado de atrator sai do nome; I/2 é `halfId`); `transmission_dephases_reexport` →
   `axiomFlow_complement_decay_reexport` (re-exportação sem peso no nome: o termo re-exportado é homônimo do B9 e não o
   apoia). Toda citação de linha do programa terminal passa à forma «um.py v391 (`8e7b9927ceae64b8`) l.NNNN»,
   conferida nos bytes por script; [KNOWN] sem citação de fonte passou a [DERIVED aqui]; a BASE de D ficou marcada [INPUT da gerência]; a
   cláusula `c : TGLCoupling` de `rank_not_preserved_by_dephasing` FICA (retirá-la mudaria o tipo do enunciado — ver a
   docstring). O pré-registro ADITIVO proposto fica como ADENDO congelado por hash em `5_R3`, SEM prova nova nesta
   rodada. A rodada 2 fica intacta em `3_KERNEL\rodada2` como registro.]
"""))

# (5) [KNOWN] sem citacao -> [DERIVED aqui]
E.append((
r"""* `[KNOWN]` — [⚠ AO LADO (rodada 2; achado da auditoria de estatuto da rodada 1)]: também são de livro-texto,
  formalizados aqui como TERMO: P² = P ⟹ Tr P = posto P (Mathlib `LinearMap.IsProj.trace`; B1.b); traço e posto
  invariantes por conjugação unitária (Mathlib `Matrix.trace_mul_cycle`, `Matrix.rank_mul_eq_left_of_isUnit_det`;
  B4.a); em M₂(ℂ), Tr M² = (Tr M)² − 2 det M (Cayley–Hamilton 2×2; P1.b); posto |ψ⟩⟨ψ| = 1 (P1.d); a compressão por
  projetor de posto 1 e a leitura seletiva (G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951); P3.a); S(θ)ⁿ = S(nθ),
  corolário de `Smat_mul` (SMatrix:81; B7.a1); a não convergência de sin²(nθ) com sin θ ≠ 0, elementar (B7.a2).
  O PASSA é do TERMO; o conteúdo segue sendo da literatura.
""",
r"""* `[KNOWN]` — [⚠ AO LADO (rodada 2; achado da auditoria de estatuto da rodada 1)]: também são de livro-texto,
  formalizados aqui como TERMO, cada um COM a sua citação: P² = P ⟹ Tr P = posto P (Mathlib `LinearMap.IsProj.trace`;
  B1.b); traço e posto invariantes por conjugação unitária (Mathlib `Matrix.trace_mul_cycle`,
  `Matrix.rank_mul_eq_left_of_isUnit_det`; B4.a); a compressão por projetor de posto 1 e a leitura seletiva
  (G. Lüders, Ann. Phys. (Leipzig) 8, 322 (1951); P3.a). O PASSA é do TERMO; o conteúdo segue sendo da literatura.
  [⚠ AO LADO (rodada 3): o que na rodada 2 estava neste rótulo SEM citação de fonte passou a `[DERIVED aqui]`, abaixo.]
* `[DERIVED aqui]` — [rodada 3] provados nesta pedra a partir do kernel e da Mathlib, sem fonte externa citada: em
  M₂(ℂ), Tr M² = (Tr M)² − 2 det M (`trace_sq_fin_two`, conta direta nas entradas; P1.b); posto |ψ⟩⟨ψ| = 1
  (`rankOne_density`, via Mathlib `Matrix.rank_vecMulVec_le`; P1.d); a leitura seletiva normalizada devolve o projetor
  (`reading_returns_the_post`, corolário de `compression_by_rank_one`; P3.a); S(θ)ⁿ = S(nθ) (`Smat_pow`, corolário de
  `Smat_mul`, SMatrix.lean l.81; B7.a1); a não convergência de sin²(nθ) com sin θ ≠ 0 (`angular_leak_no_limit`,
  elementar; B7.a2).
"""))

# (6) a base de D e [INPUT da gerencia]
E.append((
r"""* `[INPUT da gerência]` — os mapeamentos frase → objeto (pré-registro, seção b).
""",
r"""* `[INPUT da gerência]` — os mapeamentos frase → objeto (pré-registro, seção b).
* `[INPUT da gerência]` — [rodada 3; achado A5 da auditoria de estatuto da rodada 2] a BASE de D: a defasagem
  `dephase` e o seu limite `diagExpect` (kernel do Nós, Ergodicity.lean l.184 e CondExpect.lean l.87) atuam ENTRADA A
  ENTRADA na base canônica de `Fin 2`, que é a base de ρ* = diag(1, 0) — o canal de medição do cânone. O negativo
  B5.e(ii) (`rank_not_preserved_by_dephasing`) e os termos `endpoint_*`, `dephased_*` e `dephasingActs` valem NESSA
  base; numa base girada (Ad S(θ) ∘ D ∘ Ad S(θ)ᴴ) o posto 1 de F_θ(1) seria preservado — isso NÃO é provado aqui.
  Escolher a base é decisão de leitura, não teorema.
"""))

# (4) citacoes do um.py no cabecalho
E.append((
r"""* `[CONJECTURE ontológica]` (um.py l.6488) — «Tudo = D_β(F(1))»: aqui só o PONTO FINAL diag(cos²θ, sin²θ) e o seu posto.
""",
r"""* `[CONJECTURE ontológica]` (""" + UMPY + r""" l.6488–6489: `def fractal_dephasing_principle(ONE)` e o rótulo
  «[CONJECTURE ontologica; ancoras REAL]») — «Tudo = D_β(F(1))»: aqui só o PONTO FINAL diag(cos²θ, sin²θ) e o seu posto.
"""))
E.append((
r"""  citação de bytes; no um.py a forma é ASCII, l.6526: «Tudo = D_beta(F(1)) = VERDADE»; a de V4 está acima, em LaTeX.]
""",
r"""  citação de bytes; no """ + UMPY + r""" a forma é ASCII, l.6526: «Tudo = D_beta(F(1)) = VERDADE»; a de V4 está
  acima, em LaTeX.]
"""))

# resumo do cabecalho: o nome novo
E.append((
r"""* a leitura de posto 1: `compression_by_rank_one`, `reading_returns_the_post`, `reading_of_the_attractor_state`;
""",
r"""* a leitura de posto 1: `compression_by_rank_one`, `reading_returns_the_post`, `selective_reading_of_half_identity`
  (rodada 3: era `reading_of_the_attractor_state`);
"""))

# "NAO afirma": a base de D
E.append((
r"""θ = 0: `literal_transmission_does_not_force_dephasing`); nem qual das duas leituras de Q̂ é a de V4 (decisão do texto
da v392).
-/
""",
r"""θ = 0: `literal_transmission_does_not_force_dephasing`); nem qual das duas leituras de Q̂ é a de V4 (decisão do texto
da v392).
[⚠ AO LADO (rodada 3)]: nem que o posto 1 de F_θ(1) se perca em TODA base — o negativo B5.e(ii) é da base de ρ*, a base
de D, marcada [INPUT da gerência]; nem que os dois polos da não-defasagem sejam «nada»: são ρ* e Q₀, traço 1 e posto 1.
-/
"""))

# (4) citacoes do um.py nas definicoes
E.append((
r"""/-- ρ* = |0⟩⟨0| = diag(1, 0): o termo de `rhoOut` (`Matrix.single 0 0 1`); um.py l.6512. -/
""",
r"""/-- ρ* = |0⟩⟨0| = diag(1, 0): o termo de `rhoOut` (`Matrix.single 0 0 1`); """ + UMPY + r""" l.6512:
    `P = np.array([[1.0, 0.0], [0.0, 0.0]])`. -/
"""))
E.append((
r"""/-- Q₀ = 1 − ρ* (um.py l.6514). -/
""",
r"""/-- Q₀ = 1 − ρ* (""" + UMPY + r""" l.6514: `Q0 = np.eye(2) - P`). -/
"""))
E.append((
r"""/-- A matriz R do um.py (l.6518): `[[c, −s], [s, c]]`. -/
""",
r"""/-- A matriz R do """ + UMPY + r""" l.6518 (`R = np.array([[c, -s], [s, c]])`): `[[c, −s], [s, c]]`. -/
"""))
E.append((
r"""/-- Q_θ = S(θ)ᴴ·Q₀·S(θ) (pré-registro; = R·Q₀·Rᵀ do um.py, ver `Qtheta_eq_rot`).
""",
r"""/-- Q_θ = S(θ)ᴴ·Q₀·S(θ) (pré-registro; = R·Q₀·Rᵀ do """ + UMPY + r""" l.6518, `Qth = R @ Q0 @ R.T`; ver
    `Qtheta_eq_rot`).
"""))
E.append((
r"""/-- «D atua» (pré-registro): ∃ t, D_t F_θ(1) ≠ F_θ(1).
    (Para quaisquer taxas, ∃ t ∈ ℝ equivale a ∃ t > 0: `dephasingActs_iff_forward`, rodada 2.) -/
""",
r"""/-- «D atua» (pré-registro): ∃ t, D_t F_θ(1) ≠ F_θ(1).
    (Para quaisquer taxas, ∃ t ∈ ℝ equivale a ∃ t > 0: `dephasingActs_iff_forward`, rodada 2.)
    (D = `dephase` atua entrada a entrada na base canônica de `Fin 2`, a base de ρ*: BASE de D [INPUT da gerência],
    rodada 3 — ver o cabeçalho.) -/
"""))
E.append((
r"""/-- [B1.a] Tr ρ* = 1 (= ω(I) no runtime, um.py l.6513). -/
""",
r"""/-- [B1.a] Tr ρ* = 1 (= ω(I) no runtime, """ + UMPY + r""" l.6513: `omega_I = float(np.trace(P))`). -/
"""))
E.append((
r"""    [KNOWN: traço de projeção = posto; o PASSA é do TERMO.] -/
""",
r"""    [KNOWN: traço de projeção = posto — Mathlib `LinearMap.IsProj.trace`; o PASSA é do TERMO.] -/
"""))

# (5) reading_returns_the_post: [KNOWN] sem citacao -> [DERIVED aqui]; o homonimo «post» dito
E.append((
r"""/-- [P3.a] ⟨a, Xa⟩ ≠ 0 ⟹ P·X·P / ⟨a, Xa⟩ = P: a leitura devolve o posto.
    (É a leitura SELETIVA de Lüders, normalizada pelo peso de Born ⟨a, Xa⟩;
    [KNOWN].) -/
""",
r"""/-- [P3.a] ⟨a, Xa⟩ ≠ 0 ⟹ P·X·P / ⟨a, Xa⟩ = P: a leitura devolve o posto.
    (É a leitura SELETIVA de Lüders, normalizada pelo peso de Born ⟨a, Xa⟩;
    [DERIVED aqui] — corolário de `compression_by_rank_one`, onde Lüders 1951 está citado; a rodada 2 trazia aqui
    [KNOWN] sem citação própria. O `post` do nome é o POSTO: o projetor de posto 1 que a leitura devolve; é homônimo de
    `TheVerbSelectsTheAction.post`, outro objeto, sem lema que os ligue — o nome FICA, por ser resíduo do operador
    (relatório final, §10, item 6).) -/
"""))

# (2) reading_of_the_attractor_state -> selective_reading_of_half_identity
E.append((
r"""/-- [P3.b] A leitura ρ* aplicada ao estado atrator I/2 devolve ρ*: ρ*(I/2)ρ*/Tr(ρ*·I/2) = ρ*, com Tr = 1/2.
    (I/2 é o estado fixo do canal da F1.ATRATOR — citado; o posto 1 volta pela LEITURA, não pelo atrator.)
    [⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1)]: a leitura é
    SELETIVA: devolve ρ* com peso de Born Tr(ρ*·I/2) = 1/2; a não seletiva devolveria a mistura. I/2 vem da F1.ATRATOR,
    cujas pedras candidatas NÃO estão no kernel do Nós (consulta por nome, 12/10). -/
theorem reading_of_the_attractor_state :
""",
r"""/-- [P3.b] A leitura seletiva ρ* aplicada a I/2 (`halfId`) devolve ρ*: ρ*(I/2)ρ*/Tr(ρ*·I/2) = ρ*, com Tr = 1/2.
    (O posto 1 volta pela LEITURA. Que I/2 seja o estado fixo do canal da F1.ATRATOR é CITAÇÃO daquela unidade, não
    termo desta pedra.)
    [⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1)]: a leitura é
    SELETIVA: devolve ρ* com peso de Born Tr(ρ*·I/2) = 1/2; a não seletiva devolveria a mistura. I/2 vem da F1.ATRATOR,
    cujas pedras candidatas NÃO estão no kernel do Nós (consulta por nome, 12/10).
    [⚠ AO LADO (rodada 3; achado A6 da auditoria de estatuto da rodada 2)]: RENOMEADA de `reading_of_the_attractor_state`
    para `selective_reading_of_half_identity` — o nome antigo emprestava o peso de atrator a uma pedra que não está no
    kernel do Nós; o enunciado e a prova são os mesmos. Uma ponte com a pedra da F1.ATRATOR, se e quando instalada, é
    termo novo (não desta rodada). -/
theorem selective_reading_of_half_identity :
"""))

# (4) citacoes do um.py: Qtheta_eq_rot e anticomm_zero_iff
E.append((
r"""/-- A receita do um.py (l.6518): Q_θ = R·Q₀·Rᵀ é o mesmo objeto que S(θ)ᴴ·Q₀·S(θ). -/
""",
r"""/-- A receita do """ + UMPY + r""" l.6518 (`Qth = R @ Q0 @ R.T`): Q_θ = R·Q₀·Rᵀ é o mesmo objeto que
    S(θ)ᴴ·Q₀·S(θ). -/
"""))
E.append((
r"""    «{Q,rho*}=0 EXATO so' em theta_M->0» do um.py v391 (l.6502): com 0 < β < 1 (`TGLCoupling`) θ = 0 fica excluído pela
    hipótese; não é «limite inalcancavel» (um.py l.6515) — nunca se pede limite ao ângulo. -/
""",
r"""    «{Q,rho*}=0 EXATO so' em theta_M->0» do """ + UMPY + r""" l.6502: com 0 < β < 1 (`TGLCoupling`) θ = 0 fica
    excluído pela hipótese; não é «limite inalcancavel» (""" + UMPY + r""" l.6515) — nunca se pede limite ao
    ângulo. -/
"""))

# (6) secao 11: a base de D
E.append((
r"""/-! ## 11. B5 — o ponto final D_∞ F_θ(1) e o seu posto (a FACE tem limite) -/
""",
r"""/-! ## 11. B5 — o ponto final D_∞ F_θ(1) e o seu posto (a FACE tem limite; a BASE de D é a de ρ*, [INPUT da gerência],
    ver o cabeçalho) -/
"""))

# (7) c : TGLCoupling fica
E.append((
r"""/-- [B5.e(ii), NEGATIVO HONESTO] «para todo θ, posto D_∞ F_θ(1) = posto F_θ(1)» é FALSO; testemunha θ_M.
    (O desfecho estava previsto no levantamento, R4: é negativo
    certificado, não descoberta.) -/
theorem rank_not_preserved_by_dephasing (c : TGLCoupling) :
""",
r"""/-- [B5.e(ii), NEGATIVO HONESTO] «para todo θ, posto D_∞ F_θ(1) = posto F_θ(1)» é FALSO; testemunha θ_M.
    (O desfecho estava previsto no levantamento, R4: é negativo
    certificado, não descoberta.)
    [⚠ AO LADO (rodada 3; sonda S3 do auditor de reprodução da rodada 2)]: a cláusula `c : TGLCoupling` é SUPÉRFLUA
    para a conclusão (a testemunha θ = π/4 basta: `probe_endpoint_both_sides`), mas FICA nesta rodada — retirá-la
    mudaria o TIPO do enunciado (de ∀ c : TGLCoupling, ¬ ∀ θ … para ¬ ∀ θ …), e a rodada 3 não muda enunciado. A forma
    incondicional é candidata ao ADENDO (pré-registro aditivo). A testemunha θ_M é a escolhida por ser o ponto da
    teoria; a negação vale na BASE de D, marcada [INPUT da gerência] no cabeçalho. -/
theorem rank_not_preserved_by_dephasing (c : TGLCoupling) :
"""))

# (1) nothing_branch -> zero_angle_pole; os dois polos juntos pelos termos ja existentes
E.append((
r"""/-! ## 14. B8 — o ramo do nada (álgebra; «nada» não é termo) -/
""",
r"""/-! ## 14. B8 — os dois polos da não-defasagem: θ = 0 (ρ*) e θ = π/2 (Q₀) (álgebra; «nada» não é termo) -/
"""))
E.append((
r"""/-- [B8.a] θ = 0: Tr(ρ*Q₀) = 0, {Q₀, ρ*} = 0, F₀(1) = ρ* = D_t ρ* para todo t; posto 1; pureza 1.
    [⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1)]: a não-defasagem tem
    DOIS polos, θ = 0 (β = 0, transmissão total) e θ = π/2 (β = 1, reflexão total), ambos de posto 1
    (`dephasing_trivial_iff`, `dephasing_trivial_at_thetaMiguel`, `endpoint_rank_one_at_poles`). Na tipagem da
    matriz-S, «O que **não** transmite (o que não defasa)» (V4 l.9) aponta θ = π/2; este ramo, θ = 0, é transmissão
    total. -/
theorem nothing_branch :
""",
r"""/-- [B8.a] O POLO θ = 0: Tr(ρ*Q₀) = 0, {Q₀, ρ*} = 0, F₀(1) = ρ* = D_t ρ* para todo t; posto 1; pureza 1.
    [⚠ AO LADO (rodada 2; auditoria de estatuto da rodada 1)]: a não-defasagem tem
    DOIS polos, θ = 0 (β = 0, transmissão total) e θ = π/2 (β = 1, reflexão total), ambos de posto 1
    (`dephasing_trivial_iff`, `dephasing_trivial_at_thetaMiguel`, `endpoint_rank_one_at_poles`). Na tipagem da
    matriz-S, «O que **não** transmite (o que não defasa)» (V4 l.9) aponta θ = π/2; este ramo, θ = 0, é transmissão
    total.
    [⚠ AO LADO (rodada 3; achado A4 da auditoria de estatuto da rodada 2)]: RENOMEADA de `nothing_branch` para
    `zero_angle_pole` — o estado deste polo é ρ*, o MESMO objeto que B1 chama a unidade (`rhoStar_unit`); chamá-lo de
    nada era nome com peso errado. Os DOIS polos, JUNTOS, pelos termos que esta pedra já tem: em θ = 0, F₀(1) = ρ*
    (`rhoOut_zero`), fixo por D (`dephase_rhoStar`), traço 1 e posto 1 (`rhoStar_unit`); em θ = π/2, F_{π/2}(1) = Q₀
    (`rhoOut_pi_div_two`), fixo por D (`dephase_Q0`), traço 1 (`rhoOut_trace` em π/2) e posto 1
    (`fractal_one_is_rank_one` em π/2; `endpoint_rank_one_at_poles`); a reflexão total sem defasagem é C13
    (`leak_without_dephasing_at_half_pi`). A CONJUNÇÃO dos dois polos num só termo (como a sonda do auditor de estatuto,
    `nondephasing_poles_are_rank_one_units`, 6/6 no trio) é enunciado NOVO e fica para o ADENDO (pré-registro aditivo),
    não para esta rodada. A frase de V4 l.9 segue [ONTO]: sem identidade não é falta de posto. -/
theorem zero_angle_pole :
"""))

# (3) transmission_dephases_reexport -> axiomFlow_complement_decay_reexport (re-exportacao sem peso)
E.append((
r"""    liga os dois (consulta por texto, 12/10): este termo existe no kernel, mas não apoia a leitura B9.b. -/
theorem transmission_dephases_reexport {A : Type*} [Ring A] [Algebra ℂ A] {P : A}
""",
r"""    liga os dois (consulta por texto, 12/10): este termo existe no kernel, mas não apoia a leitura B9.b.
    [⚠ AO LADO (rodada 3; achado A7 da auditoria de estatuto da rodada 2)]: RENOMEADA de `transmission_dephases_reexport`
    para `axiomFlow_complement_decay_reexport` — re-exportação SEM peso no nome: o que o termo diz é só que o fluxo do
    lock `axiomFlow P t` multiplica o complemento 1 − P por e^{−t} (`TheVerbSelectsTheAction.transmission_dephases`,
    TheVerbSelectsTheAction.lean l.529; `TheAxiomAndTheFalseWitness.axiomFlow`, TheAxiomAndTheFalseWitness.lean l.104).
    A palavra transmissão sai do nome porque é homônima do |𝓣|² de B9 e não o apoia; a citação B9.c (CITADO_REAL) fica,
    sem outro peso. -/
theorem axiomFlow_complement_decay_reexport {A : Type*} [Ring A] [Algebra ℂ A] {P : A}
"""))

# ------------------------------------------------------------------------------------------------------ aplicar
for antigo, novo in E:
    for proib in ('"',):
        if proib in novo:
            raise SystemExit("FALHA VISIVEL: trecho novo com aspas duplas: " + novo[:60])
log = []
s = o
for k, (antigo, novo) in enumerate(E, 1):
    c = s.count(antigo)
    if c != 1:
        raise SystemExit("FALHA VISIVEL: edicao %d ocorre %d vezes: %r" % (k, c, antigo[:90]))
    s = s.replace(antigo, novo, 1)
    log.append({"edicao": k, "antigo_bytes": len(antigo.encode("utf-8")), "novo_bytes": len(novo.encode("utf-8")),
                "antigo_inicio": antigo[:70], "novo_inicio": novo[:70]})
r3 = s

# (a) codigo sem comentarios: r3 == r2 apos as tres renomeacoes
cod2 = strip_lean_comments(o)
cod3 = strip_lean_comments(r3)
cod2r = cod2
for a, b in RENOMEACOES:
    n_a = len(re.findall(r"\b" + re.escape(a) + r"\b", cod2))
    if n_a != 1:
        raise SystemExit("FALHA VISIVEL: %s ocorre %d vezes no codigo de r2 (esperado 1: so a declaracao)" % (a, n_a))
    cod2r = re.sub(r"\b" + re.escape(a) + r"\b", b, cod2r)
    if len(re.findall(r"\b" + re.escape(a) + r"\b", cod3)) != 0:
        raise SystemExit("FALHA VISIVEL: o nome antigo %s sobrevive no CODIGO de r3" % a)
    if len(re.findall(r"\b" + re.escape(b) + r"\b", cod3)) != 1:
        raise SystemExit("FALHA VISIVEL: o nome novo %s nao ocorre exatamente 1 vez no codigo de r3" % b)
codigo_igual = (cod2r == cod3)
if not codigo_igual:
    import difflib
    d = list(difflib.unified_diff(cod2r.split("\n"), cod3.split("\n"), lineterm="", n=1))
    raise SystemExit("FALHA VISIVEL: o codigo sem comentarios mudou alem das renomeacoes:\n" + "\n".join(d[:80]))

# (b) aspas e comentarios
if '"' in r3:
    raise SystemExit("FALHA VISIVEL: a pedra r3 tem aspas duplas")
if "\r" in r3:
    raise SystemExit("FALHA VISIVEL: CR na pedra r3")

# (c) toda ocorrencia de um.py na forma com versao e hash
ocorr = [m.start() for m in re.finditer(r"um\.py", r3)]
mal = [r3[p - 20:p + 60] for p in ocorr if not r3.startswith(UMPY, p)]
if mal:
    raise SystemExit("FALHA VISIVEL: um.py sem versao/hash: %r" % mal)
linhas_umpy = sorted(set(int(x) for x in re.findall(re.escape(UMPY) + r" l\.(\d{4})", r3)))

# ------------------------------------------------------------------------------------------------------ gravar
os.makedirs(DEST_DIR, exist_ok=True)
nb = r3.encode("utf-8")
tent = None
if os.path.exists(DEST):
    k = 1
    while os.path.exists(DEST + ".tentativa%02d" % k):
        k += 1
    tent = DEST + ".tentativa%02d" % k
    os.replace(DEST, tent)
tmp = DEST + ".tmp"
with open(tmp, "wb") as fh:
    fh.write(nb)
if os.path.getsize(tmp) != len(nb):
    raise SystemExit("FALHA VISIVEL: tamanho gravado difere")
os.replace(tmp, DEST)

rec = {
    "documento": "MONTAGEM da pedra candidata TheUnitIsTheRank, RODADA 3 (so nomes, comentarios e rotulos)",
    "autor": "redator da gerencia c1 (subagente), 13/10/2026, em nome proprio",
    "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "origem_r2": {"arquivo": ORIG, "bytes": len(ob), "sha256": sha(ob), "linhas": o.count("\n") + 1},
    "pedra_r3": {"arquivo": DEST, "bytes": len(nb), "sha256": sha(nb), "linhas": r3.count("\n") + 1},
    "tentativa_anterior_preservada": tent,
    "edicoes": log,
    "n_edicoes": len(E),
    "renomeacoes": [{"de": a, "para": b} for a, b in RENOMEACOES],
    "conferencias": {
        "codigo_sem_comentarios_r3_igual_a_r2_apos_renomeacoes": codigo_igual,
        "codigo_sem_comentarios_bytes_r2": len(cod2.encode("utf-8")),
        "codigo_sem_comentarios_bytes_r3": len(cod3.encode("utf-8")),
        "sha256_codigo_sem_comentarios_r2_renomeado": sha(cod2r.encode("utf-8")),
        "sha256_codigo_sem_comentarios_r3": sha(cod3.encode("utf-8")),
        "aspas_duplas_em_r3": 0,
        "ocorrencias_um_py": len(ocorr),
        "todas_na_forma_um_py_v391_hash": True,
        "linhas_do_um_py_citadas": linhas_umpy,
    },
    "leitura": "nenhum enunciado nem prova muda: fora de comentarios e docstrings, a unica diferenca entre r2 e r3 sao os "
               "tres identificadores renomeados na propria linha de declaracao (cada nome antigo ocorria 1 vez no codigo "
               "de r2 e 0 vezes no de r3; cada nome novo ocorre 1 vez no codigo de r3).",
}
with open(os.path.join(R3, "MONTAGEM_PEDRA_R3.json"), "w", encoding="utf-8") as fh:
    json.dump(rec, fh, ensure_ascii=False, indent=1)
print(json.dumps({k: rec[k] for k in ("pedra_r3", "n_edicoes", "conferencias")}, ensure_ascii=False, indent=1))
