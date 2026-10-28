# Prova de que as folhas substitutivas do MQC plotam OS MESMOS DADOS do script de origem:
# (i) arrays de cada linha/ponto/barra (por figura, na mesma ordem) das figuras novas vs. as funcoes originais do script
# (executadas sem alteracao, com savefig interceptado); (ii) textos da tabela da Fig. 8 identicos.
import sys, json, ast, pathlib, importlib.util
import numpy as np
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import mqc_folhas as nf              # executa o preambulo (rcParams, carga do script de origem); __main__ nao roda
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.collections as mcoll
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
m = nf.m


def harvest(fig):
    out = []
    for ax in fig.axes:
        for ln in ax.lines:
            if hasattr(ln, 'get_data_3d'):
                x, y, z = ln.get_data_3d()
                out.append(('linha3d', np.array([np.asarray(x, float), np.asarray(y, float), np.asarray(z, float)])))
            else:
                out.append(('linha', np.asarray(ln.get_xydata(), float)))
        for c in ax.collections:
            if hasattr(c, '_offsets3d'):
                out.append(('pontos3d', np.array([np.asarray(a, float) for a in c._offsets3d])))
            elif isinstance(c, mcoll.PathCollection):
                out.append(('pontos', np.asarray(c.get_offsets(), float)))
        for p in ax.patches:
            if type(p) is mpatches.Rectangle and p.get_width() != 1.0 and ax.get_xlabel() == 'Estado Psiônico':
                out.append(('barra', np.array([p.get_height()], float)))
    return out


# ---- original: executa as funcoes do script sem alteracao, interceptando savefig
orig = {}
cur = {'n': None}
real_savefig = plt.savefig


def fake_savefig(*a, **k):
    orig[cur['n']] = harvest(plt.gcf())


plt.savefig = fake_savefig
for n, name in ((1, 'gerar_figura_1_topologia'), (2, 'gerar_figura_2_estabilizacao'), (3, 'gerar_figura_3_termodinamica'),
                (4, 'gerar_figura_4_translacao'), (5, 'gerar_figura_5_correcao_erros'), (6, 'gerar_figura_6_convergencia'),
                (7, 'gerar_figura_7_comunicacao')):
    cur['n'] = n
    getattr(m, name)()
plt.savefig = real_savefig
# ---- novas
novas = {}
for n, fn, land in nf.FIGS:
    if n == 8:
        continue
    fig = fn()
    novas[n] = harvest(fig)
    plt.close(fig)
res = []
for n in range(1, 8):
    a, b = orig[n], novas[n]
    # compara nas mesmas posicoes; barras do original so existem na Fig. 4 (patches) -> filtradas igual
    ok_n = len(a) == len(b)
    iguais = 0
    maxdiff = 0.0
    detalhe = []
    for i, ((ta, xa), (tb, xb)) in enumerate(zip(a, b)):
        eq = ta == tb and xa.shape == xb.shape and np.array_equal(xa, xb)
        if eq:
            iguais += 1
        else:
            detalhe.append({'i': i, 'tipo_orig': ta, 'tipo_novo': tb, 'shape_orig': list(xa.shape), 'shape_novo': list(xb.shape)})
        if xa.shape == xb.shape:
            maxdiff = max(maxdiff, float(np.max(np.abs(xa - xb))) if xa.size else 0.0)
    res.append({'figura': n, 'artistas_original': len(a), 'artistas_novos': len(b), 'mesmo_numero': ok_n, 'arrays_identicos': iguais,
                'diferencas': detalhe, 'maior_diferenca_absoluta': maxdiff,
                'pontos_de_dados_comparados': int(sum(x.size for _, x in a))})
    print(res[-1]['figura'], len(a), len(b), iguais, maxdiff)
# ---- tabela da Fig. 8: textos das celulas
src_o = (W / 'entrada' / 'mqc' / 'mqc_simulacao_celula_elementar.py').read_text(encoding='utf-8')
src_n = (W / 'fontes' / 'mqc_folhas.py').read_text(encoding='utf-8')


def lista(src, funcname, var):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == funcname:
            for st in ast.walk(node):
                if isinstance(st, ast.Assign) and any(getattr(t, 'id', None) == var for t in st.targets):
                    return ast.literal_eval(st.value)


do, dn = lista(src_o, 'gerar_figura_8_correspondencia', 'dados'), lista(src_n, 'fig8', 'dados')
co, cn = lista(src_o, 'gerar_figura_8_correspondencia', 'colunas'), lista(src_n, 'fig8', 'colunas')
tab = {'celulas_identicas': do == dn, 'cabecalhos_identicos': co == cn, 'n_celulas': sum(len(r) for r in do)}
print('tabela', tab)
(W / 'conferencia' / 'mqc_dados_identicos.json').write_text(json.dumps({'figuras_1_a_7': res, 'figura_8_tabela': tab,
        'metodo': 'arrays de linhas/pontos/barras lidos dos artistas do matplotlib nas figuras do script de origem (savefig interceptado) e nas folhas novas; np.array_equal'}, indent=1, ensure_ascii=False), encoding='utf-8')
