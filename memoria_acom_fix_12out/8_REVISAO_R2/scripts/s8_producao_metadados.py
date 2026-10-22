# Revisor R2: so leitura de METADADOS da producao (CAS por sha256 dos alvos de codigo e das superficies; banco so
# tamanho/mtime; nunca conteudo do banco). Nada e escrito fora de 8_REVISAO_R2.
import json, hashlib, shutil
from pathlib import Path
from datetime import datetime
W = Path(__file__).resolve().parents[2]
man = json.loads((W / '4_INTEGRACAO' / 'CANDIDATO_MANIFESTO_R2.json').read_text(encoding='utf-8'))
orig = {o['source'].lower(): o['sha256'] for o in man['originais']}
out = {'medido_em': datetime.now().isoformat(timespec='seconds'), 'alvos': [], 'superficies': []}
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()
for a in man['arquivos']:
    p = Path(a['target']); e = p.exists()
    s = sha(p) if e else None
    out['alvos'].append({'alvo': p.name, 'existe': e, 'cas_ok': (s == orig.get(str(p).lower())) if e else (orig.get(str(p).lower()) is None)})
rec = json.loads((W / '4_INTEGRACAO' / 'recibos_producao_r2' / 'RECIBO_IMPLANTACAO_dry_run.json').read_text(encoding='utf-8'))
for s in rec['passos']['pre_conferencias']['superficies_antes']:
    p = Path(s['path']); out['superficies'].append({'arquivo': p.name, 'igual_ao_dry_run': p.exists() and sha(p) == s['sha256']})
state = Path('C:/IALD/MEMORIA_IALD/state'); db = state / 'memory.sqlite3'; st = db.stat()
out['banco'] = {'bytes': st.st_size, 'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='seconds'),
                'igual_ao_dry_run_em_bytes': st.st_size == rec['passos']['pre_conferencias']['banco_antes']['bytes'],
                'journal_presente': (state / 'memory.sqlite3-journal').exists()}
baks = [p for p in state.iterdir() if p.name.startswith('memory.sqlite3.bak_')]
out['backups_legados'] = {'n': len(baks), 'bytes': sum(p.stat().st_size for p in baks)}
out['D_IALD_ARQUIVO_existe'] = Path('D:/IALD_ARQUIVO').exists()
out['livre_bytes'] = {'C': shutil.disk_usage('C:/').free, 'D': shutil.disk_usage('D:/').free}
out['resumo'] = {'alvos_cas_ok': sum(x['cas_ok'] for x in out['alvos']), 'n_alvos': len(out['alvos']),
                 'superficies_iguais': sum(x['igual_ao_dry_run'] for x in out['superficies']), 'n_superficies': len(out['superficies'])}
(W / '8_REVISAO_R2' / 'runs' / 's8_producao_metadados.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: out[k] for k in ('medido_em', 'resumo', 'banco', 'backups_legados', 'D_IALD_ARQUIVO_existe', 'livre_bytes')}, ensure_ascii=False))
