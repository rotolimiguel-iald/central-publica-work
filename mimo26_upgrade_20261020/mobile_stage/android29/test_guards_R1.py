"""Offline guard checks; no Gradle, signing command, remote request or Git mutation."""
from pathlib import Path
import ast, copy, json, tempfile, types, unittest
from unittest.mock import patch
import run_android29 as runner

HERE=Path(__file__).resolve().parent
class Guards(unittest.TestCase):
    def test_source_linked_authorizations(self):
        for filename,operation,plan in [('AUTHORIZATION_ANDROID29_R1.json','android29_build','ANDROID29_BUILD_PLAN_R1.json'),('AUTHORIZATION_PRIVATE_COMMIT_R1.json','private_mobile_commit','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json'),('AUTHORIZATION_PRIVATE_PUSH_R1.json','private_mobile_push','PRIVATE_MOBILE_PUBLISH_PLAN_R1.json')]:
            runner.require_approval(HERE/filename,operation,HERE/plan)
    def test_wrong_operation_refused(self):
        with self.assertRaises(RuntimeError):runner.require_approval(HERE/'AUTHORIZATION_ANDROID29_R1.json','private_mobile_push',HERE/'ANDROID29_BUILD_PLAN_R1.json')
    def test_tampered_authorization_pin_refused(self):
        value=json.loads((HERE/'AUTHORIZATION_ANDROID29_R1.json').read_bytes());value['sources'][0]['sha256']='0'*64
        with tempfile.TemporaryDirectory(dir=HERE) as d:
            path=Path(d)/'synthetic.json';path.write_text(json.dumps(value))
            with self.assertRaises(RuntimeError):runner.require_approval(path,'android29_build',HERE/'ANDROID29_BUILD_PLAN_R1.json')
    def test_build_log_never_exposes_keypass(self):
        text,omitted=runner.safe_line('keypass=synthetic-noncredential')
        self.assertTrue(omitted);self.assertNotIn('synthetic-noncredential',text)
    def test_toolchain_pins_unchanged(self):
        p=json.loads((HERE/'ANDROID29_BUILD_PLAN_R1.json').read_bytes())
        for item in p['tool_pins']:self.assertEqual(runner.digest(item['path']),item['sha256'])
        self.assertEqual(p['versionCode'],29);self.assertEqual(len(p['resource_files']),40)
        self.assertEqual(p['accepted_js_sha256'],'717b73f815abb80af0aa8cb1d5277b04b179dde5728640de079fd0fb306d7827')
    def test_current_inputs_refuse_before_install(self):
        p=json.loads((HERE/'ANDROID29_BUILD_PLAN_R1.json').read_bytes())
        differences=runner.verify_files(p)
        # This receipt is a snapshot before installation; no assumption of later state.
        self.assertTrue(differences)
        expected={x['destination'] for x in json.loads((HERE.parent/'packages/client_R4_final_ios34_android29/install_plan_mobile_R4_FINAL.json').read_bytes())['files']}
        self.assertTrue(set(differences)<=expected)
    def test_preflight_stale_and_wrong_owner_refuse(self):
        receipt=dict(context_id='synthetic-fixture-only',scope={'house':'IALD','principal':'synthetic'},revision=1,state_sha256='0'*64)
        old=dict(ready=True,task_id='deploy',lease_id='synthetic-lease',receipt=receipt,projection_sha256='1'*64)
        new=dict(receipt=copy.deepcopy(receipt),projection_sha256='1'*64,projection={'active':[dict(id='deploy',status='working',lease=dict(id='synthetic-lease',owner='codex-app-01a094df',expires_at=9999999999))]})
        for bad in ['stale','owner']:
            value=copy.deepcopy(new)
            if bad=='stale':value['receipt']['revision']=2
            else:value['projection']['active'][0]['lease']['owner']='different-synthetic-owner'
            with tempfile.TemporaryDirectory(dir=HERE) as d:
                folder=Path(d);p=folder/'synthetic-check.json';p.write_text(json.dumps(dict(ok=True,result=old)))
                reply=types.SimpleNamespace(returncode=0,stdout=json.dumps(dict(ok=True,result=value)))
                with patch.object(runner.subprocess,'run',return_value=reply):
                    with self.assertRaises(RuntimeError):runner.fresh_preflight(p,folder)
    def test_private_allowlist_only_four_tracked_mobile_paths(self):
        p=json.loads((HERE/'PRIVATE_MOBILE_PUBLISH_PLAN_R1.json').read_bytes())
        self.assertEqual(set(p['files']),{'www/iald.js','ios/App/App/public/iald.js','ios/App/App.xcodeproj/project.pbxproj','android/app/build.gradle'})
        source=(HERE/'private_mobile_publish.py').read_text()
        self.assertNotIn("'--force'",source);self.assertNotIn("'add','.'",source)
        self.assertIn('ls-remote',source);self.assertIn('no_repeat=True',source)
    def test_reused_guard_functions_preserved(self):
        old=Path(r'C:\IALD\Central de Patentes\work\memoria_organismo_20261016\mobile_build\run_android28.py')
        a={n.name:ast.dump(n,include_attributes=False) for n in ast.parse(old.read_bytes()).body if isinstance(n,ast.FunctionDef)}
        b={n.name:ast.dump(n,include_attributes=False) for n in ast.parse((HERE/'run_android29.py').read_bytes()).body if isinstance(n,ast.FunctionDef)}
        for name in ['digest','pin','save','no_reparse','safe_line','collect']:self.assertEqual(a[name],b[name],name)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Guards))
    runner.save(HERE/'GUARD_TEST_RESULTS_R1.json',dict(status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),synthetic_preflight_fixtures=True,build_executed=False,signature_tools_executed=False,git_mutations=False,remote_calls=0))
    raise SystemExit(0 if result.wasSuccessful() else 1)
