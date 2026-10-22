# ====================== v378: O QUE FALTOU -- o nucleo derivado D1b e a dupla contagem de beta; a lei da dissipacao com CONTRASTE; a Fase 4 (o desvio) ======================
# O operador (30/09/2026, noite, verbatim em _V378_OPERATOR_VERBATIM): «isso significa que estamos fazendo alguma coisa incompleta ainda [...] tem alguma coisa que
# deixamos passar, examine por favor»; e, a proposta da gerencia («a v378 generaliza a pedra da dissipacao ao contraste g = |1+w_eff(N)|, na mesma familia de
# vazamento e^{-t beta g} que o kernel ja tem, com g = 1 recuperando o D1a; e as Fases 2 e 4 se refazem pre-registradas na convencao do artigo, com o D1b como
# nucleo e o desvio delta como foco»): «concordo prossiga». O QUE FALTOU, medido: (1) o artigo 1 («Haja Luz», predict_H0_zero_free / D1_kernel_discrimination)
# tem DOIS nucleos para a lei de fluxo d ln H/dN = beta.W -- o D1a (W = 1, a pedra da v377) e o D1b, o DERIVADO da continuidade (W = |1+w_eff|) -- e a Bancada
# e a v377 so testaram o D1a; (2) o artigo transporta pela lei a calibracao LCDM de Planck (H0_CMB_LCDM), e as Fases 2-3 aplicaram a lei sobre o fundo TGL do
# mapa efetivo, que JA carrega beta (mapa R.sqrt(1+beta) + camada E1) -- os numeros diferem por convencao (-2,94 sigma vs -0,09 sigma na Fase 3); a leitura
# «dupla contagem de beta» e da gerencia sob a convencao do artigo 1 [DERIVED da convencao, nao medida; aferidor v378 B4]: o artigo 1 trata a camada E1 e a lei
# como hipoteses distintas e coexistentes, e qual fundo e o fundo segue decisao do operador [OPEN].
# Entram: (1) a pedra TGLExt.TheFlowLawContrast (a lei com contraste variavel: H0_local = H0_fundo.exp(beta int_0^N g); g = 1 devolve a pedra v377; a forma
# FECHADA do nucleo derivado pelo teorema fundamental do calculo: int g = (2/3)(ln E(N) - ln E(0)), logo K = (E(N)/E(0))^{2beta/3} -- na Bancada K_D1b =
# E(z*)^{2beta/3} = 1,083977 contra K_D1a = 1,087799; o DESVIO LE ABAIXO DA ASSINTOTA: int g <= N => beta.g_medio <= beta, sem parametro livre); (2) a
# reanalise NAO-CEGA da Fase 3 lida por hash (convencao do artigo + D1b: os seis leitores de sombra a -0,09 sigma da lei); (3) a Fase 4 pre-registrada (o
# desvio delta = beta_hat - beta_TGL na convencao do artigo, D1b): a escada (registro inteiro) e os cronometros (registros intermediarios, o teste que podia
# perder), lidos por hash com o veredito pre-registrado. Errata AO LADO (E12): os numeros das Fases 2-3 no modulo bancada_fases_v377 empilhavam beta; o modulo
# e o seu veredito ficam como estavam. O que NAO e: nada aqui confirma a TGL pela natureza (PROVADA != CONFIRMADA); o gate nao se move.

_V378_OPERATOR_VERBATIM = {
    "what_was_missed_20260930": ("isso significa que estamos fazendo alguma coisa incompleta ainda, eu escrevi muito sobre a tensão de hubble, especificamente no Custo "
                                 "Geométrico do Zero Absoluto: Haja Luz (tgl.paper_unified.py) e em outros ensaios anteriores, tem alguma coisa que deixamos passar, examine por favor"),
    "proceed_20260930": "concordo prossiga",
}
_DLC_FLAGS_V378 = (
    "ext_dlc_accumulatedContrast_kernel_checked", "ext_dlc_meanContrast_kernel_checked", "ext_dlc_survivingWeightContrast_kernel_checked",
    "ext_dlc_H0localContrast_kernel_checked", "ext_dlc_frwContrast_kernel_checked", "ext_dlc_survivingWeightContrast_pos_kernel_proved",
    "ext_dlc_survivingWeightContrast_eq_kernel_proved", "ext_dlc_the_flow_law_contrast_kernel_proved", "ext_dlc_accumulatedContrast_one_kernel_proved",
    "ext_dlc_contrast_one_recovers_D1a_kernel_proved", "ext_dlc_beta_zero_recovers_lcdm_contrast_kernel_proved", "ext_dlc_local_exceeds_background_contrast_kernel_proved",
    "ext_dlc_accumulatedContrast_ge_of_le_kernel_proved", "ext_dlc_accumulatedContrast_le_of_le_one_kernel_proved", "ext_dlc_the_deviation_reads_below_the_asymptote_kernel_proved",
    "ext_dlc_frw_accumulated_contrast_kernel_proved", "ext_dlc_the_derived_kernel_factor_kernel_proved", "ext_dlc_the_derived_kernel_factor_normalized_kernel_proved",
    "ext_dlc_the_dissipation_law_with_contrast_kernel_proved", "ext_dlc_the_dissipation_law_with_contrast_and_the_physical_arrow_kernel_proved")
_V378_STONES = ("TGLExt/TheFlowLawContrast.lean",)
_V378_BANCADA_FILES = {
    "fase4_pre": "PREREGISTRO_FASE4_DESVIO_20260930.json", "fase4_res": "RESULTADO_FASE4_DESVIO_20260930.json", "fase4_smoke": "SMOKE_FASE4.json",
    "fase3bis_rean": "REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json", "cc_moresco": "moresco_2022_cc.json",
}
# o fundo LCDM de Planck 2018 (VI, Tab. 2, TT,TE,EE+lowE+lensing) como [INPUT], o MESMO da reanalise e da Bancada; nunca literal de beta
_V378_PLANCK = {"H0": 67.36, "ombh2": 0.02237, "omch2": 0.1200, "mnu_eV": 0.06, "TCMB": 2.7255, "Neff": 3.046}
_V378_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")


def _v378_own_source_has(s):
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return s.encode("utf-8") in fh.read()
    except Exception:
        return False


def _v378_lcdm_E(z, H0, ombh2, omch2, mnu_eV, TCMB, Neff, og_coef=4.4814e-7):
    """v378: E(z) = H(z)/H0 do LCDM plano com radiacao (fotons + N_eff, como a Bancada: og = 4.4814e-7 T^4; nu massivo como materia, m/93.14)."""
    h2 = (H0 / 100.0) ** 2
    og = og_coef * TCMB ** 4
    Or = og * (1.0 + Neff * (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)) / h2
    Om = (ombh2 + omch2 + mnu_eV / 93.14) / h2
    OL = 1.0 - Om - Or
    z = np.asarray(z, float)
    return np.sqrt(Om * (1.0 + z) ** 3 + Or * (1.0 + z) ** 4 + OL), Om, Or, OL


def _v378_contrast_integral(zs, P, og_coef=4.4814e-7, n=200001):
    """v378: I_b = int_0^{N*} |1+w_eff| dN pelo trapezio (1+w_eff = (2/3) d ln E/dN, a equacao de Raychaudhuri em FRW plano) E pela forma fechada
    (2/3) ln E(z*) -- o numero corrige a frase dentro do rito. Devolve (I_trap, I_fechada, min(1+w), max(1+w))."""
    N = np.linspace(0.0, math.log1p(zs), n)
    E, _, _, _ = _v378_lcdm_E(np.expm1(N), P["H0"], P["ombh2"], P["omch2"], P["mnu_eV"], P["TCMB"], P["Neff"], og_coef)
    lnE = np.log(E)
    g = (2.0 / 3.0) * np.gradient(lnE, N)
    return float(np.trapezoid(np.abs(g), N)), float((2.0 / 3.0) * lnE[-1]), float(g.min()), float(g.max())


def _v378_num(x, nd=4):
    try:
        return round(float(x), nd)
    except Exception:
        return None


def _v378_tag(x):
    return ("%.2f" % float(x)).replace(".", "P").replace("-", "M")


def prove_the_dissipation_law_with_contrast_v378(ONE, core):
    """v378 -- A LEI DA DISSIPACAO COM CONTRASTE: o nucleo derivado D1b tipado [ADITIVO; nao move o gate]. O operador: «concordo prossiga». KERNEL
    (TGLExt.TheFlowLawContrast, sobre a pedra v377): o contraste ACUMULADO no registro, int_0^N g; o contraste MEDIO; o peso sobrevivente e o MESMO verbo de
    vazamento (leakVerb de NoFullWitness/v377) com o contraste medio: exp(-beta int g); a taxa local e a de fundo dividida pelo peso [DEFINICAO]; a lei
    the_flow_law_contrast: H0_local = H0_fundo.exp(beta int_0^N g); contrast_one_recovers_D1a: g = 1 devolve a pedra v377 (o D1a e o caso particular);
    beta = 0 devolve o LCDM; local > fundo se int g > 0; o contraste de FRW plano g = (2/3) d ln E/dN, a derivada ASSINADA [KNOWN: Raychaudhuri; a
    identificacao com |1+w_eff| do artigo 1 supoe rho+p >= 0, a NEC, DITA na prosa da pedra -- nao e binder de teorema (aferidor v378) -- e MEDIDA na
    grade]; frw_accumulated_contrast (a forma FECHADA pelo teorema fundamental do calculo:
    int g = (2/3)(ln E(N) - ln E(0))); the_derived_kernel_factor: K = (E(N)/E(0))^{2beta/3} -- o fator da lei e a potencia 2beta/3 da razao das taxas de
    expansao; the_deviation_reads_below_the_asymptote: int g <= N => beta.g_medio <= beta e K_D1b <= K_D1a (o desvio delta = beta(g_medio - 1) <= 0 e FIXADO
    pelo fundo, sem parametro livre); the_dissipation_law_with_contrast reune tudo com beta_forbids_full_static_witness; a seta fisica poe beta := alpha.sqrt(e).
    RUNTIME: I_b por trapezio = forma fechada; min(1+w) >= 0 na grade; I_b < N*; K_b < K_a; K_b = E(z*)^{2beta/3}; conferido com a Bancada (SMOKE, por hash).
    PROVADA != CONFIRMADA: o que a natureza decide (os leitores leem ou nao esse fator, por registro) segue com o observador."""
    fl = _v372_flags(core, _DLC_FLAGS_V378)
    src = _v372_embedded("TGLExt/TheFlowLawContrast.lean")
    src7 = _v372_embedded("TGLExt/TheFlowLawD1a.lean")
    beta = float(core.get("beta") or 0.0)
    zs = float(COMA_DEPH_INPUTS["Z_STAR"]); N = math.log(1.0 + zs)
    K_a = (1.0 + zs) ** beta
    I_trap, I_cl, gmin, gmax = _v378_contrast_integral(zs, _V378_PLANCK)
    K_b = math.exp(beta * I_cl)
    Ezs, Om, Or, OL = _v378_lcdm_E(zs, _V378_PLANCK["H0"], _V378_PLANCK["ombh2"], _V378_PLANCK["omch2"], _V378_PLANCK["mnu_eV"], _V378_PLANCK["TCMB"], _V378_PLANCK["Neff"])
    Ezs = float(Ezs)
    d7 = core.get("the_dissipation_law_v377") or {}
    K7 = d7.get("K_factor_runtime")
    smoke, sm_txt, sm_bytes = _read_external_json_with_hashes(os.path.join(CACHE, "bancada_30set", _V378_BANCADA_FILES["fase4_smoke"]))
    smoke = smoke or {}
    Kb_bancada = smoke.get("K_b"); Ib_bancada = smoke.get("I_b_fechada"); gmin_bancada = smoke.get("min_1_mais_w")
    pred = (core.get("coma_distance_dephasing") or {}).get("prediction") or {}
    _lit = '"flow_layer_kernel_v378": "CONTRAST_' + 'KERNEL_D1B_TYPED__TGLExt.TheFlowLawContrast.the_derived_kernel_factor'
    _ck = pred.get("flow_layer_kernel_v378")
    if _ck is not None:
        _beside_ok, _beside_ramo = ("TheFlowLawContrast" in str(_ck)), "core"
    else:
        _beside_ok, _beside_ramo = _v378_own_source_has(_lit), "fonte (modulo v39 nao re-executado nesta rodada)"
    num = [
        ("RUNTIME: beta = alpha.sqrt(e) do core (nunca literal) > 0; K_a = (1+z*)^beta recomputado (%.6f) = K da pedra v377 a 1e-12" % K_a,
         beta > 0 and K7 is not None and abs(float(K7) - K_a) < 1e-12),
        ("RUNTIME (o numero corrige a frase): I_b por trapezio de |1+w_eff| = (2/3) d ln E/dN (%.6f) = a forma FECHADA (2/3) ln E(z*) (%.6f) a 1e-6" % (I_trap, I_cl),
         abs(I_trap - I_cl) < 1e-6),
        ("RUNTIME: a NEC medida na grade LCDM de Planck [INPUT]: min(1+w_eff) = %.4f >= 0 (max %.4f; a radiacao passa de 1 perto de z*)" % (gmin, gmax), gmin >= 0.0),
        ("RUNTIME: I_b = %.4f < N* = %.4f nats: a hipotese de the_deviation_reads_below_the_asymptote esta SATISFEITA pelo fundo" % (I_cl, N), I_cl < N),
        ("RUNTIME: K_b = exp(beta.I_b) = %.6f < K_a = %.6f (K_b/K_a = %.6f): o nucleo derivado vaza MENOS que o scale-free" % (K_b, K_a, K_b / K_a), K_b < K_a),
        ("RUNTIME: K_b = E(z*)^{2beta/3} (the_derived_kernel_factor avaliado: E(z*) = %.3f) a 1e-12" % Ezs, abs(K_b - Ezs ** (2.0 * beta / 3.0)) < 1e-12),
        ("RUNTIME: K_b e I_b conferem com a Bancada (SMOKE_FASE4.json por hash, texto %s / bytes %s) a 1e-4 relativo" % (sm_txt, sm_bytes),
         Kb_bancada is not None and Ib_bancada is not None and abs(K_b / float(Kb_bancada) - 1.0) < 1e-4 and abs(I_cl / float(Ib_bancada) - 1.0) < 1e-4),
        ("RUNTIME: a NEC medida na Bancada (min(1+w) = %s) tambem >= 0" % gmin_bancada, gmin_bancada is not None and float(gmin_bancada) >= 0.0),
        ("RUNTIME: o custo efetivo por nat sob D1b, beta.I_b/N* = %.5f <= beta = %.5f (o desvio previsto delta/beta = %.4f <= 0)" % (beta * I_cl / N, beta, I_cl / N - 1.0), beta * I_cl / N <= beta),
    ]
    checks = [
        ("A PEDRA esta embutida, importa a pedra v377 (TheFlowLawD1a) e o teorema fundamental do calculo do Mathlib", bool(src) and "import TGLExt.TheFlowLawD1a" in src and "FundThmCalculus" in src),
        ("O CONTRASTE ACUMULADO tipado como integral no registro: def accumulatedContrast := ∫ s in (0 : ℝ)..N, g s", "def accumulatedContrast" in src and "∫ s in (0 : ℝ)..N, g s" in src),
        ("O MESMO VERBO DO VAZAMENTO com o contraste MEDIO: survivingWeightContrast := leakVerb β (meanContrast g N) N 1", "leakVerb β (meanContrast g N) N 1" in src),
        ("O CONTRASTE DE FRW PLANO: frwContrast E := deriv (fun s => (2 / 3 : ℝ) * Real.log (E s)) [KNOWN: Raychaudhuri]", "def frwContrast" in src and "deriv (fun s => (2 / 3 : ℝ) * Real.log (E s))" in src),
        ("A LEI COM CONTRASTE por termo: H0localContrast β Hcmb g N = Hcmb * Real.exp (β * accumulatedContrast g N)", "theorem the_flow_law_contrast" in src and "= Hcmb * Real.exp (β * accumulatedContrast g N)" in src),
        ("O D1a E O CASO PARTICULAR: contrast_one_recovers_D1a devolve survivingWeight β z da pedra v377", "theorem contrast_one_recovers_D1a" in src and "= survivingWeight β z" in src),
        ("A FORMA FECHADA pelo teorema fundamental do calculo: frw_accumulated_contrast usa integral_deriv_eq_sub", "theorem frw_accumulated_contrast" in src and "integral_deriv_eq_sub" in src),
        ("O FATOR DO NUCLEO DERIVADO: the_derived_kernel_factor da (E N / E 0) ^ ((2 / 3 : ℝ) * β); a versao normalizada E 0 = 1",
         "theorem the_derived_kernel_factor" in src and "(E N / E 0) ^ ((2 / 3 : ℝ) * β)" in src and "theorem the_derived_kernel_factor_normalized" in src),
        ("O DESVIO LE ABAIXO DA ASSINTOTA: the_deviation_reads_below_the_asymptote (β * meanContrast g N ≤ β)", "theorem the_deviation_reads_below_the_asymptote" in src and "β * meanContrast g N ≤ β" in src),
        ("beta = 0 devolve o LCDM; local > fundo; a condicao suficiente g <= 1 (accumulatedContrast_le_of_le_one)",
         all(t in src for t in ("theorem beta_zero_recovers_lcdm_contrast", "theorem local_exceeds_background_contrast", "theorem accumulatedContrast_le_of_le_one"))),
        ("TUDO NUM SO TERMO com a MESMA familia: the_dissipation_law_with_contrast usa beta_forbids_full_static_witness; a seta fisica usa couplingOfAlpha_beta",
         "theorem the_dissipation_law_with_contrast" in src and "beta_forbids_full_static_witness" in src and "theorem the_dissipation_law_with_contrast_and_the_physical_arrow" in src and "couplingOfAlpha_beta" in src),
        ("A NEC (ρ + p ≥ 0) esta DITA NA PROSA da pedra como a condicao da identificacao g = |1+w_eff| (aferidor v378: nao e binder de teorema; os teoremas valem para o contraste assinado; conferida na grade); a pedra DIZ: sem sorry, sem axiom; PROVADA != CONFIRMADA",
         "ρ + p ≥ 0" in src and "não binder" in src and "Sem sorry, sem axiom" in src and "PROVADA ≠ CONFIRMADA" in src),
        ("A pedra v377 (TheFlowLawD1a) segue embutida e intacta (the_dissipation_law presente): a v378 ACRESCENTA, nao substitui", bool(src7) and "theorem the_dissipation_law" in src7),
        ("A CHAVE AO LADO no modulo de Coma v39 (ramo %s): flow_layer_kernel_v378 aponta o termo; as chaves antigas ficam" % _beside_ramo,
         _beside_ok and str(pred.get("flow_layer_status", "")).startswith("CONJECTURE_DECLARED") and "TheFlowLawD1a" in str(pred.get("flow_layer_status_v377", ""))),
        ("O operador, verbatim: «tem alguma coisa que deixamos passar, examine por favor»; «concordo prossiga»", all(_V378_OPERATOR_VERBATIM.get(k) for k in ("what_was_missed_20260930", "proceed_20260930"))),
    ] + num
    checks += [("KERNEL " + k, v) for k, v in fl.items()]
    verdict, ok = _v372_verdict("TGL_THE_DISSIPATION_LAW_WITH_CONTRAST_V378", checks, fl, len(fl),
                                "__FLOW_LAW_WITH_CONTRAST_TYPED_H0LOCAL_EQ_H0FUNDO_TIMES_EXP_BETA_INT_G__CONTRAST_ONE_RECOVERS_D1A__FRW_CLOSED_FORM_INT_G_EQ_TWO_THIRDS_LN_E__"
                                "DERIVED_KERNEL_FACTOR_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__DEVIATION_READS_BELOW_THE_ASYMPTOTE_FIXED_BY_THE_BACKGROUND__NEC_STATED_IN_PROSE_FOR_THE_IDENTIFICATION_NOT_A_THEOREM_BINDER_MEASURED_ON_GRID__"
                                "SAME_LEAK_FAMILY_AS_V377_AND_NO_FULL_STATIC_WITNESS__PHYSICAL_ARROW_BETA_ALPHA_SQRT_E__WHAT_NATURE_DECIDES_STAYS_WITH_THE_OBSERVER__KERNEL_%d_OF_%d__GATE_UNTOUCHED")
    return {"operator_verbatim": dict(_V378_OPERATOR_VERBATIM), "checks": checks, "all_verified": ok, "verdict": verdict, "kernel_flags": fl,
            "beta_runtime": beta, "z_star_input": zs, "register_N_star_nats": N, "planck_lcdm_input": dict(_V378_PLANCK), "Omega_m": Om, "Omega_r": Or, "Omega_L": OL,
            "E_z_star": Ezs, "I_b_trapezoid": I_trap, "I_b_closed_form": I_cl, "min_1_plus_w_eff_grid": gmin, "max_1_plus_w_eff_grid": gmax,
            "K_D1a_runtime": K_a, "K_D1b_runtime": K_b, "K_b_over_K_a": K_b / K_a, "H0_local_D1a_from_planck": _V378_PLANCK["H0"] * K_a, "H0_local_D1b_from_planck": _V378_PLANCK["H0"] * K_b,
            "per_nat_cost_D1b": beta * I_cl / N, "predicted_deviation_over_beta_D1b": I_cl / N - 1.0,
            "bancada_smoke_beside": {"K_b": Kb_bancada, "I_b_fechada": Ib_bancada, "min_1_mais_w": gmin_bancada, "sha16_text": sm_txt, "sha16_bytes": sm_bytes},
            "coma_v39_flow_layer_kernel_v378_beside": pred.get("flow_layer_kernel_v378"), "beside_ramo": _beside_ramo,
            "statute": ("PROVADA como implicacao (kernel), SEM axioma novo: a familia e a da v377/NoFullWitness com o contraste MEDIO; as identificacoes entram como DEFINICOES nomeadas "
                        "(o contraste acumulado; o contraste de FRW plano, a derivada assinada [KNOWN: Raychaudhuri]); a NEC e a condicao DITA na prosa para ler g como |1+w_eff| "
                        "(nao e binder de teorema; medida na grade); o fundo LCDM e o de Planck 2018 da Bancada [INPUT], nao os literais do artigo 1 (I_b difere em ~1e-4 relativo, "
                        "imaterial nos vereditos); o teorema e a implicacao a jusante: K = E(z*)^{2beta/3} e o desvio le abaixo da assintota, fixado pelo fundo; a natureza decide a "
                        "incidencia: PROVADA != CONFIRMADA"),
            "does_not_gate_core": True}


def prove_what_was_missed_v378(ONE, core):
    """v378 -- O QUE FALTOU [ADITIVO; nao move o gate; leitura (E12) AO LADO]. O operador (30/09, noite): «tem alguma coisa que deixamos passar, examine por favor».
    Achados: (1) [REAL] o nucleo DERIVADO D1b do artigo 1 (W = |1+w_eff|) nunca fora testado NA BANCADA nem tipado (so o D1a, W = 1); o artigo 1 o computa
    (predict_H0_zero_free: 0,034 sigma vs SH0ES); (2) [REAL] o modo tgl da Bancada tem beta no fundo (mapa R.sqrt(1+beta) + camada E1) e as Fases 2-3 aplicaram
    a lei sobre esse fundo; na CONVENCAO do artigo 1 (a lei transporta a calibracao LCDM de Planck; beta so na lei) os numeros diferem por convencao (-2,94 vs
    -0,09 sigma). A LEITURA «dupla contagem de beta» e da gerencia sob a convencao do artigo 1 [DERIVED da convencao, nao medida]: o artigo 1 trata a camada
    E1 e a lei de fluxo como hipoteses DISTINTAS e coexistentes (tgl_paper_unified.py: «the flow equation is NOT redundant -- it is a SEPARATE physical
    hypothesis»), e o mapa efetivo foi ratificado pelo operador; o operador acolheu a proposta de trabalhar na convencao do artigo («concordo prossiga»), mas
    qual fundo e o fundo segue decisao dele [OPEN] (aferidor v378, B4). A reanalise NAO-CEGA da Fase 3 (declarada como tal, lida por hash): na convencao do
    artigo com D1b os seis leitores de sombra ficam a -0,09 sigma da lei; com o fundo empilhado -2,60. LEITURA (E12) AO LADO, nao errata: os numeros das Fases
    2-3 do modulo bancada_fases_v377 (pull +1,95; z -2,94) sao os do fundo efetivo + lei -- o modulo e o seu veredito ficam como estavam (pinados); a leitura
    muda, o numero nao. [OPEN]: a forma da camada E1 (Bancada «fator sobre o TOTAL» vs artigo sqrt(1+beta|1+w|)) foi medida em 30/09 e registrada na memoria,
    nao lida por hash aqui. NOT_FALSIFIED nao e CONFIRMADA."""
    rean, r_txt, r_bytes = _read_external_json_with_hashes(os.path.join(CACHE, "bancada_30set", _V378_BANCADA_FILES["fase3bis_rean"]))
    rean = rean or {}
    beta = float(core.get("beta") or 0.0)
    zs = float(rean.get("z_star") or COMA_DEPH_INPUTS["Z_STAR"])
    # a reanalise usou omega_gamma h^2 = 2.469e-5 (T = 2.7255): og_coef = 2.469e-5 / 2.7255^4
    I_trap, I_cl, gmin, gmax = _v378_contrast_integral(zs, _V378_PLANCK, og_coef=2.469e-5 / 2.7255 ** 4)
    fam = rean.get("familias") or {}
    F = lambda k: (fam.get(k) or {})
    seis_b = F("Fc_planck2018_lcdm__D1b__seis"); novos_b = F("Fc_planck2018_lcdm__D1b__novos"); emp_b = F("Fa_tgl_eff_planck_dr2__D1b__seis"); seis_a = F("Fc_planck2018_lcdm__D1a__seis"); emp_a = F("Fa_tgl_eff_planck_dr2__D1a__seis")
    b7 = core.get("bancada_fases_v377") or {}
    v7 = str(b7.get("verdict") or "")
    vr = str(rean.get("veredito") or "")
    checks = [
        ("A reanalise da Fase 3 LIDA POR HASH do cache do rito (texto %s / bytes %s)" % (r_txt, r_bytes), bool(rean)),
        ("A reanalise DECLARA-SE NAO-CEGA (cega = False) e o seu veredito termina em NOT_A_CONFIRMATION sem palavra proibida",
         rean.get("cega") is False and vr.endswith("__NOT_A_CONFIRMATION") and "REANALYSIS_NOT_BLIND" in vr and not _V378_GUARDA.search(vr)),
        ("beta da reanalise = alpha.sqrt(e) do core a 1e-9 relativo; z* = %.2f" % zs, beta > 0 and rean.get("beta") is not None and abs(float(rean["beta"]) / beta - 1.0) < 1e-9),
        ("O nucleo derivado recomputado aqui: I_b = %.5f (forma fechada) = o I da reanalise (%s) a 1e-5 relativo; K_D1b = %.6f e K_D1a = %.6f conferem a 1e-6"
         % (I_cl, rean.get("I_kernel_D1b"), rean.get("K_D1b") or 0.0, rean.get("K_D1a") or 0.0),
         rean.get("I_kernel_D1b") is not None and abs(I_cl / float(rean["I_kernel_D1b"]) - 1.0) < 1e-5
         and abs(math.exp(beta * I_cl) - float(rean.get("K_D1b") or 0.0)) < 1e-6 and abs((1.0 + zs) ** beta - float(rean.get("K_D1a") or 0.0)) < 1e-6),
        ("Convencao do artigo (fundo Planck 2018 LCDM) + D1b: os SEIS leitores de sombra e os CINCO novos presentes, com z", seis_b.get("z_comb") is not None and novos_b.get("z_comb") is not None),
        ("O controle EMPILHADO (fundo efetivo das Fases 2-3) presente com D1b e D1a: a dupla contagem medida ao lado", emp_b.get("z_comb") is not None and emp_a.get("z_comb") is not None),
        ("O modulo bancada_fases_v377 segue no core com o seu veredito PINADO (a leitura E12 e AO LADO; os numeros da v377 nao mudam)", bool(v7) and b7.get("all_verified") is True),
        ("O operador, verbatim: «tem alguma coisa que deixamos passar, examine por favor»", bool(_V378_OPERATOR_VERBATIM.get("what_was_missed_20260930"))),
    ]
    ok = all(v for _, v in checks)
    if ok:
        verdict = ("TGL_WHAT_WAS_MISSED_V378__DERIVED_KERNEL_D1B_NEVER_TESTED_ON_THE_BENCH_BEFORE_NOW_TYPED__ARTICLE_CONVENTION_LAW_TRANSPORTS_THE_LCDM_CALIBRATION__"
                   "STACKING_THE_LAW_ON_THE_EFFECTIVE_BACKGROUND_READ_AS_COUNTING_BETA_TWICE_UNDER_THE_ARTICLE_CONVENTION_DERIVED_NOT_MEASURED_READING_E12_BESIDE__"
                   "FASE3_REANALYSIS_NOT_BLIND_SHADOW_READERS_Z_%s_WITH_D1B_ON_PLANCK_LCDM_NEW_READERS_Z_%s__"
                   "STACKED_CONTROL_Z_%s__E1_LAYER_FORM_OPEN__WHICH_BACKGROUND_IS_THE_BACKGROUND_IS_THE_OPERATORS_DECISION__READ_BY_HASH__NOT_A_CONFIRMATION"
                   % (_v378_tag(seis_b["z_comb"]), _v378_tag(novos_b["z_comb"]), _v378_tag(emp_b["z_comb"])))
    else:
        verdict = "TGL_WHAT_WAS_MISSED_V378__NOT_READ_THIS_RUN__%s__GATE_UNTOUCHED" % ("ARTIFACT_ABSENT" if not rean else "CHECKS_FAILED")
    return {"operator_verbatim": {"what_was_missed_20260930": _V378_OPERATOR_VERBATIM["what_was_missed_20260930"]}, "checks": checks, "all_verified": ok, "verdict": verdict,
            "reanalysis_hashes": {"file": _V378_BANCADA_FILES["fase3bis_rean"], "sha16_text": r_txt, "sha16_bytes": r_bytes}, "reanalysis_verdict": vr, "reanalysis_declared_blind": rean.get("cega"),
            "I_b_reanalysis": rean.get("I_kernel_D1b"), "I_b_recomputed": I_cl, "K_D1a": rean.get("K_D1a"), "K_D1b": rean.get("K_D1b"),
            "shadow_readers_planck_lcdm_D1b": {k: _v378_num(seis_b.get(k)) for k in ("H0_predito", "H0_sombra", "z_comb", "custo_por_nat_medido", "custo_por_nat_sigma")},
            "new_readers_planck_lcdm_D1b": {k: _v378_num(novos_b.get(k)) for k in ("H0_predito", "H0_sombra", "z_comb")},
            "shadow_readers_planck_lcdm_D1a_z": _v378_num(seis_a.get("z_comb")), "stacked_control_D1b_z": _v378_num(emp_b.get("z_comb")), "stacked_control_D1a_z": _v378_num(emp_a.get("z_comb")),
            "reading_E12_beside": ("os numeros das Fases 2-3 no modulo bancada_fases_v377 (pull da escada +1,95 sigma; leitores -2,94 sigma contra a lei) aplicaram a lei sobre o fundo TGL efetivo, "
                                   "que ja carrega beta pelo mapa R.sqrt(1+beta) e pela camada E1. LEITURA da gerencia sob a convencao do artigo 1 [DERIVED da convencao, nao medida]: dupla contagem. "
                                   "Na convencao do artigo 1 (a lei transporta a calibracao LCDM de Planck) e com o nucleo derivado D1b, os leitores de sombra ficam a -0,09 sigma da lei. "
                                   "O artigo 1 trata a camada E1 e a lei como hipoteses distintas e coexistentes; o mapa efetivo foi ratificado pelo operador; qual fundo e o fundo segue [OPEN]. "
                                   "O modulo e o seu veredito ficam como estavam; a leitura muda, o numero nao."),
            "bancada_fases_v377_verdict_pinned": v7,
            "open_items": ["a forma da camada E1 (Bancada «fator sobre o TOTAL», decisao de 15/09, vs artigo sqrt(1+beta|1+w|)): medida em 30/09 e registrada na memoria; nao lida por hash aqui",
                           "qual fundo e o fundo sobre o qual a lei incide (Planck LCDM como no artigo -- a convencao de TRABALHO acolhida em 30/09 -- ou o efetivo com o angulo dentro): decisao do operador (a pergunta do angulo)",
                           "se a leitura «dupla contagem» e fato ou convencao depende da decisao anterior: fica [DERIVED da convencao do artigo]"],
            "does_not_gate_core": True, "statute": "[REAL -- reanalise NAO-CEGA, lida por hash; o D1b nao testado NA BANCADA]; a dupla contagem e leitura [DERIVED da convencao]; (E12) leitura AO LADO; [OPEN] as decisoes do operador; NOT_FALSIFIED nao e CONFIRMADA"}


def prove_bancada_fase4_v378(ONE, core):
    """v378 -- A FASE 4 DA BANCADA UM (30/09/2026, noite): O DESVIO, na convencao do artigo, com o nucleo derivado -- LIDA POR HASH [ADITIVO; nao move o gate].
    Pre-registrada (hash conferido pelo runner antes de abrir numero): theta = (H0, w_b, w_c, beta) com o fundo LCDM (Planck comprimido Chen+2019 + BAO) medindo
    H0, w_b, w_c e a lei ligando beta SO na lei (beta_no_fundo = 'nao'); D1b primario (K = E_LCDM(z*)^{2beta/3}), D1a secundario; o estimando e o DESVIO delta =
    beta_hat - beta_TGL (sigma por J^T J), com beta_TGL como assintota e a funcao de aproximacao FIXADA pelo nucleo derivado (sem parametro livre). Dois registros:
    a escada (SH0ES R22, o registro inteiro N*) e os 32 cronometros cosmicos de Moresco+ 2022 (registros intermediarios, importados do artigo 1, lidos com a lei
    ACUMULADA de z* ate z como em D1_kernel_discrimination do artigo 1) -- o teste que PODIA PERDER, com poder previo > 1 sigma (erros diagonais: poder
    sobrestimado, dito no veredito). Familias P (escada), Q (+Pantheon+), R (DR1), S (escada + cronometros), T (so cronometros: a incidencia nova); controle
    empilhado (P no modo tgl) ao lado. O veredito e o pre-registrado; cada um termina em NOT_A_CONFIRMATION. Se os registros intermediarios NAO leem o fator e
    a escada le, a leitura «so a sombra (os leitores locais por distancia) le o vazamento; os relogios intermediarios leem a face» fica registrada como [OPEN/ONTO]
    para o operador -- nao adotada. NOT_FALSIFIED nao e CONFIRMADA; a RG e o limite classico."""
    d = os.path.join(CACHE, "bancada_30set")
    lidos, hashes = {}, {}
    for k, fn in _V378_BANCADA_FILES.items():
        obj, ht, hb = _read_external_json_with_hashes(os.path.join(d, fn))
        lidos[k] = obj
        try:
            with open(os.path.join(d, fn), "rb") as fh:
                full = hashlib.sha256(fh.read()).hexdigest()
        except Exception:
            full = None
        hashes[k] = {"file": fn, "sha16_text": ht, "sha16_bytes": hb, "sha256_bytes": full}
    pre = lidos.get("fase4_pre") or {}; res = lidos.get("fase4_res") or {}; smoke = lidos.get("fase4_smoke") or {}; cc = lidos.get("cc_moresco") or {}
    fam = res.get("familias") or {}
    G = lambda f, n: (((fam.get(f) or {}).get("nucleos") or {}).get(n) or {})
    Pb, Pa, Tb, Ta, Sb, Qb, Rb = G("P_dr2_escada", "d1b"), G("P_dr2_escada", "d1a"), G("T_dr2_cc", "d1b"), G("T_dr2_cc", "d1a"), G("S_dr2_escada_cc", "d1b"), G("Q_dr2_escada_pantheon", "d1b"), G("R_dr1_escada", "d1b")
    Pc = (res.get("controle") or {}).get("P_empilhado") or {}
    postP = (fam.get("P_dr2_escada") or {}).get("posterior_d1b") or {}; postT = (fam.get("T_dr2_cc") or {}).get("posterior_d1b") or {}
    v4, vT = str(res.get("veredito") or ""), str(res.get("veredito_T") or "")
    beta = float(core.get("beta") or 0.0)
    permitidos = pre.get("vereditos_permitidos") or []
    cc_prov = ((pre.get("dados") or {}).get("cc") or {}).get("proveniencia") or {}
    ptb = Pb.get("pontos", {}).get("tgl") or {}
    checks = [
        ("Os artefatos da Fase 4 (pre-registro, resultado, prova de fumaca, cronometros) e a reanalise LIDOS POR HASH do cache do rito", all(lidos.get(k) is not None for k in _V378_BANCADA_FILES)),
        ("O RESULTADO conferiu o sha256 do SEU pre-registro e o hash bate com o arquivo lido aqui", str(res.get("preregistro_sha256")) == str(hashes["fase4_pre"]["sha256_bytes"])),
        ("Os cronometros: o JSON lido aqui tem o sha256 que o RESULTADO e o pre-registro gravaram; 32 pontos importados do artigo 1 (sha256 do artigo registrado)",
         str((res.get("cc") or {}).get("json_sha256")) == str(hashes["cc_moresco"]["sha256_bytes"]) == str(cc_prov.get("json_sha256")) and int((res.get("cc") or {}).get("n") or 0) == 32
         and str((cc.get("proveniencia") or {}).get("artigo_sha256") or "").startswith(str((res.get("cc") or {}).get("artigo_sha256") or "x")[:16])),
        ("A convencao do artigo declarada no pre-registro (beta so na lei; fundo LCDM) e o nucleo D1b como PRIMARIO",
         "beta_no_fundo = 'nao'" in str(pre.get("convencao", "")) and "PRIMÁRIO" in str((pre.get("nucleos") or {}).get("d1b", ""))),
        ("A funcao de aproximacao a assintota FIXADA pelo nucleo derivado (sem parametro livre), decidida antes de ver o dado", "sem parâmetro livre" in str(pre.get("decisao_da_variavel_assintotica", ""))),
        ("As cinco familias P, Q, R, S, T presentes com os dois nucleos; o controle empilhado ao lado", all(G(f, n).get("z_delta") is not None for f in ("P_dr2_escada", "Q_dr2_escada_pantheon", "R_dr1_escada", "S_dr2_escada_cc", "T_dr2_cc") for n in ("d1b", "d1a")) and Pc.get("z_delta") is not None),
        ("O veredito base e um dos PRE-REGISTRADOS; o da familia T presente; os dois terminam em NOT_A_CONFIRMATION sem palavra proibida (a MESMA guarda do rito)",
         any(v4.startswith(p) for p in permitidos) and bool(vT) and v4.endswith("__NOT_A_CONFIRMATION") and vT.endswith("__NOT_A_CONFIRMATION") and not (_V378_GUARDA.search(v4) or _V378_GUARDA.search(vT))),
        ("beta_tgl do RESULTADO = alpha.sqrt(e) do core a 1e-9 relativo (nunca literal)", beta > 0 and res.get("beta_tgl") is not None and abs(float(res["beta_tgl"]) / beta - 1.0) < 1e-9),
        ("O poder previo dos cronometros (prova de fumaca, por hash) > 1 sigma: o bloco T era um teste com poder, nao UNDERPOWERED a priori", smoke.get("poder_cc_sigma") is not None and float(smoke["poder_cc_sigma"]) > 1.0),
        ("Os posteriores de P e T (d1b) presentes, com delta = beta - beta_TGL nas amostras", postP.get("delta") is not None and postT.get("delta") is not None),
        ("O pre-registro DECLARA o que a gerencia ja tinha visto (visto_antes: a DIRECAO do bloco T ja fora vista na prova de fumaca -- cego PARCIAL, aferidor C5) e a circularidade (a familia P nao testa a descoberta da lei; a incidencia nova e T); os erros diagonais dos cronometros ditos",
         bool(pre.get("visto_antes")) and "cronômetros" in str(pre.get("visto_antes")) and bool(pre.get("circularidade_declarada")) and "DIAGONAL" in v4),
        ("O operador, verbatim: «concordo prossiga»", bool(_V378_OPERATOR_VERBATIM.get("proceed_20260930"))),
    ]
    ok = all(v for _, v in checks)
    if ok:
        verdict = ("TGL_BANCADA_FASE4_V378__ARTICLE_CONVENTION_BETA_ONLY_IN_THE_LAW_D1B_PRIMARY__LADDER_DELTA_Z_%s_PULL_AT_BETA_TGL_%s_LNB_TGL_VS_LCDM_%s__"
                   "INTERMEDIATE_REGISTERS_CC_DELTA_Z_%s_LAW_GAIN_Z_%s_LNB_%s__DIAGONAL_ERRORS_ONLY__JOINT_S_DELTA_Z_%s__STACKED_CONTROL_Z_%s__"
                   "OPEN_READING_SHADOW_READS_THE_LEAK_INTERMEDIATE_CLOCKS_READ_THE_FACE_NOT_ADOPTED__PREREGISTERED__READ_BY_HASH__NOT_A_CONFIRMATION"
                   % (_v378_tag(Pb["z_delta"]), _v378_tag(ptb.get("pull", 0.0)), _v378_tag(((Pb.get("evidencia") or {}).get("lnB") or {}).get("tgl_vs_lcdm", 0.0)),
                      _v378_tag(Tb["z_delta"]), _v378_tag(Tb.get("z_ganho_da_lei", 0.0)), _v378_tag(((Tb.get("evidencia") or {}).get("lnB") or {}).get("tgl_vs_lcdm", 0.0)),
                      _v378_tag(Sb["z_delta"]), _v378_tag(Pc["z_delta"])))
    else:
        verdict = "TGL_BANCADA_FASE4_V378__NOT_READ_THIS_RUN__%s__GATE_UNTOUCHED" % ("ARTIFACTS_ABSENT" if any(lidos.get(k) is None for k in _V378_BANCADA_FILES) else "CHECKS_FAILED")
    num = lambda blk, ks: {k: _v378_num(blk.get(k), 5) for k in ks}
    KS = ("delta", "sigma_delta", "z_delta", "z_perfil_beta_tgl", "z_ganho_da_lei", "beta_livre", "custo_por_nat_medido")
    return {"checks": checks, "all_verified": ok, "verdict": verdict, "hashes": hashes, "veredito_fase4": v4, "veredito_T": vT,
            "P_ladder_d1b": dict(num(Pb, KS), H0_bg=_v378_num(ptb.get("H0")), K=_v378_num(ptb.get("K"), 6), H0_local=_v378_num(ptb.get("H0_local")), pull=_v378_num(ptb.get("pull")),
                                 lnB=(Pb.get("evidencia") or {}).get("lnB"), chi2=Pb.get("chi2")),
            "P_ladder_d1a": num(Pa, KS), "Q_pantheon_d1b": num(Qb, KS), "R_dr1_d1b": num(Rb, KS), "S_joint_d1b": dict(num(Sb, KS), lnB=(Sb.get("evidencia") or {}).get("lnB")),
            "T_intermediate_d1b": dict(num(Tb, KS), lnB=(Tb.get("evidencia") or {}).get("lnB"), chi2=Tb.get("chi2")), "T_intermediate_d1a": num(Ta, KS),
            "stacked_control": num(Pc, KS), "posterior_P": {"delta": postP.get("delta"), "fracao_beta_acima_de_beta_tgl": postP.get("fracao_beta_acima_de_beta_tgl"), "fracao_beta_acima_de_zero": postP.get("fracao_beta_acima_de_zero")},
            "posterior_T": {"delta": postT.get("delta"), "fracao_beta_acima_de_beta_tgl": postT.get("fracao_beta_acima_de_beta_tgl"), "fracao_beta_acima_de_zero": postT.get("fracao_beta_acima_de_zero")},
            "power_prior_cc_sigma": smoke.get("poder_cc_sigma"), "cc_n": (res.get("cc") or {}).get("n"),
            "open_reading": ("[OPEN/ONTO, nao adotada] o que a Fase 4 MEDE: os relogios intermediarios sozinhos leem beta_hat consistente com zero (posterior P(beta > 0) ~ 0,6) e DESFAVORECEM a "
                             "leitura de fluxo acumulado em beta_TGL (ganho da lei -3,2 sigma; z_delta -3,1), com erros diagonais (a covariancia sistematica de Moresco+ 2020 nao entrou: a "
                             "significancia do bloco T fica sobrestimada por fator nao medido aqui); a direcao de T ja fora vista na prova de fumaca (visto_antes). A LEITURA: se os relogios "
                             "nao leem o fator e a escada (a sombra) le, entao so a sombra le o vazamento e os relogios leem a face -- a decisao e do operador; a leitura inversa (a lei "
                             "esta errada) e igualmente admissivel pelos dados"),
            "operator_verbatim": {"proceed_20260930": _V378_OPERATOR_VERBATIM["proceed_20260930"]},
            "does_not_gate_core": True, "statute": "[REAL -- medido na Bancada Um em 30/09/2026 (noite), pre-registrado e lido por hash]; NOT_FALSIFIED nao e CONFIRMADA; a RG e o limite classico"}
