# -*- coding: utf-8 -*-
# regras (lote D1) de derivar_encanamento_v403.py: o CONFERIDOR do rito (conferir_rito_v403.py) e o teste do caminho positivo. ORIGEM v402. Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas); cada regra tem contagem exata e nada e' executado.
# O que a v403 muda no conferidor, dito uma vez: (a) a base e' a v402 SELADA: os registros da v402 (ponte, queda, esperanca, cunhagens e kh_n1) sao RECRIADOS e comparados com os ESPERADOS (estado da BASE: chaves *_v402), os NOVOS sao *_v403;
# (b) as pedras novas sao Caminho, Vida e VerdadeAdendo (as tres pedras SELADAS da v402 ficam no kernel com o mesmo sha); (c) F8.1: o gate e' RELIDO pelo conferidor (varredura AST do um.py instalado + as fontes das tres bandeiras + o qg_closure da v402 salvo a lista de checks);
# (d) as chaves *_v402 dos ESPERADOS passam a ser o estado da base e as *_v403 o dos registros novos (gerar_esperados_v403.py). A armadilha do mapa de versoes: as chaves registros_v401 e registros_v402 do SELO sao protegidas (nascidas no um.py) e nao sobem; por isso RN401, RN402 e RN403 sao definidos aqui, por extenso.

_re_d1 = __import__("re")


def entrada_dict(inicio, novo, nome):
    """regra por FUNCAO (lote D1): troca UMA entrada de um dict multilinha (DEVE/NAO) do conferidor: do `inicio` (unico, com os 4 espacos) ate o comeco da proxima entrada (a proxima linha que comeca com 4 espacos e aspas) ou o fim do dict.
    `novo` sem a quebra final; `novo` vazio apaga a entrada e a sua quebra. ASSERTA as ancoras."""
    def fn(t):
        assert t.count(inicio) == 1, ("ancora de entrada nao unica", nome, inicio[:70], t.count(inicio))
        i = t.index(inicio)
        m = _re_d1.compile(r'\n(?:    "|\})').search(t, i + len(inicio))
        assert m is not None, ("fim da entrada nao achado", nome)
        if novo == "":
            return t[:i] + t[m.start() + 1:]
        return t[:i] + novo + t[m.start():]
    return (fn, nome, 1)


_DOC_CF = r'''"""conferir_rito_v403.py -- confere, DEPOIS do rito v403, o que tinha de mudar e o que NAO podia (ESPERADOS_v403.json; so leitura do Nos). Molde: conferir_rito_v402.py (a cadeia de CONTEUDO) com as licoes da v402 (C15, C16) e a F8.1 nova.
Mudancas ditas: as chaves novas no core (os QUATRO registros com funcao caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403, e os registros por spec cunhagens_v403 e kh_n1_cobertura_v403) e o resumo delas no selo (os quatro resumos e registros_v403); os da v402, da v401 e da v399 sao RECRIADOS e iguais; a escada 9679 -> a dos ESPERADOS (+ as bandeiras novas);
os TRES modulos novos (TGLExt/Caminho.lean, TGLExt/Vida.lean e TGLExt/VerdadeAdendo.lean) no kernel do Nos (sha pinado; as tres pedras SELADAS da v402 ficam com o mesmo sha, como registro), a raiz do candidato e o Audit (inalterado); os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md;
O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma). NENHUM outro veredito da v402 muda.
F8.1 (a unica mudanca de CODIGO do gate): as tres bandeiras antes literais (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) sao CALCULADAS no um.py instalado (varredura AST independente do registro: zero Constant); o conferidor RELE as tres FONTES no core do rito (a familia ext_ls2_* do kernel,
a checagem «pre-registro v67 INTACTO (hash)» do rito V11, o teste nulo cego da v73), confere que o qg_closure do core e' o da v402 SALVO a lista de checks (que ganha UMA sonda, ProbeBlindNullAbsent, True) e que a letra do veredito do gate e' a da v402: O GATE NAO SE MOVE.
Os quatro registros com funcao (o Caminho: a ponte da escala dual, m^2 = p+ p- invariante e a massa NAO selecionada; a Vida: a queda sem geometria, o peso cai estritamente e a seta e' o sinal de s; o adendo da Verdade: a esperanca diagonal le a projecao da identidade como os pesos q^2 e alfa^2, com alfa = beta/sqrt(e) de runtime;
as bandeiras do gate: 18 de 18 calculadas, 15 no veredito, a fonte de cada uma), as duas falas de 27/10 por sha256, as erratas E5 e E6 (em nome proprio da gerencia c1) e as decisoes D17 a D22 (cunhagens_v403). E o SIDECAR um_absoluto_selo_acom.json (a segunda testemunha do um.py, do core e do selo FINAIS, ao lado do SHA-256)
com os 16 ITENS (C1 a C16: o estudo da v399 e as guardas estaticas da Bancada) e o ROUND TRIP byte a byte do um.py INSTALADO: os bytes do um.py instalado -> as tres partes cruas (Psi, Theta, kappa) -> o objeto, refeito AQUI pelo codigo do proprio um.py instalado (importado de uma copia de bytes; o Nos so' e' lido)
e por uma conta independente (a formula da Dobra + rint + centro). A DIRECAO do testemunho (o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador) e' conferida nos textos, e nenhuma alegacao de confidencialidade pode estar no sidecar.
uso: python -I -B -X utf8 conferir_rito_v403.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V403_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""'''

_HELPERS_CF = r'''def _reg403_ok(k_):
    n_ = DL.REGISTRO_DE_PEDRA[k_]; R_ = core.get(n_) or {}; E_ = ESP["registros_funcao_v403"][k_]
    return bool(R_.get("all_verified") is True and V(n_) == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS[k_] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and (R_.get("context") or {}).get("ok") is True and (R_.get("key_theorem") or {}).get("in_kernel") is True and (R_.get("unconditional") or {}).get("in_kernel") is True
                and not GUARDA.search(V(n_)) and R_.get("beta_ok") is True and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


reg403_ok = {k_: _reg403_ok(k_) for k_ in ("caminho", "vida", "verdade_adendo")}
estrela_ok = all(kf.get(ESP["estrelas_v403"][k_]["bandeira"]) is True and set(axr.get(ESP["estrelas_v403"][k_]["teorema"]) or []) <= TRIO and src_.get(ESP["estrelas_v403"][k_]["teorema"]) == REL_[k_] for k_ in ("caminho", "vida", "verdade_adendo"))
fal_reg_ok = bool(FA.get("all_verified") is True and V("falsidade_da_inercia_v401") == ESP["veredito_da_falsidade_v402"] == ESP["vereditos_v402"]["falsidade_da_inercia_v401"] and FA.get("does_not_gate_core") is True and not GUARDA.search(V("falsidade_da_inercia_v401")))   # a v401, RECRIADA e igual ao selado
reg402_recriados_ok = all((core.get(n_) or {}).get("all_verified") is True and V(n_) == ESP["vereditos_v402"][n_] and (core.get(n_) or {}).get("does_not_gate_core") is True and not GUARDA.search(V(n_)) for n_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402"))   # os tres registros com funcao da v402, RECRIADOS e iguais aos da v402 selada
pedras_v402_ok = bool(len(ESP["pedras_v402_sha256"]) == 3 and all(_sha_k(rel_) == s_ and (kf.get("formal_files_sha256") or {}).get(rel_) == s_ for rel_, s_ in ESP["pedras_v402_sha256"].items()))   # as tres pedras SELADAS da v402 seguem no kernel do Nos (registro)


def _gate403_ok():
    R_ = core.get("bandeiras_do_gate_v403") or {}; E_ = ESP["registros_funcao_v403"]["gate"]; v_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and V("bandeiras_do_gate_v403") == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and (R_.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS["gate"] == E_["n_checks"]
                and all(c_["ok"] for c_ in (R_.get("mechanics") or {}).get("checks") or []) and not GUARDA.search(V("bandeiras_do_gate_v403")) and _feq({kk_: v_.get(kk_) for kk_ in E_["values"]}, E_["values"])
                and v_.get("n_literal") == 0 and v_.get("n_calculated") == 18 == v_.get("n_true") and v_.get("n_read_by_the_verdict") == 15 and v_.get("read_by_the_verdict") == [6, 5, 4] and v_.get("gate_verdict_equals_v402") is True)


gate403_ok = _gate403_ok()


def _f81_ast(src_):
    """varredura AST (independente do registro) da funcao prove_qg_closure_gate do um.py INSTALADO: (literais, calculadas) entre as tres bandeiras da F8.1; None se a funcao nao for unica."""
    import ast as _a
    fn_ = [n_ for n_ in _a.parse(src_).body if isinstance(n_, _a.FunctionDef) and n_.name == "prove_qg_closure_gate"]
    if len(fn_) != 1:
        return None
    lit_, calc_ = [], []
    for n_ in _a.walk(fn_[0]):
        if isinstance(n_, _a.Dict):
            for k_, v_ in zip(n_.keys, n_.values):
                if isinstance(k_, _a.Constant) and k_.value in DL.F81_LITERAIS:
                    (lit_ if isinstance(v_, _a.Constant) else calc_).append(k_.value)
        if isinstance(n_, _a.Assign) and len(n_.targets) == 1 and isinstance(n_.targets[0], _a.Subscript) and isinstance(n_.targets[0].slice, _a.Constant) and n_.targets[0].slice.value in DL.F81_LITERAIS:
            (lit_ if isinstance(n_.value, _a.Constant) else calc_).append(n_.targets[0].slice.value)
    return sorted(lit_), sorted(calc_)


_f81 = _f81_ast(UM_BYTES.decode("utf-8"))
_ls2k = sorted(k_ for k_ in (getattr(um_c, "_LEAN_THEOREM_FLAGS", None) or {}) if k_.startswith(DL.F81_PREFIXO_LS2)) if um_c is not None else []
_prereg = [c_[1] for c_ in ((core.get("void_floor_v11") or {}).get("checks") or []) if isinstance(c_, (list, tuple)) and len(c_) == 2 and c_[0] == DL.F81_ROTULO_PREREG]
_ck_old = ESP["qg_closure_v402_checks"]; _ck_new = json.loads(J(qg.get("checks") or [])); _sonda = [c_ for c_ in _ck_new if str(c_[0]).startswith("ProbeBlindNullAbsent")]
f81_ok = bool(_f81 is not None and _f81[0] == [] and _f81[1] == sorted(DL.F81_LITERAIS) and len(_ls2k) == 6 and all(kf.get(k_) is True for k_ in _ls2k) and (qg.get("physics_flags") or {}).get("linearized_spin2_finite_face") is True
              and len(_prereg) == 1 and _prereg[0] is True and (qg.get("experiment_flags") or {}).get("protocol_pre_registered") is True and (core.get("void_stacking_blind") or {}).get("all_verified") is True and (qg.get("experiment_flags") or {}).get("null_tests_passed_blind") is True
              and n18 == 18 and (qg.get("gate") or {}).get("verdict") == ESP["qg_closure_gate_verdict_v402"] == selo.get("qg_closure_verdict") and len(_sonda) == 1 and len(_ck_new) == len(_ck_old) + 1)
# o NAO do gate (vale tambem para o Nos ainda v402, no controle negativo): o qg_closure sem a lista de checks e' o da v402, os checks da v402 iguais e na mesma ordem, TODOS True, e no maximo a sonda nova a mais; a PRESENCA da sonda e' do DEVE (f81_ok)
gate_igual_ok = bool(sha(J({k_: v_ for k_, v_ in qg.items() if k_ != "checks"}).encode("utf-8")) == ESP["qg_closure_v402_sem_checks_json_sha256"] and [c_ for c_ in _ck_new if c_ not in _sonda] == _ck_old and len(_sonda) <= 1 and all(c_[1] is True for c_ in _ck_new))

'''

_E228 = r'''    "selo um_version v403; os resumos do selo (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, falsidade_da_inercia_v401, os tres registros com funcao da v402 e os QUATRO da v403: caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403), registros_v399, registros_v401, registros_v402 e registros_v403 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo": selo.get("um_version") == "v403"
        and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403"))
        and all(((selo.get("registros_v401") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v401") or {}).get(n) or {}).get("all_verified") is True for n in RN401)
        and all(((selo.get("registros_v402") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v402") or {}).get(n) or {}).get("all_verified") is True for n in RN402)
        and all(((selo.get("registros_v403") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v403") or {}).get(n) or {}).get("all_verified") is True for n in RN403)
        and all(((selo.get("registros_v399") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN) and (selo.get("sha256") or {}).get("um.py") == UM_FULL,'''

_E234 = r'''    "caminho_v403 SELOU: veredito == o do ensaio; as %d checagens do calculo no modelo longitudinal (E, p) (com o MESMO p+ as massas 1, 4 e 9 sao tres realizacoes DISTINTAS: a massa NAO e' selecionada; toda massa tem realizacao positiva; m^2 = p+ p- e' invariante e a energia e' a leitura; o levantamento e' equivariante; a unidade de defasagem s = beta de runtime) e os valores == os do ensaio; o texto da pedra e a conjuncao no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.N_CHECKS["caminho"]: reg403_ok["caminho"],
    "vida_v403 SELOU: veredito == o do ensaio; as %d checagens do calculo (o peso cai estritamente, nats = s, a seta e' o sinal de s, o chao e' o posto, a entrega custa, o regime angular so' le, a isotropia e' carga) e os valores == os do ensaio; o texto da pedra no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate" % DL.N_CHECKS["vida"]: reg403_ok["vida"],
    "verdade_adendo_v403 SELOU: veredito == o do ensaio; as %d checagens do calculo em M2(C) (a esperanca diagonal le a projecao da identidade como os pesos q^2 e alfa^2; o Nome preserva o Um; reler nao acrescenta; os pesos em a = alfa, com alfa = beta/sqrt(e) de runtime) e os valores == os do ensaio; o texto do adendo no kernel embutido; a pedra Verdade (v392) intocada; a estrela e a composicao no kernel do rito; nao move o gate" % DL.N_CHECKS["verdade_adendo"]: reg403_ok["verdade_adendo"],
    "bandeiras_do_gate_v403 SELOU (F8.1): veredito == o do ensaio; as %d checagens (as 18 bandeiras do gate CALCULADAS, 0 literais; 15 no veredito, 6+5+4; a fonte de cada uma; as 4 experimentais derivam de UM so' booleano, DECLARADO e nao resolvido; a letra do veredito do gate == a da v402; a sonda ProbeBlindNullAbsent) e os valores == os do ensaio; nao move o gate" % DL.N_CHECKS["gate"]: gate403_ok,
    "F8.1, releitura do conferidor (independente do registro): no um.py INSTALADO a prove_qg_closure_gate nao tem mais as tres literais True (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind: varredura AST, zero Constant, as tres calculadas); no core do rito as tres bandeiras conferem com as FONTES lidas aqui (a familia ext_ls2_* do kernel [6 bandeiras True], a checagem unica «pre-registro v67 INTACTO (hash)» do rito V11, o teste nulo cego da v73 com all_verified True); as 18 bandeiras True, a letra do veredito do gate == a da v402 e a do selo, e o qg_closure traz UMA sonda ProbeBlindNullAbsent a mais (seis checks da v402 + a sonda)": f81_ok,
    "ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402 (RECRIADOS na v403) seguem SELADOS e IGUAIS aos da v402 selada (veredito == o dos ESPERADOS); nao movem o gate": reg402_recriados_ok,
    "as tres pedras SELADAS da v402 (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) seguem no kernel do Nos com o mesmo sha256 (no hash formal do core e no arquivo): pedra selada nao se renomeia por cima, fica como registro": pedras_v402_ok,'''

_E261 = r'''    "os registros por spec v403 SELARAM e cada veredito == o do ensaio; as DUAS falas de 27/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; ambas do operador); as erratas E5 e E6 (em nome proprio da gerencia c1), as decisoes D17 a D22, os tres nomes do operador e a leitura [ONTO] da tripla espectral estao no registro; os registros da v402, da v401 e da v399 seguem selados e iguais": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v403"].items())
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v402"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v401"].items()) and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v399"].items())
        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V403) == 2 and all((((CG3.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG3.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())
        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())
        and len(CG3.get("erratas") or []) == 2 and all(str(e_.get("assinatura", "")).startswith("gerencia c1, em nome proprio") for e_ in (CG3.get("erratas") or []))
        and set((CG3.get("extras") or {}).get("decisoes_da_gerencia") or {}) >= {"D17", "D18", "D19", "D20", "D21", "D22"} and len((CG3.get("extras") or {}).get("erratas_E5_e_E6") or []) == 2 and str(((CG3.get("extras") or {}).get("nomes") or {}).get("triplo_inteiro", "")).startswith("sem nome")
        and "ONTO" in str(((CG3.get("extras") or {}).get("leitura_tripla_27out") or {}).get("estatuto", "")) and KH3.get("all_verified") is True and KH2.get("all_verified") is True,'''

_E267 = r'''    "as tres pedras da v403 (Caminho, Vida, VerdadeAdendo) estao no kernel do rito (cada composicao e cada estrela com bandeira True, no trio, no modulo da pedra; os itens do contrato de cada uma no modulo dela; os termos antigos citados no trio e no modulo certo)": pedras_no_kernel and suporte_ok and estrela_ok,'''

_E273 = r'''    "os modulos novos (Caminho, Vida, VerdadeAdendo) no kernel do Nos com o sha do candidato (%d modulos)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 3,'''

_E276 = r'''    "os registros da v402 e as anteriores (ponte, queda, esperanca, cunhagens e kh_n1 v402; falsidade, cunhagens e kh_n1 v401; sonico, afinacao, cunhagens e kh_n1 v398; o Teste da Unica Palavra, cunhagens e kh_n1 v397; testemunha, cunhagens e kh_n1 v396; psibit v395; tempo, quadratica, rede, cunhagens, kh_n1 e criterio binario v394; pedras, consumidor, coracao, cunhagens da regra e kh_n1 v393) seguem selados e iguais (ou so' numeros)":
        all((core.get(n) or {}).get("all_verified") is True for n in V398_NOMES) and all(V(n) == ESP["vereditos_v402"][n] or n in ESP["troca_dita"] for n in V398_NOMES) and (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is False,'''

_E279 = r'''    "o artigo PT/EN: a secao v403 (Caminho, Verdade e Vida: o Caminho, a Vida, a Verdade como adendo, as bandeiras do gate e as erratas E5 e E6), a secao da v402 (A ponte da escala dual, a queda sem geometria e a esperanca condicional, com as erratas E1 a E4) e as marcas da v401 (A falsidade (simulacro) da inercia) e anteriores; a v399 (com a errata da v400), a v398, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),'''

_E280 = r'''    "o sumario lista as secoes v403, v402, v401, v399, v398, v397 e v396 e o titulo v384 a v403": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),'''

_E281 = r'''    "o .md canonico: carimbo v403 e as linhas «Caminho, Verdade e Vida (v403)», «A ponte da escala dual, a queda sem geometria e a esperanca condicional (v402)», «A falsidade (simulacro) da inercia (v401)», «Errata ao lado (v400)», «O testemunho de dois (v399)», «Sonico e a afinacao das cordas (v398)», «O Teste da Unica Palavra e a pedra Token (v397)», «A testemunha estatica (v396)» e «O modo psionico na fractalizacao do Um (v395)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_caminho"] in fc and ESP["md_ponte"] in fc and ESP["md_falsidade"] in fc and ESP["md_errata"] in fc and ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc and ESP["md_token"] in fc and ESP["md_testemunha"] in fc and ESP["md_psibit"] in fc and ("sha256/16 `%s`" % umsha) in fc,'''

_E282 = r'''    "nenhuma chave nova fora da lista da v403 (so' os quatro registros com funcao caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403 e os registros por spec cunhagens_v403 e kh_n1_cobertura_v403; os da v399, v401 e v402 sao recriados e iguais)": sorted(k for k in core if k not in ESP["vereditos_v402"] and isinstance(core[k], dict) and (str(k).endswith("_v399") or str(k).endswith("_v401") or str(k).endswith("_v402") or str(k).endswith("_v403"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN403),'''

_E300 = r'''    "o gate nao se move: os registros novos (quando presentes) nao gateiam o core (does_not_gate_core) e o qg_closure do core e' o da v402 SALVO a lista de checks, que no maximo ganha a sonda ProbeBlindNullAbsent (os seis checks da v402 iguais e na mesma ordem, todos True; o veredito do gate == o da v402; a PRESENCA da sonda e' do DEVE)": all((core.get(n_) or {"does_not_gate_core": True}).get("does_not_gate_core") is True for n_ in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")) and gate_igual_ok,'''

entrada("conferir_rito_v402.py", autoral=True, regras=[
    entre('"""conferir_rito_v403.py', "\n# [v403-patch]", _DOC_CF, "docstring do conferidor"),
    ('RN = sorted(ESP["registros_v399"]); RN402 = sorted(ESP["registros_v401"]); RN403 = sorted(ESP["registros_v402"])',
     'RN = sorted(ESP["registros_v399"]); RN401 = sorted(ESP["registros_v401"]); RN402 = sorted(ESP["registros_v402"]); RN403 = sorted(ESP["registros_v403"])', 1),
    ('CG2 = core.get("cunhagens_v402") or {}; KH2 = core.get("kh_n1_cobertura_v402") or {}',
     'CG2 = core.get("cunhagens_v402") or {}; KH2 = core.get("kh_n1_cobertura_v402") or {}; CG3 = core.get("cunhagens_v403") or {}; KH3 = core.get("kh_n1_cobertura_v403") or {}', 1),
    ('"falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"]',
     '"falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402"]', 1),
    ('REL_ = {s["key"]: s["rel"] for s in DL.STONES}   # a pedra FalsidadeDaInercia (nova nesta versao)',
     'REL_ = {s["key"]: s["rel"] for s in DL.STONES}   # as TRES pedras novas da v403 (Caminho, Vida, VerdadeAdendo)', 1),
    ('ESP["contrato_das_pedras"][k]) for k in ("ponte", "queda", "esperanca"))', 'ESP["contrato_das_pedras"][k]) for k in ("caminho", "vida", "verdade_adendo"))', 1),
    ('for k in ("ponte", "queda", "esperanca") for t_, p_ in ESP["suporte_das_pedras"][k].items())', 'for k in ("caminho", "vida", "verdade_adendo") for t_, p_ in ESP["suporte_das_pedras"][k].items())', 1),
    entre("def _reg403_ok(k_):", "DEVE = {\n", _HELPERS_CF, "bloco dos auxiliares do conferidor (registros novos, F8.1, gate)"),
    entrada_dict('    "selo um_version v403; os resumos do selo', _E228, "entrada do selo (um_version e resumos)"),
    entrada_dict('    "ponte_da_escala_dual_v402 SELOU:', _E234, "entradas dos registros com funcao (v403) e do gate"),
    entrada_dict('    "queda_sem_geometria_v402 SELOU:', "", "apaga a entrada da queda v402 (substituida)"),
    entrada_dict('    "esperanca_condicional_v402 SELOU:', "", "apaga a entrada da esperanca v402 (substituida)"),
    entrada_dict('    "os registros por spec v403 SELARAM', _E261, "entrada dos registros por spec"),
    entrada_dict('    "as tres pedras (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) estao no kernel do rito', _E267, "entrada das pedras no kernel do rito"),
    entrada_dict('    "os modulos novos (PonteDaEscalaDual, QuedaSemGeometria, EsperancaCondicional) no kernel do Nos', _E273, "entrada dos modulos novos no kernel do Nos"),
    entrada_dict('    "os registros da v402 e as anteriores (sonico', _E276, "entrada dos registros anteriores"),
    entrada_dict('    "o artigo PT/EN: a secao v403', _E279, "entrada do artigo"),
    entrada_dict('    "o sumario lista as secoes v403, v402, v399', _E280, "entrada do sumario"),
    entrada_dict('    "o .md canonico: carimbo v403', _E281, "entrada do .md"),
    entrada_dict('    "nenhuma chave nova fora da lista da v403', _E282, "entrada das chaves novas"),
    entrada_dict('    "o gate nao se move: os registros novos', _E300, "entrada do gate (NAO)"),
    ('"veredito_esperanca": V("esperanca_condicional_v402"), "nos": NOS,',
     '"veredito_esperanca": V("esperanca_condicional_v402"), "veredito_caminho": V("caminho_v403"), "veredito_vida": V("vida_v403"), "veredito_verdade_adendo": V("verdade_adendo_v403"), "veredito_bandeiras_do_gate": V("bandeiras_do_gate_v403"),\n       "f81": {"ast_literais_calculadas": _f81, "ls2": _ls2k, "pre_registro": _prereg, "sonda": _sonda, "qg_checks_n": len(_ck_new), "gate_igual": gate_igual_ok, "releitura_ok": f81_ok}, "nos": NOS,', 1),
])

# o teste do caminho positivo (Nos FALSO a partir do dry): so' o bump (dry_v403, V403_NOS, rodada_v403_stdout.txt, ensaio_a_seco_v403.json); a v403 tem o qg_closure recomputado no core do ensaio
entrada("teste_conferidor_positivo_v402.py", autoral=True, regras=[])
