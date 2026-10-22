from review_helpers import *

def main():
    previous=R/'revisao_implementador_modular/preservation_19_940.json'
    base=load(previous);checked=[];validate_pin_tree(base,checked)
    assert len(base['rows'])==940 and len(base['original_v351'])==19
    for row in base['rows']:
        q=V/row['relative']
        if q.exists():
            own=pin(q)
            assert (own['bytes'],own['sha256'])==(row['original']['bytes'],row['original']['sha256'])
            row['own_source']=own
    base.update(timestamp=now(),previous_independent_check=pin(previous),remeasured_for_delta=33,all_matched=True)
    save(OUT/'preservation_19_940.json',base)
    config=load(R/'delivery_configs/modular_cut_balance.json')
    documents=[];providers=[];dp=[]
    for name in config['docs']:
        jp=R/(name+'.json');mp=R/(name+'.md')
        jd=load(jp);validate_pin_tree(jd,dp)
        documents.append(dict(json=pin(jp),markdown=pin(mp),content=jd))
        for pr in jd.get('providers',[]):
            fp=Path(pr.get('source',pr)['path']);ls=fp.read_text(encoding='utf-8-sig').splitlines()
            row=dict(document=name,author=pin(fp))
            if 'line' in pr:
                stmt=pr.get('statement',pr.get('excerpt'));assert stmt
                actual='\n'.join(ls[pr['line']-1:pr['line']-1+len(stmt.splitlines())])
                assert re.sub(r'\s+',' ',actual).strip().startswith(re.sub(r'\s+',' ',stmt).strip()),pr
                row.update(line=pr['line'],statement=stmt,source_excerpt='\n'.join(ls[pr['line']-1:pr['line']+15]))
            q=V/fp.relative_to(K)
            row['own_source_available']=q.exists()
            if q.exists():
                assert q.read_bytes()==fp.read_bytes(),fp
                row['own']=pin(q)
            providers.append(row)
    save(OUT/'provider_checks.json',dict(documents=documents,providers=providers,pins=dp,entry_count=len(providers),all_pins_match=True,search_completeness_claimed=False))
    authorpath=R/'AUDITORIA_BALANCO_DOS_CORTES_A1B_TIPO_COMPLETO.json'
    author=load(authorpath);pins=[];validate_pin_tree(author,pins)
    original=load(Path(author['metadata_correction']['previous_audit']['path']))
    corrected=json.loads(json.dumps(author));corrected.pop('metadata_correction')
    for old,new in zip(original['targets'],corrected['targets']):
        assert new['statement'].startswith(old['statement'])
        new['statement']=old['statement']
    assert corrected==original
    assert not author['metadata_correction']['checks_rerun']
    source=Path(author['modules'][0]['source']['path']);ck(author['modules'][0]['source'])
    text=source.read_text(encoding='utf-8-sig');statement=author['targets'][0]['statement']
    assert text.splitlines()[author['targets'][0]['line']-1].startswith('theorem scalarTomitaResolvent_double_cut_balance')
    assert statement+' := by' in text
    rows=[]
    for row in author['commands']:
        stdout=Path(row['stdout']['path']).read_text(encoding='utf-8-sig')
        stderr=Path(row['stderr']['path']).read_text(encoding='utf-8-sig')
        rows.append(dict(**row,source_text=Path(row['source']['path']).read_text(encoding='utf-8-sig'),stdout_text=stdout,stderr_text=stderr))
        if row['label'].startswith('Bad'):
            assert row['returncode']==1 and 'type mismatch' in stdout.lower()
            assert not any(w in stdout.lower() for w in ['unknown identifier','unknown module','object file','timeout','unexpected token'])
        else:
            assert row['returncode']==0
            axioms=parse_axioms(stdout);assert len(axioms)==1 and all(set(v)<=ALLOWED for v in axioms.values())
    build=load(Path(author['positive_build']['path']));validate_pin_tree(build,pins)
    assert build['returncode']==0 and build['sources_unchanged_during_build'] and not build['dev_objects_used']
    save(OUT/'author_evidence_read.json',dict(audit=pin(authorpath),metadata=author,commands=rows,build=build,pins=pins,full_source_type_matches_corrected_metadata=True,only_statement_metadata_changed=True))
    history=[]
    for rp in sorted((R/'dev_double_cut_balance').glob('*/run.json')):
        j=load(rp);sp=pin(rp.parent/'V351ModularCutBalance.lean')
        assert (sp['bytes'],sp['sha256'])==(j['source']['bytes'],j['source']['sha256'])
        ck(j['stdout']);ck(j['stderr'])
        code=uncomment(Path(sp['path']).read_text(encoding='utf-8-sig'))
        history.append(dict(run=pin(rp),source=sp,historical_location=j['source']['path'],stdout=j['stdout'],stderr=j['stderr'],returncode=j['returncode'],used_as_own_build=False,whole_final_candidate=(sp['sha256']==author['modules'][0]['source']['sha256']),public_theorems=len(re.findall(r'^theorem\s+',code,re.M)),private_theorems=len(re.findall(r'^private theorem\s+',code,re.M)),heartbeat_limits=re.findall(r'set_option maxHeartbeats (\d+)',code),stdout_text=Path(j['stdout']['path']).read_text(encoding='utf-8-sig'),stderr_text=Path(j['stderr']['path']).read_text(encoding='utf-8-sig')))
    assert history[-1]['whole_final_candidate'] and history[-1]['returncode']==0
    save(OUT/'history_read.json',dict(rows=history,failed_count=sum(x['returncode']!=0 for x in history),partial_success_count=sum(x['returncode']==0 and not x['whole_final_candidate'] for x in history),failures_excluded=True,partial_successes_not_final_acceptance=True,historical_locations_not_active_pins=True))
    save(OUT/'inspection_summary.json',dict(timestamp=now(),baseline=pin(OUT/'preservation_19_940.json'),providers=pin(OUT/'provider_checks.json'),author=pin(OUT/'author_evidence_read.json'),history=pin(OUT/'history_read.json'),all_checks_passed=True))
    print(json.dumps(dict(providers=len(providers),baseline=940,original_subset=19,history_count=len(history),failed_history=sum(x['returncode']!=0 for x in history),partial_rc0=sum(x['returncode']==0 and not x['whole_final_candidate'] for x in history),metadata_correction_verified=True),ensure_ascii=False))

if __name__=='__main__':main()
