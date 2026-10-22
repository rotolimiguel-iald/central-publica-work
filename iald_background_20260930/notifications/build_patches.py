"""Read native source; generate REVIEW-ONLY patches inside this staging directory."""
from pathlib import Path
import difflib
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
records = []


def replace_once(text, old, new):
    if text.count(old) != 1: raise RuntimeError('Source context changed; review required')
    return text.replace(old,new,1)


def patch(group, relative, transform=None, new=None):
    source=SOURCE/relative
    raw=source.read_bytes() if source.exists() else b''
    before=raw.decode('utf-8').replace('\r\n','\n')
    after=transform(before) if transform else new
    if not after or after==before: raise RuntimeError('Empty or ineffective patch')
    diff=''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
         fromfile='a/'+relative if raw else '/dev/null',tofile='b/'+relative))
    destination=ROOT/'patches'/group
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('a',encoding='utf-8',newline='\n') as out:
        out.write('diff --git a/'+relative+' b/'+relative+'\n'+('new file mode 100644\n' if not raw else '')+diff)
    proposed=ROOT/'proposed'/relative
    proposed.parent.mkdir(parents=True,exist_ok=True)
    proposed.write_text(after,encoding='utf-8',newline='\n')
    records.append({'path':relative,'patch':group,'source_exists':bool(raw),
                    'source_sha256':hashlib.sha256(raw).hexdigest() if raw else None,
                    'proposed_sha256':hashlib.sha256(after.encode()).hexdigest()})


def main():
    # Refuse to overwrite a review snapshot; all generated paths stay under ROOT.
    if (ROOT/'patches').exists(): raise RuntimeError('Patches already exist; do not overwrite baseline')
    patch('01-dependency.patch','package.json',lambda s:replace_once(s,
      '"@capacitor/ios": "8.5.2",','"@capacitor/ios": "8.5.2",\n    "@capacitor/push-notifications": "8.1.2",'))
    def config(s):
        value=json.loads(s)
        value['plugins']['PushNotifications']={'presentationOptions':['banner','list','sound']}
        return json.dumps(value,ensure_ascii=False,indent=2)+'\n'
    patch('02-capacitor-config.patch','capacitor.config.json',config)
    callbacks='''    // Forward APNs registration to the official Capacitor plugin.
    func application(_ application: UIApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
        NotificationCenter.default.post(name: .capacitorDidRegisterForRemoteNotifications, object: deviceToken)
    }

    func application(_ application: UIApplication, didFailToRegisterForRemoteNotificationsWithError error: Error) {
        NotificationCenter.default.post(name: .capacitorDidFailToRegisterForRemoteNotifications, object: error)
    }

'''
    patch('03-ios-after-approval.patch','ios/App/App/AppDelegate.swift',lambda s:replace_once(s,
       '    func applicationWillResignActive(',callbacks+'    func applicationWillResignActive('))
    patch('03-ios-after-approval.patch','ios/App/App/App.entitlements',lambda s:replace_once(s,
       '</dict>','\t<key>aps-environment</key>\n\t<string>$(APS_ENVIRONMENT)</string>\n</dict>'))
    def project(s):
        s=replace_once(s,'\t\t\t\t\t\tProvisioningStyle = Automatic;',
          '\t\t\t\t\t\tProvisioningStyle = Automatic;\n\t\t\t\t\t\tSystemCapabilities = {\n'
          '\t\t\t\t\t\t\tcom.apple.Push = { enabled = 1; };\n\t\t\t\t\t\t};')
        for identifier,environment in [('504EC3171FED79650016851F','development'),('504EC3181FED79650016851F','production')]:
            expression=r'('+identifier+r' /\* (?:Debug|Release) \*/ = \{.*?buildSettings = \{)'
            s,n=re.subn(expression,lambda m:m.group(1)+'\n\t\t\t\tAPS_ENVIRONMENT = '+environment+';',s,count=1,flags=re.S)
            if n!=1: raise RuntimeError('Missing Xcode target configuration')
        return s
    patch('03-ios-after-approval.patch','ios/App/App.xcodeproj/project.pbxproj',project)
    metadata='''        <!-- Disabled until explicit authenticated opt-in. register() enables FCM. -->
        <meta-data android:name="firebase_messaging_auto_init_enabled" android:value="false" />
        <meta-data android:name="firebase_analytics_collection_enabled" android:value="false" />
        <meta-data android:name="com.google.firebase.messaging.default_notification_channel_id" android:value="iald_responses_v1" />
        <meta-data android:name="com.google.firebase.messaging.default_notification_icon" android:resource="@drawable/ic_stat_iald" />
'''
    patch('04-android-opt-in.patch','android/app/src/main/AndroidManifest.xml',lambda s:
      replace_once(replace_once(s,'        <activity\n',metadata+'        <activity\n'),
        '    <!-- Permissions -->','    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />\n\n    <!-- Permissions -->'))
    def gradle(s):
        old=s[s.index("try {\n    def servicesJSON = file('google-services.json')"):]
        tail='''// Default builds keep push disabled and do not require Firebase configuration.
def ialdPushEnabled = project.findProperty('ialdPushEnabled') == 'true'
android.defaultConfig.resValue 'bool', 'iald_push_enabled', ialdPushEnabled.toString()
if (ialdPushEnabled) {
    def configFile = file('google-services.json')
    if (!configFile.isFile() || configFile.length() == 0) {
        throw new GradleException('Push enabled but google-services.json is missing')
    }
    apply plugin: 'com.google.gms.google-services'
}
'''
        return replace_once(s,old,tail)
    patch('04-android-opt-in.patch','android/app/build.gradle',gradle)
    patch('04-android-opt-in.patch','android/app/src/main/java/br/ia/iald/app/MainActivity.java',new='''package br.ia.iald.app;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.os.Build;
import android.os.Bundle;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        registerPlugin(IaldPushReadinessPlugin.class);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                "iald_responses_v1", "Respostas prontas", NotificationManager.IMPORTANCE_DEFAULT);
            channel.setDescription("Avisos de respostas concluídas na IALD");
            channel.setLockscreenVisibility(Notification.VISIBILITY_PRIVATE);
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) manager.createNotificationChannel(channel);
        }
        super.onCreate(savedInstanceState);
    }
}
''')
    patch('04-android-opt-in.patch','android/app/src/main/java/br/ia/iald/app/IaldPushReadinessPlugin.java',new='''package br.ia.iald.app;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "IaldPushReadiness")
public class IaldPushReadinessPlugin extends Plugin {
    @PluginMethod
    public void getStatus(PluginCall call) {
        boolean ready = false;
        if (getContext().getResources().getBoolean(R.bool.iald_push_enabled)) {
            try {
                // No Firebase dependency required in disabled builds; never creates a token.
                Class<?> firebase = Class.forName("com.google.firebase.FirebaseApp");
                ready = firebase.getMethod("getInstance").invoke(null) != null;
            } catch (Exception | LinkageError ignored) {
                // No exception body, config or credential goes to JavaScript/logs.
            }
        }
        JSObject result = new JSObject();
        result.put("ready", ready);
        call.resolve(result);
    }
}
''')
    patch('04-android-opt-in.patch','android/app/src/main/res/drawable/ic_stat_iald.xml',new='''<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFFFF" android:pathData="M4,3h16v13H9l-5,5zM8,7v2h8V7zM8,11v2h6v-2z" android:fillType="evenOdd" />
</vector>
''')
    (ROOT/'patch-manifest.json').write_text(json.dumps({'source':str(SOURCE),'files':records,
      'applied':False,'dependency_lock':'PENDING: resolve package-lock with authorized npm install; none run here'},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'patches':len(set(r['patch'] for r in records)),'files':len(records),'applied':False}))


if __name__=='__main__': main()
