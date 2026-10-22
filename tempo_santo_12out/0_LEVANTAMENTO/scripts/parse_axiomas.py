"""Le a saida do Lean (somente leitura) e extrai, por nome, a lista de axiomas (multi-linha), conferindo o trio.
Uso: python -I parse_axiomas.py <saida_lean.txt> <arquivo.lean> <saida.json>"""
import hashlib
import json
import re
import sys

TRIO = {"propext", "Classical.choice", "Quot.sound"}


def main(saida, src, out):
    raw = open(saida, "rb").read()
    txt = raw.decode("utf-8", "replace")
    pedidos = re.findall(r"^#print axioms\s+(\S+)", open(src, encoding="utf-8").read(), re.M)
    res = {}
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", txt, re.S):
        axs = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
        res[m.group(1)] = axs
    for m in re.finditer(r"'([^']+)' does not depend on any axioms", txt):
        res[m.group(1)] = []
    faltam = [p for p in pedidos if p not in res]
    fora = {k: v for k, v in res.items() if not set(v) <= TRIO}
    d = dict(saida=saida, saida_sha256=hashlib.sha256(raw).hexdigest(), fonte=src,
             fonte_sha256=hashlib.sha256(open(src, "rb").read()).hexdigest(),
             n_pedidos=len(pedidos), n_respondidos=len(res), faltam=faltam, fora_do_trio=fora,
             sorryAx_no_texto=txt.count("sorryAx"), todos_no_trio=(not fora and not faltam), axiomas=res)
    with open(out, "w", encoding="utf-8") as fo:
        json.dump(d, fo, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in d.items() if k != "axiomas"}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
