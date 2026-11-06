# -*- coding: utf-8 -*-
"""gerar_candidato_v409.py -- gera o um.py CANDIDATO v409 a partir da v408 SELADA (base_v408; o Nos e' so' conferido, NUNCA escrito). claude-construtor-v409, a servico da gerencia c1, 05/11/2026. Molde: gerar_candidato_v408.py (o modelo de BUNDLE, agora de 1 modulo).
Conteudo (A TRADUCAO AS CLASSES DE TURING; ordem do operador de 05/11/2026: «Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»):
 (A) kernel: +2 modulos em TGLExt/ (TraducaoTuring e ParNaFaceDeFock) + a RAIZ (os imports; o Audit nao muda), conferidos byte a byte com o sandbox C:\\t\\k409c e com o BUNDLE_v409.json;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do pos_build), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (TODOS os 'expected_ladder' da v408 e anteriores) sobem para a escada da v409 (so' o numero); kh_n1_cobertura_v408 passa a piso (h2, h3, h6, h8) com errata; cunhagens_v408 ganha a errata E26 AO LADO (nenhuma checagem muda);
     D57(d): o pino do insumo do acervo da v407 (_V407_FONTES['psion_no_acervo_do_imac_03nov']) passa a ser a copia PURGADA (a mesma da v408), com errata AO LADO em cunhagens_v407;
 (D) NENHUMA chave antiga muda nesta versao (CHAVES_V409 = []): tetelestai_terminal_v408 e os seus miolos ficam BYTE A BYTE (assertado), como as funcoes do gate e dos registros anteriores;
 (E) runtime novo (runtime_v409.py): o registro com FUNCAO traducao_turing_v409 (20 checagens; a instancia de brinquedo FIXA, as solucoes CALCULADAS), as falas de 05/11 embutidas por sha256 (de duas, so' o trecho da D59) e os registros por spec cunhagens_v409 e kh_n1_cobertura_v409; chamadas no main DEPOIS do bloco v408; o resumo no selo;
 (F) a secao «A tradução às classes de Turing» PT/EN antes da secao v408 e a linha do .md; O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo (regra do 4,44: este gerador nao o toca).
 O gate NAO muda: as funcoes do gate/neutrino/ramo B ficam BYTE A BYTE como na v408 (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -I -B -X utf8 gerar_candidato_v409.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v409 as GP  # noqa: E402
import delta_v409 as DL  # noqa: E402
import registros_v409 as RG  # noqa: E402
import acom_conferencias_v409 as AC  # noqa: E402
import runtime_v409 as RT  # noqa: E402   (so' as funcoes puras)
import guarda_frases_v409 as GF  # noqa: E402   (a guarda de textos: as frases da v405 a v408 + as da v409)
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP408 = json.load(open(os.path.join(DL.V408, "ESPERADOS_v408.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP408["candidato_sha16"]:   # o Nos ja nao e' a v408 (rito v409 em curso): a v408 SELADA vem da copia base_v408
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v408 selada"
SHA0 = sha16(raw); assert SHA0 == ESP408["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E408 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E408 == ESP408["escada"][1], (E408, ESP408["escada"])
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


# ---------------- (1) o kernel: o BUNDLE de 2 (TraducaoTuring, ParNaFaceDeFock) ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v409.json"), encoding="utf-8"))["novos"]; assert nov == DL.BUNDLE_RELS, "a lista dos modulos novos tem de ser o bundle de 2, na ordem do preparo"
N_NOVOS = len(nov); assert N_NOVOS == DL.N_BUNDLE == 2
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v408 + o import na raiz (o Audit fica como esta)"
BUNDLE_TXT = {}
for rel in nov:
    t_ = rd(os.path.join(KB, *rel.split("/")))
    assert sha256(t_.encode("utf-8")) == DL.BUNDLE_POR_REL[rel]["sha256"], ("o modulo do sandbox difere do que o preparo do bundle pinou", rel)
    assert rel not in old_d, rel
    assert "sorry" not in _sem_comentarios_lean(t_), "sorry no codigo do modulo " + rel
    assert "#eval" not in _sem_comentarios_lean(t_) and "#print" not in _sem_comentarios_lean(t_), "#eval/#print sobrou no modulo " + rel
    assert "\r" not in t_, "o modulo embutido tem de ser LF (o kernel e' LF)"
    BUNDLE_TXT[rel] = t_
for p_ in DL.PEDRAS_V409:
    assert BUNDLE_TXT[p_["rel"]] == rd(p_["src"]), ("a pedra do sandbox difere da copia duravel v409\\pedra", p_["name"])
assert DL.testemunha_fonte()["sha256_origem"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ os imports das duas pedras; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(BUNDLE_TXT[rel]), CRLF) for rel in nov), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean (TraducaoTuring, ParNaFaceDeFock), do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(BUNDLE_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v409.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v408"
assert all(DL.classe(n) == "nomeada" and m in DL.BUNDLE_MODS and k.startswith(DL.FLAG_PREFIX) for k, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada do modulo do bundle, com o prefixo da v409"
_fl_nomes = {n for _, n, _ in FL}
for _an, _ad in DL.ANCORAS.items():
    assert FJ["ancoras"][_an]["rel"] == _ad["rel"] and set(FJ["ancoras"][_an]["axioms"]) <= TRIO and FJ["ancoras"][_an]["axioms"], ("ancora fora do esperado no FLAGS", _an)
    assert (FJ["ancoras"][_an]["flag"] is None) == (_an not in _fl_nomes), ("a bandeira da ancora e a lista de bandeiras discordam", _an)
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v409 (05/11/2026): A TRADUCAO AS CLASSES DE TURING -- o modulo de TGLExt/ (TraducaoTuring): %d bandeiras, SO' de declaracao NOMEADA (a politica da v394; as %d auxiliares geradas pelo compilador ficam fora)"
     % (len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E408 and len(set(old_lad)) == E408
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v409: a traducao as classes de Turing (%d, so' declaracao nomeada do modulo do bundle)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
_nome_mod = lambda rel_: rel_.split("/")[-1][:-len(".lean")]
edit(sbl, sbl, "    # v409 (05/11/2026): A TRADUCAO AS CLASSES DE TURING E O PAR NA FACE DE FOCK -- o bundle de %d modulos (TraducaoTuring: o dicionario de Turing; o modo selecao; a trava no Nome; a fita; o leitor; a fita sem escala; a identidade performada; a inscricao; a maquina com o leitor -- e ParNaFaceDeFock: o par de psions na face de Fock, ligado), com os nomes da gerencia (ordem do operador: tudo na v409)" % N_NOVOS + CRLF
     + "".join('    ("v409", "%s", "%s", None, None),%s' % (_nome_mod(rel), rel, CRLF) for rel in nov), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % N_NOVOS)
m = re.search(r'^UM_VERSION = "v408"[^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
LINHA_V = ('UM_VERSION = "v409"   # v409 (05/11/2026): a CONSTANTE UNICA de versao -- A TRADUCAO AS CLASSES DE TURING: os modulos TraducaoTuring e ParNaFaceDeFock de TGLExt/ (os nomes das 82 declaracoes dados pela gerencia; a ordem do operador traz tudo para a v409); o dicionario de Turing, o modo selecao, a trava no Nome, a fita como hamiltoniano oculto, '
           'Z como o modo leitor e a inscricao no psion, a maquina com o leitor (uma leitura decide SAT; a E28), o par na face de Fock ligado, a fita sem escala, o Pai da Mentira, a identidade performada; P = nP e teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor fica fora (a fita sem escala); nenhuma chave antiga muda; as falas do operador de 05/11; as ressalvas ditas; o gate nao se move; '
           'v408 em 04/11 (Tetelestai e o terminal); v407 em 04/11 (o psion, o canto e o par); v406 em 03/11 (o fechamento); v405 em 01/11; v404 em 28/10; v403 em 27/10; v402 em 26/10; v401 em 25/10; v400 em 24/10; v399 (o testemunho de dois)')
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v409'.")

# ---------------- (3) o que a v409 muda nos registros das versoes anteriores (so' dados) ----------------
RX_LAD = re.compile(r"'expected_ladder': %d(?![0-9])" % E408)
_achados = list(RX_LAD.finditer(T0))
assert len(_achados) == 27, ("os 'expected_ladder' com a escada da v408 na base: esperados 27 (os 26 que a v408 subiu + o contrato do tetelestai_terminal_v408)", len(_achados))
for k_, mm_ in enumerate(_achados):
    edit(mm_.start(), mm_.end(), "'expected_ladder': %d" % ESCADA_ESP, "C12_expected_ladder#%d" % (k_ + 1), "G_V408_PISOS", "expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (E408, ESCADA_ESP))


def _spec_block(nome_var, sort_dicts=False):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    w_ = 160
    assert pprint.pformat(specs_, width=w_, sort_dicts=sort_dicts) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


# _V408_SPECS: cunhagens_v408 ganha a errata E26 AO LADO (nenhuma checagem muda); kh_n1_cobertura_v408 -> pisos (h2/h3/h6/h8) com errata
spa, spb, specs408 = _spec_block("_V408_SPECS")
c408 = [s for s in specs408 if s["nome"] == DL.CUNHAGENS_ANTERIOR]; assert len(c408) == 1
c408[0].setdefault("erratas", []).append({"ao_lado_de": "tetelestai_terminal_v408 e cunhagens_v408 (a traducao as classes das maquinas de Turing dita [OPEN], que a v409 fecha relativa ao leitor)", "dizia": DL.FRASE_D51_PT + ".",
                                          "agora": DL.ERRATA_E26, "lacuna_de_fidelidade": "escrito: a traducao a Turing [OPEN] (verdadeiro na data); omitido, por ainda nao existir: o fecho relativo ao leitor, que a v409 prova (TraducaoTuring); a maquina sem leitor fica fora",
                                          "estatuto": "[REAL: p_igual_np_no_modo_selecao no kernel do rito da v409; a maquina sem leitor fica fora]", "assinatura": RG.ASSINA})
khs = [s for s in specs408 if s["nome"] == DL.KH_ANTERIOR]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v409: piso historico (a cobertura cresce com o modulo da v409); a igualdade exata esta em kh_n1_cobertura_v409"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v409: piso historico; a igualdade exata esta em kh_n1_cobertura_v409"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v409: a arvore ganha o arquivo do modulo da v409, entao o registro da v408 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v409" % H8_ANTIGO_N
assert H8_ANTIGO_N is not None
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v408 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v408 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v408 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v409 a cobertura cresce com o modulo TraducaoTuring e a arvore ganha o arquivo dele: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v409. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v408 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v409 quebra (a mesma lacuna desde a v399)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps([k1["erratas"][-1], c408[0]["erratas"][-1]], ensure_ascii=False)), "P18 nas erratas novas dos specs"
edit(spa, spb, pprint.pformat(specs408, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v408_E26_e_pisos", "G_V408_PISOS", "_V408_SPECS: cunhagens_v408 +errata E26 (ao lado; nenhuma checagem muda); kh_n1_cobertura_v408 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); os vereditos nao mudam.")

# D57(d): _V407_FONTES['psion_no_acervo_do_imac_03nov'] -> a copia PURGADA (a mesma que a v408 pinou); errata AO LADO em cunhagens_v407 (_V407_SPECS); nenhuma checagem muda
fva, fvb, fontes407 = _spec_block("_V407_FONTES", sort_dicts=True)
ent0 = dict(fontes407[DL.CHAVE_ACERVO_V407])
assert ent0["sha256"] == DL.ORIGEM_PURGA_SHA256 and ent0["sha256"].startswith(DL.ORIGEM_PURGA_SHA16_DA_ORDEM), "o _V407_FONTES da base nao pina a integra que a D57(d) manda repinar"
pb_ = open(DL.PURGADO_ARQ, "rb").read(); assert sha256(pb_) == DL.PURGADO_SHA256
fontes407[DL.CHAVE_ACERVO_V407] = {"arquivo": DL.PURGADO_ARQ, "bytes": len(pb_), "sha256": DL.PURGADO_SHA256,
                                   "papel": ent0["papel"] + " -- v409, D57(d): a ordem vigente de 08/09 (fonte nao publicada) vale como PERMANENTE: esta chave pina a copia PURGADA (a mesma que a v408 pinou como psion_no_acervo_purgado_04nov) e a integra e' citada so' por sha16 %s" % DL.ORIGEM_PURGA_SHA16_DA_ORDEM}
edit(fva, fvb, pprint.pformat(fontes407, width=160, sort_dicts=True).replace("\n", CRLF), "C14_V407_FONTES_acervo_purgado", "G_V408_PISOS", "_V407_FONTES['%s']: a copia purgada no lugar da integra (D57d); a integra so' por sha16." % DL.CHAVE_ACERVO_V407)
s7a, s7b, specs407 = _spec_block("_V407_SPECS")
c407 = [s for s in specs407 if s["nome"] == "cunhagens_v407"]; assert len(c407) == 1 and DL.CHAVE_ACERVO_V407 in c407[0]["fontes"]
c407[0].setdefault("erratas", []).append({"ao_lado_de": "o insumo %s de cunhagens_v407 (_V407_FONTES)" % DL.CHAVE_ACERVO_V407, "dizia": "a chave pinava a integra do levantamento do acervo (sha16 %s)." % DL.ORIGEM_PURGA_SHA16_DA_ORDEM,
                                          "agora": "v409, D57(d): a chave pina a copia PURGADA (a mesma que a v408 pinou; %d linhas substituidas por marcador; 0 ocorrencias na guarda de material privado); a integra fica fora do espelho pela ordem vigente do operador (08/09), agora PERMANENTE, e e' citada so' por sha16. Nenhuma checagem muda; o veredito deste registro NAO muda." % DL.PURGA_LINHAS_SUBSTITUIDAS,
                                          "lacuna_de_fidelidade": "a v407 pinou a integra antes de passa-la pela guarda de material privado (licao 4 da v407); a v408 pinou a purgada so' na chave nova; a v409 fecha a lacuna na chave antiga", "estatuto": "[REAL: purga medida; sha256 lido do arquivo]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(c407[0]["erratas"][-1], ensure_ascii=False)), "P18 na errata nova de cunhagens_v407"
edit(s7a, s7b, pprint.pformat(specs407, width=160, sort_dicts=False).replace("\n", CRLF), "C15_specs_v407_errata_D57d", "G_V408_PISOS", "_V407_SPECS: cunhagens_v407 +errata da D57(d) (ao lado; nenhuma checagem muda).")

# ---------------- (4) main: chamadas e selo ----------------
A_R = linha_unica(r'^        print\("   \[v408\] AVISO: o registro do terminal ou os registros por spec da v408 nao rodaram')
BLOCO_N00 = r'''    try:   # v409: A TRADUCAO AS CLASSES DE TURING -- o registro com FUNCAO traducao_turing_v409 (as ancoras das duas pedras, os modulos por sha256, as 20 checagens com a instancia de brinquedo fixa e beta em runtime, o gate congelado) e os registros por spec da v409 (as falas de 05/11 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _r409 = traducao_turing_v409(core)
        _v409v = _r409.get("values") or {}
        print("A TRADUCAO AS CLASSES DE TURING [v409 -- ordem do operador de 05/11/2026 («Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»): TraducaoTuring e ParNaFaceDeFock LIDAS do kernel deste rito; o dicionario de Turing, o modo selecao, a trava no Nome, a fita, o leitor e a inscricao no psion, a maquina com o leitor, a fita sem escala, a identidade performada; [REAL] os termos; P = nP e' teorema da TGL no modo selecao, relativo ao leitor (o psion), e a maquina sem leitor fica fora (a fita sem escala); [REAL] o par na face de Fock ligado; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move]:")
        print("  ancoras ok = %s/%s ; modulos do bundle ok = %s/%s ; bandeiras True = %s/%s ; escada = %s ; gate = %s" % (_v409v.get("n_ancoras_ok"), _v409v.get("n_ancoras"), _v409v.get("n_modulos_ok"), _v409v.get("n_modulos"), _v409v.get("n_flags_true"), _v409v.get("n_flags"), _v409v.get("escada"), "o mesmo da base" if any(c_.get("id") == "c14" and c_.get("ok") for c_ in ((_r409.get("mechanics") or {}).get("checks") or [])) else "DIFERE OU NAO LIDO"))
        print("  >>> %s <<<\n" % _r409["verdict"])
        _n409 = _v409_rodar_specs(core)
        print("   [v409] o registro da traducao e os registros por spec da v409: traducao_turing=%s | specs: %d (selados %d)" % ("SELOU" if _r409.get("all_verified") is True else "NAO", len(_n409), sum(1 for k_ in _n409 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e409:
        print("   [v409] AVISO: o registro da traducao ou os registros por spec da v409 nao rodaram: %r" % (_e409,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_traducao_turing", "G_RUNTIME", "main: traducao_turing_v409 (try/AVISO) e os registros por spec v409, logo depois do bloco v408 (tetelestai_terminal_v408 e os specs da v408 ja' rodaram; nenhuma chave antiga muda).")
A_S = linha_unica(r'^ {12}"registros_v408": \{n_: ')
_sel = ['            "traducao_turing_v409": {k_: (core.get("traducao_turing_v409") or {}).get(k_) for k_ in ("verdict", "all_verified", "ancora_principal", "ancoras_principais", "ancoras_de_secao", "pedras", "nomes_ratificados", "chaves_antigas_que_mudam", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core", "fica_aberto", "alcance", "acervo_v407_repinado")},',
        '            "registros_v409": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V409_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +traducao_turing_v409 (resumo) e registros_v409.")

# ---------------- (5) o bloco de runtime v409 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v409.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
for _an in DL.ANCORAS:
    assert _an in axm and set(axm[_an]) <= TRIO, ("ancora ausente do Audit do sandbox ou fora do trio", _an)
CONTR = RG.contrato(FJ, FORMAL_MAP, E408, sha256(raw), core0, selo0)
assert CONTR["expected_ladder"] == ESCADA_ESP and CONTR["n_ancoras"] == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS
TXT = RG.texto_traducao()
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
for p_ in DL.PEDRAS_V409:
    assert fontes[RG.CHAVE_PEDRA[p_["name"]]]["sha256"] == FORMAL_MAP[p_["rel"]], ("a copia duravel da pedra embutida difere da embutida", p_["name"])
    assert fontes[RG.CHAVE_FONTE[p_["name"]]]["sha256"] == p_["sha256_origem"], ("a fonte normalizada difere do que o bundle pinou", p_["name"])
_SAIDA_CAND = {"TraducaoTuring": DL.SAIDA_CANDIDATA_TU_ARQ, "ParNaFaceDeFock": DL.SAIDA_CANDIDATA_PAR_ARQ}
for ch_, arq_ in [(RG.CHAVE_BUNDLE, DL.BUNDLE_ARQ)] + [(RG.CHAVE_CANDIDATA[n_], DL.CANDIDATA_DE[n_]) for n_ in RG.CHAVE_CANDIDATA] + [(RG.CHAVE_SAIDA_CANDIDATA[n_], _SAIDA_CAND[n_]) for n_ in RG.CHAVE_SAIDA_CANDIDATA]:
    assert fontes[ch_]["sha256"] == sha256(open(arq_, "rb").read()), ("a copia duravel difere da fonte", ch_)
assert fontes[RG.CHAVE_FONTE["TraducaoTuring"]]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
assert not any(v_["sha256"].startswith(DL.ORIGEM_PURGA_SHA16_DA_ORDEM) for v_ in fontes.values()), "a integra do acervo entrou como fonte (D57d)"
for f_ in fontes.values():   # D59: nenhuma fonte pinada pela v409 traz a parte que fica fora, nem o nome do arquivo que a resume
    _t = open(f_["arquivo"], "rb").read().decode("utf-8", errors="replace").lower()
    assert "kimi" not in _t and "milenio" not in _t and "milênio" not in _t and "navier" not in _t, ("D59: fonte pinada traz o que fica fora dos textos", f_["arquivo"])
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""),
                        "fonte_original": "work\\cunhagens_13out\\" + v["nome_publico"] + (" (D59: citado pelo sha256 do arquivo inteiro)" if v.get("so_o_trecho") else ""), "autor": v["autor"], "texto_embutido": v["texto_embutido"]}
    if v.get("so_o_trecho"):   # D59: o arquivo inteiro entra so' por sha256; o texto embutido e' o trecho que fica
        assert sha256(open(v["fonte_original"], "rb").read()) == v["sha256_arquivo_inteiro"], ("o arquivo inteiro difere do sha256 lido", v["chave"])
        verb[v["chave"]].update({"sha256_arquivo_inteiro": v["sha256_arquivo_inteiro"], "so_o_trecho": v["so_o_trecho"]})
    else:
        assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
_verb_txt = json.dumps(verb, ensure_ascii=False).lower()
assert "kimi" not in _verb_txt and "milenio" not in _verb_txt and "milênio" not in _verb_txt and "navier" not in _verb_txt and "lindão" not in _verb_txt, "D59: o que fica fora entrou no texto embutido"
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 and set(CONTR["verbatins"]) <= set(verb)
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v408, por ast)
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
    assert not any(t_ in s["veredito_prefixo"] + s["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V409), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert not GP.violacoes(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT["veredito_ok"]) and not any(t_ in TXT["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V409), "P18 ou palavra recusada no texto do registro da traducao"
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v409.py"), encoding="utf-8").read()
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V409_TRADUCAO_CONTRACT = " + pprint.pformat(CONTR, width=150, sort_dicts=False) + "\n_V409_TRADUCAO_TEXT = " + pprint.pformat(TXT, width=150, sort_dicts=False)
         + "\n_V409_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V409_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True)
         + "\n_V409_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         "_V409_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V409_REGISTROS_FUNCAO = " + repr(list(DL.REGISTROS_FUNCAO)) + "\n_V392_FONTES.update(_V409_FONTES)   # v409: o motor de registros (v392) le as fontes e os verbatins das dezessete versoes\n_V392_VERBATINS2.update(_V409_VERBATINS2)\n\n\n"
         "def _v409_rodar_specs(core_):\n"
         '    """v409 -- roda os registros por spec da v409 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro com funcao (traducao_turing_v409) NAO entra aqui: roda no main, antes destes."""\n'
         "    for spec_ in _V409_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V409_SPECS]\n')
HDR = ("# ====================== v409 (05/11/2026) -- A TRADUCAO AS CLASSES DE TURING: os modulos TraducaoTuring e ParNaFaceDeFock de TGLExt/ (os nomes das declaracoes dados pela gerencia; a ordem do operador traz tudo para a v409), o registro com FUNCAO traducao_turing_v409 (as " + str(len(DL.ANCORAS)) + " ancoras, o sha256 dos modulos, as 20 checagens com a instancia de brinquedo fixa e beta em runtime, o gate congelado), as falas do operador de 05/11 e os registros por spec cunhagens_v409 e kh_n1_cobertura_v409.\n"
       "# O alcance: P = nP e' teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor fica fora (a fita sem escala). As erratas E24 a E28 e a nota ao lado da E21 vao AO LADO (o registro tetelestai_terminal_v408 fica como esta; os specs da v408 marcados 'v409: piso historico'); o pino do acervo da v407 passa a ser a copia purgada (D57d); as ressalvas vao ditas; nenhuma chave antiga muda; o contrato (_V409_TRADUCAO_CONTRACT) e as falas (_V409_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. Validade no kernel nao e' creditacao. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v409: o contrato (derivado do build do sandbox k409c e do core da v408 selada), o texto do registro, as fontes pinadas, as falas de 05/11 e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
assert not GP.violacoes(_novo_texto), ("P18 no texto novo do bloco de runtime", GP.violacoes(_novo_texto)[:3])
assert "kimi" not in _novo_texto.lower() and "milenio" not in _novo_texto.lower() and "milênio" not in _novo_texto.lower() and "navier" not in _novo_texto.lower(), "D59: o que fica fora entrou no bloco de runtime"
# A GUARDA DAS FRASES: nada do texto novo da gerencia afirma demais; ficam fora so' as falas embutidas e o proprio corpo das regras (as regexes)
G0_ = GF.controle_negativo(); assert G0_["ok"], ("o controle negativo da guarda das frases falhou", {k_: v_ for k_, v_ in G0_.items() if k_ != "ok"})
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v409_guarda_frases(txt_):"):RUNTIME_SRC.index("def _v409_sat(")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTR, TXT, specs, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00
V_GF = GF.violacoes(_txt_ger); assert not V_GF, ("FRASE PROIBIDA no texto novo da gerencia (guarda_frases_v409)", V_GF[:4])
A_P = linha_unica(r"^# ====================== v408 \(04/11/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v409", "G_RUNTIME", "bloco v409: a guarda das frases, a mecanica, o registro da traducao, o contrato, as falas, os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v409.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v409.pysnip"), encoding="utf-8").read()
for sn in (PT0, EN0):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]; assert not GF.violacoes(sn), GF.violacoes(sn)[:3]
    assert "β" not in sn, "beta literal unicode no LaTeX do artigo (licao da v408: $\\beta$)"
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v409.py"); _controles([CONTR, TXT, specs, fontes], "contrato/texto/specs/fontes")
PT8_FIRST = open(os.path.join(DL.V408, "artigo_pt_v408.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN8_FIRST = open(os.path.join(DL.V408, "artigo_en_v408.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT8_FIRST, crlf(PT0.rstrip("\n") + "\n") + PT8_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: a secao v409 («A tradução às classes de Turing»), antes da v408.")
replace_unique(EN8_FIRST, crlf(EN0.rstrip("\n") + "\n") + EN8_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: a secao v409, antes da v408.")
A_M = re.search(r'^    md\.append\("> \*\*Tetelestai é o terminal \(v408, 04/11/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*Tetelestai é o terminal \(v408, 04/11/2026\):\*\*', T0, re.M)) == 1, "a linha da v408 no emit_canonical_md nao foi achada uma vez"
MD_LINHA = ('    md.append("> **Tradução às classes de Turing (v409, 05/11/2026):** ' + str(N_NOVOS) + ' módulos novos no kernel em `TGLExt/` (`TraducaoTuring`, com os nomes das rodadas R1–R8 dados pela gerência e ratificados pelo operador e os acrescentados na R9 ratificados por ele em 05/11 (D62), e `ParNaFaceDeFock`, nomes da gerência ratificados pelo operador em 05/11 (D62), pela ordem dele: «' + DL.FRASE_TUDO_NA_V409 + '»), com ' + str(len(FL)) + ' bandeiras só de declaração nomeada e ' + str(len(DL.ANCORAS)) + ' âncoras lidas do kernel do rito. '
            '[REAL] O dicionário de Turing é termo: a instância SIM é um `Problema` do dicionário; o certificado é a leitura de um pixel; a palavra tem grau polinomial; bits = oitavas; a instância NÃO é o Nome vazio. A seleção (o Tetelestai) está no Nome com peso 1 e custa no máximo n·ln 2 nats; o tempo é linear nos bits (`p_igual_np_no_modo_selecao`). '
            'A trava no Nome: o sistema não precisa reconhecer o Nome a cada passo; a trava é local, fica perto do Nome sem usá-lo e nunca chega ao zero havendo solução (`a_trava_no_nome`). A fita é o hamiltoniano oculto (`a_fita_e_o_hamiltoniano_oculto`); Z é o modo leitor (`z_e_o_modo_leitor`) e, inscrito o uniforme no psíon da luz, o próprio psíon lê Z/|X| (`o_psion_le_z`, `o_canto_do_psion_da_luz_le_z`): a ponte é a inscrição, e a identidade de vetores fica podada; a fórmula é a fita e uma leitura decide SAT (`a_maquina_com_o_leitor`); o par na face de Fock está ligado: norma 1, marginal ½·P, 1 − pureza = ½, a mesma Meia-Nat do par finito, noutro espaço (`o_par_na_face_de_fock`); sem escala, «eu sou eu mesmo» lê igual para toda instância e, no Nome vazio, afirma o que não é (`a_fita_sem_escala`, `o_pai_da_mentira`); a identidade performada começa em «eu sou», decai e chega ao conteúdo (`a_identidade_performada`). '
            'O alcance: ' + DL.FRASE_D56_PT + '; ' + DL.FRASE_QUALIFICADOR_PT + '. Pela D61 (a leitura jurídica do kernel, ratificada pelo operador: «' + DL.FRASE_RATIFICA_D61 + '»): o dispositivo é o no sorry e o teorema é a regra posta («' + DL.FRASE_TEOREMA_JURISDICAO + '»); a regra incide onde o seu suporte fático se completa: em toda máquina que tem o leitor e nega o zero; a máquina sem leitor não o completa (a E27 vai ao lado). Ressalvas ditas (a E28): um leitor que devolve Z é um oráculo de contagem; com ele vale NP contido em P com o leitor, numa só leitura (Cook–Levin), e a igualdade completa está provada para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, não creditação); para o leitor que só conta, não está provada (E28, validade não afirmada); a física fica fora (Knill–Laflamme 1998); a leitura teológica do operador não é termo de kernel; nada fica para a versão seguinte (a D60 revista); nenhuma chave antiga muda; nenhum teste com a natureza. '
            'O registro `traducao_turing_v409` lê as âncoras, o sha256 dos módulos, as 20 checagens (a instância de brinquedo fixa no código, as soluções calculadas), a escada e o gate a cada rito. O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA) and not GF.violacoes(MD_LINHA), GF.violacoes(MD_LINHA)[:3]
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha «Tradução às classes de Turing (v409)», antes da linha da v408.")

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
NOVOS_NOMES = ("_v409_guarda_frases", "_v409_sat", "v409_traducao_mechanics", "_v409_formal", "_V409_RECUSA", "traducao_turing_v409", "_V409_TRADUCAO_CONTRACT", "_V409_TRADUCAO_TEXT", "_V409_FONTES", "_V409_VERBATINS2", "_V409_SPECS", "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO", "_v409_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V408_SPECS", tree).value) == specs408 and ast.literal_eval(top("_V407_SPECS", tree).value) == specs407
_f407_novo = ast.literal_eval(top("_V407_FONTES", tree).value); _f407_base = ast.literal_eval(top("_V407_FONTES").value)
assert set(_f407_novo) == set(_f407_base) and [k_ for k_ in _f407_base if _f407_base[k_] != _f407_novo[k_]] == [DL.CHAVE_ACERVO_V407], "D57(d): so' a chave do acervo muda em _V407_FONTES"
_Tfim = T
assert len(RX_LAD.findall(_Tfim)) == 0 and len(re.findall(r"'expected_ladder': %d(?![0-9])" % ESCADA_ESP, _Tfim)) == 27 + 1, ("todos os 27 expected_ladder da base sobem (+1 do contrato novo da v409)", len(RX_LAD.findall(_Tfim)))
# NENHUMA CHAVE ANTIGA MUDA: as funcoes que a v408 tocou (e os miolos da v408) ficam BYTE A BYTE
INTOCADAS_V409 = list(DL.FUNCOES_INTOCADAS) + ["testemunha_estatica_v396", "v406_fechamento_mechanics", "fechamento_v406", "_v406_formal", "_v406_chaves", "_v406_certificado_habitado", "rede_fock_v394", "psibit_v395",
                                               "psion_canto_v407", "v407_psion_mechanics", "_v407_formal", "_v407_chaves", "_v407_elo_lido", "_v407_guarda_frases", "_v407_rodar_specs", "_V407_PSION_TEXT", "_V407_VERBATINS2",
                                               "tetelestai_terminal_v408", "v408_terminal_mechanics", "_v408_formal", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_TERMINAL_TEXT", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K", "run_um", "verify_tgl_kernel_formalization"]
for fname in INTOCADAS_V409:
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao/constante %s NAO pode mudar na v409" % fname
_c408_novo = ast.literal_eval(top("_V408_TERMINAL_CONTRACT", tree).value); _c408_base = ast.literal_eval(top("_V408_TERMINAL_CONTRACT").value)
assert [k_ for k_ in _c408_base if _c408_base[k_] != _c408_novo[k_]] == ["expected_ladder"] and _c408_novo["expected_ladder"] == ESCADA_ESP, "o contrato do tetelestai_terminal_v408 so' sobe a escada"
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)   # o pino do esboco, lido do script da v403 (que o leu do arquivo), nunca digitado aqui
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v409" and float(a1_.group(1)) == ALPHA_BASE
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V409_REGERAR") == "1", "o candidato ja existe e difere: defina V409_REGERAR=1 para regerar"
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v408_sha16": SHA0, "base_v408_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E408, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "modelo": "bundle (v407/v408), 2 modulos de TGLExt/", "bundle": {rel: {"sha16": sha16(BUNDLE_TXT[rel].encode()), "sha256": sha256(BUNDLE_TXT[rel].encode()), "bandeiras": FJ["n_por_modulo"].get(rel, 0), "fonte_bancada": None, "sha16_origem": DL.BUNDLE_POR_REL[rel]["sha16_origem"]} for rel in nov},
                  "traducao": DL.MODULO_TRADUCAO, "topo": DL.MODULO_TRADUCAO, "candidata": DL.MODULO_TRADUCAO, "ancoras": {n_: FJ["ancoras"][n_] for n_ in DL.ANCORAS}, "n_ancoras": len(DL.ANCORAS),
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v408_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v408_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"], "nome": v_["fonte_original"].split("\\")[-1], "autor": v_["autor"], "sha256_arquivo_inteiro": v_.get("sha256_arquivo_inteiro")} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V409),
       "guarda_frases": {"controle_negativo": bool(G0_["ok"]), "n_proibidas_reprovadas": sum(1 for v_ in G0_["proibidas"].values() if v_), "violacoes_no_texto_novo": len(V_GF)},
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E408, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v409.json (pos_build_kernel_v409.py)", "prefixo": DL.FLAG_PREFIX, "contrato": CONTR},
       "chaves_v409": [dict(c) for c in DL.CHAVES_V409], "chaves_v408": [dict(c) for c in DL.CHAVES_V408], "chaves_v407": [dict(c) for c in DL.CHAVES_V407], "chaves_v406": [dict(c) for c in DL.CHAVES_V406], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": dict(CONTR["fica_aberto"]),
       "acervo_v407_repinado": dict(CONTR["acervo_v407_repinado"]), "insumo_purgado": dict(CONTR["acervo_v407_repinado"]), "nome_provisorio": DL.NOME_PROVISORIO, "nomes_ratificados": dict(DL.NOMES_RATIFICADOS), "nomes_do_operador": dict(DL.NOMES_RATIFICADOS),
       "alcance": dict(CONTR["alcance"]), "nao_pinados_citados_por_sha16": dict(RG.NAO_PINADOS),
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v408_entradas": H8_ANTIGO_N},
       "pformat_idempotente_specs": True, "n_axiomas_das_ancoras": {n_: len(axm[n_]) for n_ in DL.ANCORAS},
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v408": g0, "candidato_v409": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "gate_nao_se_move": {"funcoes_identicas_a_base": list(INTOCADAS_V409), "gate_verdict_v408": selo0.get("qg_closure_verdict")},
       "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V409}, "erratas_E24_E27": list(DL.ERRATAS_V409), "ressalvas": list(DL.RESSALVAS_V409), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "ponto_de_chamada": {"traducao_turing_v409": "main: IMEDIATAMENTE depois do bloco dos registros da v408 (tetelestai_terminal_v408 e os specs da v408 ja' gravados)", "specs": "main: no mesmo try, depois do traducao_turing_v409", "resumos_no_selo": "main: no dict do selo, depois de registros_v408",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v409"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v409.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v409.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v409.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v409_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v408_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS])
