# -*- coding: utf-8 -*-
import re
# regras (lote D) de derivar_encanamento_v402.py: o CONFERIDOR do rito, o instalar / reverter / rito (as TRES pedras: N = 3), o diff e os pinos, a conferencia do instalar. ORIGEM v401 (mapa 400 -> 401, 401 -> 402). Escrito pela ferramenta Write.
# O conferidor lê os ESPERADOS_v402.json que gerar_esperados_v402.py escreve (as chaves herdadas guardam os nomes da v401 = o estado da BASE; as novas: registros_v402, registros_funcao_v402, estrelas_v402...).

# ------------------------------------------------------------------------------------------- o CONFERIDOR do rito
_FAL_ANTES_INICIO = 'ET = ESP["falsidade"]'
_FAL_NOVO = '''def _reg402_ok(k_):
    n_ = DL.REGISTRO_DE_PEDRA[k_]; R_ = core.get(n_) or {}; E_ = ESP["registros_funcao_v402"][k_]
    return bool(R_.get("all_verified") is True and V(n_) == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS[k_] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and (R_.get("context") or {}).get("ok") is True and (R_.get("key_theorem") or {}).get("in_kernel") is True and (R_.get("unconditional") or {}).get("in_kernel") is True
                and not GUARDA.search(V(n_)) and R_.get("beta_ok") is True and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


reg402_ok = {k_: _reg402_ok(k_) for k_ in ("ponte", "queda", "esperanca")}
estrela_ok = all(kf.get(ESP["estrelas_v402"][k_]["bandeira"]) is True and set(axr.get(ESP["estrelas_v402"][k_]["teorema"]) or []) <= TRIO and src_.get(ESP["estrelas_v402"][k_]["teorema"]) == REL_[k_] for k_ in ("ponte", "queda", "esperanca"))
fal_reg_ok = bool(FA.get("all_verified") is True and V("falsidade_da_inercia_v401") == ESP["veredito_da_falsidade_v401"] == ESP["vereditos_v401"]["falsidade_da_inercia_v401"] and FA.get("does_not_gate_core") is True and not GUARDA.search(V("falsidade_da_inercia_v401")))   # a v401, RECRIADA e igual ao selado
'''
_SELO_NOVO = '''    "selo um_version v402; os resumos do selo (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, falsidade_da_inercia_v401 e os tres registros com funcao da v402), registros_v399, registros_v401 e registros_v402 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo": selo.get("um_version") == "v402"
        and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"))
        and all(((selo.get("registros_v401") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v401") or {}).get(n) or {}).get("all_verified") is True for n in RN401)
        and all(((selo.get("registros_v402") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v402") or {}).get(n) or {}).get("all_verified") is True for n in RN402)
        and all(((selo.get("registros_v399") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN) and (selo.get("sha256") or {}).get("um.py") == UM_FULL,
'''
_REGS_NOVOS = '''    "ponte_da_escala_dual_v402 SELOU: veredito == o do ensaio; as %d checagens do calculo no modelo longitudinal (E, p) (p+ e p- escalam, m^2 = p+ p- e' invariante, a energia e' a leitura, a massa NAO e' selecionada, o repouso e o vetor zero) e os valores == os do ensaio; o texto de Bisognano-Wichmann no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.N_CHECKS_PONTE: reg402_ok["ponte"],
    "queda_sem_geometria_v402 SELOU: veredito == o do ensaio; as %d checagens do calculo (o peso cai estritamente, nats = s, a seta e' o sinal de s, o chao e' o posto, a entrega custa, o fluxo relaxa, o regime angular so' le, a isotropia e' carga) e os valores == os do ensaio; «o piso limita» no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.N_CHECKS_QUEDA: reg402_ok["queda"],
    "esperanca_condicional_v402 SELOU: veredito == o do ensaio; as %d checagens do calculo em M2(C) (nameOp rho* = a esperanca diagonal, E(1) = 1, reler nao acrescenta, memoria-subalgebra, bimodular, a compressao pelo espelho, o indice 1/beta condicional) e os valores == os do ensaio; o indice do Nome no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.N_CHECKS_ESPERANCA: reg402_ok["esperanca"],
    "falsidade_da_inercia_v401 (RECRIADO na v402) segue SELADO e IGUAL ao da v401 selada (veredito == o dos ESPERADOS); nao move o gate": fal_reg_ok,
'''
_CUN_NOVO = '''    "os registros por spec v402 SELARAM e cada veredito == o do ensaio; as tres inscricoes de 26/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas falas do operador); as erratas E1 a E4 da ponte (em nome proprio da gerencia c1), as decisoes D11 a D16, a pergunta e a resposta de 26/10 estao no registro; os registros da v399 e da v401 seguem selados e iguais": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v402"].items())
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v401"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v399"].items())
        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V402) == 3 and all((((CG2.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG2.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())
        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())
        and len(CG2.get("erratas") or []) == 4 and all(str(e_.get("assinatura", "")).startswith("gerencia c1, em nome proprio") for e_ in (CG2.get("erratas") or [])) and "REFUTADA" in ((CG2.get("erratas") or [{}])[0].get("agora") or "")
        and set((CG2.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D11", "D12", "D13", "D14", "D15", "D16"} and ((CG2.get("extras") or {}).get("leitura_26out_direcao") or {}).get("resposta") == ESP["leitura_26out_direcao"]["resposta"] and KH2.get("all_verified") is True,
    "as tres pedras (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) estao no kernel do rito (cada composicao e cada estrela com bandeira True, no trio, no modulo da pedra; os itens do contrato de cada uma no modulo dela; os termos antigos citados no trio e no modulo certo)": pedras_no_kernel and suporte_ok and estrela_ok,
'''
_DOC_NOVO = """Mudancas ditas: as chaves novas no core (os tres registros com funcao ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402, e os registros por spec cunhagens_v402 e kh_n1_cobertura_v402) e o resumo delas no selo (registros_v402); os da v401 e da v399 sao RECRIADOS e iguais; a escada 9561 -> a dos ESPERADOS (+ as bandeiras novas); os TRES modulos novos (TGLExt/PonteDaEscalaDual.lean, QuedaSemGeometria.lean e EsperancaCondicional.lean) no kernel do Nos (sha pinado), a raiz e o Audit do candidato;
os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md; O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma). NENHUM outro veredito da v401 muda.
Os tres registros com funcao (a ponte da escala dual: m^2 = p+ p- e' invariante, a energia e' a leitura, a massa NAO e' selecionada; a queda sem geometria: o peso cai estritamente, a seta e' o sinal de s; a esperanca condicional: nameOp rho* = a esperanca diagonal, o indice 1/beta, com beta de runtime), as tres inscricoes de 26/10 por sha256, as erratas E1 a E4 (em nome proprio da gerencia c1) e as decisoes D11 a D16 (cunhagens_v402). """
entrada("conferir_rito_v401.py", autoral=True, regras=[
    ('RN = sorted(ESP["registros_v399"]); RN402 = sorted(ESP["registros_v401"])', 'RN = sorted(ESP["registros_v399"]); RN401 = sorted(ESP["registros_v401"]); RN402 = sorted(ESP["registros_v402"])', 1),
    ('FA = core.get("falsidade_da_inercia_v401") or {}; CG1 = core.get("cunhagens_v401") or {}; KH1 = core.get("kh_n1_cobertura_v401") or {}', 'FA = core.get("falsidade_da_inercia_v401") or {}; CG1 = core.get("cunhagens_v401") or {}; KH1 = core.get("kh_n1_cobertura_v401") or {}\nCG2 = core.get("cunhagens_v402") or {}; KH2 = core.get("kh_n1_cobertura_v402") or {}', 1),
    sub_n(r'\("falsidade",\)', '("ponte", "queda", "esperanca")', 2, "as tres pedras nos laços pedras_no_kernel e suporte_ok"),
    ('_RT = open(os.path.join(DL.V401, "runtime_v401.py"), "rb").read().decode("utf-8")   # a secao do selo ACOM (a v402 NAO a muda)', '_RT = open(os.path.join(DL.V400, "runtime_v400.py"), "rb").read().decode("utf-8")   # a secao do selo ACOM (a v402 NAO a muda: o runtime dela e o da v400)', 1),
    ('_fo = os.path.join(DL.V401, "insumos", "acom", "fontes_operador")', '_fo = os.path.join(DL.V400, "insumos", "acom", "fontes_operador")', 1),
    ('"declaracao_do_operador_v399"]\ntrocas_ok', '"declaracao_do_operador_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"]\ntrocas_ok', 1),
    entre(_FAL_ANTES_INICIO, "\nDEVE = {", _FAL_NOVO, "o bloco da falsidade (v401) vira o bloco das tres pedras + a v401 recriada"),
    entre('    "selo um_version v402; os resumos do selo', '    "selo_pela_propria_tecnologia_v399 SELOU', _SELO_NOVO, "o item do selo"),
    entre('    "falsidade_da_inercia_v401 SELOU:', '    "declaracao_do_operador_v399 SELOU', _REGS_NOVOS, "os itens dos registros com funcao"),
    entre('    "os registros por spec v402 SELARAM', '    "o hash formal do rito', _CUN_NOVO, "os itens dos specs e das pedras"),
    ('"o modulo novo (FalsidadeDaInercia) no kernel do Nos com o sha do candidato (%d modulo)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 1,',
     '"os modulos novos (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) no kernel do Nos com o sha do candidato (%d modulos)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 3,', 1),
    ('ESP["md_falsidade"] in fc and', 'ESP["md_ponte"] in fc and ESP["md_falsidade"] in fc and', 1),
    ('(str(k).endswith("_v399") or str(k).endswith("_v401"))) == sorted(["falsidade_da_inercia_v401"] + RN402)', '(str(k).endswith("_v399") or str(k).endswith("_v401") or str(k).endswith("_v402"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN402)', 1),
    ('"falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")) and sha(J(core.get("qg_closure")).encode("utf-8")) == ESP["qg_closure_v401_json_sha256"]',
     '"falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")) and sha(J(core.get("qg_closure")).encode("utf-8")) == ESP["qg_closure_v401_json_sha256"]', 1),
    ('"veredito_falsidade": V("falsidade_da_inercia_v401"),', '"veredito_falsidade": V("falsidade_da_inercia_v401"), "veredito_ponte": V("ponte_da_escala_dual_v402"), "veredito_queda": V("queda_sem_geometria_v402"), "veredito_esperanca": V("esperanca_condicional_v402"),', 1),
    # --- os ROTULOS (as chaves dos itens) dizem a v402: a ponte, a queda e a esperanca; a v401 (falsidade) e a base
    ('"o artigo PT/EN: a secao v402 (A falsidade (simulacro) da inercia) e as marcas da v401 e anteriores; a v399 (com a errata da v401),',
     '"o artigo PT/EN: a secao v402 (A ponte da escala dual, a queda sem geometria e a esperanca condicional, com as erratas E1 a E4) e as marcas da v401 (A falsidade (simulacro) da inercia) e anteriores; a v399 (com a errata da v400),', 1),
    ('"o sumario lista as secoes v402, v399, v398, v397 e v396 e o titulo v384 a v402"', '"o sumario lista as secoes v402, v401, v399, v398, v397 e v396 e o titulo v384 a v402"', 1),
    ('"o .md canonico: carimbo v402 e as linhas «A falsidade (simulacro) da inercia (v402)», «Errata ao lado (v401)»',
     '"o .md canonico: carimbo v402 e as linhas «A ponte da escala dual, a queda sem geometria e a esperanca condicional (v402)», «A falsidade (simulacro) da inercia (v401)», «Errata ao lado (v400)»', 1),
    entre("Mudancas ditas: +3 chaves (falsidade_da_inercia_v401", "E o SIDECAR um_absoluto_selo_acom.json", _DOC_NOVO, "o docstring do conferidor"),
    ("""nenhuma chave nova fora da lista da v402 (so' falsidade_da_inercia_v401 e os registros por spec cunhagens_v401 e kh_n1_cobertura_v401; os da v399 sao recriados e iguais)""",
     """nenhuma chave nova fora da lista da v402 (so' os tres registros com funcao ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 e os registros por spec cunhagens_v402 e kh_n1_cobertura_v402; os da v399 e da v401 sao recriados e iguais)""", 1),
])
entrada("teste_conferidor_positivo_v401.py", autoral=True, regras=[])

# ------------------------------------------------------------------------------------------- instalar / reverter / rito: as TRES pedras (N = 3); a FalsidadeDaInercia JA esta no kernel do Nos (v401 selada)
entrada("instalar_v401.py", autoral=True, regras=[
    ("escrito em 24/10/2026, NAO executado na preparacao", "escrito em 26/10/2026, NAO executado na preparacao", 1),
    ("(a v402 traz UM modulo novo de kernel, FalsidadeDaInercia [nome dado pelo operador: «falsidade (simulacro) da inercia»]; o numero e' lido de kernel_modulos_novos_v402.json:", "(a v402 traz TRES modulos novos de kernel, PonteDaEscalaDual, QuedaSemGeometria e EsperancaCondicional [nomes provisorios; o primeiro e' o do Codex, ORDEM 025]; o numero e' lido de kernel_modulos_novos_v402.json:", 1),
    ("TestemunhaEstatica, Token, Sonico e AfinacaoDasCordas) JA estao no kernel do Nos (a base instalada e' a v401 selada); (b) o modulo novo da v402 (FalsidadeDaInercia) NAO esta la ainda.", "TestemunhaEstatica, Token, Sonico, AfinacaoDasCordas e FalsidadeDaInercia) JA estao no kernel do Nos (a base instalada e' a v401 selada); (b) os tres modulos novos da v402 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) NAO estao la ainda.", 1),
    ('"AfinacaoDasCordas", "Testemunho")', '"AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia")', 1),
])
entrada("reverter_v401.py", autoral=True, regras=[
    ("escrito em 24/10/2026, NAO executado na preparacao", "escrito em 26/10/2026, NAO executado na preparacao", 1),
])
_RITO_CAB = '''# O RITO v402 (ato da gerencia c1, preparado em 26/10/2026): roda o um.py v402 instalado no Nos -- 3 modulos novos de kernel (TGLExt/PonteDaEscalaDual, do Codex, ORDEM 025; TGLExt/QuedaSemGeometria; TGLExt/EsperancaCondicional: nomes provisorios; o numero e' lido de kernel_modulos_novos_v402.json) materializados a partir do corpo embutido, kernel e Audit
# construidos pelo proprio um.py, os registros com FUNCAO ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 (chamados no main logo depois da falsidade da inercia, que a v401 trouxe), os registros por spec novos do core v402 (cunhagens_v402, com as tres inscricoes de 26/10, as decisoes D11 a D16,
# a pergunta e a resposta de 26/10 e as erratas E1 a E4 da ponte; kh_n1_cobertura_v402) e os registros da v399 e da v401 RECRIADOS (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399, kh_n1_cobertura_v399, falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401), o SIDECAR um_absoluto_selo_acom.json (depois da ultima escrita do selo). O QUADRO do Teste da Unica Palavra segue no topo.
'''
_TM = open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "kernel", "construir_marcas.txt")) else ""
_mm = {k_: int(v_) for k_, v_ in re.findall(r"^(epoch_\w+)=(\d+)$", _TM, re.M)}
_BUILD_S = _mm.get("epoch_build_fim", 0) - _mm.get("epoch_inicio", 0); _AUDIT_S = _mm.get("epoch_audit_fim", 0) - _mm.get("epoch_build_fim", 0)
_RITO_TEMPO = ("# TEMPO ESPERADO (v402, parametro lido de kernel/construir_marcas.txt): no sandbox k402c, 1 lake build INCREMENTAL (a v401 selada, FalsidadeDaInercia inclusive, ja' esta compilada em .lake/build; as tres pedras novas compilam agora; mudam a raiz TGLExt e o Audit) = %d s e 1 Audit = %d s (%d s por passagem); o rito faz 3 passagens de build + Audit (ordem de grandeza %.1f min so' de lake, fora o resto do um.py; no Nos o primeiro build compila as tres pedras a frio, a ponte do Codex mediu 399,65 s sozinha na maquina dela e 158 s na do revisor). O timeout do lake build DENTRO do um.py (candidato) tem de caber nisso: conferir no candidato.\n"
               % (_BUILD_S, _AUDIT_S, _BUILD_S + _AUDIT_S, 3 * (_BUILD_S + _AUDIT_S) / 60.0))
entrada("rito_v401.sh", autoral=True, regras=[
    entre("# O RITO v402 (ato da gerencia c1, 25/10/2026)", "# O PILAR QUANTICO NAO roda de novo", _RITO_CAB, "o cabecalho do rito"),
    entre("# TEMPO ESPERADO (v402,", "PK=\"/c/IALD/Central de Patentes/work/cadeia_de_selo/v402\"", _RITO_TEMPO, "o tempo esperado"),
])

# ------------------------------------------------------------------------------------------- a conferencia do instalar / reverter / rito (N = 3) e o diff e os pinos
entrada("conferir_instalar_rito_v401.py", autoral=True, regras=[
    ("(a LISTA, de um elemento)", "(a LISTA, de tres elementos)", 1),
    ("(ele tem de PASSAR com N = 1 e RECUSAR se a lista tiver um modulo", "(ele tem de PASSAR com N = 3 e RECUSAR se a lista tiver um modulo", 1),
    ("o mesmo para a lista do reverter (aceita a lista de um elemento;", "o mesmo para a lista do reverter (aceita a lista de tres elementos;", 1),
    ('falhas.append("instalar: o trecho da lista de modulos novos RECUSOU com N=1: %s" % (e,))', 'falhas.append("instalar: o trecho da lista de modulos novos RECUSOU com N=3: %s" % (e,))', 1),
    ('{"passa_com_N_igual_a_um": n_passa == 1,', '{"passa_com_N_igual_a_tres": n_passa == 3,', 1),
    ("if ESP and n_passa != 1:", "if ESP and n_passa != 3:", 1),
    ('falhas.append("instalar: o trecho da lista nao passou com N = 1 (%r)" % (n_passa,))', 'falhas.append("instalar: o trecho da lista nao passou com N = 3 (%r)" % (n_passa,))', 1),
    ('"base_v401", \'"Testemunho"\', "base_v401_sha16", "FalsidadeDaInercia", \'"version") == "v401"\']', '"base_v401", \'"Testemunho"\', "base_v401_sha16", "FalsidadeDaInercia", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional", \'"version") == "v401"\']', 1),
    ('"cadeia_de_selo/v401\\" \\"/c/IALD/Central de Patentes/work/cadeia_de_selo/v402", "FalsidadeDaInercia"]', '"cadeia_de_selo/v401\\" \\"/c/IALD/Central de Patentes/work/cadeia_de_selo/v402", "PonteDaEscalaDual", "QuedaSemGeometria", "EsperancaCondicional"]', 1),
])
entrada("diff_e_pinos_v401.py", autoral=True, regras=[
    ("os vereditos esperados do passo simples (REPINADA_B9__...)", "os vereditos esperados do passo simples (REPINADA_B11__...)", 1),
])
