# ---- v396: a TESTEMUNHA ESTATICA (o psion habita a fronteira). A mecanica numerica do canto do psion (o projetor de Bell 4x4), da reducao a um sitio e do fluxo diagonal construido, calculada a cada rito com beta =
# alfa CODATA 2018 x sqrt(e) (nunca literal) e confrontada com os termos do kernel do proprio rito (TGLExt.TestemunhaEstatica). [REAL] os termos e o calculo; [CONSTRUCTED] o fluxo psionFlow e o colapso psionCollapse;
# [INPUT/ONTO] as tres falas do operador de 22/10/2026; a face de Fock do psion (Psibit) segue CONDICIONAL e fora do modulo da pedra. O gate nao se move. Fonte autoral deste bloco: runtime_testemunha_v396.py
# (cadeia_de_selo/v396); o contrato (_V396_TESTEMUNHA_CONTRACT) e as falas (_V396_VERBATINS2) sao DERIVADOS do build e dos arquivos, nunca digitados.
import math as _m396


def _v396_mm(a_, b_):
    """Produto de matrizes quadradas (listas de listas)."""
    n_ = len(a_)
    return [[sum(a_[i_][k_] * b_[k_][j_] for k_ in range(n_)) for j_ in range(n_)] for i_ in range(n_)]


def _v396_mv(a_, x_):
    return [sum(a_[i_][k_] * x_[k_] for k_ in range(len(x_))) for i_ in range(len(a_))]


def _v396_tr(a_):
    return sum(a_[i_][i_] for i_ in range(len(a_)))


def _v396_emax(a_, b_):
    """Maior |a - b| entre duas matrizes (ou vetores) do mesmo formato; aceita complexos."""
    if isinstance(a_[0], (list, tuple)):
        return max(abs(a_[i_][j_] - b_[i_][j_]) for i_ in range(len(a_)) for j_ in range(len(a_[0])))
    return max(abs(a_[i_] - b_[i_]) for i_ in range(len(a_)))


def _v396_ix(a_, c_):
    """O indice de (a, c) em Fin 2 x Fin 2, como o Lean indexa o canto: 2a + c."""
    return 2 * a_ + c_


def _v396_bell_projector():
    """TestemunhaEstatica.the_density_is_the_psion: o canto do psion e' o projetor de Bell 4x4, as entradas 1/2 nos pares (p, q) com p.1 = p.2 e q.1 = q.2 (indices 00 e 11)."""
    diag_ = (_v396_ix(0, 0), _v396_ix(1, 1))
    return [[0.5 if (p_ in diag_ and q_ in diag_) else 0.0 for q_ in range(4)] for p_ in range(4)]


def _v396_ptr(pm_, site_):
    """O traco parcial 2x2 do operador 4x4: site_ = 2 soma no SEGUNDO sitio (o ptr do kernel), site_ = 1 soma no primeiro."""
    if site_ == 2:
        return [[sum(pm_[_v396_ix(a_, b_)][_v396_ix(c_, b_)] for b_ in range(2)) for c_ in range(2)] for a_ in range(2)]
    return [[sum(pm_[_v396_ix(b_, a_)][_v396_ix(b_, c_)] for b_ in range(2)) for c_ in range(2)] for a_ in range(2)]


def _v396_vn_entropy(rho_):
    """Entropia de von Neumann (nats) de uma densidade 2x2 hermitiana real: autovalores pela formula fechada."""
    t_ = rho_[0][0] + rho_[1][1]
    d_ = rho_[0][0] * rho_[1][1] - rho_[0][1] * rho_[1][0]
    disc_ = max(0.0, t_ * t_ - 4.0 * d_)
    ls_ = ((t_ + _m396.sqrt(disc_)) / 2.0, (t_ - _m396.sqrt(disc_)) / 2.0)
    return -sum(l_ * _m396.log(l_) for l_ in ls_ if l_ > 0.0)


def _v396_bell_basis():
    """TestemunhaEstatica.bsign/bellUnit: a base de Bell ortonormal u_i = b_i / sqrt 2 em R^4, indices (00, 01, 10, 11): Phi+ = (1,0,0,1), Phi- = (1,0,0,-1), Psi+ = (0,1,1,0), Psi- = (0,1,-1,0)."""
    b_ = [[1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, -1.0], [0.0, 1.0, 1.0, 0.0], [0.0, 1.0, -1.0, 0.0]]
    r_ = _m396.sqrt(2.0)
    return [[x_ / r_ for x_ in v_] for v_ in b_]


def _v396_flow(beta_, g_, t_):
    """TestemunhaEstatica.psionFlow: o diagFlow do kernel (BoundaryException) com taxas d = (0, g, g, g) na base de Bell, de volta a R^4: F_t = sum_i exp(-t beta d_i) u_i u_i^T."""
    u_ = _v396_bell_basis(); d_ = (0.0, g_, g_, g_)
    return [[sum(_m396.exp(-t_ * beta_ * d_[i_]) * u_[i_][p_] * u_[i_][q_] for i_ in range(4)) for q_ in range(4)] for p_ in range(4)]


def _v396_identity(n_):
    return [[1.0 if i_ == j_ else 0.0 for j_ in range(n_)] for i_ in range(n_)]


def _v396_collapse(pm_, y_):
    """TestemunhaEstatica.psionCollapse: o passo do colapso do psion, y -> P y P."""
    return _v396_mm(_v396_mm(pm_, y_), pm_)


def v396_static_witness_mechanics(beta_):
    """v396 -- a mecanica da testemunha estatica: o par ecoa, o individuo nao ecoa, o fluxo fixa exatamente a reta do psion, a testemunha global e' falsa e o colapso ecoa a identidade, com beta recebido (o chamador o calcula em
    runtime: alfa CODATA x sqrt(e); NUNCA literal). Cada checagem e' a leitura numerica de um teorema do kernel (TestemunhaEstatica.*); g e t sao parametros de TESTE (a pedra os deixa como variaveis: nenhum acoplamento da teoria entra).
    Devolve {passed, checks, values, n_checks}. Nao levanta para beta invalido: devolve passed False."""
    checks_ = []

    def ck_(id_, desc_, ok_, val_=None):
        checks_.append({"id": id_, "descricao": desc_, "ok": bool(ok_), "valor": val_})
    if not (isinstance(beta_, float) and _m396.isfinite(beta_) and 0.0 < beta_ < 1.0):
        return {"passed": False, "checks": [{"id": "w0", "descricao": "beta finito em (0, 1)", "ok": False, "valor": repr(beta_)}], "values": {}, "n_checks": 1}
    ln2_ = _m396.log(2.0)
    pm_ = _v396_bell_projector(); id4_ = _v396_identity(4); u_ = _v396_bell_basis()
    # (1) o par ecoa
    p2_ = _v396_mm(pm_, pm_); e_idem_ = _v396_emax(p2_, pm_)
    pur_pair_ = _v396_tr(p2_); tr_pair_ = _v396_tr(pm_)
    p_rank1_ = _v396_emax(pm_, [[u_[0][p_] * u_[0][q_] for q_ in range(4)] for p_ in range(4)])
    ck_("w1a", "o PAR ecoa: P^2 = P (the_pair_echoes), Tr P = 1 (psionCorner_trace_one) e o par e' PURO, Tr(P^2) = 1", e_idem_ <= 1e-16 and abs(tr_pair_ - 1.0) <= 1e-16 and abs(pur_pair_ - 1.0) <= 1e-16, [e_idem_, tr_pair_, pur_pair_])
    ck_("w1b", "o canto e' o projetor de posto 1 sobre o vetor de Bell: P = |Phi+><Phi+| (the_density_is_the_psion; bellUnit_zero_is_the_bell_vector)", p_rank1_ <= 1e-15, p_rank1_)
    # (2) o individuo nao ecoa
    red2_, red1_ = _v396_ptr(pm_, 2), _v396_ptr(pm_, 1)
    meia_ = [[0.5, 0.0], [0.0, 0.5]]
    e_red_ = max(_v396_emax(red2_, meia_), _v396_emax(red1_, meia_))
    r2_ = _v396_mm(red2_, red2_); defeito_ = _v396_emax(r2_, red2_)
    pur_ind_ = _v396_tr(r2_); deficit_ = 1.0 - pur_ind_
    ck_("w2a", "a reducao do psion a UM sitio e' (1/2) I nos dois sitios (the_individual_does_not_echo; bell_reduced_half)", e_red_ <= 1e-16, e_red_)
    ck_("w2b", "o INDIVIDUO nao ecoa: (ptr P)^2 != ptr P (defeito 1/4), Tr(rho^2) = 1/2 e o deficit de pureza 1 - Tr(rho^2) = 1/2 (bell_cci_half)", abs(defeito_ - 0.25) <= 1e-16 and abs(pur_ind_ - 0.5) <= 1e-16 and abs(deficit_ - 0.5) <= 1e-16, [defeito_, pur_ind_, deficit_])
    s_vn_ = _v396_vn_entropy(red2_)
    ck_("w2c", "o deficit 1/2 e' a entropia LINEAR; a entropia de von Neumann da reducao e' ln 2 nat e e' DIFERENTE de 1/2 (fair_bit_entropy_is_log_two, fair_bit_entropy_is_not_half_nat)", abs(s_vn_ - ln2_) <= 1e-12 and abs(s_vn_ - 0.5) >= 0.19 and abs(deficit_ - 0.5) <= 1e-16, [s_vn_, ln2_, deficit_])
    q_ = [[1.0 if (p_ == 0 and c_ == 0) else 0.0 for c_ in range(4)] for p_ in range(4)]   # o estado NAO ligado e00 (x) e00
    rq_ = _v396_ptr(q_, 2); rq2_ = _v396_mm(rq_, rq_)
    ck_("w2d", "o DENTE: o estado produto reduz a um projetor puro que ECOA, e00^2 = e00, com deficit 0 (the_unbonded_marginal_echoes; product_cci_zero): o nao-eco e' do PAR visto por um lado", _v396_emax(rq2_, rq_) <= 1e-16 and abs(1.0 - _v396_tr(rq2_)) <= 1e-16, [_v396_emax(rq2_, rq_), 1.0 - _v396_tr(rq2_)])
    # (3) a ponte construida: a base de Bell e o fluxo
    gram_ = max(abs(sum(u_[i_][p_] * u_[j_][p_] for p_ in range(4)) - (1.0 if i_ == j_ else 0.0)) for i_ in range(4) for j_ in range(4))
    compl_ = max(abs(sum(u_[i_][p_] * u_[i_][q2_] for i_ in range(4)) - (1.0 if p_ == q2_ else 0.0)) for p_ in range(4) for q2_ in range(4))
    ck_("w3a", "a base de Bell e' ORTONORMAL e COMPLETA em R^4 e o 1o vetor e' (e00 + e11)/sqrt 2 (bellUnit_orthonormal, bellUnit_complete, bellUnit_zero_is_the_bell_vector)", gram_ <= 1e-15 and compl_ <= 1e-15 and abs(u_[0][0] - 1.0 / _m396.sqrt(2.0)) <= 1e-16 and abs(u_[0][3] - 1.0 / _m396.sqrt(2.0)) <= 1e-16 and u_[0][1] == 0.0 and u_[0][2] == 0.0, [gram_, compl_])
    gs_, taus_ = (0.5, 1.0, 2.0), (0.0, 0.5, 1.0, 3.0)
    r_closed_ = r_eig_ = r_line_ = 0.0
    move_min_ = 1e9
    for g_ in gs_:
        for tau_ in taus_:
            t_ = tau_ / (beta_ * g_)
            f_ = _v396_flow(beta_, g_, t_)
            lam_ = _m396.exp(-t_ * beta_ * g_)
            clo_ = [[pm_[p_][q2_] + lam_ * (id4_[p_][q2_] - pm_[p_][q2_]) for q2_ in range(4)] for p_ in range(4)]
            r_closed_ = max(r_closed_, _v396_emax(f_, clo_))
            for i_ in range(4):
                lam_i_ = _m396.exp(-t_ * beta_ * (0.0 if i_ == 0 else g_))
                r_eig_ = max(r_eig_, _v396_emax(_v396_mv(f_, u_[i_]), [lam_i_ * x_ for x_ in u_[i_]]))
            r_line_ = max(r_line_, _v396_emax(_v396_mv(f_, u_[0]), u_[0]))
            if tau_ > 0.0:
                for i_ in (1, 2, 3):
                    move_min_ = min(move_min_, _v396_emax(_v396_mv(f_, u_[i_]), u_[i_]))
    ck_("w3b", "o fluxo e' F_t = P + exp(-t beta g)(1 - P): a forma fechada concorda com a soma sobre a base de Bell, e cada u_i e' autovetor com autovalor exp(-t beta d_i), d = (0, g, g, g) (psionFlow_eq, bellUnit_eigen; g e t de teste)", r_closed_ <= 1e-15 and r_eig_ <= 1e-15, [r_closed_, r_eig_])
    ck_("w3c", "o testemunhado estaticamente e' EXATAMENTE a reta do psion: o vetor de Bell e' fixado por todo t (residuo <= 1e-15) e cada um dos tres outros modos e' MOVIDO (the_static_set_is_the_psion_line, the_psion_line_is_inhabited)", r_line_ <= 1e-15 and move_min_ >= 0.1, [r_line_, move_min_])
    pu0_ = _v396_mv(pm_, u_[0]); pui_ = [_v396_mv(pm_, u_[i_]) for i_ in (1, 2, 3)]; pe_ = _v396_mv(pm_, [1.0, 0.0, 0.0, 0.0])
    ck_("w3d", "a reta do psion e' o conjunto de pontos fixos do canto: P Phi+ = Phi+, P u_i = 0 nos outros tres, e e00 NAO e' fixado (psionLine_iff_fixed_by_the_corner, bellProjector_is_real)", _v396_emax(pu0_, u_[0]) <= 1e-16 and all(max(abs(x_) for x_ in v_) <= 1e-16 for v_ in pui_) and _v396_emax(pe_, [1.0, 0.0, 0.0, 0.0]) >= 0.4)
    f1_ = _v396_flow(beta_, 1.0, 1.0 / beta_); e00_ = [1.0, 0.0, 0.0, 0.0]
    move_e00_ = _v396_emax(_v396_mv(f1_, e00_), e00_)
    ck_("w3e", "a testemunha estatica GLOBAL e' FALSA: existe x (aqui e00) que nenhum t positivo fixa; (F_t - 1) e00 tem norma maxima > 0 (the_global_witness_is_false; boundary_is_the_only_exception)", move_e00_ >= 0.1, move_e00_)
    r_lim_ = 0.0
    for x_ in ([1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.3, -1.2, 0.7, 2.0]):
        f_ = _v396_flow(beta_, 1.0, 60.0 / beta_)
        r_lim_ = max(r_lim_, _v396_emax(_v396_mv(f_, x_), _v396_mv(pm_, x_)))
    ck_("w3f", "o fluxo ENTREGA ao canto: F_t x -> P x quando t cresce (exp(-t beta g) = exp(-60) em t = 60/(beta g); the_flow_delivers_to_the_psion; regime da FACE: o vazamento tem limite)", r_lim_ <= 1e-14, r_lim_)
    # (4) o colapso ecoa a identidade
    r_idem_ = r_id_ = r_sc_ = 0.0
    ys_ = [[[complex(_m396.sin(1.0 + i_ + 2 * j_ + k_), _m396.cos(i_ - j_ + k_)) for j_ in range(4)] for i_ in range(4)] for k_ in range(3)]
    for y_ in ys_:
        sy_ = _v396_collapse(pm_, y_); ssy_ = _v396_collapse(pm_, sy_)
        r_idem_ = max(r_idem_, _v396_emax(ssy_, sy_))
        r_id_ = max(r_id_, abs(_v396_tr(_v396_mm(pm_, sy_)) - _v396_tr(_v396_mm(pm_, y_))))
        tpy_ = _v396_tr(_v396_mm(pm_, y_))
        r_sc_ = max(r_sc_, _v396_emax(sy_, [[tpy_ * pm_[i_][j_] for j_ in range(4)] for i_ in range(4)]))
    r_fixc_ = _v396_emax(_v396_collapse(pm_, pm_), pm_)
    ck_("w4a", "o COLAPSO do psion ecoa a identidade: P y P = Tr(P y) P (escalarizacao), idempotente, conserva Tr(P y) e fixa o proprio canto (the_collapse_of_the_psion_echoes_its_identity; psionCollapse e' CONSTRUIDO)", max(r_idem_, r_id_, r_sc_, r_fixc_) <= 1e-14, [r_idem_, r_id_, r_sc_, r_fixc_])
    y1_ = ys_[0]; c_ = complex(0.3, 0.2)
    y2_ = [[y1_[i_][j_] + c_ * (id4_[i_][j_] - pm_[i_][j_]) for j_ in range(4)] for i_ in range(4)]
    gap_in_ = _v396_emax(y1_, y2_); gap_out_ = _v396_emax(_v396_collapse(pm_, y1_), _v396_collapse(pm_, y2_))
    ck_("w4b", "o colapso NAO tem inversa a esquerda: duas entradas distintas (diferem em (1 - P)) tem o MESMO colapso, logo ele nao e' injetivo (collapse_has_no_left_inverse); a autoatestacao fica fora do tipo (no_self_attestation)", gap_in_ >= 0.1 and gap_out_ <= 1e-14, [gap_in_, gap_out_])
    vals_ = {"beta": beta_, "g_testes": list(gs_), "tau_testes": list(taus_), "pair_idempotence_residual": e_idem_, "pair_trace": tr_pair_, "pair_purity": pur_pair_, "pair_rank1_residual": p_rank1_,
             "individual_reduction_residual": e_red_, "individual_idempotence_defect": defeito_, "individual_purity": pur_ind_, "individual_deficit": deficit_, "von_neumann_entropy": s_vn_, "ln2": ln2_,
             "unbonded_purity_deficit": 1.0 - _v396_tr(rq2_), "bell_gram_residual": gram_, "bell_completeness_residual": compl_, "closed_form_residual": r_closed_, "eigen_residual": r_eig_, "line_fixed_residual": r_line_,
             "off_line_min_move": move_min_, "global_witness_move": move_e00_, "limit_residual": r_lim_, "collapse_idempotence_residual": r_idem_, "collapse_identity_residual": r_id_, "collapse_scalarisation_residual": r_sc_,
             "collapse_noninjectivity_input_gap": gap_in_, "collapse_noninjectivity_output_gap": gap_out_}
    return {"passed": all(k_["ok"] for k_ in checks_), "checks": checks_, "values": vals_, "n_checks": len(checks_)}


_V396_GUARDA_FORMAL = "TGL_STATIC_WITNESS_V396__REFUSED_%s__GATE_UNMOVED"


def testemunha_estatica_v396(core):
    """v396 -- A TESTEMUNHA ESTATICA: o psion habita a fronteira (cunhagens do operador de 22/10/2026, embutidas por sha256). Chamado no PONTO REAL do main junto do psibit_v395 (a fractalizacao do Um). Le do kernel do PROPRIO rito a conjuncao
    INCONDICIONAL (TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness) e os teoremas da pedra que o contrato lista (bandeira True, trio, proveniencia no modulo da pedra), os termos antigos de que a composicao depende (no trio, com a
    proveniencia que o compilador emite) e CONFERE que a face de Fock do psion segue declarada em Psibit.lean (CONDICIONAL, fora do modulo desta pedra); confere a pedra por sha256 e as tres falas do operador por sha256; e CALCULA, com beta =
    alfa CODATA 2018 x sqrt(e) em runtime (nunca literal; SEALED_CODATA_ALPHA e o literal ALPHA_FINE_CODATA_2018 do script embutido do nivel 2 sao um dado e dois nomes, conferidos por _v376_same_alpha_literal), a mecanica do canto do psion, da
    reducao a um sitio, do fluxo construido e do colapso. Fail-closed em cada elo; excecao vira recusa visivel; nao move o gate. Validade no kernel nao e' creditacao."""
    import hashlib
    c_ = _V396_TESTEMUNHA_CONTRACT
    kf_ = core.get("kernel_formalization") or {}
    axr_ = kf_.get("axiom_report") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    src_ = kf_.get("declaration_sources_v394") or {}
    lad_ = core.get("external_ladder") or {}
    cnt_ = [lad_.get("n_theorems_clean"), lad_.get("n_theorems_expected"), c_["expected_ladder"]]
    exact_ = all(type(x_) is int for x_ in cnt_) and len(set(cnt_)) == 1
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and all(isinstance(x_, str) for x_ in axr_.get(n_)) and set(axr_.get(n_)) <= trio_)
    per_ = {}
    for th_, fl_ in c_["theorems"].items():
        per_[th_] = bool(em_trio_(th_) and kf_.get(fl_) is True and src_.get(th_) == c_["stone"]["path"])
    sup_ = {n_: bool(em_trio_(n_) and src_.get(n_) == p_) for n_, p_ in c_["support"].items()}
    body_ = _EMBEDDED_KERNEL_FILES.get(c_["stone"]["path"])
    src_ok_ = bool(isinstance(body_, str) and hashlib.sha256(body_.encode("utf-8")).hexdigest() == c_["stone"]["sha256"] and (kf_.get("formal_files_sha256") or {}).get(c_["stone"]["path"]) == c_["stone"]["sha256"])
    ver_ = {}
    for k_ in c_["verbatins"]:
        v_ = _V396_VERBATINS2.get(k_)
        ver_[k_] = bool(v_ and hashlib.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"]))
    alfa_ = globals().get("SEALED_CODATA_ALPHA")   # o DADO (CODATA 2018); no script embutido do nivel 2 o mesmo literal chama-se ALPHA_FINE_CODATA_2018
    dois_nomes_ = bool(callable(globals().get("_v376_same_alpha_literal")) and _v376_same_alpha_literal())
    beta_rt_ = (alfa_ * _m396.sqrt(_m396.e)) if isinstance(alfa_, float) else None
    beta_core_ = core.get("beta")
    beta_rel_ = (abs(beta_rt_ - beta_core_) / abs(beta_rt_)) if (isinstance(beta_rt_, float) and isinstance(beta_core_, float) and beta_rt_ != 0.0) else None
    beta_ok_ = bool(isinstance(beta_rt_, float) and isinstance(beta_core_, float) and 0.0 < beta_rt_ < 1.0 and beta_rel_ is not None and beta_rel_ <= 1e-9 and dois_nomes_)
    unc_th_, unc_fl_ = c_["unconditional"]["theorem"], c_["unconditional"]["flag"]
    unc_ = {"theorem": unc_th_, "flag": unc_fl_, "flag_true": kf_.get(unc_fl_) is True, "axioms": axr_.get(unc_th_), "in_trio": em_trio_(unc_th_), "declared_in": src_.get(unc_th_), "in_kernel": bool(per_.get(unc_th_)),
            "composition": "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"}
    fk_ = c_["fock_face"]
    fock_ok_ = bool(src_.get(fk_["theorem"]) == fk_["path"] and fk_["path"] != c_["stone"]["path"] and fk_["theorem"] not in c_["theorems"] and em_trio_(fk_["theorem"]))
    fock_ = {"theorem": fk_["theorem"], "declared_in": src_.get(fk_["theorem"]), "declared_outside_the_stone": fock_ok_, "status": "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE", "inhabitant_exhibited": False,
             "linked_to_the_corner_by_a_lemma": False,
             "reading": "the Fock face of the psion (psion C = C.Omega, fixed by the light) is a statement for every Fock certificate, declared in the Psibit module; the kernel exhibits no inhabitant of the certificate and no lemma identifies psion C with the psionCorner of this stone"}
    import json as _j396
    guarda_ = _v392_guarda_texto(_j396.dumps(_V396_TESTEMUNHA_TEXT, ensure_ascii=False))
    formal_ = bool(kf_.get("all_verified") is True and exact_ and per_ and all(per_.values()) and sup_ and all(sup_.values()) and fock_ok_ and src_ok_ and ver_ and all(ver_.values()) and not guarda_)
    out_ = {"all_verified": False, "estatuto": _V396_TESTEMUNHA_TEXT["estatuto"], "exact_ladder": exact_, "formal_theorems": per_, "support_theorems": sup_, "embedded_source_ok": src_ok_, "inscriptions": ver_, "beta_ok": beta_ok_,
            "beta_core_rel_diff": beta_rel_, "alpha_two_names_same": dois_nomes_, "unconditional": unc_, "fock_face": fock_, "runtime_executed": False, "does_not_gate_core": True, "scope": _V396_TESTEMUNHA_TEXT["escopo"],
            "limites": _V396_TESTEMUNHA_TEXT["limites"], "diz": _V396_TESTEMUNHA_TEXT["diz"], "nao_diz": _V396_TESTEMUNHA_TEXT["nao_diz"], "guarda_p18_violacoes": guarda_[:5]}
    if not formal_:
        out_["verdict"] = _V396_GUARDA_FORMAL % "FORMAL_OR_SOURCE_EVIDENCE"
    elif not beta_ok_:
        out_["verdict"] = _V396_GUARDA_FORMAL % "BETA_IS_NOT_ALPHA_SQRT_E"
    else:
        try:
            mec_ = v396_static_witness_mechanics(beta_rt_)
            out_.update(runtime_executed=True, mechanics={"passed": mec_["passed"], "n_checks": mec_["n_checks"], "checks": mec_["checks"]}, values=mec_["values"], all_verified=bool(mec_["passed"]))
            out_["verdict"] = (_V396_TESTEMUNHA_TEXT["veredito_ok"] if mec_["passed"] else _V396_GUARDA_FORMAL % "MECHANICS_CHECK_FAILED")
        except Exception as e_:   # noqa: BLE001
            out_.update(runtime_executed=True, error=repr(e_)[:300])
            out_["verdict"] = _V396_GUARDA_FORMAL % "RUNTIME_ERROR"
    core["testemunha_estatica_v396"] = out_
    return out_
