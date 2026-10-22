"""Copy existing omitted inputs; do not touch the active runtime or originals."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import shutil

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um')
DEST = ROOT / 'runtime_inputs_pending'
items = [
    (SOURCE / 'Nós/STOKES_A_Prova_do_Contorno.md', Path('STOKES_A_Prova_do_Contorno.md')),
    *[(SOURCE / 'TGL_CODE_ONE_REAL_FALSIFIER/release_clean/data/voids/desivast' / name,
       Path('cache/voids/desivast') / name) for name in (
        'DESIVAST_BGS_VOLLIM_V2_REVOLVER_NGC.fits',
        'DESIVAST_BGS_VOLLIM_V2_REVOLVER_SGC.fits')],
]

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

records = []
for source, relative in items:
    target = DEST / relative
    assert target.resolve().is_relative_to(ROOT.resolve())
    source_hash = digest(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert digest(target) == source_hash, str(target)
    else:
        temporary = target.with_name(target.name + '.copying')
        assert not temporary.exists()
        shutil.copyfile(source, temporary)
        assert temporary.stat().st_size == source.stat().st_size
        assert digest(temporary) == source_hash
        os.replace(temporary, target)
    assert digest(source) == digest(target) == source_hash
    records.append(dict(source=str(source), destination=str(target),
                        relative_to_runtime=relative.as_posix(),
                        bytes=target.stat().st_size, sha256=source_hash))

result = dict(timestamp=datetime.now().astimezone().isoformat(),
              active_runtime_untouched=True, original_files_readonly=True,
              status='EXISTING_INPUTS_STAGED_NOT_APPLIED', files=records)
output = DEST / 'manifest.json'
assert not output.exists()
raw = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
temporary = output.with_suffix('.tmp')
with temporary.open('xb') as stream:
    stream.write(raw)
assert temporary.read_bytes() == raw
os.replace(temporary, output)
print(json.dumps(result, ensure_ascii=False))
