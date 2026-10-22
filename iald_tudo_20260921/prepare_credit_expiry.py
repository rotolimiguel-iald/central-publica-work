"""Prepare support for provider-observed date-only expiry in the admin panel."""
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')

def main():
    source_path = ROOT / 'iald_deadlines.py'
    source_raw = source_path.read_bytes()
    source = source_raw.decode('utf8')
    assert source.count('from datetime import datetime, timezone') == 1
    source = source.replace('from datetime import datetime, timezone', 'from datetime import date, datetime, timezone', 1)
    old = '    for ident, label in LABELS.items():\n'
    new = '''    labels = dict(LABELS)
    # Optional operational records appear only after provider observation.
    for ident, label in (('anthropic_credit', 'Créditos Claude'),
                         ('anthropic_admin_key', 'Chave administrativa Claude')):
        if ident in raw['items']:
            labels[ident] = label
    for ident, label in labels.items():
'''
    assert source.count(old) == 1
    source = source.replace(old, new, 1)
    old = '        items.append(row)\n'
    new = '''        elif entry.get('expires_on') is not None:
            try:
                value = entry['expires_on']
                if (not isinstance(value, str) or len(value) != 10
                        or entry.get('date_timezone') != 'UTC'):
                    raise ValueError('Provider date or timezone missing')
                day = date.fromisoformat(value)
                if day.isoformat() != value:
                    raise ValueError('Expected full ISO date')
                delta = (day - now.astimezone(timezone.utc).date()).days
                level = ('expired' if delta < 0 else 'critical' if delta <= 3
                         else 'warning' if delta <= 14 else 'attention' if delta <= 30 else 'ok')
                when = day.strftime('%d/%m/%Y')
                message = (f'Prazo informado encerrado em {when} (UTC).' if delta < 0 else
                           f'Vence hoje ({when}, UTC) — horário não informado.' if delta == 0 else
                           f'Vence em {when} (UTC); faltam {delta} dias de calendário — horário não informado.')
                row.update(expires_on=value, date_timezone='UTC', precision='date',
                           days_remaining=max(0, delta), level=level, message=message,
                           alert_threshold_days=next((n for n in (1, 3, 7, 14, 30) if delta <= n), None))
            except (ValueError, TypeError, AttributeError, OverflowError):
                row['message'] = 'Data ou fuso inválido — conferir no provedor.'
        items.append(row)
'''
    assert source.count(old) == 1
    source = source.replace(old, new, 1)
    stage = WORK / ('credit_expiry_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    stage.mkdir()
    target = stage / 'iald_deadlines.py'
    with target.open('xb') as stream:
        stream.write(source.encode('utf8'))
    spec = importlib.util.spec_from_file_location('date_expiry_candidate', target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    spec = importlib.util.spec_from_file_location('existing_expiry_tests', WORK / 'test_deadlines.py')
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
    tests.module = module
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
    assert result.wasSuccessful()
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / 'fixture.json'
        fixture = {'items': {'anthropic_credit': {'expires_at': None, 'expires_on': '2027-09-23', 'date_timezone': 'UTC'}}}
        path.write_bytes(json.dumps(fixture).encode())
        now = datetime(2027, 9, 22, 23, tzinfo=timezone.utc)
        row = module.snapshot(path, now)['items'][-1]
        assert row['days_remaining'] == 1 and row['expires_at'] is None and row['precision'] == 'date'
        row = module.snapshot(path, now.replace(day=23))['items'][-1]
        assert row['level'] == 'critical' and row['days_remaining'] == 0 and 'horário não informado' in row['message']
        row = module.snapshot(path, now.replace(day=24))['items'][-1]
        assert row['level'] == 'expired'
        del fixture['items']['anthropic_credit']['date_timezone']
        path.write_bytes(json.dumps(fixture).encode())
        assert module.snapshot(path, now)['items'][-1]['level'] == 'unknown'
    baseline = ROOT / 'iald_deadlines.json'
    before = baseline.read_bytes()
    dates = json.loads(before)
    dates['items']['anthropic_credit'] = {'label': 'Créditos Claude', 'expires_at': None,
        'expires_on': '2027-09-23', 'date_timezone': 'UTC',
        'source': 'Anthropic Console Billing, observed 2026-09-22T19:07:03.985Z; invoice dates labeled UTC; no time shown.'}
    dates['checked_at'] = datetime.now().astimezone().isoformat()
    raw = (json.dumps(dates, ensure_ascii=False, indent=2) + '\n').encode('utf8')
    with (stage / 'iald_deadlines.json').open('xb') as stream:
        stream.write(raw)
    receipt = {'status': 'PREPARED_NOT_INSTALLED', 'tests_existing': result.testsRun,
        'date_only_checks': 4, 'server_or_app_files_changed': 0,
        'old_module_sha256': hashlib.sha256(source_raw).hexdigest(),
        'new_module_sha256': hashlib.sha256(source.encode('utf8')).hexdigest(),
        'old_data_sha256': hashlib.sha256(before).hexdigest(), 'new_data_sha256': hashlib.sha256(raw).hexdigest()}
    with (stage / 'receipt.json').open('xb') as stream:
        stream.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'stage': str(stage), 'tests': result.testsRun, 'date_only_checks': 4}))

if __name__ == '__main__':
    main()
