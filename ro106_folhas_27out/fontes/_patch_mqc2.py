import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\mqc_folhas.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)


rep("ax1 = cm_axes(fig, 1.6, 1.4, 8.4, 13.2, projection='3d')", "ax1 = cm_axes(fig, 0.3, 1.2, 9.5, 10.6, projection='3d')")
rep("    ax1.set_box_aspect((1, 1, 1), zoom=0.92)\n    ax1.legend(loc='upper left', bbox_to_anchor=(-0.16, 1.03), fontsize=FS, frameon=True,",
    "    ax1.set_box_aspect((1, 1, 1), zoom=0.80)\n    ax1.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])\n    ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])\n    ax1.set_zticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])\n    ax1.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))\n    ax1.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))\n    ax1.zaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))\n    ax1.legend(loc='upper left', bbox_to_anchor=(-0.02, 1.52), fontsize=FS, frameon=True,")
rep("    ax1.set_title('Estrutura 3D da Célula', pad=-6)\n", "    fig.text(7.6 / 25.0, 14.95 / 15.7, 'Estrutura 3D da Célula', ha='center', va='center', fontsize=FS)\n")
rep("import matplotlib.patches as mpatches", "import matplotlib.patches as mpatches\nimport matplotlib.ticker")
rep("    xs = (2.9, 11.9)\n    Wl, Wr = 7.7, 10.6\n    ys = (10.0, 2.7)\n    Ht, Hb = 4.3, 5.2", "    xs = (2.9, 12.9)\n    Wl, Wr = 7.7, 10.0\n    ys = (10.4, 2.7)\n    Ht, Hb = 4.2, 5.6")
rep("ax.text(0.985, 0.30, textstr,", "ax.text(0.985, 0.33, textstr,")
p.write_text(s, encoding='utf-8')
print('ok')
