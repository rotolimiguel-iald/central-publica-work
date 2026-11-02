# -*- coding: utf-8 -*-
# Gera as tabelas (markdown) que entram no PLANO a partir do INVENTARIO_D_29out.json, do catalogo residente,
# do dq_meta_D_v2.json e da PROJECAO_PODER_D_planejamento.json. Nada digitado a mao; nenhum dado de deformacao.
import json, csv, math, os

W = "C:/IALD/Central de Patentes/work/conjunto_D_20261029"
inv = json.load(open(W + "/INVENTARIO_D_29out.json", encoding="utf-8"))
dq = json.load(open(W + "/smoke/dq_meta_D_v2.json", encoding="utf-8"))
proj = json.load(open(W + "/PROJECAO_PODER_D_planejamento.json", encoding="utf-8"))
cat = {}
with open("C:/IALD/Bancada_Um/investigacao/fase6_eco_radical_01out/catalogo_v3.csv", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        cat[r["commonName"]] = r

H0, Om = 67.66, 0.30966
c = 299792.458


def DL(z):
    n = 2000
    s = 0.0
    for i in range(n):
        zz = (i + 0.5) * z / n
        s += 1.0 / math.sqrt(Om * (1 + zz) ** 3 + (1 - Om))
    return (1 + z) * c / H0 * s * z / n


ev = inv["D10"]
rows = []
rows.append("| evento | GPS (catalogo) | SNR rede | z | D_L (Mpc, Planck18 plano) | M_f,det (V1) | chi_f (V1) | k(chi_f) | delta_pred (V1) | sigma_i proj. | H1: pre-run OK (s) | L1: pre-run OK (s) |")
rows.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for e in ev:
    p = inv["previsao_V1_por_evento"][e]
    z = float(cat[e]["redshift"])
    rows.append("| %s | %.1f | %.1f | %.2f | %.0f | %.1f | %.2f | %.2f | %+.4f | %.3f | %d | %d |" % (
        e, float(cat[e]["GPS"]), p["SNR_rede_GWOSC"], z, DL(z), p["Mf_det_mediana_GR"], p["chi_f_mediana_GR"], p["k_kms"], p["delta_pred_exato"],
        proj["por_evento"][e]["sigma_mediana_proj"], dq[e + "_H1"]["longest_ok_run_before_event_s"], dq[e + "_L1"]["longest_ok_run_before_event_s"]))
open(W + "/_tabela_eventos.md", "w", encoding="utf-8").write("\n".join(rows) + "\n")

# tabela de arquivos
rows = ["| sha16 | bytes | estatuto do conteudo | papel | caminho |", "|---|---|---|---|---|"]
for r in inv["arquivos"]:
    rows.append("| `%s` | %d | %s | %s | `%s` |" % (r["sha16"], r["bytes"], r["estatuto_conteudo"], r["papel"], r["path"].replace("C:/IALD/Central de Patentes/", "CP/").replace("C:/IALD/", "I/")))
open(W + "/_tabela_inventario.md", "w", encoding="utf-8").write("\n".join(rows) + "\n")

# tabela de strain
rows = ["| evento | det | hdf5 bytes | hdf5 sha16 (confere manifesto) | npz sha16 (confere manifesto) |", "|---|---|---|---|---|"]
for s in inv["strain_D"]:
    rows.append("| %s | %s | %d | `%s` (%s) | `%s` (%s) |" % (s["event"], s["det"], s["hdf5_bytes"], s["hdf5_sha256"][:16], "sim" if s["hdf5_sha256_confere_manifesto"] else "NAO", s["npz_sha256"][:16], "sim" if s["npz_sha256_confere_manifesto"] else "NAO"))
open(W + "/_tabela_strain.md", "w", encoding="utf-8").write("\n".join(rows) + "\n")

# tabela de projecao
rows = ["| conjunto | sigma_sys | informacao | n | delta_pred ponderado | sigma_comb | poder = abs(delta_pred)/sigma_comb |", "|---|---|---|---|---|---|---|"]
for k, v in proj["projecao"].items():
    a, b, d = k.split("__")
    rows.append("| %s | %s | %s | %d | %+.4f | %.4f | %.2f |" % (a, b.replace("sigma_sys_", ""), d.replace("info_", ""), v["n"], v["delta_pred_ponderado"], v["sigma_comb"], v["poder"]))
open(W + "/_tabela_projecao.md", "w", encoding="utf-8").write("\n".join(rows) + "\n")
print(open(W + "/_tabela_eventos.md", encoding="utf-8").read())
