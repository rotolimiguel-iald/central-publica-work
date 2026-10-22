"""Synthetic tests only. No production mutation, process control, Git or build."""
from pathlib import Path
import ast, contextlib, hashlib, io, json, tempfile, unittest
from unittest.mock import patch
import prepare
import guards

@contextlib.contextmanager
def sandbox_fixture():
    # Keep synthetic evidence under the writable release; no recursive cleanup.
    import uuid
    p=prepare.W/'test_fixtures'/uuid.uuid4().hex
    p.mkdir(parents=True)
    yield str(p)

class PreparationTests(unittest.TestCase):
    def test_imports_have_no_subprocess_calls(self):
        # Imports of the runners must not start their main functions.
        with patch('subprocess.run', side_effect=AssertionError('Unexpected subprocess')), \
             patch('subprocess.Popen', side_effect=AssertionError('Unexpected process')):
            import mobile_release
            import deploy_controlled
            import publish_apk33

    def test_no_plan_no_admission(self):
        with sandbox_fixture() as temp, patch.object(guards,'W',Path(temp)), \
             patch.object(guards,'preflight',side_effect=AssertionError('Unexpected admission')):
            with self.assertRaises(FileNotFoundError):
                guards.reviewed()

    def test_private_paths_refused(self):
        for name in ['.env','iald_stack_v7.py','keystore.properties','signing.jks']:
            with self.assertRaises(ValueError):
                prepare.safe(Path(tempfile.gettempdir())/name)

    def test_synthetic_assembly_and_cas(self):
        with sandbox_fixture() as temp:
            root=Path(temp);parent=root/'task';w=parent/'release';prod=root/'production';mobile=prod/'iald-app'
            w.mkdir(parents=True);source=parent/'asset.js';source.write_bytes(b'new content')
            surfaces=(prod/'app',mobile/'www',mobile/'ios/App/App/public',mobile/'android/app/src/main/assets/public')
            for s in surfaces:
                s.mkdir(parents=True);(s/'asset.js').write_bytes(b'old content')
            ios=mobile/prepare.NATIVES[0];ios.parent.mkdir(parents=True,exist_ok=True)
            ios.write_bytes(b'CURRENT_PROJECT_VERSION = 37;\nCURRENT_PROJECT_VERSION = 37;\n')
            gradle=mobile/prepare.NATIVES[1];gradle.write_bytes(b'versionCode 32\n')
            science=prod/'science.txt';science.write_bytes(b'preserved')
            (w/'SCIENCE_BASELINE.json').write_text(json.dumps({'files':[{'path':str(science),'sha256':prepare.sha(science)}]}))
            spec={'assets':[{'name':'asset.js','source':str(source),'sha256':prepare.sha(source),
                            'baselines':{str(s/'asset.js'):prepare.sha(s/'asset.js') for s in surfaces}}], 'runtime':[]}
            manifest=parent/'manifest.json';manifest.write_text(json.dumps(spec))
            before={str(p):p.read_bytes() for p in prod.rglob('*') if p.is_file()}
            with patch.multiple(prepare,W=w,PARENT=parent,ROOT=prod,MOBILE=mobile,SURFACES=surfaces):
                with self.assertRaises(ValueError):
                    prepare.row(source,surfaces[0]/'asset.js','0'*64,prepare.sha(surfaces[0]/'asset.js'))
                with self.assertRaises(ValueError):
                    prepare.row(source,surfaces[0]/'asset.js',prepare.sha(source),'0'*64)
                with contextlib.redirect_stdout(io.StringIO()):
                    prepare.assemble(manifest)
                plan=prepare.load(w/'install_plan.json')
                self.assertEqual(len(plan['files']),6)
                self.assertEqual(prepare.load(w/'NATIVE_PLAN.json')['ios'],'4.1(38)')
                self.assertEqual(prepare.load(w/'NATIVE_PLAN.json')['android'],'4.1(33)')
                self.assertEqual(len(prepare.load(w/'PRIVATE_GIT_PLAN.json')['files']),4)
                self.assertFalse((w/'validation/review_final.json').exists())
                with self.assertRaises(ValueError):
                    prepare.assemble(manifest)
            after={str(p):p.read_bytes() for p in prod.rglob('*') if p.is_file()}
            self.assertEqual(before,after)

    def test_candidate_syntax_and_offline_configuration(self):
        for p in [*prepare.W.glob('*.py'), prepare.W/'mobile_prepare/build_log.py']:
            ast.parse(p.read_bytes())
        mobile=(prepare.W/'mobile_release.py').read_text()
        self.assertIn("'--offline'",mobile)
        self.assertIn('def commit(',mobile)
        self.assertIn('def push(',mobile)
        self.assertIn('COMMIT_INTENT.json',mobile)
        self.assertIn('PUSH_INTENT.json',mobile)
        self.assertIn("plan['assets']",mobile)
        self.assertIn('versionCode=33',mobile)

if __name__=='__main__':
    unittest.main(verbosity=2)
