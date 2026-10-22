"""Build DIFF.patch (originals vs copy, plus tests) and MANIFESTO.json (sha256 of every delivered file).

Everything by script; hashes read from the files on disk. Writes only inside 1_NUCLEO.
Run from anywhere:  C:\\Python314\\python.exe -X utf8 tests\\make_diff_and_manifest.py
"""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

NUCLEO = Path(__file__).resolve().parents[1]
os.chdir(NUCLEO)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def git_diff(a, b):
    proc = subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false', 'diff', '--no-index',
                           '--no-color', '--text', '--src-prefix=a/', '--dst-prefix=b/', a, b],
                          capture_output=True)
    if proc.returncode not in (0, 1):
        raise SystemExit(proc.stderr.decode('utf-8', 'replace'))
    return proc.stdout


EXCLUDE_DIRS = {'__pycache__'}
HEADER = (
    '# DIFF.patch -- FRENTE NUCLEO, conserto ACOM 12/10 (gerado 13/10/2026 por tests/make_diff_and_manifest.py)\n'
    '# a/originais_arvore/ = originais (byte-iguais a C:\\IALD\\MEMORIA_IALD e ao core de 10/10, conferido por cmp);\n'
    '# b/copia/MEMORIA_IALD/ = a arvore v2 desta frente, espelhando C:\\IALD\\MEMORIA_IALD; b/tests/ = os testes.\n'
    '# Arquivos novos aparecem como adicoes integrais. Este e um diff de REVISAO entre duas arvores (prefixos a/ e b/\n'
    '# apontam para pastas diferentes): a instalacao (passo M3, ato da gerencia) e a copia byte a byte de\n'
    '# copia/MEMORIA_IALD/* sobre C:\\IALD\\MEMORIA_IALD/* com .bak_<data> de cada arquivo tocado, nunca git apply.\n\n'
).encode('utf-8')
parts = [
    HEADER,
    git_diff('originais_arvore/MEMORIA_IALD', 'copia/MEMORIA_IALD'),
    git_diff('originais_arvore/tests/test_store.py', 'tests/test_store.py'),
]
# New test and tooling files as whole additions.
for new in ('tests/test_store_v2.py', 'tests/run_tests.py', 'tests/guard_summary.py', 'tests/make_diff_and_manifest.py',
            'tests/store_v1_frozen.sha256'):
    parts.append(git_diff(os.devnull, new).replace(b'a/' + os.devnull.encode(), b'/dev/null').replace(b'a/nul', b'/dev/null'))
patch = b''.join(parts)
Path('DIFF.patch').write_bytes(patch)

entries = []
for root, dirs, files in os.walk(NUCLEO):
    dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
    rel_root = Path(root).relative_to(NUCLEO)
    if rel_root.parts and rel_root.parts[0] == 'tmp':
        continue
    for name in sorted(files):
        p = Path(root) / name
        rel = str(p.relative_to(NUCLEO)).replace('\\', '/')
        if rel == 'MANIFESTO.json':
            continue
        st = p.stat()
        entries.append({'path': rel, 'bytes': st.st_size, 'sha256': sha256(p),
                        'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds')})

by_path = {e['path']: e for e in entries}
summary = {
    'titulo': 'FRENTE NUCLEO -- conserto ACOM 12/10 -- MANIFESTO',
    'gerado_em': datetime.now(timezone.utc).isoformat(timespec='seconds'),
    'pasta': str(NUCLEO),
    'gerado_por': 'tests/make_diff_and_manifest.py (hashes lidos dos arquivos por script; nenhum hash de memoria)',
    'ordem_do_operador': {'arquivo': r'C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt',
                          'sha16_declarado_pela_gerencia': '78ef70e6f9868281'},
    'producao_nao_tocada': True,
    'originais_byte_iguais_a_producao': 'conferido por cmp em 13/10/2026: store.py, __init__.py, CORE.md (C:\\IALD\\MEMORIA_IALD) e test_store.py (core de 10/10)',
    'entregas': {
        'codigo_v2 (arvore espelhando C:\\IALD\\MEMORIA_IALD)': [k for k in by_path if k.startswith('copia/')],
        'testes': [k for k in by_path if k.startswith('tests/')],
        'evidencias': [k for k in by_path if k.startswith('evidencias/')],
        'diff': 'DIFF.patch', 'testes_md': 'TESTES.md',
        'originais_congelados': [k for k in by_path if k.startswith('originais/') or k.startswith('originais_arvore/')],
        'guarda': [k for k in by_path if k.startswith('guard/')],
    },
    'testes_rodada_final': {m: json.loads(Path(f'evidencias/unittest_{m}.json').read_text('utf-8'))
                            for m in ('test_store', 'test_store_v2')},
    'arquivos': entries,
}
for m, s in summary['testes_rodada_final'].items():
    s.pop('results', None)
Path('MANIFESTO.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
print('DIFF.patch', len(patch), 'bytes; MANIFESTO.json entries', len(entries))
print('sha256 DIFF.patch', sha256('DIFF.patch'))
print('sha256 MANIFESTO.json', sha256('MANIFESTO.json'))
for k in ('copia/MEMORIA_IALD/lib/iald_memory/store.py', 'copia/MEMORIA_IALD/lib/iald_memory/journal.py',
          'copia/MEMORIA_IALD/lib/iald_memory/snapshots.py', 'copia/MEMORIA_IALD/lib/iald_memory/migrate.py',
          'copia/MEMORIA_IALD/lib/iald_memory/__init__.py', 'copia/MEMORIA_IALD/migrar_para_delta.py',
          'copia/MEMORIA_IALD/mover_backups_antigos.py', 'copia/MEMORIA_IALD/CORE.md', 'tests/test_store_v2.py',
          'tests/test_store.py', 'TESTES.md', 'evidencias/crescimento_n300.json'):
    print(f"{by_path[k]['sha256'][:16]}  {by_path[k]['bytes']:7d}  {k}")
