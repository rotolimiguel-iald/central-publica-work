from pathlib import Path
import ast, collections, hashlib, importlib.util, json, sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;W=R.parent;S=W/'science';ST=S/'memory_stage'
pins=json.loads((R/'inputpins.json').read_bytes())
def read(p):
    p=Path(p);b=p.read_bytes();key=str(p.resolve())
    if key in pins:assert hashlib.sha256(b).hexdigest()==pins[key]['sha256'],key
    return b
source=json.loads(read(S/'verified_sources/um_absoluto.json'))
spec=importlib.util.spec_from_file_location('codec',R/'capture_haiku_codec.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
tree=ast.parse(read(R/'capture_build_release.py'));ns={'codec':c,'json':json}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='read_topics'],type_ignores=[]),'reader','exec'),ns)
topics=ns['read_topics'](read(ST/'TGL_CLUSTER_v392.md').decode())
details=json.loads(read(R/'test_details.json'));prepared=json.loads(read(ST/'prepared.json'))
checks=[]
def check(name,condition,details=None):
    checks.append({'name':name,'pass':bool(condition),'details':details})
h3=source['core']['lei_de_campo_curvo_v392'];h3project=topics['lei_de_campo_curvo_v392']
f81=source['core']['f81_nao_fechada_v392'];f81project=topics['f81_nao_fechada_v392']
check('H3_conditional_claim_literal',h3['diz'][0]==h3project['diz'][0] and 'CONDICIONAL' in h3project['diz'][0] and 'hH3' in h3project['diz'][0])
check('H3_limits_and_no_claims_literal',h3project['nao_diz']==h3['nao_diz'] and h3project['limites']==h3['limites'])
lean=read(ST/'kernel/TGLExt/LiganteLeiCampoCurvo.lean').decode()
check('H3_named_premise_in_pinned_source','(hH3 :' in lean and 'NamedAtlasH3 ((4 * G)⁻¹) U R screens)' in lean and 'have harea := hH3 hpost' in lean,'Source checked, not recompilation')
check('F81_not_closed_verdict',f81project['verdict']==f81['verdict'] and 'NOT_CLOSED' in f81project['verdict'] and 'STAYS_PROPOSAL' in f81project['verdict'])
check('F81_explicit_no_recalculation',f81project['nao_diz']==f81['nao_diz'] and f81project['diz']==f81['diz'])
check('F81_proposal_status_retained',f81project['extras']['fields']['/f81/status']=='PROPOSTA' and f81['extras']['fecha_a_f81'] is False)
new_missing=[x for x in details['fields_not_inline'] if x['topic'] in prepared['added_topics']]
check('new_32_topics_all_protected_math_represented',not new_missing,{'new_topics':len(prepared['added_topics']),'missing':new_missing})
check('H3_46_fields_all_represented',next(x for x in details['topics'] if x['topic']=='lei_de_campo_curvo_v392')['not_inline']==0)
adapt=json.loads(read(S/'builder_adaptation.json'));old=Path(adapt['source']);raw=read(old)
check('old_builder_pin',hashlib.sha256(raw).hexdigest()==adapt['source_sha256'])
for name in ('haiku_codec.py','fit_transport.py','fit_memory.py'):
    check('reused_builder_'+name,read(old.parent/name)==read(S/'memory_build'/name))
missing=details['fields_not_inline']
counter=collections.Counter(prepared['topic_modes'][x['topic']] for x in missing)
result={'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),
    'legacy_reference_scope':{'not_inline_total':len(missing),'by_topic_mode':dict(counter),
    'kernel_formalization':sum(x['topic']=='kernel_formalization' for x in missing),
    'interpretation':'Recoverable exactly from pinned JSON. Not a claim that every protected or mathematical field is literal in the prompt. No missing protected/math field in any of the 32 added topics.'},
    'additional_inputs':[{'path':str(p.resolve()),'sha256':hashlib.sha256(read(p)).hexdigest(),'bytes':len(read(p))} for p in [old,*[old.parent/n for n in ('haiku_codec.py','fit_transport.py','fit_memory.py')]]]}
out=R/'semantic_tests.json';assert not out.exists();out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
