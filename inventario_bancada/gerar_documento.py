# -*- coding: utf-8 -*-
# Gera INVENTARIO_BANCADA_CHATGPT.md (+ .json) a partir de inventario_bancada.json -- tudo LIDO, nada digitado.
import json, os, re, collections, hashlib, time, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'inventario_bancada.json'), encoding='utf-8'))
TUN = r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT'
FP = os.path.join(TUN, 'FECHAMENTO_PARCIAL_016')
leans = R['lean']
orig = [x for x in leans if not x['no_kernel_canonico']]
by = collections.defaultdict(list)
for x in orig:
    by[x['sha16']].append(x)
uniq = []
for s, v in by.items():
    v = sorted(v, key=lambda z: z['mtime'])
    u = dict(v[0]); u['copias'] = len(v); u['caminhos_das_copias'] = [z['arquivo'] for z in v][:8]
    uniq.append(u)
# familias de versao: mesmo nome-base sem _vN
def base(p):
    n = os.path.basename(p)[:-5]
    return re.sub(r'_v\d+$', '', n)
fam = collections.defaultdict(list)
for u in uniq:
    fam[base(u['arquivo'])].append(u)
def vnum(p):
    m = re.search(r'_v(\d+)\.lean$', p); return int(m.group(1)) if m else 1
vig = {}
for b, us in fam.items():
    us.sort(key=lambda z: (vnum(z['arquivo']), z['mtime']))
    vig[b] = us[-1]['sha16']
# o que esta no kernel canonico (por nome-base, na pasta O16 ou TGLExt)
ker = set()
KER = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel'
for dp, dn, fn in os.walk(KER):
    dn[:] = [d for d in dn if d != '.lake']
    for f in fn:
        if f.endswith('.lean'):
            ker.add(f[:-5])
temas = collections.defaultdict(list)
for u in uniq:
    for t in (u['temas'] or ['sem_tema']):
        temas[t].append(u)
pastas = collections.Counter(u['arquivo'].split('/')[0] if '/' in u['arquivo'] else '(raiz)' for u in uniq)
# os quadros de estatuto da propria bancada
quadro = []
try:
    Q = json.load(open(os.path.join(FP, 'P1_QUADRO.json'), encoding='utf-8'))
    L = Q if isinstance(Q, list) else (Q.get('itens') or Q.get('items') or [])
    for it in L:
        quadro.append({'item': it.get('item'), 'status': it.get('status'), 'escopo': it.get('scope'),
                       'hipoteses_abertas': it.get('named_open_hypotheses') or [], 'n_declaracoes': len(it.get('declarations') or [])})
except Exception as e:
    quadro = [{'erro': repr(e)}]
hip = []
try:
    H = json.load(open(os.path.join(FP, 'P3_HIPOTESES_ABERTAS.json'), encoding='utf-8'))
    for h in (H if isinstance(H, list) else []):
        hip.append({'nome': h.get('name'), 'itens': h.get('items'), 'status': h.get('status'), 'onde_descarregar': (h.get('discharge_at') or '')[:200]})
except Exception as e:
    hip = [{'erro': repr(e)}]
docs = sorted(R['docs'], key=lambda d: d['mtime'])
ent = [d for d in docs if 'TUNEL/DO_CHATGPT' in d['arquivo'] or os.path.basename(d['arquivo']).startswith('ENTREGA_')]

sha_inv = hashlib.sha256(open(os.path.join(HERE, 'inventario_bancada.json'), 'rb').read()).hexdigest()[:16]
L = []
L += ['# INVENTÁRIO DA BANCADA DO CHATGPT — tudo o que foi examinado e produzido', '',
      '> Gerado por script em %s a partir da varredura `inventario_bancada.json` (sha16 `%s`), SÓ LEITURA da pasta `Chatgpt\\`. Nenhum número digitado.' % (R['gerado_em'], sha_inv),
      '> **Ordem do operador (27/09/2026, verbatim):** «Precisamos fazer um inventário de tudo que foi examinado e produzido na bancada do chatgpt pra não nos perdermos mais em serviço já executado, vc está pedindo o que já pediu» e «Depois de inventariar tudo, precisamos indexar ao atlas da tgl para ficar referenciado».',
      '> **Regra de uso:** ANTES de pedir qualquer construção à bancada ou de construí-la na gerência, procurar aqui (por tema, por nome, por hash). O que é sabido e importável não se prova de novo (regra do operador de 27/08: «prova emprestada»).', '',
      '## 1. Os números', '',
      '| medida | valor |', '|---|---|',
      '| arquivos `.lean` varridos (sem `.lake`) | %d |' % R['n_lean'],
      '| … que são CÓPIA do kernel canônico (cada ordem traz a sua) | %d |' % R['n_lean_no_kernel'],
      '| … da própria bancada (fora do kernel) | %d |' % len(orig),
      '| conteúdos `.lean` ÚNICOS da bancada | %d |' % len(uniq),
      '| declarações nesses únicos | %d |' % sum(u['n_decl'] for u in uniq),
      '| famílias de versão (mesmo nome-base, _v1…_vN) | %d |' % len(fam),
      '| únicos cujo nome-base JÁ está no kernel canônico | %d |' % sum(1 for u in uniq if base(u['arquivo']) in ker or os.path.basename(u['arquivo'])[:-5] in ker),
      '| únicos com `sorry`/`admit`/`native_decide` fora de comentário | %d |' % sum(1 for u in uniq if u['tokens_proibidos_fora_de_comentario']),
      '| únicos que declaram `axiom` | %d |' % sum(1 for u in uniq if u['declara_axiom']),
      '| documentos de entrega/quadro/relatório/medida | %d |' % R['n_docs'], '',
      '## 2. O quadro de estatutos da própria bancada (FECHAMENTO_PARCIAL_016, P1)', '',
      '| item | estatuto | escopo | hipóteses nomeadas em aberto | nº de declarações |', '|---|---|---|---|---|']
for q in quadro:
    L.append('| %s | %s | %s | %s | %s |' % (q.get('item'), q.get('status'), str(q.get('escopo') or '').replace('|', '/')[:180], ', '.join(q.get('hipoteses_abertas') or []), q.get('n_declaracoes')))
L += ['', '## 3. As hipóteses nomeadas em aberto (P3) — o que se IMPORTA por citação ou ainda se deve', '',
      '| hipótese | itens | estatuto | onde se descarregaria |', '|---|---|---|---|']
for h in hip:
    L.append('| `%s` | %s | %s | %s |' % (h.get('nome'), h.get('itens'), h.get('status'), str(h.get('onde_descarregar') or '').replace('|', '/')))
L += ['', '## 4. Por tema (arquivos únicos; a versão VIGENTE de cada família marcada ★)', '']
for t in sorted(temas, key=lambda k: -len(temas[k])):
    us = sorted(temas[t], key=lambda z: z['mtime'])
    L.append('### %s — %d arquivos' % (t, len(us)))
    L.append('')
    L.append('| ★ | arquivo | sha16 | decl | cópias | no kernel? | data | declarações (até 6) |')
    L.append('|---|---|---|---|---|---|---|---|')
    for u in us:
        star = '★' if vig.get(base(u['arquivo'])) == u['sha16'] else ''
        nk = 'sim' if (base(u['arquivo']) in ker or os.path.basename(u['arquivo'])[:-5] in ker) else ''
        ds = '; '.join(d.split(' ', 1)[-1] for d in u['decls'][:6])
        L.append('| %s | `%s` | `%s` | %d | %d | %s | %s | %s |' % (star, u['arquivo'], u['sha16'], u['n_decl'], u['copias'], nk, u['mtime'], ds.replace('|', '/')))
    L.append('')
L += ['## 5. Pastas da bancada (conteúdos `.lean` únicos por pasta)', '', '| pasta | únicos |', '|---|---|']
for p, n in pastas.most_common():
    L.append('| `%s` | %d |' % (p, n))
L += ['', '## 6. Entregas e documentos (em ordem de data)', '', '| data | arquivo | sha16 | título |', '|---|---|---|---|']
for d in docs:
    L.append('| %s | `%s` | `%s` | %s |' % (d['mtime'], d['arquivo'], d['sha16'], str(d['titulo']).replace('|', '/')[:160]))
neg = [u for u in uniq if u['tokens_proibidos_fora_de_comentario'] or u['declara_axiom']]
L += ['', '## 7. Arquivos com `sorry`/`admit` ou `axiom` (NÃO importar sem exame)', '',
      'Todos os achados estão em pastas de CONTROLE NEGATIVO (mutantes do auditor, sondas, sintéticos) — existem para provar que o auditor morde; não são entregas.', '',
      '| arquivo | tokens | axiom | data |', '|---|---|---|---|']
for u in sorted(neg, key=lambda z: z['arquivo']):
    L.append('| `%s` | %s | %s | %s |' % (u['arquivo'], ', '.join(u['tokens_proibidos_fora_de_comentario']) or '—', 'sim' if u['declara_axiom'] else '—', u['mtime']))
assert all(re.search(r'mutante|mutations|C_controles|probes|sinteticos|autoteste', u['arquivo']) for u in neg), 'achado FORA de pasta de controle -- examinar'
L += ['', '---', 'Estatuto: inventário [REAL — medido por varredura]; os estatutos das seções 2–3 são os DA BANCADA (lidos dos quadros dela), não da gerência. Nada aqui move o gate. PROVADA ≠ CONFIRMADA.']
md = '\n'.join(L) + '\n'
open(os.path.join(HERE, 'INVENTARIO_BANCADA_CHATGPT.md'), 'w', encoding='utf-8', newline='\n').write(md)
J = {'gerado_em': R['gerado_em'], 'varredura_sha16': sha_inv, 'numeros': {'n_lean': R['n_lean'], 'n_copias_kernel': R['n_lean_no_kernel'], 'n_bancada': len(orig), 'n_unicos': len(uniq), 'n_decl_unicos': sum(u['n_decl'] for u in uniq), 'n_familias': len(fam), 'n_docs': R['n_docs']},
     'quadro_P1': quadro, 'hipoteses_P3': hip, 'unicos': [{k: u[k] for k in ('arquivo', 'sha16', 'n_decl', 'copias', 'temas', 'mtime', 'decls', 'caminhos_das_copias', 'tokens_proibidos_fora_de_comentario', 'declara_axiom')} | {'vigente': vig.get(base(u['arquivo'])) == u['sha16']} for u in uniq],
     'documentos': docs}
json.dump(J, open(os.path.join(HERE, 'INVENTARIO_BANCADA_CHATGPT.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('md', len(md.encode('utf-8')), 'B; json', os.path.getsize(os.path.join(HERE, 'INVENTARIO_BANCADA_CHATGPT.json')), 'B')
print(json.dumps(J['numeros'], ensure_ascii=False))
print('temas:', {t: len(v) for t, v in temas.items()})
