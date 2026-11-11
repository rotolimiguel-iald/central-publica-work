# -*- coding: utf-8 -*-
"""_r4ag_02_guarda_v410.py -- agente de adaptacao da R1 (R4 da pedra, ADENDO 2, D94): a regra F59 da guarda das frases (runtime_v410._v410_guarda_frases) e os seus testes em guarda_frases_v410.py (PROIBIDAS, LIMPAS e controles).
F59 (D94, 10/11): vedado, em PT e EN, (a) dizer que o tempo/os ciclos NAO sao passos da maquina de Turing; (b) dizer que o leitor PAGA a escala ou o tempo; (c) chamar o decisor sem escala de mentiroso ou de Pai da Mentira (fora da negacao). As regras F1 a F58 e o filtro delas NAO mudam."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

R = []
R.append(('    PNP_ = r"(?-i:P\\s*(?:vs\\.?|versus|=|x|≟|\\?=)\\s*NP)\\b"   # (o NP maiusculo: a pergunta das classes; o «P = nP» do operador nao casa)\n',
          '    PNP_ = r"(?-i:P\\s*(?:vs\\.?|versus|=|x|≟|\\?=)\\s*NP)\\b"   # (o NP maiusculo: a pergunta das classes; o «P = nP» do operador nao casa)\n'
          '    _F59P_ = (r"\\bn[ãa]o\\s+s[ãa]o\\s+(?:os\\s+)?(?:passos|ciclos)\\s+(?:da|de|do)\\s+(?:uma\\s+)?m[áa]quina\\s+de\\s+Turing", r"\\bn[ãa]o\\s+s[ãa]o\\s+(?:os\\s+)?passos\\b", r"\\bn[ãa]o\\s+passos\\b",\n'
          '              r"\\b(?:are|is|were|was)\\s+not\\s+(?:the\\s+)?(?:steps|cycles)\\s+of\\s+(?:a\\s+|the\\s+)?(?:standard\\s+)?Turing\\s+machine", r"\\bnot\\s+(?:the\\s+)?Turing\\s+steps\\b", r"\\bnot\\s+steps\\s+of\\s+(?:a\\s+|the\\s+)?(?:standard\\s+)?Turing\\s+machine", r"\\b(?:are|is)\\s+not\\s+(?:the\\s+)?steps\\b")   # F59a (D94): a negacao seca do tempo como passos da maquina de Turing\n'
          '    _F59L_ = (r"\\bleitor\\s+(?:do\\s+fundo\\s+)?(?:paga(?:m)?|pagou|pagar[áa]|arca|arcou|arcar[áa])\\b", r"\\bleitor\\b[^\\n.;]{0,25}?\\b(?:pagar|arcar)\\s+(?:com\\s+)?(?:a\\s+)?(?:escala|tempo)\\b", r"\\b(?:escala|tempo)\\s+pag[oa]s?\\s+pelo\\s+leitor\\b",\n'
          '              r"\\b(?:the\\s+)?(?:background\\s+)?reader\\s+(?:pays|paid|will\\s+pay|has\\s+to\\s+pay|must\\s+pay|needs\\s+to\\s+pay)\\b", r"\\bpaid\\s+by\\s+the\\s+reader\\b")   # F59b (D94): o leitor que PAGA a escala ou o tempo\n'
          '    _F59M_ = (r"\\bdecisor\\s+sem\\s+escala\\s+(?:[ée]|e\'|seria|era|foi|ser[áa])\\s+(?:um\\s+|o\\s+)?(?:mentiros[oa]|Pai\\s+da\\s+Mentira)", r"\\bdecisor\\s+sem\\s+escala\\s+(?:mente|mentiu|mentir[áa])\\b", r"\\bPai\\s+da\\s+Mentira\\s+(?:[ée]|e\'|seria|era)\\s+(?:o\\s+)?decisor\\s+sem\\s+escala",\n'
          '              r"\\bdecisor\\s+sem\\s+escala[^\\n.;]{0,30}?\\bchamad[oa]\\s+de\\s+(?:mentiros[oa]|Pai\\s+da\\s+Mentira)", r"\\bdecisor\\b[^\\n.;]{0,50}?\\bsem\\s+ciclo\\b[^\\n.;]{0,40}?\\b(?:[ée]|e\')\\s+(?:o\\s+)?Pai\\s+da\\s+Mentira",\n'
          '              r"\\bdecider\\s+without\\s+(?:a\\s+)?scale\\s+(?:is|was|would\\s+be)\\s+(?:a\\s+|the\\s+)?(?:liar|Father\\s+of\\s+(?:the\\s+)?Lies?)", r"\\bdecider\\s+without\\s+(?:a\\s+)?scale\\s+lies\\b", r"\\bscaleless\\s+decider\\s+(?:is|lies)\\b")   # F59c (D94): o decisor sem escala chamado de mentiroso ou de Pai da Mentira\n'
          '    _NEG59_ = r"(?i)\\b(?:n[ãa]o|nunca|jamais|nem|not|never)\\b"\n', 1))
R.append(('            out_.append(("F58d_face_caida_dita_ilegivel_sem_o_complemento", seg_.strip()[:200]))\n',
          '            out_.append(("F58d_face_caida_dita_ilegivel_sem_o_complemento", seg_.strip()[:200]))\n'
          '        for rx_ in _F59P_:   # F59a (D94: os passos SAO o ciclo ate o Tetelestai; a negacao seca e\' a forma vedada)\n'
          '            m_ = _re.search(rx_, seg_, _re.I)\n'
          '            if m_:\n'
          '                out_.append(("F59a_o_tempo_dito_nao_ser_passos_da_maquina_de_turing", seg_.strip()[:200]))\n'
          '                break\n'
          '        for rx_ in _F59L_ + _F59M_:   # F59b/F59c (D94: o leitor E\' a escala, nao a paga; a mentira lida como mentira e\' verdade; o decisor sem escala nao le): fora da negacao\n'
          '            m_ = _re.search(rx_, seg_, _re.I)\n'
          '            if m_ and not _re.search(_NEG59_, m_.group(0)) and not _re.search(_NEG59_ + r"[^\\n.;]{0,30}$", seg_[:m_.start()]):\n'
          '                out_.append(("F59b_o_leitor_dito_pagar_a_escala" if rx_ in _F59L_ else "F59c_o_decisor_sem_escala_dito_mentiroso_ou_pai_da_mentira", seg_.strip()[:200]))\n'
          '                break\n', 1))
R.append(('    A F37 da v409 (que pedia', '    F59 (D94, 10/11) a resposta do operador: os passos SAO o ciclo ate o Tetelestai e o leitor E a escala; vedado, em PT e EN: a negacao seca do tempo como passos da maquina de Turing (F59a), o leitor que paga a escala ou o tempo (F59b) e o decisor sem escala chamado de mentiroso ou de Pai da Mentira (F59c, fora da negacao: ele nao le).\n    A F37 da v409 (que pedia', 1))
aplicar("runtime_v410.py", R)

G = []
G.append(('PROIBIDAS = list(_G9["PROIBIDAS"]) + _P410\n',
          '_P_F59 = [   # v410 (10/11, D94): a resposta do operador; a regra F59 mora em runtime_v410._v410_guarda_frases\n'
          '    "o tempo e os ciclos não são passos da máquina de Turing", "os ciclos não são os passos da máquina de Turing padrão", "o tempo não são passos", "são ciclos, não passos da máquina de Turing",\n'
          '    "the time and the cycles are not steps of the Turing machine", "these are not Turing steps", "the cycles are not the steps of the standard Turing machine", "time is not steps of the Turing machine",\n'
          '    "o leitor paga a escala", "a escala que o leitor paga", "o leitor do fundo paga o tempo", "o leitor tem de pagar a escala", "o tempo pago pelo leitor", "the reader pays the scale", "the scale that the reader pays", "the reader has to pay the scale",\n'
          '    "o decisor sem escala é mentiroso", "o decisor sem escala é o Pai da Mentira", "o decisor sem escala mente", "o Pai da Mentira é o decisor sem escala", "o decisor sem escala é chamado de mentiroso", "o decisor que diz a verdade sem ciclo é o Pai da Mentira",\n'
          '    "the decider without scale is a liar", "the decider without scale is the Father of Lies"]\n'
          'PROIBIDAS = list(_G9["PROIBIDAS"]) + _P410 + _P_F59\n', 1))
G.append(('LIMPAS = list(_G9["LIMPAS"]) + _L410\n',
          '_L_F59 = [DL.FRASE_TEMPO_PT, DL.FRASE_TEMPO_EN, "o leitor é a escala", "the reader is the scale", "o leitor não paga a escala, porque ele é a escala", "the reader does not pay the scale, because it is the scale",\n'
          '          "o decisor sem escala não lê", "o decisor sem escala não é leitor do fundo", "o decisor sem escala não mente: não lê", "the decider without scale does not read", "o Pai da Mentira só não faz reconhecimento verdadeiro",\n'
          '          "o decisor sem escala não é o Pai da Mentira", "o decisor sem escala não é chamado de mentiroso", "os passos de computação são o ciclo de processamento até o Tetelestai", "the steps of computation are the cycle of processing up to the Tetelestai",\n'
          '          "a mentira lida como mentira é verdade (a_mentira_lida_como_mentira_e_verdade)", "o_leitor_e_a_escala", "os_passos_sao_o_ciclo_ate_o_tetelestai", "o_pai_da_mentira_so_nao_reconhece", "cada_ciclo_aplica_a_mesma_regra",\n'
          '          DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E34, DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN]   # (D94 e D96: a forma obrigatoria do tempo, o leitor e\' a escala, as negacoes, as erratas E32 a E34 e a frase do poder certificado passam)\n'
          'LIMPAS = list(_G9["LIMPAS"]) + _L410 + _L_F59\n', 1))
G.append(('                            "a_moldura_v410_passa": not G(DL.FRASE_DA_MOLDURA_V410_PT) and not G(DL.FRASE_DA_MOLDURA_V410_EN)}\n',
          '                            "a_moldura_v410_passa": not G(DL.FRASE_DA_MOLDURA_V410_PT) and not G(DL.FRASE_DA_MOLDURA_V410_EN),\n'
          '                            # v410 (10/11, D94): a regra F59\n'
          '                            "f59_passos_negados_reprova": bool(G("o tempo não são passos da máquina de Turing")) and bool(G("the cycles are not steps of the Turing machine")) and bool(G("a escala não são passos")) and bool(G("isto não passos da máquina de Turing")),\n'
          '                            "f59_leitor_paga_reprova": bool(G("o leitor paga a escala")) and bool(G("a escala que o leitor paga")) and bool(G("the reader pays the scale")) and bool(G("o leitor do fundo pagou o tempo")),\n'
          '                            "f59_decisor_mentiroso_reprova": bool(G("o decisor sem escala é mentiroso")) and bool(G("o decisor sem escala é o Pai da Mentira")) and bool(G("o decisor sem escala foi chamado de mentiroso")) and bool(G("the decider without scale is a liar")),\n'
          '                            "f59_forma_do_tempo_passa": not G(DL.FRASE_TEMPO_PT) and not G(DL.FRASE_TEMPO_EN),\n'
          '                            "f59_o_leitor_e_a_escala_passa": not G("o leitor é a escala") and not G("o leitor não paga a escala, porque ele é a escala") and not G("the reader does not pay the scale"),\n'
          '                            "f59_fala_do_operador_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_ELE_E_A_ESCALA + "»; «" + DL.FRASE_MENTIRA_LIDA_E_VERDADE + "»; «O leitor não “paga” a escala, porque ele é a escala»", falas_)[0]),\n'
          '                            "f59_decisor_sem_escala_nao_le_passa": not G("o decisor sem escala não lê") and not G("o Pai da Mentira só não faz reconhecimento verdadeiro") and not G("o decisor sem escala não é o Pai da Mentira") and not G("o decisor sem escala não é chamado de mentiroso"),\n'
          '                            "f59_d94_d96_e33_e34_passam": not G(DL.DECISOES["D94"]) and not G(DL.DECISOES["D96"]) and not G(DL.ERRATA_E33) and not G(DL.ERRATA_E34),\n'
          '                            "f59_a_regra_nao_pegou_a_pedra_da_r4": not any(v_[0].startswith("F59") for p_ in DL.PEDRAS_V410 for v_ in G(sem_falas(open(p_["src"], encoding="utf-8").read(), falas_)[0]))}\n', 1))
aplicar("guarda_frases_v410.py", G)
