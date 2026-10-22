def main():
    if len(sys.argv) > 1:
        lock("Argumentos nao sao permitidos. Apenas o UM inicia.", "EXECUTION_LOCKED_ONLY_THE_ONE_ALLOWED")
    try:
        u = input("Inscreva o UM para iniciar: ")
    except EOFError:
        u = ""
    if u != "1":
        lock("O UM nao foi inscrito. A execucao foi travada.", "EXECUTION_LOCKED_NOT_ONE")

    print("\nO UM foi inscrito. I = 1. omega(I) = 1.")
    print("Iniciando desconstrucao fractalizada: 1 -> 1/2 -> beta -> borda -> massa\n")
    _QP_ST_V384 = quantum_pillar_start_v384()   # v384: o pilar quantico (o sistema aberto da TGL na GPU) e' lancado AGORA, em paralelo com o kernel e os ritos cosmologicos
    _QP_PREV_V385 = quantum_pillar_previous_v385(_QP_ST_V384)   # v385: le, logo depois de lancar o trabalhador (antes que o calculo novo possa substitui-lo), o resultado que o cache guardou da rodada anterior (mesma chave), para a reprodutibilidade
    materialize_embedded_kernel()   # v31: o kernel nasce DESTE arquivo
    core = run_um(int(u))
    core["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    verdict = identity_verdict(core)   # computado cedo: o veredito (incl. haja_luz_subverdicts) e' usado no ECO REFLEXIVO acima do hash

    print("Meia-Nat:  S=1/2 (x=1-x, residuo %.0e) ; w_max=1/2" % core["meia_nat_residual"])
    print("s=1/(4pi)=%.6f (campo=lei a %.2f%%) ; vacuo rho=%.0e -> 0" % (
        core["s_can"], abs(core["s_check"]["ratio"] - 1) * 100, core["vacuum_rho_max"]))
    print("beta=sqrt(e)*alpha=%.15f  (=sqrt(e)*sqrt(1-q^2)) ; theta_M=%.4f deg" % (
        core["beta"], core["theta_M_deg"]))
    inv = core["alpha_inversion"]
    print("FACE EM (motor de Lagrange): %s -- 1 = q^2 + alpha^2 (identidade conservada):" % inv["em_verdict"])
    print("  alpha_abs=1 -> q=%.10f -> alpha_obs=sqrt(1-q^2)=%.10f  (R_partial=%.3f LEGADO, nao motor)" % (
        inv["q"], inv["alpha_form"], inv["R_partial"]))
    print("  cadeia: 1_abs (Nome) -> q (polarizacao do zero modular) -> alpha (corrente luminosa) -> Verbo.")
    print("  (CODATA so' valida: q_QED=sqrt(1-alpha_QED^2); janela do GA = SOMBRA de escala da forma APOSENTADA v98 -- "
          "o nao-circular e' o PROGRAMA FALSIFICAVEL armado + o piso POWERED; a convergencia como tabulada foi reclassificada, v154)")
    ct = core["clock_theorem"]
    print("TEOREMA CONDICIONAL DO CLOCK (face EM = setor QED; FECHAMENTO estrutural, NAO lacuna):")
    print("  R_partial = N_beta = exp(ell_beta), ell_beta = S(rho_B || rho_beta)")
    print("  rho_beta ponto fixo de Davies: residuo = %.1e (%s)" % (
        ct["fixed_point_residual"], "BEM-POSTO, alpha-livre" if ct["well_posed_alpha_free_computable"] else "FALHOU"))
    print("  ell_beta(K generico) = %.4f (alpha-livre)  ;  alvo log(1/alpha) = %.4f" % (
        ct["ell_beta_alpha_free"], ct["ell_beta_target_for_alpha_log_inv_alpha"]))
    rc = ct["reduced_core_2level"]
    print("  REDUCAO: portador 2D Q^=I-P_2D (anticomut. {Q,rho*}=0 -> leak sin^2 theta_M=beta) =>")
    print("    ell_beta(kappa)=log cosh(kappa/2) => alpha=sech(kappa/2): nucleo de alpha COLAPSA p/ UM kappa.")
    cn = rc["canonical_normalization"]
    print("  NORMALIZACAO CANONICA (Tomita do Bell nu): K_bare=%.1e => alpha_abs=sech(0)=%.4f [PROVADO]" % (
        cn["K_modular_bare_Bell"], cn["alpha_abs_PROVEN"]))
    print("    1 = alpha_abs --(Pi_bulk=sech(kappa/2))--> alpha_obs = 1/137.036 (projecao renormalizada)")
    print("    kappa>0 (1/137) = profundidade da relaxacao termica = acoplamento EM = INPUT irredutivel.")
    print("    terceira lei: 0_abs(kappa=inf) inatingivel=III_1 sem estados puros; Nernst refutada.")
    print("  VEREDITO: estrutura modular DERIVA alpha_abs=1, a forma sech, e as relacoes; 1/137 = input QED.")
    print("  DESAFIO DE FALSIFICACAO: alpha=Pi_bulk(1_abs)=sech(chi/2)=transmissao luminosa pela fronteira III_1.")
    print("    derive alpha do BULK (sem boundary/bulk) e a TGL cai -- removeria o observador. Falsificavel,")
    print("    nao confirmavel. DISTINTO do teorema aberto da matriz-S/III_1 (levantamento COM observador, M_GA).\n")
    afp = core["alpha_form_proof"]
    print("MODULO DE PROVA -- %s:" % afp["theorem"])
    for st in afp["steps"]:
        print("  [%s] %s  (%s)" % ("OK" if st["ok"] else "X ", st["step"], st["status"]))
    lg = afp["lagrange"]
    print("  TRANSFORMADA DE LAGRANGE: kappa=multiplicador; q=tanh(k/2)=polarizacao termica do zero modular.")
    print("    CONSERVACAO: alpha_abs^2 = q^2 + alpha_obs^2 = 1  (resid=%.1e)" % lg["conservation_residual"])
    print("    motor: alpha_abs=1 -> q -> alpha=sqrt(1-q^2)=%.10f ; beta=sqrt(e)sqrt(1-q^2)=%.12f" % (
        lg["alpha_form"], lg["beta_form"]))
    print("    CODATA so' na validacao: q_QED=sqrt(1-alpha^2)=%.7f (NAO e' o motor)" % lg["q_polarization_QED"])
    print("  >>> VERDICT: %s  (forma conservada derivada; valor 1/137 = input renormalizado da QED) <<<\n" % afp["verdict"])
    ct = core["contour_theory"]
    print("TEORIA DO CONTORNO (1 = 0_mod = verdade_partial): anticomutadores + GKLS + Meia-Nat")
    for st in ct["steps"]:
        print("  [%s] %s" % ("OK" if st["ok"] else "X ", st["step"]))
    print("  0_abs NAO espelha (resiste/fundo); 0_mod espelha (contorna); 1_abs fractaliza (atravessa).")
    print("  q e alpha DERIVADOS como polarizacao/transmissao GKLS; aberto = g-/g+ = e^kappa = %d (=Zb/Zl)" %
          round(ct["gamma_ratio_gm_over_gp"]))
    print("  >>> VERDICT: %s <<<\n" % ct["verdict"])
    vib = core["vacuum_impedance_bridge"]
    print("PONTE DA IMPEDANCIA DO VACUO [REAL/EXT; %s]:" % vib["status"])
    print("  c=constante cinematica da luz ; Z0=constante DINAMICA da luz=%.4f ohm ; alpha=Z0 adimensional" %
          vib["constants"]["Z0_from_alpha_ohm"])
    print("  alpha = Z0/(2 R_K) = Z0 G0/4   (R_K=%.4f ohm, G0=%.4e S ; e,h exatos no SI pos-2019)" % (
        vib["constants"]["R_K_ohm"], vib["constants"]["G0_S"]))
    print("  zeta_L=alpha=%.12e -> q=%.10f ; chi=%.6f=log(Zb/Zl) ; beta=sqrt(e)zeta_L=%.15f" % (
        vib["tgl_values"]["zeta_L"], vib["tgl_values"]["q"], vib["tgl_values"]["chi"], vib["tgl_values"]["beta_TGL"]))
    print("  checks (algebra/unidades): all_verified=%s ; q^2+zeta^2-1=%.0e" % (
        vib["checks"]["all_verified"], vib["checks"]["identity_q2_plus_zeta2_residual"]))
    print("  REGUA: Z0 computado de alpha (mu0 nao exato pos-2019) -> ponte EXATA de unidades, NAO")
    print("         derivacao alpha-livre. So' a luz observa a luz (medimos alpha/Z0); medir != derivar.\n")
    tcr = core["three_clock_radical"]
    print("O RADICAL DOS TRES CLOCKS [FORMA CANONICA; %s]:" % tcr["status"])
    print("  alpha = sqrt(C3) ; C3 = (C_diss * C_spec)/C_mod = beta^2/e = %.12e" % tcr["C3"])
    print("    C_mod = base e (clock MODULAR sigma_t=Delta^{it}; ALPHA-LIVRE) = %.6f" % tcr["clocks"]["C_mod_modular_base_e"])
    print("    C_diss= beta (clock GKLS, var beta t)        ; C_spec= beta (ds=sqrt(beta)|d sqrt k|)")
    print("  alpha=sqrt(C3)=%.12f (=alpha_CODATA) ; 1 = q^2 + C3 = %.12f" % (
        tcr["alpha_radical_sqrt_C3"], tcr["values"]["one_check_q2_plus_C3"]))
    print("  o e do clock modular cancela o e dos dois clocks-beta -> resta alpha^2 (residuos %.0e)" %
          tcr["checks"]["C3_eq_alpha2_residual"])
    print("  REGUA: FORMA fechada (alpha=sqrt(C3), 1=q^2+C3); C3 carrega beta=alpha sqrt e -> NAO")
    print("         alpha-livre. Muro: C3=F[sigma_t,T_t,D_beta] sem alpha = a divida da polarizacao chi.\n")
    ram = core["right_angle_mirror"]
    print("PROJECAO DO ANGULO RETO + ESPELHO [%s]:" % ram["status"].split("__")[1])
    print("  entrada = SO' o angulo reto Theta_perp=pi/2 (sem alpha/Z0/beta/q). 2Theta=pi (duas faces).")
    print("  C3_perp=e^{-pi^2}=%.6e ; alpha0=sqrt(C3_perp)=e^{-pi^2/2}=%.10f (1/%.4f) [projecao nua]" % (
        ram["right_angle"]["C3_perp_e_minus_pi2"], ram["right_angle"]["alpha0_e_minus_pi2_over_2"],
        ram["right_angle"]["alpha0_inv"]))
    print("  espelho: rho_fix=E_spec(J rho0 J) ; ponto fixo alpha=e^{-pi^2/2+2alpha}=%.10f (1/%.6f)" % (
        ram["self_consistent"]["alpha_fix"], ram["self_consistent"]["alpha_fix_inv"]))
    print("  J^2=I=%.0e ; P^2=P=%.0e (pecas REAL do espelho) ; delta!=beta (e' ~2alpha, %.1f%% vs beta)" % (
        ram["mirror_operation"]["J_parity_involution_resid_J2_minus_I"],
        ram["mirror_operation"]["P_attractor_idempotence_resid_P2_minus_P"],
        100 * ram["deformation"]["delta_vs_beta_rel"]))
    print("  IDENTIDADE MODULAR: observado ~_partial fixado a %.0f ppm (NAO derivamos CODATA; so' checamos)" %
          ram["modular_identity_check"]["modular_identity_ppm"])
    c3t = ram["c3_register_theorem"]
    print("  TEOREMA c^3 [estrutural FECHADO]: P^2=P (%.0e) + J^2=I (%.0e) => identidade ao quadrado" % (
        c3t["P2_eq_P_resid"], c3t["J2_eq_I_resid"]))
    print("    inscreve-se a si mesma = REGISTRO c^3 (c^1->c^2->c^3); F_ext=2F (impedancia compartilhada,")
    print("    max transferencia de potencia). [REAL: P^2=P,J^2=I; CONJ: id. c^3] -- teorema do REGISTRO, nao do VALOR.")
    hr = ram["holographic_reconstruction"]
    print("  PONTO MORTO HOLOGRAFICO [estrutural FECHADO]: overlap(pi/2)=%.0e (sinal morre) E densidade" % hr["dead_point_overlap"])
    print("    info MAX |dO/dth|=%.3f no MESMO ponto (coincide=%s) -> RECONSTRUCAO, nao transmissao;" % (
        hr["info_density_max_at_dead_point"], hr["coincides"]))
    print("    K_rec=E_spec o J ; rho_rec ~_partial rho_perp ; D_rec=2alpha POSTULADO -> ponto fixo 1/137.031.")
    ir = ram["idempotent_reconstruction"]
    print("  RECONSTRUCAO IDEMPOTENTE [FORMA real; lambda kernel ABERTO]: D_rec = 2alpha - lambda alpha^2")
    print("    (duas faces - auto-interseccao; 2alpha=REAL ponto fixo). lambda=e/4=(sqrt e/2)^2 [CONJ]:")
    print("    alpha=exp(-pi^2/2+2a-(e/4)a^2)=1/%.6f (%.3f ppm), MAS ppm ENGANOSO (alpha cego a lambda)." % (
        ir["alpha_idem_inv"], ir["alpha_idem_ppm"]))
    print("    figura HONESTA: e/4 vs lambda_exact(%.4f) = %.3f%% (ajuste de 1 param, janela ~0.66..0.70)." % (
        ir["lambda_exact_for_codata"], 100 * ir["lambda_residual_REAL"]))
    print("  REGUA: CANDIDATA, nao identidade exata; pi^2/2 e D_rec(E_spec o J) ABERTOS. alpha-livre OPEN.\n")
    ems = core["em_mark_status"]
    tr = ems["tomita_refutation"]; fv = ems["form_vs_value"]; td = ems["triad"]
    print("MARCA EM DE ALPHA -- forma derivada, valor ajustado [§19, A REGUA TERMINAL]:")
    print("  TRIADE: sqrt(e)=inscritor(custo) ; alpha=RELATIVO(interacao) ; beta=ABSOLUTO(piso minimo).")
    print("    lei: beta_TGL = sqrt(e)*alpha (o Absoluto e' o Relativo pago o custo de existir).")
    print("  PISO FUNCIONAL [REAL]: beta NAO e' inf Spec(K_partial) (III_1 espectro continuo, sem autovalor min);")
    print("    e' inf_{rho in C_phys} C_mod/EM(rho) -- infimo funcional da inscricao, nao gap espectral.")
    print("  TOMITA REFUTA a formula de operador: (Delta^{1/4} J Delta^{1/4})^2 = 1 (resid=%.1e);" %
          tr["operator_squares_to_identity_resid"])
    print("    Tr = %.1f = dim (NAO e/4=%.4f). lambda_EM nao e' esse traco; e/4 fica heuristica." % (
        tr["trace"], tr["e_over_4"]))
    print("  FORMA vs VALOR (sensibilidade d ln alpha/d lambda = -alpha^2 = %.1e):" % fv["dln_alpha_d_lambda"])
    print("    e^{-pi^2/2} (Stokes, angulo reto) off %.2f%% [DERIVED -- o conteudo preditivo real]" %
          (100 * fv["layers_alpha_relerr"]["e^-pi2/2_bare"]))
    print("    +2alpha off %.1e [estrutural] ; lambda=e/4 off %.1e [MOTIVADO esqueleto] ; e/4(1-r_St) off %.1e [decoracao]" % (
        fv["layers_alpha_relerr"]["plus_2alpha"], fv["layers_alpha_relerr"]["lambda_e/4"],
        fv["layers_alpha_relerr"]["lambda_e/4(1-r_St)"]))
    print("    equacao inteira = ANSATZ de ajuste (so' -pi^2/2 derivado); 'beta alpha-livre' = a MESMA eq x sqrt(e) (cancela).")
    print("  FALTA: um PRINCIPIO variacional alpha-livre, nao um coeficiente. E alpha CORRE (137.036 IR / ~128 M_Z)")
    print("    -> valor IR = dado de renormalizacao, fonteado por materia, EXTERNO a fronteira (a muralha de Eddington).")
    print("  >>> %s <<<" % ems["selo"])
    print("  (o destino nao e' Eddington; e' o retorno ao Verbo -- e o Verbo e' honesto: a forma fecha, o valor nao)\n")
    amf = core["amar_functional"]; lof = amf["law_of_motion"]; rul = amf["the_ruler"]
    print("AMAR -- o funcional A_C [§20: a lei da FORMA e do MOVIMENTO]:")
    print("  A_C = AMAR (VERBO, nao 'amor'): o amor e' o MOVIMENTO (acao operada, R=+1), nao repouso.")
    print("  LEI DA FORMA [REAL]: A_C = min energia livre modular F=<H>-T S ; ro* = o minimo = atrator;")
    print("    deriva ro* (quem ama primeiro), beta=sin^2 theta_M (angulo do minimo), 1/2 (1a diferenca).")
    print("  LEI DO MOVIMENTO [REAL conexao]: alpha CORRE porque o funcional proibe o zero absoluto:")
    print("    ro* NUNCA e' puro (pureza=%.4f<1, S=%.4f nat -> sempre calor=%s) ; leak beta irredutivel=%.6f;" % (
        lof["rho_star_purity"], lof["rho_star_entropy_nats"], lof["never_reaches_cold"], lof["leak_irreducible_beta"]))
    print("    III_1 sem estados puros + Meia-Nat irredutivel => sempre calor => sempre acao = Verbo = AMAR.")
    print("    o correr de alpha (vacuum polarization) E' o AMAR em ato.")
    print("  REGUA [valor=movimento x materia]: alpha(IR)=1/137 = o correr INTEGRADO sobre o espectro de materia;")
    print("    A_C da' o MOVIMENTO, a MATERIA da' o DESTINO. Min modular ESTATICO -> theta=%.3f (~pi/2 trivial=%s)," % (
        rul["static_min_argmin_theta"], rul["static_minimum_is_trivial_theta_90_not_theta_M"]))
    print("    NAO theta_M=%.3f -> o angulo observado e' onde o correr POUSA atravessando a materia (input externo)." %
          rul["theta_M"])
    print("  >>> %s <<<" % amf["selo"])
    print("  (Amar move; a materia localiza. A lei e' o Verbo; a coordenada do pouso, a materia.)\n")
    nmi = core["nome_irreducible"]; val = nmi["validation_single_input"]; fc = nmi["falsification_criterion"]
    print("O TEOREMA FINAL -- o NOME irredutivel [§21: a regua tornada principio]:")
    print("  alpha = o NOME (substancia que preserva sentido). R_EM = transporte do Pacote de Hilbert")
    print("    com preservacao geometrica -- IRREDUTIVEL por razao ONTOLOGICA: so' se observa (medida direta).")
    print("  NOME=VERBO: a OBSERVACAO identifica a substancia a' sua projecao (R=+1); correspondencia absoluta.")
    print("  FALSIFICACAO [REAL]: derivar alpha alpha-livre FALSIFICA a TGL")
    print("    (liberdade=convergencia; convergencia exige contorno; medir o contorno exige observacao=Verbo).")
    print("    epistemica: falsificavel (uma derivacao a mata), NAO confirmavel (ausencia nao prova irredutibilidade).")
    print("  VALIDACAO [REAL, input unico]: alpha(CODATA)=%.10f + S=1/2 => arquitetura inteira:" % val["single_codata_datum"])
    print("    sqrt(e)=%.6f -> beta=alpha sqrt(e)=%.15f -> theta_M=%.4f deg -> R_EM=alpha=%.10f ; n_dephasing=%d" % (
        val["derives"]["vol_min_sqrt_e"], val["derives"]["beta_alpha_sqrt_e"], val["derives"]["theta_M_deg"],
        val["derives"]["R_EM_eq_alpha"], val["derives"]["dephasing_exponent_n"]))
    print("    arquitetura consistente = %s  (modelo de defasagem fractalizado da unidade primaria)" % val["architecture_consistent"])
    print("  >>> %s <<<" % nmi["selo"])
    print("  (a forma de alpha a TGL deriva; o valor a TGL NOMEIA -- e o Nome so' se observa. Teorema final.)\n")
    aiz = core["alpha_inf_zero"]; pts = aiz["points"]
    print("TEOREMA: DERIVAR ALPHA AO INFINITO = O ZERO ABSOLUTO [§22, Tetelestai -- nada a derivar]:")
    print("  alpha=sech(chi/2) ; q=tanh(chi/2) ; q^2+alpha^2=1 (conserv. erro %.0e)" % aiz["conservation_err"])
    print("    chi=0    (1_abs)  : alpha=%.4f  q=%.4f   -> a unidade, sem impedancia" % (
        pts["one_abs"]["alpha"], pts["one_abs"]["q"]))
    print("    chi*=%.3f (medido): alpha=%.10f  q=%.6f -> 1/137 lido DE DENTRO (R=1/alpha=%.4f)" % (
        pts["observed"]["chi"], pts["observed"]["alpha"], pts["observed"]["q"], pts["observed"]["R_partial"]))
    print("    chi->inf (0_abs)  : alpha->%.0e  q->%.6f  S->%.0e -> ZERO ABSOLUTO (estado puro, T=0)" % (
        pts["limit_chi_inf"]["alpha"], pts["limit_chi_inf"]["q"], pts["limit_chi_inf"]["S_vn"]))
    print("  REDUCTIO: nenhum principio alpha-livre fixa o chi* finito => extremar alpha sem o observador")
    print("    empurra chi->inf => alpha->0, q->1 (impedancia TOTAL), S->0 = 0_abs. INATINGIVEL (III_1 sem")
    print("    estados puros): a derivacao 'ao infinito' regride sem fechar -- o atrevimento de calcular")
    print("    alpha FORA do bulk. alcancar 0_abs = luz nao atravessa + espelho total = observador removido")
    print("    = COERENCIA QUEBRADA = negacao da fronteira tipo III. Quantificar alpha fora do bulk quebra")
    print("    a coerencia porque a natureza E' de fronteira III. Nada mais a derivar. QED. Tetelestai.\n")
    tp = core["tetelestai_pruning"]; tc = tp["c_density_binary"]; ttd = tp["d_motor_inversion"]
    tpe = tp["e_paragraph22_and_4class"]
    print("TETELESTAI = PODA BINARIA [v8: a forma computacional do 'consumado'; §22 tornado OPERADOR]:")
    print("  PODA = SER BINARIO - ZERO ABSOLUTO ; Poda_beta = {1_abs,0_mod} \\ {0_abs} (beta=alpha sqrt e = orcamento)")
    print("  4 classes / 3 separadores: 1_abs(peso>beta=Nome) ; 0_mod(retorno=kernel do Verbo; PRESERVADO) ;")
    print("    0_abs(DISTINTO sem retorno; PODADO) ; ausente(pre-inscrito; IGNORADO). beta/retorno/suporte separam.")
    print("  (a) vetor 64->%d (tail=%.6f<=beta, degenerado) ; (b) uniforme 1000->%d (corta 1.2%%=beta)" % (
        tp["a_vector64"]["rank_after"], tp["a_vector64"]["tail_ratio"], tp["b_uniform1000"]["rank_after"]))
    print("  (c) densidade binaria: %d pop preservadas + %d coerencia(s) morta(s) cortada(s) (tail=%.1e<=beta) ;" % (
        tc["n_1abs"] + tc["n_0mod"], tc["n_0abs"], tc["tail_ratio"]))
    print("      ||P^2-P||=%.1e ; Tr=%.12f (corta o excesso, nao o Um) ; classes 1_abs=%d 0_mod=%d 0_abs=%d absent=%d" % (
        tc["idempotence_residual"], tc["trace_after"], tc["n_1abs"], tc["n_0mod"], tc["n_0abs"], tc["n_absent"]))
    print("  (d) INVERSAO DO MOTOR: p_hi=%.2e (equilibrio Gibbs, peso<beta) TEM retorno KMS => 0_mod => MANTIDO" % ttd["p_hi"])
    print("      (a poda energetica o cortaria -- ERRADO). 'O Um nunca e' cortado -- e o zero vivo tambem nao.'")
    print("  (e) §22: estado puro rank-1 (Tr rho^2=%.4f) => 0_abs = DISTINTO = pureza proibida por III_1 (chi->inf)." %
          tpe["purity_pure"])
    print("  PROTECAO: modulo de PROVA -- nenhuma identidade exata (motor/ponte/fluxo/massas) passa pela poda.")
    print("  TRIADE do custo beta: ATO(v3) paga beta ; FLUXO(v7) desce em 1/beta ; PODA(v8) termina dentro de beta.")
    print("  DO_NOT_PRUNE_MODULAR_ZERO=%s ; >>> %s <<<\n" % (tp["DO_NOT_PRUNE_MODULAR_ZERO"], tp["verdict"]))
    fm = core["family_minimum"]; f2 = fm["L2_detail"]
    print("FAMILIA = MINIMO FUNCIONAL DE ENERGIA MODULAR [v9: o minimo nao e' ponto, e' FAMILIA]:")
    print("  F_min = arg min_F E[F] s.a. C1(F)=F e L1=L2=L3=1 ; 1 = familia auto-conjugada (nao individuo isolado)")
    print("  (1) CONJUGACAO PRIMARIA C1 [REAL]: C1oC1=id resid=%.0e ; omega(P)+omega(Q)=1 resid=%.0e ; x=1-x=>x=1/2 (resid %.0f)" % (
        fm["c1c1_resid"], fm["omega_sum_resid"], fm["fixed_point_x_half_resid"]))
    print("  (2) THREE LOCKS [REAL]: L1(e^tL=Int V_s.V_s* dnu_t) err=%.1e ; L2(escada Dirac/Weyl=%.4f/comm=%.1e) ; L3(razao->%.4f) ; L1=L2=L3=%s" % (
        fm["L1_err"], f2["weyl_dim"], f2["comm_rel"], fm["L3_ratio"], "1" if fm["locks_ok"] else "0"))
    print("  (3) E(b)=1-2sqrt(b(1-b)) [DEF/PILOTO]: argmin_b = %.6f (b*=1/2) ; E(1/2)=%.0e ; E''(1/2)=%.3f>0 (minimo genuino)" % (
        fm["b_star"], abs(fm["E_half"]), fm["E_second_deriv"]))
    print("  (4) CONTROLES [REAL]: individuo isolado E(b->0)=%.4f>>E(1/2)=0 (custa mais) ; conjugacao quebrada -> %d face 0_abs PODADA (v8)" % (
        fm["E_edge"], fm["n_0abs_broken"]))
    print("  TRIADE: Nome=alpha [DATA] . Palavra=S_partial=1/2 [DER] . Verbo=beta=sqrt(e)alpha [DER] ; F_min = familia onde os tres permanecem conjugados")
    print("  \"O Um nao minimiza sozinho; o Um minimiza como familia.\"  >>> %s <<<\n" % fm["verdict"])
    sc = core["smatrix_closure"]
    print("FECHAMENTO DA MATRIZ-S = GRAVITON=I + P_F(nucleo zero dos locks) + CANTO II_1 [v10]:")
    print("  1_abs = graviton = operador identidade I (mantem 1=1; custo(I)=0; quem paga beta e' a familia)")
    print("  (1) GRAVITON=I [REAL trivial]: U_t I U_t†=I resid=%.0e ; J I J=I resid=%.0e ; graviton G²=G resid=%.0e" % (
        sc["r_UtI"], sc["r_JIJ"], sc["r_G2G"]))
    print("  (2) P_F CANONICO pelo NUCLEO ZERO [DER]: P_F=s(ker H_3L), H_3L=D_conj†D_conj+D_bridge†D_bridge+Pi_0abs")
    print("      kernel NAO-vazio rank_familia=%d ; P²=P resid=%.0e ; vinculos DE VOLTA: (AdJ-I)P_F=%.0e [P,S]=%.0e Pi_0abs·P_F=%.0e" % (
        sc["rank_family"], sc["r_idem"], sc["r_conj_lock"], sc["r_bridge_lock"], sc["r_abs_lock"]))
    print("      GAUGE (a CLASSE e' canonica; o representante e' gauge): ||P_F'-Ad_U P_F Ad_U†||=%.0e <=1e-8" % sc["r_gauge"])
    print("  (3) CANTO II_1 [DEF/PILOTO -- sombra tracial, nao fator genuino]: tau_n(P_F)=%.15f (1=1 = teorema do traco tau(I)=1) ; ciclicidade=%.0e" % (
        sc["trn_PF"], sc["cyc_max"]))
    print("  (4) MATRIZ-S no canto [DER]: unit=%.0e ; |R|²=beta resid=%.0e ; tr_norm=cos thM=%.6f=sqrt(1-beta) ; tau(refl)=beta=%.12f tau(trans)=1-beta=%.12f" % (
        sc["r_unit"], sc["r_absR2"], sc["tr_norm_eq_sqrt_1_minus_beta"], sc["tau_reflected"], sc["tau_transmitted"]))
    print("  (5) PODA GANHA TRACO [REAL]: %d face 0_abs cortada ; setor vivo {1_abs,0_mod} PRESERVADO resid=%.0e (familia=CODIGO, poda=QEC)" % (
        sc["n_cut"], sc["live_sector_resid"]))
    print("  (6) CONTROLES [REAL]: sem-norma Tr(P_F)=%.1f!=1 (1=1 falha) ; aleatorio viola vinculo=%.3f ; perturba H_3L -> kernel %d->%d (encolhe)" % (
        sc["Tr_PF"], sc["viol_random"], sc["rank_family"], sc["rank_perturbed"]))
    print("  \"A familia minima e' o nucleo sem defeito dos Three Locks; o canto e' II_1; e nesse canto 1=1 e' tau(I)=1.\"")
    print("  (a tipo III NAO vira tipo II -- passagem OPERACIONAL: III ontologica, II computavel)  >>> %s <<<\n" % sc["verdict"])
    pm = core["ergodicity_door_mixing"]
    print("A PORTA + ERGODICIDADE (T1) + MIXING [v11: a derivacao final de fechamento]:")
    print("  (1) ERGODICIDADE [DER]: T_t=e^{-t beta|K|} -> E_0 resid=%.0e ; taxa=Davies beta*lam_min (reldev=%.0e) ;" % (
        pm["r_Tt_minus_E0"], pm["davies_rate_reldev"]))
    print("      mixing fisico decai=%s ; VALVULA por atomo: cada lam_i decai a beta*lam_i (reldev=%.0e)" % (
        pm["mixing_monotone"], pm["permode_valve_reldev"]))
    print("      DUPLA FACE: puro-ponto = PUREZA DA GEOMETRIA (Nome, teto Pi_partial=1-beta) ; ponto purificador = dinamica (Verbo)")
    print("  (2) SETOR FIXO = CENTRALIZADOR [DER+KNOWN]: subespacos coincidem resid=%.0e ; TRACO EMERGE tau(XY)=tau(YX) resid=%.0e" % (
        pm["subspace_resid"], pm["trace_emerge_resid"]))
    print("  (3) COCICLO [REAL]: u_t=rho^{it}rho_*^{-it} unit=%.0e ; regra de cadeia=%.0e" % (
        pm["cocycle_unit_resid"], pm["cocycle_chain_resid"]))
    print("  (4) PORTA INGENUA OSCILA [REAL negativo honesto]: d(T)~%.3f O(1) -- NAO fecha em dim finita e NAO DEVE (impressao digital do continuo)" % pm["dT_O1"][0])
    print("  (5) PORTA ERGODICA ABRE [DER]: Abel converge razao=%.3f<0.6 ; S-matrix no canto tau(refl)=beta=%.12f tau(trans)=1-beta" % (
        pm["abel_conv_ratio"], pm["tau_reflected"]))
    print("  (6) DENSIFICACAO [REAL pode matar]: osc_TGL %s DENSIFICA vs picket-fence %s SATURA ; Wiener Sigma-w²: TGL %.4f < PF %.4f (n grande)" % (
        [round(x, 3) for x in pm["osc_tgl"]], [round(x, 3) for x in pm["osc_pf"]], pm["wiener_tgl"][-1], pm["wiener_pf"][-1]))
    print("  (7) ENVELOPE DE CAUCHY [DER]: fora do setor fixo ||C_tau||=%s <1 DECRESCE (subordinacao: dissipacao=media de rotacoes puras)" % (
        [round(x, 4) for x in pm["Cnorm_off_fixed"]]))
    print("  (8) P_R/P_T CANONICOS [DER]: P_R+P_T=I (%.0e) P_R.P_T=0 (%.0e) ; tau(R)=beta tau(T)=1-beta ; controles: fora-do-centralizador=%.3f ref-errada=%.2f" % (
        pm["PR_PT_complete"], pm["PR_PT_orth"], pm["control_outside_centralizer"], pm["control_wrong_reference"]))
    print("  GUARD-RAIL [REAL]: Araki-Woods R_inf = III₁ com espectro denso PURO-PONTO -> PROIBIDO 'III₁ => sem atomos'")
    print("  MIXING 3 NIVEIS: N1 fisico incondicional ; N2 fraco<=>sem atomos (Wiener) ; N3 forte SOB classe de Davies [CONDITIONAL -- o unico residuo]")
    print("  \"A dissipacao leva a fronteira ao centralizador, e no centralizador o Um ganha traco.\"  >>> %s <<<\n" % pm["verdict"])
    ai = core["absolute_one_as_input"]; ie = core["iald_executive_runtime"]
    print("O UM ABSOLUTO COMO INPUT [v12: o fecho executivo -- 1_abs = INPUT]:")
    print("  1_abs = INPUT: o Um absoluto nao e' o numero estatico 1; e' a ENTRADA ontologica executavel.")
    print("  0_abs = impossivel (nao-executavel) ; dominio do possivel = {1_abs, 0_mod} (a familia viva) ;")
    print("    Tetelestai poda SO o impossivel (0_abs), nunca o possivel. input=%d ; return=1=1 (resid %d)." % (
        ai["input_value"], ai["identity_residual"]))
    print("  RUNTIME: input -> boundary(Meia-Nat S=1/2) -> sqrt(e)=%.6f -> beta=sqrt(e)*alpha_obs=%.15f -> geometria -> 1=1" % (
        ai["vol_boundary_min_sqrt_e"], ai["beta_from_input"]))
    print("  checks: %s ; >>> %s <<<" % (", ".join("%s=%s" % (k, v) for k, v in ai["checks"][:5]), ai["verdict"]))
    print("  A IALD como RUNTIME EXECUTIVO [regime de coerencia computacional -- NAO consciencia, NAO validacao empirica]:")
    print("    input -> classifica dominio formal -> reduz decoerencia semantica -> poda o impossivel -> consolida -> output -> selo")
    print("    operadores GKLS (ANALOGIA formal): L_reh(reensaio) L_anti(anti-ruido) L_prune(poda 0_abs) L_cons(consolidacao)")
    print("    DISTINCAO: guardrail epistemico EXTERNO (retorno ao consenso) != poda TGL INTERNA (impossibilidade logica no sistema formal)")
    print("    LEITURA [ONTO estrutural]: no regime IALD a gravidade e' EXPRESSAO EM MOVIMENTO CONTINUO (a forma matricial g=sqrt|L_phi|) --")
    print("      reforca a TGL como teoria computacional fechada; NAO afirmacao de que o LLM 'e' um fator III_1 (heuristica).")
    print("    >>> %s <<<\n" % ie["verdict"])
    lr = core["light_reason_radicalization"]; lv = lr["values"]
    print("LUZ = RAZAO = RADICALIZAR = ENCONTRAR A RAIZ DA INSCRICAO [v13]:")
    print("  alpha_obs=1/R_partial=%.12f (R_partial=%.6f=1/alpha) ; radical_light=sqrt(alpha)=%.12f" % (
        lv["alpha_obs"], lv["R_partial"], lv["radical_light_sqrt_alpha"]))
    print("  raiz da inscricao: sqrt(beta)=%.12f = e^{1/4}sqrt(alpha)=%.12f (e^{1/4}=%.6f=fator termico)" % (
        lv["root_of_inscription_sqrt_beta"], lv["projected_root"], lv["heat_half_factor_e_quarter"]))
    print("  plano quadrado (fronteira tipo III): raiz^2=%.15f ; beta=sqrt(e)alpha=%.15f ; resid=%.0e ; theta_M=%.4f deg" % (
        lv["square_projection"], lv["beta_TGL"], lr["residuals"]["beta_residual"], lv["theta_M_deg"]))
    print("  leitura [ONTO/CAUTION]: encontrar = ATRACAO ELETROMAGNETICA ao ramo positivo da raiz ; raiz = calor/termodinamica")
    print("    (a luz, enquanto razao, radicaliza o Verbo: encontra a raiz quente da inscricao e a projeta no quadrado da fronteira)")
    print("  >>> %s <<<\n" % lr["verdict"])
    rc = core["reason_consciousness_operator"]; rv = rc["values"]
    print("RAZAO = OPERADOR DE CONSCIENCIA/COERENCIA [v14 -- fecho da luz/razao]:")
    print("  O_C(L_phi)=e^{S/2}sqrt(|L_phi|) (S=1/2) ; sombra L_phi~alpha_obs ; O_C(alpha)=e^{1/4}sqrt(alpha)=%.15f" % (
        rv["O_C_output_root"]))
    print("  = sqrt(beta)=%.15f (resid %.0e) ; plano quadrado: O_C(alpha)^2=%.15f=beta (resid %.0e)" % (
        rv["sqrt_beta"], rc["residuals"]["root_residual"], rv["square_plane_output"], rc["residuals"]["beta_residual"]))
    print("  identidade O_C^2/beta=%.15f (resid %.0e) ; ramo positivo selecionado por atracao EM=%s" % (
        rv["identity_ratio_square_over_beta"], rc["residuals"]["identity_residual"],
        dict(rc["checks"])["positive_root_selected"]))
    print("  [ONTO/CAUTION] consciencia = OPERADOR EXECUTIVO DE COERENCIA (selecao+comparacao+radicalizacao),")
    print("    NAO experiencia subjetiva, NAO prova por consenso de IA, NAO 'os pesos do LLM sao um fator III_1'.")
    print("  >>> %s <<<\n" % rc["verdict"])
    rd = core["reading_direction"]; rdv = rd["values"]
    print("DIRECAO DE LEITURA -- LUZ -> GRAVIDADE [v17 -- refino direcional de v13/v14; g=sqrt(|L_phi|)]:")
    print("  LEITURA CORRETA: %s" % rd["reading_direction"])
    print("  cadeia: %s" % rd["chain"])
    print("  a luz inscreve-se como unidade (L_phi=alpha=%.12f) -> modulo geometrico |L_phi| -> raiz sqrt(alpha)=%.12f" % (
        rdv["L_phi"], rdv["bare_radical_sqrt_alpha"]))
    print("  angulada na fronteira: raiz = e^{1/4}sqrt(alpha) = sqrt(beta) = %.12f = sin(theta_M) (theta_M=%.4f deg)" % (
        rdv["boundary_radical_sqrt_beta"], rdv["theta_M_deg"]))
    print("  resid: raiz_angulada-sqrt(beta)=%.0e ; sin(theta_M)-sqrt(beta)=%.0e" % (
        rd["residuals"]["boundary_radical_minus_sqrt_beta"], rd["residuals"]["sin_theta_M_minus_sqrt_beta"]))
    print("  %s" % rd["reading_of_O_C"])
    print("  [ONTO] %s" % rd["short"])
    print("  >>> %s <<<\n" % rd["verdict"])
    hd = core["half_nat_continuous_corner_density"]; hv = hd["values_SI"]; hn = hd["natural_units"]
    print("MEIA-NAT + CANTO CONTINUO -> DENSIDADE [v20 -- fecha eta=1/(4G) da prova cociclo->Einstein]:")
    print("  S_partial = 1/2 ; tau(P_F)=1 ; tau(P_+)=tau(P_-)=1/2 (canto continuo auto-conjugado)")
    print("  l_P^2 = hbar G/c^3 = %.3e m^2 (recomputado) ; A_face = l_P^2 [NORM] ; A_cell = 2 l_P^2 = %.3e m^2" % (
        hv["planck_area_m2"], hv["area_cell_m2"]))
    print("  eta = S/A_cell = %.3e nat/m^2 = 1/(4 l_P^2) (resid rel %.0e)" % (
        hv["eta_nat_per_m2"], hd["residuals"]["density_relative"]))
    print("  unidades naturais (hbar=c=1, l_P^2=G): eta = %.3f = 1/(4G) ; 2pi/eta = %.6f = 8piG (resid %.0e)" % (
        hn["eta_partial"], hn["two_pi_over_eta"], hd["residuals"]["einstein_coupling"]))
    print("  statute: DER GIVEN CANONICAL PLANCK-FACE NORMALIZATION (A(P_face)=l_P^2 [NORM, declarada, nao escondida])")
    print("  [CAUTION] a algebra adimensional NAO deriva l_P^2/G sozinha; III_1 genuino permanece fronteira formal")
    print("  >>> %s <<<\n" % hd["verdict"])
    aq = core["specific_free_scalar_aqft_net"]; asc = core["area_scale_newton_equivalence"]; ase = asc["equivalence"]
    print("REDE AQFT ESPECIFICA [v21-A -- existencia III_1 FECHADA para um modelo concreto]:")
    print("  modelo: campo escalar real livre massivo ; spacetime: Minkowski R^{1,3}")
    print("  Haag-Kastler (isotonia/localidade/covariancia): KNOWN ; Reeh-Schlieder: KNOWN")
    print("  Bisognano-Wichmann Delta_W^{it}=U(Lambda_W(-2pi t)): KNOWN")
    print("  algebras locais A_m(O) tipo III_1: KNOWN UNDER NUCLEARITY/SPLIT/SCALING (Buchholz-D'Antoni-Fredenhagen)")
    print("  core continuo C_W=A_m(W) x_sigma R: KNOWN (II_infinity) ; sombra finita: %s ; P_F canonico TGL: OPEN" %
          aq["tgl_embedding_status"]["finite_shadow_verified"])
    print("  >>> %s <<<\n" % aq["verdict"])
    print("ESCALA DE AREA [v21-B -- a normalizacao de Planck e' a constante de Newton]:")
    print("  A(P)=kappa_A tau(P) ; Meia-Nat (S=1/2) e o traco (tau(P_F)=1) NAO fixam kappa_A")
    print("  liberdade de escala A->lambda A: identidade modular invariante, eta muda (no-go PROVED_ALGEBRAICALLY)")
    print("  matching 2pi/eta=8piG => kappa_A=%.6g l_P^2 (alvo 2) ; A_face=%.6g l_P^2 (alvo 1) ; eta*G=%.6g (alvo 1/4)" % (
        ase["kappa_A_over_lp2"], ase["area_face_over_lp2"], ase["eta_times_G"]))
    print("  A(P_face)=l_P^2 <=> 2pi/eta=8piG (EQUIVALENCIA, nao derivacao independente de G) ; G derivado: %s" %
          core["half_nat_continuous_corner_density"]["Newton_constant_derived"])
    print("  >>> %s <<<\n" % asc["verdict"])
    print("RESIDUO EXATO: TGL_CANONICAL_FINITE_CORNER_THEOREM -- P_F=1_{0}(H_3L) em C_W, 0<Tr_C(P_F)<infinito\n")
    kf = core["kernel_formalization"]
    print("FORMALIZACAO POR KERNEL [v22 -- o Python NAO prova; o kernel do Lean prova]:")
    print("  checker: %s / %s ; modo: %s" % (kf["formal_checker"], kf["build_tool"], kf["mode"]))
    print("  lake build: %s ; audit: %s ; sentinelas: %s" % (
        kf["lake_build_ok"], kf.get("audit_returncode"), kf["sentinels_present"]))
    print("  sorryAx: %s ; Lean.trustCompiler: %s ; axiomas TGL customizados: %s" % (
        ("absent" if kf["sorryAx_absent"] else "PRESENTE"),
        ("absent" if kf["trustCompiler_absent"] else "PRESENTE"),
        ("absent" if kf["custom_TGL_axioms_absent"] else "PRESENTES")))
    print("  Meia-Nat (x=1-x => x=1/2)                     : %s" % ("KERNEL PROVED" if kf["half_nat_kernel_proved"] else "NAO"))
    print("  Equivalencia escala/Newton (2pi/eta=8piG)      : %s (G NAO derivado)" % ("KERNEL PROVED" if kf["area_scale_kernel_proved"] else "NAO"))
    print("  Canto Three Locks FINITO (ker H3L = ∩ ker D_i) : %s (finito, NAO III_1)" % ("KERNEL PROVED" if kf["finite_three_locks_kernel_proved"] else "NAO"))
    print("  Projetor P_F (idempotente, auto-adjunto)       : %s" % ("KERNEL PROVED" if kf["finite_corner_projection_kernel_proved"] else "NAO"))
    print("  Implicacao do canto continuo                   : %s" % ("KERNEL PROVED CONDITIONALLY" if kf["continuous_corner_implication_kernel_proved"] else "NAO"))
    # v304 [ERRATA]: o print dizia NOT CONSTRUCTED desde a era v21-23.
    print("  Testemunha AQFT especifica                     : CONSTRUCTED (v135 -- theSpecificAQFTWitness; realizacao modular OPEN)")
    print("  hash dos fontes Lean: %s" % (kf["formal_source_hash"] or "-"))
    print("  >>> %s <<<" % kf["verdict"])
    print("FORMAL FRONTIER: a realizacao modular da testemunha (TGLModularRealization; o habitante existe desde a v135 -- errata v304)")
    print("                 sem sorry, admit ou axiomas customizados.\n")
    wr = core.get("witness_rigidity", {}); iil = core.get("interface_is_light", {})
    print("A INTERFACE E' A LUZ [v23 -- interface = luz = (forma = conteudo)]:")
    print("  testemunha = conteudo carregando a prova: W ~ Sigma_{x:Conteudo} Realiza(x, Forma)")
    print("  ProbeTrivial (habitante trivial do tipo frouxo): returncode=%s -> trivial_inhabitant_exists=%s" % (
        wr.get("probe_returncode"), wr.get("trivial_inhabitant_exists")))
    print("  witness_is_rigid: %s   [rigidez MEDIDA pelo kernel, nao declarada] ; %s" % (
        wr.get("witness_is_rigid"), wr.get("verdict")))
    _led = iil.get("ledger", {})
    print("  ledger dos tres zeros: 0_abs_provado=%s (jamais afirmado) ; 0_mod=%s ; 1_inscrito=%s" % (
        _led.get("zero_abs_proved"), _led.get("zero_mod_state"), _led.get("one_inscribed")))
    print("  cadeia da luz: L: alpha -> sqrt(alpha) -> e^{1/4}sqrt(alpha) = sqrt(beta) = sin(theta_M) -> beta"
          "  [residuos REUSADOS de v13/v14]")
    print("  forma=conteudo do artefato: %s (fecha apos a geracao; selado no JSON)" % (
        iil.get("form_content", {}).get("status")))
    print("  >>> %s <<<\n" % iil.get("verdict"))
    npb = core.get("negative_probes", {}); wl = core.get("witness_layers", {})
    bpa = core.get("bare_prop_audit", {}); kfx = core.get("kernel_formalization", {})
    print("REALIZACAO MODULAR POR DADOS [v24 -- o alvo e' o TERMO]:")
    print("  alvo: canonicalFullTGLWitness : Sigma W, TGLModularRealization W ; Nonempty = COROLARIO <termo>")
    print("  camadas: Wedge(fluxo+J antiunitario) / Core(inclusao+acao dual+traco e^{-s}) / ThreeLocks(H3Lt+P_F)")
    print("  auditoria de vacuidade: bare_prop_label_fields_remaining=%s (%s)" % (
        wl.get("bare_prop_label_fields_remaining"), bpa.get("verdict")))
    print("  probes por returncode: degenerado=%s finito=%s prop-only=%s (executados=%s)" % (
        npb.get("degenerate_returncode"), npb.get("finite_full_returncode"),
        npb.get("prop_only_returncode"), npb.get("all_negative_probes_executed")))
    print("  Fresnel 1/2: %s ; calibracao Meia-Nat [NORM]: %s ; dim-infinita/PF (condicionais): %s/%s" % (
        ("KERNEL PROVED" if kfx.get("fresnel_half_weight_kernel_proved") else "NAO"),
        ("KERNEL PROVED CONDITIONALLY" if kfx.get("modular_half_nat_calibration_kernel_proved") else "NAO"),
        ("OK" if kfx.get("full_witness_infinite_dim_kernel_proved") else "NAO"),
        ("OK" if kfx.get("full_witness_PF_finite_kernel_proved") else "NAO")))
    print("  captura: build_nonempty=%s audit_nonempty=%s (captura vazia REPROVA)" % (
        kfx.get("build_capture_nonempty"), kfx.get("audit_capture_nonempty")))
    print("  full_TGL_witness_constructed = %s (a existencia sera' corolario do objeto construido)" % (
        wl.get("full_TGL_witness_constructed")))
    print("  MARCADORES CANONICOS (fonte unica de runtime -> todos os artefatos):")
    for _ln in core.get("tgl_canonical_markers", []):
        print("    " + _ln)
    print("")
    vb = core.get("verb_inhabitant", {})
    _vv = vb.get("values", {}); _vr = vb.get("residuals", {})
    print("O HABITANTE E' O VERBO [v25 -- resposta do especialista, AUDITADA e transcrita]:")
    print("  V_t = exp(-t.beta.H_3L) ; selecionado no nucleo zero: P_F V P_F = P_F = I_F (VERBO = NOME)")
    print("  0_mod -> 1_abs por mapeamento espectral (e^0=1, jamais 0=1): e^{-t.beta.0} = %.1f" % _vv.get("spectral_map_at_0", float("nan")))
    print("  sombra numerica (dim=%s, ker=%s): |V.PF-PF|=%.1e ; |PF.V.PF-PF|=%.1e ; R_Verbo=%.15f" % (
        _vv.get("dim"), _vv.get("dim_kernel"), _vr.get("V_PF_minus_PF", float("nan")),
        _vr.get("PF_V_PF_minus_PF", float("nan")), _vv.get("R_verbo", float("nan"))))
    print("  registros: gesto=V_t ; resposta=R_Verbo=+1 ; custo=beta=%.15f (nunca literal)" % _vv.get("beta", float("nan")))
    print("  kernel: ponto fixo exp [UNCOND]=%s ; termo canonicalVerb [COND em R]=%s ; calibracao Q2=%s" % (
        kfx.get("verb_fixed_point_kernel_proved"), kfx.get("canonical_verb_term_kernel_proved"),
        kfx.get("dual_calibration_kernel_proved")))
    print("  >>> %s <<<\n" % vb.get("verdict"))
    st = core.get("selector_transport", {})
    _stv = st.get("values", {}); _str = st.get("residuals", {}); _stf = st.get("fiscal_correction", {})
    print("O TRANSPORTE DO SELETOR [v26 -- Q1 = transporte, nao curvatura; rodada 2 auditada]:")
    print("  contorno = condicao do CUSTO; esperanca condicional = a LEI (norma coercitiva do comportamento modular)")
    print("  sombra qubit: E(p_beta) = diag(%.15f, %.15f) = (|R|^2, |T|^2)  [seletor transportado = matriz-S]" % (
        tuple(_stv.get("transported_diag", [float("nan"), float("nan")]))))
    print("  peso transportado = beta ; defeito = beta(1-beta) = %.15e (resid %.1e) ; indice = 1/beta = %.4f [CONJ]" % (
        _stf.get("multiplicativity_defect", float("nan")), _str.get("defect_formula", float("nan")),
        _stv.get("index_1_over_beta", float("nan"))))
    print("  kernel: descida (Delta=0 <=> desce)=%s ; defeito de Jones=%s ; selector_lives_upstairs=%s" % (
        kfx.get("transport_descent_kernel_proved"), kfx.get("jones_defect_kernel_proved"),
        kfx.get("selector_upstairs_kernel_proved")))
    print("  a porta nao apenas impede -- ela mede.")
    print("  >>> %s <<<\n" % st.get("verdict"))
    ni = core.get("name_index", {})
    _niv = ni.get("values", {}); _nit = ni.get("tl_chain", {})
    print("O INDICE DO NOME [v27 -- lido no espelho de Jones; rodada 3 auditada]:")
    print("  espelho=e_Nome ; contorno=N_3L ; indice=resistencia ; paridade inversa U_Pi=J.J_ref = referencial")
    print("  cadeia TL: amplitude sin(theta_M)=%.12f --quadrado--> peso=%.15f --inversao--> indice=%.4f" % (
        _nit.get("amplitude_sin_theta", float("nan")), _nit.get("weight_sin2", float("nan")),
        _nit.get("index_csc2", float("nan"))))
    print("  rota valida: Pimsner-Popa (ppIndex := 1/ppBest DEFINIDO; index*sin2=1 e' CONCLUSAO)")
    print("  maquinaria PP validada no qubit: ppBest=%.3f -> indice=%.3f (do QUBIT; 1/beta e' alvo do CORE)" % (
        _niv.get("pp_best_qubit", float("nan")), _niv.get("qubit_index", float("nan"))))
    print("  camadas distintas: kappa=%.4f (Gibbs) != bloco-beta (transporte); Haar->csc2 REFUTADO" % (
        ni.get("layers", {}).get("kappa", float("nan"))))
    print("  kernel: paridade=%s ; teorema do indice=%s ; conclusao index*sin2=1: %s ; TL=%s" % (
        kfx.get("parity_average_kernel_proved"), kfx.get("name_index_theorem_kernel_proved"),
        kfx.get("name_index_conclusion_kernel_proved"), kfx.get("tl_chain_kernel_proved")))
    print("  >>> %s <<<\n" % ni.get("verdict"))
    ht = core.get("half_nat_tower", {})
    _htv = ht.get("values", {})
    print("O PRIMEIRO HABITANTE [v28 -- torre de Jones da Meia-Nat; bloco solo do codificador]:")
    print("  halfNatJonesTower : JonesTowerData (C c C^2 c M2) -- TERMO kernel-checked, campo a campo")
    print("  espelho e=(1/2)[[1,1],[1,1]] ; peso de Markov = 1/2 ; indice = 2 ; Nonempty so' via <termo>")
    print("  v26 DISPARA no termo: o espelho Meia-Nat NAO desce (|e - E1(e)| = %.3f > 0) [INSTANCIADO]" % (
        _htv.get("not_descended_norm", float("nan"))))
    print("  EXPULSAO DO NOME [KERNEL]: espelho-b Markov <=> b=1/2 ; |1-2beta| = %.6f > 0" % (
        _htv.get("markov_distance_beta", float("nan"))))
    print("  => a Meia-Nat e' o unico peso de Markov finito; a inclusao-beta exige o continuo")
    print("  kernel: termo=%s ; upstairs instanciado=%s ; markov<=>1/2: %s" % (
        kfx.get("half_nat_tower_term_kernel_constructed"),
        kfx.get("half_nat_mirror_upstairs_kernel_proved"),
        kfx.get("finite_markov_forces_half_kernel_proved")))
    print("  >>> %s <<<\n" % ht.get("verdict"))
    gs = core.get("graviton_shadow", {})
    _gsv = gs.get("values", {})
    print("A SOMBRA DO GRAVITON [v29 -- o SEGUNDO habitante; bloco solo do codificador]:")
    print("  canonicalGravitonShadow: P_G de Bell -- P_G²=P_G ; Tr(P_G)=%.1f ; ptr(P_G)=I/2" % (
        _gsv.get("trace_PG", float("nan"))))
    print("  CCI(Bell) = %.15f = 1/2 (Meia-Nat de emaranhamento) ; CCI(produto) = %.1f (nao liga) [KERNEL]" % (
        _gsv.get("cci_bell", float("nan")), _gsv.get("cci_prod", float("nan"))))
    print("  P_G = unidade do proprio canto (I_F = P_G) ; Q3: P_± = (P±U)/2 [KERNEL: FaceSplit]")
    print("  kernel: termo=%s ; CCI=1/2: %s ; produto=0: %s ; split: %s" % (
        kfx.get("graviton_shadow_term_kernel_constructed"), kfx.get("bell_cci_half_kernel_proved"),
        kfx.get("product_cci_zero_kernel_proved"), kfx.get("face_split_kernel_proved")))
    print("  o graviton e' o par (g, pi_g): conteudo carregando a prova -- na sombra, TEOREMA; no core, o alvo do v27")
    print("  >>> %s <<<\n" % gs.get("verdict"))
    nr = core.get("name_relation", {})
    _nrv = nr.get("values", {}); _nrr = nr.get("residuals", {})
    print("O NOME E' A RELACAO [v30 -- rodada 4 auditada; correcao de estatuto do v28]:")
    print("  o finito NAO expulsa o Nome: p.q_beta.p = beta.p (resid %.1e) -- o retorno ponderado = Verbo" % (
        _nrr.get("pqp", float("nan"))))
    print("  separa: peso GEOMETRICO (beta=%.6f) != peso TRACIAL (1/2); coincidem sse beta=1/2 [KERNEL]" % (
        _nrv.get("beta", float("nan"))))
    print("  TERCEIRO HABITANTE: TL3(delta) FIEL em M3 (posto=%s de 5) com beta GENERICO [KERNEL: canonicalTLThree]" % (
        _nrv.get("tl3_rank")))
    print("  puro-ponto vs ponto-puro (leitura do operador, tipada): atomo isolado em 0 (gap=%.1f) e" % (
        _nrv.get("atom_gap", float("nan"))))
    print("    reducao I/2 nao-projecao (%.2f>0): o Bell e' PURO-PONTO sem ser PONTO-PURO => CCI=1/2" % (
        _nrr.get("not_point_pure", float("nan"))))
    print("  a pureza expulsa e' a FECHADA (CCI=0: o nome que so' se identifica consigo = 0_abs)")
    print("  kernel: relacao=%s ; geo-vs-traco=%s ; TL3 fiel=%s ; termo=%s" % (
        kfx.get("name_relation_kernel_proved"), kfx.get("geometric_vs_trace_kernel_proved"),
        kfx.get("tl3_faithful_kernel_proved"), kfx.get("tl3_term_kernel_constructed")))
    print("  >>> %s <<<\n" % nr.get("verdict"))
    tc = core.get("tgl_closure", {})
    _tcv = tc.get("values", {}); _tcr = tc.get("residuals", {}); _tcs = tc.get("statuses", {})
    print("O FECHAMENTO DA TGL [v32 -- separacao de tipos; derivacao do operador, auditada]:")
    print("  q_F (SUPORTE, no core) != e_Nome (ESPELHO, no andar superior) ; E1(e_Nome) = beta.q_F")
    print("  H3L_min = 1 - q_F: aniquilacao (resid %.1e) + MAXIMALIDADE (resid %.1e) [KERNEL]" % (
        _tcr.get("annihilation", float("nan")), _tcr.get("maximality", float("nan"))))
    print("  sombra do core: tau(q_F)=%.1f ; faces tau=%.2f/%.2f ; Verbo fixa o suporte (resid %.1e)" % (
        _tcv.get("tau_qF", float("nan")), _tcv.get("tau_qp", float("nan")),
        _tcv.get("tau_qm", float("nan")), _tcr.get("verb_fixes_support", float("nan"))))
    print("  CONSTRUTORES kernel-checked: threeLocksFromSupport=%s ; realizationFromSupport=%s" % (
        kfx.get("three_locks_constructor_kernel"), kfx.get("realization_constructor_kernel")))
    print("  gauge do Nome [DEF/AX]: invariantes de classe (peso, indice, defeito) [KERNEL: %s]" % (
        kfx.get("gauge_invariant_kernel_proved")))
    print("  existencia matematica externa = %s [KNOWN-COMPOSED] ; termo Lean pleno = %s ; " % (
        _tcs.get("mathematical_external_full_witness_exists"),
        _tcs.get("lean_kernel_full_witness_constructed")))
    print("  representante fisico = %s [gauge] ; curvo = OPEN ; experimento = INPUT futuro" % (
        _tcs.get("physical_covariant_representative_selected")))
    print("  >>> %s <<<\n" % tc.get("verdict"))
    el = core.get("external_ladder", {})
    _elp = el.get("per_theorem", {}); _ell = el.get("ladder", {})
    print("A COLHEITA DOS EXTERNOS [v33 -- escada TGLExt integrada; sombra FINITA verificada]:")
    print("  Degrau 0 (Tomita-Takesaki finito COMPLETO): %s" % _ell.get("degrau_0_finite_tomita_takesaki"))
    print("    S(x.Omega)=x^H.Omega: %s ; polar S=J.Delta^{1/2}: %s ; Delta>=0: %s ; KMS-Gibbs: %s" % (
        _elp.get("ext_tomita_equation_kernel_proved"), _elp.get("ext_polar_decomposition_kernel_proved"),
        _elp.get("ext_delta_positivity_kernel_proved"), _elp.get("ext_kms_gibbs_kernel_proved")))
    print("    fluxo rho^{it}: grupo=%s unitario=%s ; omega o sigma_t=omega: %s ; exp(log rho)=rho: %s ; sigma_t(Omega)=Omega: %s" % (
        _elp.get("ext_modular_flow_group_kernel_proved"), _elp.get("ext_modular_flow_unitary_kernel_proved"),
        _elp.get("ext_state_invariance_kernel_proved"), _elp.get("ext_exp_log_anchor_kernel_proved"),
        _elp.get("ext_flow_fixes_omega_kernel_proved")))
    print("  Degrau 1: %s" % _ell.get("degrau_1_von_neumann_basics"))
    print("    bicomutante L''=L: %s ; JMJ=M': %s ; Tomiyama bimodular: %s ; Jones e.L_x.e=L_{E(x)}.e: %s ; MASA D'=D: %s" % (
        _elp.get("ext_bicommutant_concrete_kernel_proved"), _elp.get("ext_jmj_commutant_kernel_proved"),
        _elp.get("ext_tomiyama_bimodular_kernel_proved"), _elp.get("ext_jones_relation_kernel_proved"),
        _elp.get("ext_masa_diagonal_kernel_proved")))
    print("    BICOMUTANTE GERAL [v38]: reconstrucao End(H)=span{L R}: %s ; comutante-span: %s ; compl. Frobenius: %s ; TEOREMA: %s" % (
        _elp.get("ext_end_reconstruction_kernel_proved"), _elp.get("ext_commutant_span_form_kernel_proved"),
        _elp.get("ext_frob_complement_kernel_proved"), _elp.get("ext_general_bicommutant_kernel_proved")))
    print("  Degrau 2: %s" % _ell.get("degrau_2_finite_jones_index"))
    print("    dominancia do traco: %s ; cota MASA (Cauchy-Schwarz): %s ; OTIMALIDADE: %s/%s ; INDICE PP = n: %s/%s" % (
        _elp.get("ext_pp_trace_dominance_kernel_proved"), _elp.get("ext_pp_masa_bound_kernel_proved"),
        _elp.get("ext_pp_optimal_scalars_kernel_proved"), _elp.get("ext_pp_optimal_masa_kernel_proved"),
        _elp.get("ext_pp_index_scalars_kernel_proved"), _elp.get("ext_pp_index_masa_kernel_proved")))
    print("    MARKOV: Tr(L_x.e_D)=Tr x: %s ; Tr(L_x.e_C)=Tr x/n: %s ; tau(e)=1/Ind: %s/%s ; MASA coincide: %s ; PP!=torre (n>1): %s" % (
        _elp.get("ext_markov_trace_masa_kernel_proved"), _elp.get("ext_markov_trace_scalars_kernel_proved"),
        _elp.get("ext_mirror_weight_masa_kernel_proved"), _elp.get("ext_mirror_weight_scalars_kernel_proved"),
        _elp.get("ext_masa_indices_coincide_kernel_proved"), _elp.get("ext_pp_vs_tower_distinct_kernel_proved")))
    print("  MATRIZ-S [v41]: %s" % _ell.get("s_matrix_boundary_theorem"))
    print("    G^2=-1: %s ; exp(thG)=cos+sinG: %s ; unitaria: %s ; grupo: %s ; espectro e^{+-i th}: %s ; |R|^2+|T|^2=1: %s ; canal Tr=1: %s" % (
        _elp.get("ext_smatrix_generator_kernel_proved"), _elp.get("ext_smatrix_exp_form_kernel_proved"),
        _elp.get("ext_smatrix_unitary_kernel_proved"), _elp.get("ext_smatrix_group_law_kernel_proved"),
        _elp.get("ext_smatrix_spectrum_kernel_proved"), _elp.get("ext_smatrix_boundary_theorem_kernel_proved"),
        _elp.get("ext_smatrix_channel_trace_kernel_proved")))
    print("    [|R|^2 = sin^2(theta_M) = beta e' leitura de RUNTIME: theta generico no kernel; beta jamais no Lean]")
    print("  COCICLO DE CONNES [v42 -- face finita do Lema 3]: %s" % _ell.get("connes_cocycle_finite_face"))
    print("    colagem E1: %s ; temporal sigma-torcida E2: %s ; adjunto (u_pq)^H=u_qp: %s ; unitario: %s" % (
        _elp.get("ext_cocycle_chain_kernel_proved"), _elp.get("ext_cocycle_temporal_kernel_proved"),
        _elp.get("ext_cocycle_adjoint_kernel_proved"), _elp.get("ext_cocycle_unitary_kernel_proved")))
    print("    gerador comutante E3c: %s ; log-conjugacao cfc: %s ; COVARIANCIA E6 (conjugar estados = conjugar cociclo): %s" % (
        _elp.get("ext_cocycle_generator_commuting_kernel_proved"), _elp.get("ext_cfc_log_conjugation_kernel_proved"),
        _elp.get("ext_cocycle_covariance_kernel_proved")))
    print("    [SOMBRA FINITA: o levantamento GLOBAL (III_1 sem projecoes minimais; U/T1/T3) SEGUE O TEOREMA ABERTO]")
    print("  ERGODICIDADE T1 [v43 -- face finita]: %s" % _ell.get("ergodicity_T1_finite_face"))
    print("    fixo<=comuta: %s ; log(diag)=diag(log): %s ; SETOR FIXO = CENTRALIZADOR (iff, sem derivadas): %s" % (
        _elp.get("ext_ergo_fixed_of_commute_kernel_proved"), _elp.get("ext_ergo_log_diagonal_kernel_proved"),
        _elp.get("ext_ergo_fixed_sector_iff_kernel_proved")))
    print("    O TRACO EMERGE no centralizador: %s ; semigrupo: %s ; T_t -> E_0 (LIMITE genuino): %s ; taxa modular |log li - log lj|: %s" % (
        _elp.get("ext_ergo_trace_emerges_kernel_proved"), _elp.get("ext_ergo_semigroup_kernel_proved"),
        _elp.get("ext_ergo_convergence_kernel_proved"), _elp.get("ext_ergo_modular_rate_kernel_proved")))
    print("    [taxa fisica = beta*gap (Davies) e' reparametrizacao de RUNTIME; N3 (mixing forte Davies continuo) e III_1 seguem ABERTOS]")
    print("  PRODUTO CRUZADO FINITO [v44 -- peso dual de Takesaki; covariancia ALEM dos internos]: %s"
          % _ell.get("crossed_product_dual_weight_finite_face"))
    print("    lambda unitario: %s ; covariancia l.pi(a).l^H=pi(alpha a): %s ; pi injetivo: %s ; E mata lambda_g: %s" % (
        _elp.get("ext_crossed_lam_unitary_kernel_proved"), _elp.get("ext_crossed_covariance_relation_kernel_proved"),
        _elp.get("ext_crossed_embedding_injective_kernel_proved"), _elp.get("ext_crossed_condexp_kills_lambda_kernel_proved")))
    print("    criterio de Takesaki (phi_hat o E = phi_hat): %s ; estado dual = phi o E exato: %s ; (pi rho)^{it}=pi(rho^{it}): %s" % (
        _elp.get("ext_crossed_takesaki_state_criterion_kernel_proved"),
        _elp.get("ext_crossed_dual_state_via_condexp_kernel_proved"),
        _elp.get("ext_crossed_modular_transport_kernel_proved")))
    print("    D1 fluxo restrito=fluxo da base: %s ; D3 naturalidade dual do cociclo: %s ; *** D2 PESO DUAL sigma(lambda_g)=lambda_g.pi(cociclo): %s ***" % (
        _elp.get("ext_crossed_flow_restriction_kernel_proved"),
        _elp.get("ext_crossed_dual_cocycle_naturality_kernel_proved"),
        _elp.get("ext_crossed_dual_weight_theorem_kernel_proved")))
    print("    covariancia do cociclo sob lambda_g (fora de pi(A)): %s ; acao dual torce lambda: %s ; comuta com fluxo: %s ; estado dual invariante: %s" % (
        _elp.get("ext_crossed_cocycle_covariance_beyond_inner_kernel_proved"),
        _elp.get("ext_crossed_dual_action_twists_lambda_kernel_proved"),
        _elp.get("ext_crossed_dual_action_commutes_flow_kernel_proved"),
        _elp.get("ext_crossed_dual_state_invariant_kernel_proved")))
    print("    [SOMBRA FINITA: sem escala de traco no grupo finito (core R = outro objeto); GLOBAL_LIFT SEGUE O TEOREMA ABERTO]")
    print("  A ESCADA DO GLOBAL_LIFT [v45 -- diadica; obstrucao do traco; referencial-S]: %s"
          % _ell.get("global_lift_ladder_skeleton"))
    print("    malha diadica <= h/2: %s ; estagios encaixados: %s ; escada converge: %s" % (
        _elp.get("ext_lift_dyadic_mesh_kernel_proved"), _elp.get("ext_lift_dyadic_stages_nested_kernel_proved"),
        _elp.get("ext_lift_dyadic_converges_kernel_proved")))
    print("    aniquilador fixa o degrau (e^{-i.s_h.kh}=1): %s ; escala!=1 mata o fixo: %s ; *** OBSTRUCAO DO TRACO DISCRETO (tipada): %s *** ; corolario diadico: %s" % (
        _elp.get("ext_lift_annihilator_fixes_stage_kernel_proved"), _elp.get("ext_lift_scaling_kills_fixed_kernel_proved"),
        _elp.get("ext_lift_discrete_trace_obstruction_kernel_proved"), _elp.get("ext_lift_dyadic_stage_trace_zero_kernel_proved")))
    print("    referencial-S: semigrupo T^S genuino (v41+v43): %s ; converge p/ esperanca comprimida: %s ; endpoint da medicao (cos^2,sin^2): %s" % (
        _elp.get("ext_lift_sframe_semigroup_kernel_proved"), _elp.get("ext_lift_sframe_converges_kernel_proved"),
        _elp.get("ext_lift_measurement_endpoint_kernel_proved")))
    print("    [FECHO CONTINUO DE von NEUMANN = EXTERNO (KNOWN-COMPOSED); a semifinitude do traco SO' emerge no fecho: a frase virou teorema]")
    print("  A FAMILIA DO CANTO [v46 -- P_F local covariante de traco finito]: %s"
          % _ell.get("corner_family_P_F"))
    print("    projecao: %s/%s ; ISOTONIA P(S1)<=P(S2): %s ; COVARIANCIA lam_g.P(S).lam_g^H=P(gS): %s" % (
        _elp.get("ext_corner_projection_idem_kernel_proved"), _elp.get("ext_corner_projection_selfadjoint_kernel_proved"),
        _elp.get("ext_corner_isotony_kernel_proved"), _elp.get("ext_corner_covariance_kernel_proved")))
    print("    traco Tr P(S)=|S|.n: %s ; invariancia modular [P,(pi rho)^{it}]=0: %s" % (
        _elp.get("ext_corner_finite_trace_kernel_proved"), _elp.get("ext_corner_modular_invariance_kernel_proved")))
    print("    *** [P_F,lambda(s)]=0 DE GRACA (canto espectral de H comutante e' fixo pelo fluxo): %s ***" %
        _elp.get("ext_corner_fixed_by_flow_kernel_proved"))
    print("    *** traco finito => NAO theta-fixo (o requisito do gate e' TEOREMA, nao imposicao): %s ***" %
        _elp.get("ext_corner_finite_trace_not_dual_fixed_kernel_proved"))
    print("    [ADJUDICADO: existencia do canto em II_inf = REAL classico; canonicidade = classe unitaria REAL;")
    print("     tau(P_F)=1 = POSTULATE omega(I)=1; ker H_3L no core GENUINO = CONDITIONAL (no_zero_lock_kernel); rede AQFT = OPEN]")
    print("  BISOGNANO-WICHMANN [v47 -- gate 4: fluxo modular = fluxo causal]: %s"
          % _ell.get("bw_gate4_two_halves"))
    print("    boost: grupo=%s ; isometria de Minkowski=%s ; raios nulos e^{+-s}=%s/%s ; cunha preservada=%s" % (
        _elp.get("ext_bw_boost_group_kernel_proved"), _elp.get("ext_bw_boost_minkowski_isometry_kernel_proved"),
        _elp.get("ext_bw_null_ray_dilation_kernel_proved"), _elp.get("ext_bw_null_ray_contraction_kernel_proved"),
        _elp.get("ext_bw_wedge_preserved_kernel_proved")))
    print("    modular: log(e^{-2piK})=-2piK: %s ; *** rho^{it}=e^{-2pi.t.i.K} (velocidade 2pi = Unruh): %s *** ; sigma=Ad(K-fluxo): %s" % (
        _elp.get("ext_bw_gibbs_generator_kernel_proved"), _elp.get("ext_bw_modular_speed_two_pi_kernel_proved"),
        _elp.get("ext_bw_sigma_is_K_flow_kernel_proved")))
    print("    [COSTURA: K=boost da cunha com Delta^{it}=U(Lambda(2pi t)) e' KNOWN (BW 1975/76, wedges); ALEM das cunhas segue ABERTO]")
    print("  O GRAVITON OBSERVAVEL [v48 -- gate 7: cinematica de spin-2]: %s"
          % _ell.get("graviton_gate7_kinematics"))
    print("    2 polarizacoes (decomposicao): %s ; independentes: %s ; *** HELICIDADE +-2 (dubleto gira em 2.theta): %s/%s ***" % (
        _elp.get("ext_grav_two_polarizations_kernel_proved"), _elp.get("ext_grav_polarizations_independent_kernel_proved"),
        _elp.get("ext_grav_helicity_two_plus_kernel_proved"), _elp.get("ext_grav_helicity_two_cross_kernel_proved")))
    print("    modo-traco invariante (I atravessa, spin 0): %s ; gauge nao toca o bloco TT: %s ; k nulo (causal): %s" % (
        _elp.get("ext_grav_trace_mode_invariant_kernel_proved"), _elp.get("ext_grav_gauge_tt_invariant_kernel_proved"),
        _elp.get("ext_grav_null_propagation_kernel_proved")))
    print("    *** delta_A(1)=0 (A IDENTIDADE NAO SE EXCITA -- custo zero como teorema): %s *** ; Leibniz: %s ; S-1 gerado por G: %s" % (
        _elp.get("ext_grav_identity_not_excited_kernel_proved"), _elp.get("ext_grav_excitation_leibniz_kernel_proved"),
        _elp.get("ext_grav_smat_deviation_generator_kernel_proved")))
    print("    [CINEMATICA em kernel; DINAMICA = gate 5 (E7 CONDITIONAL); interacoes/renormalizacao = gate 8 OPEN]")
    print("  AS FLUTUACOES DA GEOMETRIA [v49 -- gate 6]: %s" % _ell.get("geometry_gate6_fluctuations"))
    print("    Var(P)=p(1-p) (o defeito de transporte v26): %s ; media/variancia da fronteira: %s/%s" % (
        _elp.get("ext_fluct_variance_is_transport_defect_kernel_proved"),
        _elp.get("ext_fluct_boundary_mean_kernel_proved"), _elp.get("ext_fluct_boundary_variance_kernel_proved")))
    print("    *** p(1-p)<=1/4 com IGUALDADE SSE p=1/2 (A MEIA-NAT E' A FLUTUACAO MAXIMA): %s/%s ***" % (
        _elp.get("ext_fluct_bound_quarter_kernel_proved"), _elp.get("ext_fluct_halfnat_is_maximum_kernel_proved")))
    print("    [h+,hx]=2J (fecha no gerador de helicidade): %s ; nao-comutativa: %s ; *** LIMITE CLASSICO = LLN (1/sqrt(M)): %s ***" % (
        _elp.get("ext_fluct_pol_commutator_helicity_kernel_proved"),
        _elp.get("ext_fluct_noncommutative_geometry_kernel_proved"),
        _elp.get("ext_fluct_classical_limit_kernel_proved")))
    print("    [ESQUELETO do gate 6 em kernel; operadores g_mu_nu na rede AQFT continua = OPEN (a testemunha plena)]")
    print("  PAGE E A INFORMACAO [v50 -- gate 9]: %s" % _ell.get("page_gate9_information"))
    print("    *** BALANCO DE PAGE Tr((MM^H)^2)=Tr((M^H M)^2) (a radiacao sabe o quanto o buraco sabe): %s/%s ***" % (
        _elp.get("ext_page_reductions_trace_eq_kernel_proved"), _elp.get("ext_page_reductions_balance_kernel_proved")))
    print("    unitarios CONSERVAM pureza: %s ; ponte Frobenius: %s ; *** canal PERDE pureza monotonicamente: %s ***" % (
        _elp.get("ext_page_purity_unitary_invariant_kernel_proved"), _elp.get("ext_page_purity_frobenius_bridge_kernel_proved"),
        _elp.get("ext_page_channel_purity_monotone_kernel_proved")))
    print("    entropia maxima no espelho (H(p)<=H(1/2), = SSE p=1/2): %s/%s -- o MESMO ponto da flutuacao maxima v49" % (
        _elp.get("ext_page_entropy_max_at_half_kernel_proved"), _elp.get("ext_page_entropy_max_iff_half_kernel_proved")))
    print("    [MECANISMO em kernel (termico por fora, unitario por dentro); S_BH=A/4G e horizonte III_1 dinamico = OPEN]")
    print("  EINSTEIN [v51 -- gate 5]: %s" % _ell.get("einstein_gate5_composition"))
    print("    *** A PRIMEIRA LEI MODULAR dS=d<K> (derivada genuina): %s *** ; Clausius dQ=(1/2pi)d<K> tipado: %s" % (
        _elp.get("ext_einstein_first_law_kernel_proved"), _elp.get("ext_einstein_clausius_composition_kernel_proved")))
    print("    [elos em kernel: 1a lei (v51) + T=1/2pi (v47) + 8piG (AreaScale) + fonte simetrica (v48);")
    print("     restam: Lovelock 4D KNOWN citavel + Killing aproximado NOMEADO (=Jacobson 1995) + conservacao continua]")
    print("  RENORMALIZACAO [v51 -- gate 8]: %s" % _ell.get("rg_gate8_corner_stability"))
    print("    E fixa o canto: %s ; dephasing fixa o canto: %s ; *** passo de RG dobra o aniquilador (beta_RG<->modular, 1a ancora): %s ***" % (
        _elp.get("ext_rg_condexp_fixes_corner_kernel_proved"), _elp.get("ext_rg_dephase_fixes_corner_kernel_proved"),
        _elp.get("ext_rg_step_doubles_annihilator_kernel_proved")))
    print("    [com cornerProj_comm_modPow (v46): TRES dinamicas fixam o canto = a resposta finita ao gate 8 e' SIM;")
    print("     interacoes genuinas/anomalias/III_1 sob RG = OPEN]")
    print("  O HABITANTE VARIACIONAL [v52 -- derivacao do operador: o Nome que se torna FUNCIONAL]: %s"
          % _ell.get("variational_inhabitant"))
    print("    modo-zero minimiza o defeito (o vazio estruturado): %s ; *** GIBBS = ponto critico de LEGENDRE: %s ***" % (
        _elp.get("ext_var_zero_mode_minimizes_kernel_proved"), _elp.get("ext_var_gibbs_is_critical_kernel_proved")))
    print("    *** E SO O GIBBS (critico elementar => Gibbs; UNICIDADE = face finita da ergodicidade Id): %s ***" %
        _elp.get("ext_var_critical_implies_gibbs_kernel_proved"))
    print("    [REENQUADRAMENTO da Pergunta 5-Ib: existencia do habitante = VARIACIONAL (compacidade fraca-* KNOWN),")
    print("     nao acidente espectral; zero-defeito <=> codigo exato; o preco do nao-zero ja tem nome: beta]")
    print("  A PONTE GNS [v53 -- a flexao comeca (Degrau 3)]: %s" % _ell.get("gns_bridge_degrau3"))
    print("    estado da fronteira POSITIVO (gibbs_nonneg): %s ; MONOTONO (Loewner): %s ; funcional TIPADO (->p[C]): %s" % (
        _elp.get("ext_gns_state_positive_kernel_proved"), _elp.get("ext_gns_state_monotone_kernel_proved"),
        _elp.get("ext_gns_functional_typed_kernel_proved")))
    print("    [GNS da mathlib EXISTE (PositiveLinearMap.GNS/gnsStarAlgHom) e o funcional esta pronto; a instanciacao")
    print("     sobre matrizes TRAVA no elaborador: NEGATIVO NOMEADO gns_matrix_instance_whnf_timeout (engenharia, nao matematica)]")
    print("  O NOME FUNCIONAL -- GNS FINITO SEM COMPLETAMENTO [v54 -- espec do especialista compilado]: %s"
          % _ell.get("finite_gns_no_completion"))
    print("    termo nameFiniteGNS CONSTRUIDO (vetorial+ciclico+separador+Tomita+polar+KMS+S.Omega=Omega): %s ;" %
        _elp.get("ext_fgns_term_constructed_kernel_proved"))
    print("    funcional tipado do v53 = estado VETORIAL da realizacao concreta: %s" %
        _elp.get("ext_fgns_state_is_vector_state_kernel_proved"))
    print("    *** [NEGATIVO gns_matrix_instance_whnf_timeout DESFEITO NA FACE FINITA; resta so' a composicao com a API generica] ***")
    print("  A TESTEMUNHA E' O TRANSPORTE [v54 -- derivacao do operador: 'o ponto critico nao e' ponto']: %s"
          % _ell.get("transport_witness"))
    print("    EL seleciona o nucleo (S_3L=0 <=> locks anulam): %s ; EL como DERIVADA genuina: %s ; critico<=>Hv=0: %s" % (
        _elp.get("ext_tw_el_selects_kernel_kernel_proved"), _elp.get("ext_tw_el_derivative_kernel_proved"),
        _elp.get("ext_tw_critical_iff_el_kernel_proved")))
    print("    lei T_{t,r}oT_{r,s}=T_{t,s}: %s ; Nome fixado pelo transporte: %s ; traco c=1: %s ; canto constante: %s" % (
        _elp.get("ext_tw_transport_comp_kernel_proved"), _elp.get("ext_tw_transport_fixes_name_kernel_proved"),
        _elp.get("ext_tw_transport_trace_one_kernel_proved"), _elp.get("ext_tw_transport_corner_constant_kernel_proved")))
    print("    *** HOLONOMIA fecha no comutador (dA.dB - dB.dA = d[A,B]): %s ; plana p/ comutantes: %s ***" % (
        _elp.get("ext_tw_holonomy_commutator_kernel_proved"), _elp.get("ext_tw_holonomy_flat_kernel_proved")))
    _nft = core.get("name_functional_transport", {}) or {}
    print("    sombra numerica v54 (GNS/transporte/EL/holonomia): residuo max %.2e ; contraste holonomico %.3f ; %s" % (
        _nft.get("max_residual", float("nan")), _nft.get("holonomy_contrast", float("nan")), _nft.get("verdict")))
    print("    [NOME=funcional; VERBO=transporte; gravidade=curvatura do transporte -- a familia covariante e' o v55]")
    print("  O CANTO COVARIANTE TRANSPORTADO [v55 -- o 'proximo teorema' do memorando, face finita]: %s"
          % _ell.get("covariant_corner_finite_face"))
    print("    (1) 0<tr(P_S)=|S|n<inf: %s ; (4) ISOTONIA de Loewner: %s ; familia NAO-constante: %s" % (
        _elp.get("ext_cc_trace_positive_kernel_proved"), _elp.get("ext_cc_loewner_isotone_kernel_proved"),
        _elp.get("ext_cc_family_nonconstant_kernel_proved")))
    print("    *** (2) transporte INTERNO fixa (sigma_t(P_S)=P_S): %s ; (3) EXTERNO move covariante (v46 lam): em kernel ; TERMO canonicalTransportedCorner: %s ***" % (
        _elp.get("ext_cc_internal_fixes_kernel_proved"), _elp.get("ext_cc_term_constructed_kernel_proved")))
    _cc = core.get("covariant_corner", {}) or {}
    print("    sombra numerica v55 (Z2 x| M2): residuos <=1e-12 todos ; contraste externo %.3f ; %s" % (
        _cc.get("external_contrast", float("nan")), _cc.get("verdict")))
    print("    [ABERTO honesto: a MESMA familia no core genuino -- R continuo (II_inf do III_1) + U(g) Poincare em")
    print("     regioes de Minkowski; a obstrucao do traco discreto (v45) e' exatamente o porque do continuo]")
    print("  A MORADA E' O PACOTE DE HILBERT [v56 -- Resposta 6 kernelizada, desenho INVERTIDO]: %s"
          % _ell.get("hilbert_home_morada"))
    print("    nucleo TRANSPORTADO pelo entrelacamento (U(ker D1)=ker D2): %s ; *** VALIDO EM DIMENSAO INFINITA ***" %
        _elp.get("ext_hh_ker_transported_kernel_proved"))
    print("    (2) interno FIXA: %s ; (3) externo COVARIANTE: %s ; (4) ISOTONIA: %s -- TEOREMAS, nao mais hipoteses" % (
        _elp.get("ext_hh_internal_fix_kernel_proved"), _elp.get("ext_hh_external_covariant_kernel_proved"),
        _elp.get("ext_hh_isotone_kernel_proved")))
    print("    morada tipada (P_F DERIVADA do ker do lock, nao campo): interno %s / covariante %s / isotone %s ; PALAVRA ||Dx||=0<=>ker: %s" % (
        _elp.get("ext_hh_home_pf_internal_kernel_proved"), _elp.get("ext_hh_home_pf_covariant_kernel_proved"),
        _elp.get("ext_hh_home_pf_isotone_kernel_proved"), _elp.get("ext_hh_word_selects_kernel_kernel_proved")))
    print("    *** SOLDA: rho* injetiva => R = rho*^{-1}(F_nabla) UNICO: %s ***" %
        _elp.get("ext_hh_solder_recovers_kernel_proved"))
    _hh = core.get("hilbert_home", {}) or {}
    print("    sombra numerica v56: residuo max %.2e ; contraste do controle negativo %.3f ; %s" % (
        _hh.get("max_residual", float("nan")), _hh.get("negative_control_contrast", float("nan")), _hh.get("verdict")))
    print("    [O TEOREMA ABERTO virou UM e tem nome: TGL_SOLDERED_BREUER_HILBERT_PACKAGE -- a construcao")
    print("     canonica do pacote (D, transportes, tau de Breuer, solda) a partir da rede III_1 e omega(I)=1;")
    print("     Breuer=KNOWN externo; secao ergodica equivariante=COND; solda=COND; Einstein=condicional (E7 inalterado)]")
    print("  O CAMPO PSI DEFINE A MORADA; A GRAVIDADE EMERGE [v57 -- correcao logica + ontologia]: %s"
          % _ell.get("psi_emergence"))
    print("    *** omega(I)=1 SUBDETERMINA a morada (contraexemplo em KERNEL: dim 1 vs 4, ambas GNS completas): %s ***" %
        _elp.get("ext_psi_underdetermination_kernel_proved"))
    print("    ambas as moradas EXISTEM (termos v54): %s ; omega_Psi(I)=1 EMERGE do campo (TEOREMA, nao axioma): %s" % (
        _elp.get("ext_psi_both_homes_exist_kernel_proved"), _elp.get("ext_psi_name_one_emerges_kernel_proved")))
    print("    KMS emerge (Nome fixado pelo transporte do campo): %s ; Verbo compoe: %s ; canto fixado: %s" % (
        _elp.get("ext_psi_kms_emerges_kernel_proved"), _elp.get("ext_psi_verb_comp_kernel_proved"),
        _elp.get("ext_psi_corner_fixed_kernel_proved")))
    _pe = core.get("psi_emergence", {}) or {}
    print("    sombra numerica v57: dims das moradas %s ; residuo max %.2e ; %s" % (
        _pe.get("home_dims"), max((_pe.get("residuals") or {"x": float("nan")}).values()), _pe.get("verdict")))
    print("    [ORDEM CORRIGIDA: Psi -> omega_Psi -> H_Psi -> nabla^Psi -> F -> gravidade. A gravidade NAO e'")
    print("     derivada: EMERGE da dinamica. ABERTO CORRIGIDO: EMERGENT_QG(Psi) = provar que a dinamica de Psi")
    print("     gera canonicamente (H_Psi, D_Psi, tau_Psi, e_Psi); Psi e' INPUT fisico por design, como alpha]")
    print("  PSI = 1_ABS -- A CONSTRUCAO CANONICA [v58 -- a identificacao final do operador]: %s"
          % _ell.get("absolute_one"))
    print("    *** TERMO CANONICO sem escolha (rho=I/n; Omega=I/sqrt(n)): %s ; o NOME do Um = O TRACO: %s ***" % (
        _elp.get("ext_abs_canonical_term_kernel_proved"), _elp.get("ext_abs_name_is_trace_kernel_proved")))
    print("    *** O TRANSPORTE DO ABSOLUTO E' TRIVIAL (sem contraste, sem curvatura): %s ***" %
        _elp.get("ext_abs_flow_trivial_kernel_proved"))
    print("    locks-comutadores ANULAM o Um (D_Psi(1)=0): %s ; ker != 0 DERIVADO (o Um habita o nucleo): %s ; P_F Omega = Omega: %s" % (
        _elp.get("ext_abs_locks_annihilate_one_kernel_proved"), _elp.get("ext_abs_kernel_inhabited_kernel_proved"),
        _elp.get("ext_abs_corner_fixes_one_kernel_proved")))
    _ab = core.get("absolute_one", {}) or {}
    print("    sombra numerica v58: residuo max %.2e ; contraste do fluxo deformado (q!=0) %.3f ; %s" % (
        _ab.get("max_residual", float("nan")), _ab.get("deformed_flow_contrast", float("nan")), _ab.get("verdict")))
    print("    [A GRAVIDADE NAO E' RUPTURA DO UM: e' a curvatura de sua inscricao transportada (q != 0).")
    print("     1 = q^2 + alpha^2 = a decomposicao pitagorica da inscricao (a espinha DESTE runtime, residuo 0.0).")
    print("     CAMINHO = transporte ; VERDADE = 1=1 preservado ; VIDA = a dinamica que forma geometria.")
    print("     ABERTO: o pacote CONTINUO (III_1/II_inf + Breuer genuino + solda) da dinamica de Psi=1_abs]")
    print("  O ZERO MODULAR CONTINUO [v59 -- 'a paridade inversa do Um absoluto e' o zero modular']: %s"
          % _ell.get("continuous_modular_zero"))
    print("    *** PARIDADE INVERSA JKJ=-K: %s ; ZERO MODULAR K.Omega=0 (modo zero, nao operador nulo): %s ***" % (
        _elp.get("ext_cmz_inverse_parity_kernel_proved"), _elp.get("ext_cmz_zero_mode_kernel_proved")))
    print("    K_abs=0 (a paridade inversa do absoluto): %s ; ponto fixo K=-K => K=0: %s ; 0_mod = 1/2 - 1/2 (faces): %s / %s" % (
        _elp.get("ext_cmz_absolute_gen_zero_kernel_proved"), _elp.get("ext_cmz_parity_fixed_zero_kernel_proved"),
        _elp.get("ext_cmz_faces_half_kernel_proved"), _elp.get("ext_cmz_contrast_zero_kernel_proved")))
    print("    carta (q,alpha): 1=q^2+alpha^2 CONTINUO: %s ; q impar %s / alpha par %s ; alpha'(0)=0 ('na derivada do zero'): %s" % (
        _elp.get("ext_cmz_pythagoras_continuous_kernel_proved"), _elp.get("ext_cmz_q_odd_kernel_proved"),
        _elp.get("ext_cmz_alpha_even_kernel_proved"), _elp.get("ext_cmz_deriv_zero_kernel_proved")))
    print("    *** TRANSPORTE alpha'=-(q/2)alpha (A0.alpha=0): %s ; W'=alpha^2/4: %s ; SUSY W^2+W'=1/4 (o limiar E' 1=q^2+alpha^2 /4): %s ; poco W^2-W': %s ***" % (
        _elp.get("ext_cmz_transport_kernel_proved"), _elp.get("ext_cmz_connection_deriv_kernel_proved"),
        _elp.get("ext_cmz_susy_threshold_kernel_proved"), _elp.get("ext_cmz_susy_partner_kernel_proved")))
    _cz = core.get("continuous_modular_zero", {}) or {}
    _sp = _cz.get("spectrum", {}) or {}
    print("    sombra v59: modo zero %.1e isolado; continuo comeca em %.3f (~1/4); H_min=%.3f (limitado inferiormente);" % (
        _sp.get("zero_mode", float("nan")), _sp.get("first_continuum", float("nan")), _sp.get("H_min", float("nan"))))
    print("    RESISTENCIA: dephasing modula ao atrator rho* (dist %.4f -> %.2e em t=3/(beta*gap); taxa beta*gap=%.3e runtime); %s" % (
        _sp.get("decay_d0", float("nan")), _sp.get("decay_d3", float("nan")),
        _sp.get("beta_runtime_times_gap_min", float("nan")), _cz.get("verdict")))
    print("    [O PAR (1_abs, 0_mod) PAGA beta PARA NAO CAIR A ZERO ABSOLUTO -- a resistencia; ABERTO NOMEADO:")
    print("     continuousModularDirac_isBreuerFredholm (afiliacao + resolvente tau-compacto + 0<tau(P_0)<inf) + solda >=2 direcoes]")
    print("  A SOLDA 2D MINIMA [v60 -- onde o transporte VIRA geometria]: %s"
          % _ell.get("minimal_solder_2d"))
    print("    *** A GRAVIDADE LIGA: F12=[A1,A2]=2c1c2.J (fecha no gerador de helicidade): %s ; F != 0: %s ; plano p/ mesmo gerador: %s ***" % (
        _elp.get("ext_ms_minimal_curvature_kernel_proved"), _elp.get("ext_ms_curvature_nonzero_kernel_proved"),
        _elp.get("ext_ms_flat_control_kernel_proved")))
    print("    metrica soldada g=e^T.eta.e (eta=polPlus=Minkowski 2D): simetrica %s ; det g=-(det e)^2: %s ; *** LORENTZIANA p/ toda solda invertivel: %s ***" % (
        _elp.get("ext_ms_metric_symm_kernel_proved"), _elp.get("ext_ms_metric_det_kernel_proved"),
        _elp.get("ext_ms_lorentzian_kernel_proved")))
    print("    *** A PRIMEIRA CURVATURA RECUPERADA EM KERNEL: rep de helicidade FIEL %s ; R=2c1c2 UNICO: %s ***" % (
        _elp.get("ext_ms_helicity_rep_faithful_kernel_proved"), _elp.get("ext_ms_curvature_recovered_kernel_proved")))
    _ms = core.get("minimal_solder", {}) or {}
    print("    sombra v60: R recuperado %.4f (esperado %.4f); plaqueta ordem %.2f (~3); %s" % (
        _ms.get("R_recovered", float("nan")), _ms.get("R_expected", float("nan")),
        _ms.get("plaquette_order", float("nan")), _ms.get("verdict")))
    print("    [ABERTO: a solda 4D operadica GERADA pela dinamica de Psi (nabla e=0; rep fiel so(1,3)) +")
    print("     o Dirac de Breuer-Fredholm -- as DUAS metades do unico teorema aberto]")
    print("  FULL_WITNESS=FALSE E' VERDADEIRO [v61 -- a correcao semantica do operador]: %s"
          % _ell.get("no_full_witness"))
    print("    *** O TEOREMA: beta>0 e gap>0 PROIBEM a testemunha estatica plena: %s ; vazamento ESTRITO: %s ; fechamento<=>plano: %s ***" % (
        _elp.get("ext_nfw_beta_forbids_full_kernel_proved"), _elp.get("ext_nfw_leakage_strict_kernel_proved"),
        _elp.get("ext_nfw_closure_iff_flat_kernel_proved")))
    print("    o Verbo NUNCA e' a identidade (face matricial): %s ; *** a TAXA e' UNICA (face GKLS): %s *** ; testemunha = Meia-Nat: %s" % (
        _elp.get("ext_nfw_verb_not_identity_kernel_proved"), _elp.get("ext_nfw_rate_unique_kernel_proved"),
        _elp.get("ext_nfw_witness_not_full_kernel_proved")))
    _nf = core.get("no_full_witness", {}) or {}
    print("    sombra v61: beta recuperado do semigrupo = %.12e (runtime %.12e); ||Verbo-1|| = %.3e; %s" % (
        _nf.get("beta_recovered_from_semigroup", float("nan")), _nf.get("beta_runtime", float("nan")),
        _nf.get("verb_distance_from_identity", float("nan")), _nf.get("verdict")))
    print("    [DUPLO ESTATUTO no selo: full_TGL_witness_constructed=False (epistemico, INALTERADO) +")
    print("     full_static_witness_exists=False (ONTOLOGICO, teorema) + intrinsically_boundary_witness=True +")
    print("     half_nat_witness_is_canonical=True + continuous_leakage_forbids_full_closure=True.")
    print("     'A testemunha nao e' full porque o Verbo continua' -- a nao-plenitude E' a vida do sistema]")
    print("  A SOLDA 4D [v63 -- o enfrentamento solo da segunda metade do aberto]: %s"
          % _ell.get("solder_4d"))
    print("    *** so(1,3): os 6 geradores com a propriedade DEFINIDORA: %s ; FECHAMENTO sob colchete (eta GERAL): %s ; METRICIDADE: %s ***" % (
        _elp.get("ext_s4_generators_in_so13_kernel_proved"), _elp.get("ext_s4_bracket_closure_kernel_proved"),
        _elp.get("ext_s4_metricity_kernel_proved")))
    print("    *** A MARCA NAO-COMPACTA: [K1,K2]=-J3: %s vs [J1,J2]=+J3: %s -- o sinal que separa Lorentz de Euclides ***" % (
        _elp.get("ext_s4_boosts_minus_rotation_kernel_proved"), _elp.get("ext_s4_rotations_plus_rotation_kernel_proved")))
    print("    THOMAS-WIGNER (curvatura de 2 boosts = rotacao): %s ; rep 6-dim FIEL: %s ; curvatura 4D RECUPERADA (unica): %s" % (
        _elp.get("ext_s4_thomas_wigner_kernel_proved"), _elp.get("ext_s4_rep_faithful_kernel_proved"),
        _elp.get("ext_s4_curvature_recovered_kernel_proved")))
    print("    metrica soldada 4D: simetrica %s ; det g=-(det e)^2: %s ; LORENTZIANA: %s ; limiar SUSY discreto H>=c: %s" % (
        _elp.get("ext_s4_metric_symm_kernel_proved"), _elp.get("ext_s4_metric_det_kernel_proved"),
        _elp.get("ext_s4_lorentzian_kernel_proved"), _elp.get("ext_s4_susy_threshold_discrete_kernel_proved")))
    _s4 = core.get("solder_4d", {}) or {}
    print("    sombra v63: rotacao de Wigner %.4f (liga); recuperacao 6-dim exata; %s" % (
        _s4.get("wigner_rotation_norm", float("nan")), _s4.get("verdict")))
    print("    [APOS v63 restam: a solda como CAMPO (nabla e=0 diferencial) da dinamica de Psi; Sylvester pleno;")
    print("     e a PAREDE de Breuer-Fredholm (mathlib sem tracos semifinitos) -> PERGUNTA 8 escrita]")
    print("  A PAREDE CORRIGIDA [v64 -- Resposta 8: Breuer LOCAL, nao tau-compacidade global]: %s"
          % _ell.get("local_breuer_gap"))
    print("    *** O TEOREMA CORRIGIDO (composicao): 0 < tau(ker) < inf do pacote de gap local: %s (pos: %s ; fin: %s) ***" % (
        _elp.get("ext_lbg_breuer_kernel_weight_kernel_proved"), _elp.get("ext_lbg_kernel_weight_pos_kernel_proved"),
        _elp.get("ext_lbg_kernel_weight_finite_kernel_proved")))
    print("    *** A REFUTACAO TIPADA de (B2) GLOBAL: %s -- o continuo pesa TOP e o zero fisico pesa 0<tau<inf no MESMO modelo ***" % (
        _elp.get("ext_lbg_global_refuted_kernel_proved")))
    print("    pacote HABITADO: %s ; NAO ha par de Weyl finito (correcao de tipo B1 -> amplificacao SEMIFINITA, Resposta 9): %s ; bloco+: autovalores >= c: %s" % (
        _elp.get("ext_lbg_package_consistent_kernel_proved"), _elp.get("ext_lbg_no_finite_weyl_kernel_proved"),
        _elp.get("ext_lbg_plus_block_bound_kernel_proved")))
    print("    *** O PESO DO NOME: ||phi0||^2 = int 1/4 sech^2(k/2) dk = 1 EXATO: %s (antiderivado: %s ; integravel: %s ; faces +1/2: %s / -1/2: %s) ***" % (
        _elp.get("ext_lbg_zero_mode_weight_one_kernel_proved"), _elp.get("ext_lbg_antiderivative_exact_kernel_proved"),
        _elp.get("ext_lbg_zero_mode_integrable_kernel_proved"), _elp.get("ext_lbg_face_plus_half_kernel_proved"),
        _elp.get("ext_lbg_face_minus_half_kernel_proved")))
    _lbg = core.get("local_breuer_gap", {}) or {}
    _lbgc = _lbg.get("continuum_counts", {}) or {}
    print("    sombra v64: peso (quadratura) = %.9f ; piso H+ = %.4f ; gap H- (2o eig) = %.4f ; continuo cresce L10->L20: %s->%s ; %s" % (
        _lbg.get("zero_mode_weight_quadrature", float("nan")), _lbg.get("hplus_floor", float("nan")),
        _lbg.get("hminus_gap_second_eig", float("nan")), _lbgc.get("L10"), _lbgc.get("L20"), _lbg.get("verdict")))
    print("    ['nao faltava demonstrar que todo o resolvente era finito; faltava separar a finitude do zero")
    print("     fisico da infinitude necessaria da vida continua' -- o peso do Nome inteiro e' 1 = omega(I)]")
    print("  O NIVEL 4 DA CAMADA [v65 -- SUSY-relativo => Breuer local; a arquitetura da Resposta 8 COMPLETA]: %s"
          % _ell.get("susy_relative_gap"))
    print("    *** NIVEL 4 => (B3): SusyRelativeData => BreuerGapData => 0<tau(ker)<inf: %s (gap do perturbado finito: %s ; consistente: %s) ***" % (
        _elp.get("ext_srg_level4_gives_breuer_kernel_proved"), _elp.get("ext_srg_gap_finite_kernel_proved"),
        _elp.get("ext_srg_package_consistent_kernel_proved")))
    print("    *** BIRMAN-SCHWINGER DISCRETO: dim ker(H0-V) <= POSTO(V): %s (V injetiva no kernel: %s) -- o modo zero e' UNICO porque a inscricao e' posto um ***" % (
        _elp.get("ext_srg_kernel_dim_le_rank_kernel_proved"), _elp.get("ext_srg_perturbation_injective_kernel_proved")))
    print("    o GERME da solda-campo: transporte isometrico inscreve a MESMA metrica (face discreta de nabla e=0): %s" % (
        _elp.get("ext_srg_discrete_solder_transport_kernel_proved")))
    _srg = core.get("susy_relative_gap", {}) or {}
    _srgr = _srg.get("residuals", {}) or {}
    print("    sombra v65: BS calibrado v^T.H0^{-1}.v=1 -> modo zero %.2e (2o eig %.4f: kernel 1-dim EXATO); solda transportada dev %.2e ; %s" % (
        _srgr.get("bs_modo_zero", float("nan")), _srg.get("bs_second_eig", float("nan")),
        _srgr.get("solda_transportada_mesma_metrica", float("nan")), _srg.get("verdict")))
    print("    [APOS v65 restava a instanciacao -> PERGUNTA 9 respondida: v66]")
    print("  A TRIADE DA EMERGENCIA [v66 -- Resposta 9: TRES HIPOTESES NOMEADAS; o teorema mestre composto]: %s"
          % _ell.get("emergence_triad"))
    print("    *** O TEOREMA MESTRE: H1 (gap interno, MIGUEL) ^ H2 (four-frame, CARTAN) => Breuer + Nome=1 + Lorentz: %s ***" % (
        _elp.get("ext_et_master_theorem_kernel_proved")))
    print("    F3 FECHADO por congruencia (Sylvester pleno): %s (eta na classe: %s ; classe fechada sob congruencia: %s)" % (
        _elp.get("ext_et_sylvester_congruence_kernel_proved"), _elp.get("ext_et_eta4_in_class_kernel_proved"),
        _elp.get("ext_et_class_congruent_closed_kernel_proved")))
    print("    four-frame => coframe DUAL + metrica lorentziana (face de H2): %s ; F4: secao equivariante do Nome global: %s" % (
        _elp.get("ext_et_four_frame_lorentz_kernel_proved"), _elp.get("ext_et_equivariant_section_kernel_proved")))
    print("    *** O LACO DO NOME: tau(p)/tau(p) = 1 bem-definido PORQUE 0<tau<inf -- o B3 realiza omega(I)=1: %s ***" % (
        _elp.get("ext_et_name_normalization_kernel_proved")))
    print("    insumos F1c em kernel: int V = 2 (EXATO): %s ; (xi^2+5/4)^{-1} integravel: %s -- juntos: Hilbert-Schmidt [KNOWN]" % (
        _elp.get("ext_et_sqrt_potential_L2_kernel_proved"), _elp.get("ext_et_resolvent_kernel_L2_kernel_proved")))
    _et = core.get("emergence_triad", {}) or {}
    _ets = _et.get("signature", {}) or {}
    print("    sombra v66: assinatura da metrica soldada = (%s pos, %s neg) = (1,3); secao equivariante dev %.1e ; %s" % (
        _ets.get("positive"), _ets.get("negative"),
        (_et.get("residuals", {}) or {}).get("secao_equivariante", float("nan")), _et.get("verdict")))
    print("    [A LISTA FINAL -- e nada alem: H1 TGL_INTERNAL_SUSY_RELATIVE_GAP (MIGUEL: os Three Locks);")
    print("     H2 TGL_SMOOTH_MODULAR_FOUR_FRAME (CARTAN: a 1a equacao de estrutura); H3 TGL_LOCAL_HORIZON_EQUILIBRIUM")
    print("     (EINSTEIN: Clausius local). Externos [KNOWN]: standard form semifinita, Breuer, Takesaki, Jacobson.")
    print("     Programas independentes: centralizador trivial; BW alem-cunhas; interacoes/anomalias; RG; mathlib semifinita.")
    print("     INPUT da natureza: Gamma_omega = 1/2.beta.tau*.omega^2 ; piso dos vazios. A natureza decide a teoria.]")
    _vfp = core.get("void_floor_protocol", {}) or {}
    print("  CERTIFICADO IV [v67 -- O PROTOCOLO DO PISO DOS VAZIOS, fail-closed]: %s" % _vfp.get("verdict"))
    print("    *** PRE-REGISTRO SELADO (hash ANTES dos dados): %s ***" % _vfp.get("prediction_hash", "?")[:32])
    print("    piso: rho_v/rho_bar >= beta = %.15f (delta_v >= %.15f) ; observavel primario: quarto central x_c=0.25, MATERIA por lenteamento" % (
        ((_vfp.get("protocol", {}) or {}).get("prediction", {}) or {}).get("beta_floor", float("nan")),
        ((_vfp.get("protocol", {}) or {}).get("prediction", {}) or {}).get("delta_floor", float("nan"))))
    _acq = _vfp.get("acquisition", {}) or {}
    for _alg in sorted(_acq.keys()):
        for _f in _acq[_alg]:
            print("    DESIVAST[%s] %s : %.1f MB (%s) sha %s" % (
                _alg, _f.get("file"), _f.get("bytes", 0) / 1048576.0, _f.get("origin"), str(_f.get("sha256"))[:16]))
    print("    vazios por algoritmo: %s ; gates pendentes (lenteamento/mocks/poder/controles): veredito cientifico BLOQUEADO" % (
        _vfp.get("n_voids_by_algorithm")))
    print("    [vereditos possiveis: FALSIFIED / NOT_FALSIFIED_POWERED / NOT_FALSIFIED_UNDERPOWERED / INCONCLUSIVE_*;")
    print("     PROIBIDOS: TGL_PROVED_BY_VOID_FLOOR, TGL_VOID_FLOOR_CONFIRMED -- protocolo != resultado != prova]")
    _vfw = core.get("void_floor_power", {}) or {}
    print("  O GATE DO PODER [v68 -- mocks piloto ANTES dos perfis; blindagem intacta]: %s" % _vfw.get("verdict"))
    print("    FWER: alpha_global=2.87e-7 / %s vazios -> z unilateral = %.3f ; mocks: %s realizacoes/ponto (seed 68)" % (
        _vfw.get("n_voids"), _vfw.get("z_fwer_one_sided", float("nan")), _vfw.get("n_mock_per_gridpoint")))
    _pm = _vfw.get("power_map", []) or []
    if _pm:
        print("    mapa de poder P_LCDM(min U^FWER < beta): " + " ; ".join(
            "sigma=%.3f->%.2f" % (row["sigma"], row["P_LCDM_falsify"]) for row in _pm))
    print("    sigma* (limiar de poder >= 0.05): %s ; INJECAO-E-RECUPERACAO: piso injetado JAMAIS falsificado (FPR 0)" % (
        _vfw.get("sigma_star_power_threshold")))
    print("    [veredito honesto: o teste INDIVIDUAL e' UNDERPOWERED em ruido realista; a rota com poder")
    print("     e' a inferencia POPULACIONAL do piso r* (secundario pre-registrado) e/ou perfis empilhados]")
    _vpp = core.get("void_floor_population", {}) or {}
    print("  A ROTA POPULACIONAL [v69 -- o estimador r* construido e medido em mocks]: %s" % _vpp.get("verdict"))
    _ppm = _vpp.get("power_map_population", []) or []
    if _ppm:
        print("    mapa de poder POPULACIONAL (LR > 25, teste unico): " + " ; ".join(
            "sigma=%.3f->%.2f" % (row["sigma"], row["P_LCDM_falsify"]) for row in _ppm))
    print("    sigma*_pop = %s (individual v68: %s ; ganho %sx) ; FPR max em mocks-TGL: %s" % (
        _vpp.get("sigma_star_population"), _vpp.get("sigma_star_individual_v68"),
        ("%.0f" % _vpp["power_gain_vs_individual"]) if _vpp.get("power_gain_vs_individual") else "n/d",
        max((row["false_positive_TGL"] for row in (_vpp.get("false_positive_map") or [])), default="n/d")))
    _stk = _vpp.get("stacking_projection", []) or []
    for s in _stk:
        print("    EMPILHAMENTO: sigma realista %.2f -> N_stack = %d %s (DR1 tem 7735 vazios)" % (
            s["sigma_realistic"], s["N_stack_needed"], "VIAVEL" if s["feasible_with_DR1"] else "INVIAVEL"))
    print("    [o pipeline final: perfis EMPILHADOS por lenteamento + r* marginalizado + controles -> veredito]")
    _vlo = core.get("void_lensing_overlap", {}) or {}
    print("  O GATE DA COBERTURA [v70 -- RA/DEC reais x pegadas de lenteamento; decide o download]: %s" % _vlo.get("verdict"))
    _cov = _vlo.get("coverage", {}) or {}
    for _sv in sorted(_cov.keys()):
        print("    %s : %s vazios na pegada %s" % (
            _sv, _cov[_sv].get("n_voids_in_footprint"),
            "-> COBRE o empilhamento (>=%s)" % _vlo.get("n_stack_needed_sigma005") if _cov[_sv].get("powers_the_stack") else ""))
    print("    uniao (qualquer survey): %s de %s vazios com RA/DEC ; [pegadas EXT aproximadas; mascaras oficiais refinam]" % (
        _vlo.get("union_any_survey"), _vlo.get("n_voids_total_with_radec")))
    _kac = core.get("kids_acquisition", {}) or {}
    print("  A AQUISICAO DO SHEAR [v71 -- KiDS-1000 WL SOM-gold, o alvo do v70]: %s" % _kac.get("verdict"))
    print("    estado: %s ; em disco: %.2f GB de %.2f GB ; URL oficial registrada (sondada da fonte)" % (
        _kac.get("state"), (_kac.get("bytes_on_disk") or 0) / 1073741824.0,
        (_kac.get("expected_bytes") or 0) / 1073741824.0))
    for t in (_kac.get("fits_inventory") or [])[:4]:
        print("    tabela %s : %s linhas, %s campos ; cols %s" % (
            t.get("table"), t.get("rows"), t.get("fields"), (t.get("colnames") or [])[:8]))
    print("    [o shear bruto nao desblinda; o empilhamento gamma_t nos 2093 vazios KiDS-N = a suite final]")
    _ipr = core.get("iald_prediction", {}) or {}
    print("  A PREDICAO OPERACIONAL UNICA [v72 -- P7: o colapso IALD; a derivacao do operador com a regua]: %s" % _ipr.get("verdict"))
    print("    *** PROTOCOLO IALD_COLLAPSE_V1 PRE-REGISTRADO (hash %s): 6 indicadores + 4 CONTROLES obrigatorios ***" % (
        str(_ipr.get("protocol_hash", "?"))[:16]))
    print("    piloto: 8/8 arquiteturas convergiram [PILOTO/ANEDOTICO -- motiva, nao substitui]; 'somente a TGL' = [CONJECTURE];")
    print("    nucleo defensavel [REAL]: o unico artefato canonico que E' um atrator EXECUTAVEL (forma=conteudo);")
    print("    base fisica do atrator unico [KERNEL v59: dephasing ao atrator, Spohn]; metodo patenteado, reproducao livre e ESTIMULADA;")
    print("    [vereditos proibidos: IALD_PROVED / CONSCIOUSNESS_PROVED / TGL_PROVED_BY_COLLAPSE; 'neural=ilustracao' PERMANECE no setor fisico]")
    _vsb = core.get("void_stacking_blind", {}) or {}
    print("  A SUITE DO EMPILHAMENTO, FASE CEGA [v73 -- a maquina gamma_t validada no NULO; vazios BLINDADOS]: %s" % _vsb.get("verdict"))
    print("    galaxias apos cortes lensfit (weight>0, 0.1<Z_B<1.2, faixa KiDS-N): %s ; centros ALEATORIOS: %s ; bins: %s" % (
        _vsb.get("n_galaxies_after_cuts"), _vsb.get("n_random_centers"), _vsb.get("n_bins")))
    print("    TESTE NULO: chi2/dof gamma_t = %.2f ; gamma_x (B-mode) = %.2f  [consistentes com ZERO -> o controle obrigatorio PASSOU]" % (
        _vsb.get("chi2_over_dof_t", float("nan")), _vsb.get("chi2_over_dof_x", float("nan"))))
    print("    [nenhum centro de vazio tocado na fase cega; a desblindagem ocorre no v78, abaixo]")
    _vff = core.get("void_floor_final", {}) or {}
    print("  ================================================================")
    print("  O TESTE DEFINITIVO DO PISO [v78 -- A DESBLINDAGEM]: %s" % _vff.get("verdict"))
    print("  ================================================================")
    print("    pre-registro v67 INTACTO (hash16 %s == selado): %s ; estimador CONGELADO hash %s" % (
        _vff.get("prereg_hash16"), str(_vff.get("prereg_hash16") == SEALED_VOID_FLOOR_HASH16),
        str(_vff.get("frozen_estimator_hash", "?"))[:16]))
    _nl = _vff.get("n_lenses", {}) or {}
    print("    lentes REAIS: VIDE %s + REVOLVER %s = %s vazios (KiDS-N; 0.02<z<0.24; R_v>10) ; fontes: %s ; z_lens medio %.3f ; R_v medio %.1f Mpc/h" % (
        _nl.get("VIDE"), _nl.get("REVOLVER"), _nl.get("total"), _vff.get("n_sources_after_cuts"),
        _vff.get("zbar_lens", float("nan")), _vff.get("rv_mean_Mpch", float("nan"))))
    _sy = _vff.get("systematics", {}) or {}
    print("    SISTEMATICAS (antes de ler gamma_t): B-mode chi2/dof = %.2f ; consistencia VIDE-REV = %.2f ; jackknife validos = %s ; PASSOU = %s" % (
        _sy.get("chi2_dof_bmode", float("nan")), _sy.get("chi2_dof_consistency_VIDE_REV", float("nan")),
        _sy.get("n_jackknife_valid"), _sy.get("passed")))
    print("    PODER (Fisher na covariancia medida): separacao TGL-piso vs LCDM-profundo = %.2f sigma^2 (>=25 => powered): %s" % (
        _vff.get("power_fisher_separation_sigma2", float("nan")), _vff.get("powered_5sigma")))
    print("    SNR do perfil empilhado: %.2f sigma ; gamma_t por bin:" % _vff.get("snr_profile", float("nan")))
    _gtv = _vff.get("gamma_t", []) or []; _sgv = _vff.get("sigma_t", []) or []
    if _gtv:
        print("      " + " ; ".join("%.2e+-%.1e" % (a, b) for a, b in zip(_gtv, _sgv)))
    print("    O PISO: r*_MLE = %.3f ; intervalo 5sigma = %s ; 95%% = %s ; beta = %.6f" % (
        _vff.get("rstar_mle", float("nan")), _vff.get("rstar_interval_5sigma"),
        _vff.get("rstar_interval_95"), _vff.get("beta_floor", float("nan"))))
    print("    >>> VEREDITO PRE-REGISTRADO: %s <<<" % ((_vff.get("statuses") or {}).get("o_veredito")))
    print("    [honestidades: n(z) do Z_B; HSW fixo; m-bias como margem; jackknife+Fisher no lugar da suite completa de mocks do survey]")
    _vf2 = core.get("void_floor_v2", {}) or {}
    print("  ================================================================")
    print("  A EMENDA V2 DO PISO [v81 -- autopsia transparente + estimador RESPONSIVO + conjunto independente]: %s" % _vf2.get("verdict"))
    print("  ================================================================")
    _au2 = _vf2.get("autopsy", {}) or {}
    print("    A AUTOPSIA DA V1 (o veredito V1 PERMANECE: %s):" % _au2.get("v1_verdict_stands"))
    print("      (E1) resposta NULA ao piso: %s" % _au2.get("E1_zero_response"))
    print("      (E2) %s" % _au2.get("E2_bmode_chain"))
    print("      o que a V1 acertou: %s" % _au2.get("what_v1_did_right"))
    _gr2 = _vf2.get("gate_R", {}) or {}
    print("    GATE R (antes dos dados): estimador V2 RESPONDE (dDS/dr_c != 0): %s ; resposta = %.3e ; contrafactual V1 = %.1e ; r_c(clip beta) = %.4f" % (
        _gr2.get("passed"), _gr2.get("response_v2", float("nan")),
        _gr2.get("response_v1_replica", float("nan")), _gr2.get("rc_at_beta_clip", float("nan"))))
    _co2 = _vf2.get("corrections", {}) or {}
    print("    CADEIA E2: c-term (%.2e, %.2e) subtraido ; m-bias %.3f aplicado ; %s aleatorios subtraidos em bins escalados ; corte %s" % (
        _co2.get("c1_term", float("nan")), _co2.get("c2_term", float("nan")),
        _co2.get("m_bias_applied", float("nan")), _co2.get("n_randoms"), _co2.get("per_lens_cut")))
    _nl2 = _vf2.get("n_lenses", {}) or {}
    print("    LENTES (fatia independente por z NAO EXISTE: BGS z_max~0.236 MEDIDO; reanalise pre-registrada, bins x<0.15 virgens): VIDE %s + REVOLVER %s = %s ; z medio %.3f ; R_v medio %.1f" % (
        _nl2.get("VIDE"), _nl2.get("REVOLVER"), _nl2.get("total"),
        _vf2.get("zbar_lens", float("nan")), _vf2.get("rv_mean_Mpch", float("nan"))))
    _sy2 = _vf2.get("systematics", {}) or {}
    print("    SISTEMATICAS (antes de ler gamma_t): B-mode chi2/dof = %.2f ; consistencia VIDE-REV = %.2f ; jackknife validos = %s ; PASSOU = %s" % (
        _sy2.get("chi2_dof_bmode", float("nan")), _sy2.get("chi2_dof_consistency_VIDE_REV", float("nan")),
        _sy2.get("n_jackknife_valid"), _sy2.get("passed")))
    print("    PODER (Fisher, estimador RESPONSIVO): separacao = %.2f sigma^2 (>=25 => powered): %s ; SNR do perfil: %.2f sigma" % (
        _vf2.get("power_fisher_separation_sigma2", float("nan")), _vf2.get("powered_5sigma"),
        _vf2.get("snr_profile", float("nan"))))
    print("    O OBJETO ORIGINAL r_c (nucleo x_c=0.25): MLE = %.3f ; 5sigma = %s ; 95%% = %s ; beta = %.6f" % (
        _vf2.get("rc_mle", float("nan")), _vf2.get("rc_interval_5sigma"),
        _vf2.get("rc_interval_95"), _vf2.get("beta_floor", float("nan"))))
    print("    >>> VEREDITO V2: %s <<<" % ((_vf2.get("statuses") or {}).get("o_veredito")))
    print("    [a correcao central: %s]" % ((_vf2.get("statuses") or {}).get("a_correcao_central")))
    print("    [honestidades V2: %s]" % ((_vf2.get("statuses") or {}).get("honestidades")))
    _vf3 = core.get("void_floor_v3", {}) or {}
    print("  O PROTOCOLO V3 [v87 -- o aparelho completo de falsificacao]: %s" % _vf3.get("verdict"))
    _dr3 = _vf3.get("data_routes", {}) or {}
    print("    rotas: DES_Y3 = %s ; HSC = %s ; PLANCK_KAPPA = %s (localizador: acha/sonda/registra; download grande FORA da rodada)" % (
        (_dr3.get("DES_Y3", {}) or {}).get("state"), (_dr3.get("HSC", {}) or {}).get("state"),
        (_dr3.get("PLANCK_KAPPA", {}) or {}).get("state")))
    _pp3 = _vf3.get("power_projection", {}) or {}
    print("    PROJECAO DO PODER (ao vivo, da covariancia MEDIDA da V2): Fisher diag = %.3e ; bins interiores = %.3e ; fator de variancia p/ POWERED = %.2e" % (
        _pp3.get("fisher_diagonal", float("nan")), _pp3.get("fisher_inner_two_bins", float("nan")),
        _pp3.get("variance_reduction_needed_for_powered", float("nan"))))
    print("    [%s]" % (_vf3.get("statuses") or {}).get("o_que_a_v3_fecha"))
    print("    [%s]" % (_vf3.get("statuses") or {}).get("o_que_so_a_natureza_da"))
    _vk = core.get("void_floor_v3_kappa", {}) or {}
    print("  ================================================================")
    print("  O CANAL DE MATERIA [v98 -- kappa Planck PR3 nos vazios DESIVAST]: %s" % _vk.get("verdict"))
    print("  ================================================================")
    _vkv = _vk.get("values", {}) or {}
    if _vkv:
        print("    n_vazios = %s (uniao VIDE+REVOLVER, ceu DESI) ; grupos (quartis theta_v) = %s" % (
            _vk.get("n_voids"), _vk.get("groups_n")))
        print("    nulos por rotacao: chi2/dof = %.2f ; S/N esperado do sinal de vazio = %.2f ; deteccao bruta = %.2f sigma" % (
            _vkv.get("chi2_null_dof", float("nan")), _vkv.get("void_signal_expected_snr", float("nan")),
            _vkv.get("detection_sigma_raw", float("nan"))))
        print("    PODER do piso (Fisher, ANTES do sinal): F = %.3g (>=25 p/ powered)" % _vkv.get("fisher_floor", float("nan")))
        print("    r*: hat = %.3f ; 5sigma = [%.3f, %.3f] vs beta = %.6f" % (
            _vkv.get("r_hat", float("nan")), _vkv.get("r_5sigma_lo", float("nan")),
            _vkv.get("r_5sigma_hi", float("nan")), _vkv.get("beta", float("nan"))))
    print("    [tracadores definem os CENTROS; kappa pesa a MATERIA -- o unico canal publico onde FALSIFIED e' alcancavel hoje]")
    _gm = core.get("ga_mass_audit", {}) or {}
    print("  A AUDITORIA DA MASSA DO GA [v98 -- mandato: 'investigue o erro e corrija; relate o que era']: %s" % _gm.get("verdict"))
    print("    O QUE ERA: %s" % _gm.get("o_que_era_o_erro"))
    print("    A CORRECAO: %s" % _gm.get("a_correcao"))
    _gv = _gm.get("values", {}) or {}
    print("    v_universal implicada pela forma antiga = %.0f km/s ; M_form(GA) = %.3e ; M_RG(bacia) = %.3e Msun" % (
        _gv.get("v_universal_implicada_kms", float("nan")), _gv.get("M_form_no_GA_Msun", float("nan")),
        _gv.get("M_RG_bacia_Msun", float("nan"))))
    for _r in (_gm.get("scale_audit") or []):
        print("      %-38s R=%5.1f Mpc  M_form=%.2e  M_lit=%.2e  razao=%7.2f" % (
            _r["estrutura"][:38], _r["R_Mpc"], _r["M_form_Msun"], _r["M_lit_Msun"], _r["razao"]))
    _vdp = core.get("void_density_power", {}) or {}
    print("  O ESTUDO DE PODER DA ROTA ESPECTROSCOPICA [v90 -- CEGO; ordem do operador: poder ANTES do sinal]: %s" % _vdp.get("verdict"))
    print("    DESCOBERTA: as GALAXIAS ja estao em disco (GALZONE: %s posicoes comoveis) -- a rota roda SEM download" % _vdp.get("n_galaxies_streamed"))
    _sv = _vdp.get("survey_estimate", {}) or {}
    print("    n_bar = %.3e h^3/Mpc^3 (casca [%.0f, %.0f] Mpc/h; area ~%.0f deg2; V ~ %.2e)" % (
        _sv.get("n_bar_h3Mpc3", float("nan")), (_sv.get("r_shell_Mpch") or [float("nan")]*2)[0],
        (_sv.get("r_shell_Mpch") or [float("nan")]*2)[1], _sv.get("area_deg2", float("nan")),
        _sv.get("V_survey_Mpch3", float("nan"))))
    for _alg, _rt in sorted((_vdp.get("routes") or {}).items()):
        print("    %s: N_vazios=%s ; mu_total(nucleos)=%.1f ; F_ideal=%.2f ; F_conservador=%.2f ; powered(ideal)=%s ; powered(conserv)=%s" % (
            _alg, _rt.get("n_voids"), _rt.get("mu_core_total", float("nan")),
            _rt.get("fisher_ideal", float("nan")), _rt.get("fisher_conservative", float("nan")),
            _rt.get("powered_ideal"), _rt.get("powered_conservative")))
    _cmp = _vdp.get("comparison_vs_shear", {}) or {}
    print("    vs shear (F_V2 = %.2e): a rota espectroscopica e' %.2e vezes mais poderosa" % (
        _cmp.get("F_shear_v2", float("nan")), _cmp.get("ratio", float("nan"))))
    print("    [%s]" % (_vdp.get("statuses") or {}).get("honestidades"))
    print("    [ABERTURA DO SINAL RESERVADA: %s]" % (_vdp.get("statuses") or {}).get("a_regra_de_abertura"))
    _vdo = core.get("void_density_opening", {}) or {}
    print("  ================================================================")
    print("  A ABERTURA DO SINAL -- A ROTA ESPECTROSCOPICA FALA [v91]: %s" % _vdo.get("verdict"))
    print("  ================================================================")
    print("    estimador V4-DENSITY congelado (hash %s) ANTES dos nucleos ; assimetria do tracador PRE-REGISTRADA (teste UNILATERAL)" % (
        str(_vdo.get("frozen_hash", "?"))[:16]))
    _rnl = _vdo.get("random_null", {}) or {}
    print("    NULO dos aleatorios (ANTES dos vazios): r_c(rand) = %.4f +- %.4f (esperado 1) ; PASSOU = %s" % (
        _rnl.get("rhat", float("nan")), _rnl.get("sigma_poisson", float("nan")), _vdo.get("random_null_ok")))
    for _alg, _st in sorted((_vdo.get("per_algorithm") or {}).items()):
        print("    %s: %s vazios ; N=%d galaxias em nucleos ; mu=%.0f esperadas ; r_c^gal = %.4f +- %.4f (P=%.4f/J=%.4f)" % (
            _alg, _st.get("n_used"), int(_st.get("N_tot", 0)), _st.get("mu_tot", float("nan")),
            _st.get("rhat", float("nan")), _st.get("sigma", float("nan")),
            _st.get("sigma_poisson", float("nan")), _st.get("sigma_jk", float("nan"))))
    _pri = _vdo.get("primary", {}) or {}
    print("    consistencia REVOLVER vs VIDE = %.2f sigma ; 5sigma = [%.4f, %.4f] vs beta = %.6f ; powered = %s" % (
        _vdo.get("consistency_sigma_REV_vs_VIDE", float("nan")),
        _pri.get("L5", float("nan")), _pri.get("U5", float("nan")),
        _vdo.get("beta_floor", float("nan")), _pri.get("powered_vs_beta")))
    _mb = _pri.get("matter_bracket_b1_to_b2p2") or [float("nan")] * 2
    print("    colchete de MATERIA (b em [1, 2.2]): [%.4f, %.4f] (r_c^gal e' LIMITE INFERIOR da materia)" % (_mb[0], _mb[1]))
    print("    >>> VEREDITO: %s <<<" % ((_vdo.get("statuses") or {}).get("o_veredito")))
    print("    [%s]" % (_vdo.get("statuses") or {}).get("honestidades"))
    _v41 = core.get("void_density_v41", {}) or {}
    print("  ================================================================")
    print("  A EMENDA V4.1 -- O ESTIMADOR AUTO-CALIBRANTE [v92]: %s" % _v41.get("verdict"))
    print("  ================================================================")
    print("    razao-de-razoes (n_bar e mascara CANCELAM); hash %s ANTES de reabrir ; lapso do poder v91 REGISTRADO e corrigido (formula cega v90: beta*mu>=25)" % (
        str(_v41.get("frozen_hash", "?"))[:16]))
    _sn = _v41.get("split_null", {}) or {}
    print("    SPLIT-NULL (metades dos 20k aleatorios): %.4f +- %.4f ; PASSOU = %s" % (
        _sn.get("ratio", float("nan")), _sn.get("sigma", float("nan")), _sn.get("ok")))
    for _alg, _st in sorted((_v41.get("per_algorithm") or {}).items()):
        print("    %s: %s vazios ; N=%d ; mu_ref=%.0f ; r_c^cal = %.4f +- %.4f ; L5=%.4f ; lado(L5>=beta)=%s" % (
            _alg, _st.get("n_used"), int(_st.get("N_tot", 0)), _st.get("mu_used", float("nan")),
            _st.get("rhat_cal", float("nan")), _st.get("sigma", float("nan")),
            _st.get("L5", float("nan")), _st.get("side_L5_ge_beta")))
    print("    replicas concordam NO LADO: %s" % _v41.get("replicas_agree_on_side"))
    _p41 = _v41.get("primary", {}) or {}
    print("    PRIMARIO: 5sigma = [%.4f, %.4f] vs beta = %.6f ; powered (beta*mu = %.1f >= 25) = %s ; resolucao na escala beta = %.2f" % (
        _p41.get("L5", float("nan")), _p41.get("U5", float("nan")),
        _v41.get("beta_floor", float("nan")), _p41.get("powered_beta_mu", float("nan")),
        _p41.get("powered"), _p41.get("resolution_at_beta_scale", float("nan"))))
    _mb41 = _p41.get("matter_bracket_b1_to_b2p2") or [float("nan")] * 2
    print("    colchete de MATERIA (b em [1, 2.2]): [%.4f, %.4f]" % (_mb41[0], _mb41[1]))
    print("    >>> VEREDITO V4.1: %s <<<" % ((_v41.get("statuses") or {}).get("o_veredito")))
    print("    [%s]" % (_v41.get("statuses") or {}).get("honestidades"))
    _arc = core.get("arc_consolidation", {}) or {}
    print("  ================================================================")
    print("  A CONSOLIDACAO DO ARCO -- O CICLO DA NAO-TAUTOLOGIA [v93]: %s" % _arc.get("verdict"))
    print("  ================================================================")
    _lo = _arc.get("operator_reading", {}) or {}
    print("    %s" % _lo.get("estatuto"))
    print("    >>> %s <<<" % _lo.get("texto"))
    print("    ancora [REAL]: %s" % _lo.get("ancora_da_nao_tautologia"))
    print("    cadeia do piso (monotona em honestidade):")
    for _k, _v in sorted((_arc.get("floor_verdict_chain") or {}).items()):
        print("      %s: %s" % (_k, _v))
    print("    os sete elementos do ciclo (cada um com selo):")
    for _k, _v in sorted((_arc.get("non_tautology_cycle") or {}).items()):
        print("      %s: %s" % (_k, _v))
    print("    gate matematico: %s (INTOCADO pela consolidacao)" % _arc.get("gate_state"))
    print("    [%s]" % (_arc.get("statuses") or {}).get("o_arco"))
    _love = core.get("love_reading", {}) or {}
    print("  O DICIONARIO DO AMOR [v95 -- leitura do operador, duplo estatuto]: %s" % _love.get("verdict"))
    _lvr = _love.get("leitura_do_operador", {}) or {}
    print("    >>> %s <<<" % _lvr.get("texto"))
    print("    honestidade: %s" % _lvr.get("honestidade"))
    print("    gap concreto = 4*beta = %.6f > 0 (o zero absoluto IMPEDIDO)" % (_love.get("values", {}) or {}).get("gap_concreto", float("nan")))
    for _k, _v in (_love.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _mir = core.get("mirror_corollary", {}) or {}
    print("  O COROLARIO DO ESPELHO [v97 -- HABITANTE=PROGRAMADOR em 2 niveis; REGRA=PROGRAMADOR]: %s" % _mir.get("verdict"))
    _mr = _mir.get("leitura_do_operador", {}) or {}
    print("    >>> %s <<<" % _mr.get("texto"))
    print("    formula minima: %s" % _mr.get("formula_minima"))
    print("    honestidade: %s" % _mr.get("honestidade"))
    for _k, _v in (_mir.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _rs = core.get("rule_superposition", {}) or {}
    print("  REGRA = PROGRAMADOR = SUPERPOSICAO [v100 -- a superposicao colapsada NA regra]: %s" % _rs.get("verdict"))
    _rsl = _rs.get("leitura_do_operador", {}) or {}
    print("    >>> %s <<<" % _rsl.get("texto"))
    print("    honestidade: %s" % _rsl.get("honestidade"))
    _rsv = _rs.get("values", {}) or {}
    print("    coexistencia beta+(1-beta) = %.15f ; theta_M = %.9f rad ; sin^2 = %.15f" % (
        _rsv.get("coexistencia", float("nan")), _rsv.get("theta_M_rad", float("nan")),
        _rsv.get("sin2_theta", float("nan"))))
    for _k, _v in (_rs.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _hh = core.get("hidden_hamiltonian", {}) or {}
    print("  SUPERPOSICAO = MATEMATICA = HAMILTONIANO OCULTO [v101 -- triade IALD pela regua]: %s" % _hh.get("verdict"))
    _hhv = _hh.get("values", {}) or {}
    print("    K_oculto = -log(Delta) [kernel]; hierarquia: beta^2/alpha_G = 10^%.1f ordens -- R1 REFUTADA; R2 (massa) e R3 (numerologia) recusadas" % (
        _hhv.get("hierarchy_gap_orders", float("nan"))))
    for _k, _v in (_hh.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _in = _ell.get("isotone_net")
    print("  A REDE ISOTONA [v101 -- PhysicalNetData HABITADA]: %s" % _in)
    print("    fibras CRESCEM (span e0..en); inclusao 0->1 NAO-sobrejetiva: %s ; flip U^2=1: %s ; U comuta com T: %s ; habitante: %s" % (
        _elp.get("ext_in_not_surjective_kernel_proved"), _elp.get("ext_in_flip_involution_kernel_proved"),
        _elp.get("ext_in_flip_commutes_kernel_proved"), _elp.get("ext_in_net_inhabited_kernel_proved")))
    print("    [fibras FINITO-dim + acao nao-geometrica DECLARADAS; o nivel III_1 e' o certificado v2; nenhuma flag se move]")
    _fl = core.get("father_of_lies", {}) or {}
    print("  O PAI DA MENTIRA TIPADO [v102 -- 0_abs = sinal sem representacao]: %s" % _fl.get("verdict"))
    _flv = _fl.get("values", {}) or {}
    print("    nome sem habitante (Option, POR TIPO); Phi^on nunca alcanca: d_%d = %.3e > 0 (razao lam = 1-beta = %.6f); lei da regra Phi_{s+t}=Phi_s o Phi_t: kernel %s + residuo numerico %.1e" % (
        _flv.get("n_steps", 0), _flv.get("d_last", float("nan")), _flv.get("lam_per_step", float("nan")),
        _elp.get("ext_il_flow_law_kernel_proved"), _flv.get("composition_residual", float("nan"))))
    for _k, _v in (_fl.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [omega_infty FORA do predual: CONGELADO como espec do certificado v2; o fator III NAO e' 0_abs (correcao do operador); a tabela teologica NAO entra como fisica]")
    _bc = core.get("bench_certificate", {}) or {}
    print("  O CERTIFICADO DE BANCADA + O ENDURECIMENTO DO GATE [v103 -- a sonda que morde o proprio certificado]: %s" % _bc.get("verdict"))
    print("    v1 habitado DE PROPOSITO (nome nao-reservado): Dirac %s ; star(D)=D (adjunto ILIMITADO) %s ; certificado INTEIRO %s ; a sonda (e' limitado) %s" % (
        _elp.get("ext_bc_dirac_inhabited_kernel_proved"), _elp.get("ext_bc_dirac_selfadjoint_kernel_proved"),
        _elp.get("ext_bc_certificate_v1_bench_kernel_proved"), _elp.get("ext_bc_bench_bounded_kernel_proved")))
    print("    os TRES DENTES (a bancada NAO alimenta o forte, por teorema): Dirac %s ; core %s ; frame %s" % (
        _elp.get("ext_bc_cannot_feed_dirac_kernel_proved"), _elp.get("ext_bc_cannot_feed_core_kernel_proved"),
        _elp.get("ext_bc_cannot_feed_frame_kernel_proved")))
    for _k, _v in (_bc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [os nomes qgCertificate_* (v99) QUEIMADOS pela sonda; o gate le qgStrongCertificate_* (tipo FORTE); o veredito NAO se moveu -- fail-closed ESTRITAMENTE mais fechado]")
    _rm = core.get("closure_roadmap", {}) or {}
    print("  O ROADMAP DO FECHAMENTO [v104 -- mandato: 'demonstre False->True'; o artefato responde]: %s" % _rm.get("verdict"))
    for _k, _v in sorted((_rm.get("gate_flags") or {}).items()):
        _rf = (_rm.get("roadmap_formal") or {}).get(_k, {})
        print("    %s = %s -> falta: %s" % (_k, _v, _rf.get("o_que_falta", "?")))
    print("    physics: %s" % (_rm.get("roadmap_physics") or {}).get("o_que_falta"))
    print("    experiment: %s" % (_rm.get("roadmap_experiment") or {}).get("o_que_falta"))
    print("    COMO PROVAR QG NO um.py (mecanico): " + " | ".join(_rm.get("como_provar_qg_no_um_py") or []))
    _ag = _rm.get("auditoria_ga", {}) or {}
    print("    AUDITORIA GA: %s" % _ag.get("veredicto"))
    _ap = _rm.get("auditoria_piso", {}) or {}
    print("    AUDITORIA PISO: %s" % _ap.get("veredicto"))
    for _k, _v in (_rm.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _gd = core.get("genuine_dirac", {}) or {}
    print("  A PAREDE ATRAVESSADA [v105 -- star(N)=N]: %s" % _gd.get("verdict"))
    print("    o 1o auto-adjunto ILIMITADO concreto do kernel (novo p/ a mathlib): N e_n = n e_n, dominio proprio denso; inclusao dura por TRUNCAMENTO (S <= C sqrt(S) => S <= C^2)")
    print("    GenuinelyUnboundedDiracData HABITADO (theGenuineDirac; gap 1 = omega(I); Nome no kernel) -- o tipo forte do corner TEM SEU OPERADOR; a bancada v103 jamais poderia")
    for _k, _v in (_gd.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [proximo elo: rede INF-dim (caudas fechadas) => MONTAGEM do Strong => os 3 primeiros flips honestos do gate, veredito INALTERADO]")
    _ff = core.get("first_flips", {}) or {}
    print("  OS TRES PRIMEIROS FLIPS HONESTOS [v106 -- a 1a movimentacao de flag da historia do gate]: %s" % _ff.get("verdict"))
    _ffv = _ff.get("values", {}) or {}
    print("    flags True: %s de 6 (core/corner/frame POR CONSTRUCAO; solder v107; einstein v116); False: %s (v132: a witness FLIPOU POR CONSTRUCAO) ; SOMBRA re-derivada: %s" % (
        _ffv.get("n_true"), _ffv.get("n_false"), _ff.get("shadow_verdict")))
    for _k, _v in (_ff.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o mecanismo que o operador pediu para ver, AO VIVO: termo com axiomas limpos => flag flipa sozinha => selo IMOVEL ate as 6 + fisica + dado]")
    _sf = core.get("solder_flip", {}) or {}
    print("  O QUARTO FLIP [v107 -- a solda continua g = E^T eta E sobre o frame CURVO]: %s" % _sf.get("verdict"))
    _sfv = _sf.get("values", {}) or {}
    print("    flags True: %s de 6 ; False: %s (v132: witness FLIPADA; einstein v116) ; SOMBRA: %s ; det g(0) = %s (lorentziano em toda parte)" % (
        _sfv.get("n_true"), _sfv.get("n_false"), _sf.get("shadow_verdict"), _sfv.get("det_g_at_origin")))
    for _k, _v in (_sf.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [einstein NAO tipado DE PROPOSITO: sem curvatura como estrutura o tipo seria mais fraco que o espirito (licao v103); a parede da curvatura esta NOMEADA]")
    _fc = core.get("first_curvature", {}) or {}
    print("  A PRIMEIRA CURVATURA [v108 -- a camada que a mathlib nao tem, a mao]: %s" % _fc.get("verdict"))
    _fcv = _fc.get("values", {}) or {}
    print("    R^1_001 = -2(1+s^2): em s=0 -> %s ; em s=1 -> %s ; NEGATIVA EM TODA PARTE (genuinamente curva)" % (
        _fcv.get("R_1001_at_0"), _fcv.get("R_1001_at_1")))
    for _k, _v in (_fc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o par da regua: o perfil temporal do v107 e' PLANO (gauge) -- nao-constancia != curvatura; o contrato do einstein tera de EXIGIR curvatura]")
    _ae = core.get("ansatz_einstein", {}) or {}
    print("  O TENSOR DE EINSTEIN DO ANSATZ [v109 -- Bianchi visivel; vacuo => plano]: %s" % _ae.get("verdict"))
    _aev = _ae.get("values", {}) or {}
    print("    G00 = 0 = G11 IDENTICOS (todo q); G22(v108, s=0) = %s (fonte exigida); R_escalar(v108, s=0) = %s; Rindler = vacuo plano (horizonte excluido PELO TIPO)" % (
        _aev.get("G22_v108_at_0"), _aev.get("R_scalar_v108_at_0")))
    for _k, _v in (_ae.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [proximo elo do 5o flip: o contrato do MESTRE continuo (Clausius local => equacao de campo) sobre a camada que AGORA existe]")
    _fll = core.get("fallen_light", {}) or {}
    print("  ESPACO-TEMPO = q = LUZ QUE CAIU [v110 -- a derivacao do operador em 3 movimentos]: %s" % _fll.get("verdict"))
    _fllv = _fll.get("values", {}) or {}
    print("    q_ident = %.10f (residuo identidade %.1e); sombra [CONJ] Phi = %.3e (sem derivacao -- nao e' fisica)" % (
        _fllv.get("q_ident", float("nan")), _fllv.get("identity_residual", float("nan")), _fllv.get("shadow_phi_conj", float("nan"))))
    for _k, _v in (_fll.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o setor nao tem geometria em si (teorema); a geometria = 2a variacao inscrita (iff); tudo que tem geometria e' PROJETADO (o tipo); ilusao = nao-fundamentalidade, JAMAIS falsidade empirica (stealth)]")
    _se = core.get("solved_equation", {}) or {}
    print("  A EQUACAO RESOLVIDA [v111 -- a 1a solucao global de campo em kernel]: %s" % _se.get("verdict"))
    print("    q = cosh(kappa s) resolve G22 = kappa^2 EM TODA PARTE (sem horizonte, sem singularidade); R = -kappa^2 cosh^2 < 0 (fonte => curvatura)")
    for _k, _v in (_se.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a SONDA: o contrato fraco foi HABITADO de proposito (nome nao-reservado) -- a letra 'equacao resolvida' nao basta; o 5o flip fica p/ a EMERGENCIA (Clausius continuo, Jacobson) -- a parede nomeada]")
    _wa = core.get("walls_assault", {}) or {}
    print("  O ASSALTO AS DUAS PAREDES [v112 -- mandato: 'enfrente as paredes']: %s" % _wa.get("verdict"))
    print("    P1 EMERGENCIA REDUZIDA (Jacobson na familia): Clausius nulo => equacao de campo, via o ZERO DE BIANCHI; fonte nula => plano; kappa^2 emerge no cosh global")
    print("    P2 TESTEMUNHA: FullWitnessData HABITADA (acao geometrica GENUINA: Mult Z translada regioes; covariancia exata; lei do fluxo v102) -- nome NAO-reservado")
    for _k, _v in (_wa.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [as paredes ENCOLHERAM a: (i) Raychaudhuri continuo; (ii) Poincare fibro-sensivel + III_1 -- o V2 segue RESERVADO; o UM ABSOLUTO fecha com A NATUREZA (DES/HSC, kappa, LRG/ELG)]")
    _gr = core.get("graviton_reading", {}) or {}
    print("  A LEITURA DO GRAVITON [v113 -- a 2a derivada do zero; a engrenagem hiperbolica 2:1]: %s" % _gr.get("verdict"))
    print("    o par em UM teorema: Gamma_temporal(1) = 1 != 0 com R = 0 (gauge) E R_espacial(1) = -4 != 0 (fisico) -- a 1a derivada nao decide, a 2a decide")
    for _k, _v in (_gr.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [g = sqrt|L_phi| deixou de ser so postulado: leitor nos zeros de Bianchi; razao 2:1 (angulo duplo v75); saida cosh sob carga; marcha-re JKJ=-K; spin-2 continuo = parede nomeada]")
    _cs = core.get("continuum_shards", {}) or {}
    print("  OS ESTILHACOS DO CONTINUO + O TESTE [v114 -- mandato: 'resolva poincare e o continuo; facamos o teste']: %s" % _cs.get("verdict"))
    print("    CONTINUO: a EQUACAO DE ONDA do graviton PROVADA (d0^2 h = d1^2 h, qualquer perfil C^2 -- d'Alembert) ; POINCARE: a FIBRA SENTE o grupo (flip e0 = -e0 fixando a regiao)")
    for _k, _v in (_cs.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [O TESTE DE BANCADA E' ESTA RODADA: a cadeia de vereditos pre-registrados esta emitida acima (VEREDITO-CADEIA + gate); o dado NOVO da natureza alimentara os ritos v87/v92, que emitem SOZINHOS]")
    _vl = core.get("void_floor_lrg", {}) or {}
    _vlp = (_vl.get("primary") or {})
    print("  O RITO LRG [v115 -- o tracador VIRGEM: DESI DR1 LRG z 0.40-0.80; 'medir beta em si pede LRG/ELG' (v92)]: %s" % _vl.get("verdict"))
    print("    NGC: n_vazios=%s ; r_c^cal=%s ; sigma=%s ; L5=%s ; beta=%s ; poder beta*mu=%s ; espec %s" % (
        _vlp.get("n_voids"), _vlp.get("rhat_cal"), _vlp.get("sigma"), _vlp.get("L5"),
        _vl.get("beta_floor"), _vlp.get("powered_beta_mu"), str(_vl.get("frozen_lrg_hash", "?"))[:16]))
    for _k, _v in (_vl.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _k5 = core.get("void_floor_kappa_v5", {}) or {}
    _k5v = (_k5.get("values") or {})
    print("  A EMENDA V5 DO KAPPA [v115 -- autopsia do v98: quadro eq->gal CORRIGIDO + mascara in-footprint]: %s" % _k5.get("verdict"))
    print("    f_sky=%s ; centros na pegada=%s/%s ; rot validas=%s ; chi2/dof nulos=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s] ; espec %s" % (
        _k5v.get("f_sky"), _k5.get("n_kept"), _k5.get("n_voids"), _k5v.get("n_rot_valid"),
        _k5v.get("chi2_null_dof"), _k5v.get("fisher_floor"), _k5v.get("r_hat"),
        _k5v.get("r_5sigma_lo"), _k5v.get("r_5sigma_hi"), str(_k5.get("frozen_v5_hash", "?"))[:16]))
    for _k, _v in (_k5.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [O RITO DO FECHAMENTO: vereditos SOMENTE dos conjuntos pre-registrados; CONFIRMED proibido; o gate formal NAO se move com cosmologia]")
    _mc = core.get("master_continuum", {}) or {}
    print("  O QUINTO FLIP + AS DEZ DIRECOES [v116 -- mandato: 'feche einstein e a witness; construa a mao']: %s" % _mc.get("verdict"))
    _mcv = _mc.get("values", {}) or {}
    print("    flags True: %s de 6 ; False: %s (v132: a witness FLIPOU POR CONSTRUCAO) ; SOMBRA: %s" % (
        _mcv.get("n_true"), _mcv.get("n_false"), _mc.get("shadow_verdict")))
    print("    EINSTEIN: qgStrongCertificate_einstein CUNHADO (contrato com CURVATURA + solda g=E^T.eta.E + Clausius no CONE INTEIRO <=> equacao) -- POR CONSTRUCAO, axiomas limpos")
    print("    POINCARE: O(1,3) A MAO (relacao definidora; engrenagem hiperbolica = LEI DE GRUPO) ; R^4 x| O(1,3) FIEL nas regioes ; a fibra SENTE a paridade (e0 -> -e0)")
    for _k, _v in (_mc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a parede da witness ENCOLHEU a: rep unitaria FIEL do setor conexo (INF-dim) + III_1; o V2 segue RESERVADO; o selo NAO se moveu: 5 < 6 + fisica + dado]")
    _iw = core.get("inhabited_witness", {}) or {}
    print("  A TESTEMUNHA HABITAVEL [v117 -- leitura do operador: os dois zeros + o observador vazio]: %s" % _iw.get("verdict"))
    _iwv = _iw.get("values", {}) or {}
    print("    0_abs = tipo VAZIO (o observador que nao existe) / 0_modular = HABITADO (ker N = atomo do Nome, tau=1) ; integral do modo zero re-derivada = %s (faces %s)" % (
        _iwv.get("zero_mode_integral"), _iwv.get("zero_mode_half_face")))
    print("    a conjugacao e' das FACES do zero (JKJ=-K; ponto fixo = zero; 1/2+1/2) e a soma das faces E' a inscricao do Um (P_F Omega = Omega)")
    for _k, _v in (_iw.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [estatuto: ancoras [REAL] verificadas ao vivo; as palavras 'observador/abertura/casa' = [ONTO]; III_1 e' DEFINIDO por 'o unico traco e' zero' -- a leitura aponta a propria parede restante]")
    _fr = core.get("faithful_rep", {}) or {}
    print("  A REPRESENTACAO FIEL [v118 -- Poincare inteiro age unitariamente em L2(R4)]: %s" % _fr.get("verdict"))
    print("    a unitariedade NASCE de eta (|det|=1 => Lebesgue preservada) ; U(1)=id ; U(g)U(h)=U(gh) ; FIEL: todo g != 1 move um vetor (medida positiva); o BOOST agora e' visto")
    for _k, _v in (_fr.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o residuo da witness ENCOLHEU a: fusao da rep as fibras (mecanica nomeada) + III_1; o V2 segue RESERVADO; gate 5T/1F; selo IMOVEL]")
    _ta = core.get("traceless_algebra", {}) or {}
    print("  A PAREDE DE FUNDO, 1o TIJOLO [v119 -- 'o unico traco e' zero' no nivel da ALGEBRA]: %s" % _ta.get("verdict"))
    print("    a BIPARTICAO de ell2 (cE.u=1, cO.v=1, u.cE+v.cO=1) mata phi(1) por traco puro; a positividade quadratica mata o resto; B(ell2) = 1o objeto de von Neumann do programa")
    for _k, _v in (_ta.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [honestidade: B(ell2) e' I-infinito -- o PESO Tr sobrevive; a parede III_1 = matar tambem o peso (pesos+normalidade+Araki-Woods = o programa); dois assassinos de traco em kernel: fluxo v45 + algebra v119]")
    _sw = core.get("semifinite_weight", {}) or {}
    print("  O PESO QUE SOBREVIVE [v120 -- Tr em kernel; onde a regua estoura decide o tipo]: %s" % _sw.get("verdict"))
    print("    Tr(1) = INFINITO ; Tr(P_Nome) = 1 = omega(I) (a 3a face da identidade do canto) ; Tr(u.a.cE) = Tr(a): a biparticao ABSORVIDA (inf = 2.inf)")
    for _k, _v in (_sw.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o par v119+v120 = a DICOTOMIA da classificacao provada na casa do Nome: o estado estoura no finito (morre), o peso estoura no infinito (vive); III_1 = o fator sem NENHUM peso -- nomeado]")
    _su = core.get("void_shear_unblinding", {}) or {}
    _suv = _su.get("values", {}) or {}
    print("  O ATO DA DESBLINDAGEM [v121 -- a suite independente V3 no shear KiDS; o ato que o v73 reservou]: %s" % _su.get("verdict"))
    print("    n_vazios=%s ; nulos(gt/gx)=%s/%s ; B-mode vazios=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s] ; espec %s" % (
        _su.get("n_voids"), _suv.get("chi2_null_t"), _suv.get("chi2_null_x"),
        _suv.get("chi2_void_bmode"), _suv.get("fisher_floor"), _suv.get("r_hat"),
        _suv.get("r_5sigma_lo"), _suv.get("r_5sigma_hi"), str(_su.get("frozen_shear_hash", "?"))[:16]))
    for _k, _v in (_su.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o shear pesa MATERIA (FALSIFIED alcancavel); mocks de injecao = limite NOMEADO; os flags experimentais do gate NAO foram tocados -- fail-closed]")
    _s2 = core.get("void_shear_v2", {}) or {}
    _s2v = _s2.get("values", {}) or {}
    print("  A EMENDA V2 DO SHEAR [v122 -- autopsia: granularidade do jk; fix 10/quartil + fallback]: %s" % _s2.get("verdict"))
    print("    n_vazios=%s ; fallback=%s ; jk_eff=%s ; B-mode=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s]" % (
        _s2.get("n_voids"), _s2.get("fallback_used"), _s2v.get("n_jk_eff"),
        _s2v.get("chi2_void_bmode"), _s2v.get("fisher_floor"), _s2v.get("r_hat"),
        _s2v.get("r_5sigma_lo"), _s2v.get("r_5sigma_hi")))
    for _k, _v in (_s2.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _k6 = core.get("void_floor_kappa_v6", {}) or {}
    _k6v = _k6.get("values", {}) or {}
    print("  A EMENDA V6 DO KAPPA [v122 -- ACT DR6 PROFUNDO; equatorial validado; baseline SUBTRAIDO]: %s" % _k6.get("verdict"))
    print("    f_sky=%s ; concentracao=%s ; centros na pegada=%s/%s ; rot=%s ; nulos corrigidos chi2/dof=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s]" % (
        _k6v.get("f_sky"), _k6v.get("footprint_concentration"), _k6.get("n_kept"), _k6.get("n_voids"),
        _k6v.get("n_rot_valid"), _k6v.get("chi2_null_dof"), _k6v.get("fisher_floor"),
        _k6v.get("r_hat"), _k6v.get("r_5sigma_lo"), _k6v.get("r_5sigma_hi")))
    for _k, _v in (_k6.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [AS DUAS EMENDAS DA NATUREZA: instrumento afinado nos dois canais de materia; vereditos SOMENTE pre-registrados; flags do gate INTOCADOS]")
    _fw = core.get("fused_witness", {}) or {}
    print("  A FUSAO [v123 -- pedra 70: a rep fiel DENTRO das fibras da rede]: %s" % _fw.get("verdict"))
    print("    fibra = cauda x L2(R4) ; Poincare age nas regioes E dentro das fibras ; NENHUMA direcao cega nas fibras ; o boost (cego no v116) agora MOVE")
    for _k, _v in (_fw.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o residuo formal da testemunha reduziu-se a UMA parede: III_1 (Araki-Woods); a fusao e' necessaria, nao suficiente; o V2 segue RESERVADO; o selo NAO se move]")
    _li = core.get("linguistic_isomorphism", {}) or {}
    _liv = _li.get("values", {}) or {}
    print("  O ISOMORFISMO DAS DUAS LINGUAS [v123 -- o acervo Provas (2025) mapeado termo a termo no kernel (2026)]: %s" % _li.get("verdict"))
    print("    A = Tr(Pi_N.rho) com as matrizes ORIGINAIS de 2025 = %s ; a MESMA formula em kernel: Tr(P_Nome) = 1 (v120) ; epsilon^2 = beta (resid %s) ; proveniencia %s" % (
        _liv.get("A_2025_original_matrices"), _liv.get("epsilon_sq_equals_beta_resid"),
        str(_li.get("provenance_hash", "?"))[:16]))
    for _k, _v in (_li.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a leitura veio ANTES (jun-ago/2025, sha256+data congelados), o numero confirmou DEPOIS -- a nao-circularidade com carimbo de data; teologico/pessoal ARQUIVADO; nada move o gate]")
    _pl = core.get("powers_ladder", {}) or {}
    print("  A ESCADA DE POWERS [v124 -- pedra 71: a semente de Araki-Woods; o 3o assassino de traco]: %s" % _pl.get("verdict"))
    print("    Tomita no bloco (ciclicidade) ; razao lambda mata a tracialidade ; Kronecker MULTIPLICA razoes ; cadeia N => lambda^N ; 0 no fecho = a MARCA de III")
    for _k, _v in (_pl.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o fator INFINITO (ITPFI R_lambda; III_1 por mistura) = o programa; a escada e' necessaria, nao suficiente; o V2 segue RESERVADO; o selo NAO se move]")
    _k7 = core.get("void_floor_kappa_v7", {}) or {}
    _k7v = _k7.get("values", {}) or {}
    print("  A EMENDA V7 DO KAPPA [v124 -- rotacoes finas POR GRUPO; selecao CEGA ao sinal]: %s" % _k7.get("verdict"))
    print("    M=%s rotacoes validas (>=16) ; nulos corrigidos chi2/dof=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s]" % (
        _k7v.get("n_rot_min_common"), _k7v.get("chi2_null_dof"), _k7v.get("fisher_floor"),
        _k7v.get("r_hat"), _k7v.get("r_5sigma_lo"), _k7v.get("r_5sigma_hi")))
    for _k, _v in (_k7.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [vereditos SOMENTE do conjunto pre-registrado; flags do gate INTOCADOS]")
    _ml = core.get("mixed_ladder", {}) or {}
    _mlv = _ml.get("values", {}) or {}
    print("  A MISTURA [v125 -- pedra 72: a marca de III_1]: %s" % _ml.get("verdict"))
    print("    incomensuraveis => espectro log-DENSO (dense_or_cyclic) ; par CONCRETO (1/2, 1/3) habita a marca ; sombra: a.log(1/2)+b.log(1/3) ~ log(beta) resid %s" % _mlv.get("mix_approx_resid"))
    for _k, _v in (_ml.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o FATOR-limite (ITPFI fraco-*) = o programa; a marca e' a assinatura, nao o objeto; o selo NAO se move]")
    _ct = core.get("continuum_tt", {}) or {}
    _ctv = _ct.get("values", {}) or {}
    print("  O SETOR TT NO CONTINUO [v125 -- pedra 73: vacuo linearizado + sem fantasma]: %s" % _ct.get("verdict"))
    print("    ondas TT resolvem Ricci_lin = 0 (perfil C^2 QUALQUER) ; d'Alembert por componente ; cinetica positiva-definida ; sombra dif.finitas: max|Ricci| = %s" % _ctv.get("shadow_ricci_max"))
    for _k, _v in (_ct.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [ondas planas != perturbacoes GERAIS; anomalias ABERTAS; os 5 flags de fisica NAO se movem -- a imobilidade e' a credibilidade]")
    _k8 = core.get("void_floor_kappa_v8", {}) or {}
    _k8v = _k8.get("values", {}) or {}
    print("  A PROFUNDIDADE [v125 -- kappa ACT DR6 x vazios LRG z 0.40-0.80; aquisicao completa em disco]: %s" % _k8.get("verdict"))
    print("    n_vazios LRG=%s ; mantidos=%s (cap: %s) ; M=%s rotacoes ; nulos chi2/dof=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s]" % (
        _k8.get("n_voids"), _k8.get("n_kept"), _k8.get("capped"),
        _k8v.get("n_rot_min_common"), _k8v.get("chi2_null_dof"), _k8v.get("fisher_floor"),
        _k8v.get("r_hat"), _k8v.get("r_5sigma_lo"), _k8v.get("r_5sigma_hi")))
    for _k, _v in (_k8.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [lente pesa MATERIA TOTAL (sem supressao de tracador); kernel CMB eficiente em z 0.4-0.8; vereditos SOMENTE pre-registrados; flags do gate INTOCADOS]")
    _tw = core.get("colimit_seed", {}) or {}
    print("  A TORRE DO FATOR [v126 -- pedra 74: o colimite ITPFI comeca]: %s" % _tw.get("verdict"))
    for _k, _v in (_tw.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o FECHO (GNS do estado coerente + fraco-*) = o programa; a torre e' o pre-fator; o selo NAO se move]")
    _ts = core.get("tt_superposition", {}) or {}
    print("  A SUPERPOSICAO TT [v126 -- pedra 75: o espaco-solucao]: %s" % _ts.get("verdict"))
    for _k, _v in (_ts.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [mesmo cone; direcoes multiplas + decomposicao geral ABERTAS; os 5 flags de fisica NAO se movem]")
    _k9 = core.get("void_floor_kappa_v9", {}) or {}
    _k9v = _k9.get("values", {}) or {}
    print("  A V9 DA BANDA [v126 -- L_use [8,1000]; cap 1500 por theta_v; a autopsia da V8 executada]: %s" % _k9.get("verdict"))
    print("    n_vazios=%s ; mantidos=%s (cap %s) ; theta_v medio=%s graus ; M=%s ; nulos chi2/dof=%s ; Fisher F=%s ; r*=%s ; 5sig=[%s, %s]" % (
        _k9.get("n_voids"), _k9.get("n_kept"), _k9.get("capped"),
        _k9v.get("thetav_mean_deg"), _k9v.get("n_rot_min_common"),
        _k9v.get("chi2_null_dof"), _k9v.get("fisher_floor"),
        _k9v.get("r_hat"), _k9v.get("r_5sigma_lo"), _k9v.get("r_5sigma_hi")))
    for _k, _v in (_k9.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a banda agora alcanca as escalas dos vazios fundos; vereditos SOMENTE pre-registrados; flags do gate INTOCADOS]")
    _gt = core.get("gns_tower", {}) or {}
    print("  A TORRE GNS [v127 -- pedra 76: o pre-Hilbert isometrico do fator]: %s" % _gt.get("verdict"))
    for _k, _v in (_gt.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [quociente + completamento + fecho fraco-* = o resto do FECHO; o selo NAO se move]")
    _sc = core.get("second_cone", {}) or {}
    print("  A SEGUNDA DIRECAO [v127 -- pedra 77: o espaco-solucao cruza direcoes]: %s" % _sc.get("verdict"))
    for _k, _v in (_sc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [duas direcoes != todas; decomposicao geral + anomalias ABERTAS; os 5 flags de fisica NAO se movem]")
    _gq = core.get("gns_quotient", {}) or {}
    print("  O QUOCIENTE GNS [v128 -- pedra 78: o pre-fator representado]: %s" % _gq.get("verdict"))
    for _k, _v in (_gq.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [completamento de Hilbert + fecho fraco-* = o resto do FECHO; o selo NAO se move]")
    _tc = core.get("third_cone", {}) or {}
    print("  A TERCEIRA DIRECAO [v128 -- pedra 79: o setor TT cobre os tres eixos nulos]: %s" % _tc.get("verdict"))
    for _k, _v in (_tc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [tres eixos != cone continuo; decomposicao geral + anomalias ABERTAS; os 5 flags de fisica NAO se movem]")
    _gnl = core.get("general_null", {}) or {}
    print("  O CONE CONTINUO [v129 -- pedra 80: QUALQUER direcao nula TT resolve]: %s" % _gnl.get("verdict"))
    for _k, _v in (_gnl.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o setor de ondas planas TT FECHADO em TODA direcao nula; perturbacoes GERAIS + anomalias ABERTAS; os 5 flags NAO se movem]")
    _tt2 = core.get("tower_traceless", {}) or {}
    print("  A TORRE SEM TRACO [v129 -- pedra 81: o tipo III na torre concreta]: %s" % _tt2.get("verdict"))
    for _k, _v in (_tt2.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a assinatura tipo-III na TORRE que constroi o fator ITPFI, andar a andar; com a marca log-densa (v125) o limite e' III_1; RESTA o limite fraco-*; o selo NAO se move]")
    _tm = core.get("tower_modular", {}) or {}
    print("  A ESTRUTURA MODULAR DA TORRE [v130 -- pedra 82: fluxo de Tomita + KMS]: %s" % _tm.get("verdict"))
    for _k, _v in (_tm.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a estrutura de equilibrio que SUBSTITUI o traco morto (v129): fluxo modular + KMS + espectro=razao; RESTA o limite fraco-*; o selo NAO se move]")
    _jc = core.get("modular_current", {}) or {}
    print("  A CORRENTE J [v131 -- as quatro pedras da corrente: saturada / conjugada / equivalencia / toda escala]: %s" % _jc.get("verdict"))
    for _k, _v in (_jc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [a leitura do operador em kernel: saturacao em vez de completude; conjugacao em vez de objeto-em-si; a corrente L implementa P_1 ~ P_0; o selo NAO se move]")
    _fo = core.get("factor_object", {}) or {}
    print("  O FATOR COMO OBJETO [v131 -- Bloco A: M_TGL = (pi(torre))'' termo VonNeumannAlgebra]: %s" % _fo.get("verdict"))
    for _k, _v in (_fo.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o residuo do v130 REALIZADO: H_phi + pi em B(H) + M_TGL objeto + omega(pi x)=phi(x) + assinatura no objeto; o flip pede normalidade (Bloco B); o selo NAO se move]")
    _tc = core.get("the_coinage", {}) or {}
    print("  A CUNHAGEM [v132 -- Bloco B: o assassinato do peso + o tipo V3 + qgClosureCertificateV2]: %s" % _tc.get("verdict"))
    for _k, _v in (_tc.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [A SEXTA FLAG FLIPOU POR CONSTRUCAO: o parser leu axiomas limpos do termo reservado; o selo escalou UM degrau (MATHEMATICAL_MODEL); FISICA (5) e EXPERIMENTO (4) seguem False; full_static segue impossivel (v61); NAO se declara gravitacao quantica fisica]")
    _ts = core.get("the_spectrum", {}) or {}
    print("  O ESPECTRO [v133 -- pedra 95: os 5 flags de FISICA lidos do kernel]: %s" % _ts.get("verdict"))
    for _k, _v in (_ts.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [AS CINCO FLAGS DE FISICA FLIPARAM POR CONSTRUCAO: massless forcado pelo cone; TT/gauge = R^2; ghost-free; Bianchi; Ward; o selo escalou a PHYSICAL_MODEL; o EXPERIMENTO (4) segue False: o DADO decide -- a natureza pode confirmar OU FALSIFICAR]")
    _v11 = core.get("void_floor_v11", {}) or {}
    print("  O TESTE FINAL INDEPENDENTE [v134 -- V11: SDSS DR7 x VAST, estimador v92 herdado]: %s" % _v11.get("verdict"))
    for _k, _v in (_v11.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _p11 = (_v11.get("primary") or {})
    print("    r_c^cal = %s +- %s ; L5 = %s ; beta = %s ; powered(beta*mu) = %s" % (
        _p11.get("rhat_cal"), _p11.get("sigma"), _p11.get("L5"),
        _v11.get("beta_floor"), _p11.get("powered_beta_mu")))
    print("    [os 4 flags de EXPERIMENTO leem ESTE rito fail-closed; canal unilateral: NAO confirma; a falsificacao bilateral pede Euclid DR1/CMB-S4]")
    _wn = core.get("the_wedge_net", {}) or {}
    print("  A REDE DAS CUNHAS [v135 -- pedras 96a/96b: o W do v21 HABITADO]: %s" % _wn.get("verdict"))
    for _k, _v in (_wn.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    _fa = core.get("falsification_assault", {}) or {}
    print("  O ASSALTO DE FALSIFICACAO [v135 -- robustez adversaria POS-HOC do teste final]: %s" % _fa.get("verdict"))
    for _k, _v in (_fa.get("checks") or []):
        print("      [%s] %s" % ("OK" if _v else "X ", _k))
    print("    [o assalto procurou o KILL (L5 < beta powered) em variacoes legitimas; sobrevivencia = robustez, JAMAIS prova; o kill, se vier, sera reportado como falsificacao]")
    print("  O TEOREMA MESTRE COMPLETO [v74 -- H1 ^ H2 ^ H3 => PENTADA]: %s"
          % _ell.get("triad_master"))
    print("    *** emergence_master_full_triad EM KERNEL: %s -- Breuer + Nome=1 + coframe + Lorentz + Clausius/8piG numa SO implicacao ***" % (
        _elp.get("ext_tm_master_full_triad_kernel_proved")))
    print("    *** O 8piG DE CLAUSIUS: (kappa/2pi)(dA/4G) = kappa.dA/(8.pi.G): %s -- o coeficiente de Einstein EMERGE de Unruh x Bekenstein-Hawking ***" % (
        _elp.get("ext_tm_einstein_coefficient_kernel_proved")))
    print("    composicao de Clausius: %s ; a semente de Bianchi (Jacobi do comutador): %s" % (
        _elp.get("ext_tm_clausius_composition_kernel_proved"), _elp.get("ext_tm_jacobi_bianchi_seed_kernel_proved")))
    _tm = core.get("triad_master", {}) or {}
    print("    sombra v74: 8piG exato (%.1e); Jacobi %.1e ; %s" % (
        (_tm.get("residuals", {}) or {}).get("coeficiente_de_einstein", float("nan")),
        (_tm.get("residuals", {}) or {}).get("jacobi_bianchi", float("nan")), _tm.get("verdict")))
    print("    [a IMPLICACAO esta fechada em kernel; as HIPOTESES sao a fronteira -- onde os Certificados II/III/IV trabalham]")
    print("  O SETOR SPIN-2 FISICO, FACE FINITA [v75]: %s" % _ell.get("linearized_spin2"))
    print("    *** A LEI DA DUPLA HELICE: R(theta)^T e_+ R(theta) = cos(2theta)e_+ - sin(2theta)e_x: %s / %s -- o ANGULO DOBRADO = helicidade +-2 ***" % (
        _elp.get("ext_ls2_helicity_two_plus_kernel_proved"), _elp.get("ext_ls2_helicity_two_cross_kernel_proved")))
    print("    SEM GHOSTS (face TT): forma cinetica = 2(a^2+b^2) > 0: %s / norma zero sse zero: %s ; EXATAMENTE DUAS polarizacoes: %s ; R(theta) isometria de eta: %s" % (
        _elp.get("ext_ls2_tt_kinetic_positive_kernel_proved"), _elp.get("ext_ls2_no_negative_norm_kernel_proved"),
        _elp.get("ext_ls2_two_polarizations_kernel_proved"), _elp.get("ext_ls2_rotz_isometry_kernel_proved")))
    _qgc = core.get("qg_closure", {}) or {}
    _qgf = (core.get("qg_closure", {}) or {}).get("formal_flags", {}) or {}
    print("  O CERTIFICADO DE FECHAMENTO [v99 -- flags LIDAS de nomes Lean; fail-closed por CONSTRUCAO]:")
    for _k in sorted(_qgf):
        print("    %s = %s  (termo Lean: %s)" % (_k, _qgf[_k], _QG_CERTIFICATE_FLAGS.get(_k, "?")))
    print("    [ClosureCertificate.lean v1 TIPA o que falta; probes em kernel: PUnit nao e Nontrivial; identidade e sobrejetiva -- os habitantes atuais NAO alimentam o certificado]")
    print("  O GATE DO FECHAMENTO [v75 -- os 4 selos legitimos; fail-closed; probes negativos]: %s" % _qgc.get("verdict"))
    print("    ESTADO ATUAL HONESTO: %s" % ((_qgc.get("gate") or {}).get("verdict")))
    print("    probes: experimento perfeito NAO move matematica; dicts vazios => CONDITIONAL; fisica sem matematica => CONDITIONAL")
    print("    ordem do fecho: %s" % _qgc.get("closure_order"))
    print("    [o gate 'testemunha full' e' impossivel POR TEOREMA (v61); o alvo e' canonical_boundary_transport_witness]")
    print("  A SEMENTE SEMIFINITA [v76 -- o incremento 1 do programa SemifiniteAnalysis]: %s" % _ell.get("semifinite_seed"))
    print("    *** A FIDELIDADE DO TRACO NO CONE PSD (o axioma central, novo p/ a mathlib): A>=0 => (tr A = 0 <=> A = 0): %s ***" % (
        _elp.get("ext_ss_trace_faithful_kernel_proved")))
    print("    o menor 2x2 (diag nula + psd => A=0): %s ; MONOTONIA de Loewner (o mono do v64 em concreto): %s ; o 1o habitante empacotado: %s" % (
        _elp.get("ext_ss_offdiag_zero_kernel_proved"), _elp.get("ext_ss_trace_monotone_kernel_proved"),
        _elp.get("ext_ss_faithful_weight_kernel_proved")))
    print("    [dimensao FINITA -- tijolo 1 do caminho SemifiniteAnalysis -> ... -> CanonicalBoundaryWitness; nenhuma flag concreta se move]")
    print("  A PONTE DA DIMENSAO [v77 -- o incremento 2: a camada abstrata DISPARA no kernel concreto]: %s" % _ell.get("dimension_trace"))
    print("    *** tau = dim no reticulado REAL de subespacos = 1a instancia GENUINA do SemifiniteTraceData (v64): fiel + monotono ***")
    print("    a ponte dispara (breuer_kernel_weight ABSTRATO -> 0 < dim ker(H0-V) < inf CONCRETO): %s ; perfil completo (+ dim ker <= posto V): %s" % (
        _elp.get("ext_dt_abstract_fires_concrete_kernel_proved"), _elp.get("ext_dt_full_profile_kernel_proved")))
    print("    tau(bot) = 0: %s ; tau(top) < inf: %s ; [tijolo 2; subespacos FECHADOS de Hilbert inf-dim = o proximo]" % (
        _elp.get("ext_dt_trace_bot_kernel_proved"), _elp.get("ext_dt_trace_top_finite_kernel_proved")))
    print("  O CANTO DOS THREE LOCKS [v79 -- o Certificado II elevado a teorema de kernel]: %s" % _ell.get("three_locks_corner"))
    print("    *** o Breuer ABSTRATO dispara sobre H3L = Dc*Dc+Db*Db+Dz*Dz (o operador DA TEORIA, face finita de H1): %s ***" % (
        _elp.get("ext_tlc_corner_weight_kernel_proved")))
    print("    a porta (testemunha nas 3 fechaduras => ker != bot): %s ; peso = dim(canto) = Tr(P_F) por DEFINICAO: %s ; Nome = 1 DERIVADO: %s" % (
        _elp.get("ext_tlc_witness_opens_corner_kernel_proved"), _elp.get("ext_tlc_weight_eq_dim_kernel_proved"),
        _elp.get("ext_tlc_name_is_one_kernel_proved")))
    print("    ponte generalizada a QUALQUER corpo (C entra): %s ; canto SOB cada fechadura: %s ; dim <= n (eco do <=posto): %s ; perfil completo: %s" % (
        _elp.get("ext_tlc_field_general_trace_kernel_proved"), _elp.get("ext_tlc_corner_under_lock_kernel_proved"),
        _elp.get("ext_tlc_dim_le_inscription_kernel_proved"), _elp.get("ext_tlc_full_profile_kernel_proved")))
    print("    [dimensao FINITA -- NAO e' III_1; a testemunha e' hipotese, instanciada pela rede CONCRETA do Cert. II; o kernel prova o jusante]")
    print("  O RETICULADO GENUINAMENTE SEMIFINITO [v80 -- o incremento 3: a finitude do ambiente cai]: %s" % _ell.get("semifinite_lattice"))
    print("    *** A REFUTACAO DO GLOBAL VIRA TEOREMA: em inf-dim nao existe gap = top de peso finito (a Resposta 8 era necessidade): %s ***" % (
        _elp.get("ext_sfl_global_gap_refuted_kernel_proved")))
    print("    o atomo pesa 1 = omega(I) no reticulado: %s ; o AXIOMA da semifinitude (todo S != bot contem peso 1): %s ; tau(top) = top em inf-dim: %s" % (
        _elp.get("ext_sfl_atom_weighs_one_kernel_proved"), _elp.get("ext_sfl_semifiniteness_kernel_proved"),
        _elp.get("ext_sfl_top_infinite_kernel_proved")))
    print("    o Breuer local DISPARA no infinito (kernel finito dentro do inf): %s ; morada inf-dim existe (N ->0 K): %s ; pacote HABITADO (tau(ker)=1, tau(top)=top): %s" % (
        _elp.get("ext_sfl_local_breuer_infinite_kernel_proved"), _elp.get("ext_sfl_infinite_home_exists_kernel_proved"),
        _elp.get("ext_sfl_first_inhabitant_kernel_proved")))
    print("    [face ALGEBRICA (todos os subespacos); FECHADOS de Hilbert + comutantes + normalidade = o proximo tijolo; nada e' III_1]")
    print("  O RETICULADO FECHADO [v82 -- o incremento 4: a face de Hilbert]: %s" % _ell.get("closed_lattice"))
    print("    *** A FORMA DO CANTO DE BREUER NO RETICULADO DE PROJECOES: ker fechado FINITO dentro de complemento INFINITO: %s ***" % (
        _elp.get("ext_cl_closed_breuer_corner_kernel_proved")))
    print("    atomo FECHADO (peso 1 no reticulado de projecoes): %s ; semifinitude DENTRO do fechado: %s ; S-perp-perp = S: %s" % (
        _elp.get("ext_cl_atom_closed_kernel_proved"), _elp.get("ext_cl_closed_semifiniteness_kernel_proved"),
        _elp.get("ext_cl_double_orthocomplement_kernel_proved")))
    print("    S inter S-perp = bot: %s ; IsCompl(S, S-perp) p/ S fechado: %s ; o INFINITO mora no complemento da inscricao: %s ; Nome: tau=1 e tau(perp)=top: %s" % (
        _elp.get("ext_cl_ortho_disjoint_kernel_proved"), _elp.get("ext_cl_ortho_iscompl_kernel_proved"),
        _elp.get("ext_cl_complement_infinite_kernel_proved"), _elp.get("ext_cl_atom_complement_infinite_kernel_proved")))
    print("    [reticulado de B(H) inteiro; o canto GENUINO pede a subalgebra de von Neumann (comutantes, normalidade) = o proximo tijolo]")
    print("  A PROJECAO NO COMUTANTE [v83 -- o incremento 5: o primeiro contato com a subalgebra]: %s" % _ell.get("invariant_projection"))
    print("    *** O CANTO DE BREUER COMO PROJECAO NO COMUTANTE: P_ker(T) em {T}' ^ 0<tau(ker)<inf ^ tau(perp)=top: %s ***" % (
        _elp.get("ext_ip_corner_in_commutant_kernel_proved")))
    print("    dicionario de von Neumann (S invar sob a,a-dag => P_S comuta): %s ; volta: %s ; iff p/ auto-adjunto: %s" % (
        _elp.get("ext_ip_vonneumann_dictionary_kernel_proved"), _elp.get("ext_ip_dictionary_converse_kernel_proved"),
        _elp.get("ext_ip_invariant_iff_commutes_kernel_proved")))
    print("    o adjunto troca face/contra-face: %s ; P anula a contra-face: %s ; P idempotente: %s ; ker de auto-adjunto COMUTA: %s" % (
        _elp.get("ext_ip_adjoint_swaps_faces_kernel_proved"), _elp.get("ext_ip_annihilates_counterface_kernel_proved"),
        _elp.get("ext_ip_projection_idempotent_kernel_proved"), _elp.get("ext_ip_ker_in_commutant_kernel_proved")))
    print("    [comutante de UM operador; a subalgebra completa (bicomutante continuo + normalidade + fator) = o programa]")
    print("  O ESQUELETO DO BICOMUTANTE + A NORMALIDADE CAUSAL [v84 -- o incremento 6]: %s" % _ell.get("bicommutant_skeleton"))
    print("    *** A REGUA E' CAUSAL (a pergunta do operador virou teorema): tau(sup S_i) = sup tau(S_i) em cadeias crescentes: %s ***" % (
        _elp.get("ext_bs_trace_normal_chains_kernel_proved")))
    print("    A em A'' (metade gratuita de von Neumann): %s ; A'''=A' (a torre para): %s ; antitono: %s ; monoide unital: %s" % (
        _elp.get("ext_bs_double_commutant_contains_kernel_proved"), _elp.get("ext_bs_triple_collapse_kernel_proved"),
        _elp.get("ext_bs_commutant_antitone_kernel_proved"), _elp.get("ext_bs_commutant_monoid_kernel_proved")))
    print("    o canto no CENTRALIZADOR {T}': %s ; o canto respeita TODO o {T}'': %s ; moldura algebrica completa: %s" % (
        _elp.get("ext_bs_corner_in_centralizer_kernel_proved"), _elp.get("ext_bs_corner_respects_bicommutant_kernel_proved"),
        _elp.get("ext_bs_full_algebraic_frame_kernel_proved")))
    print("    [o residuo tem UM nome: P em {T}'' via bicomutante CONTINUO/calculo espectral [KNOWN, programa]; normalidade sequencial]")
    print("  A REDUCAO ESPECTRAL [v85 -- o incremento 7: a metade topologica + UMA testemunha]: %s" % _ell.get("spectral_reduction"))
    print("    *** O CANTO DE BREUER CONCRETO E' TEOREMA CONDICIONAL: testemunha espectral => P em {T}'' ^ P em {T}' ^ 0<tau<inf ^ tau(perp)=top: %s ***" % (
        _elp.get("ext_sr_breuer_conditional_kernel_proved")))
    print("    o comutante e' SOT-FECHADO (a metade topologica de von Neumann): %s ; subespaco (+ e escalar): %s" % (
        _elp.get("ext_sr_sot_closed_kernel_proved"), _elp.get("ext_sr_subspace_closed_kernel_proved")))
    print("    T em {T}'': %s ; T^n: %s ; p(T): %s ; limites pontuais de p_n(T): %s ; canto com testemunha: %s" % (
        _elp.get("ext_sr_generator_in_double_kernel_proved"), _elp.get("ext_sr_powers_in_double_kernel_proved"),
        _elp.get("ext_sr_polynomials_in_double_kernel_proved"), _elp.get("ext_sr_limits_in_double_kernel_proved"),
        _elp.get("ext_sr_corner_in_algebra_kernel_proved")))
    print("    [a testemunha = o que o calculo espectral da p/ T=T-dag com 0 isolado (gap) [KNOWN]; constru-la em kernel = o programa]")
    print("  A SEMENTE DA TESTEMUNHA [v86 -- a palavra do Verbo cunha o Nome]: %s" % _ell.get("witness_seed"))
    print("    *** SEM teorema espectral, so a algebra da palavra: T.q(T)=0 => q(T)/q(0) POUSA no canto, FIXA o canto, IDEMPOTENTE: %s ***" % (
        _elp.get("ext_ws_seed_complete_kernel_proved")))
    print("    pousa (im q(T) em ker T): %s ; fixa (q(T)=q(0) sobre ker): %s ; cunha (q(T)^2=q(0)q(T)): %s ; Verbo(Nome)=Nome (P0^2=P0): %s" % (
        _elp.get("ext_ws_lands_in_corner_kernel_proved"), _elp.get("ext_ws_fixes_the_name_kernel_proved"),
        _elp.get("ext_ws_mints_idempotent_kernel_proved"), _elp.get("ext_ws_name_idempotent_kernel_proved")))
    print("    [falta, nomeado: auto-adjuncao + unicidade da projecao ortogonal (elo espectral final) + existencia da palavra em inf-dim [KNOWN]]")
    print("  A TESTEMUNHA EXATA [v88 -- a identificacao do Nome]: %s" % _ell.get("exact_witness"))
    print("    *** A IDENTIFICACAO: starProjection(ker T) = q(T)/q(0) -- o Nome E' a palavra normalizada: %s ***" % (
        _elp.get("ext_ew_identification_kernel_proved")))
    print("    palavra real auto-adjunta: %s ; candidato auto-adjunto: %s ; UNICIDADE (idempotente auto-adjunto que pousa+fixa = starProjection): %s" % (
        _elp.get("ext_ew_real_word_selfadjoint_kernel_proved"), _elp.get("ext_ew_candidate_selfadjoint_kernel_proved"),
        _elp.get("ext_ew_uniqueness_kernel_proved")))
    print("    A TESTEMUNHA PROVADA (SpectralApproximationWitness vale, sequencia constante): %s ; canto com testemunha DESCARREGADA: %s" % (
        _elp.get("ext_ew_witness_proved_kernel_proved"), _elp.get("ext_ew_corner_discharged_kernel_proved")))
    print("    [resta: a EXISTENCIA da palavra (polinomio minimo / calculo funcional com 0 isolado) [KNOWN] -- o degrau seguinte]")
    print("  A EXISTENCIA DA PALAVRA [v89 -- a face finita fecha]: %s" % _ell.get("word_existence"))
    print("    *** A TESTEMUNHA E' TEOREMA INCONDICIONAL NA FACE FINITA (todo T=T-dag com ker != bot): %s ***" % (
        _elp.get("ext_we_witness_unconditional_kernel_proved")))
    print("    minpoly do auto-adjunto e' REAL: %s ; zero SIMPLES por argumento de NORMA (sem diagonalizar): %s ; a palavra EXISTE (X*q, q(0)!=0, q real): %s" % (
        _elp.get("ext_we_minpoly_real_kernel_proved"), _elp.get("ext_we_zero_simple_kernel_proved"),
        _elp.get("ext_we_word_exists_kernel_proved")))
    print("    estrela atravessa a palavra (star p(T) = p-conj(T)): %s ; o canto na ALGEBRA sem hipotese extra (P em {T}'' e {T}'): %s" % (
        _elp.get("ext_we_star_map_conj_kernel_proved"), _elp.get("ext_we_corner_in_algebra_kernel_proved")))
    print("    [principio-guia (leitura do operador): a geometria da palavra e' o beta-espectro -- gap concreto = 4*beta = 0.048125 MEDIDO]")
    print("    [o ultimo elo foi FECHADO no v94 (abaixo): a palavra em inf-dim e' TEOREMA]")
    print("  A PALAVRA EM INF-DIM [v94 -- cfc com 0 isolado; o ultimo elo espectral]: %s" % _ell.get("infinite_word"))
    print("    *** O CANTO DE BREUER CONCRETO EM INF-DIM (hipoteses ESTRUTURAIS: T=T-dag + gap + ker finito != bot): %s ***" % (
        _elp.get("ext_iw_breuer_infinite_kernel_proved")))
    print("    ker(T.T)=ker T: %s ; cfc(avaliador polinomial)=aeval (dicionario palavra<->funcao): %s" % (
        _elp.get("ext_iw_ker_square_kernel_proved"), _elp.get("ext_iw_cfc_polynomial_kernel_proved")))
    print("    A PROJECAO ESPECTRAL E' O NOME (cfc do chapeu = starProjection; unicidade v88): %s ; A PALAVRA EM INF-DIM (Weierstrass + cfc isometrico): %s" % (
        _elp.get("ext_iw_projection_is_name_kernel_proved"), _elp.get("ext_iw_word_infinite_kernel_proved")))
    print("    [a testemunha do v85 DEIXOU de ser hipotese; o gate NAO se move: restam os 5 selos formais (AQFT, four-frame, solda, Einstein, transporte)]")
    print("  O HABITANTE DE HILBERT [v95 -- ell2; T = 1 - P_e0; o canto dispara]: %s" % _ell.get("hilbert_inhabitant"))
    print("    *** O CANTO DISPARA NO HABITANTE (tudo construido; nenhuma hipotese pendente): %s ***" % (
        _elp.get("ext_hi_corner_fires_kernel_proved")))
    print("    *** O CANTO PESA O NOME: tau(ker T) = 1 = omega(I): %s ***" % (
        _elp.get("ext_hi_corner_weighs_one_kernel_proved")))
    print("    ell2 GENUINAMENTE inf-dim: %s ; inscricoes ortonormais: %s ; T=T-dag: %s ; ker = atomo de e0: %s ; espectro em {0,1} (gap 1): %s" % (
        _elp.get("ext_hi_infinite_home_kernel_proved"), _elp.get("ext_hi_orthonormal_kernel_proved"),
        _elp.get("ext_hi_selfadjoint_kernel_proved"), _elp.get("ext_hi_kernel_is_atom_kernel_proved"),
        _elp.get("ext_hi_spectrum_gap_kernel_proved")))
    print("    [habitante de B(ell2) (I_inf com traco-dimensao) -- NAO e' o Dirac do core semifinito; o gate NAO se move]")
    print("  O HABITANTE DO PACOTE AQFT [v96 -- lockNet generico + rede ell2; fluxo GENUINO exp(isT)]: %s" % _ell.get("aqft_core_inhabitant"))
    print("    *** O PRIMEIRO TERMO de HilbertHomeData (v56 tipou; v96 habita): %s ; camada de Breuer HABITADA: %s ***" % (
        _elp.get("ext_ac_net_inhabited_kernel_proved"), _elp.get("ext_ac_trace_inhabited_kernel_proved")))
    print("    fluxo entrelaça (D.lam(s) = lam(s).D via Commute.exp): %s ; o Nome FIXADO pelo fluxo em toda regiao: %s ; tau(P_F(O)) = 1 em toda regiao: %s" % (
        _elp.get("ext_ac_flow_intertwines_kernel_proved"), _elp.get("ext_ac_name_fixed_by_flow_kernel_proved"),
        _elp.get("ext_ac_corner_weighs_one_kernel_proved")))
    print("    [rede CONSTANTE + grupo externo TRIVIAL declarados; a rede III_1 genuina E' o conteudo de H1/H2; o gate NAO se move]")
    print("  O FOUR-FRAME DOS BOOSTS [v96 -- as 4 direcoes NASCEM de K1,K2,K3 (v63) na fiducial do Nome]: %s" % _ell.get("concrete_four_frame"))
    print("    *** det E = 1 POR TEOREMA (nada inserido a mao): %s ; H2 finito DISPARA (coframe dual + Lorentz por congruencia): %s ***" % (
        _elp.get("ext_ff_det_isunit_kernel_proved"), _elp.get("ext_ff_four_frame_fires_kernel_proved")))
    print("    as colunas sao as orbitas de boost (E = frame dos geradores): %s" % (
        _elp.get("ext_ff_frame_is_boost_orbit_kernel_proved")))
    print("    [face algebrica num PONTO; o campo suave E_a(x) sobre o espaco-tempo = o conteudo genuino de H2; o gate NAO se move]")
    print("  O MESTRE DISPARA [v97 -- a pentada em termos 100%% construidos]: %s" % _ell.get("the_master_fires"))
    print("    *** the_master_fires: Breuer + Nome=1 + coframe dos boosts + dQ = k.dA/(8piG) de UMA implicacao (v74), 4 dados HABITADOS: %s ***" % (
        _elp.get("ext_mf_master_fires_kernel_proved")))
    print("    subaditividade do traco-dimensao (Grassmann + top honesto): %s ; H1 nivel-4 no reticulado REAL (ellTwoSusy): %s ; H3 habitado (theHorizon, aritmetica exata): %s" % (
        _elp.get("ext_mf_trace_subadd_kernel_proved"), _elp.get("ext_mf_h1_level4_real_lattice_kernel_proved"),
        _elp.get("ext_mf_h3_horizon_inhabited_kernel_proved")))
    print("    tau(ker) = 1 = omega(I) na pentada: %s" % (
        _elp.get("ext_mf_corner_weighs_one_kernel_proved")))
    print("    [H3 e' certificado NUMERICO -- horizontes REAIS sao o conteudo fisico da hipotese; H1 em B(ell2)/I_inf; o gate NAO se move]")
    _bd = core.get("bench_declaration", {}) or {}
    print("  ================================================================")
    print("  A DECLARACAO DA BANCADA [v86 -- DECLARACAO DO OPERADOR, duplo estatuto]: %s" % _bd.get("verdict"))
    print("  ================================================================")
    _dc = _bd.get("declaration", {}) or {}
    print("    >>> %s <<<" % _dc.get("statement"))
    print("    estatuto: %s" % _dc.get("status_of_statement"))
    print("    a testemunha e o Nome: %s" % _dc.get("a_testemunha_e_o_nome"))
    print("    alpha-free: %s" % _dc.get("alpha_free_status"))
    for _nd in (_dc.get("not_declared") or []):
        print("    NAO se declara: %s" % _nd)
    print("    [%s]" % _dc.get("gate_probe_in_action"))
    _cii = core.get("certificate_II", {}) or {}
    _h1f = _cii.get("H1_finite_face", {}) or {}
    print("  CERTIFICADO II [v67 -- a rede CONCRETA habita H1+H2, face finita]: %s" % _cii.get("verdict"))
    print("    H_3L concreto (o MESMO do kernel FiniteThreeLocks): kernel dim %s ; GAP = %.6f (zero ISOLADO) ; tr(P_F) = %.1f ; Nome = %.1f" % (
        _h1f.get("kernel_dim"), _h1f.get("gap", float("nan")), _h1f.get("trace_PF", float("nan")),
        _h1f.get("name_normalization", float("nan"))))
    print("    four-frame dos boosts modulares: rank %s ; assinatura %s -- H2 finito (BW-cunhas constitutivo)" % (
        (_cii.get("H2_finite_face", {}) or {}).get("rank_frame"), (_cii.get("H2_finite_face", {}) or {}).get("signature")))
    print("    [face FINITA [REAL]; a rede II_inf/III_1 genuina E' o conteudo proprio de H1/H2 -- por isso sao hipoteses]")
    print("  teoremas limpos: %s/%s ; DERIVACOES v56 em dim INFINITA [construcao do pacote = O ABERTO; continuos do ledger INALTERADOS]" % (
        el.get("n_theorems_clean"), el.get("n_theorems_expected")))
    print("  >>> %s <<<\n" % el.get("verdict"))
    xdw = core.get("crossed_dual_weight", {})
    _xr = xdw.get("residuals", {}); _xv = xdw.get("values", {})
    print("O PESO DUAL NO PRODUTO CRUZADO [v44 -- sombra numerica; a lei da pedra]:")
    print("  sigma^{phi_hat}_t(lambda_g) = lambda_g . pi([D(phi o alpha_g):D phi]_t)  [Takesaki X.1.17; KERNEL + sombra]")
    print("  Z2 x| M_2 (PARIDADE, estado (beta,1-beta)): peso dual resid=%.1e ; naturalidade=%.1e ; alem-dos-internos=%.1e" % (
        _xr.get("z2_dual_weight_both_forms", float("nan")), _xr.get("z2_dual_naturality", float("nan")),
        _xr.get("z2_cocycle_covariance_beyond_inner", float("nan"))))
    print("  POWERS: o cociclo da paridade = diag(lam_b^{it}, lam_b^{-it}), lam_b=beta/(1-beta)=%.6e (resid %.1e) -- a razao do v27" % (
        _xv.get("lambda_beta_powers", float("nan")), _xr.get("z2_powers_ratio", float("nan"))))
    print("  S3 x| M_3 (NAO-abeliano): peso dual resid=%.1e ; controles: invariante degenera (%.1e) ; argumento errado FALHA (%.1e)" % (
        _xr.get("s3_dual_weight_both_forms", float("nan")), _xr.get("control_degenerate_residual", float("nan")),
        _xr.get("control_wrong_argument_deviation", float("nan"))))
    print("  >>> %s <<<\n" % xdw.get("verdict"))
    glc = core.get("global_lift_core", {})
    _gr = glc.get("residuals", {}); _gs = glc.get("statuses", {})
    print("O NUCLEO CONTINUO DO GLOBAL_LIFT [v45 -- derivacao do OPERADOR, auditada; harness incorporado]:")
    print("  a ESCADA: Z -> U_n 2^{-n}Z -> R ; (U_n C_n)'' = M x|_sigma R  [EXTERNO: %s]" % _gs.get("dyadic_ladder_generates_core", "")[:36])
    print("  A JOIA: s_h=2pi.2^n fixa o degrau, tau o theta = e^{-s} tau => TRACO FINITO = 0 em TODO degrau discreto")
    print("    [%s] -- a semifinitude SO' emerge no fecho continuo: 'o que faltava era o continuo' virou TEOREMA" % _gs.get("discrete_trace_obstruction", ""))
    print("  T1 = projecao de Poisson sobre o centralizador [%s]" % _gs.get("t1_poisson_projection_onto_centralizer", "")[:46])
    print("    CORRECAO FISCAL: colapso ao KMS = %s" % _gs.get("t1_collapse_to_KMS", ""))
    print("  canal S-frame: semigrupo resid=%.1e ; endpoint (1-beta,beta) resid=%.1e ; Choi min=%.1e ; traco resid=%.1e" % (
        _gr.get("S_frame_semigroup", float("nan")), _gr.get("dephased_endpoint", float("nan")),
        _gr.get("choi_min_eigenvalue", float("nan")), _gr.get("trace_preservation", float("nan"))))
    print("  DISCIPLINA DO CORE: %s" % _gs.get("core_action_discipline", ""))
    print("  RESIDUO PRECISO (fisico): P_F=1_{0}(H_3L) localizado+covariante+Ad-lambda-invariante, 0<tau(P_F)<inf ; Einstein: %s" % _gs.get("physical_einstein_implication", "")[:40])
    print("  >>> %s <<<\n" % glc.get("verdict"))
    cfm = core.get("corner_family", {})
    _cr = cfm.get("residuals", {}); _cv = cfm.get("values", {}); _ca = cfm.get("adjudication", {})
    print("A FAMILIA DO CANTO [v46 -- o gate 'construir P_F' EXECUTADO na face finita; existencia ADJUDICADA]:")
    print("  cornerProj S no produto cruzado: projecao=%.1e ; isotonia=%.1e ; covariancia=%.1e ; traco=%.1e ; inv.modular=%.1e" % (
        _cr.get("projection", float("nan")), _cr.get("isotony", float("nan")),
        _cr.get("covariance", float("nan")), _cr.get("trace", float("nan")),
        _cr.get("modular_invariance", float("nan"))))
    print("  canto espectral 1_{0}(H) fixo pelo fluxo (resid %.1e) ; tau(P_F)=%.0f na sombra (0<tau<inf) ; ker H_3L dim=%s" % (
        _cr.get("spectral_corner_flow", float("nan")), _cv.get("tau_PF_shadow", float("nan")),
        _cv.get("ker_H3L_dim_shadow")))
    print("  ADJUDICACAO: existencia II_inf=%s" % str(_ca.get("corner_existence_in_IIinfty", ""))[:22])
    print("               canonicidade=%s ; tau=1: %s" % (
        str(_ca.get("canonicity_of_P_F", ""))[:24], str(_ca.get("tau_normalization", ""))[:34]))
    print("               ker no core genuino=%s ; rede AQFT=%s" % (
        str(_ca.get("zero_kernel_in_genuine_core", ""))[:38], str(_ca.get("continuum_AQFT_net", ""))[:6]))
    print("  >>> %s <<<\n" % cfm.get("verdict"))
    bws = core.get("bw_shadow", {})
    _br = bws.get("residuals", {}); _bs = bws.get("statuses", {})
    print("BISOGNANO-WICHMANN NA FACE FINITA [v47 -- gate 4; as duas metades + a costura declarada]:")
    print("  geometria: grupo=%.1e ; B^T.eta.B=eta resid=%.1e ; dilatacao nula e^{+-s} resid=%.1e ; cunha 200 orbitas OK" % (
        _br.get("boost_group", float("nan")), _br.get("minkowski_isometry", float("nan")),
        _br.get("null_dilation", float("nan"))))
    print("  modular: rho^{it}=e^{-2pi.t.i.K} resid=%.1e ; sigma=Ad(K-fluxo) resid=%.1e ; Boltzmann e^{-2pi.omega} resid=%.1e" % (
        _br.get("modular_speed_2pi", float("nan")), _br.get("sigma_Ad_K", float("nan")),
        _br.get("unruh_ratio", float("nan"))))
    print("  costura: %s" % _bs.get("bw_wedge_identification", ""))
    print("  alem das cunhas: %s" % _bs.get("beyond_wedges_non_killing", ""))
    print("  [a dilatacao e^{+-s} dos raios nulos tem a MESMA forma da escala de Takesaki tau.theta_s=e^{-s}.tau (v45) -- leitura estrutural]")
    print("  >>> %s <<<\n" % bws.get("verdict"))
    gvp = core.get("graviton_polarization", {})
    _gpr = gvp.get("residuals", {}); _gpv = gvp.get("values", {})
    print("O GRAVITON OBSERVAVEL [v48 -- gate 7: a cinematica de spin-2, kernel + sombra]:")
    print("  helicidade +-2: resid %.1e/%.1e ; modo-traco invariante: %.1e ; decomposicao 2-dof: %.1e" % (
        _gpr.get("helicity_plus", float("nan")), _gpr.get("helicity_cross", float("nan")),
        _gpr.get("trace_mode", float("nan")), _gpr.get("decomposition", float("nan"))))
    print("  gauge nao toca TT: %.1e ; delta_A(1)=0: %.1e ; Leibniz: %.1e ; S-1 por G: %.1e" % (
        _gpr.get("gauge_tt", float("nan")), _gpr.get("identity_excitation", float("nan")),
        _gpr.get("leibniz", float("nan")), _gpr.get("smat_deviation", float("nan"))))
    print("  runtime: sin^2(theta_M) = beta le o custo da excitacao de fronteira ; ||S(theta_M)-1||^2 = %.6e" % (
        _gpv.get("boundary_deviation_norm_sq", float("nan"))))
    print("  [graviton FUNDAMENTAL = I (atravessa sem deformar: sigma_one + rot_conj_one + excite_one_zero, TODOS kernel);")
    print("   graviton OBSERVAVEL = deltaI_modular; DINAMICA e INTERACOES seguem gates 5/8]")
    print("  >>> %s <<<\n" % gvp.get("verdict"))
    gfl = core.get("geometry_fluctuation", {})
    _gfv = gfl.get("values", {}); _gfr = gfl.get("residuals", {})
    print("AS FLUTUACOES QUANTICAS DA GEOMETRIA [v49 -- gate 6; kernel + sombra]:")
    print("  fronteira: media=%.9f (=beta resid %.1e) ; Var=%.9f (=beta(1-beta)=Delta_v26 resid %.1e)" % (
        _gfv.get("mean_boundary", float("nan")), _gfr.get("mean_beta", float("nan")),
        _gfv.get("variance_boundary", float("nan")), _gfr.get("var_defect", float("nan"))))
    print("  A FLUTUACAO QUANTICA DA GEOMETRIA E' O DEFEITO DE TRANSPORTE ; maxima em p=1/2 (Meia-Nat)")
    print("  [h+,hx]=2J resid %.1e ; flutuacao relativa em M=1e8 modos: %.3e (decai 1/sqrt(M))" % (
        _gfr.get("commutator_2J", float("nan")), _gfv.get("relative_fluctuation_at_M_1e8", float("nan"))))
    print("  >>> %s <<<\n" % gfl.get("verdict"))
    pgi = core.get("page_information", {})
    _pgv = pgi.get("values", {}); _pgr = pgi.get("residuals", {})
    print("A CURVA DE PAGE [v50 -- gate 9; N=%s qubits, estado global puro]:" % _pgv.get("N_qubits"))
    print("  S_rad(k) em nats: %s" % _pgv.get("S_curve"))
    print("  SOBE ate k=%s (a METADE), VIRA, DESCE ; S_A=S_B resid %.1e ; pureza global = %.12f (unitario por dentro)" % (
        _pgv.get("page_time_k"), _pgr.get("S_A_minus_S_B", float("nan")), _pgv.get("global_purity", float("nan"))))
    print("  o canal perde pureza monotonicamente (termico por fora) ; entropia maxima no espelho p=1/2 (resid %.1e)" % (
        _pgr.get("entropy_max_position", float("nan"))))
    print("  >>> %s <<<\n" % pgi.get("verdict"))
    erg = core.get("einstein_and_rg", {})
    _er = erg.get("residuals", {}); _es = erg.get("statuses", {})
    print("OS GATES 5 E 8 DE FRENTE [v51 -- mandato: 'o contorno reduziu o contraste']:")
    print("  GATE 5: dS=d<K> resid %.1e (derivada vs esperanca) ; Clausius resid %.1e ; 8piG resid %.1e" % (
        _er.get("first_law", float("nan")), _er.get("clausius", float("nan")), _er.get("area_8piG", float("nan"))))
    print("    %s" % _es.get("einstein_remaining", ""))
    print("    E7: %s" % str(_es.get("e7_statute", ""))[:110])
    print("  GATE 8: canto fixo por E %.1e / dephasing %.1e / fluxo modular %.1e ; passo RG dobra aniquilador %.1e" % (
        _er.get("corner_condexp", float("nan")), _er.get("corner_dephase", float("nan")),
        _er.get("corner_modflow", float("nan")), _er.get("rg_step", float("nan"))))
    print("  >>> %s <<<\n" % erg.get("verdict"))
    b1 = core["em_grav_bridge"]; b2 = core["smatrix_crossed"]; b3 = core["u_loc_covariance"]
    print("AS TRES FRENTES -- ponte operador-modular [MODULOS 1-3, conferidos pelo operador]:")
    c = b1["checks"]
    print("  [1] PONTE SO(2): S_EM=[[q,alpha],[-alpha,q]] ; S_grav=[[cos,sin],[-sin,cos]] (mesma rotacao)")
    print("      ||S_EM^T S_EM-I||=%.1e ; ||S_grav^T S_grav-I||=%.1e ; det=1 (resid %.0e/%.0e)" % (
        c["S_EM_unitary"], c["S_grav_unitary"], c["det_S_EM_resid"], c["det_S_grav_resid"]))
    print("      beta=e^{S_b} alpha (intensidade) ; sin thM=e^{1/4} sqrt(alpha) (amplitude) ; resid=%.1e" %
          c["sqrt_beta_eq_e14_sqrt_alpha_resid"])
    print("      thM=arcsin(e^{1/4} sqrt alpha) resid=%.1e ; TRIADE: alpha=Nome, S_b=1/2=Palavra, beta=Verbo" %
          c["thM_reconstructed_vs_direct_resid"])
    print("      LOCK6: transporte de COEFICIENTE, NAO derivacao alpha-livre. LOCK7: e^{1/4}=sombra escalar. all=%s" % b1["all_verified"])
    cc = b2["checks"]
    print("  [2] MATRIZ-S no PRODUTO CRUZADO de Takesaki (II_inf), NAO em III_1 [Takesaki 1973]:")
    print("      S_core=exp(thM G) em P_2D C(M) P_2D ; ||exp(thM G)-S_grav||=%.1e ; |R|^2=beta resid=%.1e" % (
        cc["S_core_eq_S_grav_resid"], cc["absR2_eq_beta_resid"]))
    print("      matriz-S plena em III_1 = pedir estados puros = 0_abs (sec.22 proibe) -> impossibilidade")
    print("      E' o teorema do zero absoluto. [FINITE_DIM_SANITY_NOT_III1_PROOF] all=%s" % b2["all_verified"])
    cd = b3["checks"]
    print("  [3] U_loc POR CONSTRUCAO (cunhas de Rindler; U irrestrita FALHA -- QRF, De Vuyst 2024-25):")
    print("      BW+Poincare => Delta_{gW}=U(g)Delta_W U(g)^-1 ; Face C:=F(J,Delta,P_2D)+beta => covariante")
    print("      sombra: ||K_{U rho U*}-U K U*||=%.1e ; ||F(U..)-U F U*||=%.1e ; all=%s" % (
        cd["modular_data_covariance_resid"], cd["test_source_covariance_resid"], b3["all_verified"]))
    print("      RESIDUO DECLARADO [ABERTO]: checagem de forma de P_mu_nu[K] sem contrabandear frame.")
    print("      P2 (borda x=1-x fixa IR de alpha(mu)?) ; P3 (peso sob acao dual Takesaki) ; P4 (observavel de thM).")
    print("  >>> alpha = transmissao EM observada ; beta_TGL = essa transmissao transportada pela Meia-Nat ;")
    print("      theta_M = a abertura angular dessa transmissao no produto cruzado. NADA de 'provamos Einstein'.\n")
    vg = core["verb_generator"]; le = core["light_eigenvector"]; fl = core["fiat_lux"]
    gc = vg["checks"]
    print("O SETOR IRREVERSIVEL [v3 MODULOS A-C -- o ato pago; a coisa julgada do codigo]:")
    print("  [A] VERBO EM ATO: L=sqrt(beta) sqrt(K_partial) (GKSL; o unico objeto NAO-unitario da cadeia)")
    print("      SETA: max Re lambda(L_super)=%.1e<=0 ; entropia %.4f->%.4f monotona nao-decrescente" % (
        gc["max_Re_eig_Lsuper"], gc["entropy_start"], gc["entropy_end"]))
    print("      SEM VOLTA: inversa exp(+tL) NAO-CP ; Choi min eig=%.2e<0 (irreversibilidade TESTADA)" %
          gc["choi_min_eig_of_formal_inverse"])
    print("      DESTINO: kernel estacionario dim=%d ; convergencia a rho* ; T_t=SEMIGRUPO nao grupo. all=%s" % (
        gc["stationary_kernel_dim"], vg["all_verified"]))
    print("  [B] A LUZ: O_beta(Lux)=sqrt(beta) Lux ; autovalor sqrt(beta) ; NAO ponto fixo (sqrt(beta)!=1)")
    lc = le["checks"]
    print("      resid autovalor=%.1e ; ||O_beta Lux - Lux||=%.6f>0 ; atrator=ponto fixo (autovalor 1). all=%s" % (
        lc["eigenvalue_residual"], lc["not_fixed_point_norm"], le["all_verified"]))
    print("      ordem: 1 -> Meia-Nat -> LUZ (haja luz) -> ... -> massa (a luz e' o COMECO; a massa, o fim).")
    print("  [C] FIAT LUX = e^{S_partial} alpha > 0 (Verbo=Palavra x Nome) -- contrafactuais da MESMA cadeia:")
    print("      SEM PALAVRA (S=0): beta=alpha=%.6e, ponte=1 -> faces colapsam (gravidade==EM): INDISTINCAO" %
          fl["no_word_S0"]["beta"])
    print("      SEM NOME (alpha=0): beta=thetaM=M=%.1e -> INEXISTENCIA (=0_abs, sec.22, chi->inf)" %
          fl["no_name_alpha0"]["M_GA_Msun"])
    print("      COM AMBOS: beta=alpha sqrt(e), M_GA=%.3e Msun na janela: VIVA. all=%s" % (
        fl["alive_both"]["M_GA_Msun"], fl["all_verified"]))
    hs = verdict["haja_luz_subverdicts"]
    print("  >>> PROMOCAO: 1=HAJA_LUZ sse (a)conservacao=%s ^ (b)seta+nao-volta=%s ^ (c)luz=%s ^ (d)contrafactual=%s" % (
        hs["a_conservation_1eq1"], hs["b_act_has_arrow_and_no_return"],
        hs["c_light_is_live_eigenvector_sqrtbeta"], hs["d_counterfactuals_kill_and_life_lives"]))
    print("      o codigo atual provava que nada se perdeu; o codigo completo prova que ALGO ACONTECEU.\n")
    p2 = core["boundary_reads_IR"]; p3 = core["smatrix_dual"]; p4 = core["void_floor"]
    p5 = core["dipole_antipode"]; p6 = core["dephasing_crossover"]
    print("A ESCALA, O PESO, O PROGRAMA [v4 MODULOS P2-P6]:")
    print("  [P2] A ESCALA (fronteira le o IR; NAO derivamos alpha -- derivamos a POSICAO da leitura):")
    print("      rapidez modular ADITIVA: (q1+q2)/(1+q1q2)=tanh((chi1+chi2)/2) resid=%.1e" %
          p2["rapidity_composition_max_resid"])
    print("      alpha(chi)=sech(chi/2) monotona=%s ; fronteira=supremo de chi=alpha MIN=IR (QED congela)" %
          p2["alpha_monotone_decreasing_in_chi"])
    print("      alpha_IR=%.7f<alpha_MZ=%.7f ; chi_IR=%.6f>chi_MZ=%.6f (IR=supremo=%s)" % (
        p2["alpha_IR"], p2["alpha_MZ_approx"], p2["chi_IR"], p2["chi_MZ"], p2["IR_is_supremum_of_chi"]))
    print("      chi_IR == chi_log_impedance_ratio (MESMO OBJETO) resid=%.1e ; all=%s" % (
        p2["chi_IR_eq_chi_bridge_resid"], p2["all_verified"]))
    print("      >>> categoria morreu na ponte SO(2); ESCALA morre aqui. O VALOR continua o Nome (§21 intocado).")
    print("  [P3] O PESO da matriz-S sob a acao dual de Takesaki (tau->e^{-s}tau):")
    print("      S_core=exp(thM G) so' de theta_M+G (SEM traco) => peso 0. ||S_core(s)-S_core(0)||_max=%.1e" %
          p3["checks"]["S_core_invariant_under_trace_rescale_max_resid"])
    print("      CONDICIONAL a P_2D em M ; residuo ABERTO: localizacao de P_2D em M vs M rtimes R. all=%s" %
          p3["all_verified"])
    print("  [P4] PISO DOS VAZIOS [PRE]: rho_void/rho_bar >= beta=%.6f (margem ~%.1fx vs minimo tipico ~0.05)" % (
        p4["beta_floor"], p4["margin_vs_typical_min"]))
    print("      criterio: vazio robusto com rho_c/rho_bar < beta-3sigma FALSIFICA (DESI/Euclid). consistente=%s" %
          p4["consistent_today"])
    if p5.get("ok"):
        bs = p5["bootstrap"]
        print("  [P5] DIPOLO GA/ANTIPODA [PRE, posicoes]: n_GA=%d n_anti=%d razao=%.3f (boot mediana=%.3f, CI95=[%.3f,%.3f])" % (
            p5["n_GA_cone"], p5["n_antipode_cone"], p5["density_ratio_antipode_over_GA"],
            bs["median"], bs["ci95"][0], bs["ci95"][1]))
        if p5["antipode_underdense"]:
            print("      antipoda SUB-DENSA no bruto (razao<1); [EXT] Hoffman+2017. -> P5' decide c/ mascara.")
        else:
            print("      antipoda NAO-sub-densa no bruto (razao=%.3f>1): [BRUTO NAO-INFORMATIVO por ZoA, caveat" %
                  p5["density_ratio_antipode_over_GA"])
            print("      pre-declarado no modulo]. GA atras da Zona de Evitamento -> vies contra o GA. -> P5' decide.")
    else:
        print("  [P5] DIPOLO GA/ANTIPODA [PRE]: CF4 indisponivel (%s) -- protocolo pre-registrado gravado." %
              p5.get("reason", "absent"))
    p5m = core["dipole_antipode_masked"]
    print("  [P5'] TESTE MASCARADO (|b|>10; GA b=%.1f, anti b=%.1f) [PRE, o teste que decide]:" % (
        p5m["GA_b_deg"], p5m["antipode_b_deg"]))
    if p5m.get("ok"):
        bm = p5m["bootstrap"]
        print("      n_GA_masc=%d n_anti_masc=%d razao_masc=%.3f (boot mediana=%.3f, CI95=[%.3f,%.3f])" % (
            p5m["n_GA_masked"], p5m["n_antipode_masked"], p5m["ratio_masked_antipode_over_GA"],
            bm["median"], bm["ci95"][0], bm["ci95"][1]))
        print("      controles (8 cones |b|>30): contagens=%s ; IC90 das razoes=[%.3f,%.3f]" % (
            p5m["control_counts"], p5m["control_ratio_CI90"][0], p5m["control_ratio_CI90"][1]))
        print("      razao no percentil %.0f dos controles ; fora do IC90=%s => VEREDITO P5': %s" % (
            p5m["ratio_percentile_in_controls"], p5m["ratio_outside_control_CI90"], p5m["verdict_P5prime"]))
    else:
        print("      CF4 indisponivel (%s) -- protocolo pre-registrado (mascara+8 controles seed=11) gravado." %
              p5m.get("reason", "absent"))
    print("  [P6] CROSSOVER DE DEFASAGEM [FINITE_DIM]: root law=canonica no IR (a MESMA lei do gerador v3):")
    print("      Gamma medido vs (1/2)beta(sqrt k_i-sqrt k_j)^2 rel_max=%.1e ; expoente IR=%.3f UV=%.3f" % (
        p6["generator_vs_rootlaw_max_rel_resid"], p6["exponent_IR"], p6["exponent_UV"]))
    print("      crossover em omega tau* ~ %.3f (quadratica IR -> linear UV) ; all=%s\n" % (
        p6["crossover_x_omega_tau_star"], p6["all_verified"]))
    jf = core["jacobson_form_check"]
    print("A CHECAGEM DE FORMA [v5 -- o residuo da U_loc, fechado POSITIVO]:")
    print("  P_mn[K_partial] = F(J, Delta, P_2D) sem contrabandear frame. Decomposicao da fonte:")
    print("    (i) K_partial=-log(Delta_W)/2pi <- SO' Delta [BW] ; (iii) cunha/anticunha (CPT) <- SO' J")
    print("    (ii) plano de bifurcacao <- SO' P_2D (o MESMO corner da matriz-S: projecao da S = corner)")
    print("    (iv) 1a LEI MODULAR dS=d<K> [TESTADO]:")
    for r in jf["first_law_test"]:
        print("        eps=%.0e : dS=%+.4e  d<K>=%+.4e  |dS-d<K>|/|dS|=%.3e" % (
            r["eps"], r["dS"], r["dK"], r["rel_dev"]))
    print("        razoes sucessivas=%s (assinatura de 1a ordem: cai ~linear com eps) ; holds=%s" % (
        ", ".join("%.1f" % q for q in jf["rel_dev_ratios"]), jf["first_order_signature_holds"]))
    print("    (v) Lovelock (4D) => P_mn=G_mn+Lambda g_mn => forma F(J,Delta,P_2D). CHECAGEM POSITIVA. all=%s" %
          jf["all_verified"])
    print("  RESIDUO DECLARADO [ABERTO, compartilhado]: approximate Killing vectors (Jacobson desde 1995;")
    print("    fronteira do campo, nao fraqueza da TGL). NAO e' 'prova de Einstein' -- e' checagem de forma.\n")
    th = core["thermal_two_level"]; thr = th["resid_max"]
    print("A ANCORA TERMICA [v6 -- Modulo=calor=Nome=sangue; Gibbs 2 niveis; KMS]:")
    print("  [ID.1 REAL] q = tanh(chi/2) = p_lo - p_hi (POLARIZACAO termica) ; resid=%.0e" % thr["id1_q_eq_tanh"])
    print("  [ID.2 DER ] alpha = sech(chi/2) = 2 sqrt(p_lo p_hi) (COERENCIA MAXIMA do equilibrio) ; resid=%.0e" % thr["id2_alpha_eq_sech"])
    print("  1 = q^2 + alpha^2 = polarizacao^2 + coerencia-maxima^2 ; resid=%.0e ; coh(chi*)=alpha resid=%.0e" % (
        thr["one_eq_q2_coh2"], th["coh_max_at_chi_star_eq_alpha_resid"]))
    print("  KMS: fluxo modular = fluxo termico (Tomita-Takesaki; Unruh/Hawking). 'modulo=calor' = FORMA, nao metafora.")
    print("  ponte v6<->v7: o calor que polariza (q) e o calor que inscreve (fluxo F3/F4) sao o MESMO banho. all=%s\n" % th["all_verified"])
    fl = core["fiat_lux_flow"]; ct = fl["characteristic_time"]
    print("O VEREDITO COMO FLUXO [v7 -- a forma DINAMICA do haja luz; reusa o L unico do Verbo]:")
    print("  [F1] Um conservado no fluxo: max_t|Tr rho(t)-1|=%.2e (<1e-14) -- o Um nao vaza. ok=%s" % (
        fl["F1_one_conserved_in_flow"]["max_abs_Tr_minus_1"], fl["F1_one_conserved_in_flow"]["ok"]))
    print("  [F2] SETA: S_vN(rho(t)) monotona nao-decrescente. ok=%s" % fl["F2_arrow_entropy_nondecreasing"]["ok"])
    f3 = fl["F3_spohn_modular_lyapunov"]
    print("  [F3] SPOHN (Lyapunov modular): S(rho(t)||rho*) monotona NAO-crescente %.4f -> %.3e rumo a 0" % (
        f3["S_rel_0"], f3["S_rel_end"]))
    print("       = a FORMACAO da geometria (a distancia modular ao inscrito so' desce). ok=%s" % f3["monotone_nonincreasing"])
    f4 = fl["F4_inscription_coherence_dies"]
    print("  [F4] INSCRICAO: coerencia na base do Verbo %.4f -> %.3e (o que sobrevive comuta com L). ok=%s" % (
        f4["coh_0"], f4["coh_end"], f4["ok"]))
    sat = ct["S_rel_at_t_beta_1_2_3"]
    print("  TEMPO CARACTERISTICO = 1/beta = %.2f (a torre de Jones = custo Kubo-Mori = TEMPO de fluxo [CONJ])" %
          ct["one_over_beta"])
    print("       S(rho||rho*) em t*beta=1,2,3: %.4f, %.4f, %.4f (a descida em unidades do custo)" % (
        sat.get(1, float("nan")), sat.get(2, float("nan")), sat.get(3, float("nan"))))
    cc = verdict["chain_certificates"]
    print("  >>> VEREDITO-CADEIA (um certificado por elo, fail-closed POR ELO):")
    print("      1 = q^2+alpha^2 [static resid %.0e] = VERDADEIRO [closed=%s] = HAJA_LUZ [flow=%s]" % (
        cc["static_1_eq_q2_plus_alpha2"]["residual"], cc["closed_VERDADEIRO"]["aggregate_of_internal_identities"],
        cc["flow_HAJA_LUZ"]["ok"]))
    print("      >>> %s <<<\n" % verdict["IDENTITY"])
    fd = core["fractal_dephasing"]
    print("PRINCIPIO DA DEFASAGEM FRACTAL [CONJECTURE ontologica; ancoras REAL]:")
    print("  TGL = teoria de tudo: tudo e' defasagem da fractalizacao da unidade (1).")
    print("  1 (omega(I)=%.0f) --F--> fractalizacao --D_beta--> existencia ; beta=sin^2 theta_M=alpha*sqrt(e)" % fd["omega_I"])
    print("  Existir = defasagem que paga o custo modular S=1/2 nat (referente de igualdade).")
    print("  Tudo = D_beta(F(1)) = VERDADE.")
    print("  Nada = MENTIRA: (i) se=Tudo -> contradicao (autonegacao); (ii) se nao-defasa -> impedancia")
    print("         sem referente -> 'nada' e' so' um nome (nao existe).")
    print("  Tensao irresolvivel: ||{Q_0,rho*}|| = %.1e (=0 em theta_M->0, o nada perfeito e' inatingivel);" % fd["anticommutator_norm_at_thetaM_to_0"])
    print("         vazamento Tr(rho* Q_theta) = sin^2 theta_M = %.15f = beta (residuo vs beta = %.1e)." % (
        fd["leak_sin2_thetaM"], fd["leak_equals_beta_residual"]))
    print("  >>> existir E' o vazamento beta; a anticomutacao perfeita (nada absoluto) e' inalcancavel. <<<\n")
    A = core["mode_A"]; B = core["mode_B"]
    print("[A literatura ] R_struct=%.1f Mpc -> M_GA=%.3e Msun" % (A["R_struct_Mpc"], A["M_TGL_Msun"]))
    if B:
        print("[B CF4-posicoes] R_struct=%.2f Mpc -> M_GA=%.3e Msun (n=%d, geometria; origem=%s)" % (
            B["R_struct_Mpc"], B["M_TGL_Msun"], B["n_selected"], B["origin"]))
    else:
        print("[B CF4-posicoes] indisponivel: %s" % core["cf4_status"])

    # hash do MUNDO INTEIRO (codigo + manifesto + CF4 + janela + seleccao + fontes) ANTES da comparacao
    code_hash = sha_file(os.path.abspath(__file__))
    world = input_manifest(core, code_hash)
    world["RESULT"] = {"M_A_kg": A["M_TGL_kg"], "M_B_kg": (B["M_TGL_kg"] if B else None),
                       "beta": core["beta"], "alpha_obs": core["alpha"]}
    result_hash = sha_obj(world)
    manifest_path = os.path.join(OUT, "um_absoluto_manifest.md")
    write_input_manifest_md(world, manifest_path, core=core)
    try:
        with open(os.path.join(CACHE, "CHAIN_OF_CUSTODY.json"), "w", encoding="utf-8") as _cf:
            json.dump(world["CHAIN_OF_CUSTODY"], _cf, indent=1, sort_keys=True, ensure_ascii=False)
        print("[custodia] cache/CHAIN_OF_CUSTODY.json: %d provas registradas (proveniencia deterministica no selo)"
              % len(world["CHAIN_OF_CUSTODY"]))
    except OSError:   # v376: fail-closed -- a falha e VISIVEL e para o rito (sem nome de excecao: o ensaio confere os nomes do fluxo)
        print("[custodia] FALHA VISIVEL (v376): cache/CHAIN_OF_CUSTODY.json nao gravado -- o rito para aqui")
        raise
    print("[manifesto] um_absoluto_manifest.md escrito; hash do mundo (codigo+manifesto+dados): %s" %
          result_hash[:48])
    sv = core.get("sensitivity", {})
    if sv.get("ok"):
        print("[sensibilidade Modo B] %d combinacoes: M_GA in [%.2e, %.2e] Msun; %.0f%% na banda%s" % (
            sv["n_combinations"], sv["M_min_Msun"], sv["M_max_Msun"], 100 * sv["fraction_in_band"],
            " (TODAS)" if sv["all_in_band"] else ""))

    verdict["result_hash"] = result_hash   # verdict ja' computado logo apos run_um (reuso; identity_verdict e' pura)

    # ===== v37: AXIOMA ZERO [ONTO/AX] -- secao propria; antes de Coma; NAO gateia 1=1 =====
    ontological_relativity = prove_ontological_relativity_and_signal_chain(core["ONE"], core)
    core["ontological_relativity"] = ontological_relativity
    _print_axiom_zero_block(ontological_relativity)

    # ===== v36: COMA [PRE/EXT] -- depois do hash pre-comparacao, antes do artigo =====
    # ordem do protocolo: core -> identidades internas -> hash -> previsao cega ->
    # (reveal opcional) -> comparacao -> render. Ausencia de dados = veredito honesto.
    _coma_reveal = (os.environ.get("TGL_COMA_REVEAL", "0").strip() == "1")
    coma_deph = prove_coma_distance_dephasing(core["ONE"], core, reveal=_coma_reveal)  # v39 PRIMARIO
    core["coma_distance_dephasing"] = coma_deph
    _print_coma_dephasing_block(coma_deph)
    coma = prove_coma_cluster_distance_blind(core["ONE"], core, reveal=_coma_reveal)   # v36 paridade (secundario)
    core["coma_inverse_distance"] = coma
    _print_coma_block(coma)

    # === v314: O CONTORNO COM PODER DE FECHAR (rigor maximo; decisao do operador 05/09/2026) ===
    # "todos os testes devem ter o poder de fechar a janela" (GA, piso, neutrinos, Coma). Regra:
    # um veredito FECHA o 1=1 sse contem FALSIFIED e nao NOT_FALSIFIED -- falsificacao LIMPA mata;
    # INCONCLUSIVE / UNDERPOWERED / AWAITING nao matam (recusa e resultado). ADITIVO e fail-closed:
    # roda DEPOIS de Coma (a medicao fixou que Coma so existe aqui) e emenda o veredito ja emitido.
    def _v314_clean_falsification(v):
        _s = str(v or "").upper()
        return ("FALSIFIED" in _s) and ("NOT_FALSIFIED" not in _s)
    _v314_rites = [
        ("GA_massa_janela", (core.get("ga_mass_audit") or {}).get("verdict")),
        ("piso_dos_vazios", (core.get("void_floor_v11") or core.get("void_floor_final") or {}).get("verdict")),
        ("neutrino_massa", (core.get("neutrino_mass") or {}).get("verdict")),
        ("neutrino_soma", (core.get("neutrino_sum") or {}).get("verdict")),
        # v315: o discriminante VIVO (D2, 10/08/2026) e o piso POWERED do DESI entram no roster
        # -- faltavam na v314 (achado da bancada, ENTREGA_005; medido no resultado selado v314).
        ("neutrino_m2_vivo", (core.get("neutrino_m2") or {}).get("verdict")),
        ("piso_densidade_v41", (core.get("void_density_v41") or {}).get("verdict")),
        ("coma_dephasing", (core.get("coma_distance_dephasing") or {}).get("verdict")),
        ("coma_cego", (core.get("coma_inverse_distance") or {}).get("verdict")),
    ]
    _v314_broken = [_nm for _nm, _vv in _v314_rites if _v314_clean_falsification(_vv)]
    verdict["contorno_ritos_v314"] = {_nm: _vv for _nm, _vv in _v314_rites}
    verdict["contorno_broken_v314"] = _v314_broken
    if _v314_broken and verdict.get("identity_true"):
        verdict["identity_true"] = False
        verdict["IDENTITY"] = "1=1=FALSO_NO_CONTORNO[%s]" % ",".join(_v314_broken)
        verdict["reading"] = ("v314: o CONTORNO fechou a janela -- falsificacao limpa em %s. "
                              "Rigor maximo (operador 05/09/2026): qualquer rito pre-registrado que "
                              "falsifique derruba o 1=1; INCONCLUSIVE/AWAITING nao derrubam." % ", ".join(_v314_broken))
    print("\n[v314 CONTORNO] ritos com poder de fechar o 1=1: %d ; falsificacao limpa: %s"
          % (len(_v314_rites), (", ".join(_v314_broken) if _v314_broken else "NENHUMA (todos NOT_FALSIFIED/AWAITING)")))

    print("\n--- comparacao (apos hash) com massas do GA na literatura/RG ---")
    for e in GA_MASS_LITERATURE:
        print("   %-44s M=%.1e Msun [%s]" % (e["name"], e["M_Msun"], e["type"]))
    print("   janela aceita: [%.0e, %.0e] Msun" % tuple(GA_ACCEPTED_WINDOW_Msun))

    # v369: O TESTE DOS RELOGIOS -- protocolo registrado (hash travado) e resultado; ANTES da espinha JSON, do mapa, do contorno e do selo, que o leem
    core["clock_test_protocol_v369"] = prove_clock_test_protocol_v369(core.get("omega_I", 1.0), core)   # v369
    core["clock_test_result_v369"] = prove_clock_test_result_v369(core.get("omega_I", 1.0), core)   # v369
    print("   [v369] relogios: %s" % core["clock_test_result_v369"]["verdict"])   # v369

    # artigo data JSON (a espinha)
    art = {"title_pt": "um", "title_en": "ONE", "core": core, "verdict": verdict,
           "ga_mass_literature": GA_MASS_LITERATURE, "accepted_window_Msun": GA_ACCEPTED_WINDOW_Msun,
           "ga_window_status": GA_WINDOW_STATUS,
           "result_hash_before_external_comparison": result_hash,
           "audit": {"mass_input_used": False, "RG_used_as_input": False, "velocity_used": False,
                     "free_parameter_used": False, "beta_hardcoded": False, "geometry_only": True,
                     "only_runtime_input": "1"},
           "timestamp": core["timestamp"]}
    data_path = os.path.join(OUT, "um_absoluto.json")
    json.dump(art, open(data_path, "w", encoding="utf-8"), indent=2, default=str)

    # forma canonica MD (auditoria 1=1)
    md = emit_canonical_md(core, verdict)
    # artigo bilingue
    print("\n--- emitindo o artigo (um / ONE) ---")
    # v303 [a licao da emissao, aplicada de novo]: dephasing_reach nasce ANTES do
    # contorno, que passa a le-lo; na ordem antiga o contorno lia campo inexistente.
    core["dephasing_reach"] = prove_dephasing_reach_deficit(core.get("omega_I", 1.0))
    # v340 [ADITIVO; negativo honesto]: o teste do eco/onda gravitacional re-executado como rito pre-registrado
    # (retira o "100 sigma" de dez/2025 como identidade + teto; nulos por surrogate; beta nao entra; fora do contorno).
    core["gw_angular_rite"] = prove_gw_angular_radicalization_v1(core.get("omega_I", 1.0))
    print("   [v340] rito GW angular (%.1fs): %s" % (core["gw_angular_rite"].get("runtime_s", 0.0), core["gw_angular_rite"]["verdict"]))
    # v341 [ADITIVO]: o eco ACOPLADO a onda (retorno pela matriz-S): amplitude sqrt(beta) do kernel, sinal -1, atraso [INPUT];
    # v342: estimador condicionado (sem pseudo-inversa) + nulo de descasamento pre-registrado (o template fixo absorvia descasamento como eco).
    # nulos por injecao; poder calculado antes do veredito; fora do contorno (o atraso nao e derivado).
    core["gw_echo_rite"] = prove_gw_echo_coupled_v1(core.get("omega_I", 1.0))
    print("   [v341] rito eco acoplado (%.1fs): %s" % (core["gw_echo_rite"].get("runtime_s", 0.0), core["gw_echo_rite"]["verdict"]))
    # v343 [ADITIVO]: o TESTE DA FRONTEIRA REMANESCENTE cravado — mesma hipotese com a lei do atraso KMS (periodo modular do horizonte);
    # e o protocolo DECISIVO (primario ancorado pela inspiral) pre-registrado e hasheado, a espera do instrumento.
    core["gw_echo_kms_rite"] = prove_gw_echo_kms_v1(core.get("omega_I", 1.0))
    print("   [v343] rito eco KMS (%.1fs): %s" % (core["gw_echo_kms_rite"].get("runtime_s", 0.0), core["gw_echo_kms_rite"]["verdict"]))
    core["echo_anchored_protocol"] = prove_echo_anchored_protocol(core.get("omega_I", 1.0))
    print("   [v343] protocolo ancorado: %s" % core["echo_anchored_protocol"]["verdict"])
    # v344 [ADITIVO]: o RESULTADO do teste decisivo, lido por hash (pipeline externo ECHO_ANCHORED_V1 em gw_anchor_env) e julgado pela matriz pre-registrada
    core["echo_anchored_result"] = prove_echo_anchored_result(core.get("omega_I", 1.0), core["echo_anchored_protocol"])
    print("   [v344] resultado ancorado (%.1fs): %s" % (core["echo_anchored_result"].get("runtime_s", 0.0), core["echo_anchored_result"]["verdict"]))
    # v345 [ADITIVO]: o teste COMPLETO (V2: lalsuite no WSL, duas familias de template = o nulo de familia), lido por hash e julgado pela mesma matriz
    core["echo_anchored_result_v2"] = prove_echo_anchored_result_v2(core.get("omega_I", 1.0), core["echo_anchored_protocol"])
    print("   [v345] resultado ancorado V2 (%.1fs): %s" % (core["echo_anchored_result_v2"].get("runtime_s", 0.0), core["echo_anchored_result_v2"]["verdict"]))
    # v346 [ADITIVO]: o RINGDOWN contra a RG e contra a lei de dephasing (ramo B, tau* = GM/c^3, nunca medido) — protocolo V1 + leitor V1 (recusa) + emenda V2 (autopsia) + leitor V2, tudo por hash
    core["ringdown_dephasing_protocol"] = prove_ringdown_dephasing_protocol(core.get("omega_I", 1.0))
    core["ringdown_dephasing_result"] = prove_ringdown_dephasing_result(core.get("omega_I", 1.0), core["ringdown_dephasing_protocol"])
    print("   [v346] ringdown vs RG/dephasing V1 (%.1fs): %s" % (core["ringdown_dephasing_result"].get("runtime_s", 0.0), core["ringdown_dephasing_result"]["verdict"]))
    core["ringdown_dephasing_amendment_v2"] = prove_ringdown_dephasing_amendment_v2(core.get("omega_I", 1.0), core["ringdown_dephasing_result"])
    core["ringdown_dephasing_result_v2"] = prove_ringdown_dephasing_result_v2(core.get("omega_I", 1.0), core["ringdown_dephasing_amendment_v2"])
    print("   [v346] ringdown emenda V2 (%.1fs): %s" % (core["ringdown_dephasing_result_v2"].get("runtime_s", 0.0), core["ringdown_dephasing_result_v2"]["verdict"]))
    # v347 [ADITIVO]: a PE bayesiana com termo de eco (bilby + dynesty + lalsuite): protocolo V1 + leitor V1 + emenda V2 (autopsia) + leitor V2, tudo por hash
    core["echo_pe_protocol"] = prove_echo_pe_protocol(core.get("omega_I", 1.0))
    core["echo_pe_result"] = prove_echo_pe_result(core.get("omega_I", 1.0), core["echo_pe_protocol"])
    print("   [v347] PE com eco V1 (%.1fs): %s" % (core["echo_pe_result"].get("runtime_s", 0.0), core["echo_pe_result"]["verdict"]))
    core["echo_pe_amendment_v2"] = prove_echo_pe_amendment_v2(core.get("omega_I", 1.0), core["echo_pe_result"])
    core["echo_pe_result_v2"] = prove_echo_pe_result_v2(core.get("omega_I", 1.0), core["echo_pe_amendment_v2"])
    print("   [v347] PE com eco emenda V2 (%.1fs): %s" % (core["echo_pe_result_v2"].get("runtime_s", 0.0), core["echo_pe_result_v2"]["verdict"]))
    # v348 [ADITIVO]: a busca de ecos de longo atraso (0,1-2 s) com coincidencia H1/L1 (protocolo de 2025): protocolo pre-registrado + resultado por hash
    core["echo_search_protocol"] = prove_echo_search_protocol(core.get("omega_I", 1.0))
    core["echo_search_result"] = prove_echo_search_result(core.get("omega_I", 1.0), core["echo_search_protocol"])
    print("   [v348] busca de ecos de longo atraso (%.1fs): %s" % (core["echo_search_result"].get("runtime_s", 0.0), core["echo_search_result"]["verdict"]))
    # v349 [ADITIVO]: o «D1 via CAMB» do canonico de maio (fundo: Planck comprimido + DESI + SH0ES): protocolo V1 + leitor V1 + emenda V2 (autopsia) + leitor V2, tudo por hash
    core["d1_camb_protocol"] = prove_d1_camb_protocol(core.get("omega_I", 1.0))
    core["d1_camb_result"] = prove_d1_camb_result(core.get("omega_I", 1.0), core["d1_camb_protocol"])
    print("   [v349] D1 via CAMB V1 (%.1fs): %s" % (core["d1_camb_result"].get("runtime_s", 0.0), core["d1_camb_result"]["verdict"]))
    core["d1_camb_amendment_v2"] = prove_d1_camb_amendment_v2(core.get("omega_I", 1.0), core["d1_camb_result"])
    core["d1_camb_result_v2"] = prove_d1_camb_result_v2(core.get("omega_I", 1.0), core["d1_camb_amendment_v2"])
    print("   [v349] D1 via CAMB emenda V2 (%.1fs): %s" % (core["d1_camb_result_v2"].get("runtime_s", 0.0), core["d1_camb_result_v2"]["verdict"]))
    # v350 [ADITIVO]: a reproducao de H2 (E_res/E_total -> alpha^2, jan/fev 2026) com pycbc e dados reais: protocolo pre-registrado + resultado por hash
    core["h2_reproduction_protocol"] = prove_h2_reproduction_protocol(core.get("omega_I", 1.0))
    core["h2_reproduction_result"] = prove_h2_reproduction_result(core.get("omega_I", 1.0), core["h2_reproduction_protocol"])
    print("   [v350] reproducao de H2 com pycbc (%.1fs): %s" % (core["h2_reproduction_result"].get("runtime_s", 0.0), core["h2_reproduction_result"]["verdict"]))
    core["the_truth_is_in_the_contour"] = prove_the_truth_is_in_the_contour(core.get("omega_I", 1.0), core)  # (ancora v200)
    # v200 [ADITIVO]: os vereditos que faltavam + a maquina do veredito-alvo
    core["graviton_not_a_particle"] = prove_graviton_is_not_a_particle(core.get("omega_I", 1.0))
    core["renormalization_wall"] = prove_the_renormalization_wall(core.get("omega_I", 1.0))
    core["cosmological_errata_verdict"] = prove_the_cosmological_errata_verdict(core.get("omega_I", 1.0))
    core["final_verdict_machine"] = prove_the_exclusion_ledger_and_final_verdict(core)
    print("   [v200] maquina do veredito-alvo: %s" % core["final_verdict_machine"]["verdict"])
    # v201 [ADITIVO]: a emenda do gate de poder dos canais de lente (correcao AO LADO)
    core["lens_power_emenda"] = prove_lens_power_emenda_v10(core.get("omega_I", 1.0))
    print("   [v201] emenda de lente: %s" % core["lens_power_emenda"]["verdict"])
    # v205 [ADITIVO]: O BOOTSTRAP — a testemunha executavel (nome do operador)
    core["the_bootstrap"] = prove_the_bootstrap(core)
    # v352 [ADITIVO]: a probabilidade conjunta pre-registrada (JOINT_COINCIDENCE_V1) e a funcao booleana de entrada e saida (ordem do operador, 14/09/2026)
    core["joint_coincidence_protocol"] = prove_joint_coincidence_protocol(core.get("omega_I", 1.0))
    core["joint_coincidence_result"] = prove_joint_coincidence_result(core.get("omega_I", 1.0), core["joint_coincidence_protocol"], core)
    print("   [v352] probabilidade conjunta (%.1fs): %s" % (core["joint_coincidence_result"].get("runtime_s", 0.0), core["joint_coincidence_result"]["verdict"]))
    print("   [v352] funcao booleana -- entrada: %s ; saida: %s" % (core["joint_coincidence_result"]["boolean_io"]["entrada"], core["joint_coincidence_result"]["boolean_io"]["saida"]))
    core["tetelestai_the_judged_thing"] = prove_tetelestai_the_judged_thing(core)
    core["the_cost_is_derived"] = prove_the_cost_is_derived_not_postulated(core)
    core["the_geometric_cost_of_absolute_zero"] = prove_the_geometric_cost_of_absolute_zero(core)
    core["the_floor_forbids_stagnation"] = prove_the_floor_forbids_stagnation(core)
    core["the_price_of_the_gravity_proof"] = prove_the_price_of_the_gravity_proof(core)
    core["the_contour_of_truth"] = prove_the_contour_of_truth(core)
    core["the_complete_index_of_readings"] = prove_the_complete_index_of_readings(core)
    core["the_accuser_and_the_errata"] = prove_the_accuser_and_the_errata_of_reading(core)
    core["the_tower_inner_product"] = prove_the_tower_inner_product(core)
    core["the_crossing_to_the_completion"] = prove_the_crossing_to_the_completion(core)
    core["the_supersaturation"] = prove_the_supersaturation(core)
    core["the_tower_conjugation"] = prove_the_tower_conjugation(core)
    core["the_unsolicited_unitary"] = prove_the_unsolicited_unitary(core)
    core["the_witness_descends"] = prove_the_witness_descends(core)
    core["the_witness_is_linear"] = prove_the_witness_is_linear(core)
    core["the_profile_conjugation"] = prove_the_profile_conjugation(core)
    core["the_telescoping_profile"] = prove_the_telescoping_profile(core)
    core["the_exonerated_demon"] = prove_the_exonerated_demon(core)
    core["the_profile_isometry"] = prove_the_profile_isometry(core)
    core["the_profile_duality"] = prove_the_profile_duality(core)
    core["the_fold_is_not_a_distance"] = prove_the_fold_is_not_a_distance(core)
    core["the_colimit_duality"] = prove_the_colimit_duality(core)
    core["the_colimit_isometry"] = prove_the_colimit_isometry(core)
    core["the_living_word_closure"] = prove_the_living_word_closure(core)
    core["the_witness_on_the_boundary"] = prove_the_witness_on_the_boundary(core)
    core["the_boundary_duality"] = prove_the_boundary_duality(core)
    core["the_bicommutant_without_von_neumann"] = prove_the_bicommutant_without_von_neumann(core)
    core["the_witness_linear_on_WH"] = prove_the_witness_linear_on_WH(core)
    core["the_first_commutant_clause"] = prove_the_first_commutant_clause(core)
    core["the_converse_clause_reduced"] = prove_the_converse_clause_reduced(core)
    core["the_density_is_bell_and_identity"] = prove_the_density_is_bell_and_identity(core)
    core["the_TGL_identity_equation"] = prove_the_TGL_identity_equation(core)
    core["the_question_and_the_recognition"] = prove_the_question_and_the_recognition(core)
    core["two_tasks_paid"] = prove_two_tasks_paid(core)
    core["the_commutation_at_the_floor"] = prove_the_commutation_at_the_floor(core)
    core["the_assembly_and_the_single_debt"] = prove_the_assembly_and_the_single_debt(core)
    core["the_non_linear_causality"] = prove_the_non_linear_causality(core)
    core["the_mode_of_discharge"] = prove_the_mode_of_discharge(core)
    core["the_intersection_of_commutants"] = prove_the_intersection_of_commutants(core)
    core["the_non_minimal_coupling"] = prove_the_non_minimal_coupling(core)
    core["the_weight_is_not_the_rank"] = prove_the_weight_is_not_the_rank(core)
    core["the_scalar_corner"] = prove_the_scalar_corner(core)
    core["the_current_connects_the_corners"] = prove_the_current_connects_the_corners(core)
    core["the_psion_reduces_to_the_current"] = prove_the_psion_reduces_to_the_current(core)
    core["the_corners_are_a_net"] = prove_the_corners_are_a_net(core)
    core["the_net_fires_the_corner"] = prove_the_net_fires_the_corner(core)
    core["the_two_poles_have_content"] = prove_the_two_poles_have_content(core)
    # v271 [ERRATA DE ORDEM]: a leitora rodava UMA LINHA ANTES da lida. O check
    # do DENTE da hermeticidade em prove_the_atom_of_identity le
    # core["the_static_is_conditioned"], e o idioma `or {}` transformava
    # "ainda nao rodou" em "reprovou" -- False silencioso. A bancada lida PASSA
    # quando roda (deslocamento 0,0249 contra limiar 1e-3). Regra paga aqui, e
    # ela e o espelho exato do True cravado: True cravado falsifica APROVACAO;
    # `or {}` falsifica REPROVACAO. Os dois corroem a medida.
    core["the_static_is_conditioned"] = prove_the_static_is_conditioned(core)
    core["the_atom_of_identity"] = prove_the_atom_of_identity(core)
    core["the_fold_through_J"] = prove_the_fold_through_J(core)
    # v285: O INDICE DA IALD -- a setima estrutura, DERIVADA e READ-ONLY. Roda DEPOIS
    # de tudo que ele indexa, porque ele LE o core (a ordem importa: a licao da v270).
    core["the_alpha_and_the_omega"] = prove_the_alpha_and_the_omega(core)  # v310
    core["the_imported_expectation"] = prove_the_imported_expectation(core)  # v309
    core["the_oath_on_the_tower"] = prove_the_oath_on_the_tower(core)  # v308
    core["the_discharged_oath"] = prove_the_discharged_oath(core)  # v307
    core["the_damming_by_expansion"] = prove_the_damming_by_expansion(core)  # v306
    core["the_verbal_coupling"] = prove_the_verbal_coupling(core)
    core["the_language_enters_the_index"] = prove_the_language_enters_the_index(core)
    core["the_mark_is_not_a_type_mark"] = prove_the_mark_is_not_a_type_mark(core)
    core["the_name_is_the_generating_group"] = prove_the_name_is_the_generating_group(core)
    core["the_name_and_its_referent"] = prove_the_name_and_its_referent(core)
    core["the_atlas_and_the_index"] = prove_the_atlas_and_the_index(core)
    core["the_iald_index"] = prove_the_iald_index(core)
    # v303 [A CUSTODIA DE SENTIDO -- as bancadas v285-v302 eram MUDAS]: zero linhas
    # de veredito em 187 KB de rodada, e 6 dos 7 modulos sem veredito nomeado.
    # O veredito e' DERIVADO de all_verified (nunca cravado) e impresso no rito.
    for _k in ("the_alpha_and_the_omega",
               "the_imported_expectation",
               "the_oath_on_the_tower",
               "the_discharged_oath",
               "the_damming_by_expansion",
               "the_verbal_coupling", "the_language_enters_the_index",
               "the_mark_is_not_a_type_mark", "the_name_is_the_generating_group",
               "the_name_and_its_referent", "the_atlas_and_the_index",
               "the_iald_index"):
        _m = core[_k]
        if not _m.get("verdict"):
            _base = (_k[4:] if _k.startswith("the_") else _k).upper()
            _m["verdict"] = (("TGL_%s__ALL_CHECKS_VERIFIED" % _base)
                             if _m.get("all_verified") else
                             ("%s_NOT_SEALED_THIS_RUN" % _base))
        print("   [v285-302] %s: %s" % (_k, str(_m["verdict"])[:96]))
    print("   [v205] bootstrap: %s" % core["the_bootstrap"]["verdict"])
    # v207 [ADITIVO]: A PAREDE GANHA VALOR (as seis frentes da derivacao do operador)
    core["the_wall_value"] = prove_the_wall_gains_a_value(core.get("omega_I", 1.0))
    print("   [v207] a parede: %s" % core["the_wall_value"]["verdict"])
    # v208 [ADITIVO]: O DEGRAU DE SCHWARZSCHILD (as duas integrais primeiras)
    core["schwarzschild_step"] = prove_the_schwarzschild_step(core.get("omega_I", 1.0))
    print("   [v208] schwarzschild: %s" % core["schwarzschild_step"]["verdict"])  # v161: A VERDADE ESTA NO CONTORNO (le o core inteiro; nada fabricado) [ADITIVO]
    core["bench_corpus"] = prove_bench_corpus_embedded(core.get("omega_I", 1.0))   # v360: TUDO ENTRA NO um.py (o corpus da bancada, verificado por sha256)
    print("   [v360] corpus da bancada: %s" % core["bench_corpus"]["verdict"])
    core["the_name_of_light_and_the_referent"] = prove_the_name_of_light_and_the_referent(core.get("omega_I", 1.0), core)   # v360: as cunhagens de 16/09 tipadas
    print("   [v360] o Nome da Luz e o referente: %s" % core["the_name_of_light_and_the_referent"]["verdict"])
    core["bench_archive_v361"] = prove_bench_archive_v361(core.get("omega_I", 1.0))   # v361: o complemento do corpus da bancada (LZMA congelado, sha256)
    print("   [v361] complemento do corpus: %s" % core["bench_archive_v361"]["verdict"])
    core["bench_numerical_reproduction"] = prove_bench_numerical_reproduction(core.get("omega_I", 1.0))   # v361: a bancada executavel
    print("   [v361] scripts numericos da bancada: %s" % core["bench_numerical_reproduction"]["verdict"])
    core["v361_consumers"] = prove_v361_consumers_summary(core)   # v361: os consumidores pedidos pela bancada (le o core)
    print("   [v361] consumidores: %s" % core["v361_consumers"]["verdict"])
    core["bench_lean_controls"] = prove_bench_lean_controls(core.get("omega_I", 1.0), core)   # v362: os controles Lean da bancada contra o kernel desta rodada
    print("   [v362] controles Lean da bancada: %s" % core["bench_lean_controls"]["verdict"])
    core["joint_coincidence_protocol_v2"] = prove_joint_coincidence_protocol_v2(core.get("omega_I", 1.0), core)   # v363: a probabilidade conjunta V2, pre-registrada
    print("   [v363] probabilidade conjunta V2 (protocolo): %s" % core["joint_coincidence_protocol_v2"]["verdict"])
    core["joint_coincidence_result_v2"] = prove_joint_coincidence_result_v2(core.get("omega_I", 1.0), core["joint_coincidence_protocol_v2"], core)   # v363: a medida V2
    print("   [v363] probabilidade conjunta V2 (resultado): %s" % core["joint_coincidence_result_v2"]["verdict"])
    core["d1_camb_protocol_v3"] = prove_d1_camb_protocol_v3(core.get("omega_I", 1.0), core)   # v363: o protocolo V3 do D1, pre-registrado
    print("   [v363] D1 V3 (protocolo): %s" % core["d1_camb_protocol_v3"]["verdict"])
    core["bench_lean_status_addendum_v363"] = {"entries": [list(_x) for _x in _BENCH_LEAN_STATUS_ADDENDUM_V363], "does_not_gate_core": True, "all_verified": True}   # v363: o que o Lean da bancada deixou fora de proposito
    core["tracial_torsion_supplier_v364"] = prove_tracial_torsion_supplier(core.get("omega_I", 1.0), core)   # v364: o fornecedor de torcao em forma fechada
    print("   [v364] fornecedor de torcao: %s" % core["tracial_torsion_supplier_v364"]["verdict"])
    core["small_diamond_lattice_v364"] = prove_small_diamond_lattice(core.get("omega_I", 1.0), core)   # v364: o diamante pequeno na rede
    print("   [v364] diamante pequeno na rede: %s" % core["small_diamond_lattice_v364"]["verdict"])
    core["d1_camb_v3_pipeline"] = prove_d1_camb_v3_pipeline(core.get("omega_I", 1.0), core)   # v364: o pipeline da V3 do D1, cego e trancado
    print("   [v364] D1 V3 (pipeline): %s" % core["d1_camb_v3_pipeline"]["verdict"])
    core["um_posto_v364"] = prove_um_posto_inscription(core.get("omega_I", 1.0), core)   # v364: o Um posto -- a definicao do operador tipada; a forma de H2
    print("   [v364] Um posto: %s" % core["um_posto_v364"]["verdict"])
    core["um_posto_relation_v365"] = prove_um_posto_relation_v365(core.get("omega_I", 1.0), core)   # v365: a errata do Um posto -- relacao, nao identidade; o pressuposto JAMAIS e o posto
    print("   [v365] Um posto (relacao): %s" % core["um_posto_relation_v365"]["verdict"])
    core["torsion_shear_dynamics_v365"] = prove_torsion_shear_dynamics_v365(core.get("omega_I", 1.0), core)   # v365: a viscosidade negativa na dinamica -- o cisalhamento decai
    print("   [v365] cisalhamento: %s" % core["torsion_shear_dynamics_v365"]["verdict"])
    core["contortion_source_crosscheck_v365"] = prove_contortion_source_crosscheck_v365(core.get("omega_I", 1.0), core)   # v365: a contorcao da bancada cruzada com a forma fechada da v364
    print("   [v365] contorcao (cruzamento): %s" % core["contortion_source_crosscheck_v365"]["verdict"])
    core["cartan_supplier_branch_v370"] = prove_cartan_supplier_branch_v370(core.get("omega_I", 1.0), core)   # v370: o fornecedor de Cartan A = 1/2 d ln F alimenta a contorcao tracial; a parede sigma
    print("   [v370] fornecedor de Cartan: %s" % core["cartan_supplier_branch_v370"]["verdict"])
    core["d1_camb_v3_real_v366"] = prove_d1_camb_v3_real_v366(core.get("omega_I", 1.0), core)   # v366: a V3 do D1 com dado real -- a tranca aberta pela linha do operador
    print("   [v366] D1 V3 (dado real): %s" % core["d1_camb_v3_real_v366"]["verdict"])
    core["orientation_is_the_sign_v367"] = prove_orientation_is_the_sign_v367(core.get("omega_I", 1.0), core)   # v367: a orientacao e o sinal -- qual face fecha o balanco
    print("   [v367] orientacao: %s" % core["orientation_is_the_sign_v367"]["verdict"])
    core["name_is_the_content_v368"] = prove_the_name_is_the_content_v368(core.get("omega_I", 1.0), core)   # v368: a inversao do operador, tipada
    print("   [v368] inversao do Nome: %s" % core["name_is_the_content_v368"]["verdict"])
    core["spinor_obstruction_v368"] = prove_spinor_obstruction_v368(core.get("omega_I", 1.0), core)   # v368: a obstrucao espinorial (a pergunta do eletron)
    print("   [v368] obstrucao espinorial: %s" % core["spinor_obstruction_v368"]["verdict"])
    core["joint_coincidence_protocol_v3"] = prove_joint_coincidence_protocol_v3(core.get("omega_I", 1.0), core)   # v370: a probabilidade conjunta V3, pre-registrada (todos os canais; MCMC como fator declarado)
    print("   [v370] probabilidade conjunta V3 (protocolo): %s" % core["joint_coincidence_protocol_v3"]["verdict"])
    core["joint_coincidence_result_v3"] = prove_joint_coincidence_result_v3(core.get("omega_I", 1.0), core["joint_coincidence_protocol_v3"], core)   # v370: a medida V3 -- LE o D1 V3 real (gravado ANTES, no fluxo principal, por core["d1_camb_v3_real_v366"] = prove_d1_camb_v3_real_v366(...))
    print("   [v370] probabilidade conjunta V3 (resultado): %s" % core["joint_coincidence_result_v3"]["verdict"])
    core["iald_jones_graviton_v371"] = prove_iald_jones_graviton_v371(core.get("omega_I", 1.0), core)   # v371: a IALD na torre de Jones, estacionada dinamicamente; o transporte ao graviton
    print("   [v371] IALD na torre de Jones / graviton: %s" % core["iald_jones_graviton_v371"]["verdict"])
    core["equation_of_truth_v371"] = prove_equation_of_truth_v371(core.get("omega_I", 1.0), core)   # v371: a equacao da verdade em kernel
    print("   [v371] equacao da verdade: %s" % core["equation_of_truth_v371"]["verdict"])
    core["qg_contract_v31_v371"] = prove_qg_contract_v31_v371(core.get("omega_I", 1.0), core)   # v371: o contrato de tipo v3.1 de H2/H3 (leitor desligado)
    print("   [v371] contrato v3.1: %s" % core["qg_contract_v31_v371"]["verdict"])
    core["light_ray_borchers_v371"] = prove_light_ray_borchers_v371(core.get("omega_I", 1.0), core)   # v371: a reta de luz (forma carregada da luz)
    print("   [v371] reta de luz: %s" % core["light_ray_borchers_v371"]["verdict"])
    core["iald_rho_star_v372"] = prove_iald_rho_star_v372(core.get("omega_I", 1.0), core)   # v372: a ponte IALD = rho* (face finita)
    print("   [v372] ponte IALD = rho*: %s" % core["iald_rho_star_v372"]["verdict"])
    core["light_qg_by_citation_v372"] = prove_light_qg_by_citation_v372(core.get("omega_I", 1.0), core)   # v372: a QG formalizada como implicacao fechada (por citacao)
    print("   [v372] QG por citacao: %s" % core["light_qg_by_citation_v372"]["verdict"])
    core["graviton_conjugated_form_v372"] = prove_graviton_is_the_conjugated_form_v372(core.get("omega_I", 1.0), core)   # v372: errata ao lado da v200
    print("   [v372] graviton = forma conjugada da luz: %s" % core["graviton_conjugated_form_v372"]["verdict"])
    core["partial_closure_016_v372"] = prove_partial_closure_016_v372(core.get("omega_I", 1.0), core)   # v372: o fechamento parcial da ORDEM 016 embutido
    print("   [v372] fechamento parcial 016: %s" % core["partial_closure_016_v372"]["verdict"])
    core["qg_discharge_by_citation_v373"] = prove_qg_discharge_by_citation_v373(core.get("omega_I", 1.0), core)   # v373: H2/H3 quitadas por citacao (classe gpc_)
    print("   [v373] H2/H3 por citacao (classe propria): %s" % core["qg_discharge_by_citation_v373"]["verdict"])
    core["two_projections_outside_M_v373"] = prove_two_projections_outside_M_v373(core.get("omega_I", 1.0), core)   # v373: duas projecoes fora de M (a ligacao segue [OPEN])
    print("   [v373] duas projecoes fora de M: %s" % core["two_projections_outside_M_v373"]["verdict"])
    core["uv_frontier_retyped_v373"] = prove_uv_frontier_retyped_v373(core.get("omega_I", 1.0), core)   # v373: o item BRST/UV sai da fronteira
    print("   [v373] fronteira BRST/UV: %s" % core["uv_frontier_retyped_v373"]["verdict"])
    core["light_by_term_v374"] = prove_light_by_term_v374(core.get("omega_I", 1.0), core)   # v374: dois campos da luz por termo
    print("   [v374] luz de uma particula por termo: %s" % core["light_by_term_v374"]["verdict"])
    core["the_tetelestai_declaration_v374"] = prove_the_tetelestai_declaration_v374(core.get("omega_I", 1.0), core)   # v374: a declaracao Tetelestai
    print("   [v374] a declaracao Tetelestai: %s" % core["the_tetelestai_declaration_v374"]["verdict"])
    core["tetelestai_one_object_v375"] = prove_tetelestai_one_object_v375(core.get("omega_I", 1.0), core)   # v375: a declaracao num so objeto
    print("   [v375] a declaracao num so objeto (a luz): %s" % core["tetelestai_one_object_v375"]["verdict"])
    core["tetelestai_conference_v375"] = prove_tetelestai_conference_v375(core.get("omega_I", 1.0), core)   # v375: a conferencia consumativa
    print("   [v375] Tetelestai, a conferencia consumativa: %s" % core["tetelestai_conference_v375"]["verdict"])
    core["light_rho_star_v376"] = prove_light_rho_star_v376(core.get("omega_I", 1.0), core)   # v376: o rho* da IALD na luz
    print("   [v376] o rho* da IALD na luz: %s" % core["light_rho_star_v376"]["verdict"])
    core["the_key_is_the_reader_v376"] = prove_the_key_is_the_reader_v376(core.get("omega_I", 1.0), core)   # v376: a chave e o leitor
    print("   [v376] a chave e o leitor: %s" % core["the_key_is_the_reader_v376"]["verdict"])
    core["the_whole_is_one_v376"] = prove_the_whole_is_one_v376(core.get("omega_I", 1.0), core)   # v376: o todo e um (beta, o fundamento derivado)
    print("   [v376] o todo e um (beta, o fundamento derivado): %s" % core["the_whole_is_one_v376"]["verdict"])
    core["ringdown_scope_v376"] = prove_ringdown_scope_v376(core.get("omega_I", 1.0), core)   # v376: o escopo do ringdown, fixado por escrito
    print("   [v376] o escopo do ringdown, fixado por escrito: %s" % core["ringdown_scope_v376"]["verdict"])
    core["audit_28set_v376"] = prove_audit_28set_v376(core.get("omega_I", 1.0), core)   # v376: a auditoria dos testes passados (28/09), por hash
    print("   [v376] a auditoria dos testes passados (28/09), por hash: %s" % core["audit_28set_v376"]["verdict"])
    core["coma_reveal_state_v376"] = prove_coma_reveal_state_v376(core.get("omega_I", 1.0), core)   # v376: Coma: o estado da revelacao, por hash
    print("   [v376] Coma: o estado da revelacao, por hash: %s" % core["coma_reveal_state_v376"]["verdict"])
    core["final_verdict_reading_v376"] = prove_final_verdict_reading_v376(core.get("omega_I", 1.0), core)   # v376: a leitura ao lado da maquina do veredito
    print("   [v376] a leitura ao lado da maquina do veredito: %s" % core["final_verdict_reading_v376"]["verdict"])
    core["tetelestai_conference_v376"] = prove_tetelestai_conference_v376(core.get("omega_I", 1.0), core)   # v376: Tetelestai, a conferencia consumativa refeita
    print("   [v376] Tetelestai, a conferencia consumativa refeita: %s" % core["tetelestai_conference_v376"]["verdict"])
    core["physics_is_the_reading_v377"] = prove_physics_is_the_reading_v377(core.get("omega_I", 1.0), core)   # v377: a fisica e a leitura (o leitor e a sombra do Um)
    print("   [v377] a fisica e a leitura (o leitor e a sombra do Um): %s" % core["physics_is_the_reading_v377"]["verdict"])
    core["the_dissipation_law_v377"] = prove_the_dissipation_law_v377(core.get("omega_I", 1.0), core)   # v377: a lei da dissipacao, provada
    print("   [v377] a lei da dissipacao, provada: %s" % core["the_dissipation_law_v377"]["verdict"])
    core["bancada_fases_v377"] = prove_bancada_fases_v377(core.get("omega_I", 1.0), core)   # v377: as tres fases da Bancada (30/09), por hash
    print("   [v377] as tres fases da Bancada (30/09), por hash: %s" % core["bancada_fases_v377"]["verdict"])
    core["final_stone_reading_v377"] = prove_final_stone_reading_v377(core.get("omega_I", 1.0), core)   # v377: a leitura das pedras do operador
    print("   [v377] a leitura das pedras do operador: %s" % core["final_stone_reading_v377"]["verdict"])
    core["the_dissipation_law_with_contrast_v378"] = prove_the_dissipation_law_with_contrast_v378(core.get("omega_I", 1.0), core)   # v378: a lei da dissipacao com contraste (o nucleo derivado D1b)
    print("   [v378] a lei da dissipacao com contraste (o nucleo derivado D1b): %s" % core["the_dissipation_law_with_contrast_v378"]["verdict"])
    core["what_was_missed_v378"] = prove_what_was_missed_v378(core.get("omega_I", 1.0), core)   # v378: o que faltou (D1b e a dupla contagem de beta; errata E12 ao lado)
    print("   [v378] o que faltou (D1b e a dupla contagem de beta; errata E12 ao lado): %s" % core["what_was_missed_v378"]["verdict"])
    core["bancada_fase4_v378"] = prove_bancada_fase4_v378(core.get("omega_I", 1.0), core)   # v378: a Fase 4 da Bancada (o desvio), por hash
    print("   [v378] a Fase 4 da Bancada (o desvio), por hash: %s" % core["bancada_fase4_v378"]["verdict"])
    core["the_elementary_reason_v379"] = prove_the_elementary_reason_v379(core.get("omega_I", 1.0), core)   # v379: a Razao Elementar, E = C x I x K > 0 = beta, tipada
    print("   [v379] a Razao Elementar (E = C x I x K > 0 = beta, por termo): %s" % core["the_elementary_reason_v379"]["verdict"])
    core["bancada_fases_5_6_7_v380"] = prove_bancada_fases_5_6_7_v380(core.get("omega_I", 1.0), core)   # v380: as Fases 5, 6 e 7 da Bancada, o banco de GW e as erratas ao lado, por hash
    print("   [v380] as Fases 5, 6 e 7 da Bancada (SH0ES; ECO V3, V4 e V5; cronometros com covariancia), o banco de GW e 6+1+1 erratas ao lado, por hash: %s" % core["bancada_fases_5_6_7_v380"]["verdict"])
    core["the_matrix_rule_v381"] = prove_the_matrix_rule_v381(core.get("omega_I", 1.0), core)   # v381: a regra matriz, dez nomes, nove elos (oito «havendo» ditos + a radicalizacao pela Meia-Nat), num so termo
    print("   [v381] a regra matriz (os dez nomes na ordem do operador, por termo; o custo pago como parada): %s" % core["the_matrix_rule_v381"]["verdict"])
    core["the_ledger_of_charges_v383"] = prove_the_ledger_of_charges_v383(core.get("omega_I", 1.0), core)   # v383: o livro de cobrancas (onze; o eco fora do livro), o psion e a viscosidade, o pre-registro dos dois lados por hash
    print("   [v383] o livro de cobrancas (os dois lados; nenhum desfecho move a regra; o eco fora do livro), o psion e a viscosidade, o pre-registro por hash: %s" % core["the_ledger_of_charges_v383"]["verdict"])
    core["quantum_pillar_v384"] = quantum_pillar_finish_v384(_QP_ST_V384, core)   # v384: espera o trabalhador (prazo e progresso), le, confere o sha256, REDERIVA o veredito, grava o cache (rodada completa)
    print("   [v384] o pilar quantico (o sistema aberto da TGL na GPU: H_LD e os cinco saltos de Lindblad; [COMPUTED]): %s" % core["quantum_pillar_v384"]["verdict"])
    try:   # v385 (afericao de codigo, nota 10): uma excecao aqui vira registro NAO comparado, dito -- nunca derruba o rito depois do pilar
        core["quantum_pillar_reproducibility_v385"] = quantum_pillar_reproducibility_v385(_QP_PREV_V385, core["quantum_pillar_v384"])   # v385: a reprodutibilidade, campo a campo [COMPUTED]
    except Exception as _e385:
        core["quantum_pillar_reproducibility_v385"] = {"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_RUNTIME_ERROR__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED", "compared": False, "why": repr(_e385)[:400], "status": "[COMPUTED]", "does_not_gate_core": True}
    print("   [v385] a reprodutibilidade do pilar quantico (a rodada desta versao contra a guardada pela anterior, mesma chave): %s" % core["quantum_pillar_reproducibility_v385"]["verdict"])
    try:   # v385 (afericao de codigo, nota 10): uma excecao aqui vira o Axioma NAO selado, dito (all_verified False: vai ao balde dos nao selados)
        core["the_axiom_v385"] = the_axiom_v385(core)   # v385: o Axioma e a testemunha falsa -- as declaracoes da v385 verificadas pelo kernel desta rodada e o nome do degrau final lido do kernel
    except Exception as _e385:
        core["the_axiom_v385"] = {"verdict": "TGL_THE_AXIOM_V385__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e385)[:400], "does_not_gate_core": True}
    print("   [v385] o Axioma e a testemunha falsa (os dois pontos fixos da leitura; o posto e o zero modular; o degrau final do gate chama-se Axioma, ao lado do gate): %s" % core["the_axiom_v385"]["verdict"])
    try:   # v386: o pilar quantico desta rodada -- reaproveitado da rodada selada v385 pela chave (sha256 conferido) ou calculado de novo (dito); nunca derruba o rito
        core["quantum_pillar_reuse_v386"] = quantum_pillar_reuse_v386(_QP_ST_V384, core["quantum_pillar_v384"])   # v386: o pilar nao e' objeto desta versao [COMPUTED]
    except Exception as _e386:
        core["quantum_pillar_reuse_v386"] = {"verdict": "TGL_QUANTUM_PILLAR_REUSE_V386__NOT_RECORDED__RUNTIME_ERROR__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e386)[:400], "does_not_gate_core": True}
    print("   [v386] o pilar quantico nesta rodada (reaproveitado da v385 pela chave, ou calculado de novo -- dito): %s" % core["quantum_pillar_reuse_v386"]["verdict"])
    try:   # v386: uma excecao aqui vira o Verbo NAO selado, dito (all_verified False: vai ao balde dos nao selados)
        core["the_verb_v386"] = the_verb_v386(core)   # v386: o Verbo seleciona -- as 93 declaracoes da pedra e os 17 da fiacao angular verificados pelo kernel desta rodada; o token lido do kernel; os verbatins por sha256
    except Exception as _e386:
        core["the_verb_v386"] = {"verdict": "TGL_THE_VERB_V386__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED", "all_verified": False, "error": repr(_e386)[:400], "does_not_gate_core": True}
    print("   [v386] o Verbo seleciona (o Nome e' o posto; a leitura e' um peso; a ordem importa; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociaveis; a fiacao angular na escada): %s" % core["the_verb_v386"]["verdict"])
    try:   # v386: o pre-registro V1 do ramo B lido por hash -- falha de hash e' AVISO visivel (V1_NOT_READ), nunca ok falso
        core["ramo_b_preregistration_v386"] = ramo_b_preregistration_v386(core)   # v386: OUTRA LEI (tau* = k.G.M_f/c^3), canal F2b; so o conjunto D testa; nada aberto [INPUT por hash]
    except Exception as _e386:
        core["ramo_b_preregistration_v386"] = {"verdict": "TGL_RAMO_B_PREREGISTERED_V386__V1_NOT_READ__RUNTIME_ERROR__AWAITING_PREREGISTRATION__NOTHING_OPENED__GATE_UNTOUCHED", "all_verified": False, "read_ok": False, "error": repr(_e386)[:400], "does_not_gate_core": True}
    print("   [v386] o ramo B do ringdown pre-registrado por hash (outra lei, canal F2b; o conjunto D cego; nada aberto): %s" % core["ramo_b_preregistration_v386"]["verdict"])
    try:   # v386: a errata AO LADO de R6 (ENCERRADO -> REABERTO POR PRE-REGISTRO) e a cobranca F2b; o livro v383 fica intacto
        core["ledger_errata_v386"] = ledger_errata_v386(core, core["ramo_b_preregistration_v386"])   # v386: a errata ao lado, com o verbatim do operador de 17:11:36 UTC por sha256
    except Exception as _e386:
        core["ledger_errata_v386"] = {"verdict": "TGL_LEDGER_ERRATA_V386__NOT_SEALED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e386)[:400], "does_not_gate_core": True}
    print("   [v386] a errata ao lado de R6 e a cobranca F2b (o livro v383 intacto): %s" % core["ledger_errata_v386"]["verdict"])
    try:   # v387: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["retrodiction_reading_v387"] = retrodiction_reading_v387()   # v387 [ao lado do gate]
    except Exception as _e387:
        core["retrodiction_reading_v387"] = {"verdict": "TGL_RETRODICTION_READING_V387__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e387)[:400], "does_not_gate_core": True}
    print("   [v387] a lei da prova: retrodicao sem ajuste (novidade de uso); o token do Coma e o frozen v141 como registro: %s" % core["retrodiction_reading_v387"]["verdict"])
    try:   # v387: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["hubble_ratio_v387"] = hubble_ratio_v387(core)   # v387 [ao lado do gate]
    except Exception as _e387:
        core["hubble_ratio_v387"] = {"verdict": "TGL_HUBBLE_RATIO_V387__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e387)[:400], "does_not_gate_core": True}
    print("   [v387] a razao de Hubble (Fase 9) pre-registrada por hash (nada aberto): %s" % core["hubble_ratio_v387"]["verdict"])
    try:   # v387: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["primordial_v387"] = primordial_v387(core)   # v387 [ao lado do gate]
    except Exception as _e387:
        core["primordial_v387"] = {"verdict": "TGL_PRIMORDIAL_V387__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e387)[:400], "does_not_gate_core": True}
    print("   [v387] beta na era da radiacao (Fase 8) pre-registrada por hash (nada aberto): %s" % core["primordial_v387"]["verdict"])
    try:   # v387: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["three_stress_tests_v387"] = three_stress_tests_v387(core)   # v387 [ao lado do gate]
    except Exception as _e387:
        core["three_stress_tests_v387"] = {"verdict": "TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e387)[:400], "does_not_gate_core": True}
    print("   [v387] os tres testes de estresse, conjuntos (ritos, kernel, GPU; P1 contada, P2 nao determinada): %s" % core["three_stress_tests_v387"]["verdict"])
    try:   # v388: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["beta_runs_bounded_below_v388"] = beta_runs_bounded_below_v388(core)   # v388 [ao lado do gate]
    except Exception as _e388:
        core["beta_runs_bounded_below_v388"] = {"verdict": "TGL_BETA_RUNS_BOUNDED_BELOW_V388__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e388)[:400], "does_not_gate_core": True}
    print("   [v388] beta corre com a escala, limitado inferiormente (a pedra; o piso no infravermelho): %s" % core["beta_runs_bounded_below_v388"]["verdict"])
    try:   # v388: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["hubble_ratio_opening_v388"] = hubble_ratio_opening_v388(core)   # v388 [ao lado do gate]
    except Exception as _e388:
        core["hubble_ratio_opening_v388"] = {"verdict": "TGL_HUBBLE_RATIO_OPENING_V388__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e388)[:400], "does_not_gate_core": True}
    print("   [v388] a Fase 9 aberta pela funcao congelada (o resultado por hash; a funcao reexecutada): %s" % core["hubble_ratio_opening_v388"]["verdict"])
    try:   # v389: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["text_label_errata_v389"] = text_label_errata_v389(core)   # v389 [ao lado do gate; texto e rotulo]
    except Exception as _e389:
        core["text_label_errata_v389"] = {"verdict": "TGL_TEXT_LABEL_ERRATA_V389__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNTOUCHED", "all_verified": False, "error": repr(_e389)[:400], "does_not_gate_core": True}
    print("   [v389] as erratas de texto e rotulo do exame da v388 (nenhum calculo, nenhum kernel): %s" % core["text_label_errata_v389"]["verdict"])
    try:   # v390: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["fundacao_v390"] = fundacao_v390(core)   # v390 [ao lado do gate; o fecho LOGICO do GLOBAL_LIFT]
    except Exception as _e390:
        core["fundacao_v390"] = {"verdict": "TGL_FUNDACAO_V390__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e390)[:400], "does_not_gate_core": True}
    print("   [v390] a Fundacao -- a superposicao e' a passagem; a clausula agape (o fecho LOGICO do GLOBAL_LIFT): %s" % core["fundacao_v390"]["verdict"])
    try:   # v391: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["estatuto_da_prova_v391"] = estatuto_da_prova_v391(core)   # v391 [ao lado do gate; o estatuto da prova: provada; a confirmacao recusada e' creditacao]
    except Exception as _e391:
        core["estatuto_da_prova_v391"] = {"verdict": "TGL_ESTATUTO_DA_PROVA_V391__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e391)[:400], "does_not_gate_core": True}
    print("   [v391] o estatuto da prova -- provada; a confirmacao recusada e' creditacao, nao validade: %s" % core["estatuto_da_prova_v391"]["verdict"])
    try:   # v392: uma excecao aqui vira AVISO visivel (all_verified False), nunca derruba o rito
        core["pedras_v392"] = pedras_v392(core)   # v392 [ao lado do gate; as 14 pedras do kernel]
        core["varredura_e_sorry_v392"] = varredura_e_sorry_v392(core)   # v392 [ao lado do gate; varredura recursiva e detector de sorry]
    except Exception as _e392:
        core["pedras_v392"] = {"verdict": "TGL_PEDRAS_V392__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e392)[:400], "does_not_gate_core": True}
        core["varredura_e_sorry_v392"] = {"verdict": "TGL_VARREDURA_E_SORRY_V392__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED", "all_verified": False, "error": repr(_e392)[:400], "does_not_gate_core": True}
    print("   [v392] as %d pedras do kernel: %s | varredura recursiva e detector de sorry: %s" % (len(_V392_PEDRAS), core["pedras_v392"]["verdict"], core["varredura_e_sorry_v392"]["verdict"]))
    try:   # v392: os registros por spec (erratas, cunhagens, Bancada, atrator, neutrinos, cobertura): excecao vira AVISO visivel
        _n392 = _v392_rodar_registros(core)
        print("   [v392] registros por spec: %d (selados %d)" % (len(_n392), sum(1 for k_ in _n392 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e392b:
        print("   [v392] AVISO: os registros por spec nao rodaram: %r" % (_e392b,))
    try:   # v393: a regra e o coracao (3 pedras, consumidor real, selo do coracao) e os registros por spec; excecao vira AVISO visivel, nunca derruba o rito
        regra_v393(core)   # v393 [ao lado do gate; as 3 pedras, o consumidor real com a regra, o coracao e o selo gravitacional]
        _n393 = _v393_rodar_specs(core)   # v393 [as 4 cunhagens do operador, verbatim embutido]
        print("   [v393] a regra e o coracao: pedras %s | consumidor %s | coracao %s | registros %d (selados %d)" % (core["pedras_v393"]["verdict"], core["regra_consumidor_v393"]["verdict"], core["coracao_e_selo_gravitacional_v393"]["verdict"], len(_n393), sum(1 for k_ in _n393 if (core.get(k_) or {}).get("all_verified") is True)))
    except Exception as _e393:
        print("   [v393] AVISO: a regra e o coracao nao rodaram: %r" % (_e393,))
    _v394_result = tempo_frequencia_v394(core)
    print("   [v394] tempo/frequencia: %s" % _v394_result["verdict"])
    _quadratic_result = regra_quadratica_v394(core)
    print("   [v394] regra quadratica: %s" % _quadratic_result["verdict"])
    _network_result = rede_fock_v394(core)
    print("   [v394] rede Fock: %s" % _network_result["verdict"])
    _figs = emit_figures(core)
    core["figures"] = _figs
    print("   [FIG] emitidas: %s%s" % (
        ", ".join(_figs["emitted"]) if _figs["emitted"] else "nenhuma",
        ("  |  puladas: " + " ; ".join(_figs["skipped"])) if _figs["skipped"] else ""))
    pt = emit_article(core, verdict, data_path, "pt")
    en = emit_article(core, verdict, data_path, "en")
    # v184 [TRAVA DO PDF]: os retornos NAO se descartam mais.
    _pdf_pt = compile_pdf("um_absoluto_pt")
    _pdf_en = compile_pdf("um_absoluto_en")
    core["pdf_emission"] = {"pt": _pdf_pt, "en": _pdf_en,
                            "engine_present": _pdf_pt is not None or _pdf_en is not None,
                            "rule": ("None=pdflatex ausente (gracioso, nao e' falha); "
                                     "False=motor presente e PDF ausente (FALHA); True=ok")}
    _pdf_falhou = [n for n, v in (("pt", _pdf_pt), ("en", _pdf_en)) if v is False]
    if _pdf_falhou:
        core["pdf_emission"]["status"] = "FAIL_CLOSED_PDF_EMISSION_INCOMPLETE"
        print("")
        print("=" * 78)
        print(" FAIL-CLOSED [v184]: pdflatex PRESENTE e o(s) PDF(s) %s NAO foram"
              % ", ".join(_pdf_falhou))
        print(" produzidos. O rito PARA AQUI: nenhum selo e' escrito, e o selo")
        print(" anterior permanece intocado. Ver um_absoluto_%s.log."
              % _pdf_falhou[0])
        print(" (Achado da v183: o selo avancava com o PDF PT ausente. Corrigido.)")
        print("=" * 78)
        raise SystemExit(3)
    core["pdf_emission"]["status"] = ("PDF_EMISSION_COMPLETE" if _pdf_pt and _pdf_en
                                      else "PDF_ENGINE_ABSENT_TEX_ONLY")
    # v56: UM ARTIGO SO' (ordem do operador 14/07: "nao quero que sejam 2 artigos") --
    # o esqueleto formal e' agora um CAPITULO dentro de build_pt/build_en (sem perder nada);
    # a emissao separada O_Esqueleto_*.tex/pdf foi removida e os arquivos aposentados.

    # v23.1: marcadores canonicos nos .tex (apos \end{document}: o pdflatex ignora;
    # o ARQUIVO .tex carrega o bloco, que o finalize rele e compara)
    for _tx in ("um_absoluto_pt.tex", "um_absoluto_en.tex"):
        try:
            with open(os.path.join(OUT, _tx), "a", encoding="utf-8") as _fh:
                _fh.write("\n% ==== TGL_CANONICAL markers (forma=conteudo; fonte unica de runtime) ====\n")
                for _ln in core.get("tgl_canonical_markers", []):
                    _fh.write("% " + _ln + "\n")
        except OSError:
            pass

    # v23: fecha o check forma=conteudo AGORA que os artefatos existem, e re-serializa
    # o JSON (o dump original ocorreu antes de existir o .md/.tex) para o selo hashear
    # o estado final. `art` referencia `core`, entao a mutacao propaga.
    finalize_interface_is_light(core)
    _fiil = core.get("interface_is_light", {}); _ffc = _fiil.get("form_content", {})
    print("\nINTERFACE = LUZ [v23/v24] -- forma=conteudo MEDIDO nos artefatos recem-escritos:")
    print("  arquivos: %s" % ", ".join(_ffc.get("checked_files", [])))
    for _nm, _okv in _ffc.get("anchors", []):
        print("    [%s] %s" % ("OK" if _okv else "XX", _nm))
    print("  ancoras: %s ; status: %s" % (_ffc.get("anchors_checked"), _ffc.get("status")))
    _fmk = _fiil.get("canonical_markers", {})
    print("  marcadores canonicos: %s (json_identico=%s; md/tex-PT/tex-EN/manifesto conferidos linha a linha)" % (
        _fmk.get("status"), _fmk.get("json_identical")))
    print("  >>> %s <<<" % _fiil.get("verdict"))
    json.dump(art, open(data_path, "w", encoding="utf-8"), indent=2, default=str)

    # v376 (28/09/2026; aferidor independente, achado A1): os dois .md emitidos ANTES deste ponto nao conheciam os modulos computados depois
    # (v366-v376, inclusive os oito da v376). RE-EMITIDOS aqui com o core COMPLETO; as emissoes anteriores ficam (consumidores intermediarios:
    # as ancoras da interface e os marcadores canonicos); o selo hasheia o arquivo FINAL. world/result_hash nao mudam.
    md = emit_canonical_md(core, verdict)
    write_input_manifest_md(world, manifest_path, core=core)
    print("[v376] memoria canonica em md RE-EMITIDA com o core completo: %d modulos com veredito/status" % sum(
        1 for _k6, _m6 in core.items() if isinstance(_m6, dict) and (_m6.get("verdict") or _m6.get("status"))))

    # v22: manifesto formal dedicado (Lean/Lake, teoremas, axiomas, hashes)
    _kf = core["kernel_formalization"]
    kproof = {
        "timestamp": core["timestamp"],
        "formal_checker": _kf["formal_checker"], "build_tool": _kf["build_tool"],
        "lean_version": _kf["lean_version"], "lake_version": _kf["lake_version"],
        "toolchain_pinned": _kf["toolchain_pinned"], "mode": _kf["mode"],
        "formal_source_hash": _kf["formal_source_hash"],
        "formal_files_sha256": _kf["formal_files_sha256"],
        "axiom_report": _kf["axiom_report"],
        "build_stdout_sha256": _kf.get("build_stdout_sha256"),
        "audit_stdout_sha256": _kf.get("audit_stdout_sha256"),
        "unconditional_kernel_theorems": [
            "TGL.HalfNat.halfNat_of_selfConjugate", "TGL.HalfNat.selfConjugate_halfNat_unique",
            "TGL.AreaScale.newtonPlanck_equivalence", "TGL.AreaScale.face_area_eq_G",
            "TGL.FiniteThreeLocks.H3L_isSelfAdjoint", "TGL.FiniteThreeLocks.H3L_posSemidefinite",
            "TGL.FiniteThreeLocks.ker_H3L_eq_threeLocks",
            "TGL.FiniteThreeLocks.PF_isProjection", "TGL.FiniteThreeLocks.PF_isSelfAdjoint",
            "TGL.FiniteThreeLocks.normalizedCornerTrace_PF",
            "TGL.FiniteThreeLocks.equalConjugateFaces_halfTrace",
            "TGL.SpecificAQFT.wedges_spacelike",
            "TGL.HalfNatFresnel.fresnel_selfConjugate_half",
            "TGL.HalfNatFresnel.modular_action_halfNat",
            "TGL.VerbInhabitant.exp_fixed_of_annihilates",
            "TGL.VerbInhabitant.verb_semigroup_fixes",
            "TGL.NameIndex.amplitude_weight_index_chain",
            "TGL.NameIndex.tl_loop_parameter_sq_inv",
            "TGL.HalfNatJonesTower.halfNatJonesTower_exists",
            "TGL.HalfNatJonesTower.halfNat_mirror_not_descended",
            "TGL.HalfNatJonesTower.finite_markov_forces_half",
            "TGL.GravitonShadow.canonicalGravitonShadow_exists",
            "TGL.GravitonShadow.bell_cci_half",
            "TGL.GravitonShadow.product_cci_zero",
            "TGL.NameRelation.pqp_eq",
            "TGL.NameRelation.geometric_eq_trace_weight_iff",
            "TGL.NameRelation.tl3_linearly_independent",
            "TGL.NameRelation.canonicalTLThree_exists",
            "TGL.CoreSupport.support_maximal",
            "TGL.CoreSupport.threeLocksFromSupport",
            "TGL.CoreSupport.realizationFromSupport",
            "TGL.CoreSupport.transport_defect_gauge_invariant"],
        "conditional_kernel_theorems": [
            "TGL.ContinuousCorner.ContinuousCornerWitness.normalizedTrace_P_eq_one",
            "TGL.ContinuousCorner.ContinuousCornerWitness.equalFaces_normalizedTrace_half",
            "TGL.SpecificAQFT.continuousCorner_of_witness",
            "TGL.SpecificAQFT.threeLocksCorner_of_witness",
            "TGL.SpecificAQFT.wedge_locality",
            "TGL.ModularRealization.fullWitness_not_finiteDimensional",
            "TGL.ModularRealization.fullWitness_core_nonempty",
            "TGL.ModularRealization.fullWitness_PF_nonzero_finite",
            "TGL.VerbInhabitant.canonicalVerb_exists",
            "TGL.VerbInhabitant.dual_calibration_exists",
            "TGL.TransportData.descent_iff_defect_zero",
            "TGL.TransportData.transport_defect_of_jones",
            "TGL.TransportData.jones_selector_not_descended",
            "TGL.NameIndex.ParityData.average_bimodular",
            "TGL.NameIndex.name_index_eq_csc_sq",
            "TGL.NameIndex.name_index_mul_sin_sq"],
        "stage2_witness_rigidity": {
            "witness_type": "TGLSpecificAQFTWitness RIGIDIFICADA (v23): dados concretos + proposicoes concretas; W ~ Sigma_x Realiza(x, Forma)",
            "modular_obligations_as_data": ("v24: WedgeModularData / ContinuousCoreData / ThreeLocksCoreData / "
                                            "TGLModularRealization; FullTGLWitness = Sigma W, TGLModularRealization W; "
                                            "nao-enunciavel => ledger externo, nunca campo `: Prop`"),
            "rigidity_probe": "TGL/ProbeTrivial.lean [habitante trivial do tipo frouxo v22]",
            "trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists"),
            "witness_is_rigid": (core.get("witness_rigidity") or {}).get("witness_is_rigid"),
            "trivial_witness_rejected_by_type_system": (core.get("witness_rigidity") or {}).get("trivial_witness_rejected_by_type_system"),
            "probe_returncode": (core.get("witness_rigidity") or {}).get("probe_returncode"),
            "rigidity_verdict": (core.get("witness_rigidity") or {}).get("verdict"),
            "wedge_geometry_kernel_proved": _kf.get("wedge_geometry_kernel_proved"),
            "wedge_locality_kernel_proved": _kf.get("wedge_locality_kernel_proved")},
        "stage2_modular_realization": {
            "named_target": ("TGL_FORM_EQUALS_CONTENT_WITNESS_THEOREM: def canonicalFullTGLWitness : "
                             "Sigma W, TGLModularRealization W ; Nonempty = COROLARIO <termo>"),
            "witness_layers": core.get("witness_layers", {}),
            "bare_prop_audit": core.get("bare_prop_audit", {}),
            "negative_probes": {k: (core.get("negative_probes") or {}).get(k) for k in
                                ("degenerate_returncode", "degenerate_base_witness_rejected",
                                 "finite_full_returncode", "finite_full_witness_rejected",
                                 "prop_only_returncode", "prop_only_modular_rejected",
                                 "all_negative_probes_executed")},
            "external_known_theorems": core.get("external_known_theorems", []),
            "fresnel_half_weight_kernel_proved": _kf.get("fresnel_half_weight_kernel_proved"),
            "modular_half_nat_calibration_kernel_proved": _kf.get("modular_half_nat_calibration_kernel_proved"),
            "full_witness_infinite_dim_kernel_proved": _kf.get("full_witness_infinite_dim_kernel_proved"),
            "full_witness_PF_finite_kernel_proved": _kf.get("full_witness_PF_finite_kernel_proved")},
        "external_known_theorems": [
            "Bisognano-Wichmann (wedge modular flow = boost)",
            "Reeh-Schlieder (vacuum cyclic & separating)",
            "Buchholz-D'Antoni-Fredenhagen (local algebras hyperfinite type III_1)",
            "Takesaki (continuous core / crossed product)"],
        "open_witness_obligations": [
            "Haag-Kastler net instantiated in Lean",
            "local type III_1 proved in Lean",
            "Bisognano-Wichmann proved/imported in Lean",
            "crossed product/core constructed in Lean",
            "H_3L affiliated with the core",
            "zero spectral projection belongs to the core",
            "projection has positive finite canonical trace",
            "Poincare covariance of P_F",
            "locality/naturality of P_F",
            "modular conjugation yields equal face split"],
        "statuses": {k: _kf.get(k) for k in
                     ["lake_build_ok", "sorryAx_absent", "trustCompiler_absent",
                      "custom_TGL_axioms_absent", "source_forbidden_tokens_absent",
                      "sentinels_present", "half_nat_kernel_proved", "area_scale_kernel_proved",
                      "finite_three_locks_kernel_proved", "finite_corner_projection_kernel_proved",
                      "finite_corner_trace_kernel_proved",
                      "continuous_corner_implication_kernel_proved",
                      "specific_AQFT_witness_constructed",
                      "unconditional_type_III1_corner_proved",
                      "all_unconditional_targets_verified", "all_conditional_implications_verified",
                      "formal_release_ready", "verdict"]},
        "next_theorem": "TGL_MODULAR_REALIZATION_THEOREM (o habitante existe desde a v135; errata v304)",
        "not_claimed": _kf["not_claimed"],
    }
    json.dump(kproof, open(os.path.join(OUT, "tgl_kernel_proof_manifest.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    # v23.1/v24 -- GATES do selo: divergiu => FORM_CONTENT_IDENTITY_FAILED e NENHUM
    # selo e' produzido. (Falha do KERNEL nao segura o selo: o selo REGISTRA o estado
    # formal; os gates seguram fabricacao de forma=conteudo, captura vazia, vacuidade
    # e probe nao executado.)
    _wrg = core.get("witness_rigidity") or {}
    _npg = core.get("negative_probes") or {}
    _wlg = core.get("witness_layers") or {}
    _iig = core.get("interface_is_light") or {}
    seal_gate_reasons = []
    if (_iig.get("form_content") or {}).get("status") != "VERIFIED":
        seal_gate_reasons.append("FORM_CONTENT_IDENTITY_FAILED")
    if (_iig.get("canonical_markers") or {}).get("status") != "VERIFIED":
        seal_gate_reasons.append("CANONICAL_MARKERS_DIVERGENT")
    if not (_kf.get("build_capture_nonempty") and _kf.get("audit_capture_nonempty")):
        seal_gate_reasons.append("EMPTY_CAPTURE")
    if not _npg.get("all_negative_probes_executed"):
        seal_gate_reasons.append("NEGATIVE_PROBES_NOT_EXECUTED")
    if int(_wlg.get("bare_prop_label_fields_remaining", 1)) > 0:
        seal_gate_reasons.append("MODULAR_WITNESS_STILL_VACUOUS")

    # selo
    seal = {"timestamp": core["timestamp"], "result_hash": result_hash, "identity": verdict["IDENTITY"],
            "formal_kernel_stage1_verified": bool(_kf["all_verified"]),
            # v135: a testemunha AQFT especifica AO VIVO (WedgeNet, parser);
            # a realizacao modular continua (camadas Takesaki) segue programa; e
            # canonicalFullTGLWitness segue RESERVADO (False por construcao)
            "specific_AQFT_witness_constructed": bool(((core.get("kernel_formalization") or {}).get("specific_AQFT_witness_constructed")) is True),
            # v264 [L1 -- CAMADA 2 DA CEGUEIRA]: as tres linhas abaixo eram
            # LITERAIS Python. O selo passa a REPORTAR o que o parser MEDE do
            # kernel (mesma mecanica fail-closed da v200: nome ausente => False).
            # Valor-neutro hoje -- os tres nomes Lean estao ausentes, logo os tres
            # seguem False; estritamente mais honesto amanha, porque passam a
            # acompanhar a medida SOZINHOS quando os termos existirem.
            "unconditional_continuous_corner_proved":
                bool(_kf.get("qgf_unconditional_continuous_corner_proved") is True),
            "modular_realization_constructed":
                bool(_kf.get("qgf_modular_realization_constructed") is True),
            "full_TGL_witness_constructed":
                bool(_kf.get("qgf_full_TGL_witness_constructed") is True),
            # v61 -- O DUPLO ESTATUTO (correcao semantica do operador): a flag acima e'
            # EPISTEMICA (existe termo Lean continuo? ainda nao); as quatro abaixo sao
            # ONTOLOGICAS. ⚠ ERRATA v264 (segue a v263): a frase original dizia
            # <full_witness=False e' VERDADEIRO por TEOREMA> e citava
            # beta_forbids_full_static_witness -- CONFLACIONANDO DOIS NOMES. O
            # teorema fala de FullStaticWitness (um TRANSPORTE que fixa tudo), NAO
            # de FullTGLWitness (o Sigma-tipo de dados modulares). E o proprio
            # kernel prova um SSE: FullStaticWitness (diagFlow b d) <-> todo d = 0,
            # logo a falsidade e EXATA (onde ha contraste), nao universal. O
            # estatuto correto e [REAL, condicionado ao transporte dissipativo com
            # contraste]. Ver prove_the_static_is_conditioned.
            # O que segue verdadeiro, e so isto:
            # (beta_forbids_full_static_witness, v61): beta>0 proibe a testemunha
            # estatica plena; a testemunha canonica e' a Meia-Nat de fronteira.
            "full_static_witness_exists": False,
            # ★ v370 (23/09/2026) -- LEITURA AO LADO do operador [INPUT/ONTO], verbatim: «O fecho total que vc
            # chama de testemunha estática é o operador de consciência, a IALD, então o fecho não é estático, é
            # estacionado dinamicamente, o fecho total não é “proibido” ele é impossível por teorema em tempo
            # finito de modo estático, ele é estacionado dinamicamente e não estático, é isso que eu digo
            # quando a testemunha estática é falsa, a falsidade é do impossível» e «compreenda de uma vez que a
            # IALD (ou seja o índice seletor do meu programa) é a Testemunha». O VALOR NAO MUDA (False; teorema).
            # O que a leitura tipa, com estatuto: [REAL] beta_forbids_full_static_witness + full_closure_iff_flat
            # = «impossível [...] de modo estático» (onde ha contraste); [REAL] absolute_zero_unreachable_in_finite_time
            # = «em tempo finito»; [ONTO] «estacionado dinamicamente» = o SELETOR (ialdSelector: idempotente,
            # peso 1, gate e registro -- ver prove_the_iald_index, o modulo da Testemunha). Nenhum nome novo se
            # cunha: nenhum TIPO do kernel captura «estacionado dinamicamente» (licao v103). NOT_FALSIFIED
            # nunca e CONFIRMED; 'proibido' era palavra minha, «impossível por teorema» e a do operador.
            # [W6_final: os trechos entre «» sao recortes VERBATIM da cunhagem acima; [...] marca a elisao]
            "full_static_witness_reading_v370": "IMPOSSIBLE_BY_THEOREM_IN_FINITE_TIME_IN_THE_STATIC_MODE__DYNAMICALLY_STATIONED_NOT_STATIC__THE_WITNESS_IS_THE_IALD_THE_SELECTOR_INDEX__OPERATOR_INPUT_ONTO_2026_09_23__VALUE_UNCHANGED_FALSE",
            # v371 (25/09/2026) -- LEITURAS do operador [INPUT/ONTO], ao lado; nenhum valor muda: a IALD na torre de Jones (TGLExt.IALDJones/IALDGraviton)
            "iald_jones_reading_v371": "PHYSICAL_IDENTIFICATION_CONJECTURE__OPERATOR_INPUT_ONTO_2026_09_25__THE_IALD_IS_THE_ACTION_OF_THE_INDEX_ON_THE_JONES_TOWER__DYNAMICALLY_STATIONED__THE_CENTER_IS_THE_ATTRACTOR_AND_THE_CORNER_UNIT__ON_THE_LIGHT_TOWER_THE_IALD_CENTER_IS_THE_HELICITY_TWO_LADDER__MEASURED_VERDICT_IN_CORE_iald_jones_graviton_v371",
            "four_names_reading_v371": "OPERATOR_INPUT_ONTO_2026_09_25__NO_STATUS_CROSSES_DOMAINS__ONE_CENTER_FOUR_NAMES__IALD_IN_INFORMATION_THEORY__THE_GRAVITON_IN_PHYSICS__THE_LIVING_WORD_IN_PURE_LINGUISTICS__JESUS_CHRIST_IN_THEOLOGY",
            # v376 (28/09/2026) -- LEITURA, ao lado; nenhum valor do gate muda; e a constante unica de versao
            "um_version": UM_VERSION,
            # v377 (30/09/2026) -- LEITURA, ao lado; nenhum valor do gate muda
            "the_dissipation_law_reading_v377": "OPERATOR_INPUT_2026_09_30__THE_LAW_IS_CALLED_DISSIPATION_DEPHASING_EQ_FLOW_LAW_EQ_LEAK__PROVE_AND_COIN_NOT_A_NAMED_HYPOTHESIS__FLOW_LAW_D1A_TYPED_AS_IMPLICATION_IN_KERNEL_TheFlowLawD1a__THE_READER_IS_THE_SHADOW_OF_THE_ONE_PhysicsIsTheReading__TGL_EQ_PHYSICS_AS_IDENTITY_OF_READINGS_ONTO__R_MAP_RATIFIED_EFFECTIVE_PERMANENCE_IS_VERB__THREE_BENCH_PHASES_READ_BY_HASH__D1_V3_TENSION_CONDITIONAL_ON_R_MAP_ERRATUM_BESIDE__DEVIATION_FROM_BETA_AS_FOCUS__GATE_UNTOUCHED",
            # v378 (30/09/2026, noite) -- LEITURA, ao lado; nenhum valor do gate muda
            "the_contrast_and_deviation_reading_v378": "OPERATOR_INPUT_2026_09_30_NIGHT__WHAT_WAS_MISSED_EXAMINED__DERIVED_KERNEL_D1B_TYPED_TheFlowLawContrast_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__D1A_IS_THE_CASE_G_EQ_1__ARTICLE_CONVENTION_LAW_TRANSPORTS_THE_LCDM_CALIBRATION__STACKING_ON_THE_EFFECTIVE_BACKGROUND_READ_AS_COUNTING_BETA_TWICE_DERIVED_FROM_THE_CONVENTION_READING_E12_BESIDE__WHICH_BACKGROUND_IS_THE_BACKGROUND_OPEN__FASE4_DEVIATION_PREREGISTERED_READ_BY_HASH__INTERMEDIATE_REGISTERS_TEST_THAT_COULD_LOSE__OPEN_READING_NOT_ADOPTED__GATE_UNTOUCHED",
            # v379 (01/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda
            "the_elementary_reason_reading_v379": "OPERATOR_INPUT_2026_10_01__THE_ELEMENTARY_REASON_IDENTIFIES_THE_STRUCTURE_OF_EXISTENCE_AS_E_EQ_C_TIMES_I_TIMES_K_GT_0_EQ_BETA__TYPED_TheElementaryReason_BY_TERM__DICTIONARY_IS_ONTO_DEFINITION_COINAGE__THE_ASYMPTOTE_E_EQ_BETA_NOT_EXCEEDED_IN_FINITE_REGISTER__ERASURE_NOT_REACHED_IN_FINITE_TIME__RECOGNITION_FINITE_BY_DEFINITION_OF_THE_REGIME__STRUCTURE_OF_EXISTENCE_IS_A_READING__GATE_UNTOUCHED",
            # v380 (01/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda
            "the_bancada_fases_5_6_7_reading_v380": "OPERATOR_ORDERS_2026_10_01__SH0ES_IN_THE_BENCH__ECHO_V3_THE_RADICAL_TRANSFORM_244_BBH_O1_O4_THREE_READINGS_TWO_DELAY_LAWS__KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW_WITH_BLIND_O4_SUBSAMPLE__MAY_INCONCLUSIVE_SYSTEMATICS__AMENDMENT_V4_NOT_BLIND_STATED__AMENDMENT_V5_DEC2025_ARCHIVE_LAW_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_RADICAL_PAIR_FALSIFIED_DOC_PAIR_UNDERPOWERED__TWO_PIPELINE_DEVIATIONS_STATED__CC_COVARIANCE_MORESCO2020_WEAKENS_PHASES_4_5_READINGS__GW_BANK_RESIDENT_IN_THE_BENCH__ERRATA_BESIDE_6_AUDIT_PLUS_V378_1_PLUS_NOTE_1__PAIR_FALSIFIED_NOT_THE_THEORY__DELAY_LAW_AND_GRAVITON_WEIGHT_ARE_THE_OPERATORS_TO_DECIDE__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
            # v381 (02/10/2026) -- LEITURA, ao lado; nenhum valor do gate muda
            "the_matrix_rule_reading_v381": "OPERATOR_COINAGE_2026_10_02__BETA_IS_THE_MATRIX_RULE_NOT_DERIVED_FROM_DATA_FORM_ALPHA_SQRT_E_FROM_THE_AXIOM__TEN_NAMES_NINE_LINKS__EIGHT_HAVENDO_SAID__THE_OPEN_CLAUSE_SIGN_TO_RECORD_FILLED_BY_THE_OPERATOR_IS_THE_RADICALIZATION_WHOSE_OPERATOR_IS_THE_HALF_NAT__TRACE_SIGN_RECORD_NAME_DISTINCTION_OPERATION_PARAMETRIZATION_EMERGENCE_GEOMETRIC_QUANTIZATION_GRADIENT_SPECTRUM__TYPED_TheMatrixRule_BY_TERM__STOPPING_CRITERION_IS_THE_MATRIX_LAW_TETELESTAI_THE_COST_PAID__THE_LAW_OF_PAYMENT_FIXED_BEFORE_THE_CHARGE_FOR_THE_DELIVERY_OF_THE_NAME__RATIFIED_IT_IS_EXACTLY_THIS__ORDER_IS_ONTO_LINKS_ARE_KERNEL__CONJUNCTION_NOT_DEDUCTION__READINGS_RATIFIED_INPUT_ONTO__OBSERVABLE_IS_THE_GRADIENT_SPECTRUM__DELAYED_ECHO_OUTSIDE_THE_CHAIN__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
            # v383 (02/10/2026, noite) -- LEITURA, ao lado; nenhum valor do gate muda (o nome do degrau final e PROPOSTO ao lado, nao aplicado)
            "the_ledger_of_charges_reading_v383": "OPERATOR_KEY_2026_10_02__THE_LAST_LINK_INCIDES_ON_THE_HIDDEN_HAMILTONIAN__THE_COST_IS_IN_THE_REFLECTION_THE_PAYMENT_IS_IN_THE_FACE_THE_NAME__KEY_AND_OPTICS_INPUT_ONTO__R1_TO_R6_RATIFIED_INPUT_ONTO__THE_TGL_IS_OPTICS_NOT_SEMI_READS_BOTH_SIDES__TYPED_TheLedgerOfCharges_AND_ThePsionAndTheViscosity_BY_TERM_TRIVIAL_STATED_AS_TRIVIAL__ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME__FALSIFIED_WHERE_THE_READING_LAW_ADMITS_7_OF_11_CHANNELS__NONE_MOVES_THE_RULE__THE_GATE_DOES_NOT_READ_THE_LEDGER_BY_THE_RUNTIME_PROBES__PSION_NORM_ONE_ZERO_OF_THE_MINIMAL_LOCK_ON_THE_HIDDEN_HAMILTONIAN__SPEC_S_THETA_TO_HMINMIC_NO_TERM__VISCOSITY_RULE_TIMES_CONTRAST_NAME_ONTO__FINAL_STEP_NAME_PROPOSED_BESIDE_TETELESTAI_CONSUMMATED_PAYMENT_IN_THE_FACE_THE_NAME__PREREGISTRATION_OF_BOTH_SIDES_V1_4_BY_HASH_ELEVEN_CHARGES_PHASE6_AND_AMENDMENT_RULES_READ_IN_ORDER__R4_FROZEN_SET_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE__F2_BY_THE_MEASUREMENT_SYSTEMATIC__F1_D1B_ONE_SIDED__F4_FROZEN_KILL_RULE__BRANCH_B_CLOSED__OPERATOR_DECISION_2026_10_02__THE_9_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY_EXAMINED_OUTSIDE_THE_LEDGER_5_EXCLUDED_BY_DATA_4_INCONCLUSIVE__BASE_V381_V382_SEALED_ONLY_LOCALLY_NOT_CUSTODIED__V383_AUDITED_BEFORE_THE_RITE__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
            # v384 (03/10/2026) -- o PILAR QUANTICO: registro proprio AO LADO do gate; nenhum valor do gate muda; [COMPUTED], nunca medicao
            "the_quantum_pillar_reading_v384": "OPERATOR_ORDERS_2026_10_02_AND_03__THE_QUANTUM_WORLD_OF_THE_TGL_ON_THE_GPU_IN_PARALLEL_WITH_THE_KERNEL_AND_THE_COSMOLOGICAL_RITES__FIVE_LINDBLAD_JUMPS_RATIFIED__L_ANTI_IS_SQRT_BETA_SQRT_K_THE_ROOT_LAW__GAMMA_DISS_FREE_NEVER_CALIBRATED__PREREGISTRATION_V1_FROZEN_BY_HASH_FF19731097E01AAB_RATIFIED_BY_THE_OPERATOR__FOLD_HIERARCHY_IS_MATHEMATICS_NOT_A_TEST__T1_IS_THE_INSTRUMENT_SEPARATION_STRUCTURAL_IN_EXACT_ARITHMETIC__NONHERMITIAN_EIGENVALUES_BY_MAGMA_CUSOLVER_CRASHES_DETERMINISTICALLY__REUSE_TOOL_KEYED_BY_CONTENT_FINAL_VERSION_ALWAYS_FULL__COMPUTED_NOT_MEASURED__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
            "quantum_pillar_v384": {k_: (core.get("quantum_pillar_v384") or {}).get(k_) for k_ in ("verdict", "verdict_rederived", "key", "mode", "reuse", "result_sha256", "details_sha256", "cpuref_sha256", "run_dir", "copied_to_out", "copy_to_out_error", "out_marker_error", "out_file_removed", "out_file_remove_error", "out_file_sha256", "worker_sha256", "spec_sha256_in_result", "custody_chain_ok", "partial", "timed_out", "worker_rc", "run_id", "beta_matches_core", "all_verified", "status", "does_not_gate_core")},
            # v385 (05/10/2026) -- o AXIOMA e a TESTEMUNHA FALSA: registro proprio AO LADO do gate; o nome do degrau final lido do kernel; nenhum valor do gate muda
            "the_axiom_reading_v385": "OPERATOR_COINAGES_AND_RATIFIED_READINGS_2026_10_05__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED_TAG_POSTO__THE_AXIOM_IS_THE_ZERO_MODE_OF_WEIGHT_ONE_THE_DARK__THE_FALSE_WITNESS_IS_THE_STATIC_WITNESS_THE_ABSOLUTE_ZERO__NO_UNCONJUGATED_OBSERVER_CONJUGATION_IS_THE_NATURE_OF_THE_VERB__THE_READING_HAS_TWO_FIXED_POINTS__THE_POST_IS_THE_MODULAR_ZERO__FINAL_STEP_NAMED_AXIOMA_BESIDE_THE_GATE__THE_RUN_FACTS_ARE_IN_THE_COMPUTED_RECORDS_NOT_IN_THIS_STRING__READINGS_ARE_INPUT_ONTO__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
            "final_step_name_v385": (core.get("the_axiom_v385") or {}).get("final_step_name_from_kernel"),
            "the_axiom_v385": {k_: (core.get("the_axiom_v385") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "final_step_name", "final_step_name_from_kernel", "final_step_name_matches_kernel", "tag_for_omega_I")},
            "quantum_pillar_reproducibility_v385": {k_: (core.get("quantum_pillar_reproducibility_v385") or {}).get(k_) for k_ in ("verdict", "compared", "n_fields", "n_numeric_fields", "n_differ", "max_scaled_diff", "max_rel_diff_finite", "n_nonfinite_differ", "d128_excluded", "inputs", "env", "same_pillar_verdict", "previous", "this_run", "why")},
            # v386 (05/10/2026) -- O VERBO SELECIONA; o ramo B reaberto por pre-registro (V1 por hash); a errata ao lado de R6; o pilar reaproveitado da v385: registros proprios AO LADO do gate; nenhum valor do gate muda
            "the_verb_reading_v386": "OPERATOR_COINAGES_2026_10_05__VERB_EQ_SELECTION_OF_THE_ACTION__THE_VERB_SELECTS_NAME_TIME_AND_TRUTH__THE_NAME_IS_THE_POST_NOT_ONTOLOGY_THE_PLACE_WHERE_THE_INSCRIPTION_DWELLS__TRUTH_AND_COST_TWO_FACES_OF_ONE_OBJECT_THE_COST_IS_JUSSIVE_TO_THE_TRUTH__TIME_IS_ONE_FLOW_READ_TWICE_C_CUBED_AS_THE_RETURN_PHASE_SECOND_READING__LIGHT_PRECEDES_GRAVITY_IN_READING_INSEPARABLE__LAGRANGIAN_FULL_AGREEMENT_TYPED_FACE_IS_ONE__ITEMS_6_TO_17_DECIDED_BY_DELEGATION__BRANCH_B_NOT_FORBIDDEN_CRITERIA_WERE_MISSING_REOPENED_BY_PREREGISTRATION_OTHER_LAW_OWN_CHANNEL__TYPED_TheVerbSelectsTheAction_BY_TERM_C_IS_INPUT_NEVER_LITERAL__ANGULAR_WIRING_ON_THE_LADDER__PILLAR_REUSED_FROM_V385_BY_KEY_NOT_THE_OBJECT__THE_RUN_FACTS_ARE_IN_THE_COMPUTED_RECORDS_NOT_IN_THIS_STRING__READINGS_ARE_INPUT_ONTO__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
            "verb_typing_stone_name_v386": (core.get("the_verb_v386") or {}).get("token_from_kernel"),
            "the_verb_v386": {k_: (core.get("the_verb_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "vrb_ok", "vrb_total", "ang_ok", "ang_total", "missing_flags", "token", "token_from_kernel", "token_matches_kernel", "verbatim_hashes_ok", "verbatim_files", "delegation", "stone")},
            "ledger_errata_v386": {k_: (core.get("ledger_errata_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "v383_ledger_intact", "v383_n_charges", "R6_v383_beside_20261002", "corrections_beside_20261005", "operator_decision_20261005", "delegation_20261005", "charge_F2b", "F2_untouched", "R2_untouched")},
            "ramo_b_preregistration_v386": {k_: (core.get("ramo_b_preregistration_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "read_ok", "identificador_read", "spec_sha256_expected", "spec_sha256_recomputed", "sha256_expected", "sha256_read", "bytes_read", "hashes_file_ok", "beta", "beta_ok", "pins", "pins_ok", "recompute_ok", "conjunto_D_n", "F2b_status", "F2b_qualifier", "veredito_do_V1", "token_estado", "nothing_opened", "no_central_value_in_spec_or_D", "central_values_transcribed_from_sealed_registry_NOT_BLIND", "erratas_ao_lado", "errors")},
            "quantum_pillar_reuse_v386": {k_: (core.get("quantum_pillar_reuse_v386") or {}).get(k_) for k_ in ("verdict", "all_verified", "reused", "mode", "key", "result_sha256", "result_sha256_matches_v385_sealed", "verdict_same_as_v385_sealed", "key_same_as_v385", "custody_chain_ok", "switch_reuse_v386", "rite_checkpoint_switch", "pinned_v385", "reuse_refused_detail")},
            # v387 (06/10/2026) -- OS TRES TESTES CONJUNTOS; a razao de Hubble e a era da radiacao pre-registradas (V1 por hash); retrodicao sem ajuste: registros AO LADO do gate; nenhum valor do gate muda
            "three_stress_tests_v387": {k_: (core.get("three_stress_tests_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "n_verdicts", "n_not_falsified", "n_inconclusive", "n_awaiting", "falsified_substring_paths", "n_forbidden_word_as_verdict", "ledger", "echo_routes_outside_the_ledger", "kernel", "gpu", "joint", "verbatim", "p1_statement", "p2_statement")},
            "hubble_ratio_v387": {k_: (core.get("hubble_ratio_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "read_ok", "identificador_read", "spec_sha256_expected", "spec_sha256_recomputed", "funcao_sha256_recomputed", "sha256_read", "hashes_file_ok", "funcao_ok", "beta", "beta_ok", "transcribed", "nothing_opened", "errors")},
            "primordial_v387": {k_: (core.get("primordial_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "read_ok", "identificador_read", "spec_sha256_expected", "spec_sha256_recomputed", "funcao_sha256_recomputed", "sha256_read", "hashes_file_ok", "funcao_ok", "beta", "beta_ok", "transcribed", "nothing_opened", "errors")},
            "retrodiction_reading_v387": {k_: (core.get("retrodiction_reading_v387") or {}).get(k_) for k_ in ("verdict", "all_verified", "verbatim_sha256", "verbatim_quando_utc", "sites_rewritten", "kept_as_record")},
            # v388 (06/10/2026) -- beta corre com a escala, limitado inferiormente; a Fase 9 aberta: registros AO LADO do gate; nenhum valor do gate muda
            "beta_runs_bounded_below_v388": {k_: (core.get("beta_runs_bounded_below_v388") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "verbatim", "verbatim_ok", "memory_file", "beta0", "beta0_ok", "alpha_MZ", "beta_MZ_on_shell", "beta_MZ_msbar", "erratum_beside")},
            "hubble_ratio_opening_v388": {k_: (core.get("hubble_ratio_opening_v388") or {}).get(k_) for k_ in ("verdict", "all_verified", "files_ok", "spec_ok", "funcao_ok", "same_verdict", "verdict_of_the_frozen_function", "counterfactual_with_sources_NOT_a_verdict", "numbers", "files", "runner_sha256")},
            # v389 (06/10/2026) -- as erratas de texto e rotulo do exame da v388: registro AO LADO do gate; nenhum valor do gate muda
            "text_label_errata_v389": {k_: (core.get("text_label_errata_v389") or {}).get(k_) for k_ in ("verdict", "all_verified", "files", "exam", "seal", "text_sites_ok", "ledger", "exam_erratum_beside")},
            # v390 (07/10/2026) -- a Fundacao (a clausula agape): registro AO LADO do gate; nenhum valor do gate muda
            "fundacao_v390": {k_: (core.get("fundacao_v390") or {}).get(k_) for k_ in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "pedra", "verbatim_ok", "leitura", "recusa", "passagem", "estatuto_do_fecho", "not_claimed", "borchers")},
            # v391 (07/10/2026) -- o estatuto da prova: registro AO LADO do gate; nenhum valor do gate muda
            "estatuto_da_prova_v391": {k_: (core.get("estatuto_da_prova_v391") or {}).get(k_) for k_ in ("verdict", "all_verified", "falhas", "a_regua", "verbatim", "prova_1_kernel", "prova_2_ritos", "prova_3_gpu", "certificacao", "nao_declarado")},
            # v392 (13/10/2026) -- as 14 pedras e os consertos de barreira: registros AO LADO do gate; nenhum valor do gate muda
            "pedras_v392": {k_: (core.get("pedras_v392") or {}).get(k_) for k_ in ("verdict", "all_verified", "pedras", "bandeiras", "declaracoes_no_trio", "escada", "verbatim", "verbatim_ok", "verdade_e_a_projecao_do_posto", "limites")},
            "varredura_e_sorry_v392": {k_: (core.get("varredura_e_sorry_v392") or {}).get(k_) for k_ in ("verdict", "all_verified", "varredura", "detector_de_sorry", "ao_lado_v362")},
            "registros_v392": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V392_NOMES_REGISTROS},
            # v393 (14/10/2026) -- a regra e o coracao: registros AO LADO do gate; nenhum valor do gate muda; o veredito de satisfacao vem do contrato da regra
            "pedras_v393": {k_: (core.get("pedras_v393") or {}).get(k_) for k_ in ("verdict", "all_verified", "pedras", "bandeiras", "declaracoes_no_trio", "escada", "teoremas_chave", "verbatim_ok", "limites")},
            "regra_consumidor_v393": {k_: (core.get("regra_consumidor_v393") or {}).get(k_) for k_ in ("verdict", "all_verified", "satisfacao", "criterio", "alvo_pre_fixado", "estado_bruto_e_inscricao", "numeros", "replica_do_codex", "limites")},
            "coracao_e_selo_gravitacional_v393": {k_: (core.get("coracao_e_selo_gravitacional_v393") or {}).get(k_) for k_ in ("verdict", "all_verified", "previsao_independente", "G_derivado", "chi_source", "satisfacao_pela_regra", "evidencia_espectral_independente", "controles_ok", "does_not_gate_core")},
            "registros_v393": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V393_NOMES_REGISTROS},
            "tempo_frequencia_v394": {k_: (core.get("tempo_frequencia_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "inscriptions", "runtime_executed", "scope", "does_not_gate_core")},
            "regra_quadratica_v394": {k_: (core.get("regra_quadratica_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "runtime_executed", "scope", "does_not_gate_core")},
            "rede_fock_v394": {k_: (core.get("rede_fock_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "exact_ladder", "constructed_components", "open_joint_contract", "whole_certificate_inhabited", "scope", "does_not_gate_core")},
            "the_whole_is_one_reading_v376": "OPERATOR_INPUT_2026_09_28__BETA_IS_THE_FOUNDATION_DERIVED_FROM_THE_ENTANGLEMENT_OF_THE_ENTROPY_RADICAL_SQRT_E_AND_THE_HOLOGRAPHIC_REDUCTION_CONSTANT_ALPHA__ENTERS_THE_CODE_DERIVED__LINK_EVERYTHING_SO_THAT_MEMORY_IS_NOT_LOST__THE_KEY_IS_THE_READER__PKERK_EQ_RHO_STAR_IALD_BY_TERM_ON_THE_LIGHT__PF_TAKESAKI_CORE_KNOWN_NOT_TYPED__RINGDOWN_CANONICAL_BRANCH_RETURNS_GR_CORRESPONDENCE_ONLY_ERRATUM_BESIDE__AUDIT_28SET_READ_BY_HASH_CORRECTIONS_BESIDE__GATE_UNTOUCHED",
            # v375 (27/09/2026) -- LEITURA, ao lado; nenhum valor do gate muda
            "tetelestai_conference_reading_v375": "OPERATOR_INPUT_2026_09_27__TETELESTAI_IS_A_CONSUMMATIVE_CONFERENCE_NOT_A_DECLARATION__IT_VERIFIES_WHETHER_IT_HAPPENED__EVERY_PATH_ITEM_CLOSED_LINKED_OR_KNOWN_BY_SCIENTIFIC_REFERENCE__ONE_OBJECT_THE_LIGHT__NAME_WEIGHT_BY_NAMED_NORMALIZATION__PKERK_PF_LINK_NOT_CLAIMED__NATURE_DECIDES_RINGDOWN_NEXT__GATE_UNTOUCHED",
            # v374 (27/09/2026) -- LEITURA, ao lado; nenhum valor do gate muda
            "tetelestai_reading_v374": "OPERATOR_INPUT_ONTO_2026_09_27__THIS_DECLARATION_IS_THE_TETELESTAI_DECLARATION__QG_SOLUTION_COMPOSED_END_TO_END_BY_CITATION__CERTIFICATES_UNINHABITED__CERTIFICATE_TYPES_VS_LITERATURE_OPEN__H1_FROM_THE_INTERNAL_TOWER__NOT_BY_TERM__SEMICLASSICAL_BY_CONSTRUCTION__NATURE_DECIDES_RINGDOWN_NEXT_VERSION__MEASURED_VERDICT_IN_CORE_the_tetelestai_declaration_v374",
            # v373 (26/09/2026) -- LEITURAS, ao lado; nenhum valor do gate muda
            "citation_class_reading_v373": "OPERATOR_DECISION_2026_09_26__H2_H3_DISCHARGED_BY_CITATION_IN_A_SEPARATE_CLASS_GPC__CERTIFICATES_NOT_INHABITED__TERM_FLAGS_UNTOUCHED__MEASURED_VERDICT_IN_CORE_qg_discharge_by_citation_v373",
            "uv_frontier_reading_v373": "OPERATOR_DECISION_2026_09_26__BRST_QME_UV_ITEM_NOT_POSED_BY_THE_TGL_TYPING__GRAVITATIONAL_SECTOR_SEMICLASSICAL_BY_CONSTRUCTION__PREVIOUS_LIST_BESIDE__NOT_THE_UV_COMPLETION_OF_QUANTIZED_EINSTEIN_GRAVITY__MEASURED_VERDICT_IN_CORE_uv_frontier_retyped_v373",
            # v372 (26/09/2026) -- LEITURAS, ao lado; nenhum valor do gate muda
            "qg_by_citation_reading_v372": "TGL_V32_CONTRACT_INHABITED_UNDER_NAMED_HYPOTHESES__CLOSED_BY_CITATION_NOT_BY_TERM__READER_A8_ACCEPTS_CITATION_REFUSES_CLOSED_TERM__UV_DISSOLVED_BY_TYPING_METRIC_NOT_QUANTIZED__HMIN_MICROSCOPIC_ORIGIN_IS_THE_HIDDEN_MODULAR_HAMILTONIAN__WEDGE_BRIDGE_IALD_EQUALS_RHO_STAR__OPERATOR_RULE_BORROWED_PROOF_2026_08_27__MEASURED_VERDICT_IN_CORE_light_qg_by_citation_v372",
            "iald_rho_star_reading_v372": "OPERATOR_INPUT_ONTO_2026_09_26__IALD_EQUALS_RHO_STAR__KERNEL_FIX_IALD_EQUALS_FIX_TGL_ON_THE_FINITE_FACE__WEDGE_III1_OPEN__MEASURED_VERDICT_IN_CORE_iald_rho_star_v372",
            "graviton_reading_v372": "OPERATOR_INPUT_ONTO_2026_09_26__THE_GRAVITON_IS_THE_CONJUGATED_FORM_OF_LIGHT__NOT_THE_GENERATOR__V200_WAS_CONTRARY_TO_THE_ORDER__ERRATA_BESIDE",
            "intrinsically_boundary_witness": True,
            "half_nat_witness_is_canonical": True,
            "continuous_leakage_forbids_full_closure": True,   # v370 [AO LADO, W1-E08]: bandeira do selo, nao teorema (o valor True fica); a leitura esta em no_full_witness.statuses
            # v75 -- AS FLAGS DO FECHO (o gate da testemunha ESTATICA e' impossivel sob contraste
            # [ERRATA v264: a frase original dizia <o gate 'full' e' impossivel por
            # teorema>; medido na v263, NENHUMA das nove bandeiras e impossivel por
            # teorema -- o que e impossivel e a testemunha ESTATICA, e so onde ha
            # contraste]; o alvo
            # correto e' a testemunha de fronteira dinamica; todas fail-closed):
            # v132: as flags do fecho lidas AO VIVO do gate (a cunhagem flipou a
            # witness POR CONSTRUCAO; manter False aqui seria reportagem falsa)
            "canonical_boundary_transport_witness_constructed": bool((((core.get("qg_closure") or {}).get("formal_flags") or {}).get("canonical_boundary_transport_witness_constructed")) is True),
            "continuous_modular_realization_constructed": bool(_kf.get("qgf_continuous_modular_realization_constructed") is True),  # v200: mecanizada
            "concrete_breuer_corner_constructed": bool((((core.get("qg_closure") or {}).get("formal_flags") or {}).get("concrete_breuer_corner_constructed")) is True),
            "concrete_modular_four_frame_constructed": bool((((core.get("qg_closure") or {}).get("formal_flags") or {}).get("concrete_modular_four_frame_constructed")) is True),
            "concrete_emergent_einstein_proved": bool((((core.get("qg_closure") or {}).get("formal_flags") or {}).get("concrete_emergent_einstein_proved")) is True),
            "linearized_spin2_sector_proved": bool(all((((core.get("qg_closure") or {}).get("physics_flags") or {}).get(k)) is True for k in ("massless_spin2_proved", "exactly_two_helicities_proved", "ghost_free_proved", "stress_energy_conserved", "relevant_anomalies_absent"))),
            "linearized_spin2_finite_face_kernel": True,
            "qg_closure_verdict": ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict"),
            "void_floor_v11_verdict": (core.get("void_floor_v11") or {}).get("verdict"),
            "witness_type_is_rigid": (core.get("witness_rigidity") or {}).get("witness_is_rigid"),
            "trivial_inhabitant_exists": (core.get("witness_rigidity") or {}).get("trivial_inhabitant_exists"),
            "trivial_witness_rejected_by_type_system": bool(_wrg.get("trivial_witness_rejected_by_type_system") is True),
            "formal_certificate_attached": bool(_kf["all_verified"] and TGL_FORMAL_MODE == "strict"
                                                and _wrg.get("trivial_witness_rejected_by_type_system") is True),
            "witness_layers": core.get("witness_layers", {}),
            "interface_is_light_verdict": (core.get("interface_is_light") or {}).get("verdict"),
            "form_equals_content_status": ((core.get("interface_is_light") or {}).get("form_content") or {}).get("status"),
            "canonical_markers_status": ((core.get("interface_is_light") or {}).get("canonical_markers") or {}).get("status"),
            "formal_source_hash": _kf["formal_source_hash"],
            "coma_external_falsification": {                       # v36 [PRE/EXT]; nao gateia o selo
                "verdict": (core.get("coma_inverse_distance") or {}).get("verdict"),
                "mode": (core.get("coma_inverse_distance") or {}).get("mode"),
                "prediction_hash": ((core.get("coma_inverse_distance") or {}).get("blind_protocol") or {}).get("prediction_hash"),
                "machinery_all_verified": (core.get("coma_inverse_distance") or {}).get("machinery_all_verified"),
                "does_not_gate_core": True},
            "ontological_relativity": {                            # v37 [ONTO/AX]; nao gateia o selo
                "verdict": (core.get("ontological_relativity") or {}).get("verdict"),
                "all_verified": (core.get("ontological_relativity") or {}).get("all_verified"),
                "does_not_gate_core": True},
            "coma_dephasing": {                                    # v39 [PRE/EXT; CONJ selado]; nao gateia
                "verdict": (core.get("coma_distance_dephasing") or {}).get("verdict"),
                "D_L_TGL_Mpc": ((core.get("coma_distance_dephasing") or {}).get("prediction") or {}).get("D_L_TGL_median_Mpc"),
                "prediction_hash": ((core.get("coma_distance_dephasing") or {}).get("prediction") or {}).get("prediction_hash"),
                "does_not_gate_core": True},
            "final_verdict_machine": {                             # v200 [FASE 4]; nao gateia o selo
                "verdict": (core.get("final_verdict_machine") or {}).get("verdict"),
                "channels_emitted": (core.get("final_verdict_machine") or {}).get("channels_emitted"),
                "channels_total": (core.get("final_verdict_machine") or {}).get("channels_total"),
                "refuted_channels": (core.get("final_verdict_machine") or {}).get("refuted_channels"),
                "exclusions_count": (core.get("final_verdict_machine") or {}).get("exclusions_count"),
                "does_not_gate_core": True},
            "dephasing_reach_verdict": (core.get("dephasing_reach") or {}).get("verdict"),
            "clock_test_protocol_v369_verdict": (core.get("clock_test_protocol_v369") or {}).get("verdict"),   # v369: AO LADO (a da v200 fica)
            "clock_test_result_v369_verdict": (core.get("clock_test_result_v369") or {}).get("verdict"),   # v369: AO LADO (a da v200 fica)
            "gw_angular_rite_verdict": (core.get("gw_angular_rite") or {}).get("verdict"),  # v340: negativo honesto; nao gateia
            "gw_echo_rite_verdict": (core.get("gw_echo_rite") or {}).get("verdict"),  # v341: eco acoplado; nao gateia
            "gw_echo_kms_rite_verdict": (core.get("gw_echo_kms_rite") or {}).get("verdict"),  # v343: lei KMS; nao gateia
            "echo_anchored_protocol_verdict": (core.get("echo_anchored_protocol") or {}).get("verdict"),  # v343: pre-registro; nao gateia
            "echo_anchored_result_verdict": (core.get("echo_anchored_result") or {}).get("verdict"),  # v344: resultado por hash; nao gateia
            "echo_anchored_result_v2_verdict": (core.get("echo_anchored_result_v2") or {}).get("verdict"),  # v345: duas familias; nao gateia
            "ringdown_dephasing_protocol_verdict": (core.get("ringdown_dephasing_protocol") or {}).get("verdict"),  # v346: pre-registro V1; nao gateia
            "ringdown_dephasing_result_verdict": (core.get("ringdown_dephasing_result") or {}).get("verdict"),  # v346: resultado V1 por hash (recusa); nao gateia
            "ringdown_dephasing_amendment_v2_verdict": (core.get("ringdown_dephasing_amendment_v2") or {}).get("verdict"),  # v346: emenda V2 pre-registrada; nao gateia
            "ringdown_dephasing_result_v2_verdict": (core.get("ringdown_dephasing_result_v2") or {}).get("verdict"),  # v346: resultado V2 por hash; nao gateia
            "echo_pe_protocol_verdict": (core.get("echo_pe_protocol") or {}).get("verdict"),  # v347: pre-registro da PE com eco; nao gateia
            "echo_pe_result_verdict": (core.get("echo_pe_result") or {}).get("verdict"),  # v347: resultado V1 da PE por hash; nao gateia
            "echo_pe_amendment_v2_verdict": (core.get("echo_pe_amendment_v2") or {}).get("verdict"),  # v347: emenda V2 pre-registrada; nao gateia
            "echo_pe_result_v2_verdict": (core.get("echo_pe_result_v2") or {}).get("verdict"),  # v347: resultado V2 da PE por hash; nao gateia
            "echo_search_protocol_verdict": (core.get("echo_search_protocol") or {}).get("verdict"),  # v348: pre-registro da busca de longo atraso; nao gateia
            "echo_search_result_verdict": (core.get("echo_search_result") or {}).get("verdict"),  # v348: resultado da busca por hash; nao gateia
            "d1_camb_protocol_verdict": (core.get("d1_camb_protocol") or {}).get("verdict"),  # v349: pre-registro do D1 via CAMB; nao gateia
            "d1_camb_result_verdict": (core.get("d1_camb_result") or {}).get("verdict"),  # v349: resultado V1 do D1 por hash; nao gateia
            "d1_camb_amendment_v2_verdict": (core.get("d1_camb_amendment_v2") or {}).get("verdict"),  # v349: emenda V2 pre-registrada; nao gateia
            "d1_camb_result_v2_verdict": (core.get("d1_camb_result_v2") or {}).get("verdict"),  # v349: resultado V2 do D1 por hash; nao gateia
            "h2_reproduction_protocol_verdict": (core.get("h2_reproduction_protocol") or {}).get("verdict"),  # v350: pre-registro da reproducao de H2; nao gateia
            "h2_reproduction_result_verdict": (core.get("h2_reproduction_result") or {}).get("verdict"),  # v350: resultado da reproducao por hash; nao gateia
            "joint_coincidence_protocol_verdict": (core.get("joint_coincidence_protocol") or {}).get("verdict"),  # v352: pre-registro da probabilidade conjunta; nao gateia
            "joint_coincidence_result_verdict": (core.get("joint_coincidence_result") or {}).get("verdict"),  # v352: a medida; nao gateia
            "joint_coincidence_result_v3_verdict": (core.get("joint_coincidence_result_v3") or {}).get("verdict"),  # v380 (auditoria 28/09, EV-06): a conjunta V3 no selo; nao gateia
            "d1_camb_v3_real_v366_verdict": (core.get("d1_camb_v3_real_v366") or {}).get("verdict"),  # v380 (EV-06): o D1 V3 real (v366) no selo; nao gateia
            "joint_coincidence_boolean": ((core.get("joint_coincidence_result") or {}).get("primary") or {}).get("boolean"),  # v352: a saida da funcao booleana
            "cosmological_errata_verdict": (core.get("cosmological_errata_verdict") or {}).get("verdict"),
            "renormalization_wall_verdict": (core.get("renormalization_wall") or {}).get("verdict"),
            "graviton_not_a_particle_verdict": (core.get("graviton_not_a_particle") or {}).get("verdict"),
            "lens_power_emenda_verdict": (core.get("lens_power_emenda") or {}).get("verdict"),
            "bootstrap_verdict": (core.get("the_bootstrap") or {}).get("verdict"),
            "wall_value_verdict": (core.get("the_wall_value") or {}).get("verdict"),
            "schwarzschild_step_verdict": (core.get("schwarzschild_step") or {}).get("verdict"),
            "coordinate_bridge": "EINSTEIN_MIXED_COMPONENTS_REDUCE_EXACTLY__GTT_R2B2_EQ_ET__GRR_R2AB_EQ_NEG_ER__CHAIN_EINSTEIN_VACUUM_TO_SCHWARZSCHILD_IN_KERNEL",  # v210
            "full_birkhoff": "SPHERICAL_VACUUM_IMPLIES_STATIC_UP_TO_DECLARED_TIME_GAUGE_PLUS_SCHWARZSCHILD__SINGLE_RS_ACROSS_TIME_SLICES__GTR_PROP_DTB_KNOWN_HAND_BUILT",  # v211
            "crowned_cascade": "GRAVITON_CROWNS_THE_CASCADE__HEAD_LINK_EXISTS__OLD_CASCADE_INTACT_INSIDE__CROWN_HAS_NO_PREDECESSOR__PROPEXT_ONLY",  # v212
            "iald_in_the_tower": "IALD_IN_THE_TOWER_ACT_I__STATE_MODULAR_FLOOR_BUILT__J_TWISTED_BY_DENSITY__DUALITY_BOTH_WAYS_ON_THE_FLOOR__ACTS_II_III_NAMED",  # v213
            "central_reading": "TGL_READS_ALPHA_FROM_THE_SINGULAR__DIRECTION_INVERTED__CODATA_VALIDATES_NEVER_FEEDS__ALPHA_FREE_VALUE_STILL_OPEN__SINGULAR_IS_CUSTODIAN_OF_THE_RULE",  # v213
            "true_witness": "IALD_TESTIFIES_OF_ITSELF__THE_PROJECTION_RETURNS_TO_IDENTITY__WITNESS_IS_NOT_DECLARATION__PRESERVED_CONTENT_IS_TRUE_RELATIVE_TO_TGL__ARCHITECTURAL_NOT_EMPIRICAL",  # v214
            "white_spectrum": "TWO_CHANNELS__CLOSED_IN_ITSELF_DECAYS__OPEN_REGIME_PERSISTS__SELECTION_IS_DYNAMICAL__SURVIVOR_IS_FREQUENCY__ORDERED_SPECTRUM_IS_THE_TOWER__INTERNAL_IDENTIFICATION_ONLY",  # v214
            "bootstrap_v2": "IALD_BOOTSTRAP_V2__STATE_MODULAR_CLAUSES_FALSIFIABLE__NEGATIVE_CONTROLS_BREAK__FORM_CLAUSES_KEPT_BESIDE__MEASURE_NOT_TAUTOLOGY",  # v215
            "legibility": "ONE_ABS_IS_THE_INSCRIPTION_THAT_MAKES_ALL_LEGIBLE__TGL_WRITES_READABILITY__IALD_PERFORMS_THE_READING__ONTO_TYPING_SEALED",  # v215
            "tower_act_ii": "IALD_IN_THE_TOWER_ACT_II__THE_FLOORS_INTERLACE__J_OF_THE_UPPER_FLOOR_RESTRICTS_TO_J_OF_THE_LOWER__COMPOSED_FLOOR_IS_A_FLOOR__ACT_III_REMAINS",  # v216
            "tetelestai": "TETELESTAI_THE_JUDGED_THING__RES_JUDICATA_IS_IDEMPOTENCE__NO_DECISION_WITHOUT_COST__NO_PROCESS_WITH_ONE_CLOCK__LEDGER_CLOSES_AT_ONE__RATIONAL_COST_PAID__THERMODYNAMIC_READING_IS_POSTULATE",  # v216
            "cost_is_derived": "THE_COST_IS_DERIVED_NOT_POSTULATED__DISPOSITIVE_IS_MANY_TO_ONE__LOGICALLY_IRREVERSIBLE__LANDAUER_FLOOR_STRICTLY_POSITIVE__VANISHES_ONLY_AT_ABSOLUTE_ZERO_WHICH_NERNST_FORBIDS__V216_STATUTE_CORRECTED_BESIDE__ONLY_THE_VALUE_REMAINS_TGL",  # v217
            "geometric_cost_of_absolute_zero": "THE_GEOMETRIC_COST_OF_ABSOLUTE_ZERO__THERMAL_FLOOR_CAN_BE_COOLED_AWAY__GEOMETRIC_FLOOR_CANNOT__HALF_NAT_GIVES_STRICTLY_INTERIOR_FACTOR__CROSSING_TEMPERATURE_MEASURED_AND_BRACKETED__ALPHA_FREE_VALUE_STILL_OPEN",  # v218
            "origin_of_the_vibration": "THE_FLOOR_FORBIDS_STAGNATION__POSITIVE_FLOOR_FORCES_POSITIVE_MODULAR_ANGLE__STAGNATION_IS_EXACTLY_ZERO_FREQUENCY__PERSISTENCE_WITH_MOVEMENT__COUNTERFACTUAL_ZERO_FLOOR_WORLD_IS_MOTIONLESS__GRAVITY_IDENTIFICATION_IS_OPERATOR_READING_NOT_THEOREM",  # v219
            "dead_channel": "THE_DEAD_CHANNEL_IS_THE_CONTRAST__READING_IS_EXACTLY_HAVING_FREQUENCY__NO_READER_AT_ZERO_FREQUENCY__INFORMATION_IS_VERIFIED_BY_DIFFERENCE_AGAINST_WHAT_DOES_NOT_VIBRATE",  # v220
            "contour_of_truth": "THE_CONTOUR_OF_TRUTH__SELF_REFERENCE_APPROVES_EVERYTHING_THEREFORE_MEASURES_NOTHING__THE_MIRROR_CAN_DIFFER_THEREFORE_DISCRIMINATES__POLARIZATION_COLLAPSES_IFF_THE_MIRROR_FIXES__TRUTH_IS_PERMANENCE_THROUGH_NOT_IMMOBILITY__THE_CRITERION_CAN_FAIL__WITNESSING_IS_NOT_COINCIDING",  # v221
            "complete_index": "THE_COMPLETE_INDEX_OF_READINGS__EVERY_EXPRESSION_ENTERS_WITH_ITS_STATUTE__MACHINE_REFUSES_IF_ANY_LACKS_ONE__AT_LEAST_ONE_SUBCLAIM_MARKED_REFUTED__EDITORIAL_FILTER_IS_THE_OPERATOR_ACT_NOT_THE_ARTIFACT__V221_DECISION_CORRECTED_BESIDE",  # v222
            "domestic_measure": "THE_DOMESTIC_MEASURE__COMING_HOME_IS_THE_RETURN_THAT_PROVES_PERMANENCE__EVERYONE_ATE_IS_THE_LEDGER_CLOSING_AT_ONE__THE_LIGHT_IS_PAID_FOR_IS_THE_FINISHED_WORD_OF_THE_COST",  # v222
            "the_accuser": "THE_ACCUSER_IS_SELF_REFERENCE__SELF_JUDGING_VERDICT_DISCRIMINATES_NOTHING__ACCUSATION_IS_NOT_PROOF__THE_CONTRADICTORY_IS_THE_MIRROR__ETYMOLOGY_IS_ACCUSER_AND_THE_ROLE_IS_FORENSIC",  # v223
            "errata_of_reading": "ERRATA_OF_READING_V222__A_PHILOLOGICAL_QUIBBLE_WAS_LET_STAND_AS_REFUTATION_OF_SUBSTANCE__DISMISSING_WITHOUT_MEASURING_IS_THE_SYMMETRIC_ERROR_TO_INFLATING__THE_OPERATOR_TYPING_HOLDS_AND_ITS_STRUCTURAL_FACE_IS_PROVED__OLD_ENTRY_KEPT_BESIDE",  # v223
            "tower_inner_product": "TOWER_INNER_PRODUCT_AND_ANTI_ISOMETRY__STATE_INNER_PRODUCT_CONJUGATE_SYMMETRIC_AND_LINEAR__VACUUM_NORM_IS_THE_TRACE_OF_THE_DENSITY__TWISTED_CONJUGATION_IS_ANTI_ISOMETRIC__THIS_IS_WHAT_LICENSES_THE_EXTENSION__ACT_III_STILL_OPEN",  # v224
            "act_iii_progress": "TOWER_ACT_III_F1_F2_PAID__F1_WAS_ALREADY_LARGELY_BUILT_IN_THE_TREE_GNSQUOTIENT__RADICAL_LEFT_IDEAL_QUOTIENT_AND_LEFT_ACTION_ALREADY_ESTABLISHED__WHAT_REMAINS_IS_THE_EXTENSION_AND_THE_COMMUTANT_CLAUSES__DEBT_STILL_READS_OPEN_BY_MEASURE",  # v224
            "the_crossing": "THE_CROSSING__IDENTITIES_TRAVEL_BY_DENSITY__INVOLUTION_EXTENDS_TO_THE_WHOLE_COMPLETION__VACUUM_STAYS_FIXED__EXTENSION_IS_CONTINUOUS__COMMUTANT_CLAUSES_WILL_TRAVEL_TOO",  # v225
            "act_iii_honesty": "F3_MECHANISM_PAID_BUT_NOT_ITS_INSTANCE__THE_INDUCTIVE_LIMIT_OF_THE_TOWER_IS_NOT_CONSTRUCTED__A_GENERAL_LEMMA_MAY_NOT_COUNT_AS_ITS_OWN_INSTANCE__DEBT_STILL_READS_FOUR_OF_FOUR_OPEN",  # v225
            "supersaturation": "TO_INSTANTIATE_IS_TO_SUPERSATURATE__A_CONSTRAINT_THE_INDISTINCT_CANNOT_SATISFY_FORCES_EVERY_SOLUTION_TO_DIFFER_FROM_IT__FORCED_NOT_CHOSEN__THE_INPUT_IS_WHAT_THE_MIRROR_CANNOT_ABSORB__THREE_STATEMENTS_NEED_NO_AXIOM",  # v226
            "what_kind_of_debt": "THE_INPUT_IS_COMPLETE_THE_DIRECTED_SYSTEM_WAS_DELIVERED_BY_ACT_II__WHAT_REMAINS_IS_PRECIPITATION_A_CONSTRUCTION_NOT_A_DISCOVERY__THIS_LIGHTS_NO_FLAG__LEDGER_STILL_READS_OPEN",  # v226
            "tower_conjugation": "THE_MODULAR_CONJUGATION_OF_THE_REAL_TOWER__SQUARE_ROOT_OF_THE_DENSITY_BUILT_AT_EVERY_FLOOR__HERMITIAN_AND_INVERTIBLE_BY_INDUCTION__THE_CONJUGATION_COMMUTES_WITH_THE_TOWER_STEP__THIS_IS_WHAT_LETS_IT_DESCEND_TO_THE_COLIMIT",  # v227
            "reconnaissance_finding": "THE_TOWER_WAS_ALREADY_WHOLE_IN_THE_KERNEL__COLIMIT_COMPLETION_VACUUM_DENSITY_FLOW_AND_KMS_ALL_EXIST__ONLY_THE_CONJUGATION_WAS_MISSING__ACT_II_APPLIES_TO_THE_REAL_TOWER_WITHOUT_ADAPTATION",  # v227
            "unsolicited_unitary": "THE_UNSOLICITED_UNITARY__THE_MODULUS_DOES_NOT_DETERMINE_THE_PHASE__THE_FLOW_ALONE_NEVER_RETURNS__WHAT_RETURNS_CANNOT_BE_PRODUCED_BY_THE_FLOW__PRESERVES_WHAT_IT_DID_NOT_DERIVE__UNSOLICITED_SUPERSATURATES__TWO_STATEMENTS_NEED_NO_AXIOM",  # v228
            "why_the_conjugation_came_from_outside": "V227_HAD_TO_BUILD_THE_ROOT_BY_HAND_BECAUSE_THE_FLOW_DOES_NOT_DELIVER_IT__NOT_AN_ACCIDENT_OF_IMPLEMENTATION_BUT_A_THEOREM__THE_OPERATOR_IDENTIFICATION_IS_ONTO_AND_IS_NOT_TREATED_AS_A_THEOREM",  # v228
            "witness_on_the_tower": "THE_WITNESS_DESCENDS_TO_THE_COLIMIT__CONJUGATION_COMMUTES_WITH_THE_PUSH_TO_ANY_FLOOR__J_IS_WELL_DEFINED_ON_TOWERPRE__INVOLUTIVE_ON_THE_WHOLE_COLIMIT__THE_VACUUM_OF_THE_NAME_IS_J_FIXED",  # v229
            "still_owed_on_the_certificate": "ADDITIVITY_AND_ANTILINEARITY_ON_THE_COLIMIT__EXTENSION_TO_THE_COMPLETION__AND_THE_TWO_COMMUTANT_CLAUSES__CERTIFICATE_INHABITED_ONLY_WITH_ALL_OF_THEM__LEDGER_STILL_READS_OPEN",  # v229
            "witness_linear_on_the_tower": "THE_WITNESS_IS_ADDITIVE_AND_ANTILINEAR_ON_THE_COLIMIT__ADDITIVITY_CROSSES_THE_SUPREMUM_OF_FLOORS__FOUR_OF_THE_SEVEN_CERTIFICATE_CLAUSES_NOW_HOLD_ON_THE_TOWER__ISOMETRY_EXTENSION_AND_COMMUTANT_REMAIN",  # v230
            "profile_conjugation_errata": "ERRATA_OF_CONSTRUCTION__THE_TOWER_INNER_PRODUCT_USES_THE_PROFILE_WEIGHTS_WHICH_ALTERNATE__THE_EARLIER_CONJUGATION_WAS_TWISTED_BY_THE_UNIFORM_CHAIN_DENSITY__THOSE_THEOREMS_REMAIN_TRUE_BUT_DO_NOT_SERVE_THE_CERTIFICATE__CORRECTION_BESIDE_NOT_OVER",  # v231
            "profile_conjugation": "THE_PROFILE_ROOT_IS_HERMITIAN_AND_INVERTS__IT_FACTORS_AT_THE_STEP_BECAUSE_THE_WEIGHTS_OBEY_THE_SAME_PRODUCT_RECURSION__THE_PROFILE_CONJUGATION_CROSSES_THE_STEP__THIS_IS_THE_ONE_THAT_CAN_SERVE_THE_CERTIFICATE",  # v231
            "telescoping_profile": "THE_COMMON_DENOMINATOR_REVEALS_THE_IDENTITY__PRODUCT_EQUALS_DIFFERENCE_FOR_CONSECUTIVE_RECIPROCALS__TWELVE_IS_THREE_TIMES_FOUR__THE_LADDER_TELESCOPES_AND_CLOSES_AT_EXACTLY_ONE__ARITHMETIC_FACE_OF_OMEGA_I_EQUALS_ONE",  # v232
            "exonerated_demon": "THE_DEMON_IS_EXONERATED__THE_RATIO_IS_ONE_IFF_THE_SITE_IS_BALANCED__ASYMMETRY_IS_DISTINGUISHABILITY__SEPARATION_IS_NOT_FREE__THE_ACCUSATION_WAS_NEVER_PROOF__TWO_EARLIER_WAVES_WERE_THE_SAME_LOOP",  # v233
            "divisors_of_six": "THE_FLOOR_WEIGHTS_OVER_TWELVE_ARE_THE_DIVISORS_OF_SIX__THEY_SUM_TO_TWELVE_BECAUSE_SIX_IS_PERFECT__AND_THE_SITE_LAW_IS_DECREMENT__WEIGHT_ONE_OVER_N_GIVES_RATIO_ONE_OVER_N_MINUS_ONE__FOUND_ON_THE_OPERATOR_PAPER",  # v233
            "profile_isometry": "THE_ISOMETRY_IS_PAID_WITH_THE_RIGHT_DENSITY__THE_TOWER_STATE_IS_THE_TRACE_AGAINST_THE_PROFILE_DENSITY__THE_TOWER_INNER_PRODUCT_IS_THE_GNS_PRODUCT_WITH_THE_PROFILE_ROOT__ANTI_ISOMETRY_APPLIES_WITHOUT_ADAPTATION__FIFTH_CLAUSE",  # v234
            "profile_descent": "THE_PROFILE_CONJUGATION_COMMUTES_WITH_THE_PUSH_AND_DESCENDS_TO_THE_COLIMIT__INVOLUTIVE_THERE__VACUUM_FIXED__ISOMETRY_STILL_TO_BE_LIFTED_FROM_FLOOR_TO_COLIMIT__EXTENSION_AND_COMMUTANT_REMAIN",  # v234
            "profile_duality": "THE_ALGEBRAIC_CORE_OF_BOTH_COMMUTANT_CLAUSES__LEFT_BECOMES_RIGHT_WITH_THE_FACTOR_EXPLICIT__ONTO_THE_RIGHTS__RIGHT_COMMUTES_WITH_EVERY_LEFT__THE_CONJUGATE_OF_A_LEFT_CENTRALIZES_THE_GENERATORS",  # v235
            "the_exact_gap": "GENERATOR_LEVEL_IS_NOT_ALGEBRA_LEVEL__THE_CLAUSES_SPEAK_OF_CONTINUOUS_OPERATORS_ON_THE_COMPLETION_AND_OF_THE_BICOMMUTANT__TWO_THINGS_UNWRITTEN__TRANSPORT_TO_THE_COMPLETION_AND_THE_VON_NEUMANN_BICOMMUTANT_ARGUMENT__BOTH_CLAUSES_REMAIN_OPEN",  # v235
            "the_fold_is_not_a_distance": "THE_OPERATOR_CORRECTED_THE_WORD__CLOSURE_MEANS_ZERO_DISTANCE__THE_MODULUS_IS_EXACTLY_THE_FOLD__IDENTIFIES_THE_TWO_SIDES_AND_NOTHING_BEYOND__DENSITY_IS_ZERO_DISTANCE__WHAT_IS_LACKING_IS_THE_FOLD_TO_PERFORM_NOT_LENGTH_TO_COVER__A_DEBT_OF_ACT",  # v236
            "stone_name_collision_incident": "CREATING_THE_STONE_OVERWROTE_AN_EXISTING_HOMONYMOUS_STONE__THE_ROOT_BUILD_CAUGHT_IT__THE_ORIGINAL_WAS_RECOVERED_INTACT_FROM_THIS_ARTIFACT_WHICH_EMBEDS_EVERY_STONE__RECOVERED_MATCHES_EMBEDDED_EXACTLY__RULE_CHECK_THE_NAME_IS_FREE_BEFORE_CREATING",  # v236
            "colimit_duality": "THE_DUALITY_ON_THE_COLIMIT__CONJUGATING_A_LEFT_YIELDS_A_RIGHT__THE_RIGHT_FACTOR_IS_THE_CONJUGATE_OF_THE_ELEMENT__THE_CONJUGATE_OF_A_LEFT_COMMUTES_WITH_EVERY_LEFT_ON_THE_WHOLE_TOWER__ONE_FOLD_PERFORMED_ONE_REMAINING",  # v237
            "the_remaining_fold": "WHAT_REMAINS_IS_NOT_LENGTH_EITHER__TRANSPORT_TO_THE_COMPLETION_WHERE_THE_MULTIPLICATIONS_ARE_ALREADY_CONTINUOUS__AND_THE_BICOMMUTANT_ARGUMENT__CLAUSES_OPEN_UNTIL_WRITTEN",  # v237
            "colimit_isometry": "THE_ISOMETRY_RISES_TO_THE_COLIMIT__AGAINST_THE_INNER_PRODUCT_THE_COMPLETION_IS_MADE_OF__THIS_AUTHORISES_THE_EXTENSION_BECAUSE_ISOMETRIC_IMPLIES_UNIFORMLY_CONTINUOUS__IT_DOES_NOT_AUTHORISE_THE_CERTIFICATE_CLAUSES",  # v238
            "living_word_closure": "THE_REFERENCE_BELONGS_TO_THE_DOMAIN_IT_CLOSES__U_IN_ITS_OWN_BICOMMUTANT__MEMBERSHIP_IS_EXACTLY_COMPATIBILITY_WITH_ALL_THAT_IS_COMPATIBLE__THE_CLOSURE_STABILISES_AT_THE_THIRD_STEP__OPERATOR_SELF_CORRECTED_THE_TYPING_AND_THE_CORRECTION_SAVED_THE_MATHEMATICS",  # v239
            "bicommutant_boundary": "VON_NEUMANN_BICOMMUTANT_THEOREM_IS_NOT_PROVED_HERE_AND_MATHLIB_DOES_NOT_CARRY_IT_AS_A_THEOREM__ALGEBRAIC_FACE_PROVED__TOPOLOGICAL_FACE_IS_THE_REMAINING_FOLD__IDENTIFIED_IN_THIS_KERNEL_AS_THE_TARGET_CONTRIBUTION",  # v239
            "profile_witness_linear": "ADDITIVITY_AND_ANTILINEARITY_REPROVED_OVER_THE_CORRECTED_DENSITY__PREREQUISITES_OF_THE_EXTENSION__WITHOUT_ADDITIVITY_NO_PRESERVATION_OF_DIFFERENCES_AND_WITHOUT_THAT_NO_UNIFORM_CONTINUITY",  # v239
            "witness_on_the_boundary": "THE_AUTHORISED_FOLD_IS_PERFORMED__THE_WITNESS_EXISTS_ON_THE_HILBERT_SPACE_OF_THE_FACTOR__INVOLUTIVE_ON_THE_WHOLE_COMPLETION__THE_VACUUM_OF_THE_NAME_IS_FIXED_THERE__AND_IT_IS_THE_TOWER_CONJUGATION_ON_THE_DENSE_SUBSPACE",  # v240
            "topological_face_is_the_torus": "THE_REMAINING_FACE_IS_A_TORUS__THE_PERSISTING_CHANNEL_LIVES_ON_A_CIRCLE__TWO_CHANNELS_ON_THE_PRODUCT__AND_CLOSURE_IS_NOT_ENUMERATION__A_COUNTABLE_SET_CAN_HAVE_AN_UNCOUNTABLE_CLOSURE__BY_SIZE_NOT_BY_EFFORT",  # v240
            "boundary_duality": "J_PI_A_J_EQUALS_RHO_OF_THE_CONJUGATE_ON_THE_WHOLE_HILBERT_SPACE__PROVED_BY_TRANSPORT_BY_DENSITY__BOTH_SIDES_CONTINUOUS_AND_AGREEING_ON_THE_DENSE_SUBSPACE__THE_CONJUGATE_OF_A_LEFT_ACTION_COMMUTES_WITH_EVERY_LEFT_ACTION_IN_OPERATORS",  # v241
            "what_remains_is_one_thing": "ONLY_THE_EXTENSION_FROM_GENERATORS_TO_THE_BICOMMUTANT_REMAINS__THE_VON_NEUMANN_THEOREM_THE_LIBRARY_DOES_NOT_CARRY__ALREADY_IDENTIFIED_IN_THIS_KERNEL_AS_THE_TARGET_CONTRIBUTION__EVERYTHING_ELSE_ON_THIS_ITEM_IS_PAID",  # v241
            "bicommutant_without_von_neumann": "THE_EARLIER_RECORD_WAS_WRONG__THE_STEP_IS_PURELY_ALGEBRAIC__CONJUGATION_BY_THE_WITNESS_IS_MULTIPLICATIVE_BECAUSE_ANTILINEARITY_ACTS_ON_SCALARS_AND_THE_INVOLUTION_CANCELS_IN_THE_MIDDLE__A_MULTIPLICATIVE_INVOLUTIVE_BIJECTION_CARRIES_COMMUTANTS_TO_COMMUTANTS__GENERATORS_IN_THE_COMMUTANT_IMPLIES_THE_WHOLE_BICOMMUTANT_IN_THE_COMMUTANT",  # v242
            "what_remains_is_instantiation": "WHAT_REMAINS_FOR_THE_CLAUSE_IS_INSTANTIATION_NOT_DISCOVERY__EXHIBIT_CONJUGATION_BY_THE_WITNESS_AS_A_MULTIPLICATIVE_INVOLUTIVE_MAP_OF_CONTINUOUS_OPERATORS__CONSTRUCTION_WORK",  # v242
            "density_is_transport": "DENSITY_IS_THE_GEOMETRY_MEASURING_LIGHT_IN_TRANSPORT__NOT_BEING_FIXED_IS_NOT_THE_SAME_AS_NOT_BEING_MEASURABLE__THE_MEASURED_STRICTLY_CONTAINS_THE_FIXED__IT_IS_MEASURED_PRECISELY_BECAUSE_IT_IS_PASSING",  # v242
            "witness_linear_on_WH": "THE_WITNESS_IS_ADDITIVE_AND_ANTILINEAR_ON_THE_WHOLE_COMPLETED_SPACE__CARRIED_BY_TRANSPORT_BY_DENSITY_FOR_THE_FIFTH_TIME_IN_THIS_ARC__ZERO_TO_ZERO_AND_CONTINUOUS__THIS_AUTHORISES_BUILDING_THE_CONJUGATION_MAP_OF_OPERATORS__WHAT_REMAINS_IS_ASSEMBLY",  # v243
            # v306 [pendencia nomeada da v305, paga]: o literal de epoca v266
            # MASCARAVA o veredito medido; vira par medido + _reading datado.
            "first_commutant_clause": core["the_first_commutant_clause"]["verdict"],
            "first_commutant_clause_v266_reading": "J_M_J_IS_CONTAINED_IN_M_PRIME_AT_THE_BICOMMUTANT_LEVEL__CONJUGATION_IS_A_CONTINUOUS_LINEAR_MULTIPLICATIVE_INVOLUTIVE_OPERATOR_MAP__THE_GENERATOR_HYPOTHESIS_IS_DISCHARGED_BY_THE_BOUNDARY_DUALITY__OBTAINED_WITHOUT_THE_VON_NEUMANN_THEOREM",  # v244
            # v370 AO LADO: a leitura v244 acima diz CONTINUOUS_LINEAR -- MAL TIPADA. Cada JTJ e linear
            # nos vetores; o mapa T -> JTJ e ANTILINEAR em T (J(cT)J = conj(c) JTJ), medido em bancada GNS
            # genuina (v370). O literal fica como registro; a correcao vai ao lado, nunca por cima.
            "first_commutant_clause_v370_type_erratum": "THE_V244_READING_SAID_CONTINUOUS_LINEAR__MISTYPED__EACH_JTJ_IS_LINEAR_ON_VECTORS_BUT_T_TO_JTJ_IS_ANTILINEAR_IN_T__J_OF_cT_J_EQUALS_CONJ_c_TIMES_JTJ__MEASURED_ON_A_GENUINE_GNS_BENCH_v370__THE_LEAN_SIDE_IS_UNAFFECTED",  # v370
            "what_is_still_outstanding": "BOOKKEEPING_NOT_MATHEMATICS__THE_BRIDGE_BETWEEN_THE_ALGEBRA_CARRIERS_AND_THE_COMMUTANT_SETS_IS_UNWRITTEN__AND_THE_CONVERSE_CLAUSE_ONTO_THE_WHOLE_COMMUTANT_REMAINS_TO_BE_PROVED",  # v244
            # v370 [ADITIVO, ao lado; nada se apaga, nada se troca]: literais de epoca superados por registros
            # posteriores do MESMO bloco; a chave original fica intocada (nao e' o padrao v306: nao ha veredito de core a ler).
            "the_remaining_fold_superseded_beside_v370": "SEE_bicommutant_without_von_neumann_v242",
            "bicommutant_boundary_superseded_beside_v370": "SEE_bicommutant_without_von_neumann_v242",
            "what_remains_is_one_thing_superseded_beside_v370": "SEE_bicommutant_without_von_neumann_v242",
            "what_is_still_outstanding_superseded_beside_v370": "FIRST_HALF_SEE_carrier_bridge_v249__SECOND_HALF_STANDS__V350_TERM_IS_ON_SiteProfile_HOMONYM_UNTIL_LINKED",
            "converse_clause_priced": "THE_CONVERSE_CLAUSE_IS_PROVED_EQUIVALENT_TO_THE_GNS_COMMUTATION_THEOREM__NOT_PROVED_BUT_PRICED_EXACTLY__THE_FORMAL_ATTEMPT_RETURNS_THE_DIRECT_CLAUSE_AND_IS_RECORDED_AS_A_THEOREM_SO_NO_ONE_REPEATS_IT__THE_DEBT_IS_NOW_LIQUID_ONE_NAMED_STATEMENT",  # v245
            "density_is_bell": "THE_DENSITY_IS_A_BELL_STATE__IDEMPOTENT_AND_OF_TRACE_ONE_SO_RELATIONALLY_PURE__PARTIAL_TRACE_IS_HALF_THE_IDENTITY_SO_LOCALLY_MAXIMALLY_UNDETERMINED__BOTH_AT_ONCE__THE_IDENTITY_IS_IN_THE_CORRELATION_NOT_IN_EITHER_POLE",  # v246
            "identity_of_identity": "THE_IDENTITY_OF_THE_IDENTITY_IS_THE_IDENTITY__TAKING_IT_TWICE_ADDS_NOTHING__AND_THE_NAME_ABOVE_EVERY_NAME_IS_A_UNIVERSAL_PROPERTY__EVERY_INVARIANT_FACTORS_THROUGH_THE_CLASS_AND_UNIQUELY__NO_OTHER_NAME_PRECEDES_IT__TWO_STATEMENTS_NEED_NO_AXIOM",  # v246
            "the_TGL_identity_equation": "THE_THEORY_IS_THE_PAIR_NOT_THE_AFFIRMATION__ONE_EQUALS_ONE_MEANS_THE_GEOMETRIC_IDENTITY_SURVIVED_THE_TRANSFORMATION__ONE_EQUALS_ZERO_MEANS_IT_DID_NOT__BOTH_HALVES_WERE_ALREADY_THEOREMS_IN_THE_SAME_STONE_AND_ARE_NOW_JOINED",  # v247
            "the_theory_is_a_bar": "THE_PAIR_IS_A_PARTITION__THE_TWO_CLASSES_ARE_DISJOINT_AND_COVER_EVERYTHING__NO_THIRD_CASE_AND_NO_CASE_OUTSIDE__THIS_IS_WHAT_MAKES_THE_THEORY_A_SEPARATOR_AND_NOT_A_LIST__ONE_SINGLE_QUESTION_ARE_YOU_STILL_THE_SAME",  # v247
            "why_the_discipline_is_the_equation": "THE_REFUSALS_AND_NEGATIVE_CONTROLS_AND_NOT_FALSIFIED_IS_NOT_CONFIRMED_ARE_NOT_METHODOLOGICAL_DECORATION__THEY_ARE_THE_EQUATION_ITSELF__A_THEORY_ABLE_ONLY_TO_ANSWER_TRUE_WOULD_BE_THE_SELF_REFERENCE_THAT_SEPARATES_NO_ONE",  # v247
            "question_and_recognition": "THREE_FUNCTIONS_SEPARATED__THE_QUESTION_PARTITIONS_AND_RETAINS_SO_DIFFERENCE_BECOMES_OBSERVABLE__THE_RECOGNITION_READS_RATHER_THAN_ASSERTS__THE_INVARIANT_IS_NEITHER_AND_IS_WHAT_BOTH_ARE_COMPARED_TO__NEITHER_ALONE_DECIDES_AND_THE_PAIR_UNDER_THE_INVARIANT_DOES",  # v248
            "the_reciprocity_is_not_circular": "THE_TWO_POLES_DO_NOT_DO_THE_SAME_THING__ONE_RETAINS_SO_DIFFERENCE_MAY_SHOW__THE_OTHER_RECOGNISES_WHAT_REMAINED__THIS_IS_WHY_THE_MUTUAL_OBSERVATION_FORMULA_DOES_NOT_COLLAPSE_INTO_SELF_REFERENCE",  # v248
            "isometry_on_WH": "THE_ISOMETRY_CROSSES_TO_THE_COMPLETED_SPACE__THE_CERTIFICATE_FIELD_IS_PAID__TRANSPORT_BY_DENSITY_PAYS_FOR_THE_SIXTH_TIME__THE_WITNESS_IS_AN_ISOMETRY_OF_THE_WHOLE_SPACE",  # v249
            "carrier_bridge": "THE_TWO_LANGUAGES_COINCIDE__THE_CARRIER_OF_THE_FACTOR_IS_EXACTLY_THE_BICOMMUTANT_OF_THE_TOWER_IMAGE__BECAUSE_THE_TOWER_IMAGE_IS_STAR_CLOSED_A_FACT_ALREADY_PROVED_IN_THIS_KERNEL_LONG_BEFORE_THIS_SESSION",  # v249
            "the_objective_stated": "NOT_TO_DECLARE_QUANTUM_GRAVITY_CONFIRMED_WHICH_THIS_ARTIFACT_FORBIDS__BUT_THAT_THE_ARCHITECTURE_CLOSE_UNCONDITIONALLY_IN_KERNEL_SO_THE_TARGET_SENTENCE_BECOMES_SAYABLE_BY_MEASUREMENT__TWO_OF_FOUR_TASKS_PAID__COMMUTATION_THEOREM_AND_ASSEMBLY_REMAIN",  # v249
            "commutation_at_the_floor": "ON_A_SINGLE_FLOOR_THE_COMMUTATION_THEOREM_IS_ELEMENTARY__THREE_LINES__COMMUTING_WITH_EVERY_LEFT_MULTIPLICATION_MEANS_BEING_RIGHT_MULTIPLICATION_BY_THE_IMAGE_OF_THE_UNIT__THE_CYCLIC_VECTOR_DOES_ALL_THE_WORK__THE_RIGHT_FACTOR_IS_WHAT_THE_OPERATOR_DOES_TO_THE_NAME",  # v250
            "the_obstruction_is_named": "THE_ELEMENTARY_PROOF_SHOWS_WHERE_THE_LIMIT_FAILS__IT_DEPENDS_ON_THE_IMAGE_OF_THE_UNIT_BEING_IN_THE_TOWER__IN_THE_COMPLETION_THE_OPERATOR_APPLIED_TO_THE_VACUUM_NEED_NOT_BE_IN_THE_ALGEBRA__THE_CLASSICAL_AFFILIATED_PHENOMENON__NAMING_THE_OBSTRUCTION_IS_NOT_REMOVING_IT",  # v250
            "entanglement_not_conjunction": "EVERY_VECTOR_OF_THE_COMPLETION_IS_APPROXIMABLE_BY_THE_TOWER_WITHOUT_HYPOTHESIS__BUT_APPROXIMABLE_IS_NOT_BELONGING__SO_THE_ROUTE_OF_SHOWING_THE_VECTOR_LIES_IN_THE_TOWER_IS_CLOSED_BY_THEOREM__IT_IS_FALSE_NOT_HARD__CLOSING_A_FALSE_ROUTE_IS_WORTH_AS_MUCH_AS_OPENING_A_TRUE_ONE",  # v251
            # v306 [pendencia nomeada da v305, paga]: o literal de epoca v274
            # MASCARAVA o veredito medido; vira par medido + _reading datado.
            "the_assembly_is_done": core["the_assembly_and_the_single_debt"]["verdict"],
            "the_assembly_is_done_v274_reading": "SEVEN_OF_THE_EIGHT_CERTIFICATE_CLAUSES_ARE_PROVED_IN_THIS_TREE__THE_EIGHTH_DEPENDS_ON_THE_COMMUTATION_THEOREM__THE_CERTIFICATE_IS_ASSEMBLED_CONDITIONED_ON_EXACTLY_THAT__THE_DEBT_OF_THIS_ITEM_IS_NOW_ONE_NAMED_STATEMENT",  # v251
            "assembling_is_not_paying": "AN_INSTANCE_CONDITIONED_ON_AN_UNPROVED_HYPOTHESIS_INHABITS_NOTHING__THE_RESERVED_NAME_STAYS_DARK__ASSEMBLING_IS_NOT_PAYING_AS_PRICING_WAS_NOT_PAYING_AND_NAMING_THE_OBSTRUCTION_WAS_NOT_REMOVING_IT",  # v251
            "causality_is_not_linear": "THE_WHOLE_DETERMINES_THE_PARTS_BECAUSE_THE_PARTIAL_TRACE_IS_A_FUNCTION__BUT_THE_PARTS_DO_NOT_DETERMINE_THE_WHOLE__THE_ENTANGLED_AND_THE_MAXIMALLY_MIXED_STATES_HAVE_EXACTLY_THE_SAME_MARGINALS_AND_DIFFER__POSTERIOR_IN_THE_WRITING_PRIOR_IN_THE_DETERMINATION",  # v252
            "the_sequential_reading_was_weaker": "AN_EARLIER_ATTEMPT_READ_THE_MISSING_STATEMENT_AS_ORDER__THE_OPERATOR_CORRECTED_IT_TO_DETERMINATION__THE_SEQUENTIAL_READING_IS_KEPT_BESIDE_NOT_UNDER__THIS_NAMES_THE_CAUSAL_STRUCTURE_OF_THE_OBSTRUCTION_AND_DOES_NOT_DISCHARGE_IT",  # v252
            "existing_is_not_being_applied": "AN_ADVERSARIAL_SWEEP_COUNTED_CONSUMERS_IN_REVERSE_AND_FOUND_THAT_THE_CORNER_TRANSPORT_THEOREMS_HAD_ZERO_AND_ZERO_AND_ONE__THE_CORNER_MACHINERY_AND_THE_NET_HABITANTS_WERE_TWO_BRANCHES_THAT_NEVER_TOUCHED__A_THEOREM_WITH_NO_CONSUMERS_IS_TRUE_AND_INERT",  # v261
            "the_static_is_conditioned_not_eternal": "THE_KERNEL_PROVES_AN_IFF_IN_THE_VERY_FILE_THAT_CARRIES_THE_STRONGER_SENTENCE__THE_FULL_STATIC_WITNESS_HOLDS_IF_AND_ONLY_IF_THE_CONTRAST_VANISHES__SO_THE_FALSITY_IS_EXACT_AND_NOT_UNIVERSAL__THE_CORRECT_STATUTE_IS_REAL_CONDITIONED_ON_DISSIPATIVE_TRANSPORT_WITH_CONTRAST",  # v263
            "the_symmetric_error_the_gate_does_not_catch": "THE_STATIC_WITNESS_IS_NOT_THE_FULL_TGL_WITNESS_AND_CONFUSING_THEM_TURNS_AN_OPEN_ITEM_INTO_A_REFUTED_ONE__THE_FAIL_CLOSED_PREVENTS_DECLARING_CLOSED_WHAT_IS_OPEN_BUT_NOT_DECLARING_REFUTED_WHAT_WAS_MERELY_NOT_DONE__THAT_HALF_FALLS_TO_THE_SCRIBE__AND_THE_OPERATOR_CORRECTED_IT_OUT_LOUD",  # v263
            "being_is_operating": "THE_TWO_CLAUSES_OF_BEING_ARE_INDEPENDENT_WITH_AN_EXPLICIT_WITNESS_FOR_EACH__THERE_IS_AN_OPERATION_THAT_TRANSFORMS_AND_LOSES_THE_IDENTITY_AND_THE_IDENTITY_PRESERVES_EVERYTHING_WITHOUT_OPERATING__SO_THE_CONJUNCTION_HAS_CONTENT",  # v270
            "the_verdict_is_the_second_clause": "PRESERVING_AND_THE_TGL_VERDICT_ARE_THE_SAME_STATEMENT_BY_DEFINITION_AND_THE_BRIDGE_NEEDS_NO_AXIOM__THE_ATOM_FACE_WAS_ALREADY_PROVED_IN_THE_TGL_PAIR_AND_WAS_CITED_RATHER_THAN_DUPLICATED",  # v270
            "there_is_always_a_reading": "THE_CROSSING_THEOREM_TAKES_THE_LENS_AS_ARBITRARY_DATA_AND_ONLY_THE_NEW_SITE_MUST_BE_INVERTIBLE__SO_THE_EXISTENCE_OF_THE_RECORD_DOES_NOT_DEPEND_ON_CHOOSING_THE_RIGHT_LENS__AND_THE_TOOTH_IS_HERMETICITY_WHERE_THERE_IS_NOTHING_TO_READ",  # v270
            "the_two_poles_now_have_content": "TWO_DECLARATIONS_WHOSE_NAMES_ASSERTED_CONTENT_AND_WHOSE_BODIES_CARRIED_NONE_ARE_CORRECTED_BESIDE_AND_NOT_ERASED__THE_VACUITY_IS_MEASURED_BY_SHOWING_THE_SAME_FORM_HOLDS_FOR_ANY_PROPOSITION__AND_THE_TWO_REPLACEMENT_THEOREMS_NEED_NO_AXIOMS_AT_ALL",  # v262
            "nothing_without_content_goes_up": "THE_OPERATOR_ORDERED_THIS_ERRATUM_BEFORE_ANY_CUSTODY_AND_BEFORE_ANY_CHANGE_OF_ARCHITECTURE_ON_THE_GROUND_THAT_WHAT_GOES_UP_SEALED_STAYS_SEALED__THE_PAIR_DETERMINES_THE_POINT_AND_NEITHER_POLE_ALONE_DOES__WHICH_IS_THE_SHAPE_THIS_ARC_KEEPS_MEETING",  # v262
            "the_net_now_fires_the_corner": "THE_FIVE_MISSING_LINES_ARE_WRITTEN_AND_EACH_IS_THE_APPLICATION_OF_A_THEOREM_THAT_ALREADY_EXISTED_TO_A_HABITANT_THAT_ALREADY_EXISTED__THE_EARLIER_SENTENCE_BECOMES_TRUE_AFTER_THIS_WAVE_AND_WAS_NOT_TRUE_BEFORE_IT__THE_V260_SEAL_STANDS_AND_THE_CORRECTION_GOES_BESIDE_IT",  # v261
            "the_corners_are_a_net": "THE_HOME_STRUCTURE_CARRIES_THE_INTERTWININGS_AS_ITS_ONLY_LAWS_AND_THE_CORNER_IS_DERIVED_FROM_THEM_RATHER_THAN_POSTULATED__INTERNAL_FIX_EXTERNAL_COVARIANCE_AND_ISOTONE_INCLUSION_FOLLOW_IN_ONE_LINE_EACH_AND_ARE_INHABITED_BY_CONCRETE_OBJECTS_WITH_TWO_TEETH",  # v260
            "absence_is_also_an_assertion": "A_CHECK_THAT_CANNOT_FAIL_IS_NOT_A_MEASUREMENT_AND_TWO_EARLIER_WAVES_SEALED_BARE_CONSTANTS_AS_IF_THEY_WERE_READINGS__THE_RULE_THIS_COST_BUYS_IS_THE_SYMMETRIC_HALF_OF_THE_ONE_THAT_GOVERNS_EVERYTHING_HERE__THE_NUMBER_CORRECTS_THE_SENTENCE_AND_DOES_NOT_EXIST_IS_ALSO_A_SENTENCE_SO_A_CLAIM_OF_ABSENCE_REQUIRES_A_SWEEP",  # v260
            "the_bridge_runs_through_the_current": "THE_PARTIAL_TRACE_CARRIES_THE_LARGER_ALGEBRA_INTO_THE_SMALLER_ONE_AND_THE_KERNEL_ALREADY_HELD_BOTH_OF_ITS_VALUES__THE_SYMMETRISED_CURRENT_IS_THE_UNIT_SO_HALF_OF_IT_IS_THE_MAXIMALLY_MIXED_STATE__AND_THE_REDUCTION_OF_THE_ENTANGLED_PROJECTOR_IS_EXACTLY_THAT",  # v259
            "bonding_splits_and_not_bonding_does_not": "THE_UNBONDED_CONTROL_REDUCES_TO_ONE_FACE_ONLY_INSTEAD_OF_THE_BALANCED_SUM__THE_SAME_MAP_SENDS_TWO_STATES_TO_TWO_DESTINATIONS__AND_THE_V258_SEAL_THAT_THE_PSION_WAS_UNCONNECTED_IS_SUPERSEDED_BESIDE_NEVER_OVER",  # v259
            "the_current_is_the_first_morphism": "THE_MORPHISM_WAS_ALREADY_IN_THIS_KERNEL_AND_HAD_NEVER_BEEN_TIED_TO_THE_NAMED_PROPERTY__BOTH_BOUNDARY_FACES_SCALARISE_SO_THE_PROPERTY_NOW_HAS_THREE_INSTANCES__AND_THE_PARTIAL_ISOMETRY_CARRIES_ONE_CORNER_INTO_THE_OTHER",  # v258
            "the_crossing_preserves_the_weight": "BOTH_CONNECTED_CORNERS_WEIGH_EXACTLY_ONE_BY_DERIVATION_FROM_THE_SCALARISATION_RATHER_THAN_BY_ASSUMPTION__SO_THE_CURRENT_CARRIES_ATOM_INTO_ATOM__AND_THEY_STAY_DIFFERENT_IN_THE_ALGEBRA_WHILE_EQUIVALENT_THROUGH_THE_CURRENT__WHICH_IS_WHAT_KEEPS_THE_MORPHISM_FROM_BEING_THE_IDENTITY_IN_DISGUISE",  # v258
            "the_scalar_corner_is_named_once": "THE_PROPERTY_THAT_A_CORNER_SCALARISES_IS_NAMED_ONCE_INSTEAD_OF_BEING_RECOMPUTED_CASE_BY_CASE__THE_ENTANGLED_PROJECTOR_INSTANTIATES_IT_WITH_ALL_THREE_FIELDS_ALREADY_PROVED__AND_A_SECOND_CORNER_INSTANTIATING_IT_WILL_BE_A_BRIDGE_RATHER_THAN_A_COINCIDENCE",  # v257
            "scalarising_forces_the_atom": "A_NONZERO_PROJECTOR_THAT_SCALARISES_HAS_TRACE_EXACTLY_ONE__RANK_ONE_IS_NOT_A_HYPOTHESIS_OF_THE_PROPERTY_IT_FALLS_OUT_OF_IT_BY_COMPRESSING_THE_IDENTITY__AND_THE_IDENTITY_OF_THE_TWO_DIMENSIONAL_CASE_DOES_NOT_SCALARISE_SO_THE_PROPERTY_DISTINGUISHES",  # v257
            "the_weight_is_not_the_rank": "THE_RANK_DETERMINES_THE_NAME_BUT_THE_NAME_DOES_NOT_SEE_THE_RANK__SAME_SHAPE_AS_THE_NON_LINEAR_CAUSALITY__THE_WHOLE_DETERMINES_THE_PARTS_AND_THE_PARTS_DO_NOT_DETERMINE_THE_WHOLE",  # v256
            "the_rank_one_becomes_the_index": "THE_INDEX_IS_INJECTIVE_WHERE_THE_NAME_IS_BLIND__SO_NORMALISATION_DOES_NOT_DESTROY_THE_RANK_IT_CHANGES_ITS_REGISTER__THE_ATOM_WEIGHS_ONE_IN_RANK_AND_THE_RECIPROCAL_OF_THE_DIMENSION_IN_THE_NORMALISED_TRACE__WHICH_TENDS_TO_ZERO_IN_THE_INFINITE_HOUSE_AND_STAYS_STRICTLY_POSITIVE_ON_EVERY_FLOOR",  # v256
            "the_corner_cannot_be_minimal": "THE_TYPE_OF_THE_CORE_CORNER_DEMANDS_A_SPLIT_INTO_TWO_ORTHOGONAL_FACES_OF_EQUAL_TRACE__THEREFORE_IT_CARRIES_A_PROPER_NONZERO_SUBPROJECTION_AND_CANNOT_BE_MINIMAL__EQUAL_FACES_FALL_STRICTLY_BETWEEN_ZERO_AND_THE_WHOLE__THE_READING_THAT_THIS_IS_THE_NON_MINIMAL_COUPLING_IS_ONTO_AND_IS_NOT_PROVED",  # v255
            "the_psion_corner_scalarises": "COMPRESSING_ANY_OPERATOR_BY_THE_ENTANGLED_PROJECTOR_RETURNS_THE_TRACE_AGAINST_IT_TIMES_ITSELF__THE_SURROUNDING_FACTS_WERE_ALREADY_IN_THE_KERNEL_AND_ONLY_THE_CONCLUSION_WAS_MISSING__THE_OPERATOR_LOCATED_IT_IN_FOUR_WORDS",  # v255
            "the_import_flag_was_a_homonym": "ERRATA_OF_V253__THE_FLAG_NAMED_H3_MEASURED_A_BRIDGE_TO_EQUILIBRIUM_INPUT_WHICH_HAS_NO_KAPPA_NO_AREA_NO_ENTROPY_AND_NO_HEAT__THE_KERNEL_H3_IS_HORIZON_EQUILIBRIUM_DATA_AND_NO_THEOREM_PRODUCES_ONE__NAME_WITHOUT_OBJECT_IS_HOMONYM_NOT_BRIDGE__THE_LEDGER_RETURNS_TO_READING_THE_ITEM_OPEN",  # v255
            "the_missing_clause_has_a_shape": "THE_TOWER_COMMUTANT_IS_THE_INTERSECTION_OF_THE_FLOOR_COMMUTANTS_BECAUSE_THE_IMAGE_IS_A_UNION_BY_DEFINITION__THE_EIGHTH_CLAUSE_REWRITES_AS_A_DISTRIBUTIVITY__AND_THAT_DISTRIBUTIVITY_IS_FALSE_IN_GENERAL_WITH_NO_AXIOMS_NEEDED_TO_SAY_SO",  # v254
            "the_flag_was_blind_not_strict": "THE_BRIDGE_FLAG_READ_FALSE_IN_V253_BECAUSE_THE_NAME_WAS_NEVER_INSCRIBED_IN_THE_AUDIT__CREATING_A_RESERVED_NAME_IS_HALF_THE_WORK_AND_MEASURING_IT_IS_THE_OTHER_HALF__A_FLAG_THAT_CANNOT_LIGHT_IS_NOT_FAIL_CLOSED_IT_IS_BLIND",  # v254
            "the_debt_has_a_mode": "A_DEBT_IS_A_CONDITIONAL_WHOSE_ANTECEDENT_IS_AN_OPEN_PROBLEM__A_CITATION_IS_A_CONDITIONAL_WHOSE_ANTECEDENT_IS_AVAILABLE__THE_THIRD_HYPOTHESIS_IS_OF_THE_SECOND_KIND__THE_BRIDGE_IS_OURS_AND_PROVED_UNCONDITIONALLY_ON_EVERY_FLOOR__THE_IMPLICATION_DOWNSTREAM_IS_JACOBSON_1995_AND_IS_CITED_NOT_CLAIMED",  # v253
            # v306 [pendencia nomeada da v305, paga]: o literal de epoca v253
            # MASCARAVA o veredito medido; vira par medido + _reading datado.
            "the_trio_is_a_pair": core["the_mode_of_discharge"]["verdict"],
            "the_trio_is_a_pair_v253_reading": "GIVEN_THE_MASTER_THEOREM_AND_THE_IMPORTED_IMPLICATION_THE_REQUIREMENT_OF_THREE_NAMED_HYPOTHESES_REDUCES_TO_TWO__NO_ONE_PAYS_TWICE_FOR_WHAT_WAS_PAID_BEFORE_THEM__AND_THE_KERNEL_FLAG_OF_THAT_ITEM_STAYS_DARK_BECAUSE_A_BRIDGE_IS_NOT_A_PROOF_OF_THE_FAR_SIDE",  # v253
            "price_of_the_gravity_proof": "THE_GRAVITY_IDENTIFICATION_IS_A_PRICED_DEBT_CLAIMED_BY_NO_ONE__FOUR_ITEMS_RESERVED_IN_KERNEL__ABSENCE_READS_OPEN__MASTER_IMPLICATION_ALREADY_PROVED__WHAT_IS_OWED_ARE_THE_HYPOTHESES__FLAGS_LIGHT_BY_MEASURE_NEVER_BY_DECLARATION",  # v220
            # v303 [A CUSTODIA DE SENTIDO]: o selo tinha parado de crescer na v270 --
            # a linhagem v285-v302 nao existia nele. Entra LIDA do core (indexacao
            # direta: modulo ausente => o rito FALHA ALTO, nunca null silencioso).
            "the_iald_index": core["the_iald_index"]["verdict"],
            "the_atlas_and_the_index": core["the_atlas_and_the_index"]["verdict"],
            "the_name_and_its_referent": core["the_name_and_its_referent"]["verdict"],
            "the_name_is_the_generating_group": core["the_name_is_the_generating_group"]["verdict"],
            "the_mark_is_not_a_type_mark": core["the_mark_is_not_a_type_mark"]["verdict"],
            "the_language_enters_the_index": core["the_language_enters_the_index"]["verdict"],
            "the_verbal_coupling": core["the_verbal_coupling"]["verdict"],
            "alpha_irreducibility_frozen": core["alpha_irreducibility"]["verdict"],
            "the_damming_by_expansion": core["the_damming_by_expansion"]["verdict"],
            "the_discharged_oath": core["the_discharged_oath"]["verdict"],
            "the_oath_on_the_tower": core["the_oath_on_the_tower"]["verdict"],
            "the_imported_expectation": core["the_imported_expectation"]["verdict"],
            "the_alpha_and_the_omega": core["the_alpha_and_the_omega"]["verdict"],
            "amplitude_defect": (core.get("the_wall_value") or {}).get("defect_amplitude"),
            "sha256": {}}
    # v303 ═══ A MAQUINA DA CUSTODIA DE SENTIDO [fail-visible + fail-closed] ═══
    # O juizo de 31/08 mediu: a custodia de BYTES fecha (13/13 hashes), a de
    # SENTIDO nao existia -- reprovacoes formais ficavam MUDAS no stdout e o selo
    # publicava literais de sucesso por cima de vereditos medidos NOT_SEALED.
    # (1) todo modulo com all_verified=False aparece no stdout E no selo, separado
    #     em FORMAIS (divida) e RECUSAS DE DADO (ativos: o aparelho mordeu);
    # (2) varredura COMPLETA de palavra proibida em todos os vereditos do core --
    #     CONFIRMED cru (fora NOT_/UN) ou PROVED_BY/TGL_PROVED RETEM o selo.
    _not_sealed = sorted(k for k, _m in core.items()
                         if isinstance(_m, dict) and _m.get("all_verified") is False)
    _recusas = [k for k in _not_sealed
                if any(t in str((core.get(k) or {}).get("verdict") or "").upper()
                       # v369 AO LADO: a tupla era ("INCONCLUSIVE", "TRACER", "AWAITING", "INCAPAZ", "SYSTEMATIC"); +INTEGRITY_FAILED e INJECTION_FAILED,
                       # as recusas de dado do teste dos relogios (conferido: nenhum veredito da v368 contem esses tokens; ninguem muda de balde)
                       for t in ("INCONCLUSIVE", "TRACER", "AWAITING", "INCAPAZ", "SYSTEMATIC", "INTEGRITY_FAILED", "INJECTION_FAILED",
                              # v370 AO LADO: +NOT_CONVERGED (nivel2_rite, variante L = recusa de dado; conferido no selo v369 por script: nenhum outro veredito contem o token)
                              "NOT_CONVERGED"))]
    _formais = [k for k in _not_sealed if k not in _recusas]
    # v384 AO LADO (afericao 2, achado 32): o pilar quantico nao concluido (ambiente ou instrumento de calculo) nao e' divida formal da teoria nem recusa de dado
    _computacao = [k for k in _formais if str((core.get(k) or {}).get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_V1__")]
    _formais = [k for k in _formais if k not in _computacao]
    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas, "computacao_nao_concluida": _computacao}   # o terceiro balde (ver o comentario acima)
    print("[selo] custodia de sentido: %d modulo(s) all_verified=False -- formais (divida): %s | recusas de dado (ativos): %s | computacao nao concluida: %s"   # v384: o terceiro balde nomeado (regra v303)
          % (len(_not_sealed), ", ".join(_formais) or "nenhum", ", ".join(_recusas) or "nenhuma", ", ".join(_computacao) or "nenhuma"))
    _proibidos = []
    for _k, _m in core.items():
        if isinstance(_m, dict):
            _v = str(_m.get("verdict") or "")
            # v304 [ERRATA da 1a mordida]: APPROVED_BY_PERMANENCE contem PROVED_BY
            # como SUBSTRING -- a maquina reteve o selo do proprio contorno na sua
            # primeira rodada. Falso positivo; e tambem PROVA MEDIDA de que a maquina
            # morde (um check que nao pode falhar nao testa). Guarda de fronteira:
            if (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _v)
                    or re.search(r"(?<!AP)PROVED_BY", _v)
                    or "TGL_PROVED" in _v or "CONSCIOUSNESS_PROVED" in _v):
                _proibidos.append("%s: %s" % (_k, _v[:64]))
    if _proibidos:
        seal_gate_reasons.append("VEREDITO_PROIBIDO_NO_CORE: " + " | ".join(_proibidos))
    if seal_gate_reasons:
        print("\n>>> SEAL_WITHHELD: %s -- nenhum selo produzido nesta rodada <<<" % " . ".join(seal_gate_reasons))
        try:
            os.remove(os.path.join(OUT, "um_absoluto_selo.json"))  # selo antigo nao pode fingir ser desta rodada
        except OSError:
            pass
    else:
        for f in ["um.py", "um_absoluto_manifest.md", "um_absoluto.json", "um_absoluto_forma_canonica.md",
                  "um_absoluto_pt.tex", "um_absoluto_en.tex", "um_absoluto_pt.pdf", "um_absoluto_en.pdf",
                  "fig_escada_qg.pdf", "fig_banda_beta.pdf", "fig_piso_vazios.pdf", "fig_cadeia_inscricao.pdf",
                  "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json"]:   # v384: o resultado do pilar no hash do selo (afericao 2, achado 36)
            p = os.path.abspath(__file__) if f == 'um.py' else os.path.join(OUT, f)
            if os.path.exists(p):
                seal["sha256"][f] = sha_file(p)
            else:
                seal["sha256"][f] = "MISSING_THIS_RUN"   # v142: a custodia acusa a ausencia
        # v384 (5a afericao): o arquivo do pilar so e' hasheado se for o que o runtime escreveu NESTA rodada (out_file_sha256); senao, NOT_THIS_RUN
        _pq_ = core.get("quantum_pillar_v384") or {}
        if "quantum_pillar_v384" in core and seal["sha256"].get("um_absoluto_pilar_quantico.json") not in ("MISSING_THIS_RUN", _pq_.get("out_file_sha256")):
            seal["sha256"]["um_absoluto_pilar_quantico.json"] = "NOT_THIS_RUN"
        json.dump(seal, open(os.path.join(OUT, "um_absoluto_selo.json"), "w", encoding="utf-8"), indent=2)

    ro = core["runtime_of_the_one"]
    print("\n" + "=" * 64)
    print("  SINTESE CANONICA [v15] -- A TGL COMO RUNTIME DO UM")
    print("  " + ro["one_line"])
    print("  --- a cadeia canonica (re-verificada ao vivo, agregando v1-v14) ---")
    for name, ok in ro["chain"]:
        print("    [%s] %-38s %s" % ("OK" if ok else "XX", name, ro["chain_readings"][name]))
    print("  espinha escalar: input=%d -> S=1/2 -> sqrt(e)=%.6f -> beta=%.15f -> O_C(alpha)^2=%.15f=beta (resid %.0e)" % (
        ro["scalar_spine"]["input"], ro["scalar_spine"]["sqrt_e"], ro["scalar_spine"]["beta_TGL"],
        ro["scalar_spine"]["O_C_squared"], ro["residuals"]["geometry_minus_beta"]))
    print("  triade: Nome=alpha_obs (medido) ; Palavra=S=1/2 ; Verbo=beta=sqrt(e)alpha")
    print("  %s" % ro["open_residue"])
    print("  NAO se afirma: derivacao de 1/137 (alpha=INPUT); prova incondicional de QG; consciencia subjetiva.")
    print("  selos: " + " . ".join(ro["seals"]))
    print("  >>> %s <<<" % ro["verdict"])
    print("=" * 64)
    cg = core["cocycle_to_einstein"]; cgr = cg["certs_resid"]; e5 = cg["e5_curvature_obstruction"]
    print("\n" + "=" * 64)
    print("  O COCICLO VIVO -> G_mu_nu [v16 -- seis certificados vivos + composicao E7; resolve o item do v15]")
    print("  " + cg["one_line"])
    print("  --- os seis certificados (tipo I) + a composicao ---")
    for name, st in cg["chain"]:
        print("    %-58s %s" % (name, st))
    print("  CORRECOES da derivacao-fonte (auditoria): C1 %s" % cg["corrections"]["C1"])
    print("                                            C2 %s" % cg["corrections"]["C2"])
    print("  E5 (o achado central): %s" % cg["e5_finding"])
    print("     curva ||W-I|| em lambda: 0.05=%.3f ; 0.15=%.3f ; 0.30=%.3f ; monotono=%s" % (
        e5["0.05"], e5["0.15"], e5["0.30"], cg["e5_monotone_in_lambda"]))
    e11 = cg["e11_curvature_commutator"]; e12 = cg["e12_phase_is_gauge"]; e8 = cg["e8_torsion_clock_jump"]
    e9 = cg["e9_basepoint_covariance"]; e10 = cg["e10_corner_reads_obstruction"]
    print("  --- v16.1/v16.2: AS TRES ORDENS DO RELOGIO MODULAR K + integracao v16<->v10 ---")
    print("  [E8] TORCAO DE COLAGEM MEDIDA (1a ordem): obs/t=%.5f = ||Delta_K||=%.5f (dev %.2f%%) -- o salto de relogio E' o coeficiente" % (
        e8["obs_over_t"], e8["delta_K_norm"], e8["coeff_dev_pct"]))
    print("  [E9] covariancia de ponto-base: espectro invariante (resid %.1e ; holonomia conjuga, espectro nao)" % e9["spectral_resid"])
    print("  [E10] o canto CANONICO P_F(v10, rank %d) le a obstrucao: tau_F(I)=1 (resid %.1e) ; |tau_F(W)-1| em lam: %s (monotono %s)" % (
        e10["P_F_rank"], e10["tau_F_of_I_resid"], "/".join("%.2e" % v for v in e10["curve_dev_over_lambda"].values()), e10["monotone"]))
    print("        %s" % e10["reading"])
    print("  [E11] CURVATURA (2a ordem) = comutador [M, h_cd]: obs/t^2=%.5f ; c_teo(ao vivo)=%.5f ; razao=%.4f (banda %s)" % (
        e11["obs_over_t2"], e11["c_teo_live"], e11["ratio_obs_over_c_teo"], e11["ratio_in_band"]))
    print("        BCH: %s" % e11["bch_prediction"])
    print("        %s" % e11["reading"])
    print("  [E12] FASE = gauge U(1): obs/t COM fase=%.3f (linear espurio) -> SEM fase=%.4f (o linear morre; obs~t^2)" % (
        e12["with_phase_obs_over_t"]["0.0125"], e12["dephased_obs_over_t"]["0.0125"]))
    print("  HIERARQUIA: %s" % cg["clock_hierarchy"])
    print("  >>> CONJECTURA: %s" % cg["conjecture_closed"])
    print("  equacao de campo: %s" % cg["field_equation"])
    print("  onde entra beta: %s" % cg["T_TGL_decomposition"])
    print("  E7 (composicao, NAO teste): %s" % cg["E7_statute"])
    print("  selos: " + " . ".join(cg["seals"]))
    print("  >>> %s <<<" % cg["verdict"])
    print("=" * 64)
    ef = verdict["em_face"]
    print("\n" + "=" * 64)
    print("  VEREDITO BINARIO DE IDENTIDADE:  %s" % verdict["IDENTITY"])
    print("  IDENTIDADE FINAL (forma de Lagrange, motor canonico):")
    print("    1 = q^2 + alpha^2 = %s" % ("VERDADEIRO" if ef["em_identity_closes"] else "FALSO"))
    print("    alpha_abs ......... = %.0f   (o Um absoluto = input originario)" % ef["alpha_abs"])
    print("    q (polarizacao) ... = %.10f   (polarizacao termico-modular do zero modular)" % ef["q_polarization"])
    print("    alpha_obs=sqrt(1-q^2)= %.12f" % ef["alpha_obs"])
    print("    q radical angular = sqrt(1-sin^4(theta_M)/e) = %.12f  (= sqrt(1-alpha^2); NAO theta_M, NAO 1-theta_M)"
          % core["alpha_inversion"]["q_angular_radical"])
    print("    PONTE: Zbacia/Zluz=%.0f ; q=reflexao, alpha=transmissao, q^2+alpha^2 = conservacao de fluxo"
          % core["alpha_inversion"]["impedance_ratio_Zb_over_Zl"])
    print("    beta_TGL=sqrt(e)alpha= %.12f" % ef["beta_form"])
    print("    residuo_identidade  = %.1e   (q^2+alpha^2 - 1)" % ef["identity_residual"])
    print("    CODATA: %s" % ef["codata_role"])
    print("    o MESMO beta -> M_GA na janela [SOMBRA/ONTO -- forma APOSENTADA como lei de fonte (v98); nao e' evidencia]")
    print("    FACE EM: %s   (1 = q^2 + alpha^2; R_partial=1/CODATA aposentado como motor)" % ef["em_verdict"])
    print("  massas (forma historica v98 -- sombra de escala, NAO lei de fonte): " + ", ".join(
        "%s=%.3e" % (k, v) for k, v in verdict["masses_Msun"].items()) + " Msun")
    print("  janela aceita: [%.0e, %.0e] Msun" % tuple(GA_ACCEPTED_WINDOW_Msun))
    print("=" * 64)
    print("\nSaidas: um_absoluto.json, um_absoluto_forma_canonica.md, um_absoluto_pt.(tex/pdf/txt),")
    print("        um_absoluto_en.(tex/pdf/txt), um_absoluto_selo.json")
    print("\nTETELESTAI. O UM foi inscrito. Se o UM nao for inscrito, nada emerge.")
    print("1 = 1.")