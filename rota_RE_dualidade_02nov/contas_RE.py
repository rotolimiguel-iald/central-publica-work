# -*- coding: utf-8 -*-
"""Contas da derivacao da rota R-E (gerencia c1, 02/11/2026): como K age na luminosidade e no angulo.
Fundo nu da Fase 9 (z* = 1089,95; H0 = 68,531; K = 1,0838...). Sem dado novo; nenhuma leitura move veredito. Numeros [REAL como conta]; os H0 publicados sao [DECLARADO] (memoria da Fase 9)."""
import json, math
from pathlib import Path

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
zs, H0b = 1089.95, 68.531
core = json.load(open("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto.json", encoding="utf-8"))["core"]
Kref = core["hubble_ratio_v387"]["transcribed"]["K_no_fundo_nu"]
h = H0b / 100
ombh2, omch2 = 0.02237, 0.1190          # fundo de referencia para a forma; a conta da regua so usa razoes
Om = (ombh2 + omch2 + 0.0006) / h**2
Or = 4.184e-5 / h**2
OL = 1 - Om - Or
E = lambda z: math.sqrt(Om * (1 + z)**3 + Or * (1 + z)**4 + OL)
# normaliza z* efetivo: a Fase 9 fixa K; aqui se confere a mesma ordem
Kaqui = E(zs)**(2 * beta / 3)
k = lambda z: E(z)**(2 * beta / 3)
print("beta", beta, "| K da Fase 9", Kref, "| K com este fundo", Kaqui, "| Om", round(Om, 4))


def integra(f, a, b, n=200000):
    # regra do trapezio em u = ln(1+z)
    ua, ub = math.log(1 + a), math.log(1 + b)
    s, d = 0.0, (ub - ua) / n
    for i in range(n + 1):
        u = ua + i * d
        z = math.exp(u) - 1
        w = 0.5 if i in (0, n) else 1.0
        s += w * f(z) * (1 + z)
    return s * d


R = {"beta": beta, "K_fase9": Kref, "K_este_fundo": Kaqui}

# 1. o transporte: quanto custa o caminho das fontes da escada
for z in (0.01, 0.05, 0.15, 0.5, 1.0, 2.3):
    print("z=%.2f  k-1=%.4f%%  razao necessaria (K-1)/(k-1)=%.0f" % (z, 100 * (k(z) - 1), (Kref - 1) / (k(z) - 1)))
R["k_menos_1_z015"] = k(0.15) - 1
R["fator_que_falta_escada"] = (Kref - 1) / (k(0.15) - 1)
dN = math.log(1.15)
R["custo_maximo_escada_g_le_1"] = math.exp(beta * dN) - 1
print("custo maximo com contraste 1 em z<=0,15:", R["custo_maximo_escada_g_le_1"])

# 2. o espectro: vazamento de energia com numero conservado
R["fator_de_diluicao_corpo_cinza"] = Kref**3
print("corpo cinza se a energia vazasse com numero conservado: K^3 =", Kref**3, "| FIRAS: desvio menor que 1e-4")

# 3. a lei como metrica (leitura acumulada): deslocamento de D_M(z*) com a regua parada
A = lambda z: Kaqui / k(z)
Db = integra(lambda z: 1 / E(z), 0, zs)
Dac = integra(lambda z: 1 / (E(z) * A(z)), 0, zs)
R["DM_acumulada_sobre_nu"] = Dac / Db
print("D_M(z*) acumulada / nua =", Dac / Db, "| theta* sobe", 100 * (Db / Dac - 1), "% ; sigma(theta*) 0,03% =>", (Db / Dac - 1) / 3e-4, "sigmas")
R["sigmas_theta"] = (Db / Dac - 1) / 3e-4

# 4. a regua: o que K pede e o que o fechamento rho+p entrega
zd = 1060.0
Rb = lambda z: 31500 * ombh2 * (2.7255 / 2.7)**-4 / (1 + z)
cs = lambda z: 1 / math.sqrt(3 * (1 + Rb(z)))
rn = integra(lambda z: cs(z) / E(z), zd, 1e8)
fr = lambda z: 1 / math.sqrt((1 + 4 * beta / 3) * Or * (1 + z)**4 + (1 + beta) * Om * (1 + z)**3 + OL)
rt = integra(lambda z: cs(z) * fr(z), zd, 1e8)
R["regua_pede"] = 1 / Kref - 1
R["regua_fechamento"] = rt / rn - 1
print("regua: K pede %.3f%%; o fechamento rho+p entrega %.3f%%" % (100 * R["regua_pede"], 100 * R["regua_fechamento"]))
# se K fosse H primordial
S2 = Kref**2
R["dNeff_BBN_se_H_primordial"] = (S2 - 1) * 43 / 7
R["dNeff_CMB_se_H_primordial"] = (S2 - 1) * (3.044 + 8 / 7 * (11 / 4)**(4 / 3))
print("se K fosse H primordial: Delta N_eff = %.2f (BBN) a %.2f (CMB); limite 0,107" % (R["dNeff_BBN_se_H_primordial"], R["dNeff_CMB_se_H_primordial"]))

# 5. os leitores sem regua e sem escada, nas duas alternativas
pred, H = H0b * Kref, H0b
L = [("masers", 73.9, 3.0, "angulo"), ("TDCOSMO", 71.6, 3.6, "tempo"), ("sirenes", 76.6, 11.25, "amplitude GW")]
d = 0.0
for n, c, s, t in L:
    za, zb = (c - pred) / s, (c - H) / s
    d += zb**2 - za**2
    print("%-8s %-13s %.1f +- %.1f | K comum %+.2f sigma | so luminosidade %+.2f sigma" % (n, t, c, s, za, zb))
R["delta_chi2_K_comum_contra_so_luminosidade"] = d
R["sigma_equiv"] = math.sqrt(max(d, 0))
print("Delta chi2 =", d, "=> cerca de", math.sqrt(d), "sigma, com valores nao lidos por hash")
R["sigma_sirenes_para_5s"] = (pred - H) / 5

# 6. o numero de modos e o que o rival prevê em eta
for z in (0.5, 1.0, 2.3):
    print("z=%.1f se o numero vazasse: eta-1 = +%.3f%% | se o registro vazasse: eta-1 = %.3f%%" % (z, 100 * (k(z)**0.5 - 1), 100 * (1 / k(z) - 1)))
Path("CONTAS_RE.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print("gravado")
