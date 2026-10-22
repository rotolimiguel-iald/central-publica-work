"""Record browser-observed billing metadata; no credential or payment actions."""
from datetime import datetime
import json
from pathlib import Path

WORK = Path(r'C:\IALD\Central de Patentes\work\iald_saldo_claude_20260922')
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')

def create(path, content):
    with path.open('xb') as stream:
        stream.write(content)
    assert path.read_bytes() == content

def main():
    WORK.mkdir(exist_ok=True)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    anchor = json.loads((ROOT / 'iald_saldo_claude.json').read_bytes())['ancora']
    assert anchor['valor_usd'] == 98.53 and anchor['em'].startswith('2026-09-22T19:07:03')
    result = {
        'observed_at': '2026-09-22T19:07:03.985Z',
        'source_url': 'https://platform.claude.com/settings/billing',
        'organization': 'IALD LTDA',
        'balance_usd': 98.53,
        'auto_reload': False,
        'credit_grant': {'amount_usd': 100, 'date_displayed': '22 de set. de 2026',
                         'expiry_displayed': '23 de set. de 2027',
                         'expires_on': '2027-09-23', 'exact_expiry_time': None},
        'anchor_written': anchor,
        'cost_source': 'IALD ledger only; administrative key not yet created',
        'admin_key_draft': {'name': 'IALD servidor - leitura de custos',
                            'expiry_selected': '2026-12-21T17:00:00-03:00',
                            'created': False, 'operator_approval': 'pending'},
        'purchases_or_billing_changes': 0,
        'admin_panel_visual_check': 'pending authenticated operator session',
        'credit_expiry_panel_integration': 'pending; date recorded without inventing a time',
    }
    path = WORK / 'ancora.json'
    before = path.read_bytes() if path.exists() else None
    if before is not None:
        create(path.with_name(path.name + '.bak_' + stamp), before)
    data = json.dumps(result, ensure_ascii=False, indent=2).encode('utf8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    create(temp, data)
    assert (path.read_bytes() if path.exists() else None) == before
    temp.replace(path)
    assert path.read_bytes() == data
    print(json.dumps({'receipt': str(path), 'balance_usd': result['balance_usd']}))

if __name__ == '__main__':
    main()
