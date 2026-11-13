# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-M-v411] REESCRITO para o texto curto novo (H0DN x BG1 aberto): roda o script INTEIRO (linha de comando) sobre um Nos SINTETICO com o registro offline TESTE_H0DN_OFFLINE_v411_registro.json no lugar de core["h0dn_bg1_v411"], e controles negativos (sem a linha das Cefeidas livres e as outras obrigacoes: a guarda_frases_v411 TEM de reprovar)
"""teste_x_custodia_sem_candidato_v411.py -- (claude-sonnet-posrito-M-v411, 12/11/2026) o teste POSSIVEL SEM CANDIDATO do rascunho do texto curto do X da v411 (gerar_x_custodia_v411.py):
roda o script INTEIRO, por linha de comando, sobre um Nos SINTETICO (selo e core minimos; o registro h0dn_bg1_v411 e' o substituto offline TESTE_H0DN_OFFLINE_v411_registro.json; os registros anteriores e os dois por spec sao sinteticos so' em all_verified)
e um ESPERADOS sintetico, numa pasta temporaria passada por argumento; o rascunho vai para essa pasta (nunca para pos_rito). Confere: rc 0; o texto passa nas guardas (P18, frases v411 com a F67, 4,44, D59, D65, tokens); traz os DOIS numeros
(o primario contra o nulo e as Cefeidas livres, PT e EN), sob o modelo de erros publicado / under the published error model, retrodicao e nao cego, validade nao creditacao; nao traz a cabeca do teste; e CONTROLES NEGATIVOS: sem a linha das Cefeidas livres,
sem o modelo publicado, sem a validade, sem a retrodicao, sem o nao cego, a palavra da creditacao, o teste dito cego, o poder certificado, a descoberta, a evidencia independente, 5 sigma atingido, o 4,44, o que a D65 deixa fora, o token proibido,
um paragrafo que cita o primario sozinho: cada um TEM de ser reprovado por conferir(). montar_post() tambem recusa (AssertionError) o selo de outra versao, o registro que nao selou, a escada diferente, o veredito diferente de ESPERADOS. rc 0 = passou.
uso: python -B -X utf8 teste_x_custodia_sem_candidato_v411.py <pasta_temporaria>"""
import copy, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PKG)
sys.stdout.reconfigure(encoding="utf-8")
assert len(sys.argv) > 1, "uso: teste_x_custodia_sem_candidato_v411.py <pasta_temporaria> (a saida nunca vai para a pasta da cadeia)"
TMP = os.path.abspath(sys.argv[1]); NOS = os.path.join(TMP, "Nos"); os.makedirs(NOS, exist_ok=True)
assert not os.path.normcase(TMP).startswith(os.path.normcase(PKG)), "a saida do teste nao pode ir para a pasta da cadeia"
import delta_v411 as DL  # noqa: E402
import consts_mapa_x_v411 as C  # noqa: E402
import gerar_x_custodia_v411 as G  # noqa: E402
OK = [True]


def check(nome, cond, extra=""):
    print("  %-100s %s%s" % (nome, "ok" if cond else "FALHOU", (" -- " + str(extra)) if extra else ""))
    if not cond:
        OK[0] = False
    return bool(cond)


def levanta(fn):
    try:
        fn()
    except AssertionError:
        return True
    except Exception as ex:  # noqa: BLE001
        print("     (levantou %s em vez de AssertionError: %s)" % (type(ex).__name__, str(ex)[:160]))
        return False
    return False


PIN64 = "0123456789abcdef" * 4
HD = json.load(open(os.path.join(PKG, "TESTE_H0DN_OFFLINE_v411_registro.json"), encoding="utf-8"))
F = C.fatos_h0dn(HD)
BC = json.load(open(os.path.join(PKG, "base_v410", "um_absoluto.json"), encoding="utf-8"))["core"]
ESC = BC["external_ladder"]["n_theorems_expected"]; GATE = BC["qg_closure"]["gate"]["verdict"]
N_DECL = 34300   # (contagem SINTETICA do relatorio de axiomas: so' o formato do numero; o real sai do core)


def core_sint(f_=None):
    c_ = {DL.FECHO_REGISTRO: copy.deepcopy(HD), DL.CUNHAGENS_REGISTRO: {"all_verified": True}, DL.KH_REGISTRO: {"all_verified": True}, "external_ladder": {"n_theorems_clean": ESC, "n_theorems_expected": ESC},
          "kernel_formalization": {"axiom_report": [0] * N_DECL}}
    for k_ in DL.REGISTROS_FUNCAO_V410:
        c_[k_] = {"all_verified": True}
    if f_:
        f_(c_)
    return c_


SELO = {"um_version": "v411", "sha256": {"um.py": PIN64}, "qg_closure_verdict": GATE}
ESP = {"candidato_sha16": PIN64[:16], "escada_v410_e_v411": [ESC, ESC], "vereditos_novos_v411": {DL.FECHO_REGISTRO: HD["verdict"]}}
json.dump({"core": core_sint()}, open(os.path.join(NOS, "um_absoluto.json"), "w", encoding="utf-8"))
json.dump(SELO, open(os.path.join(NOS, "um_absoluto_selo.json"), "w", encoding="utf-8"))
ESP_P = os.path.join(TMP, "ESPERADOS_v411.json"); json.dump(ESP, open(ESP_P, "w", encoding="utf-8"))
OUT = os.path.join(TMP, "CUSTODIA_v411_RASCUNHO.txt")
if os.path.exists(OUT):
    os.remove(OUT)

print("== (1) o script INTEIRO, por linha de comando, sobre o Nos sintetico")
r_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "gerar_x_custodia_v411.py"), "--nos", NOS, "--esp", ESP_P, "--saida", OUT], capture_output=True, text=True, encoding="utf-8")
check("rc 0 e o rascunho gravado na pasta temporaria (nunca em pos_rito)", r_.returncode == 0 and os.path.isfile(OUT), (r_.stdout + r_.stderr)[-300:])
check("o rascunho foi para a pasta temporaria, nao para pos_rito", os.path.normcase(os.path.dirname(OUT)) != os.path.normcase(HERE))
txt = open(OUT, encoding="utf-8").read()
print("     post: %d B, %d caracteres, %d linhas (texto curto; NAO publicado)" % (len(txt.encode("utf-8")), len(txt), txt.count("\n")))
pr = G.conferir(txt)
check("conferir(): P18, guarda de frases da v411 (F60 a F67), 4,44, D59, D65 e tokens passam", not pr, pr[:3])
check("os DOIS numeros no texto, PT: o primario %s contra o nulo e %s contra K; as Cefeidas livres %s" % (F["zn_pt"], F["zk_pt"], F["cn_pt"]), all(x_ in txt for x_ in (F["zn_pt"], F["zk_pt"], F["cn_pt"])))
check("os DOIS numeros no texto, EN: %s / %s" % (F["zn_en"], F["cn_en"]), all(x_ in txt for x_ in (F["zn_en"], F["cn_en"])))
check("sob o modelo de erros publicado / under the published error model", DL.OBRIG_MODELO_PT in txt and DL.OBRIG_MODELO_EN in txt)
check("retrodicao e nao cego / retrodiction and not blind", all(x_ in txt for x_ in (DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT, DL.OBRIG_RETRO_EN, DL.OBRIG_NAO_CEGO_EN)))
check("validade, nao creditacao / validity, not creditation", DL.OBRIG_VALIDADE_PT in txt and DL.OBRIG_VALIDADE_EN in txt)
check("as Cefeidas livres / the free Cepheids com o numero, PT e EN, no mesmo trecho do primario", DL.OBRIG_CEFEIDAS_PT in txt and DL.OBRIG_CEFEIDAS_EN in txt and C.moldura_pt(F) in txt and C.moldura_en(F) in txt)
check("a moldura vem do delta (a frase da gerencia) e os numeros do core, nao digitados", txt.count(F["zn_pt"]) >= 1 and F["atos"]["commit_do_pre_registro"][:12] in txt and F["atos"]["commit_do_resultado"][:12] in txt)
check("o alcance de P = nP (D64): relativo ao leitor; a maquina de Turing padrao sem o leitor fica fora", DL.D10.FRASE_QUALIFICADOR_PT in txt)
check("o sha256 do programa e o da escada vem do selo e do core", PIN64 in txt and ("%d/%d" % (ESC, ESC)) in txt)
check("nao traz a cabeca do teste (o campo cabeca_do_teste fica no registro) nem token de veredito", not any(x_ in txt for x_ in ("BETA_TGL_PRO", "PROVED_IN_" + "NATURE", "BETA_TGL_" + "PROVED")) and not any(t_ in txt for t_ in DL.TOKENS_PROIBIDOS_V411))
check("nao diz 'confirmada' nem a palavra da creditacao afirmada; diz que a creditacao e' de quem observa de fora (ou nao a afirma)", not any(v_[0].startswith("F60") for v_ in G.conferir(txt)) and "creditação" in txt)
check("e' texto CURTO: abaixo de 4.500 bytes (a v410 tinha mais de 8.000)", len(txt.encode("utf-8")) < 4500)

print("== (2) controles negativos de texto: cada um TEM de ser reprovado por conferir()")
mod_pt = C.moldura_pt(F); cef_pt = "as %s leem %s (ramo %d); " % (DL.OBRIG_CEFEIDAS_PT, F["cn_pt"], F["ramo_c"]); cef_en = "the %s read %s (branch %d); " % (DL.OBRIG_CEFEIDAS_EN, F["cn_en"], F["ramo_c"])
assert mod_pt in txt and cef_pt in mod_pt and cef_en in C.moldura_en(F)
NEG = {"SEM a linha das Cefeidas livres (so' na moldura PT)": (txt.replace(mod_pt, mod_pt.replace(cef_pt, "")), "F67", "cefeidas_livres_com_o_numero"),
       "SEM a linha das Cefeidas livres (em todo o texto PT)": (txt.replace(cef_pt, "").replace("%s; as %s leem %s (ramo %d); " % (DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, F["cn_pt"], F["ramo_c"]), DL.OBRIG_MODELO_PT + "; "), "F67", "cefeidas_livres_com_o_numero"),
       "SEM as free Cepheids (so' na moldura EN)": (txt.replace(C.moldura_en(F), C.moldura_en(F).replace(cef_en, "")), "F67", "cefeidas_livres_com_o_numero"),
       "SEM sob o modelo de erros publicado": (txt.replace(DL.OBRIG_MODELO_PT, "XXXX"), "F67", "modelo_publicado"), "SEM under the published error model": (txt.replace(DL.OBRIG_MODELO_EN, "XXXX"), "F67", "modelo_publicado"),
       "SEM validade, nao creditacao": (txt.replace(DL.OBRIG_VALIDADE_PT, "XXXX"), "F67", "validade_nao_creditacao"), "SEM validity, not creditation": (txt.replace(DL.OBRIG_VALIDADE_EN, "XXXX"), "F67", "validade_nao_creditacao"),
       "SEM retrodicao": (txt.replace(DL.OBRIG_RETRO_PT, "XXXX"), "F67", "retrodicao"), "SEM retrodiction": (txt.replace(DL.OBRIG_RETRO_EN, "XXXX"), "F67", "retrodicao"),
       "SEM nao cego": (txt.replace(DL.OBRIG_NAO_CEGO_PT, "XXXX"), "F67", "nao_cego"), "SEM not blind": (txt.replace(DL.OBRIG_NAO_CEGO_EN, "XXXX"), "F67", "nao_cego"),
       "um paragrafo que cita o primario SOZINHO": (txt + "\nNo H0DN o primário fica a %s contra o nulo.\n" % F["zn_pt"], "F67", None),
       "a palavra da creditacao afirmada": (txt + "\nA TGL foi " + "CONF" + "IRMED" + " pela natureza.\n", "F60", None), "o teste dito cego": (txt + "\nFoi um teste cego.\n", "F63", None), "o poder certificado": (txt + "\nO teste tem poder certificado.\n", "F61", None),
       "a descoberta": (txt + "\nA descoberta do H0DN a 6 sigma.\n", "F65", None), "evidencia independente sem a negacao": (txt + "\nÉ evidência independente das Fases 4, 5 e 9.\n", "F64", None), "o vetor fora do suporte como erro de montagem": (txt + "\nO vetor fora do suporte é erro de montagem.\n", "F62", None),
       "o beta literal": (txt + "\nCom beta = 0,0120313.\n", "F66", None), "5 sigma atingido": (txt + "\n5 sigma atingido no H0DN.\n", "F53", None), "a covariancia fisica fechada": (txt + "\nA covariância física está fechada.\n", "F56", None)}
for nome_, (t_, regra_, falta_) in NEG.items():
    regras_ = [x_[1][0] for x_ in G.conferir(t_) if x_[0] == "guarda_frases_v411"]   # (as violacoes da guarda de frases: (regra, trecho))
    ach_ = [r_ for r_ in regras_ if r_.startswith(regra_)]
    check("controle negativo: %-58s" % nome_, bool(ach_) and (falta_ is None or any(falta_ in r_ for r_ in ach_)), ach_[:1])
for nome_, t_, tag_ in (("o 4,44 no post", txt + "\nz_disc = 4,44.\n", "regra_da_ordem"), ("o que a D65 deixa fora", txt + "\n" + DL.FORA_D65[0] + "\n", "D65"), ("o nome do Kimi fora do H0DN", "A ordem ao Kimi para outra coisa.\n", "D59"), ("o Milenio", txt + "\nproblema do Milênio\n", "D59"),
                         ("token proibido", txt + "\n" + DL.TOKENS_PROIBIDOS_V411[0] + "\n", "token_proibido"), ("a cabeca do teste por extenso (a P18 a recusa)",txt + "\n" + F["cabeca"] + "\n", "P18")):
    check("controle negativo: %-58s" % nome_, any(x_[0] == tag_ for x_ in G.conferir(t_)))
check("a forma certa passa: o paragrafo do primario COM as obrigacoes", not G.conferir(txt + "\n" + C.cap(C.moldura_pt(F)) + ".\n"))

print("== (3) montar_post() recusa (AssertionError) o que nao confere; a linha de comando recusa o selo da v410")
NEG_P = {"o selo e' de outra versao": lambda: G.montar_post(core_sint(), dict(SELO, um_version="v410"), ESP, "12/11/2026"), "o um.py do selo nao e' o candidato": lambda: G.montar_post(core_sint(), dict(SELO, sha256={"um.py": "f" * 64}), ESP, "12/11/2026"),
         "o registro h0dn_bg1_v411 nao selou": lambda: G.montar_post(core_sint(lambda c: c[DL.FECHO_REGISTRO].update(all_verified=False)), SELO, ESP, "12/11/2026"),
         "o registro h0dn_bg1_v411 sem a linha das Cefeidas livres": lambda: G.montar_post(core_sint(lambda c: c[DL.FECHO_REGISTRO].pop("linha_ao_lado_cefeidas_livres")), SELO, ESP, "12/11/2026"),
         "o veredito do registro != ESPERADOS": lambda: G.montar_post(core_sint(), SELO, dict(ESP, vereditos_novos_v411={DL.FECHO_REGISTRO: "OUTRO"}), "12/11/2026"),
         "um registro da v410 (recriado) nao selou": lambda: G.montar_post(core_sint(lambda c: c.update(iald2_v410={"all_verified": False})), SELO, ESP, "12/11/2026"),
         "o cunhagens_v411 nao selou": lambda: G.montar_post(core_sint(lambda c: c[DL.CUNHAGENS_REGISTRO].update(all_verified=False)), SELO, ESP, "12/11/2026"),
         "a escada difere da v410": lambda: G.montar_post(core_sint(lambda c: c["external_ladder"].update(n_theorems_clean=ESC - 1)), SELO, ESP, "12/11/2026"),
         "o gate lido pelo registro != o do selo": lambda: G.montar_post(core_sint(), dict(SELO, qg_closure_verdict="OUTRO"), ESP, "12/11/2026"),
         "o relatorio de axiomas vazio": lambda: G.montar_post(core_sint(lambda c: c["kernel_formalization"].update(axiom_report=[])), SELO, ESP, "12/11/2026")}
for k_, f_ in NEG_P.items():
    check("montar_post() recusa: %s" % k_, levanta(f_))
json.dump(dict(SELO, um_version="v410"), open(os.path.join(NOS, "um_absoluto_selo.json"), "w", encoding="utf-8"))
r2_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "gerar_x_custodia_v411.py"), "--nos", NOS, "--esp", ESP_P, "--saida", os.path.join(TMP, "NAO_DEVE_EXISTIR.txt")], capture_output=True, text=True, encoding="utf-8")
check("a linha de comando RECUSA (rc 2) quando o selo do Nos e' o da v410, e nao grava nada", r2_.returncode == 2 and "RECUSO" in r2_.stdout and not os.path.exists(os.path.join(TMP, "NAO_DEVE_EXISTIR.txt")))
print("RESULTADO:", "PASSOU" if OK[0] else "REPROVOU")
sys.exit(0 if OK[0] else 1)
