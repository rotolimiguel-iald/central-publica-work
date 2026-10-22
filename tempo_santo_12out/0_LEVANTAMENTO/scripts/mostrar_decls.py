"""Mostra (somente leitura) a docstring e o enunciado de declaracoes do kernel listadas por nome (sufixo).
Le kernel_decls.jsonl (gerado por varrer_kernel.py) e o arquivo-fonte para o enunciado completo ate ':=' ou 'by'.
Uso: python -I mostrar_decls.py nome1 nome2 ..."""
import json
import os
import sys

ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"


def enunciado(rel, line, maxl=14):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        lines = fh.read().decode("utf-8", "replace").splitlines()
    out = []
    for j in range(line - 1, min(line - 1 + maxl, len(lines))):
        out.append(lines[j].rstrip())
        s = lines[j]
        if ":= by" in s or s.rstrip().endswith(":=") or " := " in s or s.strip().startswith("|"):
            break
    return "\n".join(out)


def main(names):
    decls = [json.loads(l) for l in open("kernel_decls.jsonl", encoding="utf-8")]
    for nm in names:
        hits = [d for d in decls if d["name"] == nm or d["name"].endswith("." + nm)]
        if not hits:
            print("#### NAO ENCONTRADO:", nm)
            continue
        for d in hits:
            print("#### ", d["name"], "|", d["file"], "l.", d["line"], "|", d["kind"], "| sha16", d["sha16"])
            if d["doc"]:
                print("   DOC:", d["doc"][:900])
            print(enunciado(d["file"], d["line"]))
            print()


if __name__ == "__main__":
    main(sys.argv[1:])
