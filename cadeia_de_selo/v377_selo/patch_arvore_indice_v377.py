# -*- coding: utf-8 -*-
# v376: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), no scratchpad-casa das ferramentas (sessao d554e796).
# No molde do _v371 (ancoras = as linhas da v371): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS da rodada
# (leitura_v376.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p377) e primeiro nome livre.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v377, textos_v377
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'   # v376: a casa canonica das ferramentas da cadeia (copias byte a byte, sha256 conferido)


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p377_' + ST
    assert not os.path.exists(tmp)
    with open(tmp, 'wb') as f:
        f.write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p377'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p377_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v377.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **A LEI DA DISSIPAÇÃO, PROVADA (v377)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **O TODO É UM (v376)")]
    assert len(idx) == 1, ('ancora v376', len(idx))
    linha = 'L.append(%s)   # v377' % repr(textos_v377.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v377)')
else:
    print('arvore_da_prova.py: a linha v377 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v377_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i376p = ')
    L.insert(i + 1, "_i377p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v377_incorporacao_manifesto.json'); _i377 = json.load(open(_i377p, encoding='utf-8')) if os.path.exists(_i377p) else {}   # v376")
    i = acha('verbetes = [')
    L.insert(i, '_V377TXT = %s   # v377' % repr(textos_v377.verbete(V)))
    i = acha(" ('O todo é um: β, o fundamento derivado, ligado à QG num só termo; a chave é o leitor; o ρ* na luz; o escopo do ringdown; a auditoria de 28/09 (v376)', _V376TXT),")
    L.insert(i + 1, " ('A lei da dissipação, provada; a física é a leitura; as três fases da Bancada por hash; o desvio de β como foco (v377)', _V377TXT),")
    i = acha("       '- **O todo é um (v376)")
    L.insert(i + 1, '       %s,' % repr(textos_v377.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v377_incorporacao_manifesto') == 2 and s.count('_V377TXT') == 2
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v377)')
else:
    print('atlas_indice.py: a v377 ja esta (idempotente)')
