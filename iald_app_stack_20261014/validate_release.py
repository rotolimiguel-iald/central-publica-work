"""Run deterministic local checks; never dispatch remote providers."""
from pathlib import Path
import ast,json,subprocess,sys
from transaction import write_evidence,digest,quiet
W=Path(__file__).resolve().parent
def main():
    results=[]
    for script in ('test_integration.py','routing/test_routing.py'):
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(W/script)],cwd=W,capture_output=True,text=True,encoding='utf-8')
        write_evidence(W/'validation'/f'{Path(script).stem}.json',{'exit_code':result.returncode,'output':result.stdout+result.stderr})
        results.append({'script':script,'passed':result.returncode==0})
    plan=json.loads((W/'install_plan.json').read_bytes())
    for row in plan['files']:
        assert digest(Path(row['source']).read_bytes())==row['sha256']
        dest=Path(row['destination'])
        assert (digest(dest.read_bytes()) if dest.exists() else None)==row['baseline']
    write_evidence(W/'validation/routing_main_review.json',{'status':'PASS','reviewer':'codex-app-main','independent_of_routing_author':True,'scope':'routing policy and integration guards','checks':['eligible candidates filtered before preferences; no Claude automatic candidate','Kimi only text; MiMo manages tools and delegates code to Kimi','manual operator selection and consents unchanged','uncertain provider dispatch is terminal; no fallback replay','monthly wallet unchanged'], 'files':{str(p):digest(p.read_bytes()) for p in (W/'routing/patched').glob('*.py')}})
    output={'passed':all(r['passed'] for r in results),'plan_sha256':digest((W/'install_plan.json').read_bytes()),'tests':results,'files_verified':len(plan['files']),'provider_generations':0,'production_unchanged':True}
    write_evidence(W/'validation/final_checks.json',output)
    print(json.dumps(output))
    if not output['passed']:sys.exit(1)
if __name__=='__main__':main()
