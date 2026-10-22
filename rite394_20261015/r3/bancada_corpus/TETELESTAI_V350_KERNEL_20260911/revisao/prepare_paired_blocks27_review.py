from pathlib import Path
REV=Path(__file__).resolve().parent
s=(REV/'run_paired_blocks25_review.py').read_text(encoding='utf-8')
s=s.replace("'paired_blocks_latest_run.txt'","'paired_blocks25_latest_run.txt'")
s=s.replace("'paired_blocks25_independent_'","'paired_blocks27_independent_'")
s=s.replace("'exact_13_targets'","'exact_25_targets'").replace("'binary_equal_author'","'new_binary_equal_author'")
a=s.index("VNA=REV/");b=s.index("name='ScalarPairedProjectionBlocks'",a)
s=s[:a]+s[b:]
s=s.replace("name='ScalarPairedProjectionBlocks'","name='ScalarWeightedProjectionTest'")
s=s.replace('20260913_065106_761132','20260913_065924_871127')
s=s.replace('len(set(newtargets))==12','len(set(newtargets))==2').replace('len(set(targets))==25','len(set(targets))==27')
insert="""
draftpath=ROOT/'paired_blocks_draft_status.json';draft=load(draftpath)
assert len(draft['modules'])==4 and len(draft['targets'])==27 and draft['targets']==allax
assert draft['parent_custody_sha256']==pm['parent_custody_sha256']
assert draft['integrated_working_sha256']==load(Path(pm['parent_custody_path']))['working_sha256']
assert draft['integrated'] is False and draft['independent_review_complete'] is False
assert draft['projection_block_uniform_lower_bound_proved'] is False and draft['KMS_proved'] is False
for mn,md in draft['modules'].items():
    ms=ROOT/'kernel/TGLV350'/(mn+'.lean');mb=ROOT/'build/TGLV350'/(mn+'.olean');ml=Path(md['final_log']);mr=load(ml)
    assert hf(ms)==md['source_sha256']==mr['sha256'] and hf(mb)==md['binary_sha256']==mr['output_sha256']
    assert mr['returncode']==mr['lean_returncode']==0 and mr['output_exists'] and mr['source_unchanged_during_compile']
    assert hf(ml)==md['final_log_sha256'] and hf(mr['stdout'])==md['stdout_sha256'] and hf(mr['stderr'])==md['stderr_sha256']
    if mn!=name:
        cd=catalog['TGLV350.'+mn];assert hf(cd['source'])==md['source_sha256'] and hf(cd['binary'])==md['binary_sha256']
    for p in [ms,mb,ml,Path(mr['stdout']),Path(mr['stderr'])]:readonly[str(p)]=hf(p)
    for hp in md['failed_attempts']:assert load(hp)['returncode']!=0
assert sum(len(v['failed_attempts']) for v in draft['modules'].values())==7
import ast
docs=[draftpath,Path(draft['report_path'])]+[ROOT/x for x in ['record_paired_blocks_draft.py','prepare_paired_blocks_stage.py','record_paired_blocks_progress.py','verify_paired_blocks_custody.py']]
assert hf(docs[1])==draft['report_sha256']
docpins={}
for p in docs:
    bb=p.read_bytes()
    if p.suffix=='.py':ast.parse(bb)
    put(RUN/'documents'/p.name,bb);readonly[str(p)]=sha(bb);docpins[str(p)]=sha(bb)
"""
s=s.replace("allax={**pm['author_axioms'],**authorax}","allax={**pm['author_axioms'],**authorax}\n"+insert)
s=s.replace("'additional_own_origin':str(VNA),'additional_own_manifest_sha256':hf(VNA/'manifest.json'),'additional_own_compilation_sha256':hf(VNA/'compilation.json'),", "'draft_path':str(draftpath),'draft_sha256':hf(draftpath),'document_pins':docpins,'cumulative_modules':draft['modules'],")
s=s.replace('PairedBlocksAudit25','PairedBlocksAudit27').replace('PARTIAL_DEV25_13_INHERITED_12_NEW','FINAL_DEV27_25_INHERITED_2_NEW')
s=s.replace("'paired_blocks25_latest_run.txt',str(RUN)","'paired_blocks27_latest_run.txt',str(RUN)")
s=s.replace("'new_targets':12,'cumulative_targets':25","'new_targets':2,'cumulative_targets':27")
# Only the result key changes; keep the inherited DEV25 success assertion above.
s=s.replace("'exact_25_targets':len(records)==2", "'exact_27_targets':len(records)==2")
out=REV/'run_paired_blocks27_review.py';assert not out.exists()
tmp=out.with_suffix('.py.tmp');tmp.write_bytes(s.encode());assert tmp.read_bytes()==s.encode();tmp.replace(out)
print(out)
