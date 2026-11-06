# -*- coding: utf-8 -*-
"""_adapt_comparar_v409.py -- (claude-construtor-v409, 05/11/2026) adapta comparar_v408_v409.py (subida mecanica da v408) ao conteudo da v409: o modulo TraducaoTuring, o registro traducao_turing_v409 e o miolo _v409_*,
os nos da v408 que a v409 muda (o contrato do tetelestai_terminal_v408 so' na escada; _V408_SPECS com E26 e pisos) e os da v407 (o contrato do psion so' na escada; _V407_SPECS com a errata da D57d; _V407_FONTES com a chave do acervo repinada).
Trocas com contagem exata (_adapt_util_v409)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("comparar_v408_v409.py")
# ---- a docstring (so' o que diz o que a v409 e')
a.troca("Os nos NOVOS esperados sao so' os da v409: o registro com funcao `tetelestai_terminal_v408` e a mecanica dele ", "Os nos NOVOS esperados sao so' os da v409: o registro com funcao `traducao_turing_v409` e a mecanica dele (v409_traducao_mechanics, _v409_sat) ")
a.troca("(TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), nao um conjunto de funcoes de pedra", "(TraducaoTuring, UM modulo), nao um conjunto de funcoes de pedra")
# ---- as explicacoes
a.troca('"K00/K01: a raiz TGLExt.lean regenerada (+ os %d imports dos modulos novos; o Audit nao muda) e +%d modulos Lean em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP); nenhum arquivo da base some e nenhum muda alem da raiz" % (NM, NM)',
        '"K00/K01: a raiz TGLExt.lean regenerada (+ %d import do modulo novo; o Audit nao muda) e +%d modulo Lean em TGLExt/ (TraducaoTuring); nenhum arquivo da base some e nenhum muda alem da raiz" % (NM, NM)')
a.troca('"_V406_FECHO_CONTRACT": EXPL_CONTRATO + " no contrato do fechamento_v406", "_V407_PSION_CONTRACT": EXPL_CONTRATO + " no contrato do psion_canto_v407 (o unico contrato nascido na v408)",',
        '"_V406_FECHO_CONTRACT": EXPL_CONTRATO + " no contrato do fechamento_v406", "_V407_PSION_CONTRACT": EXPL_CONTRATO + " no contrato do psion_canto_v407", "_V408_TERMINAL_CONTRACT": EXPL_CONTRATO + " no contrato do tetelestai_terminal_v408 (o unico contrato nascido na v408)",')
a.troca('    "_V407_SPECS": "C13: cunhagens_v407 ganha a errata E21 AO LADO (nenhuma checagem muda) e kh_n1_cobertura_v407 h2/h3/h6 -> pisos e h8 -> tamanho minimo (a igualdade exata da v409 esta\' em kh_n1_cobertura_v408); +1 errata em cada spec; os vereditos nao mudam",\n',
        '    "_V408_SPECS": "C13: cunhagens_v408 ganha a errata E26 AO LADO (nenhuma checagem muda) e kh_n1_cobertura_v408 h2/h3/h6 -> pisos e h8 -> tamanho minimo (a igualdade exata da v409 esta\' em kh_n1_cobertura_v409); +1 errata em cada spec; os vereditos nao mudam",\n'
        '    "_V407_SPECS": "C15: cunhagens_v407 ganha a errata da D57(d) AO LADO (o insumo do acervo repinado na copia purgada; nenhuma checagem muda); kh_n1_cobertura_v407 nao muda; o veredito nao muda",\n'
        '    "_V407_FONTES": "C14: D57(d) -- so\' a chave psion_no_acervo_do_imac_03nov muda: a copia PURGADA (a mesma que a v408 pinou) no lugar da integra, que fica citada so\' por sha16",\n')
a.troca('    "main": "N00/N02: a chamada do `tetelestai_terminal_v408` e dos registros por spec da v409 (logo depois do bloco do psion_canto_v407 e dos specs da v408, antes de emit_figures; try/AVISO) e as chaves novas do selo (tetelestai_terminal_v408, registros_v408); nada do que existia muda",',
        '    "main": "N00/N02: a chamada do `traducao_turing_v409` e dos registros por spec da v409 (logo depois do bloco do tetelestai_terminal_v408 e dos specs da v408, antes de emit_figures; try/AVISO) e as chaves novas do selo (traducao_turing_v409, registros_v409); nada do que existia muda",')
a.troca('    "build_pt": "W04: a secao «Tetelestai é o terminal: a leitura, a poda, a quitação; o tempo é a moeda de β; o dicionário e o ponto de contradição» do artigo PT, antes da secao v408 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",',
        '    "build_pt": "W04: a secao «A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala» do artigo PT, antes da secao v408 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",')
a.troca('    "build_en": "W05: the section «Tetelestai is the terminal: the reading, the pruning, the settlement; time is the currency of β; the dictionary and the point of contradiction» of the EN article, before the v408 section (the box at the top does NOT change)",',
        '    "build_en": "W05: the section «The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale» of the EN article, before the v408 section (the box at the top does NOT change)",')
a.troca('    "emit_canonical_md": "W09: a linha «Tetelestai é o terminal (v409, 04/11/2026)» no .md canonico, antes da linha da v408 (o quadro do topo NAO muda)",',
        '    "emit_canonical_md": "W09: a linha «Tradução às classes de Turing (v409, 05/11/2026)» no .md canonico, antes da linha da v408 (o quadro do topo NAO muda)",')
a.troca('                  "C13_specs_v408_E21_e_pisos": ["_V407_SPECS"], "N00_main_tetelestai_terminal": ["main"], "N02_selo": ["main"]}',
        '                  "C13_specs_v408_E26_e_pisos": ["_V408_SPECS"], "C14_V407_FONTES_acervo_purgado": ["_V407_FONTES"], "C15_specs_v407_errata_D57d": ["_V407_SPECS"], "N00_main_traducao_turing": ["main"], "N02_selo": ["main"]}')
a.troca('"psion_canto_v407", "_v407_formal", "_v407_chaves", "_v407_elo_lido", "v407_psion_mechanics", "_V407_PSION_TEXT", "_v407_guarda_frases", "_v407_rodar_specs", "_V407_FONTES", "_V407_VERBATINS2")   # (v409: nenhuma chave ',
        '"psion_canto_v407", "_v407_formal", "_v407_chaves", "_v407_elo_lido", "v407_psion_mechanics", "_V407_PSION_TEXT", "_v407_guarda_frases", "_v407_rodar_specs", "_V407_VERBATINS2",\n'
        '                            "tetelestai_terminal_v408", "_v408_formal", "v408_terminal_mechanics", "_V408_TERMINAL_TEXT", "_v408_guarda_frases", "_v408_rodar_specs", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA", "_V408_KB_SI_J_PER_K")   # (v409: nenhuma chave ')
a.troca('NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"v408_terminal_mechanics", "_v408_formal", "_v408_guarda_frases", "_V408_KB_SI_J_PER_K", "_V408_TERMINAL_CONTRACT", "_V408_TERMINAL_TEXT", "_V408_FONTES", "_V408_VERBATINS2", "_V408_RECUSA",\n'
        '                                              "_V408_NOMES_REGISTROS", "_V408_REGISTROS_FUNCAO", "_V408_SPECS", "_v408_rodar_specs"}\n'
        'MEXIDOS_DA_V408_DECLARADOS = {"_V407_PSION_CONTRACT": "C12", "_V407_SPECS": "C13"}   # os UNICOS nos nascidos na v408 que a v409 muda\n',
        'NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"v409_traducao_mechanics", "_v409_formal", "_v409_guarda_frases", "_v409_sat", "_V409_TRADUCAO_CONTRACT", "_V409_TRADUCAO_TEXT", "_V409_FONTES", "_V409_VERBATINS2", "_V409_RECUSA",\n'
        '                                              "_V409_NOMES_REGISTROS", "_V409_REGISTROS_FUNCAO", "_V409_SPECS", "_v409_rodar_specs"}\n'
        'MEXIDOS_DA_V408_DECLARADOS = {"_V408_TERMINAL_CONTRACT": "C12", "_V408_SPECS": "C13"}   # os UNICOS nos nascidos na v408 que a v409 muda\n'
        'MEXIDOS_DA_V407_DECLARADOS = {"_V407_PSION_CONTRACT": "C12", "_V407_SPECS": "C15", "_V407_FONTES": "C14"}   # os UNICOS nos nascidos na v407 que a v409 muda (C14/C15: a D57d)\n')
a.troca('anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V408_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V408_VERBATINS2)" in x for x in anon_novos_txt) == 1',
        'anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V409_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V409_VERBATINS2)" in x for x in anon_novos_txt) == 1')
a.troca("# ---- os 26 patches C12:", "# ---- os 27 patches C12:")
# ---- os specs: parametrizado (v408: E26 e pisos; v407: a errata da D57d so' no cunhagens_v407)
a.troca('def r_specs():\n    a, b = da["_V407_SPECS"].value.elts, db["_V407_SPECS"].value.elts\n',
        'def r_specs(var_="_V408_SPECS", esperado=None):\n    a, b = da[var_].value.elts, db[var_].value.elts\n')
a.troca('        out[nome] = {"mesmas_chaves": chaves_iguais, "chaves_que_mudam": sorted(dif), "checks_com_mesmos_ids": ids(ca) == ids(cb), "checks_que_mudam": ch_dif, "erratas_a_base_e_prefixo": len(eb) == len(ea) + 1 and all(dump_eq(x, y) for x, y in zip(ea, eb))}\n'
        '    esperado = {"cunhagens_v407": ([], ["erratas"]), "kh_n1_cobertura_v407": (["h2", "h3", "h6", "h8"], ["checks", "erratas"])}\n'
        '    out["ok"] = bool(out["mesmo_numero_de_specs"] and set(esperado) <= set(out) and all(out[n_]["mesmas_chaves"] and out[n_]["chaves_que_mudam"] == v_[1] and out[n_]["checks_com_mesmos_ids"] and out[n_]["checks_que_mudam"] == v_[0] and out[n_]["erratas_a_base_e_prefixo"] for n_, v_ in esperado.items()))\n',
        '        out[nome] = {"mesmas_chaves": chaves_iguais, "chaves_que_mudam": sorted(dif), "checks_com_mesmos_ids": ids(ca) == ids(cb), "checks_que_mudam": ch_dif, "erratas_a_base_e_prefixo": len(eb) == len(ea) + 1 and all(dump_eq(x, y) for x, y in zip(ea, eb)), "identico": dump_eq(sa_, sb_)}\n'
        '    if esperado is None:\n'
        '        esperado = {"cunhagens_v408": ([], ["erratas"]), "kh_n1_cobertura_v408": (["h2", "h3", "h6", "h8"], ["checks", "erratas"])}\n'
        '    out["ok"] = bool(out["mesmo_numero_de_specs"] and set(esperado) <= set(out) and all(out[n_]["mesmas_chaves"] and out[n_]["chaves_que_mudam"] == v_[1] and out[n_]["checks_com_mesmos_ids"] and out[n_]["checks_que_mudam"] == v_[0] and out[n_]["erratas_a_base_e_prefixo"] for n_, v_ in esperado.items())\n'
        '                     and all(v_["identico"] for n_, v_ in out.items() if isinstance(v_, dict) and n_ not in esperado))   # (v409: o spec que nao esta\' no esperado fica IDENTICO)\n')
a.troca('def insercoes(nome, esperadas):',
        'def r_fontes407():\n'
        '    """D57(d): no _V407_FONTES so\' a chave do acervo muda, e para a copia purgada (o sha256 e os bytes da v408), com a integra so\' por sha16."""\n'
        '    fa_, fb_ = ast.literal_eval(da["_V407_FONTES"].value), ast.literal_eval(db["_V407_FONTES"].value)\n'
        '    muda_ = sorted(k_ for k_ in fa_ if fa_[k_] != fb_.get(k_))\n'
        '    e_ = fb_.get(DL.CHAVE_ACERVO_V407) or {}\n'
        '    return {"mesmas_chaves": sorted(fa_) == sorted(fb_), "so_a_chave_do_acervo_muda": muda_ == [DL.CHAVE_ACERVO_V407], "a_nova_e_a_copia_purgada": e_.get("sha256") == DL.PURGADO_SHA256 and e_.get("arquivo") == DL.PURGADO_ARQ,\n'
        '            "a_antiga_era_a_integra": (fa_.get(DL.CHAVE_ACERVO_V407) or {}).get("sha256") == DL.ORIGEM_PURGA_SHA256, "a_integra_so_por_sha16": DL.ORIGEM_PURGA_SHA16_DA_ORDEM in str(e_.get("papel")) and DL.ORIGEM_PURGA_SHA256 not in json.dumps(fb_)}\n'
        '\n\n'
        'def insercoes(nome, esperadas):')
a.troca('"traz_a_secao_da_v409": secao in txt, "traz_o_registro_da_v409": "tetelestai_terminal_v408" in txt,', '"traz_a_secao_da_v409": secao in txt, "traz_o_registro_da_v409": "traducao_turing_v409" in txt,')
a.troca('"traz_o_texto_da_v409": "Tetelestai é o terminal (v409" in txt,', '"traz_o_texto_da_v409": "Tradução às classes de Turing (v409" in txt,')
a.troca('"o_bloco_chama_tetelestai_terminal_v409_e_os_specs": "tetelestai_terminal_v408(core)" in txt and "_v408_rodar_specs(core)" in txt, "logo_depois_do_bloco_da_v408": "_v407_rodar_specs" in anterior or "psion_canto_v407" in anterior,',
        '"o_bloco_chama_traducao_turing_v409_e_os_specs": "traducao_turing_v409(core)" in txt and "_v409_rodar_specs(core)" in txt, "logo_depois_do_bloco_da_v408": "_v408_rodar_specs" in anterior or "tetelestai_terminal_v408" in anterior,')
a.troca('sorted(sel["chaves_novas"]) == sorted(["tetelestai_terminal_v408", "registros_v408"])', 'sorted(sel["chaves_novas"]) == sorted(["traducao_turing_v409", "registros_v409"])')
a.troca('REFINAMENTOS = {"UM_VERSION": r_versao(), "_EMBEDDED_KERNEL_FILES": r_embutidos(), "_LEAN_THEOREM_FLAGS": r_bandeiras(), "_ESQUELETO_STONES": r_ledger(), "prove_external_ladder": r_ext_flags(), "_V407_SPECS": r_specs(),\n'
        '                "build_pt": r_artigo("build_pt", "Tetelestai é o terminal: a leitura, a poda, a quitação", "_rg407"), "build_en": r_artigo("build_en", "Tetelestai is the terminal: the reading, the pruning, the settlement", "_rg407"),',
        'REFINAMENTOS = {"UM_VERSION": r_versao(), "_EMBEDDED_KERNEL_FILES": r_embutidos(), "_LEAN_THEOREM_FLAGS": r_bandeiras(), "_ESQUELETO_STONES": r_ledger(), "prove_external_ladder": r_ext_flags(), "_V408_SPECS": r_specs("_V408_SPECS"),\n'
        '                "_V407_SPECS": r_specs("_V407_SPECS", {"cunhagens_v407": ([], ["erratas"])}), "_V407_FONTES": r_fontes407(),\n'
        '                "build_pt": r_artigo("build_pt", "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala", "_rg408"), "build_en": r_artigo("build_en", "The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale", "_rg408"),')
a.troca('REF_OK["_V407_SPECS"] = bool(REFINAMENTOS["_V407_SPECS"]["ok"])\n', 'REF_OK["_V408_SPECS"] = bool(REFINAMENTOS["_V408_SPECS"]["ok"])\nREF_OK["_V407_SPECS"] = bool(REFINAMENTOS["_V407_SPECS"]["ok"])\n')
a.troca('herdados_v408 = sorted(k for k in da if k.startswith("_v407") or k.startswith("v408_") or k.endswith("_v407") or k.startswith("_V408_"))\nv408_mexidos = [k for k in herdados_v408 if k in mud]\n',
        'herdados_v408 = sorted(k for k in da if k.startswith("_v408") or k.startswith("v408_") or k.endswith("_v408") or k.startswith("_V408_"))\nv408_mexidos = [k for k in herdados_v408 if k in mud]\n'
        'herdados_v407 = sorted(k for k in da if k.startswith("_v407") or k.startswith("v407_") or k.endswith("_v407") or k.startswith("_V407_"))\nv407_mexidos = [k for k in herdados_v407 if k in mud]\n')
a.troca('"herdados_da_v406_conferidos": len(herdados_v406),', '"herdados_da_v407_conferidos": len(herdados_v407), "herdados_da_v407_mexidos": v407_mexidos, "herdados_da_v407_mexidos_declarados": MEXIDOS_DA_V407_DECLARADOS, "herdados_da_v406_conferidos": len(herdados_v406),')
a.troca('and sorted(v408_mexidos) == sorted(MEXIDOS_DA_V408_DECLARADOS) and sorted(v406_mexidos)', 'and sorted(v408_mexidos) == sorted(MEXIDOS_DA_V408_DECLARADOS) and sorted(v407_mexidos) == sorted(MEXIDOS_DA_V407_DECLARADOS) and sorted(v406_mexidos)')
a.troca('"herdados_da_v408_mexidos", "herdados_da_v406_mexidos",', '"herdados_da_v408_mexidos", "herdados_da_v407_mexidos", "herdados_da_v406_mexidos",')
a.marca("NADA DA v408 PERDIDO: os nos novos da v409 (traducao_turing_v409 e o miolo _v409_*), os mexidos declarados da v408 (C12, C13) e da v407 (C12, C14, C15: a D57d), os refinamentos da secao, da linha do md, do main e do selo")
a.grava()
