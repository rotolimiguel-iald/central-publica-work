"""Ship only the deadline removal; preserve parallel Selo work in app/ untouched."""
from pathlib import Path
from datetime import datetime
import subprocess,os,hashlib,json
M=Path(r'C:\IALD\projetos_pyhton\IALD\iald-app');W=Path(__file__).resolve().parent
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
raw=subprocess.check_output(['git','-C',str(M),'show','HEAD:www/iald.js'])
text=raw.decode('utf8').replace('\r\n','\n')
for line in ["import { renderDeadlines } from './operational_deadlines.js';\n",
             "  if (S.servidor.estado !== 'offline') verificarAlertas();\n",
             "  alertasMostrados: new Set(),     // 15/09/2026: bandeira do crédito da OpenAI, uma vez por nível na sessão\n"]:
    assert text.count(line)==1;text=text.replace(line,'')
start=text.index('// ALERTAS DO SERVIDOR (15/09/2026)')
start=text.rfind('// ═════════',0,start)
end=text.index('// ═════════',text.index('async function verificarAlertas()',start))
text=text[:start]+text[end:]
new=text.encode('utf8');p=M/'www/iald.js';old=p.read_bytes()
backup=M/('_backups_admin_only_isolated_'+stamp);backup.mkdir()
with (backup/'iald.js').open('xb')as f:f.write(old)
tmp=p.with_name('iald.js.tmp_'+stamp)
with tmp.open('xb')as f:f.write(new)
assert tmp.read_bytes()==new and p.read_bytes()==old;os.replace(tmp,p)
with (W/('admin_only_isolated_'+stamp+'.json')).open('x')as f:
    json.dump({'base':'HEAD:www/iald.js','mobile_sha256':hashlib.sha256(new).hexdigest(),
               'parallel_source':'app/iald.js Selo/export unchanged; not included in this hotfix'},f,indent=2)
print('Isolated mobile change prepared; parallel app source preserved.')
