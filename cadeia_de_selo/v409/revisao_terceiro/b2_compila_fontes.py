# -*- coding: utf-8 -*-
"""Revisor v409 R1: compilacao INDEPENDENTE das fontes embutidas (pedra/ == embutido == sandbox): copia cada .lean para o sandbox como zz_rev_<Nome>.lean, acrescenta os #print axioms das ancoras e roda `lake env lean`
(UM processo por vez; nunca lake build). As copias sao APAGADAS ao fim (run_lean2.sh). So escreve nesta pasta; as copias no sandbox sao temporarias."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
c = json.load(open(R + "CANDIDATO_v409.json", encoding="utf-8"))
anc = list(c["kernel"]["ancoras"].keys())
os.makedirs(R + "revisao_terceiro/_fontes_compilar", exist_ok=True)
for nome in ("TraducaoTuring", "ParNaFaceDeFock"):
    t = open(R + "pedra/" + nome + ".lean", "rb").read().decode("utf-8")
    L = [t.rstrip("\n"), ""]
    L += ["#print axioms " + a for a in anc if a.startswith("TGLExt." + nome + ".")]
    open(R + "revisao_terceiro/_fontes_compilar/zz_rev_%s.lean" % nome, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(nome, len([a for a in anc if a.startswith("TGLExt." + nome + ".")]))
