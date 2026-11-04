# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): (1) renderiza _paragrafo_v407_de sobre dry_v407/core_ensaio.json e roda verificar_paragrafo_v407 (controle negativo: ressalva cortada reprova);
(2) roda as guardas (P18 + frases v407) sobre TODOS os textos publicos (pysnips, delta/registros, pedras, textos rendidos do harness); (3) confere as RESSALVAS_V407 inteiras nos textos rendidos."""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
sys.path.insert(0, R); sys.path.insert(0, R + "pos_rito")
import delta_v407 as DL
import guarda_p18_v407 as G18
import guarda_frases_v407 as GF
import importlib.util
spec = importlib.util.spec_from_file_location("textos_v407_rev", R + "pos_rito/textos_v407.py"); T = importlib.util.module_from_spec(spec); sys.modules["textos_v407_rev"] = T; spec.loader.exec_module(T)
core = json.load(open(R + "dry_v407/core_ensaio.json", encoding="utf-8"))["core"]
esp = json.load(open(R + "ESPERADOS_v407.json", encoding="utf-8"))
par = T._paragrafo_v407_de(core)
fa = T.verificar_paragrafo_v407(par, core, esp)
print("paragrafo: %d chars; verificacoes falhas: %s" % (len(par), fa))
open(R + "revisao_terceiro/paragrafo_renderizado_R3.txt", "w", encoding="utf-8").write(par)
# controle negativo: ressalva 10 cortada
par_cortado = par.replace(T._sem_chaves(DL.RESSALVAS_V407[9]), T._sem_chaves(DL.RESSALVAS_V407[9]).split(":")[0])
print("controle negativo (ressalva 10 cortada) reprova:", bool(T.verificar_paragrafo_v407(par_cortado, core, esp)))
# ressalvas em cada texto rendido
ress = [T._sem_chaves(r) for r in DL.RESSALVAS_V407]
out = {"paragrafo_falhas": fa, "guardas": {}, "ressalvas_no_paragrafo": [r in par for r in ress]}
print("ressalvas inteiras no paragrafo:", sum(out["ressalvas_no_paragrafo"]), "de", len(ress))
# guardas sobre arquivos
arqs = [R + "artigo_pt_v407.pysnip", R + "artigo_en_v407.pysnip", R + "registros_v407.py", R + "runtime_v407.py", R + "delta_v407.py", R + "pos_rito/textos_v407_novo.pysnip", R + "pos_rito/textos_v407.py", R + "pos_rito/textos_custodia_handoff_v407_03nov.py"]
arqs += sorted(glob.glob("C:/t/h407/harness_saida_v407/textos/*.txt"))
for a in arqs:
    t = open(a, encoding="utf-8").read()
    v1 = G18.violacoes(t); v2 = GF.violacoes(t)
    out["guardas"][os.path.basename(a)] = {"p18": [list(x) for x in v1[:6]], "frases": [list(x) for x in v2[:6]]}
    if v1 or v2:
        print("GUARDA ACHOU em", os.path.basename(a), "P18:", v1[:3], "| frases:", v2[:3])
print("arquivos varridos:", len(arqs), "| com achado:", sum(1 for v in out["guardas"].values() if v["p18"] or v["frases"]))
# pedras
ped = GF.pedras(); print("pedras():", {k: (len(v["violacoes"]), v["falas_retiradas"], v["apontadas"]) for k, v in ped.items()})
# pedras SEM a excecao das apontadas: o que a guarda diz do texto cru
import runtime_v407 as RT
for p in DL.PEDRAS_V407:
    t = open(p["src"], encoding="utf-8").read(); v = RT._v407_guarda_frases(t)
    if v: print("pedra (cru, sem retirar falas):", p["name"], [(x[0], x[1][:90]) for x in v[:4]])
out["pedras"] = ped
cn = GF.controle_negativo(); print("controle_negativo():", cn["ok"])
json.dump(out, open(R + "revisao_terceiro/r3_h_guardas_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
