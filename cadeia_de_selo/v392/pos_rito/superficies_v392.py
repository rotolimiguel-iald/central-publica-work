# -*- coding: utf-8 -*-
# Registro da v392 SELADA nas superficies de memoria (molde: superficies_v391.py), pela regra da linhagem completa.
# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado; a v391 nao o tocou), o CLAUDE.md da Haja_Luz, as memorias-topico
# (missao, central, estatuto, e o topico NOVO da v392), o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V392_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.
# ERRATAS AO LADO (inline, depois da linha que traz a frase; a linha antiga fica; tirar o bloco devolve o arquivo original, conferido): CR-08 (a lei de campo curva) na linhagem, no desenho,
# no Atlas e nos dois handoffs da v390; a errata (3) (a ressalva do estatuto da prova) ao lado do paragrafo da v391 na linhagem; a atribuicao do residuo de raiz de 2 (Coulomb) no CLAUDE.md da Haja_Luz.
# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup392); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;
# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.
# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas.
import os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v392, textos_v392 as T
from guarda_p18_v392 import violacoes
NOS = leitura_v392.NOS
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")
ATLAS = os.path.join(ATLD, "TGL_ATLAS.md"); COREM = os.path.join(ATLD, "TGL_CORE_MEMORY.md")
HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
AVISO = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "AVISO_GERENCIA.md")
REMAP = sys.argv[sys.argv.index('--copias') + 1] if '--copias' in sys.argv else None
STAMP = time.strftime('%Y%m%d_%H%M%S'); MARCA_BAK = '_sup392'; LIMITE = 24000; LIMITE_LINHAS = 195
alvo = lambda p: os.path.join(REMAP, os.path.basename(p)) if REMAP else p
RX_CR08 = [re.compile(r"lei de campo no (espa[çc]o-tempo )?curvo[^.\n]{0,40}?N[ÃAãa]O[^.\n]{0,12}?(é|e|sendo) termo de kernel", re.I),
           re.compile(r"FIELD_EQUATION_IN_CURVED_SPACETIME_NOT_A_KERNEL_TERM")]
RX_V391_ENTROU = [re.compile(r"^\*\*O que entrou\*\* \(pacote `work\\v391_pacote`")]
RX_COULOMB = [re.compile(r"Coulomb")]
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


V, PROB = leitura_v392.ler()
if PROB:
    print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
# ---- 1. as erratas ao lado (inline), ANTES dos appends
E_CR08 = T.errata_cr08(V); MK_CR08 = 'errata_cr08_v392'
for p in (os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), ATLAS, os.path.join(NOS, 'HANDOFF_v390_CUSTODIA.md'), os.path.join(UMEM, 'handoff-v390-custodia.md')):
    inserir_ao_lado(p, RX_CR08, E_CR08, MK_CR08, minimo=1)
inserir_ao_lado(os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), RX_V391_ENTROU, T.errata_3(V), 'errata_3_v392', exato=1)
inserir_ao_lado(HAJA, RX_COULOMB, T.errata_coulomb(V), 'errata_coulomb_v392', minimo=1, juntar=True)
# ---- 2. os appends datados
for p, bloco, marca in ((os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), T.linhagem(V), '<!-- linhagem_v392_selada -->'), (os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), T.desenho(V), '<!-- adendo_v392_selada -->'),
                        (ATLAS, T.atlas(V), '<!-- atlas_v392_selada -->'), (COREM, T.core_memory(V), '<!-- core_v392_selada -->'), (HAJA, T.haja_luz(V), '<!-- haja_luz_v392_selada -->')):
    append(p, bloco, marca or bloco.split('\n', 1)[0])
for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.id_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.id_central(V)),
                           ('estatuto-da-prova-07out.md', T.topico_estatuto(V), '<!-- v392_selada -->'), (T.TOPICO_NOVO, T.topico_novo(V), '# v392 SELADA (')):
    append(os.path.join(UMEM, nome), bloco, marca)
REIV = os.environ.get('V392_AVISO_REIVINDICACAO', '').strip()
if REIV:
    append(AVISO, T.aviso(V, REIV), '<!-- aviso_v392_selada -->')
else:
    print(T.aviso_pulado())
# ---- 3. MEMORY.md (+ MEMORY_2.md): as linhas velhas VERBATIM ao MEMORY_2; no lugar, o gancho curto
idx = alvo(os.path.join(UMEM, 'MEMORY.md')); idx2 = alvo(os.path.join(UMEM, 'MEMORY_2.md'))
raw = open(idx, 'rb').read(); raw2 = open(idx2, 'rb').read()
assert b'\r\n' not in raw, 'MEMORY.md com CRLF: o molde espera LF'
lines = raw.decode('utf-8').split('\n')
TROCAS = [  # (o trecho que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2
    ('(missao-ultima-flag-um-py.md)', "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + T.marca_missao(V) + "íntegra anterior no MEMORY_2.md (movida %s)" % V['data'][:5]),
    ('(a-leitura-cria-o-objeto-07out.md)', T.linha_palavra(V)),
]
if any(('v392 SELADA' in l and V['s16'] in l) for l in lines):
    print('JA ESTA (idempotente): MEMORY.md')
else:
    movidas = []
    for chave, nova in TROCAS:
        guarda(nova, 'MEMORY.md (gancho)')
        k = [i for i, l in enumerate(lines) if chave in l and l.startswith('- [')]
        assert len(k) == 1, ('linha do indice', chave, len(k))
        movidas.append(lines[k[0]]); lines[k[0]] = nova
    hl = T.linha_handoff(V); guarda(hl, 'MEMORY.md (handoff)')
    kh = [i for i, l in enumerate(lines) if '(handoff-v391-custodia.md)' in l and l.startswith('- [HANDOFF v391')]
    assert len(kh) == 1, ('linha do handoff v391', len(kh))
    lines.insert(kh[0], hl)
    novo = '\n'.join(lines).encode('utf-8')
    nlin = novo.count(b'\n')
    if len(novo) > LIMITE or nlin > LIMITE_LINHAS:
        print('SUPERFICIES RECUSADAS -- o MEMORY.md ficaria com %d B e %d linhas (limites %d B e %d linhas): nada foi escrito' % (len(novo), nlin, LIMITE, LIMITE_LINHAS)); sys.exit(3)
    nl2 = nl_de(raw2)
    bloco2 = ['', '', '## %s — linhas do MEMORY.md tornadas velhas pela v392, VERBATIM (regra dos dois arquivos)' % V['data']] + sum((['', '<!-- movida %s (v392) -->' % V['data'][:5], l] for l in movidas), [])
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
    print('NADA A GRAVAR: todas as superficies ja tem a v392 (idempotente)'); sys.exit(0)
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
print('SUPERFICIES v392: %d alvo(s) gravado(s); MEMORY.md %d B, %d linhas (limites %d B e %d linhas)' % (len(FEITOS), os.path.getsize(idx), open(idx, 'rb').read().count(b'\n'), LIMITE, LIMITE_LINHAS))
