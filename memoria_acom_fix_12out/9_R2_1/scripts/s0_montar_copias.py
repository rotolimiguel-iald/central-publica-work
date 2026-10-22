# -*- coding: utf-8 -*-
"""R2.1: monta DUAS cópias das suítes a partir da cópia do revisor (8_REVISAO_R2/copia, chave já redigida):
  copia_r2   — os arquivos «candidato» do R2 (linha de base: os testes novos devem FALHAR aqui)
  copia      — os arquivos «candidato» trocados pelos do candidato_r2_1 (chave do web server redigida, mesmo tamanho)
Não segue junções; não copia __pycache__ nem tmp/ (recriado vazio). Os testes novos (src_r2_1/*.py) entram em
suite/r2_1 nas duas cópias, e o rodar.py da cópia ganha a suíte «R2.1 novos». Nada fora de 9_R2_1."""
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

R21 = Path(__file__).resolve().parents[1]
WORK = R21.parent
REVCOPIA = WORK / '8_REVISAO_R2' / 'copia'
INT = WORK / '4_INTEGRACAO'
CAND_R2 = INT / 'candidato_r2' / 'C'
CAND_R21 = R21 / 'candidato_r2_1' / 'C'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')


def redact(data):
    n = [0]

    def sub(m):
        n[0] += 1
        return m.group(0)[:4] + b'R' * (len(m.group(0)) - 4)
    return KEY.sub(sub, data), n[0]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def is_reparse(p):
    try:
        return bool(os.lstat(p).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except OSError:
        return True


def copy_tree(src, dst, log):
    for root, dirs, files in os.walk(src, followlinks=False):
        rel = Path(root).relative_to(src)
        keep = []
        for d in dirs:
            if is_reparse(os.path.join(root, d)):
                log['reparse_skipped'].append(os.path.join(root, d))
            elif d == '__pycache__':
                continue
            elif d == 'tmp':
                (dst / rel / d).mkdir(parents=True, exist_ok=True)
            else:
                keep.append(d)
        dirs[:] = keep
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            sp = Path(root) / f
            if is_reparse(sp):
                log['reparse_skipped'].append(str(sp))
                continue
            # só o web server carrega chave real; os testes trazem fichas SINTÉTICAS de propósito (não redigir)
            data, n = redact(sp.read_bytes()) if f == 'iald_web_server.py' else (sp.read_bytes(), 0)
            if n:
                log['redacted'].append(str(dst / rel / f))
            (dst / rel / f).write_bytes(data)
            log['files'] += 1


def montar(nome, cand_root):
    out = R21 / nome
    if out.exists() and any(out.iterdir()):
        raise SystemExit('%s já existe; nada feito' % out)
    log = {'files': 0, 'redacted': [], 'reparse_skipped': [], 'candidato_trocados': []}
    for d in ('testes_r2', 'guard', 'testes_r2_src'):
        copy_tree(REVCOPIA / d, out / d, log)
    man = json.loads((INT / 'testes_r2' / 'SUITE_MANIFEST.json').read_text(encoding='utf-8'))
    base_old = str(INT / 'testes_r2').lower()
    for f in man['files']:
        if f['role'] != 'candidato':
            continue
        rel = f['target'][len(base_old) + 1:]
        src_rel = Path(f['source']).relative_to(CAND_R2)
        src = cand_root / src_rel
        raw = src.read_bytes()
        red, n = redact(raw)
        dst = out / 'testes_r2' / rel
        dst.write_bytes(red)
        log['candidato_trocados'].append({'alvo_rel': rel, 'origem': str(src), 'sha256_origem': sha(raw),
                                          'sha256_na_copia': sha(red), 'chave_redigida': n})
    for t in sorted((R21 / 'src_r2_1').glob('*.py')):
        d = out / 'testes_r2' / 'suite' / 'r2_1' / t.name
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(t.read_bytes())
    for t in sorted((R21 / 'src_r2_1' / 'hb').glob('*.py')):
        (out / 'testes_r2' / 'hb' / 'tests' / t.name).write_bytes(t.read_bytes())
    rodar = out / 'testes_r2' / 'rodar.py'
    s = rodar.read_bytes().decode('utf-8')
    linha = "    ('R2 novos (achados bloqueantes 13/10)', SUITE / 'r2', ['test_r2'], [CORE, str(SUITE / 'sessions')], False),\n"
    assert s.count(linha) == 1
    s = s.replace(linha, linha + "    ('R2.1 novos (revisao R2 13/10)', SUITE / 'r2_1', ['test_r2_1'], [CORE, str(SUITE / 'sessions')], False),\n"
                  "    ('R2.1 heartbeat novos (revisao R2 13/10)', HERE / 'hb' / 'tests', ['test_heartbeat_r2_1'], [], True),\n")
    s = s.replace("'# TESTES — INTEGRAÇÃO R2 (conserto ACOM 12/10; candidato_r2)'",
                  "'# TESTES — R2.1 (conserto ACOM 12/10; %s)'" % nome)
    rodar.write_bytes(s.encode('utf-8'))
    (out / 'guard_log').mkdir(exist_ok=True)
    (out / 'evidencias_r2').mkdir(exist_ok=True)
    return log


def main():
    quais = sys.argv[1:] or ['copia_r2', 'copia']
    res = {n: montar(n, CAND_R2 if n == 'copia_r2' else CAND_R21) for n in quais}
    (R21 / 'runs' / ('s0_montar_%s.json' % '_'.join(quais))).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: {'files': v['files'], 'trocados': len(v['candidato_trocados']), 'redigidos': len(v['redacted']),
                          'reparse': len(v['reparse_skipped'])} for k, v in res.items()}))


if __name__ == '__main__':
    sys.exit(main())
