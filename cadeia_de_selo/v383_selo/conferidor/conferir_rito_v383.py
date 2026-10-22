# -*- coding: utf-8 -*-
"""conferir_rito_v383.py -- confere, DEPOIS do rito v383, o que tinha de mudar e o que NAO podia mudar. Esperados LIDOS de ESPERADOS_v383.json.
SO LEITURA do Nos. A guarda de palavra proibida e a MESMA do rito. Contra o selo da v382 que esta no Nos (controle): REPROVA 'deve mudar', APROVA 'nao pode mudar'."""
import hashlib, json, os, re, sys
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
HERE = os.path.dirname(os.path.abspath(__file__))
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v383.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
qg = core.get("qg_closure") or {}
fr = (qg.get("gate") or {}).get("kernel_frontier") or {}
n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
nst = selo.get("not_sealed_this_run") or {}
ns_ver = {k: V(k) for k, m in core.items() if isinstance(m, dict) and "verdict" in m}
FL = [f for f, _ in ESP["bandeiras"]]
FE = ESP["kernel_frontier_v381"]
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")


def arq16(rel):
    p = os.path.join(NOS, "tgl_kernel", *rel.split("/"))
    return hashlib.sha256(open(p, "r", encoding="utf-8", newline="").read().encode("utf-8")).hexdigest()[:16] if os.path.exists(p) else None


def md(nome):
    p = os.path.join(NOS, nome)
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""


esc = core.get("external_ladder") or {}
novos = ESP["kernel"]["new"]; mud = ESP["kernel"]["changed"]
ix = core.get("the_iald_index") or {}
fc = md("um_absoluto_forma_canonica.md"); mf = md("um_absoluto_manifest.md")
lc = core.get("the_ledger_of_charges_v383") or {}; rt = lc.get("runtime") or {}; pr = lc.get("preregistration") or {}
pred = (core.get("coma_distance_dephasing") or {}).get("prediction") or {}
DEVE_MUDAR = {
    "um.py = o candidato aplicado (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "as %d bandeiras ext_loc_/ext_psv_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 32,
    "escada %d/%d (v381 %d + %d)" % (ESP["escada_esperada_v383"], ESP["escada_esperada_v383"], ESP["escada_v381"][0], len(FL)):
        esc.get("n_theorems_clean") == ESP["escada_esperada_v383"] == esc.get("n_theorems_expected"),
    "axiom_report >= o do sandbox (%d)" % ESP["axiom_report_sandbox"]: len(kf.get("axiom_report") or {}) >= ESP["axiom_report_sandbox"],
    "os 2 arquivos NOVOS do kernel materializados com os sha16 do candidato": all(arq16(k) == v for k, v in novos.items()) and len(novos) == 2,
    "os %d arquivos ALTERADOS do kernel (raiz, Audit) com os sha16 novos" % len(mud): all(arq16(k) == v[1] for k, v in mud.items()),
    "selo: a leitura the_ledger_of_charges_reading_v383 presente e um_version = v383": "the_ledger_of_charges_reading_v383" in selo and selo.get("um_version") == "v383",
    "O LIVRO DE COBRANCAS: TESTES -- beta do core = alpha.sqrt(e) (1e-9 rel.); o pre-registro V1.4 lido por hash (JSON e MD = os do gerador; 11 cobrancas); as 11 cobrancas com o desfecho lido pelo modo dito (token / numero com regra / declarado) e iguais ao pre-registro; todas as chaves com token no veredito do core; 0 FALSIFIED no livro, >= 1 EXCLUDED_IN_READING, >= 1 AWAITING; as 9 ROTAS do eco FORA do livro (estado lido do rotulo da Fase 6, igual ao V1.4; 5 excluidas pelos dados, 4 inconclusivas; as fontes do motivo no core; a base v381); R2 sem poder em numero (Gamma(100 Hz) < 1e-30 s^-1); o nome do degrau final lido do fonte = o proposto; o gate inalterado; IDENTIDADES DE SANIDADE (nao testes) -- cos^2 theta_M = 1 - beta, sin^2 theta_M = beta, e^{-beta} + complemento = 1":
        rt.get("beta_core") is not None and abs(float(rt["law_alpha_sqrt_e"]) / float(core["beta"]) - 1.0) < 1e-9 and pr.get("read_ok") is True and pr.get("n_cobrancas") == 11
        and pr.get("sha256_read") == ESP["preregistro_sha256"] and len(lc.get("ledger") or []) == 11 and all(c.get("outcome_ok") and c.get("matches_preregistration") for c in (lc.get("ledger") or []))
        and lc.get("n_token_in_core") == lc.get("n_with_core_key") == 10 and sum((lc.get("by_how") or {}).values()) == 11 and (lc.get("counts") or {}).get("FALSIFIED", 1) == 0
        and (lc.get("counts") or {}).get("EXCLUDED_IN_READING", 0) >= 1 and (lc.get("counts") or {}).get("AWAITING", 0) >= 1
        and (lambda er: er.get("n") == 9 and er.get("excluded_by_data", 0) + er.get("inconclusive", 0) == 9 and er.get("not_charges_of_the_theory") is True and er.get("sources_in_core_ok") is True
             and all(r.get("state_ok") and r.get("matches_preregistration") and r.get("not_a_charge") is True for r in (er.get("routes") or [])) and len(er.get("routes") or []) == 9)(lc.get("echo_routes_outside_the_ledger") or {})
        and (lc.get("base_and_local_seal") or {}).get("base") == "v381" and (lc.get("base_and_local_seal") or {}).get("v382_local_only_sha16") == ESP["v382_so_local_sha16"]
        and 0.0 < float(rt["R2_gamma_100hz_per_s"]) < 1e-30 and lc.get("final_step_name_from_source") == lc.get("final_step_name_proposed") and lc.get("gate_unchanged") is True
        and abs(float(rt["face_weight_cos2"]) - (1.0 - float(core["beta"]))) < 1e-12 and abs(float(rt["reflection_weight_sin2"]) - float(core["beta"])) < 1e-12
        and abs(float(rt["transmitted_t1_g1"]) + float(rt["charged_t1_g1"]) - 1.0) < 1e-12
        and bool(lc.get("r4_frozen_set")) and bool(lc.get("corrections_beside_20261002")) and len(lc.get("readings_ratified_20261002") or {}) == 6
        and (lc.get("operator_decision_20261002") or {}).get("verbatim") == "prefiro a primeira opção",
    "a chave da v382 (selada so no Nos) NAO esta no core da v383": "the_ledger_of_charges_v382" not in core and "the_ledger_of_charges_reading_v382" not in selo,
    "os %d homonimos novos (nomeados em _AMBIGUOS_CONJUNTO_V383) estao no conjunto de ambiguos do indice da IALD" % len(ESP["homonimos_novos"]):
        len(ESP["homonimos_novos"]) == 3 and all(n in set(ix.get("ambiguos") or []) for n in ESP["homonimos_novos"]),
    "A1 do aferidor (v376): o .md SELADO lista TODOS os modulos com veredito/status do core final (contagem igual) e o v383":
        (lambda ks: len(ks) == sum(1 for _k, _m in core.items() if isinstance(_m, dict) and (_m.get("verdict") or _m.get("status")))
         and all(k in ks for k in ESP["vereditos_v383_do_ensaio"]) and len(ks) == ESP["n_modulos_md_esperado"])(set(re.findall(r"^- `([A-Za-z0-9_]+)`: `", fc, flags=re.M))),
    "carimbo do .md = sha16 do um.py do disco (forma canonica e manifesto)": ("sha256/16 `%s`" % umsha) in fc and ("sha256/16 `%s`" % umsha) in mf,
    "as 32 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":
        kf.get("lake_build_ok") is True and all(set((kf.get("axiom_report") or {}).get(nm, ["X"])) <= {"propext", "Classical.choice", "Quot.sound"} for _, nm in ESP["bandeiras"]),
    "A MEMORIA CANONICA .md com o carimbo de versao v383 e a secao de TODOS os modulos (forma canonica + manifesto)":
        ESP["md_carimbo"] in fc and ESP["md_todos_os_modulos"] in fc and ESP["md_carimbo"] in mf and fc.count("v383") > 0 and mf.count("v383") > 0,
    "cache/CHAIN_OF_CUSTODY.json gravado (JSON valido)": (lambda p: os.path.exists(p) and bool(json.load(open(p, encoding="utf-8"))))(os.path.join(os.path.dirname(NOS), "cache", "CHAIN_OF_CUSTODY.json")),
}
for k, v in ESP["vereditos_v383_do_ensaio"].items():
    DEVE_MUDAR["veredito %s = o do ensaio (selado)" % k] = V(k) == v and (core.get(k) or {}).get("all_verified") is True
NAO_PODE_MUDAR = {
    "qg_closure_verdict (a string inteira)": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict_v381"],
    "the_iald_index: mesmo veredito e n_ausentes %d (nao pode mudar)" % ESP["the_iald_index_v381"]["n_ausentes"]:
        V("the_iald_index") == ESP["the_iald_index_v381"]["verdict"] and ix.get("n_ausentes") == ESP["the_iald_index_v381"]["n_ausentes"],
    "beta, alpha e omega_I do core inalterados": core.get("beta") == ESP["beta_v381"] and core.get("alpha") == ESP["alpha_v381"] and core.get("omega_I") == ESP["omega_I_v381"],
    "nenhum sorryAx no axiom_report": not any("sorryAx" in a for v in (kf.get("axiom_report") or {}).values() for a in (v or [])),
    "as 18 bandeiras do gate True": n18 == 18,
    "full_static_witness_exists False (selo e gate)": selo.get("full_static_witness_exists") is False and (qg.get("gate") or {}).get("full_static_witness_exists") is False,
    "POR TERMO: gpf_H2 / gpf_H3 / gpi_H3 False": all(kf.get(k) is False for k in (
        "gpf_H2_smooth_modular_four_frame_discharged", "gpf_H3_local_horizon_equilibrium_discharged", "gpi_H3_horizon_data_produced")),
    "a classe por citacao gpc_ segue acesa (3)": all(kf.get(k) is True for k in ("gpc_H2_smooth_modular_four_frame_discharged",
        "gpc_H3_local_horizon_equilibrium_discharged", "gpc_H3_horizon_data_produced")),
    "as 92 bandeiras das v377-v381 (ext_pir_/ext_dis_/ext_dlc_/ext_ter_/ext_tmr_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_antigas"]) and len(ESP["bandeiras_antigas"]) == 92,
    "as chaves EV-06 do selo (conjunta V3; D1 V3 real) seguem presentes": all(k in selo for k in ESP["selo_chaves_ev06"]),
    "fronteira: remaining POR TERMO inalterado (os 2 itens)": fr.get("remaining") == FE["remaining"],
    "fronteira: closed_by_citation_v374 inalterado": fr.get("closed_by_citation_v374") == FE["closed_by_citation_v374"],
    "fronteira: remaining_after_citation_v374 = []": fr.get("remaining_after_citation_v374") == [],
    "formais nao selados inalterados (%s)" % ESP["not_sealed_formais_v381"]: sorted(nst.get("formais") or []) == ESP["not_sealed_formais_v381"],
    "red_clause_JMJ_contains True": kf.get("red_clause_JMJ_contains") is True,
    "zero_abs_proved False": ((core.get("interface_is_light") or {}).get("ledger") or {}).get("zero_abs_proved") is False,
    "nenhum veredito proibido pela MESMA guarda do rito": not [k for k, v in ns_ver.items() if (GUARDA.search(v) or "TGL_PROVED" in v or "CONSCIOUSNESS_PROVED" in v)],
    "o selo EXISTE e registrou o selftest": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
    "a leitura v383 do selo sem palavra proibida (com a terceira palavra)": not GUARDA.search(str(selo.get("the_ledger_of_charges_reading_v383", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_ledger_of_charges_reading_v383", "")),
    "as leituras v377, v378, v379, v380 e v381 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),
    "as chaves do modulo de Coma (flow_layer_status; _v377; _kernel_v378) NAO mudaram": all(pred.get(k) == v for k, v in ESP["coma_keys_pinned"].items()),
}
for k, v in ESP["vereditos_pinados_v381"].items():
    NAO_PODE_MUDAR["veredito inalterado: %s" % k] = V(k) == v
res = {"um_py_sha16": umsha, "deve_mudar": DEVE_MUDAR, "nao_pode_mudar": NAO_PODE_MUDAR,
       "escada_lida": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")], "axiom_report_lido": len(kf.get("axiom_report") or {}),
       "vereditos_v383_lidos": {k: V(k) for k in ESP["vereditos_v383_do_ensaio"]}, "timestamp_selo": selo.get("timestamp"), "um_version_selo": selo.get("um_version")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
ok = all(DEVE_MUDAR.values()) and all(NAO_PODE_MUDAR.values())
res["tudo_bate"] = ok
tag = sys.argv[1] if len(sys.argv) > 1 else ""
json.dump(res, open(os.path.join(HERE, "conferencia_rito_v383%s.json" % tag), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TUDO BATE" if ok else "NAO BATE")
sys.exit(0 if ok else 1)
