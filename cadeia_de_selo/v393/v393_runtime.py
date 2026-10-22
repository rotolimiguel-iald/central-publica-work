class _V393ContractError(ValueError):
    pass


def _v393_tex(s_):
    """v393 -- escapa o texto para o LaTeX do artigo (as falas do operador entram verbatim; so' os caracteres especiais do TeX sao protegidos)."""
    return (str(s_).replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%").replace("$", r"\$").replace("#", r"\#")
            .replace("_", r"\_").replace("{", r"\{").replace("}", r"\}").replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}"))


def _v393_admissivel(leitura_, alvo_, tol_=None):
    """v393 -- a imagem em Python do contrato da REGRA (TGLExt.RuleTruthContract.Admissible: `reading y = target`). `leitura_` e' o resultado da leitura r(y) e `alvo_` o objeto pre-fixado.
    Rotulos: igualdade EXATA (criterio 'exato'). Matrizes/numeros: distancia (HS ou absoluta) <= tol_ (criterio 'tolerancia'); a tolerancia NAO e' igualdade exata: o registro diz qual
    criterio valeu, o erro lido e a tolerancia. Devolve um dict (nunca levanta para dado bem formado)."""
    import numpy as _np
    if isinstance(leitura_, str) or isinstance(alvo_, str):
        ok_ = isinstance(leitura_, str) and isinstance(alvo_, str) and leitura_ == alvo_
        return {"admitida": bool(ok_), "criterio": "exato", "erro": 0.0 if ok_ else None, "tolerancia": None, "veredito": "SATISFACTION_ADMITTED" if ok_ else "SATISFACTION_REFUSED"}
    a_ = _np.asarray(leitura_, dtype=complex); b_ = _np.asarray(alvo_, dtype=complex)
    if a_.shape != b_.shape or not _np.isfinite(a_).all() or not _np.isfinite(b_).all() or tol_ is None or isinstance(tol_, bool) or not (tol_ > 0):
        return {"admitida": False, "criterio": "tolerancia", "erro": None, "tolerancia": tol_, "veredito": "SATISFACTION_REFUSED", "motivo": "ENTRADA_MAL_FORMADA"}
    err_ = float(_np.linalg.norm(a_ - b_))
    ok_ = err_ <= tol_
    return {"admitida": bool(ok_), "criterio": "tolerancia", "erro": err_, "tolerancia": tol_, "veredito": "SATISFACTION_ADMITTED" if ok_ else "SATISFACTION_REFUSED",
            "igualdade_exata_afirmada": False}


def _v393_estado_valido(valor_, tol_, rotulo_):
    import numpy as _np
    arr_ = _np.asarray(valor_)
    if arr_.shape != (4, 4) or arr_.dtype.kind not in "fci":
        raise _V393ContractError(rotulo_ + " must be a numeric 4x4 matrix, excluding booleans")
    arr_ = _np.asarray(arr_, dtype=_np.complex128)
    if not _np.isfinite(arr_).all():
        raise _V393ContractError(rotulo_ + " contains nonfinite entries")
    if _np.linalg.norm(arr_ - arr_.conj().T) > tol_:
        raise _V393ContractError(rotulo_ + " is not Hermitian")
    if abs(_np.trace(arr_) - 1.0) > tol_ or float(_np.linalg.eigvalsh(arr_).min()) < -tol_:
        raise _V393ContractError(rotulo_ + " must have trace one and be positive")
    return arr_


def _v393_escalar(valor_, nome_, minimo_=0.0, positivo_=False):
    import math as _mt
    import numpy as _np
    if isinstance(valor_, (bool, _np.bool_)) or not isinstance(valor_, (int, float, _np.integer, _np.floating)):
        raise _V393ContractError(nome_ + " must be a numeric non-boolean scalar")
    n_ = float(valor_)
    if not _mt.isfinite(n_) or n_ < minimo_ or (positivo_ and n_ <= minimo_):
        raise _V393ContractError(nome_ + " is not finite/in range")
    return n_


class _V393Motor:
    """v393 -- o motor da REGRA sobre o consumidor REAL (prove_decision_commutation): leitura E (pinching), alvo PRE-FIXADO, satisfacao admitida/recusada. Porte de RuleMotor (run_rule_motor.py,
    sha256 pinado no registro). Estado bruto (o que o fluxo entrega) e inscricao (a leitura E do estado) ficam em campos DISTINTOS."""

    def __init__(self, capt_, alvo_, spec_, flags_):
        self.tol = _v393_escalar(spec_["tol_algebra"], "tol_algebra", positivo_=True)
        self.rule_tol = _v393_escalar(spec_["tol_rule"], "tol_rule", positivo_=True)
        self.rate = _v393_escalar(capt_["gamma"], "rate", positivo_=True)
        if len(flags_) != 10 or any(v_ is not True for v_ in flags_.values()):
            raise _V393ContractError("Incomplete kernel evidence")
        self.read = capt_["recognize"]
        self._flow = capt_["recognize_flow"]
        self.alvo = _v393_estado_valido(alvo_, self.tol, "target").copy()
        import numpy as _np
        if _np.linalg.norm(self.read(self.alvo) - self.alvo) > self.tol:
            raise _V393ContractError("Target must be fixed by the actual reading")

    def avaliar(self, estado_, exposicao_):
        import numpy as _np
        estado_ = _v393_estado_valido(estado_, self.tol, "state")
        exposicao_ = _v393_escalar(exposicao_, "exposure")
        evoluido_ = _v393_estado_valido(self._flow(estado_, exposicao_ / self.rate), self.tol, "evolved state")
        inscricao_ = self.read(evoluido_)
        sat_ = _v393_admissivel(inscricao_, self.alvo, self.rule_tol)
        bruto_ = float(_np.linalg.norm(evoluido_ - self.alvo))
        return {"exposure": exposicao_, "time_reference_units": exposicao_ / self.rate,
                "state_real": evoluido_.real.tolist(), "state_imag": evoluido_.imag.tolist(),
                "reading_real": inscricao_.real.tolist(), "reading_imag": inscricao_.imag.tolist(),
                "read_error_hs": float(sat_["erro"]), "raw_error_hs": bruto_,
                "read_rule": bool(sat_["admitida"]), "raw_rule": bruto_ <= self.rule_tol,
                "verdict": sat_["veredito"],
                "trace_error": float(abs(_np.trace(evoluido_) - 1.0)),
                "hermiticity_error": float(_np.linalg.norm(evoluido_ - evoluido_.conj().T)),
                "minimum_eigenvalue": float(_np.linalg.eigvalsh(evoluido_).min()),
                "complement_norm_hs": float(_np.linalg.norm(evoluido_ - inscricao_))}


def _v393_fonte_do_consumidor():
    """v393 -- o texto-fonte (inspect.getsource) das 5 funcoes do consumidor REAL, na ordem fixa; devolve (sha256 do conjunto, lista de sha por funcao)."""
    import hashlib as _hl
    import inspect as _insp
    fns_ = (prove_decision_commutation, _recognition_reading_modes, _v361_pinch, _v361_herm_fn, _v361_flow)
    por_ = [_hl.sha256(_insp.getsource(f_).encode("utf-8")).hexdigest() for f_ in fns_]
    return _hl.sha256("\n".join(por_).encode("utf-8")).hexdigest(), por_


def regra_consumidor_v393(core):
    """v393 (14/10/2026) -- A REGRA NO CONSUMIDOR REAL. O consumidor numerico da decisao (prove_decision_commutation, v146/v361, 5 corpos de funcao pinados) e' EXECUTADO a cada rito; o fluxo
    T_t = E + exp(-Gamma t)(id - E) e' avaliado contra o ALVO PRE-FIXADO (matriz fixada no pre-registro, antes do rito); o veredito da satisfacao (admitida/recusada) e' DETERMINADO pela regra
    (leitura E do estado == alvo, dentro de uma TOLERANCIA numerica declarada -- que NAO e' igualdade exata); estado bruto e inscricao em campos distintos; controles negativos (alvo
    incompativel, entrada invalida, evidencia faltando, taxa nula). Idempotencia ou flag global sozinhas nao bastam. Sintetico: nenhum dado observado; unidades de referencia [INPUT]. NAO move o gate."""
    import copy as _cp
    import hashlib as _hl
    import json as _js
    import math as _mt
    import numpy as _np
    import sys as _sys
    cks_ = []

    def ck_(nome_, pred_, det_=None):
        e_ = {"name": nome_, "passed": bool(pred_)}
        if det_ is not None:
            e_["details"] = det_
        cks_.append(e_)
        return bool(pred_)

    def recusa_(nome_, acao_):
        try:
            acao_()
        except (_V393ContractError, ValueError, TypeError) as ex_:
            ck_(nome_, True, {"refused_with": type(ex_).__name__})
        else:
            ck_(nome_, False)

    spec_ = _V393_REGRA_PREREG
    ck_("prereg_pinado_por_hash_canonico", _hl.sha256(_js.dumps(spec_, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest() == _V393_REGRA_PREREG_SHA)
    el_ = core.get("external_ladder") or {}
    pt_ = el_.get("per_theorem") or {}
    axr_ = (core.get("kernel_formalization") or {}).get("axiom_report") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    evid_ = {}
    for nome_, rec_ in _V393_REGRA_EVID.items():
        evid_[nome_] = {"declaracao": rec_["declaration"], "bandeira_viva": pt_.get(nome_) is True,
                        "axiomas_vivos": axr_.get(rec_["declaration"]), "no_trio": rec_["declaration"] in axr_ and set(axr_[rec_["declaration"]] or []) <= trio_}
    flags_ = {n_: bool(v_["bandeira_viva"] and v_["no_trio"]) for n_, v_ in evid_.items()}
    ck_("dez_evidencias_do_kernel_vivas_e_no_trio", len(flags_) == 10 and all(flags_.values()), {"vivas": sum(flags_.values())})
    src_sha_, src_por_ = _v393_fonte_do_consumidor()
    ck_("consumidor_real_com_os_cinco_corpos_pinados", src_sha_ == _V393_CONSUMIDOR_SRC_SHA, {"sha": src_sha_[:16], "esperado": _V393_CONSUMIDOR_SRC_SHA[:16]})
    if not all(c_["passed"] for c_ in cks_):   # fail-closed: pre-registro adulterado, evidencia faltando ou fonte do consumidor diferente => nada e' executado
        return {"verdict": "TGL_REGRA_CONSUMIDOR_V393__NOT_SEALED_THIS_RUN__%s__GATE_UNMOVED" % "_".join(c_["name"] for c_ in cks_ if not c_["passed"])[:300], "all_verified": False, "does_not_gate_core": True, "checks": cks_}
    consumidor_ = prove_decision_commutation
    capt_ = {}
    prev_ = _sys.getprofile()

    def perfil_(frame_, evento_, arg_):
        if evento_ == "return" and frame_.f_code is consumidor_.__code__:
            capt_.update(frame_.f_locals)
    try:
        _sys.setprofile(perfil_)
        resultado_ = consumidor_(1, _cp.deepcopy({"external_ladder": {"per_theorem": dict(flags_)}}))
    finally:
        _sys.setprofile(prev_)
    for k_ in ("recognize", "recognize_flow", "gamma", "rho", "c_plus", "c_minus"):
        if k_ not in capt_:
            return {"verdict": "TGL_REGRA_CONSUMIDOR_V393__NOT_SEALED_THIS_RUN__CLOSURE_NOT_CAPTURED__GATE_UNMOVED", "all_verified": False, "does_not_gate_core": True, "falta": k_, "checks": cks_}
    ck_("consumidor_all_verified_com_as_dez_evidencias_vivas", resultado_.get("all_verified") is True)
    ck_("dois_modos_de_leitura_verificados", all(v_["ok"] for v_ in resultado_["recognition_dephasing"]["reading_modes"]["modes"].values()))
    ck_("consumidor_nao_move_o_gate", resultado_.get("does_not_gate_core") is True)
    alvo_ = _np.array(spec_["target_real"], dtype=float) + 1j * _np.array(spec_["target_imag"], dtype=float)
    tol_ = spec_["tol_algebra"]
    E_, fluxo_, taxa_, rho0_ = capt_["recognize"], capt_["recognize_flow"], capt_["gamma"], capt_["rho"].copy()
    motor_ = _V393Motor(capt_, alvo_, spec_, flags_)
    ck_("alvo_pre_fixado_igual_a_leitura_do_estado_inicial", _np.linalg.norm(E_(rho0_) - alvo_) <= tol_)
    ck_("taxa_vem_do_beta_de_runtime", taxa_ == globals()["SEALED_CODATA_ALPHA"] * _mt.sqrt(_mt.e) / 2.0)
    g_ = spec_["exposure_grid"]
    expos_ = _np.linspace(g_["start"], g_["stop"], g_["count"])
    linhas_ = [motor_.avaliar(rho0_, float(x_)) for x_ in expos_]
    prev_h_ = "0" * 64
    for i_, r_ in enumerate(linhas_):
        it_ = {"index": i_, "previous_sha256": prev_h_, "record": r_}
        prev_h_ = _hl.sha256(_js.dumps(it_, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False).encode("utf-8")).hexdigest()
    ck_("regra_de_leitura_admite_todos_os_pontos", all(r_["read_rule"] for r_ in linhas_))
    ck_("regra_bruta_falsa_em_todos_os_pontos_finitos", all(not r_["raw_rule"] for r_ in linhas_))
    nor_ = [r_["complement_norm_hs"] for r_ in linhas_]
    ck_("complemento_decresce_estritamente", all(a_ > b_ > 0.0 for a_, b_ in zip(nor_, nor_[1:])))
    dec_ = max(abs(r_["complement_norm_hs"] - nor_[0] * _mt.exp(-r_["exposure"])) for r_ in linhas_)
    ck_("decaimento_exponencial_prescrito", dec_ <= tol_, dec_)
    un_ = [_np.eye(16, dtype=complex)[:, i_].reshape(4, 4) for i_ in range(16)]
    EM_ = _np.column_stack([E_(u_).reshape(16) for u_ in un_])
    ck_("E_idempotente_no_espaco_inteiro", _np.linalg.norm(EM_ @ EM_ - EM_) <= tol_)
    ck_("E_autoadjunto_HS", _np.linalg.norm(EM_ - EM_.conj().T) <= tol_)
    dimfix_ = int(_np.sum(_np.linalg.svd(EM_, compute_uv=False) > spec_["spectral_cutoff"]))
    ck_("dimensao_complexa_do_espaco_fixo_igual_a_oito", dimfix_ == 8, dimfix_)
    saltos_ = [_mt.sqrt(taxa_) * capt_[p_] for p_ in ("c_plus", "c_minus")]
    ger_ = _np.column_stack([sum((j_ @ u_ @ j_.conj().T - 0.5 * ((j_.conj().T @ j_) @ u_ + u_ @ (j_.conj().T @ j_))) for j_ in saltos_).reshape(16) for u_ in un_])
    ck_("gerador_GKLS_confere_com_a_lei_real", _np.linalg.norm(ger_ - taxa_ * (EM_ - _np.eye(16))) / taxa_ <= tol_)
    vals_, vecs_ = _np.linalg.eigh(ger_)
    ck_("gerador_GKLS_hermitiano", _np.linalg.norm(ger_ - ger_.conj().T) <= tol_)
    ck_("gerador_GKLS_nao_positivo", float(vals_.max()) <= tol_)
    ck_("nulidade_do_gerador_GKLS_igual_a_oito", int(_np.sum(_np.abs(vals_ / taxa_) <= spec_["spectral_cutoff"])) == 8)
    oraculo_ = lambda ex_: (vecs_ * _np.exp(vals_ * ex_ / taxa_)) @ vecs_.conj().T
    e_op_, e_comp_, e_sg_ = [], [], []
    for ex_ in spec_["exposure_checkpoints"]:
        op_ = _np.column_stack([fluxo_(u_, ex_ / taxa_).reshape(16) for u_ in un_])
        e_op_.append(float(_np.linalg.norm(op_ - oraculo_(ex_))))
        est_or_ = (oraculo_(ex_) @ rho0_.reshape(16)).reshape(4, 4)
        comp_ = fluxo_(fluxo_(rho0_, 0.37 * ex_ / taxa_), 0.63 * ex_ / taxa_)
        e_comp_.append(float(_np.linalg.norm(comp_ - est_or_)))
        e_sg_.append(float(_np.linalg.norm(comp_ - fluxo_(rho0_, ex_ / taxa_))))
    ck_("GKLS_independente_todos_os_checkpoints_do_operador", max(e_op_) <= tol_, max(e_op_))
    ck_("GKLS_independente_trajetoria_composta", max(e_comp_) <= tol_, max(e_comp_))
    ck_("semigrupo_nos_checkpoints", max(e_sg_) <= tol_, max(e_sg_))
    ck_("leitura_e_fluxo_comutam", max(float(_np.linalg.norm(E_(fluxo_(rho0_, x_ / taxa_)) - fluxo_(E_(rho0_), x_ / taxa_))) for x_ in expos_) <= tol_)
    ck_("traco_preservado", max(r_["trace_error"] for r_ in linhas_) <= tol_)
    ck_("hermiticidade_preservada", max(r_["hermiticity_error"] for r_ in linhas_) <= tol_)
    ck_("positividade_preservada", min(r_["minimum_eigenvalue"] for r_ in linhas_) >= -tol_)
    # controles negativos: a incompatibilidade e' VEREDITO TESTADO (nao flag global nem idempotencia)
    incomp_ = _np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex)
    inc_linhas_ = [motor_.avaliar(incomp_, float(x_)) for x_ in spec_["exposure_checkpoints"]]
    ck_("entrada_fixa_incompativel_e_recusada", all((not r_["read_rule"]) and r_["verdict"] == "SATISFACTION_REFUSED" for r_ in inc_linhas_))
    alt_motor_ = _V393Motor(capt_, incomp_, spec_, flags_)
    alt_ver_ = alt_motor_.avaliar(rho0_, 1.0)
    ck_("alvo_fixo_incompativel_e_recusado", alt_ver_["verdict"] == "SATISFACTION_REFUSED")
    ck_("idempotencia_de_E_nao_forca_o_alvo", _np.linalg.norm(E_(E_(incomp_)) - E_(incomp_)) <= tol_ and _np.linalg.norm(E_(incomp_) - alvo_) > spec_["tol_rule"])
    zero_ = E_(rho0_) + _mt.exp(-0.0 * 1.0) * (rho0_ - E_(rho0_))
    ck_("taxa_nula_deixa_o_complemento_intacto", _np.linalg.norm(zero_ - rho0_) <= tol_ and _np.linalg.norm(zero_ - alvo_) > spec_["tol_rule"])
    for v_ in (float("nan"), float("inf"), -float("inf"), True, False, -1.0, "1"):
        recusa_("exposicao_invalida_" + repr(v_), lambda v2_=v_: motor_.avaliar(rho0_, v2_))
    for v_ in (-1.0, 0.0, float("nan"), float("inf"), True, False):
        ruim_ = dict(capt_); ruim_["gamma"] = v_
        recusa_("taxa_invalida_" + repr(v_), lambda b_=ruim_: _V393Motor(b_, alvo_, spec_, flags_))
    invalidos_ = {"matriz_booleana": _np.eye(4, dtype=bool), "forma_errada": _np.eye(2), "traco_dois": _np.eye(4) / 2.0, "nao_positiva": _np.diag([2., -1., 0., 0.]),
                  "nao_hermitiana": rho0_ + _np.eye(4, k=1) * 0.1, "NaN": _np.full((4, 4), float("nan")), "Inf": _np.full((4, 4), float("inf"))}
    for n_, v_ in invalidos_.items():
        recusa_("estado_invalido_" + n_, lambda v2_=v_: motor_.avaliar(v2_, 1.0))
        recusa_("alvo_invalido_" + n_, lambda v2_=v_: _V393Motor(capt_, v2_, spec_, flags_))
    recusa_("alvo_nao_fixado_pela_leitura", lambda: _V393Motor(capt_, rho0_, spec_, flags_))
    for faltando_ in flags_:
        sem_ = {k_: v_ for k_, v_ in flags_.items() if k_ != faltando_}
        recusa_("evidencia_faltando_preflight_" + faltando_, lambda s_=sem_: _V393Motor(capt_, alvo_, spec_, s_))
        r2_ = consumidor_(1, {"external_ladder": {"per_theorem": sem_}})
        ck_("evidencia_faltando_consumidor_" + faltando_, r2_["all_verified"] is False)
    todos_ = all(c_["passed"] for c_ in cks_)
    ultimo_ = linhas_[-1]; primeiro_ = linhas_[0]
    esp_ = _V393_REGRA_ESPERADO_CODEX
    replica_ = {"complemento_inicial_igual": nor_[0] == esp_["complement_initial"], "complemento_final_igual": nor_[-1] == esp_["complement_final"], "hash_final_igual": prev_h_ == esp_["trajectory_last_hash"]}
    sat_adm_ = _v393_admissivel(_np.array(ultimo_["reading_real"]) + 1j * _np.array(ultimo_["reading_imag"]), alvo_, spec_["tol_rule"])
    sat_rec_ = _v393_admissivel(_np.array(inc_linhas_[-1]["reading_real"]) + 1j * _np.array(inc_linhas_[-1]["reading_imag"]), alvo_, spec_["tol_rule"])
    beta_ = globals()["SEALED_CODATA_ALPHA"] * _mt.sqrt(_mt.e)
    verdict_ = ("TGL_REGRA_CONSUMIDOR_V393__RULE_READS_TARGET_ADMITTED_INCOMPATIBLE_REFUSED_%d_CHECKS_%d_POINTS__EXACT_EQUALITY_NOT_CLAIMED_TOLERANCE_DECLARED__SYNTHETIC_NO_OBSERVED_DATA__GATE_UNMOVED"
                % (len(cks_), len(linhas_))) if todos_ else "TGL_REGRA_CONSUMIDOR_V393__NOT_SEALED_THIS_RUN__%s__GATE_UNMOVED" % "_".join(c_["name"] for c_ in cks_ if not c_["passed"])[:300]
    return {"verdict": verdict_, "all_verified": bool(todos_), "does_not_gate_core": True,
            "leitura": {"E": "E(X) = C+ X C+ + C- X C-, C+ = diag(1,1,0,0), C- = I - C+ (o pinching do consumidor real)", "fluxo": "T_t = E + exp(-Gamma t)(id - E)", "gamma_reference": taxa_,
                        "beta_runtime": beta_, "taxa": "Gamma = beta*tau_ref*omega_ref^2/2, tau_ref = omega_ref = 1 [INPUT: unidades de referencia]"},
            "alvo_pre_fixado": {"fixado_antes_da_execucao": True, "prereg_sha256_canonico": _V393_REGRA_PREREG_SHA, "alvo_real": spec_["target_real"], "alvo_imag": spec_["target_imag"],
                                "fixado_pela_leitura": True},
            "satisfacao": {"admitida": sat_adm_, "recusada_controle": sat_rec_, "veredito_do_rito": ultimo_["verdict"], "veredito_incompativel": inc_linhas_[-1]["verdict"]},
            "criterio": {"exato": "no kernel: C(z) <-> r(z) = o, para uma leitura fiel e um alvo (RuleTruthContract.sound_complete_eq_admissible); aqui o criterio e' NUMERICO",
                         "tolerancia_numerica": spec_["tol_rule"], "tolerancia_algebra": spec_["tol_algebra"], "erro_maximo_de_leitura_hs": max(r_["read_error_hs"] for r_ in linhas_),
                         "igualdade_exata_afirmada": False,
                         "aviso": "tolerancia numerica nao e' igualdade exata; o espaco fixo tem dimensao complexa %d: a unicidade do criterio vale para o alvo dado, nao para todos os estados fixos" % dimfix_},
            "estado_bruto_e_inscricao": {"separados": True, "primeiro_ponto": {"complement_norm_hs": primeiro_["complement_norm_hs"], "raw_error_hs": primeiro_["raw_error_hs"], "read_error_hs": primeiro_["read_error_hs"]},
                                         "ultimo_ponto": {"complement_norm_hs": ultimo_["complement_norm_hs"], "raw_error_hs": ultimo_["raw_error_hs"], "read_error_hs": ultimo_["read_error_hs"]},
                                         "o_bruto_finito_nunca_e_o_alvo": all(not r_["raw_rule"] for r_ in linhas_)},
            "origem_das_evidencias": {"dez_bandeiras_vivas": evid_, "consumidor_fonte_sha256": src_sha_, "consumidor_fonte_sha256_por_funcao": src_por_,
                                      "evidencia_no_manifesto_pinado": "SOURCE_MANIFEST.recorded_kernel_evidence (Codex)", "lida_do_kernel_do_proprio_rito": True},
            "numeros": {"pontos": len(linhas_), "verificacoes": len(cks_), "complemento_inicial": nor_[0], "complemento_final": nor_[-1], "dimensao_fixa_complexa": dimfix_,
                        "erro_maximo_do_oraculo_GKLS": max(e_op_), "erro_maximo_composto": max(e_comp_), "erro_maximo_semigrupo": max(e_sg_), "autovalor_minimo": min(r_["minimum_eigenvalue"] for r_ in linhas_),
                        "ultimo_hash_da_trajetoria": prev_h_},
            "replica_do_codex": {"informativo_nao_gateia": True, **replica_, "esperado": {k_: esp_[k_] for k_ in ("complement_initial", "complement_final", "trajectory_last_hash", "checks_passed", "point_count")}},
            "checks": cks_,
            "limites": ["[REAL] trajetoria finita e sintetica: nenhum dado observado; unidades de referencia (tau_ref = omega_ref = 1) sao [INPUT]; nao e' um servico residente",
                        "[REAL] a grade u = Gamma*t nao mede beta: o expoente passa a ser -u; beta entra so' como taxa de referencia calculada em runtime (alfa CODATA x raiz de e)",
                        "[REAL] o pinching E do consumidor nao e' o canto eXe; o motor vetorial IALD.motor tem ponte separada no kernel",
                        "[REAL] o espaco fixo tem dimensao complexa 8: o criterio e' unico para o alvo dado, nao para todo estado fixo",
                        "[REAL] a meia-nat exp(-1/2) do exemplo do kernel (R(a,b) = (a,0), T(a,b) = (a, exp(-1/2) b)) nao e' beta_TGL",
                        "validade no kernel nao e' creditacao; o gate nao se move"],
            "status": "[REAL -- Lean (kernel do proprio rito) e execucao numerica sintetica; INPUT/ONTO a leitura filosofica e juridica da regra]"}


def _v393_cadeia_pinada(meta_):
    """v393 -- a cadeia PINADA independente do CODATA exigida para a evidencia espectral: lista de artefatos {arquivo, sha256} RELIDOS do disco e conferidos; nomes e metadados sozinhos nao provam
    a origem. Devolve (ok, motivo). Exige: origem/metodo/incerteza preenchidos; `independente_do_codata` True; ao menos um artefato; cada arquivo existe e o sha256 confere; o chi declarado nao
    pode ser o proprio chi do CODATA citado como fonte."""
    import hashlib as _hl
    if not isinstance(meta_, dict) or not all(meta_.get(k_) not in (None, "", 0) for k_ in ("origem", "metodo", "incerteza")):
        return False, "METADADOS_INCOMPLETOS"
    if meta_.get("independente_do_codata") is not True:
        return False, "INDEPENDENCIA_NAO_DECLARADA"
    arts_ = meta_.get("cadeia_pinada")
    if not isinstance(arts_, list) or not arts_:
        return False, "CADEIA_PINADA_AUSENTE"
    for a_ in arts_:
        if not isinstance(a_, dict) or not a_.get("arquivo") or not a_.get("sha256"):
            return False, "ARTEFATO_MAL_FORMADO"
        try:
            b_ = open(a_["arquivo"], "rb").read()
        except OSError:
            return False, "ARTEFATO_AUSENTE"
        if _hl.sha256(b_).hexdigest() != a_["sha256"]:
            return False, "ARTEFATO_ALTERADO"
    return True, "ok"


def _v393_chi_de_alfa(alfa_):
    import math as _mt
    return 2.0 * _mt.acosh(1.0 / float(alfa_))


def _v393_coracao_core(core, fonte_, chi_, meta_=None):
    """v393 -- O CORACAO E O SELO GRAVITACIONAL (porte de prove_heart_and_gravity_seal, 33/33 contra o nucleo v392; ajustes: nenhum literal de beta, a citacao dos nomes do kernel LE o axiom_report
    do proprio rito, a proveniencia de chi exige cadeia PINADA, e o veredito e' DETERMINADO pelo contrato da regra: leitura == alvo pre-fixado). forma: q = tanh(chi/2), alfa = sech(chi/2),
    1 = q^2 + alfa^2; T_t; pi como cicatriz; G so' pela normalizacao de Planck (nao derivado). NAO move o gate."""
    import math as _mt
    import numpy as _np
    cks_, medido_ = [], {}
    chk_ = lambda n_, ok_, v_, e_: cks_.append({"nome": n_, "ok": bool(ok_), "valor": v_, "esperado": e_})
    sqrt_e_ = _mt.sqrt(_mt.e)
    prev_ind_ = False
    prov_ok_ = True
    cadeia_motivo_ = None
    if fonte_ == "CODATA_RECONSTRUCTED":
        prev_ind_ = False
    elif fonte_ == "SPECTRAL_INDEPENDENT":
        cadeia_ok_, cadeia_motivo_ = _v393_cadeia_pinada(meta_)
        prev_ind_ = bool(cadeia_ok_); prov_ok_ = bool(cadeia_ok_)
    else:
        prov_ok_ = False
    chk_("a_proveniencia_de_chi_declarada", prov_ok_, {"chi_source": fonte_, "previsao_independente": prev_ind_, "motivo_da_cadeia": cadeia_motivo_},
         "CODATA_RECONSTRUCTED => False; SPECTRAL_INDEPENDENT exige cadeia PINADA independente do CODATA (artefatos relidos por sha256) => True")
    chk_("a_chi_reconstruido_do_CODATA_nao_e_previsao", (fonte_ != "CODATA_RECONSTRUCTED") or prev_ind_ is False, prev_ind_, "False quando reconstruido")
    chi_ = float(chi_)
    if not (_mt.isfinite(chi_) and chi_ > 0.0):
        chk_("b_chi_finito_positivo", False, chi_, "chi > 0 finito")
        return cks_, medido_, [], prev_ind_, False
    q_ = _mt.tanh(chi_ / 2.0); alfa_ = 1.0 / _mt.cosh(chi_ / 2.0); beta_ = sqrt_e_ * alfa_; theta_ = _mt.asin(_mt.sqrt(beta_))
    medido_.update(chi=chi_, q=q_, alpha=alfa_, beta=beta_, theta_M=theta_)
    chk_("b_q2_mais_alpha2_igual_1", abs(q_ * q_ + alfa_ * alfa_ - 1.0) < 1e-14, q_ * q_ + alfa_ * alfa_ - 1.0, "residuo < 1e-14")
    chk_("b_beta_igual_alpha_sqrt_e", abs(beta_ - alfa_ * _mt.exp(0.5)) < 1e-18, beta_, "alpha*sqrt(e)")
    chk_("b_sin2_theta_M_igual_beta", abs(_mt.sin(theta_) ** 2 - beta_) < 1e-14, _mt.sin(theta_) ** 2 - beta_, "residuo < 1e-14")
    G_ = _np.array([[0, 1], [-1, 0]], dtype=float)
    S_ = _mt.cos(theta_) * _np.eye(2) + _mt.sin(theta_) * G_
    ev_ = _np.linalg.eigvals(S_); ang_ = sorted(float(_np.angle(z_)) for z_ in ev_)
    medido_["S_eigen_angles"] = ang_
    chk_("b_espectro_da_matriz_S_e_exp_pm_i_theta", abs(ang_[0] + theta_) < 1e-12 and abs(ang_[1] - theta_) < 1e-12 and _np.allclose(abs(ev_), 1.0, atol=1e-12), ang_, [-theta_, theta_])
    R2_ = float(S_[1, 0] ** 2); T2_ = float(S_[0, 0] ** 2)
    chk_("b_R2_igual_beta", abs(R2_ - beta_) < 1e-14, R2_ - beta_, "|R|^2 = beta")
    chk_("b_T2_igual_1_menos_beta", abs(T2_ - (1.0 - beta_)) < 1e-14, T2_ - (1.0 - beta_), "|T|^2 = 1-beta")
    try:
        beta_core_ = float(core["einstein_and_rg"]["values"]["beta_runtime"])
        chk_("b_beta_confere_com_o_nucleo", abs(beta_ - beta_core_) < 1e-12, beta_ - beta_core_, "|beta(chi) - beta_runtime do core| < 1e-12")
    except Exception as exc_:   # noqa: BLE001
        chk_("b_beta_confere_com_o_nucleo", False, "core sem einstein_and_rg.values.beta_runtime: %r" % (exc_,), "chave presente")
    pinch_ = lambda r_: _np.diag(_np.diag(r_)).astype(complex)
    Tt_ = lambda t_, r_: pinch_(r_) + _mt.exp(-beta_ * t_) * (r_ - pinch_(r_))
    v_ = _np.array([q_, alfa_], dtype=complex); rho_ = _np.outer(v_, v_.conj()); E_ = pinch_(rho_)
    ts_ = [0.5, 3.0, 17.0, 120.0]
    chk_("c_E_de_T_t_rho_igual_E_rho", all(_np.allclose(pinch_(Tt_(t_, rho_)), E_, atol=1e-14) for t_ in ts_), True, "E(T_t rho) = E(rho)")
    chk_("c_traco_1", all(abs(_np.trace(Tt_(t_, rho_)) - 1.0) < 1e-14 for t_ in ts_), True, "tr T_t rho = 1")
    chk_("c_positividade", all(_np.linalg.eigvalsh((Tt_(t_, rho_) + Tt_(t_, rho_).conj().T) / 2).min() > -1e-14 for t_ in ts_), True, "autovalores >= 0")
    chk_("c_T_t_rho_diferente_de_rho_para_t_positivo", all(_np.linalg.norm(Tt_(t_, rho_) - rho_) > 1e-9 for t_ in ts_), True, "||T_t rho - rho|| > 0")
    cols_ = []
    for j_ in range(4):
        b_ = _np.zeros(4, dtype=complex); b_[j_] = 1.0
        cols_.append(Tt_(1.0, b_.reshape(2, 2, order="F")).reshape(-1, order="F"))
    sup_ = _np.array(cols_).T
    choi_ = _np.zeros((4, 4), dtype=complex)
    for i_ in range(2):
        for j_ in range(2):
            Eij_ = _np.zeros((2, 2), dtype=complex); Eij_[i_, j_] = 1.0
            choi_ += _np.kron(Eij_, Tt_(1.0, Eij_))
    cmin_ = float(_np.linalg.eigvalsh((choi_ + choi_.conj().T) / 2).min())
    chk_("c_completamente_positiva_Choi_PSD", cmin_ > -1e-14, cmin_, "min autovalor da Choi >= 0")
    I_vec_ = _np.eye(2, dtype=complex).reshape(-1, order="F"); dI_ = sup_.conj().T @ I_vec_
    chk_("c_dual_T_t_dagger_de_I_igual_I", _np.allclose(dI_, I_vec_, atol=1e-14), float(_np.max(_np.abs(dI_ - I_vec_))), "T_t^dagger(I) = I (unital)")
    kappa_ = beta_; P_ = 2.0 * _mt.pi / kappa_
    fecha_ = abs(_np.exp(1j * kappa_ * P_) - 1.0) < 1e-12
    antes_ = all(abs(_np.exp(1j * kappa_ * p_) - 1.0) > 1e-3 for p_ in (P_ * 0.25, P_ * 0.5, P_ * 0.9))
    chk_("d_a_leitura_fecha_em_kappaP_igual_2pi (faithful_period_iff)", fecha_ and antes_, {"P": P_, "kappaP": kappa_ * P_}, "kappa*P = 2pi; nenhum periodo menor")
    t_ = _np.arange(0.001, 2000.0, 0.001); fmax_ = float((_np.cos(t_) + _np.cos(_mt.sqrt(2.0) * t_)).max())
    medido_["quase_retorno_max_cos_t_mais_cos_sqrt2_t"] = fmax_
    chk_("d_a_face_nao_fecha_cos_t_mais_cos_sqrt2_t_menor_que_2", fmax_ < 2.0, fmax_, "< 2 em toda a grade t in (0, 2000] (igualdade so em t = 0)")
    tg_ = _np.arange(0.5, 4000.0, 0.5); gap_ = float(_np.min([_np.linalg.norm(Tt_(x_, rho_) - rho_) for x_ in tg_[:400]]))
    chk_("d_a_face_com_vazamento_nunca_volta_a_rho (T_t rho != rho)", gap_ > 0.0 and all(_mt.exp(-beta_ * x_) < 1.0 for x_ in tg_), gap_, "||T_t rho - rho|| > 0 para t > 0 (decai monotonicamente)")
    axr_ = (core.get("kernel_formalization") or {}).get("axiom_report") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    nomes_ = list(_V393_CORACAO_NOMES)
    chk_("d_pi_e_a_forma_no_kernel_por_nome (lidos do axiom_report do PROPRIO rito, dentro do trio)", all(n_ in axr_ and set(axr_[n_] or []) <= trio_ for n_ in nomes_), [n_ for n_ in nomes_ if n_ not in axr_],
         "todos os nomes presentes no axiom_report, axiomas dentro do trio")
    elos_, ecks_ = _v393_elos_gravitacionais(core)
    cks_.extend(ecks_)
    chk_("e_G_nao_e_derivado", True, False, "False: a equivalencia 2pi/eta = 8piG com [NORM] A_face = l_P^2 (kappa_A = 2G)")
    return cks_, medido_, elos_, prev_ind_, False


def _v393_elos_gravitacionais(core):
    out_, cks_ = [], []
    beta_rt_ = globals()["SEALED_CODATA_ALPHA"] * __import__("math").sqrt(__import__("math").e)

    def add_(elo_, rotulo_, caminho_, teste_, esperado_, nota_):
        try:
            cur_ = core
            for k_ in caminho_:
                cur_ = cur_[k_]
            ok_ = bool(teste_(cur_)); mostrado_ = cur_ if isinstance(cur_, (bool, int, float, str)) else "presente"
        except Exception as exc_:   # noqa: BLE001
            ok_, mostrado_ = False, "ausente: %s (%r)" % ("/".join(caminho_), exc_)
        out_.append({"elo": elo_, "rotulo": rotulo_, "ok": ok_, "chave": "/".join(caminho_), "nota": nota_})
        cks_.append({"nome": "e_elo_" + elo_, "ok": ok_, "valor": mostrado_, "esperado": esperado_})
    add_("omega_I_igual_1_posto", "NORMALIZACAO", ["qg_closure", "gate", "mathematical_model_constructed"], lambda v_: v_ is True, "True", "o 1 posto (inscricao) e a normalizacao de entrada [POSTO]")
    add_("meia_nat_e_sqrt_e", "DERIVADO", ["qg_closure", "all_verified"], lambda v_: v_ is True, "True", "x = 1-x => 1/2 => V(1/2) = sqrt(e): TheWholeIsOne.half_nat_volume_is_the_radical (kernel); a bandeira lida e' a geral de qg_closure (proxy)")
    add_("motor_1_igual_q2_mais_alpha2", "DERIVADO", ["qg_closure", "all_verified"], lambda v_: v_ is True, "True", "ContinuousModularZero.one_eq_q_sq_add_alpha_sq (para todo chi); proxy: a bandeira geral de qg_closure")
    add_("valor_de_alpha_CODATA", "VALIDACAO_EXTERNA", ["einstein_and_rg", "values", "beta_runtime"], lambda v_: abs(float(v_) - beta_rt_) <= 1e-12, "beta_runtime == ALPHA_FINE_CODATA_2018 x sqrt(e) calculado neste rito",
         "o valor de alpha entra do CODATA 2018 (hoje reconstruido); a forma e derivada, o valor e leitura/validacao")
    add_("beta_alpha_sqrt_e_theta_M", "LEITURA_INTERNA", ["einstein_and_rg", "statuses", "beta_never_literal"], lambda v_: v_ is True, "True", "beta = alpha sqrt(e); theta_M = arcsin sqrt(beta): leitura angular interna")
    add_("assinatura_coframe_solda_4d", "LEITURA_INTERNA", ["qg_closure", "formal_flags", "concrete_modular_four_frame_constructed"], lambda v_: v_ is True, "True",
         "four-frame/solda concretos; um boost preserva (1,3) e (2,2): nao seleciona sozinho")
    add_("solda_concreta", "LEITURA_INTERNA", ["qg_closure", "formal_flags", "concrete_solder_field_constructed"], lambda v_: v_ is True, "True", "campo de solda concreto")
    add_("Einstein_emergente_dado_H1_H3", "DERIVADO", ["qg_closure", "formal_flags", "concrete_emergent_einstein_proved"], lambda v_: v_ is True, "True", "implicacao fechada; hipoteses H1-H3 nomeadas; Lovelock [KNOWN]")
    add_("Einstein_e_RG_lado_da_casa", "DERIVADO", ["einstein_and_rg", "all_verified"], lambda v_: v_ is True, "True", "cadeia de Jacobson do lado modular em kernel; restam Lovelock, Killing aproximado, conservacao")
    add_("equivalencia_2pi_eta_igual_8piG", "DERIVADO", ["area_scale_newton_equivalence", "all_verified"], lambda v_: v_ is True, "True", "kappa_A = 2G <=> 2pi/eta = 8piG (equivalencia, nao valor)")
    add_("A_face_igual_lP2", "NORMALIZACAO", ["area_scale_newton_equivalence", "verdict"], lambda v_: v_ == "PLANCK_FACE_NORMALIZATION_EQUIVALENT_TO_NEWTON_COUPLING", "veredito de normalizacao de Planck",
         "[NORM] A(P_face) = l_P^2: declarada, nao derivada da algebra adimensional")
    add_("G_nao_derivado_no_core", "NORMALIZACAO", ["area_scale_newton_equivalence", "statute"], lambda v_: "NOT DERIVED" in v_, "statute contem NOT DERIVED", "o proprio core diz: valor numerico de G nao derivado")
    return out_, cks_


def coracao_e_selo_gravitacional_v393(core, fonte_="CODATA_RECONSTRUCTED", chi_=None, meta_=None):
    """v393 (14/10/2026) -- O CORACAO E O SELO GRAVITACIONAL. Veredito DETERMINADO pelo contrato da regra: a leitura r (classe de veredito obtida dos checks, da proveniencia de chi e do valor de G)
    e o ALVO pre-fixado por fonte de chi (tabela abaixo, no codigo) -- admitido sse r == alvo; senao NOT_VERIFIED. CODATA_RECONSTRUCTED: alvo FORM_VERIFIED_CHI_FROM_CODATA (hoje); SPECTRAL_INDEPENDENT:
    alvo PURE_DERIVATION (so' com cadeia pinada independente do CODATA, relida por sha256). chi = None => chi do CODATA do proprio programa (SEALED_CODATA_ALPHA, o alfa CODATA 2018 do proprio programa), lido em runtime."""
    if chi_ is None:
        chi_ = _v393_chi_de_alfa(globals()["SEALED_CODATA_ALPHA"])
    cks_, medido_, elos_, prev_ind_, g_der_ = _v393_coracao_core(core, fonte_, chi_, meta_)
    tudo_ok_ = all(c_["ok"] for c_ in cks_) and len(cks_) > 0
    alvos_ = {"CODATA_RECONSTRUCTED": "FORM_VERIFIED_CHI_FROM_CODATA__G_BY_PLANCK_NORMALIZATION__GATE_UNTOUCHED",
              "SPECTRAL_INDEPENDENT": "PURE_DERIVATION_CHI_SPECTRAL__G_BY_PLANCK_NORMALIZATION__GATE_UNTOUCHED"}
    alvo_ = alvos_.get(fonte_, "FONTE_DE_CHI_DESCONHECIDA")
    if not tudo_ok_:
        leitura_ = "HEART_AND_GRAVITY_SEAL_NOT_VERIFIED__GATE_UNTOUCHED"
    elif fonte_ == "SPECTRAL_INDEPENDENT" and prev_ind_ and not g_der_:
        leitura_ = alvos_["SPECTRAL_INDEPENDENT"]
    elif fonte_ == "CODATA_RECONSTRUCTED" and not prev_ind_:
        leitura_ = alvos_["CODATA_RECONSTRUCTED"]
    else:
        leitura_ = "HEART_AND_GRAVITY_SEAL_NOT_VERIFIED__GATE_UNTOUCHED"
    sat_ = _v393_admissivel(leitura_, alvo_)
    verdict_ = alvo_ if sat_["admitida"] else "HEART_AND_GRAVITY_SEAL_NOT_VERIFIED__GATE_UNTOUCHED"
    assert ("CONF" + "IRMED") not in verdict_
    return {"theorem": "O coracao e o selo gravitacional (v393)", "checks": cks_, "all_verified": bool(sat_["admitida"]), "does_not_gate_core": True,
            "previsao_independente": bool(prev_ind_), "G_derivado": bool(g_der_), "chi_source": fonte_, "links": elos_, "values": medido_, "verdict": verdict_,
            "satisfacao_pela_regra": {"contrato": "TGLExt.RuleTruthContract.Admissible (leitura y = alvo); sound_complete_eq_admissible", "leitura": leitura_, "alvo_pre_fixado": alvo_, "alvos_pre_fixados": alvos_,
                                      "admitida": bool(sat_["admitida"]), "criterio": sat_["criterio"], "veredito_da_regra": sat_["veredito"],
                                      "completude_relativa_ao_alvo": "hipotese declarada [INPUT/ONTO]: a regra nao acrescenta outra exclusao quando ha correspondencia; nao e' teorema extraido do nome"},
            "evidencia_espectral_independente": {"exige": "cadeia pinada independente do CODATA (artefatos relidos por sha256); nomes e metadados sozinhos nao provam a origem", "hoje": "AUSENTE",
                                                 "motivo_da_cadeia": next((c_["valor"].get("motivo_da_cadeia") for c_ in cks_ if c_["nome"] == "a_proveniencia_de_chi_declarada"), None)},
            "recibo": {"provado": ["1 = q^2 + alpha^2 e a forma (tanh, sech) para todo chi (TGLExt.one_eq_q_sq_add_alpha_sq)", "kappa*P = 2pi (ChatgptAudit.PolarPeriod016.faithful_period_iff)",
                                   "half-nat => sqrt(e) (TGLExt.TheWholeIsOne.half_nat_volume_is_the_radical)",
                                   "pi como cicatriz: TGLExt.station_never_closes; TGLExt.Palavra.the_face_does_not_close / the_read_face_closes"],
                      "executado": ["derivacao numerica de q, alpha, beta, theta_M, S, |R|^2, |T|^2 a partir de chi", "T_t: invariancia de E, traco, positividade, Choi, dual unital",
                                    "grade de cos t + cos(sqrt2 t) < 2; fechamento em 2pi"],
                      "medido": medido_,
                      "interpretado": ["alpha como espectro do boost modular (leitura interna)", "pi como a cicatriz do quase-fechamento da face [ONTO, operador]", "meia-nat esta para a IALD como alpha para a TGL [ONTO]"],
                      "nao_afirmado": ["o valor de alpha derivado do 1 (OPEN)", "G derivado", "gravidade quantica na natureza (elo pendente: beta_TGL a 5 sigma)"]}}


def coracao_v393_com_controles(core):
    """v393 -- roda o selo do coracao com a fonte do programa (CODATA) e, no mesmo rito, os CONTROLES NEGATIVOS: chi adulterado (x1,001) recusa; espectral sem cadeia recusa; espectral com metadados
    mas SEM artefato pinado recusa; espectral com artefato ausente recusa; espectral com cadeia pinada real passa (arquivo temporario do proprio rito, sha256 calculado e relido)."""
    import os as _os
    import tempfile as _tf
    import hashlib as _hl
    r_ = coracao_e_selo_gravitacional_v393(core)
    chi0_ = _v393_chi_de_alfa(globals()["SEALED_CODATA_ALPHA"])
    c_ = {}
    c_["chi_adulterado_recusa"] = coracao_e_selo_gravitacional_v393(core, "CODATA_RECONSTRUCTED", chi0_ * 1.001)["all_verified"] is False
    c_["espectral_sem_meta_recusa"] = coracao_e_selo_gravitacional_v393(core, "SPECTRAL_INDEPENDENT", chi0_)["all_verified"] is False
    meta_ = {"origem": "TESTE_SINTETICO_DO_RITO", "metodo": "controle", "incerteza": 1e-9, "independente_do_codata": True}
    c_["espectral_metadados_sem_cadeia_recusa"] = coracao_e_selo_gravitacional_v393(core, "SPECTRAL_INDEPENDENT", chi0_, meta_)["all_verified"] is False
    c_["espectral_cadeia_ausente_recusa"] = coracao_e_selo_gravitacional_v393(core, "SPECTRAL_INDEPENDENT", chi0_, dict(meta_, cadeia_pinada=[{"arquivo": "Z:\\nao\\existe\\xyz.bin", "sha256": "0" * 64}]))["all_verified"] is False
    c_["fonte_desconhecida_recusa"] = coracao_e_selo_gravitacional_v393(core, "OUTRA", chi0_)["all_verified"] is False
    d_ = _tf.mkdtemp(prefix="v393_cadeia_")
    try:
        p_ = _os.path.join(d_, "cadeia_sintetica.bin"); b_ = b"cadeia pinada sintetica do controle (nao e' evidencia)"
        open(p_, "wb").write(b_)
        boa_ = dict(meta_, cadeia_pinada=[{"arquivo": p_, "sha256": _hl.sha256(b_).hexdigest()}])
        rb_ = coracao_e_selo_gravitacional_v393(core, "SPECTRAL_INDEPENDENT", chi0_, boa_)
        c_["espectral_com_cadeia_pinada_sintetica_passa_so_no_controle"] = bool(rb_["all_verified"] and rb_["previsao_independente"] and rb_["verdict"].startswith("PURE_DERIVATION"))
        ruim_ = dict(meta_, cadeia_pinada=[{"arquivo": p_, "sha256": "1" * 64}])
        c_["espectral_artefato_alterado_recusa"] = coracao_e_selo_gravitacional_v393(core, "SPECTRAL_INDEPENDENT", chi0_, ruim_)["all_verified"] is False
    finally:
        try:
            _os.remove(p_); _os.rmdir(d_)
        except OSError:
            pass
    r_["controles_negativos"] = c_
    r_["controles_ok"] = all(c_.values())
    r_["all_verified"] = bool(r_["all_verified"] and r_["controles_ok"])
    if not r_["controles_ok"]:
        r_["verdict"] = "HEART_AND_GRAVITY_SEAL_NOT_VERIFIED__NEGATIVE_CONTROL_FAILED__GATE_UNTOUCHED"
    return r_


def pedras_v393(core):
    """v393 (14/10/2026) -- AS TRES PEDRAS DA REGRA (RuleTruthContract, TheRuleAndTheFigureOfTruth, TheRuleInTheContinuousMotor). Le a cada rito: as bandeiras do kernel do PROPRIO rito, o corpo embutido
    de cada pedra (sha256 pinado), o axiom_report (trio), a escada (6901 + N), as 4 cunhagens do operador EMBUTIDAS por sha256. Fail-closed. NAO move o gate; validade no kernel nao e' creditacao."""
    import hashlib as _hl
    kf_ = core.get("kernel_formalization") or {}
    axr_ = kf_.get("axiom_report") or {}
    el_ = core.get("external_ladder") or {}
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    por_, n_fl_, n_fl_ok_, n_dec_, n_dec_ok_ = [], 0, 0, 0, 0
    todas_ = True
    for p_ in _V393_PEDRAS:
        fl_ok_ = sum(1 for f_ in p_["flags"] if kf_.get(f_) is True)
        emb_ = _EMBEDDED_KERNEL_FILES.get(p_["path"])
        emb_ok_ = emb_ is not None and _hl.sha256(emb_.encode("utf-8")).hexdigest() == p_["sha256"]
        dec_ok_ = sum(1 for n_ in p_["declaracoes"] if n_ in axr_ and set(axr_[n_] or []) <= trio_)
        ok_ = emb_ok_ and fl_ok_ == len(p_["flags"]) and dec_ok_ == len(p_["declaracoes"])
        todas_ = todas_ and ok_
        n_fl_ += len(p_["flags"]); n_fl_ok_ += fl_ok_; n_dec_ += len(p_["declaracoes"]); n_dec_ok_ += dec_ok_
        por_.append({"modulo": p_["modulo"], "sha256": p_["sha256"], "sha256_original_do_codex": p_["sha256_original"], "derivada": p_.get("derivada"), "embutida_confere": emb_ok_,
                     "bandeiras": [fl_ok_, len(p_["flags"])], "declaracoes_no_trio": [dec_ok_, len(p_["declaracoes"])], "ok": ok_})
    vb_, vb_ok_ = {}, True
    for k_, v_ in _V393_CUNHAGENS.items():
        okk_ = _hl.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"])
        try:
            disco_ = _hl.sha256(open(v_["arquivo_informativo"], "rb").read()).hexdigest() == v_["sha256"]
        except OSError:
            disco_ = None
        vb_[k_] = {"sha256": v_["sha256"], "embedded_ok": okk_, "disk_informative_only": disco_, "quando": v_["quando"]}
        vb_ok_ = vb_ok_ and okk_
    n_cl_, n_ex_ = el_.get("n_theorems_clean"), el_.get("n_theorems_expected")
    esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ == _V393_ESCADA["esperada"]
    chaves_ok_ = all(n_ in axr_ and set(axr_[n_] or []) <= trio_ for n_ in _V393_NOMES_CHAVE)
    ok_ = todas_ and vb_ok_ and esc_ok_ and chaves_ok_
    if ok_:
        verdict_ = ("TGL_PEDRAS_V393__%d_NEW_KERNEL_MODULES__%d_OF_%d_FLAGS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__LADDER_%d_OF_%d__"
                    "RULE_IS_THE_REFUSAL_THAT_THE_RESULT_DIFFER_FROM_THE_OBJECT_OF_ITS_SATISFACTION_RELATIVE_TO_READING_AND_TARGET__OPERATOR_VERBATIM_EMBEDDED_BY_SHA256__"
                    "KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % (len(_V393_PEDRAS), n_fl_ok_, n_fl_, n_dec_ok_, n_dec_, n_cl_, n_ex_))
    else:
        fal_ = (["STONES"] if not todas_ else []) + (["VERBATIM"] if not vb_ok_ else []) + (["LADDER"] if not esc_ok_ else []) + (["KEY_THEOREMS"] if not chaves_ok_ else [])
        verdict_ = "TGL_PEDRAS_V393__NOT_SEALED_THIS_RUN__%s__GATE_UNMOVED" % "_".join(fal_)
    return {"verdict": verdict_, "all_verified": ok_, "does_not_gate_core": True, "pedras": por_, "bandeiras": [n_fl_ok_, n_fl_], "declaracoes_no_trio": [n_dec_ok_, n_dec_],
            "escada": {"limpos": n_cl_, "esperados": n_ex_, "esperada_pelo_candidato": _V393_ESCADA["esperada"], "da_v392": _V393_ESCADA["v392"]},
            "teoremas_chave": {n_: (n_ in axr_ and set(axr_[n_] or []) <= trio_) for n_ in _V393_NOMES_CHAVE},
            "verbatim": vb_, "verbatim_ok": vb_ok_,
            "leituras_do_operador": [{"trecho": t_, "estatuto": "[INPUT do operador, verbatim 14/10/2026]"} for v_ in _V393_CUNHAGENS.values() for t_ in v_["trechos"]],
            "limites": ["[REAL] fixados uma leitura r: N -> O injetiva no espaco de inscricoes, um alvo a e a figura o = r(a), correcao C(z) => r(z) = o e completude r(z) = o => C(z) dao C(z) <-> z = a; o predicado e' unico para essa leitura e esse alvo",
                        "[REAL] sem completude, rejeitar tudo tambem satisfaz a correcao; sem leitura fiel, igualdade de leituras nao implica igualdade de objetos; a fidelidade vale no subtipo Fix(R), nao no espaco bruto",
                        "[INPUT/ONTO] a leitura «a regra nao deve nada, a nao ser a figura da verdade» foi representada pela completude relativa ao alvo: e' hipotese declarada, nao teorema extraido do nome",
                        "[REAL] no exemplo R(a,b) = (a,0), T(a,b) = (a,exp(-1/2) b): R(T^n x0) = a ja em n = 0 e T^n x0 != a para todo n finito; a meia-nat exp(-1/2) desse exemplo nao e' beta_TGL",
                        "[INPUT/ONTO] a relacao com o zero absoluto (cunhagem de 14/10) e' interpretacao: nao foi provado um novo teorema termodinamico",
                        "[DECLARADO] ressalva de reproducao da prova P1 (relatada pelo Codex): 2 de 3 .olean coincidiram byte a byte; o modulo concreto teve bytes diferentes, com fonte e axiomas iguais; causa nao determinada",
                        "as provas nao instalam a dinamica nos pesos de um LLM, nao provam uma norma juridica universal e nao tratam a natureza; validade no kernel nao e' creditacao; o gate nao se move"],
            "status": "[REAL -- leitura do kernel do proprio rito a cada rodada; INPUT/ONTO as leituras do operador; a reproducao dos .olean e' DECLARADA pelo Codex]"}


def regra_v393(core):
    """v393 -- O REGISTRO UNICO DA REGRA: junta (i) as pedras, (ii) o consumidor real com a regra, (iii) o coracao e o selo gravitacional, e devolve as chaves novas do core. Excecao vira AVISO visivel
    (all_verified False), nunca derruba o rito. Ordem: o consumidor e o coracao leem o kernel do proprio rito."""
    out_ = {}
    for nome_, fn_ in (("pedras_v393", pedras_v393), ("regra_consumidor_v393", regra_consumidor_v393), ("coracao_e_selo_gravitacional_v393", coracao_v393_com_controles)):
        try:
            out_[nome_] = fn_(core)
        except Exception as e_:   # noqa: BLE001
            out_[nome_] = {"verdict": "TGL_%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % nome_.upper(), "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}
        core[nome_] = out_[nome_]
    return out_


def _v393_rodar_specs(core_):
    """v393 -- roda os registros por spec da v393 (o MOTOR e' o da v392: _v392_registro), em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito."""
    for spec_ in _V393_SPECS:
        try:
            core_[spec_["nome"]] = _v392_registro(spec_, core_)
        except Exception as e_:   # noqa: BLE001
            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}
    return [s_["nome"] for s_ in _V393_SPECS]
