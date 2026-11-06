# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_gerador_v409.py -- (claude-construtor-v409, 05/11/2026) gerar_candidato_v409.py: o bundle passa a DOIS modulos (TraducaoTuring da R9 + ParNaFaceDeFock; AO LADO mais novo do DESENHO_v409.md).
A conferencia `N_NOVOS == 1` vira `N_NOVOS == DL.N_BUNDLE == 2` (a causa: o bundle mudou; nada relaxado) e as frases do patch do kernel e do ledger dizem os dois modulos."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("gerar_candidato_v409.py")
a.troca("# ---------------- (1) o kernel: o BUNDLE de 1 ----------------", "# ---------------- (1) o kernel: o BUNDLE de 2 (TraducaoTuring, ParNaFaceDeFock) ----------------")
a.troca('''assert nov == DL.BUNDLE_RELS, "a lista dos modulos novos tem de ser o bundle de 1, na ordem do preparo"''', '''assert nov == DL.BUNDLE_RELS, "a lista dos modulos novos tem de ser o bundle de 2, na ordem do preparo"''')
a.troca("N_NOVOS = len(nov); assert N_NOVOS == 1", "N_NOVOS = len(nov); assert N_NOVOS == DL.N_BUNDLE == 2")
a.troca('''"kernel embutido: TGLExt.lean regenerado (+ o import da pedra; sandbox == embutido)"''', '''"kernel embutido: TGLExt.lean regenerado (+ os imports das duas pedras; sandbox == embutido)"''')
a.troca('''"kernel embutido: +%d modulo Lean (TraducaoTuring), do sandbox." % N_NOVOS''', '''"kernel embutido: +%d modulos Lean (TraducaoTuring, ParNaFaceDeFock), do sandbox." % N_NOVOS''')
a.troca('''"    # v409 (05/11/2026): A TRADUCAO AS CLASSES DE TURING -- o bundle de %d modulo (o dicionario de Turing; o modo selecao; a trava no Nome; a fita; o leitor; a fita sem escala; a identidade performada), com os nomes da gerencia ratificados pelo operador" % N_NOVOS''',
        '''"    # v409 (05/11/2026): A TRADUCAO AS CLASSES DE TURING E O PAR NA FACE DE FOCK -- o bundle de %d modulos (TraducaoTuring: o dicionario de Turing; o modo selecao; a trava no Nome; a fita; o leitor; a fita sem escala; a identidade performada; a inscricao; a maquina com o leitor -- e ParNaFaceDeFock: o par de psions na face de Fock, ligado), com os nomes da gerencia (ordem do operador: tudo na v409)" % N_NOVOS''')
a.grava()
