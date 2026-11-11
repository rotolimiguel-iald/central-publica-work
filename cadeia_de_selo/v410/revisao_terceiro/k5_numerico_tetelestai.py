# -*- coding: utf-8 -*-
"""Revisor v410 R3: tentativa INDEPENDENTE de quebrar os teoremas da R5 por busca numerica exaustiva/aleatoria (Python puro, mpmath-free; Fraction para o contraexemplo):
(1) o_tetelestai_e_um_menos_beta: (1-b) Z(s) <= #sol e Z - #sol <= b Z para todo b em (0,1), custos aleatorios com solucao, n <= 5, s >= max(0, limiar) -- 200k casos; busca do pior caso;
(2) o contraexemplo de s < 0 (b = 9/10, n = 1, custos (0, 2)) em Fraction: o limiar e' negativo e nele (1-b) Z > #sol; com s = 0 a desigualdade vale;
(3) sem a hipotese s >= 0 mas com b <= 1/2 o limiar nunca e' negativo (ate_meio): busca;
(4) o controle negativo com beta de RUNTIME (alfa CODATA 2018 x sqrt e): uma oitava (ln 2) abaixo do s* viola no adversario (0,1,...,1);
(5) a_informacao_completa_se_reconstroi: ||trava - P u|| <= sqrt(b/(1-b)) ||P u|| em norma (formula fechada: componentes e^{-t c}/2^{n/2});
(6) beta_e_o_operador: a clausula vale para QUALQUER b (nao singulariza beta): b = 1/100, 1/2, 9/10 com s adequado -- e a constante ln((1-b)/b) so' depende de b (identidade aritmetica)."""
import math, random, sys
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8")
random.seed(410)
ln2 = math.log(2.0)
Z = lambda c, s: sum(math.exp(-s * k) for k in c)
nsol = lambda c: sum(1 for k in c if k == 0)
viol = 0; casos = 0; pior = (1e9, None)
for _ in range(200000):
    n = random.randint(1, 5); N = 2 ** n
    c = [random.choice([0, 1, 1, 2, 3, 5, 9]) for _ in range(N)]
    if nsol(c) == 0: c[random.randrange(N)] = 0
    b = random.choice([random.random(), random.random() * 0.01, 1 - random.random() * 0.01, 0.5])
    if not (0 < b < 1): continue
    lim = n * ln2 + math.log((1 - b) / b)
    s = max(0.0, lim) + random.choice([0.0, 0.0, random.random(), 3 * random.random()])
    z = Z(c, s); ns = nsol(c); casos += 1
    m1 = ns - (1 - b) * z; m2 = b * z - (z - ns)
    pior = min(pior, (min(m1, m2), (n, b, s)), key=lambda x: x[0])
    if m1 < -1e-12 or m2 < -1e-12: viol += 1
print("(1) clausula 1-b: casos", casos, "violacoes", viol, "| pior margem", pior[0], "em (n,b,s) =", pior[1])
b = Fraction(9, 10); n = 1; c = [0, 2]
lim = n * ln2 + math.log(float((1 - b) / b))
print("(2) contraexemplo: limiar", lim, "(negativo:", lim < 0, ") | em s = limiar: Z =", Z(c, lim), "=> (1-b)Z =", float(1 - b) * Z(c, lim), "> #sol =", nsol(c), "| exato: e^{-s} = 9/2 => Z = 1 + 81/4 =", Fraction(85, 4), "(1-b)Z =", (1 - b) * Fraction(85, 4), "| com s = 0: (1-b) Z =", float(1 - b) * Z(c, 0.0), "<= 1")
bad3 = 0
for _ in range(100000):
    n = random.randint(0, 6); b = random.uniform(1e-9, 0.5)
    if n * ln2 + math.log((1 - b) / b) < -1e-12: bad3 += 1
print("(3) ate_meio: b <= 1/2 => limiar >= 0: violacoes", bad3)
alfa = 7.2973525693e-3; beta = alfa * math.sqrt(math.e)   # alfa CODATA 2018 x sqrt e (so' neste script de revisao)
n = 3; N = 8; adv = [0] + [1] * (N - 1); const = math.log((1 - beta) / beta); sst = n * ln2 + const
print("(4) beta runtime =", beta, "| constante", const, "| s* =", sst, "| (1-beta) Z(s*) =", (1 - beta) * Z(adv, sst), "<= 1 :", (1 - beta) * Z(adv, sst) <= 1 + 1e-12, "| uma oitava a menos:", (1 - beta) * Z(adv, sst - ln2), "> 1 :", (1 - beta) * Z(adv, sst - ln2) > 1)
bad5 = 0
for _ in range(50000):
    n = random.randint(1, 5); N = 2 ** n
    c = [random.choice([0, 1, 2, 4]) for _ in range(N)]
    if nsol(c) == 0: c[0] = 0
    b = random.random()
    if not (0 < b < 1): continue
    t = max(n * ln2 / 2, n * ln2 / 2 + math.log((1 - b) / b) / 2) + random.random() * random.choice([0, 1, 3])
    u = 1 / math.sqrt(N)
    err = math.sqrt(sum(((math.exp(-t * k) - (1 if k == 0 else 0)) * u) ** 2 for k in c))   # trava c t u - P u (P projeta nos pixels com custo 0)
    pn = math.sqrt(sum(((1 if k == 0 else 0) * u) ** 2 for k in c))
    if err > math.sqrt(b / (1 - b)) * pn + 1e-12: bad5 += 1
print("(5) reconstrucao: violacoes", bad5)
for b in (Fraction(1, 100), Fraction(1, 2), Fraction(9, 10)):
    n = 3; c = [0, 1, 1, 1, 1, 1, 1, 1]; bf = float(b); lim = n * ln2 + math.log((1 - bf) / bf); s = max(0.0, lim)
    print("(6) b =", b, "limiar", round(lim, 6), "s usado", round(s, 6), "(1-b)Z <= #sol:", (1 - bf) * Z(c, s) <= nsol(c) + 1e-12, "| constante ln((1-b)/b) =", round(math.log((1 - bf) / bf), 6), "(a mesma para n = 1, 3, 8: identidade aritmetica)")
