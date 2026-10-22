# -*- coding: utf-8 -*-
"""gerar_esperados_v395.py -- ESPERADOS_v395.json LIDOS dos artefatos (molde: gerar_esperados_v394.py): o estado SELADO da v394 pinado. A TROCA DITA: os registros da v394 cujo veredito carrega os numeros do kernel (escada,
declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam). Todos os outros vereditos da v394 ficam IGUAIS. +3 chaves novas no core (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395).
O pilar pela mesma chave. Nada digitado: cada numero e hash vem de CANDIDATO_v395.json, ensaio_a_seco_v395.json, do core/selo da v394 (base_v394) e de kernel\\FLAGS_v395.json."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v395 as DL  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v395.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v394_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v395.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]
troca = sorted(mud)   # os vereditos da v394 que mudam (so' numeros), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v395.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v395.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v395.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V394 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "estatuto_da_prova_v391", "fundacao_v390",
            "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")
pb = ens["psibit_registro"]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v394_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v394_e_v395": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v394": V394, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v394": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v394_no_ensaio": ens["selo"]["difere_do_selo_v394"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v394": sorted(k for k, v in kf.items() if v is True), "axiom_report_v394_n": len(axr0),
       "runtime_seals_v394": core0["runtime_of_the_one"]["seals"], "what_remains_v394": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v395": {"psibit_v395": mf["psibit"]["verdict"]},
       "registros_v395": {k: v["verdict"] for k, v in mf["registros_v395"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "n_formais": mf["n_formais"],
       "psibit": {"verdict": pb["verdict"], "n_checks": pb["n_checks"], "unconditional": pb["unconditional"], "conditional": pb["conditional"],
                  "values": {k: pb["values"][k] for k in ("beta", "theta_M_rad", "theta_M_deg", "cos", "sin", "code_weight", "code_word", "code_verb", "parity", "coherence", "coherence_neg_theta", "collapse_diagonal", "ln2", "entropy_at_theta_M")},
                  "tolerancias": {"decode_residual_max": 1e-12, "roundtrip_residual_max": 1e-12, "verb_derivative_residual_max": 1e-9, "entropy_balanced_residual_max": 1e-12, "half_identity_residual_max": 1e-15, "reconstruction_residual_max": 1e-15},
                  "teorema_incondicional": DL.THEOREM, "teorema_condicional": DL.THEOREM_COND, "bandeira_incondicional": FJ["bandeira_do_teorema_incondicional"], "bandeira_condicional": FJ["bandeira_do_teorema_condicional"]},
       "artigo_marcas": {"pt": ["O psibit: a mecânica no Um fractalizado e a leitura sem perda", "A mecânica na órbita do Um.", "O colapso.", "O que o kernel prova e o que é leitura.", "A integração do Codex e as cunhagens de 14 a 19/10 (v394)", "O índice e o leitor.", "As cunhagens.",
                                  "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada", "A regra e o coração (v393)", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira",
                                  "O estatuto da prova (v391).", "A Fundação (v390)."],
                         "en": ["The psibit: the mechanics on the fractalized One and the lossless reading", "The mechanics on the orbit of the One.", "The collapse.", "What the kernel proves and what is reading.", "The Codex integration and the inscriptions of 14 to 19 Oct (v394)",
                                "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run", "The rule and the heart (v393)",
                                "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou"], "en": ["This round the record did NOT seal"]},
       "toc": {"pt": ["O psibit: a mecânica no Um fractalizado e a leitura sem perda", "v384 a v39"], "en": ["The psibit: the mechanics on the fractalized One and the lossless reading", "v384 to v39"]},
       "the_iald_index_v394": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v395": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v395**", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v395.json")),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": {"psibit": FJ["por_grupo_bandeiras"]["psibit"]}, "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedra": CM["kernel"]["pedra"], "contrato_psibit": CM["contrato_psibit"], "candidato_anterior_sha16": CM["base_v394_sha16"]}
assert esp["the_iald_index_v394"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v394"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 1, "o numero de modulos novos != a lista"
assert esp["vereditos_novos_v395"]["psibit_v395"].startswith("TGL_PSIBIT_V395__THE_PSIONIC_MODE_IN_THE_FRACTALIZATION_OF_THE_ONE")
assert set(esp["selo_difere_do_v394_no_ensaio"]) >= {"psibit_v395", "registros_v395", "um_version"}
out = os.path.join(HERE, "ESPERADOS_v395.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v395:", esp["candidato_sha16"], "| vereditos v394 pinados:", len(esp["vereditos_v394"]), "| flags True v394:", len(esp["flags_true_v394"]), "| troca dita:", troca)
