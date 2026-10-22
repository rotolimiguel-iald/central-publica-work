"""Persist the observed delivery matrix; operational dates stay admin-only."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent

def create(path, raw):
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert path.read_bytes() == raw

def main():
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    target = ROOT / 'iald_deadlines.json'
    before = target.read_bytes()
    data = json.loads(before)
    data['checked_at'] = now.isoformat()
    for key, group in [('testflight_internal', 'IALD Equipe'), ('testflight_external', 'IALD Piloto')]:
        data['items'][key].update(expires_at=None, label=f'IALD 4.1 (21) — {group}',
            source='App Store Connect,23/09/2026: Em testes; Expira em90dias. Data exata não exibida; não inferida.',
            build='4.1 (21)', status='Em testes')
    after = (json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode('utf8')
    backup = target.with_name(target.name + '.bak_' + stamp)
    create(backup, before)
    temporary = target.with_name(target.name + '.tmp_' + stamp)
    create(temporary, after)
    assert target.read_bytes() == before
    os.replace(temporary, target)
    assert target.read_bytes() == after
    receipt = {
        'observed_at': now.isoformat(),
        'web': 'Deployed Haiku client, Selo and exports; no operational alerts in chat app',
        'ios': {'version':'4.1 (21)', 'internal':'Em testes', 'external':'Em testes',
                'build_id':'b0da2779-223c-4470-854f-32bfb5b806a4',
                'external_auto_notify':True,
                'physical_test':'Operator confirmed updating and saving Text, Markdown and PDF on iPhone'},
        'android':{'version':'4.1 (20)', 'apk':'https://demo.iald.ia.br/downloads/IALD-4.1-20.apk',
                   'receipt':'android20_20260923_083715_070156.json','download_requires_login':True,
                   'physical_test':'pending','google_play':'registration/DUNS pending'},
        'haiku':{'public_enabled':False,'operator_enabled':True,
                 'issue':'Tool results exhaust remaining context during QG request; fix in progress'},
        'billing':{'balance_usd':96.24,'observed_at':'2026-09-23T11:40:18.351Z',
                   'source':'Anthropic billing UI; stored using existing provider-balance script'},
        'admin_deadlines_sha256':hashlib.sha256(after).hexdigest(),
        'admin_deadlines_backup':str(backup),
        'limits':['Exact TestFlight expiry not provided by UI','No new paid model calls by agent']}
    path=WORK/('release21_delivery_'+stamp+'.json')
    create(path,(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
    print(json.dumps({'receipt':str(path),'admin_metadata_updated':True}))

if __name__=='__main__':
    main()
