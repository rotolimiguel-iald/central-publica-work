import json, os, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
SCR = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD'); W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'): raise RuntimeError('blocked ' + event)
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int): return
        p = Path(os.fsdecode(path)).resolve()
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and not p.is_relative_to(SCR): raise RuntimeError('write outside reviewer folder: ' + str(p))
sys.addaudithook(guard); sys.path.insert(0, str(R))
import iald_core_indexado as ci
M = W / 'app/science/memory_stage/manifest_staged.json'
m = json.loads(M.read_bytes()); txt = Path(m['published_evidence']['result']['path']).read_bytes().decode('utf-8-sig')
name = 'ext_v318_profile026_profile_state_one_kernel_proved'
pat = '"%s": true' % name
occ = [mm.start() for mm in re.finditer(re.escape(pat), txt)]
print('occurrences of the exact flag text in the sealed result:', len(occ), occ[:10])
top = lambda pos: re.findall(r'\n    "([^"\n]+)": \{', txt[:pos])[-1]
for p in occ: print('  pos', p, 'inside topic:', top(p))
# also names that CONTAIN this name as substring (e.g. longer flags)
longer = sorted(set(re.findall(r'"([A-Za-z0-9_σΔ]*%s[A-Za-z0-9_]*)": true' % re.escape(name), txt)))
print('flags containing the name as substring:', longer[:8])
r = ci.execute_tool(M, 'search_tgl', {'query': name, 'limit': 5})
for x in r['results']:
    print(' hit', x['id'], 'offset', x.get('offset'), 'topic?', top(x['offset']) if x['id']=='resultado_publicado_integral' else '-', '| keys:', sorted(x)[:8])
    if x['id'] == 'resultado_publicado_integral':
        f = ci.execute_tool(M, 'fetch_tgl', {'id': x['id'], 'offset': max(0, x['offset'] - 2000), 'max_chars': 4500})
        print('    window has exact text:', pat in f['text'], '| window covers positions:', max(0, x['offset']-2000), '..', max(0, x['offset']-2000)+len(f['text']))
for lim in (10, 20):
    r = ci.execute_tool(M, 'search_tgl', {'query': name, 'limit': lim})
    ok = False
    for x in r['results']:
        if x['id'] != 'resultado_publicado_integral': continue
        f = ci.execute_tool(M, 'fetch_tgl', {'id': x['id'], 'offset': max(0, x['offset'] - 2000), 'max_chars': 4500})
        s = max(0, x['offset']-2000)
        if any(s <= p < s+len(f['text']) for p in occ) and pat in f['text']: ok = True
    print('limit', lim, 'n_results', len(r['results']), 'covers the kernel_formalization occurrence:', ok)
