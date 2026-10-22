"""Preserve completed map/error-consumer qualifications separately from CAMB R4."""
from setup_mission import ROOT,UNIT,pin,save
from pathlib import Path
import json
def main():
    reviews=[ROOT/'REVIEW_MAP_BOUND_R4.json',ROOT/'REVIEW_THETA_GATE_R4.json']
    for p in reviews:
        assert json.loads(p.read_text(encoding='utf-8'))['status']=='PASS_WITH_SCOPE'
    summary='Cota geométrica parcial e consumidor de recusa numérica revisados; sem novo sigma observado. A próxima campanha CAMB R4 é separada desta qualificação.'
    next_action='Complete independent preflight of numerical R4 and run once if approved; reuse729 physical results, max4184new, fixedprior/tolerance. Track actual live handle then terminal receipt. Consume numerical result with theta_gate_r4b. Physical reader maps, independent bias bounds, sampling and actual acts remain open.'
    report='''FASE9 — QUALIFICAÇÕES R4, 19/10/2026
Em nome de codex-gerente-tgl; unidadeF3.INTEGRACAO_20261019, reivindicação1033.

[DERIVED condicional] Reaproveitada a prova deQ como média positiva. Sob FLRW
plana, componentes positivas conservadas e−1<=w_eff<=1/3, E(z)<=(1+z)^2.
Logo Q<=(1+zmax)^(4beta/3). Beta calculado de alpha_CODATA2018*sqrt(e).
Uma única avaliação pré-pinada, semCAMB e sem ajuste, limitou o desvio nominal:
z<=.04:0,046716km/s/Mpc; z<=.15:0,166338km/s/Mpc.
Tetos na caixa condicional:0,063329 e0,225490. Os valores nominais representam
14,16% e50,41% da margem de planejamento0,329978; essa margem não é um limite
de viés nulo medido nem um orçamento de sistemáticas validado.

[OPEN — alcance] Só o fator de formaQ é limitado. Masers exigem promoção angular
adicional, identificação da distância e disco preservado. vCMB/c publicado não
limita o redshift latente com prior gaussiano de velocidade peculiar; z<=.04 é
domínio condicional. O corte.15 é doR22/Pantheon+, não transferido aCSP/SBF/R25.
Iref/I para fundos diferentes, calibrações, âncoras e seleção não estão cobertos.
Para composto com pesos fixos, usar sum|w_i|b_i: negativos podem amplificar.
Nenhuma dessas cotas é novo sigma observado ou aceitação do mapa completo.

[REAL — integração de recusa] Novo theta_gate_r4b consome JSON e receita pinados
da integração conjunta, recalcula gaps/indicador, exige contagens e coerência dos
integrais finais/razões. A rodadaR3 real é recusada emH1,H2,H4 porque excede.01.
Oito mutações iniciais e três adicionais foram recusadas. Um cenário sintético
de igualdade de níveis passa apenas diagnóstico, sem liberar conclusão física.
Uma diferença pequena entre grades não certifica picos perdidos, erroCAMB,
probabilidade de cauda, admissão humana ou uma execução do escalarV2.
Revisão independentePASS_WITH_SCOPE dos dois componentes; testes não repetidos.

[PROCESSO] O primeiro preflight do turno foiR2rev11; o preflight específicoR5
ocorreu depois da primeira versão/teste do consumidor e antes da camadaR4B.
A reivindicaçãoR5 estava vigente; não se apresenta aquela checagem como prévia.
Sem efeito emoriginais, produção, dados observados, congelamento ou gate.

[CONTINUIDADE] A campanha numéricaR4 foi preparada separadamente:9³→17³,
729reusos+até4184novos,4913total, mesmosprior/dados/tolerância,1800s1thread.
Esta entrega NÃO a declara executada nem concluída. Seu início/término dependem
dos recibos próprios, revisão e handle. Não repetir resultados ou IDs encerrados.
Os cinco requisitos da missão permanecem abertos no escopo integral.
'''
    save('RELATORIO_PROGRESSO_R4.txt',report)
    note='''\n\n## 19/10/2026 — Fase9: cotas geométricas e recusa numérica R4
<!-- IALD_FASE9_INTEGRACAO_20261019_R4 -->
[DERIVED/REAL — em nome de codex-gerente-tgl, F3.INTEGRACAO_20261019, reivindicação1033] Sob hipótesesFLRWpositivas explícitas, Q<=(1+zmax)^(4beta/3). Cotas nominais parciais0,046716(z<=.04) e0,166338(z<=.15)km/s/Mpc; caixa condicional0,063329/0,225490. Não são viés total nem sigma; promoçãoangular/latentes/pesos/cortes preservados. Não transferir corteR22 aCSP/SBF/R25. Seisfontes conferidas; avaliaçãoúnica pré-pinada, semCAMB.
[REAL] Consumidor theta_gate_r4b relêpinos, recalcula gaps/indicador e verifica valoresfinais/contagens; R3recusadaH1/H2/H4>.01.11mutaçõesrecusadas, revisão distinta dosdoiscomponentes. Convergênciaindicadora nãoéerrocertificado/admissão/abertura. Cronologia dopreflightR5 inicialmente posterior àprimeiraversão está registrada, não ocultada.
[OPEN] CampanhaCAMBR4separada, preparada729reusos+4184novos; esta nota nãoafirma inícioou término. Consultarhandle/reciboexato. Mapasinstrumentais/vieses/caudas/atos permanecemabertos. Nenhumobservado/produção/gate.
Artefatos: work/fase9_integracao_20261019/PROGRESS_R4.json e RELATORIO_PROGRESSO_R4.txt; ACOMprópriaSESSION_REFERENCE.json.
<!-- END_IALD_FASE9_INTEGRACAO_20261019_R4 -->
'''
    save('MEMORY_APPEND_R4.txt',note)
    files={ROOT/n for n in ['PROGRESS_R3.json','REGISTRATION_R3.json','RELATORIO_PROGRESSO_R4.txt','MEMORY_APPEND_R4.txt','stage_qualifications_r4.py','register_progress_r4.py']}
    files.update(reviews)
    for folder in ['r1_map_bound_r4','r5_theta_gate_r4']:
        files.update(p for p in (ROOT/folder).rglob('*') if p.is_file())
    assert not any('__pycache__' in p.parts or p.suffix=='.pyc' for p in files)
    save('PROGRESS_R4.json',{'unit':UNIT,'status':'PARTIAL_QUALIFICATION__NUMERICAL_CAMPAIGN_SEPARATE',
      'summary':summary,'next_action':next_action,'new_observed_sigma':None,'five_sigma_demonstrated':False,
      'parameter_tuning_to_data':False,'production_changed':False,'gate_changed':False,
      'reviews':[pin(p) for p in reviews],'evidence':[pin(p) for p in sorted(files)]})
    print(json.dumps({'progress':pin(ROOT/'PROGRESS_R4.json'),'files':len(files)}))
if __name__=='__main__':main()
