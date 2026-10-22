from review import *

def main():
    initial=read(ROOT/'INPUTS.json'); more=read(ROOT/'ASSEMBLY_INPUTS.json')
    discovery=read(ROOT/'ASSEMBLY_BUILD.json')['discovery']; assert discovery['returncode']==0
    output=Path(discovery['stdout']['path']).read_text(encoding='utf-8')
    names=[s.rstrip('.') for s in re.findall(r'^(TGLV354\.[\w.]+)',output,re.M)]
    assert len(names)==len(set(names))
    explicit=initial['public_names']+more['explicit_public_names']
    assert len(explicit)==len(set(explicit)) and set(explicit)<=set(names)
    generated=sorted(set(names)-set(explicit))
    assert generated==['TGLV354.boundedPolar.congr_simp','TGLV354.instBoundedOrderCoreProjection']
    author=read(ROOT/'inputs/AUDIT_NAMES_FULL.json')['names']
    susy=read(ROOT/'inputs/SUSY_AUDIT_NAMES.json')['names']
    assert set(author)|set(susy)==set(explicit)
    source=SRC/'AuditAllFinal.lean'
    write(source,'import TGLExt.V354RegularLegacyWitness\nimport TGLExt.V354RegularSusy\nset_option pp.universes true\n'+
        '\n'.join('#check '+n+'\n#print '+n+'\n#print axioms '+n for n in names)+'\n')
    result,out=run(source,ROOT/'final_audit',OUT/'AuditAllFinal.olean')
    record(ROOT/'FINAL_AUDIT.json',dict(result=result,names=names,explicit_names=explicit,generated_names=generated,
        author_main_count=len(author),author_susy_count=len(susy),explicit_union_count=len(explicit),total_count=len(names)))
    print('Final public audit',result['returncode'],len(explicit),'explicit +',len(generated),'additional exports =',len(names),flush=True)
    if result['returncode']: print(out[-8000:]); raise RuntimeError('Final audit failed')

if __name__=='__main__': main()
