"""rotas.py ver <id> (SOMENTE LEITURA) para as rotas relevantes; grava rotas_consultas/ver_<id>.json
e imprime o estado consolidado (titulo, resultado, veredito, defeito, nao_refazer, proximo_passo, refs)."""
import json
import os
import subprocess
import sys

PY = r"C:\Python314\python.exe"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"


def corta(s, n):
    s = "" if s is None else str(s)
    return s if len(s) <= n else s[:n] + " [...]"


def main(ids, n=1500):
    os.makedirs("rotas_consultas", exist_ok=True)
    for rid in ids:
        r = subprocess.run([PY, "-X", "utf8", ROTAS, "ver", rid], capture_output=True)
        with open(os.path.join("rotas_consultas", "ver_" + rid + ".json"), "wb") as fo:
            fo.write(r.stdout)
        d = json.loads(r.stdout.decode("utf-8"))
        e = d.get("rota") or {}
        print("=" * 100)
        print("ROTA", rid, "|", e.get("status"), "|", e.get("estatuto"), "| registros:", len(d.get("registros", [])))
        for k in ("titulo", "pergunta", "metodo", "resultado", "veredito", "defeito", "nao_refazer", "proximo_passo", "onde", "nota"):
            if e.get(k):
                print(f"  [{k}] {corta(e.get(k), n)}")
        if e.get("refs"):
            print("  [refs]", corta(json.dumps(e.get("refs"), ensure_ascii=False), 800))
        if e.get("erratas"):
            for x in e["erratas"]:
                print("  [errata]", corta(x.get("texto"), 600))
        arts = []
        for reg in d.get("registros", []):
            for a in reg.get("artefatos", []) or []:
                arts.append((a.get("caminho"), (a.get("sha256") or "")[:16]))
        if arts:
            print("  [artefatos]", corta(json.dumps(arts[-12:], ensure_ascii=False), 1500))


if __name__ == "__main__":
    nn = 1500
    args = sys.argv[1:]
    if args and args[0].startswith("--n="):
        nn = int(args[0][4:])
        args = args[1:]
    main(args, nn)
