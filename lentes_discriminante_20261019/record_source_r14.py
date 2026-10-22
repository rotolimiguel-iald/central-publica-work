"""Append reviewed R14 evidence to the existing lens mission only."""
from setup import ROOT,UNIT,ACTOR,save,command,memory
from record_trajectory_r2 import pin
from pathlib import Path
import json,datetime,sys,os

if __name__=='__main__':
    d=ROOT/'full_source_r14'
    for n in ['DELIVERY_R14.json','MEMORY_APPLIED_R14.json','MAP_ENTRY_R14.json','REGISTRATION_R14.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    review=json.loads((d/'REVIEW_R14.json').read_text(encoding='utf-8'))
    assert str(review['status']).startswith('PASS')
    for a in review['evidence']:assert pin(a['path'])['sha256']==a['sha256'],a['path']
    board=json.loads(command('BOARD_PREFLIGHT_REG_R14',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao'];assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json');state=memory({'operation':'get','reference':ref},'GET_BEFORE_R14')
    assert state['revision']==15
    p=json.loads((d/'PINS_RELEASE_R14.json').read_text(encoding='utf-8'))
    for a in p['sources']+p['artifacts']:assert pin(a['path'])['sha256']==a['sha256'],a['path']
    names=['OPERADOR.txt','SOURCE_ACTION_R14.json','PINS_RELEASE_R14.json','PLAN_R14.json','derive_r14.py','RESULT_R14.json','PLAN_CARTAN_R14.json','cartan_r14.py','CARTAN_RESULT_R14.json','DERIVACAO_R14.txt','REVIEW_R14.json']
    if (d/'ESCOPO_APOS_REVISAO_R14.txt').exists():names.append('ESCOPO_APOS_REVISAO_R14.txt')
    names.append('ERRATA_REVISAO_R14.txt')
    save('DELIVERY_R14.json',{'unit':UNIT,'status':'NULL_SOURCE_TO_LENS_POTENTIAL_DERIVED__GALACTIC_SUPPLIER_OPEN','goal_complete':False,
        'observed_data_composed':False,'gate_changed':False,'evidence':[pin(d/n) for n in names],
        'script':pin(__file__),'scope':'R88 literal one-form source projected into linearized lens potential; spinless Cartan correction composed; full physical state/signs/modular source not supplied.',
        'checks':{'symbolic':14,'negative_controls':3,'review':review['status']}})
    note='''\n\n## 19/10/2026 — Lentes R14: fonte variada e potencial óptico\n<!-- IALD_LENSING_SOURCE_R14_20261019 -->\n[REAL documental — em nome de codex-gerente-tgl, F8.LENTES_5SIGMA_20261019, claim1009] Oito fontes pinadas: ação Custo/Ponte/v394 e variaçõesR86/R88/R89. Programa v394 aplicado permanece igual ao snapshot; selo conferido ainda v393. Fonte covetorial já variada reaproveitada; não afirmar ausência de toda fonte nem estado selado para candidatos.\n[DERIVED condicional] No ramo literal R88 (+---, fR, T=-2deltaS e ressalva de sinal energético preservada), fundo plano/Abar/fbar constantes, estático/harmônico/Born: 2fbar Delta W_n=deltaT_kk+2xi partial_z²delta u−2xi R1(Abar.k)². W_n=h_kk/2, igualPhi+Psi no caso escalar métrico. Projeção ao longo do raio transforma a Hessiana em termo de extremos; a parcela de curvatura pode permanecer, mas ainda depende das EOM acopladas. FundoAbarzero a elimina nesta ordem. Condições de contorno/gauge nomeadas.\n[DERIVED] Fornecedor Cartan sem spin: o cinético3(df)²/(2f) tem fonte linear6xi Abar tensor Abar box(deltaf)/fbar quando f depende da norma métrica. A combinação trocaRg1 porR_Gamma1=Rg1−3box(deltaf)/fbar; não contar ambos separadamente. MatériaDirac comspin não foi coberta. Termo modular bL0 exige variar b e a corrente de bordo deL0: fórmula local Tb=bT0−2L0delta b/deltag só no subcaso sem derivadas métricas, conforme ERRATA_REVISAO_R14. Green2D é potencial regularizado/módulo constante ou diferenças, não integral infinita absoluta. R86poeira conserva a degenerescência de massaR10.\n[REAL computacional / DERIVED]14 identidades simbólicas e3controles negativos, planos prévios; fórmula Green2D e primeira variação do atraso de Fermat em DERIVACAO_R14.txt. Revisão independente REVIEW_R14.json. Sem parâmetros galácticos ajustados, observado, nova provaLean ou5sigma.\n[OPEN] Fonte física galáctica única: estado/perfil, sinais, ligação escalar/1forma e derivada funcional modular. v394Gibbs não fornece esse tensor/relógio local. Termo algébrico candidato não é sinal nãozero demonstrado após EOM. Próxima ação é completar esse fornecedor pela mesma ação, não somar consistências nem repetirforecastsR10. Nenhum um.py/kernel/Bancada/gate alterado. Entrega work/lentes_discriminante_20261019/DELIVERY_R14.json.\n<!-- END_IALD_LENSING_SOURCE_R14_20261019 -->\n'''
    save('MEMORY_APPEND_R14.txt',note);extra=note.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        q=Path(r'C:\IALD\Central de Patentes\memory')/name;raw=q.read_bytes();before=pin(q)
        assert b'IALD_LENSING_SOURCE_R14_20261019' not in raw
        bak=q.with_name(q.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=q.with_name(q.name+'.tmp_R14_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and q.read_bytes()==raw
        os.replace(tmp,q);assert q.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(q),'pure_append':True})
    save('MEMORY_APPLIED_R14.json',rows)
    e=json.loads((ROOT/'MAP_ENTRY_R13.json').read_text(encoding='utf-8'))
    e.update({'titulo':'Lentes R14: fonte nula, potencial projetado e Cartan sem spin',
      'resultado':'Hessiana vira bordo; termo covetorial de curvatura e fonte modular entram no potencial. Ramo galactico completo ainda nao selecionado.',
      'veredito':'NULL_SOURCE_LENS_PROJECTION_DERIVED__GALACTIC_INPUT_OPEN',
      'nota':'14 identidades e3controles negativos; revisao independente; sem observado ou ajuste. v394construcao/selo v393.',
      'proximo_passo':'Identificar estado/fonte modular/convencoes fisicas da mesma acao e resolver EOM acopladas antes de significancia.',
      'artefatos':[str(ROOT/'DELIVERY_R14.json'),str(d/'DERIVACAO_R14.txt'),str(d/'REVIEW_R14.json')]})
    save('MAP_ENTRY_R14.json',e)
    command('MAP_REGISTER_R14',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R14.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R14',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R14.json'),'--nota','R14: fonte nula para potencial de lentes e correcaoCartan derivadas condicionalmente; fornecedor galactico completo aberto. Sem5sigma/ajuste/composto.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':15,'event_id':'lensing-full-source-r14-derived','changes':{
      'records':[{'id':'lensing-source-r14','kind':'fact','statute':'DERIVED','text':note,
       'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R14.json'),'sha256':pin(ROOT/'DELIVERY_R14.json')['sha256']}]},
       {'id':'operator-source-r14','kind':'decision','statute':'INPUT','text':(d/'OPERADOR.txt').read_text(encoding='utf-8'),
       'sources':[{'kind':'artifact','ref':str(d/'OPERADOR.txt'),'sha256':pin(d/'OPERADOR.txt')['sha256']}]}],
      'flow':{'phase':'null_source_to_lens_potential_r14','next_action':'Reuse R14 null projection and spinlessCartan correction. Missing material step is same-action galactic state/source, signs and modular metric variation; solve coupled EOM before claiming nonzero beta lens signal. Do not repeat R9/R10/R13 algebra or select parameters from delays. v394 construction remains separate from observedv393seal.','handles':state['p']['handles']}}},'TRANSITION_R14')
    save('REGISTRATION_R14.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R14.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R14.json'),'map':pin(ROOT/'MAP_REGISTER_R14.json'),'board':pin(ROOT/'BOARD_UPDATE_R14.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
