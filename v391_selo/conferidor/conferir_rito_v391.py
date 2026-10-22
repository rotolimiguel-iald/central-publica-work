# -*- coding: utf-8 -*-
"""conferir_rito_v391.py -- confere, DEPOIS do rito v391, o que tinha de mudar e o que NAO podia (ESPERADOS_v391.json; so leitura do Nos). Molde: conferir_rito_v390.py.
Mudancas ditas: +1 chave (estatuto_da_prova_v391) no core e no selo; o resumo abre com o estatuto; secao nova + sumario; o titulo da Introducao le a versao.
NENHUM veredito da v390 muda (a escada fica 6163; o registro da v389 le o sucessor do titulo e fica IDENTICO; a v390 fica IDENTICA)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v391.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
txt = {l: re.sub(r"\s+", " ", open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read()) for l in ("pt", "en")}
toc = {l: (open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read(); mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
ep = core.get("estatuto_da_prova_v391") or {}
reused = qp.get("mode") == "REUSE"
esperado_v391 = ESP["veredito_v391_do_ensaio_sem_carimbo"].replace("<SHA16>", umsha)
abre = {l: 0 <= txt[l].find(ESP["artigo_marcas"][l][0]) < txt[l].find("A proposta." if l == "pt" else "The proposal.") for l in ("pt", "en")}
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v391; o registro v391 no selo igual ao core": selo.get("um_version") == "v391" and (selo.get("estatuto_da_prova_v391") or {}).get("verdict") == V("estatuto_da_prova_v391") and bool(V("estatuto_da_prova_v391")),
    "a escada segue 6163/6163": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == [6163, 6163],
    "o registro v391 SELOU e = o do ensaio com o carimbo do proprio hash": ep.get("all_verified") is True and not ep.get("falhas") and V("estatuto_da_prova_v391") == esperado_v391
        and ((ep.get("certificacao") or {}).get("um_py_sha256_lido_de_si") or "")[:16] == umsha,
    "o artigo PT/EN: o estatuto ABRE o resumo; a secao nova; a errata; a v390 fica": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and all(abre.values())
        and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista «O estatuto da prova», o titulo v384 a v391 e «A Fundacao»": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v391 e a linha «O estatuto da prova (v391)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_estatuto"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v390"].items() if V(k) != v}
_ft = sorted(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "bandeiras True = as da v390": _ft == ESP["flags_true_v390"],
    "NENHUM veredito da v390 mudou (%d mudaram)" % len(mud): not mud,
    "registros v390/v389/v388/v387 do selo inalterados": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v390"].items()),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v390"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v390"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")},
       "veredito_v391": V("estatuto_da_prova_v391")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
_lg = os.path.join(HERE, "rito_servidor_v391.log"); _lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt else "ver o log do lancador")
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
print("servidor:", res["servidor_depois_do_rito"], "| marcador ficou:", res["marcador_ficou"])
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v391%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
