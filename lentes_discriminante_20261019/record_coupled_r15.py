"""Append reviewed R15 evidence to the existing lens mission only."""
from setup import ROOT,UNIT,ACTOR,save,command,memory
from record_trajectory_r2 import pin
from pathlib import Path
import json,datetime,sys,os

if __name__=='__main__':
    d=ROOT/'coupled_r15'
    for n in ['DELIVERY_R15.json','MEMORY_APPLIED_R15.json','MAP_ENTRY_R15.json','REGISTRATION_R15.json']:
        if (ROOT/n).exists():raise FileExistsError(n)
    review=json.loads((d/'REVIEW_R15.json').read_text(encoding='utf-8'))
    assert str(review['status']).startswith('PASS')
    for a in review['evidence']:assert pin(a['path'])['sha256']==a['sha256'],a['path']
    board=json.loads(command('BOARD_PREFLIGHT_REG_R15',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao'];assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json');state=memory({'operation':'get','reference':ref},'GET_BEFORE_R15')
    assert state['revision']==16
    p=json.loads((d/'PINS_RELEASE_R15.json').read_text(encoding='utf-8'))
    for a in p['sources']+p['artifacts']:assert pin(a['path'])['sha256']==a['sha256'],a['path']
    names=['OPERADOR.txt','SOURCE_BACKGROUND_R15.json','PINS_RELEASE_R15.json','PLAN_R15.json','solve_r15.py','RESULT_R15.json','DERIVACAO_R15.txt','REVIEW_R15.json']
    if (d/'ERRATA_REVISAO_R15.txt').exists():names.append('ERRATA_REVISAO_R15.txt')
    save('DELIVERY_R15.json',{'unit':UNIT,'status':'COUPLED_BRANCH_SOLVED__OPTICAL_CANCELLATION__PHYSICAL_SELECTION_OPEN','goal_complete':False,
        'observed_data_composed':False,'gate_changed':False,'evidence':[pin(d/n) for n in names],
        'script':pin(__file__),'scope':'Named static covector plus spinless Cartan branch solved. Optical curvature contribution cancels prefactor; constant dynamics/light ratio remains conditional. Full galactic source not selected.',
        'checks':{'symbolic':21,'bookkeeping_identity':1,'negative_controls':1,'review':review['status']}})
    note='\n\n## 19/10/2026 — Lentes R15: sistema acoplado resolvido no ramo estático\n<!-- IALD_LENSING_COUPLED_R15_20261019 -->\n[DERIVED condicional — em nome de codex-gerente-tgl, F8.LENTES_5SIGMA_20261019, claim1009] Reuso da ação covetorial R88, Cartan sem spin v370/v394 e projeção R14. No ramo literal +---, f=f0+xi A², Abar=a dt, fonte efetiva compacta/pressão nula na primeira ordem, campos regulares decaindo e sem termos adicionais E_rest,A: Phi=(1+q)W0, Psi=(1−q)W0, q=xi(1+4xi)a²/f0; Delta W0=rho_eff/(4f0). Maxwell linear é mantido. Acurvatura RGamma1=−rho_eff/(2f0) é não nula; a combinação rho_eff−2xi a² RGamma1=rho_eff fbar/f0 cancela a mudança do prefator óptico. Assim Phi+Psi=2W0. Não há nova forma radial nos atrasos desse ramo.\n[DERIVED] Se adotado o fluido R86 w=0, rho_eff=(1+beta)rho é absorvido em massa óptica M_fit=(1+beta)M. A razão dinâmica/óptica 1+q pode permanecer em calibração independente; não dizer que uma única massa apaga todos os observáveis. a e correspondência de G_lab ao f0 não foram selecionados. A_tor=df/(2f) da v394 não é o campo A luminodinâmico. Sinais literais/estabilidade e completude escalar versus1forma preservados como limites.\n[REAL computacional] Plano anterior; 21 checagens simbólicas do sistema/limites/componentes, uma identidade tautológica de reparametrização explicitamente identificada, um controle negativo Cartan. Revisão independente em REVIEW_R15.json; cálculo não é provaLean. v394 aplicada e selo v393 conferidos por hash, sem alterações.\n[OPEN] Estado galáctico completo e termos adicionais da mesma ação podem mudar a resposta; recuperação de fonte modular/potencial e seleção independente de fundo é a próxima ação concreta. Nenhum parâmetro aos atrasos, dado observado, 5sigma, kernel/Bancada/gate. DERIVACAO_R15.txt e DELIVERY_R15.json em work/lentes_discriminante_20261019.\n<!-- END_IALD_LENSING_COUPLED_R15_20261019 -->\n'
    save('MEMORY_APPEND_R15.txt',note);extra=note.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        q=Path(r'C:\IALD\Central de Patentes\memory')/name;raw=q.read_bytes();before=pin(q)
        assert b'IALD_LENSING_COUPLED_R15_20261019' not in raw
        bak=q.with_name(q.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=q.with_name(q.name+'.tmp_R15_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and q.read_bytes()==raw
        os.replace(tmp,q);assert q.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(q),'pure_append':True})
    save('MEMORY_APPLIED_R15.json',rows)
    e=json.loads((ROOT/'MAP_ENTRY_R14.json').read_text(encoding='utf-8'))
    e.update({'titulo':'Lentes R15: solucao acoplada, cancelamento optico e razao dinamica',
      'resultado':'Ramo estatico acoplado: Phi+Psi=2W0; curvatura cancela prefator. Razao dinamica/luz constante1+q; estado fisico nao selecionado.',
      'veredito':'COUPLED_OPTICAL_CANCELLATION__GALACTIC_SELECTION_OPEN',
      'nota':'21checagens,1identidade bookkeeping e1controle negativo; revisao independente; sem observado ou ajuste. v394construcao/selo v393.',
      'proximo_passo':'Selecionar estado e termos adicionais de A pela mesma acao; calibrar a e G independentemente dos atrasos, sem repetir ramo resolvido.',
      'artefatos':[str(ROOT/'DELIVERY_R15.json'),str(d/'DERIVACAO_R15.txt'),str(d/'REVIEW_R15.json')]})
    save('MAP_ENTRY_R15.json',e)
    command('MAP_REGISTER_R15',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R15.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R15',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R15.json'),'--nota','R15: ramo acoplado resolvido, cancelamento optico e razao constante dinamica/luz. Estado fisico completo aberto. Sem5sigma/ajuste/composto.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':16,'event_id':'lensing-coupled-r15-derived','changes':{
      'records':[{'id':'lensing-source-r15','kind':'fact','statute':'DERIVED','text':note,
       'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R15.json'),'sha256':pin(ROOT/'DELIVERY_R15.json')['sha256']}]},
       {'id':'operator-source-r15','kind':'decision','statute':'INPUT','text':(d/'OPERADOR.txt').read_text(encoding='utf-8'),
       'sources':[{'kind':'artifact','ref':str(d/'OPERADOR.txt'),'sha256':pin(d/'OPERADOR.txt')['sha256']}]}],
      'flow':{'phase':'coupled_static_branch_solved_r15','next_action':'R15 coupled static timelike covector plus spinless Cartan branch solved: optical contribution cancels prefactor, constant dynamics/light ratio remains. Next: same-action additional A equation and independently selected galactic background/calibration. Do not repeat solved algebra, fit delays or assert5sigma. v394 construction distinct from sealv393.','handles':state['p']['handles']}}},'TRANSITION_R15')
    save('REGISTRATION_R15.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R15.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R15.json'),'map':pin(ROOT/'MAP_REGISTER_R15.json'),'board':pin(ROOT/'BOARD_UPDATE_R15.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
