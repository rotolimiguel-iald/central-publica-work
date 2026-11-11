# -*- coding: utf-8 -*-
"""_r6c_13_aditivo1_orquestrador_v410.py -- ADITIVO 1 a ordem do conserto unico (gerencia c1, 10/11/2026; a custodia da v410 e' automatica), parte B, FORA do candidato: no orquestrador
(orquestrador\\pos_treino_v410.py) um passo FINAL novo, S9_gatilho_custodia, depois de tudo: escreve work\\cadeia_de_selo\\v410\\ORDEM_HANDOFF_CUSTODIA_v410.md (o gatilho que a sessao de custodia espera),
pelo molde da v409 (as mesmas secoes), com TODOS os valores LIDOS por script. So' escreve SE todos os passos anteriores estiverem feitos e verdadeiros, o HANDOFF existir no Nos com os sete marcadores e os dois
blocos do README, e o portao do G1 tiver rodado limpo no S6d; senao NAO escreve e registra o motivo (fail-closed). A escrita e' por temporario e os.replace. O orquestrador continua SEM S7 e SEM S10.
Idempotente; backup de BYTES; LF como o arquivo; temporario + os.replace; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "orquestrador", "pos_treino_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8"); assert "\r\n" not in t; log = []


def tr(a, b, n=1):
    global t
    c = t.count(a)
    if c == 0 and b in t:
        log.append("ja' feito: " + a[:50]); return
    assert c == n, ("contagem", c, "esperado", n, a[:140])
    t = t.replace(a, b); log.append("trocado x%d: %s" % (c, a[:50]))


NOVO = r'''# ---------------------------------------------------------------- S9_gatilho_custodia (ADITIVO 1 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' AUTOMATICA, por ordem do operador a sessao de custodia)
PASSOS_ANTES_DO_GATILHO = ("S0_treino", "S1_prep", "S1b_revisao", "S2_prevoo", "S3_instalar", "S4_rito", "S5_cadeia_0_10", "S6a_parada", "S6a_chain", "S6b_aplicar", "S6c_religamento", "S6c_chain_10c_14", "S6d_textos_custodia", "S8_nativa")   # (D57: sem S7_g1 e sem S10_app nesta versao)
GATILHO = PK / "ORDEM_HANDOFF_CUSTODIA_v410.md"   # o arquivo-gatilho que a sessao de custodia espera
ORDEM_PUBLICACAO = CEN / "work" / "cunhagens_13out" / "OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"   # a ORDEM DE PUBLICACAO da v410 (o caminho do --ordem; o sha16 e' LIDO do arquivo)
TRECHO_PUBLICACAO = "quando isso acontecer quero que vc atualize tudo e publique tudo"   # (verbatim: conferido contra o arquivo antes de escrever)
DIVISAO_0411 = CEN / "work" / "cunhagens_13out" / "OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt"   # a divisao de 04/11 (como na v409)
MARCADORES_README = ("README_FRENTE", "README_O_QUE_SAI")   # os dois blocos do README que o gerador do handoff poe na secao «README: o que fica evidente» (ADITIVO 1)


def _gatilho_ler(e, nos, pk, cen_g1):
    """Le TUDO o que o gatilho cita (so' leitura) e junta os MOTIVOS pelos quais ele nao pode ser escrito (lista vazia = pode). Nenhum valor e' digitado: o selo, o um.py, o core, o ESPERADOS, o stdout do rito, os horarios,
    o ESTADO, o HANDOFF (pelo parser do proprio G1), o recibo dos textos, a revisao de terceiro e as falas do operador sao lidos dos arquivos."""
    import hashlib
    import types
    motivos = []; d = {}
    p = e.get("passos", {})
    faltam = [k for k in PASSOS_ANTES_DO_GATILHO if p.get(k, {}).get("ok") is not True]
    if faltam:
        motivos.append("passo anterior nao feito ou falso: " + ", ".join(faltam))
    s6d = p.get("S6d_textos_custodia", {})
    if s6d.get("portao_g1_handoff_inteiro") != "limpo":
        motivos.append("o portao do G1 nao rodou limpo no S6d: %r" % (s6d.get("portao_g1_handoff_inteiro"),))
    s6b = p.get("S6b_aplicar", {}); d["evento"], d["evento_hash"] = s6b.get("evento"), s6b.get("hash")
    if not (d["evento"] and d["evento_hash"]):
        motivos.append("o evento c1 do B(n) (S6b) nao tem seq e hash legiveis no ESTADO")
    # ---- o selo, o um.py, o core e o ESPERADOS
    pin = None
    try:
        selo = jload(nos / "um_absoluto_selo.json"); umb = (nos / "um.py").read_bytes(); pin = hashlib.sha256(umb).hexdigest()[:16]
        esp = jload(pk / "ESPERADOS_v410.json"); core = jload(nos / "um_absoluto.json")["core"]
        lad = core.get("external_ladder") or {}; gate = ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict")
        d.update(selo_ts=selo.get("timestamp"), selftest=selo.get("fail_closed_selftest"), pin=pin, um_bytes=len(umb), escada=[lad.get("n_theorems_clean"), lad.get("n_theorems_expected")], gate=gate)
        if selo.get("um_version") != "v410":
            motivos.append("o selo do Nos nao e' o da v410: %r" % (selo.get("um_version"),))
        if not (selo.get("sha256", {}).get("um.py", "")[:16] == pin == esp.get("candidato_sha16")):
            motivos.append("o um.py do Nos, o pino do selo e o candidato de ESPERADOS nao sao o mesmo")
        if selo.get("fail_closed_selftest") != "FAIL_CLOSED_SELFTEST_PASSED" or not selo.get("timestamp"):
            motivos.append("o selo nao traz FAIL_CLOSED_SELFTEST_PASSED (ou nao traz o timestamp)")
        if not (type(lad.get("n_theorems_clean")) is int and lad.get("n_theorems_clean") == lad.get("n_theorems_expected") == (esp.get("escada") or [None, None])[1]):
            motivos.append("a escada do core nao e' exata ou nao e' a de ESPERADOS: %r" % (d["escada"],))
        if not (isinstance(gate, str) and gate and gate == selo.get("qg_closure_verdict") == esp.get("qg_closure_gate_verdict_v409")):
            motivos.append("o veredito do gate (core, selo, ESPERADOS) nao e' o mesmo: o gate nao pode ter se movido")
    except Exception:  # noqa: BLE001
        motivos.append("selo, um.py, core ou ESPERADOS ilegiveis: " + traceback.format_exc()[-300:])
    # ---- o trailer do rito e os horarios
    try:
        linhas = (nos / "rodada_v410_stdout.txt").read_text(encoding="utf-8", errors="replace").rstrip().splitlines()
        d["trailer"] = next((l for l in reversed(linhas[-5:]) if l.startswith("RITO_RC=")), "")
    except Exception:  # noqa: BLE001
        d["trailer"] = ""
    if not (d["trailer"] == "RITO_RC=0" == p.get("S4_rito", {}).get("trailer")):
        motivos.append("o trailer do rito (stdout do Nos e S4) nao e' RITO_RC=0: %r" % (d["trailer"],))
    try:
        d["rito_h0"], d["rito_h1"] = (pk / "rito_horarios_v410.txt").read_text(encoding="utf-8").split()[:2]
        assert re.fullmatch(r"\d\d:\d\d:\d\d", d["rito_h0"]) and re.fullmatch(r"\d\d:\d\d:\d\d", d["rito_h1"])
    except Exception:  # noqa: BLE001
        motivos.append("os horarios do rito (rito_horarios_v410.txt) nao foram lidos")
    # ---- o HANDOFF no Nos, pelo parser do proprio G1: os sete marcadores, a secao README e os dois blocos do README
    corpos = {}
    try:
        sys.path.insert(0, str(CEN / "tools"))
        from custodia_g1 import nos as _NOSG1, textos as _TXG1   # o parser e o portao do G1 (os mesmos que a custodia usa)
        hp = nos / "HANDOFF_v410_CUSTODIA.md"
        if not hp.is_file():
            motivos.append("o HANDOFF nao existe no Nos")
        else:
            hb = hp.read_bytes(); d.update(handoff_bytes=len(hb), handoff_sha16=hashlib.sha256(hb).hexdigest()[:16])
            h = _NOSG1.ler_handoff(types.SimpleNamespace(NOS=nos, CEN=cen_g1), "v410"); corpos = dict(h.corpos)
            if h.problemas:
                motivos.append("o HANDOFF tem marcador com problema: %r" % (h.problemas[:3],))
            sem = ["%s_v410" % i for i in tuple(_TXG1.MARCADORES_OPCIONAIS) + MARCADORES_README if not corpos.get("%s_v410" % i, "").strip()]
            if len(_TXG1.MARCADORES_OPCIONAIS) != 7 or sem:
                motivos.append("o HANDOFF nao traz os sete marcadores e os dois blocos do README: faltam %s" % sem)
            i0 = h.texto.find("**README: o que fica evidente**"); i1 = h.texto.find("<!-- INICIO_README_FRENTE_v410 -->"); i2 = h.texto.find("<!-- INICIO_README_O_QUE_SAI_v410 -->")
            if not (0 <= i0 < i1 < i2):
                motivos.append("a secao «README: o que fica evidente» nao esta' no HANDOFF, ou os dois blocos do README nao vem depois dela, nesta ordem")
            o = h.o_que_e
            if not (o and o.versao == "v410" and o.pin16 == pin and o.rc0 and o.selftest_passou and o.gate_intocado and o.completa and o.escada == "%s/%s" % tuple(d.get("escada") or ("?", "?"))):
                motivos.append("o paragrafo «O que e'» do HANDOFF nao e' o desta versao (versao, pino, escada, COMPLETA, rc 0, selftest, gate intocado)")
    except Exception:  # noqa: BLE001
        motivos.append("o HANDOFF nao foi lido pelo parser do G1: " + traceback.format_exc()[-300:])
    # ---- o recibo dos textos (S6d): o HANDOFF nao mudou depois do portao; os dois blocos do README sao os do recibo e passaram nas guardas e no portao do G1
    try:
        rp = pk / "pos_rito" / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json"; rec = jload(rp); d["recibo_sha16"] = sha16(rp)
        rf = corpos.get("README_FRENTE_v410", "").strip("\n"); rs = corpos.get("README_O_QUE_SAI_v410", "").strip("\n")
        d.update(rf_bytes=len(rf.encode("utf-8")), arco_pt=str((rec.get("textos") or {}).get("ARCO_PT") or ""))
        if rec.get("sha16_depois") != d.get("handoff_sha16"):
            motivos.append("o HANDOFF do Nos nao e' o que o S6d gravou e passou pelo portao (sha16 do recibo != o de agora)")
        if not (rf and rf == rec.get("readme_frente") and rec.get("readme_frente_bytes_utf8") == d["rf_bytes"] and rs and rs == rec.get("readme_o_que_sai")):
            motivos.append("os dois blocos do README no HANDOFF nao sao os do recibo do S6d (texto ou bytes)")
        g = rec.get("guardas") or {}
        if not all(isinstance(g.get(i), dict) and g[i].get("guarda_frases_v410") == [] and g[i].get("portao_g1") == [] and g[i].get("forma") == [] for i in MARCADORES_README):
            motivos.append("o recibo do S6d nao mostra os dois blocos do README limpos nas guardas e no portao do G1")
        if not (d["arco_pt"] and d["arco_pt"] == corpos.get("ARCO_PT_v410", "").strip("\n")):
            motivos.append("o texto ARCO_PT do recibo nao e' o do HANDOFF")
    except Exception:  # noqa: BLE001
        motivos.append("o recibo dos textos da custodia (S6d) nao foi lido: " + traceback.format_exc()[-300:])
    # ---- a revisao de terceiro
    try:
        rvp = pk / "revisao_terceiro" / "REVISAO_TERCEIRO_v410.json"; rv = jload(rvp)
        sev = {}
        for a_ in (rv.get("achados") or []):
            if isinstance(a_, dict) and a_.get("sev"):
                sev[str(a_["sev"])] = sev.get(str(a_["sev"]), 0) + 1
        d.update(rev_sha16=sha16(rvp), rev_revisor=str(rv.get("revisor") or "n/d"), rev_sev=sev)
        if not (rv.get("aprovada") is True and rv.get("candidato_sha16") == pin):
            motivos.append("a revisao de terceiro nao esta' aprovada sobre este candidato")
    except Exception:  # noqa: BLE001
        motivos.append("a revisao de terceiro nao foi lida: " + traceback.format_exc()[-300:])
    # ---- as falas do operador: a ordem desta versao, a ORDEM DE PUBLICACAO e a divisao de 04/11
    try:
        d["ordem_sha16"] = _conferir_ordem()
        d["pub_sha16"] = sha16(ORDEM_PUBLICACAO); d["div_sha16"] = sha16(DIVISAO_0411)
        if TRECHO_PUBLICACAO not in ORDEM_PUBLICACAO.read_text(encoding="utf-8"):
            motivos.append("o trecho citado da ORDEM DE PUBLICACAO nao esta' no arquivo da fala")
    except Exception:  # noqa: BLE001
        motivos.append("as falas do operador (a ordem, a ORDEM DE PUBLICACAO, a divisao de 04/11) nao foram lidas: " + traceback.format_exc()[-300:])
    d["n_autoria"] = len(_DL.NOMES_DECLARADOS_PELA_AUTORIA_AESCALA)
    return d, motivos


def _gatilho_render(d):
    """O texto do gatilho, pelo molde da v409 (work/cadeia_de_selo/v409/ORDEM_HANDOFF_CUSTODIA_v409.md: as mesmas secoes); todo valor vem de `d` (lido por _gatilho_ler)."""
    hoje = dt.date.today(); sev = d.get("rev_sev") or {}
    rev_n = (" (" + ", ".join("%d %s" % (sev[k], k) for k in sorted(sev)) + ")") if sev else ""
    L = ["# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v410 SELADA (%s)" % hoje.strftime("%d/%m/%Y"), "",
         "> Para a sessão de custódia (o papel que fez a custódia da v409 pelo G1). Escrita pelo orquestrador da v410 (passo S9_gatilho_custodia), por ordem da gerência c1: a custódia desta versão é automática, por ordem do operador de 10/11/2026, "
         "e este arquivo é o gatilho que a sessão de custódia espera. Ele só é escrito com todos os passos anteriores feitos, o HANDOFF no Nós com os sete marcadores e os dois blocos do README, e o portão do G1 limpo no S6d. "
         "Vale a regra de custodiar sempre que o handoff aparecer: as três marcas estão no Nós.", "",
         "## A ordem do operador", "",
         "- `%s` (sha16 `%s`): «%s»; «%s» — a ordem desta versão." % (ORDEM.name, d["ordem_sha16"], _DL.FRASE_ORDEM_V410, _DL.FRASE_TUDO_ENTRA),
         "- `%s` (sha16 `%s`): «%s» — a ORDEM DE PUBLICAÇÃO desta versão (use este caminho em `--ordem`)." % (ORDEM_PUBLICACAO.name, d["pub_sha16"], TRECHO_PUBLICACAO),
         "- A divisão de 04/11 (`%s`, sha16 `%s`): a custódia inteira é da sessão de custódia; a c1 fica só com o um.py." % (DIVISAO_0411.name, d["div_sha16"]), "",
         "## O estado, lido em %s por script" % hoje.strftime("%d/%m"), "",
         "- Selo do Nós **v410** (timestamp %s; `%s`; `%s`); `um.py` sha16 **`%s`** (%d B); escada **%s/%s**; gate intocado (`%s…`)." % (d["selo_ts"], d["selftest"], d["trailer"], d["pin"], d["um_bytes"], d["escada"][0], d["escada"][1], d["gate"][:60]),
         "- Rito %s–%s; pós-rito 0 → 14 OK; Bancada: o B(n) da versão aplicado (evento %s, hash `%s`), serviço religado." % (d["rito_h0"][:5], d["rito_h1"][:5], d["evento"], d["evento_hash"]),
         "- `Nós\\HANDOFF_v410_CUSTODIA.md` (%d B, sha16 `%s`) com os sete textos, os parágrafos prontos e, na seção “README: o que fica evidente”, os dois blocos do README (`README_FRENTE_v410`, %d bytes em UTF-8, e `README_O_QUE_SAI_v410`); "
         "recibo `work\\cadeia_de_selo\\v410\\pos_rito\\RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json` (sha16 `%s`); o portão do G1 rodou sobre o HANDOFF INTEIRO no S6d: limpo." % (d["handoff_bytes"], d["handoff_sha16"], d["rf_bytes"], d["recibo_sha16"]),
         "- O orquestrador da v410 NÃO tem S7 (G1 --publicar) nem S10 (release do app): a cadeia termina no handoff; a custódia é sua.",
         "- Revisão de terceiro: `work\\cadeia_de_selo\\v410\\revisao_terceiro\\REVISAO_TERCEIRO_v410.json` (sha16 `%s`), aprovada sobre o candidato `%s`; revisor: %s%s." % (d["rev_sha16"], d["pin"], d["rev_revisor"], rev_n), "",
         "## O que entrou (para a custódia saber o que publica)", "",
         d["arco_pt"], "",
         "## O que é da custódia, na ordem", "",
         "1. `custodiar.py planejar --versao v410 --seco` → `custodiar.py executar --versao v410 --publicar --ordem \"%s\"` → `custodiar.py auditar --versao v410`. Nunca `--aceitar-molde`; não editar insumos." % ORDEM_PUBLICACAO,
         "2. O README do espelho, pela seção “README: o que fica evidente” do handoff: o bloco pronto para a frente (entre os marcadores `README_FRENTE_v410`) e o que sai (entre os marcadores `README_O_QUE_SAI_v410`).",
         "3. A release v410 do app, os dispositivos, a Central, o site e os links pelo G1.",
         "4. A linha do MEMORY.md é promoção da gerência: depositar na fila (`memoria.py depositar`) e avisar a c1.", "",
         "## Notas", "",
         "- O teste H0DN × BG1 NÃO foi aberto, e o README diz isso.",
         "- %d nomes da pedra `AEscala` seguem [DECLARADO pela autoria], pendentes de confirmação do operador (a lista está no handoff)." % d["n_autoria"],
         "- A custódia decidiu “accreditation” na prosa em inglês do README; os conectores novos do bloco já a usam; as constantes do delta trazem “creditation” e a unificação fica para a versão seguinte.", "",
         "Validade no kernel não é creditação; NOT_FALSIFIED nunca é CONFIRMED; o gate não se move.", "",   # (sem crases: a formula da regua que o portao do G1 reconhece e' a frase inteira, letra por letra)
         "— gerência c1, pelo orquestrador da v410 (passo S9_gatilho_custodia), %s." % hoje.strftime("%d/%m/%Y"), ""]
    return "\n".join(L)


def s9_gatilho_custodia(e, nos=None, pk=None, destino=None, cen_g1=None):
    """S9_gatilho_custodia (ADITIVO 1, 10/11/2026): o passo FINAL, depois de tudo. Escreve o gatilho da custodia (ORDEM_HANDOFF_CUSTODIA_v410.md) SO' SE todos os passos anteriores estiverem feitos e verdadeiros, o HANDOFF existir no Nos
    com os sete marcadores e os dois blocos do README, e o portao do G1 tiver rodado limpo no S6d (mais: o selo, o um.py, a escada, o gate, o trailer do rito, o recibo dos textos e a revisao de terceiro conferem). Senao NAO escreve e
    registra o motivo: a custodia continua esperando (fail-closed). Nao sobrescreve um gatilho que ja' exista. A escrita e' por temporario e os.replace: o arquivo e' o gatilho e tem de aparecer inteiro.
    (nos, pk, destino e cen_g1 so' mudam nos testes em sandbox; em producao sao os da casa.)"""
    if feito(e, "S9_gatilho_custodia"):
        return True
    nos = Path(nos) if nos else NOS; pk = Path(pk) if pk else PK; destino = Path(destino) if destino else GATILHO; cen_g1 = Path(cen_g1) if cen_g1 else CEN
    try:
        d, motivos = _gatilho_ler(e, nos, pk, cen_g1)
        if destino.exists():
            motivos.append("o gatilho ja' existe e este passo nao o registrou: nao sobrescrevo (%s)" % destino.name)
        txt = ""
        if not motivos:
            txt = _gatilho_render(d)
            import guarda_frases_v410 as _GF   # as mesmas guardas dos textos da custodia: a guarda das frases da v410 e o portao do G1 (os hashes conhecidos sao os do proprio texto, lidos por script)
            from custodia_g1 import textos as _TXG1
            conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", txt)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", txt))
            viol = [list(x) for x in _GF.violacoes(txt)] + list(_TXG1.portao(txt, conh, rotulo=destino.name))
            if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", txt) or (re.search(r"(?i)kimi", txt) and not re.search(r"(?i)h0dn", txt)) or any(x_.lower() in txt.lower() for x_ in _DL.FORA_D65):   # (a MESMA regra do S6d: a D59, com o nome do executor so' no contexto do H0DN, e a D65)
                viol.append("D59/D65: o gatilho traz o que fica fora dos textos")
            if viol:
                motivos.append("o texto do gatilho nao passa nas guardas: %r" % (viol[:3],))
        if motivos:
            marcar(e, "S9_gatilho_custodia", False, gatilho_escrito=False, motivo=motivos[:10])
            log("S9_gatilho_custodia: o gatilho NAO foi escrito; a custodia continua esperando (fail-closed); a gerencia decide")
            return False
        b = txt.encode("utf-8"); tmp = destino.with_name(destino.name + ".tmp")
        tmp.write_bytes(b); assert tmp.stat().st_size == len(b) > 0
        os.replace(tmp, destino); assert destino.read_bytes() == b
        marcar(e, "S9_gatilho_custodia", True, gatilho_escrito=True, gatilho=str(destino), bytes=len(b), sha16=sha16(destino), handoff_sha16=d["handoff_sha16"], readme_frente_bytes_utf8=d["rf_bytes"], ordem_de_publicacao=str(ORDEM_PUBLICACAO), ordem_de_publicacao_sha16=d["pub_sha16"])
        log("S9_gatilho_custodia: o gatilho da custodia foi escrito (%s; %d B): a custodia da v410 e' da sessao de custodia" % (destino, len(b)))
        return True
    except Exception:  # noqa: BLE001
        marcar(e, "S9_gatilho_custodia", False, gatilho_escrito=destino.exists(), erro=traceback.format_exc()[-600:]); return False


'''
if "def s9_gatilho_custodia(" not in t:
    anc = "def s9_relatorio(e):\n"; assert t.count(anc) == 1
    t = t.replace(anc, NOVO + anc); log.append("o passo S9_gatilho_custodia acrescentado antes de s9_relatorio")
tr("  S9  relatório RELATORIO_POS_TREINO_v410.{json,md} + anotação no PROGRAMA.\n",
   "  S9  relatório RELATORIO_POS_TREINO_v410.{json,md} + anotação no PROGRAMA.\n"
   "  S9_gatilho_custodia (ADITIVO 1 à ordem do conserto único, 10/11/2026: a custódia da v410 é automática): o passo FINAL, depois de tudo: escreve work/cadeia_de_selo/v410/ORDEM_HANDOFF_CUSTODIA_v410.md, o gatilho que a sessão de custódia espera, pelo molde da v409, com todos os valores LIDOS por script;\n"
   "      só escreve SE todos os passos anteriores estiverem feitos e verdadeiros, o HANDOFF existir no Nós com os sete marcadores e os dois blocos do README, e o portão do G1 tiver rodado limpo no S6d; senão NÃO escreve e registra o motivo (fail-closed); a escrita é por temporário e os.replace.\n")
tr('    passos = ["S0_treino", "S1_prep", "S1b_revisao", "S2_prevoo", "S3_instalar", "S4_rito", "S5_cadeia_0_10", "S6a_parada", "S6a_chain", "S6b_aplicar", "S6c_religamento", "S6c_chain_10c_14", "S6d_textos_custodia", "S8_nativa"]',
   '    passos = list(PASSOS_ANTES_DO_GATILHO) + ["S9_gatilho_custodia"]')
tr('    print("arquivos que o orquestrador usa e NÃO existem:", faltam or "nenhum")',
   '    faltam += [str(x) for x in (ORDEM_PUBLICACAO, DIVISAO_0411) if not Path(x).exists()]   # (ADITIVO 1) as falas que o gatilho da custodia cita\n'
   '    print("gatilho da custodia (S9_gatilho_custodia):", ("JA EXISTE: %s" % GATILHO) if GATILHO.exists() else "ainda nao escrito (so\' sai com tudo feito, o HANDOFF com os sete marcadores e os dois blocos do README, e o portao do G1 limpo no S6d)")\n'
   '    print("arquivos que o orquestrador usa e NÃO existem:", faltam or "nenhum")')
tr("        for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s8_nativa):",
   "        for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s8_nativa, s9_gatilho_custodia):")
ast.parse(t)
b1 = t.encode("utf-8")
if b1 != b0:
    bak = p + ".bak_" + TS + "_aditivo1"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    tmp = p + ".tmp_r6c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > len(b0); os.replace(tmp, p); assert open(p, "rb").read() == b1
print("orquestrador/pos_treino_v410.py:", "MUDOU" if b1 != b0 else "igual", log)
