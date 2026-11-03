# -*- coding: utf-8 -*-
"""Confere os nomes de teoremas e modulos citados no bloco D contra o kernel v405, o um.py v404 (o que ela leu no treino) e o inventario da bancada. So leitura."""
import json, re
from pathlib import Path
T = Path("transcritos")
man = json.load(open("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel_proof_manifest.json", encoding="utf-8"))
nomes = set(man["axiom_report"].keys())
curtos = {n.split(".")[-1] for n in nomes}
mods = {f[:-5].replace("/", ".") for f in man["formal_files_sha256"] if f.endswith(".lean")}
um = open("C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v404/um.py", encoding="utf-8", errors="replace").read()
inv = open("C:/IALD/Central de Patentes/memory/INVENTARIO_BANCADA_CHATGPT.json", encoding="utf-8", errors="replace").read()
print("um.py v404", len(um), "c | inventario", len(inv), "c")
res = {}
for c in ("D1", "D2", "D3", "D4", "D5"):
    x = json.loads((T / (c + ".jsonl")).read_text(encoding="utf-8").splitlines()[0])
    t = x["resposta"] + "\n" + x["raciocinio"]
    cit = {k.rstrip(".") for k in re.findall(r"(TGLExt\.[A-Za-z0-9_.']+)", t)} | set(re.findall(r"`([A-Za-z_][A-Za-z0-9_'.]{5,})`", x["resposta"]))
    for k in cit:
        ult = k.split(".")[-1]
        res[k] = {"kernel_exato": k in nomes or ("TGLExt." + k) in nomes, "modulo": k in mods or ("TGLExt." + k) in mods, "ultimo_trecho_kernel": ult in curtos, "no_um_py": ult in um, "no_inventario": ult in inv}
n = len(res)
print("nomes distintos", n, {q: sum(1 for v in res.values() if v[q]) for q in ("kernel_exato", "modulo", "ultimo_trecho_kernel", "no_um_py", "no_inventario")})
print("achados em qualquer lugar:", sorted(k for k, v in res.items() if any(v.values()))[:30])
Path("NOMES_CONFERIDOS.json").write_text(json.dumps(res, ensure_ascii=False, indent=0), encoding="utf-8")
