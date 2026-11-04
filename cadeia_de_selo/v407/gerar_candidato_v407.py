# -*- coding: utf-8 -*-
"""gerar_candidato_v407.py -- gera o um.py CANDIDATO v407 a partir da v406 SELADA (base_v406; o Nos e' so' conferido, NUNCA escrito). claude-prep-v407, a servico da gerencia c1, 03/11/2026. Molde: gerar_candidato_v406.py (o modelo de BUNDLE, agora de 9 modulos).
Conteudo (O PSION, O CANTO E O PAR ENTRAM NO um.py; ordens do operador de 03/11/2026: «o lema que liga o psion ao canto também já pode ser derivado», «prossigamos com tudo, ratifico tudo», os nomes das pedras):
 (A) kernel: +9 modulos em TGLExt/ (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado) + a RAIZ (os nove imports; o Audit nao muda), conferidos byte a byte com o sandbox C:\\t\\k407c e com o BUNDLE_v407.json;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do pos_build), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (TODOS os 'expected_ladder' da v406, v405 e anteriores) sobem para a escada da v407 (so' o numero); kh_n1_cobertura_v406 passa a piso (h2, h3, h6, h8) com errata; cunhagens_v406 u7 (o lema que falta segue False) ganha a versao (errata E20); a checagem c8 do fechamento_v406 idem;
 (D) a funcao testemunha_estatica_v396, que trazia o literal linked_to_the_corner_by_a_lemma = False, passa a LER o kernel por _v407_elo_lido (errata E18 AO LADO; o texto selado dela nao e' reescrito: so' o literal vira leitura e ganha errata);
 (E) runtime novo (runtime_v407.py): o registro com FUNCAO psion_canto_v407, as falas de 03/11 embutidas por sha256 e os registros por spec cunhagens_v407 e kh_n1_cobertura_v407; chamadas no main DEPOIS do bloco v406; o resumo no selo;
 (F) a secao «O psíon e o canto» PT/EN antes da secao v406 e a linha do .md; O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo (regra do 4,44: este gerador nao o toca).
 O gate NAO muda: as funcoes do gate/neutrino/ramo B ficam BYTE A BYTE como na v406 (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -I -B -X utf8 gerar_candidato_v407.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v407 as GP  # noqa: E402
import delta_v407 as DL  # noqa: E402
import registros_v407 as RG  # noqa: E402
import acom_conferencias_v407 as AC  # noqa: E402
import runtime_v407 as RT  # noqa: E402   (so' as funcoes puras)
import guarda_frases_v407 as GF  # noqa: E402   (a guarda de textos: as frases da v406 + as da v407)
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP406 = json.load(open(os.path.join(DL.V406, "ESPERADOS_v406.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP406["candidato_sha16"]:   # o Nos ja nao e' a v406 (rito v407 em curso): a v406 SELADA vem da copia base_v406
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v406 selada"
SHA0 = sha16(raw); assert SHA0 == ESP406["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E406 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E406 == ESP406["escada"][1], (E406, ESP406["escada"])
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


# ---------------- (1) o kernel: o BUNDLE de 9 ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v407.json"), encoding="utf-8"))["novos"]; assert nov == DL.BUNDLE_RELS, "a lista dos modulos novos tem de ser o bundle de 9, na ordem do preparo"
N_NOVOS = len(nov); assert N_NOVOS == 9
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v406 + os nove imports na raiz (o Audit fica como esta)"
BUNDLE_TXT = {}
for rel in nov:
    t_ = rd(os.path.join(KB, *rel.split("/")))
    assert sha256(t_.encode("utf-8")) == DL.BUNDLE_POR_REL[rel]["sha256"], ("o modulo do sandbox difere do que o preparo do bundle pinou", rel)
    assert rel not in old_d, rel
    assert "sorry" not in _sem_comentarios_lean(t_), "sorry no codigo do modulo " + rel
    assert "#eval" not in _sem_comentarios_lean(t_) and "#print" not in _sem_comentarios_lean(t_), "#eval/#print sobrou no modulo " + rel
    BUNDLE_TXT[rel] = t_
for p_ in DL.PEDRAS_V407:
    assert BUNDLE_TXT[p_["rel"]] == rd(p_["src"]), ("a pedra do sandbox difere da copia duravel v407\\pedra", p_["name"])
assert DL.testemunha_fonte()["sha256_origem"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os nove imports das pedras; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(BUNDLE_TXT[rel]), CRLF) for rel in nov), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean (PsionCanto, Par e as sete pedras de 02/11), do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(BUNDLE_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v407.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v406"
assert all(DL.classe(n) == "nomeada" and m in DL.BUNDLE_MODS and k.startswith(DL.FLAG_PREFIX) for k, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada dos modulos do bundle, com o prefixo da v407"
_fl_nomes = {n for _, n, _ in FL}
for _an, _ad in DL.ANCORAS.items():
    assert FJ["ancoras"][_an]["rel"] == _ad["rel"] and set(FJ["ancoras"][_an]["axioms"]) <= TRIO and FJ["ancoras"][_an]["axioms"], ("ancora fora do esperado no FLAGS", _an)
    assert (FJ["ancoras"][_an]["flag"] is None) == (_an not in _fl_nomes), ("a bandeira da ancora e a lista de bandeiras discordam", _an)
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v407 (03/11/2026): O PSION, O CANTO E O PAR -- os %d modulos de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11): %d bandeiras, SO' de declaracao NOMEADA (a politica da v394; as %d auxiliares geradas pelo compilador ficam fora)"
     % (N_NOVOS, len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E406 and len(set(old_lad)) == E406
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v407: o psion, o canto e o par (%d, so' declaracao nomeada dos %d modulos do bundle)" % (len(FL), N_NOVOS) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
_nome_mod = lambda rel_: rel_.split("/")[-1][:-len(".lean")]
edit(sbl, sbl, "    # v407 (03/11/2026): O PSION, O CANTO E O PAR -- o bundle de %d modulos (o lema das duas faces, o par ligado e as sete pedras de 02/11 de nome ratificado)" % N_NOVOS + CRLF
     + "".join('    ("v407", "%s", "%s", None, None),%s' % (_nome_mod(rel), rel, CRLF) for rel in nov), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % N_NOVOS)
m = re.search(r'^UM_VERSION = "v406"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v407"   # v407 (03/11/2026): a CONSTANTE UNICA de versao -- O PSION, O CANTO E O PAR: os 9 modulos de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11, com os nomes do operador); o lema das duas faces do psion e a chave linked_to_the_corner_by_a_lemma lida do kernel; o par ligado, que nunca se cancela; '
           'o teste (d) so por citacao; o motor continuo fora; as falas do operador de 03/11; as ressalvas ditas; o gate nao se move; v406 em 03/11 (o fechamento: o certificado de Fock habitado); v405 em 01/11 (a massa derivada e a identidade definida); v404 em 28/10; v403 em 27/10; v402 em 26/10; v401 em 25/10; v400 em 24/10; v399 (o testemunho de dois)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v407'.")

# ---------------- (3) o que a v407 muda nos registros das versoes anteriores (so' dados) ----------------
RX_LAD = re.compile(r"'expected_ladder': %d(?![0-9])" % E406)
_achados = list(RX_LAD.finditer(T0))
assert len(_achados) == 25, ("os 'expected_ladder' com a escada da v406 na base: esperados 25 (v406 fecho 1 + v405 8 + v404 2 + v403 3 + v402 3 + v401 1 + v398 2 + v396 1 + v395 1 + v394 3)", len(_achados))
for k_, mm_ in enumerate(_achados):
    edit(mm_.start(), mm_.end(), "'expected_ladder': %d" % ESCADA_ESP, "C12_expected_ladder#%d" % (k_ + 1), "G_V406_PISOS", "expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (E406, ESCADA_ESP))


def _spec_block(nome_var):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    assert pprint.pformat(specs_, width=160, sort_dicts=False) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


def _versiona_check(spec_, id_, novo_op=None, novo_valor=None, nota_=""):
    """a checagem antiga fica como registro (descricao marcada «ate v406»); a vigente exige o estado lido do kernel (errata E20)."""
    cs_ = [c_ for c_ in spec_["checks"] if c_["id"] == id_]; assert len(cs_) == 1, (spec_["nome"], id_)
    c_ = cs_[0]
    antes_ = {"op": c_["op"], "valor": c_.get("valor")}
    if novo_op is not None:
        c_["op"] = novo_op
    if novo_valor is not None:
        c_["valor"] = novo_valor
    c_["descricao"] = "desde a v407 a chave e' LIDA do kernel do rito e a checagem exige o estado lido (%s%s)%s (errata E20, ao lado) -- ate' a v406 cobrava %s%s (o literal registrava o estado de entao); a descricao antiga, como registro: %s" % (c_["op"], (" " + repr(c_["valor"])) if c_.get("valor") is not None else "", nota_, antes_["op"], (" " + repr(antes_["valor"])) if antes_["valor"] is not None else "", c_["descricao"])
    return antes_


ERRATA_SPEC = lambda nome_, ids_: {"ao_lado_de": "%s (%s)" % (nome_, ", ".join(ids_)), "dizia": "a chave linked_to_the_corner_by_a_lemma cobrada como falsa: o literal da v396 a v406.",
                                   "agora": DL.ERRATA_E20, "lacuna_de_fidelidade": "um registro preso a um estado que a versao seguinte muda: o literal nao era leitura; a gerencia derivou o lema em 03/11 (errata E18)",
                                   "estatuto": "[REAL: o lema no kernel do rito; conferido no ensaio a seco]", "assinatura": RG.ASSINA}
# _V406_SPECS: cunhagens_v406 u7 (o lema que falta) e kh_n1_cobertura_v406 -> pisos (h2/h3/h6/h8)
spa, spb, specs406 = _spec_block("_V406_SPECS")
c406 = [s for s in specs406 if s["nome"] == "cunhagens_v406"]; assert len(c406) == 1
_u7 = _versiona_check(c406[0], "u7", novo_op="verdadeiro"); assert _u7 == {"op": "falso", "valor": None}, _u7
c406[0].setdefault("erratas", []).append(ERRATA_SPEC("cunhagens_v406", ["u7"]))
khs = [s for s in specs406 if s["nome"] == "kh_n1_cobertura_v406"]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v407: piso historico (a cobertura cresce com os 9 modulos da v407); a igualdade exata esta em kh_n1_cobertura_v407"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v407: piso historico; a igualdade exata esta em kh_n1_cobertura_v407"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v407: a arvore ganha os arquivos dos 9 modulos, entao o registro da v406 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v407" % H8_ANTIGO_N
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v406 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v406 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v406 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v407 a cobertura cresce com os 9 modulos e a arvore ganha os arquivos deles: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v407. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v406 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v407 quebra (a mesma lacuna desde a v399)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps([k1["erratas"][-1], c406[0]["erratas"][-1]], ensure_ascii=False)), "P18 nas erratas novas dos specs"
edit(spa, spb, pprint.pformat(specs406, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v406_u7_e_pisos", "G_V406_PISOS", "_V406_SPECS: cunhagens_v406 u7 falso -> verdadeiro (+ errata E20); kh_n1_cobertura_v406 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); os vereditos nao mudam.")
# fechamento_v406: a checagem c8 (o lema que falta segue False) -> versionada
OLD_C8 = ('        {"id": "c8", "descricao": "o que fica False por teorema segue False (full_static_witness_exists, trivial_inhabitant_exists) e o lema que falta segue False (linked_to_the_corner_by_a_lemma)", "ok": ch_["qg_closure.gate.full_static_witness_exists"] is False and ch_["witness_rigidity.trivial_inhabitant_exists"] is False and ch_["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is False},\r\n')
NEW_C8 = ('        {"id": "c8", "descricao": "o que fica False por teorema segue False (full_static_witness_exists, trivial_inhabitant_exists); a chave linked_to_the_corner_by_a_lemma e\' LIDA do kernel do rito desde a v407 (errata E20, ao lado) -- ate\' a v406 esta checagem cobrava que o lema que falta SEGUIA False (o literal registrava o estado de entao)", "ok": ch_["qg_closure.gate.full_static_witness_exists"] is False and ch_["witness_rigidity.trivial_inhabitant_exists"] is False and ch_["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is bool(_v407_elo_lido(kf_))},   # v407: o lema e\' lido do kernel (True quando o rito traz a PsionCanto no trio); na v406 era False\r\n')
replace_unique(OLD_C8, NEW_C8, "C20_fechamento_v406_c8", "G_CHAVES", "fechamento_v406 c8: o lema que falta deixa de ser cobrado False e passa a ser igual a leitura do kernel (_v407_elo_lido); errata E20.")

# ---------------- (G) a funcao que trazia o literal linked_to_the_corner_by_a_lemma = False: o literal vira LEITURA do kernel (errata E18 AO LADO); o texto selado nao e' reescrito ----------------
OLD_TE = ('             "linked_to_the_corner_by_a_lemma": False,\r\n')
NEW_TE = ('             "linked_to_the_corner_by_a_lemma": _v407_elo_lido(kf_),   # v407: LIDA do kernel do rito (TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces no trio, declarado em TGLExt/PsionCanto.lean, fonte por sha256); ate\' a v406 era o literal False (errata E18 AO LADO)\r\n'
          '             "elo_v407": {"lemma": "TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces" if _v407_elo_lido(kf_) else None, "kind": ("STRUCTURE_NOT_VECTORS" if _v407_elo_lido(kf_) else None), "identifies_omega_with_bell_vector": False, "pair_on_the_fock_face": "OPEN", "bell_to_tt_bridge": "NOT_A_TERM",\r\n'
          '                          "reading_v396_v406": "no lemma identifies psion C with the psionCorner of this stone (literal False, v396 to v406; errata E18)", "reading_v407": "the lemma of the two faces is in the kernel of the rite (PsionCanto): on both faces the psion is the unit vector whose corner is the projector onto it, the corner scalarises, weighs one and returns itself under the Jones reading; the link is one of structure, not of vectors (Omega and the Bell vector live in distinct spaces and are not identified); the pair of psions on the Fock face stays open"},\r\n')
OLD_RD = '             "reading": ("the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; since v406 the kernel of the rite exhibits an inhabitant of the certificate (physicalFockCertificate, read from the axiom report and the provenance, not literal); no lemma identifies psion C with the psionCorner of this stone" if _hab406t_ else "the Fock face of the psion is a statement for every Fock certificate; this rite reads no inhabitant of the certificate in its kernel; no lemma identifies psion C with the psionCorner of this stone"),'   # [R2, 03/11] a LINHA INTEIRA da base (antes era so' o prefixo; a precedencia deixava o prefixo novo so' no ramo com habitante)
NEW_RD = '             "reading": (("since v407 the lemma of the two faces is a term of the kernel of the rite (TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; a link of structure, not of vectors; errata E18): the sentence that follows is the reading of v396 to v406, kept as record: " if _v407_elo_lido(kf_) else "") + ("the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; since v406 the kernel of the rite exhibits an inhabitant of the certificate (physicalFockCertificate, read from the axiom report and the provenance, not literal); no lemma identifies psion C with the psionCorner of this stone" if _hab406t_ else "the Fock face of the psion is a statement for every Fock certificate; this rite reads no inhabitant of the certificate in its kernel; no lemma identifies psion C with the psionCorner of this stone")),'   # [R2, 03/11] prefixo (quando o lema e' lido) + (o IfExp antigo, verbatim, como operando direito)
replace_unique(OLD_RD, NEW_RD, "C19b_testemunha_reading_ramifica", "G_CHAVES", "testemunha_estatica_v396: o campo fock_face.reading ramifica pela chave lida (v407: o lema e' termo; a frase antiga fica como registro de v396-v406). BAIXO 4 da R1.")
replace_unique(OLD_TE, NEW_TE, "C19_testemunha_linked_vira_leitura", "G_CHAVES", "testemunha_estatica_v396: linked_to_the_corner_by_a_lemma deixa de ser literal False e passa a _v407_elo_lido(kf_); +elo_v407 (estrutura, nao vetores; o par na face de Fock OPEN); errata E18.")

# ---------------- (4) main: chamadas e selo ----------------
A_R = linha_unica(r'^        print\("   \[v406\] AVISO: o fechamento ou os registros por spec da v406 nao rodaram')
BLOCO_N00 = r'''    try:   # v407: O PSION, O CANTO E O PAR -- o registro com FUNCAO psion_canto_v407 (as ancoras das nove pedras, os 9 modulos por sha256, a chave do lema LIDA do kernel, as respostas do operador, a escada, o gate) e os registros por spec da v407 (as falas de 03/11 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _r407 = psion_canto_v407(core)
        _v407v = _r407.get("values") or {}
        print("O PSION, O CANTO E O PAR [v407 -- ordem do operador de 03/11/2026 («o lema que liga o psion ao canto também já pode ser derivado»): o lema das duas faces (PsionCanto) e o par ligado (Par) LIDOS do kernel deste rito; a chave linked_to_the_corner_by_a_lemma deixa de ser literal; [REAL] os termos e a leitura; [OPEN] o par na face de Fock; [ONTO] a ponte Bell-TT; os nomes das pedras sao do operador; validade no kernel nao e' creditacao; o gate nao se move]:")
        print("  ancoras ok = %s/%s ; modulos do bundle ok = %s/%s ; bandeiras True = %s/%s ; chave do lema (lida do kernel) = %s ; escada = %s ; gate = %s" % (_v407v.get("n_ancoras_ok"), _v407v.get("n_ancoras"), _v407v.get("n_modulos_ok"), _v407v.get("n_modulos"), _v407v.get("n_flags_true"), _v407v.get("n_flags"), _r407.get("link_read_from_the_kernel"), _v407v.get("escada"), "o mesmo da base" if any(c_.get("id") == "c14" and c_.get("ok") for c_ in ((_r407.get("mechanics") or {}).get("checks") or [])) else "DIFERE OU NAO LIDO"))
        print("  >>> %s <<<\n" % _r407["verdict"])
        _n407 = _v407_rodar_specs(core)
        print("   [v407] o registro do psion e do canto e os registros por spec da v407: psion_canto=%s | specs: %d (selados %d)" % ("SELOU" if _r407.get("all_verified") is True else "NAO", len(_n407), sum(1 for k_ in _n407 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e407:
        print("   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v407 nao rodaram: %r" % (_e407,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_psion_canto", "G_RUNTIME", "main: psion_canto_v407 (try/AVISO) e os registros por spec v407, logo depois do bloco v406 (fechamento_v406, rede_fock_v394, psibit_v395, testemunha_estatica_v396 e witness_layers ja' rodaram: as chaves que ele le ja' estao gravadas).")
A_S = linha_unica(r'^ {12}"registros_v406": \{n_: ')
_sel = ['            "psion_canto_v407": {k_: (core.get("psion_canto_v407") or {}).get(k_) for k_ in ("verdict", "all_verified", "link_read_from_the_kernel", "lemma", "pair_theorem", "keys", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core", "pedras", "nomes_do_operador", "fica_aberto", "teste_d")},',
        '            "registros_v407": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V407_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +psion_canto_v407 (resumo) e registros_v407.")

# ---------------- (5) o bloco de runtime v407 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v407.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
for _an in DL.ANCORAS:
    assert _an in axm and set(axm[_an]) <= TRIO, ("ancora ausente do Audit do sandbox ou fora do trio", _an)
CONTR = RG.contrato(FJ, FORMAL_MAP, E406, sha256(raw), core0, selo0)
assert CONTR["expected_ladder"] == ESCADA_ESP
TXT = RG.texto_psion()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
for p_ in DL.PEDRAS_V407:
    assert fontes[RG.CHAVE_PEDRA[p_["name"]]]["sha256"] == FORMAL_MAP[p_["rel"]], ("a copia duravel da pedra difere da embutida", p_["name"])
for ch_, arq_ in ((RG.CHAVE_BUNDLE, DL.BUNDLE_ARQ), (RG.CHAVE_TESTE_D, DL.D_TESTE_MANIFESTO), (RG.CHAVE_FASE9, DL.FASE9_V2_ARQ), (RG.CHAVE_ACERVO, DL.ACERVO_PSION_ARQ), (RG.CHAVE_REVISAO_PEDRAS, DL.REVISAO_PEDRAS_02NOV_ARQ), (RG.CHAVE_PLANO, DL.PLANO_ARQ), (RG.CHAVE_DESENHO, DL.DESENHO_ARQ)):
    assert fontes[ch_]["sha256"] == sha256(open(arq_, "rb").read()), ("a copia duravel difere da fonte", ch_)
assert fontes[RG.CHAVE_FASE9]["sha256"][:16] == DL.FASE9_V2_SHA16_DA_ORDEM and fontes[RG.CHAVE_TESTE_D]["sha256"][:16] == DL.D_TESTE_SHA16_DA_ORDEM
assert fontes[RG.CHAVE_CANDIDATA_PSION_R1]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""), "fonte_original": v.get("fonte_original", "")}
    assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V407) and set(CONTR["verbatins"]) <= set(verb)
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v406, por ast)
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
assert not GP.violacoes(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT["veredito_ok"]), "P18 ou palavra recusada no texto do registro do psion e do canto"
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v407.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V407_PSION_CONTRACT = " + pprint.pformat(CONTR, width=150, sort_dicts=False) + "\n_V407_PSION_TEXT = " + pprint.pformat(TXT, width=150, sort_dicts=False)
         + "\n_V407_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V407_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True)
         + "\n_V407_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V407_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V407_REGISTROS_FUNCAO = " + repr(list(DL.REGISTROS_FUNCAO)) + "\n_V392_FONTES.update(_V407_FONTES)   # v407: o motor de registros (v392) le as fontes e os verbatins das quinze versoes\n_V392_VERBATINS2.update(_V407_VERBATINS2)\n\n\n"
         "def _v407_rodar_specs(core_):\n"
         '    """v407 -- roda os registros por spec da v407 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro com funcao (psion_canto_v407) NAO entra aqui: roda no main, antes destes."""\n'
         "    for spec_ in _V407_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V407_SPECS]\n')
HDR = ("# ====================== v407 (03/11/2026) -- O PSION, O CANTO E O PAR ENTRAM NO um.py: os 9 modulos de TGLExt/ (PsionCanto, Par e as sete pedras de 02/11 de nome ratificado), o registro com FUNCAO psion_canto_v407 (as ancoras, os 9 sha256, a chave do lema LIDA do kernel, as respostas do operador), as falas do operador de 03/11 e os registros por spec cunhagens_v407 e kh_n1_cobertura_v407.\n"
       "# As erratas E18 a E20 vao AO LADO (o literal da v396 a v406 fica como registro: elo_v407.reading_v396_v406, os specs marcados «ate' a v406»); as ressalvas vao ditas; o contrato (_V407_PSION_CONTRACT) e as falas (_V407_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. Validade no kernel nao e' creditacao. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v407: o contrato (derivado do build do sandbox k407c e do core da v406 selada), o texto do registro, as fontes pinadas, as falas de 03/11 e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
# A GUARDA DAS FRASES: nada do texto novo da gerencia afirma demais; ficam fora so' as falas embutidas e o proprio corpo das regras (as regexes)
G0_ = GF.controle_negativo(); assert G0_["ok"], ("o controle negativo da guarda das frases falhou", {k_: v_ for k_, v_ in G0_.items() if k_ != "ok"})
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v407_guarda_frases(txt_):"):RUNTIME_SRC.index("def _v407_elo_lido(kf_):")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTR, TXT, specs, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00 + NEW_TE + NEW_C8
V_GF = GF.violacoes(_txt_ger); assert not V_GF, ("FRASE PROIBIDA no texto novo da gerencia (guarda_frases_v407)", V_GF[:4])
A_P = linha_unica(r"^# ====================== v406 \(02/11/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v407", "G_RUNTIME", "bloco v407: a guarda das frases, a leitura do lema, o registro do psion e do canto, o contrato, as falas, os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v407.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v407.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]; assert not GF.violacoes(sn), GF.violacoes(sn)[:3]
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v407.py"); _controles([CONTR, TXT, specs, fontes], "contrato/texto/specs/fontes")
PT6_FIRST = open(os.path.join(DL.V406, "artigo_pt_v406.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN6_FIRST = open(os.path.join(DL.V406, "artigo_en_v406.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT6_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT6_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: a secao v407 («O psíon e o canto»), antes da v406.")
replace_unique(EN6_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN6_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: a secao v407, antes da v406.")
A_M = re.search(r'^    md\.append\("> \*\*O fechamento \(v406, 02/11/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*O fechamento \(v406, 02/11/2026\):\*\*', T0, re.M)) == 1, "a linha da v406 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **O psíon, o canto e o par (v407, 03/11/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel em `TGLExt/` (`PsionCanto`, `Par`, `APonteDoAtrito`, `OUmInscrito`, `KEhATangente`, `AChaveDaGuarda`, `OGuarda`, `LeituraPreservada` e `OIgual`, com os nomes do operador), com ' + str(len(FL)) + ' bandeiras só de declaração nomeada. '
            '[REAL] O lema `the_psion_is_the_corner_on_both_faces` diz que nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor sobre ele, que o canto escalariza, pesa 1 e devolve o canto sob a leitura de Jones (`P Δ^{it} P = P`); o elo é de ESTRUTURA, não de vetores: o vácuo de Fock Ω e o vetor de Bell Φ⁺ não são identificados. '
            'A chave `linked_to_the_corner_by_a_lemma`, literal `False` da v396 à v406, passa a ser lida do kernel do próprio rito, com errata E18 ao lado. A pedra `Par` confere, com termos que o kernel já tinha, que o par é ligado (CCI = 1/2), nunca se cancela, é lido pela fase dobrada e pelo retorno de fase e que o canto é o projetor 4×4. '
            'Ressalvas ditas: o par na face de Fock segue [OPEN] (o certificado não tem operadores de criação como termo); a ponte Bell–TT não é termo; K(O) ≠ ⊥ só na cunha; três das sete pedras de 02/11 foram revistas pelo Sonnet, as outras quatro não; o teste (d) do ramo B entra só por citação do pré-registro V1.1, sem resultado; o motor contínuo fica fora. '
            'Os nomes das pedras são do operador (03/11/2026). O registro `psion_canto_v407` lê as âncoras, os 9 sha256, a chave, as respostas do operador, a escada e o gate a cada rito. O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA) and not GF.violacoes(MD_LINHA)
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «O psíon, o canto e o par (v407)», antes da linha da v406.")

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
NOVOS_NOMES = ("_v407_guarda_frases", "_v407_elo_lido", "_v407_chaves", "v407_psion_mechanics", "_v407_formal", "_V407_RECUSA", "psion_canto_v407", "_V407_PSION_CONTRACT", "_V407_PSION_TEXT", "_V407_FONTES", "_V407_VERBATINS2", "_V407_SPECS", "_V407_NOMES_REGISTROS", "_V407_REGISTROS_FUNCAO", "_v407_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V406_SPECS", tree).value) == specs406
_Tfim = T
assert len(RX_LAD.findall(_Tfim)) == 0 and len(re.findall(r"'expected_ladder': %d(?![0-9])" % ESCADA_ESP, _Tfim)) == 25 + 1, ("todos os 25 expected_ladder da base sobem (+1 do contrato novo da v407)", len(RX_LAD.findall(_Tfim)))
# as duas funcoes tocadas: so' as linhas dos patches C19/C19b/C20 mudam
import difflib
for fname in ("testemunha_estatica_v396", "v406_fechamento_mechanics"):
    s0 = ast.get_source_segment(T0, top(fname)).splitlines(); s1 = ast.get_source_segment(T, top(fname, tree)).splitlines()
    dif = [l_ for l_ in difflib.unified_diff(s0, s1, lineterm="", n=0) if l_[:1] in "+-" and not l_.startswith(("+++", "---"))]
    rem = [l_[1:] for l_ in dif if l_.startswith("-")]; add = [l_[1:] for l_ in dif if l_.startswith("+")]
    _old_lines = set((OLD_TE + "\n" + OLD_C8).replace("\r\n", "\n").split("\n")); _new_lines = set((NEW_TE + "\n" + NEW_C8).replace("\r\n", "\n").split("\n"))
    # [R2, 03/11] o C19b: OLD_RD/NEW_RD sao PREFIXOS da linha do reading (o resto da linha fica igual); a guarda os trata como um par (removida, acrescentada) com o mesmo resto. A primeira regeracao R2 pegou a omissao; a segunda, o prefixo.
    _rd_add = [l_ for l_ in add if l_.startswith(NEW_RD)]; _rd_rem = [l_ for l_ in rem if l_.startswith(OLD_RD)]
    assert len(_rd_add) == len(_rd_rem) <= 1 and all(a_[len(NEW_RD):] == r_[len(OLD_RD):] for a_, r_ in zip(_rd_add, _rd_rem)), (fname, "C19b: a linha do reading so' pode mudar no prefixo OLD_RD -> NEW_RD", len(_rd_add), len(_rd_rem))
    add = [l_ for l_ in add if l_ not in _rd_add]; rem = [l_ for l_ in rem if l_ not in _rd_rem]
    assert set(add) <= (_new_lines - _old_lines) and set(rem) <= (_old_lines - _new_lines), (fname, [l_ for l_ in add if l_ not in _new_lines][:2], [l_ for l_ in rem if l_ not in _old_lines][:2])
    assert len(rem) + len(_rd_rem) == {"testemunha_estatica_v396": 2, "v406_fechamento_mechanics": 1}[fname] and "_v407_elo_lido" in "\n".join(s1) and "_v407_elo_lido" not in "\n".join(s0), (fname, len(rem), len(_rd_rem))   # [R2] testemunha: C19 + C19b; fechamento: C20
# O GATE NAO SE MOVE (sobre o texto FINAL)
for fname in DL.FUNCOES_INTOCADAS:
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao %s NAO pode mudar na v407" % fname
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)   # o pino do esboco, lido do script da v403 (que o leu do arquivo), nunca digitado aqui
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v407" and float(a1_.group(1)) == ALPHA_BASE
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V407_REGERAR") == "1", "o candidato ja existe e difere: defina V407_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v406_sha16": SHA0, "base_v406_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E406, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "modelo": "bundle (v406), 9 modulos de TGLExt/", "bundle": {rel: {"sha16": sha16(BUNDLE_TXT[rel].encode()), "sha256": sha256(BUNDLE_TXT[rel].encode()), "bandeiras": FJ["n_por_modulo"].get(rel, 0), "fonte_bancada": None, "sha16_origem": DL.BUNDLE_POR_REL[rel]["sha16_origem"]} for rel in nov},
                  "topo": DL.MODULO_PSION, "par": DL.MODULO_PAR, "rede": DL.MODULO_PAR, "candidata": DL.MODULO_PSION, "ancoras": {n_: FJ["ancoras"][n_] for n_ in DL.ANCORAS},
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v406_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v406_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"], "nome": os.path.basename(v_["fonte_original"])} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "guarda_frases": {"controle_negativo": bool(G0_["ok"]), "n_proibidas_reprovadas": sum(1 for v_ in G0_["proibidas"].values() if v_), "violacoes_no_texto_novo": len(V_GF)},
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E406, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v407.json (pos_build_kernel_v407.py)", "prefixo": DL.FLAG_PREFIX, "contrato": CONTR},
       "chaves_v407": [dict(c) for c in DL.CHAVES_V407], "chaves_v406": [dict(c) for c in DL.CHAVES_V406], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": {"par_na_face_de_fock": DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "ponte_bell_tt": DL.FICA_ABERTO_PONTE_BELL_TT},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v406_entradas": H8_ANTIGO_N},
       "pformat_idempotente_specs": True, "n_axiomas_das_ancoras": {n_: len(axm[n_]) for n_ in DL.ANCORAS},
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v406": g0, "candidato_v407": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "gate_nao_se_move": {"funcoes_identicas_a_base": list(DL.FUNCOES_INTOCADAS), "gate_verdict_v406": selo0.get("qg_closure_verdict")},
       "decisoes": dict(DL.DECISOES), "erratas_E18_E20": list(DL.ERRATAS_V407), "ressalvas": list(DL.RESSALVAS_V407), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"psion_canto_v407": "main: IMEDIATAMENTE depois do bloco dos registros da v406 (fechamento_v406, rede_fock_v394, psibit_v395, testemunha_estatica_v396 e witness_layers ja' gravados)", "specs": "main: no mesmo try, depois do psion_canto_v407", "resumos_no_selo": "main: no dict do selo, depois de registros_v406",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v407"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v407.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v407.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v407.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v407.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v407_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v406_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS])
