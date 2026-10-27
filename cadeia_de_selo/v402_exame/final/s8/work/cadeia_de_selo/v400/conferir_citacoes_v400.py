# -*- coding: utf-8 -*-
"""conferir_citacoes_v400.py -- confere, por script, toda inscricao de 24/10/2026 que a v400 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia; nunca inverter a DIRECAO do testemunho): (a) cada texto embutido em _V399_VERBATINS2 e' IGUAL, byte a
byte, ao arquivo duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v399 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente as
quatro inscricoes (todas falas do operador: nenhuma e' da gerencia) e a fala da DECLARACAO embutida em _V399_DECLARACAO_TXT e' IGUAL, byte a byte, a quarta inscricao (sha256 == _V399_DECLARACAO_SHA256); (e) as citacoes entre «» (PT) e `` '' (EN) dos .pysnip existem nos snippets e a fala correspondente esta
VERBATIM nos textos do operador, e cada um dos quatro sha16 aparece nos dois snippets; (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE da gerencia NAO aparece em nenhum artefato novo; (g) a DIRECAO: nenhuma frase dos artefatos novos poe a IALD como quem testifica DO operador, fora
da fala em que ele a recusa; (h) VARREDURA das aspas dos artefatos novos e (i) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out) ou no Atlas (ou ser rotulo da propria cadeia). Sai 0 se tudo bate. Molde: conferir_citacoes_v399.py."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v400_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v399 como esta no CANDIDATO v400 (extraido por gerar_candidato_v400.py)
ns = {}
alvo = {"_V399_VERBATINS2", "_V399_SPECS", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V399_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}, "direcao": {}}; ok = True
todos_op = ""; todos = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = v.get("fonte_original", ""); orig_ok = None
    if orig and os.path.exists(orig):
        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]
    gerencia = os.path.basename(v["fonte_original"]).startswith("GERENCIA_")
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else "operador"}
    ok = ok and igual and (orig_ok is True) and not gerencia
    todos += " " + re.sub(r"\s+", " ", v["text"])
    if not gerencia:
        todos_op += " " + re.sub(r"\s+", " ", v["text"])
R["n_inscricoes_embutidas"] = len(V); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM) == 4
R["nenhuma_e_da_gerencia_as_quatro_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).startswith("OPERADOR_24out_") for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_as_quatro_sao_do_operador"]
# a DECLARACAO embutida (a fala do registro declaracao_do_operador_v399) == a quarta inscricao, byte a byte
decl_v = [v for v in V.values() if os.path.basename(v["fonte_original"]) == os.path.basename(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX])]
R["declaracao_embutida_igual_a_quarta_inscricao"] = bool(len(decl_v) == 1 and ns["_V399_DECLARACAO_TXT"] == decl_v[0]["text"] and hashlib.sha256(ns["_V399_DECLARACAO_TXT"].encode("utf-8")).hexdigest() == ns["_V399_DECLARACAO_SHA256"] == decl_v[0]["sha256"]
                                                         and hashlib.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()).hexdigest() == ns["_V399_DECLARACAO_SHA256"]); ok = ok and R["declaracao_embutida_igual_a_quarta_inscricao"]
cg = [s for s in ns["_V399_SPECS"] if s["nome"] == "cunhagens_v399"][0]
for it in cg["leituras_do_operador"]:
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"]["cunhagens_v399: " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
# as citacoes dos snippets: (citacao PT entre «», citacao EN entre `` '', o trecho que tem de estar VERBATIM nos textos do operador). A declaracao fica em PORTUGUES nos dois (a traducao, sem aspas, e' da gerencia).
DECL = "o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD"
CIT = [("«" + DECL + "»", "``" + DECL + "''", DECL)]
for lang, idx in (("pt", 0), ("en", 1)):
    sn = open(os.path.join(DL.V399, "artigo_%s_v399.pysnip" % lang), encoding="utf-8").read()
    R["snippets"][lang] = {}
    for c in CIT:
        quote, frag = c[idx], c[2]
        achou = quote in sn and re.sub(r"\s+", " ", frag) in todos_op
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": quote in sn, "trecho_verbatim_na_fala_do_operador": re.sub(r"\s+", " ", frag) in todos_op}; ok = ok and achou
    ph = sorted(set(re.findall(r"@@(S_[A-Z]+)@@", sn))); esperado = sorted(["S_JOAO", "S_HASH", "S_DECL"])
    R["snippets"][lang]["marcadores_de_sha16_das_inscricoes_citadas"] = ph == esperado; ok = ok and ph == esperado
    # (g) a direcao do testemunho dita no snippet e sem inversao
    dir_ok = bool(re.search(r"(testifica \\emph\{(da|of)\} (a )?(the )?IALD|testifica \\emph\{(da|of)\} (the )?IALD)", sn) or ("testifica \\emph{da} IALD" in sn) or ("testifies \\emph{of} the IALD" in sn))
    nao_ok = ("A IALD \\emph{não} testifica do operador" in sn) if lang == "pt" else ("The IALD does \\emph{not} testify of the operator" in sn)
    R["direcao"][lang] = {"o_operador_testifica_da_IALD": dir_ok, "a_IALD_nao_testifica_do_operador": nao_ok}; ok = ok and dir_ok and nao_ok
# (f) o QUADRO (4,44, v397) segue com a frase VERBATIM do operador; a parafrase da gerencia nao aparece em nenhum artefato novo
q444 = open(os.path.join(DL.WK, "cunhagens_13out", "OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt"), encoding="utf-8").read()
rq = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
nsq = {}; exec(compile(rq, "<runtime_quadro_v397>", "exec"), nsq)
R["frase_do_quadro_verbatim_na_fala_de_23out"] = nsq["_V397_FRASE_444"] in re.sub(r"\s+", " ", q444) and nsq["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44; ok = ok and R["frase_do_quadro_verbatim_na_fala_de_23out"]
PARAFRASE = "5σ é o cala a boca"   # «o 5σ é o cala a boca; 4,44 é um silêncio...» (parafrase da gerencia, NAO verbatim)
arts = ["runtime_v400.py", "artigo_pt_v400.pysnip", "artigo_en_v400.pysnip", "registros_v400.py", "gerar_candidato_v400.py", "montar_runtime_v400.py", "v400_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) a DIRECAO nos artefatos novos: nenhuma frase poe a IALD como quem testifica DO operador, fora da fala em que ele a RECUSA («eu nao podia dizer que IALD testifica a mim»)
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)", re.I)
inv = {}
for a in arts + ["pos_rito/textos_v400.py", "pos_rito/registrar_mapa_v400.py"]:
    p = os.path.join(HERE, *a.split("/"))
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8", errors="replace").read(); ruins = []
    for m in _RX_INV.finditer(t):
        ant = t[max(0, m.start() - 40):m.start()].lower()
        if not (ant.endswith("nao ") or ant.endswith("não ") or "podia dizer que " in ant):
            ruins.append(t[max(0, m.start() - 40):m.end() + 20].replace("\n", " "))
    inv[a] = ruins; ok = ok and not ruins
R["direcao"]["inversao_nos_artefatos_novos"] = inv
# (h) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out) ou no Atlas; so' passam os rotulos da propria cadeia (titulos) e os
# trechos de codigo. Citacao composta ou parafraseada entre aspas reprova. O texto da GERENCIA (GERENCIA_*) NAO e' corpus: o que e' da gerencia nao se cita entre aspas como fala.
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in glob.glob(os.path.join(DL.WK, "cunhagens_13out", "*OPERADOR_*.txt")))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)", "o testemunho de dois: o selo pela própria tecnologia", "the testimony of two: sealing by its own technology", "o testemunho de dois: o selo pela propria tecnologia",
            "o testemunho de dois: o selo pela propria tecnologia (v399)", "nenhuma face sozinha dá o um", "nenhuma face sozinha da' o um", "nenhuma face sozinha da o um",
            "beta do runtime", "β do runtime", "$\\beta$ do runtime", "$\\beta$ of the runtime", "errata ao lado (v400)"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
R["varredura_de_aspas"] = {}
for _a in ("runtime_v400.py", "artigo_pt_v400.pysnip", "artigo_en_v400.pysnip", "registros_v400.py", "gerar_candidato_v400.py", "pos_rito/textos_v400.py", "pos_rito/registrar_mapa_v400.py"):
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _norm(_m.group(1).replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'")).replace(" --- ", " — ").strip(" .,;:")
            if len(_fr) < 12 or "_V400_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _fr.lower() in _OPB.lower() or _fr.lower() in _ATL.lower() or _fr.lower() in _ROTULOS:
                continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (i) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v399 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia); citacao que a base ja' tem nao e' deste delta.
_cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read(); _base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
for _l in _novas:
    for _rx in _rxs:
        for _m in _rx.finditer(_l):
            _fr = _norm(_m.group(1).replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'")).replace(" --- ", " — ").strip(" .,;:")
            if len(_fr) < 12 or "_V400_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                continue
            if _fr.lower() in _OPB.lower() or _fr.lower() in _ATL.lower() or _fr.lower() in _ROTULOS:
                continue
            _nao_c.append(_fr[:140])
R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
