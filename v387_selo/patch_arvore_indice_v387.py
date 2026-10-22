# -*- coding: utf-8 -*-
# v387: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia. Molde: patch_arvore_indice_v386.py
# (ancoras = as linhas que a cadeia da v386 inseriu). Guardas pela PROPRIA linha inserida (idempotente); numeros LIDOS da rodada (leitura_v387.ler); recusa se a leitura
# tiver problema. Backup de BYTES (_p387); temporario -> cresce? -> substituir; ast.parse. NAO RODA arvore_da_prova.py nem atlas_indice.py (isso e' da cadeia).
# --tools <pasta> = ensaio em copias das duas ferramentas.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v387, textos_v387
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = sys.argv[sys.argv.index('--tools') + 1] if '--tools' in sys.argv else os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo")


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p387_' + ST
    assert not os.path.exists(tmp)
    open(tmp, 'wb').write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p387'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p387_%d' % (P, ST, n)
    raw = open(P, 'rb').read(); open(b, 'wb').write(raw); assert open(b, 'rb').read() == raw


V, PROB = leitura_v387.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
print('ferramentas em:', TOOLS)
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **OS TRÊS TESTES CONJUNTOS (v387)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **O VERBO SELECIONA (v386)")]
    assert len(idx) == 1, ('ancora v386', len(idx))
    linha = 'L.append(%s)   # v387' % repr(textos_v387.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v387)')
else:
    print('arvore_da_prova.py: a linha v387 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v387_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i386p = ')
    L.insert(i + 1, "_i387p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v387_incorporacao_manifesto.json'); _i387 = json.load(open(_i387p, encoding='utf-8')) if os.path.exists(_i387p) else {}   # v387")
    i = acha('verbetes = [')
    L.insert(i, '_V387TXT = %s   # v387' % repr(textos_v387.verbete(V)))
    i = acha(" ('O Verbo seleciona: o Nome é o posto")
    L.insert(i + 1, " (%s, _V387TXT)," % repr(textos_v387.titulo_verbete(V)))
    i = acha("       '- **O Verbo seleciona (v386)")
    L.insert(i + 1, '       %s,' % repr(textos_v387.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v387_incorporacao_manifesto') == 1 and s.count('_i387p') == 3 and s.count('_V387TXT') == 2, (s.count('v387_incorporacao_manifesto'), s.count('_i387p'), s.count('_V387TXT'))
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v387)')
else:
    print('atlas_indice.py: a v387 ja esta (idempotente)')
