from review import *

def main():
    attempt=ROOT/'controls_attempts'/stamp()
    p=SRC/'IndependentCompatibilityControls.lean'
    clean=code_only(p.read_text(encoding='utf-8'))
    names=['IndependentTraceCompatibility.'+n for n in re.findall(r'^theorem\s+(\w+)',clean,re.M)]
    positive,out=run(p,attempt/'positive',OUT/'IndependentCompatibilityControls.olean')
    print('Positive controls',positive['returncode'],flush=True)
    if positive['returncode']: print(out); raise RuntimeError('Positive control failed; no valid rejection evidence')
    audit=SRC/'AuditOwnControls.lean'
    write(audit,'import IndependentCompatibilityControls\n'+ '\n'.join('#print axioms '+n for n in names)+'\n')
    ar,out=run(audit,attempt/'audit',OUT/'AuditOwnControls.olean')
    if ar['returncode']: print(out); raise RuntimeError('Control axiom audit failed')
    cases=[('UnitTraceZero','unit_read_nonzero',
        'example (P : TGLExt.SiteProfile) :\n  TGLV354.TraceCompletion.cyclicTraceCandidate P\n    (1 : (TGLV350.Regular.regularCoreAlgebra P).toStarSubalgebra) = 0 := by\n  exact IndependentTraceCompatibility.unit_read_exact P\n'),
        ('PolarSupportZero','polar_one_product_nonzero',
        'example : star (TGLV354.boundedPolar (1 : ℂ →L[ℂ] ℂ)) *\n  TGLV354.boundedPolar (1 : ℂ →L[ℂ] ℂ) = 0 := by\n  exact IndependentTraceCompatibility.polar_one_product\n'),
        ('LagZeroKernel','zero_power_zero_nonzero',
        'example : ((0 : ℂ →L[ℂ] ℂ) ^ 0) 1 = 0 := by\n  exact IndependentTraceCompatibility.zero_operator_at_one\n')]
    negative=[]
    for name,wall,body in cases:
        source=SRC/'negative'/(name+'.lean'); write(source,'import IndependentCompatibilityControls\n\n'+body)
        row,out=run(source,attempt/name)
        row.update(name=name,wall='IndependentTraceCompatibility.'+wall,
            semantic_rejection=row['returncode']!=0 and 'Type mismatch' in out and not re.search(
                r'unknown (identifier|constant|namespace|module)|unexpected token|object file .*does not exist',out,re.I))
        negative.append(row); print(name,row['returncode'],row['semantic_rejection'],flush=True)
    record(ROOT/'CONTROLS.json',dict(positive=positive,audit=ar,names=names,negative_controls=negative,
        rationale='Only new risks: exact nonzero positive reading, extra polar support, and positive lag. No repetition of the paid 33-lemma controls.'))

if __name__=='__main__': main()
