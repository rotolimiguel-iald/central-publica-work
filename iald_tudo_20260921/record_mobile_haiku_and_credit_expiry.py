"""Record the native client preparation and installed administrative date-only support."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import record_admin_boundary_verified as record

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
MARKER = 'IALD_MOBILE_HAIKU_PREPARED_CREDIT_DATE_ADMIN_20260922'
NOTE = '''[REAL — cliente móvel preparado, NÃO distribuído] mobile_haiku_client_20260922_162344_477579 contém delta isolado do cliente Haiku aplicado à base móvel20(e65d695 lido no git), sem levar trabalho incompleto do Selo: motor_selecao distingue Sonnet/Haiku; X-IALD-Context; histórico integral no Haiku; proteção contra respostas assíncronas antigas. Node syntax e6cenários comportamentais passaram. Avisos operacionais continuam ausentes. Somente W alterado nesta preparação; repoiald-app permanecia limpo. Não publicar este candidato como se incluísse a futura exportação/Selo; reconciliar com o cliente final e produzir iOS21/Android20 após a conclusão paralela.

[REAL — vencimento dos créditos somente na administração] Instalados apenas iald_deadlines.py e iald_deadlines.json, com backupsbytes/CAS. Campo expires_on=2027-09-23, date_timezone=UTC, expires_at=null; fonte é a página de faturamento lida em19:07:03.985UTC. Não inventa horário. Leitor preserva os4itens anteriores, adiciona créditosClaude e suporta chaveadmin opcional apenas quando cadastrada. No diaUTC indicado mostra Vence hoje/horário não informado; expired apenas no dia seguinte. Fonte de data diária não garante crédito disponível até fimdo dia.4testesanteriores+4checagens novas passaram; revisão independente14sondas semachados bloqueantes noescopo (credit_expiry_review_20260922_162652_765664.json). Nenhuma alteração em servidorSelo/app/mobile.

[REAL — aplicação verificada] Recibo credit_expiry_installed_20260922_162722_807852.json. Reiniciado somente filho web71684 apószeroreservas/slots; novo9420, pai41020, início16:27:46.925941BRT. Healthlocal200, rotasapi/alertas eadmin/api/prazos401sem sessão. Importação do leitorinstalado sobreJSONreal retornou data23/09/2027, precisão date, nenhumhorário,366diasdecalendário; é verificação do módulo maisHTTPprotegido, não painel autenticado. Artefatos server/web/client permanecem no estado anotado no recibo desta entrega. Esta mudança só de servidor não exige nova build.

[OPEN — continuidade sem reclassificar progresso como conclusão] ChaveadminAnthropic segue comoformuláriopreparado, Adicionar não acionado, perguntaespecíficaaguardaresposta. Login luiz nonavegador aindaaguardaoperador para testesSonnet2mensagens/cachejáautorizados. OrçamentoHaikupúblico e testeHaikupago pendentes; Haikuinterno flag1preservada, seleção atualdousuáriointacta. Selo: busca atualnão encontrouCONCLUSÃO—Selo IALD; não háhandleverificadodotrabalhoClaudequepermita chamarisso deprocessoaguardado. Clientepróxima build preparado; ainda nãocompilado/não enviado. T1visualCentral eT5exportaçãonoaparelhopendentes. Nenhumagastopago novo,nemchavecriada,nemenv tocado nesta etapa.

[MATRIZ] Web: Haikuconfigurado somenteLuiz, visual/testeautenticadopendente; prazoscréditos exclusivamenteadmin. iOSinterno/externo4.1(20) últimoestadoconferidoEmtestes, operadortelemetria20; não contémHaiku. Android4.1(19)APK/AABanterior, GooglePlaypendenteDUNS; candidatoclienteHaikuaindasem build. Links/convitespreservados. Objetivogeralativo, não concluído.
'''

def main():
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    evidence = {'checked_at': now.isoformat(), 'web_child': 9420, 'supervisor': 41020,
                'health': 200, 'unauthenticated_alert_routes': 401,
                'files': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ['iald_deadlines.py', 'iald_deadlines.json', 'iald_web_server.py', 'app/iald.js']},
                'native_candidate': 'mobile_haiku_client_20260922_162344_477579',
                'published_new_native_build': False, 'paid_generation_calls': 0}
    evidence_path = WORK / ('mobile_haiku_credit_status_' + stamp + '.json')
    record.helper.create(evidence_path, json.dumps(evidence, ensure_ascii=False, indent=2).encode('utf8'))
    targets = [p.with_name('MEMORY_2.md') if p.name == 'MEMORY.md' else p for p in record.helper.TARGETS]
    rows = [record.append(p, MARKER, 'Cliente Haiku preparado e prazo dos créditos somente na administração',
                          NOTE + '\nRecibo: ' + str(evidence_path), stamp, now) for p in targets]
    receipt = WORK / ('mobile_haiku_credit_memory_' + stamp + '.json')
    record.helper.create(receipt, json.dumps(rows, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'surfaces': len(rows), 'receipt': str(receipt)}))

if __name__ == '__main__':
    main()
