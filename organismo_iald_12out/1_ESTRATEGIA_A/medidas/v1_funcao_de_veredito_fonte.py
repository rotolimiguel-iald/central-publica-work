def veredito_fase9_v1(r):
    """Funcao UNICA de veredito da Fase 9 (V1, 06/10/2026). Entrada: dict r produzido pelo runner sobre a familia P_primaria.
    Ordem (a primeira que casa decide):
    1 INCONCLUSIVE_SYSTEMATICS: alvo do composto sem fonte lida por hash (r["n_alvos_declarados"] > 0) OU dispersao interna
      chi2_int/(n-1) > 2 OU p_dispersao < 0,01 OU melhor ajuste beta-livre no limite do prior;
    2 FALSIFIED_AT_5SIGMA: |z_delta| >= 5, ou um leitor do composto com sigma_i <= 1,0 e |z_i| >= 5 — falsifica o PAR
      (lei D1b, convencao, conjunto), nao beta, nao a teoria;
    3 TENSION_3_TO_5_SIGMA: 3 <= |z_delta| < 5;
    4 NOT_FALSIFIED_UNDERPOWERED: poder previo < 5 (sufixo POWER_<x>_OF_5_SIGMA);
    5 NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_<n>SIGMA__ZERO_FREE_PARAMETERS: z_disc >= 5 E |z_delta| < 3 E
      lnB(TGL/LCDM) >= 5 E lnB(TGL/beta-livre) >= -1; n = floor(z_disc); __USE_NOVEL se a clausula de PARAMETROS vale
      (senao __USE_NOVELTY_PENDING); sufixos reportados __VS_LADDER_SYSTEMATIC_LNB_<x>, __VS_FREE_BACKGROUND_LNB_<x>;
      __NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC se lnB(TGL/shift-Cefeidas) < 0 com poder_nao_cefeida >= 5;
      __NOT_DISCRIMINATED_FROM_FREE_BACKGROUND se |lnB(TGL/fundo-livre)| < 1;
    6 NOT_FALSIFIED_POWERED (senao) com DEVIATION_CONSISTENT_WITHIN_1SIGMA ou DEVIATION_1_TO_3_SIGMA e, se z_disc < 5,
      __NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY.
    Sufixo sempre: __D1B__FUNDO_<id>__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED."""
    import math
    def f(x):
        return ("M" if x < 0 else "P") + ("%.1f" % abs(x)).replace(".", "P")
    base = "TGL_FASE9_RAZAO_DE_HUBBLE_V1__"
    suf = "__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED" % r["fundo"]
    zd = abs(r["z_delta"])
    if (r["n_alvos_declarados"] > 0 or (r["n_local"] > 1 and (r["dispersao_por_gl"] > 2.0 or r["p_dispersao"] < 0.01))
            or r["beta_livre_no_limite"]):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suf
    if zd >= 5 or any(s <= 1.0 and abs(z) >= 5 for (s, z) in r["sigma_z_por_alvo"]):
        return base + "FALSIFIED_AT_5SIGMA" + suf
    if zd >= 3:
        return base + "TENSION_3_TO_5_SIGMA" + suf
    if r["poder_previo"] < 5:
        return base + "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA" % f(r["poder_previo"]) + suf
    if r["z_disc"] >= 5 and zd < 3 and r["lnB_lcdm"] >= 5 and r["lnB_livre"] >= -1:
        t = base + "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA__ZERO_FREE_PARAMETERS" % int(math.floor(r["z_disc"]))
        t += "__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        t += "__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s" % (f(r["lnB_shift"]), f(r["lnB_fundo_livre"]))
        if r["lnB_shift"] < 0 and r["poder_nao_cefeida"] >= 5:
            t += "__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(r["lnB_fundo_livre"]) < 1:
            t += "__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return t + suf
    t = base + "NOT_FALSIFIED_POWERED__" + ("DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd < 1 else "DEVIATION_1_TO_3_SIGMA")
    if r["z_disc"] < 5:
        t += "__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    return t + suf
