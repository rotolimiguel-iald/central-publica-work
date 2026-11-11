"""Independent pins for the exact files delivered from the local preview."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,http.client,json,zipfile
from urllib.parse import quote
W=Path(__file__).resolve().parent
B=W/'acom_windows';UI=Path(r'C:\IALD\um_interface');D=UI/'downloads';review=B/'review'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def pin(p):return dict(path=str(p),sha256=sha(p))
setup=D/'ACOM-Setup.exe';sources=D/'ACOM-fonte.zip';sample=D/'Primeira-luz.acom'
ix=read(B/'build-info'/'last-build.json')
if ix['development'] or sha(setup)!=ix['setupSHA256'] or sha(sources)!=ix['sourceSHA256']:
    raise RuntimeError('O instalador não corresponde à montagem final')
contents={i['name']:i['sha256'] for i in ix['manifest']}
for name in ('index.html','src/acom.js','src/main.js','src/styles.css','downloads/ACOM-fonte.zip','downloads/Primeira-luz.acom'):
    if contents['web/'+name]!=sha(UI/name): raise RuntimeError('UI ou recursos mudaram: '+name)
if 'Primeira-luz.acom' not in (UI/'index.html').read_text(encoding='utf8')+(UI/'src/acom.js').read_text(encoding='utf8'):
    raise RuntimeError('Amostra ausente da UI')
for name in ('app/host.py','app/archive_safe.py','LICENSE-IALD.txt'):
    if contents[name]!=sha(B/name):raise RuntimeError('Adaptador ou licença divergente: '+name)
with zipfile.ZipFile(sources) as z:
    for name in ('app/host.py','app/archive_safe.py','app/acom_archive.py','app/acom_codec.py','app/acom_auto.py','LICENSE-IALD.txt'):
        if hashlib.sha256(z.read(name)).hexdigest()!=contents[name]:raise RuntimeError(name)
    if z.testzip():raise RuntimeError('ZIP corrompido')
delivery=[]
for file in (setup,sources,sample):
    con=http.client.HTTPConnection('127.0.0.1',7100,timeout=12)
    con.request('GET','/downloads/'+quote(file.name))
    resp=con.getresponse()
    if resp.status!=200 or hashlib.file_digest(resp,'sha256').hexdigest()!=sha(file):raise RuntimeError('Download divergente: '+file.name)
    con.close()
    delivery.append(dict(**pin(file),bytes=file.stat().st_size))
installer_reviews=[(p,read(p)) for p in review.glob('INSTALLER_REVIEW*.json')]
match=[(p,r) for p,r in installer_reviews if r['setupSha256']==ix['setupSHA256'] and r['passed']==r['total']]
if not match: raise RuntimeError('Revisão independente do instalador final pendente')
web_test=read(UI/'verification'/'results.json')
if not web_test['ok'] or not all(i['pass'] for i in web_test['checks']):raise RuntimeError('Falha na interface')
layout_checks=[(p,read(p)) for p in (B/'build-info').glob('*admin*json')]
layout=next((p for p,i in layout_checks if i.get('installer')==ix['setupSHA256'] and i.get('msiexec_admin_result')==0),None)
if layout is None: raise RuntimeError('A imagem administrativa do MSI final não foi conferida')
receipt={'time':datetime.now(timezone.utc).isoformat(),'status':'REAL — edição local de teste; distribuição pública não efetuada','downloads':delivery,
 'independent_package_review':pin(match[0][0]),'inputs':[pin(W/'ADENDO_ACOM.txt'),pin(W/'ADENDO_INSTALADOR.txt')], 'tunnel':[pin(W/'TUNEL'/name) for name in ('013_CODEX.md','014_KIMI.md','015_CODEX.md') if (W/'TUNEL'/name).exists()],'kimi_evidence':pin(UI/'verification'/'results.json'),
 'ui_checks':len(web_test['checks']),'ui_receipt':pin(UI/'verification'/'results.json'),'windows_installer_admin':pin(layout),
 'api':read(B/'API_ROUNDTRIP.json'),'packaged_python_test':read(B/'API_PACKAGED_ROUNDTRIP_R2.json'),'native_dialog':'Tk 8.6.15 win32 iniciou; clique de seleção de arquivo não verificado nesta sessão.','format_tests':pin(review/'codec_validation.json'),'native_artifact':dict(payload_files=len(contents),offline=True,per_user=True,explorer_opt_in=True,locale_catalogs=['pt','en','ar'],target='Windows x64',authenticode='unsigned'),'limits':['Ensaios isolados; instalação e remoção interativas em um perfil limpo não verificadas.','1 GiB por membro; 4 GiB totais; 10.000 arquivos/pastas. Edição sem senha.','Sem teste de todas as versões do Windows ou dos idiomas do mundo.']}
if (W/'REVISAO_ACOM.json').exists():raise FileExistsError('Review already exists')
(W/'REVISAO_ACOM.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf8')
print(json.dumps({'validated':True,'payload_files':len(contents),'deliveries':[d['bytes'] for d in delivery]},ensure_ascii=False))

