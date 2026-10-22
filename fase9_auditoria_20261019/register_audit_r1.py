"""Register this bounded audit, preserving all earlier scientific artifacts."""
from setup_audit import ROOT, UNIT, ACTOR, save, cmd, mem, pin
from pathlib import Path
import json, sys, datetime, os

if __name__ == '__main__':
    for name in ['DELIVERY_R1.json','MEMORY_APPLIED_R1.json','MAP_ENTRY_R1.json','REGISTRATION_R1.json']:
        if (ROOT/name).exists():
            raise FileExistsError(name)
    review=json.loads((ROOT/'FINAL_REVIEW_R1.json').read_text(encoding='utf-8'))
    assert str(review['status']).startswith('PASS'), review
    for item in review['evidence']:
        assert pin(item['path'])['sha256']==item['sha256'],item['path']
    board=json.loads(cmd('BOARD_PREFLIGHT_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao']
    assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json')
    state=mem('GET_BEFORE_REGISTER_R1',{'operation':'get','reference':ref})
    assert state['revision']==0
    files=['OPERADOR.txt','UNIT.json','CLAIM.json','NOS_F3_1.json','NOS_F3_2.json','NOS_AUDIT_UNIT_R1.json','BOARD_F3_1.json','BOARD_F3_2.json','MAP_BEFORE.json',
           'ADMINISTRATIVE_SNAPSHOT_R1.json','capture_administration_r1.py',
           'AUDITORIA_FASE9_R1.txt','PRECISION_PLAN_R1.json','precision_budget_r1.py','PRECISION_RESULT_R1.json',
           'SYSTEMATICS_AUDIT_R1.json','SYSTEMATICS_AUDIT_R1.txt','SYSTEMATICS_ANCHOR_CORRECTION_R1.json',
           'EXECUTION_AUDIT_R1.json','EXECUTION_AUDIT_R1.txt','STATISTICAL_SCOPE_R1.json','STATISTICAL_SCOPE_R1.txt','FINAL_REVIEW_R1.json']
    if (ROOT/'ERRATA_REVISAO_R1.txt').exists():
        files.append('ERRATA_REVISAO_R1.txt')
    save('DELIVERY_R1.json',{'unit':UNIT,'status':'AUDIT_DELIVERED__EXPECTED_SEPARATION_CONDITIONAL__NO_NEW_OBSERVED_RESULT',
        'c1_acceptance':'PENDING','audit_scope_complete':True,'five_sigma_detection_demonstrated':False,
        'precision_status':'DERIVED_FROM_PINNED_DESIGN_NOT_OBSERVED','observed_V2_Z':None,
        'primary_BG1_expected_range':[5.721408279546075,6.6232188561058924],
        'no_cepheids_BG1_expected_range':[3.9379173289752343,4.395122057191511],
        'historical_V1_score_role':'4.2837356; original INCONCLUSIVE_SYSTEMATICS; not a new calibrated tail',
        'remaining':['Covariance/physical observable map qualification','Real background and free-background likelihood integration',
                     'Pinned D-H admission consumer','Numerical convergence refusal contract','Null-tail and multiplicity qualification',
                     'Applicable operator acts, freeze and authorized opening'],
        'reused':['F3.1 R5.2/E1','F3.2 E1 bytes portable harness','C1 audit registered by event679','Joint covariance/theta/tail contracts'],
        'index_limit':'New bounded audit unit is not yet in NOS_VIVO graph; failure receipt retained. Existing F3.1 and F3.2 queries succeeded and supplied reuse context. Global index was not rebuilt.',
        'observed_data_composed':False,'old_tests_repeated':False,'provider_calls':0,'production_science_changed':False,'gate_changed':False,
        'evidence':[pin(ROOT/n) for n in files],'registration_script':pin(__file__)})
    note=r'''

## 19/10/2026 — Fase 9: auditoria de suficiência e acompanhamento de sigma
<!-- IALD_FASE9_AUDIT_20261019_R1 -->
[REAL documental — em nome de codex-gerente-tgl, F3.AUDITORIA_20261019, reivindicação 1029] Reaproveitados F3.1 R5.2/E1 e F3.2 E1 bytes/harness portátil. A c1 aprovou o harness em 08/10 e registrou novamente no evento679 em12/10; não é novo teste. 46 verificações de integridade na auditoria estática, sem repetir testes antigos. Pareceres de sistemáticas/execução/estatística e revisão independente da síntese estão na entrega. Não é aceite formal c1.
[DERIVED — desenho condicional, não medida] Recalculados beta=alpha_CODATA2018*sqrt(e) e K em runtime;12 extremos conferidos. Separação nominal primária BG1:5,721408–6,623219. Sem Cefeidas:3,937917–4,395122. Na mesma hipótese de sinal/fundo/erros, sigma_local paraD=5 é1,101379835km/s/Mpc; sem Cefeidas requer redução12,96%–22,52%. Isso não é ganho observado nem poder probabilístico do pipeline. V1histórica z_disc4,2837356/INCONCLUSIVE_SYSTEMATICS permanece separada; V2observada NULL. A estimativa anterior14,3% se referia a contraste/modelo fixos históricos, não a esta previsão V2.
[OPEN] Correlações SN/Pantheon/HST fora da caixa, mapas físicos dos leitores, origem0,031SBF, alcance das compressões e incerteza cosmológica deK. Fundo gaussiano comum já marginalizado corretamente no contrato; fundo livre físico ainda não ligado (há mock). Faltam consumidorD-H, critério numérico de convergência e qualificação de cauda/multiplicidade para alegar5sigma. sqrtDeltaQ não é automaticamente um desvio normal sobH0; não foi recalculado p doV1. Contratos conjuntos já existem e não se somam/emprestam à testemunha escalar.
[INPUT/OPEN administrativo] F3.4 já resolvida. Quadro/lista recuperados conservam X13/D-H; abertura própria preservada. d72 é da rota conjunta, não condição inventada para toda execução escalar. Esta auditoria não concede esses atos. Nenhum dado V2composto, congelamento, provedor, Bancada, kernel, um.py ou gate alterado. Próximo trabalho material: qualificar insumos/ligação física e calibração em cópia antes de execução observada autorizada, sem ajustar beta/fundo/covariâncias ao resultado.
Entrega: C:\IALD\Central de Patentes\work\fase9_auditoria_20261019\DELIVERY_R1.json. Referência ACOM própria SESSION_REFERENCE.json nessa pasta. Original e evidências anteriores preservados; NOT_FALSIFIED nunca é CONFIRMED.
<!-- END_IALD_FASE9_AUDIT_20261019_R1 -->
'''
    # All prose is saved as a separate artifact before append; byte backups stay beside memory.
    save('MEMORY_APPEND_R1.txt',note)
    extra=note.encode('utf-8'); stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        target=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=target.read_bytes(); before=pin(target)
        assert b'IALD_FASE9_AUDIT_20261019_R1' not in raw
        backup=target.with_name(target.name+'.bak_'+stamp)
        with backup.open('xb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        assert backup.read_bytes()==raw
        temp=target.with_name(target.name+'.tmp_fase9_'+stamp)
        with temp.open('xb') as f:
            f.write(raw+extra); f.flush(); os.fsync(f.fileno())
        assert temp.read_bytes()==raw+extra and target.read_bytes()==raw
        os.replace(temp,target)
        assert target.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(backup),'after':pin(target),'pure_append':True})
    save('MEMORY_APPLIED_R1.json',rows)
    entry={'tipo':'ROTA','rota_id':'d1.fase9.auditoria_suficiencia_20261019','dominio':'D1_FUNDO_COSMOLOGICO',
        'titulo':'Auditoria de suficiência Fase9: desenho nominal acima de5, execução e sistemáticas condicionadas',
        'pergunta':'O que falta corrigir para avaliar5sigma sem ajustar parâmetros ao dado?',
        'dados':['Artefatos existentes F3.1/F3.2 e auditorias c1; sem composto observado V2'],
        'metodo':'Revisão estática, conferência de pins, reaproveitamento de testes,12 extremos algébricos só por sigmas e BG preselecionado; revisão independente',
        'resultado':'Primário BG1 D=5.721408–6.623219; sem Cefeidas D=3.937917–4.395122. Separação esperada condicional; V2 observada não calculada. Histórico V1 escore4.2837356 preservado.',
        'veredito':'EXPECTED_SEPARATION_SUFFICIENT_CONDITIONALLY__OBSERVED_V2_OPEN','estatuto':'DERIVED','status':'EXAMINADA_COM_DEFEITO',
        'olhou_dados':False,'defeito':'Covariâncias/mapas incompletos; fundo livre mock; integração D-H/modo real pendentes; calibração de cauda e tolerância numérica a qualificar.',
        'nao_refazer':'Gate e harness já auditados; não repetir consertosNaN/portabilidade/pinos nem reconstruir contratos conjuntos.',
        'proximo_passo':'Qualificar fontes, mapas, ligação física e calibração em cópia; atos X13/D-H/congelamento/abertura próprios; d72 pertence à conjunta.',
        'onde':str(ROOT/'AUDITORIA_FASE9_R1.txt'),'artefatos':[str(ROOT/'DELIVERY_R1.json'),str(ROOT/'AUDITORIA_FASE9_R1.txt'),str(ROOT/'PRECISION_RESULT_R1.json'),str(ROOT/'FINAL_REVIEW_R1.json')],
        'refs':['d1.fase9.f3_1_semantica_v1x_leitores'],
        'nota':'Nenhum novo p/Z observado, provedor, produção ou gate. Audit delivered, formal c1 acceptance pending.'}
    save('MAP_ENTRY_R1.json',entry)
    cmd('MAP_REGISTER_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R1.json'),'--quem',ACTOR['id']])
    cmd('BOARD_DELIVERY_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','ENTREGUE','--evidencia',str(ROOT/'DELIVERY_R1.json'),'--nota','Auditoria limitada concluída; reusoE1,12extremos conferidos, síntese revisada. Desenho nominal primário>5 condicional, observadoV2null; integração/sistemáticas/cauda abertas. Sem mover gate.'])
    transition=mem('TRANSITION_R1',{'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':0,'event_id':'fase9-audit-r1-delivered','changes':{
        'records':[{'id':'fase9-audit-r1','kind':'fact','statute':'DERIVED','text':note,'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R1.json'),'sha256':pin(ROOT/'DELIVERY_R1.json')['sha256']}]}],
        'flow':{'phase':'audit_delivered_pending_c1','next_action':'Reuse delivered audit. Primary expected separation5.72–6.62 conditional, noCepheids3.94–4.40; no observedV2. Qualify covariance/maps, real background/admission and tail calibration in copies before authorized freeze/opening. Do not rerun fixed harness or tune beta/covariance to outcome.','handles':state['p']['handles']}}})
    cmd('RELEASE_R1',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','liberar',UNIT,'--quem',ACTOR['id'],'--nota','Auditoria entregue com evidências novas; aguarda c1. Memórias previstas atualizadas com backups.'])
    save('REGISTRATION_R1.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R1.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R1.json'),'map':pin(ROOT/'MAP_REGISTER_R1.json'),'board':pin(ROOT/'BOARD_DELIVERY_R1.json'),'release':pin(ROOT/'RELEASE_R1.json'),'acom':transition})
    print(json.dumps({'status':'PASS','unit':UNIT,'acom':transition},ensure_ascii=False))
