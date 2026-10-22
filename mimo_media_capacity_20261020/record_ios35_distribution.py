"""Record only states actually observed in the authenticated Apple UI."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
W=Path(__file__).resolve().parent
def pin(name):
    p=W/'mobile_stage'/name
    raw=p.read_bytes()
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
eq=(W/'mobile_stage/IOS35_EQUIPE.txt').read_text()
pi=(W/'mobile_stage/IOS35_PILOTO.txt').read_text()
op=(W/'mobile_stage/IOS35_OPERATOR_PARTICIPATION.txt').read_text()
assert '4.1 (35)' in eq and 'Em testes' in eq
assert '4.1 (35)' in pi and 'Em testes' in pi
assert 'Luiz Antonio Rotoli Miguel' in op and 'Instalado 4.1' in op and '( 35 )' in op
value=dict(status='OBSERVED_TESTING_BOTH_EXISTING_GROUPS',observed_at=datetime.now(timezone.utc).isoformat(),
 version='4.1',build='35',cloud_run='0f6ac04a-e005-4831-874e-c8952e3ffa82',
 cloud_status='Processada com sucesso',commit='46753594c421b186c20d7cc0e4b9d3d3f7ce448f',
 testflight_build_id='321fab2e-183c-4360-8b9f-9d163190a418',
 groups=[dict(name='IALD Equipe',type='internal',testers=1,status='Em testes',operator_participation_verified=True),
         dict(name='IALD Piloto',type='external',testers=6,status='Em testes')],
 apple_reported_operator_installed='4.1(35)',apple_install_date_displayed='20 de out. de 2026',
 physical_installation_verified=False,expiry_displayed='Expira em 90 dias',expires_at=None,
 expiry_scope='Relative display only; exact expiration timestamp unavailable, not inferred.',
 beta_notes_submitted=True,automatic_tester_notification_existing_setting=True,
 testers_or_permissions_modified=False,manual_duplicate_build_started=False,
 sources=[pin(n) for n in ['IOS35_CLOUD_SUCCESS.jpg','IOS35_BOTH_GROUPS.jpg','IOS35_EQUIPE.txt',
                           'IOS35_OPERATOR_PARTICIPATION.txt','IOS35_PILOTO.txt','IOS35_PILOTO.jpg']])
with (W/'mobile_stage/IOS35_DISTRIBUTION.json').open('xb') as f:
    f.write(json.dumps(value,ensure_ascii=False,indent=2).encode())
print('iOS35: both groups testing; operator participation verified; physical test not asserted')
