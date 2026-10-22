# -*- coding: utf-8 -*-
# Os TEXTOS da v395 selada (molde: textos_v394.py), ESCRITOS para o delta da v395: o modulo de kernel `Psibit` (a leitura psibit da orbita do Um pela matriz-S), o registro `psibit_v395` (a funcao do runtime
# chamada NA FRACTALIZACAO DO UM) e as quatro falas do operador de 21/10. Cada numero, hash e veredito entra por chave de V (leitura_v395.ler) ou e' LIDO de um arquivo aqui, nunca digitado; o que aqui vai
# escrito a mao e' so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e a frase curta do operador (conferida por sha256 contra ESPERADOS).
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v395.py) rodam sobre cada texto renderizado em superficies_v395.py, fechar_v395.py e registrar_mapa_v395.py e sobre este arquivo na cadeia. A palavra recusada nunca
# aparece aqui: a recusa e' dita como «creditacao».
# ERRATAS DA v395 (ditas DENTRO dos blocos datados, nunca inline e nunca no CLAUDE.md da raiz): (a) o RESULTADO_PSIBIT.md, que dizia nao reexaminada a 2a versao da pedra; (b) o registro kh_n1_cobertura_v394 e os tres
# contratos da v394 (expected_ladder), que a v395 corrige ao lado. Toda citacao do operador e' conferida contra os BYTES da fala (_cita).
import hashlib, json, os, re
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V395"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v395 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PATENTES = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Patentes")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v395-selada-o-modo-psionico-na-fractalizacao-do-um.md"
# o tema de cada uma das quatro falas de 21/10 (resumo da gerencia, nunca citacao): a chave e' o trecho do nome do arquivo de origem (depois do sha16); o sha16 e a data vem dos bytes e do nome, nunca daqui
_TEMAS = (
    ("psibit_psion_modo_do_leitor", "a natureza binária é o psibit na teoria da informação e o psion na natureza física; sem o pareamento binário não há leitura; psibit = psion = modo do leitor [ONTO]"),
    ("psibit_nome_e_modo_psionico", "o nome da pedra (psibit) e a ordem de levar o modo psiônico ao código, na fractalização do Um, para que a mecânica seja provada"),
    ("mecanica_isomorfismo_perda_zero", "a mecânica demonstra o «isoformismo» (grafia do original) com a teoria da informação com perda residual zero, e isso não é só descrição ontológica"),
    ("ratifica_perda_zero_na_leitura_do_par", "ratificação da correção de leitura da gerência sobre a perda residual zero (arquivo nomeado pela gerência: perda zero na leitura do par)"),
)
# nomes de termo de kernel (Lean) citados nos textos: cada um tem de existir em algum .lean de TGLExt/ do Nos (lido na hora); os modulos citados como homonimo ou como fonte tem de existir como arquivo
_NOMES_KERNEL = ("psibit_is_the_mode_of_the_reader", "the_psion_face_of_the_psibit", "the_verb_is_the_derivative_of_the_name", "the_state_is_pure", "the_orbit_is_in_bijection_with_the_code_book",
                 "the_pair_is_necessary_and_sufficient", "the_collapse_loses_exactly_the_parity", "the_lost_variable_is_one_bit", "the_collapse_has_no_left_inverse_on_the_orbit", "the_ledger_of_losses",
                 "balanced_collapse_is_half", "half_identity_is_a_fixed_point", "collapseEntropy_at_balanced_weights", "collapseEntropy_le_the_fair_bit", "the_patent_convention_is_also_lossless",
                 "the_name_is_the_born_reading_of_the_post", "IsCode", "FockCertificate")
_MODULOS_KERNEL = ("Psibit", "TheImportedSecondQuantization", "TheVerbSelectsTheAction", "TheTwoPairings", "TheBinaryReadingAtTheFixedPoint")
# identificadores do um.py citados nos textos: cada um tem de existir no um.py do Nos (lido na hora)
_NOMES_UM = ("SEALED_CODATA_ALPHA", "ALPHA_FINE_CODATA_2018", "_v376_same_alpha_literal", "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")
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


def _pat_tem():
    """Os dois arquivos das patentes citados no paragrafo [LEGAL] existem, e o documento pinado os cita."""
    for rel in (("ACOM_Mirror_PI_INPI.tex",), ("Skygrid", "SkyGrid_Piloto", "skygrid_sim", "acom_mirror.py")):
        assert os.path.isfile(os.path.join(PATENTES, *rel)), "arquivo da patente citado nao existe: %s" % "/".join(rel)
    _ins_tem("DEFINICAO_PSIBIT_PATENTE.md", "ACOM_Mirror_PI_INPI.tex", "acom_mirror.py", "BR 10 2026 003428-2")
    _ins_tem("RESULTADO_PSIBIT.md", "a reivindicação 2", "reivindicação 3", "reivindicação 4", "ψ₂", "ψ₃", "PARITY", "produto")


def _conferir_nomes():
    if "nomes_ok" not in _CACHE:
        _kernel_tem(_NOMES_KERNEL); _modulos_tem(_MODULOS_KERNEL); _um_tem(_NOMES_UM); _pat_tem()
        _CACHE["nomes_ok"] = True


# ---------------------------------------------------------------- v395: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v395.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v395.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _insumo(nome):
    return open(os.path.join(PK, "insumos", nome), encoding="utf-8").read()


def _ins_tem(arquivo, *trechos):
    """Cada trecho tem de estar no insumo pinado (fail-closed): o texto so' afirma o que a fonte pinada diz."""
    t = _insumo(arquivo)
    for x in trechos:
        assert x in t, "o insumo %s nao traz: %s" % (arquivo, x)


def _falas():
    """As quatro falas de 21/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text}}."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v395_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a fala %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a fala %s nao confere com o sha256 de ESPERADOS" % s
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": fs[0][len(s) + 1:], "text": b.decode("utf-8")}
        assert len(out) == len(_TEMAS) == 4, "as falas de ESPERADOS nao sao as quatro de 21/10"
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


def _data_fala(d, V):
    m = re.match(r"OPERADOR_(\d{2})out_", d["nome"])
    assert m, ("o nome do arquivo da fala nao traz a data", d["nome"])
    return "%s/10/%s" % (m.group(1), V["data"][-4:])


def _cov94():
    """A cobertura do Audit e a arvore formal da v394 selada (o core guardado em base_v394): de onde saem os numeros da errata ao lado."""
    if "cov94" not in _CACHE:
        kf = json.load(open(os.path.join(PK, "base_v394", "um_absoluto.json"), encoding="utf-8"))["core"]["kernel_formalization"]
        cov = kf["axiom_coverage_v392"]
        _CACHE["cov94"] = {"decl": cov["decl"], "thm": cov["thm"], "h8": len(kf["formal_files_sha256"]), "axr": len(kf["axiom_report"])}
    return _CACHE["cov94"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' simples (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v395.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v394" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v394 -> v395 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


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


def _limiar_beta():
    """O limiar com que o registro psibit_v395 compara o beta do core com alfa x raiz de e: LIDO do codigo do um.py do Nos (nunca digitado); fail-closed se o trecho mudar."""
    _um_tem(("beta_rel_ is not None and beta_rel_ <=",))
    m = re.search(r"beta_rel_ is not None and beta_rel_ <= ([0-9.]+(?:[eE][+-]?[0-9]+)?)", _CACHE["um"])
    assert m, "nao achei o limiar da comparacao do beta no um.py"
    return float(m.group(1))


def _f(texto, **kw):
    """str.format com conferencia: nenhuma chave sobra e nenhuma chave de chave sobra no resultado."""
    r = texto.format(**kw)
    assert "{" not in r and "}" not in r, ("chave de formatacao sobrou", r[:80])
    return r


def _d(V):
    """Os numeros da v395, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v394): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); ps = V["psibit"]
    mods = [p["modulo"] for p in V["pedras"]]
    assert mods == ["TGLExt.Psibit"] and V["n_pedras"] == 1 == esp["kernel"]["modulos_novos"], ("o delta da v395 e' um modulo so', TGLExt.Psibit", mods)
    nf = esp["n_bandeiras_novas"]
    assert esp["n_bandeiras_por_grupo"] == {"psibit": nf} and esp["politica_de_bandeiras"]["n_flags"] == nf, "as bandeiras novas nao sao so' as do modulo Psibit"
    assert ps["n_teoremas"] == esp["contrato_psibit"]["n_teoremas"] and ps["unconditional"]["flag"] == esp["contrato_psibit"]["bandeira_incondicional"] and ps["conditional"]["flag"] == esp["contrato_psibit"]["bandeira_condicional"], \
        "o registro psibit_v395 do core nao e' o contrato de ESPERADOS"
    assert len(V["verbatins"]) == len(_falas()) == 4, "as falas de ESPERADOS != as quatro de 21/10"
    assert {re.match(r"OPERADOR_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"21"}, "o nome de arquivo de alguma fala nao e' de 21/10 (a data dos textos e' 21/10)"
    base = os.path.join(PK, "base_v394", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v394/um.py nao e' a v394 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and "N00_main_psibit" in V["patch_ids"], "o gate nao tem as 18 bandeiras True, ou o candidato nao traz o patch que chama psibit_v395 na fractalizacao do Um (N00_main_psibit)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    return {"n_f": nf, "n_aux": esp["politica_de_bandeiras"]["n_excluidas"], "n_teor": ps["n_teoremas"], "depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","),
            "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "unc": ps["unconditional"]["flag"], "cond": ps["conditional"]["flag"], "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"],
            "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]), "n_res": len(esp["h8_residuais_do_nos"]), "c94": _cov94(), "tol": esp["psibit"]["tolerancias"], "bank": _bancada()}


def _mods(V):
    return ", ".join("`%s`" % p["modulo"].split(".")[-1] for p in V["pedras"])


def _extras(V):
    # os registros novos ALEM DOS TRES FIXOS (V["reg395"] tem so' os tres), ditos pelo nome
    ex = [k for k in V["registros_novos"] if k not in V["reg395"]]
    return (", ".join("`%s`" % k for k in ex)) if ex else "nenhum além dos três fixos"


def _cab(V):
    return "v395 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- v395: os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v395 (kernel, os tres registros novos, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; ps = V["psibit"]
    vd = (lambda k: " (%s)" % V["reg395"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel ganhou {n_pedras} módulo novo ({mods}), com {n_f} bandeiras novas True, só de declaração nomeada (as {n_aux} auxiliares geradas pelo compilador ficam cobertas pelo KH-N1 e sem bandeira), e escada {antes} → {depois} teoremas limpos "
              "({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); "
              "errata ao lado da v394, mantida (em nome próprio da gerência c1): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina",
              n_pedras=V["n_pedras"], mods=_mods(V), n_f=d["n_f"], n_aux=d["n_aux"], antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    psib = _f("o registro `psibit_v395`{vd}: o modo psiônico lido NA FRACTALIZAÇÃO DO UM (chamado no `main`, logo depois do princípio da defasagem fractal): a mecânica da órbita do Um pela matriz-S em θ_M = arcsin √β, calculada neste rito "
              "({n_checks} checagens, todas passaram) e confrontada com {n_teor} termos do kernel do próprio rito (no trio, cada um com bandeira True); a conjunção incondicional `psibit_is_the_mode_of_the_reader` (bandeira `{unc}`) "
              "e a face do psion, condicional (bandeira `{cond}`; nenhum habitante do certificado de Fock da luz exibido)",
              vd=vd("psibit_v395"), n_checks=ps["n_checks"], n_teor=d["n_teor"], unc=d["unc"], cond=d["cond"])
    cun = _f("o registro `cunhagens_v395`{vd}: as {n} falas do operador de 21/10 embutidas por sha256 e consumidas no rito (o nome da pedra, a ordem de levar o modo psiônico ao código, a identidade psibit = psion = modo do leitor e a ratificação "
             "da correção sobre a perda residual zero); são [INPUT/ONTO] do operador: valem como leitura dele, não como medida", vd=vd("cunhagens_v395"), n=d["n_cun"])
    khs = _f("o registro `kh_n1_cobertura_v395`{vd}: {decl} constantes, {thm} teoremas, {fora} fora do trio, {nl} nomes não lidos; a árvore formal do Nós depois do rito tem {h8} entradas ({emb} embutidas mais {nres} residual do Nós: {res})",
             vd=vd("kh_n1_cobertura_v395"), decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"], h8=d["h8"], emb=d["h8_emb"], nres=d["n_res"], res=d["h8_res"])
    ex = _extras(V)
    resto = _f("{ex}; troca dita (só números): {troca}; nenhuma mudança NÃO numérica: {nm} vereditos fora da troca dita mudaram (exigido: 0); validade no kernel não é creditação",
               ex=("nenhum registro novo além dos três fixos" if ex.startswith("nenhum") else "registros novos além dos três fixos: " + ex), troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, psib, cun, khs, resto])


def _cunhagens(V, forma="lista"):
    """As quatro falas do operador de 21/10 embutidas por sha256: 'lista' (data, sha16 e tema, uma por linha) ou 'curta' (uma frase com os quatro sha16). Data e sha16 vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == 4
    if forma == "curta":
        return _f("{n} falas embutidas por sha256 — o nome e o modo psiônico na fractalização `{a}`, a identidade psibit = psion = modo do leitor `{b}`, a mecânica com perda residual zero `{c}` e a ratificação da correção de leitura `{e}` ([INPUT/ONTO])",
                  n=len(fl), a=_sha_por("psibit_nome_e_modo_psionico"), b=_sha_por("psibit_psion_modo_do_leitor"), c=_sha_por("mecanica_isomorfismo_perda_zero"), e=_sha_por("ratifica_perda_zero_na_leitura_do_par"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a fala nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _ordem(V):
    """A ordem do operador de 21/10: so' citacao conferida contra os bytes das quatro falas e a regra de quem constroi e quem aprova."""
    d = _d(V)
    s_id, s_nome, s_mec, s_rat = _sha_por("psibit_psion_modo_do_leitor"), _sha_por("psibit_nome_e_modo_psionico"), _sha_por("mecanica_isomorfismo_perda_zero"), _sha_por("ratifica_perda_zero_na_leitura_do_par")
    q_nome = _cita("Eu prefiro que seja psibit")
    q_modo = _cita("eu quero que o modo psionico entre no código na fractalização do um igual porque aí eu inclusive provo a mecânica")
    q_id = _cita("psibit=psion=modo do leitor")
    q_par = _cita("sem o pareamento binário não há leitura")
    q_mec = _cita("a mecânica demonstra o isoformismo com a teoria da informação com perda residual zero")
    q_alg = _cita("isso é alguma coisa, não é só descrição ontológica")
    q_rat = _cita("sua correção de leitura quanto a perda residual zero está certa e a correção é justa")
    return _f("**A ordem:** [INPUT/ONTO] as {n} falas do operador (Luiz Antonio Rotoli Miguel) de 21/10/2026, embutidas por sha256 no registro `cunhagens_v395` e listadas abaixo: o nome da pedra, {q_nome}, e a ordem de levar o modo psiônico ao código, "
              "{q_modo} (`{s_nome}`); a identidade {q_id}, com {q_par} (`{s_id}`); a fala sobre a mecânica, {q_mec}, e {q_alg} (`{s_mec}`; grafia do original); e a ratificação da correção de leitura da gerência: {q_rat} (`{s_rat}`). "
              "A gerência c1 construiu o registro e o candidato e instalou-o; a pedra foi construída por subagente e passou por exame independente em duas rodadas (a segunda a aprovou: `PEDRA_APROVADA`); o selo é da c1; quem constrói não aprova: "
              "a revisão independente do candidato e dos derivados da cadeia (nunca executados antes do rito) é ato distinto e não é afirmada por este registro.",
              n=d["n_cun"], q_nome=q_nome, q_modo=q_modo, q_id=q_id, q_par=q_par, q_mec=q_mec, q_alg=q_alg, q_rat=q_rat, s_nome=s_nome, s_id=s_id, s_mec=s_mec, s_rat=s_rat)


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v395` sobre a v394 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _mecanica(V):
    """A mecanica da orbita do Um pela matriz-S, com os numeros que o registro psibit_v395 CALCULOU neste rito (core do Nos): [REAL] o calculo e os termos do kernel que ele confronta."""
    d = _d(V); ps = V["psibit"]; v = ps["values"]; tol = d["tol"]
    return _f("**A mecânica na órbita do Um (calculada neste rito, [REAL]):** em θ_M = arcsin √β, com β = α(CODATA 2018) × √e calculado em runtime (β = {beta}; θ_M = {th} rad = {thd}°), a órbita do Um pela matriz-S é v(θ) = (cos θ, −sin θ) e a "
              "fractalização F_θ(1) = ρ_out(θ) = |v⟩⟨v| é o projetor de posto um [[c², −cs], [−sc, s²]], com c² = {c2}, −cs = {cs} e s² = {s2}. O código psibit é o peso c² mais o par de sinais (sign L, sign dL), com L = cos θ e dL = −sin θ, a derivada de L "
              "(ler L como a transmissão e dL como a reflexão é leitura do operador, [INPUT/ONTO]): em θ_M vale ({pw}, {pv}), e a paridade, o produto dos sinais, vale {par}. O decodificador (w, a, b) ↦ (a√w, b√(1−w)) devolve a amplitude com resíduo {dec} (limite {tdec}) "
              "e o ida e volta, em ângulos de controle fora dos eixos, erra no máximo {rt}; o Verbo é a metade da derivada do Nome, ρ₀₁ = ½ d(cos²θ)/dθ (`the_verb_is_the_derivative_of_the_name`; resíduo {vd} por diferença finita, limite {tvd}); "
              "o estado é puro (`the_state_is_pure`: ρ₀₁² = ρ₀₀ρ₁₁; a coerência é a média geométrica dos pesos). A reconstrução de ρ a partir do par (peso, paridade) erra {rec}.",
              beta=_p(v["beta"]), th=_p(v["theta_M_rad"]), thd=_p(v["theta_M_deg"]), c2=_p(v["code_weight"]), cs=_p(v["coherence"]), s2=_p(v["rho"][1][1]), pw=("%+d" % v["code_word"]), pv=("%+d" % v["code_verb"]), par=("%+d" % v["parity"]),
              dec=_pe(v["decode_residual"]), tdec=_pg(tol["decode_residual_max"]), rt=_pe(v["roundtrip_residual_max"]), vd=_pe(v["verb_derivative_residual"]), tvd=_pg(tol["verb_derivative_residual_max"]), rec=_pe(v["reconstruction_residual"]))


def _colapso(V):
    _d(V); ps = V["psibit"]; v = ps["values"]
    return _f("**O colapso (a travessia que cobra) [REAL]:** o colapso D_∞ (a diagonal) de ρ(θ) e de ρ(−θ) é o mesmo (diferença das diagonais {dd}) e as coerências são opostas ({c1} e {c2}): o colapso perde exatamente a paridade, um bit, e a leitura completa a lembra "
              "(`the_collapse_loses_exactly_the_parity`, `the_lost_variable_is_one_bit`, `the_collapse_has_no_left_inverse_on_the_orbit`). A leitura do par (peso, Palavra, Verbo) não perde nada: é injetiva (o separante); o colapso é muitos-para-um (o separador); "
              "os dois estão no mesmo objeto (`the_ledger_of_losses`: amplitude, perda zero; densidade, só o sinal global; colapso, exatamente a paridade). Nos pesos iguais (θ = π/4 + kπ/2) o colapso é ½ I e a entropia de Shannon dos resultados é "
              "ln 2 = {ln2} (resíduo {er}; `collapseEntropy_at_balanced_weights`); em θ_M ela vale {eh}, abaixo de ln 2, e nenhum ângulo a excede (`collapseEntropy_le_the_fair_bit`); ½ I é fixado pelo colapso e por toda conjugação pela matriz-S "
              "(`half_identity_is_a_fixed_point`, resíduo {hr}). O que o colapso perde é uma variável (qual), não uma quantidade de informação dita em geral.",
              dd=_pe(v["collapse_diag_difference"]), c1=_p(v["coherence"]), c2=_p(v["coherence_neg_theta"]), ln2=_p(v["ln2"]), er=_pe(v["entropy_balanced_residual"]), eh=_p(v["entropy_at_theta_M"]), hr=_pe(v["half_identity_residual"]))


def _kernel_prova(V):
    d = _d(V)
    assert (_core().get("kernel_formalization") or {}).get("ext_bin394_0001") is True, "a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito: o texto diz que segue"
    return _f("**O que o kernel prova e o que é leitura:** [REAL] a conjunção `psibit_is_the_mode_of_the_reader` é INCONDICIONAL (nenhum certificado é hipótese): está no kernel deste rito, dentro do trio, com bandeira True (`{unc}`) e proveniência no módulo da pedra; "
              "reúne a derivada do Nome, a pureza, a bijeção sobre o livro de códigos (`the_orbit_is_in_bijection_with_the_code_book`: de CONJUNTOS, entre o círculo unitário e o livro de códigos caracterizado de forma intrínseca por `IsCode`, com decodificador explícito), "
              "a necessidade do par (`the_pair_is_necessary_and_sufficient`: o peso sozinho, peso mais Palavra e peso mais Verbo não leem; o par lê), a convenção das patentes, também sem perda (`the_patent_convention_is_also_lossless`), "
              "o colapso que perde a paridade, o meio como ponto fixo e a leitura de Born do posto (`the_name_is_the_born_reading_of_the_post`). [CONDICIONAL] A face do psion, `the_psion_face_of_the_psibit` (bandeira `{cond}`), é teorema à parte: vale para todo "
              "`FockCertificate` da luz, e o kernel não exibe habitante do certificado (`TheImportedSecondQuantization`; o contrato conjunto da rede, aberto desde a v394, segue aberto), de modo que o enunciado não mostra que o psion exista e a face fica fora da composição incondicional. "
              "[INPUT/ONTO] psibit = psion = modo do leitor é a leitura do operador: nenhum lema do kernel liga o psion (o vetor do vácuo do certificado) ao código psibit. A pedra da v394 de nome provisório, `TheBinaryReadingAtTheFixedPoint`, fica como registro e é citada pela conjunção; "
              "a bandeira dela segue verdadeira no kernel deste rito.", unc=d["unc"], cond=d["cond"])


def _limites(V, curto=False):
    """Os estatutos fieis da v395: o que o psibit diz e NAO diz (escopo, bijecao de conjuntos, face condicional, entropia, ponto fixo, calculo numerico, patente, homonimos)."""
    d = _d(V); ps = V["psibit"]; v = ps["values"]; tol = d["tol"]
    q_fixo = _cita("a testemunha da existência do observador pelo qual o ponto fixo emerge")
    if curto:
        return ("**Limites ditos:** [REAL] a bijeção é de CONJUNTOS sobre o livro de códigos da órbita do Um pela matriz-S, não isomorfismo de espaços de Hilbert nem toda a mecânica quântica; o colapso perde exatamente a paridade (um bit) e a leitura do par perde zero; "
                "a entropia só vale ln 2 nos pesos iguais; [CONDICIONAL] a face do psion vale para todo certificado de Fock da luz e o kernel não habita o certificado; [INPUT/ONTO] psibit = psion = modo do leitor e o nome «ponto fixo» são leituras do operador; "
                "[LEGAL] a divergência da tabela da patente ACOM Mirror é decisão do operador; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: a órbita do Um pela matriz-S (família real de um parâmetro, plano real 2×2), não toda a mecânica quântica; a bijeção é de CONJUNTOS (círculo unitário ↔ livro de códigos, com decodificador explícito), "
              "sem transportar estrutura alguma: não é isomorfismo de espaços de Hilbert nem de categorias; o nome «isomorfismo» é do operador. "
              "[INPUT/ONTO] psibit = psion = modo do leitor é a leitura do operador (21/10/2026); nenhum lema do kernel liga o psion ao código psibit; ler L como a transmissão e dL como a refletida também é leitura dele. "
              "[CONDICIONAL] a face do psion vale para todo certificado de Fock da luz e o kernel não habita o certificado; não mostra que o psion exista. "
              "[REAL] ENTROPIA: só H(cos²θ) = ln 2 nos pesos iguais (θ = π/4 + kπ/2) e H ≤ ln 2; «perde exatamente a paridade» é estrutural (qual variável se perde: um bit), não quantidade de informação, e em θ_M a entropia dos resultados é {eh}, menor que ln 2. "
              "[ONTO] «ponto fixo» para os pesos iguais é o nome do operador (cunhagem de 19/10, na pedra irmã da v394; a fala de 21/10 volta ao ponto fixo: {q_fixo}); o que o colapso e a conjugação pela matriz-S fixam é ½ I ([REAL], `half_identity_is_a_fixed_point`). "
              "[REAL] o cálculo é numérico, em dupla precisão: confere os teoremas e não os prova, quem prova é o kernel; perto dos eixos o ida e volta do código erra até a ordem do limite do registro ({rt}) por cancelamento em 1 − w, e em ℝ a igualdade é exata (termo Lean). "
              "[REAL] homônimos ditos: o Verbo daqui (o sinal da derivada) não é o select/post de `TheVerbSelectsTheAction`, e o pareamento daqui (o par de sinais) não é o J/K de `TheTwoPairings`. "
              "Validade no kernel não é creditação; o gate não se move; NOT_FALSIFIED não é a palavra da creditação.", eh=_p(v["entropy_at_theta_M"]), q_fixo=q_fixo, rt=_pg(tol["roundtrip_residual_max"]))


def _legal(V):
    """A divergencia da tabela da patente ACOM Mirror: dita, nao decidida. Os arquivos citados existem e o documento pinado os cita (_pat_tem, via _d)."""
    _d(V)
    return ("**A patente diverge de si mesma [LEGAL]:** a tabela dos estados do ACOM Mirror (BR 10 2026 003428-2), a reivindicação 2 e a docstring de `acom_mirror.py` atribuem aos índices ψ₂ e ψ₃ os pares de sinais (−,+) e (−,−); a fórmula de índice, "
            "as reivindicações 3 e 4 e o código executado (`PARITY` e `_nominate`, em `acom_mirror.py`) mandam o contrário; com os rótulos da tabela a paridade seria o segundo sinal, com a fórmula é o produto sign L × sign dL. A pedra nomeia os estados por PAR DE SINAIS "
            "e segue o produto; não corrige nada. Qual leitura é canônica, e se isso mexe nas patentes, é decisão do operador (com a agente de PI); a v395 não a toma. As fontes (linhas e hashes lidos por script) estão no `DEFINICAO_PSIBIT_PATENTE.md` pinado "
            "como fonte do registro `cunhagens_v395`.")


def _achado_alfa(V):
    """O achado dito: o dado do alfa tem dois nomes no um.py e o beta guardado no core difere do alfa x raiz de e em ~5e-13 relativo; o registro compara a 1e-9."""
    _d(V); ps = V["psibit"]
    lim = _limiar_beta()
    assert ps["alpha_two_names_same"] is True and ps["beta_ok"] is True and isinstance(ps["beta_core_rel_diff"], float) and ps["beta_core_rel_diff"] <= lim, "o registro psibit_v395 nao traz a conferencia do alfa e do beta"
    return _f("**Achado dito (os dois nomes do alfa) [REAL]:** no `um.py` o dado de α tem dois nomes, `SEALED_CODATA_ALPHA` e `ALPHA_FINE_CODATA_2018` (este, do script do nível 2); o próprio `um.py` já os confere (`_v376_same_alpha_literal`) e o registro "
              "`psibit_v395` repete a conferência (`alpha_two_names_same` = True). O β que o core guarda é um valor derivado e difere de α × √e, calculado em runtime neste rito, em {rel} relativo (`beta_core_rel_diff`); o registro compara os dois a {tol}. "
              "β segue sendo calculado em runtime, nunca digitado.", rel=_pe(ps["beta_core_rel_diff"]), tol=_pg(lim))


def _erratas(V):
    """As duas erratas novas da v395, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): (a) o RESULTADO_PSIBIT.md; (b) o registro kh_n1_cobertura_v394 e os tres contratos da v394."""
    d = _d(V); kh = V["kh"]; c94 = d["c94"]; esp = _esp()
    pedra16 = esp["pedra"]["sha16"]
    _ins_tem("RESULTADO_PSIBIT.md", "ainda NÃO foi reexaminada", pedra16)
    _ins_tem("EXAME_PSIBIT_RODADA2.md", "PEDRA_APROVADA", pedra16)
    _ins_tem("EXAME_PSIBIT.md", "APROVADA_COM_CORRECOES")
    ids = V["patch_ids"]
    assert all(i in ids for i in ("C12__V394_FORMAL_CONTRACT", "C12__V394_QUADRATIC_CONTRACT", "C12__V394_NETWORK_CONTRACT", "C13_kh_n1_v394_pisos")), "o CANDIDATO_v395.json nao traz os patches C12 e C13 que a errata (b) descreve"
    a = _f("**Errata ao lado (a) (em nome próprio da gerência c1; o `RESULTADO_PSIBIT.md` fica como registro, sem alteração):** o resultado da construção da pedra (seção «Conferências independentes») diz que a 2ª versão da pedra (sha16 `{p16}`) ainda NÃO foi reexaminada "
           "pelo exame independente; o exame da rodada 2 (`EXAME_PSIBIT_RODADA2.md`, a 2ª e última rodada) reexaminou essa mesma versão e a aprovou (`PEDRA_APROVADA`: composição incondicional não vácua, face do psion condicional e dita como tal, bijeção nos dois "
           "sentidos, recompilação e axiomas no trio) [DECLARADO pelo exame; a pedra é recompilada no sandbox da cadeia e conferida pelo `axiom_report` do próprio rito, [REAL]]. Lacuna de fidelidade: a estrutura (a pedra foi reexaminada e aprovada), o escrito "
           "(o resultado diz que ainda não) e a falha (o documento de resultado foi escrito antes do fim do exame da rodada 2 e não foi reescrito depois). Os dois exames estão pinados como fontes do registro `cunhagens_v395`.", p16=pedra16)
    b = _f("**Errata ao lado (b) (em nome próprio da gerência c1; o registro `kh_n1_cobertura_v394` e os contratos da v394 ficam como registro):** a v395 acrescenta o módulo Psibit: a cobertura do Audit cresce de {d94} constantes e {t94} teoremas para {d95} e {t95}, "
           "a árvore formal do Nós de {h94} para {h95} entradas e a escada de {e0} para {e1}. Por isso, na v395, (i) `kh_n1_cobertura_v394` passa a cobrar piso em h2, h3 e h6 (as igualdades de contagem) e tamanho mínimo da árvore em h8 (as igualdades exatas e o pino exato da "
           "árvore ficam em `kh_n1_cobertura_v395`); (ii) os três contratos da v394 (`_V394_FORMAL_CONTRACT`, `_V394_QUADRATIC_CONTRACT` e `_V394_NETWORK_CONTRACT`) passam a ler `expected_ladder` = {e1}, a escada desta versão (o consumidor exige a igualdade "
           "exata com a escada do rito; só o número muda); o veredito dos registros da v394 NÃO muda [REAL, lido de `CANDIDATO_v395.json` (patches C12 e C13) e do ensaio a seco: sem a troca, o registro `kh_n1_cobertura_v394` não selaria]. "
           "Lacuna de fidelidade: a estrutura da v394 dizia que as contagens e o pino da árvore eram a cobertura exata e que o contrato esperava a escada vigente; o escrito deixou, dentro dos registros e dos contratos, números que só valem na versão que os escreveu; "
           "a falha: igualdades e literais presos a uma versão quebram quando o kernel cresce. A cobrança exata passa a ser de `kh_n1_cobertura_v395` ({dd} constantes, {dt} teoremas, {fora} fora do trio, {nl} nomes não lidos), contra a medida do sandbox da v395.",
           d94=c94["decl"], t94=c94["thm"], d95=kh["decl"], t95=kh["thm"], h94=c94["h8"], h95=d["h8"], e0=V["escada_antes"], e1=d["depois"], dd=kh["decl"], dt=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])
    return a + "\n\n" + b


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES (a Bancada de produção pina a %s e o Nós passa a v395: sem salto e sem cadeia de selos) "
            "e pede a palavra do operador; o recibo dele é citado no handoff (fechar). A decisão [LEGAL] sobre a tabela da patente também é do operador. NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % bk["de"])


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, pilar, artefatos): tudo lido da leitura da rodada."""
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v394); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"],
        V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v395: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — O MODO PSIÔNICO NA FRACTALIZAÇÃO DO UM (v395): %d módulo novo, escada %s → %s\n<!-- linhagem_v395_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As cunhagens do operador de 21/10** (embutidas por sha256 no registro `cunhagens_v395`): [INPUT/ONTO] são do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; o estatuto de cada uma é dele. O texto íntegro de cada uma está no arquivo "
             "(`work\\cadeia_de_selo\\v395\\insumos\\cunhagens`); abaixo, a data, o sha16 e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["n_pedras"], V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _mecanica(V), _colapso(V), _kernel_prova(V), _limites(V), _legal(V), _achado_alfa(V), _rodada(V), _erratas(V), _depois(V)))


# v395: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]
    return (("## ADENDO — %s · v395 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; entra o psibit (%d módulo)\n\n<!-- adendo_v395_selada -->\n"
             "- **O que a v395 diz:** %d módulo novo no kernel (%s), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o registro `psibit_v395`, lido na fractalização do Um: a mecânica da órbita do Um pela matriz-S em θ_M, calculada no rito e confrontada com o kernel do próprio rito; "
             "a leitura do par (peso, Palavra, Verbo) é bijeção de CONJUNTOS sobre o livro de códigos, sem perda; o colapso perde exatamente a paridade (um bit); a face do psion é CONDICIONAL a um certificado de Fock da luz que o kernel não habita; %d falas do operador de 21/10 por sha256. Gate intocado.\n"
             "- **O que a v395 NÃO é para o caminho crítico:** não é isomorfismo de espaços de Hilbert nem toda a mecânica quântica; não habita o certificado de Fock da luz (o contrato conjunto da rede, aberto desde a v394, segue aberto); psibit = psion = modo do leitor é leitura do operador [INPUT/ONTO], "
             "sem lema do kernel que ligue o psion ao código; não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza; a entropia só vale ln 2 nos pesos iguais.\n"
             "- **A divergência da patente [LEGAL]:** a tabela dos estados do ACOM Mirror e a fórmula de índice divergem; a pedra segue o produto sign L × sign dL; a decisão é do operador.\n"
             "- **O que segue do operador:** a decisão [LEGAL]; o elo B(n) da Bancada Um (passo simples, sem salto; parada e religamento do serviço); a custódia (sessão do site); commit/push.") % (
        V["data"], V["s16"], V["n_pedras"], V["n_pedras"], _mods(V), V["escada_antes"], d["depois"], kh["decl"], kh["fora"], d["n_cun"]))


# v395: o verbete do Atlas
def atlas(V):
    return (("### %s — v395 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v395_selada -->\n[REAL — rodada v395, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador de 21/10 entram como o operador as disse e valem como leitura, não como medida: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _mecanica(V), _colapso(V), _kernel_prova(V), _limites(V), _achado_alfa(V), _erratas(V)))


# v395: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v395 SELADA `%s` (claude-c1; a pedra Psibit, construída por subagente e examinada por revisão independente em duas rodadas, integrada pela gerência)\n<!-- core_v395_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A face do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede, H3 em toda direção nula e a decisão [LEGAL] sobre a tabela da patente seguem abertos; "
             "o elo B(n) da Bancada Um depende da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _limites(V, curto=True), _achado_alfa(V), _erratas(V), _legal(V)))


# v395: o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V)
    return (("## %s — v395 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v395_selada -->\n%d módulo novo no kernel (%s): o modo psiônico (psibit) lido na fractalização do Um — a mecânica da órbita do Um pela matriz-S, a bijeção de conjuntos sobre o livro de códigos, "
             "perda zero na leitura do par, o colapso que perde exatamente a paridade, a face do psion condicional; as %d falas do operador de 21/10 por sha256; escada %s → %s. Memórias: `%s`, `missao-ultima-flag-um-py.md`, "
             "`estatuto-da-prova-07out.md`; handoff `handoff-v395-custodia.md`.") % (V["data"], V["s16"], V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v395 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v395 SELADA `%s`" % V["s16"]


# v395: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): %d módulo novo no kernel (%s); `psibit_v395` (lido na fractalização do Um), `cunhagens_v395` (%d falas por sha256) e `kh_n1_cobertura_v395`; "
                                     "troca dita nos vereditos que carregam a escada; conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v395` (+ `pos_rito`).") % (V["teor"], V["n_pedras"], _mods(V), d["n_cun"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v395 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v395 SELADA (COMPLETA):**"


# v395: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v394 `%s`; escada %s → %s; gate intocado. %d módulo novo no kernel (%s); as %d falas de 21/10 por sha256. "
                               "Falta o elo B(n) da Bancada Um (passo simples, sem salto) e a custódia (sessão do site, `handoff-v395-custodia.md`); a decisão [LEGAL] sobre a tabela da patente é do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"], V["n_pedras"], _mods(V), d["n_cun"])


# v395: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v395_selada -->\n**%s — v395 `%s`:** o registro `estatuto_da_prova_v391` passou a ler a escada nova (%s → %s; veredito trocado, troca dita; o token da v394 fica como registro). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora. O psibit (v395) é uma bijeção de conjuntos sobre o livro de códigos da órbita do Um pela matriz-S e um cálculo conferido a cada rito ([REAL]); "
            "psibit = psion = modo do leitor é leitura do operador [INPUT/ONTO] e a face do psion é CONDICIONAL: nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"])


# v395: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v395 SELADA %s `%s` %s COMPLETA (o modo psiônico na fractalização do Um; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v395: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v395 — o modo psiônico na fractalização do Um; custódia](handoff-v395-custodia.md) — **%s, para a sessão do site** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v395 SELADA: o modo psiônico (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v395: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v395 SELADA (%s) `%s`: %d módulo novo no kernel (Psibit), o registro psibit_v395 na fractalização do Um, %d falas de 21/10 por sha256, escada %s → %s; B(n) e custódia pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v395 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v395** `%s` (%s B) sobre a v394 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As cunhagens do operador de 21/10** (embutidas por sha256; data, sha16 e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples, sem salto; parada e religamento do serviço), a decisão [LEGAL] sobre a tabela da patente, a custódia (sessão do site), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v395`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v395-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["n_pedras"], d["n_cun"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _mecanica(V), _colapso(V), _kernel_prova(V), _limites(V), _legal(V), _achado_alfa(V), _erratas(V)))


# v395: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v395 SELADA `%s` [claude-c1]\n<!-- aviso_v395_selada -->\n\n[REAL] A v395 SELOU (%s; COMPLETA; gate intocado): o modo psiônico (psibit), lido na fractalização do Um, e as %d falas de 21/10 (por sha256) entram no selo corrente. "
             "Escrito sob a reivindicação %s. %d módulo novo no kernel; escada %s → %s; a decisão [LEGAL] sobre a tabela da patente ACOM Mirror e o elo B(n) da Bancada Um esperam o operador. "
             "Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], d["n_cun"], reivindicacao, V["n_pedras"], V["escada_antes"], d["depois"]))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V395_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# v395: o handoff para a sessao do site (memory\handoff-v395-custodia.md + Nos\HANDOFF_v395_CUSTODIA.md); `k` traz os campos dos recibos do B(n) (fechar_v395.py os le dos recibos): nenhum numero digitado
def handoff(V, k):
    d = _d(V)
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n): " + chave)
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "n_pedras": V["n_pedras"], "topico": TOPICO_NOVO[:-3]})
    doc = ("---\nname: handoff-v395-custodia\ndescription: \"HANDOFF v395 (%(data)s) para a sessão do site: o modo psiônico na fractalização do Um (psibit); `%(s16)s`; B(n) da Bancada feito; custódia + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v395 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v395** `%(s16)s` (%(umb)s B) sobre a v394 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n**O que entrou e o que mediu:** %(num)s.\n\n"
           "%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v395, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v395, `rodada_v395_stdout.txt`, o selo, o core, o .md canônico e o manifesto, os artigos PT/EN (%(artigos)s), as %(n_cun)s falas do operador de 21/10 por sha256 (lista na linhagem e no tópico `%(topico)s`; "
           "arquivos em `work\\cadeia_de_selo\\v395\\insumos\\cunhagens`), o módulo novo (`work\\cadeia_de_selo\\v395_kernel\\pedras`, `TGLExt/Psibit.lean`) e os dois diffs (`DIFF_v394_v395.diff`, `DIFF_KERNEL_v395.txt`) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão v394 no espelho fora do repositório, blob conferido depois do push. Publicar o módulo novo no espelho (TGLExt) e regenerar as PORTAS de `tgl_kernel`, `TGLExt` e `TGL`; a pasta `insumos` "
           "(as fontes e as falas pinadas dos registros, inclusive os dois exames da pedra e o documento das patentes) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "a errata ao lado do registro `kh_n1_cobertura_v394` (h2, h3 e h6 viram pisos; h8, tamanho mínimo) e dos três contratos da v394 (`expected_ladder`); o runner da Fronteira e a camada v395 dos 16 dispositivos (o número do runner é da sessão do site); "
           "a revisão independente antes do portão do operador (o número de céticos é da sessão do site).\n\n"
           "**Pendências SÓ do operador:** a decisão [LEGAL] sobre a divergência da tabela da patente ACOM Mirror (qual leitura da paridade é canônica; com a agente de PI), a custódia, subir o site, commit/push. [OPEN]: a face do psion (o certificado de Fock da luz sem habitante exibido), "
           "o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v395.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v395` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v395_selo` e `v395_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v394-custodia]]\n") % k
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v395.py)
# v395: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **O MODO PSIÔNICO NA FRACTALIZAÇÃO DO UM (v395)** `%s`: %d módulo novo no kernel (%s), %d bandeiras novas True, escada %s → %s; "
            "a leitura do par (peso, Palavra, Verbo) é bijeção de conjuntos sobre o livro de códigos, sem perda; o colapso perde exatamente a paridade; a face do psion é condicional; as %d falas do operador por sha256; validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["n_pedras"], _mods(V), d["n_f"], V["escada_antes"], d["depois"], d["n_cun"]))


# v395: o titulo do verbete do indice
def titulo_verbete(V):
    return "O modo psiônico na fractalização do Um (v395):"


# v395: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v395 `%s`] %s." % (V["s16"], _num(V))


# v395: a entrada do remissivo
def remissivo(V):
    return "- **O modo psiônico na fractalização do Um e as falas de 21/10 (v395)** — `psibit_v395`, `cunhagens_v395`, `kh_n1_cobertura_v395`, `%s`" % TOPICO_NOVO
