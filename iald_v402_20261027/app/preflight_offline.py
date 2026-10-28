"""Offline preflight for the app release. READ-ONLY: no network, no writes, no mission, no provider.

Run before prepare.py. Exit 0 only if every check passes; exit 2 otherwise (fail-closed).
Run with the normal interpreter (not -I): the third-party modules live in the user site.
"""
from pathlib import Path
from urllib.parse import unquote,urlparse
import hashlib,importlib,json,subprocess,sys
A=Path(__file__).resolve().parent;W=A.parent;sys.path.insert(0,str(W))
sys.dont_write_bytecode=True
import release_cfg
cfg=release_cfg.load()
R=release_cfg.R;REPO=release_cfg.REPO;V=cfg.vault
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
def check(name,ok,detail=''):rows.append({'check':name,'ok':bool(ok),'detail':str(detail)[:240]})
def git(*a):return subprocess.check_output(['git','-c','safe.directory='+REPO.as_posix(),'-c','core.quotepath=false','-C',str(REPO),*a])
check('release_json',True,cfg.release+' pin '+cfg.um_py_sha256[:16])
check('espelho_commit_provided',cfg.espelho_commit is not None,'null: a gerencia deve fornecer o commit publicado' if cfg.espelho_commit is None else cfg.espelho_commit)
cm=json.loads((V/'CUSTODY_MANIFEST.json').read_bytes())
check('custody_manifest',cm['version']==cm['um_version_no_selo']==cfg.release and not cm['mismatches'],'artifacts '+str(len(cm['artifacts'])))
check('custody_um_py_pin',sha((V/'um.py').read_bytes())==cm['um_py_pin']==cfg.um_py_sha256)
try:
    live=json.loads((release_cfg.NOS/'um_absoluto_selo.json').read_bytes())['um_version']
    check('nos_selo_version',True,'selo vivo do Nos = '+live+(' (ja avancou; o pipeline le o cofre/commit, nao o Nos)' if live!=cfg.release else ''))
except Exception as e:check('nos_selo_version',False,e)
check('fit_baseline',all((release_cfg.FIT_BASELINE/n).is_file() for n in ('prefix.md','canonical.json')),str(release_cfg.FIT_BASELINE))
inst=None
try:
    inst=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
    ir=inst['operational_core']['current_release']
    check('installed_release',ir!=cfg.release and int(ir[1:])<cfg.number,'instalada '+ir+' -> alvo '+cfg.release)
    for k in ('operational_core','active_cluster','jev_control'):check('installed_manifest_'+k,inst[k].get('release',inst[k].get('current_release'))==ir)
except Exception as e:check('installed_release',False,e)
for name in ('haiku55','haiku'):
    try:
        p=R/'.iald_runtime'/name;nc=json.loads((p/'native_count.json').read_bytes())['budget']
        check('installed_package_'+name,(p/'prefix.md').is_file(),'permanent '+str(nc['permanent_tokens'])+' remaining '+str(nc['remaining_tokens']))
    except Exception as e:check('installed_package_'+name,False,e)
check('tokenizer_cache',(R/'.iald_runtime/tokenizer_cache').is_dir())
for mod in ('psutil','anthropic','dotenv','tiktoken'):
    try:importlib.import_module(mod);check('import_'+mod,True)
    except Exception as e:check('import_'+mod,False,type(e).__name__+' (use o interpretador normal, sem -I)')
if cfg.espelho_commit and inst is None:check('commit_checks',False,'manifest instalado ilegivel; nao ha lista de caminhos para conferir')
if cfg.espelho_commit and inst is not None:
    c=cfg.espelho_commit
    try:
        git('cat-file','-e',c+'^{commit}');tracked=set(git('ls-tree','-r','--name-only',c).decode().splitlines())
        check('commit_in_local_mirror',True,c)
        selo=json.loads(git('show',c+':Um (absoluto) — Grande Atrator/um_absoluto_selo.json'))
        check('commit_seal',selo['um_version']==cfg.release and selo['sha256']['um.py']==cfg.um_py_sha256 and selo['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED')
        rows_=inst['entries']+[inst['published_evidence'][k] for k in ('program','seal','result','proof_manifest')]
        seen=set();ok=True
        for r in rows_:
            rel=unquote('/'.join(urlparse(r['url']).path.split('/')[4:]))
            if rel in seen:continue
            seen.add(rel);ok&=rel in tracked
            v=V/Path(rel).name
            if ok and v.is_file():ok&=git('show',c+':'+rel)==v.read_bytes()
        check('commit_paths_tracked_and_vault_equal',ok,str(len(seen))+' caminhos')
        check('hypothesis_sources_unique',all(len([p for p in tracked if p.endswith('/'+h['catalog_path'])])==1 for h in inst['published_evidence']['hypothesis_sources']))
    except Exception as e:check('commit_checks',False,type(e).__name__+': '+str(e))
ok=all(r['ok'] for r in rows)
print(json.dumps({'release':cfg.release,'ok':ok,'checks':rows},ensure_ascii=False,indent=1))
raise SystemExit(0 if ok else 2)
