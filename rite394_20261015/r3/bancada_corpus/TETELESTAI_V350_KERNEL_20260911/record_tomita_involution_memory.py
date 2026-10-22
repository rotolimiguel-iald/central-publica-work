"""Append an explicitly unintegrated DEV result to all inherited memory surfaces."""
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER = 'TETELESTAI_V350_TOMITA_INVOLUTION_DEV_20260912'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert raw and not path.exists()
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw

parent_path = ROOT / 'tomita_polar_custody.json'
parent = json.loads(parent_path.read_bytes())
draft_path = ROOT / 'tomita_involution_draft_status.json'
draft = json.loads(draft_path.read_bytes())
assert draft['polar_involution_proved'] and not draft['integrated']
assert draft['parent_custody_sha256'] == sha(parent_path)
assert sha(ROOT / 'um.py') == parent['working_sha256'] == draft['integrated_working_sha256']
for name, row in draft['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
surfaces = [Path(p) for p in parent['surface_sha256']]
before = {}
for path in surfaces:
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert sha(path) == parent['surface_sha256'][str(path)]
    before[str(path)] = path.read_bytes()
    assert MARKER.encode() not in before[str(path)]
report = ROOT / 'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md'
assert sha(report) == draft['report_sha256']
note = f'''

## {MARKER} — {DATE}

[REAL — DEV compilado, revisão independente e integração pendentes] No mesmo H_I,
o fator antiunitário U de S=UB satisfaz U²=I. A prova usa SR=(I−R)S em D(S),
UR=(I−R)U, a conjugação das raízes positivas sem supor U=U⁻¹, e S²=I sobre
a imagem densa de √R. Quatro módulos/19 alvos, somente o trio lógico permitido.
A documentação anterior em que a involução era aberta é preservada como história.

Este é DEV posterior aos nove módulos/41 alvos integrados. A cópia permanece
com 841 embutidos, 139 registros incrementais e 80 controles; não contém os 19
novos alvos. Nenhum gate foi promovido. A identificação com álgebra/peso e
domínio máximo, KMS, traço/canto, H1/H2/H3 físicos, interação quântica e runtime
continuam abertos. Objetivo integral ativo; originais preservados.

[Prova, hipóteses, falhas corrigidas e limites](<{report.as_posix()}>).
[Manifesto DEV](<{draft_path.as_posix()}>).
'''
backups = {}
for path in surfaces:
    raw = before[str(path)]
    assert path.read_bytes() == raw
    backup = path.with_name(path.name + '.bak_' + STAMP)
    create(backup, raw)
    backups[str(path)] = str(backup)
    newline = '\r\n' if b'\r\n' in raw else '\n'
    updated = raw + note.replace('\n', newline).encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as stream:
        stream.write(updated)
    assert temporary.read_bytes() == updated and path.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes().startswith(backup.read_bytes())
    assert path.stat().st_size > backup.stat().st_size
record = {'timestamp': DATE, 'status': 'DEV_MEMORY_APPEND__NO_INTEGRATION',
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'working_sha256': sha(ROOT / 'um.py'), 'draft_path': str(draft_path),
    'draft_sha256': sha(draft_path), 'report_path': str(report), 'report_sha256': sha(report),
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': backups,
    'surface_before_sha256': {str(p): sha(Path(backups[str(p)])) for p in surfaces},
    'remaining_flags': parent['remaining_flags'], 'integrated': False,
    'gate_changed': False, 'full_goal_complete': False}
out = ROOT / 'tomita_involution_dev_memory_custody.json'
create(out, json.dumps(record, ensure_ascii=False, indent=2).encode())
for path in surfaces:
    assert sha(path) == record['surface_sha256'][str(path)]
    assert Path(backups[str(path)]).read_bytes() == before[str(path)]
assert sha(ROOT / 'um.py') == parent['working_sha256']
print(json.dumps({'custody_sha256': sha(out), 'memory_surfaces': len(surfaces),
    'byte_backups_and_prefixes_verified': len(surfaces), 'integrated': False, 'gate_changed': False}))
