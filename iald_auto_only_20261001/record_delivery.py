"""Record measured delivery and explicit remaining budget approval; byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os
W=Path(__file__).parent;C=W.parent.parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
M=Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory')
live=json.loads((W/'live_verification.json').read_bytes());checks=json.loads((W/'checks.json').read_bytes())
mobile=json.loads((W/'mobile_audit.json').read_bytes());android=json.loads((W/'android_release.json').read_bytes());deployment=json.loads((W/'deployment.json').read_bytes())
assert checks['passed'] and mobile['passed'] and android['versionCode']==26
assert live['health']==200 and live['router_available'] and live['installed_file_hashes_verified']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(R/n)==h for n,h in deployment['files'].items())
assert all(sha(R/n)==h for n,h in deployment['scientific_unchanged'].items())
assert sha(Path(android['apk']['path']))==android['apk']['sha256']
assert not (W/'public_budget_configuration.json').exists(),'Budget state changed; update this record before running'
marker='IALD_AUTO_CONTINUOUS_ONLY_LUIZ_MANUAL_20261001'
note=f'''

## {datetime.now():%d/%m/%Y %H:%M} — Seletor contínuo automático; escolha manual somente Luiz

<!-- {marker} -->

[INPUT — ordem central] O modo automático deve coordenar cada mensagem/tarefa de todos os usuários. Somente a conta exata `luiz` conserva seleção individual de modelos para testes. Alana, Liana e demais aprovados não escolhem modelo; escolhas antigas não prevalecem. Todos os executores do app são admissíveis no automático quando prontos, consentidos e com orçamento, exceto Sonnet para qualquer outra conta. Esta ordem substitui a liberdade manual geral do adendo anterior de JEV padrão. Manter consentimento individual, bloqueio/revogação e isolamento; não inferir aceite de terceiros.

[REAL — implantado] Servidor atualizado e reiniciado pelo supervisor existente, saúde local200. Nove contas aprovadas conferidas; oito contas diferentes de luiz recebem automático continuamente; somente luiz tem manual=true. API oculta opções manuais e recusa troca manual direta ou administrativa para os demais. JEV seleciona novamente a cada turno/tarefa; DeepSeek agora elegível, junto de OpenAI, Haiku, MiMo, Kimi e nativa, sujeito às condições efetivas. Sonnet continua só luiz. Nativa automática usa contexto científico público isolado, sem memória privada do operador, com ferramentas fechadas e moderação/consentimento próprios. Revalida conta e consentimentos antes de cada envio/delegação; uma chamada comprovadamente recusada antes do transporte devolve a reserva, enquanto envio iniciado/incerto preserva a reserva conservadora.

[REAL — cliente] Escolha de motor oculta para usuários comuns. Configurações de privacidade permitem ler/autorizar/revogar os provedores sem selecionar motor; nenhum aceite automático. Interface sintética393x852 conferida para convidado e operador; no domínio real, entrada com a conta beta anteriormente autorizada mostrou IALD Automática, sem seletor e com os novos controles. Nenhuma mensagem de geração ou aceite de provedor foi enviado nessa sessão beta. Autenticação web preservada: GET não autenticado de app/iald.js retorna HTML de login. O hash remoto desse recurso está explicitamente NOT_VERIFIED; NÃO usar esse HTML como auditoria de JS. Hashes de arquivos instalados e empacotados conferidos separadamente.

[REAL — validação] {checks['tests']} testes executados, {checks['skipped']} ignorado, zero falhas/erros; transportes simulados, zero novas chamadas pagas. Revisão independente fechou os três ajustes finais de reserva não enviada, aviso de consentimento e primeiro aceite da nativa. Auditoria móvel aprovada: versões, mesmo certificado Android anterior, integridade APK/AAB, espelhos web/www/iOS/Android e ausência de backups/segredos nos padrões examinados. Ausência de matches não é prova absoluta de ausência de segredos. Recibos locais delimitam as verificações; nenhum teste em aparelho físico feito pelo agente.

[OPEN — autorização financeira específica] A configuração efetiva ainda não contém IALD_HAIKU_PUBLICO_USD_DIA nem IALD_HAIKU_GRUPO_USD_DIA. Assim Haiku público permanece indisponível e MiMo/DeepSeek públicos recusam antes do gasto, apesar da nova permissão de acesso. O operador havia escolhido usar o orçamento público do Haiku, mas os valores nunca haviam sido salvos. Preparado configure_public_budget.py, que apenas acrescenta US$1/pessoa/dia e US$5/grupo/dia, com backups protegidos; teto geral Anthropic e conta luiz intactos. MiMo e DeepSeek compartilham um grupo; Haiku tem grupo separado. A revisão automática recusou por ausência de aceite explícito dos valores exatos; pergunta enviada, ainda sem resposta neste registro. NÃO executar esse script ou remover a guarda enquanto aguarda. Depois de autorização, aplicar, validar orçamento/contexto real, reiniciar somente web ocioso e conferir Haiku nas opções/avisos de privacidade. Não anunciar todos os modelos operantes para público antes disso.

[DISPONIBILIDADE] Web ativo. iOS4.1(29), build Apple3ce92114-47fe-41c8-8ebc-1563b49f165a: IALD Equipe(interno1tester) e IALD Piloto(externo6testers) ambos Em testes, observado no App Store Connect; notificações automáticas habilitadas no envio. Convite existente https://testflight.apple.com/join/A5XEdy1H. Apple mostra90dias relativos; vencimento absoluto não conferido, não inferir. Android4.1(26) APK assinado publicado em {android['url']} (requer login da IALD); AAB local auditado. GooglePlay continua pendente de cadastroDUNS, sem envio à loja nesta entrega. Instalação física não certificada; nenhum prazo operacional inserido na conversa pública. Commit móvel {mobile['commit']} enviado à branch privada codex/mobile-release. Handoff local atualizado após o commit, sem novo push que dispare build repetida.

[ESCOPO E INTEGRIDADE] Release científico v378 preservado, inclusive manifesto, kernelv5 e pacote medidoHaiku; nenhum original um.py executado/editado, peso ou gate alterado. Arquivos de usuários/senhas não regravados. A fila científica e sua memória própria não foram atualizadas. Evidências: work/iald_auto_only_20261001/checks.json, review_closed.txt, deployment.json, restart.json, live_verification.json, mobile_audit.json, android_verified.json e android_release.json. A primeira publicação APK foi recusada por leitura equivocada de versionCode25; aapt confirmou26 e nova revisão autorizou o mesmo script correto. A sondagem remotaJS foi segregada como não verificada, sem falsa auditoria de hash. Orçamento público é a única ação ainda bloqueada por revisão automática.
'''
paths=[R/'CLAUDE.md',C/'work/iald_openai_motor_20260914/HANDOFF_RUNTIME.md',R/'iald-app/HANDOFF_MOTOR_OPENAI_20260914.md',C/'memory/TGL_ATLAS.md',C/'memory/TGL_INDICE_VIVO.md',M/'MEMORY_2.md',M/'app-iald-mobile.md']
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');report=[]
def save(p,raw):
 old=p.read_bytes() if p.exists() else None
 if old is not None:
  b=p.with_name(p.name+'.bak_'+stamp)
  with b.open('xb') as f:f.write(old);f.flush();os.fsync(f.fileno())
  assert b.read_bytes()==old
 t=p.with_name(p.name+'.tmp_auto_'+stamp)
 with t.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert t.read_bytes()==raw and raw
 assert (p.read_bytes() if p.exists() else None)==old
 os.replace(t,p);assert p.read_bytes()==raw
 return str(b) if old is not None else None
for p in paths:
 assert p.is_file()
 old=p.read_bytes()
 if marker.encode() in old:continue
 new=old+note.encode();backup=save(p,new)
 assert len(new)>len(old)
 report.append({'path':str(p),'backup':backup,'sha256':sha(p)})
delivery={'at':datetime.now().astimezone().isoformat(),'policy':'ONLY_LUIZ_MANUAL_ALL_OTHER_APPROVED_AUTO_EVERY_TURN','web':'ACTIVE','ios_version':'4.1 (29)','ios_internal':'Em testes','ios_external':'Em testes','android_version':'4.1 (26)','android_url':android['url'],'google_play':'DUNS_PENDING','pending':'PUBLIC_BUDGET_EXACT_VALUES_APPROVAL','paid_test_calls':0,'scientific_release':'v378_preserved','memories':report}
save(W/'delivery.json',json.dumps(delivery,ensure_ascii=False,indent=2).encode())
print(json.dumps({'surfaces_updated':len(report),'status':'DELIVERED_POLICY_MOBILE_BUDGET_PENDING'}))
