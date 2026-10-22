# -*- coding: utf-8 -*-
"""R2.2: monta DUAS cópias das suítes a partir da cópia da R2.1 (9_R2_1/copia, chave já redigida):
  copia_r2_1 — os arquivos «candidato» da R2.1 (linha de base: os testes novos devem FALHAR aqui; ferramentas de
               9_R2_2/ref_r2_1, byte a byte as da R2.1)
  copia      — os arquivos «candidato» trocados pelos do candidato_r2_2 (chave do web server REDIGIDA, mesmo tamanho)
Não segue junções; não copia __pycache__ nem os resultados da R2.1 (regerados); tmp/, guard_log/ e evidencias_r2/ vazios.
Os testes novos (src_r2_2) entram em suite/r2_2 (ferramentas, guard N1, manifesto) e suite/app (via do app) nas duas
cópias, e o rodar.py ganha as duas suítes R2.2. Nada fora de 9_R2_2."""
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
WORK = R22.parent
R21 = WORK / '9_R2_1'
BASE_COPIA = R21 / 'copia'
CAND_R21 = R21 / 'candidato_r2_1' / 'C'
CAND_R22 = R22 / 'candidato_r2_2' / 'C'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')
PULAR = {'RESULTADOS_TESTES.json', 'RESULTADOS_TESTES_parcial.json', 'TESTES.md', 'TESTES_parcial.md'}


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
            if rel == Path('.') and f in PULAR or (rel.name == 'testes_r2' and f in PULAR):
                continue
            data = sp.read_bytes()
            if f == 'iald_web_server.py':
                data, n = redact(data)            # já redigido na cópia da R2.1; conferido de novo
                if n:
                    log['redacted_again'].append(str(dst / rel / f))
            (dst / rel / f).write_bytes(data)
            log['files'] += 1


def montar(nome, cand_root):
    out = R22 / nome
    if out.exists() and any(out.iterdir()):
        raise SystemExit('%s já existe; nada feito' % out)
    log = {'files': 0, 'redacted_again': [], 'reparse_skipped': [], 'candidato_trocados': []}
    for d in ('testes_r2', 'guard', 'testes_r2_src'):
        copy_tree(BASE_COPIA / d, out / d, log)
    # os 28 arquivos de papel «candidato» (mapa da montagem da R2.1, lido do disco)
    mapa = json.loads((R21 / 'runs' / 's0_montar_copia_r2_copia.json').read_text(encoding='utf-8'))['copia']['candidato_trocados']
    for item in mapa:
        rel_alvo = item['alvo_rel']
        src_rel = Path(item['origem']).relative_to(CAND_R21)
        src = cand_root / src_rel
        raw = src.read_bytes()
        red, n = redact(raw)
        dst = out / 'testes_r2' / Path(rel_alvo)
        dst.write_bytes(red)
        log['candidato_trocados'].append({'alvo_rel': rel_alvo, 'origem': str(src), 'sha256_origem': sha(raw),
                                          'sha256_na_copia': sha(red), 'chave_redigida': n})
    novos = {'test_r2_2.py': out / 'testes_r2' / 'suite' / 'r2_2' / 'test_r2_2.py',
             'test_app_r2_2.py': out / 'testes_r2' / 'suite' / 'app' / 'test_app_r2_2.py'}
    for n, d in novos.items():
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes((R22 / 'src_r2_2' / n).read_bytes())
    rodar = out / 'testes_r2' / 'rodar.py'
    s = rodar.read_bytes().decode('utf-8')
    linha = "    ('R2.1 heartbeat novos (revisao R2 13/10)', HERE / 'hb' / 'tests', ['test_heartbeat_r2_1'], [], True),\n"
    assert s.count(linha) == 1
    s = s.replace(linha, linha + "    ('R2.2 novos (revisao R2.1 13/10)', SUITE / 'r2_2', ['test_r2_2'], [CORE, str(SUITE / 'sessions')], False),\n"
                  "    ('R2.2 app novos (revisao R2.1 13/10)', SUITE / 'app', ['test_app_r2_2'], [], True),\n")
    antigo = "'# TESTES — R2.1 (conserto ACOM 12/10; copia)'"
    assert s.count(antigo) == 1
    s = s.replace(antigo, "'# TESTES — R2.2 (conserto ACOM 12/10; %s)'" % nome)
    rodar.write_bytes(s.encode('utf-8'))
    for d in ('guard_log', 'evidencias_r2', 'tmp'):
        (out / d).mkdir(exist_ok=True)
    # nenhuma chave de produção na cópia
    vaz = []
    for p in out.rglob('*'):
        if p.is_file() and KEY.search(p.read_bytes() if p.stat().st_size < 50_000_000 else b''):
            for mm in KEY.finditer(p.read_bytes()):
                if not set(mm.group(0)[4:]) <= {ord('R')} and b'FAKE' not in mm.group(0):
                    vaz.append(str(p.relative_to(out)))
                    break
    log['arquivos_com_padrao_de_chave_nao_redigido'] = sorted(set(vaz))
    return log


def main():
    quais = sys.argv[1:] or ['copia_r2_1', 'copia']
    res = {n: montar(n, CAND_R21 if n == 'copia_r2_1' else CAND_R22) for n in quais}
    (R22 / 'runs' / ('s3_montar_%s.json' % '_'.join(quais))).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: {'files': v['files'], 'trocados': len(v['candidato_trocados']),
                          'chave_redigida': sum(x['chave_redigida'] for x in v['candidato_trocados']),
                          'reparse': len(v['reparse_skipped']),
                          'padrao_nao_redigido': v['arquivos_com_padrao_de_chave_nao_redigido']} for k, v in res.items()},
                     ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main())
