# -*- coding: utf-8 -*-
# Custodia das duas auditorias da F1.FREQUENCIA (trilha POSTO): copia BYTE A BYTE as pastas dos auditores, que moram no
# scratchpad da sessao (efemero), para 4_RELATORIO\auditorias_copia, e grava o manifesto com o sha256 da origem e da copia.
# So leitura na origem; escreve so em 4_RELATORIO.
import os, shutil, hashlib, json, time

ORIG = (r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes"
        r"\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12")
REL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(REL, "auditorias_copia")
PASTAS = ("POSTO_AUD_REPRO", "POSTO_AUD_ESTATUTO")


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


if os.path.exists(DEST):
    raise SystemExit("FALHA VISIVEL: auditorias_copia ja existe (nao sobrescrevo)")
man = {"documento": "MANIFESTO_COPIA_AUDITORIAS — custodia das pastas dos dois auditores (copia de bytes)",
       "quando_local": time.strftime("%Y-%m-%d %H:%M:%S"), "origem": ORIG, "destino": DEST, "arquivos": [], "falhas": []}
for pasta in PASTAS:
    raiz = os.path.join(ORIG, pasta)
    for dp, dns, fns in os.walk(raiz):
        dns.sort()
        for fn in sorted(fns):
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, ORIG)
            q = os.path.join(DEST, rel)
            os.makedirs(os.path.dirname(q), exist_ok=True)
            shutil.copy2(p, q)
            h1, h2 = sha(p), sha(q)
            man["arquivos"].append({"rel": rel.replace("\\", "/"), "bytes": os.path.getsize(q), "sha256": h2,
                                    "igual_a_origem": h1 == h2})
            if h1 != h2:
                man["falhas"].append(rel)
man["n_arquivos"] = len(man["arquivos"])
man["bytes_total"] = sum(a["bytes"] for a in man["arquivos"])
man["veredito"] = "COPIA_CONFERE_BYTE_A_BYTE" if not man["falhas"] else "COPIA_COM_FALHAS"
open(os.path.join(REL, "MANIFESTO_COPIA_AUDITORIAS.json"), "w", encoding="utf-8").write(
    json.dumps(man, ensure_ascii=False, indent=1))
print(json.dumps({k: man[k] for k in ("n_arquivos", "bytes_total", "veredito", "falhas")}, ensure_ascii=False))
