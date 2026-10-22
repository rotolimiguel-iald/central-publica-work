# -*- coding: utf-8 -*-
"""gerar_esperados_v393.py -- ESPERADOS_v393.json LIDOS dos artefatos (molde: gerar_esperados_v392.py): o estado SELADO da v392 pinado. A TROCA DITA: os registros da v392 cujo veredito carrega os numeros
do kernel (escada, declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam). Todos os outros vereditos da v392 ficam IGUAIS. +4 chaves novas
(pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393, cunhagens_regra_v393). O pilar pela mesma chave."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
if h16(os.path.join(NOS, "um.py")) != "b590c0aa80055e2a":   # o Nos ja nao e' a v392 (rito v393 em curso): a v392 SELADA vem da copia base_v392
    NOS = os.path.join(HERE, "base_v392")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v393.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, "um_v393_candidato.py"))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v392_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v393.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v392"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
troca = sorted(ens["vizinhos"]["mudaram"])   # os vereditos da v392 que mudam (so' numeros), recomputados pelo ensaio
assert troca and not ens["vizinhos"]["carregam_e_nao_recomputados"], (troca, ens["vizinhos"]["carregam_e_nao_recomputados"])
pins = {x["path"]: x["sha256"] for x in CM["pedras"]}
V392 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v392_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v392_e_v393": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins,
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v392": V392, "troca_dita": troca,
       "veredito_da_troca_no_ensaio": {k: ens["vizinhos"]["mudaram"][k]["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v392": {k: selo0.get(k) for k in ("estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")},
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v392": sorted(k for k, v in kf.items() if v is True), "axiom_report_v392_n": len(axr0),
       "runtime_seals_v392": core0["runtime_of_the_one"]["seals"], "what_remains_v392": core0["tgl_closure"]["what_remains_named"],
       "veredito_pedras_do_ensaio": ens["mainflow"]["pedras"]["verdict"], "veredito_consumidor_do_ensaio": ens["mainflow"]["consumidor"]["verdict"], "veredito_coracao_do_ensaio": ens["mainflow"]["coracao"]["verdict"],
       "registros_v393": {k: v["verdict"] for k, v in ens["mainflow"]["registros"].items()}, "cobertura_kh_n1": ens["cobertura_kh_n1"], "axiom_report_esperado_min": ens["cobertura_kh_n1"]["lidas_pelo_regex"],
       "numeros_do_consumidor": ens["mainflow"]["consumidor"]["numeros"], "replica_do_codex": ens["mainflow"]["consumidor"]["replica_do_codex"],
       "artigo_marcas": {"pt": ["A regra e o coração (v393): a regra como inadmissão", "O coração:", "O que entra.", "As quatro inscrições do operador", "A regra no consumidor real.", "O coração e o selo gravitacional.",
                                "Regra é negar tudo aquilo que não pode ser", "A regra não deve nada, a não ser a figura da verdade", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
                         "en": ["The rule and the heart (v393): the rule as the refusal", "The heart:", "What enters.", "The operator's four inscriptions", "The rule in the real consumer.", "The heart and the gravitational seal.",
                                "Regra é negar tudo aquilo que não pode ser", "A regra não deve nada, a não ser a figura da verdade", "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou"], "en": ["This round the record did NOT seal"]},
       "toc": {"pt": ["A regra e o coração (v393)", "v384 a v393"], "en": ["The rule and the heart (v393)", "v384 to v393"]},
       "the_iald_index_v392": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "md_carimbo": "**Versão v393**", "md_regra": "A regra e o coração (v393, 14/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v393.json"))}
assert esp["the_iald_index_v392"]["all_verified"] is True and esp["the_iald_index_v392"]["verdict"].startswith("THE_IALD_INDEX_IS_BUILT") and esp["not_sealed_formais"] == [], (esp["the_iald_index_v392"], esp["not_sealed_formais"])
assert esp["veredito_pedras_do_ensaio"].startswith("TGL_PEDRAS_V393__%d_NEW_KERNEL_MODULES__" % len(CM["pedras"]))
out = os.path.join(HERE, "ESPERADOS_v393.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v393:", esp["candidato_sha16"], "| vereditos v392 pinados:", len(esp["vereditos_v392"]), "| flags True v392:", len(esp["flags_true_v392"]), "| troca dita:", troca)
