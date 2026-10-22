from pathlib import Path
from datetime import datetime
import plistlib
import uuid

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
def write(rel,data):
    path=ROOT/rel
    path.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,str): data=data.encode()
    if path.exists():
        backup=ROOT/('_backups_'+stamp)/rel
        backup.parent.mkdir(parents=True,exist_ok=True)
        backup.write_bytes(path.read_bytes())
        assert backup.read_bytes()==path.read_bytes()
    tmp=path.with_suffix(path.suffix+'.tmp_release')
    tmp.write_bytes(data)
    assert tmp.stat().st_size==len(data)>0
    tmp.replace(path)

icon=(ROOT/'IOS_entregas_marco_2026/IALD_iOS_v2.1_final/Assets_para_arrastar/AppIcon.appiconset/appicon_1024.png').read_bytes()
write('ios/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png',icon)
privacy={'NSPrivacyTracking':False,'NSPrivacyAccessedAPITypes':[{
    'NSPrivacyAccessedAPIType':'NSPrivacyAccessedAPICategoryUserDefaults',
    'NSPrivacyAccessedAPITypeReasons':['CA92.1']}]}
write('ios/App/App/PrivacyInfo.xcprivacy',plistlib.dumps(privacy))
path=ROOT/'ios/App/App.xcodeproj/project.pbxproj'
project=path.read_text(encoding='utf-8')
ref=uuid.uuid4().hex[:24].upper()
build=uuid.uuid4().hex[:24].upper()
assert 'PrivacyInfo.xcprivacy' not in project
project=project.replace('/* Begin PBXBuildFile section */',f'/* Begin PBXBuildFile section */\n\t\t{build} /* PrivacyInfo.xcprivacy in Resources */ = {{isa = PBXBuildFile; fileRef = {ref} /* PrivacyInfo.xcprivacy */; }};')
project=project.replace('/* Begin PBXFileReference section */',f'/* Begin PBXFileReference section */\n\t\t{ref} /* PrivacyInfo.xcprivacy */ = {{isa = PBXFileReference; lastKnownFileType = text.xml; path = PrivacyInfo.xcprivacy; sourceTree = "<group>"; }};')
project=project.replace('\t\t\t\t504EC3131FED79650016851F /* Info.plist */,',f'\t\t\t\t504EC3131FED79650016851F /* Info.plist */,\n\t\t\t\t{ref} /* PrivacyInfo.xcprivacy */,')
project=project.replace('\t\t\t\t504EC30F1FED79650016851F /* Assets.xcassets in Resources */,',f'\t\t\t\t504EC30F1FED79650016851F /* Assets.xcassets in Resources */,\n\t\t\t\t{build} /* PrivacyInfo.xcprivacy in Resources */,')
assert project.count(build)==2 and project.count(ref)==3
write('ios/App/App.xcodeproj/project.pbxproj',project)
write('resources/icon-only.png',icon)
print('IALD original icon and required-reason privacy manifest included in iOS target.')
