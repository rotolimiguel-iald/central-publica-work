import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\mqc_folhas.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)


# ---- fig1
rep("ax1 = cm_axes(fig, 0.0, 1.5, 10.8, 13.4, projection='3d')", "ax1 = cm_axes(fig, 1.6, 1.4, 8.4, 13.2, projection='3d')")
rep("edgecolors=ec, linewidth=1.4, alpha=1.0, zorder=5)", "edgecolors=ec, linewidth=1.4, alpha=1.0, zorder=5, depthshade=False)")
rep("    ax1.legend(loc='upper left', fontsize=FS, frameon=True,",
    "    ax1.set_box_aspect((1, 1, 1), zoom=0.92)\n    ax1.legend(loc='upper left', bbox_to_anchor=(-0.16, 1.03), fontsize=FS, frameon=True,")
rep("ax2 = cm_axes(fig, 10.9, 1.5, 14.1, 13.4)\n    u = 14.1 / 10.0", "ax2 = cm_axes(fig, 10.0, 1.4, 15.0, 13.0)\n    u = 15.0 / 10.0")
rep("ax2.set_ylim(0.9, 0.9 + 13.4 / u)", "ax2.set_ylim(1.15, 1.15 + 13.0 / u)")
# ---- figs 2 e 7 (2 paineis)
rep("fig = plt.figure(figsize=(17.0 / 2.54, 22.3 / 2.54))\n    t = dados['t'] * 1e6\n    ax = cm_axes(fig, 2.9, 12.6, 13.8, 7.4)",
    "fig = plt.figure(figsize=(17.0 / 2.54, 23.0 / 2.54))\n    t = dados['t'] * 1e6\n    ax = cm_axes(fig, 2.9, 13.2, 13.8, 7.4)")
rep("    ax = cm_axes(fig, 2.9, 2.0, 13.8, 7.4)\n    ax.plot(t, 1 - dados['coerencia_conv']",
    "    ax = cm_axes(fig, 2.9, 3.0, 13.8, 7.4)\n    ax.plot(t, 1 - dados['coerencia_conv']")
rep("fig = plt.figure(figsize=(17.0 / 2.54, 22.3 / 2.54))\n    mk =", "fig = plt.figure(figsize=(17.0 / 2.54, 23.0 / 2.54))\n    mk =")
rep("L, Wd, Hh = 3.3, 13.4, 7.4\n    ax = cm_axes(fig, L, 12.6, Wd, Hh)", "L, Wd, Hh = 3.3, 13.4, 7.4\n    ax = cm_axes(fig, L, 13.2, Wd, Hh)")
rep("    ax = cm_axes(fig, L, 2.0, Wd, Hh)\n    for nome, lab, kd, kf in", "    ax = cm_axes(fig, L, 3.0, Wd, Hh)\n    for nome, lab, kd, kf in")
# ---- figs 3, 5, 6 (3 paineis)
rep("L, Wd, Hh = 2.9, 13.8, 5.0\n    ax = cm_axes(fig, L, 16.6, Wd, Hh)", "L, Wd, Hh = 2.9, 13.8, 4.9\n    ax = cm_axes(fig, L, 17.9, Wd, Hh)", 2)
rep("L, Wd, Hh = 3.3, 13.4, 5.0\n    ax = cm_axes(fig, L, 16.6, Wd, Hh)", "L, Wd, Hh = 3.3, 13.4, 4.9\n    ax = cm_axes(fig, L, 17.9, Wd, Hh)")
s = s.replace("ax = cm_axes(fig, L, 9.0, Wd, Hh)", "ax = cm_axes(fig, L, 10.4, Wd, Hh)")
s = s.replace("ax = cm_axes(fig, L, 1.7, Wd, Hh)", "ax = cm_axes(fig, L, 2.9, Wd, Hh)")
# ---- fig4
rep("""    Wd, Hh = 9.1, 4.7
    xs = (2.9, 15.5)
    ys = (9.2, 1.9)""", """    xs = (2.9, 11.9)
    Wl, Wr = 7.7, 10.6
    ys = (10.0, 2.7)
    Ht, Hb = 4.3, 5.2""")
rep("ax = cm_axes(fig, xs[0], ys[0], Wd, Hh)\n    ax.plot(dados['t_signal'], dados['L_in']", "ax = cm_axes(fig, xs[0], ys[0], Wl, Ht)\n    ax.plot(dados['t_signal'], dados['L_in']")
rep("ax = cm_axes(fig, xs[1], ys[0], Wd, Hh)\n    ax.plot(dados['t_signal'], np.abs", "ax = cm_axes(fig, xs[1], ys[0], Wr, Ht)\n    ax.plot(dados['t_signal'], np.abs")
rep("ax = cm_axes(fig, xs[0], ys[1], Wd, Hh)\n    nomes_psi", "ax = cm_axes(fig, xs[0], ys[1], Wl, Hb)\n    nomes_psi")
rep("ax = cm_axes(fig, xs[1], ys[1], Wd, Hh)\n    ax.plot(dados['alpha2_sweep']", "ax = cm_axes(fig, xs[1], ys[1], Wr, Hb)\n    ax.plot(dados['alpha2_sweep']")
rep("textstr = (f'Correlação: η = {dados[\"correlacao\"]:.6f}\\n'", "textstr = (f'Correlação:\\nη = {dados[\"correlacao\"]:.6f}\\n'")
rep("ax.text(0.62, 0.36, textstr, transform=ax.transAxes, fontsize=FS, ha='left', va='bottom',", "ax.text(0.985, 0.30, textstr, transform=ax.transAxes, fontsize=FS, ha='right', va='bottom',")
rep("fig = plt.figure(figsize=(25.0 / 2.54, 16.2 / 2.54))\n    Wd", "fig = plt.figure(figsize=(25.0 / 2.54, 16.2 / 2.54))\n    Wd") if False else None
p.write_text(s, encoding='utf-8')
print('ok')
