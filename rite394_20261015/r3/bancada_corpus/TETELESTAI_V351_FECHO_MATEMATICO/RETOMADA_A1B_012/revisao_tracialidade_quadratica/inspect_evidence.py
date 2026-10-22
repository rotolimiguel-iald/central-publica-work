from review_helpers import *

def main():
 previous=R/'revisao_balanco_dos_cortes/preservation_19_940.json'
 base=load(previous);checked=[];validate_pin_tree(base,checked)
 assert len(base['rows'])==940 and len(base['original_v351'])==19
 for row in base['rows']:
  p=V/row['relative']
  if p.exists():
   q=pin(p);assert (q['bytes'],q['sha256'])==(row['original']['bytes'],row['original']['sha256']);row['own_source']=q
 base.update(timestamp=now(),previous_independent_check=pin(previous),remeasured_for_delta=34,all_matched=True)
 save(OUT/'preservation_19_940.json',base)
 cfg=load(R/'delivery_configs/quadratic_trace.json');docs=[];providers=[];pins=[]
 for name in cfg['docs']:
  jp=R/(name+'.json');mp=R/(name+'.md');j=load(jp);validate_pin_tree(j,pins)
  docs.append(dict(json=pin(jp),markdown=pin(mp),content=j))
  for pr in j.get('providers',[]):
   fp=Path(pr['source']['path']);ls=fp.read_text(encoding='utf-8-sig').splitlines();stmt=pr['statement']
   actual='\n'.join(ls[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
   assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr
   q=V/fp.relative_to(K);assert q.read_bytes()==fp.read_bytes()
   providers.append(dict(document=name,name=pr['name'],author=pin(fp),own=pin(q),line=pr['line'],statement=stmt,source_excerpt='\n'.join(ls[pr['line']-1:pr['line']+18])))
 save(OUT/'provider_checks.json',dict(documents=docs,providers=providers,pins=pins,entry_count=len(providers),all_pins_match=True,search_completeness_claimed=False))
 ap=R/'AUDITORIA_TRACIALIDADE_QUADRATICA_A1B.json';author=load(ap);pp=[];validate_pin_tree(author,pp)
 assert author['all_axioms_allowed'] and author['negative_controls_rejected'] and author['full_trace_constructed'] and author['core_traciality_proved']
 for target in author['targets']:
  st=Path(target['source']['path']).read_text(encoding='utf-8-sig')
  assert st.splitlines()[target['line']-1].startswith(target['statement'].splitlines()[0]);assert target['statement'] in st
 rows=[]
 for row in author['commands']:
  so=Path(row['stdout']['path']).read_text(encoding='utf-8-sig');se=Path(row['stderr']['path']).read_text(encoding='utf-8-sig')
  rows.append(dict(**row,source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),stdout_text=so,stderr_text=se))
  if row['label'].startswith('Bad'):
   assert row['returncode']==1 and 'type mismatch' in so.lower()
   assert not any(w in so.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
  else:
   aa=parse_axioms(so);assert row['returncode']==0 and len(aa)==2 and all(set(x)<=ALLOWED for x in aa.values())
 build=load(Path(author['positive_build']['path']));validate_pin_tree(build,pp)
 assert build['returncode']==0 and build['sources_unchanged_during_build'] and not build['dev_objects_used']
 bst=Path(build['stdout']['path']).read_text(encoding='utf-8-sig');bse=Path(build['stderr']['path']).read_text(encoding='utf-8-sig')
 bax=parse_axioms(re.sub(r'^info: [^\n]*?\.lean:\d+:\d+:\s*','',bst,flags=re.M))
 assert bax and all(set(x)<=ALLOWED for x in bax.values());assert not re.search(r'^error:',bst,re.M)
 complete=R/'quadratic_trace_validation/20260915_032117_800118/complete.json'
 save(OUT/'author_evidence_read.json',dict(audit=pin(ap),metadata=author,commands=rows,build=build,build_stdout_text=bst,build_stderr_text=bse,build_axioms=bax,complete=pin(complete),complete_content=load(complete),pins=pp))
 history=[]
 for folder in sorted((R/'dev_quadratic_trace').iterdir()):
  if not folder.is_dir():continue
  rp=folder/'run.json';sp=folder/'V351QuadraticTrace.lean'
  if not sp.exists():continue
  row=dict(source=pin(sp),run_available=rp.exists(),used_as_own_build=False)
  code=uncomment(sp.read_text(encoding='utf-8-sig'))
  row.update(public_theorems=len(re.findall(r'^theorem\s+',code,re.M)),private_theorems=len(re.findall(r'^private theorem\s+',code,re.M)),heartbeat_limits=re.findall(r'set_option maxHeartbeats (\d+)',code),whole_final_candidate=pin(sp)['sha256']==author['modules'][0]['source']['sha256'])
  if rp.exists():
   j=load(rp);assert (row['source']['bytes'],row['source']['sha256'])==(j['source']['bytes'],j['source']['sha256'])
   ck(j['stdout']);ck(j['stderr'])
   row.update(run=pin(rp),historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],stdout_text=Path(j['stdout']['path']).read_text(encoding='utf-8-sig'),stderr_text=Path(j['stderr']['path']).read_text(encoding='utf-8-sig'))
  else:row.update(returncode=None,scope='snapshot without final run.json, never accepted')
  history.append(row)
 assert any(x['whole_final_candidate'] and x['returncode']==0 for x in history)
 save(OUT/'history_read.json',dict(rows=history,failed_count=sum(x['returncode'] not in [None,0] for x in history),partial_success_count=sum(x['returncode']==0 and not x['whole_final_candidate'] for x in history),missing_run_count=sum(x['returncode'] is None for x in history),final_success_count=sum(x['returncode']==0 and x['whole_final_candidate'] for x in history),failures_excluded=True,partial_successes_not_final_acceptance=True,historical_locations_not_active_pins=True))
 save(OUT/'inspection_summary.json',dict(timestamp=now(),baseline=pin(OUT/'preservation_19_940.json'),providers=pin(OUT/'provider_checks.json'),author=pin(OUT/'author_evidence_read.json'),history=pin(OUT/'history_read.json'),all_checks_passed=True))
 print(json.dumps(dict(providers=len(providers),baseline=940,original_subset=19,history_count=len(history),failed_history=sum(x['returncode'] not in [None,0] for x in history),partial_rc0=sum(x['returncode']==0 and not x['whole_final_candidate'] for x in history),missing_run=sum(x['returncode'] is None for x in history)),ensure_ascii=False))
if __name__=='__main__':main()
