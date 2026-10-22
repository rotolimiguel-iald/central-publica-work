# -*- coding: utf-8 -*-
"""ERRATA AO LADO (gerencia, em nome proprio): a gravacao da 4a passada indexou os itens por id e, como o mesmo id aparece em mais de uma lente, OMITIU
entradas e contou 38/9/3 por id unico. Aqui: acrescenta ao AFERIDOR_v384.txt as entradas omitidas (verbatim) e corrige, nas disposicoes, as contagens --
por entrada (lente x item) e por item unico com o PIOR estado. So acrescimo; backup de bytes."""
import hashlib, json, os, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
A4 = json.load(open(os.path.join(HERE, "afericao4_resultado.json"), encoding="utf-8"))
ENT = [(g["lente"], a) for g in A4["grupos"] for a in (g.get("itens") or [])]
ultimo = {}
for i, (l, a) in enumerate(ENT):
    ultimo[a["id"]] = i
omitidas = [(l, a) for i, (l, a) in enumerate(ENT) if ultimo[a["id"]] != i]
ORD = {"RESOLVIDO": 0, "PARCIAL": 1, "NAO_RESOLVIDO": 2, "REGRESSAO": 3}
pior = {}
for l, a in ENT:
    if a["id"] not in pior or ORD[a["estado"]] > ORD[pior[a["id"]]]:
        pior[a["id"]] = a["estado"]
c_ent = Counter(a["estado"] for _, a in ENT); c_id = Counter(pior.values())
print("entradas", len(ENT), dict(c_ent), "| ids unicos", len(pior), dict(c_id), "| omitidas", len(omitidas))
L = ["\n" + "-" * 80, "ERRATA AO LADO (gerencia, %s): a gravacao acima da 4a passada indexou por id e OMITIU %d entradas de id repetido em outra lente; ei-las, verbatim. "
     "Contagem correta: %d entradas (lente x item) = %s; %d itens unicos pelo PIOR estado = %s." % (time.strftime("%d/%m/%Y %H:%M"), len(omitidas), len(ENT), dict(c_ent), len(pior), dict(c_id)), "-" * 80]
for l, a in omitidas:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"ERRATA AO LADO (gerencia" in raw and b"OMITIU" in raw:
    print("errata ja gravada")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + ("\n".join(L) + "\n").encode("utf-8"); open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    print("AFERIDOR:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
open(dp + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(open(dp, "rb").read())
D["passada4"]["itens_da_3a"] = {"por_entrada_lente_x_item": dict(c_ent), "n_entradas": len(ENT), "por_item_unico_pior_estado": dict(c_id), "n_itens_unicos": len(pior),
                                "errata": "a contagem anterior (38/9/3) era por id com a ultima lente; corrigida ao lado"}
nao_resolvidos = sorted(k for k, v in pior.items() if v != "RESOLVIDO")
assert all(k in D["disposicoes_4a_itens"] for k in nao_resolvidos), [k for k in nao_resolvidos if k not in D["disposicoes_4a_itens"]]
base = D["texto_para_o_pre_registro"].split("; 4ª passada")[0]
nov = D["passada4"]["novos"]; sob = D["passada4"]["sobreviventes"]
D["texto_para_o_pre_registro"] = base + ("; 4ª passada (conferência das correções da 3ª): %d entradas (item × lente) — %d resolvidas, %d parciais e %d regressões; por item, pelo pior estado, "
                                         "%d de %d ainda pediam correção; %d achados novos, %d sobreviventes à verificação (quase todos de severidade baixa); tratados no código ou no texto antes deste documento") % (
    len(ENT), c_ent.get("RESOLVIDO", 0), c_ent.get("PARCIAL", 0), c_ent.get("REGRESSAO", 0), len(nao_resolvidos), len(pior), nov, sob)
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); open(dp + ".tmp", "wb").write(b); os.replace(dp + ".tmp", dp)
print("nao resolvidos (pior estado):", nao_resolvidos); print(D["texto_para_o_pre_registro"][-420:])
