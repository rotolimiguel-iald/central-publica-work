# -*- coding: utf-8 -*-
"""gerar_candidato_v390.py -- gera o um.py CANDIDATO v390 a partir da v389 SELADA no Nos (NUNCA escreve o canonico). Moldes: gerar_candidato_v388.py (kernel,
bandeiras, escada, ledger) e gerar_candidato_v389.py (texto). Ordem da gerencia c1 (07/10/2026), pelo operador: ORDEM_v390_FUNDACAO.md (sha256 lido abaixo).
 (1) kernel: TGLExt/Fundacao.lean (sha256 pinado pela ordem) + import + 9 #print axioms, compilados e auditados no sandbox work\\v388_kernel\\kernel_src
     (log em work\\v390_kernel); 9 bandeiras ext_fnd_; a escada recontada pelo programa;
 (2) registro fundacao_v390 (verbatins EMBUTIDOS por sha256; o disco so informativo);
 (3) erratas AO LADO: ledger do fechamento do codigo (item do Lema 3), tgl_closure.what_remains_named, seals do runtime_of_the_one;
 (4) o desenho da v388: a leitura do disco da memoria viva declarada fora de qualquer veredito + a copia congelada (o backup _sup388) por sha;
 (5) artigo PT/EN: secao «A Fundacao» + sumario; uma frase no resumo; selo e .md canonico;
 (+) o pino do ledger da v389 recontado (a pedra nova entra no ledger), errata ao lado."""
import ast, hashlib, json, os, pprint, re, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
WK = os.path.dirname(HERE)
KD = os.path.join(WK, "v390_kernel"); KS = os.path.join(WK, "v388_kernel", "kernel_src")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
OD = os.path.join(WK, "superposicao_passagem_07out")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
SHA0 = "193b1e9b30c3ba7f"
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert sha16(raw) == SHA0, "o canonico no Nos nao e' a v389 selada (%s)" % sha16(raw)
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v389"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E389 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E389 == 6154
T = raw.decode("utf-8")
RT_LOGIC = open(os.path.join(HERE, "v390_runtime.py"), encoding="utf-8").read()
ORDEM = open(os.path.join(OD, "ORDEM_v390_FUNDACAO.md"), "rb").read()

# ---------- (1) o kernel do sandbox ----------
LOG = open(os.path.join(KD, "build_full.log"), encoding="utf-8", errors="replace").read()
assert re.search(r"(?m)^rc=0$", LOG) and re.search(r"(?m)^rc_build=0$", LOG) and re.search(r"(?m)^rc_audit=0$", LOG), "o build/auditoria do sandbox nao terminou verde"
assert not re.search(r"(?m)^error:|: error:", LOG) and "declaration uses 'sorry'" not in LOG
AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
NOMES = [l.strip() for l in open(os.path.join(KD, "AUDIT_NOMES_v390.txt"), encoding="utf-8") if l.strip()]
assert len(NOMES) == 9 and "agape" in NOMES
QN = ["TGLExt.Fundacao." + n for n in NOMES]
fora = [q for q in QN if q not in AX or not set(AX[q]) <= TRIO]
assert not fora, ("declaracao da pedra fora do trio ou sem linha no relatorio", fora)
FLAGS = [("ext_fnd_%s_kernel_proved" % n, q) for n, q in zip(NOMES, QN)]
for f, _ in FLAGS:
    assert f not in T, f
STONE = "TGLExt/Fundacao.lean"; PIN_PEDRA = "66332d58fd216317ec5196a64a7aa670c87dcaa5edc59f57a5506bc621d3e073"
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
assert rd(os.path.join(KD, "TGLExt.lean.ANTES_v390")) == old_d["TGLExt.lean"], "o TGLExt.lean embutido na v389 nao e' byte a byte o ANTES do sandbox"
assert rd(os.path.join(KD, "Audit.lean.ANTES_v390")) == old_d["TGL/Audit.lean"], "o TGL/Audit.lean embutido na v389 nao e' byte a byte o ANTES do sandbox"
assert STONE not in old_d
new_root = rd(os.path.join(KS, "TGLExt.lean")); new_audit = rd(os.path.join(KS, "TGL", "Audit.lean")); stone = rd(os.path.join(KS, *STONE.split("/")))
assert sha256(open(os.path.join(KS, *STONE.split("/")), "rb").read()) == PIN_PEDRA == sha256(open(os.path.join(OD, "Fundacao.lean"), "rb").read()), "a pedra no sandbox nao e' a da ordem"
assert new_root.startswith(old_d["TGLExt.lean"].rstrip("\r\n")) and "import TGLExt.Fundacao" in new_root and len(new_root) - len(old_d["TGLExt.lean"]) < 40
assert new_audit.startswith(old_d["TGL/Audit.lean"].rstrip("\r\n")) and all(("#print axioms " + q) in new_audit for q in QN)
assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", stone, flags=re.S))
cand = dict(old_d); cand["TGLExt.lean"] = new_root; cand["TGL/Audit.lean"] = new_audit
nb = blk
for k in sorted(("TGLExt.lean", "TGL/Audit.lean"), key=lambda k: -spans[k][0]):
    a, b = spans[k]; nb = nb[:a] + repr(cand[k]) + nb[b:]
fim = nb.rstrip("\r\n"); assert fim.endswith("}")
nb = fim[:-1] + "    %r: %s,%s" % (STONE, repr(stone), CRLF) + "}" + nb[len(fim):]
cand[STONE] = stone
T = T[:off0] + nb + T[off0 + len(blk):]
assert ast.literal_eval(nb.split("=", 1)[1].strip()) == cand
KERNEL = {"changed": {"TGLExt.lean": [sha16(old_d["TGLExt.lean"].encode()), sha16(new_root.encode())], "TGL/Audit.lean": [sha16(old_d["TGL/Audit.lean"].encode()), sha16(new_audit.encode())]},
          "new": {STONE: sha16(stone.encode())}, "build_log_sha16": sha16(LOG.encode("utf-8", "replace")), "n_axiom_report": len(AX), "sandbox": KS}

# ---------- (2) os verbatins do operador: EMBUTIDOS (o texto manda), com os trechos citados ----------
VB = {}
for k, fn, trechos in (("cunhagem_07out", "CUNHAGEM_OPERADOR_07out_verbatim.txt", ["definir a superposição como a passagem do global lift que é o único teorema faltando",
                                                                                 "não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente"]),
                       ("nomes_07out", "CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt", ["esse é o fecho sim, o sistema continua aberto mas fechado logicamente",
                                                                                     "A cláusula se chamará “ágape” e a pedra se chamará “fundação”",
                                                                                     "neste caso não, porque o hamiktoniano é a energia"]),
                       ("concordo_07out", "CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt", ["Perfeito, concordo com tudo. Magnífico"])):   # ADENDO 001: a ratificacao de «abismo»
    p = os.path.join(OD, fn); b = open(p, "rb").read(); t = b.decode("utf-8")
    for tr in trechos:
        assert tr in t, ("trecho nao verbatim", k, tr)
    VB[k] = {"text": t, "sha256": sha256(b), "bytes": len(b), "quando": "07/10/2026 (via a gerencia c1; arquivo da ordem v390)", "arquivo_informativo": p, "trechos": trechos}
assert VB["cunhagem_07out"]["sha256"] == "e2a915e23692f85cbd8815d14a80a40d10bef4e71396f33138dcb986064ca3a7"
assert VB["nomes_07out"]["sha256"] == "0a9a5a98b3a3bd99242fb937ed234850ac0fa4c3c8904ac5144f34e99493a343"
assert VB["concordo_07out"]["sha256"] == "d16bc8a7dc54962e102ed58b4c536411927e48d8ed574adb372febb94c3fdda7"
CLAUS = [("acima de toda escala não trivial, nada porta posto positivo", "above every non-trivial scale, nothing bears a positive post", "nothing_above_bears_a_post"),
         ("a subida não tem topo", "the climb has no top", "the_climb_has_no_top"),
         ("nem teto: a subida é ilimitada", "nor ceiling: the climb is unbounded", "the_climb_is_unbounded"),
         ("a queda nunca toca o zero em escala finita", "the fall never touches zero at finite scale", "the_fall_never_lands"),
         ("o ABISMO: a queda não tem fundo atingido, passa abaixo de todo ε > 0", "the ABYSS: the fall has no bottom reached, it passes below every ε > 0", "abismo"),
         ("o piso ω(I) = 1 fixa o corte, unívoco", "the floor ω(I) = 1 fixes the cut, uniquely", "the_floor_fixes_the_cut"),
         ("ÁGAPE: a composição das seis", "AGAPE: the composition of the six", "agape"),
         ("a conjunção não é vácua (modelo concreto, o Um posto)", "the conjunction is not vacuous (concrete model, the One posited)", "agape_is_inhabited"),
         ("o posto mora na passagem (face finita)", "the post lives in the passage (finite face)", "the_post_lives_in_the_passage")]
assert [c[2] for c in CLAUS] == NOMES
BORCHERS = ["TGLExt.ContratoQGv31.positiveEnergy_orientation", "TGLExt.ContratoQGv31.halfsided_inclusion", "TGLExt.ContratoQGv31.ContratoH2.contract_borchers_form"]
assert all(set(core0["kernel_formalization"]["axiom_report"].get(n) or ["X"]) <= TRIO for n in BORCHERS)
# (4) a copia congelada da memoria da v388: o backup _sup388 (o estado pinado ANTES da cadeia), por sha
MEMB = [f for f in os.listdir(UMEM) if f.startswith("beta-escalar-limitado-inferiormente-06out.md.bak_") and f.endswith("_sup388")]; assert len(MEMB) == 1
_mb = open(os.path.join(UMEM, MEMB[0]), "rb").read()
MEM388 = {"path": os.path.join(UMEM, MEMB[0]).replace("\\", "/"), "sha256": sha256(_mb), "bytes": len(_mb)}
assert MEM388["sha256"] == "c897200c85b95b47397115bfd0a43d1dae48e8858f738f1493d837fb6b38405a"

PINS = ("# ====================== v390 (07/10/2026) -- OS PINOS: lidos dos artefatos por script (gerar_candidato_v390.py), nunca digitados ======================\n"
        "# as 9 bandeiras da pedra TGLExt/Fundacao.lean (auditadas no sandbox); os 3 verbatins do operador EMBUTIDOS (o texto manda; o arquivo so informativo) com os\n"
        "# trechos citados; as 9 clausulas em palavras; os 3 nomes da ponte de Borchers; a copia congelada da memoria da v388 (o backup _sup388) por sha. O gate nao se move.\n"
        "_FND_FLAGS_V390 = [\n" + "".join("    %r,\n" % f for f, _ in FLAGS) + "]\n"
        + "_V390_VERBATINS = " + pprint.pformat(VB, width=150, sort_dicts=False) + "\n"
        + "_V390_PEDRA = " + pprint.pformat({"path": STONE, "sha256": PIN_PEDRA, "bytes": len(stone.encode("utf-8")), "ordem_sha256": sha256(ORDEM)}, width=150, sort_dicts=False) + "\n"
        + "_V390_CLAUSULAS = " + pprint.pformat(CLAUS, width=150) + "\n"
        + "_V390_BORCHERS = " + pprint.pformat(BORCHERS, width=150) + "\n"
        + "_V390_MEM388_CONGELADA = " + pprint.pformat(MEM388, width=150, sort_dicts=False) + "\n")
MEMFN = ("\n\ndef _v390_mem388_congelada():\n"
         "    \"\"\"v390: a copia de bytes CONGELADA do estado pinado da memoria da v388 (o backup _sup388), lida por sha -- INFORMATIVA, fora de qualquer veredito.\"\"\"\n"
         "    import hashlib as _hl\n"
         "    try:\n"
         "        b_ = open(_V390_MEM388_CONGELADA[\"path\"], \"rb\").read()\n"
         "        m_ = _hl.sha256(b_).hexdigest() == _V390_MEM388_CONGELADA[\"sha256\"] == _V388_BETA_ESCALA[\"memoria\"][\"sha256\"]\n"
         "    except OSError:\n"
         "        m_ = None\n"
         "    return {\"path\": _V390_MEM388_CONGELADA[\"path\"], \"sha256\": _V390_MEM388_CONGELADA[\"sha256\"], \"matches_the_pin\": m_, \"informative_only\": True}\n")
_ns = {}; exec(compile(PINS, "<pins>", "exec"), _ns)
assert _ns["_V390_VERBATINS"] == VB and _ns["_FND_FLAGS_V390"] == [f for f, _ in FLAGS] and _ns["_V390_CLAUSULAS"] == CLAUS
open(os.path.join(HERE, "v390_pins.py") + ".tmp", "w", encoding="utf-8", newline="\n").write(PINS); os.replace(os.path.join(HERE, "v390_pins.py") + ".tmp", os.path.join(HERE, "v390_pins.py"))
RT = PINS.rstrip("\n") + MEMFN + "\n\n" + RT_LOGIC
ast.parse(RT)
assert not GUARDA.search(RT.replace("NOT_FALSIFIED nunca é CONFIRMED", "")), "palavra proibida no runtime/pinos (fora da citacao)"

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


A01 = '    "ext_cpl_half_nat_fixed_point_kernel_proved": "TGLExt.TheCouplingRunsBoundedBelow.half_nat_fixed_point",' + CRLF
add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v390 (07/10/2026; a Fundacao -- a superposicao e' a passagem; a clausula agape): fnd (%d)" % len(FLAGS) + CRLF
    + CRLF.join('    "%s": "%s",' % fn for fn in FLAGS) + CRLF, "_LEAN_THEOREM_FLAGS: +%d (ext_fnd_)." % len(FLAGS))
A02 = '        "ext_cpl_half_nat_fixed_point_kernel_proved",' + CRLF
add("V02_escada", "G_PEDRAS", A02, A02 + "        # v390: a Fundacao (%d)" % len(FLAGS) + CRLF + CRLF.join('        "%s",' % f for f, _ in FLAGS) + CRLF, "external_ladder: +%d." % len(FLAGS))
A03 = '    ("v388", "TheCouplingRunsBoundedBelow", "TGLExt/TheCouplingRunsBoundedBelow.lean", None, None),' + CRLF
add("V03_ledger", "G_PEDRAS", A03, A03 + "    # v390 (07/10/2026): a Fundacao -- a superposicao e' a passagem; a clausula agape (o fecho LOGICO do GLOBAL_LIFT; definicao do operador)" + CRLF
    + '    ("v390", "Fundacao", "TGLExt/Fundacao.lean", None, None),' + CRLF, "ledger de pedras: +1.")
patches.append({"id": "V04_kernel", "grupo": "G_PEDRAS", "o_que_muda": "kernel embutido: +1 pedra (Fundacao.lean); TGLExt.lean (+1 import) e TGL/Audit.lean (+9 #print axioms), conferidos byte a byte contra os ANTES."})
m = re.search(r'^UM_VERSION = "v389"[^\r\n]*' + CRLF, T, re.M); assert m
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v390"   # v390 (07/10/2026): a CONSTANTE UNICA de versao -- a Fundacao (a superposicao e\' a passagem; a clausula agape): o fecho LOGICO do GLOBAL_LIFT; v389 em 06/10' + CRLF, "UM_VERSION = 'v390'.")
# (3) erratas AO LADO
E1 = '         "nota": "implicacao PROVADA; antecedente = juramento constitutivo (assinatura, nao divida)"},' + CRLF
add("E01_ledger_lema3", "G_ERRATA", E1, E1[:-len("}," + CRLF)] + "," + CRLF
    + '         "ao_lado_v390": "v390 (07/10/2026), AO LADO (o texto acima fica): o GLOBAL_LIFT lido como a SUPERPOSICAO -- definicao do operador; recusa FECHADO (TGLExt.Fundacao.agape, termo no kernel); '
      'passagem VINCULADO (TGLExt.Fundacao.the_post_lives_in_the_passage, face finita) + SABIDO POR REFERENCIA (Jacobson 1995, H3 nomeada); FECHO LOGICO, programa aberto; ver core.fundacao_v390"},' + CRLF,
    "ledger do fechamento: o item do Lema 3 ganha a leitura v390 AO LADO (nenhum item novo; as contagens nao mudam).")
E2 = '            "extensao_geometrica": "[OPEN] levantamento completo ao espaco-tempo curvo (o velho GLOBAL_LIFT)",' + CRLF
add("E02_what_remains", "G_ERRATA", E2, E2 + '            "extensao_geometrica__ao_lado_v390": "v390 (07/10/2026), AO LADO: o velho GLOBAL_LIFT lido como a SUPERPOSICAO (definicao do operador); a recusa no kernel '
    '(TGLExt.Fundacao.agape) e a passagem local (the_post_lives_in_the_passage + Jacobson 1995 [KNOWN], H3 nomeada): FECHO LOGICO; a lei de campo no curvo segue NAO sendo termo de kernel; ver core.fundacao_v390",' + CRLF,
    "tgl_closure.what_remains_named: +extensao_geometrica__ao_lado_v390.")
E3 = '                  "GLOBAL_LIFT_REMAINS_THE_SINGLE_OPEN_THEOREM"],' + CRLF
add("E03_seals_runtime", "G_ERRATA", E3, '                  "GLOBAL_LIFT_REMAINS_THE_SINGLE_OPEN_THEOREM",   # historico; a leitura v390 ao lado:' + CRLF
    + '                  "GLOBAL_LIFT_IS_THE_SUPERPOSITION__FUNDACAO_AGAPE__LOGICAL_CLOSURE"],' + CRLF, "runtime_of_the_one.seals: +1 ao lado (a antiga fica).")
E4 = '"memory_file": {"path": _V388_BETA_ESCALA["memoria"]["path"], "sha256": _V388_BETA_ESCALA["memoria"]["sha256"], "on_disk_matches": disk},'
add("E04_desenho_v388", "G_ERRATA", E4, '"memory_file": {"path": _V388_BETA_ESCALA["memoria"]["path"], "sha256": _V388_BETA_ESCALA["memoria"]["sha256"], "on_disk_matches": disk, '
    '"estatuto_v390": "INFORMATIVO, FORA DE QUALQUER VEREDITO (v390, errata ao lado da emenda do conferidor de 06/10): a memoria e\' arquivo VIVO -- a cadeia de selo a acrescenta; a copia do estado pinado e\' o backup _sup388 (anterior a cadeia da v388), conferido por sha, INFORMATIVO (nao embutido)", '
    '"copia_congelada": _v390_mem388_congelada()},', "beta_runs_bounded_below_v388: a leitura do disco declarada fora do veredito + a copia do estado pinado por sha (informativa).")
# (+) o ledger da v389 NAO se reconta (afericao v390, CORRIGIR): a contagem do registro da v389 passa a ler o estado da v389 (ate=389); a Parte C le o vivo
_tree = ast.parse(T)
_LED = [ast.literal_eval(n.value) for n in _tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_ESQUELETO_STONES"][0]
_ver = lambda s_: int(str(s_[0])[1:]) if str(s_[0])[:1] == "v" and str(s_[0])[1:].isdigit() else 0
_tup = [s_ for s_ in _LED if isinstance(s_, tuple) and len(s_) > 2]
_ext = {k for k in cand if k.startswith("TGLExt/") and k.endswith(".lean")}


def _conta(ate):
    led = {s_[2] for s_ in _tup if ate is None or _ver(s_) <= ate}; post = set() if ate is None else {s_[2] for s_ in _tup if _ver(s_) > ate}
    fora = (_ext - post) - led
    return [len(led), len(fora), sum(1 for f in fora if f.startswith("TGLExt/O16/"))]


LEDGER = _conta(None); LEDGER389 = _conta(389)
assert LEDGER == [1026, 156, 156] and LEDGER389 == [1025, 156, 156], (LEDGER, LEDGER389)
L0 = ('def _ledger_counts_v389():' + CRLF)
add("L01_ledger_ate_v389", "G_ERRATA", L0, 'def _ledger_counts_v389(ate=None):' + CRLF
    + '    # v390 (07/10/2026), AO LADO: `ate` (o numero da versao) conta so as pedras do ledger ate essa versao e tira do conjunto embutido os caminhos das pedras' + CRLF
    + '    # posteriores -- o registro da v389 le o estado da v389 (1025/156/156); a Parte C le o vivo (ate=None). O pino da v389 NAO se reconta: recontar faria a v389' + CRLF
    + '    # dizer que o exame errou por 11 (ele errou por 10; o +1 e\' a pedra da v390) -- achado da afericao adversarial da v390.' + CRLF,
    "_ledger_counts_v389(ate=None): o corte por versao, ao lado.")
L2 = ('    led_ = {s_[2] for s_ in _ESQUELETO_STONES if isinstance(s_, tuple) and len(s_) > 2}' + CRLF
      + '    ext_ = {k_ for k_ in _EMBEDDED_KERNEL_FILES if k_.startswith("TGLExt/") and k_.endswith(".lean")}' + CRLF
      + '    fora_ = ext_ - led_' + CRLF)
add("L02_ledger_ate_corpo", "G_ERRATA", L2,
    '    _ver_ = lambda s_: int(str(s_[0])[1:]) if str(s_[0])[:1] == "v" and str(s_[0])[1:].isdigit() else 0' + CRLF
    + '    _tup_ = [s_ for s_ in _ESQUELETO_STONES if isinstance(s_, tuple) and len(s_) > 2]' + CRLF
    + '    led_ = {s_[2] for s_ in _tup_ if ate is None or _ver_(s_) <= ate}' + CRLF
    + '    post_ = set() if ate is None else {s_[2] for s_ in _tup_ if _ver_(s_) > ate}' + CRLF
    + '    ext_ = {k_ for k_ in _EMBEDDED_KERNEL_FILES if k_.startswith("TGLExt/") and k_.endswith(".lean")} - post_' + CRLF
    + '    fora_ = ext_ - led_' + CRLF, "o corpo do corte por versao.")
L3 = '    n_led, n_fora, n_o16 = _ledger_counts_v389()' + CRLF
add("L03_registro_v389_ate", "G_ERRATA", L3, '    n_led, n_fora, n_o16 = _ledger_counts_v389(ate=389)   # v390, ao lado: o registro da v389 le o estado da v389' + CRLF, "text_label_errata_v389: conta ate a v389.")
A_P = linha_unica(r"^# ====================== v389 \(06/10/2026\) -- OS PINOS:")
add("W02_runtime", "G_RUNTIME", A_P, crlf(RT.rstrip("\n") + "\n\n\n") + A_P, "runtime v390: os pinos + _v390_mem388_congelada + fundacao_v390.")
A_R = linha_unica(r'^    print\("   \[v389\] as erratas de texto e rotulo do exame da v388')
reg = ['    try:   # v390: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito',
       '        core["fundacao_v390"] = fundacao_v390(core)   # v390 [ao lado do gate; o fecho LOGICO do GLOBAL_LIFT]',
       '    except Exception as _e390:',
       '        core["fundacao_v390"] = {"verdict": "TGL_FUNDACAO_V390__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e390)[:400], "does_not_gate_core": True}',
       '    print("   [v390] a Fundacao -- a superposicao e\' a passagem; a clausula agape (o fecho LOGICO do GLOBAL_LIFT): %s" % core["fundacao_v390"]["verdict"])']
add("W04_registro", "G_RUNTIME", A_R, A_R + CRLF.join(reg) + CRLF, "core: +1 chave v390.")
PT0 = open(os.path.join(HERE, "artigo_pt_v390.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v390.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn)
    assert not GUARDA.search(sn)
P9 = os.path.join(WK, "v389_pacote")
PT9_FIRST = open(os.path.join(P9, "artigo_pt_v389.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN9_FIRST = open(os.path.join(P9, "artigo_en_v389.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
add("W05_artigo_PT", "G_ARTIGO", PT9_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT9_FIRST, "artigo PT: «A Fundação», antes da v389.")
add("W06_artigo_EN", "G_ARTIGO", EN9_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN9_FIRST, "artigo EN: «The Foundation», before v389.")
R_PT = '             r"replicada e \\textbf{verificada ao vivo}, com os estatutos separados.")' + CRLF + '    s.append(r"\\end{abstract}")' + CRLF
R_EN = '             r"dipole) is replicated and \\textbf{verified live}, with the statuses kept separate.")' + CRLF + '    s.append(r"\\end{abstract}")' + CRLF
FR_PT = ('    _fa390 = core.get("fundacao_v390") or {}   # v390: UMA frase da Fundacao no resumo (a W10 da GPU e a dos tres testes ficam)' + CRLF
         + '    s.append(r"\\textbf{A Fundação (v390).} O velho Lema 3 (GLOBAL\\_LIFT) é lido como a superposição --- definição do operador ---, e a cláusula Ágape prova no kernel, sobre a lei de escala de Takesaki tomada como dado [KNOWN], que acima da escala não há posto positivo ("'
         + ' + (str(_fa390.get("kernel_flags_ok")) + r" de " + str(_fa390.get("kernel_flags_total")) + r" declarações no kernel" if _fa390.get("all_verified") is True else r"\\textbf{não selada nesta rodada}")'
         + ' + r"): o fecho é lógico, o programa segue aberto e o gate não se move.")' + CRLF)
FR_EN = ('    _fa390 = core.get("fundacao_v390") or {}   # v390: ONE sentence of the Foundation in the abstract (the GPU W10 and the three-tests sentences stay)' + CRLF
         + '    s.append(r"\\textbf{The Foundation (v390).} The old Lemma 3 (GLOBAL\\_LIFT) is read as the superposition --- the operator\'s definition ---, and the Agape clause proves in the kernel, on Takesaki\'s scaling law taken as data [KNOWN], that above the scale there is no positive post ("'
         + ' + (str(_fa390.get("kernel_flags_ok")) + r" of " + str(_fa390.get("kernel_flags_total")) + r" declarations in the kernel" if _fa390.get("all_verified") is True else r"\\textbf{not sealed in this run}")'
         + ' + r"): the closure is logical, the programme stays open and the gate does not move.")' + CRLF)
add("W09_resumo_PT", "G_ARTIGO", R_PT, R_PT.replace('    s.append(r"\\end{abstract}")' + CRLF, FR_PT + '    s.append(r"\\end{abstract}")' + CRLF), "resumo PT: +1 frase da Fundação.")
add("W10_resumo_EN", "G_ARTIGO", R_EN, R_EN.replace('    s.append(r"\\end{abstract}")' + CRLF, FR_EN + '    s.append(r"\\end{abstract}")' + CRLF), "abstract EN: +1 sentence of the Foundation.")
A_S = linha_unica(r'^ {12}"text_label_errata_v389": \{k_: ')
_sel = ["            # v390 (07/10/2026) -- a Fundacao (a clausula agape): registro AO LADO do gate; nenhum valor do gate muda",
        '            "fundacao_v390": {k_: (core.get("fundacao_v390") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "pedra", "verbatim_ok", "leitura", "recusa", "passagem", "estatuto_do_fecho", "not_claimed", "borchers")},']
add("W07_selo", "G_SELO", A_S, A_S + CRLF.join(_sel) + CRLF, "selo: +1 registro v390.")
A_M = linha_unica(r'^    md\.append\("> \*\*Ao lado \(v389, 06/10/2026\):\*\*')
add("W08_md", "G_ARTIGO", A_M, A_M + '    md.append("> **A Fundação (v390, 07/10/2026):** a superposição é a passagem — a pedra `TGLExt.Fundacao` (9 nomes; a cláusula `agape`; `fundacao_v390`): o GLOBAL_LIFT, o velho Lema 3, lido como a superposição '
    + '(definição do operador); a recusa provada no kernel; a passagem local [KNOWN, Jacobson 1995, H3 nomeada]. Fecho LÓGICO; o programa segue aberto; o gate não muda.\\n\\n")' + CRLF, "md canonico: a linha «A Fundação (v390)».")
# ---------- guardas finais ----------
assert T.count("def fundacao_v390(") == 1 and T.count('core["fundacao_v390"] = ') == 2 and T.count("def _v390_mem388_congelada(") == 1
for f, _ in FLAGS:
    assert T.count('"%s"' % f) == 2 and T.count("'%s'" % f) == 1, f
assert T.count("GLOBAL_LIFT_REMAINS_THE_SINGLE_OPEN_THEOREM") == 1 + T.count("GLOBAL_LIFT_REMAINS_THE_SINGLE_OPEN_THEOREM\"") - 1   # a antiga fica
b = T.encode("utf-8"); ast.parse(T)
out = os.path.join(HERE, "um_v390_candidato.py")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v389_sha16": SHA0, "escada": [E389, E389 + len(FLAGS)], "kernel": KERNEL,
       "flags": [f for f, _ in FLAGS], "nomes": QN, "pins_sha16": sha16(PINS.encode("utf-8")), "verbatins": {k: {x: v[x] for x in ("sha256", "bytes")} for k, v in VB.items()},
       "ordem_sha256": sha256(ORDEM), "pedra_sha256": PIN_PEDRA, "ledger": LEDGER, "mem388": MEM388, "patches": patches, "snips": {"pt0": sha16(PT0.encode()), "en0": sha16(EN0.encode())}}
open(os.path.join(HERE, "CANDIDATO_v390.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v390.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v390.json"))
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v389_sha16", "escada", "kernel", "verbatins", "ledger")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(patches), [p["id"] for p in patches])
