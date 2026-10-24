# -*- coding: utf-8 -*-
"""construir_probe_nomes.py -- le probe_nomes_lista.json (gerado por conferir_cabecalho.py) e escreve C:\\t\\k398b\\probe\\afin_nomes.lean com um `#check @nome` por
identificador citado nos docstrings (menos arquivos, letras soltas e o modulo TGLExt.TheStation, conferido a parte). So escreve no sandbox k398b\\probe.
Uso: python -I -B -X utf8 construir_probe_nomes.py
"""
import json
import os

W = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398"
PROBE = r"C:\t\k398b\probe\afin_nomes.lean"
nomes = json.load(open(os.path.join(W, "probe_nomes_lista.json"), encoding="utf-8"))
EXCLUI_MODULO = {"TGLExt.TheStation", "AfinacaoDasCordas"}  # modulos / o nome da pedra (o modulo TGLExt.AfinacaoDasCordas e' importado pelos probes)
saida = []
excl = []
for n in nomes:
    if n.endswith(".tex") or n.endswith(".txt") or len(n) == 1 or n in EXCLUI_MODULO:
        excl.append(n)
        continue
    saida.append(n)
linhas = [
    "import TGLExt.AfinacaoDasCordas",
    "",
    "open ChatgptAudit.PolarPeriod016 TGLExt.AfinacaoDasCordas",
    "",
]
for n in saida:
    linhas.append("#check @" + n)
open(PROBE, "w", encoding="utf-8", newline="\n").write("\n".join(linhas) + "\n")
json.dump({"checados": saida, "excluidos": excl}, open(os.path.join(W, "probe_nomes_construido.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(len(saida), "nomes no probe;", len(excl), "excluidos:", excl)
