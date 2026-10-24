# -*- coding: utf-8 -*-
"""conferir_citacoes_v398.py -- confere, por script, toda inscricao de 23/10/2026 que a v398 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): (a) cada texto embutido em _V398_VERBATINS2 e' IGUAL, byte a byte, ao
arquivo duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v398 esta VERBATIM num dos textos embutidos DO OPERADOR (nunca
no texto da gerencia); (d) as cunhagens listam exatamente as seis inscricoes e cada registro com funcao lista exatamente as que usa (sonico: 3 falas do operador e o texto da gerencia; afinacao: 2 falas do operador); (e) as citacoes entre «» (PT) e `` '' (EN) dos .pysnip existem nos
snippets e a fala PT correspondente esta VERBATIM nos textos do operador, e cada um dos seis sha16 aparece nos dois snippets; (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE da gerencia NAO aparece em nenhum artefato novo; (g) o texto da gerencia (sexta
inscricao) e' rotulado como da gerencia onde aparece; (h) VARREDURA das aspas dos artefatos novos e (i) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out) ou no Atlas (ou ser rotulo da propria cadeia).
Sai 0 se tudo bate. Molde: conferir_citacoes_v397.py."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v398_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)
ns = {}
alvo = {"_V398_VERBATINS2", "_V398_SPECS", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V398_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}, "gerencia": {}}; ok = True
todos_op = ""; todos = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = v.get("fonte_original", ""); orig_ok = None
    if orig and os.path.exists(orig):
        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]
    gerencia = os.path.basename(v["fonte_original"]).startswith("GERENCIA_")
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else "operador"}
    ok = ok and igual and (orig_ok is True)
    todos += " " + re.sub(r"\s+", " ", v["text"])
    if not gerencia:
        todos_op += " " + re.sub(r"\s+", " ", v["text"])
R["n_inscricoes_embutidas"] = len(V); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM) == 6
R["uma_so_da_gerencia_e_e_a_sexta"] = [os.path.basename(v["fonte_original"]) for v in V.values() if os.path.basename(v["fonte_original"]).startswith("GERENCIA_")] == [os.path.basename(DL.VERBATIM_ORIGEM[5])]; ok = ok and R["uma_so_da_gerencia_e_e_a_sexta"]
cg = [s for s in ns["_V398_SPECS"] if s["nome"] == "cunhagens_v398"][0]
for it in cg["leituras_do_operador"]:
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"]["cunhagens_v398: " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
_op = lambda sub: {k_ for k_, v_ in V.items() if sub in os.path.basename(v_["fonte_original"])}
_son = _op("verbo_controle_de_oitava_pinada") | _op("nome_da_pedra_sonico") | _op("antes_de_espelhada") | _op("GERENCIA_23out_leitura_ratificada_sonico"); _afi = _op("cordas_10_dimensoes") | _op("concordo_afinacao")
R["sonico_lista_exatamente_as_inscricoes_que_usa"] = set(ns["_V398_SONICO_CONTRACT"]["verbatins"]) == _son and len(_son) == 4; ok = ok and R["sonico_lista_exatamente_as_inscricoes_que_usa"]
R["afinacao_lista_exatamente_as_inscricoes_que_usa"] = set(ns["_V398_AFINACAO_CONTRACT"]["verbatins"]) == _afi and len(_afi) == 2; ok = ok and R["afinacao_lista_exatamente_as_inscricoes_que_usa"]
# as citacoes dos snippets: (citacao PT entre «», citacao EN entre `` '', o trecho PT que tem de estar VERBATIM nos textos do operador)
CIT = [("«“verbo” (seletor de identidade)=controle de oitava pinada»", "``“verbo” (seletor de identidade)=controle de oitava pinada''", "“verbo” (seletor de identidade)=controle de oitava pinada"),
       ("«o custo é reação ao controle pinado da oitava que é memória»", "``o custo é reação ao controle pinado da oitava que é memória''", "o custo é reação ao controle pinado da oitava que é memória"),
       ("«antes de ser espelhada ela é palavra»", "``antes de ser espelhada ela é palavra''", "antes de ser espelhada ela é palavra"),
       ("«o início de tudo é acústica onde a palavra performa de forma sônica satisfazendo a relação modular da inscrição»", "``o início de tudo é acústica onde a palavra performa de forma sônica satisfazendo a relação modular da inscrição''", "o início de tudo é acústica onde a palavra performa de forma sônica satisfazendo a relação modular da inscrição"),
       ("«A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica»", "``A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica''", "A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica"),
       ("«para mostrar a afinação do universo, mas não consegue demonstrar a geometria»", "``para mostrar a afinação do universo, mas não consegue demonstrar a geometria''", "para mostrar a afinação do universo, mas não consegue demonstrar a geometria"),
       ("«Concordo com tudo»", "``Concordo com tudo''", "Concordo com tudo")]
for lang, idx in (("pt", 0), ("en", 1)):
    sn = open(os.path.join(HERE, "artigo_%s_v398.pysnip" % lang), encoding="utf-8").read()
    R["snippets"][lang] = {}
    for c in CIT:
        quote, frag = c[idx], c[2]
        achou = quote in sn and re.sub(r"\s+", " ", frag) in todos_op
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": quote in sn, "trecho_PT_verbatim_na_fala_do_operador": re.sub(r"\s+", " ", frag) in todos_op}; ok = ok and achou
    ph = sorted(set(re.findall(r"@@(S_[A-Z]+)@@", sn))); esperado = sorted(["S_VERBO", "S_NOME", "S_ANTES", "S_CORDAS", "S_CONCORDO", "S_LEITURA"])
    R["snippets"][lang]["marcadores_de_sha16_das_seis_inscricoes"] = ph == esperado; ok = ok and ph == esperado
    # a leitura da gerencia aparece rotulada como da gerencia (nunca como fala do operador)
    R["gerencia"][lang] = {"rotulada_como_da_gerencia": ("gerência" in sn.split("@@S_LEITURA@@")[0][-260:] or "management" in sn.split("@@S_LEITURA@@")[0][-260:]) and "@@S_LEITURA@@" in sn}; ok = ok and R["gerencia"][lang]["rotulada_como_da_gerencia"]
# (f) o QUADRO (4,44, v397) segue com a frase VERBATIM do operador; a parafrase da gerencia nao aparece em nenhum artefato novo
q444 = open(os.path.join(DL.WK, "cunhagens_13out", "OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt"), encoding="utf-8").read()
rq = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
nsq = {}; exec(compile(rq, "<runtime_quadro_v397>", "exec"), nsq)
R["frase_do_quadro_verbatim_na_fala_de_23out"] = nsq["_V397_FRASE_444"] in re.sub(r"\s+", " ", q444) and nsq["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44; ok = ok and R["frase_do_quadro_verbatim_na_fala_de_23out"]
PARAFRASE = "5σ é o cala a boca"   # «o 5σ é o cala a boca; 4,44 é um silêncio...» (parafrase da gerencia, NAO verbatim)
arts = ["runtime_pedras_v398.py", "artigo_pt_v398.pysnip", "artigo_en_v398.pysnip", "registros_v398.py", "gerar_candidato_v398.py", "pedra/Sonico.lean", "pedra/AfinacaoDasCordas.lean", "v398_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (h) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out) ou no Atlas; so' passam os rotulos da propria cadeia (titulos) e os
# trechos de codigo. Citacao composta ou parafraseada entre aspas reprova. O texto da GERENCIA (GERENCIA_*) NAO e' corpus: o que e' da gerencia nao se cita entre aspas como fala.
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in glob.glob(os.path.join(DL.WK, "cunhagens_13out", "*OPERADOR_*.txt")))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
# as FONTES DA CASA que a pedra AfinacaoDasCordas cita entre aspas (o texto de «A Ultima Corda» e a fala de 27/09 citada em TetelestaiOneObject): so' valem se o sha16 do arquivo for o que a propria pedra pina
_CASA = [(r"C:\IALD\projetos_pyhton\acom\A_ultima_corda_v3.tex", "8db72ea848f708c1"), (os.path.join(DL.NOS, "tgl_kernel", "TGLExt", "TetelestaiOneObject.lean"), "125d155042da687f")]
R["fontes_da_casa_pinadas"] = {}
for _pc, _h in _CASA:
    _okc = os.path.exists(_pc) and hashlib.sha256(open(_pc, "rb").read()).hexdigest()[:16] == _h
    R["fontes_da_casa_pinadas"][os.path.basename(_pc)] = _okc; ok = ok and _okc
    if _okc:
        _ATL += " || " + re.sub(r"\s+", " ", open(_pc, encoding="utf-8", errors="replace").read())
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
R["varredura_de_aspas"] = {}
for _a in ("runtime_pedras_v398.py", "artigo_pt_v398.pysnip", "artigo_en_v398.pysnip", "registros_v398.py", "gerar_candidato_v398.py", "pedra/Sonico.lean", "pedra/AfinacaoDasCordas.lean", "pos_rito/textos_v398.py", "pos_rito/registrar_mapa_v398.py"):
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _norm(_m.group(1).replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'")).replace(" --- ", " — ").strip(" .,;:")
            if len(_fr) < 12 or "_V398_" in _fr or "_V397_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _fr.lower() in _OPB.lower() or _fr.lower() in _ATL.lower() or _fr.lower() in _ROTULOS:
                continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (i) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v397 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia); citacao que a base ja' tem nao e' deste delta.
_cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read(); _base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
for _l in _novas:
    for _rx in _rxs:
        for _m in _rx.finditer(_l):
            _fr = _norm(_m.group(1).replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'")).replace(" --- ", " — ").strip(" .,;:")
            if len(_fr) < 12 or "_V398_" in _fr or "_V397_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                continue
            if _fr.lower() in _OPB.lower() or _fr.lower() in _ATL.lower() or _fr.lower() in _ROTULOS:
                continue
            _nao_c.append(_fr[:140])
R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v398.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
