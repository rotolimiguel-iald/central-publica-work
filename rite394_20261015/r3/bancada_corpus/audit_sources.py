"""Auditoria estática: lê AST, nunca importa ou executa um.py."""
import ast
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
source = root / 'fontes' / 'um.py'
raw = source.read_bytes()
tree = ast.parse(raw.decode('utf-8-sig'))
embedded = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in node.targets
    ):
        embedded = ast.literal_eval(node.value)
        break
assert isinstance(embedded, dict)
rows = []
for name, text in embedded.items():
    path = root / 'fontes' / 'tgl_kernel' / name
    if not path.exists():
        rows.append({'path': name, 'status': 'NOT_COPIED_OR_ABSENT'})
        continue
    disk = path.read_bytes()
    rows.append({'path': name,
                 'same_text_normalizing_EOL': disk.decode('utf-8-sig').replace('\r\n', '\n') == text.replace('\r\n', '\n'),
                 'sha256_copy': hashlib.sha256(disk).hexdigest()})
report = {
    'um_sha256': hashlib.sha256(raw).hexdigest(),
    'um_bytes': len(raw),
    'um_lines': len(raw.splitlines()),
    'embedded_files': len(embedded),
    'compared': sum('same_text_normalizing_EOL' in r for r in rows),
    'text_differences': [r['path'] for r in rows if r.get('same_text_normalizing_EOL') is False],
    'not_compared': [r['path'] for r in rows if 'same_text_normalizing_EOL' not in r],
    'files': rows,
    'scope': 'Compara fontes; não revalida os objetos .olean preexistentes nem reexecuta o rito.'
}
target = root / 'auditoria_fontes.json'
temporary = target.with_suffix('.json.tmp')
data = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
temporary.write_bytes(data)
assert temporary.stat().st_size == len(data) > 0
temporary.replace(target)
print(json.dumps({k: v for k, v in report.items() if k != 'files'}, ensure_ascii=False, indent=2))
