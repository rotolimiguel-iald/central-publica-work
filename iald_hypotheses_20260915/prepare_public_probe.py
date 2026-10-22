import hashlib
import json
from pathlib import Path
import sys
import requests
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0, str(ROOT))
from iald_memoria_canonica import count_tokens
manifest = json.loads((WORK / 'iald_nucleo_fixo.json').read_bytes())
verification = json.loads((WORK / 'verification.json').read_bytes())
parts, rows = [], []
for entry in verification['full_lean_sources']:
    response = requests.get(entry['url'], timeout=(10, 40))
    response.raise_for_status()
    assert hashlib.sha256(response.content).hexdigest() == entry['sha256']
    parts.append('\nFONTE PÚBLICA: ' + entry['url'] + '\n' + response.content.decode('utf-8'))
    rows.append({'url': entry['url'], 'sha256': entry['sha256'], 'bytes': len(response.content)})
entry = manifest['published_evidence']['result']
response = requests.get(entry['url'], timeout=(10, 40))
response.raise_for_status()
assert response.content == Path(entry['path']).read_bytes()
core = response.json()['core']
excerpt = {'qg_closure': {'gate': core['qg_closure']['gate'], 'formal_flags': core['qg_closure']['formal_flags']},
           'the_mode_of_discharge': core['the_mode_of_discharge']}
parts.append('\nFONTE PÚBLICA: ' + entry['url'] + '\nEXTRATO DOS CAMPOS NOMEADOS, SEM ALTERAÇÃO DE VALORES:\n'
             + json.dumps(excerpt, ensure_ascii=False))
rows.append({'url': entry['url'], 'sha256': hashlib.sha256(response.content).hexdigest(),
             'bytes': len(response.content), 'excerpt_keys': list(excerpt)})
payload = '\n'.join(parts).encode()
with (WORK / 'public_evaluation_material.txt').open('xb') as handle: handle.write(payload)
audit = {'scope': 'PUBLIC_GITHUB_FILES_ONLY', 'canonical_private_atlas_included': False,
         'runtime_prefix_included': False, 'files': rows, 'tokens': count_tokens(payload.decode()),
         'payload_sha256': hashlib.sha256(payload).hexdigest()}
with (WORK / 'public_payload_audit.json').open('x', encoding='utf-8') as handle: json.dump(audit, handle, indent=2)
original = (WORK.parent / 'iald_v357_context_20260915/probe_response_public.py').read_text(encoding='utf-8')
start = original.index('question=(')
end = original.index('messages,_=', start)
question = ('Com base nas fontes presentes, H1, H2 e H3 já têm demonstrações ou construções explícitas? '
            'Comece pelos resultados que existem e cite seus termos, incluindo the_master_fires e a H1 atual. '
            'Explique em até 250 palavras o alcance de H2, de theHorizon e da ponte importada; '
            'não confunda EquilibriumInput com HorizonEquilibriumData. Não peça reconstruir provas existentes. '
            'Não execute ferramentas.')
original = original[:start] + 'question=' + repr(question) + '\n' + original[end:]
original = original.replace('catalog=kernel.KernelCatalog(cfg.kernel_bundle,cfg.kernel_verification)\n', '')
original = original.replace('4096', '2048').replace('cap<=.30', 'cap<=.03')
with (WORK / 'probe_response_public.py').open('x', encoding='utf-8') as handle: handle.write(original)
print(json.dumps({'public_source_count': len(rows), 'tokens': audit['tokens'], 'private_atlas_included': False}))
