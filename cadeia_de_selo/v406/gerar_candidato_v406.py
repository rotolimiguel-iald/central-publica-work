# -*- coding: utf-8 -*-
"""gerar_candidato_v406.py -- gera o um.py CANDIDATO v406 a partir da v405 SELADA (base_v405; o Nos e' so' conferido, NUNCA escrito). Gerencia c1, 02/11/2026. Molde: gerar_candidato_v405.py (a cadeia de CONTEUDO) + gerar_candidato_v394.py (o modelo de BUNDLE).
Conteudo (O FECHAMENTO ENTRA NO um.py; ordem do operador de 02/11/2026: «construir tudo» e «compile a nova versão do um.py, rode, publique e atualize tudo por favor»):
 (A) kernel: +301 modulos em TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT, recompilados do fonte na integracao R3; e a candidata CanonicalFullTGLWitnessR1) + a RAIZ (os dois imports; o Audit nao muda), conferidos byte a byte com o sandbox C:\\t\\k406c e com o BUNDLE_v406.json;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do pos_build), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (os 11 da v394 a v404 e os OITO da v405) sobem para a escada da v406 (so' o numero `expected_ladder`); kh_n1_cobertura_v405 passa a piso (h2, h3, h6, h8) com errata; os specs que cobravam «falso» nas chaves de testemunha (u4 da v394; u3/u4 da v395; u3/u5 da v396; x_i do gap_v405) ganham a versao (errata E17);
 (D) as TRES funcoes que traziam o literal False (rede_fock_v394, psibit_v395, testemunha_estatica_v396) passam a LER o kernel por _v406_certificado_habitado (errata E14 AO LADO; o texto selado delas nao e' reescrito: so' o literal vira leitura e ganha errata);
 (E) runtime novo (runtime_v406.py): o registro com FUNCAO fechamento_v406, as falas de 02/11 embutidas por sha256 e os registros por spec cunhagens_v406 e kh_n1_cobertura_v406; chamadas no main DEPOIS do bloco v405; o resumo no selo;
 (F) a secao «O fechamento» PT/EN antes da secao v405 e a linha do .md; O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo (regra do 4,44: este gerador nao o toca).
 O gate NAO muda: as funcoes do gate/neutrino/ramo B ficam BYTE A BYTE como na v405 (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -I -B -X utf8 gerar_candidato_v406.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v406 as GP  # noqa: E402
import delta_v406 as DL  # noqa: E402
import registros_v406 as RG  # noqa: E402
import acom_conferencias_v406 as AC  # noqa: E402
import runtime_v406 as RT  # noqa: E402   (so' as funcoes puras)
import guarda_frases_v406 as GF  # noqa: E402   (a guarda de textos: as frases da v405 + as da v406)
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP405 = json.load(open(os.path.join(DL.V405, "ESPERADOS_v405.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP405["candidato_sha16"]:   # o Nos ja nao e' a v405 (rito v406 em curso): a v405 SELADA vem da copia base_v405
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v405 selada"
SHA0 = sha16(raw); assert SHA0 == ESP405["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E405 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E405 == ESP405["escada"][1], (E405, ESP405["escada"])
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


def _sem_comentarios_lean(t_):
    return re.sub(r"--[^\n]*", "", re.sub(r"/-.*?-/", "", t_, flags=re.S))


# ---------------- (1) o kernel: o BUNDLE de 301 ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v406.json"), encoding="utf-8"))["novos"]; assert nov == DL.BUNDLE_RELS, "a lista dos modulos novos tem de ser o bundle de 301, na ordem do preparo"
N_NOVOS = len(nov)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v405 + os dois imports do fecho na raiz (o Audit fica como esta)"
BUNDLE_TXT = {}
for rel in nov:
    t_ = rd(os.path.join(KB, *rel.split("/")))
    assert sha256(t_.encode("utf-8")) == DL.BUNDLE_POR_REL[rel]["sha256"], ("o modulo do sandbox difere do que o preparo do bundle pinou", rel)
    assert rel not in old_d, rel
    assert "sorry" not in _sem_comentarios_lean(t_), "sorry no codigo do modulo " + rel
    assert "#eval" not in _sem_comentarios_lean(t_), "#eval (instrumentacao da bancada) sobrou no modulo " + rel
    BUNDLE_TXT[rel] = t_
assert BUNDLE_TXT[DL.MODULO_TESTEMUNHA] == rd(DL.TESTEMUNHA["src"]) == rd(DL.TESTEMUNHA["origem"]), "a candidata do sandbox difere da fonte (v406\\pedra / fechamento_02nov)"
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os dois imports do fecho; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(BUNDLE_TXT[rel]), CRLF) for rel in nov), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean (o fecho: os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte; e a candidata CanonicalFullTGLWitnessR1), do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(BUNDLE_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v406.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v405"
assert all(DL.classe(n) == "nomeada" and m in DL.BUNDLE_MODS and k.startswith(DL.FLAG_PREFIX) for k, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada dos modulos do bundle, com o prefixo da v406"
_fl_nomes = {n for _, n, _ in FL}
for _an, _ad in DL.ANCORAS.items():
    assert FJ["ancoras"][_an]["rel"] == _ad["rel"] and set(FJ["ancoras"][_an]["axioms"]) <= TRIO and FJ["ancoras"][_an]["axioms"], ("ancora fora do esperado no FLAGS", _an)
    assert (FJ["ancoras"][_an]["flag"] is None) == (_an not in _fl_nomes), ("a bandeira da ancora e a lista de bandeiras discordam", _an)
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v406 (02/11/2026): O FECHAMENTO -- os %d modulos de TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte; e a candidata CanonicalFullTGLWitnessR1): %d bandeiras, SO' de declaracao NOMEADA (a politica da v394; as %d auxiliares geradas pelo compilador ficam fora)"
     % (N_NOVOS, len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E405 and len(set(old_lad)) == E405
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v406: o fechamento (%d, so' declaracao nomeada dos %d modulos do bundle)" % (len(FL), N_NOVOS) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
_nome_mod = lambda rel_: rel_.split("/")[-1][:-len(".lean")]
edit(sbl, sbl, "    # v406 (02/11/2026): O FECHAMENTO -- o bundle de %d modulos (a passagem para o continuo, o certificado de Fock habitado, a rede fisica, o termo canonico da testemunha)" % N_NOVOS + CRLF
     + "".join('    ("v406", "%s", "%s", None, None),%s' % (_nome_mod(rel), rel, CRLF) for rel in nov), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % N_NOVOS)
m = re.search(r'^UM_VERSION = "v405"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v406"   # v406 (02/11/2026): a CONSTANTE UNICA de versao -- O FECHAMENTO: os 301 modulos de TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT, recompilados do fonte na integracao R3, e a candidata CanonicalFullTGLWitnessR1); o certificado de Fock habitado por construcao (physicalFockCertificate) e a passagem para o continuo (modularCoreInput) lidos do kernel; '
           'as quatro chaves de testemunha deixam de ser literal; as falas do operador de 02/11; as ressalvas ditas; o gate nao se move; v405 em 01/11 (a massa derivada e a identidade definida); v404 em 28/10 (Jo 8,32 e a projecao transversal da Meia-Nat); v403 em 27/10 (Caminho, Verdade e Vida); v402 em 26/10; v401 em 25/10; v400 em 24/10; v399 (o testemunho de dois)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v406'.")

# ---------------- (3) o que a v406 muda nos registros das versoes anteriores (so' dados) ----------------
CONTRATOS_DA_ESCADA = ("_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V401_FALSIDADE_CONTRACT")
for cname in CONTRATOS_DA_ESCADA:
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    old = "'expected_ladder': %d" % E405
    assert seg.count(old) == 1 and not seg[seg.index(old) + len(old)].isdigit(), (cname, seg.count(old))
    edit(a, b, seg.replace(old, "'expected_ladder': %d" % ESCADA_ESP), "C12_" + cname, "G_V405_PISOS", "%s: expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (cname, E405, ESCADA_ESP))
for cname, n_esperado in (("_V402_CONTRACTS", 3), ("_V403_CONTRACTS", 3), ("_V404_CONTRACTS", 2), ("_V405_CONTRACTS", 8)):
    vn = top(cname).value; a, b = span(vn); seg = T0[a:b]
    seg_novo, n_sub = re.subn(r"'expected_ladder': %d(?![0-9])" % E405, "'expected_ladder': %d" % ESCADA_ESP, seg)
    assert n_sub == n_esperado, ("%s tem de trazer %d 'expected_ladder' com a escada da v405" % (cname, n_esperado), n_sub)
    edit(a, b, seg_novo, "C12_" + cname, "G_V405_PISOS", "%s: expected_ladder %d -> %d nos %d contratos de pedra (o consumidor exige a igualdade exata com a escada do rito)." % (cname, E405, ESCADA_ESP, n_esperado))


def _spec_block(nome_var):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    assert pprint.pformat(specs_, width=160, sort_dicts=False) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


def _versiona_check(spec_, id_, novo_op=None, novo_valor=None, nota_=""):
    """a checagem antiga fica como registro (descricao marcada «ate v405»); a vigente exige o estado lido do kernel (errata E17)."""
    cs_ = [c_ for c_ in spec_["checks"] if c_["id"] == id_]; assert len(cs_) == 1, (spec_["nome"], id_)
    c_ = cs_[0]
    antes_ = {"op": c_["op"], "valor": c_.get("valor")}
    if novo_op is not None:
        c_["op"] = novo_op
    if novo_valor is not None:
        c_["valor"] = novo_valor
    c_["descricao"] = "desde a v406 a chave e' LIDA do kernel do rito e a checagem exige o estado lido (%s%s)%s (errata E17, ao lado) -- ate' a v405 cobrava %s%s (o literal registrava o estado de entao); a descricao antiga, como registro: %s" % (c_["op"], (" " + repr(c_["valor"])) if c_.get("valor") is not None else "", nota_, antes_["op"], (" " + repr(antes_["valor"])) if antes_["valor"] is not None else "", c_["descricao"])
    return antes_


ERRATA_SPEC = lambda nome_, ids_: {"ao_lado_de": "%s (%s)" % (nome_, ", ".join(ids_)), "dizia": "a(s) chave(s) de testemunha cobrada(s) como falso / status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE: o literal da v394 a v405.",
                                   "agora": DL.ERRATA_E17, "lacuna_de_fidelidade": "um registro preso a um estado que a versao seguinte muda: o literal nao era leitura; desde 16/10/2026 a bancada tinha o habitante e a gerencia so' o leu em 02/11 (errata E14)",
                                   "estatuto": "[REAL: as ancoras no kernel do rito; conferido no ensaio a seco]", "assinatura": RG.ASSINA}
# _V394_SPECS: cunhagens_v394 u4
s4a, s4b, specs394 = _spec_block("_V394_SPECS")
c394 = [s for s in specs394 if s["nome"] == "cunhagens_v394"]; assert len(c394) == 1
_an = _versiona_check(c394[0], "u4", novo_op="verdadeiro"); assert _an == {"op": "falso", "valor": None}
c394[0].setdefault("erratas", []).append(ERRATA_SPEC("cunhagens_v394", ["u4"]))
edit(s4a, s4b, pprint.pformat(specs394, width=160, sort_dicts=False).replace("\n", CRLF), "C14_specs_v394_u4", "G_V405_PISOS", "_V394_SPECS: cunhagens_v394 u4 (whole_certificate_inhabited) falso -> verdadeiro (+ errata E17); o veredito nao muda de prefixo.")
# _V395_SPECS: cunhagens_v395 u3 (status) e u4 (inhabitant_exhibited)
s5a, s5b, specs395 = _spec_block("_V395_SPECS")
c395 = [s for s in specs395 if s["nome"] == "cunhagens_v395"]; assert len(c395) == 1
_an3 = _versiona_check(c395[0], "u3", novo_valor=DL.STATUS_HABITADO); assert _an3 == {"op": "igual", "valor": DL.STATUS_ANTIGO}
_an4 = _versiona_check(c395[0], "u4", novo_op="verdadeiro"); assert _an4 == {"op": "falso", "valor": None}
c395[0].setdefault("erratas", []).append(ERRATA_SPEC("cunhagens_v395", ["u3", "u4"]))
edit(s5a, s5b, pprint.pformat(specs395, width=160, sort_dicts=False).replace("\n", CRLF), "C15_specs_v395_u3_u4", "G_V405_PISOS", "_V395_SPECS: cunhagens_v395 u3 (status) -> INHABITED_BY_physicalFockCertificate_V406, u4 falso -> verdadeiro (+ errata E17).")
# _V396_SPECS: cunhagens_v396 u3 (status) e u5 (inhabitant_exhibited)
s6a, s6b, specs396 = _spec_block("_V396_SPECS")
c396 = [s for s in specs396 if s["nome"] == "cunhagens_v396"]; assert len(c396) == 1
_bn3 = _versiona_check(c396[0], "u3", novo_valor=DL.STATUS_HABITADO); assert _bn3 == {"op": "igual", "valor": DL.STATUS_ANTIGO}
_bn5 = _versiona_check(c396[0], "u5", novo_op="verdadeiro"); assert _bn5 == {"op": "falso", "valor": None}
c396[0].setdefault("erratas", []).append(ERRATA_SPEC("cunhagens_v396", ["u3", "u5"]))
edit(s6a, s6b, pprint.pformat(specs396, width=160, sort_dicts=False).replace("\n", CRLF), "C16_specs_v396_u3_u5", "G_V405_PISOS", "_V396_SPECS: cunhagens_v396 u3 (status) -> INHABITED_BY_physicalFockCertificate_V406, u5 falso -> verdadeiro (+ errata E17).")
# _V405_SPECS: kh_n1_cobertura_v405 -> pisos (h2/h3/h6/h8) e gap_v405 x_i -> verdadeiro
spa, spb, specs405 = _spec_block("_V405_SPECS")
khs = [s for s in specs405 if s["nome"] == "kh_n1_cobertura_v405"]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v406: piso historico (a cobertura cresce com os 301 modulos do fecho); a igualdade exata esta em kh_n1_cobertura_v406"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v406: piso historico; a igualdade exata esta em kh_n1_cobertura_v406"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v406: a arvore ganha os arquivos dos 301 modulos do fecho, entao o registro da v405 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v406" % H8_ANTIGO_N
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v405 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v405 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v405 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v406 a cobertura cresce com os 301 modulos do fecho e a arvore ganha os arquivos deles: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v406. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v405 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v406 quebra (a mesma lacuna desde a v399)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
gaps = [s for s in specs405 if s["nome"] == "gap_v405"]; assert len(gaps) == 1
_xi = _versiona_check(gaps[0], "x_i", novo_op="verdadeiro", nota_="; a instancia HminMic_e_o_lock segue CONDICIONAL por enunciado (o seu antecedente, o certificado, agora tem habitante no kernel: isso nao muda a pedra PontoZeroDoPsion nem o gap)"); assert _xi == {"op": "falso", "valor": None}
gaps[0].setdefault("erratas", []).append(ERRATA_SPEC("gap_v405", ["x_i"]))
assert not GP.violacoes(json.dumps([k1["erratas"][-1], gaps[0]["erratas"][-1], c394[0]["erratas"][-1]], ensure_ascii=False)), "P18 nas erratas novas dos specs"
edit(spa, spb, pprint.pformat(specs405, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v405_pisos_e_gap", "G_V405_PISOS", "_V405_SPECS: kh_n1_cobertura_v405 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); gap_v405 x_i falso -> verdadeiro (+ errata E17); os vereditos nao mudam.")

# ---------------- (G) as TRES funcoes que traziam o literal False: o literal vira LEITURA do kernel (errata E14 AO LADO); o texto selado nao e' reescrito ----------------
OLD_RF = ("        open_joint_contract=contract['open_joint_contract'],\r\n"
          "        whole_certificate_inhabited=False,\r\n"
          "        scope='Current compiled components on the same Fock; the remaining joint contract is explicit.',\r\n")
NEW_RF = ("        open_joint_contract=contract['open_joint_contract'],\r\n"
          "        whole_certificate_inhabited=_v406_certificado_habitado(report),   # v406: LIDA do kernel do rito (physicalFockCertificate no trio, no modulo do topo do fecho, fonte por sha256); ate' a v405 era o literal False (errata E14 AO LADO)\r\n"
          "        inhabited_by_v406=('F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate' if _v406_certificado_habitado(report) else None),\r\n"
          "        joint_contract_v406={'inhabited_by_the_physical_certificate': [x_ for x_ in contract['open_joint_contract'] if 'twenty-one' in x_] if _v406_certificado_habitado(report) else [], 'still_open': [x_ for x_ in contract['open_joint_contract'] if 'twenty-one' not in x_]},   # v406: o item habitado e' escolhido pelo CONTEUDO (o dos vinte e um campos), nao pela posicao; os outros tres seguem abertos\r\n"
          "        errata_v406='o literal False da v394 a v405 registrava o estado de entao (o kernel do um.py nao exibia habitante); desde 16/10/2026 a bancada do ChatGPT tinha physicalFockCertificate e a gerencia so o leu em 02/11; na v406 a chave e lida do kernel do proprio rito (errata E14, gerencia c1, em nome proprio)',\r\n"
          "        scope='Current compiled components on the same Fock; the remaining joint contract is explicit.',\r\n")
replace_unique(OLD_RF, NEW_RF, "C17_rede_fock_literal_vira_leitura", "G_CHAVES", "rede_fock_v394: whole_certificate_inhabited deixa de ser literal False e passa a _v406_certificado_habitado(report); +inhabited_by_v406, joint_contract_v406, errata_v406.")
OLD_RFV = ("    result['verdict'] = (\r\n"
           "        'TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CONTRACT_OPEN__GATE_UNMOVED'\r\n"
           "        if passed else\r\n")
NEW_RFV = ("    result['verdict'] = (   # v406: a TROCA DITA do veredito -- quando o certificado esta' habitado (lido do kernel) o nome diz JOINT_CERTIFICATE_INHABITED_V406; os tres itens restantes do contrato conjunto seguem abertos (joint_contract_v406)\r\n"
           "        'TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN__GATE_UNMOVED'\r\n"
           "        if (passed and result['whole_certificate_inhabited'] is True) else\r\n"
           "        'TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS__JOINT_CONTRACT_OPEN__GATE_UNMOVED'\r\n"
           "        if passed else\r\n")
replace_unique(OLD_RFV, NEW_RFV, "C17b_rede_fock_veredito", "G_CHAVES", "rede_fock_v394: o veredito ganha a variante JOINT_CERTIFICATE_INHABITED_V406 quando a chave lida e' True (troca dita).")
OLD_PB = ('    cond_.update({"status": "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE", "inhabitant_exhibited": False,\r\n'
          '                  "reading": "for every Fock certificate of the light the psion has norm one and is fixed by the light; the kernel exhibits no inhabitant of the certificate (TheImportedSecondQuantization, non-vacuity argued, no term); the statement does not show that the psion exists",\r\n'
          '                  "joint_contract_open_v394": bool((globals().get("_V394_NETWORK_CONTRACT") or {}).get("open_joint_contract"))})\r\n')
NEW_PB = ('    _hab406_ = _v406_certificado_habitado(kf_)   # v406: a face do psion LE o habitante do certificado no kernel do rito (physicalFockCertificate); ate\' a v405 o status e inhabitant_exhibited eram literais (errata E14 AO LADO); o texto da v395 fica como registro em reading_v395\r\n'
          '    cond_.update({"status": ("%s" if _hab406_ else "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"), "inhabitant_exhibited": bool(_hab406_),\r\n'
          '                  "reading_v395": "for every Fock certificate of the light the psion has norm one and is fixed by the light; the kernel exhibits no inhabitant of the certificate (TheImportedSecondQuantization, non-vacuity argued, no term); the statement does not show that the psion exists",\r\n'
          '                  "reading": ("for every Fock certificate of the light the psion has norm one and is fixed by the light; since v406 the kernel of the rite exhibits an inhabitant of the certificate (physicalFockCertificate, F1Fecho.CanonicalFockModularCoreInputR1, read from the axiom report and the provenance, not literal), so the statement applies to it; the identification with this stone\'s psionCorner still has no lemma" if _hab406_ else "for every Fock certificate of the light the psion has norm one and is fixed by the light; this rite reads no inhabitant of the certificate in its kernel"),\r\n'
          '                  "inhabited_by_v406": ("F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate" if _hab406_ else None), "errata_v406": "o literal False / CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE da v395 a v405 registrava o estado de entao; na v406 a chave e lida do kernel (errata E14, gerencia c1, em nome proprio)",\r\n'
          '                  "joint_contract_open_v394": bool((globals().get("_V394_NETWORK_CONTRACT") or {}).get("open_joint_contract")),   # v406: fica como na v395: o contrato conjunto SEGUE aberto em tres dos quatro itens (so\' o item dos vinte e um campos foi habitado; ver rede_fock_v394.joint_contract_v406)\r\n'
          '                  "joint_contract_items_still_open_v406": [x_ for x_ in ((globals().get("_V394_NETWORK_CONTRACT") or {}).get("open_joint_contract") or []) if "twenty-one" not in x_]})\r\n') % DL.STATUS_HABITADO
replace_unique(OLD_PB, NEW_PB, "C18_psibit_literal_vira_leitura", "G_CHAVES", "psibit_v395: inhabitant_exhibited e status deixam de ser literais e passam a leitura do kernel; reading_v395 guarda o texto antigo; +inhabited_by_v406, errata_v406.")
OLD_TE = ('    fock_ = {"theorem": fk_["theorem"], "declared_in": src_.get(fk_["theorem"]), "declared_outside_the_stone": fock_ok_, "status": "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE", "inhabitant_exhibited": False,\r\n'
          '             "linked_to_the_corner_by_a_lemma": False,\r\n'
          '             "reading": "the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; the kernel exhibits no inhabitant of the certificate and no lemma identifies psion C with the psionCorner of this stone"}\r\n')
NEW_TE = ('    _hab406t_ = _v406_certificado_habitado(kf_)   # v406: a face de Fock LE o habitante do certificado no kernel do rito; ate\' a v405 o status e inhabitant_exhibited eram literais (errata E14 AO LADO); linked_to_the_corner_by_a_lemma SEGUE False: nenhum lema liga psion C ao psionCorner\r\n'
          '    fock_ = {"theorem": fk_["theorem"], "declared_in": src_.get(fk_["theorem"]), "declared_outside_the_stone": fock_ok_, "status": ("%s" if _hab406t_ else "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"), "inhabitant_exhibited": bool(_hab406t_),\r\n'
          '             "linked_to_the_corner_by_a_lemma": False,\r\n'
          '             "reading_v396": "the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; the kernel exhibits no inhabitant of the certificate and no lemma identifies psion C with the psionCorner of this stone",\r\n'
          '             "reading": ("the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; since v406 the kernel of the rite exhibits an inhabitant of the certificate (physicalFockCertificate, read from the axiom report and the provenance, not literal); no lemma identifies psion C with the psionCorner of this stone" if _hab406t_ else "the Fock face of the psion is a statement for every Fock certificate; this rite reads no inhabitant of the certificate in its kernel; no lemma identifies psion C with the psionCorner of this stone"),\r\n'
          '             "inhabited_by_v406": ("F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate" if _hab406t_ else None), "errata_v406": "o literal False / CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE da v396 a v405 registrava o estado de entao; na v406 a chave e lida do kernel (errata E14, gerencia c1, em nome proprio)"}\r\n') % DL.STATUS_HABITADO
replace_unique(OLD_TE, NEW_TE, "C19_testemunha_literal_vira_leitura", "G_CHAVES", "testemunha_estatica_v396: inhabitant_exhibited e status deixam de ser literais e passam a leitura do kernel; reading_v396 guarda o texto antigo; linked_to_the_corner_by_a_lemma segue False; +errata_v406.")

# ---------------- (4) main: chamadas e selo ----------------
A_R = linha_unica(r'^        print\("   \[v405\] AVISO: os registros por spec da v405 nao rodaram')
BLOCO_N00 = r'''    try:   # v406: O FECHAMENTO -- o registro com FUNCAO fechamento_v406 (as oito ancoras, os 301 modulos por sha256, as quatro chaves de testemunha LIDAS do kernel, o que fica False por teorema, a escada, o gate) e os registros por spec da v406 (as falas de 02/11 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _r406 = fechamento_v406(core)
        _v406v = _r406.get("values") or {}
        print("O FECHAMENTO [v406 -- ordem do operador de 02/11/2026 («construir tudo»): o certificado de Fock habitado por construcao (physicalFockCertificate, bancada do ChatGPT 16/10, recompilado do fonte), a passagem para o continuo (modularCoreInput, para todo CanonicalNetInput) e o termo canonico da testemunha (canonicalFullTGLWitness) LIDOS do kernel deste rito; as quatro chaves de testemunha deixam de ser literal; [REAL] os termos e a leitura; [OPEN/KNOWN] K(O) != bot so' na cunha; [DECLARADO] R7 e a ratificacao; validade no kernel nao e' creditacao; o gate nao se move]:")
        print("  ancoras ok = %s/8 ; modulos do bundle ok = %s/%s ; bandeiras True = %s/%s ; certificado habitado (lido do kernel) = %s ; escada = %s ; gate = %s" % (_v406v.get("n_ancoras_ok"), _v406v.get("n_modulos_ok"), _v406v.get("n_modulos"), _v406v.get("n_flags_true"), _v406v.get("n_flags"), _r406.get("certificate_inhabited"), _v406v.get("escada"), "o mesmo da base" if any(c_.get("id") == "c14" and c_.get("ok") for c_ in ((_r406.get("mechanics") or {}).get("checks") or [])) else "DIFERE OU NAO LIDO"))
        print("  >>> %s <<<\n" % _r406["verdict"])
        _n406 = _v406_rodar_specs(core)
        print("   [v406] o fechamento e os registros por spec da v406: fechamento=%s | specs: %d (selados %d)" % ("SELOU" if _r406.get("all_verified") is True else "NAO", len(_n406), sum(1 for k_ in _n406 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e406:
        print("   [v406] AVISO: o fechamento ou os registros por spec da v406 nao rodaram: %r" % (_e406,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_fechamento", "G_RUNTIME", "main: fechamento_v406 (try/AVISO) e os registros por spec v406, logo depois do bloco v405 (rede_fock_v394, psibit_v395, testemunha_estatica_v396 e witness_layers ja' rodaram: as chaves que ele le ja' estao gravadas).")
A_S = linha_unica(r'^ {12}"registros_v405": \{n_: ')
_sel = ['            "fechamento_v406": {k_: (core.get("fechamento_v406") or {}).get(k_) for k_ in ("verdict", "all_verified", "certificate_inhabited", "inhabited_by", "canonical_full_witness_term", "four_keys", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core", "nome_provisorio_da_candidata")},',
        '            "registros_v406": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V406_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +fechamento_v406 (resumo) e registros_v406.")

# ---------------- (5) o bloco de runtime v406 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v406.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
for _an in DL.ANCORAS:
    assert _an in axm and set(axm[_an]) <= TRIO, ("ancora ausente do Audit do sandbox ou fora do trio", _an)
CONTR = RG.contrato(FJ, FORMAL_MAP, E405, sha256(raw), core0, selo0)
assert CONTR["expected_ladder"] == ESCADA_ESP
TXT = RG.texto_fecho()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
assert fontes[RG.CHAVE_TESTEMUNHA]["sha256"] == FORMAL_MAP[DL.MODULO_TESTEMUNHA], "a copia duravel da candidata difere da embutida"
for ch_, arq_ in ((RG.CHAVE_BUNDLE, DL.BUNDLE_ARQ), (RG.CHAVE_RATIFICACAO, DL.RATIFICACAO_ARQ), (RG.CHAVE_MANIFEST_INTEGRACAO, DL.MANIFEST_INTEGRACAO_ARQ), (RG.CHAVE_RECEIPT_BANCADA, DL.RECEIPT_BANCADA_ARQ), (RG.CHAVE_FASE9, DL.FASE9_V2_ARQ)):
    assert fontes[ch_]["sha256"] == sha256(open(arq_, "rb").read()), ("a copia duravel difere da fonte", ch_)
assert fontes[RG.CHAVE_FASE9]["sha256"][:16] == DL.FASE9_V2_SHA16_DA_ORDEM
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V406) and set(CONTR["verbatins"]) <= set(verb)
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v405, por ast)
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
specs = RG.especs(FORMAL_MAP, khj, H8, FJ, core0["kernel_formalization"]["axiom_coverage_v392"], core0)
spec_nomes = [s["nome"] for s in specs]
assert spec_nomes == [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]
_ax_antigos = core0["kernel_formalization"]["axiom_report"]
for s in specs:   # todo termo do kernel que o spec le tem de existir (no axiom_report da base ou no Audit do sandbox): senao o check nunca selaria
    for d_ in s.get("kernel_decls", []):
        assert d_ in _ax_antigos or d_ in axm, ("termo lido pelo spec ausente do kernel", s["nome"], d_)
    for f_ in s.get("kernel_flags", []):
        assert f_ in {k for k, _, _ in FL}, ("bandeira lida pelo spec ausente", s["nome"], f_)
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert not GP.violacoes(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT["veredito_ok"]), "P18 ou palavra recusada no texto do registro do fechamento"
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v406.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V406_FECHO_CONTRACT = " + pprint.pformat(CONTR, width=150, sort_dicts=False) + "\n_V406_FECHO_TEXT = " + pprint.pformat(TXT, width=150, sort_dicts=False)
         + "\n_V406_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V406_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True)
         + "\n_V406_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V406_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V406_REGISTROS_FUNCAO = " + repr(list(DL.REGISTROS_FUNCAO)) + "\n_V392_FONTES.update(_V406_FONTES)   # v406: o motor de registros (v392) le as fontes e os verbatins das catorze versoes\n_V392_VERBATINS2.update(_V406_VERBATINS2)\n\n\n"
         "def _v406_rodar_specs(core_):\n"
         '    """v406 -- roda os registros por spec da v406 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro com funcao (fechamento_v406) NAO entra aqui: roda no main, antes destes."""\n'
         "    for spec_ in _V406_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V406_SPECS]\n')
HDR = ("# ====================== v406 (02/11/2026) -- O FECHAMENTO ENTRA NO um.py: os 301 modulos de TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte na integracao R3; e a candidata CanonicalFullTGLWitnessR1), o registro com FUNCAO fechamento_v406 (as oito ancoras, os 301 sha256, as quatro chaves de testemunha LIDAS do kernel), as falas do operador de 02/11 e os registros por spec cunhagens_v406 e kh_n1_cobertura_v406.\n"
       "# As erratas E14 a E17 vao AO LADO (os literais das versoes anteriores ficam como registro: reading_v395, reading_v396, os specs marcados «ate' a v405»); as ressalvas da ratificacao R10 vao ditas; o contrato (_V406_FECHO_CONTRACT) e as falas (_V406_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. Validade no kernel nao e' creditacao. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v406: o contrato (derivado do build do sandbox k406c e do core da v405 selada), o texto do registro, as fontes pinadas, as falas de 02/11 e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
# A GUARDA DAS FRASES: nada do texto novo da gerencia afirma demais; ficam fora so' as falas embutidas e o proprio corpo das regras (as regexes)
G0_ = GF.controle_negativo(); assert G0_["ok"], ("o controle negativo da guarda das frases falhou", {k_: v_ for k_, v_ in G0_.items() if k_ != "ok"})
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v406_guarda_frases(txt_):"):RUNTIME_SRC.index("def _v406_certificado_habitado(kf_):")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTR, TXT, specs, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00 + NEW_RF + NEW_RFV + NEW_PB + NEW_TE
V_GF = GF.violacoes(_txt_ger); assert not V_GF, ("FRASE PROIBIDA no texto novo da gerencia (guarda_frases_v406)", V_GF[:4])
A_P = linha_unica(r"^# ====================== v405 \(01/11/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v406", "G_RUNTIME", "bloco v406: a guarda das frases, a leitura do certificado, o registro do fechamento, o contrato, as falas, os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v406.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v406.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]; assert not GF.violacoes(sn), GF.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v406.py"); _controles([CONTR, TXT, specs, fontes], "contrato/texto/specs/fontes")
PT5_FIRST = open(os.path.join(DL.V405, "artigo_pt_v405.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN5_FIRST = open(os.path.join(DL.V405, "artigo_en_v405.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT5_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT5_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: a secao v406 («O fechamento»), antes da v405.")
replace_unique(EN5_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN5_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: a secao v406, antes da v405.")
A_M = re.search(r'^    md\.append\("> \*\*A massa derivada e a identidade definida \(v405, 01/11/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*A massa derivada e a identidade definida \(v405', T0, re.M)) == 1, "a linha da v405 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **O fechamento (v406, 02/11/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel em `TGLExt/F1Fecho394` (os 300 da bancada do ChatGPT, missão F1.FECHO_20261015, recompilados do fonte na integração R3; e a candidata `CanonicalFullTGLWitnessR1`, nome provisório da gerência), com ' + str(len(FL)) + ' bandeiras só de declaração nomeada. '
            '[REAL] O topo do fecho (`CanonicalFockModularCoreInputR1`) habita, para todo `D : CanonicalNetInput`, os 21 campos de `RemainingModularCoreInput D` (a passagem para o contínuo: o traço cíclico, P_F com traço 1 pela calibração dual, as metades iguais) e, sobre a rede física `physicalCanonicalNet`, o certificado `physicalFockCertificate`; a candidata monta o termo canônico `canonicalFullTGLWitness : FullTGLWitness`. '
            'As quatro chaves de testemunha (três literais `False` desde a v394, `whole_certificate_inhabited` e as duas `inhabitant_exhibited`; e uma medida, `canonical_full_witness_term_constructed`, nome ausente ⇒ `False` desde a v367) passam a ser lidas do kernel do próprio rito, com errata E14 ao lado; o que fica `False` fica por teorema (`full_static_witness_exists`, `trivial_inhabitant_exists`) e o lema que liga `psion C` ao `psionCorner` segue faltando. Onde as seções v395, v396 e v405 deste documento e os registros selados dessas versões dizem, no presente, que o kernel não habita o certificado, leia-se: era o estado da data; a leitura vigente é esta; os textos ficam como registro. '
            'Ressalvas ditas: K(O) ≠ ⊥ só na cunha; «núcleo II∞» [KNOWN/DECLARADO]; o traço é ENNReal e cíclico, não linear; R7 foi Codex revisando Codex, a revisão distinta é do Sonnet; a integração removeu ' + str(DL.N_EVAL_BLOCOS) + ' blocos `#eval` de instrumentação (`IO.println`, `IO.FS.withFile`) em ' + str(DL.N_EVAL_MODULOS) + ' módulos, nenhum em prova; o cabeçalho dos módulos da bancada é da data da escrita (rótulo `UNCOMPILED CANDIDATE`), a compilação é a do recibo de 16/10, da integração R3 e do sandbox; R4/R5 ficam fora. O registro `fechamento_v406` lê as oito âncoras, os 301 sha256, as quatro chaves, a escada e o gate a cada rito. '
            'A ordem do operador (02/11/2026): «construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento»; a prioridade: «a construção da passagem para o contínuo é o que mais importa». '
            'O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA) and not GF.violacoes(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «O fechamento (v406)», antes da linha da v405.")

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
    """AJUSTE DO CONTROLE N10 (licao da v401): o controle negativo N10 (transposicao de 2 bytes) da secao do selo pela propria tecnologia so' existe SE os bytes nas posicoes n//2 e n//2 + 3 do objeto forem diferentes -- o um.py INTEIRO e a AMOSTRA de 1 MiB; o gerador acrescenta, se preciso, espacos ao FIM do comentario da linha UM_VERSION ate' os dois bytes diferirem."""
    bb = T_.encode("utf-8")

    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF): toda insercao tem de passar por crlf()"
NOVOS_NOMES = ("_v406_guarda_frases", "_v406_certificado_habitado", "_v406_chaves", "v406_fechamento_mechanics", "_v406_formal", "_V406_RECUSA", "fechamento_v406", "_V406_FECHO_CONTRACT", "_V406_FECHO_TEXT", "_V406_FONTES", "_V406_VERBATINS2", "_V406_SPECS", "_V406_NOMES_REGISTROS", "_V406_REGISTROS_FUNCAO", "_v406_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V405_SPECS", tree).value) == specs405 and ast.literal_eval(top("_V394_SPECS", tree).value) == specs394 and ast.literal_eval(top("_V395_SPECS", tree).value) == specs395 and ast.literal_eval(top("_V396_SPECS", tree).value) == specs396
for cname in CONTRATOS_DA_ESCADA:
    assert ast.literal_eval(top(cname, tree).value)["expected_ladder"] == ESCADA_ESP, cname
assert all(c_["expected_ladder"] == ESCADA_ESP for c_ in ast.literal_eval(top("_V402_CONTRACTS", tree).value).values())
assert [c_["expected_ladder"] for c_ in ast.literal_eval(top("_V403_CONTRACTS", tree).value).values()] == [ESCADA_ESP] * 3 + [None]
assert [c_["expected_ladder"] for c_ in ast.literal_eval(top("_V404_CONTRACTS", tree).value).values()] == [ESCADA_ESP] * 2 + [None]
assert [c_["expected_ladder"] for c_ in ast.literal_eval(top("_V405_CONTRACTS", tree).value).values()] == [ESCADA_ESP] * 8
# as tres funcoes das chaves: so' o literal virou leitura (o resto do corpo e' o da base) -- medido por diff de linhas
import difflib
for fname, esperado_add in (("rede_fock_v394", 7), ("psibit_v395", 5), ("testemunha_estatica_v396", 5)):
    s0 = ast.get_source_segment(T0, top(fname)).splitlines(); s1 = ast.get_source_segment(T, top(fname, tree)).splitlines()
    dif = [l_ for l_ in difflib.unified_diff(s0, s1, lineterm="", n=0) if l_[:1] in "+-" and not l_.startswith(("+++", "---"))]
    rem = [l_[1:] for l_ in dif if l_.startswith("-")]; add = [l_[1:] for l_ in dif if l_.startswith("+")]
    _old_lines = set((OLD_RF + OLD_RFV + OLD_PB + OLD_TE).replace("\r\n", "\n").split("\n")); _new_lines = set((NEW_RF + NEW_RFV + NEW_PB + NEW_TE).replace("\r\n", "\n").split("\n"))
    assert set(add) <= (_new_lines - _old_lines) and set(rem) <= (_old_lines - _new_lines), (fname, [l_ for l_ in add if l_ not in _new_lines][:2], [l_ for l_ in rem if l_ not in _old_lines][:2])   # so' as linhas dos patches C17-C19 mudam nessas funcoes
    assert len(rem) <= 4 and "_v406_certificado_habitado" in "\n".join(s1) and "_v406_certificado_habitado" not in "\n".join(s0), (fname, len(rem))
# O GATE NAO SE MOVE (sobre o texto FINAL)
for fname in DL.FUNCOES_INTOCADAS:
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao %s NAO pode mudar na v406" % fname
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(DL.V404 if False else os.path.join(os.path.dirname(HERE), "v403"), "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)   # o pino do esboco, lido do script da v403 (que o leu do arquivo), nunca digitado aqui
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v406" and float(a1_.group(1)) == ALPHA_BASE
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V406_REGERAR") == "1", "o candidato ja existe e difere: defina V406_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v405_sha16": SHA0, "base_v405_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E405, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "modelo": "bundle (v394)", "bundle": {rel: {"sha16": sha16(BUNDLE_TXT[rel].encode()), "sha256": sha256(BUNDLE_TXT[rel].encode()), "bandeiras": FJ["n_por_modulo"].get(rel, 0), "fonte_bancada": DL.BUNDLE_POR_REL[rel]["fonte_bancada"]} for rel in nov},
                  "topo": DL.MODULO_TOPO, "rede": DL.MODULO_REDE, "candidata": DL.MODULO_TESTEMUNHA, "ancoras": {n_: FJ["ancoras"][n_] for n_ in DL.ANCORAS},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v405_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v405_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"], "nome": os.path.basename(v_["fonte_original"])} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "guarda_frases": {"controle_negativo": bool(G0_["ok"]), "n_proibidas_reprovadas": sum(1 for v_ in G0_["proibidas"].values() if v_), "violacoes_no_texto_novo": len(V_GF)},
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E405, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v406.json (pos_build_kernel_v406.py)", "prefixo": DL.FLAG_PREFIX, "contrato": CONTR},
       "chaves_v406": [dict(c) for c in DL.CHAVES_V406], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "troca_dita_v406": ["rede_fock_v394"],
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v405_entradas": H8_ANTIGO_N},
       "pformat_idempotente_specs": True, "n_axiomas_das_ancoras": {n_: len(axm[n_]) for n_ in DL.ANCORAS},
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v405": g0, "candidato_v406": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "gate_nao_se_move": {"funcoes_identicas_a_base": list(DL.FUNCOES_INTOCADAS), "gate_verdict_v405": selo0.get("qg_closure_verdict")},
       "decisoes": dict(DL.DECISOES), "erratas_E14_E17": list(DL.ERRATAS_V406), "ressalvas": list(DL.RESSALVAS_V406), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"fechamento_v406": "main: IMEDIATAMENTE depois do bloco dos registros por spec da v405 (rede_fock_v394, psibit_v395, testemunha_estatica_v396 e witness_layers ja' gravados)", "specs": "main: no mesmo try, depois do fechamento_v406", "resumos_no_selo": "main: no dict do selo, depois de registros_v405",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v406"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v406.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v406.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v406.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v406.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v406_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v405_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS])
