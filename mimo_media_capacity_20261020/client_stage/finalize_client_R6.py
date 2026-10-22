"""Freeze a new final client receipt and Goodall input, no installation."""
from pathlib import Path
import hashlib,json,sys
S=Path(__file__).resolve().parent;W=S.parent;OUT=S/'release_R6'
sys.path.insert(0,str(W));import task
def pin(p):return dict(path=str(p),sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest())
def put(p,b):
    if not isinstance(b,bytes):b=json.dumps(b,ensure_ascii=False,indent=2).encode()
    with Path(p).open('xb') as f:f.write(b)
    assert Path(p).read_bytes()==b
check=task.check('implementation')
plan=json.loads((OUT/'install_plan_R6.json').read_bytes())
for x in plan['files']:
    assert pin(x['source'])['sha256']==x['sha256']
    assert pin(x['destination'])['sha256']==x['baseline'],'Runtime baseline changed'
contract=W/'backend_stage/CONTRACT.json';body=json.loads(contract.read_bytes());assert 'expected_media_scope' in json.dumps(body)
put(OUT/'CONTRACT_BOUND_R6.json',contract.read_bytes())
plan.update(status='PREPARED_CLIENT_R6_WAIT_DISTINCT_REVIEW_NOT_INSTALLED',backend_contract=pin(contract),backend_contract_frozen=pin(OUT/'CONTRACT_BOUND_R6.json'),pending=['Independent real final review','Parent controlled install','Real authenticated browser/WebView QA','Android30 build and private push after review/install'])
plan['backend_R4_handoff']=pin(W/'backend_stage/BACKEND_R4_HANDOFF.json')
plan['supersedes']=[str(S/'release_R5/install_plan_R5.json'),str(S/'android30_R1/DELIVERY_PREPARED_R1.json'),str(S/'android30_R2/DELIVERY_PREPARED_R1.json')]
put(OUT/'install_plan_R6_FINAL.json',plan)
controls=S/'scope_e2e_4f57518ec04a4ddf9eca66fd2197cc47/INDEPENDENT_CONTROLS_R1.json'
control=json.loads(controls.read_bytes())
for x in control['backend']:assert pin(x['path'])==x
replay=S/'host_client_replay_2a8571938ed242ce9e8b20e84152dc91/RESULT.json'
r=json.loads(replay.read_bytes());assert pin(r['host']['path'])==r['host']
receipt=dict(status=plan['status'],reference=str(W/'SESSION_REFERENCE.json'),task_id='implementation',actor=task.OWNER,
    project_revision=check['receipt']['revision'],plan=pin(OUT/'install_plan_R6_FINAL.json'),files=plan['files'],
    asset_sha256=plan['files'][0]['sha256'],versions=dict(ios_baseline=34,ios_candidate=35,android_baseline=29,android_candidate=30),
    contract=pin(contract),backend_handoff=plan['backend_R4_handoff'],tests=dict(helper=pin(OUT/'PRIVATE_MEDIA_TESTS_R6.json'),actual_send=pin(OUT/'CLIENT_FLOW_TESTS_R6.json'),client_scope=pin(OUT/'INDEPENDENT_CONTROLS_R1.json'),real_adapter_client=pin(controls),host_json_idb_reload=pin(replay)),
    assertions=dict(client_regression=91,client_scope=24,host_json_idb=9,actual_adapter_cases=8,actual_adapter_response_client=4),
    response_scope_stripped_before_history=True,token_is_authentication=False,no_retry_uncertain=True,
    canonical_science_preserved='Only the embedded media helper changed from pinned R5; four scientific/context functions and mandatory TGL bytes outside helper unchanged.',
    runtime_writes=False,provider_calls=0,real_network_calls=0,build=False,push=False,
    review='Builder tests are not independent acceptance. Real reviewer must approve final R6 plus current host/backend/routing.')
put(OUT/'DELIVERY_PREPARED_R6.json',receipt)
goodall=dict(final_for_packaging=True,receipt=str((OUT/'DELIVERY_PREPARED_R6.json').relative_to(W)),receipt_sha256=pin(OUT/'DELIVERY_PREPARED_R6.json')['sha256'],receipt_status=receipt['status'],
    files=[dict(target=str(Path(x['destination']).relative_to(Path('C:/IALD/projetos_pyhton/IALD'))).replace('\\','/'),source=str(Path(x['source']).relative_to(W)),sourcehash=x['sha256'],baseline=x['baseline']) for x in plan['files']])
put(S/'GOODALL_CLIENT_GROUP_R6.json',goodall)
put(S/'CICERO_SCOPE_CLIENT_READY_R6.json',dict(status='READY_FOR_SHARED_REVIEW_NOT_DEPLOY',client_receipt=pin(OUT/'DELIVERY_PREPARED_R6.json'),matched_backend=plan['backend_R4_handoff'],real_adapter_controls=pin(controls),interface='expected_media_scope query on POST/GET; actual scope echo top-level validated and stripped',transport='Filesystem handoff; no callable Cicero/Goodall agent handle exposed in this session. Parent relay required.'))
print(json.dumps(pin(OUT/'DELIVERY_PREPARED_R6.json')))
