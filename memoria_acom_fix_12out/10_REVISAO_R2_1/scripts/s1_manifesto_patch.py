# -*- coding: utf-8 -*-
"""Revisor c1 R2.1, passo 1: manifesto e patch.

- hashes lidos dos 15 arquivos do candidato R2.1 x manifesto R2.1
- os 12 nao mudados iguais byte a byte ao candidato R2 (4_INTEGRACAO/candidato_r2)
- r2_1_mudancas: sha_r2 e sha_r2_1 conferem
- ferramentas e config: hashes lidos
- prova do patch: copia do candidato R2 (web server REDIGIDO) em tmp proprio, git -c core.autocrlf=false apply,
  comparacao com o R2.1 (web server REDIGIDO). Tambem com core.autocrlf=true para medir o efeito.
Escreve so em 10_REVISAO_R2_1. A chave nunca e impressa.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
WORK = ME.parent
R21 = WORK / '9_R2_1'
INT = WORK / '4_INTEGRACAO'
R2C = INT / 'candidato_r2' / 'C'
R21C = R21 / 'candidato_r2_1' / 'C'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def red(b):
    return KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), b)


def rel_of(target):
    return Path(*Path(target).parts[1:])


out = {'checks': {}}
m21 = json.loads((R21 / 'CANDIDATO_MANIFESTO_R2_1.json').read_text(encoding='utf-8'))
m2 = json.loads((INT / 'CANDIDATO_MANIFESTO_R2.json').read_text(encoding='utf-8'))
out['sha_manifesto_r2_1'] = sha(R21 / 'CANDIDATO_MANIFESTO_R2_1.json')
out['sha_manifesto_r2'] = sha(INT / 'CANDIDATO_MANIFESTO_R2.json')
out['manifesto_r2_1_cita_r2'] = m21['r2']['sha256'] == out['sha_manifesto_r2']

rows = []
m2map = {x['target']: x['sha256'] for x in m2['arquivos']}
for it in m21['arquivos']:
    rel = rel_of(it['target'])
    p21, p2 = R21C / rel, R2C / rel
    s21, s2 = sha(p21), sha(p2)
    rows.append({'target': it['target'], 'manifesto_ok': s21 == it['sha256'], 'bytes_ok': p21.stat().st_size == it['bytes'],
                 'r2_disco_igual_manifesto_r2': s2 == m2map.get(it['target']), 'mudou': s21 != s2,
                 'sha_r2': s2[:16], 'sha_r2_1': s21[:16]})
out['arquivos'] = rows
out['n_arquivos'] = len(rows)
out['n_mudados'] = sum(r['mudou'] for r in rows)
out['todos_manifesto_ok'] = all(r['manifesto_ok'] and r['bytes_ok'] for r in rows)
out['todos_r2_iguais_manifesto_r2'] = all(r['r2_disco_igual_manifesto_r2'] for r in rows)
files = sorted(p for p in R21C.rglob('*') if p.is_file())
out['arquivos_na_arvore_r2_1'] = len(files)
mud = {x['target']: x for x in m21['r2_1_mudancas']}
out['mudancas_declaradas'] = sorted(mud)
out['mudancas_medidas'] = sorted(r['target'] for r in rows if r['mudou'])
out['mudancas_conferem'] = out['mudancas_declaradas'] == out['mudancas_medidas'] and all(
    mud[t]['sha256_r2'][:16] == r['sha_r2'] and mud[t]['sha256_r2_1'][:16] == r['sha_r2_1']
    for r in rows for t in [r['target']] if t in mud)

tools = {}
for n in ['implantar.py', 'reverter.py', 'implantacao_lib.py', 'implantar_config_producao_r2_1.json',
          'RESULTADO_R2_1.md', 'TESTES_R2_1.md', 'CANDIDATO_MANIFESTO_R2_1.json', 'DIFF_R2_R2_1.patch',
          'MANIFESTO_R2_1.json']:
    tools[n] = sha(R21 / n)[:16]
for x in m21['ferramentas']:
    tools[Path(x['arquivo']).name] = {'disco': sha(x['arquivo'])[:16], 'manifesto': x['sha256'][:16]}
out['hashes'] = tools

# chave: quantas ocorrencias em cada web server (sem imprimir)
ws = Path('IALD/projetos_pyhton/IALD/iald_web_server.py')
k2 = KEY.findall((R2C / ws).read_bytes())
k21 = KEY.findall((R21C / ws).read_bytes())
out['chave'] = {'n_r2': len(k2), 'n_r2_1': len(k21), 'iguais': k2 == k21,
                'no_patch': bool(KEY.search((R21 / 'DIFF_R2_R2_1.patch').read_bytes()))}
del k2, k21

# prova do patch
for mode in ['false', 'true']:
    tmp = ME / 'tmp' / ('patch_autocrlf_' + mode)
    if tmp.exists():
        shutil.rmtree(tmp)
    (tmp / 'w').mkdir(parents=True)
    for p in R2C.rglob('*'):
        if p.is_file():
            d = tmp / 'w' / p.relative_to(R2C)
            d.parent.mkdir(parents=True, exist_ok=True)
            d.write_bytes(red(p.read_bytes()))
    subprocess.run(['git', 'init', '-q'], cwd=tmp / 'w')
    r = subprocess.run(['git', '-c', 'core.autocrlf=' + mode, 'apply', '--whitespace=nowarn',
                        str(R21 / 'DIFF_R2_R2_1.patch')], cwd=tmp / 'w', capture_output=True, text=True)
    diffs = []
    for p in R21C.rglob('*'):
        if p.is_file():
            q = tmp / 'w' / p.relative_to(R21C)
            if not q.exists() or q.read_bytes() != red(p.read_bytes()):
                diffs.append(p.relative_to(R21C).as_posix())
    extra = [q.relative_to(tmp / 'w').as_posix() for q in (tmp / 'w').rglob('*')
             if q.is_file() and '.git' not in q.parts and not (R21C / q.relative_to(tmp / 'w')).exists()]
    out['checks']['git_apply_autocrlf_' + mode] = {'rc': r.returncode, 'stderr': r.stderr[-400:],
                                                   'n_diferentes': len(diffs), 'diferentes': diffs, 'extra': extra}
    shutil.rmtree(tmp)

ok = (out['todos_manifesto_ok'] and out['todos_r2_iguais_manifesto_r2'] and out['n_mudados'] == 3
      and out['arquivos_na_arvore_r2_1'] == 15 and out['mudancas_conferem'] and out['manifesto_r2_1_cita_r2']
      and out['checks']['git_apply_autocrlf_false']['rc'] == 0 and out['checks']['git_apply_autocrlf_false']['n_diferentes'] == 0
      and not out['chave']['no_patch'])
out['OK'] = ok
(ME / 'runs' / 's1_manifesto_patch.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: v for k, v in out.items() if k not in ('arquivos',)}, ensure_ascii=False, indent=1))
