"""Custody of partial implementation; never declares the five requirements done."""
from setup_mission import ROOT,pin,save,UNIT
import json

def read(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8'))

if __name__=='__main__':
    for n in ['PROGRESS_R1.json','RELATORIO_PROGRESSO_R1.txt']:
        assert not (ROOT/n).exists(),n
    # The numeric overflow correction must receive its own distinct review first.
    review_names=['r1_systematics/REVIEW_R1_COMPONENT.json','REVIEW_BACKGROUND_R2.json',
                  'REVIEW_STATISTICS_R1.json','r5_operations/REVIEW_R5_R1.json']
    for n in review_names:
        r=read(n)
        assert r.get('status',r.get('verdict'))=='PASS_WITH_SCOPE',n
    report='''FASE 9 — PROGRESSO DA INTEGRAÇÃO, 19/10/2026
Unidade F3.INTEGRACAO_20261019. Em nome de codex-gerente-tgl.

RESULTADO CIENTÍFICO
[REAL documental] Nenhum composto observado V2, nenhum novo p observado ou sigma de cauda. O escore histórico V1 4,2837356 e o veredito INCONCLUSIVE_SYSTEMATICS não foram reclassificados. A auditoria anterior calculou separação nominal primária BG1 5,721408–6,623219 e sem Cefeidas 3,937917–4,395122. São desenho condicional, não medição nova nem garantia de detecção. Não somar testemunhas, sigmas ou evidências.

R1 — SISTEMÁTICAS
[REAL sintético/documental] Reaproveitados o builder conjunto e o gate escalar. Inventário de28pares e8mapas com consumidor que recusa pares omitidos, componentes OPEN, zero sem justificativa, unidades incompatíveis e matriz inadequada.24controles passaram; revisão distinta conferiu cobertura e fontes.
[OPEN] Correlacionar SN/Pantheon/âncoras entre leitores requer componentes publicados, catálogo admitido e mapas físicos. Pequena mudança deH0 ao remover uma covariância INTERNA não limita uma covariância ENTRE leitores. Uma matriz admitida individualmente não qualifica a caixa inteira nem impõe por si a regra lambda_N comum. Não substituímos lacunas por zero.

R2/R3 — FORNECEDOR FÍSICO E INCERTEZA
[REAL sintético] Ligado o fornecedor CAMB existente em cópia, com7chamadas/7retornos para pontos teóricos previamente fixados;16controles do adaptador. Nenhum solver foi repetido na revisão. Fonte H5 é BAO com rd livre, não uma cosmologia primordial genérica. CMB e redshift da lei permanecem explicitamente tipados. O K calculado no ponto sintético não substitui o K do escalar congelado.
[DERIVED/REAL sintético] Propagação comum J C_theta J^T, conferida independentemente por somas escalares; preserva correlação entre todos os leitores que compartilham os mesmos parâmetros. A primeira conferência do coordenador usou por engano a covariância dos observáveis, falhou e foi corrigida para a fonte C_theta do plano; resíduo6,94e-18. Nenhum resultado do fornecedor mudou. Sem covariância cosmológica admitida, a conclusão fica explicitamente condicional. Linearização sintética não certifica a marginalização não linear.
[OPEN] Integração da evidência sobre o prior físico completo e tratamento das compressões/fontes. O adaptador físico já permite abandonar o mock no desenvolvimento, mas esta entrega não calculou lnB físico nem qualifica todo o prior. Revisão posterior encontrou possibilidade de overflow com entradas finitas extremas; a versãoR2 ao lado recusa esse caso, preservando aR1.

R4 — CALIBRAÇÃO
[DERIVED] No modelo escalar com fatores uniformes e C fixa, o resíduo GLS perpendicular cancela. A comparação reduz exatamente a h~N(H_BG,v+s_BG^2) contra h~N(K H_BG,v+K^2 s_BG^2), v=(1^T C^-1 1)^-1. A cauda vem de uma quadrática gaussiana, não de assumir sqrt(DeltaQ) como sigma. Implementados p, equivalente normal e multiplicidade explicitamente separados.
[REAL sintético]38controles na primeira versão;4controles adicionais da correção de raízes naR2. Os38não foram apresentados como reexecutados naR2. Revisão distinta conferiu a derivação e a correção. A hipótese amostral é preditiva, com fundo gaussiano sorteado; marginalizar o fundo no código não demonstra cobertura uniforme para umH0 físico fixo desconhecido. Bonferroni exige família explicitada; cenário finito não substitui supremo contínuo. R4 integral permanece OPEN.

R5 — ADMISSÃO E EXECUÇÃO
[REAL sintético/documental] Consumidor de atoD-H pinado, ligado ao gate documental existente;17controles. Ausência de admissão resulta em PENDING_D_H e required_sources_admitted=false. Inventário inteiro: L1b eL6 continuam não verificados e não admitidos, n_alvos_declarados=2. O consumidor não fabrica o ato nem o autentica por hash; a autoridade chega de uma fonte confiável externa. X13/congelamento/abertura continuam atos separados.
[REAL sintético] Recusa de níveis de integração ausentes, não finitos e discordantes. A concordância entre refinamentos é diagnóstico, não cota rigorosa de erro; decisão próxima ao limiar exige orçamento de erro justificado. Nenhum resultado observado pode ser autorizado por esse diagnóstico.

PRÓXIMO TRABALHO
1. Resolver componentes residuais e mapas dos leitores por fonte/limite independente, conservando a regra comum das âncoras.
2. Integrar a likelihood física sobre o prior com erro controlado; manter a conclusão condicional enquanto a incerteza externa deK não estiver admitida.
3. Qualificar o modelo amostral real, os nuisances e a família de testes. Só então um p pode receber o rótulo5sigma.
4. Consumir os atos reaisD-H/X13 e a revisão/congelamento/abertura aplicáveis. Nenhum ato é presumido desta entrega.

Tudo novo fica em cópia; originais, um.py, kernel, Bancada e gate preservados. Sem ajustar parâmetros, covariâncias ou critérios ao resultado observado. PASS_WITH_SCOPE dos componentes não é aceitec1 nem conclusão dos cinco requisitos. Referência exata de continuidade: SESSION_REFERENCE.json nesta pasta.
'''
    save('RELATORIO_PROGRESSO_R1.txt',report)
    # Snapshot only the four finished component folders and coordinator reviews.
    names=review_names+['REVIEW_BACKGROUND_R1.json','STATISTICS_DELTA_REVIEW_R1.txt',
                       'review_background_r1.py','review_background_r2.py','review_statistics_r1.py','RELATORIO_PROGRESSO_R1.txt',
                       'OPERADOR_OBJETIVO.txt','SESSION_REFERENCE.json','CLAIM.json','HANDOFF.json',
                       'package_progress_r1.py']
    files={ROOT/n for n in names}
    for folder in ['r1_systematics','r2_background','r4_statistics','r5_operations']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    assert not any(p.suffix=='.pyc' or '__pycache__' in p.parts for p in files)
    requirements={
     'R1':{'status':'OPEN','completed':'Coverage contract and inventory; synthetic refusal controls',
           'remaining':'Published or independently bounded residual cross-reader systematics; observable maps; admissible covariance box'},
     'R2':{'status':'OPEN','completed':'Real supplier adapter and seven synthetic evaluations, H5 BAO-only free rd',
           'remaining':'Physical likelihood evidence integration and full prior accuracy qualification'},
     'R3':{'status':'CONDITIONAL_ONLY','completed':'Explicit fixed-theta scope and common linear propagation',
           'remaining':'Admitted cosmological covariance or nonlinear integral; no unconditional claim'},
     'R4':{'status':'OPEN','completed':'Exact scalar Gaussian reduction; analytic tails and explicit multiplicity API',
           'remaining':'Observed sampling model/nuisance coverage/frozen family/numerical error qualification'},
     'R5':{'status':'OPEN','completed':'Pinned admission consumer and numerical refusal contract; documentary gate connected',
           'remaining':'Actual acts, justified error budget, freezing/review and authorized opening'}}
    previous=ROOT.parent/'fase9_auditoria_20261019'/'DELIVERY_R1.json'
    save('PROGRESS_R1.json',{'unit':UNIT,'status':'MATERIAL_PARTIAL_PROGRESS__REQUIREMENTS_NOT_CLOSED',
         'requirements':requirements,'reviews':[pin(ROOT/n) for n in review_names],
         'previous_audit':pin(previous),'observed_V2_sigma':None,'five_sigma_demonstrated':False,
         'production_changed':False,'gate_changed':False,'parameters_tuned_to_observed':False,
         'new_provider_calls':0,'evidence':[pin(p) for p in sorted(files)]})
    print(json.dumps({'status':'PARTIAL_PROGRESS','receipt':pin(ROOT/'PROGRESS_R1.json'),'requirements':requirements},ensure_ascii=False))
