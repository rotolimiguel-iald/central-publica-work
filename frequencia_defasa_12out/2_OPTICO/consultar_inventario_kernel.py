# -*- coding: utf-8 -*-
"""Cetico aferidor (SO LEITURA): antes de escrever «nao ha lema» no anexo do ensaio otico, consultar o kernel do Nos
(TGLExt/*.lean e TGL/*.lean, fora de .lake) e o inventario da bancada (INVENTARIO_BANCADA_CHATGPT.json) e gravar o que
foi achado. Grava SO em 2_OPTICO/consultas_mapa/k_inventario_kernel.json; nunca sobrescreve.
"""
import hashlib
import json
import os
import re
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
KERNEL = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
INVENT = r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json"
DEST = os.path.join(AQUI, "consultas_mapa", "k_inventario_kernel.json")

PADROES = {
    "lei_de_grupo_ou_potencia_da_matriz_S": r"\b(Smat_pow|Smat_mul|Smat_add|Smat_nsmul|Smat_npow)\b",
    "anticomutador": r"anticomm|anticommut|anticomut",
    "Matrix_rank": r"Matrix\.rank|\.rank\b",
    "pureza_posto_um": r"\b(pure_iff\w*|rank_one\w*|trace_square_rank_one\w*)\b",
    "dephase_e_diagExpect": r"\b(def dephase|dephase_tendsto_expectation|def diagExpect)\b",
}


def main():
    if os.path.exists(DEST):
        print("FALHA VISIVEL: destino ja existe (nao sobrescrevo): " + DEST, file=sys.stderr)
        return 2
    out = dict(documento="consulta so-leitura: kernel do Nos e inventario da bancada (rodada 2 do construtor otico)",
               quando_local=time.strftime("%Y-%m-%d %H:%M:%S"), kernel=KERNEL, padroes=PADROES, kernel_achados={}, inventario={})
    arquivos = []
    for sub in ("TGLExt", "TGL"):
        base = os.path.join(KERNEL, sub)
        for dp, dns, fns in os.walk(base):
            dns[:] = sorted(d for d in dns if d != ".lake")
            for fn in sorted(fns):
                if fn.endswith(".lean"):
                    arquivos.append(os.path.join(dp, fn))
    out["kernel_n_arquivos_lean_varridos"] = len(arquivos)
    for nome, pat in PADROES.items():
        rx = re.compile(pat)
        achados = []
        for p in arquivos:
            raw = open(p, "rb").read()
            txt = raw.decode("utf-8", errors="replace")
            for i, linha in enumerate(txt.splitlines(), 1):
                if rx.search(linha):
                    achados.append(dict(arquivo=os.path.relpath(p, KERNEL).replace("\\", "/"), linha=i, texto=linha.strip()[:160],
                                        sha16=hashlib.sha256(raw).hexdigest()[:16]))
        out["kernel_achados"][nome] = dict(n=len(achados), primeiros=achados[:25])
    inv_raw = open(INVENT, "rb").read()
    inv = json.loads(inv_raw.decode("utf-8"))
    out["inventario"]["arquivo"] = INVENT
    out["inventario"]["sha256"] = hashlib.sha256(inv_raw).hexdigest()
    out["inventario"]["numeros"] = inv.get("numeros")
    for nome, pat in PADROES.items():
        rx = re.compile(pat)
        achados = []
        for u in inv.get("unicos", []):
            for dcl in u.get("decls", []):
                if rx.search(dcl):
                    achados.append(dict(arquivo=u["arquivo"], sha16=u["sha16"], decl=dcl, vigente=u.get("vigente")))
        out["inventario"][nome] = dict(n=len(achados), primeiros=achados[:25])
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps({k: v["n"] for k, v in out["kernel_achados"].items()}, ensure_ascii=False),
          json.dumps({k: v["n"] for k, v in out["inventario"].items() if isinstance(v, dict) and "n" in v}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
