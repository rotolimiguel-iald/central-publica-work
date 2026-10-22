from finish_delta import *
out=Path(__file__).resolve().parent;rows=[]
for p in sorted((R/'dev_right_action_algebra').glob('*/run.json')):
 j=load(p);r=dict(run=pin(p),returncode=j['returncode'],streams=[])
 for k in ['stdout','stderr']:
  ck(j[k]);r['streams'].append(j[k])
  if k=='stdout':r['stdout_text']=Path(j[k]['path']).read_text(encoding='utf8')
 rows.append(r)
save(out/'history_read.json',dict(rows=rows,only_final_rc0_accepted=True,old_sources_not_equated_with_final_pin=True))
print(json.dumps([dict(path=x['run']['path'],rc=x['returncode'],errors=[l for l in x['stdout_text'].splitlines() if 'error' in l or 'warning' in l][:8]) for x in rows],ensure_ascii=False))
