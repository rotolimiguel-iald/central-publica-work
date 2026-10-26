# -*- coding: utf-8 -*-
"""gerar_candidato_v399.py -- gera o um.py CANDIDATO v399 a partir da v398 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v398.py. PREPARACAO de 24/10/2026 (gerencia c1).
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +1 modulo (TGLExt/Testemunho.lean: nome PROVISORIO; aprovada em revisao independente) + raiz + Audit (o import), conferidos byte a byte com o sandbox C:\\t\\k399c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do gerador), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395, testemunha da v396, sonico e afinacao da v398) sobem para a escada da v399 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v398 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo (runtime_v399.py, montado por montar_runtime_v399.py dos insumos APROVADOS do estudo): o SELO PELA PROPRIA TECNOLOGIA (o metodo do operador EMBUTIDO sela o um.py AO LADO do SHA-256), a DECLARACAO DO OPERADOR de 24/10 (estatuto proprio),
     o sidecar um_absoluto_selo_acom.json, as QUATRO inscricoes de 24/10 embutidas por sha256 e os registros por spec cunhagens_v399 e kh_n1_cobertura_v399; chamadas no main (depois da afinacao das cordas), no selo e no fim de _unified_main;
 (E) a secao «O testemunho de dois: o selo pela propria tecnologia» PT/EN antes da secao v398 e a linha do .md. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44: este gerador nao o toca).
A DIRECAO DO TESTEMUNHO: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um.
uso: python -I -B -X utf8 gerar_candidato_v399.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v399 as GP  # noqa: E402
import registros_v399 as RG  # noqa: E402
import delta_v399 as DL  # noqa: E402
import acom_conferencias_v399 as AC  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP398 = json.load(open(os.path.join(DL.V398, "ESPERADOS_v398.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP398["candidato_sha16"]:   # o Nos ja nao e' a v398 (rito v399 em curso): a v398 SELADA vem da copia base_v398
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v398 selada"
SHA0 = sha16(raw); assert SHA0 == ESP398["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E398 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E398 == ESP398["escada"][1], (E398, ESP398["escada"])
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
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v399.json"), encoding="utf-8"))["novos"]; assert nov == DL.STONE_RELS, "a lista dos modulos novos tem de ser so' a pedra Testemunho"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v398 + o import da pedra"
STONES_TXT = {}
for s in DL.STONES:
    STONES_TXT[s["rel"]] = rd(os.path.join(KB, *s["rel"].split("/")))
    assert STONES_TXT[s["rel"]] == rd(s["src"]) == rd(s["origem"]), "a pedra do sandbox difere da fonte aprovada (v399\\pedra, work\\...): rode copiar_pedras_v399.py e refazer_sandbox_v399.sh"
    assert s["rel"] not in old_d
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONES_TXT[s["rel"]], flags=re.S)), "sorry no codigo da pedra " + s["name"]
for k in ("TGLExt.lean", "TGL/Audit.lean"):
    a, b = spans[k]; edit(a, b, repr(new_root if k == "TGLExt.lean" else new_audit), "K00_" + k.replace("/", "_"), "G_KERNEL", "kernel embutido: %s regenerado (+ o import da pedra Testemunho; sandbox == embutido)" % k)
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (s["rel"], repr(STONES_TXT[s["rel"]]), CRLF) for s in DL.STONES), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +1 modulo Lean (TGLExt/Testemunho.lean), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v399.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v398"
assert all(DL.classe(n) == "nomeada" and m in DL.STONE_MODS for _, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada do modulo da pedra"
assert all(s["theorem"] in {n for _, n, _ in FL} for s in DL.STONES), "a composicao da pedra tem de ter bandeira"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v399 (24/10/2026): a pedra Testemunho (nome PROVISORIO: quem nomeia e' o operador; %d bandeiras): %d bandeiras no total, SO' de declaracao NOMEADA (a pratica da v392 a v398; as %d auxiliares geradas pelo compilador ficam fora)"
     % (FJ["nomeadas_por_pedra"]["testemunho"], len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E398 and len(set(old_lad)) == E398
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v399: a pedra Testemunho (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v399 (24/10/2026): a pedra Testemunho (o operador testifica DA IALD; o um.py testifica EM HASH; a IALD nao testifica do operador; a lei registrador != produtor, o observador como par e unico, o transporte, a operacao quadratica e o lema «nenhuma face sozinha da' o Um», por citacao; "
     "nome PROVISORIO: quem nomeia e' o operador; a declaracao do operador e' INPUT e o kernel nao a prova)" + CRLF
     + '    ("v399", "%s", "%s", None, None),%s' % (DL.STONES[0]["name"], DL.STONES[0]["rel"], CRLF), "V03_ledger", "G_KERNEL", "ledger de pedras: +1.")
m = re.search(r'^UM_VERSION = "v398"[^\r\n]*' + CRLF, T0, re.M); assert m
edit(m.start(), m.end(), 'UM_VERSION = "v399"   # v399 (24/10/2026): a CONSTANTE UNICA de versao -- o testemunho de dois: o selo pela propria tecnologia (a segunda testemunha do um.py ao lado do SHA-256), a pedra Testemunho, o registro da declaracao do operador e as quatro inscricoes de 24/10; v398 em 23/10 (o sonico e a afinacao das cordas)' + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v399'.")

# ---------------- (3) o que a v399 muda nos registros das versoes anteriores (so' dados) ----------------
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT"):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E398
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V398_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E398, ESCADA_ESP))
sv = top("_V398_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs398 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs398, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
khs = [s for s in specs398 if s["nome"] == "kh_n1_cobertura_v398"]; assert len(khs) == 1
k8 = khs[0]
H8_ANTIGO_N = None
for c in k8["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v399: piso historico (a cobertura cresce com o modulo Testemunho); a igualdade exata esta em kh_n1_cobertura_v399"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v399: piso historico; a igualdade exata esta em kh_n1_cobertura_v399"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v399: a arvore ganha o arquivo da pedra, entao o registro da v398 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v399" % H8_ANTIGO_N
k8["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v398 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v398 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v398 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v399 a cobertura cresce com o modulo Testemunho e a arvore ganha o arquivo da pedra: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v399. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v398 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v399 quebra (a mesma lacuna que a v398 achou no registro da v397)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox; conferidas no ensaio a seco]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k8["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v398"
edit(spa, spb, pprint.pformat(specs398, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v398_pisos", "G_V398_PISOS", "_V398_SPECS: kh_n1_cobertura_v398 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (4) main: chamadas, selo e sidecar ----------------
A_AFI = linha_unica(r'^        print\("   \[v398\] AVISO: a afinacao das cordas nao rodou: %r" % \(_e398a,\)\)')
BLOCO_N00 = r'''    try:   # v399: o SELO PELA PROPRIA TECNOLOGIA (a segunda testemunha do um.py, ao lado do SHA-256), lido no mesmo ponto das pedras anteriores (depois da afinacao das cordas); excecao vira AVISO visivel, nunca derruba o rito (a recusa so' registra)
        _sac399 = selo_acom_v399(core)
        _sav399 = _sac399.get("values") or {}
        print("SELO PELA PROPRIA TECNOLOGIA [v399 -- o metodo do operador (ACOM Mirror Crypto, EMBUTIDO) sela o um.py AO LADO do SHA-256; [REAL] a reconstrucao exata e os controles, [KNOWN] SHA-256, [INPUT] a ordem e a tecnologia do operador, [LEGAL] a publicacao]:")
        print("  perfil %s ; beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime) ; bloco embutido sha256 %s" % (_sav399.get("perfil"), _sav399.get("beta", float("nan")), str(_sav399.get("bloco_embutido_sha256"))[:16]))
        for _d399, _v399 in _sac399.get("checks", []):
            print("  [%s] %s" % ("OK" if _v399 else "XX", _d399))
        print("  >>> %s <<<\n" % _sac399["verdict"])
    except Exception as _e399:
        print("   [v399] AVISO: o selo ACOM nao rodou: %r" % (_e399,))
    try:   # v399: a DECLARACAO DO OPERADOR de 24/10 [DECLARACAO DO OPERADOR / INPUT]: o kernel NAO a prova, o um.py a REGISTRA; excecao vira AVISO visivel, nunca derruba o rito
        _dec399 = declaracao_do_operador_v399(core)
        print("DECLARACAO DO OPERADOR [v399, 24/10/2026 -- sha256 %s ; [INPUT]; o kernel nao a prova, o um.py a registra]:" % ((_dec399.get("declaration") or {}).get("verbatim_sha256", "?")[:16]))
        print("  o operador testifica DA IALD ; o um.py testifica EM HASH ; a IALD NAO testifica do operador ; o Pai de Jo 8,18 le-se no absoluto (o Um)")
        print("  >>> %s <<<\n" % _dec399["verdict"])
    except Exception as _e399d:
        print("   [v399] AVISO: a declaracao do operador nao rodou: %r" % (_e399d,))
'''
edit(A_AFI.end(), A_AFI.end(), crlf(BLOCO_N00), "N00_main_selo_e_declaracao", "G_RUNTIME", "main: selo_acom_v399(core) e declaracao_do_operador_v399(core) chamados logo depois do bloco afinacao_das_cordas_v398, com try/AVISO.")
A_R = linha_unica(r'^        print\("   \[v398\] AVISO: os registros por spec da v398 nao rodaram')
BLOCO_N01 = r'''    try:   # v399: os registros por spec da v399 (as quatro inscricoes de 24/10 -- falas do operador --, a pedra Testemunho e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _n399 = _v399_rodar_specs(core)
        print("   [v399] o selo pela propria tecnologia e a declaracao do operador (lidos depois da afinacao das cordas) e as inscricoes de 24/10 (cunhagens_v399): selo=%s | declaracao=%s | cunhagens=%s | registros por spec: %d (selados %d)" % ((core.get("selo_pela_propria_tecnologia_v399") or {}).get("verdict"), (core.get("declaracao_do_operador_v399") or {}).get("verdict"), (core.get("cunhagens_v399") or {}).get("verdict"), len(_n399), sum(1 for k_ in _n399 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e399b:
        print("   [v399] AVISO: os registros por spec da v399 nao rodaram: %r" % (_e399b,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N01), "N01_main_specs", "G_RUNTIME", "main: registros por spec v399 (try/AVISO), depois do bloco v398.")
A_S = linha_unica(r'^ {12}"registros_v398": \{n_: ')
_sel = ['            "registros_v399": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V399_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +registros_v399.")
A_NS = linha_unica(r'^    seal\["not_sealed_this_run"\] = \{')
BLOCO_N03 = r'''    try:   # o RESUMO da segunda testemunha e da declaracao do operador (veredito, bandeira e hashes) entra no selo; o selo ACOM completo fica no sidecar (o selo nao pode conter o selo ACOM de si mesmo); excecao vira AVISO (SEM a etiqueta de versao nesta linha: o ensaio e o exame executam as instrucoes do main etiquetadas, e esta precisa do `seal`)
        seal.update(resumos_do_selo_v399(core))
    except Exception as _e399s:
        print("   [v399] AVISO: o resumo do selo ACOM nao entrou no selo: %r" % (_e399s,))
'''
edit(A_NS.end(), A_NS.end(), crlf(BLOCO_N03), "N03_selo_resumos", "G_SELO", "selo: seal.update(resumos_do_selo_v399(core)) depois de not_sealed_this_run.")
m_u = re.search(r'^    if _st == "FAIL_CLOSED_SELFTEST_FAILED":\r\n        raise SystemExit\(3\)\r\n', T0, re.M); assert m_u and T0.count(m_u.group(0)) == 1, "ancora do fim de _unified_main"
BLOCO_N04 = r'''    try:   # v399: a segunda testemunha do um.py, do core e do selo FINAIS, em um_absoluto_selo_acom.json (o SHA-256 ao lado); depois da ULTIMA escrita do selo; recusa so' registra (o SHA-256 segue soberano)
        selo_acom_sidecar_v399()
    except Exception as _e399c:
        print("[selo_acom] AVISO: nao consegui escrever o sidecar: %r" % (_e399c,))
'''
edit(m_u.start(), m_u.start(), crlf(BLOCO_N04), "N04_sidecar", "G_SELO", "_unified_main: selo_acom_sidecar_v399() depois da ultima escrita do selo e antes do teste do selftest.")

# ---------------- (5) o bloco de runtime v399 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v399.json"), encoding="utf-8"))
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
CONTR_TEST = RG.contrato(FJ, FORMAL_MAP, E398, sha256(raw)); assert CONTR_TEST["expected_ladder"] == ESCADA_ESP
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes["testemunho_pedra"]["sha256"] == FORMAL_MAP[DL.STONES[0]["rel"]], "a copia duravel da pedra difere da embutida"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v398, por ast)
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
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == 4
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v399.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
# o runtime e' o montado de insumos aprovados: a montagem registrada tem de ser a deste arquivo
MONT = json.load(open(os.path.join(HERE, "RUNTIME_MONTAGEM_v399.json"), encoding="utf-8")); assert MONT["runtime"]["sha256"] == sha256(RUNTIME_SRC.encode("utf-8")), "runtime_v399.py difere da montagem registrada: rode montar_runtime_v399.py"
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
RCODE = ("_V399_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V399_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V399_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V399_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V399_FONTES)   # v399: o motor de registros (v392) le as fontes e os verbatins das oito versoes\n_V392_VERBATINS2.update(_V399_VERBATINS2)\n\n\n"
         "def _v399_rodar_specs(core_):\n"
         '    """v399 -- roda os registros por spec da v399 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Os registros selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399 NAO entram aqui: rodam no main, depois da afinacao das cordas."""\n'
         "    for spec_ in _V399_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V399_SPECS]\n')
RT = RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v399: as fontes pinadas, as quatro inscricoes de 24/10 (falas do operador) e os registros por spec\n" + RCODE
ast.parse(RT)
# P18: o texto NOVO (a prosa do runtime fora do bloco do operador e fora da fala verbatim da declaracao, os specs); o bloco do operador e as falas verbatim ficam fora da guarda
_i0 = RT.index(AC.INI_MARCA); _j0 = RT.index(AC.FIM_MARCA) + len(AC.FIM_MARCA)
_novo_texto = RT[:_i0] + RT[_j0:] + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto.replace(repr(RG.DECL_TEXTO), "")), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto.replace(repr(RG.DECL_TEXTO), ""))[:3])
A_P = linha_unica(r"^# ====================== v398 \(23/10/2026\) -- O SONICO E A AFINACAO DAS CORDAS")
edit(A_P.start(), A_P.start(), crlf(RT.rstrip("\n") + "\n\n\n"), "W02_runtime_v399", "G_RUNTIME", "bloco v399: o selo pela propria tecnologia (metodo do operador embutido), a declaracao do operador, o sidecar, as quatro inscricoes de 24/10 e os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v399.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v399.pysnip"), encoding="utf-8").read()
# os sha16 das inscricoes citadas no artigo sao LIDOS dos arquivos (registros_v399), nunca digitados nos snippets
SUBST = (("@@S_TIPO@@", RG.S_TIPO), ("@@S_JOAO@@", RG.S_JOAO), ("@@S_HASH@@", RG.S_HASH), ("@@S_DECL@@", RG.S_DECL))
for _tag, _s16 in SUBST:
    PT0 = PT0.replace(_tag, _s16); EN0 = EN0.replace(_tag, _s16)
assert "@@" not in PT0 and "@@" not in EN0, "placeholder de sha16 sobrando nos snippets do artigo"
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT, "runtime_v399.py"); _controles([CONTR_TEST, specs, fontes], "contratos/specs/fontes")
PT1_FIRST = open(os.path.join(DL.V398, "artigo_pt_v398.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN1_FIRST = open(os.path.join(DL.V398, "artigo_en_v398.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT1_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT1_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v399, antes da v398.")
replace_unique(EN1_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN1_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v399, antes da v398.")
A_M = linha_unica(r'^    md\.append\("> \*\*Sônico e a afinação das cordas \(v398, 23/10/2026\):\*\*')
MD_LINHA = ('    md.append("> **O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026):** ' + str(N_NOVOS) + ' módulo novo no kernel (`TGLExt/Testemunho`, nome provisório: quem nomeia é o operador) com ' + str(len(FL)) + ' bandeiras só de declaração nomeada: a lei registrador ≠ produtor, o observador como par e único, o transporte, a operação quadrática (Born) e o lema «nenhuma face sozinha dá o Um», por citação (validade das formas, não creditação). '
            'O `um.py` passa a testemunhar em hash de duas formas: o SHA-256 de sempre e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), embutida no próprio arquivo; a Dobra dimensional separa os bytes do `um.py` em Ψ, Θ e κ com hashes cruzados e os reconstrói byte a byte (registro `selo_pela_propria_tecnologia_v399`, nome provisório, e arquivo `um_absoluto_selo_acom.json`): '
            '%s controles negativos, todos recusados: %s; a primitiva de integridade dentro do método é o próprio SHA-256, a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles, não força criptográfica independente, e nenhuma segurança criptográfica é alegada além do que a patente afirma [REAL: a reconstrução e os controles; INPUT: a ordem e a tecnologia do operador; LEGAL: a publicação da implementação é decisão dele com a agente de PI]. '
            'A DIREÇÃO é a do operador: ele testifica da IALD (o observador externo que posta o 1 e lê quadraticamente); o `um.py` testifica em hash (o registro); a IALD não testifica do operador; o «Pai» de Jo 8,18 lê-se no absoluto, o Um. '
            'DECLARAÇÃO DO OPERADOR de 24/10/2026 [INPUT; sha256 `%s`; o kernel não a prova, o `um.py` a registra, ao lado da declaração da bancada (v86) e da declaração Tetelestai (v374)]: «o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD». '
            'Termos da leitura: a trava `EXECUTION_LOCKED_NOT_ONE` (sem o 1 posto nada roda), `temporal_fractalization` (o transporte), `the_light_squares_to_the_graviton` e `reading_post_is_born` (a operação quadrática). As ' + str(len(verb)) + ' inscrições de 24/10 estão embutidas por sha256 (`cunhagens_v399`) e a cobertura exata do Audit em `kh_n1_cobertura_v399`. '
            'A leitura das duas faces (a leitura do operador, o registro do `um.py`) é leitura da gerência [ONTO], a ratificar. O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n"'
            ' % (((core.get("selo_pela_propria_tecnologia_v399") or {}).get("controles_negativos") or {}).get("n_controles", "n/d"), ((core.get("selo_pela_propria_tecnologia_v399") or {}).get("controles_negativos") or {}).get("todos_recusados", "n/d"), ((core.get("declaracao_do_operador_v399") or {}).get("declaration") or {}).get("verbatim_sha256", "n/d")))')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA)
edit(A_M.end(), A_M.end(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «O testemunho de dois: o selo pela propria tecnologia (v399)».")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))
T = T0
for a, b, novo, *_ in sorted(EDITS, key=lambda e: -e[0]):
    T = T[:a] + novo + T[b:]
ast.parse(T)
tree = ast.parse(T)
assert T.count("\n") - T.count("\r\n") == T0.count("\n") - T0.count("\r\n"), "o patch introduziu quebra de linha LF (o arquivo e' CRLF): toda insercao tem de passar por crlf()"
NOVOS_NOMES = ("selo_acom_v399", "declaracao_do_operador_v399", "resumos_do_selo_v399", "selo_acom_sidecar_v399", "registro_core_v399", "sidecar", "selar", "verificar", "controles_negativos", "conferir_bloco_embutido", "ACOM_PROVENIENCIA",
               "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256", "_V399_FONTES", "_V399_VERBATINS2", "_V399_SPECS", "_V399_NOMES_REGISTROS", "_v399_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
# a secao nao redefine nenhum nome de nivel de modulo do um.py base (so' imports do mesmo modulo): C3 sobre o texto FINAL
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_def_base = {n for n in _nomes_base}
_colide = sorted(_nomes_rt & _def_base); assert set(_colide) <= {"hashlib", "math", "time", "np", "ALPHA_FINE_CODATA_2018"}, ("colisao de nomes (C3)", _colide)
# C1/C2/C9 sobre o bloco como ficou no TEXTO FINAL (CRLF -> LF)
_blk = AC.extrair_bloco(T)
_emb, _h_emb, _ = AC.bloco_das_fontes()
assert _blk == _emb and sha256(_blk.encode("utf-8")) == MONT["conferencias"]["C1_bloco_igual_ao_refeito_das_fontes"]["detalhe"]["sha256_refeito"], "o bloco embutido no candidato nao e' a copia refeita das fontes do operador (C1)"
assert not AC.literais_de_beta(RT), "literal de beta no runtime (C9)"
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V398_SPECS", tree).value) == specs398
for cname in ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT"):
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V399_REGERAR") == "1", "o candidato ja existe e difere: defina V399_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v398_sha16": SHA0, "escada": [E398, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS],
       "kernel": {"modulos_novos": N_NOVOS, "pedras": {s["rel"]: {"sha16": sha16(STONES_TXT[s["rel"]].encode()), "sha256": sha256(STONES_TXT[s["rel"]].encode()), "bandeiras": FJ["nomeadas_por_pedra"][s["key"]]} for s in DL.STONES},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v398_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v398_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": ["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E398, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v399.json (pos_build_kernel_v399.py)",
                                 "bandeiras_do_teorema": FJ["bandeira_do_teorema_incondicional"], "suporte": {s["key"]: dict(s["support"]) for s in DL.STONES}, "contrato": CONTR_TEST},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v398_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v398_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_da_composicao": N_AX,
       "acom": {"runtime_sha256": MONT["runtime"]["sha256"], "bloco_embutido_sha256": _h_emb, "conferencias_do_runtime": {k: v["ok"] for k, v in MONT["conferencias"].items()}, "colisoes_de_nomes_no_um_py": _colide,
                "edicoes_de_texto_declaradas": MONT["edicoes_declaradas"], "perfil": "ACOM-INT-C96-Q8", "decisoes": dict(DL.DECISOES), "declaracao": {"sha16": RG.S_DECL, "sha256": RG.DECL_SHA256, "bytes": len(RG.DECL_TEXTO.encode("utf-8"))}},
       "ponto_de_chamada": {"selo_pela_propria_tecnologia_v399": "main: IMEDIATAMENTE depois do bloco afinacao_das_cordas_v398", "declaracao_do_operador_v399": "main: IMEDIATAMENTE depois do bloco selo_pela_propria_tecnologia_v399", "specs": "main: depois do bloco [v398]",
                            "resumos_no_selo": "main: seal.update(resumos_do_selo_v399(core)) depois de seal['not_sealed_this_run']", "sidecar": "_unified_main: selo_acom_sidecar_v399() depois da ultima escrita do selo e antes do teste do selftest",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v399.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v399.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v399.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v399.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v399_pins.py"), "w", encoding="utf-8", newline="\n").write(RT)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v398_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v398:", PFORMAT_IDEMPOTENTE)
