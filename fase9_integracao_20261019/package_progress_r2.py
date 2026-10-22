"""Custody of the R2 partial result after distinct component review."""
from setup_mission import ROOT,UNIT,pin,save
from pathlib import Path
import json,sys
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
    terminal_review=Path(sys.argv[1]).resolve()
    if not terminal_review.is_relative_to(ROOT):raise ValueError('REVIEW_OUTSIDE_WORK')
    reviews=[ROOT/'REVIEW_ENVELOPE_R1.json',ROOT/'REVIEW_PIVOT_R2.json',ROOT/'REVIEW_DESIGN_R2.json',
             ROOT/'r5_source_completion/REVIEW_COMPANION_R2.json',terminal_review]
    for p in reviews:
        r=read(p)
        expected='PASS_WITH_SCOPE_NUMERICAL_INCONCLUSIVE' if p==terminal_review else 'PASS_WITH_SCOPE'
        if r.get('status',r.get('verdict'))!=expected:raise ValueError('REVIEW_STATUS_MISMATCH: '+str(p))
    full=read(ROOT/'r2_full_integration/DELIVERY_FULL_R2.json')
    assert full['recovery']['aggregate_unique_CAMB_calls']==125
    assert full['refinement']['indicator_satisfied'] is False
    assert full['sigma'] is None and full['observed_lnB'] is None
    report='''FASE 9 — AUDITORIA E INTEGRAÇÃO R2, 19/10/2026
Em nome de codex-gerente-tgl. Unidade F3.INTEGRACAO_20261019; reivindicação1033.

RESPOSTA CIENTÍFICA
Ainda não há novo sigma observado. O 4,2837356 histórico e seu INCONCLUSIVE_SYSTEMATICS permanecem como estavam. A rodada presente verifica contratos, fontes e execução sintética. Nenhum centro local foi composto e nenhum parâmetro teórico foi ajustado ao dado.

SISTEMÁTICAS E POTENCIAL PARA5SIGMA
[DERIVED] Envelope PSD com variâncias marginais totais corretas: sup_C w^T C w=(sum |w_i| sigma_i)^2. O desenho minimax de soma de pesos1 tem variância sigma_min^2; selecionar só pelo menor erro é candidato de desenho, não alteração da primária oficial. A cota GLS do acervo vale para a covariância correta conhecida; não se transfere a pesos congelados numa matriz incorreta.
[DERIVED condicional] Para local−f*fundo, correlações local–BG irrestritas dão SE_max=sum|w_i|sigma_i+|f|sigma_BG. f=1 testa o nulo LCDM; f=K testa compatibilidade TGL. No desenho conservador com BG1, f=1 dá separação nominal4,282915 se todas essas correlações forem desconhecidas, e5,304778 sob independência local–BG nomeada. O primeiro número NÃO reproduz o histórico4,28; é coincidência numérica entre objetos diferentes. Os números5,72–6,62 anteriores usam outra caixa/desenho e não foram substituídos por uma medição.
[DERIVED condicional] A separação5,304778 significa poder~61,97% para ultrapassar limiar unilateral5, sob Gaussianidade e mesma variância no nulo/alternativa. Para90% neste desenho independente, sigma_local precisaria<=0,863361, contra1,04 atual. Sem hipótese sobre correlação local–BG, nominal5 requer sigma_local<=0,847678. São requisitos de planejamento, não novas medições nem mudança de amostra. K está fixo neste cálculo; incerteza cosmológica pertence à integração física.
[OPEN] Erros marginais completos, vieses, mapas físicos e hipóteses amostrais. Um viés comum irrestrito pode reproduzir a média TGL sem alterar a covariância: IDENTIFICABILIDADE_E_MAPAS_R2.txt explica o alcance. Limitar correlação não limita viés. O orçamento0,329978 limita uma redução adversa da separação alternativa nominal; não controla viés no nulo.

ESTATÍSTICA
[DERIVED] Pivô candidato Z_f=(w^T X−fB)/sqrt(w^T C w+f²s_B²−2f w^T d), com soma(w)=1, cancela H0 desconhecido sob modelo conjunto Gaussiano e erros conhecidos. Não requer sortear H0 de um prior para essa propriedade. A covariância cruzada d é explícita: ausente não vira zero. Compatibilidade bilateral TGL e rejeição unilateral LCDM são distintas, dependentes e não se somam. Família/multiplicidade precisam ser fixadas; sqrt(DeltaQ) antigo não foi reclassificado.
[REAL sintético]26controles do pivô passaram. Revisão distinta encontrou overflow no auxiliar de poder; versãoR2 nova, quatro controles focais e revisão separada corrigiram/refusaram a faixa. Os26 não foram repetidos. Prova analítica ao lado liga o envelope a p conservador sob Gaussianidade/médiazero, sem reclamar cobertura para viés ou caudas arbitrárias.

EXECUÇÃO FÍSICA
[REAL sintético] Reaproveitados os contratos conjuntos ORDEM018, fornecedor CAMB real, cinco modelos,283componentes e63nuisance, prior completo em(H0,ombh2,omch2). A primeira execução parou após dois retornosCAMB porque normalization.log_prefactor era np.float64. Falha preservada; camadaR2 converte só esse campo, com igualdade binária, após revisão distinta. Recuperação reutilizou os dois pontos e acrescentou123; total125únicos, sem repetir solver concluído/incerto. Exit0,30,04s científicos.
[REAL diagnóstico] A integral não passou na regra de refinamento: diferençaslogZ de0,183199 a0,312583, tolerância0,01. Logo INCONCLUSIVE; nenhuma preferência física deve ser extraída dos números intermediários. A concordância eventual de duas grades seria diagnóstico, não certificado rigoroso de erro. Serviços internos não registraram underflow nem falha de convergência.
[DERIVED/REAL sintético] Mesmo theta alimenta todos os leitores e modelos. Beta é fixo em runtime e K varia na grade1,0801894..1,0878974. Esse intervalo é de uma grade de prior, não intervalo de confiança observado. H5 continua BAO com rd livre, preservando CMB; não é toda cosmologia precoce. Esta ligação é da testemunha CONJUNTA, não execução do escalarV2. MM continua CONDITIONAL_UNRATIFIED.

FONTES E EXECUÇÃO SEGURA
[REAL documental] Bytes públicos novos de arXiv2509.01667v1 e LIGO-P2400152-v10/O4a foram guardados e verificados com âncoras únicas. Novo companion liga L1b eL6 ao gate existente, sem alterar spec/vínculo antigos.10controles e revisão distinta; n_alvos_declarados2→0 somente nessa extensão candidata. D-H continua pendente e required_sources_admitted=false; nada foi admitido pelo operador nesta etapa.
[KNOWN na fonte / DERIVED na compressão] L6 publica mediana e intervalo de credibilidade68,3% assimétrico, não sigma amostral. A média dos dois lados reproduz a compressão11,25 do rascunho, sem validar Gaussianidade ou independência. Mapas físicos L1b/L6 permanecemOPEN, como os demais. L1b é substituto de réplica, nunca somado comL1.

O QUE AINDA FALTA
1. Qualificar os mapas e os erros/vieses totais, além de justificar/limitar a covariância local–BG. O envelope oferece alternativa conservadora que paga em sensibilidade; não fabrica informação física.
2. Obter erro de integração controlado no prior. Próxima grade/campanha precisa de plano próprio que reutilize125pontos por identidade física, sem mudar prior, dados, tolerância ou resultado alvo.
3. Validar a lei amostral/caudas, a multiplicidade e a comparação com alternativas físicas. Um nulo rejeitado com TGL compatível não identifica sozinho a TGL entre todas as alternativas.
4. Consumir atosD-H/X13 e revisão/congelamento/abertura aplicáveis. d72 e testemunhas preservam seus contratos. Nenhum ato foi presumido.

ARTEFATOS
PROGRESS_R2.json contém pinos e requisitos; recibos completos em r1_envelope, r4_pivot, r5_source_completion e r2_full_integration. Revisões são de componentes com escopo, não aceitec1 da unidade. ACOM própria SESSION_REFERENCE.json. Nenhum um.py, kernel, Bancada de produção ou gate alterado. Os resultados anteriores permanecem intactos.
'''
    save('RELATORIO_PROGRESSO_R2.txt',report)
    note='''\n\n## 19/10/2026 — Fase9: envelope, pivô e integral física sintética R2
<!-- IALD_FASE9_INTEGRACAO_20261019_R2 -->
[REAL/DERIVED — em nome de codex-gerente-tgl; F3.INTEGRACAO_20261019, reivindicação1033] Envelope PSD de todas correlações com diagonais corretas e pivô Gaussiano que elimina H0 fixo, sob hipóteses nomeadas.13controles do envelope;26do pivô e4focais após overflow corrigido em arquivo novo, sem repetir26. Separação nominal conservadora f=1:4,282915 com cross local–BG livre;5,304778 com independência nomeada. Não é sigma observado; coincidência com histórico4,28 não significa reprodução. Poder condicional~61,97%, não certeza5sigma.
[REAL documental] Fontes exatasL1b/L6 custodiadas, companionnovo com10controles: n_declared2→0 só no candidato; D-Hfalse, mapasOPEN. L6 é intervalo posterior assimétrico; compressãoGaussiana não qualificada.
[REAL sintético] Testemunha conjunta:125pontosCAMBúnicos (2retornos recuperados+123novos),5modelos,283linhas/63nuisance,theta marginalizado; exit0,30,04s. R1falhou no transportefloat64 e permanece custodiada; reparo binário exato revisado. DiferençaslogZ0,183..0,313>.01: INCONCLUSIVE. Kgrid1,0801894..1,0878974 não éICobservado. Beta fixo; nenhum ajuste ao dado. Revisões distintas de componentes, sem aceitec1 integral.
[OPEN] Mapas/erros/vieses, covariância física, erro de integração, calibração real/multiplicidade, atos e revisão antes de congelar/abrir. Viés comum não é limitado por covariância. HistóricoV1 e gateintactos; nenhum compostoV2/observado/provedor/produção. Reutilizar125pontos e todosrecibos, não repetir por compactação.
Entrega parcial: work/fase9_integracao_20261019/PROGRESS_R2.json e RELATORIO_PROGRESSO_R2.txt; referência própriaSESSION_REFERENCE.json. Os cinco requisitos seguem sem fecho integral.
<!-- END_IALD_FASE9_INTEGRACAO_20261019_R2 -->
'''
    save('MEMORY_APPEND_R2.txt',note)
    next_action='Reuse PROGRESS_R2, exact125 CAMB packets and terminal receipts. Plan numerical refinement with fixed priors/tolerance; qualify physical maps/bias/total errors and local-background covariance. Calibrate real sampling/multiplicity. No observed composite/freeze without recorded acts. Do not repeat completed solver calls.'
    names=['RELATORIO_PROGRESSO_R2.txt','MEMORY_APPEND_R2.txt','IDENTIFICABILIDADE_E_MAPAS_R2.txt',
        'DESIGN_PLAN_R2.json','DESIGN_REQUIREMENTS_R2.json','design_requirements_r2.py','package_progress_r2.py',
        'register_progress_r2.py','PROGRESS_R1.json','REGISTRATION_R1.json']
    files=set(ROOT/n for n in names)|set(reviews)
    for folder in ['r1_envelope','r4_pivot','r5_source_completion','r2_full_integration']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    assert not any('__pycache__' in p.parts or p.suffix=='.pyc' for p in files)
    summary='Envelope/pivô/fontes qualificados em escopo;125CAMB sintéticos e5modelos ligados, mas refinamento .183.. .313>.01 inconclusivo. Nenhum sigma observado novo; mapas/erros/calibração/atos abertos.'
    save('PROGRESS_R2.json',{'unit':UNIT,'status':'PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA','summary':summary,
        'next_action':next_action,'requirements':{'R1':'OPEN_PHYSICAL_MAPS_BIAS_TOTAL_ERRORS','R2':'CONNECTED_NUMERICAL_INTEGRATION_INCONCLUSIVE',
        'R3':'COMMON_THETA_MARGINALIZATION_SYNTHETIC_NOT_NUMERICALLY_QUALIFIED','R4':'CONDITIONAL_GAUSSIAN_PIVOT_REAL_SAMPLING_OPEN',
        'R5':'DOCUMENTARY_EXTENSION_COMPLETE_ACTS_OPEN'},'new_observed_sigma':None,'five_sigma_demonstrated':False,
        'parameter_tuning_to_data':False,'production_changed':False,'gate_changed':False,
        'reviews':[pin(p) for p in reviews],'evidence':[pin(p) for p in sorted(files)]})
    print(json.dumps({'receipt':pin(ROOT/'PROGRESS_R2.json'),'artifacts':len(files),'summary':summary},ensure_ascii=False))
if __name__=='__main__':main()
