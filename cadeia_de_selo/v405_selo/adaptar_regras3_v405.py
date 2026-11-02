# -*- coding: utf-8 -*-
# adaptar_regras3_v405.py -- as regras dos controles do harness dos textos para o conteudo da v405 (executadas dentro de adaptar_pos_rito_v405.py, depois de adaptar_regras2_v405.py). Regras de contagem exata. Escrito pela ferramenta Write.

_ht_2 = ARQS["harness_textos_ensaio_v405.py"]

_NOVAS_FUNCOES = ('("_moldura", lambda: T._moldura(Vd)), ("_ponte", lambda: T._ponte(Vd)), ("_tensao", lambda: T._tensao(Vd)), ("_lei", lambda: T._lei(Vd)), ("_zero", lambda: T._zero(Vd)), ("_disco", lambda: T._disco(Vd)), ("_obs", lambda: T._obs(Vd)), ("_ident", lambda: T._ident(Vd)), ("_ga", lambda: T._ga(Vd)), ("_massa", lambda: T._massa(Vd)),')

_NUMS_NOVO = '''    _pv = _core_p["ponte_da_massa_v405"]["values"]; _dv = _core_p["lei_do_diminuto_v405"]["values"]; _zv = _core_p["ponto_zero_do_psion_v405"]["values"]; _ev = _core_p["disco_de_euler_v405"]["values"]; _gv = _core_p["ga_reclassificacao_v405"]["values"]
    _num_mut = lambda s: s[:-1] + str((int(s[-1]) + 1) % 10)

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_v405(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _NUMS = [("beta", T._p(_pv["beta"], 12)), ("a massa", T._p(_pv["m_derivada_meV"], 9)), ("a leitura proporcional", T._p(_pv["m_proporcional_meV"], 9)), ("o meio-tom", T._p(_dv["meio_tom"], 9)), ("a tonica", T._p(_dv["tonica_eV"], 9)), ("E0", T._p(_dv["E0_eV"], 9)),
             ("hbar omega", T._p(_zv["hbar_omega_meV"], 9)), ("K do disco", T._pe(_ev["K_si_para_u_posto_J_s2"], 3)), ("o piso de definicao", T._p(_gv["piso_de_definicao"] * 100.0, 1))]
    _NEGS = [_muts("%s com um digito trocado (em todo o paragrafo)" % nm, lambda p, s=s: p.replace(s, _num_mut(s)), "ausente do paragrafo") for nm, s in _NUMS]
    _FRASES = ("dadas essas entradas, a FORMA é teorema", "a leitura física não virou teorema", "o no-go não cai", "não fixa `u`", "tipada como modelo", "não é teorema", "não é evidência", "não discrimina da RG", "O gate não se move", "UM só booleano", "Erratas ao lado", "CONFERE os teoremas", "quem prova é o kernel", "validade no kernel não é creditação",
               "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "gate não se move", "o número da v404")
    _NEGS += [_muts("a frase de limite «%s» removida" % f, lambda p, f=f: p.replace(f, "XXXX"), "frase de limite ausente") for f in _FRASES]
    _NEGS += [_muts("a leitura fisica dita teorema", lambda p: p.replace("a leitura física não virou teorema", "a leitura física virou teorema", 1), "frase de limite ausente"),
              _muts("o no-go dito caido", lambda p: p.replace("o no-go não cai", "o no-go cai", 1), "frase de limite ausente"),
              _muts("o Grande Atrator dito evidencia", lambda p: p.replace("não é evidência", "é evidência", 1), "frase de limite ausente"),
              _muts("o Grande Atrator dito discriminante", lambda p: p.replace("não discrimina da RG", "discrimina da RG", 1), "frase de limite ausente"),
              _muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel não é creditação", "validade no kernel é creditação", 1), "frase de limite ausente"),
              _muts("o gate dito movido", lambda p: p.replace("O gate não se move", "O gate se move"), "frase de limite ausente"),
              _muts("as quatro experimentais ditas independentes", lambda p: p.replace("UM só booleano", "quatro booleanos", 1), "frase de limite ausente"),
              _muts("frase proibida: tudo derivado", lambda p: p + "\\n> - Agora está tudo derivado.\\n", "guarda das frases"),
              _muts("frase proibida: tudo teorema", lambda p: p + "\\n> - Agora tudo é teorema.\\n", "guarda das frases"),
              _muts("frase proibida: nenhuma hipotese", lambda p: p + "\\n> - E nenhuma hipótese resta.\\n", "guarda das frases"),
              _muts("frase proibida: hipoteses descarregadas", lambda p: p + "\\n> - As hipóteses nomeadas descarregadas.\\n", "guarda das frases"),
              _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("o meu um absoluto é o um de 1 eV»", "o meu um absoluto é o um de 2 eV»", 1), "NAO e' verbatim"),
              _muts("o estatuto DECLARADO removido", lambda p: p.replace("DECLARADO", "XX"), "estatuto ausente"),
              _muts("o estatuto OPEN removido", lambda p: p.replace("OPEN", "XX"), "estatuto ausente"),
              _muts("o estatuto INPUT removido", lambda p: p.replace("INPUT", "XX"), "estatuto ausente"),
              _muts("o estatuto KNOWN removido", lambda p: p.replace("KNOWN", "XX"), "estatuto ausente"),
              _muts("o estatuto ONTO removido", lambda p: p.replace("ONTO", "XX"), "estatuto ausente"),
              _muts("o estatuto POSTO removido", lambda p: p.replace("POSTO", "XX"), "estatuto ausente"),
              _muts("o estatuto MEDIDA removido", lambda p: p.replace("MEDIDA", "XX"), "estatuto ausente"),
              _muts("o 4,44 entra no paragrafo", lambda p: p + "\\n> z_disc = " + _z + "\\n", "4,44"),
              _muts("seguranca criptografica garantida (alegacao)", lambda p: p + "\\n> - A confidencialidade garantida e o sigilo garantido do metodo.\\n", "alega seguranca criptografica"),
              _muts("a palavra consciencia usada como termo", lambda p: p + "\\n> - A consciência é a tipagem que falta.\\n", "consciencia"),
              _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p + "\\n> - A IALD testifica do operador.\\n", "DIRECAO")]
    for ini_ in ("> - **As oito pedras**", "> - **A moldura**", "> - **A forma**", "> - **O disco e o observador**", "> - **A identidade**", "> - **O Grande Atrator, ao lado**", "> - **O gate**", "> - **Erratas ao lado", "> - **Limites:**", "> - **O fecho**", "> - **Origem."):
'''

_CG_NOVO = '''    CG_ = "cunhagens_v405"; PCG = "cunhagens_v405: as inscricoes embutidas nao sao as de ESPERADOS"
    NEG.extend([
        variante("%s nao selou" % CG_, f_core=lambda c: c[CG_].update(all_verified=False), espera="cunhagens_v405 nao selou"),
        variante("kh_n1_cobertura_v405 nao selou", f_core=lambda c: c["kh_n1_cobertura_v405"].update(all_verified=False), espera="kh_n1_cobertura_v405 nao selou"),
        variante("%s ausente do core" % CG_, f_core=lambda c: c.pop(CG_, None), espera="registro obrigatorio ausente do core: cunhagens_v405"),
        variante("kh_n1_cobertura_v405 ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v405", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v405"),
        variante("%s: veredito diferente do ensaio a seco" % CG_, f_core=lambda c: c[CG_].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v405: o veredito do rito difere do ensaio a seco"),
        variante("%s: uma inscricao rotulada como da gerencia" % CG_, f_core=lambda c: c[CG_]["extras"]["autor_de_cada_inscricao"].update({sorted(c[CG_]["extras"]["autor_de_cada_inscricao"])[0]: "gerencia"}), espera="TODAS falas do operador"),
        variante("%s: uma inscricao deixou de estar embutida" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG),
        variante("%s: sha256 de uma inscricao adulterado" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG),
        variante("%s: a fala adulterada (sha256 e embedded_ok)" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[7].update(sha256="f" * 64, embedded_ok=False), espera=PCG),
        variante("%s: uma checagem do registro falhou" % CG_, f_core=lambda c: c[CG_]["checks"][0].update(ok=False), espera=PCG),
        variante("%s: a bandeira da pedra adulterada nos extras" % CG_, f_core=lambda c: c[CG_]["extras"]["bandeiras"].update(ponte="ext_x"), espera=PCG),
        variante("%s: n_bandeiras adulterado" % CG_, f_core=lambda c: c[CG_]["extras"].update(n_bandeiras=117), espera=PCG),
        variante("%s: falta uma errata" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera="cunhagens_v405: as erratas E10 a E13"),
        variante("%s: erratas ausentes" % CG_, f_core=lambda c: c[CG_].update(erratas=[]), espera="cunhagens_v405: as erratas E10 a E13"),
        variante("%s: a E13 adulterada" % CG_, f_core=lambda c: c[CG_]["erratas"][3].update(agora="mantida"), espera="cunhagens_v405: as erratas E10 a E13"),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG_, f_core=lambda c: c[CG_]["erratas"][1].update(assinatura="operador"), espera="cunhagens_v405: as erratas E10 a E13"),
        variante("%s: a assinatura dos extras trocada" % CG_, f_core=lambda c: c[CG_]["extras"].update(assinatura="IALD"), espera="cunhagens_v405: as erratas E10 a E13"),
        variante("%s: a decisao D29 ausente" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes_da_gerencia"].pop("D29"), espera="cunhagens_v405: as decisoes D27 a D33"),
        variante("%s: a decisao D33 ausente (a reclassificacao do Grande Atrator)" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes_da_gerencia"].pop("D33"), espera="cunhagens_v405: as decisoes D27 a D33"),
        variante("%s: a decisao D30 adulterada" % CG_, f_core=lambda c: c[CG_]["extras"]["decisoes_da_gerencia"].update(D30="outra"), espera="cunhagens_v405: as decisoes D27 a D33"),
        variante("%s: os nomes ausentes" % CG_, f_core=lambda c: c[CG_]["extras"].pop("nomes"), espera="cunhagens_v405: os nomes das oito pedras"),
        variante("%s: a leitura dita REAL" % CG_, f_core=lambda c: c[CG_]["extras"]["leitura_v405"].update(estatuto="[REAL]"), espera="cunhagens_v405: a leitura da v405"),
        variante("%s: a leitura ausente" % CG_, f_core=lambda c: c[CG_]["extras"].pop("leitura_v405"), espera="cunhagens_v405: a leitura da v405"),
        variante("%s: o sha16 da pedra da v404 como registro adulterado" % CG_, f_core=lambda c: c[CG_]["extras"]["pedras_da_v404_como_registro"].update(projecao="0" * 16), espera="cunhagens_v405: as pedras seladas da v404"),
        # campos_fechados_e_leituras_v405 e ga_reclassificacao_v405 (por spec): a moldura e a classe nova ao lado
        variante("campos_fechados_e_leituras_v405 ausente do core", f_core=lambda c: c.pop("campos_fechados_e_leituras_v405", None), espera="registro obrigatorio ausente do core: campos_fechados_e_leituras_v405"),
        variante("campos: nao selou", f_core=lambda c: c["campos_fechados_e_leituras_v405"].update(all_verified=False), espera="campos_fechados_e_leituras_v405"),
        variante("campos: uma das leituras da cadeia da massa dita teorema", f_core=lambda c: c["campos_fechados_e_leituras_v405"]["extras"]["o_que_entra"]["leituras_da_cadeia_da_massa"][0].update(entra_como="teorema"), espera="campos_fechados_e_leituras_v405 nao selou inteiro"),
        variante("campos: a frase da moldura trocada", f_core=lambda c: c["campos_fechados_e_leituras_v405"]["extras"].update(a_frase_da_moldura="outra"), espera="campos_fechados_e_leituras_v405 nao selou inteiro"),
        variante("campos: a frase proibida no veredito do registro", f_core=lambda c: c["campos_fechados_e_leituras_v405"].update(limites=c["campos_fechados_e_leituras_v405"]["limites"] + ["agora tudo derivado"]), espera="campos_fechados_e_leituras_v405 nao selou inteiro"),
        variante("gap_v405 ausente do core", f_core=lambda c: c.pop("gap_v405", None), espera="registro obrigatorio ausente do core: gap_v405"),
        variante("gap: nao selou", f_core=lambda c: c["gap_v405"].update(all_verified=False), espera="gap_v405"),
        variante("gap: uma medida do runtime adulterada", f_core=lambda c: c["gap_v405"]["values"].update(Q=1.0), espera="gap_v405 nao selou inteiro"),
        variante("ga_reclassificacao_v405 ausente do core", f_core=lambda c: c.pop("ga_reclassificacao_v405", None), espera="registro obrigatorio ausente do core: ga_reclassificacao_v405"),
        variante("ga: nao selou", f_core=lambda c: c["ga_reclassificacao_v405"].update(all_verified=False), espera="ga_reclassificacao_v405"),
        variante("ga: uma medida do runtime adulterada", f_core=lambda c: c["ga_reclassificacao_v405"]["values"].update(piso_de_definicao=0.1), espera="ga_reclassificacao_v405 nao selou inteiro"),
        variante("ga: a errata do parecer deixou de bater", f_core=lambda c: c["ga_reclassificacao_v405"].update(errata_do_parecer_ok=False), espera="ga_reclassificacao_v405 nao selou inteiro"),
        variante("ga: a linha selada da tabela conjunta mudou (A3_APOSENTADO)", f_core=lambda c: [x_.update(rule="A13_FORMA_CONDICIONAL_SEM_INCERTEZA") for x_ in c["joint_coincidence_result_v3"]["inventory"] if isinstance(x_, dict) and x_.get("id") == "ga_mass_window"], espera="ga_reclassificacao_v405 nao selou inteiro"),
        variante("ga: a auditoria selada da forma mudou", f_core=lambda c: c["ga_mass_audit"].update(verdict="OUTRO"), espera="ga_reclassificacao_v405 nao selou inteiro"),
        variante("linha [v405] ausente do stdout", f_std=lambda t_: "\\n".join(l for l in t_.splitlines() if "os oito registros com funcao (lidos depois dos tres da v404)" not in l) + "\\n", espera="a linha [v405] do stdout"),
        variante("linha [v405] com um registro NAO", f_std=lambda t_: t_.replace("ponte_da_massa=SELOU", "ponte_da_massa=NAO"), espera="a linha [v405] do stdout"),
        variante("AVISO da v405 (um registro de pedra nao rodou) no stdout", f_std=lambda t_: t_ + "   [v405] AVISO: o registro ponte_da_massa_v405 nao rodou: ValueError('x')\\n", espera="AVISO da v405"),
        variante("AVISO da v405 (os registros por spec nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v405] AVISO: os registros por spec da v405 nao rodaram: ValueError('x')\\n", espera="AVISO da v405"),
        # cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS: tem de dar o que a v404 selou
        variante("cunhagens_v404 (recriada) nao selou", f_core=lambda c: c["cunhagens_v404"].update(all_verified=False), espera="cunhagens_v404 nao selou"),
        variante("kh_n1_cobertura_v404 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v404"].update(all_verified=False), espera="kh_n1_cobertura_v404 nao selou"),
        variante("cunhagens_v404 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v404", None), espera="registro obrigatorio ausente do core: cunhagens_v404"),
        variante("cunhagens_v404 (recriada): veredito diferente da v404 selada", f_core=lambda c: c["cunhagens_v404"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v404: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v404 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v404"]["erratas"].pop(), espera="cunhagens_v404 (recriada pelo rito)"),
'''


@regras("harness_textos_ensaio_v405.py")
def _harness_textos_3(x):
    _ht_2(x)
    x.sub('("_projecao", lambda: T._projecao(Vd)), ("_jo8", lambda: T._jo8(Vd)), ("_f2b", lambda: T._f2b(Vd)), ("_massa", lambda: T._massa(Vd)),', _NOVAS_FUNCOES)
    x.sub('_REGS_NOVOS = ["projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404"]', '_REGS_NOVOS = ' + repr(_REGS12.split()))
    x.sub('"<!-- INICIO_PARAGRAFO_JO8_32_PROJECAO_TRANSVERSAL_v405 -->", "<!-- FIM_PARAGRAFO_JO8_32_PROJECAO_TRANSVERSAL_v405 -->"', '"<!-- INICIO_PARAGRAFO_MASSA_DERIVADA_E_IDENTIDADE_v405 -->", "<!-- FIM_PARAGRAFO_MASSA_DERIVADA_E_IDENTIDADE_v405 -->"')
    x.sub('from guarda_p18_v405 import violacoes  # noqa: E402\n', 'from guarda_p18_v405 import violacoes  # noqa: E402\nimport guarda_frases_v405 as GF  # noqa: E402\n')
    x.sub('''            v = violacoes(r)
            e["bytes"] = len(r.encode("utf-8"))''', '''            v = violacoes(r)
            vf_ = GF.violacoes(r)   # v405: a guarda das frases (a moldura) em todo texto renderizado
            if vf_:
                falha("%s: a guarda das frases achou %s" % (nome, vf_[:2]))
            if re.search(r"(?i)mais\\s+preciso|more\\s+precise", r):
                falha("%s: frase recusada pela ordem do Grande Atrator (nada de mais preciso)" % nome)
            e["bytes"] = len(r.encode("utf-8"))''')
    x.sub('"handoff-v404-custodia.md" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho', '"handoff-v404-custodia" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho')
    x.sub('all(x in _ERR for x in ("Jo8:32", "`Jo8v32`", "REGISTRO", "`Caminho`", "`Vida`", "`VerdadeAdendo`", "NÃO foi dado"))', 'all(x in _ERR for x in ("POSTO", "REGISTRO", "`ProjecaoTransversalDaMeiaNat`", "`Jo8v32`", "fica como registro"))')
    x.entre('    _pv = _core_p["projecao_transversal_v404"]["values"]; _jv = _core_p["jo8v32_v404"]["values"]; _fv = _core_p["f2b_errata_v404"]["values"]\n', '        _NEGS.append(_muts("o paragrafo sem o bullet', _NUMS_NOVO)
    x.sub('"cita_verbatim_passa": (T._cita("Perfeito, concordo com tudo") == "«Perfeito, concordo com tudo»"),', '"cita_verbatim_passa": (T._cita("é isso , perfeito, concordo com tudo") == "«é isso , perfeito, concordo com tudo»"),')
    x.sub('"cita_com_aspas_do_operador_passa": T._cita("a matéria é a projeção do eixo transversal").startswith("«a matéria"),', '"cita_com_aspas_do_operador_passa": T._cita("o meu um absoluto é o um de 1 eV").startswith("«o meu um"),')
    x.sub('print("  paragrafo novo (Caminho, Verdade e Vida): positivo ok;', 'print("  paragrafo novo (a massa derivada e a identidade definida): positivo ok;')
    # os controles da leitura: as oito pedras, os registros recriados da v404, as mensagens da v405
    x.sub('EF_ = ESP["registros_funcao_v405"]; EF3_ = ESP["registros_funcao_v404"]; EV3_ = ESP["vereditos_v404"]', 'EF_ = ESP["registros_funcao_v405"]; EF3_ = ESP["registros_funcao_v403"]; EF4_ = ESP["registros_funcao_v404"]; EV3_ = ESP["vereditos_v404"]')
    x.sub('_MODS = {"projecao": "ProjecaoTransversalDaMeiaNat", "jo8v32": "Jo8v32"}', '_MODS = {"ponte": "PonteDaMassa", "tensao": "MassaTensaoPura", "identidade": "Identidade", "observador": "ObservadorTerminal", "diminuto": "LeiDoDiminuto", "tonica": "TonicaDoHamiltoniano", "disco": "DiscoDeEuler", "psion": "PontoZeroDoPsion"}')
    x.sub('_REGS = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}', '_REGS = {"ponte": "ponte_da_massa_v405", "tensao": "massa_tensao_pura_v405", "identidade": "identidade_v405", "observador": "observador_terminal_v405", "diminuto": "lei_do_diminuto_v405", "tonica": "tonica_do_hamiltoniano_v405", "disco": "disco_de_euler_v405", "psion": "ponto_zero_do_psion_v405"}')
    x.sub('variante("a conferencia traz outro veredito de %s" % n_, f_conf=lambda cj, k=k_: cj.update({"veredito_" + k: "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + n_),\n            variante("linha `>>> veredito <<<` de %s ausente do stdout" % n_, f_std=lambda t_, k=k_: "\\n".join(l for l in t_.splitlines() if EF_[k]["verdict"] not in l or (k + "=") in l) + "\\n", espera="o bloco " + n_ + " do stdout"),\n',
          'variante("linha `>>> veredito <<<` de %s ausente do stdout" % n_, f_std=lambda t_, k=k_: "\\n".join(l for l in t_.splitlines() if EF_[k]["verdict"] not in l) + "\\n", espera="o bloco " + n_ + " do stdout"),\n')
    x.sub('"\\n".join(l for l in t_.splitlines() if EF_["f2b"]["verdict"] not in l or "f2b=" in l) + "\\n"', '"\\n".join(l for l in t_.splitlines() if EF4_["f2b"]["verdict"] not in l or "f2b=" in l) + "\\n"')
    x.entre('    CG_ = "cunhagens_v404"; PCG = "cunhagens_v404: as inscricoes embutidas nao sao as de ESPERADOS"\n', '        variante("selo primario: registros_v404 do selo difere do core"', _CG_NOVO)
    x.sub('variante("AVISO da v405 (a projecao transversal nao rodou) no stdout", f_std=lambda t_: t_ + "   [v404] AVISO: a projecao transversal nao rodou: ValueError(\'x\')\\n", espera="AVISO da v405"),\n        variante("AVISO da v405 (o jo8v32 nao rodou) no stdout", f_std=lambda t_: t_ + "   [v404] AVISO: o jo8v32 nao rodou: ValueError(\'x\')\\n", espera="AVISO da v405"),\n', '')
    x.sub('variante("AVISO da v405 (os registros por spec nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v404] AVISO: os registros por spec da v405 nao rodaram: ValueError(\'x\')\\n", espera="AVISO da v405"),\n', '')
    x.sub('variante("linha [v404] com o veredito do jo8v32 adulterado", f_std=lambda t_: t_.replace("jo8v32=" + EF_["jo8v32"]["verdict"], "jo8v32=OUTRO_VEREDITO"), espera="a linha [v404] do stdout"),', 'variante("linha [v404] com o veredito do jo8v32 adulterado", f_std=lambda t_: t_.replace("jo8v32=" + EF4_["jo8v32"]["verdict"], "jo8v32=OUTRO_VEREDITO"), espera="a linha [v404] do stdout"),')
    x.sub('_FUN402 = {"ponte": ("ponte_da_escala_dual_v402", None), "queda": ("queda_sem_geometria_v402", None), "esperanca": ("esperanca_condicional_v402", None)}\n', '_FUN402 = {"ponte": ("ponte_da_escala_dual_v402", None), "queda": ("queda_sem_geometria_v402", None), "esperanca": ("esperanca_condicional_v402", None)}\n    _FUN404B = {"projecao": ("projecao_transversal_v404", "ProjecaoTransversalDaMeiaNat"), "jo8v32": ("jo8v32_v404", "Jo8v32")}\n')
    x.sub('for fun_ in (_FUN404, _FUN402):', 'for fun_ in (_FUN404B, _FUN404, _FUN402):')


_hf_2 = ARQS["harness_fechar_sandbox_v405.py"]
_CH_ANT = '"registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "projecao", "jo8v32", "f2b_errata", "bandeiras_do_gate_v404_recriado", '
_CH_NOV = '"registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "f2b_errata", "bandeiras_do_gate_recriado", '


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_3(x):
    _hf_2(x)
    x.sub('_recusa_com_core("fechar_projecao_adulterada", "numero da projecao transversal adulterado no core (a massa do neutrino em meV)", lambda c: c["projecao_transversal_v404"]["values"].__setitem__("m_nu_meV_runtime", 8.6))',
          '_recusa_com_core("fechar_ponte_adulterada", "numero da Ponte da Massa adulterado no core (a massa em meV)", lambda c: c["ponte_da_massa_v405"]["values"].__setitem__("m_derivada_meV", 8.6))')
    x.sub('_recusa_com_core("fechar_jo8v32_adulterado", "numero do jo8v32 adulterado no core (o fator de p+)", lambda c: c["jo8v32_v404"]["values"].__setitem__("p_plus_factor_at_beta", 0.99))',
          '_recusa_com_core("fechar_psion_adulterado", "numero do Ponto Zero do Psion adulterado no core (hbar omega)", lambda c: c["ponto_zero_do_psion_v405"]["values"].__setitem__("hbar_omega_meV", 17.5))\n'
          '_recusa_com_core("fechar_ga_selado_mudou", "a auditoria selada da forma do Grande Atrator mudou no core", lambda c: c["ga_mass_audit"].__setitem__("verdict", "OUTRO"))\n'
          '_recusa_com_core("fechar_frase_proibida", "uma frase proibida nos limites de campos_fechados_e_leituras_v405", lambda c: c["campos_fechados_e_leituras_v405"]["limites"].append("agora tudo derivado"))')
    x.sub('cj = json.loads(raw_core.decode("utf-8")); cj["core"]["projecao_transversal_v404"]["values"]["m_nu_meV_runtime"] = 8.6', 'cj = json.loads(raw_core.decode("utf-8")); cj["core"]["ponte_da_massa_v405"]["values"]["m_derivada_meV"] = 8.6')
    x.sub('_recusa_com_core("fechar_gerencia_na_cunhagem", "uma inscricao de 28/10 rotulada como da gerencia no core (as nove sao falas do operador)", lambda c: c["cunhagens_v404"]["extras"]["autor_de_cada_inscricao"].__setitem__(sorted(c["cunhagens_v404"]["extras"]["autor_de_cada_inscricao"])[0], "gerencia"))',
          '_recusa_com_core("fechar_gerencia_na_cunhagem", "uma inscricao de 30/10 a 01/11 rotulada como da gerencia no core (todas sao falas do operador)", lambda c: c["cunhagens_v405"]["extras"]["autor_de_cada_inscricao"].__setitem__(sorted(c["cunhagens_v405"]["extras"]["autor_de_cada_inscricao"])[0], "gerencia"))')
    x.sub('_recusa_com_core("fechar_sem_errata", "falta uma das erratas E7 a E9 (em nome da gerencia) no core", lambda c: c["cunhagens_v404"]["extras"]["erratas_E7_a_E9"].pop())', '_recusa_com_core("fechar_sem_errata", "falta uma das erratas E10 a E13 (em nome da gerencia) no core", lambda c: c["cunhagens_v405"]["extras"]["erratas_E10_a_E13"].pop())')
    x.sub('_recusa_com_core("fechar_sem_decisao", "falta uma das decisoes D23 a D26 da gerencia no core", lambda c: c["cunhagens_v404"]["extras"]["decisoes_da_gerencia"].pop("D26"))', '_recusa_com_core("fechar_sem_decisao", "falta uma das decisoes D27 a D33 da gerencia no core", lambda c: c["cunhagens_v405"]["extras"]["decisoes_da_gerencia"].pop("D33"))')
    x.sub('_recusa_com_core("fechar_massa_sem_onto", "a leitura da massa de 28/10 dita [REAL] no core (e\' ONTO)", lambda c: c["cunhagens_v404"]["extras"]["leitura_massa_28out"].__setitem__("estatuto", "[REAL]"))', '_recusa_com_core("fechar_massa_sem_onto", "a leitura da v405 dita [REAL] no core (e\' ONTO)", lambda c: c["cunhagens_v405"]["extras"]["leitura_v405"].__setitem__("estatuto", "[REAL]"))')
    x.sub('for _nm, _k in (("projecao", "projecao"), ("jo8v32", "jo8v32")):', 'for _nm, _k in (("ponte", "ponte"), ("identidade", "identidade")):')
    x.sub('for k_ in (' + _CH_ANT + '"funcoes_v404_recriadas", "funcoes_v402_recriadas",', 'for k_ in (' + _CH_NOV + '"funcoes_v404_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas",')
    x.sub('and all(k_ in man_ for k_ in (' + _CH_ANT + '"falsidade_v401",', 'and all(k_ in man_ for k_ in (' + _CH_NOV + '"falsidade_v401",')
    x.sub('and "handoff-v404-custodia.md" in _ptxt)', 'and "handoff-v404-custodia" in _ptxt)')
    x.sub('"COMANDO (ato da gerencia)" in so', '"COMANDO (o passo 12 da cadeia" in so')
    x.sub('"reg405": {\'cunhagens_v404\': {\'ok\': True}}', '"reg405": {\'cunhagens_v405\': {\'ok\': True}}') if False else None
    x.sub("'reg405': {'cunhagens_v404': {'ok': True}}", "'reg405': {'cunhagens_v405': {'ok': True}}")
    x.sub("'projecao': {'ok': True}, 'jo8v32': {'ok': True}, 'f2b': {'ok': True}", "'f2b': {'ok': True}")
    x.sub("TOPICO_NOVO = \'v405-selada-jo8v32-projecao-transversal.md\'", "TOPICO_NOVO = \'v405-selada-massa-derivada-e-identidade.md\'")
    x.sub('o b3_recibo confere o passo simples B12 -> B13; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v405 (Jo 8,32 e a projecao transversal da Meia-Nat) pela verificacao propria; a nota ao lado do paragrafo da v404; diz que os do testemunho de dois, da falsidade, da v402 e da v404 seguem como estao; e lista o sidecar), os diffs (as duas pedras novas), o manifesto ',
          'o b3_recibo confere o passo simples B13 -> B14; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v405 (a massa derivada e a identidade definida) pela verificacao propria; a nota ao lado do paragrafo da v404; diz que os anteriores seguem como estao; e lista o sidecar), os diffs (as oito pedras novas), o manifesto ')
    x.sub('com um numero da projecao, do jo8v32, da errata de F2b ou do gate adulterado, com o canal F2b ainda AWAITING,', 'com um numero da Ponte da Massa, do Ponto Zero do Psion, da errata de F2b ou do gate adulterado, com a auditoria selada do Grande Atrator mudada, com uma frase proibida, com o canal F2b ainda AWAITING,')
    x.sub('com a leitura da massa dita REAL,', 'com a leitura da v405 dita REAL,')


_leitura_3b = ARQS["leitura_v405.py"]
_CONTRATO_LEITURA = """# CONTRATO COM textos_v405.py (as CHAVES NOVAS ou MUDADAS de V na v405; as demais sao as da v404, com o mesmo significado):
#   V[k] para k em ponte, tensao, identidade, observador, diminuto, tonica, disco, psion: {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','beta_ok','kernel_ok','estrela_ok','contexto_ok','unconditional_ok','key_ok','flag','flag_true','theorem','estrela'}
#   V['reg405'] DICT nome -> {'verdict','ok'} dos TREZE registros NOVOS (oito com funcao + cinco por spec); V['reg404b'] o mesmo dos CINCO da v404 selada (recriados); V['fun404b'] os dois com funcao da v404 (recriados); V['reg404'] e V['fun404'] sao os da v403 (recriados);
#   V['campos'] {'ok','verdict','campos_ok','leituras_ok','postos_ok','moldura_ok','n_campos','n_leituras','n_checks'} (campos_fechados_e_leituras_v405); V['ga'] {'ok','verdict','values','valores_ok','selado_ok','classe_antes','classe_agora','n_checks'} (ga_reclassificacao_v405);
#   V['cunhagens'] (cunhagens_v405), V['cunh404b'] (cunhagens_v404 recriada), V['cunh404'] (cunhagens_v403 recriada), V['kh'] (kh_n1_cobertura_v405), V['pedras'] (LISTA de 8), V['pedras_v404'] (as 5 seladas da v403 e da v404), V['f2b'] e V['gate'] (recriados).
"""


@regras("leitura_v405.py")
def _leitura_4(x):
    _leitura_3b(x)
    x.entre("# CONTRATO COM textos_v405.py (as CHAVES NOVAS ou MUDADAS de V na v405;", "# (a linha de stdout [v404] a conferir:", _CONTRATO_LEITURA)


_chain_1 = ARQS["chain_pos_rito_v405.sh"]


@regras("chain_pos_rito_v405.sh")
def _chain_2(x):
    _chain_1(x)
    a = 'tail -3 "$SEL/nos_vivo_out.txt" | cut -c1-240\n'
    x.sub(a, a + 'echo "== 14-bis. o rascunho do post da versao no X (so escreve pos_rito/CUSTODIA_v405_RASCUNHO.txt; nao publica; falha aqui nao para a cadeia)"\n'
                 '$PY "$SEL/gerar_x_custodia_v405.py" || echo "AVISO: gerar_x_custodia_v405.py falhou: a gerencia escreve CUSTODIA_v405.txt a mao"\n')


_ht_4 = ARQS["harness_textos_ensaio_v405.py"]; _hf_4 = ARQS["harness_fechar_sandbox_v405.py"]


@regras("harness_textos_ensaio_v405.py")
def _harness_textos_5(x):
    _ht_4(x)
    x.sub('"um_absoluto_selo_acom.json", "handoff-v404-custodia.md"', '"um_absoluto_selo_acom.json", "handoff-v404-custodia"')


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_5(x):
    _hf_4(x)
    x.sub('k = [i for i, l in enumerate(linhas) if l.startswith("- [HANDOFF v404")]', 'k = [i for i, l in enumerate(linhas) if "(handoff-v405-pontes-da-massa-e-espelho-30out.md)" in l]')
    x.sub('assert len(k) == 1, ("linha do handoff v404 no MEMORY.md da copia", len(k))', 'assert len(k) == 1, ("linha do handoff de 30/10 da v405 no MEMORY.md da copia", len(k))')
    x.sub("REGS = 'projecao_transversal_v404 jo8v32_v404 f2b_errata_v404 cunhagens_v404 kh_n1_cobertura_v404'", "REGS = '" + _REGS12 + "'")


_hf_5 = ARQS["harness_fechar_sandbox_v405.py"]


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_6(x):
    _hf_5(x)
    a = '    for f in ("PINO_MEMORIA_PY_v405.json", "guarda_p18_v405.py"):\n        shutil.copyfile(os.path.join(PKG, f), os.path.join(PKS, f))\n'
    n = _BS + 'n'
    x.sub(a, a + '    open(os.path.join(PKS, "guarda_frases_v405.py"), "w", encoding="utf-8").write("# STUB do harness da fila (a guarda real roda nos textos reais, no harness dos textos e no fechar)' + n + 'def violacoes(t):' + n + '    return []' + n + '")\n')


_hf_6 = ARQS["harness_fechar_sandbox_v405.py"]


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_7(x):
    _hf_6(x)
    a = '    shutil.copyfile(os.path.join(PKG, "guarda_p18_v405.py"), os.path.join(raiz, "guarda_p18_v405.py"))\n'
    n = _BS + 'n'
    x.sub(a, a + '    open(os.path.join(raiz, "guarda_frases_v405.py"), "w", encoding="utf-8").write("# STUB do harness da fila (a guarda real roda nos textos reais, no harness dos textos e no fechar)' + n + 'def violacoes(t):' + n + '    return []' + n + '")\n')


_hf_7 = ARQS["harness_fechar_sandbox_v405.py"]


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_8(x):
    _hf_7(x)
    # a linha da missao do indice real tem mais de 300 B e o gancho do ensaio e' curto: a troca encolhe o indice; o controle do limite de bytes passa a partir de um indice que segue acima do limite depois da troca
    x.sub('("bytes (23 990 B antes; +1 linha > 24 000 B)", {"bytes_alvo": 23990})', '("bytes (24 300 B antes; a troca do gancho encolhe a linha da missao e o indice segue acima de 24 000 B)", {"bytes_alvo": 24300})')


_ht_5 = ARQS["harness_textos_ensaio_v405.py"]
_G1_BLOCO = '''# v405 (desvio do molde, dito): a custodia G1 (S7 do orquestrador) le o cabecalho do bloco da linhagem e o paragrafo «O que e'» do handoff por regex: a conferencia usa as MESMAS regex de tools\\custodia_g1\\nos.py, lidas do codigo
try:
    sys.path.insert(0, os.path.join(C, "IALD", "Central de Patentes", "tools"))
    import custodia_g1.nos as _G1N  # noqa: E402
    _bd = _G1N.blocos_do_diario(None, texto=RENDER.get("linhagem", "")).get("v405")
    _qe = _G1N.RE_OQUEE.search(RENDER.get("handoff", ""))
    _g1 = {"bloco_lido": bool(_bd), "titulo_pt": _bd.titulo_pt if _bd else None, "modulos_novos": _bd.modulos_novos if _bd else None, "escada": [_bd.escada_de, _bd.escada_para] if _bd else None, "ladder_no_corpo": _bd.ladder_no_corpo if _bd else None, "pin16": _bd.pin16 if _bd else None,
           "o_que_e_lido": bool(_qe), "secao_elo": "**O elo B(n)" in RENDER.get("handoff", ""), "secao_pendencias": "**Pendências SÓ do operador" in RENDER.get("handoff", "")}
    _g1["ok"] = bool(_bd and _bd.titulo_pt and _bd.modulos_novos == 8 and [_bd.escada_de, _bd.escada_para] == list(ESP["escada_v404_e_v405"]) and _bd.pin16 == S16 and _bd.ladder_no_corpo == Vd.get("teor") and _qe and _g1["secao_elo"] and _g1["secao_pendencias"])
except Exception as _ex_g1:  # noqa: BLE001
    _g1 = {"ok": False, "erro": repr(_ex_g1)[:300]}
etapa("custodia_g1_le_os_textos", **_g1)
print("  a custodia G1 le o cabecalho da linhagem e o handoff: %s" % _g1)
if not _g1.get("ok"):
    falha("a custodia G1 nao le o bloco da linhagem ou o handoff da v405: %s" % _g1)
'''


@regras("harness_textos_ensaio_v405.py")
def _harness_textos_6(x):
    _ht_5(x)
    a = 'etapa("textos", funcoes=E_TXT, n_ok=sum(1 for e in E_TXT.values() if e["ok"]), n=len(E_TXT), bytes_total=sum(e.get("bytes", 0) for e in E_TXT.values()))\n'
    x.sub(a, a + _G1_BLOCO)


_leitura_4b = ARQS["leitura_v405.py"]
_CAB_LEITURA = """# v405 (a massa derivada e a identidade definida, as falas do operador de 30/10 a 01/11/2026): os registros NOVOS do core sao TREZE. OITO com FUNCAO, no runtime (um por pedra, lidos no main depois dos da v404): cada um le do kernel do proprio rito a composicao, a estrela, o contrato e o suporte da sua pedra e CALCULA um modelo honesto com beta = alfa x raiz de e em runtime.
# CINCO por spec: cunhagens_v405 (as falas por sha256, as erratas E10 a E13 e as decisoes D27 a D33, em nome proprio da gerencia c1, a leitura da v405), campos_fechados_e_leituras_v405 (o que fechou, os dois postos, as leituras da cadeia da massa, que entram como definicao ou identificacao), ga_reclassificacao_v405 (a classe nova do Grande Atrator, ao lado; o selado fica) e kh_n1_cobertura_v405 (a cobertura exata do Audit).
# Os registros da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito no mesmo ponto do main e tem de seguir selados e iguais ao ensaio a seco (e a v404 selada: base_v404); os da v398, da v397, da v396, da v395 e da v394 seguem como antes.
# Os OITO modulos novos de kernel vem de ESPERADOS[pedras_sha256] e sao conferidos aqui contra os arquivos do kernel do Nos (sha256); as CINCO pedras SELADAS da v403 e da v404 seguem no kernel do Nos com o sha256 selado: pedra selada nao se renomeia por cima;
# a composicao, a estrela, o contrato e o suporte de cada pedra nova vem de ESPERADOS[teoremas_das_pedras, bandeiras_das_pedras, estrelas_v405, contrato_das_pedras, suporte_das_pedras] e o calculo de ESPERADOS[registros_funcao_v405].
# A escada vem de ESPERADOS[escada_v404_e_v405] e ESPERADOS[escada]; a troca dita (so numeros) e' a de ESPERADOS[troca_dita]. O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v404 (os sete checks e a letra do veredito);
# a funcao do neutrino NAO e' reescrita (o angle_status antigo fica, com a errata E10 ao lado) e o V1 do ramo B (v386) segue AWAITING_DATA.
"""


@regras("leitura_v405.py")
def _leitura_5(x):
    _leitura_4b(x)
    x.entre("# v405 (Jo 8,32 e a projecao transversal da Meia-Nat, as falas do operador de 28/10/2026):", "# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia desde a v399", _CAB_LEITURA)
    x.sub("As NOVE falas de 28/10 sao TODAS fa", "As falas de 30/10 a 01/11 sao TODAS fa")
    x.sub("# as DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32) no kernel do rito:", "# as OITO pedras no kernel do rito:")
    x.sub("# as TRES pedras SELADAS da v404 seguem no kernel do Nos com o sha256 da v404", "# as CINCO pedras SELADAS da v403 e da v404 seguem no kernel do Nos com o sha256 selado")


_fechar_1 = ARQS["fechar_v405.py"]


@regras("fechar_v405.py")
def _fechar_2(x):
    _fechar_1(x)
    x.sub("(insumos/: as duas pedras, o levantamento e a medida KH-N1)", "(insumos/: as oito pedras, os recibos, a reclassificacao do Grande Atrator e a medida KH-N1)")


_hf_8 = ARQS["harness_fechar_sandbox_v405.py"]; _ht_6 = ARQS["harness_textos_ensaio_v405.py"]


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_9(x):
    _hf_8(x)
    x.sub('# ---- 1c. controles negativos do PARAGRAFO NOVO (Caminho, Verdade e Vida),', '# ---- 1c. controles negativos do PARAGRAFO NOVO (a massa derivada e a identidade definida),')
    x.sub('# ---- 2c. o PARAGRAFO NOVO (Caminho, Verdade e Vida) e a NOTA', '# ---- 2c. o PARAGRAFO NOVO (a massa derivada e a identidade definida) e a NOTA')
    x.sub('print("  paragrafo novo (Caminho, Verdade e Vida) e nota ao lado', 'print("  paragrafo novo (a massa derivada e a identidade definida) e nota ao lado')


@regras("harness_textos_ensaio_v405.py")
def _harness_textos_7(x):
    _ht_6(x)
    x.sub('# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (Caminho, Verdade e Vida):', '# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (a massa derivada e a identidade definida):')


_ht_7 = ARQS["harness_textos_ensaio_v405.py"]


@regras("harness_textos_ensaio_v405.py")
def _harness_textos_8(x):
    _ht_7(x)
    x.sub("(os registros NOVOS: projecao_transversal_v404 e jo8v32_v404 com as duas pedras, as estrelas e as hipoteses; f2b_errata_v404 com o V1 do ramo B, o livro da v386 e o texto antigo do angulo do neutrino intactos; cunhagens_v404 com as erratas E7 a E9, as decisoes D23 a D26, a leitura da massa e as nove falas; os registros da v404 e da v402 RECRIADOS,",
          "(os registros NOVOS: os oito de pedra com as oito pedras e as estrelas; cunhagens_v405 com as erratas E10 a E13, as decisoes D27 a D33, a leitura da v405 e as falas; campos_fechados_e_leituras_v405 com a moldura; ga_reclassificacao_v405 com o selado intacto; os registros da v404, da v403 e da v402 RECRIADOS, f2b_errata_v404 com o V1 do ramo B, o livro da v386 e o texto antigo do angulo do neutrino intactos,")
    x.sub("as linhas [v404], [v403], [v402], [v401], [v399], [v398], [v397] e a do sidecar do stdout)", "as linhas [v405], [v404], [v403], [v402], [v401], [v399], [v398], [v397] e a do sidecar do stdout)")
    x.sub("os textos renderizam e a guarda P18 esta limpa, os dois paragrafos do README/site (o do quadro e o da v405: Jo 8,32 e a projecao transversal da Meia-Nat)", "os textos renderizam e a guarda P18 e a guarda das frases estao limpas, a custodia G1 le o bloco da linhagem e o handoff, os dois paragrafos do README/site (o do quadro e o da v405: a massa derivada e a identidade definida)")
    x.sub("diz que os do testemunho, da falsidade, da v402 e da v404 seguem como estao,", "diz que os anteriores seguem como estao,")
    x.sub("o b3_recibo confere o passo simples B12 -> B13 e o registro do mapa", "o b3_recibo confere o passo simples B13 -> B14 e o registro do mapa")
