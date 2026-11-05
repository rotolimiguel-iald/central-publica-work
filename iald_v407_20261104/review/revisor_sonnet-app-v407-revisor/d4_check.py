"""Revisor sonnet-app-v407-revisor -- D4 REESCRITO como funcao pura, para a rodada da INSTALACAO (nao a executo sobre a producao agora).
D4 (texto do briefing): "os arquivos do RUNTIME_BASELINE ficam intactos, EXCETO o manifesto ativo iald_nucleo_fixo.json, que o plano troca por desenho
(conferir backup dos bytes do baseline e hash novo = plano); a varredura de escopo da janela conta os plano, os backups e os logs do supervisor como mudancas esperadas".
Entradas: raiz, RUNTIME_BASELINE.json (dict), install_plan.json (dict), deployment.json (dict) e a janela [t0, t1] em epoch. Somente leitura."""
import hashlib, os
from pathlib import Path

sha = lambda b: hashlib.sha256(b).hexdigest()


def d4(root, baseline, plan, deployment, t0, t1, logs_subdir='logs', skip_dirs=('.git', 'node_modules', '__pycache__')):
    root = Path(root)
    res = {'checks': {}, 'stray': [], 'expected_in_window': {'plan': 0, 'backups': 0, 'logs': 0}}
    files = plan['files']
    manifest_dest = os.path.normcase(files[-1]['destination'])
    # (1) baseline intacto, exceto o manifesto ativo
    changed, missing = [], []
    man_entry = None
    for e in baseline['files']:
        p = Path(e['path'])
        if os.path.normcase(str(p)) == manifest_dest:
            man_entry = e
            continue
        if not p.is_file():
            missing.append(str(p)); continue
        if sha(p.read_bytes()) != e['sha256']:
            changed.append(str(p))
    res['checks']['baseline_intact_except_manifest'] = {'ok': not changed and not missing, 'n': len(baseline['files']) - 1, 'changed': changed[:5], 'missing': missing[:5]}
    # (2) manifesto: backup dos bytes do baseline + hash novo = plano
    bk = (deployment.get('backups') or {})
    bpath = next((v for k, v in bk.items() if os.path.normcase(k) == manifest_dest), None)
    ok_backup = bool(bpath) and Path(bpath).is_file() and man_entry is not None and sha(Path(bpath).read_bytes()) == man_entry['sha256'] == files[-1]['baseline']
    cur = sha(Path(files[-1]['destination']).read_bytes()) if Path(files[-1]['destination']).is_file() else None
    res['checks']['manifest_backup_bytes_and_new_hash'] = {'ok': bool(ok_backup and cur == files[-1]['sha256'] == deployment.get('files', {}).get(files[-1]['destination'], files[-1]['sha256'])), 'backup_ok': ok_backup, 'current_equals_plan': cur == files[-1]['sha256']}
    # (3) varredura da janela: so' plano, backups e logs do supervisor
    plan_dests = {os.path.normcase(r['destination']) for r in files}
    backups = {os.path.normcase(v) for v in bk.values()}
    logs_root = os.path.normcase(str(root / logs_subdir)) + os.sep
    visited = 0
    for top, dirs, fns in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in fns:
            fp = Path(top) / fn
            try:
                mt = fp.stat().st_mtime
            except OSError:
                continue
            visited += 1
            if not (t0 <= mt <= t1):
                continue
            k = os.path.normcase(str(fp))
            if k in plan_dests:
                res['expected_in_window']['plan'] += 1
            elif k in backups:
                res['expected_in_window']['backups'] += 1
            elif k.startswith(logs_root):
                res['expected_in_window']['logs'] += 1
            else:
                res['stray'].append(str(fp))
    res['checks']['window_scan_only_plan_backups_logs'] = {'ok': not res['stray'], 'visited': visited, 'stray_sample': res['stray'][:5]}
    res['PASS'] = all(c['ok'] for c in res['checks'].values())
    return res
