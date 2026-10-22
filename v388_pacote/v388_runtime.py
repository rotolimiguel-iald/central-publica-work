# ====================== v388 (06/10/2026) -- O ACOPLAMENTO CORRE COM A ESCALA, LIMITADO INFERIORMENTE; a Fase 9 ABERTA pela funcao congelada ======================
# A cunhagem do operador de 06/10/2026 (13:27:52 e 13:48:42 UTC; verbatim em _V388_BETA_ESCALA, nos PINOS logo acima: textos EMBUTIDOS lidos por sha256 da
# memoria beta-escalar-limitado-inferiormente-06out.md, os carimbos lidos do transcrito pela igualdade do texto): alpha como indice de escala da fronteira, beta_TGL
# como a sua conjugacao; beta escalar, mas limitado inferiormente; a dicotomia (dividir pela metade sem nunca alcancar o limite). A pedra
# TGLExt/TheCouplingRunsBoundedBelow.lean (17 nomes) prova a MATEMATICA: alpha(chi) = sech(chi/2) e beta(chi) = alpha(chi) exp(1/2) estritamente decrescentes na
# profundidade; o piso no supremo de chi (o infravermelho); a ligacao a couplingOfAlpha; a soma das metades < 1 com limite 1; a Meia-Nat como ponto fixo. A
# identificacao fisica (alpha = sech de uma profundidade que cresce para o infravermelho) e' [INPUT/ONTO] do runtime; que alpha(mu) cresca com mu e' [KNOWN];
# qual mu cada rito usa e' [OPEN]. A constante da FRONTEIRA segue beta0 = alpha(0).sqrt(e) (o Teorema da Escala selado no artigo); beta(chi) e' a leitura de BULK.
# A ERRATA AO LADO de «alpha observa-se, nao se deriva»: o que se deriva e' a FORMA (alpha como indice de escala; beta como conjugacao), nao o NUMERO (lido do CODATA).
# A FASE 9 foi ABERTA em 06/10 pela funcao CONGELADA do V1 (ordem do operador via a sessao c1); hubble_ratio_opening_v388 le o RESULTADO por hash e REEXECUTA a funcao
# congelada sobre a entrada gravada: o veredito tem de ser o MESMO. [KERNEL] a pedra; [INPUT/ONTO] as leituras; [INPUT por hash] o resultado; o gate nao se move.
_CPL_STONE_V388 = "TGLExt/TheCouplingRunsBoundedBelow.lean"
_V388_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")


def _v388_sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _v388_get(o, path):
    try:
        for p in path:
            if isinstance(o, dict):
                o = o.get(p)
            elif isinstance(o, list) and isinstance(p, int) and -len(o) <= p < len(o):
                o = o[p]
            else:
                return None
        return o
    except Exception:
        return None


def beta_runs_bounded_below_v388(core):
    """O ACOPLAMENTO CORRE COM A ESCALA, LIMITADO INFERIORMENTE (v388): as 17 declaracoes da pedra verificadas pelo kernel desta rodada (trio, sem sorry); os dois
    verbatins do operador conferidos pelo sha256 (embutidos; o disco e' so informativo); beta0 = alpha(0).sqrt(e) em runtime (do alpha do core); beta(M_Z) on-shell
    (1/alpha(M_Z) a um laco do Teorema da Escala, lido do texto selado pelo gerador) e MS-bar [KNOWN] ao lado; a errata ao lado (forma x numero). Nao move o gate."""
    kf = core.get("kernel_formalization") or {}
    ok_flags = [f_ for f_ in _CPL_FLAGS_V388 if kf.get(f_) is True]
    vb = {}
    vb_ok = True
    for k_, f_ in (_V388_BETA_ESCALA.get("verbatins") or {}).items():
        got = _v388_sha(f_.get("text") or "")
        okk = got == f_.get("sha256")
        vb[k_] = {"quando_utc": f_.get("quando_utc"), "sha256": f_.get("sha256"), "embedded_ok": okk}
        vb_ok = vb_ok and okk
    disk = None
    try:
        p_ = _V388_BETA_ESCALA["memoria"]["path"]
        if os.path.exists(p_):
            disk = hashlib.sha256(open(p_, "rb").read()).hexdigest() == _V388_BETA_ESCALA["memoria"]["sha256"]
    except Exception:
        disk = None
    a0 = float(core.get("alpha") or 0.0); b_core = float(core.get("beta") or 0.0)
    b0 = a0 * math.sqrt(math.exp(1.0))
    b0_ok = a0 > 0 and b_core > 0 and abs(b0 / b_core - 1.0) < 1e-9
    inv_on = float(_V388_ALPHA_MZ["on_shell_inv"]); inv_ms = float(_V388_ALPHA_MZ["msbar_inv"])
    bmz_on = math.sqrt(math.exp(1.0)) / inv_on; bmz_ms = math.sqrt(math.exp(1.0)) / inv_ms
    floor_ok = bmz_on > b0 and bmz_ms > b0   # a direcao fixada: so sobe acima do piso
    n_all = len(_CPL_FLAGS_V388); n_ok = len(ok_flags)
    ok = (n_ok == n_all) and vb_ok and b0_ok and floor_ok
    fz = lambda x_, n_=6: ("%%.%df" % n_ % x_).replace(".", "P")
    if ok:
        verdict = ("TGL_BETA_RUNS_BOUNDED_BELOW_V388__ALPHA_IS_THE_SCALE_INDEX_OF_THE_BOUNDARY_BETA_ITS_CONJUGATION__ALPHA_SECH_CHI_OVER_2_STRICTLY_DECREASING_IN_DEPTH__"
                   "FLOOR_AT_THE_INFRARED_SUPREMUM_OF_CHI__BETA0_%s__BETA_MZ_ON_SHELL_%s_MSBAR_%s__LINKED_TO_COUPLING_OF_ALPHA__ZENO_HALVES_NEVER_REACH_THE_ONE_LIMIT_IS_THE_ONE__"
                   "HALF_NAT_IS_THE_FIXED_STEP__KERNEL_%d_OF_%d__BOUNDARY_CONSTANT_STAYS_BETA0_BULK_READING_RUNS__FORM_DERIVED_NUMBER_READ__OPERATOR_VERBATIM_EMBEDDED_BY_SHA256__"
                   "WHICH_MU_PER_RITE_OPEN__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED" % (fz(b0, 8), fz(bmz_on), fz(bmz_ms), n_ok, n_all))
    else:
        verdict = ("TGL_BETA_RUNS_BOUNDED_BELOW_V388__NOT_SEALED_THIS_RUN__KERNEL_%d_OF_%d__VERBATIM_%s__BETA0_%s__GATE_UNTOUCHED"
                   % (n_ok, n_all, "OK" if vb_ok else "FAILED", "OK" if b0_ok else "MISMATCH"))
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "kernel_flags_ok": n_ok, "kernel_flags_total": n_all,
            "missing_flags": [f_ for f_ in _CPL_FLAGS_V388 if kf.get(f_) is not True], "stone": _CPL_STONE_V388,
            "verbatim": vb, "verbatim_ok": vb_ok, "memory_file": {"path": _V388_BETA_ESCALA["memoria"]["path"], "sha256": _V388_BETA_ESCALA["memoria"]["sha256"], "on_disk_matches": disk},
            "beta0": b0, "beta0_vs_core_rel": (b0 / b_core - 1.0) if b_core else None, "beta0_ok": b0_ok,
            "alpha_MZ": dict(_V388_ALPHA_MZ), "beta_MZ_on_shell": bmz_on, "beta_MZ_msbar": bmz_ms, "ratio_on_shell": bmz_on / b0 if b0 else None,
            "ratio_msbar": bmz_ms / b0 if b0 else None, "floor_direction_ok": floor_ok,
            "reading": "[INPUT/ONTO] beta0 = alpha_Thomson.sqrt(e) (alpha no limite q -> 0; NAO o alphaOfChi 0 = 1 da pedra) = a constante da FRONTEIRA (o Teorema da Escala: a fronteira de tipo III_1 "
                       "seleciona Thomson); beta(mu) = alpha(mu).sqrt(e) e' a LEITURA de bulk em cada escala, >= beta0 (o congelamento infravermelho: alpha(Q) >= alpha_Thomson [KNOWN]); qual mu cada rito usa [OPEN]; "
                       "o 1/alpha(M_Z) do Teorema da Escala e' a um laco (o rotulo on-shell nao esta na fonte)",
            "erratum_beside": _V388_ERRATA_FORMA_NUMERO,
            "patents_note": "a frase do operador sobre as patentes com beta variavel: nos arquivos da Central so' foram achados beta constante nos runners e o beta_emergent dos "
                            "prototipos ACOM v18 (razao de contagens, outro objeto) -- [DECLARADO], vinculo nao verificado (mapa seq 638)",
            "what_is_not_typed": ["a identificacao alpha_fisico = sech(chi/2) [INPUT/ONTO]", "a monotonia de alpha(mu) em mu [KNOWN, QED]", "qual mu cada rito usa [OPEN]"],
            "status": "[KERNEL] a pedra; [INPUT/ONTO] as leituras; [KNOWN] alpha(M_Z); PROVADA != CONFIRMADA", "gate_unchanged_by_design": True}


def hubble_ratio_opening_v388(core):
    """A FASE 9 ABERTA (v388): o RESULTADO da abertura (06/10, pela funcao CONGELADA do V1) lido por hash; o V1 lido por hash (spec_sha256 recomputado; a funcao
    re-hasheada); a funcao REEXECUTADA sobre a entrada gravada do primario -- o veredito tem de ser o MESMO; o contrafactual (fontes supostas por hash, NAO veredito)
    recomputado pela mesma funcao e dito ao lado. Falha de hash = AVISO visivel, nunca ok falso. Nao move o gate."""
    P = _V388_FASE9_RES
    out = {"does_not_gate_core": True, "status": "[INPUT por hash] o resultado; a funcao congelada reexecutada; os leitores [DECLARADO] ate as fontes por sha256", "errors": {}}
    read = {}
    for k_, f_ in (P.get("files") or {}).items():
        try:
            b_ = open(f_["path"], "rb").read()
            read[k_] = (hashlib.sha256(b_).hexdigest() == f_["sha256"] and len(b_) == int(f_["bytes"]), b_)
        except Exception as e_:
            read[k_] = (False, None); out["errors"][k_] = repr(e_)
    files_ok = bool(read) and all(v_[0] for v_ in read.values())
    same = spec_ok = func_ok = False; R = None; v_re = None; v_cf = None
    if files_ok:
        try:
            R = json.loads(read["resultado_json"][1].decode("utf-8")); J = json.loads(read["v1_json"][1].decode("utf-8"))
            canon = json.dumps(J["spec"], sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            spec_ok = hashlib.sha256(canon).hexdigest() == J["spec_sha256"] == P["v1_spec_sha256"] == R["V1"]["spec_sha256"]
            src_ = J["spec"]["funcao_de_veredito"]["fonte"]
            func_ok = _v388_sha(src_) == P["funcao_sha256"] == R["V1"]["funcao_sha256"]
            if spec_ok and func_ok:
                ns_ = {}
                exec(compile(src_, "<veredito_fase9_v1>", "exec"), ns_)
                r_ = dict(R["primario"]["entrada_da_funcao"]); r_["sigma_z_por_alvo"] = [tuple(x_) for x_ in r_["sigma_z_por_alvo"]]
                v_re = ns_["veredito_fase9_v1"](r_)
                same = v_re == R["veredito"] == R["primario"]["veredito"]
                rc_ = dict(r_); rc_["n_alvos_declarados"] = 0
                v_cf = ns_["veredito_fase9_v1"](rc_)
        except Exception as e_:
            out["errors"]["reexecucao"] = repr(e_)
    ok = files_ok and spec_ok and func_ok and same
    st = _v388_get(R, ["primario", "estatisticas"]) or {}; ent = _v388_get(R, ["primario", "entrada_da_funcao"]) or {}
    lnb = st.get("lnB") or {}
    fz = lambda x_: ("M" if x_ < 0 else "P") + ("%.2f" % abs(x_)).replace(".", "P") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "NA"
    if ok:
        seg = "INCONCLUSIVE_SYSTEMATICS_READERS_DECLARED_UNTIL_SOURCES_BY_SHA256" if "INCONCLUSIVE_SYSTEMATICS" in str(v_re) else str(v_re).split("__")[1]
        verdict = ("TGL_HUBBLE_RATIO_OPENING_V388__RESULT_READ_BY_HASH_%s__FROZEN_FUNCTION_RE_EXECUTED_SAME_VERDICT__%s__Z_DELTA_%s__Z_DISC_%s__LNB_LCDM_%s_BETA_FREE_%s_SHIFT_%s_FREE_BG_%s__"
                   "COUNTERFACTUAL_WITH_SOURCES_%s__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
                   % (str(P["files"]["resultado_json"]["sha256"])[:16], seg, fz(ent.get("z_delta")), fz(ent.get("z_disc")), fz(lnb.get("TGL_vs_LCDM")), fz(lnb.get("TGL_vs_beta_livre")),
                      fz(lnb.get("TGL_vs_shift_cefeidas")), fz(lnb.get("TGL_vs_fundo_livre")),
                      "NOT_DISCRIMINATED_FROM_LCDM_AT_5SIGMA" if "NOT_DISCRIMINATED_FROM_LCDM" in str(v_cf) else str(v_cf).split("__")[1] if v_cf else "NA"))
    else:
        reason = "FILES_MISMATCH" if not files_ok else "SPEC_MISMATCH" if not spec_ok else "FUNCTION_MISMATCH" if not func_ok else "VERDICT_NOT_REPRODUCED"
        verdict = "TGL_HUBBLE_RATIO_OPENING_V388__NOT_READ__%s__GATE_UNTOUCHED" % reason
    if _V388_GUARDA.search(verdict):
        verdict = "TGL_HUBBLE_RATIO_OPENING_V388__GUARD_HIT__GATE_UNTOUCHED"; ok = False
    # AO LADO (afericao adversarial de 06/10): o recalculo da quadratura (n = 25 nao convergiu) e o z_disc nas duas formas -- arquivo proprio por sha256, o RESULTADO congelado intocado
    rec = None
    try:
        _rb = open(_V388_FASE9_RECALCULO["path"], "rb").read()
        if hashlib.sha256(_rb).hexdigest() == _V388_FASE9_RECALCULO["sha256"]:
            rec = json.loads(_rb.decode("utf-8"))
    except Exception as e_:
        out["errors"]["recalculo_ao_lado"] = repr(e_)
    out["recalculo_ao_lado"] = ({"lnB_TGL_vs_beta_livre_convergido": rec.get("convergido_n200"), "erro_quadratura_n25_n35": rec.get("erro_n25_n35"),
                                 "z_disc_forma_quadratica": rec.get("z_disc_forma_quadratica_runner"), "z_disc_com_logdet": rec.get("z_disc_com_logdet"), "sha256": _V388_FASE9_RECALCULO["sha256"],
                                 "estatuto": "[REAL — ao lado; NAO e' veredito; o resultado congelado fica]"} if rec else None)
    out.update({"verdict": verdict, "all_verified": ok, "files_ok": files_ok, "spec_ok": spec_ok, "funcao_ok": func_ok, "same_verdict": same,
                "verdict_of_the_frozen_function": v_re, "counterfactual_with_sources_NOT_a_verdict": v_cf,
                "numbers": {"H0_bg": st.get("H0_bg"), "H0_local_previsto": st.get("H0_local_previsto"), "media_GLS_locais": st.get("media_GLS_locais"),
                            "sigma_GLS_locais": st.get("sigma_GLS_locais"), "beta_hat": st.get("beta_hat"), "sigma_beta": st.get("sigma_beta"), "z_delta": ent.get("z_delta"),
                            "z_disc": ent.get("z_disc"), "lnB": lnb, "lnB_erro_quadratura": st.get("lnB_erro_quadratura"), "dispersao_por_gl": ent.get("dispersao_por_gl"),
                            "z_por_leitor": {k_: {"z_vs_TGL": v_.get("z_vs_TGL"), "z_vs_LCDM": v_.get("z_vs_LCDM")} for k_, v_ in (_v388_get(R, ["primario", "z_por_leitor"]) or {}).items()},
                            "fundo_livre": _v388_get(R, ["fundo_livre"])},
                "files": {k_: v_["sha256"] for k_, v_ in (P.get("files") or {}).items()}, "runner_sha256": P.get("runner_sha256"),
                "reading": "o veredito e' o que a funcao congelada devolveu; com os leitores [DECLARADO] a regra 1 devolve INCONCLUSIVE_SYSTEMATICS; o contrafactual (SE as fontes por hash "
                           "confirmassem os valores declarados) NAO e' veredito: sob este V1, z_disc < 5 nao discrimina; ao lado: o executor marginaliza o fundo (o V1 dizia perfilada) e usa -2lnL com log-det para "
                           "z_delta (o V1: Delta chi2 = 1) -- diferenca medida desprezivel; o fundo-livre (r_d livre so no BAO) e' alternativa fraca, nao analise de fisica precoce; NOT_FALSIFIED nunca e' confirmacao"})
    return out
