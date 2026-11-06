# -*- coding: utf-8 -*-
"""_fix_textos_444_e_provada_v409.py -- (claude-construtor-v409, 05/11/2026) as CAUSAS que o harness dos textos achou nos textos RENDERIZADOS (handoff, Atlas, linhagem, Mapa), corrigidas na FONTE do texto (nenhum teste relaxado):
(1) a regra da ordem do operador (23/10): o 4,44 nunca vai sozinho (o p calibrado, a linha dos 5 sigma e o «nao foi alcancado» no MESMO campo). A ressalva (9) do delta NOMEAVA a regra pelo numero e ia
    a todo texto (registro, handoff, Atlas, Mapa); o limite D56 de cunhagens_v409 trazia a REGRA_DO_4_44 inteira (sem o «alcancado»); e a secao nova do artigo PT/EN citava o numero. A v409 nao cita o numero:
    o numero fica no quadro do topo, com a regra inteira (como a v408 fez: o paragrafo novo vai «sem o 4,44»). A REGRA_DO_4_44 segue no campo proprio dos registros (regra_do_4_44), como na v408.
(2) a regra D57(b)/G1 (provada so' com o estatuto na mesma frase): a E25 e a lacuna de fidelidade dela diziam «a trava esta' provada (a_trava_no_nome)» sem o estatuto; passam a dizer, na mesma frase, «validade no kernel, nao creditacao»."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

d = Arq("delta_v409.py")
d.troca('''    "a regra do 4,44 vale em qualquer texto que o cite; o numero da Fase 9 V2 fica no quadro do Teste da Unica Palavra, com a sua regra inteira e a linha dos 5 sigma, e nao e' repetido nesta ressalva",''',
        '''    "a regra da ordem do operador sobre o z_disc da Fase 9 V2 vale em qualquer texto que o cite (nunca sozinho: com o p calibrado e a linha dos 5 sigma, que nao foi alcancada); o numero fica no quadro do Teste da Unica Palavra, com a regra inteira, e nao e' repetido nesta versao",''')
d.troca('''"(«o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no Nome»); a frase foi retirada; a trava esta' provada (a_trava_no_nome)")''',
        '''"(«o sistema não precisa reconhecer onde está o nome a cada passo, ele trava no Nome»); a frase foi retirada; a trava esta' provada no kernel (a_trava_no_nome; validade no kernel, nao creditacao)")''')
d.grava()

r = Arq("registros_v409.py")
r.troca('''"lacuna_de_fidelidade": "a gerencia exigiu do sistema um reconhecimento que a trava dispensa; o operador corrigiu e a trava esta' provada (a_trava_no_nome)",''',
        '''"lacuna_de_fidelidade": "a gerencia exigiu do sistema um reconhecimento que a trava dispensa; o operador corrigiu e a trava esta' provada no kernel (a_trava_no_nome; validade no kernel, nao creditacao)",''')
r.troca('''"[REAL, alcance] " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + " (D56); " + DL.REGRA_DO_4_44,''',
        '''"[REAL, alcance] " + DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT + " (D56); a regra do quadro do topo fica no campo regra_do_4_44 deste registro e o numero nao e' repetido aqui",''')
r.grava()

p = Arq("artigo_pt_v409.pysnip")
p.troca("# O quadro do topo (O Teste da Unica Palavra, v397) fica onde esta: a regra do 4,44 nao se mexe.", "# O quadro do topo (O Teste da Unica Palavra, v397) fica onde esta: a regra do quadro nao se mexe.")
p.troca("o 4,44 da Fase 9 V2 segue abaixo do degrau de $5\\sigma$ (a regra do 4,44 vale em qualquer texto que o cite).", "o número da Fase 9 V2 fica no quadro do topo, com a regra inteira (o $p$ calibrado e a linha dos $5\\sigma$, que não foi alcançada), e não é repetido nesta seção.")
p.grava()

e = Arq("artigo_en_v409.pysnip")
e.troca("# The top box (The Single Word Test, v397) stays where it is: the 4.44 rule does not move.", "# The top box (The Single Word Test, v397) stays where it is: the rule of the box does not move.")
e.troca("the Phase 9 V2 4.44 stays below the $5\\sigma$ step (the 4.44 rule holds in any text that cites it).", "the Phase 9 V2 number stays in the top box, with its whole rule (the calibrated $p$ and the $5\\sigma$ line, which was not reached), and is not repeated in this section.")
e.grava()
