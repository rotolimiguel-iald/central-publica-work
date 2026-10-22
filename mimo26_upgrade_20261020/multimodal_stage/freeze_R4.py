"""Freeze with supplementary metrics delta; do not rewrite existing pins."""
import ast
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import types
import unicodedata

p=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=json.loads((p/'MANIFEST_R4_FINAL.json').read_text(encoding='utf-8'))
assert all(sha(p/name)==pin for name,pin in manifest['files'].items())
source=p/'iald_app_providers.py'
s=source.read_text(encoding='utf-8')
n=s.replace('import iald_app_memory as app_memory','import iald_app_memory as app_memory\nimport iald_routing_metrics as routing_metrics',1)
old="metrics_source='existing_app_sse', task=metric_task(messages) if messages is not None else 'unknown')"
assert n.count(old)==1
n=n.replace(old,"metrics_source='existing_app_sse')\n        routing_metrics.stamp(record, messages)",1)
old="streaming=provider != 'kimi', calls=[], first_text_seconds=None, task=metric_task(messages))"
assert n.count(old)==1
n=n.replace(old,"streaming=provider != 'kimi', calls=[], first_text_seconds=None)\n        routing_metrics.stamp(record, messages)",1)
node=next(x for x in ast.parse(n).body if isinstance(x,ast.FunctionDef) and x.name=='metric_task')
lines=n.splitlines(True);n=''.join(lines[:node.lineno-1]+lines[node.end_lineno:])
compile(n,'unified-metrics','exec')
assert n.count('routing_metrics.stamp(record, messages)')==2
assert 'metric_task(' not in n
(p/'metrics_hooks_R4.patch').write_text(''.join(difflib.unified_diff(s.splitlines(True),n.splitlines(True),fromfile='a/iald_app_providers.py',tofile='b/iald_app_providers.py')),encoding='utf-8')
# Final derived provider combines both independent deltas without changing R3.
needle='        "A moderação das mensagens continua usando a OpenAI. "'
replacement='''        + ("Os anexos de imagem, áudio e vídeo são enviados somente à Xiaomi MiMo. "
           "Os PDFs são enviados como texto extraído, sem o arquivo PDF original. "
           "Os bytes dos anexos não são enviados ao TypeSafe nem à OpenAI. "
           "A moderação textual continua usando a OpenAI. " if provider == 'mimo' else
           "A moderação das mensagens continua usando a OpenAI. ")'''
assert n.count(needle)==1
n=n.replace(needle,replacement,1)
compile(n,'final-derived-provider','exec')
(p/'iald_app_providers_R4_final.py').write_text(n,encoding='utf-8')

# Exercise actual routing metrics and actual pure classifier, without app imports.
policy_source=Path('C:/IALD/projetos_pyhton/IALD/iald_task_policy.py')
policy=types.ModuleType('iald_task_policy');policy.__dict__.update(re=re,unicodedata=unicodedata)
function=next(x for x in ast.parse(policy_source.read_text(encoding='utf-8')).body if isinstance(x,ast.FunctionDef) and x.name=='classify')
exec(compile(ast.Module(body=[function],type_ignores=[]),'pure-classifier','exec'),policy.__dict__)
sys.modules['iald_task_policy']=policy
metrics_path=p.parent/'staging'/'routing_stage'/'iald_routing_metrics.py'
spec=importlib.util.spec_from_file_location('metrics_under_test',metrics_path)
metrics=importlib.util.module_from_spec(spec);spec.loader.exec_module(metrics)
record={'model':'mimo-v2.6-pro'}
metrics.stamp(record,[{'role':'system','content':'python'},{'role':'user','task':'code','content':'[ARQUIVO: x]\npython\n[FIM]\nOlá'}])
assert record['task']=='conversation' and record['model']=='mimo-v2.6-pro'
metrics.stamp(record,[{'role':'user','content':[{'type':'video_url','video_url':{'url':'data:video/mp4;base64,AAAA'}},{'type':'text','text':'descreva'}]}])
assert record['task']=='video_analysis' and record['modality_counts']['video']==1
assert 'base64' not in json.dumps(record)
assert record['task_source']==metrics.VERSION
assert all(sha(p/name)==pin for name,pin in manifest['files'].items())
files=['iald_mimo_multimodal.py','app/iald.js','client.patch','consent_R4.patch','metrics_hooks_R4.patch','iald_app_providers_R4_final.py','real_decoder_result_R4.json']
receipt={'status':'FROZEN_READY_FOR_COORDINATION_BUNDLE_REVIEW_NOT_INSTALLED',
    'prior_final_manifest_verified':True,'prior_pins_unchanged':True,
    'media_api':'media_capabilities() matches INTEGRATION_R4_FINAL.json; dynamic decoder gate',
    'metrics_hooks':'stream and observe stamp(record,messages), host classifier/media partition, exact record.model preserved',
    'metrics_module_source':str(metrics_path),'metrics_module_sha256':sha(metrics_path),
    'metrics_semantic_assertions':'PASS: real classifier; system/client labels/file data excluded; video partition; no payload in metrics',
    'files':{name:sha(p/name) for name in files},
    'integration_order':'Merge R3 transport, then metrics_hooks_R4.patch and consent_R4.patch; or review derived iald_app_providers_R4_final.py against concurrent provider edits. Include coordinator routing metrics module pinned here, module/client/vendor resources. Do not blindly replace concurrent edits.',
    'limitations':'No full backend/browser/provider execution in this front; coordinator validates consent2, media exclusion from JEV/OpenAI and combined bundle before installation.',
    'next_modification':'Requires new explicit receipt; this front is frozen.'}
(p/'FREEZE_R4_RECEIPT.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'freeze':receipt['status'],'prior_pins_unchanged':True,'metrics_hooks':2,'semantic_assertions':'PASS'}))
