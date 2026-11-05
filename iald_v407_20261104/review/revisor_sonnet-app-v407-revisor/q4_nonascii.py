r"""Revisor sonnet-app-v407-revisor -- Q4 extra: TODOS os nomes catalogados com caractere nao-ASCII (guardados escapados \uXXXX no selado). Regra fixada na partitura: conta a consulta literal OU a escapada. Somente leitura; guarda de auditoria."""
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
m = json.loads(M.read_bytes()); txt = Path(m['published_evidence']['result']['path']).read_bytes().decode('utf-8-sig'); kf = json.loads(txt)['core']['kernel_formalization']
ESS = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
WHOLE = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I); KEEP = re.compile(r'H[123]|discharg|condition|verif', re.I)
cat = [k for k, v in kf.items() if v is True and re.match(r'(?:ext|red)_', k) and not (WHOLE.search(k) or ESS.search(k) or KEEP.search(k))]
na = [k for k in cat if not k.isascii()]
res = {'catalogued': len(cat), 'non_ascii_names': len(na), 'names': na, 'raw_file_form_escaped_present': {}, 'literal_query': {}, 'escaped_query': {}, 'recovered_by_either': {}}
for k in na:
    esc = json.dumps(k)[1:-1]
    needle = '"%s": true' % esc
    res['raw_file_form_escaped_present'][k] = needle in txt
    for label, q in (('literal_query', k), ('escaped_query', esc)):
        ok = False
        for x in ci.execute_tool(M, 'search_tgl', {'query': q, 'limit': 5})['results']:
            if x['id'] != 'resultado_publicado_integral': continue
            f = ci.execute_tool(M, 'fetch_tgl', {'id': x['id'], 'offset': max(0, x['offset'] - 2000), 'max_chars': 4500})
            if needle in f['text']: ok = True; break
        res[label][k] = ok
    res['recovered_by_either'][k] = res['literal_query'][k] or res['escaped_query'][k]
res['all_recovered_by_either'] = all(res['recovered_by_either'].values())
json.dump(res, open(SCR / 'q4_nonascii_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'names'}, ensure_ascii=False, indent=1)); print(res['names'])
