"""Revisor sonnet-app-v407-revisor -- Q4 (R3-2 e recuperacao dos nomes de bandeira catalogados). ADAPTADO de qc_recovery.py do revisor da v406.
Exercita a receita ENSINADA pela capsula do haiku55, sem provedor e sem rede, com o runtime importado SO PARA LEITURA (gancho de auditoria recusa socket, subprocess,
os.system e qualquer escrita fora da pasta do revisor):
  search_tgl(query=<nome exato>, limit=5); para cada resultado de resultado_publicado_integral: fetch_tgl(id=resultado_publicado_integral, offset=max(0, offset-2000), max_chars=4500)
Sucesso: a janela devolvida contem '"<nome>": true'; metrica mais forte: a janela cobre a posicao da bandeira DENTRO do topico kernel_formalization.
REGRA FIXADA ANTES DE MEDIR (partitura): nome com caractere nao-ASCII e' guardado escapado (\\uXXXX) no selado; para esses a agulha e' a forma escapada e conta a consulta literal OU a escapada.
Semente do revisor 407407407 (nem a do construtor, 20261104, nem a do revisor da v406, 40640406); catalogo recomputado do selado v407 com a regra da capsula, independente do haiku_codec."""
import json, os, random, re, sys, time
from pathlib import Path

sys.dont_write_bytecode = True
SEED = 407407407
N_RANDOM = 520
R = Path(r'C:\IALD\projetos_pyhton\IALD')
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
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
        if p.name in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json') or p.name.startswith('.env'):
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
# v406 sealed (installed) para achar os nomes NOVOS da v407
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes())
kf6 = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes().decode('utf-8-sig'))['core']['kernel_formalization']
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
WHOLE = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I)
KEEP = re.compile(r'H[123]|discharg|condition|verif', re.I)
catalogued = [k for k, v in kf.items() if v is True and re.match(r'(?:ext|red)_', k) and not (WHOLE.search(k) or ESS.search(k) or KEEP.search(k))]
NL = chr(10)
a = RESULT_TEXT.index(NL + '    "kernel_formalization": {')
mm = re.compile(r'\r?\n    \},?\r?\n').search(RESULT_TEXT, a + 10)
SPAN = (a, mm.end())


def esc(name):
    return json.dumps(name)[1:-1]   # ensure_ascii escaping, como no arquivo selado


def flag_pos(name):
    pat = '"%s": true' % esc(name)
    first = RESULT_TEXT.find(pat, SPAN[0], SPAN[1])
    second = RESULT_TEXT.find(pat, first + 1, SPAN[1]) if first >= 0 else -1
    return first, second


rng = random.Random(SEED)
sample = [(k, 'random') for k in rng.sample(catalogued, N_RANDOM)]
seen = {k for k, _ in sample}
extra = []
extra += [(k, 'shortest') for k in sorted(catalogued, key=len)[:25]]
extra += [(k, 'longest') for k in sorted(catalogued, key=len, reverse=True)[:25]]
srt = sorted(catalogued)
prefix_of_other = [srt[i] for i in range(len(srt) - 1) if srt[i + 1].startswith(srt[i])]
extra += [(k, 'proper_prefix_of_another') for k in prefix_of_other[:30]]
new407 = [k for k in catalogued if kf6.get(k) is not True]
extra += [(k, 'new_in_v407') for k in rng.sample(new407, min(40, len(new407)))]
for k, tag in extra:
    if k not in seen:
        sample.append((k, tag)); seen.add(k)
t0 = time.time()
rows = []
for name, tag in sample:
    fp, fp2 = flag_pos(name)
    needle = '"%s": true' % esc(name)
    row = {'name': name, 'tag': tag, 'len': len(name), 'ascii': name.isascii(), 'pos': fp, 'unique_in_topic': bool(fp >= 0 and fp2 < 0)}
    queries = [name] if name.isascii() else [name, esc(name)]
    ok_text = ok_pos = first_hit_ok = False
    used_query = None
    n_hits_total = 0
    for qi, q in enumerate(queries):
        r = ci.execute_tool(M, 'search_tgl', {'query': q, 'limit': 5})
        hits = [x for x in r['results'] if x['id'] == 'resultado_publicado_integral']
        n_hits_total += len(hits)
        for i, x in enumerate(hits):
            f = ci.execute_tool(M, 'fetch_tgl', {'id': x['id'], 'offset': max(0, x['offset'] - 2000), 'max_chars': 4500})
            t = needle in f['text']
            p = bool(fp >= 0 and max(0, x['offset'] - 2000) <= fp < max(0, x['offset'] - 2000) + len(f['text']))
            if i == 0 and qi == 0:
                first_hit_ok = bool(t and p)
            ok_text = ok_text or t
            ok_pos = ok_pos or (t and p)
            if ok_text and ok_pos:
                used_query = 'literal' if qi == 0 else 'escaped'
                break
        if ok_text and ok_pos:
            break
    row.update(found_text=ok_text, found_in_topic=ok_pos, first_hit_ok=first_hit_ok, used_query=used_query, n_hits=n_hits_total)
    rows.append(row)
tot = len(rows)
fails_text = [r['name'] for r in rows if not r['found_text']]
fails_pos = [r['name'] for r in rows if not r['found_in_topic']]
by = {}
for r in rows:
    d = by.setdefault(r['tag'], {'n': 0, 'found_text': 0, 'found_in_topic': 0, 'first_hit_ok': 0})
    d['n'] += 1; d['found_text'] += int(r['found_text']); d['found_in_topic'] += int(r['found_in_topic']); d['first_hit_ok'] += int(r['first_hit_ok'])
nonascii = [r for r in rows if not r['ascii']]
cap55 = (W / 'app/packages/haiku_expanded/prefix.md').read_text('utf-8')
summary = {'seed': SEED, 'catalogued_total': len(catalogued), 'sample': tot, 'n_random': N_RANDOM, 'found_text': tot - len(fails_text), 'found_in_topic': tot - len(fails_pos), 'first_hit_ok': sum(1 for r in rows if r['first_hit_ok']),
           'failures_text': fails_text, 'failures_in_topic': fails_pos, 'non_unique_key_in_topic': [r['name'] for r in rows if not r['unique_in_topic']][:10],
           'non_ascii_in_sample': {'n': len(nonascii), 'names': [r['name'] for r in nonascii], 'recovered_by': {r['name']: r['used_query'] for r in nonascii}},
           'by_tag': by, 'seconds': round(time.time() - t0, 1),
           'new_in_v407_total': len(new407), 'recipe_text_present_in_capsule': 'max_chars 4500' in cap55 and 'limit 5' in cap55,
           'kernel_formalization_span_chars': [SPAN[0], SPAN[1]], 'provider_calls': 0, 'network': 'blocked by audit hook', 'writes_outside_reviewer_folder': 'blocked by audit hook'}
json.dump({'summary': summary, 'rows': rows}, open(SCR / 'q4_recovery_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
