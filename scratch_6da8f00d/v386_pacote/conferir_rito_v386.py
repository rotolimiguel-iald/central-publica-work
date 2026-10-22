# -*- coding: utf-8 -*-
"""conferir_rito_v386.py -- confere, DEPOIS do rito v386, o que tinha de mudar, o que NAO podia mudar e o que MUDA E E' DITO. Esperados LIDOS de
ESPERADOS_v386.json (o estado selado da v385 pinado). SO LEITURA do Nos e do cache. A guarda de palavra proibida e a MESMA do rito. Molde: conferir_rito_v385.py.

O pilar NAO roda de novo: o conferidor exige o REAPROVEITAMENTO pela chave (sha256 do resultado = o da v385 selada; mesmo veredito) -- se o reuse foi
recusado e o pilar calculou de novo, isso NAO reprova (fica dito, com o veredito e a reprodutibilidade medida contra o resultado anterior). A
reprodutibilidade v385 sob reuse MUDA para NOT_COMPARED (a funcao v385 e' honesta) -- e' esperado e dito, nao reprova."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v386.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}
axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
qg = core.get("qg_closure") or {}
n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
ns_ver = {k: V(k) for k, m in core.items() if isinstance(m, dict) and "verdict" in m}
esc = core.get("external_ladder") or {}
qp = core.get("quantum_pillar_v384") or {}; sq = selo.get("quantum_pillar_v384") or {}
rp = core.get("quantum_pillar_reproducibility_v385") or {}; srp = selo.get("quantum_pillar_reproducibility_v385") or {}
vb = core.get("the_verb_v386") or {}; svb = selo.get("the_verb_v386") or {}
rb = core.get("ramo_b_preregistration_v386") or {}; srb = selo.get("ramo_b_preregistration_v386") or {}
le = core.get("ledger_errata_v386") or {}; sle = selo.get("ledger_errata_v386") or {}
qr = core.get("quantum_pillar_reuse_v386") or {}; sqr = selo.get("quantum_pillar_reuse_v386") or {}
txt = {l: (open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read() if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
_toc = {l: (open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}   # W10
_lin = lambda l, frag: next((x_ for x_ in txt[l].splitlines() if frag in x_), "")
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read()
mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
_vq = V("quantum_pillar_v384")
_stone = os.path.join(NOS, "tgl_kernel", *"TGLExt/TheVerbSelectsTheAction.lean".split("/"))
_stone_sha = hashlib.sha256(open(_stone, "rb").read()).hexdigest()[:16] if os.path.exists(_stone) else None
_nomes = ESP["nomes_lean_v386"]
_ax_trio = {f: (axr.get(n) is not None and set(axr.get(n) or []) <= TRIO) for f, n in _nomes.items()}
NF = len(ESP["flags_v386"])   # as bandeiras da v386 (93 da pedra + 17 da fiacao), LIDAS dos esperados
reused = qp.get("mode") == "REUSE" and (qp.get("reuse") or {}).get("reused") is True
computed = qp.get("mode") == "COMPUTE" and (qp.get("reuse") or {}).get("reused") is False
V1 = ESP["ramo_b_V1"]
v1_disk_ok = all(os.path.isfile(f["path"]) and hashlib.sha256(open(f["path"], "rb").read()).hexdigest() == f["sha256"] for f in V1["files"].values())
DEVE_MUDAR = {
    "um.py = o candidato aplicado (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo: um_version = v386; a leitura v386, o token (lido do kernel) e os quatro registros novos presentes": selo.get("um_version") == "v386" and bool(selo.get("the_verb_reading_v386"))
        and selo.get("verb_typing_stone_name_v386") == ESP["verb_token"] and bool(svb) and bool(srb) and bool(sle) and bool(sqr),
    "a escada subiu para %d/%d (%d bandeiras novas, todas limpas)" % (ESP["escada_v386"][1], ESP["escada_v386"][1], NF):
        [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == [ESP["escada_v386"][1], ESP["escada_v386"][1]],
    "a pedra nova esta no kernel do Nos com o sha do candidato": _stone_sha == ESP["kernel"]["new"]["TGLExt/TheVerbSelectsTheAction.lean"],
    "as %d bandeiras da v386 True no kernel_formalization" % NF: all(kf.get(f) is True for f in ESP["flags_v386"]),
    "as %d declaracoes no axiom_report, todas dentro do trio" % NF: all(_ax_trio.values()),
    "o Verbo SELOU: %d de %d; o token lido do kernel = o do pino; os verbatins conferidos por sha256" % (NF, NF): vb.get("all_verified") is True and vb.get("kernel_flags_ok") == NF
        and vb.get("token_matches_kernel") is True and vb.get("token_from_kernel") == ESP["verb_token"] and vb.get("verbatim_hashes_ok") is True
        and V("the_verb_v386").startswith("TGL_THE_VERB_V386__THE_VERB_SELECTS_THE_ACTION__") and ("__KERNEL_%d_OF_%d__" % (NF, NF)) in V("the_verb_v386") and V("the_verb_v386").endswith("__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED"),
    "o selo registra o mesmo veredito do Verbo e os mesmos numeros": svb.get("verdict") == V("the_verb_v386") and all(svb.get(k_) == vb.get(k_) for k_ in ("all_verified", "kernel_flags_ok", "kernel_flags_total", "token_from_kernel", "verbatim_hashes_ok")),
    "o V1 do ramo B (json, md, hashes, poder, gerador) esta em disco com os sha256 pinados": v1_disk_ok,
    "o ramo B foi LIDO POR HASH: read_ok, all_verified, 14 em D, AWAITING_DATA, nada aberto": rb.get("all_verified") is True and rb.get("read_ok") is True and rb.get("conjunto_D_n") == V1["conjunto_D_n"] == 14
        and (rb.get("sha256_read") or {}).get("json") == V1["files"]["json"]["sha256"] and rb.get("identificador_read") == V1["identificador"] and rb.get("spec_sha256_recomputed") == V1["spec_sha256"]
        and V("ramo_b_preregistration_v386").startswith("TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_" + V1["files"]["json"]["sha256"][:16]) and V("ramo_b_preregistration_v386").endswith("__AWAITING_DATA__NOTHING_OPENED__GATE_UNTOUCHED")
        and rb.get("nothing_opened") is True and rb.get("F2b_status") == "AWAITING" and rb.get("veredito_do_V1") == V1["veredito_do_V1"] and rb.get("token_estado") == V1["token_estado"],
    "o selo registra o mesmo veredito e os mesmos sha256/numeros do ramo B": srb.get("verdict") == V("ramo_b_preregistration_v386") and all(srb.get(k_) == rb.get(k_) for k_ in ("all_verified", "read_ok", "sha256_read", "spec_sha256_recomputed", "conjunto_D_n", "F2b_status", "pins")),
    "a errata ao lado de R6 SELOU: o livro v383 intacto (11), F2b AWAITING, F2/R2 intocados": le.get("all_verified") is True and le.get("v383_ledger_intact") is True and le.get("v383_n_charges") == 11
        and (le.get("charge_F2b") or {}).get("token") == "AWAITING" and le.get("F2_untouched") is True and le.get("R2_untouched") is True
        and V("ledger_errata_v386").startswith("TGL_LEDGER_ERRATA_V386__R6_CLOSED_TO_REOPENED_BY_PREREGISTRATION_BESIDE_NOT_OVERWRITTEN__") and sle.get("verdict") == V("ledger_errata_v386"),
    "o pilar foi REAPROVEITADO pela chave da v385 (mode REUSE; o resultado = o sha256 pinado; o veredito igual) -- OU calculou de novo, DITO": (reused and qp.get("key") == ESP["pilar_v385"]["key"] and qp.get("result_sha256") == ESP["pilar_v385"]["result_sha256"]
        and _vq == ESP["pilar_v385"]["verdict"] and qp.get("custody_chain_ok") is True and (qp.get("reuse") or {}).get("reading") == ESP["muda_e_e_dito"]["quantum_pillar_v384_reuse"]["v386_esperado"]["reading"])
        or (computed and _vq.startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__") and qp.get("custody_chain_ok") is True),
    "o registro do reuse v386 SELOU e diz o que aconteceu (reaproveitado com sha/veredito iguais, ou calculado de novo)": qr.get("all_verified") is True and qr.get("key_same_as_v385") is True
        and ((reused and qr.get("reused") is True and qr.get("result_sha256_matches_v385_sealed") is True and qr.get("verdict_same_as_v385_sealed") is True and "REUSED_FROM_THE_SEALED_V385_RUN_BY_KEY__RESULT_SHA256_MATCHES__VERDICT_SAME__CUSTODY_CHAIN_OK" in V("quantum_pillar_reuse_v386"))
             or (computed and "COMPUTED_AGAIN_THIS_RUN_REUSE_REFUSED" in V("quantum_pillar_reuse_v386"))) and sqr.get("verdict") == V("quantum_pillar_reuse_v386"),
    "o resultado do pilar esta no Nos e no hash do selo (o mesmo arquivo da v385 sob reuse)": (lambda p_: os.path.exists(p_) and (selo.get("sha256") or {}).get("um_absoluto_pilar_quantico.json") == hashlib.sha256(open(p_, "rb").read()).hexdigest() == qp.get("result_sha256"))(os.path.join(NOS, "um_absoluto_pilar_quantico.json")),
    "o selo registra o mesmo veredito e o mesmo sha256 do resultado do pilar": sq.get("verdict") == _vq and sq.get("result_sha256") == qp.get("result_sha256"),
    "details.jsonl e cpuref.json da pasta do pilar (o cache, sob reuse) batem com os sha256 do resultado": bool(qp.get("run_dir")) and all(
        os.path.exists(os.path.join(qp["run_dir"], f_)) and hashlib.sha256(open(os.path.join(qp["run_dir"], f_), "rb").read()).hexdigest() == qp.get(k_)
        for f_, k_ in (("details.jsonl", "details_sha256"), ("cpuref.json", "cpuref_sha256"))),
    "o terceiro balde da custodia de sentido existe e esta vazio": (selo.get("not_sealed_this_run") or {}).get("computacao_nao_concluida") == [],
    "o artigo PT e EN trazem a secao v386 (antes da v385), a errata de R6 e o V1 lido": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l])
        and all(txt[l].find(ESP["artigo_marcas"][l][0]) < txt[l].find(ESP["artigo_marcas"][l][3]) for l in ("pt", "en")),
    "o artigo diz o token do Verbo e os tres vereditos v386": all(ESP["verb_token"] in txt[l].replace("\n", "") and V("the_verb_v386") in txt[l].replace("\n", "") and V("ramo_b_preregistration_v386") in txt[l].replace("\n", "") and V("ledger_errata_v386") in txt[l].replace("\n", "") for l in ("pt", "en")),
    "W10 (ordem do operador): o sumario (.toc) PT/EN lista «Ao lado (v385)», «… (v384)» e a «Nota: … GPU …»; a apresentacao (linha 2), «O método»/«The method» e as palavras-chave trazem a GPU":
        all(all(w in _toc[l] for w in ESP.get("toc_marcas_W10", {}).get(l, [])) and "GPU" in (txt[l].splitlines()[1] if len(txt[l].splitlines()) > 1 else "")
            and "GPU" in _lin(l, "O método" if l == "pt" else "The method") and "GPU" in _lin(l, "Palavras-chave" if l == "pt" else "Keywords") for l in ("pt", "en")),
    "a memoria canonica .md com o carimbo v386, a errata de R6 (e a errata do posto da v385 que fica) e os registros v386 listados": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_errata_R6"] in fc and ESP["md_errata_posto_v385_fica"] in fc
        and all(k in fc for k in ("the_verb_v386", "ramo_b_preregistration_v386", "ledger_errata_v386", "quantum_pillar_reuse_v386")),
    "carimbo do .md = sha16 do um.py do disco": ("sha256/16 `%s`" % umsha) in fc and ("sha256/16 `%s`" % umsha) in mf,
}
dif = {k: (v, V(k)) for k, v in ESP["vereditos_v385"].items() if V(k) != v}
_ft = sorted(k for k, v in kf.items() if v is True)
NAO_PODE_MUDAR = {
    "qg_closure_verdict (a string inteira)": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict_v385"],
    "the_iald_index: mesmo veredito e n_ausentes": V("the_iald_index") == ESP["the_iald_index_v385"]["verdict"] and (core.get("the_iald_index") or {}).get("n_ausentes") == ESP["the_iald_index_v385"]["n_ausentes"],
    "beta, alpha e omega_I do core inalterados": core.get("beta") == ESP["beta_v385"] and core.get("alpha") == ESP["alpha_v385"] and core.get("omega_I") == ESP["omega_I_v385"],
    "nenhum sorryAx no axiom_report": not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "as 18 bandeiras do gate True": n18 == 18,
    "full_static_witness_exists False (selo e gate)": selo.get("full_static_witness_exists") is False and (qg.get("gate") or {}).get("full_static_witness_exists") is False,
    "as bandeiras gpf_/gpc_/gpi_ inalteradas": {k: kf.get(k) for k in ESP["flags_gpf_gpc_gpi_v385"]} == ESP["flags_gpf_gpc_gpi_v385"],
    "as bandeiras True do kernel = as da v385 + exatamente as %d da v386" % NF: _ft == sorted(set(ESP["flags_true_v385"]) | set(ESP["flags_v386"])),
    "formais nao selados inalterados (vazio) e recusas de dado inalteradas": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais_v385"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas_v385"],
    "TODOS os vereditos da v385 inalterados, INCLUSIVE o do pilar (%d; fora so a reprodutibilidade, que muda e e' dita)" % len(ESP["vereditos_v385"]): not dif,
    "as leituras v377-v385 do selo INALTERADAS; final_step_name_v385 e the_axiom_v385 do selo inalterados": all(selo.get(k) == v for k, v in ESP["selo_leituras_pinadas"].items())
        and selo.get("final_step_name_v385") == ESP["final_step_name_v385"] and selo.get("the_axiom_v385") == ESP["selo_registros_v385_pinados"]["the_axiom_v385"],
    "o registro da v385 (o Axioma) selou de novo igual": V("the_axiom_v385") == ESP["vereditos_v385"]["the_axiom_v385"] and (core.get("the_axiom_v385") or {}).get("all_verified") is True,
    "nenhum veredito proibido pela MESMA guarda do rito": not [k for k, v in ns_ver.items() if (GUARDA.search(v) or "TGL_PROVED" in v or "CONSCIOUSNESS_PROVED" in v)],
    "a leitura v386 do selo sem palavra proibida": not GUARDA.search(str(selo.get("the_verb_reading_v386", ""))) and "TGL_PRO" + "VED" not in str(selo.get("the_verb_reading_v386", "")),
    "o selo EXISTE e registrou o selftest": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED",
    "o rito rodou a rodada completa (rite_checkpoints desligado; o reuse do pilar e' pela chave da v386, nao pelo interruptor)": (selo.get("rite_checkpoints") or {}).get("switch_on") is False and qr.get("rite_checkpoint_switch") is False and qr.get("switch_reuse_v386") is True,
}
MUDA_E_E_DITO = {
    "quantum_pillar_reproducibility_v385: sob reuse = NOT_COMPARED (o esperado medido no ensaio); se calculou de novo, comparado contra o resultado da v385": (reused and rp.get("verdict") == ESP["muda_e_e_dito"]["quantum_pillar_reproducibility_v385"]["v386_esperado_sob_reuse"] and rp.get("compared") is False)
        or (computed and rp.get("compared") is True and (rp.get("previous") or {}).get("sha256") == ESP["pilar_v385"]["result_sha256"] and str(rp.get("verdict") or "").startswith("TGL_QUANTUM_PILLAR_REPRODUCIBILITY_V385__")),
    "o selo registra a reprodutibilidade igual ao core (veredito e numeros)": srp.get("verdict") == rp.get("verdict") and all(srp.get(k_) == rp.get(k_) for k_ in ("compared", "n_fields", "n_differ", "max_scaled_diff", "d128_excluded")),
    "quantum_pillar_v384.reuse: reused True com a leitura v386 (ou False se calculou de novo, dito)": ((qp.get("reuse") or {}).get("reused") is True and (qp.get("reuse") or {}).get("reading") == ESP["muda_e_e_dito"]["quantum_pillar_v384_reuse"]["v386_esperado"]["reading"]) or computed,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE_MUDAR, "nao_pode_mudar": NAO_PODE_MUDAR, "muda_e_e_dito": MUDA_E_E_DITO, "vereditos_que_mudaram": dif,
       "verbo": {k: vb.get(k) for k in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "missing_flags", "token_matches_kernel", "verbatim_hashes_ok")},
       "ramo_b": {k: rb.get(k) for k in ("verdict", "all_verified", "read_ok", "conjunto_D_n", "beta", "F2b_status", "errors")},
       "errata": {k: le.get(k) for k in ("verdict", "all_verified", "v383_ledger_intact")},
       "declaracoes_fora_do_trio_ou_ausentes": [_nomes[f] for f, ok_ in _ax_trio.items() if not ok_],
       "pilar": {k: qp.get(k) for k in ("verdict", "mode", "key", "result_sha256", "custody_chain_ok", "reuse", "run_id")},
       "pilar_reuse_v386": {k: qr.get(k) for k in ("verdict", "reused", "result_sha256_matches_v385_sealed", "verdict_same_as_v385_sealed", "reuse_refused_detail")},
       "reprodutibilidade": {k: rp.get(k) for k in ("verdict", "compared", "why", "n_fields", "n_differ")},
       "timestamp_selo": selo.get("timestamp"), "um_version_selo": selo.get("um_version")}
for sec in ("deve_mudar", "nao_pode_mudar", "muda_e_e_dito"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if dif:
    print("vereditos que mudaram:", json.dumps(dif, ensure_ascii=False)[:3000])
if res["declaracoes_fora_do_trio_ou_ausentes"]:
    print("declaracoes fora do trio ou ausentes:", res["declaracoes_fora_do_trio_ou_ausentes"])
print("PILAR (informacao):", "REAPROVEITADO" if reused else ("CALCULADO DE NOVO" if computed else "nem um nem outro"), "|", V("quantum_pillar_reuse_v386"))
print("REPRODUTIBILIDADE v385 nesta rodada (muda e e' dito):", rp.get("verdict"))
# INFORMACAO (nao decide): o servidor do modelo nativo depois do rito, lido do log do lancador
_lg = os.path.join(HERE, "rito_servidor_v386.log")
_lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = ("PAROU DEPOIS DE ESCUTAR (o marcador ficou) -- conferir a tarefa" if "escutou e PAROU" in _lt else
                                  "ESCUTA, MAS A CONTAGEM DAS PARADAS NAO FOI LEGIVEL (o marcador ficou) -- conferir a tarefa" if "a contagem das paradas em curso nao foi legivel" in _lt else
                                  "ESCUTA, MAS HAVIA PARADA EM CURSO (o marcador ficou) -- conferir a tarefa" if ("ainda em curso" in _lt and ("ha parada (Stop-ScheduledTask" in _lt or "ha parada da tarefa" in _lt)) else
                                  "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt
                                  else ("AVISO: a porta 8081 nao escutou -- conferir a tarefa" if "AVISO: a porta 8081" in _lt else "sem registro no log do lancador")))
res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if re.match(r"^\d\d:\d\d:\d\d ", l_) and ("AVISO" in l_ or "FALHA VISIVEL" in l_)]
_sg = os.path.join(HERE, "rito_v386_sinal.txt")
res["sinais_desta_rodada"] = (open(_sg, encoding="utf-8", errors="replace").read().splitlines() if os.path.exists(_sg) else [])
_av_rel = [l_ for l_ in res["avisos_do_lancador"] if "AVISO_PID_VELHO" not in l_]
if _av_rel and res["servidor_depois_do_rito"].startswith("RELIGADO"):
    res["servidor_depois_do_rito"] = "RELIGADO COM AVISO: " + " | ".join(_av_rel)
print("servidor do modelo nativo depois do rito (informacao):", res["servidor_depois_do_rito"])
for l_ in res["avisos_do_lancador"]:
    print("  AVISO DO LANCADOR:", l_)
for l_ in res["sinais_desta_rodada"]:
    print("  SINAL/FALHA desta rodada (rito_v386_sinal.txt):", l_)
ok = all(DEVE_MUDAR.values()) and all(NAO_PODE_MUDAR.values()) and all(MUDA_E_E_DITO.values())
res["tudo_bate"] = ok
tag = sys.argv[1] if len(sys.argv) > 1 else ""
p = os.path.join(HERE, "conferencia_rito_v386%s.json" % tag)
with open(p + ".tmp", "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE")
sys.exit(0 if ok else 1)
