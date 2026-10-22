"""New candidate for scope-bound upload/metadata; never modify pinned R5."""
from pathlib import Path
import json,hashlib,difflib,re
S=Path(__file__).resolve().parent;W=S.parent;OLD=S/'release_R5';OUT=S/'release_R6'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(b,bytes):b=json.dumps(b,ensure_ascii=False,indent=2).encode()
    with p.open('xb') as f:f.write(b)
    assert p.read_bytes()==b
OUT.mkdir(exist_ok=False)
before=(S/'private_media_client_R4.js').read_bytes().decode();helper=before
needle='async function mediaUpload(anexo, owner, conversation) {'
addition='''function mediaBoundResponse(value, expected) {
  if (typeof expected !== 'string' || !/^[0-9a-f]{32}$/.test(expected) || !value || value.media_scope !== expected)
    throw Error('O escopo da resposta de mídia não corresponde à conta original. Nada foi anexado; o envio não foi repetido.');
  const { media_scope, ...part } = value;
  return canonicalMediaPart(part);
}
'''
helper=helper.replace(needle,addition+needle)
helper=helper.replace('  const originalStorageScope = mediaStorageScope();','  const originalStorageScope = mediaStorageScope();\n  if (!originalStorageScope) throw Error("O servidor não forneceu escopo seguro de envio. O arquivo permanece local; aguarde a atualização da conta.");')
helper=helper.replace("  if (record.part) return canonicalMediaPart(record.part);","  if (record.storageScope !== originalStorageScope) throw Error('O rascunho pertence a outro escopo de conta.');\n  if (record.part) return canonicalMediaPart(record.part);")
helper=helper.replace("encodeURIComponent(conversation), {\n    method: 'POST'","encodeURIComponent(conversation) + '&expected_media_scope=' + encodeURIComponent(originalStorageScope), {\n    method: 'POST'")
helper=helper.replace('  const part = canonicalMediaPart(await response.json());','  const part = mediaBoundResponse(await response.json(), originalStorageScope);')
helper=helper.replace('        mediaScope(owner, conversation); canonicalMediaPart(p);','        mediaScope(owner, conversation); canonicalMediaPart(p);\n        const expectedScope = mediaStorageScope();\n        if (!expectedScope) throw Error("Escopo seguro de mídia indisponível; nada foi consultado.");')
helper=helper.replace("encodeURIComponent(conversation), { cache: 'no-store' }","encodeURIComponent(conversation) + '&expected_media_scope=' + encodeURIComponent(expectedScope), { cache: 'no-store' }")
helper=helper.replace('        const actual = canonicalMediaPart(await r.json()); mediaScope(owner, conversation);','        const actual = mediaBoundResponse(await r.json(), expectedScope); mediaScope(owner, conversation);\n        if (expectedScope !== mediaStorageScope()) throw Error("O escopo da conta mudou durante a consulta.");')
assert helper.count('expected_media_scope=')==2
put(S/'private_media_client_R6.js',helper.encode())
plan=json.loads((OLD/'install_plan_R5.json').read_bytes());files=[]
for item in plan['files']:
    src=Path(item['source']);rel=src.relative_to(OLD);raw=src.read_bytes()
    if src.name=='iald.js':
        text=raw.decode();assert text.count(before)==1
        raw=text.replace(before,helper).encode()
    dest=OUT/rel;put(dest,raw);files.append({**item,'source':str(dest),'sha256':sha(raw)})
plan.update(status='CANDIDATE_R6_SCOPE_BINDING_WAIT_BACKEND_CONTRACT_TESTS_REVIEW',files=files,
    supersedes=str(OLD/'install_plan_R5.json'),pending=['Backend expected_media_scope pre-body comparison + response scope','Bind updated contract after backend stable'])
plan.pop('backend_contract_frozen',None)
put(OUT/'install_plan_R6.json',plan)
for src in ['test_private_media_R4.cjs','test_client_flow_R4.cjs','CLIENT_FUNCTION_FIXTURE_R4.js']:
    name=src.replace('_R4','_R6');t=(S/src).read_text(encoding='utf8').replace('_R4','_R6')
    t=t.replace("'/api/private-media?conversation_id=conv-A'","'/api/private-media?conversation_id=conv-A&expected_media_scope='+'a'.repeat(32)")
    t=t.replace('json:async()=>part(options.body.size)',"json:async()=>({...part(options.body.size),media_scope:'a'.repeat(32)})")
    t=t.replace("json:async()=>part(file('concurrent').size)","json:async()=>({...part(file('concurrent').size),media_scope:'a'.repeat(32)})")
    put(S/name,t.encode())
put(OUT/'SCOPE_DIFF_R6.patch',''.join(difflib.unified_diff(before.splitlines(True),helper.splitlines(True),fromfile='R5helper',tofile='R6helper')).encode())
print(json.dumps({'sha256':files[0]['sha256'],'out':str(OUT),'targets':len(files)}))
