# -*- coding: utf-8 -*-
"""conferir_rito_v385.py -- confere, DEPOIS do rito v385, o que tinha de mudar e o que NAO podia mudar. Esperados LIDOS de ESPERADOS_v385.json (o estado
selado da v384 pinado). SO LEITURA do Nos e do cache. A guarda de palavra proibida e a MESMA do rito. Molde: conferir_rito_v384.py.

A reprodutibilidade do pilar e' RESULTADO: o conferidor exige que a comparacao TENHA ACONTECIDO (contra o resultado pinado da v384), e DIZ o que ela deu;
um NOT_REPRODUCED nao reprova o rito -- fica dito, como negativo honesto (decisao: o operador aprovou a rodada inteira como teste de reprodutibilidade)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v385.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}
axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
qg = core.get("qg_closure") or {}
n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
ns_ver = {k: V(k) for k, m in core.items() if isinstance(m, dict) and "verdict" in m}
esc = core.get("external_ladder") or {}
qp = core.get("quantum_pillar_v384") or {}
sq = selo.get("quantum_pillar_v384") or {}
ax = core.get("the_axiom_v385") or {}
rp = core.get("quantum_pillar_reproducibility_v385") or {}
sax = selo.get("the_axiom_v385") or {}
srp = selo.get("quantum_pillar_reproducibility_v385") or {}
txt = {l: (open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
cache_ok = False
_sv = (qp.get("reuse") or {}).get("saved_to_cache")
_d128_ran = str(((qp.get("summary") or {}).get("D128") or {}).get("status_code")) == "RAN"
if _sv and os.path.exists(os.path.join(_sv, "result.json")):
    cache_ok = hashlib.sha256(open(os.path.join(_sv, "result.json"), "rb").read()).hexdigest() == qp.get("result_sha256") == open(os.path.join(_sv, "result.json.sha256"), encoding="ascii").read().strip()
elif not _d128_ran:
    cache_ok = str((qp.get("reuse") or {}).get("not_cached_code") or "").startswith("D128_NOT_RAN")
_vq = V("quantum_pillar_v384")
_stone = os.path.join(NOS, "tgl_kernel", *"TGLExt/TheAxiomAndTheFalseWitness.lean".split("/"))
_stone_sha = hashlib.sha256(open(_stone, "rb").read()).hexdigest()[:16] if os.path.exists(_stone) else None
_nomes = ESP["nomes_lean_v385"]
_ax_trio = {f: (axr.get(n) is not None and set(axr.get(n) or []) <= TRIO) for f, n in _nomes.items()}
_prev = rp.get("previous") or {}
NF = len(ESP["flags_v385"])   # as bandeiras da v385 (22 da pedra + 7 do TheDarkSplit), LIDAS dos esperados
DEVE_MUDAR = {
    "um.py = o candidato aplicado (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo: um_version = v385; a leitura, o nome do degrau final e os dois registros novos presentes": selo.get("um_version") == "v385" and bool(selo.get("the_axiom_reading_v385"))
        and selo.get("final_step_name_v385") == ESP["final_step_name"] and bool(sax) and bool(srp),
    "a escada subiu para %d/%d (%d pedras novas, todas limpas)" % (ESP["escada_v385"][1], ESP["escada_v385"][1], NF):
        [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == [ESP["escada_v385"][1], ESP["escada_v385"][1]],
    "a pedra nova esta no kernel do Nos com o sha do candidato": _stone_sha == ESP["kernel"]["new"]["TGLExt/TheAxiomAndTheFalseWitness.lean"],
    "as %d bandeiras da v385 True no kernel_formalization" % NF: all(kf.get(f) is True for f in ESP["flags_v385"]),
    "as %d declaracoes no axiom_report, todas dentro do trio" % NF: all(_ax_trio.values()),
    "o Axioma SELOU: %d de %d, o nome do degrau final lido do kernel e igual ao do operador" % (NF, NF): ax.get("all_verified") is True and ax.get("kernel_flags_ok") == NF
        and ax.get("final_step_name_matches_kernel") is True and ax.get("final_step_name_from_kernel") == ESP["final_step_name"]
        and V("the_axiom_v385").startswith("TGL_THE_AXIOM_V385__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED__") and ("__KERNEL_%d_OF_%d__" % (NF, NF)) in V("the_axiom_v385"),
    "o selo registra o mesmo veredito do Axioma": sax.get("verdict") == V("the_axiom_v385"),
    "o pilar RODOU de novo nesta rodada (mode COMPUTE, rodada completa, sem reaproveitamento)": qp.get("mode") == "COMPUTE" and (qp.get("reuse") or {}).get("reused") is False and qp.get("checkpoint_switch") is False,
    "o pilar rodou com a MESMA chave da v384 (mesmo trabalhador, especificacao e beta)": qp.get("key") == ESP["pilar_v384"]["key"],
    "o veredito do pilar e' da arvore congelada, rederivado igual ao do trabalhador, sem NOT_RUN/VOID/PARCIAL": _vq.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__")
        and qp.get("verdict_rederived") == qp.get("verdict_worker") == _vq and not _vq.startswith("TGL_QUANTUM_PILLAR_V1__NOT_RUN__")
        and not any(t in _vq for t in ("__RESULTS_VOID__", "__PARTIAL_RESULT_", "__CUSTODY_CHAIN_INCOMPLETE__")),
    "a cadeia de custodia do pilar confere (sha256 do resultado; a especificacao e o trabalhador do V1; o pre-registro em disco)": qp.get("custody_chain_ok") is True
        and qp.get("spec_sha256_in_result") == ESP["spec_sha256"] and qp.get("worker_sha256") == ESP["worker_sha256"]
        and all(((qp.get("preregistration") or {}).get("on_disk_matches") or {}).get(k) is True for k in ("json", "md")),
    "o resultado novo foi GRAVADO no cache e o sha256 bate (ou o D128 nao rodou e a razao esta dita com o codigo)": cache_ok,
    "o resultado novo NAO e' o arquivo da v384 (o pilar calculou de novo)": bool(qp.get("result_sha256")) and qp.get("run_id") != ESP["pilar_v384"]["run_id"],
    "o selo registra o mesmo veredito e o mesmo sha256 do resultado do pilar": sq.get("verdict") == _vq and sq.get("result_sha256") == qp.get("result_sha256"),
    "o beta do trabalhador e' o do core (bit a bit) e a marca da rodada esta no resultado": qp.get("beta_matches_core") is True and bool(qp.get("run_id")),
    "o resultado do pilar esta no Nos e no hash do selo": (lambda p_: os.path.exists(p_) and (selo.get("sha256") or {}).get("um_absoluto_pilar_quantico.json") == hashlib.sha256(open(p_, "rb").read()).hexdigest() == qp.get("result_sha256"))(os.path.join(NOS, "um_absoluto_pilar_quantico.json")),
    "o terceiro balde da custodia de sentido existe e esta vazio": (selo.get("not_sealed_this_run") or {}).get("computacao_nao_concluida") == [],
    "details.jsonl e cpuref.json da rodada batem com os sha256 do resultado": bool(qp.get("run_dir")) and all(
        os.path.exists(os.path.join(qp["run_dir"], f_)) and hashlib.sha256(open(os.path.join(qp["run_dir"], f_), "rb").read()).hexdigest() == qp.get(k_)
        for f_, k_ in (("details.jsonl", "details_sha256"), ("cpuref.json", "cpuref_sha256"))),
    "a reprodutibilidade FOI MEDIDA, contra o resultado pinado da v384 (mesma chave, mesmo sha256)": rp.get("compared") is True
        and _prev.get("sha256") == ESP["pilar_v384"]["result_sha256"] and _prev.get("key") == ESP["pilar_v384"]["key"]
        and str(rp.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__") and srp.get("verdict") == rp.get("verdict")
        and all(srp.get(k_) == rp.get(k_) for k_ in ("compared", "n_fields", "n_differ", "max_scaled_diff", "d128_excluded")),   # (3a passada, N1) os NUMEROS do selo = os do core
    "o artigo PT e EN trazem a secao v385, a errata ao lado e a etiqueta [POSTO]": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]),
    "o artigo diz o nome do degrau final e o veredito do Axioma": all(ESP["final_step_name"] in txt[l].replace("\n", "") and V("the_axiom_v385") in txt[l].replace("\n", "") for l in ("pt", "en")),
    "a memoria canonica .md com o carimbo v385, a errata do posto e o Axioma listado": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_errata_posto"] in fc and "the_axiom_v385" in fc,
    "carimbo do .md = sha16 do um.py do disco": ("sha256/16 `%s`" % umsha) in fc and ("sha256/16 `%s`" % umsha) in mf,
}
dif = {k: (v, V(k)) for k, v in ESP["vereditos_v384"].items() if V(k) != v}
_ft = sorted(k for k, v in kf.items() if v is True)
NAO_PODE_MUDAR = {
    "qg_closure_verdict (a string inteira)": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict_v384"],
    "the_iald_index: mesmo veredito e n_ausentes": V("the_iald_index") == ESP["the_iald_index_v384"]["verdict"] and (core.get("the_iald_index") or {}).get("n_ausentes") == ESP["the_iald_index_v384"]["n_ausentes"],
    "beta, alpha e omega_I do core inalterados": core.get("beta") == ESP["beta_v384"] and core.get("alpha") == ESP["alpha_v384"] and core.get("omega_I") == ESP["omega_I_v384"],
    "nenhum sorryAx no axiom_report": not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "as 18 bandeiras do gate True": n18 == 18,
    "full_static_witness_exists False (selo e gate)": selo.get("full_static_witness_exists") is False and (qg.get("gate") or {}).get("full_static_witness_exists") is False,
    "as bandeiras gpf_/gpc_/gpi_ inalteradas": {k: kf.get(k) for k in ESP["flags_gpf_gpc_gpi_v384"]} == ESP["flags_gpf_gpc_gpi_v384"],
    "as bandeiras True do kernel = as da v384 + exatamente as %d da v385" % NF: _ft == sorted(set(ESP["flags_true_v384"]) | set(ESP["flags_v385"])),
    "formais nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais_v384"],
    "TODOS os vereditos da v384 inalterados, fora o do pilar (%d)" % len(ESP["vereditos_v384"]): not dif,
    "as leituras v377-v384 do selo INALTERADAS": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items()),
    "nenhum veredito proibido pela MESMA guarda do rito": not [k for k, v in ns_ver.items() if (GUARDA.search(v) or "TGL_PROVED" in v or "CONSCIOUSNESS_PROVED" in v)],
    "a leitura v385 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_axiom_reading_v385", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_axiom_reading_v385", "")),
    "o selo EXISTE e registrou o selftest": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
    "o rito rodou a rodada completa (rite_checkpoints desligado)": (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE_MUDAR, "nao_pode_mudar": NAO_PODE_MUDAR, "vereditos_que_mudaram": dif,
       "axioma": {k: ax.get(k) for k in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "final_step_name_matches_kernel")},
       "declaracoes_fora_do_trio_ou_ausentes": [_nomes[f] for f, ok_ in _ax_trio.items() if not ok_],
       "pilar": {k: qp.get(k) for k in ("verdict", "mode", "key", "result_sha256", "custody_chain_ok", "partial", "timed_out", "worker_rc", "run_id")},
       # INFORMACAO (nao decide): o que a reprodutibilidade deu, e se o veredito do pilar e' o mesmo da v384
       "reprodutibilidade": {k: rp.get(k) for k in ("verdict", "compared", "n_fields", "n_numeric_fields", "n_differ", "max_scaled_diff", "max_rel_diff_finite", "n_nonfinite_differ", "d128_excluded", "inputs", "env", "same_pillar_verdict", "why")},
       "reprodutibilidade_primeiras_diferencas": (rp.get("first_differences") or [])[:10],
       "veredito_do_pilar_igual_ao_da_v384": _vq == ESP["pilar_v384"]["verdict"],
       "timestamp_selo": selo.get("timestamp"), "um_version_selo": selo.get("um_version")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if dif:
    print("vereditos que mudaram:", json.dumps(dif, ensure_ascii=False)[:3000])
if res["declaracoes_fora_do_trio_ou_ausentes"]:
    print("declaracoes fora do trio ou ausentes:", res["declaracoes_fora_do_trio_ou_ausentes"])
print("REPRODUTIBILIDADE (resultado, nao decide):", rp.get("verdict"), "| veredito do pilar igual ao da v384:", res["veredito_do_pilar_igual_ao_da_v384"])
for d_ in res["reprodutibilidade_primeiras_diferencas"]:
    print("   diferenca:", json.dumps(d_, ensure_ascii=False)[:300])
# INFORMACAO (nao decide): o servidor do modelo nativo depois do rito, lido do log do lancador
_lg = os.path.join(HERE, "rito_servidor_v385.log")
_lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = ("PAROU DEPOIS DE ESCUTAR (o marcador ficou) -- conferir a tarefa" if "escutou e PAROU" in _lt else
                                  "ESCUTA, MAS A CONTAGEM DAS PARADAS NAO FOI LEGIVEL (o marcador ficou) -- conferir a tarefa" if "a contagem das paradas em curso nao foi legivel" in _lt else
                                  "ESCUTA, MAS HAVIA PARADA EM CURSO (o marcador ficou) -- conferir a tarefa" if ("ainda em curso" in _lt and ("ha parada (Stop-ScheduledTask" in _lt or "ha parada da tarefa" in _lt)) else
                                  "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt
                                  else ("AVISO: a porta 8081 nao escutou -- conferir a tarefa" if "AVISO: a porta 8081" in _lt else "sem registro no log do lancador")))
res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if re.match(r"^\d\d:\d\d:\d\d ", l_) and ("AVISO" in l_ or "FALHA VISIVEL" in l_)]
_sg = os.path.join(HERE, "rito_v385_sinal.txt")
res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])
_av_rel = [l_ for l_ in res["avisos_do_lancador"] if "AVISO_PID_VELHO" not in l_]
if _av_rel and res["servidor_depois_do_rito"].startswith("RELIGADO"):
    res["servidor_depois_do_rito"] = "RELIGADO COM AVISO: " + " | ".join(_av_rel)
print("servidor do modelo nativo depois do rito (informacao):", res["servidor_depois_do_rito"])
for l_ in res["avisos_do_lancador"]:
    print("  AVISO DO LANCADOR:", l_)
for l_ in res["sinais_desta_rodada"]:
    print("  SINAL/FALHA desta rodada (rito_v385_sinal.txt):", l_)
ok = all(DEVE_MUDAR.values()) and all(NAO_PODE_MUDAR.values())
res["tudo_bate"] = ok
tag = sys.argv[1] if len(sys.argv) > 1 else ""
p = os.path.join(HERE, "conferencia_rito_v385%s.json" % tag)
with open(p + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE")
sys.exit(0 if ok else 1)
