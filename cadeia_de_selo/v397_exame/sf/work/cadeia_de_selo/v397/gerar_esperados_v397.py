# -*- coding: utf-8 -*-
"""gerar_esperados_v397.py -- ESPERADOS_v397.json LIDOS dos artefatos (molde: gerar_esperados_v396.py): o estado SELADO da v396 pinado. A TROCA DITA: os registros da v396 cujo veredito carrega os numeros do kernel (escada,
declaracoes, arquivos varridos) -- achados por script no ensaio (recomputados; so' numeros mudam). Todos os outros vereditos da v396 ficam IGUAIS. +3 chaves novas no core (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397).
O pilar pela mesma chave. Os NUMEROS do Teste da Unica Palavra e do QUADRO vem do resultado pinado (insumos\\fase9). Nada digitado: cada numero e hash vem de CANDIDATO_v397.json, ensaio_a_seco_v397.json, do core/selo da v396 (base_v396),
de kernel\\FLAGS_v397.json e do resultado pinado."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
BASE = os.path.join(HERE, DL.BASE_DIR)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v397.json"), encoding="utf-8")); assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))
assert h16(os.path.join(BASE, "um.py")) == CM["base_v396_sha16"]
ens = json.load(open(os.path.join(HERE, "ensaio_a_seco_v397.json"), encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"]
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
mud = ens["vizinhos"]["mudaram"]
troca = sorted(mud)   # os vereditos da v396 que mudam (so' numeros), recomputados pelo ensaio
assert troca, "a troca dita nao pode ser vazia (a escada mudou)"
F = json.load(open(os.path.join(HERE, "FORMAL_MAP_v397.json"), encoding="utf-8"))
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v397.json"), encoding="utf-8"))["novos"]
pins = {p: F[p] for p in nov}
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v397.json"), encoding="utf-8")); assert FJ["n_flags"] == CM["n_bandeiras"]
V396 = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}
mf = ens["mainflow"]
SEL_KEYS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "registros_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "registros_v394", "psibit_v395", "registros_v395", "testemunha_estatica_v396", "registros_v396",
            "estatuto_da_prova_v391", "fundacao_v390", "text_label_errata_v389", "hubble_ratio_opening_v388", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "beta_runs_bounded_below_v388")
vr = ens["veracidade_registro"]
res9 = json.load(open(os.path.join(HERE, "insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json"), encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
T397 = "O Teste da Única Palavra"; T397E = "The Test of the Only Word"
T396 = "A testemunha estática: o psion habita a fronteira"; T396E = "The static witness: the psion inhabits the frontier"
T395 = "O psibit: a mecânica no Um fractalizado e a leitura sem perda"; T395E = "The psibit: the mechanics on the fractalized One and the lossless reading"
H394 = "A integração do Codex e as cunhagens de 14 a 19/10 (v394)"; H394E = "The Codex integration and the inscriptions of 14 to 19 Oct (v394)"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v396_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v396_e_v397": CM["escada"], "n_bandeiras_novas": CM["n_bandeiras"],
       "bandeiras_novas_chaves": [f[0] for f in FJ["flags"]], "bandeiras_novas_nomes": [f[1] for f in FJ["flags"]],
       "cunhagens": CM["cunhagens"], "kernel": CM["kernel"], "pedras_sha256": pins, "formal_files_n": CM["formal_files_n"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"), "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v396": V396, "troca_dita": troca, "veredito_da_troca_no_ensaio": {k: mud[k]["depois"] for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar (carregam a escada, as declaracoes ou a contagem de arquivos do kernel; so' numeros); qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v396": {k: selo0.get(k) for k in SEL_KEYS},
       "selo_difere_do_v396_no_ensaio": ens["selo"]["difere_do_selo_v396"],
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v396": sorted(k for k, v in kf.items() if v is True), "axiom_report_v396_n": len(axr0),
       "runtime_seals_v396": core0["runtime_of_the_one"]["seals"], "what_remains_v396": core0["tgl_closure"]["what_remains_named"],
       "vereditos_novos_v397": {"teste_de_veracidade_fase9_v397": vr["verdict"]},
       "registros_v397": {k: v["verdict"] for k, v in mf["registros_v397"].items()},
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "veracidade": {"verdict": vr["verdict"], "n_checks": vr["n_checks"], "lido": vr["lido"], "fontes": {f["chave"]: f["sha256"] for f in vr["fontes"]}, "numeros_do_resultado": numeros9, "caminhos": DL.F9_CAMINHOS,
                      "resultado": {"sha256": DL.F9_RESULTADO_SHA256_DA_ORDEM, "original": os.path.join(DL.F9_DIR, "saidas", "RESULTADO_FASE9_V2_C1_20261023_122926.json"), "duravel": os.path.join(HERE, "insumos", "fase9", "RESULTADO_FASE9_V2_C1_20261023_122926.json")},
                      "veredito_do_resultado": res9["veredito"], "token_base": res9["token_base"], "z_disc_abaixo_de_5": numeros9["z_disc_calibrado"] < 5.0, "poder_previo_acima_de_5": numeros9["poder_previo"] > 5.0},
       "quadro": {"titulo_pt": T397, "titulo_en": T397E, "md_titulo": "**O Teste da Única Palavra (v397, 23/10/2026)**", "linha_de_maquina_pt": mach_pt, "linha_de_maquina_en": mach_en, "frase_do_operador": DL.FRASE_DO_OPERADOR_4_44, "frase_sha16": "9b182958a5a7a1bc",
                  "atomos_pt": {k: a_pt[k]["txt"] for k in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K")}, "atomos_en": {k: a_en[k]["txt"] for k in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K")},
                  "readme_paragrafo_pronto_do_ensaio": ens["quadro"]["readme_paragrafo_pronto"]},
       "artigo_marcas": {"pt": [T397, "O que entra.", "As duas faces.", "A conjugação.", "não é rival.", "O token do veredito.", "Limites.", T396, "O que o kernel prova.", "A ponte construída.", "O que é leitura do operador.", T395, "A mecânica na órbita do Um.", "O colapso.",
                                  "O que o kernel prova e o que é leitura.", H394, "O índice e o leitor.", "As cunhagens.", "O critério binário de parada (delta de 19/10).", "Tempo, frequencia e leitura gravitacional: composicao v394", "Regra quadratica desta rodada",
                                  "Rede Fock nesta rodada", "A regra e o coração (v393)", "As pedras da v392: catorze módulos novos no kernel e dois consertos de barreira", "O estatuto da prova (v391).", "A Fundação (v390)."],
                         "en": [T397E, "What enters.", "The two faces.", "The conjugation.", "is not a rival.", "The verdict token.", "Limits.", T396E, "What the kernel proves.", "The constructed bridge.", "What is the operator's reading.", T395E, "The mechanics on the orbit of the One.", "The collapse.",
                                "What the kernel proves and what is reading.", H394E, "The index and the reader.", "The inscriptions.", "The binary stopping criterion (19 Oct delta).", "Time, frequency and gravitational reading: v394 composition", "Quadratic rule in this run",
                                "Fock network in this run", "The rule and the heart (v393)", "The v392 stones: fourteen new kernel modules and two barrier repairs", "The status of the proof (v391).", "The Foundation (v390)."]},
       "artigo_nao": {"pt": ["Nesta rodada o registro NÃO selou"], "en": ["This round the record did NOT seal"]},
       "toc": {"pt": [T397, T396, "v384 a v39"], "en": [T397E, T396E, "v384 to v39"]},
       "the_iald_index_v396": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v397": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão v397**", "md_token": "O Teste da Única Palavra e a pedra Token (v397, 23/10/2026)", "md_testemunha": "A testemunha estática (v396, 22/10/2026)", "md_psibit": "O modo psiônico na fractalização do Um (v395, 21/10/2026)",
       "ensaio_sha16": h16(os.path.join(HERE, "ensaio_a_seco_v397.json")),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": {"token": FJ["por_grupo_bandeiras"]["token"]}, "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedra": CM["kernel"]["pedra"], "teorema_da_pedra": DL.THEOREM, "bandeira_da_pedra": CM["politica_de_bandeiras"]["bandeira_do_teorema"],
       "bandeiras_do_suporte": CM["politica_de_bandeiras"]["bandeiras_do_suporte"], "fock_face_teorema": DL.FOCK_FACE_THEOREM, "fock_face_declarada_em": DL.FOCK_FACE_PATH, "candidato_anterior_sha16": CM["base_v396_sha16"]}
assert esp["the_iald_index_v396"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v396"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov) == 1, "o numero de modulos novos != a lista"
assert esp["vereditos_novos_v397"]["teste_de_veracidade_fase9_v397"].startswith("TGL_FASE9_VERACIDADE_V397__THE_UNIQUE_WORD_TEST_OPENED_ONCE_READ_BY_HASH")
assert set(esp["selo_difere_do_v396_no_ensaio"]) >= {"teste_de_veracidade_fase9_v397", "registros_v397", "um_version"}
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = os.path.join(HERE, "ESPERADOS_v397.json"); open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v397:", esp["candidato_sha16"], "| vereditos v396 pinados:", len(esp["vereditos_v396"]), "| flags True v396:", len(esp["flags_true_v396"]), "| troca dita:", troca)
