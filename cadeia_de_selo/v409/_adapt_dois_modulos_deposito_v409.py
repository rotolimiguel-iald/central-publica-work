# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_deposito_v409.py -- (claude-construtor-v409, 05/11/2026) o deposito na fila e a rota no mapa (depositar_construtor_v409.py) e o texto do fechar_preparacao_v409.py (ato da gerencia; so' adaptado)
passam ao AO LADO mais novo do DESENHO_v409.md: dois modulos (TraducaoTuring da R9, ParNaFaceDeFock), 82 ancoras, 13 falas, o par na face de Fock ligado, a ponte Omega-uniforme pela inscricao (a identidade de vetores
podada), a E28, nada passa a v410. Os numeros do resumo seguem lidos do PREPARACAO_v409_PRONTA.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
d = Arq("depositar_construtor_v409.py")
d.troca("kernel recibo %s (bundle de %s modulo novo em TGLExt/: TraducaoTuring);", "kernel recibo %s (bundle de %s modulos novos em TGLExt/: TraducaoTuring e ParNaFaceDeFock);")
d.troca('''txt = ("v409 (A traducao as classes de Turing) preparada em 05/11/2026''', '''txt = ("v409 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026''')
d.troca('''"O par na face de Fock segue [OPEN] (D60, da v410 em diante); o Omega do psion e o uniforme da instancia: mesma forma, nao ponte ([OPEN], provar ou podar); de duas falas de 05/11 so' o trecho da D59 entra;''',
        '''"O par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; a E21 da v408 ao lado; D60 revista); a ponte entre o Omega do psion e o uniforme da instancia e' a inscricao, e a identidade de vetores fica podada; com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28), que segue [OPEN] com o leitor que so' conta; de tres falas de 05/11 so' o trecho entra (duas pela D59, uma pelo aviso operacional);''')
d.troca('''"titulo": "v409 preparada (A traducao as classes de Turing, 05/11/2026): candidato %s; pronta=%s"''', '''"titulo": "v409 preparada (A traducao as classes de Turing e o par na face de Fock, 05/11/2026): candidato %s; pronta=%s"''')
d.troca('''"pergunta": "a pedra TraducaoTuring (1 modulo, 62 ancoras) compila no trio sobre o kernel da v408 selada,''', '''"pergunta": "as pedras TraducaoTuring e ParNaFaceDeFock (2 modulos, 82 ancoras) compilam no trio sobre o kernel da v408 selada,''')
d.troca('''"pedra: work\\\\pedras_candidatas_05nov (TraducaoTuringR8 -> TraducaoTuring)", "10 falas do operador de 05/11 (de duas, so' o trecho da D59)"],''',
        '''"pedras: work\\\\pedras_candidatas_05nov (TraducaoTuringR9 -> TraducaoTuring; ParNaFaceDeFockR2 -> ParNaFaceDeFock)", "13 falas do operador de 05/11 (de tres, so' o trecho)"],''')
d.troca('''"metodo": "bundle de 1 modulo em TGLExt/ (molde: a v408),''', '''"metodo": "bundle de 2 modulos em TGLExt/ (molde: a v408),''')
d.troca('''"refs": ["cadeia.preparacao_v408", "kernel.traducao_turing_a_identidade_performada_r8_05nov"],''', '''"refs": ["cadeia.preparacao_v408", "kernel.traducao_turing_r9_inscricao_e_sat_05nov", "kernel.par_na_face_de_fock_ligado_05nov"],''')
d.grava()
f = Arq("fechar_preparacao_v409.py")
f.troca('''txt = ("v409 (A traducao as classes de Turing) preparada em 05/11/2026''', '''txt = ("v409 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026''')
f.troca("o Omega do psion e o estado uniforme da instancia tem a mesma forma, e que sejam o mesmo segue [OPEN] (provar ou podar); o par na face de Fock segue [OPEN] e passa a v410 em diante (D60); de duas falas de 05/11 so' o trecho da D59 entra;",
        "a ponte entre o Omega do psion e o estado uniforme da instancia e' a inscricao, e que sejam o mesmo vetor fica PODADO (espacos diferentes; D60 revista); com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28); o par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; a E21 da v408 ao lado); de tres falas de 05/11 so' o trecho entra (duas pela D59, uma pelo aviso operacional);")
f.troca("Os nomes (o modulo TraducaoTuring e as 62 declaracoes) foram dados pela gerencia c1 e ratificados pelo operador em 05/11/2026 (D55).",
        "Os nomes (o modulo TraducaoTuring e as 72 declaracoes dele) foram dados pela gerencia c1 e ratificados pelo operador em 05/11/2026 (D55); os da ParNaFaceDeFock (o modulo e as 10 declaracoes), dados pela gerencia e ditos ratificados pelo cabecalho da pedra [DECLARADO]; a ParNaFaceDeFock entra pela ordem do operador de tudo entrar na v409.")
f.grava()
g = Arq("acom_inscrever_prep_v409.py")
g.troca("Preparacao da v409 (A traducao as classes de Turing): 1 modulo (TraducaoTuring; os nomes dados pela gerencia c1 e ratificados pelo operador em 05/11, D55) no sandbox k409c;",
        "Preparacao da v409 (A traducao as classes de Turing e o par na face de Fock): 2 modulos (TraducaoTuring, com os nomes dados pela gerencia c1 e ratificados pelo operador em 05/11, D55; ParNaFaceDeFock, nomes da gerencia, ratificacao dita pelo cabecalho da pedra [DECLARADO]) no sandbox k409c;")
g.grava()
