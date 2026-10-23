def veredito_fase9_v2_c1(r):
    """O Teste da Unica Palavra (Fase 9 V2-c1). minimum: falsificacao; maximum: poder e discriminacao.
    z_delta e z_disc chegam CALIBRADOS (p calibrado -> z equivalente; spec calibracao_de_cauda). FALSIFIED_AT_5SIGMA = beta_TGL refutado na natureza
    (alcance do operador, 23/10/2026): a lei K = E(z*)^(2 beta/3) e a voz unica de beta_TGL na expansao; sem saida posterior. NOT_FALSIFIED nunca é a palavra da creditação."""
    import math
    from decimal import Decimal, ROUND_DOWN

    def label(x):
        if not math.isfinite(x):
            raise ValueError("non-finite verdict input")
        magnitude = Decimal(str(abs(x))).quantize(Decimal("0.1"), rounding=ROUND_DOWN)
        return ("M" if x < 0 else "P") + format(magnitude, ".1f").replace(".", "P")

    allowed_flags = {
        "r.required_sources_admitted", "r.beta_livre_no_limite", "r.use_novel_parametros"
    }

    def finite(value):
        try:
            return math.isfinite(value)
        except (OverflowError, TypeError, ValueError):
            return False

    def scan(value, path):
        if isinstance(value, bool):
            if path not in allowed_flags:
                raise ValueError("INVALID_NUMERIC_INPUT:" + path)
        elif type(value) in (int, float):
            if not finite(value):
                raise ValueError("INVALID_NUMERIC_INPUT:" + path)
        elif isinstance(value, dict):
            for key, child in value.items():
                if not isinstance(key, str):
                    raise ValueError("INVALID_INPUT_KEY:" + path)
                scan(child, path + "." + key)
        elif isinstance(value, (list, tuple)):
            for index, child in enumerate(value):
                scan(child, path + "[" + str(index) + "]")
        elif value is None or isinstance(value, str):
            return
        else:
            raise ValueError("INVALID_INPUT_TYPE:" + path)

    def number(mapping, key, path):
        value = mapping.get(key) if isinstance(mapping, dict) else None
        if type(value) not in (int, float) or not finite(value):
            raise ValueError("INVALID_NUMERIC_INPUT:" + path)
        return value

    if not isinstance(r, dict):
        raise ValueError("INVALID_INPUT_TYPE:r")
    scan(r, "r")
    for flag in ("required_sources_admitted", "beta_livre_no_limite", "use_novel_parametros"):
        if type(r.get(flag)) is not bool:
            raise ValueError("INVALID_BOOLEAN_INPUT:r." + flag)
    if not isinstance(r.get("fundo"), str) or not r["fundo"]:
        raise ValueError("INVALID_INPUT_TYPE:r.fundo")
    n_local = number(r, "n_local", "r.n_local")
    n_alvos = number(r, "n_alvos_declarados", "r.n_alvos_declarados")
    if type(n_local) is not int or n_local < 1:
        raise ValueError("INVALID_NUMERIC_INPUT:r.n_local")
    if type(n_alvos) is not int or n_alvos < 0:
        raise ValueError("INVALID_NUMERIC_INPUT:r.n_alvos_declarados")
    low, high = r.get("minimum"), r.get("maximum")
    number(low, "z_delta", "r.minimum.z_delta")
    for key in ("poder_previo", "z_disc", "lnB_lcdm", "lnB_livre", "lnB_shift",
                "lnB_fundo_livre", "poder_nao_cefeida"):
        number(high, key, "r.maximum." + key)
    pairs = low.get("sigma_z_por_alvo") if isinstance(low, dict) else None
    if not isinstance(pairs, (list, tuple)) or not pairs:
        raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo")
    for index, pair in enumerate(pairs):
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo[" + str(index) + "]")
        for field, value in enumerate(pair):
            if type(value) not in (int, float) or not finite(value):
                raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo["
                                 + str(index) + "][" + str(field) + "]")
        if pair[0] <= 0:
            raise ValueError("INVALID_NUMERIC_INPUT:r.minimum.sigma_z_por_alvo[" + str(index) + "][0]")
    endpoints_for_validation = r.get("dispersao_endpoints")
    if isinstance(endpoints_for_validation, dict):
        for name, row in endpoints_for_validation.items():
            if isinstance(row, dict):
                for key in ("chi2_por_gl", "p"):
                    if key in row:
                        value = number(row, key, "r.dispersao_endpoints." + name + "." + key)
                        if (key == "chi2_por_gl" and value < 0) or (key == "p" and not 0 <= value <= 1):
                            raise ValueError("INVALID_NUMERIC_INPUT:r.dispersao_endpoints."
                                             + name + "." + key)

    base = "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL__"
    suffix = ("__D1B__FUNDO_%s__NOT_BLIND_TO_DATA_STATED"
              "__NOT_A_CONFIRMATION__GATE_UNTOUCHED") % r["fundo"]
    if (r["n_alvos_declarados"] > 0 or not r["required_sources_admitted"]
            or r["beta_livre_no_limite"]):
        return base + "INCONCLUSIVE_SYSTEMATICS" + suffix

    if r["n_local"] > 1:
        endpoints = r.get("dispersao_endpoints")
        if not isinstance(endpoints, dict) or set(endpoints) != {"minimum", "maximum"}:
            return base + "INCONCLUSIVE_SYSTEMATICS" + suffix
        for point in ("minimum", "maximum"):
            row = endpoints[point]
            if not isinstance(row, dict) or "chi2_por_gl" not in row or "p" not in row:
                return base + "INCONCLUSIVE_SYSTEMATICS" + suffix
            chi2, p = row["chi2_por_gl"], row["p"]
            if (not isinstance(chi2, (int, float)) or not isinstance(p, (int, float))
                    or not math.isfinite(chi2) or not math.isfinite(p)
                    or chi2 < 0 or not 0 <= p <= 1):
                return base + "INCONCLUSIVE_SYSTEMATICS" + suffix
            if chi2 > 2 or p < 0.01:
                return base + "INCONCLUSIVE_SYSTEMATICS" + suffix

    low, high = r["minimum"], r["maximum"]
    zd = abs(low["z_delta"])
    if zd >= 5 or any(s <= 1 and abs(z) >= 5 for s, z in low["sigma_z_por_alvo"]):
        return base + "FALSIFIED_AT_5SIGMA" + suffix
    if zd >= 3:
        return base + "TENSION_3_TO_5_SIGMA" + suffix
    if high["poder_previo"] < 5:
        return (base + "NOT_FALSIFIED_UNDERPOWERED__POWER_%s_OF_5_SIGMA"
                % label(high["poder_previo"]) + suffix)
    if (high["z_disc"] >= 5 and high["lnB_lcdm"] >= 5
            and high["lnB_livre"] >= -1):
        token = (base + "NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_%dSIGMA"
                 "__ZERO_FREE_PARAMETERS" % int(math.floor(high["z_disc"])))
        token += "__USE_NOVEL" if r["use_novel_parametros"] else "__USE_NOVELTY_PENDING"
        token += "__VS_LADDER_SYSTEMATIC_LNB_%s__VS_FREE_BACKGROUND_LNB_%s" % (
            label(high["lnB_shift"]), label(high["lnB_fundo_livre"]))
        if high["lnB_shift"] < 0 and high["poder_nao_cefeida"] >= 5:
            token += "__NOT_DISCRIMINATED_FROM_LADDER_SYSTEMATIC"
        if abs(high["lnB_fundo_livre"]) < 1:
            token += "__NOT_DISCRIMINATED_FROM_FREE_BACKGROUND"
        return token + suffix

    token = base + "NOT_FALSIFIED_POWERED__" + (
        "DEVIATION_CONSISTENT_WITHIN_1SIGMA" if zd < 1 else "DEVIATION_1_TO_3_SIGMA")
    if high["z_disc"] < 5:
        token += "__NOT_DISCRIMINATED_FROM_LCDM_AT_AVAILABLE_SENSITIVITY"
    if high["lnB_lcdm"] < 5:
        token += "__NOT_DISCRIMINATED_FROM_LCDM_LNB_BELOW_5"
    if high["lnB_livre"] < -1:
        token += "__NOT_DISCRIMINATED_FROM_LCDM_BETA_FREE_LNB_BELOW_MINUS_1"
    return token + suffix
