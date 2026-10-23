# -*- coding: utf-8 -*-
# Os TEXTOS da v397 selada (molde: textos_v396.py), ESCRITOS para o delta da v397: o módulo de kernel `Token` (o nome «token» é do operador, 23/10/2026; compõe, por citação, `psibit_is_the_mode_of_the_reader` e
# `the_psion_inhabits_the_static_witness`), o registro `teste_de_veracidade_fase9_v397` (nome PROVISÓRIO: quem nomeia é o operador; LÊ o resultado do Teste da Única Palavra, aberto UMA vez em 23/10, por sha256, ao lado do V1;
# NENHUM σ novo), as QUATRO falas do operador de 23/10 e o QUADRO «O Teste da Única Palavra» no topo do artigo e do .md. Cada número, hash e veredito entra por chave de V (leitura_v397.ler), por ESPERADOS ou pelo core
# do Nós, ou é LIDO de um arquivo aqui, nunca digitado; o que aqui vai escrito à mão é só prosa, nome de termo (conferido em tempo de execução no kernel do Nós, no um.py ou no pacote) e a frase curta do operador
# (conferida palavra por palavra contra os bytes das falas).
# REGRA DA ORDEM DO OPERADOR (23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no início do artigo, no README e em tudo mais): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item
# (a discriminação a 5σ, o degrau da creditação, NÃO foi alcançada; NOT_FALSIFIED nunca é a palavra da creditação; o gate não se move; o teste não foi cego). A frase do operador entra VERBATIM (nunca parafraseada entre aspas); os números
# do quadro e do parágrafo do README/site saem das MESMAS funções (quadro_v397 / runtime_quadro_v397), sobre o core SELADO do Nós.
# Estatutos marcados; erratas AO LADO, em nome próprio da gerência c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a tradução falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v397.py) rodam sobre cada texto renderizado em superficies_v397.py, fechar_v397.py e registrar_mapa_v397.py e sobre este arquivo na cadeia. A palavra recusada nunca
# aparece aqui: a recusa é dita como «creditação».
# ERRATA DA v397 (dita DENTRO dos blocos datados, nunca inline e nunca no CLAUDE.md da raiz): o registro `kh_n1_cobertura_v396` e os cinco contratos (expected_ladder), que a v397 corrige ao lado.
# NÃO é teste novo: a ordem de processo do operador de 22/10 (nada de teste armado) molda o delta; o registro de veracidade LÊ o resultado da abertura única de 23/10, não abre dado, não calcula σ e não acrescenta rito.
import hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V397"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v397 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v397-selada-o-teste-da-unica-palavra.md"
# os marcadores entre os quais o handoff traz o PARAGRAFO PRONTO do README do espelho e do site (o harness e a sessao do site os procuram)
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
# a ordem de processo do operador de 22/10 («nada de teste armado, gordura no um.py»): INSTRUCAO que molda o delta; nao e' uma das quatro falas embutidas
ARQ_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")
# o tema de cada uma das quatro falas de 23/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16 e a data vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("fase9_decisoes_unica_palavra", "as decisões da Fase 9: a única palavra que o Nome pronuncia é Betatgl; o devido processo legal, a lei anterior à lei, e não a coisa julgada; aceita o veredito do teste da Única Palavra: observar é nomear [INPUT/ONTO]"),
    ("nome_da_pedra_token", "o nome da pedra é «token» [INPUT]"),
    ("teste_de_veracidade_palavra_flutua", "o que se quer é um teste de veracidade (conjugar os fatores num resultado único); a leitura binária do operador, 1=1 verdadeiro e 1=0 falso; o teste lido sobre uma face e relido sobre a outra; a «palavra» como o quantum mínimo de permanência (o psion, o psibit) que flutua sobre o abismo, o referente último [INPUT/ONTO]"),
    ("4_44_silencio_forcado", "reportar o z_disc calibrado no início do artigo, no README e em tudo mais, porque basta para a leitura conjunta de todo o acervo; o 5σ é o degrau da creditação, e o silêncio forçado pela lógica é leitura dele [INPUT/ONTO]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte ou homonimo tem de existir como arquivo
_NOMES_KERNEL = ("token_is_the_psibit_in_the_static_witness", "psibit_is_the_mode_of_the_reader", "the_psion_inhabits_the_static_witness", "the_psion_face_of_the_psibit", "FockCertificate", "psionCorner", "the_collapse_of_the_psion_echoes_its_identity")
_MODULOS_KERNEL = ("Token", "TestemunhaEstatica", "Psibit", "TheImportedSecondQuantization")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "hubble_ratio_opening_v388", "_V397_VERACIDADE_SPEC", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444", "testemunha_estatica_v396",
             "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
_CACHE = {}


def _g(d, *ks):
    for k in ks:
        d = (d or {}).get(k) if isinstance(d, dict) else None
    return d


def _kernel_tem(nomes):
    """Fail-closed: cada nome de termo citado aqui tem de existir em algum .lean de TGLExt/ do Nos (lido na hora)."""
    if "kernel" not in _CACHE:
        base = os.path.join(NOS, "tgl_kernel", "TGLExt"); blob = []
        for r, ds, fs in os.walk(base, followlinks=False):
            ds[:] = [d for d in ds if not os.path.islink(os.path.join(r, d))]
            for f in fs:
                if f.endswith(".lean"):
                    blob.append(open(os.path.join(r, f), encoding="utf-8", errors="replace").read())
        _CACHE["kernel"] = "\n".join(blob)
    for n in nomes:
        assert n in _CACHE["kernel"], "termo citado nao esta no kernel do Nos: %s" % n


def _modulos_tem(nomes):
    """Cada modulo citado existe como arquivo .lean em TGLExt/ do Nos."""
    for n in nomes:
        assert os.path.isfile(os.path.join(NOS, "tgl_kernel", "TGLExt", n + ".lean")), "modulo citado nao esta no kernel do Nos: %s" % n


def _um_tem(nomes):
    """Cada identificador do um.py citado aqui existe no um.py do Nos (lido na hora)."""
    if "um" not in _CACHE:
        _CACHE["um"] = open(os.path.join(NOS, "um.py"), encoding="utf-8", errors="replace").read()
    for n in nomes:
        assert n in _CACHE["um"], "identificador citado nao esta no um.py do Nos: %s" % n


def _conferir_nomes():
    if "nomes_ok" not in _CACHE:
        _kernel_tem(_NOMES_KERNEL); _modulos_tem(_MODULOS_KERNEL); _um_tem(_NOMES_UM)
        _CACHE["nomes_ok"] = True


# ---------------------------------------------------------------- v397: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v397.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v397.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v396 selada (a copia de bytes em base_v396): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v396", "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["base_core"]


def _qd():
    """O modulo quadro_v397 (da pasta do pacote): as MESMAS funcoes que o artigo, o .md e o paragrafo do README/site usam."""
    if "qd" not in _CACHE:
        if PK not in sys.path:
            sys.path.insert(0, PK)
        import quadro_v397 as QD
        _CACHE["qd"] = QD
    return _CACHE["qd"]


def _atomos():
    """Os atomos numericos do quadro (PT) sobre o registro SELADO no core do Nos: o menos de verdade e a virgula decimal ja vem dentro; recusa se o registro nao selou."""
    a = _qd().Q._v397_atomos(_core().get("teste_de_veracidade_fase9_v397") or {}, "pt")
    assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core do Nos (algum numero ausente ou all_verified falso): nenhum texto diz o 4,44 assim"
    return a


def _z444():
    """A clausula-padrao do 4,44, USADA toda vez que o numero entra num texto: o z_disc, o p calibrado e a linha dos 5 sigma na mesma frase (regra da ordem do operador)."""
    a = _atomos()
    return "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (a["z_disc"]["md"], a["p_disc"]["md"], a["z_disc"]["md"])


def _ins_tem(arquivo, *trechos):
    """Cada trecho tem de estar no insumo pinado (fail-closed): o texto so' afirma o que a fonte pinada diz."""
    t = open(os.path.join(PK, "insumos", arquivo), encoding="utf-8").read()
    for x in trechos:
        assert x in t, "o insumo %s nao traz: %s" % (arquivo, x)


def _falas():
    """As quatro falas de 23/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text}}."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v397_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a fala %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a fala %s nao confere com o sha256 de ESPERADOS" % s
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": fs[0][len(s) + 1:], "text": b.decode("utf-8")}
        assert len(out) == len(_TEMAS) == 4, "as falas de ESPERADOS nao sao as quatro de 23/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica fala cujo arquivo de origem contem `sub` (as falas sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("fala nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das quatro falas, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao. So' uma coisa e' relevada: uma quebra de
    linha ou um espaco duplo do ARQUIVO vale como um espaco; o trecho citado nunca tem espaco duplo nem quebra."""
    assert "\n" not in trecho and "  " not in trecho, "o trecho citado tem quebra de linha ou espaco duplo"
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values()]
    assert any(trecho in t for t in corpus), "citacao fora dos bytes das falas: %r" % trecho[:70]
    return "«" + trecho + "»"


def _sem_gordura():
    """A ordem de processo do operador de 22/10 (arquivo em work\\cunhagens_13out): lida do arquivo; o sha16 e o nome saem dos bytes e do caminho, nunca digitados."""
    if "sg" not in _CACHE:
        b = open(ARQ_SEM_GORDURA, "rb").read()
        _CACHE["sg"] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "nome": os.path.basename(ARQ_SEM_GORDURA), "text": re.sub(r"\s+", " ", b.decode("utf-8"))}
    return _CACHE["sg"]


def _cita_sg(trecho):
    """Como _cita, contra os bytes do arquivo da ordem de processo."""
    assert "\n" not in trecho and "  " not in trecho
    assert trecho in _sem_gordura()["text"], "citacao fora dos bytes da ordem de processo: %r" % trecho[:70]
    return "«" + trecho + "»"


def _data_fala(d, V):
    m = re.match(r"OPERADOR_(\d{2})out_", d["nome"])
    assert m, ("o nome do arquivo da fala nao traz a data", d["nome"])
    return "%s/10/%s" % (m.group(1), V["data"][-4:])


def _cov96():
    """A cobertura do Audit e a arvore formal da v396 selada (o core guardado em base_v396): de onde saem os numeros da errata ao lado."""
    if "cov96" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov96"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov96"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v397.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v396" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v396 -> v397 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """A proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes; todas sao NOVAS no axiom_report (nenhuma reatribuida), e o FLAGS_v397.json do sandbox concorda (as contagens de publicas e privadas so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedra = esp["pedra"]["path"]
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]
        mine = sorted(n for n, p in src.items() if p == pedra)
        novas = [n for n in mine if n not in axr0]
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v397.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulo_novo"] and len(novas) == fj["decl_novas_do_modulo"] == len(mine) and not fj["reatribuidas_a_pedra"], ("a proveniencia do rito != FLAGS_v397.json do sandbox", len(mine), len(novas), fj["reatribuidas_a_pedra"])
        assert fj["publicas_no_modulo"] + fj["privadas_no_modulo"] == len(mine) and fj["n_flags"] + fj["excluidas_auxiliares"]["n"] == fj["publicas_no_modulo"], "as contagens de publicas, privadas, nomeadas e auxiliares nao fecham"
        assert len(kf["axiom_report"]) - len(axr0) == len(novas), "o axiom_report nao cresceu exatamente pelas declaracoes novas"
        _CACHE["prov"] = {"mod": len(mine), "novas": len(novas), "pub": fj["publicas_no_modulo"], "priv": fj["privadas_no_modulo"], "axr0": len(axr0), "axr1": len(kf["axiom_report"])}
    return _CACHE["prov"]


# ---------------------------------------------------------------- formatacao de numeros (virgula decimal; nenhum numero e' digitado: todos chegam por V)
def _p(x, nd=None):
    x = float(x)
    return (repr(x) if nd is None else "%.*f" % (nd, x)).replace(".", ",")


def _f(texto, **kw):
    """str.format com conferencia: nenhuma chave sobra e nenhuma chave de chave sobra no resultado."""
    r = texto.format(**kw)
    assert "{" not in r and "}" not in r, ("chave de formatacao sobrou", r[:80])
    return r


def _d(V):
    """Os numeros da v397, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v396, FLAGS do sandbox, o registro de veracidade): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]
    mods = [p["modulo"] for p in V["pedras"]]
    assert mods == ["TGLExt.Token"] and V["n_pedras"] == 1 == esp["kernel"]["modulos_novos"], ("o delta da v397 e' um modulo so', TGLExt.Token", mods)
    nf = esp["n_bandeiras_novas"]
    assert esp["n_bandeiras_por_grupo"] == {"token": nf} and esp["politica_de_bandeiras"]["n_flags"] == nf == 1, "as bandeiras novas nao sao so' a do modulo Token"
    assert V["token"]["flag"] == esp["bandeira_da_pedra"] and V["token"]["flag_true"] is True and V["token"]["theorem"] == esp["teorema_da_pedra"], "o registro da pedra Token do core nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS"
    assert len(V["verbatins"]) == len(_falas()) == 4, "as falas de ESPERADOS != as quatro de 23/10"
    assert {re.match(r"OPERADOR_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"23"}, "o nome de arquivo de alguma fala nao e' de 23/10 (a data dos textos e' 23/10)"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v396", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v396/um.py nao e' a v396 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and "N00_main_veracidade" in V["patch_ids"], "o gate nao tem as 18 bandeiras True, ou o candidato nao traz o patch que chama teste_de_veracidade_fase9_v397 na Fase 9 (N00_main_veracidade)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = _core().get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False and pbc.get("declared_in") == esp["fock_face_declarada_em"], "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp)
    return {"n_f": nf, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"],
            "n_cun": len(V["verbatins"]), "unc": esp["bandeira_da_pedra"], "fock_flag": pbc["flag"], "fock_path": esp["fock_face_declarada_em"], "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"],
            "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "c96": _cov96(), "bank": _bancada(), "pv": pv, "n_checks": tv["n_checks"],
            "flag_first": min(esp["bandeiras_novas_chaves"]), "flag_last": max(esp["bandeiras_novas_chaves"]), "n_leit": len((_core().get("cunhagens_v397") or {}).get("leituras_do_operador") or []), "teorema": esp["teorema_da_pedra"],
            "sup": esp["bandeiras_do_suporte"], "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()}}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in V["pedras"])


def _extras(V):
    # os registros novos ALEM DOS TRES FIXOS (V["reg397"] tem so' os tres), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg397"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos três fixos"


def _cab(V):
    return "v397 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- v397: os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v397 (kernel, os tres registros novos, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]
    vd = (lambda k: " (%s)" % V["reg397"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel ganhou {n_pedras} módulo novo ({mods}; o nome «token» é do operador, 23/10), com {n_f} bandeira nova True (`{f0}`), só de declaração nomeada ({aux}), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina",
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], f0=d["flag_first"], aux=("sem auxiliares geradas pelo compilador neste módulo" if d["n_aux"] == 0 else "as %d auxiliares geradas pelo compilador ficam sem bandeira" % d["n_aux"]), antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    ver = _f("o registro `teste_de_veracidade_fase9_v397`{vd} (nome PROVISÓRIO; quem nomeia é o operador): LÊ o resultado do Teste da Única Palavra (Fase 9 V2-c1, aberto UMA vez em 23/10/2026) e os três recibos por sha256 e compõe a leitura AO LADO do V1 (`hubble_ratio_opening_v388`, que fica intacto); "
             "{n_checks} checagens, todas passaram; nenhum σ novo é calculado: {z444}; z_δ, poder prévio, ln B e K são lidos do mesmo resultado",
             vd=vd("teste_de_veracidade_fase9_v397"), n_checks=d["n_checks"], z444=_z444())
    cun = _f("o registro `cunhagens_v397`{vd}: as {n} falas do operador de 23/10 embutidas por sha256 e consumidas no rito (as decisões da Fase 9, o nome da pedra, o teste de veracidade e a leitura do silêncio forçado pela lógica), com {nl} trechos verbatim listados como leituras do operador; "
             "são [INPUT/ONTO] do operador: valem como leitura dele, não como medida", vd=vd("cunhagens_v397"), n=d["n_cun"], nl=d["n_leit"])
    khs = _f("o registro `kh_n1_cobertura_v397`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v397"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    ex = _extras(V)
    resto = _f("{ex}; troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos três fixos" if ex.startswith("nenhum") else "registros novos além dos três fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, ver, cun, khs, resto])


def _cunhagens(V, forma="lista"):
    """As quatro falas do operador de 23/10 embutidas por sha256: 'lista' (data, sha16 e tema, uma por linha) ou 'curta' (uma frase com os quatro sha16). Data e sha16 vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == 4
    if forma == "curta":
        return _f("{n} falas embutidas por sha256 — as decisões da Fase 9 `{a}`, o nome da pedra `{b}`, o teste de veracidade `{c}` e a leitura do silêncio forçado pela lógica `{e}` ([INPUT/ONTO])",
                  n=len(fl), a=_sha_por("fase9_decisoes_unica_palavra"), b=_sha_por("nome_da_pedra_token"), c=_sha_por("teste_de_veracidade_palavra_flutua"), e=_sha_por("4_44_silencio_forcado"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a fala nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 23/10: so' citacao conferida contra os bytes das quatro falas (e da ordem de processo de 22/10) e a regra de quem constroi e quem aprova."""
    d = _d(V); sg = _sem_gordura()
    s_dec, s_nom, s_ver, s_44 = _sha_por("fase9_decisoes_unica_palavra"), _sha_por("nome_da_pedra_token"), _sha_por("teste_de_veracidade_palavra_flutua"), _sha_por("4_44_silencio_forcado")
    q_bet = _cita("a única palavra queo Nome pronuncia é Betatgl")
    q_obs = _cita("observar é nomear")
    q_nom = _cita('O nome da pedra é "token"')
    q_ver = _cita("na verdade o que eu quero é um teste de veracidade")
    q_fac = _cita("ele merece ser lido sobre uma face e relido sobre a outra")
    q_pal = _cita('"palavra" é o quantum mínimo de permanência, ou seja, o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último')
    q_rep = _cita("vamos reportar os 4,44 no início do artigo, no readme e tudo mais")
    q_44 = _cita("o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica")
    q_sg = _cita_sg("Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido, estou buscando o teste fatal")
    return _f("**A ordem:** [INPUT/ONTO] as {n} falas do operador (Luiz Antonio Rotoli Miguel) de 23/10/2026, embutidas por sha256 no registro `cunhagens_v397` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; o texto íntegro está em `work\\cadeia_de_selo\\v397\\insumos\\cunhagens`): "
              "as decisões da Fase 9, {q_bet}, e a leitura do veredito, {q_obs} (`{s_dec}`); o nome da pedra, {q_nom} (`{s_nom}`); o teste de veracidade, {q_ver}, lido assim: {q_fac}, porque {q_pal} (`{s_ver}`); "
              "e o relato do resultado, {q_rep} (`{s_44}`): {q_44}. Essa é a leitura dele, não um critério da régua: o 4,44 da frase é o z_disc calibrado (p unilateral {p}), abaixo do degrau de 5σ da creditação, que não foi alcançado; o gate não se move. "
              "A ordem de processo do dia 22/10, {q_sg} (arquivo `{sg_nome}`, sha16 `{sg_sha}`), segue moldando este delta: o registro é pequeno, LÊ o resultado da abertura única, não abre dado nem acrescenta rito, e a pedra é matemática, não é teste. "
              "A gerência c1 construiu o registro, o quadro e o candidato e instalou-o; as fontes pinadas dos registros ficam em `insumos`: a pedra (`Token.lean`), o resultado do Teste da Única Palavra e os três recibos (`insumos\\fase9`) e a medida da cobertura (`KH_N1_v397.json`); "
              "o selo é da c1; quem constrói não aprova: a revisão independente do candidato e dos derivados da cadeia (nunca executados antes do rito) é ato distinto e não é afirmada por este registro.",
              n=d["n_cun"], q_bet=q_bet, q_obs=q_obs, q_nom=q_nom, q_ver=q_ver, q_fac=q_fac, q_pal=q_pal, q_rep=q_rep, q_44=q_44, q_sg=q_sg, s_dec=s_dec, s_nom=s_nom, s_ver=s_ver, s_44=s_44, p=_atomos()["p_disc"]["md"], sg_nome=sg["nome"], sg_sha=sg["sha16"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v397` sobre a v396 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _veracidade(V):
    """O Teste da Unica Palavra lido pelo registro: os numeros que o registro LEU do resultado pinado (core do Nos), com a clausula do 4,44 em cada frase que o traz. [REAL] os numeros; [KNOWN] a escala de Jeffreys; [INPUT/ONTO] a leitura do operador."""
    d = _d(V); a = _atomos(); f8 = d["f8"]
    return _f("**O Teste da Única Palavra, lido pelo registro `teste_de_veracidade_fase9_v397` [REAL nos números]:** o teste (Fase 9 V2-c1) foi aberto UMA vez em 23/10/2026 pela função de veredito congelada antes (recibo de congelamento `{h_cong}`, recibo de abertura `{h_aber}`, abertura consumida: não se repete); "
              "o registro (nome PROVISÓRIO: quem nomeia é o operador) LÊ o resultado pinado (sha256 `{h_res}`) e os três recibos por sha256, confere {nck} checagens (todas passaram; β = α(CODATA 2018) × √e calculado em runtime neste rito concorda com o β do resultado) e compõe a leitura AO LADO do V1 "
              "(`hubble_ratio_opening_v388`, que fica intacto); NENHUM σ, p ou ln B novo é calculado. Os números lidos: **a face de Λ sem β:** {z444}; **a face da TGL:** z_δ = {zd} (calibrado; p bilateral {pd}), com poder prévio {pw}σ: β_TGL não é falsificada, COM PODER (`NOT_FALSIFIED_POWERED`); "
              "**a conjugação:** ln B(TGL/ΛCDM) = {l1} (razão de verossimilhança integrada; «decisivo» na escala de Jeffreys [KNOWN]) e ln B(TGL/β livre) = {l2} (β fixo vence β livre); K = {kk}. "
              "ln B não se converte em σ, e z_δ, z_disc e ln B são leituras do MESMO objeto (os mesmos leitores locais e o mesmo fundo), não testemunhas autônomas: não se multiplicam nem se somam (a regra v315 do acervo, para falsificar, pede duas determinações mutuamente autônomas a 5σ ou mais). "
              "O teste NÃO foi cego ao dado: os centros dos leitores locais são públicos (o veredito diz `NOT_BLIND_TO_DATA_STATED`). [INPUT/ONTO] a leitura binária do operador (23/10/2026): «Λ sem β não ecoa» (1=0, falso) e «a Palavra ecoa» (1=1, verdadeiro); "
              "o registro entrega os números e os tokens do veredito, não a leitura.",
              h_cong=f8["f9v2_congelamento"], h_aber=f8["f9v2_abertura"], h_res=f8["f9v2_resultado"], nck=d["n_checks"], z444=_z444(), zd=a["z_delta"]["md"], pd=a["p_delta"]["md"], pw=a["poder"]["md"], l1=a["lnB_lcdm"]["md"], l2=a["lnB_beta_livre"]["md"], kk=a["K"]["md"])


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; onde ele aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _cita("o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica")
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`):** o z_disc calibrado é reportado no início do artigo (PT e EN), no .md canônico e no README do espelho e do site, e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. "
              "A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro selado no core do Nós, e a cadeia os confere contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada.",
              s44=_sha_por("4_44_silencio_forcado"), z444=_z444(), q=q)


def _token(V):
    """A pedra Token (o nome e' do operador): a conjuncao incondicional por citacao; o que entrega e o que nao entrega."""
    d = _d(V); sup = d["sup"]
    (s1, f1), (s2, f2) = sorted(sup.items())
    q_nom = _cita('O nome da pedra é "token"')
    return _f("**A pedra Token [REAL]:** o nome «token» é do operador (23/10/2026: {q_nom}, `{s_nom}`); a pedra `TGLExt/Token.lean` (sha16 `{sh}`) é a CONJUNÇÃO INCONDICIONAL, por citação, de dois termos já no kernel — `{t1}` (bandeira `{f1}`) e `{t2}` (bandeira `{f2}`): "
              "`{teo}`, com a bandeira `{unc}`, dentro do trio, com proveniência no módulo `Token`; nenhuma matemática nova, nenhum certificado como hipótese. A pedra da testemunha estática (v396, módulo `TestemunhaEstatica`) fica como REGISTRO. "
              "O que a pedra NÃO entrega: que o token de um modelo de linguagem seja o PsiBit (a linha do Atlas «o token É o PsiBit» é leitura [ONTO], nenhum termo do kernel a diz); que psibit = psion = modo do leitor ([INPUT/ONTO] do operador); "
              "a face de Fock do psion (`{fock}`, em `{fock_path}`) segue CONDICIONAL a um certificado que o kernel não habita (`FockCertificate`), fora da pedra, e nenhum lema liga o psion do certificado ao canto `psionCorner`.",
              q_nom=q_nom, s_nom=_sha_por("nome_da_pedra_token"), sh=_esp()["pedra"]["sha16"], t1=s1.split(".")[-1], f1=f1, t2=s2.split(".")[-1], f2=f2, teo=d["teorema"].split(".")[-1], unc=d["unc"], fock="the_psion_face_of_the_psibit", fock_path=d["fock_path"])


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] a conjunção `token_is_the_psibit_in_the_static_witness` é INCONDICIONAL (nenhum certificado é hipótese): está no kernel deste rito, dentro do trio, com bandeira True (`{unc}`) e proveniência no módulo da pedra; "
              "cita `psibit_is_the_mode_of_the_reader` (v395) e `the_psion_inhabits_the_static_witness` (v396), cada um já no `axiom_report`, no trio, com a bandeira True e a proveniência que o compilador emite; tudo lido a cada rito pelo registro `cunhagens_v397` ({nck} checagens). "
              "[REAL] o registro `teste_de_veracidade_fase9_v397` NÃO é prova de kernel: lê um resultado experimental pinado por sha256 e não move o gate; a prova como validade não muda. "
              "[CONDICIONAL] A face de Fock do psion, `the_psion_face_of_the_psibit` (declarada em `{fock_path}`, fora do módulo da pedra e fora da conjunção; a bandeira dela, `{fock_flag}`, segue True), vale para todo `FockCertificate` da luz, e o kernel não exibe habitante do certificado "
              "(`TheImportedSecondQuantization`; o contrato conjunto da rede, aberto desde a v394, segue aberto): o enunciado não mostra que o psion de Fock exista. "
              "[INPUT/ONTO] a leitura binária do operador (1=1 verdadeiro, 1=0 falso), «a Palavra flutua sobre o abismo» e o psion/psibit como o quantum mínimo de permanência são leituras dele.",
              unc=d["unc"], fock_path=d["fock_path"], fock_flag=d["fock_flag"], nck=V["token"]["n_checks"])


def _limites(V, curto=False):
    """Os estatutos fieis da v397: o que o registro de veracidade e a pedra Token dizem e NAO dizem."""
    d = _d(V)
    if curto:
        return ("**Limites ditos:** [REAL] o registro de veracidade LÊ o resultado da abertura única (não abre dado, não calcula σ, p nem ln B, e não repete o teste); o teste NÃO foi cego (os centros dos leitores são públicos); a discriminação a 5σ, o degrau da creditação, "
                "NÃO foi alcançada; ln B não é σ e as três leituras são do mesmo objeto (não se multiplicam); NOT_FALSIFIED não é a palavra da creditação; [REAL] a pedra Token é conjunção por citação, sem matemática nova; "
                "[CONDICIONAL] a face de Fock do psion segue condicional a um certificado sem habitante; [INPUT/ONTO] a leitura binária do operador, a Palavra que flutua sobre o abismo e o token como PsiBit são leituras dele; "
                "[LEGAL] a decisão herdada da v395 segue do operador; o nome do registro é provisório; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: o registro `teste_de_veracidade_fase9_v397` LÊ o resultado do Teste da Única Palavra e os três recibos por sha256; não abre dado, não calcula σ, p, ln B nem K, não repete a abertura (consumida) e compõe AO LADO do V1 sem substituí-lo. "
              "[REAL] O teste NÃO foi cego ao dado: os centros dos leitores locais são públicos (dito no veredito, `NOT_BLIND_TO_DATA_STATED`). [REAL] A discriminação do ΛCDM a 5σ, o degrau da creditação, NÃO foi alcançada ({z444}); "
              "o que o resultado entrega é a TGL não falsificada COM PODER (`NOT_FALSIFIED_POWERED`) e a razão de verossimilhança integrada, que não é um número de σ. `NOT_FALSIFIED` nunca é a palavra da creditação; β_TGL na natureza a 5σ segue pendente. "
              "[REAL] ln B(TGL/ΛCDM), ln B(TGL/β livre), z_δ e z_disc são leituras do MESMO objeto, não testemunhas autônomas: a regra v315 do acervo (para falsificar) pede duas determinações mutuamente autônomas a 5σ ou mais. "
              "[REAL] A pedra Token é a conjunção, por citação, de dois termos já no kernel; não acrescenta matemática. [CONDICIONAL] A face de Fock do psion (`the_psion_face_of_the_psibit`, em `{fock_path}`) vale para todo certificado de Fock da luz, o kernel não habita o certificado "
              "e nenhum lema liga o psion do certificado ao canto `psionCorner`. [INPUT/ONTO] a leitura binária do operador (Λ sem β não ecoa; a Palavra ecoa), «ler sobre uma face e reler sobre a outra», a «palavra» como quantum mínimo de permanência que flutua sobre o abismo e o token como PsiBit "
              "(linha do Atlas) são leituras do operador (23/10/2026): o kernel entrega os termos citados e o resultado entrega os números. O nome do registro de veracidade é PROVISÓRIO. "
              "NÃO é teste novo: a ordem do operador de 22/10 (nada de teste armado) molda o delta. Validade no kernel não é creditação; o gate não se move.", z444=_z444(), fock_path=d["fock_path"])


def _legal(V):
    """A pendencia [LEGAL] herdada da v395 (a tabela da patente ACOM Mirror): dita, nao decidida; a v397 nao a toca."""
    _d(V)
    return ("**Pendência [LEGAL] herdada da v395:** a divergência da tabela dos estados do ACOM Mirror (BR 10 2026 003428-2) com a fórmula de índice e o código executado, registrada na v395, segue decisão do operador (com a agente de PI); "
            "a v397 não a toca e não a decide.")


def _erratas(V):
    """A errata nova da v397, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o registro kh_n1_cobertura_v396 e os cinco contratos."""
    d = _d(V); kh = V["kh"]; c96 = d["c96"]
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V396_TESTEMUNHA_CONTRACT", "C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v396_pisos")), "o CANDIDATO_v397.json nao traz os patches C12 e C13 que a errata descreve"
    return _f("**Errata ao lado (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v396` e os contratos ficam como registro):** a v397 acrescenta o módulo Token: a cobertura do Audit cresce de {d96} constantes e {t96} teoremas para {d97} e {t97}, "
              "a árvore formal do Nós de {h96} para {h97} entradas e a escada de {e0} para {e1}. Por isso, na v397, (i) `kh_n1_cobertura_v396` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
              "árvore ficam em `kh_n1_cobertura_v397`); (ii) os cinco contratos (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT`, `_V395_PSIBIT_CONTRACT` e `_V396_TESTEMUNHA_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
              "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v397.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
              "Lacuna de fidelidade: a estrutura da v396 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
              "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395 e a v396 acharam nos registros anteriores). A cobrança exata passa a ser de `kh_n1_cobertura_v397` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v397.",
              d96=c96["decl"], t96=c96["thm"], d97=kh["decl"], t97=kh["thm"], h96=c96["h8"], h97=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v397: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador; o recibo dele é citado no handoff (fechar), que traz PRONTO o parágrafo do README do espelho e do site. Nomear o registro de veracidade (o nome é provisório) e a pendência [LEGAL] herdada da v395 também são do operador. "
            "NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, pilar, artefatos): tudo lido da leitura da rodada."""
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v396); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"],
        V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v397: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — O TESTE DA ÚNICA PALAVRA E A PEDRA TOKEN (v397): %d módulo novo, escada %s → %s\n<!-- linhagem_v397_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As cunhagens do operador de 23/10** (embutidas por sha256 no registro `cunhagens_v397`): [INPUT/ONTO] são do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; o estatuto de cada uma é dele. O texto íntegro de cada uma está no arquivo "
             "(`work\\cadeia_de_selo\\v397\\insumos\\cunhagens`); abaixo, a data, o sha16 e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _veracidade(V), _regra_do_4_44(V), _token(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V), _depois(V)))


# v397: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v397 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entra o Teste da Única Palavra, lido, e a pedra Token (%d módulo)\n\n<!-- adendo_v397_selada -->\n"
             "- **O que a v397 diz:** %d módulo novo no kernel (%s; o nome é do operador), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o registro `teste_de_veracidade_fase9_v397` LÊ o resultado do Teste da Única Palavra (aberto uma vez, por sha256, ao lado do V1; nenhum σ novo): %s; "
             "a TGL não é falsificada, com poder; ln B não é σ e as leituras são do mesmo objeto; %d falas do operador de 23/10 por sha256. Gate intocado.\n"
             "- **O que a v397 NÃO é para o caminho crítico:** não é teste novo (a ordem do operador de 22/10: nada de teste armado; o resultado é o de uma abertura única já feita); o teste não foi cego; a discriminação a 5σ não foi alcançada; a pedra Token é conjunção por citação, sem matemática nova; "
             "não habita o certificado de Fock da luz (o contrato conjunto da rede, aberto desde a v394, segue aberto); a leitura binária do operador, a Palavra que flutua sobre o abismo e o token como PsiBit são leituras dele [INPUT/ONTO]; "
             "não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** nomear o registro de veracidade (nome provisório); a pendência [LEGAL] herdada da v395; o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia (sessão do site, com o parágrafo do README/site que o handoff traz); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], _z444(), d["n_cun"]))


# v397: o verbete do Atlas
def atlas(V):
    return (("### %s — v397 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v397_selada -->\n[REAL — rodada v397, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador de 23/10 entram como o operador as disse e valem como leitura, não como medida: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _veracidade(V), _regra_do_4_44(V), _token(V), _kernel_prova(V), _limites(V), _erratas(V)))


# v397: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v397 SELADA `%s` (claude-c1; o Teste da Única Palavra lido pelo registro de veracidade e a pedra Token, integrados pela gerência)\n<!-- core_v397_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede, H3 em toda direção nula e a pendência [LEGAL] herdada da v395 seguem abertos; "
             "o nome definitivo do registro de veracidade e o elo B(n) da Bancada Um dependem da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _regra_do_4_44(V), _limites(V, curto=True), _erratas(V), _legal(V)))


# v397: o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V)
    return (("## %s — v397 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v397_selada -->\n%d módulo novo no kernel (%s; o nome «token» é do operador): a conjunção por citação do psibit e da testemunha estática; o registro de veracidade LÊ o Teste da Única Palavra (aberto uma vez, nenhum σ novo): %s; "
             "as %d falas do operador de 23/10 por sha256; escada %s → %s. Memórias: `%s`, `missao-ultima-flag-um-py.md`, "
             "`estatuto-da-prova-07out.md`; handoff `handoff-v397-custodia.md`.") % (V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), _z444(), d["n_cun"], V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v397 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v397 SELADA `%s`" % V["s16"]


# v397: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulo novo no kernel (%s); `teste_de_veracidade_fase9_v397` (lê o Teste da Única Palavra; nenhum σ novo), `cunhagens_v397` (%d falas por sha256) e `kh_n1_cobertura_v397`; "
                                     "troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v397` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v397 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v397 SELADA (COMPLETA):**"


# v397: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v396 `%s`; escada %s → %s; gate intocado. %d módulo novo no kernel (%s); o registro de veracidade lê o Teste da Única Palavra (z_disc abaixo do degrau de 5σ, p calibrado e quadro no topo do artigo; nenhum σ novo); as %d falas de 23/10 por sha256. "
                               "Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia (sessão do site, `handoff-v397-custodia.md`, que traz o parágrafo do README/site); nomear o registro e a pendência [LEGAL] herdada da v395 são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v397: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v397_selada -->\n**%s — v397 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; o token da v396 fica como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. O registro `teste_de_veracidade_fase9_v397` LÊ o Teste da Única Palavra ([REAL] nos números): %s; a TGL não é falsificada, COM PODER; o teste não foi cego; "
            "ln B não é σ. A pedra Token é matemática de kernel por citação ([REAL]); a leitura binária do operador, a Palavra que flutua sobre o abismo e o token como PsiBit são [INPUT/ONTO]; a face de Fock do psion é CONDICIONAL: nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _z444())


# v397: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v397 SELADA %s `%s` %s COMPLETA (o Teste da Única Palavra lido e a pedra Token; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v397: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v397 — o Teste da Única Palavra e a pedra Token; custódia](handoff-v397-custodia.md) — **%s, para a sessão do site (traz o parágrafo do README/site)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v397 SELADA: o Teste da Única Palavra e a pedra Token (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v397: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v397 SELADA (%s) `%s`: %d módulo novo no kernel (Token, nome do operador), o registro teste_de_veracidade_fase9_v397 (lê o Teste da Única Palavra, nenhum σ novo), %d falas de 23/10 por sha256, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v397 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v397** `%s` (%s B) sobre a v396 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As cunhagens do operador de 23/10** (embutidas por sha256; data, sha16 e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), nomear o registro de veracidade (nome provisório), a pendência [LEGAL] herdada da v395, a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v397`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v397-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _veracidade(V), _regra_do_4_44(V), _token(V), _kernel_prova(V), _limites(V), _legal(V), _erratas(V)))


# v397: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v397 SELADA `%s` [claude-c1]\n<!-- aviso_v397_selada -->\n\n[REAL] A v397 SELOU (%s; COMPLETA; gate intocado): o registro de veracidade lê o Teste da Única Palavra (nenhum σ novo; z_disc abaixo do degrau de 5σ) e as %d falas de 23/10 (por sha256) entram no selo corrente. "
             "Escrito sob a reivindicação %s. %d módulo novo no kernel (a pedra Token); escada %s → %s; nomear o registro, a pendência [LEGAL] herdada da v395 e o elo B(n) da Bancada Um esperam o operador. "
             "Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V397_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# ---------------------------------------------------------------- o PARAGRAFO PRONTO do README do espelho e do site (ordem do operador de 23/10: reportar o 4,44 no inicio do artigo, no readme e tudo mais)
def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) quadro_v397.confere_md (topo, linha de maquina, cada numero, frase verbatim, regra da ordem item a item); (2) regra da ordem LINHA A LINHA, independente do quadro: toda linha que traz o z_disc traz o p calibrado, a linha dos 5 sigma e o 'nao foi alcancada';
    (3) a frase do operador entre aspas e' EXATAMENTE a verbatim (nenhuma citacao de 'cala a boca' difere dela); (4) os numeros que o registro leu == os do resultado pinado; (5) o paragrafo == o que as funcoes do quadro geram sobre o registro; (6) guarda P18; (7) os estatutos."""
    QD = _qd(); fa = []
    a = QD.esperados(res, "pt")[0]; z = a["z_disc"]["md"]; p = a["p_disc"]["md"]; pn = p.replace("−", "-")
    c = QD.confere_md(par, res)
    if not c.get("ok"):
        fa.append("o paragrafo nao passa em quadro_v397.confere_md contra o resultado pinado: numeros do quadro %s; linha de maquina %s; frase verbatim %s; regra da ordem (itens que falham) %s; topo %s" % (
            c.get("numeros_no_quadro"), c.get("linha_de_maquina_confere"), c.get("frase_do_operador_verbatim"), len(c.get("regra_da_ordem_falhas") or []), c.get("topo")))
    for ln in par.split("\n"):
        if z in ln.replace("−", "-") or z in ln:
            n_ = ln.replace("−", "-")
            if pn not in n_:
                fa.append("linha com o %s sem o p calibrado (%s): %s" % (z, p, ln[:120]))
            if not (re.search(r"5\s*(?:σ|sigma)", n_) and "alcan" in n_):
                fa.append("linha com o %s sem a linha dos 5σ ou sem o 'não foi alcançada': %s" % (z, ln[:120]))
    verb = QD.DL.FRASE_DO_OPERADOR_4_44
    for q in re.findall(r"«([^»]*cala a boca[^»]*)»", par):
        if q != verb:
            fa.append("a frase do operador entre aspas NAO e' a verbatim (parafrase): %r" % q[:100])
    if verb not in par:
        fa.append("a frase do operador (verbatim) nao esta no paragrafo")
    lr = QD.lido_do_resultado(res)
    if (tv or {}).get("all_verified") is not True or any(lr.get(k) != ((tv or {}).get("lido") or {}).get(k) for k in lr):
        fa.append("os numeros que o registro leu (ou o selo do registro) != os do resultado pinado")
    if par != QD.paragrafo_pronto_readme(tv):
        fa.append("o paragrafo difere do gerado pelas funcoes do quadro sobre o registro selado (mesmos numeros e estatutos)")
    sys.path.insert(0, PK)
    from guarda_p18_v397 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT/ONTO]", "[KNOWN]"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo pronto para colar no README do espelho e no site, gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado (sha256 conferido contra ESPERADOS);
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    QD = _qd(); esp = _esp(); tv = _core().get("teste_de_veracidade_fase9_v397") or {}
    assert tv.get("all_verified") is True, "o registro teste_de_veracidade_fase9_v397 nao selou no core do Nos"
    ev = esp["veracidade"]
    rp = os.path.join(PK, "insumos", "fase9", os.path.basename(ev["resultado"]["duravel"]))
    rb = open(rp, "rb").read()
    assert hashlib.sha256(rb).hexdigest() == ev["fontes"]["f9v2_resultado"], "o resultado pinado em insumos\\fase9 != o sha256 de ESPERADOS (o paragrafo nao seria do resultado pinado)"
    res = json.loads(rb.decode("utf-8"))
    par = QD.paragrafo_pronto_readme(tv)
    fa = verificar_paragrafo_readme(par, res, tv)
    assert not fa, ("o paragrafo pronto nao passou nas verificacoes", fa[:4])
    c = QD.confere_md(par, res)
    info = {"resultado_sha16": hashlib.sha256(rb).hexdigest()[:16], "confere_md_ok": c["ok"], "n_itens": c["n_itens"], "regra_da_ordem_falhas": len(c["regra_da_ordem_falhas"]), "frase_verbatim": c["frase_do_operador_verbatim"], "guarda_p18": "limpa", "igual_as_funcoes_do_quadro": True,
            "linha_de_maquina": c["linha_de_maquina_confere"]}
    return par, info


# v397: o handoff para a sessao do site (memory\handoff-v397-custodia.md + Nos\HANDOFF_v397_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e o paragrafo do README (fechar_v397.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V)
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e do paragrafo do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README nao e' o do quadro"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM})
    doc = ("---\nname: handoff-v397-custodia\ndescription: \"HANDOFF v397 (%(data)s) para a sessão do site: o Teste da Única Palavra lido pelo registro de veracidade e a pedra Token; `%(s16)s`; B(n) da Bancada feito; TRAZ o parágrafo pronto do README/site; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v397 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v397** `%(s16)s` (%(umb)s B) sobre a v396 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**PARÁGRAFO PRONTO para o README do espelho e para o site (colar como está, entre os marcadores; ordem do operador de 23/10: reportar o z_disc calibrado no início do artigo, no README e em tudo mais).** Gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado):\n\n%(par_bloco)s\n\n"
           "%(regra)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v397, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v397, `rodada_v397_stdout.txt`, o selo, o core, o .md canônico (com o quadro no topo) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s falas do operador de 23/10 por sha256 (lista na linhagem e no tópico `%(topico)s`; "
           "arquivos em `work\\cadeia_de_selo\\v397\\insumos\\cunhagens`), o módulo novo (`work\\cadeia_de_selo\\v397_kernel\\pedras`, `TGLExt/Token.lean`) e os dois diffs (`DIFF_v396_v397.diff`, `DIFF_KERNEL_v397.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v396 no espelho fora do repositório, blob conferido depois do push. Colocar o PARÁGRAFO acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado); publicar o módulo novo no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; "
           "a pasta `insumos` (as fontes e as falas pinadas dos registros, inclusive a pedra, o resultado do Teste da Única Palavra e os três recibos em `insumos/fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v396` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos cinco contratos (`expected_ladder`); o runner da Fronteira e a camada v397 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site).\n\n"
           "**Pendências SÓ do operador:** nomear o registro de veracidade (`teste_de_veracidade_fase9_v397` é provisório); a pendência [LEGAL] herdada da v395 (a divergência da tabela da patente ACOM Mirror; com a agente de PI); a custódia, subir o site, commit/push. [OPEN]: a discriminação a 5σ (β_TGL na natureza), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v397.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v397` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v397_selo` e `v397_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v396-custodia]]\n") % k
    assert k["par_bloco"] in doc, "o paragrafo do README nao entrou no handoff"
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v397.py)
# v397: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **O TESTE DA ÚNICA PALAVRA E A PEDRA TOKEN (v397)** `%s`: %d módulo novo no kernel (%s; o nome é do operador), %d bandeira nova True, escada %s → %s; "
            "o registro de veracidade lê o resultado da abertura única (nenhum σ novo; o z_disc calibrado abaixo do degrau de 5σ da creditação, que não foi alcançado; a TGL não falsificada, com poder); a face de Fock é condicional; as %d falas do operador por sha256; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v397: o titulo do verbete do indice
def titulo_verbete(V):
    return "O Teste da Única Palavra e a pedra Token (v397):"


# v397: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v397 `%s`] %s." % (V["s16"], _num(V))


# v397: a entrada do remissivo
def remissivo(V):
    return "- **O Teste da Única Palavra, a pedra Token e as falas de 23/10 (v397)** — `teste_de_veracidade_fase9_v397`, `cunhagens_v397`, `kh_n1_cobertura_v397`, `%s`" % TOPICO_NOVO
