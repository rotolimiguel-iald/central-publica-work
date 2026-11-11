"""Verify immutable public source URLs against staged git bytes; GET only."""
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

A = Path(__file__).resolve().parent
sys.path.insert(0, str(A.parent))
import task
import release_cfg
cfg = release_cfg.load(require_commit=True)
assert task.check('sources', actor=cfg.builder)['ready']
binding = json.loads((A/'PUBLIC_GIT_BINDING.json').read_bytes())
assert binding['commit'] == cfg.espelho_commit
rows = []
for relative, expected in binding['sources'].items():
    url = expected['url']
    assert url.startswith('https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+cfg.espelho_commit+'/')
    with urllib.request.urlopen(url, timeout=60) as response:
        assert response.status == 200 and response.url == url
        raw = response.read()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == expected['sha256'] and len(raw) == expected['bytes'], relative
    rows.append(dict(path=relative, url=url, sha256=digest, bytes=len(raw), http=200))
out = dict(status='PUBLIC_RAW_EXACT_BYTES_VERIFIED', commit=cfg.espelho_commit,
           files=rows, source_binding_sha256=hashlib.sha256((A/'PUBLIC_GIT_BINDING.json').read_bytes()).hexdigest(),
           generation_calls=0, production_writes=0)
with (A/'PUBLIC_RAW_VERIFIED.json').open('x', encoding='utf8') as stream:
    json.dump(out, stream, ensure_ascii=False, indent=2)
print(json.dumps(dict(status=out['status'], files=len(rows))))
