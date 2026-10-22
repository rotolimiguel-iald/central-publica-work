"""Record observed delivery; only selected operational metrics are read."""
from pathlib import Path
from datetime import datetime, timezone
import json
import sqlite3
from transaction import write_evidence, backup, atomic, digest

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')

def main():
    now = datetime.now(timezone.utc).isoformat()
    metric_id = 'cdf3cb7cb0814d4098c84c4f9455e6b3'
    keys = ('id','utc','provider','model','status','memory_sha256',
            'first_text_seconds','elapsed_seconds','calls')
    columns = ','.join("json_extract(data,'$." + k + "')" for k in keys)
    path = R / '.iald_runtime/app_evaluation/metrics.sqlite3'
    with sqlite3.connect(path.as_uri()+'?mode=ro', uri=True) as db:
        row = db.execute('SELECT ' + columns + ' FROM turns WHERE id=?', (metric_id,)).fetchone()
    assert row and row[4] == 'completed'
    metric = dict(zip(keys, row))
    metric['calls'] = json.loads(metric['calls'])
    assert len(metric['calls']) == 1 and metric['calls'][0]['status'] == 'completed'
    seal = json.loads((W/'science/verified_sources/um_absoluto_selo.json').read_bytes())
    live = {
        'status':'PASS', 'scope':'Dispatch, completion, scientific version/author and H3 scope; not a complete answer-quality benchmark',
        'observed_at':now, 'url':'https://demo.iald.ia.br/app/index.html',
        'test_prompt':'Teste da atualização: informe a versão do pacote científico efetivamente carregado e o autor da TGL. Em duas frases, explique o alcance da lei de campo curvo v392 e sua hipótese H3. Responda em até seis linhas, usando o núcleo já carregado; não execute bancada, não gere arquivos e não delegue tarefas.',
        'account':'luiz', 'mode':'automatic', 'metric':metric,
        'checks':{'selected_tool_capable_manager':'mimo','completed_response_visible':True,
                  'version':'v392','author':'Luiz Antonio Rotoli Miguel',
                  'conditional_h3_scope_preserved':True,'tool_calls':0,
                  'no_bench_execution':True,'no_artifact_generation':True,'no_delegation':True},
        'limitations':[
            'Single short reply; not a broad scientific-quality or provider-comparison benchmark.',
            'Test appended to an existing synthetic code-test conversation; not a new isolated conversation.',
            'Reply volunteered an inaccurate seal date (14/10/2026). Actual sealed source timestamp is '+seal['timestamp']+'. Scientific version and hashes matched; deployment date must not be treated as seal date.',
            'Cost is an estimate derived from measured usage, not the provider invoice.'
        ]
    }
    write_evidence(W/'live_validation.json',live)
    base='https://appstoreconnect.apple.com/teams/7e576f08-1ae7-4b38-ac9f-cfdb952c2cac/apps/6760655636'
    distribution={
        'observed_at':now,'status':'AVAILABLE_BOTH_GROUPS',
        'summary':'iOS4.1(32) disponível e Em testes nos grupos IALD Equipe (1tester, identidade de Luiz conferida) e IALD Piloto (6testers). Apple ainda mostrava4.1(29) instalada na conta de Luiz; atualização no aparelho não realizada nesta sessão.',
        'version':'4.1','build':32,'build_id':'afc1b28c-50fd-4ca4-8697-889d846d63d6',
        'detail_url':base+'/testflight/ios/afc1b28c-50fd-4ca4-8697-889d846d63d6',
        'internal':{'group':'IALD Equipe','id':'0f9c8943-18f0-4f10-82ad-89a5832b9dec','testers':1,'status':'Em testes','operator_identity_verified':True,'last_installed_version_reported':'4.1 (29)'},
        'external':{'group':'IALD Piloto','id':'a2f7c246-06e1-4f7c-8fcd-d0c2a79cc345','testers':6,'status':'Em testes','automatically_notify_testers':True},
        'expiry':{'expires_at':None,'displayed':'Expira em 90 dias','exact_date_not_displayed':True},
        'upload_displayed':'14 de out. de 2026 às 09:14','binary_status':'Validado','device_family':['iPhone','iPad'],
        'contract':{'revision':'LYL260','issued':'2026-10-13','accepted':'2026-10-14','specific_human_authorization':True,'observed_accepted':True},
        'cloud_build':{'number':32,'status':'SUCCEEDED','warnings':5,'errors':0,'build_id':'3d38edbe-5df5-470b-a68b-e9751e9313c5','commit':'59f9e5d09d9c928964b258818fb429cdb92ce31c','previous_attempts':{'30':'FAILED Homebrew OpenSSL installation lock','31':'FAILED same lock'},'fix':'Official Node24.21.0 archive with verified fixed SHA; Homebrew removed from post-clone setup.'},
        'physical_installation_verified':False,
        'android':{'existing_version':'4.1 (27)','backend_updated':True,'new_binary_required_for_backend_changes':False,'new_binary_built_this_delivery':False,'play_published_this_delivery':False,'historical_blocker':'Developer organization enrollment / D-U-N-S not completed in prior delivery'}
    }
    write_evidence(W/'mobile/distribution.json',distribution)
    path=R/'iald_deadlines.json'
    original=path.read_bytes()
    deadlines=json.loads(original)
    preserved={k:v for k,v in deadlines['items'].items() if k not in ('testflight_internal','testflight_external')}
    deadlines['checked_at']=now
    for key,group in [('testflight_internal','IALD Equipe'),('testflight_external','IALD Piloto')]:
        deadlines['items'][key]={'expires_at':None,'label':'IALD 4.1 (32) — '+group,'source':'App Store Connect '+now+': Em testes; Expira em 90 dias; data/hora exatas não exibidas. Não inferidas da duração nominal.','build':'4.1 (32)','status':'Em testes'}
    assert preserved=={k:v for k,v in deadlines['items'].items() if k not in ('testflight_internal','testflight_external')}
    saved=backup(path)
    assert path.read_bytes()==original
    raw=json.dumps(deadlines,ensure_ascii=False,indent=2).encode()
    atomic(path,raw)
    write_evidence(W/'deadlines_delivery.json',{'status':'PASS','backup':saved,'sha256':digest(raw),'exact_expiry':'unknown','scope':'Internal administration only; no new key data and no public chat/client notice'})
    for name in ('installed_verification.json','restart.json'):
        assert json.loads((W/name).read_bytes())['status']=='PASS'
    result={
        'status':'DELIVERED','observed_at':now,'unit':'F9.APP_STACK_20261014',
        'science':{'version':'v392','topics':411,'new_topics':32,'formal_sources':1230,'sealed_source_timestamp':seal['timestamp'],'full_public_context_anthropic_tokens':648972,'compact_context_anthropic_tokens':314674,'kernel_v5_preserved':True,'originals_not_modified':True,'no_new_custody_issued':True},
        'routing':'Kimi > MiMo > OpenAI > DeepSeek > native, filtered by capability, rights, consent and budget; Claude manual only in normal selection; separate Anthropic sandbox unchanged',
        'verification':{'functional_tests':35,'independent_review':'PASS after maintenance-race correction','installed_files':1257,'live_test':str(W/'live_validation.json')},
        'availability':{'web':'Active, real automatic MiMo reply completed','ios_internal':'4.1 (32) Em testes; operator membership verified','ios_external':'4.1 (32) Em testes; six existing testers','android':'Shared backend updated; existing4.1(27) APK/AAB; Google Play not published'},
        'argon':'Official documentation studied; recommended internal pilot; not enabled or called',
        'remaining_limits':['Physical installation not verified','Exact TestFlight expiration not exposed by UI; recorded unknown','Kimi still buffered text and no interactive tools','Image/video generation not integrated','One model reply confused seal date with deployment date; source preserved and discrepancy recorded'],
        'evidence':[str(W/x) for x in ['installed_verification.json','validation/final_checks.json','validation/wallet_regression.json','validation/review_final.json','science_review/DELIVERY.json','live_validation.json','mobile/distribution.json','stack_assessment.json','deadlines_delivery.json']]
    }
    write_evidence(W/'delivery.json',result)
    route=json.loads((W/'route_prepared.json').read_bytes())
    route.update(tipo='RESULTADO',status='EXAMINADA',olhou_dados=True,
                 resultado='v392 instalada;411tópicos;1257arquivos;35testes funcionais e revisão independente; teste real MiMo concluído; iOS4.1(32) Em testes em ambos os grupos.',
                 veredito='DELIVERED_WITH_EXPLICIT_LIMITS',
                 defeito='Sem instalação física verificada. Argon não ativado; Kimi textual sem ferramentas interativas. Data exata de expiração não exibida. Teste acertou versão/autoria/H3 mas errou data voluntária do selo; fonte correta preservada.',
                 proximo_passo='Usar a build32; próximos aprimoramentos recomendados em stack_assessment.json, sem novas chamadas automáticas.',
                 artefatos=[str(W/'delivery.json'),str(W/'live_validation.json'),str(W/'mobile/distribution.json')])
    write_evidence(W/'route_delivery.json',route)
    print(json.dumps({'status':'DELIVERED','metric':metric_id,'build':32,'deadlines':'internal_only'}))

if __name__=='__main__': main()
