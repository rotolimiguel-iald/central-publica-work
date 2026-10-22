from pathlib import Path
import hashlib,json,datetime,subprocess,sys
W=Path(__file__).resolve().parents[1];D=W/'review';R=Path(r'C:\IALD\projetos_pyhton\IALD')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):
    p=D/name;raw=json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    if p.exists():
        backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));backup.write_bytes(p.read_bytes());assert backup.read_bytes()==p.read_bytes()
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
receipt=json.loads((W/'client_stage/receipt.json').read_bytes())
files=[]
for item in receipt['files']:
    p=W/'client_stage'/item['file'];b=W/'client_stage/origin'/item['file'];runtime=Path(item['source'])
    files.append(dict(file=item['file'],staged_sha256=sha(p),origin_sha256=sha(b),runtime_sha256=sha(runtime),receipt_stage_matches=sha(p)==item['staged_sha256'],receipt_origin_matches=sha(b)==item['origin_sha256']))
save('client_review_r1.json',{
 'status':'BLOCK_CLIENT_R1','installation_approval':False,'unit':'F9.APP_READABILITY_RELIABLE_TOOLS_20261021','reviewer':'codex-independent-review','files':files,
 'findings':[{'id':'CLIENT-01','severity':'MEDIO','status':'OPEN','file':str(W/'client_stage/iald.js'),'lines':[3047,3140,4093,4097],
 'title':'Histórico local de mídia impede nova mensagem apenas textual',
 'reproduction':'enviarTexto(texto,[]) detecta iald_local_media antigo; mediaPrepareLegacy chama mediaUpload, que recusa incondicionalmente. Zero anexos novos, zero transmissão, histórico conservado porém conversa bloqueada.',
 'evidence':str(D/'legacy_continuation_result.json'),'evidence_sha256':sha(D/'legacy_continuation_result.json'),
 'requested_resolution':'Projetar somente o envio: substituir mídia histórica por metadados explícitos sem alegar análise; preservar texto, referências e bytes do histórico armazenado. Não executar upload. Mídia nova continua recusada. Requer revisão R2 dos bytes efetivamente entregues.'}],
 'existing_tests':{'checks':31,'status':'PASS','receipt':str(D/'existing_client_tests.json'),'limitation':'Os 31 checks não cobrem continuação textual com mídia local histórica; funções históricas inalteradas não bastam para excluir regressão.'},
 'confirmed_scope':['Tarja removida da montagem de anexos.','Conversa 16.5px para 15.5px; input e edição 16px preservados; tamanhos absolutos de código inline e fórmulas compensados.','index.html idêntico; múltiplos/documentos/imagens preservados nos testes existentes.'],
 'r2_required_cases':['Histórico iald_local_media seguido de texto, sem anexos novos: enviar sem upload e preservar original.','Histórico iald_media e referências antigas: projeção explícita de metadados, sem inferência de análise ou fetch/upload implícito.','Áudio/vídeo inline legado após migração e antes dela, conforme caminho de recuperação: continuidade sem apagar original.','Texto/imagens/documentos históricos mantidos em ordem; nenhum falso marcador de análise de áudio/vídeo.','Novos anexos áudio/vídeo no picker/drop/paste e envio direto continuam bloqueados.','Projeção não modifica S.conversas nem mensagens/content; repetir montagem não degrada metadados.','Backend admite a continuação textual e recusa mídia nova apesar de cliente forjado; carteira/consentimento/uncertain retries continuam protegidos.'],
 'runtime_modified':False,'stage_modified':False,'models_called':False,'tests_network_calls':0,'final_plan_review':'NOT_STARTED_AWAITING_CLOSED_PLAN'})
sources=[R/'iald-app/package.json',R/'iald-app/capacitor.config.json',R/'iald-app/ios/App/ci_scripts/ci_post_clone.sh',R/'iald-app/scripts/validate-release.mjs',R/'iald-app/ios/App/App.xcodeproj/project.pbxproj',R/'iald-app/android/app/build.gradle',R/'iald_app_providers.py',R/'iald_web_server.py']
save('review_preparation.json',{
 'status':'PREPARATION_ONLY_NOT_APPROVED','date':'2026-10-21','reference':str(W/'SESSION_REFERENCE.json'),'memory_usage':'Referência fornecida explicitamente recuperada; nenhuma memória antiga adotada; nenhuma transição compartilhada nesta subtarefa com escrita limitada a review.',
 'source_hashes':{str(p):sha(p) for p in sources},
 'mobile':{'source_versions':{'ios':'4.1 (35), Debug e Release','android':'4.1 (30)'},'proposed_minimum':{'ios':'4.1 (36)','android':'4.1 (31)'},'scope':'Valores medidos nos fontes; não provam versões disponíveis nas lojas. Revalidar antes de fechar plano.',
 'pipeline':'webDir=www, recursos embarcados, appId br.ia.IALD; npm sync:ios/android executa validate antes de cap sync. CI usa Node pinado e valida SHA antes de npm ci; nenhum script executado.',
 'required':'Conferir recursos web/www/public por hash e conteúdo efetivamente empacotado; não reutilizar intermediários Android divergentes. Validar identidades, assinatura e versões no artefato. TestFlight Equipe/Piloto e disponibilidade do operador exigem evidência posterior. Não confundir build com instalação física.'},
 'attachment_limits':{'per_message':6,'images':3,'image_bytes':8000000,'pdf_bytes':25000000,'text_bytes':2000000,'chat_body_bytes':50*1024*1024,'scope':'Limites distintos, não 50 MB por arquivo/sessão; contexto/extração/provedor podem restringir.'},
 'deepseek_official':{'accessed':'2026-10-21','pricing_url':'https://api-docs.deepseek.com/quick_start/pricing/','thinking_url':'https://api-docs.deepseek.com/guides/thinking_mode/','alias':'deepseek-flash','documented_current_version':'DeepSeek-V4.1-Flash-1017','rates_usd_per_million':{'peak':{'input_cache_miss':0.30,'input_cache_hit':0.006,'output':1.20},'off_peak':{'input_cache_miss':0.15,'input_cache_hit':0.003,'output':0.60}},'local_rates_observed':[0.30,0.006,1.20],'interpretation':'Tarifas locais observadas já correspondem ao pico oficial; não anunciar queda nova sem referência temporal comparável. Separar estimativa conservadora de cobrança real. Alias móvel não é versão pinada.',
 'tools':'Tool calls suportadas pelo fornecedor não demonstram integração local de novos recursos. Search/Fetch são APIs separadas; suporte Vision não implica disponibilidade no app. Não habilitar por inferência.',
 'thinking':'Com tools, preservar reasoning_content exigido nas rodadas posteriores; verificar adaptação real e testes antes de alegar compatibilidade.'},
 'closed_plan_requirements':['Plano imutável com fontes/destinos e hashes completos, baseline/runtime atuais e escopo exato.','client_stage R2 e provider_stage entregues com testes offline incluindo regressão histórica; não aceitar apenas nomes de testes.','Ciência/prefixos/kernel/gate e carteira/isenções/consentimentos/contas preservados por hashes/diffs e regressões pertinentes.','transaction.py, maintenance.py e deploy_controlled.py conferidos contra revisão precedente e escopo atual; implantação não será executada pelo revisor.','review_final PASS somente após plano fechado: plan_sha256, transaction_sha256, maintenance_sha256 calculados dos bytes revisados.'],
 'actions_not_performed':['build','install','git','model_calls','mission_accept','AUDITADA','shared_memory_transition'],
 'current_blocker':'CLIENT-01; aguardando correção antes de R2; plano final ainda não revisado.'})
request={'operation':'project','reference':str(W/'SESSION_REFERENCE.json'),'max_chars':24000}
p=subprocess.run([sys.executable,'-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(request).encode(),capture_output=True)
try:result=json.loads(p.stdout)
except ValueError:result={'error':'mission projection unreadable','returncode':p.returncode}
save('mission_projection_readonly.json',result)
print(json.dumps({'client_status':'BLOCK_CLIENT_R1','preparation':'PREPARATION_ONLY_NOT_APPROVED','mission_project_returncode':p.returncode,'reports':[str(D/'client_review_r1.json'),str(D/'review_preparation.json')]}))
