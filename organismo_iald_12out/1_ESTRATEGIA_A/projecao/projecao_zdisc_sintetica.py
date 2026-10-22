"""ESTRATEGIA A (12/10/2026) -- projecao SINTETICA e CONDICIONAL do z_disc da razao de Hubble (Fase 9).

O que este script FAZ:
  (1) le ALPHA_FINE_CODATA_2018 dos BYTES do um.py (l.5557) e calcula beta = alpha*sqrt(e) em runtime (nunca literal);
      recompoe K = E(z*)^(2 beta/3) com Omega_m/Omega_r da Bancada pinados no desenho da Fase 9 e confere contra o K do V1;
  (2) transcreve as sigmas PUBLICAS dos leitores e as amplitudes da caixa de covariancia da V2 R5.2 (so sigma), reproduz os
      extremos sigma_comb da caixa como CONFERENCIA (o mapa de rotas manda nao refazer o poder so-sigma: aqui ele e' conferido, nao refeito);
  (3) reproduz o z_disc = 4,2837 do core v391 a partir do centro composto e da sigma composta TRANSCRITOS (prova de que a
      estatistica do V1 e' o Delta chi2 entre LCDM e TGL com o fundo perfilado);
  (4) projeta z_disc, z_delta e os limiares para centros compostos HIPOTETICOS, por familia e por fundo; e familias hipoteticas
      (H0DN como compressao; sirenes futuras; termo SN L1-L2; sigmas menores de SH0ES/CCHP).
O que este script NAO faz: nao le centro de leitor algum; nao abre dado; nao emite veredito; nao executa a funcao congelada;
nao toca Bancada, Nos, kernel, mapa ou memoria. Toda saida e' [DERIVED, sintetico, condicional].
"""
import json, math, re, hashlib, pathlib, datetime, itertools

HERE = pathlib.Path(__file__).resolve().parent
UM = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
V1 = pathlib.Path(r"C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json")
V2 = pathlib.Path(r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json")
DESENHO = pathlib.Path(r"C:\IALD\Central de Patentes\work\scratch_6da8f00d\fase9_hubble\desenho\FASE9_DESENHO_RESULTADO.json")
CORE = pathlib.Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json")

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

# ---------------------------------------------------------------- (1) beta em runtime e K
raw = UM.read_bytes()
l5557 = raw.split(b"\n")[5556].decode("utf-8", "replace")
m = re.search(r"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)", l5557)
if not m:
    raise SystemExit("FAIL-CLOSED: alpha nao encontrado na l.5557 do um.py")
ALPHA = float(m.group(1)); BETA = ALPHA * math.sqrt(math.e)

des = json.loads(DESENHO.read_bytes().decode("utf-8"))
Om = des["sensibilidade"]["bancada"]["Omega_m"]; Or = des["sensibilidade"]["bancada"]["Omega_r"]
ZSTAR = des["z_star"]
E2 = Om * (1 + ZSTAR) ** 3 + Or * (1 + ZSTAR) ** 4 + (1.0 - Om - Or)
E_ZSTAR = math.sqrt(E2)
K = E_ZSTAR ** (2.0 * BETA / 3.0)
LN_E = math.log(E_ZSTAR)

v1 = json.loads(V1.read_bytes().decode("utf-8"))
K_V1 = v1["spec"]["lei"]["K_no_fundo_nu"]
E_DES = des["sensibilidade"]["bancada"]["E_zstar"]
chk_K = abs(K - K_V1); chk_E = abs(E_ZSTAR - E_DES)

# ---------------------------------------------------------------- (2) sigmas publicas e caixa de covariancia (so sigma)
v2 = json.loads(V2.read_bytes().decode("utf-8"))
L = v2["spec"]["leitores"]
SIG = {k: float(L[k]["sigma"]) for k in L}          # sigmas publicas transcritas da V2 R5.2 (E1)
AMP = v2["spec"]["covariancia"]["amplitudes_km_s_Mpc"] # L1N, L1bN, L2N, L2T, L3N, L3T, L4N
GRID = [round(0.05 * i, 2) for i in range(21)]

def gls(cov):
    """pesos GLS e sigma_comb para a media ponderada 1'C^-1 y / 1'C^-1 1 (inversao por eliminacao de Gauss, sem numpy)."""
    n = len(cov)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(cov)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[p] = A[p], A[c]
        if abs(A[c][c]) < 1e-15:
            return None, None, None
        f = A[c][c]; A[c] = [x / f for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0.0:
                g = A[r][c]; A[r] = [x - g * y for x, y in zip(A[r], A[c])]
    inv = [row[n:] for row in A]
    s = [sum(inv[i][j] for j in range(n)) for i in range(n)]
    tot = sum(s)
    if tot <= 0:
        return None, None, None
    w = [x / tot for x in s]
    return w, 1.0 / math.sqrt(tot), inv

def min_eig_ok(cov):
    """definida positiva por Cholesky (sem numpy)."""
    n = len(cov); Lc = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = cov[i][j] - sum(Lc[i][k] * Lc[j][k] for k in range(j))
            if i == j:
                if s <= 1e-12:
                    return False
                Lc[i][j] = math.sqrt(s)
            else:
                Lc[i][j] = s / Lc[j][j]
    return True

def cov_family(ids, lamN, lamT, extra=None):
    """caixa R5.2: um lambda_N comum (NGC4258) para L1N-L2N, L1N-L3N, L2N-L3N (+ L4N dos seis masers; L1bN no lugar de L1N na R_r25);
    lambda_T para o zero-point TRGB L2T-L3T. `extra` = termos adicionais (hipoteticos) {(i,j): valor}."""
    n = len(ids); C = [[0.0] * n for _ in range(n)]
    for i, a in enumerate(ids):
        C[i][i] = SIG[a] ** 2
    Nkey = {"L1_sh0es_r22": "L1N", "L1b_sh0es_r25": "L1bN", "L2_cchp": "L2N", "L3_sbf": "L3N", "L4_masers_6": "L4N"}
    Tkey = {"L2_cchp": "L2T", "L3_sbf": "L3T"}
    for i, a in enumerate(ids):
        for j, b in enumerate(ids):
            if i >= j:
                continue
            v = 0.0
            if a in Nkey and b in Nkey:
                v += lamN * AMP[Nkey[a]] * AMP[Nkey[b]]
            if a in Tkey and b in Tkey:
                v += lamT * AMP[Tkey[a]] * AMP[Tkey[b]]
            if extra and (a, b) in extra:
                v += extra[(a, b)]
            C[i][j] = C[j][i] = v
    return C

def endpoints(ids, extra=None):
    best = None
    for lamN in GRID:
        for lamT in GRID:
            C = cov_family(ids, lamN, lamT, extra)
            if not min_eig_ok(C):
                continue
            w, sc, _ = gls(C)
            if w is None:
                continue
            rec = {"lambda_N": lamN, "lambda_T": lamT, "sigma_comb": sc, "pesos": dict(zip(ids, w)),
                   "pesos_negativos": [k for k, x in zip(ids, w) if x < 0]}
            if best is None:
                best = {"min": rec, "max": rec}
            else:
                if sc < best["min"]["sigma_comb"] - 1e-12: best["min"] = rec
                if sc > best["max"]["sigma_comb"] + 1e-12: best["max"] = rec
    return best

FAM = {k: v["ids"] for k, v in v2["spec"]["familias"].items()}
PIN = {"P_primaria": v2["spec"]["covariancia"]["five_masers_decision"],
       "M_seis_masers_diagnostico": v2["spec"]["covariancia"]["six_masers_diagnostic"],
       "N_sem_cefeidas": v2["spec"]["covariancia"]["without_cepheids_diagnostic"],
       "R_r25": v2["spec"]["covariancia"]["pinned_family_endpoints_R4"]["R_r25"],
       "S_com_sirenes": v2["spec"]["covariancia"]["pinned_family_endpoints_R4"]["S_com_sirenes"]}
reproducao = {}
for fam, ids in FAM.items():
    ep = endpoints(ids)
    row = {"ids": ids, "min_sigma_comb": ep["min"]["sigma_comb"], "max_sigma_comb": ep["max"]["sigma_comb"],
           "min_at": (ep["min"]["lambda_N"], ep["min"]["lambda_T"]), "max_at": (ep["max"]["lambda_N"], ep["max"]["lambda_T"]),
           "pesos_negativos_no_max": ep["max"]["pesos_negativos"], "pesos_max": ep["max"]["pesos"]}
    if fam in PIN:
        pmin = PIN[fam]["minimum"]["sigma_comb"]; pmax = PIN[fam]["maximum"]["sigma_comb"]
        row["pinado_R5_2"] = {"min": pmin, "max": pmax, "diff_min": abs(pmin - row["min_sigma_comb"]), "diff_max": abs(pmax - row["max_sigma_comb"]),
                              "confere_1e-6": abs(pmin - row["min_sigma_comb"]) < 1e-6 and abs(pmax - row["max_sigma_comb"]) < 1e-6}
    reproducao[fam] = row

# ---------------------------------------------------------------- (3) a estatistica do V1 reproduzida do core (numeros TRANSCRITOS)
core = json.loads(CORE.read_bytes().decode("utf-8"))
def deep_find(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r = deep_find(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = deep_find(v, key)
            if r is not None: return r
    return None
ho = deep_find(core, "hubble_ratio_opening_v388")
NUM = ho["numbers"]
H_CORE = NUM["media_GLS_locais"]; S_CORE = NUM["sigma_GLS_locais"]; Z_DISC_CORE = NUM["z_disc"]; Z_DELTA_CORE = NUM["z_delta"]
BG = {k: (float(v1["spec"]["fundos"][k]["H0"]), float(v1["spec"]["fundos"][k]["sigma"]), v1["spec"]["fundos"][k]["papel"]) for k in ("BG1", "BG2", "BG3")}

def stats(h, sc, b, sb, Kf=K):
    """h = centro composto HIPOTETICO dos leitores locais; sc = sigma composta (so sigma); fundo b +- sb perfilado.
    z_disc = sinal*sqrt(chi2_LCDM - chi2_TGL) (definicao do V1); z_delta pelo perfil de beta livre (Laplace); poder so-sigma (formula do V1)."""
    chi_L = (h - b) ** 2 / (sc ** 2 + sb ** 2)
    chi_T = (h - Kf * b) ** 2 / (sc ** 2 + (Kf * sb) ** 2)
    d = chi_L - chi_T
    z_disc = math.copysign(math.sqrt(abs(d)), d)
    beta_hat = (3.0 / (2.0 * LN_E)) * math.log(h / b)
    sigma_beta = (3.0 / (2.0 * LN_E)) * math.sqrt((sc / h) ** 2 + (sb / b) ** 2)
    z_delta = (beta_hat - BETA) / sigma_beta
    poder = (Kf - 1.0) * b / math.sqrt(sc ** 2 + (Kf * sb) ** 2)
    lnB_lcdm = 0.5 * d                                   # modelos de mesma dimensao: Laplace
    occam = math.log(0.10 / (sigma_beta * math.sqrt(2 * math.pi)))  # prior U[-0,05; 0,05] do beta-livre
    lnB_livre = -0.5 * z_delta ** 2 + occam
    return {"z_disc": z_disc, "z_delta": z_delta, "beta_hat": beta_hat, "sigma_beta": sigma_beta, "poder_so_sigma": poder,
            "lnB_TGL_vs_LCDM_laplace": lnB_lcdm, "lnB_TGL_vs_beta_livre_laplace": lnB_livre}

rep_core = stats(H_CORE, S_CORE, BG["BG1"][0], BG["BG1"][1])
repro_core = {"entrada_transcrita_do_core": {"media_GLS_locais": H_CORE, "sigma_GLS_locais": S_CORE, "BG1": BG["BG1"][:2]},
              "z_disc_core": Z_DISC_CORE, "z_disc_reproduzido": rep_core["z_disc"], "diff_z_disc": abs(Z_DISC_CORE - rep_core["z_disc"]),
              "z_delta_core": Z_DELTA_CORE, "z_delta_reproduzido": rep_core["z_delta"], "diff_z_delta": abs(Z_DELTA_CORE - rep_core["z_delta"]),
              "beta_hat_core": NUM["beta_hat"], "beta_hat_reproduzido": rep_core["beta_hat"], "sigma_beta_core": NUM["sigma_beta"], "sigma_beta_reproduzido": rep_core["sigma_beta"],
              "poder_previo_V1": v1["spec"]["poder_previo"]["primario"], "poder_reproduzido": rep_core["poder_so_sigma"],
              "lnB_TGL_vs_LCDM_core": NUM["lnB"]["TGL_vs_LCDM"], "lnB_TGL_vs_LCDM_laplace": rep_core["lnB_TGL_vs_LCDM_laplace"],
              "lnB_TGL_vs_beta_livre_convergido_core": ho["recalculo_ao_lado"]["lnB_TGL_vs_beta_livre_convergido"], "lnB_TGL_vs_beta_livre_laplace": rep_core["lnB_TGL_vs_beta_livre_laplace"]}

# ---------------------------------------------------------------- (4) projecao sintetica por familia, fundo e centro hipotetico
def solve_center_for_zdisc(target, sc, b, sb):
    """menor centro h >= b tal que z_disc(h) >= target (bissecao; z_disc cresce com h acima de b)."""
    lo, hi = b, b + 12.0
    if stats(hi, sc, b, sb)["z_disc"] < target: return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if stats(mid, sc, b, sb)["z_disc"] >= target: hi = mid
        else: lo = mid
    return hi

def solve_sigma_for_zdisc(target, h, b, sb):
    """maior sigma_comb tal que z_disc(h, sc) >= target (bissecao; z_disc decresce com sc)."""
    lo, hi = 0.01, 5.0
    if stats(lo, sc=lo, b=b, sb=sb)["z_disc"] < target if False else stats(h, lo, b, sb)["z_disc"] < target: return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if stats(h, mid, b, sb)["z_disc"] >= target: lo = mid
        else: hi = mid
    return lo

def solve_sigma_for_zdelta(target_abs, h, b, sb):
    """maior sigma_comb tal que |z_delta| >= target_abs no centro h (onde TENSION/FALSIFIED precederiam a discriminacao)."""
    lo, hi = 0.01, 5.0
    if abs(stats(h, lo, b, sb)["z_delta"]) < target_abs: return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if abs(stats(h, mid, b, sb)["z_delta"]) >= target_abs: lo = mid
        else: hi = mid
    return lo

CENTROS = {  # centros compostos HIPOTETICOS (condicionais); nenhum e' leitura de dado nesta folha
    "TGL_exato (K.b)": None,                      # preenchido por fundo
    "74,00": 74.00, "73,50": 73.50, "73,20": 73.20,
    "centro_core_v391_se_persistir (72,882)": H_CORE,   # transcrito do core v391 (abertura de 06/10): condicional, nao e' abertura nova
    "72,50": 72.50, "72,00": 72.00,
    "LCDM_exato (b)": None,
}
FAM_SIGMA = {}
for fam, row in reproducao.items():
    FAM_SIGMA[fam] = {"max": row["max_sigma_comb"], "min": row["min_sigma_comb"]}
# familias HIPOTETICAS (sintese; nao pre-registradas): H0DN como compressao de L1+L2+L3+L4 (sigma 0,81, ORDEM 018 F0 [DECLARADO]) + L5; + L6
SIG["H0DN_compressao"] = 0.81
def sigma_comb_indep(sigs):
    return 1.0 / math.sqrt(sum(1.0 / s ** 2 for s in sigs))
FAM_SIGMA["H_h0dn_mais_tdcosmo (hipotetica)"] = {"max": sigma_comb_indep([0.81, SIG["L5_tdcosmo"]]), "min": sigma_comb_indep([0.81, SIG["L5_tdcosmo"]])}
FAM_SIGMA["H_h0dn_tdcosmo_sirenes (hipotetica)"] = {"max": sigma_comb_indep([0.81, SIG["L5_tdcosmo"], SIG["L6_sirenes"]]), "min": sigma_comb_indep([0.81, SIG["L5_tdcosmo"], SIG["L6_sirenes"]])}
# termo SN L1-L2 (fluxo Pantheon+ compartilhado; o V1 dizia off_diagonal_sigma_SN = 0,7; a R5.2 o deixa OPEN fora da caixa): sensibilidade no maximo
sn = float(v1["spec"]["covariancia"]["off_diagonal_sigma_SN"])
ep_sn = endpoints(FAM["P_primaria"], extra={("L1_sh0es_r22", "L2_cchp"): sn * sn})
FAM_SIGMA["P_primaria + termo SN L1-L2 (0,7x0,7) (sensibilidade)"] = {"max": ep_sn["max"]["sigma_comb"], "min": ep_sn["min"]["sigma_comb"]}
# sirenes futuras (hipoteticas): sigma_L6 de 11,25 (O4a) a 1,5
SIR = {}
for s6 in (11.25, 5.0, 3.0, 2.0, 1.5):
    SIG["L6_sirenes"] = s6
    ep = endpoints(FAM["S_com_sirenes"])
    SIR[str(s6)] = {"max": ep["max"]["sigma_comb"], "min": ep["min"]["sigma_comb"], "peso_L6_no_max": ep["max"]["pesos"]["L6_sirenes"]}
SIG["L6_sirenes"] = float(L["L6_sirenes"]["sigma"])
# SH0ES/CCHP mais precisos (hipoteticos), familia P no maximo da caixa
MELHOR = {}
for s1, s2 in ((1.04, SIG["L2_cchp"]), (0.93, SIG["L2_cchp"]), (0.80, SIG["L2_cchp"]), (0.70, SIG["L2_cchp"]), (1.04, 1.5), (1.04, 1.2), (0.80, 1.2), (0.70, 1.0)):
    old1, old2 = SIG["L1_sh0es_r22"], SIG["L2_cchp"]
    SIG["L1_sh0es_r22"], SIG["L2_cchp"] = s1, s2
    AMP_old = dict(AMP)
    # as amplitudes NGC4258/TRGB sao tetos ABSOLUTOS (km/s/Mpc) lidos da fonte; nao escalam com a sigma: mantidas, mas nao podem exceder a diagonal
    ep = endpoints(FAM["P_primaria"])
    MELHOR[f"sigma_L1={s1}, sigma_L2={s2}"] = {"max": ep["max"]["sigma_comb"], "min": ep["min"]["sigma_comb"], "nota": "amplitudes cruzadas mantidas nos tetos de fonte"}
    SIG["L1_sh0es_r22"], SIG["L2_cchp"] = old1, old2

PROJ = {}
for bg, (b, sb, papel) in BG.items():
    PROJ[bg] = {"fundo": {"H0": b, "sigma": sb, "papel": papel, "H0_local_previsto": K * b}, "familias": {}}
    for fam, sg in FAM_SIGMA.items():
        rows = {}
        for nome, h in CENTROS.items():
            hh = K * b if nome.startswith("TGL_exato") else (b if nome.startswith("LCDM_exato") else h)
            rows[nome] = {"centro": hh, "no_max_sigma": stats(hh, sg["max"], b, sb), "no_min_sigma": stats(hh, sg["min"], b, sb)}
        rows["limiares"] = {
            "centro_minimo_para_z_disc_5_no_max_sigma": solve_center_for_zdisc(5.0, sg["max"], b, sb),
            "centro_minimo_para_z_disc_5_no_min_sigma": solve_center_for_zdisc(5.0, sg["min"], b, sb),
            "sigma_comb_maxima_para_z_disc_5_no_centro_core_72p882": solve_sigma_for_zdisc(5.0, H_CORE, b, sb),
            "sigma_comb_abaixo_da_qual_TENSION_z_delta_3_no_centro_core_72p882": solve_sigma_for_zdelta(3.0, H_CORE, b, sb),
            "sigma_comb_abaixo_da_qual_FALSIFIED_z_delta_5_no_centro_core_72p882": solve_sigma_for_zdelta(5.0, H_CORE, b, sb),
        }
        PROJ[bg]["familias"][fam] = {"sigma_comb": sg, "cenarios": rows}

OUT = {
    "titulo": "ESTRATEGIA A -- projecao sintetica e condicional do z_disc da razao de Hubble (Fase 9), 12/10/2026",
    "estatuto": "[DERIVED, sintetico, condicional] nenhum centro de leitor lido; nenhum dado aberto; nenhum veredito; a funcao congelada nao foi executada; o gate nao se move",
    "gerado_em": datetime.datetime.now().isoformat(timespec="seconds"),
    "fontes_sha256": {"um_py": sha256(UM), "V1": sha256(V1), "V2_R5_2_E1": sha256(V2), "desenho_fase9": sha256(DESENHO), "core_v391": sha256(CORE)},
    "beta_runtime": {"alpha_l5557": m.group(1), "beta": BETA, "regra": "ALPHA_FINE_CODATA_2018 x sqrt(e) em runtime"},
    "K": {"Omega_m_bancada": Om, "Omega_r_bancada": Or, "z_star": ZSTAR, "E_zstar": E_ZSTAR, "E_zstar_desenho": E_DES, "diff_E": chk_E,
          "K_recomposto": K, "K_V1": K_V1, "diff_K": chk_K, "confere_1e-9": chk_K < 1e-9},
    "sigmas_publicas_transcritas_V2_R5_2": {k: float(L[k]["sigma"]) for k in L},
    "amplitudes_caixa_R5_2": AMP,
    "reproducao_extremos_caixa_R5_2_CONFERENCIA_nao_resultado_novo": reproducao,
    "reproducao_estatistica_do_core_v391": repro_core,
    "familias_hipoteticas_sigma_comb": {"H0DN_como_compressao": {k: v for k, v in FAM_SIGMA.items() if "hipotetica" in k},
                                        "termo_SN_L1_L2": FAM_SIGMA["P_primaria + termo SN L1-L2 (0,7x0,7) (sensibilidade)"],
                                        "sirenes_futuras_sigma_L6": SIR, "sh0es_cchp_mais_precisos": MELHOR},
    "projecao": PROJ,
}
(HERE / "PROJECAO_ZDISC_SINTETICA.json").write_text(json.dumps(OUT, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- tabelas em texto (para o relatorio)
def f2(x): return "n/a" if x is None else ("%.3f" % x)
lines = []
lines.append("beta_runtime = %.18f ; K = %.16f (V1: %.16f; diff %.1e) ; E(z*) = %.6f" % (BETA, K, K_V1, chk_K, E_ZSTAR))
lines.append("REPRODUCAO DO CORE v391 (entrada transcrita: h=%.6f, sigma_c=%.6f, BG1 %.3f+-%.3f): z_disc %.6f (core %.6f, diff %.1e); z_delta %.4f (core %.4f); poder %.3f (V1 5.913); lnB_LCDM Laplace %.3f (core %.3f); lnB_livre Laplace %.3f (core convergido %.3f)"
             % (H_CORE, S_CORE, BG["BG1"][0], BG["BG1"][1], rep_core["z_disc"], Z_DISC_CORE, repro_core["diff_z_disc"], rep_core["z_delta"], Z_DELTA_CORE, rep_core["poder_so_sigma"],
                rep_core["lnB_TGL_vs_LCDM_laplace"], NUM["lnB"]["TGL_vs_LCDM"], rep_core["lnB_TGL_vs_beta_livre_laplace"], ho["recalculo_ao_lado"]["lnB_TGL_vs_beta_livre_convergido"]))
lines.append("")
lines.append("EXTREMOS sigma_comb DA CAIXA R5.2 (conferencia contra o pinado):")
for fam, row in reproducao.items():
    pin = row.get("pinado_R5_2")
    lines.append("  %-28s min %.4f (lamN %.2f, lamT %.2f)  max %.4f (lamN %.2f, lamT %.2f)  pesos<0 no max: %s  %s" % (
        fam, row["min_sigma_comb"], *row["min_at"], row["max_sigma_comb"], *row["max_at"], row["pesos_negativos_no_max"] or "-",
        ("confere" if pin and pin["confere_1e-6"] else ("pinado %.4f/%.4f" % (pin["min"], pin["max"]) if pin else "(nao pinado na R5.2)"))))
lines.append("")
for bg in ("BG1", "BG2", "BG3"):
    P = PROJ[bg]; b, sb = P["fundo"]["H0"], P["fundo"]["sigma"]
    lines.append("=== FUNDO %s: %.3f +- %.3f (%s) ; H0_local previsto = K.b = %.4f ===" % (bg, b, sb, P["fundo"]["papel"][:40], K * b))
    lines.append("  %-52s %8s | %s" % ("familia (sigma_comb max / min)", "limiar h*", " | ".join("%-9s" % n[:9] for n in CENTROS)))
    for fam, F in P["familias"].items():
        sg = F["sigma_comb"]; lim = F["cenarios"]["limiares"]
        cells = []
        for nome in CENTROS:
            c = F["cenarios"][nome]
            cells.append("%5.2f/%5.2f" % (c["no_max_sigma"]["z_disc"], c["no_max_sigma"]["z_delta"]))
        lines.append("  %-52s %8s | %s" % ("%s (%.3f/%.3f)" % (fam[:34], sg["max"], sg["min"]), f2(lim["centro_minimo_para_z_disc_5_no_max_sigma"]), " | ".join(cells)))
    lim = P["familias"]["P_primaria"]["cenarios"]["limiares"]
    lines.append("  no centro do core (72,882): sigma_comb maxima para z_disc=5: %s ; TENSION (|z_delta|>=3) abaixo de sigma_comb %s ; FALSIFIED (>=5) abaixo de %s"
                 % (f2(lim["sigma_comb_maxima_para_z_disc_5_no_centro_core_72p882"]), f2(lim["sigma_comb_abaixo_da_qual_TENSION_z_delta_3_no_centro_core_72p882"]), f2(lim["sigma_comb_abaixo_da_qual_FALSIFIED_z_delta_5_no_centro_core_72p882"])))
    lines.append("")
lines.append("celulas: z_disc/z_delta no MAXIMO sigma_comb da familia (regra da ponta: discriminacao e poder no maximo). Centros compostos HIPOTETICOS.")
lines.append("")
lines.append("SIRENES FUTURAS (familia S, sigma_L6 hipotetica): " + "; ".join("sigma_L6=%s -> sigma_comb max %.4f (peso L6 %.3f)" % (k, v["max"], v["peso_L6_no_max"]) for k, v in SIR.items()))
lines.append("SH0ES/CCHP MAIS PRECISOS (familia P, hipotetico): " + "; ".join("%s -> max %.4f" % (k, v["max"]) for k, v in MELHOR.items()))
lines.append("TERMO SN L1-L2 (0,7x0,7) na caixa: P max %.4f -> %.4f" % (reproducao["P_primaria"]["max_sigma_comb"], FAM_SIGMA["P_primaria + termo SN L1-L2 (0,7x0,7) (sensibilidade)"]["max"]))
txt = "\n".join(lines)
(HERE / "PROJECAO_ZDISC_SINTETICA.txt").write_text(txt + "\n", encoding="utf-8")
print(txt)
