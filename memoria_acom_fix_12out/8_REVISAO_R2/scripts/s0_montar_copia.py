# -*- coding: utf-8 -*-
"""Revisor R2: monta a COPIA das suites (testes_r2 + guard) em 8_REVISAO_R2/copia, sem seguir juncoes,
redigindo qualquer chave embutida (padrao AIza/sk-/gh*_/xox*) por um marcador do mesmo tamanho (o valor nunca
e impresso nem gravado). Confere: cada arquivo 'candidato' da suite == candidato_r2 (sha256, com a mesma redacao)."""
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[2]
INT = WORK / '4_INTEGRACAO'
OUT = WORK / '8_REVISAO_R2' / 'copia'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')


def redact(data):
    n = [0]

    def sub(m):
        n[0] += 1
        v = m.group(0)
        return v[:4] + b'R' * (len(v) - 4)
    return KEY.sub(sub, data), n[0]


def is_reparse(p):
    try:
        st = os.lstat(p)
    except OSError:
        return True
    return bool(getattr(st, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def copy_tree(src, dst, log):
    for root, dirs, files in os.walk(src, followlinks=False):
        dirs[:] = [d for d in dirs if not is_reparse(os.path.join(root, d)) and d != '__pycache__']
        rel = Path(root).relative_to(src)
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            sp = Path(root) / f
            if is_reparse(sp):
                log['reparse_skipped'].append(str(sp))
                continue
            data = sp.read_bytes()
            data2, n = redact(data)
            if n:
                log['redacted'].append({'file': str(dst / rel / f), 'n': n})
            (dst / rel / f).write_bytes(data2)
            log['files'] += 1


def main():
    if OUT.exists() and any(OUT.iterdir()):
        print('copia ja existe; nada feito')
        return 1
    log = {'files': 0, 'redacted': [], 'reparse_skipped': []}
    copy_tree(INT / 'testes_r2', OUT / 'testes_r2', log)
    copy_tree(INT / 'guard', OUT / 'guard', log)
    copy_tree(INT / 'testes_r2_src', OUT / 'testes_r2_src', log)
    man = json.loads((INT / 'testes_r2' / 'SUITE_MANIFEST.json').read_text(encoding='utf-8'))
    checks = []
    base_old = str(INT / 'testes_r2').lower()
    for f in man['files']:
        if f['role'] != 'candidato':
            continue
        tgt = f['target']
        rel = tgt[len(base_old) + 1:] if tgt.lower().startswith(base_old) else None
        mine = OUT / 'testes_r2' / rel if rel else None
        src = Path(f['source'])
        s_red, _ = redact(src.read_bytes())
        m_bytes = mine.read_bytes() if mine and mine.exists() else None
        checks.append({'target_rel': rel, 'igual_ao_candidato_r2': m_bytes == s_red,
                       'sha16_candidato': hashlib.sha256(src.read_bytes()).hexdigest()[:16],
                       'sha16_manifesto': f['sha256'][:16]})
    log['candidato_checks'] = {'n': len(checks), 'iguais': sum(c['igual_ao_candidato_r2'] for c in checks),
                               'diferentes': [c for c in checks if not c['igual_ao_candidato_r2']],
                               'manifesto_eq_candidato': all(c['sha16_candidato'] == c['sha16_manifesto'] for c in checks)}
    (OUT.parent / 'runs' / 's0_montar_copia.json').write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in log.items() if k != 'redacted'} | {'redacted_files': len(log['redacted'])}, ensure_ascii=False)[:3000])
    return 0


if __name__ == '__main__':
    sys.exit(main())
