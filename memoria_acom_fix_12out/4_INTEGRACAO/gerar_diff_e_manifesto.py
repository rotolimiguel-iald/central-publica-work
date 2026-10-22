# -*- coding: utf-8 -*-
"""Gera DIFF.patch (originais/C -> candidato/C, git diff --no-index sobre BYTES, terminadores preservados) e
MANIFESTO.json de 4_INTEGRACAO (sha256 de cada entregável, lido do arquivo). Prova o patch: aplicá-lo num repositório
descartável sobre uma cópia de originais/ reproduz candidato/ byte a byte (DIFF_APPLY_CHECK.json).
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIG = HERE / 'originais' / 'C'
CAND = HERE / 'candidato' / 'C'
GIT = ['git', '-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false']


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    cand_files = sorted(p for p in CAND.rglob('*') if p.is_file())
    # árvore a/ só com os originais que o candidato toca (os demais originais são apoio das suítes)
    with tempfile.TemporaryDirectory(dir=str(HERE / 'tmp')) as td:
        a = Path(td) / 'a'
        b = Path(td) / 'b'
        for p in cand_files:
            rel = p.relative_to(CAND)
            if (ORIG / rel).exists():
                (a / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ORIG / rel, a / rel)
            (b / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, b / rel)
        # --no-prefix: os caminhos saem como a/IALD/... e b/IALD/...; `git apply` (-p1) sobre uma cópia de a/ resolve IALD/...
        proc = subprocess.run(GIT + ['diff', '--no-index', '--binary', '--no-prefix', 'a', 'b'],
                              cwd=td, capture_output=True)
        patch = proc.stdout
        (HERE / 'DIFF.patch').write_bytes(patch)
        # prova: aplicar sobre cópia de a/ reproduz b/
        repo = Path(td) / 'repo'
        shutil.copytree(a, repo)
        subprocess.run(GIT + ['init', '-q'], cwd=repo, capture_output=True, check=True)
        ap = subprocess.run(GIT + ['apply', '--whitespace=nowarn', str(HERE / 'DIFF.patch')], cwd=repo, capture_output=True)
        same = []
        for p in cand_files:
            rel = p.relative_to(CAND)
            same.append({'file': rel.as_posix(), 'same': (repo / rel).exists() and sha256_file(repo / rel) == sha256_file(p)})
        check = {'at': datetime.now(timezone.utc).isoformat(), 'git_apply_rc': ap.returncode, 'stderr': ap.stderr.decode('utf-8', 'replace')[-1000:],
                 'files': same, 'all_equal': ap.returncode == 0 and all(s['same'] for s in same),
                 'patch_bytes': len(patch), 'patch_sha256': hashlib.sha256(patch).hexdigest(), 'patch_cr': patch.count(b'\r')}
        (HERE / 'DIFF_APPLY_CHECK.json').write_text(json.dumps(check, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    # MANIFESTO
    skip_dirs = {'tmp', 'guard_log', 'raiz'}
    files = []
    for p in sorted(HERE.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(HERE)
        if any(part in skip_dirs for part in rel.parts) or rel.name == 'MANIFESTO.json' or '__pycache__' in rel.parts:
            continue
        if rel.parts[0] == 'testes' and rel.parts[1:2] and rel.parts[1] in ('suite', 'hb', 'nucleo', 'blocos', 'originais') and rel.suffix in ('.json', '.txt') and 'evidencias' not in rel.parts:
            pass
        st = p.stat()
        files.append({'path': rel.as_posix(), 'bytes': st.st_size, 'sha256': sha256_file(p),
                      'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds')})
    cand_manifest = json.loads((HERE / 'CANDIDATO_MANIFESTO.json').read_text(encoding='utf-8'))
    manifest = {'titulo': 'INTEGRAÇÃO — conserto ACOM 12/10 — MANIFESTO', 'gerado_em': datetime.now(timezone.utc).isoformat(),
                'pasta': str(HERE), 'gerado_por': 'gerar_diff_e_manifesto.py (hashes lidos dos arquivos)',
                'producao_nao_tocada': True,
                'entregaveis': {'candidato': [a['target'] for a in cand_manifest['arquivos']],
                                'implantacao': ['implantar.py', 'reverter.py', 'implantacao_lib.py', 'implantar_config_producao.json',
                                                'ferramentas/aplicar_blocos.py', 'ferramentas/SESSION_BRIDGE_v2.md'],
                                'resultado': ['RESULTADO_INTEGRACAO.md', 'CANDIDATO_MANIFESTO.json', 'DIFF.patch', 'DIFF_APPLY_CHECK.json',
                                              'testes/TESTES.md', 'testes/RESULTADOS_TESTES.json', 'ensaio_implantacao/ENSAIO_RECIBO.json',
                                              'evidencias/e2e_n300.json', 'evidencias/migracao_ensaio_3ctx.json', 'evidencias/PRODUCAO_INTOCADA.json']},
                'diff': check, 'n_arquivos': len(files), 'arquivos': files}
    (HERE / 'MANIFESTO.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'patch_bytes': check['patch_bytes'], 'patch_sha16': check['patch_sha256'][:16], 'apply_all_equal': check['all_equal'],
                      'manifesto_arquivos': len(files)}))


if __name__ == '__main__':
    main()
