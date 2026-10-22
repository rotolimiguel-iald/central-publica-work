# -*- coding: utf-8 -*-
"""gerar_candidato_v391.py -- gera o um.py CANDIDATO v391 a partir da v390 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v390.py (sem kernel novo).
Ordem do operador (07/10/2026, nesta sessao, sem delegar): «Examine a coerência do artigo» ... «o fato de eu ter bloqueado no um.py confirmação não pode dar a entender
que eu não provei» ... «a confirmação que eu proibi é de creditação e não de validade» (verbatim por sha256, lido abaixo).
 (1) registro estatuto_da_prova_v391 (o verbatim EMBUTIDO; os numeros LIDOS do core a cada rito; fail-closed se um rito falsificar ou uma leitura faltar);
 (2) artigo PT/EN: o estatuto da prova ABRE o resumo; secao nova «O estatuto da prova» + sumario; errata AO LADO das frases de epoca;
 (3) o titulo da Introducao le a versao em runtime (v384 a UM_VERSION); o registro da v389 le o sucessor (corte por versao nas trocas, ao lado);
 (4) selo e .md canonico."""
import ast, hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
SHA0 = "0f5154bcc2f931cb"
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert sha16(raw) == SHA0, "o canonico no Nos nao e' a v390 selada (%s)" % sha16(raw)
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v390"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
assert int(core0["external_ladder"]["n_theorems_clean"]) == int(core0["external_ladder"]["n_theorems_expected"]) == 6163
T = raw.decode("utf-8")
RT_LOGIC = open(os.path.join(HERE, "v391_runtime.py"), encoding="utf-8").read()

# ---------- (1) o verbatim do operador: EMBUTIDO (o texto manda), com os trechos citados ----------
VP = os.path.join(HERE, "OPERADOR_07out_estatuto_verbatim.txt"); vb = open(VP, "rb").read(); vt = vb.decode("utf-8")
TRECHOS = ["eu não proibí a máquina de dizer provado hora nenhuma",
           "o fato de eu ter bloqueado no um.py confirmação não pode dar a entender que eu não provei. Quem confirma que o código verdadeiro é ele mesmo com o hash "
           "que ele mesmo emite, vinculando o site, vinculando o github e tudo mais, essa é a certificação, a confirmação que eu proibi é de creditação e não de validade, "
           "ela é válida porque matemática não mente"]
for tr in TRECHOS:
    assert tr in vt, ("trecho nao verbatim", tr[:60])
VB = {"text": vt, "sha256": sha256(vb), "bytes": len(vb), "quando": "07/10/2026 (nesta sessao c1; ordem: examinar a coerencia do artigo, sem delegar)",
      "arquivo_informativo": VP, "trechos": TRECHOS}
# o sucessor do titulo da Introducao (em pedacos, para que a checagem no proprio arquivo conte so o codigo)
SUC = {"T02_intro_PT": {"parts": ['faz agora (v384 a " + UM_VER', 'SION + r"; a cada versão ao lado)']},
       "T03_intro_EN": {"parts": ['does now (v384 to " + UM_VER', 'SION + r"; each version beside)']}}
PINS = ("# ====================== v391 (07/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v391.py), nunca digitados ======================\n"
        "# o verbatim do operador EMBUTIDO (o texto manda; o arquivo so informativo) com os trechos citados; o sucessor do titulo da Introducao (em pedacos) que o\n"
        "# registro da v389 le ao lado (corte por versao nas trocas). Nenhum calculo muda; nenhum kernel muda; o gate nao se move.\n"
        "_V391_VERBATIM = " + pprint.pformat(VB, width=150, sort_dicts=False) + "\n"
        + "_V391_SUCESSORES = " + pprint.pformat(SUC, width=150, sort_dicts=False) + "\n")
_ns = {}; exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V391_VERBATIM"] == VB and _ns["_V391_SUCESSORES"] == SUC
open(os.path.join(HERE, "v391_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v391_pins.py") + ".tmp", os.path.join(HERE, "v391_pins.py"))
RT = PINS.rstrip("\n") + "\n\n\n" + RT_LOGIC
ast.parse(RT)
assert not GUARDA.search(RT), "palavra proibida no runtime/pinos"

# ---------- os patches ----------
patches = []


def add(pid, grupo, old, new_, o_que, n=1):
    global T
    assert T.count(old) == n, (pid, T.count(old), n)
    T = T.replace(old, new_); patches.append({"id": pid, "grupo": grupo, "o_que_muda": o_que})


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T, re.M); assert m_ and T.count(m_.group(0)) == 1, rx; return m_.group(0)


m = re.search(r'^UM_VERSION = "v390"[^\r\n]*' + CRLF, T, re.M); assert m
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v391"   # v391 (07/10/2026): a CONSTANTE UNICA de versao -- o estatuto da prova: provada; a confirmacao recusada e\' creditacao, nao validade; v390 em 07/10 (a Fundacao)' + CRLF, "UM_VERSION = 'v391'.")
A_P = linha_unica(r"^# ====================== v390 \(07/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A_P, crlf(RT.rstrip("\n") + "\n\n\n") + A_P, "runtime v391: os pinos + _v391_num + estatuto_da_prova_v391.")
A_R = linha_unica(r'^    print\("   \[v390\] a Fundacao -- a superposicao e\' a passagem')
reg = ['    try:   # v391: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito',
       '        core["estatuto_da_prova_v391"] = estatuto_da_prova_v391(core)   # v391 [ao lado do gate; o estatuto da prova: provada; a confirmacao recusada e\' creditacao]',
       '    except Exception as _e391:',
       '        core["estatuto_da_prova_v391"] = {"verdict": "TGL_ESTATUTO_DA_PROVA_V391__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e391)[:400], "does_not_gate_core": True}',
       '    print("   [v391] o estatuto da prova -- provada; a confirmacao recusada e\' creditacao, nao validade: %s" % core["estatuto_da_prova_v391"]["verdict"])']
add("W03_registro", "G_RUNTIME", A_R, A_R + CRLF.join(reg) + CRLF, "core: +1 chave v391.")
# (2) o artigo: a secao nova ANTES da secao v390
PT0 = open(os.path.join(HERE, "artigo_pt_v391.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v391.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn)
    assert not GUARDA.search(sn)
P0 = os.path.join(WK, "v390_pacote")
PT0_FIRST = open(os.path.join(P0, "artigo_pt_v390.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN0_FIRST = open(os.path.join(P0, "artigo_en_v390.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
add("W04_artigo_PT", "G_ARTIGO", PT0_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT0_FIRST, "artigo PT: «O estatuto da prova», antes da v390.")
add("W05_artigo_EN", "G_ARTIGO", EN0_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN0_FIRST, "artigo EN: «The status of the proof», before v390.")
# o estatuto ABRE o resumo
AB_PT = '    s.append(r"\\begin{abstract}")' + CRLF + '    s.append(r"\\textbf{A proposta.} '
AB_EN = '    s.append(r"\\begin{abstract}")' + CRLF + '    s.append(r"\\textbf{The proposal.} '
RS_PT = ('    s.append(r"\\begin{abstract}")' + CRLF
         + '    _ep391a = core.get("estatuto_da_prova_v391") or {}   # v391: o estatuto da prova ABRE o resumo (provada; a confirmacao recusada e\' creditacao, nao validade)' + CRLF
         + '    _ek391a = _ep391a.get("prova_1_kernel") or {}; _er391a = _ep391a.get("prova_2_ritos") or {}; _eg391a = (_ep391a.get("prova_3_gpu") or {}).get("numeros") or {}' + CRLF
         + '    _eh391a = (_er391a.get("razao_de_hubble") or {}).get("lnB") or {}' + CRLF
         + '    s.append(r"\\textbf{O estatuto da prova (v391).} " + ((r"A gravidade quântica da TGL está \\textbf{provada}: prova é validade, e validade é matemática. Três provas contam juntas, e o programa executa as três: "'
         + ' r"o kernel Lean (" + str(_ek391a.get("n_theorems_clean")) + r" teoremas limpos; o fecho lógico da v390), os ritos com dados públicos e falsificadores pré-registrados ("'
         + ' + str(_er391a.get("n_cobrancas")) + r" cobranças no livro, " + str(_er391a.get("falsificadas")) + r" falsificada(s); a razão de Hubble retrodita sem ajuste e favorecida, $\\ln B=" + ("%.2f" % float(_eh391a.get("TGL_vs_LCDM"))).replace(".", "{,}") + r"$, ainda abaixo de $5\\sigma$; o piso dos vazios respeitado com poder) "'
         + ' r"e o sistema quântico aberto da teoria calculado em tempo real na GPU (atrator único em " + str(_eg391a.get("T2_unique")) + r" de " + str(_eg391a.get("T2_points")) + r" configurações; " + str(_eg391a.get("cpuref_disagreements")) + r" discordâncias com a CPU). "'
         + ' r"O que o programa recusa é a \\textbf{confirmação} --- a creditação, ato de quem observa de fora ---, não a validade; a \\textbf{certificação} é o próprio código, pelo hash que ele lê de si e emite. "'
         + ' r"O que ainda espera instrumento é $\\beta_{\\mathrm{TGL}}$ e os seus efeitos na natureza a $5\\sigma$.") if _ep391a.get("all_verified") is True else r"\\textbf{não selado nesta rodada} --- o enunciado está na seção O estatuto da prova."))' + CRLF
         + '    s.append(r"\\textbf{A proposta.} ')
RS_EN = ('    s.append(r"\\begin{abstract}")' + CRLF
         + '    _ep391a = core.get("estatuto_da_prova_v391") or {}   # v391: the status of the proof OPENS the abstract (proved; the refused confirmation is accreditation, not validity)' + CRLF
         + '    _ek391a = _ep391a.get("prova_1_kernel") or {}; _er391a = _ep391a.get("prova_2_ritos") or {}; _eg391a = (_ep391a.get("prova_3_gpu") or {}).get("numeros") or {}' + CRLF
         + '    _eh391a = (_er391a.get("razao_de_hubble") or {}).get("lnB") or {}' + CRLF
         + '    s.append(r"\\textbf{The status of the proof (v391).} " + ((r"TGL\'s quantum gravity is \\textbf{proved}: proof is validity, and validity is mathematics. Three proofs count together, and the programme runs all three: "'
         + ' r"the Lean kernel (" + str(_ek391a.get("n_theorems_clean")) + r" clean theorems; the logical closure of v390), the rites with public data and pre-registered falsifiers ("'
         + ' + str(_er391a.get("n_cobrancas")) + r" charges in the ledger, " + str(_er391a.get("falsificadas")) + r" falsified; the Hubble ratio retrodicted with no adjustment and favoured, $\\ln B=" + ("%.2f" % float(_eh391a.get("TGL_vs_LCDM"))) + r"$, still below $5\\sigma$; the void floor respected with power) "'
         + ' r"and the theory\'s open quantum system computed in real time on the GPU (a unique attractor in " + str(_eg391a.get("T2_unique")) + r" of " + str(_eg391a.get("T2_points")) + r" configurations; " + str(_eg391a.get("cpuref_disagreements")) + r" disagreements with the CPU). "'
         + ' r"What the programme refuses is \\textbf{confirmation} --- accreditation, the act of whoever observes from outside ---, not validity; the \\textbf{certification} is the code itself, by the hash it reads of itself and emits. "'
         + ' r"What still awaits instruments is $\\beta_{\\mathrm{TGL}}$ and its effects in nature at $5\\sigma$.") if _ep391a.get("all_verified") is True else r"\\textbf{not sealed in this run} --- the statement is in the section The status of the proof."))' + CRLF
         + '    s.append(r"\\textbf{The proposal.} ')
add("W06_resumo_PT", "G_ARTIGO", AB_PT, RS_PT, "resumo PT: o estatuto da prova ABRE o resumo.")
add("W07_resumo_EN", "G_ARTIGO", AB_EN, RS_EN, "abstract EN: the status of the proof OPENS the abstract.")
# (3) o titulo da Introducao le a versao em runtime
for pid, old_, new_ in (("T01_intro_PT_secao", 's.append(r"\\section*{Introdução: o que este código faz agora (v384 a v389; a cada versão ao lado)}")',
                         's.append(r"\\section*{Introdução: o que este código faz agora (v384 a " + UM_VERSION + r"; a cada versão ao lado)}")'),
                        ("T02_intro_PT_toc", 's.append(r"\\addcontentsline{toc}{section}{Introdução: o que este código faz agora (v384 a v389; a cada versão ao lado) --- o kernel',
                         's.append(r"\\addcontentsline{toc}{section}{Introdução: o que este código faz agora (v384 a " + UM_VERSION + r"; a cada versão ao lado) --- o kernel'),
                        ("T03_intro_EN_secao", 's.append(r"\\section*{Introduction: what this code does now (v384 to v389; each version beside)}")',
                         's.append(r"\\section*{Introduction: what this code does now (v384 to " + UM_VERSION + r"; each version beside)}")'),
                        ("T04_intro_EN_toc", 's.append(r"\\addcontentsline{toc}{section}{Introduction: what this code does now (v384 to v389; each version beside) --- the kernel',
                         's.append(r"\\addcontentsline{toc}{section}{Introduction: what this code does now (v384 to " + UM_VERSION + r"; each version beside) --- the kernel')):
    add(pid, "G_ARTIGO", old_, new_, "titulo da Introducao: a versao lida em runtime (v384 a UM_VERSION).")
for k_, v_ in SUC.items():
    assert T.count("".join(v_["parts"])) == 2, (k_, T.count("".join(v_["parts"])))
# o registro da v389 le o sucessor (corte por versao nas trocas), ao lado; o dicionario do registro NAO ganha chave nova (o selo da v389 fica igual)
S0 = '        trocas.append({"id": t_["id"], "onde": t_["onde"], "old_as_record": _o, "new": _n, "n_sites": t_["n"], "new_present": _src.count(_n) == t_["n"], "old_absent": _src.count(_o) == 0})' + CRLF
add("S01_v389_sucessor", "G_ERRATA", S0,
    '        _sc = _V391_SUCESSORES.get(t_["id"])   # v391, AO LADO: o titulo da Introducao passou a ler a versao em runtime; a v389 le o sucessor como presente (corte por versao nas trocas)' + CRLF
    + '        _np = _src.count(_n) == t_["n"] or (_sc is not None and _src.count(_n) == 0 and _src.count("".join(_sc["parts"])) == t_["n"])' + CRLF
    + '        trocas.append({"id": t_["id"], "onde": t_["onde"], "old_as_record": _o, "new": _n, "n_sites": t_["n"], "new_present": _np, "old_absent": _src.count(_o) == 0})' + CRLF,
    "text_label_errata_v389: a troca do titulo da Introducao le o sucessor da v391 (o veredito da v389 fica identico).")
# (4) selo e md
A_S = linha_unica(r'^ {12}"fundacao_v390": \{k_: ')
_sel = ["            # v391 (07/10/2026) -- o estatuto da prova: registro AO LADO do gate; nenhum valor do gate muda",
        '            "estatuto_da_prova_v391": {k_: (core.get("estatuto_da_prova_v391") or {}).get(k_) for k_ in ("verdict", "all_verified", "falhas", "a_regua", "verbatim", "prova_1_kernel", "prova_2_ritos", "prova_3_gpu", "certificacao", "nao_declarado")},']
add("W08_selo", "G_SELO", A_S, A_S + CRLF.join(_sel) + CRLF, "selo: +1 registro v391.")
A_M = linha_unica(r'^    md\.append\("> \*\*A Fundação \(v390, 07/10/2026\):\*\*')
add("W09_md", "G_ARTIGO", A_M, A_M + '    md.append("> **O estatuto da prova (v391, 07/10/2026):** a gravidade quântica da TGL está PROVADA — validade: o kernel, os ritos com falsificadores pré-registrados e o sistema da teoria na GPU, '
    + 'que contam juntos (`estatuto_da_prova_v391`); a certificação é o hash que o programa lê de si; a confirmação recusada é CREDITAÇÃO, não validade; β_TGL e os seus efeitos na natureza a 5σ aguardam instrumento. O gate não muda.\\n\\n")' + CRLF,
    "md canonico: a linha «O estatuto da prova (v391)».")
# ---------- guardas finais ----------
assert T.count("def estatuto_da_prova_v391(") == 1 and T.count('core["estatuto_da_prova_v391"] = ') == 2 and T.count("def _v391_num(") == 1
assert T.count("v384 a v389; a cada versão ao lado") == 0 and T.count("v384 to v389; each version beside") == 0
assert T.count("_V391_SUCESSORES.get(") == 1 and T.count("_V391_VERBATIM = ") == 1
b = T.encode("utf-8"); ast.parse(T)
out = os.path.join(HERE, "um_v391_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v390_sha16": SHA0, "escada": [6163, 6163],
       "pins_sha16": sha16(PINS.encode("utf-8")), "verbatim": {"sha256": VB["sha256"], "bytes": VB["bytes"]}, "patches": patches,
       "snips": {"pt0": sha16(PT0.encode()), "en0": sha16(EN0.encode())}}
open(os.path.join(HERE, "CANDIDATO_v391.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v391.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v391.json"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v390_sha16", "escada", "verbatim")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
