"""Persist the expiry-panel requirement and verified integration state, no secrets."""
from datetime import datetime
import importlib.util
import json
from pathlib import Path

WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
spec=importlib.util.spec_from_file_location('targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

def append(path,marker,note,stamp):
    before=path.read_bytes()
    if marker.encode() in before:return 'already_recorded'
    helper.create(path.with_name(path.name+'.bak_'+stamp),before)
    nl='\r\n' if b'\r\n' in before else '\n'
    after=before+('\n\n## '+datetime.now().strftime('%d/%m/%Y %H:%M')+' — Prazos operacionais da IALD\n\n<!-- '+marker+' -->\n\n'+note+'\n').replace('\n',nl).encode()
    temp=path.with_name(path.name+'.tmp_'+stamp);helper.create(temp,after)
    assert path.read_bytes()==before
    temp.replace(path);assert path.read_bytes()==after and len(after)>len(before)
    return 'updated'

def main():
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    rule='''[INPUT — ordem permanente do operador] Prazos de chaves de API, testes e outras dependências com vencimento devem permanecer visíveis no painel da IALD, com data, tempo restante e alertas antecipados. Ao criar/renovar uma chave ou distribuir uma build de teste, conferir a data exata no provedor e atualizar o registro operacional na mesma entrega. Não inferir vencimento apenas da duração nominal nem da data do arquivo. Prazos desconhecidos/ilegíveis aparecem como não informados/indisponíveis, nunca como ilimitados. Não exibir credenciais; dados operacionais apenas ao operador. Alertas a 30/14/7/3/1 dias, vencido e falha de leitura. Visibilidade não garante continuidade se houver revogação, falta de saldo ou falha externa; não prometer renovação automática. Manter atualização conjunta web/iOS/Android aplicáveis.'''
    note=rule+'''

[REAL] Operador criou a organização Anthropic IALD LTDA e comprou créditos pessoalmente. Console: US$100 e nível Scale. Operador criou IALD servidor no workspace Default, sem Admin API; relatou duração de60 dias. O diálogo mostrou vencimento exato 29/11/2026 10:00 BRT; registrado esse valor, sem calcular pela duração relatada. Helper confirmou IALD_CLAUDE_KEY_SAVED=true. Nenhuma chave exposta em conversa/recibo; cópia virtual do navegador não funcionou, operador colou e salvou pelo formulário protegido.

[REAL] Autorização específica de envio do contexto TGL sem Atlas privado para contagem em api.anthropic.com. Contagem completou sem erros: público318984 o200k/538378 Claude; operador325288 o200k/547922 Claude. Fator operacional calculado dos tokens líquidos com margem5% e arredondamento para cima=1.77; somente essa linha do .env alterada com backup/ACL restrita. Recibos claude_chave.json e medicao_tokens.json.

[REAL] Novo pedido autoriza as mudanças limitadas de código em iald_web_server.py e app/iald.js apesar da restrição de coordenação da ordem antiga. Módulo iald_deadlines.py lê registro de datas sem acessar credenciais. /api/alertas inclui prazos apenas quando o cadastro é admin. Cartão permanente no painel admin e na interface app/web do operador, via operational_deadlines.js. www sincronizado. Datas desconhecidas da chave OpenAI e TestFlight interno/externo marcadas unknown até conferência. Registro: iald_deadlines.json. Atualização de datas é lida sem reinício. A fonte da data deve ser atualizada a cada renovação; não há integração automática com as APIs administrativas dos provedores.

[REAL] Quatro testes de prazo (limiares, fuso, dado inválido, renovação) e três do endpoint real isolado (usuário comum, admin, falha do cadastro) passaram. JS syntax e validate-release passaram. Filho web57020 reiniciado sob supervisor41020 sem reservas ativas; log r6 sem stderr, sincronização iniciada; saúde8081/8082/pública200; /api/alertas anônimo401. O primeiro recibo runtime procurou marcador incorreto chave=presente; correção usa o literal real chave=definida, conforme fonte, no recibo complementar.

[INPUT/OPEN] Operador autorizou duas mensagens Claude com o contexto já autorizado, teto US$2,00 fria +US$0,30 quente, e consentimento Anthropic. Nenhuma delas executada ainda. Login luiz pendente para conferência visual e teste de cache. Navegador set visible não confirmou exibição; open_in_codex retornou queued; fornecido link direto de login. Não declarar renderização autenticada nem teste pago concluído.

[OPEN] Build iOS18/Android17 e exportação física continuam pendentes. O hash antigo de iald.js na ordem é supersedido somente pelas modificações de prazo deste pedido; conferir o novo hash em deadlines_install.json e preservar demais mudanças coordenadas. iOS interno/externo e Android NÃO estão atualizados com a nova interface até novas builds. Confirmação visual da aba Usuários da Central e datas exatas de expiração TestFlight permanecem pendentes. Não encerrar a meta integral por esta entrega parcial.
'''
    rows=[]
    for p in helper.TARGETS:rows.append({'path':str(p),'status':append(p,'IALD_OPERATIONAL_DEADLINES_20260922',note,stamp)})
    p=Path(r'C:\Users\rotol\.codex\AGENTS.md')
    rows.append({'path':str(p),'status':append(p,'IALD_PERSISTENT_EXPIRY_VISIBILITY_20260922',rule,stamp)})
    log=(ROOT/'logs/web-server_20260921_142214_r6.log').read_text(encoding='utf-8',errors='replace')
    result={'at':now.isoformat(),'memories':rows,'claude_key_defined_in_startup':any(x.startswith('[claude]') and 'chave=definida' in x for x in log.splitlines()),'paid_tests_executed':0,'authenticated_visual_check':'pending','mobile_builds':'pending'}
    helper.create(WORK/'deadlines_memory_record.json',json.dumps(result,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'memories_updated':len(rows),'claude_key_defined_in_startup':result['claude_key_defined_in_startup'],'paid_tests_executed':0}))

if __name__=='__main__':main()
