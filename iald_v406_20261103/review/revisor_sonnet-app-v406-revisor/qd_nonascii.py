r"""QD: nomes catalogados com caracteres nao-ASCII (o arquivo selado os guarda escapados: \uXXXX). Mede quantos sao e se a consulta com a forma escapada recupera. Somente leitura; guarda de auditoria."""
import json, os, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(r'C:\IALD\projetos_pyhton\IALD'); W = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103'); SCR = Path(__file__).resolve().parent
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
res = {'catalogued': len(cat), 'non_ascii_names': len(na), 'sample_non_ascii': na[:6], 'raw_file_form_escaped_present': {}, 'exact_recipe_with_literal_unicode': {}, 'exact_recipe_with_escaped_form': {}}
for k in na[:8]:
    esc = json.dumps(k)[1:-1]
    res['raw_file_form_escaped_present'][k] = ('"%s": true' % esc) in txt
    for label, q, needle in (('exact_recipe_with_literal_unicode', k, '"%s": true' % esc), ('exact_recipe_with_escaped_form', esc, '"%s": true' % esc)):
        ok = False
        for x in ci.execute_tool(M, 'search_tgl', {'query': q, 'limit': 5})['results']:
            if x['id'] != 'resultado_publicado_integral': continue
            f = ci.execute_tool(M, 'fetch_tgl', {'id': x['id'], 'offset': max(0, x['offset'] - 2000), 'max_chars': 4500})
            if needle in f['text']: ok = True; break
        res[label][k] = ok
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open(SCR / 'qd_nonascii_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
