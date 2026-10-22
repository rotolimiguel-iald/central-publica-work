from pathlib import Path
import datetime, hashlib, json, os

rev = Path(__file__).resolve().parent
p = rev / 'run_scalar_vna_partial_review.py'
t = p.read_text(encoding='utf-8')
t = t.replace("'scalar_vna_partial_independent_'", "'scalar_vna_final_independent_'")
t = t.replace("Path((REV/'right_vector_final_latest_run.txt').read_text().strip())]", "Path((REV/'right_vector_final_latest_run.txt').read_text().strip()),Path((REV/'scalar_vna_partial_latest_run.txt').read_text().strip())]")
a=t.index('spec=['); b=t.index('\nsources=', a)
t=t[:a]+"spec=[('ScalarGNSVonNeumann','20260913_005858_479525',10)]"+t[b:]
t=t.replace('sources={};raws={};targets=[];history=[]', 'sources={};raws={};targets=list(m[\'declarations\']);history=[]')
t=t.replace('==17', '==27')
t=t.replace("'PARTIAL_THREE_MODULES_ONLY'", "'FINAL_FOUR_MODULES_WITH_THREE_REUSED_OWN_COMPILES'")
t=t.replace("'scalar_vna_partial_latest_run.txt',str(RUN)", "'scalar_vna_final_latest_run.txt',str(RUN)")
t=t.replace("audit=''.join", "audit=''.join('import '+n[:-5].replace('/','.')+'\\n' for n in m['sources'])+''.join")
t=t.replace('ScalarVNAPartialAudit', 'ScalarVNAFinalAudit')
t=t.replace('len(records)==4', 'len(records)==2')
t=t.replace('exact_17_targets', 'exact_27_targets')
t=t.replace('three_binaries_equal_author', 'new_binary_equals_author')
t=t.replace('len(records)>=3', 'len(records)>=1').replace('records[:3]', 'records[:1]')
extra='''
draft_path=ROOT/'scalar_vna_draft_status.json';draft=load(draft_path)
assert draft['parent_custody_sha256']==hf(ROOT/'right_vector_custody.json')
assert draft['integrated_working_sha256']==hf(ROOT/'um.py') and not draft['integrated']
assert set(draft['targets'])==set(targets) and len(draft['modules'])==4
for name,pin in draft['modules'].items():
    rel='TGLV350/'+name+'.lean';orig=ROOT/'kernel'/rel;lp=Path(pin['final_log']);lr=load(lp)
    assert hf(orig)==pin['source_sha256']==lr['sha256'] and hf(Path(lr['command'][2]))==pin['binary_sha256']==lr['output_sha256']
    assert hf(lp)==pin['final_log_sha256'] and lr['returncode']==lr['lean_returncode']==0 and lr['source_unchanged_during_compile'] and lr['output_exists']
    assert hf(lr['stdout'])==pin['stdout_sha256'] and hf(lr['stderr'])==pin['stderr_sha256']
    if name!='ScalarGNSVonNeumann':
        d=deps['TGLV350.'+name]
        assert d['source_sha256']==pin['source_sha256'] and d['sha256']==pin['binary_sha256']
assert hf(draft['report_path'])==draft['report_sha256']
frozen_docs={}
for n in ['scalar_vna_draft_status.json','RELATORIO_IMAGEM_ESCALAR_VON_NEUMANN_DEV.md','make_scalar_vna_helpers.py','record_scalar_vna_draft.py','prepare_scalar_vna_stage.py','record_scalar_vna_progress.py','verify_scalar_vna_custody.py']:
    b=(ROOT/n).read_bytes();write(RUN/'documents'/n,b);artifacts[str(ROOT/n)]=sha(b);frozen_docs[n]=sha(b)
manifest['cumulative_draft_pins']=frozen_docs
manifest['reused_three_compilation']=str(origins[-1]/'compilation.json')
manifest['reused_three_compilation_sha256']=hf(origins[-1]/'compilation.json')
'''
t=t.replace("save(RUN/'manifest.json',manifest);",extra+"\nsave(RUN/'manifest.json',manifest);")
t=t.replace("save(RUN/'compilation.json',result);print", "result['cumulative_four_pins_preserved']=all(hf(ROOT/'kernel/TGLV350'/(n+'.lean'))==p['source_sha256'] and hf(ROOT/'build/TGLV350'/(n+'.olean'))==p['binary_sha256'] for n,p in draft['modules'].items())\nresult['cumulative_27_axioms_match_draft']=records[-1]['axioms']==draft['targets'] if len(records)==2 else False\nsave(RUN/'compilation.json',result);print")
out=rev/'run_scalar_vna_final_review.py'
raw=t.encode('utf-8');compile(t,str(out),'exec')
if out.exists():
    old=out.read_bytes();bk=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bk.write_bytes(old);assert bk.read_bytes()==old
tmp=out.with_name(out.name+'.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;os.replace(tmp,out)
print(out)
