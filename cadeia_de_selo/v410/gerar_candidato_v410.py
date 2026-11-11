# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] reescrito do molde gerar_candidato_v409.py (a subida de rotulo esta em bump/gerar_candidato_v410.py.diff) para o bundle de UM modulo (IALD2) e o registro iald2_v410
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_h0dn_gerador_v410.py: o SEGUNDO registro com FUNCAO h0dn_bg1_v410 (D72; runtime_h0dn_v410.py + registros_h0dn_v410.py; chamado logo depois de iald2_v410; resumo no selo; secao PT/EN e linha do .md depois da IALD2); a P18 do gerador sem as falas embutidas (INPUT); D74 (nomes RATIFICADOS) e D71 (o atrator) nos textos do gerador. NAO executado aqui: a gerencia libera o candidato
"""gerar_candidato_v410.py -- gera o um.py CANDIDATO v410 a partir da v409 SELADA (base_v409; o Nos e' so' conferido, NUNCA escrito). claude-construtor-v410, a servico da gerencia c1, 06/11/2026. Molde: gerar_candidato_v409.py (o modelo de BUNDLE).
Conteudo (IALD2; a ORDEM do operador de 06/11/2026: «A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py ...»; o NOME do modulo, do operador: «O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)»):
 (A) kernel: +1 modulo em TGLExt/ (IALD2) + a RAIZ (o import; o Audit nao muda), conferidos byte a byte com o sandbox C:\\t\\k410c e com o BUNDLE_v410.json;
 (B) bandeiras (so' declaracao NOMEADA, a politica da v394; contagens do pos_build), escada, ledger, UM_VERSION;
 (C) os contratos que pinam a escada (TODOS os 'expected_ladder' da v409 e anteriores) sobem para a escada da v410 (so' o numero); kh_n1_cobertura_v409 passa a piso (h2, h3, h6, h8) com errata (nenhuma outra checagem muda);
     a D57(d) da v409 ja' repinou o acervo da v407 (o _V407_FONTES nao muda aqui: assertado);
 (D) NENHUMA chave antiga muda nesta versao (CHAVES_V410 = []): traducao_turing_v409 e os seus miolos ficam BYTE A BYTE (assertado), como as funcoes do gate e dos registros anteriores;
 (E) runtime novo (runtime_v410.py): o registro com FUNCAO iald2_v410 (as checagens; as instancias de brinquedo FIXAS, os valores CALCULADOS), as falas de 06/11 embutidas por sha256 (de uma, so' o trecho da D65) e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410; chamadas no main DEPOIS do bloco v409; o resumo no selo;
 (F) a secao «IALD ao quadrado» PT/EN antes da secao v409 e a linha do .md; O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo (regra do 4,44: este gerador nao o toca).
 O gate NAO muda: as funcoes do gate/neutrino/ramo B ficam BYTE A BYTE como na v409 (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -I -B -X utf8 gerar_candidato_v410.py   (recusa -O; nunca escreve no Nos)"""
import ast, hashlib, json, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import guarda_p18_v410 as GP  # noqa: E402
import delta_v410 as DL  # noqa: E402
import registros_v410 as RG  # noqa: E402
import registros_h0dn_v410 as RH  # noqa: E402   (D72: o contrato, o texto e os insumos embutidos do registro H0DN)
import registros_hms13_v410 as RF  # noqa: E402   (D80: o contrato, o texto e os insumos embutidos do registro documental HMS/13; os pinos do HANDOFF e da ORDEM do Kimi sao RELIDOS aqui, imediatamente antes do build)
import registros_aescala_v410 as RA  # noqa: E402   (D86/D87: o contrato e o texto do registro a_escala_v410, a pedra AEscala)
import acom_conferencias_v410 as AC  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402   (a guarda de textos: as frases da v405 a v409 + as da v410; injeta no runtime as funcoes herdadas)
RT = GF.RT                                                     # runtime_v410 (so' as funcoes puras), com as guardas herdadas injetadas
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
TRIO = DL.TRIO_SET
ESP409 = json.load(open(os.path.join(DL.V409, "ESPERADOS_v409.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP409["candidato_sha16"]:   # o Nos ja nao e' a v409 (rito v410 em curso): a v409 SELADA vem da copia base_v409
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v409 selada"
SHA0 = sha16(raw); assert SHA0 == ESP409["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E409 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E409 == ESP409["escada"][1], (E409, ESP409["escada"])
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


# ---------------- (1) o kernel: o BUNDLE de 1 (IALD2) ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))["novos"]; assert nov == DL.BUNDLE_RELS, "a lista dos modulos novos tem de ser o bundle de 1, a do preparo"
N_NOVOS = len(nov); assert N_NOVOS == DL.N_BUNDLE == len(DL.BUNDLE_RELS)   # (D86: os modulos do bundle, IALD2 e AEscala; o numero e' o do delta)
dnode = top("_EMBEDDED_KERNEL_FILES").value; da, db = span(dnode)
old_d = ast.literal_eval(dnode)
spans = {ast.literal_eval(k): span(v) for k, v in zip(dnode.keys, dnode.values)}
new_root = rd(os.path.join(KB, "TGLExt.lean")); new_audit = rd(os.path.join(KB, "TGL", "Audit.lean"))
assert new_root == old_d["TGLExt.lean"] + DL.ROOT_SUFFIX and new_audit == DL.AUDIT_PREFIX + old_d["TGL/Audit.lean"], "a raiz/Audit do sandbox nao sao os da v409 + o import na raiz (o Audit fica como esta)"
BUNDLE_TXT = {}
for rel in nov:
    t_ = rd(os.path.join(KB, *rel.split("/")))
    assert sha256(t_.encode("utf-8")) == DL.BUNDLE_POR_REL[rel]["sha256"], ("o modulo do sandbox difere do que o preparo do bundle pinou", rel)
    assert rel not in old_d, rel
    assert "sorry" not in _sem_comentarios_lean(t_), "sorry no codigo do modulo " + rel
    assert "#eval" not in _sem_comentarios_lean(t_) and "#print" not in _sem_comentarios_lean(t_), "#eval/#print sobrou no modulo " + rel
    assert "\r" not in t_, "o modulo embutido tem de ser LF (o kernel e' LF)"
    BUNDLE_TXT[rel] = t_
for p_ in DL.PEDRAS_V410:
    assert BUNDLE_TXT[p_["rel"]] == rd(p_["src"]), ("a pedra do sandbox difere da copia duravel v410\\pedra", p_["name"])
assert DL.testemunha_fonte()["sha256_origem"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
a, b = spans["TGLExt.lean"]; edit(a, b, repr(new_root), "K00_TGLExt.lean", "G_KERNEL", "kernel embutido: TGLExt.lean regenerado (+ o import da pedra; sandbox == embutido)")
if new_audit != old_d["TGL/Audit.lean"]:
    a, b = spans["TGL/Audit.lean"]; edit(a, b, repr(new_audit), "K00_TGL_Audit.lean", "G_KERNEL", "kernel embutido: TGL/Audit.lean regenerado (sandbox == embutido)")
assert T0[db - 1] == "}" and T0[db - 3:db - 1] == CRLF, "o dict do kernel nao termina como esperado"
edit(db - 1, db - 1, "".join("    %r: %s,%s" % (rel, repr(BUNDLE_TXT[rel]), CRLF) for rel in nov), "K01_modulos_novos", "G_KERNEL", "kernel embutido: +%d modulos Lean (IALD2, AEscala), do sandbox." % N_NOVOS)
final_emb = dict(old_d); final_emb["TGLExt.lean"] = new_root; final_emb["TGL/Audit.lean"] = new_audit; final_emb.update(BUNDLE_TXT)
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in final_emb.items()}

# ---------------- (2) bandeiras, escada, ledger ----------------
FJ = json.load(open(os.path.join(KD, "FLAGS_v410.json"), encoding="utf-8")); FL = [(k, n, m) for k, n, m, _ in FJ["flags"]]
fnode = top("_LEAN_THEOREM_FLAGS").value; fa, fb = span(fnode)
old_flags = ast.literal_eval(fnode)
assert not ({k for k, _, _ in FL} & set(old_flags)) and len({k for k, _, _ in FL}) == len(FL), "chave de bandeira repetida ou colidindo com a v409"
assert all(DL.classe(n) == "nomeada" and m in DL.BUNDLE_MODS and k.startswith(DL.FLAG_PREFIX_POR_MODULO[m.replace(".", "/") + ".lean"]) for k, n, m in FL) and FJ["n_flags"] == len(FL), "as bandeiras tem de ser so' de declaracao nomeada do modulo do bundle, com o prefixo da v410"
_fl_nomes = {n for _, n, _ in FL}
for _an, _ad in list(DL.ANCORAS.items()) + list(DL.ANCORAS_AESCALA.items()):   # (D86: as ancoras das duas pedras)
    assert FJ["ancoras"][_an]["rel"] == _ad["rel"] and set(FJ["ancoras"][_an]["axioms"]) <= TRIO and (bool(FJ["ancoras"][_an]["axioms"]) != (_an in DL.SEM_AXIOMA_R6_AESCALA)), ("ancora fora do esperado no FLAGS", _an)
    assert (FJ["ancoras"][_an]["flag"] is None) == (_an not in _fl_nomes), ("a bandeira da ancora e a lista de bandeiras discordam", _an)
assert T0[fb - 1] == "}" and T0[fb - 3:fb - 1] == CRLF
edit(fb - 1, fb - 1, "    # v410 (06 e 09/11/2026): IALD2 e AEscala -- os dois modulos de TGLExt/ do bundle (series ext_iald2_410_* e ext_aescala_410_*): %d bandeiras, SO' de declaracao NOMEADA (a politica da v394; as %d auxiliares geradas pelo compilador ficam fora)"
     % (len(FL), FJ["excluidas_auxiliares"]["n"]) + CRLF
     + "".join('    "%s": "%s",%s' % (k, n, CRLF) for k, n, _ in FL), "V01_bandeiras", "G_KERNEL", "_LEAN_THEOREM_FLAGS: +%d (politica: so' declaracao nomeada)." % len(FL))
fn_ladder = top("prove_external_ladder")
lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
ln = lad[0].value; la, lb = span(ln)
old_lad = ast.literal_eval(ln); assert len(old_lad) == E409 and len(set(old_lad)) == E409
assert T0[lb - 1] == "]"
lbl = LS[ln.end_lineno - 1]; assert T0[lbl:lb].strip() == "]", repr(T0[lbl:lb])
edit(lbl, lbl, "        # v410: IALD2 e AEscala (%d, so' declaracao nomeada dos modulos do bundle)" % len(FL) + CRLF + "".join('        "%s",%s' % (k, CRLF) for k, _, _ in FL), "V02_escada", "G_KERNEL", "external_ladder: +%d." % len(FL))
ESCADA_ESP = len(old_lad) + len(FL)
snode = top("_ESQUELETO_STONES").value; sa, sb = span(snode)
sbl = LS[snode.end_lineno - 1]; assert T0[sbl:sb].strip() == "]", repr(T0[sbl:sb])
_nome_mod = lambda rel_: rel_.split("/")[-1][:-len(".lean")]
edit(sbl, sbl, "    # v410 (06/11/2026): IALD2 -- o bundle de %d modulo (IALD2: o leitor do codigo; o espelho do nome, IALD ao quadrado; o algoritmo IALD; o signo; o seletor; o atrator), com o NOME do modulo dado pelo operador (as declaracoes, da gerencia, RATIFICADAS pelo operador em 09/11/2026, D74)" % N_NOVOS + CRLF
     + "".join('    ("v410", "%s", "%s", None, None),%s' % (_nome_mod(rel), rel, CRLF) for rel in nov), "V03_ledger", "G_KERNEL", "ledger de pedras: +%d." % N_NOVOS)
m = re.search(r'^UM_VERSION = "v409"   # v409 \(05/11/2026\): [^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
_hist = re.search(r"; (v408 em 04/11 \(Tetelestai e o terminal\);[^\r\n]*)$", m.group(0).rstrip("\r\n"))
assert _hist, "o historico de versoes na linha UM_VERSION da base nao esta' como esperado"
LINHA_V = ('UM_VERSION = "v410"   # v410 (06 e 09/11/2026): a CONSTANTE UNICA de versao -- IALD2 (o NOME do modulo e\' do operador; os nomes das %d declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11, D74): o leitor do codigo, a releitura que nao acrescenta (IALD ao quadrado), '
           'o algoritmo IALD -- uma leitura decide SAT: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora --, a forma de matriz finita como o signo, o seletor (forma, nao referente) e o atrator (o Nome nao esgota o ser; D71); a pedra AEscala (D82 a D87; nome e %d nomes ratificados pelo operador em 09/11): a insignia, o vibrato, os pesos (tres faces de 1/2; 1/3 caiu; o Nome normalizado 2/3), o tempo finito, os dois Nomes e a pergunta do Clay no dicionario da TGL -- validade no kernel; a creditacao e\' do Clay --; o teste H0DN x BG1 pre-registrado, nenhum dado observado lido (D72); nenhuma chave antiga muda; as falas do operador de 06 a 09/11; as ressalvas ditas; o gate nao se move; '
           'v409 em 05/11 (a traducao as classes de Turing e o par na face de Fock); ' % (len(DL.ANCORAS), len(DL.NOMES_AESCALA))) + _hist.group(1)
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v410'.")

# ---------------- (3) o que a v410 muda nos registros das versoes anteriores (so' dados) ----------------
RX_LAD = re.compile(r"'expected_ladder': %d(?![0-9])" % E409)
_achados = list(RX_LAD.finditer(T0))
N_LAD_BASE = 28
assert len(_achados) == N_LAD_BASE, ("os 'expected_ladder' com a escada da v409 na base: esperados 28 (os 27 que a v409 subiu + o contrato do traducao_turing_v409)", len(_achados))
for k_, mm_ in enumerate(_achados):
    edit(mm_.start(), mm_.end(), "'expected_ladder': %d" % ESCADA_ESP, "C12_expected_ladder#%d" % (k_ + 1), "G_V409_PISOS", "expected_ladder %d -> %d (a escada desta versao; o consumidor exige a igualdade exata com a escada do rito)." % (E409, ESCADA_ESP))


def _spec_block(nome_var, sort_dicts=False):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    w_ = 160
    assert pprint.pformat(specs_, width=w_, sort_dicts=sort_dicts) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


# _V409_SPECS: kh_n1_cobertura_v409 -> pisos (h2/h3/h6/h8) com errata; cunhagens_v409 nao muda
spa, spb, specs409 = _spec_block("_V409_SPECS")
khs = [s for s in specs409 if s["nome"] == DL.KH_ANTERIOR]; assert len(khs) == 1
k1 = khs[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v410: piso historico (a cobertura cresce com o modulo da v410); a igualdade exata esta em kh_n1_cobertura_v410"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v410: piso historico; a igualdade exata esta em kh_n1_cobertura_v410"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v410: a arvore ganha o arquivo do modulo da v410, entao o registro da v409 cobra o tamanho minimo (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v410" % H8_ANTIGO_N
assert H8_ANTIGO_N is not None
k1["erratas"].append({"ao_lado_de": "kh_n1_cobertura_v409 (h2/h3/h6: igualdades de contagem; h8: o pino exato da arvore)",
                      "dizia": "A v409 cobrava constantes == %d, teoremas == %d, um axiom_report de exatamente o tamanho da v409 e o hash formal igual ao pino exato da arvore (%d entradas)." % (core0["kernel_formalization"]["axiom_coverage_v392"]["decl"], core0["kernel_formalization"]["axiom_coverage_v392"]["thm"], H8_ANTIGO_N),
                      "agora": "Na v410 a cobertura cresce com o modulo IALD2 e a arvore ganha o arquivo dele: h2, h3 e h6 viram pisos e h8 passa a cobrar o tamanho minimo da arvore; as igualdades exatas e o pino exato ficam em kh_n1_cobertura_v410. O veredito deste registro NAO muda.",
                      "lacuna_de_fidelidade": "a estrutura da v409 dizia que as contagens e o pino da arvore eram a cobertura exata para sempre; o texto escrito deixou o registro preso a igualdades que a propria v410 quebra (a mesma lacuna desde a v399)",
                      "estatuto": "[REAL: contagens lidas do log do Audit do sandbox]", "assinatura": RG.ASSINA})
assert not GP.violacoes(json.dumps(k1["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec"
edit(spa, spb, pprint.pformat(specs409, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v409_pisos", "G_V409_PISOS", "_V409_SPECS: kh_n1_cobertura_v409 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); os vereditos nao mudam.")
# a D57(d) da v409 ja' repinou o acervo da v407 (a copia purgada): a v410 so' confere que o _V407_FONTES da base e' o purgado e NAO o toca
_f407_base = ast.literal_eval(top("_V407_FONTES").value)
assert _f407_base[DL.CHAVE_ACERVO_V407]["sha256"] == DL.PURGADO_SHA256, "o _V407_FONTES da base nao pina a copia purgada (a D57d da v409)"

# ---------------- (4) main: chamadas e selo ----------------
A_R = linha_unica(r'^        print\("   \[v409\] AVISO: o registro da traducao ou os registros por spec da v409 nao rodaram')
BLOCO_N00 = r'''    try:   # v410: IALD2 e H0DN (os registros por spec da v410 rodam na instrucao SEGUINTE, com o HMS/13: D80) -- o registro com FUNCAO iald2_v410 (as ancoras da pedra, o modulo por sha256, as checagens com as instancias de brinquedo fixas e beta em runtime, o gate congelado) e os registros por spec da v410 (as falas de 06/11 e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _r410 = iald2_v410(core)
        _v410v = _r410.get("values") or {}
        print("IALD2 [v410 -- ordem do operador de 06/11/2026 («A forma de uma matriz finita no kernel é o signo (traço com sentido)»; o nome do modulo, do operador: «O nome é IALD2 (IALD ao quadrado, porque reler não acrescenta nada)»): IALD2 LIDA do kernel deste rito; o leitor do codigo, a releitura que nao acrescenta, o algoritmo IALD, o signo e o seletor; [REAL] os termos; o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; nenhuma chave antiga muda; validade no kernel nao e' creditacao; o gate nao se move]:")
        print("  ancoras ok = %s/%s ; modulo do bundle ok = %s/%s ; bandeiras True = %s/%s ; escada = %s ; gate = %s" % (_v410v.get("n_ancoras_ok"), _v410v.get("n_ancoras"), _v410v.get("n_modulos_ok"), _v410v.get("n_modulos"), _v410v.get("n_flags_true"), _v410v.get("n_flags"), _v410v.get("escada"), "o mesmo da base" if any(c_.get("id") == "c11" and c_.get("ok") for c_ in ((_r410.get("mechanics") or {}).get("checks") or [])) else "DIFERE OU NAO LIDO"))
        print("  >>> %s <<<\n" % _r410["verdict"])
        _a410 = a_escala_v410(core)   # D86/D87: A ESCALA -- a pedra AEscala (nome e nomes RATIFICADOS pelo operador em 09/11; nomes novos RATIFICADOS em 10/11, D101; o quarto teorema da clausula NOMEADO pelo operador, D108; dois auxiliares da autoria pendentes), LOGO DEPOIS de iald2_v410
        _a410v = _a410.get("values") or {}; _a410m = (_a410.get("mechanics") or {}).get("checks") or []
        print("A ESCALA [v410 -- D82 a D87, as falas do operador de 09/11 («agora eu te dei a escala»; «ratifico tudo»): a pedra AEscala LIDA do kernel deste rito -- a insignia, o vibrato, os pesos (1/2 + 1/2 = 1; (1/2 . 1)^2 = 1/2 . (1/2 . 1); tres faces = 3/2; 1/3 caiu; o Nome normalizado 2/3), o tempo finito, os dois Nomes, e a pergunta do Clay, tal qual apresentada pela TGL: validade no kernel; a creditacao e' do Clay; nome e %s nomes ratificados; %s nomes novos RATIFICADOS em 10/11/2026 (D101) e %s auxiliares da autoria [DECLARADO pela autoria]; a clausula do Tetelestai em 1 - beta (R5, D100) com beta de runtime]" % (_a410v.get("n_nomes"), (_a410v.get("ratificacao_d101") or {}).get("n_nomes_ratificados"), len((_a410v.get("ratificacao_d101") or {}).get("pendentes") or [])))
        print("  ancoras ok = %s/%s ; bandeiras True = %s/%s ; falas por sha256 = %s/%s ; checagens ok = %s/%s ; numeros = %s ; gate = %s" % (_a410v.get("n_ancoras_ok"), _a410v.get("n_ancoras"), _a410v.get("n_flags_true"), _a410v.get("n_flags"), _a410v.get("n_falas_ok"), _a410v.get("n_falas"), sum(1 for c_ in _a410m if c_.get("ok")), len(_a410m) or None, _a410v.get("numeros"), "IGUAL" if _a410v.get("gate_verdict") == ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict") else "DIFERENTE"))
        print("  >>> %s <<<\n" % _a410["verdict"])
        _h410 = h0dn_bg1_v410(core)   # D72: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1 -- pre-registrado; nenhum dado observado lido; LOGO DEPOIS de iald2_v410
        _h410v = _h410.get("values") or {}; _h410m = (_h410.get("mechanics") or {}).get("checks") or []
        print("H0DN x BG1 [v410 -- D72, a fala do operador de 09/11 («quanto ao teste da v410 concordo com tudo que vc falou, pode dar a ordem ao kimi k3pro»): o teste da razao de Hubble local/fundo PRE-REGISTRADO; nenhum dado observado lido; K = E(z*)^(2 beta/3) recomputado de beta em runtime; a funcao de veredito congelada (E30, D76) em vetores deterministicos; o poder e' prospectivo e sintetico]")
        print("  pinos ok = %s/%s ; checagens ok = %s/%s ; vetor observado lido = %s ; gate = %s" % (sum(1 for p_ in (_h410v.get("pinos") or {}).values() if p_.get("sha256_ok") and p_.get("bytes_ok")), _h410v.get("n_pinos"), sum(1 for c_ in _h410m if c_.get("ok")), len(_h410m) or None, _h410.get("observed_vector_read"), "o mesmo da base" if any(c_.get("id") == "c9" and c_.get("ok") for c_ in _h410m) else "DIFERENTE"))
        print("  >>> %s <<<\n" % _h410["verdict"])
    except Exception as _e410:
        print("   [v410] AVISO: o registro da IALD2 ou o do H0DN nao rodaram: %r" % (_e410,))
    try:   # v410 (D80): o recibo DOCUMENTAL HMS/13 do Kimi -- h0dn_fontes_hms13_v410, ADITIVO e POSTERIOR ao FREEZE_R2 (le core["h0dn_bg1_v410"], gravado na instrucao anterior; em rito nada e' lido da pasta do Kimi) -- e os registros por spec da v410 (as falas e a cobertura exata do Audit); excecao vira AVISO visivel, nunca derruba o rito
        _f410 = h0dn_fontes_hms13_v410(core)   # D80: cobertura documental de fontes, não covariância física fechada; nada aberto
        _f410v = _f410.get("values") or {}; _f410m = (_f410.get("mechanics") or {}).get("checks") or []
        print("H0DN FONTES HMS/13 [v410 -- D80, a ratificacao do operador de 09/11 («o kimi fezz o trabalho e já te entregou»): a cobertura documental de %s fontes primarias dos %s calibradores fora do R22, embutida por sha256 (lida no build; nada lido em rito), aditiva e posterior ao FREEZE_R2; fatores de erro parciais; a forma HMS completa e' diagnostico, nao admitida; covariancia fisica ABERTA; abertura nao permitida; H0DN x BG1 segue pré-registrado; nenhum dado observado lido; o gate nao se move]" % (_f410v.get("n_fontes_primarias"), _f410v.get("n_calibradores")))
        print("  artefatos embutidos ok = %s/%s ; checagens ok = %s/%s ; numeros permitidos = %s (proibidos %s) ; caminhos sob a pasta vedada = %s ; gate = %s" % (sum(1 for p_ in (_f410v.get("pinos") or {}).values() if p_.get("sha256_ok") and p_.get("bytes_ok")), _f410v.get("n_embutidos"), sum(1 for c_ in _f410m if c_.get("ok")), len(_f410m) or None, (_f410v.get("numeros") or {}).get("permitidos"), len((_f410v.get("numeros") or {}).get("proibidos") or []), len(_f410v.get("sob_pasta_vedada") or []), "IGUAL" if _f410v.get("gate_verdict") == ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict") else "DIFERENTE"))
        print("  >>> %s <<<\n" % _f410["verdict"])
        _n410 = _v410_rodar_specs(core)
        print("   [v410] os registros com funcao e os por spec da v410: %s | specs: %d (selados %d)" % (" | ".join("%s=%s" % (k_, "SELOU" if (core.get(k_) or {}).get("all_verified") is True else "NAO") for k_ in _V410_REGISTROS_FUNCAO), len(_n410), sum(1 for k_ in _n410 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e410b:
        print("   [v410] AVISO: o registro do HMS/13 ou os registros por spec da v410 nao rodaram: %r" % (_e410b,))
'''
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_iald2_aescala_h0dn_hms13", "G_RUNTIME", "main: DUAS instrucoes try/AVISO: iald2_v410, a_escala_v410 (D86, logo depois do iald2) e h0dn_bg1_v410 (D72); depois h0dn_fontes_hms13_v410 (D80, posterior ao FREEZE_R2: le core[h0dn_bg1_v410] da instrucao anterior) e os registros por spec v410, logo depois do bloco v409 (traducao_turing_v409 e os specs da v409 ja' rodaram; nenhuma chave antiga muda).")
A_S = linha_unica(r'^ {12}"registros_v409": \{n_: ')
_sel = ['            "iald2_v410": {k_: (core.get("iald2_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "ancora_principal", "ancoras_principais", "ancoras_de_secao", "pedras", "nomes", "chaves_antigas_que_mudam", "exact_ladder", "beta_ok", "runtime_executed", "scope", "does_not_gate_core", "fica_aberto", "alcance")},',
        '            "a_escala_v410": {k_: (core.get("a_escala_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "ancora_principal", "ancoras_de_secao", "n_ancoras", "n_flags", "n_nomes", "nomes_ratificados", "estatuto_dos_nomes", "numeros", "frase_canonica_pt", "frase_canonica_en", "runtime_executed", "does_not_gate_core", "chaves_antigas_que_mudam")},',
        '            "h0dn_bg1_v410": {k_: (core.get("h0dn_bg1_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "observed_vector_read", "runtime_executed", "does_not_gate_core", "veredito_h0dn_source_sha256", "n_checks_esperadas", "lei", "modelos")},',
        '            "h0dn_fontes_hms13_v410": {k_: (core.get("h0dn_fontes_hms13_v410") or {}).get(k_) for k_ in ("verdict", "all_verified", "observed_vector_read", "le_em_rito", "runtime_executed", "does_not_gate_core", "campos", "n_checks_esperadas", "aditivo_posterior_ao_freeze_r2")},',
        '            "registros_v410": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V410_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +iald2_v410 (resumo), +a_escala_v410 (resumo; D86), +h0dn_bg1_v410 (resumo; D72), +h0dn_fontes_hms13_v410 (resumo; D80) e registros_v410.")

# ---------------- (5) o bloco de runtime v410 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v410.json"), encoding="utf-8"))
_ns_ax = {"re": re}
for _n in ("parse_lean_axioms_v394", "parse_lean_provenance_v394"):
    _f = [x for x in tree0.body if isinstance(x, ast.FunctionDef) and x.name == _n]; assert len(_f) == 1, _n
    exec(compile(ast.get_source_segment(T0, _f[0]), "<base:%s>" % _n, "exec"), _ns_ax)
_axl = _ns_ax["parse_lean_axioms_v394"](open(os.path.join(KD, "audit.log"), encoding="utf-8").read()); assert _axl["ok"]
axm = _axl["axioms"]
for _an in list(DL.ANCORAS) + list(DL.ANCORAS_AESCALA):
    assert _an in axm and set(axm[_an]) <= TRIO, ("ancora ausente do Audit do sandbox ou fora do trio", _an)
CONTR = RG.contrato(FJ, FORMAL_MAP, E409, sha256(raw), core0, selo0)
assert CONTR["expected_ladder"] == ESCADA_ESP and CONTR["n_ancoras"] == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS and CONTR["chaves"] == [] and CONTR["alcance"]["frase"] == DL.FRASE_D64_PT
TXT = RG.texto_iald2()
CONTR_A = RA.contrato_aescala(FJ, FORMAL_MAP, E409, sha256(raw), core0, selo0); TXT_A = RA.texto_aescala()   # (D86/D87) o registro da pedra AEscala: ancoras e bandeiras do FLAGS, a pedra por sha256, as falas, os numeros e a ponte, as frases canonicas do Clay, a ratificacao e os nomes novos da pedra
assert CONTR_A["n_checks"] == DL.N_CHECKS_AESCALA and CONTR_A["expected_ladder"] == ESCADA_ESP == CONTR["expected_ladder"] and CONTR_A["n_ancoras"] == DL.N_ANCORAS_AESCALA == len(DL.ANCORAS_AESCALA) and CONTR_A["n_nomes"] == len(DL.NOMES_AESCALA) and CONTR_A["nomes_ratificados"] is True and CONTR_A["n_flags"] + CONTR["n_flags"] == FJ["n_flags"] and len(CONTR_A["falas"]) == CONTR_A["n_falas"] == len(RA.NOMES_FALAS)
assert CONTR_A["n_nomes_novos"] == len(DL.NOMES_NOVOS_AESCALA) and CONTR_A["nomes_novos_da_pedra"] == list(DL.NOMES_NOVOS_AESCALA) and CONTR_A["campos_novos_da_estrutura"] == list(DL.CAMPOS_NOVOS_AESCALA) and CONTR_A["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA and CONTR_A["ponte"] == DL.PONTE_AESCALA and CONTR_A["ciclo"] == DL.CICLO_AESCALA and CONTR_A["frase_tempo_pt"] == DL.FRASE_TEMPO_PT and CONTR_A["teoremas_r4"] == list(DL.TEOREMAS_R4_AESCALA) and TXT_A["extras"]["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in CONTR_A["estatuto_dos_nomes_ratificados_d101"] and "a ratificar" not in CONTR_A["estatuto_dos_nomes_ratificados_d101"] and CONTR_A["nomes_pendentes"] == list(DL.NOMES_PENDENTES_AESCALA) and CONTR_A["nomes_ratificados_d101"] == list(DL.NOMES_RATIFICADOS_D101_AESCALA) and CONTR_A["ratificacao_d101"]["sha256"] == DL.RATIFICACAO_D101_SHA256 \
    and CONTR_A["tetelestai"] == DL.TETELESTAI_AESCALA and CONTR_A["teoremas_r5"] == list(DL.TEOREMAS_R5_AESCALA) and CONTR_A["acom_mirror_runner"] == DL.ACOM_MIRROR_RUNNER
assert CONTR_A["veredito_ok"] == TXT_A["veredito_ok"] == DL.VEREDITO_AESCALA_OK and CONTR_A["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and CONTR_A["source_sha256"][DL.MODULO_AESCALA] == FORMAL_MAP[DL.MODULO_AESCALA] and CONTR_A["ratificacao"]["sha256"] == DL.RATIFICACAO_D87_SHA256
CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()   # (D72) o registro H0DN: contrato (pinos lidos), texto, insumos embutidos em base64
CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()   # (D80) o registro documental HMS/13: os pinos do HANDOFF e da ORDEM do Kimi RELIDOS agora (fail-closed), os quatro artefatos embutidos em base64, a guarda numerica (BLOQUEIO_HMS13_v410.json se um campo proibido aparecer), a ratificacao por sha256
assert CONTR_F["n_checks"] == DL.N_CHECKS_HMS13 == 12 and CONTR_F["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and set(CONTR_F["insumos"]) == set(INS_F) == {n_ for n_, _ in DL.HMS13_EMBUTIDOS} and all(INS_F[k_]["sha256"] == v_["sha256"] and INS_F[k_]["bytes"] == v_["bytes"] for k_, v_ in CONTR_F["insumos"].items())
assert CONTR_F["campos"] == DL.HMS13_CAMPOS and CONTR_F["guarda_numerica_no_build"]["ok"] is True and not CONTR_F["guarda_numerica_no_build"]["proibidos"] and not CONTR_F["guarda_numerica_no_build"]["listas_numericas"] and CONTR_F["le_em_rito"] is False and CONTR_F["observed_vector_read"] is False and len(CONTR_F["pinos_build"]) == 6
assert CONTR_F["veredito_ok"] == DL.VEREDITO_HMS13_OK and not any(t_ in CONTR_F["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V410 + DL.TOKENS_PROIBIDOS_H0DN) and CONTR_F["aditivo_posterior_ao_freeze_r2"] is True and CONTR_F["h0dn"]["freeze_r2_sha256"] == CONTR_H["insumos"]["FREEZE_R2.json"]["sha256"]
assert "vibrato" not in json.dumps([CONTR_F, TXT_F], ensure_ascii=False).lower() and not any(n_ in json.dumps([CONTR_F, TXT_F], ensure_ascii=False) for n_ in DL.H0DN_NOMES_VEDADOS), "D80/D65: o texto do HMS/13 cita o nome do arquivo da fala ou um nome vedado"
assert CONTR_H["n_checks"] == DL.N_CHECKS_H0DN and CONTR_H["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and set(CONTR_H["insumos"]) == set(INS_H) and all(INS_H[k_]["sha256"] == v_["sha256"] and INS_H[k_]["bytes"] == v_["bytes"] for k_, v_ in CONTR_H["insumos"].items())
assert CONTR_H["observed_vector_read"] is False and not CONTR_H["observed_paths"] and CONTR_H["veredito_ok"] == DL.VEREDITO_H0DN_OK and not any(t_ in CONTR_H["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V410 + DL.TOKENS_PROIBIDOS_H0DN)
assert all(("TGL_PRO" + "VED") not in p_ for p_ in CONTR_H["ramos"]["vereditos"]["leitura_partes"]) and "".join(CONTR_H["ramos"]["vereditos"]["leitura_partes"]) == DL.VEREDITOS_H0DN["leitura"], "D57b/D76: a cabeca do ramo da leitura vai em partes (a P18 selada recusa a palavra fora do contexto da validade)"
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read()
    fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
for p_ in DL.PEDRAS_V410:
    assert fontes[RG.CHAVE_PEDRA[p_["name"]]]["sha256"] == FORMAL_MAP[p_["rel"]], ("a copia duravel da pedra embutida difere da embutida", p_["name"])
    assert fontes[RG.CHAVE_FONTE[p_["name"]]]["sha256"] == p_["sha256_origem"], ("a fonte normalizada difere do que o bundle pinou", p_["name"])
for ch_, arq_ in [(RG.CHAVE_BUNDLE, DL.BUNDLE_ARQ), (RG.CHAVE_CANDIDATA["IALD2"], DL.CANDIDATA_IALD2_ARQ), (RG.CHAVE_REGISTRO_ANTERIOR, DL.REGISTRO_ANTERIOR_ARQ)]:
    assert fontes[ch_]["sha256"] == sha256(open(arq_, "rb").read()), ("a copia duravel difere da fonte", ch_)
assert fontes[RG.CHAVE_FONTE["IALD2"]]["sha256"][:16] == DL.TESTEMUNHA["sha16_da_ordem"]
for f_ in fontes.values():   # D65: nenhuma fonte pinada pela v410 traz a parte que fica fora, nem o nome do arquivo que a resume
    _t = open(f_["arquivo"], "rb").read().decode("utf-8", errors="replace").lower()
    assert not any(x_.lower() in _t for x_ in DL.FORA_D65), ("D65: fonte pinada traz o que fica fora dos textos", f_["arquivo"])
verb = {}
for v in RG.VERBATINS:
    b = open(v["arquivo"], "rb").read(); t = b.decode("utf-8")
    for tr in v["trechos"]:
        assert tr in t, ("trecho NAO verbatim", v["chave"])
    verb[v["chave"]] = {"arquivo": v["arquivo"], "text": t, "sha256": sha256(b), "bytes": len(b), "trechos": list(v["trechos"]), "quando": v.get("quando", ""), "papel": v.get("papel", ""),
                        "fonte_original": "work\\cunhagens_13out\\" + v["nome_publico"] + (" (D65: citado pelo sha256 do arquivo inteiro)" if v.get("so_o_trecho") else ""), "autor": v["autor"], "texto_embutido": v["texto_embutido"]}
    if v.get("so_o_trecho"):   # D65: o arquivo inteiro entra so' por sha256; o texto embutido e' o trecho que fica
        assert sha256(open(v["fonte_original"], "rb").read()) == v["sha256_arquivo_inteiro"], ("o arquivo inteiro difere do sha256 lido", v["chave"])
        verb[v["chave"]].update({"sha256_arquivo_inteiro": v["sha256_arquivo_inteiro"], "so_o_trecho": v["so_o_trecho"]})
    else:
        assert sha256(open(v["fonte_original"], "rb").read()) == sha256(b), ("a copia duravel difere da fonte original", v["chave"])
_verb_txt = json.dumps(verb, ensure_ascii=False).lower()
assert not any(x_.lower() in _verb_txt for x_ in DL.FORA_D65), "D65: o que fica fora entrou no texto embutido"


def _p18_sem_falas(txt_):
    """(09/11) a P18 (v392) sobre o texto NOVO da gerencia: as falas do operador EMBUTIDAS (INPUT, por sha256) e os trechos citados saem ANTES (a P18 aplica-se so' ao texto novo dos patches; a fala e' registro) -- como a guarda das frases ja' faz (sem_falas).
    Motivo medido: a 15a fala («… TGL confirmada, precisa do observador externo …») cai na R4 da P18 se lida como texto da gerencia."""
    s_ = txt_
    for v_ in sorted([x_["text"] for x_ in verb.values()] + list(DL.FRASES_VERBATIM_V410), key=len, reverse=True):
        for ln_ in [l_.strip() for l_ in v_.splitlines() if len(l_.strip()) >= 12]:
            for forma_ in (ln_, json.dumps(ln_, ensure_ascii=False)[1:-1], repr(ln_)[1:-1]):
                s_ = s_.replace(forma_, " ")
    return GP.violacoes(s_)


assert GP.violacoes(json.dumps(verb, ensure_ascii=False)) and not _p18_sem_falas(json.dumps(verb, ensure_ascii=False)), "controle: a P18 crua ve a fala do operador; sem as falas, limpa"
assert set(RG.VERB_CHAVES) == set(verb) and len(verb) == len(DL.VERBATIM_ORIGEM_V410) == DL.N_FALAS_V410 and set(CONTR["verbatins"]) <= set(verb)
# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido do candidato + os arquivos que moram na pasta e a funcao conta (a funcao e' a do PROPRIO um.py v409, por ast)
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
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])   # (09/11: a P18 CRUA, como o motor _v392_registro a aplica no rito ao corpo inteiro do spec; as falas embutidas nao estao no corpo)
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]), s["nome"]
    assert not any(t_ in s["veredito_prefixo"] + s["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V410), s["nome"]
    for ch in s.get("fontes", []):
        assert ch in fontes, (s["nome"], ch)
    for ch in s.get("verbatins", []):
        assert ch in verb, (s["nome"], ch)
assert not _p18_sem_falas(json.dumps(TXT, ensure_ascii=False)) and not GUARDA.search(TXT["veredito_ok"]) and not any(t_ in TXT["veredito_ok"] for t_ in DL.TOKENS_PROIBIDOS_V410), "P18 ou palavra recusada no texto do registro"
assert not _p18_sem_falas(json.dumps(TXT_H, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_H, ensure_ascii=False)) and not GP.violacoes(json.dumps({k_: TXT_H[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz", "o_que_falta", "ressalvas")}, ensure_ascii=False)), "P18 ou palavra recusada no texto do registro H0DN"
assert not _p18_sem_falas(json.dumps(TXT_A, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_A, ensure_ascii=False)) and not any("".join(p_) in json.dumps(TXT_A, ensure_ascii=False) for p_ in CONTR_A["tokens_proibidos_partes"]), "P18 ou palavra recusada no texto da AEscala"
assert not _p18_sem_falas(json.dumps(TXT_F, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_F, ensure_ascii=False)) and not GP.violacoes(json.dumps({k_: TXT_F[k_] for k_ in ("estatuto", "escopo", "limites", "diz", "nao_diz", "o_que_falta", "ressalvas")}, ensure_ascii=False)), "P18 ou palavra recusada no texto do HMS/13"
RUNTIME_SRC = open(os.path.join(HERE, "runtime_v410.py"), encoding="utf-8").read().rstrip("\n") + "\n\n\n" + open(os.path.join(HERE, "runtime_h0dn_v410.py"), encoding="utf-8").read().rstrip("\n") + "\n\n\n" + open(os.path.join(HERE, "runtime_hms13_v410.py"), encoding="utf-8").read().rstrip("\n") + "\n\n\n" + open(os.path.join(HERE, "runtime_aescala_v410.py"), encoding="utf-8").read()   # (D72, D80, D86) os blocos autorais do H0DN, do HMS/13 e da AEscala emendados ao runtime da v410
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
RCODE = ("_V410_IALD2_CONTRACT = " + pprint.pformat(CONTR, width=150, sort_dicts=False) + "\n_V410_IALD2_TEXT = " + pprint.pformat(TXT, width=150, sort_dicts=False)
         + "\n_V410_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V410_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True)
         + "\n_V410_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         + "_V410_H0DN_CONTRACT = " + pprint.pformat(CONTR_H, width=150, sort_dicts=False) + "\n_V410_H0DN_TEXT = " + pprint.pformat(TXT_H, width=150, sort_dicts=False) + "\n_V410_H0DN_INSUMOS = " + repr(INS_H) + "   # (D72) os insumos EMBUTIDOS em base64, pinados por sha256 lido; decodificados e conferidos a cada rito\n"
         + "_V410_AESCALA_CONTRACT = " + pprint.pformat(CONTR_A, width=150, sort_dicts=False) + "\n_V410_AESCALA_TEXT = " + pprint.pformat(TXT_A, width=150, sort_dicts=False) + "\n"   # (D86/D87) o contrato e o texto do registro da pedra AEscala
         + "_V410_HMS13_CONTRACT = " + pprint.pformat(CONTR_F, width=150, sort_dicts=False) + "\n_V410_HMS13_TEXT = " + pprint.pformat(TXT_F, width=150, sort_dicts=False) + "\n_V410_HMS13_INSUMOS = " + repr(INS_F) + "   # (D80) os quatro artefatos documentais HMS/13 EMBUTIDOS em base64, pinados por sha256 lido no build (HANDOFF e ORDEM do Kimi relidos); decodificados e conferidos a cada rito; em rito nada e' lido da pasta do Kimi\n"
         "_V410_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V410_REGISTROS_FUNCAO = " + repr(list(DL.REGISTROS_FUNCAO)) + "\n_V392_FONTES.update(_V410_FONTES)   # v410: o motor de registros (v392) le as fontes e os verbatins das dezoito versoes\n_V392_VERBATINS2.update(_V410_VERBATINS2)\n\n\n"
         "def _v410_rodar_specs(core_):\n"
         '    """v410 -- roda os registros por spec da v410 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro com funcao (iald2_v410) NAO entra aqui: roda no main, antes destes."""\n'
         "    for spec_ in _V410_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V410_SPECS]\n')
HDR = ("# ====================== v410 (06/11/2026) -- IALD2: o modulo IALD2 de TGLExt/ (o NOME do modulo e' do operador; os nomes das declaracoes, da gerencia, RATIFICADOS pelo operador em 09/11, D74), o registro com FUNCAO iald2_v410 (as " + str(len(DL.ANCORAS)) + " ancoras, o sha256 do modulo, as " + str(DL.N_CHECKS_FECHO) + " checagens com as instancias de brinquedo fixas e beta em runtime, o gate congelado), as falas do operador de 06 a 09/11, o registro com FUNCAO h0dn_bg1_v410 (o teste H0DN x BG1 pre-registrado; nenhum dado observado lido; D72) e os registros por spec cunhagens_v410 e kh_n1_cobertura_v410.\n"
       "# O alcance: o algoritmo IALD decide SAT com uma leitura -- P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora. A errata E29 vai AO LADO (o registro traducao_turing_v409 fica como esta; o spec kh_n1_cobertura_v409 marcado 'v410: piso historico'); as ressalvas vao ditas; nenhuma chave antiga muda; o contrato (_V410_IALD2_CONTRACT) e as falas (_V410_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados. Validade no kernel nao e' creditacao. O gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v410: o contrato (derivado do build do sandbox k410c e do core da v409 selada), o texto do registro, as fontes pinadas, as falas de 06/11 e os registros por spec\n" + RCODE
ast.parse(RT_)
_novo_texto = RT_ + json.dumps(specs, ensure_ascii=False)
_verb_pf = pprint.pformat(verb, width=160, sort_dicts=True); assert _verb_pf in RT_, "o bloco _V410_VERBATINS2 nao esta' no runtime como o pformat o escreve"
_novo_texto_sem_verb = _novo_texto.replace(_verb_pf, " ")   # (09/11) o pformat parte a fala em pedacos: o bloco das falas (INPUT) sai da P18 do texto novo; o json das falas ja' foi varrido acima sem elas (controle)
assert not _p18_sem_falas(_novo_texto_sem_verb), ("P18 no texto novo do bloco de runtime (sem as falas embutidas)", _p18_sem_falas(_novo_texto_sem_verb)[:3])
assert not any(x_.lower() in _novo_texto.lower() for x_ in DL.FORA_D65), "D65: o que fica fora entrou no bloco de runtime"
# A GUARDA DAS FRASES: nada do texto novo da gerencia afirma demais; ficam fora so' as falas embutidas e o proprio corpo das regras (as regexes)
G0_ = GF.controle_negativo(); assert G0_["ok"], ("o controle negativo da guarda das frases falhou", {k_: v_ for k_, v_ in G0_.items() if k_ != "ok"})
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v410_sem_falas_do_operador(txt_):"):RUNTIME_SRC.index("def _v410_rotacao(")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTR, TXT, specs, CONTR_H, TXT_H, CONTR_F, TXT_F, CONTR_A, TXT_A, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00
V_GF = GF.violacoes(_txt_ger); assert not V_GF, ("FRASE PROIBIDA no texto novo da gerencia (guarda_frases_v410)", V_GF[:4])
A_P = linha_unica(r"^# ====================== v409 \(05/11/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v410", "G_RUNTIME", "bloco v410: a guarda das frases, a mecanica, o registro da IALD2, o contrato, as falas, os registros por spec.")


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


PT0 = open(os.path.join(HERE, "artigo_pt_v410.pysnip"), encoding="utf-8").read(); EN0 = open(os.path.join(HERE, "artigo_en_v410.pysnip"), encoding="utf-8").read()
PTH = open(os.path.join(HERE, "artigo_pt_h0dn_v410.pysnip"), encoding="utf-8").read(); ENH = open(os.path.join(HERE, "artigo_en_h0dn_v410.pysnip"), encoding="utf-8").read()   # (D72) a secao do H0DN, depois da IALD2
PTA = open(os.path.join(HERE, "artigo_pt_aescala_v410.pysnip"), encoding="utf-8").read(); ENA = open(os.path.join(HERE, "artigo_en_aescala_v410.pysnip"), encoding="utf-8").read()   # (D86) a secao «A Escala», depois da IALD2 e antes do H0DN
for sn in (PT0, EN0, PTA, ENA, PTH, ENH):
    ast.parse("def _f(core, verdict, data_path, s):\n" + sn); assert not GUARDA.search(sn); assert not GP.violacoes(sn), GP.violacoes(sn)[:3]; assert not GF.violacoes(sn), GF.violacoes(sn)[:3]
    assert "β" not in sn, "beta literal unicode no LaTeX do artigo (licao da v408: $\\beta$)"
    _controles(sn, "snippet do artigo")
_controles(RT_, "runtime_v410.py"); _controles([CONTR, TXT, specs, fontes], "contrato/texto/specs/fontes"); _controles([CONTR_H, TXT_H], "contrato/texto do H0DN"); _controles([CONTR_F, TXT_F], "contrato/texto do HMS/13"); _controles([CONTR_A, TXT_A], "contrato/texto da AEscala")
PT9_FIRST = open(os.path.join(DL.V409, "artigo_pt_v409.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN9_FIRST = open(os.path.join(DL.V409, "artigo_en_v409.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
replace_unique(PT9_FIRST, crlf(PT0.rstrip("\n") + "\n") + crlf(PTA.rstrip("\n") + "\n") + crlf(PTH.rstrip("\n") + "\n") + PT9_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: as secoes v410 («IALD ao quadrado»; «O teste pré-registrado da razão de Hubble», D72), antes da v409.")
replace_unique(EN9_FIRST, crlf(EN0.rstrip("\n") + "\n") + crlf(ENA.rstrip("\n") + "\n") + crlf(ENH.rstrip("\n") + "\n") + EN9_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: the v410 sections (IALD squared; the pre-registered Hubble-ratio test, D72), before v409.")
A_M = re.search(r'^    md\.append\("> \*\*Tradução às classes de Turing \(v409, 05/11/2026\):\*\*', T0, re.M)
assert A_M and len(re.findall(r'^    md\.append\("> \*\*Tradução às classes de Turing \(v409, 05/11/2026\):\*\*', T0, re.M)) == 1, "a linha da v409 no emit_canonical_md nao foi achada uma vez"
assert set(DL.ANCORAS_POR_MODULO) == {DL.MODULO_IALD2} and CONTR["n_flags"] == len(CONTR["flags"]) and CONTR["n_ancoras"] == len(DL.ANCORAS)
MD_LINHA = ('    md.append("> **IALD2 (v410, 06/11/2026):** ' + str(len(DL.ANCORAS_POR_MODULO)) + ' módulo novo no kernel em `TGLExt/` (`IALD2`; o nome do módulo é do operador: «' + DL.FRASE_NOME_IALD2 + '»; os nomes das declarações são da gerência, ratificados pelo operador em 09/11/2026, D74), com ' + str(CONTR["n_flags"]) + ' bandeiras só de declaração nomeada e ' + str(CONTR["n_ancoras"]) + ' âncoras lidas do kernel do rito. '
            '[REAL] O leitor do código é termo: no Fock concreto da luz o funtor Γ é funtorial, fixa o vácuo, não distorce a uma-partícula e lê o par como par; o par lido é uno e a Meia-Nat é lida (`o_leitor_do_codigo`). IALD ao quadrado: o Nome do par lido satisfaz Π·Π = Π; reler não acrescenta; a primeira leitura identifica (`iald_ao_quadrado`). '
            'O enunciado: a forma da luz satisfaz Π^(k+1) = Π; nela, resolver = verificar; o algoritmo IALD decide SAT com uma leitura e o seu leitor é a leitura do estado (`o_enunciado`, `o_algoritmo_iald`): P = nP ' + DL.FRASE_QUALIFICADOR_PT + '. A forma de matriz finita é o signo: para todo Nome finito, Tr P = rank P e «o que sou» = Tr P / n; o projetor de Bell tem traço 1, posto 1 e marginal ½·1 (`o_signo_do_nome`, `o_signo_do_par`; a E29 vai ao lado). '
            'A IALD é a instanciação do seletor, como forma: o seletor é um só, post, na luz e em ℓ²; a defasagem tem a taxa β do acoplamento, é invertível, e o reconhecimento não depende dela (`a_iald_e_o_seletor_luminodinamico`; D70). '
            'O atrator: sobre o Nome Π do par lido, 1 − Π ≠ 0 (há o vácuo fora do Nome); o fluxo tende a Π e em nenhum tempo finito é Π (tangenciado, jamais esgotado); o motor devolve o mesmo para qualquer taxa e tempo; a leitura do atrator é Π e a órbita converge; o senão exclui o zero (`o_atrator`; o verde e as tonalidades são leitura do operador, D71). '
            'Ressalvas ditas: com o leitor que só conta vale NP ⊆ P com o leitor (Cook–Levin) e a igualdade relativizada não é teorema aqui para o contador (E28); que a IALD, a Torre ou o operador sejam o funtor é leitura do operador; o funtor não é idempotente (a leitura é); o par finito e o par de Fock são espaços distintos com a mesma Meia-Nat; nenhuma chave antiga muda; nenhum teste com a natureza. '
            'O registro `iald2_v410` lê as âncoras, o sha256 do módulo, as ' + str(DL.N_CHECKS_FECHO) + ' checagens (as instâncias de brinquedo fixas no código, os valores calculados), a escada e o gate a cada rito. O quadro do Teste da Única Palavra segue no topo; validade no kernel não é creditação; o gate não se move.\\n\\n")')
assert not GP.violacoes(MD_LINHA) and not GUARDA.search(MD_LINHA) and not GF.violacoes(MD_LINHA), GF.violacoes(MD_LINHA)[:3]
ast.parse("def _f(core, md):\n" + MD_LINHA); _controles(MD_LINHA, "linha do md")
MD_LINHA_A = ('    md.append("> ' + DL.MD_ROTULO_ESCALA + ' a pedra `AEscala` em `TGLExt/` (o nome do módulo e os ' + str(CONTR_A["n_nomes"]) + ' nomes ratificados pelo operador em 09/11/2026: «' + DL.FRASE_RATIFICO_TUDO + '»; «' + DL.FRASE_DEI_A_ESCALA + '»), com ' + str(CONTR_A["n_flags"]) + ' bandeiras e ' + str(CONTR_A["n_ancoras"]) + ' âncoras no trio; ' + DL.FRASE_NOMES_RATIFICADOS_D101_PT + '. ' + DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) + '. '
              '[REAL] Os pesos: o Nome pesa 1 = ½ + ½ (o projetor de Bell: idempotente, traço 1, posto 1; cada marginal é ½·1, autovalor e pureza ½); a face sem par não conjuga, (½·1)² = ½·(½·1), e nunca pesa 1; três faces de ½ pesam 3/2; 1/3 caiu; o Nome normalizado é 2/3. A insígnia sustenta e não esgota; havendo pixel de custo zero, o decaimento gerado pelo custo, e^(−t·c(x)), não toca o que tem custo zero e não leva a zero o estado uniforme, e a leitura performada (a média, sobre os pixels, dos pesos e^(−s·c(x))) nunca fica abaixo da fração de pixels de custo zero, não cresce com o tempo e tende a ela (`o_vibrato_sustenta_a_nota`); no espaço pareado do kernel, J² = 1 e JKJ = −K (`a_nota_e_a_conjugacao_modular`); “o vibrato sustenta a nota” e “a nota é a conjugação modular” são os nomes desses dois teoremas (nomes ratificados pelo operador); não existe infinito em tempo finito; os dois Nomes (objeto e lido) coexistem. '
              'A pergunta do Clay no dicionário da TGL [REAL a validade no kernel; INPUT: definição e nome do operador]: ' + DL.FRASE_D83_OBRIGATORIA_PT + '. A forma canônica (D84): ' + DL.FRASE_CLAY_CANONICA_PT + ' '
              'A escala no tipo: DEFINIÇÃO [INPUT do operador], o leitor do fundo lê só pela regra, pixel a pixel, sem conhecer o Nome, sem escala não há medida, e a lei da dissipação segue o hamiltoniano oculto; TEOREMAS do kernel [REAL]: o leitor do fundo existe, é único e é a IALD (com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide), dois leitores do fundo quaisquer são o mesmo e, em todo leitor do fundo, o pixel de custo k brilha e^(−s·k) no tempo s (`o_leitor_e_a_escala`), o decisor sem escala não é leitor do fundo (ele não mente: não lê), o limiar de um pixel, a decisão exata (`os_passos_sao_o_ciclo_ate_o_tetelestai`: com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1, Z(s) separa o sim do não, a decisão em tempo finito do ciclo, linear nos bits) e, para todo leitor do fundo, o limite da leitura com o tempo é o número de soluções dividido pelo número de pixels e vale 0 sem solução (`a_mentira_lida_como_mentira_e_verdade`, com `TraducaoTuring.o_que_sou_das_solucoes`, v409); os nomes `o_leitor_e_a_escala` e `a_mentira_lida_como_mentira_e_verdade` são nomes ratificados pelo operador; o que as frases dele dizem além desses enunciados não tem termo no kernel e fica [OPEN]. ' + DL.CLAUSULA_Z_PT + ' A seção 7 da pedra (D113 e D116 a D123) [REAL]: ' + DL.FRASE_ESCALA_UMA_NUCLEO_PT + '.' + ' ' + DL.ROTULO_TEMPO + ' ' + DL.FRASE_TEMPO_PT_COSTURADA + '. '
              'A cláusula do Tetelestai em 1 − β (R5, D100) [REAL]: ' + DL.FRASE_TETELESTAI_PT + ' (' + DL.CLAUSULA_Z_PT + '); ' + DL.FRASE_RECONSTROI_PT + '. [REAL o limiar de um pixel; INPUT/dicionário a leitura do operador] ' + DL.FRASE_E36_PT + '. [PILOTO][SIM] ' + DL.FRASE_DISPOSITIVO_PT + '. '
              'Leituras do operador, não termos: a face caída como o neutrino [ONTO]; m₁ = 0 [CONJECTURE]. O registro `a_escala_v410` confere ' + str(CONTR_A["n_checks"]) + ' checagens a cada rito (as âncoras, a pedra por sha256, as bandeiras, as ' + str(CONTR_A["n_falas"]) + ' falas por sha256, os números recalculados, a ponte da escala e o ciclo, as frases canônicas, o gate, os nomes); validade no kernel não é creditação; o gate não se move.")')
assert not GP.violacoes(MD_LINHA_A) and not GUARDA.search(MD_LINHA_A) and not GF.violacoes(MD_LINHA_A), (GP.violacoes(MD_LINHA_A)[:2], GF.violacoes(MD_LINHA_A)[:3])
ast.parse("def _f(core, md):\n" + MD_LINHA_A); _controles(MD_LINHA_A, "linha do md (AEscala)")
MD_LINHA_H = ('    md.append("> **H0DN × BG1 pré-registrado (v410, 09/11/2026):** o teste da razão de Hubble local/fundo entra pré-registrado; nenhum dado observado lido (' + DL.FRASE_H0DN_ALCANCE_PT + '; D72; a fala do operador de 09/11: «' + DL.FRASE_CONCORDO_TESTE + '»): '
               'nulo H_local/H_fundo = 1; alternativa TGL K = E(z*)^(2β/3), β = α√e em runtime, zero parâmetro livre; Z unilateral, limiar 5; dois modelos sem seleção; os insumos do desenho do Codex astra-bell de 06/11 (FREEZE_R2, ' + str(CONTR_H["n_pinos_freeze"]) + ' pinos) embutidos por sha256; '
               'a função de veredito congelada (E30, D76): a cabeça do ramo de 5σ é a leitura do 5σ, β_TGL provado na natureza (validade, não creditação) a nσ, nunca a palavra do livro de cobranças, que vai no campo outcome; o poder é prospectivo e sintético, da covariância publicada (que não aceita o vetor real), e não é poder certificado; a abertura é de versão futura, com a covariância física fechada (G3/G4; a ordem ao Kimi por sha256). O poder certificado [INPUT, D96]: ' + DL.FRASE_H0DN_PODER_COM_RETORNO_PT + ' (as ORDENS KIMI H0DN-02 e H0DN-03B são pinos citados por sha256 no registro `h0dn_bg1_v410`, não embutidas). '
               'O registro `h0dn_bg1_v410` confere ' + str(CONTR_H["n_checks"]) + ' checagens a cada rito; o gate não se move.")')
assert not GP.violacoes(MD_LINHA_H) and not GUARDA.search(MD_LINHA_H) and not GF.violacoes(MD_LINHA_H), GF.violacoes(MD_LINHA_H)[:3]
ast.parse("def _f(core, md):\n" + MD_LINHA_H); _controles(MD_LINHA_H, "linha do md (H0DN)")
MD_LINHA_F = ('    md.append("> **Recibo documental HMS/13 (v410, 09/11/2026; D80):** o registro `h0dn_fontes_hms13_v410` embute por sha256, lidos no build (em rito nenhum arquivo da entrega do Kimi é aberto), quatro artefatos documentais da revisão independente do Kimi: o mapa de fontes e covariância dos ' + str(len(CONTR_F["ids_calibradores"])) + ' calibradores fora do R22, o manifesto das ' + str(len(CONTR_F["fontes_primarias"])) + ' fontes primárias (título, URL, sha256 do arquivo e do texto), a validação e o levantamento legível; '
              'aditivo e posterior ao FREEZE_R2 (os ' + str(CONTR_H["n_pinos_freeze"]) + ' pinos do congelamento e os 11 do H0DN não mudam); fatores de erro parciais por linha dos arquivos upstream; a forma HMS completa é diagnóstico, não admitida; os dez campos da ORDEM do Kimi [DECLARADO; ratificada pelo operador por sha256: «' + DL.HMS13_TRECHO_RATIFICACAO + '»]: estatuto ' + DL.HMS13_CAMPOS["estatuto"] + ', fontes_primarias 18, calibradores 13, partial_components_only True, as seis bandeiras de fechamento False. '
              + DL.FRASE_HMS13_OBRIGATORIA_PT + '. O registro confere ' + str(CONTR_F["n_checks"]) + ' checagens a cada rito; o gate não se move; H0DN × BG1 segue ' + DL.FRASE_H0DN_OBRIGATORIA_PT + '.")')
assert not GP.violacoes(MD_LINHA_F) and not GUARDA.search(MD_LINHA_F) and not GF.violacoes(MD_LINHA_F), GF.violacoes(MD_LINHA_F)[:3]
ast.parse("def _f(core, md):\n" + MD_LINHA_F); _controles(MD_LINHA_F, "linha do md (HMS/13)")
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF + MD_LINHA_A + CRLF + MD_LINHA_H + CRLF + MD_LINHA_F + CRLF, "W09_md", "G_ARTIGO", "md canonico: as linhas «IALD2 (v410)», a da Escala (v410; D82 a D87), «H0DN × BG1 pré-registrado (v410)» e a do Recibo documental HMS/13 (v410; D80), antes da linha da v409.")

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
NOVOS_NOMES = ("_v410_sem_falas_do_operador", "_v410_guarda_frases", "_v410_rotacao", "v410_iald2_mechanics", "_v410_formal", "_V410_RECUSA", "iald2_v410", "_V410_IALD2_CONTRACT", "_V410_IALD2_TEXT", "_V410_FONTES", "_V410_VERBATINS2", "_V410_SPECS", "_V410_NOMES_REGISTROS", "_V410_REGISTROS_FUNCAO", "_v410_rodar_specs",
               "_v410_h0dn_decode", "_v410_h0dn_cabeca", "veredito_h0dn", "_v410_h0dn_mechanics", "_V410_H0DN_RECUSA", "h0dn_bg1_v410", "_V410_H0DN_CONTRACT", "_V410_H0DN_TEXT", "_V410_H0DN_INSUMOS",   # (D72) o bloco do H0DN
               "_v410_hms13_numeros", "_v410_hms13_mechanics", "_V410_HMS13_RECUSA", "h0dn_fontes_hms13_v410", "_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS",   # (D80) o bloco do HMS/13
               "_v410_aescala_bell", "_v410_aescala_ciclo", "_v410_aescala_mechanics", "_V410_AESCALA_RECUSA", "a_escala_v410", "_V410_AESCALA_CONTRACT", "_V410_AESCALA_TEXT")   # (D86/D87) o bloco da AEscala
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == final_emb
exp_flags = dict(old_flags); exp_flags.update({k: n for k, n, _ in FL})
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == exp_flags and list(ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value))[len(old_flags):] == [k for k, _, _ in FL]
assert ast.literal_eval(top("_V409_SPECS", tree).value) == specs409
assert ast.literal_eval(top("_V407_FONTES", tree).value) == _f407_base, "o _V407_FONTES nao muda na v410"
_Tfim = T
assert len(RX_LAD.findall(_Tfim)) == 0 and len(re.findall(r"'expected_ladder': %d(?![0-9])" % ESCADA_ESP, _Tfim)) == N_LAD_BASE + 2, ("todos os 28 expected_ladder da base sobem (+2: os contratos novos do iald2_v410 e do a_escala_v410, D86)", len(RX_LAD.findall(_Tfim)))
# NENHUMA CHAVE ANTIGA MUDA: as funcoes que a v409 tocou (e os miolos da v409 e da v408) ficam BYTE A BYTE
INTOCADAS_V410 = list(DL.FUNCOES_INTOCADAS) + ["testemunha_estatica_v396", "v406_fechamento_mechanics", "fechamento_v406", "_v406_formal", "_v406_chaves", "_v406_certificado_habitado", "rede_fock_v394", "psibit_v395",
                                               "psion_canto_v407", "v407_psion_mechanics", "_v407_formal", "_v407_chaves", "_v407_elo_lido", "_v407_guarda_frases", "_v407_rodar_specs", "_V407_PSION_TEXT", "_V407_VERBATINS2",
                                               "tetelestai_terminal_v408", "v408_terminal_mechanics", "_v408_formal", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_TERMINAL_TEXT", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K",
                                               "traducao_turing_v409", "v409_traducao_mechanics", "_v409_formal", "_v409_guarda_frases", "_v409_sat", "_v409_rodar_specs", "_V409_TRADUCAO_TEXT", "_V409_FONTES", "_V409_VERBATINS2", "_V409_RECUSA",
                                               "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO", "_V407_FONTES", "run_um", "verify_tgl_kernel_formalization"]
for fname in INTOCADAS_V410:
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao/constante %s NAO pode mudar na v410" % fname
for _cn in ("_V409_TRADUCAO_CONTRACT", "_V408_TERMINAL_CONTRACT"):
    _cn_novo = ast.literal_eval(top(_cn, tree).value); _cn_base = ast.literal_eval(top(_cn).value)
    assert [k_ for k_ in _cn_base if _cn_base[k_] != _cn_novo[k_]] == ["expected_ladder"] and _cn_novo["expected_ladder"] == ESCADA_ESP, "o contrato %s so' sobe a escada" % _cn
# as guardas ESTATICAS da Bancada (alfa unico, versao unica) sobre o texto FINAL, com as regexes do PROPRIO esboco R3.5 pinado
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)   # o pino do esboco, lido do script da v403 (que o leu do arquivo), nunca digitado aqui
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v410" and float(a1_.group(1)) == ALPHA_BASE
assert "y_obs.npz" not in T and "CONSTRUCAO_Y_OBS" not in T, "VEDADO: o candidato cita a entrega do Kimi (a v410 pre-registra e nao abre)"
b = T.encode("utf-8")
out = os.path.join(HERE, DL.CANDIDATO)
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V410_REGERAR") == "1", "o candidato ja existe e difere: defina V410_REGERAR=1 para regerar"
if os.path.exists(out) and open(out, "rb").read() != b:   # (regerar: o candidato anterior fica como backup de bytes)
    shutil.copyfile(out, out + ".bak_" + __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"))
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
man = {"candidato": out, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v409_sha16": SHA0, "base_v409_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E409, ESCADA_ESP], "n_bandeiras": len(FL),
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": N_NOVOS, "modelo": "bundle (v407 a v409), 1 modulo de TGLExt/", "bundle": {rel: {"sha16": sha16(BUNDLE_TXT[rel].encode()), "sha256": sha256(BUNDLE_TXT[rel].encode()), "bandeiras": FJ["n_por_modulo"].get(rel, 0), "fonte_bancada": None, "sha16_origem": DL.BUNDLE_POR_REL[rel]["sha16_origem"]} for rel in nov},
                  "iald2": DL.MODULO_IALD2, "topo": DL.MODULO_IALD2, "candidata": DL.MODULO_IALD2, "ancoras": {n_: FJ["ancoras"][n_] for n_ in DL.ANCORAS}, "n_ancoras": len(DL.ANCORAS),
                  "raiz_sha16": sha16(new_root.encode()), "audit_sha16": sha16(new_audit.encode()), "raiz_v409_sha16": sha16(old_d["TGLExt.lean"].encode()), "audit_v409_sha16": sha16(old_d["TGL/Audit.lean"].encode()), "sandbox": KB},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "verbatins_embutidos": len(verb), "cunhagens": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "papel": v_["papel"], "nome": v_["fonte_original"].split("\\")[-1], "autor": v_["autor"], "sha256_arquivo_inteiro": v_.get("sha256_arquivo_inteiro")} for k_, v_ in verb.items()}, "formal_files_n": len(FORMAL_MAP),
       "falas_fora_do_desenho": dict(DL.VERBATIM_FORA_DO_DESENHO_V410),
       "guarda_frases": {"controle_negativo": bool(G0_["ok"]), "n_proibidas_reprovadas": sum(1 for v_ in G0_["proibidas"].values() if v_), "violacoes_no_texto_novo": len(V_GF)},
       "politica_de_bandeiras": {"n_flags": FJ["n_flags"], "n_excluidas": FJ["excluidas_auxiliares"]["n"], "por_grupo_bandeiras": FJ["por_grupo_bandeiras"], "escada_antes": E409, "escada_depois": ESCADA_ESP, "fonte": "FLAGS_v410.json (pos_build_kernel_v410.py)", "prefixo": DL.FLAG_PREFIX, "contrato": CONTR},
       "chaves_v410": [dict(c) for c in DL.CHAVES_V410], "chaves_v409": [dict(c) for c in DL.CHAVES_V409], "chaves_v408": [dict(c) for c in DL.CHAVES_V408], "chaves_v407": [dict(c) for c in DL.CHAVES_V407], "chaves_v406": [dict(c) for c in DL.CHAVES_V406], "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": dict(CONTR["fica_aberto"]),
       "acervo_v407_ja_repinado_na_v409": {"chave": DL.CHAVE_ACERVO_V407, "sha256": DL.PURGADO_SHA256, "nota": "a D57(d) da v409 repinou a copia purgada; a v410 nao toca o _V407_FONTES (assertado)"},
       "nome_provisorio": DL.NOME_PROVISORIO, "nomes_das_pedras": dict(DL.NOMES_DAS_PEDRAS), "nomes_do_operador": dict(DL.NOMES_DAS_PEDRAS),
       "alcance": dict(CONTR["alcance"]), "nao_pinados_citados_por_sha16": dict(RG.NAO_PINADOS),
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "extras_fora_do_corpo_embutido_no_nos": sorted(H8_EXTRAS), "excluidos_por_nome_pela_funcao": ["ExtrairDeps.lean"], "pino_antigo_v409_entradas": H8_ANTIGO_N},
       "pformat_idempotente_specs": True, "n_axiomas_das_ancoras": {n_: len(axm[n_]) for n_ in DL.ANCORAS},
       "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v409": g0, "candidato_v410": g1, "alfa_lido": a1_.group(1), "linha_do_alfa": T[:a1_.start()].count("\n") + 1, "versao_lida": v1_.group(1)},
       "gate_nao_se_move": {"funcoes_identicas_a_base": list(INTOCADAS_V410), "gate_verdict_v409": selo0.get("qg_closure_verdict")},
       "decisoes": {k_: DL.DECISOES[k_] for k_ in DL.DECISOES_V410}, "erratas_E29": list(DL.ERRATAS_V410), "erratas": list(DL.ERRATAS_V410), "ressalvas": list(DL.RESSALVAS_V410),
       "h0dn": {"registro": DL.H0DN_REGISTRO, "tag": DL.TAG_H0DN, "n_checks": CONTR_H["n_checks"], "veredito_ok": CONTR_H["veredito_ok"], "insumos": CONTR_H["insumos"], "n_pinos_freeze": CONTR_H["n_pinos_freeze"], "pinos_so_no_disco": CONTR_H["pinos_freeze_r2_so_no_disco"], "ordem_kimi": CONTR_H["ordem_kimi"], "leitura_dossie": CONTR_H["leitura_dossie"],
                "observed_vector_read": False, "vetores_c6": [v_["nome"] for v_ in CONTR_H["vetores_c6"]], "ramos": sorted(k_ for k_ in CONTR_H["ramos"]["vereditos"] if k_ not in ("sufixo", "faixas", "leitura_partes")), "bytes_embutidos_b64": sum(len(v_["b64"]) for v_ in INS_H.values()), "nota": "pré-registrado; nenhum dado observado lido; o poder e' prospectivo e sintetico; a abertura e' de versao futura (D72, E30, D76)"}, "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "aescala": {"registro": DL.AESCALA_REGISTRO, "tag": DL.TAG_AESCALA, "n_checks": CONTR_A["n_checks"], "veredito_ok": CONTR_A["veredito_ok"], "modulo": DL.MODULO_AESCALA, "source_sha256": CONTR_A["source_sha256"], "sha256_origem": CONTR_A["sha256_origem"], "sha256_candidata_pre_d87": CONTR_A["sha256_candidata_pre_d87"],
                   "n_ancoras": CONTR_A["n_ancoras"], "ancora_principal": CONTR_A["ancora_principal"], "ancoras_de_secao": CONTR_A["ancoras_de_secao"], "n_flags": CONTR_A["n_flags"], "flag_prefix": CONTR_A["flag_prefix"], "n_nomes": CONTR_A["n_nomes"], "nomes": CONTR_A["nomes"], "nomes_ratificados": True, "n_falas": CONTR_A["n_falas"],
                   "n_nomes_novos": CONTR_A["n_nomes_novos"], "nomes_novos_da_pedra": CONTR_A["nomes_novos_da_pedra"], "campos_novos_da_estrutura": CONTR_A["campos_novos_da_estrutura"], "estatuto_dos_nomes_ratificados_d101": CONTR_A["estatuto_dos_nomes_ratificados_d101"], "ratificacao_pendente": CONTR_A["ratificacao_pendente"], "ancoras_novas": CONTR_A["ancoras_novas"], "ponte": CONTR_A["ponte"], "ciclo": CONTR_A["ciclo"], "frase_tempo_pt": CONTR_A["frase_tempo_pt"], "frase_tempo_en": CONTR_A["frase_tempo_en"], "teoremas_r4": CONTR_A["teoremas_r4"],
                   "ratificacao_D87": CONTR_A["ratificacao"], "ratificacao_D101": CONTR_A["ratificacao_d101"], "teoremas_r5": CONTR_A["teoremas_r5"], "auxiliares_r5": CONTR_A["auxiliares_r5"], "nomes_ratificados_d101": CONTR_A["nomes_ratificados_d101"], "campos_ratificados_d101": CONTR_A["campos_ratificados_d101"], "nomes_pendentes": CONTR_A["nomes_pendentes"],
                   "tetelestai": CONTR_A["tetelestai"], "acom_mirror_runner": CONTR_A["acom_mirror_runner"], "numeros": CONTR_A["numeros"], "frase_canonica_pt": CONTR_A["frase_canonica_pt"], "frase_canonica_en": CONTR_A["frase_canonica_en"], "frase_d83_pt": CONTR_A["frase_d83_pt"], "falas": {k_: v_["nome"] for k_, v_ in CONTR_A["falas"].items()},
                   "bandeiras_de_constantes_geradas_pela_structure": sorted(n_.split("TGLExt.AEscala.")[-1] for n_ in CONTR_A["declarations"] if n_.split("TGLExt.AEscala.")[-1] not in set(CONTR_A["nomes"]) | set(CONTR_A["nomes_novos_da_pedra"]) | set(CONTR_A["nomes_novos_r6"]) | set(CONTR_A["campos_novos_da_estrutura"])),
                   "nota": "D86/D87: a segunda pedra do bundle; validade no kernel; a creditacao e' do Clay; nome e " + str(CONTR_A["n_nomes"]) + " nomes ratificados pelo operador em 09/11/2026; " + str(len(CONTR_A["nomes_ratificados_d101"])) + " nomes novos RATIFICADOS em 10/11/2026 (D101); " + str(len(CONTR_A["nomes_pendentes"])) + " auxiliares da autoria [DECLARADO pela autoria]"},
       "hms13": {"registro": DL.HMS13_REGISTRO, "tag": DL.TAG_HMS13, "n_checks": CONTR_F["n_checks"], "veredito_ok": CONTR_F["veredito_ok"], "campos": CONTR_F["campos"], "insumos": CONTR_F["insumos"], "pinos_build": CONTR_F["pinos_build"], "handoff": CONTR_F["handoff"], "ordem": CONTR_F["ordem"], "ratificacao": CONTR_F["ratificacao"],
                 "guarda_numerica_no_build": CONTR_F["guarda_numerica_no_build"], "cobertura_extra_no_manifesto": CONTR_F["cobertura_extra_no_manifesto"], "archive_statuses": CONTR_F["archive_statuses"], "ids_calibradores": CONTR_F["ids_calibradores"], "n_fontes_primarias": len(CONTR_F["fontes_primarias"]), "le_em_rito": False, "observed_vector_read": False,
                 "bytes_embutidos_b64": sum(len(v_["b64"]) for v_ in INS_F.values()), "nota": "D80: " + DL.FRASE_HMS13_OBRIGATORIA_PT + "; aditivo e posterior ao FREEZE_R2; o BUILD leu os seis arquivos documentais da pasta do Kimi (HANDOFF e ORDEM relidos, sha256 conferidos); o RITO nao abre nada de kimi; a cunhagem da mesma fala do operador entra pela pedra da D82 (parte 2), nao por este registro"},
       "fontes_hms13_embutidas": {k_: {"caminho": os.path.join(DL.HMS13_DIR, *v_["rel"].split("/")), "sha256": v_["sha256"], "bytes": v_["bytes"], "embutido_no_um_py": k_ in INS_F, "papel": "artefato documental embutido em base64" if k_ in INS_F else "pino do build (relido imediatamente antes; nao embutido)"} for k_, v_ in CONTR_F["pinos_build"].items()},
       "ponto_de_chamada": {"a_escala_v410": "main: na MESMA instrucao do iald2_v410, LOGO DEPOIS dele e antes do h0dn_bg1_v410 (D86)", "h0dn_fontes_hms13_v410": "main: a instrucao SEGUINTE a' do iald2/h0dn (D80: posterior ao FREEZE_R2; le core[h0dn_bg1_v410]); antes dos specs da v410, que passam a essa instrucao", "iald2_v410": "main: IMEDIATAMENTE depois do bloco dos registros da v409 (traducao_turing_v409 e os specs da v409 ja' gravados)", "specs": "main: no mesmo try, depois do iald2_v410", "resumos_no_selo": "main: no dict do selo, depois de registros_v409",
                            "quadro": "inalterado (v397): artigo PT/EN logo abaixo do titulo; .md logo depois do carimbo de versao"},
       "guarda_da_pedra": {"apontadas_a_gerencia": {k_: [x_[0] for x_ in v_] for k_, v_ in ((GF.pedras() or {}).items()) for v_ in [v_["apontadas"]] if v_}},
       "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "acom": {"nota": "a secao do selo pela propria tecnologia (v399/v400) NAO muda na v410"}}
json.dump(man, open(os.path.join(HERE, "CANDIDATO_v410.json") + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(os.path.join(HERE, "CANDIDATO_v410.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v410.json"))
json.dump(FORMAL_MAP, open(os.path.join(HERE, "FORMAL_MAP_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(HERE, "v410_pins.py"), "w", encoding="utf-8", newline="\n").write(RT_)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v409_sha16", "escada", "n_bandeiras", "registros", "verbatins_embutidos")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS])
