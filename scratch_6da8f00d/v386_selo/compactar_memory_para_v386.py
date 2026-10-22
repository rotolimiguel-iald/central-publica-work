# -*- coding: utf-8 -*-
"""Folga no MEMORY.md para a cadeia da v386, pela REGRA DOS DOIS ARQUIVOS (molde: compactar_memory_para_v385.py): nada se corta; toda linha tocada vai
INTEIRA, VERBATIM, para o fim do MEMORY_2.md ANTES de mudar aqui. Passos, na ordem, so ate caber (para quando cabe):
 (a) a linha da MISSAO (que cresce a cada selo) vira o ponteiro curto com o ULTIMO selo lido dela («**vNNN SELADA dd/mm `sha16` N/N COMPLETA** ·
     íntegra (vNNN–vMMM, cada selo) no MEMORY_2.md (movida dd/mm)»), no molde das compactações de 02/10 e 05/10;
 (b) as frases-ponteiro longas «linha integral no MEMORY_2.md (movida em DD/MM[/AAAA][ pela regra dos dois arquivos])» viram «íntegra no MEMORY_2.md
     (movida DD/MM)» -- a convenção que o próprio índice registra (linha «Compactação 30/09/2026»), só a frase-ponteiro;
 (c) as linhas dos HANDOFFS anteriores ainda longas (v385, depois v384, depois v383, nesta ordem) viram ponteiro («— **dd/mm, para a sessão do site** ·
     `sha16` · íntegra no MEMORY_2.md (movida dd/mm)»), uma de cada vez, só ate caber.
A folga pedida = o marcador da v386 na missão + a linha do handoff v386 + a marca do pilar (+ 150 B de margem), LIDOS dos textos com a leitura da rodada;
sem a leitura (rito ainda não acabou), a estimativa é 1100 B -- dito. Sem argumento: só mede. Com --gravar: grava (backup de BYTES dos dois; o MEMORY_2
primeiro; temporário -> conferir -> substituir). Honra V386_REMAP_DIR/V386_WRITE_ROOT (cópias) e o Nós SINTÉTICO (V386_UMEM)."""
import os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
AMB = A.ambiente()
GRAVAR = '--gravar' in sys.argv
ST = time.strftime('%Y%m%d_%H%M%S'); HOJE = time.strftime('%d/%m'); HOJE_L = time.strftime('%d/%m/%Y')
LIMITE = 24000; MARGEM = 150
alvo = (lambda p: os.path.join(AMB['remap'], os.path.basename(p))) if AMB['remap'] else (lambda p: p)
idx = alvo(os.path.join(AMB['umem'], 'MEMORY.md')); idx2 = alvo(os.path.join(AMB['umem'], 'MEMORY_2.md'))
try:
    import leitura_v386, textos_v386 as T
    V, PROB = leitura_v386.ler()
except Exception as e:
    V, PROB = None, ['leitura indisponivel: %r' % e]
if not PROB:
    _mp = (' · **v386 (%s): o marcador agora é `%s`**' % (V['data'][:5], os.path.join(A.PK, '.servidor_parado_pelo_rito')))   # a MESMA da superficies_v386
    precisa = len(T.marca_missao(V).encode('utf-8')) + len((T.linha_handoff(V) + '\n').encode('utf-8')) + len(_mp.encode('utf-8')) + MARGEM
    origem = 'lida dos textos da v386 (marcador da missão + linha do handoff + a marca do pilar) + %d B de margem' % MARGEM
else:
    precisa = 1100; origem = 'ESTIMADA (a leitura da rodada ainda não está limpa: %s)' % '; '.join(PROB)[:200]
raw = open(idx, 'rb').read(); raw2 = open(idx2, 'rb').read(); assert b'\r\n' not in raw, 'MEMORY.md com CRLF'
lines = raw.decode('utf-8').split('\n')
ALVO = LIMITE - precisa
tocadas = []   # (marcador, linha original)


def tam():
    return len('\n'.join(lines).encode('utf-8'))


print('MEMORY.md: %d B; a folga pedida: %d B (%s); alvo <= %d B' % (len(raw), precisa, origem, ALVO))
# (a) a linha da missao
if tam() > ALVO:
    ks = [i for i, l in enumerate(lines) if '(missao-ultima-flag-um-py.md) — ' in l]
    assert len(ks) == 1, ('linha da missao', len(ks))
    l0 = lines[ks[0]]; pre, resto = l0.split('(missao-ultima-flag-um-py.md) — ', 1)
    m = re.match(r'\*\*(v(\d{3}) SELADA \d\d/\d\d `[0-9a-f]{16}` \d+/\d+ (?:COMPLETA|INTERMEDIÁRIA))[ *]', resto)
    r = re.search(r'íntegra \(v\d{3}–v(\d{3}), cada selo\)', resto)
    if m and r and len(l0.encode('utf-8')) > 300:
        novo = pre + '(missao-ultima-flag-um-py.md) — **%s** · íntegra (v%s–v%s, cada selo) no MEMORY_2.md (movida %s)' % (m.group(1), m.group(2), r.group(1), HOJE)
        tocadas.append(('<!-- compactação v386 (%s): a linha da missão, movida inteira; ficou o ponteiro curto -->' % HOJE_L, l0)); lines[ks[0]] = novo
        print('  (a) a linha da missão: %d -> %d B' % (len(l0.encode('utf-8')), len(novo.encode('utf-8'))))
    else:
        print('  (a) a linha da missão não tem a forma esperada (ou já é curta) -- não tocada')
# (b) as frases-ponteiro longas
RE_B = re.compile(r'linha integral no MEMORY_2\.md \(movida em (\d\d/\d\d)(?:/\d{4})?(?: pela regra dos dois arquivos)?\)')
if tam() > ALVO:
    n = 0
    for i, l in enumerate(lines):
        if RE_B.search(l):
            tocadas.append(('<!-- compactação v386 (%s): só a frase-ponteiro normalizada (convenção de 30/09) -->' % HOJE_L, l))
            lines[i] = RE_B.sub(lambda mm: 'íntegra no MEMORY_2.md (movida %s)' % mm.group(1), l); n += 1
    print('  (b) frases-ponteiro normalizadas: %d linha(s)' % n)
# (c) as linhas-índice ainda longas que já têm a sua memória-tópico inteira (os handoffs anteriores; depois as memórias do Verbo e do ramo B, de 05/10),
#     uma de cada vez, so ate caber: fica o bold de abertura (+ o sha16, se houver) e o ponteiro; a linha inteira vai VERBATIM ao MEMORY_2
for arq, nome in (('handoff-v385-custodia.md', 'do handoff v385'), ('handoff-v384-custodia.md', 'do handoff v384'), ('handoff-v383-custodia.md', 'do handoff v383'),
                  ('verbo-selecao-da-acao-05out.md', 'da memória do Verbo (05/10)'), ('ramo-b-reaberto-05out.md', 'da memória do ramo B (05/10)')):
    if tam() <= ALVO:
        break
    tag = '(%s) — ' % arq
    ks = [i for i, l in enumerate(lines) if tag in l]
    if len(ks) == 1 and 'íntegra no MEMORY_2' not in lines[ks[0]] and len(lines[ks[0]].encode('utf-8')) > 250:
        l0 = lines[ks[0]]; pre, resto = l0.split(tag, 1)
        mb = re.match(r'(\*\*[^*]+\*\*)', resto); ms = re.findall(r'`([0-9a-f]{16})`', resto)
        if mb:
            novo = pre + tag + mb.group(1) + (' · `%s`' % ms[-1] if ms else '') + ' · íntegra no MEMORY_2.md (movida %s)' % HOJE
            tocadas.append(('<!-- compactação v386 (%s): a linha %s, movida inteira; ficou o ponteiro -->' % (HOJE_L, nome), l0)); lines[ks[0]] = novo
            print('  (c) a linha %s: %d -> %d B' % (nome, len(l0.encode('utf-8')), len(novo.encode('utf-8'))))
# (d) a linha do PILAR: o marcador do servidor passa a ser o do pacote CORRENTE, na forma curta que a linha já tem («conferir o marcador
#     `scratchpad\v385\.servidor_parado_pelo_rito`» -> «`scratchpad\v386\pacote\...`»); a linha inteira vai VERBATIM ao MEMORY_2 (o anterior fica lá);
#     a superficies_v386 só acrescenta a marca longa se a curta não estiver na linha
V385_MK = '`scratchpad\\v385\\.servidor_parado_pelo_rito`'; V386_MK = '`scratchpad\\v386\\pacote\\.servidor_parado_pelo_rito`'
ks = [i for i, l in enumerate(lines) if '(v384-pilar-quantico-gpu-02out.md) — ' in l]
if len(ks) == 1 and V385_MK in lines[ks[0]] and V386_MK not in lines[ks[0]]:
    l0 = lines[ks[0]]; novo_d = l0.replace(V385_MK, V386_MK)
    tocadas.append(('<!-- compactação v386 (%s): a linha do pilar, movida inteira; o marcador do servidor passou ao pacote v386 (o da v385 fica aqui) -->' % HOJE_L, l0)); lines[ks[0]] = novo_d
    print('  (d) a linha do pilar: o marcador do servidor -> pacote v386 (%d -> %d B)' % (len(l0.encode('utf-8')), len(novo_d.encode('utf-8'))))
else:
    print('  (d) a linha do pilar: já aponta o pacote v386 (ou não tem a forma curta) -- não tocada')
novo = '\n'.join(lines).encode('utf-8')
print('RESULTADO: MEMORY.md %d -> %d B (alvo <= %d; depois da cadeia: <= %d B) | linhas tocadas: %d' % (len(raw), len(novo), ALVO, len(novo) + precisa - MARGEM, len(tocadas)))
if len(novo) > ALVO:
    print('AINDA ACIMA DO ALVO -- nada gravado; liberar folga a mão (regra dos dois arquivos)'); sys.exit(3)
if not tocadas:
    print('nada a compactar: o índice já tem a folga'); sys.exit(0)
nl2 = '\r\n' if raw2.count(b'\r\n') > raw2.count(b'\n') // 2 else '\n'
bloco = nl2.join(['', '', '## %s — linhas do MEMORY.md tocadas pela compactação da v386 (regra dos dois arquivos), VERBATIM ANTES da mudança, com o marcador ao lado' % HOJE_L]
                 + sum([['', m, l] for m, l in tocadas], [])) + nl2
novo2 = raw2 + bloco.encode('utf-8')
assert all(l.encode('utf-8') in novo2 for _m, l in tocadas)
CAB = 'linhas do MEMORY.md tocadas pela compactação da v386'.encode('utf-8')
_k = raw2.rfind(CAB)
JA_NO_2 = _k >= 0 and all(l.encode('utf-8') in raw2[_k:] for _m, l in tocadas)
if JA_NO_2:
    print('o MEMORY_2.md JA tem o bloco verbatim desta compactacao (passada anterior interrompida): grava-se SO o MEMORY.md')
    novo2 = raw2
if not GRAVAR:
    print('(só medido; rode com --gravar)'); sys.exit(0)
for p in (idx, idx2):
    if AMB['write_root']:
        assert os.path.realpath(p).lower().startswith(os.path.realpath(AMB['write_root']).lower() + os.sep), 'ESCRITA FORA DA RAIZ: ' + p
    elif AMB['sint']:
        raise SystemExit('ensaio com o Nós SINTÉTICO sem V386_WRITE_ROOT -- recuso')
for p, r in ((idx, raw), (idx2, raw2)):
    b = p + '.bak_' + ST + '_comp386'; assert not os.path.exists(b); open(b, 'wb').write(r); assert open(b, 'rb').read() == r
if not JA_NO_2:
    open(idx2 + '.tmp', 'wb').write(novo2); assert os.path.getsize(idx2 + '.tmp') == len(novo2) > len(raw2); assert open(idx2, 'rb').read() == raw2; os.replace(idx2 + '.tmp', idx2)
open(idx + '.tmp', 'wb').write(novo); assert os.path.getsize(idx + '.tmp') == len(novo); assert open(idx, 'rb').read() == raw; os.replace(idx + '.tmp', idx)
assert open(idx2, 'rb').read()[:len(raw2)] == raw2 and open(idx, 'rb').read() == novo
print('OK gravado: o índice encolheu porque o MEMORY_2 cresceu com as linhas integrais (%d B -> %d B)' % (len(raw2), len(novo2)))
