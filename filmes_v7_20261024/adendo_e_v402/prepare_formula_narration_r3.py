"""R3: focused corrections FN402-01/02, preserving every other cue; strictly offline."""
from pathlib import Path
import copy, hashlib, json, os, sys, time
import rebind_audio_v402 as c
import audio_v402_revision as revision
import formula_narration_gate as gate
from prepare_formula_narration_r2 import caption_chunks, LANGS


def replace_bytes(path, raw, backups):
    path=Path(path)
    if path.exists():
        old=path.read_bytes()
        if old==raw:return
        backup=path.with_name(path.name+'.bak_formula_r3_'+str(time.time_ns()))
        with backup.open('xb') as stream:stream.write(old);stream.flush();os.fsync(stream.fileno())
        assert backup.read_bytes()==old
        backups.append({'original_before':c.old.pin(path),'backup':c.old.pin(backup)})
    tmp=path.with_name(path.name+'.tmp_'+str(time.time_ns()))
    with tmp.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    assert tmp.read_bytes()==raw
    os.replace(tmp,path)
    assert path.read_bytes()==raw


def encoded(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()


def main():
    preflight,data,old_plan,old_review,_=gate.plan_context()
    assert old_review['templates']['sha256']==c.old.digest(c.C/'AUDIO_SCRIPT_TEMPLATES_V402_FORMULA_R2.json')
    guard=revision.seal_guard(c);builder=c.builder_module();backups=[]
    old_template=c.old.read(c.C/'AUDIO_SCRIPT_TEMPLATES_V402_FORMULA_R2.json');template=copy.deepcopy(old_template)
    old_report_pin=c.old.pin(c.C/'FORMULA_NARRATION_REVIEW.json')
    edits=[]
    def change(film,key,strings,reason):
        segment=next(s for s in template['films'][film]['segments'] if s['key']==key)
        for lang,text in zip(LANGS,strings):
            before=segment['text'][lang][0];assert before!=text
            segment['text'][lang][0]=text
            edits.append({'film':film,'segment':key,'cue_index':0,'language':lang,
                          'old':before,'new':text,'reason':reason})
    independent=c.old.read(c.C/'FORMULA_NARRATION_INDEPENDENT_REVIEW.json')
    assert independent['reviewed_revision']=='R2' and independent['plan_sha256']==old_plan['plan_sha256']
    for pin in (independent['pins']['formula_review'],independent['pins']['plan'],independent['pins']['templates']):revision.verify_pin(c,pin)
    # Two Chinese-only corrections; the two other occurrences are corrected with H1 below.
    for film,key,index in [('film1','face',1),('film2','sheet',0)]:
        segment=next(x for x in template['films'][film]['segments'] if x['key']==key)
        before=segment['text']['zh-Hans'][index];assert before.count('局部能隙')==1
        after=before.replace('局部能隙','局部谱隙');segment['text']['zh-Hans'][index]=after
        edits.append({'film':film,'segment':key,'cue_index':index,'language':'zh-Hans','old':before,'new':after,
                      'reason':'FN402-01: usar gap espectral local, sem acrescentar interpretação energética.'})
    change('film1','horizon',(
        'In the Pentad, assume finite trace of the kernel projection and a local spectral gap; the coframe organizes Lorentz directions; Clausius links heat and horizon area.',
        'Na Pêntada, supomos traço finito da projeção sobre o núcleo e gap espectral local; o coframe organiza direções de Lorentz; Clausius liga calor e área no horizonte.',
        'Dans la Pentade, nous supposons une trace finie de la projection sur le noyau et un gap spectral local ; le corepère organise les directions de Lorentz ; Clausius relie chaleur et aire de l’horizon.',
        '在五元组中，假设核投影的迹有限，并存在局部谱隙；余标架组织洛伦兹方向；克劳修斯关系连接视界的热量与面积。'),
        'FN402-02: a finitude do traço pertence à projeção sobre o núcleo; não à álgebra inteira. Preservar gap espectral local, coframe/Lorentz e horizonte-Clausius. FN402-01 também corrigido no chinês.')
    change('film2','einstein',(
        'The first hypothesis requires finite trace of the kernel projection and a local spectral gap; the second, coframe and Lorentz geometry; the third links horizon heat and area through Clausius. Together they form the Pentad.',
        'A primeira hipótese exige traço finito da projeção sobre o núcleo e gap espectral local; a segunda, coframe e geometria de Lorentz; a terceira liga calor e área no horizonte por Clausius. Juntas, compõem a Pêntada.',
        'La première hypothèse exige une trace finie de la projection sur le noyau et un gap spectral local ; la deuxième, corepère et géométrie de Lorentz ; la troisième relie chaleur et aire à l’horizon par Clausius. Ensemble, elles forment la Pentade.',
        '第一项假设要求核投影的迹有限，并存在局部谱隙；第二项要求余标架与洛伦兹几何；第三项通过克劳修斯关系连接视界的热量与面积。它们共同构成五元组。'),
        'FN402-02: qualificar o objeto do traço na primeira hipótese; as outras conservam seus papéis. FN402-01: localidade espectral no chinês; redundâncias reduzidas para manter a janela sem acelerar.')
    assert len(edits)==10
    assert sum(x["old"].count("局部能隙") for x in edits)==4
    assert "局部能隙" not in json.dumps(template,ensure_ascii=False)
    assert json.dumps(template,ensure_ascii=False).count("局部谱隙")==4
    template['revision']='V402_FORMULA_R3_KERNEL_PROJECTION_TRACE_AND_SPECTRAL_GAP'
    builder.validate_templates(template)
    versioned_template=c.C/'AUDIO_SCRIPT_TEMPLATES_V402_FORMULA_R3.json'
    assert not versioned_template.exists(),'R3_ALREADY_EXISTS_DO_NOT_REPLACE'
    c.old.write_new(versioned_template,template)
    with c.old.local_only():plan=builder.make_plan(c.V,versioned_template)
    for film,content in plan['films'].items():
        assert content['total_seconds']==old_plan['films'][film]['total_seconds']
        for seg,prior in zip(content['segments'],old_plan['films'][film]['segments']):
            for key in set(seg)-{'cues','speech_budget'}:assert seg[key]==prior[key],(film,seg['key'],key)
            for index,(cue,oldcue) in enumerate(zip(seg['cues'],prior['cues'])):
                if cue!=oldcue:
                    assert (film,seg['key'],index) in {('film1','face',1),('film2','sheet',0),('film1','horizon',0),('film2','einstein',0)}
                    for lang in LANGS:
                        assert __import__('re').findall(r'[-+]?\d+(?:[.,]\d+)?',cue[lang])==__import__('re').findall(r'[-+]?\d+(?:[.,]\d+)?',oldcue[lang])
    versioned_plan=c.C/'AUDIO_PLAN_V402_FORMULA_R3.json';c.old.write_new(versioned_plan,plan)
    public_template=c.V/'audio/script_templates.json';final_plan=c.V/'audio/NARRATION_PLAN_v402_formula_final.json'
    replace_bytes(public_template,versioned_template.read_bytes(),backups)
    replace_bytes(final_plan,versioned_plan.read_bytes(),backups)
    assert builder.make_plan(c.V,public_template)==plan
    previous=revision.units(builder,c.old.read(c.C/'baseline_audio_v401/audio/NARRATION_PLAN_v401_final.json'))
    units=revision.units(builder,plan)
    for key,unit in units.items():
        hit=builder.completed_cached_audio(builder.io_path(c.V/'audio/cache'),key)
        unit['unchanged_from_v401']=key in previous
        unit['completed_cache']=None if hit is None else {'audio':c.old.pin(hit),'receipt':c.old.pin(hit.with_suffix('.json'))}
        if key in previous:assert hit is not None
    report=copy.deepcopy(old_review);rows=[];captions=[];budgets=[]
    edit_index={(x['film'],x['segment'],x['cue_index']):x for x in edits}
    old_rows={(r['film'],r['segment'],r['cue_index']):r for r in old_review['all_cues_reviewed']}
    deltas=[]
    for film,content in plan['films'].items():
        for segment in content['segments']:
            budgets.append({'film':film,'segment':segment['key'],'start':segment['start'],'end':segment['end'],'budget':segment['speech_budget']})
            for index,cue in enumerate(segment['cues']):
                key=(film,segment['key'],index);row=copy.deepcopy(old_rows[key])
                row['new']={lang:cue[lang] for lang in ('pt-BR','en')};row['translations']=cue;row['segment_budget']=segment['speech_budget']
                if key in edit_index:
                    row['changed_by_formula_revision']=True;row['reason']=edit_index[key]['reason']
                    row['anchors']=['core.local_breuer_gap','kernel projection trace: 0 < tau(ker) < infinity','baseline.hypothesis_contract','core.triad_master']
                    oldseg=next(s for s in old_plan['films'][film]['segments'] if s['key']==segment['key'])
                    deltas.append({'film':film,'segment':segment['key'],'cue_index':index,
                        'old':oldseg['cues'][index],'new':cue,'reason':row['reason'],'segment_budget':segment['speech_budget']})
                rows.append(row);captions.append({'film':film,'segment':segment['key'],'cue_index':index,
                    'reading_chunks':{lang:caption_chunks(text,lang) for lang,text in cue.items()}})
    report.update({'revision':'R3','status':'CANDIDATE_AWAITING_PARENT_TEXT_REVIEW_NO_TTS',
        'preflight':preflight,'plan_sha256':plan['plan_sha256'],'plan':c.old.pin(final_plan),'candidate_plan':c.old.pin(versioned_plan),
        'templates':c.old.pin(public_template),'versioned_templates':c.old.pin(versioned_template),
        'previous_formula_revision':{'review':old_report_pin,'plan':c.old.pin(c.C/'AUDIO_PLAN_V402_FORMULA_R2.json'),
                                     'templates':c.old.pin(c.C/'AUDIO_SCRIPT_TEMPLATES_V402_FORMULA_R2.json')},
        'all_cues_reviewed':rows,'affected_cues':[r for r in rows if r['changed_by_formula_revision']],
        'template_changes':old_review['template_changes']+edits,'r3_deltas_only':deltas,'units':list(units.values()),'timing_budget':budgets,
        'independent_r2_review_preserved':c.old.pin(c.C/'FORMULA_NARRATION_INDEPENDENT_REVIEW.json'),
        'focused_finding_responses':[{'id':i,'status':'CORRECTED_BY_BUILDER_PENDING_FOCUSED_REVIEW'} for i in ('FN402-01','FN402-02')],
        'timing_warnings':[{'film':b['film'],'segment':b['segment'],'language':lang,**v} for b in budgets for lang,v in b['budget'].items() if v['may_need_extension']],
        'counts':{'unique_units':len(units),'cue_occurrences':sum(len(u['occurrences']) for u in units.values()),
                  'new_v402_units':sum(not u['unchanged_from_v401'] for u in units.values()),
                  'reused_v401_units':sum(u['unchanged_from_v401'] for u in units.values()),
                  'new_units_missing_audio':sum(u['completed_cache'] is None for u in units.values()),
                  'reviewed_cue_pairs':len(rows),'affected_cue_pairs':sum(r['changed_by_formula_revision'] for r in rows),
                  'changed_strings_four_languages':sum(r['changed_by_formula_revision'] for r in rows)*len(LANGS)},
        'r3_changed_cue_pairs':len(deltas),'r3_changed_strings_four_languages':len(edits),
        'actual_timing_after_go':'Measure received speech and refuse overlap/overrun before mix mutation; no speed-up, shortening or time compression.',
        'listening_previews_after_go':{'status':'PENDING_APPROVED_SYNTHESIS_AND_MEASURED_MIXES','source':'new film1 normalized WAV mixes',
            'segments':['boundary','mirror'],'range_seconds':[24,72],'duration_seconds':48,
            'outputs':[str(c.C/'preview_formula_pt.wav'),str(c.C/'preview_formula_en.wav')],
            'method':'Local PCM sample slicing only; no TTS, resampling, extra normalization or original-duration change.'}})
    assert not report['timing_warnings']
    # Preserve D cue content and all formula labels by comparison, without writing cinema/data.
    for film,key,idx in [('film1','return',0),('film2','einstein',1),('film1','nature',0),('film2','identity',0)]:
        assert next(s for s in plan['films'][film]['segments'] if s['key']==key)['cues'][idx]==next(s for s in old_plan['films'][film]['segments'] if s['key']==key)['cues'][idx]
    revision.seal_guard(c)
    replace_bytes(c.C/'FORMULA_NARRATION_REVIEW.json',encoded(report),backups)
    replace_bytes(c.C/'FORMULA_SUBTITLE_READING_PREVIEW.json',encoded({'status':'UNTIMED_READING_PREVIEW','plan_sha256':plan['plan_sha256'],'items':captions}),backups)
    formula_expected={'source':'v402','source_sha256':report['source_sha256'],'plan_sha256':plan['plan_sha256'],
        **{k:report[k] for k in ('plan','templates','operator_order','corrections_order')},
        'formula_review':c.old.pin(c.C/'FORMULA_NARRATION_REVIEW.json'),'formula_translation_checked':True,'adendo_d_checked':True}
    new=[u for u in units.values() if not u['unchanged_from_v401']]
    audio_expected={'schema':'iald.audio-v402-parent-plan-review/v1','source':'v402','source_sha256':report['source_sha256'],
        'plan_sha256':plan['plan_sha256'],'plan_file':report['plan'],'templates':report['templates'],
        'formula_review':formula_expected['formula_review'],
        'counts':{k:report['counts'][k] for k in ('unique_units','new_v402_units','reused_v401_units')},
        'new_units':[{k:u[k] for k in ('key','voice','language','text','text_sha256')} for u in new]}
    contract={'status':'APPROVAL_CONTRACT_ONLY_NOT_APPROVAL','revision':'R3','actor':c.ACTOR,'gate':c.old.pin(c.C/'formula_narration_gate.py'),
        'required_approval_files':{name:{'required_fields':values,'additional_requirements':['status starts with PASS','actor is actual distinct reviewer']} for name,values in [('FORMULA_NARRATION_PARENT_REVIEW.json',formula_expected),('PARENT_AUDIO_PLAN_REVIEW.json',audio_expected)]},
        'human_consent':'Original human Edge permissions remain separate; these files approve exact content and engineering only.',
        'previous_plan_transport_held':True,'no_tts_dispatched':True}
    replace_bytes(c.C/'FORMULA_NARRATION_APPROVAL_CONTRACT.json',encoded(contract),backups)
    lines=['V402 FORMULA R3 — revisão completa EN/PT; estimativas, sem audição/TTS.','Plan SHA256: '+plan['plan_sha256'],'']
    for row in rows:
        lines.append(f"{row['film']} / {row['segment']} / fala {row['cue_index']+1}")
        for lang in ('pt-BR','en'):lines.append(lang+': '+row['new'][lang])
        lines.extend(['Motivo: '+row['reason'],'Orçamento capítulo: '+json.dumps(row['segment_budget'],ensure_ascii=False),''])
    replace_bytes(c.C/'FORMULA_NARRATION_PT_EN.txt',('\n'.join(lines)+'\n').encode(),backups)
    delta_receipt={'status':'R3_DELTAS_READY_PARENT_REVIEW_NO_TTS','actor':c.ACTOR,'source':'v402','source_sha256':report['source_sha256'],
        'preflight':preflight,'plan_sha256':plan['plan_sha256'],'review':c.old.pin(c.C/'FORMULA_NARRATION_REVIEW.json'),
        'plan':c.old.pin(final_plan),'templates':c.old.pin(public_template),'contract':c.old.pin(c.C/'FORMULA_NARRATION_APPROVAL_CONTRACT.json'),
        'deltas':deltas,'counts':report['counts'],'backups':backups,'scheduled_seconds':report['durations_unchanged'],
        'tts_sent':0,'inflight':0,'actual_timing_measured':False,'speedup':False,'previews_after_go':report['listening_previews_after_go']}
    c.old.write_new(c.C/'FORMULA_NARRATION_R3_DELTA.json',delta_receipt)
    gate.plan_context()
    print(json.dumps({k:delta_receipt[k] for k in ('status','plan_sha256','counts','review','plan','templates','contract')},ensure_ascii=False))

if __name__=='__main__':main()
