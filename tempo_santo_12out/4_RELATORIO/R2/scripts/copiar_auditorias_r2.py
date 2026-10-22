# -*- coding: utf-8 -*-
"""Copia de BYTES da evidencia das auditorias da R2 (13/10, no scratchpad temporario) para
4_RELATORIO/AUDITORIAS_R2. So arquivos com mtime posterior a 2026-10-12 19:00 local (as da R1 ja estao
em 4_RELATORIO/AUDITORIAS), fora de pastas 'toolchain', '.lake', 't' (toolchain abandonado) e com menos de 20 MB.
Confere sha256 origem x destino. Nao apaga nada na origem."""
import hashlib, json, os, sys, time
SCR = (r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes"
       r"\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12")
ORIGENS = {"TEMPO_AUD_REPRO": os.path.join(SCR, "TEMPO_AUD_REPRO"),
           "TEMPO_AUD_ESTATUTO": os.path.join(SCR, "TEMPO_AUD_ESTATUTO")}
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEST = os.path.join(BASE, "AUDITORIAS_R2")
LONG = "\\\\?\\"
CORTE = time.mktime(time.strptime("2026-10-12 19:00:00", "%Y-%m-%d %H:%M:%S"))
EXCL = {"toolchain", ".lake", "t", "l"}
MAXB = 20 * 1024 * 1024


def sha(b):
    return hashlib.sha256(b).hexdigest()


man = {"documento": "copia de bytes da evidencia das auditorias F1.TEMPO de 13/10 (R2: reproducao e estatuto)",
       "criterio": "mtime > 2026-10-12 19:00 local; sem toolchain/.lake; < 20 MB", "origem_base": SCR,
       "destino_base": DEST, "arquivos": [], "falhas": [], "excluidos_por_tamanho": []}
for nome, orig in ORIGENS.items():
    for dp, dn, fn in os.walk(LONG + orig):
        dn[:] = sorted(d for d in dn if d not in EXCL)
        for f in sorted(fn):
            src = os.path.join(dp, f)
            st = os.stat(src)
            if st.st_mtime <= CORTE:
                continue
            if st.st_size > MAXB:
                man["excluidos_por_tamanho"].append({"rel": os.path.relpath(src, LONG + orig), "bytes": st.st_size})
                continue
            rel = os.path.relpath(src, LONG + orig)
            dst = os.path.join(DEST, nome, rel)
            os.makedirs(LONG + os.path.dirname(dst), exist_ok=True)
            b = open(src, "rb").read()
            if os.path.exists(LONG + dst):
                if open(LONG + dst, "rb").read() != b:
                    man["falhas"].append({"rel": nome + "/" + rel, "erro": "destino existente difere"})
                    continue
            else:
                with open(LONG + dst + ".tmp", "wb") as fo:
                    fo.write(b)
                if open(LONG + dst + ".tmp", "rb").read() != b:
                    man["falhas"].append({"rel": nome + "/" + rel, "erro": "temporario nao confere"})
                    continue
                os.replace(LONG + dst + ".tmp", LONG + dst)
            b2 = open(LONG + dst, "rb").read()
            man["arquivos"].append({"rel": (nome + "/" + rel).replace("\\", "/"), "bytes": len(b),
                                    "mtime_local": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
                                    "sha256_origem": sha(b), "sha256_destino": sha(b2), "identico": b == b2})
man["n_arquivos"] = len(man["arquivos"])
man["todos_identicos"] = all(x["identico"] for x in man["arquivos"]) and not man["falhas"]
os.makedirs(LONG + DEST, exist_ok=True)
out = os.path.join(DEST, "MANIFESTO_COPIA_AUDITORIAS_R2.json")
with open(LONG + out + ".tmp", "wb") as fo:
    fo.write(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
os.replace(LONG + out + ".tmp", LONG + out)
sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps({"n_arquivos": man["n_arquivos"], "todos_identicos": man["todos_identicos"], "falhas": man["falhas"],
                  "excluidos": man["excluidos_por_tamanho"]}, ensure_ascii=False, indent=1))
for a in man["arquivos"]:
    print(a["rel"], a["bytes"], a["mtime_local"], a["sha256_origem"][:16])
