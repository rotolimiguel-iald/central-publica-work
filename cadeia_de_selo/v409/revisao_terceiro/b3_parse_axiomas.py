# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/"
t = open(R + "axiomas_terceiro_out.txt", encoding="utf-8").read()
c = json.load(open(R + "../CANDIDATO_v409.json", encoding="utf-8")); anc = list(c["kernel"]["ancoras"].keys())
trio = {"propext", "Classical.choice", "Quot.sound"}
ax = {}
for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", t):
    ax[m.group(1)] = sorted(x.strip() for x in re.sub(r"\s+", " ", m.group(2)).split(",") if x.strip())
sem = [a for a in anc if a not in ax]
fora = {a: v for a, v in ax.items() if not set(v) <= trio or not v}
apenas_propext = [a for a, v in ax.items() if v == ["propext"]]
print("impressos:", len(ax), "| ancoras no candidato:", len(anc), "| ancoras sem print:", sem, "| fora do trio/vazios:", fora, "| so propext:", apenas_propext, "| sorryAx:", "sorryAx" in t)
print("varredura:", re.findall(r"constantes varridas[^\n]*", t), re.findall(r"constantes FORA[^\n]*", t))
print("erros/warnings:", [l for l in t.split("\n") if re.search(r"\berror\b|warning:", l)][:5], "| rc:", re.findall(r"rc=\d+", t))
out = {"print_axioms_impressos": len(ax), "ancoras_no_candidato": len(anc), "todas_as_ancoras_impressas": not sem, "fora_do_trio": len(fora), "so_propext": apenas_propext,
       "varredura_metam": re.findall(r"constantes varridas[^\n]*", t)[0], "varredura_fora_do_trio_ou_sorryAx": 0 if "FORA do trio (ou com sorryAx): 0" in t else None,
       "rc": re.findall(r"rc=(\d+)", t), "tempo": open(R + "axiomas_terceiro_time.txt").read().strip(), "sandbox": "C:/t/k409c/final (copia axiomas_terceiro.lean apagada ao fim)"}
json.dump(out, open(R + "lean_r1_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# os #check: o enunciado
for m in re.finditer(r"^@?(TGLExt\.[A-Za-z_.]+) :", t, re.M): pass
