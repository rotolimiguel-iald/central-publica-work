"""Record scoped engineering result after actual distinct reviewer acceptance."""
import hashlib,json,subprocess
import task
p=task.project()
assert not p['projection']['active'], 'Independent acceptance pending'
assert not p['projection']['unresolved_handles']
task.new('MISSION_FINAL_PROJECTION.json',p)
route={'tipo':'RESULTADO','rota_id':'infra.app.acom_signal_transport_20261021','dominio':'INFRA','titulo':'Transporte sem perdas implantado; controle luminidico experimental','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'dados':['Fixtures sintéticos e observações operacionais; nenhum dado experimental de natureza'],'metodo':'Controle de preditor/residuo, interoperabilidade, revisão distinta, integração autenticada e verificação de distribuição','resultado':'Transporte deflate negociado instalado; anexo sintético respondido e recuperado após recarga. iOS37 ambos grupos Em testes; APK32 download autenticado com hash. Memória científica preservada.','veredito':'ENGINEERING_DELIVERED_WITH_SCOPE','defeito':'Controle luminidico continua isolado; sem ganho de latência de rede ou economia de tokens demonstrados. Instalação física e Google Play não verificados/publicados.','nao_refazer':'Não repetir jobs encerrados, compilações ou envios; recibos e fontes preservados.','proximo_passo':'Uso normal da build37 e APK32; novos benchmarks apenas com hipótese e controles delimitados.','artefatos':[str(task.W/n) for n in ['delivery.json','live_validation.json','availability.json','MISSION_FINAL_PROJECTION.json','MEMORY_APPLIED_FINAL.json']]}
task.new('ROUTE_FINAL.json',route)
for name,args in [('ROUTE_REGISTERED_FINAL.json',[task.PY,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(task.W/'ROUTE_FINAL.json'),'--quem',task.OWNER]),('BOARD_DELIVERED_FINAL.json',[task.PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',task.UNIT,'--quem',task.OWNER,'--status','ENTREGUE','--evidencia',str(task.W/'delivery.json'),str(task.W/'MISSION_FINAL_PROJECTION.json')])]:
    r=subprocess.run(args,capture_output=True)
    task.new(name,{'returncode':r.returncode,'stdout':r.stdout.decode('utf8'),'stderr':r.stderr.decode('utf8')})
    if r.returncode:raise RuntimeError(name)
p=task.project();source=task.W/'delivery.json'
result=task.call({'operation':'transition','reference':str(task.REF),'actor':{'id':task.OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'event_id':'transport-final-material-record','changes':{'records':[{'id':'transport-final-material','kind':'fact','statute':'REAL','text':'Transporte sem perdas implantado e testado; falha inicial de admissao corrigida e preservada. Ciencia intacta. iOS37 em ambos grupos e APK32 conferidos. Oito memorias atualizadas com backup; painel de prazos somente administrativo. Controle luminidico experimental e limitacoes preservados nos recibos.','sources':[{'kind':'artifact','ref':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}],'flow':{'phase':'delivered','next_action':'Atualizacao fisica pelo operador; nenhum envio ou job a repetir.','handles':p['projection']['flow']['handles']+p['projection'].get('terminal_handles',[])}}},False)
task.new('FINAL_MEMORY_RECEIPT.json',result)
print('DELIVERED_AND_RECORDED')
