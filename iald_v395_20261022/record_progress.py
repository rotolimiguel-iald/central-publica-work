"""Record installed progress without closing the authenticated verification."""
import hashlib,json,subprocess
import task
W=task.W
def run(name,args):
    p=subprocess.run([task.PY,'-B','-X','utf8',*args],capture_output=True)
    task.new(name,{'exit_code':p.returncode,'stdout':p.stdout.decode('utf-8'),'stderr':p.stderr.decode('utf-8')})
    assert p.returncode==0
assert task.check('verify')['ready']
artifacts=[W/x for x in ['DELIVERY.json','MEMORY_APPLIED.json','review/DEPLOY_REVIEW_R1.json','review/MEMORY_REVIEW.json','VERIFICATION_FIRST_ATTEMPT.json','INSTALLED_VERIFICATION.json']]
task.new('MAP_PROGRESS.json',{'tipo':'ROTA','rota_id':'infra.app.v395_20261022','dominio':'INFRA_IALD','titulo':'App e JEV v395 instalados; teste autenticado pendente','pergunta':'Sincronizar o stack com o um.py selado v395','metodo':'Hashes, revisão independente, pacotes derivados, troca controlada e carregamento em processo novo.','resultado':'1450 arquivos conferidos; 425 tópicos; 1424 fontes formais. Dez memórias acrescentadas com backup. Fila e Bancada v395 reaproveitadas.','veredito':'INSTALLED_VERIFIED_AUTHENTICATED_TEST_PENDING','estatuto':'REAL','status':'EM_CURSO','olhou_dados':False,'defeito':'Login expirado impede teste de conversa autenticada; sem alegar teste físico ou recarga de sessões antigas.','nao_refazer':'Não repetir implantação, contagem ou ativação da fila já verificados.','proximo_passo':'Após login humano, verificar conversa e continuidade HajaLuz; preservar IDs de execução.','onde':str(W),'artefatos':[str(p) for p in artifacts],'refs':['custodia.v395']})
run('MAP_PROGRESS_RECEIPT.json',[r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(W/'MAP_PROGRESS.json'),'--quem',task.OWNER])
run('BOARD_PROGRESS_RECEIPT.json',[r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',task.UNIT,'--quem',task.OWNER,'--status','AGUARDA_OPERADOR','--evidencia',str(W/'DELIVERY.json'),str(W/'MEMORY_APPLIED.json'),'--nota','Instalação v395 e revisão concluídas. Aguarda somente login no app para teste autenticado; nenhuma aprovação científica presumida.'])
p=task.call({'operation':'project','reference':str(task.REF),'max_chars':100000},False)
result=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'event_id':'v395-installed-memory-progress','changes':{'records':[{'id':'v395-installed-memory-progress','kind':'fact','statute':'REAL','text':'App/JEV v395 instalados e revisados; dez memórias atualizadas com backups. Fila/Bancada v395 conferidas. Teste autenticado pendente de login; verify permanece aberto.','sources':[{'kind':'artifact','ref':str(a),'sha256':hashlib.sha256(a.read_bytes()).hexdigest()} for a in artifacts]}],'flow':{'phase':'awaiting_authenticated_login','next_action':'Após login humano no app, realizar teste de conversa e continuidade HajaLuz; não repetir instalação.'}}},False)
task.new('ACOM_PROGRESS_RECEIPT.json',result)
print(json.dumps({'status':'RECORDED','revision':result['receipt']['revision']}))
