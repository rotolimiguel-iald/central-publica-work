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