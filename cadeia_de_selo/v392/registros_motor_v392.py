def _v392_sha256_bytes(b_):
    import hashlib as _hl
    return _hl.sha256(b_).hexdigest()


def _v392_caminho(obj_, caminho_):
    """v392 -- le um caminho (lista de chaves str / indices int) num dict/lista aninhado. Devolve (achou, valor). Nunca levanta."""
    cur_ = obj_
    for k_ in caminho_:
        try:
            if isinstance(cur_, dict):
                if k_ not in cur_:
                    return False, None
                cur_ = cur_[k_]
            elif isinstance(cur_, (list, tuple)) and isinstance(k_, int):
                cur_ = cur_[k_]
            else:
                return False, None
        except Exception:   # noqa: BLE001
            return False, None
    return True, cur_


def _v392_fonte_bytes(chave_):
    """v392 -- le o arquivo-fonte PINADO (sha256 e bytes calculados por script na geracao do candidato; nunca de memoria). Fail-closed: ausente ou diferente => (False, motivo, None)."""
    f_ = _V392_FONTES.get(chave_)
    if f_ is None:
        return False, "FONTE_NAO_PINADA", None
    try:
        b_ = open(f_["arquivo"], "rb").read()
    except OSError as e_:
        return False, "FONTE_AUSENTE:%s" % type(e_).__name__, None
    if _v392_sha256_bytes(b_) != f_["sha256"] or len(b_) != f_["bytes"]:
        return False, "FONTE_ALTERADA", None
    return True, "ok", b_


def _v392_beta_runtime():
    """v392 -- beta calculado NESTE rito: SEALED_CODATA_ALPHA (alfa CODATA 2018 do proprio um.py) x sqrt(e). Nunca literal."""
    import math as _mt
    return globals()["SEALED_CODATA_ALPHA"] * _mt.sqrt(_mt.e)


def _v392_op(op_, lido_, esperado_):
    if op_ in ("perto_de_beta_runtime", "maior_igual_beta_runtime"):
        # `esperado_` = tolerancia RELATIVA declarada; o alvo e' o beta calculado neste rito (alfa CODATA x sqrt(e)); bool nao e' numero.
        if not isinstance(lido_, (int, float)) or isinstance(lido_, bool) or not isinstance(esperado_, (int, float)):
            return False
        b_ = _v392_beta_runtime()
        if op_ == "perto_de_beta_runtime":
            return abs(lido_ - b_) <= abs(b_) * esperado_
        return lido_ >= b_ * (1.0 - esperado_)
    if op_ == "existe":
        return True
    if op_ == "igual":
        return lido_ == esperado_
    if op_ == "diferente":
        return lido_ != esperado_
    if op_ == "contem":
        return esperado_ in str(lido_)
    if op_ == "nao_contem":
        return esperado_ not in str(lido_)
    if op_ == "comeca":
        return str(lido_).startswith(esperado_)
    if op_ == "maior_igual":
        return isinstance(lido_, (int, float)) and not isinstance(lido_, bool) and lido_ >= esperado_
    if op_ == "menor_igual":
        return isinstance(lido_, (int, float)) and not isinstance(lido_, bool) and lido_ <= esperado_
    if op_ == "em":
        return lido_ in esperado_
    if op_ == "verdadeiro":
        return lido_ is True
    if op_ == "falso":
        return lido_ is False
    if op_ == "tamanho_igual":
        return hasattr(lido_, "__len__") and len(lido_) == esperado_
    if op_ == "tamanho_maior_igual":
        return hasattr(lido_, "__len__") and len(lido_) >= esperado_
    return False


def _v392_registro(spec_, core_):
    """v392 -- O MOTOR DOS REGISTROS (13/10/2026): interpreta um `spec` (dados) e devolve o registro. Fail-closed em cada elo, sem excecao silenciosa:
      fontes     : chaves de _V392_FONTES; cada arquivo e' relido e o sha256/bytes conferidos (ausente/alterado => NOT_SEALED_THIS_RUN);
      verbatins  : chaves de _V392_VERBATINS2 (texto EMBUTIDO + sha256 + trechos que TEM de estar nele) -- a fala do operador manda, o arquivo so' informativo;
      kernel     : bandeiras ext_* que tem de ser True e declaracoes que tem de estar no axiom_report dentro do trio (lidas do kernel do PROPRIO rito);
      checks     : leituras (onde = core | kf | fonte:<chave> (JSON) ; caminho ; op ; valor ; capturar) -- cada uma tem de passar;
      texto      : erratas, limites, diz/nao_diz -- passam pela guarda P18 de texto (as cinco regras) a cada rito.
    NAO move o gate (does_not_gate_core). Validade no kernel nao e' creditacao."""
    import json as _json
    nome_ = spec_["nome"]; falhas_ = []; lido_ = {}; fontes_ = []; vbs_ = {}
    for ch_ in spec_.get("fontes", []):
        ok_, det_, _b = _v392_fonte_bytes(ch_)
        f_ = _V392_FONTES.get(ch_, {})
        fontes_.append({"chave": ch_, "sha256": f_.get("sha256"), "bytes": f_.get("bytes"), "papel": f_.get("papel"), "ok": ok_, "detalhe": det_})
        if not ok_:
            falhas_.append("FONTE_" + ch_)
    for ch_ in spec_.get("verbatins", []):
        v_ = _V392_VERBATINS2.get(ch_)
        if v_ is None:
            falhas_.append("VERBATIM_NAO_PINADO_" + ch_); continue
        ok_ = _v392_sha256_bytes(v_["text"].encode("utf-8")) == v_["sha256"] and all(t_ in v_["text"] for t_ in v_["trechos"])
        try:
            disco_ = _v392_sha256_bytes(open(v_["arquivo"], "rb").read()) == v_["sha256"]
        except OSError:
            disco_ = None
        vbs_[ch_] = {"sha256": v_["sha256"], "embedded_ok": ok_, "disk_informative_only": disco_, "trechos": v_["trechos"], "quando": v_.get("quando")}
        if not ok_:
            falhas_.append("VERBATIM_" + ch_)
    kf_ = (core_.get("kernel_formalization") or {}); axr_ = kf_.get("axiom_report") or {}; trio_ = {"propext", "Classical.choice", "Quot.sound"}
    fl_ = spec_.get("kernel_flags", []); dc_ = spec_.get("kernel_decls", [])
    fl_ok_ = sum(1 for f_ in fl_ if kf_.get(f_) is True); dc_ok_ = sum(1 for n_ in dc_ if n_ in axr_ and set(axr_[n_] or []) <= trio_)
    if fl_ok_ != len(fl_):
        falhas_.append("KERNEL_BANDEIRAS")
    if dc_ok_ != len(dc_):
        falhas_.append("KERNEL_DECLARACOES")
    checks_ = []
    for ck_ in spec_.get("checks", []):
        onde_ = ck_["onde"]; fonte_json_ = None
        if onde_ == "core":
            raiz_ = core_
        elif onde_ == "kf":
            raiz_ = kf_
        elif onde_.startswith("fonte:"):
            ok_, det_, b_ = _v392_fonte_bytes(onde_.split(":", 1)[1])
            try:
                raiz_ = _json.loads(b_.decode("utf-8")) if ok_ else None
            except Exception:   # noqa: BLE001
                raiz_ = None; ok_ = False
            if not ok_:
                checks_.append({"descricao": ck_["descricao"], "ok": False, "motivo": "FONTE_ILEGIVEL"}); falhas_.append("CHECK_" + ck_.get("id", "?")); continue
        else:
            checks_.append({"descricao": ck_["descricao"], "ok": False, "motivo": "ONDE_DESCONHECIDO"}); falhas_.append("CHECK_" + ck_.get("id", "?")); continue
        achou_, val_ = _v392_caminho(raiz_, ck_["caminho"])
        ok_ = bool(achou_ and _v392_op(ck_["op"], val_, ck_.get("valor")))
        if ck_.get("capturar") and achou_:
            c_ = val_
            if isinstance(c_, str) and len(c_) > 400:
                c_ = c_[:400] + "..."
            if isinstance(c_, (dict, list)):
                c_ = _json.dumps(c_, ensure_ascii=False)[:400]
            lido_[ck_["capturar"]] = c_
        checks_.append({"descricao": ck_["descricao"], "ok": ok_, "estatuto": ck_.get("estatuto")})
        if not ok_:
            falhas_.append("CHECK_" + ck_.get("id", "?"))
    corpo_ = {"erratas": spec_.get("erratas", []), "limites": spec_.get("limites", []), "diz": spec_.get("diz", []), "nao_diz": spec_.get("nao_diz", []), "leituras_do_operador": spec_.get("leituras_do_operador", []),
              "extras": spec_.get("extras", {})}
    viol_ = _v392_guarda_texto(_json.dumps(corpo_, ensure_ascii=False)) if not spec_.get("sem_guarda") else []
    if viol_:
        falhas_.append("GUARDA_P18")
    ok_total_ = not falhas_
    verdict_ = (spec_["veredito_prefixo"] + "__" + spec_["veredito_sufixo"]) if ok_total_ else \
        ("%s__NOT_SEALED_THIS_RUN__%s__GATE_UNMOVED" % (spec_["veredito_prefixo"], "_".join(falhas_)[:300]))
    out_ = {"verdict": verdict_, "all_verified": ok_total_, "does_not_gate_core": True, "registro": nome_, "estatuto": spec_.get("estatuto", "[REAL -- fontes e kernel lidos a cada rito; INPUT/ONTO as leituras do operador]"),
            "fontes": fontes_, "verbatim": vbs_, "kernel": {"bandeiras": [fl_ok_, len(fl_)], "declaracoes_no_trio": [dc_ok_, len(dc_)]}, "checks": checks_, "lido": lido_,
            "guarda_p18_violacoes": viol_[:5]}
    out_.update(corpo_)
    return out_


def _v392_rodar_registros(core_):
    """v392 -- roda todos os registros por spec, em ordem; excecao vira AVISO visivel (all_verified False), nunca derruba o rito. Cada chave nova do core = o nome do spec."""
    for spec_ in _V392_SPECS:
        try:
            core_[spec_["nome"]] = _v392_registro(spec_, core_)
        except Exception as e_:   # noqa: BLE001
            core_[spec_["nome"]] = {"verdict": "%s__NOT_RECORDED_THIS_RUN__RUNTIME_ERROR__GATE_UNMOVED" % spec_["veredito_prefixo"], "all_verified": False, "error": repr(e_)[:400], "does_not_gate_core": True}
    return [s_["nome"] for s_ in _V392_SPECS]
