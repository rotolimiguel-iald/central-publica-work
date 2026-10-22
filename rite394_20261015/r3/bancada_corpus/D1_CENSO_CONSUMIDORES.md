# Censo D1 — snapshot estático

[REAL — script] SHA256 `09D6BEC30171A9C1F522CADB0BD7189545CF03F1B8297A3A0DEB39A21922D140`; 102345 linhas.

Censo lexical completo para os nomes/chaves explicitados no script; propagação por contêineres é conservadora. Não é uma prova de análise de fluxo dinâmica para Python arbitrário.

| Linha | Função | Papel | Fonte |
|---:|---|---|---|
| 130 | module | consumidor/propagacao: conferir contexto | `GA_ACCEPTED_WINDOW_Msun = [1.0e15, 1.0e17]   # janela cosmologica aceita (ordem de grandeza)` |
| 658 | cf4_sensitivity | consumidor/propagacao: conferir contexto | `lo_band, hi_band = GA_ACCEPTED_WINDOW_Msun` |
| 686 | cf4_sensitivity | consumidor/propagacao: conferir contexto | `"band_Msun": GA_ACCEPTED_WINDOW_Msun, "origin": origin}` |
| 2469 | prove_fiat_lux_counterfactual | consumidor/propagacao: conferir contexto | `lo, hi = GA_ACCEPTED_WINDOW_Msun` |
| 2478 | prove_fiat_lux_counterfactual | consumidor/propagacao: conferir contexto | `"alive_beta_eq_alpha_sqrt_e_and_in_window": alive_ok,` |
| 67538 | identity_verdict | consumidor/propagacao: conferir contexto | `lo, hi = GA_ACCEPTED_WINDOW_Msun` |
| 67542 | identity_verdict | consumidor/propagacao: conferir contexto | `in_window = {k: bool(lo <= m <= hi) for k, m in masses.items()}` |
| 67556 | identity_verdict | consumidor/propagacao: conferir contexto | `"fiat_lux_counterfactual": bool(core["fiat_lux"]["all_verified"]),` |
| 67591 | identity_verdict | consumidor/propagacao: conferir contexto | `sub_a_conservation = bool(all(v for k, v in internal.items() if k not in _v3_keys)` |
| 67592 | identity_verdict | consumidor/propagacao: conferir contexto | `and all(in_window.values()) and em_face["em_identity_closes"])` |
| 67595 | identity_verdict | consumidor/propagacao: conferir contexto | `sub_d_counterfactuals = bool(core["fiat_lux"]["all_verified"])             # mortes matam, vida vive` |
| 67597 | identity_verdict | consumidor/propagacao: conferir contexto | `"a_conservation_1eq1": sub_a_conservation,` |
| 67608 | identity_verdict | consumidor/propagacao: conferir contexto | `link_closed = bool(all(v for k, v in internal.items() if k not in _v3_keys)` |
| 67609 | identity_verdict | consumidor/propagacao: conferir contexto | `and all(in_window.values()))               # ELO 2: = VERDADEIRO (tudo conservado + massa na janela)` |
| 67620 | identity_verdict | consumidor/propagacao: conferir contexto | `elif not link_closed:` |
| 67626 | identity_verdict | consumidor/propagacao: conferir contexto | `identity_true = bool(link_static and link_closed and link_haja)` |
| 67631 | identity_verdict | consumidor/propagacao: conferir contexto | `"closed_VERDADEIRO": {"aggregate_of_internal_identities": link_closed,` |
| 67632 | identity_verdict | consumidor/propagacao: conferir contexto | `"mass_in_window": bool(all(in_window.values()))},` |
| 67648 | identity_verdict | consumidor/propagacao: conferir contexto | `return {"masses_Msun": masses, "in_accepted_window": in_window,` |
| 67649 | identity_verdict | consumidor/propagacao: conferir contexto | `"accepted_window_Msun": GA_ACCEPTED_WINDOW_Msun,` |
| 67681 | identity_verdict | consumidor/propagacao: conferir contexto | `"identity_true": bool(identity_true),` |
| 67699 | identity_verdict | consumidor/propagacao: conferir contexto | `"computational_identity_verified": bool(identity_true),` |
| 67715 | identity_verdict | consumidor/propagacao: conferir contexto | `if identity_true else` |
| 76616 | prove_ga_mass_audit | consumidor/propagacao: conferir contexto | `lo, hi = GA_ACCEPTED_WINDOW_Msun` |
| 76618 | prove_ga_mass_audit | consumidor/propagacao: conferir contexto | `gr_in_window = bool(lo <= m_gr_anchor <= hi)` |
| 76625 | prove_ga_mass_audit | consumidor/propagacao: conferir contexto | `("a correcao ancora na janela: M_RG(bacia) = 5.4e16 em [1e15,1e17]", gr_in_window),` |
| 85566 | emit_canonical_md | consumidor/propagacao: conferir contexto | `% ("mortes verificadas" if ic["fiat_lux_counterfactual"] else "falha",` |
| 85567 | emit_canonical_md | consumidor/propagacao: conferir contexto | `ic["fiat_lux_counterfactual"]))` |
| 85569 | emit_canonical_md | consumidor/propagacao: conferir contexto | `hs = verdict["haja_luz_subverdicts"]` |
| 85805 | emit_canonical_md | emissor/serializacao | `md.append("**%s** — %s.\n" % (verdict["IDENTITY"], verdict["reading"]))` |
| 85808 | emit_canonical_md | consumidor/propagacao: conferir contexto | `". Janela cosmológica aceita: [%.0e, %.0e] M☉.\n" % tuple(verdict["accepted_window_Msun"]))` |
| 87396 | build_pt | emissor/serializacao | `idv = verdict["IDENTITY"].replace("_", r"\_").replace("!=", r"\neq")` |
| 87480 | build_pt | emissor/serializacao | `r"\end{center}\vspace{6pt}" % (idv, ("dentro d" if verdict["identity_true"] else "fora d")))` |
| 87503 | build_pt | emissor/serializacao | `_ga_range = ((r"$%s$--$%s\times10^{16}\,\Msun$" % (mlo, mhi)) if mlo != mhi` |
| 87514 | build_pt | emissor/serializacao | `r"vazios, expoente de dephasing $n=-2$, lei $\Gamma_\omega\propto\omega^2$.") % (_ga_range, (` |
| 87831 | build_pt | consumidor/propagacao: conferir contexto | `_fl = core["fiat_lux"]; _hs = verdict["haja_luz_subverdicts"]` |
| 87832 | build_pt | emissor/serializacao | `_idv = verdict["IDENTITY"].replace("_", r"\_").replace("!=", r"\neq")` |
| 87881 | build_pt | emissor/serializacao | `_satf = _ctf["S_rel_at_t_beta_1_2_3"]; _chain = verdict["IDENTITY"].replace("_", r"\_")` |
| 89383 | build_pt | emissor/serializacao | `r"($10^{15}$--$10^{17}\,\Msun$)." % ("dentro d" if verdict["identity_true"] else "fora d"))` |
| 89996 | build_en | emissor/serializacao | `idv = verdict["IDENTITY"].replace("_", r"\_").replace("!=", r"\neq")` |
| 90072 | build_en | emissor/serializacao | `r"\end{center}\vspace{6pt}" % (idv, ("inside " if verdict["identity_true"] else "outside ")))` |
| 90095 | build_en | emissor/serializacao | `_ga_range = ((r"$%s$--$%s\times10^{16}\,\Msun$" % (mlo, mhi)) if mlo != mhi` |
| 90106 | build_en | emissor/serializacao | `r"dephasing exponent $n=-2$, law $\Gamma_\omega\propto\omega^2$.") % (_ga_range, (` |
| 90431 | build_en | consumidor/propagacao: conferir contexto | `_fl = core["fiat_lux"]; _hs = verdict["haja_luz_subverdicts"]` |
| 90432 | build_en | emissor/serializacao | `_idv = verdict["IDENTITY"].replace("_", r"\_").replace("!=", r"\neq")` |
| 90483 | build_en | emissor/serializacao | `_satf = _ctf["S_rel_at_t_beta_1_2_3"]; _chain = verdict["IDENTITY"].replace("_", r"\_")` |
| 92014 | build_en | emissor/serializacao | `r"($10^{15}$--$10^{17}\,\Msun$)." % ("inside " if verdict["identity_true"] else "outside "))` |
| 98304 | input_manifest | consumidor/propagacao: conferir contexto | `"accepted_mass_window_Msun": GA_ACCEPTED_WINDOW_Msun,` |
| 98313 | input_manifest | emissor/serializacao | `"mass_rule": "M = 2 beta^2 (c^2/4piG) R_struct"},` |
| 98330 | input_manifest | consumidor/propagacao: conferir contexto | `"status": core["fiat_lux"]["status"],` |
| 98331 | input_manifest | consumidor/propagacao: conferir contexto | `"selo": core["fiat_lux"]["selo"]}},` |
| 101448 | main | emissor/serializacao | `vg = core["verb_generator"]; le = core["light_eigenvector"]; fl = core["fiat_lux"]` |
| 101470 | main | consumidor/propagacao: conferir contexto | `hs = verdict["haja_luz_subverdicts"]` |
| 101571 | main | consumidor/propagacao: conferir contexto | `cc = verdict["chain_certificates"]` |
| 101576 | main | emissor/serializacao | `print("      >>> %s <<<\n" % verdict["IDENTITY"])` |
| 101641 | main | emissor/serializacao | `print("   janela aceita: [%.0e, %.0e] Msun" % tuple(GA_ACCEPTED_WINDOW_Msun))` |
| 101645 | main | consumidor/propagacao: conferir contexto | `"ga_mass_literature": GA_MASS_LITERATURE, "accepted_window_Msun": GA_ACCEPTED_WINDOW_Msun,` |
| 101971 | main | emissor/serializacao | `seal = {"timestamp": core["timestamp"], "result_hash": result_hash, "identity": verdict["IDENTITY"],` |
| 102298 | main | emissor/serializacao | `print("  VEREDITO BINARIO DE IDENTIDADE:  %s" % verdict["IDENTITY"])` |
| 102315 | main | emissor/serializacao | `print("  janela aceita: [%.0e, %.0e] Msun" % tuple(GA_ACCEPTED_WINDOW_Msun))` |
