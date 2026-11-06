# -*- coding: utf-8 -*-
"""_adapt_esperados_v409.py -- (claude-construtor-v409, 05/11/2026) adapta gerar_esperados_v409.py (subida mecanica da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
o registro NOVO com funcao e' traducao_turing_v409 (1 modulo, 62 ancoras, 17 checagens); o tetelestai_terminal_v408 (v408), o psion_canto_v407 (v407) e o fechamento_v406 sao HERDADOS (recriados);
as chaves do ESPERADOS seguem o esquema que o pos-rito adaptado le (registros_funcao_v409.traducao_turing, _v408.tetelestai_terminal, _v407.psion_canto; estrelas_v409/v408/v407; bundle_v408/v407/v406_sha256;
chaves_v409 vazio e chaves_v407_esperadas; decisoes_v409_ids D55-D60; erratas_E24_E26; md_traducao lida do candidato). Trocas com contagem exata (_adapt_util_v409)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("gerar_esperados_v409.py")
i = a.t.index('"""gerar_esperados_v409.py --'); j = a.t.index('uso: python -I -B -X utf8 gerar_esperados_v409.py"""') + len('uso: python -I -B -X utf8 gerar_esperados_v409.py"""')
a.t = a.t[:i] + '''"""gerar_esperados_v409.py -- ESPERADOS_v409.json LIDOS dos artefatos (molde: gerar_esperados_v408.py FINAL, com as licoes da v399 a v408; adaptado em 05/11/2026 por claude-construtor-v409 a v409, A TRADUCAO AS CLASSES DE TURING:
bundle de 1 modulo em TGLExt/ -- TraducaoTuring --, registro com funcao traducao_turing_v409, 62 ancoras, 17 checagens): o estado SELADO da v408 pinado.
A TROCA DITA da v409 e' SO' de NUMEROS: os vereditos da v408 que carregam os numeros do kernel (escada, declaracoes, arquivos varridos) e o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py -- achados por script no ensaio (recomputados; so' numeros mudam).
NAO ha troca dita de TEXTO (o CANDIDATO_v409.json nao declara `troca_dita_v409`) e NENHUMA chave antiga muda: os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406, psion_canto_v407 e tetelestai_terminal_v408 NAO mudam; `troca_dita_textual` fica vazio, por asseveracao (se o ensaio medir que algum deles mudou, este script PARA no assert: e' defeito do candidato ou do contrato, nao se 'conserta' aqui).
Todos os outros vereditos da v408 ficam IGUAIS (os registros das v399 a v408 sao RECRIADOS e iguais ao selado; o fechamento_v406, o psion_canto_v407 e o tetelestai_terminal_v408 recriados com a escada do contrato subida pela C12, o veredito igual). +3 chaves novas no core (traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409) e +2 chaves no selo (traducao_turing_v409 e registros_v409); o selo pela propria tecnologia (v399) muda so' nos hashes do novo um.py. O pilar pela mesma chave.
O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\\\insumos\\\\fase9) e o conferidor os confere de novo.
As CHAVES: nenhuma nova e nenhuma antiga muda (`chaves_v409` vazio); as que o psion_canto_v407 le seguem como na v408 selada (`chaves_v407_esperadas`, lidas do ensaio e asseveradas iguais as de ESPERADOS_v408); full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
O GATE NAO SE MOVE: o qg_closure da v409 e' IDENTICO ao da v408 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v408, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e' reescrita (o angle_status antigo fica):
o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e' o da base).
Nada digitado: cada numero e hash vem de CANDIDATO_v409.json, ensaio_a_seco_v409.json, do core/selo da v408 (base_v408), de kernel\\\\FLAGS_v409.json, kernel\\\\KH_N1_v409.json, de ESPERADOS_v408.json (o que o quadro pinou e os registros da v408) e do resultado pinado. As chaves herdadas guardam os nomes da v408:
`vereditos_v408`, `flags_true_v408`... sao o estado da BASE; `registros_funcao_v405/v404/v403` e `estrelas_v405/v404/v403` sao os pinos dos registros de pedra das versoes anteriores (RECRIADOS), lidos de ESPERADOS_v408;
`registros_funcao_v406.fechamento` e `estrelas_v406` sao o fechamento_v406 herdado; `registros_funcao_v407.psion_canto` e `estrelas_v407` (as 76 ancoras) sao o psion_canto_v407 herdado; `registros_funcao_v408.tetelestai_terminal` e `estrelas_v408` (as 48 ancoras) sao o tetelestai_terminal_v408 herdado (RECRIADOS neste rito);
`registros_funcao_v409.traducao_turing` e `estrelas_v409` (as 62 ancoras) sao os desta versao; `bundle_v408_sha256` (os 4 modulos do terminal), `bundle_v407_sha256` (os 9 do psion) e `bundle_v406_sha256` (os 301 do fecho) seguem no kernel como registro, e `pedras_v405_sha256` (as TREZE pedras seladas das versoes anteriores).
As erratas E24 a E26 e as decisoes D55 a D60 da gerencia vao nos registros (cunhagens_v409); aqui so' se pinam os vereditos, os valores, as ancoras e os contratos.
ORDEM DE USO: depende do ensaio (ensaio_a_seco_v409.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed). uso: python -I -B -X utf8 gerar_esperados_v409.py"""''' + a.t[j:]
a.troca('sys.modules.setdefault("delta_v408", DL)   # quadro_v397.py (copia da v408, nao adaptada nesta pasta) faz `import delta_v408`, que nao existe aqui; delta_v409 traz o mesmo F9_CAMINHOS e o mesmo lido(); defeito apontado no relatorio (quadro_v397.py:12)\n', '')
a.troca('for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407"):   # estes cinco NAO mudam',
        'for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408"):   # estes seis NAO mudam')
a.troca('"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407")\nassert all(k in selo0 for k in SEL_KEYS)',
        '"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407", "tetelestai_terminal_v408", "registros_v408")\nassert all(k in selo0 for k in SEL_KEYS)')
a.troca('assert set(selo_chaves_que_mudam) <= {"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407"}, selo_chaves_que_mudam',
        'assert set(selo_chaves_que_mudam) <= {"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407", "tetelestai_terminal_v408", "registros_v408"}, selo_chaves_que_mudam')
a.troca('TV408 = E408["titulo_secao_v408"]   # {pt, en} = «O psíon e o canto: a passagem sob compressão e o par» (a secao da v408 vem logo depois da v409)',
        'TV408 = E408["titulo_secao_v408"]   # {pt, en} = o titulo da secao da v408 (Tetelestai e\' o terminal), que vem logo depois da secao da v409')
# o registro NOVO e os HERDADOS
a.troca('''# ---- o registro NOVO com funcao (tetelestai_terminal_v408) e os HERDADOS (psion_canto_v407 e fechamento_v406, RECRIADOS neste rito)
PS = _ens_reg(DL.FECHO_REGISTRO)
PC7 = _ens_reg("psion_canto_v407")
FE6 = _ens_reg("fechamento_v406")
PSV = RG.texto_terminal()["veredito_ok"]''',
        '''# ---- o registro NOVO com funcao (traducao_turing_v409) e os HERDADOS (tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406, RECRIADOS neste rito)
PS = _ens_reg(DL.FECHO_REGISTRO)
TT8 = _ens_reg(DL.D8.FECHO_REGISTRO)
PC7 = _ens_reg("psion_canto_v407")
FE6 = _ens_reg("fechamento_v406")
PSV = RG.texto_traducao()["veredito_ok"]''')
a.troca('''assert PV["n_ancoras_ok"] == PV["n_ancoras"] == len(DL.ANCORAS) and PV["n_modulos_ok"] == PV["n_modulos"] == DL.N_BUNDLE and PV["n_flags_true"] == PV["n_flags"] == CM["n_bandeiras"] and PV["escada"][0] == PV["escada"][1] == PV["escada"][2] == CM["escada"][1] and PV.get("respostas_ok") is True and (PV.get("insumo_purgado") or {}).get("ok") is True, (PV.get("escada"), PV.get("respostas_ok"))
# o psion_canto_v407 HERDADO (recriado com a escada do contrato subida pela C12): as cinco chaves que ele le seguem EXATAMENTE como na v408 selada (nenhuma chave antiga muda); o veredito e' o selado
chaves_v408_esperadas = dict(PC7["values"]["chaves"])
assert chaves_v408_esperadas["kernel_reads_the_link"] is True and chaves_v408_esperadas["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and chaves_v408_esperadas["rede_fock_v394.whole_certificate_inhabited"] is True \\
    and chaves_v408_esperadas["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and chaves_v408_esperadas["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and chaves_v408_esperadas["witness_layers.canonical_full_witness_term_constructed"] is True \\
    and chaves_v408_esperadas["witness_rigidity.trivial_inhabitant_exists"] is False and chaves_v408_esperadas["qg_closure.gate.full_static_witness_exists"] is False and chaves_v408_esperadas == E408["chaves_v408_esperadas"], chaves_v408_esperadas
assert PC7["all_verified"] is True and PC7["n_checks"] == DL.D7.N_CHECKS_FECHO and PC7["verdict"] == V("psion_canto_v407") == MF4.get("psion_canto_v407", {"verdict": V("psion_canto_v407")})["verdict"] and PC7["values"]["elo_lido_do_kernel"] is True and PC7["values"]["escada"] == [CM["escada"][1]] * 3 \\
    and PC7["values"]["n_ancoras_ok"] == PC7["values"]["n_ancoras"] == len(E408["estrelas_v408"]) and PC7["values"]["n_modulos_ok"] == PC7["values"]["n_modulos"] == len(E408["bundle_sha256"]), (PC7.get("verdict"), PC7.get("n_checks"))''',
        '''assert PV["n_ancoras_ok"] == PV["n_ancoras"] == len(DL.ANCORAS) and PV["n_modulos_ok"] == PV["n_modulos"] == DL.N_BUNDLE and PV["n_flags_true"] == PV["n_flags"] == CM["n_bandeiras"] and PV["escada"][0] == PV["escada"][1] == PV["escada"][2] == CM["escada"][1] and PV.get("respostas_ok") is True \\
    and (PV.get("instancia_sim") or {}).get("solucoes", 0) >= 1 and (PV.get("instancia_nao") or {}).get("solucoes") == 0 and CM["acervo_v407_repinado"]["sha256"] == DL.PURGADO_SHA256, (PV.get("escada"), PV.get("respostas_ok"), PV.get("instancia_sim"), PV.get("instancia_nao"))
# o tetelestai_terminal_v408 HERDADO (recriado com a escada do contrato subida pela C12): o veredito e' o selado; as 48 ancoras e os 4 modulos da v408
TV8 = TT8["values"]
assert TT8["all_verified"] is True and TT8["n_checks"] == DL.D8.N_CHECKS_FECHO and TT8["verdict"] == V(DL.D8.FECHO_REGISTRO) and TV8["escada"] == [CM["escada"][1]] * 3 and TV8.get("respostas_ok") is True and (TV8.get("insumo_purgado") or {}).get("ok") is True \\
    and TV8["n_ancoras_ok"] == TV8["n_ancoras"] == len(E408["estrelas_v408"]) and TV8["n_modulos_ok"] == TV8["n_modulos"] == len(E408["bundle_sha256"]) and TV8["n_flags_true"] == TV8["n_flags"] == E408["n_bandeiras_novas"], (TT8.get("verdict"), TT8.get("n_checks"), TV8.get("escada"))
# o psion_canto_v407 HERDADO (recriado com a escada do contrato subida pela C12): as chaves que ele le seguem EXATAMENTE como na v408 selada (nenhuma chave antiga muda); o veredito e' o selado
chaves_v407_esperadas = dict(PC7["values"]["chaves"])
assert chaves_v407_esperadas["kernel_reads_the_link"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and chaves_v407_esperadas["rede_fock_v394.whole_certificate_inhabited"] is True \\
    and chaves_v407_esperadas["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["witness_layers.canonical_full_witness_term_constructed"] is True \\
    and chaves_v407_esperadas["witness_rigidity.trivial_inhabitant_exists"] is False and chaves_v407_esperadas["qg_closure.gate.full_static_witness_exists"] is False and chaves_v407_esperadas == E408["chaves_v407_esperadas"], chaves_v407_esperadas
assert PC7["all_verified"] is True and PC7["n_checks"] == DL.D7.N_CHECKS_FECHO and PC7["verdict"] == V("psion_canto_v407") and PC7["values"]["elo_lido_do_kernel"] is True and PC7["values"]["escada"] == [CM["escada"][1]] * 3 \\
    and PC7["values"]["n_ancoras_ok"] == PC7["values"]["n_ancoras"] == len(E408["estrelas_v407"]) and PC7["values"]["n_modulos_ok"] == PC7["values"]["n_modulos"] == len(E408["bundle_v407_sha256"]), (PC7.get("verdict"), PC7.get("n_checks"))''')
a.troca('assert FE6["all_verified"] is True and FE6["n_checks"] == DL.D6.N_CHECKS_FECHO and FE6["verdict"] == V("fechamento_v406") == MF4.get("fechamento_v406", {"verdict": V("fechamento_v406")})["verdict"], (FE6.get("verdict"), V("fechamento_v406"))',
        'assert FE6["all_verified"] is True and FE6["n_checks"] == DL.D6.N_CHECKS_FECHO and FE6["verdict"] == V("fechamento_v406"), (FE6.get("verdict"), V("fechamento_v406"))')
a.troca('''# os registros por spec da v406 (versionados na v408 pela E20) e da v408 (cunhagens_v407 com a errata E21 ao lado; kh_n1_cobertura_v407 com pisos em h2/h3/h6/h8): RECRIADOS, o veredito NAO muda
for n_ in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO, DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO):''',
        '''# os registros por spec da v406 (versionados na v408 pela E20), da v407 (cunhagens_v407 com a errata E21 e, nesta versao, a da D57(d) ao lado; kh_n1_cobertura_v407 com pisos) e da v408 (cunhagens_v408 com a errata E26 ao lado; kh_n1_cobertura_v408 com pisos pela C13): RECRIADOS, o veredito NAO muda
for n_ in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO, DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO, DL.D8.CUNHAGENS_REGISTRO, DL.D8.KH_REGISTRO):''')
a.troca('"bundle_sha256": pins, "bundle_v408_sha256": E408["bundle_sha256"], "bundle_v406_sha256": E408["bundle_v406_sha256"],',
        '"bundle_sha256": pins, "bundle_v408_sha256": E408["bundle_sha256"], "bundle_v407_sha256": E408["bundle_v407_sha256"], "bundle_v406_sha256": E408["bundle_v406_sha256"],')
a.troca('"titulo_secao_v409": TIT409, "titulo_secao_v408": dict(TV408),', '"titulo_secao_v409": TIT409, "titulo_secao_v408": dict(TV408), "titulo_secao_v407": dict(E408["titulo_secao_v407"]),')
a.troca('''       "registros_v408": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},   # os dois por spec desta versao (o de funcao, tetelestai_terminal_v408, esta' em registros_funcao_v409)
       "registros_v407": {k: V(k) for k in (DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO)},   # os dois por spec da v408: RECRIADOS (E21 ao lado; pisos no kh), veredito igual ao selado''',
        '''       "registros_v409": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},   # os dois por spec desta versao (o de funcao, traducao_turing_v409, esta' em registros_funcao_v409)
       "registros_v408": {k: V(k) for k in (DL.D8.CUNHAGENS_REGISTRO, DL.D8.KH_REGISTRO)},   # os dois por spec da v408: RECRIADOS (E26 ao lado; pisos no kh pela C13), veredito igual ao selado
       "registros_v407": {k: V(k) for k in (DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO)},   # os dois por spec da v407: RECRIADOS (E21 e a errata da D57(d) ao lado; pisos no kh), veredito igual ao selado''')
a.troca('''       "registros_funcao_v409": {"tetelestai_terminal": {"nome": DL.FECHO_REGISTRO, "verdict": PS["verdict"], "values": PS["values"], "n_checks": PS["n_checks"]}},
       "registros_funcao_v408": {"psion_canto": {"nome": DL.D7.FECHO_REGISTRO, "verdict": PC7["verdict"], "values": PC7["values"], "n_checks": PC7["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},''',
        '''       "registros_funcao_v409": {"traducao_turing": {"nome": DL.FECHO_REGISTRO, "verdict": PS["verdict"], "values": PS["values"], "n_checks": PS["n_checks"]}},
       "registros_funcao_v408": {"tetelestai_terminal": {"nome": DL.D8.FECHO_REGISTRO, "verdict": TT8["verdict"], "values": TT8["values"], "n_checks": TT8["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},
       "registros_funcao_v407": {"psion_canto": {"nome": DL.D7.FECHO_REGISTRO, "verdict": PC7["verdict"], "values": PC7["values"], "n_checks": PC7["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},''')
a.troca('"estrelas_v408": E408["estrelas_v408"], "estrelas_v406": E408["estrelas_v406"],', '"estrelas_v408": E408["estrelas_v408"], "estrelas_v407": E408["estrelas_v407"], "estrelas_v406": E408["estrelas_v406"],')
a.troca('''"decisoes_v409_ids": sorted((k for k in DL.DECISOES if k[1:].isdigit() and int(k[1:]) >= 48), key=lambda k: int(k[1:])), "erratas_E21_E23": list(DL.ERRATAS_V409),''',
        '''"decisoes_v409_ids": list(DL.DECISOES_V409), "erratas_E24_E26": list(DL.ERRATAS_V409),''')
a.troca('''"chaves_v409": [dict(c_) for c_ in DL.CHAVES_V409], "chaves_v407": [dict(c_) for c_ in DL.CHAVES_V408], "chaves_v408_esperadas": chaves_v408_esperadas,''',
        '''"chaves_v409": [dict(c_) for c_ in DL.CHAVES_V409], "chaves_v408": [dict(c_) for c_ in DL.CHAVES_V408], "chaves_v407": [dict(c_) for c_ in E408["chaves_v407"]], "chaves_v407_esperadas": chaves_v407_esperadas,''')
a.troca('''"md_fechamento": E408["md_fechamento"], "md_psion": E408["md_psion"],   # (md_psion: a linha da v408, que fica logo depois da nova; md_fechamento: a da v406)''',
        '''"md_fechamento": E408["md_fechamento"], "md_psion": E408["md_psion"], "md_tetelestai": E408["md_tetelestai"],   # (md_tetelestai: a linha da v408, que fica logo depois da nova; md_psion: a da v407; md_fechamento: a da v406)''')
a.troca('''# a linha do .md da v409 (nova) sai do PROPRIO candidato (nada digitado): «> **Tetelestai é o terminal (v409, DD/MM/AAAA):**» antes da linha da v408
_cand_txt = open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8")
_mdp = re.findall(r"> \\*\\*(Tetelestai [^*:]*?\\(v409, \\d\\d/\\d\\d/\\d{4}\\)):\\*\\*", _cand_txt)
assert len(set(_mdp)) == 1, ("a linha do .md da v409 nao e' unica no candidato", set(_mdp))
esp["md_tetelestai"] = _mdp[0]''',
        '''# a linha do .md da v409 (nova) sai do PROPRIO candidato (nada digitado): «> **Tradução às classes de Turing (v409, DD/MM/AAAA):**» antes da linha da v408
_cand_txt = open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8")
_mdp = re.findall(r"> \\*\\*(Tradução [^*:]*?\\(v409, \\d\\d/\\d\\d/\\d{4}\\)):\\*\\*", _cand_txt)
assert len(set(_mdp)) == 1, ("a linha do .md da v409 nao e' unica no candidato", set(_mdp))
esp["md_traducao"] = _mdp[0]
assert esp["md_tetelestai"] == "Tetelestai é o terminal (v408, 04/11/2026)" or esp["md_tetelestai"] in _cand_txt, "a linha do .md da v408 nao esta' no candidato"''')
a.troca('''CM["h8"]["pino_antigo_v408_entradas"] + len(DL.BUNDLE_RELS)''', '''CM["h8"]["pino_antigo_v408_entradas"] + len(DL.BUNDLE_RELS)''')
a.troca('''assert len(esp["bundle_v408_sha256"]) == E408["kernel"]["modulos_novos"] and all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp["bundle_v408_sha256"].items()), "o bundle da v408 nao esta' todo no hash formal do core selado"''',
        '''assert len(esp["bundle_v408_sha256"]) == E408["kernel"]["modulos_novos"] and all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp["bundle_v408_sha256"].items()), "o bundle da v408 nao esta' todo no hash formal do core selado"
assert len(esp["bundle_v407_sha256"]) == 9 and all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp["bundle_v407_sha256"].items()), "o bundle da v407 nao esta' todo no hash formal do core selado"''')
a.troca('esp["axiom_report_v408_n"] + KH["delta_vs_v407"]["decl"]', 'esp["axiom_report_v408_n"] + KH["delta_vs_v408"]["decl"]')
a.troca('''sorted(esp["registros_v408"]) == sorted([DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and sorted(esp["registros_v407"])''',
        '''sorted(esp["registros_v409"]) == sorted([DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and sorted(esp["registros_v408"]) == ["cunhagens_v408", "kh_n1_cobertura_v408"] and sorted(esp["registros_v407"])''')
a.troca('''_rf8 = esp["registros_funcao_v409"]["tetelestai_terminal"]
assert _rf8["values"]["n_ancoras_ok"] == _rf8["values"]["n_ancoras"] == len(esp["estrelas_v409"]) == len(DL.ANCORAS) and _rf8["values"]["n_modulos_ok"] == _rf8["values"]["n_modulos"] == DL.N_BUNDLE and _rf8["values"]["n_flags_true"] == _rf8["values"]["n_flags"] == esp["n_bandeiras_novas"] \\
    and _rf8["values"]["escada"] == [CM["escada"][1]] * 3 and _rf8["values"].get("respostas_ok") is True, _rf8["values"]
_rf7 = esp["registros_funcao_v408"]["psion_canto"]   # o psion HERDADO: as 76 estrelas da v408, os 9 modulos, a chave do lema lida do kernel, as cinco chaves iguais as da v408 selada
assert _rf7["values"]["n_ancoras_ok"] == _rf7["values"]["n_ancoras"] == len(esp["estrelas_v408"]) and _rf7["values"]["n_modulos_ok"] == _rf7["values"]["n_modulos"] == len(esp["bundle_v408_sha256"]) and _rf7["values"]["escada"] == [CM["escada"][1]] * 3 and _rf7["values"]["elo_lido_do_kernel"] is True and _feq(_rf7["values"]["chaves"], chaves_v408_esperadas), _rf7["values"]''',
        '''_rf9 = esp["registros_funcao_v409"]["traducao_turing"]
assert _rf9["values"]["n_ancoras_ok"] == _rf9["values"]["n_ancoras"] == len(esp["estrelas_v409"]) == len(DL.ANCORAS) and _rf9["values"]["n_modulos_ok"] == _rf9["values"]["n_modulos"] == DL.N_BUNDLE and _rf9["values"]["n_flags_true"] == _rf9["values"]["n_flags"] == esp["n_bandeiras_novas"] \\
    and _rf9["values"]["escada"] == [CM["escada"][1]] * 3 and _rf9["values"].get("respostas_ok") is True and _rf9["n_checks"] == DL.N_CHECKS_FECHO, _rf9["values"]
_rf8 = esp["registros_funcao_v408"]["tetelestai_terminal"]   # o terminal HERDADO: as 48 estrelas da v408, os 4 modulos
assert _rf8["values"]["n_ancoras_ok"] == _rf8["values"]["n_ancoras"] == len(esp["estrelas_v408"]) and _rf8["values"]["n_modulos_ok"] == _rf8["values"]["n_modulos"] == len(esp["bundle_v408_sha256"]) and _rf8["values"]["escada"] == [CM["escada"][1]] * 3 and _rf8["verdict"] == esp["vereditos_v408"][DL.D8.FECHO_REGISTRO], _rf8["values"]
_rf7 = esp["registros_funcao_v407"]["psion_canto"]   # o psion HERDADO: as 76 estrelas da v407, os 9 modulos, a chave do lema lida do kernel, as chaves iguais as da v408 selada
assert _rf7["values"]["n_ancoras_ok"] == _rf7["values"]["n_ancoras"] == len(esp["estrelas_v407"]) and _rf7["values"]["n_modulos_ok"] == _rf7["values"]["n_modulos"] == len(esp["bundle_v407_sha256"]) and _rf7["values"]["escada"] == [CM["escada"][1]] * 3 and _rf7["values"]["elo_lido_do_kernel"] is True and _feq(_rf7["values"]["chaves"], chaves_v407_esperadas), _rf7["values"]''')
a.troca('''# o selo da v409 difere do da v408 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (psion_canto_v407 e registros_v407), as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita) e as que LEEM a chave nova; o ensaio EXPLICA chave por chave
assert ({"selo_pela_propria_tecnologia_v399", "um_version", "tetelestai_terminal_v408", "registros_v408"}) <= set(esp["selo_difere_do_v408_no_ensaio"])''',
        '''# o selo da v409 difere do da v408 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (traducao_turing_v409 e registros_v409), as chaves que carregam os numeros do kernel ou o hash proprio (a troca dita) e as que LEEM a chave nova; o ensaio EXPLICA chave por chave
assert ({"selo_pela_propria_tecnologia_v399", "um_version", "traducao_turing_v409", "registros_v409"}) <= set(esp["selo_difere_do_v408_no_ensaio"])''')
a.marca("a v409 (A TRADUCAO AS CLASSES DE TURING): o registro novo traducao_turing_v409 (1 modulo, 62 ancoras, 17 checagens); o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados; o esquema de chaves que o pos-rito le; md_traducao lida do candidato")
a.grava()
