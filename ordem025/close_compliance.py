"""Custody final compliance evidence; management approval remains separate."""
from task import *
import datetime
OUT=Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025')
D=OUT/'CUMPRIMENTO_FINAL'

def board(args):
    p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True)
    if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
    r=json.loads(p.stdout)
    assert r['ok']
    return r

def main():
    p=project();t=next(x for x in p['projection']['active'] if x['id']=='compliance_final')
    assert act('check',task_id=t['id'],lease_id=t['lease']['id'])['ready']
    review=W/'REVIEW_COMPLIANCE_FINAL.json'
    r=json.loads(review.read_text(encoding='utf8'))
    assert r['verdict'] in ('PASS','PASS_WITH_SCOPE')
    with (D/'REVISAO_CUMPRIMENTO.json').open('xb') as f:f.write(review.read_bytes())
    for item in json.loads((OUT/'RESULTADO.json').read_text(encoding='utf8'))['files']:
        assert pin(Path(item['path']))['sha256']==item['sha256']
    files=[pin(x) for x in sorted(D.iterdir()) if x.is_file()]
    result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'execution_status':'ENTREGA_TECNICA_COMPLETA_A_D_E_ADENDO_A',
      'scientific_result':'PONTE PARCIAL',
      'management_status':'AGUARDA_EXAME_REGISTRO_MAPA_E_EVENTUAL_INTEGRACAO',
      'unit':UNIT,'files':files,'prior_delivery':pin(OUT/'RESULTADO.json'),
      'source_addendum':pin(OUT/'ADENDO_A/FONTES_VIGENTES_ADENDO_A.json'),
      'review':pin(review),
      'completed_now':'Consulta reproduzivel do inventario e leitura das fontes para D; conferencia dos requisitos e80checks de integridade.',
      'no_new_lean_build':True,'original_proof_unchanged':True,
      'open_scientific_limits':['identificacao/calibracao do corpo observado','selecao da massa','identificacao plena theta/sigma BW','T/fluxo e H3','assinatura CP/rank4'],
      'scope':'Cumprimento da ordem permite PONTE PARCIAL; nao equivale a provar a identificacao fisica plena nem ao aceite da gerencia.',
      'gate_changed':False,'production_installed':False}
    final=D/'RESULTADO_CUMPRIMENTO.json'
    data=json.dumps(result,ensure_ascii=False,indent=2).encode('utf8')
    with final.open('xb') as f:f.write(data)
    assert final.read_bytes()==data
    new('COMPLIANCE_SUBMIT.json',act('submit',task_id=t['id'],lease_id=t['lease']['id'],
        evidence=[pin(final),pin(review)],event_id='o25-compliance-submit'))
    b=board(['avancar',UNIT,'--quem',OWNER,'--status','ENTREGUE','--evidencia',str(final),str(D/'CUMPRIMENTO.md'),
       '--nota','Conferencia integral A-D e AdendoA; lacuna documental D suprida; revisao distinta. Resultado PONTE PARCIAL, sem promover identificacao fisica plena. Gerencia registra mapa e decide integracao.'])
    new('COMPLIANCE_BOARD.json',b)
    p=call({'operation':'project','reference':str(REF),'max_chars':100000},False)
    new('COMPLIANCE_MEMORY.json',call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},
      'expected_revision':p['receipt']['revision'],'event_id':'o25-compliance-material',
      'changes':{'records':[{'id':'o25-final-compliance','kind':'fact','statute':'REAL',
        'text':'Conferencia final da ORDEM025:80checks passaram; A-D e AdendoA atendidos no escopo permitido de PONTE PARCIAL. Revisao independente apontou ausencia do recibo de consulta ao inventario; complemento D foi produzido e revisado, sem nova ciencia. Gerencia ainda deve examinar, registrar mapa e decidir integracao. Original Lean e evidencias preservados; nao foi declarada identificacao fisica plena.',
        'sources':[{'kind':'artifact','ref':str(final),'sha256':pin(final)['sha256']},
                   {'kind':'artifact','ref':str(review),'sha256':pin(review)['sha256']}]}],
        'flow':{'phase':'awaiting_management_audit','next_action':'Gerencia examina entrega ORDEM025 completa, resultado PONTE PARCIAL, com AdendoA e CUMPRIMENTO_FINAL. Nao repetir provas; mapa e integracao sao da gerencia.'}}},False))
    new('COMPLIANCE_RELEASE.json',board(['liberar',UNIT,'--quem',OWNER,'--nota','Conferencia e complemento D entregues; nenhuma reivindicacao restante deste executor.']))
    verify=call({'operation':'verify','reference':str(REF)},False)
    new('COMPLIANCE_MEMORY_VERIFY.json',verify)
    print(json.dumps({'board_event':b['evento'],'evidence':pin(final),'memory_revision':project()['receipt']['revision'],'verify':verify},ensure_ascii=False))

if __name__=='__main__':main()
