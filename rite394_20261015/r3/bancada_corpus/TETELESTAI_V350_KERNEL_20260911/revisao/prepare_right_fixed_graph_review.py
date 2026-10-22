from pathlib import Path
import ast
REV=Path(__file__).resolve().parent
t=(REV/'run_right_graph_partial_review.py').read_text(encoding='utf-8')
t=t.replace("'right_graph_partial_independent_'", "'right_fixed_graph_independent_'")
t=t.replace("Path((REV/'scalar_vna_final_latest_run.txt').read_text().strip())]", "Path((REV/'scalar_vna_final_latest_run.txt').read_text().strip()),Path((REV/'right_graph_partial_latest_run.txt').read_text().strip()),Path((REV/'right_graph_blocks_latest_run.txt').read_text().strip())]")
a=t.index('spec=[');b=t.index('\nsources=',a)
t=t[:a]+"spec=[('FixedVectorGraphCore','20260913_014340_002699',9)]"+t[b:]
t=t.replace("sources={};raws={};targets=[];history=[]", """prior=Path((REV/'right_graph_blocks_latest_run.txt').read_text().strip())
prior_m=load(prior/'manifest.json');prior_c=load(prior/'compilation.json')
assert prior_c['complete'] and prior_c['all_exit_zero'] and prior_c['exact_39_targets'] and prior_c['new_binary_equals_author']
assert len(prior_m['declarations'])==39
inherited_sources={**prior_m['inherited_partial_review']['sources'],**prior_m['sources']}
assert len(inherited_sources)==3
for d in inherited_sources.values():
    assert hf(d['path'])==d['sha256'] and hf(d['author_binary'])==d['author_binary_sha256']
inherited={'run':str(prior),'manifest_sha256':hf(prior/'manifest.json'),'compilation_sha256':hf(prior/'compilation.json'),'declarations':prior_m['declarations'],'sources':inherited_sources}
sources={};raws={};targets=list(prior_m['declarations']);history=[]""")
t=t.replace('assert len(targets)==len(set(targets))==22','assert len(targets)==len(set(targets))==48')
t=t.replace('for n in raws:visit(n)', "for n in list(raws)+['TGLV350.ScalarRightMultiplicationGraph','TGLV350.HilbertProjectionBlocks']:visit(n)")
t=t.replace("'scope':'PARTIAL_TWO_MODULES_ONLY_22_TARGETS'", "'inherited_partial_review':inherited,'scope':'PARTIAL_FOUR_ACCEPTED_MODULES_9_NEW_48_CUMULATIVE_TARGETS'")
t=t.replace("'right_graph_partial_latest_run.txt',str(RUN).encode()", "'right_fixed_graph_latest_run.txt',str(RUN).encode()")
t=t.replace("audit=''.join('import TGLV350.'+n+'\\n' for n,_,_ in spec)", "audit='import TGLV350.ScalarRightMultiplicationGraph\\nimport TGLV350.HilbertProjectionBlocks\\n'+''.join('import TGLV350.'+n+'\\n' for n,_,_ in spec)")
t=t.replace('RightGraphPartialAudit','RightFixedGraphAudit')
t=t.replace('len(records)==3','len(records)==2').replace('exact_22_targets','exact_48_targets')
t=t.replace("'two_binaries_equal_author':len(records)>=2 and all(x.get('binary_equals_author',False) for x in records[:2])", "'new_binary_equals_author':len(records)>=1 and records[0].get('binary_equals_author',False)")
t=t.replace("'author_source_binary_preserved':all", "'inherited_sources_binaries_preserved':all(hf(x['path'])==x['sha256'] and hf(x['author_binary'])==x['author_binary_sha256'] for x in inherited_sources.values()),'author_source_binary_preserved':all")
ast.parse(t);out=REV/'run_right_fixed_graph_review.py';assert not out.exists()
raw=t.encode();tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);print(out)
