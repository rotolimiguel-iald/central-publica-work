"""AST/text-only checks: never import or execute a release pipeline."""
from pathlib import Path
import ast,json,hashlib
W=Path(__file__).resolve().parent.parent
O=W/'mobile_prepare'
checks=[]
def check(name,value):
    assert value,name
    checks.append({'name':name,'pass':True})
for path in [W/'mobile_release.py',W/'publish_apk32.py',O/'prepare_native.py',O/'build_log.py']:
    ast.parse(path.read_bytes());check('syntax_'+path.name,True)
s=(W/'mobile_release.py').read_text();pub=(W/'publish_apk32.py').read_text();init=(W/'android32.init.gradle').read_text()
needles={
 'current_deploy':"assert check('deploy')['ready']",
 'installed_plan':"deployment['plan_sha256']==sha(W/'install_plan.json')",
 'exact_resource_plan':'resources=resource_pins(checked())',
 'four_surfaces':'for surface in SURFACES:',
 'eight_git_files':'assert len(allowed)==8',
 'new_file_mode':"mode=tracked.split()[0] if tracked else '100644'",
 'raw_git_bytes':"'hash-object','-w','--no-filters'",
 'new_index_entry':"'update-index','--add','--cacheinfo'",
 'push_url_recheck':"gs('remote','get-url','--push','origin') in urls",
 'offline':'--offline', 'explicit_init':'android32.init.gradle',
 'apk32':"versionCode='32'",'aab_negative':'unsigned entries',
 'aab_positive':'jar verified.','aab_cert':'aab_cert[0]',
 'science':'mobile_prepare/SCIENCE_PINS.json','one_shot_build':'a.mkdir(exist_ok=False)',
 'commit_intent':'COMMIT_INTENT.json','push_intent':'PUSH_INTENT.json',
}
for name,text in needles.items():check(name,text in s)
check('no_old_staging',all(x not in s for x in ['OLD','client_stage','android31','build31']))
check('init32', 'versionCode != 32' in init and 'acom_signal_transport_20261021/mobile_stage' in init)
check('publisher32',"['versionCode']==32" in pub and 'IALD-4.1-32.apk' in pub and 'APK_PUBLICATION_INTENT.json' in pub)
def functions(path):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_bytes()).body if isinstance(n,ast.FunctionDef)}
old=W.parent/'mimo_media_capacity_20261020/client_stage/android30_final19_label_R8/run_android30_R1.py'
a=functions(old);b=functions(O/'build_log.py')
check('logger_functions_exact_AST',all(a[n]==b[n] for n in b))
check('private_key_log_guard','private-key block omitted' in (O/'build_log.py').read_text())
baseline=json.loads((O/'PREPARATION_BASELINE.json').read_bytes())
check('original_inputs_unchanged',all(hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in baseline['inputs']))
result={'status':'PASS_STATIC_ONLY','checks':checks,'count':len(checks),'pipeline_imported_or_executed':False,'build_git_publication_runtime':False,'credentials_read':False}
(O/'STATIC_TESTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'checks':len(checks)}))
