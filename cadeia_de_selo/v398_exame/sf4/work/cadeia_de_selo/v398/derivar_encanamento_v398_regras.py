# -*- coding: utf-8 -*-
# regras (lote A) de derivar_encanamento_v398.py (exec no escopo dele: `entrada(src, dst=None, regras=[(antigo_depois_do_mapa, novo, contagem), ...], com_bump=True, autoral=False)`)
# O MAPA muda 396 -> 397 e 397 -> 398 em todo o texto, MENOS nos identificadores protegidos (nomes nascidos no um.py); as regras abaixo corrigem o que o mapa nao pode saber: conteudo especifico das pedras
# (Token -> Sonico e AfinacaoDasCordas), o ponto de chamada novo (o sonico e a afinacao logo depois da testemunha, na fractalizacao do Um), os rotulos que o mapa subiu e nao devia (o "[v397]" do print do registro
# de veracidade e o rotulo "v396" do grupo da testemunha) e B7 -> B8. Cada regra tem contagem exata; nada e' executado.
# AUTORAIS (a logica muda; uma subida mecanica nao basta): delta, registros, runtime_pedras, gerar_candidato, os .pysnip, preparar_kernel, pos_build_kernel, copiar_insumos, copiar_base, copiar_pedras e o pos_rito; e, depois da subida mecanica
# abaixo (autoral=True: o derivador NAO sobrescreve o que ja' existe e difere), editados a mao: p00_precondicoes, ensaio_a_seco, conferir_rito, gerar_esperados, gerar_estado, gerar_registro_mapa_prep, conferir_citacoes, comparar e derivar_instalar_rito.

# ------------------------------------------------------------------------------------------- guarda P18 (identica; so' o mapa e o nome)
entrada("guarda_p18_v397.py")

# ------------------------------------------------------------------------------------------- o QUADRO do Teste da Unica Palavra (v397): COPIAS que a cadeia v398 so' IMPORTA para conferir (o quadro nao se mexe; os nomes ficam)
entrada("runtime_quadro_v397.py", dst="runtime_quadro_v397.py", com_bump=False)
entrada("quadro_v397.py", dst="quadro_v397.py", com_bump=False, regras=[
    ("import delta_v397 as DL  # noqa: E402", "import delta_v398 as DL  # noqa: E402", 1),
    ('"""quadro_v397.py -- o lado da CADEIA do quadro', '"""quadro_v397.py [copia na cadeia v398: so\' o import do delta mudou; o quadro nao se mexe] -- o lado da CADEIA do quadro', 1),
])

# ------------------------------------------------------------------------------------------- refazer_* (sandbox, arvore pos-selo, candidato)
entrada("refazer_arvore_v397_pos_selo.py")
entrada("refazer_sandbox_v397.sh", regras=[
    ("a v397 instalada: sem a pasta probe\\ de rascunhos e sem a pedra compilada em .lake/build, entao o build COMPILA A PEDRA A FRIO, como o rito", "a v397 instalada: sem a pasta probe\\ de rascunhos e sem as pedras compiladas em .lake/build, entao o build COMPILA AS PEDRAS A FRIO, como o rito", 1),
    ("acrescenta a pedra Token e GERA a raiz e o Audit", "acrescenta as pedras Sonico e AfinacaoDasCordas e GERA a raiz e o Audit", 1),
])
entrada("refazer_sandbox_v397_pos_selo.sh")
entrada("refazer_candidato_v397.sh", regras=[("runtime_quadro_v398.py", "runtime_pedras_v398.py", 1)])

# ------------------------------------------------------------------------------------------- diff_e_pinos
entrada("diff_e_pinos_v397.py", regras=[
    ("assert novos == [DL.STONE_REL] and not removidos and sorted(mudados) == [\"TGL/Audit.lean\", \"TGLExt.lean\"], (\"o diff do kernel nao e' so' a pedra + raiz + Audit\", novos, removidos, mudados)",
     "assert novos == sorted(DL.STONE_RELS) and not removidos and sorted(mudados) == [\"TGL/Audit.lean\", \"TGLExt.lean\"], (\"o diff do kernel nao e' so' as duas pedras + raiz + Audit\", novos, removidos, mudados)", 1),
    ("os vereditos esperados do passo simples (REPINADA_B7__...)", "os vereditos esperados do passo simples (REPINADA_B8__...)", 1),
])

# ------------------------------------------------------------------------------------------- instalar / reverter / regras
entrada("instalar_v397.py", regras=[
    ("(a v398 traz UM modulo novo de kernel, o numero lido de kernel_modulos_novos_v398.json: o proprio rito o materializa a partir do corpo embutido)", "(a v398 traz DOIS modulos novos de kernel, o numero lido de kernel_modulos_novos_v398.json: o proprio rito os materializa a partir do corpo embutido)", 1),
    ("# v398: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit e TestemunhaEstatica) JA estao no kernel do Nos (a base instalada e' a v397 selada); (b) o modulo novo da v398 (Token) NAO esta la ainda.",
     "# v398: (a) as pedras anteriores (o criterio binario, a rede de Fock, o tempo, Psibit, TestemunhaEstatica e Token) JA estao no kernel do Nos (a base instalada e' a v397 selada); (b) os modulos novos da v398 (Sonico e AfinacaoDasCordas) NAO estao la ainda.", 1),
    ('_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica")', '_PEDRAS_ANTERIORES = ("TheBinaryReadingAtTheFixedPoint", "TimeGravitonMatrix", "RuleQuadraticResidual", "Psibit", "TestemunhaEstatica", "Token")', 1),
])
entrada("reverter_v397.py")
entrada("regras_v397.py")

# ------------------------------------------------------------------------------------------- teste do conferidor (caminho positivo)
entrada("teste_conferidor_positivo_v397.py")

# ------------------------------------------------------------------------------------------- simular_arvore_do_nos: o sonico e a afinacao rodam na arvore simulada do Nos (os registros por spec v398 selam nela)
entrada("simular_arvore_do_nos_v397.py", regras=[
    ("roda o indice, o psibit_v395, a testemunha_estatica_v396, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec",
     "roda o indice, o psibit_v395, a testemunha_estatica_v396, o sonico_v398 e a afinacao_das_cordas_v398, o teste_de_veracidade_fase9_v397 (spec do V2 da Fase 9, lido por hash) e os registros por spec", 1),
    ("um.psibit_v395(core); um.testemunha_estatica_v396(core)   # (na fractalizacao do Um, no main; aqui o kf ja' e' o da arvore simulada do Nos)",
     "um.psibit_v395(core); um.testemunha_estatica_v396(core); um.sonico_v398(core); um.afinacao_das_cordas_v398(core)   # (na fractalizacao do Um, no main; aqui o kf ja' e' o da arvore simulada do Nos)", 1),
    ("um._v397_rodar_specs(core)   # (v398: o spec de veracidade roda no ponto do V1 no main; aqui, antes dos specs que o leem)",
     "um._v397_rodar_specs(core); um._v398_rodar_specs(core)   # (v397: o spec de veracidade roda no ponto do V1 no main; aqui, antes dos specs que o leem)", 1),
    ('for k in ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396",', 'for k in ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396",', 1),
])

# ------------------------------------------------------------------------------------------- exame_pontos: os pontos de chamada REAIS do sonico_v398 e da afinacao_das_cordas_v398
_SON_BLOCO = r'''# (4a'') os PONTOS DE CHAMADA REAIS do sonico_v398 e da afinacao_das_cordas_v398 (v398): as duas instrucoes do main (cada uma um `try`) que vem IMEDIATAMENTE depois da testemunha_estatica_v396 (que vem imediatamente depois do psibit_v395), na fractalizacao do Um
isn = [i for i, s_ in enumerate(unp) if "sonico_v398(core)" in s_]
assert len(isn) == 1 and isn[0] == ipt + 1, ("a instrucao do main que chama sonico_v398 nao e' unica ou nao vem IMEDIATAMENTE depois da testemunha_estatica_v396", isn, ipt)
isn = isn[0]
iaf = [i for i, s_ in enumerate(unp) if "afinacao_das_cordas_v398(core)" in s_]
assert len(iaf) == 1 and iaf[0] == isn + 1, ("a instrucao do main que chama afinacao_das_cordas_v398 nao e' unica ou nao vem IMEDIATAMENTE depois do sonico_v398", iaf, isn)
iaf = iaf[0]
R["ponto_sonico"] = {"indice_no_main": isn, "linha": main.body[isn].lineno, "antes_do_bloco_v393": isn < i0, "logo_depois_da_testemunha_v396": "testemunha_estatica_v396(core)" in unp[isn - 1], "instrucao_anterior": unp[isn - 1][:160].replace("\n", " | ")}
R["ponto_afinacao"] = {"indice_no_main": iaf, "linha": main.body[iaf].lineno, "antes_do_bloco_v393": iaf < i0, "logo_depois_do_sonico_v398": "sonico_v398(core)" in unp[iaf - 1], "instrucao_anterior": unp[iaf - 1][:160].replace("\n", " | ")}
builtins.open = _open_tr; _so = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(ast.fix_missing_locations(ast.Module(body=[main.body[isn], main.body[iaf]], type_ignores=[])), "<main:sonico_v398+afinacao_das_cordas_v398>", "exec"), g); errs = None
except Exception as e:
    import traceback; errs = repr(e) + traceback.format_exc()[-900:]
finally:
    stdout_son = sys.stdout.getvalue(); builtins.open = _open0; sys.stdout = _so
sn = core.get("sonico_v398") or {}; af = core.get("afinacao_das_cordas_v398") or {}
R["ponto_sonico"].update({"erro": errs, "stdout": stdout_son.splitlines(), "avisos": [l for l in stdout_son.splitlines() if "AVISO" in l], "verdict": sn.get("verdict"), "all_verified": sn.get("all_verified"),
                          "mecanica": {"passed": (sn.get("mechanics") or {}).get("passed"), "n_checks": (sn.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (sn.get("unconditional") or {}).get("in_kernel"), "beta_ok": sn.get("beta_ok"),
                          "entropia_theta_M_nats": (sn.get("values") or {}).get("collapse_entropy_theta_M_nats")})
R["ponto_afinacao"].update({"erro": errs, "avisos": [l for l in stdout_son.splitlines() if "AVISO" in l], "verdict": af.get("verdict"), "all_verified": af.get("all_verified"),
                            "mecanica": {"passed": (af.get("mechanics") or {}).get("passed"), "n_checks": (af.get("mechanics") or {}).get("n_checks")}, "unconditional_in_kernel": (af.get("unconditional") or {}).get("in_kernel"),
                            "hipotese": af.get("hypothesis"), "geometria": af.get("geometry"), "deriva_cordas_do_axioma": af.get("derives_strings_from_the_axiom")})
out["core.sonico_v398"] = {"all_verified": sn.get("all_verified"), "verdict": str(sn.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((sn.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
out["core.afinacao_das_cordas_v398"] = {"all_verified": af.get("all_verified"), "verdict": str(af.get("verdict"))[:300], "falhas": [ck_["id"] for ck_ in ((af.get("mechanics") or {}).get("checks") or []) if not ck_["ok"]]}
'''
_SON_FALSO = r'''ps_ = R["ponto_sonico"]
if ps_.get("erro") or ps_.get("avisos") or ps_.get("all_verified") is not True or not ps_.get("antes_do_bloco_v393") or not ps_.get("logo_depois_da_testemunha_v396") or ps_.get("beta_ok") is not True: falsos.append("ponto_sonico")
pa_ = R["ponto_afinacao"]
if (pa_.get("erro") or pa_.get("avisos") or pa_.get("all_verified") is not True or not pa_.get("antes_do_bloco_v393") or not pa_.get("logo_depois_do_sonico_v398") or (pa_.get("hipotese") or {}).get("status") != "KNOWN" or pa_.get("geometria") != "OPEN"
        or pa_.get("deriva_cordas_do_axioma") is not False): falsos.append("ponto_afinacao")
'''
entrada("exame_pontos_v397.py", regras=[
    ("(4) sobre o core anterior + kf novo, NA ORDEM DO MAIN:", "(4) [v398: + os pontos do sonico_v398 e da afinacao_das_cordas_v398, logo depois da testemunha] sobre o core anterior + kf novo, NA ORDEM DO MAIN:", 1),
    ('+ ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0', '+ ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) + ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS):\n    core.pop(n_, None)   # o fluxo os recria; comparam-se depois com os do core0', 1),
    ("# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v398): a instrucao do main (um `try` + o `print` [v398])", _SON_BLOCO + "# (4a') o PONTO DE CHAMADA REAL do teste_de_veracidade_fase9_v397 (v397): a instrucao do main (um `try` + o `print` [v397])", 1),
    ('assert "[v398]" in unp[iv + 1] and "teste_de_veracidade_fase9_v397" in unp[iv + 1]', 'assert "[v397]" in unp[iv + 1] and "teste_de_veracidade_fase9_v397" in unp[iv + 1]', 1),
    ('os.path.join(H, "insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json")', "os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)", 1),
    ('"v397": [k for k in ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],',
     '"v396": [k for k in ["testemunha_estatica_v396"] + list(um._V396_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v397": [k for k in ["teste_de_veracidade_fase9_v397"] + list(um._V397_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],\n'
     '                   "v398": [k for k in ["sonico_v398", "afinacao_das_cordas_v398"] + list(um._V398_NOMES_REGISTROS) if (core.get(k) or {}).get("all_verified") is not True],', 1),
    ('"registros_v397": {n_: ((seal.get("registros_v397") or {}).get(n_) or {}).get("all_verified") for n_ in um._V397_NOMES_REGISTROS}}',
     '"registros_v397": {n_: ((seal.get("registros_v397") or {}).get(n_) or {}).get("all_verified") for n_ in um._V397_NOMES_REGISTROS},\n'
     '                 "sonico_v398": {x: (seal.get("sonico_v398") or {}).get(x) for x in ("verdict", "all_verified")}, "afinacao_das_cordas_v398": {x: (seal.get("afinacao_das_cordas_v398") or {}).get(x) for x in ("verdict", "all_verified")},\n'
     '                 "registros_v398": {n_: ((seal.get("registros_v398") or {}).get(n_) or {}).get("all_verified") for n_ in um._V398_NOMES_REGISTROS}}', 1),
    ('pv = R["ponto_veracidade"]\nif (pv.get("erro")', _SON_FALSO + 'pv = R["ponto_veracidade"]\nif (pv.get("erro")', 1),
])

# ------------------------------------------------------------------------------------------- AUTORAIS: subida mecanica agora; edicao a mao depois (o derivador nao os sobrescreve)
# (p00_precondicoes e derivar_instalar_rito tem regras no lote D; conferir_citacoes, copiar_insumos, gerar_esperados, conferir_rito, gerar_estado e gerar_registro_mapa_prep sao ESCRITOS a mao, nunca regerados)
