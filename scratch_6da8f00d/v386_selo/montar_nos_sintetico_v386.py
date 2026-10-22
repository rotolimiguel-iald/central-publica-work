# -*- coding: utf-8 -*-
"""Monta o Nos SINTETICO da v386 para o ENSAIO da cadeia pos-rito -- NUNCA o rito, NUNCA o real. Tudo marcado SINTETICO. (Molde: montar_nos_sintetico_v385.py.)
Base: o estado SELADO da v385 lido dos backups de BYTES do Nos gravados pelo instalar_v386.py (conferidos contra o APLICADO_AO_CANONICO), SO LEITURA --
o Nos REAL (onde o rito v386 esta rodando) NAO e' lido alem do rodada_v385_stdout.txt (selado, da v385) e dos backups .bak_<ts> (congelados).
Dois MODOS (V386_SINT_MODO):
 - AINDA_V385 (o estado ATUAL do Nos enquanto o rito nao acaba): o core e o selo da v385, o um.py v386 (do ensaio a seco) e um stdout PARCIAL sem RITO_RC;
   a cadeia tem de detectar «o rito ainda nao selou v386» e parar limpo (espera: tempo esgotado; leitura: PROBLEMAS; superficies: recusa, nada escrito);
 - V386 (o padrao): um selo v386 SINTETICO -- o core v385 + as 110 bandeiras e as 110 entradas do axiom_report LIDAS do relatorio do kernel do sandbox
   + a escada da v386 + o pilar na forma REAPROVEITADA (a pasta = a copia de bytes do cache da v385 no pacote, pilar_anterior_v385_*) + os quatro registros
   v386 calculados pelas PROPRIAS funcoes do candidato (importado de dry_v386, como no ensaio a seco; o import nao roda o rito; o ramo B le o V1 real da
   Bancada, so leitura); selo: o da v385 + as chaves do W07 extraidas do candidato, timestamp e chave SINTETICO_ENSAIO_V386; stdout: o da v385 com o reuse,
   a escada da v386 e as linhas [v386]; os .txt/.toc do artigo e os .md do ensaio a seco (marca [SINTETICO] no FIM dos .txt: a linha 2 fica intacta para o W10).
Escreve SO em v386_selo\\ensaio_nos_sintetico (e ensaio_horarios_v386_SINTETICO.txt ao lado)."""
import ast, glob, hashlib, io, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
NOS = A.NOS_REAL; PK = A.PK; DAT = A.DAT
OUT = os.path.join(HERE, 'ensaio_nos_sintetico')
HOR = os.path.join(HERE, 'ensaio_horarios_v386_SINTETICO.txt')
MODO = os.environ.get('V386_SINT_MODO', 'V386'); assert MODO in ('V386', 'AINDA_V385'), MODO
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, 'rb').read()
assert os.path.realpath(OUT).lower().startswith(os.path.realpath(HERE).lower() + os.sep)
if os.path.isdir(OUT):
    assert os.path.exists(os.path.join(OUT, A.MARCA_SINT)), 'a pasta de saida existe e NAO e sintetica -- nao apago'
    shutil.rmtree(OUT)
os.makedirs(OUT)


def w(rel, b):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p + '.tmp', 'wb') as f:
        f.write(b)
    assert os.path.getsize(p + '.tmp') == len(b); os.replace(p + '.tmp', p)
    return p


MARCA = ('SINTETICO -- ENSAIO DA CADEIA POS-RITO v386 (gerencia auxiliar, sessao 6da8f00d). NAO E O RITO. NAO E RESULTADO. '
         'Montado por montar_nos_sintetico_v386.py a partir dos backups de bytes da v385 selada, do ensaio a seco da v386 e do kernel do sandbox (modo %s).' % MODO)
w(A.MARCA_SINT, (MARCA + '\n').encode('utf-8'))
AP = json.load(open(sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v386.json'), encoding='utf-8'))
CM = json.load(open(os.path.join(PK, 'CANDIDATO_v386.json'), encoding='utf-8'))
# ---- a base: a v385 selada, pelos backups de bytes do instalador (conferidos contra o APLICADO)
base = {}
for nm in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md', 'um_absoluto_pilar_quantico.json'):
    b = rb(AP['backups'][nm]['backup'])
    assert sha(b)[:16] == AP['backups'][nm]['sha16'], nm
    base[nm] = b
R0 = json.loads(base['um_absoluto.json'].decode('utf-8')); S0 = json.loads(base['um_absoluto_selo.json'].decode('utf-8'))
assert S0.get('um_version') == 'v385' and 'the_verb_v386' not in R0['core']
# ---- o um.py e o kernel: a copia do candidato do ensaio a seco
DRY = os.path.join(PK, 'dry_v386')
umb = rb(os.path.join(DRY, 'um.py'))
assert sha(umb)[:16] == AP['um_py_novo']['sha16'] == CM['sha16'] == ESP['candidato_sha16'], 'o um.py do ensaio a seco nao e o candidato instalado'
w('um.py', umb); UM64 = sha(umb)
STONE = 'TGLExt/TheVerbSelectsTheAction.lean'
sb = rb(os.path.join(DRY, 'tgl_kernel', *STONE.split('/'))); assert sha(sb)[:16] == ESP['kernel']['new'][STONE]
w(os.path.join('tgl_kernel', *STONE.split('/')), sb)
for _rel in ('TGLExt.lean', 'TGL/Audit.lean'):
    _b = rb(os.path.join(DRY, 'tgl_kernel', *_rel.split('/'))); assert sha(_b)[:16] == ESP['kernel']['changed'][_rel][1], _rel
    w(os.path.join('tgl_kernel', *_rel.split('/')), _b)
w(os.path.join('tgl_kernel', 'TGLExt', 'TheAxiomAndTheFalseWitness.lean'), rb(os.path.join(DRY, 'tgl_kernel', 'TGLExt', 'TheAxiomAndTheFalseWitness.lean')))
# ---- o stdout da v385 (selado; a base do sintetico)
so = open(os.path.join(NOS, 'rodada_v385_stdout.txt'), encoding='utf-8').read().replace('\r\n', '\n')
L = so.split('\n')
while L and (not L[-1].strip() or L[-1].startswith('RITO_RC=')):
    L.pop()
P385 = ESP['pilar_v385']
REUSE_LINE = "[v386] pilar quantico: REAPROVEITADO da rodada selada v385 de %s (chave %s) -- o pilar nao e' objeto desta versao (_QP_REUSE_V386)" % (R0['core']['quantum_pillar_v384'].get('finished'), P385['key'])
i_l = [k for k, l in enumerate(L) if l.startswith('[v384] pilar quantico: o trabalhador da GPU foi lancado')]; assert len(i_l) == 1
L[i_l[0]] = REUSE_LINE
if MODO == 'AINDA_V385':
    # o estado ATUAL: core/selo da v385 intocados; os .md e o pilar da v385; um stdout PARCIAL (as 6 primeiras linhas), sem RITO_RC; um horario so
    for nm in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md', 'um_absoluto_pilar_quantico.json'):
        w(nm, base[nm])
    w('rodada_v386_stdout.txt', ('[SINTETICO] ' + MARCA + '\n' + '\n'.join(L[:6]) + '\n').encode('utf-8'))
    with open(HOR + '.tmp', 'w', encoding='utf-8', newline='\n') as f:
        f.write('SINT-17:28:57\n')
    os.replace(HOR + '.tmp', HOR)
    for lg in ('pt', 'en'):
        w('um_absoluto_%s.txt' % lg, b'')   # nao se le o artigo vivo do Nos real (o rito o grava): vazio, dito
    w('SINTETICO_MODO_AINDA_V385.txt', b'o selo e o core sao os da v385 selada; o rito v386 ainda nao acabou (stdout parcial, sem RITO_RC)\n')
    print(json.dumps({'nos_sintetico': OUT, 'modo': MODO, 'um_py_sha16': UM64[:16], 'selo_um_version': S0.get('um_version'), 'horarios': HOR}, ensure_ascii=False, indent=1))
    sys.exit(0)
# ---- MODO V386: as funcoes do candidato (importado de dry_v386; o import nao roda o rito), conferidas contra o v386_runtime.py
KREP = json.load(open(os.path.join(DAT, 'kernel', 'sandbox_raiz_v386.json'), encoding='utf-8'))
AXR = json.load(open(os.path.join(DAT, 'kernel', 'sandbox_axiom_report_v386.json'), encoding='utf-8'))
AXR = AXR.get('axiom_report', AXR)
sys.path.insert(0, DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
assert os.path.normcase(um.FORMAL_DIR) == os.path.normcase(os.path.join(DRY, 'tgl_kernel')), um.FORMAL_DIR
assert um.UM_VERSION == 'v386' and um._QP_REUSE_V386 is True
ct = rb(os.path.join(PK, 'um_v386_candidato.py')).decode('utf-8').replace('\r\n', '\n'); assert sha(rb(os.path.join(PK, 'um_v386_candidato.py')))[:16] == CM['sha16']
rt = open(os.path.join(PK, 'v386_runtime.py'), encoding='utf-8').read().replace('\r\n', '\n')


def fatia(t, nome):
    i = t.index('\ndef %s(' % nome) + 1; j = t.find('\ndef ', i + 1)
    return t[i:(j if j >= 0 else len(t))].rstrip() + '\n'


for fn in ('the_verb_v386', 'quantum_pillar_reuse_v386', 'ramo_b_preregistration_v386', 'ledger_errata_v386'):
    assert fatia(rt, fn).rstrip() in ct, 'a funcao %s do v386_runtime.py nao esta, inteira, no candidato' % fn


def chaves(k):
    m = re.search(r'"%s": \{k_: \(core\.get\("%s"\) or \{\}\)\.get\(k_\) for k_ in \(([^)]*)\)\}' % (k, k), ct); assert m, k
    return ast.literal_eval('(' + m.group(1) + ')')


CH = {k: chaves(k) for k in ('quantum_pillar_v384', 'quantum_pillar_reproducibility_v385', 'the_verb_v386', 'ledger_errata_v386', 'ramo_b_preregistration_v386', 'quantum_pillar_reuse_v386')}
_lx = re.search(r'"the_verb_reading_v386": "([A-Z0-9_a-zA-Z]+)",', ct); assert _lx, 'a leitura do selo v386 nao foi achada no candidato'
LEIT = _lx.group(1)
# ---- o pilar na forma REAPROVEITADA: a pasta = a copia de bytes do cache da v385 no pacote (nao o cache real)
CDIR = AP['pilar_anterior_v385']['para']; assert os.path.isdir(CDIR)
assert sha(rb(os.path.join(CDIR, 'result.json'))) == P385['result_sha256'] == R0['core']['quantum_pillar_v384']['result_sha256']
QP = json.loads(json.dumps(R0['core']['quantum_pillar_v384']))
QP_REUSED = dict(QP, mode='REUSE', run_dir=CDIR, reuse={'reused': True, 'from_run_finished': QP.get('finished'), 'cache_dir': CDIR,
                                                        'reading': ESP['muda_e_e_dito']['quantum_pillar_v384_reuse']['v386_esperado']['reading']})
for k_ in ('worker_rc', 'timed_out'):
    QP_REUSED.pop(k_, None)
QP_REUSED['SINTETICO_ENSAIO_V386'] = MARCA
ST_REUSE = {'mode': 'REUSE', 'cache_dir': CDIR, 'key': QP['key'], 'checkpoint_switch': False}
# ---- o core: v385 + as 110 bandeiras e o axiom_report do sandbox + a escada da v386 + o pilar reaproveitado + os quatro registros (pelas funcoes do candidato)
C1 = json.loads(json.dumps(R0['core']))
FLAGS = ESP['flags_v386']
assert all(KREP['bandeiras'].get(f) is True for f in FLAGS)
kf = C1['kernel_formalization']
for f in FLAGS:
    kf[f] = True
kf['axiom_report'] = dict(kf.get('axiom_report') or {})
for f, n in ESP['nomes_lean_v386'].items():
    assert n in AXR, n
    kf['axiom_report'][n] = AXR[n]
C1['external_ladder'] = dict(C1['external_ladder']); C1['external_ladder']['n_theorems_clean'] = C1['external_ladder']['n_theorems_expected'] = ESP['escada_v386'][1]
C1['quantum_pillar_v384'] = QP_REUSED
_prev = um.quantum_pillar_previous_v385(ST_REUSE)
C1['quantum_pillar_reproducibility_v385'] = um.quantum_pillar_reproducibility_v385(_prev, QP_REUSED)
assert 'NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT' in C1['quantum_pillar_reproducibility_v385']['verdict']
C1['the_verb_v386'] = um.the_verb_v386(C1)
C1['ramo_b_preregistration_v386'] = um.ramo_b_preregistration_v386(C1)
C1['ledger_errata_v386'] = um.ledger_errata_v386(C1, C1['ramo_b_preregistration_v386'])
C1['quantum_pillar_reuse_v386'] = um.quantum_pillar_reuse_v386(ST_REUSE, QP_REUSED)
for k in ('the_verb_v386', 'ramo_b_preregistration_v386', 'ledger_errata_v386', 'quantum_pillar_reuse_v386'):
    assert C1[k]['all_verified'] is True, (k, C1[k]['verdict'])
R1 = dict(R0); R1['core'] = C1; R1['SINTETICO_ENSAIO_V386'] = MARCA
w('um_absoluto.json', json.dumps(R1, ensure_ascii=False, indent=1).encode('utf-8'))
S1 = dict(S0)
S1.update({'SINTETICO_ENSAIO_V386': MARCA, 'timestamp': '2026-10-05 19:30:00 SINTETICO', 'um_version': 'v386',
           'quantum_pillar_v384': {k: QP_REUSED.get(k) for k in CH['quantum_pillar_v384']},
           'quantum_pillar_reproducibility_v385': {k: C1['quantum_pillar_reproducibility_v385'].get(k) for k in CH['quantum_pillar_reproducibility_v385']},
           'the_verb_reading_v386': LEIT, 'verb_typing_stone_name_v386': C1['the_verb_v386'].get('token_from_kernel')})
for k in ('the_verb_v386', 'ledger_errata_v386', 'ramo_b_preregistration_v386', 'quantum_pillar_reuse_v386'):
    S1[k] = {kk: C1[k].get(kk) for kk in CH[k]}
S1['sha256'] = dict(S0.get('sha256') or {}); S1['sha256']['um.py'] = UM64; S1['sha256']['um_absoluto_pilar_quantico.json'] = P385['result_sha256']
S1['not_sealed_this_run'] = dict(S0.get('not_sealed_this_run') or {}); S1['not_sealed_this_run']['computacao_nao_concluida'] = []
w('um_absoluto_selo.json', json.dumps(S1, ensure_ascii=False, indent=2).encode('utf-8'))
w('um_absoluto_pilar_quantico.json', rb(os.path.join(CDIR, 'result.json')))
# ---- o stdout sintetico: o da v385 com o reuse, a escada da v386, a reprodutibilidade sob reuse e as linhas [v386]
n_es = 0
for k, l in enumerate(L):
    if re.search(r'teoremas limpos:\s*%d/%d' % (ESP['escada_v385'][0], ESP['escada_v385'][1]), l):
        L[k] = re.sub(r'teoremas limpos:\s*\d+/\d+', 'teoremas limpos: %d/%d' % (ESP['escada_v386'][1], ESP['escada_v386'][1]), l); n_es += 1
assert n_es >= 1, 'o stdout da v385 nao tem a linha da escada'
i_rp = [k for k, l in enumerate(L) if l.strip().startswith('[v385] a reprodutibilidade do pilar quantico')]; assert len(i_rp) == 1
L[i_rp[0]] = '   [v385] a reprodutibilidade do pilar quantico (a rodada desta versao contra a guardada pela anterior, mesma chave): %s' % C1['quantum_pillar_reproducibility_v385']['verdict']
j = max(k for k, l in enumerate(L) if '[v385] o Axioma e a testemunha falsa' in l)
L[j + 1:j + 1] = ['   [v386] o pilar quantico nesta rodada (reaproveitado da v385 pela chave, ou calculado de novo -- dito): %s' % C1['quantum_pillar_reuse_v386']['verdict'],
                  "   [v386] o Verbo seleciona (o Nome e' o posto; a leitura e' um peso; a ordem importa; verdade e custo duas faces; o tempo lido duas vezes; luz e gravidade indissociaveis; a fiacao angular na escada): %s" % C1['the_verb_v386']['verdict'],
                  '   [v386] o ramo B do ringdown pre-registrado por hash (outra lei, canal F2b; o conjunto D cego; nada aberto): %s' % C1['ramo_b_preregistration_v386']['verdict'],
                  '   [v386] a errata ao lado de R6 e a cobranca F2b (o livro v383 intacto): %s' % C1['ledger_errata_v386']['verdict']]
L = ['[SINTETICO] ' + MARCA] + L + ['RITO_RC=0']
w('rodada_v386_stdout.txt', ('\n'.join(L) + '\n').encode('utf-8'))
with open(HOR + '.tmp', 'w', encoding='utf-8', newline='\n') as f:
    f.write('SINT-17:28:57\nSINT-19:30:00\n')
os.replace(HOR + '.tmp', HOR)
# ---- os .txt/.toc do artigo e os .md do ensaio a seco (a marca [SINTETICO] no FIM dos .txt)
for lg in ('pt', 'en'):
    t = rb(os.path.join(DRY, 'dry_v386_%s.txt' % lg))
    w('um_absoluto_%s.txt' % lg, t + ('\n[SINTETICO] ' + MARCA + '\n').encode('utf-8'))
    w('um_absoluto_%s.toc' % lg, rb(os.path.join(DRY, 'dry_v386_%s.toc' % lg)))
for nm in ('um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
    w(nm, rb(os.path.join(DRY, nm)))
print(json.dumps({'nos_sintetico': OUT, 'modo': MODO, 'um_py_sha16': UM64[:16], 'verbo': C1['the_verb_v386']['verdict'][:80] + '...', 'ramo_b': C1['ramo_b_preregistration_v386']['verdict'][:80] + '...',
                  'errata': C1['ledger_errata_v386']['verdict'][:70] + '...', 'reuse': C1['quantum_pillar_reuse_v386']['verdict'][:80] + '...', 'repro_v385': C1['quantum_pillar_reproducibility_v385']['verdict'][:80],
                  'pasta_do_pilar': CDIR, 'chaves_do_selo_W07': {k: len(v) for k, v in CH.items()}, 'leitura_do_selo_v386': LEIT[:60] + '...', 'horarios': HOR}, ensure_ascii=False, indent=1))
