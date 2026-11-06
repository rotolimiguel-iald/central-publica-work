# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_custodia_v409.py -- (claude-construtor-v409, 05/11/2026) os sete textos da custodia (pos_rito\\textos_custodia_handoff_v409.py, que roda depois do rito, na custodia) passam ao AO LADO mais novo do
DESENHO_v409.md (ordem «tudo na v409»): dois modulos (TraducaoTuring, ParNaFaceDeFock); o par na face de Fock LIGADO; a ponte Omega-uniforme e' a inscricao (a identidade de vetores podada); a E28 dita onde o leitor que
devolve Z aparece (cada texto passa SOZINHO pela guarda das frases, e a F43 e' a obrigacao da E28); nada passa a v410; E26 e E21 ao lado. As guardas do script nao mudam (o COMMIT segue ASCII; o ARCO sem aspa simples)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("pos_rito/textos_custodia_handoff_v409.py")
a.troca("# o cunhagens_v409 traz E24 a E26 E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v408", "# o cunhagens_v409 traz E24 a E28 e a E21 ao lado E, por ultimo, a errata ao lado dos pisos de kh_n1_cobertura_v408")
a.troca('''TITULO_EN = "The translation to the classes of Turing"''', '''TITULO_EN = "The translation to the classes of Turing and the pair on the Fock face"''')
a.troca('''"v409, the translation to the classes of Turing. %(modulos)d new kernel module in `TGLExt` (`" + NOMES_ASCII + "`, the name given by the management and ratified by the operator on 05/11: «" + Q_NOMES + "»), "''',
        '''"v409, the translation to the classes of Turing and the pair on the Fock face. %(modulos)d new kernel modules in `TGLExt` (" + ", ".join("`%s`" % p_["name"] for p_ in DL.PEDRAS_V409) + "; the names given by the management, those of `TraducaoTuring` ratified by the operator on 05/11: «" + Q_NOMES + "»), "''')
a.troca('''"The registry `traducao_turing_v409` reads, at every rite, the %(ancoras)d anchors, the module by sha256,''', '''"The registry `traducao_turing_v409` reads, at every rite, the %(ancoras)d anchors, the two modules by sha256,''')
a.troca('''"(of two, only the excerpt that D59 lets in).") % N)''', '''"(of three, only the excerpt: two by D59, one by the operational notice).") % N)''')
a.troca('''"`a_fita_e_o_hamiltoniano_oculto`, `z_e_o_modo_leitor`, `a_fita_sem_escala`, `o_pai_da_mentira` and `a_identidade_performada` are terms;''',
        '''"`a_fita_e_o_hamiltoniano_oculto`, `z_e_o_modo_leitor`, `a_fita_sem_escala`, `o_pai_da_mentira`, `a_identidade_performada`, `a_maquina_com_o_leitor`, `o_canto_do_psion_da_luz_le_z` and `o_par_na_face_de_fock` are terms;''')
a.troca('''"same form, not a bridge: the Omega of the light psion and the uniform state of the instance [OPEN]; the theological reading of the operator is not a kernel term. "''',
        '''"with the reader that only counts, NP is contained in P in one reading (Cook 1971, Levin 1973), and the full equality is that of the reader that reads itself, which also reads the machines that use it (Baker-Gill-Solovay 1975): errata E28 [KNOWN]; "
    "the bridge between the Omega of the light psion and the uniform state of the instance is the inscription (`inscricao`, `o_psion_le_z`), and the identity of the vectors is pruned (they live in different spaces); the theological reading of the operator is not a kernel term. "''')
a.troca('''"The pair of psions on the Fock face stays open as a LINK to be made (errata E21 of v408), from v410 onward (D60). The Omega of the light psion as the uniform state of the instance stays open: same form, not a bridge. "''',
        '''"The pair of psions on the Fock face is LINKED in this version (`ParNaFaceDeFock`: in sector two of the concrete Fock space of light the pair has norm one, is orthogonal to the vacuum, and its marginal is one half of the projection, the same Half-Nat as the finite Bell pair, in distinct spaces); errata E21 of v408 goes beside it. "
    "The bridge between the Omega of the light psion and the uniform state of the instance is the inscription; the identity of the vectors is pruned. With the reader that only counts, the full equality is not a theorem here (E28) [OPEN]. "''')
a.troca('''"and E26 goes beside the sealed registry of v408, whose text is not rewritten.''', '''"E26 and E21 go beside the sealed registries of v408, whose text is not rewritten, and E28 corrects a phrase of the management on the equality with the reader that only counts.''')
a.troca('''"The custody of v409 (complete round): the translation to the classes of Turing. %(modulos)d new kernel module (" + NOMES_ASCII + ", name given by the management and ratified by the operator), %(bandeiras)d new flags,''',
        '''"The custody of v409 (complete round): the translation to the classes of Turing and the pair on the Fock face. %(modulos)d new kernel modules (" + NOMES_ASCII + ", names given by the management), %(bandeiras)d new flags,''')
a.troca('''Z is the reader mode. No old key changes. Validity in the kernel is not accreditation; the gate did not move. Not falsified is not the word of accreditation.")''',
        '''Z is the reader mode. The pair on the Fock face is linked. No old key changes. Validity in the kernel is not accreditation; the gate did not move. Not falsified is not the word of accreditation.")''')
a.troca('''"A custódia da v409 (rodada completa): a tradução às classes de Turing. %(modulos)d módulo novo no kernel (" + NOMES_ASCII + ", nome da gerência ratificado pelo operador), %(bandeiras)d bandeiras novas,''',
        '''"A custódia da v409 (rodada completa): a tradução às classes de Turing e o par na face de Fock. %(modulos)d módulos novos no kernel (" + NOMES_ASCII + ", nomes da gerência), %(bandeiras)d bandeiras novas,''')
a.troca('''Z é o modo leitor. Nenhuma chave antiga muda. Validade no kernel não é creditação;''', '''Z é o modo leitor. O par na face de Fock está ligado. Nenhuma chave antiga muda. Validade no kernel não é creditação;''')
a.troca('''"A traducao as classes de Turing: P = nP e teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor fica fora (a fita sem escala). %(modulos)d modulo novo (" + NOMES_ASCII + ", nome da gerencia ratificado pelo operador), %(bandeiras)d bandeiras, "''',
        '''"A traducao as classes de Turing e o par na face de Fock: P = nP e teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor fica fora (a fita sem escala). %(modulos)d modulos novos (" + NOMES_ASCII + ", nomes da gerencia), %(bandeiras)d bandeiras, "''')
a.troca('''nenhuma chave antiga muda; o par na face de Fock segue em aberto. Validade no kernel nao e creditacao; o gate nao se moveu.") % N + REV_COMMIT''',
        '''nenhuma chave antiga muda; o par na face de Fock ligado. Validade no kernel nao e creditacao; o gate nao se moveu.") % N + REV_COMMIT''')
a.troca('''"o alcance é relativo ao leitor e a máquina sem leitor fica fora; o par de psíons na face de Fock segue em aberto como ligação; nenhuma chave antiga muda; validade no kernel não é creditação):**\\n")''',
        '''"o alcance é relativo ao leitor e a máquina sem leitor fica fora; o par de psíons na face de Fock está ligado nesta versão; nenhuma chave antiga muda; validade no kernel não é creditação):**\\n")''')
a.grava()
