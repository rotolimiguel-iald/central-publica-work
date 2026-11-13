"""Conferencia independente (numpy puro, escrito do zero) de D congelado e de S0.
Entradas: SOMENTE desenho (A, C, c_cepheid, h_index do network.npz; BG1.json; logK).
Nenhum vetor observado, nenhuma semente, nenhum Monte Carlo."""
import json, math
import numpy as np

B = "C:/IALD/Central de Patentes/work/astra_bell_fock_tt_05nov/h0dn_bg1_06nov/"
with np.load(B + "network/network.npz", allow_pickle=False) as d:
    A = d["A"].copy(); C = d["C"].copy(); c = d["c_cepheid"].copy(); h = int(d["h_index"])
bg = json.load(open(B + "background/BG1.json", encoding="utf-8"))
Cb = np.array(bg["covariance"], float)
H0 = float(bg["mean_parameters"][0])
LN10 = math.log(10.0)
gh = np.array([1.0 / (H0 * LN10), 0.0, 0.0])           # d log10 H0 / d theta (primeira ordem)
vb = float(gh @ Cb @ gh)                                 # variancia do fundo em log10 H
logK = math.log10(float(bg["K"]))                        # K congelado -> log10 K

def support(C, rel=1e-9):
    C = 0.5 * (C + C.T)
    w, U = np.linalg.eigh(C)
    tol = rel * w[-1]
    keep = w > tol
    assert w[~keep].max() < tol and w[0] > -tol, "autovalor negativo substancial"
    return w, U, keep, tol

def gls_h(A, C, c, h, rel=1e-9):
    """Variancia de h-hat por GLS no suporte da covariancia (pseudo-inversa), modelo publicado e c livre."""
    w, U, keep, tol = support(C, rel)
    Uk, wk = U[:, keep], w[keep]
    P = (Uk / wk) @ Uk.T                    # pseudo-inversa de C no suporte
    null = U[:, ~keep]
    out = {"rank": int(keep.sum()), "nullity": int((~keep).sum()),
           "eig_min_pos": float(wk.min()), "eig_max": float(w[-1]), "tol": float(tol),
           "design_off_support": float(np.linalg.norm(null.T @ np.column_stack([A, c])))}
    for name, X in (("publicado", A), ("c_livre", np.column_stack([A, c]))):
        N = X.T @ P @ X
        V = np.linalg.inv(N)                # covariancia GLS dos parametros
        wts = V @ X.T @ P                   # pesos GLS (linhas = parametros)
        wh = wts[h]
        ident = float(np.max(np.abs(wh @ X - np.eye(X.shape[1])[h])))
        vh_a = float(V[h, h])               # variancia pela inversa da matriz normal
        vh_b = float(wh @ C @ wh)           # variancia w' C w
        out[name] = {"Vh_normal": vh_a, "Vh_wCw": vh_b, "ident_err": ident, "w": wh, "cond_N": float(np.linalg.cond(N))}
        out[name]["resp_c"] = float(wh @ c)
        out[name]["D"] = logK / math.sqrt(vh_a + vb)
        out[name]["sd_null"] = math.sqrt(vh_a + vb)
    return out

def show(tag, r, expected):
    print("== %s : rank C=%d nullity=%d eigmin+=%.4e eigmax=%.4e design_off_support=%.2e" %
          (tag, r["rank"], r["nullity"], r["eig_min_pos"], r["eig_max"], r["design_off_support"]))
    for k, e in zip(("publicado", "c_livre"), expected):
        m = r[k]
        print("  %-10s Vh=%.10e (wCw %.10e) vb=%.10e sd=%.10e D=%.10f  esperado=%.6f  |dif|=%.3e  %s  ident=%.1e" %
              (k, m["Vh_normal"], m["Vh_wCw"], vb, m["sd_null"], m["D"], e, abs(m["D"] - e),
               "CONFERE" if abs(m["D"] - e) < 1e-6 else "NAO CONFERE", m["ident_err"]))

print("logK=%.15f  K=%.15f  H0=%.12f  vb=%.12e  gh0=%.12e" % (logK, bg["K"], H0, vb, gh[0]))
print("n,p =", A.shape, " h_index =", h)

# ---------- T1: congelamento (255 linhas) ----------
r1 = gls_h(A, C, c, h)
show("T1 congelado n=255", r1, (6.823355, 5.316944))
# estabilidade ao corte de suporte
for rel in (1e-12, 1e-7):
    rr = gls_h(A, C, c, h, rel)
    print("  corte rel=%g -> rank %d, D=%.10f / %.10f" % (rel, rr["rank"], rr["publicado"]["D"], rr["c_livre"]["D"]))
# comparacao com os pesos congelados (estimator_frozen.npz: chaves de desenho 'weights','sd_null')
with np.load(B + "estimator_frozen.npz", allow_pickle=False) as f:
    W = f["weights"].copy(); sd0 = f["sd_null"].copy(); lk = float(f["logK"])
print("  pesos congelados vs meus: max|dw| publicado=%.3e  c_livre=%.3e" %
      (np.max(np.abs(W[0] - r1["publicado"]["w"])), np.max(np.abs(W[1] - r1["c_livre"]["w"][:0] if False else 0))) if False else "")
# (c_livre: pesos sobre as 255 linhas = wts[h] @ P?  -> nesta implementacao w ja esta em 255 linhas)
print("  pesos congelados vs meus: max|dw| publicado=%.3e  c_livre=%.3e" %
      (np.max(np.abs(W[0] - r1["publicado"]["w"] if r1["publicado"]["w"].shape[0]==255 else 0)),
       np.max(np.abs(W[1] - r1["c_livre"]["w"] if r1["c_livre"]["w"].shape[0]==255 else 0))))
print("  logK congelado no npz = %.15f ; meu = %.15f ; sd_null npz = %s ; meu = %s" %
      (lk, logK, sd0, (r1["publicado"]["sd_null"], r1["c_livre"]["sd_null"])))

# ---------- T2: S0 (retira as 13 linhas 221:234; C0 = C[keep,keep]; zero cruzado local-BG1) ----------
keep = np.ones(255, bool); keep[221:234] = False
A0, C0, c0 = A[keep], C[np.ix_(keep, keep)], c[keep]
r0 = gls_h(A0, C0, c0, h)
show("T2 S0 n=242", r0, (6.710151, 5.191312))
for rel in (1e-12, 1e-7):
    rr = gls_h(A0, C0, c0, h, rel)
    print("  corte rel=%g -> rank %d, D=%.10f / %.10f" % (rel, rr["rank"], rr["publicado"]["D"], rr["c_livre"]["D"]))
json.dump({"logK": logK, "vb": vb,
           "T1": {k: {kk: vv for kk, vv in r1[k].items() if kk != "w"} for k in ("publicado", "c_livre")},
           "S0": {k: {kk: vv for kk, vv in r0[k].items() if kk != "w"} for k in ("publicado", "c_livre")}},
          open("resultado_D.json", "w"), indent=1)
