"""Register delivery as pending management audit; never self-accept the mission."""
from task import *
import zipfile
OUT=Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025')
result=OUT/'RESULTADO.json'
manifest=json.loads(result.read_text())
for item in manifest['files']:
    assert pin(Path(item['path']))['sha256']==item['sha256']
assert check()['ready']
bundle=W/'ENTREGA_ORDEM025.zip'
with zipfile.ZipFile(bundle,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(OUT))
with zipfile.ZipFile(bundle) as z:
    assert z.testzip() is None
new('BUNDLE_RECEIPT.json',{'archive':pin(bundle),'files':len(manifest['files'])+1})
def board(args,name):
    p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True)
    if p.returncode:raise RuntimeError(p.stdout.decode('utf-8')+p.stderr.decode('utf-8'))
    r=json.loads(p.stdout)
    assert r['ok']
    new(name,r)
    return r
delivered=board(['avancar',UNIT,'--quem',OWNER,'--status','ENTREGUE','--evidencia',str(result),str(bundle),
    '--nota','ORDEM025 PONTE PARCIAL: build EXIT0/trio, 40 declaracoes, lift concreto com massa livre; revisao semantica distinta PASS_WITH_SCOPE. Integracao e mapa pela gerencia.'], 'BOARD_DELIVERED.json')
proj=project()
lease=next(t for t in proj['projection']['active'] if t['id']=='bridge')['lease']['id']
new('MISSION_SUBMITTED.json',act('submit',task_id='bridge',lease_id=lease,
    evidence=[pin(result),pin(W/'REVIEW_SEMANTIC.json'),pin(bundle)],event_id='o25-delivery-submit'))
board(['liberar',UNIT,'--quem',OWNER,'--nota','Entrega concluida; livre para exame e eventual fecho da gerencia.'], 'BOARD_RELEASED.json')
p=call({'operation':'project','reference':str(REF),'max_chars':100000},False)
sources=[{'kind':'artifact','ref':str(result),'sha256':pin(result)['sha256']},
         {'kind':'artifact','ref':str(W/'BOARD_DELIVERED.json'),'sha256':pin(W/'BOARD_DELIVERED.json')['sha256']}]
new('MEMORY_DELIVERY.json',call({'operation':'transition','reference':str(REF),
    'actor':{'id':OWNER,'kind':'agent'},'expected_revision':p['receipt']['revision'],'event_id':'o25-delivery-material-record',
    'changes':{'records':[{'id':'o25-local-build-and-delivery','kind':'fact','statute':'REAL',
        'text':'ORDEM025 entregue: build local EXIT0, 40 declaracoes explicitas/29 teoremas e 65 entradas de axiomas no trio; zero sorry. Revisao semantica distinta PASS_WITH_SCOPE. Classificacao da entrega PONTE PARCIAL: lift equivarante nao canonico, massa livre, calibracao fisica/H3/assinatura/rank4 abertos. ArquivoZIP custodiado no quadro; fontes pinadas preservadas. O aceite da gerencia e a integracao nao ocorreram.',
        'sources':sources}],
        'flow':{'phase':'awaiting_management_audit','next_action':'Gerencia confere ORDEM025, registra mapa preparado e decide integracao. Nao repetir builds concluidos nem alterar fontes pinadas.'}}},False))
new('MEMORY_VERIFY.json',call({'operation':'verify','reference':str(REF)},False))
q=project()
new('FINAL_STATE.json',{'board_event':delivered['evento'],'mission_revision':q['receipt']['revision'],
    'active':q['projection']['active'],'settled':q['projection']['settled'],'flow':q['projection']['flow'],
    'result':pin(result),'bundle':pin(bundle),'review':pin(W/'REVIEW_SEMANTIC.json')})
print(json.dumps({'board':delivered,'mission_revision':q['receipt']['revision'],'mission_status':q['projection']['active'][0]['status']},ensure_ascii=False))
