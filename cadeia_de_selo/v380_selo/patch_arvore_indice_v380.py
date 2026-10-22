# -*- coding: utf-8 -*-
# v380: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# No molde do _v379 (ancoras = as linhas da v379): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS da rodada
# (leitura_v380.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p380) e primeiro nome livre.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v380, textos_v380
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p380_' + ST
    assert not os.path.exists(tmp)
    with open(tmp, 'wb') as f:
        f.write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p380'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p380_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v380.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **AS FASES 5, 6 E 7 DA BANCADA UM POR HASH (v380)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **A RAZÃO ELEMENTAR (v379)")]
    assert len(idx) == 1, ('ancora v379', len(idx))
    linha = 'L.append(%s)   # v380' % repr(textos_v380.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v380)')
else:
    print('arvore_da_prova.py: a linha v380 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v380_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i379p = ')
    L.insert(i + 1, "_i380p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v380_incorporacao_manifesto.json'); _i380 = json.load(open(_i380p, encoding='utf-8')) if os.path.exists(_i380p) else {}   # v380")
    i = acha('verbetes = [')
    L.insert(i, '_V380TXT = %s   # v380' % repr(textos_v380.verbete(V)))
    i = acha(" ('A Razão Elementar: E = C × I × K > 0 = β_TGL tipada por termo; E é a assíntota; o reconhecimento é finito por definição (v379)', _V379TXT),")
    L.insert(i + 1, " ('As Fases 5, 6 e 7 da Bancada Um por hash: o SH0ES; o eco como resposta radical da fronteira — o par (√β ou sin 2θ, 2π/κ) falsificado; MAY inconclusivo; a covariância dos cronômetros; o banco de GW; seis erratas da auditoria (+1 da v378, +1 nota) ao lado (v380)', _V380TXT),")
    i = acha("       '- **A Razão Elementar (v379)")
    L.insert(i + 1, '       %s,' % repr(textos_v380.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v380_incorporacao_manifesto') == 2 and s.count('_V380TXT') == 2
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v380)')
else:
    print('atlas_indice.py: a v380 ja esta (idempotente)')
