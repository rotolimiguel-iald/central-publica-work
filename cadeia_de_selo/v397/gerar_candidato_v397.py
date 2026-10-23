# -*- coding: utf-8 -*-
"""gerar_candidato_v397.py -- gera o um.py CANDIDATO v397 a partir da v396 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v396.py. PREPARACAO de 23/10/2026 (gerencia c1).
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +1 modulo (TGLExt/Token.lean: o nome «token» e' do operador; compoe por citacao o psibit e a testemunha estatica) + raiz + Audit (o import), conferidos byte a byte com o sandbox C:\\t\\k397c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395 e testemunha da v396) sobem para a escada da v397 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v396 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo: o REGISTRO teste_de_veracidade_fase9_v397 (SPEC: le por sha256 o resultado do Teste da Unica Palavra e os tres recibos, ao lado do V1; nenhum sigma novo; chamado no ponto real do main logo depois de
     hubble_ratio_opening_v388), as SEIS falas do operador de 23/10 embutidas por sha256, os registros por spec cunhagens_v397 e kh_n1_cobertura_v397, as funcoes puras do QUADRO; chamadas no main e no selo;
 (E) o QUADRO «O Teste da Unica Palavra» no TOPO do artigo PT/EN (logo abaixo do titulo) e do .md; a secao curta PT/EN e a linha do .md.
uso: python -I -B -X utf8 gerar_candidato_v397.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v397 as GP  # noqa: E402
import registros_v397 as RG  # noqa: E402
import delta_v397 as DL  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP396 = json.load(open(os.path.join(DL.V396, "ESPERADOS_v396.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP396["candidato_sha16"]:   # o Nos ja nao e' a v396 (rito v397 em curso): a v396 SELADA vem da copia base_v396
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v396 selada"
SHA0 = sha16(raw); assert SHA0 == ESP396["candidato_sha16"]
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E396 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E396 == ESP396["escada"][1], (E396, ESP396["escada"])
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


def depois_do_comando(funcao, agulhas, pid, grupo, o_que, novo):
    """Insere `novo` (texto com CRLF) logo depois do UNICO comando do corpo de `funcao` (por AST) cujo texto contem todas as `agulhas`."""
    fn = top(funcao); cands = []
    for st in fn.body:
        a, b = span(st); seg = T0[a:b]
        if all(x in seg for x in agulhas):
            cands.append((a, b))
    assert len(cands) == 1, (pid, funcao, agulhas, len(cands))
    b = cands[0][1]
    assert T0[b:b + 2] == CRLF, (pid, "o comando nao termina em CRLF")
    edit(b + 2, b + 2, novo, pid, grupo, o_que)


# ---------------- (1) o kernel ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v397.json"), encoding="utf-8"))["novos"]; assert nov == [DL.STONE_REL], "a lista dos modulos novos tem de ser so' a pedra Token"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v396 + o import da pedra"
STONE = rd(os.path.join(KB, *DL.STONE_REL.split("/")))
assert STONE == rd(DL.STONE_SRC), "a pedra do sandbox difere da fonte autoral (v397\\pedra\\Token.lean): rode refazer_sandbox_v397.sh"
assert DL.STONE_REL not in old_d
assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONE, flags=re.S)), "sorry no codigo da pedra"
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (+ o import da pedra Token; sandbox == embutido)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "    %r: %s,%s" % (DL.STONE_REL, repr(STONE), CRLF), "K01_modulo_novo", "G_KERNEL", "kernel embutido: +1 modulo Lean (TGLExt/Token.lean, a pedra Token), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb[DL.STONE_REL] = STONE
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v397.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v396"
assert all(DL.classe(n) == "nomeada" and m == DL.STONE_MOD for _, n, m in FL) and FJ["n_flags"] == len(FL) and [n for _, n, _ in FL] == [DL.THEOREM], "as bandeiras da pedra Token tem de ser exatamente a do teorema da conjuncao"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v397 (23/10/2026): a pedra Token (o nome e' do operador; compoe por citacao o psibit e a testemunha estatica): %d bandeira, SO' de declaracao NOMEADA (a pratica da v392 a v396; as %d auxiliares geradas pelo compilador ficam fora)" % (len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E396 and len(set(old_lad)) == E396
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v397: a pedra Token (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v397 (23/10/2026): a pedra Token (o nome «token» e' do operador, 23/10; que ele nomeia a pedra da testemunha estatica e' o contexto registrado pela gerencia; compoe por citacao psibit_is_the_mode_of_the_reader e the_psion_inhabits_the_static_witness; nenhuma matematica nova)" + CRLF + '    ("v397", "%s", "%s", None, None),%s' % (DL.STONE_NAME, DL.STONE_REL, CRLF), "V03_ledger", "G_KERNEL", "ledger de pedras: +1.")
m = re.search(r'^UM_VERSION = "v396"[^\r\n]*' + CRLF, T0, re.M); assert m
edit(m.start(), m.end(), 'UM_VERSION = "v397"   # v397 (23/10/2026): a CONSTANTE UNICA de versao -- o Teste da Unica Palavra lido por hash (o registro teste_de_veracidade_fase9_v397), a pedra Token e as seis falas do operador de 23/10; v396 em 22/10' + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v397'.")

# as bandeiras dos dois termos de suporte que a pedra cita (ja' no ladder da v396): a inversa de _LEAN_THEOREM_FLAGS (nome -> chave), lida do candidato, nunca digitada
inv_flags = {n: k for k, n in old_flags.items()}
FLAGS_SUP = {t: inv_flags[t] for t in DL.SUPPORT_THEOREMS}
FJX = dict(FJ); FJX["bandeira_do_teorema"] = FL[0][0]; FJX["bandeiras_do_suporte"] = FLAGS_SUP

# ---------------- (3) o que a v397 muda nos registros das versoes anteriores (so' dados) ----------------
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT"):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E396
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V396_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E396, ESCADA_ESP))
sv = top("_V396_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs396 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs396, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
khs = [s for s in specs396 if s["nome"] == "kh_n1_cobertura_v396"]; assert len(khs) == 1
k6 = khs[0]
H8_ANTIGO_N = None
for c in k6["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v397: piso historico (a cobertura cresce com o modulo Token); a igualdade exata esta em kh_n1_cobertura_v397"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v397: piso historico; a igualdade exata esta em kh_n1_cobertura_v397"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v397: a arvore ganha o arquivo da pedra, entao o registro da v396 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v397" % H8_ANTIGO_N
k6["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v396 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v396 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v396 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v397 a cobertura cresce com o modulo Token e a arvore ganha o arquivo da pedra: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v397. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v396 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v397 quebra (a mesma lacuna que a v396 achou no registro da v395)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; conferidas no ensaio a seco]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k6["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v396"
edit(spa, spb, pprint.pformat(specs396, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v396_pisos", "G_V396_PISOS", "_V396_SPECS: kh_n1_cobertura_v396 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (4) main: chamadas e selo ----------------
# N00 -- o registro do Teste da Unica Palavra, no PONTO REAL em que a Fase 9 do V1 e' lida (logo depois do bloco hubble_ratio_opening_v388), AO LADO dele
A_H = linha_unica(r'^    print\("   \[v388\] a Fase 9 aberta pela funcao congelada \(o resultado por hash; a funcao reexecutada\): %s" % core\["hubble_ratio_opening_v388"\]\["verdict"\]\)')
ver = ['    try:   # v397: o REGISTRO do resultado do Teste da Unica Palavra (Fase 9 V2-c1, aberto UMA vez em 23/10/2026), lido por sha256 junto com os tres recibos, AO LADO do V1 (o V1 fica); nenhum sigma novo; excecao vira AVISO visivel (all_verified False), nunca derruba o rito',
       '        core["teste_de_veracidade_fase9_v397"] = _v392_registro(_V397_VERACIDADE_SPEC, core)   # v397 [ao lado do gate]',
       '    except Exception as _e397:',
       '        core["teste_de_veracidade_fase9_v397"] = {"verdict": "TGL_FASE9_VERACIDADE_V397__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e397)[:400], "does_not_gate_core": True}',
       '    print("   [v397] o Teste da Unica Palavra (Fase 9 V2-c1, aberto uma vez em 23/10), lido por hash ao lado do V1 (nenhum sigma novo): %s" % core["teste_de_veracidade_fase9_v397"]["verdict"])']
edit(A_H.end(), A_H.end(), CRLF.join(ver) + CRLF, "N00_main_veracidade", "G_RUNTIME", "main: o registro teste_de_veracidade_fase9_v397 chamado logo depois do bloco hubble_ratio_opening_v388 (ao lado do V1), com try/AVISO.")
A_R = linha_unica(r'^        print\("   \[v396\] AVISO: os registros por spec da v396 nao rodaram')
reg = ['    try:   # v397: os registros por spec da v397 (as seis falas do operador de 23/10, a pedra Token e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito',
       '        _n397 = _v397_rodar_specs(core)',
       '        print("   [v397] a pedra Token e as falas de 23/10 (cunhagens_v397): %s | registros por spec: %d (selados %d)" % ((core.get("cunhagens_v397") or {}).get("verdict"), len(_n397), sum(1 for k_ in _n397 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e397b:',
       '        print("   [v397] AVISO: os registros por spec da v397 nao rodaram: %r" % (_e397b,))']
edit(A_R.end(), A_R.end(), CRLF.join(reg) + CRLF, "N01_main_specs", "G_RUNTIME", "main: registros por spec v397 (try/AVISO), depois do bloco v396.")
A_S = linha_unica(r'^ {12}"registros_v396": \{n_: ')
_sel = ['            "teste_de_veracidade_fase9_v397": {k_: (core.get("teste_de_veracidade_fase9_v397") or {}).get(k_) for k_ in ("verdict", "all_verified", "lido", "does_not_gate_core")},',
        '            "registros_v397": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V397_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +teste_de_veracidade_fase9_v397 (com os numeros lidos) e registros_v397.")

# ---------------- (5) o bloco de runtime v397 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v397.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]; assert set(axm[DL.THEOREM]) == TRIO
N_AX_UNC = len(axm[DL.THEOREM])
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes["token_pedra"]["sha256"] == FORMAL_MAP[DL.STONE_REL], "a copia duravel da pedra difere da embutida"
F9 = RG.f9_dados()
for k_ in F9:
    assert fontes[k_]["sha256"] == F9[k_]["sha256"], ("a fonte duravel do Teste da Unica Palavra difere da lida", k_)
assert fontes["f9v2_resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v396, por ast)
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
spec_verac = RG.espec_veracidade(F9)
specs = RG.especs(FORMAL_MAP, khj, H8, FJX, core0["kernel_formalization"]["axiom_coverage_v392"], N_AX_UNC)
spec_nomes = [s["nome"] for s in specs]
for s in [spec_verac] + specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
HDR = ("# ====================== v397 (23/10/2026) -- O TESTE DA UNICA PALAVRA LIDO POR HASH E A PEDRA TOKEN: o registro teste_de_veracidade_fase9_v397 (SPEC: o resultado e os tres recibos por sha256, ao lado do V1; nenhum sigma novo), a pedra Token,\n"
       "# as seis falas do operador de 23/10 e o QUADRO do topo do artigo. Os valores esperados dos checks sao LIDOS dos arquivos pinados na geracao (gerar_candidato_v397.py), nunca digitados; as falas entram EMBUTIDAS por sha256. O gate nao se move. ======================\n")
RUNTIME_SRC = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
_ns_q = {}
exec(compile(RUNTIME_SRC, "<runtime_quadro_v397>", "exec"), _ns_q)     # sintaxe + definicoes sem efeito colateral
assert _ns_q["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44, "a frase do operador do quadro difere da fala (delta_v397)"
RCODE = ("_V397_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V397_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V397_VERACIDADE_SPEC = " + pprint.pformat(spec_verac, width=160, sort_dicts=False)
         + "\n_V397_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n_V397_NOMES_REGISTROS = " + repr(spec_nomes)
         + "\n_V392_FONTES.update(_V397_FONTES)   # v397: o motor de registros (v392) le as fontes e os verbatins das seis versoes\n_V392_VERBATINS2.update(_V397_VERBATINS2)\n\n\n"
         "def _v397_rodar_specs(core_):\n"
         '    """v397 -- roda os registros por spec da v397 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro teste_de_veracidade_fase9_v397 NAO entra aqui: roda no ponto do V1 (main)."""\n'
         "    for spec_ in _V397_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V397_SPECS]\n')
RT = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v397: os registros (o do Teste da Unica Palavra e os por spec), as fontes pinadas e as seis falas do operador\n" + RCODE
ast.parse(RT)
_novo_texto = RUNTIME_SRC + json.dumps(spec_verac, ensure_ascii=False) + json.dumps(specs, ensure_ascii=False)   # as falas do operador (verbatim) nao contem palavra da guarda; a guarda vale para o texto NOVO
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v396 \(22/10/2026\) -- A TESTEMUNHA ESTATICA")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v397", "G_RUNTIME", "bloco v397: o registro teste_de_veracidade_fase9_v397 (spec), as funcoes puras do quadro, as seis falas, registros por spec.")


# ---------------- (6) artigo e md ----------------
def _controles(obj, onde):
    """Guarda de CARACTERE DE CONTROLE (licao da v396: o heredoc do Bash colapsa `\\\\` em `\\` e `\\texttt` virou TAB + `exttt`): nenhuma string de texto novo pode ter caractere de controle alem do fim de linha."""
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo (barra invertida colapsada?)", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


PT0 = open(os.path.join(HERE, "artigo_pt_v397.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v397.pysnip"), encoding="utf-8").read()
# os sha16 das duas falas citadas na leitura ratificada do fator K sao LIDOS dos arquivos (registros_v397: S_VERAC, S_RATK), nunca digitados nos snippets
for _tag, _s16 in (("@@SHA16_VERAC@@", RG.S_VERAC), ("@@SHA16_RATK@@", RG.S_RATK)):
    PT0 = PT0.replace(_tag, _s16); EN0 = EN0.replace(_tag, _s16)
assert "@@" not in PT0 and "@@" not in EN0, "placeholder de sha16 sobrando nos snippets do artigo"
QPT = ('    # v397 (23/10/2026) -- O QUADRO «O Teste da Unica Palavra», logo abaixo do titulo (ordem do operador de 23/10: reportar o 4,44 no inicio do artigo, no readme e tudo mais); numeros LIDOS do registro teste_de_veracidade_fase9_v397. Nada aqui move o gate.\n'
       '    for _l397 in _v397_quadro_tex(core.get("teste_de_veracidade_fase9_v397"), "pt"):\n        s.append(_l397)\n')
QEN = QPT.replace('"pt"', '"en"').replace("QUADRO «O Teste da Unica Palavra», logo abaixo do titulo", "BOX «The Test of the Only Word», right below the title").replace("ordem do operador de 23/10: reportar o 4,44 no inicio do artigo, no readme e tudo mais", "operator's order of 23/10: report the 4.44 at the start of the article, in the readme and everywhere")
for sn in (PT0, EN0, QPT, QEN):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RUNTIME_SRC, "runtime_quadro_v397.py"); _controles([spec_verac, specs, fontes], "specs/fontes")
PT1_FIRST = open(os.path.join(DL.V396, "artigo_pt_v396.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(DL.V396, "artigo_en_v396.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v397, antes da v396.")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v397, antes da v396.")
depois_do_comando("build_pt", ['% core["timestamp"])', r"\vspace{4pt}"], "W06_quadro_PT", "G_ARTIGO", "artigo PT: o QUADRO «O Teste da Unica Palavra» logo abaixo do titulo.", crlf(QPT))
depois_do_comando("build_en", ['% core["timestamp"])', r"\vspace{4pt}"], "W07_quadro_EN", "G_ARTIGO", "artigo EN: o QUADRO «The Test of the Only Word» logo abaixo do titulo.", crlf(QEN))
QMD = ('    for _l397 in _v397_quadro_md(core.get("teste_de_veracidade_fase9_v397")):   # v397 (23/10/2026): o QUADRO do Teste da Unica Palavra no TOPO do .md (ordem do operador: reportar o 4,44 no inicio, no readme e tudo mais); numeros LIDOS do registro\n'
       '        md.append(_l397)\n    md.append("")\n')
ast.parse("def _f(core, md):\n" + QMD)
depois_do_comando("emit_canonical_md", ["> **Versão %s**", "_self_sha16()"], "W08_quadro_MD", "G_ARTIGO", "md canonico: o QUADRO do Teste da Unica Palavra no topo (logo depois do carimbo de versao).", crlf(QMD))
A_M = linha_unica(r'^    md\.append\("> \*\*A testemunha estática \(v396, 22/10/2026\):\*\*')
edit(A_M.end(), A_M.end(), '    md.append("> **O Teste da Única Palavra e a pedra Token (v397, 23/10/2026):** o resultado do teste, aberto uma única vez em 23/10, é lido por sha256 pelo registro `teste_de_veracidade_fase9_v397` (ao lado do V1; nenhum σ novo; o quadro está no topo deste arquivo); '
     + str(N_NOVOS) + ' módulo novo no kernel (`TGLExt/Token`, o nome «token» é do operador; a pedra da testemunha estática fica como registro), com ' + str(len(FL)) + ' bandeira(s) só de declaração nomeada, que cita `psibit_is_the_mode_of_the_reader` (v395) e `the_psion_inhabits_the_static_witness` (v396); as ' + str(len(verb)) + ' falas do operador de 23/10 embutidas por sha256 (`cunhagens_v397`) e a cobertura exata do Audit (`kh_n1_cobertura_v397`). A discriminação a 5σ, o degrau da creditação, não foi alcançada; `NOT_FALSIFIED` nunca é a palavra da creditação; validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF,
     "W09_md", "G_ARTIGO", "md canonico: a linha «O Teste da Unica Palavra e a pedra Token (v397)».")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
T = T0
for a, b, novo, *_ in sorted(EDITS, key=lambda e: -e[0]):
    T = T[:a] + novo + T[b:]
ast.parse(T)
tree = ast.parse(T)
for n in ("_v397_atomos", "_v397_linha_de_maquina", "_v397_quadro_tex", "_v397_quadro_md", "_v397_rodar_specs", "_V397_FONTES", "_V397_VERBATINS2", "_V397_VERACIDADE_SPEC", "_V397_SPECS", "_V397_NOMES_REGISTROS", "_V397_FRASE_444"):
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V396_SPECS", tree).value) == specs396
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT"):
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V397_REGERAR") == "1", "o candidato ja existe e difere: defina V397_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v396_sha16": SHA0, "escada": [E396, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS],
       "kernel": {"modulos_novos": N_NOVOS, "pedra": {"path": DL.STONE_REL, "sha16": sha16(STONE.encode()), "sha256": sha256(STONE.encode())}, "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()),
                  "raiz_v396_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v396_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": [RG.NOME_VERACIDADE] + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "fase9": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in fontes.items() if k_.startswith("f9v2_")},
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E396, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v397.json (pos_build_kernel_v397.py)",
                                 "bandeira_do_teorema": FJX["bandeira_do_teorema"], "bandeiras_do_suporte": FLAGS_SUP},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v396_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v396_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_do_teorema_da_pedra": N_AX_UNC,
       "ponto_de_chamada": {"teste_de_veracidade_fase9_v397": "main: logo depois do bloco hubble_ratio_opening_v388 (a Fase 9 do V1, lida por hash), ao lado dele", "specs": "main: depois do bloco [v396]", "quadro": "artigo PT/EN: logo abaixo do titulo; .md: logo depois do carimbo de versao"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v397.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v397.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v397.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v397_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v396_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v396:", PFORMAT_IDEMPOTENTE)
