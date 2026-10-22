"""Build only staged shared client copies. Preserve runtime and earlier pinned preparation."""
from pathlib import Path
import hashlib,json,re,difflib

S=Path(__file__).resolve().parent;W=S.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
OUT=S/'release_R4';OUT.mkdir(exist_ok=True)
if any(OUT.iterdir()):raise RuntimeError('Existing output; use another revision')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
def new(path,raw):
    if not isinstance(raw,bytes):raw=json.dumps(raw,ensure_ascii=False,indent=2).encode()
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(raw)
    assert path.read_bytes()==raw
base=json.loads((S/'BASELINES_R1.json').read_bytes())
for item in base['client_baselines']:assert sha(Path(item['destination']).read_bytes())==item['baseline']
raw=(R/'app/iald.js').read_bytes();text=raw.decode('utf-8')
def span(source,name):
    match=re.search(r'(?m)^(?:export )?(?:async )?function '+re.escape(name)+r'\(',source)
    if not match:raise ValueError('Missing function '+name)
    start=source.index('{',match.end());depth=0;i=start
    while i<len(source):
        c=source[i]
        if source.startswith('//',i):
            end=source.find('\n',i);i=len(source) if end<0 else end;continue
        if source.startswith('/*',i):i=source.index('*/',i+2)+2;continue
        if c in "'\"`":
            quote=c;i+=1
            while i<len(source):
                if source[i]=='\\':i+=2;continue
                if source[i]==quote:i+=1;break
                i+=1
            continue
        if c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:return match.start(),i+1
        i+=1
    raise ValueError('Unclosed function '+name)
def get(source,name):a,b=span(source,name);return source[a:b]
def replace_function(source,name,body):
    a,b=span(source,name);return source[:a]+body+source[b:]
science={name:get(text,name) for name in ['promptSistema','contextoUsuario','recortar','estimarTokens']}
old_reader=get(text,'lerMidiaLocal');text=text.replace(old_reader,'',1)
integration=(S/'private_media_client_R4.js').read_bytes().decode()
needle='// Staging R3: local inline media only; server consent and validation authoritative.'
assert text.count(needle)==1;text=text.replace(needle,integration,1)

def patch(name,before,after,count=1):
    global text
    current=get(text,name);assert current.count(before)==count,(name,before,current.count(before))
    text=replace_function(text,name,current.replace(before,after,count))
patch('persistirConversasBackground',"  const key = backgroundHistoryKey(backgroundOwner);","  mediaAssertHistory(S.conversas);\n  const key = backgroundHistoryKey(backgroundOwner);")
patch('salvarConversas',"  guardar(K.conversas, S.conversas);","  mediaAssertHistory(S.conversas);\n  guardar(K.conversas, S.conversas);")
patch('desanexarRespostasBackground',"  if (sair) artifactAccessUI?.reset();","  if (sair) { mediaDetach(); mediaCapsAccount = ''; }\n  if (sair) artifactAccessUI?.reset();")
patch('identificarContaBackground',"    persistirConversasBackground();","    await carregarMotor();\n    await mediaMigrateLegacy(S.conversas, account);\n    persistirConversasBackground();")
patch('identificarContaBackground',"  refreshNativeNotificationsUI();","  if (await mediaMigrateLegacy(S.conversas, account)) persistirConversasBackground();\n  refreshNativeNotificationsUI();")
patch('apagarJobsDaConversa',"    await backgroundJobs.purgeConversation(id);","    await backgroundJobs.purgeConversation(id);\n    await mediaClearConversationLocal(owner, id);")
patch('apagarConversa',"mostrarFaixaFlutuante('Conversa apagada.'", "mostrarFaixaFlutuante('Conversa apagada. Anexos privados excluídos não são recuperados por Desfazer.'")
patch('abrirConversa',"  atualizarTitulo();","  atualizarTitulo();\n  mediaRestoreDrafts(c).catch(error => avisar(error.message));")
patch('desenharMensagem',"    corpo.textContent = textoDe(conteudo);","    corpo.textContent = textoDe(conteudo);\n    mediaHistoryControls(corpo, conteudo, conversaAtiva()?.id, backgroundOwner);")
patch('textoDe',"p?.type === 'input_audio'","p?.type === 'input_audio' || (['iald_media','iald_local_media'].includes(p?.type) && p.kind === 'audio')")
patch('textoDe',"p?.type === 'video_url'","p?.type === 'video_url' || (['iald_media','iald_local_media'].includes(p?.type) && p.kind === 'video')")
patch('desenharAnexos',"tirar.addEventListener('click', () => { S.anexos.splice(i, 1); desenharAnexos(); atualizarBotaoEnviar(); });", "tirar.addEventListener('click', async () => {\n      try {\n        if (a.localDraftId) await mediaRemoveLocal(a.mediaOwner, a.mediaConversation, a.localDraftId);\n        S.anexos.splice(i, 1); desenharAnexos(); atualizarBotaoEnviar();\n      } catch (error) { avisar(error.message); }\n    });")
patch('desenharAnexos',"  let chars = 0;","  let chars = 0;\n  if (midiaPermitida('audio') || midiaPermitida('video')) zona.appendChild(el('p', 'ajuda', MEDIA_LIMIT_TEXT));")

old=get(text,'enviar');updated=old.replace('function enviar()','async function enviar()',1)
updated=updated.replace("  if (respostaPendenteBackground()) return;","  if (mediaSending || respostaPendenteBackground()) return;",1)
start=updated.index("  S.anexos = []; S.dicaImagem = false; desenharAnexos();")
updated=updated[:start]+'''  const conversation = S.ativaId;
  mediaSending = true;
  try {
    if (await enviarTexto(texto, anexos) === false) return;
    if (S.ativaId === conversation) {
      S.anexos = S.anexos.filter(a => !anexos.includes(a)); S.dicaImagem = false; desenharAnexos();
      if ($('#entrada').value.trim() === texto) { $('#entrada').value = ''; redimensionarEntrada(); }
    }
  } catch (error) { avisar(error.message); }
  finally { mediaSending = false; atualizarBotaoEnviar(); }
}'''
text=replace_function(text,'enviar',updated)
old=get(text,'enviarTexto');updated=old.replace('function enviarTexto(','async function enviarTexto(',1)
a=updated.index('  let conteudo = texto;');b=updated.index('  if (arquivos.length)',a)
updated=updated[:a]+'''  const owner = backgroundOwner;
  const hasMedia = anexos.some(a => a.localDraftId) || c.mensagens.some(m => Array.isArray(m.content) && m.content.some(p => ['iald_media','iald_local_media'].includes(p?.type)));
  const midias = [];
  if (hasMedia) {
    if (!await mediaConsent(anexos, texto, c.id)) return false;
    await mediaPrepareLegacy(c, owner);
    for (const a of anexos) if (a.localDraftId) midias.push(await mediaUpload(a, owner, c.id));
    mediaActiveConversation(owner, c.id);
  }
  let conteudo = texto;
  const imagens = anexos.filter(a => a.image).map(a => a.image);
  const arquivos = anexos.filter(a => !a.image && !a.localDraftId && a.content);
'''+updated[b:]
updated=updated.replace('  salvarConversas();','  mediaAssertHistory(S.conversas);\n  salvarConversas();\n  if (hasMedia) mediaMarkSubmitted(anexos, owner, c.id).catch(error => avisar("Mídia preservada no histórico; falha ao atualizar o rascunho local: " + error.message));',1)
updated=updated.replace('  transmitir(montarEnvio(c));','  transmitir(montarEnvio(c));\n  return true;',1)
text=replace_function(text,'enviarTexto',updated)
patch('montarEnvio',"    const conteudo = m.content;","    const conteudo = m.content;\n    if (Array.isArray(conteudo) && conteudo.some(p => p?.type === 'iald_local_media')) throw Error('Mídia local ainda não foi enviada com autorização; histórico preservado.');")
patch('consentirEContinuar',"    fecharFolhas();","    fecharFolhas();\n    if (mediaPendingConsent) {\n      try { await mediaResumeConsent(); } catch (error) { estadoConsentimento(error.message); }\n      return;\n    }")
patch('lerMotor',"  const ticket = ++motorRequest;","  const ticket = ++motorRequest;\n  const mediaOwner = backgroundOwner, mediaEpoch = backgroundEpoch;")
patch('lerMotor',"    S.motor = next;","    if (mediaOwner !== backgroundOwner || mediaEpoch !== backgroundEpoch) return;\n    const previousMediaScope = mediaStorageScope();\n    if (previousMediaScope && previousMediaScope !== (next.limites?.media_capabilities?.media_scope || null)) mediaDetach();\n    S.motor = next; mediaCapsAccount = mediaOwner;")
patch('excluirConta',"  if (backgroundOwner) {","  try {\n    for (const c of S.conversas) if (backgroundOwner && c.background_owner === backgroundOwner) await mediaClearConversationLocal(backgroundOwner, c.id);\n  } catch (error) { alert('Conta excluída no servidor; falha visível na limpeza da mídia local: ' + error.message); }\n  if (backgroundOwner) {")
needle="$('#btn-recusar-consentimento').addEventListener('click', () => { S.avisoConsentimento = null; fecharFolhas(); });"
assert text.count(needle)==1;text=text.replace(needle,"$('#btn-recusar-consentimento').addEventListener('click', () => { mediaPendingConsent = null; S.avisoConsentimento = null; fecharFolhas(); });")
text=text.replace('    enviarTexto(novo, []);',"    enviarTexto(novo, []).catch(error => avisar(error.message));",1)
text=text.replace('  enviarTexto(textoDe(anterior.content), []);',"  enviarTexto(textoDe(anterior.content), []).catch(error => avisar(error.message));",1)
for name,value in science.items():assert get(text,name)==value,'Scientific/context function changed: '+name
assert 'Duração máxima: áudio 30 s; vídeo 10 s.' not in text and 'Limite local de 512 KB' not in text
payload=text.encode();files=[]
for item in base['client_baselines']:
    dest=Path(item['destination']);rel=dest.relative_to(R);source=OUT/rel;new(source,payload)
    files.append(dict(source=str(source),destination=str(dest),sha256=sha(payload),baseline=item['baseline']))
for item in base['version_candidates']:
    assert sha(Path(item['destination']).read_bytes())==item['baseline']
    source=OUT/Path(item['source']).relative_to(S/'version_candidates');new(source,Path(item['source']).read_bytes())
    files.append({**{k:item[k] for k in ['destination','sha256','baseline']},'source':str(source)})
new(OUT/'CLIENT_DIFF_R4.patch',''.join(difflib.unified_diff(raw.decode().splitlines(True),text.splitlines(True),fromfile='baseline/app/iald.js',tofile='candidate/app/iald.js')).encode())
new(OUT/'install_plan_R4.json',dict(status='CANDIDATE_NOT_INSTALLED_REQUIRES_TESTS_REVIEW',files=files,helper_embedded=True,external_script_or_index_changes=False,backend_contract=dict(path=str(W/'backend_stage/CONTRACT.json'),sha256=sha((W/'backend_stage/CONTRACT.json').read_bytes())),scientific_context_functions_preserved=list(science),build=False,push=False))
new(OUT/'BUILD_RECORD_R4.json',dict(status='STAGED_ONLY',client_sha256=sha(payload),bytes=len(payload),targets=len(files),runtime_unchanged=all(sha(Path(i['destination']).read_bytes())==i['baseline'] for i in files),scientific_context_functions_preserved=True,required_backend_hooks=['Host supplies generation-bound media_scope in authenticated capabilities.','Host authorizes conversation before upload; conversation registration is server-owned.','Existing explicit conversation/account deletion must remove private attachments and report failures.'],no_remote_playback_route=True))
print(json.dumps(dict(out=str(OUT),sha256=sha(payload),files=len(files),runtime_changed=False)))
