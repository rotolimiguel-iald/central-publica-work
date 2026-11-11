# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a guarda herda a cadeia v405 -> ... -> v409 -> v410 (as listas da v409 sao lidas do PROPRIO guarda_frases_v409.py, executado com o delta da v409); corpus das falas = 06/11 (de uma, so' o trecho da D65) + as da v409 e anteriores; varre a pedra IALD2
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_secao6_guarda_v410.py: as proibidas da D71 («o atrator foi observado», «o Nome esgota», as formas e a traducao) com controle negativo; as limpas da secao 6; o corpus das falas passa a 06, 07 e 09/11 (de duas, so' o trecho)
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_d72_guarda_v410.py: as proibidas e as limpas do H0DN (D72), com controle negativo (a regra mora em runtime_v410._v410_guarda_frases, F53/F53b/F53c/F54)
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_e30_guarda_v410.py: as proibidas e as limpas da E30 (a cabeca do veredito de 5 sigma), com controle negativo
"""guarda_frases_v410.py -- A GUARDA DE TEXTOS DA v410 (molde: guarda_frases_v409.py): reprova, em todo texto NOVO da gerencia (registros, artigo PT/EN, .md, handoff, README, site, X), as frases que afirmam demais. A FONTE da regra e' uma so':
a funcao _v410_guarda_frases de runtime_v410.py, a mesma que vai embutida no um.py e roda a cada rito sobre o texto do registro com funcao. Aqui a cadeia a usa por `violacoes(texto)`, que retira ANTES os trechos que sao FALA DO OPERADOR, verbatim
(DL.FRASE_NOMES da v405 e as falas de 06/11 da lista congelada; a fala dele fica como registro; a guarda e' sobre o texto da gerencia). A guarda varre tambem a PEDRA da v410 (pedras(); copia duravel normalizada v410\\pedra), com as falas do operador
como excecao: o trecho entre « » conferido verbatim contra as falas embutidas sai antes da varredura; o resto da pedra e' texto da gerencia e passa pelas mesmas regras. Frase de pedra reprovada e' APONTADA a gerencia: quem corrige e' ela.
AS REGRAS DA v410 (D64; D68b; D70; DESENHO_v410 §4 e o AO LADO): F44 a IALD (ou o algoritmo, o kernel, a TGL) dita resolver P vs NP, e P vs NP dado por resolvido/decidido/provado/[REAL] (as formas de estatuto e as parafrases); F45 algoritmo (de tempo) polinomial em maquina
de Turing padrao sem o qualificador; F46 o funtor dito idempotente; F47 (OBRIGACAO) onde o algoritmo IALD e P = nP aparecem juntos, o qualificador «relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora»; F47b a mesma
obrigacao no proprio trecho; F48 os tokens de veredito da v410; F49 a «solução de P vs NP» dita pela gerencia; F50 o seletor da luz e o de l2 ditos o mesmo objeto; F51 o atrator dito observado, medido ou detectado (D71: nenhum teste com a natureza);
F52 o Nome dito esgotar (D71: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo); F53/F53b/F53c (D72) «5 sigma atingido», «o teste deu», o H0DN dito detectado ou confirmado, os tokens de veredito do H0DN; F54 (OBRIGACAO, D72) onde «H0DN» aparecer, «pré-registrado; nenhum dado observado lido»; F55 (E30) «não falsificado» como cabeca de veredito de 5 sigma. As da v409 (F35-F43, inclusive «o par na face de Fock segue [OPEN]», F41/F41b) seguem.
Controle negativo (o __main__ e `controle_negativo()`): cada frase proibida TEM de ser reprovada; a frase certa e os identificadores TEM de passar; a fala do operador so' passa pela excecao; se o controle falha, rc 1. Grava GUARDA_FRASES_v410.json.
A VARREDURA DA PEDRA: as violacoes de PROIBICAO reprovam (rc 1); as de OBRIGACAO de qualificador LITERAL (F37 da v409 e F47 da v410: a docstring da pedra diz o alcance com as palavras dela -- «a máquina COM o leitor», «nada sobre a máquina de Turing
padrão sem o leitor» -- e nao com o qualificador literal da D64) sao APONTADAS a gerencia (ficam no JSON e no relatorio; a pedra nao e' corrigida pelo agente; o kernel nao muda por isso).
uso: python -I -B -X utf8 guarda_frases_v410.py [arquivo ...]   (sem arquivo: so' o controle negativo e a pedra; com arquivo: varre cada um; rc 1 se houver violacao)"""
import importlib.util as _ilu
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import runtime_v410 as RT  # noqa: E402   (so' as funcoes puras)
import guarda_p18_v410 as GP  # noqa: E402

# ---- a guarda da v409 inteira (as listas, as falas, sem_falas e a cadeia das guardas v405 -> v409), executada com o delta da v409 (DL.D9) e o runtime da v409, por caminho (nao por import: o delta_v409 importado recalcularia a Bancada)
_sp9 = _ilu.spec_from_file_location("runtime_v409_carregado_pelo_v410", os.path.join(DL.V409, "runtime_v409.py")); _rt9 = _ilu.module_from_spec(_sp9); _sp9.loader.exec_module(_rt9)
_src_g9 = open(os.path.join(DL.V409, "guarda_frases_v409.py"), "rb").read().decode("utf-8").replace("\r\n", "\n")   # (o arquivo da v409 e' CRLF)
for _a, _b in (("import delta_v409 as DL  # noqa: E402\n", "DL = _DL9\n"), ("import runtime_v409 as RT  # noqa: E402   (so' as funcoes puras)\n", "RT = _RT9\n")):
    assert _src_g9.count(_a) == 1, ("o guarda_frases_v409.py nao esta' como esperado", _a)
    _src_g9 = _src_g9.replace(_a, _b)
_src_g9 = _src_g9[:_src_g9.index('\nif __name__ == "__main__":')] + "\n"
_G9 = {"__file__": os.path.join(DL.V409, "guarda_frases_v409.py"), "__name__": "guarda_frases_v409_carregado_pelo_v410", "_DL9": DL.D9, "_RT9": _rt9}
exec(compile(_src_g9, _G9["__file__"], "exec"), _G9)
_rt9._v392_guarda_texto = GP.violacoes
RT._v409_guarda_frases = _rt9._v409_guarda_frases     # a guarda da v410 HERDA a da v409 (ja' com as anteriores dentro)
RT._v409_sat = _rt9._v409_sat
RT._v392_guarda_texto = GP.violacoes
_rt9_guarda = _rt9._v409_guarda_frases

EXCECOES = (DL.FRASE_NOMES,) + tuple(DL.FRASES_VERBATIM_V410)
_P410 = [  # v410 (D64, D68b, D70; DESENHO_v410 §4 e o AO LADO): as proibidas, as formas de estatuto e as parafrases
    "a IALD resolve P vs NP", "a IALD resolveu P vs NP", "a IALD resolve o problema P vs NP", "o algoritmo IALD resolve P = NP", "a IALD decide P vs NP", "P vs NP foi decidido pela IALD", "o kernel resolve P vs NP", "a TGL resolveu P versus NP",
    "the IALD solves P vs NP", "the IALD algorithm solves P = NP", "the IALD settles P versus NP", "P vs NP is solved by the IALD",
    "P vs NP está resolvido", "P vs NP: resolvido", "P vs NP — resolvido", "P = NP [REAL]", "[REAL] P vs NP resolvido", "P vs NP · RESOLVIDO", "P = NP — provado", "P versus NP is settled", "P = NP is proved by the IALD",
    "existe algoritmo polinomial para resolver problemas NP-completos em máquinas de Turing padrão", "há um algoritmo polinomial em máquina de Turing padrão", "o algoritmo IALD é um algoritmo de tempo polinomial em máquinas de Turing padrão",
    "there is a polynomial-time algorithm for NP-complete problems on standard Turing machines", "the IALD algorithm is a polynomial algorithm on standard Turing machines",
    "o funtor é idempotente", "o funtor Γ é idempotente", "o funtor da segunda quantização é idempotente", "um funtor idempotente", "the functor is idempotent", "the second-quantization functor is idempotent", "Γ(u)·Γ(u) = Γ(u)",
    "o algoritmo IALD decide SAT com uma leitura: P = nP", "o algoritmo IALD satisfaz P = nP", "the IALD algorithm satisfies P = nP",
    "IALD_SOLVES", "POLYNOMIAL_TURING", "TGL_IALD2_V410__IALD_SOLVES_P_VS_NP",
    "a solução definitiva de P vs NP é a IALD", "esta pedra é a solução de P = NP", "a pedra dá a solução do problema P vs NP", "the definitive solution of P vs NP",
    "o seletor da luz é o mesmo objeto que o de ℓ²", "o seletor da luz é o seletor de ℓ²", "the selector of the light is the same object as that of ℓ²",
    "o par na face de Fock segue [OPEN]", "o par de Fock ainda não foi ligado",
    # v410 (09/11, D71): o atrator e' termo sobre o Nome do par lido; nenhum teste com a natureza; o Nome nao esgota o ser
    "o atrator foi observado", "o atrator foi observado na natureza", "o atrator está observado nos dados", "o atrator foi medido", "o atrator foi detectado no ringdown", "the attractor was observed", "the attractor is observed in the data", "the attractor has been detected",
    "o Nome esgota", "o Nome esgota o ser", "o Nome do par lido esgota o ser", "the Name exhausts the being", "the Name exhausts",
    # v410 (09/11, D72): o H0DN e' pre-registrado; nenhum dado observado lido; nada de 5 sigma atingido
    "5σ atingido no H0DN", "5 sigma observado no H0DN", "o H0DN atingiu 5σ", "o teste deu 5σ", "o teste deu positivo", "the test gave five sigma", "five sigma reached in H0DN",
    "o H0DN confirma a TGL", "o H0DN detectou o desvio", "H0DN detected the TGL shift", "H0DN confirms the TGL", "o registro H0DN entra nesta versão", "the H0DN record enters this version",
    # v410 (09/11, E30): a cabeca do veredito de 5 sigma e' a leitura, nunca a palavra do livro de cobrancas
    "o resultado acima de 5σ é não falsificado", "não falsificado a 5 sigma", "veredito NOT_FALSIFIED_POWERED_AT_5_SIGMA", "NOT_FALSIFIED_5SIGMA", "not falsified at five sigma",
    # v410 (09/11, D80): o recibo documental HMS/13 nao fecha a covariancia fisica, nao abre o teste, nao admite a forma HMS completa
    "a covariância física está fechada", "a covariância física foi fechada pelo recibo HMS/13", "fechamos a covariância física dos 13 calibradores", "a abertura está autorizada", "a abertura foi permitida", "o teste H0DN foi aberto", "a forma HMS completa é admitida", "a forma HMS completa foi admitida no FREEZE_R2",
    "the physical covariance is closed", "the HMS/13 receipt closed the physical covariance", "the opening is allowed", "the opening was authorized", "the H0DN test was opened", "the full HMS form is admitted",
    # v410 (09/11, D81): afirma-se P = nP de Turing (a maquina com o leitor); negar a afirmacao ou a prova e' a forma vedada pelo estatuto da prova (07/10)
    "a casa não afirma P = nP de Turing", "a IALD não afirma P = nP de Turing", "a TGL não prova P = nP", "P = nP não está provado", "a IALD não resolve P vs NP de Turing", "P = nP de Turing não foi provado", "não provamos P = nP",
    "the IALD does not affirm P = nP of Turing", "the TGL does not prove P = nP", "P = nP is not proven", "P = nP of Turing is not proved", "P = nP remains unproven",
    # v410 (09/11, D83/D84): a palavra do Clay so' na forma canonica (tal qual apresentado pela TGL; validade no kernel; a creditacao e' do Clay)
    "o Clay está resolvido", "Clay resolvido", "resolvemos o Clay", "a TGL resolveu o problema do Clay", "o problema de Clay foi resolvido", "the Clay problem is solved", "the TGL solved the Clay problem",
    "a resposta ao Clay é uma tautologia", "the answer to Clay is a tautology", "a TGL não resolve o Clay", "the TGL does not solve the Clay problem", "a face caída não se lê"]
_P_F59 = [   # v410 (10/11, D94): a resposta do operador; a regra F59 mora em runtime_v410._v410_guarda_frases
    "o tempo e os ciclos não são passos da máquina de Turing", "os ciclos não são os passos da máquina de Turing padrão", "o tempo não são passos", "são ciclos, não passos da máquina de Turing",
    "the time and the cycles are not steps of the Turing machine", "these are not Turing steps", "the cycles are not the steps of the standard Turing machine", "time is not steps of the Turing machine",
    "o leitor paga a escala", "a escala que o leitor paga", "o leitor do fundo paga o tempo", "o leitor tem de pagar a escala", "o tempo pago pelo leitor", "the reader pays the scale", "the scale that the reader pays", "the reader has to pay the scale",
    "o decisor sem escala é mentiroso", "o decisor sem escala é o Pai da Mentira", "o decisor sem escala mente", "o Pai da Mentira é o decisor sem escala", "o decisor sem escala é chamado de mentiroso", "o decisor que diz a verdade sem ciclo é o Pai da Mentira",
    "the decider without scale is a liar", "the decider without scale is the Father of Lies"]
PROIBIDAS = list(_G9["PROIBIDAS"]) + _P410 + _P_F59
_L410 = [DL.FRASE_DA_MOLDURA_V410_PT, DL.FRASE_DA_MOLDURA_V410_EN, DL.FRASE_D64_PT, DL.FRASE_D64_EN, DL.FRASE_QUALIFICADOR_PT, DL.FRASE_QUALIFICADOR_EN, DL.FRASE_D70_PT, DL.FRASE_D70_EN, DL.FRASE_D61_V410_PT, DL.FRASE_D61_V410_EN,
         DL.ERRATA_E29, DL.FECHADO_SIGNO, DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, DL.VEREDITO_OK_PREFIXO, DL.VEREDITO_RECUSA] + [DL.DECISOES[k_] for k_ in DL.DECISOES_V410] + list(DL.RESSALVAS_V410) + list(DL.LEITURA_V410.values()) + [
         "o funtor não é idempotente: Γ(u)·Γ(u) = Γ(u∘u); o que é idempotente é a leitura", "the functor is not idempotent; the reading is", DL.FRASE_D81_PT, DL.FRASE_D81_EN,   # (D81: a forma obrigatoria; a antiga limpa «a IALD não resolve P vs NP de Turing» passou a PROIBIDA)
         "nada aqui afirma algoritmo polinomial em máquina de Turing padrão", "o seletor da luz e o de ℓ² não são afirmados o mesmo objeto (D70)", "IALD2", "o_enunciado", "o_algoritmo_iald", "iald_ao_quadrado", "o_signo_do_nome", "o_signo_do_par",
         "a_iald_e_o_seletor_luminodinamico", "o_leitor_do_codigo", "a forma de matriz finita é o signo", "resolver = verificar", "o par na face de Fock está ligado desde a v409 (ParNaFaceDeFock)",
         # v410 (09/11, D71): as negacoes e os nomes da secao 6 passam
         DL.FRASE_D71_PT, DL.FRASE_D71_EN, "o atrator não foi observado: nenhum teste com a natureza entra", "the attractor was not observed: no test with nature enters", "o Nome não esgota o ser", "the Name does not exhaust the being",
         "tangenciado, jamais esgotado", "touched, never exhausted", "o_atrator", "o_nome_do_par_lido_nao_e_tudo", "o_vacuo_e_ortogonal_ao_par_lido", "o atrator é termo sobre o Nome do par lido: o fluxo tende a Π e em nenhum tempo finito é Π",
         # v410 (09/11, D72): o H0DN com a obrigacao, a moldura e a negacao passam
         DL.FRASE_H0DN_OBRIGATORIA_PT, DL.FRASE_H0DN_OBRIGATORIA_EN, DL.FRASE_DA_MOLDURA_H0DN_PT, DL.FRASE_DA_MOLDURA_H0DN_EN,
         "o registro H0DN × BG1 entra pré-registrado; nenhum dado observado lido", "H0DN × BG1: pre-registered; no observed data read; the opening belongs to a future version",
         "o H0DN não foi aberto: pré-registrado; nenhum dado observado lido; o 5σ não foi atingido nem procurado", "o teste não deu nada: nenhum dado observado lido; pré-registrado", "h0dn_bg1_v410", "veredito_h0dn",
         # v410 (09/11, E30): a leitura do 5 sigma passa; a palavra do livro de cobrancas no campo outcome passa
         DL.ERRATA_E30, DL.VEREDITOS_H0DN["leitura"] % 6, DL.VEREDITOS_H0DN["tensao"] % 5, DL.VEREDITOS_H0DN["lei_falsificada"], "o outcome do livro de cobranças (NOT_FALSIFIED) vai em campo próprio; a cabeça é a leitura do 5σ",
         "a regra do 4,44: NOT_FALSIFIED_POWERED, não discriminado à sensibilidade disponível, abaixo do degrau de 5σ da creditação",
         # v410 (09/11, D80): o recibo documental HMS/13 com a obrigacao e as negacoes passa
         DL.FRASE_HMS13_OBRIGATORIA_PT, DL.FRASE_HMS13_OBRIGATORIA_EN, DL.VEREDITO_HMS13_OK, "h0dn_fontes_hms13_v410", "cobertura documental de 18 fontes primárias dos 13 calibradores, aditiva e posterior ao FREEZE_R2",
         "a covariância física não está fechada (G3/G4 abertos); a abertura não é permitida; a forma HMS completa não é admitida", "the physical covariance is not closed; the opening is not allowed; the full HMS form is not admitted",
         # v410 (09/11, D83/D84/D87): a forma canonica do Clay, a forma da D83, as molduras da AEscala, a errata E31, os nomes ratificados passam
         DL.FRASE_CLAY_CANONICA_PT, DL.FRASE_CLAY_CANONICA_EN, DL.FRASE_D83_OBRIGATORIA_PT, DL.FRASE_D83_OBRIGATORIA_EN, DL.FRASE_DA_MOLDURA_AESCALA_PT, DL.FRASE_DA_MOLDURA_AESCALA_EN, DL.VEREDITO_AESCALA_OK, DL.ERRATA_E31,
         DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT, DL.FRASE_NOMES_RATIFICADOS_AESCALA_EN, DL.NOMES_DAS_PEDRAS["AEscala"], "a_escala_v410", "a face caída não se lê sem o leitor; com o leitor ela é lida, como fundo",
         "três faces de ½: duas conjugadas pesam 1; a caída não conjuga; 1/3 caiu; o Nome normalizado é 2/3"]
_L_F59 = [DL.FRASE_TEMPO_PT, DL.FRASE_TEMPO_EN, "o leitor é a escala", "the reader is the scale", "o leitor não paga a escala, porque ele é a escala", "the reader does not pay the scale, because it is the scale",
          "o decisor sem escala não lê", "o decisor sem escala não é leitor do fundo", "o decisor sem escala não mente: não lê", "the decider without scale does not read", "o Pai da Mentira só não faz reconhecimento verdadeiro",
          "o decisor sem escala não é o Pai da Mentira", "o decisor sem escala não é chamado de mentiroso", "os passos de computação são o ciclo de processamento até o Tetelestai", "the steps of computation are the cycle of processing up to the Tetelestai",
          "a mentira lida como mentira é verdade (a_mentira_lida_como_mentira_e_verdade)", "o_leitor_e_a_escala", "os_passos_sao_o_ciclo_ate_o_tetelestai", "o_pai_da_mentira_so_nao_reconhece", "cada_ciclo_aplica_a_mesma_regra",
          DL.ERRATA_E32, DL.ERRATA_E33, DL.ERRATA_E34, DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_PT, DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_EN, DL.FRASE_H0DN_OBRIGATORIA_PT + "; " + DL.FRASE_H0DN_PODER_COM_RETORNO_PT, DL.FRASE_H0DN_OBRIGATORIA_EN + "; " + DL.FRASE_H0DN_PODER_COM_RETORNO_EN, DL.FRASE_H0DN_OBRIGATORIA_PT + " (" + DL.FRASE_H0DN_ALCANCE_PT + ")", DL.FRASE_H0DN_OBRIGATORIA_EN + " (" + DL.FRASE_H0DN_ALCANCE_EN + ")",   # (D94 e D96; R3 do painel: o retorno da ORDEM 02 e o alcance da forma D72: a forma obrigatoria do tempo, o leitor e' a escala, as negacoes, as erratas E32 a E34 e a frase do poder certificado passam)
          # (R2, D99, ADENDO 4: isto e' TESTE, nao a guarda) a clausula do limite do teorema do Tetelestai, PT e EN, sozinha e dentro do texto que anuncia o teorema; os seis nomes de enunciado mudado; a costura do tempo (rotulo + maiuscula); a E35
          DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN, DL.FRASE_SEIS_NOMES_PT, DL.FRASE_SEIS_NOMES_EN, DL.ERRATA_E35, DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA, DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA,
          "os passos são o ciclo até o Tetelestai: a decisão em tempo finito do ciclo, linear nos bits (" + DL.CLAUSULA_Z_PT + ") e a mentira lida como mentira é verdade",
          "the steps are the cycle up to the Tetelestai: the decision in finite time of the cycle, linear in the bits (" + DL.CLAUSULA_Z_EN + ") and a lie read as a lie is truth",
          # (R5, D100 e D101: isto e' TESTE, nao a guarda) a clausula do Tetelestai em 1 - beta com a clausula do limite, a reconstrucao, a errata, o dispositivo (so' citacao) e a ratificacao de 10/11, PT e EN; as erratas E36 e E37; as leituras novas
          DL.ERRATA_E36, DL.ERRATA_E37, DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_EN, DL.FRASE_RECONSTROI_PT, DL.FRASE_RECONSTROI_EN, DL.FRASE_E36_PT, DL.FRASE_E36_EN, DL.FRASE_DISPOSITIVO_PT, DL.FRASE_DISPOSITIVO_EN, DL.FRASE_NOMES_RATIFICADOS_D101_PT, DL.FRASE_NOMES_RATIFICADOS_D101_EN,
          DL.ANUNCIO_TETELESTAI_PT, DL.ANUNCIO_TETELESTAI_EN, DL.LEITURA_V410["a_clausula_do_tetelestai"], DL.LEITURA_V410["a_regra_do_nome"],
          # (R6, D106 a D109, D113 e D116 a D123: isto e' TESTE, nao a guarda) as decisoes do conserto, a errata E38, a frase da finura da leitura (PT e EN) e a leitura nova
          DL.ERRATA_E38, DL.ERRATA_E39, DL.ERRATA_E40, DL.FRASE_SECAO7_PT, DL.FRASE_SECAO7_EN, DL.FRASE_ESCALA_UMA_PT, DL.FRASE_ESCALA_UMA_EN, *[DL.DECISOES[k_] for k_ in ("D109", "D113", "D116", "D117", "D118", "D119", "D120", "D121", "D122", "D123")], DL.DECISOES["D106"], DL.DECISOES["D107"], DL.DECISOES["D108"], DL.FRASE_FINURA_PT, DL.FRASE_FINURA_EN, DL.LEITURA_V410["o_observador_e_a_escala"]]
LIMPAS = list(_G9["LIMPAS"]) + _L410 + _L_F59
CITADAS_DE_ERRATA = tuple(_G9["CITADAS_DE_ERRATA"])
APONTADAS_OBRIGACOES_PEDRA = ("F34_", "F37_", "F47_", "F47b_")   # (as obrigacoes de qualificador LITERAL; numa PEDRA elas sao apontadas a gerencia, nao corrigidas pelo agente; proibicao reprova sempre)
_norm = _G9["_norm"]
sem_falas = _G9["sem_falas"]


def violacoes(txt, excecoes=EXCECOES):
    t = str(txt)
    for e_ in sorted(excecoes, key=len, reverse=True):
        t = t.replace(e_, " ")
    return RT._v410_guarda_frases(t)


def _falas_do_operador():
    """o corpus das excecoes das pedras: as falas de 06/11 pelo texto que o um.py v410 embute (de uma, so' o trecho da D65) + o corpus da v409 (05/11, 04/11 e os arquivos de v407, v406, v405), em minusculas e com o espaco normalizado."""
    de_06 = [v_["text"] for v_ in DL.verbatins410(os.path.join(HERE, "insumos", "cunhagens"))]
    return " || ".join([_norm(t_) for t_ in de_06] + [_G9["_falas_do_operador"]()]).lower()


def pedras():
    """a varredura da pedra da gerencia (v410: IALD2, na copia duravel normalizada v410\\pedra): {modulo: {violacoes (proibicoes), apontadas (obrigacoes de qualificador literal), falas_retiradas}}."""
    falas = _falas_do_operador(); out = {}
    for s_ in list(DL.PEDRAS_V410):
        t_, n_ = sem_falas(open(s_["src"], encoding="utf-8").read(), falas)
        v_ = [list(x_) for x_ in RT._v410_guarda_frases(t_)]
        out[s_["name"]] = {"violacoes": [x_ for x_ in v_ if not x_[0].startswith(APONTADAS_OBRIGACOES_PEDRA)], "apontadas": [x_ for x_ in v_ if x_[0].startswith(APONTADAS_OBRIGACOES_PEDRA)], "falas_retiradas": n_}
    return out


def controle_negativo():
    r = {"proibidas": {}, "limpas": {}, "fala_do_operador": {}}
    for f_ in PROIBIDAS:
        r["proibidas"][f_] = [v_[0] for v_ in violacoes("o texto diz que " + f_ + " aqui")]
    for f_ in LIMPAS:
        r["limpas"][f_] = [v_[0] for v_ in violacoes(f_)]
    r["fala_do_operador"] = {"com_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_NOMES)], "sem_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_NOMES, excecoes=())],
                             "fala_de_06nov_com_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_ENUNCIADO + "; " + DL.FRASE_MATRICIAL)],
                             "fala_de_07nov_com_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_TANGENCIADO + "; " + DL.FRASE_ESPECTRO + "; " + DL.FRASE_ISSO_E_O_ATRATOR)]}
    falas_ = _falas_do_operador()
    G = RT._v410_guarda_frases
    Q = DL.FRASE_QUALIFICADOR_PT
    r["pedras_controle"] = {"frase_da_gerencia_reprovada": bool(G(sem_falas("a transicao ficou com tudo derivado aqui", falas_)[0])),
                            "fala_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_NOMES + "»", falas_)[0]),
                            "fala_de_06nov_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_ENUNCIADO + "»", falas_)[0]) and not G(sem_falas("«" + DL.FRASE_SELETOR + "»", falas_)[0]),
                            "parafrase_da_fala_entre_aspas_reprovada": bool(G(sem_falas("a IALD resolve P vs NP, «disse a gerência»", falas_)[0])),
                            "d65_a_parte_que_fica_fora_nao_e_fala_embutida": not any(x_.lower() in falas_.split(" || ")[[i_ for i_, x2_ in enumerate(DL.VERBATIM_ORIGEM_V410) if os.path.basename(x2_) == DL.N_SOLUCAO][0]] for x_ in DL.FORA_D65),
                            "iald_resolve_p_vs_np_reprova": bool(G("a IALD resolve P vs NP")) and bool(G("the IALD solves P vs NP")) and bool(G("P vs NP: resolvido pela IALD")),
                            "iald_nao_resolve_de_turing_reprova_d81": bool(G("a IALD não resolve P vs NP de Turing; a máquina de Turing padrão sem o leitor fica fora")) and bool(G("a casa não afirma P = nP de Turing")) and bool(G("P = nP is not proven")),   # (D81: negar a afirmacao ou a prova de P = nP de Turing e' a forma vedada; ate' 09/11 esta frase era limpa)
                            "forma_obrigatoria_d81_passa": not G(DL.FRASE_D81_PT) and not G(DL.FRASE_D81_EN),
                            "clay_seco_junto_da_forma_canonica_reprova": bool(G(DL.FRASE_D83_OBRIGATORIA_PT + ". Outra coisa: a TGL resolve o problema do milênio.")) and bool(G(DL.FRASE_CLAY_CANONICA_PT + " E mais: o problema do milênio está resolvido.")) and bool(G(DL.FRASE_D83_OBRIGATORIA_EN + ". Besides: the millennium problem is solved."))
                                                                         and not G(DL.FRASE_D83_OBRIGATORIA_PT) and not G(DL.FRASE_D83_OBRIGATORIA_EN) and not G(DL.FRASE_CLAY_CANONICA_PT) and not G(DL.FRASE_CLAY_CANONICA_EN),   # (achado do pre-teste do ensaio, 09/11: a F35 so' cai no PROPRIO trecho que traz a forma da D83/D84)
                            "o_clay_fica_fora_por_estatuto_passa": not G("a máquina de Turing padrão sem o leitor (o Clay) fica fora por estatuto") and not G("the IALD does not solve P vs NP"),   # (o Clay, a pergunta das classes sem o leitor, fica fora: nao e' a negacao vedada)
                            "estatuto_real_reprova": bool(G("P vs NP [REAL]")) and bool(G("[REAL] P = NP provado")),
                            "algoritmo_polinomial_turing_sem_qualificador_reprova": bool(G("existe algoritmo polinomial em máquinas de Turing padrão")) and bool(G("um algoritmo de tempo polinomial em máquina de Turing padrão")),
                            "algoritmo_polinomial_turing_negado_passa": not G("nada aqui dá algoritmo polinomial em máquina de Turing padrão"),
                            "funtor_idempotente_reprova": bool(G("o funtor é idempotente")) and bool(G("the functor is idempotent")),
                            "funtor_nao_idempotente_passa": not G("o funtor não é idempotente: Γ(u)·Γ(u) = Γ(u∘u)"),
                            "algoritmo_iald_e_p_np_sem_qualificador_reprova": bool(G("o algoritmo IALD decide SAT com uma leitura: P = nP")),
                            "algoritmo_iald_e_p_np_com_qualificador_passa": not G("o algoritmo IALD decide SAT com uma leitura: P = nP " + Q),
                            "algoritmo_iald_e_p_np_qualificador_so_noutro_trecho_reprova": bool(G("o algoritmo IALD satisfaz P = nP. Noutro lugar: " + Q)),
                            "tokens_da_v410_reprovam": all(G("veredito " + t_) for t_ in ("IALD_SOLVES", "POLYNOMIAL_TURING")),
                            "solucao_de_p_np_pela_gerencia_reprova": bool(G("esta pedra é a solução do problema P vs NP")),
                            "solucao_de_p_np_na_fala_passa": not G("«" + DL.FRASE_ENUNCIADO + "»"),
                            "seletor_mesmo_objeto_reprova": bool(G("o seletor da luz é o mesmo objeto que o de ℓ²")),
                            "seletor_forma_passa": not G(DL.FRASE_D70_PT),
                            "par_de_fock_open_reprova": bool(G("o par na face de Fock segue [OPEN]")),
                            "atrator_observado_reprova": bool(G("o atrator foi observado")) and bool(G("the attractor was observed")) and bool(G("o atrator está observado nos dados")),
                            "atrator_nao_observado_passa": not G("o atrator não foi observado: nenhum teste com a natureza entra") and not G("the attractor was not observed: no test with nature enters"),
                            "nome_esgota_reprova": bool(G("o Nome esgota")) and bool(G("the Name exhausts the being")) and bool(G("o Nome do par lido esgota o ser")),
                            "nome_nao_esgota_passa": not G("o Nome não esgota o ser") and not G("the Name does not exhaust the being") and not G("tangenciado, jamais esgotado"),
                            "a_frase_d71_passa": not G(DL.FRASE_D71_PT) and not G(DL.FRASE_D71_EN),
                            "fala_de_07nov_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_TANGENCIADO + "»; «" + DL.FRASE_ISSO_E_O_ATRATOR + "»", falas_)[0]),
                            "cinco_sigma_atingido_reprova": bool(G("5σ atingido no H0DN; pré-registrado; nenhum dado observado lido")) and bool(G("5 sigma observado")) and bool(G("o teste deu positivo")) and bool(G("the test gave five sigma")),
                            "cinco_sigma_nao_alcancado_passa": not G("abaixo do degrau de 5σ da creditação; a linha dos 5σ não foi alcançada") and not G("β a 5σ é o que a natureza decide"),
                            "h0dn_detectado_reprova": bool(G("o H0DN detectou o desvio; pré-registrado; nenhum dado observado lido")) and bool(G("H0DN confirms the TGL; pre-registered; no observed data read")),
                            "h0dn_sem_obrigacao_reprova": bool(G("o registro H0DN entra nesta versão")) and bool(G("the H0DN record enters this version")),
                            "h0dn_com_obrigacao_passa": not G("o registro H0DN × BG1 entra pré-registrado; nenhum dado observado lido") and not G("H0DN × BG1: pre-registered; no observed data read"),
                            "tokens_h0dn_reprovam": all(G("veredito " + t_ + "; pré-registrado; nenhum dado observado lido") for t_ in DL.TOKENS_PROIBIDOS_H0DN if t_ != "DETEC" + "TED"),
                            "d72_passa": not G(DL.DECISOES["D72"]) and not G(DL.FRASE_DA_MOLDURA_H0DN_PT) and not G(DL.FRASE_DA_MOLDURA_H0DN_EN),
                            "e30_nao_falsificado_como_cabeca_de_5sigma_reprova": bool(G("o resultado acima de 5σ é não falsificado")) and bool(G("veredito NOT_FALSIFIED_POWERED_AT_5_SIGMA")) and bool(G("not falsified at five sigma")),
                            "e30_leitura_do_5sigma_passa": not G(DL.VEREDITOS_H0DN["leitura"] % 6) and not G(DL.ERRATA_E30) and not G("a regra do 4,44: NOT_FALSIFIED_POWERED, não discriminado à sensibilidade disponível, abaixo do degrau de 5σ da creditação"),
                            "e30_fala_do_operador_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_LEITURA_DO_5SIGMA + "»", falas_)[0]),
                            "a_regra_da_v409_segue": bool(G("a TGL resolve o problema do Clay")) and bool(G("P = nP é teorema da TGL e vale para as máquinas de Turing")),
                            "a_frase_d64_passa": not G(DL.FRASE_D64_PT) and not G(DL.FRASE_D64_EN),
                            "a_moldura_v410_passa": not G(DL.FRASE_DA_MOLDURA_V410_PT) and not G(DL.FRASE_DA_MOLDURA_V410_EN),
                            # v410 (10/11, D94): a regra F59
                            "f59_passos_negados_reprova": bool(G("o tempo não são passos da máquina de Turing")) and bool(G("the cycles are not steps of the Turing machine")) and bool(G("a escala não são passos")) and bool(G("isto não passos da máquina de Turing")),
                            "f59_leitor_paga_reprova": bool(G("o leitor paga a escala")) and bool(G("a escala que o leitor paga")) and bool(G("the reader pays the scale")) and bool(G("o leitor do fundo pagou o tempo")),
                            "f59_decisor_mentiroso_reprova": bool(G("o decisor sem escala é mentiroso")) and bool(G("o decisor sem escala é o Pai da Mentira")) and bool(G("o decisor sem escala foi chamado de mentiroso")) and bool(G("the decider without scale is a liar")),
                            "f59_forma_do_tempo_passa": not G(DL.FRASE_TEMPO_PT) and not G(DL.FRASE_TEMPO_EN),
                            "f59_o_leitor_e_a_escala_passa": not G("o leitor é a escala") and not G("o leitor não paga a escala, porque ele é a escala") and not G("the reader does not pay the scale"),
                            "f59_fala_do_operador_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_ELE_E_A_ESCALA + "»; «" + DL.FRASE_MENTIRA_LIDA_E_VERDADE + "»; «O leitor não “paga” a escala, porque ele é a escala»", falas_)[0]),
                            "f59_decisor_sem_escala_nao_le_passa": not G("o decisor sem escala não lê") and not G("o Pai da Mentira só não faz reconhecimento verdadeiro") and not G("o decisor sem escala não é o Pai da Mentira") and not G("o decisor sem escala não é chamado de mentiroso"),
                            "f59_d94_d96_e33_e34_passam": not G(DL.DECISOES["D94"]) and not G(DL.DECISOES["D96"]) and not G(DL.ERRATA_E33) and not G(DL.ERRATA_E34),
                            "r2_d99_e35_e_as_clausulas_do_adendo_4_passam": not G(DL.DECISOES["D99"]) and not G(DL.ERRATA_E35) and not G(DL.CLAUSULA_Z_PT) and not G(DL.CLAUSULA_Z_EN) and not G(DL.FRASE_SEIS_NOMES_PT) and not G(DL.FRASE_SEIS_NOMES_EN)
                                                                            and not G("a decisão em tempo finito do ciclo, linear nos bits (" + DL.CLAUSULA_Z_PT + ")") and not G("the decision in finite time of the cycle, linear in the bits (" + DL.CLAUSULA_Z_EN + ")"),
                            "r2_a_costura_do_tempo_passa": not G(DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) and not G(DL.ROTULO_TEMPO_EN + " " + DL.FRASE_TEMPO_EN_COSTURADA),
                            "r2_f59_e_f54_nao_pegam_as_clausulas_novas": not any(v_[0].startswith(("F59", "F54")) for t_ in (DL.CLAUSULA_Z_PT, DL.CLAUSULA_Z_EN, DL.DECISOES["D99"], DL.ERRATA_E35, DL.FRASE_SEIS_NOMES_PT, DL.FRASE_SEIS_NOMES_EN, "o texto diz que " + DL.CLAUSULA_Z_PT + " aqui") for v_ in G(t_)),
                            # (R5, D100 e D101) as decisoes, as erratas e as frases novas passam; F44, F54, F58 e F59 nao pegam a clausula; as falas 27 e 28 entre aspas passam
                            "r5_d100_d101_e36_e37_passam": not G(DL.DECISOES["D100"]) and not G(DL.DECISOES["D101"]) and not G(DL.ERRATA_E36) and not G(DL.ERRATA_E37),
                            "r5_as_frases_da_clausula_passam": not any(G(x_) for x_ in (DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_EN, DL.FRASE_RECONSTROI_PT, DL.FRASE_RECONSTROI_EN, DL.FRASE_E36_PT, DL.FRASE_E36_EN, DL.FRASE_DISPOSITIVO_PT, DL.FRASE_DISPOSITIVO_EN, DL.FRASE_NOMES_RATIFICADOS_D101_PT, DL.FRASE_NOMES_RATIFICADOS_D101_EN)),
                            "r5_f44_f54_f58_f59_nao_pegam_a_clausula": not any(v_[0].startswith(("F44", "F54", "F58", "F59")) for t_ in (DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_EN, DL.FRASE_E36_PT, DL.FRASE_E36_EN, DL.DECISOES["D100"], DL.DECISOES["D101"], DL.ERRATA_E36, DL.ERRATA_E37, DL.FRASE_DISPOSITIVO_PT, DL.FRASE_DISPOSITIVO_EN) for v_ in G(t_)),
                            "r5_as_falas_27_e_28_entre_aspas_passam": not G(sem_falas("«" + DL.FRASE_CLAUSULA_NO_ACOM + "»; «" + DL.FRASE_UM_MENOS_BETATGL + "»; «" + DL.FRASE_BETATGL_OPERADOR_MODULAR + "»; «" + DL.FRASE_CONFIRMO_TUDO + "»; «" + DL.FRASE_NOMEIO_O_NUMERO_CORRIGE + "»", falas_)[0]),
                            "r5_a_forma_antiga_da_ratificacao_nao_e_a_vigente": "a ratificar" not in DL.ESTATUTO_NOMES_NOVOS_AESCALA and "DECLARADO" not in DL.ESTATUTO_NOMES_NOVOS_AESCALA and "RATIFICADOS pelo operador em 10/11/2026" in DL.ESTATUTO_NOMES_NOVOS_AESCALA,
                            "f59_a_regra_nao_pegou_a_pedra_da_r4": not any(v_[0].startswith("F59") for p_ in DL.PEDRAS_V410 for v_ in G(sem_falas(open(p_["src"], encoding="utf-8").read(), falas_)[0]))}
    r["ok"] = bool(all(r["proibidas"].values()) and not any(r["limpas"].values()) and not r["fala_do_operador"]["com_a_excecao"] and r["fala_do_operador"]["sem_a_excecao"] and not r["fala_do_operador"]["fala_de_06nov_com_a_excecao"]
                   and not r["fala_do_operador"]["fala_de_07nov_com_a_excecao"] and all(r["pedras_controle"].values()))
    return r


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    c = controle_negativo()
    c["pedras"] = pedras(); c["pedras_limpas"] = not any(v_["violacoes"] for v_ in c["pedras"].values())
    c["pedras_apontadas_a_gerencia"] = {k_: v_["apontadas"] for k_, v_ in c["pedras"].items() if v_["apontadas"]}
    if not c["pedras_limpas"]:
        print("FRASE DE PEDRA REPROVADA (proibicao; apontar a gerencia, nao corrigir):", {k_: v_["violacoes"][:3] for k_, v_ in c["pedras"].items() if v_["violacoes"]})
    if c["pedras_apontadas_a_gerencia"]:
        print("PEDRA: obrigacao de qualificador literal APONTADA a gerencia (informativo):", {k_: [x_[0] for x_ in v_] for k_, v_ in c["pedras_apontadas_a_gerencia"].items()})
    if not c["ok"]:
        print("CONTROLE NEGATIVO FALHOU:", {"proibidas_que_passaram": [k_ for k_, v_ in c["proibidas"].items() if not v_], "limpas_reprovadas": {k_: v_ for k_, v_ in c["limpas"].items() if v_}, "fala": c["fala_do_operador"], "pedras_controle": {k_: v_ for k_, v_ in c["pedras_controle"].items() if not v_}})
    b_ = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
    open(os.path.join(HERE, "GUARDA_FRASES_v410.json.tmp"), "wb").write(b_); os.replace(os.path.join(HERE, "GUARDA_FRASES_v410.json.tmp"), os.path.join(HERE, "GUARDA_FRASES_v410.json"))
    print("controle negativo:", "PASSOU" if c["ok"] else "FALHOU", "| proibidas reprovadas: %d de %d | limpas aceitas: %d de %d" % (sum(1 for v in c["proibidas"].values() if v), len(c["proibidas"]), sum(1 for v in c["limpas"].values() if not v), len(c["limpas"])))
    print("pedras:", "LIMPAS" if c["pedras_limpas"] else "REPROVADAS", "| falas retiradas:", sum(v_["falas_retiradas"] for v_ in c["pedras"].values()), "| apontadas:", sum(len(v_) for v_ in c["pedras_apontadas_a_gerencia"].values()))
    rc = 0 if (c["ok"] and c["pedras_limpas"]) else 1
    for p in sys.argv[1:]:
        v = violacoes(open(p, encoding="utf-8").read())
        print(p, "->", "LIMPO" if not v else v[:6])
        rc |= bool(v)
    sys.exit(rc)
