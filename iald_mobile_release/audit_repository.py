from pathlib import Path
import subprocess
import re

root=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app')
assert Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=root,text=True).strip()).resolve()==root.resolve()
files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=root).decode().split('\0')
files=sorted(set(filter(None,files)))
bad=[]
for name in files:
    p=root/name
    if re.search(r'(^|/)(node_modules|IOS_entregas_marco_2026|_backups_[^/]+)(/|$)|(^|/)(\.env[^/]*|keystore.properties|local.properties|HANDOFF[^/]*|GUIA_DISTRIBUICAO_APPSTORE.md)$|\.(jks|keystore|p12|p8|mobileprovision)$|\.bak_',name,re.I):
        bad.append(name+' (excluded file)'); continue
    if p.suffix.lower() in {'.png','.jpg','.jar'}: continue
    data=p.read_text(encoding='utf-8-sig',errors='replace')
    patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'\bAIza[0-9A-Za-z_-]{30,}',r'\bgh[pousr]_[0-9A-Za-z]{20,}',r'\bgithub_pat_[0-9A-Za-z_]{30,}']
    if any(re.search(pattern,data) for pattern in patterns): bad.append(name+' (credential-like content)')
if bad:
    print('\n'.join(bad)); raise SystemExit(1)
required=['ios/App/App.xcodeproj/project.pbxproj','ios/App/App/public/index.html','ios/App/App/capacitor.config.json','ios/App/ci_scripts/ci_post_clone.sh','ios/App/App.xcodeproj/xcshareddata/xcschemes/App.xcscheme']
assert all(n in files for n in required)
print(f'Audit passed: {len(files)} app files, no excluded paths or credential patterns; required iOS assets present.')
