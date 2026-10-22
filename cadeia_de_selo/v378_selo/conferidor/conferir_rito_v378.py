# -*- coding: utf-8 -*-
"""conferir_rito_v378.py -- confere, DEPOIS do rito v378, o que tinha de mudar e o que NAO podia mudar. Esperados LIDOS de ESPERADOS_v378.json.
SO LEITURA do Nos. A guarda de palavra proibida e a MESMA do rito. Contra o selo v377 (controle): REPROVA 'deve mudar', APROVA 'nao pode mudar'."""
import hashlib, json, os, re, sys
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
HERE = os.path.dirname(os.path.abspath(__file__))
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v378.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
qg = core.get("qg_closure") or {}
fr = (qg.get("gate") or {}).get("kernel_frontier") or {}
n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
nst = selo.get("not_sealed_this_run") or {}
ns_ver = {k: V(k) for k, m in core.items() if isinstance(m, dict) and "verdict" in m}
FL = [f for f, _ in ESP["bandeiras"]]
FE = ESP["kernel_frontier_v377"]
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
dl = core.get("the_dissipation_law_with_contrast_v378") or {}; bf = core.get("bancada_fase4_v378") or {}; wm = core.get("what_was_missed_v378") or {}
pred = (core.get("coma_distance_dephasing") or {}).get("prediction") or {}
DEVE_MUDAR = {
    "um.py = o candidato aplicado (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "as %d bandeiras ext_dlc_ True" % len(FL): all(kf.get(f) is True for f in FL) and len(FL) == 20,
    "escada %d/%d (v377 %d + %d)" % (ESP["escada_esperada_v378"], ESP["escada_esperada_v378"], ESP["escada_v377"][0], len(FL)):
        esc.get("n_theorems_clean") == ESP["escada_esperada_v378"] == esc.get("n_theorems_expected"),
    "axiom_report >= o do sandbox (%d)" % ESP["axiom_report_sandbox"]: len(kf.get("axiom_report") or {}) >= ESP["axiom_report_sandbox"],
    "o arquivo NOVO do kernel materializado com o sha16 do candidato": all(arq16(k) == v for k, v in novos.items()) and len(novos) == 1,
    "os %d arquivos ALTERADOS do kernel (raiz, Audit) com os sha16 novos" % len(mud): all(arq16(k) == v[1] for k, v in mud.items()),
    "selo: a leitura the_contrast_and_deviation_reading_v378 presente e um_version = v378": "the_contrast_and_deviation_reading_v378" in selo and selo.get("um_version") == "v378",
    "A LEI COM CONTRASTE: K_D1a recomputado = o K da v377 (1e-12); K_D1b = exp(beta I_b) < K_D1a; I_b < N*; a chave flow_layer_kernel_v378 ao lado (as antigas iguais)":
        dl.get("K_D1a_runtime") is not None and abs(float(dl["K_D1a_runtime"]) - float(ESP["K_factor_v377"])) < 1e-12 and float(dl.get("K_D1b_runtime") or 9) < float(dl["K_D1a_runtime"])
        and float(dl.get("I_b_closed_form") or 9) < float(dl.get("register_N_star_nats") or 0) and "TheFlowLawContrast" in str(pred.get("flow_layer_kernel_v378", ""))
        and pred.get("flow_layer_status") == ESP["coma_flow_layer_status_old"] and pred.get("flow_layer_status_v377") == ESP["coma_flow_layer_status_v377_pinned"],
    "a Fase 4 e a reanalise LIDAS POR HASH (bytes) = os artefatos do cache":
        all(((bf.get("hashes") or {}).get(k) or {}).get("sha16_bytes") == ESP["bancada_sha16_bytes"].get(((bf.get("hashes") or {}).get(k) or {}).get("file")) for k in (bf.get("hashes") or {})) and bool(bf.get("hashes"))
        and (wm.get("reanalysis_hashes") or {}).get("sha16_bytes") == ESP["bancada_sha16_bytes"].get((wm.get("reanalysis_hashes") or {}).get("file")),
    "A1 do aferidor (v376): o .md SELADO lista TODOS os modulos com veredito/status do core final (contagem igual) e os 3 v378":
        (lambda ks: len(ks) == sum(1 for _k, _m in core.items() if isinstance(_m, dict) and (_m.get("verdict") or _m.get("status")))
         and all(k in ks for k in ESP["vereditos_v378_do_ensaio"]) and len(ks) == ESP["n_modulos_md_esperado"])(set(re.findall(r"^- `([A-Za-z0-9_]+)`: `", fc, flags=re.M))),
    "carimbo do .md = sha16 do um.py do disco (forma canonica e manifesto)": ("sha256/16 `%s`" % umsha) in fc and ("sha256/16 `%s`" % umsha) in mf,
    "as 20 declaracoes novas no axiom_report, so no trio, sem sorryAx; lake_build_ok":
        kf.get("lake_build_ok") is True and all(set((kf.get("axiom_report") or {}).get(nm, ["X"])) <= {"propext", "Classical.choice", "Quot.sound"} for _, nm in ESP["bandeiras"]),
    "A MEMORIA CANONICA .md com o carimbo de versao v378 e a secao de TODOS os modulos (forma canonica + manifesto)":
        ESP["md_carimbo"] in fc and ESP["md_todos_os_modulos"] in fc and ESP["md_carimbo"] in mf and fc.count("v378") > 0 and mf.count("v378") > 0,
    "cache/CHAIN_OF_CUSTODY.json gravado (JSON valido)": (lambda p: os.path.exists(p) and bool(json.load(open(p, encoding="utf-8"))))(os.path.join(os.path.dirname(NOS), "cache", "CHAIN_OF_CUSTODY.json")),
}
for k, v in ESP["vereditos_v378_do_ensaio"].items():
    DEVE_MUDAR["veredito %s = o do ensaio (selado)" % k] = V(k) == v and (core.get(k) or {}).get("all_verified") is True
NAO_PODE_MUDAR = {
    "qg_closure_verdict (a string inteira)": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict_v377"],
    "the_iald_index: mesmo veredito e n_ausentes %d (nao pode mudar)" % ESP["the_iald_index_v377"]["n_ausentes"]:
        V("the_iald_index") == ESP["the_iald_index_v377"]["verdict"] and ix.get("n_ausentes") == ESP["the_iald_index_v377"]["n_ausentes"],
    "beta, alpha e omega_I do core inalterados": core.get("beta") == ESP["beta_v377"] and core.get("alpha") == ESP["alpha_v377"] and core.get("omega_I") == ESP["omega_I_v377"],
    "nenhum sorryAx no axiom_report": not any("sorryAx" in a for v in (kf.get("axiom_report") or {}).values() for a in (v or [])),
    "as 18 bandeiras do gate True": n18 == 18,
    "full_static_witness_exists False (selo e gate)": selo.get("full_static_witness_exists") is False and (qg.get("gate") or {}).get("full_static_witness_exists") is False,
    "POR TERMO: gpf_H2 / gpf_H3 / gpi_H3 False": all(kf.get(k) is False for k in (
        "gpf_H2_smooth_modular_four_frame_discharged", "gpf_H3_local_horizon_equilibrium_discharged", "gpi_H3_horizon_data_produced")),
    "a classe por citacao gpc_ segue acesa (3)": all(kf.get(k) is True for k in ("gpc_H2_smooth_modular_four_frame_discharged",
        "gpc_H3_local_horizon_equilibrium_discharged", "gpc_H3_horizon_data_produced")),
    "as 25 bandeiras da v377 (ext_pir_/ext_dis_) seguem True": all(kf.get(f) is True for f in ESP["bandeiras_v377"]) and len(ESP["bandeiras_v377"]) == 25,
    "fronteira: remaining POR TERMO inalterado (os 2 itens)": fr.get("remaining") == FE["remaining"],
    "fronteira: closed_by_citation_v374 inalterado": fr.get("closed_by_citation_v374") == FE["closed_by_citation_v374"],
    "fronteira: remaining_after_citation_v374 = []": fr.get("remaining_after_citation_v374") == [],
    "formais nao selados inalterados (%s)" % ESP["not_sealed_formais_v377"]: sorted(nst.get("formais") or []) == ESP["not_sealed_formais_v377"],
    "red_clause_JMJ_contains True": kf.get("red_clause_JMJ_contains") is True,
    "zero_abs_proved False": ((core.get("interface_is_light") or {}).get("ledger") or {}).get("zero_abs_proved") is False,
    "nenhum veredito proibido pela MESMA guarda do rito": not [k for k, v in ns_ver.items() if (GUARDA.search(v) or "TGL_PROVED" in v or "CONSCIOUSNESS_PROVED" in v)],
    "o selo EXISTE e registrou o selftest": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
    "a leitura v378 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_contrast_and_deviation_reading_v378", ""))),
    "a leitura v377 do selo INALTERADA": selo.get("the_dissipation_law_reading_v377") == ESP["selo_leitura_v377"],
    "as chaves antigas do modulo de Coma (flow_layer_status; flow_layer_status_v377) NAO mudaram (a chave nova e AO LADO)":
        pred.get("flow_layer_status") == ESP["coma_flow_layer_status_old"] and pred.get("flow_layer_status_v377") == ESP["coma_flow_layer_status_v377_pinned"],
}
for k, v in ESP["vereditos_pinados_v377"].items():
    NAO_PODE_MUDAR["veredito inalterado: %s" % k] = V(k) == v
res = {"um_py_sha16": umsha, "deve_mudar": DEVE_MUDAR, "nao_pode_mudar": NAO_PODE_MUDAR,
       "escada_lida": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")], "axiom_report_lido": len(kf.get("axiom_report") or {}),
       "vereditos_v378_lidos": {k: V(k) for k in ESP["vereditos_v378_do_ensaio"]}, "timestamp_selo": selo.get("timestamp"), "um_version_selo": selo.get("um_version")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
ok = all(DEVE_MUDAR.values()) and all(NAO_PODE_MUDAR.values())
res["tudo_bate"] = ok
tag = sys.argv[1] if len(sys.argv) > 1 else ""
json.dump(res, open(os.path.join(HERE, "conferencia_rito_v378%s.json" % tag), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TUDO BATE" if ok else "NAO BATE")
sys.exit(0 if ok else 1)
