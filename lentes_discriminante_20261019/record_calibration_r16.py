"""Append reviewed R16 evidence to the existing lens mission only."""
from setup import ROOT,UNIT,ACTOR,save,command,memory
from record_trajectory_r2 import pin
from pathlib import Path
import json,datetime,sys,os

if __name__=='__main__':
    d=ROOT/'calibration_r16'
    for n in ['DELIVERY_R16.json','MEMORY_APPLIED_R16.json','MAP_ENTRY_R16.json','REGISTRATION_R16.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    review=json.loads((d/'REVIEW_R16.json').read_text(encoding='utf-8'))
    assert str(review['status']).startswith('PASS')
    for a in review['evidence']:assert pin(a['path'])['sha256']==a['sha256'],a['path']
    board=json.loads(command('BOARD_PREFLIGHT_REG_R16',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao'];assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json');state=memory({'operation':'get','reference':ref},'GET_BEFORE_R16')
    assert state['revision']==17
    p=json.loads((d/'PINS_RELEASE_R16.json').read_text(encoding='utf-8'))
    for a in p['sources']+p['artifacts']:assert pin(a['path'])['sha256']==a['sha256'],a['path']
    names=['OPERADOR.txt','SOURCE_AMPLITUDE_R16.json','SOURCE_G_R16.json','PINS_RELEASE_R16.json','PLAN_R16.json','calibrate_r16.py','RESULT_R16.json','DERIVACAO_R16.txt','PROGRESSO_SIGMA_R16.json','FASE9_BOARD_SNAPSHOT_R16.json','REVIEW_R16.json']
    if (d/'ERRATA_REVISAO_R16.txt').exists():names.append('ERRATA_REVISAO_R16.txt')
    save('DELIVERY_R16.json',{'unit':UNIT,'status':'G_CALIBRATION_DERIVED__AMPLITUDE_OPEN__SIGMA_TRACKED','goal_complete':False,
        'observed_data_composed':False,'gate_changed':False,'evidence':[pin(d/n) for n in names],
        'script':pin(__file__),'scope':'R15 branch calibrated conditionally to measured G, apparent masses and covariance. Independent field amplitude remains open. Historical Fase9 kept separate from lens forecast and observed values.',
        'checks':{'symbolic':8,'negative_controls':2,'review':review['status']}})
    note='\n\n## 19/10/2026 — Lentes R16: calibração de G e acompanhamento de sigma\n<!-- IALD_LENSING_CALIBRATION_R16_20261019 -->\n[REAL documental — em nome de codex-gerente-tgl, F8.LENTES_5SIGMA_20261019, claim1009] Releitura dos3artigos, v394 e extraçãoMacR67 por fontes/trechos pinados. G é entrada medida; normalizaçãoPlanck usa o mesmoG. Custo escreve f0=c4/(16piG), mas não fornece nesse recorte matchingCavendish do fundo a. Retirada autoral G→G(1−beta) recuperada, sem endossar os números experimentais alegados nela. Norma interna1, amplitude ontológicaMac eK0 dohalo não fixam a dimensional sem mapa campo→fonte. Ausência limitada à cobertura, não ao acervo inteiro.\n[DERIVED condicional ao ramoR15, c=1] Gmed=C_lab(1+q_lab)/(16pi f0), q_lab=xi(1+4xi)a_lab²/f0. Com amplitude/fator de matéria independentes a raizpositiva fixa f0; sóGmed não fixa os três. Se mantidos f0=1/(16piGmed) eC_lab1, exigeq_lab0, não demonstra esse fundo na teoria. M_D/M_L=1+q_g cancela normalização comum sob o mesmo perfil físico; não autorizaq=beta nem calibração da teoria pelos atrasos.\n[DERIVED/REAL simbólico]8identidades e2controles negativos; Var(q)≈(1+q)²(vL+vD−2cLD), covariância completa e modelo comum de massa. Lente isolada temFisherdeficiente. Sem amplitude prevista/covariância, Z_esperado eZ_observado sãoNULL, nunca0sigma. Previsão nominal de5 requer sigma_logcontraste<=|ln(1+qTGL)|/5; não é90%depoder nem discriminação exclusiva de teoria.\n[REAL documental] Fase9V1 preservada na construçãov394: zdisc4.2837356139 eINCONCLUSIVE_SYSTEMATICS, não resultadoV2. QuadroF3.1/F3.2AUDITADA eF3.4FECHADA. Contraste fixo precisaria incerteza14.3%menor para5; equivalência36%mais informação vale somente com erro estatístico independente dominante. Não somar com lentes, não transformarσempercentualdeprova, não promover a confirmação. Não foi auditado integralmente estado posterior de admissões nem executado composto.\n[OPEN] qgal(beta,estado) independente, matchingG e fonte galáctica completa; Fase9 permanece candidata quantitativa a priorizar, sem mudar critérios retrospectivamente. PROGRESSO_SIGMA_R16.json acompanha lei/versão/fontes/efeito/covariância/forecast/observado/impedimento separadamente. Revisão independente em REVIEW_R16.json. MemóriaACOM própria, nenhuma alteração deum.py/kernel/Bancada/gate ouobservado. Entrega work/lentes_discriminante_20261019/DELIVERY_R16.json.\n<!-- END_IALD_LENSING_CALIBRATION_R16_20261019 -->\n'
    save('MEMORY_APPEND_R16.txt',note);extra=note.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        q=Path(r'C:\IALD\Central de Patentes\memory')/name;raw=q.read_bytes();before=pin(q)
        assert b'IALD_LENSING_CALIBRATION_R16_20261019' not in raw
        bak=q.with_name(q.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=q.with_name(q.name+'.tmp_R16_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and q.read_bytes()==raw
        os.replace(tmp,q);assert q.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(q),'pure_append':True})
    save('MEMORY_APPLIED_R16.json',rows)
    e=json.loads((ROOT/'MAP_ENTRY_R15.json').read_text(encoding='utf-8'))
    e.update({'titulo':'Lentes R16: calibracao de G, amplitude aberta e acompanhamento de sigma',
      'resultado':'Gmed calibra combinacao f0,a_lab,C_lab. RazaoMdin/Mlens=1+qgal; amplitude independente aberta. Sigma lentesnull; Fase9V1historica4.28inconclusiva.',
      'veredito':'G_MATCHING_DERIVED__NO_LENS_NUMERIC_SIGMA',
      'nota':'8checagens e2controles negativos; revisao independente; sem observado ou ajuste. v394construcao/selo v393.',
      'proximo_passo':'Buscar fornecedor dimensional independente qgal(beta,estado); Fase9 e candidata quantitativa distinta, preservados criterios e admissoes. Nao repetir matching ou ajustar atraso.',
      'artefatos':[str(ROOT/'DELIVERY_R16.json'),str(d/'DERIVACAO_R16.txt'),str(d/'REVIEW_R16.json')]})
    save('MAP_ENTRY_R16.json',e)
    command('MAP_REGISTER_R16',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R16.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R16',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R16.json'),'--nota','R16: matchingG e erro da razao dinamica/luz derivados; amplitudeaberta, sigmalentesnull. Fase9historica separada. Semajuste/composto.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':17,'event_id':'lensing-calibration-r16-derived','changes':{
      'records':[{'id':'lensing-source-r16','kind':'fact','statute':'DERIVED','text':note,
       'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R16.json'),'sha256':pin(ROOT/'DELIVERY_R16.json')['sha256']}]},
       {'id':'operator-source-r16','kind':'decision','statute':'INPUT','text':(d/'OPERADOR.txt').read_text(encoding='utf-8'),
       'sources':[{'kind':'artifact','ref':str(d/'OPERADOR.txt'),'sha256':pin(d/'OPERADOR.txt')['sha256']}]}],
      'flow':{'phase':'g_matching_and_sigma_tracker_r16','next_action':'R16 measured-G matching and covariance derived conditionally from R15. Field amplitude qgal(beta,state) is not selected; norms/Planck/G are not independent calibrations. Lens forecast and observed sigma null, historical Fase9V1 4.2837 inconclusive kept separate; quantitative route to prioritize only with current criteria/admissions audit. Do not repeat solved algebra or fit delays. v394 construction distinct from sealv393.','handles':state['p']['handles']}}},'TRANSITION_R16')
    save('REGISTRATION_R16.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R16.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R16.json'),'map':pin(ROOT/'MAP_REGISTER_R16.json'),'board':pin(ROOT/'BOARD_UPDATE_R16.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
