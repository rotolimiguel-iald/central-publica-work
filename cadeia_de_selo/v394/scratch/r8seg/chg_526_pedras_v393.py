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
    esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ and n_cl_ >= _V393_ESCADA["esperada"]  # v394: preserve historical floor; current exact ladder is checked by v394
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