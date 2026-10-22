from pathlib import Path
from datetime import datetime
import json
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
def write(path,data):
    if isinstance(data,str): data=data.encode()
    if path.exists() and path.read_bytes()==data: return
    if path.exists():
        backup=ROOT/('_backups_'+stamp)/path.relative_to(ROOT)
        backup.parent.mkdir(parents=True,exist_ok=True)
        backup.write_bytes(path.read_bytes())
        assert backup.read_bytes()==path.read_bytes()
    tmp=path.with_suffix(path.suffix+'.tmp_release')
    tmp.write_bytes(data)
    assert tmp.stat().st_size==len(data)>0
    tmp.replace(path)
icon=(ROOT/'resources/icon-only.png').read_bytes()
res=ROOT/'android/app/src/main/res'
for path in res.glob('mipmap-*/ic_launcher.png'):
    if path.parent.name=='mipmap-anydpi-v26': continue
    write(path.with_name('ic_launcher_foreground.png'),path.read_bytes())
for path in res.glob('drawable*/splash.png'): write(path,icon)
for path in (ROOT/'ios/App/App/Assets.xcassets/Splash.imageset').glob('*.png'): write(path,icon)
write(res/'values/ic_launcher_background.xml','<?xml version="1.0" encoding="utf-8"?>\n<resources><color name="ic_launcher_background">#090b10</color></resources>\n')
styles=res/'values/styles.xml'
write(styles,styles.read_text().replace('<item name="android:background">@drawable/splash</item>', '''<item name="windowSplashScreenBackground">#090b10</item>
        <item name="windowSplashScreenAnimatedIcon">@mipmap/ic_launcher</item>
        <item name="postSplashScreenTheme">@style/AppTheme.NoActionBar</item>'''))
story=ROOT/'ios/App/App/Base.lproj/LaunchScreen.storyboard'
write(story,story.read_text().replace('contentMode="scaleAspectFill"','contentMode="scaleAspectFit"').replace('<color white="1" alpha="1"','<color white="0" alpha="1"'))
config=json.loads((ROOT/'capacitor.config.json').read_text())
config['plugins']['SplashScreen'].update(launchShowDuration=500,backgroundColor='#090b10',androidScaleType='FIT_CENTER')
write(ROOT/'capacitor.config.json',json.dumps(config,indent=2)+'\n')
print('Original IALD assets now cover adaptive icons and launch screens.')
