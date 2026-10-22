"""Compare the candidate against the server's existing validated formal evidence."""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from iald_kernel import KernelCatalog
from iald_estado_publicado import published_evidence
from build_haiku_candidate import ENC, store

manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
cluster = manifest['active_cluster']
catalog = KernelCatalog(cluster['kernel_bundle'], cluster['kernel_verification'])
block, metadata = published_evidence(manifest['published_evidence'], catalog)
candidate = (WORK / 'haiku_candidate.md').read_text(encoding='utf-8')
rows = []
for entry in metadata['fixed_hypothesis_sources']:
    source = catalog._read_checked(entry['path'])
    rows.append({'id': entry['id'], 'path': entry['path'], 'sha256': entry['sha256'],
                 'full_source_in_candidate': source in candidate,
                 'term_names_in_candidate': {term['name']: term['name'] in candidate for term in entry['terms']},
                 'source_o200k_tokens': len(ENC.encode(source, disallowed_special=()))})
result = {'status': 'FORMAL_COVERAGE_AUDIT_NOT_DEPLOYED',
          'candidate_sha256': hashlib.sha256(candidate.encode()).hexdigest(),
          'published_evidence_checked': metadata['published_evidence_checked'],
          'formal_evidence_block_o200k_tokens': len(ENC.encode(block, disallowed_special=())),
          'sources': rows, 'compiler_rerun': False}
store(WORK / 'haiku_formal_evidence.md', block.encode())
store(WORK / 'haiku_formal_coverage.json', (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode())
print(json.dumps(result, ensure_ascii=False))
