# -*- coding: utf-8 -*-
"""ilustracao_contaminacao_8k.py -- NAO-CEGO, ILUSTRACAO, NAO VEREDITO (G2/G6d). Estende aos 8 k a ilustracao do critico
(CRITICO_RECOMPUTO2.json): z_excl = (dbar_registro - delta_exato)/sigma_comb com a deformacao comum dos 31 JA NO REGISTRO desde 22/09
(+0,072; memoria ordem-013-confrontacao-ringdown.md l.102; a mesma constante que o critico usou). Nenhum dado novo lido.
Tambem: E_rad do GW250114 a partir das razoes de massa da lente fisica (KNOWN). Saida: ILUSTRACAO_CONTAMINACAO_8K.json."""
import json, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))
def sha(p): return hashlib.sha256(open(p,"rb").read()).hexdigest()
pv = os.path.join(HERE, "PODER_CEGO_RAMO_B_v2.json"); j = json.load(open(pv, encoding="utf-8"))
pf = os.path.join(HERE, "..", "fisica_do_ramo_b", "RAMO_B_FISICA_TABELAS.json"); f = json.load(open(pf, encoding="utf-8"))
pc = os.path.join(HERE, "..", "critico", "CRITICO_RECOMPUTO2.json"); c = json.load(open(pc, encoding="utf-8"))
dbar = 0.072  # [NAO-CEGO] deformacao comum registrada 22/09 (memoria l.102); identica a do critico_recomputo2.py
out = {"fontes": {"PODER_CEGO_RAMO_B_v2.json": sha(pv)[:16], "RAMO_B_FISICA_TABELAS.json": sha(pf)[:16], "CRITICO_RECOMPUTO2.json": sha(pc)[:16]},
       "estatuto": "NAO-CEGO; ilustracao da contaminacao do conjunto A; nao e veredito nem poder; dbar_registro = +0,072 (memoria 22/09)",
       "z_excl_ilustracao_8k": {}, "conferencia_com_critico_5k": {}}
for nome, r in j["resultados"].items():
    e = r["GWTC5_31_std"]; z = (dbar - e["delta_pred_weighted_exact"]) / e["sigma_comb"]
    out["z_excl_ilustracao_8k"][nome] = {"delta_exato_31": e["delta_pred_weighted_exact"], "sigma_comb": e["sigma_comb"], "z_excl_se_o_registro_valer": z, "legivel_hoje_a_5sigma": z >= 5}
for nome, r in c["ILUSTRACAO_CONTAMINACAO_conjunto_A"]["valores"].items():
    out["conferencia_com_critico_5k"][nome] = {"critico": r["z_excl_se_o_registro_valer_(NAO_CEGO, ilustracao)"], "aqui": out["z_excl_ilustracao_8k"][nome]["z_excl_se_o_registro_valer"]}
m = f["massas_GW250114"]; k = f["GW250114_KNOWN"]
out["GW250114_massas_KNOWN"] = {"M_f_src": k["M_f_src"], "M_f_det": k["M_f_det"], "m1_src": k["m1_src"], "m2_src": k["m2_src"], "one_plus_z": m["one_plus_z"],
                               "M_tot_src": m["M_tot_src"], "M_chirp_src": m["M_chirp_src"], "ratio_tot_over_f": m["ratio_tot_over_f"], "ratio_chirp_over_f": m["ratio_chirp_over_f"],
                               "E_rad_fraction_of_Mtot_DERIVED": 1 - 1 / m["ratio_tot_over_f"], "ratio_Mf_det_over_src": k["M_f_det"] / k["M_f_src"]}
out["tabela_4pi_do_v2"] = j["tabela_k_x_chi_lida_da_fisica"]["k=4π (calculado aqui, mesmo N BCW)"]
po = os.path.join(HERE, "ILUSTRACAO_CONTAMINACAO_8K.json"); json.dump(out, open(po, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)); print("saida:", po, sha(po)[:16], os.path.getsize(po), "B")
