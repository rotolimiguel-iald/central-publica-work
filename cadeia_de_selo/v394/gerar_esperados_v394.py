# -*- coding: utf-8 -*-
"""gerar_esperados_v394.py -- ESPERADOS_v394.json LIDOS dos artefatos (molde: gerar_esperados_v393.py): o estado SELADO da v393 pinado. A TROCA DITA: os registros da v393 cujo veredito carrega os numeros do kernel
(escada, declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam) -- e a MUDANCA NAO NUMERICA DECLARADA do indice (o veredito do indice qualificado, do Codex, substitui o da v393).
Todos os outros vereditos da v393 ficam IGUAIS. +5 chaves novas no core (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394). O pilar pela mesma chave."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402   (DELTA 19/10: candidato novo, kernel_d19)
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
if h16(os.path.join(NOS, "um.py")) != "18be2ddb06c60f90":   # o Nos ja nao e' a v393 (rito v394 em curso): a v393 SELADA vem da copia base_v393
    NOS = os.path.join(HERE, "base_v393")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v394.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v393_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v394.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v393"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]
IX = "the_iald_index"
troca = sorted(k for k in mud if k != IX)   # os vereditos da v393 que mudam (so' numeros), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v394.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v394.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V393 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v393_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v393_e_v394": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v393": V393, "troca_dita": troca,
       "veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca},
       "mudanca_nao_numerica_declarada": {IX: {"antes": V(IX)[:200], "depois": ens["indice_da_iald"]["verdict"], "motivo": "o indice qualificado pelo compilador (Codex, R3 a R8) substitui a lista de nomes ambiguos congelados"}},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros) e o veredito do indice (mudanca declarada); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v393": {k: selo0.get(k) for k in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")},
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v393": sorted(k for k, v in kf.items() if v is True), "axiom_report_v393_n": len(axr0),
       "runtime_seals_v393": core0["runtime_of_the_one"]["seals"], "what_remains_v393": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v394": {"tempo_frequencia_v394": mf["tempo"]["verdict"], "regra_quadratica_v394": mf["quadratica"]["verdict"], "rede_fock_v394": mf["rede"]["verdict"]},
       "registros_v394": {k: v["verdict"] for k, v in mf["registros_v394"].items()}, "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "n_formais": mf["n_formais"],
       "artigo_marcas": {"pt": ["A integração do Codex e as cunhagens de 14 a 19/10 (v394)", "O que entra.", "O índice e o leitor.", "As cunhagens.", "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada", "Rede Fock nesta rodada",
                                "A regra e o coração (v393)", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
                         "en": ["The Codex integration and the inscriptions of 14 to 19 Oct (v394)", "What enters.", "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run", "Fock network in this run",
                                "The rule and the heart (v393)", "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou"], "en": ["This round the record did NOT seal"]},
       "toc": {"pt": ["A integração do Codex e as cunhagens de 14 a 19/10 (v394)", "v384 a v39"], "en": ["The Codex integration and the inscriptions of 14 to 19 Oct (v394)", "v384 to v39"]},
       "the_iald_index_v393": {"all_verified": (core0.get(IX) or {}).get("all_verified"), "verdict": V(IX)}, "the_iald_index_v394": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v394**", "md_integracao": "A integração do Codex e as cunhagens (v394, 19/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v394.json"))}
esp.update({"troca_de_palavra": ens["vizinhos"].get("palavra_trocada") or {},   # a TROCA DE PALAVRA declarada (THEOREMS -> FLAGS): so' o que o ensaio mediu; o conferidor a aplica ao veredito da v393 antes de comparar
            "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
            "n_bandeiras_por_grupo": {"tempo": FJ["por_grupo_bandeiras"]["tempo"], "quadratica": FJ["por_grupo_bandeiras"]["quadratica"], "rede": FJ["por_grupo_bandeiras"]["rede"], "outros": FJ["por_grupo_bandeiras"]["outro"]},
            "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedra_do_delta": CM["kernel"]["pedra_do_delta"], "teorema_do_delta": DL.THEOREM, "bandeira_do_delta": DL.FLAG_KEY,
            "criterio_binario": ens["criterio_binario"], "candidato_anterior_sha16": DL.CANDIDATO_ANTERIOR_SHA16})
assert esp["the_iald_index_v393"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v393"], esp["not_sealed_formais"])
assert set(esp["troca_de_palavra"]) <= set(esp["troca_dita"]) and esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov), "o numero de modulos novos != a lista"
assert esp["vereditos_novos_v394"]["tempo_frequencia_v394"].startswith("TGL_TIME_FREQUENCY_V394__DERIVED_M2") and esp["vereditos_novos_v394"]["rede_fock_v394"].startswith("TGL_FOCK_NETWORK_V394__DERIVED_COMPONENTS")
out = os.path.join(HERE, "ESPERADOS_v394.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v394:", esp["candidato_sha16"], "| vereditos v393 pinados:", len(esp["vereditos_v393"]), "| flags True v393:", len(esp["flags_true_v393"]), "| troca dita:", troca, "| mudanca declarada:", list(esp["mudanca_nao_numerica_declarada"]))
