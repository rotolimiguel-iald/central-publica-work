"""Read-only source comparison; write only this staging manifest."""
import ast
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import build_staging

ROOT=Path(__file__).resolve().parent
SOURCE=build_staging.SOURCE


def pin(path):
    raw=path.read_bytes()
    return {'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}


def main():
    baseline=json.loads((ROOT/'BASELINE.json').read_text())
    source_checks=[]
    for entry in baseline:
        current=pin(Path(entry['path']))
        current['unchanged']=current['sha256']==entry['sha256']
        if not current['unchanged']:raise ValueError('Runtime changed; do not install stale patch')
        transform=build_staging.server_patch if Path(entry['path']).name=='iald_web_server.py' else build_staging.motor_patch
        raw=Path(entry['path']).read_bytes()
        modified=transform(raw.decode('utf-8').replace('\r\n','\n'))
        ast.parse(modified)
        output=build_staging.preserve_unchanged_bytes(raw,modified)
        if hashlib.sha256(output).hexdigest()!=entry['patched_sha256']:raise ValueError('Patch hash mismatch')
        source_checks.append(current)
    dependencies=[pin(SOURCE/name) for name in (
        'claude_route_bridge.py','iald_auto_router.py','iald_app_spend.py',
        'iald_activity_operations.py','iald_app_memory.py','iald_wallet_runtime.py',
        'iald_wallet_routes.py','iald_monthly_wallet.py','iald_orcamento.py',
        'iald_app_providers.py','iald_task_bridge.py','iald_chat_jobs.py')]
    science_file=ROOT.parent/'science'/'SCIENCE_STATUS.json'
    science=json.loads(science_file.read_text(encoding='utf-8'))
    science_checks=science['installed_files']['checks']
    mismatches=[]
    for item in science_checks:
        path=Path(item['path'])
        if path.name.lower() in {'.env','iald_stack_v7.py','iald_psion_state.json'}:
            raise ValueError('Unexpected confidential path in scientific receipt')
        if pin(path)['sha256']!=item['expected_sha256']:mismatches.append(item['path'])
    if mismatches:raise ValueError('Scientific baseline changed; parent must reconcile')
    result=json.loads((ROOT/'TEST_RESULT.json').read_text())
    if not result['success']:raise ValueError('Tests not passing')
    artifacts=[pin(path) for path in sorted(ROOT.iterdir()) if path.is_file() and path.name!='MANIFEST.json']
    for artifact in artifacts:
        if Path(artifact['path']).suffix=='.py':ast.parse(Path(artifact['path']).read_text(encoding='utf-8'))
    manifest=dict(status='STAGING_READY_FOR_INDEPENDENT_REVIEW',
        utc=datetime.now(timezone.utc).isoformat(),
        mission_reference=str(ROOT.parent/'SESSION_REFERENCE.json'),requirement='recovery',
        owner='codex-app-01a094df',acom_modified=False,board_modified=False,
        provider_calls=0,runtime_installed=False,server_preamble_copied=False,
        modified_existing_files=2,new_runtime_modules=1,
        coverage='Initial explicit OpenAI refusal in public textual AUTO only',
        known_parent_probe=pin(ROOT.parent/'OPENAI_AUTH_PROBE.json'),
        science_receipt=pin(science_file),science_files_rehashed=len(science_checks),science_mismatches=mismatches,
        runtime_baseline_checks=source_checks,dependencies=dependencies,tests=result,artifacts=artifacts,
        limitations=['No live or full-server middleware/mobile test',
            'No recovery FROM other providers or attachments',
            'Process-local300s circuit; no persisted/cross-process health',
            'Existing observer may report rejected attempt as interrupted',
            'Independent review and installation are parent responsibilities'])
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ('status','science_files_rehashed','science_mismatches','modified_existing_files','new_runtime_modules')}))


if __name__=='__main__':main()
