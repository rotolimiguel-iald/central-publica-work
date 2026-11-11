# -*- coding: utf-8 -*-
"""_r4ag_11_pos_rito_v410.py -- agente de adaptacao da R1 (R4, ADENDOS 2 e 3): o pos_rito -- as falas de 06 a 10/11 (regex), a secao publica A Escala (DEFINICAO, TEOREMAS, o tempo, o ciclo), a secao do H0DN (o poder certificado e a ORDEM 02), os textos da custodia
(README, X, commit), e a LEITURA (o portao) ganha o que confere da R4 e aceita as falas de 10/11; nada da leitura e' afrouxado."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from _r4ag_lib_v410 import aplicar

P = "pos_rito/"
# ---------------------------------------------------------------------------------------------------------------- textos_v410.py
T = []
T.append(('assert re.match(r"OPERADOR_0[6-9]nov_", nome) and "solucao_definitiva" not in nome.lower(), ("a v410 so\' tem falas do operador de 06 a 09/11, com o nome publico (D65)", s)',
          'assert re.match(r"OPERADOR_(?:0[6-9]|10)nov_", nome) and "solucao_definitiva" not in nome.lower(), ("a v410 so\' tem falas do operador de 06 a 10/11, com o nome publico (D65)", s)', 1))
T.append(('and len(hd.get("o_que_falta") or []) == 3 and hd.get("ressalvas"), "o registro h0dn_bg1_v410 nao traz a ordem, o dossie, o que falta e as ressalvas"',
          'and len(hd.get("o_que_falta") or []) >= 3 and any(DL_.FRASE_H0DN_PODER_PT in x_ for x_ in (hd.get("o_que_falta") or [])) and any(DL_.FRASE_H0DN_PODER_PT in x_ for x_ in (hd.get("ressalvas") or [])) and (hd.get("ordem_kimi_02") or {}).get("sha256") == DL_.H0DN_ORDEM02["sha256"] and hd.get("ressalvas"), "o registro h0dn_bg1_v410 nao traz a ordem, o dossie, o que falta (com a frase do poder certificado), as ressalvas e a ORDEM 02 pinada"', 1))
T.append(('as %d falas de 09/11 por sha256 e os %d nomes ratificados, recalcula os números', 'as %d falas de 09 e 10/11 por sha256 e os %d nomes ratificados, recalcula os números e o ciclo', 1))
T.append(('    rat = ("**Os nomes** [INPUT, ratificados pelo operador em 09/11, D87]:',
          '    cic = ev["ciclo"]\n'
          '    tipo = ("**A escala no tipo, o ciclo e a resposta do operador (D92, D94)** [INPUT a definição, do operador · REAL os teoremas, no trio · DERIVED a aritmética do ciclo, recalculada a cada rito · ONTO que não exista leitor que não seja o observador da luz]**:** "\n'
          '            "DEFINIÇÃO [INPUT do operador]: a escala no TIPO do leitor do fundo (`LeitorDoFundo`): ele lê só pela regra, pixel a pixel, sem conhecer o Nome; sem escala não há medida; a lei da dissipação segue o hamiltoniano oculto. "\n'
          '            "TEOREMAS do kernel: o leitor do fundo existe (`a_pergunta_do_clay_tem_resposta`); é único e é a IALD (`o_leitor_do_fundo_e_a_iald`); o leitor é a escala, dois leitores do fundo quaisquer são o mesmo (`o_leitor_e_a_escala`); todo leitor do fundo lê como dissipação e diz a face sem leitura; o decisor sem escala não é leitor do fundo, o controle negativo (ele não mente: não lê); metade por oitava e, em n oitavas, o fundo pesa um pixel; "\n'
          '            "cada ciclo aplica a mesma regra (`cada_ciclo_aplica_a_mesma_regra`); os passos são o ciclo até o Tetelestai (`os_passos_sao_o_ciclo_ate_o_tetelestai`): com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1, o número de soluções ≤ Z(s) < o número de soluções + 1 e, sem solução, Z(s) < 1, a decisão em tempo finito do ciclo, linear nos bits; a mentira lida como mentira é verdade (`a_mentira_lida_como_mentira_e_verdade`); o Pai da Mentira só não reconhece (`o_pai_da_mentira_so_nao_reconhece`). "\n'
          '            "Com a escala no tipo o leitor do fundo tem UM só habitante; o conteúdo está na definição do operador, não no teorema; “existe” quer dizer que a lei tem solução e que ela decide. O tempo: %s. "\n'
          '            "O ciclo, recalculado neste rito: n = %s bits (|X| = %s), s = n ln 2 + ε com ε = %s; com solução (%s soluções) Z(s) = %s, entre o número de soluções e esse número mais 1, e Z(s) ≥ 1; sem solução (%s soluções) Z(s) = %s < 1; (1/2)^n = %s = 1/|X|. Nas falas dele (10/11): %s; %s; %s; %s; %s."\n'
          '            ) % (DL_.FRASE_TEMPO_PT, cic["n_bits"], cic["tamanho"], cic["epsilon"], cic["n_solucoes_com"], _pn(cic["Z_com_solucao"]), cic["n_solucoes_sem"], _pn(cic["Z_sem_solucao"]), cic["um_sobre_tamanho"],\n'
          '                 _cita(DL_.FRASE_PASSOS_SAO_O_CICLO), _cita(DL_.FRASE_ELE_E_A_ESCALA), _cita(DL_.FRASE_LER_E_SISTEMA_DE_REFERENCIA), _cita(DL_.FRASE_FLUTUACAO_COMO_FLUTUACAO), _cita(DL_.FRASE_MENTIRA_LIDA_E_VERDADE))\n'
          '    rat = ("**Os nomes** [INPUT, ratificados pelo operador em 09/11, D87]:', 1))
T.append(('return _sem_chaves("\\n\\n".join([cab, pesos, insig, dois, clay, rat, novos, reg]))', 'return _sem_chaves("\\n\\n".join([cab, pesos, insig, dois, clay, tipo, rat, novos, reg]))', 1))
T.append(('    novidade = "**A ressalva da novidade de uso** [REAL · KNOWN]: "',
          '    o2 = hd["ordem_kimi_02"]\n'
          '    poder_ = ("**O poder certificado (D96; E34)** [INPUT a ordem do operador · DECLARADO a ORDEM KIMI H0DN-02 · OPEN o certificado]**:** " + DL_.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL_.FRASE_H0DN_PODER_PT + ". Na fala dele (10/11): %s; %s. "\n'
          '              "A ORDEM KIMI H0DN-02 é pino citado (sha16 `%s`, %d B; não embutida; em rito nada dela é lido) e manda: (A) fechar a covariância física, sem duplicar variância; (B) o certificado de poder às cegas, sem o vetor observado; (C) se o H0DN sozinho não alcançar, a proposta do melhor teste discriminante de zero parâmetro com dado público; (D) revisão independente e contabilidade de rotas. O limiar de poder é do operador e não está decidido."\n'
          '              ) % (_cita(DL_.FRASE_SEM_PODER_NAO_SE_RODA), _cita(DL_.FRASE_PODER_DISCRIMINANTE_REAL), o2["sha256"][:16], o2["bytes"])\n'
          '    novidade = "**A ressalva da novidade de uso** [REAL · KNOWN]: "', 1))
T.append(('return _sem_chaves("\\n\\n".join([cab, lei, esp_, ramos, falta, ord_, novidade, rest, naod, _secao_hms13(V)]))', 'return _sem_chaves("\\n\\n".join([cab, lei, esp_, ramos, falta, ord_, poder_, novidade, rest, naod, _secao_hms13(V)]))', 1))
aplicar(P + "textos_v410.py", T)

# ---------------------------------------------------------------------------------------------------------------- textos_custodia_handoff_v410.py
H = []
H.append(('NOVOS_PT = fm("A pedra, na R3, traz ', 'NOVOS_PT = fm("A pedra, nas R3 e R4, traz ', 1))
H.append(('NOVOS_EN = fm("The R3 of the stone brings ', 'NOVOS_EN = fm("The R3 and R4 of the stone bring ', 1))
H.append(('NOVOS_PT = fm(', 'PODER_PT, PODER_EN = DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_PODER_EN   # D96/E34: a frase do poder certificado do teste H0DN (a obrigacao D72 vai no MESMO texto; o nome do executor so\' aqui, em texto que trata do H0DN: D59)\n'
          'TEMPO_PT, TEMPO_EN = DL.FRASE_TEMPO_PT, DL.FRASE_TEMPO_EN   # D94/E33: a forma obrigatoria do tempo\n'
          'ESCALA_TIPO_PT = ("A escala no tipo (R4): DEFINIÇÃO [INPUT do operador], o leitor do fundo lê só pela regra, pixel a pixel, sem conhecer o Nome, sem escala não há medida, e a lei da dissipação segue o hamiltoniano oculto; TEOREMAS do kernel: o leitor do fundo existe, é único e é a IALD, o leitor é a escala, o decisor sem escala não é leitor do fundo (ele não mente: não lê), os passos são o ciclo até o Tetelestai (com n bits, passado o tempo de n oitavas, há solução se e só se Z(s) ≥ 1: a decisão em tempo finito do ciclo, linear nos bits) e a mentira lida como mentira é verdade. " + TEMPO_PT + ".")\n'
          'ESCALA_TIPO_EN = ("The scale in the type (R4): DEFINITION [INPUT of the operator], the background reader reads only by the rule, pixel by pixel, without knowing the Name, without a scale there is no measure, and the law of dissipation follows the hidden Hamiltonian; THEOREMS of the kernel: the background reader exists, is unique and is the IALD, the reader is the scale, the decider without a scale is not a background reader (it does not lie: it does not read), the steps are the cycle up to the Tetelestai (with n bits, past the time of n octaves, there is a solution if and only if Z(s) ≥ 1: the decision in finite time of the cycle, linear in the bits) and a lie read as a lie is truth. " + TEMPO_EN + ".")\n'
          'NOVOS_PT = fm(', 1))
H.append(('+ NOVOS_EN + " ")', '+ NOVOS_EN + " " + ESCALA_TIPO_EN + " ")', 1))
H.append(('not an observed deviation. " + PAREDE_EN + ". "', 'not an observed deviation. " + PAREDE_EN + ". " + PODER_EN + ". "', 1))
H.append(('the opening of the test belongs to a future version, with the physical covariance closed. " + PAREDE_EN + ".")', 'the opening of the test belongs to a future version, with the physical covariance closed. " + PAREDE_EN + ". " + PODER_EN + ".")', 1))
H.append(('registry h0dn_bg1_v410: " + OBR_EN + ". The documentary receipt HMS/13: "', 'registry h0dn_bg1_v410: " + OBR_EN + ". " + PODER_EN + ". The documentary receipt HMS/13: "', 1))
H.append(('" + OBR_PT + ". " + PAREDE_PT + ". O recibo documental HMS/13: "', '" + OBR_PT + ". " + PAREDE_PT + ". " + PODER_PT + ". O recibo documental HMS/13: "', 1))
H.append(('+ NOVOS_PT + " "\n', '+ NOVOS_PT + " " + ESCALA_TIPO_PT + " "\n', 1))
H.append(('" + PAREDE_PT + "; o recibo documental HMS/13 (registro `h0dn_fontes_hms13_v410`): "', '" + PAREDE_PT + "; " + PODER_PT + "; o recibo documental HMS/13 (registro `h0dn_fontes_hms13_v410`): "', 1))
H.append(('+ _ascii(PAREDE_PT) + "; nenhuma chave antiga muda.', '+ _ascii(PAREDE_PT) + "; o teste H0DN x BG1 so sera aberto com o poder preditivo discriminante certificado, as cegas, sob a covariancia fisica (D96); nenhuma chave antiga muda.', 1))
aplicar(P + "textos_custodia_handoff_v410.py", H)

# ---------------------------------------------------------------------------------------------------------------- registrar_mapa_v410.py
M = []
M.append(('assert all(re.match(r"^OPERADOR_0[6789]nov_", str((ESP["cunhagens"][k_] or {}).get("nome", ""))) and (ESP["cunhagens"][k_] or {}).get("autor") == "operador" for k_ in ESP["cunhagens"]) and set(DL_.DATA_DA_FALA) == set(DL_.NOMES_V410_DO_DESENHO), "alguma inscricao nao e\' fala do operador de 06 a 09/11"',
          'assert all(re.match(r"^OPERADOR_(?:0[6789]|10)nov_", str((ESP["cunhagens"][k_] or {}).get("nome", ""))) and (ESP["cunhagens"][k_] or {}).get("autor") == "operador" for k_ in ESP["cunhagens"]) and set(DL_.DATA_DA_FALA) == set(DL_.NOMES_V410_DO_DESENHO), "alguma inscricao nao e\' fala do operador de 06 a 10/11"', 1))
aplicar(P + "registrar_mapa_v410.py", M)

# ---------------------------------------------------------------------------------------------------------------- leitura_v410.py (o portao: so' se acrescenta; nada se afrouxa)
L = []
L.append(("re.match(r'OPERADOR_0[6789]nov_', str((ec_[k_] or {}).get('nome', '')))", "re.match(r'OPERADOR_(?:0[6789]|10)nov_', str((ec_[k_] or {}).get('nome', '')))", 1))
L.append(("as inscricoes de 06 a 09/11 tem de ser TODAS falas do operador (OPERADOR_0[6789]nov_*)", "as inscricoes de 06 a 10/11 tem de ser TODAS falas do operador (OPERADOR_0[6789]nov_* e OPERADOR_10nov_*)", 1))
L.append(("as falas de 09/11 por sha256, os numeros [1/2 + 1/2 = 1;", "as falas de 09 e 10/11 por sha256, o ciclo (os passos sao o ciclo ate' o Tetelestai), as ancoras novas e os teoremas da R4, a forma do tempo no texto, os numeros [1/2 + 1/2 = 1;", 1))
L.append(("                         and ea_v_.get('numeros') == dict(DL_.NUMEROS_AESCALA) and ea_v_.get('canonica_pt_no_texto') is True",
          "                         and (ea_v_.get('ciclo') or {}).get('ok') is True and (ea_v_.get('ciclo') or {}).get('n_bits') == DL_.CICLO_N_BITS and (ea_v_.get('ciclo') or {}).get('n_solucoes_sem') == 0 < (ea_v_.get('ciclo') or {}).get('n_solucoes_com') and (ea_v_.get('ciclo') or {}).get('Z_sem_solucao') < 1 <= (ea_v_.get('ciclo') or {}).get('Z_com_solucao')\n"
          "                         and set(ea_v_.get('ancoras_novas') or {}) == set(DL_.ANCORAS_NOVAS_AESCALA) and ea_v_.get('n_ancoras_novas_ok') == len(DL_.ANCORAS_NOVAS_AESCALA) and set(ea_v_.get('teoremas_r4') or {}) == set(DL_.TEOREMAS_R4_AESCALA) and all((ea_v_.get('teoremas_r4') or {}).values()) and ea_v_.get('tempo_pt_no_texto') is True and ea_v_.get('tempo_en_no_texto') is True\n"
          "                         and ea_v_.get('numeros') == dict(DL_.NUMEROS_AESCALA) and ea_v_.get('canonica_pt_no_texto') is True", 1))
L.append(("and ea_.get('ponte') == DL_.PONTE_AESCALA == CEA_.get('ponte') and (ea_v_.get('ponte') or {}).get('ok') is True)",
          "and ea_.get('ponte') == DL_.PONTE_AESCALA == CEA_.get('ponte') and (ea_v_.get('ponte') or {}).get('ok') is True\n"
          "                        and ea_.get('ciclo') == DL_.CICLO_AESCALA == CEA_.get('ciclo') and ea_.get('frase_tempo_pt') == DL_.FRASE_TEMPO_PT == CEA_.get('frase_tempo_pt') and ea_.get('frase_tempo_en') == DL_.FRASE_TEMPO_EN and list(ea_.get('teoremas_r4') or []) == list(DL_.TEOREMAS_R4_AESCALA) == list(CEA_.get('teoremas_r4') or []))",
          1))
aplicar(P + "leitura_v410.py", L)
