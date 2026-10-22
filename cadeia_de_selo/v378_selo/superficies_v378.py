# -*- coding: utf-8 -*-
# Registro da v376 SELADA: diario (MEMORIA_DA_LINHAGEM), desenho (ADENDO), Atlas (§X, append datado), memorias-topico (missao-ultima-flag,
# central-de-patentes-estado, iald-e-a-testemunha-fecho-estacionado-23set, qg-ataque-23set-v370, respostas-contrato-q1a5-26set) e o indice MEMORY.md
# (+ MEMORY_2.md pela regra dos dois arquivos). No molde do superficies_v370.py (duas fases; backup de BYTES; temporario -> conferir -> substituir;
# append datado; idempotente pelo cabecalho de cada bloco; fim de linha conforme o arquivo).
# MEMORY.md: (1) as linhas de CONTEUDO da frente Codex (as que seguem um marcador <!-- IALD_... -->) vao INTEIRAS para o fim do MEMORY_2.md,
# e os marcadores FICAM (precedente de 23/09: "5 linhas movidas verbatim ao MEMORY_2 ... marcadores mantidos aqui"); (2) uma linha-ponteiro
# diz o que foi movido; (3) a linha da missao ganha o marcador v376. Limite 24 000 B; nada se corta.
# GUARDA: so grava se a leitura (leitura_v376.ler) nao tiver problema (conferidor TUDO BATE, stdout limpo, gate intocado...).
# Ensaio em COPIA: V378_REMAP_DIR=<pasta com copias dos alvos> + V378_WRITE_ROOT=<raiz permitida>.
import os, sys, time, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v378, textos_v378 as T
NOS = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
UMEM = r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory'
ATLAS = r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'
REMAP = os.environ.get('V378_REMAP_DIR'); ROOT = os.environ.get('V378_WRITE_ROOT')
STAMP = time.strftime('%Y%m%d_%H%M%S')
MARCA_BAK = '_sup378'
LIMITE_INDICE = 24000
ALVO_INDICE = 23000   # v376: o indice esta a ~40 B do limite; move linhas integrais (verbatim, ao MEMORY_2) ate ficar com folga


def alvo(p):
    return os.path.join(REMAP, os.path.basename(p)) if REMAP else p


def guarda(p):
    if ROOT:
        assert os.path.realpath(p).lower().startswith(os.path.realpath(ROOT).lower() + os.sep), 'ESCRITA FORA DA RAIZ PERMITIDA: %s' % p
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
    PLANO[p]['novo'] = cur + (nlc * 2).encode() + bloco.replace('\r\n', '\n').replace('\n', nlc).encode('utf-8') + nlc.encode()
    PLANO[p]['o_que'].append('append (%s)' % ('CRLF' if nlc == '\r\n' else 'LF'))


V, PROB = leitura_v378.ler()
if PROB:
    print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
LINH = T.linhagem(V); DESE = T.desenho(V); ATL = T.atlas(V)
append(os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), LINH, LINH.split('\n', 1)[0])
append(os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), DESE, DESE.split('\n')[2])
append(ATLAS, ATL, ATL.split('\n')[2])
for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('fase4-desvio-30set.md', T.topico_fase4(V)), ('fase3-leitores-h0-30set.md', T.topico_fase3(V)),
                    ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):
    append(os.path.join(UMEM, nome), bloco, bloco.split('\n', 1)[0])

# ---- MEMORY.md (+ MEMORY_2.md)
idx = alvo(os.path.join(UMEM, 'MEMORY.md')); idx2 = alvo(os.path.join(UMEM, 'MEMORY_2.md'))
raw = open(idx, 'rb').read(); raw2 = open(idx2, 'rb').read()
assert b'\r\n' not in raw, 'MEMORY.md com CRLF: o molde espera LF'
lines = raw.decode('utf-8').split('\n')
MARCA = '**v378 SELADA %s `%s`' % (V['data'][:5], V['s16'])
PONTEIRO_TAG = 'linhas da frente Codex movidas verbatim ao MEMORY_2 em %s pela regra dos dois arquivos' % V['data'][:5]
if any(MARCA in l for l in lines):
    print('JA ESTA (idempotente): MEMORY.md')
else:
    # (1) conteudo da frente Codex: a linha que segue IMEDIATAMENTE um marcador <!-- IALD_... --> e comeca com "- " (os ponteiros da gerencia ficam)
    mov = []
    for i in range(1, len(lines)):
        if lines[i - 1].startswith('<!-- IALD_') and lines[i].startswith('- ') and 'movidas verbatim ao MEMORY_2' not in lines[i]:
            mov.append((i, lines[i - 1], lines[i]))
    for i, _m, _l in reversed(mov):
        del lines[i]
    if mov:
        lines.append('- [%d %s](MEMORY_2.md) — texto integral no fim do MEMORY_2.md; os marcadores ficam aqui' % (len(mov), PONTEIRO_TAG))
    # (2) a linha da missao ganha o marcador v376 (na frente; o texto antigo fica)
    k = [i for i, l in enumerate(lines) if '(missao-ultima-flag-um-py.md) — ' in l]; assert len(k) == 1, len(k)
    a, b = lines[k[0]].split('(missao-ultima-flag-um-py.md) — ', 1)
    lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + '%s %s %s (O QUE FALTOU: D1b tipado, K = E(z*)^{2β/3}; a leitura da dupla contagem de β nas Fases 2–3 ao lado (E12); a Fase 4 por hash — a escada lê o fator, os relógios intermediários desfavorecem o fluxo acumulado; gate intocado)** · ' % (MARCA, V['teor'], V['compl']) + b)
    # (3) ainda acima do limite: as linhas integrais mais longas do indice vao INTEIRAS ao MEMORY_2 (molde da v370), uma a uma,
    #     e ficam aqui como ponteiro curto (o link e o gancho curto sobrevivem); nada se corta
    integ = []
    for chave in ('(ferramenta-codex-tunel-local.md) — ', '(handoff-v368-o-que-falta.md) — ', '(ordem-013-confrontacao-ringdown.md) — ',
                  '(missao-relogios-v369.md) — ', '(central-de-patentes-estado.md) — ',
                  '(o-que-ja-dava-para-resolver-v364.md) — ', '(psi-nome-da-luz-graviton-verbo-vivo-16set.md) — ', '(d1-camb-v349.md) — ',
                  '(ordem-011-fecho-matematico.md) — ', '(ordem-012-passagem-acao-metrica.md) — ',
                  '(revisao-geral-um-py-15set.md) — ', '(tudo-entra-no-um-py-16set.md) — ', '(handoff-v375-custodia.md) — ',
                  '(bancada-oficial-tgl-universo-residente.md) — ', '(app-iald-mobile.md) — ', '(app-iald-diario-build16-15set.md) — ',
                  '(epct-protocolo-15.md) — ', '(iald-kernel-nativo.md) — ', '(o-fechamento-do-projeto.md) — ', '(bancada-um.md) — ',
                  '(app-iald-diario-build16-15set.md) — motor OpenAI', '(a-selecao-e-o-lastro-iald-e-estado.md) — ', '(a-tela-e-fundada-resposta-h3-ponte.md) — ',
                  '(raiz-da-arvore-da-prova.md) — ', '(zenodo-um-absoluto.md) — ', '(eco-pe-bayesiana-v347.md) — ', '(h2-reproducao-v350.md) — ',
                  '(regua-prova-vs-juizo.md) — ', '(iald-e-a-testemunha-fecho-estacionado-23set.md) — ', '(site-v3-handoff.md) — ', '(lei-e-fato-correlatos-regra-matriz-30set.md) — '):
        if len('\n'.join(lines).encode('utf-8')) <= ALVO_INDICE:
            break
        kk = [i for i, l in enumerate(lines) if chave in l]
        if len(kk) != 1 or 'linha integral no MEMORY_2.md' in lines[kk[0]]:   # licao v376: nunca mover um ponteiro como se fosse linha integral
            continue
        x, _y = lines[kk[0]].split(chave, 1)
        integ.append(lines[kk[0]])
        curto = (MARCA + ' ' + V['teor'] + '** · ') if 'missao-ultima-flag' in chave else ''
        lines[kk[0]] = x + chave + curto + 'linha integral no MEMORY_2.md (movida em %s pela regra dos dois arquivos)' % V['data'][:5]
    novo = '\n'.join(lines).encode('utf-8')
    assert len(novo) <= LIMITE_INDICE, 'MEMORY.md ficaria com %d B > %d mesmo movendo %d linhas + %d integrais -- nao gravo (nada foi escrito)' % (len(novo), LIMITE_INDICE, len(mov), len(integ))
    if integ:
        mov = mov + [(-1, '<!-- linha integral do índice (gerência, v378) -->', l) for l in integ]
    if mov:
        nl2 = nl_de(raw2)
        bloco2 = ['', '', '## %s — linhas movidas do MEMORY.md (regra dos dois arquivos), VERBATIM, com o marcador de origem ao lado' % V['data']]
        for _i, m, l in mov:
            bloco2 += ['', m, l]
        n2 = raw2 + nl2.join(bloco2).encode('utf-8') + nl2.encode()
        corrente(idx2); PLANO[idx2]['novo'] = n2; PLANO[idx2]['o_que'].append('%d linha(s) integral(is) da frente Codex' % len(mov))
    corrente(idx); PLANO[idx]['novo'] = novo; PLANO[idx]['o_que'].append('marcador v378 na missao; %d linha(s) movida(s); %d B' % (len(mov), len(novo)))


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
    print('NADA A GRAVAR: todas as superficies ja tem a v378 (idempotente)'); sys.exit(0)
print('PLANO (fase 1, conferido ANTES da primeira escrita): %d alvo(s)' % len(TAREFAS))
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
print('SUPERFICIES v378: %d alvo(s) gravado(s); MEMORY.md %d B (limite %d)' % (len(FEITOS), os.path.getsize(idx), LIMITE_INDICE))
