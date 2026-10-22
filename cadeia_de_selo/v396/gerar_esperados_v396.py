# -*- coding: utf-8 -*-
"""gerar_esperados_v396.py -- ESPERADOS_v396.json LIDOS dos artefatos (molde: gerar_esperados_v395.py): o estado SELADO da v395 pinado. A TROCA DITA: os registros da v395 cujo veredito carrega os numeros do kernel (escada,
declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam). Todos os outros vereditos da v395 ficam IGUAIS. +3 chaves novas no core (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396).
O pilar pela mesma chave. Nada digitado: cada numero e hash vem de CANDIDATO_v396.json, ensaio_a_seco_v396.json, do core/selo da v395 (base_v395) e de kernel\\FLAGS_v396.json."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v396 as DL  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v396.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v395_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v396.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]
troca = sorted(mud)   # os vereditos da v395 que mudam (so' numeros), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v396.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v396.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v396.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V395 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "estatuto_da_prova_v391", "fundacao_v390",
            "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")
tr = ens["testemunha_registro"]
T396 = "A testemunha estática: o psion habita a fronteira"; T396E = "The static witness: the psion inhabits the frontier"
T395 = "O psibit: a mecânica no Um fractalizado e a leitura sem perda"; T395E = "The psibit: the mechanics on the fractalized One and the lossless reading"
H394 = "A integração do Codex e as cunhagens de 14 a 19/10 (v394)"; H394E = "The Codex integration and the inscriptions of 14 to 19 Oct (v394)"
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v395_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v395_e_v396": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v395": V395, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v395": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v395_no_ensaio": ens["selo"]["difere_do_selo_v395"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v395": sorted(k for k, v in kf.items() if v is True), "axiom_report_v395_n": len(axr0),
       "runtime_seals_v395": core0["runtime_of_the_one"]["seals"], "what_remains_v395": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v396": {"testemunha_estatica_v396": mf["testemunha"]["verdict"]},
       "registros_v396": {k: v["verdict"] for k, v in mf["registros_v396"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "n_formais": mf["n_formais"],
       "testemunha": {"verdict": tr["verdict"], "n_checks": tr["n_checks"], "unconditional": tr["unconditional"], "fock_face": tr["fock_face"],
                      "values": {k: tr["values"][k] for k in ("beta", "pair_idempotence_residual", "pair_trace", "pair_purity", "pair_rank1_residual", "individual_reduction_residual", "individual_idempotence_defect", "individual_purity", "individual_deficit",
                                                              "von_neumann_entropy", "ln2", "unbonded_purity_deficit", "bell_gram_residual", "bell_completeness_residual", "closed_form_residual", "eigen_residual", "line_fixed_residual", "off_line_min_move",
                                                              "global_witness_move", "limit_residual", "collapse_idempotence_residual", "collapse_identity_residual", "collapse_scalarisation_residual", "collapse_noninjectivity_input_gap", "collapse_noninjectivity_output_gap")},
                      "tolerancias": {"pair_idempotence_residual": 1e-16, "pair_rank1_residual": 1e-15, "individual_reduction_residual": 1e-16, "bell_gram_residual": 1e-15, "bell_completeness_residual": 1e-15, "closed_form_residual": 1e-15, "eigen_residual": 1e-15,
                                      "line_fixed_residual": 1e-15, "limit_residual": 1e-14, "collapse_idempotence_residual": 1e-14, "collapse_identity_residual": 1e-14, "collapse_scalarisation_residual": 1e-14, "collapse_noninjectivity_output_gap": 1e-14},
                      "teorema_incondicional": DL.THEOREM, "bandeira_incondicional": FJ["bandeira_do_teorema_incondicional"], "fock_face_teorema": DL.FOCK_FACE_THEOREM, "fock_face_declarada_em": DL.FOCK_FACE_PATH},
       "artigo_marcas": {"pt": [T396, "O que entra.", "O que o kernel prova.", "A ponte construída.", "O que é leitura do operador.", "Limites.", T395, "A mecânica na órbita do Um.", "O colapso.", "O que o kernel prova e o que é leitura.", H394, "O índice e o leitor.", "As cunhagens.",
                                  "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada", "A regra e o coração (v393)", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira",
                                  "O estatuto da prova (v391).", "A Fundação (v390)."],
                         "en": [T396E, "What enters.", "What the kernel proves.", "The constructed bridge.", "What is the operator's reading.", "Limits.", T395E, "The mechanics on the orbit of the One.", "The collapse.", "What the kernel proves and what is reading.", H394E,
                                "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run", "The rule and the heart (v393)",
                                "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou"], "en": ["This round the record did NOT seal"]},
       "toc": {"pt": [T396, T395, "v384 a v39"], "en": [T396E, T395E, "v384 to v39"]},
       "the_iald_index_v395": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v396": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v396**", "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v396.json")),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": {"testemunha_estatica": FJ["por_grupo_bandeiras"]["testemunha_estatica"]}, "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedra": CM["kernel"]["pedra"], "contrato_testemunha": CM["contrato_testemunha"], "candidato_anterior_sha16": CM["base_v395_sha16"]}
assert esp["the_iald_index_v395"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v395"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 1, "o numero de modulos novos != a lista"
assert esp["vereditos_novos_v396"]["testemunha_estatica_v396"].startswith("TGL_STATIC_WITNESS_V396__THE_PSION_INHABITS_THE_STATIC_WITNESS")
assert set(esp["selo_difere_do_v395_no_ensaio"]) >= {"testemunha_estatica_v396", "registros_v396", "um_version"}
out = os.path.join(HERE, "ESPERADOS_v396.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v396:", esp["candidato_sha16"], "| vereditos v395 pinados:", len(esp["vereditos_v395"]), "| flags True v395:", len(esp["flags_true_v395"]), "| troca dita:", troca)
