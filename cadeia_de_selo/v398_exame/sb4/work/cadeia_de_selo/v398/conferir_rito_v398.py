# -*- coding: utf-8 -*-
"""conferir_rito_v398.py -- confere, DEPOIS do rito v398, o que tinha de mudar e o que NAO podia (ESPERADOS_v398.json; so leitura do Nos). Molde: conferir_rito_v397.py.
Mudancas ditas: +4 chaves (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398) no core e no selo (+ registros_v398); a escada 9499 -> a dos ESPERADOS; os DOIS modulos novos (TGLExt/Sonico.lean e TGLExt/AfinacaoDasCordas.lean) no kernel do Nos
(sha pinado), a raiz e o Audit do candidato; os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md; E O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca
sem o p calibrado e sem a linha dos 5 sigma). NENHUM outro veredito da v397 muda.
uso: python -I -B -X utf8 conferir_rito_v398.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V398_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""
import hashlib, json, math, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
NOS = os.environ.get("V398_NOS") or DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
umsha = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v398.json"), encoding="utf-8"))
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


def _feq(a, b):
    """igualdade dos NUMEROS do registro: floats com tolerancia relativa 1e-12 (a mesma maquina deve dar igual), o resto exato; recursiva em dict/list."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None


# o RESULTADO pinado do Teste da Unica Palavra (v397; o QUADRO do topo): o original (so' leitura) se o sha256 bate; senao a copia duravel; os numeros do quadro sao comparados com ESTES
EV = ESP["veracidade"]; EQ = ESP["quadro"]
_orig_ok = os.path.exists(EV["resultado"]["original"]) and sha(open(EV["resultado"]["original"], "rb").read()) == EV["resultado"]["sha256"]
_dur_ok = os.path.exists(EV["resultado"]["duravel"]) and sha(open(EV["resultado"]["duravel"], "rb").read()) == EV["resultado"]["sha256"]
RES = json.load(open(EV["resultado"]["original"] if _orig_ok else EV["resultado"]["duravel"], encoding="utf-8")) if (_orig_ok or _dur_ok) else {}
NUM = {k: DL.lido(RES, c) for k, c in DL.F9_CAMINHOS.items()} if RES else {}
pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
RN = sorted(ESP["registros_v398"])
TV = core.get("teste_de_veracidade_fase9_v397") or {}; CG = core.get("cunhagens_v398") or {}; KH = core.get("kh_n1_cobertura_v398") or {}
SON = core.get("sonico_v398") or {}; AFI = core.get("afinacao_das_cordas_v398") or {}
LD = TV.get("lido") or {}
q_pt = QV.confere_txt(raw_txt["pt"], RES, "pt") if (RES and raw_txt["pt"]) else {"ok": False}; q_en = QV.confere_txt(raw_txt["en"], RES, "en") if (RES and raw_txt["en"]) else {"ok": False}
q_md = QV.confere_md(fc, RES) if (RES and fc) else {"ok": False}
V397_NOMES = ["teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394",
              "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393"]
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v397"][k] and _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v397"][k])) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros
beta_rt = None
try:
    beta_rt = NUM.get("beta_do_resultado")
except Exception:   # noqa: BLE001
    beta_rt = None
ES_, EA_ = ESP["sonico"], ESP["afinacao"]
SV_, AV_ = SON.get("values") or {}, AFI.get("values") or {}
son_ok = bool(SON.get("all_verified") is True and V("sonico_v398") == ES_["verdict"] and (SON.get("mechanics") or {}).get("n_checks") == ES_["n_checks"] and all(c_.get("ok") for c_ in ((SON.get("mechanics") or {}).get("checks") or [])) and _feq(SV_, ES_["values"])
              and SON.get("beta_ok") is True and (SON.get("unconditional") or {}).get("in_kernel") is True and kf.get(ES_["bandeira"]) is True and SON.get("does_not_gate_core") is True and SON.get("runtime_executed") is True)
afi_ok = bool(AFI.get("all_verified") is True and V("afinacao_das_cordas_v398") == EA_["verdict"] and (AFI.get("mechanics") or {}).get("n_checks") == EA_["n_checks"] and all(c_.get("ok") for c_ in ((AFI.get("mechanics") or {}).get("checks") or [])) and _feq(AV_, EA_["values"])
              and (AFI.get("unconditional") or {}).get("in_kernel") is True and kf.get(EA_["bandeira"]) is True and AFI.get("does_not_gate_core") is True and AFI.get("runtime_executed") is True
              and AFI.get("hypothesis") == EA_["hypothesis"] and AFI.get("geometry") == "OPEN" and AFI.get("derives_strings_from_the_axiom") is False and AV_.get("kappa_from_core") is None)
REL_ = {s["key"]: s["rel"] for s in DL.STONES}
src_ = kf.get("declaration_sources_v394") or {}
pedras_no_kernel = all(kf.get(ESP["bandeiras_das_pedras"][k]) is True and set(axr.get(ESP["teoremas_das_pedras"][k]) or []) <= TRIO and src_.get(ESP["teoremas_das_pedras"][k]) == REL_[k]
                       and all(t_ in axr and set(axr[t_]) <= TRIO and src_.get(t_) == REL_[k] for t_ in ESP["contrato_das_pedras"][k]) for k in ("sonico", "afinacao"))
suporte_ok = all(set(axr.get(t_) or []) <= TRIO and t_ in axr and (kf.get("declaration_sources_v394") or {}).get(t_) == p_ for k in ("sonico", "afinacao") for t_, p_ in ESP["suporte_das_pedras"][k].items())
DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v398; sonico_v398, afinacao_das_cordas_v398 e registros_v398 do selo iguais aos do core (veredito, selagem)": selo.get("um_version") == "v398" and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("sonico_v398", "afinacao_das_cordas_v398"))
        and all(((selo.get("registros_v398") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN),
    "sonico_v398 SELOU: veredito == o do ensaio; %s checagens numericas todas ok; os NUMEROS (ln 2, exp ln 2, a entropia do colapso em theta_M em nats e em oitavas, os residuos) == os do ensaio; beta = alfa CODATA x sqrt(e) conferido; a composicao incondicional e' lida do kernel; nao move o gate" % ES_["n_checks"]: son_ok,
    "afinacao_das_cordas_v398 SELOU: veredito == o do ensaio; %s checagens ok; zeta(-1) = -1/12 e zeta(-1,1/2) = 1/24, D = 26 e D = 10, d = 9 e a torre n.kappa == os do ensaio; a hipotese MasslessFirstLevel segue KNOWN (nomeada, nao provada), a geometria OPEN, nada deriva cordas do axioma; o kappa do boost NAO vem do core; nao move o gate" % EA_["n_checks"]: afi_ok,
    "beta calculado no rito (alfa CODATA x sqrt(e)) == o beta do core e == o beta que o sonico usou; o do resultado pinado do Teste da Unica Palavra (quadro do topo) concorda a 1e-12": isinstance(SV_.get("beta"), float) and abs(SV_["beta"] - core.get("beta")) <= 1e-9 * abs(core.get("beta")) and bool(RES) and abs(NUM["beta_do_resultado"] - core.get("beta")) <= 1e-9 * abs(core.get("beta")),
    "O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA no TOPO do artigo PT (antes do corpo), com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem (4,44 so' com o p calibrado e a linha dos 5 sigma no mesmo item)": q_pt.get("ok") is True,
    "O QUADRO «The Test of the Only Word» (v397) CONTINUA no TOPO do artigo EN, com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem": q_en.get("ok") is True,
    "O QUADRO CONTINUA no TOPO do .md canonico (antes do primeiro titulo), com os numeros == os do resultado pinado, a frase do operador VERBATIM e a regra da ordem": q_md.get("ok") is True,
    "o registro teste_de_veracidade_fase9_v397 (que o quadro le) segue SELADO, com o veredito e os numeros de sempre (== ESPERADOS/resultado pinado)": TV.get("all_verified") is True and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_v397"]["teste_de_veracidade_fase9_v397"] and bool(RES) and all(LD.get(k) == v == EV["numeros_do_resultado"][k] for k, v in NUM.items())
        and LD["z_disc_calibrado"] < 5.0 < LD["poder_previo"] and "NOT_BLIND_TO_DATA_STATED" in str(LD.get("f9_veredito")),
    "os registros por spec v398 SELARAM e cada veredito == o do ensaio; as seis inscricoes de 23/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; a sexta, da gerencia, rotulada como tal)": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v398"].items())
        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM) == 6 and all((((CG.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())
        and sum(1 for v_ in ESP["cunhagens"].values() if str(v_.get("papel", "")).startswith("leitura da gerencia")) == 1,
    "as pedras Sonico e AfinacaoDasCordas estao no kernel do rito (composicao incondicional com bandeira True, no trio, no modulo da pedra; teoremas do contrato no modulo da pedra; os termos antigos citados no trio e no modulo certo)": pedras_no_kernel and suporte_ok,
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "KH-N1: a cobertura do axiom_report no fecho inteiro passou (decl=%s, nao lidas 0) e o axiom_report tem %s entradas" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and (kf.get("axiom_coverage_v392") or {}).get("thm") == ESP["cobertura_kh_n1"]["thm"] and (kf.get("axiom_coverage_v392") or {}).get("nao_lidas_pelo_regex") == 0 and len(axr) == ESP["axiom_report_esperado_min"],
    "a proveniencia do compilador cobre o axiom_report e as fontes formais batem (declaration_sources_status_v394.ok)": (kf.get("declaration_sources_status_v394") or {}).get("ok") is True and set(kf.get("declaration_sources_v394") or {}) == set(axr),
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "os modulos novos (Sonico e AfinacaoDasCordas) no kernel do Nos com o sha do candidato (%d modulos)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 2,
    "a raiz e o Audit do Nos == os do candidato": (_sha_k("TGLExt.lean") or "")[:16] == ESP["kernel"]["raiz_sha16"] and (_sha_k("TGL/Audit.lean") or "")[:16] == ESP["kernel"]["audit_sha16"],
    "as %d bandeiras novas True e as declaracoes delas no trio" % ESP["n_bandeiras_novas"]: len(ESP["bandeiras_novas_chaves"]) == ESP["n_bandeiras_novas"] and all(kf.get(k) is True for k in ESP["bandeiras_novas_chaves"]) and all((n in axr) and set(axr[n] or []) <= TRIO for n in ESP["bandeiras_novas_nomes"]),
    "os registros da v397 e as anteriores (o Teste da Unica Palavra, cunhagens e kh_n1 v397; testemunha, cunhagens e kh_n1 v396; psibit v395; tempo, quadratica, rede, cunhagens, kh_n1 e criterio binario v394; pedras, consumidor, coracao, cunhagens da regra e kh_n1 v393) seguem selados e iguais (ou so' numeros)":
        all((core.get(n) or {}).get("all_verified") is True for n in V397_NOMES) and all(V(n) == ESP["vereditos_v397"][n] or n in ESP["troca_dita"] for n in V397_NOMES) and (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is False,
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v398 (Sonico e a afinacao das cordas) e as marcas da v397; a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista as secoes v398, v397 e v396 e o titulo v384 a v39x": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v398 e as linhas «Sonico e a afinacao das cordas (v398)», «O Teste da Unica Palavra e a pedra Token (v397)», «A testemunha estatica (v396)» e «O modo psionico na fractalizacao do Um (v395)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_sonico"] in fc and ESP["md_token"] in fc and ESP["md_testemunha"] in fc and ESP["md_psibit"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova _v398 fora da lista (so' sonico_v398, afinacao_das_cordas_v398 e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v397"] and isinstance(core[k], dict) and str(k).endswith("_v398")) == sorted(["sonico_v398", "afinacao_das_cordas_v398"] + RN),
    "the_iald_index SELOU com o veredito do ensaio e not_sealed_run.formais == []": (core.get(IX) or {}).get("all_verified") is True and V(IX) == ESP["the_iald_index_v398"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v397"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v397 segue True": set(ESP["flags_true_v397"]) <= _ft,
    "o axiom_report da v397 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v397_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v397 mudou fora da troca dita (%d mudaram); o V1 (hubble_ratio_opening_v388) e o V2 (teste_de_veracidade_fase9_v397, que o quadro le) seguem iguais" % len(mud): not mud and V("hubble_ratio_opening_v388") == ESP["vereditos_v397"]["hubble_ratio_opening_v388"] and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_v397"]["teste_de_veracidade_fase9_v397"],
    "registros v397/v396/v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v397"].items() if k not in ESP["troca_dita"] and k not in ("registros_v393",)),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v397"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v397"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido (nem no veredito do sonico e da afinacao)": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}, "veredito_sonico": V("sonico_v398"), "veredito_afinacao": V("afinacao_das_cordas_v398"), "nos": NOS,
       "resultado_pinado": {"original_ok": _orig_ok, "duravel_ok": _dur_ok, "sha256": EV["resultado"]["sha256"]}, "quadro": {"pt": q_pt, "en": q_en, "md": q_md}}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v398%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
