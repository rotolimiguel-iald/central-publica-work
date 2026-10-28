import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\mqc_folhas.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)


rep("ax1 = cm_axes(fig, 0.3, 1.2, 9.5, 10.6, projection='3d')", "ax1 = cm_axes(fig, 0.2, 0.8, 9.8, 11.9, projection='3d')")
rep("ax1.set_box_aspect((1, 1, 1), zoom=0.80)", "ax1.set_box_aspect((1, 1, 1), zoom=0.98)")
rep("ax1.legend(loc='upper left', bbox_to_anchor=(-0.02, 1.52), fontsize=FS, frameon=True,",
    "ax1.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), bbox_transform=fig.transFigure, fontsize=FS, frameon=True,")
rep("ax1.set_xlabel('X (μm)', labelpad=8)", "ax1.set_xlabel('X (μm)', labelpad=12)")
rep("ax1.set_ylabel('Y (μm)', labelpad=8)", "ax1.set_ylabel('Y (μm)', labelpad=12)")
rep("    Ht, Hb = 4.2, 5.6", "    Ht, Hb = 4.0, 6.0")
rep("    ys = (10.4, 2.7)", "    ys = (10.7, 2.7)")
rep("    legend(ax, loc='lower right', bbox_to_anchor=(1.0, 0.0))\n    textstr", "    legend(ax, loc='lower right', bbox_to_anchor=(1.0, 0.0), labelspacing=0.25, borderpad=0.35)\n    textstr")
rep("    lg = ax.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1.0, borderpad=0.5, labelspacing=0.45,\n                   handlelength=2.6, **kw)",
    "    kw.setdefault('borderpad', 0.5)\n    kw.setdefault('labelspacing', 0.45)\n    lg = ax.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1.0, handlelength=2.6, **kw)")
rep("fig = plt.figure(figsize=(25.0 / 2.54, 16.2 / 2.54))\n    xs", "fig = plt.figure(figsize=(25.0 / 2.54, 16.7 / 2.54))\n    xs") if "fig = plt.figure(figsize=(25.0 / 2.54, 16.2 / 2.54))\n    xs" in s else None
p.write_text(s, encoding='utf-8')
print('ok', s.count('16.2 / 2.54'))
