"""Regenerate the existing Tower contract, with byte backups for replaced views."""
from pathlib import Path
import contextlib
import hashlib
import importlib.util
import io
import json

from transaction import WORK, backup

def main():
    installed=json.loads((WORK/'INSTALLED_VERIFICATION.json').read_bytes())['identity']
    release=installed['release']
    q=WORK.parent/'scientific_memory_sync_20261105_v408/DELIVERY_TECHNICAL_R1.json'
    assert json.loads(q.read_bytes())['release']==release
    root=Path(r'C:\IALD\TORRE_IALD')
    module_spec=importlib.util.spec_from_file_location('verified_tower',root/'torre.py')
    tower=importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(tower)
    writer=tower.escreve
    backups=[]
    def with_backup(path,data,backup_requested=False,**kwargs):
        if Path(path).is_file():
            backups.append(backup(path))
        return writer(path,data,backup=False)
    tower.escreve=with_backup
    # Capture diagnostics locally. Only counts and scientific/JEV pins enter this receipt.
    with contextlib.redirect_stdout(io.StringIO()):
        code=tower.cmd_gerar()
    contract=root/('TORRE_'+release+'.json')
    d=json.loads(contract.read_bytes())
    jev=d['jev']['contrato']
    measured=json.loads((root/'MEDIDA_ULTIMA.json').read_bytes())
    result={'tower_status':code,'jev_current':jev['release']==release and jev['source_sha256']==installed['source_sha256'],
            'release':release,'contract_sha256':hashlib.sha256(contract.read_bytes()).hexdigest(),
            'summary':measured['resumo'],'prior_byte_backups':len(backups),
            'outstanding':[(r['superficie'],r['item'],r['estado']) for r in measured['itens']
                           if r['estado'] in ('PENDENTE_OPERADOR','FALHA','DEFASADO')]}
    assert result['jev_current']
    with (WORK/'TORRE_RESULT.json').open('x',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(release,result['summary'],'JEV',result['jev_current'])

if __name__=='__main__':
    main()
