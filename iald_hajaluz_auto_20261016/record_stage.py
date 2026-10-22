from pathlib import Path
import hashlib,json,subprocess,sys
W=Path(__file__).resolve().parent;PY=r'C:\Python314\python.exe'
def invoke(script,payload):
    p=subprocess.run([PY,'-B','-X','utf8',script],input=json.dumps(payload,ensure_ascii=False).encode(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
    result=json.loads(p.stdout);print(json.dumps({'ok':result['ok'],'result':result.get('result')},ensure_ascii=False));return result
if __name__=='__main__':
    proof=W/'reproduction.json';fixed=W/'reproduction_fixed.json'
    req={'operation':'transition','reference':str(W/'SESSION_REFERENCE.json'),'expected_revision':0,'event_id':'hajaluz-diagnosed-tested-20261016',
         'actor':{'id':'codex-app-01a094df','kind':'agent'},'changes':{
          'records':[{'id':'diagnosis-routing-wire-overflow','kind':'fact','statute':'REAL','text':'Recusa antes do JEV reproduzida com memória da conta do operador: state 32627 e 34955 bytes excede limite30000; 0 chamadas remotas. Correção staged recorta apenas recuperação de candidatos opcionais; três projeções passaram por transporte simulado. 11 regressões e 5 testes de intenção aprovados. Não instalado ainda.','sources':[{'kind':'artifact','ref':str(x),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in (proof,fixed)]}],
          'flow':{'phase':'tested_awaiting_review','next_action':'Revisão independente, instalação em ociosidade e teste pelo chat autenticado.','handles':[{'id':'work','path':str(W)},{'id':'review','agent':'01a14479-5823-76a1-bbdd-da2b5edf6705'}]}}}
    invoke(r'C:\IALD\MEMORIA_IALD\session_memory.py',req)
    route={'tipo':'ROTA','rota_id':'infra.app.hajaluz_auto_20261016','dominio':'INFRA_IALD','titulo':'Continuidade Haja Luz no roteador automático','pergunta':'Por que o segundo comando curto falha apenas em automático?','dados':['Código local e metadados da memória da conta do operador'],'metodo':'Reprodução offline por hash e contexto real; nenhum envio de conversa. Projeção obrigatória íntegra, candidatos opcionais selecionados pelo core existente.','resultado':'State32627/34955bytes acima30000; correção staged validou3contextos e16testes.','veredito':'REPRODUCED_AND_STAGED','estatuto':'REAL','status':'EM_CURSO','olhou_dados':False,'defeito':'Implantação e teste vivo ainda pendentes.','nao_refazer':'Reutilizar diagnóstico e patch desta rota.','proximo_passo':'Revisão independente e implantação controlada.','onde':'iald_auto_router.py; iald_app_memory.py','artefatos':[str(proof),str(fixed),str(W/'validation/test_fix.json')],'refs':[],'nota':'Infraestrutura, sem execução do programa científico ou mudança de gate.'}
    p=W/'route_started.json'
    with p.open('xb') as f:f.write(json.dumps(route,ensure_ascii=False,indent=2).encode())
    proc=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(p),'--quem','codex-app-01a094df'],capture_output=True)
    print(proc.stdout.decode());assert proc.returncode==0,proc.stderr.decode()
