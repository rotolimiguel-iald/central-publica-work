# -*- coding: utf-8 -*-
"""conferir_rito_v394.py -- confere, DEPOIS do rito v394, o que tinha de mudar e o que NAO podia (ESPERADOS_v394.json; so leitura do Nos). Molde: conferir_rito_v393.py.
Mudancas ditas: +6 chaves (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394, criterio_binario_de_parada_v394) no core e no selo (+ registros_v394); a escada 7045 -> a dos ESPERADOS; os modulos novos (189 do Codex + a pedra do delta) no kernel
do Nos (sha pinados), a raiz e o Audit do candidato; os vereditos da TROCA DITA (so' numeros); o veredito do indice (mudanca declarada); artigo, sumario, .md. NENHUM outro veredito da v393 muda.
uso: python -I -B -X utf8 conferir_rito_v394.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
umsha = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v394.json"), encoding="utf-8"))
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
tf = core.get("tempo_frequencia_v394") or {}; rq = core.get("regra_quadratica_v394") or {}; rf = core.get("rede_fock_v394") or {}
reused = qp.get("mode") == "REUSE"
E = ESP["escada"]
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
IX = "the_iald_index"
def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None
pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
RN = sorted(ESP["registros_v394"])
TP = ESP.get("troca_de_palavra") or {}   # a TROCA DE PALAVRA declarada pela gerencia (THEOREMS -> FLAGS em estatuto_da_prova_v391): so' o que os ESPERADOS declaram
_pw = lambda k, s_: s_.replace(TP[k][0], TP[k][1]) if k in TP else s_
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v393"][k] and _num(_nc(V(k))) == _num(_nc(_pw(k, ESP["vereditos_v393"][k]))) and (k not in TP or (TP[k][1] in V(k) and TP[k][0] not in V(k))) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros (mais a palavra declarada)
CB = core.get("criterio_binario_de_parada_v394") or {}
# (n in axr): a lista VAZIA (declaracao sem axioma algum) e' valida; so' a AUSENCIA reprova. Achado do teste positivo de 19/10: o antigo `set(axr.get(n) or ["?"])` reprovava as bandeiras de lista vazia (12 das 3707 do candidato anterior; 2 das 2287 de agora).
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v394; os 3 registros v394 do selo e o resumo registros_v394 iguais aos do core": selo.get("um_version") == "v394" and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"))
        and all(((selo.get("registros_v394") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN),
    "os registros por spec v394 SELARAM e cada veredito == o do ensaio": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v394"].items()),
    "o registro criterio_binario_de_parada_v394 SELOU: veredito == o do ensaio; as duas falas de 19/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS); a bandeira e o teorema da pedra no kernel do rito, no trio": CB.get("all_verified") is True and V("criterio_binario_de_parada_v394") == ESP["criterio_binario"]["verdict"]
        and all(((CB.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True and ((CB.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"] for k_, v_ in ESP["criterio_binario"]["verbatim"].items()) and len(ESP["criterio_binario"]["verbatim"]) == 2
        and kf.get(ESP["bandeira_do_delta"]) is True and (ESP["teorema_do_delta"] in axr and set(axr[ESP["teorema_do_delta"]] or []) <= TRIO) and ((kf.get("declaration_sources_v394") or {}).get(ESP["teorema_do_delta"]) == ESP["pedra_do_delta"]["path"]),
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "tempo_frequencia_v394, regra_quadratica_v394 e rede_fock_v394 SELARAM e cada veredito == o do ensaio; nenhum certificado inteiro da rede": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["vereditos_novos_v394"].items()) and rf.get("whole_certificate_inhabited") is False,
    "as contagens formais == as do ensaio (tempo, quadratica, rede, fontes da rede)": {"tempo": len(tf.get("formal_theorems") or {}), "quadratica": len(rq.get("formal_theorems") or {}), "rede": len(rf.get("formal_declarations") or {}), "rede_fontes": len(rf.get("embedded_sources") or {})} == ESP["n_formais"],
    "KH-N1: a cobertura do axiom_report no fecho inteiro passou (decl=%s, nao lidas 0) e o axiom_report tem %s entradas" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and (kf.get("axiom_coverage_v392") or {}).get("nao_lidas_pelo_regex") == 0 and len(axr) == ESP["axiom_report_esperado_min"],
    "a proveniencia do compilador cobre o axiom_report e as fontes formais batem (declaration_sources_status_v394.ok)": (kf.get("declaration_sources_status_v394") or {}).get("ok") is True and set(kf.get("declaration_sources_v394") or {}) == set(axr),
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "os %d modulos novos no kernel do Nos com os sha do candidato" % len(ESP["pedras_sha256"]): pedras_ok,
    "a raiz e o Audit do Nos == os do candidato": _sha_k("TGLExt.lean")[:16] == ESP["kernel"]["raiz_sha16"] and _sha_k("TGL/Audit.lean")[:16] == ESP["kernel"]["audit_sha16"],
    "as %d bandeiras novas True e as declaracoes delas no trio" % ESP["n_bandeiras_novas"]: len(ESP["bandeiras_novas_chaves"]) == ESP["n_bandeiras_novas"] and all(kf.get(k) is True for k in ESP["bandeiras_novas_chaves"]) and all((n in axr) and set(axr[n] or []) <= TRIO for n in ESP["bandeiras_novas_nomes"]),
    "os 5 registros da v393 (pedras, consumidor, coracao, cunhagens da regra, cobertura v393) seguem selados e iguais (ou so' numeros)": all((core.get(n) or {}).get("all_verified") is True for n in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393"))
        and all(V(n) == ESP["vereditos_v393"][n] or n in ESP["troca_dita"] for n in ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")),
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v394, o bloco final do Codex, as marcas; a v393, a v392, a v391 e a v390 ficam; o registro selou (sem a frase de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista a secao v394 e o titulo v384 a v39x": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v394 e a linha «A integração do Codex»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_integracao"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova _v394 fora da lista (so' tempo, quadratica, rede e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v393"] and isinstance(core[k], dict) and str(k).endswith("_v394")) == sorted(["tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394"] + RN),
    "the_iald_index SELOU com o veredito do indice qualificado (mudanca declarada) e not_sealed_this_run.formais == []": (core.get(IX) or {}).get("all_verified") is True and V(IX) == ESP["the_iald_index_v394"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v393"].items() if V(k) != v and k not in ESP["troca_dita"] and k != IX}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v393 segue True": set(ESP["flags_true_v393"]) <= _ft,
    "o axiom_report da v393 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v393_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v393 mudou fora da troca dita e do indice (%d mudaram)" % len(mud): not mud,
    "registros v393/v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v393"].items() if k not in ESP["troca_dita"] and k != "registros_v393"),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v393"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v393"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")},
       "veredito_tempo": V("tempo_frequencia_v394"), "veredito_quadratica": V("regra_quadratica_v394"), "veredito_rede": V("rede_fock_v394")}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v394%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
