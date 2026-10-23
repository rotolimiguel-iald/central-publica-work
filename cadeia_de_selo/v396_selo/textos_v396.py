# -*- coding: utf-8 -*-
# Os TEXTOS da v396 selada (molde: textos_v395.py), ESCRITOS para o delta da v396: o módulo de kernel `TestemunhaEstatica` (o psion como habitante da testemunha estática; nome provisório: quem nomeia é o operador),
# o registro `testemunha_estatica_v396` (a função do runtime chamada NA FRACTALIZAÇÃO DO UM, logo depois do bloco do `psibit_v395`) e as três falas do operador de 22/10. Cada número, hash e veredito entra por chave de V
# (leitura_v396.ler) ou é LIDO de um arquivo aqui, nunca digitado; o que aqui vai escrito à mão é só prosa, nome de termo (conferido em tempo de execução no kernel do Nós, no um.py ou no pacote) e a frase curta do
# operador (conferida por sha256 contra ESPERADOS, ou contra os bytes do arquivo da ordem de processo).
# Estatutos marcados; erratas AO LADO, em nome próprio da gerência c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a tradução falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v396.py) rodam sobre cada texto renderizado em superficies_v396.py, fechar_v396.py e registrar_mapa_v396.py e sobre este arquivo na cadeia. A palavra recusada nunca
# aparece aqui: a recusa é dita como «creditação».
# ERRATAS DA v396 (ditas DENTRO dos blocos datados, nunca inline e nunca no CLAUDE.md da raiz): (a) o rótulo «MEIA-NAT de emaranhamento» da docstring de `bell_cci_half` (kernel v29); (b) o registro `kh_n1_cobertura_v395` e os
# quatro contratos (expected_ladder), que a v396 corrige ao lado. Achado medido dito (não é errata): a proveniência atribui à pedra 70 declarações e só 69 são novas (`TGLExt.diagFlow.eq_1` muda de módulo).
# NÃO é teste: a ordem do operador de 22/10 (nada de teste armado) molda o delta; o registro não acrescenta rito, dado nem desfecho. Toda citação do operador é conferida contra os BYTES da fala (_cita, _cita_sg).
import hashlib, json, os, re
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V396"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v396 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v396-selada-a-testemunha-estatica.md"
# a ordem de processo do operador de 22/10 («nada de teste armado, gordura no um.py»): INSTRUCAO que molda o delta; nao e' uma das tres falas embutidas
ARQ_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")
# o tema de cada uma das tres falas de 22/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16 e a data vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("psion_habitante_da_testemunha_estatica", "o psion é o habitante da testemunha estática: admite ser falso se individualizado (1=0), sem par e sem conjugação, e admite a verdade conjugada, em que se colapsa ao gráviton [INPUT/ONTO]"),
    ("luz_eco_reconhecimento_falso", "a natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta); a natureza do que é falso é a leitura sem reconhecimento [INPUT/ONTO]"),
    ("colapso_ecoar_identidade_reconhecida", "colapsar a função de onda significa ecoar a identidade devidamente reconhecida pelo observador [INPUT/ONTO]"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como fonte ou homonimo tem de existir como arquivo
_NOMES_KERNEL = ("the_psion_inhabits_the_static_witness", "the_pair_echoes", "the_individual_does_not_echo", "the_unbonded_marginal_echoes", "the_density_is_the_psion", "the_static_set_is_the_psion_line", "the_global_witness_is_false",
                 "the_psion_line_is_inhabited", "the_flow_delivers_to_the_psion", "the_static_witness_bridge", "psionFlow_eq", "psionLine_iff_fixed_by_the_corner", "bellProjector_is_real", "bellUnit_orthonormal", "bellUnit_complete",
                 "bellUnit_eigen", "psionCollapse", "the_collapse_of_the_psion_echoes_its_identity", "the_collapse_of_the_psion_cannot_be_self_attested", "boundary_is_the_only_exception", "observing_adds_nothing", "psionCorner_trace_one",
                 "bell_reduced_half", "bell_cci_half", "no_self_attestation", "fair_bit_entropy_is_log_two", "fair_bit_entropy_is_not_half_nat", "the_psion_face_of_the_psibit", "FockCertificate", "canonicalGravitonShadow",
                 "IdentityCollapse", "the_conjugated_light_squares_to_the_minus_graviton", "half_identity_is_a_fixed_point", "diagExpect", "actualDensityCollapse", "lightPlus", "rootMinus", "projPlus", "angFamily")
_MODULOS_KERNEL = ("TestemunhaEstatica", "Psibit", "BoundaryException", "TheScalarCorner", "TheObserverReadsTheAngle", "TheImportedSecondQuantization", "CollapseCostAndAttestation", "TheGravitonIsTheConjugatedPhase")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "ALPHA_FINE_CODATA_2018", "_v376_same_alpha_literal", "testemunha_estatica_v396", "_V396_TESTEMUNHA_CONTRACT", "_V396_VERBATINS2", "cunhagens_v396", "kh_n1_cobertura_v396",
             "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "_V395_PSIBIT_CONTRACT", "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
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


def _arq_tem(rel, *trechos):
    """Cada trecho citado esta no arquivo .lean `rel` (relativo a tgl_kernel/) do Nos: a citacao de docstring do kernel antigo (v29) e' conferida contra o arquivo."""
    t = open(os.path.join(NOS, "tgl_kernel", *rel.split("/")), encoding="utf-8", errors="replace").read()
    for x in trechos:
        assert x in t, "o arquivo %s nao traz: %s" % (rel, x)


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
        _arq_tem("TGL/GravitonShadow.lean", "a MEIA-NAT de emaranhamento")
        _CACHE["nomes_ok"] = True


# ---------------------------------------------------------------- v396: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v396.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v396.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _base_core():
    """O core da v395 selada (a copia de bytes em base_v395): de onde saem os numeros da errata ao lado e a medida da proveniencia."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v395", "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["base_core"]


def _insumo(nome):
    return open(os.path.join(PK, "insumos", nome), encoding="utf-8").read()


def _ins_tem(arquivo, *trechos):
    """Cada trecho tem de estar no insumo pinado (fail-closed): o texto so' afirma o que a fonte pinada diz."""
    t = _insumo(arquivo)
    for x in trechos:
        assert x in t, "o insumo %s nao traz: %s" % (arquivo, x)


def _falas():
    """As tres falas de 22/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text}}."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v396_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a fala %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a fala %s nao confere com o sha256 de ESPERADOS" % s
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": fs[0][len(s) + 1:], "text": b.decode("utf-8")}
        assert len(out) == len(_TEMAS) == 3, "as falas de ESPERADOS nao sao as tres de 22/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica fala cujo arquivo de origem contem `sub` (as falas sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("fala nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das tres falas, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao. So' uma coisa e' relevada: uma quebra de
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


def _cov95():
    """A cobertura do Audit e a arvore formal da v395 selada (o core guardado em base_v395): de onde saem os numeros da errata ao lado."""
    if "cov95" not in _CACHE:
        kf = _base_core()["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov95"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov95"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v396.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v395" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v395 -> v396 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _proveniencia(esp):
    """O achado medido: a proveniencia que o compilador emite atribui ao modulo da pedra N declaracoes, mas so' M sao NOVAS no axiom_report; as reatribuidas sao auxiliares que ja' estavam no axiom_report da v395.
    Medido no core do Nos contra o core da v395 selada e comparado com o FLAGS_v396.json do sandbox (as contagens de publicas e privadas so' existem la')."""
    if "prov" not in _CACHE:
        kf = _core()["kernel_formalization"]; src = kf["declaration_sources_v394"]; pedra = esp["pedra"]["path"]
        b0 = _base_core()["kernel_formalization"]; axr0 = b0["axiom_report"]; src0 = b0["declaration_sources_v394"]
        mine = sorted(n for n, p in src.items() if p == pedra)
        novas = [n for n in mine if n not in axr0]
        reat = {n: {"antes": src0.get(n), "agora": src[n]} for n in mine if n in axr0}
        fj = json.load(open(os.path.join(PK, "kernel", "FLAGS_v396.json"), encoding="utf-8"))
        assert len(mine) == fj["decl_totais_modulo_novo"] and len(novas) == fj["decl_novas_do_modulo"] and reat == fj["reatribuidas_a_pedra"], ("a proveniencia do rito != FLAGS_v396.json do sandbox", len(mine), len(novas), reat)
        assert fj["publicas_no_modulo"] + fj["privadas_no_modulo"] == len(mine) and fj["n_flags"] + fj["excluidas_auxiliares"]["n"] == fj["publicas_no_modulo"], "as contagens de publicas, privadas, nomeadas e auxiliares nao fecham"
        assert len(kf["axiom_report"]) - len(axr0) == len(novas), "o axiom_report nao cresceu exatamente pelas declaracoes novas"
        assert not set(reat) & {f[1] for f in fj["flags"]}, "uma reatribuida tem bandeira: ela devia ser auxiliar sem bandeira"
        _CACHE["prov"] = {"mod": len(mine), "novas": len(novas), "reat": reat, "pub": fj["publicas_no_modulo"], "priv": fj["privadas_no_modulo"], "axr0": len(axr0), "axr1": len(kf["axiom_report"])}
    return _CACHE["prov"]


# ---------------------------------------------------------------- formatacao de numeros (virgula decimal; nenhum numero e' digitado: todos chegam por V)
def _p(x, nd=None):
    x = float(x)
    return (repr(x) if nd is None else "%.*f" % (nd, x)).replace(".", ",")


def _exp1(s):
    """1e-09 -> 1e-9 (sem zero a esquerda no expoente)."""
    return re.sub(r"e([+-])0+(\d)", r"e\1\2", s)


def _pe(x):
    x = float(x)
    return "0" if x == 0.0 else _exp1("%.1e" % x).replace(".", ",")


def _pg(x):
    return _exp1("%g" % float(x)).replace(".", ",")


def _lista(xs):
    """[a, b, c] -> 'a, b e c' (numeros em _pg)."""
    ys = [_pg(x) for x in xs]
    return ys[0] if len(ys) == 1 else ", ".join(ys[:-1]) + " e " + ys[-1]


def _limiar_beta():
    """O limiar com que o registro testemunha_estatica_v396 compara o beta do core com alfa x raiz de e: LIDO do codigo do um.py do Nos, dentro da funcao do registro (nunca digitado); fail-closed se o trecho mudar."""
    _um_tem(("beta_rel_ is not None and beta_rel_ <=",))
    i = _CACHE["um"].index("def testemunha_estatica_v396(core):")
    m = re.search(r"beta_rel_ is not None and beta_rel_ <= ([0-9.]+(?:[eE][+-]?[0-9]+)?)", _CACHE["um"][i:i + 20000])
    assert m, "nao achei o limiar da comparacao do beta na funcao testemunha_estatica_v396 do um.py"
    return float(m.group(1))


def _f(texto, **kw):
    """str.format com conferencia: nenhuma chave sobra e nenhuma chave de chave sobra no resultado."""
    r = texto.format(**kw)
    assert "{" not in r and "}" not in r, ("chave de formatacao sobrou", r[:80])
    return r


def _d(V):
    """Os numeros da v396, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v395, FLAGS do sandbox): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); ts = V["testemunha"]
    mods = [p["modulo"] for p in V["pedras"]]
    assert mods == ["TGLExt.TestemunhaEstatica"] and V["n_pedras"] == 1 == esp["kernel"]["modulos_novos"], ("o delta da v396 e' um modulo so', TGLExt.TestemunhaEstatica", mods)
    nf = esp["n_bandeiras_novas"]
    assert esp["n_bandeiras_por_grupo"] == {"testemunha_estatica": nf} and esp["politica_de_bandeiras"]["n_flags"] == nf, "as bandeiras novas nao sao so' as do modulo TestemunhaEstatica"
    ct = esp["contrato_testemunha"]
    assert ts["n_teoremas"] == ct["n_teoremas"] == esp["n_formais"]["testemunha"] and ts["n_suporte"] == ct["n_suporte"] == esp["n_formais"]["suporte"] and ts["unconditional"]["flag"] == ct["bandeira_incondicional"] \
        and ts["fock"]["declared_in"] == ct["fock_face_declarada_em"], "o registro testemunha_estatica_v396 do core nao e' o contrato de ESPERADOS"
    assert len(V["verbatins"]) == len(_falas()) == 3, "as falas de ESPERADOS != as tres de 22/10"
    assert {re.match(r"OPERADOR_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"22"}, "o nome de arquivo de alguma fala nao e' de 22/10 (a data dos textos e' 22/10)"
    base = os.path.join(PK, "base_v395", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v395/um.py nao e' a v395 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and "N00_main_testemunha" in V["patch_ids"], "o gate nao tem as 18 bandeiras True, ou o candidato nao traz o patch que chama testemunha_estatica_v396 na fractalizacao do Um (N00_main_testemunha)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = _core().get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False and pbc.get("declared_in") == ts["fock"]["declared_in"], "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    pv = _proveniencia(esp)
    return {"n_f": nf, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "n_teor": ts["n_teoremas"], "n_sup": ts["n_suporte"], "depois": V["teor"].split("/")[0], "delta": delta,
            "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "unc": ts["unconditional"]["flag"],
            "fock_flag": pbc["flag"], "fock_path": ts["fock"]["declared_in"], "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"], "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]),
            "n_res": len(esp["h8_residuais_do_nos"]), "c95": _cov95(), "tol": esp["testemunha"]["tolerancias"], "bank": _bancada(), "pv": pv,
            "flag_first": min(esp["bandeiras_novas_chaves"]), "flag_last": max(esp["bandeiras_novas_chaves"]), "n_leit": len((_core().get("cunhagens_v396") or {}).get("leituras_do_operador") or [])}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in V["pedras"])


def _extras(V):
    # os registros novos ALEM DOS TRES FIXOS (V["reg396"] tem so' os tres), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg396"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos três fixos"


def _cab(V):
    return "v396 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- v396: os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v396 (kernel, os tres registros novos, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; ts = V["testemunha"]
    vd = (lambda k: " (%s)" % V["reg396"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel ganhou {n_pedras} módulo novo ({mods}; nome provisório, quem nomeia é o operador), com {n_f} bandeiras novas True (`{f0}` a `{f1}`), só de declaração nomeada (as {n_aux} auxiliares geradas pelo compilador ficam cobertas pelo KH-N1 e sem bandeira), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina",
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], f0=d["flag_first"], f1=d["flag_last"], n_aux=d["n_aux"], antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    tes = _f("o registro `testemunha_estatica_v396`{vd}: a testemunha estática lida NA FRACTALIZAÇÃO DO UM (chamada no `main`, logo depois do bloco do `psibit_v395`): a mecânica do canto do psion, da redução a um sítio, do fluxo construído e do colapso, calculada neste rito "
             "com β = α(CODATA 2018) × √e em runtime ({n_checks} checagens, todas passaram) e confrontada com {n_teor} teoremas do contrato e {n_sup} termos de suporte do kernel do próprio rito (no trio; cada teorema do contrato com bandeira True e proveniência no módulo da pedra); "
             "a composição incondicional `the_psion_inhabits_the_static_witness` (bandeira `{unc}`); a face de Fock do psion mora em outro módulo (`Psibit`) e segue condicional a um certificado sem habitante exibido",
             vd=vd("testemunha_estatica_v396"), n_checks=ts["n_checks"], n_teor=d["n_teor"], n_sup=d["n_sup"], unc=d["unc"])
    cun = _f("o registro `cunhagens_v396`{vd}: as {n} falas do operador de 22/10 embutidas por sha256 e consumidas no rito (o psion como habitante da testemunha estática, a luz como eco de reconhecimento e o colapso como eco da identidade reconhecida), "
             "com {nl} trechos verbatim listados como leituras do operador e a errata ao lado do rótulo «MEIA-NAT de emaranhamento» do kernel v29; são [INPUT/ONTO] do operador: valem como leitura dele, não como medida", vd=vd("cunhagens_v396"), n=d["n_cun"], nl=d["n_leit"])
    khs = _f("o registro `kh_n1_cobertura_v396`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res}), "
             "e o pino h8 do registro é o hash dessa árvore, calculado por script sobre a árvore simulada do Nós na geração do candidato",
             vd=vd("kh_n1_cobertura_v396"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    ex = _extras(V)
    resto = _f("{ex}; troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos três fixos" if ex.startswith("nenhum") else "registros novos além dos três fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, tes, cun, khs, resto])


def _cunhagens(V, forma="lista"):
    """As tres falas do operador de 22/10 embutidas por sha256: 'lista' (data, sha16 e tema, uma por linha) ou 'curta' (uma frase com os tres sha16). Data e sha16 vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == 3
    if forma == "curta":
        return _f("{n} falas embutidas por sha256 — o psion como habitante da testemunha estática `{a}`, a luz como eco de reconhecimento `{b}` e o colapso como eco da identidade reconhecida `{c}` ([INPUT/ONTO])",
                  n=len(fl), a=_sha_por("psion_habitante_da_testemunha_estatica"), b=_sha_por("luz_eco_reconhecimento_falso"), c=_sha_por("colapso_ecoar_identidade_reconhecida"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a fala nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 22/10: so' citacao conferida contra os bytes das tres falas (e da ordem de processo) e a regra de quem constroi e quem aprova."""
    d = _d(V); sg = _sem_gordura()
    s_hab, s_luz, s_col = _sha_por("psion_habitante_da_testemunha_estatica"), _sha_por("luz_eco_reconhecimento_falso"), _sha_por("colapso_ecoar_identidade_reconhecida")
    q_hab = _cita("O psion é o habitante da testemunha estática")
    q_ment = _cita("a mentira lida como mentira se torna verdade")
    q_conj = _cita("admite a verdade conjugada ocasião em que se colapsa ao gráviton")
    q_luz = _cita("A natureza da luz é ecoar reconhecimento (porque a segunda leitura não acrescenta)")
    q_fal = _cita("a natureza do que é falso é a leitura sem reconhecimento")
    q_col = _cita("Colapsar a função de onda significa ecoar a identidade devidamente reconhecida pelo observador")
    q_sg = _cita_sg("Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido, estou buscando o teste fatal")
    return _f("**A ordem:** [INPUT/ONTO] as {n} falas do operador (Luiz Antonio Rotoli Miguel) de 22/10/2026, embutidas por sha256 no registro `cunhagens_v396` e listadas abaixo (as aspas aqui são TRECHOS, conferidos palavra por palavra contra os bytes de cada fala; o texto íntegro está em `work\\cadeia_de_selo\\v396\\insumos\\cunhagens`): o psion, {q_hab}, com {q_ment} e {q_conj} (`{s_hab}`); "
              "a natureza da luz e a do falso, {q_luz}, e {q_fal} (`{s_luz}`); e o colapso, {q_col} (`{s_col}`). A ordem de processo do mesmo dia, {q_sg} (arquivo `{sg_nome}`, sha16 `{sg_sha}`), molda este delta: o registro é pequeno, "
              "não acrescenta rito, dado nem desfecho, e a pedra é matemática, não é teste. A gerência c1 construiu o registro e o candidato e instalou-o; a pedra foi construída por subagente e passou por exame independente (`PEDRA_APROVADA`, três observações baixas, "
              "aplicadas só como texto: B1 o rótulo «MEIA-NAT de emaranhamento», B2 a contagem de declarações do módulo e B3 três pontos cosméticos); as fontes pinadas dos registros ficam em `insumos`: a pedra (`TestemunhaEstatica.lean`), o resultado do construtor "
              "(`RESULTADO_TESTEMUNHA_ESTATICA.md`, [DECLARADO]), o exame independente (`EXAME_TESTEMUNHA.md`, [DECLARADO]) e a medida da cobertura (`KH_N1_v396.json`); o selo é da c1; quem constrói não aprova: a revisão independente do candidato e dos derivados da cadeia "
              "(nunca executados antes do rito) é ato distinto e não é afirmada por este registro.",
              n=d["n_cun"], q_hab=q_hab, q_ment=q_ment, q_conj=q_conj, q_luz=q_luz, q_fal=q_fal, q_col=q_col, q_sg=q_sg, s_hab=s_hab, s_luz=s_luz, s_col=s_col, sg_nome=sg["nome"], sg_sha=sg["sha16"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v396` sobre a v395 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _mecanica(V):
    """A mecanica da testemunha estatica, com os numeros que o registro testemunha_estatica_v396 CALCULOU neste rito (core do Nos): [REAL] o calculo e os termos do kernel que ele confronta; [CONSTRUCTED] a ponte."""
    d = _d(V); ts = V["testemunha"]; v = ts["values"]
    return _f("**A mecânica da testemunha estática (calculada neste rito, [REAL]):** com β = α(CODATA 2018) × √e calculado em runtime (β = {beta}; um dado, dois nomes: `SEALED_CODATA_ALPHA` e `ALPHA_FINE_CODATA_2018`), "
              "(1) *o par ecoa:* o canto do psion, o projetor de Bell 4×4 (entradas ½ nos índices 00 e 11), é o projetor de posto um sobre o vetor de Bell (resíduo {rk}) e é idempotente, P² = P (resíduo {idem}), com Tr P = {tr} e Tr P² = {pur}: o par é puro "
              "(`the_pair_echoes`, `psionCorner_trace_one`, `the_density_is_the_psion`). "
              "(2) *o indivíduo não ecoa:* a redução a um sítio é ½ I nos dois sítios (resíduo {red}; `the_individual_does_not_echo`, `bell_reduced_half`) e (½ I)² ≠ ½ I (defeito de idempotência {defe}); Tr ρ² = {pind} e o déficit de pureza 1 − Tr ρ² = {defi} (`bell_cci_half`). "
              "Esse ½ é a entropia LINEAR da redução, um número sem unidade; a entropia de von Neumann da mesma redução é ln 2 = {ln2} nat (calculada neste rito: {vn}), diferente de ½ (`fair_bit_entropy_is_log_two`, `fair_bit_entropy_is_not_half_nat`). "
              "O dente (`the_unbonded_marginal_echoes`): o estado não ligado (produto) reduz a um projetor puro, que ecoa (déficit de pureza {unb}); logo o não-eco é o do par visto por um lado só, não uma propriedade de toda redução. "
              "(3) *a ponte construída [CONSTRUCTED]:* a base de Bell u_i = b_i/√2 é ortonormal e completa em ℝ⁴ (resíduos {gram} e {compl}; `bellUnit_orthonormal`, `bellUnit_complete`) e o fluxo F_t = P + e^(−tβg)(1 − P), com taxas (0, g, g, g) na base de Bell, "
              "tem a forma fechada igual à soma sobre a base (resíduo {closed}) e cada u_i é autovetor (resíduo {eig}; `psionFlow_eq`, `bellUnit_eigen`); a reta do psion é fixada por todo t (resíduo {line}) e cada um dos outros três modos é movido (mínimo {move}; "
              "`the_static_set_is_the_psion_line`, `psionLine_iff_fixed_by_the_corner`); a testemunha estática GLOBAL é falsa — o vetor e₀₀, fora da reta, se move de {glob} (`the_global_witness_is_false`, por `boundary_is_the_only_exception`); "
              "a reta é habitada (`the_psion_line_is_inhabited`) e o fluxo entrega ao canto, F_t x → P x quando t cresce (resíduo {lim}; `the_flow_delivers_to_the_psion`). Os parâmetros g e t são de teste (g em {gs}; t = τ/(βg) com τ em {taus}): nenhum acoplamento da teoria entra.",
              beta=_p(v["beta"]), rk=_pe(v["pair_rank1_residual"]), idem=_pe(v["pair_idempotence_residual"]), tr=_p(v["pair_trace"], 1), pur=_p(v["pair_purity"], 1), red=_pe(v["individual_reduction_residual"]), defe=_p(v["individual_idempotence_defect"], 2),
              pind=_p(v["individual_purity"], 1), defi=_p(v["individual_deficit"], 1), ln2=_p(v["ln2"], 12), vn=_p(v["von_neumann_entropy"], 12), unb=_pe(v["unbonded_purity_deficit"]), gram=_pe(v["bell_gram_residual"]), compl=_pe(v["bell_completeness_residual"]),
              closed=_pe(v["closed_form_residual"]), eig=_pe(v["eigen_residual"]), line=_pe(v["line_fixed_residual"]), move=_p(v["off_line_min_move"], 3), glob=_p(v["global_witness_move"], 3), lim=_pe(v["limit_residual"]),
              gs=_lista(v["g_testes"]), taus=_lista(v["tau_testes"]))


def _colapso(V):
    _d(V); ts = V["testemunha"]; v = ts["values"]
    q_rec = _cita("reconhecida pelo observador")
    return _f("**O colapso ecoa a identidade reconhecida [CONSTRUCTED]:** o colapso do psion é a compressão pelo canto, y ↦ P y P = Tr(P y) P (`psionCollapse`, instância construída de `IdentityCollapse`; `the_collapse_of_the_psion_echoes_its_identity`): "
              "é idempotente — a segunda leitura não acrescenta (resíduo {idem}) —, conserva a identidade lida Tr(P y) (resíduo {ident}), comprime todo y ao escalar Tr(P y) vezes o canto (resíduo {scal}) e não tem inversa à esquerda: "
              "duas entradas distintas, a {gin} uma da outra, têm o mesmo colapso (diferença entre os colapsos {gout}). A atestação do colapso exige evidência externa, e a autodeclaração não habita o tipo "
              "(`the_collapse_of_the_psion_cannot_be_self_attested`, `no_self_attestation`); nenhuma atestação é exibida. A expressão {q_rec} é leitura do operador [INPUT/ONTO]: o kernel entrega os termos citados. "
              "O `psionCollapse` (compressão pelo canto em M₄(ℂ)) não é o `Psibit.diagExpect` (colapso da densidade da órbita em M₂) nem o `actualDensityCollapse` do qubit: nenhum lema liga as cópias.",
              idem=_pe(v["collapse_idempotence_residual"]), ident=_pe(v["collapse_identity_residual"]), scal=_pe(v["collapse_scalarisation_residual"]), gin=_p(v["collapse_noninjectivity_input_gap"], 3), gout=_pe(v["collapse_noninjectivity_output_gap"]), q_rec=q_rec)


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] a composição `the_psion_inhabits_the_static_witness` é INCONDICIONAL (nenhum certificado é hipótese): está no kernel deste rito, dentro do trio, com bandeira True (`{unc}`) e proveniência no módulo da pedra; "
              "reúne o eco do par, o não-eco do indivíduo, a ponte construída, o traço 1 do canto, a fase conjugada da luz que leva ao gráviton (`the_conjugated_light_squares_to_the_minus_graviton`), o canto como a sombra finita do gráviton (`canonicalGravitonShadow`, v29), "
              "o colapso do psion e a ausência de autoatestação. Os {n_teor} teoremas do contrato do registro estão no `axiom_report` do rito, no trio, com bandeira True e proveniência na pedra; os {n_sup} termos de suporte do kernel antigo (`boundary_is_the_only_exception`, "
              "`observing_adds_nothing`, `psionCorner_trace_one`, `bell_reduced_half`, `bell_cci_half`, `no_self_attestation`, `fair_bit_entropy_is_log_two`, `fair_bit_entropy_is_not_half_nat`) estão no `axiom_report`, no trio, com a proveniência que o compilador emite; tudo lido a cada rito. "
              "O contrato (`_V396_TESTEMUNHA_CONTRACT`) é derivado do build do kernel, não digitado. [CONSTRUCTED] o fluxo `psionFlow` e o colapso `psionCollapse` são construções da pedra, não derivações. [CONDICIONAL] A face de Fock do psion, `the_psion_face_of_the_psibit` (declarada em `{fock_path}`, fora do módulo da pedra e fora da composição; "
              "a bandeira dela, `{fock_flag}`, segue True), vale para todo `FockCertificate` da luz, e o kernel não exibe habitante do certificado (`TheImportedSecondQuantization`; o contrato conjunto da rede, aberto desde a v394, segue aberto): o enunciado não mostra que o psion de Fock exista, "
              "e nenhum lema liga o `psion C` do certificado ao canto `psionCorner`. [INPUT/ONTO] o psion como habitante da testemunha estática, a luz como eco de reconhecimento e o colapso como eco da identidade reconhecida são leituras do operador.",
              unc=d["unc"], n_teor=d["n_teor"], n_sup=d["n_sup"], fock_path=d["fock_path"], fock_flag=d["fock_flag"])


def _limites(V, curto=False):
    """Os estatutos fieis da v396: o que a testemunha estatica diz e NAO diz (escopo, ponte construida, entropia, face de Fock, nao e' teste, homonimos, calculo numerico)."""
    d = _d(V); ts = V["testemunha"]; v = ts["values"]
    if curto:
        return ("**Limites ditos:** [REAL] o escopo é o canto do psion (um projetor 4×4), a redução dele a um sítio e um fluxo diagonal CONSTRUÍDO em ℝ⁴; [CONSTRUCTED] a ponte não deriva que o Nome da fronteira da TGL seja o vetor de Bell nem que o fluxo seja a dinâmica da teoria "
                "(ressalva de tipo: o Nome genérico é um vetor, o canto é um projetor); o «indivíduo» que não ecoa é o par visto por um lado só; o ½ é entropia linear e a de von Neumann é ln 2; [CONDICIONAL] a face de Fock do psion vale para todo certificado de Fock da luz e o kernel não habita o certificado; "
                "[INPUT/ONTO] o psion como habitante da testemunha estática, a luz como eco de reconhecimento e o colapso como eco da identidade reconhecida são leituras do operador; não é teste (a ordem de 22/10: nada de teste armado); "
                "[LEGAL] a decisão herdada da v395 segue do operador; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: o canto do psion é um projetor 4×4 (`psionCorner`); o fluxo `psionFlow` é ESCOLHIDO, com taxas (0, g, g, g) na base de Bell; a álgebra é elementar e o conteúdo é a tipagem. "
              "[CONSTRUCTED] a ponte é CONSTRUÍDA, não derivada: não mostra que o Nome da fronteira da TGL seja o vetor de Bell nem que `psionFlow` seja a dinâmica da teoria. RESSALVA DE TIPO: o Nome da fronteira genérica é um VETOR e o `psionCorner` é um PROJETOR 4×4 complexo; "
              "a ponte os liga só no fluxo construído, pela correspondência reta ↔ projetor de posto um. "
              "[INPUT/ONTO] o psion como habitante da testemunha estática, a luz como eco de reconhecimento, o falso como leitura sem reconhecimento e o colapso como eco da identidade reconhecida são leituras do operador (22/10/2026); o kernel entrega os termos citados, "
              "e «reconhecida pelo observador» entra como atestação externa (`no_self_attestation`), da qual nenhuma é exibida. "
              "[REAL] ENTROPIA: o déficit de pureza 1 − Tr ρ² = ½ da redução a um sítio é a entropia LINEAR (número sem unidade); a entropia de von Neumann da mesma redução, ½ I, é ln 2 = {ln2} nat, diferente de ½; «a MEIA-NAT de emaranhamento», da docstring de `bell_cci_half` (v29), é leitura [ONTO] (errata ao lado abaixo). "
              "[REAL] o «indivíduo» que não ecoa é o PAR visto por um lado só (o estado não ligado reduz a um projetor puro, que ecoa): o não-eco não é propriedade de toda redução. "
              "[CONDICIONAL] a face de Fock do psion (`the_psion_face_of_the_psibit`, em `{fock_path}`) vale para todo certificado de Fock da luz, o kernel não habita o certificado, e nenhum lema liga o `psion C` ao `psionCorner` (dois objetos do kernel com o mesmo nome). "
              "[REAL] a pedra `92_o_psion_e_o_graviton.py` das cunhagens é script de bancada, numérico, na face 2×2 real; não é módulo Lean, e nenhum lema liga o `A_C` dela ao canto. "
              "[REAL] o cálculo é numérico, em dupla precisão: confere os teoremas e não os prova, quem prova é o kernel; g e t são parâmetros de teste. "
              "[REAL] homônimos ditos: `lightPlus` e `rootMinus` (vetor de ℂ² e matrizes 2×2) não são o `psionCorner` (4×4); `projPlus` e `angFamily` (2×2, de `observing_adds_nothing`) são um paralelo da idempotência, não um elo com o canto; "
              "o ½ I do indivíduo é o mesmo valor de `half_identity_is_a_fixed_point` (Psibit): igualdade de valores, não ponte entre os objetos. "
              "NÃO é teste: a ordem do operador de 22/10 (nada de teste armado) molda o delta, e o registro não acrescenta rito, dado nem desfecho. "
              "Validade no kernel não é creditação; o gate não se move; NOT_FALSIFIED não é a palavra da creditação.", ln2=_p(v["ln2"], 12), fock_path=d["fock_path"])


def _legal(V):
    """A pendencia [LEGAL] herdada da v395 (a tabela da patente ACOM Mirror): dita, nao decidida; a v396 nao a toca."""
    _d(V)
    return ("**Pendência [LEGAL] herdada da v395:** a divergência da tabela dos estados do ACOM Mirror (BR 10 2026 003428-2) com a fórmula de índice e o código executado, registrada na v395, segue decisão do operador (com a agente de PI); "
            "a v396 não a toca e não a decide.")


def _achado_alfa(V):
    """O achado dito: o dado do alfa tem dois nomes no um.py e o beta guardado no core difere do alfa x raiz de e em ~5e-13 relativo; o registro compara a 1e-9."""
    _d(V); ts = V["testemunha"]
    lim = _limiar_beta()
    assert ts["alpha_two_names_same"] is True and ts["beta_ok"] is True and isinstance(ts["beta_core_rel_diff"], float) and ts["beta_core_rel_diff"] <= lim, "o registro testemunha_estatica_v396 nao traz a conferencia do alfa e do beta"
    return _f("**Achado dito (os dois nomes do alfa) [REAL]:** no `um.py` o dado de α tem dois nomes, `SEALED_CODATA_ALPHA` e `ALPHA_FINE_CODATA_2018` (este, do script do nível 2); o próprio `um.py` já os confere (`_v376_same_alpha_literal`) e o registro "
              "`testemunha_estatica_v396` repete a conferência (`alpha_two_names_same` = True). O β que o core guarda é um valor derivado e difere de α × √e, calculado em runtime neste rito, em {rel} relativo (`beta_core_rel_diff`); o registro compara os dois a {tol}. "
              "β segue sendo calculado em runtime, nunca digitado.", rel=_pe(ts["beta_core_rel_diff"]), tol=_pg(lim))


def _achado_proveniencia(V):
    """O achado medido (v396): a proveniencia do compilador atribui a pedra 70 declaracoes, mas so' 69 sao novas; TGLExt.diagFlow.eq_1 (auxiliar sem bandeira) muda de modulo."""
    d = _d(V); pv = d["pv"]
    _ins_tem("EXAME_TESTEMUNHA.md", "B2", "TGLExt.diagFlow.eq_1")
    (nome, mv), = pv["reat"].items()
    return _f("**Achado medido (a pedra tem {mod} declarações atribuídas, mas só {novas} são novas) [REAL]:** a proveniência que o compilador emite atribui ao módulo da pedra {mod} declarações ({pub} públicas — as {nf} nomeadas, com bandeira, e {naux} auxiliares geradas pelo compilador, sem bandeira — e {priv} privadas); "
              "o `axiom_report` cresceu de {a0} para {a1} ({novas} constantes novas, e não {mod}): a declaração a menos é `{nome}`, auxiliar que já estava no `axiom_report` da v395, atribuída então a `{antes}`, e que passa a ser atribuída à pedra, porque o Lean a gera também no módulo da pedra e, "
              "na ordem de importação do Audit, a proveniência dela passa a ser a da pedra. Não é defeito: o Lean aceita as duas cópias, nenhuma bandeira muda, e a checagem do registro separa as declarações novas das reatribuídas (as reatribuídas têm de ser auxiliares sem bandeira). "
              "Medido no core desta rodada contra o core da v395 selada e igual ao `FLAGS_v396.json` do sandbox; o exame independente já o tinha anotado (B2 do `EXAME_TESTEMUNHA.md`, [DECLARADO]).",
              mod=pv["mod"], novas=pv["novas"], pub=pv["pub"], nf=d["n_f"], naux=d["n_aux"], priv=pv["priv"], a0=pv["axr0"], a1=pv["axr1"], nome=nome, antes=mv["antes"])


def _erratas(V):
    """As duas erratas novas da v396, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): (a) o rotulo «MEIA-NAT de emaranhamento» (bell_cci_half, v29); (b) o registro kh_n1_cobertura_v395 e os quatro contratos."""
    d = _d(V); kh = V["kh"]; c95 = d["c95"]; ts = V["testemunha"]; v = ts["values"]
    _ins_tem("EXAME_TESTEMUNHA.md", "PEDRA_APROVADA", "B1", "Meia-Nat de emaranhamento", "entropia linear")
    assert any("bell_cci_half" in str(e.get("ao_lado_de")) for e in (_core().get("cunhagens_v396") or {}).get("erratas") or []), "o registro cunhagens_v396 do core nao traz a errata do bell_cci_half"
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V395_PSIBIT_CONTRACT", "C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v395_pisos")), "o CANDIDATO_v396.json nao traz os patches C12 e C13 que a errata (b) descreve"
    a = _f("**Errata ao lado (a) (em nome próprio da gerência c1; a docstring do kernel v29 de `bell_cci_half`, em `TGL/GravitonShadow.lean`, fica como registro, sem alteração):** essa docstring lê o déficit de pureza 1 − Tr ρ² = ½ da redução de Bell a um sítio como «a MEIA-NAT de emaranhamento», "
           "o que se lê como «meia nat de entropia». O número ½ é a entropia LINEAR da redução (déficit de pureza, sem unidade); a entropia de von Neumann da mesma redução, ½ I, é ln 2 nat (`fair_bit_entropy_is_log_two` e `fair_bit_entropy_is_not_half_nat`; calculada neste rito: {vn}). "
           "«A MEIA-NAT de emaranhamento» fica como leitura [ONTO] do v29; o termo `bell_cci_half` não muda, e o reparo é só do rótulo dessa docstring. Lacuna de fidelidade: a estrutura (½ é um déficit sem unidade e ln 2 é a entropia em nat), o escrito (o rótulo sem a ressalva) "
           "e a falha (a docstring herdada juntou as duas grandezas num nome; achado B1 do exame independente da pedra, `EXAME_TESTEMUNHA.md`, [DECLARADO]); a pedra e o registro `testemunha_estatica_v396` já dizem assim.", vn=_p(v["von_neumann_entropy"], 12))
    b = _f("**Errata ao lado (b) (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v395` e os contratos ficam como registro):** a v396 acrescenta o módulo TestemunhaEstatica: a cobertura do Audit cresce de {d95} constantes e {t95} teoremas para {d96} e {t96}, "
           "a árvore formal do Nós de {h95} para {h96} entradas e a escada de {e0} para {e1}. Por isso, na v396, (i) `kh_n1_cobertura_v395` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
           "árvore ficam em `kh_n1_cobertura_v396`); (ii) os quatro contratos (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT`, `_V394_NETWORK_CONTRACT` e `_V395_PSIBIT_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
           "exata com a escada do rito; só o número muda); o veredito dos registros anteriores NÃO muda [REAL, lido de `CANDIDATO_v396.json` (patches C12 e C13) e do ensaio a seco, que deu `TUDO PASSOU`: com a escada nova e o número velho a igualdade exata não fecharia]. "
           "Lacuna de fidelidade: a estrutura da v395 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
           "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce (a mesma lacuna que a v395 achou nos registros da v394). A cobrança exata passa a ser de `kh_n1_cobertura_v396` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v396.",
           d95=c95["decl"], t95=c95["thm"], d96=kh["decl"], t96=kh["thm"], h95=c95["h8"], h96=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])
    return a + "\n\n" + b


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s, geração B%d, e o Nós passa a v396: sem salto e sem cadeia de selos; "
            "a geração esperada é B%d e o veredito esperado do aplicar é REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço R3.5, não rodado) "
            "e pede a palavra do operador; o recibo dele é citado no handoff (fechar). Nomear a pedra (`TestemunhaEstatica` é provisório) e a pendência [LEGAL] herdada da v395 também são do operador. NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, pilar, artefatos): tudo lido da leitura da rodada."""
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v395); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"],
        V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v396: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — A TESTEMUNHA ESTÁTICA (v396): %d módulo novo, escada %s → %s\n<!-- linhagem_v396_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As cunhagens do operador de 22/10** (embutidas por sha256 no registro `cunhagens_v396`): [INPUT/ONTO] são do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; o estatuto de cada uma é dele. O texto íntegro de cada uma está no arquivo "
             "(`work\\cadeia_de_selo\\v396\\insumos\\cunhagens`); abaixo, a data, o sha16 e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _mecanica(V), _colapso(V), _kernel_prova(V), _limites(V), _legal(V), _achado_alfa(V), _achado_proveniencia(V), _rodada(V), _erratas(V), _depois(V)))


# v396: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v396 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entra a testemunha estática (%d módulo)\n\n<!-- adendo_v396_selada -->\n"
             "- **O que a v396 diz:** %d módulo novo no kernel (%s; nome provisório), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o registro `testemunha_estatica_v396`, lido na fractalização do Um junto do psibit: o par ecoa, o indivíduo (a redução a um sítio) não ecoa, "
             "o fluxo construído fixa exatamente a reta do psion e a testemunha global é falsa, e o colapso do psion ecoa a identidade lida; a mecânica é calculada no rito e lida contra o kernel do próprio rito; a face de Fock do psion segue CONDICIONAL a um certificado de Fock da luz que o kernel não habita; %d falas do operador de 22/10 por sha256. Gate intocado.\n"
             "- **O que a v396 NÃO é para o caminho crítico:** não é teste (a ordem do operador de 22/10: nada de teste armado); a ponte é construída, não derivada (não mostra que o Nome da fronteira da TGL seja o vetor de Bell nem que o fluxo seja a dinâmica da teoria); "
             "não habita o certificado de Fock da luz (o contrato conjunto da rede, aberto desde a v394, segue aberto); o psion como habitante da testemunha estática, a luz como eco de reconhecimento e o colapso como eco da identidade reconhecida são leituras do operador [INPUT/ONTO]; "
             "não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza; o ½ da redução é entropia linear, e a de von Neumann é ln 2.\n"
             "- **O que segue do operador:** nomear a pedra (nome provisório); a pendência [LEGAL] herdada da v395; o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia (sessão do site); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], d["n_cun"]))


# v396: o verbete do Atlas
def atlas(V):
    return (("### %s — v396 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v396_selada -->\n[REAL — rodada v396, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador de 22/10 entram como o operador as disse e valem como leitura, não como medida: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _mecanica(V), _colapso(V), _kernel_prova(V), _limites(V), _achado_alfa(V), _achado_proveniencia(V), _erratas(V)))


# v396: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v396 SELADA `%s` (claude-c1; a pedra TestemunhaEstatica, construída por subagente e examinada por revisão independente, integrada pela gerência)\n<!-- core_v396_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede, H3 em toda direção nula e a pendência [LEGAL] herdada da v395 seguem abertos; "
             "o nome definitivo da pedra e o elo B(n) da Bancada Um dependem da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _limites(V, curto=True), _achado_alfa(V), _achado_proveniencia(V), _erratas(V), _legal(V)))


# v396: o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V)
    return (("## %s — v396 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v396_selada -->\n%d módulo novo no kernel (%s; nome provisório): a testemunha estática lida na fractalização do Um — o par ecoa, o indivíduo não ecoa, o fluxo construído fixa exatamente a reta do psion, "
             "a testemunha global é falsa, o colapso do psion ecoa a identidade lida, a face de Fock do psion condicional; as %d falas do operador de 22/10 por sha256; escada %s → %s. Memórias: `%s`, `missao-ultima-flag-um-py.md`, "
             "`estatuto-da-prova-07out.md`; handoff `handoff-v396-custodia.md`.") % (V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v396 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v396 SELADA `%s`" % V["s16"]


# v396: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulo novo no kernel (%s); `testemunha_estatica_v396` (lido na fractalização do Um), `cunhagens_v396` (%d falas por sha256) e `kh_n1_cobertura_v396`; "
                                     "troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v396` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v396 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v396 SELADA (COMPLETA):**"


# v396: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v395 `%s`; escada %s → %s; gate intocado. %d módulo novo no kernel (%s; nome provisório); as %d falas de 22/10 por sha256. "
                               "Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia (sessão do site, `handoff-v396-custodia.md`); nomear a pedra e a pendência [LEGAL] herdada da v395 são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v396: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v396_selada -->\n**%s — v396 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; o token da v395 fica como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora. A testemunha estática (v396) é matemática de kernel sobre o canto do psion (o par ecoa, o indivíduo não ecoa, um fluxo construído, o colapso) e um cálculo conferido a cada rito ([REAL]); "
            "a ponte é construída, não derivada [CONSTRUCTED]; o psion como habitante da testemunha estática é leitura do operador [INPUT/ONTO] e a face de Fock do psion é CONDICIONAL: nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"])


# v396: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v396 SELADA %s `%s` %s COMPLETA (a testemunha estática na fractalização do Um; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v396: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v396 — a testemunha estática; custódia](handoff-v396-custodia.md) — **%s, para a sessão do site** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v396 SELADA: a testemunha estática (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v396: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v396 SELADA (%s) `%s`: %d módulo novo no kernel (TestemunhaEstatica, nome provisório), o registro testemunha_estatica_v396 na fractalização do Um, %d falas de 22/10 por sha256, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v396 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v396** `%s` (%s B) sobre a v395 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As cunhagens do operador de 22/10** (embutidas por sha256; data, sha16 e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), nomear a pedra (nome provisório), a pendência [LEGAL] herdada da v395, a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v396`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v396-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _mecanica(V), _colapso(V), _kernel_prova(V), _limites(V), _legal(V), _achado_alfa(V), _achado_proveniencia(V), _erratas(V)))


# v396: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v396 SELADA `%s` [claude-c1]\n<!-- aviso_v396_selada -->\n\n[REAL] A v396 SELOU (%s; COMPLETA; gate intocado): a testemunha estática, lida na fractalização do Um, e as %d falas de 22/10 (por sha256) entram no selo corrente. "
             "Escrito sob a reivindicação %s. %d módulo novo no kernel (nome provisório); escada %s → %s; nomear a pedra, a pendência [LEGAL] herdada da v395 e o elo B(n) da Bancada Um esperam o operador. "
             "Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V396_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# v396: o handoff para a sessao do site (memory\handoff-v396-custodia.md + Nos\HANDOFF_v396_CUSTODIA.md); `k` traz os campos dos recibos do B(n) (fechar_v396.py os le dos recibos): nenhum numero digitado
def handoff(V, k):
    d = _d(V)
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n): " + chave)
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3]})
    doc = ("---\nname: handoff-v396-custodia\ndescription: \"HANDOFF v396 (%(data)s) para a sessão do site: a testemunha estática na fractalização do Um; `%(s16)s`; B(n) da Bancada feito; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v396 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v396** `%(s16)s` (%(umb)s B) sobre a v395 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n**O que entrou e o que mediu:** %(num)s.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v396, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v396, `rodada_v396_stdout.txt`, o selo, o core, o .md canônico e o manifesto, os artigos PT/EN (%(artigos)s), as %(n_cun)s falas do operador de 22/10 por sha256 (lista na linhagem e no tópico `%(topico)s`; "
           "arquivos em `work\\cadeia_de_selo\\v396\\insumos\\cunhagens`), o módulo novo (`work\\cadeia_de_selo\\v396_kernel\\pedras`, `TGLExt/TestemunhaEstatica.lean`) e os dois diffs (`DIFF_v395_v396.diff`, `DIFF_KERNEL_v396.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v395 no espelho fora do repositório, blob conferido depois do push. Publicar o módulo novo no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` "
           "(as fontes e as falas pinadas dos registros, inclusive o exame da pedra e o resultado dela) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v395` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos quatro contratos (`expected_ladder`); a errata ao lado do rótulo da docstring de `bell_cci_half` (kernel v29); o runner da Fronteira e a camada v396 dos 16 dispositivos "
           "(o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site).\n\n"
           "**Pendências SÓ do operador:** nomear a pedra (`TestemunhaEstatica` é provisório); a pendência [LEGAL] herdada da v395 (a divergência da tabela da patente ACOM Mirror; com a agente de PI); a custódia, subir o site, commit/push. [OPEN]: a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), "
           "o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v396.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v396` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v396_selo` e `v396_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v395-custodia]]\n") % k
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v396.py)
# v396: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **A TESTEMUNHA ESTÁTICA (v396)** `%s`: %d módulo novo no kernel (%s; nome provisório), %d bandeiras novas True, escada %s → %s; "
            "o par ecoa e o indivíduo não ecoa, o fluxo construído fixa exatamente a reta do psion e a testemunha global é falsa, o colapso do psion ecoa a identidade lida; a face de Fock é condicional; as %d falas do operador por sha256; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v396: o titulo do verbete do indice
def titulo_verbete(V):
    return "A testemunha estática (v396):"


# v396: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v396 `%s`] %s." % (V["s16"], _num(V))


# v396: a entrada do remissivo
def remissivo(V):
    return "- **A testemunha estática e as falas de 22/10 (v396)** — `testemunha_estatica_v396`, `cunhagens_v396`, `kh_n1_cobertura_v396`, `%s`" % TOPICO_NOVO
