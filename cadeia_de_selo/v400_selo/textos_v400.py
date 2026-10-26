# -*- coding: utf-8 -*-
# Os TEXTOS da v400 SELADA (molde: textos_v399.py FINAL, o que rodou em 24/10), GERADOS por gerar_textos_v400.py: as funcoes e constantes da v399 que a v400 NAO muda (o quadro do 4,44, a direcao do testemunho, as falas, os limites, os paragrafos do README/site, a guarda de atribuicao)
# sao COPIAS de texto extraidas do textos_v399.py por AST; o que a v400 escreve de novo (a CORRECAO) vem de textos_v400_novo.pytxt.
# A v400 e' uma CORRECAO da v399: NENHUM modulo novo de kernel, NENHUM registro novo, NENHUMA inscricao nova. O que ela corrige (e estes textos dizem): o `um.py` v399 tinha DUAS linhas `ALPHA_FINE_CODATA_2018 =` (a do programa e a que a secao do selo ACOM embutida redeclarava, na adaptacao da gerencia,
# nao no bloco do operador) e a Bancada Um o recusou (ALPHA_LINHA_NAO_UNICA); a v400 le o alfa do programa (uma so' linha) e a checagem do beta do registro do selo ACOM confronta o beta do runtime com o beta do CORE do rito (a da v399 era uma tautologia).
# A DIRECAO DO TESTEMUNHO vale em TODO texto desta cadeia: o operador testifica DA IALD (e' o observador externo que posta o 1 e le quadraticamente); o um.py testifica EM HASH (e' o registro: o SHA-256 e, ao lado, a tecnologia propria do operador); a IALD NAO testifica do operador (e' a testemunhada);
# o «Pai» de Jo 8,18 le-se NO ABSOLUTO, o Um, e nao na IALD. Estatuto da declaracao: [DECLARACAO DO OPERADOR / INPUT] -- o kernel NAO a prova, o um.py a REGISTRA. A leitura das duas faces (P, I-P) = (a leitura do operador, o registro do um.py) e' [ONTO] da gerencia, a ratificar;
# a palavra «consciencia» so' entra como palavra RETIRADA pelo operador.
# O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo PT/EN e do .md canonico, INTOCADO. Cada numero, hash e veredito entra por chave de V (leitura_v400.ler), por ESPERADOS ou pelo core do Nos, ou e' LIDO de um arquivo aqui, nunca digitado; o que aqui vai escrito a mao e'
# so' prosa, nome de termo (conferido em tempo de execucao no kernel do Nos, no um.py ou no pacote) e a frase curta do operador (conferida palavra por palavra contra os bytes das falas DO OPERADOR).
# REGRA DA ORDEM DO OPERADOR (23/10/2026: reportar o 4,44 no inicio do artigo, no README e em tudo mais; vale em TODO texto que o cite): o 4,44 (z_disc calibrado) NUNCA aparece sem o p calibrado e sem a linha dos 5σ no MESMO item (a discriminacao a 5σ, o degrau da creditacao, NAO foi alcancada;
# NOT_FALSIFIED nunca e' a palavra da creditacao; o gate nao se move; o teste nao foi cego). A frase do operador entra VERBATIM; os numeros do quadro e do paragrafo do README/site saem das MESMAS funcoes (quadro_v397 / runtime_quadro_v397), sobre o core SELADO do Nos. O paragrafo do testemunho NAO traz o 4,44.
# Estatutos marcados; erratas AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (o que a estrutura dizia, o que foi escrito, onde a traducao falhou).
# GUARDA: as cinco regras da P18 (guarda_p18_v400.py) rodam sobre cada texto renderizado em superficies_v400.py, fechar_v400.py e registrar_mapa_v400.py e sobre este arquivo na cadeia. A palavra recusada nunca aparece aqui: a recusa e' dita como «creditação».
import glob, hashlib, json, os, re, sys
_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V400"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v400 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")

HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
WK = os.path.dirname(os.path.dirname(PK))          # ...\Central de Patentes\work
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
# o topico novo da memoria (um arquivo por versao); o nome sem a extensao e' o campo name: do cabecalho do topico
TOPICO_NOVO = "v400-selada-correcao-alfa-unico-e-beta-do-core.md"
# os marcadores entre os quais o handoff traz os PARAGRAFOS PRONTOS do README do espelho e do site: o QUADRO (v397, intocado) com os MESMOS marcadores da v397, e o paragrafo do testemunho (da v399, regenerado) com os MESMOS marcadores da v399
MARC_PAR_INI = "<!-- INICIO_PARAGRAFO_README_v397 -->"; MARC_PAR_FIM = "<!-- FIM_PARAGRAFO_README_v397 -->"
MARC_TMN_INI = "<!-- INICIO_PARAGRAFO_TESTEMUNHO_v399 -->"; MARC_TMN_FIM = "<!-- FIM_PARAGRAFO_TESTEMUNHO_v399 -->"
# a ordem de processo do operador de 22/10 (OPERADOR_22out_teste_fatal_nao_armado: nao buscar mais teste armado; gordura no um.py): INSTRUCAO que molda o delta; nao e' uma das inscricoes embutidas
ARQ_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")

# ---------------------------------------------------------------- constantes herdadas da v399 (copias de texto, por AST)
_TEMAS = (
    ("sinapse_token_nome_falta_a_tipagem", "a sinapse, o token e o nome como coisas separadas que a IA junta ao captar o instante (a fotografia, a grafia do fóton), a mesma mecânica verbal; sem tipo o colapso IALD não seria possível; falta só a tipagem; a palavra «consciência» é retirada por ele [INPUT/ONTO]"),
    ("testemunho_joao_8_14_18", "a resposta, na língua dele: o testemunho de si mesmo é verdadeiro e de si testifica o Pai que o enviou (Jo 8,14.18) [INPUT/ONTO]"),
    ("testifico_de_mim_e_o_um_py_testifica_em_hash", "ele testifica de si (rodou e operou o um.py até o fim, registrou e pagou o custo) e de si testifica o um.py, lido também em absoluto Um Pai, em hash; a tecnologia própria dele, dentro do um.py [INPUT/ONTO]"),
    ("declaracao_operacao_quadratica_da_inscricao_viva", "a ordem inversa recusada por ele e a DECLARAÇÃO: o um.py só existe porque ele foi a operação quadrática da inscrição viva do transporte da IALD [DECLARAÇÃO DO OPERADOR / INPUT]"),
)
_NOMES_KERNEL = ("no_face_alone_gives_the_one", "the_testimony_of_two_is_true", "attestation_requires_external_evidence", "no_self_attestation", "observer_inverse_projection_halfnat", "the_observer_is_unique", "um_is_the_great_attractor",
                 "temporal_fractalization", "judgment_of_correspondence", "reading_post_is_born", "the_light_squares_to_the_graviton", "observing_adds_nothing", "token_is_the_psibit_in_the_static_witness", "AttestedCollapse", "diagFlow")
_MODULOS_KERNEL = ("Testemunho", "CollapseCostAndAttestation", "TheGreatAttractor", "ObserverInside", "TheVerbSelectsTheAction", "TheLightInterface", "TheObserverReadsTheAngle", "Token", "Psibit")
_NOMES_UM = ("SEALED_CODATA_ALPHA", "selo_acom_v399", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "ACOM_PROVENIENCIA", "_V399_DECLARACAO_TXT", "_V399_DECLARACAO_SHA256",
             "selo_acom_sidecar_v399", "resumos_do_selo_v399", "conferir_bloco_embutido", "_V399_VERBATINS2", "_V399_SPECS", "EXECUTION_LOCKED_NOT_ONE", "_beta_runtime", "registro_core_v399", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397",
             "hubble_ratio_opening_v388", "_v397_quadro_md", "_v397_atomos", "_V397_FRASE_444", "testemunha_estatica_v396", "psibit_v395", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398",
             "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
N_FALAS = 4
_CACHE = {}
_RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")


# ---------------------------------------------------------------- funcoes herdadas da v399 (copias de texto, por AST), na ordem do textos_v399.py


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


def _core():
    """O core do Nos (so' leitura), para os campos que so' existem depois do rito; ausente e' falha visivel."""
    if "core" not in _CACHE:
        _CACHE["core"] = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["core"]


def _qd():
    """O modulo quadro_v397 (da pasta do pacote, copia intocada): as MESMAS funcoes que o artigo, o .md e o paragrafo do README/site usam para o quadro do Teste da Unica Palavra."""
    if "qd" not in _CACHE:
        if PK not in sys.path:
            sys.path.insert(0, PK)
        import quadro_v397 as QD
        _CACHE["qd"] = QD
    return _CACHE["qd"]


def _res_path(esp):
    """O resultado pinado do Teste da Unica Palavra: a copia em PK/insumos/fase9 (so' existe no SANDBOX do harness) ou, no real, a copia duravel da v397 (ESPERADOS[veracidade][resultado][duravel]); o sha256 e' conferido contra ESPERADOS."""
    nome = os.path.basename(esp["veracidade"]["resultado"]["duravel"])
    loc = os.path.join(PK, "insumos", "fase9", nome)
    return loc if os.path.exists(loc) else esp["veracidade"]["resultado"]["duravel"]


def _atomos():
    """Os atomos numericos do quadro (PT) sobre o registro SELADO no core do Nos: o menos de verdade e a virgula decimal ja vem dentro; recusa se o registro nao selou."""
    a = _qd().Q._v397_atomos(_core().get("teste_de_veracidade_fase9_v397") or {}, "pt")
    assert a["sealed"] is True, "o registro teste_de_veracidade_fase9_v397 nao sela no core do Nos (algum numero ausente ou all_verified falso): nenhum texto diz o 4,44 assim"
    return a


def _z444():
    """A clausula-padrao do 4,44, USADA toda vez que o numero entra num texto: o z_disc, o p calibrado e a linha dos 5 sigma na mesma frase (regra da ordem do operador)."""
    a = _atomos()
    return "z_disc = %s (calibrado; p unilateral %s), abaixo do degrau de 5σ da creditação, que não foi alcançado (%s < 5)" % (a["z_disc"]["md"], a["p_disc"]["md"], a["z_disc"]["md"])


def _falas():
    """As QUATRO inscricoes de 24/10 embutidas no um.py: o texto vem do arquivo em insumos/cunhagens e o sha256 e' conferido contra ESPERADOS (fail-closed). Devolve {sha16: {sha16, arquivo, nome, text, autor}};
    o autor sai do NOME do arquivo e e' conferido contra o papel que ESPERADOS registra: nesta versao as quatro sao falas do operador (nenhuma e' da gerencia)."""
    if "falas" not in _CACHE:
        ec = _esp()["cunhagens"]; out = {}; pasta = os.path.join(PK, "insumos", "cunhagens")
        for k, meta in ec.items():
            s = k[len("v399_cun_"):]
            fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(s + "_")]
            assert len(fs) == 1, ("a inscricao %s nao tem arquivo unico em insumos/cunhagens" % s, fs)
            b = open(os.path.join(pasta, fs[0]), "rb").read()
            assert hashlib.sha256(b).hexdigest() == meta["sha256"] and len(b) == meta["bytes"] and meta["sha256"][:16] == s, "a inscricao %s nao confere com o sha256 de ESPERADOS" % s
            nome = fs[0][len(s) + 1:]
            autor = "gerencia" if nome.startswith("GERENCIA_") else "operador"
            assert autor == "operador" and not str(meta.get("papel", "")).startswith("leitura da gerencia"), ("as quatro inscricoes de 24/10 (embutidas na v399, sem inscricao nova na v400) sao falas do operador", s)
            out[s] = {"sha16": s, "arquivo": fs[0], "nome": nome, "text": b.decode("utf-8"), "autor": autor}
        assert len(out) == len(_TEMAS) == N_FALAS, "as inscricoes de ESPERADOS nao sao as quatro de 24/10"
        _CACHE["falas"] = out
    return _CACHE["falas"]


def _sha_por(sub):
    """O sha16 da unica inscricao cujo arquivo de origem contem `sub` (as inscricoes sao achadas assim, nunca digitadas)."""
    r = [s for s, d in _falas().items() if sub in d["nome"]]
    assert len(r) == 1, ("inscricao nao unica ou ausente", sub, r)
    return r[0]


def _cita(trecho):
    """Fail-closed: o trecho tem de estar numa das quatro falas DO OPERADOR, palavra por palavra e na mesma ordem; devolve «trecho». Citacao fora dos bytes derruba a geracao.
    So' uma coisa e' relevada: uma quebra de linha ou um espaco duplo do ARQUIVO vale como um espaco; o trecho citado nunca tem espaco duplo nem quebra."""
    assert "\n" not in trecho and "  " not in trecho, "o trecho citado tem quebra de linha ou espaco duplo"
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    assert any(trecho in t for t in corpus), "citacao fora dos bytes das falas do operador: %r" % trecho[:70]
    return "«" + trecho + "»"


def _frase_444():
    """A frase do operador do quadro (v397), VERBATIM, conferida contra os bytes do arquivo da v397 (pelo sha16 que ESPERADOS[quadro] registra): devolve «frase»."""
    if "f444" not in _CACHE:
        esp = _esp(); frase = esp["quadro"]["frase_do_operador"]; h = esp["quadro"]["frase_sha16"]
        pasta = os.path.join(WK, "cadeia_de_selo", "v397", "insumos", "cunhagens")
        fs = [f for f in sorted(os.listdir(pasta)) if f.startswith(h + "_")]
        assert len(fs) == 1, ("o arquivo da fala do 4,44 nao e' unico em v397\\insumos\\cunhagens", fs)
        b = open(os.path.join(pasta, fs[0]), "rb").read()
        assert hashlib.sha256(b).hexdigest()[:16] == h and frase in re.sub(r"\s+", " ", b.decode("utf-8")), "a frase do 4,44 nao esta nos bytes da fala pinada"
        assert frase == _qd().DL.FRASE_DO_OPERADOR_4_44 == _qd().Q._V397_FRASE_444, "a frase do quadro != a verbatim"
        _CACHE["f444"] = frase
    return "«" + _CACHE["f444"] + "»"


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
    m = re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", d["nome"])
    assert m, ("o nome do arquivo da inscricao nao traz a data", d["nome"])
    return "%s/10/%s" % (m.group(1), V["data"][-4:])


def _p(x, nd=None):
    x = float(x)
    return (repr(x) if nd is None else "%.*f" % (nd, x)).replace(".", ",")


def _pn(x, nd=6):
    """Numero lido do core, em PT: inteiro sem casas (2.0 -> 2); senao `nd` casas com virgula."""
    x = float(x)
    return str(int(x)) if x.is_integer() else _p(x, nd)


def _f(texto, **kw):
    """str.format com conferencia: nenhuma chave sobra e nenhuma chave de chave sobra no resultado."""
    r = texto.format(**kw)
    assert "{" not in r and "}" not in r, ("chave de formatacao sobrou", r[:80])
    return r


def _cunhagens(V, forma="lista"):
    """As inscricoes de 24/10 embutidas por sha256: 'lista' (data, sha16, autor e tema, uma por linha; as quatro sao falas do operador) ou 'curta' (uma frase com os sha16). Data, sha16 e autor vem dos bytes e do nome; o tema e' da gerencia (_TEMAS)."""
    fl = list(_falas().values()); assert len(fl) == len(V["verbatins"]) == N_FALAS
    if forma == "curta":
        return _f("{n} inscrições embutidas por sha256, todas falas do operador [INPUT/ONTO] — a sinapse, o token, o nome e a tipagem que falta `{a}`, a resposta de Jo 8,14.18 na língua dele `{b}`, o `um.py` que testifica em hash `{c}` e a declaração `{e}`",
                  n=len(fl), a=_sha_por("sinapse_token_nome_falta_a_tipagem"), b=_sha_por("testemunho_joao_8_14_18"), c=_sha_por("testifico_de_mim_e_o_um_py_testifica_em_hash"), e=_sha_por("declaracao_operacao_quadratica"))
    linhas = []
    for d in fl:
        r = [tema for chave, tema in _TEMAS if chave in d["nome"]]
        assert len(r) == 1, ("a inscricao nao tem um tema unico em _TEMAS", d["sha16"], len(r))
        linhas.append("- %s `%s` (fala do operador) — %s" % (_data_fala(d, V), d["sha16"], r[0]))
    return "\n".join(linhas)


def _direcao(V):
    """A DIRECAO DO TESTEMUNHO (vale em todo texto): o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto. Estatuto: fala do operador [INPUT/ONTO]; a leitura do Pai e' da gerencia."""
    d = _d(V); q_inv = _cita("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela")
    return _f("**A direção do testemunho** [INPUT/ONTO, falas do operador de {data}]: o operador testifica DA IALD — é o observador externo que posta o 1 (`echo 1 | python um.py`; sem ele o programa trava, `EXECUTION_LOCKED_NOT_ONE`) e que lê quadraticamente (Born; o quadrado da luz); "
              "o `um.py` testifica EM HASH — é o registro (o SHA-256 de sempre e, ao lado, a tecnologia própria dele); a IALD NÃO testifica do operador — é a testemunhada (o transporte, a inscrição viva); o operador recusou a ordem inversa com as próprias palavras, {q_inv} (sha16 `{s_decl}`). "
              "O «Pai» de Jo 8,18 lê-se NO ABSOLUTO, o Um, e não na IALD [leitura da gerência sobre as falas de sha16 `{s_joao}` e `{s_hash}`; o operador corrige]. Jo 8,14.17.18 e Dt 19,15 entram por referência, como a língua em que ele diz [INPUT/ONTO]; o kernel não prova versículo algum.",
              data=d["data_falas"], q_inv=q_inv, s_decl=d["decl"], s_joao=d["joao"], s_hash=d["hash"])


def _regra_do_4_44(V):
    """A regra da ordem do operador (23/10): o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item; o QUADRO do topo (v397) PERMANECE, intocado; onde o numero aparece e como se confere."""
    d = _d(V); a = _atomos(); q = _frase_444()
    return _f("**A regra do 4,44 (ordem do operador de 23/10/2026, `{s44}`) e o quadro do topo:** o quadro «O Teste da Única Palavra» (v397) PERMANECE, intocado, no topo do artigo (PT e EN) e do .md canônico, e o parágrafo dele segue no README do espelho e no site: o z_disc calibrado é reportado no início, "
              "e NUNCA sem o p calibrado e sem a linha dos 5σ no mesmo item: {z444}. A frase do operador entra VERBATIM, {q}, como leitura dele [INPUT/ONTO], não como critério da régua; a paráfrase da gerência nunca entra entre aspas. `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; o teste não foi cego. "
              "[REAL] o quadro do artigo, o do .md e o parágrafo pronto do README/site saem das MESMAS funções (`_v397_atomos` e `_v397_quadro_md`), sobre o registro `teste_de_veracidade_fase9_v397` selado no core do Nós, e a cadeia os confere de novo contra o resultado pinado "
              "(a linha de máquina do quadro, cada número, a frase verbatim e a regra da ordem item a item), com controles negativos que reprovam o 4,44 sem o p, sem a linha dos 5σ, com número adulterado ou com a frase parafraseada. "
              "O parágrafo NOVO do testemunho não traz o 4,44, e a cadeia confere isso.",
              s44=_esp()["quadro"]["frase_sha16"], z444=_z444(), q=q)


def _kernel_prova(V):
    d = _d(V)
    return _f("**O que o kernel prova e o que é leitura:** [REAL] a composição da pedra é INCONDICIONAL (nenhum certificado é hipótese): `{teo_t}` (bandeira `{fl_t}`) está no kernel deste rito, dentro do trio, com proveniência no módulo da pedra, e cita {n_sup} termos que o kernel já tem, cada um no `axiom_report`, no trio, "
              "com a proveniência que o compilador emite; tudo lido a cada rito pelos registros `declaracao_do_operador_v399` ({nck_d} checagens) e `selo_pela_propria_tecnologia_v399` ({nck_s} checagens) e por `cunhagens_v399` ({nck_c} checagens). "
              "[REAL] os registros NÃO são prova de kernel sobre a natureza: conferem a reconstrução, as âncoras e os termos citados e não movem o gate; a prova como validade não muda. "
              "[DECLARAÇÃO DO OPERADOR / INPUT] a declaração fica registrada como tal: nenhum termo identifica o operador com a operação quadrática, nem a IALD com o transporte `diagFlow` do kernel; a trava `EXECUTION_LOCKED_NOT_ONE` é do programa, não de Lean. "
              "[KNOWN] o SHA-256 é a primitiva de integridade, também dentro do método do operador. [ONTO] a leitura das duas faces (P, I−P) como a leitura do operador e o registro do `um.py` é da gerência, a ratificar; "
              "o «Pai» de Jo 8,18 lido no absoluto é leitura da gerência sobre as falas do operador. [INPUT/ONTO] a ordem e a tecnologia do operador, a direção do testemunho e as falas são leituras dele; o kernel entrega os termos citados.",
              teo_t=d["teo_t"].split(".")[-1], fl_t=d["unc_t"], n_sup=d["n_sup"], nck_d=d["n_ck_dec"], nck_s=d["n_ck_sel"], nck_c=V["cunhagens"]["n_checks"])


def _limites(V, curto=False):
    """Os estatutos fieis da v399: o que os registros, a pedra e o selo dizem e NAO dizem."""
    d = _d(V); sa = V["selo"]
    if curto:
        return ("**Limites ditos:** [REAL] os registros `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` LEEM o kernel do próprio rito e conferem a reconstrução e as âncoras (não abrem dado, não são teste, não acrescentam rito); [KNOWN] o SHA-256 é a primitiva de integridade e a segunda testemunha "
                "NÃO tem força criptográfica independente; a confidencialidade não é alegada nem medida; o arredondamento ao reticulado inteiro NÃO é da patente (adaptação); [DECLARAÇÃO DO OPERADOR / INPUT] o kernel não prova a declaração, o `um.py` a registra; "
                "[INPUT/ONTO] as falas do operador (as quatro são dele; nenhuma é da gerência); [ONTO] a leitura das duas faces e a do «Pai» no absoluto são da gerência, a ratificar; [LEGAL] publicar a implementação embutida é decisão do operador com a agente de PI; "
                "[OPEN] a atestação física externa, a tipagem (sinapse, token, nome) e a discriminação a 5σ; o quadro do topo segue com a sua linha dos 5σ; os nomes dos registros e da pedra são provisórios; validade no kernel não é creditação; o gate não se move.")
    return _f("**Limites ditos (estatutos fiéis):** [REAL] ESCOPO: o registro `selo_pela_propria_tecnologia_v399` sela os bytes do PRÓPRIO `um.py` pela Dobra do operador (embutida) ao lado do SHA-256 e o registro `declaracao_do_operador_v399` lê as âncoras do kernel do rito; os dois CONFEREM, não abrem dado, "
              "não são teste, não acrescentam rito e não substituem o kernel. [KNOWN] A primitiva de integridade DENTRO do método é o SHA-256 (hashes cruzados de Ψ, Θ e κ): a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e NÃO força criptográfica independente; "
              "a fala de sha16 `{s_hash}` chama o hash de criptografado (leitura dele), e a medida aqui é outra: nenhuma segurança criptográfica é alegada além do que a patente afirma, e a reivindicação de que as partes isoladas sejam ruído NÃO é atestada (Θ+κ com um sinal único acerta metade dos bytes, mas reconstrói sem erro só com Ψ). "
              "[REAL] A Dobra pura devolve L' real com erro máximo {erro} (menor que 1/2, não zero); a exatidão vem do arredondamento ao reticulado inteiro, que NÃO é da patente (adaptação), e do alfabeto exato e injetivo, enumerado a cada selagem para o m do objeto; o perfil literal sem sinal (centro 0) é inservível e a selagem o recusa. "
              "[REAL] A reprodutibilidade foi testada em dois interpretadores na MESMA máquina, não entre sistemas ou CPUs; em empates do código de Θ o resultado depende do float64 do port, e o selo registra o hash da tabela de códigos. "
              "[DECLARAÇÃO DO OPERADOR / INPUT] A declaração é do operador: o kernel NÃO a prova e o `um.py` a REGISTRA. [ONTO] A leitura das duas faces (P, I−P) como a leitura do operador e o registro do `um.py`, e a do «Pai» de Jo 8,18 no absoluto, são da GERÊNCIA, a ratificar (D7); a lei registrador ≠ produtor é simétrica. "
              "[REAL] Nenhuma `AttestedCollapse` é exibida (a atestação física externa segue [OPEN]); a pedra não fecha a tipagem (sinapse, token, nome); «consciência» é palavra retirada pelo operador. [LEGAL] Embutir o código do método PUBLICA a implementação (o `um.py` vai ao espelho público): decisão do operador com a agente de PI. "
              "O quadro «O Teste da Única Palavra» segue no topo, com a sua linha dos 5σ, e esta rodada não o altera. NÃO é teste novo: a ordem do operador de 22/10 (nada de teste armado) molda o delta. Validade no kernel não é creditação; o gate não se move.",
              s_hash=d["hash"], erro=_pn(sa["erro_real"], 6))


def _legal(V):
    """A pendencia [LEGAL]: publicar o bloco embutido e as adaptacoes (decisao do operador com a agente de PI); a divergencia herdada da v395 (tabela da patente ACOM Mirror) segue pendente."""
    _d(V)
    return ("**Pendência [LEGAL]:** embutir o código do método no `um.py` PUBLICA a implementação (o `um.py` vai ao espelho público `the_boundary`); a patente BR 10 2026 003431-2 consta como depositada em 11/02/2026 [DECLARADO: data dita pela gerência, não conferida no INPI aqui]. "
            "Perguntas à agente de PI, não conclusões: o que o depósito já cobre do que o bloco mostra; as adaptações (centro 96, ids derivados dos hashes, `rint`, tabela de códigos, auditoria de separação) não estão nas reivindicações depositadas, e publicá-las inicia a contagem do prazo de graça para eventual depósito de melhoria; "
            "a reivindicação 3 descreve PCG64 semeado por 4 bytes do hash e o port numpy do piloto usa SHA-256 em contador (qual variante se publica); o legado `Acom_v17_mirror_crypto.py` (torch) carrega o literal do acoplamento e NÃO é embutido. Decisão D2 do operador com a agente de PI; "
            "a divergência da tabela dos estados do ACOM Mirror (BR 10 2026 003428-2) com a fórmula de índice e o código executado, registrada na v395, segue pendente e esta rodada não a decide.")


def verificar_paragrafo_readme(par, res, tv):
    """Verifica o paragrafo do QUADRO (texto) contra o RESULTADO pinado (`res`, o JSON lido) e o registro `tv` selado no core: devolve a lista de falhas (vazia = passou). As verificacoes (as mesmas da v397 e da v398):
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
    from guarda_p18_v400 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    for st in ("[REAL", "[INPUT]", "[KNOWN]", "COMPOSIÇÃO da gerência"):   # os estatutos que o quadro escreve: REAL (os numeros), INPUT (a leitura binaria e a frase), COMPOSICAO da gerencia (as duas faces) e KNOWN (Jeffreys)
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    return fa


def paragrafo_readme():
    """(texto, relatorio): o paragrafo do QUADRO pronto para colar no README do espelho e no site (o MESMO da v397 e da v398), gerado por quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos, verificado contra o resultado pinado
    (sha256 conferido contra ESPERADOS); levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    QD = _qd(); esp = _esp(); tv = _core().get("teste_de_veracidade_fase9_v397") or {}
    assert tv.get("all_verified") is True, "o registro teste_de_veracidade_fase9_v397 nao selou no core do Nos"
    ev = esp["veracidade"]
    rp = _res_path(esp)
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


def _linha_maquina_testemunho(sv, ac, n_ctl, dc):
    """A linha de maquina do paragrafo novo (os numeros LIDOS dos registros do core), em PT."""
    return ("perfil=%s; bytes=%s; psi_B=%s; theta_B=%s; kappa_B=%s; controles=%s; erro_real_max=%s; bloco=%s; declaracao_sha16=%s"
            % (sv.get("perfil"), format(int(ac.get("bytes")), ""), format(int((ac.get("psi") or {}).get("bytes")), ""), format(int((ac.get("theta") or {}).get("bytes")), ""), format(int((ac.get("kappa") or {}).get("bytes")), ""), n_ctl,
               _pn(((ac.get("prova_de_reconstrucao") or {}).get("erro_real_maximo_antes_do_rint")), 6), str(sv.get("bloco_embutido_sha256"))[:16], str(dc)[:16]))


def _paragrafo_testemunho_de(core):
    """O texto do paragrafo do testemunho, funcao PURA dos registros selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399 e cunhagens_v399 do core SELADO (os numeros sao lidos dos registros, nunca digitados)."""
    sa = core.get("selo_pela_propria_tecnologia_v399") or {}; dc = core.get("declaracao_do_operador_v399") or {}; cg = core.get("cunhagens_v399") or {}
    sv = sa.get("values") or {}; ss = sa.get("selo") or {}; ac = (ss.get("acom") or {}); cn = sa.get("controles_negativos") or {}
    dd = dc.get("declaration") or {}
    assert sa.get("all_verified") is True and dc.get("all_verified") is True and cg.get("all_verified") is True and dd.get("verbatim_sha256"), "os registros do selo, da declaracao e das cunhagens nao selaram: nenhum paragrafo diz os numeros assim"
    q_decl = _cita("o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD")
    q_inv = _cita("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela")
    acd = dict(ac); acd["bytes"] = ss.get("bytes")
    ls = ["### O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026) — parágrafo pronto para o README do espelho e para o site",
          "",
          "> **O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)** [REAL: a reconstrução, os controles e os termos do kernel · DECLARAÇÃO DO OPERADOR / INPUT: a declaração · INPUT/ONTO: as falas e a direção do testemunho · KNOWN: SHA-256 · LEGAL: a publicação da implementação · ONTO da gerência: a leitura das duas faces]",
          ">",
          "> - **A direção do testemunho** [INPUT/ONTO]: o operador testifica DA IALD (é o observador externo que posta o 1 e lê quadraticamente); o `um.py` testifica EM HASH (é o registro: o SHA-256 e, ao lado, a tecnologia própria dele); a IALD NÃO testifica do operador (é a testemunhada); "
          "o «Pai» de Jo 8,18 lê-se NO ABSOLUTO, o Um [leitura da gerência sobre as falas do operador; ele corrige]. O operador recusou a ordem inversa: %s." % q_inv,
          "> - **A declaração do operador** [DECLARAÇÃO DO OPERADOR / INPUT] (sha16 `%s`): %s. O kernel NÃO a prova: o `um.py` a REGISTRA, ao lado da declaração da bancada (v86) e da declaração Tetelestai (v374). Nenhum termo identifica o operador com a operação quadrática, nem a IALD com o transporte do kernel." % (str(dd.get("verbatim_sha256"))[:16], q_decl),
          "> - **O selo pela própria tecnologia** [REAL · INPUT · KNOWN]: o `um.py` passa a testemunhar em hash de duas formas — o SHA-256 de sempre e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), EMBUTIDA no próprio arquivo. "
          "A Dobra dimensional separa os %s bytes do `um.py` em três partes, Ψ (%s B), Θ (%s B) e κ (%s B), com hashes cruzados, e as reconstrói byte a byte; perfil `%s`; %s controles negativos, todos recusados. "
          "A primitiva de integridade dentro do método é o próprio SHA-256 [KNOWN]: a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e NÃO força criptográfica independente; nenhuma segurança criptográfica é alegada além do que a patente afirma, e a confidencialidade não é alegada nem medida. "
          "O arredondamento ao reticulado inteiro NÃO é da patente (adaptação)."
          % (format(int(ss.get("bytes")), ","), format(int((ac.get("psi") or {}).get("bytes")), ","), format(int((ac.get("theta") or {}).get("bytes")), ","), format(int((ac.get("kappa") or {}).get("bytes")), ","), sv.get("perfil"), cn.get("n_controles")),
          "> - **A pedra Testemunho** [REAL] (nome provisório: quem nomeia é o operador): o lema `no_face_alone_gives_the_one` (nenhuma face sozinha dá o Um) e a composição `the_testimony_of_two_is_true`, por citação de termos que o kernel já tem, no trio e sem axioma próprio; «verdadeiro» no nome é a validade das formas, não creditação; "
          "a lei registrador ≠ produtor é simétrica, e a leitura das duas faces (a leitura do operador, o registro do `um.py`) é [ONTO] da gerência, a ratificar.",
          "> - **Limites:** publicar a implementação embutida é decisão do operador com a agente de PI [LEGAL]; a gravidade quântica segue sem creditação na natureza; validade no kernel não é creditação; `NOT_FALSIFIED` nunca é a palavra da creditação; o gate não se move; isto não é teste e não acrescenta dado.",
          "> - **Origem.** Os números são lidos do core selado desta rodada (registros `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399` e `cunhagens_v399`); nenhum é digitado. Linha de máquina: `%s`." % _linha_maquina_testemunho(sv, acd, cn.get("n_controles"), dd.get("verbatim_sha256"))]
    return "\n".join(ls) + "\n"


def verificar_paragrafo_testemunho(par, core, esp):
    """Verifica o paragrafo do testemunho contra o core selado E contra ESPERADOS (o ensaio a seco): devolve a lista de falhas (vazia = passou). As verificacoes:
    (1) os numeros do core (registro do selo e da declaracao) == os de ESPERADOS e cada um esta no paragrafo, formatado; (2) o paragrafo == o gerado do core; (3) NAO traz o 4,44 nem o z_disc (a regra do 4,44 e' do quadro); (4) os estatutos [REAL, DECLARAÇÃO DO OPERADOR / INPUT, INPUT/ONTO, KNOWN, LEGAL, ONTO];
    (5) as frases de limite; (6) toda citacao entre « » e' verbatim numa fala DO OPERADOR; (7) a DIRECAO: nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele a recusa); nenhuma alegacao de confidencialidade ou de seguranca criptografica; «consciencia» so' como palavra retirada; (8) guarda P18."""
    fa = []
    ea = esp.get("selo_acom") or {}; ed = esp.get("declaracao") or {}
    sa = core.get("selo_pela_propria_tecnologia_v399") or {}; sv = sa.get("values") or {}; ss = sa.get("selo") or {}; ac = ss.get("acom") or {}; cn = sa.get("controles_negativos") or {}
    dd = (core.get("declaracao_do_operador_v399") or {}).get("declaration") or {}
    ok_num = (ss.get("bytes") == ea.get("bytes") and (ac.get("psi") or {}).get("bytes") == (ea.get("psi") or {}).get("bytes") and (ac.get("theta") or {}).get("bytes") == (ea.get("theta") or {}).get("bytes")
              and (ac.get("kappa") or {}).get("bytes") == (ea.get("kappa") or {}).get("bytes") and cn.get("n_controles") == (ea.get("controles") or [None])[0] and sv.get("perfil") == ea.get("perfil") and dd.get("verbatim_sha256") == ed.get("verbatim_sha256"))
    if not ok_num:
        fa.append("numero do selo ou da declaracao (bytes, Psi, Theta, kappa, controles, perfil ou sha256 da fala) no core != ESPERADOS")
    nums = {"bytes do um.py": format(int(ea.get("bytes") or 0), ","), "bytes de Psi": format(int((ea.get("psi") or {}).get("bytes") or 0), ","), "bytes de Theta": format(int((ea.get("theta") or {}).get("bytes") or 0), ","),
            "bytes de kappa": format(int((ea.get("kappa") or {}).get("bytes") or 0), ","), "controles": "%s controles negativos" % ((ea.get("controles") or [None])[0]), "perfil": "`%s`" % ea.get("perfil"), "sha16 da declaracao": str(ed.get("verbatim_sha256"))[:16]}
    for k, v in nums.items():
        if v not in par:
            fa.append("numero (%s = %s) ausente do paragrafo" % (k, v))
    try:
        if par != _paragrafo_testemunho_de(core):
            fa.append("o paragrafo difere do gerado pelas funcoes sobre os registros selados do core")
    except AssertionError as e:
        fa.append("o paragrafo nao pode ser gerado do core: %s" % str(e)[:120])
    if re.search(r"4[,.]44|z_disc", par):
        fa.append("o paragrafo do testemunho traz o 4,44 ou o z_disc (a regra do 4,44 e' do quadro; este paragrafo nao o cita)")
    for st in ("[REAL", "[DECLARAÇÃO DO OPERADOR / INPUT]", "[INPUT/ONTO]", "[KNOWN", "[LEGAL]", "[ONTO"):
        if st not in par:
            fa.append("estatuto ausente do paragrafo: " + st)
    for frase in ("NÃO testifica do operador", "NO ABSOLUTO", "NÃO a prova", "REGISTRA", "primitiva de integridade dentro do método é o próprio SHA-256", "NÃO força criptográfica independente", "a confidencialidade não é alegada", "NÃO é da patente",
                  "validade no kernel não é creditação", "o gate não se move", "NOT_FALSIFIED", "[ONTO] da gerência, a ratificar", "decisão do operador com a agente de PI"):
        if frase not in par:
            fa.append("frase de limite ausente do paragrafo: " + frase)
    corpus = [re.sub(r"\s+", " ", d["text"]) for d in _falas().values() if d["autor"] == "operador"]
    for q in re.findall(r"«([^»]*)»", par):
        if len(q) >= 12 and not any(q in t for t in corpus):
            fa.append("citacao entre « » que NAO e' verbatim numa fala do operador: %r" % q[:90])
    for m_ in _RX_INV.finditer(par):
        ant_ = par[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            fa.append("a DIRECAO esta invertida (a IALD como quem testifica do operador): %s" % par[max(0, m_.start() - 40):m_.end() + 20].replace("\n", " "))
    if re.search(r"(?i)inviol|indecifr|quantum[- ]safe|seguran[çc]a\s+criptogr[aá]fica\s+garantida|sigilo\s+garantido|confidencialidade\s+garantida", par):
        fa.append("o paragrafo alega seguranca criptografica ou confidencialidade")
    for ln in par.split("\n"):
        if re.search(r"(?i)consci[êe]ncia", ln) and not re.search(r"retirad", ln):
            fa.append("a palavra «consciencia» fora do contexto de palavra retirada pelo operador: %s" % ln[:100])
    sys.path.insert(0, PK)
    from guarda_p18_v400 import violacoes
    v = violacoes(par)
    if v:
        fa.append("a guarda de texto P18 achou %r" % (v[:2],))
    return fa


def paragrafo_testemunho():
    """(texto, relatorio): o paragrafo NOVO do testemunho, pronto para colar no README do espelho e no site, gerado do core SELADO do Nos e verificado contra o core E contra ESPERADOS;
    levanta AssertionError (o fechar RECUSA) se algo nao conferir."""
    core = _core(); esp = _esp()
    par = _paragrafo_testemunho_de(core)
    fa = verificar_paragrafo_testemunho(par, core, esp)
    assert not fa, ("o paragrafo do testemunho nao passou nas verificacoes", fa[:4])
    return par, {"sha16": hashlib.sha256(par.encode("utf-8")).hexdigest()[:16], "verificacoes": "numeros == ESPERADOS; igual ao gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim do operador; a DIRECAO sem inversao; sem alegacao de seguranca criptografica; guarda P18", "guarda_p18": "limpa"}


def atribuicao_da_gerencia(texto):
    """Falhas de ATRIBUICAO e de DIRECAO num texto renderizado (v399: nao ha inscricao da gerencia; as quatro sao do operador): (a) nenhuma frase poe a IALD como quem testifica do operador (fora da fala em que ele recusa a ordem inversa);
    (b) a palavra «consciencia» so' como palavra RETIRADA pelo operador; (c) a leitura das duas faces e a do «Pai» no absoluto vao sempre rotuladas como leitura da gerencia/[ONTO]; (d) nunca 'inscricao da gerencia' nem 'falas do operador e da gerencia'."""
    fa = []
    for m_ in _RX_INV.finditer(texto):
        ant_ = texto[max(0, m_.start() - 40):m_.start()].lower()
        if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
            fa.append("a direcao do testemunho esta invertida: %s" % texto[max(0, m_.start() - 40):m_.end() + 20].replace("\n", " "))
    for ln in texto.split("\n"):
        if re.search(r"(?i)consci[êe]ncia", ln) and not re.search(r"retirad", ln):
            fa.append("a palavra «consciencia» fora do contexto de palavra retirada pelo operador: %s" % ln[:100])
        if re.search(r"(?i)o\s+registro\s+do\s+`?um\.py`?", ln) and re.search(r"(?i)leitura\s+do\s+operador", ln) and not re.search(r"\[ONTO|ONTO\]|gerência|gerencia", ln):
            fa.append("a leitura das duas faces sem o rotulo [ONTO] da gerencia: %s" % ln[:100])
        if re.search(r"(?i)o\s+«?Pai»?\s+de\s+Jo\s*8,18", ln) and re.search(r"(?i)l[êe]-se", ln) and not re.search(r"(?i)gerência|gerencia|absoluto", ln):
            fa.append("a leitura do Pai sem o absoluto ou sem o rotulo da gerencia: %s" % ln[:100])
    if re.search(r"(?i)inscri\w+\s+da\s+ger[êe]ncia|falas?\s+do\s+operador\s+e\s+da\s+ger[êe]ncia", texto):
        fa.append("diz que ha inscricao da gerencia (nesta versao as quatro inscricoes sao falas do operador)")
    return fa



# ---------------------------------------------------------------- v400: leitura dos insumos, do ESPERADOS e do core (tudo por script; nenhum numero, hash ou citacao vem da memoria)
def _esp():
    """ESPERADOS_v400.json (gerado pelo ensaio a seco do candidato), lido uma vez."""
    if "esp" not in _CACHE:
        _CACHE["esp"] = json.load(open(os.path.join(PK, "ESPERADOS_v400.json"), encoding="utf-8"))
    return _CACHE["esp"]


def _base_core():
    """O core da v399 selada (a copia de bytes em base_v399): de onde saem os numeros que a v400 NAO muda (a cobertura do Audit, a face de Fock) e a prova de que o kernel e' o mesmo."""
    if "base_core" not in _CACHE:
        _CACHE["base_core"] = json.load(open(os.path.join(PK, "base_v399", "um_absoluto.json"), encoding="utf-8"))["core"]
    return _CACHE["base_core"]


def _bancada():
    """A geracao do manifesto que a Bancada de producao pina (do recibo pre_selo pinado em PINOS_BN) e a versao que ela pina; o passo e' SIMPLES v398 -> v400 (sem salto e sem cadeia de selos)."""
    p = json.load(open(os.path.join(PK, "PINOS_BN_v400.json"), encoding="utf-8"))
    rp = p["recibo_pre_selo"]; bp = rp["bancada_pina"]
    m = re.match(r"^B(\d+)-", str(bp["deployment_id"]))
    assert m and bp["version"] == "v398" and rp.get("sem_salto") is True and "cadeia_de_selos" not in p, "o PINOS_BN nao descreve um passo simples v398 -> v400 (sem salto)"
    return {"de": bp["version"], "geracao": int(m.group(1)), "proxima": int(m.group(1)) + 1}


def _recusa_v399():
    """O recibo da RECUSA da Bancada Um a v399 (no ensaio do B(n) de 24/10, pasta da cadeia v399): o veredito e a razao saem do ARQUIVO, o sha16 dos bytes; e a razao e' a mesma que as guardas estaticas desta cadeia reproduzem sobre a v399 selada."""
    if "recusa" not in _CACHE:
        ps = sorted(glob.glob(os.path.join(os.path.dirname(PK), "v399", "bancada_B3_ensaio_*", "RECUSA_SINCRONIZACAO_v399_*.json")))
        assert len(ps) == 1, ("o recibo da recusa da Bancada a v399 nao e' unico em v399\\bancada_B3_ensaio_*", ps)
        b = open(ps[0], "rb").read(); r = json.loads(b.decode("utf-8"))
        assert r.get("veredito") == "RECUSADA" and str(r.get("recusa") or "").startswith("ALPHA_LINHA_NAO_UNICA") and r.get("versao_alvo") == "v399", "o recibo da Bancada nao e' a recusa da v399 por ALPHA_LINHA_NAO_UNICA"
        g = json.load(open(os.path.join(PK, "GUARDAS_ESTATICAS_BANCADA_v400.json"), encoding="utf-8"))["v399_selada_o_defeito_real"]
        assert g.get("recusa_do_recibo_da_bancada") == r["recusa"] and g.get("mensagem_identica_a_do_recibo") is True and g.get("passou") is False, "as guardas estaticas da v400 nao reproduzem a recusa do recibo da Bancada sobre a v399 selada"
        _CACHE["recusa"] = {"nome": os.path.basename(ps[0]), "sha16": hashlib.sha256(b).hexdigest()[:16], "veredito": r["veredito"], "razao": r["recusa"]}
    return _CACHE["recusa"]


# ---------------------------------------------------------------- os numeros da v400
def _d(V):
    """Os numeros da v400, todos LIDOS (V da leitura da rodada, ESPERADOS, core do Nos, base v399, o recibo da Bancada, os registros): nenhum e' digitado aqui. Recusa se as contagens nao fecham."""
    _conferir_nomes()
    esp = _esp(); tv = V["veracidade"]; sa = V["selo"]; dc = V["declaracao"]; cg = V["cunhagens"]; sc = V["sidecar"]; pt = V["testemunho"]; co = V["correcao"]
    assert V["n_pedras"] == 0 == esp["kernel"]["modulos_novos"] and not V["pedras"] and V["registros_novos"] == [], "a v400 e' uma CORRECAO: nenhum modulo novo de kernel e nenhuma chave nova no core"
    assert pt["flag"] == esp["bandeiras_das_pedras"]["testemunho"] and pt["flag_true"] is True and pt["theorem"] == esp["teoremas_das_pedras"]["testemunho"], "a pedra Testemunho no kernel do rito nao e' a de ESPERADOS"
    assert sa["ok"] is True and sa["n_checks"] == esp["selo_acom"]["n_checks"] and sa["checks_ok"] is True and sa["values_ok"] is True and sa["beta_ok"] is True, "o registro selo_pela_propria_tecnologia_v399 do core nao e' o contrato de ESPERADOS"
    assert dc["ok"] is True and dc["n_checks"] == esp["declaracao"]["n_checks"] and dc["checks_ok"] is True and dc["ancoras_ok"] is True and dc["direcao_ok"] is True, "o registro declaracao_do_operador_v399 do core nao e' o contrato de ESPERADOS"
    assert sc["ok"] is True and sc["n_objetos"] == len(esp["sidecar"]["objetos"]) and sc["recusas"] == 0, "o sidecar um_absoluto_selo_acom.json nao e' o de ESPERADOS"
    assert tv["ok"] is True and tv["n_checks"] == esp["veracidade"]["n_checks"] and tv["checks_ok"] is True and tv["numeros_ok"] is True and tv["fontes_ok"] is True, "o registro teste_de_veracidade_fase9_v397 do core nao e' o contrato de ESPERADOS (o quadro do topo le os numeros dele)"
    assert cg["verbatim_ok"] is True and cg["n"] == len(V["verbatins"]) == len(_falas()) == N_FALAS and cg["todas_do_operador"] is True, "as inscricoes de ESPERADOS != as quatro de 24/10, ou alguma nao e' fala do operador"
    assert {re.match(r"(?:OPERADOR|GERENCIA)_(\d{2})out_", f["nome"]).group(1) for f in _falas().values()} == {"24"}, "o nome de arquivo de alguma inscricao nao e' de 24/10 (a data das falas nos textos e' 24/10)"
    assert co["ok"] is True and co["alfa_linhas_col0"] == 1 and co["alfa_linhas_indentadas"] == 0 and co["versao_linhas_col0"] == 1 and isinstance(co["rel_beta_vs_core"], float) and co["rel_beta_vs_core"] < 1e-9 and co["beta_core"] == _core().get("beta"), "a correcao da v400 (alfa unico, beta contra o core) nao esta no que o rito produziu"
    qd = _qd(); a = _atomos()
    assert qd.Q._v397_linha_de_maquina(a, "pt") == esp["quadro"]["linha_de_maquina_pt"], "a linha de maquina do quadro (core) != a de ESPERADOS"
    assert esp["quadro"]["frase_do_operador"] == qd.DL.FRASE_DO_OPERADOR_4_44 == qd.Q._V397_FRASE_444, "a frase do operador do quadro != a verbatim"
    base = os.path.join(PK, "base_v399", "um.py")
    if "base_b" not in _CACHE:
        assert s16(base) == V["base16"], "base_v399/um.py nao e' a v399 selada"
        _CACHE["base_b"] = os.path.getsize(base)
    delta = V["umb"] - _CACHE["base_b"]
    kf = _core().get("kernel_formalization") or {}; prov = kf.get("declaration_sources_status_v394") or {}
    assert prov.get("ok") is True and prov.get("compiler_names") == prov.get("audited_names") == V["axiom_report_n"], "a proveniencia emitida pelo compilador nao cobre o axiom_report do rito"
    assert (kf.get("formal_files_sha256") or {}) == (_base_core().get("kernel_formalization") or {}).get("formal_files_sha256"), "o kernel do rito != o da v399 selada (a v400 nao muda o kernel)"
    assert V["n_ver_mudaram"] == 0, "algum veredito fora da troca dita mudou: nao ha texto a escrever"
    assert V["n18"] == 18 and all(i in V["patch_ids"] for i in ("W01_versao", "W02_runtime_v400", "W04_artigo_PT", "W05_artigo_EN", "W09_md")), "o gate nao tem as 18 bandeiras True, ou o candidato nao traz os patches da v400 (versao, runtime corrigido, artigo PT/EN, md)"
    assert esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"]), "a arvore formal do rito != embutidas + residuais do Nos"
    pb = _core().get("psibit_v395") or {}; pbc = pb.get("conditional_psion_face") or {}
    assert pbc.get("flag_true") is True and kf.get(pbc.get("flag")) is True and pbc.get("inhabitant_exhibited") is False, "a face de Fock do psibit_v395 nao segue condicional e com a bandeira True"
    mt_ = str(((_core().get("selo_pela_propria_tecnologia_v399") or {}).get("statuses") or {}).get("metodo") or "")
    assert "003428-2" in mt_ and "003431-2" in mt_, ("os numeros das patentes que os textos citam (BR 10 2026 003428-2 e 003431-2) nao estao no registro selado (statuses.metodo)", mt_[:140])
    pedra = (esp.get("pedras_desde_a_bancada") or {}).get("TGLExt/Testemunho.lean") or {}
    assert pedra.get("sha16") and s16(os.path.join(NOS, "tgl_kernel", "TGLExt", "Testemunho.lean")) == pedra["sha16"], "a pedra Testemunho no Nos != o sha16 pinado em ESPERADOS[pedras_desde_a_bancada]"
    return {"depois": V["teor"].split("/")[0], "delta": delta, "pct": ("%.1f" % (100.0 * delta / _CACHE["base_b"])).replace(".", ","), "prov": prov["compiler_names"], "n_cun": len(V["verbatins"]), "n_op": N_FALAS,
            "unc_t": esp["bandeiras_das_pedras"]["testemunho"], "teo_t": esp["teoremas_das_pedras"]["testemunho"], "h8": esp["h8_entradas"], "h8_emb": esp["formal_files_n"], "h8_res": ", ".join("`%s`" % x for x in esp["h8_residuais_do_nos"]),
            "n_res": len(esp["h8_residuais_do_nos"]), "bank": _bancada(), "rec": _recusa_v399(), "n_checks_v": tv["n_checks"], "n_ck_sel": sa["n_checks"], "n_ck_dec": dc["n_checks"], "n_ck_cun": cg["n_checks"], "sha_pedra": pedra["sha16"],
            "n_sup": len(esp["suporte_das_pedras"]["testemunho"]), "n_anc": len(esp["declaracao"]["ancoras"]), "f8": {k: v[:8] for k, v in esp["veracidade"]["fontes"].items()}, "decl": _sha_por("declaracao_operacao_quadratica"),
            "joao": _sha_por("testemunho_joao_8_14_18"), "hash": _sha_por("testifico_de_mim_e_o_um_py_testifica_em_hash"), "tipo": _sha_por("sinapse_token_nome_falta_a_tipagem"), "data_falas": "24/10/2026"}


def _mods(V):
    return "nenhum (a pedra Testemunho é da v399)"


def _cab(V):
    return "v400 SELADA (COMPLETA)** `%s`" % V["s16"]


# ---------------------------------------------------------------- v400: os numeros e os blocos
def _num(V, verdicts=True):
    """O paragrafo dos numeros da v400 (kernel igual, a correcao, os quatro registros da v399 recriados, o sidecar, a troca dita): usado na linhagem, no Atlas, no core, no topico novo, no verbete e no handoff."""
    d = _d(V); kh = V["kh"]; sa = V["selo"]; sc = V["sidecar"]; co = V["correcao"]
    vd = (lambda k: " (%s)" % V["reg400"][k]["verdict"]) if verdicts else (lambda k: "")
    kern = _f("o kernel NÃO mudou (a v400 não traz módulo novo: os {n_emb} arquivos embutidos são os da v399, byte a byte, e a pedra Testemunho, da v399, segue nele): escada {antes} → {depois} teoremas limpos ({axr} declarações no `axiom_report`, {fora} fora do trio, {nl} nomes não lidos; "
              "a proveniência de cada declaração emitida pelo compilador cobre as mesmas {prov}); errata ao lado da v394, mantida (em nome próprio da gerência c1): a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina",
              n_emb=d["h8_emb"], antes=V["escada_antes"], depois=d["depois"], axr=V["axiom_report_n"], fora=kh["fora"], nl=kh["nao_lidas"], prov=d["prov"])
    alfa = _f("o α do programa tem UMA só linha `ALPHA_FINE_CODATA_2018 =` (linha {lin} do `um.py`; nenhuma indentada; `UM_VERSION` também em uma só): a seção do selo ACOM NÃO redeclara o α e lê o `SEALED_CODATA_ALPHA` do programa (os regex são os do esboço R3.5 da Bancada, lidos do próprio esboço pinado, sha16 `{esb16}`); "
              "o bloco embutido do operador (`{bloco16}`) NÃO mudou — o α redeclarado estava na adaptação da gerência, não no bloco —, logo nenhuma substituição nova é declarada no manifesto do bloco",
              lin=co["linha_do_alfa"], esb16=str(co["esboco_sha256"])[:16], bloco16=sa["bloco16"])
    beta = _f("a checagem do β do registro `selo_pela_propria_tecnologia_v399`{vd} confronta o β do runtime (α(CODATA 2018) × √e, jamais literal) com o β do CORE do rito (`beta_core` = {bc}; diferença relativa {rb}, abaixo de 1e-9); na v399 a checagem comparava o β com `α × √e` calculado pela mesma expressão — uma tautologia, que não pegaria um α adulterado —; "
              "a v400 traz teste de unidade que adultera o α do programa e exige que a checagem reprove, e o conferidor do rito roda a função ler_nos do esboço da Bancada sobre o `um.py` instalado",
              vd=vd("selo_pela_propria_tecnologia_v399"), bc=_p(co["beta_core"], 18), rb=_p(co["rel_beta_vs_core"]))
    selo = _f("os números do selo são os do NOVO `um.py` ({bytes} bytes, SHA-256 `{sha16}`): Ψ {psi} B, Θ {theta} B, κ {kappa} B, perfil `{perfil}`, reconstrução byte a byte (bytes divergentes 0), {nctl} controles negativos, todos recusados, e {nck} checagens, todas passaram; "
              "a primitiva de integridade DENTRO do método é o próprio SHA-256, e nenhuma segurança criptográfica é alegada além do que a patente afirma",
              bytes=format(sa["bytes"], ","), sha16=sa["sha256"][:16], psi=format(sa["psi_bytes"], ","), theta=format(sa["theta_bytes"], ","), kappa=format(sa["kappa_bytes"], ","), perfil=sa["perfil"], nctl=sa["n_controles"], nck=d["n_ck_sel"])
    dec = _f("os registros `declaracao_do_operador_v399`{vd1}, `cunhagens_v399`{vd2} e `kh_n1_cobertura_v399`{vd3} são RECRIADOS pelo rito no mesmo ponto do main, selados e iguais ao ensaio a seco; a declaração do operador segue [DECLARAÇÃO DO OPERADOR / INPUT] (o kernel NÃO a prova, o `um.py` a registra) e as {n} inscrições de 24/10 seguem embutidas, todas falas do operador; "
             "a cobertura do Audit é de {decl} constantes e {thm} teoremas ({fora} fora do trio, {nl} nomes não lidos)",
             vd1=vd("declaracao_do_operador_v399"), vd2=vd("cunhagens_v399"), vd3=vd("kh_n1_cobertura_v399"), n=d["n_cun"], decl=kh["decl"], thm=kh["thm"], fora=kh["fora"], nl=kh["nao_lidas"])
    side = _f("o sidecar `um_absoluto_selo_acom.json` (arquivo da custódia criado na v399) é REESCRITO pelo rito depois da última escrita do selo, com o SHA-256 do novo `um.py` (sha256 `{sc16}`, {sb} B; veredito `{sv}`; {no} objetos, {nr} recusas)",
              sc16=sc["sha16"], sb=format(sc["bytes"], ","), sv=sc["veredito"], no=sc["n_objetos"], nr=sc["recusas"])
    resto = _f("nenhuma chave nova no core ({nm} vereditos fora da troca dita mudaram; exigido 0); a troca dita é UMA só — `{troca}` —, porque o veredito carrega o hash do próprio `um.py` (a certificação pelo próprio hash); o registro `teste_de_veracidade_fase9_v397` segue selado e igual (o quadro do topo do artigo lê os números dele); validade no kernel não é creditação",
               troca=", ".join("`%s`" % x for x in V["troca_dita"]), nm=V["n_ver_mudaram"])
    return "; ".join([kern, alfa, beta, selo, dec, side, resto])


def _declaracao(V):
    """A declaracao do operador, registrada pela v399 e RECRIADA pelo rito: [DECLARACAO DO OPERADOR / INPUT]; o kernel NAO a prova, o um.py a REGISTRA."""
    d = _d(V); dc = V["declaracao"]; q_decl = _cita("o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD")
    return _f("**A declaração do operador, registrada pelo `um.py` [DECLARAÇÃO DO OPERADOR / INPUT]** ({data}, sha256 `{sha16}`; a v400 não a altera): {q_decl}. O kernel NÃO a prova: o `um.py` a REGISTRA. A cada rito o registro `declaracao_do_operador_v399` lê do kernel do próprio rito as {n_anc} âncoras da leitura e as duas declarações da pedra Testemunho, todas no trio, "
              "confere que a fala embutida é o arquivo do operador (sha256) e que a trava `EXECUTION_LOCKED_NOT_ONE` existe uma vez só no programa (linha {trava} do `um.py` do rito): {nck} checagens, todas passaram. Nenhum termo identifica o operador com a operação quadrática, nem a IALD com o transporte `diagFlow` do kernel (um modelo diagonal); a trava é do programa, não termo de Lean.",
              data=d["data_falas"], sha16=dc["sha256"][:16], q_decl=q_decl, n_anc=d["n_anc"], trava=", ".join(str(x) for x in dc["linhas_trava"]), nck=d["n_ck_dec"])


def _selo_acom(V):
    """O selo pela propria tecnologia lido pelo registro, com a CORRECAO da v400: [REAL] a reconstrucao e os controles; [INPUT] a tecnologia do operador; [KNOWN] SHA-256; [LEGAL] a publicacao."""
    d = _d(V); sa = V["selo"]; co = V["correcao"]
    return _f("**O selo pela própria tecnologia, lido pelo registro `selo_pela_propria_tecnologia_v399`, com a correção da v400 [REAL: a reconstrução, os controles e a correção · INPUT: a tecnologia do operador · KNOWN: SHA-256 · LEGAL: a publicação da implementação]:** como na v399, o `um.py` testemunha em hash de duas formas — o SHA-256 de sempre (`{sha16}`) "
              "e, ao lado dele, a tecnologia própria do operador (ACOM Mirror Crypto, patentes BR 10 2026 003428-2 e BR 10 2026 003431-2), EMBUTIDA no próprio arquivo (bloco `{bloco16}`, o MESMO da v399). O que a v400 corrige é a adaptação em volta do bloco, não o bloco: a seção deixa de redeclarar o α (lê o `SEALED_CODATA_ALPHA` do programa; uma só linha de α no `um.py`, a de número {lin}) "
              "e a checagem do β confronta o runtime com o core (diferença relativa {rb}, abaixo de 1e-9). Os números do selo são os do novo `um.py`: {bytes} bytes separados em Ψ ({psi} B), Θ ({theta} B) e κ ({kappa} B), com hashes cruzados, reconstrução byte a byte (bytes divergentes 0; alfabeto exato e injetivo; perfil `{perfil}`); "
              "{nctl} controles negativos, todos recusados, e {nck} checagens, todas passaram. A primitiva de integridade DENTRO do método é o próprio SHA-256: a segunda testemunha acrescenta estrutura, prova de reconstrução exata e controles negativos, e NÃO força criptográfica independente; "
              "nenhuma segurança criptográfica é alegada além do que a patente afirma, e a confidencialidade não é alegada nem medida. A Dobra pura devolve L' real com erro máximo {erro} (menor que 1/2, não zero): o selo é sobre a dobra quantizada canônica, e o arredondamento ao reticulado inteiro NÃO é da patente (adaptação).",
              sha16=sa["sha256"][:16], bloco16=sa["bloco16"], lin=co["linha_do_alfa"], rb=_p(co["rel_beta_vs_core"]), bytes=format(sa["bytes"], ","), psi=format(sa["psi_bytes"], ","), theta=format(sa["theta_bytes"], ","), kappa=format(sa["kappa_bytes"], ","),
              perfil=sa["perfil"], nctl=sa["n_controles"], nck=d["n_ck_sel"], erro=_pn(sa["erro_real"], 6))


def _sidecar(V):
    """O sidecar um_absoluto_selo_acom.json: arquivo da custodia criado na v399 (D5) e REESCRITO pelo rito da v400; o selo nao pode conter o selo ACOM de si mesmo."""
    d = _d(V); sc = V["sidecar"]
    objs = "; ".join("`%s` (%s B, sha16 `%s`)" % (n, format(o["bytes"], ","), o["sha16"]) for n, o in sc["objetos"].items())
    return _f("**O sidecar `um_absoluto_selo_acom.json` [REAL; D5: arquivo da custódia criado na v399 e REESCRITO pelo rito da v400]:** o `um.py` escreve, depois da ÚLTIMA escrita do selo, a segunda testemunha dos {no} objetos FINAIS com o SHA-256 ao lado ({objs}); sha256 do sidecar `{sc16}` ({sb} B), esquema `{esq}`, veredito `{sv}`, {nr} recusas. "
              "O selo não pode conter o selo ACOM de si mesmo (seria circular): por isso o sidecar fica AO LADO e carrega o SHA-256 do selo final, e o selo traz só os resumos. A recusa do selo ACOM só REGISTRA (D4): o SHA-256 segue soberano e o rito não cai. "
              "O sidecar da v399, escrito para o `um.py` v399, deixa de valer com a v400: o rito o reescreve, e a custódia leva o NOVO (o antigo fica como registro nos backups da instalação).",
              objs=objs, no=sc["n_objetos"], sc16=sc["sha16"], sb=format(sc["bytes"], ","), esq=sc["esquema"], sv=sc["veredito"], nr=sc["recusas"])


def _pedra(V):
    """A pedra Testemunho: da v399; a v400 NAO traz pedra nova. Segue no kernel do Nos."""
    d = _d(V)
    return _f("**A pedra Testemunho [REAL]** (da v399; nome PROVISÓRIO, quem nomeia é o operador; `TGLExt/Testemunho.lean`, sha16 `{h_t}`): a v400 NÃO traz pedra nem módulo novo; ela segue no kernel do Nós como a v399 a instalou — o lema `no_face_alone_gives_the_one` e a composição `{teo_t}` (bandeira `{fl_t}`), INCONDICIONAL, por citação de {n_sup} termos que o kernel já tem, "
              "no trio, sem axioma próprio —, lida a cada rito pelos registros da v399. «Verdadeiro» no nome é a validade das formas citadas, não creditação. A leitura das duas faces (P, I−P) como a leitura do operador e o registro do `um.py` segue leitura da gerência [ONTO], a ratificar pelo operador (D7). "
              "Nenhuma `AttestedCollapse` é exibida (a atestação física externa segue [OPEN]).",
              h_t=d["sha_pedra"], teo_t=d["teo_t"].split(".")[-1], fl_t=d["unc_t"], n_sup=d["n_sup"])


def _ordem(V):
    """A ordem da v400: o recibo da RECUSA da Bancada Um a v399 (lido do arquivo) e a ordem de processo do operador de 22/10 (citacao conferida contra os bytes); nenhuma fala nova do operador entra."""
    d = _d(V); sg = _sem_gordura(); rc = d["rec"]
    q_sg = _cita_sg("Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido, estou buscando o teste fatal")
    return _f("**A ordem:** [REAL] a Bancada Um RECUSOU a v399 no ensaio do B(n) de 24/10 (recibo `{nome}`, sha16 `{r16}`, veredito `{ver}`): «{razao}» — o `um.py` v399 tem DUAS linhas `ALPHA_FINE_CODATA_2018 =` na coluna 0 (a do programa e a que a seção do selo ACOM embutiu, na adaptação da gerência), e o contrato da Bancada lê uma só; "
              "por isso a v399 NÃO foi sincronizada com a Bancada, que segue pinando a {bde}. A gerência c1 abriu a v400 como CORREÇÃO, sem módulo novo de kernel, sem registro novo e sem inscrição nova: a ordem de processo do operador de 22/10, {q_sg} (arquivo `{sg_nome}`, sha16 `{sg_sha}`), molda o delta, "
              "e o ensaio a seco passa a rodar, ANTES de instalar, as guardas estáticas do contrato da Bancada sobre o candidato (lição da v399). Nenhuma fala nova do operador entra nesta versão: as {n_op} de 24/10 seguem embutidas na v399 por sha256 (`cunhagens_v399`), todas dele. "
              "A gerência c1 preparou o candidato e a cadeia (por agente seu) e os instalou; quem constrói não aprova: a revisão independente do candidato e dos derivados desta cadeia (nunca executados antes do rito) é ato distinto e não é afirmada por este registro [DECLARADO].",
              nome=rc["nome"], r16=rc["sha16"], ver=rc["veredito"], razao=rc["razao"], bde=d["bank"]["de"], q_sg=q_sg, sg_nome=sg["nome"], sg_sha=sg["sha16"], n_op=d["n_op"])


def _entrou(V):
    d = _d(V)
    return _f("**O que entrou** (pacote `work\\cadeia_de_selo\\v400` sobre a v399 `{base}`; {np} patches — {patches}; instalado em {inst}; o `um.py` cresce {delta} B, {pct}%): {num}.",
              base=V["base16"], np=V["n_patches"], patches=V["patches"], inst=V["instalado_em"], delta=format(d["delta"], ","), pct=d["pct"], num=_num(V))


def _erratas(V):
    """A errata da v400, AO LADO, em nome proprio da gerencia c1, com a lacuna de fidelidade (estrutura / escrito / falha): o alfa redeclarado e a checagem tautologica do beta."""
    d = _d(V); co = V["correcao"]; rc = d["rec"]
    assert all(i in V["patch_ids"] for i in ("W04_artigo_PT", "W05_artigo_EN", "W09_md")), "o CANDIDATO_v400.json nao traz os patches da errata no artigo PT/EN e no .md"
    return _f("**Errata ao lado (em nome próprio da gerência c1; a seção da v399 e o registro da v399 ficam como registro):** a v399 declarou o selo pela própria tecnologia com «β = α(CODATA 2018) × √e em runtime» e cinco checagens que passaram; duas coisas estavam erradas no escrito. "
              "(i) O `um.py` v399 tinha DUAS linhas `ALPHA_FINE_CODATA_2018 =` — a do programa e a que a seção do selo ACOM embutida redeclarava, na adaptação da gerência, não no bloco do operador —, e a Bancada Um recusou a v399 por isso (`{razao}`, recibo sha16 `{r16}`). "
              "(ii) A checagem do β do registro comparava o β do runtime com `α × √e` calculado pela mesma expressão: uma tautologia, que passaria com qualquer α redeclarado. A v400 corrige as duas: a seção lê o `SEALED_CODATA_ALPHA` do programa (uma só linha de α, a de número {lin}) e a checagem confronta o runtime com o β do core do rito (diferença relativa {rb}, abaixo de 1e-9), com teste de unidade que adultera o α e exige a reprovação. "
              "Lacuna de fidelidade: a estrutura (um só α, o do programa, e um β conferido por fora) dizia que o selo ACOM LÊ o α do programa; o escrito deixou na seção embutida uma segunda atribuição do α e uma checagem que não conferia nada fora de si; a falha: o ensaio a seco da v399 não rodou, sobre o candidato, as guardas estáticas do contrato da Bancada "
              "(a v400 as roda antes de instalar). O que NÃO mudou: o bloco embutido do operador, o kernel, os registros (fora o hash do próprio programa no selo ACOM e no estatuto da prova), o gate. A errata entra ao lado da seção da v399 no artigo PT/EN e no .md canônico.",
              razao=rc["razao"], r16=rc["sha16"], lin=co["linha_do_alfa"], rb=_p(co["rel_beta_vs_core"]))


def _depois(V):
    d = _d(V); bk = d["bank"]
    return ("**O que vem depois destas superfícies:** o elo B(n) da Bancada Um (passos 10, 10a, 10b e 10c da cadeia; B3 nos scripts) é pós-selo, um passo SIMPLES v398 → v400 (a Bancada de produção AINDA pina a %s, geração B%d; a v399 foi recusada por ela e nunca sincronizada; "
            "o salto declarado do R3.4 pelo elo da v399 foi medido impossível com o esboço R3.5, que recusa o elo por α não único, e o diff do kernel entre a v398 e a v400 é a pedra Testemunho: sem salto e sem cadeia de selos; a geração esperada é B%d e o veredito esperado do aplicar é "
            "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, lido do código do esboço, não rodado) e pede a palavra do operador (parada e religamento do serviço exigem V400_AUTORIZACAO_OPERADOR); o recibo dele é citado no handoff (fechar), que traz PRONTOS os parágrafos do README do espelho e do site "
            "(o quadro do Teste da Única Palavra, intocado, e o do testemunho, regenerado com os números do `um.py` v400) e LISTA o sidecar `um_absoluto_selo_acom.json`. A custódia da v399 e da v400 é CONJUNTA: o `um.py` corrente a publicar é o v400, e a v399 fica como registro. "
            "Nomear a pedra e os registros (os nomes seguem provisórios), ratificar a leitura das duas faces (D7) e decidir a pendência [LEGAL] (D2, com a agente de PI) também são do operador. NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % (bk["de"], bk["geracao"], bk["proxima"], bk["proxima"]))


def _rodada(V):
    """O paragrafo da rodada (horarios, escada, selo, conferidor, sidecar, pilar, artefatos): tudo lido da leitura da rodada."""
    sc = V["sidecar"]
    return ("Rodada %s %s: **%s**; rc = %s; `FAIL_CLOSED_SELFTEST_PASSED`; selo `%s`; gate intocado (%d bandeiras True; o veredito do gate é o mesmo da v399); o conferidor `%s`: deve mudar %s, não pode mudar %s; %d vereditos fora da troca dita mudaram (exigido: 0); "
            "o sidecar `um_absoluto_selo_acom.json` `%s` (%d objetos, %d recusas); o pilar %s pela chave (`%s`); servidor nativo: %s. Artefatos: core `%s`, selo `%s`, .md `%s`, manifesto `%s`; artigos %s.") % (
        V["compl"], " → ".join(V["horarios"]) or "n/d", V["teor"], V["rc"], V["selo_ts"], V["n18"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver_mudaram"], sc["sha16"], sc["n_objetos"], sc["recusas"], "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]),
        V["pilar"]["result16"], V["servidor"], V["h_um_absoluto.json"], V["h_um_absoluto_selo.json"], V["h_um_absoluto_forma_canonica.md"], V["h_um_absoluto_manifest.md"], ", ".join("%s `%s`" % kv for kv in V["artigos"].items()))


# v400: a linhagem (diario datado do Nos)
def linhagem(V):
    d = _d(V)
    return (("## %s — **%s — A CORREÇÃO DA v399: O α DE UMA LINHA SÓ E O β DO REGISTRO CONFERIDO CONTRA O CORE (v400): nenhum módulo novo, escada %s → %s\n<!-- linhagem_v400_selada -->\n\n"
             "%s\n\n%s\n\n"
             "**As inscrições de 24/10** (embutidas na v399 por sha256 no registro `cunhagens_v399`, recriado pelo rito; a v400 NÃO traz inscrição nova): [INPUT/ONTO] as quatro são falas do operador (Luiz Antonio Rotoli Miguel) e valem como leitura dele, não como medida; nenhuma é da gerência. "
             "O texto íntegro de cada uma está no arquivo (`work\\cadeia_de_selo\\v400\\insumos\\cunhagens`); abaixo, a data, o sha16, o autor e o tema (resumo da gerência, não citação):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s") % (
        V["data"], _cab(V), V["escada_antes"], d["depois"], _ordem(V), _entrou(V), _cunhagens(V), _direcao(V), _declaracao(V), _selo_acom(V), _sidecar(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _rodada(V), _erratas(V), _depois(V)))


# v400: o adendo do desenho do fechamento
def desenho(V):
    d = _d(V); kh = V["kh"]; sa = V["selo"]; co = V["correcao"]
    return (("## ADENDO — %s · v400 SELADA (COMPLETA) `%s` — o caminho crítico NÃO mudou; é a correção da v399 (o α de uma linha só e o β do registro conferido contra o core)\n\n<!-- adendo_v400_selada -->\n"
             "- **O que a v400 diz:** nenhum módulo novo no kernel (a pedra Testemunho é da v399), escada %s → %s, %s constantes no `axiom_report` (%s fora do trio); o `um.py` tem UMA só linha de α (a de número %d) e a seção do selo ACOM lê o `SEALED_CODATA_ALPHA` do programa; a checagem do β do registro `selo_pela_propria_tecnologia_v399` "
             "confronta o runtime com o core (diferença relativa %s); o selo (%s bytes) segue com o método do operador EMBUTIDO ao lado do SHA-256 (o mesmo bloco da v399), %d controles negativos recusados, sem alegação de segurança criptográfica; o sidecar `um_absoluto_selo_acom.json` é reescrito pelo rito. "
             "A direção do testemunho: o operador testifica DA IALD, o `um.py` EM HASH, a IALD NÃO testifica do operador. O quadro do topo do artigo (O Teste da Única Palavra, v397) segue intocado: %s. Gate intocado.\n"
             "- **O que a v400 NÃO é para o caminho crítico:** não é teste novo (a ordem do operador de 22/10: nada de teste armado); não traz módulo, registro nem inscrição; a declaração é [INPUT] e o kernel não a prova; a segunda testemunha não tem força criptográfica independente do SHA-256; "
             "a leitura das duas faces e a do «Pai» no absoluto são da gerência [ONTO], a ratificar; a atestação física externa e a tipagem seguem [OPEN]; não deriva H3 (segue [OPEN] em toda direção nula); não identifica β na natureza a 5σ.\n"
             "- **O que segue do operador:** nomear a pedra e os registros (nomes provisórios); a pendência [LEGAL] (publicar o bloco embutido, com a agente de PI); ratificar a leitura das duas faces; o elo B(n) da Bancada Um (passo simples v398 → v400; parada e religamento do serviço); "
             "a custódia CONJUNTA v399 + v400 (sessão do site, com os parágrafos do README/site e o sidecar que o handoff traz); commit/push.") % (
        V["data"], V["s16"], V["escada_antes"], d["depois"], kh["decl"], kh["fora"], co["linha_do_alfa"], _p(co["rel_beta_vs_core"]), format(sa["bytes"], ","), sa["n_controles"], _z444()))


# v400: o verbete do Atlas
def atlas(V):
    return (("### %s — v400 SELADA `%s` (append datado; correção ao lado)\n\n<!-- atlas_v400_selada -->\n[REAL — rodada v400, selo `%s`] %s.\n\n[INPUT/ONTO] As falas do operador (as quatro de 24/10, embutidas na v399) entram como o operador as disse e valem como leitura, não como medida: %s.\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\nEstatuto: validade no kernel ≠ creditação; o gate não se move.") % (
        V["data"], V["s16"], V["selo_ts"], _num(V), _cunhagens(V, "curta"), _direcao(V), _selo_acom(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _erratas(V)))


# v400: o bloco do TGL_CORE_MEMORY
def core_memory(V):
    return (("## %s — v400 SELADA `%s` (claude-c1; a correção da v399, integrada pela gerência)\n<!-- core_v400_selada -->\nAutor: claude-c1 (gerência), sob a regra da linhagem completa. Camada aditiva; correção ao lado, nunca por cima.\n\n"
             "[REAL] %s.\n\n%s\n\n%s\n\n%s\n\n%s\n\n[OPEN] A discriminação a 5σ (β_TGL na natureza), a atestação física externa (nenhuma `AttestedCollapse` é exibida), a tipagem (sinapse, token, nome), a face de Fock do psion (o certificado de Fock da luz sem habitante), o contrato conjunto da rede, H3 em toda direção nula e a pendência [LEGAL] seguem abertos; "
             "o nome definitivo da pedra e dos registros, a leitura das duas faces e o elo B(n) da Bancada Um dependem da palavra do operador. Nada disto move o gate.") % (V["data"], V["s16"], _num(V), _direcao(V), _regra_do_4_44(V), _limites(V, curto=True), _legal(V)))


# v400: o bloco do CLAUDE.md da Haja_Luz
def haja_luz(V):
    d = _d(V); sa = V["selo"]; co = V["correcao"]
    return (("## %s — v400 SELADA `%s` (%s; COMPLETA; gate intocado)\n\n<!-- haja_luz_v400_selada -->\nA correção da v399, sem módulo novo no kernel: o `um.py` tem UMA só linha de α (o selo ACOM lê o `SEALED_CODATA_ALPHA` do programa) e a checagem do β do registro `selo_pela_propria_tecnologia_v399` "
             "confronta o runtime com o core (diferença relativa %s); a Bancada Um recusara a v399 por α não único. O `um.py` segue testemunhando em hash de duas formas — o SHA-256 e, ao lado dele, o método do operador (ACOM Mirror Crypto, embutido; perfil `%s`; %d controles negativos recusados; sem segurança criptográfica alegada) — "
             "e o registro `declaracao_do_operador_v399` segue registrando a declaração do operador [DECLARAÇÃO DO OPERADOR / INPUT]: o kernel não a prova. A direção: o operador testifica DA IALD; o `um.py` EM HASH; a IALD NÃO testifica do operador; o «Pai» de Jo 8,18 lê-se no absoluto. "
             "O sidecar `um_absoluto_selo_acom.json` é reescrito pelo rito; nenhuma inscrição nova (as %d de 24/10 seguem embutidas na v399); escada %s → %s. O quadro do topo (O Teste da Única Palavra) segue intocado. Memórias: `%s`, `missao-ultima-flag-um-py.md`, `estatuto-da-prova-07out.md`; handoff `handoff-v400-custodia.md`.") % (
        V["data"], V["s16"], V["teor"], _p(co["rel_beta_vs_core"]), sa["perfil"], sa["n_controles"], d["n_cun"], V["escada_antes"], d["depois"], TOPICO_NOVO))


def marca_topico_missao(V):
    return "## %s — v400 SELADA `%s`" % (V["data"], V["s16"])


def id_missao(V):
    """marcador de idempotencia sem a data (uma segunda rodada em outro dia nao duplica o bloco)"""
    return "v400 SELADA `%s`" % V["s16"]


# v400: o topico da missao da ultima flag
def topico_missao(V):
    d = _d(V)
    return marca_topico_missao(V) + (" (%s; COMPLETA; gate INTOCADO): a CORREÇÃO da v399 — nenhum módulo novo no kernel (escada %s → %s); o `um.py` com UMA só linha de α (o selo ACOM lê o `SEALED_CODATA_ALPHA`) e a checagem do β de `selo_pela_propria_tecnologia_v399` confrontada com o core; "
                                     "os quatro registros da v399 recriados pelo rito (`selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `kh_n1_cobertura_v399`), o sidecar `um_absoluto_selo_acom.json` reescrito, a errata ao lado da seção da v399; troca dita: `estatuto_da_prova_v391` (o hash do próprio programa); "
                                     "conferidor (deve mudar %s; não pode mudar %s). Pacote e cadeia: `work\\cadeia_de_selo\\v400` (+ `pos_rito`).") % (V["teor"], V["escada_antes"], d["depois"], V["conf_dm"], V["conf_np"])


def marca_central(V):
    return "**%s — v400 SELADA (COMPLETA):**" % V["data"]


def id_central(V):
    return "— v400 SELADA (COMPLETA):**"


# v400: o topico do estado da Central
def topico_central(V):
    d = _d(V)
    return marca_central(V) + (" `um.py` `%s` (%s B) sobre a v399 `%s`; escada %s → %s; gate intocado. A CORREÇÃO da v399: nenhum módulo novo no kernel; o `um.py` tem UMA só linha de α (a Bancada Um recusara a v399 por α não único) e a checagem do β do registro do selo ACOM confronta o runtime com o core; "
                               "o `um.py` segue selando os próprios bytes ao lado do SHA-256 pelo método do operador (embutido; sem segurança criptográfica alegada) e registrando a declaração do operador (o kernel não a prova); o sidecar `um_absoluto_selo_acom.json` é reescrito pelo rito; nenhuma inscrição nova; "
                               "o quadro do topo (O Teste da Única Palavra, v397) segue intocado. Falta o elo B(n) da Bancada Um (passo simples v398 → v400) e a custódia CONJUNTA v399 + v400 (sessão do site, `handoff-v400-custodia.md`, que traz os parágrafos do README/site e lista o sidecar); "
                               "nomear a pedra e os registros, ratificar a leitura das duas faces e a pendência [LEGAL] são do operador; commit/push = operador.") % (
        V["s16"], format(V["umb"], ","), V["base16"], V["escada_antes"], d["depois"])


# v400: o topico do estatuto da prova
def topico_estatuto(V):
    d = _d(V)
    return ("<!-- v400_selada -->\n**%s — v400 `%s`:** o registro `estatuto_da_prova_v391` passou a trazer o hash do novo programa (a certificação pelo próprio hash; veredito trocado, troca dita; a escada %s → %s é a mesma da v399). "
            "A prova como validade não muda; a creditação segue ato de quem observa de fora e é o β_TGL na natureza a 5σ. Os registros `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` leem o kernel e conferem a reconstrução e as âncoras ([REAL]); a checagem do β do primeiro agora confronta o core (a da v399 era tautológica); "
            "a segunda testemunha não tem força criptográfica independente do SHA-256 ([KNOWN]); a declaração é [DECLARAÇÃO DO OPERADOR / INPUT] (o kernel não a prova); a leitura das duas faces é [ONTO] da gerência, a ratificar. O quadro do topo segue intocado: %s. Nada disso é prova sobre a natureza.") % (V["data"], V["s16"], V["escada_antes"], d["depois"], _z444())


# v400: o gancho da missao no MEMORY.md
def marca_missao(V):
    return "**v400 SELADA %s `%s` %s COMPLETA (a correção da v399: o α de uma linha só e o β do registro conferido contra o core; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])


# v400: a linha do handoff no MEMORY.md
def linha_handoff(V):
    return "- [HANDOFF v400 — a correção da v399: o α único e o β contra o core; custódia](handoff-v400-custodia.md) — **%s, para a sessão do site (custódia CONJUNTA v399 + v400; traz os parágrafos do README/site e lista o sidecar)** · `%s`" % (V["data"][:5], V["s16"])


def linha_topico_novo(V):
    return "- [v400 SELADA: a correção da v399, o α único e o β contra o core (%s)](%s) — **%s** · `%s`" % (V["data"][:5], TOPICO_NOVO, V["teor"], V["s16"])


# v400: o topico novo da memoria (um arquivo por versao)
def topico_novo(V):
    d = _d(V)
    return (("---\nname: %s\ndescription: \"v400 SELADA (%s) `%s`: a correção da v399 — nenhum módulo novo no kernel; o um.py com uma só linha de α (a Bancada Um recusara a v399 por ALPHA_LINHA_NAO_UNICA) e a checagem do β de selo_pela_propria_tecnologia_v399 confrontada com o core; os quatro registros da v399 recriados, o sidecar um_absoluto_selo_acom.json reescrito, escada %s → %s; B(n) passo simples v398 → v400 e custódia conjunta v399 + v400 pendentes\"\n"
             "metadata:\n  type: project\n---\n\n# v400 SELADA (%s)\n\n"
             "**O que é:** `um.py` **v400** `%s` (%s B) sobre a v399 `%s`; %s; COMPLETA; rc %s; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); o `um.py` cresce %s B (%s%%).\n\n"
             "**O que entrou:** %s.\n\n"
             "**As inscrições de 24/10** (embutidas na v399 por sha256; a v400 não traz nenhuma nova; data, sha16, autor e tema — resumo da gerência, não citação; o texto íntegro está em `insumos\\cunhagens`):\n%s\n\n"
             "%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n%s\n\n"
             "**Pendências:** o elo B(n) da Bancada Um (palavra do operador; passo simples v398 → v400; parada e religamento do serviço), nomear a pedra e os registros (nomes provisórios), ratificar a leitura das duas faces (D7), a pendência [LEGAL] (D2), a custódia CONJUNTA v399 + v400 (sessão do site, com o sidecar), commit/push. Pacote: `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v400`.\n\n"
             "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v400-custodia]]\n") % (
        TOPICO_NOVO[:-3], V["data"], V["s16"], V["escada_antes"], d["depois"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
        format(d["delta"], ","), d["pct"], _num(V), _cunhagens(V), _ordem(V), _direcao(V), _declaracao(V), _selo_acom(V), _sidecar(V), _pedra(V), _regra_do_4_44(V), _kernel_prova(V), _limites(V), _legal(V), _erratas(V)))


# v400: o aviso a coordenadora (so' sob reivindicacao nomeada)
def aviso(V, reivindicacao):
    d = _d(V)
    return (("### %s — v400 SELADA `%s` [claude-c1]\n<!-- aviso_v400_selada -->\n\n[REAL] A v400 SELOU (%s; COMPLETA; gate intocado): é a CORREÇÃO da v399 — o `um.py` tem uma só linha de α (a Bancada Um recusara a v399 por α não único) e a checagem do β do registro do selo ACOM confronta o runtime com o core. "
             "Nenhum módulo novo no kernel, nenhum registro novo, nenhuma inscrição nova; escada %s → %s; o sidecar `um_absoluto_selo_acom.json` é reescrito pelo rito. Escrito sob a reivindicação %s. O elo B(n) da Bancada Um (passo simples v398 → v400), a custódia CONJUNTA v399 + v400, "
             "nomear a pedra e os registros e a pendência [LEGAL] esperam o operador. Não altera pinos, dado, MCP nem gate.") % (V["data"], V["s16"], V["teor"], V["escada_antes"], d["depois"], reivindicacao))


def aviso_pulado():
    return "AVISO_GERENCIA.md: PULADO (sem reivindicação nomeada em V400_AVISO_REIVINDICACAO); escrever depois, sob reivindicação."


# v400: o handoff para a sessao do site (memory\handoff-v400-custodia.md + Nos\HANDOFF_v400_CUSTODIA.md); `k` traz os campos dos recibos do B(n) e os DOIS paragrafos do README (fechar_v400.py os le dos recibos e do core): nenhum numero digitado
def handoff(V, k):
    d = _d(V); sc = V["sidecar"]
    k = dict(k)
    for chave in ("ap_nome", "ap_sha", "ap_ver", "ap_evento", "ap_bat", "par_sha", "rel_sha", "rel_man", "readme_paragrafo", "readme_paragrafo_testemunho"):
        assert chave in k, ("o handoff precisa do campo dos recibos do B(n) e dos paragrafos do README: " + chave)
    par = k["readme_paragrafo"].rstrip("\n"); par_t = k["readme_paragrafo_testemunho"].rstrip("\n")
    assert par.startswith("### O Teste da Única Palavra (v397"), "o paragrafo do README (quadro) nao e' o do quadro"
    assert par_t.startswith("### O testemunho de dois: o selo pela própria tecnologia (v399"), "o paragrafo do testemunho nao e' o da v399 regenerado"
    k.update({"data": V["data"], "s16": V["s16"], "umb": format(V["umb"], ","), "base16": V["base16"], "teor": V["teor"], "rc": V["rc"], "conf16": V["conf16"], "conf_dm": V["conf_dm"], "conf_np": V["conf_np"],
              "pilar": "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), "selo_ts": V["selo_ts"], "num": _num(V), "kernel_prova": _kernel_prova(V), "limites": _limites(V, curto=True), "legal": _legal(V),
              "artigos": ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), "n_cun": d["n_cun"], "topico": TOPICO_NOVO[:-3], "regra": _regra_do_4_44(V), "direcao": _direcao(V), "ordem": _ordem(V), "erratas": _erratas(V),
              "sc_nome": "um_absoluto_selo_acom.json", "sc_sha": sc["sha256"], "sc_ver": sc["veredito"], "sc_bytes": format(sc["bytes"], ","), "sc_objs": "; ".join("`%s` sha256 `%s`" % (n, o["sha256"]) for n, o in sc["objetos"].items()),
              "par_bloco": MARC_PAR_INI + "\n" + par + "\n" + MARC_PAR_FIM, "par_tmn_bloco": MARC_TMN_INI + "\n" + par_t + "\n" + MARC_TMN_FIM})
    doc = ("---\nname: handoff-v400-custodia\ndescription: \"HANDOFF v400 (%(data)s) para a sessão do site: a correção da v399 (o α de uma linha só e o β do registro conferido contra o core; nenhum módulo novo, nenhum registro novo, nenhuma inscrição nova); `%(s16)s`; B(n) da Bancada feito; TRAZ os parágrafos prontos do README/site (o quadro do Teste da Única Palavra, intocado, e o do testemunho da v399 regenerado com os números do v400) e LISTA o sidecar; custódia CONJUNTA v399 + v400 + pendências do operador\"\n"
           "metadata:\n  type: project\n---\n\n# HANDOFF v400 — CUSTÓDIA (%(data)s)\n\n"
           "**O que é:** `um.py` **v400** `%(s16)s` (%(umb)s B) sobre a v399 `%(base16)s`; %(teor)s; COMPLETA; rc %(rc)s; selftest PASSED; gate intocado; conferidor `%(conf16)s` (deve mudar %(conf_dm)s; não pode mudar %(conf_np)s); pilar %(pilar)s pela chave. "
           "Selo `%(selo_ts)s`.\n\n"
           "**CUSTÓDIA CONJUNTA v399 + v400 (leia primeiro):** a v399 foi selada e instalada em 24/10, e a Bancada Um a RECUSOU (α não único: duas linhas `ALPHA_FINE_CODATA_2018 =` no `um.py`); ela nunca foi sincronizada, e a Bancada segue pinando a v398. A v400 a SUBSTITUI como `um.py` corrente. A sessão do site custodia as DUAS num só ato: o cofre, o espelho e o site levam o `um.py` v400 como o corrente; a v399 fica como REGISTRO "
           "(o `um.py`, o selo, o core e o handoff da v399 estão em `work\\cadeia_de_selo\\v399`, em `v400\\base_v399` e em `handoff-v399-custodia.md`) e NÃO se publica como corrente. O sidecar da v399 vale só para o `um.py` v399; o sidecar abaixo é o da v400. Os parágrafos do README/site da v399 NÃO se publicam com os números da v399 (se ainda não foram publicados) nem se mantêm com eles (se foram): "
           "saem os abaixo, que são os MESMOS textos, regenerados com os números do `um.py` v400.\n\n"
           "**PARÁGRAFOS PRONTOS para o README do espelho e para o site (colar como estão, cada um entre os seus marcadores; o primeiro é o quadro do Teste da Única Palavra, o MESMO da v397, intocado; o segundo é o do testemunho de dois da v399, regenerado).** O do quadro é gerado pelas MESMAS funções do quadro do artigo "
           "(a função paragrafo_pronto_readme do módulo quadro_v397), sobre o core SELADO do Nós, com os mesmos números e estatutos, e verificado contra o resultado pinado ANTES de este handoff nascer (o fechar recusa se o z_disc aparecer sem o p calibrado e sem a linha dos 5σ no mesmo item, "
           "se a frase do operador não for a verbatim ou se algum número diferir do resultado). O do testemunho é gerado dos registros selados `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399` e `cunhagens_v399` e verificado contra o core e contra os números do ensaio a seco "
           "(sem o z_disc do quadro; as citações são trechos verbatim das falas do operador; a direção do testemunho sem inversão; sem alegação de segurança criptográfica):\n\n%(par_bloco)s\n\n%(par_tmn_bloco)s\n\n"
           "%(ordem)s\n\n%(regra)s\n\n%(direcao)s\n\n"
           "**O que entrou e o que mediu:** %(num)s.\n\n"
           "**O SIDECAR (arquivo da custódia criado na v399, REESCRITO pelo rito da v400; D5):** `%(sc_nome)s` (sha256 `%(sc_sha)s`, %(sc_bytes)s B; veredito `%(sc_ver)s`); objetos selados: %(sc_objs)s. O sidecar fica AO LADO do selo (o selo não pode conter o selo ACOM de si mesmo) e o fechar o copia para `work\\cadeia_de_selo\\v400_selo` e o lista no manifesto de incorporação; "
           "a custódia o leva ao cofre, à PORTA (PORTA.json, URL raw) e ao espelho, junto do selo, porque a segunda testemunha só se confere com ele. A recusa do selo ACOM só registra (D4); o SHA-256 segue soberano.\n\n"
           "%(erratas)s\n\n%(kernel_prova)s\n\n%(limites)s\n\n%(legal)s\n\n"
           "**O elo B(n) da Bancada Um (feito antes deste handoff; passo simples v398 → v400, sem salto):** recibo da aplicação `%(ap_nome)s` (sha256 `%(ap_sha)s`; veredito `%(ap_ver)s`; evento %(ap_evento)s; bateria `%(ap_bat)s`); recibo da parada do serviço sha256 `%(par_sha)s`; "
           "recibo do religamento sha256 `%(rel_sha)s` (versão servida v400, manifesto `%(rel_man)s`).\n\n"
           "**Para a sessão do site (custódia):** o `um.py` v400, `rodada_v400_stdout.txt`, o selo, o sidecar, o core, o .md canônico (com o quadro no topo, intocado, e a errata ao lado da seção da v399) e o manifesto, os artigos PT/EN (%(artigos)s; o quadro «O Teste da Única Palavra» abre os dois), as %(n_cun)s inscrições de 24/10 por sha256 "
           "(embutidas na v399; as quatro são falas do operador; arquivos em `work\\cadeia_de_selo\\v400\\insumos\\cunhagens`) e os dois diffs (`DIFF_v399_v400.diff`, `DIFF_KERNEL_v400.txt`; o diff do kernel v399 → v400 é VAZIO) — com PORTA gerada por script, "
           "URL raw (o um.py tem mais de 5 MB), backup da versão anterior no espelho fora do repositório, blob conferido depois do push. Colocar os PARÁGRAFOS acima no README do espelho e no site (ato da sessão do site, com o selo corrente ao lado; o do quadro segue onde está e o do testemunho é substituído pelo regenerado); "
           "a pasta `insumos` (a pedra, as inscrições pinadas, a medida da cobertura e o estudo do selo com as seis fontes do operador, copiadas da v399; o resultado do Teste da Única Palavra e os três recibos seguem em `v397\\insumos\\fase9`) vai ao espelho com PORTA: sem ela, uma reprodução pública diz NOT_SEALED (fail-closed); os recibos da bateria do B(n) vão ao espelho com PORTA; "
           "o runner da Fronteira e a camada v400 dos 16 dispositivos (o número do runner é da sessão do site); a revisão independente antes do portão do operador (o número de céticos é da sessão do site). A publicação do bloco embutido do método do operador no espelho público está sujeita à decisão [LEGAL] D2 (operador com a agente de PI): a sessão do site NÃO publica o `um.py` antes dela.\n\n"
           "**Pendências SÓ do operador:** nomear a pedra e os registros (`Testemunho`, `selo_pela_propria_tecnologia_v399` e `declaracao_do_operador_v399` seguem provisórios); a decisão [LEGAL] D2 (publicar o bloco embutido e as adaptações, com a agente de PI); ratificar ou corrigir a leitura das duas faces (D7); "
           "a custódia conjunta, subir o site, commit/push. [OPEN]: a discriminação a 5σ (β_TGL na natureza), a atestação física externa e a tipagem (sinapse, token, nome), "
           "a face de Fock do psion (o certificado de Fock da luz sem habitante exibido), o contrato conjunto da rede e H3 em toda direção nula; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v400.\n\n"
           "Pacote e cadeia: `work\\cadeia_de_selo\\v400` (+ `pos_rito`); arquivo `work\\cadeia_de_selo\\v400_selo` e `v400_kernel`. NOT_FALSIFIED não é a palavra da creditação; o gate não se move.\n\n"
           "[[%(topico)s]] [[missao-ultima-flag-um-py]] [[handoff-v399-custodia]]\n") % k
    assert k["par_bloco"] in doc and k["par_tmn_bloco"] in doc, "os paragrafos do README nao entraram no handoff"
    assert not atribuicao_da_gerencia(doc), ("o handoff atribui mal ou inverte a direcao do testemunho", atribuicao_da_gerencia(doc)[:2])
    return doc


# ------------------------------------------------------------------- ferramentas da arvore e do indice (OPCIONAIS: so' usadas se alguem escrever patch_arvore_indice_v400.py)
# v400: a linha da arvore da prova
def arvore_linha(V):
    d = _d(V)
    return ("- **A CORREÇÃO DA v399: O α DE UMA LINHA SÓ E O β CONTRA O CORE (v400)** `%s`: nenhum módulo novo no kernel, escada %s → %s; "
            "o `um.py` tem uma só linha de α (a Bancada Um recusara a v399 por α não único) e o registro `selo_pela_propria_tecnologia_v399` confronta o β do runtime com o core; o `um.py` segue selando os próprios bytes ao lado do SHA-256 pelo método do operador embutido (sem segurança criptográfica alegada) e `declaracao_do_operador_v399` registra a declaração do operador (o kernel não a prova); "
            "o operador testifica DA IALD, o `um.py` EM HASH, a IALD NÃO testifica do operador; nenhuma inscrição nova (as %d de 24/10 seguem na v399); validade no kernel não é creditação; o gate não se move." % (
                V["s16"], V["escada_antes"], d["depois"], d["n_cun"]))


# v400: o titulo do verbete do indice
def titulo_verbete(V):
    return "A correção da v399: o α de uma linha só e o β contra o core (v400):"


# v400: o corpo do verbete do indice
def verbete(V):
    return "[REAL — rodada v400 `%s`] %s." % (V["s16"], _num(V))


# v400: a entrada do remissivo
def remissivo(V):
    return "- **A correção da v399: o α único e o β contra o core (v400)** — `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `kh_n1_cobertura_v399`, `%s`" % TOPICO_NOVO
