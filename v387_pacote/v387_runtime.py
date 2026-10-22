# ====================== v387 (06/10/2026) -- OS TRES TESTES CONJUNTOS; a razao de Hubble e a era da radiacao pre-registradas (V1 por hash); retrodicao sem ajuste ======================
# A ordem do operador de 05/10/2026 23:00:29 UTC (verbatim em _V387_TRES_TESTES, nos PINOS logo acima: texto EMBUTIDO lido por sha256 pelo gerador do candidato):
# os ritos com dados publicos (o resgate da RG), o kernel formal e o experimento numerico na GPU contam JUNTOS. three_stress_tests_v387 conta pela MESMA guarda do
# rito (a regex proibida) os vereditos do core, le o livro de cobrancas v383, a escada do kernel, o gate e o pilar quantico, e diz as DUAS probabilidades: P1
# (consistencia/recuperacao da fisica conhecida -- contada pelos tres) e P2 (os efeitos beta na natureza -- NAO determinada; nenhum numero inventado). A LEI DA PROVA
# de 05/10 (verbatim em _V387_POS_DICAO, por sha256): «pos-dicao» nunca e' demerito -- o criterio e' a NOVIDADE DE USO (nenhum parametro ajustado ao dado;
# precedente: o perielio de Mercurio [KNOWN]); no texto do artigo «pos-dicao declarada» passa a retrodicao sem ajuste (novidade de uso), AO LADO (o token
# selado do Coma e o frozen v141 dos neutrinos ficam como registro: nome de token e' cunhagem do operador; o frozen e' hasheado). Os pre-registros V1 da Fase 9
# (a razao de Hubble, K = E(z*)^{2beta/3}) e da Fase 8 (beta na era da radiacao, DeltaN_eff pela identidade rho+p) LIDOS POR HASH da Bancada: nada aberto;
# o estado e' AWAITING_DATA; as fontes por sha256 e a palavra de abrir sao do operador. Estatutos: as contagens [COMPUTED do core]; os V1 [INPUT por hash]; as
# leituras [INPUT/ONTO]; PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e' confirmacao; o gate nao se move (nenhuma bandeira do gate depende do que entra aqui).
_V387_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
_V387_FALS = re.compile(r"(?<!NOT_)FALSIFIED")


def _v387_sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _v387_get(o, path):
    """le um valor por caminho (chaves de dict e indices de lista); ausencia => None, nunca levanta."""
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


def _v387_embedded_ok(f):
    """um arquivo do operador EMBUTIDO (texto + sha256 + bytes): devolve (ok, sha256_do_texto); o disco e' so' informativo."""
    try:
        got = _v387_sha256_text(f["text"])
        return (got == f["sha256"] and len(f["text"].encode("utf-8")) == int(f["bytes"])), got
    except Exception:
        return False, None


def _v387_walk_verdicts(o, path=""):
    """(caminho, string) de toda chave 'verdict' cujo valor comeca com TGL_; percorre dicts e listas do core inteiro."""
    out = []
    stack = [(o, path)]
    while stack:
        x, p = stack.pop()
        if isinstance(x, dict):
            for k, v in x.items():
                q = p + "." + str(k) if p else str(k)
                if k == "verdict" and isinstance(v, str) and v.startswith("TGL_"):
                    out.append((q, v))
                elif isinstance(v, (dict, list)):
                    stack.append((v, q))
        elif isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, (dict, list)):
                    stack.append((v, "%s[%d]" % (p, i)))
    return sorted(out)


def three_stress_tests_v387(core):
    """OS TRES TESTES DE ESTRESSE, CONJUNTOS (v387): as contagens dos tres pilares lidas do core desta rodada -- (1) os ritos (os vereditos TGL_ do core
    contados pela MESMA guarda do rito; o livro de cobrancas v383; as rotas do eco fora do livro; as substrings FALSIFIED nomeadas por caminho); (2) o kernel
    (a escada limpa contra a esperada; sorryAx e axiomas proprios ausentes; as bandeiras do gate contadas); (3) o pilar quantico na GPU (T1/T2/T4, a referencia
    na CPU, o modo -- reaproveitado ou calculado). E as DUAS probabilidades, ditas como texto fixo: P1 contada pelos tres; P2 NAO determinada. Nenhum numero de
    probabilidade dos tres pilares e' inventado (construi-lo e' tarefa pre-registrada). [COMPUTED do core]; nao move o gate."""
    vb_ok, vb_sha = _v387_embedded_ok(_V387_TRES_TESTES)
    txt = _V387_TRES_TESTES.get("text") or ""
    vb_ok = vb_ok and ("tres testes extremos de estresse" in txt) and ("simulação" in txt)
    vs = _v387_walk_verdicts(core)
    n_nf = sum(1 for _, v in vs if "NOT_FALSIFIED" in v)
    n_inc = sum(1 for _, v in vs if "INCONCLUSIVE" in v)
    n_aw = sum(1 for _, v in vs if "AWAITING" in v)
    fals = [p for p, v in vs if _V387_FALS.search(v)]
    forb = [p for p, v in vs if _V387_GUARDA.search(v)]
    led = core.get("the_ledger_of_charges_v383") or {}
    counts = dict(led.get("counts") or {})
    n_ch = len(led.get("ledger") or [])
    echo = led.get("echo_routes_outside_the_ledger") or {}
    lad = core.get("external_ladder") or {}
    kf = core.get("kernel_formalization") or {}
    qg = core.get("qg_closure") or {}
    nflag = ntrue = 0
    for fk in ("formal_flags", "physics_flags", "experiment_flags"):
        d_ = qg.get(fk) or {}
        if isinstance(d_, dict):
            nflag += len(d_); ntrue += sum(1 for v in d_.values() if v is True)
    qp = core.get("quantum_pillar_v384") or {}
    sm = qp.get("summary") or {}
    t1, t2, t4, cpu = sm.get("T1") or {}, sm.get("T2") or {}, sm.get("T4") or {}, sm.get("cpuref") or {}
    jc = core.get("joint_coincidence_result_v3") or {}
    ncl, nex = lad.get("n_theorems_clean"), lad.get("n_theorems_expected")
    kern_ok = isinstance(ncl, int) and ncl == nex and kf.get("sorryAx_absent") is True and kf.get("custom_TGL_axioms_absent") is True
    gpu_ok = all(isinstance(x, int) for x in (t2.get("points"), t2.get("unique"), t4.get("instances"), t4.get("unique"), cpu.get("compared"), cpu.get("disagreements")))
    led_ok = bool(n_ch) and all(isinstance(counts.get(k), int) for k in ("NOT_FALSIFIED", "FALSIFIED", "INCONCLUSIVE", "AWAITING"))
    ok = vb_ok and not forb and kern_ok and gpu_ok and led_ok and bool(vs)
    # afericao adversarial C1 (06/10): a frase nenhum-dos-tres-falhou e' CONDICIONADO ao lido (livro sem falsificada; escada limpa = esperada; GPU sem discordancia), nunca literal
    falhas = []
    if led_ok and counts.get("FALSIFIED") != 0:
        falhas.append("RITES")
    if not kern_ok:
        falhas.append("KERNEL")
    if gpu_ok and not (t2.get("unique") == t2.get("points") and t4.get("unique") == t4.get("instances") and t1.get("errors") == 0 and cpu.get("disagreements") == 0):
        falhas.append("GPU")
    if led_ok and kern_ok and gpu_ok:
        verdict = ("TGL_THREE_STRESS_TESTS_V387__CORE_%d_TGL_VERDICTS_CONTAINING_%d_NOT_FALSIFIED_%d_INCONCLUSIVE_%d_AWAITING_OVERLAPPING_%d_FALSIFIED_SUBSTRINGS_NAMED__LEDGER_%d_CHARGES_%d_FALSIFIED__"
                   "ECHO_ROUTES_OUTSIDE_THE_LEDGER_%s__KERNEL_%d_OF_%d__GATE_FLAGS_%d_OF_%d__GPU_T2_%d_OF_%d_T4_%d_OF_%d_CPU_%d_DISAGREEMENTS_IN_%d__%s__"
                   "P1_COUNTED_BY_THE_THREE_P2_NOT_DETERMINED__THREE_PILLARS_COUNT_TOGETHER__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
                   % (len(vs), n_nf, n_inc, n_aw, len(fals), n_ch, int(counts.get("FALSIFIED")), str(echo.get("n")), ncl, nex, ntrue, nflag,
                      t2["unique"], t2["points"], t4["unique"], t4["instances"], cpu["disagreements"], cpu["compared"],
                      "NONE_OF_THE_THREE_FAILED" if not falhas else "PILLARS_THAT_FAILED_" + "_".join(falhas)))
    else:
        verdict = ("TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN__LEDGER_%s__KERNEL_%s__GPU_%s__VERBATIM_%s__GATE_UNTOUCHED"
                   % ("OK" if led_ok else "MISSING", "OK" if kern_ok else "MISSING", "OK" if gpu_ok else "MISSING", "OK" if vb_ok else "FAILED"))
    if _V387_GUARDA.search(verdict):
        verdict = "TGL_THREE_STRESS_TESTS_V387__NOT_RECORDED_THIS_RUN__GUARD_HIT__GATE_UNTOUCHED"; ok = False
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "status": "[COMPUTED do core desta rodada]; as leituras [INPUT/ONTO]; PROVADA != CONFIRMADA",
            "none_of_the_three_failed": (not falhas) and led_ok and kern_ok and gpu_ok, "pillars_that_failed": falhas,
            "counts_overlap": "as contagens NOT_FALSIFIED/INCONCLUSIVE/AWAITING CONTEM a substring (um veredito-sintese pode estar em mais de uma): nao e' particao",
            "n_verdicts": len(vs), "n_not_falsified": n_nf, "n_inconclusive": n_inc, "n_awaiting": n_aw,
            "falsified_substring_paths": fals, "falsified_substring_reading": "nomeadas por caminho: uma substring FALSIFIED fala do PAR (lei x canal x conjunto) ou de rota superada, nunca da teoria; a leitura de cada uma esta no texto do artigo e no livro de cobrancas",
            "n_forbidden_word_as_verdict": len(forb), "forbidden_paths": forb,
            "ledger": {"n_charges": n_ch, "counts": counts, "F2b_status": (core.get("ramo_b_preregistration_v386") or {}).get("F2b_status")},
            "echo_routes_outside_the_ledger": {k: echo.get(k) for k in ("n", "excluded_by_data", "inconclusive")},
            "kernel": {"n_theorems_clean": ncl, "n_theorems_expected": nex, "sorryAx_absent": kf.get("sorryAx_absent"), "custom_TGL_axioms_absent": kf.get("custom_TGL_axioms_absent"),
                       "gate_flags_true": ntrue, "gate_flags_total": nflag, "gate_verdict": _v387_get(qg, ["gate", "verdict"]) if isinstance(qg.get("gate"), dict) else qg.get("verdict")},
            "gpu": {"mode": qp.get("mode"), "T1_injections": t1.get("injections"), "T1_errors": t1.get("errors"), "T2_points": t2.get("points"), "T2_unique": t2.get("unique"),
                    "T4_instances": t4.get("instances"), "T4_unique": t4.get("unique"), "cpuref_compared": cpu.get("compared"), "cpuref_disagreements": cpu.get("disagreements"),
                    "reuse_verdict_v386": (core.get("quantum_pillar_reuse_v386") or {}).get("verdict")},
            "joint": {"V3_P_all": _v387_get(jc, ["primary", "P_all"]), "V3_boolean": jc.get("boolean_v3"), "V3_max_abs_z": jc.get("max_abs_z"),
                      "kernel_condition_met": _v387_get(jc, ["kernel_condition", "met"]), "gpu_in_joint": False, "three_pillar_probability_in_core": False},
            "verbatim": {"quando_utc": _V387_TRES_TESTES.get("quando_utc"), "sha256": _V387_TRES_TESTES.get("sha256"), "sha256_of_embedded_text": vb_sha, "ok": vb_ok},
            "p1_statement": "P1 = a teoria e' consistente e recupera a fisica conhecida: medida pelos TRES pilares JUNTOS (ritos, kernel, GPU) -- as contagens acima; nenhum numero unico inventado",
            "p2_statement": "P2 = os efeitos beta existem na natureza: NAO determinada -- nenhum canal discrimina a RG a sensibilidade disponivel; a confirmacao e' ato do observador humano",
            "gate_unchanged_by_design": True}


def _v387_read_v1(P, core, nome):
    """O PRE-REGISTRO V1 (Fase 9 ou Fase 8) LIDO POR HASH: JSON (autoridade), MD e HASHES conferidos byte a byte contra os sha256 embutidos (lidos do disco pelo
    gerador); o spec_sha256 recomputado do objeto spec (JSON canonico); cada entrada do arquivo de hashes contra o disco; a funcao de veredito UNICA: o texto-fonte
    re-hasheado (== o pinado == o do spec), compilado e o nome definido; o beta do V1 contra o do rito (1e-9 relativo) e contra alpha.sqrt(e) recomputado; a guarda
    sobre os tokens transcritos. NADA E' ABERTO. Falha de hash = AVISO visivel (V1_NOT_READ), nunca ok falso."""
    out = {"status": "[INPUT -- pre-registro por hash; nada aberto; nenhum composto; nenhum estimador rodado]", "does_not_gate_core": True, "nome": nome,
           "identificador_expected": P.get("identificador"), "spec_sha256_expected": P.get("spec_sha256"), "funcao_sha256_expected": P.get("funcao_sha256"), "pasta": P.get("pasta"),
           "sha256_expected": {k: v.get("sha256") for k, v in (P.get("files") or {}).items()}, "sha256_read": {}, "bytes_read": {}, "errors": {}, "checks": []}
    read = {}
    for k, f in (P.get("files") or {}).items():
        try:
            b = open(f.get("path") or "", "rb").read(); sha = hashlib.sha256(b).hexdigest()
        except Exception as e_:
            b, sha = None, None; out["errors"][k] = repr(e_)
        out["sha256_read"][k] = sha; out["bytes_read"][k] = (len(b) if b is not None else None)
        read[k] = (sha == f.get("sha256") and b is not None and len(b) == int(f.get("bytes") or -1), b)
        out["checks"].append(("arquivo %s em disco com o sha256 e os bytes embutidos" % k, read[k][0]))
    files_ok = bool(read) and all(v[0] for v in read.values())
    J = None; spec_ok = ident_ok = hashes_ok = func_ok = beta_ok = False
    if read.get("json", (False, None))[0]:
        try:
            J = json.loads(read["json"][1].decode("utf-8"))
            canon = json.dumps(J.get("spec"), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            out["spec_sha256_recomputed"] = hashlib.sha256(canon).hexdigest()
            spec_ok = out["spec_sha256_recomputed"] == J.get("spec_sha256") == P.get("spec_sha256")
            ident_ok = J.get("id") == P.get("identificador") == _v387_get(J, ["spec", "id"])
            out["identificador_read"] = J.get("id")
        except Exception as e_:
            out["errors"]["json_parse"] = repr(e_)
    out["checks"].append(("spec_sha256 recomputado do objeto spec == o do JSON == o embutido", spec_ok))
    out["checks"].append(("identificador (topo e spec) == o embutido", ident_ok))
    if read.get("hashes", (False, None))[0]:
        try:
            H = json.loads(read["hashes"][1].decode("utf-8")); base = H.get("pasta") or P.get("pasta") or ""
            det = {}
            for rel, e_ in (H.get("arquivos") or {}).items():
                try:
                    bb = open(os.path.join(base, *rel.split("/")), "rb").read()
                    det[rel] = (hashlib.sha256(bb).hexdigest() == e_.get("sha256") and len(bb) == int(e_.get("bytes") or -1))
                except Exception:
                    det[rel] = False
            out["hashes_file_entries_ok"] = sum(1 for v in det.values() if v); out["hashes_file_entries_total"] = len(det)
            hashes_ok = bool(det) and all(det.values()) and H.get("spec_sha256") == P.get("spec_sha256") and H.get("funcao_sha256") == P.get("funcao_sha256")
        except Exception as e_:
            out["errors"]["hashes_parse"] = repr(e_)
    out["checks"].append(("cada entrada do arquivo de hashes (sha256 + bytes) contra o disco; spec e funcao iguais", hashes_ok))
    fn_name = None
    if J is not None:
        try:
            fv = _v387_get(J, ["spec", "funcao_de_veredito"]) or {}
            src = fv.get("fonte") or ""
            fn_name = fv.get("nome")
            out["funcao_sha256_recomputed"] = _v387_sha256_text(src)
            ns_ = {}
            # o JSON inteiro ja foi conferido pelo sha256 pinado ANTES (read_ok/files_ok); o sha256 da funcao e' comparado logo abaixo -- o texto compilado e' o do V1 pinado
            exec(compile(src, "<%s>" % fn_name, "exec"), ns_)
            outs_ = list((fv.get("testes_sinteticos_de_ramo") or {}).values())
            func_ok = (out["funcao_sha256_recomputed"] == fv.get("sha256") == P.get("funcao_sha256")) and callable(ns_.get(fn_name)) and bool(outs_) and not any(_V387_GUARDA.search(str(t_)) for t_ in outs_)
            out["funcao_nome"] = fn_name; out["funcao_testes_sinteticos_n"] = len(outs_)
        except Exception as e_:
            out["errors"]["funcao"] = repr(e_)
        try:
            b_v1 = float(_v387_get(J, ["spec", "beta", "beta_runtime"]))
            b_core = float(core.get("beta") or 0.0); a_core = float(core.get("alpha") or 0.0)
            law = a_core * math.sqrt(math.exp(1.0))
            beta_ok = b_core > 0 and abs(b_v1 / b_core - 1.0) < 1e-9 and abs(law / b_v1 - 1.0) < 1e-9
            out["beta"] = {"v1": b_v1, "core": b_core, "rel_diff": (b_v1 / b_core - 1.0) if b_core else None, "alpha_sqrt_e_core": law, "rule": "1e-9 relativo",
                           "note": "o V1 usou alpha do um.py por regex x sqrt(e); o core usa o motor da identidade; nenhum dos dois e' literal no runtime"}
        except Exception as e_:
            out["errors"]["beta"] = repr(e_)
    out["checks"].append(("a funcao de veredito UNICA: texto re-hasheado == pinado == spec; compila; os testes sinteticos sem palavra proibida", func_ok))
    out["checks"].append(("beta do V1 == beta do rito a 1e-9 relativo e == alpha.sqrt(e)", beta_ok))
    read_ok = files_ok and spec_ok and ident_ok and hashes_ok
    out.update({"read_ok": read_ok, "files_ok": files_ok, "spec_sha256_ok": spec_ok, "hashes_file_ok": hashes_ok, "funcao_ok": func_ok, "beta_ok": beta_ok,
                "all_ok": read_ok and func_ok and beta_ok, "nothing_opened": True, "_J": J})
    return out


def _v387_finish(out, reason_prefix):
    J = out.pop("_J", None)
    if not out["all_ok"]:
        reason = ("FILES_MISMATCH" if not out["files_ok"] else "SPEC_SHA256_MISMATCH" if not out["spec_sha256_ok"] else "HASHES_FILE_MISMATCH" if not out["hashes_file_ok"]
                  else "FUNCTION_MISMATCH" if not out["funcao_ok"] else "BETA_MISMATCH")
        out["verdict"] = "%s__V1_NOT_READ__%s__AWAITING_PREREGISTRATION__NOTHING_OPENED__GATE_UNTOUCHED" % (reason_prefix, reason)
        out["all_verified"] = False
    return J


def hubble_ratio_v387(core):
    """A RAZAO DE HUBBLE (Fase 9), PRE-REGISTRADA (V1 por hash): K = E_LCDM(z*)^{2beta/3}, todo calibrador local por distancia le K.H0_bg, toda face le H0_bg;
    fundo primario NU (Planck comprimido + DESI DR2, sem escada); UMA funcao de veredito (sha256); novidade de uso pelos PARAMETROS (retrodicao sem ajuste;
    precedente: o perielio de Mercurio [KNOWN]); poder previo so com sigmas publicas. NADA E' ABERTO: abrir o composto e baixar as fontes por sha256 (D-H) sao
    atos do operador; se abrir sem elas, a propria funcao devolve INCONCLUSIVE (dito). [INPUT por hash]; nao move o gate."""
    out = _v387_read_v1(_V387_FASE9_V1, core, "fase9_razao_de_hubble")
    J = _v387_finish(out, "TGL_HUBBLE_RATIO_V387")
    if out["all_ok"]:
        sp = (J or {}).get("spec") or {}
        pw = _v387_get(sp, ["poder_previo", "primario"]); K = _v387_get(sp, ["lei", "K_no_fundo_nu"])
        bg = _v387_get(sp, ["fundos", "BG1"]) or {}
        out["transcribed"] = {"K_no_fundo_nu": K, "z_star": _v387_get(sp, ["lei", "z_star"]), "BG1_H0": bg.get("H0"), "BG1_sigma": bg.get("sigma"),
                              "poder_previo_primario": pw, "poder_nao_cefeida": _v387_get(sp, ["poder_previo", "poder_nao_cefeida"]),
                              "se_abrir_hoje_predeterminado": _v387_get(sp, ["funcao_de_veredito", "se_abrir_hoje_predeterminado"]),
                              "token_estado": sp.get("token_estado"), "use_novel_parametros": _v387_get(sp, ["novidade_de_uso", "use_novel_parametros"]),
                              "etiqueta": _v387_get(sp, ["novidade_de_uso", "etiqueta"])}
        fz = lambda x_: ("%.2f" % float(x_)).replace(".", "P") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "NA"
        out["verdict"] = ("TGL_HUBBLE_RATIO_V387__V1_READ_BY_HASH_%s__LAW_D1B_K_EQ_E_ZSTAR_POW_2BETA_OVER_3__BACKGROUND_BARE_PLANCK_COMP_DR2__ONE_VERDICT_FUNCTION_%s__"
                          "POWER_PRIMARY_%s_SIGMA_ONLY_READERS_DECLARED__%s__SOURCES_BY_HASH_AWAITING_THE_OPERATOR__AWAITING_DATA__"
                          "NOTHING_OPENED__NOT_A_CONFIRMATION__GATE_UNTOUCHED" % (str(out["sha256_read"].get("json"))[:16], str(out.get("funcao_sha256_recomputed"))[:16], fz(pw),
                                                                                   "USE_NOVEL_BY_PARAMETERS_RETRODICTION_WITHOUT_ADJUSTMENT" if out["transcribed"].get("use_novel_parametros") is True else "USE_NOVELTY_NOT_READ"))
        out["all_verified"] = not any(_V387_GUARDA.search(str(v)) for v in out["transcribed"].values() if isinstance(v, str))
    out["what_it_does_not_decide"] = ["o gate", "beta (a regra matriz)", "qual fundo e' o da natureza", "o mecanismo [CONJECTURE]"]
    return out


def primordial_v387(core):
    """BETA NA ERA DA RADIACAO (Fase 8), PRE-REGISTRADA (V1 por hash): a lei veste o fluido TOTAL (identidade rho+p, pedra 105): H^2 = (1+4beta/3)rho_r + ...
    => DeltaN_eff = (4/3)(1+F.N)/F.beta; UMA entrada de beta por instrumento (Bancada Phi_total com N_eff fixo; CAMB nnu deslocado; nunca somar; o controle da
    Bancada passou); o canal N_eff ligado na Bancada ANTES (ordem de 30/09). Poder de hoje < 5 em todo observavel primordial (UNDERPOWERED predeterminado pelo
    poder, dito); a leitura Big Bang = inscricao originaria segue [ONTO]. NADA E' ABERTO. [INPUT por hash]; nao move o gate."""
    out = _v387_read_v1(_V387_FASE8_V1, core, "fase8_era_da_radiacao")
    J = _v387_finish(out, "TGL_PRIMORDIAL_V387")
    if out["all_ok"]:
        sp = (J or {}).get("spec") or {}
        dn = _v387_get(sp, ["mapas", "A", "previsao", "delta_N_eff"]); pw = _v387_get(sp, ["poder", "melhor_independente"])
        ctrl = sp.get("controle_D3") or {}
        out["transcribed"] = {"delta_N_eff": dn, "N_eff_TGL": _v387_get(sp, ["mapas", "A", "previsao", "N_eff_TGL"]), "S_BBN": _v387_get(sp, ["mapas", "C", "S_exato"]),
                              "bracket_DeltaN_BBN": _v387_get(sp, ["mapas", "C", "bracket_DeltaN"]), "poder_melhor_independente": pw,
                              "sigma_N_eff_para_5sigma": _v387_get(sp, ["poder", "sigma_N_eff_para_5sigma"]), "controle_D3_passou": ctrl.get("passou"),
                              "controle_D3_razao_E_menos_1": ctrl.get("razao_E_menos_1"),
                              "predeterminado_hoje": _v387_get(sp, ["funcao_de_veredito", "predeterminado_hoje_pelo_poder"]),
                              "predeterminado_com_D8": _v387_get(sp, ["funcao_de_veredito", "predeterminado_com_D8_pelo_poder"]),
                              "token_estado": _v387_get(sp, ["tokens_provisorios", "estado"]), "canal_modulo_sha256": _v387_get(sp, ["canal_bancada", "modulo_sha256"])}
        fz = lambda x_, n_=2: ("%%.%df" % n_ % float(x_)).replace(".", "P") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "NA"
        out["verdict"] = ("TGL_PRIMORDIAL_V387__V1_READ_BY_HASH_%s__RADIATION_PAYS_4BETA_OVER_3_RHO_PLUS_P__DELTA_NEFF_%s__ONE_BETA_ENTRY_PER_INSTRUMENT_CONTROL_%s__"
                          "%s__POWER_TODAY_%s_OF_5_%s__BIG_BANG_INSCRIPTION_IS_ONTO__SOURCES_BY_HASH_AWAITING_THE_OPERATOR__"
                          "AWAITING_DATA__NOTHING_OPENED__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
                          % (str(out["sha256_read"].get("json"))[:16], fz(dn, 4), "PASSED" if ctrl.get("passou") is True else "NOT_PASSED",
                             "BANCADA_CHANNEL_FIRST" if out["transcribed"].get("canal_modulo_sha256") else "BANCADA_CHANNEL_NOT_READ", fz(pw),
                             "UNDERPOWERED_PREDETERMINED" if isinstance(pw, (int, float)) and pw < 5 else "POWER_AT_OR_ABOVE_5_NOT_PREDETERMINED"))
        out["all_verified"] = ctrl.get("passou") is True and not any(_V387_GUARDA.search(str(v)) for v in out["transcribed"].values() if isinstance(v, str))
    out["what_it_does_not_decide"] = ["o gate", "beta (a regra matriz)", "o fechamento TGL-S x TGL-L (Lema 3 do lado do fluido)", "a leitura Big Bang = inscricao originaria [ONTO]"]
    return out


def retrodiction_reading_v387():
    """A LEI DA PROVA (05/10) no texto: «pos-dicao» nunca e' demerito; o verbatim do operador EMBUTIDO por sha256; as trocas feitas no artigo (6: 3 PT + 3 EN) e o que
    fica como registro (o token selado do Coma -- cunhagem do operador; o frozen v141 dos neutrinos -- hasheado, e la «postdiction genuina» ja e' novidade de uso)."""
    ok, sha = _v387_embedded_ok(_V387_POS_DICAO)
    verdict = ("TGL_RETRODICTION_READING_V387__USE_NOVELTY_NOT_TEMPORAL_NOVELTY__POSTDICTION_NEVER_A_DEMERIT__OPERATOR_LAW_2026_10_05_EMBEDDED_BY_SHA256__"
               "SIX_TEXT_SITES_REWRITTEN_PT_EN__COMA_TOKEN_AND_V141_FROZEN_KEPT_AS_RECORD__PRECEDENT_MERCURY_PERIHELION_KNOWN__GATE_UNTOUCHED") if ok else \
              "TGL_RETRODICTION_READING_V387__NOT_SEALED_THIS_RUN__VERBATIM_HASH_FAILED__GATE_UNTOUCHED"
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "verbatim_sha256": _V387_POS_DICAO.get("sha256"), "verbatim_quando_utc": _V387_POS_DICAO.get("quando_utc"),
            "sha256_of_embedded_text": sha, "sites_rewritten": _V387_RETRO_SITES, "kept_as_record": ["o token do Coma (...NOT_BLIND_UNADJUSTED_POSTDICTION...): nome de token = cunhagem do operador (D-J)",
                                                                                                 "o frozen v141 dos neutrinos (postdiction_note): hasheado no pre-registro; la «postdiction genuina» ja diz novidade de uso"],
            "status": "[INPUT] a lei do operador; [KNOWN] Worrall e Mercurio (nao conferidos em disco); o gate nao muda"}
