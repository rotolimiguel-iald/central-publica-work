"""Offline structural release gate, not Swift compilation or a device test.

Usage: python -B -X utf8 test_ios_scene_release.py --source stage_v2
Use --source ORIGINAL_APP to demonstrate the legacy lifecycle rejection.
Only public source files are read. No application, SDK, network or login runs.
The stage is an overlay: unchanged storyboards/dependencies come from --baseline.
"""
import argparse
import hashlib
import json
from pathlib import Path
import plistlib
import re
import sys
import subprocess
import unittest
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, default=HERE/'stage_v2')
parser.add_argument('--baseline', type=Path, default=ROOT)
parser.add_argument('--baseline-ref', default='f302650', help='Immutable Git baseline, independent of concurrent installation')
parser.add_argument('--source-ref', help='Read the three candidate files from this Git revision (for OLD negative control)')
parser.add_argument('--receipt', type=Path)
args = parser.parse_args()
PINS = {}

def git_read(ref, rel):
    commit = subprocess.run(['git', '-C', str(args.baseline), 'rev-parse', '--verify', ref+'^{commit}'],
                            check=True, capture_output=True).stdout.decode().strip()
    data = subprocess.run(['git', '-C', str(args.baseline), 'show', commit+':'+rel],
                          check=True, capture_output=True).stdout
    PINS['git:'+commit+':'+rel] = hashlib.sha256(data).hexdigest()
    return data

def candidate_read(rel):
    return git_read(args.source_ref, rel) if args.source_ref else read(args.source/rel)

def baseline_read(rel):
    return git_read(args.baseline_ref, rel)

def read(path):
    data = path.read_bytes()
    PINS[str(path.resolve())] = hashlib.sha256(data).hexdigest()
    return data

def overlay(rel):
    candidate = args.source/rel
    return candidate if candidate.is_file() else args.baseline/rel

def clean(text):
    # Preserve strings; remove comments so keywords in prose cannot satisfy gates.
    return re.sub(r'"(?:\\.|[^"\\])*"|/\*[\s\S]*?\*/|//[^\n]*',
                  lambda m: m.group(0) if m.group(0).startswith('"') else ' ', text)

def brace_body(text, start):
    pos = text.index('{', start)
    depth = 0
    for token in re.finditer(r'"(?:\\.|[^"\\])*"|[{}]', text[pos:]):
        if token.group() == '{': depth += 1
        elif token.group() == '}':
            depth -= 1
            if depth == 0: return text[pos+1:pos+token.start()]
    raise AssertionError('Unbalanced source braces')

def object_body(project, ident):
    match = re.search(r'\b'+re.escape(ident)+r'\s*=\s*\{', project)
    if not match: raise AssertionError('Missing PBX object '+ident)
    return brace_body(project, match.start())

def objects(project, kind):
    result = []
    for match in re.finditer(r'\b([A-F0-9]{24})\s*=\s*\{', project):
        body = brace_body(project, match.start())
        if re.search(r'\bisa\s*=\s*'+kind+r'\s*;', body):
            result.append((match[1], body))
    return result

class SceneRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plist_bytes = candidate_read('ios/App/App/Info.plist')
        cls.info = plistlib.loads(cls.plist_bytes)
        cls.old_info = plistlib.loads(baseline_read('ios/App/App/Info.plist'))
        cls.swift_bytes = candidate_read('ios/App/App/AppDelegate.swift')
        cls.swift = clean(cls.swift_bytes.decode('utf-8-sig'))
        cls.old_swift = baseline_read('ios/App/App/AppDelegate.swift')
        cls.pbx_bytes = candidate_read('ios/App/App.xcodeproj/project.pbxproj')
        cls.pbx = clean(cls.pbx_bytes.decode('utf-8-sig'))
        cls.old_pbx = baseline_read('ios/App/App.xcodeproj/project.pbxproj')

    def scene_config(self):
        manifest = self.info.get('UIApplicationSceneManifest')
        self.assertIsInstance(manifest, dict, 'Missing UIScene manifest: legacy source cannot pass release gate')
        self.assertIs(manifest.get('UIApplicationSupportsMultipleScenes'), False)
        configs = manifest.get('UISceneConfigurations', {})
        self.assertEqual(set(configs), {'UIWindowSceneSessionRoleApplication'})
        rows = configs['UIWindowSceneSessionRoleApplication']
        self.assertEqual(len(rows), 1)
        return rows[0]

    def scene_body(self):
        match = re.search(r'\bclass\s+SceneDelegate\s*:\s*UIResponder\s*,\s*UIWindowSceneDelegate\s*\{', self.swift)
        self.assertIsNotNone(match, 'SceneDelegate must conform to UIWindowSceneDelegate')
        return brace_body(self.swift, match.start())

    def test_scene_manifest_and_runtime_class_mapping(self):
        row = self.scene_config()
        self.assertEqual(row['UISceneClassName'], 'UIWindowScene')
        self.assertEqual(row['UISceneDelegateClassName'], '$(PRODUCT_MODULE_NAME).SceneDelegate')
        self.assertTrue(row.get('UISceneConfigurationName'))
        self.assertNotIn('UIMainStoryboardFile', self.info)
        self.assertEqual(len(re.findall(r'\bclass\s+SceneDelegate\b', self.swift)), 1)
        self.assertRegex(self.scene_body(), r'\bvar\s+window\s*:\s*UIWindow\?')
        self.assertNotIn('configurationForConnecting', self.swift, 'Unexpected override of plist configuration')

    def test_plist_xml_no_duplicate_keys_and_unrelated_values_preserved(self):
        for dictionary in ET.fromstring(self.plist_bytes).iter('dict'):
            keys = [n.text for n in dictionary if n.tag == 'key']
            self.assertEqual(len(keys), len(set(keys)), 'Duplicate plist keys')
        ignored = {'UIApplicationSceneManifest', 'UIMainStoryboardFile'}
        self.assertEqual({k:v for k,v in self.info.items() if k not in ignored},
                         {k:v for k,v in self.old_info.items() if k not in ignored})
        self.assertEqual(self.info['UILaunchStoryboardName'], 'LaunchScreen')
        self.assertTrue(self.info['CFBundleURLTypes'])

    def test_storyboard_initial_controller_and_resource_membership(self):
        self.assertEqual(self.scene_config()['UISceneStoryboardFile'], 'Main')
        for name in ('Main', 'LaunchScreen'):
            xml = ET.fromstring(read(overlay('ios/App/App/Base.lproj/'+name+'.storyboard')))
            initial = xml.get('initialViewController')
            self.assertTrue(initial)
            nodes = [e for e in xml.iter() if e.get('id') == initial]
            self.assertEqual(len(nodes), 1)
            if name == 'Main':
                self.assertEqual(nodes[0].get('customClass'), 'CAPBridgeViewController')
                self.assertEqual(nodes[0].get('customModule'), 'Capacitor')
            self.assertTrue(any(re.search(r'\bpath\s*=\s*Base\.lproj/'+name+r'\.storyboard;', b)
                                for _,b in objects(self.pbx, 'PBXFileReference')))
            self.assert_resource(name+'.storyboard')

    def assert_resource(self, name):
        variants = [i for i,b in objects(self.pbx, 'PBXVariantGroup')
                    if re.search(r'\bname\s*=\s*'+re.escape(name)+r';', b)]
        self.assertEqual(len(variants), 1)
        builds = [i for i,b in objects(self.pbx, 'PBXBuildFile') if variants[0] in b]
        self.assertEqual(len(builds), 1)
        self.assertTrue(any(builds[0] in b for _,b in objects(self.pbx, 'PBXResourcesBuildPhase')))

    def test_delegate_file_is_in_app_target_sources(self):
        refs = [i for i,b in objects(self.pbx, 'PBXFileReference')
                if re.search(r'\bpath\s*=\s*AppDelegate\.swift;', b)]
        self.assertEqual(len(refs), 1)
        builds = [i for i,b in objects(self.pbx, 'PBXBuildFile') if refs[0] in b]
        self.assertEqual(len(builds), 1)
        phases = [i for i,b in objects(self.pbx, 'PBXSourcesBuildPhase') if builds[0] in b]
        self.assertEqual(len(phases), 1)
        targets = [b for _,b in objects(self.pbx, 'PBXNativeTarget') if phases[0] in b]
        self.assertEqual(len(targets), 1)
        self.assertRegex(targets[0], r'\bname\s*=\s*App;')
        self.scene_body()

    def test_cold_warm_and_universal_url_forwarding(self):
        body = self.scene_body()
        expected = [
            ('willConnectTo', 'SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)'),
            ('openURLContexts', 'SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)'),
            ('continue', 'SceneDelegateProxy.shared.scene(scene, continue: userActivity)'),
        ]
        for label, statement in expected:
            match = re.search(r'func\s+scene\([^{}]*\b'+label+r'\b[^{}]*\)\s*\{', body)
            self.assertIsNotNone(match, label)
            method = brace_body(body, match.start())
            self.assertEqual(re.sub(r'\s+', '', method), re.sub(r'\s+', '', statement), label)
        self.assertEqual(body.count('SceneDelegateProxy.shared.scene('), 3)

    def test_no_second_window_or_duplicate_lifecycle_notifications(self):
        body = self.scene_body()
        for forbidden in ('UIWindow(', 'UIStoryboard(', 'WKWebView(', 'CAPBridgeViewController(',
                          'makeKeyAndVisible', 'NotificationCenter', 'UIApplication.shared',
                          'sceneDidBecomeActive', 'sceneWillEnterForeground'):
            self.assertNotIn(forbidden, body)
        self.assertTrue(self.swift_bytes.startswith(self.old_swift), 'Existing AppDelegate bytes modified')

    def test_only_project_change_is_build_21_to_22(self):
        self.assertEqual(re.findall(rb'CURRENT_PROJECT_VERSION = (\d+);', self.old_pbx), [b'21', b'21'])
        self.assertEqual(re.findall(rb'CURRENT_PROJECT_VERSION = (\d+);', self.pbx_bytes), [b'22', b'22'])
        self.assertEqual(self.pbx_bytes.replace(b'CURRENT_PROJECT_VERSION = 22;', b'CURRENT_PROJECT_VERSION = 21;'), self.old_pbx)

    def test_local_proxy_supports_deferred_cold_links_and_app_compatibility(self):
        proxy = clean(read(args.baseline/'node_modules/@capacitor/ios/Capacitor/Capacitor/CAPSceneDelegateProxy.swift').decode())
        self.assertIn('public class SceneDelegateProxy', proxy)
        self.assertIn('forName: .capacitorViewDidAppear', proxy)
        self.assertIn('NotificationCenter.default.removeObserver(token)', proxy)
        for fragment in ('self.scene(scene, openURLContexts: connectionOptions.urlContexts)',
                         'self.scene(scene, continue: userActivity)',
                         'ApplicationDelegateProxy.shared.lastURL =', '.capacitorOpenURL', '.capacitorOpenUniversalLink'):
            self.assertIn(fragment, proxy)
        app = clean(read(args.baseline/'node_modules/@capacitor/app/ios/Sources/AppPlugin/AppPlugin.swift').decode())
        self.assertIn('retainUntilConsumed: true', app)
        self.assertIn('ApplicationDelegateProxy.shared.lastURL', app)
        for event in ('didBecomeActiveNotification', 'willResignActiveNotification',
                      'didEnterBackgroundNotification', 'willEnterForegroundNotification'):
            self.assertIn('UIApplication.'+event, app)

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SceneRelease))
    receipt = {'source': str(args.source.resolve()), 'baseline': str(args.baseline.resolve()),
               'source_ref': args.source_ref, 'baseline_ref': args.baseline_ref,
               'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
               'success': result.wasSuccessful(), 'sha256_read': PINS,
               'limits': ['Structural source validation only; no Swift/Xcode compilation.',
                          'No iPhone execution, OAuth interaction or crash diagnosis.',
                          'Local dependency source inspected; Cloud SPM binary not inspected.']}
    if args.receipt:
        target = args.receipt.resolve()
        if not target.is_relative_to(HERE): raise ValueError('Receipt must remain in audit work folder')
        with target.open('x', encoding='utf-8') as handle:
            json.dump(receipt, handle, indent=2, ensure_ascii=False)
    sys.exit(0 if result.wasSuccessful() else 1)
