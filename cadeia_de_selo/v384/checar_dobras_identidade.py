# Verificacao matematica (nenhum operador da teoria): a hierarquia D_folds(c1) > D_folds(c2) > D_folds(c3) > 0 da metrica M7 do validador C3
# vale para TODO espectro com pelo menos dois autovalores nao nulos distintos? (convexidade de s -> ln sum lambda^s)
import numpy as np, sys
sys.stdout.reconfigure(encoding="utf-8")
rng = np.random.default_rng(20261003)
def folds(lam, d, niveis=3):
    out = []; cur = np.maximum(lam, 0.0)
    for n in range(niveis):
        if n > 0: cur = np.sqrt(cur)
        p = cur / cur.sum(); pr = 1.0 / np.sum(p ** 2); out.append(np.log(d) - np.log(pr))
    return out
viol = 0; N = 0; minmarg = np.inf; porcat = {}
for d in (2, 3, 4, 8, 16, 32, 64, 128):
    for kind in ("dirichlet", "posto_baixo", "quase_puro", "quase_uniforme", "lei_potencia"):
        for _ in range(2000):
            if kind == "dirichlet": lam = rng.dirichlet(np.ones(d))
            elif kind == "posto_baixo":
                r = rng.integers(2, d + 1) if d > 2 else 2; lam = np.zeros(d); lam[:r] = rng.dirichlet(np.ones(r))
            elif kind == "quase_puro": lam = np.full(d, 1e-9); lam[0] = 1.0; lam /= lam.sum()
            elif kind == "quase_uniforme": lam = 1.0 + 1e-6 * rng.standard_normal(d); lam /= lam.sum()
            else: lam = (np.arange(1, d + 1, dtype=float)) ** (-rng.uniform(0.1, 4)); lam /= lam.sum()
            if np.unique(np.round(lam[lam > 0], 15)).size < 2: continue
            D1, D2, D3 = folds(lam, d); N += 1
            ok = (D1 > D2 > D3 > 0)
            if not ok:
                viol += 1; porcat[kind] = porcat.get(kind, 0) + 1
            minmarg = min(minmarg, D1 - D2, D2 - D3, D3)
print("espectros testados:", N, "| violacoes de D1 > D2 > D3 > 0:", viol, "| menor margem:", minmarg, "| por categoria:", porcat)
print("violacoes alem de 1e-12:", "nenhuma" if minmarg > -1e-12 else "HA")
# casos de igualdade: puro, uniforme no suporte, maximamente misto
for nome, lam in (("puro", np.eye(1, 8, 0).ravel()), ("uniforme em 3 de 8", np.r_[np.ones(3) / 3, np.zeros(5)]), ("I/d", np.ones(8) / 8)):
    print(nome, ["%.6f" % x for x in folds(lam, 8)])
