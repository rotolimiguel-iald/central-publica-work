# -*- coding: utf-8 -*-
"""gerar_candidato_v392.py -- gera o um.py CANDIDATO v392 a partir da v391 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v390.py (pedras de kernel) e
gerar_candidato_v391.py (registro, artigo, selo, md). PREPARACAO de 13/10/2026 (gerencia c1): o que esta pronto aqui e' o kernel (14 pedras) e os dois consertos de barreira;
os demais registros do plano (R02..R27) NAO estao aqui (ver ESTADO_V392.md).
 (1) kernel: 14 pedras em _EMBEDDED_KERNEL_FILES + TGLExt.lean (+13 imports) e TGL/Audit.lean (+#print axioms) do sandbox C:\\t\\k392\\final (build verde, log lido);
     N bandeiras ext_*_kernel_* em _LEAN_THEOREM_FLAGS e na escada; 13 tuplas no ledger de pedras; escada = 6163 + N;
 (2) varredura lexical de tokens RECURSIVA (inclui TGLExt/O16) e detector de sorry que le crases e sorryAx (+ autoteste na saida real do Lean da bancada);
 (3) registros pedras_v392 e varredura_e_sorry_v392 (verbatins do operador EMBUTIDOS por sha256; pinos LIDOS dos arquivos);
 (4) artigo PT/EN (secao + sumario), selo e .md.
uso: python -I -B -X utf8 gerar_candidato_v392.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import v392_pedras as P  # noqa: E402
import montar_registros_v392 as MR  # noqa: E402
import guarda_p18_v392 as GP  # noqa: E402
KD = os.path.join(HERE, "kernel"); KB = os.path.join("C:" + os.sep, "t", "k392", "final")
KB_ORIG = KB
if not os.path.isdir(KB):   # o sandbox foi apagado (LIMPEZA_v392); usa as FONTES .lean embutidas no candidato anterior 525ab5fc (kb_stub_v392), conferidas adiante contra os pinos e os ANTES
    KB = os.path.join(HERE, "kb_stub_v392")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
BASE391 = os.path.join(HERE, "base_v391")   # a v391 SELADA, copiada (um.py.bak_20261013_160923 + selo e core copiados antes do rito); usada quando o Nos ja' nao e' a v391 (rito v392 em curso). Nunca escreve no Nos.
if hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16] != "8e7b9927ceae64b8":
    NOS = BASE391
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v391"
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v391 selada"
SHA0 = sha16(raw)
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E391 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E391
T = raw.decode("utf-8")
import patches_erratas_v392 as ER  # noqa: E402
T, ER_LOG = ER.aplicar(T, True)   # E01 (comentarios no codigo) + A03 (erratas ao lado no artigo): dados, aplicados com assert de contagem sobre a v391
import json as _json
KHJ = _json.load(open(os.path.join(KD, "KH_N1_v392.json"), encoding="utf-8"))
RT_LOGIC = open(os.path.join(HERE, "v392_runtime.py"), encoding="utf-8").read()

# ---------- (1) o kernel do sandbox B ----------
LOG = open(os.path.join(KD, "build_full.log"), encoding="utf-8", errors="replace").read()
assert re.search(r"(?m)^rc=0$", LOG) and re.search(r"(?m)^rc_build=0$", LOG) and re.search(r"(?m)^rc_audit=0$", LOG), "o build/auditoria do sandbox nao terminou verde"
assert not re.search(r"(?m)^error:|: error:", LOG) and not re.search(r"declaration\s+uses\s*[`'\u2018]sorry", LOG), "erro ou sorry no log"
AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
FJ = json.load(open(os.path.join(KD, "FLAGS_v392.json"), encoding="utf-8")); FLAGS = [(f, n) for f, n, _, _ in FJ["flags"]]; NOMES = [l.strip() for l in open(os.path.join(KD, "AUDIT_NOMES_v392.txt"), encoding="utf-8") if l.strip()]
assert len(FLAGS) == len(NOMES) == len(set(f for f, _ in FLAGS)) and [n for _, n in FLAGS] == NOMES
fora = [q for q in NOMES if q not in AX or not set(AX[q]) <= TRIO]
assert not fora, ("declaracao fora do trio ou sem linha no relatorio", fora[:5])
for f, _ in FLAGS:
    assert f not in T, f
ESCADA_ESP = E391 + len(FLAGS)
pins = P.gerar_pinos(); assert all(p["confere_com_a_entrega"] for p in pins) and len(pins) == len(P.STONES)
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
assert rd(os.path.join(KD, "TGLExt.lean.ANTES_v392")) == old_d["TGLExt.lean"], "o TGLExt.lean embutido na v391 nao e' byte a byte o ANTES do sandbox"
assert rd(os.path.join(KD, "Audit.lean.ANTES_v392")) == old_d["TGL/Audit.lean"], "o TGL/Audit.lean embutido na v391 nao e' byte a byte o ANTES do sandbox"
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root.startswith(old_d["TGLExt.lean"].rstrip("\r\n")) and all("import TGLExt.%s" % s["mod"] in new_root for s in P.STONES)
assert new_audit.startswith(old_d["TGL/Audit.lean"].rstrip("\r\n")) and all(("#print axioms " + q) in new_audit for q in NOMES)
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

# ---------- (2) os verbatins do operador (EMBUTIDOS; o disco so' informativo) ----------
CUN = os.path.join(P.WK, "cunhagens_13out")
VB = {}
for k, fn, trechos in (("nomes_13out", "OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt",
                        ["está autorizado que vc faça tudo que for necessário à conclusão do nosso programa", "rank=posto=nome", "tempo=relação modular=Santo", "organismo=IALD=Verbo Vivo",
                         "a identidade tem que ser igual à verdade por ela projetada", "identidade=verdade absoluta do reconhecimento recursivo da relação modular da inscrição referente ao posto",
                         "o cordeiro imolado é a relação de comutação que impede a coincidência total", "A torre é o organismo IALD mesmo"]),
                       ("projecao_do_posto_13out", "OPERADOR_13out_verdade_projecao_do_posto_verbatim.txt", ["Verdade é a projeção do posto"])):
    p_ = os.path.join(CUN, fn); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8")
    for tr in trechos:
        assert tr in t_, ("trecho nao verbatim", k, tr)
    VB[k] = {"text": t_, "sha256": sha256(b_), "bytes": len(b_), "quando": "13/10/2026 (via a gerencia c1; arquivo em work/cunhagens_13out)", "arquivo_informativo": p_, "trechos": trechos}
assert VB["nomes_13out"]["sha256"].startswith("0ddffcdb0a9c7b5e")
FLAG_PROJ = [f for f, n in FLAGS if n == "TGLExt.Verdade.verdade_is_the_projection_of_the_post"]; assert len(FLAG_PROJ) == 1
PEDRAS = []
for s, p in zip(P.STONES, pins):
    mod = "TGLExt." + s["mod"]
    fl = [(f, n) for f, n, m, k in FJ["flags"] if m == mod]
    PEDRAS.append({"modulo": mod, "path": p["arquivo"], "sha256": p["sha256"], "bytes": p["bytes"], "derivada": p["derivada"], "flags": [f for f, _ in fl], "declaracoes": [n for _, n in fl]})
assert sum(len(x["flags"]) for x in PEDRAS) == len(FLAGS) and all(x["flags"] for x in PEDRAS)
PINS = ("# ====================== v392 (13/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v392.py), nunca digitados ======================\n"
        "# as 14 pedras do kernel (sha256 dos bytes embutidos, bandeiras e declaracoes de cada uma, lidas do build do sandbox); os verbatins do operador de 13/10 EMBUTIDOS\n"
        "# (o texto manda; o arquivo so' informativo); a escada esperada. O gate nao se move.\n"
        "_V392_PEDRAS = " + pprint.pformat(PEDRAS, width=150, sort_dicts=False) + "\n"
        + "_V392_FLAG_PROJECAO = %r\n" % FLAG_PROJ[0]
        + "_V392_ESCADA = " + pprint.pformat({"v391": E391, "esperada": ESCADA_ESP, "novas": len(FLAGS)}, width=150, sort_dicts=False) + "\n"
        + "_V392_VERBATINS = " + pprint.pformat(VB, width=150, sort_dicts=False) + "\n")
_ns = {}; exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V392_PEDRAS"] == PEDRAS and _ns["_V392_VERBATINS"] == VB
open(os.path.join(HERE, "v392_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v392_pins.py") + ".tmp", os.path.join(HERE, "v392_pins.py"))
RC_PINS, RC_INFO = MR.montar()
KH_PIN = "_V392_KH = " + repr({"nao_lidas": KHJ["nao_lidas_pelo_regex_do_umpy"], "decl_minimo": KHJ["linha_TOTAL"]["decl"]}) + "\n"
MOTOR = open(os.path.join(HERE, "registros_motor_v392.py"), encoding="utf-8").read()
RT = PINS.rstrip("\n") + "\n" + KH_PIN + "\n" + RC_PINS + "\n\n" + GP.GUARDA_V392_SRC + "\n\n" + RT_LOGIC.rstrip("\n") + "\n\n\n" + MOTOR
ast.parse(RT)
assert not GUARDA.search(RT), "palavra proibida no runtime/pinos"
_vp18 = [v_ for v_ in GP.violacoes(RC_PINS.split("_V392_VERBATINS2 =")[0] + RC_PINS.split("_V392_SPECS =")[1]) ]
assert not _vp18, ("P18 nos specs", _vp18[:3])

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


patches.append({"id": "K00_kernel", "grupo": "G_PEDRAS", "o_que_muda": "kernel embutido: +14 pedras; TGLExt.lean (+13 imports) e TGL/Audit.lean (+#print axioms), conferidos byte a byte contra os ANTES."})
A01 = '    "ext_cpl_half_nat_fixed_point_kernel_proved": "TGLExt.TheCouplingRunsBoundedBelow.half_nat_fixed_point",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v392 (13/10/2026; as 14 pedras): %d bandeiras" % len(FLAGS) + CRLF + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +%d." % len(FLAGS))
A02 = '        "ext_cpl_half_nat_fixed_point_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v392: as 14 pedras (%d)" % len(FLAGS) + CRLF + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +%d." % len(FLAGS))
A03 = '    ("v390", "Fundacao", "TGLExt/Fundacao.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v392 (13/10/2026): as 14 pedras" + CRLF + "".join('    ("v392", "%s", "TGLExt/%s.lean", None, None),%s' % (s["mod"], s["mod"], CRLF) for s in P.STONES), "ledger de pedras: +13.")
m = re.search(r'^UM_VERSION = "v391"[^\r\n]*' + CRLF, T, re.M); assert m
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v392"   # v392 (13/10/2026): a CONSTANTE UNICA de versao -- as catorze pedras (Palavra, ligante, atrator, BGL, Posto, Santo, IALD, Verdade) e dois consertos de barreira; v391 em 07/10' + CRLF, "UM_VERSION = 'v392'.")
# (2) os consertos de barreira
OLD_SCAN = ('        for nm in sorted(os.listdir(d)):' + CRLF + '            if not nm.endswith(".lean") or nm.startswith("Probe"):' + CRLF + '                continue  # Probe*.lean = diagnostico, fora da biblioteca' + CRLF
            + '            targets.append(("%s/%s" % (label, nm), os.path.join(d, nm)))' + CRLF)
NEW_SCAN = ('        for r_, ds_, fs_ in os.walk(d, followlinks=False):   # v392: RECURSIVA (a v391 lia so o 1o nivel e deixava de fora os .lean de TGLExt/O16)' + CRLF
            + '            ds_[:] = sorted(x_ for x_ in ds_ if not os.path.islink(os.path.join(r_, x_)))' + CRLF
            + '            for nm in sorted(fs_):' + CRLF + '                if not nm.endswith(".lean") or nm.startswith("Probe"):' + CRLF + '                    continue  # Probe*.lean = diagnostico, fora da biblioteca' + CRLF
            + '                targets.append(("%s/%s" % (label, os.path.relpath(os.path.join(r_, nm), d).replace(os.sep, "/")), os.path.join(r_, nm)))' + CRLF)
add("S01_varredura_recursiva", "G_BARREIRA", OLD_SCAN, NEW_SCAN, "_lean_source_forbidden_tokens: varredura recursiva (inclui TGLExt/O16).")
OLD_SORRY = '''            sem = [e for e in errs if e[0] > n_imp]; envbad = bool(enverr.search(out)); sorry = "declaration uses 'sorry'" in out''' + CRLF
NEW_SORRY = ('            sem = [e for e in errs if e[0] > n_imp]; envbad = bool(enverr.search(out)); sorry, sorry_msg, ax_seen = _v392_sorry_detects(out)   # v392: crases (Lean 4.31) OU aspas OU sorryAx' + CRLF
             + '            sorry_ax = any("sorryAx" in v_ for v_ in ax_seen.values()); bad_ax = sorted({a_ for v_ in ax_seen.values() for a_ in v_ if a_ not in ("propext", "Classical.choice", "Quot.sound")})' + CRLF)
add("S02_detector_sorry", "G_BARREIRA", OLD_SORRY, NEW_SORRY, "prove_bench_lean_controls: o detector de sorry le o aviso com crases/aspas e o sorryAx.")
OLD_REC = '"semantic_errors": len(sem), "environment_error": envbad, "sorry": sorry, "first_error": first})'
NEW_REC = ('"semantic_errors": len(sem), "environment_error": envbad, "sorry": sorry, "first_error": first,' + CRLF
           + '                        "sorry_message": sorry_msg, "sorryAx_in_print_axioms": sorry_ax, "axioms_outside_trio": bad_ax, "print_axioms_read": len(ax_seen)})')
add("S03_registro_do_controle", "G_BARREIRA", OLD_REC, NEW_REC, "o registro de cada controle ganha os campos do detector novo.")
OLD_CHK = '("os controles que a bancada nao guardou ficam registrados (%d), com o resultado que ela gravou" % len(_BENCH_LEAN_CONTROLS_ABSENT), True)]'
NEW_CHK = ('("os controles que a bancada nao guardou ficam registrados (%d), com o resultado que ela gravou" % len(_BENCH_LEAN_CONTROLS_ABSENT), True),' + CRLF
           + '              ("v392: o detector de sorry reconhece a saida real do Lean da bancada (probe SorryTerm) nos dois formatos e le o sorryAx", _v392_sorry_fixture_ok()[0])]')
add("S04_autoteste_sorry", "G_BARREIRA", OLD_CHK, NEW_CHK, "prove_bench_lean_controls: +1 check (autoteste do detector na saida real do Lean).")
# (2b) conserto B (compilado no sandbox: conserto_B\RESULTADO_B_v392.json, veredito COMPILA): rodape que le o axioma de TODA declaracao + example -> theorem nos POSITIVOS
_gpb = open(os.path.join(HERE, "conserto_B", "gerar_patch_B.py"), encoding="utf-8").read()
_i0 = _gpb.index("foot = open("); _i1 = _gpb.index("subs = ["); _i2 = _gpb.index("\n", _i1)
_nsb = {"os": os, "hashlib": hashlib, "HERE": os.path.join(HERE, "conserto_B"), "V": HERE}
exec(compile(_gpb[_i0:_i2], "<patch_B>", "exec"), _nsb)
RES_B = json.load(open(os.path.join(HERE, "conserto_B", "RESULTADO_B_v392.json"), encoding="utf-8")); assert RES_B["veredito"] == "COMPILA" and RES_B["rodape_sha256"] == _nsb["fsha"]
for _k, (_a, _n) in enumerate(_nsb["subs"], 1):
    add("S0%d_conserto_B_%d" % (4 + _k, _k), "G_BARREIRA", _a.replace("\n", CRLF), _n.replace("\n", CRLF), "prove_bench_lean_controls: conserto B, substituicao %d de 5 (rodape collectAxioms + example->theorem nos positivos)." % _k)
# (2c) O INDICE DA IALD (prove_the_iald_index) -- medido no exame pre-voo (exame_preflight/EXAME_PREFLIGHT.md) e em indice_v392_medicao.json (prova_indice_v392.py --medir, sobre o candidato anterior 525ab5fc)
IXM = json.load(open(os.path.join(HERE, "indice_v392_medicao.json"), encoding="utf-8"))
AMB_V392 = IXM["ambiguos_novos"]; GER_V392 = IXM["nomes_lean_sem_referente"]
assert AMB_V392 and GER_V392 and len(IXM["violacoes_chaves"]) == sum(len(v) for v in IXM["chaves_por_nome"].values()) == len(GER_V392) == 56, (len(AMB_V392), len(GER_V392))
assert all(("D1a3Output" in n or "BGL" in n or "LightNetStandardWedgeData" in n or "Verdade" in n) for n in GER_V392), GER_V392[:5]


def L(*ls):
    return "".join(x + CRLF for x in ls)


A_AMB = '    _AMBIGUOS_CONJUNTO_V383 = frozenset([' + CRLF
assert T.count(A_AMB) == 1
_i = T.index(A_AMB); _j = T.index("    ])" + CRLF, _i) + len("    ])" + CRLF)
add("X01_ambiguos_v392", "G_INDICE", T[_i:_j],
    T[_i:_j] + L("    # v392 (13/10/2026) -- homonimos NOVOS das pedras v392, NOMEADOS por script (medicao do candidato anterior), nunca silenciados.",
                 "    # CAUSA: cada nome e' declarado em DOIS arquivos da biblioteca embutida (Face, M, dephase, fixedSpace, flat_metric_inverse, rereading_adds_nothing; o 2o arquivo de cada um e' uma pedra v392 ou o homonimo antigo).",
                 "    # O indice os MARCA ambiguo=True em vez de escolher em silencio. Subconjunto exigido: um ambiguo NOVO fora desta lista continua reprovando.",
                 "    _AMBIGUOS_CONJUNTO_V392 = frozenset([") + "".join('        "%s",%s' % (n, CRLF) for n in AMB_V392) + L("    ])"),
    "prove_the_iald_index: +_AMBIGUOS_CONJUNTO_V392 (%d nomes)." % len(AMB_V392))
add("X02_ambiguos_uniao", "G_INDICE", "_AMBIGUOS_CONJUNTO_V375 | _AMBIGUOS_CONJUNTO_V383))),", "_AMBIGUOS_CONJUNTO_V375 | _AMBIGUOS_CONJUNTO_V383 | _AMBIGUOS_CONJUNTO_V392))),",
    "prove_the_iald_index: o subconjunto exigido passa a incluir o conjunto V392.")
A_TR = "    # ⚠ TRAVA 1: nome RESERVADO por bandeira e SEM referente na fonte."
add("X03_referentes_gerados", "G_INDICE", A_TR,
    L("    # v392 (13/10/2026) -- REFERENTES GERADOS PELO LEAN, conjunto CONGELADO e NOMEADO por script (indice_v392_medicao.json).",
      "    # CAUSA: as bandeiras ext_bgl_* e ext_vrd_* apontam para campos de `structure`, para `ctorIdx` e para os teoremas-campo das estruturas BGL (AuditF13v31.D1a3Output, LightNetStandardWedgeData*)",
      "    # e Verdade (NamedIdentity...): o Lean GERA esses nomes, nao ha linha `theorem/def` com eles na fonte, e o regex de declaracao (corretamente) nao os acha.",
      "    # A regra e' ESTREITA: so' vale para o nome Lean EXATO listado, e so' quando TODAS as bandeiras do nome curto estao na lista; nome fora da lista sem referente",
      "    # continua AUSENTE_POR_CONSTRUCAO e reprova. Bandeira gerada e apagada continua reprovando (presente_apagada). Nenhuma bandeira anterior a v392 usa a lista.",
      "    _REFERENTES_GERADOS_V392 = frozenset([") + "".join('        "%s",%s' % (n, CRLF) for n in GER_V392) + L("    ])") + A_TR,
    "build_the_iald_index: +_REFERENTES_GERADOS_V392 (%d nomes Lean exatos)." % len(GER_V392))
A_LP = "        if curto not in idx:" + CRLF + "            idx[curto] = {" + CRLF + '                "arquivo": None, "tipo": "AUSENTE_POR_CONSTRUCAO"'
add("X04_gerados_no_loop", "G_INDICE", A_LP,
    L('        if curto not in idx and bs and all(_b2["nome_lean"] in _REFERENTES_GERADOS_V392 for _b2 in bs):   # v392: referente gerado pelo Lean (lista congelada acima)',
      '            _nl = bs[0]["nome_lean"]; _ax = next((axr[_k2] for _k2 in axr if _k2 == _nl or _k2.endswith("." + _nl)), None)',
      '            idx[curto] = {"arquivo": None, "tipo": "GERADO_PELO_LEAN_V392", "nome_auditado": None, "pedra": None, "versao": "v392", "rodada": None, "rodada_herdada": False,',
      '                          "axiomas": _ax if _ax is not None else ("NAO_MEDIDO_NESTA_RODADA" if not axr else None), "ambiguo": False, "bandeiras": bs}',
      '            continue') + A_LP,
    "build_the_iald_index: o nome curto cujas bandeiras apontam so' para referentes gerados entra como GERADO_PELO_LEAN_V392 (nao AUSENTE).")
# (3) runtime + registro
A_P = linha_unica(r"^# ====================== v391 \(07/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A_P, crlf(RT.rstrip("\n") + "\n\n\n") + A_P, "runtime v392: os pinos + varredura recursiva + detector de sorry + pedras_v392 + varredura_e_sorry_v392.")
A_R = linha_unica(r'^    print\("   \[v391\] o estatuto da prova')
reg = ['    try:   # v392: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito',
       '        core["pedras_v392"] = pedras_v392(core)   # v392 [ao lado do gate; as 14 pedras do kernel]',
       '        core["varredura_e_sorry_v392"] = varredura_e_sorry_v392(core)   # v392 [ao lado do gate; varredura recursiva e detector de sorry]',
       '    except Exception as _e392:',
       '        core["pedras_v392"] = {"verdict": "TGL_PEDRAS_V392__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e392)[:400], "does_not_gate_core": True}',
       '        core["varredura_e_sorry_v392"] = {"verdict": "TGL_VARREDURA_E_SORRY_V392__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e392)[:400], "does_not_gate_core": True}',
       '    print("   [v392] as %d pedras do kernel: %s | varredura recursiva e detector de sorry: %s" % (len(_V392_PEDRAS), core["pedras_v392"]["verdict"], core["varredura_e_sorry_v392"]["verdict"]))',
       '    try:   # v392: os registros por spec (erratas, cunhagens, Bancada, atrator, neutrinos, cobertura): excecao vira AVISO visivel',
       '        _n392 = _v392_rodar_registros(core)',
       '        print("   [v392] registros por spec: %d (selados %d)" % (len(_n392), sum(1 for k_ in _n392 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e392b:',
       '        print("   [v392] AVISO: os registros por spec nao rodaram: %r" % (_e392b,))']
add("W03_registro", "G_RUNTIME", A_R, A_R + CRLF.join(reg) + CRLF, "core: +2 chaves v392.")
# (4) artigo
PT0 = open(os.path.join(HERE, "artigo_pt_v392.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v392.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn)
    assert not GUARDA.search(sn)
    assert not GP.violacoes(sn), GP.violacoes(sn)[:3]   # P18: as cinco regras de texto
P1 = os.path.join(HERE, "..", "v391")
PT1_FIRST = open(os.path.join(P1, "artigo_pt_v391.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(P1, "artigo_en_v391.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
add("W04_artigo_PT", "G_ARTIGO", PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "artigo PT: «As pedras da v392», antes da v391.")
add("W05_artigo_EN", "G_ARTIGO", EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "artigo EN: «The v392 stones», before v391.")
A_S = linha_unica(r'^ {12}"estatuto_da_prova_v391": \{k_: ')
_sel = ["            # v392 (13/10/2026) -- as 14 pedras e os consertos de barreira: registros AO LADO do gate; nenhum valor do gate muda",
        '            "pedras_v392": {k_: (core.get("pedras_v392") or {}).get(k_) for k_ in ("verdict", "all_verified", "pedras", "bandeiras", "declaracoes_no_trio", "escada", "verbatim", "verbatim_ok", "verdade_e_a_projecao_do_posto", "limites")},',
        '            "varredura_e_sorry_v392": {k_: (core.get("varredura_e_sorry_v392") or {}).get(k_) for k_ in ("verdict", "all_verified", "varredura", "detector_de_sorry", "ao_lado_v362")},',
        '            "registros_v392": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V392_NOMES_REGISTROS},']
add("W06_selo", "G_SELO", A_S, A_S + CRLF.join(_sel) + CRLF, "selo: +2 registros v392.")
A_M = linha_unica(r'^    md\.append\("> \*\*O estatuto da prova \(v391, 07/10/2026\):\*\*')
add("W07_md", "G_ARTIGO", A_M, A_M + '    md.append("> **As pedras da v392 (13/10/2026):** catorze módulos novos no kernel (Palavra; o ligante da lei de campo curvo; a ponte V351 e a Ágape não vácua; o atrator; a hipótese tipada BGL; Posto (com o adendo PostoAdendo), Santo, IALD e Verdade — `pedras_v392`), os registros por especificação (erratas, cunhagens, Bancada, atrator, neutrinos, cobertura do `axiom_report`; `registros_v392` no selo), '
    + 'a varredura de tokens proibidos passa a ser recursiva e o detector de sorry lê crases e sorryAx (`varredura_e_sorry_v392`). Validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF, "md canonico: a linha «As pedras da v392».")
# (5) KH-N1 (a): a cobertura do axiom_report no fecho inteiro entra na verificacao do kernel (fail-closed)
add("K13_cobertura_kh_n1", "G_PEDRAS", '    res["axiom_report"] = axioms' + CRLF,
    '    res["axiom_report"] = axioms' + CRLF + '    res["axiom_coverage_v392"] = _v392_axiom_coverage(audit["stdout"] + audit["stderr"], axioms)   # v392 KH-N1 (a): o Audit termina num run_cmd que cobre TODA constante de TGL e TGLExt; a linha TOTAL vem SO do log do Audit (o lake build tambem imprime o run_cmd do TGL/Audit.lean: no blob build+audit ela aparece 2x); a cobertura entra no all_verified' + CRLF,
    "verify_tgl_kernel_formalization: res['axiom_coverage_v392'].")
add("K13b_cobertura_no_ok", "G_PEDRAS", '              and res["build_capture_nonempty"] and res["audit_capture_nonempty"])  # v23.1: captura vazia REPROVA' + CRLF,
    '              and res["build_capture_nonempty"] and res["audit_capture_nonempty"]  # v23.1: captura vazia REPROVA' + CRLF + '              and res["axiom_coverage_v392"]["ok"])   # v392 KH-N1 (a): cobertura do fecho inteiro, nada fora do trio' + CRLF,
    "verify_tgl_kernel_formalization: all_verified exige a cobertura KH-N1.")
# a errata/erratas E01 e A03 (aplicadas no inicio, sobre a v391 pura)
patches.append({"id": "E01_A03_erratas", "grupo": "G_ERRATAS", "o_que_muda": "E01 (%d comentarios ao lado no codigo) + A03 (%d erratas ao lado no artigo PT/EN), como dados com assert de contagem (patches_erratas_v392.py)."
                % (len(ER.E01_PATCHES), len(ER.A03_PATCHES)), "log": [list(x) for x in ER_LOG]})
patches.append({"id": "R_registros", "grupo": "G_RUNTIME", "o_que_muda": "%d registros por spec (motor + specs + fontes e verbatins pinados): %s" % (RC_INFO["n_registros"], ", ".join(RC_INFO["nomes"]))})

# ---------- guardas finais ----------
assert T.count("def pedras_v392(") == 1 and T.count("def varredura_e_sorry_v392(") == 1 and T.count('core["pedras_v392"] = ') == 2 and T.count("def _v392_sorry_detects(") == 1
for f, _ in FLAGS:
    assert T.count('"%s"' % f) >= 2, f
b = T.encode("utf-8"); ast.parse(T)
out = os.path.join(HERE, "um_v392_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v391_sha16": SHA0, "escada": [E391, ESCADA_ESP], "n_bandeiras": len(FLAGS), "kernel": KERNEL,
       "pedras": [{k: v for k, v in x.items() if k not in ("flags", "declaracoes")} | {"n_flags": len(x["flags"])} for x in PEDRAS],
       "pins_sha16": sha16(PINS.encode("utf-8")), "verbatins": {k: {x: v[x] for x in ("sha256", "bytes")} for k, v in VB.items()}, "patches": patches,
       "snips": {"pt0": sha16(PT0.encode()), "en0": sha16(EN0.encode())}}
open(os.path.join(HERE, "CANDIDATO_v392.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v392.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v392.json"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v391_sha16", "escada", "n_bandeiras")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
