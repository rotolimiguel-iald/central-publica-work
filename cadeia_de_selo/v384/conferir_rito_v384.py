# -*- coding: utf-8 -*-
"""conferir_rito_v384.py -- confere, DEPOIS do rito v384, o que tinha de mudar e o que NAO podia mudar. Esperados LIDOS de ESPERADOS_v384.json (o estado
selado da v383 pinado). SO LEITURA do Nos e do cache. A guarda de palavra proibida e a MESMA do rito."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v384.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
qg = core.get("qg_closure") or {}
n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")
ns_ver = {k: V(k) for k, m in core.items() if isinstance(m, dict) and "verdict" in m}
esc = core.get("external_ladder") or {}
qp = core.get("quantum_pillar_v384") or {}
sq = selo.get("quantum_pillar_v384") or {}
txt = {l: (open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
cache_ok = False
_sv = (qp.get("reuse") or {}).get("saved_to_cache")
_d128_ran = str(((qp.get("summary") or {}).get("D128") or {}).get("status_code")) == "RAN"
if _sv and os.path.exists(os.path.join(_sv, "result.json")):
    cache_ok = hashlib.sha256(open(os.path.join(_sv, "result.json"), "rb").read()).hexdigest() == qp.get("result_sha256") == open(os.path.join(_sv, "result.json.sha256"), encoding="ascii").read().strip()
elif not _d128_ran:
    # o D128 nao rodou (negativo honesto da arvore): o cache NAO grava, e isso tem de estar DITO com o codigo (3a afericao)
    cache_ok = str((qp.get("reuse") or {}).get("not_cached_code") or "").startswith("D128_NOT_RAN")
_vq = V("quantum_pillar_v384")
DEVE_MUDAR = {
    "um.py = o candidato aplicado (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo: um_version = v384; a leitura e o registro do pilar presentes": selo.get("um_version") == "v384" and "the_quantum_pillar_reading_v384" in selo and bool(sq),
    "o pilar RODOU nesta rodada (mode COMPUTE, rodada completa, sem reaproveitamento)": qp.get("mode") == "COMPUTE" and (qp.get("reuse") or {}).get("reused") is False and qp.get("checkpoint_switch") is False,
    "o veredito do pilar e' da arvore congelada, rederivado igual ao do trabalhador, sem NOT_RUN/VOID/PARCIAL": V("quantum_pillar_v384").startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__")
        and qp.get("verdict_rederived") == qp.get("verdict_worker") == _vq and not _vq.startswith("TGL_QUANTUM_PILLAR_V1__NOT_RUN__")
        and not any(t in _vq for t in ("__RESULTS_VOID__", "__PARTIAL_RESULT_", "__CUSTODY_CHAIN_INCOMPLETE__")),   # D128_NOT_RUN_* e' negativo honesto da arvore, nao reprova (3a afericao)
    "a cadeia de custodia do pilar confere (sha256 do resultado; a especificacao e o trabalhador congelados; o pre-registro em disco)": qp.get("custody_chain_ok") is True
        and qp.get("spec_sha256_in_result") == ESP["spec_sha256"] and qp.get("worker_sha256") == ESP["worker_sha256"]
        and all(((qp.get("preregistration") or {}).get("on_disk_matches") or {}).get(k) is True for k in ("json", "md")),
    "o resultado foi GRAVADO no cache e o sha256 bate (ou o D128 nao rodou e a razao esta dita com o codigo)": cache_ok,
    "o selo registra o mesmo veredito e o mesmo sha256 do resultado": sq.get("verdict") == V("quantum_pillar_v384") and sq.get("result_sha256") == qp.get("result_sha256"),
    "o beta do trabalhador e' o do core (bit a bit) e a marca da rodada esta no resultado": qp.get("beta_matches_core") is True and bool(qp.get("run_id")),
    "o resultado do pilar esta no Nos e no hash do selo": (lambda p_: os.path.exists(p_) and (selo.get("sha256") or {}).get("um_absoluto_pilar_quantico.json") == hashlib.sha256(open(p_, "rb").read()).hexdigest() == qp.get("result_sha256"))(os.path.join(NOS, "um_absoluto_pilar_quantico.json")),
    "o terceiro balde da custodia de sentido existe e esta vazio": (selo.get("not_sealed_this_run") or {}).get("computacao_nao_concluida") == [],
    # os artefatos da rodada que o result.json amarra por hash (4a afericao): details.jsonl e cpuref.json na pasta da rodada, conferidos contra o disco
    "details.jsonl e cpuref.json da rodada batem com os sha256 do resultado": bool(qp.get("run_dir")) and all(
        os.path.exists(os.path.join(qp["run_dir"], f_)) and hashlib.sha256(open(os.path.join(qp["run_dir"], f_), "rb").read()).hexdigest() == qp.get(k_)
        for f_, k_ in (("details.jsonl", "details_sha256"), ("cpuref.json", "cpuref_sha256"))),
    "o artigo PT e EN trazem a introducao e a nota": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]),
    "a memoria canonica .md com o carimbo v384 e o pilar listado": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and "quantum_pillar_v384" in fc,
    "carimbo do .md = sha16 do um.py do disco": ("sha256/16 `%s`" % umsha) in fc and ("sha256/16 `%s`" % umsha) in mf,
}
dif = {k: (v, V(k)) for k, v in ESP["vereditos_v383"].items() if V(k) != v}
NAO_PODE_MUDAR = {
    "qg_closure_verdict (a string inteira)": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict_v383"],
    "the_iald_index: mesmo veredito e n_ausentes": V("the_iald_index") == ESP["the_iald_index_v383"]["verdict"] and (core.get("the_iald_index") or {}).get("n_ausentes") == ESP["the_iald_index_v383"]["n_ausentes"],
    "beta, alpha e omega_I do core inalterados": core.get("beta") == ESP["beta_v383"] and core.get("alpha") == ESP["alpha_v383"] and core.get("omega_I") == ESP["omega_I_v383"],
    "a escada inalterada (nenhuma pedra nova)": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == ESP["escada_v383"],
    "nenhum sorryAx no axiom_report": not any("sorryAx" in a for v in (kf.get("axiom_report") or {}).values() for a in (v or [])),
    "as 18 bandeiras do gate True": n18 == 18,
    "full_static_witness_exists False (selo e gate)": selo.get("full_static_witness_exists") is False and (qg.get("gate") or {}).get("full_static_witness_exists") is False,
    "as bandeiras gpf_/gpc_/gpi_ inalteradas": {k: kf.get(k) for k in ESP["flags_gpf_gpc_v383"]} == ESP["flags_gpf_gpc_v383"],
    "o numero de bandeiras True do kernel inalterado": sum(1 for k, v in kf.items() if v is True) == ESP["n_flags_true_v383"],
    "formais nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais_v383"],
    "TODOS os vereditos da v383 inalterados (%d)" % len(ESP["vereditos_v383"]): not dif,
    "as leituras v377-v383 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),
    "nenhum veredito proibido pela MESMA guarda do rito": not [k for k, v in ns_ver.items() if (GUARDA.search(v) or "TGL_PROVED" in v or "CONSCIOUSNESS_PROVED" in v)],
    "a leitura v384 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_quantum_pillar_reading_v384", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_quantum_pillar_reading_v384", "")),
    "o selo EXISTE e registrou o selftest": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
    "o rito rodou a rodada completa (rite_checkpoints desligado)": (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE_MUDAR, "nao_pode_mudar": NAO_PODE_MUDAR, "vereditos_que_mudaram": dif,
       "pilar": {k: qp.get(k) for k in ("verdict", "mode", "key", "result_sha256", "custody_chain_ok", "partial", "timed_out", "worker_rc")},
       "timestamp_selo": selo.get("timestamp"), "um_version_selo": selo.get("um_version")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if dif:
    print("vereditos que mudaram:", json.dumps(dif, ensure_ascii=False)[:3000])
# INFORMACAO (nao decide): o servidor do modelo nativo depois do rito, lido do log do lancador (4a afericao)
_lg = os.path.join(HERE, "rito_servidor_v384.log")
_lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = ("PAROU DEPOIS DE ESCUTAR (o marcador ficou) -- conferir a tarefa" if "escutou e PAROU" in _lt else
                                  "ESCUTA, MAS A CONTAGEM DAS PARADAS NAO FOI LEGIVEL (o marcador ficou) -- conferir a tarefa" if "a contagem das paradas em curso nao foi legivel" in _lt else
                                  "ESCUTA, MAS HAVIA PARADA EM CURSO (o marcador ficou) -- conferir a tarefa" if ("ainda em curso" in _lt and ("ha parada (Stop-ScheduledTask" in _lt or "ha parada da tarefa" in _lt)) else
                                  "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt
                                  else ("AVISO: a porta 8081 nao escutou -- conferir a tarefa" if "AVISO: a porta 8081" in _lt else "sem registro no log do lancador")))
res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if re.match(r"^\d\d:\d\d:\d\d ", l_) and ("AVISO" in l_ or "FALHA VISIVEL" in l_)]   # so o log() do lancador (6a e 7a)
_sg = os.path.join(HERE, "rito_v384_sinal.txt")
res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])   # gira so quando a rodada vai rodar (8a)
_av_rel = [l_ for l_ in res["avisos_do_lancador"] if "AVISO_PID_VELHO" not in l_]   # o PID velho nao e' do religamento (8a afericao)
if _av_rel and res["servidor_depois_do_rito"].startswith("RELIGADO"):
    res["servidor_depois_do_rito"] = "RELIGADO COM AVISO: " + " | ".join(_av_rel)
print("servidor do modelo nativo depois do rito (informacao):", res["servidor_depois_do_rito"])
for l_ in res["avisos_do_lancador"]:
    print("  AVISO DO LANCADOR:", l_)
for l_ in res["sinais_desta_rodada"]:
    print("  SINAL/FALHA desta rodada (rito_v384_sinal.txt):", l_)
ok = all(DEVE_MUDAR.values()) and all(NAO_PODE_MUDAR.values())
res["tudo_bate"] = ok
tag = sys.argv[1] if len(sys.argv) > 1 else ""
p = os.path.join(HERE, "conferencia_rito_v384%s.json" % tag)
with open(p + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE")
sys.exit(0 if ok else 1)
