# -*- coding: utf-8 -*-
"""10a afericao no GERADOR DO PRE-REGISTRO (script salvo; count == 1; backup de BYTES feito e conferido AQUI) -- os tres achados que tocam o rascunho:
- 10N0: na nota antiga, o ESCOPO (em d = 64) vem ANTES dos numeros; o «d = 8 a 64» do cabecalho do paragrafo no MD e' GERADO dos d das sondas;
- 10N1/10N7: o texto do lancador: o PID sai em qualquer saida antecipada e, armada a restauracao, so no FIM dela; o .fase0 de tentativas anteriores e'
  ACRESCENTADO ao .fase0.anterior; os sinais giram antes do log real; o ESCOPO do «o log de uma tentativa recusada fica no .fase0» (as recusas depois da fase 0;
  as anteriores -- 6 a 9 e 16, e a 17 do proprio .fase0 -- so na saida do lancador)."""
import ast, hashlib, os, time
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert hashlib.sha256(raw).hexdigest().startswith("ee25d7f83da27c55"), "o gerador nao e' o auditado na 10a (ee25d7f8)"
bak = P + ".bak_antes_afer10_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    ('''"mostram a dispersao entre rodadas: a maior sonda sobre a corrente da %.3f (instancia) e %.3f (injecao do T1), e a maior sobre a menor da "
                                            "%.3f (instancia) -- em d = 64, a margem x%.2f %s a maior sobre a corrente (instancia e injecao do T1) e %s a dispersao maior/menor da INSTANCIA (os "
                                            "outros pontos e custos: a nota por d e por custo); nao foi medida sob a carga do rito") % (''',
     '''"mostram a dispersao entre rodadas: em d = 64, a maior sonda sobre a corrente da %.3f (instancia) e %.3f (injecao do T1), e a maior sobre a menor da "
                                            "%.3f (instancia) -- ali, a margem x%.2f %s a maior sobre a corrente (instancia e injecao do T1) e %s a dispersao maior/menor da INSTANCIA (os "
                                            "outros pontos e custos: a nota por d e por custo); nao foi medida sob a carga do rito") % ('''),
    ('''"Variabilidade das sondas de tempo (a lista: d = 64, s por instância / por injeção do T1; a nota por d e por custo cobre d = 8 a 64): "''',
     '''"Variabilidade das sondas de tempo (a lista: d = 64, s por instância / por injeção do T1; a nota por d e por custo cobre d = %d a %d): " % (min(c_pipe), max(c_pipe))'''),
    ('''gravado logo depois da guarda e só removido no FIM da restauração (com outro lançador vivo, RECUSA — código 16)''',
     '''gravado logo depois da guarda e removido em qualquer saída antecipada — armada a restauração, só no FIM dela (com outro lançador vivo, RECUSA — código 16)'''),
    ('''a tentativa escreve num log próprio (.fase0; o de uma tentativa anterior vai para .fase0.anterior)''',
     '''a tentativa escreve num log próprio (.fase0; o de tentativas anteriores é ACRESCENTADO ao .fase0.anterior, com separador datado)'''),
    ('''o log de uma tentativa recusada fica no .fase0;''',
     '''o log de uma tentativa recusada depois da fase 0 (códigos 10 a 15 e as 17 dos giros dos sinais e do log, que vêm antes de o log real sair do lugar — os sinais giram primeiro) fica no .fase0, e as recusas anteriores à fase 0 (6 a 9 e 16) e a 17 da guarda do próprio .fase0 só aparecem na saída do lançador;'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:160])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16], "| backup", os.path.basename(bak))
