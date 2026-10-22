# -*- coding: utf-8 -*-
# v384: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# No molde do _v383 (ancoras = as linhas da v383): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS
# da rodada (leitura_v384.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p384) e primeiro nome livre; temporario -> cresce? ->
# substituir; ast.parse do arquivo novo. NAO RODA arvore_da_prova.py nem atlas_indice.py (isso e' da cadeia, pela gerencia).
# Ensaio: com o Nos SINTETICO, V384_TOOLS=<copias das duas ferramentas>.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
import leitura_v384, textos_v384
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
    b = P + '.bak_' + ST + '_p384'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p384_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v384.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
print('ferramentas em:', TOOLS, V['sint'])
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **O PILAR QUÂNTICO (v384)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **O LIVRO DE COBRANÇAS (v383)")]
    assert len(idx) == 1, ('ancora v383', len(idx))
    linha = 'L.append(%s)   # v384' % repr(textos_v384.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v384)')
else:
    print('arvore_da_prova.py: a linha v384 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v384_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i383p = ')
    L.insert(i + 1, "_i384p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v384_incorporacao_manifesto.json'); _i384 = json.load(open(_i384p, encoding='utf-8')) if os.path.exists(_i384p) else {}   # v384")
    i = acha('verbetes = [')
    L.insert(i, '_V384TXT = %s   # v384' % repr(textos_v384.verbete(V)))
    assert "'" not in V['pr_escolha'] and "'" not in V['pr_id'], (V['pr_escolha'], V['pr_id'])
    i = acha(" ('O livro de cobranças: a TGL é ótica")
    L.insert(i + 1, " ('O pilar quântico na GPU: o sistema aberto da teoria (H_LD + cinco saltos de Lindblad; L_anti = √β·√K, a lei-raiz) calculado em paralelo com o kernel e os ritos, "
                    "[COMPUTED], com registro próprio ao lado do gate; o pré-registro " + V['pr_id'] + " congelado antes do cálculo e ratificado pelo operador (" + V['pr_escolha']
                    + "); quatro testes (T1 o instrumento às cegas, T2 a forma na escala, T3 os controles que têm de falhar, T4 o estresse) + D128 + a referência na CPU; o terceiro balde da "
                    "custódia de sentido; o gate não muda; kernel = o da v383 (v384)', _V384TXT),")
    i = acha("       '- **O livro de cobranças (v383)")
    L.insert(i + 1, '       %s,' % repr(textos_v384.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v384_incorporacao_manifesto') == 2 and s.count('_V384TXT') == 2, (s.count('v384_incorporacao_manifesto'), s.count('_V384TXT'))
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v384)')
else:
    print('atlas_indice.py: a v384 ja esta (idempotente)')
