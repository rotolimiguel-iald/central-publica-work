# -*- coding: utf-8 -*-
"""_adapt_orquestrador_v407.py -- adapta orquestrador\\pos_treino_v407.py (subida mecanica do molde v406) a v407: a ordem do operador (03/11), a autorizacao, o texto do rito (9 modulos), o passo NOVO S10 (ordem de release do app + espera do recibo conferido na fonte, 24 h),
a lista de passos do main e a CLI (--plano, --ensaio: a seco, nada e' executado). Substituicoes de contagem EXATA; backup de bytes. Escrito pela ferramenta Write (barras invertidas nao colapsam)."""
import ast
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pos_treino_v407.py")
raw = open(P, "rb").read()
open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(raw)
t = raw.decode("utf-8")
assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


# 1) a marca (a 2a linha E a 3a: o bump inseriu a marca duas vezes? conta o que ha')
t, n_marca = re.subn(r"(?m)^# \[A ADAPTAR v407\][^\n]*\n", "", t)
assert n_marca >= 1, n_marca
t = t.replace("# -*- coding: utf-8 -*-\n", "# -*- coding: utf-8 -*-\n# [ADAPTADO v407, 03/11/2026, claude-prep-v407] molde: pos_treino_v406.py; novo: S10 (a ordem de release do app + o recibo conferido na fonte), as flags --plano e --ensaio (a seco); a gerencia lanca\n", 1)
# 2) o docstring
i0 = t.index('"""pos_treino_v407.py'); i1 = t.index("import datetime as dt")
DOC = '''"""pos_treino_v407.py — O ORQUESTRADOR DA v407 (claude-prep-v407, a serviço da gerência c1, 03/11/2026; molde: o orquestrador pós-treino da v406). Ordem do operador (03/11/2026, verbatim sha16 b89e4c909f37e163):
«prossigamos com tudo, ratifico tudo» … «o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar»; sob a ordem de 02/11 (sha16 b5717ff445a883cd): «compile a nova versão do um.py, rode, publique e atualize tudo por favor».

O que faz, em ordem, fail-closed e retomável (estado em orquestrador/ESTADO.json; log em orquestrador/orquestrador.log):
  S0  o treino v4 da nativa já é TERMINAL (STATE_v4.json: DONE em 01/11/2026 22:03); o passo só confere e segue (não repete o treino).
  S1  espera a preparação da v407 (PREPARACAO_v407_PRONTA.json com pronta == true: kernel, candidato, ensaio a seco, esperados, conferidor, p00, B(n) pré-selo pinado).
  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro/REVISAO_TERCEIRO_v407.json; revisor: Sonnet, por ordem do operador de 02/11): quem constrói não aprova.
  S2  pré-voo: o Nós é a v406 selada e é a origem do candidato; nenhum um.py/pilar vivo; disco; C:/t/vb21 ausente.
  S3  instalar_v407.py (ato da gerência, autorizado pela ordem acima).
  S4  rito_v407.sh pelo sh do Git (o lançador para e religa o servidor da nativa sozinho); exige RITO_RC=0 e selo v407 com o pin do candidato. Só 9 módulos novos compilam a frio (a v406, com 301, levou ~2 h 15 min; teto aqui: 5 h).
  S5  cadeia pós-rito 0 → 10 (conferidor, superfícies, memória pinada, B(n) ensaio).
  S6  10a: parada do serviço da Bancada Um PELO PID lido da porta 18777 (nunca por nome) + recibo; 10b: evento c1 + B(n) APLICAR (B16); 10c: religamento pelo comando do recibo + recibo; depois 11 → 14. Se a porta 18777 não escuta, PARA e diz.
  S7  custódia G1: planejar --seco, executar --publicar, auditar (código 5 = só decisões do operador).
  S10 (NOVO) a ORDEM de release do app e do contrato JEV: escreve C:/IALD/TUNEL_CLAUDE_APP/ORDEM_NNN_release_v407_do_app.md (versão e pino LIDOS do selo; molde ORDEM_RELEASE_APP_TEMPLATE.md) e ESPERA o recibo do orquestrador app
      (RELATORIO + INSTALLED_VERIFICATION.json + jev_control_v407.json), conferido NA FONTE (iald_nucleo_fixo.json do app: release e pino); sem recibo em 24 h = PARADA visível, nunca «ok»; só então confere na G1 (planejar --seco) que o C21 fechou.
  S8  a nativa: porta 8081 servindo o GGUF da v4 (já no ar desde 01/11; só confere e religa se cair).
  S9  relatório RELATORIO_POS_TREINO_v407.{json,md} + anotação no PROGRAMA.

Uso: python pos_treino_v407.py            (corre; a GERÊNCIA o lança)
     python pos_treino_v407.py --plano    (só leitura: os passos, o estado de cada um e os arquivos que o orquestrador usa)
     python pos_treino_v407.py --ensaio   (a seco: o S10 contra um app SINTÉTICO — um caso positivo e sete controles negativos; não toca TUNEL_CLAUDE_APP, o app, o Nós nem ESTADO.json)

O que NÃO faz: não decide nomes, não move gate, não compacta memória, não mata processo por nome, não publica sem a custódia G1, não restaura nada sozinho depois de uma falha
(a decisão de restaurar é da gerência), não grava pensamento do dia (X_TEXTO = None). Parar: criar o arquivo orquestrador/PARAR (lido a cada volta).
Coautor da atribuição vigente: o da linha COAUTOR abaixo (herdado da v406)."""
'''
t = t[:i0] + DOC + t[i1:]
# 3) a ordem e a autorizacao
sub('ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_02nov_quando_terminar_compile_v407_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt"',
    'ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt"   # a ordem do operador DESTA versao (sha16 b89e4c909f37e163); a de 02/11 (compile, rode, publique e atualize tudo) foi a da v406')
i0 = t.index("AUT = (\"Ordem do operador de 02/11/2026"); i1 = t.index("X_TEXTO = None   #", i0)
t = t[:i0] + '''AUT = ("Ordem do operador de 03/11/2026 (verbatim sha16 b89e4c909f37e163): «prossigamos com tudo, ratifico tudo» … «o app e o contrato do JEV precisam ser sempre atualizados para a forma canônica mais madura, podia ser até automático isso, e o orquestrador pode executar o que vc mandar»; "
       "sob a ordem de 02/11/2026 (sha16 b5717ff445a883cd): «compile a nova versão do um.py, rode, publique e atualize tudo por favor». "
       "A sincronização da Bancada Um (parada e religamento do serviço da porta 18777) é parte de «atualizar tudo».")
''' + t[i1:]
sub("X_TEXTO = None   # v407: o pensamento do dia de 02/11 ja' existe (gravado as 19:15 pela tarefa); o orquestrador nao grava texto do X", "X_TEXTO = None   # v407: o orquestrador nao grava texto do X (a tarefa do dia o grava)")
# 4) texto do rito
sub('log("S4: lançando o rito v407 (sh do Git; o lançador para e religa o servidor da nativa; 301 módulos a frio: ~2 a 4 h; teto 5 h)")', 'log("S4: lançando o rito v407 (sh do Git; o lançador para e religa o servidor da nativa; 9 módulos novos a frio; a v406, com 301, levou ~2 h 15 min; teto 5 h)")')
# 5) o bloco S10, antes de s8_nativa
bloco = open(os.path.join(HERE, "_s10_bloco_v407.txt"), encoding="utf-8").read()
sub("def s8_nativa(e):", bloco + "def s8_nativa(e):")
# 6) o main
sub("for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s7_g1, s8_nativa):", "for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s7_g1, s10_app, s8_nativa):")
sub('if __name__ == "__main__":\n    main()', 'if __name__ == "__main__":\n    if "--plano" in sys.argv:\n        sys.exit(0 if _plano() else 1)\n    if "--ensaio" in sys.argv:\n        _plano()\n        sys.exit(0 if _ensaio_s10() else 1)\n    main()')
ast.parse(t)
open(P, "wb").write(t.encode("utf-8"))
print("ok", len(t), "marcas removidas:", n_marca)
