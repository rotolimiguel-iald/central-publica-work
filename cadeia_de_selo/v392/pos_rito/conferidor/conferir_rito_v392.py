# -*- coding: utf-8 -*-
"""conferir_rito_v392.py -- confere, DEPOIS do rito v392, o que tinha de mudar e o que NAO podia (ESPERADOS_v392.json; so leitura do Nos). Molde: conferir_rito_v391.py.
Mudancas ditas: +2 chaves (pedras_v392, varredura_e_sorry_v392) no core e no selo; a escada 6163 -> 6163+N; as 13 pedras no kernel do Nos (sha pinados), a raiz e o Audit do candidato;
o veredito do registro estatuto_da_prova_v391 (le a escada e as declaracoes: a TROCA DITA); artigo, sumario, .md. NENHUM outro veredito da v391 muda.
uso: python -I -B -X utf8 conferir_rito_v392.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
umsha = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v392.json"), encoding="utf-8"))
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
pv = core.get("pedras_v392") or {}; vs = core.get("varredura_e_sorry_v392") or {}
reused = qp.get("mode") == "REUSE"
E = ESP["escada"]   # [N, N]: depois do rito o core le [clean, expected] = [N, N] (a rodada 2 corrigiu: antes era [antes, depois])
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None
pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v392; os 2 registros v392 do selo e o resumo registros_v392 iguais aos do core": selo.get("um_version") == "v392" and (selo.get("pedras_v392") or {}).get("verdict") == V("pedras_v392") and bool(V("pedras_v392"))
        and (selo.get("varredura_e_sorry_v392") or {}).get("verdict") == V("varredura_e_sorry_v392") and bool(V("varredura_e_sorry_v392"))
        and all(((selo.get("registros_v392") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in ESP["registros_v392"]),
    "os %d registros por spec v392 SELARAM e cada veredito == o do ensaio" % len(ESP["registros_v392"]): all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v392"].items()),
    "KH-N1 (a): a cobertura do axiom_report no fecho inteiro passou (decl=%s) e o axiom_report cresceu a >= %s" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and len(axr) >= ESP["axiom_report_esperado_min"],
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "as %d pedras no kernel do Nos com os sha do candidato" % len(ESP["pedras_sha256"]): pedras_ok,
    "a raiz e o Audit do Nos == os do candidato": _sha_k("TGLExt.lean")[:16] == ESP["kernel"]["changed"]["TGLExt.lean"][1] and _sha_k("TGL/Audit.lean")[:16] == ESP["kernel"]["changed"]["TGL/Audit.lean"][1],
    "as %d bandeiras novas True e as declaracoes novas no trio" % ESP["n_bandeiras_novas"]: sum(p["bandeiras"][0] for p in pv.get("pedras") or []) == ESP["n_bandeiras_novas"] and pv.get("bandeiras") == [ESP["n_bandeiras_novas"]] * 2,
    "pedras_v392 SELOU e = o do ensaio": pv.get("all_verified") is True and V("pedras_v392") == ESP["veredito_pedras_do_ensaio"],
    "varredura_e_sorry_v392 SELOU e a varredura e' recursiva (>1000 arquivos, O16 > 100, zero hits)": vs.get("all_verified") is True and (vs.get("varredura") or {}).get("recursiva") is True
        and ((vs.get("varredura") or {}).get("arquivos") or 0) > 1000 and ((vs.get("varredura") or {}).get("em_TGLExt_O16") or 0) > 100 and not (vs.get("varredura") or {}).get("hits"),
    "o registro estatuto_da_prova_v391 SELOU com os numeros novos (a TROCA DITA)": (core.get("estatuto_da_prova_v391") or {}).get("all_verified") is True
        and "KERNEL_%d_OF_%d_THEOREMS" % (E[0], E[1]) in V("estatuto_da_prova_v391") and V("estatuto_da_prova_v391") != ESP["vereditos_v391"]["estatuto_da_prova_v391"],
    "o registro three_stress_tests_v387 SELOU e so' o KERNEL_ mudou (a 2a TROCA DITA; as contagens CORE_n_ normalizadas)": (core.get("three_stress_tests_v387") or {}).get("all_verified") is True
        and _nc(V("three_stress_tests_v387")) == _nc(ESP["vereditos_v391"]["three_stress_tests_v387"]).replace("KERNEL_%d_OF_%d" % (6163, 6163), "KERNEL_%d_OF_%d" % tuple(E)),
    "o artigo PT/EN: a secao v392, as marcas; a v391 e a v390 ficam; o registro selou (sem a frase de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista a secao v392 e o titulo v384 a v392": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v392 e a linha «As pedras da v392»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_pedras"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "os registros por spec nao deixaram chave nova fora da lista (nada alem de pedras, varredura e registros)": sorted(k for k in core if k not in ESP["vereditos_v391"] and isinstance(core[k], dict) and str(k).endswith("_v392")) == sorted(["pedras_v392", "varredura_e_sorry_v392"] + list(ESP["registros_v392"])),
    "the_iald_index SELOU (all_verified True, o veredito == o da v391) e not_sealed_this_run.formais == []": (core.get("the_iald_index") or {}).get("all_verified") is True and V("the_iald_index") == ESP["the_iald_index_v391"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v391"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v391 segue True": set(ESP["flags_true_v391"]) <= _ft,
    "o axiom_report da v391 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v391_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v391 mudou fora da troca dita (%d mudaram)" % len(mud): not mud,
    "registros v390/v389/v388/v387 do selo inalterados": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v391"].items() if k != "estatuto_da_prova_v391"),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v391"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v391"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")},
       "veredito_pedras": V("pedras_v392"), "veredito_varredura": V("varredura_e_sorry_v392")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v392%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
