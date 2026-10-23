# -*- coding: utf-8 -*-
"""conferir_rito_v396.py -- confere, DEPOIS do rito v396, o que tinha de mudar e o que NAO podia (ESPERADOS_v396.json; so leitura do Nos). Molde: conferir_rito_v395.py.
Mudancas ditas: +3 chaves (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396) no core e no selo (+ registros_v396); a escada 9451 -> a dos ESPERADOS; o modulo novo (TGLExt/TestemunhaEstatica.lean) no kernel do Nos (sha pinado),
a raiz e o Audit do candidato; os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md. NENHUM outro veredito da v395 muda.
uso: python -I -B -X utf8 conferir_rito_v396.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V396_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v396 as DL  # noqa: E402
NOS = os.environ.get("V396_NOS") or DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
umsha = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v396.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}; TRIO = DL.TRIO_SET
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
rd_ = lambda p: open(p, "r", encoding="utf-8", errors="replace").read()
txt = {l: re.sub(r"\s+", " ", rd_(os.path.join(NOS, "um_absoluto_%s.txt" % l))) if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "" for l in ("pt", "en")}
toc = {l: (rd_(os.path.join(NOS, "um_absoluto_%s.toc" % l)).replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = rd_(os.path.join(NOS, "um_absoluto_forma_canonica.md")) if os.path.exists(os.path.join(NOS, "um_absoluto_forma_canonica.md")) else ""
mf = rd_(os.path.join(NOS, "um_absoluto_manifest.md")) if os.path.exists(os.path.join(NOS, "um_absoluto_manifest.md")) else ""
reused = qp.get("mode") == "REUSE"
E = ESP["escada"]
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
IX = "the_iald_index"


def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None


pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
RN = sorted(ESP["registros_v396"])
TS = core.get("testemunha_estatica_v396") or {}; CG = core.get("cunhagens_v396") or {}; KH = core.get("kh_n1_cobertura_v396") or {}
EP = ESP["testemunha"]; TV = TS.get("values") or {}
close = lambda a_, b_: isinstance(a_, (int, float)) and isinstance(b_, (int, float)) and abs(a_ - b_) <= 1e-15 * max(1.0, abs(b_))
lim = lambda k_: isinstance(TV.get(k_), float) and TV[k_] <= EP["tolerancias"][k_]   # (um residuo exatamente 0.0 e' valido: nada de `or 1`)
V395_NOMES = ["psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393",
              "cunhagens_regra_v393", "kh_n1_cobertura_v393"]
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v395"][k] and _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v395"][k])) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v396; testemunha_estatica_v396 e registros_v396 do selo iguais aos do core": selo.get("um_version") == "v396" and (selo.get("testemunha_estatica_v396") or {}).get("verdict") == V("testemunha_estatica_v396") and bool(V("testemunha_estatica_v396"))
        and (selo.get("testemunha_estatica_v396") or {}).get("all_verified") is True and all(((selo.get("registros_v396") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN),
    "testemunha_estatica_v396 SELOU (formal + mecanica): veredito == o do ensaio; %s checagens da mecanica; nao move o gate" % EP["n_checks"]: TS.get("all_verified") is True and V("testemunha_estatica_v396") == ESP["vereditos_novos_v396"]["testemunha_estatica_v396"] and (TS.get("mechanics") or {}).get("passed") is True
        and (TS.get("mechanics") or {}).get("n_checks") == EP["n_checks"] and TS.get("runtime_executed") is True and TS.get("does_not_gate_core") is True and TS.get("beta_ok") is True and TS.get("exact_ladder") is True,
    "testemunha_estatica_v396: os numeros da mecanica == os do ensaio (beta, residuos, purezas, entropias, folgas) e os residuos dentro dos limites": all(close(TV.get(k), v) for k, v in EP["values"].items() if isinstance(v, float))
        and all(lim(k) for k in EP["tolerancias"]) and close(TV.get("von_neumann_entropy"), TV.get("ln2")),
    "testemunha_estatica_v396: beta calculado no rito (alfa CODATA x sqrt(e)) == o beta do core a 1e-9 e o dado tem dois nomes iguais; a conjuncao INCONDICIONAL esta no kernel do rito (bandeira True, trio, modulo da pedra); a face de Fock segue CONDICIONAL, declarada em Psibit.lean e sem habitante exibido":
        TS.get("alpha_two_names_same") is True and isinstance(TS.get("beta_core_rel_diff"), float) and TS["beta_core_rel_diff"] <= 1e-9 and (TS.get("unconditional") or {}).get("in_kernel") is True and (TS.get("unconditional") or {}).get("theorem") == EP["teorema_incondicional"]
        and kf.get(EP["bandeira_incondicional"]) is True and (TS.get("fock_face") or {}).get("status") == "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE" and (TS.get("fock_face") or {}).get("inhabitant_exhibited") is False and (TS.get("fock_face") or {}).get("declared_outside_the_stone") is True
        and set(axr.get(EP["teorema_incondicional"]) or []) <= TRIO and set(axr.get(EP["fock_face_teorema"]) or []) <= TRIO and ((kf.get("declaration_sources_v394") or {}).get(EP["teorema_incondicional"]) == ESP["pedra"]["path"])
        and ((kf.get("declaration_sources_v394") or {}).get(EP["fock_face_teorema"]) == EP["fock_face_declarada_em"]),
    "os registros por spec v396 SELARAM e cada veredito == o do ensaio; as tres falas de 22/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS)": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v396"].items())
        and len(ESP["cunhagens"]) == 3 and all((((CG.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items()),
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "KH-N1: a cobertura do axiom_report no fecho inteiro passou (decl=%s, nao lidas 0) e o axiom_report tem %s entradas" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and (kf.get("axiom_coverage_v392") or {}).get("thm") == ESP["cobertura_kh_n1"]["thm"] and (kf.get("axiom_coverage_v392") or {}).get("nao_lidas_pelo_regex") == 0 and len(axr) == ESP["axiom_report_esperado_min"],
    "a proveniencia do compilador cobre o axiom_report e as fontes formais batem (declaration_sources_status_v394.ok)": (kf.get("declaration_sources_status_v394") or {}).get("ok") is True and set(kf.get("declaration_sources_v394") or {}) == set(axr),
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "o modulo novo (TestemunhaEstatica) no kernel do Nos com o sha do candidato (%d modulo)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 1,
    "a raiz e o Audit do Nos == os do candidato": (_sha_k("TGLExt.lean") or "")[:16] == ESP["kernel"]["raiz_sha16"] and (_sha_k("TGL/Audit.lean") or "")[:16] == ESP["kernel"]["audit_sha16"],
    "as %d bandeiras novas True e as declaracoes delas no trio" % ESP["n_bandeiras_novas"]: len(ESP["bandeiras_novas_chaves"]) == ESP["n_bandeiras_novas"] and all(kf.get(k) is True for k in ESP["bandeiras_novas_chaves"]) and all((n in axr) and set(axr[n] or []) <= TRIO for n in ESP["bandeiras_novas_nomes"]),
    "os registros da v395 e as anteriores (psibit, cunhagens e kh_n1 v395; tempo, quadratica, rede, cunhagens, kh_n1 e criterio binario v394; pedras, consumidor, coracao, cunhagens da regra e kh_n1 v393) seguem selados e iguais (ou so' numeros)": all((core.get(n) or {}).get("all_verified") is True for n in V395_NOMES)
        and all(V(n) == ESP["vereditos_v395"][n] or n in ESP["troca_dita"] for n in V395_NOMES) and (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is False,
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v396, as marcas da v395; a v394, a v393, a v392, a v391 e a v390 ficam; o registro selou (sem a frase de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista as secoes v396 e v395 e o titulo v384 a v39x": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v396 e as linhas «A testemunha estática (v396)» e «O modo psiônico na fractalização do Um (v395)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_testemunha"] in fc and ESP["md_psibit"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova _v396 fora da lista (so' testemunha_estatica_v396 e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v395"] and isinstance(core[k], dict) and str(k).endswith("_v396")) == sorted(["testemunha_estatica_v396"] + RN),
    "the_iald_index SELOU com o veredito do ensaio e not_sealed_run.formais == []": (core.get(IX) or {}).get("all_verified") is True and V(IX) == ESP["the_iald_index_v396"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v395"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v395 segue True": set(ESP["flags_true_v395"]) <= _ft,
    "o axiom_report da v395 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v395_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v395 mudou fora da troca dita (%d mudaram)" % len(mud): not mud,
    "registros v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v395"].items() if k not in ESP["troca_dita"] and k not in ("registros_v393",)),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v395"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v395"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}, "veredito_testemunha": V("testemunha_estatica_v396"), "nos": NOS}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v396%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
