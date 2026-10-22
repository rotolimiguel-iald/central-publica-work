"""Stage only bootstrap fix. All R6 evidence/runtime remains untouched."""
from pathlib import Path
import ast,re,json,hashlib,difflib
S=Path(__file__).resolve().parent;W=S.parent;R=Path('C:/IALD/projetos_pyhton/IALD');OUT=S/'bootstrap_hotfix_R7'
OUT.mkdir(exist_ok=True)
assert not any(OUT.iterdir()),'Output already contains evidence; use a new revision'
def put(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(raw,bytes):raw=json.dumps(raw,ensure_ascii=False,indent=2).encode()
    with p.open('xb') as f:f.write(raw)
def sha(b):return hashlib.sha256(b).hexdigest()
source=(S/'release_R6/app/iald.js').read_bytes();before=source.decode();text=before
# Recover exact function extractor without importing its build script.
tree=ast.parse((S/'build_client_R4.py').read_bytes());ns=dict(re=re)
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'span','get'}]
exec(compile(ast.Module(body=nodes,type_ignores=[]),'function extraction only','exec'),ns)
def replace(name,new):
    global text
    a,b=ns['span'](text,name);text=text[:a]+new+text[b:]
old=ns['get'](text,'identificarContaBackground')
needle='''    await carregarMotor();
    await mediaMigrateLegacy(S.conversas, account);
    persistirConversasBackground();
    if (!S.conversas.length) novaConversa({ semFoco: true });
    else { listarConversas(); abrirConversa(); }'''
start=old.index('    await carregarMotor();')
end=old.index('    else { listarConversas(); abrirConversa(); }',start)+len('    else { listarConversas(); abrirConversa(); }')
needle=old[start:end]
new=old.replace(needle,'''    // Show the authenticated owner's history before asynchronous recovery.
    // Never leave the previously rendered generic/other-account list visible.
    listarConversas(); abrirConversa();''')
needle='  if (await mediaMigrateLegacy(S.conversas, account)) persistirConversasBackground();'
assert needle in new
new=new.replace(needle,'''  await mediaRecoverLegacyHistory(account);
  if (!S.conversas.length) novaConversa({ semFoco: true });
  else { listarConversas(); abrirConversa(); }''')
replace('identificarContaBackground',new)
insert='''async function mediaAwaitBoundMotor(owner) {
  const epoch = backgroundEpoch;
  let pending = carregarMotor();
  // A newer request may supersede the one awaited by this bootstrap. Follow
  // that actual promise; never equate an ignored response with ready caps.
  for (let n = 0; n < 8; n++) {
    await pending;
    if (owner !== backgroundOwner || epoch !== backgroundEpoch) throw detached();
    if (pending !== S.motorCarregando) { pending = S.motorCarregando; continue; }
    if (mediaStorageScope()) return;
    break;
  }
  throw new PendingChatJobError('O escopo seguro ainda não foi carregado. O histórico original foi preservado; a recuperação será retomada.');
}
async function mediaRecoverLegacyHistory(owner) {
  const legacy = S.conversas.some(c => (c.mensagens || []).some(m => Array.isArray(m.content) && m.content.some(p =>
    (p?.type === 'input_audio' && typeof p.input_audio?.data === 'string' && p.input_audio.data.startsWith('data:audio/')) ||
    (p?.type === 'video_url' && typeof p.video_url?.url === 'string' && p.video_url.url.startsWith('data:video/')))));
  if (!legacy) return;
  await mediaAwaitBoundMotor(owner);
  const epoch = backgroundEpoch, scope = mediaStorageScope(), snapshot = JSON.stringify(S.conversas);
  const recovered = JSON.parse(snapshot);
  await mediaMigrateLegacy(recovered, owner);
  if (owner !== backgroundOwner || epoch !== backgroundEpoch || scope !== mediaStorageScope()) throw detached();
  if (snapshot !== JSON.stringify(S.conversas)) throw new PendingChatJobError('O histórico mudou durante a recuperação; as alterações foram preservadas e a recuperação será retomada.');
  S.conversas = recovered;
  persistirConversasBackground();
}
'''
text=text.replace('async function mediaMigrateLegacy(conversations, owner) {',insert+'async function mediaMigrateLegacy(conversations, owner) {',1)
old=ns['get'](text,'mediaMigrateLegacy')
new=old.replace('  let changed = false;','''  let changed = false;
  const expectedScope = mediaStorageScope(), epoch = backgroundEpoch;
  const sameScope = () => {
    if (owner !== backgroundOwner || epoch !== backgroundEpoch || expectedScope !== mediaStorageScope()) throw detached();
  };''',1)
new=new.replace("        if (!mediaStorageScope()) throw Error", "        sameScope();\n        if (!expectedScope) throw Error",1)
new=new.replace("        await mediaLocal('readwrite', store => store.put(record));","        sameScope();\n        await mediaLocal('readwrite', store => store.put(record));\n        sameScope();",1)
replace('mediaMigrateLegacy',new)
old=ns['get'](text,'salvarConversas');assert old.count('function salvarConversas()')==1
body=old[old.index('{')+1:-1]
replace('salvarConversas','''function salvarConversas() {
  try {'''+body+'''
  } catch (error) {
    // UI actions may proceed in RAM; durable job delivery still calls the
    // strict persistirConversasBackground directly and cannot acknowledge loss.
    avisarBackground('Não foi possível salvar esta alteração. O histórico original foi preservado; esta mudança fica só nesta aba até a recuperação: ' + error.message);
    return false;
  }
}''')
for name in ['promptSistema','contextoUsuario','recortar','estimarTokens','mediaUpload','mediaHistoryControls','mediaConsent','mediaBoundResponse']:
    assert ns['get'](before,name)==ns['get'](text,name),name
payload=text.encode();files=[]
oldplan=json.loads((S/'release_R6/install_plan_R6_FINAL.json').read_bytes())
for x in oldplan['files']:
    if Path(x['destination']).name!='iald.js':continue
    dest=Path(x['destination']);assert dest.read_bytes()==source,'Runtime no longer R6'
    p=OUT/dest.relative_to(R);put(p,payload)
    files.append(dict(source=str(p),destination=str(dest),sha256=sha(payload),baseline=sha(source)))
put(OUT/'install_plan_R7.json',dict(status='STAGED_HOTFIX_WAIT_TESTS_AND_DISTINCT_REVIEW',files=files,build=False,push=False,runtime_writes=False,versions_unchanged=True,previous_mobile_runner_blocked=True))
put(OUT/'BOOTSTRAP_DIFF_R7.patch',''.join(difflib.unified_diff(before.splitlines(True),text.splitlines(True),fromfile='installedR6',tofile='candidateR7')).encode())
names=['identificarContaBackground','persistirConversasBackground','salvarConversas','novaConversa','carregarMotor','lerMotor','limitesDoPlano']
for label,content in [('R6',before),('R7',text)]:
    funcs='\n'.join(ns['get'](content,n) for n in names)
    if label=='R7':funcs+='\n'+ns['get'](content,'mediaAwaitBoundMotor')+'\n'+ns['get'](content,'mediaRecoverLegacyHistory')
    put(OUT/('BOOTSTRAP_FUNCTIONS_'+label+'.js'),funcs.encode())
helper=(S/'private_media_client_R6.js').read_text(encoding='utf8')
helper=helper.replace(ns['get'](helper,'mediaMigrateLegacy'),ns['get'](text,'mediaMigrateLegacy'))
put(OUT/'private_media_client_R7.js',helper.encode())
print(json.dumps({'asset_sha256':sha(payload),'files':len(files),'runtime_writes':False}))
