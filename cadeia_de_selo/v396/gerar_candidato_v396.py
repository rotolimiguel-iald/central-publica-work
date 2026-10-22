# -*- coding: utf-8 -*-
"""gerar_candidato_v396.py -- gera o um.py CANDIDATO v396 a partir da v395 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v395.py. PREPARACAO de 22/10/2026 (gerencia c1).
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +1 modulo (TGLExt/TestemunhaEstatica.lean, nome PROVISORIO; PEDRA_APROVADA no exame independente) + raiz + Audit (o import), conferidos byte a byte com o sandbox C:\\t\\k396c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394 e o do psibit da v395) sobem para a escada da v396 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v395 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo: testemunha_estatica_v396 (o psion habita a testemunha estatica: contrato derivado do MEU build, mecanica calculada com beta = alfa CODATA 2018 x sqrt(e) em runtime), as tres falas do operador de 22/10
     embutidas por sha256, os registros por spec cunhagens_v396 e kh_n1_cobertura_v396; chamadas no main (a de testemunha_estatica_v396 no PONTO DE CHAMADA REAL, junto do psibit_v395) e no selo;
 (E) artigo PT/EN (secao v396) e md.
uso: python -I -B -X utf8 gerar_candidato_v396.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v396 as GP  # noqa: E402
import registros_v396 as RG  # noqa: E402
import delta_v396 as DL  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP395 = json.load(open(os.path.join(DL.V395, "ESPERADOS_v395.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP395["candidato_sha16"]:   # o Nos ja nao e' a v395 (rito v396 em curso): a v395 SELADA vem da copia base_v395
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v395 selada"
SHA0 = sha16(raw); assert SHA0 == ESP395["candidato_sha16"]
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E395 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E395 == ESP395["escada"][1], (E395, ESP395["escada"])
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
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v396.json"), encoding="utf-8"))["novos"]; assert nov == [DL.STONE_REL], "a lista dos modulos novos tem de ser so' a pedra TestemunhaEstatica"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v395 + o import da pedra"
STONE = rd(os.path.join(KB, *DL.STONE_REL.split("/")))
assert STONE == rd(DL.STONE_SRC), "a pedra do sandbox difere da fonte autoral (work\\testemunha_estatica_v396\\TestemunhaEstatica.lean): rode refazer_sandbox_v396.sh"
assert DL.STONE_REL not in old_d
assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONE, flags=re.S)), "sorry no codigo da pedra"
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (+ o import da pedra TestemunhaEstatica; sandbox == embutido)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "    %r: %s,%s" % (DL.STONE_REL, repr(STONE), CRLF), "K01_modulo_novo", "G_KERNEL", "kernel embutido: +1 modulo Lean (TGLExt/TestemunhaEstatica.lean, a pedra da testemunha estatica), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb[DL.STONE_REL] = STONE
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v396.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v395"
assert all(DL.classe(n) == "nomeada" and m == DL.STONE_MOD for _, n, m in FL) and FJ["n_flags"] == len(FL)
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v396 (22/10/2026): a pedra TestemunhaEstatica (o psion habita a testemunha estatica; nome PROVISORIO): %d bandeiras, SO' de declaracao NOMEADA (a pratica da v392 a v395; as %d auxiliares geradas pelo compilador ficam fora)" % (len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E395 and len(set(old_lad)) == E395
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v396: a pedra TestemunhaEstatica (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v396 (22/10/2026): a pedra TestemunhaEstatica (o psion habita a testemunha estatica: o par ecoa, o individuo nao ecoa, o canto habita um fluxo construido; nome PROVISORIO, quem nomeia e' o operador)" + CRLF + '    ("v396", "%s", "%s", None, None),%s' % (DL.STONE_NAME, DL.STONE_REL, CRLF), "V03_ledger", "G_KERNEL", "ledger de pedras: +1.")
m = re.search(r'^UM_VERSION = "v395"[^\r\n]*' + CRLF, T0, re.M); assert m
edit(m.start(), m.end(), 'UM_VERSION = "v396"   # v396 (22/10/2026): a CONSTANTE UNICA de versao -- a testemunha estatica (a pedra TestemunhaEstatica, o registro testemunha_estatica_v396 e as tres falas do operador de 22/10); v395 em 21/10' + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v396'.")

# ---------------- (3) o que a v396 muda nos registros das versoes anteriores (so' dados) ----------------
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT"):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E395
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V395_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E395, ESCADA_ESP))
sv = top("_V395_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs395 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs395, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
khs = [s for s in specs395 if s["nome"] == "kh_n1_cobertura_v395"]; assert len(khs) == 1
k5 = khs[0]
H8_ANTIGO_N = None
for c in k5["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v396: piso historico (a cobertura cresce com o modulo TestemunhaEstatica); a igualdade exata esta em kh_n1_cobertura_v396"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v396: piso historico; a igualdade exata esta em kh_n1_cobertura_v396"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v396: a arvore ganha o arquivo da pedra, entao o registro da v395 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v396" % H8_ANTIGO_N
k5["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v395 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v395 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v395 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v396 a cobertura cresce com o modulo TestemunhaEstatica e a arvore ganha o arquivo da pedra: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v396. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v395 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v396 quebra (a mesma lacuna que a v395 achou no registro da v394)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; conferidas no ensaio a seco]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k5["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v395"
edit(spa, spb, pprint.pformat(specs395, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v395_pisos", "G_V395_PISOS", "_V395_SPECS: kh_n1_cobertura_v395 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (4) main: chamadas e selo ----------------
A_TES = re.escape('        print("   [v395] AVISO: o modo psionico (psibit) nao rodou: %r" % (_e395,))')
m_tes = re.search("^" + A_TES + r"\r\n", T0, re.M); assert m_tes and T0.count(m_tes.group(0)) == 1, "ancora do bloco psibit_v395 (no ponto da fractalizacao do Um) nao achada ou nao unica"
tes = ['    try:   # v396: a TESTEMUNHA ESTATICA (o psion habita a fronteira), no mesmo ponto de chamada do psibit: a mecanica do canto do psion, da reducao a um sitio, do fluxo construido e do colapso, calculada agora e lida contra os termos do kernel do proprio rito; excecao vira AVISO visivel, nunca derruba o rito',
       '        _tes396 = testemunha_estatica_v396(core)',
       '        _tev396 = _tes396.get("values") or {}',
       '        _nan396 = float("nan")',
       '        print("TESTEMUNHA ESTATICA [v396 -- o psion habita a testemunha estatica; [REAL] os termos do kernel e o calculo, [CONSTRUCTED] a ponte e o colapso, [INPUT/ONTO] as tres falas do operador de 22/10]:")',
       '        print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime; um dado, dois nomes: SEALED_CODATA_ALPHA = ALPHA_FINE_CODATA_2018) ; g e t sao parametros de teste (a pedra os deixa como variaveis)" % _tev396.get("beta", _nan396))',
       '        print("  o PAR ecoa: P^2 = P (residuo %.1e), Tr P = %.1f, Tr P^2 = %.1f (puro) ; o INDIVIDUO nao ecoa: ptr P = (1/2) I (residuo %.1e), defeito de idempotencia %.4f, Tr rho^2 = %.4f, deficit de pureza 1 - Tr rho^2 = %.4f (entropia LINEAR); von Neumann = ln 2 = %.12f (nao 1/2)" % (_tev396.get("pair_idempotence_residual", _nan396), _tev396.get("pair_trace", _nan396), _tev396.get("pair_purity", _nan396), _tev396.get("individual_reduction_residual", _nan396), _tev396.get("individual_idempotence_defect", _nan396), _tev396.get("individual_purity", _nan396), _tev396.get("individual_deficit", _nan396), _tev396.get("von_neumann_entropy", _nan396)))',
       '        print("  fluxo F_t = P + exp(-t beta g)(1 - P): forma fechada vs base de Bell (residuo %.1e), reta do psion fixada por todo t (residuo %.1e), os outros modos movidos (minimo %.3f), testemunha global FALSA (e00 move %.3f), limite F_t x -> P x (residuo %.1e)" % (_tev396.get("closed_form_residual", _nan396), _tev396.get("line_fixed_residual", _nan396), _tev396.get("off_line_min_move", _nan396), _tev396.get("global_witness_move", _nan396), _tev396.get("limit_residual", _nan396)))',
       '        print("  colapso P y P = Tr(P y) P: idempotente (residuo %.1e), conserva Tr(P y) (residuo %.1e), nao injetivo (entradas distintas a %.3f, colapsos a %.1e)" % (_tev396.get("collapse_idempotence_residual", _nan396), _tev396.get("collapse_identity_residual", _nan396), _tev396.get("collapse_noninjectivity_input_gap", _nan396), _tev396.get("collapse_noninjectivity_output_gap", _nan396)))',
       '        print("  kernel: composicao INCONDICIONAL = %s [%s] ; face de Fock do psion = %s, declarada em %s (fora do modulo da pedra: %s; sem habitante exibido)" % ((_tes396.get("unconditional") or {}).get("in_kernel"), (_tes396.get("unconditional") or {}).get("flag"), (_tes396.get("fock_face") or {}).get("status"), (_tes396.get("fock_face") or {}).get("declared_in"), (_tes396.get("fock_face") or {}).get("declared_outside_the_stone")))',
       '        print("  >>> %s <<<\\n" % _tes396["verdict"])',
       '    except Exception as _e396:',
       '        print("   [v396] AVISO: a testemunha estatica nao rodou: %r" % (_e396,))']
edit(m_tes.end(), m_tes.end(), CRLF.join(tes) + CRLF, "N00_main_testemunha", "G_RUNTIME", "main: testemunha_estatica_v396(core) chamado no ponto da fractalizacao do Um, logo depois do bloco psibit_v395, com try/AVISO.")
A_R = linha_unica(r'^        print\("   \[v395\] AVISO: os registros por spec da v395 nao rodaram')
reg = ['    try:   # v396: os registros por spec da v396 (as tres falas do operador de 22/10, lidas junto com a testemunha_estatica_v396, e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito',
       '        _n396 = _v396_rodar_specs(core)',
       '        print("   [v396] a testemunha estatica (o psion habita a fronteira): %s | registros por spec: %d (selados %d)" % ((core.get("testemunha_estatica_v396") or {}).get("verdict"), len(_n396), sum(1 for k_ in _n396 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e396b:',
       '        print("   [v396] AVISO: os registros por spec da v396 nao rodaram: %r" % (_e396b,))']
edit(A_R.end(), A_R.end(), CRLF.join(reg) + CRLF, "N01_main_specs", "G_RUNTIME", "main: registros por spec v396 (try/AVISO), depois do bloco v395.")
A_S = linha_unica(r'^ {12}"registros_v395": \{n_: ')
_sel = ['            "testemunha_estatica_v396": {k_: (core.get("testemunha_estatica_v396") or {}).get(k_) for k_ in ("verdict", "all_verified", "unconditional", "fock_face", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "registros_v396": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V396_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +testemunha_estatica_v396 e registros_v396.")

# ---------------- (5) o bloco de runtime v396 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v396.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]; assert set(axm[DL.THEOREM]) == TRIO
N_AX_UNC = len(axm[DL.THEOREM])
CONTR = RG.contrato(FJ, FORMAL_MAP, E395, sha256(raw)); assert CONTR["expected_ladder"] == ESCADA_ESP
TXT = RG.texto_testemunha()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes["testemunha_pedra"]["sha256"] == FORMAL_MAP[DL.STONE_REL], "a copia duravel da pedra difere da embutida"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v395, por ast)
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
HDR = ("# ====================== v396 (22/10/2026) -- A TESTEMUNHA ESTATICA: a pedra TestemunhaEstatica, o registro testemunha_estatica_v396 e as tres falas do operador de 22/10. O contrato e' DERIVADO do build do sandbox desta cadeia\n"
       "# (gerar_candidato_v396.py), nunca digitado; a fonte autoral da funcao e' runtime_testemunha_v396.py; as falas entram EMBUTIDAS por sha256. O gate nao se move. ======================\n")
RUNTIME_SRC = open(os.path.join(HERE, "runtime_testemunha_v396.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
RCODE = ("_V396_TESTEMUNHA_CONTRACT = " + pprint.pformat(CONTR, width=150, sort_dicts=False) + "\n_V396_TESTEMUNHA_TEXT = " + pprint.pformat(TXT, width=150, sort_dicts=False) + "\n\n\n"
         "_V396_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V396_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V396_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V396_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V396_FONTES)   # v396: o motor de registros (v392) le as fontes e os verbatins das cinco versoes\n_V392_VERBATINS2.update(_V396_VERBATINS2)\n\n\n"
         "def _v396_rodar_specs(core_):\n"
         '    """v396 -- roda os registros por spec da v396 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito."""\n'
         "    for spec_ in _V396_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V396_SPECS]\n')
RT = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v396: o contrato (derivado do build), as falas do operador e os registros por spec\n" + RCODE
ast.parse(RT)
_novo_texto = RUNTIME_SRC + json.dumps(CONTR, ensure_ascii=False) + json.dumps(TXT, ensure_ascii=False) + json.dumps(specs, ensure_ascii=False)   # as falas do operador (verbatim) ficam fora da guarda: a guarda vale para o texto NOVO
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v395 \(21/10/2026\) -- O MODO PSIONICO NA FRACTALIZACAO DO UM")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v396", "G_RUNTIME", "bloco v396: testemunha_estatica_v396 (mecanica + contrato derivado do build), as tres falas, registros por spec.")

# ---------------- (6) artigo e md ----------------
PT0 = open(os.path.join(HERE, "artigo_pt_v396.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v396.pysnip"), encoding="utf-8").read()
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
_controles(RUNTIME_SRC, "runtime_testemunha_v396.py"); _controles([CONTR, TXT, specs, fontes], "contrato/texto/specs/fontes")
PT1_FIRST = open(os.path.join(DL.V395, "artigo_pt_v395.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(DL.V395, "artigo_en_v395.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v396, antes da v395.")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v396, antes da v395.")
A_M = linha_unica(r'^    md\.append\("> \*\*O modo psiônico na fractalização do Um \(v395, 21/10/2026\):\*\*')
edit(A_M.end(), A_M.end(), '    md.append("> **A testemunha estática (v396, 22/10/2026):** ' + str(N_NOVOS) + ' módulo novo no kernel (`TGLExt/TestemunhaEstatica`, nome provisório: quem nomeia é o operador), ' + str(len(FL)) + ' bandeiras só de declaração nomeada, o registro `testemunha_estatica_v396` chamado junto do psibit na fractalização do Um (a mecânica do canto do psion, da redução a um sítio, do fluxo construído e do colapso, calculada com β = α·√e em runtime e lida contra a composição incondicional do kernel), as três falas do operador de 22/10 embutidas por sha256 (`cunhagens_v396`) e a cobertura exata do Audit (`kh_n1_cobertura_v396`). O par ecoa e o indivíduo não ecoa; o fluxo construído tem a reta do psion como o testemunhado estaticamente e a testemunha global é falsa; a ponte é construída, não derivada; o 1/2 da redução é entropia linear (a de von Neumann é ln 2); a face de Fock do psion segue condicional, em outro módulo; as leituras do operador são [INPUT/ONTO]; validade no kernel não é creditação; o gate não muda.\\n\\n")' + CRLF,
     "W07_md", "G_ARTIGO", "md canonico: a linha «A testemunha estática (v396)».")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
T = T0
for a, b, novo, *_ in sorted(EDITS, key=lambda e: -e[0]):
    T = T[:a] + novo + T[b:]
ast.parse(T)
tree = ast.parse(T)
for n in ("testemunha_estatica_v396", "v396_static_witness_mechanics", "_v396_rodar_specs", "_V396_TESTEMUNHA_CONTRACT", "_V396_SPECS", "_V396_NOMES_REGISTROS", "_V396_VERBATINS2", "_V396_TESTEMUNHA_TEXT"):
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V395_SPECS", tree).value) == specs395
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT"):
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V396_REGERAR") == "1", "o candidato ja existe e difere: defina V396_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v395_sha16": SHA0, "escada": [E395, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS],
       "kernel": {"modulos_novos": N_NOVOS, "pedra": {"path": DL.STONE_REL, "sha16": sha16(STONE.encode()), "sha256": sha256(STONE.encode())}, "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()),
                  "raiz_v395_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v395_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "contrato_testemunha": {"sha16": sha16(pprint.pformat(CONTR, width=150, sort_dicts=False).encode()), "n_teoremas": len(CONTR["theorems"]), "n_suporte": len(CONTR["support"]), "bandeira_incondicional": CONTR["unconditional"]["flag"],
                               "fock_face_declarada_em": CONTR["fock_face"]["path"], "expected_ladder": CONTR["expected_ladder"]},
       "registros": spec_nomes + ["testemunha_estatica_v396"], "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E395, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v396.json (pos_build_kernel_v396.py)"},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v395_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v395_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_do_teorema_incondicional": N_AX_UNC,
       "ponto_de_chamada": {"testemunha_estatica_v396": "main: logo depois do bloco psibit_v395 (que vem depois do principio da defasagem fractal, fd = core['fractal_dephasing']), na fractalizacao do Um", "specs": "main: depois do bloco [v395]"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v396.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v396.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v396.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v396.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v396_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v395_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v395:", PFORMAT_IDEMPOTENTE)
