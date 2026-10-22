# -*- coding: utf-8 -*-
"""Copia de BYTES da evidencia das duas auditorias independentes (que vivem no scratchpad temporario
desta sessao) para 4_RELATORIO/AUDITORIAS, para que o relatorio e os registros do mapa apontem para
arquivos duraveis. Confere sha256 da origem e do destino arquivo a arquivo. Nao apaga nada na origem.
Saida: AUDITORIAS/MANIFESTO_COPIA_AUDITORIAS.json.
"""
import hashlib
import json
import os
import sys

SCR = (r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes"
       r"\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12")
ORIGENS = {"TEMPO_AUD_REPRO": os.path.join(SCR, "TEMPO_AUD_REPRO"),
           "TEMPO_AUD_ESTATUTO": os.path.join(SCR, "TEMPO_AUD_ESTATUTO")}
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(BASE, "AUDITORIAS")
LONG = "\\\\?\\"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    man = {"documento": "copia de bytes da evidencia das auditorias F1.TEMPO (reproducao e estatuto)",
           "origem_base": SCR, "destino_base": DEST, "arquivos": [], "falhas": []}
    for nome, orig in ORIGENS.items():
        for dp, dn, fn in os.walk(orig):
            dn.sort()
            for f in sorted(fn):
                src = os.path.join(dp, f)
                rel = os.path.relpath(src, orig)
                dst = os.path.join(DEST, nome, rel)
                os.makedirs(LONG + os.path.dirname(dst), exist_ok=True)
                b = open(LONG + src, "rb").read()
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
                                        "sha256_origem": sha(b), "sha256_destino": sha(b2),
                                        "identico": b == b2})
    man["n_arquivos"] = len(man["arquivos"])
    man["todos_identicos"] = all(x["identico"] for x in man["arquivos"]) and not man["falhas"]
    out = os.path.join(DEST, "MANIFESTO_COPIA_AUDITORIAS.json")
    with open(out + ".tmp", "wb") as fo:
        fo.write(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(out + ".tmp", out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"n_arquivos": man["n_arquivos"], "todos_identicos": man["todos_identicos"],
                      "falhas": man["falhas"]}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
