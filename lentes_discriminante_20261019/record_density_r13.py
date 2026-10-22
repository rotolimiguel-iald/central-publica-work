"""Register the reviewed density/lens derivation; new evidence and pure memory appends."""
from setup import ROOT, UNIT, ACTOR, save, command, memory
from record_trajectory_r2 import pin
from pathlib import Path
import json, datetime, sys, os

if __name__ == '__main__':
    folder=ROOT/'density_bridge_r13'
    for name in ['DELIVERY_R13.json','MEMORY_APPLIED_R13.json','MAP_ENTRY_R13.json','REGISTRATION_R13.json']:
        if (ROOT/name).exists(): raise FileExistsError(name)
    review=json.loads((folder/'REVIEW_R13.json').read_text(encoding='utf-8'))
    assert str(review.get('status','')).startswith('PASS'),review
    for item in review['evidence']:
        assert pin(item['path'])['sha256']==item['sha256'],item['path']
    board=json.loads(command('BOARD_PREFLIGHT_REG_R13',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao'];assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    reference=str(ROOT/'SESSION_REFERENCE.json')
    state=memory({'operation':'get','reference':reference},'GET_BEFORE_R13')
    assert state['revision']==14,state['revision']
    release=json.loads((folder/'SOURCE_AND_RELEASE_RECHECK_R13.json').read_text(encoding='utf-8'))
    for item in release['source_pins']:
        assert pin(item['path'])['sha256']==item['actual'],item['path']
    for item in release['artifacts']:
        assert pin(item['path'])['sha256']==item['sha256'],item['path']
    names=['OPERADOR.txt','PLAN_R13.json','derive_r13.py','DERIVATION_R13.json','CONCLUSAO_R13.txt',
           'SOURCE_DENSITY_R13.json','MODE_PRECISION_R13.json','SOURCE_CLOCK_METRIC_R13.json',
           'SOURCE_ANSATZ_SUPPLEMENT_R13.json','SOURCE_AND_RELEASE_RECHECK_R13.json','REVIEW_R13.json',
           'ESCOPO_APOS_REVISAO_R13.txt']
    evidence=[pin(folder/n) for n in names]
    # The real review file is retained verbatim. All artifacts, including review addenda,
    # remain separately addressable; no status is invented for scientific closure.
    save('DELIVERY_R13.json',{
      'status':'DENSITY_SPECTRUM_RECOVERED__CONDITIONAL_LENS_DELAY_DERIVED__DISCRIMINANT_OPEN',
      'unit':UNIT,'goal_complete':False,'observed_data_composed':False,'gate_changed':False,
      'evidence':evidence,'registration_script':pin(__file__),
      'validation':{'symbolic_identities':13,'synthetic_quadratures':3,'tolerance':1e-10},
      'scope':'Historical halo b=2 under named weak-field source. v394 finite clock reused without assigning a physical galaxy clock. No source/lens fit, canonical changes, new seal or5sigma.'})
    text='''\n\n## 19/10/2026 — Lentes R13: densidade, espectro e funcional de atraso\n<!-- IALD_LENSING_DENSITY_R13_20261019 -->\n[REAL documental — em nome de codex-gerente-tgl, F8.LENTES_5SIGMA_20261019, reivindicação1009] Recuperação focal de oito fontes históricas e sete fontes atuais/auxiliares, pinos conferidos. Gráviton: régua L*=sqrt(epsilon*/(xi C G rho m*)), modos de psíon Dirichlet e perfil de halo. Custo: K_partial=2pi integral x1 T00 d³x na cunha de Rindler. Não há ausência global alegada. v394 consultada em construção; selo rechecado ainda v393.\n[DERIVED condicional] Sob L_cav=L*, c/L*=sqrt(xi C m*c²/epsilon*) sqrt(G rho); prefator material não fixado a1 ou beta. Espectro não determina ocupações/fonte; kappa_loss=omega/Q não é automaticamente relógio modular. Reuso v394 Gibbs seleciona Eref dadoV0/kappa, sem identificar o fornecedor galáctico.\n[DERIVED / REAL computacional] Para halo histórico b_halo=2, fonte métrica fraca usual e régua rc=K0/sqrt(rho0) imposta exatamente (a fonte só dá escala aproximada), Sigma=pi rho0 rc²/sqrt(R²+rc²), M2D=2pi²rho0rc²(sqrt(R²+rc²)-rc), vc∞²=4piG K0². Potencial projetado e atraso de Fermat completos em CONCLUSAO_R13.txt. 13 identidades simbólicas e3 quadraturas sintéticas; revisão independente REVIEW_R13.json. Sem parâmetros ajustados aos atrasos. Halo infinito idealizado, sem fonte TGL completa, bárions/ambiente ou aplicação observada.\n[DERIVED — errata de interpretação para esta rota] No ansatz q=cosh(kappa_s x), G00=G11=0 e G22=G33=kappa_s²; a glosa rho não fornece densidade galáctica de repouso. Lei antiga de massa do Grande Atrator foi retirada no próprio programa; não a reutilizar como calibração.\n[OPEN] Calibração independente da combinação material/estado e fonte covariante da mesma ação. Na métrica usual, igual perfil efetivo dá igual atraso em RG: esta derivação sozinha não fornece discriminaçãoTGL. É avanço do funcional, não5sigma. Não repetir previsões de simples reescalaR10; preservar o diagnóstico escalarR9. Sem um.py/kernel/Bancada/dado/gate alterados. Entrega: work/lentes_discriminante_20261019/DELIVERY_R13.json.\n<!-- END_IALD_LENSING_DENSITY_R13_20261019 -->\n'''
    save('MEMORY_APPEND_R13.txt',text)
    extra=text.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name;raw=p.read_bytes();before=pin(p)
        assert b'IALD_LENSING_DENSITY_R13_20261019' not in raw
        bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_R13_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R13.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R12.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R13: densidade-espectro e atraso condicional do halo recuperado',
      'resultado':'Perfil historico b=2 projetado e atraso de Fermat derivado; parametros materiais/estado preservados, sem ajuste ao dado.',
      'veredito':'CONDITIONAL_DELAY_DERIVED__DISTINCTIVE_BETA_MAP_OPEN',
      'nota':'13 identidades simbolicas e3 quadraturas; revisao independente. v394 em construcao, selo v393;sem5sigma.',
      'proximo_passo':'Confrontar fornecedor covariante da mesma acao e calibracao independente; igual perfil usual nao discriminaTGL.',
      'artefatos':[str(ROOT/'DELIVERY_R13.json'),str(folder/'CONCLUSAO_R13.txt'),str(folder/'REVIEW_R13.json')]})
    save('MAP_ENTRY_R13.json',entry)
    command('MAP_REGISTER_R13',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R13.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R13',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R13.json'),'--nota','R13: cadeia recuperada e atraso condicional derivado; calibração/fonte fisica discriminante ainda abertas. Sem dado composto ou5sigma.'])
    out=memory({'operation':'transition','reference':reference,'actor':ACTOR,'expected_revision':14,
      'event_id':'lensing-density-r13-derived','changes':{
      'records':[{'id':'lensing-density-r13','kind':'fact','statute':'DERIVED',
       'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R13.json'),'sha256':pin(ROOT/'DELIVERY_R13.json')['sha256']}],'text':text},
       {'id':'operator-density-r13','kind':'decision','statute':'INPUT',
       'sources':[{'kind':'artifact','ref':str(folder/'OPERADOR.txt'),'sha256':pin(folder/'OPERADOR.txt')['sha256']}],
       'text':(folder/'OPERADOR.txt').read_text(encoding='utf-8')}],
      'flow':{'phase':'density_spectrum_lens_functional_r13',
       'next_action':'R13 recovered density/ruler, cavity modes, regionalT00 generator and conditional b2halo Fermat functional. Do not repeat recovery or reparameterized forecasts. Next material gap: independent material/state normalization plus full covariant source giving a beta-specific optical potential; finitev394 does not supply it. No observed compound,5sigma or canonical closure.',
       'handles':state['p']['handles']}}},'TRANSITION_R13')
    save('REGISTRATION_R13.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R13.json'),
      'memory':pin(ROOT/'MEMORY_APPLIED_R13.json'),'map':pin(ROOT/'MAP_REGISTER_R13.json'),
      'board':pin(ROOT/'BOARD_UPDATE_R13.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
