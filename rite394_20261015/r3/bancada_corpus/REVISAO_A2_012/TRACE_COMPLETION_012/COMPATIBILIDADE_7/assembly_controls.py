from review import *

def main():
    folder=ROOT/'assembly_controls_attempts'/stamp()
    p=SRC/'IndependentAssemblyControls.lean'
    names=['IndependentAssembly.'+n for n in re.findall(r'^(?:def|theorem)\s+(\w+)',code_only(p.read_text(encoding='utf-8')),re.M)]
    pos,out=run(p,folder/'positive',OUT/'IndependentAssemblyControls.olean')
    print('Assembly positive controls',pos['returncode'],flush=True)
    if pos['returncode']: print(out); raise RuntimeError('Invalid positive anchor')
    ap=SRC/'AuditAssemblyControls.lean'; write(ap,'import IndependentAssemblyControls\n'+'\n'.join('#print axioms '+n for n in names)+'\n')
    audit,out=run(ap,folder/'audit',OUT/'AuditAssemblyControls.olean')
    if audit['returncode']: print(out); raise RuntimeError('Own audit failed')
    cases=[('AssemblyTraceTwo','IndependentAssembly.assembled_PF_trace_not_two',
        'example : TGLV354.TraceCompletion.regularLegacyCore.canonicalTrace\n  TGLV354.TraceCompletion.regularLegacyThreeLocks.PF = 2 := by\n  exact IndependentAssembly.assembled_PF_trace_one\n'),
        ('SusyGapZero','IndependentAssembly.susy_gap_nonzero',
        'example (P : TGLExt.SiteProfile) : (TGLV354.regularSusyData P).gapD.operator = 0 := by\n  exact IndependentAssembly.susy_gap_equals_PF P\n'),
        ('NumericSusySubstitute','IndependentAssembly.actualSusy',
        'example (P : TGLExt.SiteProfile) : TGLExt.SusyRelativeData\n  (TGLV354.CoreProjection (TGLV350.Regular.regularCoreAlgebra P))\n  (TGLV354.coreProjectionTraceSubadditive P) := by\n  exact TGLExt.modelSusy\n')]
    negatives=[]
    for name,anchor,body in cases:
        p=SRC/'negative'/(name+'.lean'); write(p,'import IndependentAssemblyControls\n\n'+body)
        row,out=run(p,folder/name)
        row.update(name=name,positive_anchor=anchor,semantic_rejection=row['returncode']!=0 and 'Type mismatch' in out
            and not re.search(r'unknown (identifier|constant|namespace|module)|unexpected token|object file .*does not exist',out,re.I))
        negatives.append(row); print(name,row['returncode'],row['semantic_rejection'],flush=True)
    record(ROOT/'ASSEMBLY_CONTROLS.json',dict(positive=pos,audit=audit,names=names,negative_controls=negatives,
        note='New assembly wiring only; numeric-SUSY rejection is a type separation, not a proof that a real-valued equality is false.'))

if __name__=='__main__': main()
