# -*- coding: utf-8 -*-
"""gerar_candidato_v395.py -- gera o um.py CANDIDATO v395 a partir da v394 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v394.py. PREPARACAO de 21/10/2026 (gerencia c1).
Conteudo (enxuto: so' o que tem funcao):
 (A) kernel: +1 modulo (TGLExt/Psibit.lean, 2a versao, PEDRA_APROVADA na rodada 2 do exame independente) + raiz + Audit (o import), conferidos byte a byte com o sandbox C:\\t\\k395c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394), escada, ledger, UM_VERSION;
 (C) os contratos v394 que pinam a escada (tempo, quadratica, rede) sobem para a escada da v395 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v394 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo: psibit_v395 (o modo psionico na fractalizacao do Um: contrato derivado do MEU build, mecanica calculada com beta = alfa CODATA 2018 x sqrt(e) em runtime), as quatro falas do operador de 21/10 embutidas
     por sha256, os registros por spec cunhagens_v395 e kh_n1_cobertura_v395; chamadas no main (a de psibit_v395 no PONTO DE CHAMADA REAL da fractalizacao do Um) e no selo;
 (E) artigo PT/EN (secao v395) e md.
uso: python -I -B -X utf8 gerar_candidato_v395.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v395 as GP  # noqa: E402
import registros_v395 as RG  # noqa: E402
import delta_v395 as DL  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP394 = json.load(open(os.path.join(DL.V394, "ESPERADOS_v394.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP394["candidato_sha16"]:   # o Nos ja nao e' a v394 (rito v395 em curso): a v394 SELADA vem da copia base_v394
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v394 selada"
SHA0 = sha16(raw); assert SHA0 == ESP394["candidato_sha16"]
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E394 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E394 == ESP394["escada"][1], (E394, ESP394["escada"])
T0 = raw.decode("utf-8")
tree0 = ast.parse(T0)
LS = [0] + [m.end() for m in re.finditer("\n", T0)]


def pos(tx_ls, lineno, col_bytes, text):
    line = text[tx_ls[lineno - 1]:tx_ls[lineno]] if lineno < len(tx_ls) else text[tx_ls[lineno - 1]:]
    return tx_ls[lineno - 1] + len(line.encode("utf-8")[:col_bytes].decode("utf-8"))


def span(node):
    return pos(LS, node.lineno, node.col_offset, T0), pos(LS, node.end_lineno, node.end_col_offset, T0)


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def top(name, tree=tree0):
    c = [n for n in tree.body if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name) or (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name)]
    assert len(c) == 1, (name, len(c))
    return c[0]


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


EDITS = []   # (a, b, novo, id, grupo, o_que)


def edit(a, b, novo, pid, grupo, o_que):
    EDITS.append((a, b, novo, pid, grupo, o_que))


def replace_unique(old, new, pid, grupo, o_que, n=1):
    assert T0.count(old) == n, (pid, T0.count(old), n)
    i = T0.index(old); edit(i, i + len(old), new, pid, grupo, o_que)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T0, re.M); assert m_ and T0.count(m_.group(0)) == 1, rx
    return m_


# ---------------- (1) o kernel ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v395.json"), encoding="utf-8"))["novos"]; assert nov == [DL.STONE_REL], "a lista dos modulos novos tem de ser so' a pedra Psibit"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v394 + o import da pedra"
STONE = rd(os.path.join(KB, *DL.STONE_REL.split("/")))
assert STONE == rd(DL.STONE_SRC), "a pedra do sandbox difere da fonte autoral (work\\psibit_v395\\Psibit.lean)"
assert DL.STONE_REL not in old_d
assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONE, flags=re.S)), "sorry no codigo da pedra"
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (+ o import da pedra Psibit; sandbox == embutido)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "    %r: %s,%s" % (DL.STONE_REL, repr(STONE), CRLF), "K01_modulo_novo", "G_KERNEL", "kernel embutido: +1 modulo Lean (TGLExt/Psibit.lean, a pedra do psibit), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb[DL.STONE_REL] = STONE
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v395.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v394"
assert all(DL.classe(n) == "nomeada" and m == DL.STONE_MOD for _, n, m in FL) and FJ["n_flags"] == len(FL)
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v395 (21/10/2026): a pedra Psibit (a leitura psibit da orbita do Um pela matriz-S): %d bandeiras, SO' de declaracao NOMEADA (a pratica da v392, v393 e v394; as %d auxiliares geradas pelo compilador ficam fora)" % (len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E394 and len(set(old_lad)) == E394
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v395: a pedra Psibit (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v395 (21/10/2026): a pedra Psibit (a leitura psibit da orbita do Um pela matriz-S; o nome e' do operador)" + CRLF + '    ("v395", "%s", "%s", None, None),%s' % (DL.STONE_NAME, DL.STONE_REL, CRLF), "V03_ledger", "G_KERNEL", "ledger de pedras: +1.")
m = re.search(r'^UM_VERSION = "v394"[^\r\n]*' + CRLF, T0, re.M); assert m
edit(m.start(), m.end(), 'UM_VERSION = "v395"   # v395 (21/10/2026): a CONSTANTE UNICA de versao -- o modo psionico na fractalizacao do Um (a pedra Psibit, o registro psibit_v395 e as quatro falas do operador de 21/10); v394 em 19/10' + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v395'.")

# ---------------- (3) o que a v395 muda nos registros da v394 ----------------
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT"):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E394
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V394_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E394, ESCADA_ESP))
sv = top("_V394_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs394 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs394, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
khs = [s for s in specs394 if s["nome"] == "kh_n1_cobertura_v394"]; assert len(khs) == 1
k4 = khs[0]
H8_ANTIGO_N = None
for c in k4["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v395: piso historico (a cobertura cresce com o modulo Psibit); a igualdade exata esta em kh_n1_cobertura_v395"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v395: piso historico; a igualdade exata esta em kh_n1_cobertura_v395"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v395: a arvore ganha o arquivo da pedra, entao o registro da v394 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v395" % H8_ANTIGO_N
k4["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v394 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v394 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v394 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v395 a cobertura cresce com o modulo Psibit e a arvore ganha o arquivo da pedra: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v395. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v394 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v395 quebra (achado no ensaio a seco e na arvore simulada do Nos)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; conferidas no ensaio a seco]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k4["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v394"
edit(spa, spb, pprint.pformat(specs394, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v394_pisos", "G_V394_PISOS", "_V394_SPECS: kh_n1_cobertura_v394 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (4) main: chamadas e selo ----------------
A_PSB = re.escape('    print("  >>> existir E\' o vazamento beta; a anticomutacao perfeita (nada absoluto) e\' inalcancavel. <<<\\n")')
m_psb = re.search("^" + A_PSB + r"\r\n", T0, re.M); assert m_psb and T0.count(m_psb.group(0)) == 1, "ancora da fractalizacao do Um (principio da defasagem fractal) nao achada ou nao unica"
psb = ['    try:   # v395: o modo psionico NA FRACTALIZACAO DO UM (psibit): a mecanica da orbita do Um pela matriz-S em theta_M, calculada agora e lida contra os termos do kernel do proprio rito; excecao vira AVISO visivel, nunca derruba o rito',
       '        _psb395 = psibit_v395(core)',
       '        _psv395 = _psb395.get("values") or {}',
       '        _nan395 = float("nan")',
       '        print("PSIBIT [v395 -- o modo psionico na fractalizacao do Um; [REAL] os termos do kernel e o calculo, [INPUT/ONTO] psibit = psion = modo do leitor]:")',
       '        print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime; um dado, dois nomes: SEALED_CODATA_ALPHA = ALPHA_FINE_CODATA_2018) ; theta_M = arcsin sqrt(beta) = %.12f rad (%.6f graus)" % (_psv395.get("beta", _nan395), _psv395.get("theta_M_rad", _nan395), _psv395.get("theta_M_deg", _nan395)))',
       '        print("  rho_out(theta_M) = F_theta(1) = [[c^2, -cs], [-sc, s^2]]: c^2 = %.12f ; -cs = %.12f ; s^2 = %.12f (= beta)" % ((_psv395.get("collapse_diagonal") or [_nan395, _nan395])[0], _psv395.get("coherence", _nan395), (_psv395.get("collapse_diagonal") or [_nan395, _nan395])[1]))',
       '        print("  codigo psibit (peso, sign L, sign dL) = (%.12f, %+d, %+d) ; paridade = produto = %+d ; decodificacao: residuo %.1e (limite 1e-12)" % (_psv395.get("code_weight", _nan395), _psv395.get("code_word", 0), _psv395.get("code_verb", 0), _psv395.get("parity", 0), _psv395.get("decode_residual", _nan395)))',
       '        print("  colapso D_inf: rho(theta) e rho(-theta) tem a MESMA diagonal (dif %.1e) e coerencias OPOSTAS (%+.9f e %+.9f): o colapso perde exatamente a paridade, um bit; a leitura do par perde zero" % (_psv395.get("collapse_diag_difference", _nan395), _psv395.get("coherence", _nan395), _psv395.get("coherence_neg_theta", _nan395)))',
       '        print("  Verbo = (1/2) d(Nome)/d(theta): residuo %.1e ; nos pesos iguais a entropia dos resultados e\' ln 2 = %.12f (residuo %.1e)" % (_psv395.get("verb_derivative_residual", _nan395), _psv395.get("ln2", _nan395), _psv395.get("entropy_balanced_residual", _nan395)))',
       '        print("  kernel: composicao INCONDICIONAL = %s [%s] ; face do psion = %s (condicional ao certificado de Fock, sem habitante exibido)" % ((_psb395.get("unconditional") or {}).get("in_kernel"), (_psb395.get("unconditional") or {}).get("flag"), (_psb395.get("conditional_psion_face") or {}).get("status")))',
       '        print("  >>> %s <<<\\n" % _psb395["verdict"])',
       '    except Exception as _e395:',
       '        print("   [v395] AVISO: o modo psionico (psibit) nao rodou: %r" % (_e395,))']
edit(m_psb.end(), m_psb.end(), CRLF.join(psb) + CRLF, "N00_main_psibit", "G_RUNTIME", "main: psibit_v395(core) chamado NA FRACTALIZACAO DO UM (logo depois do principio da defasagem fractal), com try/AVISO.")
A_R = linha_unica(r'^        print\("   \[v394\] AVISO: o tempo/frequencia, a regra quadratica, a rede ou os registros v394 nao rodaram')
reg = ['    try:   # v395: os registros por spec da v395 (as quatro falas do operador de 21/10, lidas junto com o psibit_v395 da fractalizacao, e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito',
       '        _n395 = _v395_rodar_specs(core)',
       '        print("   [v395] o modo psionico (psibit, lido na fractalizacao do Um): %s | registros por spec: %d (selados %d)" % ((core.get("psibit_v395") or {}).get("verdict"), len(_n395), sum(1 for k_ in _n395 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e395b:',
       '        print("   [v395] AVISO: os registros por spec da v395 nao rodaram: %r" % (_e395b,))']
edit(A_R.end(), A_R.end(), CRLF.join(reg) + CRLF, "N01_main_specs", "G_RUNTIME", "main: registros por spec v395 (try/AVISO), depois do bloco v394.")
A_S = linha_unica(r'^ {12}"registros_v394": \{n_: ')
_sel = ['            "psibit_v395": {k_: (core.get("psibit_v395") or {}).get(k_) for k_ in ("verdict", "all_verified", "unconditional", "conditional_psion_face", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "registros_v395": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V395_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +psibit_v395 e registros_v395.")

# ---------------- (5) o bloco de runtime v395 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v395.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]; assert set(axm[DL.THEOREM]) == TRIO and set(axm[DL.THEOREM_COND]) <= TRIO
N_AX_UNC = len(axm[DL.THEOREM])
CONTR = RG.contrato(FJ, FORMAL_MAP, E394, sha256(raw)); assert CONTR["expected_ladder"] == ESCADA_ESP
TXT = RG.texto_psibit()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes["psibit_pedra"]["sha256"] == FORMAL_MAP[DL.STONE_REL], "a copia duravel da pedra difere da embutida"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v394, por ast)
NOSK = os.path.join(DL.NOS, "tgl_kernel")
_ns_h8 = {"os": os, "hashlib": hashlib}
for _nm in ("sha_file", "sha256_directory"):
    exec(compile(ast.get_source_segment(T0, top(_nm)), "<um:%s>" % _nm, "exec"), _ns_h8)
SIMD = os.path.join(HERE, "arvore_simulada_h8")
if os.path.isdir(SIMD):
    shutil.rmtree(SIMD)
for rel, c_ in final_emb.items():
    p_ = os.path.join(SIMD, *rel.split("/")); os.makedirs(os.path.dirname(p_), exist_ok=True); open(p_, "w", encoding="utf-8", newline="").write(c_)
H8_EXTRAS = []
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\", "/")
            if rel_ not in final_emb:
                H8_EXTRAS.append(rel_); d_ = os.path.join(SIMD, *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(dp_, nm_), d_)
H8 = _ns_h8["sha256_directory"](SIMD)["files"]
assert all(H8.get(k_) == v_ for k_, v_ in FORMAL_MAP.items()) and set(H8) - set(FORMAL_MAP) <= set(H8_EXTRAS), "o hash formal simulado difere do FORMAL_MAP nos embutidos"
specs = RG.especs(FORMAL_MAP, khj, H8, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], N_AX_UNC)
spec_nomes = [s["nome"] for s in specs]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert not GP.violacoes(json.dumps(TXT, ensure_ascii=False)), GP.violacoes(json.dumps(TXT, ensure_ascii=False))[:3]
assert not GUARDA.search(TXT["veredito_ok"])
HDR = ("# ====================== v395 (21/10/2026) -- O MODO PSIONICO NA FRACTALIZACAO DO UM: a pedra Psibit, o registro psibit_v395 e as quatro falas do operador de 21/10. O contrato e' DERIVADO do build do sandbox desta cadeia\n"
       "# (gerar_candidato_v395.py), nunca digitado; a fonte autoral da funcao e' runtime_psibit_v395.py; as falas entram EMBUTIDAS por sha256. O gate nao se move. ======================\n")
RUNTIME_SRC = open(os.path.join(HERE, "runtime_psibit_v395.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
RCODE = ("_V395_PSIBIT_CONTRACT = " + pprint.pformat(CONTR, width=150, sort_dicts=False) + "\n_V395_PSIBIT_TEXT = " + pprint.pformat(TXT, width=150, sort_dicts=False) + "\n\n\n"
         "_V395_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V395_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V395_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V395_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V395_FONTES)   # v395: o motor de registros (v392) le as fontes e os verbatins das quatro versoes\n_V392_VERBATINS2.update(_V395_VERBATINS2)\n\n\n"
         "def _v395_rodar_specs(core_):\n"
         '    """v395 -- roda os registros por spec da v395 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito."""\n'
         "    for spec_ in _V395_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V395_SPECS]\n')
RT = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v395: o contrato (derivado do build), as falas do operador e os registros por spec\n" + RCODE
ast.parse(RT)
_novo_texto = RUNTIME_SRC + json.dumps(CONTR, ensure_ascii=False) + json.dumps(TXT, ensure_ascii=False) + json.dumps(specs, ensure_ascii=False)   # as falas do operador (verbatim) ficam fora da guarda: a guarda vale para o texto NOVO
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v394 \(19/10/2026\) -- A INTEGRACAO DO CODEX E AS CUNHAGENS DE 14 A 19/10: pinos e runtime")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v395", "G_RUNTIME", "bloco v395: psibit_v395 (mecanica + contrato derivado do build), as quatro falas, registros por spec.")

# ---------------- (6) artigo e md ----------------
PT0 = open(os.path.join(HERE, "artigo_pt_v395.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v395.pysnip"), encoding="utf-8").read()
def _controles(obj, onde):
    """Guarda de CARACTERE DE CONTROLE (licao desta cadeia: o heredoc do Bash colapsa `\\\\` em `\\` e `\\texttt` virou TAB + `exttt`): nenhuma string de texto novo pode ter caractere de controle alem do fim de linha."""
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo (barra invertida colapsada?)", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RUNTIME_SRC, "runtime_psibit_v395.py"); _controles([CONTR, TXT, specs, fontes], "contrato/texto/specs/fontes")
PT1_FIRST = open(os.path.join(DL.V394, "artigo_pt_v394.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(DL.V394, "artigo_en_v394.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v395, antes da v394.")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v395, antes da v394.")
A_M = linha_unica(r'^    md\.append\("> \*\*A integração do Codex e as cunhagens \(v394, 19/10/2026\):\*\*')
edit(A_M.end(), A_M.end(), '    md.append("> **O modo psiônico na fractalização do Um (v395, 21/10/2026):** ' + str(N_NOVOS) + ' módulo novo no kernel (`TGLExt/Psibit`, o nome é do operador), ' + str(len(FL)) + ' bandeiras só de declaração nomeada, o registro `psibit_v395` chamado na fractalização do Um (a mecânica da órbita do Um pela matriz-S em θ_M, calculada com β = α·√e em runtime e lida contra a conjunção incondicional do kernel), as quatro falas do operador de 21/10 embutidas por sha256 (`cunhagens_v395`) e a cobertura exata do Audit (`kh_n1_cobertura_v395`). A leitura do par (peso, Palavra, Verbo) não perde nada (bijeção de conjuntos sobre o livro de códigos, não isomorfismo de Hilbert); o colapso perde exatamente a paridade; a face do psion é condicional a um certificado sem habitante; psibit = psion = modo do leitor é leitura do operador [INPUT/ONTO]; validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF,
     "W07_md", "G_ARTIGO", "md canonico: a linha «O modo psiônico na fractalização do Um (v395)».")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
T = T0
for a, b, novo, *_ in sorted(EDITS, key=lambda e: -e[0]):
    T = T[:a] + novo + T[b:]
ast.parse(T)
tree = ast.parse(T)
for n in ("psibit_v395", "v395_psibit_mechanics", "_v395_rodar_specs", "_V395_PSIBIT_CONTRACT", "_V395_SPECS", "_V395_NOMES_REGISTROS", "_V395_VERBATINS2", "_V395_PSIBIT_TEXT"):
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V394_SPECS", tree).value) == specs394
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V395_REGERAR") == "1", "o candidato ja existe e difere: defina V395_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v394_sha16": SHA0, "escada": [E394, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS],
       "kernel": {"modulos_novos": N_NOVOS, "pedra": {"path": DL.STONE_REL, "sha16": sha16(STONE.encode()), "sha256": sha256(STONE.encode())}, "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()),
                  "raiz_v394_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v394_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "contrato_psibit": {"sha16": sha16(pprint.pformat(CONTR, width=150, sort_dicts=False).encode()), "n_teoremas": len(CONTR["theorems"]), "bandeira_incondicional": CONTR["unconditional"]["flag"], "bandeira_condicional": CONTR["conditional"]["flag"], "expected_ladder": CONTR["expected_ladder"]},
       "registros": spec_nomes + ["psibit_v395"], "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E394, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v395.json (pos_build_kernel_v395.py)"},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v394_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v394_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_do_teorema_incondicional": N_AX_UNC,
       "ponto_de_chamada": {"psibit_v395": "main: logo depois do principio da defasagem fractal (fd = core['fractal_dephasing']), na fractalizacao do Um", "specs": "main: depois do bloco [v394]"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v395.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v395.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v395.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v395.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v395_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v394_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v394:", PFORMAT_IDEMPOTENTE)
