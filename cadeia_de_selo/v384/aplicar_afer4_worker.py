# -*- coding: utf-8 -*-
"""4a afericao no TRABALHADOR: o modo zero do D128 conta mesmo se o D128 cair depois do espectro; NOT_COMPARABLE so com a referencia DESTA rodada, filho com
codigo 0 e nenhuma linha da GPU faltando (o E8 ganha esse caso); as docstrings dizem E1..E8 e o modo zero. Backup ja feito (pilar_quantico_worker_auditado_4a_passada.py)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pilar_quantico_worker.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(os.path.join(HERE, "pilar_quantico_worker_auditado_4a_passada.py"), "rb").read() == raw
PAIRS = [
    ('''    nv += int(bool((R.get("D128") or {}).get("ran")) and (R.get("D128") or {}).get("zero_mode_ok") is False)   # o modo zero em d = 128''',
     '''    nv += int((R.get("D128") or {}).get("zero_mode_ok") is False)   # o modo zero em d = 128: conta mesmo se o D128 cair DEPOIS do espectro (4a afericao)'''),
    ('''    return {"read": n, "compared": n - near, "near_threshold_not_compared": near, "not_comparable": bool(n > 0 and n == near), "disagreements": len(bad),''',
     '''    return {"read": n, "compared": n - near, "near_threshold_not_compared": near,
            "not_comparable": bool(n > 0 and n == near and meta_ok and child_rc == 0 and not bad),   # so a referencia DESTA rodada, completa (4a afericao)
            "disagreements": len(bad),'''),
    ('''    r_mt = compare_cpuref(sp8, {"a": g8}, cpu8({"a": c8}, dict(me8, run_id="outra")), me8, 0)
    ok = bool(r_eq["ok"] and r_eq["compared"] == 2 and not r_cc["ok"] and r_cc["disagreements"] == 1 and r_n2["ok"] and not r_nr["ok"] and r_nr["not_comparable"]
              and not r_mt["ok"])''',
     '''    r_mt = compare_cpuref(sp8, {"a": g8}, cpu8({"a": c8}, dict(me8, run_id="outra")), me8, 0)
    r_nm = compare_cpuref(sp8, {"a": dict(g8, gap_rel=1e-8)}, cpu8({"a": dict(c8, gap_rel=1e-8)}, dict(me8, run_id="outra")), me8, 0)   # perto do limiar + marca errada
    ok = bool(r_eq["ok"] and r_eq["compared"] == 2 and not r_cc["ok"] and r_cc["disagreements"] == 1 and r_n2["ok"] and not r_nr["ok"] and r_nr["not_comparable"]
              and not r_mt["ok"] and not r_nm["ok"] and not r_nm["not_comparable"])'''),
    ('''                                                             "wrong_run_id": r_mt["ok"]}))''',
     '''                                                             "wrong_run_id": r_mt["ok"], "near_threshold_wrong_run_id_not_comparable": r_nm["not_comparable"]}))'''),
    ('''Ordem: o MOTOR e' conferido em modelos ANALITICOS (E1..E6) e o ESTIMADOR no seu piso (E7) antes de tudo -- se falhar, nada se calcula.''',
     '''Ordem: o MOTOR e' conferido em modelos ANALITICOS (E1..E6), o ESTIMADOR no seu piso (E7) e o COMPARADOR da referencia na CPU (E8) antes de tudo -- se
falhar, nada se calcula.'''),
    ('''Modos: run (o rito) | engine (so E1..E7) |''', '''Modos: run (o rito) | engine (so E1..E8) |'''),
    ('''# E1..E7 -- o motor conferido em modelos ANALITICOS e o estimador no seu PISO (nenhum operador da teoria)''',
     '''# E1..E8 -- o motor conferido em modelos ANALITICOS, o estimador no seu PISO e o comparador da CPU com linhas sinteticas (nenhum operador da teoria)'''),
    ('''    """Devolve (violacoes, conferidas): CP, TP e o nao-retorno em toda instancia nao degenerada; PSD, o residuo do estacionario e Spohn so no atrator''',
     '''    """Devolve (violacoes, conferidas): o MODO ZERO (n0 >= 1: tr . S = 0 garante um zero), CP, TP e o nao-retorno em toda instancia nao degenerada; PSD, o residuo do estacionario e Spohn so no atrator'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "sha16", hashlib.sha256(b).hexdigest()[:16])
