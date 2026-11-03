"""Cross-check the builder's v405 RUNTIME_BASELINE.json against the independent v404 baseline (taken 29/10) and the live files.
Read-only. Answers: did any runtime code file change between the v404 baseline (29/10) and the v405 baseline (02/11)?"""
import json,hashlib
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102');V4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
b5={b['path']:b['sha256'] for b in json.loads((W/'app/RUNTIME_BASELINE.json').read_bytes())['files']}
b4={b['path']:b['sha256'] for b in json.loads((V4/'app/RUNTIME_BASELINE.json').read_bytes())['files']}
print('v404 baseline files',len(b4),'| v405 baseline files',len(b5))
print('only in v404:',sorted(set(b4)-set(b5))[:5],'| only in v405:',sorted(set(b5)-set(b4))[:5])
diff=[Path(p).name for p in b5 if p in b4 and b5[p]!=b4[p]]
print('differ between baselines:',diff)
live=[Path(p).name for p in b5 if sha(p)!=b5[p]]
print('v405 baseline vs live now:',live)
live4=[Path(p).name for p in b4 if Path(p).is_file() and sha(p)!=b4[p]]
print('v404 baseline vs live now:',live4)
json.dump({'v404_files':len(b4),'v405_files':len(b5),'only_v404':sorted(set(b4)-set(b5)),'only_v405':sorted(set(b5)-set(b4)),'differ_between_baselines':diff,'v405_vs_live':live,'v404_vs_live':live4},open(r'C:\IALD\Central de Patentes\work\iald_v405_20261102\review\revisor_sonnet-app-v405-revisor-d\d1b_out.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
