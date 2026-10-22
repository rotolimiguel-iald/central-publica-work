# -*- coding: utf-8 -*-
# Registro da v387 SELADA (molde: superficies_v386.py, enxuto): diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), o CLAUDE.md da
# Haja_Luz (append datado curto), as memorias-topico (missao, central, fase9, fase8, tres-testes, pos-dicao, proximo-passo) e o indice MEMORY.md: as linhas que a v387
# tornou VELHAS (a retomada, a Fase 9 «V1 ainda NAO congelado», a Fase 8, a missao) vao VERBATIM ao MEMORY_2.md (regra dos dois arquivos: nada se corta) e no lugar
# fica o gancho curto atualizado; + a linha do handoff v387. Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup387);
# temporario -> conferir tamanho -> substituir; append puro nos demais; idempotente pelo marcador de cada bloco; fim de linha do arquivo respeitado.
# GUARDA: so grava se a leitura (leitura_v387.ler) nao tiver problema. Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado).
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v387, textos_v387 as T
NOS = leitura_v387.NOS
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
REMAP = sys.argv[sys.argv.index('--copias') + 1] if '--copias' in sys.argv else None
STAMP = time.strftime('%Y%m%d_%H%M%S'); MARCA_BAK = '_sup387'; LIMITE = 24000
alvo = lambda p: os.path.join(REMAP, os.path.basename(p)) if REMAP else p


def nl_de(raw):
    return '\r\n' if raw.count(b'\r\n') > raw.count(b'\n') // 2 else '\n'


PLANO = {}


def corrente(p):
    if p not in PLANO:
        raw = open(p, 'rb').read(); PLANO[p] = {'raw': raw, 'novo': raw, 'o_que': []}
    return PLANO[p]['novo']


def append(p, bloco, marcador):
    p = alvo(p); cur = corrente(p)
    if marcador.encode('utf-8') in cur.replace(b'\r\n', b'\n'):
        print('JA ESTA (idempotente):', os.path.basename(p)); return
    nlc = nl_de(cur)
    sep = (nlc * 2) if cur.endswith(nlc.encode()) else (nlc * 3)
    PLANO[p]['novo'] = cur + sep.encode() + bloco.replace('\r\n', '\n').replace('\n', nlc).encode('utf-8') + nlc.encode()
    PLANO[p]['o_que'].append('append (%s)' % ('CRLF' if nlc == '\r\n' else 'LF'))


V, PROB = leitura_v387.ler()
if PROB:
    print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
for p, bloco, marca in ((os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), T.linhagem(V), None), (os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), T.desenho(V), '<!-- adendo_v387_selada -->'),
                        (ATLAS, T.atlas(V), '<!-- atlas_v387_selada -->'), (HAJA, T.haja_luz(V), None)):
    append(p, bloco, marca or bloco.split('\n', 1)[0])
for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),
                           ('fase9-razao-de-hubble-05out.md', T.topico_fase9(V), None), ('fase8-universo-primordial-05out.md', T.topico_fase8(V), None),
                           ('tres-testes-de-estresse-conjuntos-05out.md', T.topico_tres(V), None), ('pos-dicao-nao-e-prova-diabolica-05out.md', T.topico_posdicao(V), None),
                           ('proximo-passo-06out.md', "<!-- v387_selada -->\n**%s — FEITO nesta sessão:** passos A (V1 da Fase 9 `%s`), B (canal N_eff + V1 da Fase 8 `%s`) , C (v387 `%s` selada por decisão do operador via c1) e D (auditoria leve da ORDEM 018, mapa seq 632). "
                            "Resta o que é do operador (fontes por hash, abrir, qual spec F9, ratificar D1–D11/D-A..D-H, nomes, β escalar → v388, custódia, commit/push). Ver `handoff-v387-custodia.md`."
                            % (V['data'], V['V1']['fase9']['spec16'], V['V1']['fase8']['spec16'], V['s16']), None)):
    append(os.path.join(UMEM, nome), bloco, marca or '<!-- v387_selada -->\n' + bloco.split('\n', 2)[1][:60] if bloco.startswith('<!--') else (marca or bloco.split('\n', 1)[0]))
# ---- MEMORY.md (+ MEMORY_2.md): as linhas velhas VERBATIM ao MEMORY_2; no lugar, o gancho curto
idx = alvo(os.path.join(UMEM, 'MEMORY.md')); idx2 = alvo(os.path.join(UMEM, 'MEMORY_2.md'))
raw = open(idx, 'rb').read(); raw2 = open(idx2, 'rb').read()
assert b'\r\n' not in raw, 'MEMORY.md com CRLF: o molde espera LF'
lines = raw.decode('utf-8').split('\n')
MARCA = '**v387 SELADA %s `%s`' % (V['data'][:5], V['s16'])
TROCAS = [  # (o link que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2
    ('(handoff-sessao-nova-06out.md)', "- [HANDOFF SESSÃO NOVA (06/10): A–D FEITOS; v387 SELADA](handoff-sessao-nova-06out.md) · [β escalar ≥ β₀ → v388](beta-escalar-limitado-inferiormente-06out.md) — v387 `%s`; ver [handoff v387](handoff-v387-custodia.md) · íntegra anterior no MEMORY_2.md (movida %s)" % (V['s16'], V['data'][:5])),
    ('(fase9-razao-de-hubble-05out.md)', "- [Fase 9 — a razão de Hubble (05/10)](fase9-razao-de-hubble-05out.md) — **V1 CONGELADO 06/10 (Bancada, spec `%s`), lido pela v387; poder %sσ só σ; abrir = operador (D-H)** · íntegra anterior no MEMORY_2.md (movida %s)" % (V['V1']['fase9']['spec16'], T._f(V['hr_tr'].get('poder_previo_primario')), V['data'][:5])),
    ('(fase8-universo-primordial-05out.md)', "- [Fase 8 — β na era da radiação (05/10)](fase8-universo-primordial-05out.md) — **canal N_eff na Bancada + V1 CONGELADO 06/10 (spec `%s`), lido pela v387; poder hoje %sσ (sem poder, dito)** · íntegra anterior no MEMORY_2.md (movida %s)" % (V['V1']['fase8']['spec16'], T._f(V['pr_tr'].get('poder_melhor_independente')), V['data'][:5])),
    ('(missao-ultima-flag-um-py.md)', "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + T.marca_missao(V) + "íntegra anterior (v386–v375) no MEMORY_2.md (movida %s)" % V['data'][:5]),
]
if any(MARCA in l for l in lines):
    print('JA ESTA (idempotente): MEMORY.md')
else:
    movidas = []
    for chave, nova in TROCAS:
        k = [i for i, l in enumerate(lines) if chave in l and l.startswith('- [')]
        assert len(k) == 1, ('linha do indice', chave, len(k))
        movidas.append(lines[k[0]]); lines[k[0]] = nova
    hl = T.linha_handoff(V)
    kh = [i for i, l in enumerate(lines) if '(handoff-v386-custodia.md)' in l and l.startswith('- [')]
    assert len(kh) == 1
    lines.insert(kh[0], hl)
    novo = '\n'.join(lines).encode('utf-8')
    if len(novo) > LIMITE:
        print('SUPERFICIES RECUSADAS -- o MEMORY.md ficaria com %d B (> %d): nada foi escrito' % (len(novo), LIMITE)); sys.exit(3)
    nl2 = nl_de(raw2)
    bloco2 = ['', '', '## %s — linhas do MEMORY.md tornadas velhas pela v387, VERBATIM (regra dos dois arquivos)' % V['data']] + sum((['', '<!-- movida %s (v387) -->' % V['data'][:5], l] for l in movidas), [])
    corrente(idx2); PLANO[idx2]['novo'] = raw2 + nl2.join(bloco2).encode('utf-8') + nl2.encode(); PLANO[idx2]['o_que'].append('%d linha(s) integral(is) do indice' % len(movidas))
    corrente(idx); PLANO[idx]['novo'] = novo; PLANO[idx]['o_que'].append('%d gancho(s) atualizados + a linha do handoff; %d B' % (len(movidas), len(novo)))


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
        assert idx2 in PLANO and len(PLANO[idx2]['novo']) > len(PLANO[idx2]['raw']), 'MEMORY.md mudaria sem o MEMORY_2 crescer'
    else:
        assert len(d['novo']) > len(d['raw']) and d['novo'].startswith(d['raw']), 'o conteudo novo de %s nao e append puro (nada foi escrito)' % p
    TAREFAS.append((p, d, livre(p + '.bak_' + STAMP + MARCA_BAK), livre(p + '.tmp' + MARCA_BAK + '_' + STAMP)))
if not TAREFAS:
    print('NADA A GRAVAR: todas as superficies ja tem a v387 (idempotente)'); sys.exit(0)
print('PLANO (fase 1, conferido ANTES da primeira escrita): %d alvo(s)%s' % (len(TAREFAS), ' [COPIAS: %s]' % REMAP if REMAP else ''))
for p, d, bak, tmp in TAREFAS:
    if REMAP:
        assert os.path.realpath(p).lower().startswith(os.path.realpath(REMAP).lower() + os.sep), 'ESCRITA FORA DAS COPIAS: %s' % p
    assert open(p, 'rb').read() == d['raw'], '%s mudou desde a leitura -- nada foi escrito' % p
    print('   %-48s %12s -> %12s B  | %s' % (os.path.basename(p), format(len(d['raw']), ','), format(len(d['novo']), ','), '; '.join(d['o_que'])))
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
        assert open(p, 'rb').read() == d['raw'], 'o arquivo mudou entre a leitura e a troca: %s' % p
        os.replace(tmp, p); tmp_atual = None
        assert open(p, 'rb').read() == d['novo']
        FEITOS.append(p); print('OK', os.path.basename(p), format(len(d['raw']), ','), '->', format(os.path.getsize(p), ','))
except Exception as e:
    if tmp_atual and os.path.exists(tmp_atual):
        os.remove(tmp_atual)
    print('PARADA NAS SUPERFICIES: %r' % e); print('  gravados: %s' % [os.path.basename(x) for x in FEITOS])
    print('  backups de bytes ao lado de cada arquivo tocado; RERODAR e idempotente; nada foi restaurado.'); sys.exit(1)
print('SUPERFICIES v387: %d alvo(s) gravado(s); MEMORY.md %d B (limite %d)' % (len(FEITOS), os.path.getsize(idx), LIMITE))
