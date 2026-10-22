import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
from iald_hipoteses import hypothesis_sources
from iald_kernel import KernelCatalog
from iald_memoria_canonica import count_tokens
manifest = json.loads((WORK / 'iald_nucleo_fixo.json').read_bytes())
prior_audit = json.loads((WORK / 'public_payload_audit.json').read_bytes())
public_hashes = {entry['url']: entry['sha256'] for entry in prior_audit['files']}
bundle = next(line.partition('=')[2].strip() for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines()
              if line.startswith('IALD_KERNEL_BUNDLE='))
catalog = KernelCatalog(bundle)
proof = json.loads(Path(manifest['published_evidence']['proof_manifest']['path']).read_bytes())
block, records = hypothesis_sources(manifest['published_evidence']['hypothesis_sources'], catalog, proof)
assert len(records) == 5
for entry in records: assert public_hashes[entry['url']] == entry['sha256']
old = (WORK / 'public_evaluation_material.txt').read_bytes()
assert hashlib.sha256(old).hexdigest() == prior_audit['payload_sha256']
excerpt = old.decode().split('EXTRATO DOS CAMPOS NOMEADOS, SEM ALTERAÇÃO DE VALORES:\n', 1)[1]
payload = (block + '\nJSON PÚBLICO — MODOS E ESCOPO CORRENTES:\n' + excerpt).encode()
audit = {**prior_audit, 'scope': 'PUBLIC_SOURCES_AND_DERIVED_HYPOTHESIS_GUIDE_ONLY',
         'runtime_prefix_included': False, 'tokens': count_tokens(payload.decode()),
         'payload_sha256': hashlib.sha256(payload).hexdigest()}
with (WORK / 'public_guide_material.txt').open('xb') as handle: handle.write(payload)
with (WORK / 'public_guide_audit.json').open('x', encoding='utf-8') as handle: json.dump(audit, handle, indent=2)
code = (WORK / 'probe_response_public.py').read_text(encoding='utf-8')
code = code.replace('public_payload_audit.json', 'public_guide_audit.json').replace('public_evaluation_material.txt', 'public_guide_material.txt')
code = code.replace("'PUBLIC_GITHUB_FILES_ONLY'", "'PUBLIC_SOURCES_AND_DERIVED_HYPOTHESIS_GUIDE_ONLY'")
code = code.replace("sys.dont_write_bytecode=True", "sys.dont_write_bytecode=True\nsys.stdout.reconfigure(encoding='utf-8')", 1)
code = code.replace("public_response_", "public_guide_response_")
with (WORK / 'probe_response_guide.py').open('x', encoding='utf-8') as handle: handle.write(code)
print(json.dumps({'sources': len(records), 'tokens': audit['tokens'], 'private_atlas_included': False,
                  'scope': audit['scope']}))
