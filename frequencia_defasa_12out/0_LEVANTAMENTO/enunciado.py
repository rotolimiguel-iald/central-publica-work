# -*- coding: utf-8 -*-
# Imprime o enunciado (da linha da declaracao ate ':=' ) de declaracoes do kernel do Nos, por nome qualificado. Somente leitura.
import json, sys, os
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel\\"
idx = json.load(open(os.path.join(AQUI, "KERNEL_INDICE.json"), encoding="utf-8"))
alvo = set(sys.argv[1:])
for d in idx["declaracoes"]:
    if d["qual"] in alvo or d["name"] in alvo:
        p = RAIZ + d["file"].replace("/", "\\")
        L = open(p, encoding="utf-8").read().splitlines()
        i = d["line"] - 1
        # docstring imediatamente acima (ate 12 linhas)
        j = i - 1
        doc = []
        while j >= 0 and i - j <= 14:
            doc.insert(0, L[j])
            if L[j].lstrip().startswith("/--") or L[j].lstrip().startswith("/-!"):
                break
            if L[j].strip() == "" and not doc[1:]:
                break
            j -= 1
        if not any(x.lstrip().startswith("/--") for x in doc):
            doc = []
        body = []
        k = i
        while k < len(L) and k < i + 14:
            body.append(L[k])
            if ":=" in L[k]:
                break
            k += 1
        print("=" * 8, d["qual"], f'{d["file"]}:{d["line"]}', idx["arquivos"][d["file"]]["sha16"])
        for x in doc:
            print("   ", x[:200])
        for x in body:
            print("   ", x[:200])
