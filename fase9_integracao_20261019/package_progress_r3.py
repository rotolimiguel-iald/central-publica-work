"""Package reviewed R3 components; no observed inference or scientific acceptance."""
from setup_mission import ROOT,UNIT,pin,save
import json
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def main():
    delivery=ROOT/'r2_refinement_r3/DELIVERY_REFINEMENT_R3.json'
    terminal_review=ROOT/'r2_refinement_r3/REVIEW_TERMINAL_R3.json'
    reviews=[ROOT/'REVIEW_MAPS_R3.json',ROOT/'REVIEW_ROBUST_TAIL_R3.json',terminal_review]
    for path in reviews:
        r=read(path)
        if not str(r.get('status',r.get('verdict',''))).startswith('PASS_WITH_SCOPE'):
            raise ValueError('Independent scoped review required: '+str(path))
    d=read(delivery)
    assert d['sigma'] is None and d['observed_lnB'] is None
    assert d['recovery']['aggregate_unique_CAMB_calls']==729
    report=f'''FASE 9 — PROGRESSO R3, 19/10/2026
Em nome de codex-gerente-tgl, F3.INTEGRACAO_20261019, reivindicação1033.

Não há novo sigma observado. A camada atual reaproveita contratos e recibos R1/R2,
qualifica execução sintética e torna explícitos os mapas e as sistemáticas restantes.

1. MAPAS FÍSICOS [DERIVED condicional / REAL documental]
Os artigos já fornecem expansão e distâncias. O teorema de contraste fornece K no
contrato da taxa; não se refaz essa derivação. A leitura das onze fontes distinguiu
o fundo efetivo e a lei acumulada do canal de luminosidade, sem multiplicá-los como
dois efeitos independentes. Hraw(0)=Hbare sqrt(S) no fecho nu; o argumento H0 da
rotina não é automaticamente a taxa física presente. Isso já está na auditoria de
lentes e foi reaproveitado, não é uma alteração do programa.

Para um objeto com distância e redshift fixos, o consumidor dá
Hfit/Hphys=Iref/Igeo. Sob a promoção angular adicional já nomeada na ORDEM018,
Hfit/HBG=K*/Q(z), Q=(integral E^(nu-1))/(integral1/E), nu=2beta/3.
Se E é positiva/crescente e E(0)=1, 1<=Q<=E(z)^nu. Essa cota não usa centros.
A promoção angular não é consequência automática de um mapa de luminosidade.
Falta demonstrar a invariância ou transportar a likelihood do disco maser, seus
priors/latentes/velocidades e seleção. Para vários redshifts não há correção escalar
única sem prova. Lentes e sirenes também precisam do próprio contrato de observação.
A pasta v394_r12 contém um snapshot que declara v393: nenhum selo v394 foi inferido
do nome da pasta. Esta revisão de fontes não atesta a versão atualmente implantada.

2. CORRELAÇÕES E VIÉS [DERIVED / REAL sintético]
Novo consumidor reutiliza o envelope PSD, incluindo correlação local–fundo:
smax=sum|w_i|sigma_i+|f|sigma_BG. Para D=w'X-fB e média nula<=b, sob normalidade
conjunta, p<=SF((D-b)/smax) quando D>b; usa p=1 quando D<=b.
O p conservador é superuniforme dentro dessas hipóteses. Bonferroni trata uma família
finita previamente fixada sem exigir independência entre testes. O viés b é limite
de média, não covariância e não erro acrescentado em quadratura.
Ausência de b é recusada. b=0 continua hipótese que exige fundamento externo.
36 verificações analíticas sintéticas, oito recusas e revisão distinta passaram.
O cálculo erfc é float64; a prova analítica não vira certificado intervalar numérico.
Não se transporta essa calibração para K estimado/correlacionado, caudas arbitrárias,
pesos escolhidos pelos centros ou erros marginais incompletos.

3. EXECUÇÃO COSMOLÓGICA [REAL sintético]
Nova campanha pré-pinada: refinamento5³→9³, mesmo prior, mesma média sintética,
mesma covariância e modelos, mesmos critérios.125 resultados preservados por
equivalência completa dos inputs físicos,604 chamadas novas,729 únicos. A ponte
do cache conserva recibos originais; não falsifica a identidade da configuração.
Pré-revisão detectou contagens antigas no runner; correção R3A aditiva antes de rodar.
Tempo científico: {d['recovery']['seconds_scientific']:.3f}s; exit0.
Resultado: {d['status']}.
Refinamento registrado: {json.dumps(d['refinement'],ensure_ascii=False)}
Qualificação interna: {json.dumps(d['conditional_precision_summary'],ensure_ascii=False)}
Este é o executor conjunto283linhas, cinco modelos, um cenário sintético, não uma
abertura do escalarV2 nem a d72. K varia com theta compartilhado; seu intervalo na
grade não é intervalo de confiança. H5 continua BAO com rd livre, não todo fundo
cosmológico alternativo. Mesmo eventual concordância de grades é diagnóstico e
não prova global do erro integral/CAMB ou calibração física de caudas.

4. O QUE OS NÚMEROS PERMITEM DIZER
Os desenhos R2 continuam condicionais: separação nominal5,304778 sob independência
local–fundo e erros totais corretos;4,282915 permitindo toda correlação cruzada.
São desenhos conservadores diferentes do histórico4,2837356. Não são nova medição.
No desenho gaussiano independente a chance calculada de ultrapassar5 é~61,97%,
não90% nem certeza. Viés não limitado impede extrair significância física desse
contraste, mesmo com grande separação nominal. Não baixar limiar depois de ver dado.

5. ATOS E PRÓXIMA ETAPA
Snapshot do quadro custodiado: F3.4FECHADA; F3.1/F3.2AUDITADAS; F3.3PROPOSTA;
F3.5AGUARDA_OPERADOR. X13 permanece na lista consultada. Esta busca delimitada não
é prova de inexistência de ato em todo o acervo. Nenhum D-H autenticado foi fornecido
ao consumidor candidato. Verificação documental não fabrica admissão.
Reutilizar729 resultados. Resolver erro numérico sem relaxar tolerância; transportar
ou limitar mapas instrumentais e vieses; qualificar a distribuição amostral real e
comparações alternativas. Só então cumprir revisão/atos antes de congelar/abrir.

Originais, um.py, kernel, Bancada de produção e gate intactos. As revisões distintas
são de componentes, não aceitec1 integral. Arquivos novos preservam a história.
'''
    save('RELATORIO_PROGRESSO_R3.txt',report)
    summary='Mapas de distância explicitados; cauda conservadora com viés nomeado revisada;729CAMB sintéticos únicos. '+d['status']+'. Sem novo sigma observado.'
    next_action='Reuse all729 CAMB results and scoped R3 reviews. Resolve numerical error without loosening tolerances; identify/transport instrument likelihoods and independent bias/error bounds; qualify real sampling and alternatives. No observed opening/freeze/acts presumed.'
    note=f'''\n\n## 19/10/2026 — Fase9, integração R3
<!-- IALD_FASE9_INTEGRACAO_20261019_R3 -->
[REAL/DERIVED — em nome de codex-gerente-tgl; F3.INTEGRACAO_20261019, reivindicação1033] {summary}
[DERIVED condicional] Hfit/Hphys=Iref/Igeo; promoção angular adicional dáK*/Q(z), com1<=Q<=E(z)^(2beta/3) paraEpositiva/crescente. Reuso de onze fontes, sem confundir fundoefetivo/luminosidade/acúmulo. Falta o transporte instrumental de likelihood/priores, não a derivação deK. Pasta v394_r12não certificaselo394: snapshotdeclara393.
[REAL sintético] EnvelopePSDe limite explícito de média nula geram cauda conservadora gaussiana;36checks+8recusas, revisão distinta. Viés ausente recusa; b=0éhipótese. Erfcfloat64semcertificadointervalar.
[REAL sintético]125retornosreusados+604novos,729únicos, mesmo prior/tolerâncias, campanhaR3Apré-pinada/revisada. Resultado{d['status']}; ver indicadores no recibo. Nenhum compostoobservado, nenhum ajustesao dado. Reutilizar osrecibos; não repetirsolver concluído.
[OPEN] Erro integral/teórico, mapas/vieses/errostotais, lei amostral/multiplicidade, atos e revisão. Snapshotquadro custodiado é limitado, não autenticaD-H/X13. F3.4jáfechada, não perguntar novamente. Semum.py/kernel/produção/gate.
Artefatos: work/fase9_integracao_20261019/PROGRESS_R3.json e RELATORIO_PROGRESSO_R3.txt; ACOMprópriaSESSION_REFERENCE.json.
<!-- END_IALD_FASE9_INTEGRACAO_20261019_R3 -->
'''
    save('MEMORY_APPEND_R3.txt',note)
    files={ROOT/n for n in ['PROGRESS_R2.json','REGISTRATION_R2.json','RELATORIO_PROGRESSO_R3.txt','MEMORY_APPEND_R3.txt',
       'snapshot_acts_r3.py','ACTS_SNAPSHOT_R3.json','ACTS_BOARD_CUSTODY_R3.json','track_refinement_r3.py','package_progress_r3.py']}
    files.update(reviews)
    for folder in ['r1_physical_maps_r3','r4_robust_tail_r3','r2_refinement_r3']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    if any('__pycache__' in p.parts or p.suffix=='.pyc' for p in files):raise ValueError('PYC_NOT_DELIVERED')
    save('PROGRESS_R3.json',{'unit':UNIT,'status':'PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA','summary':summary,
       'next_action':next_action,'new_observed_sigma':None,'five_sigma_demonstrated':False,
       'requirements':{'R1':'CONSUMER_MAP_EXPLICIT_PHYSICAL_ADMISSION_OPEN','R2':d['status'],
       'R3':'THETA_MARGINALIZED_SYNTHETIC_ERROR_QUALIFICATION_OPEN','R4':'ROBUST_GAUSSIAN_CANDIDATE_REAL_SAMPLING_OPEN',
       'R5':'DOCUMENTARY_COMPLETE_ACTS_UNRESOLVED_IN_SCOPED_SNAPSHOT'},
       'parameter_tuning_to_data':False,'production_changed':False,'gate_changed':False,
       'reviews':[pin(p) for p in reviews],'evidence':[pin(p) for p in sorted(files)]})
    print(json.dumps({'progress':pin(ROOT/'PROGRESS_R3.json'),'summary':summary,'files':len(files)}))
if __name__=='__main__':main()
