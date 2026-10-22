from review_a2 import *

COMMON='import IndependentA2Controls\nset_option autoImplicit false\nopen TGLExt TGLV350.Regular TGLV351 TGL.ContinuousCorner IndependentA2\n'
CASES=[
 ('TraceZero','example (P : SiteProfile) : scalarInverseLimitWeight P (regularFiniteSupport P) = 0 := by\n  exact trace_positive P\n','IndependentA2.trace_not_zero'),
 ('TraceTwo','example (P : SiteProfile) : scalarInverseLimitWeight P (regularFiniteSupport P) = 2 := by\n  exact trace_positive P\n','IndependentA2.trace_not_two'),
 ('SupportZero','example (P : SiteProfile) : (regularFiniteSupport P).val = 0 := by\n  exact support_nonzero P\n','IndependentA2.support_nonzero'),
 ('SpectralZero','example (P : SiteProfile) : (regularMinimalLock P).ker.starProjection = 0 := by\n  exact spectral_positive P\n','IndependentA2.spectral_not_zero'),
 ('HalfAsOne','example (P : SiteProfile) : (regularContinuousCorner P).normalizedTrace (regularContinuousCorner P).Pplus = 1 := by\n  exact plus_half P\n','IndependentA2.plus_not_one'),
 ('EqualFromOrthogonality','example : unequalWeight leftFace = unequalWeight rightFace := by\n  exact (show (1 : ℝ) = 1 from rfl)\n','IndependentA2.orthogonality_does_not_force_equal_trace'),
 ('PositiveZero','example (P : SiteProfile) : 0 < scalarInverseLimitWeight P (PositiveCoreInput.zero P) := by\n  exact (support_trace_positive_finite P).1\n','IndependentA2.zero_positive_has_no_positive_finite_minorant'),
 ('GlobalGap','example (P : SiteProfile) : ∀ x : RegularHilbert (TowerHilbert P), ‖regularMinimalLock P x‖ = ‖x‖ := by\n  intro x\n  exact regularMinimalLock_relative_gap P x\n','IndependentA2.gap_not_global'),
 ('GlobalCyclicity','example (P : SiteProfile) : ∀ a b : (regularCoreAlgebra P).toStarSubalgebra, positiveTraceReader P (a*b) = positiveTraceReader P (b*a) := by\n  exact positiveTraceReader_positive P\n','IndependentA2.reader_not_global_cyclic')
]

def main():
    assert json.loads((ROOT/'BUILD.json').read_text(encoding='utf-8'))['all_pass']
    attempt=ROOT/'control_attempts'/stamp()
    source=SRC/'IndependentA2Controls.lean'
    positive,out=run(source,attempt/'positive',OUT/'IndependentA2Controls.olean')
    print('Positive controls',positive['returncode'],out[-7000:],flush=True)
    if positive['returncode']:
        record(attempt/'FAILED_DEV.json',dict(status='NOT_PROOF',run=positive)); sys.exit(1)
    names=['IndependentA2.'+n for n in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|lemma|abbrev)\s+(\w+)',code_only(source.read_text(encoding='utf-8')),re.M)]
    write(SRC/'AuditIndependentA2.lean','import IndependentA2Controls\nset_option pp.universes true\n'+
          '\n'.join('#check '+n+'\n#print axioms '+n for n in names)+'\n')
    audit,out=run(SRC/'AuditIndependentA2.lean',attempt/'audit',OUT/'AuditIndependentA2.olean')
    print('Own audit',audit['returncode'],flush=True)
    if audit['returncode']: print(out[-7000:]); sys.exit(1)
    def job(case):
        name,body,wall=case
        src=SRC/'controls'/('Bad'+name+'.lean')
        write(src,COMMON+body)
        row,out=run(src,attempt/name)
        row.update(name=name,wall=wall,diagnostic=out,
           semantic_rejection=row['returncode']!=0 and 'Type mismatch' in out and
           not re.search(r'unexpected token|unknown (identifier|constant|namespace|module)|object file .* does not exist|failed to',out,re.I))
        print(name,row['returncode'],row['semantic_rejection'],flush=True)
        return row
    with futures.ThreadPoolExecutor(max_workers=3) as pool: controls=list(pool.map(job,CASES))
    record(ROOT/'CONTROLS.json',dict(positive=positive,audit=audit,names=names,negative_controls=controls,
        all_pass=positive['returncode']==0 and audit['returncode']==0 and len(controls)==len(CASES) and all(r['semantic_rejection'] for r in controls)))

if __name__=='__main__': main()
