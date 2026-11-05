# -*- coding: utf-8 -*-
"""_adapt_gerar_esperados_v408.py -- adapta gerar_esperados_v408.py (subida mecanica de rotulo da v407) a v408 (04/11/2026, claude-construtor-v408, a servico da gerencia c1):
o registro NOVO com funcao e' tetelestai_terminal_v408 (registros_funcao_v408.tetelestai_terminal; 41 estrelas em estrelas_v408); os HERDADOS recriados sao psion_canto_v407 (registros_funcao_v407.psion_canto, com as cinco chaves que ele le -- chaves_v407_esperadas,
iguais as da v407 selada: nenhuma chave antiga muda) e fechamento_v406 (registros_funcao_v406.fechamento); os registros por spec: registros_v408 (novos), registros_v407 e registros_v406 (recriados); os bundles anteriores ficam como registro (bundle_v407_sha256: 9; bundle_v406_sha256: 301);
as erratas E21 a E23 e as decisoes D48 a D54; a linha do .md «Tetelestai é o terminal (v408, …)» (md_tetelestai) antes da linha da v407 (md_psion) e da v406 (md_fechamento); a troca dita segue so' de numeros, e cinco vereditos NAO mudam (os quatro de antes + psion_canto_v407).
Nenhuma guarda relaxada: toda contagem e todo hash seguem LIDOS dos artefatos; os asserts da v407 ficam, com os nomes certos. Trocas de contagem EXATA; backup de bytes; a marca sai. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_esperados_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


MARCA_RX = re.compile(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n"); assert len(MARCA_RX.findall(t)) == 1; t = MARCA_RX.sub("", t, count=1)
# ---- o docstring inteiro
_i0 = t.index('"""gerar_esperados_v408.py -- ESPERADOS_v408.json LIDOS'); _fim = 'uso: python -I -B -X utf8 gerar_esperados_v408.py"""'; _i1 = t.index(_fim) + len(_fim)
DOC = ('"""gerar_esperados_v408.py -- ESPERADOS_v408.json LIDOS dos artefatos (molde: gerar_esperados_v407.py FINAL, com as licoes da v399 a v407; adaptado em 04/11/2026 a v408, TETELESTAI E\' O TERMINAL: bundle de 4 modulos em TGLExt/ -- TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP --, registro com funcao tetelestai_terminal_v408): o estado SELADO da v407 pinado.\n'
       'A TROCA DITA da v408 e\' SO\' de NUMEROS: (i) os vereditos da v407 que carregam os numeros do kernel (escada, declaracoes, arquivos varridos) e o estatuto da prova (v391), cujo veredito carrega o hash do PROPRIO um.py -- achados por script no ensaio (recomputados; so\' numeros mudam).\n'
       'NAO ha troca dita de TEXTO (o CANDIDATO_v408.json nao declara `troca_dita_v408`) e NENHUMA chave antiga muda: os vereditos de rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406 e psion_canto_v407 NAO mudam; `troca_dita_textual` fica vazio, por asseveracao (se o ensaio medir que algum deles mudou, este script PARA no assert: e\' defeito do candidato ou do contrato, nao se \'conserta\' aqui).\n'
       'Todos os outros vereditos da v407 ficam IGUAIS (os registros das v399 a v407 sao RECRIADOS e iguais ao selado; o fechamento_v406 e o psion_canto_v407 recriados com a escada do contrato subida pela C12, o veredito igual). +3 chaves novas no core (tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408) e +2 chaves no selo (tetelestai_terminal_v408 e registros_v408); o selo pela propria tecnologia (v399) muda so\' nos hashes do novo um.py. O pilar pela mesma chave.\n'
       'O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\\\insumos\\\\fase9) e o conferidor os confere de novo.\n'
       'As CHAVES: nenhuma nova e nenhuma antiga muda (`chaves_v408` vazio); as cinco que o psion_canto_v407 le seguem como na v407 selada (`chaves_v407_esperadas`, lidas do ensaio e asseveradas iguais as de ESPERADOS_v407); full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.\n'
       'O GATE NAO SE MOVE: o qg_closure da v408 e\' IDENTICO ao da v407 (sete checks, a letra do veredito, as 18 bandeiras): o ESPERADOS pina o hash do qg_closure da v407, o hash sem a lista de checks, a propria lista de sete checks e a letra do veredito. A funcao do neutrino NAO e\' reescrita (o angle_status antigo fica):\n'
       'o ESPERADOS pina o frozen_hash da regra de decisao e o veredito do canal; o V1 do ramo B (v386) e o livro da v383 seguem como estavam (o veredito deles e\' o da base).\n'
       'Nada digitado: cada numero e hash vem de CANDIDATO_v408.json, ensaio_a_seco_v408.json, do core/selo da v407 (base_v407), de kernel\\\\FLAGS_v408.json, kernel\\\\KH_N1_v408.json, de ESPERADOS_v407.json (o que o quadro pinou e os registros da v407) e do resultado pinado. As chaves herdadas guardam os nomes da v407:\n'
       '`vereditos_v407`, `flags_true_v407`... sao o estado da BASE; `registros_funcao_v405/v404/v403` e `estrelas_v405/v404/v403` sao os pinos dos registros de pedra das versoes anteriores (RECRIADOS), lidos de ESPERADOS_v407 (onde tem os nomes verdadeiros: as oito pedras sao da v405);\n'
       '`registros_funcao_v406.fechamento` e `estrelas_v406` sao o fechamento_v406 herdado; `registros_funcao_v407.psion_canto` e `estrelas_v407` (as 76 ancoras) sao o psion_canto_v407 herdado (RECRIADOS neste rito); `registros_funcao_v408.tetelestai_terminal` e `estrelas_v408` (as 41 ancoras) sao os desta versao;\n'
       '`bundle_v407_sha256` (os 9 modulos do psion) e `bundle_v406_sha256` (os 301 do fecho) seguem no kernel como registro, e `pedras_v405_sha256` (as TREZE pedras seladas das versoes anteriores).\n'
       'As erratas E21 a E23 e as decisoes D48 a D54 da gerencia vao nos registros (cunhagens_v408); aqui so\' se pinam os vereditos, os valores, as ancoras e os contratos.\n'
       'ORDEM DE USO: depende do ensaio (ensaio_a_seco_v408.json com veredito TUDO PASSOU e o sha16 do candidato): sem ele este script PARA no primeiro assert (fail-closed). uso: python -I -B -X utf8 gerar_esperados_v408.py"""')
t = t[:_i0] + DOC + t[_i1:]
sub('for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406"):   # estes quatro NAO mudam de veredito (a chave nova e\' lida DENTRO deles; o veredito e\' o mesmo)',
    'for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407"):   # estes cinco NAO mudam de veredito (nenhuma chave antiga muda na v408; a escada do contrato do fechamento e do psion sobe pela C12, mas o veredito deles nao carrega numero)')
sub('+ tuple(SEL_STONES405) + ("registros_v405", "fechamento_v406", "registros_v406")', '+ tuple(SEL_STONES405) + ("registros_v405", "fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407")')
sub('selo_chaves_que_mudam = sorted(k for k in SEL_KEYS if k in difere_selo and k not in troca)   # as chaves do selo da v407 que mudam por LEREM a chave nova (o resumo de testemunha_estatica_v396, rede_fock_v394, psibit_v395 e o resumo do fechamento_v406, que traz as chaves): ditas, explicadas pelo ensaio\n'
    'assert set(selo_chaves_que_mudam) <= {"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "registros_v406"}, selo_chaves_que_mudam',
    'selo_chaves_que_mudam = sorted(k for k in SEL_KEYS if k in difere_selo and k not in troca)   # as chaves do selo da v407 que mudam SEM mudar de veredito: so\' os resumos que carregam a escada do contrato (fechamento_v406, psion_canto_v407) ou os pisos/erratas dos specs versionados (registros_v406, registros_v407): ditas, explicadas pelo ensaio (nenhuma chave antiga muda)\n'
    'assert set(selo_chaves_que_mudam) <= {"fechamento_v406", "registros_v406", "psion_canto_v407", "registros_v407"}, selo_chaves_que_mudam')
sub('TV407 = E407["titulo_secao_v407"]   # {pt, en} = «O fechamento: a passagem para o continuo e o certificado habitado» (a secao da v407 vem logo depois da v408)', 'TV407 = E407["titulo_secao_v407"]   # {pt, en} = «O psíon e o canto: a passagem sob compressão e o par» (a secao da v407 vem logo depois da v408)')
# ---- o registro NOVO (tetelestai_terminal_v408) e os HERDADOS (psion_canto_v407 e fechamento_v406)
_j0 = t.index("# ---- o registro NOVO com funcao (psion_canto_v407) e o HERDADO (fechamento_v406, RECRIADO neste rito)")
_jfim = 'assert FE6["all_verified"] is True and FE6["n_checks"] == DL.D6.N_CHECKS_FECHO and FE6["verdict"] == V("fechamento_v406") == MF4.get("fechamento_v406", {"verdict": V("fechamento_v406")})["verdict"], (FE6.get("verdict"), V("fechamento_v406"))\n'
_j1 = t.index(_jfim) + len(_jfim)
BLOCO = ('# ---- o registro NOVO com funcao (tetelestai_terminal_v408) e os HERDADOS (psion_canto_v407 e fechamento_v406, RECRIADOS neste rito)\n'
         'PS = _ens_reg(DL.FECHO_REGISTRO)\n'
         'PC7 = _ens_reg("psion_canto_v407")\n'
         'FE6 = _ens_reg("fechamento_v406")\n'
         'PSV = RG.texto_terminal()["veredito_ok"]\n'
         'assert PS["all_verified"] is True and PS["n_checks"] == DL.N_CHECKS_FECHO and PS["verdict"] == MF4[DL.FECHO_REGISTRO]["verdict"] == PSV and PS["verdict"].startswith(DL.VEREDITO_OK_PREFIXO) and PS["verdict"].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION" + DL.VEREDITO_SUFIXO), (PS.get("verdict"), PS.get("n_checks"))\n'
         'PV = PS["values"]\n'
         'assert PV["n_ancoras_ok"] == PV["n_ancoras"] == len(DL.ANCORAS) and PV["n_modulos_ok"] == PV["n_modulos"] == DL.N_BUNDLE and PV["n_flags_true"] == PV["n_flags"] == CM["n_bandeiras"] and PV["escada"][0] == PV["escada"][1] == PV["escada"][2] == CM["escada"][1] and PV.get("respostas_ok") is True and (PV.get("insumo_purgado") or {}).get("ok") is True, (PV.get("escada"), PV.get("respostas_ok"))\n'
         '# o psion_canto_v407 HERDADO (recriado com a escada do contrato subida pela C12): as cinco chaves que ele le seguem EXATAMENTE como na v407 selada (nenhuma chave antiga muda); o veredito e\' o selado\n'
         'chaves_v407_esperadas = dict(PC7["values"]["chaves"])\n'
         'assert chaves_v407_esperadas["kernel_reads_the_link"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"] is True and chaves_v407_esperadas["rede_fock_v394.whole_certificate_inhabited"] is True \\\n'
         '    and chaves_v407_esperadas["psibit_v395.conditional_psion_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["testemunha_estatica_v396.fock_face.inhabitant_exhibited"] is True and chaves_v407_esperadas["witness_layers.canonical_full_witness_term_constructed"] is True \\\n'
         '    and chaves_v407_esperadas["witness_rigidity.trivial_inhabitant_exists"] is False and chaves_v407_esperadas["qg_closure.gate.full_static_witness_exists"] is False and chaves_v407_esperadas == E407["chaves_v407_esperadas"], chaves_v407_esperadas\n'
         'assert PC7["all_verified"] is True and PC7["n_checks"] == DL.D7.N_CHECKS_FECHO and PC7["verdict"] == V("psion_canto_v407") == MF4.get("psion_canto_v407", {"verdict": V("psion_canto_v407")})["verdict"] and PC7["values"]["elo_lido_do_kernel"] is True and PC7["values"]["escada"] == [CM["escada"][1]] * 3 \\\n'
         '    and PC7["values"]["n_ancoras_ok"] == PC7["values"]["n_ancoras"] == len(E407["estrelas_v407"]) and PC7["values"]["n_modulos_ok"] == PC7["values"]["n_modulos"] == len(E407["bundle_sha256"]), (PC7.get("verdict"), PC7.get("n_checks"))\n'
         + _jfim)
t = t[:_j0] + BLOCO + t[_j1:]
sub('# os dois registros por spec da v407 (cunhagens_v406, kh_n1_cobertura_v406) foram VERSIONADOS pela errata E20 (u7, h2/h3/h6/h8): o veredito NAO muda\nfor n_ in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO):',
    '# os registros por spec da v406 (versionados na v407 pela E20) e da v407 (cunhagens_v407 com a errata E21 ao lado; kh_n1_cobertura_v407 com pisos em h2/h3/h6/h8): RECRIADOS, o veredito NAO muda\nfor n_ in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO, DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO):')
# ---- o dict esp
sub('"bundle_sha256": pins, "bundle_v407_sha256": E407["bundle_sha256"], "formal_files_n": CM["formal_files_n"],', '"bundle_sha256": pins, "bundle_v407_sha256": E407["bundle_sha256"], "bundle_v406_sha256": E407["bundle_v406_sha256"], "formal_files_n": CM["formal_files_n"],')
sub("(`troca_dita_textual` vazio: rede_fock_v394, psibit_v395, testemunha_estatica_v396 e fechamento_v406 nao mudam de veredito, ainda que a chave do lema passe a ser lida do kernel dentro deles); qualquer outra mudanca reprova",
    "(`troca_dita_textual` vazio: rede_fock_v394, psibit_v395, testemunha_estatica_v396, fechamento_v406 e psion_canto_v407 nao mudam de veredito; nenhuma chave antiga muda na v408); qualquer outra mudanca reprova")
sub('       "registros_v407": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},   # os dois por spec desta versao (o de funcao, psion_canto_v407, esta\' em registros_funcao_v408)\n'
    '       "registros_v406": {k: V(k) for k in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO)},   # os dois por spec da v407: RECRIADOS, versionados pela E20, veredito igual ao selado\n',
    '       "registros_v408": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},   # os dois por spec desta versao (o de funcao, tetelestai_terminal_v408, esta\' em registros_funcao_v408)\n'
    '       "registros_v407": {k: V(k) for k in (DL.D7.CUNHAGENS_REGISTRO, DL.D7.KH_REGISTRO)},   # os dois por spec da v407: RECRIADOS (E21 ao lado; pisos no kh), veredito igual ao selado\n'
    '       "registros_v406": {k: V(k) for k in (DL.D6.CUNHAGENS_REGISTRO, DL.D6.KH_REGISTRO)},   # os dois por spec da v406: RECRIADOS (versionados pela E20 na v407), veredito igual ao selado\n')
sub('       "registros_funcao_v408": {"psion_canto": {"nome": DL.FECHO_REGISTRO, "verdict": PS["verdict"], "values": PS["values"], "n_checks": PS["n_checks"]}},\n'
    '       "registros_funcao_v407": {"fechamento": {"nome": DL.D6.FECHO_REGISTRO, "verdict": FE6["verdict"], "values": FE6["values"], "n_checks": FE6["n_checks"], "recriado_com_a_c8_versionada_pela_E20": True}},\n',
    '       "registros_funcao_v408": {"tetelestai_terminal": {"nome": DL.FECHO_REGISTRO, "verdict": PS["verdict"], "values": PS["values"], "n_checks": PS["n_checks"]}},\n'
    '       "registros_funcao_v407": {"psion_canto": {"nome": DL.D7.FECHO_REGISTRO, "verdict": PC7["verdict"], "values": PC7["values"], "n_checks": PC7["n_checks"], "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},\n'
    '       "registros_funcao_v406": {"fechamento": {"nome": DL.D6.FECHO_REGISTRO, "verdict": FE6["verdict"], "values": FE6["values"], "n_checks": FE6["n_checks"], "recriado_com_a_c8_versionada_pela_E20": True, "recriado_com_a_escada_do_contrato_subida_pela_C12": True}},\n')
sub('       "estrelas_v407": E407["estrelas_v407"], "estrelas_v405": E407["estrelas_v405"],', '       "estrelas_v407": E407["estrelas_v407"], "estrelas_v406": E407["estrelas_v406"], "estrelas_v405": E407["estrelas_v405"],')
sub('"decisoes_v408_ids": sorted((k for k in DL.DECISOES if k[1:].isdigit() and int(k[1:]) >= 41), key=lambda k: int(k[1:])), "erratas_E18_E20": list(DL.ERRATAS_V408), "ressalvas": list(DL.RESSALVAS_V408), "leitura_v408": dict(DL.LEITURA_V407),',
    '"decisoes_v408_ids": sorted((k for k in DL.DECISOES if k[1:].isdigit() and int(k[1:]) >= 48), key=lambda k: int(k[1:])), "erratas_E21_E23": list(DL.ERRATAS_V408), "ressalvas": list(DL.RESSALVAS_V408), "leitura_v408": dict(DL.LEITURA_V408),')
sub('       "chaves_v408": [dict(c_) for c_ in DL.CHAVES_V408], "chaves_v406": [dict(c_) for c_ in DL.CHAVES_V407], "chaves_v408_esperadas": chaves_v408_esperadas,',
    '       "chaves_v408": [dict(c_) for c_ in DL.CHAVES_V408], "chaves_v407": [dict(c_) for c_ in DL.CHAVES_V407], "chaves_v407_esperadas": chaves_v407_esperadas,')
sub('"md_testemunha": E407["md_testemunha"], "md_psibit": E407["md_psibit"], "md_fechamento": E407["md_fechamento"],   # (md_fechamento: a linha da v407, que fica logo depois da nova)',
    '"md_testemunha": E407["md_testemunha"], "md_psibit": E407["md_psibit"], "md_fechamento": E407["md_fechamento"], "md_psion": E407["md_psion"],   # (md_psion: a linha da v407, que fica logo depois da nova; md_fechamento: a da v406)')
sub("# a linha do .md da v408 (nova) sai do PROPRIO candidato (nada digitado): «> **O psíon, o canto e o par (v408, DD/MM/AAAA):**» antes da linha da v407", "# a linha do .md da v408 (nova) sai do PROPRIO candidato (nada digitado): «> **Tetelestai é o terminal (v408, DD/MM/AAAA):**» antes da linha da v407")
sub('_mdp = re.findall(r"> \\*\\*(O ps[^*:]*?\\(v408, \\d\\d/\\d\\d/\\d{4}\\)):\\*\\*", _cand_txt)', '_mdp = re.findall(r"> \\*\\*(Tetelestai [^*:]*?\\(v408, \\d\\d/\\d\\d/\\d{4}\\)):\\*\\*", _cand_txt)')
sub('esp["md_psion"] = _mdp[0]', 'esp["md_tetelestai"] = _mdp[0]')
sub('and esp["axiom_report_esperado_min"] == esp["axiom_report_v407_n"] + KH["delta_vs_v406"]["decl"], _cb', 'and esp["axiom_report_esperado_min"] == esp["axiom_report_v407_n"] + KH["delta_vs_v407"]["decl"], _cb')
sub('assert _vn[DL.FECHO_REGISTRO].startswith(PSV) and _vn[DL.FECHO_REGISTRO].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and _vn[DL.CUNHAGENS_REGISTRO].startswith("TGL_CUNHAGENS_V408__") and _vn[DL.KH_REGISTRO].startswith("TGL_KH_N1_COBERTURA_V408__"), _vn',
    'assert _vn[DL.FECHO_REGISTRO] == PSV and _vn[DL.FECHO_REGISTRO].endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and _vn[DL.CUNHAGENS_REGISTRO].startswith("TGL_CUNHAGENS_V408__") and _vn[DL.KH_REGISTRO].startswith("TGL_KH_N1_COBERTURA_V408__"), _vn')
sub('and sorted(esp["registros_v407"]) == sorted([DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and sorted(esp["registros_v406"]) == ["cunhagens_v406", "kh_n1_cobertura_v406"]',
    'and sorted(esp["registros_v408"]) == sorted([DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and sorted(esp["registros_v407"]) == ["cunhagens_v407", "kh_n1_cobertura_v407"] and sorted(esp["registros_v406"]) == ["cunhagens_v406", "kh_n1_cobertura_v406"]')
sub('_rf7 = esp["registros_funcao_v408"]["psion_canto"]\n'
    'assert _rf7["values"]["n_ancoras_ok"] == _rf7["values"]["n_ancoras"] == len(esp["estrelas_v408"]) == len(DL.ANCORAS) and _rf7["values"]["n_modulos_ok"] == _rf7["values"]["n_modulos"] == DL.N_BUNDLE and _rf7["values"]["n_flags_true"] == _rf7["values"]["n_flags"] == esp["n_bandeiras_novas"] \\\n'
    '    and _rf7["values"]["escada"] == [CM["escada"][1]] * 3 and _rf7["values"]["elo_lido_do_kernel"] is True and _feq(_rf7["values"]["chaves"], chaves_v408_esperadas), _rf7["values"]\n',
    '_rf8 = esp["registros_funcao_v408"]["tetelestai_terminal"]\n'
    'assert _rf8["values"]["n_ancoras_ok"] == _rf8["values"]["n_ancoras"] == len(esp["estrelas_v408"]) == len(DL.ANCORAS) and _rf8["values"]["n_modulos_ok"] == _rf8["values"]["n_modulos"] == DL.N_BUNDLE and _rf8["values"]["n_flags_true"] == _rf8["values"]["n_flags"] == esp["n_bandeiras_novas"] \\\n'
    '    and _rf8["values"]["escada"] == [CM["escada"][1]] * 3 and _rf8["values"].get("respostas_ok") is True, _rf8["values"]\n'
    '_rf7 = esp["registros_funcao_v407"]["psion_canto"]   # o psion HERDADO: as 76 estrelas da v407, os 9 modulos, a chave do lema lida do kernel, as cinco chaves iguais as da v407 selada\n'
    'assert _rf7["values"]["n_ancoras_ok"] == _rf7["values"]["n_ancoras"] == len(esp["estrelas_v407"]) and _rf7["values"]["n_modulos_ok"] == _rf7["values"]["n_modulos"] == len(esp["bundle_v407_sha256"]) and _rf7["values"]["escada"] == [CM["escada"][1]] * 3 and _rf7["values"]["elo_lido_do_kernel"] is True and _feq(_rf7["values"]["chaves"], chaves_v407_esperadas), _rf7["values"]\n')
sub('assert ({"selo_pela_propria_tecnologia_v399", "um_version", "psion_canto_v407", "registros_v407"}) <= set(esp["selo_difere_do_v407_no_ensaio"])', 'assert ({"selo_pela_propria_tecnologia_v399", "um_version", "tetelestai_terminal_v408", "registros_v408"}) <= set(esp["selo_difere_do_v407_no_ensaio"])')
assert "chaves_v408_esperadas" not in t and 'esp["md_psion"]' not in t, "sobrou nome velho"
assert not any(l_.startswith("# [A ADAPTAR v408]") for l_ in t.split("\n"))
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok gerar_esperados", len(raw), "->", len(t.encode("utf-8")))
