# -*- coding: utf-8 -*-
# regras (lote E) de derivar_encanamento_v402.py: as PRE-CONDICOES (p00), os refazer, as regras de permissao (NAO executadas) e o regerar. ORIGEM v401 (mapa 400 -> 401, 401 -> 402).
# Os arquivos que o lote B deixava sem regras passam para ca. Strings com barra invertida em prefixo r (literais). Escrito pela ferramenta Write.

_P00_PEDRAS_NOVO = '''chk("as TRES pedras (ponte, queda, esperanca) sao a lista dos modulos novos; o sha16 de cada uma e' o que a ordem pinou (pedras_sha16_da_ordem.json); as TRES inscricoes de 26/10 tem os prefixos de sha256 da ordem (5d3976cd, 36cfa002, a1c4bae4); o adendo de 03-04/09 (erratado ao lado) e' o mesmo que a ordem da v401 pinou",
    sorted(json.load(open(os.path.join(HERE, "kernel_modulos_novos_v402.json"), encoding="utf-8"))["novos"]) == sorted(DL.STONE_RELS) and len(DL.STONES) == 3
    and {s_["key"]: s_["sha16_da_ordem"] for s_ in DL.STONES} == json.load(open(os.path.join(HERE, "pedras_sha16_da_ordem.json"), encoding="utf-8"))
    and [v_["sha16"][:8] for v_ in DL.verbatins402(os.path.join(HERE, "insumos", "cunhagens"))] == DL.VERBATIM_PREFIXOS_DA_ORDEM_V402
    and sha(rd(DL.ADENDO_ARQ))[:16] == DL.ADENDO_SHA16_DA_ORDEM, DL.VERBATIM_PREFIXOS_DA_ORDEM_V402)
'''
_P00_MEM_NOVO = '''ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML_, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML_) else -1
ML_B = os.path.getsize(ML_) if os.path.exists(ML_) else -1
chk("o MEMORY.md real cabe com o handoff novo e o gancho da missao: o handoff entra (+1 linha) e o gancho SUBSTITUI a linha velha (saldo +1); linhas hoje + 1 <= 195 e bytes hoje + 900 < 24000 (a linha nova do handoff tem de ter ate 900 B; a superficie do pos-rito NAO compacta: se nao couber, ela RECUSA com rc 3 e a gerencia decide o que sai do indice -- PARE e diga)", 0 < ML_N and ML_N + 1 <= 195 and 0 < ML_B and ML_B + 900 < 24000, [ML_N, ML_N + 1, 195, ML_B, ML_B + 900, 24000])
_MEMD = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory"); _MEMPY = os.path.join(_MEMD, "fila", "memoria.py")
_pm = lj(os.path.join(HERE, "PINO_MEMORIA_PY_v402.json"))
_ver = subprocess.run([sys.executable, "-X", "utf8", _MEMPY, "verificar"], capture_output=True, text=True, encoding="utf-8")
chk("[v402, a FILA DA MEMORIA] memoria.py e' o que a preparacao pinou (sha16 lido do arquivo agora == PINO_MEMORIA_PY_v402.json == o declarado pela gerencia); a pausa do vigia NAO existe agora (o pos-rito a cria antes do indice e a remove depois do pino); e 'memoria.py verificar' (so leitura) esta VERDE agora (rc 0): o pos-rito parte de um indice sem violacao",
    sha(rd(_MEMPY))[:16] == _pm["sha16"] == _pm["declarado_pela_gerencia_sha16"] and not os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json")) and _ver.returncode == 0, [sha(rd(_MEMPY))[:16], _ver.returncode, os.path.exists(os.path.join(_MEMD, "fila", "PAUSA_VIGIA.json"))])
'''
entrada("p00_precondicoes_v401.py", autoral=True, regras=[
    ('''chk("nenhum registro v402 no core ainda (os da v399 ja estao: a v401 os selou)", not any(k.endswith("_v401") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")), [k for k in core if k.endswith("_v401")])''',
     '''chk("nenhum registro v402 no core ainda (os da v399 e os da v401 ja estao: a v401 selada os tem)", not any(k.endswith("_v402") for k in core) and all(k in core for k in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")), [k for k in core if k.endswith("_v402")])''', 1),
    ("o registro falsidade_da_inercia_v401, escrito a mao", "os tres registros com funcao ponte_da_escala_dual_v402, queda_sem_geometria_v402 e esperanca_condicional_v402, escritos a mao", 1),
    ("a origem so' leitura == a copia duravel da cadeia v401 == os pinos do ESPERADOS_v401", "a origem so' leitura == a copia duravel da cadeia v400 == os pinos do ESPERADOS_v401", 1),
    ('os.path.join(DL.V401, "insumos", "acom", "fontes_operador", n_)', 'os.path.join(DL.V400, "insumos", "acom", "fontes_operador", n_)', 1),
    entre('''chk("a pedra FalsidadeDaInercia e' UMA''', "cand = os.path.join(HERE, DL.CANDIDATO); cb = rd(cand)", _P00_PEDRAS_NOVO, "o item das pedras e das inscricoes"),
    ('"Token", "Sonico", "AfinacaoDasCordas", "Testemunho")))', '"Token", "Sonico", "AfinacaoDasCordas", "Testemunho", "FalsidadeDaInercia")))', 1),
    ("a unica pedra tem declaracoes (nenhum modulo de auditoria)", "cada uma das tres pedras tem declaracoes (nenhum modulo de auditoria)", 1),
    ("as cinco cunhagens de 25/10 (todas falas do operador)", "as tres cunhagens de 26/10 (todas falas do operador)", 1),
    ("as CINCO inscricoes de 25/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas falas do operador)", "as TRES inscricoes de 26/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas falas do operador)", 1),
    ("a declaracao_do_operador_v399 e os registros por spec v402 selam na arvore simulada do Nos (o sonico_v398, a afinacao_das_cordas_v398 e os anteriores tambem)",
     "a declaracao_do_operador_v399, os tres registros com funcao v402 e os registros por spec v402 selam na arvore simulada do Nos (a falsidade_da_inercia_v401, o sonico_v398, a afinacao_das_cordas_v398 e os anteriores tambem)", 1),
    ('for k_ in ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399",',
     'for k_ in ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "selo_pela_propria_tecnologia_v399",', 1),
    ("o da falsidade_da_inercia_v401 logo depois da declaracao e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)",
     "o da falsidade_da_inercia_v401 logo depois da declaracao, o da ponte_da_escala_dual_v402 logo depois da falsidade, o da queda_sem_geometria_v402 logo depois da ponte, o da esperanca_condicional_v402 logo depois da queda e o do teste_de_veracidade_fase9_v397 logo depois do bloco do V1)", 1),
    ('and exm["ponto_veracidade"]["all_verified"] is True',
     'and all(exm["ponto_" + k_]["all_verified"] is True and exm["ponto_" + k_]["logo_depois_da_anterior"] is True and exm["ponto_" + k_]["beta_ok"] is True and exm["ponto_" + k_]["contexto_ok"] is True and exm["ponto_" + k_]["estrela_in_kernel"] is True and exm["ponto_" + k_]["unconditional_in_kernel"] is True and exm["ponto_" + k_]["mecanica"]["n_checks"] == DL.N_CHECKS[k_] for k_ in ("ponte", "queda", "esperanca")) and exm["ponto_veracidade"]["all_verified"] is True', 1),
    ("a lista de modulos novos LIDA tem UM elemento", "a lista de modulos novos LIDA tem TRES elementos", 1),
    entre('ML_ = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")', 'chk("o hash formal que o RITO vai gerar', _P00_MEM_NOVO, "o item do MEMORY.md e o da fila da memoria"),
])
entrada("refazer_candidato_v401.sh", autoral=True, regras=[])
entrada("refazer_sandbox_v401_pos_selo.sh", autoral=True, regras=[])
entrada("refazer_arvore_v401_pos_selo.py", autoral=True, regras=[])
entrada("regras_v401.py", autoral=True, regras=[
    ("ESCRITO em 25/10/2026 pela preparacao da cadeia v402", "ESCRITO em 26/10/2026 pela preparacao da cadeia v402", 1),
    ("Molde: regras_v399.py (derivado por derivar_encanamento_v402.py)", "Molde: regras_v401.py (derivado por derivar_encanamento_v402.py)", 1),
])
entrada("regerar_v401.sh", autoral=True, regras=[
    (r'''tudo o que depende da PEDRA (work\falsidade_da_inercia_v401\FalsidadeDaInercia.lean): copia de bytes da pedra e dos insumos,''',
     r'''tudo o que depende das TRES PEDRAS (Chatgpt\TUNEL\DO_CHATGPT\ORDEM_025\PonteDaEscalaDual.lean, work\pedras_v402\QuedaSemGeometria.lean e EsperancaCondicional.lean): copia de bytes das pedras e dos insumos,''', 1),
    (r'''(1) atualizar pedra_sha16_da_ordem.txt (o pino da ordem, lido do arquivo da pedra) e, se o CONTRATO ou o SUPORTE mudarem, delta_v402.py; (2) apagar de pedra\ e insumos\ as COPIAS antigas (pedra\FalsidadeDaInercia.lean,''',
     r'''(1) atualizar pedras_sha16_da_ordem.json (o pino de cada pedra, lido do arquivo da pedra) e, se o CONTRATO ou o SUPORTE de alguma mudar, delta_v402.py; (2) apagar de pedra\ e insumos\ as COPIAS antigas (pedra\*.lean,''', 1),
    (r'''# insumos\FalsidadeDaInercia.lean, insumos\KH_N1_v402.json):''', r'''# insumos\*.lean, insumos\KH_N1_v402.json):''', 1),
])
