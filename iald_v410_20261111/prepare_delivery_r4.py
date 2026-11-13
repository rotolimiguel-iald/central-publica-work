"""Create measured technical delivery; does not accept mission or close order."""
from pathlib import Path
import json,hashlib,datetime
A=Path(__file__).resolve().parent
R=Path(r'C:\IALD\projetos_pyhton\IALD')
Q=A.parent/'scientific_memory_sync_20261111_v410'
def read(p):return json.loads(Path(p).read_bytes())
def pin(p):return {'path':str(p),'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()}
def create(p,raw):
 raw=raw if isinstance(raw,bytes) else (json.dumps(raw,ensure_ascii=False,indent=2)+'\n').encode()
 with Path(p).open('xb') as f:f.write(raw)
 assert Path(p).read_bytes()==raw
inst=read(A/'INSTALLED_VERIFICATION.json');live=read(A/'LIVE_BACKEND.json');updater=read(A/'UPDATER_RUNNING_VERIFIED.json');tower=read(A/'TORRE_RESULT.json');queue=read(Q/'DELIVERY_TECHNICAL_R1.json')
assert inst['status']==live['status']==updater['status']=='PASS'
assert inst['identity']['release']==inst['JEV_release']==queue['release']=='v410'
assert tower['jev_current']
plan=read(A/'install_plan.json')
for row in plan['files']:assert hashlib.sha256(Path(row['destination']).read_bytes()).hexdigest()==row['sha256']
paths=['LICOES_v410.md','LESSONS_R4_APPLIED.json','RELEASE.json','install_plan.json','RUNTIME_DELTA_R4.json','deployment.json','restart.json','validation/review_final.json','validation/review_deploy.json','PREFLIGHT_INSTALLED_VERIFICATION.json','INSTALLED_VERIFICATION.json','LIVE_BACKEND.json','UPDATER_RUNNING_VERIFIED.json','TORRE_RESULT.json','app/R4/NATIVE_FINAL_COUNT.json']
delivery={'status':'INSTALLED_AND_VERIFIED_TECHNICAL_SCOPE','order':'ORDEM_012','identity':inst['identity'],'jev_release':inst['JEV_release'],'files_verified':inst['files_verified'],'queue':{k:queue[k] for k in ('release','generation','documents','chunks','previous_releases_preserved')},'architecture':'Immutable complete admitted public corpus; bounded core and same-version retrieval per call; mandatory statutes preserved; partial retrieval explicit','native_prefix_scope':'Native prefix is smaller; mother instruction retrievable in full, not resident','generation_calls':0,'remote_count_calls':4,'updater':updater,'availability':{'web':'Shared backend v410 loaded; local HTTP200 and installed offline fixtures verified','ios_internal':'Shared backend; no client change or new build','ios_external':'Shared backend; no client change or new build','android':'Shared backend; no client change or new build','stores':'Not inspected or distributed in this server release','physical_devices':'Not tested'},'limitations':['No live generated model response or physical device test','Every real conversation remains subject to model-specific context admission','Future releases wait for real independent ACOM acceptance; no automatic reviewer consumer integrated','No um.py or Lean execution; no scientific gate changed'],'artifacts':[pin(A/f) for f in paths]+[pin(Q/'DELIVERY_TECHNICAL_R1.json'),pin(Q/'ACTIVATION_ACCEPT_REVIEWER_R1.json')],'reference':str(A/'SESSION_REFERENCE.json')}
create(A/'TECHNICAL_DELIVERY_R4.json',delivery)
text=f'''11/11/2026 — ORDEM012: app/JEV v410 e acervo versionado.

[REAL] Instalados e conferidos {inst['files_verified']} destinos; versão/hash/commit vêm do recibo TECHNICAL_DELIVERY_R4.json. Reinício somente do filho web8082 sob o supervisor existente, HTTP200. Loaders em processo novo e recuperação documental verificados. Zero geração remota; quatro COUNT oficiais separados por modelo. Nenhuma execução de um.py/Lean ou mudança do gate.
[INPUT/REAL] A autorização R4 substituiu a residência literal P2 por núcleo limitado e corpus público integral imutável consultável. Cada chamada fixa uma versão para JEV, ferramentas e workers. Recuperação é parcial e rastreável; não se afirma corpus inteiro no prompt. A nativa usa prefixo menor, com instrução-mãe integral recuperável. Estatutos obrigatórios preservados; limites dos provedores e de cada conversa continuam.
[REAL] Atualizador local detecta versão selada/publicada, prepara, mede e espera revisão independente real; só então admite ativação com CAS e janela ociosa. Falha do loader restaura o ponteiro anterior. Candidatos falhos/incertos não são reenviados por timer. Situação só na administração.
[OPEN] Não há consumidor automático de revisão integrado: atualização futura não é totalmente desassistida. Sem teste real de resposta de modelo ou aparelho. Backend compartilhado web/iOS/Android; nenhuma nova build ou distribuição de loja necessária.
[REAL] A fila v410 já concluída foi reutilizada, sem nova ativação: {queue['documents']} documentos, {queue['chunks']} trechos. Geração no recibo próprio. Fontes originais e versões anteriores preservadas.
Fonte: {A/'TECHNICAL_DELIVERY_R4.json'}. Aceite da missão e promoção da memória permanecem atos separados.
'''
create(A/'MEMORY_DEPOSIT_v410_R4.md',text.encode())
print(json.dumps({'status':delivery['status'],'receipt':pin(A/'TECHNICAL_DELIVERY_R4.json')}))
