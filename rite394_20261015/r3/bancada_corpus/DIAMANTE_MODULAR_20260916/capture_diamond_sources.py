from pathlib import Path
import datetime
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parent
CANON = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
CACHE = ROOT.parent / 'TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k'

def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}

names = ['TGLExt/WedgeNet.lean', 'TGL/SpecificAQFTWitness.lean',
         'TGLExt/V350WedgeModularData.lean',
         'TGLExt/TheSameBetaReadsFourFaces.lean',
         'TGLExt/V350GateContract.lean', 'TGLExt/V350ModularCertificate.lean',
         'TGLExt/FrontierCertificate.lean',
         'TGLExt/TheWideNet.lean', 'TGLExt/FusedWitness.lean',
         'TGLExt/PoincareWitness.lean', 'TGLExt/GeometricWitness.lean',
         'TGLExt/ContinuumShards.lean', 'TGLExt/TailNet.lean',
         'TGLExt/IsotoneNet.lean', 'TGLExt/LocalInteractionData.lean',
         'TGLExt/LocalInteractionDynamics.lean']
sources = [pin(CANON / 'tgl_kernel' / n) for n in names]
cached = pin(CACHE / 'TGLExt/WedgeNet.lean')
assert sources[0]['sha256'] == cached['sha256'], 'Canonical and imported source differ'
hits = []
pattern = re.compile(r'net\s*:=|TGLSpecificAQFTWitness|causalDiamond|doubleCone|diamondNet')
for directory in ['TGL', 'TGLExt']:
    for p in sorted((CANON / 'tgl_kernel' / directory).rglob('*.lean')):
        found = [{'line': i, 'text': line}
                 for i, line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(), 1)
                 if pattern.search(line)]
        if found:
            hits.append({'source': pin(p), 'hits': found})
seal_path = CANON / 'um_absoluto_selo.json'
seal = json.loads(seal_path.read_text(encoding='utf-8-sig'))
data = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'sources': sources, 'canonical_um': pin(CANON / 'um.py'),
    'seal': pin(seal_path),
    'declared_gate': seal.get('qg_closure_verdict'),
    'gate_read_from_existing_seal_not_rerun': True,
    'imported_wedge_source': cached, 'canonical_source_equal_to_imported_source': True,
    'search_scope': ['tgl_kernel/TGL/**/*.lean', 'tgl_kernel/TGLExt/**/*.lean'],
    'search_pattern': pattern.pattern, 'search_results': hits,
    'canonical_code_executed_or_imported': False,
    'canonical_files_modified': False,
    'note': 'Read-only source inspection. Existing dependency objects were reused by Lean; '
            'matching source hashes do not claim a fresh rebuild of the complete canonical kernel.'
}
dest = ROOT / 'CANONICAL_DIAMOND_SOURCE_AUDIT.json'
assert not dest.exists()
raw = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
tmp = dest.with_suffix('.json.tmp')
tmp.write_bytes(raw)
assert tmp.read_bytes() == raw
os.replace(tmp, dest)
assert dest.read_bytes() == raw
print(json.dumps({'sources': len(sources), 'search_files_with_hits': len(hits),
                  'same_wedge_source': True, 'output': str(dest)}, ensure_ascii=False))
