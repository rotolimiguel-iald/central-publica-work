"""Revisor sonnet-app-v407-revisor -- RODADA 2: roda sobre a PRODUCAO a funcao d4_check.d4 que eu entreguei na rodada 1 (D4 reescrito como funcao pura), como segunda implementacao do D4.
Somente leitura. Janela = [mtime de maintenance.json .. mtime de restart.json]."""
import json, os, sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2lib as L
L.install_guard()
import d4_check as D
W, R, HERE = L.W, L.R, L.HERE
rd = L.rd
t0, t1 = os.stat(W / 'maintenance.json').st_mtime, os.stat(W / 'restart.json').st_mtime
r = D.d4(R, rd(W / 'app/RUNTIME_BASELINE.json'), rd(W / 'install_plan.json'), rd(W / 'deployment.json'), t0, t1)
out = {'PASS': r['PASS'], 'checks': r['checks'], 'expected_in_window': r['expected_in_window'], 'stray': r['stray'][:10], 'visited': r['checks']['window_scan_only_plan_backups_logs']['visited']}
(HERE / 'r2_d4_function_out.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, indent=1)[:2500])
