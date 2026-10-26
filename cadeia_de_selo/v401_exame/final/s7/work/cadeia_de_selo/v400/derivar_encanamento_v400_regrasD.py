# -*- coding: utf-8 -*-
# regras (lote D) de derivar_encanamento_v400.py: ESPERADOS, conferidor, teste do conferidor, p00, instalar/reverter/rito. Escrito pela ferramenta Write.
# O mapa subiu 398 -> 399 e 399 -> 400. A v400 NAO traz pedra, bandeira nem chave nova no core: os ESPERADOS dizem o que a v399 selada JA tinha e o que a correcao muda (so' o registro do selo ACOM).

_DOC_ESP = '''"""gerar_esperados_v400.py -- ESPERADOS_v400.json LIDOS dos artefatos (molde: gerar_esperados_v399.py): o estado SELADO da v399 pinado. A v400 e' uma CORRECAO: NENHUMA chave nova no core nem no selo, NENHUM modulo de kernel; a escada e' a da v399.
A TROCA DITA e' UMA so': o veredito do estatuto da prova (v391) carrega o hash do PROPRIO um.py (a certificacao pelo proprio hash) e muda com o programa; as contagens CORE_n_ que o ensaio computa sobre o core inteiro (um artefato dele, nao do rito) sao normalizadas.
Todos os outros vereditos da v399 ficam IGUAIS. O que a correcao muda de proposito: so' o registro do selo ACOM (os hashes do novo um.py e a checagem do beta contra o core), o sidecar, a versao e a errata ao lado no artigo e no .md. O pilar pela mesma chave.
O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\\\insumos\\\\fase9) e o conferidor os confere de novo. Nada digitado: cada numero e hash vem de CANDIDATO_v400.json, ensaio_a_seco_v400.json, do core/selo
da v399 (base_v399), de kernel\\\\FLAGS_v399.json, de ESPERADOS_v399.json (o que o quadro pinou) e do resultado pinado. A DIRECAO DO TESTEMUNHO fica nos ESPERADOS como dado: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto."""
'''

entrada("gerar_esperados_v399.py", autoral=True, regras=[
    entre('"""gerar_esperados_v400.py -- ESPERADOS_v400.json LIDOS', "import hashlib, json, os, re, sys", _DOC_ESP, "docstring do gerar_esperados v400"),
    ('mud = ens["vizinhos"]["mudaram"]\ntroca = sorted(mud)   # os vereditos da v399 que mudam (so\' numeros), recomputados pelo ensaio\nassert troca, "a troca dita nao pode ser vazia (a escada mudou)"\n',
     'mud = ens["vizinhos"]["mudaram"]\nassert not mud, ("nenhum vizinho da v399 muda alem da troca esperada (so\' o hash proprio no estatuto da prova)", sorted(mud))\nte_ = ens["vizinhos"]["troca_esperada_so_o_hash_proprio"]\ntroca = sorted(te_)   # a UNICA troca dita: o estatuto da prova carrega o hash do proprio um.py\nassert troca == ["estatuto_da_prova_v391"], troca\n', 1),
    ('"veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca}', '"veredito_da_troca_no_ensaio": {k: te_[k]["depois"] for k in troca}', 1),
    ('F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v400.json"), encoding="utf-8"))\n', 'F = {}   # a v400 nao acrescenta modulo: nao ha FORMAL_MAP novo\n', 1),
    ('FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v400.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]',
     'FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v399.json"), encoding="utf-8")); assert CM["n_bandeiras"] == 0 and FJ["n_flags"] == CM["politica_de_bandeiras"]["n_flags"]   # FLAGS_v399: as bandeiras da v399 (novas so\' para a Bancada, que pina a v398)', 1),
    ('"beta_runs_bounded_below_v388")', '"beta_runs_bounded_below_v388", "declaracao_do_operador_v399", "registros_v399")', 1),
    ('TST = DL.STONES[0]', 'TST = DL.STONES_DESDE_B8[0]   # a pedra Testemunho: nova para a Bancada (v398), nao para a v400', 1),
    ('"bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],', '"bandeiras_novas_chaves": [], "bandeiras_novas_nomes": [], "bandeiras_desde_a_bancada": {"chaves": [f[0] for f in FJ["flags"]], "nomes": [f[1] for f in FJ["flags"]]},', 1),
    ('"sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v400)"', '"sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": "um_absoluto_selo_acom/v1 (v399)"', 1),
    ('"artigo_marcas": {"pt": [TN400, "A direção do testemunho.", "A declaração do operador.", "O selo pela própria tecnologia.", "A pedra Testemunho."] + MARCAS399_PT, "en": [TN400E, "The direction of the testimony.", "The operator\'s declaration.", "Sealing by its own technology.", "The Testemunho stone."] + MARCAS399_EN},',
     '"artigo_marcas": {"pt": ["Errata ao lado (v400)."] + MARCAS399_PT, "en": ["Erratum beside it (v400)."] + MARCAS399_EN},', 1),
    (' + ["Nesta rodada os registros da v400 NÃO selaram todos"]', '', 1),
    (' + ["This round the v400 records did NOT all seal"]', '', 1),
    ('"toc": {"pt": [TN400] + list(E399["toc"]["pt"]), "en": [TN400E] + list(E399["toc"]["en"])},',
     '"toc": {"pt": [w for w in E399["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [w for w in E399["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]},   # nenhuma secao nova (a errata e\' um paragrafo da secao da v399); o titulo da introducao diz `v384 a <versao desta rodada>`', 1),
    ('"md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v400, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v399, 23/10/2026)",',
     '"md_errata": "Errata ao lado (v400, 24/10/2026)", "md_testemunho": "O testemunho de dois: o selo pela própria tecnologia (v399, 24/10/2026)", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)",', 1),
    ('"n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES},',
     '"n_bandeiras_por_grupo": {}, "bandeiras_por_grupo_desde_a_bancada": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "pedras_desde_a_bancada": CM["kernel"]["pedras_desde_a_bancada"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES_DESDE_B8},', 1),
    ('"suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES},', '"suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES_DESDE_B8},', 1),
    ('"contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES},', '"contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES_DESDE_B8},', 1),
    ('assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 1, "o numero de modulos novos != a lista"', 'assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 0, "a v400 nao acrescenta modulo: o numero de modulos novos != a lista (vazia)"', 1),
    ('assert set(esp["selo_difere_do_v399_no_ensaio"]) >= {"selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "registros_v399", "um_version"}',
     'assert {"selo_pela_propria_tecnologia_v399", "um_version"} <= set(esp["selo_difere_do_v399_no_ensaio"]) <= {"selo_pela_propria_tecnologia_v399", "um_version", "sha256", "estatuto_da_prova_v391", "three_stress_tests_v387"} and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (esp["selo_difere_do_v399_no_ensaio"], ens["selo"].get("difere_e_nao_e_so_o_esperado"))   # estatuto_da_prova_v391 (so\' o hash proprio do um.py) e three_stress_tests_v387 (so\' as contagens do core no instante) sao EXPLICADOS chave por chave pelo ensaio; o resto do selo e\' o da v399', 1),
])
