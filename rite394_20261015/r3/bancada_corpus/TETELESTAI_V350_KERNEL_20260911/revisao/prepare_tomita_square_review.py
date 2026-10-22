"""Prepare an independent two-module build plus cumulative 53-target audit."""
from pathlib import Path
R=Path(__file__).resolve().parent
code=(R/'run_scalar_tomita_adjoint_review.py').read_text(encoding='utf-8')
changes=[('closed_tomita_batch_latest_run.txt','scalar_tomita_adjoint_latest_run.txt'),("RUN=REV/('scalar_tomita_adjoint_independent_'","RUN=REV/('tomita_square_independent_'"),("NAMES={'AntilinearAdjointGraph':'20260912_103611_347285','ScalarTomitaAdjoint':'20260912_104146_918776'}","NAMES={'ScalarTomitaSquare':'20260912_105822_725293','ScalarTomitaSelfAdjoint':'20260912_105946_717528'}"),('len(targets)==len(set(targets))==23','len(targets)==len(set(targets))==18'),('INDEPENDENT_TWO_DEV_MODULES_23_TYPES_AXIOMS','INDEPENDENT_TWO_CONCRETE_MODULES_CUMULATIVE_53_TYPES_AXIOMS'),("write(REV/'scalar_tomita_adjoint_latest_run.txt'","write(REV/'tomita_square_latest_run.txt'"),('ScalarTomitaAdjointAudit','TomitaSquareFullAudit'),('exact_23_targets','exact_53_targets')]
for old,new in changes:
    assert old in code,old
    code=code.replace(old,new)
anchor="custody_raw=(ROOT/'closed_tomita_custody.json').read_bytes()"
extra="""AUX=Path((REV/'resolvent_aux_latest_run.txt').read_text(encoding='utf-8'))
am=json.loads((AUX/'manifest.json').read_bytes());ac=json.loads((AUX/'compilation.json').read_bytes())
assert ac['all_exit_zero'] and ac['all_axioms_allowed'] and ac['exact_12_targets']
for rel,r in am['sources'].items():
    cc=next(x for x in ac['records'] if x['module']==rel)
    catalog[rel[:-5].replace('/','.') ]={'source':r['snapshot'],'binary':str(AUX/'build'/Path(rel).with_suffix('.olean')),'source_sha256':r['sha256'],'sha256':cc['output_sha256'],'reviewer_origin':str(AUX)}
"""
assert anchor in code;code=code.replace(anchor,extra+anchor)
anchor="assert len(targets)==len(set(targets))==18"
code=code.replace(anchor,anchor+"\nnew_targets=targets.copy();targets=list(pm['declarations'])+list(am['declarations'])+targets\nassert len(targets)==len(set(targets))==53")
anchor="save(RUN/'manifest.json',manifest)"
extra="""status_raw=(ROOT/'tomita_square_draft_status.json').read_bytes();status=json.loads(status_raw)
assert len(status['modules'])==7 and set(status['targets'])==set(targets)
assert status['parent_custody_sha256']==sha(custody_raw)
for name,pin in status['modules'].items():
    sr=ROOT/'kernel/TGLV350'/(name+'.lean');bn=ROOT/'build/TGLV350'/(name+'.olean');lp=Path(pin['log'])
    assert sha(sr.read_bytes())==pin['source_sha256'] and sha(bn.read_bytes())==pin['output_sha256'] and sha(lp.read_bytes())==pin['log_sha256']
write(RUN/'tomita_square_draft_status.json',status_raw)
doc=(ROOT/'RELATORIO_ADJUNTO_QUADRADO_DEV.md').read_bytes();write(RUN/'RELATORIO_ADJUNTO_QUADRADO_DEV.md',doc)
manifest.update(new_targets=new_targets,secondary_run=str(AUX),secondary_manifest_sha256=sha((AUX/'manifest.json').read_bytes()),secondary_compilation_sha256=sha((AUX/'compilation.json').read_bytes()),draft_status_sha256=sha(status_raw),report_sha256=sha(doc))
"""
assert anchor in code;code=code.replace(anchor,extra+anchor)
anchor="audit='\\n'.join('import TGLV350.'+n for n in NAMES)+'\\n'"
replacement="audit='\\n'.join('import TGLV350.'+n for n in status['modules'])+'\\n'"
assert anchor in code;code=code.replace(anchor,replacement)
p=R/'run_tomita_square_review.py';assert not p.exists();raw=code.encode();tmp=p.with_suffix('.py.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(str(p))
