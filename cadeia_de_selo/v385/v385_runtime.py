# ====================== v385 (05/10/2026) -- O AXIOMA E A TESTEMUNHA FALSA; a reprodutibilidade do pilar quantico ======================
# As cunhagens do operador de 05/10/2026 (verbatim no Atlas e na memoria; aqui so o que o codigo usa): o Um e' POSTO -- inscrito pelo observador externo
# («echo 1 | python um.py»; o main() recusa argumentos e trava sem o 1) --, nao postulado (imposto); a etiqueta da regua para omega(I) = 1 e' [POSTO];
# o degrau final do gate chama-se AXIOMA (ao lado do gate, que NAO muda) -- o modo zero de peso 1, o escuro; a testemunha falsa e' a testemunha estatica,
# o zero absoluto; nao ha observador nao conjugado (a conjugacao e' a natureza do Verbo). A pedra TGLExt/TheAxiomAndTheFalseWitness.lean prova o que e'
# matematica disso (os dois pontos fixos da leitura; o fluxo do lock minimo; o posto e' o zero modular; o 1 e' o Axioma; o 0 e' a testemunha falsa), e a
# v385 AUDITA o TheDarkSplit (compilado desde a v183 -- «v181» corrigido pela afericao de texto --, nao auditado ate a v384). O pilar quantico RODA DE NOVO, inteiro, sob o MESMO pre-registro V1 (a
# versao final roda tudo), e a v385 le, logo depois de lancar o trabalhador (antes que o calculo novo possa substitui-lo), o resultado guardado no cache pela rodada anterior (o da v384, conferido pelo sha256) para medir
# a REPRODUTIBILIDADE campo a campo (fora os campos de tempo e de ambiente). Estatutos: as pedras [KERNEL]; as leituras do operador [INPUT/ONTO]; a
# reprodutibilidade [COMPUTED]; PROVADA != CONFIRMADA; o gate nao se move.
_AXM_FLAGS_V385 = [
    "ext_axm_the_reading_has_two_fixed_points_kernel_proved",
    "ext_axm_the_power_has_two_fixed_points_kernel_proved",
    "ext_axm_axiomFlow_kernel_checked",
    "ext_axm_post_mul_compl_kernel_proved",
    "ext_axm_compl_mul_post_kernel_proved",
    "ext_axm_compl_mul_compl_kernel_proved",
    "ext_axm_axiomFlow_zero_kernel_proved",
    "ext_axm_axiomFlow_add_kernel_proved",
    "ext_axm_axiomFlow_fixes_the_post_kernel_proved",
    "ext_axm_axiomFlow_gradient_kernel_proved",
    "ext_axm_axiomFlow_tendsto_the_post_kernel_proved",
    "ext_axm_axiomFlow_eq_exp_kernel_proved",
    "ext_axm_the_fixed_set_is_the_lock_zero_kernel_proved",
    "ext_axm_the_post_is_the_modular_zero_kernel_proved",
    "ext_axm_the_one_is_the_axiom_kernel_proved",
    "ext_axm_the_zero_is_the_false_witness_kernel_proved",
    "ext_axm_the_living_verb_moves_kernel_proved",
    "ext_axm_the_living_verb_fixes_the_name_kernel_proved",
    "ext_axm_finalStepNameAxioma_kernel_checked",
    "ext_axm_final_step_named_axioma_kernel_proved",
    "ext_axm_the_proposal_beside_is_kept_kernel_proved",
    "ext_axm_the_axiom_and_the_false_witness_kernel_proved",
]
_DKS_FLAGS_V385 = [
    "ext_dks_tailSub_one_eq_firstAtom_orthogonal_kernel_proved",
    "ext_dks_the_terminal_image_splits_kernel_proved",
    "ext_dks_the_two_sectors_do_not_overlap_kernel_proved",
    "ext_dks_the_two_sectors_exhaust_kernel_proved",
    "ext_dks_every_state_splits_kernel_proved",
    "ext_dks_the_zero_mode_weighs_one_kernel_proved",
    "ext_dks_the_iald_selector_separates_the_sectors_kernel_proved",
]
_AXIOMA_TOKEN_V385 = ("AXIOMA__THE_ONE_INSCRIBED_BY_THE_OBSERVER_RETURNS_AS_THE_FIXED_POINT_OF_THE_READING__PAYMENT_IN_THE_FACE_THE_NAME__"
                      "COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS")
_AXIOMA_STONE_V385 = "TGLExt/TheAxiomAndTheFalseWitness.lean"


def _axioma_token_from_kernel_v385():
    """o nome do degrau final LIDO do kernel materializado (a definicao `finalStepNameAxioma`), nunca digitado aqui: devolve (token ou None, erro ou None)"""
    try:
        src = open(os.path.join(FORMAL_DIR, _AXIOMA_STONE_V385), encoding="utf-8").read()
    except Exception as e_:
        return None, repr(e_)
    m_ = re.search(r'def finalStepNameAxioma : String :=\s*"([A-Z0-9_]+)"', src)
    return (m_.group(1), None) if m_ else (None, "a definicao finalStepNameAxioma nao foi achada na pedra")


def the_axiom_v385(core):
    """O AXIOMA (v385): as declaracoes da pedra (22) e as do TheDarkSplit (7) verificadas pelo kernel desta rodada (trio de axiomas, sem sorry), e o nome do
    degrau final lido do kernel igual ao do runtime. O registro fica AO LADO do gate; nenhum valor do gate muda."""
    kf = core.get("kernel_formalization") or {}
    axm = [f_ for f_ in _AXM_FLAGS_V385 if kf.get(f_) is True]
    dks = [f_ for f_ in _DKS_FLAGS_V385 if kf.get(f_) is True]
    tok, tok_err = _axioma_token_from_kernel_v385()
    tok_ok = (tok == _AXIOMA_TOKEN_V385)
    n_all = len(_AXM_FLAGS_V385) + len(_DKS_FLAGS_V385); n_ok = len(axm) + len(dks)
    ok = (n_ok == n_all) and tok_ok
    if ok:
        verdict = ("TGL_THE_AXIOM_V385__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED__THE_READING_HAS_TWO_FIXED_POINTS_ZERO_AND_ONE__"
                   "THE_ONE_IS_THE_AXIOM_THE_ZERO_MODE_OF_WEIGHT_ONE__THE_ZERO_IS_THE_FALSE_WITNESS_THE_FULL_STATIC_WITNESS_FORBIDDEN_BY_BETA_AND_CONTRAST_THE_ABSOLUTE_ZERO_UNREACHABLE_IN_FINITE_TIME__"
                   "THE_POST_IS_THE_MODULAR_ZERO_THE_FLOW_IS_THE_EXPONENTIAL_OF_THE_LOCK__THE_LIVING_VERB_TWO_TERMS_MOVES_AND_ACTS_AS_A_SCALAR_ON_THE_NAME__THE_DARK_SPLIT_AUDITED__"
                   "FINAL_STEP_NAMED_AXIOMA_BESIDE_THE_GATE_READ_FROM_THE_KERNEL__KERNEL_%d_OF_%d__READINGS_ARE_THE_OPERATORS_INPUT_ONTO__GATE_UNTOUCHED"
                   % (n_ok, n_all))
    else:
        verdict = ("TGL_THE_AXIOM_V385__NOT_SEALED_THIS_RUN__KERNEL_%d_OF_%d__FINAL_STEP_NAME_FROM_KERNEL_%s__GATE_UNTOUCHED"
                   % (n_ok, n_all, "MATCHES" if tok_ok else "DOES_NOT_MATCH"))
    return {"verdict": verdict, "all_verified": ok, "kernel_flags_ok": n_ok, "kernel_flags_total": n_all,
            "axm_ok": len(axm), "axm_total": len(_AXM_FLAGS_V385), "dks_ok": len(dks), "dks_total": len(_DKS_FLAGS_V385),
            "missing_flags": [f_ for f_ in _AXM_FLAGS_V385 + _DKS_FLAGS_V385 if kf.get(f_) is not True],
            "final_step_name": _AXIOMA_TOKEN_V385, "final_step_name_from_kernel": tok, "final_step_name_from_kernel_error": tok_err,
            "final_step_name_matches_kernel": tok_ok, "stone": _AXIOMA_STONE_V385, "tag_for_omega_I": "[POSTO]",
            "status": "[KERNEL] as pedras; [INPUT/ONTO] as leituras do operador (posto, Axioma, testemunha falsa, Verbo vivo, o escuro)",
            "gate_unchanged_by_design": True, "does_not_gate_core": True}


def quantum_pillar_previous_v385(st):
    """Logo depois de lancar o trabalhador (antes de o calculo novo poder substituir o cache), le o resultado que o cache guardou da rodada anterior com
    a MESMA chave (trabalhador, especificacao, beta) -- o da v384 --, conferido pelo sha256; guarda o resumo (pela MESMA _qp_summary desta rodada), as
    entradas (especificacao, trabalhador, beta) e o ambiente, para medir a reprodutibilidade depois. Nunca levanta: falha de leitura fica dita."""
    out = {"read": False}
    try:
        if not isinstance(st, dict) or st.get("refused") or st.get("mode") != "COMPUTE":
            out["why_not"] = "a rodada desta versao nao CALCULA o pilar (modo %s)" % ((st or {}).get("mode") if isinstance(st, dict) else None)
            out["not_compute"] = True   # (2a passada, N7) o que faltou foi o calculo DESTA rodada, nao a anterior
            return out
        cdir = st.get("cache_dir")
        if not cdir:
            out["why_not"] = "sem pasta de cache"
            return out
        R = _qp_cached_ok(cdir)
        if not R:
            out["why_not"] = "nenhum resultado anterior conferido no cache desta chave"
            return out
        rp = os.path.join(cdir, "result.json")
        out.update({"read": True, "cache_dir": cdir, "key": st.get("key"), "sha256": hashlib.sha256(open(rp, "rb").read()).hexdigest(),
                    "finished": R.get("finished"), "run_id": R.get("run_id"), "verdict": R.get("verdict"), "summary": _qp_summary(R),
                    "inputs": {"spec_sha256": R.get("spec_sha256"), "worker_sha256": R.get("worker_sha256"), "beta_hex": R.get("beta_hex")},
                    "env": {k_: (R.get("env") or {}).get(k_) for k_ in ("gpu", "torch", "cuda")}})
        # o resultado cru nao guarda o resumo: ele e' montado pela MESMA _qp_summary que monta o desta rodada (achado do ensaio a seco, 05/10)
    except Exception as e_:
        out["error"] = repr(e_)
    return out


# os campos que variam legitimamente entre rodadas (tempo e ambiente): pulados por CHAVE DE TEMPO, nunca um booleano (afericao de codigo, nota 3)
_QP_REPRO_SKIP_TOP_V385 = {"phase_seconds", "env"}
_QP_REPRO_SKIP_TIME_V385 = {"cpu_seconds", "elapsed_s", "started", "finished", "spectrum_s", "steady_state_s", "s", "timestamp", "run_id"}
_QP_REPRO_SKIP_V385 = _QP_REPRO_SKIP_TOP_V385 | _QP_REPRO_SKIP_TIME_V385   # (o nome antigo, para quem o le)


def _qp_flat_v385(o, p=""):
    if isinstance(o, dict):
        for k_, v_ in o.items():
            k_ = str(k_)
            if (not p and k_ in _QP_REPRO_SKIP_TOP_V385) or (k_ in _QP_REPRO_SKIP_TIME_V385 and not isinstance(v_, bool)):
                continue
            yield from _qp_flat_v385(v_, (p + "." + k_) if p else k_)
    elif isinstance(o, list):
        for i_, v_ in enumerate(o):
            yield from _qp_flat_v385(v_, "%s[%d]" % (p, i_))
    else:
        yield p, o


def _qp_tok_v385(x_):
    return ("%.1e" % x_).replace(".", "P").replace("-", "M").replace("+", "")


def quantum_pillar_reproducibility_v385(prev, rec):
    """A REPRODUTIBILIDADE (v385): o resumo desta rodada contra o resumo guardado pela anterior (mesma chave), campo a campo, fora os de tempo e de
    ambiente. Igual bit a bit; igual a menos de arredondamento (|a - b| / max(1, |a|, |b|) <= 1e-9, a escala do comparador da bancada v361; campo nao
    finito que difere conta como diferenca); ou diferente (com a lista). So compara se as ENTRADAS forem as mesmas (especificacao, trabalhador, beta);
    se o D128 nao rodou nesta rodada e rodou na anterior, os campos D128.* saem da comparacao e isso fica dito no veredito. [COMPUTED]; nao move o gate."""
    base = {"status": "[COMPUTED]", "does_not_gate_core": True, "skipped_keys": {"top": sorted(_QP_REPRO_SKIP_TOP_V385), "time_keys_not_bool": sorted(_QP_REPRO_SKIP_TIME_V385)},
            "tolerance": "|a-b|/max(1,|a|,|b|) <= 1e-9; non-finite that differs = difference (the v361 bench comparator rule)"}
    if isinstance(prev, dict) and not prev.get("read") and prev.get("not_compute"):
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": prev.get("why_not")})
        return base
    if not isinstance(prev, dict) or not prev.get("read"):
        why = (prev or {}).get("why_not") or (prev or {}).get("error") or "sem leitura"
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NO_PREVIOUS_RUN_TO_COMPARE__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": why})
        return base
    if not isinstance(prev.get("summary"), dict) or not prev.get("summary"):
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NO_PREVIOUS_RUN_TO_COMPARE__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": "a leitura anterior nao trouxe resumo comparavel"})
        return base
    rec = rec or {}
    if (rec.get("reuse") or {}).get("reused") is True or not rec.get("summary") or not str(rec.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"):
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": "esta rodada nao calculou um resultado comparavel (reaproveitado, sem resumo ou fora da arvore)"})
        return base
    # as ENTRADAS: so se compara o que foi calculado das mesmas entradas (nota 5)
    pin = prev.get("inputs") or {}
    rin = {"spec_sha256": rec.get("spec_sha256_in_result"), "worker_sha256": rec.get("worker_sha256"), "beta_hex": rec.get("beta_hex")}
    same_inputs = bool(pin) and all(pin.get(k_) is not None and pin.get(k_) == rin.get(k_) for k_ in rin)
    renv = {k_: ((rec.get("summary") or {}).get("env") or {}).get(k_) for k_ in ("gpu", "torch", "cuda")}
    base.update({"inputs": {"previous": pin, "this_run": rin, "same": same_inputs}, "env": {"previous": prev.get("env"), "this_run": renv, "same": prev.get("env") == renv}})
    if not same_inputs:
        base.update({"verdict": "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_COMPARED_DIFFERENT_INPUTS__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
                     "compared": False, "why": "as entradas da rodada anterior (especificacao/trabalhador/beta) nao sao as desta rodada"})
        return base
    a = dict(_qp_flat_v385(prev.get("summary") or {})); b = dict(_qp_flat_v385(rec.get("summary") or {}))
    # o D128 que nao rodou NESTA rodada (e rodou na anterior): sai da comparacao, dito (nota 4)
    _d_prev = str(((prev.get("summary") or {}).get("D128") or {}).get("status_code")); _d_this = str(((rec.get("summary") or {}).get("D128") or {}).get("status_code"))
    d128_excl = (_d_this != "RAN" and _d_prev == "RAN")
    if d128_excl:
        a = {k_: v_ for k_, v_ in a.items() if not k_.startswith("D128")}; b = {k_: v_ for k_, v_ in b.items() if not k_.startswith("D128")}
    keys = sorted(set(a) | set(b))
    diff = []; maxsc = 0.0; maxrel = 0.0; n_num = 0; n_nonfinite_diff = 0
    for k_ in keys:
        x_, y_ = a.get(k_, "<AUSENTE>"), b.get(k_, "<AUSENTE>")
        num = isinstance(x_, (int, float)) and isinstance(y_, (int, float)) and not isinstance(x_, bool) and not isinstance(y_, bool)
        if num:
            n_num += 1
            fx, fy = float(x_), float(y_)
            if not (math.isfinite(fx) and math.isfinite(fy)):
                if (fx != fx and fy != fy) or fx == fy:          # NaN nos dois, ou o mesmo infinito: igual
                    continue
                n_nonfinite_diff += 1
                diff.append({"field": k_, "previous": str(x_), "this_run": str(y_), "scaled": None, "rel": None}); continue
            if x_ == y_ and type(x_) is type(y_) and (not isinstance(x_, float) or x_.hex() == y_.hex()):   # (3a passada, N4) bit a bit LITERAL: tipo e bits
                continue
            sc = abs(fx - fy) / max(1.0, abs(fx), abs(fy)); rl = abs(fx - fy) / max(abs(fx), abs(fy), 1e-300)
            maxsc = max(maxsc, sc); maxrel = max(maxrel, rl)
            diff.append({"field": k_, "previous": x_, "this_run": y_, "scaled": sc, "rel": rl})
        elif x_ != y_ or type(x_) is not type(y_):   # (2a passada, N10) 1 contra True conta como diferenca
            diff.append({"field": k_, "previous": str(x_)[:200], "this_run": str(y_)[:200], "scaled": None, "rel": None})
    exact_other = all(d_["scaled"] is not None for d_ in diff)
    same_verdict = (prev.get("verdict") == rec.get("verdict"))
    ex = "__D128_EXCLUDED_NOT_RUN_THIS_RUN" if d128_excl else ""
    if not diff:
        v = "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__REPRODUCED_BIT_FOR_BIT__%d_FIELDS%s__SAME_V1_SAME_WORKER_SAME_BETA__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED" % (len(keys), ex)
    elif exact_other and maxsc <= 1e-9:
        v = ("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__REPRODUCED_WITHIN_ROUNDOFF__%d_FIELDS__%d_DIFFER_MAX_SCALED_%s%s__SAME_V1_SAME_WORKER_SAME_BETA__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED"
             % (len(keys), len(diff), _qp_tok_v385(maxsc), ex))
    else:
        v = "TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__NOT_REPRODUCED__%d_OF_%d_FIELDS_DIFFER%s__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED" % (len(diff), len(keys), ex)
    base.update({"verdict": v, "compared": True, "n_fields": len(keys), "n_numeric_fields": n_num, "n_differ": len(diff), "max_scaled_diff": maxsc,
                 "max_rel_diff_finite": maxrel, "n_nonfinite_differ": n_nonfinite_diff, "d128_excluded": d128_excl,
                 "first_differences": diff[:25], "same_pillar_verdict": same_verdict,
                 "previous": {k_: prev.get(k_) for k_ in ("sha256", "finished", "run_id", "verdict", "key")},
                 "this_run": {"result_sha256": rec.get("result_sha256"), "run_id": rec.get("run_id"), "finished": rec.get("finished"), "verdict": rec.get("verdict")}})
    return base
