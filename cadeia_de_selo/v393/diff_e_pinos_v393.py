# -*- coding: utf-8 -*-
"""diff_e_pinos_v393.py -- (1) DIFF_KERNEL_v393.txt (molde DIFF_KERNEL_v390.txt): arquivos novos, removidos e mudados do kernel embutido do candidato contra o da v392 (com o diff da raiz e a contagem
do Audit); (2) PINOS_BN_v393.json: os sha256 que o elo B(n) pede (esboco, bateria, CRITERIOS, recibo do kernel, recibo pre-selo), LIDOS dos arquivos. Uso: python -I -B -X utf8 diff_e_pinos_v393.py"""
import ast, difflib, glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote"))
from carregar_embutido import carregar  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
sha = lambda b: hashlib.sha256(b).hexdigest()
if sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16] != "b590c0aa80055e2a":   # o Nos ja nao e' a v392 (rito em curso): a v392 selada vem da copia base_v392
    NOS = os.path.join(HERE, "base_v392")
E0, _, _, h0 = carregar(os.path.join(NOS, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, "um_v393_candidato.py"))
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v392 (%s) -> v393 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a, b = E0[k].splitlines(), E1[k].splitlines(); d = list(difflib.unified_diff(a, b, "v392/" + k, "v393/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(E0[k].encode())[:16], sha(E1[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d]
    else:
        out += ["      " + l[:200] for l in d[:6]] + ["      ... (%d linhas de diff no total)" % len(d)]
open(os.path.join(HERE, "DIFF_KERNEL_v393.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:4]), "...", "novos", len(novos), "removidos", len(removidos), "mudados", mudados)
# pinos do B(n): so' o que a preparacao da v393 gerou (o elo B(n) em si -- bateria pre-selo contra a v392, recibo pre-selo -- NAO foi preparado nesta tarefa)
V = os.path.join(HERE, "vinculo")
f = lambda p: {"path": p, "sha256": sha(open(p, "rb").read())} if os.path.exists(p) else {"path": p, "sha256": None, "estado": "NAO_PREPARADO"}
pn = {"criterios": f(os.path.join(V, "CRITERIOS_v393.json")), "kernel_recibo": f(os.path.join(HERE, "kernel", "KERNEL_RECIBO_v393.json")),
      "candidato": f(os.path.join(HERE, "um_v393_candidato.py")), "esperados": f(os.path.join(HERE, "ESPERADOS_v393.json")), "pins_do_candidato": f(os.path.join(HERE, "v393_pins.py")),
      "esboco_R3_3": f(os.path.join(os.path.dirname(HERE), "v392", "vinculo", "sincronizar_bancada.py")), "bateria": f(os.path.join(os.path.dirname(HERE), "v392", "vinculo", "BATERIA_VINCULO.json")),
      "nota": "[REAL] lido dos arquivos por script; esboco e bateria sao os da v392 (reuso; conferir se a bateria cobre a v393); o recibo pre-selo e o selo anterior v392 do B(n) NAO foram preparados"}
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v393.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["sha256"] or "NAO_PREPARADO")[:16] for k, v in pn.items() if isinstance(v, dict)})
