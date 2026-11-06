# -*- coding: utf-8 -*-
"""_adapt_fechar_prep_v409.py -- (claude-construtor-v409, 05/11/2026) so' ADAPTA fechar_preparacao_v409.py (ato da gerencia; NAO e' executado aqui): a prosa da anotacao do Mapa, do deposito na fila e da transicao ACOM
passa a ser a da v409 (A traducao as classes de Turing, 05/11/2026; revisor Sonnet pela D58; a moldura e as ressalvas da v409; o slug do deposito de 05/11). O corpo (fail-closed, idempotente por marcador, tudo lido do PRONTA) fica."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("fechar_preparacao_v409.py")
a.troca("adaptado em 04/11/2026 a v409 (Tetelestai e' o terminal: bundle de 4 modulos em TGLExt/, registro tetelestai_terminal_v408; nenhuma chave antiga muda).",
        "adaptado em 05/11/2026 a v409 por claude-construtor-v409 (A traducao as classes de Turing: bundle de 1 modulo em TGLExt/, registro traducao_turing_v409; nenhuma chave antiga muda).")
a.troca('"titulo": "v409 preparada (Tetelestai e\' o terminal, 04/11/2026): candidato %s; pronta=%s"', '"titulo": "v409 preparada (A traducao as classes de Turing, 05/11/2026): candidato %s; pronta=%s"')
a.troca("revisao de terceiro (o Sonnet, D54: ate' tres rodadas; quem constroi nao aprova)", "revisao de terceiro (o Sonnet, D58: ate' tres rodadas; quem constroi nao aprova)")
i0 = a.t.index('txt = ("v409 (Tetelestai e\' o terminal) preparada em 04/11/2026'); i1 = a.t.index('       "Avisos para a gerencia:\\n"', i0)
a.t = a.t[:i0] + '''txt = ("v409 (A traducao as classes de Turing) preparada em 05/11/2026 por claude-construtor-v409 para a gerencia c1 (nada instalado; o rito nao rodou). " + res + ".\\n\\n"
       "A moldura vale em todo texto: P = nP e' teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor (a pergunta do Clay) fica fora e nao e' decidida aqui: e' a fita sem escala («eu sou eu mesmo»); validade no kernel nao e' creditacao e o gate nao se move. "
       "As ressalvas vao ditas: a igualdade relativa a um leitor nao decide a pergunta da maquina sem leitor (Baker-Gill-Solovay 1975) [KNOWN]; a fisica fica fora; o Omega do psion e o estado uniforme da instancia tem a mesma forma, e que sejam o mesmo segue [OPEN] (provar ou podar); o par na face de Fock segue [OPEN] e passa a v410 em diante (D60); de duas falas de 05/11 so' o trecho da D59 entra; o insumo do acervo da v407 entra pela copia purgada (D57d); nenhum teste com a natureza entra; a regra do 4,44 vale em qualquer texto que o cite. Os nomes (o modulo TraducaoTuring e as 62 declaracoes) foram dados pela gerencia c1 e ratificados pelo operador em 05/11/2026 (D55).\\n\\n"
''' + a.t[i1:]
a.troca('"--alvo", "novo:v409-preparada-04nov", "--casa", "Central de Patentes", "--slug", "v409-preparada-04nov",', '"--alvo", "novo:v409-preparada-05nov", "--casa", "Central de Patentes", "--slug", "v409-preparada-05nov",')
a.marca("so' adaptado (ato da gerencia, nao executado pelo construtor): a prosa da v409 (Mapa, fila, ACOM), o revisor pela D58, o slug de 05/11")
a.grava()
