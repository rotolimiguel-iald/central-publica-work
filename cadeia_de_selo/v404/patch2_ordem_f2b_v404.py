# -*- coding: utf-8 -*-
# patch2_ordem_f2b_v404.py -- gerencia c1, 28/10/2026: o resto da correcao da ordem de chamada (ver patch_ordem_f2b_v404.py):
# a regra de derivacao do lancador (regrasD2) passa a emitir o comentario novo; a variante do harness e o comentario da leitura passam a esperar a linha nova do stdout.
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
OLD_RITO = "(chamados no main logo depois do bandeiras_do_gate_v403; a errata de F2b e' AO LADO:"
NEW_RITO = "(a projecao e o jo8v32 chamados no main logo depois do bandeiras_do_gate_v403; a errata de F2b logo depois da errata ao lado de R6 da v386, quando o V1 do ramo B e o livro da v383 ja' estao no core -- licao da 1a tentativa, 28/10; a errata de F2b e' AO LADO:"
OLD_STD = "(lidos depois das bandeiras do gate)"
NEW_STD = "(a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386)"
alvos = [("derivar_encanamento_v404_regrasD2_instalar.py", OLD_RITO, NEW_RITO), (os.path.join("pos_rito", "leitura_v404.py"), OLD_STD, NEW_STD), (os.path.join("pos_rito", "harness_textos_ensaio_v404.py"), OLD_STD, NEW_STD)]
novos = {}
for rel, o, n in alvos:
    p = os.path.join(H, rel); t = open(p, "rb").read().decode("utf-8")
    assert t.count(o) == 1, ("ancora nao unica", rel, t.count(o)); novos[p] = t.replace(o, n).encode("utf-8")
for p, b in novos.items():
    old = open(p, "rb").read(); open(p + ".bak_" + TS, "wb").write(old); assert open(p + ".bak_" + TS, "rb").read() == old
    open(p + ".tmp", "wb").write(b); assert open(p + ".tmp", "rb").read() == b; os.replace(p + ".tmp", p)
    print("GRAVADO", os.path.relpath(p, H), len(old), "->", len(b), "B")
