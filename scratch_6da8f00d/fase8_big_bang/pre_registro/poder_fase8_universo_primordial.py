# -*- coding: utf-8 -*-
"""poder_fase8_universo_primordial.py -- O PODER, AS CEGAS, da Fase 8 (beta na era da radiacao), 05/10/2026.
Lente «pre_registro» da Fase 8 (rascunho). Somente leitura fora desta pasta; nada da casa e executado (nem um.py, nem a Bancada).

O que este script faz, e so isso:
  (1) le alpha do um.py canonico POR REGEX (SEALED_CODATA_ALPHA) e poe beta = alpha*sqrt(e) em runtime -- nunca literal;
  (2) aplica a lei canonica delta<K_d> = beta*|1+w| nas tres eras (w = 1/3, 0, -1) -- a identidade de fundo rho_TGL = beta*(rho+p)
      (pedra TGLExt.RhoPlusPClosure; um.py prove_rho_plus_p_closure) -- e converte a era da radiacao em Delta N_eff
      pela MESMA formula do frozen TGL_NEFF_V1 (dN/dbeta = (4/3)(1+F*N_SM)/F);
  (3) le POR REGEX, do frozen 10_frozen_neff_v1.py (08/08/2026), a tabela MEDIDAS (valor, sigma, rotulo, arXiv, independente) e a
      tabela PROJECOES (sigma, instrumento, referencia, quando) -- nenhum numero de N_eff e digitado aqui;
  (4) le do 13_nivel2_resultado.json o sigma(beta) do Nivel 2 (a verossimilhanca completa do Planck com a TGL-S dentro do CAMB);
  (5) calcula o PODER = |previsao|/sigma (a regua da Fase 6: < 5 => NOT_FALSIFIED_UNDERPOWERED) para os TRES MAPAS:
        A  = N_eff (fechamento rho+p completo; leitura TGL-S)        -> CMB
        B  = so-materia ((1+beta)*Omega_m; o mapa de R efetivo de 30/09) -> nada na era da radiacao (poder ~ 0, dito)
        C  = speed-up do BBN (a mesma densidade lida em T ~ MeV)      -> Y_p e D/H
      e, ILUSTRACAO NAO-CEGA, o z de cada medida publicada contra a previsao (ja legivel; dito como tal);
  (6) grava PODER_FASE8_UNIVERSO_PRIMORDIAL.json ao lado, com os sha256 de cada fonte lida (calculados do artefato).

Constantes digitadas aqui, todas marcadas: N_SM = 3,044 [KNOWN]; as escalas do BBN (Steigman 2007; Cyburt+2016) [KNOWN -- forma
aproximada, A CONFERIR com codigo de BBN, AUSENTE em disco]; Y_p e D/H observados [KNOWN -- Aver+2021; Cooke+2018]; z_eq [KNOWN].
Regua: beta nunca literal; NOT_FALSIFIED nunca e CONFIRMED; nada move o gate.
"""
import hashlib, json, math, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "PODER_FASE8_UNIVERSO_PRIMORDIAL.json")
UM = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
FROZEN = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py"
FROZEN_RES = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1_resultado.json"
NIVEL2 = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_resultado.json"
NIVEL2_FROZEN = r"C:\IALD\Artigo\teste_acustico_beta_tgl_v1\12_nivel2_frozen.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def read_text(p, nbytes=None):
    with open(p, "rb") as f:
        b = f.read() if nbytes is None else f.read(nbytes)
    return b.decode("utf-8", errors="replace")


fontes = {}

# ---------------------------------------------------------------- (1) beta em runtime, alpha por regex do um.py (fail-closed)
src = read_text(UM, 4_000_000)
m = re.search(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", src, re.M)
if not m:
    raise SystemExit("FALHA: SEALED_CODATA_ALPHA nao encontrado no um.py -- recusa (fail-closed)")
alpha = float(m.group(1))
beta = alpha * math.sqrt(math.e)
m_ver = re.search(r'^UM_VERSION\s*=\s*"([^"]+)"', src, re.M)
um_version = m_ver.group(1) if m_ver else "AUSENTE"
m_om = re.search(r"omega_m\s*=\s*([0-9.]+)\s*#\s*\[EXT, Planck base\]", src)
omega_m_planck = float(m_om.group(1)) if m_om else None   # o mesmo literal que prove_rho_plus_p_closure usa
fontes["um.py"] = {"caminho": UM, "sha256": sha(UM), "bytes": os.path.getsize(UM), "um_version": um_version}

# ---------------------------------------------------------------- (2) a lei nas tres eras e a conversao em N_eff
F_NU = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)
N_SM = 3.044                                   # [KNOWN] Bennett+2020 (o mesmo do frozen e do um.py)
lei = {"w_radiacao_1_3": beta * abs(1 + 1.0 / 3.0),
       "w_materia_0": beta * abs(1 + 0.0),
       "w_lambda_m1": beta * abs(1 - 1.0)}
dNdb = (4.0 / 3.0) * (1.0 + F_NU * N_SM) / F_NU
dN = dNdb * beta
N_pred = N_SM + dN
# a conta da gerencia (05/10): Delta N_eff = delta*(1 + f*N_eff)/f com delta = 4beta/3
dN_gerencia = lei["w_radiacao_1_3"] * (1.0 + F_NU * N_SM) / F_NU
S_bbn = math.sqrt(1.0 + lei["w_radiacao_1_3"])   # H/H_SM na era da radiacao pura: H^2 -> (1 + 4beta/3) rho_r
dOmc = beta * omega_m_planck if omega_m_planck else None

# ---------------------------------------------------------------- (3) MEDIDAS e PROJECOES lidas por regex do frozen (nada digitado)
ftxt = read_text(FROZEN)
fontes["10_frozen_neff_v1.py"] = {"caminho": FROZEN, "sha256": sha(FROZEN), "bytes": os.path.getsize(FROZEN)}
fontes["10_frozen_neff_v1_resultado.json"] = {"caminho": FROZEN_RES, "sha256": sha(FROZEN_RES), "bytes": os.path.getsize(FROZEN_RES)}
blk = re.search(r"MEDIDAS\s*=\s*\[(.*?)\n\]", ftxt, re.S).group(1)
MEDIDAS = re.findall(r'\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*(True|False)\s*\)', blk)
blk2 = re.search(r"PROJECOES\s*=\s*\[(.*?)\n\]", ftxt, re.S).group(1)
PROJECOES = re.findall(r'\(\s*([0-9.]+)\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)', blk2)
if len(MEDIDAS) < 3 or len(PROJECOES) < 3:
    raise SystemExit("FALHA: tabelas do frozen nao lidas por regex -- recusa (fail-closed)")
fr = json.load(open(FROZEN_RES, encoding="utf-8"))
frozen_hash_gravado = fr.get("frozen_hash")

medidas = []
for v, s, rot, src_, indep in MEDIDAS:
    v, s = float(v), float(s)
    medidas.append({
        "fonte": rot, "referencia": src_, "independente": indep == "True",
        "N_eff_obs": v, "sigma": s,
        "poder_DeltaNeff_sobre_sigma": dN / s,                 # o que decide o degrau 3 (Fase 6): < 5 => UNDERPOWERED
        "z_vs_TGL_NAO_CEGO": abs(N_pred - v) / s,            # ilustracao: ja legivel (o dado e publico)
        "z_vs_SM_NAO_CEGO": abs(N_SM - v) / s,
        "sigma_beta_implicado": s / dNdb,
        "estatuto": "[DECLARADO no frozen de 08/08/2026, com arXiv; a conferir na fonte antes de publicar]",
    })
best_indep = min((m_ for m_ in medidas if m_["independente"]), key=lambda t: t["sigma"])
# a conta da gerencia de 05/10: Planck 2018 +lensing+BAO
planck_lb = next((m_ for m_ in medidas if "lensing+BAO" in m_["fonte"]), None)

projecoes = []
for s, rot, src_, quando in PROJECOES:
    s = float(s)
    projecoes.append({"instrumento": rot, "referencia": src_, "quando": quando, "sigma_N_eff": s,
                      "poder_centro_padrao": dN / s,
                      "z_se_centro_ficar_em_best_indep": abs(N_pred - best_indep["N_eff_obs"]) / s,
                      "z_SM_se_centro_ficar_em_best_indep": abs(N_SM - best_indep["N_eff_obs"]) / s,
                      "sigma_beta_implicado": s / dNdb,
                      "cruza_5_sigma_centro_padrao": bool(dN / s >= 5.0),
                      "estatuto": "[DECLARADO no frozen; o proprio frozen marca «A CONFERIR» (RESULTADOS.md VIII)]"})
# linha conservadora adicional (memoria da gerencia, [DECLARADO, a conferir]): SO baseline 0,07 (Ade+2019, arXiv:1808.07445)
projecoes.append({"instrumento": "Simons Observatory baseline (valor alternativo lembrado pela lente)", "referencia": "arXiv:1808.07445",
                  "quando": "~2027", "sigma_N_eff": 0.07, "poder_centro_padrao": dN / 0.07,
                  "z_se_centro_ficar_em_best_indep": abs(N_pred - best_indep["N_eff_obs"]) / 0.07,
                  "z_SM_se_centro_ficar_em_best_indep": abs(N_SM - best_indep["N_eff_obs"]) / 0.07,
                  "sigma_beta_implicado": 0.07 / dNdb, "cruza_5_sigma_centro_padrao": False,
                  "estatuto": "[DECLARADO -- memoria da lente, NAO lido de arquivo em disco; a conferir]"})
sigma_5s_padrao = dN / 5.0
sigma_5s_centro_atual = abs(N_pred - best_indep["N_eff_obs"]) / 5.0

# ---------------------------------------------------------------- (4) o Nivel 2 (verossimilhanca completa, TGL-S dentro do CAMB)
n2 = json.load(open(NIVEL2, encoding="utf-8"))
fontes["13_nivel2_resultado.json"] = {"caminho": NIVEL2, "sha256": sha(NIVEL2), "bytes": os.path.getsize(NIVEL2)}
fontes["12_nivel2_frozen.json"] = {"caminho": NIVEL2_FROZEN, "sha256": sha(NIVEL2_FROZEN), "bytes": os.path.getsize(NIVEL2_FROZEN)}
n2S = n2["variantes"]["S"]
n2L = n2["variantes"]["L"]
nivel2 = {
    "frozen_hash": n2["frozen_hash"],
    "S": {"mediana": n2S["params"]["beta_TGL"]["mediana"], "sigma": n2S["params"]["beta_TGL"]["sigma_simetrico"],
          "poder_beta_sobre_sigma": beta / n2S["params"]["beta_TGL"]["sigma_simetrico"], "veredito": n2S["veredito"],
          "convergiu": n2S["convergiu"]},
    "L": {"mediana": n2L["params"]["beta_TGL"]["mediana"], "sigma": n2L["params"]["beta_TGL"]["sigma_simetrico"],
          "poder_beta_sobre_sigma": beta / n2L["params"]["beta_TGL"]["sigma_simetrico"], "veredito": n2L["veredito"],
          "convergiu": n2L["convergiu"]},
    "nota": "o Nivel 2 e a leitura do MAPA A no espectro completo (N_eff + omega_c juntos, TGL-S); o poder beta/sigma e a mesma ordem da leitura por N_eff publicado -- duas rotas, um numero (~0,7)",
}

# ---------------------------------------------------------------- (5) MAPA B: so-materia -- nada na era da radiacao
z_eq = 3400.0                                   # [KNOWN] Planck 2018 (z_eq ~ 3400)
T_bbn_MeV, T0_eV = 1.0, 2.3482e-4               # [KNOWN] T_CMB = 2,7255 K = 2,348e-4 eV
z_bbn = T_bbn_MeV * 1e6 / T0_eV
rho_m_over_r_bbn = (1.0 + z_eq) / (1.0 + z_bbn)
dH_over_H_mapB_bbn = 0.5 * beta * rho_m_over_r_bbn / (1.0 + rho_m_over_r_bbn)
mapaB = {"predicao_na_era_da_radiacao": "Delta N_eff = 0 (a radiacao nao e vestida); o unico efeito em T ~ MeV e beta*rho_m/rho_r",
         "rho_m_sobre_rho_r_em_T_1MeV": rho_m_over_r_bbn, "delta_H_sobre_H_em_T_1MeV": dH_over_H_mapB_bbn,
         "poder": dH_over_H_mapB_bbn / 0.01,    # contra qualquer sigma relativa de 1% -- ordem de grandeza
         "leitura": "o mapa so-materia NAO tem previsao no universo primordial: o seu teste vive na Fase 1 (z_eq, R, l_A); aqui e trivialmente UNDERPOWERED (poder ~ 1e-7), dito antes"}

# ---------------------------------------------------------------- (5) MAPA C: BBN speed-up -- duas parametrizacoes [KNOWN, a conferir]
# Steigman 2007 (Ann. Rev. Nucl. Part. Sci. 57, 463): y_D = 2,68 (eta_D)^-1,6, eta_D = eta10 - 6(S-1);  Y_p = 0,2485 + 0,0016[(eta10-6) + 100(S-1)]
eta10 = 6.10                                    # [KNOWN] eta10 ~ 6,1 (Planck omega_b)
dlnyD_dS_steigman = 1.6 * 6.0 / eta10           # ~1,57
dYp_dS_steigman = 0.16
# Cyburt, Fields, Olive, Yeh 2016 (RMP 88, 015004): D/H ~ (N_nu/3)^0,395 ; Y_p ~ (N_nu/3)^0,163
dlnDH_dNeff_cyburt = 0.395 / N_SM
dYp_dNeff_cyburt = 0.163 * 0.2470 / N_SM
# a parametrizacao da sessao de 08/08 (lida da lente irma registro_da_casa, NUMEROS_CONFERIDOS.json): d ln DH/d beta = 0,57*(4/3)/2 = 0,38
dlnDH_dbeta_sessao_08ago = 0.57 * (4.0 / 3.0) / 2.0
# observados [KNOWN -- digitados; nenhum arquivo em disco os contem (cooke_2018_DH.json AUSENTE no cache acom, dito pela lente irma)]
DH_obs, DH_err = 2.527e-5, 0.030e-5             # Cooke, Pettini, Steidel 2018 (ApJ 855, 102)
Yp_obs, Yp_err = 0.2453, 0.0034                 # Aver et al. 2021 (JCAP 03, 027)
sig_theo_DH_pct = 1.6                           # [KNOWN aprox.] taxas nucleares (d(p,gamma)3He): PRIMAT/Pitrou+2021 ~1-2 %  -- A CONFERIR
sig_omb_DH_pct = 1.6 * 0.67                     # omega_b do Planck a 0,67 % -> D/H ~ eta^-1,6
dS = S_bbn - 1.0
previsoes_C = {
    "S_bbn_H_sobre_H_SM": S_bbn, "S_menos_1": dS,
    "DH_dln_steigman": dlnyD_dS_steigman * dS,
    "DH_dln_cyburt_via_Neff": dlnDH_dNeff_cyburt * dN,
    "DH_dln_sessao_08ago": dlnDH_dbeta_sessao_08ago * beta,
    "Yp_delta_steigman": dYp_dS_steigman * dS,
    "Yp_delta_cyburt_via_Neff": dYp_dNeff_cyburt * dN,
}
sig_DH_obs_pct = 100.0 * DH_err / DH_obs
sig_DH_tot_pct = math.sqrt(sig_DH_obs_pct ** 2 + sig_theo_DH_pct ** 2 + sig_omb_DH_pct ** 2)
poder_C = {}
for k in ("DH_dln_steigman", "DH_dln_cyburt_via_Neff", "DH_dln_sessao_08ago"):
    poder_C[k] = {"so_obs": 100.0 * previsoes_C[k] / sig_DH_obs_pct,
                  "obs_teoria_omegab": 100.0 * previsoes_C[k] / sig_DH_tot_pct,
                  "sigma_beta_implicado_so_obs": (sig_DH_obs_pct / 100.0) / (previsoes_C[k] / beta),
                  "sigma_beta_implicado_tot": (sig_DH_tot_pct / 100.0) / (previsoes_C[k] / beta)}
for k in ("Yp_delta_steigman", "Yp_delta_cyburt_via_Neff"):
    poder_C[k] = {"so_obs": previsoes_C[k] / Yp_err, "sigma_beta_implicado_so_obs": Yp_err / (previsoes_C[k] / beta)}
bbn_decirc_casa = {"beta_hat": 0.012632, "sigma": 0.0318, "poder_beta_sobre_sigma": beta / 0.0318,
                   "fonte": "um.py prove_evidence_audit (values.bbn_decirc) -- VERIFICADO-NA-SESSAO de 08/08/2026; core.evidence_audit"}
mapaC = {"previsoes": previsoes_C, "sigmas_pct": {"DH_obs": sig_DH_obs_pct, "DH_teoria_declarada": sig_theo_DH_pct,
                                                   "DH_omega_b": sig_omb_DH_pct, "DH_total": sig_DH_tot_pct, "Yp_obs_abs": Yp_err},
         "poder": poder_C, "bbn_decircularizado_da_casa": bbn_decirc_casa,
         "discrepancia_dita": ("a sessao de 08/08 usou d ln(D/H)/d ln S ~ 0,57; Steigman 2007 da ~1,57 e Cyburt+2016 via N_eff da ~1,9; "
                               "a lente nao resolve sem codigo de BBN (AUSENTE em disco: find parthenope/primat/alterbbn = 0); "
                               "sob QUALQUER das tres o poder fica < 2 (UNDERPOWERED predeterminado) -- a discrepancia muda o numero, nao o degrau"),
         "codigo_de_bbn_em_disco": "AUSENTE (find /c/IALD -maxdepth 6 -iname '*parthenope*' -o '*primat*' -o '*alterbbn*' -o '*cooke*' -o '*bbn*': 0 ocorrencias)"}

# ---------------------------------------------------------------- resultado
res = {
    "identificador": "PODER_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO",
    "gerado_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "regua": "beta nunca literal (alpha por regex do um.py); medidas e projecoes lidas por regex do frozen 96b51333 (08/08/2026); sha256 calculados do artefato; NOT_FALSIFIED nunca e CONFIRMED; nada move o gate",
    "beta": {"alpha_regex": alpha, "beta_runtime": beta, "um_version": um_version},
    "lei_delta_K_beta_abs_1pw": lei,
    "mapa_A_Neff": {"F": F_NU, "N_SM": N_SM, "dNeff_dbeta": dNdb, "Delta_Neff": dN, "Delta_Neff_conta_gerencia_05out": dN_gerencia,
                    "identicos": abs(dN - dN_gerencia) < 1e-12, "N_eff_TGL": N_pred,
                    "Delta_omega_c_rho_mais_p": dOmc, "omega_m_planck_literal_do_um_py": omega_m_planck,
                    "frozen_hash_gravado_no_resultado": frozen_hash_gravado,
                    "medidas_publicadas": medidas, "melhor_independente": best_indep["fonte"],
                    "conta_da_gerencia_Planck_lensing_BAO": planck_lb,
                    "sigma_Neff_5sigma_centro_padrao": sigma_5s_padrao, "sigma_Neff_5sigma_centro_atual": sigma_5s_centro_atual,
                    "projecoes": projecoes, "nivel2_espectro_completo": nivel2,
                    "ressalva_TGL_S_vs_L": "a conversao em N_eff supoe TGL-S (free-streaming); se TGL-L, a resposta do CMB nao e LCDM+N_eff (frozen: ESTA E A MAIOR INCERTEZA DO RITO); o BBN (mapa C) nao depende disso (so ve H(T))"},
    "mapa_B_so_materia": mapaB,
    "mapa_C_BBN_speedup": mapaC,
    "degrau_predeterminado": {
        "A_Planck2018_lensing_BAO": "NOT_FALSIFIED_UNDERPOWERED (poder %.2f de 5) -- e NAO-CEGO" % (planck_lb["poder_DeltaNeff_sobre_sigma"] if planck_lb else float('nan')),
        "A_melhor_independente": "NOT_FALSIFIED_UNDERPOWERED (poder %.2f de 5) -- e NAO-CEGO" % best_indep["poder_DeltaNeff_sobre_sigma"],
        "A_CMB_S4_0p03_centro_padrao": "NOT_FALSIFIED_UNDERPOWERED (poder %.2f de 5); 5 sigma pede sigma(N_eff) <= %.4f" % (dN / 0.03, sigma_5s_padrao),
        "B": "NOT_FALSIFIED_UNDERPOWERED (poder ~ %.1e) -- sem previsao nesta era" % mapaB["poder"],
        "C_DH": "NOT_FALSIFIED_UNDERPOWERED (poder %.2f..%.2f de 5 conforme a parametrizacao) -- e NAO-CEGO" % (
            min(poder_C["DH_dln_sessao_08ago"]["obs_teoria_omegab"], poder_C["DH_dln_steigman"]["obs_teoria_omegab"], poder_C["DH_dln_cyburt_via_Neff"]["obs_teoria_omegab"]),
            max(poder_C["DH_dln_sessao_08ago"]["so_obs"], poder_C["DH_dln_steigman"]["so_obs"], poder_C["DH_dln_cyburt_via_Neff"]["so_obs"])),
        "C_Yp": "NOT_FALSIFIED_UNDERPOWERED (poder %.2f..%.2f de 5) -- e NAO-CEGO" % (poder_C["Yp_delta_steigman"]["so_obs"], poder_C["Yp_delta_cyburt_via_Neff"]["so_obs"]),
    },
    "fontes_lidas": fontes,
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- impressao
print("PODER FASE 8 -- beta =", beta, "(alpha regex", alpha, "; um.py", um_version, ")")
print("lei delta<K> = beta|1+w|: rad %.6f | mat %.6f | Lambda %.1f" % (lei["w_radiacao_1_3"], lei["w_materia_0"], lei["w_lambda_m1"]))
print("MAPA A: dN/dbeta = %.4f ; Delta N_eff = %+.5f ; N_eff_TGL = %.5f ; Delta omega_c = %s" % (dNdb, dN, N_pred, dOmc))
print(" %-40s %6s %6s %8s %8s %8s %10s" % ("fonte", "obs", "sigma", "poder", "z_TGL*", "z_SM*", "sig(beta)"))
for m_ in medidas:
    print(" %-40s %6.2f %6.2f %8.2f %8.2f %8.2f %10.5f %s" % (m_["fonte"][:40], m_["N_eff_obs"], m_["sigma"], m_["poder_DeltaNeff_sobre_sigma"],
                                                            m_["z_vs_TGL_NAO_CEGO"], m_["z_vs_SM_NAO_CEGO"], m_["sigma_beta_implicado"], "[indep]" if m_["independente"] else ""))
print(" (* z NAO-CEGO: ilustracao; o dado e publico)")
print(" 5 sigma pede sigma(N_eff) <= %.4f (centro padrao) | <= %.4f (centro atual %s)" % (sigma_5s_padrao, sigma_5s_centro_atual, best_indep["fonte"][:20]))
for p in projecoes:
    print(" proj %-52s sig %.3f  poder %.2f  z(centro atual) %.2f  %s" % (p["instrumento"][:52], p["sigma_N_eff"], p["poder_centro_padrao"], p["z_se_centro_ficar_em_best_indep"], p["quando"]))
print(" Nivel 2 (espectro completo, TGL-S): beta = %+.5f +- %.5f ; poder %.2f ; %s" % (nivel2["S"]["mediana"], nivel2["S"]["sigma"], nivel2["S"]["poder_beta_sobre_sigma"], nivel2["S"]["veredito"]))
print("MAPA B: rho_m/rho_r(T=1 MeV) = %.2e ; dH/H = %.2e ; poder ~ %.1e" % (rho_m_over_r_bbn, dH_over_H_mapB_bbn, mapaB["poder"]))
print("MAPA C: S = %.6f ; D/H: steigman %+.4f | cyburt %+.4f | sessao08ago %+.4f (d ln) ; Y_p: %+.5f | %+.5f" % (
    S_bbn, previsoes_C["DH_dln_steigman"], previsoes_C["DH_dln_cyburt_via_Neff"], previsoes_C["DH_dln_sessao_08ago"], previsoes_C["Yp_delta_steigman"], previsoes_C["Yp_delta_cyburt_via_Neff"]))
for k, v in poder_C.items():
    print("   poder %-26s so_obs %.2f %s" % (k, v["so_obs"], ("| obs+teoria+omega_b %.2f" % v["obs_teoria_omegab"]) if "obs_teoria_omegab" in v else ""))
print("   BBN descircularizado da casa: sigma(beta) = 0,0318 -> poder %.2f" % bbn_decirc_casa["poder_beta_sobre_sigma"])
print("DEGRAUS PREDETERMINADOS:")
for k, v in res["degrau_predeterminado"].items():
    print("  ", k, "->", v)
print("gravado:", OUT, "sha256", sha(OUT))
