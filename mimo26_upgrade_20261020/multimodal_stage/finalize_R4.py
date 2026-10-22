"""Separate consent delta and R4 manifest; never regenerate R3 transport pins."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

root=Path(__file__).parent
provider=root/'iald_app_providers.py'
original=provider.read_text(encoding='utf-8')
needle='        "A moderação das mensagens continua usando a OpenAI. "'
replacement='''        + ("Os anexos de imagem, áudio e vídeo são enviados somente à Xiaomi MiMo. "
           "Os PDFs são enviados como texto extraído, sem o arquivo PDF original. "
           "Os bytes dos anexos não são enviados ao TypeSafe nem à OpenAI. "
           "A moderação textual continua usando a OpenAI. " if provider == 'mimo' else
           "A moderação das mensagens continua usando a OpenAI. ")'''
assert original.count(needle)==1
staged=original.replace(needle,replacement,1)
compile(staged,'R4-consent','exec')
# Keep R3 provider staging immutable. Coordinator applies this small extra delta.
(root/'consent_R4.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),staged.splitlines(True),fromfile='a/iald_app_providers.py',tofile='b/iald_app_providers.py')),encoding='utf-8')
nodes=[n for n in ast.parse(staged).body if isinstance(n,ast.FunctionDef) and n.name=='consent_text']
ns={'MODELS':{'mimo':{'provider':'Xiaomi MiMo'},'kimi':{'provider':'Moonshot'}}}
exec(compile(ast.Module(body=nodes,type_ignores=[]),'consent-test','exec'),ns)
assert 'bytes dos anexos' in ns['consent_text']('mimo')
assert 'somente à Xiaomi' not in ns['consent_text']('kimi')
names=['iald_mimo_multimodal.py','app/iald.js','client.patch','client_media.js','test_dependency.py','consent_R4.patch','INTEGRATION_R4_FINAL.json']
(root/'MANIFEST_R4_FINAL.json').write_text(json.dumps({'revision':'R4_FINAL','production_install':False,'files':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}},indent=2),encoding='utf-8')
print('R4 consent assertions PASS; final manifest saved; R3 unchanged')
