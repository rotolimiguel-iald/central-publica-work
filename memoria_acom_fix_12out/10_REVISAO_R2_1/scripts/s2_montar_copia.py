# -*- coding: utf-8 -*-
"""Revisor c1 R2.1, passo 2: monta a MINHA copia da suite (independente da copia do construtor).

Base: 8_REVISAO_R2/copia (a do revisor anterior, chave ja redigida). Troca os arquivos de papel «candidato»
pelos do candidato_r2_1 (web server redigido, mesmo tamanho), acrescenta os testes novos de 9_R2_1/src_r2_1 e
as duas linhas do rodar.py, e copia as 3 ferramentas R2.1 para a pasta-mae da copia (o test_r2_1 importa de
COPIA.parent). Confere: cada candidato na copia == candidato_r2_1 redigido; e compara com a copia do construtor.
Nao segue juncoes. Escreve so em 10_REVISAO_R2_1/suite_r21.
"""
import hashlib
import json
import os
import re
import shutil
import stat
import sys
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
WORK = ME.parent
R21 = WORK / '9_R2_1'
REVCOPIA = WORK / '8_REVISAO_R2' / 'copia'
INT = WORK / '4_INTEGRACAO'
CAND_R2 = INT / 'candidato_r2' / 'C'
CAND_R21 = R21 / 'candidato_r2_1' / 'C'
BASE = ME / 'suite_r21'
OUT = BASE / 'copia'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')


def redact(b):
    return KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), b)


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
                log['reparse'].append(os.path.join(root, d))
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
                log['reparse'].append(str(sp))
                continue
            if f.startswith('RESULTADOS_TESTES') or f.startswith('TESTES') and f.endswith('.md'):
                continue
            data = sp.read_bytes()
            if f == 'iald_web_server.py':
                data = redact(data)
            (dst / rel / f).write_bytes(data)
            log['files'] += 1


def main():
    if OUT.exists():
        raise SystemExit('ja existe: ' + str(OUT))
    log = {'files': 0, 'reparse': [], 'candidatos': []}
    for d in ('testes_r2', 'guard', 'testes_r2_src'):
        copy_tree(REVCOPIA / d, OUT / d, log)
    man = json.loads((INT / 'testes_r2' / 'SUITE_MANIFEST.json').read_text(encoding='utf-8'))
    base_old = str(INT / 'testes_r2').lower()
    for f in man['files']:
        if f['role'] != 'candidato':
            continue
        rel = f['target'][len(base_old) + 1:]
        src = CAND_R21 / Path(f['source']).relative_to(CAND_R2)
        raw = src.read_bytes()
        dst = OUT / 'testes_r2' / rel
        dst.write_bytes(redact(raw))
        log['candidatos'].append({'alvo_rel': rel, 'sha_origem': sha(raw)[:16], 'sha_copia': sha(dst.read_bytes())[:16],
                                  'igual_origem_redigida': dst.read_bytes() == redact(raw),
                                  'redigido': raw != redact(raw)})
    for t in sorted((R21 / 'src_r2_1').glob('*.py')):
        d = OUT / 'testes_r2' / 'suite' / 'r2_1' / t.name
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(t.read_bytes())
    for t in sorted((R21 / 'src_r2_1' / 'hb').glob('*.py')):
        (OUT / 'testes_r2' / 'hb' / 'tests' / t.name).write_bytes(t.read_bytes())
    rodar = OUT / 'testes_r2' / 'rodar.py'
    s = rodar.read_bytes().decode('utf-8')
    linha = "    ('R2 novos (achados bloqueantes 13/10)', SUITE / 'r2', ['test_r2'], [CORE, str(SUITE / 'sessions')], False),\n"
    assert s.count(linha) == 1
    s = s.replace(linha, linha + "    ('R2.1 novos (revisao R2 13/10)', SUITE / 'r2_1', ['test_r2_1'], [CORE, str(SUITE / 'sessions')], False),\n"
                  "    ('R2.1 heartbeat novos (revisao R2 13/10)', HERE / 'hb' / 'tests', ['test_heartbeat_r2_1'], [], True),\n")
    rodar.write_bytes(s.encode('utf-8'))
    (OUT / 'guard_log').mkdir(exist_ok=True)
    (OUT / 'evidencias_r2').mkdir(exist_ok=True)
    (OUT / 'tmp').mkdir(exist_ok=True)
    for n in ('implantar.py', 'reverter.py', 'implantacao_lib.py'):
        shutil.copyfile(R21 / n, BASE / n)
        log.setdefault('ferramentas', {})[n] = sha((BASE / n).read_bytes())[:16]
    # comparacao com a copia do construtor (arquivos .py/.md/.json de testes_r2, exceto resultados)
    cmp = {'iguais': 0, 'diferentes': [], 'so_minha': [], 'so_construtor': []}
    theirs = R21 / 'copia' / 'testes_r2'
    mine = OUT / 'testes_r2'
    def lista(root):
        r = set()
        for dp, dn, fn in os.walk(root, followlinks=False):
            dn[:] = [d for d in dn if d not in ('__pycache__', 'tmp') and not is_reparse(os.path.join(dp, d))]
            for f in fn:
                if f.startswith('RESULTADOS_TESTES') or (f.startswith('TESTES') and f.endswith('.md')):
                    continue
                r.add(Path(dp, f).relative_to(root).as_posix())
        return r
    a, b = lista(mine), lista(theirs)
    for rel in sorted(a & b):
        if (mine / rel).read_bytes() == (theirs / rel).read_bytes():
            cmp['iguais'] += 1
        else:
            cmp['diferentes'].append(rel)
    cmp['so_minha'] = sorted(a - b)
    cmp['so_construtor'] = sorted(b - a)
    log['comparacao_com_copia_do_construtor'] = cmp
    log['todos_candidatos_iguais'] = all(c['igual_origem_redigida'] for c in log['candidatos'])
    log['n_candidatos'] = len(log['candidatos'])
    (ME / 'runs' / 's2_montar_copia.json').write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: v for k, v in log.items() if k != 'candidatos'}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    sys.exit(main())
