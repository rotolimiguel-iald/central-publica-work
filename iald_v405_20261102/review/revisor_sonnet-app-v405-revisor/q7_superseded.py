"""Reviewer Q7a: the superseded gate-flag wording ('15 calculadas e 3 literais' / '15 computed and 3 literal') in
 (1) the RAW and DECODED text of every package prefix, (2) every text the app can hand to a model (operational core, mother kernel, native prefix, JEV control/packet, manifests),
 (3) every file of the build folder (the builder's grep_superseded_check.py scope, re-run here with output inside the reviewer folder), (4) the pinned public git blobs.
Strict + loose patterns; marker = nearby text saying the wording was superseded / kept as record. Read-only."""
import json, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L

W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
REPO = Path(r'C:\IALD\Artigo\the_boundary')
C1 = json.loads((W / 'app/RELEASE.json').read_bytes())['espelho_commit']
SEP = r'[\s\W_]{1,12}'
OLD = [re.compile(r'15' + SEP + r'(?:as' + SEP + r')?(?:calculad\w*|computad\w*|computed|calculated)' + SEP + r'(?:e|and|plus|\+|mais|com)?' + SEP + r'3' + SEP + r'(?:as' + SEP + r')?liter\w*', re.I),
       re.compile(r'(?:15|quinze)' + SEP + r'(?:bandeiras' + SEP + r')?(?:calculad\w*|computed|calculated)', re.I),
       re.compile(r'\b(?:3|tres|três|three)' + SEP + r'(?:flags' + SEP + r'|bandeiras' + SEP + r')?(?:literais|literal|literals)\b', re.I)]
NEW = [re.compile(r'18' + SEP + r'(?:de' + SEP + r'18' + SEP + r')?(?:bandeiras' + SEP + r')?(?:calculad\w*|computed)[^\n]{0,200}?\b0' + SEP + r'liter\w*', re.I),
       re.compile(r'todas' + SEP + r'(?:as' + SEP + r')?(?:18' + SEP + r')?(?:bandeiras' + SEP + r')?calculad', re.I)]
MARKS = re.compile(r'v403|supera|ficam? como registro|verdadeiros? na sua data|stay as (?:a )?record|remain as (?:a )?record|recomput|passa a ler|diziam|substitu', re.I)
out = {'packages': {}, 'other_texts': {}, 'build_folder_scan': {}, 'git_blobs': {}}


def topic_at(text, pos):
    hs = [m for m in re.finditer(r'(?m)^### ([^\n]+)$', text) if m.start() <= pos]
    return hs[-1][1] if hs else None


for pkg in ('haiku_expanded', 'shared', 'sonnet_public'):
    t = (W / 'app/packages' / pkg / 'prefix.md').read_text('utf-8')
    rec = {'bytes': len(t.encode()), 'raw': {}, 'decoded': {}}
    for k, rx in enumerate(OLD):
        rec['raw']['old%d' % k] = [{'topic': topic_at(t, m.start()), 'text': t[m.start():m.end()][:90].replace('\n', ' '), 'marker_nearby': bool(MARKS.search(t[max(0, m.start() - 700):m.end() + 700]))} for m in rx.finditer(t)]
    rec['raw_new_counts'] = {'new%d' % k: len(list(rx.finditer(t))) for k, rx in enumerate(NEW)}
    P = L.parse_prefix(t)
    dec_hits = {}

    def scan(s, where):
        for k, rx in enumerate(OLD):
            for mm in rx.finditer(s):
                dec_hits.setdefault('old%d' % k, []).append({'where': where, 'text': s[mm.start():mm.end()][:90], 'marker_nearby': bool(MARKS.search(s[max(0, mm.start() - 700):mm.end() + 700]))})
    for lid, val in P['D'].items():
        dv = L.dec_lit(val, P['D'], P['E'])
        scan(dv if isinstance(dv, str) else json.dumps(L.canon(dv), ensure_ascii=False), 'DICT:' + lid)
    for n in P['body']:
        kind, dv = L.decode_block(P, n)
        if kind == 'JSON':
            scan(json.dumps(L.canon(dv), ensure_ascii=False), 'TOPIC:' + n)
        else:
            scan(dv, 'TEXT:' + n)
    scan(P['E'], 'EXPOSITION')
    rec['decoded'] = dec_hits
    rec['has_bandeiras_do_gate_v403_block'] = ('### bandeiras_do_gate_v403\n' in t)
    out['packages'][pkg] = rec
summary = {}
for pkg, r in out['packages'].items():
    s = {'bytes': r['bytes']}
    for k in ('old0', 'old1', 'old2'):
        s['RAW_' + k] = [(h['topic'], h['text'], h['marker_nearby']) for h in r['raw'][k]]
        s['DEC_' + k] = [(h['where'], h['text'], h['marker_nearby']) for h in r['decoded'].get(k, [])]
    s['RAW_new_counts'] = r['raw_new_counts']
    summary[pkg] = s
out['packages'] = summary


def scan_text(name, text):
    rows = []
    for k, rx in (('strict', OLD[0]), ('loose', OLD[2])):
        for m in rx.finditer(text):
            ctx = text[max(0, m.start() - 700):m.end() + 700]
            rows.append((k, m.start(), bool(MARKS.search(ctx)), text[max(0, m.start() - 90):m.end() + 110].replace('\n', ' ')))
    return {'bytes': len(text.encode()), 'strict': sum(1 for r in rows if r[0] == 'strict'), 'loose': sum(1 for r in rows if r[0] == 'loose'), 'unmarked': [(r[0], r[1], r[3]) for r in rows if not r[2]][:6]}


st = W / 'app/science/memory_stage'
for n in ['IALD_TGL_MEMORY_CORE.md', 'IALD_Kernel_v5.txt', 'core_packet_v405_bound.txt', 'jev_control_v405.json', 'iald_nucleo_fixo.json', 'manifest_install.json']:
    out['other_texts']['stage/' + n] = scan_text(n, (st / n).read_text('utf-8'))
out['other_texts']['app/native_prefix.md'] = scan_text('native', (W / 'app/native_prefix.md').read_text('utf-8'))
# build folder scan (every non-backup file except the reviewer folder), builder's scope
rows = []
scanned = 0
for p in sorted(W.rglob('*')):
    if not p.is_file() or p.suffix == '.pyc' or '.bak_' in p.name:
        continue
    rel = p.relative_to(W)
    if rel.parts[0] in ('review',):
        continue
    scanned += 1
    t = p.read_bytes().decode('utf-8', 'replace')
    for kind, rx in (('strict', OLD[0]), ('loose_3_literal', OLD[2])):
        for m in rx.finditer(t):
            ctx = t[max(0, m.start() - 600):m.end() + 700]
            rows.append({'file': str(rel), 'kind': kind, 'offset': m.start(), 'marker': bool(MARKS.search(ctx)), 'excerpt': t[max(0, m.start() - 80):m.end() + 120].replace('\n', ' ')[:260]})
unmarked = [r for r in rows if not r['marker']]
byfile = {}
for r in rows:
    d = byfile.setdefault(r['file'], {'strict': 0, 'loose_3_literal': 0, 'all_marked': True})
    d[r['kind']] += 1
    d['all_marked'] &= r['marker']
out['build_folder_scan'] = {'files_scanned': scanned, 'hits_total': len(rows), 'strict_hits': sum(r['kind'] == 'strict' for r in rows), 'unmarked_hits': len(unmarked), 'by_file': byfile, 'unmarked_excerpts': unmarked[:15]}


def git(*a):
    return subprocess.check_output(['git', '-c', 'safe.directory=' + REPO.as_posix(), '-c', 'core.quotepath=false', '-C', str(REPO), *a])


pub = json.loads((W / 'app/PUBLIC_GIT_BINDING.json').read_bytes())['sources']
for rel in pub:
    if rel.endswith(('um.py', 'um_absoluto.json', 'proof_manifest.json')):
        continue
    out['git_blobs']['git@' + C1[:8] + '/' + rel] = scan_text(rel, git('show', C1 + ':' + rel).decode('utf-8', 'replace'))
print(json.dumps(out, ensure_ascii=False, indent=1))
