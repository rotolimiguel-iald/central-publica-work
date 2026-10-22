# -*- coding: utf-8 -*-
# v392: arvore_da_prova.py (linha da v392 + erratas ao lado CR-08 e CR-02) e atlas_indice.py (manifesto, verbete + remissivo), na casa canonica das ferramentas da cadeia.
# Molde: patch_arvore_indice_v391.py. O arquivo so' CRESCE (linhas NOVAS; nada e' reescrito por cima). Cada alvo e' achado por BUSCA e tem de dar exatamente uma ocorrencia
# (zero ou mais de uma = recusa). Guardas pela PROPRIA linha inserida (idempotente); numeros LIDOS da rodada (leitura_v392.ler); recusa se a leitura tiver problema e se a guarda de
# texto (P18) achar violacao. Backup de BYTES (_p392); temporario -> cresce? -> substituir; ast.parse. NAO RODA arvore_da_prova.py nem atlas_indice.py (isso e' da cadeia).
# --tools <pasta> = ensaio em copias das duas ferramentas.
#
# As erratas da arvore (achados do critico do levantamento de 12/10, conferidos no gerador por busca):
#   CR-08  a l.155 do gerador (docblock v116: «a emergencia GERAL ... segue NOMEADA e aberta») e a l.272 («NAO PROVADO ... a emergencia geral») contradizem a l.262
#          («Emergencia geral ... PAGA como implicacao (v317)»); a errata vai ao lado das duas;
#   CR-02  a l.272 («identificacao T_c = Delta_c^{1/2} ... segue OPEN»): a raiz positiva e' termo de kernel; falta so' a unicidade (Kato) [KNOWN].
import ast, time, os, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, HERE); sys.path.insert(0, PK)
import leitura_v392, textos_v392
from guarda_p18_v392 import violacoes
ST = time.strftime('%Y%m%d_%H%M%S')
TOOLS = sys.argv[sys.argv.index('--tools') + 1] if '--tools' in sys.argv else os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo")


def grava(P, s):
    ast.parse(s)
    tmp = P + '.tmp_p392_' + ST
    assert not os.path.exists(tmp)
    open(tmp, 'wb').write(s.encode('utf-8'))
    if not os.path.getsize(tmp) > os.path.getsize(P):
        os.remove(tmp); raise AssertionError('o arquivo novo nao cresceu -- nao substituo')
    os.replace(tmp, P)


def backup(P):
    b = P + '.bak_' + ST + '_p392'; n = 1
    while os.path.exists(b):
        n += 1; b = '%s.bak_%s_p392_%d' % (P, ST, n)
    raw = open(P, 'rb').read(); open(b, 'wb').write(raw); assert open(b, 'rb').read() == raw


V, PROB = leitura_v392.ler()
if PROB:
    print('PATCH RECUSADO -- a leitura da rodada tem problema(s):'); [print('  -', p) for p in PROB]; sys.exit(2)
T = textos_v392
print('ferramentas em:', TOOLS)
# ------------------------------------------------------------------ arvore_da_prova.py
P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
L = s.split('\n')


def unico(pred, o_que):
    k = [i for i, l in enumerate(L) if pred(l)]
    assert len(k) == 1, ('alvo da arvore: %s -- ocorrencias = %d (esperado 1)' % (o_que, len(k)))
    return k[0]


TAG_L = '- **AS PEDRAS DA v392**'; TAG_E1 = 'ERRATA AO LADO (CR-08, v392'; TAG_E2 = 'ERRATA AO LADO (CR-02, v392'
novas = [T.arvore_linha(V), T.arvore_errata_cr08_a(V), T.arvore_errata_cr08_b(V), T.arvore_errata_cr02(V)]
bad = [(i, violacoes(t)[:2]) for i, t in enumerate(novas) if violacoes(t)]
if bad:
    print('PATCH RECUSADO -- a guarda de texto (P18) achou violacao(oes):', bad); sys.exit(4)
# os tres alvos e a linha de contraste (l.262) existem, por busca
i155 = unico(lambda l: l.startswith("L.append('- **Honestidade do próprio kernel** (docblock v116)") and 'segue **NOMEADA e aberta**' in l, 'l.155 (docblock v116)')
i262 = unico(lambda l: '**PAGA como implicação (v317)**' in l, 'l.262 (PAGA como implicacao)')
i272 = unico(lambda l: l.startswith("L.append('- **NÃO PROVADO, e dito com nome**") and 'a emergência geral' in l and 'T_c = Δ_c^{1/2}' in l, 'l.272 (NAO PROVADO)')
iv391 = unico(lambda l: l.startswith("L.append('- **O ESTATUTO DA PROVA (v391)"), 'linha da v391')
print('alvos achados por busca: l.%d (CR-08), l.%d (contraste), l.%d (CR-08 + CR-02), l.%d (ancora da v392)' % (i155 + 1, i262 + 1, i272 + 1, iv391 + 1))
mudou = []
# a ordem de insercao e' de baixo para cima (os indices dos alvos acima nao se movem): v391 (a ancora da linha nova) -> l.272 -> l.155
if not any(TAG_L in l for l in L):
    L.insert(iv391, 'L.append(%s)   # v392' % repr(novas[0])); mudou.append('linha v392')
if not any(TAG_E2 in l for l in L):
    L.insert(i272 + 1, 'L.append(%s)   # v392 CR-02' % repr(novas[3])); L.insert(i272 + 1, 'L.append(%s)   # v392 CR-08 (b)' % repr(novas[2])); mudou.append('CR-08(b)+CR-02 ao lado da l.272')
if not any(TAG_E1 in l and 'v116' in l for l in L):
    L.insert(i155 + 1, 'L.append(%s)   # v392 CR-08 (a)' % repr(novas[1])); mudou.append('CR-08(a) ao lado da l.155')
if mudou:
    s2 = '\n'.join(L)
    assert s2.count(TAG_L) == 1 and s2.count(TAG_E2) == 1 and s2.count(TAG_E1) == 2, (s2.count(TAG_L), s2.count(TAG_E2), s2.count(TAG_E1))
    backup(P); grava(P, s2); print('arvore_da_prova.py: +%s' % '; '.join(mudou))
else:
    print('arvore_da_prova.py: a linha v392 e as erratas ja estao (idempotente)')
# ------------------------------------------------------------------ atlas_indice.py
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v392_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i391p = ')
    L.insert(i + 1, "_i392p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v392_incorporacao_manifesto.json'); _i392 = json.load(open(_i392p, encoding='utf-8')) if os.path.exists(_i392p) else {}   # v392")
    i = acha('verbetes = [')
    L.insert(i, '_V392TXT = %s   # v392' % repr(T.verbete(V)))
    i = acha(" ('O estatuto da prova: provada; a confirmação recusada é creditação, não validade (v391):'")
    L.insert(i + 1, " (%s, _V392TXT)," % repr(T.titulo_verbete(V)))
    i = acha("       '- **O estatuto da prova; provada ≠ confirmada; creditação × validade (v391)")
    L.insert(i + 1, '       %s,' % repr(T.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v392_incorporacao_manifesto') == 1 and s.count('_i392p') == 3 and s.count('_V392TXT') == 2, (s.count('v392_incorporacao_manifesto'), s.count('_i392p'), s.count('_V392TXT'))
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v392)')
else:
    print('atlas_indice.py: a v392 ja esta (idempotente)')
