import importlib.util, io, contextlib, os, numpy as np, fitz
import matplotlib
matplotlib.use("Agg")
W = r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
RUN = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\r2\run"
os.makedirs(RUN, exist_ok=True)
os.chdir(RUN)
spec = importlib.util.spec_from_file_location("mqc_orig", W + r"\entrada\mqc\mqc_simulacao_celula_elementar.py")
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)
# main-flow order of the ORIGINAL script: figure functions 1..7 in sequence (random state carries over)
res = {}
with contextlib.redirect_stdout(io.StringIO()):
    m.gerar_figura_1_topologia()
    res["estab"] = m.gerar_figura_2_estabilizacao()
    res["termo"] = m.gerar_figura_3_termodinamica()
    res["trans"] = m.gerar_figura_4_translacao()
    res["corr"] = m.gerar_figura_5_correcao_erros()
    res["conv"] = m.gerar_figura_6_convergencia()
    res["comm"] = m.gerar_figura_7_comunicacao()
r = res["conv"]
X = np.asarray(r["t"], float)[1:]
V = np.asarray(r["v_info"], float)[1:] / m.C_LUZ


def polys(pg):
    out = []
    for dr in pg.get_drawings():
        if dr["type"] != "s":
            continue
        pts = []
        for it in dr["items"]:
            if it[0] == "l":
                if not pts:
                    pts.append((it[1].x, it[1].y))
                pts.append((it[2].x, it[2].y))
        if len(pts) >= 30:
            out.append((np.array(pts), dr))
    return out


doc = fitz.open(W + r"\FOLHAS_SUBSTITUTIVAS_050579.pdf")
for P, dr in polys(doc[5]):
    if len(P) == 477:
        px, py = P[:, 0], P[:, 1]
        xd = X.min() + (px - px.min()) / np.ptp(px) * np.ptp(X)
        yi = np.log10(np.interp(xd, X, V))
        c = np.polyfit(py, yi, 1)
        resid = yi - np.polyval(c, py)
        print("main-flow order: v_info/c polyline R^2=%.5f, residual max/range=%.3f%%" % (1 - resid.var() / yi.var(), 100 * np.abs(resid).max() / np.ptp(np.log10(V))))
# also check the alpha2 and gtt polylines tightly in main-flow data
A = np.asarray(r["alpha2"], float) * 1000
T = np.asarray(r["t"], float)
G = np.asarray(r["metrica_gtt"], float)
for P, dr in polys(doc[5]):
    if len(P) in (880, 498):
        px, py = P[:, 0], P[:, 1]
        xd = T.min() + (px - px.min()) / np.ptp(px) * np.ptp(T)
        for nm, Y in (("alpha2*1000", A), ("g_tt", G)):
            yi = np.interp(xd, T, Y)
            c = np.polyfit(py, yi, 1)
            resid = yi - np.polyval(c, py)
            print(len(P), nm, "R^2=%.6f max resid/range=%.4f%%" % (1 - resid.var() / yi.var(), 100 * np.abs(resid).max() / np.ptp(Y)))
