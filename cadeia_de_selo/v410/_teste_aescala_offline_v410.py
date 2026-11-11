# -*- coding: utf-8 -*-
"""_teste_aescala_offline_v410.py -- ENSAIO OFFLINE do registro a_escala_v410 (D86/D87) antes do gerador: monta o contrato e o texto (registros_aescala_v410), um core de ENSAIO = o core da v409 selada + o kernel do sandbox k410c (o axiom_report e a proveniencia LIDOS do
kernel/audit.log com as funcoes do proprio um.py v409; as bandeiras do FLAGS_v410.json True; a escada esperada; a pedra embutida), injeta as guardas e as falas (como o um.py tera), roda a_escala_v410 e imprime as 13 checagens. Controles negativos: a pedra adulterada; uma bandeira False;
o gate trocado; a fala da ratificacao adulterada; um numero do contrato trocado; a frase canonica retirada do texto; uma frase vedada plantada no texto; (R1) o kernel nao verificado; a raiz sem o import; um nome novo inexistente na pedra; um campo novo inexistente;
um nome novo dito ratificado; o estatuto dos nomes novos retirado do texto; a ponte da escala trocada (dois pontos); (R5, D100 e D101) a clausula do Tetelestai em 1 - beta (a clausula do limite retirada de uma folha que a anuncia; a hipotese s >= 0 retirada; a citacao do dispositivo sem [PILOTO][SIM] ou com numero de desempenho; o controle negativo da c13 invertido; o adversario com duas solucoes; o contraexemplo com b <= 1/2) e a ratificacao de 10/11 (um pendente entre os ratificados; ratificacao_pendente esvaziada; o sha256 da fala 28 trocado; a fala adulterada; o estatuto antigo restaurado ou plantado; a frase da ratificacao retirada; um ratificado retirado); (R2, D99) a clausula do limite do teorema do Tetelestai retirada (de todo o texto, de um so' campo, a EN); (B1) uma ancora nova tirada do contrato; (B3) a frase dos seis nomes retirada. Nada de numero digitado: contagens, nomes, campos e ponte vem do contrato (que as le do delta e do FLAGS). Grava TESTE_AESCALA_OFFLINE_v410.json. NAO e' o rito nem o ensaio a seco.  uso: python -B -X utf8 _teste_aescala_offline_v410.py"""
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
print("contrato AEscala: n_checks", CONTR["n_checks"], "| ancoras", CONTR["n_ancoras"], "| bandeiras", CONTR["n_flags"], "(total v410 %d)" % CONTR["n_flags_total_v410"], "| nomes ratificados", CONTR["n_nomes"], "| nomes novos da pedra", CONTR["n_nomes_novos"], "| campos novos", len(CONTR["campos_novos_da_estrutura"]), "| falas", CONTR["n_falas"], "| escada", CONTR["expected_ladder"], "| pedra", CONTR["source_sha256"][rel][:16])
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
C9 = copy.deepcopy(CONTR); C9["nomes_novos_da_pedra"] = list(C9["nomes_novos_da_pedra"]) + ["nome_que_nao_existe_na_pedra"]; C9["n_nomes_novos"] += 1; RTA._V410_AESCALA_CONTRACT = C9; r_ = RTA.a_escala_v410(core_de_ensaio()); R["nome_novo_inexistente_na_pedra"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C10 = copy.deepcopy(CONTR); C10["campos_novos_da_estrutura"] = list(C10["campos_novos_da_estrutura"]) + ["campo_que_nao_existe"]; RTA._V410_AESCALA_CONTRACT = C10; r_ = RTA.a_escala_v410(core_de_ensaio()); R["campo_novo_inexistente_na_estrutura"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C11 = copy.deepcopy(CONTR); C11["estatuto_dos_nomes_ratificados_d101"] = "RATIFICADOS pelo operador"; RTA._V410_AESCALA_CONTRACT = C11; r_ = RTA.a_escala_v410(core_de_ensaio()); R["nome_novo_dito_ratificado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T12 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.ESTATUTO_NOMES_NOVOS_AESCALA, "(retirado)")); RTA._V410_AESCALA_TEXT = T12; r_ = RTA.a_escala_v410(core_de_ensaio()); R["estatuto_dos_nomes_ratificados_d101_retirado_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C13 = copy.deepcopy(CONTR); C13["ponte"]["casos"][1][2] = "1/9"; RTA._V410_AESCALA_CONTRACT = C13; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ponte_caso_trocado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C14 = copy.deepcopy(CONTR); C14["ponte"]["em_n_oitavas_o_fundo_pesa_um_pixel"][0][1] = "1/3"; RTA._V410_AESCALA_CONTRACT = C14; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ponte_fundo_em_n_oitavas_trocado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C15 = copy.deepcopy(CONTR); C15["ciclo"]["custo_sem_solucao"][0] = 0; RTA._V410_AESCALA_CONTRACT = C15; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ciclo_instancia_sem_solucao_com_solucao"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR   # (R4, D94)
C16 = copy.deepcopy(CONTR); C16["ciclo"]["epsilon"] = "5"; RTA._V410_AESCALA_CONTRACT = C16; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ciclo_epsilon_fora_do_intervalo"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T17 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_TEMPO_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T17; r_ = RTA.a_escala_v410(core_de_ensaio()); R["forma_do_tempo_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C18 = copy.deepcopy(CONTR); C18["teoremas_r4"] = list(C18["teoremas_r4"]) + ["teorema_que_nao_existe_na_pedra"]; RTA._V410_AESCALA_CONTRACT = C18; r_ = RTA.a_escala_v410(core_de_ensaio()); R["teorema_da_r4_fora_das_ancoras"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
# (R2, D99; ADENDO 4) a clausula do limite do teorema do Tetelestai: retirada de todo o texto; retirada so' de UM campo que anuncia o teorema (diz); a EN retirada; (B1) uma ancora nova tirada do contrato; (B3) a frase dos seis nomes retirada do texto
T19 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.CLAUSULA_Z_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T19; r_ = RTA.a_escala_v410(core_de_ensaio()); R["clausula_do_limite_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T20 = copy.deepcopy(TXT); T20["diz"] = [x_.replace(DL.CLAUSULA_Z_PT, "(retirada)") for x_ in T20["diz"]]; assert T20["diz"] != TXT["diz"] and any(DL.CLAUSULA_Z_PT in x_ for x_ in T20["escopo"].split("\n") + T20["limites"]), "o controle de um campo so' faz sentido se a clausula esta em mais de um campo"
RTA._V410_AESCALA_TEXT = T20; r_ = RTA.a_escala_v410(core_de_ensaio()); R["clausula_do_limite_retirada_de_um_campo"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T21 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.CLAUSULA_Z_EN, "(removed)")); RTA._V410_AESCALA_TEXT = T21; r_ = RTA.a_escala_v410(core_de_ensaio()); R["clausula_do_limite_em_ingles_retirada"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C22 = copy.deepcopy(CONTR); C22["ancoras_novas"] = list(C22["ancoras_novas"])[1:]; RTA._V410_AESCALA_CONTRACT = C22; r_ = RTA.a_escala_v410(core_de_ensaio()); R["ancora_nova_tirada_do_contrato"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T23 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_SEIS_NOMES_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T23; r_ = RTA.a_escala_v410(core_de_ensaio()); R["seis_nomes_retirados_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
# (R5, D100 e D101) a clausula do Tetelestai em 1 - beta e a ratificacao de 10/11: cada controle tem de reprovar so' a checagem esperada
_ant_pt = "anuncio_da_clausula_do_tetelestai_pt"
T24 = copy.deepcopy(TXT); _lf = T24["extras"][_ant_pt]; assert DL.CLAUSULA_Z_PT in _lf and DL.FRASE_TETELESTAI_PT in _lf; T24["extras"][_ant_pt] = _lf.replace(DL.CLAUSULA_Z_PT, "(retirada)")
RTA._V410_AESCALA_TEXT = T24; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_clausula_do_limite_retirada_de_uma_folha_que_anuncia_os_teoremas_novos"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T25 = copy.deepcopy(TXT); T25["extras"][_ant_pt] = T25["extras"][_ant_pt].replace(DL.FRASE_TETELESTAI_PT, DL.FRASE_TETELESTAI_PT.replace("s ≥ 0", "s")); assert T25["extras"][_ant_pt] != TXT["extras"][_ant_pt]
RTA._V410_AESCALA_TEXT = T25; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_hipotese_s_nao_negativo_retirada_de_uma_folha"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C26 = copy.deepcopy(CONTR); C26["frase_tetelestai_pt"] = DL.FRASE_TETELESTAI_PT.replace("s ≥ 0", "s"); assert C26["frase_tetelestai_pt"] != CONTR["frase_tetelestai_pt"]
RTA._V410_AESCALA_CONTRACT = C26; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_hipotese_s_nao_negativo_retirada_da_frase_do_contrato"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T27 = json.loads(json.dumps(TXT, ensure_ascii=False).replace("[PILOTO][SIM]", "(retirado)")); RTA._V410_AESCALA_TEXT = T27; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_citacao_do_dispositivo_sem_piloto_sim"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T28 = copy.deepcopy(TXT); T28["nao_diz"] = list(T28["nao_diz"]) + ["o ACOM Mirror, que é [PILOTO][SIM] e do qual nada ali valida física, rodou 22 de 22 testes"]
RTA._V410_AESCALA_TEXT = T28; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_citacao_do_dispositivo_com_numero_de_desempenho"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C29 = copy.deepcopy(CONTR); C29["tetelestai"]["oitavas_a_menos_no_controle"] = 0; RTA._V410_AESCALA_CONTRACT = C29; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_controle_negativo_invertido_s_estrela_no_lugar_de_uma_oitava_a_menos"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C30 = copy.deepcopy(CONTR); C30["tetelestai"]["custo_adversario"] = [0, 0] + [1] * (2 ** C30["tetelestai"]["n_bits"] - 2); RTA._V410_AESCALA_CONTRACT = C30; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_adversario_com_duas_solucoes"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C31 = copy.deepcopy(CONTR); C31["tetelestai"]["contraexemplo_s_negativo"]["b"] = "1/10"; RTA._V410_AESCALA_CONTRACT = C31; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_contraexemplo_com_b_no_meio_ou_abaixo"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C32 = copy.deepcopy(CONTR); C32["nomes_ratificados_d101"] = list(C32["nomes_ratificados_d101"]) + [C32["nomes_pendentes"][0]]; RTA._V410_AESCALA_CONTRACT = C32; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_um_pendente_entre_os_ratificados"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C33 = copy.deepcopy(CONTR); C33["ratificacao_pendente"] = {}; RTA._V410_AESCALA_CONTRACT = C33; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_ratificacao_pendente_esvaziada"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
C34 = copy.deepcopy(CONTR); C34["ratificacao_d101"]["sha256"] = "0" * 64; RTA._V410_AESCALA_CONTRACT = C34; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_sha256_da_fala_28_trocado_no_pino"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
V35 = copy.deepcopy(VERB); V35[CONTR["chave_ratificacao_d101"]]["text"] = V35[CONTR["chave_ratificacao_d101"]]["text"] + "x"; RTA._V410_VERBATINS2 = V35; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_fala_28_adulterada"] = (r_["verdict"], _f(r_)); RTA._V410_VERBATINS2 = VERB
C36 = copy.deepcopy(CONTR); C36["estatuto_dos_nomes_ratificados_d101"] = "[DECLARADO pela gerencia e pela autoria; a ratificar pelo operador]"; RTA._V410_AESCALA_CONTRACT = C36; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_estatuto_antigo_restaurado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T37 = copy.deepcopy(TXT); T37["diz"] = list(T37["diz"]) + ["os nomes novos seguem [DECLARADO, a ratificar]"]; RTA._V410_AESCALA_TEXT = T37; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_estatuto_antigo_plantado_no_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
T38 = json.loads(json.dumps(TXT, ensure_ascii=False).replace(DL.FRASE_NOMES_RATIFICADOS_D101_PT, "(retirada)")); RTA._V410_AESCALA_TEXT = T38; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_frase_da_ratificacao_d101_retirada_do_texto"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
C39 = copy.deepcopy(CONTR); C39["nomes_ratificados_d101"] = list(C39["nomes_ratificados_d101"])[1:]; RTA._V410_AESCALA_CONTRACT = C39; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_um_ratificado_retirado"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_CONTRACT = CONTR
T40 = copy.deepcopy(TXT); _i40 = [i_ for i_, x_ in enumerate(T40["diz"]) if DL.FRASE_E36_PT in x_]; assert len(_i40) == 1 and DL.CLAUSULA_Z_PT in T40["diz"][_i40[0]]; T40["diz"][_i40[0]] = DL.FRASE_E36_PT   # (revisao do construtor) a E36 sozinha na folha, sem a clausula do limite
RTA._V410_AESCALA_TEXT = T40; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_errata_e36_sem_a_clausula_do_limite_na_folha"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT
for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:60], fl))
esp = {"pedra_adulterada": ["c3", "c7", "c8"], "bandeira_da_ancora_principal_false": ["c2", "c4"], "gate_trocado": ["c10"], "fala_da_ratificacao_adulterada": ["c5", "c11"], "numero_do_contrato_trocado": ["c6"], "frase_canonica_retirada_do_texto": ["c7"], "frase_vedada_plantada": ["c9"], "escada_um_a_menos": ["c1"], "kernel_nao_verificado": ["c2"], "raiz_sem_o_import": ["c3"], "nome_novo_inexistente_na_pedra": ["c11"], "campo_novo_inexistente_na_estrutura": ["c11"], "nome_novo_dito_ratificado": ["c11"], "estatuto_dos_nomes_ratificados_d101_retirado_do_texto": ["c11"], "ponte_caso_trocado": ["c6"], "ponte_fundo_em_n_oitavas_trocado": ["c6"], "ciclo_instancia_sem_solucao_com_solucao": ["c6"], "ciclo_epsilon_fora_do_intervalo": ["c6"], "forma_do_tempo_retirada_do_texto": ["c8"], "teorema_da_r4_fora_das_ancoras": ["c2"], "clausula_do_limite_retirada_do_texto": ["c8"], "clausula_do_limite_retirada_de_um_campo": ["c8"], "clausula_do_limite_em_ingles_retirada": ["c8"], "ancora_nova_tirada_do_contrato": ["c2"], "seis_nomes_retirados_do_texto": ["c11"],
       "r5_clausula_do_limite_retirada_de_uma_folha_que_anuncia_os_teoremas_novos": ["c8"], "r5_hipotese_s_nao_negativo_retirada_de_uma_folha": ["c8"], "r5_hipotese_s_nao_negativo_retirada_da_frase_do_contrato": ["c8"], "r5_citacao_do_dispositivo_sem_piloto_sim": ["c8"], "r5_citacao_do_dispositivo_com_numero_de_desempenho": ["c8"],
       "r5_controle_negativo_invertido_s_estrela_no_lugar_de_uma_oitava_a_menos": ["c13"], "r5_adversario_com_duas_solucoes": ["c13"], "r5_contraexemplo_com_b_no_meio_ou_abaixo": ["c13"], "r5_um_pendente_entre_os_ratificados": ["c11"], "r5_ratificacao_pendente_esvaziada": ["c11"], "r5_sha256_da_fala_28_trocado_no_pino": ["c11"],
       "r5_fala_28_adulterada": ["c5", "c11"], "r5_estatuto_antigo_restaurado": ["c11"], "r5_estatuto_antigo_plantado_no_texto": ["c11"], "r5_frase_da_ratificacao_d101_retirada_do_texto": ["c11"], "r5_um_ratificado_retirado": ["c11"], "r5_errata_e36_sem_a_clausula_do_limite_na_folha": ["c8"]}
ok_neg = all(set(esp[k]) & set(R[k][1]) and "MECHANICS_CHECK_FAILED" in R[k][0] for k in esp) and R["r5_errata_e36_sem_a_clausula_do_limite_na_folha"][1] == ["c8"] and R["gate_trocado"][1] == ["c10"] and R["numero_do_contrato_trocado"][1] == ["c6"] and R["escada_um_a_menos"][1] == ["c1"] and R["frase_vedada_plantada"][1] == ["c9"] and R["kernel_nao_verificado"][1] == ["c2"] and R["raiz_sem_o_import"][1] == ["c3"] and all(R[k_][1] == ["c11"] for k_ in ("campo_novo_inexistente_na_estrutura", "nome_novo_dito_ratificado", "estatuto_dos_nomes_ratificados_d101_retirado_do_texto")) and R["nome_novo_inexistente_na_pedra"][1] == ["c2", "c11"] and all(R[k_][1] == ["c6"] for k_ in ("ponte_caso_trocado", "ponte_fundo_em_n_oitavas_trocado", "ciclo_instancia_sem_solucao_com_solucao", "ciclo_epsilon_fora_do_intervalo")) and R["forma_do_tempo_retirada_do_texto"][1] == ["c8"] and R["teorema_da_r4_fora_das_ancoras"][1] == ["c2"] and all(R[k_][1] == ["c8"] for k_ in ("clausula_do_limite_retirada_do_texto", "clausula_do_limite_retirada_de_um_campo", "clausula_do_limite_em_ingles_retirada")) and R["ancora_nova_tirada_do_contrato"][1] == ["c2"] and R["seis_nomes_retirados_do_texto"][1] == ["c11"] and all(R[k_][1] == esp[k_] for k_ in esp if k_.startswith("r5_"))   # (R5: cada controle novo reprova EXATAMENTE a checagem esperada)
_tudo = bool(out["all_verified"] and ok_neg)
print("TUDO PASSOU" if _tudo else "FALHOU", "| controles negativos como esperado:", ok_neg)
J = {"tudo_passou": _tudo, "veredito": out["verdict"], "all_verified": out["all_verified"], "n_checks": (out.get("mechanics") or {}).get("n_checks"), "checks": [(c["id"], c["ok"]) for c in (out.get("mechanics") or {}).get("checks") or []],
     "controles_negativos": {k: {"verdict": vd, "falhos": fl, "esperado_contem": esp[k]} for k, (vd, fl) in R.items()}, "numeros": v.get("numeros"), "bell": v.get("bell"), "n_ancoras": CONTR["n_ancoras"], "n_flags": CONTR["n_flags"], "n_nomes": CONTR["n_nomes"], "n_nomes_novos": CONTR["n_nomes_novos"], "n_falas": CONTR["n_falas"], "ponte": v.get("ponte"), "escada": CONTR["expected_ladder"], "pedra_sha256": CONTR["source_sha256"][rel],
     "nota": "teste OFFLINE do registro sobre um core de ensaio (v409 selada + o kernel do sandbox k410c lido do audit.log); nao e' o rito nem o ensaio a seco; validade no kernel nao e' creditacao"}
p = os.path.join(HERE, "TESTE_AESCALA_OFFLINE_v410.json"); open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
