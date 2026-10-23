# -*- coding: utf-8 -*-
"""conferir_rito_v397.py -- confere, DEPOIS do rito v397, o que tinha de mudar e o que NAO podia (ESPERADOS_v397.json; so leitura do Nos). Molde: conferir_rito_v396.py.
Mudancas ditas: +3 chaves (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397) no core e no selo (+ registros_v397); a escada 9498 -> a dos ESPERADOS; o modulo novo (TGLExt/Token.lean) no kernel do Nos (sha pinado), a raiz e o Audit do
candidato; os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md; E O QUADRO «O Teste da Unica Palavra» NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado (ordem do operador de 23/10: reportar o 4,44 no inicio) e a regra da
ordem (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma). NENHUM outro veredito da v396 muda.
uso: python -I -B -X utf8 conferir_rito_v397.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V397_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
NOS = os.environ.get("V397_NOS") or DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
umsha = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v397.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}; TRIO = DL.TRIO_SET
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
rd_ = lambda p: open(p, "r", encoding="utf-8", errors="replace").read()
raw_txt = {l: (rd_(os.path.join(NOS, "um_absoluto_%s.txt" % l)) if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
txt = {l: re.sub(r"\s+", " ", raw_txt[l]) for l in ("pt", "en")}
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


# o RESULTADO pinado do Teste da Unica Palavra: o original (so' leitura) se o sha256 bate; senao a copia duravel; os numeros do quadro/registro/selo sao comparados com ESTES
EV = ESP["veracidade"]; EQ = ESP["quadro"]
_orig_ok = os.path.exists(EV["resultado"]["original"]) and sha(open(EV["resultado"]["original"], "rb").read()) == EV["resultado"]["sha256"]
_dur_ok = os.path.exists(EV["resultado"]["duravel"]) and sha(open(EV["resultado"]["duravel"], "rb").read()) == EV["resultado"]["sha256"]
RES = json.load(open(EV["resultado"]["original"] if _orig_ok else EV["resultado"]["duravel"], encoding="utf-8")) if (_orig_ok or _dur_ok) else {}
NUM = {k: DL.lido(RES, c) for k, c in DL.F9_CAMINHOS.items()} if RES else {}
pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
RN = sorted(ESP["registros_v397"])
TV = core.get("teste_de_veracidade_fase9_v397") or {}; CG = core.get("cunhagens_v397") or {}; KH = core.get("kh_n1_cobertura_v397") or {}
LD = TV.get("lido") or {}
q_pt = QV.confere_txt(raw_txt["pt"], RES, "pt") if (RES and raw_txt["pt"]) else {"ok": False}; q_en = QV.confere_txt(raw_txt["en"], RES, "en") if (RES and raw_txt["en"]) else {"ok": False}
q_md = QV.confere_md(fc, RES) if (RES and fc) else {"ok": False}
V396_NOMES = ["testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "pedras_v393",
              "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393"]
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v396"][k] and _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v396"][k])) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v397; teste_de_veracidade_fase9_v397 e registros_v397 do selo iguais aos do core (veredito, selagem e os numeros lidos)": selo.get("um_version") == "v397" and (selo.get("teste_de_veracidade_fase9_v397") or {}).get("verdict") == V("teste_de_veracidade_fase9_v397") and bool(V("teste_de_veracidade_fase9_v397"))
        and (selo.get("teste_de_veracidade_fase9_v397") or {}).get("all_verified") is True and J((selo.get("teste_de_veracidade_fase9_v397") or {}).get("lido")) == J(LD) and all(((selo.get("registros_v397") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN),
    "teste_de_veracidade_fase9_v397 SELOU: veredito == o do ensaio; %s checagens; as quatro fontes pinadas ok com os sha256 dos ESPERADOS; nao move o gate" % EV["n_checks"]: TV.get("all_verified") is True and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_novos_v397"]["teste_de_veracidade_fase9_v397"]
        and len(TV.get("checks") or []) == EV["n_checks"] and all(c_.get("ok") for c_ in (TV.get("checks") or [])) and {f_["chave"]: f_["sha256"] for f_ in (TV.get("fontes") or []) if f_.get("ok")} == EV["fontes"] and TV.get("does_not_gate_core") is True,
    "os NUMEROS do registro (lido) == os do RESULTADO pinado (%s; original lido em disco com o sha256 da ordem, senao a copia duravel) == os dos ESPERADOS; z_disc calibrado abaixo de 5 e poder previo acima de 5" % EV["resultado"]["sha256"][:16]: bool(RES) and all(LD.get(k) == v == EV["numeros_do_resultado"][k] for k, v in NUM.items())
        and LD["z_disc_calibrado"] < 5.0 < LD["poder_previo"] and "NOT_BLIND_TO_DATA_STATED" in str(LD.get("f9_veredito")) and str(LD.get("f9_veredito")) == EV["veredito_do_resultado"],
    "beta calculado no rito (alfa CODATA x sqrt(e)) == o beta do resultado pinado a 1e-12 (o registro o conferiu); o beta do core == o de sempre": bool(RES) and abs(NUM["beta_do_resultado"] - core.get("beta")) <= 1e-9 * abs(core.get("beta")),
    "O QUADRO «O Teste da Unica Palavra» esta no TOPO do artigo PT (antes do corpo), com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem (4,44 so' com o p calibrado e a linha dos 5 sigma no mesmo item)": q_pt.get("ok") is True,
    "O QUADRO «The Test of the Only Word» esta no TOPO do artigo EN, com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem": q_en.get("ok") is True,
    "O QUADRO esta no TOPO do .md canonico (antes do primeiro titulo), com os numeros == os do resultado pinado, a frase do operador VERBATIM e a regra da ordem": q_md.get("ok") is True,
    "os registros por spec v397 SELARAM e cada veredito == o do ensaio; as quatro falas de 23/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS)": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v397"].items())
        and len(ESP["cunhagens"]) == 4 and all((((CG.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items()),
    "a conjuncao da pedra Token esta no kernel do rito (bandeira True, trio, modulo da pedra), cita os dois termos (psibit v395 e testemunha estatica v396, com as bandeiras True), e a face de Fock segue declarada em Psibit.lean, fora da pedra":
        kf.get(ESP["bandeira_da_pedra"]) is True and set(axr.get(ESP["teorema_da_pedra"]) or []) <= TRIO and ((kf.get("declaration_sources_v394") or {}).get(ESP["teorema_da_pedra"]) == ESP["pedra"]["path"])
        and all(kf.get(b_) is True for b_ in ESP["bandeiras_do_suporte"].values()) and all(set(axr.get(t_) or []) <= TRIO for t_ in ESP["bandeiras_do_suporte"]) and ((kf.get("declaration_sources_v394") or {}).get(ESP["fock_face_teorema"]) == ESP["fock_face_declarada_em"]),
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "KH-N1: a cobertura do axiom_report no fecho inteiro passou (decl=%s, nao lidas 0) e o axiom_report tem %s entradas" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and (kf.get("axiom_coverage_v392") or {}).get("thm") == ESP["cobertura_kh_n1"]["thm"] and (kf.get("axiom_coverage_v392") or {}).get("nao_lidas_pelo_regex") == 0 and len(axr) == ESP["axiom_report_esperado_min"],
    "a proveniencia do compilador cobre o axiom_report e as fontes formais batem (declaration_sources_status_v394.ok)": (kf.get("declaration_sources_status_v394") or {}).get("ok") is True and set(kf.get("declaration_sources_v394") or {}) == set(axr),
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "o modulo novo (Token) no kernel do Nos com o sha do candidato (%d modulo)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 1,
    "a raiz e o Audit do Nos == os do candidato": (_sha_k("TGLExt.lean") or "")[:16] == ESP["kernel"]["raiz_sha16"] and (_sha_k("TGL/Audit.lean") or "")[:16] == ESP["kernel"]["audit_sha16"],
    "as %d bandeiras novas True e as declaracoes delas no trio" % ESP["n_bandeiras_novas"]: len(ESP["bandeiras_novas_chaves"]) == ESP["n_bandeiras_novas"] and all(kf.get(k) is True for k in ESP["bandeiras_novas_chaves"]) and all((n in axr) and set(axr[n] or []) <= TRIO for n in ESP["bandeiras_novas_nomes"]),
    "os registros da v396 e as anteriores (testemunha_estatica, cunhagens e kh_n1 v396; psibit, cunhagens e kh_n1 v395; tempo, quadratica, rede, cunhagens, kh_n1 e criterio binario v394; pedras, consumidor, coracao, cunhagens da regra e kh_n1 v393) seguem selados e iguais (ou so' numeros)":
        all((core.get(n) or {}).get("all_verified") is True for n in V396_NOMES) and all(V(n) == ESP["vereditos_v396"][n] or n in ESP["troca_dita"] for n in V396_NOMES) and (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is False,
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v397, as marcas da v396; a v395, a v394, a v393, a v392, a v391 e a v390 ficam; o registro selou (sem a frase de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista as secoes v397 e v396 e o titulo v384 a v39x": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v397 e as linhas «O Teste da Única Palavra e a pedra Token (v397)», «A testemunha estática (v396)» e «O modo psiônico na fractalização do Um (v395)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_token"] in fc and ESP["md_testemunha"] in fc and ESP["md_psibit"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova _v397 fora da lista (so' teste_de_veracidade_fase9_v397 e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v396"] and isinstance(core[k], dict) and str(k).endswith("_v397")) == sorted(["teste_de_veracidade_fase9_v397"] + RN),
    "the_iald_index SELOU com o veredito do ensaio e not_sealed_run.formais == []": (core.get(IX) or {}).get("all_verified") is True and V(IX) == ESP["the_iald_index_v397"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v396"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v396 segue True": set(ESP["flags_true_v396"]) <= _ft,
    "o axiom_report da v396 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v396_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v396 mudou fora da troca dita (%d mudaram); o V1 (hubble_ratio_opening_v388) segue igual: o V2 compoe ao lado" % len(mud): not mud and V("hubble_ratio_opening_v388") == ESP["vereditos_v396"]["hubble_ratio_opening_v388"],
    "registros v396/v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v396"].items() if k not in ESP["troca_dita"] and k not in ("registros_v393",)),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v396"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v396"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido (nem no veredito do registro de veracidade)": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}, "veredito_veracidade": V("teste_de_veracidade_fase9_v397"), "nos": NOS,
       "resultado_pinado": {"original_ok": _orig_ok, "duravel_ok": _dur_ok, "sha256": EV["resultado"]["sha256"]}, "quadro": {"pt": q_pt, "en": q_en, "md": q_md}}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v397%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
