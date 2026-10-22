# -*- coding: utf-8 -*-
# v379: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# No molde do _v378 (ancoras = as linhas da v378): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS da rodada
# (leitura_v379.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p379) e primeiro nome livre.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v379, textos_v379
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p379_' + ST
    assert not os.path.exists(tmp)
    with open(tmp, 'wb') as f:
        f.write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p379'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p379_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v379.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **A RAZÃO ELEMENTAR (v379)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **A LEI DA DISSIPAÇÃO COM CONTRASTE (v378)")]
    assert len(idx) == 1, ('ancora v378', len(idx))
    linha = 'L.append(%s)   # v379' % repr(textos_v379.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v379)')
else:
    print('arvore_da_prova.py: a linha v379 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v379_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i378p = ')
    L.insert(i + 1, "_i379p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v379_incorporacao_manifesto.json'); _i379 = json.load(open(_i379p, encoding='utf-8')) if os.path.exists(_i379p) else {}   # v379")
    i = acha('verbetes = [')
    L.insert(i, '_V379TXT = %s   # v379' % repr(textos_v379.verbete(V)))
    i = acha(" ('O que faltou: o núcleo derivado D1b e a dupla contagem de β; a lei da dissipação com contraste; a Fase 4, o desvio (v378)', _V378TXT),")
    L.insert(i + 1, " ('A Razão Elementar: E = C × I × K > 0 = β_TGL tipada por termo; E é a assíntota; o reconhecimento é finito por definição (v379)', _V379TXT),")
    i = acha("       '- **O que faltou (v378)")
    L.insert(i + 1, '       %s,' % repr(textos_v379.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v379_incorporacao_manifesto') == 2 and s.count('_V379TXT') == 2
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v379)')
else:
    print('atlas_indice.py: a v379 ja esta (idempotente)')
