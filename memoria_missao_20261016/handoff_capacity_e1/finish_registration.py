"""Resume only registration after a visible duplicate-route refusal."""
import json
from finish import ROOT,PARENT,REF,ACTOR,UNIT,BOARD,command,new,pin,source,project,call

def main():
    failed=json.loads((ROOT/'MAP_RECEIPT_E1.json').read_bytes())
    assert failed['exit_code']==2 and not failed['result']['ok']
    delivery=ROOT/'DELIVERY_E1.json';memories=ROOT/'MEMORY_E1.json'
    for row in json.loads(memories.read_bytes())['surfaces']:
        assert pin(row['surface']['path'])['sha256']==row['surface']['sha256']
    entry=json.loads((ROOT/'MAP_ENTRY_E1.json').read_bytes());entry['tipo']='RESULTADO'
    entry['nota']+=' A tentativa anterior recusou ROTA duplicada sem gravar; este RESULTADO continua a mesma rota.'
    entry_path=new('MAP_ENTRY_E1_RESULTADO.json',entry)
    mapped=command([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry_path,'--quem',ACTOR['id']],'MAP_RECEIPT_E1_RESULTADO')
    command([BOARD,'avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',delivery,memories,
        ROOT/'MAP_RECEIPT_E1_RESULTADO.json',ROOT/'ACCEPT_E1_RECEIPT.json','--nota',
        'Complemento MCP grande instalado e aceito independentemente; sem reiniciar sessões, sem ciência/gate. Quatro memórias com backup.'],'BOARD_DELIVERY_E1')
    p=project('BEFORE_FINAL_FLOW')
    record={'id':'memory-e1-delivered','kind':'fact','statute':'REAL',
        'text':'Memory correction delivered: explicit MCP handoff capacity, real/synthetic large mission verified, independent technical acceptance, additive map/board/memories. Existing science requirements preserved; resume only current residues.',
        'sources':[source(delivery),source(memories),source(ROOT/'MAP_RECEIPT_E1_RESULTADO.json')]}
    call('session_memory.py',{'operation':'transition','reference':str(REF),'actor':ACTOR,
        'expected_revision':p['receipt']['revision'],'event_id':'memory-e1-delivered',
        'changes':{'records':[record],'flow':{'phase':'memory_correction_delivered',
        'next_action':'Project exact mission; continue R4/R5/R7/R8 residues with preflight. R7 R11 handle already running; prefix probe complete. Final R3/R10 await dependencies.'}}},'FINAL_FLOW')
    call('session_memory.py',{'operation':'verify','reference':str(REF)},'FINAL_VERIFY')
    own_ref=PARENT/'ACOM_REFERENCE.json'
    own=call('session_memory.py',{'operation':'project','reference':str(own_ref),'max_chars':100000},'OWN_CURRENT')
    call('session_memory.py',{'operation':'transition','reference':str(own_ref),'actor':ACTOR,
        'expected_revision':own['receipt']['revision'],'event_id':'memory-e1-delivered',
        'changes':{'records':[record],'flow':{'phase':'handoff_correction_delivered',
        'next_action':'Current mission reference carries scientific progress; memory unit awaits programme review.'}}},'OWN_FINAL_FLOW')
    command([BOARD,'liberar',UNIT,'--quem',ACTOR['id'],'--nota','Complemento E1 entregue, memória registrada sob reivindicação904.'],'BOARD_RELEASE_E1')
    new('FINAL_E1.json',{'ok':True,'unit':UNIT,'delivery':pin(delivery),'memory':pin(memories),
        'map':pin(ROOT/'MAP_RECEIPT_E1_RESULTADO.json'),'board':pin(ROOT/'BOARD_DELIVERY_E1.json'),
        'acceptance':pin(ROOT/'ACCEPT_E1_RECEIPT.json'),'claim_released':True,
        'registration_refusal_preserved':pin(ROOT/'MAP_RECEIPT_E1.json')})
    print(json.dumps({'ok':True,'unit':UNIT,'map':mapped,'delivery':str(delivery)},ensure_ascii=False))

if __name__=='__main__':main()
