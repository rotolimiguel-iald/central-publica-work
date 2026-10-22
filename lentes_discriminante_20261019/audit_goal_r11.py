"""Audit the original lens goal without promoting conditional models to its solution."""
from setup import ROOT, UNIT, ACTOR, save, command
from record_trajectory_r2 import pin,checkpins
from pathlib import Path
import json,datetime,sys

if __name__=='__main__':
    folder=ROOT/'audit_r11';folder.mkdir(exist_ok=True)
    targets=['LITERATURE_R11.json','COMPLETION_AUDIT_R11.json','BLOCKED_AUDIT_R11.json','CONCLUSAO_R11.txt']
    for n in targets:
        if (folder/n).exists():raise FileExistsError(n)
    board=json.loads(command('BOARD_PREFLIGHT_AUDIT_R11',[sys.executable,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py','ver',UNIT]))
    c=board['reivindicacao'];assert c['quem']==ACTOR['id']
    assert datetime.datetime.fromisoformat(c['vence_em'])>datetime.datetime.now(datetime.timezone.utc)
    for n in [9,10]:
        d=json.loads((ROOT/f'DELIVERY_R{n}.json').read_text(encoding='utf-8'));checkpins(d)
        assert d['goal_complete'] is False
    source=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015\stationary_selection_r89\source\ACTION_EOM_RESIDUAL_R89.md')
    program=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
    literature={'scope':'Focused primary-source web inspection, not exhaustive literature review, not data admission or reproduced likelihood. Remote source bytes not custodied here.',
        'papers':[
         {'url':'https://arxiv.org/abs/1806.08300','title':'A precise extragalactic test of General Relativity',
          'read':'author abstract','finding':'Joint imaging and spatially resolved kinematics; gamma=0.97 +/-0.09. A potential-ratio test, not independent total-mass calibration at0.239%.',
          'inference':'A constant-gamma posterior is not automatically a likelihood for the radially varying scalar candidate.'},
         {'url':'https://link.springer.com/article/10.1140/epjc/s10052-026-15856-0','title':'Extragalactic test of general relativity with time-delay gravitational lenses',
          'read':'abstract and methodology/data sections; published14June2026',
          'finding':'Four H0LiCOW lenses plus BAO reconstruction; gamma=0.93 +0.16/-0.17, ratio route0.89 +0.19/-0.15. Paper identifies published distance PDFs/chains and preserved correlations.',
          'inference':'Public data exist; a mapping from the complete TGL to this observable is still required. These gamma errors are not mass errors or sigma_beta; no significance conversion performed.'},
         {'url':'https://arxiv.org/abs/1512.00462','title':'Strong Gravitational Lensing and the Stellar IMF of Early-type Galaxies',
          'read':'author abstract', 'finding':'Population synthesis and spectroscopy combined with lens masses for18galaxies; allowed IMF and dark-matter fractions discussed.',
          'inference':'This joint procedure is not evidence of a total-mass anchor independent of lens gravity at the required precision.'}],
        'failures':[{'url':'https://www.aanda.org/articles/aa/full_html/2025/02/aa53014-24/aa53014-24.html','status':'web tool internal fetch error'},
                    {'url':'https://www.aanda.org/articles/aa/full_html/2021/07/aa40549-21/aa40549-21.html','status':'403 Forbidden'}],
        'not_claimed':['No such calibration exists anywhere.','No lens data are public.','TGL is excluded.','A gamma discrepancy is a beta measurement.']}
    save('audit_r11/LITERATURE_R11.json',literature)
    requirements=[
      {'requirement':'Use existing authoritative TGL work and current program','status':'SATISFIED_FOR_BOUNDED_REVIEW','evidence':[pin(program),pin(source),pin(ROOT/'candidate_r9/SOURCE_CURRENT_R9.json')],
       'limit':'Source bytes and pinned deliveries checked; no new program run or canonical proof.'},
      {'requirement':'Obtain a physically normalized TGL prediction for each lens trajectory','status':'INCOMPLETE','evidence':[pin(ROOT/'candidate_r9/DERIVACAO_R9.txt'),pin(source)],
       'reason':'Scalar response is conditional on effective-field identification, background, kinetic/potential and modular source. These are not uniquely selected in the inspected full-action contract; arbitrary choices would define another completion.'},
      {'requirement':'Compute surviving signal after permitted mass and distance adjustments','status':'PARTIAL_WITH_NEGATIVE_BRANCH_RESULT','evidence':[pin(ROOT/'sector_r10/RESULT_R10.json'),pin(ROOT/'sector_r10/REVIEW_R10.json'),pin(ROOT/'DELIVERY_R4.json')],
       'reason':'Proportional local sector has exactly zero residual with free mass, even at shared fixed distances; other constructed branches preserve their narrower scopes. No complete TGL-specific non-proportional signal supplied.'},
      {'requirement':'A concrete independent calibration removes the relevant degeneracy','status':'NOT_ESTABLISHED','evidence':[pin(ROOT/'sector_r10/RESULT_R10.json'),pin(folder/'LITERATURE_R11.json')],
       'reason':'Ideal0.23919% external log-mass benchmark is not a measured calibration. Joint gravitational mass inference is not automatically independent.'},
      {'requirement':'Pre-register and evaluate an admissible observed discriminant at5sigma','status':'NOT_DONE','evidence':[pin(ROOT/'DELIVERY_R10.json')],
       'reason':'No full fixed observable law, no observed likelihood composed, no observed5sigma. Reported gamma posteriors are not substitute beta tests.'},
      {'requirement':'Preserve originals, gate and previous work; document genuine remaining gap','status':'SATISFIED_IN_DELIVERIES','evidence':[pin(ROOT/'REGISTRATION_R9.json'),pin(ROOT/'REGISTRATION_R10.json')]}]
    save('audit_r11/COMPLETION_AUDIT_R11.json',{'objective':'Derive TGL lens time-delay prediction per trajectory and its identifiable residual after mass/distance fits toward5sigma.',
      'goal_complete':False,'requirements':requirements,'audit_script':pin(__file__)})
    blocked={'same_blocking_condition':'No uniquely specified physically normalized full-TGL lens observable with a nonzero residual after allowed nuisance fits, nor an independently calibrated mass anchor for the proportional branch.',
       'resumed_turns':[
        {'turn':'R9, user-authorized resumption','classification':'PROGRESS','evidence':pin(ROOT/'DELIVERY_R9.json'),
         'remaining_blocker':'Conditional scalar source derived; its physical parameters/complete-action map remain open.'},
        {'turn':'R10, automatic continuation','classification':'PROGRESS','evidence':pin(ROOT/'DELIVERY_R10.json'),
         'remaining_blocker':'Existing covariant proportional source gives zero identifiable residual; external calibration not established.'},
        {'turn':'R11, current continuation','classification':'PROGRESS_IN_AUDIT_AND_DATA_ROUTE_CHECK','evidence':pin(folder/'COMPLETION_AUDIT_R11.json'),
         'remaining_blocker':'Unchanged source contract and public observable checks do not fix the missing transfer or independent mass calibration.'}],
       'live_execution_wait':False,
       'safe_actions_exhausted_for_current_contract':['Reused and checked historical amplitudes/profiles; conditional source response; existing covariant sector; mass/distance profiling; focused public data/calibration check.',
            'Another arbitrary scalar parameter choice or generic forecast would not make the requested fullTGL prediction determined.'],
       'unblock_conditions':['A concrete full-action representation/source or additional physical relation fixes the non-proportional lens response without fitting target delays.',
            'A documented independent mass calibration with its uncertainty and theory dependence is available to test the existing proportional branch.'],
       'decision':'BLOCKED_NOT_COMPLETE','scope_limit':'Not a proof that no future construction or dataset can resolve the problem; current mission lacks the required physical input.'}
    save('audit_r11/BLOCKED_AUDIT_R11.json',blocked)
    save('audit_r11/CONCLUSAO_R11.txt','''Auditoria da meta de lentes — R11,19/10/2026, codex-gerente-tgl.
A meta integral não foi atingida. R9 e R10 são progresso verdadeiro e permanecem reutilizáveis; não substituem a previsão física completa.
O mesmo impedimento persistiu nas três etapas desde a retomada autorizada: o ramo com parâmetros físicos determinados aqui é absorvido pela massa, e o ramo que pode mudar a forma depende de uma identificação/normalização física ainda não fornecida. O programa corrente e o diagnóstico funcionalR89 permanecem com os mesmos bytes.
Há dados públicos para testes de potenciais gravitacionais. A consulta primária em LITERATURE_R11 identifica esses trabalhos e seus escopos; não demonstra uma calibração independente de massa a0,239% nem uma previsão de gamma para a TGL completa. Não há composto observado,5sigma ou confirmação nesta missão.
O bloqueio é do contrato físico necessário para calcular a previsão solicitada. Repetir modelos condicionais escolhendo a amplitude ou somar previsões de ramos diferentes não resolve esse bloqueio. A retomada requer uma relação física adicional verificável ou uma calibração externa independente documentada, conforme BLOCKED_AUDIT_R11.
Nenhuma execução pendente exige espera. Nenhum original científico,kernel,um.py,Bancada ougate foi alterado. A biblioteca de cálculos e o histórico permanecem preservados; unidade não é declarada FECHADA.
''')
    print(json.dumps({'status':'AUDIT_COMPLETE_GOAL_NOT_ACHIEVED','blocked_audit':pin(folder/'BLOCKED_AUDIT_R11.json')},ensure_ascii=False))
