"""Record this server delivery additively, with immediate byte backups."""
from pathlib import Path
from datetime import datetime
import hashlib,json,os,sys
W=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
M=W.parent/'iald_memory_refresh_20260930'
sys.path.insert(0,str(ROOT))
import iald_auto_router as router
stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
previous=json.loads((W.parent/'iald_app_models_20260930/delivery.json').read_bytes())
installed=json.loads((W/'installed_reviewed.json').read_bytes())
probe=json.loads((W/'deepseek_probe.json').read_bytes())
scientific=json.loads((M/'local_candidate_v377/validation.json').read_bytes())
cost=sum(c['cost_estimate_usd'] for c in probe['records'][0]['calls'])
marker='IALD_PUBLIC_MIMO_FAMILY_JEV_PILOT_20260930'
for name,entry in installed['files'].items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==entry['sha256']
report={'at':datetime.now().astimezone().isoformat(),'status':'SERVER_DELIVERY_VERIFIED_WITH_EXPLICIT_PENDING_ITEMS',
    'installed':installed,'tests':{'passed':57,'real_provider_calls':'one new DeepSeek date/time test, two rounds; no replay of failed user conversations'},
    'deepseek_probe':probe,'deepseek_cost_estimate_usd':cost,
    'access':{'approved_accounts':['openai','mimo','claude-haiku when its readiness gates pass'],
      'alanacaroline':['nativa','openai','claude-haiku','mimo','kimi','deepseek'],
      'liana':['nativa','openai','claude-haiku','mimo','kimi','deepseek'],
      'sonnet':'luiz only','automatic':'luiz only; NOT ACTIVE pending successful credential validation'},
    'mimo_public_budget':'same configured Haiku public daily/group/global values, separate MiMo spending ledger; luiz unchanged',
    'jev':{'pilot_available':router.available(),'last_receipt':router.report()[:1],
       'pending':'User created/copied replacement key; local authenticated credential form is open; user must paste/save'},
    'memory':[],
    'scientific':{'active':'v368','candidate':'v377','status':scientific['status'],
       'candidate_validation':str(M/'local_candidate_v377/validation.json'),
       'public_head_last_observed':'6fc6a0824f7fa3f88896b44d545a0ffefbf05e58',
       'public_version_last_observed':'v376','automation':'not created; explicit approval pending after auto-review rejection'},
    'availability':{'web':'server restarted and reachable; model selector observed; installed hashes verified',
       'ios_internal':'server features apply to existing 4.1 (25); no client change or new binary',
       'ios_external':'same existing 4.1 (25); no new invitation or binary required',
       'android':'server features apply to existing 4.1 (22); no new binary',
       'google_play':'previous account/DUNS blocker unchanged; not published here',
       'invite':previous['ios']['invite'],'android_download':previous['android']['download']}}
assert not report['jev']['pilot_available'],'Re-read new activation before recording stale pending state'
note=f"""

## 30/09/2026 — MiMo público, acesso familiar e piloto JEV

<!-- {marker} -->

[INPUT — substitui a restrição pessoal anterior] Operador autorizou MiMo para todos os usuários aprovados junto com ChatGPT. Para alanacaroline e liana, todos os motores de conversa integrados exceto Sonnet; automático JEV somente luiz durante o piloto. MiMo público usa os tetos públicos já configurados para Haiku, por resposta expressa; a conta luiz mantém sua configuração. Não conceder administração nem promover automaticamente outro usuário ao piloto.

[REAL — implantado e verificado] Seis módulos instalados com backups de bytes e verificação contra alteração concorrente; somente processo web reiniciado pelo supervisor existente. MiMo público; Kimi/DeepSeek para luiz e as duas contas familiares; Haiku e Nativa mantêm suas regras. Matriz das três contas conferida sem divulgar senha/contato. Cada provedor exige seu próprio consentimento. 57 testes aprovados, incluindo reservas SQLite concorrentes e ausência de envio quando recusado. Revisão independente local identificou e motivou correções de cancelamento após cabeçalhos e exclusão por conta durante roteamento/resposta. Não há nova chamada paga nesses testes.

[REAL — orçamento] PublicAccount reutiliza SpendingGuard, com reserva antes de cada chamada MiMo pública, valores diário/grupo/global obtidos da configuração Haiku já carregada, banco próprio .iald_runtime/app_evaluation/public_spend.sqlite3. Herda os VALORES, sem somar gastos MiMo ao saldo Anthropic. Entrada conservadora por bytes UTF-8 e saída máxima; consumo final liquida a reserva; falta de uso/cancelamento mantém o teto. Não reduz silenciosamente o kernel. luiz não recebe novo teto. Não alterados .env, credenciais, registros de usuários ou limites da fila científica.

[REAL — DeepSeek] Novo teste expressamente autorizado até US$0,25, com kernel v5/core/cluster v368 sem Atlas privado, concluiu get_current_datetime e a resposta em duas chamadas; custo estimado US${cost:.9f}, duração 6,138s. Conexão/ferramenta verificadas; isto NÃO reproduz nem explica definitivamente as duas falhas complexas anteriores sem diagnóstico. Novo conector registra códigos e estágio sem texto/segredo; recebe até 32 ferramentas no protocolo, executa até quatro por rodada e devolve resultado explícito para as demais. Nenhuma repetição automática de chamada incerta.

[REAL/OPEN — JEV] Piloto implementado como escolha estruturada TypeSafe jev-1.13.0: última mensagem textual mais trecho público verificado (até 8 mil caracteres), modelos autorizados e consentidos; executor recebe seu pacote fixo completo. Não decide prova/gate, não transmite anexos/Atlas privado/identidade da conta ao roteador. Sonnet só luiz; DeepSeek e Nativa ainda fora da escolha automática do piloto. Baixa confiança usa MiMo/OpenAI autorizado ANTES de gerar, sem fallback depois do envio. Trava por conta abrange escolha e resposta. Interface e envio exigem recibo de conexão válido. Primeiro teste recusado HTTP403 por autenticação; chave guardada não corresponde à ativa observada no console. Operador criou/cop iou uma substituta; formulário local autenticado /admin/agi/orquestracao/jev aberto para ele salvar. Ainda NÃO ativo; não anunciar JEV funcionando. Após salvar, validar conexão por teste novo identificado e o contrato de escolha; nunca repetir o registro recusado como se fosse a mesma chamada.

[REAL/OPEN — v377] Rodada local encerrada RITO_RC=0, FAIL_CLOSED_SELFTEST_PASSED; hashes dos sete artefatos científicos copiados conferem com selo. Extração AST do kernel, sem executar um.py; {scientific['lean_files_hash_matched']} fontes Lean conferem com relatório, {scientific['reported_terms']} declarações registradas, somente axiomas permitidos. Candidato e cluster derivados em {M}/local_candidate_v377. Não é nova compilação, confirmação física ou implantação. Memória ativa permanece v368; pedido é ativar diretamente v377, nunca v376. Último HEAD público conferido ainda v376. Falta publicação correspondente, revisão dos escopos novos, empacotamento/contagem Haiku real com núcleo >=180 mil e reserva dinâmica, validação conjunta e ativação atômica. A revisão automática recusou automação horária persistente por exigir autorização específica; pergunta pendente. Não foi criado monitor nem fila duplicada.

[DISPONIBILIDADE] Web verificada após reinício; iOS interno/externo usa 4.1 (25), Android 4.1 (22), sem alteração de cliente nesta entrega. Recursos são de servidor; nenhum binário novo necessário. Link TestFlight existente {previous['ios']['invite']}; Android {previous['android']['download']}. Google Play continua com pendência anterior de cadastro/DUNS. Instalação física de terceiros não verificada nesta entrega. Alertas, custos e prazos operacionais continuam na administração, não no chat. Evidência: {W}/delivery.json; backups e hashes em installed_reviewed.json. Nenhum original científico, cânone, kernel formal ou gate foi modificado.
""".replace('cop iou','copiou')

def atomic_append(path,addition):
    old=path.read_bytes();assert marker.encode() not in old
    backup=Path(str(path)+'.bak_'+stamp)
    with backup.open('xb') as f:f.write(old)
    assert backup.read_bytes()==old
    raw=old+addition.encode('utf-8');assert len(raw)>len(old)
    temp=Path(str(path)+'.tmp_'+stamp)
    with temp.open('xb') as f:f.write(raw)
    assert temp.read_bytes()==raw and path.read_bytes()==old
    os.replace(temp,path);assert path.read_bytes()==raw
    return {'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(raw).hexdigest()}
for record in previous['memory']:
    report['memory'].append(atomic_append(Path(record['path']),note))
path=W/'delivery.json';assert not path.exists();raw=json.dumps(report,ensure_ascii=False,indent=2).encode()
temp=path.with_suffix('.tmp');temp.write_bytes(raw);assert temp.read_bytes()==raw;temp.replace(path)
print(json.dumps({'delivery':str(path),'memories':len(report['memory']),'status':report['status']},ensure_ascii=False))
