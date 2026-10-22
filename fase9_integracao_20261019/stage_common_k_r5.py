"""Verify and package the documentary common-K qualification; no science run."""
from setup_mission import ROOT, pin, save
import json

def load(p):
    return json.loads(p.read_text(encoding='utf-8'))

def main():
    folder=ROOT/'r3_common_k_r5'
    evidence=[]
    for name in ['DELIVERY_COMMON_K_R5.json','DELIVERY_ADDENDUM_R5.json']:
        p=folder/name
        delivery=load(p)
        evidence.append(pin(p))
        for row in delivery['evidence']:
            assert pin(row['path'])['sha256']==row['sha256'],row['path']
            evidence.append(pin(row['path']))
    custody=load(folder/'SOURCE_CUSTODY_R5.json')
    anchors=0
    for row in custody['sources']:
        assert pin(row['path'])['sha256']==row['sha256'],row['path']
        from pathlib import Path
        lines=Path(row['path']).read_text(encoding='utf-8').splitlines()
        for a in row['anchors']:
            assert '\n'.join(lines[a['start']-1:a['end']])==a['text']
            anchors+=1
    review={'status':'PASS_WITH_SCOPE','reviewer':'/root','builder':'/root/r69_calibration_bridge',
      'source_count':len(custody['sources']),'anchors_verified':anchors,
      'checks':['Pointwise Gaussian positive-tail bound uses total SD envelope and null mean bound.',
      'For alpha<1 rejection implies confidence-set failure or true pointwise p <= alpha-gamma.',
      'Union bound does not require independence between confidence set and statistic.',
      'Common-set family correction pays gamma once and controls finite multiplicity by union.',
      'Covariance identity preserves common KH and covariance with H; no Gaussian mixture claim.',
      'Prior integration, grid maximum and posterior credibility are not coverage certificates.',
      'At f=1 K absent from this null contrast; this does not identify the historic score with it.'],
      'limits':['Analytic conditional contract, not Lean proof or implemented confidence procedure.',
      'No admitted physical sampling model, null bias bound, coverage or continuous supremum supplied.',
      'No new observed p/sigma; no provider or CAMB repeated.'], 'evidence':evidence}
    save('REVIEW_COMMON_K_R5.json',review)
    evidence.append(pin(ROOT/'REVIEW_COMMON_K_R5.json'))
    evidence.append(pin(ROOT/'r5_operations/ACTS_DELTA_R5.json'))
    note='''
<!-- IALD_FASE9_INTEGRACAO_20261019_R5 -->
19/10/2026 — codex-gerente-tgl, F3.INTEGRACAO_20261019, reivindicação1033.
[DERIVED condicional] Contrato K comum revisto: p_U=min(1,sup_C p_theta+gamma),
com cobertura uniforme1-gamma e p pontual válido, não exige independência.
Prior/credibilidade/grade não certificam cobertura/supremo. Covariância preditiva
E(Sigma_theta)+Cov(mu_theta) inclui Var(KH) e Cov(KH,H), sem inferir gaussianidade.
No contraste f=1 contraLCDM K afeta previsão/poder, não esse p nulo; isso não
requalifica o escore histórico. Região95% não basta para5sigma por esta fórmula.
[OPEN] Mapas físicos, viés nulo, cobertura, supremo e caudas reais permanecem abertos.
[REAL documental] Consulta focal ACTS_DELTA_R5 não localizou novos atos X13/D-H/d72/
abertura no recorte posteriorR3; não é busca universal. F3.4 segue resolvida.
CampanhaR4 tem handle próprio em andamento; este registro não afirma seu resultado.
Fontes/limites: work/fase9_integracao_20261019/PROGRESS_R5.json. Nada abre ou move gate.
<!-- END_IALD_FASE9_INTEGRACAO_20261019_R5 -->
'''
    for name in ['MEMORY_APPEND_R5.txt','RELATORIO_PROGRESSO_R5.txt']:
        with (ROOT/name).open('xb') as f:f.write(note.encode('utf-8'))
    summary='Contrato analítico de K comum e cobertura revisto; prior não vira cauda uniforme. Consulta focal de atos sem nova autorização. Nenhum sigma observado.'
    save('PROGRESS_R5.json',{'status':'PARTIAL_STATISTICAL_QUALIFICATION','summary':summary,
        'next_action':'Concluir e revisar campanhaR4; obter limites físicos e qualificação amostral, preservar atos pendentes antes de congelar/abrir.',
        'evidence':evidence,'observed_sigma':None,'all_requirements_complete':False})
    print(json.dumps({'status':'STAGED','sources':len(custody['sources']),'anchors':anchors,'progress':pin(ROOT/'PROGRESS_R5.json')}))

if __name__=='__main__':main()
