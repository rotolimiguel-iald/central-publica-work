from review import *

def main():
    assert json.loads((ROOT/'BUILD.json').read_text(encoding='utf-8'))['all_pass']
    run_id=stamp()
    runroot=ROOT/'independent_logs'/run_id
    source=K/'IndependentSubstitution.lean'
    write(runroot/source.name,source.read_bytes())
    result,out=run_lean(source,runroot/'positive',K/'.lake'/'build'/'lib'/'lean'/'IndependentSubstitution.olean')
    print('Independent positive',result['returncode'],out[-8000:],flush=True)
    if result['returncode']:
        record(runroot/'FAILED_DEV.json',dict(result=result,status='NOT_PROOF'))
        sys.exit(1)
    rows=[]
    for name in ['IndependentBadBeta','IndependentBadXi']:
        src=K/(name+'.lean')
        write(runroot/src.name,src.read_bytes())
        row,output=run_lean(src,runroot/name)
        row.update(name=name,diagnostic=output,
            semantic_type_rejection=row['returncode']!=0 and 'Type mismatch' in output and
            not re.search(r'unexpected token|unknown (identifier|constant|namespace|module)|object file .* does not exist|failed to',output,re.I))
        rows.append(row)
        print(name,row['returncode'],row['semantic_type_rejection'],flush=True)
    record(ROOT/'INDEPENDENT_CONTROLS.json',dict(positive=result,negatives=rows,
        all_pass=result['returncode']==0 and len(rows)==2 and all(r['semantic_type_rejection'] for r in rows)))

if __name__=='__main__': main()
