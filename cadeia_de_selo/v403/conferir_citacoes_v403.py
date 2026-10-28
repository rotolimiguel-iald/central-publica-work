# -*- coding: utf-8 -*-
"""conferir_citacoes_v403.py -- confere, por script, toda inscricao de 27/10/2026 que a v403 EMBUTE ou CITA (regua nº 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): (a) cada texto embutido em _V403_VERBATINS2 e' IGUAL, byte a byte, ao arquivo
duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original (work\\cunhagens_13out) existe e tem o MESMO sha256; (c) cada fala de `leituras_do_operador` do registro cunhagens_v403 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente
as duas inscricoes (todas falas do operador: nenhuma e' da gerencia); (e) as citacoes do operador dos .pysnip existem nos snippets e a fala correspondente esta VERBATIM nos textos do operador; (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE
da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas, no texto do kernel embutido na base (e os textos da v402 que as erratas citam),
no adendo de 03-04/09, nas fontes das tres pedras, no CLAUDE.md da casa (a regua de beta que a pedra do Nome cita) ou ser rotulo da propria cadeia. Sai 0 se tudo bate. Escrito a mao para a v403 (molde: conferir_citacoes_v402.py)."""
import ast, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v403 as DL  # noqa: E402
pins = open(os.path.join(HERE, "v403_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v403 como esta no CANDIDATO (extraido por gerar_candidato_v403.py)
ns = {}
alvo = {"_V403_VERBATINS2", "_V403_SPECS", "_V403_CONTRACTS"}
for n in tree.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
        ns[n.targets[0].id] = ast.literal_eval(n.value)
V = ns["_V403_VERBATINS2"]; R = {"verbatins": {}, "leituras": {}, "snippets": {}}; ok = True
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
R["n_inscricoes_embutidas"] = len(V); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V403) == 2
R["nenhuma_e_da_gerencia_as_duas_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).startswith("OPERADOR_27out_") for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_as_duas_sao_do_operador"]
cg = [s for s in ns["_V403_SPECS"] if s["nome"] == "cunhagens_v403"][0]
for it in cg["leituras_do_operador"]:
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"]["cunhagens_v403: " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
# as citacoes do operador nos snippets: o fragmento PRECISA estar no snippet e verbatim nos textos do operador (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo)
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_KERN = _norm(_base.replace("**", ""))
_ADENDO = _norm(open(DL.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
_PEDRAS = _norm(" ".join(open(s["src"], encoding="utf-8").read() for s in DL.STONES).replace("**", "").replace("`", ""))
_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
CIT_OP = ["a meu ver o nome é", DL.FRASE_CONCORDO]   # (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo; a fala de 27/10 traz o resto)
for lang in ("pt", "en"):
    sn = open(os.path.join(HERE, "artigo_%s_v403.pysnip" % lang), encoding="utf-8").read()
    sn_flat = _norm(sn.replace("\\texttt{", "").replace("\\emph{", ""))
    R["snippets"][lang] = {}
    for frag in CIT_OP:
        presente = _norm(frag) in sn_flat.replace("}", "") or _norm(frag) in sn_flat
        achou = presente and _norm(frag) in _norm(todos_op)
        R["snippets"][lang][frag[:50]] = {"citacao_presente_no_snippet": bool(presente), "trecho_verbatim_na_fala_do_operador": _norm(frag) in _norm(todos_op)}; ok = ok and bool(achou)
# (f) o QUADRO (4,44, v397) segue com a frase VERBATIM do operador; a parafrase da gerencia nao aparece em nenhum artefato novo
q444 = open(os.path.join(DL.WK, "cunhagens_13out", "OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt"), encoding="utf-8").read()
rq = open(os.path.join(HERE, "runtime_quadro_v397.py"), encoding="utf-8").read()
nsq = {}; exec(compile(rq, "<runtime_quadro_v397>", "exec"), nsq)
R["frase_do_quadro_verbatim_na_fala_de_23out"] = nsq["_V397_FRASE_444"] in re.sub(r"\s+", " ", q444) and nsq["_V397_FRASE_444"] == DL.FRASE_DO_OPERADOR_4_44; ok = ok and R["frase_do_quadro_verbatim_na_fala_de_23out"]
PARAFRASE = "5σ é o cala a boca"   # «o 5σ é o cala a boca; 4,44 é um silêncio...» (parafrase da gerencia, NAO verbatim)
arts = ["runtime_v403.py", "artigo_pt_v403.pysnip", "artigo_en_v403.pysnip", "registros_v403.py", "delta_v403.py", "gerar_candidato_v403.py", "v403_pins.py"]
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas, no kernel embutido da base (que contem os textos da v402 que as erratas citam), no adendo,
# nas fontes das tres pedras, no CLAUDE.md da casa, ou ser rotulo da propria cadeia (titulos, nomes de registros).
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in glob.glob(os.path.join(DL.WK, "cunhagens_13out", "*OPERADOR_*.txt")))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)", "o testemunho de dois: o selo pela própria tecnologia", "the testimony of two: sealing by its own technology", "o testemunho de dois: o selo pela propria tecnologia",
            "o testemunho de dois: o selo pela propria tecnologia (v399)", "nenhuma face sozinha dá o um", "nenhuma face sozinha da' o um", "nenhuma face sozinha da o um",
            "beta do runtime", "β do runtime", "$\\beta$ do runtime", "$\\beta$ of the runtime", "errata ao lado (v400)",
            "a falsidade (simulacro) da inércia", "a falsidade (simulacro) da inercia", "a falsidade (simulacro) da inercia (v402)", "the falsity (simulacrum) of inertia", "falsidade (simulacro) da inércia", "falsidade (simulacro) da inercia",
            # v403: titulos e rotulos da propria cadeia; as aspas de ENFASE dos textos novos; a TRADUCAO inglesa de citacoes em portugues (que no EN vem seguida do original)
            "a ponte da escala dual, a queda sem geometria e a esperança condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional (v403)",
            "the dual-scale bridge, the fall without geometry and the conditional expectation", "inertial", "movimento livre", "free motion", "e = mc^2 composta da escala", "$e=mc^2$ composta da escala", "$e=mc^2$ composed from the scale", "e = mc^2 composed from the scale",
            "does the posted one have a direction?", "the arrow of the fall of the phase, not of space", "o um posto tem direção?", "o um posto tem direcao?", "a seta da queda da fase, não do espaço", "a seta da queda da fase, nao do espaco",
            "when it inscribes itself, it falls; the phase falls", "so it has direction, but not geometric", "the fall i want to translate is not a force either", "the one, when it is posted, performs the", "conditional expectation = name", "τ é a massa de newton", "$\\tau$ é a massa de newton", "$\\tau$ is newton's mass", "tau e' a massa de newton",
            # v403 (pos_rito): rotulos de consulta ao Mapa de Rotas e de erratas nos scripts do pos-rito (registrar_mapa, leitura); a frase em ASCII e' a da v402 citada pela errata E1 (os registros da v402 a escrevem com acentos)
            "ponte da escala dual", "esperanca condicional = nome", "a unica hipotese nomeada e' h_tau [open] (tau e' a massa de newton e a metrica de einstein), que nenhum teorema usa", "inercial = fixo por todos os boosts", "h_tau na forma literal refutada no kernel",
            # v403: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "caminho, verdade e vida (v403)", "caminho, verdade e vida", "way, truth and life"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
_limpa = lambda s: _norm(s.replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'").replace("\\texttt{", "").replace("\\emph{", "").replace("\\textsf{", "").replace("}", "").replace("**", "").replace("`", "")).replace(" --- ", " — ").strip(" .,;:")
_corpus_ok = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())
R["varredura_de_aspas"] = {}
for _a in ("runtime_v403.py", "artigo_pt_v403.pysnip", "artigo_en_v403.pysnip", "registros_v403.py", "delta_v403.py", "gerar_candidato_v403.py", "pos_rito/textos_v403.py", "pos_rito/registrar_mapa_v403.py", "pos_rito/fechar_v403.py", "pos_rito/leitura_v403.py", "pos_rito/superficies_v403.py"):
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V403_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _corpus_ok(_fr):
                continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (h) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v402 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia / texto do kernel / adendo / fonte das pedras / casa); citacao que a base ja' tem nao e' deste delta.
_cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read()
_bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
for _l in _novas:
    for _rx in _rxs:
        for _m in _rx.finditer(_l):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V403_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                continue
            if _corpus_ok(_fr):
                continue
            _nao_c.append(_fr[:140])
R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
R["todas_conferem"] = ok
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
