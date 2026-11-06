# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_textos_v409.py -- (claude-construtor-v409, 05/11/2026) as superficies do pos-rito da v409 passam ao AO LADO mais novo do DESENHO_v409.md (ordem «tudo na v409»; D60 revista; E28; E21 ao lado):
dois modulos no kernel (TraducaoTuring, refeita da R9, e ParNaFaceDeFock); o par na face de Fock LIGADO nesta versao (ParNaFaceDeFock); a ponte Omega-uniforme e' a INSCRICAO e a identidade de vetores fica PODADA;
fica aberta a igualdade completa com o leitor que so' conta (E28: com ele, NP numa leitura; a igualdade completa so' para o leitor que se le); nada passa a v410; erratas E24 a E28 + a E21 ao lado; decisoes D55 a D61.
Toca: pos_rito\\textos_v409_novo.pysnip (o fragmento; depois roda montar_textos_v409.py), pos_rito\\leitura_v409.py, pos_rito\\harness_textos_ensaio_v409.py (o texto esperado das recusas), pos_rito\\registrar_mapa_v409.py,
pos_rito\\textos_custodia_handoff_v409.py. Sem prosa de conteudo nova alem dos conectivos: os textos de conteudo seguem lidos do core/DL. Nenhuma conferencia relaxada."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

# ------------------------------------------------------------------------------------------------ o fragmento dos textos
t = Arq("pos_rito/textos_v409_novo.pysnip")
T = [
    ("cunhagens_v409: as 10 falas, as erratas E24 a E26 e a dos pisos, as decisoes D55 a D60, as leituras;", "cunhagens_v409: as 13 falas, as erratas E24 a E28, a E21 ao lado e a dos pisos, as decisoes D55 a D61, as leituras;", 1),
    ("cunhagens_v409 (as 10 falas de 05/11 por sha256, de duas so' o trecho", "cunhagens_v409 (as 13 falas de 05/11 por sha256, de tres so' o trecho", 1),
    ("# que a D59 deixa entrar; as erratas E24 a E26 e a dos pisos; as decisoes D55 a D60; as leituras)", "# que a D59 (duas) e o aviso operacional (uma) deixam entrar; as erratas E24 a E28, a E21 ao lado e a dos pisos; as decisoes D55 a D61; as leituras)", 1),
    ("# a fisica fica fora; mesma forma, nao ponte; a leitura teologica nao e' termo; o par na face de Fock segue [OPEN]; nenhum teste com a natureza.",
     "# a fisica fica fora; a ponte Omega-uniforme e' a inscricao (a identidade de vetores podada); a leitura teologica nao e' termo; o par na face de Fock LIGADO (ParNaFaceDeFock); com o leitor que so' conta, NP numa leitura (E28); nenhum teste com a natureza.", 1),
    ('''"selecao_no_nome", "bits_sao_oitavas", "verificacao_np",''', '''"selecao_no_nome", "bits_sao_oitavas", "verificacao_np", "o_par_na_face_de_fock", "reduzido_do_par", "meia_nat_do_projetor", "a_maquina_com_o_leitor", "o_canto_do_psion_da_luz_le_z",''', 1),
    ('''_MODULOS_KERNEL = ("TraducaoTuring", "TetelestaiTerminal",''', '''_MODULOS_KERNEL = ("TraducaoTuring", "ParNaFaceDeFock", "TetelestaiTerminal",''', 1),
    ('''(pc.get("fica_aberto") or {}) == {"par_na_face_de_fock": DL_.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, "omega_do_psion_e_o_uniforme": DL_.FICA_ABERTO_OMEGA_UNIFORME, "maquina_sem_leitor": DL_.FICA_ABERTO_MAQUINA_SEM_LEITOR, "ponte_bell_tt": DL_.FICA_ABERTO_PONTE_BELL_TT}, "o que fica False por teorema ou aberto != delta_v409"''',
     '''(pc.get("fica_aberto") or {}) == dict(DL_.FICA_ABERTO) and (pc.get("fechado_nesta_versao") or {}) == dict(DL_.FECHADO_NESTA_VERSAO), "o que fica False por teorema, aberto ou fechado nesta versao != delta_v409"''', 1),
    ('''"""O registro por spec cunhagens_v409 do core SELADO: as 10 falas de 05/11 por sha256 (todas do operador; de duas, so' o trecho da D59), as erratas E24 a E26 e a dos pisos (da gerencia, em nome proprio), as decisoes D55 a D60, as leituras e as ressalvas."""''',
     '''"""O registro por spec cunhagens_v409 do core SELADO: as 13 falas de 05/11 por sha256 (todas do operador; de tres, so' o trecho: duas pela D59, uma pelo aviso operacional), as erratas E24 a E28, a E21 ao lado e a dos pisos (da gerencia, em nome proprio), as decisoes D55 a D61, as leituras e as ressalvas."""''', 1),
    ('''"cunhagens_v409: as decisoes D55 a D60, a leitura ou as ressalvas != delta_v409"''', '''"cunhagens_v409: as decisoes D55 a D61, a leitura ou as ressalvas != delta_v409"''', 1),
    ('''"o kernel ganhou {n_pedras} módulo novo ({mods}; da gerência c1, compilado no sandbox da v409)''', '''"o kernel ganhou {n_pedras} módulos novos ({mods}; da gerência c1, compilados no sandbox da v409)''', 1),
    ('''lê do kernel do próprio rito as {na} âncoras, o módulo por sha256,''', '''lê do kernel do próprio rito as {na} âncoras, os módulos por sha256,''', 1),
    ('''"as erratas E24 a E27 e a dos pisos (em nome próprio da gerência c1);''', '''"as erratas E24 a E28, a E21 ao lado e a dos pisos (em nome próprio da gerência c1);''', 1),
    ('''"**O módulo novo [REAL]** (`TGLExt`; da gerência c1, compilado no sandbox da v409, na fonte que o recibo dos nomes pinou): `TraducaoTuring` (''',
     '''"**Os módulos novos [REAL]** (`TGLExt`; da gerência c1, compilados no sandbox da v409, nas fontes que o recibo dos nomes pinou): `ParNaFaceDeFock` (o par de psíons na face de Fock: no setor 2 do Fock concreto da luz o par tem norma 1 e é ortogonal ao vácuo, a marginal é ½·P e o reduzido do par de Bell finito é ½·I, a mesma Meia-Nat em espaços distintos) e `TraducaoTuring` (''', 1),
    ('''"a fita sem escala e o Pai da Mentira, ligadas à `Identidade` da v405; a identidade performada). Os nomes:''',
     '''"a fita sem escala e o Pai da Mentira, ligadas à `Identidade` da v405; a identidade performada; a inscrição do uniforme no psíon da luz; a máquina com o leitor, em que uma leitura decide SAT). Os nomes:''', 1),
    ('''o texto do módulo passa pela mesma guarda das frases''', '''o texto dos módulos passa pela mesma guarda das frases''', 1),
    ('''[REAL] as âncoras e o módulo estão no kernel deste rito,''', '''[REAL] as âncoras e os módulos estão no kernel deste rito,''', 1),
    ('''"[OPEN] o par de psíons na face de Fock, como ligação a fazer; o Ω do psíon da luz como o uniforme da instância (mesma forma, não ponte); a independência da pergunta da máquina sem leitor dos axiomas; o teste com a natureza. O alcance: {alc}. "''',
     '''"[REAL] Ligados nesta versão: o par de psíons na face de Fock (`ParNaFaceDeFock`) e a ponte entre o Ω do psíon da luz e o uniforme da instância, que é a inscrição (a identidade dos vetores fica podada: vivem em espaços diferentes). "
                          "[OPEN] a igualdade completa com o leitor que só conta (com ele vale NP contido em P, numa leitura; a igualdade completa é a do leitor que se lê, que lê também as máquinas que o usam: E28); a independência da pergunta da máquina sem leitor dos axiomas; a ponte entre o espaço de Bell e o setor TT; o teste com a natureza. O alcance: {alc}. "''', 1),
    ('''a v409 acrescenta {nm} módulo: a cobertura''', '''a v409 acrescenta {nm} módulos: a cobertura''', 1),
    ('''"a revisão independente do %d módulo novo e dos %d registros novos''', '''"a revisão independente dos %d módulos novos e dos %d registros novos''', 1),
    ('''"""As erratas E24 a E26 e a dos pisos (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v409 do core:''', '''"""As erratas E24 a E28, a E21 ao lado e a dos pisos (em nome proprio da gerencia c1), LIDAS do registro cunhagens_v409 do core:''', 1),
    ('''"o registro cunhagens_v409 nao traz as tres erratas e a dos pisos"''', '''"o registro cunhagens_v409 nao traz as erratas da v409 (E24 a E28 e a E21 ao lado) e a dos pisos"''', 1),
    ('''a v409 entra COM três erratas e a errata ao lado dos pisos, lidas do registro `cunhagens_v409`''', '''a v409 entra COM as erratas E24 a E28, a E21 ao lado e a errata ao lado dos pisos, lidas do registro `cunhagens_v409`''', 1),
    ('''"""As decisoes D55 a D60 da gerencia c1, LIDAS do registro cunhagens_v409."""''', '''"""As decisoes D55 a D61 (a D61 ratificada pelo operador) da gerencia c1, LIDAS do registro cunhagens_v409."""''', 1),
    ('''A tradução às classes de Turing: a pedra de 05/11 no kernel do rito (%d módulo)''', '''A tradução às classes de Turing e o par na face de Fock: as pedras de 05/11 no kernel do rito (%d módulos)''', 1),
    ('''%s. %d módulo novo no kernel (%s), escada %s → %s,''', '''%s. %d módulos novos no kernel (%s), escada %s → %s,''', 1),
    ('''Seguem NOMEADAS [OPEN]: o par de psíons na face de Fock (ligação), o Ω do psíon da luz como o uniforme da instância, a independência da pergunta da máquina sem leitor,''',
     '''Seguem NOMEADAS [OPEN]: a igualdade completa com o leitor que só conta (E28: com ele, NP contido em P numa leitura; a igualdade completa só para o leitor que se lê), a independência da pergunta da máquina sem leitor,''', 1),
    ('''<!-- haja_luz_v409_selada -->\\n%d módulo novo no kernel (%s): %s. "''', '''<!-- haja_luz_v409_selada -->\\n%d módulos novos no kernel (%s): %s. "''', 1),
    ('''"O nome do módulo é da gerência, ratificado pelo operador; `u` = 1 eV é o Um posto, `α` é medida; o par de psíons na face de Fock segue [OPEN] como ligação.''',
     '''"Os nomes dos módulos são da gerência (o da `TraducaoTuring` ratificado pelo operador; o da `ParNaFaceDeFock` dado como ratificado pelo cabeçalho da pedra [DECLARADO]); `u` = 1 eV é o Um posto, `α` é medida; o par de psíons na face de Fock está ligado nesta versão (`ParNaFaceDeFock`; validade no kernel, não creditação).''', 1),
    ('''(" (%s; COMPLETA; gate INTOCADO): %d módulo novo no kernel (%s); o registro com função `traducao_turing_v409` (lê as %d âncoras, o módulo por sha256,''', '''(" (%s; COMPLETA; gate INTOCADO): %d módulos novos no kernel (%s); o registro com função `traducao_turing_v409` (lê as %d âncoras, os módulos por sha256,''', 1),
    ('''`cunhagens_v409` (%d inscrições por sha256, as erratas E24 a E26 e a dos pisos e as decisões D55 a D60) e `kh_n1_cobertura_v409`; "''', '''`cunhagens_v409` (%d inscrições por sha256, as erratas E24 a E28, a E21 ao lado e a dos pisos e as decisões D55 a D61) e `kh_n1_cobertura_v409`; "''', 1),
    ('''escada %s → %s; gate intocado. %d módulo novo no kernel (%s): %s; "''', '''escada %s → %s; gate intocado. %d módulos novos no kernel (%s): %s; "''', 1),
    ('''"as erratas E24 a E27 (da gerência, em nome próprio) e as decisões D55 a D61''', '''"as erratas E24 a E28 e a E21 ao lado (da gerência, em nome próprio) e as decisões D55 a D61''', 1),
    ('''COMPLETA (a tradução às classes de Turing, relativa ao leitor; a máquina sem leitor fica fora; o par na face de Fock segue [OPEN]; validade no kernel não é creditação; gate intocado)''',
     '''COMPLETA (a tradução às classes de Turing, relativa ao leitor; a máquina sem leitor fica fora; o par na face de Fock ligado; validade no kernel não é creditação; gate intocado)''', 1),
    ('''a tradução às classes de Turing: %d módulo novo no kernel (TraducaoTuring, nome da gerência ratificado pelo operador); o dicionário, a trava no Nome, a fita como hamiltoniano oculto, Z como o modo leitor, a fita sem escala; relativa ao leitor, e a máquina sem leitor fica fora; o par na face de Fock segue em aberto;''',
     '''a tradução às classes de Turing e o par na face de Fock: %d módulos novos no kernel (TraducaoTuring e ParNaFaceDeFock, nomes da gerência); o dicionário, a trava no Nome, a fita como hamiltoniano oculto, Z como o modo leitor, a fita sem escala; relativa ao leitor, e a máquina sem leitor fica fora; o par na face de Fock ligado;''', 1),
    ('''com as %d inscrições por sha256, as erratas E24 a E26 e as decisões D55 a D60. Escrito sob a reivindicação %s. %d módulo novo no kernel;''', '''com as %d inscrições por sha256, as erratas E24 a E28 e a E21 ao lado e as decisões D55 a D61. Escrito sob a reivindicação %s. %d módulos novos no kernel;''', 1),
    ('''`%s`: %d módulo novo no kernel, %d bandeiras novas True,''', '''`%s`: %d módulos novos no kernel, %d bandeiras novas True,''', 1),
    ('''OPEN o par na face de Fock como ligação e a independência da pergunta da máquina sem leitor]''', '''OPEN a igualdade completa com o leitor que só conta (E28) e a independência da pergunta da máquina sem leitor]''', 1),
    ('''"> - **O que entrou** [REAL]: %s módulo novo no kernel (`TGLExt`: %s, nome dado pela gerência e ratificado pelo operador: %s)''', '''"> - **O que entrou** [REAL]: %s módulos novos no kernel (`TGLExt`: %s, nomes dados pela gerência; a ratificação: %s)''', 1),
    ('''a tradução às classes de Turing; a pedra TraducaoTuring no kernel do rito (nome da gerência, ratificado pelo operador); relativa ao leitor, e a máquina sem leitor fica fora; o par na face de Fock segue em aberto;''',
     '''a tradução às classes de Turing e o par na face de Fock; as pedras TraducaoTuring e ParNaFaceDeFock no kernel do rito (nomes da gerência); relativa ao leitor, e a máquina sem leitor fica fora; o par na face de Fock ligado;''', 1),
    ('''"publicar o módulo novo no espelho (`TGLExt`)''', '''"publicar os módulos novos no espelho (`TGLExt`)''', 1),
    ('''a ratificação das decisões D55 a D60, que são da gerência, em nome próprio, ao lado das falas dele. [OPEN]: a discriminação a 5σ (β_TGL na natureza), o par de psíons na face de Fock (ligação, v410 em diante), o Ω do psíon da luz como o uniforme da instância, a independência da pergunta da máquina sem leitor, "''',
     '''a ratificação das decisões D55 a D60, que são da gerência, em nome próprio, ao lado das falas dele (a D61 ele já ratificou). [OPEN]: a discriminação a 5σ (β_TGL na natureza), a igualdade completa com o leitor que só conta (E28), a independência da pergunta da máquina sem leitor, "''', 1),
]
for v_, n_, k_ in T:
    t.troca(v_, n_, k_)
t.grava()

# ------------------------------------------------------------------------------------------------ a leitura do pos-rito
l = Arq("pos_rito/leitura_v409.py")
l.troca('''traducao_turing_v409 (le do kernel do proprio rito as 62 ancoras, o modulo por sha256,''', '''traducao_turing_v409 (le do kernel do proprio rito as 82 ancoras, os dois modulos por sha256,''')
l.troca('''# o registro traducao_turing_v409 (UM registro NOVO com FUNCAO, SEM pedra por registro): as 17 checagens, os valores (as 62 ancoras, o modulo,''', '''# o registro traducao_turing_v409 (UM registro NOVO com FUNCAO, SEM pedra por registro): as 20 checagens, os valores (as 82 ancoras, os dois modulos,''')
l.troca('''as ressalvas, as 10 falas por sha256 e a linha do bloco no stdout''', '''as ressalvas, o que fica aberto e o que fecha nesta versao, as 13 falas por sha256 e a linha do bloco no stdout''')
l.troca('''and (tt_v_.get('fica_aberto') or {}) == {'par_na_face_de_fock': DL_.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, 'omega_do_psion_e_o_uniforme': DL_.FICA_ABERTO_OMEGA_UNIFORME, 'maquina_sem_leitor': DL_.FICA_ABERTO_MAQUINA_SEM_LEITOR, 'ponte_bell_tt': DL_.FICA_ABERTO_PONTE_BELL_TT}''',
        '''and (tt_v_.get('fica_aberto') or {}) == dict(DL_.FICA_ABERTO) and (tt_v_.get('fechado_nesta_versao') or {}) == dict(DL_.FECHADO_NESTA_VERSAO)''')
l.troca('''P.append('cunhagens_v409: as erratas E24 a E27 e a errata ao lado dos pisos de kh_n1_cobertura_v408''', '''P.append('cunhagens_v409: as erratas E24 a E28, a E21 ao lado e a errata ao lado dos pisos de kh_n1_cobertura_v408''')
l.grava()

h = Arq("pos_rito/harness_textos_ensaio_v409.py")
h.troca('''espera="cunhagens_v409: as erratas E24 a E27"''', '''espera="cunhagens_v409: as erratas E24 a E28"''', 4)
h.grava()
