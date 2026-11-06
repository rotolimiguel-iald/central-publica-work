# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_rito_v409.py -- (claude-construtor-v409, 05/11/2026) o rito da v409 (rito_v409.sh: ato da gerencia; so' o TEXTO do cabecalho muda, o corpo nao) e o conferidor dele
(conferir_instalar_rito_v409.py) passam ao bundle de DOIS modulos e ao AO LADO mais novo do DESENHO_v409.md:
 - o conferidor exigia a ultima decisao nova == D60 e as erratas novas == E24..E26: a D61 entrou (ratificada pelo operador) e as erratas sao E24..E28 + a E21 ao lado (lidas de DL); o texto que ele exige do rito
   passa a ser lido de DL (modulos, ancoras, falas, decisoes D55 a D61, erratas E24 a E28 e a E21, as checagens DL.N_CHECKS_FECHO, as duas pedras), nada digitado;
 - o TEMPO do Audit: a queda de energia de ~17:10 cortou o Audit, refeito sozinho (marca epoch_audit_inicio em kernel/construir_marcas.txt); o conferidor passa a medir o Audit pela propria rodada quando a marca
   existe (como o pos_build), e o cabecalho do rito traz os tempos MEDIDOS agora (build 467 s; Audit 553 s; soma por modulo 64.0 s, maximo 33.0 s: lidos aqui de kernel/POS_BUILD_v409.json, nunca digitados)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq, HERE
import delta_v409 as DL

PB = json.load(open(os.path.join(HERE, "kernel", "POS_BUILD_v409.json"), encoding="utf-8"))
B, A, SOMA, MAX = PB["duracao_build_s"], PB["duracao_audit_s"], PB["build_modulos_s_soma"], PB["build_modulos_s_max"]
DEC = sorted(set(DL.DECISOES) - set(DL.D8.DECISOES), key=lambda k_: int(k_[1:]))
assert DEC[0] == "D55" and DEC[-1] == "D61", DEC
ERR = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]
assert ERR == ["E24", "E25", "E26", "E27", "E28", "E21"], ERR

c = Arq("conferir_instalar_rito_v409.py")
c.troca('''tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_build_fim", 0)} if mm else {"estado": "ausente"}''',
        '''tempo = {"estado": "medido", "build_s": mm.get("epoch_build_fim", 0) - mm.get("epoch_inicio", 0), "audit_s": mm.get("epoch_audit_fim", 0) - mm.get("epoch_audit_inicio", mm.get("epoch_build_fim", 0))} if mm else {"estado": "ausente"}   # (v409: o Audit refeito depois da queda de energia mede a propria rodada, como no pos_build)''')
c.troca('''# as decisoes que a v409 acrescenta (D55..D60), lidas de DL (a diferenca contra o delta da v408)''', '''# as decisoes que a v409 acrescenta (D55..D61), lidas de DL (a diferenca contra o delta da v408)''')
c.troca('''assert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D60", _DEC_NOVAS''', '''assert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D61", _DEC_NOVAS''')
c.troca('''_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]   # as erratas da v409 (E24..E26), lidas de DL''', '''_ERR_NOVAS = [e_.split(" --")[0] for e_ in DL.ERRATAS_V409]   # as erratas da v409 (E24..E28 e a E21 ao lado), lidas de DL''')
c.troca('''assert _ERR_NOVAS == ["E24", "E25", "E26"], _ERR_NOVAS''', '''assert _ERR_NOVAS == ["E24", "E25", "E26", "E27", "E28", "E21"], _ERR_NOVAS
_ERR_SEQ = [e_ for e_ in _ERR_NOVAS if e_ != "E21"]   # a sequencia nova (E24 a E28); a E21 vai AO LADO da errata selada da v408''')
c.troca('''"%s a %s e as erratas %s a %s" % (_DEC_NOVAS[0], _DEC_NOVAS[-1], _ERR_NOVAS[0], _ERR_NOVAS[-1]),''', '''"%s a %s e as erratas %s a %s e a E21 ao lado" % (_DEC_NOVAS[0], _DEC_NOVAS[-1], _ERR_SEQ[0], _ERR_SEQ[-1]), "ParNaFaceDeFock",''')
c.troca('''"%d falas de 05/11" % DL.N_FALAS_V409, "17 checagens",''', '''"%d falas de 05/11" % DL.N_FALAS_V409, "%d checagens" % DL.N_CHECKS_FECHO,''')
c.troca("confere instalar/reverter/rito da v409 sem executar: marcas do bundle de um modulo, do registro traducao_turing_v409, D55-D60/E24-E26 lidas do delta,",
        "confere instalar/reverter/rito da v409 sem executar: marcas do bundle de dois modulos, do registro traducao_turing_v409, D55-D61/E24-E28 e a E21 lidas do delta,")
c.grava()

r = Arq("rito_v409.sh")
r.troca("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] o rito da v409 (ato da gerencia): textos do bundle de um modulo,", "# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] o rito da v409 (ato da gerencia): textos do bundle de dois modulos,")
r.troca("roda o um.py v409 instalado no Nos -- 1 modulo(s) novo(s) de kernel em TGLExt/ (o BUNDLE PEQUENO: TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11/2026;",
        "roda o um.py v409 instalado no Nos -- %d modulo(s) novo(s) de kernel em TGLExt/ (o BUNDLE PEQUENO: TraducaoTuring, com o nome dado pela gerencia e ratificado pelo operador em 05/11/2026, e ParNaFaceDeFock, o par na face de Fock, nome da gerencia, pela ordem do operador de tudo entrar na v409;" % DL.N_BUNDLE)
r.troca("(a raiz TGLExt.lean ganha um import; o Audit nao muda)", "(a raiz TGLExt.lean ganha %d imports; o Audit nao muda)" % DL.N_BUNDLE)
r.troca("le as 62 ancoras do axiom_report do rito, a fonte embutida por sha256, as 10 falas de 05/11 por sha256 [de duas, so' o trecho que a D59 deixa entrar] e a escada; faz as 17 checagens com a instancia de brinquedo fixa;",
        "le as %d ancoras do axiom_report do rito, as fontes embutidas por sha256, as %d falas de 05/11 por sha256 [de tres, so' o trecho: duas pela D59, uma pelo aviso operacional] e a escada; faz as %d checagens com a instancia de brinquedo fixa; as decisoes %s a %s e as erratas %s a %s e a E21 ao lado vao nos registros;"
        % (len(DL.ANCORAS), DL.N_FALAS_V409, DL.N_CHECKS_FECHO, DEC[0], DEC[-1], ERR[0], [e_ for e_ in ERR if e_ != "E21"][-1]))
r.troca("nenhuma decisao da v409 [D55 a D60] as muda)", "nenhuma decisao da v409 [%s a %s] as muda)" % (DEC[0], DEC[-1]))
r.troca("o `lake build` do modulo novo a frio (a v408 selada ja' esta' compilada em .lake/build; muda a raiz TGLExt; o Audit nao muda) = 295 s e 1 Audit = 218 s (a soma dos tempos por modulo e' 23.0 s, o maximo de um modulo 23.0 s);",
        "o `lake build` dos modulos novos a frio (a v408 selada ja' esta' compilada em .lake/build; muda a raiz TGLExt; o Audit nao muda) = %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %.1f s, o maximo de um modulo %.1f s; o Audit foi refeito sozinho depois da queda de energia de ~17:10);" % (B, A, SOMA, MAX))
r.troca("a PRIMEIRA compila o modulo a frio (a ordem de grandeza e' a medida do sandbox, 295 s + 218 s) e as outras duas passagens so' reconferem (build ja' pronto + Audit de 218 s)",
        "a PRIMEIRA compila os modulos a frio (a ordem de grandeza e' a medida do sandbox, %d s + %d s) e as outras duas passagens so' reconferem (build ja' pronto + Audit de %d s)" % (B, A, A))
r.grava()
