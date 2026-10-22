# -*- coding: utf-8 -*-
"""R2: re-roda os testes dos REVISORES que falharam (A: E6, E7, E7b; B: t3), com os scripts deles COPIADOS byte a byte
(sha256 conferido contra o original em 5_REVISAO_A/B) e o código sob teste trocado pelo candidato_r2. Estrutura espelho:
  A/exp/{common.py, e7_guard_perf.py, e7b_guard_realistic.py}   (verbatim)  -> A/exp/runs/*.json
  A/int/candidato/C/...                                          (= candidato_r2, bytes)
  A/int/ensaio_implantacao/e6_parcial.py                         (verbatim) + rodar_ensaio.py (adaptador: R2)
  B/testes/t3_session_content.py                                 (verbatim) -> B/testes/t3_result.json
  B/copia/MEMORIA_IALD/{session_memory.py, lib/iald_memory/*}    (= candidato_r2, bytes)
Escreve só em 4_INTEGRACAO/revisores_r2. Não lê confidenciais.
"""
import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
INT = HERE.parent
WORK = INT.parent
REV_A, REV_B = WORK / '5_REVISAO_A', WORK / '5_REVISAO_B'
R2 = INT / 'candidato_r2' / 'C'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def put(src, dst, log):
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = Path(src).read_bytes()
    dst.write_bytes(data)
    assert sha(dst) == hashlib.sha256(data).hexdigest()
    log.append({'src': str(src), 'dst': str(dst.relative_to(HERE)), 'sha256': sha(dst)})


def main():
    for d in ('A', 'B'):
        if (HERE / d).exists():
            shutil.rmtree(HERE / d)
    log = []
    for name in ('common.py', 'e7_guard_perf.py', 'e7b_guard_realistic.py'):
        put(REV_A / 'exp' / name, HERE / 'A' / 'exp' / name, log)
    put(REV_A / 'int' / 'ensaio_implantacao' / 'e6_parcial.py', HERE / 'A' / 'int' / 'ensaio_implantacao' / 'e6_parcial.py', log)
    for p in sorted(R2.rglob('*')):
        if p.is_file():
            put(p, HERE / 'A' / 'int' / 'candidato' / 'C' / p.relative_to(R2), log)
    put(REV_B / 'testes' / 't3_session_content.py', HERE / 'B' / 'testes' / 't3_session_content.py', log)
    mem = R2 / 'IALD' / 'MEMORIA_IALD'
    put(mem / 'session_memory.py', HERE / 'B' / 'copia' / 'MEMORIA_IALD' / 'session_memory.py', log)
    for p in sorted((mem / 'lib' / 'iald_memory').glob('*.py')):
        put(p, HERE / 'B' / 'copia' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / p.name, log)
    shim = '''# -*- coding: utf-8 -*-
"""ADAPTADOR (R2): o e6_parcial.py da revisão A importa `rodar_ensaio` da pasta dele. Aqui ele recebe a montagem do ensaio
R1 (mesmas funções) apontando para o candidato_r2, o CANDIDATO_MANIFESTO_R2.json e os implantar.py/reverter.py R2."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
INT = Path(%r)
sys.path.insert(0, str(INT / 'ensaio_implantacao'))
import importlib.util
_spec = importlib.util.spec_from_file_location('rodar_ensaio_r1', INT / 'ensaio_implantacao' / 'rodar_ensaio.py')
_E = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_E)
_E.RAIZ = HERE / 'raiz'
_E.CAND = INT / 'candidato_r2' / 'C'
globals().update({k: v for k, v in vars(_E).items() if not k.startswith('__') and k not in ('HERE', 'INT', 'config')})


def config():
    sys.path.insert(0, str(INT / 'ensaio_implantacao_r2'))
    import rodar_ensaio_r2 as R2
    R2.E.RAIZ = RAIZ
    R2.HERE = HERE
    return R2.config(None, 'ensaio_config_e6.json')
''' % str(INT)
    (HERE / 'A' / 'int' / 'ensaio_implantacao' / 'rodar_ensaio.py').write_text(shim, encoding='utf-8')
    (HERE / 'MONTAGEM.json').write_text(json.dumps(log, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(log), 'arquivos')


if __name__ == '__main__':
    main()
