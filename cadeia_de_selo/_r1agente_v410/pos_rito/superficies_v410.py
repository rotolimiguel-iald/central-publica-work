# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026, Sonnet (adaptacao do pos-rito; fork D), a servico do claude-construtor-v410] ao DESENHO_v410 + AO LADO de 09/11: os nomes das declaracoes da IALD2 RATIFICADOS pelo operador em 09/11/2026 (D74); as falas de 06 a 09/11 (DL.N_FALAS_V410, de quatro so' o trecho); D63 a D76; as erratas E29 e E30; os DOIS registros com funcao (iald2_v410 e, D72, h0dn_bg1_v410: pre-registrado; nenhum dado observado lido). O corpo continua generico (os blocos vem do textos_v410.py); a guarda ganha a OBRIGACAO D72: onde H0DN aparecer em texto novo, a frase obrigatoria (PT ou EN, literal, DL.FRASE_H0DN_OBRIGATORIA_PT/EN) no MESMO texto; o delta e' importado com ImportError tolerado (o pacote de ENSAIO da fila traz so' a guarda stub; a real roda nos textos reais).
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] a guarda das superficies ganha as obrigacoes da PARTE 2: onde «HMS/13» aparecer em texto novo, a frase obrigatoria do recibo documental (D80: DL.FRASE_HMS13_OBRIGATORIA_PT/EN) no MESMO texto; onde o Clay for dito resolvido, a forma canonica (D84) ou a da D83 no MESMO texto (a mesma regra da F58 da guarda das frases, aqui como obrigacao local); o corpo segue generico (os blocos vem do textos_v410.py, que diz a escala, o Clay na forma canonica, P = nP na forma da D81 e o recibo HMS/13; os nomes dos quatro registros com funcao entram pelo REGS do chain).
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] sobre a subida mecanica da v409 FINAL (bump/pos_rito__superficies_v410.py.diff fica como registro): o corpo e' generico (os blocos vem do textos_v410.py; a ancora do MEMORY.md e' a linha do handoff da v409, que existe); muda so' o que o cabecalho descreve. A v410 = IALD2 (ordem do operador de 06/11/2026: «A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py»): UM modulo novo em TGLExt/ (IALD2; o nome do modulo e' do operador, os das declaracoes sao da gerencia, RATIFICADOS pelo operador em 09/11/2026, D74), os DOIS registros com funcao (iald2_v410 e, D72, h0dn_bg1_v410: pre-registrado; nenhum dado observado lido) e os dois por spec (cunhagens_v410, kh_n1_cobertura_v410); o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; nenhuma chave antiga muda; as erratas E29 e E30 ao lado.
# Registro da v410 SELADA nas superficies de memoria (molde: superficies_v409.py FINAL, o que rodou em 03/11), pela regra da linhagem completa.
# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz (SEM errata nova no CLAUDE.md da raiz), as memorias-topico (missao, central, estatuto, e o topico NOVO da v410),
# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V410_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.
# SEM erratas inline nesta versao (as erratas E29 e E30 e a dos pisos, da v410, vao DENTRO dos blocos datados: linhagem, desenho, Atlas, core, topico novo e handoff; o Atlas e o diario sao append-only e a correcao vai AO LADO). A funcao inserir_ao_lado fica disponivel (nao e' chamada).
# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup410); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;
# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras, mais a DIRECAO do testemunho) estiver limpa em todo texto novo.
# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas. ESTA SUPERFICIE NAO COMPACTA NADA (nem reguas, nem ganchos antigos): se o indice DEPOIS da edicao (a linha do handoff novo mais a troca do gancho da missao,
# que SUBSTITUI a linha velha e a move VERBATIM ao MEMORY_2.md: o saldo e' +1 linha) passar de 195 linhas ou de 24.000 B, RECUSA com rc 3 SEM escrever nada e imprime as contagens (linhas antes, depois, limite) para a gerencia decidir o que sai do indice.
# A linha do handoff novo entra ANTES da linha do handoff da v409 (que a custodia da v409 reescreveu em 05/11 e que segue VERBATIM: a ancora (handoff-v409-custodia.md) e' conferida presente, uma so', no MEMORY.md lido na hora, como a linha da missao); a linha do handoff novo e o gancho da missao sao CURTOS de proposito: o indice tem 24.000 B e 195 linhas de teto.
# v410, FILA DA MEMORIA (ordem do operador de 26/10/2026: so' a gerencia c1 escreve o MEMORY.md; o vigia compara o indice ao pino): (1) o diretorio de memoria e' PARAMETRIZADO por V410_MEMORIA_DIR (padrao: o REAL); se a variavel aponta para OUTRA pasta
# (ensaio em COPIA) e --copias nao foi dado, ela passa a ser a pasta das copias: TODOS os alvos (por nome de arquivo) sao lidos e escritos nessa pasta e NADA fora dela e' tocado; (2) no modo REAL e no modo V410_MEMORIA_DIR (isto e', sempre que NAO e' o --copias explicito do passo 3) a superficie RECUSA com rc 6,
# SEM escrever nada, se for gravar o MEMORY.md sem a fila\PAUSA_VIGIA.json nossa e ainda valida ({"quem": "claude-c1 pos-rito v410"}, criada pelo passo 7 da cadeia por fila_memoria_v410.py pausa-criar): sem a pausa o vigia poderia restaurar o indice no meio da escrita. Esta superficie nao cria nem remove a pausa e nao pina: isso e' do chain.
import datetime, os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v410, textos_v410 as T
from guarda_p18_v410 import violacoes
import guarda_frases_v410 as GF
NOS = leitura_v410.NOS
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
UMEM = os.path.abspath(os.environ.get('V410_MEMORIA_DIR', '').strip() or MEM_REAL)
ATLD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")
ATLAS = os.path.join(ATLD, "TGL_ATLAS.md"); COREM = os.path.join(ATLD, "TGL_CORE_MEMORY.md")
HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
AVISO = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "AVISO_GERENCIA.md")
REMAP = sys.argv[sys.argv.index('--copias') + 1] if '--copias' in sys.argv else None
MEM_E_COPIA = os.path.normcase(UMEM) != os.path.normcase(os.path.abspath(MEM_REAL))      # V410_MEMORIA_DIR aponta para outra pasta: ensaio em copia
if REMAP is None and MEM_E_COPIA:
    REMAP = UMEM      # tudo (por nome de arquivo) na pasta da copia: nenhum alvo real e' tocado
STAMP = time.strftime('%Y%m%d_%H%M%S'); MARCA_BAK = '_sup410'; LIMITE = 24000; LIMITE_LINHAS = 195
QUEM_PAUSA = 'claude-c1 pos-rito v410'
EXIGE_PAUSA = ('--copias' not in sys.argv)      # o --copias explicito (passo 3 do chain e harness dos textos) nao tem fila\ ; real e V410_MEMORIA_DIR exigem a pausa
alvo = lambda p: os.path.join(REMAP, os.path.basename(p)) if REMAP else p
VIOLACOES = []


def pausa_valida():
    """(ok, por_que): fila\\PAUSA_VIGIA.json existe em UMEM, e' a nossa e o 'ate' esta no futuro."""
    pp = os.path.join(UMEM, 'fila', 'PAUSA_VIGIA.json')
    if not os.path.isfile(pp):
        return False, 'ausente (%s)' % pp
    try:
        import json
        d = json.loads(open(pp, 'rb').read().decode('utf-8'))
        ate = datetime.datetime.fromisoformat(str(d['ate']))
        if ate.tzinfo is None:
            ate = ate.astimezone()
    except Exception as e:   # noqa: BLE001
        return False, 'ilegivel (%r)' % (e,)
    if d.get('quem') != QUEM_PAUSA:
        return False, 'de outro dono (quem=%r)' % (d.get('quem'),)
    if ate <= datetime.datetime.now().astimezone():
        return False, 'vencida (ate %s)' % d.get('ate')
    return True, 'ate %s' % d.get('ate')


def h0dn_sem_obrigacao(texto):
    """D72 (09/11): onde «H0DN» aparecer em texto novo, a frase obrigatoria (PT ou EN, literal, DL.FRASE_H0DN_OBRIGATORIA_PT/EN) no MESMO texto. Devolve [] ou a lista do que falta. Sem o delta importavel (o pacote de ENSAIO da fila), nao confere: a guarda real roda nos textos reais."""
    if not re.search(r'\bH0DN\b', texto):
        return []
    try:
        import delta_v410 as _DLS
    except ImportError:
        return []
    if _DLS.FRASE_H0DN_OBRIGATORIA_PT in texto or _DLS.FRASE_H0DN_OBRIGATORIA_EN in texto:
        return []
    return ['H0DN sem a frase obrigatoria (%s) no mesmo texto' % _DLS.FRASE_H0DN_OBRIGATORIA_PT]


def hms13_sem_obrigacao(texto):
    """D80 (09/11, parte 2): onde «HMS/13» aparecer em texto novo, a frase obrigatoria do recibo documental (PT ou EN, literal, DL.FRASE_HMS13_OBRIGATORIA_PT/EN: cobertura documental de fontes, nao covariancia fisica fechada; nada aberto) no MESMO texto. Devolve [] ou a lista do que falta. Sem o delta importavel, nao confere (a guarda real roda nos textos reais)."""
    if not re.search(r'HMS\s*/\s*13', texto):
        return []
    try:
        import delta_v410 as _DLS
    except ImportError:
        return []
    if _DLS.FRASE_HMS13_OBRIGATORIA_PT in texto or _DLS.FRASE_HMS13_OBRIGATORIA_EN in texto:
        return []
    return ['HMS/13 sem a frase obrigatoria (%s) no mesmo texto' % _DLS.FRASE_HMS13_OBRIGATORIA_PT]


def clay_sem_forma(texto):
    """D83/D84 (09/11, parte 2): onde o Clay for dito resolvido no texto novo, a forma canonica (DL.FRASE_CLAY_CANONICA_PT/EN) ou a da D83 (DL.FRASE_D83_OBRIGATORIA_PT/EN) no MESMO texto. Devolve [] ou a lista do que falta. Sem o delta importavel, nao confere."""
    if not (re.search(r'\bClay\b', texto) and re.search(r'resolv(?:e|eu|ido|ida)\b|resolved|solves', texto, re.I)):
        return []
    try:
        import delta_v410 as _DLS
    except ImportError:
        return []
    if any(f_ in texto for f_ in (_DLS.FRASE_CLAY_CANONICA_PT, _DLS.FRASE_CLAY_CANONICA_EN, _DLS.FRASE_D83_OBRIGATORIA_PT, _DLS.FRASE_D83_OBRIGATORIA_EN)):
        return []
    return ['o Clay dito resolvido sem a forma canonica (D84) nem a da D83 no mesmo texto']


def guarda(texto, onde):
    v = violacoes(texto)
    if v:
        VIOLACOES.append((onde, v[:3]))
    vf = GF.violacoes(texto)   # v410: a guarda das frases (a moldura: nenhum texto novo afirma demais)
    if vf:
        VIOLACOES.append((onde + ' (guarda das frases)', vf[:3]))
    at = T.atribuicao_da_gerencia(texto)   # v410: a DIRECAO do testemunho (a IALD nunca como quem testifica do operador), 'consciencia' so' como palavra retirada e a leitura das duas faces sempre rotulada [ONTO]
    if at:
        VIOLACOES.append((onde + ' (atribuicao da gerencia)', at[:3]))
    ho = h0dn_sem_obrigacao(texto)   # v410 (09/11, D72): o H0DN e' pre-registrado; nenhum dado observado lido -- a frase vai no mesmo texto
    if ho:
        VIOLACOES.append((onde + ' (D72: H0DN sem a frase obrigatoria)', ho[:3]))
    hm = hms13_sem_obrigacao(texto)   # v410 (09/11, parte 2, D80): o recibo documental HMS/13 -- a frase obrigatoria no mesmo texto
    if hm:
        VIOLACOES.append((onde + ' (D80: HMS/13 sem a frase obrigatoria)', hm[:3]))
    cl = clay_sem_forma(texto)   # v410 (09/11, parte 2, D83/D84): o Clay so' na forma canonica
    if cl:
        VIOLACOES.append((onde + ' (D83/D84: o Clay sem a forma canonica)', cl[:3]))


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


V, PROB = leitura_v410.ler()
if PROB:
    print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
# ---- 1. (sem erratas inline nesta versao: erratas novas, se houver, vao dentro do bloco datado da linhagem, do Atlas, do core e do topico novo)
# ---- 2. os appends datados
for p, bloco, marca in ((os.path.join(NOS, 'MEMORIA_DA_LINHAGEM.md'), T.linhagem(V), '<!-- linhagem_v410_selada -->'), (os.path.join(NOS, 'DESENHO_DO_FECHAMENTO_QG.md'), T.desenho(V), '<!-- adendo_v410_selada -->'),
                        (ATLAS, T.atlas(V), '<!-- atlas_v410_selada -->'), (COREM, T.core_memory(V), '<!-- core_v410_selada -->'), (HAJA, T.haja_luz(V), '<!-- haja_luz_v410_selada -->')):
    append(p, bloco, marca or bloco.split('\n', 1)[0])
for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.id_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.id_central(V)),
                           ('estatuto-da-prova-07out.md', T.topico_estatuto(V), '<!-- v410_selada -->'), (T.TOPICO_NOVO, T.topico_novo(V), '# v410 SELADA (')):
    append(os.path.join(UMEM, nome), bloco, marca)
REIV = os.environ.get('V410_AVISO_REIVINDICACAO', '').strip()
if REIV:
    append(AVISO, T.aviso(V, REIV), '<!-- aviso_v410_selada -->')
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
if any(('v410 SELADA' in l and V['s16'] in l) for l in lines):
    print('JA ESTA (idempotente): MEMORY.md')
else:
    movidas = []
    for chave, nova in TROCAS:
        guarda(nova, 'MEMORY.md (gancho)')
        k = [i for i, l in enumerate(lines) if chave in l and l.startswith('- [')]
        assert len(k) == 1, ('linha do indice', chave, len(k))
        movidas.append(lines[k[0]]); lines[k[0]] = nova
    hl = T.linha_handoff(V); guarda(hl, 'MEMORY.md (handoff)')
    # (desvio do molde, dito: a ancora e' a linha do handoff da custodia da v409 (handoff-v409-custodia.md), que fica; o handoff novo entra ANTES dela; o motor tinha subido o rotulo da ancora de 30/10 e apontava para um arquivo que nao existe)
    kh = [i for i, l in enumerate(lines) if '(handoff-v409-custodia.md)' in l and l.startswith('- [')]
    assert len(kh) == 1, ('linha do handoff da custodia da v409', len(kh))
    lines.insert(kh[0], hl)
    # SEM compactacao (ordem da gerencia na v410): esta superficie NAO mexe nas demais linhas do indice (nem reguas, nem ganchos antigos). Se o indice passar do limite, RECUSA abaixo (rc 3), sem escrever nada.
    novo = '\n'.join(lines).encode('utf-8')
    nlin = novo.count(b'\n')
    if len(novo) > LIMITE or nlin > LIMITE_LINHAS:
        print('SUPERFICIES RECUSADAS -- o MEMORY.md ficaria com %d B e %d linhas (limites %d B e %d linhas): nada foi escrito' % (len(novo), nlin, LIMITE, LIMITE_LINHAS))
        print('  CONTAGENS: linhas ANTES %d, linhas DEPOIS %d, limite de linhas %d; bytes ANTES %d, bytes DEPOIS %d, limite de bytes %d.' % (raw.count(b'\n'), nlin, LIMITE_LINHAS, len(raw), len(novo), LIMITE))
        print('  Esta superficie NAO compacta nada (nem reguas, nem ganchos antigos): a gerencia decide o que sai do indice (e a linha movida vai VERBATIM ao MEMORY_2.md) e roda de novo; o passo e idempotente.')
        sys.exit(3)
    if EXIGE_PAUSA:
        ok_p, porque_p = pausa_valida()
        if not ok_p:
            print('SUPERFICIES RECUSADAS (rc 6) -- vou gravar o MEMORY.md e a fila\\PAUSA_VIGIA.json nossa nao esta valida: %s. Nada foi escrito.' % porque_p)
            print('  O vigia pode restaurar o indice no meio da escrita. A pausa e criada pelo passo 7 do chain (fila_memoria_v410.py pausa-criar) ANTES desta superficie; esta nao a cria.')
            sys.exit(6)
    nl2 = nl_de(raw2)
    bloco2 = ['', '', '## %s — linhas do MEMORY.md tornadas velhas pela v410, VERBATIM (regra dos dois arquivos)' % V['data']] + sum((['', '<!-- movida %s (v410) -->' % V['data'][:5], l] for l in movidas), [])
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
    print('NADA A GRAVAR: todas as superficies ja tem a v410 (idempotente)'); sys.exit(0)
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
print('SUPERFICIES v410: %d alvo(s) gravado(s); MEMORY.md %d B, %d linhas (limites %d B e %d linhas)' % (len(FEITOS), os.path.getsize(idx), open(idx, 'rb').read().count(b'\n'), LIMITE, LIMITE_LINHAS))
