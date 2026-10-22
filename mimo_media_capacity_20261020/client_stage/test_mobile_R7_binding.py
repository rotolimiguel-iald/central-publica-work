"""Offline R7 lineage/binding checks; no build, Git, signature or provider calls."""
from pathlib import Path
import ast,json,sys,subprocess
S=Path(__file__).resolve().parent;D=S/'android30_R7_bound'
sys.path.insert(0,str(D))
import run_android30_R1 as runner
import release_lineage_R7 as guard
def main():
    build=json.loads((D/'ANDROID30_BUILD_PLAN_R1.json').read_bytes())
    pub=json.loads((D/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json').read_bytes());checks={}
    runner.verify_main_plan(build);runner.verify_main_plan(pub);checks['both_plans_bound']=True
    effective=json.loads(Path(build['main_plan_current_pin']['path']).read_bytes())
    six=json.loads(Path(build['resource_plan']['path']).read_bytes())
    checks['effective_explicit_not_installable']=effective['installable'] is False and effective['status']=='NOT_INSTALLABLE_EFFECTIVE_STATE' and all('baseline' not in x for x in effective['files'])
    checks['effective18_mobile6_hotfix4']=len(effective['files'])==18 and len(six['files'])==6 and sum(x['origin']=='hotfix4' for x in effective['files'])==4
    checks['native_versions_from_original18']=sum(x['installed_by']=='original18' for x in six['files'])==2 and six['versions']==dict(ios=35,android=30)
    checks['exact4_private_paths']=set(pub['files'])=={'www/iald.js','ios/App/App/public/iald.js','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle'}
    code=(D/'private_mobile_publish_R1.py').read_text()
    checks['raw_no_filter_staging']="'hash-object','-w','--no-filters'" in code and "'update-index','--cacheinfo'" in code and "git(root,'add'" not in code
    checks['no_force_or_gitconfig']='--force' not in code and "git(root,'config'" not in code
    for n in ['run_android30_R1.py','audit_android30_R1.py','private_mobile_publish_R1.py','release_lineage_R7.py']:
        ast.parse((D/n).read_bytes());checks[n+'_syntax']=True
    for op in ['android30_build','private_mobile_commit','private_mobile_push']:
        path=D/('TEMPLATE_'+op.upper()+'.json');template=json.loads(path.read_bytes())
        checks[op+'_two_installations']=len(template['installation_receipts'])==2 and {x['role'] for x in template['installation_receipts']}=={'original18','hotfix4'}
        try:guard.verify_release_admission(template,build,D.parents[1])
        except RuntimeError:checks[op+'_pending_hotfix_blocks']=True
        else:checks[op+'_pending_hotfix_blocks']=False
    # Original18 evidence cannot stand in for the missing hotfix installation.
    original=build['installation_chain']['original18_installed']
    sample=dict(review_receipts=[dict(role='original18',**build['installation_chain']['original18_review']),dict(role='hotfix4',**build['installation_chain']['original18_review'])],
                installation_receipts=[dict(role='original18',**original),dict(role='hotfix4',**original)],ui_verification=None)
    try:guard.verify_release_admission(sample,build,D.parents[1])
    except RuntimeError as e:checks['original18_cannot_impersonate_hotfix4']='actual installation plan' in str(e)
    else:checks['original18_cannot_impersonate_hotfix4']=False
    cp=subprocess.run([sys.executable,'-B',str(D/'run_android30_R1.py')],capture_output=True)
    reply=json.loads(cp.stdout);checks['plan_only_execution_false']=cp.returncode==0 and reply['mode']=='PLAN_ONLY' and reply['build_started'] is False
    checks['no_execution_intents']=not (D/'RUN_INTENT_R1.json').exists() and not (D/'git_commit_R1').exists() and not (D/'git_push_R1').exists()
    assert all(checks.values()),checks
    runner.save(D/'BINDING_TEST_RESULTS_R7.json',dict(status='PASS_OFFLINE_BINDING_GUARDS',checks=checks,count=len(checks),expected_pre_hotfix_installed_pin_mismatches=reply['input_mismatches'],build=False,commit=False,push=False,install=False))
    print(json.dumps(dict(status='PASS',checks=len(checks),mismatches=len(reply['input_mismatches']))))
if __name__=='__main__':main()
