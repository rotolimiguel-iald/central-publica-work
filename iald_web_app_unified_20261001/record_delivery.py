from pathlib import Path
from datetime import datetime
import hashlib,json,os
W=Path(__file__).parent;C=W.parent.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
M=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
checks=json.loads((W/'checks.json').read_bytes());runtime=json.loads((W/'runtime.json').read_bytes());deployment=json.loads((W/'deployment.json').read_bytes())
assert checks['passed'] and runtime['health']==200 and runtime['installed_files_match'] and runtime['public_manifest_bytes_match']
assert (W/'review_closed.txt').exists()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/n)==h for n,h in deployment['installed'].items())
assert all(sha(R/n)==h for n,h in deployment['preserved_sha256'].items())
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');marker='IALD_ONE_CONVERSATION_UI_WEB_NATIVE_20261001'
note=f'''

## {datetime.now():%d/%m/%Y %H:%M} — Site e app com a mesma interface de conversa
<!-- {marker} -->
[INPUT] Operador pediu que demo.iald.ia.br use a mesma forma e conteúdo de interface do app. Manter uma interface compartilhada nas próximas entregas; não retornar o operador ou o motor nativo à tela web antiga.
[REAL — causa e correção] _destino_web ainda enviava administradores e contas nativas a iald_chat.html. Agora todas as contas autenticadas seguem para /app/index.html; artefato pendente válido conserva seu UUID e é consumido uma vez. O endereço antigo redireciona302 com no-store à mesma interface, passando pela autenticação existente. Manifesto web abre /app/index.html, conserva identidade /iald_chat.html e explicita scope=/ para manter login/retornos no escopo do atalho instalado. Descrição alinhada à interface. Ícones/display preservados. Somente iald_web_server.py e manifest.json foram alterados; cópias byte a byte guardadas imediatamente antes da troca.
[REAL — paridade e testes] HTML, JS principal, CSS e identificação cadastral conferidos por hash: mesmos bytes em web/app, www, iOS public e Android assets. {checks['checks']} verificações isoladas aprovadas, incluindo administrador, convidado, anônimo, bloqueado, arquivos não permitidos, UUID único e recusa de redirecionamento externo. require_auth tem AST idêntica ao estado anterior. Revisão independente corrigiu scope da PWA antes da implantação. Nenhuma geração de IA/pagamento ou aceite de provedor. Servidor web reiniciado sozinho pelo supervisor existente, após zero jobs/reservas ativos; saúde200 e manifesto servido conferidos. No navegador autenticado com a conta beta já autorizada, domínio principal e /iald_chat.html chegaram a /app/index.html com Haja Luz, prompts, ferramentas e configurações comuns. Hash de JavaScript autenticado remoto não medido; paridade é dos arquivos locais instalados/empacotados, distinta da verificação visual.
[DISPONIBILIDADE] Web ativo em https://demo.iald.ia.br/. iOS interno/externo permanecem4.1(29), ambos Em testes na entrega anterior; Android permanece4.1(26), APK publicado no canal autenticado. Binários não precisaram nova compilação porque os recursos compartilhados não mudaram. GooglePlay segue pendenteDUNS. Nenhuma nova instalação física foi certificada. Entrada no site continua exigindo conta aprovada; automático para demais contas e escolha manual somente luiz, conforme regra anterior. A pendência de aprovação dos valores públicos Haiku/MiMo/DeepSeek permanece separada e NÃO foi interpretada como aprovada pelo pedido de unificar o site.
[INTEGRIDADE E LIMITES] Contas, senhas, kernel, manifesto científico v378 e pacote Haiku preservados por hash. Originais científicos e gate não alterados. Histórico local antigo não foi apagado nem migrado, e unificar interface não sincroniza automaticamente conversas entre aparelhos. Não criado serviço novo de armazenamento ou notificação. Evidências: work/iald_web_app_unified_20261001/checks.json, review.txt, review_closed.txt, deployment.json, restart.json e runtime.json.
'''
paths=[R/'CLAUDE.md',C/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',C/'memory/TGL_ATLAS.md',C/'memory/TGL_INDICE_VIVO.md',M/'MEMORY_2.md',M/'app-iald-mobile.md']
def save(p,data):
 old=p.read_bytes() if p.exists() else None;b=None
 if old is not None:
  b=p.with_name(p.name+'.bak_'+stamp)
  with b.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
  assert b.read_bytes()==old
 t=p.with_name(p.name+'.tmp_unified_'+stamp)
 with t.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==data and data and (p.read_bytes() if p.exists() else None)==old
 os.replace(t,p);assert p.read_bytes()==data
 return str(b) if b else None
memories=[]
for p in paths:
 assert p.is_file();old=p.read_bytes()
 if marker.encode() in old:continue
 new=old+note.encode('utf-8');backup=save(p,new);assert len(new)>len(old)
 memories.append({'path':str(p),'backup':backup,'sha256':sha(p)})
result={'at':datetime.now().astimezone().isoformat(),'web':'ACTIVE_SHARED_APP_UI','authenticated_browser_root':'/app/index.html','authenticated_browser_legacy':'/app/index.html','browser_test_account':'authorized_beta','provider_calls':0,'checks':checks['checks'],'shared_client_changed':False,'ios_internal':'4.1 (29), unchanged','ios_external':'4.1 (29), unchanged','android':'4.1 (26), unchanged','google_play':'DUNS_PENDING','public_budget':'EXACT_VALUES_APPROVAL_STILL_PENDING','memories':memories}
save(W/'delivery.json',json.dumps(result,ensure_ascii=False,indent=2).encode());print(json.dumps({'web':result['web'],'memories':len(memories),'checks':checks['checks']}))
