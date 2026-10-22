from pathlib import Path
import datetime, json

REV=Path(__file__).resolve().parent
old=(REV/'run_paired_graph_review.py').read_text(encoding='utf-8')
s=old.replace("'paired_graph_independent_'", "'paired_blocks_independent_'")
a=s.index("lp=ROOT/'logs/ScalarPairedMultiplicationGraph_")
b=s.index("parent=ROOT/'square_resolvent_custody.json'")
s=s[:a]+'''specs=[('ScalarPairedMultiplicationGraph','20260913_063138_562066',5,1),
       ('HilbertProjectionOrder','20260913_063505_616727',8,2)]
sources={}; targets=[]; authorax={}; history=[]; raw_sources=[]; module_targets={}
for name,stamp,count,failed_count in specs:
    lp=ROOT/'logs'/f'{name}_{stamp}.json';lr=load(lp)
    src=ROOT/'kernel/TGLV350'/f'{name}.lean';raw=src.read_bytes();ab=Path(lr['command'][2])
    assert lr['returncode']==lr['lean_returncode']==0 and lr['output_exists'] and lr['source_unchanged_during_compile']
    assert Path(lr['source'])==src and sha(raw)==lr['sha256'] and hf(ab)==lr['output_sha256']
    ts=['TGLV350.Regular.'+n for n in re.findall(r'^#print axioms ([\\w.]+)$',raw.decode(),re.M)]
    assert len(ts)==len(set(ts))==count
    ax=axioms(Path(lr['stdout']).read_text(encoding='utf-8'))
    assert set(ax)==set(ts) and all(set(v)<=allowed for v in ax.values())
    assert not Path(lr['stderr']).read_bytes()
    clean=re.sub(r'/\\-.*?\\-/','',raw.decode(),flags=re.S);clean=re.sub(r'--[^\\n]*','',clean)
    assert not re.search(r'\\b(?:axiom|sorry|admit|unsafe)\\b|\\[(?:irreducible|reducible)\\]',clean)
    for p in [src,ab,lp,Path(lr['stdout']),Path(lr['stderr'])]:readonly[str(p)]=hf(p)
    for p in [lp,Path(lr['stdout']),Path(lr['stderr'])]:write(RUN/'author_final'/p.name,p.read_bytes())
    rel=f'TGLV350/{name}.lean';snap=RUN/'sources'/rel;write(snap,raw)
    sources[rel]={'path':str(src),'snapshot':str(snap),'sha256':sha(raw),'author_binary':str(ab),
      'author_binary_sha256':hf(ab),'author_log':str(lp),'author_log_sha256':hf(lp),
      'author_stdout_sha256':hf(lr['stdout']),'author_stderr_sha256':hf(lr['stderr'])}
    targets+=ts;authorax.update(ax);raw_sources.append(raw);module_targets[rel]=ts
    mh=[]
    for p in sorted((ROOT/'logs').glob(name+'_*.json')):
        d=load(p);row={'log':str(p),'log_sha256':hf(p),'returncode':d['returncode'],
          'source_sha256':d['sha256'],'accepted_final':p==lp}
        write(RUN/'author_history'/p.name,p.read_bytes())
        for k in ['stdout','stderr']:
            bb=Path(d[k]).read_bytes();write(RUN/'author_history'/Path(d[k]).name,bb);row[k+'_sha256']=sha(bb)
        mh.append(row)
    assert sum(d['returncode']!=0 for d in mh)==failed_count
    history+=mh
assert len(targets)==len(set(targets))==13
''' +s[b:]
s=s.replace('for n in imports(raw):visit(n)','for raw in raw_sources:\n    for n in imports(raw):visit(n)')
s=s.replace("        assert d.get('previously_reviewed_comment_only_erratum') is True,n\n        assert s.replace(d['frozen_old_comment'].encode(),d['live_corrected_comment'].encode())==live,n",'''        assert n=='TGLV350.DualSemifiniteIdeal',n
        old_comment=b'/-- A single bound for all vectors: this is finiteness of the output form\\nas a bounded operator, not just finiteness on a chosen vector domain. -/'
        new_comment=b'/-- A single bound for all vectors: the output is a uniformly bounded\\nquadratic form, not just finite on a chosen vector domain. Realization by\\na bounded operator in the fixed algebra is a separate obligation. -/'
        if b'\\r\\n' in s:old_comment=old_comment.replace(b'\\n',b'\\r\\n');new_comment=new_comment.replace(b'\\n',b'\\r\\n')
        assert s.count(old_comment)==1 and s.replace(old_comment,new_comment)==live,n
        d={**d,'previously_reviewed_comment_only_erratum':True,'frozen_old_comment':old_comment.decode(),
           'live_corrected_comment':new_comment.decode(),'exact_literal_replacement_verified':True}
''')
s=s.replace("external=pm['external_direct_pins']", "external=pm['external_direct_pins']\n# Direct Mathlib import added by the second module; only read the installed package.\nfor n in sorted({x for raw in raw_sources for x in imports(raw) if x.startswith('Mathlib.')}):\n    pp=next(Path(p) for p in pkg if (Path(p)/Path(*n.split('.')).with_suffix('.olean')).exists())\n    bp=pp/Path(*n.split('.')).with_suffix('.olean')\n    sp=pp.parents[3]/Path(*n.split('.')).with_suffix('.lean')\n    assert sp.exists(),str(sp)\n    external[n]={'source':str(sp),'binary':str(bp),'source_sha256':hf(sp),'binary_sha256':hf(bp)}")
a=s.index("aud='import TGLV350.ScalarPairedMultiplicationGraph")
b=s.index("records=[]",a)
s=s[:a]+'''aud=''.join('import '+rel[:-5].replace('/','.')+'\\n' for rel in sources)+''.join('set_option pp.universes true in\\n#check '+n+'\\n#print axioms '+n+'\\n' for n in targets)
write(RUN/'sources/PairedBlocksAudit13.lean',aud.encode())
manifest={'run':str(RUN),'timestamp':datetime.datetime.now().astimezone().isoformat(),'scope':'PARTIAL_DEV_PAIRED_BLOCKS_2_MODULES_13_TARGETS',
 'compiler':compiler,'compiler_sha256':hf(compiler),'lean_version_inherited':'4.31.0 — compiler hash inherited and reread','lean_path':env['LEAN_PATH'],
 'sources':sources,'declarations':targets,'module_targets':module_targets,'author_axioms':authorax,'dependencies':deps,
 'external_direct_pins':external,'readonly_pins':readonly,'parent_custody_path':str(parent),'parent_custody_sha256':hf(parent),
 'parent_full_reaudit':False,'author_project_build_on_lean_path':False,'packages_rebuilt':False,'memory_writes':False,'own_origin_runs':[str(PHASE)]}
save(RUN/'manifest.json',manifest);save(RUN/'author_history.json',history)
write(REV/'paired_blocks_latest_run.txt',str(RUN).encode())
print(json.dumps({'run':str(RUN),'new_modules':2,'targets':13,'project_dependencies':len(deps),'author_failures_excluded':3}),flush=True)
''' +s[b:]
s=s.replace("for rel in ['TGLV350/ScalarPairedMultiplicationGraph.lean','PairedGraphAudit5.lean']:","for rel in list(sources)+['PairedBlocksAudit13.lean']:")
s=s.replace("    row={'module':rel", "    expected=module_targets.get(rel,targets);expectedax={n:authorax[n] for n in expected}\n    row={'module':rel")
s=s.replace("set(ax)==set(targets),'axioms_match_author':ax==authorax", "set(ax)==set(expected),'axioms_match_author':ax==expectedax")
s=s.replace("row['output_sha256']==hf(ab)","row['output_sha256']==sources[rel]['author_binary_sha256']")
s=s.replace("len(records)==2", "len(records)==3").replace("'exact_5_targets'","'exact_13_targets'")
s=s.replace("'binary_equal_author':records[0].get('binary_equals_author',False)","'binary_equal_author':len(records)==3 and all(x.get('binary_equals_author',False) for x in records[:2])")
s=s.replace("'source_snapshot_preserved':hf(snap)==sha(raw)","'source_snapshot_preserved':all(hf(d['snapshot'])==d['sha256'] for d in sources.values())")
s=s.replace("'complete':len(records)==3", "'complete':len(records)==3")
out=REV/'run_paired_blocks_review.py'
assert not out.exists()
temp=out.with_suffix('.py.tmp');temp.write_bytes(s.encode('utf-8'));assert temp.read_bytes()==s.encode('utf-8');temp.replace(out)
print(out)
