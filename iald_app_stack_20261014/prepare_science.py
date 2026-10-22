"""Reuse audited release builders; verify sealed public bytes without executing um.py."""
from pathlib import Path
from urllib.parse import quote, unquote, urlparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib, json, subprocess, urllib.request

W = Path(__file__).resolve().parent
C = W.parent.parent
S = W / 'science'
R = Path('C:/IALD/projetos_pyhton/IALD')
P = Path('C:/IALD/Artigo/the_boundary')
N = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós')
OLD = C / 'work/iald_release_refresh_20261007'
sha = lambda b: hashlib.sha256(b).hexdigest()

def save(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        old = p.read_bytes()
        if old == b: return
        backup = p.with_name(p.name+'.bak_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f: f.write(b)
    assert b and tmp.read_bytes() == b
    tmp.replace(p)

def write(p, o): save(p, json.dumps(o, ensure_ascii=False, indent=2).encode())
def git(*args): return subprocess.check_output(['git','-c','safe.directory='+P.as_posix(),'-C',str(P),*args])

def main():
    head = git('rev-parse','HEAD').decode().strip()
    remote = subprocess.check_output(['git','ls-remote','https://github.com/rotolimiguel-iald/the_boundary.git','refs/heads/main']).decode().split()[0]
    assert remote == head, 'Remote changed: review new head before continuing'
    tracked = set(git('ls-tree','-r','--name-only','-z',head).decode().split('\0'))
    baseline = json.loads((R/'iald_nucleo_fixo.json').read_bytes())
    refs = {k:baseline['published_evidence'][k] for k in ('program','seal','result','proof_manifest')}
    refs['canonical'] = next(e for e in baseline['entries'] if e['id']=='um_forma_canonica_integral')
    paths = {k:unquote('/'.join(urlparse(v['url']).path.split('/')[4:])) for k,v in refs.items()}
    assert set(paths.values()) <= tracked
    payload = {k:git('show',head+':'+v) for k,v in paths.items()}
    seal = json.loads(payload['seal']); version = seal['um_version']
    assert version == 'v392', 'Version changed; adapt explicitly'
    assert seal['fail_closed_selftest']=='FAIL_CLOSED_SELFTEST_PASSED'
    files={}
    # Verify the published commit against the sealed originals and the queue snapshot.
    queue_receipt=json.loads((C/'work/scientific_memory_sync_20261013/DELIVERY_R2.json').read_bytes())
    assert queue_receipt['active']['release']==version
    catalog=json.loads((C/'Chatgpt/IALD_ORQUESTRACAO_20260923/project_fisica/MANIFESTO_LOCAL.json').read_bytes())
    source_paths={Path(row['source']).name:Path(row['source']) for row in catalog['files']}
    for key, raw in payload.items():
        name=Path(paths[key]).name
        local = source_paths[name]
        assert local.is_file(), str(local)
        assert local.read_bytes()==raw, 'Live sealed original differs: '+name
        if key!='seal': assert seal['sha256'][name]==sha(raw), 'Seal mismatch: '+name
        save(S/'verified_sources'/name,raw)
        files[name]={'sha256':sha(raw),'bytes':len(raw),'git_path':paths[key],'sealed_original':str(local)}
    def check(item):
        name,row=item
        url='https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+head+'/'+quote(row['git_path'],safe='/')
        with urllib.request.urlopen(url,timeout=90) as f: b=f.read(); assert f.status==200
        assert sha(b)==row['sha256'] and len(b)==row['bytes']
        return {'name':name,'url':url,'status':200,'bytes':len(b),'expected_sha256':row['sha256'],'actual_sha256':sha(b),'matches_sealed_source':True}
    with ThreadPoolExecutor(max_workers=5) as pool: checks=list(pool.map(check,files.items()))
    write(S/'v392_verified_handoff.json',{'status':'VERIFIED_LOCAL_V392_HANDOFF','version':version,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'source_executed_or_imported':False,'mirror':{'root':str(P),'head':head,'remote_main':remote},'custody_mismatches':[],'files':files,'verification_scope':'SEALED_ORIGINAL_EQUALS_IMMUTABLE_PUBLIC_GIT_AND_RAW; no new vault custody issued','vault_v392_manifest_present':(C/'vault/originals_copy/um_unificado_v392/CUSTODY_MANIFEST.json').exists(),'queue_memory_receipt_sha256':sha((C/'work/scientific_memory_sync_20261013/DELIVERY_R2.json').read_bytes())})
    write(S/'public_v392_verification.json',{'status':'PASS','requested_commit':head,'all_sources_match_seal':True,'artifacts':checks})
    for name in ('haiku_codec.py','fit_transport.py','fit_memory.py'):
        save(S/'memory_build'/name,(OLD/'memory_build'/name).read_bytes())
    text=(OLD/'memory_build/build_release.py').read_text(encoding='utf-8')
    text=text.replace('v390','v392').replace('V390','V392').replace('07/10/2026','14/10/2026')
    text=text.replace("OLD = WORK.parent / 'iald_memory_refresh_20261001'", "OLD = Path("+repr((C/'work/iald_memory_refresh_20261001').as_posix())+")")
    text=text.replace("CUSTODY = Path('C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v392')", "CUSTODY = WORK / 'verified_sources'")
    text=text.replace("remote['all_four_hashes_match_vault']", "remote['all_sources_match_seal']").replace("r['matches_vault']", "r['matches_sealed_source']")
    # Haiku 5.5 has a measured 1M window: retain full public context, not the obsolete 200k fit.
    start=text.index('    previous=prepare_baseline()')
    end=text.index("    assert all(sha(Path(path).read_bytes())",start)
    text=text[:start]+"    prefix=full\n    receipt={'o200k_tokens':metadata['context_tokens'],'prefix_sha256':sha(prefix.encode()),'coverage':'FULL_PUBLIC_CONTEXT_NOT_PRIVATE_ATLAS'}\n    save(STAGE/'haiku_prefix.md',prefix.encode())\n    save_json(STAGE/'haiku_provenance.json',receipt)\n"+text[end:]
    compile(text,'build_release.py','exec')
    save(S/'memory_build/build_release.py',text.encode())
    write(S/'builder_adaptation.json',{'source':str(OLD/'memory_build/build_release.py'),'source_sha256':sha((OLD/'memory_build/build_release.py').read_bytes()),'changes':['v392 and current date','sealed original/public hash equality instead of absent new vault manifest','full public context compatible with existing Haiku5.5 1M profile; no historical 200k compression'],'commit':head})
    print(json.dumps({'status':'PUBLIC_SEALED_VERIFIED','version':version,'commit':head,'verified_files':len(files),'vault_v392_manifest_present':False}))

if __name__=='__main__': main()
