"""Custody of observed UI results; no model or scientific execution."""
from pathlib import Path
import hashlib,json,re
import task
W=task.W
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
ui=(W/'LIVE_UI_R1.txt').read_text(encoding='utf-8')
activity=(W/'LIVE_ACTIVITY_FULL_R1.txt').read_text(encoding='utf-8')
assert all(s in ui for s in ['FAROL-395','v395','sem habitante','MiMo V2.6 Pro','Haja Luz'])
assert '2 atividades' in activity and 'Aguardando sua revisão' in activity
plan=json.loads((W/'install_plan.json').read_bytes())
for row in plan['files']:
    assert hashlib.sha256(Path(row['destination']).read_bytes()).hexdigest()==row['sha256']
live={'status':'PASS_WITH_SCOPE','ui_source':pin(W/'LIVE_UI_R1.txt'),'screenshot':pin(W/'LIVE_UI_R1.png'),'activity_source':pin(W/'LIVE_ACTIVITY_FULL_R1.txt'),'automatic_model_observed':'MiMo V2.6 Pro','user_messages':2,'reference':'FAROL-395','version_answer':'v395','conditional_certificate_preserved':True,'first_response_preserved_after_reload':True,'haja_luz_continued_same_reference':True,'activities_awaiting_review':2,'activities_accepted':0,'installed_files_rechecked':len(plan['files']),'limitations':['Two synthetic UI conversations turns only; no universal accuracy or isolated causal memory benchmark.','No physical mobile inspection, new store distribution or scientific proof.','Token usage and cost were not measured in this receipt.','Version reply alone is not evidence of deployment; separately bound installed hashes were checked.']}
task.new('LIVE_VALIDATION_R1.json',live)
previous=json.loads((W/'DELIVERY.json').read_bytes())
task.new('FINAL_DELIVERY_R1.json',{'status':'INSTALLED_VERIFIED_LIVE_TEST_PASSED','release':'v395','previous_delivery':pin(W/'DELIVERY.json'),'live':pin(W/'LIVE_VALIDATION_R1.json'),'installed_files':len(plan['files']),'matrix':previous.get('matrix',previous.get('availability')),'new_mobile_build':False,'physical_installation_verified':False,'deployment_review':pin(W/'review/DEPLOY_REVIEW_R1.json'),'memory_previous':pin(W/'MEMORY_APPLIED.json'),'scope':'Backend science update; no runtime code or scientific source changes. Independent final acceptance follows.'})
old=json.loads((W/'MEMORY_PLAN.json').read_bytes())
marker='IALD_APP_V395_LIVE_20261022'
text=f'''\n\n## 22/10/2026 — Verificação autenticada da v395
<!-- {marker} -->
[REAL — codex-gerente-tgl, F9.APP_V395_20261022] Após entrada do operador, dois turnos sintéticos no modo automático receberam respostas MiMo V2.6 Pro. O primeiro identificou v395 e conservou o certificado Psion como condicional, sem habitante; a resposta persistiu após recarga. “Haja Luz” retomou FAROL-395 e o mesmo limite. O painel mostrou duas atividades aguardando revisão, sem aceite automático. Os 1450 arquivos instalados foram novamente conferidos por hash.
[ESCOPO] Resolve a pendência de login/teste do adendo anterior. Teste observado na web, não benchmark de acurácia universal nem isolamento causal da memória. Backend comum web/iOS/Android; sem mudança de cliente, nova build ou inspeção física. Custos/tokens destes turnos não medidos neste recibo. Nenhuma execução de um.py/Lean, nova prova ou mudança de gate.
[EVIDÊNCIAS] {W}/LIVE_VALIDATION_R1.json, FINAL_DELIVERY_R1.json, LIVE_UI_R1.txt, LIVE_UI_R1.png e LIVE_ACTIVITY_FULL_R1.txt. Referência própria {task.REF}; revisões e aceites posteriores em recibos separados.
<!-- END_{marker} -->
'''
rows=[]
for r in old['surfaces']:
    p=Path(r['path']);b=p.read_bytes();assert marker.encode() not in b
    rows.append({'path':str(p),'baseline_sha256':hashlib.sha256(b).hexdigest(),'baseline_bytes':len(b),'append_utf8':text.replace('\n','\r\n' if b'\r\n' in b else '\n')})
task.new('MEMORY_LIVE_PLAN.json',{'marker':marker,'surfaces':rows,'delivery_sha256':hashlib.sha256((W/'FINAL_DELIVERY_R1.json').read_bytes()).hexdigest()})
print('LIVE_AND_MEMORY_PLAN_READY')
