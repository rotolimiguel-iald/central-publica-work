# -*- coding: utf-8 -*-
"""conferir_rito_v387.py -- confere, DEPOIS do rito v387, o que tinha de mudar, o que NAO podia mudar e o que muda e e' dito. Esperados LIDOS de
ESPERADOS_v387.json (o estado selado da v386 pinado). SO LEITURA do Nos e do cache. A guarda de palavra proibida e a MESMA do rito. Molde: conferir_rito_v386.py.
O pilar NAO roda de novo: exige o REAPROVEITAMENTO pela chave (o mesmo resultado e veredito da v386); se o reuse foi recusado e o pilar calculou de novo, isso
NAO reprova (fica dito)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v387.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}
axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
qg = core.get("qg_closure") or {}
n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")
ns_ver = {k: V(k) for k, m in core.items() if isinstance(m, dict) and "verdict" in m}
esc = core.get("external_ladder") or {}
qp = core.get("quantum_pillar_v384") or {}
txt = {l: (open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
flat = {l: re.sub(r"\s+", " ", t) for l, t in txt.items()}
toc = {l: (open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
reused = qp.get("mode") == "REUSE" and (qp.get("reuse") or {}).get("reused") is True
computed = qp.get("mode") == "COMPUTE"
R = {k: core.get(k) or {} for k in ESP["registros_v387"]}
S = {k: selo.get(k) or {} for k in ESP["registros_v387"]}
hr, pr, tt, rr = R["hubble_ratio_v387"], R["primordial_v387"], R["three_stress_tests_v387"], R["retrodiction_reading_v387"]
v1_disk_ok = all(os.path.isfile(f["path"]) and hashlib.sha256(open(f["path"], "rb").read()).hexdigest() == f["sha256"] for P in ESP["V1"].values() for f in P["files"].values())
DEVE_MUDAR = {
    "um.py = o candidato aplicado (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo: um_version = v387; os quatro registros v387 presentes no selo, iguais ao core (veredito)": selo.get("um_version") == "v387" and all(S[k].get("verdict") == V(k) and S[k].get("verdict") for k in ESP["registros_v387"]),
    "os quatro registros v387 SELARAM (all_verified)": all(R[k].get("all_verified") is True for k in ESP["registros_v387"]),
    "C3: os 4 vereditos v387 = os pinados do ensaio a seco (o mesmo core, as mesmas contagens)": all(V(k) == v for k, v in ESP["vereditos_v387_do_ensaio"].items()),
    "os dois V1 (json, md, hashes e os demais da pasta) em disco com os sha256 pinados": v1_disk_ok,
    "a razao de Hubble LIDA POR HASH (o json, o spec e a funcao), AWAITING_DATA, nada aberto": hr.get("read_ok") is True and hr.get("funcao_ok") is True and hr.get("beta_ok") is True
        and (hr.get("sha256_read") or {}).get("json") == ESP["V1"]["fase9"]["files"]["json"]["sha256"] and hr.get("spec_sha256_recomputed") == ESP["V1"]["fase9"]["spec_sha256"]
        and hr.get("funcao_sha256_recomputed") == ESP["V1"]["fase9"]["funcao_sha256"] and hr.get("nothing_opened") is True
        and V("hubble_ratio_v387").startswith("TGL_HUBBLE_RATIO_V387__V1_READ_BY_HASH_" + ESP["V1"]["fase9"]["files"]["json"]["sha256"][:16]) and "__AWAITING_DATA__NOTHING_OPENED__" in V("hubble_ratio_v387"),
    "a era da radiacao LIDA POR HASH (o json, o spec e a funcao), o controle D3 passou, AWAITING_DATA, nada aberto": pr.get("read_ok") is True and pr.get("funcao_ok") is True and pr.get("beta_ok") is True
        and (pr.get("sha256_read") or {}).get("json") == ESP["V1"]["fase8"]["files"]["json"]["sha256"] and pr.get("spec_sha256_recomputed") == ESP["V1"]["fase8"]["spec_sha256"]
        and (pr.get("transcribed") or {}).get("controle_D3_passou") is True and pr.get("nothing_opened") is True
        and V("primordial_v387").startswith("TGL_PRIMORDIAL_V387__V1_READ_BY_HASH_" + ESP["V1"]["fase8"]["files"]["json"]["sha256"][:16]),
    "os tres testes contados pela MESMA guarda: kernel %d/%d, gate 18/18, 0 palavra proibida, verbatim por sha256" % tuple(ESP["escada"]): ("__KERNEL_%d_OF_%d__" % tuple(ESP["escada"])) in V("three_stress_tests_v387")
        and "__GATE_FLAGS_18_OF_18__" in V("three_stress_tests_v387") and tt.get("n_forbidden_word_as_verdict") == 0 and (tt.get("verbatim") or {}).get("ok") is True
        and (tt.get("verbatim") or {}).get("sha256") == ESP["verbatins"]["tres_testes"]["sha256"],
    "a lei da prova (retrodicao) com o verbatim por sha256": rr.get("verbatim_sha256") == ESP["verbatins"]["pos_dicao"]["sha256"] and V("retrodiction_reading_v387").startswith("TGL_RETRODICTION_READING_V387__USE_NOVELTY_NOT_TEMPORAL_NOVELTY__"),
    "o artigo PT e EN trazem as secoes novas e as frases da apresentacao/resumo/palavras-chave; os 4 vereditos v387 no texto": all(m in flat[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l])
        and all(V(k) in flat[l].replace(" ", "") or V(k) in flat[l] for l in ("pt", "en") for k in ESP["registros_v387"]),
    "a secao dos tres testes vem ANTES da v386 no artigo": all(0 <= flat[l].find(ESP["artigo_marcas"][l][0]) < flat[l].find(ESP["artigo_marcas"][l][2]) for l in ("pt", "en")),
    "«pos-dicao declarada» saiu do texto (so fica a mencao explicativa)": not any(w in flat[l] for l in ("pt", "en") for w in ESP["artigo_nao_deve"][l]),
    "o sumario (.toc) PT/EN lista os tres testes, «Ao lado (v387)», «(v386)» e «(v385)»": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc_marcas"][l]),
    "a memoria canonica .md com o carimbo v387, a linha «Ao lado (v387)» e a errata v386 que fica": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_ao_lado_v387"] in fc and ESP["md_errata_v386_fica"] in fc,
    "carimbo do .md = sha16 do um.py do disco": ("sha256/16 `%s`" % umsha) in fc and ("sha256/16 `%s`" % umsha) in mf,
    "o pilar foi REAPROVEITADO pela mesma chave (o mesmo resultado e veredito da v386) -- OU calculou de novo, DITO": (reused and qp.get("key") == ESP["pilar_v386"]["key"] and qp.get("result_sha256") == ESP["pilar_v386"]["result_sha256"]
        and V("quantum_pillar_v384") == ESP["pilar_v386"]["verdict"] and qp.get("custody_chain_ok") is True) or (computed and V("quantum_pillar_v384").startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__")),
    "o terceiro balde da custodia de sentido existe e esta vazio": (selo.get("not_sealed_this_run") or {}).get("computacao_nao_concluida") == [],
}
dif = {k: (v, V(k)) for k, v in ESP["vereditos_v386"].items() if V(k) != v}
_ft = sorted(k for k, v in kf.items() if v is True)
NAO_PODE_MUDAR = {
    "qg_closure_verdict (a string inteira)": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict_v386"],
    "the_iald_index: mesmo veredito e n_ausentes": V("the_iald_index") == ESP["the_iald_index_v386"]["verdict"] and (core.get("the_iald_index") or {}).get("n_ausentes") == ESP["the_iald_index_v386"]["n_ausentes"],
    "beta, alpha e omega_I do core inalterados": core.get("beta") == ESP["beta_v386"] and core.get("alpha") == ESP["alpha_v386"] and core.get("omega_I") == ESP["omega_I_v386"],
    "a escada inalterada (%d/%d)" % tuple(ESP["escada"]): [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == ESP["escada"],
    "nenhum sorryAx no axiom_report": not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "as 18 bandeiras do gate True": n18 == 18,
    "full_static_witness_exists False (selo e gate)": selo.get("full_static_witness_exists") is False and (qg.get("gate") or {}).get("full_static_witness_exists") is False,
    "as bandeiras gpf_/gpc_/gpi_ inalteradas": {k: kf.get(k) for k in ESP["flags_gpf_gpc_gpi_v386"]} == ESP["flags_gpf_gpc_gpi_v386"],
    "as bandeiras True do kernel = as da v386 (nenhuma pedra nova)": _ft == ESP["flags_true_v386"],
    "formais nao selados inalterados (vazio) e recusas de dado inalteradas": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais_v386"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas_v386"],
    "TODOS os vereditos da v386 inalterados (%d), inclusive o pilar e a reprodutibilidade (sob o mesmo reuse)" % len(ESP["vereditos_v386"]): not dif,
    "as 9 leituras v377-v386 do selo INALTERADAS e os registros v386 do selo inalterados": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items())
        and all(selo.get(k) == v for k, v in ESP["selo_registros_v386_pinados"].items()),
    "nenhum veredito proibido pela MESMA guarda do rito": not [k for k, v in ns_ver.items() if (GUARDA.search(v) or "TGL_PROVED" in v or "CONSCIOUSNESS_PROVED" in v)],
    "o selo EXISTE e registrou o selftest": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
    "o rito rodou a rodada completa (rite_checkpoints desligado)": (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE_MUDAR, "nao_pode_mudar": NAO_PODE_MUDAR, "vereditos_que_mudaram": dif,
       "registros_v387": {k: {x: R[k].get(x) for x in ("verdict", "all_verified", "errors")} for k in ESP["registros_v387"]},
       "pilar": {k: qp.get(k) for k in ("verdict", "mode", "key", "result_sha256", "custody_chain_ok", "reuse")},
       "timestamp_selo": selo.get("timestamp"), "um_version_selo": selo.get("um_version")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if dif:
    print("vereditos que mudaram:", json.dumps(dif, ensure_ascii=False)[:3000])
print("PILAR (informacao):", "REAPROVEITADO" if reused else ("CALCULADO DE NOVO" if computed else "nem um nem outro"))
_lg = os.path.join(HERE, "rito_servidor_v387.log")
_lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = ("RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt
                                  else ("AVISO: a porta 8081 nao escutou -- conferir a tarefa" if "AVISO: a porta 8081" in _lt else "ver o log do lancador")))
res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if re.match(r"^\d\d:\d\d:\d\d ", l_) and ("AVISO" in l_ or "FALHA VISIVEL" in l_)]
_sg = os.path.join(HERE, "rito_v387_sinal.txt")
res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])
res["marcador_do_servidor_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
print("servidor do modelo nativo depois do rito (informacao):", res["servidor_depois_do_rito"], "| marcador ficou:", res["marcador_do_servidor_ficou"])
for l_ in res["avisos_do_lancador"] + res["sinais_desta_rodada"]:
    print("  AVISO/SINAL:", l_)
ok = all(DEVE_MUDAR.values()) and all(NAO_PODE_MUDAR.values())
res["tudo_bate"] = ok
tag = sys.argv[1] if len(sys.argv) > 1 else ""
p = os.path.join(HERE, "conferencia_rito_v387%s.json" % tag)
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE")
sys.exit(0 if ok else 1)
