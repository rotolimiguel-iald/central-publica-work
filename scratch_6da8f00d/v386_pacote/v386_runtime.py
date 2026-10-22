# ====================== v386 (05/10/2026) -- O VERBO SELECIONA; o ramo B reaberto por pre-registro (V1 por hash); a errata AO LADO de R6 ======================
# As cunhagens do operador de 05/10/2026 (verbatim em _V386_OPERATOR_VERBATIM, nos PINOS logo acima: textos EMBUTIDOS de arquivos lidos por sha256 pelo gerador
# do candidato -- o VERBO 16:53:25 UTC, a DECISAO do ramo B 17:11:36 UTC, as RESPOSTAS 18:29:37 UTC): «Verbo=seleção da ação»; «O Verbo seleciona: nome, tempo
# e verdade»; «o Nome não é ontologia, o nome é "posto", é justamente "o posto", o local, como já falamos, onde a inscrição pode habitar com objeto distinto
# definido»; «são as duas faces do mesmo o objeto, porque o custo é jussivo à verdade»; «o tempo como fluxo da relatividade modular não pode ser dual, ele
# precisa ser lido duas vezes»; «a luz como setor escuro, condensado psionico, precede a gravidade, mas eles são indissociáveis»; «eu não havia proibido o ramo
# B, acontece que naquela ocasião ainda não tínhamos todos os críterios para prosseguir»; «o resto vc consegue responder tudo agroa» (delegacao: o padrao da
# gerencia vale e e' dito como «decidido por delegacao»). A pedra TGLExt/TheVerbSelectsTheAction.lean (93 declaracoes) prova o que e' MATEMATICA nessas frases
# (o Nome e' o posto: a projecao de posto 1; select = o Verbo em ato; verb reservado ao gesto V_t ja no kernel; a leitura e' um peso; a ordem importa; a triade
# su(2) escalada por c -- c = beta_TGL e' [INPUT], beta nunca literal; os postos por eixo nao comutam; verdade e custo duas faces; o tempo lido duas vezes;
# luz e gravidade indissociaveis), e a FIACAO angular (17 termos compilados sem auditoria ate a v385) entra na escada. O ramo B do ringdown: OUTRA LEI
# (tau* = k.G.M_f/c^3, k = 2pi/kappa_hat(chi_f)), canal proprio F2b, PRE-REGISTRADO POR HASH na Bancada (V1), NADA ABERTO; a errata AO LADO de R6
# (ENCERRADO -> REABERTO POR PRE-REGISTRO); o livro v383 fica INTACTO como registro. O PILAR QUANTICO nao e' objeto desta versao: e' REAPROVEITADO da rodada
# selada v385 pela chave do cache (sha256 conferido; _QP_REUSE_V386) -- a reprodutibilidade medida na v385 fica no selo da v385; nesta rodada nao ha
# comparacao nova, e isso e' dito. Estatutos: a pedra [KERNEL]; as leituras do operador e as da gerencia [INPUT/ONTO]; o V1 [INPUT, por hash]; o pilar
# [COMPUTED]; PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e' confirmacao; o gate nao se move (nenhuma bandeira do gate depende do que entra aqui).
_QP_REUSE_V386 = True   # v386: o pilar quantico NAO e' objeto desta versao -- reaproveita pela chave quando o cache confere (sha256), o ambiente e' o mesmo e o motor passa; senao calcula (dito)
_VERB_STONE_V386 = "TGLExt/TheVerbSelectsTheAction.lean"
_V386_GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")


def _v386_sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _v386_get(o, path):
    """le um valor por caminho (chaves de dict e indices de lista); ausencia => None, nunca levanta."""
    try:
        for p in path:
            if isinstance(o, dict):
                o = o.get(p)
            elif isinstance(o, list) and isinstance(p, int) and p < len(o):
                o = o[p]
            else:
                return None
        return o
    except Exception:
        return None


def _v386_verbatim():
    """Os verbatins do operador de 05/10: cada arquivo EMBUTIDO (texto) conferido contra o seu sha256 (lido do artefato pelo gerador); o disco, se ainda
    existir, e' INFORMATIVO (o scratchpad e' efemero). Devolve o dicionario com os textos decodificados; nunca levanta."""
    out = {"files": {}, "all_ok": True}
    for k, f in (_V386_OPERATOR_VERBATIM.get("files") or {}).items():
        try:
            got = _v386_sha256_text(f["text"])
            ok = (got == f["sha256"]) and (len(f["text"].encode("utf-8")) == int(f["bytes"]))
        except Exception as e_:
            got, ok = None, False
            out.setdefault("errors", []).append("%s: %r" % (k, e_))
        on_disk = None
        try:
            if os.path.exists(f.get("path") or ""):
                on_disk = hashlib.sha256(open(f["path"], "rb").read()).hexdigest() == f["sha256"]
        except Exception:
            on_disk = None
        out["files"][k] = {"quando_utc": f.get("quando_utc"), "sha256": f.get("sha256"), "bytes": f.get("bytes"), "sha256_of_embedded_text": got,
                           "embedded_matches_sha256": ok, "on_disk_matches": on_disk, "on_disk_note": "informativo: o scratchpad e' efemero; o que vale e' o texto embutido com o hash",
                           "errata_ao_lado": f.get("errata_ao_lado")}   # v386: o RESPOSTAS json ganhou a errata [sic] («tudo agroa») depois do congelamento do V1 -- dito, com o sha256 que o V1 registrou
        out["all_ok"] = out["all_ok"] and ok
    try:
        dec = json.loads(_V386_OPERATOR_VERBATIM["files"]["ramo_b_decision_20261005_1711"]["text"])
        out["ramo_b_decision_verbatim"] = dec.get("verbatim"); out["ramo_b_decision_quando_utc"] = dec.get("quando")
        out["all_ok"] = out["all_ok"] and bool(dec.get("verbatim")) and dec.get("quando") == _V386_OPERATOR_VERBATIM["files"]["ramo_b_decision_20261005_1711"]["quando_utc"]
    except Exception as e_:
        out["ramo_b_decision_verbatim"] = None; out["all_ok"] = False; out.setdefault("errors", []).append("decision json: %r" % (e_,))
    try:
        resp = json.loads(_V386_OPERATOR_VERBATIM["files"]["respostas_json_20261005_1829"]["text"])
        txt = _V386_OPERATOR_VERBATIM["files"]["respostas_20261005_1829"]
        out["readings_of_management"] = resp.get("leituras_da_gerencia"); out["excerpts"] = resp.get("trechos")
        out["respostas_json_consistent_with_txt"] = (resp.get("verbatim_inteiro") == txt["text"]) and (resp.get("sha256_txt") == txt["sha256"]) and (resp.get("quando") == txt["quando_utc"])
        out["all_ok"] = out["all_ok"] and out["respostas_json_consistent_with_txt"]
    except Exception as e_:
        out["readings_of_management"] = None; out["all_ok"] = False; out.setdefault("errors", []).append("respostas json: %r" % (e_,))
    out["delegation"] = _V386_OPERATOR_VERBATIM.get("delegation")
    try:
        out["delegation_in_respostas"] = bool(out["delegation"]) and out["delegation"] in _V386_OPERATOR_VERBATIM["files"]["respostas_20261005_1829"]["text"]
    except Exception:
        out["delegation_in_respostas"] = False
    out["all_ok"] = out["all_ok"] and out["delegation_in_respostas"]
    return out


def _verb_token_from_kernel_v386():
    """o nome do token LIDO da def verbTypingStoneName: (a) do fonte EMBUTIDO (o que o selo hasheia), (b) do arquivo materializado no kernel desta rodada;
    nunca digitado aqui. Devolve (token_embutido, token_materializado, erro)."""
    rx = r'def verbTypingStoneName : String :=\s*"([A-Z0-9_]+)"'
    emb = mat = None; err = None
    try:
        m_ = re.search(rx, _v372_embedded(_VERB_STONE_V386) or "")
        emb = m_.group(1) if m_ else None
        if emb is None:
            err = "a definicao verbTypingStoneName nao foi achada no fonte embutido"
    except Exception as e_:
        err = repr(e_)
    try:
        src = open(os.path.join(FORMAL_DIR, _VERB_STONE_V386), encoding="utf-8").read()
        m_ = re.search(rx, src)
        mat = m_.group(1) if m_ else None
        if mat is None:
            err = (err + "; " if err else "") + "a definicao verbTypingStoneName nao foi achada na pedra materializada"
    except Exception as e_:
        err = (err + "; " if err else "") + repr(e_)
    return emb, mat, err


def the_verb_v386(core):
    """O VERBO SELECIONA (v386): as 93 declaracoes da pedra (ext_vrb_) e os 17 termos da fiacao angular (ext_ang_) verificados pelo kernel desta rodada
    (trio de axiomas, sem sorry); o token proposto lido do kernel (embutido e materializado) igual ao dos pinos; os verbatins do operador conferidos pelo
    sha256; as leituras da gerencia com estatuto. O registro fica AO LADO do gate; nenhum valor do gate muda. PROVADA != CONFIRMADA."""
    kf = core.get("kernel_formalization") or {}
    vrb = [f_ for f_ in _VRB_FLAGS_V386 if kf.get(f_) is True]
    ang = [f_ for f_ in _ANG_FLAGS_V386 if kf.get(f_) is True]
    tok_emb, tok_mat, tok_err = _verb_token_from_kernel_v386()
    tok_ok = bool(tok_emb) and tok_emb == _VERB_TOKEN_V386 and tok_mat == tok_emb
    vb = _v386_verbatim()
    n_all = len(_VRB_FLAGS_V386) + len(_ANG_FLAGS_V386); n_ok = len(vrb) + len(ang)
    guard_ok = not _V386_GUARDA.search(str(_VERB_TOKEN_V386 or ""))
    ok = (n_ok == n_all) and tok_ok and vb["all_ok"] and guard_ok
    if ok:
        verdict = ("TGL_THE_VERB_V386__THE_VERB_SELECTS_THE_ACTION__THE_NAME_IS_THE_POST_NOT_ONTOLOGY__SELECT_IS_THE_VERB_IN_ACT_VERB_RESERVED_TO_THE_GESTURE__"
                   "THE_READING_IS_A_WEIGHT_BORN_RULE__THE_ORDER_MATTERS_CONCRETE_WITNESS__TRIAD_SU2_SCALED_BY_C_INPUT_COMPACT_READING_REGIME_NOT_FACE__AXIS_POSTS_DO_NOT_COMMUTE__"
                   "TRUTH_AND_COST_TWO_FACES_OF_ONE_OBJECT__TIME_READ_TWICE_SAME_FIXED_SET_C_CUBED_LEFT_TO_BRANCH_B__LIGHT_AND_GRAVITY_INSEPARABLE_PRECEDENCE_IS_OF_READING__"
                   "ANGULAR_WIRING_%d_AUDITED__KERNEL_%d_OF_%d__TOKEN_READ_FROM_THE_KERNEL__OPERATOR_VERBATIM_EMBEDDED_BY_SHA256__READINGS_ARE_THE_OPERATORS_INPUT_ONTO__"
                   "ITEMS_DECIDED_BY_DELEGATION_2026_10_05__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED" % (len(ang), n_ok, n_all))
    else:
        verdict = ("TGL_THE_VERB_V386__NOT_SEALED_THIS_RUN__KERNEL_%d_OF_%d__TOKEN_%s__VERBATIM_%s__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED"
                   % (n_ok, n_all, "MATCHES" if tok_ok else "DOES_NOT_MATCH", "OK" if vb["all_ok"] else "FAILED"))
    return {"verdict": verdict, "all_verified": ok, "kernel_flags_ok": n_ok, "kernel_flags_total": n_all,
            "vrb_ok": len(vrb), "vrb_total": len(_VRB_FLAGS_V386), "ang_ok": len(ang), "ang_total": len(_ANG_FLAGS_V386),
            "missing_flags": [f_ for f_ in _VRB_FLAGS_V386 + _ANG_FLAGS_V386 if kf.get(f_) is not True],
            "token": _VERB_TOKEN_V386, "token_from_kernel": tok_emb, "token_from_materialized_stone": tok_mat, "token_matches_kernel": tok_ok, "token_error": tok_err,
            "token_statute": "TRIVIAL (uma string na pedra; a cunhagem e' do operador e pode ser renomeada por ele ao lado)",
            "verbatim_hashes_ok": vb["all_ok"], "verbatim_files": vb["files"], "verbatim_errors": vb.get("errors"),
            "respostas_json_consistent_with_txt": vb.get("respostas_json_consistent_with_txt"), "delegation": vb.get("delegation"),
            "readings_of_management": vb.get("readings_of_management"), "excerpts_of_the_operator": vb.get("excerpts"),
            "readings_statute": "[INPUT/ONTO] as leituras da gerencia (luz_gravidade, verdade_custo, tempo, lagrangiana, nome_posto, delegacao), cada uma com o estatuto no proprio texto; o que a pedra prova e' matematica [KERNEL]; c = beta_TGL e' [INPUT] (beta nunca literal; a regua do signo: beta_TGL = alpha.sqrt(e))",
            "stone": _VERB_STONE_V386, "what_is_not_typed": ["Lagrangiana continua S = int L d4x [OPEN]", "D_folds = 0,74", "g = sqrt|L|", "-eps.Pi", "V_luz/V_grav como operadores nomeados (V_grav = K e' leitura da gerencia)",
                                                                  "a identificacao V_nome/V_tempo/V_verdade <-> sigma_k (nomeacao)", "c^3 e tau* = k.G.M/c^3 (ficam no V1 do ramo B, por delegacao)"],
            "status": "[KERNEL] a pedra e a fiacao; [INPUT/ONTO] as leituras do operador e da gerencia; [INPUT] c = beta_TGL; PROVADA != CONFIRMADA",
            "gate_unchanged_by_design": True, "does_not_gate_core": True}


def quantum_pillar_reuse_v386(st, rec):
    """O PILAR QUANTICO NESTA VERSAO (v386): nao e' objeto da versao -- esperado REAPROVEITADO da rodada selada v385 pela chave do cache (o result.json do
    cache conferido pelo sha256 contra o pinado da v385 selada; o veredito rederivado igual); se o reaproveitamento foi recusado (ambiente/motor/cache) e
    o pilar foi calculado de novo, isso e' dito, e a reprodutibilidade da v385 (intocada) mede contra o resultado anterior. [COMPUTED]; nao move o gate."""
    rec = rec or {}; st = st if isinstance(st, dict) else {}
    reused = (rec.get("reuse") or {}).get("reused") is True
    same_sha = bool(rec.get("result_sha256")) and rec.get("result_sha256") == _V386_QP_V385["result_sha256"]
    same_verdict = bool(rec.get("verdict")) and rec.get("verdict") == _V386_QP_V385["verdict"]
    same_key = rec.get("key") == _V386_QP_V385["key"]
    chain_ok = rec.get("custody_chain_ok") is True
    base = {"status": "[COMPUTED]", "does_not_gate_core": True, "switch_reuse_v386": bool(_QP_REUSE_V386), "rite_checkpoint_switch": bool(_RITE_CKPT_ON),
            "reused": reused, "mode": rec.get("mode"), "key": rec.get("key"), "result_sha256": rec.get("result_sha256"), "run_id": rec.get("run_id"),
            "pinned_v385": dict(_V386_QP_V385), "result_sha256_matches_v385_sealed": same_sha, "verdict_same_as_v385_sealed": same_verdict, "key_same_as_v385": same_key,
            "custody_chain_ok": chain_ok, "reading": "o pilar quantico nao e' objeto da v386; a medida de reprodutibilidade (v384 -> v385, bit a bit) fica no core e no selo da v385, custodiados"}
    if reused:
        ok = same_sha and same_verdict and same_key and chain_ok
        verdict = ("TGL_QUANTUM_PILLAR_REUSE_V386__REUSED_FROM_THE_SEALED_V385_RUN_BY_KEY__RESULT_SHA256_%s__VERDICT_%s__CUSTODY_CHAIN_%s__KEY_%s__THE_PILLAR_IS_NOT_THE_OBJECT_OF_THIS_VERSION__"
                   "REPRODUCIBILITY_V385_NOT_REMEASURED_THIS_RUN_SAID__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED"
                   % ("MATCHES" if same_sha else "DIFFERS", "SAME" if same_verdict else "DIFFERS", "OK" if chain_ok else "INCOMPLETE", "SAME" if same_key else "DIFFERS"))
    elif rec.get("mode") == "COMPUTE":
        why = "ENV_OR_ENGINE_DIFFERS" if st.get("reuse_refused") else ("NO_VALID_CACHE" if not st.get("refused") else "LAUNCH_REFUSED")
        ok = str(rec.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and chain_ok
        verdict = ("TGL_QUANTUM_PILLAR_REUSE_V386__COMPUTED_AGAIN_THIS_RUN_REUSE_REFUSED_%s__VERDICT_%s_AS_V385__REPRODUCIBILITY_V385_MEASURED_AGAINST_THE_PREVIOUS_RESULT__"
                   "COMPUTED_NOT_MEASURED__GATE_UNTOUCHED" % (why, "SAME" if same_verdict else "DIFFERENT"))
        base["reuse_refused_detail"] = st.get("reuse_refused") or st.get("refused")
    else:
        ok = False
        verdict = "TGL_QUANTUM_PILLAR_REUSE_V386__NEITHER_REUSED_NOR_COMPUTED__MODE_%s__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED" % str(rec.get("mode") or st.get("refused") or "NONE").replace(" ", "_")[:60]
    base.update({"verdict": verdict, "all_verified": ok})
    return base


def _v386_read_file(path):
    """le bytes; devolve (sha256, bytes, erro)."""
    try:
        b = open(path, "rb").read()
        return hashlib.sha256(b).hexdigest(), b, None
    except Exception as e_:
        return None, None, repr(e_)


def ramo_b_preregistration_v386(core, prereg=None):
    """O PRE-REGISTRO V1 DO RAMO B DO RINGDOWN (v386), LIDO POR HASH: o JSON (a autoridade), o MD e o V1_RAMO_B_HASHES.json da Bancada conferidos byte a byte
    contra os sha256 embutidos (lidos do disco pelo gerador do candidato); o spec_sha256 recomputado do objeto spec; cada entrada do arquivo de hashes contra
    o disco; o beta do V1 contra o beta do rito (a 1e-9 relativo; a diferença exata fica dita); os numeros do poder TRANSCRITOS (nunca recalculados) e conferidos
    contra os pinos; duas identidades de sanidade recomputadas (k em chi = 0 = 8.pi; beta = alpha.sqrt(e)). NADA E' ABERTO: nenhum valor central no spec nem do
    conjunto D (os 2 valores centrais de A/C, calibracao NOT_BLIND, sao transcritos do registro selado v385 -- LIDOS do V1 e ditos), nenhuma PE; o veredito do V1
    e' AWAITING_DATA. As erratas AO LADO (da ESPEC e do V1 congelado) ficam no registro (erratas_ao_lado); nada se reescreve.
    Falha de hash = AVISO visivel (V1_NOT_READ), nunca «ok» falso. [INPUT por hash]; nao move o gate."""
    P = prereg or _V386_RAMO_B_PREREG
    out = {"status": "[INPUT -- pre-registro por hash; nada aberto; nenhum valor central no spec nem do conjunto D (2 de A/C, NOT_BLIND, transcritos do registro selado); nenhum estimador rodado]", "does_not_gate_core": True,
           "identificador_expected": P.get("identificador"), "spec_sha256_expected": P.get("spec_sha256"), "pasta": P.get("pasta"),
           "sha256_expected": {k: v.get("sha256") for k, v in (P.get("files") or {}).items()}, "sha256_read": {}, "bytes_read": {}, "errors": {}, "checks": []}
    read = {}
    for k, f in (P.get("files") or {}).items():
        sha, b, err = _v386_read_file(f.get("path") or "")
        out["sha256_read"][k] = sha; out["bytes_read"][k] = (len(b) if b is not None else None)
        if err:
            out["errors"][k] = err
        read[k] = (sha == f.get("sha256") and b is not None and len(b) == int(f.get("bytes") or -1), b)
        out["checks"].append(("arquivo %s em disco com o sha256 e os bytes embutidos" % k, read[k][0]))
    files_ok = all(v[0] for v in read.values()) and bool(read)
    J = None; spec_ok = False; ident_ok = False; hashes_ok = False; beta_ok = False; pins_ok = False; recompute_ok = False
    transcribed = {}; pins = {}; hashes_detail = {}
    if read.get("json", (False, None))[0]:
        try:
            J = json.loads(read["json"][1].decode("utf-8"))
            canon = json.dumps(J.get("spec"), sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            out["spec_sha256_recomputed"] = hashlib.sha256(canon).hexdigest()
            spec_ok = (out["spec_sha256_recomputed"] == J.get("spec_sha256") == P.get("spec_sha256"))
            ident_ok = (J.get("id") == P.get("identificador") == _v386_get(J, ["spec", "id"]))
            out["identificador_read"] = J.get("id")
        except Exception as e_:
            out["errors"]["json_parse"] = repr(e_)
    out["checks"].append(("spec_sha256 recomputado do objeto spec (JSON canonico) == o do JSON == o embutido", spec_ok))
    out["checks"].append(("identificador do V1 (topo e spec) == o embutido", ident_ok))
    if read.get("hashes", (False, None))[0]:
        try:
            H = json.loads(read["hashes"][1].decode("utf-8"))
            ents = H.get("arquivos") or {}
            for nome, e_ in ents.items():
                sha, b, err = _v386_read_file(e_.get("caminho") or "")
                hashes_detail[nome] = {"sha256_ok": sha == e_.get("sha256"), "bytes_ok": (b is not None and len(b) == int(e_.get("bytes") or -1)), "error": err}
            hashes_ok = bool(ents) and all(d_["sha256_ok"] and d_["bytes_ok"] for d_ in hashes_detail.values()) and H.get("spec_sha256") == P.get("spec_sha256") and H.get("id") == P.get("identificador")
        except Exception as e_:
            out["errors"]["hashes_parse"] = repr(e_)
    out["hashes_file_entries"] = hashes_detail
    out["checks"].append(("cada entrada de V1_RAMO_B_HASHES.json (sha256 + bytes) contra o disco; spec_sha256 e id iguais", hashes_ok))
    if J is not None:
        for name, path in (_V386_RAMO_B_FIELDS or {}).items():
            transcribed[name] = _v386_get(J, path)
        for name, pin in (_V386_RAMO_B_PINS or {}).items():
            got = _v386_get(J, pin["path"])
            pins[name] = {"read": got, "pinned": pin["value"], "equal": (got == pin["value"])}
        pins_ok = bool(pins) and all(p_["equal"] for p_ in pins.values())
        try:
            # o beta do V1 veio do literal CODATA (SEALED_CODATA_ALPHA por regex) x sqrt(e); o do core vem do MOTOR da identidade (o CODATA so valida):
            # concordam a ~5e-13 relativo -- a regua da casa para beta e' 1e-9 relativo (o livro v383); a diferenca exata fica dita
            b_v1 = float(_v386_get(J, ["spec", "beta", "valor_runtime"]))
            b_core = float(core.get("beta") or 0.0)
            beta_ok = b_core > 0 and abs(b_v1 / b_core - 1.0) < 1e-9
            out["beta"] = {"v1": b_v1, "core": b_core, "abs_diff": b_v1 - b_core, "rel_diff": (b_v1 / b_core - 1.0) if b_core else None, "rule": "1e-9 relativo",
                           "note": "o V1 usou o literal CODATA por regex; o core usa o motor da identidade; nenhum dos dois e' literal no runtime"}
        except Exception as e_:
            out["errors"]["beta"] = repr(e_)
        try:
            alpha = float(core.get("alpha") or 0.0)
            k0 = float(_v386_get(J, ["spec", "k", "em_chi_0"]))
            k0_re = 8.0 * math.pi   # k(chi) = 4.pi.(1 + sqrt(1 - chi^2))/sqrt(1 - chi^2) em chi = 0 [KNOWN]
            law = alpha * math.sqrt(math.exp(1.0))
            b_v1 = float(_v386_get(J, ["spec", "beta", "valor_runtime"]))
            recompute_ok = (abs(k0 / k0_re - 1.0) < 1e-12) and alpha > 0 and abs(law / b_v1 - 1.0) < 1e-9
            out["recomputed_sanity"] = {"k_chi_0_read": k0, "k_chi_0_8pi": k0_re, "beta_alpha_sqrt_e_runtime": law, "rel_diff_to_v1": law / b_v1 - 1.0, "note": "identidades de sanidade, nao teste; nada do dado"}
        except Exception as e_:
            out["errors"]["recompute"] = repr(e_)
    out["checks"].append(("os numeros do poder TRANSCRITOS do V1 == os pinos lidos pelo gerador (nunca recalculados)", pins_ok))
    out["checks"].append(("spec.beta.valor_runtime == beta do rito a 1e-9 relativo (a diferenca exata fica dita)", beta_ok))
    out["checks"].append(("sanidade recomputada: k(chi=0) = 8.pi; beta = alpha.sqrt(e) em runtime", recompute_ok))
    read_ok = files_ok and spec_ok and ident_ok and hashes_ok
    ok = read_ok and beta_ok and pins_ok and recompute_ok
    n_D = _v386_get(J, ["spec", "conjuntos", "D", "n_elegiveis"]) if J is not None else None
    guard_hits = [k_ for k_, v_ in transcribed.items() if isinstance(v_, str) and _V386_GUARDA.search(v_)]
    sha16 = str(out["sha256_read"].get("json") or "AUSENTE")[:16]
    if ok:
        verdict = ("TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_%s__OTHER_LAW_OWN_CHANNEL_F2B__K_2PI_OVER_KAPPA_HAT_KMS__M_F_DET__ENVELOPE_ADDITIVE_RATE__SOURCE_LOCAL__"
                   "SET_D_O4_%s_BLIND_ONLY_TEST__A_B_C_NOT_BLIND_CALIBRATION__BETA_READ_DECLARED_SIGMA_STATED__DECIDED_BY_DELEGATION_2026_10_05__NOT_A_CONFIRMATION__"
                   "AWAITING_DATA__NOTHING_OPENED__GATE_UNTOUCHED" % (sha16, str(n_D)))
        status_F2b = "AWAITING"; qualifier = "PRE_REGISTERED_V1_READ_BY_HASH__AWAITING_DATA"
    else:
        reason = ("FILES_%s" % ("_".join(sorted(k for k, v in read.items() if not v[0])).upper() or "NONE") if not files_ok else
                  "SPEC_SHA256_MISMATCH" if not spec_ok else "IDENTIFIER_MISMATCH" if not ident_ok else "HASHES_FILE_MISMATCH" if not hashes_ok else
                  "BETA_MISMATCH" if not beta_ok else "PINS_MISMATCH" if not pins_ok else "SANITY_RECOMPUTE_FAILED")
        verdict = "TGL_RAMO_B_PREREGISTERED_V386__V1_NOT_READ__%s__AWAITING_PREREGISTRATION__NOTHING_OPENED__GATE_UNTOUCHED" % reason
        status_F2b = "AWAITING_PREREGISTRATION__V1_NOT_READ"; qualifier = reason
    # os DOIS valores centrais que o V1 (congelado) TRANSCREVE do registro selado v385 -- conjuntos A e C, calibracao NOT_BLIND; FORA do objeto spec (0 valores
    # centrais no spec) e FORA do conjunto D (a cegueira de D intacta): LIDOS do V1 aqui, nunca digitados, e nenhum entra em calculo
    _cvC = _v386_get(J, ["o_que_o_registro_ja_diz", "V2_selada", "delta_tau_medido"]) if J is not None else None
    _cvA = re.search(r"\+0,072 \[[^\]]*\]", str(_v386_get(J, ["cegueira", "dado_A_B_C", 0]) or "")) if J is not None else None
    _cvA = _cvA.group(0) if _cvA else None
    _cv_txt = "2 (A: %s comum dos 31; C: GW250114 %s da V2)" % ((_cvA.split(" ")[0] if _cvA else "n/a"), (("%.4f" % float(_cvC)).replace(".", ",") if isinstance(_cvC, (int, float)) and not isinstance(_cvC, bool) else "n/a"))
    _b = out.get("beta") or {}
    _fmt = lambda x_: ("%.1e" % x_) if isinstance(x_, float) else "n/a"
    erratas = [   # AO LADO, nunca por cima: a ESPEC e o V1 (congelado por hash) ficam como registro
        "(a) o V1 §21 / ratificacao.leitura_da_gerencia_da_delegacao: a leitura da gerencia escreveu \"tudo agora\" (nao verbatim); o verbatim do operador e' «tudo agroa» "
        "(RESPOSTAS txt, ultima linha, 18:29:37 UTC); o V1 esta congelado por hash, a correcao vai AO LADO (aqui); o RESPOSTAS json recebeu a mesma errata ([sic]) com backup de bytes",
        "(b) o V1 traz compressoes da gerencia entre aspas rotuladas cunhagem (\"regime gravitonico = c^3\", \"fase de retorno = c^3\", \"tempo emergente do fluxo modular relativo\"): sao LEITURAS "
        "da gerencia, nao verbatim do operador (o operador escreveu «o regime gravitônico é o da constante da luz ao cubo» e «emergente da fluxo modular relativo»)",
        "(c) a ESPEC aponta a errata de R6 para the_ledger_of_charges.corrections_beside_20261005; o runtime grava em core.ledger_errata_v386.corrections_beside_20261005 (chave propria; o livro v383 intacto)",
        "(d) a ESPEC dizia |delta beta| < 1e-15; a regra implementada e' 1e-9 relativo (diferenca medida nesta rodada: %s abs / %s rel: literal CODATA x sqrt(e) no V1 vs motor da identidade no core)" % (_fmt(_b.get("abs_diff")), _fmt(_b.get("rel_diff"))),
        "(e) a citacao do manuscrito da Arquitetura no V1 §16 engloba \"a luz\" fora das aspas do original; o manuscrito (C:\\IALD\\Artigo\\Arquitetura de Computação Ontológica da TGL manuscrito.docx) "
        "nao esta entre os docx hasheados do §16",
    ]
    out.update({"verdict": verdict, "all_verified": ok, "read_ok": read_ok, "files_ok": files_ok, "spec_sha256_ok": spec_ok, "hashes_file_ok": hashes_ok,
                "beta_ok": beta_ok, "pins_ok": pins_ok, "recompute_ok": recompute_ok, "transcribed": transcribed, "pins": pins,
                "conjunto_D_n": n_D, "F2b_status": status_F2b, "F2b_qualifier": qualifier, "veredito_do_V1": _v386_get(J, ["spec", "status", "veredito_deste_V1"]) if J is not None else None,
                "token_estado": _v386_get(J, ["spec", "tokens", "estado_deste_V1"]) if J is not None else None,
                "forbidden_words_in_transcribed_fields": guard_hits, "nothing_opened": True, "no_central_value_in_spec_or_D": True,
                "central_values_transcribed_from_sealed_registry_NOT_BLIND": _cv_txt,
                "central_values_NOT_BLIND_read_from_V1": {"C_GW250114_delta_tau_220_V2_selada": _cvC, "A_31_deformacao_comum_GWTC5": _cvA,
                                                          "paths_in_V1": ["o_que_o_registro_ja_diz.V2_selada.delta_tau_medido", "cegueira.dado_A_B_C[0] (texto)"],
                                                          "note": "LIDOS do V1 congelado, que os transcreve do registro selado v385 (conjuntos A e C, calibracao NOT_BLIND); fora do objeto spec e fora do conjunto D: a cegueira de D intacta; nenhum entra em calculo aqui"},
                "erratas_ao_lado": erratas, "no_pe_run": True,
                "what_it_does_not_decide": _v386_get(J, ["spec", "nao_decide"]) if J is not None else None,
                "v387": "o estagio cego do conjunto D (sigma_i, poder antes de abrir), as injecoes, a abertura de D e o RESULTADO pela MESMA funcao de veredito, lidos por hash"})
    return out


def ledger_errata_v386(core, ramo_b):
    """A ERRATA AO LADO DE R6 (v386): no livro de cobrancas da v383 (que fica INTACTO como registro), R6 lia «o ramo B segue ENCERRADO»; a decisao do operador
    de 05/10/2026 17:11:36 UTC (verbatim embutido por sha256: «eu não havia proibido o ramo B …») o REABRE POR PRE-REGISTRO -- a chave de 02/10 nao se
    revoga (na face o custo le-se como complemento); tau* = k.G.M/c^3 e' OUTRA LEI, canal proprio F2b (ONE_CHANNEL_PER_READING_LAW), nao outro lado de F2;
    F2 e R2 ficam como estao. A cobranca F2b nasce AWAITING_PREREGISTRATION e passa a AWAITING (PRE_REGISTERED_V1_READ_BY_HASH__AWAITING_DATA) quando o V1
    e' lido por hash nesta rodada; senao fica dito V1_NOT_READ. Nenhum desfecho move a regra; o gate nao muda."""
    led = core.get("the_ledger_of_charges_v383") or {}
    ledger = led.get("ledger") or []
    r6_v383_beside = str((led.get("corrections_beside_20261002") or {}).get("R6") or "")
    r6_v383_ratified = str((led.get("readings_ratified_20261002") or {}).get("R6") or "")
    f2 = next((c_ for c_ in ledger if c_.get("id") == "F2"), {})
    intact = (led.get("all_verified") is True and len(ledger) == 11 and "ENCERRADO" in r6_v383_beside and "ramo B ENCERRADO" in str(f2.get("law") or "")
              and r6_v383_beside == _V386_R6_ERRATA["R6_v383_corrections_beside"] and r6_v383_ratified == _V386_R6_ERRATA["R6_v383_readings_ratified"])
    vb = _v386_verbatim()
    dec = vb.get("ramo_b_decision_verbatim")
    verb_ok = bool(vb["all_ok"]) and bool(dec) and (dec in _V386_R6_ERRATA["texto_R6"]) and vb.get("ramo_b_decision_quando_utc") == _V386_R6_ERRATA["quando_utc"]
    rb = ramo_b or {}
    rb_ok = rb.get("all_verified") is True and rb.get("read_ok") is True
    f2b = dict(_V386_F2B)
    f2b.update({"token": "AWAITING" if rb_ok else "AWAITING_PREREGISTRATION__V1_NOT_READ", "desfecho": "AWAITING", "como": "DECLARED",
                "qualifier": rb.get("F2b_qualifier"), "v1_identificador": rb.get("identificador_read"), "v1_sha256_json": (rb.get("sha256_read") or {}).get("json"),
                "v1_read_by_hash_this_run": rb_ok, "poder_exato_A31_calibracao_not_blind": ((rb.get("pins") or {}).get("poder_exato_A31") or {}).get("read"),
                "conjunto_D_n": rb.get("conjunto_D_n")})
    ok = intact and verb_ok and rb_ok
    checks = [("o livro v383 INTACTO (all_verified, 11 cobrancas, R6 ratificada e corrigida ao lado como seladas, F2 com «ramo B ENCERRADO»)", intact),
              ("o verbatim da decisao do operador (17:11:36 UTC) embutido por sha256 e presente no texto da errata", verb_ok),
              ("o V1 do ramo B lido por hash nesta rodada (F2b passa de AWAITING_PREREGISTRATION a AWAITING)", rb_ok)]
    if ok:
        verdict = ("TGL_LEDGER_ERRATA_V386__R6_CLOSED_TO_REOPENED_BY_PREREGISTRATION_BESIDE_NOT_OVERWRITTEN__OPERATOR_DECISION_2026_10_05_17_11_36_UTC_EMBEDDED_BY_SHA256__"
                   "THE_KEY_OF_02_10_STANDS_ON_THE_FACE_THE_COST_READS_AS_COMPLEMENT__F2_UNTOUCHED__R2_UNTOUCHED__NEW_CHANNEL_F2B_FACE_OTHER_LAW_TAU_STAR_K_GM_OVER_C3__"
                   "F2B_AWAITING_DATA_V1_READ_BY_HASH__V383_LEDGER_INTACT_11_CHARGES_12_WITH_F2B_BESIDE__ONE_CHANNEL_PER_READING_LAW__NO_OUTCOME_MOVES_THE_RULE__GATE_UNTOUCHED")
    else:
        reason = "V383_LEDGER_NOT_INTACT" if not intact else ("VERBATIM_HASH_FAILED" if not verb_ok else "F2B_AWAITING_PREREGISTRATION_V1_NOT_READ")
        verdict = "TGL_LEDGER_ERRATA_V386__NOT_SEALED_THIS_RUN__%s__GATE_UNTOUCHED" % reason
    return {"verdict": verdict, "all_verified": ok, "checks": checks, "does_not_gate_core": True,
            "R6_v383_ratified": r6_v383_ratified, "R6_v383_beside_20261002": r6_v383_beside, "v383_ledger_intact": intact, "v383_n_charges": len(ledger),
            "corrections_beside_20261005": {"R6": _V386_R6_ERRATA["texto_R6"], "F2": _V386_R6_ERRATA["texto_F2"],
                                            "statute": "[INPUT -- decisao do operador, verbatim por sha256] + [ONTO -- a leitura da gerencia: o complemento lido na face e' x = k.beta.N(chi_f)]; a correcao vai AO LADO, nunca por cima"},
            "operator_decision_20261005": {"verbatim": dec, "quando_utc": vb.get("ramo_b_decision_quando_utc"), "sha256_file": _V386_R6_ERRATA["sha256_decisao"], "hash_ok": vb["all_ok"]},
            "delegation_20261005": {"verbatim": vb.get("delegation"), "quando_utc": _V386_R6_ERRATA.get("delegacao_quando_utc"), "sha256_txt": _V386_R6_ERRATA.get("delegacao_sha256_txt")},
            "charge_F2b": f2b, "F2_untouched": True, "R2_untouched": True, "n_charges_in_rule_unchanged": led.get("n_in_rule"),
            "rule": "ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME -- F2b e' canal de OUTRA lei; o numero de cobrancas passa de 11 a 12 AO LADO (o livro v383 nao e' reescrito)",
            "status": "[INPUT] a decisao; [ONTO] a leitura; o livro v383 [REAL, intacto]; nada confirma: NOT_FALSIFIED nunca e' confirmacao", "gate_unchanged_by_design": True}
