# -*- coding: utf-8 -*-
# v385: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# No molde do _v384 (ancoras = as linhas que a cadeia da v384 inseriu: «O PILAR QUÂNTICO (v384)», _i384p, «O pilar quântico na GPU», «O pilar quântico (v384)»): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS
# da rodada (leitura_v385.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p385) e primeiro nome livre; temporario -> cresce? ->
# substituir; ast.parse do arquivo novo. NAO RODA arvore_da_prova.py nem atlas_indice.py (isso e' da cadeia, pela gerencia).
# Ensaio: com o Nos SINTETICO, V385_TOOLS=<copias das duas ferramentas>.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v385 as A
import leitura_v385, textos_v385
ST = time.strftime('%Y%m%d_%H%M%S')
AMB = A.ambiente(); TOOLS = AMB['tools']


def grava(P, s):
    A.pode_escrever(P, AMB)
    ast.parse(s)
    tmp = P + '.tmp_p384_' + ST
    assert not os.path.exists(tmp)
    with open(tmp, 'wb') as f:
        f.write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    A.pode_escrever(P, AMB)
    b = P + '.bak_' + ST + '_p385'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p384_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v385.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
print('ferramentas em:', TOOLS, V['sint'])
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **O AXIOMA (v385)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **O PILAR QUÂNTICO (v384)")]
    assert len(idx) == 1, ('ancora v384', len(idx))
    linha = 'L.append(%s)   # v385' % repr(textos_v385.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v385)')
else:
    print('arvore_da_prova.py: a linha v385 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v385_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i384p = ')
    L.insert(i + 1, "_i385p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v385_incorporacao_manifesto.json'); _i385 = json.load(open(_i385p, encoding='utf-8')) if os.path.exists(_i385p) else {}   # v385")
    i = acha('verbetes = [')
    L.insert(i, '_V385TXT = %s   # v385' % repr(textos_v385.verbete(V)))
    i = acha(" ('O pilar quântico na GPU:")
    L.insert(i + 1, " (%s, _V385TXT)," % repr(textos_v385.titulo_verbete(V)))
    i = acha("       '- **O pilar quântico (v384)")
    L.insert(i + 1, '       %s,' % repr(textos_v385.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v385_incorporacao_manifesto') == 2 and s.count('_i385p') == 3 and s.count('_V385TXT') == 2, (s.count('v385_incorporacao_manifesto'), s.count('_i385p'), s.count('_V385TXT'))
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v385)')
else:
    print('atlas_indice.py: a v385 ja esta (idempotente)')
