# -*- coding: utf-8 -*-
"""Revisor R2: espelha os scripts ORIGINAIS dos revisores A e B (byte a byte) apontando para o candidato R2.
rev_a/exp/{common,e7_guard_perf,e7b_guard_realistic}.py + rev_a/int/candidato/C/IALD/MEMORIA_IALD (candidato_r2)
rev_b/testes/{t1_paths,t3_session_content}.py      + rev_b/copia/MEMORIA_IALD (lib + session_memory do candidato_r2)
Confere sha256 de cada copia contra a origem e grava runs/s2_montar_revisores.json."""
import hashlib
import json
import shutil
from pathlib import Path

WORK = Path(__file__).resolve().parents[2]
REV = WORK / '8_REVISAO_R2'
CAND_MEM = WORK / '4_INTEGRACAO' / 'candidato_r2' / 'C' / 'IALD' / 'MEMORIA_IALD'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def cp(src, dst, log):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    log.append({'src': str(src), 'dst': str(dst), 'sha256': sha(src), 'igual': sha(src) == sha(dst)})


def main():
    log = []
    for n in ('common.py', 'e7_guard_perf.py', 'e7b_guard_realistic.py'):
        cp(WORK / '5_REVISAO_A' / 'exp' / n, REV / 'rev_a' / 'exp' / n, log)
    for n in ('t1_paths.py', 't3_session_content.py'):
        cp(WORK / '5_REVISAO_B' / 'testes' / n, REV / 'rev_b' / 'testes' / n, log)
    lib = CAND_MEM / 'lib' / 'iald_memory'
    for f in sorted(lib.glob('*.py')):
        cp(f, REV / 'rev_a' / 'int' / 'candidato' / 'C' / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / f.name, log)
        cp(f, REV / 'rev_b' / 'copia' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / f.name, log)
    cp(CAND_MEM / 'session_memory.py', REV / 'rev_b' / 'copia' / 'MEMORIA_IALD' / 'session_memory.py', log)
    (REV / 'runs').mkdir(exist_ok=True)
    (REV / 'runs' / 's2_montar_revisores.json').write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding='utf-8')
    print(len(log), 'copias, todas iguais:', all(x['igual'] for x in log))


if __name__ == '__main__':
    main()
