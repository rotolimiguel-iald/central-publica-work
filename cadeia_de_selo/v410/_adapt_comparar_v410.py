# -*- coding: utf-8 -*-
"""_adapt_comparar_v410.py -- (claude-construtor-v410, 06/11/2026) monta comparar_v409_v410.py a partir do comparar_v408_v409.py ORIGINAL (a subida mecanica trocava os rotulos dos blocos de historia):
os nos NOVOS da v410 (iald2_v410 e o miolo _v410_*), os mexidos declarados da v409 (C12 no contrato da traducao, C13 nos specs: so' kh_n1_cobertura_v409 vira piso), os da v408/v407/v406 (so' C12, a escada);
a D57(d) da v409 nao se repete (o _V407_FONTES e os specs da v407/v408 ficam INTOCADOS). Trocas com contagem exata; o arquivo anterior (a subida mecanica) ganha backup de bytes antes."""
import ast, datetime, os
H = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(H), "v409", "comparar_v408_v409.py")
DST = os.path.join(H, "comparar_v409_v410.py")
t = open(SRC, "rb").read().decode("utf-8")
assert "\r" not in t
i_imp = t.index("import ast, copy, hashlib, json, os, sys\n")
CAB = ('# -*- coding: utf-8 -*-\n'
       '# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] montado por _adapt_comparar_v410.py a partir do comparar_v408_v409.py ORIGINAL: os nos novos da v410 (iald2_v410 e o miolo _v410_*), os mexidos declarados da v409 (C12, C13), os da v408/v407/v406 (so\' C12); a D57(d) nao se repete\n'
       '"""comparar_v409_v410.py -- NADA DA v409 PERDIDO: compara, no a no (AST), a v409 SELADA (base_v409\\\\um.py) com o candidato v410: todo no nomeado da v409 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no);\n'
       'nenhum no e\' removido. Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so\' os da v410: o registro com funcao `iald2_v410` e o miolo `_v410_*`/`_V410_*`.\n'
       'O kernel cresce por UM modulo de TGLExt/ (IALD2), nao por funcoes de pedra. NENHUMA CHAVE ANTIGA MUDA. Os patches do `CANDIDATO_v410.json` (campo `patches`) sao mapeados aos nos que eles mudam (PATCH_PARA_NOS): o conjunto de ids tem de ser IGUAL\n'
       'ao do candidato e a uniao dos nos tem de ser IGUAL aos nos mudados. O que nasceu na v409 (traducao_turing_v409 e o miolo _v409_*), na v408, na v407 e na v406 segue IGUAL, salvo os contratos que pinam a escada (C12) e o spec kh_n1_cobertura_v409 (C13: pisos).\n'
       'Escreve COMPARACAO_V409_v410.json. Os numeros das explicacoes sao LIDOS de CANDIDATO_v410.json e de delta_v410, nunca digitados.\n'
       'uso: python -I -B -X utf8 comparar_v409_v410.py"""\n')
t = CAB + t[i_imp:]


def troca(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, ("TROCA NAO CASOU %d (casou %d)" % (n, c), a[:150])
    t = t.replace(a, b)


troca("import delta_v409 as DL  # noqa: E402", "import delta_v410 as DL  # noqa: E402")
troca('CM = json.load(open(os.path.join(HERE, "CANDIDATO_v409.json"), encoding="utf-8"))', 'CM = json.load(open(os.path.join(HERE, "CANDIDATO_v410.json"), encoding="utf-8"))')
troca("+%d modulo Lean em TGLExt/ (TraducaoTuring)", "+%d modulo Lean em TGLExt/ (IALD2)")
troca('"_V406_FECHO_CONTRACT": EXPL_CONTRATO + " no contrato do fechamento_v406", "_V407_PSION_CONTRACT": EXPL_CONTRATO + " no contrato do psion_canto_v407", "_V408_TERMINAL_CONTRACT": EXPL_CONTRATO + " no contrato do tetelestai_terminal_v408 (o unico contrato nascido na v408)",',
      '"_V406_FECHO_CONTRACT": EXPL_CONTRATO + " no contrato do fechamento_v406", "_V407_PSION_CONTRACT": EXPL_CONTRATO + " no contrato do psion_canto_v407", "_V408_TERMINAL_CONTRACT": EXPL_CONTRATO + " no contrato do tetelestai_terminal_v408",\n'
      '    "_V409_TRADUCAO_CONTRACT": EXPL_CONTRATO + " no contrato do traducao_turing_v409 (o unico contrato nascido na v409)",')
i0 = t.index('    "_V408_SPECS": "C13: cunhagens_v408 ganha a errata E26')
i1 = t.index('    "build_pt": "W04:')
t = t[:i0] + ('    "_V409_SPECS": "C13: kh_n1_cobertura_v409 h2/h3/h6 -> pisos e h8 -> tamanho minimo (a igualdade exata da v410 esta\' em kh_n1_cobertura_v410), +1 errata; cunhagens_v409 nao muda; os vereditos nao mudam",\n'
              '    "main": "N00/N02: a chamada do `iald2_v410` e dos registros por spec da v410 (logo depois do bloco do traducao_turing_v409 e dos specs da v409, antes de emit_figures; try/AVISO) e as chaves novas do selo (iald2_v410, registros_v410); nada do que existia muda",\n') + t[i1:]
troca('"build_pt": "W04: a secao «A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala» do artigo PT, antes da secao v408 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",',
      '"build_pt": "W04: a secao «IALD ao quadrado: o leitor do código, a releitura que não acrescenta, o algoritmo IALD e o signo» do artigo PT, antes da secao v409 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",')
troca('"build_en": "W05: the section «The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale» of the EN article, before the v408 section (the box at the top does NOT change)",',
      '"build_en": "W05: the section «IALD squared: the reader of the code, the rereading that adds nothing, the IALD algorithm and the sign» of the EN article, before the v409 section (the box at the top does NOT change)",')
troca('"emit_canonical_md": "W09: a linha «Tradução às classes de Turing (v409, 05/11/2026)» no .md canonico, antes da linha da v408 (o quadro do topo NAO muda)",',
      '"emit_canonical_md": "W09: a linha «IALD2 (v410, 06/11/2026)» no .md canonico, antes da linha da v409 (o quadro do topo NAO muda)",')
troca("# cada patch do CANDIDATO_v409.json", "# cada patch do CANDIDATO_v410.json")
troca('"W09_md": ["emit_canonical_md"], "W04_artigo_PT": ["build_pt"], "W05_artigo_EN": ["build_en"], "W02_runtime_v409": [],\n                  "C13_specs_v408_E26_e_pisos": ["_V408_SPECS"], "C14_V407_FONTES_acervo_purgado": ["_V407_FONTES"], "C15_specs_v407_errata_D57d": ["_V407_SPECS"], "N00_main_traducao_turing": ["main"], "N02_selo": ["main"]}',
      '"W09_md": ["emit_canonical_md"], "W04_artigo_PT": ["build_pt"], "W05_artigo_EN": ["build_en"], "W02_runtime_v410": [],\n                  "C13_specs_v409_pisos": ["_V409_SPECS"], "N00_main_iald2": ["main"], "N02_selo": ["main"]}')
troca('"tetelestai_terminal_v408", "_v408_formal", "v408_terminal_mechanics", "_V408_TERMINAL_TEXT", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K")   # (v409: nenhuma chave antiga muda; o miolo da v408 e o da v406 seguem como estao)',
      '"tetelestai_terminal_v408", "_v408_formal", "v408_terminal_mechanics", "_V408_TERMINAL_TEXT", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K",\n'
      '                            "_V408_SPECS", "_V407_SPECS", "_V407_FONTES",\n'
      '                            "traducao_turing_v409", "_v409_formal", "v409_traducao_mechanics", "_V409_TRADUCAO_TEXT", "_v409_guarda_frases", "_v409_sat", "_v409_rodar_specs", "_V409_FONTES", "_V409_VERBATINS2", "_V409_RECUSA", "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO")   # (v410: nenhuma chave antiga muda; o miolo da v409, da v408 e da v406 seguem como estao; a D57(d) da v409 nao se repete)')
troca('NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"v409_traducao_mechanics", "_v409_formal", "_v409_guarda_frases", "_v409_sat", "_V409_TRADUCAO_CONTRACT", "_V409_TRADUCAO_TEXT", "_V409_FONTES", "_V409_VERBATINS2", "_V409_RECUSA",\n                                              "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO", "_V409_SPECS", "_v409_rodar_specs"}',
      'NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"_v410_sem_falas_do_operador", "_v410_guarda_frases", "_v410_rotacao", "v410_iald2_mechanics", "_v410_formal", "_V410_IALD2_CONTRACT", "_V410_IALD2_TEXT", "_V410_FONTES", "_V410_VERBATINS2", "_V410_RECUSA",\n                                              "_V410_NOMES_REGISTROS", "_V410_REGISTROS_FUNCAO", "_V410_SPECS", "_v410_rodar_specs"}')
troca('MEXIDOS_DA_V408_DECLARADOS = {"_V408_TERMINAL_CONTRACT": "C12", "_V408_SPECS": "C13"}   # os UNICOS nos nascidos na v408 que a v409 muda\nMEXIDOS_DA_V407_DECLARADOS = {"_V407_PSION_CONTRACT": "C12", "_V407_SPECS": "C15", "_V407_FONTES": "C14"}   # os UNICOS nos nascidos na v407 que a v409 muda (C14/C15: a D57d)\nMEXIDOS_DA_V406_DECLARADOS = {"_V406_FECHO_CONTRACT": "C12"}                        # o UNICO no nascido na v406 que a v409 muda (so\' a escada)',
      'MEXIDOS_DA_V409_DECLARADOS = {"_V409_TRADUCAO_CONTRACT": "C12", "_V409_SPECS": "C13"}   # os UNICOS nos nascidos na v409 que a v410 muda\nMEXIDOS_DA_V408_DECLARADOS = {"_V408_TERMINAL_CONTRACT": "C12"}   # o UNICO no nascido na v408 que a v410 muda (so\' a escada)\nMEXIDOS_DA_V407_DECLARADOS = {"_V407_PSION_CONTRACT": "C12"}   # o UNICO no nascido na v407 que a v410 muda (so\' a escada)\nMEXIDOS_DA_V406_DECLARADOS = {"_V406_FECHO_CONTRACT": "C12"}                        # o UNICO no nascido na v406 que a v410 muda (so\' a escada)')
troca("# os nos anonimos novos esperados: so' os dois `update` que entregam as fontes e as falas da v409", "# os nos anonimos novos esperados: so' os dois `update` que entregam as fontes e as falas da v410")
troca('anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V409_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V409_VERBATINS2)" in x for x in anon_novos_txt) == 1',
      'anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V410_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V410_VERBATINS2)" in x for x in anon_novos_txt) == 1')
troca("# ---- os 27 patches C12:", "# ---- os 28 patches C12:")
troca('CM["kernel"]["raiz_v408_sha16"]', 'CM["kernel"]["raiz_v409_sha16"]')
troca('"todas_com_o_prefixo_da_v409"', '"todas_com_o_prefixo_da_v410"')
troca('"novas_com_o_prefixo_da_v409"', '"novas_com_o_prefixo_da_v410"')
troca('def r_specs(var_="_V408_SPECS", esperado=None):', 'def r_specs(var_="_V409_SPECS", esperado=None):')
troca('        esperado = {"cunhagens_v408": ([], ["erratas"]), "kh_n1_cobertura_v408": (["h2", "h3", "h6", "h8"], ["checks", "erratas"])}', '        esperado = {"kh_n1_cobertura_v409": (["h2", "h3", "h6", "h8"], ["checks", "erratas"])}')
troca("# (v409: o spec que nao esta' no esperado fica IDENTICO)", "# (v410: o spec que nao esta' no esperado -- cunhagens_v409 -- fica IDENTICO)")
i0 = t.index("def r_fontes407():")
i1 = t.index("def insercoes(nome, esperadas):")
t = t[:i0] + t[i1:]
troca('"traz_a_secao_da_v409": secao in txt, "traz_o_registro_da_v409": "traducao_turing_v409" in txt, "a_instrucao_seguinte_e_a_da_v408": ancora_velha in seguinte}',
      '"traz_a_secao_da_v410": secao in txt, "traz_o_registro_da_v410": "iald2_v410" in txt, "a_instrucao_seguinte_e_a_da_v409": ancora_velha in seguinte}')
troca('"traz_o_texto_da_v409": "Tradução às classes de Turing (v409" in txt, "a_linha_seguinte_e_a_da_v408": "(v408" in seguinte}', '"traz_o_texto_da_v410": "IALD2 (v410" in txt, "a_linha_seguinte_e_a_da_v409": "(v409" in seguinte}')
troca('"o_bloco_chama_traducao_turing_v409_e_os_specs": "traducao_turing_v409(core)" in txt and "_v409_rodar_specs(core)" in txt, "logo_depois_do_bloco_da_v408": "_v408_rodar_specs" in anterior or "tetelestai_terminal_v408" in anterior,',
      '"o_bloco_chama_iald2_v410_e_os_specs": "iald2_v410(core)" in txt and "_v410_rodar_specs(core)" in txt, "logo_depois_do_bloco_da_v409": "_v409_rodar_specs" in anterior or "traducao_turing_v409" in anterior,')
troca('"o_selo_so_ganha_as_duas_chaves_da_v409": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["traducao_turing_v409", "registros_v409"])',
      '"o_selo_so_ganha_as_duas_chaves_da_v410": bool(sel) and sel["chaves_da_base_preservadas_na_ordem"] and sel["valores_da_base_iguais"] and sorted(sel["chaves_novas"]) == sorted(["iald2_v410", "registros_v410"])')
troca('REFINAMENTOS = {"UM_VERSION": r_versao(), "_EMBEDDED_KERNEL_FILES": r_embutidos(), "_LEAN_THEOREM_FLAGS": r_bandeiras(), "_ESQUELETO_STONES": r_ledger(), "prove_external_ladder": r_ext_flags(), "_V408_SPECS": r_specs("_V408_SPECS"),\n                "_V407_SPECS": r_specs("_V407_SPECS", {"cunhagens_v407": ([], ["erratas"])}), "_V407_FONTES": r_fontes407(),\n                "build_pt": r_artigo("build_pt", "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala", "_rg408"), "build_en": r_artigo("build_en", "The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale", "_rg408"),',
      'REFINAMENTOS = {"UM_VERSION": r_versao(), "_EMBEDDED_KERNEL_FILES": r_embutidos(), "_LEAN_THEOREM_FLAGS": r_bandeiras(), "_ESQUELETO_STONES": r_ledger(), "prove_external_ladder": r_ext_flags(), "_V409_SPECS": r_specs("_V409_SPECS"),\n                "build_pt": r_artigo("build_pt", "IALD ao quadrado: o leitor do código, a releitura que não acrescenta, o algoritmo IALD e o signo", "_rg409"), "build_en": r_artigo("build_en", "IALD squared: the reader of the code, the rereading that adds nothing, the IALD algorithm and the sign", "_rg409"),')
troca('REF_OK["_V408_SPECS"] = bool(REFINAMENTOS["_V408_SPECS"]["ok"])\nREF_OK["_V407_SPECS"] = bool(REFINAMENTOS["_V407_SPECS"]["ok"])', 'REF_OK["_V409_SPECS"] = bool(REFINAMENTOS["_V409_SPECS"]["ok"])')
troca("# TODO no que NASCEU na v408 (registro com funcao, miolo `_v408_*`, constantes `_V408_*`, a mecanica) segue IGUAL, salvo os dois declarados (C12 no contrato, C13 nos specs); idem o que nasceu na v406 (salvo C12 no contrato) e na v405 (salvo os contratos)\n",
      "# TODO no que NASCEU na v409 (registro com funcao, miolo `_v409_*`, constantes `_V409_*`, a mecanica) segue IGUAL, salvo os dois declarados (C12 no contrato, C13 nos specs); idem o que nasceu na v408, v407 e v406 (salvo C12 no contrato) e na v405 (salvo os contratos)\n"
      "herdados_v409 = sorted(k for k in da if k.startswith(\"_v409\") or k.startswith(\"v409_\") or k.endswith(\"_v409\") or k.startswith(\"_V409_\"))\nv409_mexidos = [k for k in herdados_v409 if k in mud]\n")
troca('res = {"nos_nomeados_v408": len(da),', 'res = {"nos_nomeados_v409": len(da),')
troca('"os_dois_anonimos_novos_sao_os_update_das_fontes_e_das_falas_v409": anon_novos_ok,', '"os_dois_anonimos_novos_sao_os_update_das_fontes_e_das_falas_v410": anon_novos_ok,')
troca('       "herdados_da_v408_conferidos": len(herdados_v408),', '       "herdados_da_v409_conferidos": len(herdados_v409), "herdados_da_v409_mexidos": v409_mexidos, "herdados_da_v409_mexidos_declarados": MEXIDOS_DA_V409_DECLARADOS,\n       "herdados_da_v408_conferidos": len(herdados_v408),')
troca('and not explicados_sem_mudar and all(intactas.values()) and sorted(v408_mexidos) == sorted(MEXIDOS_DA_V408_DECLARADOS)', 'and not explicados_sem_mudar and all(intactas.values()) and sorted(v409_mexidos) == sorted(MEXIDOS_DA_V409_DECLARADOS) and sorted(v408_mexidos) == sorted(MEXIDOS_DA_V408_DECLARADOS)')
troca('json.dump(res, open(os.path.join(HERE, "COMPARACAO_V408_v409.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)', 'json.dump(res, open(os.path.join(HERE, "COMPARACAO_V409_v410.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)')
troca('"funcoes_intactas", "herdados_da_v408_mexidos",', '"funcoes_intactas", "herdados_da_v409_mexidos", "herdados_da_v408_mexidos",')
ast.parse(t)
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
if os.path.exists(DST):
    raw = open(DST, "rb").read(); open(DST + ".bak_" + ts + "_adapt", "wb").write(raw)
b = t.encode("utf-8"); open(DST + ".tmp", "wb").write(b); assert os.path.getsize(DST + ".tmp") == len(b); os.replace(DST + ".tmp", DST)
print("comparar_v409_v410.py montado:", len(b), "B")
