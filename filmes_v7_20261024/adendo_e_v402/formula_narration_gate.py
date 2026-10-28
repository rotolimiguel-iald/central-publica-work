"""Read-only exact-plan approval gate for the formula revision; no synthesis on import/run."""
import json
from pathlib import Path
import rebind_audio_v402 as c
import audio_v402_revision as revision


def same_pin(actual, expected):
    revision.verify_pin(c,actual);revision.verify_pin(c,expected)
    assert Path(actual['path']).resolve()==Path(expected['path']).resolve()
    assert actual['sha256']==expected['sha256'] and actual['bytes']==expected['bytes']


def plan_context():
    preflight=c.check();data=revision.data_gate(c)
    path=c.C/'FORMULA_NARRATION_REVIEW.json';review=c.old.read(path)
    assert review['source']=='v402' and review['source_sha256']==data['source_sha256']
    for key in ('plan','templates','operator_order','corrections_order'):
        revision.verify_pin(c,review[key])
    plan=c.old.read(review['plan']['path']);builder=c.builder_module()
    assert plan['plan_sha256']==review['plan_sha256']
    assert plan['seal_pin']==data['source_sha256']
    with c.old.local_only():
        actual=builder.make_plan(c.V,c.V/'audio/script_templates.json')
    assert plan==actual,'FORMULA_EFFECTIVE_PLAN_CHANGED'
    baseline=c.old.read(c.C/'baseline_audio_v401/audio/NARRATION_PLAN_v401_final.json')
    previous=revision.units(builder,baseline);current=revision.units(builder,plan)
    assert set(current)=={u['key'] for u in review['units']}
    new=[u for u in review['units'] if u['key'] not in previous]
    assert len(new)==review['counts']['new_v402_units']
    assert len(current)-len(new)==review['counts']['reused_v401_units']
    return preflight,data,plan,review,new


def execution_gate():
    preflight,data,plan,review,new=plan_context()
    formula=c.old.read(c.C/'FORMULA_NARRATION_PARENT_REVIEW.json')
    audio=c.old.read(c.C/'PARENT_AUDIO_PLAN_REVIEW.json')
    expected={'plan':review['plan'],'templates':review['templates'],
              'formula_review':c.old.pin(c.C/'FORMULA_NARRATION_REVIEW.json'),
              'operator_order':review['operator_order'],'corrections_order':review['corrections_order']}
    for approval in (formula,audio):
        assert approval['status'].startswith('PASS')
        assert approval['source']=='v402' and approval['source_sha256']==data['source_sha256']
        assert approval['plan_sha256']==plan['plan_sha256']
        assert approval['actor']!=c.ACTOR,'REAL_DISTINCT_PARENT_REVIEW_REQUIRED'
    for key,pin in expected.items():same_pin(formula[key],pin)
    assert formula['formula_translation_checked'] is True and formula['adendo_d_checked'] is True
    same_pin(audio['plan_file'],review['plan'])
    same_pin(audio['templates'],review['templates'])
    same_pin(audio['formula_review'],expected['formula_review'])
    for key in ('new_v402_units','reused_v401_units','unique_units'):
        assert audio['counts'][key]==review['counts'][key]
    actual_new={u['key']:{k:u[k] for k in ('key','voice','language','text','text_sha256')} for u in new}
    approved_new={u['key']:{k:u[k] for k in ('key','voice','language','text','text_sha256')} for u in audio['new_units']}
    assert approved_new==actual_new,'PARENT_NEW_UNITS_MISMATCH'
    revision.seal_guard(c)
    return preflight,data,plan,review,new


if __name__=='__main__':
    _,data,plan,review,new=execution_gate()
    print(json.dumps({'status':'EXACT_FORMULA_PLAN_REVIEWED','source':data['source'],
        'plan_sha256':plan['plan_sha256'],'counts':review['counts'],'network_calls':0}))
