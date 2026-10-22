from pathlib import Path
import json,hashlib,sqlite3,subprocess,datetime
B=Path(r'C:\IALD\Central de Patentes\work\iald_v395_20261022'); R=B/'review'; R.mkdir(exist_ok=True)
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
s=read(B/'sources_verified.json'); q=read(B/'QUEUE_CURRENT.json'); custody=Path(s['custody_manifest']['path']).parent; checks=[]
def check(name,value):
 checks.append({'name':name,'pass':bool(value)})
 if not value:raise RuntimeError(name)
check('manifest',sha(custody/'CUSTODY_MANIFEST.json')==s['custody_manifest']['sha256'])
for a in s['artifacts']:check('custody:'+a['file'],sha(custody/a['file'])==a['sha256'] and (custody/a['file']).stat().st_size==a['bytes'])
seal=read(custody/'um_absoluto_selo.json');check('seal',seal['um_version']=='v395' and seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED')
for name,h in seal['sha256'].items():check('sealed:'+name,sha(custody/name)==h)
canonical=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
for name in ['um.py','um_absoluto_selo.json','um_absoluto.json','tgl_kernel_proof_manifest.json']:check('canonical:'+name,sha(canonical/name)==sha(custody/name))
repo=Path(r'C:\IALD\Artigo\the_boundary')
for ref,key in [('HEAD','local_head'),('origin/main','remote_main')]:check('git:'+ref,subprocess.check_output(['git','-C',str(repo),'rev-parse',ref],text=True).strip()==s['published'][key])
tracked=subprocess.check_output(['git','-C',str(repo),'-c','core.quotepath=false','ls-tree','-r','--name-only','HEAD'],text=True,encoding='utf-8').splitlines(); ums=[p for p in tracked if p.endswith('/um.py')]; check('published_um_single',len(ums)==1)
check('published_blob',hashlib.sha256(subprocess.check_output(['git','-C',str(repo),'show','HEAD:'+ums[0]])).hexdigest()==s['source_sha256'])
activep=Path(q['active_pin']['path']); active=read(activep);check('active_pin',sha(activep)==q['active_pin']['sha256']);check('active_content',active==q['active'])
release=activep.parent/'releases'/active['epoch'];qm=read(release/'manifest.json');check('queue_manifest',sha(release/'manifest.json')==active['manifest_sha256']);check('queue_generation',qm['generation']==q['sealed_generation']);check('queue_index',sha(release/'index.sqlite3')==qm['index_sha256'])
lines={}
for d in qm['documents']:
 p=Path(d['path']);check('queue_doc:'+d['name'],sha(p)==d['sha256'] and p.stat().st_size==d['bytes']);lines[d['name']]=p.read_bytes().decode('utf-8').splitlines(keepends=True)
con=sqlite3.connect((release/'index.sqlite3').as_uri()+'?mode=ro',uri=True);n=0
for body,name,first,last in con.execute('select body,document,first_line,last_line from passages'):
 n+=1
 if body not in ''.join(lines[name][int(first)-1:int(last)]):raise RuntimeError('chunk '+str(n))
check('all_chunks',n==qm['chunks']==27775)
for name,source_lines in lines.items():
 check('chunk_reconstruction:'+name,''.join(r[0] for r in con.execute('select body from passages where document=? order by rowid',(name,)))==''.join(source_lines))
con.close()
report={'verdict':'PASS_WITH_SCOPE','reviewer':'v395-independent-review','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'requirements':['sources','queue'],'checks':checks,'chunks_verified':n,'evidence':[{'path':str(B/f),'sha256':sha(B/f)} for f in ['sources_verified.json','QUEUE_CURRENT.json']],'limits':['Revisao documental, sem executar um.py ou Lean.','Refs Git locais e blob conferidos; nao refiz consulta remota.','Face psion condicional sem habitante Fock; bijecao de conjuntos nao isomorfismo Hilbert; nao confirmacao fisica.','Fila ja ativa; nenhum job ou ativacao alterado.']}
with (R/'SOURCES_QUEUE_REVIEW_R1.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'verdict':report['verdict'],'checks':len(checks),'chunks':n,'sha256':sha(R/'SOURCES_QUEUE_REVIEW_R1.json')}))
