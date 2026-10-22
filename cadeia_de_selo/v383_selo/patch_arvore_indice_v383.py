# -*- coding: utf-8 -*-
# v383: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# No molde do _v381 (ancoras = as linhas da v381): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS da rodada
# (leitura_v383.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p383) e primeiro nome livre.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v383, textos_v383
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p383_' + ST
    assert not os.path.exists(tmp)
    with open(tmp, 'wb') as f:
        f.write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p383'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p383_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v383.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **O LIVRO DE COBRANÇAS (v383)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **A REGRA MATRIZ (v381)")]
    assert len(idx) == 1, ('ancora v381', len(idx))
    linha = 'L.append(%s)   # v383' % repr(textos_v383.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v383)')
else:
    print('arvore_da_prova.py: a linha v383 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v383_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i381p = ')
    L.insert(i + 1, "_i383p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v383_incorporacao_manifesto.json'); _i383 = json.load(open(_i383p, encoding='utf-8')) if os.path.exists(_i383p) else {}   # v383")
    i = acha('verbetes = [')
    L.insert(i, '_V383TXT = %s   # v383' % repr(textos_v383.verbete(V)))
    assert V['pr_label'].startswith('V') and all(x.isdigit() for x in V['pr_label'][1:].split('.')) and "'" not in V['pr_label'], V['pr_label']   # o rotulo LIDO do identificador (4a verificacao, R-6)
    i = acha(" ('A regra matriz: dez nomes")
    L.insert(i + 1, " ('O livro de cobranças: a TGL é ótica, lê a face (o pagamento) e o custo (o reflexo); |T|² + |R|² = 1; uma cobrança por lei de leitura, cinco palavras de desfecho; nenhum desfecho move a regra; com uma cobrança extinta a regra segue α√e (a hipótese não entra na prova); ψ = Ω com norma 1 é o zero do lock mínimo sobre o Hamiltoniano oculto; a viscosidade βg é a cobrança contínua; o pré-registro dos dois lados " + V['pr_label'] + " do estimando δ⟨K_∂⟩ por hash; os " + str(V['rot_n']) + " pares do eco fora do livro, como rotas examinadas (decisão do operador); o nome do degrau final pelo pagamento proposto ao lado (v383)', _V383TXT),")
    i = acha("       '- **A regra matriz (v381)")
    L.insert(i + 1, '       %s,' % repr(textos_v383.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v383_incorporacao_manifesto') == 2 and s.count('_V383TXT') == 2
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v383)')
else:
    print('atlas_indice.py: a v383 ja esta (idempotente)')
