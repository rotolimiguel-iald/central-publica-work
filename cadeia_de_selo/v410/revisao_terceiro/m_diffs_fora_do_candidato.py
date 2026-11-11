# -*- coding: utf-8 -*-
"""Revisor v410 R1 (item 5 do pedido): diffs dos consertos FORA do candidato contra o backup imediatamente anterior (.bak_*): gerar_esperados (22 -> 22+38), conferir_rito (qualificador EN da D64),
pos_treino_v410 (S6d / d59), textos_v410 (quadro do pacote), harness_textos, harness_fechar, registrar_mapa. Imprime so' as linhas -/+ (com limite) para classificacao manual: afrouxa alguma checagem?"""
import difflib, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
pares = [("gerar_esperados_v410.py", "gerar_esperados_v410.py.bak_20261109_202055_pre_fix_ancoras"),
         ("conferir_rito_v410.py", "conferir_rito_v410.py.bak_20261109_202632_pre_qualificador_en"),
         ("orquestrador/pos_treino_v410.py", "orquestrador/pos_treino_v410.py.bak_20261109_222718_pre_d59_s6d"),
         ("pos_rito/registrar_mapa_v410.py", "pos_rito/registrar_mapa_v410.py.bak_20261109_212227_agente_harness"),
         ("pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/harness_fechar_sandbox_v410.py.bak_20261109_220616_agente_harness4"),
         ("pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_textos_ensaio_v410.py.bak_20261109_211840_agente_harness"),
         ("pos_rito/textos_v410.py", "pos_rito/textos_v410.py.bak_20261109_220550_agente_harness3"),
         ("pos_rito/leitura_v410.py", "pos_rito/leitura_v410.py.bak_20261109_211240_pre_quadro_do_pacote")]
for novo, bak in pares:
    a = open(R + bak, "rb").read().decode("utf-8", "replace").split("\n"); b = open(R + novo, "rb").read().decode("utf-8", "replace").split("\n")
    d = [l for l in difflib.unified_diff(a, b, "bak", "novo", lineterm="", n=0) if (l.startswith("+") or l.startswith("-")) and not l.startswith("+++") and not l.startswith("---")]
    print("\n######", novo, "vs", bak.split(".bak_")[1], "| linhas -/+:", len(d))
    for l in d[:60]: print("  ", l[:420])
    if len(d) > 60: print("   ... (+%d)" % (len(d) - 60))
