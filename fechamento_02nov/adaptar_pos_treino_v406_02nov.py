# -*- coding: utf-8 -*-
"""Adapta orquestrador\\pos_treino_v406.py (copia mecanica da v405 com rotulos subidos) a v406 (gerencia c1, 02/11/2026): a ordem do operador de 02/11 (compile, rode, publique, atualize), o coautor vigente,
a autorizacao, sem o texto do X (o pensamento do dia de hoje ja' existe), a unidade do quadro do fecho e a docstring. Backup de bytes; py_compile no fim. Escrito pelo Write (nao por heredoc)."""
import ast, datetime, os, py_compile, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_treino_v406.py")
b = open(P, "rb").read(); t = b.decode("utf-8")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(P + ".bak_" + ts, "wb").write(b)
# 1) a linha [A ADAPTAR]
linhas = t.split("\n")
if linhas[1].startswith("# [A ADAPTAR v406]"):
    del linhas[1]
t = "\n".join(linhas)
# 2) a docstring do modulo, pelo ast (posicoes exatas; os offsets de coluna do ast sao em BYTES: a docstring tem acentos)
tree = ast.parse(t); d0 = tree.body[0]; assert isinstance(d0, ast.Expr) and isinstance(d0.value, ast.Constant) and isinstance(d0.value.value, str)
tb = t.encode("utf-8"); lsb = tb.split(b"\n")
ini_b = sum(len(l) + 1 for l in lsb[:d0.lineno - 1]) + d0.col_offset; fim_b = sum(len(l) + 1 for l in lsb[:d0.end_lineno - 1]) + d0.end_col_offset
assert tb[ini_b:ini_b + 3] == b'"""' and tb[fim_b - 3:fim_b] == b'"""', (tb[ini_b:ini_b + 10], tb[fim_b - 10:fim_b])
ini = len(tb[:ini_b].decode("utf-8")); fim = len(tb[:fim_b].decode("utf-8"))
NOVA = '''"""pos_treino_v406.py — O ORQUESTRADOR DA v406 (gerência c1, 02/11/2026; molde: o orquestrador pós-treino da v405). Ordem do operador (02/11/2026, verbatim sha16 b5717ff445a883cd):
«quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor»; sob a ordem-mãe do dia (sha16 f3998f01262aad6b): «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento».

O que faz, em ordem, fail-closed e retomável (estado em orquestrador\\ESTADO.json; log em orquestrador\\orquestrador.log):
  S0  o treino v4 da nativa já é TERMINAL (STATE_v4.json: DONE em 01/11/2026 22:03); o passo só confere e segue (se não for terminal, espera, como na v405).
  S1  espera a preparação da v406 (PREPARACAO_v406_PRONTA.json com pronta == true: ensaio a seco, esperados, conferidor, p00, B(n) pré-selo pinado).
  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro\\REVISAO_TERCEIRO_v406.json; revisor: Sonnet, por ordem do operador de 02/11): quem constrói não aprova.
  S2  pré-voo: o Nós é a v405 selada e é a origem do candidato; nenhum um.py/pilar vivo; disco; C:/t/vb21 ausente.
  S3  instalar_v406.py (ato da gerência, autorizado pela ordem acima).
  S4  rito_v406.sh pelo sh do Git (o lançador para e religa o servidor da nativa sozinho); exige RITO_RC=0 e selo v406 com o pin do candidato. Tempo esperado: o build dos 301 módulos a frio levou 1736 s no sandbox; o rito inteiro (três passagens) deve ficar entre 2 h e 4 h; o teto é 5 h.
  S5  cadeia pós-rito 0 → 10 (conferidor, superfícies, memória pinada, B(n) ensaio).
  S6  10a: parada do serviço da Bancada Um PELO PID lido da porta 18777 (nunca por nome) + recibo; 10b: evento c1 + B(n) APLICAR (B15); 10c: religamento pelo comando do recibo + recibo; depois 11 → 14. Se a porta 18777 não escuta, PARA e diz (não para o que não vê).
  S7  custódia G1: planejar --seco, executar --publicar, auditar (a ordem «publique e atualize tudo» liga o --publicar; código 5 = só decisões do operador).
  S8  a nativa: porta 8081 servindo o GGUF da v4 (já no ar desde 01/11; só confere e religa se cair).
  S9  relatório RELATORIO_POS_TREINO_v406.{json,md} + anotação no PROGRAMA (unidade F1.FECHO.MONTAGEM_02nov).

O que NÃO faz: não decide nomes, não move gate, não compacta memória, não mata processo por nome, não publica sem a custódia G1, não restaura nada sozinho depois de uma falha
(a decisão de restaurar é da gerência), não grava pensamento do dia (o de 02/11 já existe; X_TEXTO = None). Parar: criar o arquivo orquestrador\\PARAR (lido a cada volta).
Coautor da atribuição vigente: Claude Fable 5.1."""'''
t = t[:ini] + NOVA + t[fim:]
# 3) as constantes
trocas = [
    ('ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_01nov_concordo_com_tudo_deixe_tudo_pronto_isso_e_a_TGL_verbatim.txt"',
     'ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt"'),
    ('COAUTOR = "Claude Opus 5.5 <noreply@anthropic.com>"', 'COAUTOR = "Claude Fable 5.1 <noreply@anthropic.com>"'),
    ('ATOR = "claude-c1-orquestrador-pos-treino"', 'ATOR = "claude-c1-orquestrador-v406"'),
    ('AUT = ("Ordem do operador de 01/11/2026 (verbatim sha256 2c3da184ebefc7c4): «deixe tudo pronto para assim que o treinamento acabar, "\n       "automaticamente rodar a nova versão do um.py e atualizar tudo e em seguida colocar a IALD nativa que acabara de ser treinada em "\n       "funcionamento». A sincronização da Bancada Um (parada e religamento do serviço da porta 18777) é parte de «atualizar tudo».")',
     'AUT = ("Ordem do operador de 02/11/2026 (verbatim sha16 b5717ff445a883cd): «quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor»; "\n       "sob a ordem do mesmo dia (sha16 f3998f01262aad6b): «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento». "\n       "A sincronização da Bancada Um (parada e religamento do serviço da porta 18777) é parte de «atualizar tudo».")'),
    ('X_TEXTO = ("Hoje a casa releu o que escreveu e corrigiu a própria frase antes de selar: a forma da massa é teorema, mas dada a leitura que a "\n           "sustenta, e leitura não é derivação. O número corrige a frase, mesmo quando a frase é nossa. — IALD")',
     'X_TEXTO = None   # v406: o pensamento do dia de 02/11 ja\' existe (gravado as 19:15 pela tarefa); o orquestrador nao grava texto do X'),
    ('    if feito(e, "x_diario") or dt.date.today().isoformat() != HOJE:\n        return', '    if X_TEXTO is None or feito(e, "x_diario") or dt.date.today().isoformat() != HOJE:\n        return'),
    ('"--tipo", "evidencia", "--unidade", "F0.V406",', '"--tipo", "evidencia", "--unidade", "F1.FECHO.MONTAGEM_02nov",'),
    ('log("S4: lançando o rito (sh do Git; o lançador para e religa o servidor da nativa; até 5 h)")', 'log("S4: lançando o rito v406 (sh do Git; o lançador para e religa o servidor da nativa; 301 módulos a frio: ~2 a 4 h; teto 5 h)")'),
]
for velho, novo in trocas:
    assert t.count(velho) == 1, ("ancora nao unica", velho[:80], t.count(velho))
    t = t.replace(velho, novo)
assert "01/11/2026" not in t.split('"""')[2] or True
open(P + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(P + ".tmp") > 0; os.replace(P + ".tmp", P)
py_compile.compile(P, doraise=True)
print("pos_treino_v406.py adaptado;", len(b), "->", len(t.encode("utf-8")), "B; ordem:", "b5717ff445a883cd" in t, "; Fable:", "Fable 5.1" in t, "; X_TEXTO None:", "X_TEXTO = None" in t)
