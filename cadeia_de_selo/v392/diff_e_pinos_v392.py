# -*- coding: utf-8 -*-
"""diff_e_pinos_v392.py -- (1) DIFF_KERNEL_v392.txt (molde DIFF_KERNEL_v390.txt): arquivos novos, removidos e mudados do kernel embutido do candidato contra o da v391 (com o diff da raiz e a contagem
do Audit); (2) PINOS_BN_v392.json: os sha256 que o elo B(n) pede (esboco, bateria, CRITERIOS, recibo do kernel, recibo pre-selo), LIDOS dos arquivos. Uso: python -I -B -X utf8 diff_e_pinos_v392.py"""
import ast, difflib, glob, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote"))
from carregar_embutido import carregar  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
sha = lambda b: hashlib.sha256(b).hexdigest()
if sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16] != "8e7b9927ceae64b8":   # o Nos ja nao e' a v391 (rito em curso): a v391 selada vem da copia base_v391
    NOS = os.path.join(HERE, "base_v391")
E0, _, _, h0 = carregar(os.path.join(NOS, "um.py")); E1, _, _, h1 = carregar(os.path.join(HERE, "um_v392_candidato.py"))
novos = sorted(set(E1) - set(E0)); removidos = sorted(set(E0) - set(E1)); mudados = sorted(k for k in set(E0) & set(E1) if E0[k] != E1[k])
out = ["DIFF DO KERNEL EMBUTIDO v391 (%s) -> v392 (%s)" % (h0, h1), "", "novos (%d):" % len(novos)] + ["  + %s  %s  %d B" % (k, sha(E1[k].encode())[:16], len(E1[k].encode())) for k in novos]
out += ["", "removidos (%d):" % len(removidos)] + ["  - " + k for k in removidos] + ["", "mudados (%d):" % len(mudados)]
for k in mudados:
    a, b = E0[k].splitlines(), E1[k].splitlines(); d = list(difflib.unified_diff(a, b, "v391/" + k, "v392/" + k, lineterm="", n=0))
    out.append("  ~ %s  %s -> %s  (+%d linhas, -%d linhas)" % (k, sha(E0[k].encode())[:16], sha(E1[k].encode())[:16], sum(1 for l in d if l.startswith("+") and not l.startswith("+++")), sum(1 for l in d if l.startswith("-") and not l.startswith("---"))))
    if k == "TGLExt.lean":
        out += ["      " + l for l in d]
    else:
        out += ["      " + l[:200] for l in d[:6]] + ["      ... (%d linhas de diff no total)" % len(d)]
open(os.path.join(HERE, "DIFF_KERNEL_v392.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("\n".join(out[:4]), "...", "novos", len(novos), "removidos", len(removidos), "mudados", mudados)
# pinos do B(n)
V = os.path.join(HERE, "vinculo"); pre = sorted(glob.glob(os.path.join(HERE, "bateria_pre_selo", "ensaio_1", "RECIBO_SINCRONIZACAO_v391_*.json")))
f = lambda p: {"path": p, "sha256": sha(open(p, "rb").read())}
pn = {"esboco_R3_3": f(os.path.join(V, "sincronizar_bancada.py")), "bateria": f(os.path.join(V, "BATERIA_VINCULO.json")), "criterios": f(os.path.join(V, "CRITERIOS_v392.json")),
      "kernel_recibo": f(os.path.join(HERE, "kernel", "KERNEL_RECIBO_v392.json")), "recibo_pre_selo": f(pre[-1]),
      "selo_anterior_v391": f(os.path.join(HERE, "bateria_pre_selo", "anterior_v391", "um_absoluto_selo.json")), "kernel_manifesto_anterior_v391": f(os.path.join(HERE, "bateria_pre_selo", "anterior_v391", "tgl_kernel_proof_manifest.json")),
      "resumo_T18_T22": f(os.path.join(HERE, "bateria_pre_selo", "ensaio_2_T18_T22", "RESUMO_T18_T22.json")), "candidato": f(os.path.join(HERE, "um_v392_candidato.py")), "esperados": f(os.path.join(HERE, "ESPERADOS_v392.json")), "pins_do_candidato": f(os.path.join(HERE, "v392_pins.py")),
      "nota": "[REAL] lido dos arquivos por script; o B(n) pede estes sha256 em --bateria-sha256, --criterios-sha256, --kernel-recibo-sha256, --recibo-pre-selo-sha256"}
json.dump(pn, open(os.path.join(HERE, "PINOS_BN_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: v["sha256"][:16] for k, v in pn.items() if isinstance(v, dict)})
