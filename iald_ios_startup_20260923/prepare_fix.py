"""Stage the iOS scene migration without changing the installed app sources."""
from pathlib import Path
import hashlib
import json
import plistlib

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
WORK = Path(__file__).resolve().parent
STAGE = WORK / 'stage_v2'
changes = {}

def stage(relative, transform):
    before = (ROOT / relative).read_bytes()
    after = transform(before)
    assert before != after
    target = STAGE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        with target.open('xb') as out:
            out.write(after)
    assert target.read_bytes() == after
    changes[relative] = {'before': hashlib.sha256(before).hexdigest(),
                         'after': hashlib.sha256(after).hexdigest()}

def swift(raw):
    addition = '''
// iOS 27 requires the scene lifecycle for apps built with the iOS 27 SDK.
// Main.storyboard owns the window and the Capacitor bridge: do not create a
// second window/WebView here. Capacitor's proxy preserves cold/warm OAuth links.
class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?

    func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
        SceneDelegateProxy.shared.scene(scene, willConnectTo: session, options: connectionOptions)
    }

    func scene(_ scene: UIScene, openURLContexts URLContexts: Set<UIOpenURLContext>) {
        SceneDelegateProxy.shared.scene(scene, openURLContexts: URLContexts)
    }

    func scene(_ scene: UIScene, continue userActivity: NSUserActivity) {
        SceneDelegateProxy.shared.scene(scene, continue: userActivity)
    }
}
'''
    assert b'class SceneDelegate' not in raw
    newline = '\r\n' if b'\r\n' in raw else '\n'
    return raw + addition.replace('\n', newline).encode('utf8')

def plist(raw):
    newline = '\r\n' if b'\r\n' in raw else '\n'
    old = ('\t<key>UIMainStoryboardFile</key>' + newline + '\t<string>Main</string>').encode()
    assert raw.count(old) == 1
    replacement = '''	<key>UIApplicationSceneManifest</key>
	<dict>
		<key>UIApplicationSupportsMultipleScenes</key>
		<false/>
		<key>UISceneConfigurations</key>
		<dict>
			<key>UIWindowSceneSessionRoleApplication</key>
			<array>
				<dict>
					<key>UISceneConfigurationName</key>
					<string>Default Configuration</string>
					<key>UISceneClassName</key>
					<string>UIWindowScene</string>
					<key>UISceneDelegateClassName</key>
					<string>$(PRODUCT_MODULE_NAME).SceneDelegate</string>
					<key>UISceneStoryboardFile</key>
					<string>Main</string>
				</dict>
			</array>
		</dict>
	</dict>'''.replace('\n', newline).encode()
    after = raw.replace(old, replacement)
    previous = plistlib.loads(raw)
    current = plistlib.loads(after)
    assert previous.pop('UIMainStoryboardFile') == 'Main'
    scene = current.pop('UIApplicationSceneManifest')
    assert current == previous, 'Unrelated plist settings changed'
    assert scene['UIApplicationSupportsMultipleScenes'] is False
    return after

def version(raw):
    assert raw.count(b'CURRENT_PROJECT_VERSION = 21;') == 2
    return raw.replace(b'CURRENT_PROJECT_VERSION = 21;', b'CURRENT_PROJECT_VERSION = 22;')

stage('ios/App/App/AppDelegate.swift', swift)
stage('ios/App/App/Info.plist', plist)
stage('ios/App/App.xcodeproj/project.pbxproj', version)
with (WORK / 'manifest.json').open('x', encoding='utf8') as out:
    json.dump(changes, out, indent=2)
print(json.dumps({'staged': list(changes), 'web_changed': False, 'android_changed': False}))
