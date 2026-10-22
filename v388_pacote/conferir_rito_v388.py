# -*- coding: utf-8 -*-
"""conferir_rito_v388.py -- confere, DEPOIS do rito v388, o que tinha de mudar e o que NAO podia (ESPERADOS_v388.json; so leitura do Nos). Molde: conferir_rito_v387.py.
A unica mudanca dita nos vereditos da v387: '6137' -> '6154' (a escada cresce 17). O pilar: reaproveitado pela mesma chave, ou calculado de novo (dito, nao reprova)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v388.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
txt = {l: re.sub(r"\s+", " ", open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read()) for l in ("pt", "en")}
toc = {l: (open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read(); mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
stone = os.path.join(NOS, "tgl_kernel", "TGLExt", "TheCouplingRunsBoundedBelow.lean")
br, ho = core.get("beta_runs_bounded_below_v388") or {}, core.get("hubble_ratio_opening_v388") or {}
reused = qp.get("mode") == "REUSE"; computed = qp.get("mode") == "COMPUTE"
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v388; os 2 registros v388 no selo iguais ao core": selo.get("um_version") == "v388" and all((selo.get(k) or {}).get("verdict") == V(k) and V(k) for k in ("beta_runs_bounded_below_v388", "hubble_ratio_opening_v388")),
    "a escada subiu para 6154/6154": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == [6154, 6154],
    "a pedra nova no kernel do Nos com o sha do candidato": os.path.exists(stone) and hashlib.sha256(open(stone, "rb").read()).hexdigest()[:16] == ESP["pedra_sha16"],
    "as 17 bandeiras True e as 17 declaracoes no trio": all(kf.get(f) is True for f in ESP["flags_v388"]) and all(axr.get(n) is not None and set(axr.get(n) or []) <= TRIO for n in ESP["nomes_v388"]),
    "os 2 registros v388 SELARAM e = os pinados do ensaio": br.get("all_verified") is True and ho.get("all_verified") is True and all(V(k) == v for k, v in ESP["vereditos_v388_do_ensaio"].items()),
    "a funcao congelada reexecutada devolve o mesmo veredito da abertura": ho.get("same_verdict") is True,
    "o artigo PT/EN traz a secao v388 (antes da v387) e os 2 vereditos": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and all(V(k) in txt[l].replace(" ", "") or V(k) in txt[l] for l in ("pt", "en") for k in ESP["vereditos_v388_do_ensaio"])
        and all(txt[l].rfind(ESP["artigo_marcas"][l][0]) < txt[l].rfind(ESP["artigo_marcas"][l][-1]) for l in ("pt", "en")),
    "o sumario lista «Ao lado (v388)» e «(v387)»": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico com o carimbo v388 e a linha «Ao lado (v388)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_ao_lado"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "o pilar reaproveitado pela mesma chave -- ou calculado de novo, DITO": (reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"]) or computed,
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v387"].items() if V(k) != v}
ilegais = {k: x for k, x in mud.items() if x[0].replace("6137", "6154") != x[1]}
_ft = sorted(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "bandeiras True = as da v387 + as 17": _ft == sorted(set(ESP["flags_true_v387"]) | set(ESP["flags_v388"])),
    "vereditos da v387: so a troca dita 6137 -> 6154 (%d mudaram, todos por ela)" % len(mud): not ilegais,
    "as 9 leituras do selo e os registros v387 (exceto contagens da escada) inalterados": all(selo.get(k) == v for k, v in ESP["selo_leituras"].items())
        and all(json.dumps(selo.get(k), sort_keys=True) == json.dumps(v, sort_keys=True) for k, v in ESP["selo_registros_v387"].items()),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram": mud, "mudancas_ilegais": ilegais, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram (dito):", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
_lg = os.path.join(HERE, "rito_servidor_v388.log"); _lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt else "ver o log do lancador")
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
print("servidor:", res["servidor_depois_do_rito"], "| marcador ficou:", res["marcador_ficou"])
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v388%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
