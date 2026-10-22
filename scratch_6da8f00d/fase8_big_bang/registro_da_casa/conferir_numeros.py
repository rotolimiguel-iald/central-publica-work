# -*- coding: utf-8 -*-
"""Conferência por script (lente: registro da casa, Fase 8 Big Bang).
β nunca literal: α lido do um.py por regex em runtime; β = α·√e.
Só leitura fora desta pasta. Não roda o um.py."""
import re, io, math, json, hashlib, os

UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
src = io.open(UM, encoding="utf-8", errors="replace").read()
m = re.search(r"SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", src)
if not m:
    m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", src)
alpha = float(m.group(1))
beta = alpha * math.sqrt(math.e)
out = {"alpha_regex": alpha, "beta": beta}

# (1) o canal N_eff da casa (prove_rho_plus_p_closure / prove_neff_channel)
F = (7.0/8.0) * (4.0/11.0) ** (4.0/3.0)
N_SM = 3.044
dNdb = (4.0/3.0) * (1.0 + F*N_SM) / F
dN = dNdb * beta
Neff_pred = N_SM + dN
out["F"] = F; out["dNeff_dbeta"] = dNdb; out["Delta_Neff"] = dN; out["Neff_pred"] = Neff_pred
# a leitura da gerência (05/10): δ = 4β/3 lido como fração da radiação total
delta_rad = 4.0*beta/3.0
dN_gerencia = delta_rad * (1.0 + F*N_SM) / F
out["delta_4beta_3"] = delta_rad; out["Delta_Neff_gerencia"] = dN_gerencia
out["identicos"] = abs(dN_gerencia - dN) < 1e-12

# (2) tensões contra as medidas tabuladas no frozen TGL_NEFF_V1 (10_frozen_neff_v1.py)
medidas = [
    (2.92, 0.19, "Planck 2018 TT,TE,EE+lowE", "arXiv:1807.06209"),
    (2.99, 0.17, "Planck 2018 +lensing+BAO", "arXiv:1807.06209"),
    (2.86, 0.13, "ACT DR6 + Planck (P-ACT-LB)", "arXiv:2503.14454"),
    (2.89, 0.11, "ACT DR6 + Planck + BBN", "arXiv:2503.14454"),
    (2.97, 0.12, "SPT-3G D1 + Planck + ACT (CMB-SPA)", "arXiv:2506.20707"),
]
out["tensoes_vs_centro_medido"] = [
    {"fonte": r, "ref": s, "obs": v, "sigma": e,
     "tensao_centro": abs(Neff_pred - v)/e,
     "delta_sobre_sigma_(a conta da gerencia)": dN/e,
     "sigma_beta_implicado": e/dNdb}
    for v, e, r, s in medidas]
out["sigma_Neff_que_mata_centro_atual_2p97"] = abs(Neff_pred - 2.97)/5.0
out["sigma_Neff_que_mata_centro_padrao"] = dN/5.0
out["CMB_S4_0p03_separacao_TGL_SM"] = dN/0.03

# (3) BBN: H_TGL/H_LCDM na era da radiação e o D/H (Steigman 0,57), como no artigo (D8)
ratioH = math.sqrt(1.0 + (4.0/3.0)*beta)
steig = 0.57
ratioDH = ratioH ** steig
DH_LCDM_canonical = 2.515e-5
DH_TGL = DH_LCDM_canonical * ratioDH
DH_obs, DH_err = 2.527e-5, 0.030e-5
out["BBN"] = {"H_ratio": ratioH, "DH_ratio": ratioDH, "DH_TGL_pred": DH_TGL,
              "DH_obs": DH_obs, "DH_err": DH_err,
              "tensao_sigma_D8": abs(DH_TGL - DH_obs)/DH_err,
              "sigma_beta_de_DH_sozinho": (DH_err/DH_obs) / (steig * (4.0/3.0) / 2.0),
              "nota": "σ(β) de D/H sozinho = (σ_DH/DH) / (d ln DH/dβ), d ln DH/dβ = 0,57·(4/3)/2 = 0,38 ⟹ ~0,031: confere com o 0,0318 do evidence_audit"}

# (4) BBN circular por construção (tgl_paper_unified.py:4499): DH_LCDM := DH_obs / f(β_TGL) ⟹ χ²(β_TGL) = 0
DH_LCDM_circ = DH_obs / (ratioH ** steig)
pred_circ = DH_LCDM_circ * (ratioH ** steig)
out["BBN_circular_chi2_em_beta_TGL"] = ((pred_circ - DH_obs)/DH_err)**2

# (5) hashes lidos dos artefatos citados
def sha16(p):
    try:
        return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    except Exception as ex:
        return "AUSENTE: %s" % ex
arts = {
    "um.py": UM,
    "um_absoluto.json": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json",
    "um_absoluto_selo.json": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json",
    "10_frozen_neff_v1_resultado.json": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1_resultado.json",
    "10_frozen_neff_v1.py": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py",
    "12_nivel2_frozen_e_verossimilhanca.py": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\12_nivel2_frozen_e_verossimilhanca.py",
    "13_nivel2_resultado.json": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_resultado.json",
    "13_nivel2_chains.h5": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_chains.h5",
    "RESULTADOS.md (teste_acustico)": r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\RESULTADOS.md",
    "JUIZ_LA_V1_RESULT.json": r"C:\IALD\Artigo\BANCADA_TOE\juiz_lA\JUIZ_LA_V1_RESULT.json",
    "C1_F1_calibracao_previsao.json": r"C:\IALD\Bancada_Um\investigacao\C1_F1_calibracao_previsao.json",
    "M1_mapa_de_R.json": r"C:\IALD\Bancada_Um\investigacao\M1_mapa_de_R.json",
    "RESULTADO_FASE1_EFF_20260930.json": r"C:\IALD\Bancada_Um\investigacao\fase1_eff_30set\RESULTADO_FASE1_EFF_20260930.json",
    "errata_cosmologica_TGL.tex": r"C:\IALD\Artigo\Haja_Luz\Manuscrito\errata_cosmologica_TGL.tex",
    "tgl_paper_unified.py": r"C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py",
    "RhoPlusPClosure.lean": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\RhoPlusPClosure.lean",
    "ThermodynamicFriedmann.lean": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\ThermodynamicFriedmann.lean",
    "TheAxiomAndTheFalseWitness.lean": r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheAxiomAndTheFalseWitness.lean",
    "camb_lcdm_v1.npz (Bancada)": r"C:\IALD\Bancada_Um\tabelas\camb_lcdm_v1.npz",
    "cooke_2018_DH.json (cache acom)": r"C:\IALD\projetos_pyhton\acom\tgl_data_cache\cooke_2018_DH.json",
}
out["sha16"] = {k: sha16(p) for k, p in arts.items()}
out["bytes"] = {k: (os.path.getsize(p) if os.path.exists(p) else None) for k, p in arts.items()}

# (6) o selo: versão corrente lida do artefato
selo = json.load(io.open(arts["um_absoluto_selo.json"], encoding="utf-8"))
out["selo_um_version"] = selo.get("um_version")
out["selo_result_hash"] = str(selo.get("result_hash"))[:16]
out["selo_formal_source_hash"] = str(selo.get("formal_source_hash"))[:16]
out["selo_timestamp"] = selo.get("timestamp")

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NUMEROS_CONFERIDOS.json")
json.dump(out, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
