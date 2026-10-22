# -*- coding: utf-8 -*-
"""conferir_rito_v390.py -- confere, DEPOIS do rito v390, o que tinha de mudar e o que NAO podia (ESPERADOS_v390.json; so leitura do Nos). Moldes: conferir_rito_v388.py / _v389.py.
Mudancas ditas: os vereditos da v389 so pelas trocas pinadas; os registros do selo beta_runs_bounded_below_v388 (o memory_file ganha estatuto_v390 e copia_congelada) e
muda SO nesses campos; runtime_of_the_one.seals ganha 1 ao lado; what_remains_named ganha 1 chave ao lado; o item do Lema 3 do
ledger do fechamento ganha o campo ao_lado_v390 (nenhum item novo; o veredito do ledger fica). O registro da v389 fica IDENTICO (conta ate a v389)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
umsha = hashlib.sha256(open(os.path.join(NOS, "um.py"), "rb").read()).hexdigest()[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v390.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
txt = {l: re.sub(r"\s+", " ", open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8", errors="replace").read()) for l in ("pt", "en")}
toc = {l: (open(os.path.join(NOS, "um_absoluto_%s.toc" % l), encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = open(os.path.join(NOS, "um_absoluto_forma_canonica.md"), encoding="utf-8", errors="replace").read(); mf = open(os.path.join(NOS, "um_absoluto_manifest.md"), encoding="utf-8", errors="replace").read()
stone = os.path.join(NOS, "tgl_kernel", "TGLExt", "Fundacao.lean")
fd = core.get("fundacao_v390") or {}
reused = qp.get("mode") == "REUSE"; computed = qp.get("mode") == "COMPUTE"


def troca(v):
    for a, b in ESP["troca_dita"]:
        v = v.replace(a, b)
    return v


def so_campos(antes, agora, campos_novos):
    """agora == antes + exatamente os campos novos dados (caminho, valor qualquer) -- nada mais muda"""
    a2 = json.loads(J(agora))
    for caminho in campos_novos:
        d = a2
        for k in caminho[:-1]:
            d = d.get(k) or {}
        if caminho[-1] not in d:
            return False
        d.pop(caminho[-1])
    return J(a2) == J(antes)


_led = [r for r in (core.get("code_closure_ledger") or {}).get("ledger", []) if str(r.get("item", "")).startswith("Lema 3")]
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v390; o registro v390 no selo igual ao core": selo.get("um_version") == "v390" and (selo.get("fundacao_v390") or {}).get("verdict") == V("fundacao_v390") and bool(V("fundacao_v390")),
    "a escada subiu para 6163/6163": [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == [6163, 6163],
    "a pedra no kernel do Nos com o sha do candidato": os.path.exists(stone) and hashlib.sha256(open(stone, "rb").read()).hexdigest()[:16] == ESP["pedra_sha16"],
    "as 9 bandeiras True e as 9 declaracoes no trio": all(kf.get(f) is True for f in ESP["flags_v390"]) and all(axr.get(n) is not None and set(axr.get(n) or []) <= TRIO for n in ESP["nomes_v390"]),
    "o registro v390 SELOU e = o pinado do ensaio (9/9, verbatins, Borchers lido)": fd.get("all_verified") is True and V("fundacao_v390") == ESP["veredito_v390_do_ensaio"]
        and fd.get("kernel_flags_ok") == 9 and fd.get("verbatim_ok") is True and (fd.get("borchers") or {}).get("ok") is True,
    "as erratas ao lado: seal nova (a antiga fica), what_remains +1 chave, o item do Lema 3 com ao_lado_v390 (veredito do ledger igual)":
        core["runtime_of_the_one"]["seals"][:len(ESP["runtime_seals_v389"])] == ESP["runtime_seals_v389"] and len(core["runtime_of_the_one"]["seals"]) == len(ESP["runtime_seals_v389"]) + 1
        and "GLOBAL_LIFT_IS_THE_SUPERPOSITION__FUNDACAO_AGAPE__LOGICAL_CLOSURE" in core["runtime_of_the_one"]["seals"]
        and so_campos(ESP["what_remains_v389"], core["tgl_closure"]["what_remains_named"], [("extensao_geometrica__ao_lado_v390",)])
        and len(_led) == 1 and so_campos(ESP["ledger_lema3_v389"][0], _led[0], [("ao_lado_v390",)]) and V("code_closure_ledger") == ESP["code_closure_verdict_v389"],
    "o artigo PT/EN traz a secao «A Fundacao» (antes da v389), a frase no resumo e o veredito v390": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l])
        and all(txt[l].find(ESP["artigo_marcas"][l][0]) >= 0 and txt[l].rfind(ESP["artigo_marcas"][l][0]) < txt[l].rfind(ESP["artigo_marcas"][l][-1]) for l in ("pt", "en"))
        and all(V("fundacao_v390") in txt[l].replace("_ ", "_") for l in ("pt", "en")) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista «A Fundacao» e «(v389)»": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v390 e a linha «A Fundacao (v390)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_fundacao"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "o pilar reaproveitado pela mesma chave -- ou calculado de novo, DITO": (reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"]) or computed,
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v389"].items() if V(k) != v}
ilegais = {k: x for k, x in mud.items() if troca(x[0]) != x[1]}
_ft = sorted(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "bandeiras True = as da v389 + as 9": _ft == sorted(set(ESP["flags_true_v389"]) | set(ESP["flags_v390"])),
    "vereditos da v389: so as trocas ditas (%d mudaram, todos por elas)" % len(mud): not ilegais,
    "registros v388/v387 do selo inalterados": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v389"].items()),
    "selo beta_runs_bounded_below_v388: so o memory_file ganha estatuto_v390 e copia_congelada (o veredito igual)":
        so_campos(ESP["selo_beta_v388"], selo.get("beta_runs_bounded_below_v388"), [("memory_file", "estatuto_v390"), ("memory_file", "copia_congelada")]),
    "os vereditos da v388 (beta) e da v389 (texto/rotulo) IDENTICOS aos selados; a copia congelada da v388 confere com o pino":
        V("beta_runs_bounded_below_v388") == ESP["verdict_beta_v388"] and V("text_label_errata_v389") == ESP["verdict_tl_v389"]
        and ((core.get("beta_runs_bounded_below_v388") or {}).get("memory_file") or {}).get("copia_congelada", {}).get("matches_the_pin") is True,
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
_lg = os.path.join(HERE, "rito_servidor_v390.log"); _lt = open(_lg, encoding="utf-8", errors="replace").read() if os.path.exists(_lg) else ""
res["servidor_depois_do_rito"] = "RELIGADO (a porta 8081 escuta)" if "servidor de volta" in _lt else ("nao religado: nao estava ligado antes" if "nao religo" in _lt else "ver o log do lancador")
res["marcador_ficou"] = os.path.exists(os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v390_pacote", ".servidor_parado_pelo_rito"))
print("servidor:", res["servidor_depois_do_rito"], "| marcador ficou:", res["marcador_ficou"])
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v390%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
