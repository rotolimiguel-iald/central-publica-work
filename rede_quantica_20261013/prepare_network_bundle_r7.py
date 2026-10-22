"""Transpose the reviewed modular/KMS chain, reusing identical prior modules."""
import ast,datetime as dt,json,re
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
REDE=OUT.parent/'F1.REDE'
DEST=OUT/'network_bundle_r7'
PREFIX='TGLExt.F1Fecho394.'
ROOTS=['CanonicalModularCoreAssemblyR1','CanonicalFockWeightClosedTomitaR2',
       'OrbitalSpatialCovarianceR2','OrbitalSpatialContinuityR1','AnnihilationDomainR1',
       'CanonicalFockGNSNormalityR4','RootRateFrequencyR2','DeviceRootObstructionR4']

def imports(text):return re.findall(r'^import\s+([\w.]+)\s*$',text,re.M)

def main():
    assert not DEST.exists(),'Already attempted; recover instead of overwriting'
    chosen={};active=set();order=[]
    def resolve(name):
        if name in ('Lean','Mathlib','Std') or name.startswith(('TGLExt.','TGL.','Mathlib.','Lean.','Std.','Batteries.')):return
        if name in chosen:return
        assert name not in active,('cycle',name)
        active.add(name)
        files=[p for root in (OUT,REDE) for p in root.glob('*/'+name+'.lean') if 'review' not in p.parent.name]
        assert len(files)==1,('source ambiguity',name,files)
        source=files[0];sp=pin(source);matches=[]
        for root in (OUT,REDE):
            for obj in root.glob('*/attempts/*/'+name+'.olean'):
                snap=obj.with_suffix('.lean');rp=obj.parent/'RECEIPT.json'
                if snap.exists() and rp.exists() and pin(snap)['sha256']==sp['sha256']:
                    r=json.loads(rp.read_bytes())
                    if r.get('exit_code')==0:matches.append((obj,rp,r))
        assert matches,('no compiled source',name)
        obj,rp,r=sorted(matches,key=lambda x:str(x[0]))[-1]
        text=source.read_text(encoding='utf-8')
        assert not re.search(r'(?m)^\s*(?:axiom|sorry)\b',text),name
        for dep in imports(text):resolve(dep)
        chosen[name]=dict(name=name,source=sp,receipt=pin(rp),object=pin(obj),body=text)
        order.append(name);active.remove(name)
    for name in ROOTS:resolve(name)
    baseline=OUT/'full_rite/reconciliation_candidate_r3/um_v394_reconciled.py'
    t=ast.parse(baseline.read_bytes())
    embedded=next(ast.literal_eval(n.value) for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='_EMBEDDED_KERNEL_FILES' for x in n.targets))
    rows=[]
    for name in order:
        row=chosen[name];body=row.pop('body')
        transformed=re.sub(r'^import\s+([\w.]+)\s*$',lambda m:'import '+(PREFIX+m[1] if m[1] in chosen else m[1]),body,flags=re.M)
        # Inline engineering audits identify modules by Lean Name literals.
        # Rename only exact local module literals; mathematical namespaces stay.
        literals=[]
        def rename_literal(m):
            n=m[1]
            if n in chosen:literals.append(n);return '`'+PREFIX+n
            return m[0]
        transformed=re.sub(r'`([A-Za-z_][A-Za-z0-9_]*)(?![\w.])',rename_literal,transformed)
        rel=(PREFIX+name).replace('.','/')+'.lean'
        if rel in embedded:
            baseline_body=embedded[rel]
            normalized_baseline=re.sub(r'^import\s+([\w.]+)\s*$',r'import \1',baseline_body,flags=re.M)
            assert transformed==baseline_body or transformed==normalized_baseline,('existing module body would change',rel)
            row['baseline_import_whitespace_preserved']=transformed!=baseline_body
            transformed=baseline_body
            reuse=OUT/'network_bundle_r4/lib'/Path(rel).with_suffix('.olean')
            assert reuse.exists(),('prior binary missing',reuse)
            row['reuse_prior_object']=pin(reuse)
            row['reuse_prior_source']=pin(OUT/'network_bundle_r4/src'/rel)
            assert (OUT/'network_bundle_r4/src'/rel).read_text(encoding='utf-8')==transformed
        row.update(relative=rel,module=PREFIX+name,inline_audit_module_literals=sorted(set(literals)))
        path=DEST/'src'/rel;new(path,transformed);row['transposed_source']=pin(path)
        rows.append(row)
    audit=''.join('import '+PREFIX+n+'\n' for n in ROOTS)+'import Lean\n\n'
    audit+='''open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? n then
      let mod := env.header.moduleNames[idx]!
      if (`TGLExt.F1Fecho394).isPrefixOf mod then
        count := count + 1
        let axs ← collectAxioms n
        IO.println ("BUNDLE_DECL\\t" ++ n.toString ++ "\\t" ++ mod.toString ++ "\\t" ++ String.intercalate "," (axs.toList.map Name.toString))
        unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
          throwError "AXIOM_AUDIT_REFUSED: {n}"
        match ci with
        | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
        | _ => pure ()
  if count == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("BUNDLE_COUNT\\t" ++ toString count)
'''
    ap=DEST/'src/TGLExt/F1Fecho394/NetworkProofAuditR7.lean';new(ap,audit)
    new(DEST/'PLAN.json',dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),unit='F1.FECHO_20261015',claim_event=845,
      baseline=pin(baseline),roots=ROOTS,modules=rows,audit=pin(ap),audit_module='TGLExt.F1Fecho394.NetworkProofAuditR7',
      audit_relative='TGLExt/F1Fecho394/NetworkProofAuditR7.lean',script=pin(__file__),
      status='TRANSPOSED_PENDING_COMPILATION_AND_REVIEW',
      scope='Full concrete standard-wedge modular/KMS realization, weight GNS core, strongly continuous scalar orbital orthogonal group and concrete annihilation and physical root-rate obstruction. Global net, full weight modular/scaled trace and Maxwell remain separate.'))
    print(json.dumps(dict(plan=pin(DEST/'PLAN.json'),modules=len(rows),reuse=sum('reuse_prior_object' in r for r in rows),new=sum('reuse_prior_object' not in r for r in rows),inline_audits=[(r['name'],r['inline_audit_module_literals']) for r in rows if r['inline_audit_module_literals']]),ensure_ascii=False))

if __name__=='__main__':main()
