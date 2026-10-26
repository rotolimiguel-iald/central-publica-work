"""Exact all-field comparison with source-derived, narrowly authorized deltas."""
import ast
import copy
import datetime
import hashlib
import math
import re
from manage_v401_data import B, C, S, ORDER, read, pin, sha, save, check, stable_seal

FILES = ['hud.json', 'frames.json', 'scene.json', 'PROVENANCE_PUBLIC.json', 'STDOUT_LINES.json', 'MANIFEST.json']

def digest(raw): return hashlib.sha256(raw).hexdigest()

def differences(a, b, path=''):
    if type(a) is not type(b):
        return [{'path':path, 'before':a, 'after':b, 'kind':'type'}]
    if isinstance(a, dict):
        out=[]
        for k in sorted(a.keys() | b.keys()):
            p=path+'/'+k.replace('~','~0').replace('/','~1')
            if k not in a or k not in b:
                out.append({'path':p,'before':a.get(k),'after':b.get(k),'kind':'key'})
            else: out += differences(a[k],b[k],p)
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':path,'before_length':len(a),'after_length':len(b),'kind':'array_length'}]
        return [r for i,(x,y) in enumerate(zip(a,b)) for r in differences(x,y,path+'/'+str(i))]
    if isinstance(a,float): assert math.isfinite(a) and math.isfinite(b), path
    return [] if a==b else [{'path':path,'before':a,'after':b,'kind':'value'}]

def inspect(root):
    seal=read(root/'source/um_absoluto_selo.json')
    core=read(root/'source/um_absoluto.json')['core']
    proof=read(root/'source/tgl_kernel_proof_manifest.json')
    docs={name:read(root/'data'/name) for name in FILES}
    prov=docs['PROVENANCE_PUBLIC.json']; hud=docs['hud.json']; stdout=docs['STDOUT_LINES.json']
    for name,rec in prov['sources'].items():
        f=root/'source'/name
        assert rec=={'path':name,'bytes':f.stat().st_size,'sha256':sha(f)}, name
        if name in seal['sha256']:assert sha(f)==seal['sha256'][name],name
    assert docs['MANIFEST.json']==prov
    assert (root/'PROVENANCE_PUBLIC.json').read_bytes()==(root/'data/PROVENANCE_PUBLIC.json').read_bytes()
    ladder=core['estatuto_da_prova_v391']['prova_1_kernel']
    counts={'proof_ladder_clean':ladder['n_theorems_clean'], 'proof_ladder_total':ladder['n_theorems_expected'],
            'formal_count':len(proof['formal_files_sha256']), 'declaration_count':len(proof['axiom_report'])}
    assert counts['declaration_count']==ladder['declaracoes_auditadas']
    for k in ['formal_files_sha256','axiom_report','formal_source_hash']:
        assert core['kernel_formalization'][k]==proof[k], k
    assert {k:hud['extra'][k] for k in counts}==counts
    assert prov['kernel']['formal_source_hash']==proof['formal_source_hash']
    assert prov['seal_version']==hud['seal_version']==seal['um_version']
    assert prov['selo']['timestamp']==hud['seal_timestamp']==hud['selo_timestamp']==seal['timestamp']
    assert prov['selo']['result_hash']==seal['result_hash']
    assert hud['result_hash16']==seal['result_hash'][:16]
    assert hud['seal_pin']==seal['sha256']['um.py'] and prov['um_sha16']==hud['seal_pin'][:16]
    assert stdout['source']==f"rodada_{seal['um_version']}_stdout.txt"
    assert stdout['source_sha256']==sha(root/'source'/stdout['source'])==hud['stdout_sha256']
    assert hud['stdout_lines']==stdout['lines']
    lines=(root/'source'/stdout['source']).read_bytes().splitlines(keepends=True)
    for row in stdout['lines']:
        raw=lines[row['line']-1]
        assert digest(raw)==row['line_sha256']
        assert raw.decode('utf-8').rstrip('\r\n')==row['text']
        assert digest(row['text'].encode())==row['text_sha256']
    ratio=re.search(r'teoremas limpos:\s*(\d+)\s*/\s*(\d+)', (root/'source'/stdout['source']).read_text(encoding='utf-8'))
    assert [int(ratio[1]),int(ratio[2])]==[counts['proof_ladder_clean'],counts['proof_ladder_total']]
    src=(root/'source/um.py').read_bytes(); src_lines=src.splitlines(keepends=True)
    functions={x.name:x for x in ast.parse(src).body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
    sections={}
    for name,rng in prov['source_code_sections'].items():
        fn=functions[name]
        assert rng=={'start':fn.lineno,'end':fn.end_lineno}
        sections[name]=b''.join(src_lines[fn.lineno-1:fn.end_lineno])
    assert len(prov['anchors'])>=64 and prov['anchors_all_ok'] is True
    for a in prov['anchors']:
        assert a['ok'] is True and math.isfinite(a['residual']) and 0<=a['residual']<=a['tol'],a['name']
        assert math.isfinite(a['json_value']) and math.isfinite(a['live_value'])
    return {'docs':docs,'seal':seal,'counts':counts,'proof':proof,'sections':sections,'source_lines':src_lines}

def expected_from(old,new):
    d=copy.deepcopy(old['docs']); ns=new['seal']; nc=new['counts']; nd=new['docs']
    h=d['hud.json']; p=d['PROVENANCE_PUBLIC.json']; st=d['STDOUT_LINES.json']
    h['extra'].update(nc)
    by_id={'theorems':'proof_ladder_clean','n_formal':'formal_count',**{k:k for k in nc}}
    for item in h['items']:
        if item['id'] in by_id:
            item['value']=nc[by_id[item['id']]]
            item['text']=f"{nc['proof_ladder_clean']}/{nc['proof_ladder_total']}" if item['id']=='theorems' else str(item['value'])
        elif item['id']=='um_sha16':item['value']=item['text']=ns['sha256']['um.py'][:16]
    for field in ['seal_timestamp','selo_timestamp']:h[field]=ns['timestamp']
    h.update(seal_version=ns['um_version'],seal_pin=ns['sha256']['um.py'],result_hash16=ns['result_hash'][:16])
    d['scene.json']['source_sha256']=ns['sha256']['um.py']
    old_ratio=f"{old['counts']['proof_ladder_clean']}/{old['counts']['proof_ladder_total']}"
    new_ratio=f"{nc['proof_ladder_clean']}/{nc['proof_ladder_total']}"
    assert len(st['lines'])==len(nd['STDOUT_LINES.json']['lines'])
    for before,after in zip(st['lines'],nd['STDOUT_LINES.json']['lines']):
        expected_text=before['text']
        if re.search(r'teoremas limpos:\s*'+re.escape(old_ratio),expected_text):
            expected_text=expected_text.replace(old_ratio,new_ratio,1)
        assert after['text']==expected_text, 'STOP: other stdout text changed'
        assert after['chapter']==before['chapter']
        before.update(line=after['line'],text=expected_text,line_sha256=after['line_sha256'],text_sha256=digest(expected_text.encode()))
    st['source']=nd['STDOUT_LINES.json']['source'];st['source_sha256']=sha(S/'source'/st['source'])
    h['stdout_lines']=copy.deepcopy(st['lines']);h['stdout_sha256']=st['source_sha256']
    anchor_counts={'proof ladder clean':'proof_ladder_clean','proof ladder expected':'proof_ladder_total',
                   'kernel formal files':'formal_count','kernel declarations':'declaration_count',
                   **{'HUD '+k:k for k in nc}}
    for a in p['anchors']:
        if a['name'] in anchor_counts:a['json_value']=a['live_value']=nc[anchor_counts[a['name']]]
    p['kernel'].update(theorems_clean=nc['proof_ladder_clean'],theorems_total=nc['proof_ladder_total'],
                       axiom_report_entries=nc['declaration_count'],formal_files=nc['formal_count'],
                       formal_source_hash=new['proof']['formal_source_hash'])
    p['seal_version']=ns['um_version'];p['generated_at']=ns['timestamp'];p['um_sha16']=ns['sha256']['um.py'][:16]
    p['selo'].update(timestamp=ns['timestamp'],result_hash=ns['result_hash'])
    p['sources']=copy.deepcopy(nd['PROVENANCE_PUBLIC.json']['sources'])
    assert set(p['sources'])=={'um.py','um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json',st['source']}
    assert old['sections']==new['sections'], 'STOP: scientific function text changed'
    p['source_code_sections']=copy.deepcopy(nd['PROVENANCE_PUBLIC.json']['source_code_sections'])
    d['MANIFEST.json']=copy.deepcopy(p)
    return d

def verify_replay(new):
    manifest=read(S/'replay/replay-manifest.json'); previous=read(B/'replay/replay-manifest.json')
    assert manifest['source']=={'name':'um.py','version':'v401','sha256':sha(S/'source/um.py'),'bytes':(S/'source/um.py').stat().st_size}
    assert manifest['seal']=={'sha256':sha(S/'source/um_absoluto_selo.json'),'timestamp':new['seal']['timestamp']}
    assert manifest['core_sha256']==sha(S/'source/um_absoluto.json')
    excerpt=(S/'replay/um_nucleo_filme.py').read_bytes()
    for rng in manifest['excerpt_ranges']:
        raw=b''.join(new['source_lines'][rng['source_start_line']-1:rng['source_end_line']])
        assert digest(raw)==rng['sha256']
        assert excerpt[rng['excerpt_byte_start']:rng['excerpt_byte_end']]==raw
    rng=manifest['scalar_range'];raw=b''.join(new['source_lines'][rng['source_start_line']-1:rng['source_end_line']])
    assert raw==(S/'replay/um_scalar_excerpt.py').read_bytes() and digest(raw)==rng['sha256']
    for asset in manifest['assets'].values():
        path=S/'replay'/asset['url'];assert sha(path)==asset['sha256'] and path.stat().st_size==asset['bytes']
    assert manifest['vendor']==previous['vendor'] and manifest['tolerance_policy']==previous['tolerance_policy']
    assert (S/'replay/anchors.json').read_bytes()==(B/'replay/anchors.json').read_bytes()
    assert excerpt==(B/'replay/um_nucleo_filme.py').read_bytes()
    for f in manifest['vendor']['files']:
        path=S/'web/vendor/pyodide'/f['name'];assert sha(path)==f['sha256'] and path.stat().st_size==f['bytes']
    assert sum(x['bytes'] for x in manifest['vendor']['files'])==manifest['vendor']['total_bytes']<=25000000
    for name in ['TEST_OFFLINE.json','TEST_BROWSER.json']:
        r=read(S/'replay'/name)
        assert r['status']=='PASS' and r['source']=='v401' and r['source_sha256']==manifest['source']['sha256']
        assert r['manifest_sha256']==sha(S/'replay/replay-manifest.json')
    assert read(S/'replay/TEST_OFFLINE.json')['tests']==13
    browser=read(S/'replay/TEST_BROWSER.json')
    assert len(browser['result']['rows'])==61 and all(x['ok'] for x in browser['result']['rows'])
    assert all(x['ok'] for x in browser['checks']) and not browser['external_requests']
    return {'exact_excerpt_ranges':len(manifest['excerpt_ranges']),'scalar_range_exact':True,'offline_tests':13,
            'browser_numeric_checks':61,'browser_control_groups':len(browser['checks']),'vendor_bytes':manifest['vendor']['total_bytes'],
            'tolerances_unchanged':True,'excerpt_bytes_unchanged':True}

def run():
    preflight=check();stable_seal()
    old=inspect(B);new=inspect(S)
    assert old['seal']['um_version']=='v400' and new['seal']['um_version']=='v401'
    assert list(old['counts'].values())==[9541,9541,1429,29296]
    assert list(new['counts'].values())==[9561,9561,1430,29318]
    expected=expected_from(old,new)
    results=[];unexpected=[]
    for name in FILES:
        bad=differences(expected[name],new['docs'][name]);unexpected += [{'file':name,**x} for x in bad]
        delta=differences(old['docs'][name],new['docs'][name])
        results.append({'file':name,'before':pin(B/'data'/name),'after':pin(S/'data'/name),
                        'identical_bytes':sha(B/'data'/name)==sha(S/'data'/name),'differences':delta,'unexpected':bad})
    negatives=[]
    for label,alter in [('other_number',lambda x:x['hud.json']['extra'].__setitem__('threshold_sigma',99)),
                        ('array_length',lambda x:x['hud.json']['items'].pop()),
                        ('unapproved_text',lambda x:x['STDOUT_LINES.json']['lines'][0].__setitem__('text','alterado')),
                        ('new_field',lambda x:x['scene.json'].__setitem__('unapproved_field',True))]:
        mutated=copy.deepcopy(expected);alter(mutated)
        refused=any(differences(expected[n],mutated[n]) for n in FILES);assert refused
        negatives.append({'name':label,'refused':refused})
    replay=verify_replay(new);stable_seal()
    report={'status':'PASS' if not unexpected else 'STOP_UNAUTHORIZED_DELTA','source':'v401',
            'source_sha256':sha(S/'source/um.py'),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'order':pin(ORDER),'baseline':pin(C/'BASELINE_MANIFEST.json'),'source_capture':pin(C/'SOURCE_CAPTURE.json'),
            'preflight':preflight,'method':'Exact recursive comparison of every field, type, scalar, array length and element; source-derived allowed deltas only; no comparison tolerance.',
            'scope':'Six exported JSONs plus identical root provenance; full historical stdout is archived, only selected lines are displayed and compared. No empirical confirmation or Lean rebuild.',
            'authorized_counts':{k:{'before':old['counts'][k],'after':v} for k,v in new['counts'].items()},
            'metadata_validation':'Source hashes/bytes, sealed version/timestamp/result hash, formal source hash, AST line ranges, selected stdout bytes and line hashes verified independently against files.',
            'anchors':{'total':len(new['docs']['PROVENANCE_PUBLIC.json']['anchors']),
                       'serialization_checks':sum('serialization' in a.get('method','') for a in new['docs']['PROVENANCE_PUBLIC.json']['anchors']),
                       'all_ok':True,'note':'Serialization checks are explicitly labeled and are not independent proofs.'},
            'files':results,'unexpected_differences':unexpected,'negative_controls':negatives,'replay':replay,
            'seals':{'before':pin(B/'source/um_absoluto_selo.json'),'after':pin(S/'source/um_absoluto_selo.json')}}
    save(C/'NUMERIC_COMPARISON.json',report)
    print({'status':report['status'],'diff_counts':{x['file']:len(x['differences']) for x in results},'replay':replay})
    assert not unexpected, unexpected
    return report

if __name__=='__main__':run()
