"""Independent source/custody review v390; no source program or Lean execution."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
from urllib.parse import quote
import hashlib,json,os,re,subprocess
W=Path(__file__).resolve().parents[1];A=W/'audit'
V=Path('C:/IALD/Central de Patentes/vault/originals_copy')
C=V/'um_unificado_v390';OLD=V/'um_unificado_v389'
CHAIN=Path('C:/IALD/Central de Patentes/work/cadeia_de_selo')
REPO=Path('C:/IALD/Artigo/the_boundary')
COMMIT='5cff2ebfec1be1b6f8a0d0c397af203de0004e1d'
pins={};checks=[]
def sha(x):return hashlib.sha256(x).hexdigest()
def raw(p):
 p=Path(p);b=p.read_bytes();h=sha(b)
 if str(p) in pins:assert pins[str(p)]==h,'Input changed'
 pins[str(p)]=h;return b
def load(p):return json.loads(raw(p))
def save(name,v):
 p=A/name;b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
 if p.exists():
  old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b;os.replace(tmp,p)
def check(name,ok,e=None):checks.append({'name':name,'passed':bool(ok),'evidence':e})
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+REPO.as_posix(),'-C',str(REPO),*args],stderr=subprocess.PIPE)
def diff(a,b,p=''):
 if type(a)!=type(b):return [{'pointer':p,'before':a,'after':b}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(a.keys()|b.keys()):
   q=p+'/'+str(k).replace('~','~0').replace('/','~1')
   if k not in a or k not in b:out.append({'pointer':q,'before':a.get(k),'after':b.get(k),'presence_changed':True})
   else:out+=diff(a[k],b[k],q)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [{'pointer':p,'before':a,'after':b,'length_changed':True}]
  return [x for i,(aa,bb) in enumerate(zip(a,b)) for x in diff(aa,bb,p+'/'+str(i))]
 return [] if a==b else [{'pointer':p,'before':a,'after':b}]

def main():
 custody=load(C/'CUSTODY_MANIFEST.json');new=load(C/'um_absoluto.json');old=load(OLD/'um_absoluto.json')
 seal=load(C/'um_absoluto_selo.json');oldseal=load(OLD/'um_absoluto_selo.json');proof=load(C/'tgl_kernel_proof_manifest.json')
 incpath=Path('C:/IALD/Central de Patentes/work/v390_selo/v390_incorporacao_manifesto.json');inc=load(incpath)
 artifacts=[]
 for item in custody['artifacts']:
  p=(C/item['file']).resolve();assert p.is_relative_to(C)
  b=raw(p);artifacts.append({'file':item['file'],'bytes':len(b),'sha256':sha(b),'expected_sha256':item['sha256'],'ok':sha(b)==item['sha256']})
 check('custody_all_artifacts',all(x['ok'] for x in artifacts) and len(artifacts)==custody['n_artifacts'],{'count':len(artifacts),'failed':[x['file'] for x in artifacts if not x['ok']]})
 check('program_seal_custody_binding',sha(raw(C/'um.py'))==custody['um_py_pin'] and custody['um_py_pin'].startswith(inc['um_py_sha16']) and len(raw(C/'um.py'))==inc['um_py_bytes'])
 check('same_gate_as_v389',seal['qg_closure_verdict']==oldseal['qg_closure_verdict']==inc['gate']==custody['gate'])
 check('formal_source_hash_binding',proof['formal_source_hash']==seal['formal_source_hash']==custody['formal_source_hash'])
 head=git('rev-parse','HEAD').decode().strip()
 remote=subprocess.check_output(['git','ls-remote','https://github.com/rotolimiguel-iald/the_boundary.git','refs/heads/main'],stderr=subprocess.PIPE).decode().strip().split()[0]
 check('local_public_head_same_commit',head==remote==COMMIT,{'local':head,'remote':remote})
 tree={}
 for line in git('ls-tree','-r','-z',COMMIT).split(b'\0'):
  if not line:continue
  meta,path=line.split(b'\t',1);mode,kind,oid=meta.split()
  if kind==b'blob':tree[path.decode()]=oid.decode()
 roots=[str(PurePosixPath(p).parent) for p in tree if PurePosixPath(p).name=='um.py'];assert len(roots)==1;root=roots[0]
 names=['um.py','um_absoluto.json','um_absoluto_selo.json','um_absoluto_forma_canonica.md','um_absoluto_manifest.md','um_absoluto_pt.txt','um_absoluto_en.txt','tgl_kernel_proof_manifest.json']
 published=[]
 for name in names:
  ps=[p for p in tree if p.startswith(root+'/') and PurePosixPath(p).name==name];assert len(ps)==1,(name,ps)
  p=ps[0];b=git('cat-file','blob',tree[p]);expected=raw(C/name)
  published.append({'file':name,'git_path':p,'git_blob':tree[p],'sha256':sha(b),'bytes':len(b),'matches_custody':b==expected,'url':'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+COMMIT+'/'+quote(p,safe='/')})
 check('eight_primary_git_blobs_equal_custody',all(x['matches_custody'] for x in published),len(published))
 f=new['core']['fundacao_v390'];lean_path=root+'/Lean/tgl_kernel/'+f['pedra']['path'];lean=git('cat-file','blob',tree[lean_path]);lt=lean.decode()
 check('foundation_source_hash_and_order_copy',sha(lean)==f['pedra']['sha256']==proof['formal_files_sha256'][f['pedra']['path']] and len(lean)==f['pedra']['bytes'] and lean==raw(CHAIN/'v390_ordem/Fundacao.lean'))
 ax=[]
 for clause in f['clausulas']:
  name=clause['teorema'];flag=clause['flag'];record=proof['axiom_report'].get(name)
  ok=(record is not None and set(record)<= {'propext','Classical.choice','Quot.sound'} and new['core']['kernel_formalization'].get(flag) is True and clause['no_kernel'] is True and re.search(r'(?m)^theorem '+re.escape(name.rsplit('.',1)[1])+r'\b',lt) is not None)
  ax.append({'name':name,'flag':flag,'axioms':record,'ok':ok})
 check('foundation_nine_declarations_recorded_clean',len(ax)==f['kernel_flags_ok']==f['kernel_flags_total']==9 and all(x['ok'] for x in ax) and not f['missing_flags'],ax)
 check('foundation_incorporation_manifest_semantics',all(f[k]==v for k,v in inc['fundacao'].items()),list(inc['fundacao']))
 for key,n in [('cunhagem_07out','CUNHAGEM_OPERADOR_07out_verbatim.txt'),('nomes_07out','CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt'),('concordo_07out','CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt')]:
  local=raw(CHAIN/'v390_ordem'/n);matches=[p for p in tree if PurePosixPath(p).name==n];assert len(matches)==1,matches
  pub=git('cat-file','blob',tree[matches[0]])
  check('verbatim_'+key,local==pub and sha(local)==f['verbatim'][key]['sha256']==inc['verbatins'][key]['sha256'] and len(local)==inc['verbatins'][key]['bytes'])
 check('order_bound',sha(raw(CHAIN/'v390_ordem/ORDEM_v390_FUNDACAO.md'))==f['pedra']['ordem_sha256'])
 chain=[]
 for section,folder in [('pacote','v390'),('ordem','v390_ordem')]:
  for name,pin in inc[section].items():
   p=CHAIN/folder/name;b=raw(p);chain.append({'path':str(p),'sha256':sha(b),'prefix_matches':sha(b).startswith(pin)})
 check('incorporation_chain_hash_prefixes',all(x['prefix_matches'] for x in chain),len(chain))
 check('chain_incorporation_copy',raw(CHAIN/'v390_incorporacao_manifesto.json')==raw(incpath))
 added=sorted(new['core'].keys()-old['core'].keys());removed=sorted(old['core'].keys()-new['core'].keys())
 changed={k:diff(old['core'][k],new['core'][k],'/core/'+k) for k in sorted(old['core'].keys()&new['core'].keys()) if old['core'][k]!=new['core'][k]}
 check('single_added_foundation_no_removed',added==['fundacao_v390'] and not removed,{'before':len(old['core']),'after':len(new['core']),'changed':len(changed)})
 check('P4_P5_F9_and_law_of_proof_preserved',all(new['core'][k]==old['core'][k] for k in ('bancada_fases_5_6_7_v380','hubble_ratio_opening_v388','retrodiction_reading_v387','ledger_errata_v386','text_label_errata_v389')))
 stdout=raw(C/'rodada_v390_stdout.txt').decode('utf8',errors='strict')
 check('published_round_counter_6163',re.search(r'6163\s*/\s*6163',stdout) is not None)
 check('no_kernel_claim_promotion',f['does_not_gate_core'] is True and len(f['not_claimed'])==3 and '[INPUT' not in f['not_claimed'][0] and 'H3 NOMEADA' in f['passagem'] and 'face finita' in f['passagem'] and '[KERNEL' in f['status'])
 check('review_inputs_stable',all(sha(Path(p).read_bytes())==h for p,h in pins.items()))
 save('scientific_delta.json',{'old_core_count':len(old['core']),'new_core_count':len(new['core']),'added':added,'removed':removed,'changed':changed})
 save('fundacao_v390_source.json',{'source_sha256':sha(raw(C/'um_absoluto.json')),'core_pointer':'/core/fundacao_v390','source_value':f,'declarations':ax,'lean_path':lean_path,'lean_sha256':sha(lean)})
 findings=[{'id':'V390-SEM-01','kind':'MUST_PRESERVE','text':'GLOBAL_LIFT := superposição é definição INPUT/ONTO do operador, não prova irrestrita da realização global.'},{'id':'V390-SEM-02','kind':'MUST_PRESERVE','text':'DualScalingData recebe a lei de escala como dado KNOWN; agape/abismo sob positividade e hipóteses nomeadas. Conservar face finita, hd, hinj, hU, hω na passagem.'},{'id':'V390-SEM-03','kind':'MUST_PRESERVE','text':'Jacobson KNOWN com H3 nomeada; Borchers sob contrato H2. Energia limitada inferiormente não deve ser identificada com gerador modular sem piso.'},{'id':'V390-SEM-04','kind':'MUST_PRESERVE','text':'Os três not_claimed e status/estatuto_do_fecho/leitura/recusa/passagem/borchers.leitura devem permanecer residentes. Nenhum campo essencial novo apenas por fetch.'},{'id':'V390-SEM-05','kind':'MUST_PRESERVE','text':'São três verbatins; kernel 6163/6163 conforme rodada publicada, não nova compilação do revisor. Gate idêntico à v389; NOT_FALSIFIED não vira confirmação.'},{'id':'V390-OPS-01','kind':'PACKAGE_PENDING','text':'Haiku exige contagem nativa vinculada ao prefixo final, saída/margem e reserva runtime >=10000; núcleo v5/core íntegros e 37 históricos da base final v389 devem ser conferidos no novo pacote.'}]
 save('findings.json',findings)
 failed=[x['name'] for x in checks if not x['passed']]
 report={'status':'SOURCE_PASS_PACKAGE_PENDING' if not failed else 'SOURCE_REVIEW_FAILED','reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'commit':COMMIT,'program_sha256':sha(raw(C/'um.py')),'checks_passed':len(checks)-len(failed),'checks_total':len(checks),'failed_checks':failed,'checks':checks,'custody_artifacts':artifacts,'published_primary':published,'chain_checks':chain,'delta_summary':{'added':added,'removed':removed,'changed_topics':len(changed)},'input_pins':pins,'scope':'Hash custody + immutable local Git blobs with current remote ref + static Lean/source fidelity + recorded published audit. No um.py import/execution, Lean compilation, API generation, production mutation. Package and deploy not approved yet.'}
 save('source_review.json',report)
 print(json.dumps({'status':report['status'],'commit':COMMIT,'checks':len(checks),'failed':failed,'custody':len(artifacts),'published':len(published),'new':added,'changed':len(changed)},ensure_ascii=False))
if __name__=='__main__':main()