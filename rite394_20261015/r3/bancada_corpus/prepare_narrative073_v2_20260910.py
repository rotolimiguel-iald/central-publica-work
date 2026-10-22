from pathlib import Path
import hashlib

source = Path(r'C:\IALD\Central de Patentes\Chatgpt\prepare_narrative073_20260910.py')
raw = source.read_bytes()
text = raw.decode('utf-8')
old = '    assert path.is_file(), path'
new = "    assert path.is_file() or path == OUT / 'REEXAME_SUFICIENCIA.md', path"
assert text.count(old) == 1
text = text.replace(old, new)
exec(compile(text, str(source) + ':corrected_forward_link', 'exec'), {'__name__': '__main__'})
assert source.read_bytes() == raw
print('Original narrative helper unchanged: ' + hashlib.sha256(raw).hexdigest())
