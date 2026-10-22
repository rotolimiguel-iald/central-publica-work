"""Bind scientific staging and control without changing any running service."""
from pathlib import Path
import copy
import json
import sys

W=Path(__file__).resolve().parent
S=W/'memory_stage'
R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'app_patch'),str(R),str(W)]
from transaction import digest,write_evidence,atomic
import iald_jev_control as control

def main():
    raw=(W/'controller/jev_control_v380.json').read_bytes()
    contract=control.validate_contract(json.loads(raw))
    manifest=json.loads((S/'manifest_staged.json').read_bytes())
    if (contract['source_sha256']!=manifest['operational_core']['release_source_sha256']
        or contract['release']!=manifest['operational_core']['current_release']):
        raise ValueError('Scientific and executive releases differ')
    manifest['jev_control']={'path':str(W/'controller/jev_control_v380.json'),'sha256':digest(raw),
                             'release':contract['release'],'source_sha256':contract['source_sha256']}
    write_evidence(W/'iald_nucleo_fixo.json',manifest)
    loaded=control.load_contract(W)
    if loaded!=contract:raise ValueError('Control verification mismatch')
    print(json.dumps({'staged_runtime':'READY','release':contract['release'],'contract_sha256':digest(raw)}))

if __name__=='__main__':main()
