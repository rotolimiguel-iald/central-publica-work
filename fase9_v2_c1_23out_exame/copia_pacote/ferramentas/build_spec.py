# -*- coding: utf-8 -*-
"""Constroi spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json a partir da R5.2-E1 (sha256 81a970926345832a...), aplicando as DECISOES DO OPERADOR de 23/10/2026 e as ordens da
gerencia c1 (E1-E5, S5, calibracao de cauda, trava), e gera o DIFF com CADA mudanca atribuida (o build FALHA se uma secao mudou sem atribuicao).
Rodar:  python -P -E -X utf8 ferramentas/build_spec.py   (apos build_funcao.py e build_registro_dh.py)."""
import copy
import difflib
import hashlib
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
sys.path.insert(0, os.path.join(ROOT, "testes"))
import f9v2_stats as ST  # noqa: E402
import f9v2_verdict as VER  # noqa: E402
import verdict_fixtures as FX  # noqa: E402

R52 = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"
OP = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_fase9_decisoes_unica_palavra_verbatim.txt"
sha = lambda b: hashlib.sha256(b).hexdigest()


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


raw52 = open(R52, "rb").read()
assert sha(raw52).startswith("81a970926345832a"), "R5.2-E1 mudou"
old_wrap = json.loads(raw52.decode("utf-8"))
old = old_wrap["spec"]
new = copy.deepcopy(old)
opb = open(OP, "rb").read()
op_sha = sha(opb)

# ---------------------------------------------------------------- tags
OPA, OPB, OPC, OPD = "OP-a ALCANCE", "OP-b X13", "OP-c D-H", "OP-d D-J"
E1, E2, E3, E4, E5 = "C1-E1 fornecedor real do fundo", "C1-E2 reproducao do fundo", "C1-E3 quadraturas 100/200", "C1-E4 registro D-H pinado", "C1-E5 modo observado"
S5, CAL, TRAVA, ID = "C1-S5 fundo propagado", "C1-CAL calibracao de cauda", "C1-TRAVA recibo de congelamento", "C1-ID versao/estado"
ATTR = {}   # secao -> [(tag, resumo)]


def attr(section, tag, resumo):
    ATTR.setdefault(section, []).append((tag, resumo))


# ---------------------------------------------------------------- (a) ALCANCE
new["alcance"] = {
    "nome_do_teste": "O Teste da Unica Palavra",
    "a_unica_palavra": "beta_TGL: a lei K = E(z*)^(2 beta_TGL/3) e' a voz UNICA de beta_TGL na expansao",
    "FALSIFIED_AT_5SIGMA": "beta_TGL refutado na natureza (o unico elo pendente do estatuto da prova v391), SEM saida posterior por outra lei, convencao ou conjunto",
    "nao_esta_em_jogo": ["a validade do kernel (a prova como fecho logico)", "o gate (cosmologia nao move matematica)", "a RG como limite classico"],
    "devido_processo": "o pre-registro e' o DEVIDO PROCESSO (a lei anterior a lei), nao a coisa julgada",
    "NOT_FALSIFIED": "NOT_FALSIFIED nunca e' CONFIRMED; DISCRIMINATES e' escore e evidencia, nao confirmacao (confirmar/creditar e' ato do observador humano)",
    "leitura_anterior_superada": "o V1 escrevia que FALSIFIED_AT_5SIGMA falsifica o PAR (lei D1b, convencao, conjunto), nao beta, nao a teoria; o operador decidiu o contrario em 23/10/2026",
    "fonte_do_operador": {"path": OP, "sha256": op_sha, "bytes": len(opb),
                          "trechos": ["a única palavra que o Nome pronuncia é Betatgl", "o devido processo legal ... não a coisa julgada, o due process of law é a LEI anterior à LEI",
                                      "de resto concordo com tudo", "observar é nomear"]},
    "leitura_da_gerencia": "os itens (a)-(d) sao a proposta da gerencia c1 que o operador aceitou («de resto concordo com tudo»); a frase sobre a unica palavra e sobre o devido processo e' do operador, verbatim",
    "estatuto": "[INPUT] decisao do operador, 23/10/2026",
}
attr("alcance", OPA, "secao nova: FALSIFIED_AT_5SIGMA = beta_TGL refutado na natureza, voz unica, sem saida posterior; validade do kernel fora de jogo; pre-registro = devido processo")
new["nao_decide"] = [
    "o gate (18 bandeiras, funcao so do formal)",
    "a implicacao da QG e a correspondencia com a RG",
    "a derivacao de beta a partir do axioma (a regra matriz) e a validade do kernel (a prova como fecho logico)",
    "qual fundo e o da natureza (aqui so o primario do registro)",
    "o mecanismo [CONJECTURE]",
    "a dependencia em z de K (<= 0,9 % em z = 2, abaixo do poder)",
    "a creditacao (a confirmacao): ato do observador humano",
]
attr("nao_decide", OPA, "'beta (a regra matriz)' vira 'a derivacao de beta ... e a validade do kernel' (o teste decide beta na natureza, nao a derivacao); saem D-H e NAT22/X13 (decididos); entra a creditacao")

# ---------------------------------------------------------------- (b) X13
new.pop("estatisticas_executor_observado_sujeito_NAT22")
new["estatisticas_do_executor"] = {
    "X13": "SIM (operador, 23/10/2026): este texto descreve o que o executor faz",
    "fundo": "marginalizado: y ~ N(P f, C + V f f') com V = variancia da previsao local; com S5, V propaga H0, Omega_m e Omega_r do fundo BG1; sem S5, V = (K sigma_bg)^2",
    "z_delta": "(beta_hat - beta_TGL)/sigma_beta pelo PERFIL de ln L, que INCLUI o log-det de S; beta em U[-0,05; 0,05]; sigma_beta = media dos dois lados (ambos obrigatorios; sem os dois => beta_livre_no_limite => INCONCLUSIVE)",
    "z_disc": "forma quadratica: sinal * sqrt|chi2_LCDM - chi2_TGL| (4,2837 no V1); a variante com log-det (4,2818 no V1) vai ao lado, diagnostico",
    "lnB": "quatro comparacoes (LCDM; beta-livre U[-0,05; 0,05]; shift das Cefeidas SH0ES U[-0,15; 0,15]; fundo-livre r_d U[130; 160] Mpc); beta-livre e shift por quadratura de Gauss-Legendre n = 100 (decisorio) conferida com n = 200; fundo-livre = Laplace do V1 + massa do prior por GL 100/200",
    "tolerancia_da_quadratura": "|ln Z(n=100) - ln Z(n=200)| > 1e-6 em qualquer uma => RECUSA (QuadratureUnstable), sem veredito",
    "lnB_TGL_vs_beta_livre_do_V1": "1,97 (n >= 100 converge), nao 2,24 (n = 25; erro 0,30): errata auditada; nao e' composto novo",
    "dispersao": "chi2_int/(n-1) e p (n_local > 1) com a covariancia do ponto, SEM o fundo, nos DOIS extremos; chi2/(n-1) > 2 ou p < 0,01 em qualquer um => INCONCLUSIVE_SYSTEMATICS",
    "extremos": "falsificacao e tensao: ponto de MENOR sigma_comb; poder e discriminacao: ponto de MAIOR sigma_comb; beta_livre_no_limite vale se QUALQUER extremo tiver beta_hat na borda ou perfil sem os dois lados",
    "z_calibrado": "z_delta e z_disc entram na funcao como o z EQUIVALENTE de um p CALIBRADO (secao calibracao_de_cauda); os escores brutos vao ao lado no resultado",
    "estatuto": "[INPUT] X13 = SIM (operador, 23/10/2026); [DERIVED] a descricao e' a do codigo em runner/f9v2_stats.py",
}
attr("estatisticas_executor_observado_sujeito_NAT22", OPB, "removida (NAT22 pendente -> decidido)")
attr("estatisticas_do_executor", OPB, "secao nova: o texto da V2 descreve o que o executor faz (fundo marginalizado; z_delta pelo perfil com log-det; ln B com n >= 100; ln B(TGL/beta-livre) = 1,97)")
attr("estatisticas_do_executor", CAL, "linha 'z_calibrado': a funcao le o z equivalente do p calibrado")
new["estatisticas"]["background"] = "marginalized by the observed executor (X13 = SIM); S5 propagates H0, Omega_m, Omega_r"
attr("estatisticas", OPB, "background: 'NAT22 pending' -> marginalizado pelo executor (X13 = SIM)")

# ---------------------------------------------------------------- (c) D-H
new["registro_dh"] = {"path": "spec/REGISTRO_DH_V2_C1.json", "sha256": None, "papel": "registro D-H do operador (23/10/2026): fontes pinadas por sha256 + regras de extracao + L1b e L6 baixados"}
reg_bytes = open(os.path.join(ROOT, "spec", "REGISTRO_DH_V2_C1.json"), "rb").read()
new["registro_dh"]["sha256"] = sha(reg_bytes)
new["registro_dh"]["bytes"] = len(reg_bytes)
attr("registro_dh", OPC, "secao nova: aponta o registro D-H pinado (8 leitores, sha256, regra de extracao testada contra os bytes; L1b e L6 baixados em 23/10)")
reg = json.loads(reg_bytes.decode("utf-8"))
for rid, r in new["leitores"].items():
    rr = reg["leitores"][rid]
    r["documentary_gate_status"] = "REAL_DOCUMENTARY_HASH_ONLY"
    r["documentary_source"] = {"path": rr["file"], "sha256": rr["sha256"]}
    r["source_admission"] = "ADMITTED_BY_OPERATOR_D_H_23OUT2026"
    r["estatuto_hoje"] = "[REAL documental por hash no registro D-H; admissao D-H do operador de 23/10/2026]"
    if rid in ("L4_masers_5", "L4_masers_6"):
        r["source_path"] = rr["file"]
        r["source_sha256"] = rr["sha256"]
    if "status" in r and rid == "L4_masers_5":
        r["status"] = "REAL_DOCUMENTARY_ADMITTED_D_H"
attr("leitores", OPC, "os 8 leitores: source_admission PENDING_D_H -> ADMITTED_BY_OPERATOR_D_H_23OUT2026; L1b e L6 passam de DECLARADO_UNVERIFIED a REAL_DOCUMENTARY_HASH_ONLY; caminhos viram relativos ao pacote (copias dos bytes, hashes identicos)")
new["source_admission"] = {
    "status": "D_H_ADMITTED_23OUT2026", "registro": "spec/REGISTRO_DH_V2_C1.json",
    "L4_new_source": "Pesce PDF pinned; extraction rule requires Table 2 fiducial (1) row and both asymmetric sides on page 6",
    "SBF_section_III_3": "DECLARADO_WEB_NO_LOCAL_INTEGRAL_BYTES", "TDCOSMO_section_VIII_2_1": "DECLARADO_WEB_NO_LOCAL_INTEGRAL_BYTES",
    "freezing_guard": "RECIBO_DE_CONGELAMENTO da gerencia (pina spec, funcao, runner, registro D-H, fontes, calibracao); X13 e D-H pinados; auditoria c1 do runner",
    "opening_guard": "RECIBO_DE_ABERTURA (ato proprio) referido ao hash do recibo de congelamento; ALVOS_FASE9_LIDOS.json montado a mao => RECUSA",
}
attr("source_admission", OPC, "PENDING -> ADMITTED; as travas passam a ser os dois recibos")
new["freeze_preflight"] = {
    "current": "X13 e D-H SATISFEITOS (23/10/2026); AGUARDA auditoria c1 do runner e RECIBO_DE_CONGELAMENTO",
    "substitui": "a guarda documental preflight_congelamento_f31_r5_1 (que devolvia flags) pela trava executavel runner/f9v2_freeze.py",
    "status": "TRAVA_EXECUTAVEL_TESTADA_SO_SINTETICO",
}
attr("freeze_preflight", OPB, "X13 satisfeito")
attr("freeze_preflight", OPC, "D-H satisfeito")
attr("freeze_preflight", TRAVA, "a guarda documental vira a trava executavel (recibo de congelamento + recibo de abertura)")
new["pending_operator_decisions"] = [
    "RECIBO DE CONGELAMENTO (gerencia) depois da auditoria c1 do runner e da conferencia do PEDIDO_DE_CONGELAMENTO",
    "RECIBO DE ABERTURA (ato proprio; F3.3) — a palavra 'abrir' so depois de congelar e auditar",
    "d72: qualificacao da testemunha conjunta ROOT90da (outra testemunha; nao soma, nao empresta poder)",
]
attr("pending_operator_decisions", OPB, "X13 sai da lista (decidido)")
attr("pending_operator_decisions", OPC, "D-H sai da lista (decidido)")
attr("pending_operator_decisions", OPD, "D-J sai da lista (decidido)")
attr("pending_operator_decisions", TRAVA, "entram os dois recibos")
dp = new["decisoes_padrao_da_gerencia"]
dp["D-H"] = "ADMITIDOS pelo operador em 23/10/2026: os cinco leitores + masers_5 (PDF); L1b (arXiv:2509.01667) e L6 (sirenes LVK O4a) baixados e pinados por sha256; papeis tipados mantidos"
dp["D-J"] = "DECIDIDO (operador, 23/10/2026): token TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL + sufixo da ordem da funcao de veredito"
dp["NAT22_X13"] = "DECIDIDO (operador, 23/10/2026): SIM, o texto descreve o que o executor faz"
attr("decisoes_padrao_da_gerencia", OPC, "D-H: pendente -> admitido")
attr("decisoes_padrao_da_gerencia", OPD, "D-J: pendente -> decidido")
attr("decisoes_padrao_da_gerencia", OPB, "NAT22_X13: pendente -> decidido")

# ---------------------------------------------------------------- (d) D-J + funcao
new.pop("token_base_provisorio")
new.pop("token_estado")
new["token"] = {
    "base": VER.TOKEN_BASE,
    "formato": "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL__<CLASSE>[__<detalhes>]__D1B__FUNDO_<BG>__NOT_BLIND_TO_DATA_STATED__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
    "ordem_do_sufixo": ["INCONCLUSIVE_SYSTEMATICS", "FALSIFIED_AT_5SIGMA", "TENSION_3_TO_5_SIGMA", "NOT_FALSIFIED_UNDERPOWERED", "DISCRIMINATION (NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_nSIGMA)", "NOT_FALSIFIED_POWERED"],
    "estado": "PREPARADO__AGUARDA_RECIBO_DE_CONGELAMENTO__GATE_UNTOUCHED",
    "estatuto": "[INPUT] D-J: a proposta da gerencia foi aceita de antemao pelo operador (23/10/2026); nome do teste: O Teste da Unica Palavra",
}
attr("token_base_provisorio", OPD, "removida")
attr("token_estado", OPD, "removida")
attr("token", OPD, "secao nova: token TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL + a ordem do sufixo")
fn_src = open(os.path.join(ROOT, "spec", "veredito_fase9_v2_c1.py"), "rb").read().decode("utf-8")
fn_sha = sha(fn_src.encode("utf-8"))
fv = new["funcao_de_veredito"]
fv["nome"] = VER.FUNCTION_NAME
fv["fonte"] = fn_src
fv["sha256"] = fn_sha
fv["estatuto"] = "FUNCAO_PINADA_V2_C1__AGUARDA_RECIBO_DE_CONGELAMENTO"
fv["final_token"] = VER.TOKEN_BASE
fv["se_abrir_hoje"] = {"cause": "nenhuma recusa de conteudo restante apos X13 e D-H; a abertura exige o RECIBO_DE_CONGELAMENTO e o RECIBO_DE_ABERTURA", "real_opening_permitted": False}
fv["n_alvos_declarados_rule"] = {"current_count": 0, "current_ids": [], "predicate": "NOT gate_verified AND NOT operator_admitted_in_pinned_D_H_register",
                                  "primary_result": "INCONCLUSIVE_SYSTEMATICS se algum leitor do inventario nao estiver verificado e admitido; hoje 0 (8 de 8 admitidos e verificados por sha256)",
                                  "same_in": ["preflight", "runner"], "universe": "whole V1.x inventory (8 leitores), not active family"}
fv["regra"] = "The runner executes THIS exact UTF-8 source after checking sha256 (spec e arquivo spec/veredito_fase9_v2_c1.py); no independently rewritten copy"
fv["entrada_calibrada"] = "z_delta e z_disc de entrada sao os z EQUIVALENTES de p calibrado (calibracao_de_cauda); o escore bruto nao e' o que a funcao le"
# testes de ramo regenerados com a funcao nova
fn_obj, _ = VER.load_pinned_verdict(fn_src, fn_sha)
branches = FX.run_branches(fn_obj)
for name, (r, expect) in FX.BRANCHES.items():
    assert expect in branches[name], (name, branches[name])
fv["testes_sinteticos_de_ramo"] = branches
numeric = {}
for name in FX.NUMERIC_GUARDS:
    try:
        numeric[name] = fn_obj(FX.numeric_case(name))
    except ValueError as e:
        numeric[name] = "ValueError:" + str(e)
    assert numeric[name].startswith("ValueError"), (name, numeric[name])
fv.pop("testes_sinteticos_r5_2")
fv["testes_sinteticos_numericos"] = numeric
attr("funcao_de_veredito", OPD, "nome, fonte e sha256 (3 trocas literais no texto: nome, docstring, base do token); final_token; testes de ramo regenerados")
attr("funcao_de_veredito", OPC, "n_alvos_declarados_rule: 2 (L1b, L6) -> 0; se_abrir_hoje")
attr("funcao_de_veredito", CAL, "entrada_calibrada: a funcao le z equivalente de p calibrado; logica e limiares NAO mudam")
fp = new["funcao_de_veredito_proposta"]
fp["final_token_name"] = VER.TOKEN_BASE
fp["status"] = "EXECUTAVEL_APOS_RECIBO_DE_CONGELAMENTO_E_RECIBO_DE_ABERTURA"
fp["n_alvos_declarados_rule"] = fv["n_alvos_declarados_rule"]
fp["n_alvos_declarados"] = fv["n_alvos_declarados_rule"]["predicate"] + " over whole V1.x inventory, not active family"
attr("funcao_de_veredito_proposta", OPD, "final_token_name e status")
attr("funcao_de_veredito_proposta", OPC, "n_alvos_declarados: 2 -> 0")

# ---------------------------------------------------------------- C1: S5, calibracao, trava, runner
q = json.load(open(os.path.join(ROOT, "testes", "QUALIFICACAO_FORNECEDOR_REAL.json"), encoding="utf-8"))
consts = {"og_coef": 4.4814e-7, "TCMB": 2.7255, "Neff": 3.046, "mnu_eV": 0.06}
lei = new["lei"]
lnE = ST.lnE_pinned(lei["Omega_m"], lei["Omega_r"], lei["z_star"])
beta = old["beta"]["alpha_read"] * math.sqrt(math.e)
law5 = ST.Law(beta, lei["K_frozen_V1"], lnE, q["fundo"]["bg1"]["H0"], q["fundo"]["bg1"]["cov_theta"], q["fundo"]["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"], consts, s5=True)
law0 = ST.Law(beta, lei["K_frozen_V1"], lnE, q["fundo"]["bg1"]["H0"], q["fundo"]["bg1"]["cov_theta"], q["fundo"]["bg1"]["theta_H0_ombh2_omch2"], lei["z_star"], consts, s5=False)
Kth, Eth, Omth, Orth = law5.K_at_theta()
new["S5_propagacao"] = {
    "habilitado": True,
    "regra": "a previsao local TGL e' P = K(theta) H0(theta), com theta = (H0, omega_b, omega_c) do fundo BG1 real; V = grad(P)' Cov(theta) grad(P) substitui (K sigma_bg)^2 na covariancia marginal. A media da previsao continua K_congelado * H0_BG1 (pre-registrada).",
    "constantes_E": {**consts, "origem": "um.py::_v378_lcdm_E (og = 4.4814e-7 T^4) e _V378_PLANCK; o runner confere com o um.py instalado e REGISTRA a divergencia (nao recusa)"},
    "gradiente": "diferencas centrais, passo relativo 1e-5, de ln E(z*; H0, omega_b, omega_c)",
    "efeito_medido_no_fundo_real_de_qualificacao": {
        "arquivo": "testes/QUALIFICACAO_FORNECEDOR_REAL.json", "V_T_S5": law5.V(beta), "V_T_ingenuo": law0.V(beta), "razao": law5.V(beta) / law0.V(beta),
        "grad_lnE": [float(v) for v in law5.gl], "Omega_m_no_theta_do_fundo": float(Omth), "Omega_r_no_theta_do_fundo": float(Orth),
        "K_no_theta_do_fundo": Kth, "K_congelado": lei["K_frozen_V1"], "delta_K_vezes_H0_km_s_Mpc": (Kth - lei["K_frozen_V1"]) * q["fundo"]["bg1"]["H0"]},
    "conclusao": "S5 FECHADA por propagacao: a variancia da previsao muda ~-2% e o deslocamento da media por Omega_m do proprio fundo (0,3011 contra 0,3023 pre-registrado) e' ~-0,001 km/s/Mpc; ambos despreziveis frente a sigma_comb 0,80-0,95. Os numeros estao ditos; nada e' ajustado.",
    "estatuto": "[DERIVED] c1; propagacao no runner, nao premissa",
}
attr("S5_propagacao", S5, "secao nova: propaga H0, Omega_m, Omega_r do fundo na covariancia marginal (S5 do levantamento)")
new["sistematicas"]["S5"] = "propagado (S5_propagacao); efeito medido ~ -2% em V e ~ -0,001 km/s/Mpc na media"
new["sistematicas"]["calibracao"] = "z_delta e z_disc calibrados por p sob a nula, com a sistematica da caixa de covariancia (calibracao_de_cauda)"
attr("sistematicas", S5, "entrada S5")
attr("sistematicas", CAL, "entrada calibracao")
new["calibracao_de_cauda"] = {
    "modo": "sup_caixa",
    "modos_possiveis": {"sup_caixa": "p = sup sobre a grade de covariancia (a caixa nao e' medida)", "proprio": "p com a covariancia do ponto de analise (sem a sistematica da caixa)", "bruto": "a funcao le o escore bruto (equivale a R5.2)"},
    "motivo": "o '5 sigma' tem de ser p calibrado, nao a raiz do qui-quadrado; o perfil com log-det e a forma quadratica de variancias diferentes nao sao lineares-gaussianos",
    "z_delta": "bilateral; nula = TGL verdadeira: u = m - K mu ~ N(0, tau_f^2), m = media GLS no ponto de MENOR sigma_comb; z_cal = Phi^{-1}(1 - p/2)",
    "z_disc": "unilateral; nula = LCDM verdadeira: x = m - mu ~ N(0, tau_d^2), m no ponto de MAIOR sigma_comb; z_cal = Phi^{-1}(1 - p)",
    "reducao_exata": "com o fundo marginalizado e f = 1, todas as hipoteses sem shift dependem de y so por m e por chi2_int; z_delta(u) e' deterministico; verificado contra o pipeline completo por simulacao",
    "recibo": "calibracao/CALIBRACAO_CAUDA_RECIBO.json",
    "guarda": "o runner reconstroi os limiares brutos equivalentes a 3 e 5 sigma com o fundo vivo e RECUSA se divergirem do recibo mais que runner_contract.tolerancias.recibo_calibracao_rel",
    "multiplicidade": "o veredito decisorio e' UM: P_primaria x BG1; replicas e diagnosticos (R_r25, N_sem_cefeidas, S_com_sirenes, T_so_cchp, M_seis_masers, BG2, BG3) nunca decidem",
    "estatuto": "[DERIVED] c1; decisao reversivel ate o congelamento (a gerencia pode escolher 'proprio' ou 'bruto' no PEDIDO_DE_CONGELAMENTO)",
}
attr("calibracao_de_cauda", CAL, "secao nova")
rc = new["runner_contract"]
new["runner_contract"] = {
    "fornecedor_do_fundo": "E1: BancadaBackgroundProvider (Planck comprimido Chen+2019 + DESI DR2, sem escada; o R2 do V1). kind=BANCADA_REAL exigido no pacote REAL; mock sintetico so em pacote SYNTHETIC_TEST_PACKAGE",
    "tolerancias": {"BG1_H0_abs": 0.01, "BG1_sigma_abs": 0.005, "poder_pino_abs": 0.002, "extracao_abs": 1e-9, "quadratura_ln_abs": ST.QUAD_TOL, "recibo_calibracao_rel": 0.01},
    "E2_reproducao": "|H0_BG1 - 68,531| < 0,01 (pino do V1) e |sigma - 0,301| < 0,005 (acrescimo c1); divergencia INTERROMPE, nunca calibra",
    "E3_quadraturas": "ln B por GL n = 100 (decisorio) e n = 200 (conferencia); |diferenca| > 1e-6 => RECUSA, sem veredito",
    "E4_registro_dh": "n_alvos_declarados e required_sources_admitted vem do registro D-H pinado (spec/REGISTRO_DH_V2_C1.json), sobre o inventario inteiro",
    "E5_ordem": ["recibos e pinos (bytes lidos uma vez)", "beta em runtime + K", "fundo BG1 real + E2", "PODER_FASE9_ANTES_DE_ABRIR.json (so sigma), gravado e hasheado", "centros extraidos das FONTES por regra pinada",
                 "estatistica + calibracao", "funcao pinada do texto", "resultado inteiro"],
    "centros_lacrados": "spec['leitores'][i]['H0'] e' removido da memoria antes do poder; so o cofre devolve, e so depois do poder gravado",
    "ALVOS_manual": "ALVOS_FASE9_LIDOS.json em qualquer lugar do pacote => RECUSA (REFUSE__MANUAL_TARGET_LEDGER)",
    "no_target_ledger_write": True, "read_source_bytes_once": True, "real_data_opened": False,
    "beta_em_runtime": "ALPHA_FINE_CODATA_2018 lido do um.py instalado (regex) x sqrt(e); confere com spec.beta.alpha_read (1e-15) e beta_runtime (1e-12); K recalculado confere com K congelado (1e-12)",
    "comando": "python -P -E -X utf8 runner/f9v2_runner.py --package-root <pacote> --mode observed",
}
new["especificacao_do_runner"] = [
    "R0 recibos: freeze/RECIBO_DE_CONGELAMENTO.json (gerencia) e freeze/RECIBO_DE_ABERTURA.json (ato proprio, referido ao hash do primeiro); sem eles, RECUSA antes de ler qualquer fonte",
    "R1 pinos: spec, funcao, registro D-H, modulos do runner (e nenhum .py a mais), fontes, recibo de calibracao e arquivos da Bancada, tudo lido UMA vez",
    "R2 E1/E2: fundo BG1 real recomputado; |H0-68,531|<0,01 e |sigma-0,301|<0,005 ou INTERROMPE",
    "R3 PODER_FASE9_ANTES_DE_ABRIR.json com so sigmas, gravado e hasheado antes de qualquer centro local",
    "R4 E5: centros extraidos das fontes pinadas pela regra do registro D-H e conferidos contra o declarado (1e-9)",
    "R5 cinco hipoteses, GLS/dispersao nos dois extremos, quatro lnB (GL 100/200), S5, calibracao de cauda",
    "R6 diagnosticos (R_r25, N_sem_cefeidas, S_com_sirenes, T_so_cchp, M_seis_masers, BG2, BG3) com a mesma funcao, ao lado, nunca somados",
    "R7 resultado inteiro (tambem abaixo de 5 sigma); escore, p calibrado, lnB, diagnosticos e limitacoes separados",
    "R8 mudancas posteriores ganham versao nova ao lado desta",
]
attr("runner_contract", E1, "fornecedor real do fundo BG1 (nao mock)")
attr("runner_contract", E2, "reproducao do fundo: H0 e sigma; diverge interrompe")
attr("runner_contract", E3, "tolerancia 1e-6 e recusa entre as quadraturas 100/200")
attr("runner_contract", E4, "n_alvos e fontes admitidas vem do registro D-H pinado")
attr("runner_contract", E5, "ordem PODER_ANTES_DE_ABRIR -> fonte lida uma vez -> funcao pinada; proibido ALVOS a mao")
attr("especificacao_do_runner", E5, "R0-R8 reescritos para o modo observado")
new["trava_de_congelamento"] = {
    "recibo_de_congelamento": "freeze/RECIBO_DE_CONGELAMENTO.json: schema F9V2C1_RECIBO_DE_CONGELAMENTO_V1, autohash, package_kind, atos {x13, D-H, auditoria c1}, pinos sha256 de spec/funcao/registro/runner/fontes/calibracao/Bancada",
    "recibo_de_abertura": "freeze/RECIBO_DE_ABERTURA.json: schema F9V2C1_RECIBO_DE_ABERTURA_V1, referido ao sha256 do recibo de congelamento, com o ato do operador",
    "recusas": ["REFUSE__FREEZE_RECEIPT_MISSING", "REFUSE__FREEZE_RECEIPT_INVALID", "REFUSE__FREEZE_ACT_MISSING", "REFUSE__PIN_MISMATCH", "REFUSE__SOURCE_ADULTERATED", "REFUSE__RUNNER_FILESET_DIFFERS",
                "REFUSE__OPENING_ACT_MISSING", "REFUSE__OPENING_ACT_INVALID", "REFUSE__MANUAL_TARGET_LEDGER", "REFUSE__CENTERS_BEFORE_POWER", "REFUSE__PROVIDER_NOT_REAL", "REFUSE__EXTRACTION_DIFFERS_FROM_DECLARED", "E2/E3 (BackgroundError, QuadratureUnstable)"],
    "emitente": "gerencia c1 (ferramentas/emitir_recibo_de_congelamento.py, NAO executada nesta preparacao)",
    "estatuto": "a trava nao e' autenticacao: e' o ato da gerencia + conferencia dos bytes",
}
attr("trava_de_congelamento", TRAVA, "secao nova")

# ---------------------------------------------------------------- C1-ID
new["estado"] = "PREPARADO_NAO_CONGELADO; congelamento exige o RECIBO_DE_CONGELAMENTO da gerencia depois da auditoria c1 do runner; abertura exige o RECIBO_DE_ABERTURA"
attr("estado", ID, "texto do estado")
new["state"] = "PREPARADO_NAO_CONGELADO"
attr("state", ID, "RASCUNHO_NAO_CONGELADO -> PREPARADO_NAO_CONGELADO")
new["id"] = "PREREG_FASE9_V2_C1_A_UNICA_PALAVRA_20261023"
attr("id", ID, "novo id")
new["supersede"] = {**old["supersede"], "R5_2_E1_LABELS_sha256": sha(raw52), "R5_2_spec_sha256": old_wrap["spec_sha256"], "V1_remains_frozen": True}
attr("supersede", ID, "aponta a R5.2-E1 como pai")
new["generated_from"] = {**old["generated_from"], "R5_2_E1_LABELS": {"path": R52, "sha256": sha(raw52), "bytes": len(raw52)},
                         "operador_23out": {"path": OP, "sha256": op_sha, "bytes": len(opb)}}
attr("generated_from", ID, "entram o pai (R5.2-E1) e a fala do operador de 23/10")

# ---------------------------------------------------------------- confere que TODA mudanca esta atribuida
changed = []
for k in sorted(set(old) | set(new)):
    if k not in old:
        changed.append((k, "nova"))
    elif k not in new:
        changed.append((k, "removida"))
    elif canon(old[k]) != canon(new[k]):
        changed.append((k, "alterada"))
missing = [k for k, _ in changed if k not in ATTR]
extra = [k for k in ATTR if k not in {c[0] for c in changed}]
assert not missing, ("secao mudou sem atribuicao", missing)
assert not extra, ("atribuicao sem mudanca", extra)

# ---------------------------------------------------------------- escreve a spec
spec_sha = sha(canon(new))
wrap = {"derived_from": {"bytes": len(raw52), "path": R52, "sha256": sha(raw52)}, "id": "PREREG_FASE9_V2_C1_A_UNICA_PALAVRA_20261023",
        "integration_note": "Fase 9 V2-c1 «O Teste da Unica Palavra»: a R5.2-E1 com as decisoes do operador de 23/10/2026 (alcance, X13, D-H, D-J) e as ordens da gerencia c1 (E1-E5, S5, calibracao, trava). "
                            "PREPARADA, NAO CONGELADA, NAO ABERTA. Nenhum composto observado foi calculado.",
        "spec": new, "spec_sha256": spec_sha, "state": "PREPARADO_NAO_CONGELADO"}
p = os.path.join(ROOT, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json")
b = json.dumps(wrap, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
open(p + ".tmp", "wb").write(b)
assert os.path.getsize(p + ".tmp") == len(b)
os.replace(p + ".tmp", p)
print("SPEC arquivo", sha(b)[:16], "canonico", spec_sha[:16], "funcao", fn_sha[:16], "registro", sha(reg_bytes)[:16])

# ---------------------------------------------------------------- DIFF (md + patch)
a_txt = json.dumps(old, ensure_ascii=False, indent=1, sort_keys=True).splitlines(keepends=True)
b_txt = json.dumps(new, ensure_ascii=False, indent=1, sort_keys=True).splitlines(keepends=True)
patch = "".join(difflib.unified_diff(a_txt, b_txt, "R5_2_E1_spec.json", "V2_C1_spec.json", n=1))
open(os.path.join(ROOT, "spec", "DIFF_R52_PARA_V2C1.patch"), "w", encoding="utf-8", newline="\n").write(patch)
lines = ["# DIFF R5.2-E1 -> V2-c1 «O Teste da Unica Palavra» (cada mudanca atribuida)\n",
         "Pai: R5.2-E1 `%s` (spec canonico `%s`). Filha: `%s` (spec canonico `%s`). Patch linha a linha (JSON ordenado, indent 1): `spec/DIFF_R52_PARA_V2C1.patch` (%d linhas).\n" % (
             sha(raw52)[:16], old_wrap["spec_sha256"][:16], sha(b)[:16], spec_sha[:16], patch.count("\n")),
         "Legenda: **OP-a..d** = decisao do operador de 23/10/2026 (verbatim sha256 `%s`); **C1-...** = ordem da gerencia c1 (reversivel ate o congelamento).\n" % op_sha[:16],
         "| secao | tipo | atribuicao | o que mudou |", "|---|---|---|---|"]
kinds = dict(changed)
for k in sorted(ATTR):
    for tag, resumo in ATTR[k]:
        lines.append("| `%s` | %s | %s | %s |" % (k, kinds[k], tag, resumo))
lines += ["", "## O que NAO mudou (conferido por igualdade canonica)", "",
          "`base`, `beta`, `lei` (K congelado = 1,0838071748529643), `hipoteses`, `familias`, `fundos`, `poder_previo`, `covariancia` (grade, amplitudes, extremos pinados), `novidade_de_uso`, `contaminacao_declarada`, `D5_*`, `observable_TGL_H0_map`, `f34_duas_testemunhas`, `source_pin_verification_R4`, `mu_do_rito`, `gate`. "
          "Na funcao de veredito: **a logica de precedencia e todos os limiares sao os da R5.2** (so mudam o nome, a docstring e a base do token).", ""]
unchanged = sorted(k for k in old if k in new and k not in ATTR)
lines.append("Secoes inalteradas: " + ", ".join("`%s`" % k for k in unchanged))
open(os.path.join(ROOT, "spec", "DIFF_R52_PARA_V2C1.md"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("DIFF: %d secoes mudaram, todas atribuidas; %d inalteradas" % (len(changed), len(unchanged)))
