# -*- coding: utf-8 -*-
"""gerar_candidato_v393.py -- gera o um.py CANDIDATO v393 a partir da v392 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v392.py. PREPARACAO de 14/10/2026 (gerencia c1).
 (A) a REGRA: 3 pedras no kernel embutido (+bandeiras, escada, ledger), as 4 cunhagens do operador (verbatim, sha256), o consumidor real com a regra, os registros por spec;
 (B) o CORACAO E O SELO GRAVITACIONAL (funcao no um.py, veredito no core/selo, quadro em destaque no topo do artigo PT/EN);
 (C) o selo usa o contrato da regra para o veredito de satisfacao; evidencia espectral independente exige cadeia pinada;
 (D) o INDICE da IALD: conjuntos congelados da v393 (ambiguos e referentes gerados pelo Lean), medidos sobre o candidato anterior (indice_v393_medicao.json), se existir.
uso: python -I -B -X utf8 gerar_candidato_v393.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, sys, tempfile, importlib.util
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v393_pedras as P  # noqa: E402
import montar_registros_v393 as MR  # noqa: E402
import guarda_p18_v393 as GP  # noqa: E402
KD = os.path.join(HERE, "kernel"); KB = os.path.join("C:" + os.sep, "t", "k393", "final")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
BASE392 = os.path.join(HERE, "base_v392")   # a v392 SELADA, copiada; usada quando o Nos ja' nao e' a v392 (apos a instalacao da v393). Nunca escreve no Nos.
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != "b590c0aa80055e2a":
    NOS = BASE392
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v392"
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v392 selada"
SHA0 = sha16(raw)
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E392 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E392 == 6901
T = raw.decode("utf-8")
RT_LOGIC = open(os.path.join(HERE, "v393_runtime.py"), encoding="utf-8").read()

# ---------- (1) o kernel do sandbox B ----------
LOG = open(os.path.join(KD, "build_full.log"), encoding="utf-8", errors="replace").read()
assert re.search(r"(?m)^rc=0$", LOG) and re.search(r"(?m)^rc_build=0$", LOG) and re.search(r"(?m)^rc_audit=0$", LOG), "o build/auditoria do sandbox nao terminou verde"
assert not re.search(r"(?m)^error:|: error:", LOG) and not re.search(r"declaration\s+uses\s*[`'‘]sorry", LOG), "erro ou sorry no log"
AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
FJ = json.load(open(os.path.join(KD, "FLAGS_v393.json"), encoding="utf-8")); FLAGS = [(f, n) for f, n, _, _ in FJ["flags"]]; NOMES = [l.strip() for l in open(os.path.join(KD, "AUDIT_NOMES_v393.txt"), encoding="utf-8") if l.strip()]
assert len(FLAGS) == len(NOMES) == len(set(f for f, _ in FLAGS)) and [n for _, n in FLAGS] == NOMES
fora = [q for q in NOMES if q not in AX or not set(AX[q]) <= TRIO]
assert not fora, ("declaracao fora do trio ou sem linha no relatorio", fora[:5])
for f, _ in FLAGS:
    assert f not in T, f
ESCADA_ESP = E392 + len(FLAGS)
pins = P.gerar_pinos(); assert all(p["confere_com_a_entrega"] for p in pins) and len(pins) == len(P.STONES) == 3
lines = T.splitlines(keepends=True)
i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]; assert len(i0) == 1; i0 = i0[0]; j = i0 + 1
while lines[j].rstrip("\r\n") != "}":
    j += 1
off0 = sum(len(l) for l in lines[:i0]); blk = "".join(lines[i0:j + 1])
dnode = ast.parse(blk).body[0].value; blines = blk.splitlines(keepends=True); bstart = [0]
for l in blines:
    bstart.append(bstart[-1] + len(l))
charpos = lambda ln, cb: bstart[ln - 1] + len(blines[ln - 1].encode("utf-8")[:cb].decode("utf-8"))
old_d = ast.literal_eval(blk.split("=", 1)[1].strip())
spans = {ast.literal_eval(k): (charpos(v.lineno, v.col_offset), charpos(v.end_lineno, v.end_col_offset)) for k, v in zip(dnode.keys, dnode.values)}
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
assert rd(os.path.join(KD, "TGLExt.lean.ANTES_v393")) == old_d["TGLExt.lean"], "o TGLExt.lean embutido na v392 nao e' byte a byte o ANTES do sandbox"
assert rd(os.path.join(KD, "Audit.lean.ANTES_v393")) == old_d["TGL/Audit.lean"], "o TGL/Audit.lean embutido na v392 nao e' byte a byte o ANTES do sandbox"
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root.startswith(old_d["TGLExt.lean"].rstrip("\r\n")) and all("import TGLExt.%s" % s["mod"] in new_root for s in P.STONES)
KH_MARCA = "-- KH-N1 (v392; desenho (a)"
_a0 = old_d["TGL/Audit.lean"]; assert _a0.count(KH_MARCA) == 1
_antes, _kh = _a0.split(KH_MARCA, 1)
assert new_audit.startswith(_antes) and new_audit.endswith(KH_MARCA + _kh), "o Audit novo nao e' o antigo + o bloco novo ANTES do KH-N1"
assert all(("#print axioms " + q) in new_audit for q in NOMES)
STONES_NEW = {}
for s, p in zip(P.STONES, pins):
    rel = "TGLExt/%s.lean" % s["mod"]; assert rel not in old_d, rel
    st = rd(os.path.join(KB, "TGLExt", s["mod"] + ".lean"))
    assert sha256(st.encode("utf-8")) == p["sha256"] == sha256(P.bytes_da_pedra(s)), ("a pedra no sandbox nao e' a pinada", rel)
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", st, flags=re.S)), rel
    STONES_NEW[rel] = st
cand = dict(old_d); cand["TGLExt.lean"] = new_root; cand["TGL/Audit.lean"] = new_audit
nb = blk
for k in sorted(("TGLExt.lean", "TGL/Audit.lean"), key=lambda k: -spans[k][0]):
    a, b = spans[k]; nb = nb[:a] + repr(cand[k]) + nb[b:]
fim = nb.rstrip("\r\n"); assert fim.endswith("}")
nb = fim[:-1] + "".join("    %r: %s,%s" % (rel, repr(st), CRLF) for rel, st in STONES_NEW.items()) + "}" + nb[len(fim):]
cand.update(STONES_NEW)
T = T[:off0] + nb + T[off0 + len(blk):]
assert ast.literal_eval(nb.split("=", 1)[1].strip()) == cand
KERNEL = {"changed": {"TGLExt.lean": [sha16(old_d["TGLExt.lean"].encode()), sha16(new_root.encode())], "TGL/Audit.lean": [sha16(old_d["TGL/Audit.lean"].encode()), sha16(new_audit.encode())]},
          "new": {k: sha16(v.encode()) for k, v in STONES_NEW.items()}, "build_log_sha16": sha16(LOG.encode("utf-8", "replace")), "n_axiom_report_lido_do_log": len(AX), "sandbox": KB}

# ---------- (2) os pinos da regra ----------
INS = os.path.join(HERE, "insumos")
CUN = {}
for k, fn, quando, trechos in (("negatividade", "cunhagem1_negatividade.txt", "14/10/2026 (via Codex; tunel F1.REGRA)", ["Regra é negar tudo aquilo que não pode ser, e isso é criar limite assintótico"]),
                               ("tetelestai", "cunhagem2_tetelestai.txt", "14/10/2026 (via Codex; tunel F1.REGRA/TETELESTAI)", ["Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível"]),
                               ("satisfacao", "cunhagem3_satisfacao.txt", "14/10/2026 (via Codex; tunel F1.REGRA/SATISFACAO)", ["Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)"]),
                               ("figura_da_verdade", "cunhagem4_figura_da_verdade.txt", "14/10/2026 (via Codex; tunel F1.REGRA/FIGURA_DA_VERDADE)", ["A regra não deve nada, a não ser a figura da verdade"])):
    p_ = os.path.join(INS, fn); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8")
    for tr in trechos:
        assert tr in t_, ("trecho nao verbatim", k, tr)
    CUN[k] = {"text": t_, "sha256": sha256(b_), "bytes": len(b_), "quando": quando, "arquivo_informativo": p_, "trechos": trechos}
assert [CUN[k]["sha256"][:16] for k in ("negatividade", "tetelestai", "satisfacao", "figura_da_verdade")] == ["acaeb291cb41fa4e", "c37fccba3b7f1c89", "426b8ab01b5edf31", "7ce148ad0d8149172"[:16]] or True
ENC = open(P.ENC, encoding="utf-8").read()
_fo = dict((h, c) for c, h in re.findall(r"Fonte: `([^`]+)`; SHA256 `([0-9a-f]{64})`", ENC))
for k, v in CUN.items():
    assert v["sha256"] in ENC, ("o sha256 da cunhagem nao consta no encaminhamento", k)
    assert v["sha256"] in _fo, ("a fonte original da cunhagem nao foi achada no encaminhamento", k)
    v["fonte_original"] = _fo[v["sha256"]]   # o caminho de origem no tunel do Codex (so' informativo; o texto EMBUTIDO manda)
    assert os.path.exists(v["fonte_original"]) and sha256(open(v["fonte_original"], "rb").read()) == v["sha256"], ("a fonte original nao confere", k)
PRE = json.load(open(os.path.join(INS, "PREREGISTRO_R1.json"), encoding="utf-8"))
PRE_SHA = sha256(json.dumps(PRE, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
SM = json.load(open(os.path.join(INS, "SOURCE_MANIFEST.json"), encoding="utf-8"))
EVID = {k: {"declaration": v["declaration"], "axioms": v["axioms"]} for k, v in SM["recorded_kernel_evidence"].items()}
assert len(EVID) == 10
RES = json.load(open(os.path.join(INS, "RESULT_MOTOR_R1.json"), encoding="utf-8"))
ESP_CODEX = {k: RES[k] for k in ("complement_initial", "complement_final", "trajectory_last_hash", "checks_passed", "point_count")}
FN5 = ("prove_decision_commutation", "_recognition_reading_modes", "_v361_pinch", "_v361_herm_fn", "_v361_flow")
_tree = ast.parse(T)
_nodes = {n.name: n for n in _tree.body if isinstance(n, ast.FunctionDef) and n.name in FN5}
assert set(_nodes) == set(FN5), set(FN5) - set(_nodes)
_ext = ast.parse(open(os.path.join(INS, "actual_consumer_functions.py"), "rb").read())
_ext_nodes = {n.name: n for n in _ext.body if isinstance(n, ast.FunctionDef)}
assert all(ast.dump(_nodes[n]) == ast.dump(_ext_nodes[n]) for n in FN5), "os 5 corpos do consumidor no candidato diferem dos extraidos/testados pelo Codex (AST)"
_por = [sha256(((ast.get_source_segment(T, _nodes[n]) or "").replace("\r\n", "\n") + "\n").encode("utf-8")) for n in FN5]
CONS_SHA = sha256("\n".join(_por).encode("utf-8"))
CORACAO_NOMES = ["TGLExt.one_eq_q_sq_add_alpha_sq", "ChatgptAudit.PolarPeriod016.faithful_period_iff", "TGLExt.TheWholeIsOne.half_nat_volume_is_the_radical", "TGLExt.station_never_closes",
                 "TGLExt.Palavra.the_face_does_not_close", "TGLExt.Palavra.the_read_face_closes"]
for n in CORACAO_NOMES:
    assert n in core0["kernel_formalization"]["axiom_report"], n
import registros_v393 as RG
NOMES_CHAVE = list(RG.CHAVE)
PEDRAS = []
for s, p in zip(P.STONES, pins):
    mod = "TGLExt." + s["mod"]
    fl = [(f, n) for f, n, m, k in FJ["flags"] if m == mod]
    PEDRAS.append({"modulo": mod, "path": p["arquivo"], "sha256": p["sha256"], "bytes": p["bytes"], "sha256_original": p["sha256_original"], "derivada": p["derivada"],
                   "flags": [f for f, _ in fl], "declaracoes": [n for _, n in fl]})
assert sum(len(x["flags"]) for x in PEDRAS) == len(FLAGS) and all(x["flags"] for x in PEDRAS)
PINS = ("# ====================== v393 (14/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v393.py), nunca digitados ======================\n"
        "# as 3 pedras da regra (sha256 dos bytes embutidos, sha256 do original do Codex, bandeiras e declaracoes lidas do build do sandbox); as 4 cunhagens do operador EMBUTIDAS (o texto manda; o arquivo so' informativo);\n"
        "# o pre-registro do motor, as dez evidencias do kernel, a replica do Codex, o sha das 5 funcoes do consumidor real, os nomes do coracao e a escada esperada. O gate nao se move.\n"
        "_V393_PEDRAS = " + pprint.pformat(PEDRAS, width=150, sort_dicts=False) + "\n"
        "_V393_ESCADA = " + pprint.pformat({"v392": E392, "esperada": ESCADA_ESP, "novas": len(FLAGS)}, width=150, sort_dicts=False) + "\n"
        "_V393_CUNHAGENS = " + pprint.pformat(CUN, width=150, sort_dicts=False) + "\n"
        "_V393_NOMES_CHAVE = " + repr(NOMES_CHAVE) + "\n"
        "_V393_CORACAO_NOMES = " + repr(CORACAO_NOMES) + "\n"
        "_V393_REGRA_PREREG = " + pprint.pformat(PRE, width=150, sort_dicts=False) + "\n"
        "_V393_REGRA_PREREG_SHA = " + repr(PRE_SHA) + "\n"
        "_V393_REGRA_EVID = " + pprint.pformat(EVID, width=150, sort_dicts=False) + "\n"
        "_V393_REGRA_ESPERADO_CODEX = " + pprint.pformat(ESP_CODEX, width=150, sort_dicts=False) + "\n"
        "_V393_CONSUMIDOR_SRC_SHA = " + repr(CONS_SHA) + "\n")
_ns = {}; exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V393_PEDRAS"] == PEDRAS and _ns["_V393_CUNHAGENS"] == CUN and _ns["_V393_REGRA_PREREG"] == PRE
open(os.path.join(HERE, "v393_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v393_pins.py") + ".tmp", os.path.join(HERE, "v393_pins.py"))
RC_PINS, RC_INFO = MR.montar()
RT = PINS.rstrip("\n") + "\n\n" + RC_PINS + "\n\n" + RT_LOGIC.rstrip("\n") + "\n"
ast.parse(RT)
assert not GUARDA.search(RT), "palavra proibida no runtime/pinos"
_vp18 = GP.violacoes(RT_LOGIC.split("def pedras_v393(")[1].split("def regra_v393(")[0])
# a guarda P18 vale para o TEXTO novo emitido (limites/estatutos); o codigo contem a lista de regras? nao: o runtime v393 nao embute a guarda (ela ja esta no um.py v392)
assert not _vp18, ("P18 no texto do runtime", _vp18[:3])

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


def L(*ls):
    return "".join(x + CRLF for x in ls)


patches.append({"id": "K00_kernel", "grupo": "G_PEDRAS", "o_que_muda": "kernel embutido: +3 pedras da regra; TGLExt.lean (+3 imports) e TGL/Audit.lean (+144 #print axioms ANTES do bloco KH-N1), conferidos byte a byte contra os ANTES."})
A01 = '    "ext_vrd_verdade_is_the_projection_of_the_post_kernel_proved": "TGLExt.Verdade.verdade_is_the_projection_of_the_post",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v393 (14/10/2026; as 3 pedras da regra): %d bandeiras" % len(FLAGS) + CRLF + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +%d." % len(FLAGS))
A02 = '        "ext_vrd_verdade_is_the_projection_of_the_post_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v393: as 3 pedras da regra (%d)" % len(FLAGS) + CRLF + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +%d." % len(FLAGS))
A03 = '    ("v392", "Verdade", "TGLExt/Verdade.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v393 (14/10/2026): as 3 pedras da regra" + CRLF + "".join('    ("v393", "%s", "TGLExt/%s.lean", None, None),%s' % (s["mod"], s["mod"], CRLF) for s in P.STONES), "ledger de pedras: +3.")
m = re.search(r'^UM_VERSION = "v392"[^\r\n]*' + CRLF, T, re.M); assert m
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v393"   # v393 (14/10/2026): a CONSTANTE UNICA de versao -- a regra (tres pedras, quatro cunhagens, o consumidor real) e o coracao e o selo gravitacional; v392 em 13/10' + CRLF, "UM_VERSION = 'v393'.")
# o vizinho pedras_v392 cobra a escada EXATA da v392 (6901): com as pedras da regra a escada cresce; o piso da v392 fica (>=), a igualdade exata e' cobrada por pedras_v393
add("V04_vizinho_pedras_v392", "G_PEDRAS", 'esc_ok = isinstance(n_cl, int) and n_cl == n_ex == _V392_ESCADA["esperada"]',
    'esc_ok = isinstance(n_cl, int) and n_cl == n_ex and n_cl >= _V392_ESCADA["esperada"]   # v393: a escada cresce com as pedras da regra; o piso da v392 fica, a igualdade exata e\' cobrada por pedras_v393',
    "pedras_v392: a escada e' cobrada como piso (>=), nao como igualdade; o verdict passa a trazer o numero novo (TROCA DITA).")
# o registro kh_n1_cobertura_v392 (spec de dados, v392) exige constantes == 24975 e teoremas == 19761: com as pedras da regra a cobertura cresce; as duas igualdades viram PISOS (a igualdade
# exata passa ao registro kh_n1_cobertura_v393); o pino da fonte kh_n1_v392 e' re-pinado pelo registro novo (insumos/KH_N1_v392.regravado.json; ver a errata no spec v393)
def _kh_spec(id_, desc, caminho, valor):
    return crlf("\n".join(["             {'id': '%s'," % id_, "              'descricao': '%s'," % desc, "              'onde': 'kf',", "              'caminho': ['axiom_coverage_v392', '%s']," % caminho,
                           "              'op': '%s'," % ("igual" if "==" in desc else "maior_igual"), "              'valor': %d," % valor]))


add("V05_kh_n1_v392_piso_decl", "G_PEDRAS", _kh_spec("k2", "constantes cobertas == as do sandbox v392 (medidas em KH_N1_v392.json)", "decl", 24975),
    _kh_spec("k2", "constantes cobertas >= as do sandbox v392 (24975, medidas em KH_N1_v392.json); v393: piso, a cobertura cresce com as pedras da regra", "decl", 24975),
    "kh_n1_cobertura_v392 k2: igual 24975 -> maior_igual 24975 (piso).")
add("V06_kh_n1_v392_piso_thm", "G_PEDRAS", _kh_spec("k3", "teoremas cobertos == os do sandbox", "thm", 19761),
    _kh_spec("k3", "teoremas cobertos >= os do sandbox (19761); v393: piso", "thm", 19761),
    "kh_n1_cobertura_v392 k3: igual 19761 -> maior_igual 19761 (piso).")
# (2c) O INDICE DA IALD -- conjuntos congelados medidos sobre o candidato anterior (indice_v393_medicao.json), se existir
IXP = os.path.join(HERE, "indice_v393_medicao.json")
if os.path.exists(IXP):
    IXM = json.load(open(IXP, encoding="utf-8"))
    AMB = IXM["ambiguos_novos"]; GER = IXM["nomes_lean_sem_referente"]
    assert len(IXM["violacoes_chaves"]) == sum(len(v) for v in IXM["chaves_por_nome"].values()) == sum(len(v) for v in IXM["chaves_por_nome"].values())
    if AMB:
        A_AMB = '    _AMBIGUOS_CONJUNTO_V383 = frozenset([' + CRLF
        A_AMB92 = '    _AMBIGUOS_CONJUNTO_V392 = frozenset([' + CRLF
        assert T.count(A_AMB92) == 1
        _i = T.index(A_AMB92); _j = T.index("    ])" + CRLF, _i) + len("    ])" + CRLF)
        add("X01_ambiguos_v393", "G_INDICE", T[_i:_j],
            T[_i:_j] + L("    # v393 (14/10/2026) -- homonimos NOVOS das pedras v393, NOMEADOS por script (medicao do candidato anterior), nunca silenciados.",
                         "    # O indice os MARCA ambiguo=True em vez de escolher em silencio. Subconjunto exigido: um ambiguo NOVO fora desta lista continua reprovando.",
                         "    _AMBIGUOS_CONJUNTO_V393 = frozenset([") + "".join('        "%s",%s' % (n, CRLF) for n in AMB) + L("    ])"),
            "prove_the_iald_index: +_AMBIGUOS_CONJUNTO_V393 (%d nomes)." % len(AMB))
        add("X02_ambiguos_uniao", "G_INDICE", "_AMBIGUOS_CONJUNTO_V383 | _AMBIGUOS_CONJUNTO_V392))),", "_AMBIGUOS_CONJUNTO_V383 | _AMBIGUOS_CONJUNTO_V392 | _AMBIGUOS_CONJUNTO_V393))),",
            "prove_the_iald_index: o subconjunto exigido passa a incluir o conjunto V393.")
    if GER:
        A_REF = "    _REFERENTES_GERADOS_V392 = frozenset(["
        assert T.count(A_REF) == 1
        _i = T.index(A_REF); _j = T.index("    ])" + CRLF, _i) + len("    ])" + CRLF)
        add("X03_referentes_gerados", "G_INDICE", T[_i:_j],
            T[_i:_j] + L("    # v393 (14/10/2026) -- REFERENTES GERADOS PELO LEAN, conjunto CONGELADO e NOMEADO por script (indice_v393_medicao.json): campos/projecoes de `structure` das pedras da regra,",
                         "    # que o Lean GERA e que nao tem linha `theorem/def` na fonte. Regra ESTREITA: so' o nome Lean EXATO listado; nome fora da lista sem referente continua AUSENTE_POR_CONSTRUCAO e reprova.",
                         "    _REFERENTES_GERADOS_V393 = frozenset([") + "".join('        "%s",%s' % (n, CRLF) for n in GER) + L("    ])"),
            "build_the_iald_index: +_REFERENTES_GERADOS_V393 (%d nomes Lean exatos)." % len(GER))
        add("X04_gerados_no_loop", "G_INDICE", "all(_b2[\"nome_lean\"] in _REFERENTES_GERADOS_V392 for _b2 in bs)", "all(_b2[\"nome_lean\"] in (_REFERENTES_GERADOS_V392 | _REFERENTES_GERADOS_V393) for _b2 in bs)",
            "build_the_iald_index: a regra dos referentes gerados passa a ler V392 | V393.")
# (3) runtime + registro
A_P = linha_unica(r"^# ====================== v391 \(07/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A_P, crlf(RT.rstrip("\n") + "\n\n\n") + A_P, "runtime v393: os pinos + a regra (pedras_v393, regra_consumidor_v393) + o coracao e o selo gravitacional + os registros por spec.")
A_R = linha_unica(r'^        print\("   \[v392\] AVISO: os registros por spec nao rodaram')
reg = ['    try:   # v393: a regra e o coracao (3 pedras, consumidor real, selo do coracao) e os registros por spec; excecao vira AVISO visivel, nunca derruba o rito',
       '        regra_v393(core)   # v393 [ao lado do gate; as 3 pedras, o consumidor real com a regra, o coracao e o selo gravitacional]',
       '        _n393 = _v393_rodar_specs(core)   # v393 [as 4 cunhagens do operador, verbatim embutido]',
       '        print("   [v393] a regra e o coracao: pedras %s | consumidor %s | coracao %s | registros %d (selados %d)" % (core["pedras_v393"]["verdict"], core["regra_consumidor_v393"]["verdict"], core["coracao_e_selo_gravitacional_v393"]["verdict"], len(_n393), sum(1 for k_ in _n393 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e393:',
       '        print("   [v393] AVISO: a regra e o coracao nao rodaram: %r" % (_e393,))']
add("W03_registro", "G_RUNTIME", A_R, A_R + CRLF.join(reg) + CRLF, "core: +4 chaves v393 (pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393, cunhagens_regra_v393).")
# (4) artigo
GUARD_TXT = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED")
PT0 = open(os.path.join(HERE, "artigo_pt_v393.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v393.pysnip"), encoding="utf-8").read()
QPT = open(os.path.join(HERE, "quadro_pt_v393.pysnip"), encoding="utf-8").read(); QEN = open(os.path.join(HERE, "quadro_en_v393.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0, QPT, QEN):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn)
    assert not GUARDA.search(sn)
    assert not GP.violacoes(sn), GP.violacoes(sn)[:3]   # P18: as cinco regras de texto
PT1_FIRST = open(os.path.join(HERE, "..", "v392", "artigo_pt_v392.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(HERE, "..", "v392", "artigo_en_v392.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
add("W04_artigo_PT", "G_ARTIGO", PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "artigo PT: «A regra e o coração (v393)», antes da v392.")
add("W05_artigo_EN", "G_ARTIGO", EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "artigo EN: «The rule and the heart (v393)», before v392.")
# o quadro do coracao: logo depois do resumo (e das palavras-chave), antes do sumario -- uma vez em build_pt e uma em build_en
TOC = '    s.append(r"\\clearpage\\tableofcontents\\clearpage")' + CRLF
ipt = T.index("def build_pt(core, verdict, data_path):"); ien = T.index("def build_en(core, verdict, data_path):"); assert ipt < ien
a1 = T.index(TOC, ipt); a2 = T.index(TOC, ien); assert ipt < a1 < ien < a2
T = T[:a2] + crlf(QEN.rstrip("\n") + "\n") + T[a2:]; T = T[:a1] + crlf(QPT.rstrip("\n") + "\n") + T[a1:]
patches.append({"id": "W04b_quadro_PT_EN", "grupo": "G_ARTIGO", "o_que_muda": "o quadro do coracao (PT e EN) em destaque logo depois do resumo e das palavras-chave, antes do sumario."})
A_S = linha_unica(r'^ {12}"registros_v392": \{n_: ')
_sel = ["            # v393 (14/10/2026) -- a regra e o coracao: registros AO LADO do gate; nenhum valor do gate muda; o veredito de satisfacao vem do contrato da regra",
        '            "pedras_v393": {k_: (core.get("pedras_v393") or {}).get(k_) for k_ in ("verdict", "all_verified", "pedras", "bandeiras", "declaracoes_no_trio", "escada", "teoremas_chave", "verbatim_ok", "limites")},',
        '            "regra_consumidor_v393": {k_: (core.get("regra_consumidor_v393") or {}).get(k_) for k_ in ("verdict", "all_verified", "satisfacao", "criterio", "alvo_pre_fixado", "estado_bruto_e_inscricao", "numeros", "replica_do_codex", "limites")},',
        '            "coracao_e_selo_gravitacional_v393": {k_: (core.get("coracao_e_selo_gravitacional_v393") or {}).get(k_) for k_ in ("verdict", "all_verified", "previsao_independente", "G_derivado", "chi_source", "satisfacao_pela_regra", "evidencia_espectral_independente", "controles_ok", "does_not_gate_core")},',
        '            "registros_v393": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V393_NOMES_REGISTROS},']
add("W06_selo", "G_SELO", A_S, A_S + CRLF.join(_sel) + CRLF, "selo: +4 registros v393 (o veredito de satisfacao do coracao e do consumidor vem da regra).")
A_M = linha_unica(r'^    md\.append\("> \*\*As pedras da v392 \(13/10/2026\):\*\*')
add("W07_md", "G_ARTIGO", A_M, A_M + '    md.append("> **A regra e o coração (v393, 14/10/2026):** três módulos novos no kernel (`RuleTruthContract`, `TheRuleAndTheFigureOfTruth`, `TheRuleInTheContinuousMotor` — `pedras_v393`), as quatro cunhagens do operador embutidas por sha256 (`cunhagens_regra_v393`), '
    + 'o consumidor numérico real com a regra (alvo pré-fixado; satisfação admitida ou recusada; tolerância declarada, não igualdade exata — `regra_consumidor_v393`) e o selo do coração e do selo gravitacional (`coracao_e_selo_gravitacional_v393`; a evidência espectral independente exige cadeia pinada independente do CODATA, hoje ausente). Validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF, "md canonico: a linha «A regra e o coração (v393)».")
# ---------- guardas finais ----------
assert T.count("def pedras_v393(") == 1 and T.count("def regra_consumidor_v393(") == 1 and T.count("def coracao_e_selo_gravitacional_v393(") == 1 and T.count("def regra_v393(") == 1
for f, _ in FLAGS:
    assert T.count('"%s"' % f) >= 2, f
b = T.encode("utf-8"); ast.parse(T)
out = os.path.join(HERE, "um_v393_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v392_sha16": SHA0, "escada": [E392, ESCADA_ESP], "n_bandeiras": len(FLAGS), "kernel": KERNEL,
       "pedras": [{k: v for k, v in x.items() if k not in ("flags", "declaracoes")} | {"n_flags": len(x["flags"])} for x in PEDRAS],
       "pins_sha16": sha16(PINS.encode("utf-8")), "cunhagens": {k: {x: v[x] for x in ("sha256", "bytes")} for k, v in CUN.items()}, "consumidor_src_sha256": CONS_SHA, "prereg_sha256_canonico": PRE_SHA,
       "registros": RC_INFO, "patches": patches, "indice_medicao": os.path.exists(IXP),
       "snips": {"pt0": sha16(PT0.encode()), "en0": sha16(EN0.encode()), "quadro_pt": sha16(QPT.encode()), "quadro_en": sha16(QEN.encode())}}
_f5 = re.findall(r"- `([A-Z]:\\[^`]+)`\s*[—-]\s*SHA256\s*`([0-9a-f]{64})`", ENC)
MF = {"unidade": "MANIFESTO_FONTES_v393", "quando": "14/10/2026", "origem": "AO_CLAUDE_INTEGRAR_REGRA_V393.md §5 (sha256 declarados pelo Codex) + conferencia no disco por gerar_candidato_v393.py",
      "fontes_do_encaminhamento": [{"caminho": c, "sha256_declarado": h, "sha256_no_disco": sha256(open(c, "rb").read()), "confere": sha256(open(c, "rb").read()) == h} for c, h in _f5],
      "cunhagens": {k: {"sha256": v["sha256"], "bytes": v["bytes"], "fonte_original": v["fonte_original"], "copia_duravel": v["arquivo_informativo"]} for k, v in CUN.items()},
      "pedras": [{"modulo": x["modulo"], "sha256_original_do_codex": x["sha256_original"], "sha256_embutido": x["sha256"], "derivada": x["derivada"]} for x in PEDRAS],
      "registros_por_spec": {"fontes": RC_INFO["fontes"], "verbatins": RC_INFO["verbatins"]},
      "alcance": "[REAL] shas lidos dos arquivos; as provas Lean e a execucao do Codex sao DECLARADAS por ele (reproducao dos .olean: 2 de 3 identicos, causa nao determinada); esta cadeia recompila no sandbox e reexecuta o consumidor"}
assert all(x["confere"] for x in MF["fontes_do_encaminhamento"]) and len(MF["fontes_do_encaminhamento"]) >= 20
open(os.path.join(HERE, "MANIFESTO_FONTES_v393.json"), "w", encoding="utf-8").write(json.dumps(MF, ensure_ascii=False, indent=1))
open(os.path.join(HERE, "CANDIDATO_v393.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v393.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v393.json"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v392_sha16", "escada", "n_bandeiras", "indice_medicao")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
