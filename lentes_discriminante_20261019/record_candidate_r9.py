"""Register the reviewed conditional scalar completion; preserve all earlier evidence."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, json, os, sys

if __name__ == '__main__':
    folder = ROOT/'candidate_r9'
    names = ['DELIVERY_R9.json', 'MEMORY_APPEND_R9.txt', 'MEMORY_APPLIED_R9.json',
             'REGISTRATION_R9.json', 'MAP_ENTRY_R9.json', 'BOARD_PREFLIGHT_DELIVERY_R9.json',
             'GET_BEFORE_DELIVERY_R9_REQUEST.json', 'GET_BEFORE_DELIVERY_R9_RESULT.json']
    for name in names:
        if (ROOT/name).exists(): raise FileExistsError(name)
    review=json.loads((folder/'REVIEW_R9.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS'),review
    checkpins(review)
    checkpins(json.loads((folder/'SOURCE_CURRENT_R9.json').read_text(encoding='utf-8')))
    board=json.loads(command('BOARD_PREFLIGHT_DELIVERY_R9',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    c=board['reivindicacao'];assert c['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(c['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json')
    state=memory({'operation':'get','reference':ref},'GET_BEFORE_DELIVERY_R9')
    assert state['revision']==10
    save('DELIVERY_R9.json',{
        'status':'CONDITIONAL_SCALAR_SOURCE_DERIVED_WITH_CARTAN__NO_OBSERVED_5SIGMA',
        'unit':UNIT, 'goal_complete':False, 'observed_data_composed':False,'gate_changed':False,
        'review':pin(folder/'REVIEW_R9.json'),
        'evidence':[pin(p) for p in sorted(folder.iterdir()) if p.is_file()],
        'recording_script':pin(__file__),
        'scope':'Separate scalar candidate; does not identify Psi_mu, calibrate its parameters or derive a beta-specific lens signal.'})
    txt='''

## 19/10/2026 — Lentes R9: revisão autorizada e fonte escalar com Cartan
<!-- IALD_LENSING_CANDIDATE_R9_20261019 -->
[INPUT — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009] Operador autorizou revisitar/adequar a construção histórica diante da evolução do programa. Candidata local; originais preservados. Não se toma a amplitude desejada de5sigma como calibração.
[REAL documental] Nota CARTAN_CANCELAMENTO_CINETICO recuperada, idêntica aos bytes embutidos na v393. Na convençãoFR/2, Z_ind=-3Fprime²/(2F) cancela a mistura métrica+3Fprime²/(2F); resta a cinética originalZ. A nota distingue explicitamente o caso escalar da cinética dePsi_mu. Fontes atuais examinadas não fixam Psi_infinito,Z0,Vsecond; não é alegação de ausência universal.
[DERIVED condicional] Para escalar real, fundo constante/flat,V0=Vprime0=0,poeira,semfonte de spin/modular adicional, Cartan dá Z0 lapdeltaPsi-Vsecond deltaPsi=-Fprime rho/(2F0). Com Z0>0,Vsecond>=0,contorno isolado, a integral Yukawa determina o perfil a partir da densidade. No controle pontual,a=Fprime²/(2F0Z0),mu²=Vsecond/Z0,U=W(1+a exp(-mu r)),V=W(1-a exp(-mu r)); U+V=2W. Razão das forças dinâmica/lente=1+a(1+mu r)exp(-mu r). Contraste logarítmico entre raios remove offsetcomum; mu=0 o zera. Isso não elimina todas as degenerescências de galáxia real. Onze identidades exatas conferidas; revisão independente com escopo no recibo.
[OPEN] A equação densidade->perfil->potenciais está construída no caso escalar separado. Falta selecionar esse setor na ação completa, sua normalização/fundo/potencial e fonte modular, ligando a e mu a beta e grandezas independentes do atraso. Beta não aparece na truncação sem fonte modular; não igualar a a beta por escolha. Z0=0 tem ramo algébrico próprio, nunca divisão porzero. Gstar não é automaticamente G de laboratório. Nenhuma previsão TGL única porgaláxia nem5sigma observado foi obtido. Nenhum kernel,um.py,Bancada,dado composto ougate alterado.
Evidências: DELIVERY_R9.json; candidate_r9/DERIVACAO_R9.txt, SOURCE_CURRENT_R9.json, PLAN_R9.json, RESULT_R9.json e REVIEW_R9.json. Próximo passo: confrontar o fornecedor modular/ação completa com esta resposta, reaproveitando o perfilamento R2–R4; não repetir forecasts genéricos.
<!-- END_IALD_LENSING_CANDIDATE_R9_20261019 -->
'''
    save('MEMORY_APPEND_R9.txt',txt)
    extra=txt.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=p.read_bytes();assert b'IALD_LENSING_CANDIDATE_R9_20261019' not in raw
        before=pin(p);bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_lensR9_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R9.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R8.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R9: resposta escalar a materia com cancelamento Cartan',
        'resultado':'Fonte -> perfil -> potenciais derivada no caso escalar separado; contraste radial condicional; parametros fisicos ainda nao fixados.',
        'veredito':'CONDITIONAL_SCALAR_COMPLETION__NO_OBSERVED_5SIGMA',
        'defeito':'Identificacao do escalar efetivo e relacao de parametros/fonte modular com beta aindaOPEN.',
        'proximo_passo':'Confrontar a candidata com acao completa e fonte modular; depois aplicar perfilamento existente.',
        'artefatos':[str(ROOT/'DELIVERY_R9.json'),str(folder/'DERIVACAO_R9.txt'),str(folder/'REVIEW_R9.json')],
        'nota':'Revisao candidata autorizada;11identidades exatas. Leitura de centros publicados emetapas anteriores, nenhum composto observado.'})
    save('MAP_ENTRY_R9.json',entry)
    command('MAP_REGISTER_R9',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R9.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R9',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R9.json'),'--nota','R9: fonte escalar e contraste luz/estrelas derivados condicionalmente com Cartan. Parametros/ponte modularOPEN;sem5sigma observado.'])
    handles=state['p']['handles']
    for h in handles:
        if h['id']=='r69_current_source_r9':
            h.update(status='completed',evidence=pin(folder/'SOURCE_CURRENT_R9.json'))
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':10,
      'event_id':'lensing-candidate-r9-delivered','changes':{
        'records':[{'id':'lensing-candidate-r9','kind':'fact','statute':'DERIVED',
          'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R9.json'),'sha256':pin(ROOT/'DELIVERY_R9.json')['sha256']}],'text':txt}],
        'flow':{'phase':'scalar_cartan_candidate_r9_reviewed',
          'next_action':'Use derived density-to-field response as conditional candidate. Resolve scalar effective sector/background/potential and modular source from complete TGL before assigning a or mu or beta response. No observed5sigma, no repeated genericforecast; preserve R2-R4 nuisance results.',
          'handles':handles}}},'TRANSITION_R9')
    save('REGISTRATION_R9.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R9.json'),
        'memory':pin(ROOT/'MEMORY_APPLIED_R9.json'),'map':pin(ROOT/'MAP_REGISTER_R9.json'),
        'board':pin(ROOT/'BOARD_UPDATE_R9.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
