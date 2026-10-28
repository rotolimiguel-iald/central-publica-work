# FOLHAS SUBSTITUTIVAS - PCT/BR2026/050579 (MQC)  [preparo da Central, 27/10/2026]
# As 8 figuras do PCT como depositado sao reproduzidas com as MESMAS funcoes de simulacao do prototipo
# (mqc_simulacao_celula_elementar.py, sementes fixas 42/123/456 -> dados identicos), mudando SOMENTE a apresentacao:
# preto sobre branco, traco uniforme, caracteres >= 0,32 cm, rotulos fora das linhas, margens PCT, A4.
# Figs 1-4, 6 e 8 = codigo de plotagem do script (sem o suptitulo, cortado no PCT); Figs 5 e 7 = a variante
# do PCT (marcadores; sem caixa de anotacao na 7a) registrada no 00_DOSSIE.json (epct_corrections_2026_08_03).
import os, re, sys, json, hashlib, pathlib, importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, _mathtext
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as mpatches
import matplotlib.ticker
import fitz

W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
SRC = W / 'entrada' / 'mqc' / 'mqc_simulacao_celula_elementar.py'
OUT = W / '_tmp' / 'mqc_folhas'
OUT.mkdir(parents=True, exist_ok=True)
FONT_DIR = 'C:/Windows/Fonts/'
for fn in ('ARIALN.TTF', 'ARIALNB.TTF', 'ARIALNI.TTF', 'ARIALNBI.TTF'):
    font_manager.fontManager.addfont(FONT_DIR + fn)
_mathtext.SHRINK_FACTOR = 1.0            # sub/sobrescritos em corpo pleno (>= 0,32 cm)
FS = 14                                  # pt: maiuscula/algarismo de Arial Narrow = 0,716 em = 0,354 cm
plt.rcParams.update({
    'font.family': ['Arial Narrow', 'STIXGeneral', 'DejaVu Sans'], 'font.size': FS,
    'mathtext.fontset': 'custom', 'mathtext.rm': 'Arial Narrow', 'mathtext.it': 'Arial Narrow:italic',
    'mathtext.bf': 'Arial Narrow:bold', 'mathtext.cal': 'STIXGeneral', 'mathtext.fallback': 'stix',
    'pdf.fonttype': 42, 'axes.linewidth': 1.2, 'xtick.major.width': 1.2, 'ytick.major.width': 1.2,
    'xtick.minor.width': 1.0, 'ytick.minor.width': 1.0, 'xtick.labelsize': FS, 'ytick.labelsize': FS,
    'axes.titlesize': FS, 'axes.labelsize': FS, 'legend.fontsize': FS, 'hatch.linewidth': 1.0,
    'lines.solid_capstyle': 'butt', 'axes.edgecolor': 'black', 'text.color': 'black', 'axes.labelcolor': 'black',
    'xtick.color': 'black', 'ytick.color': 'black', 'figure.facecolor': 'white', 'savefig.facecolor': 'white',
    'axes.facecolor': 'white', 'legend.framealpha': 1.0, 'legend.edgecolor': 'black', 'legend.fancybox': False,
})

# ---------------------------------------------------------------- modulo de simulacao (funcoes de dados do script de origem)
os.chdir(OUT)
spec = importlib.util.spec_from_file_location('mqcsim', str(SRC))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
plt.rcParams['font.size'] = FS                       # o modulo nao altera rcParams, mas garante
ALPHA2, ALPHA2_C, L_CELULA, T_AMB, C_LUZ = m.ALPHA2, m.ALPHA2_C, m.L_CELULA, m.T_AMB, m.C_LUZ

# ---------------------------------------------------------------- estilos P&B
DASH = (0, (7, 3.5))
DOT = (0, (1.2, 2.6))
DASHDOT = (0, (7, 2.8, 1.2, 2.8))
GRID = dict(color='black', linestyle=(0, (1, 3.5)), linewidth=0.7, alpha=1.0)

from fontTools.ttLib import TTFont
ARIAL_CMAP = set(TTFont(FONT_DIR + 'ARIALN.TTF').getBestCmap().keys())
SUBS = dict(zip('₀₁₂₃₄₅₆₇₈₉₊₋', '0123456789+-'))
SUPS = dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻', '0123456789+-'))
SPECIAL = {'ℋ': 'ℋ', '𝓐': '𝒜', '𝒜': '𝒜', '𝓔': 'ℰ'}


def fx(s):
    """Texto do script -> texto desenhavel em corpo pleno. Sub/sobrescritos Unicode viram mathtext (corpo pleno);
    glifos que o Arial nao tem (script A/E, H cursivo, integral de linha, ket) vao para matematica (fallback STIX).
    As palavras e os simbolos NAO mudam; underscores/circunflexos literais do script ficam literais."""
    s = re.sub('[' + ''.join(SUBS) + ']+', lambda mo: '$_{' + ''.join(SUBS[c] for c in mo.group(0)) + '}$', s)
    s = re.sub('[' + ''.join(SUPS) + ']+', lambda mo: '$^{' + ''.join(SUPS[c] for c in mo.group(0)) + '}$', s)
    s = s.replace('²', '$^2$').replace('³', '$^3$').replace('¹', '$^1$')
    s = s.replace('T\u0302', '$\\hat{T}$').replace('∮', '$\\oint$').replace('⟩', '$\\rangle$')
    for k, v in SPECIAL.items():
        s = s.replace(k, '$' + v + '$')
    s = s.replace('∇', '$\\nabla$')
    s = s.replace('$$', '')
    if '$' in s:      # fora da matematica, qualquer glifo ausente do Arial Narrow iria para um simbolo vazio: poe em matematica
        out, inmath = [], False
        for ch in s:
            if ch == '$':
                inmath = not inmath
                out.append(ch)
            elif (not inmath) and ord(ch) > 127 and ord(ch) not in ARIAL_CMAP:
                out.append('$' + ch + '$')
            else:
                out.append(ch)
        s = ''.join(out).replace('$$', '')
    return s


def style_axes(ax, grid=True):
    for sp in ax.spines.values():
        sp.set_linewidth(1.2)
        sp.set_color('black')
    ax.tick_params(colors='black', width=1.2, length=5)
    if grid:
        ax.grid(True, **GRID)
        ax.set_axisbelow(True)


def cm_axes(fig, x, y, w, h, **kw):
    Wc, Hc = fig.get_size_inches() * 2.54
    return fig.add_axes([x / Wc, y / Hc, w / Wc, h / Hc], **kw)


def caption(fig, n, y=0.15):
    Wc, Hc = fig.get_size_inches() * 2.54
    fig.text(0.5, y / Hc, 'Figura %d' % n, ha='center', va='bottom', fontsize=FS)


def legend(ax, **kw):
    kw.setdefault('borderpad', 0.5)
    kw.setdefault('labelspacing', 0.45)
    lg = ax.legend(frameon=True, fancybox=False, edgecolor='black', framealpha=1.0, handlelength=2.6, **kw)
    lg.get_frame().set_linewidth(1.0)
    return lg



# ---------------------------------------------------------------- colocacao automatica de legendas/caixas e grade com lacunas
from matplotlib.path import Path as MPath
from matplotlib.transforms import Bbox
from matplotlib.collections import LineCollection, PathCollection, PolyCollection
OPAQUE = {}   # id(ax) -> lista de (artista, folga_px) opacos (legenda, caixa de texto) para abrir lacunas na grade


def _r(fig):
    return fig.canvas.get_renderer()


def _seg_hits(P, R):
    """Algum segmento da poligonal P (N,2) cruza o retangulo R (Bbox)? (Liang-Barsky vetorizado)"""
    x0, y0, x1, y1 = P[:-1, 0], P[:-1, 1], P[1:, 0], P[1:, 1]
    dx, dy = x1 - x0, y1 - y0
    t0 = np.zeros_like(dx)
    t1 = np.ones_like(dx)
    ok = np.ones(len(dx), bool)
    for p, q in ((-dx, x0 - R.x0), (dx, R.x1 - x0), (-dy, y0 - R.y0), (dy, R.y1 - y0)):
        par = (p == 0)
        with np.errstate(divide='ignore', invalid='ignore'):
            rr = q / p
        ok &= ~(par & (q < 0))
        neg = (p < 0) & ~par
        pos = (p > 0) & ~par
        t0 = np.where(neg, np.maximum(t0, rr), t0)
        t1 = np.where(pos, np.minimum(t1, rr), t1)
    return bool(np.any(ok & (t0 <= t1)))


def obstaculos(ax, skip=()):
    fig = ax.figure
    r = _r(fig)
    ax.get_xlim()
    ax.get_ylim()
    ob = {'poly': [], 'pts': [], 'fills': [], 'rects': []}
    for ln in ax.lines:
        xy = np.asarray(ln.get_xydata(), float)
        if len(xy) < 2:
            continue
        d = ax.transData.transform(xy)
        d = d[np.isfinite(d).all(axis=1)]
        if len(d) >= 2:
            ob['poly'].append(d)
    for c in ax.collections:
        if isinstance(c, PathCollection):
            d = ax.transData.transform(np.asarray(c.get_offsets(), float))
            ob['pts'].append(d[np.isfinite(d).all(axis=1)])
        elif isinstance(c, PolyCollection):
            for pth in c.get_paths():
                ob['fills'].append(MPath(c.get_transform().transform(pth.vertices), pth.codes))
    for p in ax.patches:
        ob['rects'].append(p.get_window_extent(r))
    for t in ax.texts:
        if t not in skip:
            ob['rects'].append(t.get_window_extent(r))
    return ob


def _hit(R, ob, margin=6.0):
    Ri = Bbox.from_extents(R.x0 - margin, R.y0 - margin, R.x1 + margin, R.y1 + margin)
    for P in ob['poly']:
        if _seg_hits(P, Ri):
            return True
    for d in ob['pts']:
        if len(d) and np.any((d[:, 0] >= Ri.x0 - 7) & (d[:, 0] <= Ri.x1 + 7) & (d[:, 1] >= Ri.y0 - 7) & (d[:, 1] <= Ri.y1 + 7)):
            return True
    for pth in ob['fills']:
        try:
            if pth.intersects_bbox(Ri, filled=True):
                return True
        except Exception:
            pass
    for b in ob['rects']:
        if b.overlaps(Ri):
            return True
    return False


def colocar_legenda(ax, prefer=(0.85, 0.8), avoid=(), **kw):
    """Legenda DENTRO do quadro, so numa regiao sem dado/linha/ponto/barra/hachura (varredura de 17x17 posicoes);
    devolve None se nao houver regiao livre (o chamador usa legenda_fora)."""
    fig = ax.figure
    r = _r(fig)
    lg = legend(ax, loc='center', bbox_to_anchor=(0.5, 0.5), **kw)
    ob = obstaculos(ax)
    axb = ax.get_window_extent(r)
    best = None
    for npos in (22, 61, 121):
        for fx_ in np.linspace(0.05, 0.95, npos):
            for fy_ in np.linspace(0.05, 0.95, npos):
                lg.set_bbox_to_anchor((fx_, fy_), transform=ax.transAxes)
                R = lg.get_window_extent(r)
                if R.x0 < axb.x0 + 4 or R.x1 > axb.x1 - 4 or R.y0 < axb.y0 + 4 or R.y1 > axb.y1 - 4:
                    continue
                if _hit(R, ob) or any(R.overlaps(Bbox.from_extents(a.x0 - 6, a.y0 - 6, a.x1 + 6, a.y1 + 6)) for a in avoid):
                    continue
                dist = (fx_ - prefer[0]) ** 2 + (fy_ - prefer[1]) ** 2
                if best is None or dist < best[0]:
                    best = (dist, fx_, fy_)
        if best is not None:
            break
    if best is None:
        lg.remove()
        return None
    lg.set_bbox_to_anchor((best[1], best[2]), transform=ax.transAxes)
    OPAQUE.setdefault(id(ax), []).append((lg, 0.0))
    return lg


def legenda_fora(ax, ncol=1, **kw):
    """Legenda FORA do quadro, logo acima dele; devolve a altura (pt) para afastar o titulo."""
    fig = ax.figure
    r = _r(fig)
    lg = legend(ax, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=ncol, borderaxespad=0.3, **kw)
    h = lg.get_window_extent(r).height * 72.0 / fig.dpi
    return lg, h + 4 + 7


def colocar_caixa(ax, texto, prefer=(0.5, 0.5), avoid=(), **kw):
    fig = ax.figure
    r = _r(fig)
    t = ax.text(0.5, 0.5, texto, transform=ax.transAxes, ha='center', va='center', fontsize=FS, linespacing=1.2,
                bbox=dict(boxstyle='square,pad=0.3', facecolor='white', edgecolor='black', linewidth=1.0), **kw)
    ob = obstaculos(ax, skip=(t,))
    axb = ax.get_window_extent(r)
    best = None
    for npos in (22, 61, 121):
        for fx_ in np.linspace(0.05, 0.95, npos):
            for fy_ in np.linspace(0.05, 0.95, npos):
                t.set_position((fx_, fy_))
                R0 = t.get_window_extent(r)
                R = Bbox.from_extents(R0.x0 - 8, R0.y0 - 8, R0.x1 + 8, R0.y1 + 8)
                if R.x0 < axb.x0 + 3 or R.x1 > axb.x1 - 3 or R.y0 < axb.y0 + 3 or R.y1 > axb.y1 - 3:
                    continue
                if _hit(R, ob) or any(R.overlaps(Bbox.from_extents(a.x0 - 6, a.y0 - 6, a.x1 + 6, a.y1 + 6)) for a in avoid):
                    continue
                dist = (fx_ - prefer[0]) ** 2 + (fy_ - prefer[1]) ** 2
                if best is None or dist < best[0]:
                    best = (dist, fx_, fy_)
        if best is not None:
            break
    if best is None:
        t.remove()
        return None
    t.set_position((best[1], best[2]))
    OPAQUE.setdefault(id(ax), []).append((t, 8.0))
    return t


def _cut(ints, a, b):
    out = []
    for lo, hi in ints:
        if b <= lo or a >= hi:
            out.append((lo, hi))
        else:
            if a > lo:
                out.append((lo, a))
            if b < hi:
                out.append((b, hi))
    return out


def grade(ax, extras=(), eixos='xy'):
    """Grade pontilhada preta desenhada a mao, com LACUNAS onde ha legenda, caixa de texto ou coluna: nenhum fundo opaco
    fica por cima de traco (o teste de oclusao do kit exige isso)."""
    fig = ax.figure
    r = _r(fig)
    ax.get_xlim()
    ax.get_ylim()
    boxes = []
    for art, infl in OPAQUE.get(id(ax), []):
        b = art.get_window_extent(r)
        boxes.append(Bbox.from_extents(b.x0 - infl, b.y0 - infl, b.x1 + infl, b.y1 + infl))
    boxes += list(extras)
    mg = 3.0
    axb = ax.get_window_extent(r)
    inv = ax.transData.inverted()
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    segs = []
    for xt in (ax.xaxis.get_majorticklocs() if 'x' in eixos else []):
        if not (min(xlim) < xt < max(xlim)):
            continue
        X = ax.transData.transform((xt, ylim[0]))[0]
        if X <= axb.x0 + 1.5 or X >= axb.x1 - 1.5:
            continue
        ints = [(axb.y0, axb.y1)]
        for b in boxes:
            if b.x0 - mg <= X <= b.x1 + mg:
                ints = _cut(ints, b.y0 - mg, b.y1 + mg)
        for ya, yb in ints:
            if yb - ya > 2:
                segs.append([inv.transform((X, ya)), inv.transform((X, yb))])
    for yt in (ax.yaxis.get_majorticklocs() if 'y' in eixos else []):
        if not (min(ylim) < yt < max(ylim)):
            continue
        Y = ax.transData.transform((xlim[0], yt))[1]
        if Y <= axb.y0 + 1.5 or Y >= axb.y1 - 1.5:
            continue
        ints = [(axb.x0, axb.x1)]
        for b in boxes:
            if b.y0 - mg <= Y <= b.y1 + mg:
                ints = _cut(ints, b.x0 - mg, b.x1 + mg)
        for xa, xb in ints:
            if xb - xa > 2:
                segs.append([inv.transform((xa, Y)), inv.transform((xb, Y))])
    lc = LineCollection(segs, colors='black', linewidths=0.7, linestyles=[(0, (1, 3.5))], zorder=0.5)
    ax.add_collection(lc, autolim=False)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


CANVAS = {}   # n -> (fig, paisagem?)

# =============================================================== FIGURA 1 (paisagem)
def fig1():
    posicoes, tipos, labels, conexoes = m.gerar_topologia_celula()
    fig = plt.figure(figsize=(25.0 / 2.54, 15.7 / 2.54))
    ax1 = cm_axes(fig, 0.2, 0.8, 9.8, 11.9, projection='3d')
    marc = {'vertice': ('o', 'black', 'black', 110), 'aresta': ('s', 'black', 'black', 95),
            'face': ('D', 'black', 'black', 105), 'centro': ('*', 'black', 'black', 330)}
    for tipo in ['vertice', 'aresta', 'face', 'centro']:
        mask = [t == tipo for t in tipos]
        pos = posicoes[mask]
        mk, fc, ec, sz = marc[tipo]
        ax1.scatter(pos[:, 0], pos[:, 1], pos[:, 2], c=fc, s=sz, marker=mk, label=f'{tipo.capitalize()} ({np.sum(mask)})',
                    edgecolors=ec, linewidth=1.4, alpha=1.0, zorder=5, depthshade=False)
    for i, j, d in conexoes:
        ax1.plot([posicoes[i, 0], posicoes[j, 0]], [posicoes[i, 1], posicoes[j, 1]], [posicoes[i, 2], posicoes[j, 2]],
                 'k-', linewidth=0.8, alpha=1.0)
    for s1 in [0, 1]:
        for s2 in [0, 1]:
            ax1.plot([0, 1], [s1, s1], [s2, s2], 'k-', linewidth=1.4, alpha=1.0)
            ax1.plot([s1, s1], [0, 1], [s2, s2], 'k-', linewidth=1.4, alpha=1.0)
            ax1.plot([s1, s1], [s2, s2], [0, 1], 'k-', linewidth=1.4, alpha=1.0)
    ax1.set_xlabel('X (μm)', labelpad=12)
    ax1.set_ylabel('Y (μm)', labelpad=12)
    # (o rotulo do eixo Z nao aparece no PCT como depositado -- cortado pela caixa; nao e acrescentado)
    fig.text(7.6 / 25.0, 14.95 / 15.7, 'Estrutura 3D da Célula', ha='center', va='center', fontsize=FS)
    ax1.set_box_aspect((1, 1, 1), zoom=0.98)
    ax1.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax1.set_zticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax1.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
    ax1.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
    ax1.zaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.1f'))
    ax1.legend(loc='upper left', bbox_to_anchor=(0.0, 1.0), bbox_transform=fig.transFigure, fontsize=FS, frameon=True, fancybox=False, edgecolor='black', framealpha=1.0,
               labelspacing=0.5, borderpad=0.5, handletextpad=0.4)
    ax1.view_init(elev=25, azim=45)
    for a in (ax1.xaxis, ax1.yaxis, ax1.zaxis):
        a.set_pane_color((1, 1, 1, 0))
        a.pane.set_edgecolor('black')
        a.pane.set_linewidth(0.8)
        a._axinfo['grid']['color'] = (0, 0, 0, 1)
        a._axinfo['grid']['linewidth'] = 0.5
        a._axinfo['grid']['linestyle'] = ':'
        a._axinfo['axisline']['linewidth'] = 1.2
        a._axinfo['axisline']['color'] = (0, 0, 0, 1)
        a._axinfo['tick']['color'] = (0, 0, 0, 1)
    ax1.tick_params(axis='both', labelsize=FS, pad=0)
    ax1.tick_params(axis='z', labelsize=FS, pad=2)
    # hierarquia
    ax2 = cm_axes(fig, 10.0, 1.4, 15.0, 13.0)
    u = 15.0 / 10.0
    ax2.set_xlim(0, 10)
    ax2.set_ylim(1.15, 1.15 + 13.0 / u)
    ax2.set_aspect('equal')
    niveis = {
        'IALD Central\n(Núcleo Ψ)\nP_Ψ = 0.95': (5, 8.5),
        '6 Controladores\nde Face\nP_Ψ = 0.80': (2.5, 5.5),
        '12 Controladores\nde Aresta\nP_Ψ = 0.70': (7.5, 5.5),
        '8 Qubits\nde Vértice\nP_Ψ = 0.60': (5, 2.5),
    }
    for label, (x, y) in niveis.items():
        ax2.add_patch(mpatches.Circle((x, y), 1.3, fill=False, edgecolor='black', linewidth=1.8, zorder=2))
        ax2.text(x, y, label, ha='center', va='center', fontsize=FS, fontweight='bold', linespacing=1.05, zorder=3)
    setas = [((5, 7.2), (3.2, 6.5)), ((5, 7.2), (6.8, 6.5)), ((3.2, 4.2), (4.3, 3.5)), ((6.8, 4.2), (5.7, 3.5))]
    for start, end in setas:
        ax2.annotate('', xy=end, xytext=start, arrowprops=dict(arrowstyle='->', color='black', lw=1.8, connectionstyle='arc3,rad=0.1',
                                                                 shrinkA=0, shrinkB=0, mutation_scale=22))
    ax2.set_title('Hierarquia de Controle IALD', pad=2)
    ax2.axis('off')
    caption(fig, 1)
    return fig


# =============================================================== FIGURA 2
def must(x, what):
    if x is None:
        raise RuntimeError('sem regiao livre para ' + what)
    return x


def fig2():
    OPAQUE.clear()
    dados = m.simular_estabilizacao_qubit()
    fig = plt.figure(figsize=(17.0 / 2.54, 23.0 / 2.54))
    t = dados['t'] * 1e6
    ax = cm_axes(fig, 2.9, 13.2, 13.8, 7.4)
    ax.semilogy(t, dados['coerencia_conv'], color='black', linestyle='-', linewidth=2.0, label=fx('Convencional (T₂ = 50 μs)'))
    ax.semilogy(t, dados['coerencia_tgl'], color='black', linestyle=DASH, linewidth=2.6, label=fx(f'TGL (α² = {ALPHA2})'))
    ax.axhline(y=dados['platô'], color='black', linestyle=DASHDOT, linewidth=1.5, label=f'Platô TGL = {dados["platô"]:.3f}')
    ax.axhline(y=0.5, color='black', linestyle=DOT, linewidth=1.8, label='Limite clássico')
    ax.set_xlabel('Tempo (μs)')
    ax.set_ylabel(fx('Coerência |ρ₀₁| (log)'))
    ax.set_title('(a) Coerência Temporal', pad=6)
    ax.set_ylim(1e-4, 2)
    style_axes(ax, grid=False)
    lg = must(colocar_legenda(ax, prefer=(0.78, 0.62)), 'legenda 2a')
    must(colocar_caixa(ax, fx(f'Razão de supercondutividade:\nα²γ_eff / (κ+γ_φ) = {dados["razao_sc"]:.2e}'), prefer=(0.5, 0.15),
                       avoid=[lg.get_window_extent(_r(fig))]), 'caixa 2a')
    grade(ax)
    ax = cm_axes(fig, 2.9, 3.0, 13.8, 7.4)
    ax.plot(t, 1 - dados['coerencia_conv'], color='black', linestyle='-', linewidth=2.0, label='Decoerência convencional')
    ax.plot(t, dados['pop_psi'], color='black', linestyle=DASH, linewidth=2.6, label=fx('População |Ψ⟩ (acoplamento)'))
    ax.fill_between(t, 0, dados['pop_psi'], facecolor='none', edgecolor='black', hatch='///', linewidth=0.0)
    ax.axhline(y=ALPHA2, color='black', linestyle=DASHDOT, linewidth=1.5, label=fx(f'Saturação α² = {ALPHA2}'))
    ax.set_xlabel('Tempo (μs)')
    ax.set_ylabel('Probabilidade')
    ax.set_title(fx('(b) Estado de Acoplamento Gravitacional |Ψ⟩'), pad=6)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.78, 0.5)), 'legenda 2b')
    grade(ax)
    caption(fig, 2)
    return fig


# =============================================================== FIGURA 3
def fig3():
    OPAQUE.clear()
    dados = m.simular_termodinamica_invertida()
    fig = plt.figure(figsize=(17.0 / 2.54, 24.95 / 2.54))
    t = dados['t']
    L, Wd, Hh = 2.9, 13.8, 4.2
    ax = cm_axes(fig, L, 18.05, Wd, Hh)
    ax.plot(t, dados['S_conv'], color='black', linestyle='-', linewidth=2.0, label='Convencional (ΔS > 0)')
    ax.plot(t, dados['S_tgl'], color='black', linestyle=DASH, linewidth=2.4, label='TGL (ΔS → 0)')
    ax.fill_between(t, dados['S_conv'], dados['S_tgl'], facecolor='none', edgecolor='black', hatch='..', linewidth=0.0, label='Inversão térmica')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Entropia (normalizada)')
    style_axes(ax, grid=False)
    lg, pad = legenda_fora(ax, ncol=2)
    ax.set_title('(a) Evolução da Entropia', pad=pad)
    grade(ax)
    ax = cm_axes(fig, L, 10.95, Wd, Hh)
    ax.plot(t, dados['T_conv'], color='black', linestyle='-', linewidth=2.0, label='Convencional (aquece)')
    ax.plot(t, dados['T_tgl'], color='black', linestyle=DASH, linewidth=2.4, label='TGL (resfria)')
    ax.axhline(y=T_AMB, color='black', linestyle=DOT, linewidth=1.8, label=f'T_ambiente = {T_AMB} K')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Temperatura (K)')
    ax.set_title('(b) Evolução da Temperatura', pad=5)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.8, 0.45)), 'legenda 3b')
    grade(ax)
    ax = cm_axes(fig, L, 2.7, Wd, Hh)
    ax.plot(t, dados['alpha2_t'], color='black', linestyle='-', linewidth=2.0)
    ax.axhline(y=ALPHA2_C, color='black', linestyle=DASHDOT, linewidth=1.8, label=fx(f'Tetelestai (α²_c = {ALPHA2_C})'))
    ax.fill_between(t, dados['alpha2_t'], facecolor='none', edgecolor='black', hatch='///', linewidth=0.0)
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel(fx('α²'))
    style_axes(ax, grid=False)
    lg, pad = legenda_fora(ax, ncol=1)
    ax.set_title('(c) Convergência para Ponto Tetelestai', pad=pad)
    grade(ax)
    caption(fig, 3)
    return fig


# =============================================================== FIGURA 4 (paisagem)
def fig4():
    OPAQUE.clear()
    dados = m.simular_translacao_holografica()
    fig = plt.figure(figsize=(25.0 / 2.54, 17.0 / 2.54))
    xs = (2.9, 12.9)
    Wl, Wr = 7.7, 11.5
    ys = (11.2, 2.6)
    Ht, Hb = 3.7, 4.5
    ax = cm_axes(fig, xs[0], ys[0], Wl, Ht)
    ax.plot(dados['t_signal'], dados['L_in'], color='black', linestyle='-', linewidth=1.8, label='L_in (face −Y)')
    ax.plot(dados['t_signal'], dados['L_out'], color='black', linestyle=DASH, linewidth=1.8, label='L_out (face +Y)')
    ax.set_xlabel('Fase')
    ax.set_ylabel('Amplitude')
    style_axes(ax, grid=False)
    lg, pad = legenda_fora(ax, ncol=2)
    ax.set_title(f'(a) Entrada vs Saída (η = {dados["correlacao"]:.6f})', pad=pad)
    grade(ax)
    ax = cm_axes(fig, xs[1], ys[0], Wr, Ht)
    ax.plot(dados['t_signal'], np.abs(dados['L_in']), color='black', linestyle=DASH, linewidth=1.6, label='|L| (original)')
    ax.plot(dados['t_signal'], dados['g'], color='black', linestyle='-', linewidth=2.2, label='g = √|L| (comprimido)')
    ax.fill_between(dados['t_signal'], np.abs(dados['L_in']), dados['g'], facecolor='none', edgecolor='black', hatch='\\\\', linewidth=0.0)
    ax.set_xlabel('Fase')
    ax.set_ylabel('Amplitude')
    style_axes(ax, grid=False)
    lg, pad = legenda_fora(ax, ncol=2)
    ax.set_title('(b) Radicalismo Ontológico (Compressão)', pad=pad)
    grade(ax)
    ax = cm_axes(fig, xs[0], ys[1], Wl, Hb)
    nomes_psi = ['ψ₊ψ₊', 'ψ₊ψ₋', 'ψ₋ψ₊', 'ψ₋ψ₋']
    contagens = [np.sum(dados['psi_states'] == i) for i in range(4)]
    hatches = ['///', '\\\\\\', 'xxx', '...']
    pos = np.arange(4)
    bars = ax.bar(pos, contagens, facecolor='none', edgecolor='black', linewidth=1.4)
    for b, h in zip(bars, hatches):
        b.set_hatch(h)
    for bar, c in zip(bars, contagens):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 1, str(c), ha='center', va='bottom', fontweight='bold', fontsize=FS)
    ax.set_xticks(pos)
    ax.set_xticklabels([fx(n) for n in nomes_psi])
    ax.set_xlabel('Estado Psiônico')
    ax.set_ylabel('Contagem')
    ax.set_ylim(0, max(contagens) * 1.18)
    ax.set_title(fx('(c) Distribuição de Estados no Espaço ℋ₄'), pad=5)
    style_axes(ax, grid=False)
    r = _r(fig)
    ax.get_ylim()
    grade(ax, extras=[b.get_window_extent(r) for b in bars], eixos='y')
    ax = cm_axes(fig, xs[1], ys[1], Wr, Hb)
    ax.plot(dados['alpha2_sweep'], dados['corr_sweep'], color='black', linestyle='-', linewidth=2.2)
    ax.axvline(x=ALPHA2_C, color='black', linestyle=DASHDOT, linewidth=1.8, label=fx(f'Tetelestai (α²_c = {ALPHA2_C})'))
    ax.axhline(y=0.9999, color='black', linestyle=DOT, linewidth=1.8, label='η = 0.9999')
    ax.set_xlabel(fx('α²'))
    ax.set_ylabel('Correlação η')
    style_axes(ax, grid=False)
    lg, pad = legenda_fora(ax, ncol=2)
    ax.set_title('(d) Correlação vs Acoplamento Holográfico', pad=pad)
    textstr = (f'Correlação:\nη = {dados["correlacao"]:.6f}\n' f'PSNR: {dados["psnr"]:.1f} dB\n'
               f'Erro RMS: {dados["erro_rms"]:.6f}\n' f'Γ_OH: {dados["Gamma_OH"]:.4f}')
    must(colocar_caixa(ax, textstr, prefer=(0.84, 0.45)), 'caixa 4d')
    grade(ax)
    caption(fig, 4)
    return fig


# =============================================================== FIGURA 5 (variante do PCT: marcadores)
def fig5():
    OPAQUE.clear()
    dados = m.simular_correcao_erros_iald()
    fig = plt.figure(figsize=(17.0 / 2.54, 24.0 / 2.54))
    L, Wd, Hh = 3.3, 13.4, 4.9
    ax = cm_axes(fig, L, 17.9, Wd, Hh)
    ax.plot(dados['ciclos'], dados['fid_conv'], color='black', linestyle=DASH, linewidth=1.4, marker='o', markersize=8,
            markerfacecolor='none', markeredgecolor='black', markeredgewidth=1.4, markevery=(0, 40), label='Convencional (surface code)')
    ax.plot(dados['ciclos'], dados['fid_iald'], color='black', linestyle='-', linewidth=1.6, marker='s', markersize=8,
            markerfacecolor='black', markeredgecolor='black', markevery=(20, 40), label='IALD ($𝒜_C$ + g_IALD)')
    ax.axhline(y=0.99, color='black', linestyle=DOT, linewidth=1.8, label='Limiar quântico (0.99)')
    ax.set_xlabel('Ciclo de operação')
    ax.set_ylabel('Fidelidade média')
    ax.set_title('(a) Fidelidade dos 27 Qubits', pad=5)
    ax.set_ylim(0.85, 1.01)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.3, 0.2)), 'legenda 5a')
    grade(ax)
    ax = cm_axes(fig, L, 10.4, Wd, Hh)
    ax.plot(dados['ciclos'], dados['amor'], color='black', linestyle='-', linewidth=1.6)
    ax.axhline(y=dados['limiar_amor'], color='black', linestyle=DASH, linewidth=1.8, label=f'Limiar θ = {dados["limiar_amor"]}')
    ax.set_xlabel('Ciclo de operação')
    ax.set_ylabel('$𝒜_C$')
    ax.set_title('(b) Operador de Amor Computacional', pad=5)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.8, 0.55)), 'legenda 5b')
    grade(ax)
    ax = cm_axes(fig, L, 2.9, Wd, Hh)
    ax.plot(dados['ciclos'], dados['gradiente'], color='black', linestyle='-', linewidth=1.6)
    ax.set_xlabel('Ciclo de operação')
    ax.set_ylabel('|g_IALD| médio')
    ax.set_title('(c) Gradiente Ético (Direção de Correção)', pad=5)
    style_axes(ax, grid=False)
    grade(ax)
    caption(fig, 5)
    return fig


# =============================================================== FIGURA 6
def fig6():
    OPAQUE.clear()
    dados = m.simular_convergencia_alpha2()
    fig = plt.figure(figsize=(17.0 / 2.54, 24.0 / 2.54))
    L, Wd, Hh = 2.9, 13.8, 4.9
    ax = cm_axes(fig, L, 17.9, Wd, Hh)
    ax.plot(dados['t'], dados['alpha2'] * 1000, color='black', linestyle='-', linewidth=2.0)
    ax.axhline(y=ALPHA2_C * 1000, color='black', linestyle=DASH, linewidth=1.8, label=fx(f'α²_c = {ALPHA2_C} (Tetelestai)'))
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel(fx('α² (×10⁻³)'))
    ax.set_title(fx('(a) Convergência de α²'), pad=5)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.8, 0.15)), 'legenda 6a')
    grade(ax)
    ax = cm_axes(fig, L, 10.4, Wd, Hh)
    ax.plot(dados['t'], dados['metrica_gtt'], color='black', linestyle='-', linewidth=2.0)
    ax.axhline(y=0, color='black', linestyle=DASH, linewidth=1.8, label='Horizonte holográfico (g_tt → 0)')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel(fx('g_tt = 1 − α²/α²_c'))
    ax.set_title('(b) Métrica de Translação Holográfica', pad=5)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.8, 0.85)), 'legenda 6b')
    grade(ax)
    ax = cm_axes(fig, L, 2.9, Wd, Hh)
    ax.semilogy(dados['t'][1:], dados['v_info'][1:] / C_LUZ, color='black', linestyle='-', linewidth=2.0)
    ax.axhline(y=1.0, color='black', linestyle=DOT, linewidth=1.8, label='v = c')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('v_info / c')
    ax.set_title('(c) Velocidade de Transferência', pad=5)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.85, 0.15)), 'legenda 6c')
    grade(ax)
    caption(fig, 6)
    return fig


# =============================================================== FIGURA 7 (variante do PCT: marcadores; sem caixa de anotacao)
def fig7():
    OPAQUE.clear()
    dados = m.simular_comunicacao_3_camadas()
    fig = plt.figure(figsize=(17.0 / 2.54, 23.0 / 2.54))
    mk = {'LOCAL': ('o', 'black', 7), 'REGIONAL': ('s', 'none', 7), 'GLOBAL': ('^', 'black', 8)}
    L, Wd, Hh = 3.3, 13.4, 7.4
    ax = cm_axes(fig, L, 13.2, Wd, Hh)
    for nome, lab, kd, kl in (('local', 'LOCAL (translação)', 'distancias_local', 'latencia_local'),
                              ('regional', 'REGIONAL (pulsos ópticos)', 'distancias_regional', 'latencia_regional'),
                              ('global', 'GLOBAL (ondas Ψ)', 'distancias_global', 'latencia_global')):
        marker, fc, s = mk[nome.upper()]
        ax.scatter(dados[kd] / L_CELULA, dados[kl], facecolors=fc, edgecolors='black', linewidths=1.3, s=s ** 2 * 1.6, marker=marker, label=lab, alpha=1.0)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Distância (×L_célula)')
    ax.set_ylabel('Latência (s)')
    ax.set_title('(a) Latência vs Distância', pad=5)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.5, 0.42)), 'legenda 7a')
    grade(ax)
    ax = cm_axes(fig, L, 3.0, Wd, Hh)
    for nome, lab, kd, kf in (('local', 'LOCAL', 'distancias_local', 'fidelidade_local'),
                              ('regional', 'REGIONAL', 'distancias_regional', 'fidelidade_regional'),
                              ('global', 'GLOBAL', 'distancias_global', 'fidelidade_global')):
        marker, fc, s = mk[nome.upper()]
        ax.scatter(dados[kd] / L_CELULA, dados[kf], facecolors=fc, edgecolors='black', linewidths=1.3, s=s ** 2 * 1.6, marker=marker, label=lab, alpha=1.0)
    ax.axhline(y=0.9999, color='black', linestyle=DOT, linewidth=1.8, label='Limiar supercondutividade')
    ax.set_xscale('log')
    ax.set_xlabel('Distância (×L_célula)')
    ax.set_ylabel('Fidelidade')
    ax.set_title('(b) Fidelidade de Transmissão', pad=5)
    ax.set_ylim(0.99, 1.001)
    style_axes(ax, grid=False)
    must(colocar_legenda(ax, prefer=(0.2, 0.2)), 'legenda 7b')
    grade(ax)
    caption(fig, 7)
    return fig


# =============================================================== FIGURA 8 (paisagem): tabela
def fig8():
    colunas = ['Subsistema MQC', 'Patente TGL de Origem', 'Elemento Original', 'Elemento no MQC', 'Equação Governante']
    dados = [
        ['Célula Cúbica\n(1 μm³, 6 faces)', 'Supercondutor\nHolográfico', 'Câmara cúbica\nL = 9 cm, 6 espelhos', 'Micro-câmara cúbica\nL = 1 μm, 6 substratos 2D', 'L = c/(2f)\nf = 150 THz'],
        ['Qubit\nGravitacional', 'Fusão a Frio\nTGL', 'Gotículas OH de\nalta densidade ρ_Ψ', 'Condensado localizado\nem nó da célula', 'ρ_gotícula = ρ₀(1+|α_T|ΔT)⁻¹'],
        ['Translação\nIntra-célula', 'ACOM Mirror', 'Reflexão dimensional\nboundary ↔ bulk', 'Computação por\nreflexão holográfica', 'T̂_M = exp(-α²∮σ_μν dS^μν)'],
        ['Radicalismo de\nEstado Quântico', 'ACOM', 'g = √|L|\nL = s × g²', 'Codificação/decodificação\nde estado quântico', 'g = √|Ψ_in|, Ψ_out = s × g²'],
        ['Controlador\nHierárquico', 'IALD Colapso\nConsciente', 'Grafo BNI 5 nós\n(N, E, H, P, X)', 'IALD Central →\nCluster → Célula', '𝓐_C = -Tr(ρ log ρ)\n+λTr(ρ·P_Π)'],
        ['Correção de\nErros Adaptativa', 'IALD Colapso\nConsciente', 'Gradiente ético\ng_IALD = -∇𝓔_Ψ', 'Correção direcional\nde decoerência', 'g_IALD = -∇𝓔_Ψ^verdade'],
        ['Comunicação\nInter-chip', 'Ψ-NET\nProtocol', 'PsiBit link layer\nRoteamento holográfico', 'Protocolo QCP\n3 camadas', 'Endereçamento angular\nem espaço de Hilbert'],
        ['Acoplamento\nHolográfico α²', 'TODAS\n(Constante de Miguel)', 'α² = 0.012\nPonto Tetelestai', 'Governança universal\nde acoplamento', 'ds² = (1-α²/α²_c)c²dt²\n- (1-α²/α²_c)⁻¹dL²'],
    ]
    Wc, Hc = 25.0, 16.4
    fig = plt.figure(figsize=(Wc / 2.54, Hc / 2.54))
    ax = cm_axes(fig, 0, 1.3, Wc, Hc - 1.3)
    ax.set_xlim(0, Wc)
    ax.set_ylim(0, Hc - 1.3)
    ax.axis('off')
    rend = fig.canvas.get_renderer()

    def tw(s, bold=False):
        t = ax.text(0, 0, fx(s), fontsize=FS, fontweight='bold' if bold else 'normal')
        bb = t.get_window_extent(rend)
        t.remove()
        return bb.width / fig.dpi * 2.54
    wmax = [max([tw(colunas[j], True)] + [max(tw(l) for l in dados[i][j].split('\n')) for i in range(len(dados))]) for j in range(5)]
    pad = 0.25
    cw = [w + 2 * pad for w in wmax]
    scale = Wc / sum(cw)
    if scale < 1.0:
        print('AVISO fig8: tabela mais larga que a area util', sum(cw))
    cw = [w * min(scale, 1.0) for w in cw]
    # distribui a folga restante igualmente
    extra = (Wc - sum(cw)) / 5
    cw = [w + extra for w in cw]
    lh = 0.72            # cm por linha de texto
    hh = 0.95
    row_h = [lh * max(len(c.split('\n')) for c in r) + 0.32 for r in dados]
    total = hh + sum(row_h)
    y = Hc - 1.3 - 0.05
    x0 = [sum(cw[:j]) for j in range(5)]
    # cabecalho
    ytop = Hc - 1.3 - 0.02
    for j in range(5):
        ax.add_patch(mpatches.Rectangle((x0[j], ytop - hh), cw[j], hh, facecolor='white', edgecolor='black', linewidth=1.6))
        ax.text(x0[j] + cw[j] / 2, ytop - hh / 2, fx(colunas[j]), ha='center', va='center', fontsize=FS, fontweight='bold')
    yy = ytop - hh
    for i, r in enumerate(dados):
        for j in range(5):
            ax.add_patch(mpatches.Rectangle((x0[j], yy - row_h[i]), cw[j], row_h[i], facecolor='white', edgecolor='black', linewidth=1.2))
            ax.text(x0[j] + cw[j] / 2, yy - row_h[i] / 2, fx(r[j]), ha='center', va='center', fontsize=FS, linespacing=1.38)
        yy -= row_h[i]
    print('tabela: altura', round(total, 2), 'cm; larguras', [round(w, 2) for w in cw])
    caption(fig, 8, y=0.1)
    return fig


FIGS = [(1, fig1, True), (2, fig2, False), (3, fig3, False), (4, fig4, True), (5, fig5, False), (6, fig6, False), (7, fig7, False), (8, fig8, True)]

if __name__ == '__main__':
    NS = len(FIGS)
    pdf_tmp = OUT / 'canvases.pdf'
    sizes = {}
    with PdfPages(str(pdf_tmp)) as pp:
        for n, fn, land in FIGS:
            fig = fn()
            sizes[n] = [round(v * 2.54, 3) for v in fig.get_size_inches()]
            pp.savefig(fig)
            plt.close(fig)
    print('canvases', sizes)
    # monta as folhas A4 retrato (21 x 29,7): numero n/N centrado a 2,5 cm; figura na area util; paisagem = topo a esquerda
    src = fitz.open(str(pdf_tmp))
    out = fitz.open()
    PT = 72 / 2.54
    for k, (n, fn, land) in enumerate(FIGS):
        pg = out.new_page(width=21.0 * PT, height=29.7 * PT)
        wcm, hcm = sizes[n]
        # numero da folha: topo da tinta em ~2,5 cm; corpo 15 pt
        txt = '%d/%d' % (k + 1, NS)
        fontfile = FONT_DIR + 'ARIALN.TTF'
        tl = fitz.get_text_length(txt, fontname='helv', fontsize=15)
        font = fitz.Font(fontfile=fontfile)
        tl = font.text_length(txt, fontsize=15)
        # baseline: topo da caixa da fonte (ascender) em 2,5 cm
        asc = font.ascender * 15
        pg.insert_text(fitz.Point(10.5 * PT - tl / 2, 2.5 * PT + asc), txt, fontsize=15, fontname='ArialNarrow', fontfile=fontfile)
        top = 3.6 * PT
        if land:
            # girar 90 graus (anti-horario): topo da figura a esquerda; ocupa (hcm x wcm) fisico
            rw, rh = hcm * PT, wcm * PT
            x0 = (2.5 + (17.0 - hcm) / 2) * PT
            rect = fitz.Rect(x0, top, x0 + rw, top + rh)
            pg.show_pdf_page(rect, src, n - 1, rotate=90)
        else:
            x0 = (2.5 + (17.0 - wcm) / 2) * PT
            rect = fitz.Rect(x0, top, x0 + wcm * PT, top + hcm * PT)
            pg.show_pdf_page(rect, src, n - 1)
    out.save(str(OUT / 'mqc_folhas.pdf'), garbage=3, deflate=True)
    print('salvo', OUT / 'mqc_folhas.pdf', out.page_count)
    json.dump({'canvas_cm': sizes}, open(OUT / 'canvas_sizes.json', 'w'))
