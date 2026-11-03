# -*- coding: utf-8 -*-
"""Reviewer r3 Q4: recovery of CATALOGUED TRUE flags by the recipe EXACTLY as written in the r3 reading:
  "search_tgl com o nome exato e limit 5; depois, para cada resultado dessa fonte, fetch_tgl id=resultado_publicado_integral com offset igual ao do resultado menos 2000."
NEW sample of mine (seed 405111, different from r1's 20261102 and the builder's 20261102): 3 strata x 100 random + all 113 red_ names + edge cases (r1 hard names, builder's failure,
the 14 names of clause-C imprecision, longest/shortest, mixed-case, pure-number family suffix). Fresh process, runtime imported READ-ONLY from R with an audit hook (no sockets, no subprocess,
no write outside the reviewer folder), no provider call.
Two variants of the same recipe: V_default = fetch_tgl WITHOUT max_chars (tool default 4000 -> window [off-2000, off+2000)); V_4500 = max_chars 4500 (tool maximum).
Success (strict) = the fetched window contains the line '"<name>": true' AT ITS POSITION INSIDE kernel_formalization; success (loose) = the text '"<name>": true' anywhere in the window.
Models follow 'for each result of that source' -> any result counts; first-result-only also reported."""
import json, os, random, re, sys, time
from pathlib import Path

sys.dont_write_bytecode = True
R = Path(r'C:\IALD\projetos_pyhton\IALD')
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
SCR = (W / 'review/revisor_sonnet-app-v405-revisor').resolve()
M = W / 'app/science/memory_stage/manifest_staged.json'
LIMIT_N = int(sys.argv[1]) if len(sys.argv) > 1 else None  # smoke test


def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('blocked ' + event)
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        p = Path(os.fsdecode(path)).resolve()
        if p.name in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json'):
            raise RuntimeError('private input forbidden')
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and not p.is_relative_to(SCR):
            raise RuntimeError('write outside reviewer folder: ' + str(p))


sys.addaudithook(guard)
sys.path.insert(0, str(R))
import iald_core_indexado as ci

RESULT_PATH = Path(json.loads(M.read_bytes())['published_evidence']['result']['path'])
TEXT = RESULT_PATH.read_bytes().decode('utf-8-sig')
core = json.loads(TEXT)['core']
kf = core['kernel_formalization']
NL = chr(10)
_a = TEXT.index(NL + '    "kernel_formalization": {')
_m = re.compile(r'\r?\n    \},?\r?\n').search(TEXT, _a + 10)
KF = (_a, _m.end())


def flag_pos(name):
    pat = '"%s": true' % name
    first = TEXT.find(pat, KF[0], KF[1])
    second = TEXT.find(pat, first + 1, KF[1]) if first >= 0 else -1
    return first, second


# catalogue = TRUE flags that are NOT literal in the r3 capsule (recomputed from the capsule with my own decoder)
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L
P3 = L.parse_prefix((W / 'app/packages/haiku_expanded/prefix.md').read_text('utf-8'))
kind, dv = L.decode_block(P3, 'kernel_formalization')
lit_true = {k for k, v in dv.items() if v is True}
catalogued = [k for k, v in kf.items() if v is True and k not in lit_true]
SEED = 405111
rng = random.Random(SEED)
n = len(catalogued)
thirds = [catalogued[: n // 3], catalogued[n // 3: 2 * n // 3], catalogued[2 * n // 3:]]
sample, seen = [], set()


def add(k, tag):
    if k in catalogued and k not in seen:
        sample.append((k, tag))
        seen.add(k)


for tag, part in zip(('random_start', 'random_middle', 'random_end'), thirds):
    for k in rng.sample(part, 100):
        add(k, tag)
for k in [x for x in catalogued if x.startswith('red_')]:
    add(k, 'red_family_all')
for k in ('ext_vrd_eInner_kernel_checked', 'ext_net394r7_01827', 'ext_net394_0646', 'ext_psb395_0011', 'ext_mtp405_0024', 'ext_ldd405_0034', 'ext_dde405_0006', 'ext_obt405_0031', 'ext_no_symmetric_kernel_proved'):
    add(k, 'edge_known_hard')
for k in ('ext_isq_light_H2v32_by_citation_kernel_proved', 'ext_isq_light_H3v32_by_citation_kernel_proved', 'ext_cq32_contract_H2v32_type_kernel_checked', 'ext_lig_NamedAtlasH3_kernel_checked'):
    add(k, 'edge_H_embedded')
for k in [x for x in catalogued if re.search(r'verifies', x)]:
    add(k, 'edge_verifies')
add(max(catalogued, key=len), 'edge_longest')
add(min(catalogued, key=len), 'edge_shortest')
mixed = [x for x in catalogued if re.search(r'[a-z][A-Z]', x)]
for k in rng.sample(mixed, min(20, len(mixed))):
    add(k, 'edge_mixed_case')
numeric = [x for x in catalogued if re.search(r'_\d{3,}$', x)]
for k in rng.sample(numeric, min(20, len(numeric))):
    add(k, 'edge_numeric_suffix')
if LIMIT_N:
    sample = sample[:LIMIT_N]
rows = []
t0 = time.time()
for name, tag in sample:
    fp, fp2 = flag_pos(name)
    row = {'name': name, 'tag': tag, 'flag_pos': fp, 'unique_in_topic': bool(fp >= 0 and fp2 < 0)}
    r = ci.execute_tool(M, 'search_tgl', {'query': name, 'limit': 5})
    hits = [x for x in r['results'] if x['id'] == 'resultado_publicado_integral']
    row['n_results'] = len(r['results'])
    row['n_from_source'] = len(hits)
    for variant, kw in (('default', {}), ('m4500', {'max_chars': 4500})):
        loose_any = strict_any = False
        loose_first = strict_first = False
        rank = None
        delta = None
        for i, x in enumerate(hits):
            f = ci.execute_tool(M, 'fetch_tgl', dict({'id': 'resultado_publicado_integral', 'offset': max(0, x['offset'] - 2000)}, **kw))
            t = f['text']
            loose = ('"%s": true' % name) in t
            strict = bool(loose and fp >= 0 and f['offset'] <= fp < f['offset'] + len(t))
            if i == 0:
                loose_first, strict_first = loose, strict
            if strict and not strict_any:
                strict_any, rank = True, i + 1
                delta = fp - x['offset']
            loose_any = loose_any or loose
            if strict_any:
                break
        row[variant] = {'strict_any': strict_any, 'loose_any': loose_any, 'strict_first_result': strict_first, 'loose_first_result': loose_first, 'rank_of_first_strict_hit': rank, 'flag_minus_result_offset': delta}
    rows.append(row)
summary = {'seed': SEED, 'sample_size': len(rows), 'catalogued_total': len(catalogued), 'seconds': round(time.time() - t0, 1), 'recipe': 'search_tgl(query=nome exato, limit=5); para cada resultado de resultado_publicado_integral: fetch_tgl(id, offset=max(0, offset-2000))'}
for v in ('default', 'm4500'):
    summary[v] = {'strict_any': sum(r[v]['strict_any'] for r in rows), 'loose_any': sum(r[v]['loose_any'] for r in rows), 'strict_first_result': sum(r[v]['strict_first_result'] for r in rows),
                  'failures_strict': [r['name'] for r in rows if not r[v]['strict_any']], 'failures_loose': [r['name'] for r in rows if not r[v]['loose_any']]}
    deltas = [r[v]['flag_minus_result_offset'] for r in rows if r[v]['flag_minus_result_offset'] is not None]
    summary[v]['delta_flag_minus_result_offset'] = {'min': min(deltas), 'max': max(deltas), 'n_ge_2000': sum(1 for d in deltas if d >= 2000), 'n_ge_2500': sum(1 for d in deltas if d >= 2500)} if deltas else None
    summary[v]['rank_of_first_hit'] = {str(k): sum(1 for r in rows if r[v]['rank_of_first_strict_hit'] == k) for k in (1, 2, 3, 4, 5)}
summary['by_tag'] = {}
for r in rows:
    t = summary['by_tag'].setdefault(r['tag'], {'n': 0, 'default_strict': 0, 'm4500_strict': 0})
    t['n'] += 1
    t['default_strict'] += int(r['default']['strict_any'])
    t['m4500_strict'] += int(r['m4500']['strict_any'])
summary['n_results_from_source_distribution'] = {str(k): sum(1 for r in rows if r['n_from_source'] == k) for k in range(0, 6)}
summary['non_unique_key_inside_topic'] = [r['name'] for r in rows if not r['unique_in_topic']]
print(json.dumps({'summary': summary}, ensure_ascii=False, indent=1))
if not LIMIT_N:
    json.dump({'summary': summary, 'rows': rows}, open(SCR / 'r3' / 'q4_r3_rows.json', 'w', encoding='utf8'), ensure_ascii=False)
