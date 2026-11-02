# -*- coding: utf-8 -*-
"""Medida da gerência c1 (01/11/2026) para a reclassificação do teste do Grande Atrator. Só aritmética sobre constantes e âncoras seladas; nenhum dado novo;
beta em runtime (ALPHA_FINE_CODATA_2018 x sqrt(e)), nunca literal. Saída: MEDIDA_GA_01nov.json."""
import json, math, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ctl = json.loads(Path(r"C:\IALD\Central de Patentes\work\rite394_20261015\r3\bancada_corpus\ORDEM005_MASSA_CONTROLES.json").read_text(encoding="utf-8"))["constants"]
core = json.loads(Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json").read_text(encoding="utf-8"))
alpha, c, G, MSUN, MPC = ctl["SEALED_CODATA_ALPHA"], ctl["C_LIGHT"], ctl["G_NEWTON"], ctl["MSUN"], ctl["MPC_M"]
beta = alpha * math.sqrt(math.e)
W = c ** 2 / (4 * math.pi * G)                     # kg/m
por_mpc = W * MPC / MSUN
form = lambda R: 2 * beta ** 2 * por_mpc * R       # v4/v98: M = 2 beta^2 (c^2/4piG) R
flux = lambda R: beta * por_mpc * R                # junho: M = (c^2/4piG) beta R_B
M_A, M_B = core["verdict"]["masses_Msun"]["A_literature"], core["verdict"]["masses_Msun"]["B_cf4_positions"]
lo, hi = core["accepted_window_Msun"]
R_A, R_B_cf4 = M_A / form(1), M_B / form(1)
out = {"beta_runtime": beta, "constantes_seladas": ctl and {"alpha": alpha, "c": c, "G": G, "MSUN": MSUN, "MPC_M": MPC}}
out["1_a_formula_nao_contem_u"] = {"form_por_Mpc_Msun": form(1), "flux_por_Mpc_Msun": flux(1), "v_caracteristica_kms": beta * c / math.sqrt(2 * math.pi) / 1000,
                                   "leitura": "M/R so depende de beta, c e G: dM/du = 0; a unidade da massa do neutrino nao aparece; a cadeia E0 nao tem por onde entrar"}
linhas = []
for nome, M in (("bacia LB88", 5.4e16), ("nucleo Norma", 1.0e15), ("Laniakea", 1.0e17)):
    Mk = M * MSUN; rs = 2 * G * Mk / c ** 2; tau = 4 * math.pi * G * Mk / c ** 3          # o tempo do monopolo, 31/10
    Gamma = beta / tau; RB = c / Gamma                                                   # Gamma_B = beta/tau (identidade de 31/10); R_B = c/Gamma_B (junho)
    M_volta = (c ** 2 / (4 * math.pi * G)) * beta * RB / MSUN                            # a lei de fluxo de junho
    linhas.append({"ancora": nome, "M_Msun": M, "r_s_Mpc": rs / MPC, "tau_s": tau, "tau_kyr": tau / 3.15576e10, "tau_igual_2pi_rs_sobre_c": abs(tau - 2 * math.pi * rs / c) / tau < 1e-12,
                   "Gamma_s-1": Gamma, "R_B_Mpc": RB / MPC, "R_B_sobre_r_s": RB / rs, "2pi_sobre_beta": 2 * math.pi / beta, "M_de_volta_Msun": M_volta, "residuo_relativo": abs(M_volta - M) / M})
out["2_a_mesma_parede"] = {"linhas": linhas, "leitura": "lei de fluxo de junho + R_B = c/Gamma_B + Gamma_B = beta/tau + tau do monopolo (31/10) => M = M: identidade; beta cancela; a massa fixa tau, nao o contrario. O numero que falta e' um so: a escala do setor."}
out["3_piso_de_definicao"] = {"M_A_literatura_Msun": M_A, "M_B_cf4_Msun": M_B, "R_A_Mpc": R_A, "R_B_cf4_Mpc": R_B_cf4, "razao_A_sobre_B": M_A / M_B,
                              "leitura": "so a definicao do raio move a propria previsao em 38 por cento; nao ha sigma selado"}
anc = 5.4e16
out["4_precisao_necessaria"] = {"janela_Msun": [lo, hi], "decadas_da_janela": math.log10(hi / lo), "fator_de_folga_sobre_a_ancora_para_cima": hi / anc, "fator_de_folga_para_baixo": anc / lo,
                                "para_5sigma_entre_form_R57_e_ancora": {"diferenca_Msun": anc - M_A, "sigma_necessario_Msun": (anc - M_A) / 5, "sigma_relativo_na_ancora": (anc - M_A) / 5 / anc},
                                "resposta_de_materia_beta": {"desvio_relativo": beta, "sigma_relativo_para_5sigma": beta / 5, "leitura": "se o efeito fosse a resposta w=0 = beta, seria preciso medir a massa a 0,24 por cento"}}
s45 = math.sin(math.pi / 4)
out["5_escolha_antes_de_olhar"] = {"fator_se_a_leitura_da_massa_valer_para_o_GA": s45, "M_form_com_sen45_R57_Msun": form(57) * s45, "M_form_com_sen45_cf4_Msun": M_B * s45,
                                   "na_janela": bool(lo <= form(57) * s45 <= hi), "ramo_galactico_MW_razao": form(0.1) * s45 / 1e12, "ramo_galactico_GL_razao": form(1.5) * s45 / 5e12,
                                   "leitura": "aplicar o sen45 NAO resgata o ramo galactico e cabe na janela como a forma antiga: a janela nao distingue; e' escolha a ler antes, nao teste"}
(HERE / "MEDIDA_GA_01nov.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("beta", beta); print(json.dumps(out["1_a_formula_nao_contem_u"], ensure_ascii=False)[:230])
for l in linhas:
    print("%-14s r_s %.5f Mpc | tau %.1f kyr | R_B %.3f Mpc | R_B/r_s %.2f | residuo %.1e | tau=2pi r_s/c %s" % (l["ancora"], l["r_s_Mpc"], l["tau_kyr"], l["R_B_Mpc"], l["R_B_sobre_r_s"], l["residuo_relativo"], l["tau_igual_2pi_rs_sobre_c"]))
print(json.dumps(out["3_piso_de_definicao"], ensure_ascii=False)[:260]); print(json.dumps(out["4_precisao_necessaria"], ensure_ascii=False)[:420]); print(json.dumps(out["5_escolha_antes_de_olhar"], ensure_ascii=False)[:300])
