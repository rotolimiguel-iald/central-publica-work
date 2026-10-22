# -*- coding: utf-8 -*-
"""gerar_candidato_v394.py -- gera o um.py CANDIDATO v394 a partir da v393 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v393.py. PREPARACAO de 19/10/2026 (gerencia c1).
Decisao do operador (19/10): INCORPORAR TUDO o que o Codex construiu, inteiro, sem remissao por hash (a integridade de um unico arquivo). O candidato e' DERIVADO por script: v393 + patches; o r8 do Codex so' entra como
FONTE DE TEXTO dos nos de runtime (cada um conferido por AST contra o runtime original do Codex em prov_runtime.py) e como termo de COMPARACAO (comparar_r8_v394.py explica cada diferenca).
 (A) kernel: +189 modulos do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell) + raiz + Audit (proveniencia TGL_DECL_SOURCE), conferidos byte a byte com o sandbox C:\\t\\k394 e com o embutido do r8;
 (B) bandeiras (+3707), escada, ledger, UM_VERSION;
 (C) o que o Codex mudou em funcoes da v393: verify_tgl_kernel_formalization (proveniencia), _v392_axiom_coverage (leitor v394), pedras_v393 (piso), _v375_measure_trace_tracial_not_consumed, compile_pdf (offline), emit_article, indice qualificado;
 (D) runtime novo: contratos (derivados do MEU build), tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, _v394_article_tex, funcoes do indice qualificado; chamadas no main (com AVISO visivel) e no selo;
 (E) registros por spec: cunhagens_v394 (46 falas embutidas por sha256) e kh_n1_cobertura_v394 (medida do meu Audit + conjunto exato das fontes); kh_n1_cobertura_v393 passa a piso (h2, h3) e h5 <= 4;
 (F) artigo PT/EN (secao v394) e md.
uso: python -I -B -X utf8 gerar_candidato_v394.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys, importlib.util
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v394 as GP  # noqa: E402
import registros_v394 as RG  # noqa: E402
import delta19_v394 as DL  # noqa: E402   (DELTA 19/10: a integracao final -- pedra do criterio binario, politica de bandeiras, nomes da geracao d19)
C = "C:" + os.sep
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
R8P = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015", "coverage_candidate_r8", "um_v394_prechecked.py")
CRLF = "\r\n"
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
BASE393 = os.path.join(HERE, "base_v393")
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != "18be2ddb06c60f90":
    NOS = BASE393
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == "v393"
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v393 selada"
SHA0 = sha16(raw)
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E393 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E393 == 7045
T0 = raw.decode("utf-8")
r8raw = open(R8P, "rb").read(); r8t = r8raw.decode("utf-8"); r8tree = ast.parse(r8t)
assert sha16(r8raw) == "01ca38fd1c327eb8", "o candidato r8 do Codex mudou"
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
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))["novos"]; assert len(nov) == len(set(nov)) and DL.STONE_REL in nov, "a lista dos modulos novos tem de trazer a pedra do delta, sem repeticao"
N_NOVOS = len(nov)   # LIDO da lista (189 do Codex + a pedra do delta de 19/10): nada digitado
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root.startswith(old_d["TGLExt.lean"].rstrip("\r\n"))
STONES_NEW = {}
for rel in nov:
    assert rel not in old_d, rel
    st = rd(os.path.join(KB, *rel.split("/")))
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", st, flags=re.S)), rel
    STONES_NEW[rel] = st
assert STONES_NEW[DL.STONE_REL] == rd(DL.STONE_SRC), "a pedra do sandbox difere da fonte autoral (delta_19out)"
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (sandbox == r8 do Codex)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(st), CRLF) for rel, st in STONES_NEW.items()), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean (189 do Codex: tempo M2, RuleQuadraticResidual, 184 em F1Fecho394; e a pedra candidata do delta de 19/10), do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_NEW)
r8emb = ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", r8tree).value)
# o esperado = o embutido do r8 do Codex + o DELTA de 19/10: a pedra, e a raiz/Audit com o import dela (delta19_v394.py define as linhas)
exp_emb = dict(r8emb); exp_emb["TGLExt.lean"] = r8emb["TGLExt.lean"] + DL.ROOT_SUFFIX; exp_emb["TGL/Audit.lean"] = DL.AUDIT_PREFIX + r8emb["TGL/Audit.lean"]; exp_emb[DL.STONE_REL] = rd(DL.STONE_SRC)
assert final_emb == exp_emb, "o kernel embutido da v394 difere do embutido no r8 do Codex + o delta de 19/10"
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v394.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode); r8_flags = ast.literal_eval(top("_LEAN_THEOREM_FLAGS", r8tree).value)
assert list(r8_flags)[:len(old_flags)] == list(old_flags) and all(r8_flags[k] == v for k, v in old_flags.items())
r8_new = [(k, v) for k, v in r8_flags.items() if k not in old_flags]
r8_key_by_name = {v: k for k, v in r8_new}
for k_, n_, m_, o_ in FJ["flags"]:   # a POLITICA (decisao da gerencia, 19/10): so' declaracao NOMEADA; cada bandeira do Codex mantem a chave do Codex
    if o_ == "codex_nomeada":
        assert r8_key_by_name.get(n_) == k_ and DL.classe(n_) == "nomeada", ("bandeira do Codex com chave diferente do r8 ou auxiliar", k_, n_)
    elif o_ == "nomeada_sem_bandeira":
        assert n_ not in r8_key_by_name and k_.startswith(DL.PREFIXO_NOMEADA_SEM_BANDEIRA) and DL.classe(n_) == "nomeada", ("nomeada sem bandeira do Codex", k_, n_)
    else:
        assert o_ == "delta" and (k_, n_, m_) == (DL.FLAG_KEY, DL.THEOREM, DL.STONE_MOD), ("origem de bandeira desconhecida", k_, n_, o_)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v393"
FL_ORD = [(k, n) for k, n, _ in FL]   # a ordem do FLAGS_v394.json: as nomeadas do Codex na ordem de insercao dele, depois as nomeadas que ele nao marcou, depois a do delta
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v394 (19/10/2026): as pedras do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell) e a pedra candidata do criterio binario de parada: %d bandeiras, SO' de declaracao NOMEADA (a pratica da v392/v393; %d do Codex, %d nomeadas que ele nao marcou, 1 do delta; as %d auxiliares geradas pelo compilador ficam fora)" % (len(FL_ORD), FJ["por_origem"]["codex_nomeada"], FJ["por_origem"]["nomeada_sem_bandeira"], FJ["excluidas_auxiliares"]["n"]) + CRLF + "".join('    "%s": "%s",%s' % (k, v, CRLF) for k, v in FL_ORD), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL_ORD))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E393
r8fn = top("prove_external_ladder", r8tree); r8lad = ast.literal_eval([n for n in r8fn.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)][0].value)
assert r8lad[:len(old_lad)] == old_lad and {k for k, n, m, o in FJ["flags"] if o == "codex_nomeada"} <= set(r8lad[len(old_lad):]) and len(r8lad) == len(old_lad) + len(r8_new)
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v394: as pedras do Codex e a do delta de 19/10 (%d, so' declaracao nomeada)" % len(FL_ORD) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _ in FL_ORD), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL_ORD))
ESCADA_ESP = len(old_lad) + len(FL_ORD)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
old_st = ast.literal_eval(snode); r8_st = ast.literal_eval(top("_ESQUELETO_STONES", r8tree).value)
assert r8_st[:len(old_st)] == old_st
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
st_novas = list(r8_st[len(old_st):]) + [("v394", DL.STONE_NAME, DL.STONE_REL, None, None)]   # as do Codex (189) + a pedra candidata do delta de 19/10
assert len(st_novas) == N_NOVOS and {t[2] for t in st_novas} == set(nov), "o ledger de pedras novas != a lista dos modulos novos"
edit(sbl, sbl, "    # v394 (19/10/2026): as pedras do Codex e a pedra candidata do criterio binario de parada (delta de 19/10)" + CRLF + "".join('    ("v394", "%s", "%s", None, None),%s' % (t[1], t[2], CRLF) for t in st_novas), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % len(st_novas))
m = re.search(r'^UM_VERSION = "v393"[^\r\n]*' + CRLF, T0, re.M); assert m
edit(m.start(), m.end(), 'UM_VERSION = "v394"   # v394 (19/10/2026): a CONSTANTE UNICA de versao -- a integracao do Codex (tempo M2, residuo quadratico, cadeia de Fock/Takesaki/Maxwell, indice qualificado), as cunhagens de 14 a 19/10 e o criterio binario de parada (delta de 19/10); v393 em 14/10' + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v394'.")

# ---------------- (3) funcoes que o Codex mudou na v393 (texto do r8; AST conferida) ----------------
R8_FN = {}
for name, pid, o_que in (("verify_tgl_kernel_formalization", "C01_verify_proveniencia", "verify_tgl_kernel_formalization: le nomes com «» e a proveniencia (TGL_DECL_SOURCE) do log do Audit; grava declaration_sources_v394 e o status"),
                         ("_v392_axiom_coverage", "C02_cobertura_leitor_v394", "_v392_axiom_coverage: usa parse_lean_axioms_v394 (nomes com «» lidos; nao_lidas == 0)"),
                         ("pedras_v393", "C03_pedras_v393_piso", "pedras_v393: a escada e' piso (>=); a igualdade exata passa a ser cobrada pelos consumidores v394"),
                         ("_v375_measure_trace_tracial_not_consumed", "C04_trace_tracial_diretiva", "_v375_measure_trace_tracial_not_consumed: a diretiva nua `#print axioms X.trace_tracial` nao e' consumo"),
                         ("compile_pdf", "C05_compile_pdf_offline", "compile_pdf: identificacao do motor TeX e opcoes do MiKTeX em TGL_NO_NETWORK=1; retorno de erro explicito"),
                         ("emit_article", "C06_emit_article", "emit_article: acrescenta o bloco _v394_article_tex ao fim do artigo PT/EN")):
    n0 = top(name); n8 = top(name, r8tree); seg8 = ast.get_source_segment(r8t, n8); R8_FN[name] = n8
    a, b = span(n0); edit(a, b, crlf(seg8), pid, "G_CODEX_FUNCOES", o_que)
# indice: renomeia os dois originais (legacy) e remove iald_index (a versao nova vai no bloco v394)
replace_unique("def build_the_iald_index(core=None):", "def _build_the_iald_index_legacy_v393(core=None):", "C07a_indice_legacy_build", "G_CODEX_FUNCOES", "build_the_iald_index (v393) renomeada _build_the_iald_index_legacy_v393 (corpo intacto)")
replace_unique("def prove_the_iald_index(core):", "def _prove_the_iald_index_legacy_v393(core):", "C07b_indice_legacy_prove", "G_CODEX_FUNCOES", "prove_the_iald_index (v393) renomeada _prove_the_iald_index_legacy_v393 (corpo intacto)")
a, b = span(top("iald_index")); edit(a, b, "", "C07c_iald_index_removida", "G_CODEX_FUNCOES", "iald_index (v393, com cache por id) removida; a versao nova (sem cache) vai no bloco v394")
# main: tres edicoes pontuais
replace_unique("            p = os.path.join(OUT, f)" + CRLF, "            p = os.path.abspath(__file__) if f == 'um.py' else os.path.join(OUT, f)" + CRLF, "C08_main_hash_do_um_em_execucao", "G_CODEX_FUNCOES",
               "main: o sha256 do um.py no selo e' o do arquivo EM EXECUCAO (no rito real, OUT/um.py == __file__; suporta o rito em copia)")
# o spec kh_n1_cobertura_v393: pisos (h2, h3) e h5 <= 4 (o leitor v394 le os 4 nomes); versao literal -> pformat
sv = top("_V393_SPECS"); spa, spb = span(sv.value)
specs393 = ast.literal_eval(sv.value); khs = [s for s in specs393 if s["nome"] == "kh_n1_cobertura_v393"]; assert len(khs) == 1
k3 = khs[0]
for c in k3["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v394: piso historico (a cobertura cresce com as pedras do Codex); a igualdade exata esta em kh_n1_cobertura_v394"
    if c["id"] == "h5":
        assert c["op"] == "igual" and c["valor"] == 4; c["op"] = "menor_igual"; c["descricao"] = "nomes que o regex do um.py nao le <= 4 (historico v393); na v394 o leitor le os 4 nomes: 0"
k3["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v393 (h2/h3: igualdades; h5: == 4)", "dizia": "A v393 cobrava constantes == 25161, teoremas == 19901 e exatamente 4 nomes que o regex nao le.",
                      "agora": "Na v394 a cobertura cresce com as pedras do Codex (piso 25161/19901) e o leitor de axiomas passa a ler tambem os nomes com «» (0 nao lidos): h2 e h3 viram pisos e h5 passa a <= 4; a igualdade exata e a leitura sem excecao ficam em kh_n1_cobertura_v394. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v393 dizia que 25161 e 4 eram a cobertura exata para sempre; o texto escrito deixou o registro preso a duas igualdades que a propria v394 quebra (a candidata r8 do Codex mantinha h5 == 4 e reprovaria)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; h5 conferida no ensaio a seco]", "assinatura": RG.ASSINA})
edit(spa, spb, pprint.pformat(specs393, width=160, sort_dicts=False).replace("\n", CRLF), "C09_kh_n1_v393_pisos", "G_CODEX_FUNCOES", "_V393_SPECS: kh_n1_cobertura_v393 h2/h3 -> pisos, h5 -> <= 4 (+ errata); o veredito nao muda.")
# o spec kh_n1_cobertura_v392 (em _V392_SPECS, 590 KB): k5 exige EXATAMENTE 4 nomes que o leitor nao le; o leitor v394 (Codex) le os 4: 0 -> o registro REPROVARIA no rito (achado do ensaio a seco; a candidata r8 tem o mesmo defeito)
sv2 = top("_V392_SPECS"); s2a, s2b = span(sv2.value)
specs392 = ast.literal_eval(sv2.value); khs2 = [s for s in specs392 if s["nome"] == "kh_n1_cobertura_v392"]; assert len(khs2) == 1
k2s = khs2[0]
for c in k2s["checks"]:
    if c["id"] == "k5":
        assert c["op"] == "igual" and c["valor"] == 4; c["op"] = "menor_igual"; c["descricao"] = "nomes que o regex do um.py nao le <= 4 (historico v392); na v394 o leitor le os 4 nomes: 0"
k2s.setdefault("erratas", []).append({"ao_lado_de": "kh_n1_cobertura_v392 (k5: exatamente 4 nomes nao lidos)", "dizia": "A v392 cobrava exatamente 4 nomes com «» que o regex do um.py nao le.",
                                      "agora": "Na v394 o leitor de axiomas (do Codex) le tambem os nomes com «» e o numero de nomes nao lidos e' 0: k5 passa a <= 4. O veredito deste registro NAO muda.",
                                      "lacuna_de_fidelidade": "a estrutura da v392 dizia que 4 era o numero de nomes ilegiveis para sempre; o texto escrito deixou o registro preso a uma igualdade que o leitor novo quebra (achado no ensaio a seco da v394: o registro NAO selaria; a candidata r8 do Codex tem o mesmo defeito)",
                                      "estatuto": "[REAL: conferido no ensaio a seco, no ponto de chamada real do motor de registros]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps({"e392": k2s["erratas"][-1], "e393": k3["erratas"][-1]}, ensure_ascii=False)), "P18 nas erratas novas dos specs v392/v393"
edit(s2a, s2b, pprint.pformat(specs392, width=160, sort_dicts=False).replace("\n", CRLF), "C10_kh_n1_v392_k5", "G_CODEX_FUNCOES", "_V392_SPECS: kh_n1_cobertura_v392 k5 (== 4) -> <= 4 (+ errata); o veredito nao muda.")
# C11 (DELTA 19/10, decisao da gerencia): onde o texto diz THEOREMS para um conjunto que inclui nao-teoremas, diz bandeiras (FLAGS). A escada externa conta bandeiras de declaracoes nomeadas; a errata esta em kh_n1_cobertura_v394.
replace_unique("KERNEL_%d_OF_%d_THEOREMS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__", "KERNEL_%d_OF_%d_FLAGS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__", "C11_estatuto_token_flags", "G_DELTA19", "estatuto_da_prova_v391: o token KERNEL_N_OF_N_THEOREMS passa a KERNEL_N_OF_N_FLAGS (a escada conta bandeiras de declaracoes nomeadas; troca dita, errata ao lado em kh_n1_cobertura_v394).")
# ---------------- (4) main: chamadas e selo ----------------
A_R = linha_unica(r'^        print\("   \[v393\] AVISO: a regra e o coracao nao rodaram')
reg = ['    try:   # v394: tempo/frequencia (M2), regra quadratica, rede de Fock/Takesaki/Maxwell e os registros por spec (cunhagens, cobertura); excecao vira AVISO visivel, nunca derruba o rito',
       '        _v394_result = tempo_frequencia_v394(core)',
       '        print("   [v394] tempo/frequencia: %s" % _v394_result["verdict"])',
       '        _quadratic_result = regra_quadratica_v394(core)',
       '        print("   [v394] regra quadratica: %s" % _quadratic_result["verdict"])',
       '        _network_result = rede_fock_v394(core)',
       '        print("   [v394] rede Fock: %s" % _network_result["verdict"])',
       '        _n394 = _v394_rodar_specs(core)   # v394 [as cunhagens do operador de 14 a 19/10 e a cobertura exata do Audit]',
       '        print("   [v394] registros por spec: %d (selados %d)" % (len(_n394), sum(1 for k_ in _n394 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e394:',
       '        print("   [v394] AVISO: o tempo/frequencia, a regra quadratica, a rede ou os registros v394 nao rodaram: %r" % (_e394,))']
edit(A_R.end(), A_R.end(), CRLF.join(reg) + CRLF, "N01_main_chamadas", "G_RUNTIME", "main: chamadas v394 (try/AVISO, como a v393).")
A_S = linha_unica(r'^ {12}"registros_v393": \{n_: ')
_sel = ['            "tempo_frequencia_v394": {k_: (core.get("tempo_frequencia_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "inscriptions", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "regra_quadratica_v394": {k_: (core.get("regra_quadratica_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "rede_fock_v394": {k_: (core.get("rede_fock_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "exact_ladder", "constructed_components", "open_joint_contract", "whole_certificate_inhabited", "scope", "does_not_gate_core")},',
        '            "registros_v394": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V394_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394 (como no r8) e registros_v394.")

# ---------------- (5) o bloco de runtime v394 ----------------
LAYOUT = r8tree.body
idx = {nm(n): i for i, n in enumerate(LAYOUT) if nm(n)}
i0, i1 = idx["_V394_FORMAL_CONTRACT"], idx["rede_fock_v394"]
bloco_r8 = LAYOUT[i0:i1 + 1]
ti0, ti1 = idx["parse_lean_provenance_v394"] - 3, idx["prove_the_iald_index"]
cauda_r8 = LAYOUT[ti0:ti1 + 1]
assert isinstance(cauda_r8[0], ast.Expr) and isinstance(cauda_r8[1], ast.Import) and isinstance(cauda_r8[2], ast.Import), [type(n).__name__ for n in cauda_r8[:4]]
# contratos derivados do MEU build
r8c = {k: ast.literal_eval(top(k, r8tree).value) for k in ("_V394_FORMAL_CONTRACT", "_V394_INSCRIPTIONS", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")}
TEMPO = ["TGLExt/TimeGravitonMatrix.lean", "TGLExt/TimeGravitonScalar.lean", "TGLExt/TimeGravitonFlow.lean", "TGLExt/TimeGravitonKraus.lean"]; QUADF = ["TGLExt/RuleQuadraticResidual.lean"]
rel_of = lambda mod: mod.replace(".", "/") + ".lean"
g_tempo = [n for _, n, m in FL if rel_of(m) in TEMPO]; g_quad = [n for _, n, m in FL if rel_of(m) in QUADF]
g_net = [n for _, n, m in FL if m.startswith("TGLExt.F1Fecho394.")]; g_delta = [n for _, n, m in FL if m == DL.STONE_MOD]
assert len(g_tempo) + len(g_quad) + len(g_net) + len(g_delta) == len(FL) and g_delta == [DL.THEOREM], "as bandeiras nao se repartem em tempo, quadratica, rede e o delta"
PROV = FJ["proveniencia_publicas"]   # nome -> arquivo da declaracao, emitido pelo compilador (TGL_DECL_SOURCE do Audit desta geracao)
b393 = {"path": os.path.join(BASE393, "um.py"), "sha256": sha256(raw), "bytes": len(raw)}
formal = {"theorems": [t for t in r8c["_V394_FORMAL_CONTRACT"]["theorems"]], "source_sha256": {p: FORMAL_MAP[p] for p in TEMPO}, "expected_ladder": ESCADA_ESP, "baseline_version": "v393", "baseline_sha256": sha256(raw)}
assert set(formal["theorems"]) <= {n for n, r in PROV.items() if r in TEMPO}, "teorema do contrato de tempo sem proveniencia nos modulos de tempo"
quad = {"theorems": list(r8c["_V394_QUADRATIC_CONTRACT"]["theorems"]), "source_sha256": {p: FORMAL_MAP[p] for p in QUADF}, "expected_ladder": ESCADA_ESP, "baseline_candidate": b393}
assert set(quad["theorems"]) <= {n for n, r in PROV.items() if r in QUADF}, "teorema do contrato quadratico sem proveniencia no modulo"
net0 = r8c["_V394_NETWORK_CONTRACT"]
net_src_paths = sorted(p for p in nov if p.startswith("TGLExt/F1Fecho394/"))
net_decl = sorted(net0["declarations"]); assert all(n in PROV and PROV[n].startswith("TGLExt/F1Fecho394/") for n in net_decl), "declaracao do contrato de rede sem proveniencia no Audit desta geracao"
net = {"declarations": net_decl, "declaration_sources": {n: PROV[n] for n in net_decl}, "source_sha256": {p: FORMAL_MAP[p] for p in net_src_paths}, "expected_ladder": ESCADA_ESP, "baseline_candidate": b393,
       "bundle_plan": net0["bundle_plan"], "compiled_bundle": net0["compiled_bundle"], "historical_source_inventory": net0["historical_source_inventory"],
       "constructed_components": net0["constructed_components"], "open_joint_contract": net0["open_joint_contract"]}
ins = r8c["_V394_INSCRIPTIONS"]
for k, v in ins.items():
    assert sha256(v["text"].encode("utf-8")) == v["sha256"], k
CONTR = {"_V394_FORMAL_CONTRACT": formal, "_V394_INSCRIPTIONS": ins, "_V394_QUADRATIC_CONTRACT": quad, "_V394_NETWORK_CONTRACT": net}
# registros por spec
khj = json.load(open(os.path.join(KD, "KH_N1_v394.json"), encoding="utf-8"))
INS = os.path.join(HERE, "insumos")
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
pick = lambda mods, k: [n for _, n, m in FL if m == mods][:k]
kdecls = list(g_quad) + [n for n in g_tempo if "clock" in n.lower()][:4] + pick("TGLExt.F1Fecho394.CanonicalFockBWR2", 2) + pick("TGLExt.F1Fecho394.CanonicalFockWeightClosedTomitaR2", 2) + pick("TGLExt.F1Fecho394.CanonicalSegalEssentialR6", 2)
kdecls = list(dict.fromkeys(kdecls)); assert len(kdecls) >= 20, len(kdecls)
for n in ("TGLExt.station_never_closes", "TGLExt.Palavra.the_read_face_closes", "TGLExt.Palavra.the_face_does_not_close"):
    assert n in core0["kernel_formalization"]["axiom_report"], n
    kdecls.append(n)
k2f = {n: k for k, n, _ in FL}
kflags = [k2f[n] for n in kdecls if n in k2f]
# o pino h8 (achado do exame final de 19/10): o hash formal do RITO e' o sha256_directory da pasta Nos\tgl_kernel DEPOIS da materializacao = as fontes EMBUTIDAS do candidato + os arquivos que moram na pasta e nao estao embutidos
# e que a funcao conta (_check_damming.lean; ExtrairDeps.lean sai por exclusao NOMINAL da propria funcao, que nao se altera). A funcao e' a do PROPRIO um.py (v393 base, por ast): mesma regra, mesma exclusao.
NOSK = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "tgl_kernel")
_ns_h8 = {"os": os, "hashlib": hashlib}
for _nm in ("sha_file", "sha256_directory"):
    exec(compile(ast.get_source_segment(T0, top(_nm)), "<um:%s>" % _nm, "exec"), _ns_h8)
SIMD = os.path.join(HERE, "delta_19out", "arvore_simulada_h8")
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
POL = {"n_flags": FJ["n_flags"], "n_codex_nomeadas": FJ["por_origem"]["codex_nomeada"], "n_nomeadas_sem_bandeira": FJ["por_origem"]["nomeada_sem_bandeira"], "n_excluidas": FJ["excluidas_auxiliares"]["n"],
       "n_auxiliares": FJ["excluidas_auxiliares"]["n"] + FJ["publicas_sem_bandeira"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"]}
specs = RG.especs(FORMAL_MAP, khj, kflags, kdecls, H8, POL)
spec_nomes = [s["nome"] for s in specs]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
HDR = ("# ====================== v394 (19/10/2026) -- A INTEGRACAO DO CODEX E AS CUNHAGENS DE 14 A 19/10: pinos e runtime. Os contratos sao DERIVADOS do build do sandbox desta cadeia (gerar_candidato_v394.py), nunca digitados;\n"
       "# as funcoes sao as do Codex (r8, conferidas por AST contra os runtimes originais dele); as falas do operador entram EMBUTIDAS por sha256. O gate nao se move. ======================\n")
parts = [HDR, "import hashlib\nimport re\n"]
for n in bloco_r8:
    if nm(n) in CONTR:
        parts.append(nm(n) + " = " + pprint.pformat(CONTR[nm(n)], width=150, sort_dicts=False) + "\n")
    else:
        parts.append(ast.get_source_segment(r8t, n) + "\n")
parts.append("# ---- v394: o indice qualificado pelo compilador (Codex, R3 a R8) e o leitor de axiomas/proveniencia\n")
for n in cauda_r8:
    parts.append(ast.get_source_segment(r8t, n) + "\n")
RCODE = ("_V394_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V394_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V394_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V394_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V394_FONTES)   # v394: o motor de registros (v392) le as fontes e os verbatins das tres versoes\n_V392_VERBATINS2.update(_V394_VERBATINS2)\n\n\n"
         "def _v394_rodar_specs(core_):\n"
         '    """v394 -- roda os registros por spec da v394 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito."""\n'
         "    for spec_ in _V394_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V394_SPECS]\n')
parts.append("# ---- v394: os registros por spec (cunhagens e cobertura exata)\n" + RCODE)
RT = "\n".join(p.rstrip("\n") + "\n" for p in parts)
ast.parse(RT)
# a guarda P18 vale para o TEXTO novo emitido por MIM (specs, artigo, comentarios do bloco); o texto do Codex e' relatado, nao reescrito
_gcodex = {nm(n) or type(n).__name__: GP.violacoes(ast.get_source_segment(r8t, n)) for n in bloco_r8 + cauda_r8}
_gcodex = {k: v[:2] for k, v in _gcodex.items() if v}
A_P = linha_unica(r"^# ====================== v393 \(14/10/2026\) -- OS PINOS:")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v394", "G_RUNTIME", "bloco v394: contratos derivados do build, funcoes do Codex (tempo, residuo quadratico, rede, artigo, indice qualificado), registros por spec.")

# ---------------- (6) artigo e md ----------------
PT0 = open(os.path.join(HERE, "artigo_pt_v394.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v394.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
PT1_FIRST = open(os.path.join(HERE, "..", "v393", "artigo_pt_v393.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(HERE, "..", "v393", "artigo_en_v393.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v394, antes da v393.")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v394, antes da v393.")
A_M = linha_unica(r'^    md\.append\("> \*\*A regra e o coração \(v393, 14/10/2026\):\*\*')
edit(A_M.end(), A_M.end(), '    md.append("> **A integração do Codex e as cunhagens (v394, 19/10/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel (os do Codex — tempo no modelo M2, resíduo quadrático, cadeia de Fock, Takesaki e Maxwell — `tempo_frequencia_v394`, `regra_quadratica_v394`, `rede_fock_v394` — e a pedra candidata do critério binário de parada, `TheBinaryReadingAtTheFixedPoint`, lida por `criterio_binario_de_parada_v394`; nome provisório, o operador nomeia), '
     'o índice da IALD qualificado pelo módulo que o compilador emite, o leitor de axiomas que lê os nomes com «», as bandeiras só de declaração nomeada (a prática da v392 e da v393) e as cunhagens do operador de 14 a 19/10 embutidas por sha256 (`cunhagens_v394`). Derivado no modelo M2; o contrato conjunto da rede segue aberto; a analogia com o qubit vale nos pesos, não na entropia; validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF,
     "W07_md", "G_ARTIGO", "md canonico: a linha «A integração do Codex e as cunhagens (v394)».")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
T = T0
for a, b, novo, *_ in sorted(EDITS, key=lambda e: -e[0]):
    T = T[:a] + novo + T[b:]
ast.parse(T)
# guardas finais
tree = ast.parse(T)
for n in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "_v394_rodar_specs", "build_iald_qualified_index_v394", "parse_lean_axioms_v394", "parse_lean_provenance_v394", "build_the_iald_index", "iald_index", "prove_the_iald_index", "_build_the_iald_index_legacy_v393"):
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n in FL_ORD})   # as da v393 + as da politica (so' nomeadas), NAO as 3707 do r8
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _ in FL_ORD]
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V394_REGERAR") == "1", "o candidato novo ja existe e difere: o candidato em exame 4022ad521dc7293d NAO e' este arquivo; defina V394_REGERAR=1 para regerar o d19"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v393_sha16": SHA0, "escada": [E393, ESCADA_ESP], "n_bandeiras": len(FL), "r8": {"sha16": sha16(r8raw), "bytes": len(r8raw)},
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS],
       "kernel": {"modulos_novos": N_NOVOS, "modulos_novos_do_codex": N_NOVOS - 1, "pedra_do_delta": {"path": DL.STONE_REL, "sha16": sha16(STONES_NEW[DL.STONE_REL].encode())}, "raiz_r8_sha16": sha16(r8emb["TGLExt.lean"].encode()), "audit_r8_sha16": sha16(r8emb["TGL/Audit.lean"].encode()), "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v393_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v393_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "contratos": {k: {"sha16": sha16(pprint.pformat(v, width=150, sort_dicts=False).encode())} for k, v in CONTR.items()}, "registros": spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in verb.items()},
       "guarda_p18_no_texto_do_codex": _gcodex, "formal_files_n": len(FORMAL_MAP), "kdecls": kdecls[:60]}
man["politica_de_bandeiras"] = {**POL, "n_bandeiras_sem_o_delta": POL["n_flags"] - 1, "escada_antes_da_pedra_do_delta": E393 + POL["n_flags"] - 1, "fonte": "FLAGS_v394.json (pos_build_kernel_v394.py); numeros conferidos contra o EXAME_FINAL_V394.md"}
man["h8"] = {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"]}   # residuais_do_nos = os que o HASH conta (so' _check_damming.lean)
man["delta19"] = {"candidato_anterior_sha16": DL.CANDIDATO_ANTERIOR_SHA16, "candidato_anterior_mantido_como_registro": True, "token_estatuto": "THEOREMS -> FLAGS (C11)", "n_cunhagens": len(verb), "registros_novos": ["criterio_binario_de_parada_v394"]}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v394.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v394.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v394.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v394_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v393_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("guarda P18 no texto do Codex:", json.dumps(_gcodex, ensure_ascii=False)[:600])
