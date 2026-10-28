import sys
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import mqc_folhas as nf
import numpy as np
import matplotlib.pyplot as plt
m = nf.m
dados = m.simular_translacao_holografica()
fig = plt.figure(figsize=(25.0 / 2.54, 17.0 / 2.54))
ax = nf.cm_axes(fig, 12.9, 2.6, 10.0, 4.5)
ax.plot(dados['alpha2_sweep'], dados['corr_sweep'], color='black', linewidth=2.2)
ax.axvline(x=nf.ALPHA2_C, color='black')
ax.axhline(y=0.9999, color='black')
nf.style_axes(ax, grid=False)
r = nf._r(fig)
t = ax.text(0.5, 0.5, 'Correlação:\nη = 0.999996\nPSNR: 56.1 dB\nErro RMS: 0.002308\nΓ_OH: 0.9866', transform=ax.transAxes, ha='center', va='center', fontsize=14, linespacing=1.2,
            bbox=dict(boxstyle='square,pad=0.3'))
R0 = t.get_window_extent(r)
axb = ax.get_window_extent(r)
print('dpi', fig.dpi, 'axes px', axb.width, axb.height, 'box px', R0.width, R0.height, 'cm', R0.width / fig.dpi * 2.54, R0.height / fig.dpi * 2.54)
print('xlim', ax.get_xlim(), 'ylim', ax.get_ylim())
X = ax.transData.transform((nf.ALPHA2_C, 0.996))[0]
print('x da linha vertical (px desde o eixo)', X - axb.x0, 'fracao', (X - axb.x0) / axb.width)
Y = ax.transData.transform((0.012, 0.9999))[1]
print('y da linha eta fracao', (Y - axb.y0) / axb.height)
