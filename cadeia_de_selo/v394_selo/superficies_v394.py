# -*- coding: utf-8 -*-
# Registro da v394 SELADA nas superficies de memoria (molde: superficies_v393.py), pela regra da linhagem completa.
# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz, as memorias-topico (missao, central, estatuto, e o topico NOVO da v394),
# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V394_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.
# SEM erratas inline nesta versao (erratas novas, se houver, vao DENTRO do bloco datado). A funcao inserir_ao_lado fica disponivel (nao e' chamada).
# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup394); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;
# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.
# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas; se passar de 195 linhas, COMPACTA corridas de ganchos antigos (linhas que ja sao ponteiros ao
# MEMORY_2.md) num ponteiro unico, com as linhas movidas VERBATIM ao MEMORY_2.md (regra dos dois arquivos).
# Rotulos desta versao (no molde v393 ficaram uma versao atras no codigo): MARCA_BAK = _sup394 e a variavel de ambiente V394_AVISO_REIVINDICACAO (a mesma que a cadeia usa).
import os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v394, textos_v394 as T
from guarda_p18_v394 import violacoes
NOS = leitura_v394.NOS
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")
ATLAS = os.path.join(ATLD, "TGL_ATLAS.md"); COREM = os.path.join(ATLD, "TGL_CORE_MEMORY.md")
HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
AVISO = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "AVISO_GERENCIA.md")
REMAP = sys.argv[sys.argv.index('--copias') + 1] if '--copias' in sys.argv else None
STAMP = time.strftime('%Y%m%d_%H%M%S'); MARCA_BAK = '_sup394'; LIMITE = 24000; LIMITE_LINHAS = 195
alvo = lambda p: os.path.join(REMAP, os.path.basename(p)) if REMAP else p
VIOLACOES = []


def guarda(texto, onde):
    v = violacoes(texto)
    if v:
        VIOLACOES.append((onde, v[:3]))


def nl_de(raw):
    return '\r\n' if raw.count(b'\r\n') > raw.count(b'\n') // 2 else '\n'


PLANO = {}


def corrente(p):
    if p not in PLANO:
        ex = os.path.exists(p); raw = open(p, 'rb').read() if ex else b''
        PLANO[p] = {'raw': raw, 'novo': raw, 'existia': ex, 'o_que': [], 'blocos': [], 'apendou': False}
    return PLANO[p]['novo']


def append(p, bloco, marcador):
    p = alvo(p); cur = corrente(p)
    guarda(bloco, os.path.basename(p) + ' (append)')
    if marcador.encode('utf-8') in cur.replace(b'\r\n', b'\n'):
        print('JA ESTA (idempotente):', os.path.basename(p)); return
    nlc = nl_de(cur) if cur else '\n'
    sep = b'' if not cur else ((nlc * 2) if cur.endswith(nlc.encode()) else (nlc * 3)).encode()
    PLANO[p]['novo'] = cur + sep + bloco.replace('\r\n', '\n').replace('\n', nlc).encode('utf-8') + nlc.encode()
    PLANO[p]['apendou'] = True
    PLANO[p]['o_que'].append('arquivo novo' if not PLANO[p]['existia'] else 'append (%s)' % ('CRLF' if nlc == '\r\n' else 'LF'))


def inserir_ao_lado(p, rxs, texto, marca, minimo=1, exato=None, juntar=False):
    """ERRATA AO LADO: insere `texto` (uma linha) logo depois de cada linha que casa com algum rx, com linha em branco antes e depois. A linha antiga fica. Idempotente: se a proxima linha
    nao vazia ja traz `marca`, pula. Zero ocorrencias (menos que `minimo`, ou != `exato`) = recusa. juntar=True: linhas casadas em sequencia (ate 2 de distancia) recebem uma errata so', depois da ultima."""
    p = alvo(p); cur = corrente(p); d = PLANO[p]
    assert not d['apendou'], 'a errata inline vem ANTES de qualquer append no mesmo arquivo: ' + p
    guarda(texto, os.path.basename(p) + ' (errata)')
    assert marca in texto
    nlc = nl_de(cur); eol = nlc
    txt = cur.decode('utf-8'); linhas = re.findall(r'[^\n]*\n|[^\n]+\Z', txt); assert ''.join(linhas) == txt
    hits = [i for i, l in enumerate(linhas) if marca not in l and any(rx.search(l) for rx in rxs)]
    if juntar:
        g = []
        for i in hits:
            if g and i - g[-1][-1] <= 2:
                g[-1].append(i)
            else:
                g.append([i])
        hits = [x[-1] for x in g]
    if len(hits) < minimo or (exato is not None and len(hits) != exato):
        print('ERRATA RECUSADA: %s: %d ocorrencia(s) (esperado %s)' % (os.path.basename(p), len(hits), exato if exato is not None else '>= %d' % minimo)); sys.exit(5)

    def ja_tem(i):
        j = i + 1
        while j < len(linhas) and linhas[j].strip() == '':
            j += 1
        return j < len(linhas) and marca in linhas[j]
    novos = [i for i in hits if not ja_tem(i)]
    if not novos:
        print('JA ESTA (idempotente): erratas %s em %s (%d ocorrencia(s))' % (marca, os.path.basename(p), len(hits))); return
    saida = []; blocos = []
    for i, l in enumerate(linhas):
        saida.append(l)
        if i in novos:
            assert l.endswith('\n'), 'linha casada sem fim de linha (ultima do arquivo)'
            prox_branca = (i + 1 >= len(linhas)) or linhas[i + 1].strip() == ''
            blk = ('' if l.strip() == '' else eol) + texto + eol + ('' if prox_branca else eol)
            saida.append(blk); blocos.append(blk)
    mid = ''.join(saida); rec = mid
    for b in blocos:
        rec = rec.replace(b, '', 1)
    assert rec == txt, 'tirar as erratas nao devolve o original'
    d['novo'] = mid.encode('utf-8'); d['blocos'] += blocos
    d['o_que'].append('%d errata(s) ao lado [%s]' % (len(novos), marca))
    print('  erratas %s em %s: %d ocorrencia(s), %d nova(s) (linhas %s)' % (marca, os.path.basename(p), len(hits), len(novos), [i + 1 for i in novos][:12]))


V, PROB = leitura_v394.ler()
if PROB:
    print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
# ---- 1. (sem erratas inline nesta versao: erratas novas, se houver, vao dentro do bloco datado da linhagem, do Atlas, do core e do topico novo)
# ---- 2. os appends datados
for p, bloco, marca in ((os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), T.linhagem(V), '<!-- linhagem_v394_selada -->'), (os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), T.desenho(V), '<!-- adendo_v394_selada -->'),
                        (ATLAS, T.atlas(V), '<!-- atlas_v394_selada -->'), (COREM, T.core_memory(V), '<!-- core_v394_selada -->'), (HAJA, T.haja_luz(V), '<!-- haja_luz_v394_selada -->')):
    append(p, bloco, marca or bloco.split('\n', 1)[0])
for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.id_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.id_central(V)),
                           ('estatuto-da-prova-07out.md', T.topico_estatuto(V), '<!-- v394_selada -->'), (T.TOPICO_NOVO, T.topico_novo(V), '# v394 SELADA (')):
    append(os.path.join(UMEM, nome), bloco, marca)
REIV = os.environ.get('V394_AVISO_REIVINDICACAO', '').strip()
if REIV:
    append(AVISO, T.aviso(V, REIV), '<!-- aviso_v394_selada -->')
else:
    print(T.aviso_pulado())
# ---- 3. MEMORY.md (+ MEMORY_2.md): as linhas velhas VERBATIM ao MEMORY_2; no lugar, o gancho curto
idx = alvo(os.path.join(UMEM, 'MEMORY.md')); idx2 = alvo(os.path.join(UMEM, 'MEMORY_2.md'))
raw = open(idx, 'rb').read(); raw2 = open(idx2, 'rb').read()
assert b'\r\n' not in raw, 'MEMORY.md com CRLF: o molde espera LF'
lines = raw.decode('utf-8').split('\n')
TROCAS = [  # (o trecho que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2
    ('(missao-ultima-flag-um-py.md)', "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + T.marca_missao(V) + "íntegra anterior no MEMORY_2.md (movida %s)" % V['data'][:5]),
]
if any(('v394 SELADA' in l and V['s16'] in l) for l in lines):
    print('JA ESTA (idempotente): MEMORY.md')
else:
    movidas = []
    for chave, nova in TROCAS:
        guarda(nova, 'MEMORY.md (gancho)')
        k = [i for i, l in enumerate(lines) if chave in l and l.startswith('- [')]
        assert len(k) == 1, ('linha do indice', chave, len(k))
        movidas.append(lines[k[0]]); lines[k[0]] = nova
    hl = T.linha_handoff(V); guarda(hl, 'MEMORY.md (handoff)')
    kh = [i for i, l in enumerate(lines) if '(handoff-v393-custodia.md)' in l and l.startswith('- [HANDOFF v393')]
    assert len(kh) == 1, ('linha do handoff v393', len(kh))
    lines.insert(kh[0], hl)
    # compactacao: se o indice passar do limite de linhas, junta corridas de ganchos antigos (linhas que ja sao ponteiros ao MEMORY_2.md) num ponteiro; as linhas vao VERBATIM ao MEMORY_2.md
    gancho = lambda l: l.startswith('- [') and 'MEMORY_2.md (' in l and '**' not in l and 'linhas íntegras' not in l and 'handoff-v39' not in l and 'Ganchos antigos' not in l
    ALVO = LIMITE_LINHAS - 3
    if len(lines) - 1 > ALVO:
        corridas = []; k = 0
        while k < len(lines):
            if gancho(lines[k]):
                k2 = k
                while k2 + 1 < len(lines) and gancho(lines[k2 + 1]):
                    k2 += 1
                if k2 > k:
                    corridas.append((k, k2))
                k = k2 + 1
            else:
                k += 1
        escolhidas = []; falta = (len(lines) - 1) - ALVO
        for a_, b_ in sorted(corridas, key=lambda ab: -(ab[1] - ab[0])):
            if falta <= 0:
                break
            escolhidas.append((a_, b_)); falta -= (b_ - a_)
        if falta > 0:
            print('SUPERFICIES RECUSADAS -- o MEMORY.md nao pode ser compactado o bastante (faltam %d linhas): nada foi escrito' % falta); sys.exit(3)
        for a_, b_ in sorted(escolhidas, reverse=True):
            movidas.extend(lines[a_:b_ + 1])
            ptr = '- [Ganchos antigos consolidados (%d)](MEMORY_2.md) — %d linhas íntegras no MEMORY_2.md (movidas %s pela regra dos dois arquivos)' % (b_ - a_ + 1, b_ - a_ + 1, V['data'][:5])
            guarda(ptr, 'MEMORY.md (ponteiro)'); lines[a_:b_ + 1] = [ptr]
            print('  MEMORY.md compactado: %d linhas de ganchos antigos -> 1 ponteiro (verbatim no MEMORY_2)' % (b_ - a_ + 1))
    novo = '\n'.join(lines).encode('utf-8')
    nlin = novo.count(b'\n')
    if len(novo) > LIMITE or nlin > LIMITE_LINHAS:
        print('SUPERFICIES RECUSADAS -- o MEMORY.md ficaria com %d B e %d linhas (limites %d B e %d linhas): nada foi escrito' % (len(novo), nlin, LIMITE, LIMITE_LINHAS)); sys.exit(3)
    nl2 = nl_de(raw2)
    bloco2 = ['', '', '## %s — linhas do MEMORY.md tornadas velhas pela v394, VERBATIM (regra dos dois arquivos)' % V['data']] + sum((['', '<!-- movida %s (v394) -->' % V['data'][:5], l] for l in movidas), [])
    corrente(idx2); PLANO[idx2]['novo'] = raw2 + nl2.join(bloco2).encode('utf-8') + nl2.encode(); PLANO[idx2]['o_que'].append('%d linha(s) integral(is) do indice' % len(movidas)); PLANO[idx2]['apendou'] = True
    corrente(idx); PLANO[idx]['novo'] = novo; PLANO[idx]['o_que'].append('%d gancho(s) atualizados + a linha do handoff; %d B, %d linhas' % (len(movidas), len(novo), nlin))
    PLANO[idx]['apendou'] = True
if VIOLACOES:
    print('SUPERFICIES RECUSADAS -- a guarda de texto (P18) achou violacao(oes); nada foi escrito:')
    for onde, v in VIOLACOES:
        print('  -', onde, v)
    sys.exit(4)


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
        assert len(d['novo']) > len(d['raw']), 'o conteudo novo de %s nao cresceu (nada foi escrito)' % p
        # tirar as erratas inline e o append devolve o original: o novo = (original com erratas) + append; sem os blocos, o prefixo e' o original
        rec = d['novo'].decode('utf-8')
        for b in d['blocos']:
            rec = rec.replace(b, '', 1)
        assert rec.encode('utf-8').startswith(d['raw']), 'o conteudo novo de %s nao e (original + erratas ao lado + append): nada foi escrito' % p
    TAREFAS.append((p, d, livre(p + '.bak_' + STAMP + MARCA_BAK), livre(p + '.tmp' + MARCA_BAK + '_' + STAMP)))
if not TAREFAS:
    print('NADA A GRAVAR: todas as superficies ja tem a v394 (idempotente)'); sys.exit(0)
print('PLANO (fase 1, conferido ANTES da primeira escrita): %d alvo(s)%s' % (len(TAREFAS), ' [COPIAS: %s]' % REMAP if REMAP else ''))
for p, d, bak, tmp in TAREFAS:
    if REMAP:
        assert os.path.realpath(p).lower().startswith(os.path.realpath(REMAP).lower() + os.sep), 'ESCRITA FORA DAS COPIAS: %s' % p
    if d['existia']:
        assert open(p, 'rb').read() == d['raw'], '%s mudou desde a leitura -- nada foi escrito' % p
    else:
        assert not os.path.exists(p), '%s apareceu desde a leitura -- nada foi escrito' % p
    print('   %-48s %12s -> %12s B  | %s' % (os.path.basename(p), format(len(d['raw']), ','), format(len(d['novo']), ','), '; '.join(d['o_que'])))
FEITOS = []; tmp_atual = None
try:
    for p, d, bak, tmp in TAREFAS:
        if d['existia']:
            with open(bak, 'wb') as f:
                f.write(d['raw'])
            assert open(bak, 'rb').read() == d['raw'], 'backup de bytes falhou: %s' % bak
        tmp_atual = tmp
        with open(tmp, 'wb') as f:
            f.write(d['novo'])
        assert os.path.getsize(tmp) == len(d['novo'])
        if d['existia']:
            assert open(p, 'rb').read() == d['raw'], 'o arquivo mudou entre a leitura e a troca: %s' % p
        os.replace(tmp, p); tmp_atual = None
        assert open(p, 'rb').read() == d['novo']
        FEITOS.append(p); print('OK', os.path.basename(p), format(len(d['raw']), ','), '->', format(os.path.getsize(p), ','))
except Exception as e:
    if tmp_atual and os.path.exists(tmp_atual):
        os.remove(tmp_atual)
    print('PARADA NAS SUPERFICIES: %r' % e); print('  gravados: %s' % [os.path.basename(x) for x in FEITOS])
    print('  backups de bytes ao lado de cada arquivo tocado; RERODAR e idempotente; nada foi restaurado.'); sys.exit(1)
print('SUPERFICIES v394: %d alvo(s) gravado(s); MEMORY.md %d B, %d linhas (limites %d B e %d linhas)' % (len(FEITOS), os.path.getsize(idx), open(idx, 'rb').read().count(b'\n'), LIMITE, LIMITE_LINHAS))
