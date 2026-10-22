from pathlib import Path
import hashlib, json, os, datetime

ROOT = Path(__file__).resolve().parent
source = Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py')
raw = source.read_bytes()
lines = raw.decode('utf-8').splitlines()
ranges = [(10106, 10155), (10156, 10218), (10219, 10249)]
out = ROOT / 'primary'
out.mkdir(exist_ok=True)

def create(path, payload):
    assert path.is_relative_to(ROOT) and not path.exists() and payload
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_bytes(payload)
    assert tmp.read_bytes() == payload
    os.replace(tmp, path)

text = '# Artigo A — excertos primários lidos\n\n'
text += 'Leitura de texto, sem executar/importar o programa. Não é auditoria da derivação variacional.\n\n'
for first, last in ranges:
    text += f'## Linhas {first}–{last}\n\n```text\n'
    text += '\n'.join(f'{i}: {lines[i-1]}' for i in range(first, last+1)) + '\n```\n\n'
excerpt = out / 'ARTIGO_A_EXCERTOS.md'
create(excerpt, text.encode('utf-8'))
record = dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    source=dict(path=str(source), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()),
    ranges=ranges, whole_file_read_as_text=False, source_unchanged=source.read_bytes()==raw,
    excerpt=dict(path=str(excerpt), bytes=excerpt.stat().st_size,
        sha256=hashlib.sha256(excerpt.read_bytes()).hexdigest()),
    scope='READ_PRIMARY_TEXT_ONLY; EOM and coefficient locations confirmed; variational derivation not verified')
assert record['source_unchanged']
create(out / 'PROVENIENCIA_ARTIGO_A.json', json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(record, ensure_ascii=False))
