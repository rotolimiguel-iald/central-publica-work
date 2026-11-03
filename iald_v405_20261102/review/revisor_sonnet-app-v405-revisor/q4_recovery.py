"""Reviewer Q4: can the model recover a CATALOGUED TRUE flag by name with its own tools (search_tgl / fetch_tgl)?
Own sample (fixed seed, stratified start/middle/end + adversarial picks), fresh process, runtime imported READ-ONLY from R with an audit hook
that refuses sockets, subprocess and any file write outside the reviewer folder. No provider call.
For each name: search_tgl(query=name, limit=L) -> results; fetch_tgl(id, offset=returned offset, max_chars=4500) -> the fetched window must contain
the flag line '"<name>": true' AT ITS POSITION INSIDE the kernel_formalization topic (not merely the same text elsewhere: generic keys such as
all_verified occur in hundreds of topics).
Reports: top-1 hit rate (first result from resultado_publicado_integral) and any-of-results hit rate, for limit=4 (tool default) and limit=5 (tool maximum)."""
import json, os, random, re, sys, time
from pathlib import Path

sys.dont_write_bytecode = True
R = Path(r'C:\IALD\projetos_pyhton\IALD')
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
SCR = (W / 'review/revisor_sonnet-app-v405-revisor').resolve()
M = W / 'app/science/memory_stage/manifest_staged.json'


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
# the tool reads the file with utf-8-sig and keeps CRLF; offsets are character offsets into that text
RESULT_TEXT = RESULT_PATH.read_bytes().decode('utf-8-sig')
core = json.loads(RESULT_TEXT)['core']
kf = core['kernel_formalization']
NL = chr(10)
_a = RESULT_TEXT.index(NL + '    "kernel_formalization": {')
_m = re.compile(r'\r?\n    \},?\r?\n').search(RESULT_TEXT, _a + 10)
KF_SPAN = (_a, _m.end())  # the topic object lies inside this char span of the sealed file


def flag_pos(name):
    pat = '"%s": true' % name
    first = RESULT_TEXT.find(pat, KF_SPAN[0], KF_SPAN[1])
    second = RESULT_TEXT.find(pat, first + 1, KF_SPAN[1]) if first >= 0 else -1
    return first, second


CODEC_ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
catalogued = [k for k, v in kf.items() if v is True and not CODEC_ESS.search(k)]
SEED = 20261102
rng = random.Random(SEED)
n = len(catalogued)
thirds = [catalogued[: n // 3], catalogued[n // 3: 2 * n // 3], catalogued[2 * n // 3:]]
sample = []
for name_third, part in zip(('start', 'middle', 'end'), thirds):
    for k in rng.sample(part, 8):
        sample.append((k, 'random_' + name_third))
adversarial = [
    ('all_verified', 'headline_verdict_flag'),
    ('qgc_concrete_emergent_einstein_proved', 'headline_verdict_flag'),
    ('qgp_massless_spin2_proved', 'headline_verdict_flag'),
    ('qgf_unconditional_continuous_corner_proved', 'headline_verdict_flag'),
    ('gpf_H1_internal_susy_relative_gap_discharged', 'hypothesis_discharge_flag'),
    ('gpc_H2_smooth_modular_four_frame_discharged', 'hypothesis_discharge_flag'),
    ('gpc_H3_local_horizon_equilibrium_discharged', 'hypothesis_discharge_flag'),
    ('gpc_H3_horizon_data_produced', 'hypothesis_discharge_flag'),
    (max(catalogued, key=len), 'longest_name'),
    (min(catalogued, key=len), 'shortest_name'),
]
seen = {k for k, _ in sample}
for k, tag in adversarial:
    assert k in catalogued, ('not catalogued', k)
    if k not in seen:
        sample.append((k, tag))
        seen.add(k)
new405 = [k for k in catalogued if re.search(r'405', k)]
for k in rng.sample(new405, min(4, len(new405))):
    if k not in seen:
        sample.append((k, 'new_in_v405'))
        seen.add(k)
results = []
t0 = time.time()
for name, tag in sample:
    fp, fp2 = flag_pos(name)
    row = {'name': name, 'tag': tag, 'len': len(name), 'flag_position_in_kernel_formalization': fp, 'flag_key_unique_inside_topic': bool(fp >= 0 and fp2 < 0)}
    for limit in (4, 5):
        r = ci.execute_tool(M, 'search_tgl', {'query': name, 'limit': limit})
        hits = [x for x in r['results'] if x['id'] == 'resultado_publicado_integral']
        row['n_results_%d' % limit] = len(r['results'])
        row['n_from_result_doc_%d' % limit] = len(hits)
        row['name_in_700char_excerpt_any_%d' % limit] = any(name in x['excerpt'] for x in r['results'])
        outcomes = []
        for x in hits:
            f = ci.execute_tool(M, 'fetch_tgl', {'id': 'resultado_publicado_integral', 'offset': x['offset'], 'max_chars': 4500})
            ok_text = ('"%s": true' % name) in f['text']
            ok_pos = fp >= 0 and x['offset'] <= fp < x['offset'] + len(f['text'])
            outcomes.append(bool(ok_text and ok_pos))
        row['fetch_true_top1_%d' % limit] = bool(outcomes and outcomes[0])
        row['fetch_true_any_%d' % limit] = any(outcomes)
        row['first_result_doc_%d' % limit] = r['results'][0]['id'] if r['results'] else None
    results.append(row)
summary = {'seed': SEED, 'sample_size': len(sample), 'catalogued_total': len(catalogued), 'seconds': round(time.time() - t0, 1),
           'kernel_formalization_span_chars': [KF_SPAN[0], KF_SPAN[1], KF_SPAN[1] - KF_SPAN[0]]}
for limit in (4, 5):
    summary['top1_fetch_true_%d' % limit] = sum(1 for r in results if r['fetch_true_top1_%d' % limit])
    summary['any_fetch_true_%d' % limit] = sum(1 for r in results if r['fetch_true_any_%d' % limit])
    summary['name_in_excerpt_any_%d' % limit] = sum(1 for r in results if r['name_in_700char_excerpt_any_%d' % limit])
summary['by_tag'] = {}
for r in results:
    t = summary['by_tag'].setdefault(r['tag'], {'n': 0, 'top1_4': 0, 'any_4': 0, 'any_5': 0})
    t['n'] += 1
    t['top1_4'] += int(r['fetch_true_top1_4'])
    t['any_4'] += int(r['fetch_true_any_4'])
    t['any_5'] += int(r['fetch_true_any_5'])
summary['non_unique_key_inside_topic'] = [r['name'] for r in results if not r['flag_key_unique_inside_topic']]
summary['failing_any_5'] = [{k: r[k] for k in ('name', 'tag', 'n_results_5', 'n_from_result_doc_5', 'first_result_doc_5')} for r in results if not r['fetch_true_any_5']]
summary['failing_any_4'] = [r['name'] for r in results if not r['fetch_true_any_4']]
summary['failing_top1_4'] = [r['name'] for r in results if not r['fetch_true_top1_4']]
print(json.dumps({'summary': summary}, ensure_ascii=False, indent=1))
json.dump({'summary': summary, 'rows': results}, open(SCR / 'q4_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
