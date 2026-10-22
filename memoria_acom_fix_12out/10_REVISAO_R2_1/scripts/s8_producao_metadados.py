# -*- coding: utf-8 -*-
"""Revisor c1 R2.1: so leitura de METADADOS de producao (CAS por sha256 dos 15 alvos contra os originais do manifesto
R2.1; superficies contra o dry-run do R2; banco so tamanho/mtime/journal; nunca conteudo do banco, nunca confidencial).
Mostra tambem o que a trava do implantar R2.1 veria nas pastas de recibo da config de producao (so le JSON de recibo).
Nada e escrito fora de 10_REVISAO_R2_1. Nao roda implantar.py/reverter.py."""
import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
W = ME.parent
R21 = W / '9_R2_1'
man = json.loads((R21 / 'CANDIDATO_MANIFESTO_R2_1.json').read_text(encoding='utf-8'))
cfg = json.loads((R21 / 'implantar_config_producao_r2_1.json').read_text(encoding='utf-8'))
orig = {o['source'].lower(): o['sha256'] for o in man['originais']}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


out = {'medido_em': datetime.now().isoformat(timespec='seconds'), 'alvos': [], 'superficies': []}
for a in man['arquivos']:
    p = Path(a['target'])
    e = p.exists()
    s = sha(p) if e else None
    out['alvos'].append({'alvo': p.name, 'existe': e,
                         'cas_ok': (s == orig.get(str(p).lower())) if e else (orig.get(str(p).lower()) is None),
                         'ja_e_o_candidato': s == a['sha256']})
rec = json.loads((W / '4_INTEGRACAO' / 'recibos_producao_r2' / 'RECIBO_IMPLANTACAO_dry_run.json').read_text(encoding='utf-8'))
for s in rec['passos']['pre_conferencias']['superficies_antes']:
    p = Path(s['path'])
    out['superficies'].append({'arquivo': p.name, 'igual_ao_dry_run_r2': p.exists() and sha(p) == s['sha256']})
state = Path('C:/IALD/MEMORIA_IALD/state')
db = state / 'memory.sqlite3'
st = db.stat()
out['banco'] = {'bytes': st.st_size, 'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
                'bytes_no_dry_run_r2': rec['passos']['pre_conferencias']['banco_antes']['bytes'],
                'journal_presente': (state / 'memory.sqlite3-journal').exists()}
baks = [p for p in state.iterdir() if p.name.startswith('memory.sqlite3.bak_')]
out['backups_legados'] = {'n': len(baks), 'bytes': sum(p.stat().st_size for p in baks)}
out['D_IALD_ARQUIVO_existe'] = Path('D:/IALD_ARQUIVO').exists()
out['livre_bytes'] = {'C': shutil.disk_usage('C:/').free, 'D': shutil.disk_usage('D:/').free}
out['pasta_recibos_r2_1_existe'] = Path(cfg['recibos_dir']).exists()
out['recibos_r2_listados'] = sorted(p.name for p in Path(cfg['recibos_dirs_anteriores'][0]).iterdir())
sys.path.insert(0, str(R21))
import implantacao_lib as L  # noqa: E402  (so a funcao de leitura de recibos)
r = L.recibos_pendentes([cfg['recibos_dir']] + cfg.get('recibos_dirs_anteriores', []))
out['trava_veria'] = {'pendentes': len(r['pendentes']), 'ilegiveis': len(r['ilegiveis'])}
out['candidato_root_existe'] = Path(cfg['candidato_root']).exists()
for k in ('ordem_operador', 'bridge_v2', 'aplicar_blocos', 'memory_md'):
    out.setdefault('extras_existem', {})[k] = Path(cfg[k]).exists()
out['superficies_config_existem'] = all(Path(p).exists() for p in cfg['superficies'])
out['resumo'] = {'alvos_cas_ok': sum(x['cas_ok'] for x in out['alvos']), 'n_alvos': len(out['alvos']),
                 'superficies_iguais': sum(x['igual_ao_dry_run_r2'] for x in out['superficies']),
                 'n_superficies': len(out['superficies'])}
(ME / 'runs' / 's8_producao_metadados.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: v for k, v in out.items() if k not in ('alvos', 'superficies')}, ensure_ascii=False, indent=1))
