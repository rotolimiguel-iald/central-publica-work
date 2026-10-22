"""JUIZ (12/10/2026) -- conferencia em runtime dos numeros que o programa cita. Nenhum dado aberto; nenhum veredito.
beta = ALPHA_FINE_CODATA_2018 (bytes do um.py, l.5557) * sqrt(e). Centros usados: SO o composto que o core v391 ja carrega
(hubble_ratio_opening_v388.numbers) e os sigmas publicos; tudo o mais e' hipotetico/condicional [DERIVED aqui]."""
import json, math, re, hashlib, pathlib, datetime
UM = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
CORE = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")
raw = UM.read_bytes()
m = re.search(rb"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", raw.split(b"\n")[5556])
ALPHA = float(m.group(1)); BETA = ALPHA * math.sqrt(math.e)
core = json.loads(CORE.read_bytes().decode("utf-8"))
num = core["core"]["hubble_ratio_opening_v388"]["numbers"]
b, sb = num["H0_bg"], 0.301           # BG1 (sigma transcrita do V1/Estrategias)
y, sy = num["media_GLS_locais"], num["sigma_GLS_locais"]
K_core = num["H0_local_previsto"] / b
lnK = math.log(K_core); lnE = lnK / (2 * BETA / 3)
def chi2_L(y, sy): return (y - b) ** 2 / (sy ** 2 + sb ** 2)
def chi2_T(y, sy): return (y - K_core * b) ** 2 / (sy ** 2 + (K_core * sb) ** 2)
def zdisc(y, sy):
    d = chi2_L(y, sy) - chi2_T(y, sy); return math.copysign(math.sqrt(abs(d)), d)
def zdelta(y, sy): return (y - K_core * b) / math.sqrt(sy ** 2 + (K_core * sb) ** 2)
def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi); fm = f(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return 0.5 * (lo + hi)
out = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "um_py_sha16": hashlib.sha256(raw).hexdigest()[:16],
       "beta_runtime": BETA, "K_core": K_core, "lnK": lnK, "lnE_zstar_implicito": lnE, "E_zstar_implicito": math.exp(lnE)}
out["reproducao_core"] = {"z_disc_sqrt_delta_chi2": zdisc(y, sy), "z_disc_core": num["z_disc"], "dif": zdisc(y, sy) - num["z_disc"],
                          "z_delta_grosseiro": zdelta(y, sy), "z_delta_core_logdet": num["z_delta"],
                          "poder_previo_se_centro_na_previsao": zdisc(K_core * b, sy)}
# limiares no centro do core
out["limiares_centro_core"] = {"sigma_local_max_para_5sigma": bisect(lambda s: zdisc(y, s) - 5.0, 0.2, 2.0),
                               "sigma_local_hoje": sy}
# centro minimo para 5 sigma com sigma de hoje e com os tetos das familias (A: 0,9494 P; 0,8635 R25)
out["centro_min_para_5sigma"] = {s_name: bisect(lambda h, s=s: zdisc(h, s) - 5.0, b, 80.0)
                                 for s_name, s in {"sigma_GLS_hoje_0p915": sy, "P_primaria_teto_0p9494": 0.9494, "R_r25_teto_0p8635": 0.8635, "P_primaria_piso_0p8035": 0.8035}.items()}
out["projecao_condicional_centro_persistindo"] = {s_name: {"z_disc": zdisc(y, s), "z_delta": zdelta(y, s)}
                                 for s_name, s in {"P_teto_0p9494": 0.9494, "P_piso_0p8035": 0.8035, "R25_teto_0p8635": 0.8635, "R25_piso_0p7494": 0.7494, "SH0ES_0p80_comb_0p756": 0.756}.items()}
# o PAR (Estrategia B): razao fixa, beta cancela
F = (7 / 8) * (4 / 11) ** (4 / 3); NSM = 3.044
dNeff = (4 / 3) * (1 + F * NSM) / F * BETA
R = dNeff / lnK; R_fechada = 2 * (1 + F * NSM) / (F * lnE)
out["par_B"] = {"F": F, "N_SM_KNOWN": NSM, "delta_Neff": dNeff, "Neff_TGL": NSM + dNeff, "R_dNeff_sobre_lnK": R, "R_forma_fechada": R_fechada,
                "S_BBN": math.sqrt(1 + 4 * BETA / 3)}
pH = out["reproducao_core"]["poder_previo_se_centro_na_previsao"]
out["par_B_poder_quadratura_se_independentes"] = {k: math.sqrt(pH ** 2 + (dNeff / s) ** 2) for k, s in
    {"SO_baseline_0p055": 0.055, "SO_goal_0p050": 0.050, "SO_ASO_0p045": 0.045, "sigma_0p024": 0.024}.items()}
out["par_B_perna_Neff_sozinha"] = {k: dNeff / s for k, s in {"hoje_0p12": 0.12, "SO_baseline_0p055": 0.055, "SO_goal_0p050": 0.050, "SO_ASO_0p045": 0.045}.items()}
out["par_B_sigma_Neff_para_5sigma"] = dNeff / 5
out["par_B_morte_condicional_perna_Neff"] = {"centro_2p82_SO_baseline": (NSM + dNeff - 2.82) / 0.055, "centro_2p96_SO_baseline": (NSM + dNeff - 2.96) / 0.055}
# m2
m2 = BETA * math.sin(math.pi / 4) * 1000.0   # meV, com sin45 [POSTULATE] e 1 eV [NORM] declarados
out["m2"] = {"m2_pred_meV": m2, "JUNO_59d_z": (8.660254037844387 - m2) / 0.0692820323027551,
             "sigma_beta_implicita_JUNO": 0.0692820323027551 / 1000 / math.sin(math.pi / 4), "beta_sobre_2": BETA / 2}
out["nota"] = ("z_disc do V1 = sqrt(chi2_LCDM - chi2_TGL) com o fundo perfilado em cada hipotese (reproduz o core a <1e-9); "
               "o par de B e' informativo: a quadratura supoe as duas pernas independentes e o fundo contado uma vez -- as duas pernas leem Planck, "
               "logo a quadratura e' um TETO [OPEN ate a covariancia u-v do fundo].")
json.dump(out, open(pathlib.Path(__file__).resolve().parent.parent / "medidas" / "numeros_juiz.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
