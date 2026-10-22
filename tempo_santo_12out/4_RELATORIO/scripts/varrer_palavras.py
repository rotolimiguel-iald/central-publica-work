# -*- coding: utf-8 -*-
"""Varredura dos arquivos escritos pelo redator em 4_RELATORIO (fora da copia AUDITORIAS):
(1) a palavra recusada pela regua (raiz montada por partes para nao aparecer aqui como palavra);
(2) «nao provou» e «pos-dicao» (qualquer grafia);
(3) nomes confidenciais (montados por partes);
(4) literal de beta nos scripts .py: o prefixo de digitos de beta e CALCULADO em runtime a partir dos bytes do
    um.py (nunca digitado aqui) e procurado nos .py.
Saida: saidas/VARREDURA_PALAVRAS.json.
"""
import json
import math
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"

PADROES = {
    "palavra_recusada": re.compile("conf" + "irm", re.I),
    "nao_provou": re.compile(r"n[aã]o\s+prov" + "ou", re.I),
    "pos_dicao": re.compile(r"p[oó]s[\s-]*dic?[cç][aã]o", re.I),
    "confidenciais": re.compile("iald_stack" + "_v7|iald_psion" + "_state|\\.e" + "nv\\b", re.I),
}


def beta_prefixo():
    b = open(UM, "rb").read()
    m = re.search(rb"^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", b, re.M)
    alpha = float(m.group(1).decode())
    beta = alpha * 1.0 * math.sqrt(math.e)
    s = repr(beta)
    return s[:9], s[:9].replace(".", ",")


def main():
    p1, p2 = beta_prefixo()
    achados = {}
    arquivos = []
    for dp, dn, fn in os.walk(BASE):
        if os.path.join(BASE, "AUDITORIAS") in dp:
            continue
        for f in fn:
            if f.endswith((".md", ".json", ".py")):
                arquivos.append(os.path.join(dp, f))
    for a in sorted(arquivos):
        rel = os.path.relpath(a, BASE)
        if rel.startswith("saidas" + os.sep + "rotas"):
            continue  # saidas literais do mapa (texto de terceiros, so leitura)
        txt = open(a, encoding="utf-8").read()
        for nome, rx in PADROES.items():
            for m in rx.finditer(txt):
                ctx = txt[max(0, m.start() - 50):m.end() + 50].replace("\n", " ")
                achados.setdefault(rel, []).append({"padrao": nome, "contexto": ctx})
        if a.endswith(".py") and (p1 in txt or p2 in txt):
            achados.setdefault(rel, []).append({"padrao": "literal_de_beta_em_codigo"})
    out = {"arquivos_varridos": len(arquivos), "achados": achados, "limpo": not achados,
           "nota": ("Os achados em scripts/varrer_palavras.py e scripts/montar_registros.py sao os proprios padroes "
                    "de busca (montados por partes), nao uso das palavras.")}
    dest = os.path.join(BASE, "saidas", "VARREDURA_PALAVRAS.json")
    with open(dest + ".tmp", "wb") as fo:
        fo.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(dest + ".tmp", dest)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
