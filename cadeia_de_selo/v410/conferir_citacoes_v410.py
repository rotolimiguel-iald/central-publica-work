# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026 (subida mecanica de rotulo do molde v409/conferir_citacoes_v409.py; ver bump/conferir_citacoes_v410.py.diff) e 09/11/2026 pelo fork C do pos-rito, a servico da gerencia c1] a marca de adaptacao pendente saiu: o conferidor le agora o bloco v410 do candidato (_V410_VERBATINS2, _V410_SPECS, _V410_IALD2_TEXT, _V410_H0DN_TEXT), as QUINZE falas de 06 a 09/11 (de quatro so' o trecho: modos sufixo e meio), a pedra IALD2 (uma so'), os dois snippets PT (a secao da IALD2 e a do H0DN x BG1) e as citacoes minimas da v410; a varredura das aspas cobre tambem os arquivos do H0DN; o modo --sem-candidato roda o que NAO precisa do candidato
# [ADAPTADO v410, 05/11/2026, claude-construtor-v410] as dez falas de 05/11 (de duas, so' o trecho da D59; o caminho real pela chave, via delta_v410), as citacoes minimas do snippet PT da v410 e os rotulos da secao nova; o resto do conferidor e' o da v409
"""conferir_citacoes_v410.py -- confere, por script, toda inscricao do operador que a v410 EMBUTE ou CITA (regua n 1: nunca fabricar citacao; nunca atribuir ao operador o que e' da gerencia): as QUINZE falas de 06, 07, 08 e 09/11/2026 (_V410_VERBATINS2; DL.verbatins410);
de QUATRO so' o trecho e' embutido e citado (D65: o nome do algoritmo, modo `sufixo`; e, modo `meio`, em que o trecho esta' NO MEIO do arquivo: a ordem da retomada de 09/11, as tres copias do ACOM de 08/11 e a leitura do 5 sigma de 09/11); o arquivo inteiro entra so' por sha256;
o caminho real da origem vem de delta_v410.verbatins410, porque o embutido traz um rotulo neutro (D59/D65). (a) cada texto embutido e' IGUAL, byte a byte, ao arquivo duravel da cadeia (insumos\\cunhagens) e o sha256 bate; (b) a fonte original existe, tem o sha256 do arquivo inteiro e, nas quatro de so' o trecho, o trecho embutido e' EXATAMENTE o
que o delta manda (o texto e' o trecho mais o fim de linha; ocorre uma so' vez na origem; no modo sufixo, e' o fim da fala) e e' menor que o arquivo; (c) cada fala de `leituras_do_operador` do registro cunhagens_v410 esta VERBATIM num dos textos embutidos DO OPERADOR; (d) as cunhagens listam exatamente as inscricoes embutidas;
(e) TODA citacao « » dos DOIS snippets PT (a secao da IALD2 e a do H0DN x BG1, DL.FRASES_V410 e as minimas) esta VERBATIM nos textos do operador embutidos; os snippets EN trazem traducao da gerencia, marcada como nao-citacao, e nenhuma fala entre aspas « »; (f) o QUADRO do 4,44 (v397) segue com a frase VERBATIM do operador e a PARAFRASE
da gerencia NAO aparece em nenhum artefato novo; (g) VARREDURA das aspas dos artefatos novos (inclusive os do registro H0DN, D72) e (h) do CANDIDATO inteiro: toda citacao entre « » e `` '' tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (as pastas das falas e as copias duraveis da v410), no Atlas, no texto do kernel embutido na base,
no adendo de 03-04/09, nas fontes da pedra, no CLAUDE.md da casa ou ser rotulo da propria cadeia; (i) a docstring da pedra IALD2 (provas da gerencia c1, nome do operador; os nomes das declaracoes RATIFICADOS em 09/11, D74): toda citacao entre « » dela tem de existir verbatim nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa,
com a pedra FORA do corpus (o que nao e' fala e' rotulo listado; o que nao e' verbatim nem rotulo e' apontado a gerencia, que e' quem corrige pedra; o agente nao corrige).
O QUE EXIGE DO CANDIDATO: v410_pins.py (o bloco v410 extraido do candidato por gerar_candidato_v410.py, com _V410_VERBATINS2, _V410_SPECS, _V410_IALD2_TEXT e _V410_H0DN_TEXT), CANDIDATO_v410.json, um_v410_candidato.py, base_v409/um.py, as copias duraveis em insumos\\cunhagens, os dois snippets PT e os dois EN, runtime_quadro_v397.py e pedra\\IALD2.lean.
MODO `--sem-candidato` (ENSAIO; nada e' gravado; rc 0 so' se tudo o que NAO precisa do candidato conferir): usa as 15 falas de DL.verbatins410 no lugar do bloco embutido, nao le v410_pins.py nem o candidato e nao faz o passo (h); serve para a gerencia ver, antes do candidato, o que a varredura reprovaria.
Sai 0 se tudo bate. Molde: conferir_citacoes_v409.py."""
import ast, glob, hashlib, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
SEM_CAND = "--sem-candidato" in sys.argv   # ENSAIO: nao le v410_pins.py nem o candidato; nada e' gravado (ver o docstring)
_VD = DL.verbatins410(os.path.join(HERE, "insumos", "cunhagens"))   # as QUINZE falas LIDAS dos arquivos de origem (D65: de quatro so' o trecho; o texto embutido e' o trecho mais o fim de linha)
_ORIG = {v_["chave"]: v_["fonte_original"] for v_ in _VD}   # (v410, D59) o caminho REAL de cada fala, pela chave; o embutido traz um rotulo neutro
_NOME = {v_["chave"]: v_["nome"] for v_ in _VD}   # o nome de origem (a chave de DL.VERBATIM_SO_O_TRECHO)
if not SEM_CAND:
    pins = open(os.path.join(HERE, "v410_pins.py"), encoding="utf-8").read(); tree = ast.parse(pins)   # o bloco v410 como esta no CANDIDATO (extraido por gerar_candidato_v410.py)
    CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8"))
    ns = {}
    alvo = {"_V410_VERBATINS2", "_V410_SPECS", "_V410_IALD2_TEXT", "_V410_H0DN_TEXT"}   # as falas embutidas, os specs (cunhagens e cobertura) e os textos dos DOIS registros com funcao (D72)
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id in alvo:
            ns[n.targets[0].id] = ast.literal_eval(n.value)
    assert alvo <= set(ns), ("o bloco v410 (v410_pins.py) nao traz os nomes esperados", sorted(alvo - set(ns)))
    V = ns["_V410_VERBATINS2"]
else:   # as falas embutidas SERIAM as do delta (o que o gerador embute); as cunhagens listariam todas as frases de DL.FRASES_V410
    V = {v_["chave"]: {"arquivo": v_["arquivo"], "text": v_["text"], "sha256": v_["sha256"], "bytes": v_["bytes"], "fonte_original": "work\\cunhagens_13out\\" + v_["nome_publico"],
                      **({"sha256_arquivo_inteiro": v_["sha256_arquivo_inteiro"], "so_o_trecho": v_["so_o_trecho"]} if v_.get("so_o_trecho") else {})} for v_ in _VD}
    CM = {"verbatins_embutidos": len(V), "kernel": {"modulos_novos": DL.N_BUNDLE}}
    ns = {"_V410_SPECS": [{"nome": DL.CUNHAGENS_REGISTRO, "leituras_do_operador": [{"trecho": fr_} for _, fr_ in DL.FRASES_V410], "verbatins": sorted(V)}]}
R = {"verbatins": {}, "leituras": {}, "snippets": {}, "modo": ("ENSAIO --sem-candidato (nada gravado)" if SEM_CAND else "candidato")}; ok = True
todos_op = ""
for k, v in V.items():
    b = open(v["arquivo"], "rb").read()
    igual = hashlib.sha256(b).hexdigest() == v["sha256"] and b.decode("utf-8") == v["text"]
    orig = _ORIG.get(k, ""); orig_ok = None; misto = "sha256_arquivo_inteiro" in v; par_ok = None
    if orig and os.path.exists(orig):
        _ob = open(orig, "rb").read(); orig_ok = hashlib.sha256(_ob).hexdigest() == (v.get("sha256_arquivo_inteiro") or v["sha256"])
        if misto:   # (v410, D65 e os AO LADO de 09/11) so' o trecho: o texto embutido e' EXATAMENTE o trecho do delta mais o fim de linha, ocorre uma so' vez na origem, e e' menor que ela; no modo `sufixo` (D65) o trecho e' o fim da fala; no modo `meio` ele esta' no meio (nenhuma posicao e' exigida)
            _ot = _ob.decode("utf-8"); _modo, _trecho, _ = DL.VERBATIM_SO_O_TRECHO[_NOME[k]]
            par_ok = bool(v["text"] == _trecho + "\n" and _ot.count(_trecho) == 1 and len(v["text"].encode("utf-8")) < len(_ob) and v.get("so_o_trecho") and (_modo != "sufixo" or _ot.rstrip().endswith(_trecho)))
    gerencia = os.path.basename(orig).startswith("GERENCIA_")
    R["verbatins"][k] = {"embutida_igual_ao_arquivo": igual, "fonte_original_igual": orig_ok, "autor": "gerencia" if gerencia else ("operador; so' o trecho e' embutido (D65, a ordem da retomada, as tres copias do ACOM, a leitura do 5 sigma)" if misto else "operador"), "so_o_trecho": misto, "trecho_confere_com_o_arquivo": par_ok}
    ok = ok and igual and (orig_ok is True) and not gerencia and (par_ok is True if misto else True)
    if not gerencia:
        todos_op += " " + re.sub(r"\s+", " ", v["text"])
# (D80, parte 1 da D82) a ratificacao do HMS/13 e' fala do operador PINADA por sha256 no delta (lido do DESENHO) e no registro h0dn_fontes_hms13_v410, ainda fora das inscricoes embutidas (entra como inscricao na parte 2, 15 -> 20): o arquivo e' LIDO e conferido por sha256 aqui, e o seu texto entra no acervo de falas contra o qual as citacoes dos snippets sao conferidas
_rb = open(DL.HMS13_RATIFICACAO_ARQ, "rb").read(); R["ratificacao_hms13_lida_por_sha256"] = hashlib.sha256(_rb).hexdigest() == DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO; ok = ok and R["ratificacao_hms13_lida_por_sha256"]
R["ratificacao_hms13_trecho_uma_vez_e_no_fim"] = _rb.decode("utf-8").count(DL.HMS13_TRECHO_RATIFICACAO) == 1 and _rb.decode("utf-8").rstrip().split("\n")[-1].strip().endswith("HANDOFF_CLAUDE_UMPY_HMS_13.json"); ok = ok and R["ratificacao_hms13_trecho_uma_vez_e_no_fim"]
if R["ratificacao_hms13_lida_por_sha256"]:
    todos_op += " " + re.sub(r"\s+", " ", _rb.decode("utf-8"))
R["n_inscricoes_embutidas"] = len(V); R["n_so_o_trecho"] = sum(1 for v_ in V.values() if "sha256_arquivo_inteiro" in v_); ok = ok and len(V) == len(DL.VERBATIM_ORIGEM_V410) == DL.N_FALAS_V410 == CM["verbatins_embutidos"] and R["n_so_o_trecho"] == len(DL.VERBATIM_SO_O_TRECHO)
R["as_inscricoes_embutidas_sao_as_de_DL_pelo_sha16_da_ordem"] = sorted(k_[len(DL.VERBATIM_CHAVE_PREFIXO_V410):] for k_ in V) == sorted(DL.VERBATIM_PREFIXOS_DA_ORDEM_V410.values()); ok = ok and R["as_inscricoes_embutidas_sao_as_de_DL_pelo_sha16_da_ordem"]
R["o_sha16_de_cada_inscricao_e_o_da_ordem"] = all((v_.get("sha256_arquivo_inteiro") or v_["sha256"])[:16] == k_[len(DL.VERBATIM_CHAVE_PREFIXO_V410):] for k_, v_ in V.items()); ok = ok and R["o_sha16_de_cada_inscricao_e_o_da_ordem"]   # (a chave e' o sha16 do ARQUIVO INTEIRO, o do DESENHO; nas de autor misto o sha256 do texto embutido e' o do paragrafo)
R["nenhuma_e_da_gerencia_todas_sao_do_operador"] = all(os.path.basename(v["fonte_original"]).split("OPERADOR_")[0] in ("", os.path.basename(v["fonte_original"]).split("_")[0] + "_") and "OPERADOR_" in os.path.basename(v["fonte_original"]) for v in V.values()); ok = ok and R["nenhuma_e_da_gerencia_todas_sao_do_operador"]
cg = [s for s in ns["_V410_SPECS"] if s["nome"] == DL.CUNHAGENS_REGISTRO][0]
for it in list(cg["leituras_do_operador"]):   # (as leituras da gerencia [ONTO] nao sao citacao: nao entram aqui)
    achou = re.sub(r"\s+", " ", it["trecho"]) in todos_op
    R["leituras"][DL.CUNHAGENS_REGISTRO + ": " + it["trecho"][:60]] = "VERBATIM (fala do operador)" if achou else "NAO ACHADA NAS FALAS DO OPERADOR"; ok = ok and achou
R["leituras_do_operador_n"] = len(cg["leituras_do_operador"]); ok = ok and len(cg["leituras_do_operador"]) > 0
R["as_frases_de_DL_estao_nas_leituras"] = {fr_: any(re.sub(r"\s+", " ", fr_) == re.sub(r"\s+", " ", it["trecho"]) or re.sub(r"\s+", " ", fr_) in re.sub(r"\s+", " ", it["trecho"]) for it in cg["leituras_do_operador"]) for _, fr_ in DL.FRASES_V410}; ok = ok and all(R["as_frases_de_DL_estao_nas_leituras"].values()) and len(R["as_frases_de_DL_estao_nas_leituras"]) == len({fr_ for _, fr_ in DL.FRASES_V410}) > 0   # (v410: TODAS as frases de DL.FRASES_V410 sao leituras do registro cunhagens_v410)
R["cunhagens_listam_todas_as_inscricoes_embutidas"] = sorted(cg["verbatins"]) == sorted(V); ok = ok and R["cunhagens_listam_todas_as_inscricoes_embutidas"]
# as citacoes do operador nos snippets: o fragmento PRECISA estar no snippet e verbatim nos textos do operador (os fragmentos nao carregam aspas retas: o LaTeX as escreve de outro modo)
_base = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
_norm = lambda s: re.sub(r"\s+", " ", s.replace("’", "'")).strip()
_KERN = _norm(re.sub(r"\s--\s+", " ", _base.replace("**", "").replace("`", "").replace("\\n", " ")))   # (v410: sem crases, como o resto do corpus e como o trecho conferido; e com a quebra de linha dos comentarios Lean (o `\n` literal do kernel embutido + o prefixo `-- ` da linha seguinte) desfeita: uma citacao que atravessa a quebra de linha de um comentario do kernel confere. Normalizacao SIMETRICA: as palavras seguem tendo de ser identicas)
_ADENDO = _norm(open(DL.ADENDO_ARQ, encoding="utf-8").read().replace("**", "").replace("`", ""))
_PEDRAS = _norm(" ".join(open(p_["src"], encoding="utf-8").read() for p_ in DL.PEDRAS_V410).replace("**", "").replace("`", ""))   # (v410: a pedra IALD2, uma so'; a docstring dela e' verificada em (i), FORA do corpus; aqui vale como corpus do que o runtime re-cita)
_CASA = _norm(open(os.path.join("C:" + os.sep, "IALD", "CLAUDE.md"), encoding="utf-8", errors="replace").read().replace("**", ""))
_RX_ASPAS = re.compile("«([^»]{3,900})»")
CIT_OP_MINIMAS = [DL.FRASE_ORDEM_V410, DL.FRASE_NOME_IALD2, DL.FRASE_PAR_UNO, DL.FRASE_FUNTOR, DL.FRASE_ALGORITMO_DE_LEITURA, DL.FRASE_SELETOR, DL.FRASE_ISSO_E_O_ATRATOR, DL.FRASE_RATIFICO, DL.FRASE_CONCORDO_TESTE, DL.FRASE_SELO_PROVADO, DL.FRASE_DEI_A_ESCALA, DL.FRASE_RATIFICO_TUDO, DL.FRASE_PERGUNTA_DO_CLAY, DL.FRASE_EXISTE_E_IALD]   # (v410: a ordem, o nome, o par uno, o funtor, o nome do algoritmo (D65), o seletor, o atrator, a ratificacao dos nomes (D74), o teste pre-registrado (D72) e o selo que diz beta_TGL provado (D76); todas de DL.FRASES_V410; tem de estar nos snippets PT: so' o PT cita a fala, o EN traz traducao da gerencia, marcada como nao-citacao)
_SNIP = {"pt": ["artigo_pt_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip"], "en": ["artigo_en_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_en_h0dn_v410.pysnip"]}   # (D86: a secao da AEscala entre a da IALD2 e a do H0DN)
_SNIP_ANTES_DA_D86 = {"pt": ["artigo_pt_v410.pysnip", "artigo_pt_h0dn_v410.pysnip"], "en": ["artigo_en_v410.pysnip", "artigo_en_h0dn_v410.pysnip"]}   # (v410: a secao da IALD2 e, depois dela, a do H0DN x BG1, D72)
for lang in ("pt", "en"):
    sn = "\n".join(open(os.path.join(HERE, f_), encoding="utf-8").read() for f_ in _SNIP[lang])
    _unlatex = lambda s_: s_.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_").replace("\\#", "#")   # (v410: os escapes LaTeX de % & _ # desfeitos dos DOIS lados da comparacao; a fala do terminal tem «100%»)
    sn_flat = _norm(_unlatex(sn.replace("\\texttt{", "").replace("\\emph{", "")))   # (v410: desfaz os escapes LaTeX de % & _ # para comparar com a fala; a fala do terminal tem «100%»)
    R["snippets"][lang] = {}
    _citadas = [_norm(_unlatex(m_.group(1))) for m_ in _RX_ASPAS.finditer(sn)]   # TODA citacao « » do snippet (escapes LaTeX desfeitos)
    if lang == "pt":
        CIT_OP = list(dict.fromkeys(CIT_OP_MINIMAS + _citadas))   # as tres minimas primeiro; depois toda a que o snippet cita (cada uma tem de estar verbatim nas falas do operador)
        R["snippets"][lang]["_n_citacoes_com_aspas_no_snippet"] = len(_citadas); ok = ok and len(_citadas) > 0
        R["snippets"][lang]["_citadas_nao_verbatim_nas_falas_do_operador"] = [c_[:100] for c_ in _citadas if _norm(c_) not in _norm(todos_op)]; ok = ok and not R["snippets"][lang]["_citadas_nao_verbatim_nas_falas_do_operador"]   # (dito: quem corrige o snippet e a gerencia)
    else:
        CIT_OP = []
        R["snippets"][lang]["_sem_citacao_com_aspas_«_»"] = (len(_citadas) == 0); R["snippets"][lang]["_citacoes_com_aspas_no_en"] = [c_[:100] for c_ in _citadas]; ok = ok and len(_citadas) == 0   # o EN so' traz a traducao da gerencia, marcada como nao-citacao
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
arts = [a_ for a_ in ["runtime_v410.py", "runtime_h0dn_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "registros_v410.py", "registros_h0dn_v410.py", "registros_hms13_v410.py", "runtime_hms13_v410.py", "registros_aescala_v410.py", "runtime_aescala_v410.py", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "delta_v410.py", "gerar_candidato_v410.py", "v410_pins.py"] if os.path.exists(os.path.join(HERE, a_))]   # (D72: os arquivos do H0DN; o v410_pins.py so existe depois do candidato)
R["parafrase_da_gerencia_ausente"] = {a: (PARAFRASE not in open(os.path.join(HERE, *a.split("/")), encoding="utf-8").read()) for a in arts}; ok = ok and all(R["parafrase_da_gerencia_ausente"].values())
# (g) VARREDURA DAS ASPAS: toda citacao entre «» e `` '' dos artefatos NOVOS (embutidos e do pos_rito) tem de existir VERBATIM nos bytes dos OPERADOR_*/CUNHAGEM_OPERADOR_* (cunhagens_13out), no Atlas, no kernel embutido da base (que contem os textos da v409 que as erratas citam), no adendo,
# nas fontes das tres pedras, no CLAUDE.md da casa, ou ser rotulo da propria cadeia (titulos, nomes de registros).
ATLAS = os.path.join(DL.WK, "..", "memory", "TGL_ATLAS.md")
_OPB = " || ".join(_norm(open(p, encoding="utf-8", errors="replace").read()) for p in sum([glob.glob(os.path.join(DL.WK, d_, "*OPERADOR_*.txt")) for d_ in ("cunhagens_13out", "cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out")] + [glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*OPERADOR_*.txt"))], []))
_ATL = re.sub(r"\s+", " ", open(ATLAS, encoding="utf-8", errors="replace").read().replace("**", "")) if os.path.exists(ATLAS) else ""
_ROTULOS = {"o teste da unica palavra", "o teste da única palavra", "the test of the only word", "o teste da unica palavra e a pedra token (v397)", "sônico e a afinação das cordas", "sonic and the tuning of the strings",
            "sonico e a afinacao das cordas", "sonico e a afinacao das cordas (v398)", "o testemunho de dois: o selo pela própria tecnologia", "the testimony of two: sealing by its own technology", "o testemunho de dois: o selo pela propria tecnologia",
            "o testemunho de dois: o selo pela propria tecnologia (v399)", "nenhuma face sozinha dá o um", "nenhuma face sozinha da' o um", "nenhuma face sozinha da o um",
            "beta do runtime", "β do runtime", "$\\beta$ do runtime", "$\\beta$ of the runtime", "errata ao lado (v400)",
            "a falsidade (simulacro) da inércia", "a falsidade (simulacro) da inercia", "a falsidade (simulacro) da inercia (v409)", "the falsity (simulacrum) of inertia", "falsidade (simulacro) da inércia", "falsidade (simulacro) da inercia",
            # v410: titulos e rotulos da propria cadeia; as aspas de ENFASE dos textos novos; a TRADUCAO inglesa de citacoes em portugues (que no EN vem seguida do original)
            "a ponte da escala dual, a queda sem geometria e a esperança condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional", "a ponte da escala dual, a queda sem geometria e a esperanca condicional (v410)",
            # v410 (fechamento): titulos e rotulos da secao nova e do md (rotulos da propria cadeia, nao citacao)
            "o fechamento: a passagem para o contínuo e o certificado habitado", "o fechamento: a passagem para o continuo e o certificado habitado", "the closure: the passage to the continuum and the inhabited certificate", "o fechamento (v410)", "o fechamento",
            "the dual-scale bridge, the fall without geometry and the conditional expectation", "inertial", "movimento livre", "free motion", "e = mc^2 composta da escala", "$e=mc^2$ composta da escala", "$e=mc^2$ composed from the scale", "e = mc^2 composed from the scale",
            "does the posted one have a direction?", "the arrow of the fall of the phase, not of space", "o um posto tem direção?", "o um posto tem direcao?", "a seta da queda da fase, não do espaço", "a seta da queda da fase, nao do espaco",
            "when it inscribes itself, it falls; the phase falls", "so it has direction, but not geometric", "the fall i want to translate is not a force either", "the one, when it is posted, performs the", "conditional expectation = name", "τ é a massa de newton", "$\\tau$ é a massa de newton", "$\\tau$ is newton's mass", "tau e' a massa de newton",
            # v410 (pos_rito): rotulos de consulta ao Mapa de Rotas e de erratas nos scripts do pos-rito (registrar_mapa, leitura); a frase em ASCII e' a da v409 citada pela errata E1 (os registros da v409 a escrevem com acentos)
            "ponte da escala dual", "esperanca condicional = nome", "a unica hipotese nomeada e' h_tau [open] (tau e' a massa de newton e a metrica de einstein), que nenhum teorema usa", "inercial = fixo por todos os boosts", "h_tau na forma literal refutada no kernel",
            # v410: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "caminho, verdade e vida (v409)", "caminho, verdade e vida", "way, truth and life",
            # v410: as frases ERRADAS da propria gerencia, citadas nas erratas E15 a E17 para corrigi-las; a lista das frases proibidas da guarda; a transliteracao ASCII do «nucleo II_∞» da bancada (docstring do ChatGPT)
            "nucleo ii_inf", "núcleo ii_inf", "núcleo ii$_\\infty$", "ii$_\\infty$ core", "a luz nao tem autovetor", "a luz nao tem autovetor nenhum", "unico autovetor", "unico vetor fixo", "o espectro pontual e' o um e so' ele", "o espectro pontual e' o um e so' ele; o resto e' continuo", "falta replicar o traco", "igual conditional_on_an_uninhabited_certificate", "certificado/fechamento/gravidade quantica confirmad(o/a)", "k(o) != bot provado",
            # v410: o titulo da secao nova e o seu rotulo no .md (rotulos da propria cadeia, nao citacao)
            "jo 8,32 e a projeção transversal da meia-nat", "jo 8,32 e a projecao transversal da meia-nat", "john 8:32 and the transverse projection of the half-nat", "jo 8,32 e a projeção transversal da meia-nat (v409)", "a transição para a massa", "a transicao para a massa", "o teste da única palavra",
            # v410: os titulos das secoes novas, os nomes das pedras em portugues e os rotulos dos textos (rotulos da propria cadeia, nao citacao)
            "a massa derivada e a identidade definida", "the derived mass and the defined identity", "a massa derivada e a identidade definida (v410)", "massa = tensão pura", "massa = tensao pura", "o que sou", "a identidade", "ponte da massa", "lei do diminuto", "tônica do hamiltoniano", "tonica do hamiltoniano", "disco de euler", "ponto zero do psíon", "ponto zero do psion", "observador = terminal", "## o texto (r2)",
            # v410 (03/11/2026): titulos e rotulos da propria cadeia (a secao nova, a linha do .md) e as TRES frases que a guarda das frases da v410 PROIBE, listadas entre « » no docstring do runtime (a gerencia as lista para a guarda as recusar; nao sao fala de ninguem)
            "o psíon e o canto: a passagem sob compressão e o par", "o psion e o canto: a passagem sob compressao e o par", "the psion and the corner: the passage under compression, and the pair", "o psíon, o canto e o par (v410)", "o psíon, o canto e o par (v410, 03/11/2026)",
            "o par de psions na face de fock esta provado/construido", "o vacuo de fock e o vetor de bell", "a ponte bell-tt e' teorema",
            # v410 (04/11/2026): o titulo da secao nova (PT/EN), a linha do .md e o rotulo da linha da v409 (rotulos da propria cadeia, nao citacao)
            "tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de $\\beta$; o dicionário e o ponto de contradição", "tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of $\\beta$; the dictionary and the point of contradiction",
            "tetelestai é o terminal (v410)", "tetelestai é o terminal (v410, 04/11/2026)", "tetelestai e' o terminal (v410)", "tetelestai é o terminal", "tetelestai e' o terminal", "o psíon, o canto e o par (v409)", "o psion, o canto e o par (v409)",
            # v410: a frase que a guarda das frases da v410 PROIBE, listada entre « » no docstring do runtime (a gerencia a lista para a guarda a recusar; nao e' fala de ninguem)
            "p = np está provado/é teorema/é candidato",
            # v410 (05/11/2026): o titulo da secao nova (PT/EN) e a linha do .md (rotulos da propria cadeia); as frases da GERENCIA que o texto novo cita entre « » como regra (a guarda D56: o qualificador obrigatorio) ou como o que fica aberto (D60, a formulacao do DESENHO_v409)
            "a tradução às classes de turing: o dicionário, a trava, o leitor e a fita sem escala", "the translation to turing's classes: the dictionary, the lock, the reader and the tape without scale", "tradução às classes de turing (v410, 05/11/2026)",
            "relativa ao leitor", "relativa ao leitor (o psíon); a máquina sem leitor fica fora", "relativa ao leitor (o psion); a maquina sem leitor fica fora", "o ω do psíon da luz é o uniforme da instância",
            "a maquina sem leitor", "a máquina sem leitor", "a maquina sem leitor fica fora", "a máquina sem leitor fica fora", "(kernel validity, not creditation)", "a tradução às classes de turing", "tradução às classes de turing (v410)", "a traducao as classes de turing",
            # v410 (09/11/2026): o titulo da secao da IALD2 e o da secao do H0DN x BG1 (PT/EN) e o rotulo da rota Kimi do H0DN (rotulos da propria cadeia, nao citacao; a rota consta como NOT_TESTABLE e nao e' o teste)
            "iald ao quadrado: o leitor do código, a releitura que não acrescenta, o algoritmo iald e o signo", "iald squared: the reader of the code, the rereading that adds nothing, the iald algorithm and the sign", "iald2 (v410, 06/11/2026)",
            "o teste pré-registrado da razão de hubble com a rede de distâncias (h0dn × bg1)", "the pre-registered hubble-ratio test with the distance network (h0dn × bg1)", "h0dn × bg1 pré-registrado (v410, 09/11/2026)",
            "coerência espectro × fotometria", "coerencia espectro x fotometria", "coerência espectro $\\times$ fotometria", "spectrum $\\times$ photometry coherence", "spectrum × photometry coherence", "coherence spectrum x photometry",
            # v410 (09/11/2026): as frases de REGRA da guarda (listadas entre « » nos docstrings do runtime e do delta: o que a guarda PROIBE ou EXIGE; a gerencia as lista para a guarda as recusar ou exigir; nao sao fala de ninguem) e as formas obrigatorias da D72 e da D76
            "a maquina de turing padrao sem o leitor fica fora", "a máquina de turing padrão sem o leitor fica fora", "relativo ao leitor (a maquina com o leitor); a maquina de turing padrao sem o leitor fica fora", "relativo ao leitor (a máquina com o leitor); a máquina de turing padrão sem o leitor fica fora",
            "solução (definitiva) de p vs np", "5 sigma atingido/observado", "a/acima de/mais que 5 sigma", "nenhum dado observado lido", "pré-registrado; nenhum dado observado lido", "pre-registered; no observed data read",
            "provado na natureza (validade, não creditação)", "proved in nature (validity, not creditation)", "provado na natureza (validade, nao creditacao)",
            # v410 (09/11/2026): titulos das secoes do H0DN, linhas do .md e rotulos de linhas de stdout (rotulos da propria cadeia)
            "o teste pré-registrado da razão de hubble", "o teste pre-registrado da razao de hubble (h0dn x bg1)", "o teste pré-registrado da razão de hubble (h0dn × bg1)", "iald2 (v410)", "h0dn × bg1 pré-registrado (v410)", "h0dn x bg1 pre-registrado (v410)", "o registro da iald2 e os registros por spec"}
_rxs = [re.compile("«([^»]{8,700})»"), re.compile(r"``(.{8,700}?)''")]
_limpa = lambda s: _norm(s.replace("\\%", "%").replace("\\_", "_").replace("\\&", "&").replace("\\#", "#").replace("\\n", " ").replace("\\'E", "É").replace('\\"', '"').replace("\\'", "'").replace("\\texttt{", "").replace("\\emph{", "").replace("\\textsf{", "").replace("}", "").replace("**", "").replace("`", "")).replace(" --- ", " — ").strip(" .,;:")
_corpus_um = lambda fr: (fr.lower() in _OPB.lower() or fr.lower() in _ATL.lower() or fr.lower() in _ROTULOS or fr.lower() in _KERN.lower() or fr.lower() in _ADENDO.lower() or fr.lower() in _PEDRAS.lower() or fr.lower() in _CASA.lower())
_corpus_ok = lambda fr: _corpus_um(fr) or (re.search("…|" + re.escape("[...]"), fr) is not None and all(_corpus_um(x_.strip(" .,;:")) for x_ in re.split("…|" + re.escape("[...]"), fr) if len(x_.strip(" .,;:")) >= 8))   # v410: trecho com elisao (… ou [...]) e' conferido por segmento, como em (i)
_APONTADAS_GH = {}   # (v410: as apontadas da v409 eram dos textos daquela versao; nenhuma apontada declarada para a v410 ate' a varredura dizer o contrario -- o que ela reprovar fica em varredura_de_aspas, nunca e' feito passar)
_ROTULOS = {x_.lower() for x_ in _ROTULOS}
R["varredura_de_aspas"] = {}; R["apontadas_a_gerencia_aspas"] = []
for _a in ("runtime_v410.py", "runtime_h0dn_v410.py", "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "registros_v410.py", "registros_h0dn_v410.py", "registros_hms13_v410.py", "runtime_hms13_v410.py", "registros_aescala_v410.py", "runtime_aescala_v410.py", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "delta_v410.py", "gerar_candidato_v410.py", "pos_rito/textos_v410.py", "pos_rito/registrar_mapa_v410.py", "pos_rito/fechar_v410.py", "pos_rito/leitura_v410.py", "pos_rito/superficies_v410.py"):   # (v410: + os arquivos do H0DN, D72)
    _p = os.path.join(HERE, *_a.split("/"))
    if not os.path.exists(_p):
        continue
    _t = open(_p, encoding="utf-8", errors="replace").read(); _nao = []
    for _rx in _rxs:
        for _m in _rx.finditer(_t):
            _fr = _limpa(_m.group(1))
            if len(_fr) < 12 or "_V410_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr:
                continue
            if _corpus_ok(_fr):
                continue
            if _fr.lower() in _APONTADAS_GH:
                R["apontadas_a_gerencia_aspas"].append({"arquivo": _a, "trecho": _fr[:140], "por_que": _APONTADAS_GH[_fr.lower()]}); continue
            _nao.append(_fr[:140])
    R["varredura_de_aspas"][_a] = _nao; ok = ok and not _nao
# (g2) (v410, D72) os DOIS textos de registros com FUNCAO embutidos no candidato (_V410_IALD2_TEXT e _V410_H0DN_TEXT, do bloco v410_pins.py): toda citacao entre « » deles passa pelo mesmo corpus da varredura (g); e o texto do H0DN traz a obrigacao (pré-registrado; nenhum dado observado lido),
# nenhum token de veredito proibido do H0DN (DL.TOKENS_PROIBIDOS_H0DN) e nenhuma aritmetica do agregado publico (DL.H0DN_AGREGADO_NAO_ENTRA). So' com o candidato (em --sem-candidato os textos nao existem).
if not SEM_CAND:
    for _nm in ("_V410_IALD2_TEXT", "_V410_H0DN_TEXT"):
        _tt = json.dumps(ns[_nm], ensure_ascii=False); _nao_t = []
        for _rx in _rxs:
            for _m in _rx.finditer(_tt):
                _fr = _limpa(_m.group(1))
                if len(_fr) < 12 or "_V410_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _corpus_ok(_fr):
                    continue
                _nao_t.append(_fr[:140])
        R["varredura_de_aspas"][_nm] = sorted(set(_nao_t)); ok = ok and not _nao_t
    _th = json.dumps(ns["_V410_H0DN_TEXT"], ensure_ascii=False)
    R["texto_do_h0dn"] = {"traz_a_obrigacao_d72": DL.FRASE_H0DN_OBRIGATORIA_PT in _th, "sem_token_de_veredito_proibido": not any(t_ in _th for t_ in DL.TOKENS_PROIBIDOS_H0DN), "sem_a_aritmetica_do_agregado_publico": not any(a_ in _th for a_ in DL.H0DN_AGREGADO_NAO_ENTRA),
                          "sem_a_cabeca_do_ramo_de_5_sigma_por_extenso": DL.VEREDITOS_H0DN["leitura"] % 6 not in _th and "BETA_TGL_" not in _th}
    ok = ok and all(R["texto_do_h0dn"].values())
# (h) VARREDURA DO CANDIDATO INTEIRO: toda citacao entre «» e `` '' das linhas que o candidato traz e a BASE v409 selada NAO traz tem de existir VERBATIM nos OPERADOR_* ou no Atlas (ou ser rotulo da cadeia / texto do kernel / adendo / fonte das pedras / casa); citacao que a base ja' tem nao e' deste delta.
if not SEM_CAND:   # (h) so' com o candidato; em --sem-candidato este passo NAO roda e o relatorio o diz
    _cand = open(os.path.join(HERE, DL.CANDIDATO), encoding="utf-8").read()
    _bls = set(_base.splitlines()); _novas = [_l for _l in _cand.splitlines() if _l not in _bls]; _nao_c = []
    for _l in _novas:
        for _rx in _rxs:
            for _m in _rx.finditer(_l):
                _fr = _limpa(_m.group(1))
                if len(_fr) < 12 or "_V410_" in _fr or "_V399_" in _fr or "+" in _fr or "%s" in _fr or _m.group(1) in _base:
                    continue
                if _corpus_ok(_fr):
                    continue
                if _fr.lower() in _APONTADAS_GH:
                    R["apontadas_a_gerencia_aspas"].append({"arquivo": "candidato", "trecho": _fr[:140], "por_que": _APONTADAS_GH[_fr.lower()]}); continue
                _nao_c.append(_fr[:140])
    R["varredura_de_aspas"]["candidato (%d linhas novas sobre a base)" % len(_novas)] = sorted(set(_nao_c)); ok = ok and not _nao_c
else:
    R["varredura_de_aspas"]["candidato"] = "NAO RODADO (--sem-candidato): o passo (h) precisa do candidato"
# (i) VARREDURA DAS PEDRAS (errata R2 da gerencia, 01/11/2026; achado 12 da revisao de terceiro; v410: a pedra IALD2, uma so'): toda citacao entre « » da docstring da pedra tem de existir VERBATIM nas falas do operador, no Atlas, no kernel embutido da base, no adendo e no CLAUDE.md da casa. As pedras NAO contam como corpus aqui. Trecho com elisao (… ou [...]) e' conferido por segmento. O que nao e' fala e e' rotulo da propria pedra esta em _ROTULOS_PEDRAS; o que esta entre aspas, nao e' verbatim e nao e' rotulo esta em _APONTADAS_PEDRAS: dito a gerencia no relatorio, porque o agente nao corrige pedra. Qualquer outra coisa reprova.
_BANC = [os.path.join(DL.SANDBOX, *r_.split("/")) for r_ in DL.BUNDLE_DA_BANCADA]   # (v410: DL.BUNDLE_DA_BANCADA == [] -- a pedra IALD2 e' prova da gerencia c1 com o nome do operador; nenhum modulo da bancada do ChatGPT entra neste bundle)
_XP = [p_ for p_ in _BANC if os.path.exists(p_)]   # (a pedra IALD2 e os recibos da gerencia NAO sao corpus: texto da gerencia nao abona citacao)
_LX = lambda t_: t_.replace(chr(92) + "(" + chr(92) + "kappa" + chr(92) + ")", "κ").replace(chr(92) + "(" + chr(92) + "tau^" + chr(92) + "star" + chr(92) + ")", "τ★")   # a notacao LaTeX do relatorio do Kimi
_CP = " || ".join([_OPB, _ATL, _KERN, _ADENDO, _CASA] + [_LX(_norm(open(p_, encoding="utf-8", errors="replace").read().replace("**", "").replace("`", ""))) for p_ in _XP]).lower()
_sem_acento = lambda s_: "".join(c_ for c_ in unicodedata.normalize("NFD", s_) if unicodedata.category(c_) != "Mn")
_CPU = _sem_acento(_CP)   # v410: a candidata escreve «nucleo II_∞» (transliteracao sem acento) onde a bancada escreve «núcleo II_∞»; o trecho vale se bate com o corpus SEM acento, e o fato fica dito em varredura_das_pedras.so_sem_acento
_noc_a = lambda x_: re.search(r"(?<![\w])" + re.escape(x_.lower()) + r"(?![\w])", _CP) is not None   # com fronteira de palavra: trecho curto nao passa por acaso no meio de outra palavra
_noc_u = lambda x_: re.search(r"(?<![\w])" + re.escape(_sem_acento(x_.lower())) + r"(?![\w])", _CPU) is not None
_SO_SEM_ACENTO = []


def _noc(x_):
    if _noc_a(x_):
        return True
    if _noc_u(x_):
        _SO_SEM_ACENTO.append(x_[:100]); return True
    return False

_ROTULOS_PEDRAS = {}   # (v410: SO' o que a propria pedra diz ser rotulo/nome dela, nunca para fazer passar citacao; as entradas da v409 eram das nove pedras daquela versao; a lista da v410 comeca vazia)
_APONTADAS_PEDRAS = {}   # (v410, 09/11/2026: comeca VAZIA -- a pedra IALD2 e' nova e as apontadas da v409 eram das pedras TraducaoTuring e ParNaFaceDeFock; so' entra aqui o que a varredura (i) REPROVAR de fato, com a razao conferida por grep, e DITO A GERENCIA no relatorio: o agente nao corrige pedra; a lista da v409 fica como registro no conferir_citacoes_v409.py)
_PQ_AE_PARAFRASE = "pedra AEscala (autor claude-autor-aescala; nomes ratificados pelo operador, D87): citacao entre « » que NAO e' verbatim nas falas de 09/11 -- e' PARAFRASE ou ABREVIACAO da fala indicada (reticencias, ordem trocada, artigo trocado ou o glifo ½ no lugar de 1/2); conferido por grep nas oito falas; o agente nao corrige pedra: DITO A GERENCIA"
_PQ_AE_ROTULO = "pedra AEscala: ROTULO, titulo de tabela ou formula da propria pedra posto entre « », nao citacao de fala; conferido por grep nas oito falas; o agente nao corrige pedra: DITO A GERENCIA"
_APONTADAS_PEDRAS.update({   # (v410, parte 2, 09/11/2026: as 20 citacoes « » da AEscala que a varredura REPROVOU de fato; nenhuma e' verbatim; a fala de origem dita em cada uma)
    "fala → termos": _PQ_AE_ROTULO + " (o titulo da tabela)", "nota = J": _PQ_AE_ROTULO, "Nome = par conjugado, face caída = a que não conjuga": _PQ_AE_ROTULO,
    "a insígnia … não esgota o signo … sustenta": _PQ_AE_PARAFRASE + " [fala 1: «embora não seja capaz de esgotar o signo, a insígnia é suficiente para sustenta-lo»]",
    "a nota é a conjugação modular": _PQ_AE_PARAFRASE + " [fala 1: «sustenta a nota que é a conjugação modular»]",
    "o nome pesa 1 … duas faces que pesam ½ cada": _PQ_AE_PARAFRASE + " [fala 2, com 1/2]",
    "o inalcançável … não conjuga, nunca chega a pesar 1, não acopla": _PQ_AE_PARAFRASE + " [fala 2: «como não conjuga nunca chega a pesar 1 e por isso não acopla»]",
    "tres faces de ½ … 1/3 caiu": _PQ_AE_PARAFRASE + " [fala 2, com 1/2]", "fundamental para P=nP": _PQ_AE_PARAFRASE + " [fala 3: «fundamenal para a compreensão completa de P=nP», com a grafia dele]",
    "qual algoritmo lê a face sem leitura … existe, é IALD": _PQ_AE_PARAFRASE + " [fala 6]", "é a justiça, é o ideal, mas é intocável": _PQ_AE_PARAFRASE + " [fala 6: «ela é a justiça, ela é o ideal, mas é intocável»]",
    "ela é a justiça, é o ideal, mas é intocável": _PQ_AE_PARAFRASE + " [fala 6: «ela é a justiça, ela é o ideal, mas é intocável»]", "um de três caiu": _PQ_AE_PARAFRASE + " [fala 2: «(1/3 caiu)»]",
    "não esgota o signo, mas sustenta a travessia": _PQ_AE_PARAFRASE + " [fala 1]", "o infinito inscrito no finito como Nome": _PQ_AE_PARAFRASE + " [fala 1: «o infinito se inscreve no finito como NOME»]",
    "três faces de ½, duas conjugadas, uma caída (1/3 caiu)": _PQ_AE_PARAFRASE + " [fala 2, com 1/2]", "as duas faces que pesam 1/2 cada": _PQ_AE_PARAFRASE + " [fala 2: «das duas faces que pesam 1/2 cada»]",
    "o nome pesa 1 porque é a conjugação das duas faces que pesam ½ cada": _PQ_AE_PARAFRASE + " [fala 2, com 1/2: a unica diferenca e' o glifo]", "o Nome acima do Nome": _PQ_AE_PARAFRASE + " [fala 4: «o que eu chamo de Nome acima do Nome»]",
    "O negativo como tela de fundo da experiência": _PQ_AE_PARAFRASE + " [fala 6: «eu uso ela como tela de fundo, como negativo, para a minha própria experiência»]"})
_APONTADAS_PEDRAS = {k_.lower(): v_ for k_, v_ in _APONTADAS_PEDRAS.items()}   # chave = o trecho inteiro (minuscula) ou, se tiver >= 20 caracteres, um PREFIXO dele: o trecho longo nao precisa ser redigitado
_apontada_por_prefixo = lambda fr_: next((v_ for k_, v_ in _APONTADAS_PEDRAS.items() if fr_.lower() == k_ or (len(k_) >= 20 and fr_.lower().startswith(k_))), None)
R["varredura_das_pedras"] = {"citacoes_conferidas": 0, "rotulos": [], "apontadas_a_gerencia": [], "reprovadas": [], "corpus_bancada_n": len(_XP), "so_sem_acento": _SO_SEM_ACENTO}
R["varredura_das_pedras"]["n_pedras_varridas"] = len(DL.PEDRAS_V410); ok = ok and len(DL.PEDRAS_V410) == DL.N_BUNDLE == CM["kernel"]["modulos_novos"]
for _s in DL.PEDRAS_V410:
    _t = _norm(re.sub(r"\n>\s*", " ", open(_s["src"], encoding="utf-8").read()))
    for _m in re.finditer("«([^»]{8,900})»", _t):
        _fr = _norm(_m.group(1).replace("`", "").replace("**", "")).strip(" .,;:")
        _sg = [x_.strip(" .,;:") for x_ in re.split(r"…|\[\.\.\.\]", _fr) if len(x_.strip(" .,;:")) >= 8]
        if all(_noc(x_) for x_ in _sg):
            R["varredura_das_pedras"]["citacoes_conferidas"] += 1
        elif _fr.lower() in _ROTULOS_PEDRAS:
            R["varredura_das_pedras"]["rotulos"].append({"pedra": _s["name"], "trecho": _fr[:120], "por_que": _ROTULOS_PEDRAS[_fr.lower()]})
        elif _apontada_por_prefixo(_fr):
            R["varredura_das_pedras"]["apontadas_a_gerencia"].append({"pedra": _s["name"], "trecho": _fr[:160], "por_que": _apontada_por_prefixo(_fr)})
        else:
            R["varredura_das_pedras"]["reprovadas"].append({"pedra": _s["name"], "trecho": _fr[:160]})
ok = ok and not R["varredura_das_pedras"]["reprovadas"] and R["varredura_das_pedras"]["citacoes_conferidas"] > 0
# (i-bis) [R1, 09/11/2026: D91 e MEDIO 2 da revisao de terceiro] VARREDURA ESTRITA DAS PEDRAS, fail-closed: toda passagem entre aspas angulares em pedra\\*.lean tem de ser fala VERBATIM do operador (a casa reserva as angulares a fala verbatim);
# a normalizacao e' a do requote da gerencia (work\\pedras_candidatas_09nov\\R2_aspas\\requote_aescala_v410.py): espacos colapsados, minusculas, reticencias toleradas por pedaco; rotulo, parafrase e docstring citada NAO passam.
import glob as _glob_r1
_CUN_R1 = os.path.normpath(os.path.join(HERE, "..", "..", "cunhagens_13out"))
_arqs_r1 = sorted(_glob_r1.glob(os.path.join(_CUN_R1, "OPERADOR_*.txt"))) + sorted(_glob_r1.glob(os.path.join(HERE, "insumos", "cunhagens", "*.txt")))
_norm_r1 = lambda s_: re.sub(r"\s+", " ", s_).strip().lower()
_NC_R1 = _norm_r1("\n".join(open(p_, encoding="utf-8", errors="replace").read() for p_ in _arqs_r1))


def _verbatim_r1(q_):
    n_ = _norm_r1(q_).rstrip(".,;: ")
    partes_ = [x_.strip(" .,;:") for x_ in re.split(r"\u2026|\[\.\.\.\]|\.\.\.", n_) if x_.strip(" .,;:")]
    return bool(partes_) and all(pt_ in _NC_R1 for pt_ in partes_)


_RX_R1 = re.compile(chr(0xAB) + "([^" + chr(0xBB) + "]{1,400})" + chr(0xBB))
_ped_r1 = sorted(_glob_r1.glob(os.path.join(HERE, "pedra", "*.lean")))
_rep_r1 = []; _n_r1 = 0
for _pp in _ped_r1:
    for _q in _RX_R1.findall(open(_pp, encoding="utf-8").read()):
        _n_r1 += 1
        if not _verbatim_r1(_q):
            _rep_r1.append({"pedra": os.path.basename(_pp), "trecho": re.sub(r"\s+", " ", _q)[:160]})
_ctl_r1 = {"trecho_que_o_operador_nunca_disse_reprova": not _verbatim_r1("isto o operador nunca disse nesta casa xyzzy 4711"), "fala_do_operador_passa": _verbatim_r1(DL.FRASE_RATIFICO_TUDO) and _verbatim_r1(DL.FRASE_DEI_A_ESCALA),
           "reticencias_por_pedaco": _verbatim_r1(DL.FRASE_DEI_A_ESCALA + " ... " + DL.FRASE_RATIFICO_TUDO) and not _verbatim_r1(DL.FRASE_DEI_A_ESCALA + " ... xyzzy 4711"), "corpus_nao_vazio": len(_arqs_r1) >= 23 and len(_NC_R1) > 1000,
           "as_pedras_do_bundle_foram_varridas": sorted(os.path.basename(p_) for p_ in _ped_r1) == sorted(os.path.basename(r_) for r_ in DL.BUNDLE_RELS)}
R["varredura_estrita_das_pedras_r1"] = {"n_pedras": len(_ped_r1), "n_passagens": _n_r1, "n_verbatim": _n_r1 - len(_rep_r1), "reprovadas": _rep_r1, "controle_negativo": _ctl_r1, "corpus_arquivos": len(_arqs_r1),
                                        "regra": "toda passagem entre aspas angulares nas pedras e' fala verbatim do operador (espacos colapsados, minusculas, reticencias por pedaco); o resto usa aspas tipograficas"}
ok = ok and not _rep_r1 and _n_r1 > 0 and all(_ctl_r1.values())
_vistos = set(); _un = []
for x_ in R["apontadas_a_gerencia_aspas"]:   # sem repeticao (a mesma citacao aparece no delta, nos registros e no candidato)
    k_ = (x_["arquivo"], x_["trecho"])
    if k_ not in _vistos:
        _vistos.add(k_); _un.append(x_)
R["apontadas_a_gerencia_aspas"] = _un
R["resumo_dito_a_gerencia"] = {"aspas_apontadas": len(R["apontadas_a_gerencia_aspas"]), "pedras_apontadas": len(R["varredura_das_pedras"]["apontadas_a_gerencia"]), "pedras_rotulos": len(R["varredura_das_pedras"]["rotulos"]), "nota": "apontada NAO e' reprovada: a citacao entre « » nao e' verbatim nas falas do operador nem na base; a gerencia decide (o agente nao corrige pedra nem texto da gerencia); nenhuma e' atribuida ao operador por este script"}
R["todas_conferem"] = ok
if SEM_CAND:   # ENSAIO: nada e' gravado; imprime o que reprovou, para a gerencia ver antes do candidato
    def _ruim(k_, v_):
        if isinstance(v_, dict):
            return not all(v_.values())
        if isinstance(v_, list):
            return bool(v_)
        if k_ == "_n_citacoes_com_aspas_no_snippet":
            return v_ == 0
        return v_ is False
    _f = {"falas": {k_: v_ for k_, v_ in R["verbatins"].items() if not (v_["embutida_igual_ao_arquivo"] and v_["fonte_original_igual"] is True and v_["trecho_confere_com_o_arquivo"] in (None, True))},
          "snippets": {l_: {k_: v_ for k_, v_ in d_.items() if _ruim(k_, v_)} for l_, d_ in R["snippets"].items()},
          "varredura_de_aspas": {k_: v_ for k_, v_ in R["varredura_de_aspas"].items() if v_ and not isinstance(v_, str)},
          "parafrase_da_gerencia_ausente": R.get("parafrase_da_gerencia_ausente"), "frase_do_quadro_verbatim": R.get("frase_do_quadro_verbatim_na_fala_de_23out"),
          "pedras_reprovadas": R["varredura_das_pedras"]["reprovadas"], "pedras_apontadas": R["varredura_das_pedras"]["apontadas_a_gerencia"], "pedras_n_conferidas": R["varredura_das_pedras"]["citacoes_conferidas"]}
    print("ENSAIO --sem-candidato (nada gravado):", json.dumps(_f, ensure_ascii=False, indent=1)); print("TODAS CONFEREM (sem candidato)" if ok else "FALHOU (sem candidato)"); sys.exit(0 if ok else 1)
json.dump(R, open(os.path.join(HERE, "conferir_citacoes_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k == "todas_conferem" else len(v) if isinstance(v, (dict, list)) else v) for k, v in R.items()}, ensure_ascii=False)); print("TODAS CONFEREM" if ok else "FALHOU"); sys.exit(0 if ok else 1)
