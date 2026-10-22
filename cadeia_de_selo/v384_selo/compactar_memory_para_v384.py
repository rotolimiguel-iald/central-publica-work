# -*- coding: utf-8 -*-
"""Folga no MEMORY.md para a cadeia da v384, pela REGRA DOS DOIS ARQUIVOS (molde: compactar_memory_para_v383.py): nada se corta; toda linha tocada vai
INTEIRA, VERBATIM, para o fim do MEMORY_2.md ANTES de mudar aqui. Passos, na ordem, so ate caber (para quando cabe):
 (a) a linha da MISSAO (que cresce a cada selo) vira o ponteiro curto com o ULTIMO selo lido dela («**vNNN SELADA dd/mm `sha16` N/N COMPLETA** ·
     íntegra (vNNN–vMMM, cada selo) no MEMORY_2.md (movida dd/mm)»), no molde das compactações de 02/10;
 (b) as frases-ponteiro longas «linha integral no MEMORY_2.md (movida em DD/MM[/AAAA][ pela regra dos dois arquivos])» viram «íntegra no MEMORY_2.md
     (movida DD/MM)» -- a convenção que o próprio índice registra (linha «Compactação 30/09/2026»), só a frase-ponteiro;
 (c) a linha do HANDOFF v383 vira ponteiro («— **dd/mm, para a sessão do site** · `sha16` · íntegra no MEMORY_2.md (movida dd/mm)»).
A folga pedida = o marcador da v384 na missão + a linha do handoff v384 (+ 150 B de margem), LIDOS dos textos com a leitura da rodada; sem a leitura
(rito ainda não acabou), a estimativa é 900 B -- dito. Sem argumento: só mede. Com --gravar: grava (backup de BYTES dos dois; o MEMORY_2 primeiro;
temporário -> conferir -> substituir). Honra V384_REMAP_DIR/V384_WRITE_ROOT (cópias) e o Nós SINTÉTICO (V384_UMEM)."""
import os, re, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
AMB = A.ambiente()
GRAVAR = '--gravar' in sys.argv
ST = time.strftime('%Y%m%d_%H%M%S'); HOJE = time.strftime('%d/%m'); HOJE_L = time.strftime('%d/%m/%Y')
LIMITE = 24000; MARGEM = 150
alvo = (lambda p: os.path.join(AMB['remap'], os.path.basename(p))) if AMB['remap'] else (lambda p: p)
idx = alvo(os.path.join(AMB['umem'], 'MEMORY.md')); idx2 = alvo(os.path.join(AMB['umem'], 'MEMORY_2.md'))
try:
    import leitura_v384, textos_v384 as T
    V, PROB = leitura_v384.ler()
except Exception as e:
    V, PROB = None, ['leitura indisponivel: %r' % e]
if not PROB:
    precisa = len(T.marca_missao(V).encode('utf-8')) + len((T.linha_handoff(V) + '\n').encode('utf-8')) + MARGEM
    origem = 'lida dos textos da v384 (marcador da missão + linha do handoff) + %d B de margem' % MARGEM
else:
    precisa = 900; origem = 'ESTIMADA (a leitura da rodada ainda não está limpa: %s)' % '; '.join(PROB)[:200]
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
        tocadas.append(('<!-- compactação v384 (%s): a linha da missão, movida inteira; ficou o ponteiro curto -->' % HOJE_L, l0)); lines[ks[0]] = novo
        print('  (a) a linha da missão: %d -> %d B' % (len(l0.encode('utf-8')), len(novo.encode('utf-8'))))
    else:
        print('  (a) a linha da missão não tem a forma esperada (ou já é curta) -- não tocada')
# (b) as frases-ponteiro longas
RE_B = re.compile(r'linha integral no MEMORY_2\.md \(movida em (\d\d/\d\d)(?:/\d{4})?(?: pela regra dos dois arquivos)?\)')
if tam() > ALVO:
    n = 0
    for i, l in enumerate(lines):
        if RE_B.search(l):
            tocadas.append(('<!-- compactação v384 (%s): só a frase-ponteiro normalizada (convenção de 30/09) -->' % HOJE_L, l))
            lines[i] = RE_B.sub(lambda mm: 'íntegra no MEMORY_2.md (movida %s)' % mm.group(1), l); n += 1
    print('  (b) frases-ponteiro normalizadas: %d linha(s)' % n)
# (c) a linha do handoff v383
if tam() > ALVO:
    ks = [i for i, l in enumerate(lines) if '(handoff-v383-custodia.md) — ' in l]
    if len(ks) == 1 and 'íntegra no MEMORY_2' not in lines[ks[0]]:
        l0 = lines[ks[0]]; pre, resto = l0.split('(handoff-v383-custodia.md) — ', 1)
        mb = re.match(r'(\*\*[^*]+\*\*)', resto); ms = re.findall(r'`([0-9a-f]{16})`', resto)
        if mb:
            novo = pre + '(handoff-v383-custodia.md) — ' + mb.group(1) + (' · `%s`' % ms[-1] if ms else '') + ' · íntegra no MEMORY_2.md (movida %s)' % HOJE
            tocadas.append(('<!-- compactação v384 (%s): a linha do handoff v383, movida inteira; ficou o ponteiro -->' % HOJE_L, l0)); lines[ks[0]] = novo
            print('  (c) a linha do handoff v383: %d -> %d B' % (len(l0.encode('utf-8')), len(novo.encode('utf-8'))))
novo = '\n'.join(lines).encode('utf-8')
print('RESULTADO: MEMORY.md %d -> %d B (alvo <= %d; depois da cadeia: <= %d B) | linhas tocadas: %d' % (len(raw), len(novo), ALVO, len(novo) + precisa - MARGEM, len(tocadas)))
if len(novo) > ALVO:
    print('AINDA ACIMA DO ALVO -- nada gravado; liberar folga a mão (regra dos dois arquivos)'); sys.exit(3)
if not tocadas:
    print('nada a compactar: o índice já tem a folga'); sys.exit(0)
nl2 = '\r\n' if raw2.count(b'\r\n') > raw2.count(b'\n') // 2 else '\n'
bloco = nl2.join(['', '', '## %s — linhas do MEMORY.md tocadas pela compactação da v384 (regra dos dois arquivos), VERBATIM ANTES da mudança, com o marcador ao lado' % HOJE_L]
                 + sum([['', m, l] for m, l in tocadas], [])) + nl2
novo2 = raw2 + bloco.encode('utf-8')
assert all(l.encode('utf-8') in novo2 for _m, l in tocadas)
# idempotencia (10o achado da revisao de 04/10): se o MEMORY_2 JA tem, depois do ultimo cabecalho desta compactacao, TODAS as linhas tocadas verbatim,
# uma passada anterior trocou o MEMORY_2 e caiu antes de trocar o MEMORY.md: grava-se SO o MEMORY.md (o bloco nunca entra duas vezes)
CAB = 'linhas do MEMORY.md tocadas pela compactação da v384'.encode('utf-8')
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
        raise SystemExit('ensaio com o Nós SINTÉTICO sem V384_WRITE_ROOT -- recuso')
for p, r in ((idx, raw), (idx2, raw2)):
    b = p + '.bak_' + ST + '_comp384'; assert not os.path.exists(b); open(b, 'wb').write(r); assert open(b, 'rb').read() == r
if not JA_NO_2:
    open(idx2 + '.tmp', 'wb').write(novo2); assert os.path.getsize(idx2 + '.tmp') == len(novo2) > len(raw2); assert open(idx2, 'rb').read() == raw2; os.replace(idx2 + '.tmp', idx2)
open(idx + '.tmp', 'wb').write(novo); assert os.path.getsize(idx + '.tmp') == len(novo); assert open(idx, 'rb').read() == raw; os.replace(idx + '.tmp', idx)
assert open(idx2, 'rb').read()[:len(raw2)] == raw2 and open(idx, 'rb').read() == novo
print('OK gravado: o índice encolheu porque o MEMORY_2 cresceu com as linhas integrais (%d B -> %d B)' % (len(raw2), len(novo2)))
