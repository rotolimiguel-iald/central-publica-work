"""Register the authorized source reconciliation; do not accept any requirement."""
import json, hashlib, os, subprocess, sys, uuid
from pathlib import Path

ROOT = Path(r'C:\IALD\Central de Patentes')
OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/documentary_reconciliation_R55'
REF = ROOT/'work/memoria_missao_20261016/FECHO_MISSION_REFERENCE.json'
CORE = Path(r'C:\IALD\MEMORIA_IALD')
ACTOR = {'id':'codex-gerente-tgl','kind':'agent'}

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw=(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode('utf-8')
    tmp=path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
    if tmp.read_bytes()!=raw: raise RuntimeError('Byte verification failed')
    os.rename(tmp,path)

def pin(path):
    return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def call(op, label, **kw):
    req={'operation':op,'reference':str(REF),**kw}
    save(OUT/(label+'_REQUEST.json'),req)
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(CORE/'mission_cli.py')],
        input=json.dumps(req,ensure_ascii=False),text=True,encoding='utf-8',capture_output=True)
    value=json.loads(r.stdout); save(OUT/(label+'_RECEIPT.json'),value)
    if r.returncode or not value.get('ok'): raise RuntimeError(str(value))
    return value['result']

def main():
    if OUT.exists(): raise RuntimeError('Recover existing reconciliation, do not repeat')
    source=OUT/'AUTORIZACAO_CONTEXTO.json'
    save(source, {'user_verbatim':'Prossiga',
        'preceding_user_question_verbatim':'Que ponte é essa q vc se refere?',
        'scope':'Conferir a indicacao do dispositivo e fontes existentes antes de exigir escolha humana. Nao aceitar requisitos por este registro.',
        'parent_unit':'F1.FECHO_20261015','board_claim_event':931})
    p=call('project','START',max_chars=150000)
    call('extend','EXTEND',actor=ACTOR,expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256'],event_id='r55-documentary-reconciliation-extend',
        reason='Pedido humano de prosseguir na conferencia documental antes de pedir escolha de dispositivo.',
        requirements=[{'id':'R11_SOURCE_RECONCILIATION',
            'criterion':'Conferir fontes da rede/dispositivo/relogio e distinguir complementaridade documental de realizacao matematica; corrigir ao lado a exigencia prematura de escolha exclusiva sem declarar R4/R5 satisfeitos. Relatorio novo com fontes e hashes.',
            'depends_on':[]}],sources=[pin(source)])
    p=call('project','BEFORE_CLAIM',max_chars=150000)
    c=call('claim','CLAIM',actor=ACTOR,expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256'],event_id='r55-documentary-reconciliation-claim',
        task_id='R11_SOURCE_RECONCILIATION',lease_seconds=14400)
    p=call('project','CURRENT',max_chars=150000)
    t=next(x for x in p['projection']['active'] if x['id']=='R11_SOURCE_RECONCILIATION')
    call('check','PREFLIGHT',actor=ACTOR,expected_revision=p['receipt']['revision'],
        projection_sha256=p['projection_sha256'],task_id=t['id'],lease_id=t['lease']['id'])
    print(json.dumps({'revision':p['receipt']['revision'],'reference':str(REF),'output':str(OUT)},ensure_ascii=False))

if __name__=='__main__': main()
