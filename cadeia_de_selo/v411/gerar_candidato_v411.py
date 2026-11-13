# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] reescrito do molde gerar_candidato_v410.py para uma versao SEM modulo novo: o registro com funcao h0dn_bg1_v411, os specs da v411 e o topo do artigo
"""gerar_candidato_v411.py -- gera o um.py CANDIDATO v411 a partir da v410 SELADA (base_v410; o Nos e' so' conferido, NUNCA escrito). claude-construtor-v411, a servico da gerencia c1, 12/11/2026. Molde: gerar_candidato_v410.py.
Conteudo (DESENHO_v411; a ordem do operador de 12/11/2026 (D169), o testemunho e a ordem do topo (D170): so' CITADOS por data e sha256, lidos do arquivo da casa, nunca transcritos; D181):
 (A) kernel: NENHUM modulo novo; o embutido _EMBEDDED_KERNEL_FILES fica BYTE A BYTE e e' conferido contra o sandbox C:\\t\\k411c\\final (copia do k410c; build incremental sem compilar nada e Audit com o log da v410);
 (B) bandeiras e escada: nenhuma nova (escada 12308, lida do core da base); UM_VERSION = v411;
 (C) _V410_SPECS: kh_n1_cobertura_v410 passa a piso (h2, h3, h6, h8) com errata; nenhuma outra checagem muda; NENHUMA chave antiga muda de literal; os quatro registros com funcao da v410 ficam BYTE A BYTE (assertado);
 (D) runtime novo (quadro_v411.py + runtime_h0dn_v411.py): o registro com FUNCAO h0dn_bg1_v411 (16 checagens; o resultado da abertura RECALCULADO a partir dos bytes embutidos), o quadro do topo, a secao, a linha do .md,
     as falas de 11 e 12/11 por sha256 e os specs cunhagens_v411 e kh_n1_cobertura_v411; chamadas no main DEPOIS do bloco da v410 (h0dn_fontes_hms13_v410); resumos no selo;
 (E) artigo: o quadro novo ACIMA do quadro “O Teste da Unica Palavra” (que fica, com uma linha de remissao), o paragrafo de apresentacao ABRE com o texto RATIFICADO do topo (TOPO_RATIFICADO_v411.json, da gerencia;
     SEM ELE O CANDIDATO NAO E' GERADO) e duas trocas ditas (a remissao da tensao de Hubble e a frase dos efeitos de beta; tambem no paragrafo “O metodo”); a frase AO LADO do “estatuto da prova (v391)” e do “coracao”;
     a secao “O teste decisivo” PT/EN antes da secao da v410; a linha do .md antes das da v410.
 O gate NAO muda: as funcoes do gate/neutrino e os registros anteriores ficam BYTE A BYTE (assertado). REGRA DOS PATCHES: cada ancora textual ocorre EXATAMENTE uma vez na base (senao a geracao PARA e diz a contagem).
uso: python -B -X utf8 gerar_candidato_v411.py            (exige TOPO_RATIFICADO_v411.json; recusa -O; nunca escreve no Nos)
     V411_ENSAIO_TOPO_PROPOSTO=1 python -B -X utf8 gerar_candidato_v411.py   (ENSAIO do topo proposto, ordem da gerencia de 12/11: o texto PROPOSTO do DESENHO 5.1 b com TODAS as guardas ESTRITAS; grava o ARTEFATO DE ENSAIO
        um_v411_ENSAIO_TOPO_PROPOSTO.py e o manifesto dele SO' em C:\\t\\k411c\\ensaio_topo_proposto, fora de work; NUNCA e' candidato, nao se instala, o hash nao entra na pasta da cadeia)
     python -B -X utf8 gerar_candidato_v411.py --prevoo   (PRE-VOO: o texto PROPOSTO do DESENHO 5.1 b no lugar do ratificado, marcado; roda TODAS as assercoes e as guardas e grava so' PREVOO_GERADOR_v411.json; NAO grava candidato)"""
import ast, datetime, hashlib, json, math, os, pprint, re, shutil, sys
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PREVOO = "--prevoo" in sys.argv
import delta_v411 as DL  # noqa: E402
import registros_v411 as RG  # noqa: E402
import registros_h0dn_v411 as RH  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
import acom_conferencias_v411 as AC  # noqa: E402
CRLF = "\r\n"
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX
sha256 = lambda b: hashlib.sha256(b).hexdigest(); sha16 = lambda b: sha256(b)[:16]
GUARDA = re.compile(r"(?<!NOT_)(?<!UN)CONF" + r"IRMED|(?<!AP)PRO" + r"VED_BY|TGL_PRO" + r"VED")
ESP410 = json.load(open(os.path.join(DL.V410, "ESPERADOS_v410.json"), encoding="utf-8"))
NOS = DL.NOS; BASE = os.path.join(HERE, DL.BASE_DIR)
if sha16(open(os.path.join(NOS, "um.py"), "rb").read()) != ESP410["candidato_sha16"]:   # o Nos ja nao e' a v410 (rito v411 em curso): a v410 SELADA vem da copia base_v410
    NOS = BASE
raw = open(os.path.join(NOS, "um.py"), "rb").read()
selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); assert selo0.get("um_version") == DL.BASE_VERSION
assert sha256(raw) == selo0["sha256"]["um.py"], "o canonico no Nos nao e' a v410 selada"
SHA0 = sha16(raw); assert SHA0 == ESP410["candidato_sha16"] == DL.BASE_SHA16_DA_ORDEM
assert raw == open(os.path.join(BASE, "um.py"), "rb").read(), "a base copiada difere do canonico lido"
core0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
E410 = int(core0["external_ladder"]["n_theorems_expected"]); assert int(core0["external_ladder"]["n_theorems_clean"]) == E410 == ESP410["escada"][1], (E410, ESP410["escada"])
T0 = raw.decode("utf-8")
tree0 = ast.parse(T0)
LS = [0] + [m.end() for m in re.finditer("\n", T0)]
LF_SOLTOS0 = len(re.findall(r"(?<!\r)\n", T0))


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


EDITS = []


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


def _controles(obj, onde):
    if isinstance(obj, str):
        ruins = sorted({hex(ord(c)) for c in obj if ord(c) < 32 and c not in "\n\r"})
        assert not ruins, ("caractere de controle em texto novo", onde, ruins, repr(obj[:80]))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            _controles(k, onde); _controles(v, onde)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _controles(v, onde)


# ---------------- (0) o TOPO (DESENHO 5.1 b): o texto ratificado pela gerencia, ou (so' no pre-voo) a proposta, marcada ----------------
_m_prop = {"pt": re.search(r"^> PT — “(.+)”$", DL._S5, re.M), "en": re.search(r"^> EN — “(.+)”$", DL._S5, re.M)}
assert _m_prop["pt"] and _m_prop["en"], "a proposta do topo nao foi achada no DESENHO 5.1 b"
ENSAIO = DL.ENSAIO_TOPO_PROPOSTO
assert not (ENSAIO and PREVOO), "o pre-voo e o ensaio do topo proposto sao modos distintos"
if ENSAIO:
    TOPO = {"pt": _m_prop["pt"].group(1), "en": _m_prop["en"].group(1), "ratificado": False, "arquivo": None, "sha256": None, "nota": "ENSAIO do topo proposto (ordem da gerencia de 12/11): o texto PROPOSTO pela gerencia no DESENHO 5.1 b, PENDENTE da palavra do operador; o artefato NAO e' candidato e fica fora de work"}
elif os.path.exists(DL.TOPO_RATIFICADO_ARQ):
    _tb = open(DL.TOPO_RATIFICADO_ARQ, "rb").read(); _tj = json.loads(_tb.decode("utf-8"))
    TOPO = {"pt": str(_tj["pt"]), "en": str(_tj["en"]), "ratificado": True, "arquivo": DL.TOPO_RATIFICADO_ARQ, "sha256": sha256(_tb), "bytes": len(_tb), "extras_do_arquivo": sorted(k_ for k_ in _tj if k_ not in ("pt", "en"))}
elif PREVOO:
    TOPO = {"pt": _m_prop["pt"].group(1), "en": _m_prop["en"].group(1), "ratificado": False, "arquivo": None, "sha256": None, "nota": "PRE-VOO: o texto PROPOSTO pela gerencia no DESENHO 5.1 b, PENDENTE da palavra do operador; nenhum candidato e' gravado"}
else:
    raise SystemExit("RECUSO: TOPO_RATIFICADO_v411.json ausente (DESENHO_v411 5.1 b e secao 8: sem a palavra do operador sobre o texto do topo o candidato NAO e' gerado). Use --prevoo para o pre-voo.")
# (D172/D173) os marcadores do topo sao DIRIGIDOS pela tabela `marcadores` do TOPO_RATIFICADO_v411.json (doze; a fonte de maquina de cada um em DL.MARCADORES_V411); no pre-voo e no ensaio do topo PROPOSTO, os quatro
# de antes (a proposta do DESENHO 5.1 b so' traz esses). Todo marcador do texto tem de estar na tabela; marcador fora dela = PARAR.
_TAB_MK = (DL.MARCADORES_V411 if TOPO["ratificado"] else {k_: v_ for k_, v_ in DL.MARCADORES_V411.items() if k_ in re.findall("⟨[^⟩]*⟩", TOPO["pt"])}) if DL.MARCADORES_V411 else None
assert _TAB_MK, "a tabela de marcadores do topo nao foi lida: PARAR"
_LIVRO = {"caminho": ["estatuto_da_prova_v391", "prova_2_ritos"], "categorias": ["NOT_FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING"], "frases_pt": ["nenhuma foi falsificada", "nenhuma falsificada"],
          "frases_en": ["none was falsified", "none falsified"], "regra": "a frase de que nenhuma cobranca foi falsificada so' sai com falsificadas == 0 e a soma das categorias + as falsificadas == n_cobrancas (D173; regra do TOPO_RATIFICADO_v411.json); o H0DN nao entra no livro"}
if TOPO["ratificado"]:
    assert all(any(c_ in r_ for r_ in DL.REGRAS_DO_TOPO_V411) for c_ in ("falsificadas == 0", "soma das quatro categorias", "NÃO entra na contagem do livro", "F65")), "as regras do topo ratificado nao sao as que o gerador cumpre: PARAR"
    _cats = [re.search(r"ledger\.([A-Z_]+)$", ".".join(v_["caminho"])) for v_ in _TAB_MK.values()]
    assert sorted(m_.group(1) for m_ in _cats if m_) == sorted(_LIVRO["categorias"]), "as quatro categorias do livro na tabela nao sao as do fail-closed: PARAR"
    _p2r = core0["estatuto_da_prova_v391"]["prova_2_ritos"]; _led = _p2r["ledger"]
    assert _p2r["falsificadas"] == 0 == _led.get("FALSIFIED", 0) and sum(_led[c_] for c_ in _LIVRO["categorias"]) + _led.get("FALSIFIED", 0) == _p2r["n_cobrancas"], "o livro da base nao sustenta a frase do acrescimo: PARAR"
    _V397N = ast.literal_eval(top("_V397_CHAVES_NUM").value)
    assert all(v_["caminho"][-1] in _V397N for v_ in _TAB_MK.values() if v_["caminho"][0] == "teste_de_veracidade_fase9_v397"), "a Fase 9 V2 da tabela nao e' lida pelas chaves do quadro da v397: PARAR"
_MK = {"pt": list(_TAB_MK), "en": [v_["en"] for v_ in _TAB_MK.values()]}
for _lg in ("pt", "en"):
    _no_texto = re.findall("⟨[^⟩]*⟩", TOPO[_lg])
    assert _no_texto and set(_no_texto) <= set(_MK[_lg]) and set(_MK[_lg]) <= set(_no_texto), ("marcador do topo fora da tabela, ou da tabela fora do texto: PARAR", _lg, sorted(set(_no_texto) ^ set(_MK[_lg])))
    assert not re.search(r"(?<![0-9])\d+[,.]\d{2}\b", re.sub("⟨[^⟩]*⟩", "", TOPO[_lg])), ("numero digitado no texto do topo (os numeros sao do core)", _lg)
    _v_topo = GF.violacoes(TOPO[_lg].replace("⟨n⟩", "6").replace("⟨", "").replace("⟩", "6,1"))
    assert not _v_topo or PREVOO, ("o texto do topo reprova na guarda de frases da v411", _lg, _v_topo[:3])
TOPO_GUARDA = {_lg: GF.violacoes(TOPO[_lg].replace("⟨n⟩", "6").replace("⟨", "").replace("⟩", "6,1")) for _lg in ("pt", "en")}
TOPO_P18 = {_lg: GF.p18(TOPO[_lg]) for _lg in ("pt", "en")}

# ---------------- (1) o kernel: NENHUM modulo novo; o embutido fica byte a byte e e' o do sandbox ----------------
rd = lambda p: open(p, "r", encoding="utf-8", newline="").read()
dnode = top("_EMBEDDED_KERNEL_FILES").value
old_d = ast.literal_eval(dnode)
_dif_sb = [rel for rel, txt in old_d.items() if not os.path.exists(os.path.join(KB, *rel.split("/"))) or rd(os.path.join(KB, *rel.split("/"))) != txt]
assert not _dif_sb, ("o kernel EMBUTIDO da base difere do sandbox k411c (a v411 nao tem modulo novo: tem de ser identico)", _dif_sb[:5])
FJ = json.load(open(os.path.join(KD, "FLAGS_v411.json"), encoding="utf-8")); assert FJ["n_flags"] == 0 and not FJ["flags"], "a v411 nao tem bandeira nova"
POSB = json.load(open(os.path.join(KD, "POS_BUILD_v411.json"), encoding="utf-8")); assert POSB["ok"] is True and POSB["n_modulos_compilados"] == 0 and POSB["escada"] == [E410, E410]
FORMAL_MAP = {k: sha256(v.encode("utf-8")) for k, v in old_d.items()}
ESCADA_ESP = E410
fn_ladder = top("prove_external_ladder"); lad = [n for n in fn_ladder.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "ext_flags" for t in n.targets)]; assert len(lad) == 1
assert len(ast.literal_eval(lad[0].value)) == E410, "a escada da base nao e' a do core"
m = re.search(r'^UM_VERSION = "v410"   # v410 \(06 e 09/11/2026\): [^\r\n]*' + CRLF, T0, re.M); assert m and len(re.findall(r'^UM_VERSION[ \t]*=', T0, re.M)) == 1
_hist = re.search(r"; (v409 em 05/11 \(a traducao as classes de Turing e o par na face de Fock\);[^\r\n]*)$", m.group(0).rstrip("\r\n")); assert _hist, "o historico de versoes na linha UM_VERSION da base nao esta' como esperado"
LINHA_V = ('UM_VERSION = "v411"   # v411 (12/11/2026): a CONSTANTE UNICA de versao -- o teste H0DN x BG1 da razao de Hubble local/fundo ABERTO uma vez, depois do commit publico do pre-registro (D169); a emenda da regra (D162) e o resultado '
           'RECALCULADO no rito a partir dos bytes embutidos; o primario sob o modelo de erros publicado e, ao lado, as Cefeidas livres, sempre juntos; retrodicao sem ajuste, emenda posterior a guarda, teste nao cego; '
           'provado e\' validade, nao creditacao; nenhum modulo novo no kernel (escada %d); nenhuma chave antiga muda; as ordens do operador de 11 e 12/11 citadas por data e sha256, nao transcritas (D181); o gate nao se move; '
           'v410 em 06 e 09/11 (IALD2, A Escala e o H0DN pre-registrado); ' % E410) + _hist.group(1)
edit(m.start(), m.end(), LINHA_V + CRLF, "W01_versao", "G_MEMORIA", "UM_VERSION = 'v411'.")

# ---------------- (2) _V410_SPECS: kh_n1_cobertura_v410 -> pisos (h2/h3/h6/h8) com errata; cunhagens_v410 nao muda ----------------
import guarda_p18_v411 as GP  # noqa: E402


def _spec_block(nome_var):
    sv_ = top(nome_var); a_, b_ = span(sv_.value); seg_ = T0[a_:b_]; specs_ = ast.literal_eval(sv_.value)
    assert pprint.pformat(specs_, width=160, sort_dicts=False) == seg_.replace("\r\n", "\n"), "o pformat de %s no um.py base nao e' idempotente: nao reescrevo o bloco" % nome_var
    return a_, b_, specs_


spa, spb, specs410 = _spec_block("_V410_SPECS")
k1 = [s for s in specs410 if s["nome"] == DL.KH_ANTERIOR]; assert len(k1) == 1; k1 = k1[0]
H8_ANTIGO_N = None
for c in k1["checks"]:
    if c["id"] in ("h2", "h3"):
        assert c["op"] == "igual"; c["op"] = "maior_igual"; c["descricao"] += " -- v411: piso historico; a igualdade exata esta em kh_n1_cobertura_v411"
    elif c["id"] == "h6":
        assert c["op"] == "tamanho_igual"; c["op"] = "tamanho_maior_igual"; c["descricao"] += " -- v411: piso historico; a igualdade exata esta em kh_n1_cobertura_v411"
    elif c["id"] == "h8":
        assert c["op"] == "igual" and isinstance(c["valor"], dict); H8_ANTIGO_N = len(c["valor"]); c["op"] = "tamanho_maior_igual"; c["valor"] = H8_ANTIGO_N
        c["descricao"] += " -- v411: o registro da v410 cobra o tamanho minimo da arvore (%d entradas); o pino exato da arvore esta em kh_n1_cobertura_v411" % H8_ANTIGO_N
assert H8_ANTIGO_N is not None
COV_BASE = core0["kernel_formalization"]["axiom_coverage_v392"]
k1["erratas"].append(RG.errata_pisos_v410(COV_BASE))
assert not GP.violacoes(json.dumps(k1["erratas"][-1], ensure_ascii=False)), "P18 na errata nova do spec"
edit(spa, spb, pprint.pformat(specs410, width=160, sort_dicts=False).replace("\n", CRLF), "C13_specs_v410_pisos", "G_V410_PISOS", "_V410_SPECS: kh_n1_cobertura_v410 h2/h3/h6 -> pisos, h8 -> tamanho minimo (+ errata); os vereditos nao mudam.")

# ---------------- (3) main: chamadas e selo ----------------
A_R = linha_unica(r'^        print\("   \[v410\] AVISO: o registro do HMS/13 ou os registros por spec da v410 nao rodaram')
_ordem_sha16 = DL.FALA_ORDEM_V411["sha256"][:16]   # (D181, O2) a linha da v411 na saida do rito cita a ordem de abrir por data e sha16, lido do arquivo da casa: sem o texto e sem aspas angulares
BLOCO_N00 = ('''    try:   # v411: H0DN x BG1 ABERTO -- o registro com FUNCAO h0dn_bg1_v411 (o resultado da abertura RECALCULADO dos bytes embutidos; %d checagens; o gate congelado) e os registros por spec da v411; excecao vira AVISO visivel, nunca derruba o rito
        _h411 = h0dn_bg1_v411(core)
        _h411v = _h411.get("values") or {}; _h411m = (_h411.get("mechanics") or {}).get("checks") or []
        _p411 = _h411v.get("primario") or {}; _c411 = _h411v.get("cefeidas_livres") or {}
        print("H0DN x BG1 ABERTO [v411 -- D169, a ordem do operador de 12/11/2026, citada por data e sha16 %s, nao transcrita: o teste da razao de Hubble local/fundo, aberto uma vez depois do commit publico do pre-registro, RECALCULADO neste rito a partir dos bytes embutidos; o primario sob o modelo de erros publicado e, ao lado, as Cefeidas livres; retrodicao sem ajuste, emenda posterior a guarda, teste nao cego; provado e' validade, nao creditacao; o gate nao se move]")
        print("  primario (modelo publicado): Z nulo = %%s ; Z K = %%s ; ramo %%s  ||  Cefeidas livres (ao lado, no mesmo item): Z nulo = %%s ; Z K = %%s ; ramo %%s  ||  checagens ok = %%s/%%s ; gate = %%s" %% (_p411.get("z_null"), _p411.get("z_tgl"), _p411.get("ramo"), _c411.get("z_null"), _c411.get("z_tgl"), _c411.get("ramo"), sum(1 for c_ in _h411m if c_.get("ok")), len(_h411m) or None, "o mesmo da base" if any(c_.get("id") == "c14" and c_.get("ok") for c_ in _h411m) else "DIFERENTE OU NAO LIDO"))
        print("  >>> %%s <<<\\n" %% _h411["verdict"])
        _n411 = _v411_rodar_specs(core)
        print("   [v411] o registro com funcao e os por spec da v411: %%s | specs: %%d (selados %%d)" %% (" | ".join("%%s=%%s" %% (k_, "SELOU" if (core.get(k_) or {}).get("all_verified") is True else "NAO") for k_ in _V411_REGISTROS_FUNCAO), len(_n411), sum(1 for k_ in _n411 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e411:
        print("   [v411] AVISO: o registro do H0DN v411 ou os registros por spec da v411 nao rodaram: %%r" %% (_e411,))
''' % (DL.N_CHECKS_FECHO, _ordem_sha16))
ast.parse("def _f(core):\n" + BLOCO_N00)
edit(A_R.end(), A_R.end(), crlf(BLOCO_N00), "N00_main_h0dn_v411", "G_RUNTIME", "main: UMA instrucao try/AVISO: h0dn_bg1_v411 e os registros por spec da v411, LOGO DEPOIS do bloco da v410 (h0dn_fontes_hms13_v410 e os specs da v410 ja' rodaram) e antes de emit_figures.")
assert "emit_figures(core" in T0[A_R.end():], "o bloco da v411 tem de ficar ANTES da chamada de emit_figures no main (DESENHO secao 2)"
A_S = linha_unica(r'^ {12}"registros_v410": \{n_: ')
_sel = ['            "h0dn_bg1_v411": {k_: (core.get("h0dn_bg1_v411") or {}).get(k_) for k_ in ("verdict", "all_verified", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "observed_vector_read", "opened_once", "runtime_executed", "does_not_gate_core", "n_checks_esperadas", "lei", "modelos", "p2_ao_lado_da_v387")},',
        '            "registros_v411": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V411_NOMES_REGISTROS},']
edit(A_S.end(), A_S.end(), CRLF.join(_sel) + CRLF, "N02_selo", "G_SELO", "selo: +h0dn_bg1_v411 (resumo, com a cabeca do teste e a linha ao lado) e registros_v411.")

# ---------------- (4) o bloco de runtime v411 ----------------
khj = json.load(open(os.path.join(KD, "KH_N1_v411.json"), encoding="utf-8"))
c410 = ast.literal_eval(top("_V410_H0DN_CONTRACT").value)
CONTR_H = RH.contrato_h0dn_v411(core0, selo0, c410, sha256(raw)); TXT_H = RH.texto_h0dn_v411(); INS_H = RH.insumos_embutidos(c410["insumos"])
assert CONTR_H["n_checks"] == DL.N_CHECKS_FECHO == len(CONTR_H["checagens"]) and set(CONTR_H["insumos"]) == set(INS_H) and all(INS_H[k_]["sha256"] == v_["sha256"] and INS_H[k_]["bytes"] == v_["bytes"] for k_, v_ in CONTR_H["insumos"].items())
assert CONTR_H["baseline"]["gate_verdict"] == selo0.get("qg_closure_verdict") and CONTR_H["baseline"]["escada"] == E410 and sum(1 for v_ in INS_H.values() if "reuso_v410" in v_) == 2
assert not any(t_ in CONTR_H["veredito_ok_prefixo"] + CONTR_H["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V411) and not GUARDA.search(CONTR_H["veredito_ok_prefixo"] + CONTR_H["veredito_meio_molde"] + CONTR_H["veredito_sufixo"])
fontes = {}
for f in RG.FONTES:
    b = open(f["arquivo"], "rb").read(); fontes[f["chave"]] = {"arquivo": f["arquivo"], "papel": f["papel"], "sha256": sha256(b), "bytes": len(b)}
verb = {}   # (D181) NENHUM texto de fala no programa: _V411_VERBATINS2 vai vazio; as 11 entram CITADAS (data, sha256 lido do arquivo da casa na construcao, papel, autor), sem texto, sem trecho e sem o nome do arquivo
FALAS_CIT = {k_: dict(v_) for k_, v_ in RG.FALAS_CITADAS.items()}
assert not RG.VERBATINS and len(FALAS_CIT) == DL.N_FALAS_V411 == 11 and all(re.fullmatch(r"[0-9a-f]{64}", c_["sha256"]) and c_["autor"] == "operador" and c_["quando"] and c_["papel"] for c_ in FALAS_CIT.values())
assert [c_["sha256"] for c_ in FALAS_CIT.values()] == [f_["sha256"] for f_ in DL.FALAS_V411], "as citacoes nao seguem a lista congelada (o sha256 vem dos arquivos da casa, lidos pelo delta)"


def _p18_sem_falas(txt_):
    s_ = txt_
    for v_ in sorted([x_["text"] for x_ in verb.values()] + list(DL.D10.FRASES_VERBATIM_V410), key=len, reverse=True):
        for ln_ in [l_.strip() for l_ in v_.splitlines() if len(l_.strip()) >= 12]:
            for forma_ in (ln_, json.dumps(ln_, ensure_ascii=False)[1:-1], repr(ln_)[1:-1]):
                s_ = s_.replace(forma_, " ")
    return GP.violacoes(s_)


# o pino h8: a ARVORE SIMULADA do Nos depois do rito = o embutido + os residuais da pasta (fora de work\: licao D135)
NOSK = os.path.join(DL.NOS, "tgl_kernel")
_ns_h8 = {"os": os, "hashlib": hashlib}
for _nm in ("sha_file", "sha256_directory"):
    exec(compile(ast.get_source_segment(T0, top(_nm)), "<um:%s>" % _nm, "exec"), _ns_h8)
SIMD = os.path.join(DL.RODADA_PAI, "arvore_simulada_h8")
if os.path.isdir(SIMD):
    shutil.rmtree(SIMD)
for rel, c_ in old_d.items():
    p_ = os.path.join(SIMD, *rel.split("/")); os.makedirs(os.path.dirname(p_), exist_ok=True); open(p_, "w", encoding="utf-8", newline="").write(c_)
H8_EXTRAS = []
for dp_, dn_, fn_ in os.walk(NOSK):
    if ".lake" in dp_.replace("\\", "/").split("/"):
        continue
    for nm_ in fn_:
        if nm_.endswith(".lean") or nm_ in ("lakefile.toml", "lean-toolchain", "README.md", "lake-manifest.json"):
            rel_ = os.path.relpath(os.path.join(dp_, nm_), NOSK).replace("\\", "/")
            if rel_ not in old_d:
                H8_EXTRAS.append(rel_); d_ = os.path.join(SIMD, *rel_.split("/")); os.makedirs(os.path.dirname(d_), exist_ok=True); shutil.copyfile(os.path.join(dp_, nm_), d_)
H8 = _ns_h8["sha256_directory"](SIMD)["files"]
assert all(H8.get(k_) == v_ for k_, v_ in FORMAL_MAP.items()) and set(H8) - set(FORMAL_MAP) <= set(H8_EXTRAS), "o hash formal simulado difere do FORMAL_MAP nos embutidos"
_h8_v410 = [c_ for c_ in [s for s in ast.literal_eval(top("_V410_SPECS").value) if s["nome"] == DL.KH_ANTERIOR][0]["checks"] if c_["id"] == "h8"][0]["valor"]
H8_IGUAL_AO_DA_V410 = (dict(H8) == dict(_h8_v410))
specs = RG.especs(FORMAL_MAP, khj, H8, COV_BASE, core0)
spec_nomes = [s["nome"] for s in specs]; assert spec_nomes == [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]
_ax_antigos = core0["kernel_formalization"]["axiom_report"]
for s in specs:
    corpo = json.dumps({k: s.get(k) for k in ("erratas", "limites", "diz", "nao_diz", "leituras_do_operador", "extras")}, ensure_ascii=False)
    v = GP.violacoes(corpo); assert not v, (s["nome"], v[:3])
    assert not GF.violacoes(corpo), (s["nome"], GF.violacoes(corpo)[:3])
    assert not GUARDA.search(s["veredito_prefixo"] + "__" + s["veredito_sufixo"]) and not any(t_ in s["veredito_prefixo"] + s["veredito_sufixo"] for t_ in DL.TOKENS_PROIBIDOS_V411), s["nome"]
    assert all(ch in fontes for ch in s.get("fontes", [])) and all(ch in verb for ch in s.get("verbatins", [])), s["nome"]
    for c_ in s["checks"]:
        if c_["onde"] == "core" and c_["op"] == "verdadeiro" and c_["caminho"][-1] == "all_verified" and c_["caminho"][0] != DL.FECHO_REGISTRO:
            assert (core0.get(c_["caminho"][0]) or {}).get("all_verified") is True, ("o spec cobra um registro anterior que nao selou na base", c_["caminho"][0])
assert not _p18_sem_falas(json.dumps(TXT_H, ensure_ascii=False)) and not GUARDA.search(json.dumps(TXT_H, ensure_ascii=False)), "P18 ou palavra recusada no texto do registro H0DN v411"
assert not GF.violacoes(json.dumps(TXT_H, ensure_ascii=False)), ("guarda de frases no texto do registro", GF.violacoes(json.dumps(TXT_H, ensure_ascii=False))[:3])
QUADRO_SRC = open(os.path.join(HERE, "quadro_v411.py"), encoding="utf-8").read(); RTH_SRC = open(os.path.join(HERE, "runtime_h0dn_v411.py"), encoding="utf-8").read()
assert RTH_SRC.count("__SHA16_DA_ORDEM_DE_ABRIR__") == 1, "o marcador do sha16 da ordem de abrir (docstring do runtime) nao esta' uma vez so'"
RTH_SRC = RTH_SRC.replace("__SHA16_DA_ORDEM_DE_ABRIR__", DL.FALA_ORDEM_V411["sha256"][:16]); assert "__SHA16_DA_ORDEM" not in RTH_SRC
RUNTIME_SRC = QUADRO_SRC.rstrip("\n") + "\n\n\n" + RTH_SRC.rstrip("\n") + "\n"
assert "\r" not in RUNTIME_SRC
ast.parse(RUNTIME_SRC)
assert not GUARDA.search(RUNTIME_SRC), "veredito proibido no runtime"
assert not AC.literais_de_beta(RUNTIME_SRC), "literal de beta no runtime (C9)"
_TITULOS = {"quadro_pt": DL.TITULO_QUADRO_TOPO_PT, "secao_pt": DL.TITULO_SECAO_PT, "secao_en": DL.TITULO_SECAO_EN}
RCODE = ("_V411_H0DN_CONTRACT = " + pprint.pformat(CONTR_H, width=150, sort_dicts=False) + "\n_V411_H0DN_TEXT = " + pprint.pformat(TXT_H, width=150, sort_dicts=False)
         + "\n_V411_H0DN_INSUMOS = " + repr(INS_H) + "   # os insumos EMBUTIDOS em base64, pinados por sha256 lido; os dois de reuso apontam o blob da v410 (_V410_H0DN_INSUMOS), o mesmo sha256; decodificados e conferidos a cada rito\n"
         + "_V411_FONTES = " + pprint.pformat(fontes, width=160, sort_dicts=True) + "\n_V411_VERBATINS2 = " + pprint.pformat(verb, width=160, sort_dicts=True) + "   # (D181) vazio de proposito: nenhuma fala embutida; as 11 vao so' citadas em _V411_FALAS_CITADAS\n_V411_FALAS_CITADAS = " + pprint.pformat(FALAS_CIT, width=160, sort_dicts=False)
         + "\n_V411_TEXTOS_DA_GERENCIA = " + pprint.pformat(DL.TEXTOS_DA_GERENCIA_V411, width=160, sort_dicts=False) + "   # (revisao de terceiro R1) os fechos, os rotulos e a errata E44: texto da gerencia, lido do DESENHO\n"
         + "\n_V411_SPECS = " + pprint.pformat(specs, width=160, sort_dicts=False) + "\n"
         + "_V411_TOPO = " + pprint.pformat({"pt": TOPO["pt"], "en": TOPO["en"], "ratificado": TOPO["ratificado"], "sha256_do_arquivo": TOPO["sha256"], "marcadores": _TAB_MK, "livro": _LIVRO}, width=160, sort_dicts=False) + "   # (DESENHO 5.1 b) o texto do topo; os numeros sao preenchidos do core em rito\n"
         + "_V411_TITULO_QUADRO_PT = " + repr(DL.TITULO_QUADRO_TOPO_PT) + "\n_V411_TITULO_SECAO = " + repr({"pt": DL.TITULO_SECAO_PT, "en": DL.TITULO_SECAO_EN}) + "\n_V411_ESTATUTO_AO_LADO_PT = " + repr(DL.FRASE_ESTATUTO_DA_PROVA_AO_LADO_PT) + "\n"
         "_V411_NOMES_REGISTROS = " + repr(spec_nomes) + "\n_V411_REGISTROS_FUNCAO = " + repr(list(DL.REGISTROS_FUNCAO)) + "\n_V392_FONTES.update(_V411_FONTES)   # v411: o motor de registros (v392) le as fontes e os verbatins tambem da v411\n_V392_VERBATINS2.update(_V411_VERBATINS2)\n\n\n"
         "def _v411_citar_falas(reg_):\n"
         '    """v411 (D181) -- as falas do operador de 11 e 12/11 entram so\' CITADAS: o motor da v392 so\' embute texto; aqui o registro cunhagens_v411 recebe, em verbatim, os itens citados (data, sha256, papel, autor; sem texto, sem trecho, sem o nome do arquivo). Estrutura malformada => nao sela."""\n'
         "    import re as _re\n"
         "    cit_ = {k_: dict(v_, citado_por_sha256=True, texto_transcrito=False) for k_, v_ in _V411_FALAS_CITADAS.items()}\n"
         "    ok_ = bool(cit_) and len(cit_) == int((reg_.get(\"extras\") or {}).get(\"n_falas\", -1)) and all(isinstance(v_.get(\"sha256\"), str) and _re.fullmatch(r\"[0-9a-f]{64}\", v_[\"sha256\"]) and v_.get(\"autor\") == \"operador\" and bool(v_.get(\"quando\")) and bool(v_.get(\"papel\")) for v_ in cit_.values())\n"
         "    reg_[\"verbatim\"] = cit_\n"
         "    if not ok_ and reg_.get(\"all_verified\"):\n"
         "        reg_[\"all_verified\"] = False; reg_[\"verdict\"] = \"%s__NOT_SEALED_THIS_RUN__CITED_SAYINGS_MALFORMED__GATE_UNMOVED\" % reg_[\"verdict\"].split(\"__\")[0]\n"
         "    return reg_\n\n\n"
         "def _v411_rodar_specs(core_):\n"
         '    """v411 -- roda os registros por spec da v411 (o MOTOR e\' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. O registro com funcao (h0dn_bg1_v411) roda antes, no main."""\n'
         "    for spec_ in _V411_SPECS:\n        try:\n            core_[spec_[\"nome\"]] = _v392_registro(spec_, core_)\n            if spec_[\"nome\"] == \"cunhagens_v411\":\n                core_[spec_[\"nome\"]] = _v411_citar_falas(core_[spec_[\"nome\"]])\n        except Exception as e_:   # noqa: BLE001\n"
         '            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}\n'
         '    return [s_["nome"] for s_ in _V411_SPECS]\n')
HDR = ("# ====================== v411 (12/11/2026) -- O TESTE DECISIVO: H0DN x BG1 ABERTO uma vez, depois do commit publico do pre-registro; o registro com FUNCAO h0dn_bg1_v411 (" + str(DL.N_CHECKS_FECHO) + " checagens; o resultado da abertura RECALCULADO a partir dos bytes embutidos, pela rotina pinada), o quadro do topo, a secao do artigo, as falas do operador de 11 e 12/11 e os registros por spec cunhagens_v411 e kh_n1_cobertura_v411.\n"
       "# NENHUM modulo novo no kernel (o da v410, byte a byte). O primario sob o modelo de erros publicado e, ao lado, as Cefeidas livres; retrodicao sem ajuste, com emenda posterior a guarda; teste nao cego; provado e' validade, nao creditacao. As erratas E41, E42 e E43 vao AO LADO; nenhuma chave antiga muda; o gate nao se move.\n")
RT_ = HDR + RUNTIME_SRC.rstrip("\n") + "\n\n\n# ---- v411: o contrato, o texto e os insumos do registro (derivados dos arquivos pinados e do core da v410 selada), as fontes, as falas e os specs\n" + RCODE
ast.parse(RT_)
_novo_texto_sem_verb = RT_ + json.dumps(specs, ensure_ascii=False)   # (D181) nenhuma fala embutida: nada a retirar
_p18_novo = [v_ for v_ in _p18_sem_falas(_novo_texto_sem_verb.replace(repr(INS_H), " "))]
_p18_novo_fora_do_topo = list(_p18_novo)   # (decisao (c): nenhum filtro ad hoc; a cabeca nao esta' no codigo-fonte, vai em partes no literal embutido)
assert not _p18_novo, ("P18 no texto novo do bloco de runtime (sem as falas embutidas)", _p18_novo[:3])
G0_ = GF.controle_negativo(); assert G0_["ok"], "o controle negativo da guarda das frases falhou"
_corpo_guarda = RUNTIME_SRC[RUNTIME_SRC.index("def _v411_guarda_frases(txt_):"):RUNTIME_SRC.index("def _v411_h0dn_decode(")]
_txt_ger = RUNTIME_SRC.replace(_corpo_guarda, "") + json.dumps([CONTR_H, TXT_H, specs, {k_: v_["papel"] for k_, v_ in fontes.items()}], ensure_ascii=False) + HDR + LINHA_V + BLOCO_N00
V_GF = [v_ for v_ in GF.violacoes(_txt_ger) if not v_[0].startswith("F67_")]   # (no CODIGO-FONTE os numeros sao %s/concatenacao: a obrigacao F67 se confere no texto RENDERIZADO, abaixo)
assert not V_GF, ("FRASE PROIBIDA no texto novo da gerencia (guarda_frases_v411)", V_GF[:4])
# o texto RENDERIZADO (o quadro, a remissao, a secao, a linha e o quadro do .md, o topo, as trocas e a frase ao lado), com o registro do ensaio offline (o mesmo recalculo, os mesmos insumos): as duas guardas linha a linha
_REG_ENSAIO = os.path.join(HERE, "TESTE_H0DN_OFFLINE_v411_registro.json")
assert os.path.exists(_REG_ENSAIO), "rode antes _teste_h0dn_offline_v411.py (o registro do ensaio, para renderizar o quadro e a secao)"
_rq = json.load(open(_REG_ENSAIO, encoding="utf-8")); assert _rq.get("all_verified") is True
_nsq = {"_V411_TOPO": {"pt": TOPO["pt"], "en": TOPO["en"], "marcadores": _TAB_MK, "livro": _LIVRO}, "_V411_ESTATUTO_AO_LADO_PT": DL.FRASE_ESTATUTO_DA_PROVA_AO_LADO_PT, "_V411_TEXTOS_DA_GERENCIA": DL.TEXTOS_DA_GERENCIA_V411}
exec(compile(QUADRO_SRC, "quadro_v411.py", "exec"), _nsq)
_corq = {"h0dn_bg1_v411": _rq, "estatuto_da_prova_v391": core0.get("estatuto_da_prova_v391"), "teste_de_veracidade_fase9_v397": core0.get("teste_de_veracidade_fase9_v397")}   # (o topo le o livro e a Fase 9 V2 do core; o H0DN, do registro do ensaio offline)
RENDER = {"quadro_pt": _nsq["_v411_quadro_tex"](_rq, "pt", DL.TITULO_QUADRO_TOPO_PT), "quadro_en": _nsq["_v411_quadro_tex"](_rq, "en", DL.TITULO_QUADRO_TOPO_PT), "remissao": [_nsq["_v411_remissao_tex"]("pt"), _nsq["_v411_remissao_tex"]("en")],
          "secao_pt": _nsq["_v411_secao_tex"](_corq, "pt", DL.TITULO_SECAO_PT), "secao_en": _nsq["_v411_secao_tex"](_corq, "en", DL.TITULO_SECAO_EN), "md": _nsq["_v411_quadro_md"](_rq, DL.TITULO_QUADRO_TOPO_PT) + [_nsq["_v411_linha_md"](_rq)],
          "topo": [_nsq["_v411_topo_texto"](_corq, "pt"), _nsq["_v411_topo_texto"](_corq, "en")], "efeitos": [_nsq["_v411_efeitos_tex"](_corq, "pt"), _nsq["_v411_efeitos_tex"](_corq, "en")], "efeitos_metodo": [_nsq["_v411_efeitos_tex"](_corq, "pt", "metodo"), _nsq["_v411_efeitos_tex"](_corq, "en", "metodo")],
          "p2_v387": [_nsq["_v411_p2_ao_lado_tex"](_corq, "pt"), _nsq["_v411_p2_ao_lado_tex"](_corq, "en")], "estatuto": [_nsq["_v411_estatuto_tex"](_corq, "pt"), _nsq["_v411_estatuto_tex"](_corq, "en")]}
_cabq = (_rq.get("values") or {}).get("primario", {}).get("cabeca_do_teste") or ""
RENDER_VIOL = {}
for _k, _ls in RENDER.items():
    _vv = [(i_, GF.p18_sem_cabeca(l_, GF.RAMOS_V411, GF.N_DA_CABECA), GF.violacoes(l_)) for i_, l_ in enumerate(_ls)]   # (decisao (c): a UNICA excecao da P18)
    _vv = [x_ for x_ in _vv if x_[1] or x_[2]]
    if _vv:
        RENDER_VIOL[_k] = _vv[:3]
    assert not any("n/d" in l_ for l_ in _ls), ("numero faltando (n/d) no texto renderizado", _k)
    if _k not in ("md",):
        assert not any(any(0x370 <= ord(ch_) <= 0x3FF for ch_ in l_) for l_ in _ls), ("letra grega Unicode no LaTeX renderizado (licao da v408; na v411 o Λ do ΛCDM, achado do ensaio a seco)", _k, sorted({ch_ for l_ in _ls for ch_ in l_ if 0x370 <= ord(ch_) <= 0x3FF}))
assert not RENDER_VIOL or PREVOO, ("o texto RENDERIZADO reprova nas guardas", RENDER_VIOL)
A_P = linha_unica(r"^# ====================== v410 \(06/11/2026\)")
edit(A_P.start(), A_P.start(), crlf(RT_.rstrip("\n") + "\n\n\n"), "W02_runtime_v411", "G_RUNTIME", "bloco v411: o quadro e a secao, a guarda das frases da v411, a mecanica, o registro h0dn_bg1_v411, o contrato, os insumos, as falas, os specs.")

# ---------------- (5) o artigo e o .md ----------------
for _lg, _d in (("pt", "pt"), ("en", "en")):
    _a = linha_unica(r'^    for _l397 in _v397_quadro_tex\(core\.get\("teste_de_veracidade_fase9_v397"\), "%s"\):' % _lg)
    edit(_a.start(), _a.start(), crlf('    # v411 (12/11/2026) -- O QUADRO H0DN x BG1 (DESENHO 5.1 a), ACIMA do quadro “O Teste da Unica Palavra” (que fica, como registro de 23/10, com a linha de remissao logo abaixo dele); numeros LIDOS do core["h0dn_bg1_v411"]. Nada aqui move o gate.\n'
                                     '    for _l411 in _v411_quadro_tex(core.get("h0dn_bg1_v411"), "%s", _V411_TITULO_QUADRO_PT):\n        s.append(_l411)\n' % _lg), "W03_quadro_" + _lg, "G_ARTIGO", "artigo %s: o quadro H0DN x BG1 acima do quadro da v397." % _lg)
    _b = re.search(r'^    for _l397 in _v397_quadro_tex\(core\.get\("teste_de_veracidade_fase9_v397"\), "%s"\):\r\n        s\.append\(_l397\)\r\n' % _lg, T0, re.M); assert _b and T0.count(_b.group(0)) == 1
    edit(_b.end(), _b.end(), crlf('    s.append(_v411_remissao_tex("%s"))   # v411: a remissao do quadro da v397 (registro de 23/10) ao quadro H0DN x BG1\n' % _lg), "W03b_remissao_" + _lg, "G_ARTIGO", "artigo %s: a linha de remissao depois do quadro da v397." % _lg)
_am = linha_unica(r'^    for _l397 in _v397_quadro_md\(core\.get\("teste_de_veracidade_fase9_v397"\)\):')
edit(_am.start(), _am.start(), crlf('    for _l411 in _v411_quadro_md(core.get("h0dn_bg1_v411"), _V411_TITULO_QUADRO_PT):   # v411 (12/11/2026): o QUADRO H0DN x BG1 no TOPO do .md, antes do quadro da v397\n        md.append(_l411)\n'), "W03_quadro_md", "G_ARTIGO", "md: o quadro H0DN x BG1 antes do quadro da v397.")
# o paragrafo de apresentacao ABRE com o texto do topo (5.1 b) e as duas trocas ditas
_t_pt = re.search(r'\{\\large\\itshape "\r\n             r"Apresentação do programa terminal da TGL', T0); assert _t_pt and T0.count(_t_pt.group(0)) == 1
edit(_t_pt.start(), _t_pt.end(), '{\\large\\itshape " + _v411_topo_texto(core, "pt") + r""' + CRLF + '             r"Apresentação do programa terminal da TGL', "W06_topo_pt", "G_ARTIGO", "artigo PT: o paragrafo de apresentacao ABRE com o texto do topo (5.1 b; numeros do core).")
_t_en = re.search(r'\{\\large\\itshape "\r\n             r"Presentation of the terminal program', T0)
if not _t_en:
    _t_en = re.search(r'\{\\large\\itshape "\r\n             r"[A-Z][^"\r\n]{0,40}terminal program', T0)
assert _t_en and T0.count(_t_en.group(0)) == 1, "a ancora do paragrafo de apresentacao EN nao foi achada uma vez"
edit(_t_en.start(), _t_en.start() + len('{\\large\\itshape "'), '{\\large\\itshape " + _v411_topo_texto(core, "en") + r""', "W06_topo_en", "G_ARTIGO", "artigo EN: the presentation paragraph OPENS with the top text (5.1 b; numbers from the core).")
replace_unique('resolve a tensão de Hubble por "' + CRLF + '             r"remissão expressa ao trabalho publicado\\footnote{Remissão expressa: a resolução da "',
               'lê a razão de Hubble pelo teste acima (a remissão ao trabalho publicado fica como registro, na nota)\\footnote{Remissão expressa (registro da v410): a resolução da "', "W07_troca1_pt", "G_ARTIGO", "artigo PT: a remissao da tensao de Hubble vira registro; a razao de Hubble e' lida pelo teste acima (5.1 b).")
replace_unique('resolves the Hubble tension by "' + CRLF + '             r"express remission to the published work\\footnote{Express remission: the resolution of "',
               'reads the Hubble ratio through the test above (the remission to the published work stays as record, in the note)\\footnote{Express remission (v410 record): the resolution of "', "W07_troca1_en", "G_ARTIGO", "artigo EN: the Hubble-tension remission becomes record (5.1 b).")
replace_unique('a probabilidade de os "' + CRLF + '                     r"efeitos $\\beta$ existirem na natureza segue indeterminada")', '" + _v411_efeitos_tex(core, "pt"))', "W08_troca2_pt", "G_ARTIGO", "artigo PT: a frase dos efeitos de beta (5.1 b), so' se o registro selou.")
replace_unique('the probability that the $\\beta$ effects exist in nature remains undetermined")', '" + _v411_efeitos_tex(core, "en"))', "W08_troca2_en", "G_ARTIGO", "artigo EN: the sentence on the beta effects (5.1 b), only if the record sealed.")
replace_unique('a de os efeitos "' + CRLF + '             r"$\\beta_{\\rm TGL}$ existirem na natureza não está determinada, porque nenhum canal discrimina a RG à sensibilidade disponível; nenhuma soma de "',
               '" + _v411_efeitos_tex(core, "pt", "metodo").replace("%", "%%") + r"; nenhuma soma de "', "W08_troca2_metodo_pt", "G_ARTIGO", "artigo PT: a mesma troca no paragrafo “O metodo” (5.1 b).")
replace_unique('the probability that the "' + CRLF + '             r"$\\beta_{\\rm TGL}$ effects exist in nature is not determined, because no channel discriminates GR at the available sensitivity; no sum of consistencies "',
               '" + _v411_efeitos_tex(core, "en", "metodo").replace("%", "%%") + r"; no sum of consistencies "', "W08_troca2_metodo_en", "G_ARTIGO", "artigo EN: the same swap in “The method” (5.1 b).")
for _lg, _rx in (("pt", r'^    s\.append\(r"\\textbf\{O estatuto da prova \(v391\)\.\} '), ("en", r'^    s\.append\(r"\\textbf\{The status of the proof \(v391\)\.\} ')):
    _e = linha_unica(_rx); edit(_e.end(), _e.end(), '    s.append(_v411_estatuto_tex(core, "%s"))   # v411 (5.1 c): a frase AO LADO do estatuto da prova (v391)' % _lg + CRLF, "W10_estatuto_" + _lg, "G_ARTIGO", "artigo %s: a frase ao lado do estatuto da prova (5.1 c)." % _lg)
for _lg, _rx in (("pt", r'^    s\.append\(r"\\item Nada disto credita a gravidade quântica na natureza; o elo pendente é'), ("en", r'^    s\.append\(r"\\item None of this credits quantum gravity in nature; the pending link is')):
    _e = linha_unica(_rx); edit(_e.end(), _e.end(), '    s.append(r"\\item " + _v411_estatuto_tex(core, "%s"))   # v411 (5.1 c): a mesma remissao no item do coracao' % _lg + CRLF, "W11_coracao_" + _lg, "G_ARTIGO", "artigo %s: a remissao no item do coracao (5.1 c)." % _lg)
PT10_FIRST = open(os.path.join(DL.V410, "artigo_pt_v410.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
EN10_FIRST = open(os.path.join(DL.V410, "artigo_en_v410.pysnip"), encoding="utf-8").read().splitlines()[0] + CRLF
SEC_PT = ('    # v411 (12/11/2026) -- O TESTE DECISIVO: H0DN x BG1 aberto, a emenda e a abertura (DESENHO 5.2); MONTADA do core selado (o registro h0dn_bg1_v411) e do pre-registro embutido; antes da secao da v410. Nada aqui move o gate.\n'
          '    for _l411s in _v411_secao_tex(core, "pt", _V411_TITULO_SECAO["pt"]):\n        s.append(_l411s)\n')
SEC_EN = ('    # v411 (12/11/2026) -- THE DECISIVE TEST: H0DN x BG1 opened, the amendment and the opening (DESENHO 5.2); ASSEMBLED from the sealed core and the embedded pre-registration; before the v410 section. Nothing here moves the gate.\n'
          '    for _l411s in _v411_secao_tex(core, "en", _V411_TITULO_SECAO["en"]):\n        s.append(_l411s)\n')
for sn_ in (SEC_PT, SEC_EN):
    ast.parse("def _f(core, s):\n" + sn_); assert not GUARDA.search(sn_) and not GP.violacoes(sn_) and not GF.violacoes(sn_)
replace_unique(PT10_FIRST, crlf(SEC_PT) + PT10_FIRST, "W04_artigo_PT", "G_ARTIGO", "artigo PT: a secao “O teste decisivo” antes da secao da v410.")
replace_unique(EN10_FIRST, crlf(SEC_EN) + EN10_FIRST, "W05_artigo_EN", "G_ARTIGO", "artigo EN: the “decisive test” section before the v410 section.")
_A2_ANC = '    t = t.replace("~", " ").replace("{", "").replace("}", "")' + CRLF   # (A2 da revisao de terceiro da v410; medido em A2_MEDIDA_v411.json: mudanca CONTIDA no conversor _tex_to_txt)
assert ast.get_source_segment(T0, top("_tex_to_txt")).count(_A2_ANC.rstrip("\r\n")) == 1
replace_unique(_A2_ANC, '    t = _re.sub(r"\\^\\{([^{}]{2,})\\}", r"^(\\1)", t)   # v411 (A2 da revisao de terceiro da v410): o expoente agrupado de mais de um caractere fica agrupado no TXT, como no PDF' + CRLF + _A2_ANC,
               "W12_a2_txt", "G_ARTIGO", "TXT do artigo: o expoente agrupado ^{X} (X de 2 ou mais caracteres) vira ^(X) antes de dissolver as chaves (A2; medido em A2_MEDIDA_v411.json).")
A_M = linha_unica(r'^    md\.append\("> \*\*IALD2 \(v410, 06/11/2026\):\*\*')
MD_LINHA = '    md.append("' + DL.MD_ROTULO_H0DN_V411 + ' " + _v411_linha_md(core.get("h0dn_bg1_v411")))'
ast.parse("def _f(core, md):\n" + MD_LINHA); assert not GP.violacoes(MD_LINHA) and not GF.violacoes(MD_LINHA)
edit(A_M.start(), A_M.start(), MD_LINHA + CRLF, "W09_md", "G_ARTIGO", "md canonico: a linha “H0DN × BG1 ABERTO (v411)” antes das linhas da v410.")
# (aditivo da gerencia c1, 12/11) a frase AO LADO do P2 na secao dos tres testes de estresse (v387), PT e EN: ANTES da linha do veredito da v387 (que fica, selado); o texto selado da v387 nao e' reescrito
for _lg, _sec in (("pt", r'    _sec3s.append(r"\section*{Os três testes de estresse, conjuntos (v387)}")'), ("en", r'    _sec3s.append(r"\section*{The three stress tests, taken together (v387)}")')):
    assert T0.count(_sec) == 1, ("a ancora da secao da v387 nao e' unica", _lg)
    _vl = r'    _sec3s.append(r"\begin{center}\small\texttt{" + _tx3s(_t3s.get("verdict") or "TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN__SECTION_COUNTED_ALONE__GATE_UNTOUCHED") + r"}\end{center}")' + CRLF
    _i0 = T0.index(_sec); _i1 = T0.index(_vl, _i0); _prox = [T0.find(x_, _i0 + len(_sec)) for x_ in (r'_sec3s.append(r"\section*{The three stress tests', r'_sec3s.append(r"\section*{Os três testes de estresse')]
    assert all(p_ < 0 or p_ > _i1 or p_ <= _i0 for p_ in _prox), ("a linha do veredito da v387 achada nao e' a da secao", _lg)
    edit(_i1, _i1, '    _sec3s.append(_v411_p2_ao_lado_tex(core, "%s"))   # v411 (aditivo da gerencia c1, 12/11): o P2 AO LADO do texto selado da v387, com as quatro obrigacoes da F67' % _lg + CRLF, "W13_p2_v387_" + _lg, "G_ARTIGO",
         "artigo %s: a frase AO LADO do P2 na secao dos tres testes de estresse (v387); o texto selado da v387 fica." % _lg)
_controles(RT_, "runtime_v411"); _controles([CONTR_H, TXT_H, specs, fontes, TOPO], "contrato/texto/specs/fontes/topo")

# ---------------- aplicar ----------------
EDITS.sort(key=lambda e: (e[0], e[1]))
for (a1, b1, *_), (a2, b2, *_) in zip(EDITS, EDITS[1:]):
    assert b1 <= a2, ("edicoes sobrepostas", (a1, b1), (a2, b2))


def montar(k_espacos):
    T_ = T0
    for a_, b_, novo_, pid_, *_r in sorted(EDITS, key=lambda e: -e[0]):
        if pid_ == "W01_versao":
            novo_ = novo_[:-len(CRLF)] + " " * k_espacos + CRLF
        T_ = T_[:a_] + novo_ + T_[b_:]
    return T_


def n10_aplica(T_):
    bb = T_.encode("utf-8")

    def difere(b_):
        n_ = len(b_); i_ = max(0, n_ // 2); j_ = min(n_ - 1, i_ + 3)
        return b_[i_] != b_[j_]
    return difere(bb) and difere(bb[:1 << 20])


K_N10 = next(k_ for k_ in range(0, 64) if n10_aplica(montar(k_)))
T = montar(K_N10)
tree = ast.parse(T)
assert len(re.findall(r"(?<!\r)\n", T)) == LF_SOLTOS0, "o patch criou ou perdeu um LF solto (o arquivo e' CRLF)"
NOVOS_NOMES = ("_v411_n", "_v411_p", "_v411_tt", "_v411_tex_unicode", "_v411_atomos", "_v411_hora", "_v411_quadro_tex", "_V411_NAO_DECIDE_EN", "_v411_remissao_tex", "_v411_quadro_md", "_v411_secao_tex", "_v411_linha_md", "_V411_MARCADORES",
               "_v411_tex_misto", "_v411_topo_texto", "_v411_fecho_blocos", "_v411_rotulo_agregado", "_v411_errata_e44_tex", "_v411_efeitos_tex", "_v411_p2_ao_lado_tex", "_v411_estatuto_tex", "_v411_guarda_frases", "_v411_p18_sem_cabeca","_v411_h0dn_decode", "_v411_h0dn_carregar_codigo", "_v411_h0dn_guarda_finitude", "_v411_h0dn_compara",
               "_v411_h0dn_json", "_v411_h0dn_secao", "v411_h0dn_mechanics", "_V411_H0DN_RECUSA", "h0dn_bg1_v411", "_V411_H0DN_CONTRACT", "_V411_H0DN_TEXT", "_V411_H0DN_INSUMOS", "_V411_FONTES", "_V411_VERBATINS2", "_V411_FALAS_CITADAS", "_V411_TEXTOS_DA_GERENCIA", "_V411_SPECS",
               "_V411_TOPO", "_V411_TITULO_QUADRO_PT", "_V411_TITULO_SECAO", "_V411_ESTATUTO_AO_LADO_PT", "_V411_NOMES_REGISTROS", "_V411_REGISTROS_FUNCAO", "_v411_citar_falas", "_v411_rodar_specs")
for n in NOVOS_NOMES:
    assert sum(1 for x in tree.body if nm(x) == n) == 1, n
_nomes_base = AC.nomes_de_nivel_de_modulo(T0); _nomes_rt = AC.nomes_de_nivel_de_modulo(RUNTIME_SRC)
_colide = sorted(_nomes_rt & set(_nomes_base)); assert not _colide, ("colisao de nomes (C3)", _colide)
assert ast.literal_eval(top("_EMBEDDED_KERNEL_FILES", tree).value) == old_d, "o kernel embutido mudou (a v411 nao tem modulo novo)"
assert ast.literal_eval(top("_LEAN_THEOREM_FLAGS", tree).value) == ast.literal_eval(top("_LEAN_THEOREM_FLAGS").value), "as bandeiras mudaram"
assert ast.literal_eval(top("_V410_SPECS", tree).value) == specs410
INTOCADAS_V411 = list(DL.D10.FUNCOES_INTOCADAS) + ["iald2_v410", "v410_iald2_mechanics", "a_escala_v410", "h0dn_bg1_v410", "veredito_h0dn", "_v410_h0dn_mechanics", "h0dn_fontes_hms13_v410", "_v410_guarda_frases", "_v410_rodar_specs",
                                                   "_V410_IALD2_CONTRACT", "_V410_IALD2_TEXT", "_V410_H0DN_CONTRACT", "_V410_H0DN_TEXT", "_V410_H0DN_INSUMOS", "_V410_HMS13_CONTRACT", "_V410_HMS13_TEXT", "_V410_HMS13_INSUMOS",
                                                   "_V410_AESCALA_CONTRACT", "_V410_AESCALA_TEXT", "_V410_FONTES", "_V410_VERBATINS2", "_V409_SPECS", "_v397_quadro_tex", "_v397_quadro_md", "run_um", "verify_tgl_kernel_formalization",
                                                   "_EMBEDDED_KERNEL_FILES", "_LEAN_THEOREM_FLAGS", "prove_external_ladder"]
for fname in INTOCADAS_V411:
    assert ast.get_source_segment(T, top(fname, tree)) == ast.get_source_segment(T0, top(fname)), "a funcao/constante %s NAO pode mudar na v411" % fname
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = re.search(r'ESBOCO_SHA256 = "([0-9a-f]{64})"', open(os.path.join(os.path.dirname(HERE), "v403", "gerar_candidato_v403.py"), encoding="utf-8").read()).group(1)
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
conta = lambda t: {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(t)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(t)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(t)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(t))}
g0, g1 = conta(T0), conta(T)
assert g0 == g1 == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}, ("as guardas estaticas da Bancada", g0, g1)
ALPHA_BASE = ast.literal_eval(top("SEALED_CODATA_ALPHA").value)
a1_ = RX["RE_ALPHA"].search(T); v1_ = RX["RE_VERSAO"].search(T)
assert a1_ and v1_ and v1_.group(1) == "v411" and float(a1_.group(1)) == ALPHA_BASE
_rt_sem_b64 = RT_.replace(repr(INS_H), " ")
_vedada_repr = repr(DL.H0DN_PASTA_VEDADA_V410)[1:-1]
_kimi_paths = re.findall(r"[A-Za-z]:\\\\[^'\"]*kimi[^'\"]*", _rt_sem_b64)
assert all(p_ == _vedada_repr for p_ in _kimi_paths), ("veto: o bloco novo cita um caminho da pasta do Kimi que nao e' o da propria pasta vedada (a recusa)", sorted(set(_kimi_paths))[:3])
b = T.encode("utf-8")
man = {("artefato_de_ensaio" if ENSAIO else "candidato"): DL.CANDIDATO_ARQ, "sha16": sha16(b), "sha256": sha256(b), "bytes": len(b), "base_v410_sha16": SHA0, "base_v410_bytes": len(raw), "delta_bytes": len(b) - len(raw), "escada": [E410, ESCADA_ESP], "n_bandeiras": 0,
       "patches": [{"id": e[3], "grupo": e[4], "o_que_muda": e[5], "bytes_removidos": e[1] - e[0], "bytes_inseridos": len(e[2])} for e in EDITS], "n_patches": len(EDITS),
       "kernel": {"modulos_novos": 0, "modelo": "sem modulo novo: o embutido da v410, conferido contra o sandbox k411c", "sandbox": KB, "pos_build": {k_: POSB[k_] for k_ in ("ok", "linha_TOTAL", "audit_log_sha256", "duracao_build_s", "duracao_audit_s")}},
       "registros": list(DL.REGISTROS_FUNCAO) + spec_nomes, "falas_citadas": len(FALAS_CIT), "formal_files_n": len(FORMAL_MAP), "topo": {k_: TOPO[k_] for k_ in ("ratificado", "arquivo", "sha256")}, "topo_guarda": TOPO_GUARDA, "topo_p18": TOPO_P18,
       "h0dn": {"registro": DL.FECHO_REGISTRO, "n_checks": CONTR_H["n_checks"], "insumos": CONTR_H["insumos"], "bytes_embutidos_b64": sum(len(v_.get("b64", "")) for v_ in INS_H.values()), "reuso_v410": sorted(k_ for k_, v_ in INS_H.items() if "reuso_v410" in v_), "citados": CONTR_H["citados"]},
       "h8": {"entradas": len(H8), "embutidas": len(FORMAL_MAP), "residuais_do_nos": sorted(set(H8) - set(FORMAL_MAP)), "igual_ao_pino_da_v410": H8_IGUAL_AO_DA_V410, "pino_antigo_v410_entradas": H8_ANTIGO_N, "arvore_simulada": SIMD},
       "gate_nao_se_move": {"funcoes_identicas_a_base": list(INTOCADAS_V411), "gate_verdict_v410": selo0.get("qg_closure_verdict")}, "guardas_estaticas_da_bancada": {"esboco": ESBOCO, "esboco_sha256": ESBOCO_SHA256, "base_v410": g0, "candidato_v411": g1, "alfa_lido": a1_.group(1), "versao_lida": v1_.group(1)},
       "guarda_frases": {"controle_negativo": bool(G0_["ok"]), "violacoes_no_texto_novo": len(V_GF), "violacoes_no_texto_renderizado": RENDER_VIOL, "partes_renderizadas": {k_: len(v_) for k_, v_ in RENDER.items()}}, "p18_no_runtime_so_a_cabeca_pre_registrada": len(_p18_novo) - len(_p18_novo_fora_do_topo), "ajuste_n10_espacos_no_fim_do_comentario_da_versao": K_N10,
       "contratos_de_registro_fora_da_escada": list(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA), "runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "quando": datetime.datetime.now().isoformat(timespec="seconds"), **DL.MARCA_ENSAIO}
if PREVOO:
    pv = os.path.join(HERE, "PREVOO_GERADOR_v411.json")
    man_pv = dict(man, contrato="PREVOO_GERADOR_v411", nota="PRE-VOO com o texto PROPOSTO do topo (DESENHO 5.1 b), pendente da palavra do operador: NENHUM candidato gravado; o sha16 acima e' do texto que SERIA gerado com a proposta", ok=True)
    open(pv + ".tmp", "w", encoding="utf-8").write(json.dumps(man_pv, ensure_ascii=False, indent=1)); os.replace(pv + ".tmp", pv)
    print(json.dumps({k: man_pv[k] for k in ("contrato", "sha16", "bytes", "n_patches", "escada", "registros", "falas_citadas", "topo_guarda")}, ensure_ascii=False, indent=1)); print("patches:", [e[3] for e in EDITS])
    sys.exit(0)
out = DL.CANDIDATO_ARQ
assert not ENSAIO or os.path.normcase(DL.WK) not in os.path.normcase(os.path.abspath(out)), "o artefato de ensaio nao pode ficar em work"
assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V411_REGERAR") == "1" or ENSAIO, "o candidato ja existe e difere: defina V411_REGERAR=1 para regerar"
if os.path.exists(out) and open(out, "rb").read() != b:
    shutil.copyfile(out, out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
open(DL.MANIFESTO_ARQ + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(DL.MANIFESTO_ARQ + ".tmp", DL.MANIFESTO_ARQ)
open(DL.FORMAL_MAP_ARQ + ".tmp", "w", encoding="utf-8").write(json.dumps(FORMAL_MAP, ensure_ascii=False, indent=0)); os.replace(DL.FORMAL_MAP_ARQ + ".tmp", DL.FORMAL_MAP_ARQ)
open(DL.PINS_ARQ + ".tmp", "w", encoding="utf-8", newline="\n").write(RT_); os.replace(DL.PINS_ARQ + ".tmp", DL.PINS_ARQ)
if ENSAIO:
    print("ENSAIO do topo proposto: o ARTEFATO (NAO candidato) em", out)
print(json.dumps({k: man[k] for k in ("sha16", "bytes", "base_v410_sha16", "escada", "registros", "falas_citadas")}, ensure_ascii=False, indent=1))
print("patches (%d):" % len(EDITS), [e[3] for e in EDITS])
