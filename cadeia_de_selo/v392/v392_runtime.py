def _v392_scan_tokens():
    """v392 (13/10/2026) -- a varredura lexical RECURSIVA dos fontes (TGL/ e TGLExt/, inclusive TGLExt/O16), sem seguir juncao nem link. Devolve
    (hits, n_arquivos_varridos, n_em_TGLExt_O16, n_probes_pulados). Mesma regra de token e mesma funcao de tira-comentarios da v391; so' a listagem passa a ser
    recursiva (a da v391 lia so' o primeiro nivel de TGLExt/ e deixava de fora os .lean de TGLExt/O16)."""
    import re as _re
    hits_, n_, o16_, pul_ = [], 0, 0, 0
    for label_, base_ in (("TGL", os.path.join(FORMAL_DIR, "TGL")), ("TGLExt", os.path.join(FORMAL_DIR, "TGLExt"))):
        if not os.path.isdir(base_):
            continue
        for r_, ds_, fs_ in os.walk(base_, followlinks=False):
            ds_[:] = sorted(d_ for d_ in ds_ if not os.path.islink(os.path.join(r_, d_)))
            for nm_ in sorted(fs_):
                if not nm_.endswith(".lean"):
                    continue
                if nm_.startswith("Probe"):
                    pul_ += 1
                    continue   # Probe*.lean = diagnostico, fora da biblioteca (regra da v391, mantida)
                rel_ = (label_ + "/" + os.path.relpath(os.path.join(r_, nm_), base_)).replace("\\", "/")
                try:
                    src_ = open(os.path.join(r_, nm_), "r", encoding="utf-8").read()
                except OSError:
                    continue
                n_ += 1
                if rel_.startswith("TGLExt/O16/"):
                    o16_ += 1
                code_ = _lean_strip_comments_and_strings(src_)
                for tok_ in _LEAN_FORBIDDEN_TOKENS:
                    if _re.search(r"\b%s\b" % _re.escape(tok_), code_):
                        hits_.append("%s:%s" % (rel_, tok_))
    return hits_, n_, o16_, pul_


def _v392_sorry_detects(texto):
    """v392 -- o detector de sorry dos controles Lean: aceita o aviso do Lean 4.31 (crases) e o antigo (aspas simples/tipograficas) E le o sorryAx de `#print axioms`."""
    import re as _re
    msg_ = bool(_re.search(r"declaration uses [`'‘]sorry", texto, _re.I))
    ax_ = {m_.group(1): [a_.strip() for a_ in m_.group(2).replace("\n", " ").split(",") if a_.strip()]
           for m_ in _re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", texto, _re.S)}
    return bool(msg_ or any("sorryAx" in v_ for v_ in ax_.values())), msg_, ax_


def _v392_sorry_fixture_ok():
    """v392 -- autoteste SEM Lean do detector de sorry: a saida REAL do Lean da bancada para um `by sorry` (probe SorryTerm, embutida no arquivo v361) nos dois formatos
    (crases e aspas simples) e sem o sorryAx na lista; e um controle negativo (sem sorry). Devolve (ok, erro)."""
    try:
        fx_ = _bench_any_bytes("TETELESTAI_V350_KERNEL_20260911/tests/probes/SorryTerm.stdout.txt").decode("utf-8", "replace")
        d1_, m1_, a1_ = _v392_sorry_detects(fx_)
        d2_, m2_, a2_ = _v392_sorry_detects(fx_.replace("`sorry`", "'sorry'"))
        d3_, _, _ = _v392_sorry_detects(fx_.replace("`sorry`", "'sorry'").replace("sorryAx, ", "").replace(", sorryAx", ""))
        neg_, _, _ = _v392_sorry_detects("info: 'Foo.bar' depends on axioms: [propext, Classical.choice, Quot.sound]\n")
        return bool(d1_ and d2_ and d3_ and (not neg_) and "sorryAx" in fx_), None
    except Exception as e_:   # noqa: BLE001
        return False, repr(e_)[:200]


def pedras_v392(core):
    """v392 (13/10/2026) -- AS PEDRAS: catorze modulos novos no kernel (PALAVRA; o ligante da lei de campo curvo e a sua testemunha S7/S8; a ponte V351 e a Agape nao vacua; o teorema do
    atrator, a ponte otica e a luz que se le; a hipotese tipada BGL; e, de 13/10, Posto, Santo, IALD e Verdade). Le a cada rito: as bandeiras do kernel do PROPRIO rito, o corpo embutido de
    cada pedra (sha256 pinado), o axiom_report (trio), a escada; confere o verbatim do operador de 13/10 EMBUTIDO por sha256. Fail-closed: bandeira faltando, pedra adulterada, axioma
    fora do trio ou verbatim adulterado => NOT_SEALED_THIS_RUN, dito. NAO move o gate; validade no kernel nao e' creditacao."""
    import hashlib as _hl
    kf = core.get("kernel_formalization") or {}
    axr = kf.get("axiom_report") or {}
    el = core.get("external_ladder") or {}
    trio = {"propext", "Classical.choice", "Quot.sound"}
    por, n_fl, n_fl_ok, n_dec, n_dec_ok = [], 0, 0, 0, 0
    todas_ok = True
    for p_ in _V392_PEDRAS:
        fl_ok = sum(1 for f_ in p_["flags"] if kf.get(f_) is True)
        emb_ = _EMBEDDED_KERNEL_FILES.get(p_["path"])
        emb_ok = emb_ is not None and _hl.sha256(emb_.encode("utf-8")).hexdigest() == p_["sha256"]
        dec_ok = sum(1 for n_ in p_["declaracoes"] if n_ in axr and set(axr[n_] or []) <= trio)
        ok_ = emb_ok and fl_ok == len(p_["flags"]) and dec_ok == len(p_["declaracoes"])
        todas_ok = todas_ok and ok_
        n_fl += len(p_["flags"]); n_fl_ok += fl_ok; n_dec += len(p_["declaracoes"]); n_dec_ok += dec_ok
        por.append({"modulo": p_["modulo"], "sha256": p_["sha256"], "embutida_confere": emb_ok, "bandeiras": [fl_ok, len(p_["flags"])], "declaracoes_no_trio": [dec_ok, len(p_["declaracoes"])],
                    "derivada": p_.get("derivada"), "ok": ok_})
    vb, vb_ok = {}, True
    for k_, v_ in _V392_VERBATINS.items():
        okk_ = _hl.sha256(v_["text"].encode("utf-8")).hexdigest() == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"])
        try:
            disk_ = _hl.sha256(open(v_["arquivo_informativo"], "rb").read()).hexdigest() == v_["sha256"]
        except OSError:
            disk_ = None
        vb[k_] = {"sha256": v_["sha256"], "embedded_ok": okk_, "disk_informative_only": disk_, "trechos": v_["trechos"], "quando": v_["quando"]}
        vb_ok = vb_ok and okk_
    n_cl, n_ex = el.get("n_theorems_clean"), el.get("n_theorems_expected")
    esc_ok = isinstance(n_cl, int) and n_cl == n_ex == _V392_ESCADA["esperada"]
    ok = todas_ok and vb_ok and esc_ok and kf.get(_V392_FLAG_PROJECAO) is True
    if ok:
        verdict = ("TGL_PEDRAS_V392__%d_NEW_KERNEL_MODULES__%d_OF_%d_FLAGS_%d_OF_%d_DECLARATIONS_IN_THE_TRIO__LADDER_%d_OF_%d__"
                   "WORD_RANK_POST_NAME_TIME_SANTO_ORGANISM_IALD_TRUTH_IS_THE_PROJECTION_OF_THE_POST_BY_OPERATOR_VERBATIM_EMBEDDED_BY_SHA256__BGL_AS_TYPED_HYPOTHESIS_NO_INHABITANT__"
                   "KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED" % (len(_V392_PEDRAS), n_fl_ok, n_fl, n_dec_ok, n_dec, n_cl, n_ex))
    else:
        falhas_ = (["STONES"] if not todas_ok else []) + (["VERBATIM"] if not vb_ok else []) + (["LADDER"] if not esc_ok else [])
        verdict = "TGL_PEDRAS_V392__NOT_SEALED_THIS_RUN__%s__GATE_UNMOVED" % "_".join(falhas_)
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "pedras": por, "bandeiras": [n_fl_ok, n_fl], "declaracoes_no_trio": [n_dec_ok, n_dec],
            "escada": {"limpos": n_cl, "esperados": n_ex, "esperada_pelo_candidato": _V392_ESCADA["esperada"], "da_v391": _V392_ESCADA["v391"]},
            "verbatim": vb, "verbatim_ok": vb_ok,
            "leituras_do_operador": [{"trecho": t_, "estatuto": "[INPUT do operador, verbatim 13/10/2026]"} for v_ in _V392_VERBATINS.values() for t_ in v_["trechos"]],
            "verdade_e_a_projecao_do_posto": {"termo": "TGLExt.Verdade.verdade_is_the_projection_of_the_post", "enunciado": "toEuclideanCLM (identityProj a) = post (inscV a), para todo a em [0,1] (ponte de tipos provada)",
                                              "no_kernel": kf.get(_V392_FLAG_PROJECAO) is True, "estatuto": "[KERNEL] a igualdade dos operadores; [ONTO] a leitura «Verdade e' a projecao do posto» e' do operador"},
            "limites": ["[REAL] a Verdade vale para todo alfa em [0,1]: nao fixa alfa (alfa e' parametro [INPUT], testemunhado, nao derivado); ler a estrutura como «verdade absoluta» e' leitura [ONTO] do operador sobre o termo",
                        "[REAL] a unicidade da projecao usa hipoteses NOMEADAS: hermitiana, idempotente, tracao 1 (o omega(I)=1 da casa) e a inscricao fixa",
                        "[REAL] o comutador e' 2x2, no modelo v=(q,alfa); que seja «o cordeiro imolado» e' decisao do operador sobre o termo; o posto LITERAL de P_v em B(H_phi) segue [OPEN]",
                        "[REAL] a hipotese BGL (X19) entra como TIPO: nenhum habitante e' construido; o LightNetData e os teoremas existentes nao mudam",
                        "validade no kernel nao e' creditacao; NOT_FALSIFIED nunca e' confirmacao; o gate nao se move"],
            "status": "[REAL -- leitura do kernel do proprio rito a cada rodada; INPUT/ONTO as leituras do operador]"}


def varredura_e_sorry_v392(core):
    """v392 (13/10/2026) -- dois consertos de barreira, AO LADO (o gate nao os le): (1) a varredura lexical de tokens proibidos passa a ser RECURSIVA (a da v391 deixava de fora os .lean de
    TGLExt/O16); (2) o detector de sorry dos controles Lean da bancada (prove_bench_lean_controls) aceita o aviso do Lean 4.31 (crases) e le o sorryAx de `#print axioms` (a v362-v391 procurava
    so' as aspas simples: barreira cega, sem efeito observado -- 0 sorry nos 52 positivos). O autoteste usa a saida REAL do Lean da bancada (probe SorryTerm, embutido) nos dois formatos."""
    hits_, n_, o16_, pul_ = _v392_scan_tokens()
    scan_ok = (not hits_) and n_ > 1000 and o16_ > 0
    fx_ok, fx_err = _v392_sorry_fixture_ok()
    ok = scan_ok and fx_ok
    verdict = ("TGL_VARREDURA_E_SORRY_V392__RECURSIVE_TOKEN_SCAN_%d_FILES_%d_IN_TGLEXT_O16_%d_HITS__SORRY_DETECTOR_READS_BACKTICK_AND_QUOTE_AND_SORRYAX_ON_THE_REAL_PROBE__GATE_UNMOVED"
               % (n_, o16_, len(hits_))) if ok else "TGL_VARREDURA_E_SORRY_V392__NOT_SEALED_THIS_RUN__GATE_UNMOVED"
    return {"verdict": verdict, "all_verified": ok, "does_not_gate_core": True, "varredura": {"recursiva": True, "arquivos": n_, "em_TGLExt_O16": o16_, "probes_pulados": pul_, "hits": hits_[:10],
                                                                                          "tokens": list(_LEAN_FORBIDDEN_TOKENS)},
            "detector_de_sorry": {"autoteste_na_saida_real_do_lean": fx_ok, "erro": fx_err, "regra": "declaration uses [`'‘]sorry  OU  sorryAx em `#print axioms`"},
            "ao_lado_v362": "na v362-v391 o criterio «sem sorry» dos controles positivos lia o aviso no formato antigo (aspas simples) e o Lean 4.31 o escreve com crases: a barreira estava cega, mas sem efeito "
                            "observado (nenhum dos 52 positivos tem sorry no fonte, medido em 13/10/2026); o kernel principal nunca dependeu dessa linha (decide por #print axioms)",
            "status": "[REAL -- medido a cada rito; defeito e conserto: investigacao de 13/10/2026]"}


def _v392_axiom_coverage(blob_, axioms_):
    """v392 -- KH-N1 (a): a COBERTURA do axiom_report no fecho inteiro. O TGL/Audit.lean termina num `run_cmd` que imprime, para TODA constante dos modulos TGL e TGLExt, o formato do
    `#print axioms`, e a linha `TGL_AXIOM_COVERAGE_TOTAL decl=N thm=M fora_do_trio=K`. Fail-closed: a linha tem de aparecer UMA vez; fora_do_trio == 0; o regex do um.py tem de ler todas as
    constantes menos as que o regex nao sabe ler (nomes com «»: contadas e iguais ao pino); e nenhum axioma lido fora do trio. NAO move o gate por si: entra no `all_verified` do kernel."""
    import re as _re
    trio_ = {"propext", "Classical.choice", "Quot.sound"}
    tots_ = _re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)\s*$", blob_)
    nao_lidas_ = len(_re.findall(r"(?m)^'[^'\n]*[\u00ab\u00bb][^'\n]*' (?:depends on axioms|does not depend on any axioms)", blob_))
    if len(tots_) != 1:
        return {"ok": False, "motivo": "LINHA_DE_COBERTURA_AUSENTE_OU_REPETIDA", "linhas": len(tots_)}
    decl_, thm_, fora_ = (int(x_) for x_ in tots_[0])
    fora_lidos_ = sorted(n_ for n_, v_ in axioms_.items() if not set(v_) <= trio_)
    lidas_ = len(axioms_)
    ok_ = bool(fora_ == 0 and not fora_lidos_ and nao_lidas_ == _V392_KH["nao_lidas"] and lidas_ >= decl_ - nao_lidas_ and decl_ >= _V392_KH["decl_minimo"])
    return {"ok": ok_, "decl": decl_, "thm": thm_, "fora_do_trio": fora_, "lidas_pelo_regex": lidas_, "nao_lidas_pelo_regex": nao_lidas_, "nao_lidas_esperadas": _V392_KH["nao_lidas"],
            "axiomas_fora_do_trio_lidos": fora_lidos_[:5], "desenho": "(a) run_cmd no Audit: fecho inteiro TGL+TGLExt"}
