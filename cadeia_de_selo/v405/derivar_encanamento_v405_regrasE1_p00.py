# -*- coding: utf-8 -*-
# regras (lote E1_p00) de derivar_encanamento_v405.py: as precondicoes. ORIGEM v404 FINAL. Mapa: 403 -> 404 (a base selada), 404 -> 405 (esta rodada).
# Alem da subida mecanica, as correcoes de CONTEUDO da v405: (1) o registro v405 ainda NAO esta no core e os da v404 JA estao; (2) as OITO pedras da v405; (3) as pedras da v403 e da v404 estao no Nos; (4) simular_arvore e exame_pontos passam a cobrir os onze registros novos; os de funcao da v404 vem do delta_v404 (D4);
# (5) a guarda das frases e a lista congelada das falas entram como checagens; (6) o marcador de servidor parado nas duas cadeias. Escrito pela ferramenta Write.
_E1_REG_V404 = '"projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404"'
_E1_REG_V405 = '"ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405", "cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405"'


def _e1_exame(t_):
    ant = 'else DL.D3.N_CHECKS[k_] if k_ in ("caminho", "vida", "verdade_adendo") else DL.N_CHECKS[k_]) for k_ in ("ponte", "queda", "esperanca", "caminho", "vida", "verdade_adendo", "projecao", "jo8v32"))'
    nov = ('else DL.D3.N_CHECKS[k_] if k_ in ("caminho", "vida", "verdade_adendo") else DL.D4.N_CHECKS[k_]) for k_ in ("ponte", "queda", "esperanca", "caminho", "vida", "verdade_adendo", "projecao", "jo8v32"))'
           ' and all(exm["ponto_v405_" + k_]["all_verified"] is True and exm["ponto_v405_" + k_]["beta_ok"] is True and exm["ponto_v405_" + k_]["contexto_ok"] is True and exm["ponto_v405_" + k_]["estrela_in_kernel"] is True and exm["ponto_v405_" + k_]["unconditional_in_kernel"] is True and exm["ponto_v405_" + k_]["mecanica"]["n_checks"] == DL.N_CHECKS[k_] and exm["ponto_v405_" + k_]["antes_do_bloco_v393"] is True for k_ in DL.N_CHECKS)')
    assert t_.count(ant) == 1, t_.count(ant)
    t_ = t_.replace(ant, nov)
    ant2 = 'exm["ponto_f2b"]["mecanica"]["n_checks"] == DL.N_CHECKS["f2b"]'
    assert t_.count(ant2) == 1
    return t_.replace(ant2, 'exm["ponto_f2b"]["mecanica"]["n_checks"] == DL.D4.N_CHECKS["f2b"]')


_E1_NOVOS = r'''_gf = lj(os.path.join(HERE, "GUARDA_FRASES_v405.json"))
chk("[v405, a MOLDURA] a guarda das frases: o controle negativo passou (cada frase proibida reprovada, a frase certa e os identificadores aceitos, a fala do operador so' pela excecao) e o gerador achou zero frase proibida no texto novo do candidato; o registro antigo nomes_e_hipoteses_descarregadas_v405 nao existe mais", _gf.get("ok") is True and CM["guarda_frases"]["controle_negativo"] is True and CM["guarda_frases"]["violacoes_no_texto_novo"] == 0 and "nomes_e_hipoteses_descarregadas_v405" not in CM["registros"] and "campos_fechados_e_leituras_v405" in CM["registros"], CM["guarda_frases"])
_cong = lj(os.path.join(HERE, "VERBATIM_CONGELADO_v405.json"))
_glob_agora = sorted(os.path.basename(p_) for p_ in DL.verbatim_origem_pelo_glob())
_novas_depois = sorted(set(_glob_agora) - set(os.path.basename(p_) for p_ in _cong["arquivos"]))
chk("[v405] a lista das falas embutidas esta congelada (VERBATIM_CONGELADO_v405.json) e e' a do candidato; fala nova depois do congelamento NAO entra nesta versao e NAO reprova o conferidor (fica dita no detalhe)", list(DL.VERBATIM_ORIGEM_V405) == list(_cong["arquivos"]) and len(_cong["arquivos"]) == len(CM["cunhagens"]), {"embutidas": len(_cong["arquivos"]), "falas_novas_depois_do_congelamento": _novas_depois})
_rec_err = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_01nov.json"))
_rec_r2 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R2_01nov.json"))
_rec_r3 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R3_01nov.json"))
_rec_r4 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R4_01nov.json"))
_rec_r5 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R5_01nov.json"))
_rec_r6 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R6_01nov.json"))
_rec_r7 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R7_01nov.json"))
_cad = [(_rec_r7, _rec_r6), (_rec_r6, _rec_r5), (_rec_r5, _rec_r4), (_rec_r4, _rec_r3), (_rec_r3, _rec_r2)]
chk("[v405] as pedras sao as da ERRATA R7 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: em R7 -> R6 -> R5 -> R4 -> R3 -> R2, cada pedra ou segue igual (depois == depois) ou tem antes == depois do recibo anterior, e R2.antes == R1.depois (sete arquivos); os recibos antigos ficam como registro", all(sha(rd(os.path.join(HERE, "pedra", k_ + ".lean"))) == v_["sha256_depois"] for k_, v_ in _rec_r7["pedras"].items()) and len(_rec_r7["pedras"]) == 8 and all(all(v_["sha256_depois"] in (n_["pedras"][k_].get("sha256_antes"), n_["pedras"][k_]["sha256_depois"]) for k_, v_ in a_["pedras"].items()) for n_, a_ in _cad) and all(_rec_r2["pedras"][a_["modulo"]]["sha256_antes"] == a_["sha256_depois"] for a_ in _rec_err["arquivos"]) and len(_rec_err["arquivos"]) == 7, len(_rec_r7["pedras"]))
chk("[v405, a lista de exclusao] nenhuma fala de VERBATIM_EXCLUIDAS_V405 esta no candidato: o sha16 nao aparece nas cunhagens do CANDIDATO_v405.json nem na copia duravel insumos\\cunhagens", not any(k_ in json.dumps(CM["cunhagens"]) for k_ in DL.VERBATIM_EXCLUIDAS_V405) and not any(os.path.basename(p_)[:16] in DL.VERBATIM_EXCLUIDAS_V405 for p_ in glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*"))), sorted(DL.VERBATIM_EXCLUIDAS_V405))
chk("[v405, a errata R2] a guarda das frases varreu as oito pedras (zero frase proibida fora das falas) e a conferencia de citacoes conferiu as docstrings delas (zero reprovada; as apontadas a gerencia ficam ditas no JSON)", CM["guarda_frases"]["pedras_varridas"] == 8 and CM["guarda_frases"]["violacoes_nas_pedras"] == 0 and not lj(os.path.join(HERE, "conferir_citacoes_v405.json"))["varredura_das_pedras"]["reprovadas"], lj(os.path.join(HERE, "conferir_citacoes_v405.json"))["varredura_das_pedras"]["citacoes_conferidas"])
'''
entrada("p00_precondicoes_v404.py", autoral=True, regras=[
    ('not any(k.endswith("_v404") for k in core) and all(k in core for k in ("caminho_v403",', 'not any(k.endswith("_v405") for k in core) and all(k in core for k in (' + _E1_REG_V404 + ', "caminho_v403",', 1),
    ('[k for k in core if k.endswith("_v404")])', '[k for k in core if k.endswith("_v405")])', 1),
    ('chk("as DUAS pedras (projecao, jo8v32) sao a lista dos modulos novos;', 'chk("as OITO pedras sao a lista dos modulos novos;', 1),
    ('len(DL.STONES) == 2\n', 'len(DL.STONES) == 8\n', 1),
    ('as NOVE falas de 28/10 (todas do operador) tem os prefixos de sha256 da ordem; o adendo de 03-04/09 (erratado ao lado) e\' o mesmo que a ordem da v404 pinou', 'as falas-chave de 30/10 a 01/11 (todas do operador) tem os prefixos de sha256 da ordem; o adendo de 03-04/09 (erratado ao lado) e\' o mesmo que a ordem da v404 pinou', 1),
    ('and [v_["sha16"][:8] for v_ in DL.verbatins405(os.path.join(HERE, "insumos", "cunhagens"))] == DL.VERBATIM_PREFIXOS_DA_ORDEM_V405\n', 'and len(DL.verbatins405(os.path.join(HERE, "insumos", "cunhagens"))) == len(DL.VERBATIM_ORIGEM_V405)   # (verbatins405 aborta se uma fala-chave diverge do prefixo da ordem)\n', 1),
    ('and sha(rd(DL.ADENDO_ARQ))[:16] == DL.ADENDO_SHA16_DA_ORDEM, DL.VERBATIM_PREFIXOS_DA_ORDEM_V405)', 'and sha(rd(DL.ADENDO_ARQ))[:16] == DL.ADENDO_SHA16_DA_ORDEM, len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V405))', 1),
    ('all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in DL.D3.STONE_RELS))', 'all(os.path.exists(os.path.join(NK, *r_.split("/"))) for r_ in list(DL.D3.STONE_RELS) + list(DL.D4.STONE_RELS)))', 1),
    ('for k_ in ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404", "caminho_v403",', 'for k_ in (' + _E1_REG_V405 + ', ' + _E1_REG_V404 + ', "caminho_v403",', 1),
    ('os TRES registros com funcao v405 e os registros por spec v405 selam na arvore simulada', 'os OITO registros com funcao v405 e os registros por spec v405 selam na arvore simulada', 1),
    ('cada uma das duas pedras tem declaracoes (nenhum modulo de auditoria)', 'cada uma das oito pedras tem declaracoes (nenhum modulo de auditoria)', 1),
    ('chk("as DUAS falas de 27/10 (ambas do operador): arquivo duravel == sha256 == fonte original"', 'chk("as falas de 30/10 a 01/11 (todas do operador): arquivo duravel == sha256 == fonte original"', 1),
    ('as DUAS falas de 27/10 desta versao tem os prefixos de sha256 que a ordem da gerencia deu (ambas do operador)', 'as falas-chave desta versao tem os prefixos de sha256 que a ordem da gerencia deu (todas do operador)', 1),
    ('o runtime novo (runtime_v405.py: os QUATRO registros com funcao caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403, escritos a mao)', 'o runtime novo (runtime_v405.py: os OITO registros com funcao, escritos a mao)', 1),
    ('(a lista de modulos novos LIDA tem DOIS elementos e e a dos ESPERADOS;', '(a lista de modulos novos LIDA tem OITO elementos e e a dos ESPERADOS;', 1),
    (_e1_exame, "exame_pontos: n_checks das pedras da v404 vem do D4; os oito pontos novos", 1),
    ('chk("ast.parse do candidato", sintaxe)\n', 'chk("ast.parse do candidato", sintaxe)\n' + _E1_NOVOS, 1),
])
