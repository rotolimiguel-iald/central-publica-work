"""Plan by default; --result audits only the new public Android30 archives."""
from pathlib import Path, PurePosixPath
from collections import Counter
import argparse, ast, hashlib, json, re, subprocess, zipfile
from run_android30_R1 import pin, save, verify_files

HERE=Path(__file__).resolve().parent
PLAN=HERE/'ANDROID30_BUILD_PLAN_R1.json'
def audit(result_path):
    plan=json.loads(PLAN.read_bytes())
    path=Path(result_path).resolve(strict=True)
    if not path.is_relative_to((HERE/'attempts').resolve()) or path.name!='RESULT_R1.json':
        raise RuntimeError('Only this new runner result can be audited')
    build=json.loads(path.read_bytes())
    if (build['plan']!=pin(PLAN) or build['status']!='BUILT_PUBLIC_CHECKS_PASS_PENDING_ARCHIVE_REVIEW'
            or not build['protected_inputs_unchanged'] or not build['init_markers_present']):
        raise RuntimeError('Successful guarded build receipt required')
    for item in [build['build']['log'],*[x['log'] for x in build['artifacts']['inspections'].values()]]:
        if pin(item['path'])!=item:raise RuntimeError('Build evidence changed')
    source=plan['parser_source']
    if pin(source['path'])!=source:raise RuntimeError('Public archive parsers changed')
    tree=ast.parse(Path(source['path']).read_bytes())
    names={'sha','run','name_issues','secret_matches','signatures','protobuf_fields','manifest_attributes'}
    selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    if {x.name for x in selected}!=names:raise RuntimeError('Missing audited parser')
    patterns=next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PATTERNS' for t in n.targets))
    ns=dict(hashlib=hashlib,subprocess=subprocess,re=re,PurePosixPath=PurePosixPath,
        PATTERNS=ast.literal_eval(patterns),TOOLS={k:Path(v) for k,v in plan['tools'].items()})
    exec(compile(ast.Module(body=selected,type_ignores=[]),source['path'],'exec'),ns)
    paths={k:Path(build['artifacts'][k]['path']) for k in ['apk','aab']}
    paths['previous_apk']=Path(plan['baseline_apk']['path'])
    for k in ['apk','aab']:
        if pin(paths[k])!=build['artifacts'][k]:raise RuntimeError('Archive bytes changed')
    if pin(paths['previous_apk'])!=plan['baseline_apk']:raise RuntimeError('Previous29 APK changed')
    signature=ns['signatures'](paths)
    expected={x['relative']:x['sha256'] for x in plan['resource_files']}
    packages={};checks={}
    for kind in ['apk','aab']:
        prefix=('base/' if kind=='aab' else '')+'assets/public/'
        with zipfile.ZipFile(paths[kind]) as z:
            members=[x.filename for x in z.infolist() if not x.is_dir()]
            duplicates=[n for n,c in Counter(members).items() if c>1]
            public={};bad=[];findings=[]
            for name in members:
                issues=ns['name_issues'](name)
                if issues:bad.append(dict(file=name,categories=issues));continue
                raw=z.read(name)
                matches=ns['secret_matches'](raw)
                if matches:findings.append(dict(file=name,categories=matches))
                if name.startswith(prefix):public[name[len(prefix):]]=hashlib.sha256(raw).hexdigest()
            registry=('base/' if kind=='aab' else '')+'assets/capacitor.plugins.json'
            regok=hashlib.sha256(z.read(registry)).hexdigest()==plan['registry']['sha256']
            packages[kind]=dict(artifact=pin(paths[kind]),public_assets=public,duplicates=duplicates,
                forbidden_names=bad,pattern_findings=findings,registry_matches=regok,crc_error=z.testzip())
            if kind=='aab':packages[kind]['manifest']=ns['manifest_attributes'](z.read('base/manifest/AndroidManifest.xml'))
            checks[kind+'_resources']=public==expected and public.get('iald.js')==plan['accepted_js_sha256'] and regok
            checks[kind+'_archive']=not duplicates and packages[kind]['crc_error'] is None and not bad and not findings
    apk=signature['apk_metadata'];aab=packages['aab']['manifest']
    checks['apk_manifest30']=apk['exit_code']==0 and all(apk['attributes'].get(k)==v for k,v in dict(name='br.ia.IALD',versionCode='30',versionName='4.1').items())
    checks['aab_manifest30']=all(aab.get(k)==v for k,v in dict(package='br.ia.IALD',versionCode='30',compiled_versionCode=30,versionName='4.1').items())
    signed=signature['aab_signature']
    checks['signed_apk_continuity']=signature['apk']['verified'] and signature['previous_apk']['verified'] and signature['all_same_certificate']
    checks['signed_aab_all_entries']=signed['exit_code']==0 and signed['jar_verified'] and not signed['unsigned_entries_warning'] and signed['signed_entries']>0 and signed['certificate_exit_code']==0
    checks['unchanged_artifacts']=signature['artifacts_unchanged_during_verification']
    checks['unchanged_protected_inputs']=not verify_files(plan)
    output=path.parent/'ARCHIVE_AUDIT_R1.json'
    save(output,dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,build_result=pin(path),
        plan=pin(PLAN),signature_evidence=signature,packages=packages,published=False,installed_on_device=False,
        scope='Technical archive audit by builder; independent main review remains required. Pattern checks are bounded detection.'))
    return dict(result=pin(output),status='PASS' if all(checks.values()) else 'FAIL',published=False)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--result',type=Path);a=p.parse_args()
    if a.result:
        out=audit(a.result);print(json.dumps(out));raise SystemExit(0 if out['status']=='PASS' else 1)
    print(json.dumps(dict(mode='PLAN_ONLY',audit_started=False,build_started=False,plan=str(PLAN))))
