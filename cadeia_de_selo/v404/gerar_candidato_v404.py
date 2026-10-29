# -*- coding: utf-8 -*-
"""gerar_candidato_v404.py -- gera o um.py CANDIDATO v404 a partir da v403 SELADA (base_v403; o Nos e' so' conferido, NUNCA escrito). PREPARACAO de 28/10/2026 (agente claude-prep-v404 para a gerencia c1; a gerencia revisa, ensaia, instala e sela). Molde: gerar_candidato_v403.py (a cadeia de CONTEUDO) com as licoes da v399 a v403.
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +2 modulos (TGLExt/ProjecaoTransversalDaMeiaNat.lean, de nome PROVISORIO da gerencia, e TGLExt/Jo8v32.lean, nome DO OPERADOR, 28/10/2026) + a RAIZ (os dois imports; o Audit nao muda: AUDIT_PREFIX vazio), conferidos byte a byte com o sandbox C:\\t\\k404c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do gerador), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395, testemunha da v396, sonico e afinacao da v398, a falsidade da inercia da v401, os TRES da v402 e os TRES de pedra da v403) sobem para a escada da v404 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v403 passa a piso (h2, h3, h6, h8) com errata;
 (D) runtime novo (runtime_v404.py): os TRES registros com funcao (projecao_transversal_v404, jo8v32_v404, f2b_errata_v404), as NOVE falas de 28/10 embutidas por sha256 e os registros por spec cunhagens_v404 e kh_n1_cobertura_v404; chamadas no main (depois do bandeiras_do_gate_v403, e os specs depois dos da v403) e o resumo no selo;
 (E) a secao «Jo 8,32 e a projecao transversal da Meia-Nat» PT/EN antes da secao v403 e a linha do .md; o artigo le o estado do CANAL F2b do registro novo (a linha do ramo B da tabela e a frase das contagens) -- a errata de F2b AO LADO; O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44: este gerador nao o toca).
 O gate NAO muda: as duas funcoes do gate (evaluate_quantum_gravity_closure e prove_qg_closure_gate) ficam BYTE A BYTE como na v403 (assertado). A funcao prove_neutrino_mass_gravitational NAO e' reescrita (a errata do angle_status e' AO LADO, no registro).
 REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -I -B -X utf8 gerar_candidato_v404.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v404 as GP  # noqa: E402
import registros_v404 as RG  # noqa: E402
import delta_v404 as DL  # noqa: E402
import acom_conferencias_v404 as AC  # noqa: E402
import runtime_v404 as RT  # noqa: E402   (so' as funcoes puras)
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP403 = json.load(open(os.path.join(DL.V403, "ESPERADOS_v403.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP403["candidato_sha16"]:   # o Nos ja nao e' a v403 (rito v404 em curso): a v403 SELADA vem da copia base_v403
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v403 selada"
SHA0 = sha16(raw); assert SHA0 == ESP403["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E403 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E403 == ESP403["escada"][1], (E403, ESP403["escada"])
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
    c = T0.count(old)
    assert c == n, ("ANCORA NAO UNICA (a regra dos patches: exatamente %d vez(es) na base; esta ocorre %d)" % (n, c), pid, old[:100])
    i = -1
    for k_ in range(n):
        i = T0.index(old, i + 1); edit(i, i + len(old), new, pid if n == 1 else "%s#%d" % (pid, k_ + 1), grupo, o_que)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T0, re.M); assert m_ and T0.count(m_.group(0)) == 1, ("ANCORA NAO UNICA", rx)
    return m_


# ---------------- (1) o kernel ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v404.json"), encoding="utf-8"))["novos"]; assert nov == DL.STONE_RELS, "a lista dos modulos novos tem de ser so' as DUAS pedras, na ordem do delta"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v403 + os dois imports das pedras na raiz (o Audit fica como esta)"
STONES_TXT = {}
for s in DL.STONES:
    STONES_TXT[s["rel"]] = rd(os.path.join(KB, *s["rel"].split("/")))
    assert STONES_TXT[s["rel"]] == rd(s["src"]) == rd(s["origem"]), "a pedra do sandbox difere da fonte (v404\\pedra, projecao_transversal_28out): rode copiar_pedras_v404.py"
    assert s["rel"] not in old_d
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONES_TXT[s["rel"]], flags=re.S)), "sorry no codigo da pedra " + s["name"]
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os dois imports das pedras; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (s["rel"], repr(STONES_TXT[s["rel"]]), CRLF) for s in DL.STONES), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +2 modulos Lean (ProjecaoTransversalDaMeiaNat, Jo8v32), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v404.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v403"
assert all(DL.classe(n) == "nomeada" and m in DL.STONE_MODS for _, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada dos modulos das pedras"
assert all(s["theorem"] in {n for _, n, _ in FL} and s["key_theorem"] in {n for _, n, _ in FL} for s in DL.STONES), "a composicao e a estrela de cada pedra tem de ter bandeira"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v404 (28/10/2026): as duas pedras ProjecaoTransversalDaMeiaNat (%d bandeiras) e Jo8v32 (%d) (a segunda tem o nome do operador): %d bandeiras no total, SO' de declaracao NOMEADA (a pratica da v392 a v403; as %d auxiliares geradas pelo compilador ficam fora)"
     % (FJ["nomeadas_por_pedra"]["projecao"], FJ["nomeadas_por_pedra"]["jo8v32"], len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E403 and len(set(old_lad)) == E403
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v404: as duas pedras (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v404 (28/10/2026): as duas pedras: ProjecaoTransversalDaMeiaNat (a Meia-Nat e' o angulo de 45 graus do neutrino, derivada no kernel; nome PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro) "
     "e Jo8v32 (o nome do operador para o triplo inteiro Caminho . Verdade . Vida: a conjuncao por citacao das tres estrelas da v403)" + CRLF
     + "".join('    ("v404", "%s", "%s", None, None),%s' % (s["name"], s["rel"], CRLF) for s in DL.STONES), "V03_ledger", "G_KERNEL", "ledger de pedras: +2.")
m = re.search(r'^UM_VERSION = "v403"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v404"   # v404 (28/10/2026): a CONSTANTE UNICA de versao -- Jo 8,32 e a projecao transversal da Meia-Nat: duas pedras (a Meia-Nat como o angulo de 45 graus do neutrino, derivada no kernel; Jo8v32, o nome do operador para o triplo inteiro), os registros projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404 (a cobranca F2b, o canal retirado antes do dado, AO LADO), '
           'as nove falas de 28/10 e as decisoes da gerencia; v403 em 27/10 (Caminho, Verdade e Vida; as bandeiras do gate calculadas); v402 em 26/10 (a ponte da escala dual, a queda sem geometria, a esperanca condicional); v401 em 25/10 (a falsidade (simulacro) da inercia); v400 em 24/10 (a correcao: o alfa unico); v399 (o testemunho de dois: o selo pela propria tecnologia)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v404'.")

# ---------------- (3) o que a v404 muda nos registros das versoes anteriores (so' dados) ----------------
CONTRATOS_DA_ESCADA = ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")
for cname in CONTRATOS_DA_ESCADA:
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E403
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V403_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E403, ESCADA_ESP))
for cname, n_esperado in (("_V402_CONTRACTS", 3), ("_V403_CONTRACTS", 3)):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    seg_novo, n_sub = re.subn(r"'expected_ladder': %d(?![0-9])" % E403, "'expected_ladder': %d" % ESCADA_ESP, seg)
    assert n_sub == n_esperado, ("%s tem de trazer %d 'expected_ladder' com a escada da v403" % (cname, n_esperado), n_sub)
    edit(a, b, seg_novo, "C12_" + cname, "G_V403_PISOS", "%s: expected_ladder %d -> %d nos %d contratos de pedra (o consumidor exige a igualdade exata com a escada do rito)." % (cname, E403, ESCADA_ESP, n_esperado))
sv = top("_V403_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs403 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs403, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
assert PFORMAT_IDEMPOTENTE, "o pformat dos specs v403 no um.py base nao e' idempotente: nao reescrevo o bloco"
khs = [s for s in specs403 if s["nome"] == "kh_n1_cobertura_v403"]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v404: piso historico (a cobertura cresce com os dois modulos novos); a igualdade exata esta em kh_n1_cobertura_v404"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v404: piso historico; a igualdade exata esta em kh_n1_cobertura_v404"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v404: a arvore ganha os arquivos das duas pedras, entao o registro da v403 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v404" % H8_ANTIGO_N
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v403 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v403 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v403 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v404 a cobertura cresce com os modulos ProjecaoTransversalDaMeiaNat e Jo8v32 e a arvore ganha os arquivos das pedras: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v404. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v403 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v404 quebra (a mesma lacuna que a v403 achou no registro da v402, a v402 no da v401 e a v401 no da v399)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k1["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v403"
edit(spa, spb, pprint.pformat(specs403, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v403_pisos", "G_V403_PISOS", "_V403_SPECS: kh_n1_cobertura_v403 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (G) o GATE nao se move: as duas funcoes ficam BYTE A BYTE como na base (assertado de novo sobre o texto FINAL, abaixo); a funcao do neutrino NAO e' reescrita ----------------
# ---------------- (F2b) o artigo le o estado do CANAL F2b do registro novo (a errata AO LADO); o V1 e o registro da v386 NAO sao tocados ----------------
A_RB = '    _rd3, _rs3, _rb3 = (core.get("ringdown_dephasing_result_v2") or {}), (core.get("ringdown_scope_v376") or {}), (core.get("ramo_b_preregistration_v386") or {})' + CRLF
replace_unique(A_RB, '    _rd3, _rs3, _rb3, _f2b4 = (core.get("ringdown_dephasing_result_v2") or {}), (core.get("ringdown_scope_v376") or {}), (core.get("ramo_b_preregistration_v386") or {}), (core.get("f2b_errata_v404") or {})   # v404: _f2b4 = a errata AO LADO da cobranca F2b (o V1 e o registro da v386 seguem como estavam)' + CRLF,
               "F2B01_atribuicao", "G_F2B", "artigo (PT e EN): _f2b4 le o registro f2b_errata_v404 ao lado de _rb3.", n=2)
replace_unique('--- F2b, ao lado", _st3s(_rb3.get("verdict"), "AWAITING_DATA", "AWAITING") + r" (F2b: " + _tx3s(_rb3.get("F2b_status")) + ")",' + CRLF,
               '--- F2b, ao lado", (_st3s(_rb3.get("verdict"), "AWAITING_DATA", "AWAITING") + r" (F2b: " + _tx3s(_rb3.get("F2b_status")) + ")") if _f2b4.get("all_verified") is not True else (r"V1 (v386, congelado por hash): " + _tk3s("AWAITING_DATA") + r"; canal F2b (v404, errata ao lado): " + _tk3s(_f2b4.get("F2b_status_now"))),' + CRLF,
               "F2B02_linha_PT", "G_F2B", "artigo PT: a linha do ramo B da tabela diz o estado do canal (retirado antes do dado) quando a errata selou; o V1 segue AWAITING_DATA.")
replace_unique('nada aberto: " + _tx3s(_rb3.get("nothing_opened")),' + CRLF + '         r"n/a (aguardando)", r"aguardando (v387)")' + CRLF,
               'nada aberto: " + _tx3s(_rb3.get("nothing_opened")),' + CRLF + '         (r"n/a (aguardando)" if _f2b4.get("all_verified") is not True else r"n/a (canal retirado antes do dado)"), (r"aguardando (v387)" if _f2b4.get("all_verified") is not True else r"retirado (v404, ao lado)"))' + CRLF,
               "F2B03_colunas_PT", "G_F2B", "artigo PT: as colunas RG? e discrimina? da linha do ramo B.")
replace_unique('--- F2b, beside", _st3s(_rb3.get("verdict"), "AWAITING_DATA", "AWAITING") + r" (F2b: " + _tx3s(_rb3.get("F2b_status")) + ")",' + CRLF,
               '--- F2b, beside", (_st3s(_rb3.get("verdict"), "AWAITING_DATA", "AWAITING") + r" (F2b: " + _tx3s(_rb3.get("F2b_status")) + ")") if _f2b4.get("all_verified") is not True else (r"V1 (v386, frozen by hash): " + _tk3s("AWAITING_DATA") + r"; channel F2b (v404, erratum beside): " + _tk3s(_f2b4.get("F2b_status_now"))),' + CRLF,
               "F2B04_linha_EN", "G_F2B", "artigo EN: a linha do ramo B da tabela.")
replace_unique('nothing opened: " + _tx3s(_rb3.get("nothing_opened")),' + CRLF + '         r"n/a (awaiting)", r"awaiting (v387)")' + CRLF,
               'nothing opened: " + _tx3s(_rb3.get("nothing_opened")),' + CRLF + '         (r"n/a (awaiting)" if _f2b4.get("all_verified") is not True else r"n/a (channel withdrawn before data)"), (r"awaiting (v387)" if _f2b4.get("all_verified") is not True else r"withdrawn (v404, beside)"))' + CRLF,
               "F2B05_colunas_EN", "G_F2B", "artigo EN: as colunas da linha do ramo B.")
replace_unique(r'a F2b (ramo B) entra ao lado como " + _tx3s(_rb3.get("F2b_status") or "n/d") + r". "',
               r'a F2b (ramo B) entra ao lado como " + (_tk3s(_f2b4.get("F2b_status_now")) + r" (v404: a errata de F2b esta ao lado; o V1 segue congelado por hash e a F2b nunca esteve entre as " + _i3s(len(_L3s)) + r" cobranças do livro)" if _f2b4.get("all_verified") is True else _tx3s(_rb3.get("F2b_status") or "n/d")) + r". "',
               "F2B06_contagens_PT", "G_F2B", "artigo PT: a frase das contagens diz o estado do canal.")
replace_unique(r'F2b (branch B) enters beside as " + _tx3s(_rb3.get("F2b_status") or "n/a") + r". "',
               r'F2b (branch B) enters beside as " + (_tk3s(_f2b4.get("F2b_status_now")) + r" (v404: the F2b erratum is beside; V1 stays frozen by hash and F2b was never among the " + _i3s(len(_L3s)) + r" charges of the ledger)" if _f2b4.get("all_verified") is True else _tx3s(_rb3.get("F2b_status") or "n/a")) + r". "',
               "F2B07_contagens_EN", "G_F2B", "artigo EN: a frase das contagens.")

# ---------------- (4) main: chamadas e selo ----------------
A_FAL = linha_unica(r'^        print\("   \[v403\] AVISO: as bandeiras do gate nao rodaram: %r" % \(_e403d,\)\)')
BLOCO_N00 = r'''    try:   # v404: a PROJECAO TRANSVERSAL DA MEIA-NAT (a pedra do sen 45 graus do neutrino; nome PROVISORIO da gerencia, aceito pelo operador ate' ele dar outro), lida no mesmo ponto das pedras anteriores (depois das bandeiras do gate da v403): o kernel do proprio rito e o calculo com beta = alfa x raiz de e em runtime; excecao vira AVISO visivel, nunca derruba o rito
        _prj404 = projecao_transversal_v404(core)
        _prv404 = _prj404.get("values") or {}
        _nan404 = float("nan")
        print("PROJECAO TRANSVERSAL DA MEIA-NAT [v404 -- a Meia-Nat e' o angulo de 45 graus do neutrino, derivado no kernel; [REAL] os teoremas e o calculo; [DERIVED] x = 1 - x => 1/2, sen^2(pi/4) = 1/2, sqrt x = sen(pi/4), a forma do neutrino = peso da reflexao x projecao transversal x o corpo; [ONTO] a massa e' a projecao transversal do estado inscrito (leitura do operador); [OPEN] E0 (1 eV declarado) e beta]:")
        print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime) ; sen(pi/4) = %.15f ; theta_M = %.9f rad ; m_nu do programa = %.9f meV (releitura beta.sen(pi/4).1 eV = %.9f)" % (_prv404.get("beta", _nan404), _prv404.get("sin_pi_over_4", _nan404), _prv404.get("theta_M", _nan404), _prv404.get("m_nu_meV_core") or _nan404, _prv404.get("m_nu_meV_runtime", _nan404)))
        print("  kernel: forma do neutrino (a pedra) = %s [%s] ; estrela do angulo = %s [%s] ; cabecalho da pedra no kernel embutido = %s" % ((_prj404.get("unconditional") or {}).get("in_kernel"), (_prj404.get("unconditional") or {}).get("flag"), (_prj404.get("key_theorem") or {}).get("in_kernel"), (_prj404.get("key_theorem") or {}).get("flag"), (_prj404.get("context") or {}).get("ok")))
        print("  >>> %s <<<\n" % _prj404["verdict"])
    except Exception as _e404a:
        print("   [v404] AVISO: a projecao transversal nao rodou: %r" % (_e404a,))
    try:   # v404: JO8v32 (o nome que o operador deu ao triplo inteiro Caminho . Verdade . Vida, 28/10/2026), lido logo depois da projecao transversal; excecao vira AVISO visivel, nunca derruba o rito
        _jo8404 = jo8v32_v404(core)
        _jov404 = _jo8404.get("values") or {}
        print("JO8v32 [v404 -- o nome do operador para o triplo inteiro; a conjuncao por citacao das tres estrelas da v403 (permanecer, conhecer, libertar); [REAL] os termos do kernel e a releitura da mecanica numerica dos tres registros da v403; [ONTO] a leitura por Jo 8,31-32; [OPEN] as hipoteses nomeadas dos componentes (IsotropicPost; hpp e hopt)]:")
        print("  beta = %.15f (runtime) ; checagens relidas da v403 = %s (passaram: %s) ; ordem do versiculo = %s" % (_jov404.get("beta", float("nan")), _jov404.get("v403_mechanics_checks"), _jov404.get("v403_mechanics_passed"), [x_.split(".")[-1] for x_ in (_jov404.get("order_of_the_verse") or [])]))
        print("  kernel: a conjuncao (a pedra Jo8v32) = %s [%s] ; cabecalho da pedra no kernel embutido = %s" % ((_jo8404.get("unconditional") or {}).get("in_kernel"), (_jo8404.get("unconditional") or {}).get("flag"), (_jo8404.get("context") or {}).get("ok")))
        print("  >>> %s <<<\n" % _jo8404["verdict"])
    except Exception as _e404b:
        print("   [v404] AVISO: o jo8v32 nao rodou: %r" % (_e404b,))
'''
edit(A_FAL.end(), A_FAL.end(), crlf(BLOCO_N00), "N00_main_projecao_jo8v32", "G_RUNTIME", "main: projecao transversal e jo8v32 (try/AVISO cada), logo depois do bloco bandeiras_do_gate_v403.")
A_F2B = linha_unica('^    ' + re.escape('print("   [v386] a errata ao lado de R6 e a cobranca F2b (o livro v383 intacto): %s" % core["ledger_errata_v386"]["verdict"])'))   # a ancora da errata de F2b: a ultima instrucao do bloco v386 (ramo B lido por hash + errata de R6)
BLOCO_N00B = r'''    try:   # v404: a ERRATA AO LADO da cobranca F2b (o canal do ramo B do ringdown retirado antes do dado), lida logo depois da errata ao lado de R6 da v386 (o V1 do ramo B, a errata da v386 e o livro da v383 ja' no core; licao da 1a tentativa do rito, 28/10/2026: chamada logo depois do Jo8v32 lia um core sem eles e recusava); o V1 (v386) e o registro ramo_b_preregistration_v386 NAO sao tocados; excecao vira AVISO visivel, nunca derruba o rito
        _f2b404 = f2b_errata_v404(core)
        _f2v404 = _f2b404.get("values") or {}
        print("ERRATA DE F2b [v404 -- o canal F2b (ramo B do ringdown) retirado antes do dado, AO LADO; o V1 segue congelado por hash e lido como antes; [REAL] a calibracao A (NOT_BLIND) e a previsao do par lidas do V1; [INPUT] a leitura do operador; nenhum desfecho; o conjunto D nao e' aberto]:")
        print("  calibracao A = %s [%s ; %s] ; previsao do par = %s ; fora do intervalo = %s ; cobrancas v383 = %s ; estado do canal = %s" % (_f2v404.get("calibracao_A_central"), _f2v404.get("calibracao_A_inferior"), _f2v404.get("calibracao_A_superior"), _f2v404.get("previsao_do_par"), _f2v404.get("previsao_fora_do_intervalo_de_A"), _f2v404.get("n_cobrancas_v383"), _f2b404.get("F2b_status_now")))
        print("  >>> %s <<<\n" % _f2b404["verdict"])
        if _f2b404.get("all_verified") is not True:
            print("   [v404] RECUSA: a errata de F2b nao selou (uma checagem falhou): o canal fica como antes e o conferidor para o rito (fail-closed; resultado honesto, nao se mascara): %r" % ([c_["id"] for c_ in ((_f2b404.get("mechanics") or {}).get("checks") or []) if not c_["ok"]],))
    except Exception as _e404c:
        print("   [v404] AVISO: a errata de F2b nao rodou: %r" % (_e404c,))
'''
edit(A_F2B.end(), A_F2B.end(), crlf(BLOCO_N00B), "N00b_main_errata_f2b", "G_RUNTIME", "main: a errata de F2b (try/AVISO), logo depois da errata ao lado de R6 da v386: o V1 do ramo B, a errata da v386 e o livro da v383 ja' estao no core (licao da 1a tentativa do rito, 28/10/2026).")
A_R = linha_unica(r'^        print\("   \[v403\] AVISO: os registros por spec da v403 nao rodaram')
BLOCO_N01 = r'''    try:   # v404: os registros por spec da v404 (as nove falas de 28/10 -- falas do operador --, os nomes, as leituras, as decisoes, as erratas E7 a E9 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _n404 = _v404_rodar_specs(core)
        print("   [v404] a projecao transversal, o jo8v32 e a errata de F2b (a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386) e as falas de 28/10 (cunhagens_v404): projecao=%s | jo8v32=%s | f2b=%s | cunhagens=%s | registros por spec: %d (selados %d)" % ((core.get("projecao_transversal_v404") or {}).get("verdict"), (core.get("jo8v32_v404") or {}).get("verdict"), (core.get("f2b_errata_v404") or {}).get("verdict"), (core.get("cunhagens_v404") or {}).get("verdict"), len(_n404), sum(1 for k_ in _n404 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e404d:
        print("   [v404] AVISO: os registros por spec da v404 nao rodaram: %r" % (_e404d,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N01), "N01_main_specs", "G_RUNTIME", "main: registros por spec v404 (try/AVISO), depois do bloco v403.")
A_S = linha_unica(r'^ {12}"registros_v403": \{n_: ')
_k_pedra = '("verdict", "all_verified", "unconditional", "key_theorem", "context", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core")'
_sel = ['            "projecao_transversal_v404": {k_: (core.get("projecao_transversal_v404") or {}).get(k_) for k_ in %s},' % _k_pedra,
        '            "jo8v32_v404": {k_: (core.get("jo8v32_v404") or {}).get(k_) for k_ in %s},' % _k_pedra,
        '            "f2b_errata_v404": {k_: (core.get("f2b_errata_v404") or {}).get(k_) for k_ in ("verdict", "all_verified", "F2b_status_now", "F2b_status_before", "values", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "registros_v404": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V404_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +projecao_transversal_v404, jo8v32_v404, f2b_errata_v404 e registros_v404.")

# ---------------- (5) o bloco de runtime v404 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v404.json"), encoding="utf-8"))
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
CONTRS = {s["key"]: RG.contrato(s, FJ, FORMAL_MAP, E403, sha256(raw), core0) for s in DL.STONES}
assert all(c["expected_ladder"] == ESCADA_ESP for c in CONTRS.values())
CONTRS["f2b"] = RG.contrato_f2b(core0)    # RECUSA (RuntimeError) se o V1 nao esta lido por hash no core da v403 selada, se algum pino nao bate ou se o livro v383 nao esta intacto
assert CONTRS["f2b"]["token_novo"] == DL.F2B_FUTURO_TOKEN and CONTRS["f2b"]["ledger_v383"]["n"] == 11
TXTS = RG.textos()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
for s in DL.STONES:
    assert fontes[RG.CHAVE_DE_FONTE[s["key"]]]["sha256"] == FORMAL_MAP[s["rel"]], "a copia duravel da pedra difere da embutida: " + s["name"]
assert fontes[RG.CHAVE_LEVANTAMENTO]["sha256"] == sha256(open(DL.LEVANTAMENTO_ARQ, "rb").read()), "a copia duravel do levantamento difere da fonte"
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v403, por ast)
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
specs = RG.especs(FORMAL_MAP, khj, H8, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], N_AX, core0)
spec_nomes = [s["nome"] for s in specs]
assert spec_nomes == [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]
_ax_antigos = core0["kernel_formalization"]["axiom_report"]
for s in specs:   # todo termo do kernel que o spec le tem de existir (no axiom_report da base ou nas bandeiras novas): senao o check nunca selaria
    for d_ in s.get("kernel_decls", []):
        assert d_ in _ax_antigos or d_ in axm, ("termo lido pelo spec ausente do kernel", s["nome"], d_)
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V404) == 9
for k_, t_ in TXTS.items():
    assert not GP.violacoes(json.dumps(t_, ensure_ascii=False)) and not GUARDA.search(t_["veredito_ok"]), "P18 ou palavra recusada no texto do registro " + k_
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v404.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V404_CONTRACTS = " + pprint.pformat(CONTRS, width=150, sort_dicts=False) + "\n_V404_TEXTS = " + pprint.pformat(TXTS, width=150, sort_dicts=False)
         + "\n_V404_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V404_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V404_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V404_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V404_FONTES)   # v404: o motor de registros (v392) le as fontes e os verbatins das doze versoes\n_V392_VERBATINS2.update(_V404_VERBATINS2)\n\n\n"
         "def _v404_rodar_specs(core_):\n"
         '    """v404 -- roda os registros por spec da v404 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Os registros projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404 NAO entram aqui: rodam no main, depois das bandeiras do gate."""\n'
         "    for spec_ in _V404_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V404_SPECS]\n')
HDR = ("# ====================== v404 (28/10/2026) -- JO 8,32 E A PROJECAO TRANSVERSAL DA MEIA-NAT: as duas pedras (a Meia-Nat como o angulo de 45 graus do neutrino, derivada no kernel; Jo8v32, o nome do operador para o triplo inteiro; as pedras da v403 ficam como estao), os registros projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404 (com FUNCAO, lidos no ponto do rito depois das bandeiras do gate da v403), as nove falas de 28/10, as decisoes da gerencia e os registros por spec cunhagens_v404 e kh_n1_cobertura_v404.\n"
       "# A errata do angulo do neutrino e a da cobranca F2b vao AO LADO (o texto antigo fica no registro; o V1 do ramo B segue congelado por hash). Os contratos (_V404_CONTRACTS) e as falas (_V404_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v404: os contratos (derivados do build e do core da v403 selada), os textos, as fontes pinadas, as nove falas de 28/10 e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v403 \(27/10/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v404", "G_RUNTIME", "bloco v404: os tres registros com funcao, as nove falas de 28/10, as decisoes, as erratas E7-E9 e os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v404.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v404.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v404.py"); _controles([CONTRS, TXTS, specs, fontes], "contratos/specs/fontes")
PT3_FIRST = open(os.path.join(DL.V403, "artigo_pt_v403.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN3_FIRST = open(os.path.join(DL.V403, "artigo_en_v403.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT3_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT3_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v404, antes da v403.")
replace_unique(EN3_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN3_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v404, antes da v403.")
A_M = re.search(r'^    md\.append\("> \*\*Caminho, Verdade e Vida \(v403, 27/10/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*Caminho, Verdade e Vida \(v403', T0, re.M)) == 1, "a linha da v403 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **Jo 8,32 e a projeção transversal da Meia-Nat (v404, 28/10/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel (`TGLExt/ProjecaoTransversalDaMeiaNat`, `TGLExt/Jo8v32`) com ' + str(len(FL)) + ' bandeiras só de declaração nomeada. A Meia-Nat é o ângulo de 45° do neutrino, derivada no kernel (nome provisório da gerência, aceito pelo operador até ele dar outro): '
            'x = 1 − x ⟹ ½, sen²(π/4) = ½, √x = sen(π/4) para todo x autoconjugado, e a forma do neutrino β·sen45°·E₀ = sen²θ_M·sen(π/4)·E₀. O sen45°, postulado desde 20/08/2026, passa a derivado, condicional à identificação [ONTO] de que a massa é a projeção transversal do estado inscrito (leitura do operador); E₀ = 1 eV segue declarado; a errata do `angle_status` vai ao lado e o texto antigo fica. '
            '`TGLExt/Jo8v32` é o nome do operador para o triplo inteiro Caminho · Verdade · Vida: a conjunção, por citação, das três estrelas da v403 (nenhuma matemática nova). '
            'A cobrança F2b (ramo B do ringdown) é retirada antes do dado, ao lado: o V1 segue congelado por hash e lido como antes; o motivo medido é a calibração A (NOT_BLIND); nenhum desfecho; o conjunto D não é aberto. '
            'Os registros `projecao_transversal_v404`, `jo8v32_v404` e `f2b_errata_v404` leem o kernel e o core do rito e calculam, com β=α·√e em tempo de execução. '
            'O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «Jo 8,32 e a projeção transversal da Meia-Nat (v404)», antes da linha da v403.")

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
    """AJUSTE DO CONTROLE N10 (licao da v401): o controle negativo N10 (transposicao de 2 bytes) da secao do selo pela propria tecnologia (v399/v400, pinada, que a v404 NAO muda) so' existe SE os bytes nas posicoes n//2 e n//2 + 3 do objeto forem diferentes -- o um.py INTEIRO no conferidor e a AMOSTRA de 1 MiB no registro do core --
    (`if b[i] != b[j]`); o conferidor do rito exige os 13 controles sobre o um.py instalado inteiro (C8). Com o corpo da v404 a coincidencia dos bytes derrubaria o N10 (12 controles): o gerador acrescenta, se preciso, espacos ao FIM do comentario da linha UM_VERSION ate' os dois bytes diferirem."""
    bb = T_.encode("utf-8")

    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])   # o um.py INTEIRO (C8 do conferidor) e a AMOSTRA de 1 MiB (o registro do selo no core: registro_core_v399, amostra = 1 << 20)


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF): toda insercao tem de passar por crlf()"
NOVOS_NOMES = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "v404_projecao_mechanics", "v404_jo8_mechanics", "v404_parse_deformacao", "_v404_close", "_v404_formal", "_v404_registro", "_V404_RECUSA",
               "_V404_CONTRACTS", "_V404_TEXTS", "_V404_FONTES", "_V404_VERBATINS2", "_V404_SPECS", "_V404_NOMES_REGISTROS", "_v404_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
# o bloco nao redefine nenhum nome de nivel de modulo do um.py base (C3 sobre o texto FINAL): so' o import `math as _m404`
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V403_SPECS", tree).value) == specs403
for cname in CONTRATOS_DA_ESCADA:
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
assert all(c_["expected_ladder"] == ESCADA_ESP for c_ in ast.literal_eval(top("_V402_CONTRACTS", tree).value).values())
assert [c_["expected_ladder"] for c_ in ast.literal_eval(top("_V403_CONTRACTS", tree).value).values()] == [ESCADA_ESP] * 3 + [None]
# O GATE NAO SE MOVE (sobre o texto FINAL): as duas funcoes ficam byte a byte como na base; a funcao do neutrino tambem (a errata do angulo e' AO LADO)
for fname in ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386"):
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao %s NAO pode mudar na v404" % fname
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado (licao da v400)
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(DL.V403, "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)   # o pino do esboco, lido do script da v403 (que o leu do arquivo), nunca digitado aqui
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v404" and float(a1_.group(1)) == 7.2973525693e-3
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V404_REGERAR") == "1", "o candidato ja existe e difere: defina V404_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v403_sha16": SHA0, "base_v403_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E403, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "pedras": {s["rel"]: {"sha16": sha16(STONES_TXT[s["rel"]].encode()), "sha256": sha256(STONES_TXT[s["rel"]].encode()), "bandeiras": FJ["nomeadas_por_pedra"][s["key"]]} for s in DL.STONES},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v403_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v403_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E403, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v404.json (pos_build_kernel_v404.py)",
                                 "bandeiras_do_teorema": FJ["bandeira_do_teorema_incondicional"], "suporte": {s["key"]: dict(s["support"]) for s in DL.STONES}, "contratos": CONTRS},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v403_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v403_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_da_composicao": N_AX,
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v403": g0, "candidato_v404": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "gate_nao_se_move": {"funcoes_identicas_a_base": ["evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386"], "gate_verdict_v403": selo0.get("qg_closure_verdict")},
       "decisoes": dict(DL.DECISOES), "erratas_E7_E9": list(DL.ERRATAS_V404), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"projecao_jo8_v404": "main: IMEDIATAMENTE depois do bloco bandeiras_do_gate_v403 (duas instrucoes try, na ordem projecao transversal, jo8v32)", "f2b_v404": "main: IMEDIATAMENTE depois da errata ao lado de R6 da v386 (uma instrucao try; ramo_b_preregistration_v386, ledger_errata_v386 e the_ledger_of_charges_v383 ja' atribuidos ao core; licao da 1a tentativa do rito, 28/10/2026)", "specs": "main: depois do bloco [v403]", "resumos_no_selo": "main: no dict do selo, depois de registros_v403 (os tres registros com funcao e registros_v404)",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao", "f2b_no_artigo": "a linha do ramo B da tabela e a frase das contagens leem core.f2b_errata_v404 (_f2b4) ao lado de ramo_b_preregistration_v386"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v404"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v404.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v404.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v404.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v404_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v403_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v403:", PFORMAT_IDEMPOTENTE)
