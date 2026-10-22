from task import *
p=project()
assert p['projection']['tetelestai'] and not p['projection']['unresolved_handles'], 'Final independent review pending'
new('MISSION_FINAL_PROJECTION.json',p)
r=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',OWNER,'--status','ENTREGUE','--evidencia',str(W/'delivery.json'),str(W/'MISSION_FINAL_PROJECTION.json')],capture_output=True)
new('BOARD_DELIVERED.json',{'returncode':r.returncode,'stdout':r.stdout.decode('utf8'),'stderr':r.stderr.decode('utf8')})
assert r.returncode==0,r.stderr
p=project();source=W/'delivery.json'
result=call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'event_id':'kimi-stack-final-material-record','changes':{'records':[{'id':'kimi-stack-delivered','kind':'fact','statute':'REAL','text':'Cinco arquivos do stack instalados e conferidos; recuperação local em processo novo validada. Corrigido orçamento de memória obrigatória+reserva e promovido ranking por relevância com blocos inteiros. Cinco arquivos científicos do app intactos. Benchmark de600candidatos sintéticos teve mediana1,239642s para0,033598s, mesma ordem; não é ganho de qualidade ou latência do modelo. Voz e corrida de modelos não ativadas; MCPs antigos não reiniciados. Três memórias operacionais com backup e retorno Kimi no mapa seq1308. Nenhum job ou chamada remota repetido.','sources':[{'kind':'artifact','ref':str(source),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}],'flow':{'phase':'delivered','next_action':'Usar CLI absoluto atualizado; preservar limites do benchmark e não repetir pedidos históricos cobertos pela entrega.','handles':[]}}},False)
new('FINAL_MEMORY_RECEIPT.json',result)
print('DELIVERED_AND_RECORDED')
