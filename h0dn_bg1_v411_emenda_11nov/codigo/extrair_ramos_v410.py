# -*- coding: utf-8 -*-
"""Extrai do um.py (v410) o dicionario literal `ramos` de producao (perto da linha 228989) por ast.literal_eval sobre o
trecho balanceado. Grava artefatos/RAMOS_V410.json (SO' o dicionario, JSON canonico: sort_keys, ensure_ascii=False,
tuplas como listas) e artefatos/RAMOS_V410_ORIGEM.json (sha256 do um.py, do JSON, n de literais, linhas, igualdade).
Nenhum dado observado e' lido."""
import ast
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "artefatos"
UM = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
CHAVE = "'ramos': {'limiar'"


def balanceado(text, i):
    """text[i] e' '{': devolve o indice logo apos o '}' que fecha, respeitando aspas simples/duplas e escapes."""
    assert text[i] == "{"
    depth, j, n, q = 0, i, len(text), None
    while j < n:
        ch = text[j]
        if q:
            if ch == "\\":
                j += 2
                continue
            if ch == q:
                q = None
        else:
            if ch in "'\"":
                q = ch
            elif ch in "{[(":
                depth += 1
            elif ch in "}])":
                depth -= 1
                if depth == 0:
                    return j + 1
        j += 1
    raise ValueError("literal nao balanceado")


def main():
    raw = UM.read_bytes()
    text = raw.decode("utf-8")
    pos, k = [], text.find(CHAVE)
    while k >= 0:
        pos.append(k)
        k = text.find(CHAVE, k + 1)
    if not pos:
        raise SystemExit("nenhum literal " + CHAVE)
    literais = []
    for k in pos:
        i = k + len("'ramos': ")
        j = balanceado(text, i)
        d = ast.literal_eval(text[i:j])
        linha = text.count("\n", 0, k) + 1
        literais.append({"linha": linha, "dict": d, "trecho_bytes": len(text[i:j].encode("utf-8"))})
    canon = [json.dumps(l["dict"], sort_keys=True, ensure_ascii=False) for l in literais]
    iguais = len(set(canon)) == 1
    ramos = literais[0]["dict"]
    body = (json.dumps(ramos, sort_keys=True, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    dest = OUT / "RAMOS_V410.json"
    tmp = dest.with_suffix(".json.tmp")
    tmp.write_bytes(body)
    assert tmp.stat().st_size == len(body)
    tmp.replace(dest)
    origem = {"um_py": {"path": str(UM), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
              "chave_procurada": CHAVE, "n_literais": len(pos), "linhas": [l["linha"] for l in literais],
              "literais_iguais_entre_si": iguais,
              "ramos_v410_json": {"path": str(dest), "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()},
              "limiar": ramos["limiar"], "compat_95": ramos["compat_95"], "chaves_vereditos": sorted(ramos["vereditos"])}
    od = OUT / "RAMOS_V410_ORIGEM.json"
    tmp = od.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(origem, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(od)
    print(json.dumps({k: origem[k] for k in ("n_literais", "linhas", "literais_iguais_entre_si", "limiar", "compat_95", "chaves_vereditos")}))
    print(origem["ramos_v410_json"])


if __name__ == "__main__":
    main()
