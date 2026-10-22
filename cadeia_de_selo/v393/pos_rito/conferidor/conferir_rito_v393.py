# -*- coding: utf-8 -*-
"""conferir_rito_v393.py -- confere, DEPOIS do rito v393, o que tinha de mudar e o que NAO podia (ESPERADOS_v393.json; so leitura do Nos). Molde: conferir_rito_v392.py.
Mudancas ditas: +4 chaves (pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393, cunhagens_regra_v393) no core e no selo (+ registros_v393); a escada 6901 -> 6901+N; as 3 pedras no kernel
do Nos (sha pinados), a raiz e o Audit do candidato; os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md. NENHUM outro veredito da v392 muda.
uso: python -I -B -X utf8 conferir_rito_v393.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
umsha = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v393.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}; TRIO = {"propext", "Classical.choice", "Quot.sound"}
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
rd_ = lambda p: open(p, "r", encoding="utf-8", errors="replace").read()
txt = {l: re.sub(r"\s+", " ", rd_(os.path.join(NOS, "um_absoluto_%s.txt" % l))) if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "" for l in ("pt", "en")}
toc = {l: (rd_(os.path.join(NOS, "um_absoluto_%s.toc" % l)).replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = rd_(os.path.join(NOS, "um_absoluto_forma_canonica.md")); mf = rd_(os.path.join(NOS, "um_absoluto_manifest.md"))
pv = core.get("pedras_v393") or {}; rc = core.get("regra_consumidor_v393") or {}; cr = core.get("coracao_e_selo_gravitacional_v393") or {}
reused = qp.get("mode") == "REUSE"
E = ESP["escada"]
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))   # so numeros e o sha16 do proprio um.py (o selo se certifica pelo self-hash)
def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None
pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
RN = sorted(ESP["registros_v393"])
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v392"][k] and _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v392"][k])) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v393; os 3 registros v393 do selo e o resumo registros_v393 iguais aos do core": selo.get("um_version") == "v393" and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"))
        and all(((selo.get("registros_v393") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN),
    "os registros por spec v393 SELARAM e cada veredito == o do ensaio": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v393"].items()),
    "KH-N1 (a): a cobertura do axiom_report no fecho inteiro passou (decl=%s) e o axiom_report cresceu a >= %s" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and len(axr) >= ESP["axiom_report_esperado_min"],
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "as %d pedras no kernel do Nos com os sha do candidato" % len(ESP["pedras_sha256"]): pedras_ok,
    "a raiz e o Audit do Nos == os do candidato": _sha_k("TGLExt.lean")[:16] == ESP["kernel"]["changed"]["TGLExt.lean"][1] and _sha_k("TGL/Audit.lean")[:16] == ESP["kernel"]["changed"]["TGL/Audit.lean"][1],
    "as %d bandeiras novas True e as declaracoes novas no trio" % ESP["n_bandeiras_novas"]: sum(p["bandeiras"][0] for p in pv.get("pedras") or []) == ESP["n_bandeiras_novas"] and pv.get("bandeiras") == [ESP["n_bandeiras_novas"]] * 2,
    "pedras_v393 SELOU e = o do ensaio": pv.get("all_verified") is True and V("pedras_v393") == ESP["veredito_pedras_do_ensaio"],
    "regra_consumidor_v393 SELOU, o alvo correto e' ADMITIDO e o incompativel RECUSADO (veredito == o do ensaio); a igualdade exata nao e' afirmada": rc.get("all_verified") is True and V("regra_consumidor_v393") == ESP["veredito_consumidor_do_ensaio"]
        and (rc.get("satisfacao") or {}).get("veredito_do_rito") == "SATISFACTION_ADMITTED" and (rc.get("satisfacao") or {}).get("veredito_incompativel") == "SATISFACTION_REFUSED" and (rc.get("criterio") or {}).get("igualdade_exata_afirmada") is False,
    "o consumidor: mesmos numeros do ensaio (verificacoes, pontos, dimensao fixa 8, complemento inicial e final)": {k: (rc.get("numeros") or {}).get(k) for k in ("verificacoes", "pontos", "dimensao_fixa_complexa", "complemento_inicial", "complemento_final")}
        == {k: ESP["numeros_do_consumidor"].get(k) for k in ("verificacoes", "pontos", "dimensao_fixa_complexa", "complemento_inicial", "complemento_final")},
    "coracao_e_selo_gravitacional_v393 SELOU = o do ensaio (CODATA reconstruido, sem previsao independente, G nao derivado, controles negativos recusam)": cr.get("all_verified") is True and V("coracao_e_selo_gravitacional_v393") == ESP["veredito_coracao_do_ensaio"]
        and cr.get("previsao_independente") is False and cr.get("G_derivado") is False and cr.get("controles_ok") is True and cr.get("does_not_gate_core") is True and (cr.get("satisfacao_pela_regra") or {}).get("admitida") is True,
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v393, o quadro do coracao, as marcas; a v392, a v391 e a v390 ficam; o registro selou (sem a frase de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista a secao v393 e o titulo v384 a v393": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v393 e a linha «A regra e o coracao»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_regra"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova _v393 fora da lista (so' pedras, consumidor, coracao e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v392"] and isinstance(core[k], dict) and str(k).endswith("_v393")) == sorted(["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393"] + RN),
    "the_iald_index SELOU (all_verified True, o veredito == o da v392) e not_sealed_this_run.formais == []": (core.get("the_iald_index") or {}).get("all_verified") is True and V("the_iald_index") == ESP["the_iald_index_v392"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v392"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v392 segue True": set(ESP["flags_true_v392"]) <= _ft,
    "o axiom_report da v392 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v392_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v392 mudou fora da troca dita (%d mudaram)" % len(mud): not mud,
    "registros v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v392"].items() if k not in ESP["troca_dita"]),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v392"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v392"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")},
       "veredito_pedras": V("pedras_v393"), "veredito_consumidor": V("regra_consumidor_v393"), "veredito_coracao": V("coracao_e_selo_gravitacional_v393")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v393%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
