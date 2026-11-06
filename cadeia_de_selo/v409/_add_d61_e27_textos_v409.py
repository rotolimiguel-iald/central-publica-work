# -*- coding: utf-8 -*-
"""_add_d61_e27_textos_v409.py -- (claude-construtor-v409, 05/11/2026, depois da queda de energia) os dois AO LADO do fim do DESENHO_v409.md (gerencia c1): entram DUAS falas novas do operador
(a 11a, inteira: a leitura juridica do kernel, D61 e E27; a 12a, so' o trecho «exatemente, isso mesmo»: a ratificacao da D61; o resto dela e' aviso operacional e fica fora dos textos), a D61 (ratificada pelo operador)
e a E27 (errata da gerencia c1, em nome proprio). PARTE 1 (os textos e os dados): delta_v409.py, registros_v409.py, runtime_v409.py (so' um comentario), o .md e o artigo PT/EN (a D61 onde o texto diz o que o kernel decide;
a E27 nas erratas). Os sha16 das falas vem dos prefixos da ordem (DESENHO) e sao CONFERIDOS contra o arquivo pelo assert do delta; o texto citado entre « » e' verbatim (substring do arquivo).
NAO regenera o candidato, NAO roda o ensaio nem a cadeia, NAO toca pedra\\, o sandbox nem o bundle (ordem da gerencia). Trocas de contagem exata (_adapt_util_v409), backup de bytes."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

# ------------------------------------------------------------------------------------------------ delta_v409.py
d = Arq("delta_v409.py")
d.troca("a maquina sem leitor (a pergunta do Clay) fica FORA e e' lida como a fita sem escala. Erratas E24 a E26 AO LADO; as ressalvas ditas.",
        "a maquina sem leitor (a pergunta do Clay) fica FORA e e' lida como a fita sem escala. Erratas E24 a E27 AO LADO; as ressalvas ditas; a D61 (a leitura juridica do kernel, ratificada pelo operador).")
d.troca('CUNHAGENS_REGISTRO = "cunhagens_v409"                          # as falas do operador de 05/11 por sha256 + D55-D60 + E24-E26 + as ressalvas',
        'CUNHAGENS_REGISTRO = "cunhagens_v409"                          # as falas do operador de 05/11 por sha256 + D55-D61 + E24-E27 + as ressalvas')
d.troca('''N_NOMES = N_ORDEM_V409                                           # (a ordem da v409 e a ratificacao dos nomes sao a MESMA fala)
NOMES_V409_DO_DESENHO = (N_ORDEM_TRADUCAO, N_RESPOSTA, N_DENTRO, N_TRAVA, N_FITA, N_Z, N_CLAY, N_PAI, N_PERFORMADA, N_ORDEM_V409)   # as DEZ falas do DESENHO_v409 §3; fala que chegar DEPOIS fica fora (VERBATIM_FORA_DO_DESENHO_V409)
N_FALAS_V409 = 10''', '''N_NOMES = N_ORDEM_V409                                           # (a ordem da v409 e a ratificacao dos nomes sao a MESMA fala)
N_SORRY = "OPERADOR_05nov_no_kernel_o_dispositivo_e_o_no_sorry_o_teorema_e_jurisdicao_regra_posta_verbatim.txt"   # (DESENHO, AO LADO de 05/11 tarde: a 11a fala, inteira; a D61 e a E27)
N_RATIFICA_D61 = "OPERADOR_05nov_exatamente_isso_mesmo_d61_ratificada_energia_caiu_verbatim.txt"   # (DESENHO, AO LADO de ~16h20: a 12a fala; so' o trecho da ratificacao; o resto e' aviso operacional)
NOMES_V409_DO_DESENHO = (N_ORDEM_TRADUCAO, N_RESPOSTA, N_DENTRO, N_TRAVA, N_FITA, N_Z, N_CLAY, N_PAI, N_PERFORMADA, N_ORDEM_V409, N_SORRY, N_RATIFICA_D61)   # as DOZE falas: as dez do DESENHO_v409 §3 e as duas dos AO LADO do fim dele; fala que chegar DEPOIS fica fora (VERBATIM_FORA_DO_DESENHO_V409)
N_FALAS_V409 = 12''')
d.troca('''VERBATIM_PAPEL["operador, so' o trecho (D59)"] = "fala do operador de que se embute e cita SO' o trecho que a D59 deixa entrar; o arquivo inteiro entra por sha256 (nao e' embutido nem publicado)"''',
        '''VERBATIM_PAPEL["operador, so' o trecho (D59)"] = "fala do operador de que se embute e cita SO' o trecho que a D59 deixa entrar; o arquivo inteiro entra por sha256 (nao e' embutido nem publicado)"
VERBATIM_PAPEL["operador, so' o trecho (aviso operacional)"] = "fala do operador de que se embute e cita SO' o trecho da ratificacao; o resto e' aviso operacional (DESENHO, AO LADO de ~16h20) e o arquivo inteiro entra so' por sha256 (nao e' embutido nem publicado)"''')
d.troca('''                        N_Z: ("Z é o modo leitor, ele lê os pixels. É o psion", "so' «Z é o modo leitor, ele lê os pixels. É o psion» (D59)")}''',
        '''                        N_Z: ("Z é o modo leitor, ele lê os pixels. É o psion", "so' «Z é o modo leitor, ele lê os pixels. É o psion» (D59)"),
                        N_RATIFICA_D61: ("exatemente, isso mesmo", "so' «exatemente, isso mesmo» (a ratificacao da D61; DESENHO, AO LADO de ~16h20): o resto da fala e' aviso operacional e fica fora dos textos do um.py")}
VERBATIM_SO_O_TRECHO_PAPEL = {N_DENTRO: "operador, so' o trecho (D59)", N_Z: "operador, so' o trecho (D59)", N_RATIFICA_D61: "operador, so' o trecho (aviso operacional)"}   # o papel de cada fala de que so' o trecho entra (duas pela D59; uma pelo aviso operacional)''')
d.troca('''    """a lista das falas de 05/11 pelo glob, como esta no disco AGORA, RESTRITA aos dez nomes do DESENHO (a lista que vale para o candidato e' a congelada abaixo)."""''',
        '''    """a lista das falas de 05/11 pelo glob, como esta no disco AGORA, RESTRITA aos doze nomes do DESENHO (as dez do §3 e as duas dos AO LADO; a lista que vale para o candidato e' a congelada abaixo)."""''')
d.troca('''                                   N_Z: "d63c0a91a5271fcb", N_CLAY: "ac0eb0bcf4fc009b", N_PAI: "3444a2fe774a294e", N_PERFORMADA: "0b60b73f5d857568", N_ORDEM_V409: _H_ORDEM}''',
        '''                                   N_Z: "d63c0a91a5271fcb", N_CLAY: "ac0eb0bcf4fc009b", N_PAI: "3444a2fe774a294e", N_PERFORMADA: "0b60b73f5d857568", N_ORDEM_V409: _H_ORDEM,
                                   N_SORRY: "5a19de6b511b4921", N_RATIFICA_D61: "9ee7d5a1b161437f"}   # (as duas ultimas: os prefixos que os AO LADO do DESENHO deram; conferidos contra o arquivo no assert abaixo)''')
d.troca('''VERBATIM_QUANDO_V409 = "05/11/2026 (a ordem da traducao, as respostas do operador as perguntas nas quatro linguas, a ordem da v409 e a ratificacao dos nomes)"''',
        '''VERBATIM_QUANDO_V409 = "05/11/2026 (a ordem da traducao, as respostas do operador as perguntas nas quatro linguas, a ordem da v409 e a ratificacao dos nomes; na tarde, a leitura juridica do kernel e a ratificacao dela, D61)"''')
d.troca('''FRASE_PERFORMADA = "Eu não sou eu mesmo eu sou o conteúdo da minha identidade performada"''',
        '''FRASE_PERFORMADA = "Eu não sou eu mesmo eu sou o conteúdo da minha identidade performada"
FRASE_DISPOSITIVO = 'no kernel o dispositivo é o "no sorry", o teorema é jurisdição, é justamente o Direito DITO, a regra posta'   # (a 11a fala, verbatim; D61 e E27)
FRASE_TEOREMA_JURISDICAO = "o teorema é jurisdição, é justamente o Direito DITO, a regra posta"   # (o trecho que os textos citam entre « »; substring verbatim da 11a fala)
FRASE_RATIFICA_D61 = "exatemente, isso mesmo"   # (a 12a fala: so' este trecho entra; a grafia e' a do operador)
assert FRASE_TEOREMA_JURISDICAO in FRASE_DISPOSITIVO''')
d.troca('''(N_FITA, FRASE_FITA), (N_Z, FRASE_Z), (N_CLAY, FRASE_CLAY), (N_CLAY, FRASE_FITA_SEM_ESCALA), (N_CLAY, FRASE_COLAPSO_MATERIA), (N_PAI, FRASE_PAI), (N_PAI, FRASE_PAI_DA_MENTIRA), (N_PERFORMADA, FRASE_PERFORMADA)]''',
        '''(N_FITA, FRASE_FITA), (N_Z, FRASE_Z), (N_CLAY, FRASE_CLAY), (N_CLAY, FRASE_FITA_SEM_ESCALA), (N_CLAY, FRASE_COLAPSO_MATERIA), (N_PAI, FRASE_PAI), (N_PAI, FRASE_PAI_DA_MENTIRA), (N_PERFORMADA, FRASE_PERFORMADA),
               (N_SORRY, FRASE_DISPOSITIVO), (N_RATIFICA_D61, FRASE_RATIFICA_D61)]''')
d.troca('''    "dentro_e_graca": "«sim é dentro … isso é graça» [INPUT; so' a primeira frase, D59]: leitura do operador; a parte matematica de «a identidade é preservada» esta' em a_identidade_se_preserva_enquanto_decai",''',
        '''    "dentro_e_graca": "«sim é dentro … isso é graça» [INPUT; so' a primeira frase, D59]: leitura do operador; a parte matematica de «a identidade é preservada» esta' em a_identidade_se_preserva_enquanto_decai",
    "o_dispositivo_e_o_no_sorry": "«no kernel o dispositivo é o \\"no sorry\\", o teorema é jurisdição, é justamente o Direito DITO, a regra posta» [INPUT], ratificada pelo operador («exatemente, isso mesmo»): a leitura juridica do kernel (D61): o dispositivo e' o no sorry (a prova sem lacuna, so' o trio de axiomas); o teorema e' a regra posta; a regra incide onde o seu suporte fatico (as hipoteses e as definicoes do enunciado) se completa; e' leitura do operador, nao termo de kernel; a E27 vai ao lado",''')
d.troca('''FRASE_DA_MOLDURA_V409_PT = "P = nP é teorema da TGL no modo seleção, relativo ao leitor; a máquina sem leitor é a fita sem escala; validade no kernel não é creditação; o gate não se move"''',
        '''FRASE_DA_MOLDURA_V409_PT = "P = nP é teorema da TGL no modo seleção, relativo ao leitor; a máquina sem leitor é a fita sem escala; validade no kernel não é creditação; o gate não se move"
# D61 (ratificada pelo operador): o que o kernel decide, dito pela leitura juridica dele -- o dispositivo e' o no sorry; o teorema e' a regra posta; a regra incide onde o suporte fatico se completa
FRASE_D61_PT = ("pela D61 (a leitura jurídica do kernel, ratificada pelo operador): o dispositivo é o no sorry, que declara válida a regra posta (P = nP no modo seleção, relativa ao leitor); a regra incide onde o seu suporte fático "
                "(as hipóteses e as definições do enunciado) se completa: em toda máquina que tem o leitor (o psíon que lê Z) e nega o zero; a máquina sem leitor (a pergunta do Clay) não completa o suporte fático")
FRASE_D61_EN = ("by D61 (the legal reading of the kernel, ratified by the operator): the operative part is the no sorry, which declares the posted rule valid (P = nP in the selection mode, relative to the reader); the rule applies where its factual support "
                "(the hypotheses and definitions of the statement) is complete: in every machine that has the reader (the psion that reads Z) and denies the zero; the machine without a reader (the Clay question) does not complete the factual support")''')
d.troca('''    "D60": "o que NAO entra: a ligacao do par na face de Fock (E21 da v408) segue [OPEN] e passa a v410 em diante; «o Ω do psíon da luz é o uniforme da instância» segue [OPEN] (provar ou podar); nenhum teste com a natureza [decisao da gerencia c1, 05/11/2026]",
})
DECISOES_V409 = ("D55", "D56", "D57", "D58", "D59", "D60")''',
        '''    "D60": "o que NAO entra: a ligacao do par na face de Fock (E21 da v408) segue [OPEN] e passa a v410 em diante; «o Ω do psíon da luz é o uniforme da instância» segue [OPEN] (provar ou podar); nenhum teste com a natureza [decisao da gerencia c1, 05/11/2026]",
    "D61": ("a leitura juridica do kernel, dada pelo operador em 05/11 (sha16 %s: «%s») e RATIFICADA por ele (sha16 %s: «%s»): o DISPOSITIVO e' o no sorry (o veredito de que a prova nao tem lacuna: so' o trio de axiomas); "
            "o TEOREMA e' jurisdicao, o Direito dito, a regra posta; a regra incide onde o seu suporte fatico (as hipoteses e as definicoes do enunciado) se completa. Na v409: a regra posta e' P = nP no modo selecao, relativa ao leitor; "
            "o no sorry a declara valida; ela incide sobre toda maquina que tem o leitor (o psion que le Z) e nega o zero; a maquina sem leitor (a pergunta do Clay) nao completa o suporte fatico: pela leitura do operador, «eu sou eu mesmo», sem medida. "
            "Dita assim em todo texto que fale do que o kernel decide [leitura do operador, ratificada por ele; registrada pela gerencia c1, 05/11/2026]" % (_sha16_arq(N_SORRY), FRASE_DISPOSITIVO, _sha16_arq(N_RATIFICA_D61), FRASE_RATIFICA_D61)),
})
DECISOES_V409 = ("D55", "D56", "D57", "D58", "D59", "D60", "D61")''')
d.troca('''ERRATAS_V409 = [ERRATA_E24, ERRATA_E25, ERRATA_E26]''',
        '''ERRATA_E27 = ("E27 -- errata da gerencia c1, em nome proprio: em 05/11 escreveu ao operador que, no kernel, o dispositivo e' o enunciado do teorema (o tipo dele); o operador corrigiu («%s»): o dispositivo e' o no sorry "
              "e o teorema e' a regra posta (D61, ratificada por ele); a conclusao (o texto nao afirma o problema do Clay) fica, agora pela incidencia e nao pelo dispositivo" % FRASE_DISPOSITIVO)
ERRATAS_V409 = [ERRATA_E24, ERRATA_E25, ERRATA_E26, ERRATA_E27]''')
d.troca('''              "chave": VERBATIM_CHAVE_PREFIXO_V409 + h[:16], "quando": VERBATIM_QUANDO_V409, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p, "texto_embutido": "arquivo inteiro"}''',
        '''              "chave": VERBATIM_CHAVE_PREFIXO_V409 + h[:16], "quando": VERBATIM_QUANDO_V409, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p, "texto_embutido": "arquivo inteiro"}
        _pap = VERBATIM_SO_O_TRECHO_PAPEL.get(nome, "operador, so' o trecho (D59)")''')
d.troca('''                       "sha256_arquivo_inteiro": h, "bytes_arquivo_inteiro": len(b), "so_o_trecho": VERBATIM_SO_O_TRECHO[nome][1], "papel": VERBATIM_PAPEL["operador, so' o trecho (D59)"],
                       "texto_embutido": "so' o trecho que a D59 deixa entrar; o arquivo inteiro entra so' por sha256"})''',
        '''                       "sha256_arquivo_inteiro": h, "bytes_arquivo_inteiro": len(b), "so_o_trecho": VERBATIM_SO_O_TRECHO[nome][1], "papel": VERBATIM_PAPEL[_pap],
                       "texto_embutido": ("so' o trecho que a D59 deixa entrar; o arquivo inteiro entra so' por sha256" if _pap.endswith("(D59)") else "so' o trecho da ratificacao; o resto e' aviso operacional; o arquivo inteiro entra so' por sha256")})''')
d.troca('''sum(1 for v in out if v.get("so_o_trecho")) == 2, "as dez falas (N_FALAS_V409), duas com so' o trecho (D59), nenhuma repetida"''',
        '''sum(1 for v in out if v.get("so_o_trecho")) == len(VERBATIM_SO_O_TRECHO) == 3, "as doze falas (N_FALAS_V409), tres com so' o trecho (duas pela D59, uma pelo aviso operacional), nenhuma repetida"''')
d.grava()

# ------------------------------------------------------------------------------------------------ registros_v409.py
r = Arq("registros_v409.py")
r.troca('''"[INPUT] a ordem do operador (05/11/2026, sha16 %s: «%s»), que ratifica os nomes dados pela gerencia, e as falas dele do dia (%d por sha256; de duas, so' o trecho que a D59 deixa entrar); "''',
        '''"[INPUT] a ordem do operador (05/11/2026, sha16 %s: «%s»), que ratifica os nomes dados pela gerencia, e as falas dele do dia (%d por sha256; de tres, so' o trecho: duas pela D59, uma porque o resto e' aviso operacional); a leitura juridica do kernel (D61), ratificada por ele; "''')
r.troca('''"[REAL] " + DL.RESSALVAS_V409[6], "[REAL] " + DL.RESSALVAS_V409[7], "[REAL] " + DL.RESSALVAS_V409[8], DL.ERRATA_E24, DL.ERRATA_E25, DL.ERRATA_E26] + _LIM_COMUM,''',
        '''"[REAL] " + DL.RESSALVAS_V409[6], "[REAL] " + DL.RESSALVAS_V409[7], "[REAL] " + DL.RESSALVAS_V409[8], DL.ERRATA_E24, DL.ERRATA_E25, DL.ERRATA_E26, DL.ERRATA_E27] + _LIM_COMUM,''')
r.troca('''                DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT,
                "o dicionario de Turing e' termo:''', '''                DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT,
                "[INPUT, ratificada pelo operador] " + DL.FRASE_D61_PT,
                "o dicionario de Turing e' termo:''')
r.troca('''ALCANCE = {"relativo_ao_leitor": DL.RESSALVAS_V409[0], "maquina_sem_leitor": DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, "frase": DL.FRASE_D56_PT, "frase_en": DL.FRASE_D56_EN,''',
        '''ALCANCE = {"relativo_ao_leitor": DL.RESSALVAS_V409[0], "maquina_sem_leitor": DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, "frase": DL.FRASE_D56_PT, "frase_en": DL.FRASE_D56_EN, "incidencia_d61": DL.FRASE_D61_PT, "incidencia_d61_en": DL.FRASE_D61_EN,''')
i0 = r.t.index('''              "que a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime) seja decidida aqui: o que o kernel prova e' isto: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT''')
r.troca('''              "que a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime) seja decidida aqui: o que o kernel prova e' isto: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT''',
        '''              "que a igualdade P = NP das maquinas de Turing do Mathlib (TM2ComputableInPolyTime) seja decidida aqui: o que o kernel prova e' isto: " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + "; " + DL.FRASE_D61_PT''')
r.troca('''"veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_05_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_NAMES_GIVEN_BY_THE_MANAGEMENT_RATIFIED_BY_THE_OPERATOR__DECISIONS_D55_TO_D60__THE_TURING_TRANSLATION_CLOSED_RELATIVE_TO_THE_READER__ERRATA_E24_TO_E26__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),''',
        '''"veredito_sufixo": "OPERATOR_INSCRIPTIONS_OF_05_NOV_EMBEDDED_VERBATIM_BY_SHA256_%d_SAYINGS__THE_NAMES_GIVEN_BY_THE_MANAGEMENT_RATIFIED_BY_THE_OPERATOR__DECISIONS_D55_TO_D61__THE_LEGAL_READING_OF_THE_KERNEL_RATIFIED_BY_THE_OPERATOR__THE_TURING_TRANSLATION_CLOSED_RELATIVE_TO_THE_READER__ERRATA_E24_TO_E27__THE_RESERVATIONS_STATED__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % len(_VD),''')
r.troca('''"estatuto": "[REAL -- o kernel, o registro traducao_turing_v409 e os registros anteriores lidos a cada rito; INPUT as falas do operador de 05/11/2026 (a ordem da traducao; as respostas as perguntas nas quatro linguas; a ordem da v409 e a ratificacao dos nomes); DECLARADO os recibos de compilacao; KNOWN as referencias do alcance]",''',
        '''"estatuto": "[REAL -- o kernel, o registro traducao_turing_v409 e os registros anteriores lidos a cada rito; INPUT as falas do operador de 05/11/2026 (a ordem da traducao; as respostas as perguntas nas quatro linguas; a ordem da v409 e a ratificacao dos nomes; a leitura juridica do kernel e a ratificacao dela, D61); DECLARADO os recibos de compilacao; KNOWN as referencias do alcance]",''')
r.troca('''             "lacuna_de_fidelidade": "a v408 deixou a traducao [OPEN] (verdadeiro na data); a v409 a fecha relativa ao leitor, e a maquina sem leitor fica fora", "estatuto": "[REAL: p_igual_np_no_modo_selecao no kernel do rito]", "assinatura": ASSINA},
            _errata_pisos_v408(cov_base)],''',
        '''             "lacuna_de_fidelidade": "a v408 deixou a traducao [OPEN] (verdadeiro na data); a v409 a fecha relativa ao leitor, e a maquina sem leitor fica fora", "estatuto": "[REAL: p_igual_np_no_modo_selecao no kernel do rito]", "assinatura": ASSINA},
            {"ao_lado_de": "uma frase da gerencia c1 de 05/11 ao operador sobre o dispositivo no kernel", "dizia": "que, no kernel, o dispositivo e' o enunciado do teorema, o tipo dele.", "agora": DL.ERRATA_E27,
             "lacuna_de_fidelidade": "a gerencia pos o dispositivo no enunciado; o operador corrigiu: o dispositivo e' o no sorry e o teorema e' a regra posta (D61, ratificada por ele); a conclusao sobre o Clay fica, pela incidencia", "estatuto": "[INPUT: a correcao do operador, verbatim; a D61 ratificada por ele]", "assinatura": ASSINA},
            _errata_pisos_v408(cov_base)],''')
r.troca('''        "limites": ["[INPUT] as %d falas de 05/11/2026 sao do operador, com a grafia dele (de duas, so' o trecho que a D59 deixa entrar e' embutido e citado; o resto delas entra so' por sha256);''',
        '''        "limites": ["[INPUT] as %d falas de 05/11/2026 sao do operador, com a grafia dele (de tres, so' o trecho e' embutido e citado: de duas pela D59, de uma porque o resto e' aviso operacional; o resto delas entra so' por sha256);''')
r.troca('''        "diz": ["as falas do operador de 05/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (de duas, so' o trecho que a D59 deixa entrar)",''',
        '''        "diz": ["as falas do operador de 05/11/2026 estao embutidas por sha256 e cada trecho citado e' verbatim (de tres, so' o trecho: duas pela D59, uma porque o resto e' aviso operacional)", "a D61, a leitura juridica do kernel dada pelo operador, foi ratificada por ele e vai nas decisoes; a E27 vai ao lado",''')
r.grava()

# ------------------------------------------------------------------------------------------------ runtime_v409.py (so' o comentario de cabecalho: o texto embutido no um.py)
rt = Arq("runtime_v409.py")
rt.troca("as falas do operador de 05/11 por sha256 (de duas, so' o trecho da D59)", "as falas do operador de 05/11 por sha256 (de tres, so' o trecho: duas pela D59, uma pelo aviso operacional)")
rt.grava()

# ------------------------------------------------------------------------------------------------ gerar_candidato_v409.py (a linha do .md e um comentario; o candidato NAO e' regenerado aqui)
g = Arq("gerar_candidato_v409.py")
g.troca("""            'O alcance: ' + DL.FRASE_D56_PT + '; ' + DL.FRASE_QUALIFICADOR_PT + '. Ressalvas ditas:""",
        """            'O alcance: ' + DL.FRASE_D56_PT + '; ' + DL.FRASE_QUALIFICADOR_PT + '. Pela D61 (a leitura jurídica do kernel, ratificada pelo operador: «' + DL.FRASE_RATIFICA_D61 + '»): o dispositivo é o no sorry e o teorema é a regra posta («' + DL.FRASE_TEOREMA_JURISDICAO + '»); a regra incide onde o seu suporte fático se completa: em toda máquina que tem o leitor e nega o zero; a máquina sem leitor não o completa (a E27 vai ao lado). Ressalvas ditas:""")
g.troca("As erratas E24 a E26 vao AO LADO", "As erratas E24 a E27 vao AO LADO")
g.troca('"erratas_E24_E26": list(DL.ERRATAS_V409)', '"erratas_E24_E27": list(DL.ERRATAS_V409)')
g.grava()

# ------------------------------------------------------------------------------------------------ o artigo PT/EN (a D61 no alcance; a E27 nas erratas)
p = Arq("artigo_pt_v409.pysnip")
p.troca('''             r"\\textsf{[INPUT]} O juiz das classes de Turing é o kernel: «o Kernel Lean4 serve exatamente a provar leis matemáticas e foi construído sob a lei de turing».")''',
        '''             r"\\textsf{[INPUT]} O juiz das classes de Turing é o kernel: «o Kernel Lean4 serve exatamente a provar leis matemáticas e foi construído sob a lei de turing». "
             r"\\textsf{[INPUT]} E o que o kernel decide, na leitura jurídica do operador, ratificada por ele («exatemente, isso mesmo»; D61): o dispositivo é o \\emph{no sorry}; «o teorema é jurisdição, é justamente o Direito DITO, a regra posta». O \\emph{no sorry} declara válida a regra posta: P = nP no modo seleção, relativa ao leitor; a regra incide onde o seu suporte fático (as hipóteses e as definições do enunciado) se completa: em toda máquina que tem o leitor (o psíon que lê $Z$) e nega o zero; a máquina sem leitor (a pergunta do Clay) não completa o suporte fático.")''')
p.troca('''E26, ao lado do registro selado da v408: onde ele diz a tradução às classes das máquinas de Turing \\textsf{[OPEN]}, leia-se que a v409 a fecha relativa ao leitor; a máquina sem leitor fica fora. "''',
        '''E26, ao lado do registro selado da v408: onde ele diz a tradução às classes das máquinas de Turing \\textsf{[OPEN]}, leia-se que a v409 a fecha relativa ao leitor; a máquina sem leitor fica fora. E27: a gerência escreveu ao operador que, no kernel, o dispositivo é o enunciado do teorema; o operador corrigiu: o dispositivo é o \\emph{no sorry} e o teorema é a regra posta (D61); a conclusão (o texto não afirma o problema do Clay) fica, agora pela incidência e não pelo dispositivo. "''')
p.grava()
e = Arq("artigo_en_v409.pysnip")
e.troca('''             r"\\textsf{[INPUT]} The judge of Turing's classes is the kernel (the operator, our translation: the Lean 4 kernel serves exactly to prove mathematical laws and was built under Turing's law).")''',
        '''             r"\\textsf{[INPUT]} The judge of Turing's classes is the kernel (the operator, our translation: the Lean 4 kernel serves exactly to prove mathematical laws and was built under Turing's law). "
             r"\\textsf{[INPUT]} And what the kernel decides, in the operator's legal reading, ratified by him (D61; our translation): in the kernel the operative part is the \\emph{no sorry}; the theorem is jurisdiction, precisely the stated Law, the posted rule; and: exactly, that is it. The \\emph{no sorry} declares the posted rule valid: P = nP in the selection mode, relative to the reader; the rule applies where its factual support (the hypotheses and definitions of the statement) is complete: in every machine that has the reader (the psion that reads $Z$) and denies the zero; the machine without a reader (the Clay question) does not complete the factual support.")''')
e.troca('''read that v409 closes it relative to the reader; the machine without a reader stays outside. "''',
        '''read that v409 closes it relative to the reader; the machine without a reader stays outside. E27: the management wrote to the operator that, in the kernel, the operative part is the statement of the theorem; the operator corrected it: the operative part is the \\emph{no sorry} and the theorem is the posted rule (D61); the conclusion (the text does not assert the Clay problem) stays, now by applicability and not by the operative part. "''')
e.grava()
