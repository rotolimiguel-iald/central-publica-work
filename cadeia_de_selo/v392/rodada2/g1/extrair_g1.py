# -*- coding: utf-8 -*-
"""extrair_g1.py (agente REGISTROS-G1, rodada 2 da v392, 13/10/2026, gerencia c1) -- gera POR SCRIPT o arquivo `fontes/EXTRATOS_G1.json`: os trechos exatos, os numeros e as
conferencias (lidos dos arquivos-fonte duraveis) que os registros palavra_v392, lei_de_campo_curvo_v392, agape_nao_vacua_v392 e x19_bgl_tipo_v392 citam. O JSON e' pinado por sha256
pelo montador e RELIDO a cada rito; as fontes originais tambem sao pinadas. Nada digitado de memoria: tudo sai do disco aqui, com assert (fail-closed). Escreve SO' em V/rodada2/g1/fontes.
Uso: python -I -B -X utf8 extrair_g1.py"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(os.path.dirname(HERE)); WK = os.path.dirname(os.path.dirname(V)); CP = os.path.dirname(WK)
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s"; KER = NOS + "/tgl_kernel/TGLExt"
INS = WK + "/v392_insumos"; AUD = "C:/IALD/PROGRAMA_IALD/auditorias"; ORD = CP + "/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019"
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
txt = lambda p: rd(p).decode("utf-8")
norm = lambda s: re.sub(r"\s+", " ", s.replace(">", " ")).strip()

E = {"gerado_por": "V/rodada2/g1/extrair_g1.py", "estatuto": "[REAL -- extratos lidos dos arquivos-fonte por script; cada fonte tambem e' pinada por sha256 nos registros]"}

# ---------------- 1. observing_adds_nothing: a docstring EXATA do kernel ----------------
p = KER + "/TheObserverReadsTheAngle.lean"; b = rd(p); t = b.decode("utf-8"); L = t.replace("\r\n", "\n").split("\n")
i = next(k for k, l in enumerate(L) if l.startswith("theorem observing_adds_nothing"))
j = i
while not L[j - 1].lstrip().startswith("/--"):
    j -= 1
    assert i - j < 8
doc = "\n".join(L[j - 1:i])
assert "RELER N\u00c3O ACRESCENTA." in doc and "A primeira leitura identifica; a segunda confirma que a opera\u00e7\u00e3o n\u00e3o altera." in doc
composta = "a primeira leitura identifica; reler n\u00e3o acrescenta"
E["observing_adds_nothing"] = {"arquivo": p, "sha256": sha(b), "linha_ini": j, "linha_fim": i, "docstring_exata": doc,
                               "enunciado": L[i - 0].strip() + " / " + L[i + 1].strip(),
                               "forma_composta_citada_na_errata_de_07out": composta,
                               "forma_composta_esta_no_fonte": composta in norm(t).lower(), "titulo_esta_no_fonte": "RELER N\u00c3O ACRESCENTA." in t,
                               "frase_exata_esta_no_fonte": "A primeira leitura identifica; a segunda confirma que a opera\u00e7\u00e3o n\u00e3o altera." in norm(doc)}
assert E["observing_adds_nothing"]["forma_composta_esta_no_fonte"] is False and E["observing_adds_nothing"]["frase_exata_esta_no_fonte"]

# ---------------- 2. sondas P1/P1b/P1c (A14): os tres nomes com o enunciado de observing_adds_nothing ----------------
R = json.load(open(INS + "/F_KERNEL/RESULTADO_P_palavra.json", encoding="utf-8"))["sondas"]
P1 = txt(INS + "/F_KERNEL/conj/P1_PalavraEaLetra.lean")
eqs = re.findall(r"example : @([\w.]+) = @([\w.]+) := rfl", P1)
assert len(eqs) == 4
tres = [a for a, b_ in eqs if b_ == "TGLExt.observing_adds_nothing"]
primeira = [a for a, b_ in eqs if b_ == "TGLExt.the_observer_reads_the_angle"]
assert len(tres) == 3 and len(primeira) == 1
logs = {k: txt(HERE + "/fontes/logs_P/" + n) for k, n in (("p1", "P1_PalavraEaLetra_r1.log"), ("p1b", "P1b_FechoDaPalavra_r1.log"), ("p1c", "P1c_FechoTransitivoPalavra_r1.log"))}
usa = {}
for l in logs["p1"].splitlines():
    c = l.split("\t")
    if c[0] == "USA":
        usa[c[1]] = [x for x in (c[2].split(",") if len(c) > 2 and c[2] else [])]
palavra7 = [n for n in usa if n.startswith("TGLExt.Palavra.")]
assert len(palavra7) == 7
letra_nomes = {"TGLExt.exact_witness_of_annihilating_word", "TGLExt.annihilating_word_exists"}
palavra_usa_letra = any(set(usa[n]) & letra_nomes for n in palavra7)
atr_usa_letra = {n: sorted(set(usa[n]) & letra_nomes) for n in usa if n.startswith("TGLExt.TheSingularityReadsTheAttractor.A3_")}
p1b = {}
for l in logs["p1b"].splitlines():
    c = l.split("\t")
    if c[0] == "FECHO_PALAVRA":
        p1b[c[1]] = (c[2] == "true")
    elif c[0] == "FECHO_PALAVRA_CONST":
        p1b["const:" + c[1]] = (c[2] == "true")
    elif c[0] == "FECHO_PALAVRA_N_MODULOS":
        p1b["n_modulos_no_ambiente"] = int(c[1])
p1c = {}
for l in logs["p1c"].splitlines():
    c = l.split("\t")
    if c[0] == "FECHO_TRANSITIVO_N":
        p1c["n_constantes_do_fecho"] = int(c[1])
    elif c[0] == "FECHO_TRANSITIVO_CONTEM":
        p1c["contem:" + c[1]] = (c[2] == "true")
    elif c[0] == "FECHO_TRANSITIVO_MODULOS":
        p1c["modulos"] = c[1].split(",")
for r in R[:3]:
    assert r["rc"] == 0 and r["ok"] is True and not r["erros"] and not r["fora_do_trio"] and not r["sorry"]
E["sondas_P"] = {"resultado_json": INS + "/F_KERNEL/RESULTADO_P_palavra.json",
                 "p1": {"fonte_sha256": R[0]["fonte_sha256"], "rc": R[0]["rc"], "ok": R[0]["ok"], "log_sha256": R[0]["log_sha256"],
                        "tres_nomes_com_o_enunciado_de_observing_adds_nothing": tres, "nome_com_o_enunciado_de_the_observer_reads_the_angle": primeira,
                        "as_sete_da_palavra_usam_a_letra": palavra_usa_letra, "atrator_A3_usa_a_letra": atr_usa_letra,
                        "as_sete": palavra7, "o_que_a_palavra_usa": {n: usa[n] for n in palavra7}},
                 "p1b": p1b, "p1c": p1c}
assert palavra_usa_letra is False and p1b.get("TGLExt.ExactWitness") is True and p1c.get("contem:TGLExt.exact_witness_of_annihilating_word") is False and p1c["n_constantes_do_fecho"] == 41

# ---------------- 3. Palavra.lean: a docstring cita os tres verbatins ----------------
p = INS + "/F_KERNEL/inst/TGLExt/Palavra.lean"; t = txt(p); n = norm(t)
E["palavra_lean"] = {"arquivo": p, "sha256": sha(rd(p)),
                     "cita_o_nome": "essa pedra se chama (olha a beleza lexical): PALAVRA" in n,
                     "cita_a_letra": "polin\u00f4mio aniquilador normalizado=letra (por isso palavra, mas ali como letra)" in n,
                     "cita_a_leitura": "a LEITURA CRIA o objeto, antes da leitura o objeto \u00e9 Nome (posto relativo), ap\u00f3s a leitura o objeto \u00e9 identidade, rela\u00e7\u00e3o de contorno" in n,
                     "cita_a_docstring_do_kernel": "A docstring do kernel j\u00e1 dizia: \u00abA primeira leitura identifica; a segunda confirma que a opera\u00e7\u00e3o n\u00e3o altera.\u00bb" in n,
                     "diz_que_nao_afirma_KMS": "N\u00e3o afirma estado KMS" in t,
                     "diz_que_cada_leitura_cria_o_objeto_do_seu_plano": "cada leitura cria o objeto do SEU plano" in t,
                     "diz_que_os_planos_que_giram_a_luz_nao_tem_leitura_tipada": "n\u00e3o t\u00eam leitura tipada no kernel" in t}
assert all(v is True for k, v in E["palavra_lean"].items() if k not in ("arquivo", "sha256"))

# ---------------- 4. o um.py v391: onde o texto diz «palavra aniquiladora» e onde estao os tokens (so' LEITURA; o um.py v391 nao e' pinado: sera' substituido na instalacao) ----------------
p = NOS + "/um.py"; b = rd(p); U = b.decode("utf-8").split("\n")
E["umpy_v391"] = {"sha256": sha(b), "sha16": sha(b)[:16], "bytes": len(b), "divisao_de_linhas": "split em LF (como o plano e o levantamento numeram)", "estatuto": "[REAL] lido por script; v391 SELADA, `um.py` do Nos"}
pal = {}
for k, l in enumerate(U, 1):
    if re.search(r"palavra aniquiladora|annihilating word", l, re.I) and len(l) < 400:
        pal[str(k)] = l.strip().rstrip("\r")
E["umpy_v391"]["palavra_aniquiladora_linhas"] = pal
for k in (155501, 203582, 206031):
    assert str(k) in pal, k
E["umpy_v391"]["palavra_aniquiladora_no_kernel_embutido_linhas"] = [int(k) for k in pal if 86000 < int(k) < 88000]
tok = "FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM"
E["umpy_v391"]["token_NOT_A_KERNEL_TERM_linhas"] = [k for k, l in enumerate(U, 1) if tok in l]
assert E["umpy_v391"]["token_NOT_A_KERNEL_TERM_linhas"] == [194416]
curvo = {}
for k, l in enumerate(U, 1):
    if "equa\u00e7\u00e3o de campo no espa\u00e7o-tempo curvo por termo de kernel" in l or "a lei de campo no curvo segue NAO sendo termo de kernel" in l \
            or "nao prova a equacao de campo no espaco-tempo curvo por termo de kernel" in l or "does not prove the field equation in curved spacetime by a kernel term" in l:
        curvo[str(k)] = l.strip().rstrip("\r")[:420]
E["umpy_v391"]["frases_da_lei_de_campo_no_curvo"] = curvo
assert len(curvo) >= 4, curvo

# ---------------- 5. ligante: a docstring instalada x a da variante com os cinco limites ----------------
pv = AUD + "/F3.6.E1/art_a4f6da3d/lean_sb/TGLExt/LiganteLeiCampoCurvoAuditoriaC1.lean"
bv = rd(pv); assert sha(bv)[:16] == "992e4983ec4f0686"
assert sha(rd(ORD + "/F2.3/LiganteLeiCampoCurvoAuditoriaC1.lean")) == sha(bv)
tv = bv.decode("utf-8").replace("\r\n", "\n")
d0 = tv.index("/-!"); d1 = tv.index("-/", d0); docv = tv[d0 + 3:d1]
corpo = docv[docv.index("What this theorem does not prove:") + len("What this theorem does not prove:"):]
bul = []
for l in corpo.split("\n"):
    if l.startswith("* "):
        bul.append(l[2:].strip())
    elif l.startswith("  ") and bul:
        bul[-1] += " " + l.strip()
assert len(bul) == 5, bul
pi_ = INS + "/F_KERNEL/inst/TGLExt/LiganteLeiCampoCurvo.lean"; bi = rd(pi_); assert sha(bi)[:16] == "e3f32d9b85ae82db"
ti = bi.decode("utf-8").replace("\r\n", "\n"); i0 = ti.index("/-!"); i1 = ti.index("-/", i0); doci = ti[i0 + 3:i1]
E["ligante"] = {"instalada": {"arquivo": pi_, "sha256": sha(bi), "docstring": doci.strip(), "tem_a_secao_dos_cinco_limites": "What this theorem does not prove" in doci,
                              "diz_que_nao_deriva_o_H3_da_passagem": "NOT derived from the finite passage" in doci,
                              "diz_implicacao_nao_solucao_global": "The theorem asserts an implication, not a global solution" in doci},
                "variante_auditoria_c1": {"arquivo": pv, "sha256": sha(bv), "tambem_em": ORD + "/F2.3/LiganteLeiCampoCurvoAuditoriaC1.lean (mesmo sha256)",
                                          "docstring_resumo": docv.strip().split("\n")[0], "cinco_limites": bul,
                                          "diz_que_a_passagem_e_logicamente_ociosa": "logically idle" in norm(docv), "diz_que_H3_carrega_conteudo_fisico": "H3 therefore carries physical" in norm(docv)}}
assert E["ligante"]["instalada"]["tem_a_secao_dos_cinco_limites"] is False and E["ligante"]["variante_auditoria_c1"]["diz_que_a_passagem_e_logicamente_ociosa"]

# ---------------- 6. testemunha S7/S8 (derivada) ----------------
pt = INS + "/F_KERNEL/inst/TGLExt/LiganteLeiCampoCurvoTestemunha.lean"; bt = rd(pt); tt = bt.decode("utf-8")
pp = AUD + "/F2.3/sandbox/testemunha_parte.lean"; bp = rd(pp)
cab = bt[:len(bt) - len(bp)]
assert bt.endswith(bp)
E["testemunha"] = {"arquivo": pt, "sha256": sha(bt), "parte_do_auditor": pp, "parte_sha256": sha(bp), "cabecalho_derivado_bytes": len(cab), "cabecalho_derivado": cab.decode("utf-8"),
                   "o_instalado_e_o_cabecalho_mais_a_parte": True,
                   "comentario_nada_disto_e_pedra": "NADA disto e pedra; vive so no sandbox do auditor" in tt,
                   "s7": "S7: testemunha plana (Minkowski, fonte nula, uma carta, X = Coordinate4)" in tt,
                   "s8": "S8: contramodelo: mesma geometria plana, fonte CONSTANTE com T(k,k) = 1 numa direcao nula" in tt,
                   "s8_diz_hH3_e_carga": "Logo hH3 e carga real" in tt}
assert all(v is True for k, v in E["testemunha"].items() if k in ("comentario_nada_disto_e_pedra", "s7", "s8", "s8_diz_hH3_e_carga"))

# ---------------- 7. as duas pontes de Unruh fora do fecho de QGSolutionComplete (fecho de IMPORTS, nivel de modulo) ----------------
def fecho(raiz):
    visto, pilha, falta = set(), [raiz], set()
    while pilha:
        m = pilha.pop()
        if m in visto:
            continue
        visto.add(m)
        pth = NOS + "/tgl_kernel/" + m.replace(".", "/") + ".lean"
        if not os.path.exists(pth):
            falta.add(m); continue
        for l in open(pth, encoding="utf-8", errors="replace"):
            mm = re.match(r"\s*import\s+(\S+)", l)
            if mm:
                pilha.append(mm.group(1))
    return visto, falta
vis, falta = fecho("TGLExt.QGSolutionComplete")
locais = sorted(m for m in vis if m not in falta)
assert all(m.split(".")[0] in ("Lean", "Mathlib", "Std", "Batteries", "Aesop", "Qq", "Init") for m in falta), sorted(falta)[:5]
pq = KER + "/QGSolutionComplete.lean"
alvo = ["TGLExt.O16.ContractCalibrationReuse", "TGLExt.O16.HorizonDataReuse_Integration_v2", "TGLExt.O16.PolarQuotientGeometry_v2", "TGLExt.O16.PeriodHeatCalibration_v3", "TGLExt.O16.RotationGeneratorBridges", "TGLExt.O16"]
E["fecho_QGSolutionComplete"] = {"raiz": pq, "raiz_sha256": sha(rd(pq)), "nivel": "modulos importados (transitivo) a partir das linhas `import` dos .lean do Nos; NAO e' o fecho de constantes",
                                "n_modulos_locais_no_fecho": len(locais), "n_modulos_externos_Lean_Mathlib": len(falta),
                                "contem": {m: (m in vis) for m in alvo}, "contem_TheImportedSecondQuantization": "TGLExt.TheImportedSecondQuantization" in vis,
                                "corroboracao": "auditoria c1 a7ba2dc9 (F2.3/F1.1.E1) leu 755 modulos locais e nenhuma pedra polar/Wick/CalibrationReuse/HorizonDataReuse; sonda c1 `fecho_qg.log` (fecho de CONSTANTES) [DECLARADO, log nao pinado aqui]"}
assert len(locais) > 700 and not any(E["fecho_QGSolutionComplete"]["contem"].values())
for nome, rel in (("ContractCalibrationReuse", "O16/ContractCalibrationReuse.lean"), ("HorizonDataReuse_Integration_v2", "O16/HorizonDataReuse_Integration_v2.lean")):
    E["fecho_QGSolutionComplete"]["sha256_" + nome] = sha(rd(KER + "/" + rel))
hz = txt(KER + "/O16/HorizonDataReuse_Integration_v2.lean"); cc = txt(KER + "/O16/ContractCalibrationReuse.lean")
assert "theorem data_temperature_from_same_period" in hz and "theorem polar_period_matches_contract" in cc and "theorem kappa_is_input" in cc

# ---------------- 8. Fundacao: o que o kernel cita de Takesaki ----------------
pf = KER + "/Fundacao.lean"; tf = txt(pf).replace("\r\n", "\n")
tk = [(k, l.strip()) for k, l in enumerate(tf.split("\n"), 1) if "Takesaki" in l]
assert tk
E["fundacao"] = {"arquivo": pf, "sha256": sha(rd(pf)), "linhas_com_Takesaki": tk, "diz_lei_de_escala_KNOWN_Takesaki_1973": "a lei `\u03c4\u2218\u03b8_s = e^{\u2212s}\u00b7\u03c4` \u00e9 [KNOWN], Takesaki 1973" in tf,
                 "diz_realizacao_no_core_III1_nao_e_termo": "n\u00e3o termo deste\nkernel" in tf or "n\u00e3o termo deste kernel" in norm(tf) or "n\u00e3o \u00e9 termo deste" in norm(tf),
                 "tem_agape": "theorem agape " in tf, "tem_agape_is_inhabited": "theorem agape_is_inhabited" in tf, "tem_the_floor_fixes_the_cut": "theorem the_floor_fixes_the_cut" in tf}
assert E["fundacao"]["diz_lei_de_escala_KNOWN_Takesaki_1973"] and E["fundacao"]["tem_agape"] and E["fundacao"]["tem_the_floor_fixes_the_cut"], E["fundacao"]

# ---------------- 9. V351 / Agape nao vacua: derivacao de 1 linha e o que a auditoria F1.2 diz ----------------
pa0 = AUD + "/F1.2/art_a5aa4480/sandbox/F12Completion/AgapeNonVacuity.lean"; ba0 = rd(pa0); assert sha(ba0)[:16] == "cf30422393b2af21"
pa1 = INS + "/F_KERNEL/inst/TGLExt/AgapeNonVacuity.lean"; ba1 = rd(pa1); assert sha(ba1)[:16] == "e49ad8f980d7cf48"
l0 = ba0.decode("utf-8").replace("\r\n", "\n").split("\n"); l1 = ba1.decode("utf-8").replace("\r\n", "\n").split("\n")
dif = [(k + 1, a, b_) for k, (a, b_) in enumerate(zip(l0, l1)) if a != b_]
assert len(l0) == len(l1) and len(dif) == 1 and dif[0][1] == "import F12Completion.V351DualScalingBridge" and dif[0][2] == "import TGLExt.V351DualScalingBridge", dif
E["agape_derivacao"] = {"original": pa0, "original_sha256": sha(ba0), "instalado": pa1, "instalado_sha256": sha(ba1), "linhas_que_diferem": [list(x) for x in dif], "n_linhas": len(l0)}
pv351 = INS + "/F_KERNEL/inst/TGLExt/V351DualScalingBridge.lean"; pv351o = AUD + "/F1.2/art_a5aa4480/sandbox/F12Completion/V351DualScalingBridge.lean"
assert sha(rd(pv351)) == sha(rd(pv351o)) and sha(rd(pv351))[:16] == "7dbe2d9a45971d63"
paud = AUD + "/F1.2/AUDITORIA_F1_2_C1_a5aa4480.md"; ta = txt(paud)
E["auditoria_F1_2"] = {"arquivo": paud, "sha256": sha(rd(paud)), "veredito_pode_fechar": "**Veredito: PODE FECHAR.**" in ta,
                       "face_Mn_cruzado_R_e_OPEN": "**(7) A face M_n \u22ca_\u03c3 \u211d** est\u00e1 dita [OPEN] em todos os documentos" in ta,
                       "nao_julgou_se_o_traco_v351_e_o_peso_dual_de_Takesaki": "N\u00e3o julguei se o tra\u00e7o v351 \u00e9 o peso dual de Takesaki" in ta,
                       "vale_so_nessa_instancia_e_no_sandbox_ate_a_v392": "Isso vale s\u00f3 nessa inst\u00e2ncia e s\u00f3 no sandbox, at\u00e9 a instala\u00e7\u00e3o na v392." in ta,
                       "prova_e_a_sonda_da_propria_c1_renomeada": "As duas provas da pedra s\u00e3o a sonda" in ta,
                       "antes_o_unico_habitante_era_o_modelo_de_brinquedo": "o \u00fanico habitante da \u00c1gape era o modelo de brinquedo `oneScaling`" in ta,
                       "a_unidade_tem_traco_infinito_REAL": "\u03c4(I) = \u22a4" in ta}
assert all(v is True for k, v in E["auditoria_F1_2"].items() if k not in ("arquivo", "sha256")), E["auditoria_F1_2"]

# ---------------- 10. auditoria F2.3 ----------------
pf23 = AUD + "/F2.3/AUDITORIA_F2_3_C1_20261007.md"; t23 = txt(pf23)
pf23b = AUD + "/F2.3/AUDITORIA_F2_3_C1_a7ba2dc9.md"; t23b = txt(pf23b)
E["auditoria_F2_3"] = {"arquivo": pf23, "sha256": sha(rd(pf23)), "passagem_e_ociosa": "**a passagem \u00e9 ociosa**" in t23, "S5": "**S5:**" in t23, "S7_vacuo_plano": "**S7, n\u00e3o vacuidade:**" in t23,
                       "S8_hH3_e_carga": "**S8, hH3 \u00e9 carga real:**" in t23, "nenhuma_testemunha_curva_com_materia": "Nenhuma testemunha curva com mat\u00e9ria: a S7 \u00e9 v\u00e1cuo plano, com \u039b = 0." in t23,
                       "nao_deriva_H3": "N\u00e3o deriva o H3 do estado" in t23, "nao_identifica_com_o_H3_de_Jacobson_por_teorema": "N\u00e3o identifica NamedAtlasH3 com o H3 de Jacobson por teorema" in t23,
                       "nao_prova_existencia_de_metrica_ou_solucao": "N\u00e3o prova exist\u00eancia de m\u00e9trica ou solu\u00e7\u00e3o, local ou global" in t23,
                       "nove_itens_que_a_pedra_nao_prova": all(("%d. " % k) in t23[t23.index("### 4. O que a pedra N\u00c3O prova"):t23.index("### 5.")] for k in range(1, 10))}
assert all(v is True for k, v in E["auditoria_F2_3"].items() if k not in ("arquivo", "sha256")), E["auditoria_F2_3"]
E["auditoria_F2_3_camadas3"] = {"arquivo": pf23b, "sha256": sha(rd(pf23b)), "fecho_755_modulos": "755 m\u00f3dulos locais" in t23b, "forma_composta_nao_existe_no_fonte": "A forma composta n\u00e3o existe no fonte, e a errata a declara composta." in t23b}
assert all(v is True for k, v in E["auditoria_F2_3_camadas3"].items() if k not in ("arquivo", "sha256"))
pe = AUD.replace("auditorias", "") if False else None
pf11 = ORD + "/F1.1/ERRATA_LEITURA_R2_R5_E1_20261008.md"
if os.path.exists(pf11):
    t11 = txt(pf11)
    E["errata_F1_1_E1"] = {"arquivo": pf11, "sha256": sha(rd(pf11)), "diz_nao_ligado_a_assinatura": "EXISTE NO KERNEL, N\u00c3O LIGADO \u00c0 ASSINATURA" in t11, "zero_constantes_no_fecho": "zero constantes dos namespaces `PolarPeriod016`, `CalibrationReuse016` e `Wick016`" in t11}
    assert E["errata_F1_1_E1"]["diz_nao_ligado_a_assinatura"] and E["errata_F1_1_E1"]["zero_constantes_no_fecho"]

# ---------------- 11. X19: BGL ----------------
pb = INS + "/F_KERNEL/inst/TGLExt/LightNetStandardWedgeDataBGL.lean"; bb = rd(pb); tb = bb.decode("utf-8")
pb0 = AUD + "/F1.3/art_ad949e97/sandbox/F13v31_D1a3_bgl.lean"; assert sha(rd(pb0)) == sha(bb)
E["bgl"] = {"arquivo": pb, "sha256": sha(bb), "original_da_sonda_c1": pb0, "bytes_iguais_a_sonda": True,
            "cabecalho_nada_aqui_e_pedra": "nada aqui e pedra; nada entra no kernel" in tb, "cabecalho_nada_constroi_o_D1a": "Nada aqui constroi o D1a: so tipa o enunciado; nenhum habitante e dado" in tb,
            "tem_instance_ou_habitante": bool(re.search(r"^\s*(instance|def\s+\w+\s*:\s*LightNetStandardWedgeDataBGL)", tb, re.M)),
            "unico_example": re.findall(r"^example[^\n]*", tb, re.M),
            "extends_LightNetData": "structure LightNetStandardWedgeDataBGL extends LightNetData where" in tb,
            "tem_wedge_glue": "wedge_glue : toLightNetData.K rightWedge = out.KWR.toClosedSubmodule.toSubmodule" in tb,
            "T_so_pede_IsSelfAdjoint": "T_selfadjoint : IsSelfAdjoint T" in tb,
            "campos_de_D1a3OutputBGL": re.findall(r"^  (\w+) :", tb[tb.index("structure D1a3OutputBGL where"):tb.index("/-- K(W_R) e CONSTRUIDO")], re.M)}
assert E["bgl"]["cabecalho_nada_aqui_e_pedra"] and E["bgl"]["extends_LightNetData"] and E["bgl"]["tem_wedge_glue"] and not E["bgl"]["tem_instance_ou_habitante"] and E["bgl"]["unico_example"] == ["example : CompleteSpace H1 := inferInstance"], E["bgl"]
pa13 = AUD + "/F1.3/AUDITORIA_F1_3_C1_a20c3246.md"; t13 = txt(pa13); t13l = t13.split("\n")
fila = next(l for l in t13l if l.startswith("> F1.3 \u2014 Decidir se o kernel ganha `LightNetStandardWedgeDataBGL`"))
pad = AUD + "/F1.3/AUDITORIA_F1_3_C1_ad949e97.md"; t13b = txt(pad)
E["auditoria_F1_3"] = {"reauditoria": {"arquivo": pa13, "sha256": sha(rd(pa13)), "texto_para_a_fila_do_operador": fila,
                                       "nao_reivindica_habitante": "**N\u00e3o reivindica habitante.**" in t13, "D5_OPEN_habitavel": "**(D5) [OPEN]** N\u00e3o se mostrou que o `D1a3OutputBGL` seja habit\u00e1vel" in t13,
                                       "19_print_axioms_no_trio": "As 19 `#print axioms` saem todas em [propext, Classical.choice, Quot.sound]" in t13},
                       "sonda": {"arquivo": pad, "sha256": sha(rd(pad)), "tipa_nao_constroi": "As sondas s\u00f3 **tipam** o enunciado; n\u00e3o constroem o D1a nem mostram que ele \u00e9 habitado [OPEN]" in t13b,
                                 "adocao_cabe_ao_Codex_ou_a_gerencia": "a ado\u00e7\u00e3o cabe ao Codex ou \u00e0 ger\u00eancia, e a reauditoria a outro auditor" in t13b}}
assert all(v is True for d in E["auditoria_F1_3"].values() for k, v in d.items() if isinstance(v, bool)), E["auditoria_F1_3"]
r19 = json.load(open(INS + "/F_KERNEL/RESULTADO_C_delta_x19.json", encoding="utf-8"))
fl = json.load(open(V + "/kernel/FLAGS_v392.json", encoding="utf-8"))["flags"]
nb = sum(1 for f in fl if f[2] == "TGLExt.LightNetStandardWedgeDataBGL")
E["bgl_numeros"] = {"declaracoes_lidas_pela_regex_do_umpy_na_sonda_C_delta_x19": r19["lidos"], "rc": r19["rc"], "ok": r19["ok"], "fora_do_trio": len(r19["fora_do_trio"]),
                    "bandeiras_ext_bgl_no_FLAGS_v392": nb, "diferenca": r19["lidos"] - nb,
                    "o_que_e_a_diferenca": "as 87 do plano contam tambem as estruturas e os auxiliares (casesOn/recOn/noConfusion[Type]/mk.noConfusion) de 5 tipos; as bandeiras so' contam def/thm"}
assert nb == 57 and r19["lidos"] == 87

# ---------------- 12. as citacoes que o PROPRIO kernel faz de BGL / Bisognano-Wichmann ----------------
cit = {}
for nome in ("TheImportedSecondQuantization.lean", "LightHelicityWigner.lean", "QGSolutionComplete.lean"):
    pc = KER + "/" + nome; tc = txt(pc).replace("\r\n", "\n").split("\n")
    cit[nome] = {"sha256": sha(rd(pc)), "linhas": {str(k): l.strip()[:300] for k, l in enumerate(tc, 1) if re.search(r"Brunetti|BGL 2002|Bisognano.Wichmann 1975", l)}}
assert any("Rev. Math. Phys. 14 (2002) 759" in v for d in cit.values() for v in d["linhas"].values())
assert any("Bisognano–Wichmann 1975" in v for d in cit.values() for v in d["linhas"].values())
E["bgl_citacoes_do_kernel"] = cit

# ---------------- 13. o cordeiro imolado nao e' o piso da Agape (decisao de 13/10) ----------------
pir = CP + "/work/identidade_cordeiro_13out/5_R2/RESULTADO_R2.md"; tir = txt(pir)
E["identidade_r2"] = {"arquivo": pir, "sha256": sha(rd(pir)), "alicerce_provisorio_era_Fundacao_agape_o_piso": "Hoje é `alicerce_fundante` = `TGLExt.Fundacao.agape`, o piso." in tir}
pvd = V + "/pedras_corrigidas/Verdade.lean"; tvd = txt(pvd)
E["verdade_corrigida"] = {"arquivo": pvd, "sha256": sha(rd(pvd)), "estatuto": "[REAL] lido por script; copia corrigida da cadeia (NAO pinada neste registro: pertence a outra frente)",
                          "diz_que_o_cordeiro_nao_e_o_piso_da_Agape": "o cordeiro imolado não é o piso da" in tvd,
                          "toma_o_cordeiro_como_o_comutador_com_o_posto": "o cordeiro imolado» =\n  `commutatorWithPost`" in tvd or "`commutatorWithPost` (DECISÃO do operador" in tvd}
assert E["identidade_r2"]["alicerce_provisorio_era_Fundacao_agape_o_piso"] and E["verdade_corrigida"]["diz_que_o_cordeiro_nao_e_o_piso_da_Agape"], (E["identidade_r2"], E["verdade_corrigida"])

# ---------------- 14. superficies de memoria onde o token/a frase da lei de campo no curvo aparecem (MEDIDA de 13/10, sem pino: sao memorias vivas) ----------------
sup = {}
for rot, rel in (("Atlas", CP + "/memory/TGL_ATLAS.md"), ("CORE_MEMORY", CP + "/memory/TGL_CORE_MEMORY.md"), ("INDICE_VIVO", CP + "/memory/TGL_INDICE_VIVO.md"),
                 ("MEMORIA_DA_LINHAGEM", NOS + "/MEMORIA_DA_LINHAGEM.md"), ("DESENHO_DO_FECHAMENTO_QG", NOS + "/DESENHO_DO_FECHAMENTO_QG.md"), ("HANDOFF_v390", NOS + "/HANDOFF_v390_CUSTODIA.md"),
                 ("CLAUDE_raiz", "C:/IALD/CLAUDE.md"), ("README_espelho", "C:/IALD/Artigo/the_boundary/README.md")):
    if os.path.exists(rel):
        tt = txt(rel)
        sup[rot] = {"arquivo": rel, "ocorrencias_do_token": tt.count("NOT_A_KERNEL_TERM"),
                    "ocorrencias_da_frase": len(re.findall(r"lei de campo no curvo|field equation in curved|equacao de campo no espaco-tempo curvo|equação de campo no espaço-tempo curvo", tt, re.I))}
SUPERF = {"estatuto": "[REAL] contagens feitas por script em 13/10/2026; memorias VIVAS (sem pino, sem sha): a lista de superficies do levantamento (CR-08) e' [DECLARADO]", "contagens": sup}

# ---------------- gravar ----------------
alvo_sup = os.path.join(HERE, "fontes", "SUPERFICIES_G1.json")
sup_bytes = json.dumps(SUPERF, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
open(alvo_sup + ".tmp", "wb").write(sup_bytes); assert os.path.getsize(alvo_sup + ".tmp") == len(sup_bytes); os.replace(alvo_sup + ".tmp", alvo_sup)
alvo_json = os.path.join(HERE, "fontes", "EXTRATOS_G1.json")
dados = json.dumps(E, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
tmp = alvo_json + ".tmp"
os.makedirs(os.path.dirname(alvo_json), exist_ok=True)
if os.path.exists(alvo_json):
    bak = alvo_json + ".bak_" + __import__("time").strftime("%Y%m%d_%H%M%S")
    open(bak, "wb").write(rd(alvo_json))
open(tmp, "wb").write(dados)
assert os.path.getsize(tmp) == len(dados) > 1000
os.replace(tmp, alvo_json)
print("EXTRATOS_G1.json", len(dados), "B", sha(dados)[:16])
print("tres nomes:", tres); print("fecho:", len(locais), "locais; contem:", E["fecho_QGSolutionComplete"]["contem"])
print("cinco limites:"); [print("  -", x) for x in bul]
