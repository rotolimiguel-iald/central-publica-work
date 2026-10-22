# -*- coding: utf-8 -*-
"""R2.2: CANDIDATO_MANIFESTO_R2_2.json, DIFF_R2_1_R2_2.patch e a prova por `git apply` (core.autocrlf=false).

  * hashes LIDOS dos arquivos; o manifesto tem o formato do R2/R2.1 (o implantar.py lê `arquivos` e `originais`;
    `originais` não mudam: são a produção congelada)
  * campo `ferramentas` (documental, revisão R2.1 §1): sha256 LIDO de cada ferramenta em 4_INTEGRACAO/ferramentas;
    o valor citado até a R2.1 fica ao lado (`sha256_citado_ate_r2_1`)
  * `ferramentas_implantacao`: sha256 de implantar.py, reverter.py e implantacao_lib.py da R2.2
  * o patch cobre os 3 arquivos mudados do candidato (a/IALD/...) e as 3 ferramentas (a/ferramentas/...); é gerado
    DIRETO dos arquivos (o web server com a chave nunca é copiado para fora da pasta do candidato); a chave não está
    em nenhum trecho do patch (conferido); a prova aplica o patch numa cópia em 9_R2_2/tmp com o web server REDIGIDO
    dos dois lados
Escreve só em 9_R2_2. Nada da chave é impresso."""
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
WORK = R22.parent
R21 = WORK / '9_R2_1'
OLD = R21 / 'candidato_r2_1' / 'C'
NEW = R22 / 'candidato_r2_2' / 'C'
FERR = WORK / '4_INTEGRACAO' / 'ferramentas'
GIT = ['git', '-c', 'core.autocrlf=false', '-c', 'core.safecrlf=false']
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')
TOOLS = ['implantar.py', 'reverter.py', 'implantacao_lib.py']
MOTIVO = {
    'guard.py': 'R2.2 (revisão R2.1, N1 por componentes): path_shape_reason (comprimento > 32.767 ou mais de 256 '
                'componentes, contados em tempo linear) ANTES do os.path.realpath em path_reason e read_checked; recusa '
                'visível path_too_long / path_too_many_components',
    'session_memory.py': 'R2.2 (documental, revisão R2.1 §1): comentário do _guarded_read corrigido (o handle é de leitura, '
                         'sem FILE_SHARE_DELETE; não «attributes only») e a nota do teto de forma (N1)',
    'iald_web_server.py': 'R2.2 (revisão R2.1, N1 e N3 pela via do app): agi_validate_path recusa a forma do caminho '
                          'ANTES do realpath e confere o arquivo pelo HANDLE do guard (read_checked: contagem de links, '
                          'identidade e caminho FINAL do mesmo handle, também dentro da whitelist, sem o prefixo '
                          'estendido); /admin/api/agi/files/read e a ação read do agi_execute leem os bytes do '
                          'read_checked, nunca de um segundo open por nome',
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def redact(b):
    return KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), b)


def diff(a, b, novo_nome):
    proc = subprocess.run(GIT + ['diff', '--no-index', '--binary', '--no-prefix', a, b], cwd=str(WORK), capture_output=True)
    assert proc.returncode == 1, proc.stderr[-300:]
    txt = proc.stdout
    txt = txt.replace(b'diff --git ' + a.encode() + b' ' + b.encode(),
                      b'diff --git a/' + novo_nome.encode() + b' b/' + novo_nome.encode(), 1)
    txt = txt.replace(b'--- ' + a.encode() + b'\n', b'--- a/' + novo_nome.encode() + b'\n', 1)
    txt = txt.replace(b'+++ ' + b.encode() + b'\n', b'+++ b/' + novo_nome.encode() + b'\n', 1)
    assert a.encode() not in txt and b.encode() not in txt
    return txt


def main():
    m1_path = R21 / 'CANDIDATO_MANIFESTO_R2_1.json'
    m1 = json.loads(m1_path.read_text(encoding='utf-8'))
    m = json.loads(json.dumps(m1))
    m['titulo'] = 'R2.2 — conserto ACOM 12/10 — CANDIDATO R2.2 (revisão independente R2.1 de 13/10)'
    m['at'] = datetime.now(timezone.utc).isoformat()
    m['r2_1'] = {'manifesto': str(m1_path), 'sha256': sha(m1_path)}
    mud = []
    for item in m['arquivos']:
        rel = Path(*Path(item['target']).parts[1:])
        s1, s2 = sha(OLD / rel), sha(NEW / rel)
        assert s1 == item['sha256'], ('candidato_r2_1 divergente do manifesto R2.1', item['target'])
        item['sha256_r2_1'] = s1
        item['sha256'] = s2
        item['bytes'] = (NEW / rel).stat().st_size
        if s2 != s1:
            item['role'] = 'r2_2_construtor'
            item['origem'] = str(NEW / rel)
            item['r2_2_motivo'] = MOTIVO[rel.name]
            mud.append({'target': item['target'], 'sha256_r2_1': s1, 'sha256_r2_2': s2, 'bytes': item['bytes'],
                        'motivo': item['r2_2_motivo']})
    files = sorted(p for p in NEW.rglob('*') if p.is_file())
    assert len(files) == len(m['arquivos']) == 15, ('árvore R2.2 com arquivo fora do manifesto', len(files))
    m['r2_2_mudancas'] = mud
    ferr = []
    for f in m['ferramentas']:
        real = sha(f['arquivo'])
        novo = dict(f, sha256=real)
        if real != f['sha256']:
            novo['sha256_citado_ate_r2_1'] = f['sha256']
            novo['correcao_r2_2'] = ('o manifesto citava o sha256 do aplicar_blocos.py do R1; o arquivo em '
                                     '4_INTEGRACAO/ferramentas (o que a config usa) é este, lido por script')
        ferr.append(novo)
    m['ferramentas'] = ferr
    m['ferramentas_implantacao'] = [{'arquivo': str(R22 / t), 'sha256': sha(R22 / t), 'sha256_r2_1': sha(R21 / t)}
                                    for t in TOOLS]
    out_m = R22 / 'CANDIDATO_MANIFESTO_R2_2.json'
    out_m.write_text(json.dumps(m, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    # ---- patch (cwd = WORK; caminhos relativos sem espaço)
    partes = []
    for x in mud:
        rel = Path(*Path(x['target']).parts[1:]).as_posix()
        assert ' ' not in rel
        partes.append(diff('9_R2_1/candidato_r2_1/C/' + rel, '9_R2_2/candidato_r2_2/C/' + rel, rel))
    for t in TOOLS:
        partes.append(diff('9_R2_1/' + t, '9_R2_2/' + t, 'ferramentas/' + t))
    patch = b''.join(partes)
    assert not KEY.search(patch), 'o patch carrega uma chave'
    patch_p = R22 / 'DIFF_R2_1_R2_2.patch'
    patch_p.write_bytes(patch)

    # ---- prova: git apply sobre uma cópia do candidato_r2_1 + ferramentas R2.1 (web server redigido dos dois lados)
    (R22 / 'tmp').mkdir(exist_ok=True)
    checks = []
    with tempfile.TemporaryDirectory(dir=str(R22 / 'tmp')) as td:
        repo = Path(td) / 'repo'
        for p in sorted(OLD.rglob('*')):
            if p.is_file():
                d = repo / p.relative_to(OLD)
                d.parent.mkdir(parents=True, exist_ok=True)
                d.write_bytes(redact(p.read_bytes()) if p.name == 'iald_web_server.py' else p.read_bytes())
        for t in TOOLS:
            d = repo / 'ferramentas' / t
            d.parent.mkdir(parents=True, exist_ok=True)
            d.write_bytes((R21 / t).read_bytes())
        subprocess.run(GIT + ['init', '-q'], cwd=repo, capture_output=True, check=True)
        ap = subprocess.run(GIT + ['apply', '--whitespace=nowarn', str(patch_p)], cwd=repo, capture_output=True)
        for p in files:
            rel = p.relative_to(NEW)
            esperado = redact(p.read_bytes()) if p.name == 'iald_web_server.py' else p.read_bytes()
            got = (repo / rel).read_bytes() if (repo / rel).exists() else None
            checks.append({'file': rel.as_posix(), 'same': got == esperado,
                           'web_server_redigido_nos_dois_lados': p.name == 'iald_web_server.py'})
        for t in TOOLS:
            got = (repo / 'ferramentas' / t).read_bytes()
            checks.append({'file': 'ferramentas/' + t, 'same': got == (R22 / t).read_bytes()})
        shutil.rmtree(repo / '.git', ignore_errors=True)
    ws_rel = Path('IALD/projetos_pyhton/IALD/iald_web_server.py')
    k1 = [mm.group(0) for mm in KEY.finditer((OLD / ws_rel).read_bytes())]
    k2 = [mm.group(0) for mm in KEY.finditer((NEW / ws_rel).read_bytes())]
    check = {'at': datetime.now(timezone.utc).isoformat(), 'patch': patch_p.name, 'patch_bytes': len(patch),
             'patch_sha256': hashlib.sha256(patch).hexdigest(), 'git_apply_rc': ap.returncode,
             'stderr': ap.stderr.decode('utf-8', 'replace')[-800:], 'files': checks,
             'all_equal': ap.returncode == 0 and all(c['same'] for c in checks),
             'patch_sem_chave': True, 'chave_igual_em_r2_1_e_r2_2': k1 == k2, 'n_chaves_web_server': len(k2),
             'nota': 'git -c core.autocrlf=false apply sobre a cópia do candidato_r2_1 e das ferramentas R2.1; '
                     'iald_web_server.py redigido dos dois lados (a chave não está em nenhum trecho do patch e é a '
                     'mesma nos dois candidatos)'}
    (R22 / 'DIFF_R2_1_R2_2_APPLY_CHECK.json').write_text(json.dumps(check, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'manifesto_r2_2_sha16': sha(out_m)[:16], 'mudancas': [(Path(x['target']).name, x['sha256_r2_2'][:16]) for x in mud],
                      'ferramentas': [(Path(f['arquivo']).name, f['sha256'][:16], f.get('sha256_citado_ate_r2_1', '')[:16]) for f in ferr],
                      'patch': (len(patch), check['patch_sha256'][:16], check['all_equal']),
                      'chave_igual': check['chave_igual_em_r2_1_e_r2_2']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
