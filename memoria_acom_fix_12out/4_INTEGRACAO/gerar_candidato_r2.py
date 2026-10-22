# -*- coding: utf-8 -*-
"""R2 (13/10/2026): manifesto do candidato_r2 e os dois patches, com hashes LIDOS dos arquivos.

  CANDIDATO_MANIFESTO_R2.json   mesmo formato do R1 (o implantar.py o lê); cada arquivo traz sha256 do R2 e do R1
  DIFF_R2.patch                 originais/C -> candidato_r2/C (o que a produção recebe), prova por `git apply`
  DIFF_R1_R2.patch              candidato/C -> candidato_r2/C (só o que a R2 mudou), prova por `git apply`
  DIFF_R2_APPLY_CHECK.json      as duas provas
Escreve só em 4_INTEGRACAO. Não lê produção (os originais já estão congelados em originais/).
"""
from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIG = HERE / 'originais' / 'C'
R1 = HERE / 'candidato' / 'C'
R2 = HERE / 'candidato_r2' / 'C'
GIT = ['git', '-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false']

MOTIVO = {
    r'C:\IALD\MEMORIA_IALD\lib\iald_memory\guard.py':
        'achado 2 (ReDoS): _ESCRITORIO_PATH e key_pem_name trocados por varreduras lineares; mesma decisão nas formas '
        'do R1 + caminho relativo ao drive (c:escritorio) e separadores %5c/%2f',
    r'C:\IALD\MEMORIA_IALD\session_memory.py':
        'achado 4: write_reference e reference passam pelo guard ANTES de exists/read/create; só as chaves do protocolo; '
        'nada do arquivo é devolvido se houver chave estranha',
    r'C:\IALD\MEMORIA_IALD\lib\iald_memory\journal.py':
        'revisão B (t3/E, não listado como bloqueante): nome do diário único também em NTFS (maiúsculas escapadas); '
        'antes, CtxCase e ctxcase dividiam um diário e os dois falhavam no verify',
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def patch_and_check(base_root, new_root, files, patch_path, td):
    a, b = Path(td) / 'a', Path(td) / 'b'
    for p in files:
        rel = p.relative_to(new_root)
        if (base_root / rel).exists():
            (a / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(base_root / rel, a / rel)
        (b / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, b / rel)
    proc = subprocess.run(GIT + ['diff', '--no-index', '--binary', '--no-prefix', 'a', 'b'], cwd=td, capture_output=True)
    patch_path.write_bytes(proc.stdout)
    repo = Path(td) / 'repo'
    shutil.copytree(a, repo)
    subprocess.run(GIT + ['init', '-q'], cwd=repo, capture_output=True, check=True)
    ap = subprocess.run(GIT + ['apply', '--whitespace=nowarn', str(patch_path)], cwd=repo, capture_output=True)
    same = [{'file': p.relative_to(new_root).as_posix(),
             'same': (repo / p.relative_to(new_root)).exists() and sha256_file(repo / p.relative_to(new_root)) == sha256_file(p)}
            for p in files]
    return {'patch': patch_path.name, 'git_apply_rc': ap.returncode, 'stderr': ap.stderr.decode('utf-8', 'replace')[-800:],
            'files': same, 'all_equal': ap.returncode == 0 and all(s['same'] for s in same),
            'patch_bytes': patch_path.stat().st_size, 'patch_sha256': sha256_file(patch_path)}


def main():
    m1 = json.loads((HERE / 'CANDIDATO_MANIFESTO.json').read_text(encoding='utf-8'))
    m2 = json.loads(json.dumps(m1))
    m2['titulo'] = 'INTEGRAÇÃO — conserto ACOM 12/10 — CANDIDATO R2 (achados bloqueantes da revisão de 13/10)'
    m2['at'] = datetime.now(timezone.utc).isoformat()
    m2['r1'] = {'manifesto': 'CANDIDATO_MANIFESTO.json', 'sha256': sha256_file(HERE / 'CANDIDATO_MANIFESTO.json')}
    mudancas = []
    for item in m2['arquivos']:
        rel = Path(*Path(item['target']).parts[1:])
        p2, p1 = R2 / rel, R1 / rel
        s1, s2 = sha256_file(p1), sha256_file(p2)
        assert s1 == item['sha256'], ('R1 divergente do manifesto R1', item['target'])
        item['sha256_r1'] = s1
        item['sha256'] = s2
        item['bytes'] = p2.stat().st_size
        if s2 != s1:
            item['role'] = 'r2_integrador'
            item['origem'] = str(p2)
            item['r2_motivo'] = MOTIVO.get(item['target'], '?')
            mudancas.append({'target': item['target'], 'sha256_r1': s1, 'sha256_r2': s2, 'bytes': item['bytes'],
                             'motivo': item['r2_motivo']})
    files = sorted(p for p in R2.rglob('*') if p.is_file())
    assert len(files) == len(m2['arquivos']), 'árvore R2 com arquivo fora do manifesto'
    m2['r2_mudancas'] = mudancas
    out_manifest = HERE / 'CANDIDATO_MANIFESTO_R2.json'
    out_manifest.write_text(json.dumps(m2, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    (HERE / 'tmp').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=str(HERE / 'tmp')) as td1, tempfile.TemporaryDirectory(dir=str(HERE / 'tmp')) as td2:
        c_full = patch_and_check(ORIG, R2, files, HERE / 'DIFF_R2.patch', td1)
        changed = [R2 / Path(*Path(x['target']).parts[1:]) for x in mudancas]
        c_delta = patch_and_check(R1, R2, changed, HERE / 'DIFF_R1_R2.patch', td2)
    check = {'at': datetime.now(timezone.utc).isoformat(), 'originais_para_r2': c_full, 'r1_para_r2': c_delta}
    (HERE / 'DIFF_R2_APPLY_CHECK.json').write_text(json.dumps(check, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'manifesto_r2_sha16': sha256_file(out_manifest)[:16], 'mudancas': [(Path(x['target']).name, x['sha256_r2'][:16]) for x in mudancas],
                      'diff_r2': (c_full['patch_bytes'], c_full['patch_sha256'][:16], c_full['all_equal']),
                      'diff_r1_r2': (c_delta['patch_bytes'], c_delta['patch_sha256'][:16], c_delta['all_equal'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
