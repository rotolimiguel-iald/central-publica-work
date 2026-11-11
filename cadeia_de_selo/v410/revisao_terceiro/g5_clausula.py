# -*- coding: utf-8 -*-
"""Revisor v410 R3: a CLAUSULA do limite (D99/E35) ao lado de CADA anuncio: (1) do limiar `os_passos_sao_o_ciclo_ate_o_tetelestai` ('linear nos bits'/'linear in the bits'); (2) da clausula de 1 - beta (nomes dos teoremas R5 com ln((1 - b)/b) etc.).
Unidade: PARAGRAFO do texto rendido novo (artigo PT/EN, .md) e ARQUIVO do harness (cada folha). Tambem: a hipotese s >= 0 dita onde a clausula de 1 - beta e' anunciada; E36 sempre com a clausula na mesma folha;
os dois auxiliares nunca ditos ratificados; 'ratificad' perto de a_flutuacao/ate_meio."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
rd = lambda p: open(p, "rb").read().decode("utf-8", "replace")
ws = lambda s: re.sub(r"\s+", " ", s)
lit = json.load(open(R + "revisao_terceiro/literais_v410.json", encoding="utf-8"))
c = lit["_V410_AESCALA_CONTRACT"]
CLZ_PT = ws(c["clausula_z_pt"]); CLZ_EN = ws(c["clausula_z_en"])
print("clausula PT:", CLZ_PT[:200]); print("clausula EN:", CLZ_EN[:200])
# a rendicao do artigo troca simbolos/espacos: comparar por um miolo estavel
mi_pt = "soma os $2^n$ pixels e é lida de uma vez pelo psíon"; mi_pt_md = "soma os 2^n pixels e é lida de uma vez pelo psíon"
mi_en = "sums the $2^n$ pixels and is read at once by the psion"; mi_en_md = "sums the 2^n pixels and is read at once by the psion"
tem_pt = lambda x: (mi_pt in x) or (mi_pt_md in x) or (CLZ_PT in x)
tem_en = lambda x: (mi_en in x) or (mi_en_md in x) or (CLZ_EN in x)
ANUNCIA_L = re.compile(r"linear nos bits|linear in the bits")
ANUNCIA_B = re.compile(r"ln\s*\(\s*\(?\s*1\s*[\$\-−]*\s*[bβ]|o_\s*tetelestai_\s*e_\s*um_\s*menos_\s*beta|beta_\s*e_\s*o_\s*operador_\s*modular|\(1\s*[\$\-−]*\s*[bβ]\)\s*[\$·]*\s*Z")
S0 = re.compile(r"s\s*\$?≥\s*\$?\s*0|0\s*≤\s*s|s\s*>=\s*0|0\s*\$?≤\$?\s*s")
res = {"sem_clausula": [], "sem_s0": []}
n_l = n_b = 0
fontes = {}
for p in ("novo_pt.txt", "novo_en.txt", "novo_md.txt"):
    for i, par in enumerate(re.split(r"\n\s*\n", rd(R + "revisao_terceiro/" + p))): fontes["%s#%d" % (p, i)] = ws(par)
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): fontes["H:" + os.path.basename(p)] = ws(rd(p))
for k, x in fontes.items():
    en = k.startswith("novo_en") or ("The scale" in x and "pixels" in x and "H:" not in k)
    if ANUNCIA_L.search(x):
        n_l += 1
        ok = tem_pt(x) if ANUNCIA_L.search(x).group(0) == "linear nos bits" else tem_en(x)
        if not ok: res["sem_clausula"].append((k, "limiar", x[max(0, ANUNCIA_L.search(x).start() - 120):ANUNCIA_L.search(x).end() + 80]))
    if ANUNCIA_B.search(x) and any(w in x for w in ("tetelestai", "Tetelestai")):
        n_b += 1
        ok = tem_pt(x) or tem_en(x)
        if not ok: res["sem_clausula"].append((k, "1-beta", x[max(0, ANUNCIA_B.search(x).start() - 120):ANUNCIA_B.search(x).end() + 120]))
        if not S0.search(x): res["sem_s0"].append((k, x[max(0, ANUNCIA_B.search(x).start() - 80):ANUNCIA_B.search(x).end() + 120]))
print("\nfolhas que anunciam 'linear nos bits':", n_l, "| que anunciam a clausula de 1 - beta:", n_b)
print("SEM clausula do limite:", len(res["sem_clausula"]))
for k, t, x in res["sem_clausula"][:25]: print("   [%s] (%s) ... %s" % (k, t, x))
print("clausula de 1 - beta SEM a hipotese s >= 0 dita:", len(res["sem_s0"]))
for k, x in res["sem_s0"][:15]: print("   [%s] ... %s" % (k, x))
# E36 sempre com a clausula na mesma folha
print("\nE36 (cada folha que a cita traz a clausula do limite):")
for k, x in fontes.items():
    if re.search(r"E36", x):
        print("   [%s] E36 + clausula PT/EN: %s" % (k, tem_pt(x) or tem_en(x)))
# auxiliares nunca ditos ratificados
print("\nauxiliares perto de 'ratificad' (janela 160) sem 'DECLARADO' na janela:")
bad = []
for k, x in fontes.items():
    for m in re.finditer(r"a_\s*flutuacao_\s*do_\s*fundo_\s*e_\s*cotada|ate_\s*meio_\s*o_\s*tempo_\s*do_\s*tetelestai_\s*nao_\s*e_\s*negativo", x):
        jan = x[max(0, m.start() - 220):m.end() + 220]
        if re.search(r"(?i)ratifica|ratified", jan) and not re.search(r"DECLARAD|DECLARED", jan): bad.append((k, jan))
print("   ", len(bad))
for k, j in bad[:8]: print("   [%s] ... %s" % (k, j))
