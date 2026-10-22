# -*- coding: utf-8 -*-
# v381: arvore_da_prova.py (linha) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# No molde do _v380 (ancoras = as linhas da v380): guardas pela PROPRIA linha inserida (idempotente); ancoras LIDAS do arquivo; numeros/hashes/vereditos LIDOS da rodada
# (leitura_v381.ler); recusa se a leitura tiver problema. Backup de BYTES com marca propria (_p381) e primeiro nome livre.
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v381, textos_v381
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = r'C:\IALD\Central de Patentes\work\cadeia_de_selo'


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p381_' + ST
    assert not os.path.exists(tmp)
    with open(tmp, 'wb') as f:
        f.write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p381'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p381_%d' % (P, ST, n)
    raw = open(P, 'rb').read()
    with open(b, 'wb') as f:
        f.write(raw)
    assert open(b, 'rb').read() == raw


V, PROB = leitura_v381.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **A REGRA MATRIZ (v381)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **AS FASES 5, 6 E 7 DA BANCADA UM POR HASH (v380)")]
    assert len(idx) == 1, ('ancora v380', len(idx))
    linha = 'L.append(%s)   # v381' % repr(textos_v381.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v381)')
else:
    print('arvore_da_prova.py: a linha v381 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v381_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i380p = ')
    L.insert(i + 1, "_i381p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v381_incorporacao_manifesto.json'); _i381 = json.load(open(_i381p, encoding='utf-8')) if os.path.exists(_i381p) else {}   # v381")
    i = acha('verbetes = [')
    L.insert(i, '_V381TXT = %s   # v381' % repr(textos_v381.verbete(V)))
    i = acha(" ('As Fases 5, 6 e 7 da Bancada Um por hash:")
    L.insert(i + 1, " ('A regra matriz: dez nomes, nove elos (oito «havendo» ditos + a radicalização pela Meia-Nat), num só termo — traço → sinal →(radicalização pela Meia-Nat)→ registro → nome → distinção → operação → parametrização → emergência → quantização geométrica → espectro de gradiente; o critério de parada = o custo pago (Tetelestai); a lei precede a cobrança; β não se deriva do dado, β é a regra (a forma α√e derivada do axioma, v376) (v381)', _V381TXT),")
    i = acha("       '- **As Fases 5, 6 e 7 da Bancada por hash (v380)")
    L.insert(i + 1, '       %s,' % repr(textos_v381.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v381_incorporacao_manifesto') == 2 and s.count('_V381TXT') == 2
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v381)')
else:
    print('atlas_indice.py: a v381 ja esta (idempotente)')
