# -*- coding: utf-8 -*-
"""Conferência SÓ-LEITURA de que a produção não foi tocada pela integração: sha256 dos 9 alvos existentes
== originais congelados; os 6 novos não existem; as 6 superfícies D5 com sha256 atual (e se o bloco antigo segue no
topo); inventário do state (banco, nº e bytes dos .bak_, sem journal/ nem snapshots/); D:\\IALD_ARQUIVO ausente.
Nenhum confidencial aberto. Escreve evidencias/PRODUCAO_INTOCADA.json.
"""
from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE = Path(r'C:\IALD\MEMORIA_IALD\state')
SUPERFICIES = [r'C:\Users\rotol\.claude\CLAUDE.md', r'C:\Users\rotol\.codex\AGENTS.md', r'C:\IALD\projetos_pyhton\IALD\CLAUDE.md',
               r'C:\IALD\PROGRAMA_IALD\README.md', r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\COORDINATOR.md',
               r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md']


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    cand = json.loads((HERE / 'CANDIDATO_MANIFESTO.json').read_text(encoding='utf-8'))
    orig = {o['source'].lower(): o for o in cand['originais']}
    out = {'at': datetime.now(timezone.utc).isoformat(), 'alvos': [], 'superficies': [], 'state': {}}
    ok = True
    for a in cand['arquivos']:
        t = Path(a['target'])
        o = orig.get(a['target'].lower())
        if o:
            real = sha256_file(t)
            same = real == o['sha256']
            ok &= same
            out['alvos'].append({'alvo': str(t), 'existe': True, 'sha256': real, 'igual_ao_original_congelado': same, 'bytes': t.stat().st_size})
        else:
            exists = t.exists()
            ok &= not exists
            out['alvos'].append({'alvo': str(t), 'existe': exists, 'novo_na_v2': True, 'nao_existe_em_producao': not exists})
    for s in SUPERFICIES:
        p = Path(s)
        b = p.read_bytes()
        out['superficies'].append({'arquivo': s, 'bytes': len(b), 'sha256': sha256_file(p), 'linhas': b.count(b'\n'),
                                   'bloco_antigo_no_topo': b.startswith(b'<!-- IALD_COMMON_ACOM_SESSION_ENTRY_20261010 -->'),
                                   'bloco_novo_presente': b'IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012' in b,
                                   'linha_memoria_acom': b.count(b'- Mem\xc3\xb3ria ACOM:'),
                                   'mtime': datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec='seconds')})
        if p.name != 'MEMORY.md':
            ok &= out['superficies'][-1]['bloco_antigo_no_topo'] and not out['superficies'][-1]['bloco_novo_presente']
    entries = sorted(STATE.iterdir())
    baks = [e for e in entries if e.name.startswith('memory.sqlite3.bak_')]
    db = STATE / 'memory.sqlite3'
    out['state'] = {'db_bytes': db.stat().st_size, 'db_mtime': datetime.fromtimestamp(db.st_mtime if hasattr(db, 'st_mtime') else db.stat().st_mtime).isoformat(timespec='seconds'),
                    'backups_n': len(baks), 'backups_bytes': sum(e.stat().st_size for e in baks),
                    'journal_dir': (STATE / 'journal').exists(), 'snapshots_dir': (STATE / 'snapshots').exists(),
                    'pre_v2': [e.name for e in entries if '.pre_v2_' in e.name], 'guard_refusals': (STATE / 'guard_refusals.jsonl').exists(),
                    'outros': [e.name for e in entries if not e.name.startswith('memory.sqlite3')]}
    ok &= not out['state']['journal_dir'] and not out['state']['snapshots_dir'] and not out['state']['pre_v2']
    out['D_IALD_ARQUIVO_existe'] = Path(r'D:\IALD_ARQUIVO').exists()
    ok &= not out['D_IALD_ARQUIVO_existe']
    out['producao_intocada'] = bool(ok)
    (HERE / 'evidencias').mkdir(exist_ok=True)
    (HERE / 'evidencias' / 'PRODUCAO_INTOCADA.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'producao_intocada': out['producao_intocada'], 'state': {k: out['state'][k] for k in ('db_bytes', 'backups_n', 'backups_bytes', 'journal_dir', 'snapshots_dir')},
                      'superficies': [(Path(s['arquivo']).name, s['sha256'][:16], s['bytes'], s['bloco_antigo_no_topo'], s['mtime']) for s in out['superficies']]}, ensure_ascii=False))


if __name__ == '__main__':
    main()
