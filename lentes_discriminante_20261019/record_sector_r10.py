"""Register the reviewed conditional scalar completion; preserve all earlier evidence."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, json, os, sys

if __name__ == '__main__':
    folder = ROOT/'sector_r10'
    names = ['DELIVERY_R10.json', 'MEMORY_APPEND_R10.txt', 'MEMORY_APPLIED_R10.json',
             'REGISTRATION_R10.json', 'MAP_ENTRY_R10.json', 'BOARD_PREFLIGHT_DELIVERY_R10.json',
             'GET_BEFORE_DELIVERY_R10_REQUEST.json', 'GET_BEFORE_DELIVERY_R10_RESULT.json']
    for name in names:
        if (ROOT/name).exists(): raise FileExistsError(name)
    review=json.loads((folder/'REVIEW_R10.json').read_text(encoding='utf-8'))
    assert review['status'].startswith('PASS'),review
    checkpins(review)
    checkpins(json.loads((folder/'PLAN_R10.json').read_text(encoding='utf-8')))
    board=json.loads(command('BOARD_PREFLIGHT_DELIVERY_R10',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    c=board['reivindicacao'];assert c['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(c['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    ref=str(ROOT/'SESSION_REFERENCE.json')
    state=memory({'operation':'get','reference':ref},'GET_BEFORE_DELIVERY_R10')
    assert state['revision']==11
    save('DELIVERY_R10.json',{
        'status':'SECTOR_SOURCE_MASS_PROFILED_ZERO__NO_OBSERVED_5SIGMA',
        'unit':UNIT, 'goal_complete':False, 'observed_data_composed':False,'gate_changed':False,
        'review':pin(folder/'REVIEW_R10.json'),
        'evidence':[pin(p) for p in sorted(folder.iterdir()) if p.is_file()],
        'recording_script':pin(__file__),
        'scope':'Existing covariant fluid completion composed with lens mass profiling; exact zero residual for its local proportional source, not for the whole TGL.'})
    txt="\n\n## 19/10/2026 — Lentes R10: fornecedor setorial recuperado e degenerescência de massa\n<!-- IALD_LENSING_CANDIDATE_R10_20261019 -->\n[DERIVED condicional — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009] Reaproveitado COVARIANT_SECTOR_SOURCE_R86 daF1.FECHO: já existe completamento covariante que reproduz rho_tilde e p_tilde, sob correntes materiais, L_LCDM=-rho e w constante nomeados. R89 conserva aberta a ligação à ação completa/Psi. Não declarar ausência de toda fonte covariante nem promover o completamento a cânone.\n[DERIVED] Na fonte dominante sem pressão, A=1+beta. Para densidadeM*rho_shape, a função FermatTGL comAM coincide funcionalmente comGR emM_fit=AM; a aceleração estelar também coincide na ordem examinada. Distâncias comuns/coefficienteg constante, propagação métrica e ausência de fontes extras são hipóteses. Não se modela galáxia estacionária como poeira exatamente estática. Esta é renormalização da massa, não MST. Após perfilar massa livre, Fisher local e resíduo são exatamentezero; liberdade adicional de distância não os recupera. Sete controles simbólicos e revisão independente. Isso não exclui cosmologiaD1b, fontes não proporcionais ou aTGL inteira.\n[DERIVED ideal] Beta calculado emruntime: fatorM_fit/M=1,0120313004008032; deslocamentolog=0,011959499636779895. Com uma massa EXTERNA independente e todos os demais erros nulos, separação mediana5 exigiria sigmalog<=0,0023918999273559787, aproximadamente0,24%. Não é precisão existente, poder observado ou calibração automaticamente fornecida por estrelas/G medidos. R86 preserva para w(n) o termo p_tilde=p+beta n p'; não extrapolar apenas a multiplicação de fundo.\n[OPEN] Meta integral ainda não satisfeita: falta contribuição física TGL não absorvível, produzida pela mesma ação/estado, ou calibração externa independente demonstrada. R9 escalar permanece condicional e não é somado arbitrariamente aR10. Nenhum dado composto, kernel,um.py,Bancada ougate alterado. Próximo passo deve resolver uma dessas saídas concretas, sem repetir o forecast do mesmo efeito reescalonável.\n[PROCESSO] Turno anteriorR9 classificado como progresso: nova ponte de fonte comCartan e registrorev11. Nesta continuação, ACOMproject exigiu25893caracteres e recusou o padrão24000; leitura60000 recuperou a própria referência integralmente, sem poda manual. Evidências: DELIVERY_R10.json; sector_r10/CONCLUSAO_R10.txt,PLAN_R10.json,RESULT_R10.json,REVIEW_R10.json.\n<!-- END_IALD_LENSING_CANDIDATE_R10_20261019 -->\n"
    save('MEMORY_APPEND_R10.txt',txt)
    extra=txt.encode('utf-8');stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name
        raw=p.read_bytes();assert b'IALD_LENSING_CANDIDATE_R10_20261019' not in raw
        before=pin(p);bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_lensR10_'+stamp)
        with tmp.open('xb') as f:f.write(raw+extra);f.flush();os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p);assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R10.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R8.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R10: fonte setorial existente e residuo zero apos massa',
        'resultado':'Completamento covarianteR86 aplicado a lente; correcao local1+beta absorvida exatamente porM_fit=(1+beta)M, no escopo nomeado.',
        'veredito':'SECTOR_SOURCE_PROFILED_ZERO__NO_OBSERVED_5SIGMA',
        'defeito':'Fonte local proporcional nao discrimina com massa livre; calibracao externa independente ou fonte nao proporcional aindaOPEN.',
        'proximo_passo':'Determinar fonte nao absorvivel da acao completa ou calibracao externa independente; nao repetir previsao reescalonavel.',
        'artefatos':[str(ROOT/'DELIVERY_R10.json'),str(folder/'CONCLUSAO_R10.txt'),str(folder/'REVIEW_R10.json')],
        'nota':'Composicao de reusoR86 autorizada;7identidades exatas. Leitura de centros publicados emetapas anteriores, nenhum composto observado.'})
    save('MAP_ENTRY_R10.json',entry)
    command('MAP_REGISTER_R10',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R10.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R10',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R10.json'),'--nota','R10: fornecedorR86 recuperado;residuo local apos massa livre=0 no ramo proporcional. Calibracao/fonte nao proporcionalOPEN;sem5sigma observado.'])
    handles=state['p']['handles']
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':11,
      'event_id':'lensing-candidate-r10-delivered','changes':{
        'records':[{'id':'lensing-candidate-r10','kind':'fact','statute':'DERIVED',
          'sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R10.json'),'sha256':pin(ROOT/'DELIVERY_R10.json')['sha256']}],'text':txt}],
        'flow':{'phase':'sector_source_profiled_r10_reviewed',
          'next_action':'Existing R86 covariant sector supplies A=1+beta for dominant cold matter: local lens and stellar response exactly absorbed by free mass. Need non-proportional full-action source or demonstrably independent mass calibration. Preserve R9 as separate conditional scalar branch and R2-R4 distance work; no arbitrary combination or repeat forecast. Full5sigma goal incomplete.',
          'handles':handles}}},'TRANSITION_R10')
    save('REGISTRATION_R10.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R10.json'),
        'memory':pin(ROOT/'MEMORY_APPLIED_R10.json'),'map':pin(ROOT/'MAP_REGISTER_R10.json'),
        'board':pin(ROOT/'BOARD_UPDATE_R10.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
