"""Revisor sonnet-app-v407-revisor -- diff de TODAS as ferramentas v407 contra as da v406 (bytes) + hunks do haiku_codec.py. Somente leitura."""
import difflib, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
BS = chr(92)
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104'); W6 = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
HERE = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
copia = json.loads((W / 'COPIA_DA_V406.json').read_bytes())
rows = []
for e in copia['arquivos']:
    a6, a7 = W6 / e['arquivo_v406'], W / e['arquivo_v407']
    b6, b7 = a6.read_bytes(), a7.read_bytes()
    rows.append({'file': e['arquivo_v407'], 'v406_file': e['arquivo_v406'], 'v406_file_sha_matches_COPIA': sha(b6) == e['sha256_v406'], 'identical_to_v406': b6 == b7, 'bytes_v406': len(b6), 'bytes_v407': len(b7)})
ident = [r['file'] for r in rows if r['identical_to_v406']]
diff = [r for r in rows if not r['identical_to_v406']]
res = {'listed_in_COPIA': len(rows), 'identical_to_v406': len(ident), 'differ': [r['file'] for r in diff], 'COPIA_hashes_of_v406_files_verified_now': all(r['v406_file_sha_matches_COPIA'] for r in rows), 'hunks': {}}
for r in diff:
    a = (W6 / r['v406_file']).read_text('utf-8').splitlines(); b = (W / r['file']).read_text('utf-8').splitlines()
    s = difflib.SequenceMatcher(None, a, b, autojunk=False)
    hs = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != 'equal':
            hs.append({'op': tag, 'v406': [i1 + 1, i2], 'v407': [j1 + 1, j2], 'removed_first': (a[i1] if i1 < i2 else '')[:150], 'added_first': (b[j1] if j1 < j2 else '')[:150], 'added_lines': j2 - j1, 'removed_lines': i2 - i1})
    res['hunks'][r['file']] = hs
# arquivos .py do release que nao estao na COPIA (escritos pelo construtor nesta release)
listed = {e['arquivo_v407'].replace(BS, '/') for e in copia['arquivos']}
extra = sorted(str(p.relative_to(W)).replace(BS, '/') for p in list(W.glob('*.py')) + list((W / 'app').glob('*.py')) + list((W / 'app/build').glob('*.py')) + list((W / 'review').glob('*.py')) if str(p.relative_to(W)).replace(BS, '/') not in listed)
res['py_files_not_in_COPIA'] = extra
json.dump(res, open(HERE / 'q_tools_diff_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('listed in COPIA:', len(rows), '| identical:', len(ident), '| differ:', len(diff))
print('differ:', res['differ'])
print('COPIA hashes of v406 files verified now:', res['COPIA_hashes_of_v406_files_verified_now'])
for f, hs in res['hunks'].items():
    print('\n' + f + ':')
    for h in hs:
        print('  ', h['op'], 'v406', h['v406'], '-> v407', h['v407'], '| +%d -%d' % (h['added_lines'], h['removed_lines']), '|', (h['added_first'] or h['removed_first'])[:100])
print('\n.py files in release not in COPIA:', extra)
