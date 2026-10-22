from pathlib import Path
from datetime import datetime
import json,hashlib,os
import task
W=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
installed=json.loads((W/'installed_verification_R4.json').read_bytes())
live=json.loads((W/'live_validation.json').read_bytes())
review=json.loads((W/'validation/review_final.json').read_bytes())
review_r4=json.loads((W/'patch_R4/validation/review_final.json').read_bytes())
assert installed['status']==live['status']==review['status']=='PASS'
assert review_r4['status']=='PASS'
task.project();task.check('deploy')
marker='IALD_JEV_KIMI_REPAIR_20261020'
text=f'''

## 20/10/2026 — Correção de continuidade e integração JEV/Kimi
<!-- {marker} -->
[REAL — engenharia local] Pedido próprio em {task.REF}. Falha reproduzida em cópia: resultado recebido pelo MiMo e custodiado, mas projeção interna excedeu2milhões de caracteres; erro secundário mascarou o overflow. Comando seguinte também recusado. Correção dimensiona a projeção com teto explícito de33.554.432caracteres (limites de bytes separados), sem truncar estado obrigatório nem alterar admissão final dos provedores. Reconhece custódia retornada antes de marcar incerteza, verificando identidade/pino. Jobs com aviso de falha deixam de aparecer como geração concluída. Pedidos antigos preservados, sem reenvio.

[REAL — memória eficiente] Novos fluxos técnicos HTTP/SSE são guardados integralmente em artefatos imutáveis de escopo, com SHA256/tamanho/representação conferidos; q recebe referência compacta. Não se apaga o legado, nem o conteúdo semântico das respostas, decisões ou núcleo científico. Fluxo sem terminador permanece incerto; referência adulterada ou de outro escopo recusa. Não altera pesos ou KV-cache.

[REAL — Kimi/JEV] Contrato v2 anterior preservado; derivado ligado aos bytes reais do pacote Kimi e comparado com fonte canônica verificada. Parada por grafo/limite inclui razão, sequência e hash do estado final. Projeção opcional de consulta tem proveniência e ponteiro ao estado completo; obrigatório não é comprimido semanticamente. A métrica estrutural não vira peso físico nem aprendizado de qualidade. Calibração F9.9.A01/sombra não foi ativada por inferência.

[REAL — instalação e teste] Dez arquivos efetivos instalados por hash; um ajuste posterior no fechamento do transporte foi revisado e instalado separadamente após o teste real. Backups imediatos, janela ociosa e reinício somente do filho web sob o supervisor existente. Ciência/kernel v394, contas, consentimentos, carteira e política de modelos preservados. Testes locais e revisão independente; teste autenticado de consulta às fontes e continuidade HajaLuz em live_validation.json. Não houve retry de pedidos anteriores. Evidências: {W}\delivery.json, validation\review_final.json, deployment.json, restart.json, patch_R4/deployment.json, installed_verification_R4.json e live_validation.json.

[DISPONIBILIDADE] Backend comum web/iOS/Android atualizado, sem alteração de recursos do cliente: nenhuma nova build ou distribuição em loja necessária nesta entrega. Teste efetivo pela web; instalação física e teste no iPhone/iPad/Android não verificados. Grupos de lojas não reinspecionados. Sessões/MCPs antigos de outras missões não reiniciados; CLI novo lê biblioteca atual.
<!-- END_{marker} -->
'''
old=json.loads(Path(r'C:\IALD\Central de Patentes\work\iald_v394_20261019\MEMORY_DELIVERY.json').read_bytes())
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
for item in old['surfaces']:
 p=Path(item['path']);before=p.read_bytes()
 if marker.encode() in before:raise RuntimeError('Existing memory marker: inspect before repeating')
 backup=p.with_name(p.name+'.bak_'+stamp)
 with backup.open('xb') as out:out.write(before);out.flush();os.fsync(out.fileno())
 assert backup.read_bytes()==before
 after=before+text.encode('utf-8');temp=p.with_name(p.name+'.tmp_'+stamp)
 with temp.open('xb') as out:out.write(after);out.flush();os.fsync(out.fileno())
 assert temp.read_bytes()==after and p.read_bytes()==before
 os.replace(temp,p);assert p.read_bytes()==after and len(after)>len(before)
 rows.append({'path':str(p),'backup':str(backup),'sha256':sha(p)})
task.new('MEMORY_DELIVERY.json',{'status':'PASS','marker':marker,'surfaces':rows})
matrix={key:{'shared_backend_updated':True,'client_resources_changed':False,'new_binary_required':False,'physical_device_tested':False,'store_distribution_reinspected':False} for key in ('web','ios_internal','ios_external','android')}
matrix['web']['authenticated_chat_tested']=True
task.new('delivery.json',{'status':'PASS','reference':str(task.REF),'files':10,'science_release':installed['release'],'matrix':matrix,'old_jobs_preserved':True,'old_jobs_retried':False,'scientific_execution':False,'scientific_gate_changed':False,'memory_surfaces':len(rows),'live_test':live,'evidence':[{'path':str(W/n),'sha256':sha(W/n)} for n in ('deployment.json','restart.json','installed_verification_R4.json','patch_R4/deployment.json','patch_R4/restart.json','patch_R4/validation/review_final.json','live_validation.json','validation/review_final.json','MEMORY_DELIVERY.json')]})
print(json.dumps({'status':'PASS','memory_surfaces':len(rows),'matrix':matrix},ensure_ascii=False))
