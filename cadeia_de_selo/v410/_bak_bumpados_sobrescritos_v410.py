# -*- coding: utf-8 -*-
"""_bak_bumpados_sobrescritos_v410.py -- (claude-construtor-v410, 06/11/2026) DESVIO DITO: delta_v410.py e preparar_bundle_v410_06nov.py (as subidas mecanicas do bump) foram REESCRITOS pela ferramenta Write
sem o backup de bytes antes (e, depois, runtime_v410.py). Este script REFAZ, pela mesma funcao do bump (_bump_copia_v410.subir + o cabecalho), o texto que estava em disco e o grava como <arquivo>.bak_<ts>_bump_refeito, conferindo o sha16
contra o BUMP_v410_RESULTADO.json (destino_sha16 da subida). Nada mais e' tocado."""
import datetime, hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
src = open(os.path.join(HERE, "_bump_copia_v410.py"), "rb").read().decode("utf-8")
src = src[:src.rindex("\nmain()")] + "\n"
ns = {"__file__": os.path.join(HERE, "_bump_copia_v410.py"), "__name__": "_bump_sem_main"}
_ARGV = list(sys.argv); sys.argv = [sys.argv[0], "--seco"] + _ARGV[1:]
exec(compile(src, "_bump_copia_v410.py", "exec"), ns)
res = json.load(open(os.path.join(HERE, "BUMP_v410_RESULTADO.json"), encoding="utf-8"))
PARES = [tuple(x.split("=")) for x in _ARGV[1:]] or [("delta_v409.py", "delta_v410.py"), ("preparar_bundle_v409_05nov.py", "preparar_bundle_v410_06nov.py")]   # uso: ... -- molde=destino ...
for molde, dest in PARES:
    t = open(os.path.join(ns["V9"], molde), "rb").read().decode("utf-8")
    novo, _ = ns["subir"](t)
    novo, _ = ns["insere_cabecalho"](novo, ns["cabecalho"](dest, molde))
    b = novo.encode("utf-8")
    assert hashlib.sha256(b).hexdigest()[:16] == res[molde]["destino_sha16"], ("o texto refeito nao e' o que o bump gravou", molde)
    p = os.path.join(HERE, dest + ".bak_" + TS + "_bump_refeito")
    open(p, "wb").write(b); assert open(p, "rb").read() == b
    print(dest, "->", os.path.basename(p), res[molde]["destino_sha16"])
