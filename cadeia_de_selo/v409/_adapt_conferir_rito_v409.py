# -*- coding: utf-8 -*-
"""_adapt_conferir_rito_v409.py -- (claude-construtor-v409, 05/11/2026) adapta conferir_rito_v409.py (subida mecanica de rotulo da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
o registro NOVO com funcao e' traducao_turing_v409 (_traducao_ok: 17 checagens, 62 ancoras, 1 modulo, a ancora principal, nenhuma chave antiga, o acervo da v407 repinado na copia purgada (D57d), as respostas do operador,
a instancia de brinquedo SIM e NAO, o alcance relativo ao leitor); os HERDADOS recriados sao tetelestai_terminal_v408 (_tetelestai408_ok: 16 checagens, 48 ancoras, 4 modulos), psion_canto_v407 (_psion407_ok: 76 ancoras, 9 modulos,
a chave do lema lida do kernel, as chaves iguais as da v408 selada) e fechamento_v406; os registros por spec: RN407/RN408 (recriados) e RN409 (novos); os bundles anteriores (4 da v408, 9 da v407, 301 da v406) seguem como registro;
a secao v409 do artigo antes da secao da v408; a linha do .md «Tradução às classes de Turing (v409)» antes da do terminal (v408), do psion (v407) e do fechamento (v406); NENHUMA chave antiga muda. Nenhuma guarda relaxada:
cada DEVE/NAO da v408 fica, com o nome certo, e os da v409 entram. Corrige tambem um rotulo herdado que afirmava errado (C15: o defeito das guardas estaticas e' o da v399, nao «o que recusou a v408»).
Trocas de contagem EXATA (_adapt_util_v409); backup de bytes; a marca sai."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("conferir_rito_v409.py")
# ---- o docstring inteiro
i0 = a.t.index('"""conferir_rito_v409.py -- confere, DEPOIS do rito v409'); fim = "(padrao: o Nos real, so' leitura).\"\"\""; i1 = a.t.index(fim) + len(fim)
DOC = ('"""conferir_rito_v409.py -- confere, DEPOIS do rito v409, o que tinha de mudar e o que NAO podia (ESPERADOS_v409.json; so leitura do Nos). Molde: conferir_rito_v408.py (a cadeia de CONTEUDO), adaptado em 05/11/2026 por claude-construtor-v409 a v409, A TRADUCAO AS CLASSES DE TURING: o modelo e\' o de BUNDLE PEQUENO (1 modulo novo em TGLExt/: TraducaoTuring).\n'
       'Mudancas ditas: as chaves novas no core (o registro com FUNCAO traducao_turing_v409 e os registros por spec cunhagens_v409 e kh_n1_cobertura_v409) e o resumo delas no selo (traducao_turing_v409 e registros_v409); o selo pela propria tecnologia (v399) muda so\' nos hashes do novo um.py; a versao (um_version v409, sha256);\n'
       'o modulo novo de TGLExt/ no kernel do Nos (sha pinado; os 4 modulos do terminal da v408, os 9 do psion da v407, os 301 do fecho da v406 e as pedras SELADAS das versoes anteriores ficam com o mesmo sha, como registro), a raiz do candidato (mais um import) e o Audit (inalterado); NENHUMA chave antiga muda: a chave do lema\n'
       '(testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) segue LIDA do kernel e le True, com o dict elo_v407 como na v408 selada; as quatro chaves da v406 seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA;\n'
       'os registros herdados tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 sao RECRIADOS e seguem selados (a escada do contrato deles sobe pela C12; cunhagens_v408 ganha a errata E26 ao lado e kh_n1_cobertura_v408 pisos pela C13; cunhagens_v407 ganha a errata da D57(d) ao lado e o acervo da v407 e\' repinado na copia purgada).\n'
       'A TROCA DITA e\' so\' de numeros (a escada e a cobertura crescem com o bundle; o estatuto da prova, que carrega o hash do proprio um.py): NENHUM veredito muda de texto.\n'
       'O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma).\n'
       'NENHUM outro veredito da v408 muda. O GATE NAO SE MOVE: o qg_closure do core e\' IDENTICO ao da v408 (sete checks, a letra do veredito, as 18 bandeiras); a funcao do neutrino NAO e\' reescrita e o numero da massa NAO muda. A MOLDURA: os textos novos nao afirmam demais (as frases proibidas estao fora dos registros novos e da secao nova do artigo; a frase certa, «validade no kernel nao e creditacao; o gate nao se move»,\n'
       'esta nos dois artigos e no .md; onde P = nP e Turing aparecem juntos, o qualificador relativo ao leitor). A secao do selo pela propria tecnologia (v399/v400) e a declaracao do operador continuam: os itens C1 a C16, o round trip e o sidecar um_absoluto_selo_acom.json.\n'
       'uso: python -B -X utf8 conferir_rito_v409.py [sufixo]   (SEM -I: o conferidor importa o um.py instalado, que precisa do numpy do usuario; com -I o import falha e o controle negativo fica vazio, nao vale; o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso; _CONTROLE_NEGATIVO_PRE_RITO e _POSITIVO_FALSO_NOS sao os sufixos da cadeia)\n'
       'Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V409_NOS=<pasta>  (padrao: o Nos real, so\' leitura)."""')
a.t = a.t[:i0] + DOC + a.t[i1:]
a.troca('sys.modules.setdefault("delta_v408", DL)   # quadro_v397.py (copia da v408, nao adaptada nesta pasta) faz `import delta_v408`, que nao existe aqui; delta_v409 traz o mesmo F9_CAMINHOS e o mesmo lido(); defeito apontado no relatorio (quadro_v397.py:12)\n', '')
# ---- os bundles
a.troca('bundle_ok = all(_sha_k(rel) == s for rel, s in ESP["bundle_sha256"].items())   # os 4 modulos do bundle da v409 no kernel do Nos, com o sha do candidato',
        'bundle_ok = all(_sha_k(rel) == s for rel, s in ESP["bundle_sha256"].items())   # o modulo do bundle da v409 (TraducaoTuring) no kernel do Nos, com o sha do candidato')
a.troca('for rel, s in ESP["bundle_v408_sha256"].items()))   # os 9 modulos do bundle da v408 (o psion e o canto) seguem no kernel (e no hash formal do core) com o mesmo sha: registro',
        'for rel, s in ESP["bundle_v408_sha256"].items()))   # os 4 modulos do bundle da v408 (o terminal) seguem no kernel (e no hash formal do core) com o mesmo sha: registro\n'
        'bundle_v407_ok = bool(len(ESP["bundle_v407_sha256"]) > 0 and all(_sha_k(rel) == s and (kf.get("formal_files_sha256") or {}).get(rel) == s for rel, s in ESP["bundle_v407_sha256"].items()))   # os 9 modulos do bundle da v407 (o psion e o canto) seguem no kernel (e no hash formal do core) com o mesmo sha: registro')
a.troca('RN406 = sorted(ESP["registros_v406"]); RN408 = sorted(ESP["registros_v407"]); RN409 = sorted(ESP["registros_v408"])   # (os registros por spec de cada versao: RN406 = os da v406 e RN408 = os da v408, RECRIADOS; RN409 = os desta versao, NOVOS)',
        'RN406 = sorted(ESP["registros_v406"]); RN407 = sorted(ESP["registros_v407"]); RN408 = sorted(ESP["registros_v408"]); RN409 = sorted(ESP["registros_v409"])   # (os registros por spec de cada versao: RN406, RN407 e RN408, RECRIADOS; RN409 = os desta versao, NOVOS)')
a.troca('CG8 = core.get("cunhagens_v408") or {}; KH8 = core.get("kh_n1_cobertura_v408") or {}; TTV = core.get("tetelestai_terminal_v408") or {}',
        'CG8 = core.get("cunhagens_v408") or {}; KH8 = core.get("kh_n1_cobertura_v408") or {}; TTV = core.get("tetelestai_terminal_v408") or {}\n'
        'CG9 = core.get("cunhagens_v409") or {}; KH9 = core.get("kh_n1_cobertura_v409") or {}; TUV = core.get("traducao_turing_v409") or {}')
a.troca('"fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407"]\n_td_txt',
        '"fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408"]\n_td_txt')
# ---- o registro NOVO e os HERDADOS
i0 = a.t.index("def _tetelestai_ok():"); i1 = a.t.index("def _fech408_ok():")
NOVO = '''def _traducao_ok():
    """traducao_turing_v409 (o registro com FUNCAO, novo): veredito == o do ensaio, as checagens do calculo (DL.N_CHECKS_FECHO), os valores == os do ensaio, as 62 ancoras (todas), o modulo do bundle por sha256, a escada exata, beta, a ancora principal, NENHUMA chave antiga,
    o acervo da v407 repinado na copia purgada (D57d), as respostas do operador, a instancia de brinquedo (SIM com solucao, NAO sem), o alcance relativo ao leitor, e nao move o gate"""
    R_ = TUV; E_ = ESP["registros_funcao_v409"]["traducao_turing"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.FECHO_REGISTRO); vv_ = R_.get("values") or {}; ac_ = R_.get("acervo_v407_repinado") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == DL.N_BUNDLE
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v409"]) == len(DL.ANCORAS) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and vv_.get("respostas_ok") is True and ac_.get("sha256") == DL.PURGADO_SHA256 and ac_.get("integra_pinada") is False
                and ((vv_.get("instancia_sim") or {}).get("solucoes") or 0) >= 1 and (vv_.get("instancia_nao") or {}).get("solucoes") == 0 and (R_.get("alcance") or {}).get("frase") == DL.FRASE_D56_PT
                and v_.startswith(DL.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _tetelestai408_ok():
    """tetelestai_terminal_v408 (HERDADO da v408, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v408 selada; as 16 checagens; os valores == os do ensaio; as 48 ancoras e os 4 modulos da v408 por sha256; nenhuma chave antiga; o insumo purgado; nao move o gate"""
    R_ = TTV; E_ = ESP["registros_funcao_v408"]["tetelestai_terminal"]; m_ = R_.get("mechanics") or {}; v_ = V(DL.D8.FECHO_REGISTRO); vv_ = R_.get("values") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v408"][DL.D8.FECHO_REGISTRO] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D8.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == len(ESP["bundle_v408_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v408"]) and all((R_.get("anchors") or {}).values()) and R_.get("ancora_principal") == DL.D8.ANCORA_PRINCIPAL and list(R_.get("ancoras_principais") or []) == list(DL.D8.ANCORAS_PRINCIPAIS)
                and R_.get("chaves_antigas_que_mudam") == [] and R_.get("nome_provisorio") is None and vv_.get("respostas_ok") is True and (vv_.get("insumo_purgado") or {}).get("ok") is True
                and v_.startswith(DL.D8.VEREDITO_OK_PREFIXO) and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: vv_.get(kk_) for kk_ in E_["values"]}, E_["values"]))


def _psion407_ok():
    """psion_canto_v407 (HERDADO da v407 via v408, RECRIADO neste rito com a escada do contrato subida pela C12): segue SELADO; veredito == o da v408 selada; as 16 checagens; os valores == os do ensaio; as 76 ancoras da v407; os 9 modulos por sha256; a chave do lema LIDA do kernel; as chaves iguais as da v408 selada; o teste (d) so' citado; nao move o gate"""
    R_ = PCV; E_ = ESP["registros_funcao_v407"]["psion_canto"]; m_ = R_.get("mechanics") or {}; v_ = V("psion_canto_v407"); td_ = R_.get("teste_d") or {}
    return bool(R_.get("all_verified") is True and v_ == E_["verdict"] == ESP["vereditos_v408"]["psion_canto_v407"] and R_.get("does_not_gate_core") is True and R_.get("runtime_executed") is True and m_.get("passed") is True and m_.get("n_checks") == DL.D7.N_CHECKS_FECHO == E_["n_checks"]
                and all(c_["ok"] for c_ in m_.get("checks") or []) and R_.get("exact_ladder") is True and R_.get("beta_ok") is True and R_.get("embedded_sources_ok") is True and R_.get("embedded_sources_n_ok") == len(ESP["bundle_v407_sha256"])
                and len(R_.get("anchors") or {}) == len(ESP["estrelas_v407"]) and all((R_.get("anchors") or {}).values()) and R_.get("link_read_from_the_kernel") is True and R_.get("lemma") == DL.D7.ANCORA_LEMA and R_.get("pair_theorem") == DL.D7.ANCORA_PAR
                and (R_.get("keys") or {}).get("testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma") is True and _feq(R_.get("keys"), ESP["chaves_v407_esperadas"]) and td_.get("so_citado") is True and td_.get("resultado_no_um_py") is None
                and v_.startswith("TGL_PSION_CANTO_V407__") and v_.endswith("__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED") and not GUARDA.search(v_)
                and _feq({kk_: (R_.get("values") or {}).get(kk_) for kk_ in E_["values"]}, E_["values"]))


'''
a.t = a.t[:i0] + NOVO + a.t[i1:]
a.troca('tetelestai_ok = _tetelestai_ok(); psion408_ok = _psion408_ok(); fech408_ok = _fech408_ok()\n# as 41 ANCORAS das quatro pedras da v409 no kernel do rito (bandeira True, so\' no trio, declaradas no modulo certo)',
        'traducao_ok = _traducao_ok(); tetelestai408_ok = _tetelestai408_ok(); psion407_ok = _psion407_ok(); fech408_ok = _fech408_ok()\n# as 62 ANCORAS da pedra da v409 (TraducaoTuring) no kernel do rito (bandeira True, so\' no trio, declaradas no modulo certo)')
a.troca('# as ANCORAS do psion_canto_v407 (76) e do fechamento_v406 (herdadas): seguem no kernel do rito\nestrela408_ok = len(ESP["estrelas_v408"]) > 0 and all(kf.get(ESP["estrelas_v408"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v408"][n_]["rel"] for n_ in ESP["estrelas_v408"])',
        '# as ANCORAS do tetelestai_terminal_v408 (48), do psion_canto_v407 (76) e do fechamento_v406 (herdadas): seguem no kernel do rito\nestrela408_ok = len(ESP["estrelas_v408"]) > 0 and all(kf.get(ESP["estrelas_v408"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v408"][n_]["rel"] for n_ in ESP["estrelas_v408"])\n'
        'estrela407_ok = len(ESP["estrelas_v407"]) > 0 and all(kf.get(ESP["estrelas_v407"][n_]["bandeira"]) is True and set(axr.get(n_) or []) <= TRIO and n_ in axr and src_.get(n_) == ESP["estrelas_v407"][n_]["rel"] for n_ in ESP["estrelas_v407"])')
a.troca('and _feq(FE.get("four_keys"), ESP["registros_funcao_v406"]["fechamento"]["values"]["chaves"]) and _feq(PCV.get("keys"), ESP["chaves_v408_esperadas"]))',
        'and _feq(FE.get("four_keys"), ESP["registros_funcao_v406"]["fechamento"]["values"]["chaves"]) and _feq(PCV.get("keys"), ESP["chaves_v407_esperadas"]) and TUV.get("chaves_antigas_que_mudam") == [] and TTV.get("chaves_antigas_que_mudam") == [])')
# ---- DEVE: o selo
a.troca('os OITO da v405, fechamento_v406, psion_canto_v407 e tetelestai_terminal_v408), registros_v399, registros_v401, registros_v402, registros_v403, registros_v404, registros_v405, registros_v406, registros_v407 e registros_v408 do selo iguais aos do core',
        'os OITO da v405, fechamento_v406, psion_canto_v407, tetelestai_terminal_v408 e traducao_turing_v409), registros_v399, registros_v401, registros_v402, registros_v403, registros_v404, registros_v405, registros_v406, registros_v407, registros_v408 e registros_v409 do selo iguais aos do core')
a.troca('"fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408"))', '"fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409"))')
a.troca('((selo.get("registros_v407") or {}).get(n) or {}).get("all_verified") is True for n in RN408)\n        and all(((selo.get("registros_v408") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v408") or {}).get(n) or {}).get("all_verified") is True for n in RN409)',
        '((selo.get("registros_v407") or {}).get(n) or {}).get("all_verified") is True for n in RN407)\n        and all(((selo.get("registros_v408") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v408") or {}).get(n) or {}).get("all_verified") is True for n in RN408)\n'
        '        and all(((selo.get("registros_v409") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v409") or {}).get(n) or {}).get("all_verified") is True for n in RN409)')
# ---- DEVE: o registro novo e os herdados
i0 = a.t.index('    "tetelestai_terminal_v408 SELOU (o registro com FUNCAO, novo)'); i1 = a.t.index('    "NENHUMA chave antiga muda na v409:')
a.t = a.t[:i0] + '''    "traducao_turing_v409 SELOU (o registro com FUNCAO, novo): veredito == o do ensaio; as %d checagens do calculo (as %d ancoras da pedra TraducaoTuring no trio e no modulo certo, o modulo embutido por sha256 == o hash formal do rito com a raiz e o import, bits = oitavas, o peso da solucao no uniforme, a trava no Nome, o tempo linear, a norma da trava e Z, a leitura nos pixels, «eu sou» e «o que sou» nas instancias SIM e NAO calculadas, a performance que nao cresce e nao desce abaixo do conteudo, o custo em nats, tempo = moeda, o gate congelado, a escada exata, as guardas limpas, beta = alfa x raiz de e) e os valores == os do ensaio; o alcance relativo ao leitor; o acervo da v407 repinado na copia purgada (D57d); NENHUMA chave antiga muda; nao move o gate" % (DL.N_CHECKS_FECHO, len(DL.ANCORAS)): traducao_ok,
    "as %d ANCORAS da pedra TraducaoTuring (nomes dados pela gerencia e ratificados pelo operador em 05/11) estao no kernel do rito: bandeira True, so' no trio, declaradas no modulo certo" % len(DL.ANCORAS): estrela_ok,
    "tetelestai_terminal_v408 (HERDADO da v408, RECRIADO na v409 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v408 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as 48 ancoras e os 4 modulos da v408 no kernel do rito; nenhuma chave antiga; o insumo purgado; nao move o gate" % DL.D8.N_CHECKS_FECHO: tetelestai408_ok and estrela408_ok,
    "psion_canto_v407 (HERDADO da v407 via v408, RECRIADO na v409 com a escada do contrato subida pela C12) segue SELADO e IGUAL ao da v408 selada em veredito; as %d checagens do calculo e os valores == os do ensaio; as 76 ancoras e os 9 modulos da v407 no kernel do rito; a chave do lema LIDA do kernel e as chaves iguais as da v408 selada; nao move o gate" % DL.D7.N_CHECKS_FECHO: psion407_ok and estrela407_ok,
''' + a.t[a.t.index('    "fechamento_v406 (HERDADO da v406 via v408, RECRIADO na v409)'):]
assert a.t.count('    "NENHUMA chave antiga muda na v409:') == 1
a.troca('full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; o psion_canto_v407 e o fechamento_v406 as leem iguais ao ensaio": chaves_ok,',
        'full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA; o psion_canto_v407 e o fechamento_v406 as leem iguais ao ensaio; o traducao_turing_v409 e o tetelestai_terminal_v408 nao mudam nenhuma": chaves_ok,')
a.troca('''"o bundle da v408 (os %d modulos do psion e do canto em TGLExt/) e o do fecho da v406 (os %d modulos de TGLExt/F1Fecho394) seguem no kernel do Nos e no hash formal do core com o mesmo sha256: a v409 nao reescreve a v408 nem a v406, ficam como registro" % (len(ESP["bundle_v408_sha256"]), len(ESP["bundle_v406_sha256"])): bundle_v408_ok and bundle_v406_ok,''',
        '''"o bundle da v408 (os %d modulos do terminal em TGLExt/), o da v407 (os %d modulos do psion e do canto) e o do fecho da v406 (os %d modulos de TGLExt/F1Fecho394) seguem no kernel do Nos e no hash formal do core com o mesmo sha256: a v409 nao reescreve a v408, a v407 nem a v406, ficam como registro" % (len(ESP["bundle_v408_sha256"]), len(ESP["bundle_v407_sha256"]), len(ESP["bundle_v406_sha256"])): bundle_v408_ok and bundle_v407_ok and bundle_v406_ok,''')
a.troca('C15 [v409, licao da v408] as guardas ESTATICAS da Bancada', 'C15 [desde a v400, licao da v399] as guardas ESTATICAS da Bancada')
a.troca('(o defeito que recusou a v408)', '(o defeito que recusou a v399)', n=2)
# ---- DEVE: os registros por spec
i0 = a.t.index('    "os registros por spec v409 (cunhagens_v408, kh_n1_cobertura_v408) SELARAM'); i1 = a.t.index('        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v407"].items())')
a.t = a.t[:i0] + '''    "os registros por spec v409 (cunhagens_v409, kh_n1_cobertura_v409) SELARAM e cada veredito == o do ensaio; as %d falas de 05/11 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas do operador; de duas, so' o trecho da D59); as erratas E24 a E26 e a dos pisos (em nome proprio da gerencia c1) e as decisoes D55 a D60 estao no registro; os registros por spec da v408 (cunhagens_v408 com a E26 ao lado, kh_n1_cobertura_v408 com pisos pela C13: o veredito nao muda), da v407 (cunhagens_v407 com a E21 e a errata da D57(d) ao lado), da v406, da v405, da v404, da v403, da v402, da v401 e da v399 seguem selados e iguais" % len(ESP["cunhagens"]): all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v409"].items()) and set(ESP["registros_v409"]) == {DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO}
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v408"].items())
''' + a.t[i1:]
a.troca('''        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V409) and all((((CG8.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG8.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())''',
        '''        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V409) and all((((CG9.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG9.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())''')
a.troca('''        and len(CG8.get("erratas") or []) >= len(DL.ERRATAS_V409) and all(str(e_.get("assinatura", "")).startswith("gerencia c1") for e_ in (CG8.get("erratas") or []))
        and set((CG8.get("extras") or {}).get("decisoes") or {}) >= set(ESP["decisoes_v409_ids"]) and KH8.get("all_verified") is True and CG8.get("all_verified") is True
        and KH7.get("all_verified") is True and CG7.get("all_verified") is True and any("E21" in str(e_.get("agora")) for e_ in (CG7.get("erratas") or [])) and KH6.get("all_verified") is True and CG6.get("all_verified") is True''',
        '''        and len(CG9.get("erratas") or []) >= len(DL.ERRATAS_V409) and all(str(e_.get("assinatura", "")).startswith("gerencia c1") for e_ in (CG9.get("erratas") or []))
        and set((CG9.get("extras") or {}).get("decisoes") or {}) >= set(ESP["decisoes_v409_ids"]) and KH9.get("all_verified") is True and CG9.get("all_verified") is True
        and KH8.get("all_verified") is True and CG8.get("all_verified") is True and any("E26" in str(e_.get("agora")) for e_ in (CG8.get("erratas") or []))
        and KH7.get("all_verified") is True and CG7.get("all_verified") is True and any("E21" in str(e_.get("agora")) for e_ in (CG7.get("erratas") or [])) and KH6.get("all_verified") is True and CG6.get("all_verified") is True''')
a.troca('"os %d modulos novos (o bundle da v409 em TGLExt/: TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP) no kernel do Nos com o sha do candidato"',
        '"os %d modulos novos (o bundle da v409 em TGLExt/: TraducaoTuring) no kernel do Nos com o sha do candidato"')
a.troca('"os registros da v408 e as anteriores (psion_canto_v407, cunhagens e kh_n1 da v408; fechamento_v406,',
        '"os registros da v408 e as anteriores (tetelestai_terminal_v408, cunhagens e kh_n1 da v408; psion_canto_v407, cunhagens e kh_n1 da v407; fechamento_v406,')
i0 = a.t.index('    "o artigo PT/EN: a secao v409 (Tetelestai é o terminal:'); i1 = a.t.index('": all(_tt(m) in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l])', i0)
a.t = a.t[:i0] + '''    "o artigo PT/EN: a secao v409 (A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala: a ordem, o que entra, o dicionário de Turing, o modo seleção, a trava no Nome, a fita é o hamiltoniano oculto, Z é o modo leitor, a máquina sem leitor, a identidade performada, o alcance, as erratas ao lado, o que o registro confere), antes da secao da v408 (Tetelestai é o terminal), da v407 (O psíon e o canto: a passagem sob compressão e o par), da v406 (O fechamento: a passagem para o contínuo e o certificado habitado), da v405 (A massa derivada e a identidade definida; A identidade), da v404 (Jo 8,32 e a projecao transversal da Meia-Nat), da v403 (Caminho, Verdade e Vida), da v402 (A ponte da escala dual, a queda sem geometria e a esperanca condicional, com as erratas E1 a E4) e as marcas da v401 (A falsidade (simulacro) da inercia) e anteriores; a v399 (com a errata da v400), a v398, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado)''' + a.t[i1:]
a.troca('"o sumario lista as secoes v409, v408, v404, v403, v402, v401, v399, v398, v397 e v396 e o titulo v384 a v409"', '"o sumario lista as secoes v409, v408, v407, v406, v405, v404, v403, v402, v401, v399, v398, v397 e v396 (as que o ESPERADOS lista) e o titulo v384 a v409"')
a.troca('"o .md canonico: carimbo v409 e as linhas «Tetelestai é o terminal (v409)» (ANTES da linha da v408), «O psíon, o canto e o par (v408)», «O fechamento (v406)»,',
        '"o .md canonico: carimbo v409 e as linhas «Tradução às classes de Turing (v409)» (ANTES da linha da v408), «Tetelestai é o terminal (v408)», «O psíon, o canto e o par (v407)», «O fechamento (v406)»,')
a.troca('and ESP["md_tetelestai"] in fc and ESP["md_psion"] in fc and ESP["md_fechamento"] in fc and fc.find(ESP["md_tetelestai"]) < fc.find(ESP["md_psion"]) < fc.find(ESP["md_fechamento"])',
        'and ESP["md_traducao"] in fc and ESP["md_tetelestai"] in fc and ESP["md_psion"] in fc and ESP["md_fechamento"] in fc and fc.find(ESP["md_traducao"]) < fc.find(ESP["md_tetelestai"]) < fc.find(ESP["md_psion"]) < fc.find(ESP["md_fechamento"])')
a.troca('''"nenhuma chave nova fora da lista da v409 (so' o registro com funcao tetelestai_terminal_v408 e os registros por spec cunhagens_v408 e kh_n1_cobertura_v408; os da v399 a v408, fechamento_v406 e psion_canto_v407 inclusive, sao recriados e iguais)"''',
        '''"nenhuma chave nova fora da lista da v409 (so' o registro com funcao traducao_turing_v409 e os registros por spec cunhagens_v409 e kh_n1_cobertura_v409; os da v399 a v408, fechamento_v406, psion_canto_v407 e tetelestai_terminal_v408 inclusive, sao recriados e iguais)"''')
a.troca('or str(k).endswith("_v407") or str(k).endswith("_v408"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN409),',
        'or str(k).endswith("_v407") or str(k).endswith("_v408") or str(k).endswith("_v409"))) == sorted(list(DL.REGISTROS_FUNCAO) + RN409),')
a.troca('"psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408")) and gate_igual_ok,',
        '"psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")) and gate_igual_ok,')
a.troca('"veredito_tetelestai_terminal": V("tetelestai_terminal_v408"), "veredito_psion_herdado": V("psion_canto_v407"),',
        '"veredito_traducao_turing": V("traducao_turing_v409"), "veredito_tetelestai_terminal": V("tetelestai_terminal_v408"), "veredito_psion_herdado": V("psion_canto_v407"),')
a.marca("a v409 (A TRADUCAO AS CLASSES DE TURING): o registro novo traducao_turing_v409; os herdados tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406; RN407/RN408/RN409; os bundles da v408, v407 e v406 como registro; a linha do .md da traducao antes da do terminal; o rotulo do C15 corrigido (licao da v399)")
a.grava()
