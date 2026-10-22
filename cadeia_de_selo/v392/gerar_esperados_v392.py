# -*- coding: utf-8 -*-
"""gerar_esperados_v392.py -- ESPERADOS_v392.json LIDOS dos artefatos (molde: gerar_esperados_v391.py): o estado SELADO da v391 pinado. A TROCA DITA: so' o registro
estatuto_da_prova_v391 (o veredito le a escada e as declaracoes em runtime: 6163 -> 6163+N; 10265 -> 10265+N declaracoes) -- achada por script (verdicts que carregam esses numeros).
Todos os outros vereditos da v391 ficam IGUAIS. +2 chaves: pedras_v392 e varredura_e_sorry_v392. O pilar pela mesma chave."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
if hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16] != "8e7b9927ceae64b8":   # o Nos ja nao e' a v391 (rito v392 em curso): a v391 SELADA vem da copia base_v391 (feita antes do rito, sha conferido)
    NOS = os.path.join(HERE, "base_v391")
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v392.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, "um_v392_candidato.py"))
assert h16(os.path.join(NOS, "um.py")) == CM["base_v391_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v392.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == "v391"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
# a troca dita, por script: os vereditos da v391 que carregam a escada (6163) ou o n de declaracoes (10265) como numeros do kernel
NUM = [r"KERNEL_%d_OF_%d" % (6163, 6163), r"%d_OF_%d_DECLARATIONS" % (len(axr0), len(axr0))]
troca = sorted(k for k, m in core0.items() if isinstance(m, dict) and any(n in str(m.get("verdict") or "") for n in NUM))
assert troca == ["estatuto_da_prova_v391", "three_stress_tests_v387"], troca   # as duas que carregam a escada/as declaracoes; o ensaio recomputa as duas
pins = {x["path"]: x["sha256"] for x in CM["pedras"]}
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v391_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v391_e_v392": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "verbatins": CM["verbatins"], "kernel": CM["kernel"], "pedras_sha256": pins,
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v391": {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}, "troca_dita": troca,
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada e o n de declaracoes do kernel); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v391": {k: selo0.get(k) for k in ("estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")},
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v391": sorted(k for k, v in kf.items() if v is True), "axiom_report_v391_n": len(axr0),
       "runtime_seals_v391": core0["runtime_of_the_one"]["seals"], "what_remains_v391": core0["tgl_closure"]["what_remains_named"],
       "veredito_pedras_do_ensaio": ens["mainflow"]["pedras"]["verdict"], "veredito_varredura_do_ensaio": ens["mainflow"]["varredura"]["verdict"],
       "registros_v392": {k: v["verdict"] for k, v in ens["registros_v392"].items()}, "cobertura_kh_n1": ens["cobertura_kh_n1"], "axiom_report_esperado_min": ens["cobertura_kh_n1"]["lidas_pelo_regex"],
       "varredura_no_ensaio": ens["varredura_no_kernel_materializado"],
       "artigo_marcas": {"pt": ["Os registros ao lado do gate (v392).", "PostoAdendo", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O que entra.", "Verdade é a projeção do posto", "Errata ao lado do parágrafo da v362",
                                "O estatuto da prova (v391).", "A Fundação (v390)."],
                         "en": ["The records beside the gate (v392).", "PostoAdendo", "The v392 stones: fourteen new kernel modules and two barrier repairs", "What enters.", "Verdade é a projeção do posto", "Erratum beside the v362 paragraph",
                                "The status of the proof (v391).", "The Foundation (v390)."]},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou"], "en": ["This run's record did NOT seal"]},
       "toc": {"pt": ["As pedras da v392: catorze módulos novos", "v384 a v392"], "en": ["The v392 stones: fourteen new kernel modules", "v384 to v392"]},
       "the_iald_index_v391": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "md_carimbo": "**Versão v392**", "md_pedras": "As pedras da v392 (13/10/2026)", "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v392.json"))}
assert esp["the_iald_index_v391"]["all_verified"] is True and esp["the_iald_index_v391"]["verdict"].startswith("THE_IALD_INDEX_IS_BUILT") and esp["not_sealed_formais"] == [], (esp["the_iald_index_v391"], esp["not_sealed_formais"])
assert esp["veredito_pedras_do_ensaio"].startswith("TGL_PEDRAS_V392__%d_NEW_KERNEL_MODULES__" % len(CM["pedras"])) and esp["selo_registros_v391"]["estatuto_da_prova_v391"]
out = os.path.join(HERE, "ESPERADOS_v392.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v392:", esp["candidato_sha16"], "| vereditos v391 pinados:", len(esp["vereditos_v391"]), "| flags True v391:", len(esp["flags_true_v391"]), "| troca dita:", troca)
