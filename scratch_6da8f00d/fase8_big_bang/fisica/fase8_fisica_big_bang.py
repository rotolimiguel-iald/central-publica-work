# -*- coding: utf-8 -*-
"""
fase8_fisica_big_bang.py -- LENTE "A FISICA" (05/10/2026): o efeito de beta_TGL no Big Bang
pela lei delta<K_d> = beta*|1+w|, por era e por MAPA da resposta modular (M1..M4).

Regua: beta NUNCA literal (lido do um.py por regex em runtime: ALPHA_FINE_CODATA_2018 * sqrt(e));
todo numero externo entra com estatuto [KNOWN] e fonte; nada e baixado; NOT_FALSIFIED != CONFIRMED.
Somente leitura fora desta pasta. Nao roda um.py nem ferramentas da casa.

Saidas (nesta pasta): fase8_fisica_resultado.json, fase8_fisica_tabela.md, e o sha256 de ambos no stdout.
"""
import os, re, io, json, math, hashlib, time

AQUI = os.path.dirname(os.path.abspath(__file__))
UM_PY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
CORE = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"

# ---------------------------------------------------------------- beta em runtime (regex no um.py; nunca literal)
def ler_beta_do_um_py(path):
    src = io.open(path, "r", encoding="utf-8", errors="replace").read()
    m = re.search(r"^ALPHA_FINE_CODATA_2018 = ([0-9.eE+-]+)", src, re.M)
    if not m:
        raise SystemExit("FAIL-CLOSED: ALPHA_FINE_CODATA_2018 nao encontrado no um.py")
    alpha = float(m.group(1))
    sha = hashlib.sha256(io.open(path, "rb").read()).hexdigest()
    return alpha, alpha * math.sqrt(math.e), sha, m.start()

ALPHA, BETA, UM_SHA, _pos = ler_beta_do_um_py(UM_PY)

# ---------------------------------------------------------------- o que o core v386 ja diz (lido por script)
core = json.load(io.open(CORE, "r", encoding="utf-8"))
c = core["core"]
casa = {
    "core_sha256": hashlib.sha256(io.open(CORE, "rb").read()).hexdigest(),
    "core_timestamp": core.get("timestamp"),
    "rho_plus_p_closure.values": c["rho_plus_p_closure"]["values"],
    "rho_plus_p_closure.verdict": c["rho_plus_p_closure"]["verdict"],
    "neff_channel.values.Delta_Neff": c["neff_channel"]["values"]["Delta_Neff"],
    "neff_channel.values.Neff_pred": c["neff_channel"]["values"]["Neff_pred"],
    "neff_channel.verdict": c["neff_channel"]["verdict"],
    "neff_channel.tensoes_literais_de_sessao": {"best": c["neff_channel"]["values"]["tensao_atual_best"],
                                               "act_bbn": c["neff_channel"]["values"]["tensao_atual_act_bbn"],
                                               "estatuto": "[INPUT/SESSAO] -- literais sem fonte datada (mapa cmb.neff_e_rho_mais_p)"},
    "evidence_audit.bbn_decirc": c["evidence_audit"]["values"]["bbn_decirc"],
    "final_verdict_machine.channels.bbn": c["final_verdict_machine"]["channels"]["bbn"],
    "planck_lcdm_input_v378": c["the_dissipation_law_with_contrast_v378"]["planck_lcdm_input"],
}

# ---------------------------------------------------------------- entradas externas [KNOWN], cada uma com fonte
KNOWN = {
    "N_eff_SM": {"valor": 3.044, "fonte": "padrao atual (Froustey+2020; Bennett+2021); o um.py usa N_SM = 3.044 (um.py:4792, :5560); o CAMB da casa usa 3.046 (v378 input)"},
    "Planck2018_Neff": {"valor": 2.99, "sigma": 0.17, "fonte": "Planck 2018 VI (Aghanim+2020, A&A 641, A6), TT,TE,EE+lowE+lensing+BAO: N_eff = 2.99 +- 0.17 (68%) [KNOWN; PDF nao em disco: a conferir na fonte]"},
    "CMB_S4_sigma_Neff": {"valor": 0.03, "fonte": "CMB-S4 Science Book / requisito sigma(N_eff) ~ 0.03 [KNOWN; o proprio um.py:4786 diz 'A CONFERIR nas fontes originais']"},
    "Yp_obs": {"valor": 0.2449, "sigma": 0.0040, "fonte": "Aver, Olive & Skillman 2015, JCAP 07, 011 [KNOWN; PDF nao em disco; buscar.py 'Aver.{0,12}2015' -> 0 ocorrencias relevantes]"},
    "DH_obs_1e5": {"valor": 2.527, "sigma": 0.030, "fonte": "Cooke, Pettini & Steidel 2018, ApJ 855, 102 [KNOWN; citado no artigo PT (um_absoluto_pt.txt:4240) e no prior omega_b do um.py:5565; o valor de D/H NAO esta no um.py]"},
    "BBN_exponents": {"Yp_Nnu": 0.163, "DH_Nnu": 0.395, "DH_eta": -1.60,
                      "fonte": "ajustes log-lineares de Cyburt, Fields, Olive & Yeh 2016 (Rev. Mod. Phys. 88, 015004), eq. (17)-(19): Yp ~ (N_nu/3)^0.163, D/H ~ (N_nu/3)^0.395 (eta10/6.10)^-1.60 [KNOWN; PDF nao em disco -- A LER DA FONTE antes de qualquer pre-registro]; cruzamento: dYp/dN_nu ~ 0.013 (regra classica)"},
    "Planck_omega_b": {"valor": 0.02237, "sigma": 0.00015, "fonte": "Planck 2018 VI base LCDM (TT,TE,EE+lowE+lensing) [KNOWN]; o um.py usa ombh2 = 0.02237 como fiducial (v378 input)"},
    "omega_m_h2": {"valor": 0.02237 + 0.1200, "fonte": "ombh2 + omch2 do fiducial da casa (v378 planck_lcdm_input: 0.02237 + 0.12); neutrino massivo (0.06 eV) nao somado aqui [simplificacao dita]"},
    "T_CMB_K": {"valor": 2.7255, "fonte": "Fixsen 2009 [KNOWN]; v378 input TCMB = 2.7255"},
    "z_star": {"valor": 1089.92, "fonte": "Planck 2018 VI, z_* = 1089.92 [KNOWN]"},
    "r_tensor_bound": {"valor": 0.036, "fonte": "BICEP/Keck 2021 (Ade+2021, PRL 127, 151301): r < 0.036 (95%) [KNOWN]; r = 16*epsilon em slow-roll [KNOWN]"},
    "m_e_MeV": {"valor": 0.5109989, "fonte": "CODATA [KNOWN]"},
}

# ---------------------------------------------------------------- 1. A LEI POR ERA [DERIVED da lei; a lei: kernel entropyFactor = 1 + beta|1+w| (ThermodynamicFriedmann.lean:21) = definicao/INPUT explicito; a casa a marca REAL na resposta modular (TheDammingByExpansion.lean:26)]
def delta(w):
    return BETA * abs(1.0 + w)

eps_max = KNOWN["r_tensor_bound"]["valor"] / 16.0            # slow-roll: r = 16 eps
w_infl_max = -1.0 + (2.0 / 3.0) * eps_max                     # 1 + w = (2/3) eps para o inflaton [KNOWN]
eras = [
    {"era": "atrator / de Sitter exato (fronteira silenciosa)", "w": -1.0, "delta": delta(-1.0), "nota": "zero exato: lambda_drops_out (RhoPlusPClosure.lean) -- o vacuo nao paga rho+p"},
    {"era": "inflacao slow-roll (cota r<0.036 => eps<%.5f)" % eps_max, "w": w_infl_max, "delta": delta(w_infl_max), "nota": "delta < beta*(2/3)*eps: a cobranca e quase silenciosa; degenerada com a normalizacao de H_infl"},
    {"era": "fim da inflacao (eps -> 1, w -> -1/3)", "w": -1.0 / 3.0, "delta": delta(-1.0 / 3.0), "nota": "2beta/3: a saida do atrator -- 'o primeiro excesso que ja nao pode retornar integralmente' [ONTO: leitura, sem termo]"},
    {"era": "reaquecimento / radiacao (BBN, CMB) w = 1/3", "w": 1.0 / 3.0, "delta": delta(1.0 / 3.0), "nota": "4beta/3: o MAXIMO entre as eras padrao -- o 'haja luz' e a era mais cobrada"},
    {"era": "materia w = 0", "w": 0.0, "delta": delta(0.0), "nota": "beta: o mapa (1+beta)Omega_m decidido em 30/09 e o hubble_form do kernel"},
    {"era": "Lambda hoje w = -1", "w": -1.0, "delta": delta(-1.0), "nota": "zero: Lambda = fronteira silenciosa"},
    {"era": "(fora do padrao) kination / stiff w = 1", "w": 1.0, "delta": delta(1.0), "nota": "2beta: so se houver tal era [OPEN]"},
]

# ---------------------------------------------------------------- 2. M1: fracao da densidade radiativa total -> Delta N_eff (duas EPOCAS)
F_nu = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)              # por especie, DEPOIS da aniquilacao e+e- (epoca do CMB)
N_SM = KNOWN["N_eff_SM"]["valor"]
d_rad = delta(1.0 / 3.0)                                      # = 4beta/3
# epoca do CMB (T << m_e): rho_r = rho_gamma (1 + F N_eff); uma especie extra pesa F/(1+F N_eff) do total
frac_por_especie_cmb = F_nu / (1.0 + F_nu * N_SM)
dNeff_cmb = d_rad / frac_por_especie_cmb                      # = (4/3)(1+F N_SM)/F * beta  (identico ao um.py:4793)
dNeff_dbeta_cmb = (4.0 / 3.0) * (1.0 + F_nu * N_SM) / F_nu
# epoca da BBN (T >~ m_e, antes da aniquilacao): g* = 2 + (7/8)(4 + 2 N_nu) = 10.75; uma especie extra pesa 1.75/10.75 = 7/43
g_star_bbn = 2.0 + (7.0 / 8.0) * (4.0 + 2.0 * 3.0)
frac_por_especie_bbn = ((7.0 / 8.0) * 2.0) / g_star_bbn       # = 7/43
dNnu_bbn = d_rad / frac_por_especie_bbn
assert abs(dNeff_dbeta_cmb - 9.9296) < 0.01, "o dial 9.9296 do um.py nao reproduziu"
assert abs(dNeff_cmb - casa["neff_channel.values.Delta_Neff"]) < 1e-9, "Delta N_eff do core nao reproduziu bit a bit"

Neff_pred_cmb = N_SM + dNeff_cmb
P = KNOWN["Planck2018_Neff"]
sep_TGL_SM_planck = dNeff_cmb / P["sigma"]                          # separacao TGL-SM na barra do Planck (o 0,70 da gerencia)
z_pred_vs_planck_centro = (Neff_pred_cmb - P["valor"]) / P["sigma"]  # a previsao contra o centro medido
z_SM_vs_planck_centro = (N_SM - P["valor"]) / P["sigma"]
s4 = KNOWN["CMB_S4_sigma_Neff"]["valor"]
sep_TGL_SM_s4 = dNeff_cmb / s4
sigma_5s = dNeff_cmb / 5.0
sigma_beta_de_sigma_Neff_planck = P["sigma"] / dNeff_dbeta_cmb     # o 'dial retroativo'
sigma_beta_de_sigma_Neff_s4 = s4 / dNeff_dbeta_cmb

# ---------------------------------------------------------------- 3. M2: so a materia veste (1+beta)Omega_m -> Omega_m(z) na recombinacao e na BBN
T0 = KNOWN["T_CMB_K"]["valor"]
omega_gamma = 2.4729e-5 * (T0 / 2.7255) ** 4                  # [KNOWN: Omega_gamma h^2 = 2.4729e-5 (T/2.7255)^4]
omega_r = omega_gamma * (1.0 + F_nu * N_SM)                   # fotons + neutrinos sem massa
omega_m = KNOWN["omega_m_h2"]["valor"]
z_eq = omega_m / omega_r - 1.0
def Omega_m_de_z(z):
    return 1.0 / (1.0 + (1.0 + z) / (1.0 + z_eq))
kB_eV_per_K = 8.617333262e-5
T0_eV = T0 * kB_eV_per_K
z_bbn_ini = 1.0e6 / T0_eV / (11.0 / 4.0) ** (1.0 / 3.0) - 1.0   # T = 1 MeV, antes da aniquilacao (T_gamma = T0 (1+z) / (11/4)^{1/3} naquela epoca)
z_bbn_fim = 7.0e4 / T0_eV - 1.0                                 # T ~ 0.07 MeV, gargalo do deuterio, apos a aniquilacao
zs = KNOWN["z_star"]["valor"]
m2 = {
    "z_eq": z_eq, "omega_r_h2": omega_r, "omega_m_h2": omega_m,
    "Omega_m(z*)": Omega_m_de_z(zs), "Omega_r(z*)": 1.0 - Omega_m_de_z(zs),
    "Omega_m(z_BBN_ini~T=1MeV)": Omega_m_de_z(z_bbn_ini), "Omega_m(z_BBN_fim~T=0.07MeV)": Omega_m_de_z(z_bbn_fim),
    "z_BBN_ini": z_bbn_ini, "z_BBN_fim": z_bbn_fim,
    # efeito em H: H^2 ~ (1+beta Omega_m) no mapa M2; dH/H = beta Omega_m / 2
    "dH/H @ z* (M2: so materia)": 0.5 * BETA * Omega_m_de_z(zs),
    "dH/H @ z* (M1: radiacao 4beta/3 + materia beta)": 0.5 * (d_rad * (1.0 - Omega_m_de_z(zs)) + BETA * Omega_m_de_z(zs)),
    "dH/H @ BBN_ini (M2)": 0.5 * BETA * Omega_m_de_z(z_bbn_ini),
    "dH/H @ BBN_fim (M2)": 0.5 * BETA * Omega_m_de_z(z_bbn_fim),
    "dH/H @ BBN (M1 = M3, constante)": math.sqrt(1.0 + d_rad) - 1.0,
    "Delta_omega_c_at_beta (um.py:4737, = beta*omega_m, omega_m=0.14301)": BETA * 0.14301,
}

# ---------------------------------------------------------------- 4. M3: speed-up S = H/H_LCDM = sqrt(1+4beta/3) na BBN -> Y_p e D/H
S = math.sqrt(1.0 + d_rad)
E = KNOWN["BBN_exponents"]
# ln-sensibilidades em S: S^2 = 1 + (7/43) dN_nu (antes da aniquilacao) => d ln S = (1/2)(7/43) dN_nu
dlnS_dNnu = 0.5 * frac_por_especie_bbn
dlnYp_dlnS = (E["Yp_Nnu"] / 3.0) / dlnS_dNnu
dlnDH_dlnS = (E["DH_Nnu"] / 3.0) / dlnS_dNnu
Yp0 = KNOWN["Yp_obs"]["valor"]; sYp = KNOWN["Yp_obs"]["sigma"]
DH0 = KNOWN["DH_obs_1e5"]["valor"]; sDH = KNOWN["DH_obs_1e5"]["sigma"]
dYp_S = Yp0 * dlnYp_dlnS * math.log(S)
dDH_S = DH0 * dlnDH_dlnS * math.log(S)
# via Delta N_nu (equivalente BBN) -- a mesma coisa por outra escada
dYp_N = Yp0 * E["Yp_Nnu"] * math.log(1.0 + dNnu_bbn / 3.0)
dDH_N = DH0 * E["DH_Nnu"] * math.log(1.0 + dNnu_bbn / 3.0)
# regra classica dYp/dN_nu ~ 0.013 (cruzamento)
dYp_classico = 0.013 * dNnu_bbn
# D/H tambem depende de omega_b: se omega_b vier do CMB com sigma 0.00015, a propagacao e:
dDH_omegab_1sigma = DH0 * abs(E["DH_eta"]) * (KNOWN["Planck_omega_b"]["sigma"] / KNOWN["Planck_omega_b"]["valor"])
m3 = {
    "S": S, "S_minus_1": S - 1.0,
    "dlnYp/dlnS": dlnYp_dlnS, "dlnDH/dlnS": dlnDH_dlnS,
    "Delta_Yp (via S)": dYp_S, "Delta_Yp (via Delta N_nu BBN)": dYp_N, "Delta_Yp (regra 0.013/N_nu)": dYp_classico,
    "z_Yp vs Aver+2015 (sigma 0.0040)": dYp_S / sYp,
    "Delta_DH_1e5 (via S)": dDH_S, "Delta_DH_1e5 (via Delta N_nu BBN)": dDH_N,
    "z_DH vs Cooke+2018 (sigma_obs 0.030, omega_b fixo)": dDH_S / sDH,
    "Delta_DH_1e5 por 1 sigma de omega_b(Planck)": dDH_omegab_1sigma,
    "z_DH com sigma_obs (+) sigma_omega_b em quadratura": dDH_S / math.sqrt(sDH ** 2 + dDH_omegab_1sigma ** 2),
    "sinal": "S > 1 => menos tempo => mais neutrons sobrevivem (Y_p sobe) e menos D queimado (D/H sobe): ambos POSITIVOS",
    "nota_teoria": "a incerteza TEORICA do D/H (taxas nucleares; Pitrou+2018 ~ +-0.036e-5; LUNA 2020 reduziu) NAO esta somada: [a ler da fonte]",
}
# sigma de S que a BBN hoje consegue: se sigma(N_nu,BBN) ~ 0.25-0.30 [ordem de grandeza da literatura, a ler da fonte], sigma(S-1) ~ dlnS_dNnu*sigma
m3["sigma(S-1) se sigma(N_nu,BBN)=0.25 [ordem de grandeza, a ler da fonte]"] = dlnS_dNnu * 0.25
m3["z_S vs BBN hoje (ordem de grandeza)"] = (S - 1.0) / (dlnS_dNnu * 0.25)

# ---------------------------------------------------------------- 5. poder: o que falsifica / o que e so correspondencia
poder = {
    "M1_CMB_hoje_Planck2018": {"sep_TGL_SM_sigma": sep_TGL_SM_planck, "z_pred_vs_centro": z_pred_vs_planck_centro, "z_SM_vs_centro": z_SM_vs_planck_centro,
                               "leitura": "nao discrimina (|z| < 2 para TGL e para o SM); correspondencia recuperada"},
    "M1_CMB_S4_centro_no_SM": {"sep_sigma": sep_TGL_SM_s4, "sigma_para_5sigma": sigma_5s, "leitura": "~4 sigma: TENSION possivel, nao FALSIFIED a 5 sigma com sigma=0.03; 5 sigma pede sigma<=%.4f" % sigma_5s},
    "M1_CMB_S4_centro_em_2.97 [literal de sessao do um.py:4801, SPT-3G CMB-SPA]": {"z": (Neff_pred_cmb - 2.97) / s4},
    "M3_BBN_hoje": {"z_Yp": dYp_S / sYp, "z_DH_omegab_fixo": dDH_S / sDH, "leitura": "0.3-1.1 sigma: nao discrimina; so correspondencia"},
    "M3_BBN_futuro_(sigma_Yp=0.001, sigma_DH_total=0.02e-5) [hipotetico]": {"z_Yp": dYp_S / 0.001, "z_DH": dDH_S / 0.02,
                                                                             "leitura": "ainda < 2 sigma: a BBN sozinha nao chega a 5 sigma para delta = 4beta/3"},
    "M2_BBN": {"dH/H": m2["dH/H @ BBN_ini (M2)"], "leitura": "efeito nulo (1e-8): correspondencia exata com LCDM na BBN; so o CMB (z*) ve 0.46% em H"},
    "o_que_FALSIFICA": {
        "M1/M3": "N_eff do CMB (CMB-S4, sigma<=0.024) centrado no SM com a TGL excluida a 5 sigma; OU N_eff medido ABAIXO do SM (o sinal da TGL e positivo, sem parametro livre); condicao previa: decidir TGL-S vs TGL-L (fechamento perturbativo = Lema 3 do lado do fluido, um.py:4819) ANTES de ler o CMB",
        "M2": "nenhum observavel primordial: M2 so cai se o CMB completo (nivel 2) excluir Delta omega_c = beta*omega_m e a TGL nao tiver outro lugar para por a materia",
        "M4 (kernel)": "nao e falsificavel por dado: e teorema sobre o fluxo (beta>0 => sem testemunha estatica); a natureza nao decide um teorema",
    },
}

# ---------------------------------------------------------------- 6. M4: a face de kernel (termos lidos por grep; ausencias ditas)
m4 = {
    "termos_existentes": [
        "the_zero_is_the_false_witness -- TGLExt/TheAxiomAndTheFalseWitness.lean:223 (sqrt 0 = 0 ∧ ¬FullStaticWitness ∧ zero absoluto inatingivel)",
        "beta_forbids_full_static_witness -- TGLExt/NoFullWitness.lean:91; full_closure_iff_flat -- :77 (e^{-t beta g} = 1 <=> t beta g = 0)",
        "absolute_zero_unreachable_in_finite_time -- TGLExt/ForbiddenBoundary.lean:150",
        "the_law_precedes_the_charge -- TGLExt/TheMatrixRule.lean:203 (beta so de alpha, fixada antes do registro)",
        "lambda_drops_out / closure_identity / hubble_form -- TGLExt/RhoPlusPClosure.lean (w=-1 nao paga; (1+4beta/3)rho_r + (1+beta)rho_m + rho_Lambda)",
        "entropyFactor c w = 1 + beta|1+w| -- TGLExt/ThermodynamicFriedmann.lean:21 (DEFINICAO: 'the modified differential entropy law is an explicit input')",
        "SectorFluid.correctedRho = (1 + beta(1+w_i)) rho_i -- TGLExt/SectorFluidClosure.lean (Ordem 012 B3: fechamento por setor = M1)",
    ],
    "ausencias_citadas": [
        "grep -rl -iE 'inflat|big ?bang|primordial|nucleos|BBN|N_eff|Neff' tgl_kernel/**/*.lean -> 6 arquivos, NENHUM com cosmologia do instante zero (RhoPlusPClosure: N_eff so em docstring; TheWeightIsNotTheRank/GravitonReading: 'primordial' = distincao primordial)",
        "grep -n -i 'big bang' um_absoluto_pt.txt -> 1 ocorrencia (linha 4307, a fronteira proibida 0 = q^2 + alpha^2), nenhuma cosmologia; 'inflacao' -> 0",
        "pip list | grep -iE 'parthenope|alterbbn|primat|bbn' -> 0 linhas: nenhum codigo de BBN em disco (AUSENTE; instalar e decisao do operador; nada foi baixado)",
    ],
    "leitura": "'beta e condicao de existencia' tem face de kernel como TEOREMA SOBRE O FLUXO (beta>0 ∧ g>0 => o Verbo nao fixa tudo; o zero nao se alcanca), nao como cosmologia de t=0; 'haja luz = t = 0' fica [ONTO] sem termo. Pela LEI, o que a casa tem e: o atrator (w=-1) e silencioso, a saida dele e a primeira cobranca, e a era da radiacao e a mais cobrada (4beta/3).",
}

# ---------------------------------------------------------------- saida
res = {
    "lente": "A FISICA -- fase8_big_bang (05/10/2026)",
    "beta_runtime": {"alpha_CODATA_2018_lido_por_regex": ALPHA, "beta_TGL": BETA, "um_py_sha256": UM_SHA, "formula": "ALPHA_FINE_CODATA_2018 * sqrt(e)"},
    "casa_lida_por_script": casa,
    "KNOWN": KNOWN,
    "1_lei_por_era": eras,
    "2_M1_fracao_da_radiacao_total": {
        "delta_radiacao_4beta_3": d_rad, "F_nu": F_nu, "N_SM": N_SM,
        "dNeff_dbeta (epoca CMB; um.py:4735 e :5561)": dNeff_dbeta_cmb,
        "Delta_Neff_equivalente_epoca_CMB (o 0,1195 da gerencia e do um.py)": dNeff_cmb,
        "Delta_Nnu_equivalente_epoca_BBN (g*=10.75; 7/43 por especie)": dNnu_bbn,
        "g_star_BBN": g_star_bbn, "fracao_por_especie_CMB": frac_por_especie_cmb, "fracao_por_especie_BBN": frac_por_especie_bbn,
        "N_eff_previsto_CMB": Neff_pred_cmb,
        "sigma_beta_que_o_Planck_da (dial retroativo)": sigma_beta_de_sigma_Neff_planck,
        "sigma_beta_que_o_S4_daria": sigma_beta_de_sigma_Neff_s4,
        "ACHADO": "a vestimenta 4beta/3 e uma FRACAO CONSTANTE da radiacao total; nao e exatamente um Delta N_eff: o equivalente muda de 0.0985 (antes da aniquilacao e+e-, BBN) para 0.1195 (depois, CMB). O canal N_eff do um.py usa so o numero do CMB.",
    },
    "3_M2_so_materia": m2,
    "4_M3_speed_up_BBN": m3,
    "5_poder_e_falsificacao": poder,
    "6_M4_face_de_kernel": m4,
    "gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
}

def _default(o):
    try:
        return float(o)
    except Exception:
        return str(o)

out_json = os.path.join(AQUI, "fase8_fisica_resultado.json")
tmp = out_json + ".tmp"
with io.open(tmp, "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1, default=_default)
os.replace(tmp, out_json)

# tabela
L = []
L.append("# Fase 8 -- a lente A FISICA: beta_TGL no Big Bang (numeros por script, %s)\n" % res["gerado_em"])
L.append("beta_TGL = alpha_CODATA2018 * sqrt(e) = %.15f (lido do um.py por regex; um.py sha256 %s)\n" % (BETA, UM_SHA[:16]))
L.append("## 1. A lei delta<K_d> = beta|1+w| por era [DERIVED da lei; a lei no kernel e DEFINICAO (entropyFactor), marcada pela casa REAL na resposta modular]\n")
L.append("| era | w | delta = beta|1+w| | nota |\n|---|---|---|---|")
for e in eras:
    L.append("| %s | %+.5f | %.6f | %s |" % (e["era"], e["w"], e["delta"], e["nota"]))
L.append("\n## 2. M1 -- fracao da radiacao total -> Delta N_eff (o que o um.py v154 ja faz: rho_plus_p_closure / neff_channel; kernel RhoPlusPClosure.hubble_form)\n")
L.append("| grandeza | valor | estatuto |\n|---|---|---|")
L.append("| delta na radiacao = 4beta/3 | %.6f | DERIVED |" % d_rad)
L.append("| dN_eff/dbeta (epoca CMB) | %.4f | REAL (reproduz um.py:4735 = 9.9296) |" % dNeff_dbeta_cmb)
L.append("| Delta N_eff equivalente, epoca CMB | %.5f | REAL (bit a bit = core.neff_channel.Delta_Neff) |" % dNeff_cmb)
L.append("| Delta N_nu equivalente, epoca BBN (g*=10.75) | %.5f | DERIVED (NOVO: nao esta no um.py) |" % dNnu_bbn)
L.append("| N_eff previsto (CMB) | %.4f | DERIVED |" % Neff_pred_cmb)
L.append("| separacao TGL-SM na barra do Planck 2018 (0.17) | %.2f sigma | KNOWN (Planck 2018 VI) -- o 0,70 da gerencia |" % sep_TGL_SM_planck)
L.append("| previsao contra o CENTRO do Planck (2.99) | %+.2f sigma | KNOWN -- o SM esta a %+.2f sigma do mesmo centro |" % (z_pred_vs_planck_centro, z_SM_vs_planck_centro))
L.append("| separacao TGL-SM no CMB-S4 (sigma 0.03) | %.2f sigma | KNOWN (sigma a conferir na fonte) |" % sep_TGL_SM_s4)
L.append("| sigma(N_eff) para 5 sigma | %.4f | DERIVED |" % sigma_5s)
L.append("| sigma(beta) que o Planck 2018 da pelo dial | %.5f (= %.1f beta) | DERIVED |" % (sigma_beta_de_sigma_Neff_planck, sigma_beta_de_sigma_Neff_planck / BETA))
L.append("| sigma(beta) que o S4 daria | %.5f (= %.2f beta) | DERIVED |" % (sigma_beta_de_sigma_Neff_s4, sigma_beta_de_sigma_Neff_s4 / BETA))
L.append("\n## 3. M2 -- so a materia veste ((1+beta)Omega_m, decisao de 30/09 sobre o mapa de R)\n")
L.append("| grandeza | valor |\n|---|---|")
for k, v in m2.items():
    L.append("| %s | %.6g |" % (k, v))
L.append("\n## 4. M3 -- speed-up S = sqrt(1+4beta/3) na BBN -> Y_p e D/H [expoentes KNOWN, a ler da fonte]\n")
L.append("| grandeza | valor |\n|---|---|")
for k, v in m3.items():
    L.append("| %s | %s |" % (k, ("%.6g" % v) if isinstance(v, float) else v))
L.append("\n## 5. Poder e falsificacao\n")
L.append("```\n" + json.dumps(poder, ensure_ascii=False, indent=1, default=_default) + "\n```")
L.append("\n## 6. M4 -- a face de kernel\n")
L.append("```\n" + json.dumps(m4, ensure_ascii=False, indent=1) + "\n```")
out_md = os.path.join(AQUI, "fase8_fisica_tabela.md")
tmp = out_md + ".tmp"
with io.open(tmp, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
os.replace(tmp, out_md)

for p in (out_json, out_md):
    print("%s  %s  %d bytes" % (hashlib.sha256(io.open(p, "rb").read()).hexdigest(), os.path.basename(p), os.path.getsize(p)))
print("beta_TGL = %.15f" % BETA)
print("delta(rad) = 4beta/3 = %.6f ; Delta N_eff(CMB) = %.5f ; Delta N_nu(BBN) = %.5f ; S-1 = %.6f" % (d_rad, dNeff_cmb, dNnu_bbn, S - 1))
print("Planck 2018: sep TGL-SM %.2f sigma ; pred vs centro %+.2f sigma ; SM vs centro %+.2f sigma" % (sep_TGL_SM_planck, z_pred_vs_planck_centro, z_SM_vs_planck_centro))
print("CMB-S4: %.2f sigma (sigma 0.03) ; 5 sigma pede sigma <= %.4f" % (sep_TGL_SM_s4, sigma_5s))
print("BBN: dYp = %.5f (%.2f sigma Aver+2015) ; dD/H = %.4fe-5 (%.2f sigma Cooke+2018, omega_b fixo; %.2f com omega_b em quadratura)" % (dYp_S, dYp_S / sYp, dDH_S, dDH_S / sDH, m3["z_DH com sigma_obs (+) sigma_omega_b em quadratura"]))
print("M2: Omega_m(z*) = %.4f -> dH/H = %.5f ; Omega_m(BBN) = %.2e -> dH/H = %.1e" % (m2["Omega_m(z*)"], m2["dH/H @ z* (M2: so materia)"], m2["Omega_m(z_BBN_ini~T=1MeV)"], m2["dH/H @ BBN_ini (M2)"]))
print("inflacao: eps < %.5f -> delta < %.2e" % (eps_max, eras[1]["delta"]))
