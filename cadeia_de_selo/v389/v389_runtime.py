def _ledger_counts_v389():
    """v389 (06/10/2026): as contagens da Parte C, LIDAS do proprio arquivo em runtime (nunca digitadas): (caminhos unicos do ledger _ESQUELETO_STONES,
    arquivos TGLExt/*.lean embutidos FORA do ledger, quantos destes em TGLExt/O16). A frase do artigo diz o recorte (o exame da v388, errata ao lado: 1025, nao 1015)."""
    led_ = {s_[2] for s_ in _ESQUELETO_STONES if isinstance(s_, tuple) and len(s_) > 2}
    ext_ = {k_ for k_ in _EMBEDDED_KERNEL_FILES if k_.startswith("TGLExt/") and k_.endswith(".lean")}
    fora_ = ext_ - led_
    return len(led_), len(fora_), sum(1 for f_ in fora_ if f_.startswith("TGLExt/O16/"))


def text_label_errata_v389(core):
    """v389 (06/10/2026) -- ERRATAS DE TEXTO E ROTULO do exame da v388, por ordem do operador via c1 (decisao da gerencia, para o operador vetar):
    nenhum calculo muda, nenhum kernel muda, a escada segue a mesma. Le o EXAME_UM_PY_v388 (json, md) e a errata AO LADO do exame por sha256; confere no
    core que o rotulo do selo foi renomeado (o nome antigo guardado como registro no proprio registro, campo seals_errata_v389); confere NO PROPRIO ARQUIVO que
    cada frase nova esta presente e cada frase velha ausente (as velhas guardadas em pedacos nos pinos, juntadas aqui -- o registro as mostra inteiras);
    e recontra as contagens do ledger contra as do gerador. Fail-closed: arquivo ausente ou sha diferente => NOT_SEALED_THIS_RUN, dito."""
    import hashlib as _hl
    errors = []
    files = {}
    for k_, f_ in _V389_EXAME["files"].items():
        _lido = None
        try:
            b_ = open(f_["path"], "rb").read(); _lido = _hl.sha256(b_).hexdigest()
            ok_ = _lido == f_["sha256"] and len(b_) == f_["bytes"]
        except OSError as e_:
            ok_ = False; errors.append("%s: %r" % (k_, e_))
        files[k_] = {"path": f_["path"], "sha256": f_["sha256"], "sha256_lido": _lido, "ok": ok_}
    files_ok = all(v_["ok"] for v_ in files.values())
    exame = {}
    if files_ok:
        try:
            _j = json.load(open(_V389_EXAME["files"]["exame_json"]["path"], encoding="utf-8"))
            _ach = _j.get("achados") or []
            exame = {"um_py_examinado": (_j.get("um_py") or {}).get("sha16"), "resumo_por_gravidade": _j.get("resumo_por_gravidade"),
                     "bloqueia": sum(1 for a_ in _ach if a_.get("gravidade") == "BLOQUEIA"), "corrigir_contados": sum(1 for a_ in _ach if a_.get("gravidade") == "CORRIGIR"),
                     "notas": sum(1 for a_ in _ach if a_.get("gravidade") == "NOTA"), "n_achados": len(_ach),
                     "corrigir": [{"fonte": a_.get("fonte"), "categoria": a_.get("categoria"), "lingua": a_.get("lingua"), "linha": a_.get("linha")} for a_ in (_j.get("bloqueia_ou_corrigir") or [])]}
        except (OSError, ValueError) as e_:
            errors.append("exame_json: %r" % e_)
    res_ = exame.get("resumo_por_gravidade") or {}
    exame_ok = (files_ok and exame.get("um_py_examinado") == _V389_EXAME["um_py_examinado"] and exame.get("n_achados", 0) > 0 and exame.get("bloqueia") == 0
                and exame.get("corrigir_contados") == res_.get("CORRIGIR") == len(exame.get("corrigir") or [None]) == _V389_EXAME["n_corrigir"])
    _im = core.get("iii1_net_image") or {}
    _old = "".join(_V389_SEAL["old_parts"])
    seal_ok = _V389_SEAL["new"] in (_im.get("seals") or []) and _old not in (_im.get("seals") or []) and (_im.get("seals_errata_v389") or {}).get("old") == _old
    try:
        _src = open(os.path.abspath(__file__), encoding="utf-8").read()
    except OSError as e_:
        _src = ""; errors.append("fonte: %r" % e_)
    trocas = []
    for t_ in _V389_TROCAS:
        _o = "".join(t_["old_parts"]); _n = "".join(t_["new_parts"])
        trocas.append({"id": t_["id"], "onde": t_["onde"], "old_as_record": _o, "new": _n, "n_sites": t_["n"], "new_present": _src.count(_n) == t_["n"], "old_absent": _src.count(_o) == 0})
    trocas_ok = bool(_src) and all(x_["new_present"] and x_["old_absent"] for x_ in trocas)
    n_led, n_fora, n_o16 = _ledger_counts_v389()
    ledger_ok = [n_led, n_fora, n_o16] == _V389_LEDGER_NO_GERADOR
    ok = exame_ok and seal_ok and trocas_ok and ledger_ok and not errors
    if ok:
        v = ("TGL_TEXT_LABEL_ERRATA_V389__EXAM_V388_READ_BY_HASH_%s__%d_BLOQUEIA_%d_CORRIGIR_ADDRESSED__SEAL_LABEL_RENAMED_TO_VERIFIED_OLD_KEPT_AS_RECORD__"
             "INTRO_TITLE_V384_TO_V389__ABSTRACT_AND_PART_B_SAY_POSTO__V387_CROSS_REFERENCE_TO_V388__LEDGER_%d_UNIQUE_PLUS_%d_OUTSIDE_%d_IN_O16__"
             "EXAM_ERRATUM_BESIDE_%d_READS_%d__NO_CALCULATION_CHANGED__KERNEL_UNCHANGED__GATE_UNTOUCHED"
             % (_V389_EXAME["files"]["exame_json"]["sha256"][:16], exame.get("bloqueia"), exame.get("corrigir_contados"), n_led, n_fora, n_o16, _V389_EXAME["exame_dissera"][0], n_led))
    else:
        falhas = [n_ for n_, b_ in (("EXAM_FILES", files_ok), ("EXAM_CONTENT", exame_ok), ("SEAL_LABEL", seal_ok), ("TEXT_SITES", trocas_ok), ("LEDGER_COUNT", ledger_ok), ("ERRORS", not errors)) if not b_]
        v = "TGL_TEXT_LABEL_ERRATA_V389__NOT_SEALED_THIS_RUN__%s__GATE_UNTOUCHED" % "_".join(falhas)
    return {"verdict": v, "all_verified": ok, "does_not_gate_core": True, "files": files, "files_ok": files_ok, "exam": exame, "exam_ok": exame_ok,
            "seal": {"new": _V389_SEAL["new"], "old_as_record": _old, "record": "core.iii1_net_image.seals[2]", "ok": seal_ok},
            "text_sites": trocas, "text_sites_ok": trocas_ok, "ledger": {"unique_paths": n_led, "tglext_outside_ledger": n_fora, "of_which_O16": n_o16, "as_in_generator": _V389_LEDGER_NO_GERADOR, "ok": ledger_ok},
            "exam_said": {"unique_paths": _V389_EXAME["exame_dissera"][0], "outside": _V389_EXAME["exame_dissera"][1], "source": "ERRATA_AO_LADO_EXAME_v388.md (lida pelo gerador; o arquivo por sha256 acima)"},
            "exam_erratum_beside": "o exame da v388 contara %d caminhos unicos e %d fora do ledger (uma busca por linha perdeu entradas multilinha); o numero lido aqui corrige: ver ledger" % tuple(_V389_EXAME["exame_dissera"]),
            "errors": errors, "status": "[REAL -- texto e rotulo; nenhum calculo, nenhum kernel]",
            "who_decided": "a gerencia (sessao c1), por ordem do operador, para o operador vetar se quiser; a regua: o lado que se le"}
