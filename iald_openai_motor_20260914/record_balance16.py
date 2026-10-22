"""Register the operator's observed balance, without reading any credential."""
import json
from pathlib import Path
import subprocess
import sys
from goal16_records import ROOT, record

sys.stdout.reconfigure(encoding='utf-8')
memory_before = (ROOT / 'CLAUDE.md').read_bytes()
target = ROOT / 'iald_saldo_openai.json'
if target.exists():
    raise SystemExit('Anchor already exists; inspect before replacing.')
helper = ROOT / 'ferramentas_openai/registrar_saldo_openai.py'
args = [r'C:\Python314\python.exe', '-B', str(helper)]
subprocess.run(args + ['--saldo', '9.90', '--em', '2026-09-15T15:15:59+00:00'],
               check=True, capture_output=True, cwd=ROOT)
result = subprocess.run(args + ['--mostrar'], check=True, capture_output=True, cwd=ROOT)
state = json.loads(result.stdout)
assert state['nivel'] != 'desconhecido'
report = {'task': 'T1 — âncora de crédito', 'status': '[REAL]',
          'balance_usd': 9.90, 'observed_at': '2026-09-15T15:15:59+00:00',
          'source': 'https://platform.openai.com/settings/organization/billing/overview',
          'auto_reload': {'enabled': True, 'threshold_usd': 5, 'target_usd': 10,
                          'monthly_limit_usd': 10, 'changed': False},
          'project': 'proj_l5qyviHwvXkQSi7KIjkSofDd',
          'project_monthly_spend_limit': None,
          'project_limit_display': 'No spend limit set',
          'project_limit_changed': False, 'mostrar': state,
          'limitations': ['Saldo estimado a partir da âncora; recargas futuras devem ser registradas.',
                         'Helper --mostrar ainda não injeta chave admin ou acesso HTTP na Costs API.']}
receipt = record('saldo_openai_ancora_20260915.json', report,
    '[REAL] Billing autenticado lido: saldo US$ 9,90 às 15:15:59 UTC. Âncora registrada pelo helper; '
    '`--mostrar` retornou nível ' + state['nivel'] + '. Recarga automática JÁ ligada: gatilho US$ 5, '
    'saldo-alvo US$ 10, máximo mensal US$ 10. Projeto IALD sem limite de gasto configurado. '
    'Nenhuma compra ou mudança de limite/recarga. [OPEN] O saldo é estimado e não detecta sozinho '
    'compras futuras. O helper CLI não injeta a chave admin/HTTP; corrigir essa lacuna antes de '
    'usar seu --mostrar como evidência da Costs API. Servidor não reiniciado.', memory_before)
print(json.dumps({'receipt': str(receipt), 'state': state}, ensure_ascii=False))
