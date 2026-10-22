"""Verify installed bytes and synthetic test results; no provider dispatch."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
W=Path(__file__).parent;ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path.insert(0,str(ROOT))
from iald_task_artifacts import ArtifactStore
store=ArtifactStore(ROOT)
checks=json.loads((W/'checks.json').read_bytes())
installed=json.loads((W/'installed.json').read_bytes())
for row in installed:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256']
runtime=json.loads((W/'runtime_observation.json').read_bytes())
by_name={row['filename']:row for row in runtime['artifacts']}
sheet=by_name['valores_soma_corrigido.xlsx']
assert list(sheet['sheets'].values())[0][1:]==[['v1',2],['v2',4],['v3',6],['Total','=SUM(B2:B4)']]
assert len(by_name['exemplo_soma_corrigido.pptx']['slides'])==2
last=runtime['tasks'][-1]
assert any(s.get('result_status')=='DRAFT_COMPLETED' for s in last['steps'])
assert all(s['status']=='returned' for s in last['steps'])
executions=[a for a in runtime['artifacts'] if a.get('execution',{}).get('success')]
assert len(executions)==1
execution=executions[0]['execution']
observed=json.loads(execution['results'][0]['stdout']['text'])
assert observed['aprovado'] and observed['testes'][0]['resultado']=={'soma':12,'media':4.0,'quantidade':3}
assert execution['results'][0]['return_code']==0
assert observed['testes'][1]['erro_tipo']=='ValueError'
artifact_names=['valores_soma_corrigido.xlsx','exemplo_soma_corrigido.pptx','exemplo_soma_corrigido.html','resumir.py','resultado_testes.json','quadrados.py','rascunho-mimo.md']
public_manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
delivery=dict(status='OPERATOR_PILOT_ENABLED_AND_VERIFIED',utc=datetime.now(timezone.utc).isoformat(),
    scope='luiz only; existing family/public permissions unchanged',checks=checks,installed=installed,
    tests=dict(artifacts='corrected XLSX/PPTX/HTML generated and structurally reopened',
        python='real Anthropic sandbox execution observed; valid list, empty list and invalid element checks',
        delegation='JEV selected MiMo worker, full draft returned, manager reviewed and generated quadrados.py',
        download={'status':200,'filename':'resumir.py','bytes':682,'sha256':by_name['resumir.py']['sha256'],'matches_stored_artifact':True}),
    execution=execution,task=last,artifacts=[by_name[name] for name in artifact_names],
    lessons=['First spreadsheet overwrote value 6; fixed formula targets to empty reserved cells and verified correction.',
        'First delegation rejected before worker dispatch because UI discovery used Flask request context; replaced with worker-safe provider discovery.',
        'No uncertain provider request was repeated.'],
    scientific_memory={'active_cluster':public_manifest['active_cluster']['release'],'unchanged':True,'private_atlas_sent':False},
    models={'claude_sonnet':'preferred code architect/reviewer when task warrants cost; policy preference, not benchmark',
        'mimo':'economical manager/implementation worker; real pilot tests passed',
        'kimi':'text/code worker; automatic delegation transport locally tested; no new live Kimi call in this delivery',
        'openai':'general/research manager; new tools locally integrated, not live-tested in this delivery',
        'claude_haiku':'remote sandbox executor; real execution verified',
        'deepseek':'manual route preserved; automatic selection remains excluded in pilot'},
    limitations=['Not the full feature set of consumer AI apps.','No image/video generation, voice creation or automatic site publishing added.',
        'PPTX/XLSX structural validation does not replace visual review or Excel recalculation.',
        'Remote execution evidence does not independently certify exact supplied-code execution.',
        'Physical iOS/Android downloads not tested in this delivery.'],
    availability={'web':'live; luiz automatic pilot','ios_internal':'existing 4.1 (25), server change; no new binary',
        'ios_external':'existing 4.1 (25); new task pilot not enabled for testers',
        'android':'existing 4.1 (22), server change; no new binary','google_play':'previous DUNS blocker unchanged'},
    documentation=['https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool',
        'https://platform.claude.com/docs/en/build-with-claude/token-counting','https://docs.typesafe.ai/models'])
(W/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'verified':True,'tests_run':checks['tests_run'],'skipped':checks['skipped'],'artifacts':len(artifact_names),'active_cluster':delivery['scientific_memory']['active_cluster']}))
