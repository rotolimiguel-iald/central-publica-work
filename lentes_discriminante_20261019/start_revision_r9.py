"""Record operator-authorized candidate revision, without changing scientific originals."""
from setup import ROOT, UNIT, ACTOR, command, memory
from record_trajectory_r2 import pin
import json, sys, datetime

if __name__ == '__main__':
    folder=ROOT/'candidate_r9'; folder.mkdir(exist_ok=True)
    source=folder/'OPERADOR_VERBATIM.txt'
    text='já escrevi sim algumas coisas, mas o programa avançou e nada impede que revisitemos e adequamos o que for necessário diante da evolução do próprio programa'
    with source.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    board=json.loads(command('BOARD_PREFLIGHT_R9',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    c=board['reivindicacao'];assert c['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(c['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json')
    state=memory({'operation':'get','reference':ref},'GET_BEFORE_START_R9');assert state['revision']==9
    evidence=pin(source)
    command('BOARD_SCOPE_R9',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','anotar','--quem',ACTOR['id'],'--tipo','REVISAO_CANDIDATA_AUTORIZADA','--unidade',UNIT,'--dados',json.dumps({'fonte':evidence,'escopo':'Revisitar/adequar modelo em sandbox; derivar fonte e resposta espacial a partir de acao explicitada, marcar hipoteses novas. Sem promover candidato ao canone, sem ajustar ao atraso, sem dado observado ou gate.'},ensure_ascii=False)])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':9,'event_id':'lensing-candidate-r9-operator-resume','changes':{
      'records':[{'id':'operator-candidate-r9','kind':'decision','statute':'INPUT','sources':[{'kind':'artifact','ref':evidence['path'],'sha256':evidence['sha256']}],'text':text+' — Escopo: revisao candidata local com hipoteses explicitadas e verificacao; preservar originais. Nao fixar parametros pelo sinal5sigma desejado.'}],
      'flow':{'phase':'candidate_scalar_source_r9','next_action':'Derive sourced scalar/metric response from explicit action family, check current-program parameter links and mass-distance identifiability; candidate not canonicalTGL yet.','handles':[{'id':'r69_current_source_r9','status':'running','kind':'subagent','agent':'/root/r69_locality_bridge','scope':'current scalar background and potential source lookup'}]}}},'START_R9')
    print(json.dumps(out,ensure_ascii=False))
