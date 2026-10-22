def verify_tgl_kernel_formalization():
    """v22 -- roda o kernel do Lean e sela a partir do resultado REAL. FAIL-CLOSED.

    Nunca considera `FORMAL_CHECKER_UNAVAILABLE` como sucesso. `all_verified` deste
    modulo significa: o kernel COMPILOU e a auditoria de axiomas passou -- NAO que a
    testemunha AQFT foi construida (ela permanece OPEN, por desenho)."""
    res = {
        "formal_checker": "Lean 4", "build_tool": "Lake", "toolchain_pinned": True,
        "formal_dir": FORMAL_DIR, "mode": TGL_FORMAL_MODE,
        "lean_version": None, "lake_version": None,
        "lake_build_ok": False, "audit_file_ok": False,
        "source_forbidden_tokens_absent": False, "sorryAx_absent": False,
        "trustCompiler_absent": False, "custom_TGL_axioms_absent": False,
        "sentinels_present": False,
        "specific_AQFT_witness_constructed": False,          # por desenho: OPEN
        "unconditional_type_III1_corner_proved": False,      # jamais reivindicado
        "axiom_report": {}, "formal_source_hash": None, "formal_files_sha256": {},
        "all_unconditional_targets_verified": False,
        "all_conditional_implications_verified": False,
        "all_verified": False, "verdict": "TGL_KERNEL_FORMALIZATION_FAILED",
        "not_claimed": [
            "Python did not prove any theorem; the Lean kernel did",
            "Bisognano-Wichmann / Reeh-Schlieder / type III_1 classification are KNOWN/EXTERNAL, not formalized here",
            "the finite Three-Locks corner is a finite-dimensional theorem, NOT a type III_1 proof",
            "G is a variable / measured input; it is NOT derived",
            # v304 [ERRATA -- a frase era de v23 e a v135 a superou; 6 superficies
            # publicavam a negacao de uma testemunha HABITADA (theSpecificAQFTWitness,
            # TGLExt/WedgeNet). O nao-reivindicado VERDADEIRO e a realizacao modular.
            "the MODULAR REALIZATION of the witness is not constructed "
            "(theSpecificAQFTWitness IS inhabited since v135; TGLModularRealization stays open)",
        ],
        "seals": [],
    }
    for k in _LEAN_THEOREM_FLAGS:
        res[k] = False

    # (1) arquivos formais presentes?
    need = [FORMAL_DIR, os.path.join(FORMAL_DIR, "lakefile.toml"),
            os.path.join(FORMAL_DIR, "lean-toolchain"), FORMAL_AUDIT_FILE]
    if not all(os.path.exists(p) for p in need):
        res["verdict"] = "FORMAL_CHECKER_UNAVAILABLE"
        res["reason"] = "tgl_kernel/ incompleto (lakefile.toml, lean-toolchain, TGL/Audit.lean)"
        return res
    res["audit_file_ok"] = True

    # (2) lake disponivel?
    lake = _find_lake()
    if lake is None:
        res["verdict"] = "FORMAL_CHECKER_UNAVAILABLE"
        res["reason"] = ("`lake` nao encontrado (PATH nem ~/.elan/bin). Instale elan/Lean 4, ou "
                         "aponte a variavel de ambiente TGL_LAKE para o binario.")
        return res
    res["lake_path"] = lake

    # (3) versoes
    v1 = run_process_checked([lake, "--version"], FORMAL_DIR, 120)
    res["lake_version"] = (v1["stdout"] or v1["stderr"]).strip().splitlines()[:1]
    v2 = run_process_checked([lake, "env", "lean", "--version"], FORMAL_DIR, 120)
    res["lean_version"] = (v2["stdout"] or v2["stderr"]).strip().splitlines()[:1]

    # (4) lake build   (5) auditoria
    build = run_process_checked([lake, "build"], FORMAL_DIR, 3600)
    audit = run_process_checked([lake, "env", "lean", "TGL/Audit.lean"], FORMAL_DIR, 1800)
    res["lake_build_ok"] = bool(build["returncode"] == 0)
    res["build_stdout_sha256"] = hashlib.sha256(build["stdout"].encode("utf-8")).hexdigest()
    res["build_stderr_sha256"] = hashlib.sha256(build["stderr"].encode("utf-8")).hexdigest()
    res["audit_stdout_sha256"] = hashlib.sha256(audit["stdout"].encode("utf-8")).hexdigest()
    res["build_returncode"] = build["returncode"]
    res["audit_returncode"] = audit["returncode"]
    # diagnostico persistente (olhe o byte): grava as capturas em UTF-8 ANTES de
    # parsear, com tamanhos -- se um dia a captura voltar vazia, o arquivo acusa.
    _caps = []  # v339: capturas por ETAPA (rastreabilidade); falha de escrita VISIVEL, nunca "pass"
    for _nm, _pr in (("tgl_kernel_build_capture.txt", build),
                     ("tgl_kernel_audit_capture.txt", audit)):
        _fn = _nm.replace(".txt", _CAPTURE_STAGE + ".txt")
        try:
            with open(os.path.join(OUT, _fn), "w", encoding="utf-8") as _fh:
                _fh.write("# stage: %s\n# cmd: %s\n# returncode: %s\n# len(stdout)=%d len(stderr)=%d\n"
                          "--- STDOUT ---\n%s\n--- STDERR ---\n%s\n"
                          % (_CAPTURE_STAGE or "principal", _pr["cmd"], _pr["returncode"], len(_pr["stdout"]),
                             len(_pr["stderr"]), _pr["stdout"], _pr["stderr"]))
            _caps.append(_fn)
        except OSError as _e:
            print("[captura] AVISO: nao consegui gravar %s: %r" % (_fn, _e))
    res["capture_stage"] = _CAPTURE_STAGE or "principal"
    res["capture_files"] = _caps
    res["build_capture_lens"] = {"stdout": len(build["stdout"]), "stderr": len(build["stderr"])}
    res["audit_capture_lens"] = {"stdout": len(audit["stdout"]), "stderr": len(audit["stderr"])}
    # v23.1 -- triagem: processo que rodou com captura VAZIA e' REPROVACAO, nao registro
    # (a assinatura e3b0c442... = sha256("") escondeu o bug v22 por tres rodadas)
    res["build_capture_nonempty"] = bool(build.get("capture_nonempty"))
    res["audit_capture_nonempty"] = bool(audit.get("capture_nonempty"))
    res["build_capture_sha256_full"] = build.get("capture_sha256")
    res["audit_capture_sha256_full"] = audit.get("capture_sha256")
    blob = (build["stdout"] + build["stderr"] + audit["stdout"] + audit["stderr"])

    # (6) sentinelas   (7) proibicoes   (8) axiomas customizados TGL.*
    res["sentinels_present"] = all(s in blob for s in _LEAN_SENTINELS)
    res["sorryAx_absent"] = ("sorryAx" not in blob)
    res["trustCompiler_absent"] = ("Lean.trustCompiler" not in blob)

    import re as _re
    axioms = {}
    custom = []
    for m in _re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", blob, _re.S):
        name, lst = m.group(1), [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
        axioms[name] = lst
        custom += [a for a in lst if a.startswith("TGL.") or a.startswith("TGLExt.")]
    # v162: a forma MAIS limpa que o kernel emite -- teorema sem axioma algum:
    # "does not depend on any axioms" => lista vazia, aprovado por construcao.
    for m in _re.finditer(r"'([\w.']+)' does not depend on any axioms", blob):
        axioms.setdefault(m.group(1), [])
    res["axiom_report"] = axioms
    res["axiom_coverage_v392"] = _v392_axiom_coverage(audit["stdout"] + audit["stderr"], axioms)   # v392 KH-N1 (a): o Audit termina num run_cmd que cobre TODA constante de TGL e TGLExt; a linha TOTAL vem SO do log do Audit (o lake build tambem imprime o run_cmd do TGL/Audit.lean: no blob build+audit ela aparece 2x); a cobertura entra no all_verified
    res["custom_TGL_axioms_absent"] = (len(custom) == 0)
    res["custom_TGL_axioms_found"] = sorted(set(custom))

    for flag, thm in _LEAN_THEOREM_FLAGS.items():
        ax = axioms.get(thm)
        res[flag] = bool(res["lake_build_ok"] and ax is not None
                         and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                         and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))
    # v99: leituras do certificado de fechamento (nomes futuros; ausencia => False)
    for flag, thm in _QG_CERTIFICATE_FLAGS.items():
        ax = axioms.get(thm)
        res["qgc_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))
    # v200 [FASE 0]: leituras das flags de FRONTEIRA (mesma mecanica; nomes
    # reservados inexistentes => False por construcao — estritamente mais fechado
    # que os literais Python que estas leituras substituem)
    for flag, thm in _QG_FRONTIER_FLAGS.items():
        ax = axioms.get(thm)
        res["qgf_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))
    # v133: leituras dos certificados de FISICA (mesma mecanica fail-closed)
    for flag, thm in _QG_PHYSICS_FLAGS.items():
        ax = axioms.get(thm)
        res["qgp_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))

    # v220: leitura do PRECO DA PROVA (ausencia => item da divida ABERTO)
    for flag, thm in _GRAVITY_PRICE_FLAGS.items():
        ax = axioms.get(thm)
        res["gpf_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))

    # v253: leitura da PONTE de importacao (mesma mecanica fail-closed). Isto NAO
    # acende bandeira de kernel: quitar por importacao e outro MODO, e o razonete
    # em prove_the_mode_of_discharge os mantem separados por construcao.
    for flag, thm in _REDUCTION_FLAGS.items():
        ax = axioms.get(thm)
        res["red_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))

    for flag, thm in _GRAVITY_IMPORT_FLAGS.items():
        ax = axioms.get(thm)
        res["gpi_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))
    # v373: a classe «quitado por citacao» (gpc_) -- lida pelo MESMO mecanismo; NAO acende gpf_ nem gpi_
    for flag, thm in _GRAVITY_CITATION_FLAGS.items():
        ax = axioms.get(thm)
        res["gpc_" + flag] = bool(res["lake_build_ok"] and ax is not None
                                  and "sorryAx" not in ax and "Lean.trustCompiler" not in ax
                                  and not any(a.startswith("TGL.") or a.startswith("TGLExt.") for a in ax))

    # (9) varredura lexical auxiliar
    hits = _lean_source_forbidden_tokens()
    res["source_forbidden_tokens_absent"] = (len(hits) == 0)
    res["source_forbidden_tokens_found"] = hits

    # (10) hashes dos fontes formais
    hd = sha256_directory(FORMAL_DIR)
    res["formal_source_hash"] = hd["aggregate"]
    res["formal_files_sha256"] = hd["files"]

    # (11) vereditos
    uncond = ["half_nat_kernel_proved", "area_scale_kernel_proved",
              "finite_three_locks_kernel_proved", "finite_corner_projection_kernel_proved",
              "finite_corner_trace_kernel_proved"]
    res["all_unconditional_targets_verified"] = all(res[k] for k in uncond)
    res["all_conditional_implications_verified"] = bool(res["continuous_corner_implication_kernel_proved"])
    ok = bool(res["lake_build_ok"] and res["audit_returncode"] == 0 and res["sentinels_present"]
              and res["sorryAx_absent"] and res["trustCompiler_absent"]
              and res["custom_TGL_axioms_absent"] and res["source_forbidden_tokens_absent"]
              and res["all_unconditional_targets_verified"]
              and res["all_conditional_implications_verified"]
              and res["build_capture_nonempty"] and res["audit_capture_nonempty"]  # v23.1: captura vazia REPROVA
              and res["axiom_coverage_v392"]["ok"])   # v392 KH-N1 (a): cobertura do fecho inteiro, nada fora do trio
    res["all_verified"] = ok
    # v135: a testemunha AQFT especifica LIDA do kernel (mecanica v99: nome
    # ausente => False; jamais declarada) -- a rede das cunhas (WedgeNet)
    _ax_saw = axioms.get("TGLExt.theSpecificAQFTWitness")
    res["specific_AQFT_witness_constructed"] = bool(
        res["lake_build_ok"] and _ax_saw is not None
        and "sorryAx" not in _ax_saw and "Lean.trustCompiler" not in _ax_saw
        and not any(a.startswith("TGL.") or a.startswith("TGLExt.")
                    for a in _ax_saw))
    res["verdict"] = (("TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_CONSTRUCTED"
                       if res["specific_AQFT_witness_constructed"] else
                       "TGL_KERNEL_STAGE1_VERIFIED__SPECIFIC_AQFT_WITNESS_OPEN") if ok
                      else "TGL_KERNEL_FORMALIZATION_FAILED")
    res["formal_release_ready"] = bool(ok and TGL_FORMAL_MODE == "strict")
    # v304 [ERRATA]: o teorema "exists W" FOI PAGO na v135 (o W existe e se chama
    # theSpecificAQFTWitness). O aberto verdadeiro e a realizacao modular.
    res["open_theorem"] = ("TGL_MODULAR_REALIZATION_THEOREM: TGLModularRealization (theSpecificAQFTWitness) "
                           "-- o habitante existe (v135); a realizacao modular e o aberto")
    res["seals"] = ["LEAN_KERNEL_CHECKED", "LAKE_BUILD_REPRODUCIBLE", "NO_SORRY_AX",
                    "NO_TRUST_COMPILER", "NO_CUSTOM_TGL_AXIOMS",
                    "HALF_NAT_KERNEL_PROVED", "AREA_SCALE_EQUIVALENCE_KERNEL_PROVED",
                    "FINITE_THREE_LOCKS_CORNER_KERNEL_PROVED",
                    "NORMALIZED_FINITE_CORNER_TRACE_KERNEL_PROVED",
                    "EQUAL_CONJUGATE_FACES_HAVE_HALF_TRACE_KERNEL_PROVED",
                    "CONTINUOUS_CORNER_IMPLICATION_KERNEL_PROVED",
                    "SPECIFIC_AQFT_WITNESS_INHABITED__MODULAR_REALIZATION_REMAINS_OPEN"] if ok else ["TGL_KERNEL_FORMALIZATION_FAILED"]
    return finalize_v350_modular_frontier(res)