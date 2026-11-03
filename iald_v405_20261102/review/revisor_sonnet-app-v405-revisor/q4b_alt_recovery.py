"""Reviewer Q4b: alternative recovery paths for the names that the plain by-name search did not surface (all_verified; ext_vrd_eInner_kernel_checked at limit 4).
Strict criterion: the fetched window must contain the flag line AT ITS POSITION inside kernel_formalization. Same read-only harness as q4_recovery.py."""
import json, os, re, sys
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

RESULT_TEXT = Path(json.loads(M.read_bytes())['published_evidence']['result']['path']).read_bytes().decode('utf-8-sig')
NL = chr(10)
_a = RESULT_TEXT.index(NL + '    "kernel_formalization": {')
_m = re.compile(r'\r?\n    \},?\r?\n').search(RESULT_TEXT, _a + 10)
KF = (_a, _m.end())


def pos_in_kf(name):
    return RESULT_TEXT.find('"%s": true' % name, KF[0], KF[1])


out = {'kernel_formalization_span': list(KF)}
cases = {
    'all_verified': ['all_verified', 'all_verified true', 'all_verified kernel_formalization', 'all_unconditional_targets_verified all_conditional_implications_verified all_verified',
                     'kernel_formalization all_verified true qgc_concrete_aqft_core_constructed', 'qgc_concrete_aqft_core_constructed all_verified'],
    'ext_vrd_eInner_kernel_checked': ['ext_vrd_eInner_kernel_checked', 'ext_vrd_eInner_kernel_checked true'],
}
for name, queries in cases.items():
    fp = pos_in_kf(name)
    rows = []
    for q in queries:
        found = []
        for limit in (4, 5):
            r = ci.execute_tool(M, 'search_tgl', {'query': q, 'limit': limit})
            hit = None
            for x in r['results']:
                if x['id'] != 'resultado_publicado_integral':
                    continue
                f = ci.execute_tool(M, 'fetch_tgl', {'id': 'resultado_publicado_integral', 'offset': x['offset'], 'max_chars': 4500})
                if ('"%s": true' % name) in f['text'] and x['offset'] <= fp < x['offset'] + len(f['text']):
                    hit = x['offset']
                    break
            found.append({'limit': limit, 'docs': [y['id'] for y in r['results']], 'strict_hit_offset': hit})
        rows.append({'query': q, 'attempts': found})
    out[name] = {'flag_position_in_kernel_formalization': fp, 'queries': rows}
print(json.dumps(out, ensure_ascii=False, indent=1))
