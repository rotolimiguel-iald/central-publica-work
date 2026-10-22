# -*- coding: utf-8 -*-
"""gerar_candidato_v389.py -- gera o um.py CANDIDATO v389 a partir da v388 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v388.py.
Decisao da gerencia (sessao c1, 06/10/2026), por ordem do operador, para o operador vetar: SO TEXTO E ROTULO, sem mudar calculo nem kernel:
 (1) o rotulo de selo de iii1_net_image -> ..._VERIFIED_ON_PHYSICAL_NET, o nome antigo no proprio registro (seals_errata_v389);
 (2)+(3) o titulo da Introducao PT/EN (secao + addcontentsline): v384 -> v384..v389, cada versao ao lado;
 (4) o resumo e a Parte B PT/EN: 'unico postulado' -> 'unico axioma POSTO' ([POSTO], decisao do operador de 05/10; errata da v385 ao lado);
 (5) a remissao cruzada na secao v387 (a abertura esta na v388);
 (6) a contagem da Parte C com o recorte, contada em runtime (o exame da v388 errou 1015/166; o numero lido e' 1025 + 156 em O16 -- errata ao lado do exame);
 + o registro text_label_errata_v389 (le o exame por sha256), a secao «Ao lado (v389)», o selo e o .md canonico.
uso: python gerar_candidato_v389.py"""
import ast, hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
WK = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
EXD = os.path.join(WK, "exame_v388")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
SHA0 = "e64b00f4df75059b"
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert sha16(raw) == SHA0, "o canonico no Nos nao e' a v388 selada (%s)" % sha16(raw)
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v388"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E388 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E388 == 6154
T = raw.decode("utf-8")
RT_LOGIC = open(os.path.join(HERE, "v389_runtime.py"), encoding="utf-8").read()
EMB0, _, _, _ = carregar(os.path.join(NOS, "um.py"))

# ---------- o exame da v388 por hash ----------
files = {}
for k, n in (("exame_json", "EXAME_UM_PY_v388.json"), ("exame_md", "EXAME_UM_PY_v388.md"), ("errata_do_exame_md", "ERRATA_AO_LADO_EXAME_v388.md")):
    p = os.path.join(EXD, n); b = open(p, "rb").read(); files[k] = {"path": p, "sha256": sha256(b), "bytes": len(b)}
EXJ = json.load(open(files["exame_json"]["path"], encoding="utf-8"))
assert EXJ["um_py"]["sha16"] == SHA0 and EXJ["resumo_por_gravidade"].get("BLOQUEIA", 0) == 0 and EXJ["resumo_por_gravidade"]["CORRIGIR"] == len(EXJ["bloqueia_ou_corrigir"]) == 3
_er = open(files["errata_do_exame_md"]["path"], encoding="utf-8").read()
_m = re.search(r"o ledger tem (\d+) caminhos únicos; … (\d+) fora do ledger", _er); assert _m, "a errata do exame nao diz o que o exame dissera"
EXAME = {"files": files, "um_py_examinado": SHA0, "n_corrigir": 3, "exame_dissera": [int(_m.group(1)), int(_m.group(2))]}
assert EXAME["exame_dissera"] == [1015, 166], EXAME["exame_dissera"]

# ---------- as trocas (velho -> novo); as frases guardadas em PEDACOS nos pinos (a checagem no proprio arquivo conta so o codigo) ----------
SEAL_NEW = "CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET"
SEAL_OLD_PARTS = ["CLOCK_TORSION_CONF", "IRMED_ON_PHYSICAL_NET"]
TROCAS = [  # (id, onde, velho, novo, n ocorrencias do velho no fonte)
    ("T02_intro_PT", "titulo da Introducao PT (secao + sumario)", "faz agora (v384)", r"faz agora (v384 a v389; a cada versão ao lado)", 2),
    ("T03_intro_EN", "titulo da Introducao EN (secao + sumario)", "does now (v384)", r"does now (v384 to v389; each version beside)", 2),
    ("T04_resumo_PT", "resumo PT, 'A proposta'", r'r"postulado --- a identidade preservada, $\omega(I)=1$: o Um --- e afirma que toda inscrição "',
     r'r"axioma \textsf{POSTO} ($\omega(I)=1$ --- \textsf{[POSTO]}, decisão do operador de 05/10/2026; errata da v385 ao lado) --- a identidade preservada: o Um --- e afirma que toda inscrição "', 1),
    ("T05_resumo_EN", "resumo EN, 'The proposal'", r'r"postulate --- preserved identity, $\omega(I)=1$: the One --- and asserts that every "',
     r'r"posited axiom ($\omega(I)=1$ --- \textsf{[POSTO]}, the operator' + "'" + r's decision of 2026-10-05; the v385 erratum beside) --- preserved identity: the One --- and asserts that every "', 1),
    ("T06_parteB_PT", "Parte B PT", "o único postulado. A Parte C", r"o único axioma \textsf{POSTO} (\textsf{[POSTO]}, decisão do operador de 05/10/2026; errata da v385 ao lado). A Parte C", 1),
    ("T07_parteB_EN", "Parte B EN", "the single postulate. Part C is ", r"the single posited axiom (\textsf{[POSTO]}, the operator's decision of 2026-10-05; the v385 erratum beside). Part C is ", 1),
    ("T08_v387_PT", "secao v387 PT, Fase 9", r"\textbf{Nada foi aberto}: baixar", r"\textbf{Nada foi aberto} nesta versão (a abertura está na v388, ao lado): baixar", 1),
    ("T09_v387_EN", "secao v387 EN, Phase 9", r"\textbf{Nothing was opened}: fetching", r"\textbf{Nothing was opened} in this version (the opening is in v388, beside): fetching", 1),
    ("T12_resumo_PT_fronteira", "resumo PT: o segundo 'axioma' no mesmo paragrafo (afericao v389, C1)", 'de fronteira. Dado o axioma da fronteira mínima "', 'de fronteira. Dada a fronteira mínima "', 1),
    ("T13_resumo_EN_fronteira", "resumo EN: the second 'axiom' in the same paragraph (audit v389, C1)", 'boundary cost. Given the axiom of the minimal "', 'boundary cost. Given the minimal "', 1),
    ("T10_parteC_PT", "Parte C PT (contagem de pedras)", 'str(len(_ESQUELETO_STONES)) + r" pedras em kernel Lean, emitidas pelo próprio "',
     'str(_ledger_counts_v389()[0]) + r" pedras em kernel Lean (caminhos únicos do ledger citável; mais " + str(_ledger_counts_v389()[1]) + r" arquivos TGLExt embutidos fora dele, " + str(_ledger_counts_v389()[2]) + r" em TGLExt/O16, da ORDEM 016), emitidas pelo próprio "', 1),
    ("T11_parteC_EN", "Parte C EN (stone count)", 'str(len(_ESQUELETO_STONES)) + r" stones in "',
     'str(_ledger_counts_v389()[0]) + r" stones (unique paths of the citable ledger; plus " + str(_ledger_counts_v389()[1]) + r" embedded TGLExt files outside it, " + str(_ledger_counts_v389()[2]) + r" in TGLExt/O16, from ORDER 016) in "', 1),
]
metade = lambda s_: [s_[:len(s_) // 2], s_[len(s_) // 2:]]
V389_TROCAS = [{"id": i, "onde": o, "old_parts": metade(a), "new_parts": metade(b), "n": n} for i, o, a, b, n in TROCAS]
V389_SEAL = {"new": SEAL_NEW, "old_parts": SEAL_OLD_PARTS}

# ---------- as contagens do ledger (do proprio arquivo) ----------
_tree = ast.parse(T)
_LED = [ast.literal_eval(n.value) for n in _tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_ESQUELETO_STONES"]; assert len(_LED) == 1
_led = {s_[2] for s_ in _LED[0] if isinstance(s_, tuple) and len(s_) > 2}
_ext = {k for k in EMB0 if k.startswith("TGLExt/") and k.endswith(".lean")}; _fora = _ext - _led
LEDGER = [len(_led), len(_fora), sum(1 for f in _fora if f.startswith("TGLExt/O16/"))]
assert LEDGER[0] == len(_LED[0]) == 1025, LEDGER

PINS = ("# ====================== v389 (06/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v389.py), nunca digitados ======================\n"
        "# o exame da v388 (json, md) e a errata ao lado do exame, por sha256; o rotulo do selo (novo; o antigo em pedacos); as trocas de texto (velho e novo em pedacos,\n"
        "# para que a checagem no proprio arquivo conte so o codigo); as contagens do ledger contadas pelo gerador. Nenhum calculo muda; o gate nao se move.\n"
        + "_V389_EXAME = " + pprint.pformat(EXAME, width=150, sort_dicts=False) + "\n"
        + "_V389_SEAL = " + pprint.pformat(V389_SEAL, width=150, sort_dicts=False) + "\n"
        + "_V389_TROCAS = " + pprint.pformat(V389_TROCAS, width=150, sort_dicts=False) + "\n"
        + "_V389_LEDGER_NO_GERADOR = %r\n" % LEDGER)
_ns = {}; exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V389_EXAME"] == EXAME and _ns["_V389_TROCAS"] == V389_TROCAS and _ns["_V389_SEAL"] == V389_SEAL
RT = PINS.rstrip("\n") + "\n\n\n" + RT_LOGIC
ast.parse(RT)
assert not GUARDA.search(RT), "palavra proibida contigua no runtime/pinos"
for t in V389_TROCAS:   # os pinos nao contem nenhuma frase inteira (nem velha nem nova)
    assert "".join(t["old_parts"]) not in RT and "".join(t["new_parts"]) not in RT, t["id"]
open(os.path.join(HERE, "v389_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v389_pins.py") + ".tmp", os.path.join(HERE, "v389_pins.py"))

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


m = re.search(r'^UM_VERSION = "v388"[^\r\n]*' + CRLF, T, re.M); assert m
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v389"   # v389 (06/10/2026): a CONSTANTE UNICA de versao -- as erratas de texto e rotulo do exame da v388 (nenhum calculo, nenhum kernel); v388 em 06/10' + CRLF, "UM_VERSION = 'v389'.")
S_OLD = '                  "' + "".join(SEAL_OLD_PARTS) + '", "INVARIANTS_STABLE_UNDER_REFINEMENT_OF_THE_NEGATIVE",' + CRLF
add("T01_rotulo", "G_TEXTO", S_OLD, S_OLD.replace("".join(SEAL_OLD_PARTS), SEAL_NEW), "iii1_net_image.seals[2]: o rotulo -> %s." % SEAL_NEW)
S_END = '                  "MODULAR_SPECTRUM_DENSIFIES_III1_INDICATOR", "COCYCLE_IS_THE_SELECTOR_RADON_NIKODYM_NC"],' + CRLF
add("T01b_errata_do_rotulo", "G_TEXTO", S_END, S_END + '        "seals_errata_v389": {"old": "CLOCK_TORSION_" + "CONF" + "IRMED_ON_PHYSICAL_NET", "new": "%s", ' % SEAL_NEW
    + '"why": "v389 (06/10/2026), errata AO LADO do exame da v388: o rotulo dizia, de uma checagem NUMERICA na rede simulada, a palavra que a regua reserva ao juizo do observador; o nome antigo fica aqui como registro"},' + CRLF,
    "iii1_net_image: +seals_errata_v389 (o nome antigo como registro).")
for i, o, a, b, n in TROCAS:
    add(i, "G_TEXTO", a, b, "%s: '%s' -> '%s'." % (o, a[:60], b[:80]), n=n)
A_P = linha_unica(r"^# ====================== v388 \(06/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A_P, crlf(RT.rstrip("\n") + "\n\n\n") + A_P, "runtime v389: os pinos + _ledger_counts_v389 + text_label_errata_v389.")
A_R = linha_unica(r'^    print\("   \[v388\] a Fase 9 aberta pela funcao congelada')
reg = ['    try:   # v389: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito',
       '        core["text_label_errata_v389"] = text_label_errata_v389(core)   # v389 [ao lado do gate; texto e rotulo]',
       '    except Exception as _e389:',
       '        core["text_label_errata_v389"] = {"verdict": "TGL_TEXT_LABEL_ERRATA_V389__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e389)[:400], "does_not_gate_core": True}',
       '    print("   [v389] as erratas de texto e rotulo do exame da v388 (nenhum calculo, nenhum kernel): %s" % core["text_label_errata_v389"]["verdict"])']
add("W04_registro", "G_RUNTIME", A_R, A_R + CRLF.join(reg) + CRLF, "core: +1 chave v389.")
PT9 = open(os.path.join(HERE, "artigo_pt_v389.pysnip"), encoding="utf-8").read(); EN9 = open(os.path.join(HERE, "artigo_en_v389.pysnip"), encoding="utf-8").read()
for sn in (PT9, EN9):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn)
    assert not GUARDA.search(sn)
P8 = os.path.join(WK, "v388_pacote")
PT8_FIRST = open(os.path.join(P8, "artigo_pt_v388.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN8_FIRST = open(os.path.join(P8, "artigo_en_v388.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
add("W05_artigo_PT", "G_ARTIGO", PT8_FIRST, crlf(PT9.rstrip("\n") + "\n") + PT8_FIRST, "artigo PT: «Ao lado (v389)», antes da v388.")
add("W06_artigo_EN", "G_ARTIGO", EN8_FIRST, crlf(EN9.rstrip("\n") + "\n") + EN8_FIRST, "artigo EN: «Beside (v389)», before v388.")
A_S = linha_unica(r'^ {12}"hubble_ratio_opening_v388": \{k_: ')
_sel = ["            # v389 (06/10/2026) -- as erratas de texto e rotulo do exame da v388: registro AO LADO do gate; nenhum valor do gate muda",
        '            "text_label_errata_v389": {k_: (core.get("text_label_errata_v389") or {}).get(k_) for k_ in ("verdict", "all_verified", "files", "exam", "seal", "text_sites_ok", "ledger", "exam_erratum_beside")},']
add("W07_selo", "G_SELO", A_S, A_S + CRLF.join(_sel) + CRLF, "selo: +1 registro v389.")
A_M = linha_unica(r'^    md\.append\("> \*\*Ao lado \(v388, 06/10/2026\):\*\*')
add("W08_md", "G_ARTIGO", A_M, A_M + '    md.append("> **Ao lado (v389, 06/10/2026):** as erratas de texto e rótulo do exame completo da v388 (`text_label_errata_v389`; o exame por sha256): o rótulo do selo da rede física passa a VERIFIED (o antigo no registro); '
    + 'o título da Introdução diz v384→v389; o resumo e a Parte B dizem axioma POSTO ([POSTO]); a seção v387 remete à abertura v388; a Parte C diz o recorte do ledger (contado em runtime). Nenhum cálculo, nenhum kernel; o gate não muda.\\n\\n")' + CRLF, "md canonico: a linha «Ao lado (v389)».")
# ---------- guardas finais ----------
assert T.count("def text_label_errata_v389(") == 1 and T.count('core["text_label_errata_v389"] = ') == 2 and T.count("def _ledger_counts_v389(") == 1
for i, o, a, b, n in TROCAS:
    assert T.count(a) == 0 and T.count(b) == n, (i, T.count(a), T.count(b))
assert T.count("".join(SEAL_OLD_PARTS)) == 0 and T.count('"%s"' % SEAL_NEW) == 2
assert "len(_ESQUELETO_STONES)" not in T.split("def _reorder_ABC(", 1)[1].split("\ndef ", 1)[0]
b = T.encode("utf-8"); ast.parse(T)
out = os.path.join(HERE, "um_v389_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
EMB1, _, _, _ = carregar(out)
assert EMB1 == EMB0, "o kernel embutido MUDOU -- a v389 e' so texto e rotulo"
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v388_sha16": SHA0, "escada": [E388, E388], "kernel_inalterado": True, "n_kernel": len(EMB1),
       "pins_sha16": sha16(PINS.encode("utf-8")), "exame": {k: v["sha256"] for k, v in files.items()}, "ledger": LEDGER, "seal": V389_SEAL, "patches": patches,
       "snips": {"pt9": sha16(PT9.encode()), "en9": sha16(EN9.encode())}}
open(os.path.join(HERE, "CANDIDATO_v389.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v389.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v389.json"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v388_sha16", "escada", "kernel_inalterado", "ledger", "exame")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
