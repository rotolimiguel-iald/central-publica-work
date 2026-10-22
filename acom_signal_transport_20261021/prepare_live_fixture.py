"""Synthetic public text only, no personal/scientific content."""
import hashlib,json
from task import W,new
p=W/'transport_fixture.txt'
raw=('ARQUIVO SINTETICO PARA TESTE DE TRANSPORTE SEM PERDAS.\n'
     'Nao contem dados pessoais nem resultado cientifico.\n'+
     'Esta linha repetida serve apenas para testar a compactacao e a leitura integral.\n'*500+
     'MARCADOR_FINAL=TRANSPORTE_INTEGRO_73\n').encode('utf-8')
with p.open('xb') as f:f.write(raw)
new('LIVE_FIXTURE.json',{'file':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'synthetic':True,'private_content':False,'expected':'TRANSPORTE_INTEGRO_73','prompt':'Teste técnico com arquivo sintético. Leia o marcador final do arquivo e responda somente com seu valor, sem explicações.'})
print(json.dumps({'bytes':len(raw),'synthetic':True}))
