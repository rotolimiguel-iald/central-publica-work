# -*- coding: utf-8 -*-
"""Nomes e Verdade (13/10), PARTE 1: gera Posto.lean, Santo.lean e IALD.lean (novo) a partir das fontes ORIGINAIS pinadas
por sha. So namespace/modulo, nomes de teoremas listados e comentarios. Cada substituicao exige a contagem esperada de
ocorrencias (falha visivel). Nenhum enunciado e nenhuma prova e tocado; a prova disso e a leitura do kernel (comparar.py)."""
import os, re, sys, hashlib, json

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "C:/IALD/Central de Patentes/work"
ORIG = {
    "posto": (W + "/frequencia_defasa_12out/5_R3/sandbox/TGLExt/TheUnitIsTheRank.lean", "e95775d61db38633"),
    "santo": (W + "/tempo_santo_12out/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean", "4d8a82591badd010"),
    "iald": (W + "/organismo_iald_12out/7_R3_DOCSTRINGS/fonte/TGLExt/IALD.lean", "d7c1f1d3b03e6095"),
}
SAIDA = {"posto": AQUI + "/1_POSTO/Posto.lean", "santo": AQUI + "/2_SANTO/Santo.lean", "iald": AQUI + "/3_IALD/IALD.lean"}
VERBATIM = W + "/cunhagens_13out/OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt"
LOG = {}


def ler(chave):
    p, pref = ORIG[chave]
    b = open(p, "rb").read()
    assert hashlib.sha256(b).hexdigest().startswith(pref), chave
    return b.decode("utf-8")


def rep(txt, velho, novo, n=1, tag=""):
    c = txt.count(velho)
    if c != n:
        print("FALHA VISIVEL: contagem", tag or velho[:50], "esperado", n, "achado", c)
        sys.exit(2)
    return txt.replace(velho, novo)


def rep_re(txt, padrao, novo, n, tag):
    novo_txt, c = re.subn(padrao, novo, txt, flags=re.M)
    if c != n:
        print("FALHA VISIVEL: contagem regex", tag, "esperado", n, "achado", c)
        sys.exit(2)
    return novo_txt


vb = open(VERBATIM, "rb").read().decode("utf-8")
assert hashlib.sha256(open(VERBATIM, "rb").read()).hexdigest().startswith("0ddffcdb0a9c7b5e")
for q in ("rank=posto=nome", "tempo=relação modular=Santo", "organismo=IALD=Verbo Vivo"):
    assert q in vb, q

# ---------------------------------------------------------------- POSTO
t = ler("posto")
t = rep(t, "namespace TGLExt.TheUnitIsTheRank\n", "namespace TGLExt.Posto\n", 1, "ns posto")
t = rep(t, "end TGLExt.TheUnitIsTheRank\n", "end TGLExt.Posto\n", 1, "end posto")
# N2: o nome acima do termo
t = rep_re(t, r"\breading_weights_are_truth_and_cost\b", "rhoStar_and_Q0_traces_of_diag_one_sub_b_b", 1, "N2")
# N3: vocabulario reservado
t = rep_re(t, r"\binscription_at_thetaMiguel\b", "dephasing_acts_and_endpoint_entry_at_thetaMiguel", 1, "N3")
# N4: docstring de reading_returns_the_post
t = rep(t,
        "O `post` do nome é o POSTO: o projetor de posto 1 que a leitura devolve; é homônimo de",
        "O `post` do nome é o POSTO: a matriz |a⟩⟨a| que a leitura devolve (de posto 1 se a ≠ 0; PROJETOR só se\n"
        "    ⟨a, a⟩ = 1 — o TIPO deste termo não pede essa normalização: ressalva N4 da auditoria c1 `a1185ceb`); é homônimo de",
        1, "N4")
# docstring de B? (verdade/custo saem do nome; a leitura ONTO fica na docstring, marcada)
t = rep(t,
        "    («verdade» e «custo» são leituras [ONTO] do nome; a conta lê as\n    duas entradas de diag(1 − b, b).)",
        "    (A conta lê as duas entradas de diag(1 − b, b). [⚠ AO LADO (13/10, rodada de nomes; ressalva N2 da auditoria c1\n"
        "    `a1185ceb`): o nome antigo, `reading_weights_are_truth_and_cost`, trazia “verdade” e “custo” — leituras [ONTO],\n"
        "    não do termo; o termo é uma conta de entradas 2×2. “Verdade” e “custo” ficam como leituras [ONTO] do operador,\n"
        "    FORA do identificador.])",
        1, "N2doc")
t = rep(t,
        "# A UNIDADE É O POSTO — pedra CANDIDATA da F1.FREQUENCIA (trilha POSTO)\n",
        "# POSTO — pedra CANDIDATA da F1.FREQUENCIA (trilha POSTO), módulo `TGLExt.Posto`\n\n"
        "  [⚠ AO LADO (13/10/2026 — RODADA DE NOMES, construtor da gerência c1, em nome próprio; por decisão do operador, verbatim\n"
        "   sha16 `0ddffcdb0a9c7b5e`, `work\\cunhagens_13out\\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`):\n"
        "   «rank=posto=nome». A pedra, que se chamava `TheUnitIsTheRank` (título antigo: “A UNIDADE É O POSTO”, que a auditoria c1\n"
        "   `a1185ceb` achou maior que o termo, ressalva N1), passa a `TGLExt.Posto`. Esta rodada muda SÓ nomes: o namespace/módulo e\n"
        "   três identificadores — `reading_weights_are_truth_and_cost` → `rhoStar_and_Q0_traces_of_diag_one_sub_b_b` (N2),\n"
        "   `inscription_at_thetaMiguel` → `dephasing_acts_and_endpoint_entry_at_thetaMiguel` (N3) — e a docstring de\n"
        "   `reading_returns_the_post` (N4: sem “projetor”, porque o tipo não pede ⟨a, a⟩ = 1). NENHUM enunciado e NENHUMA prova muda:\n"
        "   a conferência é lida do kernel (tipo e termo de cada constante, módulo o prefixo e as duas renomeações), em\n"
        "   `work\\nomes_e_verdade_13out\\TABELA_INVARIANCIA.json`. O texto abaixo é o da r3 (`e95775d61db38633`), intacto como\n"
        "   registro, salvo os identificadores citados. Nome do módulo = decisão do operador; o conteúdo continua [REAL no sandbox],\n"
        "   NÃO instalado no Nós.]\n",
        1, "titulo posto")
open(SAIDA["posto"], "w", encoding="utf-8", newline="\n").write(t)
LOG["posto"] = hashlib.sha256(t.encode("utf-8")).hexdigest()

# ---------------------------------------------------------------- SANTO
t = ler("santo")
t = rep(t, "namespace TGLExt.TheTimeIsNotAPost\n", "namespace TGLExt.Santo\n", 1, "ns santo")
t = rep(t, "end TGLExt.TheTimeIsNotAPost\n", "end TGLExt.Santo\n", 1, "end santo")
n_print = len(re.findall(r"^#print axioms TGLExt\.TheTimeIsNotAPost\.", t, flags=re.M))
t = rep_re(t, r"^#print axioms TGLExt\.TheTimeIsNotAPost\.", "#print axioms TGLExt.Santo.", n_print, "print axioms")
REN = {
    "the_two_regimes_of_time": "isometry_dephasing_and_clock_conjunction",
    "the_face_lands": "dephase_tendsto_expectation_reexport",
    "face_clock_has_no_period": "decay_clock_has_no_period",
    "face_has_a_limit": "orbit_tendsto_center_reexport",
    "face_distinguishes_instants": "diagFlow_distinguishes_instants_reexport",
}
contagens = {}
for velho, novo in REN.items():
    c = len(re.findall(r"\b" + velho + r"\b", t))
    contagens[velho] = c
    if c == 0:
        print("FALHA VISIVEL: nome ausente", velho)
        sys.exit(2)
    t = re.sub(r"\b" + velho + r"\b", novo, t)
t = rep(t,
        "**isometry_dephasing_and_clock_conjunction** (nome da R1, mantido; só conjunção)",
        "**isometry_dephasing_and_clock_conjunction** (era `the_two_regimes_of_time`, nome da R1; só conjunção)",
        1, "doc conj")
t = rep(t,
        "# O TEMPO NÃO É POSTO — pedra CANDIDATA da unidade F1.TEMPO, rodada 2 (nome provisório `TheTimeIsNotAPost`)\n",
        "# SANTO — pedra CANDIDATA da unidade F1.TEMPO, rodada 2, módulo `TGLExt.Santo` (era `TheTimeIsNotAPost`: “O TEMPO NÃO É POSTO”)\n\n"
        "[⚠ AO LADO (13/10/2026 — RODADA DE NOMES, construtor da gerência c1, em nome próprio; por decisão do operador, verbatim sha16\n"
        "`0ddffcdb0a9c7b5e`, `work\\cunhagens_13out\\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`): «tempo=relação\n"
        "modular=Santo». O nome da pedra passa de `TheTimeIsNotAPost` a `TGLExt.Santo`; o nome do TEMPO na pedra é [ONTO] do operador\n"
        "(12/10: «não consigo nomear, senão como “santo”»), NÃO um termo: o conteúdo [REAL] segue sendo o que está provado abaixo.\n"
        "Esta rodada muda SÓ nomes: o namespace/módulo e cinco identificadores, pelas ressalvas do relatório R2 (A-R2-01 e N2) —\n"
        "`the_two_regimes_of_time` → `isometry_dephasing_and_clock_conjunction` (o termo é a conjunção de nove cláusulas; a\n"
        "identificação com os dois regimes da casa segue [OPEN]); `the_face_lands` → `dephase_tendsto_expectation_reexport`;\n"
        "`face_clock_has_no_period` → `decay_clock_has_no_period`; `face_has_a_limit` → `orbit_tendsto_center_reexport`;\n"
        "`face_distinguishes_instants` → `diagFlow_distinguishes_instants_reexport` (a palavra “face” sai dos nomes: é a do regime\n"
        "hiperbólico da casa). NENHUM enunciado e NENHUMA prova muda: a conferência é lida do kernel (tipo e termo de cada\n"
        "constante, módulo o prefixo e as cinco renomeações), em `work\\nomes_e_verdade_13out\\TABELA_INVARIANCIA.json`. Nunca citar\n"
        "“os dois regimes do tempo provados” nem “a face” como regime. O texto abaixo é o da R2 (`4d8a82591badd010`), intacto como\n"
        "registro, salvo os identificadores citados. NÃO instalada no Nós.]\n",
        1, "titulo santo")
open(SAIDA["santo"], "w", encoding="utf-8", newline="\n").write(t)
LOG["santo"] = hashlib.sha256(t.encode("utf-8")).hexdigest()
LOG["santo_contagens_renomeacao"] = contagens

# ---------------------------------------------------------------- IALD
t = ler("iald")
t = rep(t, "import TGLExt.TheUnitIsTheRank\n", "import TGLExt.Posto\n", 1, "imp rank")
t = rep(t, "import TGLExt.TheTimeIsNotAPost\n", "import TGLExt.Santo\n", 1, "imp tempo")
n1 = len(re.findall(r"TGLExt\.TheUnitIsTheRank\.", t))
n2 = len(re.findall(r"TGLExt\.TheTimeIsNotAPost\.", t))
t = rep_re(t, r"TGLExt\.TheUnitIsTheRank\.", "TGLExt.Posto.", n1, "qual rank")
t = rep_re(t, r"TGLExt\.TheTimeIsNotAPost\.", "TGLExt.Santo.", n2, "qual tempo")
LOG["iald_refs_qualificadas"] = {"Posto": n1, "Santo": n2}
n3 = len(re.findall(r"(?<![\w.])TheTimeIsNotAPost\.(?=\w)", t))
n4 = len(re.findall(r"(?<![\w.])TheUnitIsTheRank\.(?=\w)", t))
t = rep_re(t, r"(?<![\w.])TheTimeIsNotAPost\.(?=\w)", "Santo.", n3, "docref tempo")
t = rep_re(t, r"(?<![\w.])TheUnitIsTheRank\.(?=\w)", "Posto.", n4, "docref rank")
LOG["iald_refs_em_docstring"] = {"Posto": n4, "Santo": n3}
t = rep(t, "porque `TheTimeIsNotAPost` o importa;", "porque `TGLExt.Santo` (era `TheTimeIsNotAPost`) o importa;", 1, "linha57")
t = rep(t,
        "# TGLExt.IALD — o motor único (nome provisório; o nome é do operador) — RODADA 3 (13/10/2026), sandbox\n",
        "# TGLExt.IALD — IALD = Verbo Vivo — RODADA 4 (13/10/2026, rodada de NOMES), sandbox\n\n"
        "[⚠ AO LADO (13/10/2026 — RODADA DE NOMES, construtor da gerência c1, em nome próprio; por decisão do operador, verbatim sha16\n"
        "`0ddffcdb0a9c7b5e`, `work\\cunhagens_13out\\OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt`): «organismo=IALD=Verbo\n"
        "Vivo». O módulo continua `TGLExt.IALD`; o TÍTULO passa de “o motor único (nome provisório)” a “IALD = Verbo Vivo”; “Verbo Vivo”\n"
        "é leitura [ONTO] do operador sobre o organismo, não um termo. Os imports passam de `TGLExt.TheUnitIsTheRank` e\n"
        "`TGLExt.TheTimeIsNotAPost` a `TGLExt.Posto` e `TGLExt.Santo` (mesmo conteúdo de termo; ver a tabela de invariância de cada\n"
        "uma), e as referências qualificadas no código seguem os novos prefixos. NENHUM tipo e NENHUM termo desta pedra mudou em\n"
        "relação à r3 (`d7c1f1d3b03e6095`): a leitura do kernel está em `work\\nomes_e_verdade_13out\\TABELA_INVARIANCIA.json`\n"
        "(módulo `TGLExt.IALD`, o que muda nos termos é só o prefixo dos módulos importados). Em todo o texto abaixo, “único” do título\n"
        "antigo e os nomes `TheUnitIsTheRank`/`TheTimeIsNotAPost` são REGISTRO da r3. NÃO instalada no Nós.]\n",
        1, "titulo iald")
open(SAIDA["iald"], "w", encoding="utf-8", newline="\n").write(t)
LOG["iald"] = hashlib.sha256(t.encode("utf-8")).hexdigest()
json.dump(LOG, open(AQUI + "/medidas/GERAR_RENOMEADAS.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(LOG, ensure_ascii=False, indent=1))
