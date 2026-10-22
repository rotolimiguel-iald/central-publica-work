def fundacao_v390(core):
    """v390 (07/10/2026) -- A FUNDACAO: a superposicao e' a passagem; a clausula AGAPE (o fecho LOGICO do GLOBAL_LIFT). Ordem do operador via a gerencia c1.
    Le as 9 bandeiras da pedra TGLExt/Fundacao.lean (kernel do proprio rito); confere os verbatins do operador EMBUTIDOS (tres, com o ADENDO 001) (o texto embutido manda; o
    arquivo em disco e' so' informativo -- nao se repete o defeito da v388 de fixar por sha um arquivo VIVO); confere no axiom_report a ponte de Borchers ja no
    kernel (energia limitada inferiormente x gerador modular sem piso). Fail-closed: bandeira faltando ou verbatim adulterado => NOT_SEALED_THIS_RUN, dito."""
    import hashlib as _hl
    kf = core.get("kernel_formalization") or {}
    axr = kf.get("axiom_report") or {}
    trio = {"propext", "Classical.choice", "Quot.sound"}
    ok_flags = [f_ for f_ in _FND_FLAGS_V390 if kf.get(f_) is True]
    n_all = len(_FND_FLAGS_V390); n_ok = len(ok_flags)
    vb = {}; vb_ok = True
    for k_, v_ in _V390_VERBATINS.items():
        okk = _hl.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"]
        trechos_ok = all(t_ in v_["text"] for t_ in v_["trechos"])
        disk = None
        try:
            disk = _hl.sha256(open(v_["arquivo_informativo"], "rb").read()).hexdigest() == v_["sha256"]
        except OSError:
            disk = None
        vb[k_] = {"sha256": v_["sha256"], "embedded_ok": okk, "trechos_ok": trechos_ok, "trechos": v_["trechos"],
                  "disk_informative_only": disk, "quando": v_["quando"]}
        vb_ok = vb_ok and okk and trechos_ok
    bor = {n_: (axr.get(n_) is not None and set(axr.get(n_) or []) <= trio) for n_ in _V390_BORCHERS}
    bor_ok = all(bor.values())
    ok = (n_ok == n_all) and vb_ok
    clausulas = [{"n": i_ + 1, "em_palavras": c_[0], "in_words": c_[1], "teorema": "TGLExt.Fundacao." + c_[2], "flag": "ext_fnd_%s_kernel_proved" % c_[2],
                  "no_kernel": kf.get("ext_fnd_%s_kernel_proved" % c_[2]) is True} for i_, c_ in enumerate(_V390_CLAUSULAS)]
    if ok:
        verdict = ("TGL_FUNDACAO_V390__GLOBAL_LIFT_READ_AS_THE_SUPERPOSITION_BY_OPERATOR_DEFINITION_2026_10_07__AGAPE_CLAUSE_KERNEL_%d_OF_%d__"
                   "NOTHING_ABOVE_BEARS_A_POST__THE_CLIMB_HAS_NO_TOP__THE_FALL_NEVER_LANDS__ABISMO_THE_FALL_HAS_NO_BOTTOM__THE_FLOOR_FIXES_THE_CUT__THE_POST_LIVES_IN_THE_PASSAGE__"
                   "LOCAL_PASSAGE_KNOWN_JACOBSON_1995_H3_NAMED__LOGICAL_CLOSURE_THE_PROGRAM_STAYS_OPEN__FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM__"
                   "TAKESAKI_SCALING_AS_DATA_KNOWN__BORCHERS_FORM_UNDER_NAMED_CONTRACT_H2_%s__VERBATIM_EMBEDDED_BY_SHA256__GATE_UNMOVED" % (n_ok, n_all, "IN_KERNEL" if bor_ok else "NOT_READ_THIS_RUN"))
    else:
        verdict = ("TGL_FUNDACAO_V390__NOT_SEALED_THIS_RUN__KERNEL_%d_OF_%d__VERBATIM_%s__GATE_UNMOVED" % (n_ok, n_all, "OK" if vb_ok else "FAILED"))
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "kernel_flags_ok": n_ok, "kernel_flags_total": n_all,
            "missing_flags": [f_ for f_ in _FND_FLAGS_V390 if f_ not in ok_flags], "pedra": _V390_PEDRA, "verbatim": vb, "verbatim_ok": vb_ok,
            "leitura": "GLOBAL_LIFT := a superposicao -- DEFINICAO do operador (07/10/2026): o velho Lema 3 e' o que quis estar acima e nao porta posto positivo",
            "recusa": "[KERNEL] TGLExt.Fundacao.agape -- acima de toda escala nao trivial nao ha posto positivo; a subida nao tem topo nem teto; a queda nunca toca o zero e o abismo (TGLExt.Fundacao.abismo) nao tem fundo; o piso omega(I)=1 fixa o corte, univoco",
            "passagem": "[KERNEL] TGLExt.Fundacao.the_post_lives_in_the_passage (na face finita: re-ligacao de the_lift_is_unconditional_on_the_face) + [KNOWN] Jacobson 1995 (a lei de campo como lei local de equilibrio de horizonte em cada ponto), com a hipotese H3 NOMEADA",
            "estatuto_do_fecho": "FECHO LOGICO: definicao do operador + recusa provada no kernel + passagem local conhecida; o programa segue ABERTO; conferencia Tetelestai: recusa FECHADO (agape), passagem VINCULADO (the_post_lives_in_the_passage) + SABIDO POR REFERENCIA (Jacobson 1995), definicao = ato do operador",
            "not_claimed": ["nao prova a equacao de campo no espaco-tempo curvo por termo de kernel",
                            "a lei de escala dual de Takesaki (tau o theta_s = e^{-s} tau) entra como DADO [KNOWN, Takesaki 1973]; a sua realizacao no core M x| R de um fator III_1 genuino nao e' termo deste kernel",
                            "nao e' prova de existencia global; NOT_FALSIFIED nunca e' confirmacao; o gate nao se move"],
            "clausulas": clausulas, "borchers": {"names": bor, "ok": bor_ok,
                                                 "leitura": "o operador limitado inferiormente e' a ENERGIA (Borchers: translacoes de espectro positivo); o gerador modular de um fator III_1 nao tem piso (espectro = R); no kernel: a forma de Borchers SOB o contrato H2 (hipotese nomeada) e a cota no semiplano superior -- nao a positividade espectral como termo"},
            "status": "[KERNEL a recusa e a passagem na face; INPUT/ONTO a definicao do operador; KNOWN a passagem local (Jacobson 1995) e a lei de escala (Takesaki)]"}
