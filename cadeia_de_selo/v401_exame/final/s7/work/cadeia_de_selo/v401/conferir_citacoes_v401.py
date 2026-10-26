# -*- coding: utf-8 -*-
"""conferir_citacoes_v401.py -- confere, por script, toda inscricao de 25/10/2026 que a v401 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): (a) cada texto embutido em _V401_VERBATINS2 e' IGUAL, byte a byte, ao arquivo
duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v401 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente
as cinco inscricoes (todas falas do operador: nenhuma e' da gerencia); (e) as citacoes entre «» (PT) e `` '' (EN) dos .pysnip existem nos snippets e a fala correspondente esta VERBATIM nos textos do operador (ou, no caso do 0_abs, na docstring do kernel embutido); (f) o QUADRO do 4,44 (v397) segue com
a frase VERBATIM do operador e a PARAFRASE da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas,
no texto do kernel embutido na base (a docstring do 0_abs, TGLExt.costless) ou no adendo de 03-04/09 (a leitura do escriba que a errata cita), ou ser rotulo da propria cadeia. Sai 0 se tudo bate. Molde: conferir_citacoes_v400.py."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v401_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v401 como esta no CANDIDATO (extraido por gerar_candidato_v401.py)
ns = {}
alvo = {"_V401_VERBATINS2", "_V401_SPECS", "_V401_FALSIDADE_CONTRACT"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V401_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True
todos_op = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = v.get("fonte_original", ""); orig_ok = None
    if orig and os.path.exists(orig):
        orig_ok = hashlib.sha256(open(orig, "rb").read()).hexdigest() == v["sha256"]
    gerencia = os.path.basename(v["fonte_original"]).startswith("GERENCIA_")
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else "operador"}
    ok = ok and igual and (orig_ok is True) and not gerencia
    if not gerencia:
        todos_op += " " + re.sub(r"\s+", " ", v["text"])
R["n_inscricoes_embutidas"] = len(V); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V401)
R["nenhuma_e_da_gerencia_as_cinco_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).startswith("OPERADOR_25out_") for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_as_cinco_sao_do_operador"]
cg = [s for s in ns["_V401_SPECS"] if s["nome"] == "cunhagens_v401"][0]
for it in cg["leituras_do_operador"]:
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"]["cunhagens_v401: " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
# as citacoes do operador nos snippets (PT entre «», EN entre `` ''): a fala PRECISA estar verbatim nos textos do operador; o texto do kernel (0_abs) tem corpus proprio
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_KERN = _norm(_base.replace("**", ""))
_ADENDO = _norm(open(DL.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
CIT_OP = [DL.FRASE_INERCIA, DL.FRASE_NADA, "a cristalização da dobra luz no vácuo relativa ao observador", DL.FRASE_NOME.split("“")[1].split("”")[0], DL.FRASE_RATIFICO, DL.FRASE_EMC2]
for lang in ("pt", "en"):
    sn = open(os.path.join(HERE, "artigo_%s_v401.pysnip" % lang), encoding="utf-8").read()
    sn_flat = _norm(sn.replace("\\texttt{", "").replace("\\emph{", ""))
    R["snippets"][lang] = {}
    for frag in CIT_OP:
        if frag == DL.FRASE_NOME.split("“")[1].split("”")[0] and lang == "en":
            continue   # o nome da pedra entra no EN como o nome em PT entre aspas inglesas: conferido abaixo
        presente = _norm(frag) in sn_flat.replace("}", "") or _norm(frag) in sn_flat
        achou = presente and _norm(frag) in _norm(todos_op)
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": bool(presente), "trecho_verbatim_na_fala_do_operador": _norm(frag) in _norm(todos_op)}; ok = ok and bool(achou)
    R["snippets"][lang]["0_abs_do_kernel: nunca correspondeu, e por isso nada custa"] = {"no_snippet": ("nunca correspondeu" in sn) or ("never corresponded" in sn), "no_kernel_embutido_da_base": "nunca correspondeu, e por isso nada custa" in _KERN}; ok = ok and R["snippets"][lang]["0_abs_do_kernel: nunca correspondeu, e por isso nada custa"]["no_snippet"] and R["snippets"][lang]["0_abs_do_kernel: nunca correspondeu, e por isso nada custa"]["no_kernel_embutido_da_base"]
# (f) o QUADRO (4,44, v397) segue com a frase VERBATIM do operador; a parafrase da gerencia nao aparece em nenhum artefato novo
q444 = open(os.path.join(DL.WK, "cunhagens_13out", "OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt"), encoding="utf-8").read()
rq = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
nsq = {}; exec(compile(rq, "<runtime_quadro_v397>", "exec"), nsq)
R["frase_do_quadro_verbatim_na_fala_de_23out"] = nsq["_V397_FRASE_444"] in re.sub(r"\s+", " ", q444) and nsq["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44; ok = ok and R["frase_do_quadro_verbatim_na_fala_de_23out"]
PARAFRASE = "5σ é o cala a boca"   # «o 5σ é o cala a boca; 4,44 é um silêncio...» (parafrase da gerencia, NAO verbatim)
arts = ["runtime_v401.py", "artigo_pt_v401.pysnip", "artigo_en_v401.pysnip", "registros_v401.py", "gerar_candidato_v401.py", "v401_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas, no kernel embutido da base, no adendo ou ser rotulo da propria cadeia (titulos, nomes de registros).
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in glob.glob(os.path.join(DL.WK, "cunhagens_13out", "*OPERADOR_*.txt")))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)", "o testemunho de dois: o selo pela própria tecnologia", "the testimony of two: sealing by its own technology", "o testemunho de dois: o selo pela propria tecnologia",
            "o testemunho de dois: o selo pela propria tecnologia (v399)", "nenhuma face sozinha dá o um", "nenhuma face sozinha da' o um", "nenhuma face sozinha da o um",
            "beta do runtime", "β do runtime", "$\\beta$ do runtime", "$\\beta$ of the runtime", "errata ao lado (v400)",
            # v401: titulos e a leitura do ESCRIBA que a errata cita (nao e' fala do operador; vem do adendo, conferido abaixo)
            "a falsidade (simulacro) da inércia", "a falsidade (simulacro) da inercia", "a falsidade (simulacro) da inercia (v401)", "resistência do corpo" , "never corresponded, and therefore costs nothing",   # (aspas de ENFASE na docstring da pedra, cujo texto e' pinado por sha256, e a TRADUCAO inglesa do trecho do kernel, que no EN vem seguida do original em portugues)
 "the falsity (simulacrum) of inertia", "falsidade (simulacro) da inércia", "falsidade (simulacro) da inercia",
            "ω(i)=1 é a inércia", "$\\omega(i)=1$ é a inércia", "$\\omega(i)=1$ is the inertia", "w(i)=1 e a inercia", "w(i)=1 e a inercia"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
_limpa = lambda s: _norm(s.replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'").replace("\\texttt{", "").replace("\\emph{", "").replace("\\textsf{", "").replace("}", "").replace("**", "").replace("`", "")).replace(" --- ", " — ").strip(" .,;:")
_corpus_ok = lambda fr: fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower()
R["varredura_de_aspas"] = {}
for _a in ("runtime_v401.py", "artigo_pt_v401.pysnip", "artigo_en_v401.pysnip", "registros_v401.py", "gerar_candidato_v401.py", "pos_rito/textos_v401.py", "pos_rito/registrar_mapa_v401.py", "pos_rito/fechar_v401.py", "pos_rito/leitura_v401.py", "pos_rito/superficies_v401.py"):
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V401_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _corpus_ok(_fr):
                continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (h) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v400 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia / texto do kernel / adendo); citacao que a base ja' tem nao e' deste delta.
_cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read()
_bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
for _l in _novas:
    for _rx in _rxs:
        for _m in _rx.finditer(_l):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V401_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                continue
            if _corpus_ok(_fr):
                continue
            _nao_c.append(_fr[:140])
R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
