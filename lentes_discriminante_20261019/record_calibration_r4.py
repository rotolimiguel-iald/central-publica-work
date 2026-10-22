"""Additive record of conditional R4 calibration; no scientific installation."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, os, sys, json

if __name__ == '__main__':
    folder=ROOT/'calibration_r4'; ref=str(ROOT/'SESSION_REFERENCE.json')
    for name in ['DELIVERY_R4.json','MEMORY_APPEND_R4.txt','MEMORY_APPLIED_R4.json','REGISTRATION_R4.json']:
        if (ROOT/name).exists(): raise FileExistsError(name)
    review=json.loads((folder/'REVIEW_R4.json').read_text(encoding='utf-8'))
    assert review['status']=='PASS_WITH_SCOPE'; checkpins(review)
    survey=json.loads((folder/'KINEMATIC_SOURCE_SURVEY_R4.json').read_text(encoding='utf-8'))
    checkpins(survey)
    board=json.loads(command('BOARD_PREFLIGHT_R4',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    claim=board['reivindicacao']; assert claim['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    state=memory({'operation':'get','reference':ref},'GET_BEFORE_R4'); assert state['revision']==4
    save('DELIVERY_R4.json',{'status':'DERIVED_CONDITIONAL_REVIEWED_NO_OBSERVED_5SIGMA','unit':UNIT,
        'goal_complete':False,'observed_data_composed':False,'gate_changed':False,
        'review':pin(folder/'REVIEW_R4.json'),
        'source_survey_scope':'Documentary retrieval; not a new physical calibration or proof of absence in the entire corpus.',
        'evidence':[pin(p) for p in sorted(folder.rglob('*')) if p.is_file()], 'recording_script':pin(__file__)})
    txt='''

## 19/10/2026 — Lentes R4: calibração comum e contraste complementar
<!-- IALD_LENSING_CALIBRATION_R4_20261019 -->
[DERIVED condicional — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação 1009] Perfilada a hipótese escalar existente em modelo gaussiano no log: y_i=a logK+h-m_comum-m_i+e_i. A escala comum da folha de massa ou o fundo inteiramente livres apagam o sinal. Transformação de Fermat verificada simbolicamente: diferenças escalam por lambda. Na realização nomeada Ddt_TGL=Ddt_bg/K, uma alternativa com lambda=1/K=0,922673352975 reproduz imagens/atrasos, sem afirmar que reproduz cinemática. Não é erro de massa total medido em uma lente.
[DERIVED sintético] Z_A=logK/sqrt[(sigma_e²+sigma_ind²)/N+sigma_comum²+sigma_bg²], K calculado em runtime, BG1 do draft. Com escolhas INPUT de 4% e 3% individuais, piso comum de 1% pede 18 sistemas para mediana5 e 56 para poder unilateral90%; piso de 2% limita Z a3,930 mesmo quando N cresce. O piso comum deve ficar abaixo de1,5485% no log para Nfinito permitir mediana5; se a média independente tem erro1%, limite1,1823%. Não são precisões medidas. Publicações de H0 não foram reutilizadas como erro cru, evitando dupla contagem.
[REAL computacional / DERIVED alcance] Trinta cenários conferidos por revisão independente; mínimos quadrados e fórmula analítica concordam a5,69e-14 em chi². Controle da leitura positiva e negativa: copiar y para (y,-y), com covariância correta, mantém o posto11 e chi²18,6892832557, sem ganho artificial de significância. A cunhagem binária orienta correspondência/exclusão; não fornece sozinha um segundo dado independente.
[OPEN] A calibração real exige relacionar o potencial dos fótons ao das estrelas e ao mesmo relógio/distância. Levantamento específico pinado em calibration_r4/KINEMATIC_SOURCE_SURVEY_R4.json; a relação de massa linear da fonte é condicional a Face C+T1 e não autoriza inventar desvio PPN de ordem beta. Resultados históricos de razões de atraso não substituem a verificação MST. Fontes recuperadas não são execução nem nova lei por trajetória. R3 e R4 usam modelos gaussianos diferentes (linear e log), não somáveis. Nenhum dado observado, programa, kernel, Bancada ou gate alterado; meta5sigma ativa.
Evidência: DELIVERY_R4.json; calibration_r4/RESULTADO_CALIBRACAO_R4.md, PLAN_R4.json, RESULT_R4.json, RUN_R4.json, REVIEW_R4.json. Revisão PASS_WITH_SCOPE; não creditação.
<!-- END_IALD_LENSING_CALIBRATION_R4_20261019 -->
'''
    save('MEMORY_APPEND_R4.txt',txt)
    extra=txt.encode('utf-8'); stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'); rows=[]
    for name in ['TGL_ATLAS.md','TGL_INDICE_VIVO.md','DIARIO_CONSTRUCAO_QG.md']:
        p=Path(r'C:\IALD\Central de Patentes\memory')/name; raw=p.read_bytes()
        assert b'IALD_LENSING_CALIBRATION_R4_20261019' not in raw
        before=pin(p); bak=p.with_name(p.name+'.bak_'+stamp)
        with bak.open('xb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes()==raw
        tmp=p.with_name(p.name+'.tmp_lensR4_'+stamp)
        with tmp.open('xb') as f: f.write(raw+extra); f.flush(); os.fsync(f.fileno())
        assert tmp.read_bytes()==raw+extra and p.read_bytes()==raw
        os.replace(tmp,p); assert p.read_bytes()==raw+extra
        rows.append({'before':before,'backup':pin(bak),'after':pin(p),'pure_append':True})
    save('MEMORY_APPLIED_R4.json',rows)
    entry=json.loads((ROOT/'MAP_ENTRY_R3.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Lentes R4: perfilamento da escala de massa e piso comum',
        'resultado':'MST absorve escala sem calibracao; modelo log-Gauss exige piso comum abaixo1,5485percent para mediana5. Contraste positivo/negativo deterministico nao duplica informacao;30cenarios revisados.',
        'veredito':'NO_OBSERVED_5SIGMA__CALIBRATION_REQUIREMENT_DERIVED',
        'defeito':'Ponte fisica de trajetoria/likelihood e calibracao real dos potenciais continuam OPEN.',
        'proximo_passo':'Rastrear o funcional historico xi integral |Psi|² e sua relacao com a acao e o campo estelar; Face C+T1 condicional. Nao repetir forecasts sem premissa nova.',
        'artefatos':[str(ROOT/'DELIVERY_R4.json'),str(folder/'RESULTADO_CALIBRACAO_R4.md'),str(folder/'KINEMATIC_SOURCE_SURVEY_R4.json')],
        'nota':'R4 sintetica nao e numero observado; widths comuns em log, K fixo e calibracoes independentes INPUT.'})
    save('MAP_ENTRY_R4.json',entry)
    command('MAP_REGISTER_R4',[sys.executable,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',str(ROOT/'MAP_ENTRY_R4.json'),'--quem',ACTOR['id']])
    command('BOARD_UPDATE_R4',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','avancar',UNIT,'--quem',ACTOR['id'],'--status','EM_CURSO','--evidencia',str(ROOT/'DELIVERY_R4.json'),'--nota','R4 sintética revisada: piso de calibracao de massa quantificado, sem dado discriminante observado. Fonte cinematica recuperada com alcance condicional.'])
    out=memory({'operation':'transition','reference':ref,'actor':ACTOR,'expected_revision':4,'event_id':'lensing-calibration-r4-delivered','changes':{
        'records':[{'id':'lensing-calibration-r4','kind':'fact','statute':'DERIVED','sources':[{'kind':'artifact','ref':str(ROOT/'DELIVERY_R4.json'),'sha256':pin(ROOT/'DELIVERY_R4.json')['sha256']}],'text':txt}],
        'flow':{'phase':'calibration_r4_reviewed','next_action':'Use KINEMATIC_SOURCE_SURVEY_R4 and ADENDO_FONTES_R4 to trace historical xi integral |Psi|² delay: field identity, normalization, same-action stellar potential. Compare with R2 action and Face C+T1. Full physical lens likelihood remains OPEN; no repeated forecasts or observed verdict.','handles':[]}}},'TRANSITION_R4')
    save('REGISTRATION_R4.json',{'status':'PASS','delivery':pin(ROOT/'DELIVERY_R4.json'),'memory':pin(ROOT/'MEMORY_APPLIED_R4.json'),'map':pin(ROOT/'MAP_REGISTER_R4.json'),'board':pin(ROOT/'BOARD_UPDATE_R4.json'),'acom':out})
    print(json.dumps({'status':'PASS','receipt':out},ensure_ascii=False))
