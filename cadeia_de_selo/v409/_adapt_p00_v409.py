# -*- coding: utf-8 -*-
"""_adapt_p00_v409.py -- (claude-construtor-v409, 05/11/2026) adapta p00_precondicoes_v409.py (subida mecanica de rotulo da v408) a v409, A TRADUCAO AS CLASSES DE TURING:
1 modulo (TraducaoTuring), 62 ancoras (oito principais), 10 falas de 05/11 (todas do operador; de duas, so' o trecho da D59: o arquivo inteiro NAO e' copiado nem pinado, so' o sha256 dele); os herdados da v408
(tetelestai_terminal_v408 e os specs) entram nas listas dos recriados; o bundle da v407 (9 modulos) entra na conferencia do kernel do Nos; a pedra e' a TraducaoTuring (a copia duravel em v409\\insumos, sha16 da ordem).
Nenhuma checagem relaxada: as igualdades da v408 ficam, com os numeros desta versao lidos do delta; a do autor misto vira a da D59 (o trecho e' o comeco da fonte original, menor que ela, e a fonte inteira so' por sha256)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("p00_precondicoes_v409.py")
a.troca("adaptado em 04/11/2026 a v409 por claude-construtor-v409 (Tetelestai e' o terminal: bundle de 4 modulos em TGLExt/, registro tetelestai_terminal_v408, 41 ancoras, 12 falas de 04/11; nenhuma chave antiga muda).",
        "adaptado em 05/11/2026 a v409 por claude-construtor-v409 (A traducao as classes de Turing: bundle de 1 modulo em TGLExt/, registro traducao_turing_v409, 62 ancoras, 10 falas de 05/11, de duas so' o trecho da D59; nenhuma chave antiga muda).")
a.troca('_chaves_base = sorted(set(esp4["vereditos_v406"]) | set(esp4["vereditos_novos_v408"]))',
        '_chaves_base = sorted(set(esp4["vereditos_v407"]) | set(esp4["vereditos_novos_v408"]))   # (v409) todo registro da v408 selada: os da base de entao (a v407) e os tres novos da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408);')
a.troca("o psion_canto_v407 selado esta' no core\" % len(_chaves_base),", "o psion_canto_v407 e o tetelestai_terminal_v408 selados estao no core\" % len(_chaves_base),")
a.troca('    not any(k.endswith("_v408") for k in core) and all(k in core for k in _chaves_base)', '    not any(k.endswith("_v409") for k in core) and all(k in core for k in _chaves_base)')
a.troca('and (core.get("psion_canto_v407") or {}).get("all_verified") is True, [k for k in core if k.endswith("_v408")])',
        'and (core.get("psion_canto_v407") or {}).get("all_verified") is True and (core.get("tetelestai_terminal_v408") or {}).get("all_verified") is True, [k for k in core if k.endswith("_v409")])')
a.troca("(runtime_v409.py: o registro com FUNCAO tetelestai_terminal_v408, escrito a mao)", "(runtime_v409.py: o registro com FUNCAO traducao_turing_v409, escrito a mao)")
# ---- o bundle
a.troca("# le os 4 modulos do sandbox e CONFERE o sha256 de cada um contra o BUNDLE_v409.json (aborta se difere)", "# le o modulo do sandbox e CONFERE o sha256 contra o BUNDLE_v409.json (aborta se difere)")
a.troca("# a TetelestaiTerminal (a pedra principal): origem == bundle, sha16 == o do recibo dos nomes", "# a TraducaoTuring (a pedra): origem (a copia duravel em v409\\insumos) == bundle, sha16 == o da ordem (o recibo dos nomes e' citado por sha16, nao pinado: D59)")
a.troca("# a fonte de origem (pedras_candidatas_04nov) == a que o preparo pinou", "# a fonte de origem (a copia duravel em v409\\insumos) == a que o preparo pinou")
a.troca('raiz_ok_ = imports_ == ["import " + m_ for m_ in DL.BUNDLE_MODS] and len(imports_) == DL.N_BUNDLE == 4', 'raiz_ok_ = imports_ == ["import " + m_ for m_ in DL.BUNDLE_MODS] and len(imports_) == DL.N_BUNDLE == 1')
a.troca('cond_ = bool(nov_ == list(DL.BUNDLE_RELS) and len(bf_) == DL.N_BUNDLE == 4 and', 'cond_ = bool(nov_ == list(DL.BUNDLE_RELS) and len(bf_) == DL.N_BUNDLE == 1 and')
a.troca('and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 15 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values())', 'and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 10 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values())')
a.troca("a raiz tem exatamente os quatro imports; a TetelestaiTerminal e' a que o recibo dos nomes pinou (sha16); as 12 falas de 04/11 tem os prefixos de sha256 do DESENHO e cada trecho citado e' verbatim (nas duas de autor misto, so' o paragrafo do operador; as falas de 02 e 03/11 ja estao no um.py v408 e nao entram de novo)",
        "a raiz tem exatamente o import; a TraducaoTuring e' a da ordem (sha16); as 10 falas de 05/11 tem os prefixos de sha256 da ordem e cada trecho citado e' verbatim (de duas, so' o trecho da D59; as falas de 04/11 e anteriores ja estao no um.py v408 e nao entram de novo)")
# ---- as ancoras
a.troca('return bool(len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 48 == len(fj_["ancoras"])', 'return bool(len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 62 == len(fj_["ancoras"])')
a.troca('and all(a_ in DL.ANCORAS for a_ in DL.ANCORAS_PRINCIPAIS) and len(DL.ANCORAS_PRINCIPAIS) == DL.N_BUNDLE and', 'and all(a_ in DL.ANCORAS for a_ in DL.ANCORAS_PRINCIPAIS) and len(DL.ANCORAS_PRINCIPAIS) == len(set(DL.ANCORAS_PRINCIPAIS)) >= DL.N_BUNDLE and DL.ANCORAS_PRINCIPAIS[0] == DL.ANCORA_PRINCIPAL and')
a.troca('dep("as 48 ancoras (#print axioms deixados pela autora das provas, lidos das fontes de origem, nunca digitados): DL.ANCORAS == o FLAGS_v409.json == o n_axiomas_das_ancoras do candidato; cada uma num modulo do bundle e so\' no trio; as quatro ancoras principais (tetelestai, o_tempo_e_a_moeda, o_ponto_de_contradicao, p_igual_np) estao entre elas; as bandeiras novas somam n_por_modulo", {}, _ancoras_ok)',
        'dep("as 62 ancoras (#print axioms deixados pela autora das provas, lidos da fonte de origem, nunca digitados): DL.ANCORAS == o FLAGS_v409.json == o n_axiomas_das_ancoras do candidato; cada uma no modulo do bundle e so\' no trio; as oito ancoras principais (p_igual_np_no_modo_selecao, a_traducao, a_trava_no_nome, a_fita_e_o_hamiltoniano_oculto, z_e_o_modo_leitor, a_fita_sem_escala, o_pai_da_mentira, a_identidade_performada) estao entre elas, a primeira e\' a ancora principal; as bandeiras novas somam n_por_modulo", {}, _ancoras_ok)')
a.troca("o gerador achou zero frase proibida no texto novo do candidato e as 4 pedras estao limpas; os registros novos do candidato sao exatamente tetelestai_terminal_v408, cunhagens_v408 e kh_n1_cobertura_v408\"",
        "o gerador achou zero frase proibida no texto novo do candidato e a pedra TraducaoTuring esta' limpa; os registros novos do candidato sao exatamente traducao_turing_v409, cunhagens_v409 e kh_n1_cobertura_v409\"")
a.troca('len(_cong["arquivos"]) == len(CM["cunhagens"]) == DL.N_FALAS_V409 == 15,', 'len(_cong["arquivos"]) == len(CM["cunhagens"]) == DL.N_FALAS_V409 == 10,')
a.troca("a conferencia de citacoes conferiu a docstring das 4 pedras", "a conferencia de citacoes conferiu a docstring da pedra TraducaoTuring")
a.troca("(os 4 modulos novos, raiz, Audit e os demais, byte a byte)", "(o modulo novo, raiz, Audit e os demais, byte a byte)")
a.troca('as pedras da v394 a v408 (os %d modulos da v408 e os %d do fecho da v406 por sha256, as oito da v405, as duas da v404 e as tres da v403 inclusive) estao" % (len(nov), len(esp4["bundle_sha256"]), len(esp4["bundle_v406_sha256"])),',
        'as pedras da v394 a v408 (os %d modulos da v408, os %d do psion da v407 e os %d do fecho da v406 por sha256, as oito da v405, as duas da v404 e as tres da v403 inclusive) estao" % (len(nov), len(esp4["bundle_sha256"]), len(esp4["bundle_v407_sha256"]), len(esp4["bundle_v406_sha256"])),')
a.troca('and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v406_sha256"].items()))',
        'and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v407_sha256"].items()) and all(sha(rd(os.path.join(NK, *rel_.split("/")))) == s_ for rel_, s_ in esp4["bundle_v406_sha256"].items()))')
a.troca("raiz e Audit compilados; os 4 modulos Built e nenhum Replayed)", "raiz e Audit compilados; o modulo Built e nenhum Replayed)")
# ---- as falas (D59)
i0 = a.t.index('_vb12 = DL.verbatins409(os.path.join(HERE, "insumos", "cunhagens")); _n_misto = sum(1 for v_ in _vb12 if "sha256_arquivo_inteiro" in v_)')
i1 = a.t.index('pr = tenta(os.path.join(HERE, "PINO_RECIBO_PRE_SELO_v409.json"))')
a.t = a.t[:i0] + '''_vb12 = DL.verbatins409(os.path.join(HERE, "insumos", "cunhagens")); _n_trecho = sum(1 for v_ in _vb12 if "sha256_arquivo_inteiro" in v_)
chk("as 10 falas de 05/11 (todas do operador; de duas, so' o trecho da D59): a copia duravel de cada texto embutido == sha256 embutido; a fonte original == sha256 do arquivo inteiro; nas duas do trecho, o trecho e' o COMECO da fonte original e menor que ela, e o arquivo inteiro NAO e' copiado em insumos\\\\cunhagens (entra so' por sha256); o manifesto traz exatamente as 10 entradas cunhagens/ e cada uma == o arquivo",
    len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 10 and len(_vb12) == DL.N_FALAS_V409 and _n_trecho == 2
    and all(sha(rd(v_["arquivo"])) == v_["sha256"] and sha(rd(v_["fonte_original"])) == (v_.get("sha256_arquivo_inteiro") or v_["sha256"])
            and (("sha256_arquivo_inteiro" not in v_) or (rd(v_["fonte_original"]).startswith(rd(v_["arquivo"]).rstrip(b"\\r\\n")) and len(rd(v_["arquivo"])) < len(rd(v_["fonte_original"])) and bool(v_.get("so_o_trecho"))
                                                         and not any(sha(rd(p_)) == v_["sha256_arquivo_inteiro"] for p_ in glob.glob(os.path.join(HERE, "insumos", "cunhagens", "*"))))) for v_ in _vb12)
    and all(sha(rd(os.path.join(HERE, "insumos", k))) == v["sha256"] for k, v in MI.items() if k.startswith("cunhagens/")), [len(_vb12), _n_trecho])
''' + a.t[i1:]
# ---- a simulacao da arvore e o exame
a.troca('_HERDADOS_V408 = ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # (os herdados da v408 e da v406, recriados no rito)',
        '_HERDADOS_V408 = ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # (os herdados da v408, da v407 e da v406, recriados no rito)')
a.troca('dep("simular_arvore_do_nos DESTE candidato: o registro com funcao tetelestai_terminal_v408 e os registros por spec v409 (cunhagens_v408, kh_n1_cobertura_v408) selam na arvore simulada do Nos, assim como os herdados da v408 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) e da v406',
        'dep("simular_arvore_do_nos DESTE candidato: o registro com funcao traducao_turing_v409 e os registros por spec v409 (cunhagens_v409, kh_n1_cobertura_v409) selam na arvore simulada do Nos, assim como os herdados da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408), da v407 (psion_canto_v407, cunhagens_v407, kh_n1_cobertura_v407) e da v406')
a.troca('and all(v_.get("all_verified") is True for v_ in pontos_.values() if "all_verified" in v_) and any("tetelestai" in k_ for k_ in pontos_)',
        'and all(v_.get("all_verified") is True for v_ in pontos_.values() if "all_verified" in v_) and any("traducao" in k_ for k_ in pontos_) and any("tetelestai" in k_ for k_ in pontos_)')
a.troca("nenhum ponto de chamada real da falso; o tetelestai_terminal_v408 e' chamado IMEDIATAMENTE depois do bloco da v408 (psion_canto_v407 e os specs da v408) e antes do emit_figures, dentro do bloco executado, e chama os specs da v409;",
        "nenhum ponto de chamada real da falso; o traducao_turing_v409 e' chamado IMEDIATAMENTE depois do tetelestai_terminal_v408 (e dos specs da v408) e antes do emit_figures, dentro do bloco executado, e chama os specs da v409;")
# ---- a pedra
a.troca('dep("a TetelestaiTerminal (a pedra principal: o terminal e\' a leitura): a fonte de origem (pedras_candidatas_04nov) == o pino do bundle (sha256_origem; sha16 == o da ordem);',
        'dep("a TraducaoTuring (a pedra da v409: o dicionario alcanca Turing relativo ao leitor): a fonte de origem (a copia duravel em v409\\\\insumos) == o pino do bundle (sha256_origem; sha16 == o da ordem);')
a.troca('V_ = {"data": "04/11/2026", "s16": CM["sha16"],', 'V_ = {"data": "05/11/2026", "s16": CM["sha16"],')
a.marca("a v409: 1 modulo (TraducaoTuring), 62 ancoras (oito principais), 10 falas (de duas, so' o trecho da D59, a fonte inteira so' por sha256); os herdados da v408 nas listas; o bundle da v407 no kernel do Nos; a data da simulacao do MEMORY.md")
a.grava()
