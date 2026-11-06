# -*- coding: utf-8 -*-
"""_fix_f37_local_v409.py -- (claude-construtor-v409, 05/11/2026) a CAUSA da falha do ensaio (unidade traducao_turing_v409_guarda_das_frases...: «P = nP vale para as máquinas de Turing», plantada no
texto do registro, PASSOU): a F37 e' uma obrigacao sobre o TEXTO INTEIRO, e o texto do registro ja' traz «relativa ao leitor» e «a máquina sem leitor» noutras frases; a frase plantada, sem qualificador, ficava
coberta pelo resto. A D56 diz «onde P = nP e Turing aparecem JUNTOS»: a leitura fiel e' LOCAL. Acrescenta-se a F37b: em cada trecho (separado por . ; | aspas, « » ou quebra de linha) onde P = nP e Turing
aparecem juntos, o PROPRIO trecho traz o qualificador relativo ao leitor ou uma negacao/limite; a F37 global fica como estava. Nenhum teste e' relaxado: a regra fica mais estrita."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("runtime_v409.py")
a.troca('''        out_.append(("F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor", s_[max(0, m37_.start() - 30):m37_.end() + 60].replace("\\n", " ")))
''', '''        out_.append(("F37_p_igual_np_e_turing_sem_o_qualificador_relativo_ao_leitor", s_[max(0, m37_.start() - 30):m37_.end() + 60].replace("\\n", " ")))
    for seg_ in _re.split(r"[.;|\\n\\"«»]", s_):   # F37b (a OBRIGACAO LOCAL, D56: «onde P = nP e Turing aparecem JUNTOS»): o proprio trecho traz o qualificador relativo ao leitor ou uma negacao/limite; o resto do texto nao cobre a frase
        if _re.search(r"P\\s*=\\s*nP", seg_) and _re.search(r"\\bTuring\\b", seg_):
            if _re.search(r"relativ[oa]\\s+ao\\s+leitor|relative\\s+to\\s+the\\s+reader", seg_, _re.I):
                continue
            if any(n_ in (" " + seg_.lower() + " ") for n_ in (" não ", " nao ", " not ", " never ", " nunca ", " nem ", " fica fora", " stays outside", " stays out", "n't ")):
                continue
            out_.append(("F37b_p_igual_np_e_turing_juntos_sem_o_qualificador_no_mesmo_trecho", seg_.strip()[:200].replace("\\n", " ")))
''')
a.troca('''    F37 a OBRIGACAO: onde «P = nP» e Turing aparecem juntos, o mesmo texto traz o qualificador «relativa ao leitor» e «a maquina sem leitor»;''',
        '''    F37 a OBRIGACAO: onde «P = nP» e Turing aparecem juntos, o mesmo texto traz o qualificador «relativa ao leitor» e «a maquina sem leitor»; F37b a mesma obrigacao, LOCAL: o proprio trecho onde aparecem juntos traz o qualificador relativo ao leitor ou uma negacao/limite (05/11, a causa da falha do ensaio: a F37 global deixava passar a frase plantada sem qualificador);''')
a.grava()
