import hashlib
import json
from pathlib import Path
import plistlib
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]


class PatchTests(unittest.TestCase):
    def test_source_and_review_hashes_match_manifest(self):
        manifest=json.loads((ROOT/'patch-manifest.json').read_text())
        for item in manifest['files']:
            with self.subTest(path=item['path']):
                source=Path(manifest['source'])/item['path']
                actual=hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None
                self.assertEqual(actual,item['source_sha256'])
                self.assertEqual(hashlib.sha256((ROOT/'proposed'/item['path']).read_bytes()).hexdigest(),item['proposed_sha256'])
                self.assertNotIn('iald.js',item['path']); self.assertNotIn('server',item['path'])

    def test_ios_entitlements_preserve_apple_login_and_scene(self):
        p=ROOT/'proposed/ios/App'
        ent=plistlib.loads((p/'App/App.entitlements').read_bytes())
        self.assertEqual(ent['com.apple.developer.applesignin'],['Default'])
        self.assertEqual(ent['aps-environment'],'$(APS_ENVIRONMENT)')
        delegate=(p/'App/AppDelegate.swift').read_text()
        self.assertEqual(delegate.count('SceneDelegateProxy.shared.scene('),3)
        self.assertEqual(delegate.count('ApplicationDelegateProxy.shared.application('),2)
        self.assertIn('.capacitorDidRegisterForRemoteNotifications',delegate)
        self.assertNotIn('UNUserNotificationCenter.current().delegate',delegate)
        project=(p/'App.xcodeproj/project.pbxproj').read_text()
        self.assertEqual(project.count('APS_ENVIRONMENT = development;'),1)
        self.assertEqual(project.count('APS_ENVIRONMENT = production;'),1)

    def test_android_defaults_disabled_and_no_custom_messaging_service(self):
        p=ROOT/'proposed/android/app'
        manifest=ET.fromstring((p/'src/main/AndroidManifest.xml').read_bytes())
        ns='{http://schemas.android.com/apk/res/android}'
        metadata={n.get(ns+'name'):n.get(ns+'value') for n in manifest.findall('.//meta-data')}
        self.assertEqual(metadata['firebase_messaging_auto_init_enabled'],'false')
        self.assertEqual(metadata['firebase_analytics_collection_enabled'],'false')
        self.assertEqual(metadata['com.google.firebase.messaging.default_notification_channel_id'],'iald_responses_v1')
        self.assertEqual(manifest.findall('.//service'),[])
        gradle=(p/'build.gradle').read_text()
        self.assertIn("findProperty('ialdPushEnabled') == 'true'",gradle)
        self.assertIn('if (ialdPushEnabled)',gradle)
        self.assertNotIn('servicesJSON.text',gradle)
        ET.fromstring((p/'src/main/res/drawable/ic_stat_iald.xml').read_bytes())

    def test_plugin_configuration_and_capacitor_version(self):
        package=json.loads((ROOT/'proposed/package.json').read_text())
        self.assertEqual(package['dependencies']['@capacitor/push-notifications'],'8.1.2')
        self.assertEqual(package['dependencies']['@capacitor/core'],'8.5.2')
        config=json.loads((ROOT/'proposed/capacitor.config.json').read_text())
        self.assertEqual(config['appId'],'br.ia.IALD')
        self.assertNotIn('url',config['server'])


if __name__=='__main__': unittest.main(verbosity=2)
