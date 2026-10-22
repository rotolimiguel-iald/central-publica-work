# -*- coding: utf-8 -*-
"""R2.2, passo 0: confere por script a base R2.1 e a revisão (sha256 lidos do disco) e copia, BYTE A BYTE,
  candidato_r2_1/C            -> candidato_r2_2/C   (o web server com a chave fica DENTRO da pasta do candidato)
  implantar/reverter/lib R2.1 -> 9_R2_2/            (as ferramentas que a R2.2 edita)
  implantar/reverter/lib R2.1 -> 9_R2_2/ref_r2_1/   (linha de base intocada para os testes «antes»)
Não segue junções (pula pontos de reanálise). Nada fora de 9_R2_2 é escrito. A chave nunca é impressa.
"""
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
WORK = R22.parent
R21 = WORK / '9_R2_1'
REV = WORK / '10_REVISAO_R2_1'

ESPERADO = {
    R21 / 'RESULTADO_R2_1.md': 'f0f4637f39e131c8',
    R21 / 'CANDIDATO_MANIFESTO_R2_1.json': 'f7ccb802d2388ac3',
    R21 / 'implantar.py': 'b913952cb2592b84',
    R21 / 'reverter.py': 'b6e3906baa88a7e5',
    R21 / 'implantacao_lib.py': 'c72ddd0a5686a4e0',
    R21 / 'implantar_config_producao_r2_1.json': '66f8caea867e91e1',
    REV / 'REVISAO_R2_1.md': '8d113857fd263bb0',
}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def is_reparse(p):
    try:
        return bool(os.lstat(p).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    except OSError:
        return True


def copiar_arvore(src, dst, log):
    for root, dirs, files in os.walk(src, followlinks=False):
        rel = Path(root).relative_to(src)
        keep = []
        for d in dirs:
            if is_reparse(os.path.join(root, d)):
                log['reparse_pulados'].append(os.path.join(root, d))
            elif d != '__pycache__':
                keep.append(d)
        dirs[:] = keep
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for f in files:
            sp = Path(root) / f
            if is_reparse(sp):
                log['reparse_pulados'].append(str(sp))
                continue
            dp = dst / rel / f
            dp.write_bytes(sp.read_bytes())
            assert sha(dp) == sha(sp), dp
            log['arquivos'] += 1


def main():
    out = {'base': {}, 'copias': {}}
    for p, esp in ESPERADO.items():
        real = sha(p)[:16]
        out['base'][str(p)] = {'sha16': real, 'esperado': esp, 'confere': real == esp}
    if not all(v['confere'] for v in out['base'].values()):
        print(json.dumps(out, ensure_ascii=False, indent=1))
        raise SystemExit('base divergente: nada copiado')
    man = json.loads((R21 / 'CANDIDATO_MANIFESTO_R2_1.json').read_text(encoding='utf-8'))
    cand21 = R21 / 'candidato_r2_1' / 'C'
    # o candidato R2.1 em disco confere com o seu manifesto (15/15)
    conf = []
    for a in man['arquivos']:
        src = cand21 / Path(*Path(a['target']).parts[1:])
        conf.append(sha(src) == a['sha256'])
    out['candidato_r2_1_confere_manifesto'] = '%d/%d' % (sum(conf), len(conf))
    assert all(conf)
    dst = R22 / 'candidato_r2_2' / 'C'
    if dst.exists():
        raise SystemExit('candidato_r2_2 já existe; nada feito')
    log = {'arquivos': 0, 'reparse_pulados': []}
    copiar_arvore(cand21, dst, log)
    out['copias']['candidato_r2_2'] = log
    for n in ('implantar.py', 'reverter.py', 'implantacao_lib.py'):
        for d in (R22, R22 / 'ref_r2_1'):
            d.mkdir(exist_ok=True)
            t = d / n
            if t.exists():
                raise SystemExit('%s já existe; nada feito' % t)
            t.write_bytes((R21 / n).read_bytes())
            assert sha(t) == sha(R21 / n)
        out['copias'][n] = sha(R21 / n)[:16]
    (R22 / 'runs' / 's0_preparar.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({'base_confere': True, 'candidato_r2_1_manifesto': out['candidato_r2_1_confere_manifesto'],
                      'copiados': log['arquivos'], 'reparse': len(log['reparse_pulados'])}, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main())
