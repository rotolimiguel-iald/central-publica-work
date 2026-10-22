from pathlib import Path
import ast,datetime,hashlib,json
W=Path(__file__).resolve().parents[1]
runner=W/'mobile_release.py';publisher=W/'publish_apk31.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def line(p,text):return next(i for i,s in enumerate(p.read_text(encoding='utf-8').splitlines(),1) if text in s)
ast.parse(runner.read_bytes());ast.parse(publisher.read_bytes())
old=W.parent/'mimo_media_capacity_20261020/client_stage/android30_final19_label_R8'
report={'status':'BLOCK','reviewer':'codex-readability-reviewer','scope':'STATIC_MOBILE_RUNNER_REVIEW_ONLY; nenhuma execução/importação dos runners, build, assinatura, Git, push ou publicação.',
 'runner_sha256':sha(runner),'publisher_sha256':sha(publisher),'plan_sha256':sha(W/'install_plan.json'),
 'findings':[
 {'id':'MOBILE-01','severity':'MEDIO','file':str(runner),'line':line(runner,"cmd=[p['wrapper']"),'title':'Diretório isolado não é conectado ao Gradle',
 'evidence':'A linha Gradle passa -Diald.mobile.output, mas não --init-script; android/build.gradle e app/build.gradle não leem essa propriedade. O consumidor existente está no android30_R1.init.gradle, omitido pelo novo comando. O runner busca APK/AAB apenas em mobile_stage/build31 após a build.',
 'impact':'Build pode escrever nos diretórios habituais do projeto e falhar depois na contagem de artefatos, consumindo a única tentativa sem recibo de auditoria.',
 'required_fix':'Preparar init script próprio de build31, pinado, com raiz W/mobile_stage/build31, aplicação br.ia.IALD/4.1/31 e isolamento de outputs; passá-lo explicitamente com --init-script e conferir marcadores. Não usar init30 intacto: ele fixa versão30 e raiz da missão anterior.'},
 {'id':'MOBILE-02','severity':'MEDIO','file':str(runner),'line':line(runner,'def push():'),'title':'Fase push não revalida o destino remoto autorizado',
 'evidence':'URLs de fetch/push são conferidas somente em commit(). push() é execução separada e usa origin em ls-remote/push sem repetir a allowlist. Igualdade do SHA remoto com baseline não autentica o repositório de destino.',
 'impact':'Alteração de origin/pushurl entre as fases pode enviar o commit para destino diferente do repositório privado revisado.',
 'required_fix':'Repetir na fase push, antes de ls-remote/intenção/envio, a validação das URLs fetch e push contra a mesma allowlist; conservar a proibição de retry incerto.'}
 ],
 'confirmed':['collect é importado sem main/guards antigos serem chamados; leitura estática das dependências não encontrou execução de build no import.','collect sanitiza saída antes de persistir, registra hash do fluxo bruto sem gravá-lo; runner recusa filtered_lines.','check(deploy) e hashes de destinos/ciência são chamados nas fases build/commit/push; publisher chama check(deploy).','Commit usa seis caminhos explícitos, índice prévio vazio, blobs raw sem filtros e comparação SHA do índice com arquivos.','Build inspeciona ZIPs, JS/CSS embutidos, extensões confidenciais, versão31, certificado APK comparado ao anterior e certificado AAB comparado ao APK.','Publisher exige audit PASS31 e SHA do APK, destino fixo novo, intenção exclusiva, rename e preservação dos APKs anteriores. Rota existente de downloads exige conta válida.'],
 'residual_notes':[{'severity':'BAIXO','note':'Badging verifica versão, mas deve também verificar package br.ia.IALD; a inspeção AAB pode exigir explicitamente jar verified. além do exit0/certificado. Nenhum artefato31 foi inspecionado nesta revisão.'}],
 'dependencies_read':{str(p):sha(p) for p in [old/'run_android30_R1.py',old/'release_lineage_R8.py',old/'android30_R1.init.gradle',old/'ANDROID30_BUILD_PLAN_R1.json']},
 'installation_review_unchanged':'validation/review_final.json permanece PASS para instalação dos12destinos; implementation aceita na revisão6. Este BLOCK vale somente aos scripts mobile atuais.',
 'executed':False,'credentials_read':False,'models_called':False,'deployment_accepted':False}
p=W/'validation/mobile_review.json';raw=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
if p.exists():
 b=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));b.write_bytes(p.read_bytes());assert b.read_bytes()==p.read_bytes()
t=p.with_suffix('.json.review_tmp');t.write_bytes(raw);assert t.read_bytes()==raw;t.replace(p)
print(json.dumps({'status':report['status'],'runner_sha256':report['runner_sha256'],'publisher_sha256':report['publisher_sha256'],'findings':[f['id'] for f in report['findings']],'report':str(p)}))
