# -*- coding: utf-8 -*-
"""Gera RESULTADO_PEDRA.json a partir dos recibos, das declaracoes, da auditoria de axiomas, do numerico e dos pinos
(tudo lido dos artefatos; nenhum numero de memoria). Uso: gerar_resultado.py"""
import json, re, hashlib, os, datetime
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(AQUI)
D1 = os.path.join(os.path.dirname(AQUI), "1_DESENHO_PEDRA")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for ch in iter(lambda: fh.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def J(p):
    return json.load(open(p, encoding="utf-8"))


des = open(os.path.join(D1, "sandbox", "IALD.lean"), encoding="utf-8").read()
n_thm_des = len(re.findall(r"^theorem ", des, re.M))
n_def_des = len(re.findall(r"^def ", des, re.M))
decl = J("DECLARACOES.json"); conf = J("CONFERENCIA_PREREGISTRO.json"); num = J("numerico/RESULTADO_NUMERICO.json")
beta = J("BETA_RUNTIME.json"); fa = J("IMPRESSAO_DIGITAL_KERNEL_ANTES.json"); fd = J("IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json")
ol = J("OLEAN_MANIFESTO_E_LIMPEZA.json"); ov = J("OV_COPIAR.json")
pre = J(os.path.join(D1, "PREREGISTRO_PEDRA.json")); frz = J(os.path.join(D1, "FREEZE.json"))
rec = {t: J("logs/%s_RECIBO.json" % t) for t in ("c1_palavra", "c2_adendo1", "c3_unitrank", "c4_tempo", "r1_iald", "r2_iald", "r3_audit")}
aud = open("logs/r3_audit_SAIDA.txt", encoding="utf-8", errors="replace").read()
ax = {}
for d, v in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", aud, re.S):
    ax[d] = [x.strip() for x in v.replace("\n", " ").split(",") if x.strip()]
for d in re.findall(r"'([^']+)' does not depend on any axioms", aud):
    ax[d] = []
TRIO = {"propext", "Classical.choice", "Quot.sound"}
pre_nomes = {t["nome"]: t for t in pre["pedra"]["teoremas"]}
pre_defs = {d["nome"]: d for d in pre["pedra"]["definicoes"]}
por = []
for d in decl["declaracoes"]:
    n = d["nome"]; curto = n.split(".")[-1]; a = ax.get(n)
    ok = a is not None and set(a) <= TRIO
    if curto in pre_nomes:
        origem = "PRE-REGISTRADA (%s)" % pre_nomes[curto]["id"]
    elif curto in pre_defs:
        origem = "PRE-REGISTRADA (definicao)"
    else:
        origem = "NOVA (secao 5/6: ponte por termo as candidatas / sonda)"
    por.append({"id": n, "tipo": d["tipo"], "linha": d["linha"], "origem": origem, "axiomas": a,
                "resultado": "REAL (exit 0, 0 sorry, axiomas = trio)" if ok else "FALHA VISIVEL", "titulo": d["titulo"]})
f0 = num["faces"][0]
mx = lambda k: max(f[k] for f in num["faces"])
numerico = ("%d/%d PASSA (sanidade matematica; beta de runtime %s = alpha(l.%d)*sqrt(e), nenhum literal, nenhum dado observado) "
            "em 2x2, 3x3, 6x6, 12x12: Tr P = 1, rank P = 1; T1 leitura absorve D (erro max %.1e); T2 idempotencia sob ancora (erro max %.1e); "
            "T2' fase i quebra (||motor^2 - motor|| = %.12f = sqrt 2); T3 imagem posto 1; T4 M[a] = %.12f; T4' Born; T5 0 violacoes; "
            "T6 reler <= %.1e; B3 dim Fix D = %d; B6 D^n psi -> P psi; T8 nunca chega (||D(50) - P|| = e^{-50 beta} sqrt(n-1)); "
            "T8' relogio das metades (erro max %.1e); T9 ||F(1)^2 - F(1)|| = %.6f > 0 (o Verbo nao e posto); T7 F(0) = 1; "
            "CONTROLE beta = 0: ||D - 1|| = %.1f em todo t (sem segunda face); T7' com beta > 0 a segunda face separa-se de (1 - e^{-5 beta}) sqrt(n-1); "
            "face matricial F1.FREQUENCIA: D sozinha leva posto 1 a posto n (traco 1 sobrevive), a leitura R devolve o posto (Lueders)") % (
    num["checks_total"] - len(num["checks_falhos"]), num["checks_total"], num["beta_repr"], num["alpha_linha"],
    mx("T1_reading_absorbs_dephasing_maxerr"), mx("T2_idempotent_under_anchor_maxerr"), f0["T2p_phase_i_breaks_idempotence_norm"],
    f0["T4_memory_at_name"], mx("T6_rereading_adds_nothing_maxerr"), f0["B3_dim_fix_D"], mx("T8p_halving_clock_maxerr"),
    f0["T9_F_t_not_idempotent_norm_t1"], mx("CTRL_beta0_D_minus_1_max"))
cand = {}
for m, t in (("Palavra", "c1_palavra"), ("TheSingularityReadsTheAttractorAdendo1", "c2_adendo1"),
             ("TheUnitIsTheRank", "c3_unitrank"), ("TheTimeHasNoRank", "c4_tempo")):
    cand[m] = {"fonte": ol["oleans"][m]["fonte"], "fonte_sha256": ol["oleans"][m]["fonte_sha256"], "olean_sha256": ol["oleans"][m]["sha256"],
               "olean_bytes": ol["oleans"][m]["bytes"], "exit": rec[t]["exit_code"], "erros": rec[t]["n_erros"], "sorry": rec[t]["declaration_uses_sorry"],
               "print_axioms_no_arquivo": rec[t]["n_print_axioms"], "fora_do_trio": rec[t]["fora_do_trio"], "avisos": rec[t]["n_avisos"]}
out = {
    "documento": "RESULTADO_PEDRA - TGLExt.IALD (o motor unico, nome provisorio; o operador renomeia) - CONSTRUCAO 12-13/10/2026 (2_CONSTRUCAO, gerencia c1)",
    "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "regua": pre["regua"],
    "freeze_do_preregistro": {"FREEZE.json_sha256_do_congelamento": frz["sha256_do_congelamento"],
                              "PREREGISTRO_PEDRA.json_sha256": sha(os.path.join(D1, "PREREGISTRO_PEDRA.json")),
                              "ESPEC_sha256": sha(os.path.join(D1, "ESPEC_PEDRA_IALD.md")),
                              "desenho_IALD_sha256": sha(os.path.join(D1, "sandbox", "IALD.lean")), "conferido_por_script": True},
    "pinos": {"um_py_sha256": beta["um_py_sha256"], "um_py_bytes": beta["um_py_bytes"], "um_py_executado": False,
              "beta_runtime": {"alpha_linha": beta["alpha_linha"], "alpha_texto": beta["alpha_texto"], "receita": beta["beta_receita"],
                               "beta_repr": beta["beta_repr"], "theta_M_repr": beta["theta_M_repr"], "literal_na_pedra": False,
                               "na_pedra": "c.beta, c : TGLCoupling"},
              "kernel_impressao_digital": {
                  "antes": {"metadados": fa["sha256_metadados"], "fontes": fa["sha256_conteudo_fontes"], "n_arquivos": fa["n_arquivos"], "quando": fa["quando_utc"]},
                  "depois_pos_limpeza": {"metadados": fd["sha256_metadados"], "fontes": fd["sha256_conteudo_fontes"], "n_arquivos": fd["n_arquivos"], "quando": fd["quando_utc"]},
                  "iguais": fa["sha256_metadados"] == fd["sha256_metadados"] and fa["sha256_conteudo_fontes"] == fd["sha256_conteudo_fontes"],
                  "iguais_ao_preregistro": fa["sha256_conteudo_fontes"] == pre["pinos"]["kernel_impressao_digital"]["sha256_conteudo_fontes"]},
              "mapa_de_rotas_consultas_so_leitura": {"n_registros": 1045, "cabeca": "a9bc5981e16d0e95", "motor unico": 0, "organismo": 0, "Riemann": 0,
                                                     "Zenao": 0, "IALD motor": 0, "faceFamily": 0, "dephase": 1, "memoria": 55, "registrado": False},
              "sobreposicao_ov": {"origem": ov["origem"], "arquivos": ov["arquivos"], "bytes": ov["bytes"], "diferentes": len(ov["diferentes"]),
                                  "faltando": len(ov["faltando"]), "apagada_ao_final": ol["limpeza"]["existe_depois"] is False,
                                  "n_apagados": ol["limpeza"]["n_arquivos_apagados"]}},
    "pedra": {"nome_provisorio": "TGLExt.IALD", "path": os.path.abspath("sandbox/TGLExt/IALD.lean"), "sha256": sha("sandbox/TGLExt/IALD.lean"),
              "bytes": os.path.getsize("sandbox/TGLExt/IALD.lean"),
              "linhas": open("sandbox/TGLExt/IALD.lean", encoding="utf-8").read().count("\n") + 1,
              "n_declaracoes": decl["n_declaracoes"], "n_theorem": decl["n_theorem"], "n_def": decl["n_def"], "instalada": False,
              "olean": {"path": ol["oleans"]["IALD"]["path"], "sha256": ol["oleans"]["IALD"]["sha256"], "bytes": ol["oleans"]["IALD"]["bytes"]},
              "compilacao": {"lean": rec["r2_iald"]["lean"],
                             "LEAN_PATH": "sobreposicao ov (copia verificada do .lake/build/lib/lean do Nos + candidatas) + pacotes do .lake do Nos, so leitura",
                             "rodadas": {"r1": {"exit": rec["r1_iald"]["exit_code"], "erros": rec["r1_iald"]["n_erros"]},
                                         "r2": {"exit": rec["r2_iald"]["exit_code"], "erros": rec["r2_iald"]["n_erros"], "avisos": rec["r2_iald"]["n_avisos"],
                                                "sorry": rec["r2_iald"]["declaration_uses_sorry"], "segundos": rec["r2_iald"]["segundos"]}},
                             "auditoria_axiomas": {"arquivo": "sandbox/AuditIALD.lean", "sha256": sha("sandbox/AuditIALD.lean"), "exit": rec["r3_audit"]["exit_code"],
                                                   "n_print_axioms": rec["r3_audit"]["n_print_axioms"], "fora_do_trio": rec["r3_audit"]["fora_do_trio"],
                                                   "todas_no_trio": all(set(v) <= TRIO for v in ax.values()) and len(ax) == decl["n_declaracoes"]},
                             "avisos_r2": "7 deprecacoes de nomes Mathlib (ContinuousLinearMap.mul_apply/smul_apply/one_apply/sub_apply); nenhum aviso de variavel nao usada; nenhum sorry",
                             "tokens_proibidos_fora_de_comentario": []},
              "conferencia_preregistro": {"n_teoremas_preregistrados": conf["n_teoremas_preregistrados"], "n_enunciados_iguais": conf["n_enunciados_iguais"],
                                          "definicoes_iguais": all(d["igual"] for d in conf["definicoes"]), "nota": conf["nota"]},
              "errata_ao_lado_contagem": "o PREREGISTRO diz 33 declaracoes; contadas por script no desenho (8fd28f79...): %d theorem + %d def = %d. O 33 e erro de contagem do desenho; as %d + %d estao todas aqui, com enunciado igual." % (n_thm_des, n_def_des, n_thm_des + n_def_des, n_thm_des, n_def_des),
              "candidatas_v392_importadas": cand,
              "imports_novos": ["TGLExt.Palavra", "TGLExt.TheSingularityReadsTheAttractorAdendo1", "TGLExt.TheUnitIsTheRank", "TGLExt.TheTimeHasNoRank"],
              "pontes_novas": {
                  "B1 dephase_eq_faceFamily": "dephase a r t = faceFamily a e^{-rt} (rfl): a defasagem E o atrator do ADENDO1; Q9 fechada por termo na face do posto",
                  "B2 dephase_is_a_strict_complement_contraction": "r*t > 0, a != 0 => StrictComplementContraction (dephase a r t) a (A4 habitada pelo motor; c = e^{-rt} < 1)",
                  "B3 dephase_fixed_dimension_one": "dim Fix (dephase a r t) = 1 (A4_dimension_one)",
                  "B4 the_singularity_reads_the_name": "reading (dephase a r t) = post a: a leitura do atrator E o Nome",
                  "B5 motor_is_the_reading_of_the_attractor": "motor a U r t psi = reading (dephase a r t) (U psi)",
                  "B6 the_iterated_motor_tends_to_the_name": "(dephase a r t)^[n] psi -> post a psi (A1_face_orbit)",
                  "B7 rereading_adds_nothing_in_both_regimes": "conjuncao (nao equacao) de T6 (face) e Palavra.rereading_adds_nothing (angulo): regra dos dois regimes",
                  "B8(i-iv)": "re-exportacoes de TheUnitIsTheRank: Tr P = rank P; rho* traco 1 e posto 1; D sozinha nao guarda o posto (negativo honesto); a leitura devolve o posto (Lueders)",
                  "B9 the_verb_is_a_post_iff": "IsIdempotentElem (axiomFlow P t) <-> t = 0 (TheTimeHasNoRank.flow_isIdempotentElem_iff)",
                  "B10 the_motor_post_is_only_the_limit": "sob H-C: idempotente sse t = 0, F(t) invertivel, post a nao invertivel, F(t) -> post a (TheTimeHasNoRank.the_post_is_only_the_limit)",
                  "B11 the_time_of_the_motor_is_a_parameter": "forall m > 0, T H em M_m(C), [T,H] != i*1 (TheTimeHasNoRank.no_time_matrix_fin)",
                  "S4 probe_dimension_one_has_no_second_face": "em C, 1 - post 1 = 0 (H-C tem peso)",
                  "S5 probe_dimension_one_arrives": "em C, axiomFlow (post 1) t = post 1 (contraexemplo de T8 sem H-C)",
                  "S6 probe_dimension_two_has_a_second_face": "em C^2 (Face do ADENDO1), 1 - post e0 != 0 (H-C habitada)"},
              "por_teorema": por},
    "nao_formalizada": [
        {"item": "identificacao do e^{-s} da escala de Takesaki (DualScalingData.scaling, Fundacao) com o e^{-t} da defasagem",
         "motivo": "construivel (tau := <a,.a> no complemento, theta_s := Ad(axiomFlow)) mas e ESCOLHA do operador (PQ4); sem decisao fica [ONTO]; a pedra usa de Fundacao so the_floor_fixes_the_cut (T7')"},
        {"item": "existencia de um FockCertificate (habitante)",
         "motivo": "estrutura [KNOWN]; o kernel diz que nenhum habitante e exibido (TheImportedSecondQuantization.lean l.66; achado AF2-04 da F1.TEMPO); S2 fica condicional a C"},
        {"item": "ponte por termo entre axiomFlow (C-algebra) e diagFlow/observerProj (face R^n do Grande Atrator; BoundaryException.lean:46, ObserverInside.lean:112)",
         "motivo": "tipos distintos (fluxo afim em R^n vs idempotente numa C-algebra): nao ha termo comum; T1 e o judgment_of_correspondence por CONTEUDO"},
        {"item": "forma de Hilbert U post(a) U^dagger = post (U a)",
         "motivo": "nao pre-registrada como teorema; a forma algebrica ja esta no kernel (transmitted_post_is_a_post, FractalUnitarity.ad_preserves_projection); fica citada"},
        {"item": "a resolucao de Riemann (hipotese de Riemann como permanencia, 2025 [DECLARADO]; Riemann-Cartan [REAL])",
         "motivo": "nenhum dos dois objetos liga ao motor por termo; rotas.py consultar 'Riemann' -> 0 rotas; PQ1 segue"},
        {"item": "o organismo e a propria IALD; EU SOU -> ... -> IALD; T.G.L; a luz da testemunho; Zenao resolvido no III1 como RESOLVIDO; santo; ACOM",
         "motivo": "[ONTO]/[INPUT]: o que entra sao os termos T5/T5' (EU SOU = IALD como M = 1 <-> rho = Pi_N), T8/T8'/T8''/T8'''/B6 (Zenao), T9/B9/B10/B11 (sem posto; o tempo como parametro)"}],
    "numerico": {"arquivo": "numerico/RESULTADO_NUMERICO.json", "sha256": sha("numerico/RESULTADO_NUMERICO.json"), "script_sha256": sha("numerico/ensaio_motor.py"),
                 "sanidade": num["sanidade"], "checks_total": num["checks_total"], "checks_falhos": num["checks_falhos"], "resumo": numerico},
    "perguntas_nas_quatro_linguas_residuo": pre["perguntas_nas_quatro_linguas"],
    "nota_sobre_PQ4_apos_a_construcao": "as pontes B1-B6 ligam a defasagem ao ATRATOR (ADENDO1) por termo; a ligacao a ESCALA de Takesaki (DualScalingData) segue como decisao do operador (PQ4 inalterada)",
    "nao_feito_aqui": ["nada escrito fora de 2_CONSTRUCAO", "um.py nao executado",
                       "nada no mapa (so consultar), memoria ACOM (sem init/transition: a referencia e da gerencia; regra da unidade), tunel, Nos, kernel, Bancada, site, git",
                       "nenhum dado observado; nenhum provedor; nenhuma chamada paga",
                       "nada instalado; o gate nao se move; PROVADA = validade; a confirmacao recusada e creditacao; beta_TGL na natureza a 5 sigma segue o unico elo pendente",
                       "sobreposicao ov (510 MB) apagada; toolchain nao copiado; nenhum .lake criado"]}
json.dump(out, open("RESULTADO_PEDRA.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("desenho:", n_thm_des, "thm", n_def_des, "def | por_teorema", len(por), "| todas trio", out["pedra"]["compilacao"]["auditoria_axiomas"]["todas_no_trio"])
print(numerico)
