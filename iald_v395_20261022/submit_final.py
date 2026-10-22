"""Submit final bounded verification and publish operational receipts."""
import hashlib,json,subprocess
import task
W=task.W
def pin(n):
    p=W/n
    return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
assert task.check('verify')['ready']
mem=json.loads((W/'MEMORY_LIVE_APPLIED.json').read_bytes());assert mem['status']=='PASS'
for row in mem['surfaces']:
    from pathlib import Path
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['after']
evidence=[pin(n) for n in ['FINAL_DELIVERY_R1.json','LIVE_VALIDATION_R1.json','MEMORY_LIVE_APPLIED.json','review/MEMORY_LIVE_REVIEW.json']]
p=task.project();t=next(x for x in p['projection']['active'] if x['id']=='verify')
task.new('VERIFY_SUBMIT_FINAL.json',task.act('submit',task_id='verify',lease_id=t['lease']['id'],evidence=evidence,event_id='v395-verify-final-submit'))
entry=json.loads((W/'MAP_PROGRESS.json').read_bytes())
entry.update(tipo='RESULTADO',status='EXAMINADA',titulo='App/JEV v395: teste autenticado e continuidade verificados',resultado='Dois turnos MiMo preservaram FAROL-395, versão e alcance condicional; recarga preservou resposta; 1450 hashes conferidos e dez memórias com adendo final.',veredito='INSTALLED_VERIFIED_LIVE_TEST_PASSED',defeito='Escopo sintético web; sem inspeção física mobile, custos ou benchmark universal.',proximo_passo='Revisão independente final da missão e aceite da gerência no quadro; não repetir testes.',artefatos=[x['path'] for x in evidence])
task.new('MAP_FINAL.json',entry)
for name,args in [('MAP_FINAL_RECEIPT.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(W/'MAP_FINAL.json'),'--quem',task.OWNER]),('BOARD_FINAL_RECEIPT.json',[r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',task.UNIT,'--quem',task.OWNER,'--status','ENTREGUE','--evidencia',str(W/'FINAL_DELIVERY_R1.json'),str(W/'MEMORY_LIVE_APPLIED.json'),'--nota','Teste autenticado concluído em dois turnos; continuidade HajaLuz e recarga verificadas. Backend v395; sem nova build ou inspeção física.'])]:
    p=subprocess.run([task.PY,'-B','-X','utf8',*args],capture_output=True)
    task.new(name,{'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()});assert p.returncode==0
print('SUBMITTED_AND_DELIVERED')
