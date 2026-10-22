"""Custody only: reconcile builds already launched; never start or repeat one."""
from datetime import datetime, timezone
from pathlib import Path
import json, subprocess
from activate import ROOT, OUT, REF, ACTOR, call, pin, source, save

def main():
    command="Get-CimInstance Win32_Process | Where-Object { $_.Name -match 'python|lean' -and $_.CommandLine -like '*F1.FECHO_20261015*' } | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Depth 3"
    p=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True,encoding='utf-8')
    if p.returncode:raise RuntimeError(p.stderr)
    live=json.loads(p.stdout) if p.stdout.strip() else []
    if isinstance(live,dict):live=[live]
    processfile=save('EXISTING_BUILD_PROCESSES.json',{'at':datetime.now(timezone.utc).isoformat(),'processes':live})
    handles=[];rows=[]
    for group in ['gns_coefficient_tomita','orbital_rotation']:
        for startpath in sorted((OUT/group/'attempts').glob('20261016T*/START_RECEIPT.json')):
            if startpath.parent.name<'20261016T105000':continue
            start=json.loads(startpath.read_bytes());endpath=startpath.with_name('RECEIPT.json')
            end=json.loads(endpath.read_bytes()) if endpath.exists() else None
            current=next((p for p in live if p['ProcessId']==start['pid'] and str(startpath.parent) in p['CommandLine']),None)
            status=('completed' if end['exit_code']==0 else 'failed') if end else ('running' if current else 'unknown')
            assert pin(start['source']['path'])['sha256']==start['source']['sha256']
            evidence=[pin(startpath),pin(start['source']['path'])]
            if end:
                assert end['source']['sha256']==start['source']['sha256']
                evidence.append(pin(endpath))
            row={'id':'build-'+startpath.parent.name,'type':'lean_build','unit':'F1.FECHO_20261015',
                'name':Path(start['source']['path']).stem,'status':status,'no_repeat':True,
                'receipt':str(endpath) if end else str(startpath),'pid_at_start':start['pid']}
            handles.append(row);rows.append({**row,'evidence':evidence,'exit_code':end['exit_code'] if end else None})
    receipt=save('EXISTING_BUILDS_CUSTODY.json',{'at':datetime.now(timezone.utc).isoformat(),
        'scope':'Recibos iniciados desde 10:50 UTC, antes da prioridade memória, em duas árvores ativas desta missão.',
        'rows':rows,'process_snapshot':pin(processfile),'new_builds_started':0,
        'correction':'RightPolarBridgeR5 e NetGeometryR1 têm recibos exit 0; não reconstruir por resumo antigo. CutoffOrderR10 permanece em execução na consulta. Compilação não é aceite semântico independente.'})
    current=call('mission_cli.py',{'operation':'project','reference':str(REF)},'BEFORE_BUILD_CUSTODY')
    call('session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,
        'expected_revision':current['receipt']['revision'],'event_id':'legacy-build-custody-v1',
        'changes':{'records':[{'id':'legacy-build-custody-v1','kind':'fact','statute':'REAL',
        'text':'Custódia dos builds previamente iniciados. Resultados exit 0/1 e processo ainda ativo foram reconciliados por recibos/pins. Não houve nova compilação. Antes de retomar, ler esta evidência; não reconstruir o que já chegou.',
        'sources':[source(receipt),source(processfile)]}],'flow':{'handles':handles}}},'BUILD_CUSTODY')
    print(json.dumps({'builds':len(rows),'states':{s:sum(r['status']==s for r in rows) for s in {'completed','failed','running','unknown'}}}))

if __name__=='__main__':main()
