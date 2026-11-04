"""Revisor sonnet-app-v406-revisor -- QC: Q5 (R3-2 e recuperacao).
Exercita a receita ENSINADA pela capsula do haiku55, sem provedor e sem rede, com o runtime importado SO PARA LEITURA (gancho de auditoria recusa socket, subprocess,
os.system e qualquer escrita fora da pasta do revisor):
  search_tgl(query=<nome exato>, limit=5); para cada resultado de resultado_publicado_integral: fetch_tgl(id=resultado_publicado_integral, offset=max(0, offset-2000), max_chars=4500)
O nome e' dado como recuperado se a janela devolvida contem '"<nome>": true'; metrica mais forte: a janela cobre a posicao da bandeira DENTRO do topico kernel_formalization.
Amostra: semente do revisor (NAO 20261103), catalogo recomputado do selado v406 com a regra da capsula (independente do haiku_codec)."""
import json, os, random, re, sys, time
from pathlib import Path

sys.dont_write_bytecode = True
SEED = 40640406
N_RANDOM = 450
R = Path(r'C:\IALD\projetos_pyhton\IALD')
W = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
SCR = Path(__file__).resolve().parent
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

manifest = json.loads(M.read_bytes())
RESULT_PATH = Path(manifest['published_evidence']['result']['path'])
RESULT_TEXT = RESULT_PATH.read_bytes().decode('utf-8-sig')
core = json.loads(RESULT_TEXT)['core']
kf = core['kernel_formalization']
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
WHOLE = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I)
KEEP = re.compile(r'H[123]|discharg|condition|verif', re.I)
catalogued = [k for k, v in kf.items() if v is True and re.match(r'(?:ext|red)_', k) and not (WHOLE.search(k) or ESS.search(k) or KEEP.search(k))]
NL = chr(10)
a = RESULT_TEXT.index(NL + '    "kernel_formalization": {')
mm = re.compile(r'\r?\n    \},?\r?\n').search(RESULT_TEXT, a + 10)
SPAN = (a, mm.end())


def flag_pos(name):
    pat = '"%s": true' % name
    first = RESULT_TEXT.find(pat, SPAN[0], SPAN[1])
    second = RESULT_TEXT.find(pat, first + 1, SPAN[1]) if first >= 0 else -1
    return first, second


rng = random.Random(SEED)
sample = [(k, 'random') for k in rng.sample(catalogued, N_RANDOM)]
seen = {k for k, _ in sample}
cs = set(catalogued)
extra = []
extra += [(k, 'shortest') for k in sorted(catalogued, key=len)[:25]]
extra += [(k, 'longest') for k in sorted(catalogued, key=len, reverse=True)[:25]]
prefix_of_other = [k for k in catalogued if any(o != k and o.startswith(k) for o in rng.sample(catalogued, 400))]
extra += [(k, 'proper_prefix_of_another') for k in prefix_of_other[:30]]
new406 = [k for k in catalogued if '406' in k]
extra += [(k, 'new_406') for k in rng.sample(new406, min(30, len(new406)))]
for k, tag in extra:
    if k not in seen:
        sample.append((k, tag)); seen.add(k)
t0 = time.time()
rows = []
for name, tag in sample:
    fp, fp2 = flag_pos(name)
    row = {'name': name, 'tag': tag, 'len': len(name), 'pos': fp, 'unique_in_topic': bool(fp >= 0 and fp2 < 0)}
    r = ci.execute_tool(M, 'search_tgl', {'query': name, 'limit': 5})
    hits = [x for x in r['results'] if x['id'] == 'resultado_publicado_integral']
    row['n_results'], row['n_from_result_doc'] = len(r['results']), len(hits)
    ok_text = ok_pos = False
    first_hit_ok = False
    for i, x in enumerate(hits):
        f = ci.execute_tool(M, 'fetch_tgl', {'id': x['id'], 'offset': max(0, x['offset'] - 2000), 'max_chars': 4500})
        t = ('"%s": true' % name) in f['text']
        p = bool(fp >= 0 and max(0, x['offset'] - 2000) <= fp < max(0, x['offset'] - 2000) + len(f['text']))
        if i == 0:
            first_hit_ok = bool(t and p)
        ok_text = ok_text or t
        ok_pos = ok_pos or (t and p)
        if ok_text and ok_pos:
            break
    row.update(found_text=ok_text, found_in_topic=ok_pos, first_hit_ok=first_hit_ok)
    rows.append(row)
tot = len(rows)
fails_text = [r['name'] for r in rows if not r['found_text']]
fails_pos = [r['name'] for r in rows if not r['found_in_topic']]
by = {}
for r in rows:
    d = by.setdefault(r['tag'], {'n': 0, 'found_text': 0, 'found_in_topic': 0, 'first_hit_ok': 0})
    d['n'] += 1; d['found_text'] += int(r['found_text']); d['found_in_topic'] += int(r['found_in_topic']); d['first_hit_ok'] += int(r['first_hit_ok'])
summary = {'seed': SEED, 'catalogued_total': len(catalogued), 'sample': tot, 'found_text': tot - len(fails_text), 'found_in_topic': tot - len(fails_pos), 'first_hit_ok': sum(1 for r in rows if r['first_hit_ok']),
           'failures_text': fails_text, 'failures_in_topic': fails_pos, 'non_unique_key_in_topic': [r['name'] for r in rows if not r['unique_in_topic']][:10], 'by_tag': by, 'seconds': round(time.time() - t0, 1),
           'recipe_text_present_in_capsule': 'max_chars 4500' in (W / 'app/packages/haiku_expanded/prefix.md').read_text('utf-8'),
           'kernel_formalization_span_chars': [SPAN[0], SPAN[1]], 'provider_calls': 0, 'network': 'blocked by audit hook'}
json.dump({'summary': summary, 'rows': rows}, open(SCR / 'qc_recovery_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
