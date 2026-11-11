# -*- coding: utf-8 -*-
"""_teste_aescala_offline_v410.py -- ENSAIO OFFLINE do registro a_escala_v410 (D86/D87) antes do gerador: monta o contrato e o texto (registros_aescala_v410), um core de ENSAIO = o core da v409 selada + o kernel do sandbox k410c (o axiom_report e a proveniencia LIDOS do
kernel/audit.log com as funcoes do proprio um.py v409; as bandeiras do FLAGS_v410.json True; a escada esperada; a pedra embutida), injeta as guardas e as falas (como o um.py tera), roda a_escala_v410 e imprime as 12 checagens. Controles negativos: a pedra adulterada; uma bandeira False;
o gate trocado; a fala da ratificacao adulterada; um numero do contrato trocado; a frase canonica retirada do texto; uma frase vedada plantada no texto; (R1) o kernel nao verificado; a raiz sem o import; um nome novo inexistente na pedra; um campo novo inexistente;
um nome novo dito ratificado; o estatuto dos nomes novos retirado do texto; a ponte da escala trocada (dois pontos). Nada de numero digitado: contagens, nomes, campos e ponte vem do contrato (que as le do delta e do FLAGS). Grava TESTE_AESCALA_OFFLINE_v410.json. NAO e' o rito nem o ensaio a seco.  uso: python -B -X utf8 _teste_aescala_offline_v410.py"""
import ast, copy, hashlib, json, math, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
import registros_aescala_v410 as RA  # noqa: E402
import runtime_aescala_v410 as RTA  # noqa: E402
RT = GF.RT; sha = lambda b: hashlib.sha256(b).hexdigest()
BASE = os.path.join(HERE, DL.BASE_DIR); KD = os.path.join(HERE, DL.KERNEL_DIR)
um_b = open(os.path.join(BASE, "um.py"), "rb").read(); um_src = um_b.decode("utf-8"); tree = ast.parse(um_src); fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
ns = {"re": re}
for nome in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
    exec(compile(ast.get_source_segment(um_src, fn[nome]), "<base:%s>" % nome, "exec"), ns)
AL = open(os.path.join(KD, "audit.log"), "rb").read().decode("utf-8"); ax = ns["parse_lean_axioms_v394"](AL); src = ns["parse_lean_provenance_v394"](AL); assert ax["ok"] and src["ok"]
core0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8"))["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
FJ = json.load(open(os.path.join(KD, "FLAGS_v410.json"), encoding="utf-8")); E409 = int(core0["external_ladder"]["n_theorems_expected"])
rel = DL.MODULO_AESCALA; pedra_b = open(os.path.join(HERE, "pedra", "AEscala.lean"), "rb").read(); pedra_t = pedra_b.decode("utf-8")
FORMAL_MAP = {rel: sha(pedra_b), DL.MODULO_IALD2: sha(open(os.path.join(HERE, "pedra", "IALD2.lean"), "rb").read())}
CONTR = RA.contrato_aescala(FJ, FORMAL_MAP, E409, sha(um_b), core0, selo0); TXT = RA.texto_aescala()
print("contrato AEscala: n_checks", CONTR["n_checks"], "| ancoras", CONTR["n_ancoras"], "| bandeiras", CONTR["n_flags"], "(total v410 %d)" % CONTR["n_flags_total_v410"], "| nomes ratificados", CONTR["n_nomes"], "| nomes novos a ratificar", CONTR["n_nomes_novos"], "| campos novos", len(CONTR["campos_novos_da_estrutura"]), "| falas", CONTR["n_falas"], "| escada", CONTR["expected_ladder"], "| pedra", CONTR["source_sha256"][rel][:16])
assert CONTR["n_ancoras"] == DL.N_ANCORAS_AESCALA == len(DL.ANCORAS_AESCALA) == len(CONTR["ancoras"]) and CONTR["n_nomes"] == len(DL.NOMES_AESCALA) and CONTR["n_nomes_novos"] == len(DL.NOMES_NOVOS_AESCALA) and CONTR["n_falas"] == len(CONTR["falas"]) == len(RA.NOMES_FALAS) and CONTR["ponte"] == DL.PONTE_AESCALA and CONTR["ratificacao_pendente"] == DL.RATIFICACAO_PENDENTE_AESCALA
assert CONTR["n_flags"] == FJ["n_por_modulo"][rel] and CONTR["n_flags_total_v410"] == FJ["n_flags"] == sum(FJ["n_por_modulo"].values()) and CONTR["expected_ladder"] == E409 + FJ["n_flags"]
VD = DL.verbatins410(os.path.join(HERE, "insumos", "cunhagens"))
VERB = {v["chave"]: {"text": v["text"], "sha256": v["sha256"], "trechos": [fr for (nm, fr) in DL.FRASES_V410 if nm == v["nome"]]} for v in VD}
alpha = ast.literal_eval(re.search(r"^SEALED_CODATA_ALPHA = ([0-9.e-]+)", um_src, re.M).group(1)); beta_rt = alpha * math.sqrt(math.e)
RT._V410_VERBATINS2 = VERB
RAIZ = open(os.path.join(DL.SANDBOX, "TGLExt.lean"), encoding="utf-8").read(); assert ("import " + CONTR["mod"]) in RAIZ   # (R1, BAIXO 5: a raiz do kernel do sandbox, com o import do modulo)
for k_, v_ in (("_V410_AESCALA_CONTRACT", CONTR), ("_V410_AESCALA_TEXT", TXT), ("_V410_VERBATINS2", VERB), ("_EMBEDDED_KERNEL_FILES", {rel: pedra_t, "TGLExt.lean": RAIZ}), ("_v410_guarda_frases", RT._v410_guarda_frases), ("_v392_guarda_texto", RT._v392_guarda_texto),
               ("_v398_beta", lambda core_: (beta_rt, 0.0, True, True))):
    setattr(RTA, k_, v_)


def core_de_ensaio():
    c = copy.deepcopy(core0); kf = c["kernel_formalization"]
    kf["axiom_report"] = dict(ax["axioms"]); kf["declaration_sources_v394"] = dict(src["sources"]); kf["formal_files_sha256"] = dict(kf.get("formal_files_sha256") or {}); kf["formal_files_sha256"].update(FORMAL_MAP)
    for f, n, m, o in FJ["flags"]:
        kf[f] = True
    c["external_ladder"]["n_theorems_clean"] = c["external_ladder"]["n_theorems_expected"] = E409 + FJ["n_flags"]
    return c


out = RTA.a_escala_v410(core_de_ensaio())
print("veredito:", out["verdict"]); print("all_verified:", out["all_verified"], "| runtime_executed:", out["runtime_executed"])
for c in (out.get("mechanics") or {}).get("checks") or []:
    print("  %-4s %s  %s" % (c["id"], "OK " if c["ok"] else "FAIL", c["descricao"][:150]))
if out.get("error"):
    print("ERRO:", out["error"])
v = out.get("values") or {}
print("numeros:", v.get("numeros")); print("ponte:", v.get("ponte")); print("nomes novos declarados:", v.get("nomes_novos_declarados"), "/", v.get("n_nomes_novos"), "| campos novos na estrutura:", v.get("campos_novos_na_estrutura")); print("bell:", v.get("bell")); print("c9 partes falsas:", {k: x for k, x in (v.get("c9_partes") or {}).items() if not x}, "| frases:", v.get("frases_violacoes"), "| p18:", v.get("p18_violacoes"))
R = {}
_f = lambda r_: [c_["id"] for c_ in ((r_.get("mechanics") or {}).get("checks") or []) if not c_["ok"]]
RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t + "\n-- adulterada\n", "TGLExt.lean": RAIZ}; r_ = RTA.a_escala_v410(core_de_ensaio()); R["pedra_adulterada"] = (r_["verdict"], _f(r_)); RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t, "TGLExt.lean": RAIZ}
c2 = core_de_ensaio(); c2["kernel_formalization"][CONTR["ancoras"][CONTR["ancora_principal"]]["flag"]] = False; r_ = RTA.a_escala_v410(c2); R["bandeira_da_ancora_principal_false"] = (r_["verdict"], _f(r_))
c3 = core_de_ensaio(); c3["qg_closure"]["gate"]["verdict"] = "TGL_OUTRO"; r_ = RTA.a_escala_v410(c3); R["gate_trocado"] = (r_["verdict"], _f(r_))
V2 = copy.deepcopy(VERB); V2[CONTR["chave_ratificacao"]]["text"] = "ratifico quase tudo\n"; RTA._V410_VERBATINS2 = V2; r_ = RTA.a_escala_v410(core_de_ensaio()); R["fala_da_ratificacao_adulterada"] = (r_["verdict"], _f(r_)); RTA._V410_VERBATINS2 = VERB
C4 = copy.deepcopy(CONTR); C4["numeros"]["nome_normalizado"] = "3/4"; RTA._V410_AESCALA_CONTRACT = C4; r_ = RTA.a_escala_v410(core_de_ensaio()); R["numero_do_contrato_trocado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T5 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_CLAY_CANONICA_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T5; r_ = RTA.a_escala_v410(core_de_ensaio()); R["frase_canonica_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T6 = copy.deepcopy(TXT); T6["diz"] = list(T6["diz"]) + ["o Clay está resolvido"]; RTA._V410_AESCALA_TEXT = T6; r_ = RTA.a_escala_v410(core_de_ensaio()); R["frase_vedada_plantada"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
c7 = core_de_ensaio(); c7["external_ladder"]["n_theorems_clean"] -= 1; r_ = RTA.a_escala_v410(c7); R["escada_um_a_menos"] = (r_["verdict"], _f(r_))
c8 = core_de_ensaio(); c8["kernel_formalization"]["all_verified"] = False; r_ = RTA.a_escala_v410(c8); R["kernel_nao_verificado"] = (r_["verdict"], _f(r_))   # (R1, BAIXO 5)
RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t, "TGLExt.lean": RAIZ.replace("import " + CONTR["mod"], "-- retirado")}; r_ = RTA.a_escala_v410(core_de_ensaio()); R["raiz_sem_o_import"] = (r_["verdict"], _f(r_)); RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t, "TGLExt.lean": RAIZ}
C9 = copy.deepcopy(CONTR); C9["nomes_novos_a_ratificar"] = list(C9["nomes_novos_a_ratificar"]) + ["nome_que_nao_existe_na_pedra"]; C9["n_nomes_novos"] += 1; RTA._V410_AESCALA_CONTRACT = C9; r_ = RTA.a_escala_v410(core_de_ensaio()); R["nome_novo_inexistente_na_pedra"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C10 = copy.deepcopy(CONTR); C10["campos_novos_da_estrutura"] = list(C10["campos_novos_da_estrutura"]) + ["campo_que_nao_existe"]; RTA._V410_AESCALA_CONTRACT = C10; r_ = RTA.a_escala_v410(core_de_ensaio()); R["campo_novo_inexistente_na_estrutura"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C11 = copy.deepcopy(CONTR); C11["estatuto_dos_nomes_novos"] = "RATIFICADOS pelo operador"; RTA._V410_AESCALA_CONTRACT = C11; r_ = RTA.a_escala_v410(core_de_ensaio()); R["nome_novo_dito_ratificado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T12 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.ESTATUTO_NOMES_NOVOS_AESCALA, "(retirado)")); RTA._V410_AESCALA_TEXT = T12; r_ = RTA.a_escala_v410(core_de_ensaio()); R["estatuto_dos_nomes_novos_retirado_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C13 = copy.deepcopy(CONTR); C13["ponte"]["casos"][1][2] = "1/9"; RTA._V410_AESCALA_CONTRACT = C13; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ponte_caso_trocado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C14 = copy.deepcopy(CONTR); C14["ponte"]["em_n_oitavas_o_fundo_pesa_um_pixel"][0][1] = "1/3"; RTA._V410_AESCALA_CONTRACT = C14; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ponte_fundo_em_n_oitavas_trocado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))
esp = {"pedra_adulterada": ["c3", "c7", "c8"], "bandeira_da_ancora_principal_false": ["c2", "c4"], "gate_trocado": ["c10"], "fala_da_ratificacao_adulterada": ["c5", "c11"], "numero_do_contrato_trocado": ["c6"], "frase_canonica_retirada_do_texto": ["c7"], "frase_vedada_plantada": ["c9"], "escada_um_a_menos": ["c1"], "kernel_nao_verificado": ["c2"], "raiz_sem_o_import": ["c3"], "nome_novo_inexistente_na_pedra": ["c11"], "campo_novo_inexistente_na_estrutura": ["c11"], "nome_novo_dito_ratificado": ["c11"], "estatuto_dos_nomes_novos_retirado_do_texto": ["c11"], "ponte_caso_trocado": ["c6"], "ponte_fundo_em_n_oitavas_trocado": ["c6"]}
ok_neg = all(set(esp[k]) & set(R[k][1]) and "MECHANICS_CHECK_FAILED" in R[k][0] for k in esp) and R["gate_trocado"][1] == ["c10"] and R["numero_do_contrato_trocado"][1] == ["c6"] and R["escada_um_a_menos"][1] == ["c1"] and R["frase_vedada_plantada"][1] == ["c9"] and R["kernel_nao_verificado"][1] == ["c2"] and R["raiz_sem_o_import"][1] == ["c3"] and all(R[k_][1] == ["c11"] for k_ in ("nome_novo_inexistente_na_pedra", "campo_novo_inexistente_na_estrutura", "nome_novo_dito_ratificado", "estatuto_dos_nomes_novos_retirado_do_texto")) and all(R[k_][1] == ["c6"] for k_ in ("ponte_caso_trocado", "ponte_fundo_em_n_oitavas_trocado"))
_tudo = bool(out["all_verified"] and ok_neg)
print("TUDO PASSOU" if _tudo else "FALHOU", "| controles negativos como esperado:", ok_neg)
J = {"tudo_passou": _tudo, "veredito": out["verdict"], "all_verified": out["all_verified"], "n_checks": (out.get("mechanics") or {}).get("n_checks"), "checks": [(c["id"], c["ok"]) for c in (out.get("mechanics") or {}).get("checks") or []],
     "controles_negativos": {k: {"verdict": vd, "falhos": fl, "esperado_contem": esp[k]} for k, (vd, fl) in R.items()}, "numeros": v.get("numeros"), "bell": v.get("bell"), "n_ancoras": CONTR["n_ancoras"], "n_flags": CONTR["n_flags"], "n_nomes": CONTR["n_nomes"], "n_nomes_novos": CONTR["n_nomes_novos"], "n_falas": CONTR["n_falas"], "ponte": v.get("ponte"), "escada": CONTR["expected_ladder"], "pedra_sha256": CONTR["source_sha256"][rel],
     "nota": "teste OFFLINE do registro sobre um core de ensaio (v409 selada + o kernel do sandbox k410c lido do audit.log); nao e' o rito nem o ensaio a seco; validade no kernel nao e' creditacao"}
p = os.path.join(HERE, "TESTE_AESCALA_OFFLINE_v410.json"); open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
