# -*- coding: utf-8 -*-
# Registro da v386 SELADA (molde: superficies_v385.py): diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (§X, append datado),
# memorias-topico (v386: missao-ultima-flag-um-py, central-de-patentes-estado, verbo-selecao-da-acao-05out, ramo-b-reaberto-05out, v384-pilar-quantico-gpu-02out),
# a superficie NOVA da linhagem C:\IALD\Artigo\Haja_Luz\CLAUDE.md (decisao do operador de 05/10, item 16 da delegacao: um append datado curto apontando as
# memorias) e o indice MEMORY.md (a linha da missao ganha o marcador v386; a linha do pilar ganha, ao lado, o marcador do servidor no pacote v386; as linhas
# de conteudo da frente Codex que seguirem um marcador <!-- IALD_... --> vao INTEIRAS ao MEMORY_2.md). Duas fases (plano conferido antes da primeira escrita);
# backup de BYTES (.bak_<STAMP>_sup386); temporario -> conferir tamanho -> substituir; append puro; idempotente pelo cabecalho de cada bloco; fim de linha do arquivo.
# O LIMITE do indice: 24 000 B COM a folga para a linha do handoff (que vem depois). Sem folga: RECUSA (rode compactar_memory_para_v386.py --gravar antes).
# GUARDA: so grava se a leitura (leitura_v386.ler) nao tiver problema (rito limpo, conferidor, gate intocado, hashes, os quatro registros v386...).
# Ensaio em COPIA: V386_REMAP_DIR=<pasta com copias dos alvos> + V386_WRITE_ROOT=<raiz permitida>; ou o Nos SINTETICO com V386_UMEM/V386_ATLAS_DIR/V386_HAJA_LUZ.
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
import leitura_v386, textos_v386 as T
AMB = A.ambiente()
NOS = AMB['nos']; UMEM = AMB['umem']; ATLAS = os.path.join(AMB['atlas_dir'], 'TGL_ATLAS.md'); HAJA = AMB['haja_luz']
REMAP = AMB['remap']; ROOT = AMB['write_root']
STAMP = time.strftime('%Y%m%d_%H%M%S')
MARCA_BAK = '_sup386'
LIMITE_INDICE = 24000


def alvo(p):
    return os.path.join(REMAP, os.path.basename(p)) if REMAP else p


def guarda(p):
    if ROOT:
        assert os.path.realpath(p).lower().startswith(os.path.realpath(ROOT).lower() + os.sep), 'ESCRITA FORA DA RAIZ PERMITIDA: %s' % p
    elif AMB['sint']:
        raise AssertionError('ensaio com o Nos SINTETICO sem V386_WRITE_ROOT -- recuso')
    print('  ESCRITA:', p)


def nl_de(raw):
    return '\r\n' if raw.count(b'\r\n') > raw.count(b'\n') // 2 else '\n'


PLANO = {}


def corrente(p):
    if p not in PLANO:
        raw = open(p, 'rb').read(); PLANO[p] = {'raw': raw, 'novo': raw, 'o_que': []}
    return PLANO[p]['novo']


def append(p, bloco, marcador):
    p = alvo(p)
    cur = corrente(p)
    if marcador.encode('utf-8') in cur.replace(b'\r\n', b'\n'):
        print('JA ESTA (idempotente):', os.path.basename(p)); return
    nlc = nl_de(cur)
    sep = (nlc * 2) if cur.endswith(nlc.encode()) else (nlc * 3)
    PLANO[p]['novo'] = cur + sep.encode() + bloco.replace('\r\n', '\n').replace('\n', nlc).encode('utf-8') + nlc.encode()
    PLANO[p]['o_que'].append('append (%s)' % ('CRLF' if nlc == '\r\n' else 'LF'))


V, PROB = leitura_v386.ler()
if PROB:
    print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
LINH = T.linhagem(V); DESE = T.desenho(V); ATL = T.atlas(V); HL = T.haja_luz(V)
append(os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), LINH, LINH.split('\n', 1)[0])
append(os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), DESE, DESE.split('\n')[2])
append(ATLAS, ATL, ATL.split('\n')[2])
append(HAJA, HL, HL.split('\n', 1)[0])   # v386: a superficie nova da linhagem (append datado curto; CRLF do arquivo respeitado)
# o marcador de idempotencia de cada bloco: um prefixo ESTAVEL -- a missao e o central-de-patentes-estado sao blocos de UMA linha cujo texto traz campos
# lidos ao vivo (a custodia vem do git da Central): o marcador e' so a data, a versao e o sha16 (T.marca_*); os demais levam <!-- v386_selada --> na 1a linha
for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),
                           ('verbo-selecao-da-acao-05out.md', T.topico_verbo(V), None), ('ramo-b-reaberto-05out.md', T.topico_ramo_b(V), None),
                           ('v384-pilar-quantico-gpu-02out.md', T.topico_pilar(V), None)):
    if marca is not None:
        assert bloco.startswith(marca), ('o bloco nao comeca pelo seu marcador estavel', nome)
    append(os.path.join(UMEM, nome), bloco, marca or bloco.split('\n', 1)[0])

# ---- MEMORY.md (+ MEMORY_2.md)
idx = alvo(os.path.join(UMEM, 'MEMORY.md')); idx2 = alvo(os.path.join(UMEM, 'MEMORY_2.md'))
raw = open(idx, 'rb').read(); raw2 = open(idx2, 'rb').read()
assert b'\r\n' not in raw, 'MEMORY.md com CRLF: o molde espera LF'
lines = raw.decode('utf-8').split('\n')
MARCA = '**v386 SELADA %s `%s`' % (V['data'][:5], V['s16'])
FOLGA_HANDOFF = len((T.linha_handoff(V) + '\n').encode('utf-8'))
MARCA_PILAR = (' · **v386 (%s): o marcador agora é `%s`**' % (V['data'][:5], os.path.join(A.PK, '.servidor_parado_pelo_rito')))
if any(MARCA in l for l in lines):
    print('JA ESTA (idempotente): MEMORY.md')
else:
    mov = []
    for i in range(1, len(lines)):
        if lines[i - 1].startswith('<!-- IALD_') and lines[i].startswith('- ') and 'movidas verbatim ao MEMORY_2' not in lines[i]:
            mov.append((i, lines[i - 1], lines[i]))
    for i, _m, _l in reversed(mov):
        del lines[i]
    if mov:
        lines.append('- [%d linhas da frente Codex movidas verbatim ao MEMORY_2 em %s pela regra dos dois arquivos](MEMORY_2.md) — texto integral no fim do MEMORY_2.md; os marcadores ficam aqui' % (len(mov), V['data'][:5]))
    k = [i for i, l in enumerate(lines) if '(missao-ultima-flag-um-py.md) — ' in l]; assert len(k) == 1, len(k)
    a, b = lines[k[0]].split('(missao-ultima-flag-um-py.md) — ', 1)
    lines[k[0]] = a + '(missao-ultima-flag-um-py.md) — ' + T.marca_missao(V) + b
    assert MARCA in lines[k[0]]
    kp = [i for i, l in enumerate(lines) if '(v384-pilar-quantico-gpu-02out.md) — ' in l]; assert len(kp) == 1, ('linha do pilar', len(kp))
    MARCA_PILAR_CURTA = '`scratchpad\\v386\\pacote\\.servidor_parado_pelo_rito`'   # a forma curta que a compactacao (d) poe na linha; se esta, a longa nao entra
    if MARCA_PILAR not in lines[kp[0]] and MARCA_PILAR_CURTA not in lines[kp[0]]:
        lines[kp[0]] = lines[kp[0]] + MARCA_PILAR
    novo = '\n'.join(lines).encode('utf-8')
    if len(novo) + FOLGA_HANDOFF > LIMITE_INDICE:
        print('SUPERFICIES RECUSADAS -- nada foi escrito: o MEMORY.md ficaria com %d B e a linha do handoff (%d B) passaria de %d B. '
              'Rode antes: python compactar_memory_para_v386.py --gravar (regra dos dois arquivos: o excesso vai VERBATIM ao MEMORY_2).' % (len(novo), FOLGA_HANDOFF, LIMITE_INDICE)); sys.exit(3)
    if mov:
        nl2 = nl_de(raw2)
        bloco2 = ['', '', '## %s — linhas movidas do MEMORY.md (regra dos dois arquivos), VERBATIM, com o marcador de origem ao lado' % V['data']]
        for _i, m, l in mov:
            bloco2 += ['', m, l]
        n2 = raw2 + nl2.join(bloco2).encode('utf-8') + nl2.encode()
        corrente(idx2); PLANO[idx2]['novo'] = n2; PLANO[idx2]['o_que'].append('%d linha(s) integral(is) da frente Codex' % len(mov))
    corrente(idx); PLANO[idx]['novo'] = novo; PLANO[idx]['o_que'].append('marcador v386 na missao; marca do pilar; %d linha(s) movida(s); %d B (+%d da linha do handoff depois)' % (len(mov), len(novo), FOLGA_HANDOFF))


def livre(base):
    n = 1; c = base
    while os.path.exists(c) or c in USADOS:
        n += 1; c = '%s_%d' % (base, n)
    USADOS.add(c); return c


USADOS = set(); TAREFAS = []
for p, d in PLANO.items():
    if d['novo'] == d['raw']:
        continue
    if p == idx:
        assert len(d['novo']) > len(d['raw']) or (idx2 in PLANO and len(PLANO[idx2]['novo']) > len(PLANO[idx2]['raw'])), 'MEMORY.md encolheria sem o MEMORY_2 crescer'
    else:
        assert len(d['novo']) > len(d['raw']) and d['novo'].startswith(d['raw']), 'o conteudo novo de %s nao e append puro (nada foi escrito)' % p
    TAREFAS.append((p, d, livre(p + '.bak_' + STAMP + MARCA_BAK), livre(p + '.tmp' + MARCA_BAK + '_' + STAMP)))
if not TAREFAS:
    print('NADA A GRAVAR: todas as superficies ja tem a v386 (idempotente)'); sys.exit(0)
print('PLANO (fase 1, conferido ANTES da primeira escrita): %d alvo(s)%s' % (len(TAREFAS), V['sint']))
for p, d, bak, tmp in TAREFAS:
    guarda(bak); guarda(tmp); guarda(p)
    assert open(p, 'rb').read() == d['raw'], '%s mudou desde a leitura -- nada foi escrito' % p
    print('   %-48s %10s -> %10s B  | %s' % (os.path.basename(p), format(len(d['raw']), ','), format(len(d['novo']), ','), '; '.join(d['o_que'])))
FEITOS = []; tmp_atual = None
try:
    for p, d, bak, tmp in TAREFAS:
        with open(bak, 'wb') as f:
            f.write(d['raw'])
        assert open(bak, 'rb').read() == d['raw'], 'backup de bytes falhou: %s' % bak
        tmp_atual = tmp
        with open(tmp, 'wb') as f:
            f.write(d['novo'])
        assert os.path.getsize(tmp) == len(d['novo'])
        assert open(p, 'rb').read() == d['raw'], 'o arquivo mudou entre a leitura e a troca -- nao substituo: %s' % p
        os.replace(tmp, p); tmp_atual = None
        assert open(p, 'rb').read() == d['novo']
        FEITOS.append(p); print('OK', os.path.basename(p), format(len(d['raw']), ','), '->', format(os.path.getsize(p), ','))
except Exception as e:
    if tmp_atual and os.path.exists(tmp_atual):
        os.remove(tmp_atual)
    print('PARADA NAS SUPERFICIES: %r' % e)
    print('  gravados: %s' % [os.path.basename(x) for x in FEITOS])
    print('  NAO gravados: %s' % [os.path.basename(t[0]) for t in TAREFAS if t[0] not in FEITOS])
    print('  backups de bytes ao lado de cada arquivo tocado; RERODAR e idempotente; nada foi restaurado.')
    sys.exit(1)
print('SUPERFICIES v386: %d alvo(s) gravado(s); MEMORY.md %d B (limite %d, com %d B de folga para a linha do handoff)' % (len(FEITOS), os.path.getsize(idx), LIMITE_INDICE, FOLGA_HANDOFF))
