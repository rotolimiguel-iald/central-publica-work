# -*- coding: utf-8 -*-
"""gerar_esperados_v398.py -- ESPERADOS_v398.json LIDOS dos artefatos (molde: gerar_esperados_v397.py): o estado SELADO da v397 pinado. A TROCA DITA: os registros da v397 cujo veredito carrega os numeros do kernel (escada,
declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam). Todos os outros vereditos da v397 ficam IGUAIS. +4 chaves novas no core (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398).
O pilar pela mesma chave. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo: os numeros dele vem do resultado pinado (v397\\insumos\\fase9) e o conferidor os confere de novo. Nada digitado: cada numero e hash vem de CANDIDATO_v398.json,
ensaio_a_seco_v398.json, do core/selo da v397 (base_v397), de kernel\\FLAGS_v398.json, de ESPERADOS_v397.json (o que o quadro pinou) e do resultado pinado."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v398.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v397_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v398.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E397 = json.load(open(os.path.join(DL.V397, "ESPERADOS_v397.json"), encoding="utf-8")); assert E397["candidato_sha16"] == CM["base_v397_sha16"]
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]
troca = sorted(mud)   # os vereditos da v397 que mudam (so' numeros), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v398.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v398.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v398.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V397 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "teste_de_veracidade_fase9_v397", "registros_v397", "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")
vr = ens["veracidade_registro"]
RESP = os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME)
res9 = json.load(open(RESP, encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
assert E397["veracidade"]["numeros_do_resultado"] == numeros9 and E397["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v397 pinou do Teste da Unica Palavra != o resultado em disco"
TS398 = "Sônico e a afinação das cordas"; TS398E = "Sonic and the tuning of the strings"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E397["quadro"]["linha_de_maquina_pt"] and mach_en == E397["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro mudou: o quadro NAO se mexe"
MARCAS397_PT = list(E397["artigo_marcas"]["pt"]); MARCAS397_EN = list(E397["artigo_marcas"]["en"])
son, afi = ens["sonico_registro"], ens["afinacao_registro"]
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v397_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v397_e_v398": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v397": V397, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v397": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v397_no_ensaio": ens["selo"]["difere_do_selo_v397"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v397": sorted(k for k, v in kf.items() if v is True), "axiom_report_v397_n": len(axr0),
       "runtime_seals_v397": core0["runtime_of_the_one"]["seals"], "what_remains_v397": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v398": {"sonico_v398": son["verdict"], "afinacao_das_cordas_v398": afi["verdict"]},
       "registros_v398": {k: v["verdict"] for k, v in mf["registros_v398"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "sonico": {"verdict": son["verdict"], "n_checks": son["n_checks"], "values": son["values"], "unconditional": son["unconditional"], "teorema": DL.STONES[0]["theorem"], "bandeira": CM["politica_de_bandeiras"]["bandeiras_do_teorema"]["sonico"]},
       "afinacao": {"verdict": afi["verdict"], "n_checks": afi["n_checks"], "values": afi["values"], "unconditional": afi["unconditional"], "hypothesis": afi["hypothesis"], "geometry": afi["geometry"], "teorema": DL.STONES[1]["theorem"],
                    "bandeira": CM["politica_de_bandeiras"]["bandeiras_do_teorema"]["afinacao"], "auxiliares_fora_da_composicao": list(DL.STONES[1]["auxiliares_fora_da_composicao"])},
       "veracidade": E397["veracidade"], "quadro": E397["quadro"],   # o QUADRO do topo (v397) e o registro do Teste da Unica Palavra: o que a v397 pinou, conferido de novo contra o resultado em disco
       "artigo_marcas": {"pt": [TS398, "Sônico.", "As falas sobre o sônico.", "Afinação das cordas.", "A fala sobre as cordas."] + MARCAS397_PT, "en": [TS398E, "Sonic.", "The sayings on the sonic stone.", "Tuning of the strings.", "The saying on the strings."] + MARCAS397_EN},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou", "Nesta rodada os registros da v398 NÃO selaram todos"], "en": ["This round the record did NOT seal", "This round the v398 records did NOT all seal"]},
       "toc": {"pt": [TS398] + list(E397["toc"]["pt"]), "en": [TS398E] + list(E397["toc"]["en"])},
       "the_iald_index_v397": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v398": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v398**", "md_sonico": "Sônico e a afinação das cordas (v398, 23/10/2026)", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)", "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v398.json")),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": dict(FJ["por_grupo_bandeiras"]), "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedras": CM["kernel"]["pedras"], "teoremas_das_pedras": {s["key"]: s["theorem"] for s in DL.STONES},
       "bandeiras_das_pedras": CM["politica_de_bandeiras"]["bandeiras_do_teorema"], "suporte_das_pedras": {s["key"]: dict(s["support"]) for s in DL.STONES},
       "contrato_das_pedras": {s["key"]: list(s["contract"]) for s in DL.STONES}, "candidato_anterior_sha16": CM["base_v397_sha16"]}
assert esp["the_iald_index_v397"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v397"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 2, "o numero de modulos novos != a lista"
assert esp["vereditos_novos_v398"]["sonico_v398"].startswith("TGL_SONICO_V398__ONE_OCTAVE_IS_THE_FAIR_BIT_LN2") and esp["vereditos_novos_v398"]["afinacao_das_cordas_v398"].startswith("TGL_AFINACAO_DAS_CORDAS_V398__CYCLIC_CLOSURE_OF_THE_BOOST_PARAMETER")
assert set(esp["selo_difere_do_v397_no_ensaio"]) >= {"sonico_v398", "afinacao_das_cordas_v398", "registros_v398", "um_version"}
assert "teste_de_veracidade_fase9_v397" not in esp["selo_difere_do_v397_no_ensaio"] and "registros_v397" not in esp["selo_difere_do_v397_no_ensaio"], "o selo do Teste da Unica Palavra mudou: o quadro NAO se mexe"
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v398.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v398:", esp["candidato_sha16"], "| vereditos v397 pinados:", len(esp["vereditos_v397"]), "| flags True v397:", len(esp["flags_true_v397"]), "| troca dita:", troca)
