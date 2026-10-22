from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,os,subprocess
W=Path(__file__).resolve().parent;OLD=W.parent/'mimo_media_capacity_20261020'
sha=lambda b:hashlib.sha256(b).hexdigest()
def new(n,d):
    b=json.dumps(d,ensure_ascii=False,indent=2).encode();(W/n).open('xb').write(b)
d=json.loads((W/'AUTO_AUDIO_EXTRA_RESULT.json').read_bytes())
assert d['job']['status']=='completed' and d['known_cost_estimate_usd']<0.50
assert d['routing'][0]['selected']=='mimo' and d['provider_real']=='mimo'
report=dict(status='ROUTING_PASS_PERCEPTION_FAILURE',job=d['job']['id'],model=d['model_real'],seconds=d['duration_seconds'],cost_estimate_usd=d['known_cost_estimate_usd'],max_cost_usd=0.50,response=d['text'],science_sha256=d['metric_memory_sha256'],scope='One new synthetic120s audio message. No video retry. No new runtime changes or builds. UI showed local record changed, response recovered by reload without resend. Cause of audio perception failure not isolated.',source=str(W/'AUTO_AUDIO_EXTRA_RESULT.json'),source_sha256=sha((W/'AUTO_AUDIO_EXTRA_RESULT.json').read_bytes()))
new('delivery.json',report)
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
marker='IALD_MIMO_EXTRA_AUDIO_20261021'
text=('\n\n## 21/10/2026 — Teste adicional automático de áudio\n<!-- '+marker+' -->\n'
'[INPUT/REAL] Operador autorizou prosseguir com o teste adicional atéUS$0,50; corrige ao lado a pendência anterior. Uma nova mensagem sintética120s, job '+d['job']['id']+', JEV selecionou MiMoV2.6Pro. Concluiu em59,615s,283338tokens de entrada/422saída; custo estimado MiMo+JEV US$0,12441885, não fatura. Memória científica manteve o hash conferido no recibo.\n'
'[REAL/OPEN] Transporte/custódia concluídos, mas percepção falhou: modelo declarou não conseguir analisar o áudio. Não comprova ausência de sinal no request nem causa isolada. Interface apresentou registro local alterado; resposta recuperada após recarga sem reenvio. Nenhum retry do vídeo incerto, nova build ou alteração de runtime/ciência/kernel/gate.\n'
'[EVIDÊNCIA] '+str(W/'delivery.json')+'; AUTO_AUDIO_EXTRA_RESULT.json; RESULT_RECOVERED.jpg. Referência própria SESSION_REFERENCE.json.\n<!-- END_'+marker+' -->\n').encode('utf-8')
plans=json.loads((OLD/'memory_stage/FINAL_R4/PLAN.json').read_bytes())['surfaces'];receipts=[]
for item in plans:
    p=Path(item['path']);before=p.read_bytes();assert marker.encode() not in before
    backup=p.with_name(p.name+'.bak_'+stamp);backup.open('xb').write(before);assert backup.read_bytes()==before
    after=before+text;tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.open('xb').write(after);assert tmp.read_bytes()==after
    assert p.read_bytes()==before;os.replace(tmp,p);assert p.read_bytes()==after
    receipts.append(dict(path=str(p),backup=str(backup),before_sha256=sha(before),after_sha256=sha(after)))
new('MEMORY_APPLIED.json',dict(status='APPLIED_8_ADDITIVE',surfaces=receipts))
def call(q):
    r=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\session_memory.py'],input=json.dumps(q).encode(),capture_output=True)
    z=json.loads(r.stdout);assert z['ok'],z;return z['result']
ref=str(W/'SESSION_REFERENCE.json');c=call(dict(operation='get',reference=ref))
sources=[dict(kind='artifact',ref=str(W/n),sha256=sha((W/n).read_bytes())) for n in ['delivery.json','AUTO_AUDIO_EXTRA_RESULT.json','MEMORY_APPLIED.json']]
r=call(dict(operation='transition',reference=ref,actor=dict(id='codex-app-01a094df',kind='agent'),expected_revision=c['receipt']['revision'],event_id='extra-audio-test-terminal-r1',changes=dict(records=[dict(id='extra-audio-test-result-r1',kind='fact',statute='REAL',sources=sources,text='Teste único automático concluído; JEV selecionou MiMo, custo estimado0.12441885USD<0.50USD. Percepção do áudio falhou. Resposta recuperada por recarga sem reenvio; nenhuma repetição do vídeo incerto.')],flow=dict(phase='test_complete_with_negative_result',next_action='Diagnóstico adicional exige nova unidade; não repetir este job.',handles=[dict(id='auto-audio-extra',provider='IALD_APP',external_id=d['job']['id'],status='completed')]))))
new('FINAL_MEMORY_RECEIPT.json',r)
print(json.dumps(report,ensure_ascii=False))
