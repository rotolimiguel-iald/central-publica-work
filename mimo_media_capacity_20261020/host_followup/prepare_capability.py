"""Stage audio capability fix separately from the diagnostic-only receipt."""
import ast,difflib,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent/'capability_R2';HERE.mkdir(exist_ok=True)
LIVE=Path('C:/IALD/projetos_pyhton/IALD')
baselines={}
def save(name,source):
    raw=(LIVE/name).read_bytes();baselines[name]=hashlib.sha256(raw).hexdigest()
    text=source.replace('\n','\r\n' if b'\r\n' in raw else '\n');ast.parse(text)
    (HERE/name).write_bytes(text.encode())
    (HERE/(name+'.patch')).write_text(''.join(difflib.unified_diff(raw.decode().splitlines(True),text.splitlines(True),fromfile='runtime/'+name,tofile='staging/'+name)),encoding='utf-8')
module=(LIVE/'new_private_media_host.py').read_text(encoding='utf-8')
old="""    if not durations:
        return {'standard': {'fps': 2., 'media_resolution': 'default'},
                'detail': {'fps': 2., 'media_resolution': 'max'}}"""
new="""    if not durations:
        # Audio has no FPS/resolution quality alternatives. The backend policy
        # shape stays canonical, but never invent a video choice for audio.
        return {'audio_full': {'fps': 2., 'media_resolution': 'default'}}"""
assert old in module;save('new_private_media_host.py',module.replace(old,new))
router=(LIVE/'iald_auto_router.py').read_text(encoding='utf-8')
old='    mod=backend()\n'
new="""    single_audio_policy=None
    if media_plans is not None and len(media_plans)==1 and media_counts['audio']>0 and not media_counts['video']:
        name,plan=next(iter(media_plans.items()))
        # Validate actual full-history plan items, not just client summary.
        if (plan.get('status')=='ESTIMADO' and plan.get('items')
                and len(plan['items'])==media_counts['audio']
                and all(item.get('kind')=='audio' for item in plan['items'])):
            single_audio_policy=name
    mod=backend()
"""
# Only the choose function receives this local. Do not alter other backend calls.
start=router.index('def choose(');head=router[:start];tail=router[start:]
assert old in tail;tail=tail.replace(old,new,1)
tail=tail.replace("    if media_plans is not None:questions['media_policy']=media_budget_policy.policy_question(media_plans)","    if media_plans is not None and single_audio_policy is None:questions['media_policy']=media_budget_policy.policy_question(media_plans)",1)
tail=tail.replace("            media_choice=media_budget_policy.resolve_policy(data['answers']['media_policy'],media_plans)","            media_choice=(single_audio_policy if single_audio_policy is not None else\n                          media_budget_policy.resolve_policy(data['answers']['media_policy'],media_plans))\n            record['media_policy_resolution']=('host_single_audio_no_quality_alternatives' if single_audio_policy is not None else 'jev_choice_confidence_validated')",1)
save('iald_auto_router.py',head+tail)
save('iald_web_server.py',(HERE.parent/'iald_web_server.py').read_text(encoding='utf-8'))
(HERE/'BASELINES.json').write_text(json.dumps(baselines,indent=2),encoding='utf-8')
