# -*- coding: utf-8 -*-
"""Revisor c1 R2.2, passo 1: manifesto e patch por hash. Escreve so em 11_REVISAO_R2_2 (runs + tmp). A chave do web server
nunca e impressa: o web server entra REDIGIDO (mesmo tamanho) nas copias do patch."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
WORK = ME.parent
R22 = WORK / '9_R2_2'
R21 = WORK / '9_R2_1'
C22 = R22 / 'candidato_r2_2' / 'C'
C21 = R21 / 'candidato_r2_1' / 'C'
KEY = re.compile(rb'(AIza[0-9A-Za-z_\-]{20,}|sk-[A-Za-z0-9_\-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[abposr]-[A-Za-z0-9-]{10,})')


def redact(b):
    return KEY.sub(lambda m: m.group(0)[:4] + b'R' * (len(m.group(0)) - 4), b)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rel_de_target(t):
    # C:\IALD\... -> IALD/...
    t = t.replace('\\', '/')
    assert t.lower().startswith('c:/'), t
    return t[3:]


out = {}
man = json.loads((R22 / 'CANDIDATO_MANIFESTO_R2_2.json').read_text(encoding='utf-8'))
out['sha16_manifesto'] = sha((R22 / 'CANDIDATO_MANIFESTO_R2_2.json').read_bytes())[:16]
# 1) 15 arquivos do candidato contra o manifesto
linhas = []
ok = 0
for a in man['arquivos']:
    p = C22 / rel_de_target(a['target'])
    b = p.read_bytes() if p.exists() else None
    bom = b is not None and sha(b) == a['sha256'] and len(b) == a['bytes']
    ok += bom
    linhas.append({'target': a['target'], 'ok': bom, 'role': a.get('role')})
out['candidato_contra_manifesto'] = {'ok': ok, 'de': len(man['arquivos']), 'detalhe_falhas': [l for l in linhas if not l['ok']]}
# 2) arvore: nenhum arquivo fora do manifesto
na_arvore = sorted(str(p.relative_to(C22)).replace('\\', '/') for p in C22.rglob('*') if p.is_file())
no_man = sorted(rel_de_target(a['target']) for a in man['arquivos'])
out['arvore_candidato'] = {'n': len(na_arvore), 'fora_do_manifesto': sorted(set(na_arvore) - set(no_man)), 'faltando': sorted(set(no_man) - set(na_arvore))}
# 3) mudados contra R2.1
mud = []
for rel in no_man:
    b2 = (C22 / rel).read_bytes()
    p1 = C21 / rel
    b1 = p1.read_bytes() if p1.exists() else None
    if b1 != b2:
        mud.append(rel)
decl = sorted(rel_de_target(m['target']) for m in man['r2_2_mudancas'])
out['mudados_contra_R2_1'] = {'reais': mud, 'declarados_r2_2_mudancas': decl, 'iguais': mud == decl}
# sha_r2_1 declarado de cada mudanca confere com o candidato R2.1 real
conf = {}
for m in man['r2_2_mudancas']:
    rel = rel_de_target(m['target'])
    conf[rel] = {'sha_r2_1_declarado_confere': sha((C21 / rel).read_bytes()) == m['sha256_r2_1'],
                 'sha_r2_2_declarado_confere': sha((C22 / rel).read_bytes()) == m['sha256_r2_2']}
out['mudancas_sha'] = conf
# 4) ferramentas
f = []
for ft in man['ferramentas_implantacao']:
    p = Path(ft['arquivo'])
    f.append({'arquivo': p.name, 'sha_confere': sha(p.read_bytes()) == ft['sha256'], 'r2_1_confere': sha((R21 / p.name).read_bytes()) == ft['sha256_r2_1']})
out['ferramentas_implantacao'] = f
# 4b) campo ferramentas (aplicar_blocos)
fb = []
for ft in man['ferramentas']:
    p = Path(ft['arquivo'])
    fb.append({'arquivo': p.name, 'existe': p.exists(), 'sha_confere': p.exists() and sha(p.read_bytes()) == ft['sha256']})
out['ferramentas_campo'] = fb
# 5) patch: hash declarado, apply sobre copia redigida da R2.1
patch = R22 / 'DIFF_R2_1_R2_2.patch'
chk = json.loads((R22 / 'DIFF_R2_1_R2_2_APPLY_CHECK.json').read_text(encoding='utf-8'))
out['patch'] = {'sha256_confere_apply_check': sha(patch.read_bytes()) == chk['patch_sha256'], 'bytes': patch.stat().st_size,
                'chave_no_patch': bool(KEY.search(patch.read_bytes()))}
T = Path(os.environ['SCRATCH']) / 'patchtest'
if T.exists():
    shutil.rmtree(T)
base = T / 'base'
for rel in no_man:
    d = base / rel
    d.parent.mkdir(parents=True, exist_ok=True)
    b = (C21 / rel).read_bytes()
    d.write_bytes(redact(b) if rel.endswith('iald_web_server.py') else b)
for n in ('implantar.py', 'reverter.py', 'implantacao_lib.py'):
    (base / 'ferramentas').mkdir(parents=True, exist_ok=True)
    (base / 'ferramentas' / n).write_bytes((R21 / n).read_bytes())
r = subprocess.run(['git', '-c', 'core.autocrlf=false', 'apply', '--whitespace=nowarn', str(patch)], cwd=str(base), capture_output=True, text=True)
out['patch']['git_apply_rc'] = r.returncode
out['patch']['stderr'] = r.stderr[:300]
dif = []
for rel in no_man:
    b2 = (C22 / rel).read_bytes()
    if rel.endswith('iald_web_server.py'):
        b2 = redact(b2)
    if (base / rel).read_bytes() != b2:
        dif.append(rel)
out['patch']['arquivos_diferentes_apos_apply'] = dif
for n in ('implantar.py', 'reverter.py', 'implantacao_lib.py'):
    if (base / 'ferramentas' / n).read_bytes() != (R22 / n).read_bytes():
        dif.append('ferramentas/' + n)
out['patch']['arquivos_diferentes_apos_apply'] = dif
out['patch']['base_fora_de_repo'] = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], cwd=str(base), capture_output=True, text=True).returncode != 0
# arquivos tocados pelo patch
tocados = re.findall(r'^diff --git a/(\S+) b/', patch.read_text(encoding='utf-8', errors='replace'), re.M)
out['patch']['arquivos_no_patch'] = tocados
# 6) config: diferenca da R2.1
c1 = json.loads((R21 / 'implantar_config_producao_r2_1.json').read_text(encoding='utf-8'))
c2 = json.loads((R22 / 'implantar_config_producao_r2_2.json').read_text(encoding='utf-8'))
out['config_diferencas'] = {k: [c1.get(k), c2.get(k)] for k in sorted(set(c1) | set(c2)) if c1.get(k) != c2.get(k)}
# manifesto em config confere
out['config_manifesto_sha'] = None
for k, v in c2.items():
    if 'manifesto' in k and isinstance(v, str) and Path(v).exists():
        out['config_manifesto_sha'] = {k: v, 'sha16': sha(Path(v).read_bytes())[:16]}
(ME / 'runs' / 's1_manifesto_patch.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])
