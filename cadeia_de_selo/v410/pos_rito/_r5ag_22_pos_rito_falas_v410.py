# -*- coding: utf-8 -*-
"""_r5ag_22_pos_rito_falas_v410.py -- R5: textos_v410.py enumerava as 26 falas de 06 a 10/11 (a funcao _ss, achada pelo nome: assert len == DL.N_FALAS_V410, que agora e' 28); as duas falas novas da R5 (a 27a, a clausula do Tetelestai, D100; a 28a, a confirmacao e a regra do nome, D101) entram:
(1) na _ss (achadas pelo NOME do arquivo: nunca digitadas; conferidas contra os prefixos que a ordem da gerencia deu); (2) na forma «curta» e na longa da secao «A ordem» (os sha16 por script e as citacoes verbatim conferidas letra por letra contra os bytes das falas, por _cita); (3) no _TEMA_ESPECIAL (o tema das duas na lista das falas, sem citacao).
Achado do harness_fechar_sandbox_v410.py (o assert das falas no fechar de sandbox). Idempotente (contagem exata); backup de bytes antes."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from _r5ag_lib_v410 import aplicar

aplicar("textos_v410.py", [
    ('''("sem_poder", "teste_sem_poder_preditivo", DL_.N_TESTE_SEM_PODER))''',
     '''("sem_poder", "teste_sem_poder_preditivo", DL_.N_TESTE_SEM_PODER),
            ("clausula", "a_clausula_do_tetelestai_esta_no_acom_mirror", DL_.N_CLAUSULA_TETELESTAI), ("confirmo", "confirmo_tudo_nomeio_e_o_numero_corrige", DL_.N_CONFIRMO_TUDO))   # (R5, D100 e D101: a 27a e a 28a falas)''', 1),
    ('''o teste sem poder preditivo não se roda `{sp10}`"''',
     '''o teste sem poder preditivo não se roda `{sp10}`; "
                  "as falas de 10/11 da R5 (inteiras): a cláusula do Tetelestai no ACOM Mirror `{ct10}`; a confirmação dos nomes e a regra do nome `{cf10}`"''', 1),
    ('''sp10=ss["sem_poder"])''', '''sp10=ss["sem_poder"], ct10=ss["clausula"], cf10=ss["confirmo"])''', 1),
    ('''("pdis", DL_.FRASE_PODER_DISCRIMINANTE_REAL))}''',
     '''("pdis", DL_.FRASE_PODER_DISCRIMINANTE_REAL),
                                  ("clau", DL_.FRASE_CLAUSULA_NO_ACOM), ("recon", DL_.FRASE_RECONHECE_A_SINGULARIDADE), ("trasl", DL_.FRASE_TRASLADA_A_INFORMACAO), ("umb", DL_.FRASE_UM_MENOS_BETATGL), ("confi", DL_.FRASE_CONFIRMO_TUDO), ("nomn", DL_.FRASE_NOMEIO_O_NUMERO_CORRIGE))}''', 1),
    ('''e o teste sem poder preditivo (`{s26}`): {semp}; {pdis}. "''',
     '''e o teste sem poder preditivo (`{s26}`): {semp}; {pdis}; "
              "as falas de 10/11 da R5 (inteiras): a cláusula do Tetelestai (`{s27}`): {clau}; {recon}; {trasl}; {umb}; e a confirmação (`{s28}`): {confi}; a regra do nome: {nomn}. "''', 1),
    ('''s26=ss["sem_poder"], alc=_d64(), **q)''', '''s26=ss["sem_poder"], s27=ss["clausula"], s28=ss["confirmo"], alc=_d64(), **q)''', 1),
    ('''_TEMA_ESPECIAL = {''',
     '''_TEMA_ESPECIAL = {"a_clausula_do_tetelestai_esta_no_acom_mirror_um_menos_beta_beta_e_o_operador_modular": "a cláusula do Tetelestai está no ACOM Mirror: o limiar de 1 − β, em que β é o operador modular do Tetelestai (D100)",
                  "confirmo_tudo_nomeio_e_o_numero_corrige_o_nome_como_zero_modular": "a confirmação do operador: ratifica os nomes pela regra dele (nomeio é o número, o número corrige o nome) e lê o nome como zero modular da inscrição da permanência (D101)",
                  ''', 1)], base=HERE)
