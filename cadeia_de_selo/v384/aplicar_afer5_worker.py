# -*- coding: utf-8 -*-
"""5a afericao no TRABALHADOR: o parcial do D128 e' gravado LOGO DEPOIS do espectro (com n0 e zero_mode_ok), para a violacao do modo zero sobreviver a uma
MORTE do processo (queda nativa ou prazo) depois do espectro; o comentario do passo 2 da arvore cita o modo zero (T2, T4 e D128).
Backup ja feito (pilar_quantico_worker_auditado_5a_passada.py)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pilar_quantico_worker.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(os.path.join(HERE, "pilar_quantico_worker_auditado_5a_passada.py"), "rb").read() == raw
PAIRS = [
    ('''def run_D128(E, spec, beta, prog):''', '''def run_D128(E, spec, beta, prog, on_spectrum=None):'''),
    ('''        out["zero_mode_ok"] = bool(cl["n0"] >= 1)      # a IDENTIDADE do modo zero tambem em d = 128 (tr . S = 0 garante um zero; 3a afericao)''',
     '''        out["zero_mode_ok"] = bool(cl["n0"] >= 1)      # a IDENTIDADE do modo zero tambem em d = 128 (tr . S = 0 garante um zero; 3a afericao)
        if on_spectrum is not None:                     # o parcial ja leva n0 e zero_mode_ok: sobrevive a uma MORTE do processo depois do espectro (5a afericao)
            try:
                on_spectrum(dict(out))
            except Exception:
                pass'''),
    ('''            R["D128"] = run_D128(E, spec, beta, prog)''',
     '''            def _d128_parcial(o_):
                R["D128"] = dict(o_, ran=False, status_code="STARTED"); write_json_atomic(os.path.join(args.out, "result_partial.json"), R)
            R["D128"] = run_D128(E, spec, beta, prog, on_spectrum=_d128_parcial)'''),
    ('''    # 2. as identidades (CP, TP, nao-retorno, PSD, residuo, Spohn; V_t P_F = P_F; sin^2 theta_M = beta; N2: I/d estacionario na parte unital)''',
     '''    # 2. as identidades (o modo zero no T2, no T4 e no D128; CP, TP, nao-retorno, PSD, residuo, Spohn; V_t P_F = P_F; sin^2 theta_M = beta; N2: I/d estacionario na parte unital)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "sha16", hashlib.sha256(b).hexdigest()[:16])
