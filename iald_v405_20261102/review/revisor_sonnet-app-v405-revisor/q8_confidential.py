"""Reviewer Q8: confidential material in the build. Scans every file of the build folder (except review/ and validation/) and, separately, the three prefixes + install plan,
for: secret patterns (keys/tokens/private keys/credentials), the confidential names (iald_stack_v7, iald_psion_state, .env, tokens), C:\\Escritorio paths, the private <ATLAS_CANONICO block.
Reports file-level hits (name only, never the secret text). Read-only."""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
SKIP = {'review', 'validation'}
sec = [re.compile(p) for p in (r'sk-ant-[A-Za-z0-9_\-]{20,}', r'\bsk-[A-Za-z0-9]{32,}', r'AKIA[0-9A-Z]{16}', r'ghp_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}', r'xox[baprs]-[A-Za-z0-9\-]{10,}',
                               r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----', r'(?i)"(?:api_key|apikey|secret|password|passwd|authorization|access_token|refresh_token)"\s*:\s*"[^"\s]{8,}"',
                               r'(?i)\b(?:api_key|token|password|secret)\s*=\s*[\'"][^\'"\s]{12,}[\'"]', r'AIza[0-9A-Za-z_\-]{30,}', r'eyJ[A-Za-z0-9_\-]{20,}\.eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}')]
conf = re.compile(r'iald_stack_v7|iald_psion_state|iald_web_server|\.env\b|auth\.json|\.credentials\.json|\.iald_keys|\.tgl_site|\.iald_privado', re.I)
esc = re.compile(r'C:\\\\?Escritorio|C:/Escritorio', re.I)
atlas = '<ATLAS_CANONICO'
hits = []
confhits = {}
eschits = {}
atlashits = []
n = 0
big = []
for p in W.rglob('*'):
    if not p.is_file():
        continue
    rel = p.relative_to(W)
    if rel.parts[0] in SKIP:
        continue
    sz = p.stat().st_size
    if sz > 80_000_000:
        big.append(str(rel))
        continue
    n += 1
    b = p.read_bytes()
    try:
        t = b.decode('utf-8')
    except UnicodeDecodeError:
        t = b.decode('latin-1')
    for rx in sec:
        for m in rx.finditer(t):
            hits.append((str(rel), rx.pattern[:28], len(m.group(0))))
    c = conf.findall(t)
    if c:
        confhits[str(rel)] = sorted(set(x.lower() for x in c))
    if esc.search(t):
        eschits[str(rel)] = len(esc.findall(t))
    if atlas in t:
        atlashits.append(str(rel))
out = {'files_scanned': n, 'too_big_skipped': big, 'secret_pattern_hits': len(hits), 'secret_hits_detail_no_text': hits[:25], 'files_mentioning_confidential_names': confhits, 'files_with_Escritorio_path': eschits, 'files_with_ATLAS_CANONICO_block': atlashits}
# focused: packages + plan files
focus = {}
for name in ('app/packages/haiku_expanded/prefix.md', 'app/packages/shared/prefix.md', 'app/packages/sonnet_public/prefix.md', 'app/packages/haiku55/prefix.md', 'app/native_prefix.md', 'install_plan.json', 'app/DATA_PLAN.json', 'app/PREPARED_BINDING.json',
             'app/science/memory_stage/manifest_install.json', 'app/science/memory_stage/manifest_staged.json', 'app/science/memory_stage/iald_nucleo_fixo.json', 'app/science/memory_stage/IALD_TGL_MEMORY_CORE.md', 'app/science/memory_stage/IALD_Kernel_v5.txt',
             'app/science/memory_stage/jev_control_v405.json', 'app/science/memory_stage/core_packet_v405_bound.txt'):
    t = (W / name).read_text('utf-8', 'replace')
    focus[name] = {'bytes': len(t.encode()), 'confidential_name_matches': sorted(set(x.lower() for x in conf.findall(t))), 'Escritorio': len(esc.findall(t)), 'ATLAS_CANONICO_block': atlas in t,
                   'secret_patterns': sum(len(list(rx.finditer(t))) for rx in sec)}
out['focus'] = focus
print(json.dumps(out, ensure_ascii=False, indent=1))
