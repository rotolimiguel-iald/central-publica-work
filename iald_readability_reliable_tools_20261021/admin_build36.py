"""Only the two TestFlight admin subtrees; preserve all other bytes exactly."""
from task import W,new,check
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,os
check('deploy')
source=W/'IOS_DISTRIBUTION.json';ios=json.loads(source.read_bytes())
assert ios['internal']['status']==ios['external']['status']=='Em testes'
p=Path(r'C:\IALD\projetos_pyhton\IALD\iald_deadlines.json');before=p.read_bytes();text=before.decode('utf-8');now=datetime.now(timezone.utc).isoformat();ranges=[]
for key,group,count in [('testflight_internal','IALD Equipe',1),('testflight_external','IALD Piloto',6)]:
    match=re.search(r'"'+key+r'"\s*:\s*',text);assert match
    start=match.end();item,length=json.JSONDecoder().raw_decode(text[start:]);end=start+length
    item.update(label='IALD 4.1 (36) — '+group,build='4.1 (36)',status='Em testes',observed_utc=now,source='App Store Connect observado em '+now+': Em testes; data/hora exatas de expiração não expostas e não inferidas.',source_reference=dict(path=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),bytes=source.stat().st_size),testers=count)
    assert item['expires_at'] is None
    line=text[text.rfind('\n',0,start)+1:start];indent=re.match(r'\s*',line).group();nl='\r\n' if b'\r\n' in before else '\n'
    lines=json.dumps(item,ensure_ascii=False,indent=2).splitlines();value=nl.join([lines[0],*[indent+x for x in lines[1:]]]);ranges.append((start,end,value))
aftertext=text
for start,end,value in sorted(ranges,reverse=True):aftertext=aftertext[:start]+value+aftertext[end:]
after=aftertext.encode('utf-8');a=json.loads(after);b=json.loads(before)
for k in ['testflight_internal','testflight_external']:a['items'][k]=b['items'][k]
assert a==b
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f');bak=p.with_name(p.name+'.bak_'+stamp);bak.open('xb').write(before);assert bak.read_bytes()==before
tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.open('xb').write(after);assert tmp.read_bytes()==after and p.read_bytes()==before;os.replace(tmp,p);assert p.read_bytes()==after
new('ADMIN_BUILD36_UPDATED.json',dict(status='PASS_TWO_ADMIN_SUBTREES_ONLY',backup=str(bak),before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),other_semantics_preserved=True,no_chat_alert=True,no_restart=True))
