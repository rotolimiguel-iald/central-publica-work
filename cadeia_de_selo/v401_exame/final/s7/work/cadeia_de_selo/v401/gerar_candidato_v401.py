# -*- coding: utf-8 -*-
"""gerar_candidato_v401.py -- gera o um.py CANDIDATO v401 a partir da v400 SELADA (base_v400; o Nos e' so' conferido, NUNCA escrito). PREPARACAO de 25/10/2026 (gerencia c1). Molde: gerar_candidato_v399.py (a cadeia de CONTEUDO) com as licoes da v400.
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +1 modulo (TGLExt/FalsidadeDaInercia.lean: o nome «falsidade (simulacro) da inercia» e' do operador) + raiz + Audit (o import), conferidos byte a byte com o sandbox C:\\t\\k401c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do gerador), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395, testemunha da v396, sonico e afinacao da v398) sobem para a escada da v401 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v399 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo (runtime_v401.py): o registro falsidade_da_inercia_v401 (le o kernel do rito e calcula o modelo oneScaling com beta = alfa x raiz de e em runtime), as CINCO inscricoes de 25/10 embutidas por sha256 e os registros por spec cunhagens_v401
     (com as ratificacoes do operador e a errata ao lado da leitura do escriba no adendo de 03-04/09) e kh_n1_cobertura_v401; chamadas no main (depois da declaracao do operador, e os specs depois dos da v399) e o resumo no selo;
 (E) a secao «A falsidade (simulacro) da inercia» PT/EN antes da secao v399 e a linha do .md. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44: este gerador nao o toca).
A INERCIA, como o operador a define: o proprio zero absoluto (0_abs, 1=0); w(I)=1 e' o Um POSTO que a interrompe (1=1). A leitura do escriba no adendo de 03-04/09 («w(I)=1 e a INERCIA») fica SUPERADA (errata ao lado, da gerencia).
uso: python -I -B -X utf8 gerar_candidato_v401.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v401 as GP  # noqa: E402
import registros_v401 as RG  # noqa: E402
import delta_v401 as DL  # noqa: E402
import acom_conferencias_v401 as AC  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP400 = json.load(open(os.path.join(DL.V400, "ESPERADOS_v400.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP400["candidato_sha16"]:   # o Nos ja nao e' a v400 (rito v401 em curso): a v400 SELADA vem da copia base_v400
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v400 selada"
SHA0 = sha16(raw); assert SHA0 == ESP400["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E400 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E400 == ESP400["escada"][1], (E400, ESP400["escada"])
T0 = raw.decode("utf-8")
tree0 = ast.parse(T0)
LS = [0] + [m.end() for m in re.finditer("\n", T0)]
LF_SOLTOS0 = len(re.findall(r"(?<!\r)\n", T0))   # os LF soltos (textos Lean embutidos); o candidato nao pode criar nem perder nenhum


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
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v401.json"), encoding="utf-8"))["novos"]; assert nov == DL.STONE_RELS, "a lista dos modulos novos tem de ser so' a pedra FalsidadeDaInercia"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v400 + o import da pedra FalsidadeDaInercia"
STONES_TXT = {}
for s in DL.STONES:
    STONES_TXT[s["rel"]] = rd(os.path.join(KB, *s["rel"].split("/")))
    assert STONES_TXT[s["rel"]] == rd(s["src"]) == rd(s["origem"]), "a pedra do sandbox difere da fonte (v401\\pedra, work\\...): rode copiar_pedras_v401.py e preparar_kernel_v401.py gerar"
    assert s["rel"] not in old_d
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONES_TXT[s["rel"]], flags=re.S)), "sorry no codigo da pedra " + s["name"]
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (+ o import da pedra FalsidadeDaInercia; sandbox == embutido)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (s["rel"], repr(STONES_TXT[s["rel"]]), CRLF) for s in DL.STONES), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +1 modulo Lean (TGLExt/FalsidadeDaInercia.lean), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v401.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v400"
assert all(DL.classe(n) == "nomeada" and m in DL.STONE_MODS for _, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada do modulo da pedra"
assert all(s["theorem"] in {n for _, n, _ in FL} and s["key_theorem"] in {n for _, n, _ in FL} for s in DL.STONES), "a composicao e a estrela da pedra tem de ter bandeira"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v401 (25/10/2026): a pedra FalsidadeDaInercia (o nome «falsidade (simulacro) da inercia» e' do operador; %d bandeiras): %d bandeiras no total, SO' de declaracao NOMEADA (a pratica da v392 a v399; as %d auxiliares geradas pelo compilador ficam fora)"
     % (FJ["nomeadas_por_pedra"]["falsidade"], len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E400 and len(set(old_lad)) == E400
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v401: a pedra FalsidadeDaInercia (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v401 (25/10/2026): a pedra FalsidadeDaInercia (a inercia, como o operador a define, e' o proprio zero absoluto: um posto de peso 1 que fosse inercial daria 1 = 0, a falsidade; o simulacro e' o custo da interrupcao, nao o zero; a inscricao do Um posto interrompe a inercia; "
     "composicao por citacao sobre os dados da escala dual de Takesaki; a identificacao com o fluxo de um corpo fisico e' [OPEN]; o nome e' do operador)" + CRLF
     + '    ("v401", "%s", "%s", None, None),%s' % (DL.STONES[0]["name"], DL.STONES[0]["rel"], CRLF), "V03_ledger", "G_KERNEL", "ledger de pedras: +1.")
m = re.search(r'^UM_VERSION = "v400"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v401"   # v401 (25/10/2026): a CONSTANTE UNICA de versao -- a falsidade (simulacro) da inercia: a pedra FalsidadeDaInercia (a inercia e o proprio zero absoluto), o registro falsidade_da_inercia_v401, as cinco inscricoes de 25/10, as ratificacoes do operador '
           'e a errata ao lado da leitura do escriba no adendo de 03-04/09; v400 em 24/10 (a correcao: o alfa unico); v399 (o testemunho de dois: o selo pela propria tecnologia)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v401'.")

# ---------------- (3) o que a v401 muda nos registros das versoes anteriores (so' dados) ----------------
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT"):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E400
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V399_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E400, ESCADA_ESP))
sv = top("_V399_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs399 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs399, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
assert PFORMAT_IDEMPOTENTE, "o pformat dos specs v399 no um.py base nao e' idempotente: nao reescrevo o bloco"
khs = [s for s in specs399 if s["nome"] == "kh_n1_cobertura_v399"]; assert len(khs) == 1
k9 = khs[0]
H8_ANTIGO_N = None
for c in k9["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v401: piso historico (a cobertura cresce com o modulo FalsidadeDaInercia); a igualdade exata esta em kh_n1_cobertura_v401"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v401: piso historico; a igualdade exata esta em kh_n1_cobertura_v401"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v401: a arvore ganha o arquivo da pedra, entao o registro da v399 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v401" % H8_ANTIGO_N
k9["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v399 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v399 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v399 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v401 a cobertura cresce com o modulo FalsidadeDaInercia e a arvore ganha o arquivo da pedra: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v401. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v399 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v401 quebra (a mesma lacuna que a v399 achou no registro da v398, a v398 no da v397 e a v397 no da v396)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k9["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v399"
edit(spa, spb, pprint.pformat(specs399, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v399_pisos", "G_V399_PISOS", "_V399_SPECS: kh_n1_cobertura_v399 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (4) main: chamadas e selo ----------------
A_DEC = linha_unica(r'^        print\("   \[v399\] AVISO: a declaracao do operador nao rodou: %r" % \(_e399d,\)\)')
BLOCO_N00 = r'''    try:   # v401: a FALSIDADE (SIMULACRO) DA INERCIA, lida no mesmo ponto das pedras anteriores (depois da declaracao do operador): o kernel do proprio rito e o modelo oneScaling com beta = alfa x raiz de e em runtime; excecao vira AVISO visivel, nunca derruba o rito
        _fal401 = falsidade_da_inercia_v401(core)
        _fav401 = _fal401.get("values") or {}
        _nan401 = float("nan")
        print("FALSIDADE (SIMULACRO) DA INERCIA [v401 -- a inercia e' o proprio zero absoluto (definicao do operador, 25/10/2026); um posto de peso 1 inercial daria 1 = 0; [REAL] os termos do kernel e o calculo no modelo oneScaling, [KNOWN] a lei de escala de Takesaki, [ONTO] a leitura de Newton e da massa, [OPEN] o fluxo de um corpo fisico]:")
        print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime) ; o peso do posto depois da escala s e' e^{-s}: distancia minima a 1 nas %s escalas de teste = %.6f ; so' o estado nulo e' fixo pelo fluxo inteiro: %s ; escalas nao triviais que fixam o posto: %s" % (_fav401.get("beta", _nan401), _fav401.get("grid_scales"), _fav401.get("min_distance_of_post_weight_to_one", _nan401), _fav401.get("fixed_by_the_whole_flow"), _fav401.get("post_inertial_scales")))
        print("  o simulacro: custo t.beta.g minimo %.9f > 0 ; defasagem maxima %.9f < 1 ; perda por unidade 1 - e^{-beta} = %.12f" % (_fav401.get("min_cost_t_beta_g", _nan401), _fav401.get("max_dephasing_factor", _nan401), _fav401.get("loss_per_unit", _nan401)))
        print("  kernel: composicao = %s [%s] ; estrela (um posto inercial daria 1 = 0) = %s [%s] ; o 0_abs de TGLExt.costless no kernel embutido = %s" % ((_fal401.get("unconditional") or {}).get("in_kernel"), (_fal401.get("unconditional") or {}).get("flag"), (_fal401.get("key_theorem") or {}).get("in_kernel"), (_fal401.get("key_theorem") or {}).get("flag"), (_fal401.get("costless") or {}).get("ok")))
        print("  >>> %s <<<\n" % _fal401["verdict"])
    except Exception as _e401:
        print("   [v401] AVISO: a falsidade da inercia nao rodou: %r" % (_e401,))
'''
edit(A_DEC.end(), A_DEC.end(), crlf(BLOCO_N00), "N00_main_falsidade", "G_RUNTIME", "main: falsidade_da_inercia_v401(core) chamada logo depois do bloco declaracao_do_operador_v399, com try/AVISO.")
A_R = linha_unica(r'^        print\("   \[v399\] AVISO: os registros por spec da v399 nao rodaram')
BLOCO_N01 = r'''    try:   # v401: os registros por spec da v401 (as cinco inscricoes de 25/10 -- falas do operador --, as ratificacoes, a errata ao lado do adendo e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _n401 = _v401_rodar_specs(core)
        print("   [v401] a falsidade (simulacro) da inercia (lida depois da declaracao do operador) e as inscricoes de 25/10 (cunhagens_v401): falsidade=%s | cunhagens=%s | registros por spec: %d (selados %d)" % ((core.get("falsidade_da_inercia_v401") or {}).get("verdict"), (core.get("cunhagens_v401") or {}).get("verdict"), len(_n401), sum(1 for k_ in _n401 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e401b:
        print("   [v401] AVISO: os registros por spec da v401 nao rodaram: %r" % (_e401b,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N01), "N01_main_specs", "G_RUNTIME", "main: registros por spec v401 (try/AVISO), depois do bloco v399.")
A_S = linha_unica(r'^ {12}"registros_v399": \{n_: ')
_sel = ['            "falsidade_da_inercia_v401": {k_: (core.get("falsidade_da_inercia_v401") or {}).get(k_) for k_ in ("verdict", "all_verified", "unconditional", "key_theorem", "costless", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "registros_v401": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V401_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +falsidade_da_inercia_v401 e registros_v401.")

# ---------------- (5) o bloco de runtime v401 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v401.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
N_AX = {}
for s in DL.STONES:
    assert set(axm[s["theorem"]]) == TRIO, s["theorem"]
    N_AX[s["key"]] = len(axm[s["theorem"]])
CONTR_FAL = RG.contrato(FJ, FORMAL_MAP, E400, sha256(raw)); assert CONTR_FAL["expected_ladder"] == ESCADA_ESP
TXT_FAL = RG.texto_falsidade()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes["falsidade_pedra"]["sha256"] == FORMAL_MAP[DL.STONES[0]["rel"]], "a copia duravel da pedra difere da embutida"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v400, por ast)
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
specs = RG.especs(FORMAL_MAP, khj, H8, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], N_AX)
spec_nomes = [s["nome"] for s in specs]
assert spec_nomes == [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V401)
assert not GP.violacoes(json.dumps(TXT_FAL, ensure_ascii=False)) and not GUARDA.search(TXT_FAL["veredito_ok"]), "P18 ou palavra recusada no texto do registro da falsidade"
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v401.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V401_FALSIDADE_CONTRACT = " + pprint.pformat(CONTR_FAL, width=150, sort_dicts=False) + "\n_V401_FALSIDADE_TEXT = " + pprint.pformat(TXT_FAL, width=150, sort_dicts=False)
         + "\n_V401_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V401_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V401_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V401_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V401_FONTES)   # v401: o motor de registros (v392) le as fontes e os verbatins das nove versoes\n_V392_VERBATINS2.update(_V401_VERBATINS2)\n\n\n"
         "def _v401_rodar_specs(core_):\n"
         '    """v401 -- roda os registros por spec da v401 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro falsidade_da_inercia_v401 NAO entra aqui: roda no main, depois da declaracao do operador."""\n'
         "    for spec_ in _V401_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V401_SPECS]\n')
HDR = ("# ====================== v401 (25/10/2026) -- A FALSIDADE (SIMULACRO) DA INERCIA: a pedra FalsidadeDaInercia, o registro falsidade_da_inercia_v401 (com FUNCAO, lido no ponto do rito depois da declaracao do operador), as cinco inscricoes de 25/10, as ratificacoes do operador e os registros por spec cunhagens_v401 e kh_n1_cobertura_v401.\n"
       "# A INERCIA, como o operador a define: o proprio zero absoluto (0_abs, 1=0); w(I)=1 e' o Um POSTO que a interrompe (1=1). O contrato (_V401_FALSIDADE_CONTRACT) e as inscricoes (_V401_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. O gate nao se move.\n")
RT = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v401: o contrato (derivado do build), o texto, as fontes pinadas, as cinco inscricoes de 25/10 e os registros por spec\n" + RCODE
ast.parse(RT)
_novo_texto = RT + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v399 \(24/10/2026\) -- O TESTEMUNHO DE DOIS")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v401", "G_RUNTIME", "bloco v401: o registro da falsidade da inercia, as cinco inscricoes de 25/10, as ratificacoes e os registros por spec.")


# ---------------- (6) artigo e md ----------------
def _controles(obj, onde):
    """Guarda de CARACTERE DE CONTROLE (licao da v396): nenhuma string de texto novo pode ter caractere de controle alem do fim de linha."""
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo (barra invertida colapsada?)", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


PT0 = open(os.path.join(HERE, "artigo_pt_v401.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v401.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT, "runtime_v401.py"); _controles([CONTR_FAL, TXT_FAL, specs, fontes], "contratos/specs/fontes")
PT9_FIRST = open(os.path.join(DL.V399, "artigo_pt_v399.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN9_FIRST = open(os.path.join(DL.V399, "artigo_en_v399.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT9_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT9_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v401, antes da v399.")
replace_unique(EN9_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN9_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v401, antes da v399.")
A_M = re.search(r'^    md\.append\("> \*\*O testemunho de dois: o selo pela própria tecnologia \(v399, 24/10/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*O testemunho de dois', T0, re.M)) == 1, "a linha da v399 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **A falsidade (simulacro) da inércia (v401, 25/10/2026):** ' + str(N_NOVOS) + ' módulo novo no kernel (`TGLExt/FalsidadeDaInercia`; o nome «falsidade (simulacro) da inércia» é do operador) com ' + str(len(FL)) + ' bandeiras só de declaração nomeada. '
            'A inércia, como o operador a define, é o próprio zero absoluto (o `0_abs` do kernel, `TGLExt.costless`: «nunca correspondeu, e por isso nada custa»; 1=0); o `ω(I)=1` é o Um posto que a interrompe (1=1). A pedra tipa a diferença por citação, sobre os dados da escala dual de Takesaki ([KNOWN]): '
            'o que o fluxo inteiro fixa pesa zero; um posto de peso 1 que fosse inercial daria `(1:ℝ)=0` (a falsidade; o simulacro é o custo da interrupção, `t·β·g>0`, não o zero); a inscrição interrompe a inércia [REAL]. '
            'A CADEIA DERIVADA [DERIVED] (a extensão da pedra, vinte teoremas, pedida pelo operador como derivada e não [ONTO] dele): nada que porte posto precede a impressão do Um posto; a inércia não é causa de si mesma; o primeiro movimento é a impressão; o zero é a consequência da poda, não o início; a tensão projetada no atrator (`falsidade_da_inercia_derivada`), a partir do axioma e da lei de Takesaki [KNOWN]. '
            'A única hipótese nomeada, `H_τ` (τ é a massa de Newton e a métrica de Einstein), é [OPEN] e nenhum teorema a usa; a ORDEM 025 ao Codex (sha16 `3fd2b5a801071343`) é pendência externa. '
            'O registro `falsidade_da_inercia_v401` lê o kernel do rito e calcula, no modelo oneScaling, com β=α·√e em tempo de execução, que o peso do posto depois da escala s é e^(−s), igual a 1 só em s=0. '
            'ERRATA AO LADO (da gerência, em nome próprio): a leitura do escriba no adendo de 03–04/09/2026, «ω(I)=1 é a inércia», fica superada pela definição do operador. As ratificações do operador de 25/10 («Ratifico tudo.») tornam definitivos os nomes antes provisórios. '
            'E = mc² é [KNOWN] (relatividade restrita), não termo do kernel; a massa lida pela TGL é o custo do nada, a cristalização da dobra da luz no vácuo relativa ao observador [ONTO]; a identificação da escala dual com o fluxo de um corpo físico é [OPEN]. '
            'O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «A falsidade (simulacro) da inercia (v401)», antes da linha da v399.")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))


def montar(k_espacos):
    """aplica os EDITS; o comentario da linha de versao ganha `k_espacos` espacos no fim (ver o AJUSTE DO CONTROLE N10 abaixo)"""
    T_ = T0
    for a_, b_, novo_, pid_, *_r in sorted(EDITS, key=lambda e: -e[0]):
        if pid_ == "W01_versao":
            novo_ = novo_[:-len(CRLF)] + " " * k_espacos + CRLF
        T_ = T_[:a_] + novo_ + T_[b_:]
    return T_


def n10_aplica(T_):
    """AJUSTE DO CONTROLE N10 (licao da v401): o controle negativo N10 (transposicao de 2 bytes) da secao do selo pela propria tecnologia (v399/v400, pinada, que a v401 NAO muda) so' existe SE os bytes nas posicoes n//2 e n//2 + 3 do objeto forem diferentes -- o um.py INTEIRO no conferidor e a AMOSTRA de 1 MiB no registro do core --
    (`if b[i] != b[j]`); o conferidor do rito exige os 13 controles sobre o um.py instalado inteiro (C8). Com o corpo da v401 a coincidencia dos bytes derrubaria o N10 (12 controles): o gerador acrescenta, se preciso, espacos ao FIM do comentario da linha UM_VERSION ate' os dois bytes diferirem."""
    bb = T_.encode("utf-8")
    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])   # o um.py INTEIRO (C8 do conferidor) e a AMOSTRA de 1 MiB (o registro do selo no core: registro_core_v399, amostra = 1 << 20)


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF): toda insercao tem de passar por crlf()"
NOVOS_NOMES = ("falsidade_da_inercia_v401", "v401_falsidade_mechanics", "_v401_formal", "_V401_RECUSA", "_V401_FALSIDADE_CONTRACT", "_V401_FALSIDADE_TEXT", "_V401_FONTES", "_V401_VERBATINS2", "_V401_SPECS", "_V401_NOMES_REGISTROS", "_v401_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
# o bloco nao redefine nenhum nome de nivel de modulo do um.py base (C3 sobre o texto FINAL): so' o import `math as _m401`
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V399_SPECS", tree).value) == specs399
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT"):
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado (licao da v400)
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v401" and float(a1_.group(1)) == 7.2973525693e-3
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V401_REGERAR") == "1", "o candidato ja existe e difere: defina V401_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v400_sha16": SHA0, "base_v400_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E400, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "pedras": {s["rel"]: {"sha16": sha16(STONES_TXT[s["rel"]].encode()), "sha256": sha256(STONES_TXT[s["rel"]].encode()), "bandeiras": FJ["nomeadas_por_pedra"][s["key"]]} for s in DL.STONES},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v400_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v400_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": [DL.REGISTRO_FALSIDADE] + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E400, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v401.json (pos_build_kernel_v401.py)",
                                 "bandeiras_do_teorema": FJ["bandeira_do_teorema_incondicional"], "suporte": {s["key"]: dict(s["support"]) for s in DL.STONES}, "contrato": CONTR_FAL},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v399_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v399_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_da_composicao": N_AX,
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v400": g0, "candidato_v401": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "ratificacoes": [r["id"] for r in DL.RATIFICACOES], "decisoes": dict(DL.DECISOES), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"falsidade_da_inercia_v401": "main: IMEDIATAMENTE depois do bloco declaracao_do_operador_v399", "specs": "main: depois do bloco [v399]", "resumos_no_selo": "main: no dict do selo, depois de registros_v399 (falsidade_da_inercia_v401 e registros_v401)",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v401"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v401.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v401.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v401.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v401_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v400_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v399:", PFORMAT_IDEMPOTENTE)
