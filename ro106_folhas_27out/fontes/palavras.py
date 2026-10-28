# Conferencia "mesmas palavras, mesmos sinais de referencia, mesmas figuras" (sem materia nova), por script.
# Aprendizado: texto vivo da FONTE compilada sem alteracao (orig_figs.pdf, identica ao PCT como depositado: apr_identidade_fonte.json)
#              vs texto vivo das folhas novas, por folha.
# MQC: textos desenhados pelas funcoes de origem (savefig interceptado) -- sem o suptitulo, sem a caixa da Fig. 7a e sem o
#      rotulo Z da Fig. 1 (nao constam do PCT como depositado) -- vs texto vivo das folhas novas, por folha.
import sys, re, json, unicodedata, pathlib, collections
import fitz
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
TOK = re.compile(r'[^\W\d_]+')


def toks(text):
    t = unicodedata.normalize('NFKC', text.replace('\x1c', 'fi').replace('\x1d', 'fl'))
    return [x.lower() for x in TOK.findall(t)]


def apr(final_pdf):
    orig = fitz.open(str(W / '_tmp' / 'orig' / 'orig_figs.pdf'))
    new = fitz.open(str(final_pdf))
    plano = {1: [1], 2: [2, 3], 3: [4, 5], 4: [6, 7], 5: [8], 6: [9]}
    out = []
    for sh, figs in plano.items():
        a = collections.Counter(t for f in figs for t in toks(orig[f - 1].get_text()))
        b = collections.Counter(t for t in toks(new[sh - 1].get_text()) if t != 'figura')
        out.append({'folha': sh, 'figuras': figs,
                    'linhas_texto_fonte_como_depositado': [l for f in figs for l in orig[f - 1].get_text().splitlines() if l.strip()],
                    'linhas_texto_folha_nova': [l for l in new[sh - 1].get_text().splitlines() if l.strip()],
                    'palavras_da_fonte': sum(a.values()), 'palavras_da_folha_nova': sum(b.values()),
                    'so_na_fonte': sorted(set(a) - set(b)), 'so_na_folha_nova': sorted(set(b) - set(a)),
                    'contagens_diferentes': {k: [a[k], b[k]] for k in set(a) & set(b) if a[k] != b[k]}})
    return out


def mqc(final_pdf):
    sys.path.insert(0, str(W / 'fontes'))
    import mqc_folhas as nf
    import matplotlib.pyplot as plt
    from matplotlib.text import Text
    m = nf.m
    orig = {}
    cur = {'n': None}
    real = plt.savefig

    def fake(*a, **k):
        fig = plt.gcf()
        skip = set()
        if getattr(fig, '_suptitle', None) is not None:
            skip.add(id(fig._suptitle))
        for ax in fig.axes:
            if hasattr(ax, 'zaxis'):
                skip.add(id(ax.zaxis.label))          # rotulo Z: cortado no PCT como depositado
        txts = []
        for t in fig.findobj(Text):
            s = t.get_text()
            if not s or id(t) in skip or not t.get_visible():
                continue
            if cur['n'] == 7 and s.startswith('τ_translação'):
                continue                              # caixa de anotacao: ausente do PCT como depositado (Fig. 7a)
            txts.append(s)
        orig[cur['n']] = '\n'.join(txts)

    plt.savefig = fake
    for n, name in ((1, 'gerar_figura_1_topologia'), (2, 'gerar_figura_2_estabilizacao'), (3, 'gerar_figura_3_termodinamica'),
                    (4, 'gerar_figura_4_translacao'), (5, 'gerar_figura_5_correcao_erros'), (6, 'gerar_figura_6_convergencia'),
                    (7, 'gerar_figura_7_comunicacao'), (8, 'gerar_figura_8_correspondencia')):
        cur['n'] = n
        getattr(m, name)()
    plt.savefig = real
    # fig 8 (tabela): textos de celula vindos do literal
    new = fitz.open(str(final_pdf))
    out = []
    for sh in range(1, 9):
        if sh == 8:
            import ast
            src = (W / 'entrada' / 'mqc' / 'mqc_simulacao_celula_elementar.py').read_text(encoding='utf-8')
            tree = ast.parse(src)
            txt = ''
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == 'gerar_figura_8_correspondencia':
                    for st in ast.walk(node):
                        if isinstance(st, ast.Assign) and any(getattr(t, 'id', None) in ('dados', 'colunas') for t in st.targets):
                            v = ast.literal_eval(st.value)
                            txt += '\n'.join(str(c) for r in (v if isinstance(v[0], list) else [v]) for c in r) + '\n'
            orig[8] = txt
        a = collections.Counter(toks(orig[sh]))
        b = collections.Counter(t for t in toks(new[sh - 1].get_text()) if t != 'figura')
        out.append({'folha': sh, 'figura': sh,
                    'linhas_texto_origem': [l for l in orig[sh].splitlines() if l.strip()],
                    'linhas_texto_folha_nova': [l for l in new[sh - 1].get_text().splitlines() if l.strip()], 'palavras_da_origem': sum(a.values()), 'palavras_da_folha_nova': sum(b.values()),
                    'so_na_origem': sorted(set(a) - set(b)), 'so_na_folha_nova': sorted(set(b) - set(a)),
                    'contagens_diferentes': {k: [a[k], b[k]] for k in set(a) & set(b) if a[k] != b[k]}})
    return out


if __name__ == '__main__':
    which, pdf = sys.argv[1], sys.argv[2]
    r = apr(pdf) if which == 'apr' else mqc(pdf)
    (W / 'conferencia' / f'palavras_{which}.json').write_text(json.dumps(r, indent=1, ensure_ascii=False), encoding='utf-8')
    for x in r:
        print(x['folha'], 'so_origem', x.get('so_na_fonte', x.get('so_na_origem')), '| so_nova', x['so_na_folha_nova'], '| contagens', x['contagens_diferentes'])
