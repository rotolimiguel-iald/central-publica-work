"""Prepare and apply an additive, independently reviewed availability update."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import support_live as s

MARKER = 'IALD_ACTIVITY_LIVE_AND_IOS33_20261017'

def prepare():
    scope = json.loads((s.ROOT/'MEMORY_SCOPE_R1.json').read_text(encoding='utf-8'))
    text = '''\n\n## 17/10/2026 — Atividade verificada no app e iOS 4.1 (33)
<!-- IALD_ACTIVITY_LIVE_AND_IOS33_20261017 -->
[REAL — em nome de codex-gerente-tgl, F9.MEMORIA_ORGANISMO_20261016, reivindicação940 e escopo941] Retomada após o operador confirmar os dois logins e restabelecer a cota. Duas mensagens sintéticas no app autenticado foram respondidas pelo MiMo. Após recarga, a referência FAROL-73 e o requisito pendente foram recuperados; o aviso final cumpriu os dois requisitos. O painel apresentou duas atividades aguardando revisão, sem aceite automático. Este exemplo verifica o fluxo e a persistência; não isola a contribuição causal da ACOM frente ao histórico normal nem demonstra memória infalível.

[REAL — disponibilidade observada na Apple] Xcode Cloud confirmou build4.1(33) do commit483641a0d875483c04c05437e35ba85d62458c54, contendo os recursos de memória de atividade. Texto de teste salvo, build vinculada aos grupos existentes IALD Equipe(1tester) e IALD Piloto(6testers); ambos mostram Em testes. Participação do operador no Equipe conferida. A Apple ainda informa instalada4.1(32), em15/10; instalação física33 não verificada. Nenhum tester, permissão ou termo novo.

[OPEN — limites preservados] Android4.1(28) permanece APK/AAB local da entrega anterior, sem nova distribuição nesta etapa. Serviço Bancada18777, clientes MCP antigos e inferência real da nativa mantêm os limites do DELIVERY_D_R1. Ciência do app preservada; memória operacional não resolve a ponte física da F1.FECHO. O painel exibe objetivos genéricos/identificadores técnicos, legibilidade a aprimorar. Nenhum kernel, um.py, dado observado ou gate alterado.

Evidências novas, sem sobrescrever a entrega anterior: C:\\IALD\\Central de Patentes\\work\\memoria_organismo_20261016\\live_followup_20261017\\APP_LIVE_RESULT_R1.json e IOS_DISTRIBUTION_RESULT_R1.json. Revisão documental independente: review\\FINAL_REVIEW_R1.json,14checks; não reproduziu as telas. Referência própria: work\\memoria_organismo_20261016\\SESSION_REFERENCE.json. Recibos de backups/apêndices: live_followup_20261017\\MEMORY_APPLIED_R1.json.
<!-- END_IALD_ACTIVITY_LIVE_AND_IOS33_20261017 -->
'''
    appendix=s.new('MEMORY_APPEND_R1.txt',text)
    extra=appendix.read_bytes()
    rows=[]
    for name in scope['surfaces']:
        p=Path(name);raw=p.read_bytes()
        assert MARKER.encode() not in raw
        rows.append({'path':name,'before':s.pin(p),'before_bytes':len(raw),
                     'append':s.pin(appendix),'after_sha256':hashlib.sha256(raw+extra).hexdigest()})
    p=s.new('MEMORY_PLAN_R1.json',{'actor':s.ACTOR,'claim':940,'scope_event':941,'marker':MARKER,
           'surfaces':rows,'applier':s.pin(__file__),'evidence':[s.pin(s.ROOT/n) for n in
           ['APP_LIVE_RESULT_R1.json','IOS_DISTRIBUTION_RESULT_R1.json','review/FINAL_REVIEW_R1.json']]})
    print(p)

def apply():
    plan_path=s.ROOT/'MEMORY_PLAN_R1.json'
    plan=json.loads(plan_path.read_text(encoding='utf-8'))
    review_path=s.ROOT/'review'/'MEMORY_PLAN_REVIEW_R1.json'
    review=json.loads(review_path.read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS')
    assert review['reviewer'] != s.ACTOR['id']
    assert review['plan']==s.pin(plan_path)
    assert review['applier']==s.pin(__file__)
    _,preflight=s.check('L3_MEMORY_FOLLOWUP')
    assert not (s.ROOT/'MEMORY_APPLIED_R1.json').exists()
    originals=[]
    for row in plan['surfaces']:
        p=Path(row['path']);raw=p.read_bytes();extra=Path(row['append']['path']).read_bytes()
        assert s.pin(p)==row['before']
        assert s.pin(row['append']['path'])==row['append']
        assert len(raw)==row['before_bytes'] and MARKER.encode() not in raw
        assert hashlib.sha256(raw+extra).hexdigest()==row['after_sha256']
        originals.append((p,raw,extra,row))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')
    s.new('MEMORY_INTENT_R1.json',{'plan':s.pin(plan_path),'review':s.pin(review_path),'preflight':s.pin(preflight)})
    backups=[]
    for p,raw,extra,row in originals:
        backup=p.with_name(p.name+'.bak_'+stamp)
        with backup.open('xb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        backups.append(backup)
    results=[]
    for i,((p,raw,extra,row),backup) in enumerate(zip(originals,backups)):
        assert p.read_bytes()==raw,'Concurrent modification'
        temp=p.with_name(p.name+'.tmp_'+stamp)
        with temp.open('xb') as f:
            f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert temp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(temp,p)
        assert p.read_bytes()==raw+extra
        result={'before':row['before'],'after':s.pin(p),'backup':s.pin(backup),
                'append':row['append'],'prefix_preserved':True,'growth_bytes':len(extra)}
        s.new(f'memory_surfaces/SURFACE_{i:02d}_R1.json',result);results.append(result)
    print(s.new('MEMORY_APPLIED_R1.json',{'status':'APPLIED_VERIFIED','author':s.ACTOR['id'],
          'time_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'plan':s.pin(plan_path),
          'review':s.pin(review_path),'surfaces':results}))

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('operation',choices=['prepare','apply'])
    globals()[parser.parse_args().operation]()
