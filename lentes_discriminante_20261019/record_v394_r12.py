"""Register the bounded v394 inspection with byte backups and new evidence names."""
from setup import ROOT,UNIT,ACTOR,save,command,memory
from record_trajectory_r2 import pin
from pathlib import Path
import json,datetime,sys,os

if __name__=='__main__':
    folder=ROOT/'v394_r12'
    for name in ['DELIVERY_R12.json','MEMORY_APPLIED_R12.json','MAP_ENTRY_R12.json','REGISTRATION_R12.json']:
        if (ROOT/name).exists():raise FileExistsError(name)
    review=json.loads((folder/'REVIEW_R12.json').read_text(encoding='utf-8'))
    assert str(review.get('status','')).startswith('PASS'),review
    for item in review['evidence']:
        assert pin(item['path'])['sha256']==item['sha256'],item['path']
    supplement=json.loads((folder/'REVIEW_RELEASE_SUPPLEMENT_R12.json').read_text(encoding='utf-8'))
    assert supplement['status']=='PASS_WITH_SCOPE'
    for item in supplement['evidence']:
        assert pin(item['path'])['sha256']==item['sha256'],item['path']
    board=json.loads(command('BOARD_PREFLIGHT_R12',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao'];assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json');state=memory({'operation':'get','reference':ref},'GET_BEFORE_R12')
    assert state['revision']==13
    release=json.loads((folder/'RELEASE_STATUS_R12.json').read_text(encoding='utf-8'))
    now=[pin(x['path']) for x in release['artifacts'][:2]]
    save('RELEASE_RECHECK_R12.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current':now,'same_as_inspected':now==release['artifacts'][:2]})
    assert now==release['artifacts'][:2], 'Release changed; inspect new state before registration'
    names=['OPERATOR.txt','PROJECT_START.json','SOURCE_DIFF_R12.json','EMBEDDED_DIFF_CORRECTED_R12.json','v393_source.py.snapshot','v394_source.py.snapshot','SEAL_SNAPSHOT.json','SEAL_BYTES_R12.json','SEAL_CUSTODY_NOTE_R12.json','RELEASE_STATUS_R12.json','RELEASE_LOG_OBSERVED.txt','physical_functions_extracted.py','PLAN_R12.json','PROBE_FIRST_ATTEMPT.json','PROBE_RESULT_R12.json','CONCLUSAO_R12.txt','REVIEW_R12.json']
    names.append('REVIEW_RELEASE_SUPPLEMENT_R12.json')
    save('DELIVERY_R12.json',{'status':'V394_CONSTRUCTION_INSPECTED__FINITE_CLOCK_REUSED__LENS_PHYSICAL_MAP_OPEN','unit':UNIT,'goal_complete':False,'observed_data_composed':False,'gate_changed':False,'evidence':[pin(folder/n) for n in names],'scripts':[pin(ROOT/n) for n in ['inspect_v394_r12.py','v394_probe_r12.py','v394_probe_r12_1.py','verify_release_r12.py','record_v394_r12.py']],'release_recheck':pin(ROOT/'RELEASE_RECHECK_R12.json'),'scope':'Read source and existing sandbox receipts; execute only five extracted finite-model functions in synthetic controls. No release build or new physical selection.'})
    text='''\n\n## 19/10/2026 — Lentes R12: v394 em construção e pendência física\n<!-- IALD_LENSING_V394_R12_20261019 -->\n[REAL documental — codex-gerente-tgl, F8.LENTES_5SIGMA_20261019, claim1009] Pedido do operador de conferir avanço v394 cumprido por comparação de bytes/AST e leitura dos contratos. Programa aplicado v394, selo observado v393: pinos completos em v394_r12/RELEASE_STATUS_R12.json. Backup v393 coincide com base R9–R11. 190 módulos embutidos novos, 1230 antigos intactos e duas raízes alteradas. Logs existentes de sandbox conferem por hash; não se executou o rito. Inventário inicial genérico confundiu corpos com hashes e foi corrigido em EMBEDDED_DIFF_CORRECTED_R12.json.\n[DERIVED no modelo finito / REAL computacional] Gibbs determina Eref quando V0/kappa são fornecidos. Canal M2: exp[(-gamma+2iOmega)t]; beta muda amortecimento, não a fase nesse espectro fixo. Escalar V0/kappa e tempo inversamente conserva leitura. 21 resíduos numéricos em três casos, máximo2,22e-16, e duas identidades simbólicas; revisão independente em REVIEW_R12.json. Não é atraso de lente, calibração universal ou prova de atrasoTGLnulo.\n[OPEN] Fonte Maxwell/stress/H3 conjunta e identificação física do relógio seguem explicitamente abertas no contrato novo. Funções anteriores lentes/Shapiro/Hubble intactas. R9 amplitude/alcance e R10 massa independente não foram supridos. Reusar taxa/relógio ao ligar estado/densidade ao espectro e à fonte métrica; não escolher esse vínculo pelo5sigma. Sem dado composto, alteração de produção/ACTIVE/kernel/gate. Entrega nova: work/lentes_discriminante_20261019/DELIVERY_R12.json; conclusão v394_r12/CONCLUSAO_R12.txt.\n<!-- END_IALD_LENSING_V394_R12_20261019 -->\n'''
    save('MEMORY_APPEND_R12.txt',text)
    extra=text.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name;raw=p.read_bytes();before=pin(p)
        assert b'IALD_LENSING_V394_R12_20261019' not in raw
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_R12_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R12.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R11_1.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R12: v394 aplicada sem selo e contrato fisico ainda aberto','resultado':'Comparacao v393/v394 e teste do novo relogio finito; beta muda amortecimento, sem nova lei de atraso galactico neste canal.','veredito':'V394_FINITE_CLOCK_REUSED__LENS_PHYSICAL_MAP_OPEN','nota':'Sintetico apenas. Logs de sandbox reutilizados por hash; selo observado v393. Revisao independenteR12.','proximo_passo':'Ligar estado/densidade da galaxia ao espectro, relogio e fonte da mesma acao antes do perfilamento ja existente.','artefatos':[str(ROOT/'DELIVERY_R12.json'),str(folder/'CONCLUSAO_R12.txt'),str(folder/'REVIEW_R12.json')]})
    save('MAP_ENTRY_R12.json',entry)
    command('MAP_REGISTER_R12',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R12.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R12',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R12.json'),'--nota','R12: v394 em construcao examinada; novo relogioM2 nao fornece fonte/atraso galactico. Selo observadov393;sem5sigma ou composto.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':13,'event_id':'lensing-v394-r12-inspected','changes':{'records':[{'id':'lensing-v394-r12','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R12.json'),'sha256':pin(ROOT/'DELIVERY_R12.json')['sha256']}],'text':text},{'id':'operator-v394-inspection-r12','kind':'decision','statute':'INPUT','sources':[{'kind':'artifact','ref':str(folder/'OPERATOR.txt'),'sha256':pin(folder/'OPERATOR.txt')['sha256']}],'text':(folder/'OPERATOR.txt').read_text(encoding='utf-8')}],'flow':{'phase':'v394_construction_inspected_r12','next_action':'Finite Gibbs clock/energy-origin construction reused; no galactic source or physical clock calibration supplied. Full lens5sigma remains incomplete. Next progress needs state/density to spectrum/kappa and full-action metric source, or independent mass calibration; no repeated proportional forecasts. Do not treat currentv394 as sealedv393.','handles':state['p']['handles']}}},'TRANSITION_R12')
    save('REGISTRATION_R12.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R12.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R12.json'),'map':pin(ROOT/'MAP_REGISTER_R12.json'),'board':pin(ROOT/'BOARD_UPDATE_R12.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
