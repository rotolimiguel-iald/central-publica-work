# -*- coding: utf-8 -*-
"""E6 (revisão A): implantação que FALHA no meio do passo 4 (um alvo somente-leitura, o último do manifesto) e a
reversão a partir do recibo dessa implantação. Pergunta: o reverter.py devolve o sistema a um estado coerente?
Sandbox = cópia (rodar_ensaio.montar_raiz) dentro de 5_REVISAO_A; nenhum processo gerido; sob a guarda."""
import json, os, sqlite3, stat, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rodar_ensaio as E
mont = E.montar_raiz(sizes=(12, 6, 0))
cfg_path, cfg = E.config()
manifesto = json.loads(Path(cfg['manifesto_candidato']).read_text(encoding='utf-8'))
last = manifesto['arquivos'][-1]['target']
alvo_ro = None
for root, real in cfg['raizes'].items():
    if last.lower().startswith(root.lower()):
        alvo_ro = Path(real) / last[len(root):].lstrip(chr(92))
os.chmod(alvo_ro, stat.S_IREAD)            # o alvo fica somente-leitura: os.replace falha no Windows
res = {'alvo_somente_leitura': str(alvo_ro), 'ordem_manifesto': [a['target'].rsplit(chr(92), 1)[-1] for a in manifesto['arquivos']]}
r = E.run([E.INT / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
rec = json.loads((E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json').read_text(encoding='utf-8'))
res['implantar'] = {'rc': r['rc'], 'stdout': r['stdout'][-600:], 'status': rec['status'],
                    'passo4': {k: v for k, v in rec['passos'].get('substituir_arquivos', {}).items() if k != 'arquivos'},
                    'passo4_tem_lista_de_arquivos': 'arquivos' in rec['passos'].get('substituir_arquivos', {})}
def estado():
    out = {}
    for item in manifesto['arquivos']:
        prod = item['target']
        for root, real in cfg['raizes'].items():
            if prod.lower().startswith(root.lower()):
                a = Path(real) / prod[len(root):].lstrip(chr(92))
        out[prod.rsplit(chr(92), 1)[-1]] = ('candidato' if a.exists() and E.sha256_file(a) == item['sha256'] else
                                         'ausente' if not a.exists() else 'original_ou_outro')
    mem = Path(cfg['raizes'][r'C:\IALD\MEMORIA_IALD'])
    c = sqlite3.connect('file:%s?mode=ro' % (mem / 'state' / 'memory.sqlite3').as_posix(), uri=True)
    sv = c.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]; c.close()
    # a lib instalada consegue ler o banco?
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', '-c',
        'import sys,json; sys.path.insert(0, sys.argv[1]); from iald_memory import MemoryStore; '
        'print(MemoryStore(sys.argv[2]).get(sys.argv[3], {"house":"IALD","principal":"operator"})["revision"])',
        str(mem / 'lib'), str(mem / 'state'), mont['contexts'][0]], capture_output=True)
    return {'arquivos': out, 'schema_version': sv, 'lib_instalada_le_o_banco': p.returncode == 0,
            'lib_erro': p.stderr.decode()[-300:] if p.returncode else None,
            'tmp_deixados': sorted(x.name for x in alvo_ro.parent.glob('*.tmp_*'))}
res['depois_da_falha'] = estado()
os.chmod(alvo_ro, stat.S_IREAD | stat.S_IWRITE)
r2 = E.run([E.INT / 'reverter.py', '--recibo', E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json'])
rr = json.loads((E.RAIZ / 'recibos' / 'RECIBO_REVERSAO.json').read_text(encoding='utf-8'))
res['reverter'] = {'rc': r2['rc'], 'stdout': r2['stdout'][-700:], 'status': rr['status'],
                   'passos': {k: (v['status'], v.get('nota')) for k, v in rr['passos'].items()}}
res['depois_da_reversao'] = estado()
(HERE.parent.parent / 'exp' / 'runs').mkdir(parents=True, exist_ok=True)
(HERE.parent.parent / 'exp' / 'runs' / 'e6_parcial.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(res, ensure_ascii=False, indent=1))
