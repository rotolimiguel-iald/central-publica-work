# -*- coding: utf-8 -*-
"""R2.1: CANDIDATO_MANIFESTO_R2_1.json, DIFF_R2_R2_1.patch e a prova por `git apply` (core.autocrlf=false).

  * hashes LIDOS dos arquivos; o manifesto tem o formato do R2 (o implantar.py o lê); `originais` não mudam
  * o patch é gerado DIRETO dos dois candidatos (sem cópia do web server, que carrega uma chave de produção) e os
    cabeçalhos viram a/… b/… como no DIFF_R1_R2.patch
  * a prova aplica o patch numa cópia de candidato_r2 em 9_R2_1/tmp; o iald_web_server.py entra REDIGIDO dos dois
    lados (a chave fica fora dos trechos do patch: conferido; então a redação não muda o resultado)
Escreve só em 9_R2_1. Nada da chave é impresso."""
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

R21 = Path(__file__).resolve().parents[1]
WORK = R21.parent
INT = WORK / '4_INTEGRACAO'
R2 = INT / 'candidato_r2' / 'C'
NEW = R21 / 'candidato_r2_1' / 'C'
GIT = ['git', '-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false']
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')
MOTIVO = {
    r'C:\IALD\MEMORIA_IALD\lib\iald_memory\guard.py':
        'R2.1 (revisão R2: N1, N2, N3 e lacunas de nome da revisão B): esqueleto do nome (NFKC, caracteres de formato, '
        'homóglifos cirílicos/gregos e travessões) e radicais iald?psion?state / iald?stack?v em qualquer posição; '
        '.env/*.env/*.env.*/*.env_*/.envrc; sufixo ~; remoção de sufixos de backup LINEAR (mesma decisão do laço do R2); '
        'read_checked abre o handle (leitura, sem FILE_SHARE_DELETE) antes de checar contagem de links, identidade e o '
        'caminho FINAL do handle, e lê do mesmo handle',
    r'C:\IALD\MEMORIA_IALD\session_memory.py':
        'R2.1 (N3): read_allowed_file e load_reference leem por guard.read_checked (mesmos códigos de erro)',
    r'C:\IALD\projetos_pyhton\IALD\iald_web_server.py':
        'R2.1 (revisão R2 §3, o 3 != 1): nova tentativa curta e limitada (HEARTBEAT_REPLACE_RETRY_S = 3 s) em '
        'PermissionError nos os.replace/os.remove do heartbeat (psion, health, rotação da telemetria) e remoção do '
        'tempário quando a troca falha. O psion segue opaco: só as trocas foram envolvidas',
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def redact(b):
    return KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), b)


def main():
    m2_path = INT / 'CANDIDATO_MANIFESTO_R2.json'
    m2 = json.loads(m2_path.read_text(encoding='utf-8'))
    m = json.loads(json.dumps(m2))
    m['titulo'] = 'R2.1 — conserto ACOM 12/10 — CANDIDATO R2.1 (revisão independente R2 de 13/10)'
    m['at'] = datetime.now(timezone.utc).isoformat()
    m['r2'] = {'manifesto': str(m2_path), 'sha256': sha(m2_path)}
    mud = []
    for item in m['arquivos']:
        rel = Path(*Path(item['target']).parts[1:])
        s2, s21 = sha(R2 / rel), sha(NEW / rel)
        assert s2 == item['sha256'], ('candidato_r2 divergente do manifesto R2', item['target'])
        item['sha256_r2'] = s2
        item['sha256'] = s21
        item['bytes'] = (NEW / rel).stat().st_size
        if s21 != s2:
            item['role'] = 'r2_1_construtor'
            item['origem'] = str(NEW / rel)
            item['r2_1_motivo'] = MOTIVO[item['target']]
            mud.append({'target': item['target'], 'sha256_r2': s2, 'sha256_r2_1': s21, 'bytes': item['bytes'],
                        'motivo': item['r2_1_motivo']})
    files = sorted(p for p in NEW.rglob('*') if p.is_file())
    assert len(files) == len(m['arquivos']) == 15, ('árvore R2.1 com arquivo fora do manifesto', len(files))
    m['r2_1_mudancas'] = mud
    out_m = R21 / 'CANDIDATO_MANIFESTO_R2_1.json'
    out_m.write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    # ---- patch direto dos candidatos (cwd = WORK; caminhos relativos sem espaço nos 3 arquivos mudados)
    partes = []
    for x in mud:
        rel = Path(*Path(x['target']).parts[1:]).as_posix()
        a = '4_INTEGRACAO/candidato_r2/C/' + rel
        b = '9_R2_1/candidato_r2_1/C/' + rel
        assert ' ' not in rel
        proc = subprocess.run(GIT + ['diff', '--no-index', '--binary', '--no-prefix', a, b], cwd=str(WORK), capture_output=True)
        assert proc.returncode == 1, proc.stderr[-300:]
        txt = proc.stdout
        txt = txt.replace(b'diff --git ' + a.encode() + b' ' + b.encode(), b'diff --git a/' + rel.encode() + b' b/' + rel.encode(), 1)
        txt = txt.replace(b'--- ' + a.encode() + b'\n', b'--- a/' + rel.encode() + b'\n', 1)
        txt = txt.replace(b'+++ ' + b.encode() + b'\n', b'+++ b/' + rel.encode() + b'\n', 1)
        assert a.encode() not in txt and b.encode() not in txt
        partes.append(txt)
    patch = b''.join(partes)
    assert not KEY.search(patch), 'o patch carrega uma chave'
    patch_p = R21 / 'DIFF_R2_R2_1.patch'
    patch_p.write_bytes(patch)

    # ---- prova: git apply sobre uma cópia do candidato_r2 (web server redigido dos dois lados)
    (R21 / 'tmp').mkdir(exist_ok=True)
    checks = []
    with tempfile.TemporaryDirectory(dir=str(R21 / 'tmp')) as td:
        repo = Path(td) / 'repo'
        for p in sorted(R2.rglob('*')):
            if p.is_file():
                d = repo / p.relative_to(R2)
                d.parent.mkdir(parents=True, exist_ok=True)
                d.write_bytes(redact(p.read_bytes()) if p.name == 'iald_web_server.py' else p.read_bytes())
        subprocess.run(GIT + ['init', '-q'], cwd=repo, capture_output=True, check=True)
        ap = subprocess.run(GIT + ['apply', '--whitespace=nowarn', str(patch_p)], cwd=repo, capture_output=True)
        for p in files:
            rel = p.relative_to(NEW)
            esperado = redact(p.read_bytes()) if p.name == 'iald_web_server.py' else p.read_bytes()
            got = (repo / rel).read_bytes() if (repo / rel).exists() else None
            checks.append({'file': rel.as_posix(), 'same': got == esperado,
                           'web_server_redigido_nos_dois_lados': p.name == 'iald_web_server.py'})
        shutil.rmtree(repo / '.git', ignore_errors=True)
    # a redação é transparente: os bytes da chave são idênticos em R2 e R2.1 e ficam fora de todo trecho do patch
    ws_rel = Path('IALD/projetos_pyhton/IALD/iald_web_server.py')
    k2 = [mm.group(0) for mm in KEY.finditer((R2 / ws_rel).read_bytes())]
    k21 = [mm.group(0) for mm in KEY.finditer((NEW / ws_rel).read_bytes())]
    check = {'at': datetime.now(timezone.utc).isoformat(), 'patch': patch_p.name, 'patch_bytes': len(patch),
             'patch_sha256': hashlib.sha256(patch).hexdigest(), 'git_apply_rc': ap.returncode,
             'stderr': ap.stderr.decode('utf-8', 'replace')[-800:], 'files': checks,
             'all_equal': ap.returncode == 0 and all(c['same'] for c in checks),
             'patch_sem_chave': True, 'chave_igual_em_r2_e_r2_1': k2 == k21, 'n_chaves_web_server': len(k21),
             'nota': 'git -c core.autocrlf=false apply sobre a cópia do candidato_r2; iald_web_server.py redigido dos dois '
                     'lados (a chave não está em nenhum trecho do patch e é a mesma nos dois candidatos)'}
    (R21 / 'DIFF_R2_R2_1_APPLY_CHECK.json').write_text(json.dumps(check, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'manifesto_r2_1_sha16': sha(out_m)[:16], 'mudancas': [(Path(x['target']).name, x['sha256_r2_1'][:16]) for x in mud],
                      'patch': (len(patch), check['patch_sha256'][:16], check['all_equal']),
                      'chave_igual': check['chave_igual_em_r2_e_r2_1']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
