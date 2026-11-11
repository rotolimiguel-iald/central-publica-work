# -*- coding: utf-8 -*-
# [AUTORAL v410, 09/11/2026, claude-construtor-v410, a servico da gerencia c1] os dados do TERCEIRO registro com FUNCAO da v410 (D80): h0dn_fontes_hms13_v410 -- o recibo documental HMS/13 do Kimi, ADITIVO e POSTERIOR ao FREEZE_R2.
"""registros_hms13_v410.py -- o CONTRATO, o TEXTO e os INSUMOS EMBUTIDOS (base64, pinados por sha256 LIDO) do registro h0dn_fontes_hms13_v410 (gerar_candidato_v410.py os emite com runtime_hms13_v410.py).
D80 (ordem do operador, 09/11/2026, ratificada por sha256): a incorporacao documental HMS/13 entra na v410 como registro NOVO, aditivo e posterior ao FREEZE_R2; os limites da ORDEM do Kimi (ORDEM_CLAUDE_UMPY_HMS_13.md) valem como contrato.
O BUILD (este modulo, chamado pelo gerador) LE a pasta do pacote do Kimi (revisao_independente\\): confere, imediatamente antes do build, os sha256 do HANDOFF e da ORDEM contra os arquivos (fail-closed), embute SOMENTE os quatro artefatos documentais
(mapa de fontes e covariancia, manifesto das fontes primarias, validacao, levantamento legivel) por bytes e sha256, e aplica a GUARDA NUMERICA: numero so' em chave de bytes, contagem, linha, caracteres de texto ou componente de erro (sigma, error);
nenhuma lista numerica; se um campo proibido aparecer, grava BLOQUEIO_HMS13_v410.json e PARA. O RITO nao abre nada de kimi\\: o registro confere so' o conteudo embutido. A ratificacao do operador entra pela frase final da fala, por sha256 do arquivo inteiro
(a cunhagem que a antecede NAO entra: fica para a v411). Nada digitado: IDs, fontes, estados e numeros vem dos artefatos."""
import base64, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402

sha256 = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos")
# as origens (copiadas por copiar_insumos_v410.py como copias duraveis insumos\\hms13_*; a excecao declarada ao veto da pasta do Kimi: SO' estas seis, por sha256) e as fontes pinadas para o motor v392
ORIGENS_HMS13 = [("hms13_" + nome_.replace("/", "_"), os.path.join(DL.HMS13_DIR, *rel_.split("/"))) for nome_, rel_ in DL.HMS13_EMBUTIDOS] + [("hms13_HANDOFF_CLAUDE_UMPY_HMS_13.json", DL.HMS13_HANDOFF_ARQ), ("hms13_ORDEM_CLAUDE_UMPY_HMS_13.md", DL.HMS13_ORDEM_ARQ)]
FONTES_HMS13_RG = [{"chave": "hms13_" + nome_.replace("/", "_").rsplit(".", 1)[0].lower(), "arquivo": os.path.join(INS, "hms13_" + nome_.replace("/", "_")), "papel": papel_} for nome_, papel_ in (
    ("MAPA_FONTES_E_COVARIANCIA_13.json", "o mapa de fontes e covariancia dos 13 calibradores (Kimi, 09/11): erro diagonal da SN, do hospedeiro, da ancora, do MAS e do grupo por linha dos arquivos upstream; compartilhamentos; admissao e proibicoes [REAL: sha256; DECLARADO pelo Kimi no conteudo]"),
    ("MANIFEST_FONTES_PRIMARIAS.json", "o manifesto das 18 fontes primarias arquivadas (titulo, URL, sha256 do arquivo e do texto extraido, cobertura por objeto) [REAL: sha256; DECLARADO pelo Kimi no conteudo]"),
    ("VALIDACAO_FONTES_13.json", "a validacao do pacote pelo validador do Kimi: SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN, 13/13 objetos, 18/18 arquivos, bandeiras de fechamento falsas [REAL: sha256; DECLARADO pelo Kimi]"),
    ("LEVANTAMENTO_FONTES_PRIMARIAS_13.md", "o levantamento legivel das fontes primarias (tabela por objeto, estruturas compartilhadas, fontes, veredito) -- para o artigo [REAL: sha256; DECLARADO pelo Kimi]"),
    ("HANDOFF_CLAUDE_UMPY_HMS_13.json", "o handoff do Kimi a gerencia (09/11): estado, base observada, os dez campos, os pinos dos artefatos [REAL: sha256]"),
    ("ORDEM_CLAUDE_UMPY_HMS_13.md", "a ORDEM do Kimi a gerencia (09/11): o que foi feito, a incorporacao permitida, a aceitacao, o que permanece aberto, a pergunta nas quatro linguas [DECLARADO pelo Kimi; ratificada pelo operador por sha256, D80]"))]
_PERM = tuple(DL.HMS13_NUMEROS_PERMITIDOS)


def numeros(obj, caminho=""):
    """percorre o JSON e devolve (permitidos, proibidos, listas_numericas): todo numero (fora bool) e' permitido so' se a chave traz um dos radicais permitidos; toda lista numerica e' proibida (D80 §5)."""
    perm, proib, arrays = [], [], []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p, q, a = numeros(v, caminho + "/" + str(k)); perm += p; proib += q; arrays += a
    elif isinstance(obj, list):
        if obj and all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in obj):
            arrays.append((caminho, len(obj), len(obj) in DL.HMS13_COMPRIMENTOS_PROIBIDOS))
        for i, v in enumerate(obj):
            p, q, a = numeros(v, caminho + "[%d]" % i); perm += p; proib += q; arrays += a
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        chave = caminho.rsplit("/", 1)[-1].lower()
        (perm if any(r_ in chave for r_ in _PERM) else proib).append((caminho, obj))
    return perm, proib, arrays


def _ler(p):
    return open(p, "rb").read()


def pinos_hms13():
    """LE, imediatamente antes do build, o HANDOFF e a ORDEM e confere os sha256 que eles listam contra os arquivos (fail-closed); devolve os seis pinos (os quatro embutidos + ORDEM + HANDOFF) e o HANDOFF decodificado."""
    bh = _ler(DL.HMS13_HANDOFF_ARQ); bo = _ler(DL.HMS13_ORDEM_ARQ); hj = json.loads(bh.decode("utf-8")); ordem_txt = bo.decode("utf-8")
    assert sha256(bo)[:16] == DL.HMS13_ORDEM_SHA16_DO_DESENHO, ("a ORDEM do Kimi em disco nao tem o sha16 que o DESENHO (D79) deu", sha256(bo)[:16], DL.HMS13_ORDEM_SHA16_DO_DESENHO)
    assert hj["order"]["sha256"] == sha256(bo) and hj["order"]["bytes"] == len(bo), "o HANDOFF pina outra ORDEM"
    assert hj["status"].startswith("HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY") and hj["opening_allowed"] is False and hj["full_HMS_admitted"] is False and hj["physical_covariance_closed"] is False and hj["observed_opening_performed"] is False, hj.get("status")
    pins_ordem = {m_.group(1): (m_.group(2), int(m_.group(3))) for m_ in re.finditer(r"- `([^`]+)`: `[^`]+`\s*\n\s*SHA-256 `([0-9a-f]{64})`; bytes `(\d+)`", ordem_txt)}
    assert len(pins_ordem) >= 5, ("a ORDEM nao traz os pinos na forma esperada", sorted(pins_ordem))
    pinos = {}
    for nome, rel in DL.HMS13_EMBUTIDOS:
        p = os.path.join(DL.HMS13_DIR, *rel.split("/")); b = _ler(p); s = sha256(b)
        ha = hj["artifacts"][nome]; assert ha["sha256"] == s and ha["bytes"] == len(b), ("DIVERGENCIA (fail-closed): o artefato em disco nao bate com o HANDOFF", nome, s, ha["sha256"])
        assert os.path.normcase(os.path.abspath(ha["path"])) == os.path.normcase(os.path.abspath(p)), ("o HANDOFF aponta outro caminho", nome)
        so, bo_ = pins_ordem[nome]; assert so == s and bo_ == len(b), ("DIVERGENCIA (fail-closed): o artefato em disco nao bate com a ORDEM", nome)
        pinos[nome] = {"sha256": s, "bytes": len(b), "rel": rel, "path": p}
    pinos["HANDOFF_CLAUDE_UMPY_HMS_13.json"] = {"sha256": sha256(bh), "bytes": len(bh), "rel": "HANDOFF_CLAUDE_UMPY_HMS_13.json", "path": DL.HMS13_HANDOFF_ARQ}
    pinos["ORDEM_CLAUDE_UMPY_HMS_13.md"] = {"sha256": sha256(bo), "bytes": len(bo), "rel": "ORDEM_CLAUDE_UMPY_HMS_13.md", "path": DL.HMS13_ORDEM_ARQ}
    return pinos, hj, ordem_txt


def insumos_embutidos_hms13():
    """{nome: {'b64', 'sha256', 'bytes', 'rel'}} -- os bytes LIDOS dos QUATRO artefatos documentais, em base64 (o um.py os decodifica e confere a cada rito); nada mais da pasta."""
    out = {}
    for nome, rel in DL.HMS13_EMBUTIDOS:
        b = _ler(os.path.join(DL.HMS13_DIR, *rel.split("/")))
        out[nome] = {"b64": base64.b64encode(b).decode("ascii"), "sha256": sha256(b), "bytes": len(b), "rel": rel}
    return out


def guarda_numerica(ins):
    """a guarda fail-closed do BUILD (D80 §5): nos tres JSON embutidos, nenhum numero fora das chaves permitidas e nenhuma lista numerica; no levantamento, nenhuma linha com um vetor de numeros. Devolve o relatorio; PARA (BLOQUEIO_HMS13_v410.json) se houver campo proibido."""
    rel = {"permitidos": 0, "proibidos": [], "listas_numericas": [], "chaves_permitidas_vistas": set()}
    for nome in ("MAPA_FONTES_E_COVARIANCIA_13.json", "MANIFEST_FONTES_PRIMARIAS.json", "VALIDACAO_FONTES_13.json"):
        obj = json.loads(base64.b64decode(ins[nome]["b64"]).decode("utf-8"))
        perm, proib, arrays = numeros(obj)
        rel["permitidos"] += len(perm); rel["proibidos"] += [(nome,) + x for x in proib]; rel["listas_numericas"] += [(nome,) + x for x in arrays]
        rel["chaves_permitidas_vistas"] |= {c.rsplit("/", 1)[-1] for c, _ in perm}
    lev = base64.b64decode(ins["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"]["b64"]).decode("utf-8")
    vetores_md = [l_[:80] for l_ in lev.splitlines() if len(re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.])", l_)) >= 20]
    rel["linhas_do_levantamento_com_vetor_numerico"] = vetores_md
    rel["chaves_permitidas_vistas"] = sorted(rel["chaves_permitidas_vistas"])
    rel["ok"] = not rel["proibidos"] and not rel["listas_numericas"] and not vetores_md
    if not rel["ok"]:
        pb = os.path.join(HERE, "BLOQUEIO_HMS13_v410.json")
        open(pb + ".tmp", "w", encoding="utf-8").write(json.dumps({"BLOQUEIO": "D80 §5: um artefato documental embutido traz numero proibido (valor do vetor observado, modulo de distancia, centro fotometrico, lista numerica): o build PARA e avisa a gerencia", "relatorio": rel}, ensure_ascii=False, indent=1, default=str)); os.replace(pb + ".tmp", pb)
        raise SystemExit("BLOQUEIO_HMS13_v410.json gravado: campo numerico proibido nos artefatos HMS/13 -- avisar a gerencia")
    return rel


def ratificacao_hms13():
    """a fala do operador LIDA por script: sha256 do arquivo inteiro == o do DESENHO (D80); a frase final e' o trecho citavel (modo sufixo: do trecho ate' o fim); o resto nao entra."""
    b = _ler(DL.HMS13_RATIFICACAO_ARQ); t = b.decode("utf-8")
    assert sha256(b) == DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO, ("a fala do operador em disco nao tem o sha256 que o DESENHO (D80) deu", sha256(b), DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO)
    i = t.find(DL.HMS13_TRECHO_RATIFICACAO); assert i >= 0 and t.count(DL.HMS13_TRECHO_RATIFICACAO) == 1, "o trecho da ratificacao nao esta' uma vez na fala"
    cauda = t[i:]   # (a frase final e o caminho do HANDOFF, como ele escreveu)
    assert "HANDOFF_CLAUDE_UMPY_HMS_13.json" in cauda and "vibrato" not in cauda.lower(), "a cauda da fala nao e' so' a ratificacao"
    return {"origem": "fala do operador de 09/11/2026 (~15:45), em work/cunhagens_13out, por sha256 do arquivo inteiro (o nome do arquivo resume a cunhagem que fica fora deste registro e nao se cita aqui)", "sha256": sha256(b), "bytes": len(b), "trecho": DL.HMS13_TRECHO_RATIFICACAO, "sha256_do_trecho": sha256(DL.HMS13_TRECHO_RATIFICACAO.encode("utf-8")),
            "modo": "sufixo: so' a frase final e o caminho do HANDOFF; a cunhagem que a antecede nao entra por este registro (D80; D82: e' a pedra nova, parte 2)",
            "aponta_o_handoff": "HANDOFF_CLAUDE_UMPY_HMS_13.json" in cauda, "quando": "09/11/2026", "autor": "operador"}


def contrato_hms13(core0, selo0, contrato_h0dn):
    """O contrato do registro h0dn_fontes_hms13_v410, DERIVADO dos artefatos LIDOS (pinos do HANDOFF e da ORDEM conferidos agora), do core/selo da v409 selada (o gate a repetir) e do contrato do H0DN (o FREEZE_R2 a que este registro e' posterior); nada digitado."""
    pinos, hj, ordem_txt = pinos_hms13(); ins = insumos_embutidos_hms13(); gn = guarda_numerica(ins); rat = ratificacao_hms13()
    mapa = json.loads(base64.b64decode(ins["MAPA_FONTES_E_COVARIANCIA_13.json"]["b64"]).decode("utf-8")); manif = json.loads(base64.b64decode(ins["MANIFEST_FONTES_PRIMARIAS.json"]["b64"]).decode("utf-8")); valid = json.loads(base64.b64decode(ins["VALIDACAO_FONTES_13.json"]["b64"]).decode("utf-8"))
    lev = base64.b64decode(ins["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"]["b64"]).decode("utf-8")
    ids = [o_["CID"] for o_ in mapa["objects"]]; fontes = [s_["key"] for s_ in manif["sources"]]
    assert len(ids) == 13 == len(set(ids)) and len(fontes) == 18 == len(set(fontes)) == manif["source_count"], (len(ids), len(fontes))
    assert set(valid["object_checks"]) == set(ids) and set(valid["archive_checks"]) == set(fontes) and set(manif["coverage"]) == set(ids) and all(valid["checks"].values()) and valid["status"] == "SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN"
    assert all(set(o_["primary_sources"]) <= set(manif["coverage"][o_["CID"]]) <= set(fontes) for o_ in mapa["objects"]), "uma fonte do mapa nao esta' na cobertura do manifesto, ou a cobertura cita fonte fora do manifesto"
    cob_extra = {o_["CID"]: sorted(set(manif["coverage"][o_["CID"]]) - set(o_["primary_sources"])) for o_ in mapa["objects"] if set(manif["coverage"][o_["CID"]]) - set(o_["primary_sources"])}   # MEDIDO no build: onde o manifesto cobre um objeto com fonte que o mapa nao lista (o rito confere a mesma assimetria; nao se esconde)
    statuses = sorted({str(s_["archive_status"]) for s_ in manif["sources"]})
    assert valid["hashes"]["MAPA_FONTES_E_COVARIANCIA_13.json"] == ins["MAPA_FONTES_E_COVARIANCIA_13.json"]["sha256"] and valid["hashes"]["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"] == ins["LEVANTAMENTO_FONTES_PRIMARIAS_13.md"]["sha256"] and valid["hashes"]["fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json"] == ins["MANIFEST_FONTES_PRIMARIAS.json"]["sha256"], "a validacao pina outros artefatos"
    campos = dict(DL.HMS13_CAMPOS)
    assert hj["primary_sources"] == campos["fontes_primarias"] and hj["calibrators"] == campos["calibradores"] and all(hj[k_] == campos[k_] for k_ in ("partial_components_only", "full_13x13_covariance_available", "within_SN_full_decomposition_available", "physical_covariance_closed", "independent_physical_review_complete", "full_HMS_admitted", "opening_allowed")), "os campos do HANDOFF divergem dos da ORDEM §3.7"
    adm = mapa["admission"]
    assert adm["opening_allowed"] is False and adm["physical_covariance_closed"] is False and adm["full_13x13_covariance_available"] is False and adm["within_SN_full_decomposition_available"] is False and adm["independent_physical_review_complete"] is False and adm["partial_factor_map_available"] is True and mapa["full_HMS_admitted"] is False and mapa["observed_vector_read"] is False and mapa["observed_statistics_computed"] is False
    gate0 = ((core0.get("qg_closure") or {}).get("gate") or {}).get("verdict"); assert isinstance(gate0, str) and gate0 == selo0.get("qg_closure_verdict") == contrato_h0dn["baseline"]["gate_verdict"]
    freeze_sha = contrato_h0dn["insumos"]["FREEZE_R2.json"]["sha256"]
    freeze_arqs = sorted(set(os.path.basename(v_["rel"]) for v_ in contrato_h0dn["insumos"].values()) | set(os.path.basename(r_) for r_ in contrato_h0dn["pinos_freeze_r2_so_no_disco"]))
    assert not (set(k_ for k_ in pinos) & set(freeze_arqs)), "um artefato HMS/13 repete um pino do FREEZE_R2: o registro e' ADITIVO, nao reescreve o congelamento"
    perguntas = {"tgl": "quais produtos internos dos ajustes permitem separar a variância independente da compartilhada sem repetir host, MAS, âncora ou intrínseco?",
                 "teologica": "que testemunha externa certifica que a decomposição está completa, e não apenas bem nomeada? [ONTO]",
                 "linguistica": "como preservar no registro a diferença entre “18 fontes cobertas”, “fatores parciais derivados” e “covariância física fechada”?",
                 "juridica": "qual prova adicional e qual revisão independente autorizam um futuro teste de suporte sem promover o recibo documental a prova física? [ONTO]"}
    for k_, q_ in perguntas.items():
        assert q_.split(" [")[0] in ordem_txt, ("a pergunta nas quatro linguas nao esta na ORDEM como transcrita", k_)
    return {"registro": DL.HMS13_REGISTRO, "tag": DL.TAG_HMS13, "veredito_ok": DL.VEREDITO_HMS13_OK, "veredito_recusa": DL.VEREDITO_HMS13_RECUSA, "n_checks": DL.N_CHECKS_HMS13,
            "campos": campos, "campos_da_ordem_secao": "ORDEM_CLAUDE_UMPY_HMS_13.md §3.7",
            "insumos": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "rel": v_["rel"]} for k_, v_ in ins.items()}, "pinos_build": {k_: {"sha256": v_["sha256"], "bytes": v_["bytes"], "rel": v_["rel"]} for k_, v_ in pinos.items()},
            "handoff": {"status": hj["status"], "rehash_required_immediately_before_build": hj["rehash_required_immediately_before_build"], "base_candidate_observed_sha16": hj["base_candidate_observed"]["sha256"][:16], "sha256": pinos["HANDOFF_CLAUDE_UMPY_HMS_13.json"]["sha256"]},
            "ordem": {"sha256": pinos["ORDEM_CLAUDE_UMPY_HMS_13.md"]["sha256"], "sha16_do_desenho": DL.HMS13_ORDEM_SHA16_DO_DESENHO, "estatuto": "[DECLARADO pelo Kimi K3 Pro, 09/11/2026; hashes lidos; ratificada pelo operador por sha256 (D80)]", "limites_valem_como_contrato": True},
            "ratificacao": rat, "cadeia_de_autoridade": ["a ORDEM do Kimi K3 Pro a gerencia (09/11/2026) [DECLARADO pelo Kimi; hashes conferidos por script]", "a ratificacao do operador (09/11/2026), verbatim por sha256: a frase final da fala, que aponta o HANDOFF", "a D80 da gerencia c1 (AO LADO do DESENHO_v410): o que entra, como, e o que nao entra"],
            "ids_calibradores": ids, "fontes_primarias": fontes, "cobertura": {k_: list(v_) for k_, v_ in manif["coverage"].items()}, "cobertura_extra_no_manifesto": cob_extra, "archive_statuses": statuses,
            "nota_cobertura": "mapa.primary_sources ⊆ manifest.coverage ⊆ manifest.sources; onde o manifesto cobre um objeto com fonte que o mapa nao lista, a diferenca esta' em cobertura_extra_no_manifesto (medida no build, conferida no rito)", "estados_cobertura": {o_["CID"]: o_["covariance_status"] for o_ in mapa["objects"]},
            "status_esperados": {"mapa": mapa["status"], "manifest": manif["status"], "validacao": valid["status"], "levantamento": "PRIMARY_SOURCES_MAPPED__PARTIAL_COMPONENTS_ONLY__PHYSICAL_COVARIANCE_OPEN"},
            "proibicoes_do_mapa": list(mapa["prohibitions"]), "estruturas_compartilhadas": sorted(mapa["shared_structures"]),
            "numeros_permitidos": list(DL.HMS13_NUMEROS_PERMITIDOS), "comprimentos_proibidos": list(DL.HMS13_COMPRIMENTOS_PROIBIDOS), "guarda_numerica_no_build": {"permitidos": gn["permitidos"], "chaves_permitidas_vistas": gn["chaves_permitidas_vistas"], "proibidos": gn["proibidos"], "listas_numericas": gn["listas_numericas"], "ok": gn["ok"]},
            "h0dn": {"registro": DL.H0DN_REGISTRO, "veredito_ok": contrato_h0dn["veredito_ok"], "n_pinos_freeze": contrato_h0dn["n_pinos_freeze"], "n_pinos": len(contrato_h0dn["insumos"]) + len(contrato_h0dn["pinos_freeze_r2_so_no_disco"]), "freeze_r2_sha256": freeze_sha, "freeze_r2_arquivos": freeze_arqs},
            "aditivo_posterior_ao_freeze_r2": True, "le_em_rito": False, "observed_vector_read": False, "observed_paths": [], "pasta_origem_do_build": DL.HMS13_DIR, "pasta_vedada": DL.H0DN_PASTA_VEDADA, "nomes_vedados_partes": [[n_[:len(n_) // 2], n_[len(n_) // 2:]] for n_ in DL.H0DN_NOMES_VEDADOS],
            "tokens_proibidos_partes": [[t_[:-4], t_[-4:]] for t_ in DL.TOKENS_PROIBIDOS_H0DN], "frase_obrigatoria_pt": DL.FRASE_HMS13_OBRIGATORIA_PT, "frase_obrigatoria_en": DL.FRASE_HMS13_OBRIGATORIA_EN, "pergunta_nas_quatro_linguas": perguntas,
            "baseline": {"version": DL.BASE_VERSION, "gate_verdict": gate0}, "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D78", "D79", "D80")}, "n_linhas_levantamento": lev.count("\n") + 1}


def texto_hms13():
    Q = DL.FRASE_HMS13_OBRIGATORIA_PT; QH = DL.FRASE_H0DN_OBRIGATORIA_PT; R = DL.HMS13_TRECHO_RATIFICACAO
    return {
        "estatuto": "[REAL_DOCUMENTAL__PHYSICS_OPEN] o que o registro CONFERE neste rito: os quatro artefatos documentais embutidos (lidos no build da entrega do Kimi, por bytes e sha256, D80), os 13 IDs dos calibradores, as 18 fontes primarias (titulo, URL, sha256 do arquivo e do texto), "
                    "os fatores PARCIAIS de erro por linha dos arquivos upstream (a sigma da SN, o erro do modulo de distancia do hospedeiro, a ancora, o MAS, o grupo), os dez campos obrigatorios da ORDEM, a guarda numerica, o gate. [DECLARADO pelo Kimi] o conteudo dos artefatos (o validador dele: 13/13 objetos, 18/18 arquivos). "
                    "[INPUT] a ordem do operador (09/11: «" + R + "», a frase final da fala, por sha256; o resto da fala nao entra por este registro). [OPEN] a covariancia fisica conjunta (G3/G4), a decomposicao completa dentro de cada SN, a matriz completa entre os 13, a revisao fisica independente. "
                    "H0DN x BG1: " + QH + ". HMS/13: " + Q + ".",
        "escopo": "[REAL_DOCUMENTAL] O que entra no um.py (D80; a ORDEM do Kimi como contrato): um registro ADITIVO e POSTERIOR ao FREEZE_R2 de 06/11 (os 9 pinos do congelamento e os 11 do registro h0dn_bg1_v410 nao mudam; nenhum artefato daqui repete um pino do congelamento), com a cobertura documental de 18 fontes primarias dos 13 calibradores fora do R22: "
                  "o mapa de fontes e covariancia (erro diagonal da SN, do hospedeiro, da ancora N4258, do MAS e do grupo, por linha; os compartilhamentos N1404, N1316, A25/CCHP/Ex e N4258; a covariancia do fluxo de Hubble fora destes calibradores), o manifesto das fontes (titulo, URL, sha256 do arquivo e do texto extraido), a validacao e o levantamento legivel. "
                  "A forma HMS completa e' so' DIAGNOSTICO, nao admitida: a diagonal HMS ja' esta contida no erro do modulo de distancia e duplicaria variancia. O que NAO e': covariancia fisica fechada; abertura; 5 sigma; prova fisica. Os campos obrigatorios: estatuto REAL_DOCUMENTAL__PHYSICS_OPEN; fontes_primarias 18; calibradores 13; "
                  "partial_components_only verdadeiro; full_13x13_covariance_available, within_SN_full_decomposition_available, physical_covariance_closed, independent_physical_review_complete, full_HMS_admitted e opening_allowed falsos. A cadeia de autoridade: a ORDEM do Kimi [DECLARADO] -> a ratificacao do operador por sha256 -> a D80 da gerencia. "
                  "A PERGUNTA NAS QUATRO LINGUAS (ORDEM §5, do Kimi): TGL, que produtos internos dos ajustes separam a variancia independente da compartilhada sem repetir hospedeiro, MAS, ancora ou intrinseco; teologica [ONTO], que testemunha externa certifica que a decomposicao esta completa e nao apenas bem nomeada; "
                  "linguistica, como preservar no registro a diferenca entre 18 fontes cobertas, fatores parciais derivados e covariancia fisica fechada (que aqui nao ha'); juridica [ONTO], qual prova adicional e qual revisao independente autorizam um futuro teste de suporte sem promover o recibo documental a prova fisica. "
                  "Em rito, nenhum arquivo da pasta do Kimi e' aberto: o registro confere so' o conteudo embutido. H0DN x BG1 segue " + QH + ". HMS/13: " + Q + ".",
        "o_que_falta": ["G3/G4: a covariancia fisica conjunta, sem duplicar a Cefeida nem a diagonal HMS [OPEN]", "a decomposicao completa dentro de cada SN (dispersao intrinseca; fotometria-modelo-extincao) e a matriz completa entre os 13 alem dos fatores documentados [OPEN]",
                        "o orcamento optico original completo de SN 1992A (NOT_FOUND_ORIGINAL_FULL_BUDGET) [OPEN]", "a revisao fisica independente, a contabilidade da selecao de rotas e, so' depois, um novo teste de suporte [OPEN]"],
        "ressalvas": ["o registro e' DOCUMENTAL: cobre fontes, hashes, IDs e componentes de erro; nao fecha a covariancia fisica, nao abre o teste, nao calcula Z, t, h_hat ou razao, nao gera semente; " + Q,
                      "a forma HMS completa nao e' admitida (duplicaria a variancia ja' contida no erro do modulo de distancia): e' diagnostico; ausencia de matriz publicada nao e' independencia; fotometria publica nao e' covariancia pronta (as proibicoes do mapa)",
                      "o conteudo dos artefatos e' [DECLARADO pelo Kimi]; o que o registro prova e' o pino (os bytes embutidos sao os lidos no build) e a coerencia interna (IDs, fontes, bandeiras, estatutos); a revisao fisica independente segue aberta",
                      "so' a frase final da fala do operador e' citada por este registro; a cunhagem que a antecede nao entra por ele (D80: provar ou podar; D82: e' materia da pedra nova, parte 2); o arquivo inteiro entra por sha256; o nome do arquivo nao se cita",
                      "beta entra so' por nome; o gate nao se move; NOT_FALSIFIED nunca e' confirmacao; a regra do 4,44 vale em qualquer texto que o cite"],
        "limites": ["[OPEN] a covariancia fisica conjunta (G3/G4): ate' la', a funcao de veredito do H0DN so' pode devolver inconclusivo por sistematica", "[DECLARADO] o conteudo dos artefatos do Kimi, pinado por sha256", "[REAL_DOCUMENTAL] o registro CONFERE o embutido e nao abre: nenhum arquivo da pasta do Kimi e' lido em rito",
                    "[REAL] " + Q, "[REAL] " + QH],
        "diz": ["a cobertura documental das 18 fontes primarias dos 13 calibradores esta' embutida por sha256 (lida no build, D80), aditiva e posterior ao FREEZE_R2, com os dez campos da ORDEM do Kimi exatamente: " + Q,
                "os 13 IDs e as 18 fontes conferem entre o mapa, o manifesto e a validacao; as bandeiras de fechamento sao falsas nos tres; a guarda numerica passa (so' bytes, contagens, linhas, caracteres de texto e componentes de erro; nenhuma lista numerica)",
                "o registro h0dn_bg1_v410 e o seu FREEZE_R2 nao mudaram; a funcao de veredito e' a mesma; o gate e' o mesmo da v409 selada; nenhuma chave antiga muda; nenhum arquivo da pasta do Kimi e' aberto em rito; H0DN x BG1: " + QH],
        "nao_diz": ["que a covariancia fisica esteja fechada: nao esta' (G3/G4 abertos); " + Q, "que o teste tenha sido aberto ou que exista desvio observado: nenhum vetor observado e' lido; H0DN x BG1: " + QH,
                    "que a forma HMS completa seja admitida: nao e' (duplicaria variancia); que ausencia de matriz seja independencia: nao e'", "que o recibo documental seja prova fisica ou leitura de 5 sigma: nao e'; que o gate tenha se movido: nao se moveu",
                    "que a cunhagem da mesma fala do operador entre por este registro: nao entra por ele (D80; D82: e' materia da pedra nova, parte 2)"],
        "extras": {"obrigatoria_pt": Q, "obrigatoria_en": DL.FRASE_HMS13_OBRIGATORIA_EN, "moldura_en": "documentary coverage of 18 primary sources for the 13 calibrators outside R22, additive and posterior to FREEZE_R2; partial error components only; the full HMS form is diagnostic, not admitted; " + DL.FRASE_HMS13_OBRIGATORIA_EN + "; H0DN x BG1: " + DL.FRASE_H0DN_OBRIGATORIA_EN,
                   "decisoes": {k_: DL.DECISOES[k_] for k_ in ("D78", "D79", "D80")}, "leituras_do_operador": {"a_ratificacao_hms13": DL.LEITURA_V410["a_ratificacao_hms13"]}, "assinatura_das_erratas": DL.ASSINA, "regra_do_4_44": DL.REGRA_DO_4_44},
    }
