"""Independent reviewer script (sonnet-app-v404-revisor): check group 1 -- RELEASE.json, ls-remote, blobs at both commits.
No network here: the ls-remote stdout literal is passed as argv[1] (done once before, by the reviewer)."""
import json,hashlib,subprocess,sys,re
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');REPO=Path(r'C:\IALD\Artigo\the_boundary')
V=Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v404')
NOS=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
sh=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','core.quotepath=false','-C',str(REPO),*a])
out=[];ok=True
def chk(n,v,achado=None):
    global ok
    out.append({'n':len(out)+1,'name':n,'ok':bool(v),'achado':achado});ok&=bool(v)
ls=sys.argv[1].split()
rel=json.loads((W/'app/RELEASE.json').read_bytes())
chk('RELEASE.json exact keys',set(rel)=={'release','espelho_commit','um_py_sha256'},sorted(rel))
chk('release == v404',rel['release']=='v404')
chk('espelho_commit == ls-remote origin refs/heads/main (literal from the single network call)',ls[0]==rel['espelho_commit'] and ls[1]=='refs/heads/main',ls)
chk('espelho_commit is 40 hex',bool(re.fullmatch(r'[0-9a-f]{40}',rel['espelho_commit'])))
seal_v=json.loads((V/'um_absoluto_selo.json').read_bytes());seal_n=json.loads((NOS/'um_absoluto_selo.json').read_bytes())
chk('selo cofre um_version == v404',seal_v['um_version']=='v404')
chk('selo Nos um_version == v404',seal_n['um_version']=='v404',seal_n['um_version'])
chk('selo cofre sha256.um.py == RELEASE.um_py_sha256',seal_v['sha256']['um.py']==rel['um_py_sha256'],seal_v['sha256']['um.py'])
chk('selo Nos sha256.um.py == RELEASE.um_py_sha256',seal_n['sha256']['um.py']==rel['um_py_sha256'])
chk('selo cofre == selo Nos (bytes)',(V/'um_absoluto_selo.json').read_bytes()==(NOS/'um_absoluto_selo.json').read_bytes())
chk('bytes of cofre um.py hash == pin',sh((V/'um.py').read_bytes())==rel['um_py_sha256'])
chk('bytes of Nos um.py hash == pin',sh((NOS/'um.py').read_bytes())==rel['um_py_sha256'])
C1=rel['espelho_commit'];C0='3ae6f43fcb11bea868673415a54ce5933eaa3527'
chk('3ae6f43f is an ancestor of the pinned commit',subprocess.call(['git','-C',str(REPO),'merge-base','--is-ancestor',C0,C1])==0)
chk('pinned commit is local HEAD and origin/main',git('rev-parse','HEAD').decode().strip()==C1==git('rev-parse','origin/main').decode().strip())
tr=git('ls-tree','-r','--name-only','-z',C1).decode().split('\0')
ump=[p for p in tr if Path(p).name=='um.py'];chk('exactly one um.py tracked at pinned commit',len(ump)==1,ump)
b1=git('show',C1+':'+ump[0]);b0=git('show',C0+':'+ump[0])
chk('um.py blob at pinned commit sha256 == RELEASE pin == cofre selo == Nos selo',sh(b1)==rel['um_py_sha256']==seal_v['sha256']['um.py']==seal_n['sha256']['um.py'],sh(b1))
chk('um.py blob identical at custody commit and pinned commit',b0==b1)
# every file prepare.py reads
bind=json.loads((W/'app/PUBLIC_GIT_BINDING.json').read_bytes())
diff=[]
for relp,row in bind['sources'].items():
    x1=git('show',C1+':'+relp);x0=git('show',C0+':'+relp)
    chk('binding sha == blob at pinned commit: '+relp,sh(x1)==row['sha256'] and len(x1)==row['bytes'])
    if x0!=x1:diff.append(relp)
chk('files prepare reads that differ between 3ae6f43f and pinned: exactly README.md and read-brief.md',sorted(diff)==['README.md','read-brief.md'],sorted(diff))
# selo, core, proof manifest and canonical form: identical at both commits
for nm in ['um_absoluto_selo.json','um_absoluto.json','um_absoluto_forma_canonica.md','Lean/tgl_kernel_proof_manifest.json','um_absoluto_pt.txt']:
    rp=[p for p in tr if p.endswith(nm) and 'Grande Atrator' in p and 'fontes_pinadas' not in p]
    chk('exactly one '+nm+' under Grande Atrator',len(rp)==1,rp)
    chk(nm+' identical at both commits',git('show',C0+':'+rp[0])==git('show',C1+':'+rp[0]))
# selo at pinned == cofre selo; core/proof/forma == cofre
sel=[p for p in tr if p.endswith('um_absoluto_selo.json') and 'Grande Atrator' in p and 'fontes_pinadas' not in p][0]
chk('selo at pinned commit == cofre selo bytes',git('show',C1+':'+sel)==(V/'um_absoluto_selo.json').read_bytes())
for nm,loc in [('um_absoluto.json','um_absoluto.json'),('um_absoluto_forma_canonica.md','um_absoluto_forma_canonica.md'),('Lean/tgl_kernel_proof_manifest.json','tgl_kernel_proof_manifest.json')]:
    rp=[p for p in tr if p.endswith(nm) and 'Grande Atrator' in p and 'fontes_pinadas' not in p][0]
    chk(nm+' at pinned commit == cofre',git('show',C1+':'+rp)==(V/loc).read_bytes())
    chk(nm+' sha == selo.sha256[...]',sh(git('show',C1+':'+rp))==seal_v['sha256'][loc.split('/')[-1]])
# README/read-brief: word-level diff; every changed token run must be in the declared correction, the date/size regeneration, or ESTADO_ATUAL size
import difflib
for nm in ['README.md','read-brief.md']:
    a=git('show',C0+':'+nm).decode('utf-8');b=git('show',C1+':'+nm).decode('utf-8')
    aw=re.split(r'(\s+)',a);bw=re.split(r'(\s+)',b)
    sm=difflib.SequenceMatcher(None,aw,bw,autojunk=False);ch=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!='equal':ch.append((''.join(aw[max(0,i1-2):i2+1])[:260],''.join(bw[max(0,j1-2):j2+1])[:260]))
    chk(nm+' word-level changes: '+str(len(ch)),len(ch)>0,ch)
print(json.dumps({'ok':ok,'n':len(out),'passed':sum(o['ok'] for o in out),'checks':out},ensure_ascii=False,indent=1))
