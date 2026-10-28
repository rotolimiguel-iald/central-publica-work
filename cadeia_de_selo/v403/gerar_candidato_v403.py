# -*- coding: utf-8 -*-
"""gerar_candidato_v403.py -- gera o um.py CANDIDATO v403 a partir da v402 SELADA (base_v402; o Nos e' so' conferido, NUNCA escrito). PREPARACAO de 27/10/2026 (subagente de preparacao da gerencia c1; a gerencia revisa, ensaia, instala e sela). Molde: gerar_candidato_v402.py (a cadeia de CONTEUDO) com as licoes da v399 a v402.
Conteudo (enxuto: so' o que tem funcao -- ordem do operador de 22/10: nada de teste armado, nada de gordura):
 (A) kernel: +3 modulos (TGLExt/Caminho.lean, TGLExt/Vida.lean, TGLExt/VerdadeAdendo.lean: os nomes sao DO OPERADOR, 27/10/2026) + a RAIZ (os tres imports; o Audit nao muda: AUDIT_PREFIX vazio), conferidos byte a byte com o sandbox C:\\t\\k403c;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do gerador), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (tempo, quadratica, rede da v394, psibit da v395, testemunha da v396, sonico e afinacao da v398, a falsidade da inercia da v401 e os TRES da v402) sobem para a escada da v403 (so' o numero `expected_ladder`); o registro kh_n1_cobertura_v402 passa a piso (h2, h3, h6, h8) com errata;
 (F) F8.1 -- AS BANDEIRAS DO GATE: as TRES literais de prove_qg_closure_gate (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) passam a CALCULADAS, fail-closed (a familia ext_ls2_* do kernel; a checagem «pre-registro v67 INTACTO (hash)» do rito V11; o teste nulo cego, kwarg novo `blind_null`),
     a chamada passa `blind_null=void_stacking_blind`, uma sonda nova (ProbeBlindNullAbsent) e a nota GV-03 nos statuses do V11; as CHAVES dos dicionarios e a letra do veredito do gate NAO mudam. REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem);
 (D) runtime novo (runtime_v403.py): os QUATRO registros com funcao (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403), as DUAS falas de 27/10 embutidas por sha256 e os registros por spec cunhagens_v403 e kh_n1_cobertura_v403; chamadas no main (depois da esperanca_condicional_v402, e os specs depois dos da v402) e o resumo no selo;
 (E) a secao «Caminho, Verdade e Vida» PT/EN antes da secao v402 e a linha do .md. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md (regra do 4,44: este gerador nao o toca).
uso: python -I -B -X utf8 gerar_candidato_v403.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v403 as GP  # noqa: E402
import registros_v403 as RG  # noqa: E402
import delta_v403 as DL  # noqa: E402
import acom_conferencias_v403 as AC  # noqa: E402
import runtime_v403 as RT  # noqa: E402   (so' as funcoes puras de leitura do codigo do gate)
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP402 = json.load(open(os.path.join(DL.V402, "ESPERADOS_v402.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP402["candidato_sha16"]:   # o Nos ja nao e' a v402 (rito v403 em curso): a v402 SELADA vem da copia base_v402
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v402 selada"
SHA0 = sha16(raw); assert SHA0 == ESP402["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E402 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E402 == ESP402["escada"][1], (E402, ESP402["escada"])
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
    i = T0.index(old); edit(i, i + len(old), new, pid, grupo, o_que)


def linha_unica(rx):
    m_ = re.search(rx + r"[^\r\n]*\r\n", T0, re.M); assert m_ and T0.count(m_.group(0)) == 1, ("ANCORA NAO UNICA", rx)
    return m_


# ---------------- (1) o kernel ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v403.json"), encoding="utf-8"))["novos"]; assert nov == DL.STONE_RELS, "a lista dos modulos novos tem de ser so' as TRES pedras, na ordem do delta"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v402 + os tres imports das pedras na raiz (o Audit fica como esta)"
STONES_TXT = {}
for s in DL.STONES:
    STONES_TXT[s["rel"]] = rd(os.path.join(KB, *s["rel"].split("/")))
    assert STONES_TXT[s["rel"]] == rd(s["src"]) == rd(s["origem"]), "a pedra do sandbox difere da fonte (v403\\pedra, v403_kernel\\pedras): rode copiar_pedras_v403.py"
    assert s["rel"] not in old_d
    assert "sorry" not in re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", STONES_TXT[s["rel"]], flags=re.S)), "sorry no codigo da pedra " + s["name"]
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os tres imports das pedras; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (s["rel"], repr(STONES_TXT[s["rel"]]), CRLF) for s in DL.STONES), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +3 modulos Lean (Caminho, Vida, VerdadeAdendo), do sandbox.")
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(STONES_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v403.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v402"
assert all(DL.classe(n) == "nomeada" and m in DL.STONE_MODS for _, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada dos modulos das pedras"
assert all(s["theorem"] in {n for _, n, _ in FL} and s["key_theorem"] in {n for _, n, _ in FL} for s in DL.STONES), "a composicao e a estrela de cada pedra tem de ter bandeira"
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v403 (27/10/2026): as tres pedras Caminho (%d bandeira), Vida (%d) e VerdadeAdendo (%d) (os nomes sao do operador): %d bandeiras no total, SO' de declaracao NOMEADA (a pratica da v392 a v402; as %d auxiliares geradas pelo compilador ficam fora)"
     % (FJ["nomeadas_por_pedra"]["caminho"], FJ["nomeadas_por_pedra"]["vida"], FJ["nomeadas_por_pedra"]["verdade_adendo"], len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E402 and len(set(old_lad)) == E402
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v403: as tres pedras (%d, so' declaracao nomeada)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
edit(sbl, sbl, "    # v403 (27/10/2026): as tres pedras (os NOMES sao do operador): Caminho (a ponte da escala dual da v402 composta por citacao: a massa NAO e' selecionada pela lei e toda massa tem realizacao positiva), Vida (a queda sem geometria da v402 composta por citacao: o peso cai estritamente, o chao e' o posto, a entrega custa) "
     "e VerdadeAdendo (adendo da pedra Verdade da v392: a esperanca diagonal le a projecao da identidade como os seus pesos, preserva o Um, reler nao acrescenta)" + CRLF
     + "".join('    ("v403", "%s", "%s", None, None),%s' % (s["name"], s["rel"], CRLF) for s in DL.STONES), "V03_ledger", "G_KERNEL", "ledger de pedras: +3.")
m = re.search(r'^UM_VERSION = "v402"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v403"   # v403 (27/10/2026): a CONSTANTE UNICA de versao -- Caminho, Verdade e Vida (os nomes do operador): tres pedras (Caminho, Vida e o adendo da Verdade), os registros caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 (a F8.1: as tres bandeiras literais do gate passam a calculadas), '
           'as duas falas de 27/10 e as decisoes da gerencia; v402 em 26/10 (a ponte da escala dual, a queda sem geometria, a esperanca condicional); v401 em 25/10 (a falsidade (simulacro) da inercia); v400 em 24/10 (a correcao: o alfa unico); v399 (o testemunho de dois: o selo pela propria tecnologia)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v403'.")

# ---------------- (3) o que a v403 muda nos registros das versoes anteriores (so' dados) ----------------
CONTRATOS_DA_ESCADA = ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")
for cname in CONTRATOS_DA_ESCADA:
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E402
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V402_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E402, ESCADA_ESP))
vn = top("_V402_CONTRACTS").value; a, b = span(vn); seg = T0[a:b]
seg_novo, n_sub = re.subn(r"'expected_ladder': %d(?![0-9])" % E402, "'expected_ladder': %d" % ESCADA_ESP, seg)
assert n_sub == 3, ("_V402_CONTRACTS tem de trazer 3 'expected_ladder' (ponte, queda, esperanca)", n_sub)
edit(a, b, seg_novo, "C12__V402_CONTRACTS", "G_V402_PISOS", "_V402_CONTRACTS: expected_ladder %d -> %d nos tres contratos (o consumidor exige a igualdade exata com a escada do rito)." % (E402, ESCADA_ESP))
sv = top("_V402_SPECS"); spa, spb = span(sv.value)
seg_specs = T0[spa:spb]
specs402 = ast.literal_eval(sv.value)
PFORMAT_IDEMPOTENTE = (pprint.pformat(specs402, width=160, sort_dicts=False) == seg_specs.replace("\r\n", "\n"))
assert PFORMAT_IDEMPOTENTE, "o pformat dos specs v402 no um.py base nao e' idempotente: nao reescrevo o bloco"
khs = [s for s in specs402 if s["nome"] == "kh_n1_cobertura_v402"]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v403: piso historico (a cobertura cresce com os tres modulos novos); a igualdade exata esta em kh_n1_cobertura_v403"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v403: piso historico; a igualdade exata esta em kh_n1_cobertura_v403"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v403: a arvore ganha os arquivos das tres pedras, entao o registro da v402 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v403" % H8_ANTIGO_N
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v402 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v402 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v402 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v403 a cobertura cresce com os modulos Caminho, Vida e VerdadeAdendo e a arvore ganha os arquivos das pedras: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v403. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v402 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v403 quebra (a mesma lacuna que a v402 achou no registro da v401, a v401 no da v399 e a v399 no da v398)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k1["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec v402"
edit(spa, spb, pprint.pformat(specs402, width=160, sort_dicts=False).replace("\n", CRLF), "C13_kh_n1_v402_pisos", "G_V402_PISOS", "_V402_SPECS: kh_n1_cobertura_v402 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); o veredito nao muda.")

# ---------------- (F) F8.1 -- as TRES bandeiras literais do gate passam a CALCULADAS (fail-closed); as CHAVES dos dicionarios e a letra do veredito NAO mudam ----------------
# a familia ext_ls2_* de _LEAN_THEOREM_FLAGS == ls2_keys de prove_external_ladder (o termo dLs2): a fonte da bandeira linearized_spin2_finite_face
_ls2_ladder = [ast.literal_eval(n.value) for n in ast.walk(top("prove_external_ladder")) if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "ls2_keys"]
assert len(_ls2_ladder) == 1 and sorted(_ls2_ladder[0]) == sorted(k for k in old_flags if k.startswith(DL.F81_PREFIXO_LS2)) and len(_ls2_ladder[0]) == 6, "a familia ext_ls2_* difere de ls2_keys"
assert "kf99" in T0[T0.index("def prove_qg_closure_gate"):T0.index("def prove_certificate_II_concrete_network")]
F1_OLD = '    physics["linearized_spin2_finite_face"] = True   # v75 [KERNEL] informativo' + CRLF
F1_NEW = crlf('    _ls2_403 = [k_ for k_ in _LEAN_THEOREM_FLAGS if k_.startswith("ext_ls2_")]   # v403 (F8.1): a familia de bandeiras do kernel do termo dLs2 de prove_external_ladder (helice dupla, setor TT sem fantasma, 2 polarizacoes)\n'
              '    physics["linearized_spin2_finite_face"] = bool(len(_ls2_403) > 0 and all(kf99.get(k_) is True for k_ in _ls2_403))   # v75 [KERNEL] informativo; v403 (F8.1): CALCULADA do kernel (antes: literal True); familia vazia ou bandeira ausente/False => False (fail-closed)\n'
              '    _pre_403 = [c_[1] for c_ in ((independent_rite or {}).get("checks") or []) if isinstance(c_, (list, tuple)) and len(c_) == 2 and c_[0] == "pre-registro v67 INTACTO (hash)"]   # v403 (F8.1): a checagem do rito V11 (prereg_ok: hash recomputado == hash selado)\n'
              '    _blind_403 = lambda bn_: bool((bn_ or {}).get("all_verified") is True)   # v403 (F8.1): o teste nulo cego da v73 (centros aleatorios, dados reais): all_verified; ausente => False\n')
replace_unique(F1_OLD, F1_NEW, "F01_physics_ls2", "G_F81", "prove_qg_closure_gate: physics['linearized_spin2_finite_face'] literal -> calculada da familia ext_ls2_* do kernel (+ os auxiliares _pre_403 e _blind_403).")
replace_unique('        "protocol_pre_registered": True,          # v67 [hash]' + CRLF,
               '        "protocol_pre_registered": bool(len(_pre_403) == 1 and _pre_403[0] is True),   # v67 [hash]; v403 (F8.1): CALCULADA da checagem «pre-registro v67 INTACTO (hash)» do rito V11; ausente ou duplicada => False' + CRLF,
               "F02_protocol", "G_F81", "prove_qg_closure_gate: experiment['protocol_pre_registered'] literal -> calculada da checagem do rito V11.")
replace_unique('        "null_tests_passed_blind": True,          # v73 [dados reais]' + CRLF,
               '        "null_tests_passed_blind": _blind_403(blind_null),   # v73 [dados reais]; v403 (F8.1): CALCULADA do teste nulo cego (void_stacking_blind.all_verified); blind_null ausente => False' + CRLF,
               "F03_blind", "G_F81", "prove_qg_closure_gate: experiment['null_tests_passed_blind'] literal -> calculada do teste nulo cego.")
replace_unique("def prove_qg_closure_gate(ONE, kernel_formalization=None, independent_rite=None):" + CRLF, "def prove_qg_closure_gate(ONE, kernel_formalization=None, independent_rite=None, blind_null=None):" + CRLF, "F04_assinatura", "G_F81", "prove_qg_closure_gate: kwarg novo blind_null=None.")
CALL_OLD = "    qg_closure = prove_qg_closure_gate(ONE, kernel_formalization, independent_rite=void_floor_v11)  # v75/v134: O GATE DO FECHAMENTO (4 selos legitimos; flags novas; probes negativos); ADITIVO" + CRLF
CALL_NEW = "    qg_closure = prove_qg_closure_gate(ONE, kernel_formalization, independent_rite=void_floor_v11, blind_null=void_stacking_blind)  # v75/v134: O GATE DO FECHAMENTO (4 selos legitimos; flags novas; probes negativos); F8.1: o teste nulo cego da v73 alimenta null_tests_passed_blind; ADITIVO" + CRLF
assert "v403" not in CALL_NEW and "void_stacking_blind = prove_void_stacking_blind(" in T0[:T0.index(CALL_OLD)] and T0.index("void_stacking_blind = prove_void_stacking_blind(") < T0.index(CALL_OLD), "void_stacking_blind tem de estar definido ANTES da chamada, na mesma funcao (run_um)"
replace_unique(CALL_OLD, CALL_NEW, "F05_chamada", "G_F81", "run_um: a chamada de prove_qg_closure_gate passa blind_null=void_stacking_blind (sem o rotulo v403 na linha: o ensaio re-executa as instrucoes etiquetadas do main).")
replace_unique('    p3 = bool(probe_physics_without_math["verdict"] == "TGL_QG_CONDITIONAL_ARCHITECTURE_ONLY")' + CRLF,
               '    p3 = bool(probe_physics_without_math["verdict"] == "TGL_QG_CONDITIONAL_ARCHITECTURE_ONLY")' + CRLF
               + crlf('    p4 = bool(_blind_403(None) is False and evaluate_quantum_gravity_closure(formal, physics, dict(experiment, null_tests_passed_blind=_blind_403(None)))["verdict"] == gate["verdict"])   # v403 (F8.1): sem o teste nulo cego (blind_null ausente) a bandeira e\' False e o veredito do gate NAO muda (a bandeira e\' informativa: a literal nunca entrou no veredito)\n'),
               "F06_sonda", "G_F81", "prove_qg_closure_gate: a sonda nova p4 (blind_null ausente => bandeira False, veredito inalterado).")
replace_unique('        ("ProbePhysicsWithoutMath: fisica sem matematica => CONDITIONAL", p3),' + CRLF,
               '        ("ProbePhysicsWithoutMath: fisica sem matematica => CONDITIONAL", p3),' + CRLF
               + crlf('        ("ProbeBlindNullAbsent (F8.1, v403): sem o teste nulo cego (blind_null ausente) a bandeira informativa e\' False e o veredito do gate NAO muda", p4),\n'),
               "F07_check_da_sonda", "G_F81", "prove_qg_closure_gate: a checagem da sonda nova na lista de checks do gate.")
V11_ANC = '                            "(Euclid DR1 2027 / CMB-S4); os 4 flags so flipam com o veredito powered DESTE rito"),' + CRLF
replace_unique(V11_ANC, V11_ANC + crlf('            "gv03_nota_v403": ("as 4 bandeiras independent_v3_* que o gate le deste rito derivam de UM so\' booleano: o veredito do V11 ser NOT_FALSIFIED_POWERED (powered_emitted implica gates_ok, que implica split_ok e dist_ok); \'survey_mocks_passed\' = split-null e dist-check, SEM mock de survey [GV-03 da auditoria de 28/09/2026, DECLARADO]; "\n'
                                       '                               "os mocks de survey seguem [OPEN]; o gate nao se move"),\n'),
               "F08_gv03_nos_statuses_do_V11", "G_F81", "prove_void_floor_v11_sdss_independent: statuses ganha a nota GV-03 (as 4 experimentais derivam de um so' booleano).")

# ---------------- (4) main: chamadas e selo ----------------
A_FAL = linha_unica(r'^        print\("   \[v402\] AVISO: a esperanca condicional nao rodou: %r" % \(_e402c,\)\)')
BLOCO_N00 = r'''    try:   # v403: o CAMINHO (o nome que o operador deu a ponte da escala dual, 27/10/2026), lido no mesmo ponto das pedras anteriores (depois da esperanca condicional da v402): o kernel do proprio rito e o modelo longitudinal (E, p) com beta = alfa x raiz de e em runtime; excecao vira AVISO visivel, nunca derruba o rito
        _cam403 = caminho_v403(core)
        _cav403 = _cam403.get("values") or {}
        _nan403 = float("nan")
        print("CAMINHO [v403 -- o nome do operador para a ponte da escala dual (v402); [REAL] os termos do kernel e o calculo; [DERIVED] a massa NAO e' selecionada pela lei e toda massa tem realizacao positiva, m^2 = p+ p- e' o invariante e a energia e' a leitura; [ONTO] a leitura pela tripla espectral; [OPEN] H_BW, H_cal, H3, a assinatura e rank c = 4]:")
        print("  beta = alfa CODATA 2018 x sqrt(e) = %.15f (runtime) ; e^{-beta} = %.9f ; massas ao quadrado dos tres levantamentos com o mesmo p+ = %s ; energia minima da realizacao no nucleo = %.4f" % (_cav403.get("beta", _nan403), _cav403.get("pplus_factor_at_beta", _nan403), _cav403.get("lifts_same_pplus_masses"), _cav403.get("min_core_energy", _nan403)))
        print("  kernel: conjuncao (a pedra Caminho) = %s [%s] ; cabecalho da pedra no kernel embutido = %s" % ((_cam403.get("unconditional") or {}).get("in_kernel"), (_cam403.get("unconditional") or {}).get("flag"), (_cam403.get("context") or {}).get("ok")))
        print("  >>> %s <<<\n" % _cam403["verdict"])
    except Exception as _e403a:
        print("   [v403] AVISO: o caminho nao rodou: %r" % (_e403a,))
    try:   # v403: a VIDA (o nome que o operador deu a queda sem geometria), lida logo depois do Caminho; excecao vira AVISO visivel, nunca derruba o rito
        _vid403 = vida_v403(core)
        _viv403 = _vid403.get("values") or {}
        print("VIDA [v403 -- o nome do operador para a queda sem geometria (v402); o peso cai estritamente (nats = s), a seta e' o sinal de s, o chao e' o posto e nunca o zero, a entrega custa, o regime angular so' le; [ONTO] a leitura pela tripla espectral; [OPEN] a dimensao 3 e IsotropicPost no atlas curvo]:")
        print("  beta = %.15f (runtime) ; peso do posto depois da escala 1 = %.9f ; custo t.beta.g minimo = %.9f ; defasagem maxima = %.9f (< 1) ; perda por unidade 1 - e^{-beta} = %.12f" % (_viv403.get("beta", float("nan")), _viv403.get("post_weight_at_scale_one", float("nan")), _viv403.get("min_cost_t_beta_g", float("nan")), _viv403.get("max_dephasing_factor", float("nan")), _viv403.get("loss_per_unit", float("nan"))))
        print("  kernel: conjuncao (a pedra Vida) = %s [%s] ; cabecalho da pedra no kernel embutido = %s" % ((_vid403.get("unconditional") or {}).get("in_kernel"), (_vid403.get("unconditional") or {}).get("flag"), (_vid403.get("context") or {}).get("ok")))
        print("  >>> %s <<<\n" % _vid403["verdict"])
    except Exception as _e403b:
        print("   [v403] AVISO: a vida nao rodou: %r" % (_e403b,))
    try:   # v403: o ADENDO da VERDADE (a esperanca condicional lida pelo Nome; a pedra Verdade da v392 fica intacta), lido logo depois da Vida; excecao vira AVISO visivel, nunca derruba o rito
        _vad403 = verdade_adendo_v403(core)
        _vav403 = _vad403.get("values") or {}
        print("VERDADE (ADENDO) [v403 -- a esperanca condicional e' a Verdade lida pelo Nome; em M2(C) a esperanca diagonal le a projecao da identidade como os pesos q^2 e alfa^2, preserva o Um, reler nao acrescenta; [KNOWN] Umegaki, Tomiyama; [ONTO] a leitura pela tripla espectral; [OPEN] a instancia do contorno e o caso III1]:")
        print("  beta = %.15f (runtime) ; alfa = beta / sqrt(e) = %.15f ; pesos (1 - alfa^2, alfa^2) = (%.12f, %.6e) ; traco depois do Nome = %.1f" % (_vav403.get("beta", float("nan")), _vav403.get("alpha", float("nan")), _vav403.get("q_squared_at_alpha", float("nan")), _vav403.get("alpha_squared", float("nan")), _vav403.get("trace_after_name", float("nan"))))
        print("  kernel: composicao = %s [%s] ; estrela = %s [%s] ; cabecalho do adendo no kernel embutido = %s" % ((_vad403.get("unconditional") or {}).get("in_kernel"), (_vad403.get("unconditional") or {}).get("flag"), (_vad403.get("key_theorem") or {}).get("in_kernel"), (_vad403.get("key_theorem") or {}).get("flag"), (_vad403.get("context") or {}).get("ok")))
        print("  >>> %s <<<\n" % _vad403["verdict"])
    except Exception as _e403c:
        print("   [v403] AVISO: o adendo da verdade nao rodou: %r" % (_e403c,))
    try:   # v403: AS BANDEIRAS DO GATE (F8.1), lidas logo depois do adendo da Verdade: o gate do proprio rito e o codigo das duas funcoes do gate; se uma bandeira CALCULADA vier False o registro RECUSA (visivel); excecao vira AVISO visivel, nunca derruba o rito
        _bdg403 = bandeiras_do_gate_v403(core)
        _bgv403 = _bdg403.get("values") or {}
        print("BANDEIRAS DO GATE [v403 -- F8.1: as 18 bandeiras do gate sao calculadas (as tres que eram literais foram recalculadas das suas fontes); 15 entram no veredito (6+5+4); as 4 experimentais derivam de UM so' booleano (GV-03, declarado); a letra do veredito e' a da v402; [OPEN] a independencia das experimentais e os mocks de survey]:")
        print("  bandeiras = %s (%s True) ; calculadas = %s ; literais = %s ; lidas pelo veredito = %s ; letra do veredito == v402: %s ; checagens do gate = %s" % (_bgv403.get("n_flags"), _bgv403.get("n_true"), _bgv403.get("n_calculated"), _bgv403.get("n_literal"), _bgv403.get("read_by_the_verdict"), _bgv403.get("gate_verdict_equals_v402"), _bgv403.get("n_gate_checks")))
        print("  >>> %s <<<\n" % _bdg403["verdict"])
        if _bdg403.get("all_verified") is not True:
            print("   [v403] RECUSA: uma bandeira calculada do gate veio False ou uma checagem do registro falhou: o conferidor para o rito (fail-closed; resultado honesto, nao se mascara): %r" % ([c_["id"] for c_ in ((_bdg403.get("mechanics") or {}).get("checks") or []) if not c_["ok"]],))
    except Exception as _e403d:
        print("   [v403] AVISO: as bandeiras do gate nao rodaram: %r" % (_e403d,))
'''
edit(A_FAL.end(), A_FAL.end(), crlf(BLOCO_N00), "N00_main_quatro_registros", "G_RUNTIME", "main: caminho, vida, adendo da verdade e bandeiras do gate (try/AVISO cada), logo depois do bloco esperanca_condicional_v402.")
A_R = linha_unica(r'^        print\("   \[v402\] AVISO: os registros por spec da v402 nao rodaram')
BLOCO_N01 = r'''    try:   # v403: os registros por spec da v403 (as duas falas de 27/10 -- falas do operador --, os tres nomes, a leitura da tripla espectral, as decisoes, as erratas E5 e E6 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _n403 = _v403_rodar_specs(core)
        print("   [v403] o caminho, a vida, o adendo da verdade e as bandeiras do gate (lidos depois da esperanca condicional) e as falas de 27/10 (cunhagens_v403): caminho=%s | vida=%s | verdade_adendo=%s | bandeiras=%s | cunhagens=%s | registros por spec: %d (selados %d)" % ((core.get("caminho_v403") or {}).get("verdict"), (core.get("vida_v403") or {}).get("verdict"), (core.get("verdade_adendo_v403") or {}).get("verdict"), (core.get("bandeiras_do_gate_v403") or {}).get("verdict"), (core.get("cunhagens_v403") or {}).get("verdict"), len(_n403), sum(1 for k_ in _n403 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e403e:
        print("   [v403] AVISO: os registros por spec da v403 nao rodaram: %r" % (_e403e,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N01), "N01_main_specs", "G_RUNTIME", "main: registros por spec v403 (try/AVISO), depois do bloco v402.")
A_S = linha_unica(r'^ {12}"registros_v402": \{n_: ')
_k_pedra = '("verdict", "all_verified", "unconditional", "key_theorem", "context", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core")'
_sel = ['            "caminho_v403": {k_: (core.get("caminho_v403") or {}).get(k_) for k_ in %s},' % _k_pedra,
        '            "vida_v403": {k_: (core.get("vida_v403") or {}).get(k_) for k_ in %s},' % _k_pedra,
        '            "verdade_adendo_v403": {k_: (core.get("verdade_adendo_v403") or {}).get(k_) for k_ in %s},' % _k_pedra,
        '            "bandeiras_do_gate_v403": {k_: (core.get("bandeiras_do_gate_v403") or {}).get(k_) for k_ in ("verdict", "all_verified", "values", "runtime_executed", "scope", "does_not_gate_core")},',
        '            "registros_v403": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V403_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +caminho, vida, verdade_adendo, bandeiras_do_gate e registros_v403.")

# ---------------- (5) o bloco de runtime v403 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v403.json"), encoding="utf-8"))
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
CONTRS = {s["key"]: RG.contrato(s, FJ, FORMAL_MAP, E402, sha256(raw)) for s in DL.STONES}
assert all(c["expected_ladder"] == ESCADA_ESP for c in CONTRS.values())
CONTRS["gate"] = RG.bandeiras_do_gate_v403(T0, core0, selo0)    # RECUSA (RuntimeError) se uma bandeira calculada viria False no core da v402 selada, se as contagens nao fecham ou se a letra do veredito diverge
assert CONTRS["gate"]["gate_verdict_v402"] == selo0["qg_closure_verdict"] and CONTRS["gate"]["n_flags"] == 18 and CONTRS["gate"]["n_no_veredito"] == 15 and CONTRS["gate"]["decomposicao_do_veredito"] == [6, 5, 4]
TXTS = RG.textos()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
for s in DL.STONES:
    assert fontes[RG.CHAVE_DE_FONTE[s["key"]]]["sha256"] == FORMAL_MAP[s["rel"]], "a copia duravel da pedra difere da embutida: " + s["name"]
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v402, por ast)
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
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V403)
for k_, t_ in TXTS.items():
    assert not GP.violacoes(json.dumps(t_, ensure_ascii=False)) and not GUARDA.search(t_["veredito_ok"]), "P18 ou palavra recusada no texto do registro " + k_
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v403.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V403_CONTRACTS = " + pprint.pformat(CONTRS, width=150, sort_dicts=False) + "\n_V403_TEXTS = " + pprint.pformat(TXTS, width=150, sort_dicts=False)
         + "\n_V403_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V403_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "\n_V403_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V403_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V392_FONTES.update(_V403_FONTES)   # v403: o motor de registros (v392) le as fontes e os verbatins das onze versoes\n_V392_VERBATINS2.update(_V403_VERBATINS2)\n\n\n"
         "def _v403_rodar_specs(core_):\n"
         '    """v403 -- roda os registros por spec da v403 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Os registros caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 NAO entram aqui: rodam no main, depois da esperanca condicional."""\n'
         "    for spec_ in _V403_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V403_SPECS]\n')
HDR = ("# ====================== v403 (27/10/2026) -- CAMINHO, VERDADE E VIDA (os nomes do operador) E A F8.1: as tres pedras (Caminho, Vida e o adendo da Verdade; as pedras da v402 ficam como registro), os registros caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 (com FUNCAO, lidos no ponto do rito depois da esperanca condicional da v402), as duas falas de 27/10, as decisoes da gerencia e os registros por spec cunhagens_v403 e kh_n1_cobertura_v403.\n"
       "# As bandeiras do gate: as TRES literais passam a calculadas (a familia ext_ls2_* do kernel; a checagem «pre-registro v67 INTACTO (hash)» do rito V11; o teste nulo cego), fail-closed; a letra do veredito do gate e' a da v402. Os contratos (_V403_CONTRACTS) e as falas (_V403_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v403: os contratos (derivados do build e do AST do gate da v402), os textos, as fontes pinadas, as duas falas de 27/10 e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
A_P = linha_unica(r"^# ====================== v402 \(26/10/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v403", "G_RUNTIME", "bloco v403: os quatro registros com funcao, as duas falas de 27/10, as decisoes, as erratas E5-E6 e os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v403.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v403.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v403.py"); _controles([CONTRS, TXTS, specs, fontes], "contratos/specs/fontes")
PT2_FIRST = open(os.path.join(DL.V402, "artigo_pt_v402.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN2_FIRST = open(os.path.join(DL.V402, "artigo_en_v402.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT2_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT2_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: secao v403, antes da v402.")
replace_unique(EN2_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN2_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: secao v403, antes da v402.")
A_M = re.search(r'^    md\.append\("> \*\*A ponte da escala dual, a queda sem geometria e a esperança condicional \(v402, 26/10/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*A ponte da escala dual', T0, re.M)) == 1, "a linha da v402 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **Caminho, Verdade e Vida (v403, 27/10/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel (`TGLExt/Caminho`, `TGLExt/Vida`, `TGLExt/VerdadeAdendo`) com ' + str(len(FL)) + ' bandeiras só de declaração nomeada. Os nomes são do operador (27/10/2026): Caminho = a ponte da escala dual, Vida = a queda sem geometria, '
            'Verdade = a esperança condicional, como ADENDO da pedra `Verdade` da v392; «Verdade» sozinha para as três foi recusada (homônimo de `TGLExt.Verdade`), as pedras da v402 ficam como registro (pedra selada não se renomeia por cima) e o nome do triplo inteiro não foi dado. '
            'As pedras Caminho e Vida compõem por citação (`caminho_e_a_ponte_da_escala_dual`, `vida_e_a_queda_sem_geometria`); o adendo traz um teorema novo e pequeno: a esperança diagonal lê a projeção da identidade como os seus pesos, `diagExpect (identityProj a) = diag(q², α²)`, preserva o Um e reler não acrescenta. '
            'A leitura pela tripla espectral de Connes e por João 14,6 é [ONTO], não é termo de kernel. '
            'F8.1: as três bandeiras literais do gate (`linearized_spin2_finite_face`, `protocol_pre_registered`, `null_tests_passed_blind`) passam a calculadas, fail-closed: 18 de 18 calculadas, 15 no veredito (6+5+4), a letra do veredito do gate é a da v402; as 4 bandeiras experimentais derivam de um só booleano (declarado, não resolvido). '
            'Os registros `caminho_v403`, `vida_v403`, `verdade_adendo_v403` e `bandeiras_do_gate_v403` leem o kernel e o gate do rito e calculam, com β=α·√e em tempo de execução, um modelo de cada pedra. '
            'O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «Caminho, Verdade e Vida (v403)», antes da linha da v402.")

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
    """AJUSTE DO CONTROLE N10 (licao da v401): o controle negativo N10 (transposicao de 2 bytes) da secao do selo pela propria tecnologia (v399/v400, pinada, que a v403 NAO muda) so' existe SE os bytes nas posicoes n//2 e n//2 + 3 do objeto forem diferentes -- o um.py INTEIRO no conferidor e a AMOSTRA de 1 MiB no registro do core --
    (`if b[i] != b[j]`); o conferidor do rito exige os 13 controles sobre o um.py instalado inteiro (C8). Com o corpo da v403 a coincidencia dos bytes derrubaria o N10 (12 controles): o gerador acrescenta, se preciso, espacos ao FIM do comentario da linha UM_VERSION ate' os dois bytes diferirem."""
    bb = T_.encode("utf-8")

    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])   # o um.py INTEIRO (C8 do conferidor) e a AMOSTRA de 1 MiB (o registro do selo no core: registro_core_v399, amostra = 1 << 20)


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF): toda insercao tem de passar por crlf()"
NOVOS_NOMES = ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "v403_caminho_mechanics", "v403_vida_mechanics", "v403_verdade_adendo_mechanics", "_v403_close", "_v403_formal", "_v403_registro", "_V403_RECUSA", "_v403_fontes_do_gate", "_v403_ast_do_gate",
               "_V403_CONTRACTS", "_V403_TEXTS", "_V403_FONTES", "_V403_VERBATINS2", "_V403_SPECS", "_V403_NOMES_REGISTROS", "_v403_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
# o bloco nao redefine nenhum nome de nivel de modulo do um.py base (C3 sobre o texto FINAL): so' o import `math as _m403`
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V402_SPECS", tree).value) == specs402
for cname in CONTRATOS_DA_ESCADA:
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
assert all(c_["expected_ladder"] == ESCADA_ESP for c_ in ast.literal_eval(top("_V402_CONTRACTS", tree).value).values())
# F8.1 sobre o texto FINAL: nenhuma das 18 bandeiras e' atribuida por literal no chamador; o veredito le as mesmas 6+5+4; as assinaturas
_src_eval_f = ast.get_source_segment(T, top("evaluate_quantum_gravity_closure", tree)); _src_prove_f = ast.get_source_segment(T, top("prove_qg_closure_gate", tree))
_lidas_f, _lit_f = RT._v403_ast_do_gate(_src_eval_f, _src_prove_f)
assert _lit_f == [], ("ainda ha bandeira atribuida por literal no chamador do gate", _lit_f)
assert [len(_lidas_f[g]) for g in ("formal", "physics", "experiment")] == [6, 5, 4]
assert _src_eval_f == ast.get_source_segment(T0, top("evaluate_quantum_gravity_closure")), "a funcao do veredito (evaluate_quantum_gravity_closure) NAO pode mudar: o gate nao se move"
_sig_f = [a.arg for a in top("prove_qg_closure_gate", tree).args.args]
assert _sig_f == ["ONE", "kernel_formalization", "independent_rite", "blind_null"] and top("prove_qg_closure_gate", tree).args.defaults[-1].value is None
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado (licao da v400)
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v403" and float(a1_.group(1)) == 7.2973525693e-3
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V403_REGERAR") == "1", "o candidato ja existe e difere: defina V403_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v402_sha16": SHA0, "base_v402_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E402, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "pedras": {s["rel"]: {"sha16": sha16(STONES_TXT[s["rel"]].encode()), "sha256": sha256(STONES_TXT[s["rel"]].encode()), "bandeiras": FJ["nomeadas_por_pedra"][s["key"]]} for s in DL.STONES},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v402_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v402_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"]} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E402, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v403.json (pos_build_kernel_v403.py)",
                                 "bandeiras_do_teorema": FJ["bandeira_do_teorema_incondicional"], "suporte": {s["key"]: dict(s["support"]) for s in DL.STONES}, "contratos": CONTRS},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v402_entradas": H8_ANTIGO_N},
       "pformat_idempotente_v402_specs": PFORMAT_IDEMPOTENTE, "n_axiomas_da_composicao": N_AX,
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v402": g0, "candidato_v403": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "f81": {"literais_na_base": CONTRS["gate"]["literais_na_base_v402"], "literais_no_candidato": _lit_f, "lidas_pelo_veredito": {g: len(v) for g, v in _lidas_f.items()}, "fontes_avaliadas_no_core_v402": CONTRS["gate"]["fontes_avaliadas_no_core_v402"], "gate_verdict_v402": CONTRS["gate"]["gate_verdict_v402"],
               "funcao_do_veredito_identica_a_da_v402": True, "assinatura": _sig_f, "ls2_flags": CONTRS["gate"]["ls2_flags"], "ancoras": "cada ancora textual ocorre exatamente uma vez na base (replace_unique)"},
       "decisoes": dict(DL.DECISOES), "erratas_E5_E6": list(DL.ERRATAS_V403), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"caminho_vida_verdade_adendo_bandeiras_v403": "main: IMEDIATAMENTE depois do bloco esperanca_condicional_v402 (quatro instrucoes try, na ordem caminho, vida, adendo da verdade, bandeiras do gate)", "specs": "main: depois do bloco [v402]", "resumos_no_selo": "main: no dict do selo, depois de registros_v402 (os quatro registros com funcao e registros_v403)",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao", "gate": "run_um: prove_qg_closure_gate(..., blind_null=void_stacking_blind) (F8.1)"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v403"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v403.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v403.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v403.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v403_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v402_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS]); print("pformat idempotente nos specs v402:", PFORMAT_IDEMPOTENTE)
