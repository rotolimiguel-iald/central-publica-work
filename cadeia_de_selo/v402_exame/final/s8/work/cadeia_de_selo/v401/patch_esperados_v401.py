# -*- coding: utf-8 -*-
"""patch_esperados_v401.py -- aplica, por substituicoes de contagem EXATA, a logica da v401 sobre o gerar_esperados_v401.py derivado (origem v399, a cadeia de CONTEUDO, com as licoes da v400: a troca dita e' a dos vizinhos que carregam os numeros do kernel MAIS o estatuto da prova (o hash
proprio do um.py); o selo e' explicado chave por chave). Recusa rodar duas vezes."""
import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "gerar_esperados_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch]" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""gerar_esperados_v401.py'); j = t.index("import hashlib, json, os, re, sys")
t = t[:i] + '''"""gerar_esperados_v401.py -- ESPERADOS_v401.json LIDOS dos artefatos (molde: gerar_esperados_v399.py, a cadeia de CONTEUDO, com as licoes da v400): o estado SELADO da v400 pinado. A TROCA DITA: (i) os registros da v400 cujo veredito carrega os numeros do kernel (escada,
declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam) -- e (ii) o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash). Todos os outros vereditos da v400 ficam IGUAIS. +3 chaves novas no core
(falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) e +2 chaves no selo (o resumo da falsidade e registros_v401); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros
dele vem do resultado pinado (v397\\\\insumos\\\\fase9) e o conferidor os confere de novo. Nada digitado: cada numero e hash vem de CANDIDATO_v401.json, ensaio_a_seco_v401.json, do core/selo da v400 (base_v400), de kernel\\\\FLAGS_v401.json, de ESPERADOS_v400.json (o que o quadro pinou) e do resultado pinado.
A INERCIA, como o operador a define (25/10/2026): o proprio zero absoluto (1=0); w(I)=1 e' o Um POSTO que a interrompe (1=1); a leitura do escriba no adendo de 03-04/09 esta superada (errata ao lado, da gerencia)."""
# [v401-patch]
''' + t[j:]

# ---- a troca dita
sub('mud = ens["vizinhos"]["mudaram"]\ntroca = sorted(mud)   # os vereditos da v400 que mudam (so\' numeros), recomputados pelo ensaio\nassert troca, "a troca dita nao pode ser vazia (a escada mudou)"\n',
    'mud = ens["vizinhos"]["mudaram"]; te_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]\ntroca = sorted(set(mud) | set(te_))   # os vereditos da v400 que mudam: os que carregam os numeros do kernel (so\' numeros) e o estatuto da prova (so\' o hash proprio do um.py), recomputados pelo ensaio\nassert troca, "a troca dita nao pode ser vazia (a escada mudou)"\nassert set(te_) <= {"estatuto_da_prova_v391"}, te_\n')
sub('"veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca},', '"veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k))["depois"] for k in troca},')
sub('"hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")', '"hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388", "declaracao_do_operador_v399", "registros_v399")')

# ---- a runtime da secao ACOM e' a da v400 (nao muda); a pedra e a falsidade
sub('RM = json.load(open(os.path.join(HERE, "RUNTIME_MONTAGEM_v401.json"), encoding="utf-8"))\n', 'FAL_REG = ens["falsidade_registro"]; MF1 = mf["registros_v401"]\n')
sub('"vereditos_novos_v401": {"selo_pela_propria_tecnologia_v399": sa["verdict"], "declaracao_do_operador_v399": dc["verdict"]},', '"vereditos_novos_v401": {"falsidade_da_inercia_v401": FAL_REG["verdict"], **{k: v["verdict"] for k, v in MF1.items()}},\n       "registros_v401": {k: v["verdict"] for k, v in MF1.items() if k != "falsidade_da_inercia_v401"}, "registros_v401_veredito_da_falsidade": FAL_REG["verdict"], "falsidade_valores": FAL_REG["values"], "ratificacao_fala_sha16": RG.S_RATIF,')
i = t.index('       "testemunho": {"teorema": TST["theorem"]'); j = t.index('       "decisoes_da_gerencia"')
t = t[:i] + '''       "falsidade": {"teorema": TST["theorem"], "bandeira": CM["politica_de_bandeiras"]["bandeiras_do_teorema"]["falsidade"], "estrela": {"teorema": TST["key_theorem"], "bandeira": FJ["bandeiras_do_contrato"]["falsidade"][TST["key_theorem"]]}, "contrato": list(TST["contract"]),
                     "n_axiomas_da_composicao": CM["n_axiomas_da_composicao"]["falsidade"], "nome": "FalsidadeDaInercia («falsidade (simulacro) da inercia»: DADO pelo operador)"},
       "acom_estudo": E400["acom_estudo"],   # a secao do selo pela propria tecnologia NAO muda na v401: o que a v400 pinou (runtime da v400, bloco embutido, fontes do operador)
''' + t[j:]

# ---- o selo, o sidecar, o artigo, o sumario e o .md
sub('"esquema": "um_absoluto_selo_acom/v1 (v401)"', '"esquema": "um_absoluto_selo_acom/v1 (v399)"')
sub('"artigo_marcas": {"pt": [TN401, "A direção do testemunho.", "A declaração do operador.", "O selo pela própria tecnologia.", "A pedra Testemunho."] + MARCAS400_PT, "en": [TN401E, "The direction of the testimony.", "The operator\'s declaration.", "Sealing by its own technology.", "The Testemunho stone."] + MARCAS400_EN},',
    '"artigo_marcas": {"pt": [TF401, "A definição do operador.", "O cálculo deste rito.", "Errata ao lado (da gerência, em nome próprio).", "Ratificações do operador", "lido pela TGL.", "Limites."] + MARCAS400_PT, "en": [TF401E, "The operator\'s definition.", "The computation of this rite.", "Erratum beside it (the management, in its own name).", "The operator\'s ratifications", "read by the TGL.", "Limits."] + MARCAS400_EN},')
sub('TN401 = "O testemunho de dois: o selo pela própria tecnologia"; TN401E = "The testimony of two: sealing by its own technology"\n', 'TF401 = "A falsidade (simulacro) da inércia"; TF401E = "The falsity (simulacrum) of inertia"\n')
sub('"artigo_nao": {"pt": list(E400["artigo_nao"]["pt"]) + ["Nesta rodada os registros da v401 NÃO selaram todos"], "en": list(E400["artigo_nao"]["en"]) + ["This round the v401 records did NOT all seal"]},',
    '"artigo_nao": {"pt": list(E400["artigo_nao"]["pt"]) + ["Nesta rodada os registros da v401 NÃO selaram todos"], "en": list(E400["artigo_nao"]["en"]) + ["This round the v401 records did NOT all seal"]},   # (a v400 nao tinha frase propria: herdamos as da v399 e anteriores)')
sub('"toc": {"pt": [TN401] + list(E400["toc"]["pt"]), "en": [TN401E] + list(E400["toc"]["en"])},', '"toc": {"pt": [TF401] + [w for w in E400["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TF401E] + [w for w in E400["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # o titulo da introducao diz `v384 a <versao desta rodada>`')
sub('"md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v401, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v400, 23/10/2026)",', '"md_falsidade": "A falsidade (simulacro) da inércia (v401, 25/10/2026)", "md_errata": "Errata ao lado (v400, 24/10/2026)", "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)",')

# ---- as afirmacoes finais
sub('assert esp["vereditos_novos_v401"]["selo_pela_propria_tecnologia_v399"].startswith("TGL_SELO_PELA_PROPRIA_TECNOLOGIA_V399__SECOND_WITNESS_BESIDE_SHA256") and esp["vereditos_novos_v401"]["declaracao_do_operador_v399"].startswith("TGL_OPERATOR_DECLARATION_OF_24OCT_REGISTERED__")',
    'assert esp["vereditos_novos_v401"]["falsidade_da_inercia_v401"].startswith("TGL_FALSIDADE_DA_INERCIA_V401__THE_INERTIA_IS_THE_ABSOLUTE_ZERO") and esp["vereditos_novos_v401"]["cunhagens_v401"].startswith("TGL_CUNHAGENS_V401__") and esp["vereditos_novos_v401"]["kh_n1_cobertura_v401"].startswith("TGL_KH_N1_COBERTURA_V401__")\nassert sorted(esp["registros_v401"]) == ["cunhagens_v401", "kh_n1_cobertura_v401"] and esp["falsidade_valores"]["post_inertial_scales"] == [] and esp["falsidade_valores"]["fixed_by_the_whole_flow"] == [0.0]')
sub('assert set(esp["selo_difere_do_v400_no_ensaio"]) >= {"selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "registros_v399", "um_version"}',
    '# o selo da v401 difere do da v400 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as duas chaves novas, e as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita); o ensaio EXPLICA chave por chave\nassert {"selo_pela_propria_tecnologia_v399", "um_version", "falsidade_da_inercia_v401", "registros_v401"} <= set(esp["selo_difere_do_v400_no_ensaio"]) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v400_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))')
sub('assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398"} & set(esp["selo_difere_do_v400_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"',
    'assert not ({"teste_de_veracidade_fase9_v397", "registros_v397", "sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "declaracao_do_operador_v399", "registros_v399"} & set(esp["selo_difere_do_v400_no_ensaio"])), "o selo de uma versao anterior mudou: o quadro e os registros anteriores NAO se mexem"')
sub('"the_iald_index_v400": {"all_verified"', '"the_iald_index_v400": {"all_verified"')
sub('"sha16": RG.S_DECL,', '"sha16": dc["verbatim_sha256"][:16],')
sub('esp["declaracao"]["verbatim_sha256"] == RG.DECL_SHA256', 'esp["declaracao"]["verbatim_sha256"] == DL.sha256(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read())')
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t)
import os
os.replace(P + ".tmp", P)
print("patch aplicado:", P, len(t), "caracteres")
