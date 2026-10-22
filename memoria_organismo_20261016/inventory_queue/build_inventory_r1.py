"""Static, local inventory; exact mission read only. No provider or runtime import."""
from pathlib import Path
import ast
import datetime as dt
import hashlib
import importlib.util
import json
import os
import uuid

WORK = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
QUEUE = Path(r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923')
MOD = QUEUE / 'iald_orchestrator'
CORE = Path(r'C:\IALD\MEMORIA_IALD')
BENCH = Path(r'C:\IALD\Bancada_Um')
ACTOR = {'id': 'codex-mission-memory-review', 'kind': 'agent'}

def pin(path):
    p = Path(path)
    assert p.name.lower() not in {'iald_stack_v7.py', '.env'}
    assert not p.name.lower().startswith('iald_psion_state')
    raw = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}

def save(path, raw):
    assert not path.exists(), 'Preserve prior inventory'
    tmp = path.with_name(path.name + '.tmp_' + uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)

def anchor(path, start, end, statement, needle):
    p = Path(path)
    lines = p.read_text(encoding='utf-8-sig').splitlines()
    section = '\n'.join(lines[start-1:end])
    assert needle in section, (p, start, needle)
    return {'path': str(p), 'line_start': start, 'line_end': end,
            'section_sha256_lf': hashlib.sha256(section.encode('utf-8')).hexdigest(),
            'statute': 'REAL_STATIC_SOURCE', 'observation': statement}

anchors = [
    anchor(MOD/'operational_memory.py', 14, 42,
        'Fila já usa biblioteca e estado ACOM comuns; scope da fila é IALD/operator e contexto deriva de request_id. Isso não equivale automaticamente à identidade de cada sessão/app.', 'IALD:operator:queue:'),
    anchor(MOD/'operational_memory.py', 45, 93,
        'Outbox na mesma transação da fila; evento idempotente; flush serial e retry de CAS apenas da escrita local. Resultados são candidatos DECLARADO.', 'memory_outbox'),
    anchor(MOD/'operational_memory.py', 116, 178,
        'Projeção verifica original e restrições; pacote verifica hashes e presença de revisão. verify_packet não consulta revisão atual de MissionController.', 'def verify_packet'),
    anchor(MOD/'runtime.py', 25, 69,
        'Runtime prepara tabelas e recuperação; instanciar para inventário não seria uma consulta estritamente sem efeitos. memory_context_id e memory_version já existem.', 'memory_context_id'),
    anchor(MOD/'runtime.py', 170, 237,
        'Admissão conserva request_id, original, constraints e contexto, recusando reuso divergente. São pontos de vínculo autenticado da Activity.', 'memory_context_id'),
    anchor(MOD/'runtime.py', 260, 291,
        'Transição da tarefa e evento de memória são gravados juntos. Falha no flush fica visível; não converte resultado concluído em autorização para repetir.', 'memory_version'),
    anchor(MOD/'runtime.py', 306, 358,
        'Um dono do drain e até três lanes de provedores; execução persistida sem dono impede novo despacho e exige reconciliação. Preservar essa proteção de resultado incerto.', 'running/uncertain'),
    anchor(MOD/'runtime.py', 360, 433,
        'prepared/dispatch_intent antecedem a chamada; binding científico e pacote ACOM são preparados. Falta vínculo automático a requisito/epoch/preflight de MissionController nesta fronteira.', 'providers.execute'),
    anchor(MOD/'runtime.py', 435, 447,
        'Uso e attempt returned são persistidos antes do follow-up. result_ready e conteúdo são gravados no ramo não cancelado; projetar novamente alimenta shadow, sem comparar epoch de missão. Não foi provada aqui preservação integral do retorno no ramo cancelado.', 'if not cancel.is_set()'),
    anchor(MOD/'coordination.py', 36, 111,
        'Coordenação preserva ID/pedido/restrições e inclui memória operacional no prompt de despacho; job e execução compartilham contexto ACOM.', 'memory_context_id'),
    anchor(MOD/'coordination.py', 117, 141,
        'Mudança de etapa usa estado esperado da coordenação, transação e outbox. Não é o CAS de critério/epoch de missão.', 'def _change'),
    anchor(MOD/'coordination.py', 180, 245,
        'Assistência Work opcional e síntese exigem executor result_ready; completed é encerramento da coordenação, sem aceite independente de requisito.', 'result_ready'),
    anchor(MOD/'providers.py', 181, 223,
        'Executor exige pacote operacional e executor obrigatório antes do transporte; resultado tem estatuto de execução, não verificação factual.', 'verify_packet'),
    anchor(MOD/'scientific_binding.py', 45, 99,
        'Vínculo científico já confere identidade original, pins e fontes antes do despacho; autoridade é uma fronteira privilegiada explícita. Activity deve preservar generation/constraints, sem substituir essa camada.', 'Pins alone NEVER authenticate a human'),
    anchor(MOD/'transport.py', 19, 72,
        'Fila única retoma trabalhos existentes, markers de handoff e request_id; receipt salva estado local. Não criar fila/heartbeat adicional.', 'def submit'),
    anchor(QUEUE/'transport_cli.py', 1, 28,
        'CLI existente oferece submit/next/get/action e execução direta; não recebe vínculo Activity autenticado. Não executado neste inventário.', 'submit_execution'),
    anchor(QUEUE/'mcp_server.py', 1, 101,
        'MCP instancia Runtime/Coordination e registra ferramentas de missão separadas. Exposição de ferramentas não integra automaticamente o fluxo submit/get/action.', 'register_tools'),
    anchor(MOD/'mission_bridge.py', 10, 55,
        'Quatro ferramentas atuais chamam CLI instalado; repassam referência/ator do chamador local e max_chars. O wrapper público não pode expor esse repasse como autoridade concedida ao modelo.', 'iald_mission_handoff'),
    anchor(MOD/'jev.py', 67, 85,
        'JEV recebe estado ACOM tipado junto da memória científica; esta entrada é consultiva e não prova satisfação de Activity.', 'operational_memory'),
    anchor(MOD/'jev_decisions.py', 67, 98,
        'Contrato de perguntas estruturadas é CONSULTATIVE_ONLY e usa a projeção operacional; preservar esta separação de autoridade.', 'CONSULTATIVE_ONLY'),
    anchor(CORE/'lib'/'iald_memory'/'mission.py', 53, 64,
        'Evidência de missão é pin de arquivo local com hash conferido. A API lê o caminho; autenticação e resolução de source_id devem ocorrer antes desta função em consumidores de modelo.', 'guard.read_checked'),
    anchor(CORE/'lib'/'iald_memory'/'mission.py', 224, 270,
        'Projeção conserva handles desconhecidos e exige ausência de pendências para parar; só índice de terminais e esquema estrito do tracker legado são compactados. Fatos obrigatórios ainda podem exceder orçamento.', 'terminal_handle_states'),
    anchor(CORE/'lib'/'iald_memory'/'mission.py', 287, 336,
        'MissionController já valida revisão/hash, posse/epoch/prazo, hold e dependências. Preflight não forma transação atômica com chamada externa futura.', 'lease_epoch_mismatch'),
    anchor(CORE/'lib'/'iald_memory'/'mission.py', 397, 409,
        'submit vai para review_pending; accept exige revisor distinto e revalida evidências/dependências. Retorno do executor não satisfaz requisito por si.', 'independent_reviewer_required'),
    anchor(CORE/'mission_cli.py', 14, 38,
        'CLI de missão resolve referência exata e âncora, usa o mesmo MemoryStore, confere saída; get é estado atual e não recuperação de revisão histórica.', 'reference_anchor_mismatch'),
    anchor(CORE/'session_memory.py', 216, 246,
        'Protocolo de sessão projeta MemoryStore e grava transition CAS; não chama MissionController para essa projeção.', 'store.project'),
    anchor(CORE/'session_hook.py', 9, 39,
        'Hook opcional resolve adapter/session_id/cwd exatos e recusa herança de contexto irmão; chama projeto de sessão ACOM. Ativação no host não foi conferida neste inventário.', 'No inheritance'),
    anchor(BENCH/'mcp_um.py', 18, 32,
        'Proxy da Bancada encaminha X-Cliente derivado do ambiente; timeout/erro retorna mensagem, sem Activity/request_id ou intenção durável no proxy. Rótulo não autentica titular.', 'X-Cliente'),
    anchor(BENCH/'mcp_um.py', 168, 188,
        'Proxy expõe rodada, consulta tarefa e livro. A existência da ferramenta não torna admissível a execução: rota HTTP atual recusa rodada histórica.', 'gw_tarefa'),
    anchor(BENCH/'um_bancada.py', 127, 141,
        'Bancada já lista requisições e tarefas ativas para ociosidade local. Não é critério de satisfação da missão.', 'active_requests'),
    anchor(BENCH/'um_bancada.py', 194, 204,
        'Resposta revalida manifesto canônico e recusa se mudou durante operação. É precedente aproveitável para revalidar a Activity adicionalmente.', 'CONTRACT_CHANGED_DURING_OPERATION'),
    anchor(BENCH/'um_bancada.py', 330, 360,
        'HTTP limita corpo e valida JSON/contrato canônico; X-Cliente é texto recebido, não identidade autenticada de missão.', 'X-Cliente'),
    anchor(BENCH/'um_bancada.py', 375, 414,
        'Despacho chama operações científicas existentes; /api/gw/rodar recusa EXPLICIT_RITE_DISPATCH_REQUIRED. Wrapper não deve remover a recusa ou mudar cálculos.', 'EXPLICIT_RITE_DISPATCH_REQUIRED'),
    anchor(BENCH/'bancada'/'regua.py', 73, 111,
        'Livro existente registra cliente/operação/família/hash/estatuto. É proveniência científica, sem request_id/contexto/epoch nem chave idempotente de chamada.', 'resultado_sha'),
]

gaps = [
    {'id':'Q1', 'statute':'DERIVED_FROM_STATIC_SOURCE', 'title':'Identidade de atividade ainda não percorre o caminho real',
     'detail':'Contexto ACOM por pedido existe; mission tools são separadas. Falta vínculo autenticado Activity→contexto/requisito/epoch→coordination job→task/provider/worker. Scope operator legado não pode ser silenciosamente reinterpretado como qualquer principal de app/sessão.'},
    {'id':'Q2', 'statute':'DERIVED_FROM_STATIC_SOURCE', 'title':'Snapshot íntegro não significa mandato ainda vigente',
     'detail':'Hashes do pacote previnem mutação do snapshot, mas não comparam missão viva no despacho/retorno. Mudança durante chamada exige guardar resultado e marcar conflito/reconciliação, sem reenvio ou aceite automático.'},
    {'id':'Q3', 'statute':'DERIVED_FROM_STATIC_SOURCE', 'title':'Conclusão técnica e aceite têm semânticas diferentes',
     'detail':'result_ready/completed/síntese retornada descrevem execução. Não autorizam satisfied. Estado failed_or_interrupted não prova terminal seguro; vocabulários da fila e Bancada precisam de tradução explícita, conservando unknown e conflitos visíveis.'},
    {'id':'Q4', 'statute':'DERIVED_FROM_STATIC_SOURCE', 'title':'Fronteira privilegiada de evidência/ator precisa permanecer no servidor',
     'detail':'evidence_pin lê arquivo local e mission action confia em ator local agent. O consumidor deve obter principal/ator de autenticação e resolver source_id com autorização no ledger; modelo não escolhe caminho local, scope, ator revisor ou lease.'},
    {'id':'Q5', 'statute':'DERIVED_FROM_STATIC_SOURCE', 'title':'Sessões e Bancada ainda não acompanham o controlador em todas as entradas',
     'detail':'Hook de sessão é ACOM e opcional; Bancada tem livro e manifesto canônico, mas proxy não propaga Activity. Integração adicional deve preservar dados e guardas existentes. Fonte em disco não prova código carregado nos processos.'},
]

proposal = {
 'statute':'DECLARADO_PROPOSTA_NAO_IMPLEMENTADA',
 'architecture':'ActivityRuntime único sobre MemoryStore/MissionController existentes; sem segundo banco de memória e sem nova fila/heartbeat.',
 'identity':'Admissão recebe request_id e source_id emitidos pelo servidor. Principal, casa, ator e escopo vêm de autenticação/registro local confiável. Vínculo persistido inclui context_id, objective_sha256, task_id, task_epoch, dispatch_revision/state_sha256/projection_sha256, request_id/job_id e no_repeat. Guardar identidades específicas de coordenação e executor, não substituí-las.',
 'source_boundary':'Para inscrição/evidência, resolver IDs do ledger dentro da atividade autenticada. Se MissionController exigir pin de arquivo, materializar recibo imutável em diretório controlado pelo servidor e piná-lo após escrita atômica. Não aceitar caminhos fornecidos por modelo; rejeitar traversal, UNC, symlink/alias escapando raiz e source_id de outro titular antes de ler bytes. O texto/referência original permanece íntegro e rastreável.',
 'criteria':'begin define requisito execution com contrato íntegro e a ligação ao pedido humano. Terminar execution pode produzir submit DECLARADO; nenhuma saída de modelo gera accept. Critérios substantivos da missão e políticas de revisão não podem ser substituídos pelo critério mínimo de transporte.',
 'enqueue':'Na transação já existente, persistir binding da atividade e outbox/handle específicos do request, junto de intenção estável. Reuso do mesmo evento com payload distinto recusa. Identidades históricas de pedidos não são reescritas para migrar.',
 'before_dispatch':'Resolver binding servidor; flush local e project fresco; preflight com dono real ou delegação explicitamente autorizada pelo wrapper, sem simular ator de sessão. Guardar o recibo antes da chamada. Uma revisão concorrente antes da admissão exige nova conciliação local. Não repetir o efeito externo para resolver CAS.',
 'during_and_return':'Intent/remote_id conservados. Ao retorno, persistir conteúdo/estatuto/uso/recibo uma vez antes de qualquer síntese, revalidar atividade/epoch/pins e conciliar contra revisão atual. Resultado pode ser válido como observação da execução anterior e inaplicável ao critério atual. Cancelamento/hold/invalidation durante chamada não autorizam descartar silenciosamente conteúdo recebido nem repetir chamada incerta.',
 'progress_and_stop':'Progresso e handles por delta no mesmo ACOM; preservar todos os demais handles. returned/failed comprovado podem encerrar o handle técnico; require review_pending/satisfied separado. Estados desconhecidos ou contraditórios continuam pendentes. Não aplicar compactação E3 de builds a fatos gerais, decisões, ordens ou resultados de modelo.',
 'bench':'Wrapper de Activity no chamador/orquestração em torno da chamada real, com autorização e intenção antes do HTTP e custódia após resposta. Reutilizar corpo/rota científica, guarda canônica e livro; resultado incerto no transporte exige reconciliação, não reenvio. Não reiniciar motor/GPU nem abrir dados para validar infraestrutura.',
 'sessions':'CLI/MCP/sessões usam a mesma resolução de identidade e projeção; hooks opcionais só após binding/trust explícito. Não herdar última tarefa ou tratar contexto citado como autorização.',
 'cost':'Transições materiais por delta; não inserir fatos duplicados a cada poll/token. Cobrar orçamento de projeção antes de envio e preservar recusa explícita quando obrigatório exceder capacidade. Medir chamadas ao store, bytes, latência e tamanho do journal em testes isolados; nenhum ganho de custo medido aqui.'
}

tests = [
 ('T1','Vinculação real','Admitir pela CLI/MCP em cópia, acompanhar Coordination→Runtime→provider falso; mesmos context_id/original/task_epoch e IDs em todos os recibos; contador remoto=1.'),
 ('T2','Isolamento e autoridade','Forjar principal/scope/actor/lease/source_id de outra atividade, caminho absoluto de modelo/traversal/UNC/symlink; recusar antes de leitura/rede e não promover candidate.'),
 ('T3','Concorrência antes de rede','Invalidar requisito/hold/mutar pin após snapshot e antes do despacho; preflight recusa sem executar. CAS stale não pode provocar novo request_id.'),
 ('T4','Concorrência durante chamada','Executor falso bloqueado; alterar requisito/epoch/hold; liberar resposta. Persistir resultado uma vez, marcar obsolescência/reconciliação e manter revisão nova; zero autoaccept/reenvio.'),
 ('T5','Crash/recovery','Interromper antes/após outbox, após intent e após retorno antes de submit; recuperar mesmo evento/ID sem repetir efeito incerto; colisão de payload explicitamente recusada.'),
 ('T6','Cancelamento e erro posterior','Retorno simultâneo a cancelamento e falha de shadow/síntese: conferir conteúdo/uso/evidência recebidos duráveis e estatuto separado; erro de memória não apaga execução nem a torna retryable.'),
 ('T7','Estados e parada','Mapear result_ready, completed, failed comprovado, interrupted, paused_by_rite, pronta/falhou e desconhecidos; conflito status/phase continua pendente; completed técnico não satisfaz requisito.'),
 ('T8','Aceite independente','Modelo só candidate/DECLARADO; submit→review_pending; mesmo autor não aceita; revisor autenticado distinto usa evidência autorizada/CAS fresco; nenhuma promoção científica.'),
 ('T9','Compatibilidade científica','generation, required_provider, max_calls, original request_id/job_id e fontes pinadas permanecem; pending/uncertain legado não reabre nem ganha fallback.'),
 ('T10','Capacidade e projeção','Muito progresso terminal em índices, handles ativos/unknown íntegros; decisões/ordens/erratas intactas; overflow obrigatório recusa; get atual confere revisão/hash e histórico usa journal.'),
 ('T11','Sessões e processos','Recuperar em processo novo via CLI/MCP/hook mock com mesma referência; sessão errada/cwd divergente recusa; conferir versão carregada em vez de presumir a partir do arquivo.'),
 ('T12','Bancada sem ciência','Transport HTTP falso em cópia; preflight/intent/response pós-check, mudança de manifesto/Activity e timeout; nenhum import de motor, acesso ao lago, cálculo ou reinício.'),
 ('T13','Custo e não duplicação','Contar transições por etapa material, tamanho de evento/projeção e latência em store privado; polls não geram registros redundantes; worker/heartbeat únicos.'),
]

deployment = {
 'statute':'DECLARADO_PLANO_DE_SUPERFICIES_NAO_AUTORIZACAO_DE_INSTALACAO',
 'writes_needed_if_proposal_approved':[
  'Core: adicionar ActivityRuntime e testes sobre a biblioteca existente; API de inscrição/pin de fonte controlada pelo servidor. Não duplicar store.',
  'Fila: operational_memory.py, runtime.py e coordination.py nos pontos anotados; extensão aditiva dos registros/outbox existentes para binding da Activity. transport.py/transport_cli.py e mcp_server.py expõem IDs autorizados, não evidência/caminho arbitrário de modelo.',
  'Sessões: adapter CLI/MCP/hook opcional conforme contrato consolidado; conservar exatos bindings e recibos legados. Mudança de instruções/memórias só pela coordenação responsável.',
  'Bancada: preferir adapter externo de Activity em torno do cliente HTTP. Assim mcp_um.py/um_bancada.py/cálculos residentes podem permanecer byte a byte. Se chamada direta ao MCP precisar cobertura, atualizar apenas o proxy autorizado e testar isoladamente.',
  'Testes/manifesto/backup de bytes e pins dos destinos afetados, revisão independente e plano de rollback antes da instalação.'
 ],
 'activation':[
  'CLI lançado em processo novo lê os módulos atuais; um MCP/worker longo já iniciado não se atualiza por trocar o arquivo.',
  'Verificar se o worker é persistente e sua identidade; suspender novas admissões, conciliar handles e ociosidade antes de substituí-lo. Não matar chamada incerta nem reiniciar para repetir.',
  'Recarga do MCP que importa Runtime só depois do plano seguro; não duplicar heartbeat/fila. Não declare instalado/ativo pela simples importação em teste.',
  'Bancada residente/GPU: nenhum reinício indispensável para wrapper externo. Reiniciar só o proxy se sua implementação for alterada, com todas as chamadas conciliadas.',
  'App/nativa/holografia têm inventários de outras frentes: este parecer não conclui seus destinos, reinícios ou cobertura.'
 ],
 'performed':'Nenhuma escrita em produção, instalação, reinício, chamada de provedor, cálculo científico, leitura de credencial ou consulta ao conteúdo dos arquivos confidenciais.'
}

initial_path = WORK/'receipts'/'20261016T223025_962429Z_inventory_queue_initial.receipt.json'
initial = json.loads(initial_path.read_bytes())['result']['projection']
spec = importlib.util.spec_from_file_location('organism_inventory_mission_io', WORK/'mission_io.py')
io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(io)
current, final_path = io.call('mission_cli.py', {
    'operation':'project','reference':str(WORK/'SESSION_REFERENCE.json'),
    'actor':ACTOR,'max_chars':125000}, 'inventory_queue_final')
projection = current['projection']
assert projection['context_id'] == initial['context_id']
assert projection['scope'] == initial['scope']
assert projection['objective_sha256'] == initial['objective_sha256']
def criteria(p):
    return {x['id']:{k:x[k] for k in ['criterion','depends_on']} for x in p['active']+p['settled']}
assert criteria(projection) == criteria(initial)

source_paths = {Path(a['path']) for a in anchors}
source_paths.update(WORK/n for n in ['OPERADOR_VERBATIM.txt','REQUIREMENTS_R1.json','NOS_VIVO_QUERY.json','SESSION_REFERENCE.json','mission_io.py'])
source_paths.update([CORE/'README.md',CORE/'MISSION_PROTOCOL.md',BENCH/'README.md',Path(__file__)])
test_catalog = []
for name in ['test_coordination.py','test_optional_work.py','test_transport.py']:
    p=QUEUE/name
    source_paths.add(p)
    tree=ast.parse(p.read_text(encoding='utf-8-sig'))
    test_catalog.append({'path':str(p),'statute':'SOURCE_PRESENT_NOT_EXECUTED',
      'tests':[{'name':n.name,'line':n.lineno} for n in ast.walk(tree)
               if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test_')]})
report = {
 'schema':'iald-organism-inventory-queue/v1',
 'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'author':ACTOR,'unit':'F9.MEMORIA_ORGANISMO_20261016','requirement':'I',
 'verdict':'INVENTORY_COMPLETE_FOR_DELEGATED_FRONT_NO_ACCEPT',
 'requirement_satisfied':False,
 'scope':'Fila/coordenação/provedores/JEV da fila, CLI/MCP e sessões; Bancada apenas por fonte. Inventário e proposta, sem implementação ou revisão final do requisito I.',
 'reference':pin(WORK/'SESSION_REFERENCE.json'),
 'synchronization':{'initial':pin(initial_path),'initial_revision':initial['revision'],
     'final':pin(final_path),'final_revision':projection['revision'],
     'context_id':projection['context_id'],'scope':projection['scope'],
     'state_sha256':projection['state_sha256'],
     'objective_and_all_requirement_criteria_unchanged':True,
     'I_status':next(x['status'] for x in projection['active']+projection['settled'] if x['id']=='I'),
     'actions_performed':['project own exact reference only'],
     'no_mission_transition_or_accept':True},
 'measurements':{'kind':'STATIC_SOURCE_AND_EXACT_REFERENCE_READ',
     'source_file_count':len(source_paths),'anchor_count':len(anchors),
     'tests_executed':0,'provider_calls':0,'bench_calls':0,'production_writes':0,
     'observations':'Pins e âncoras verificados por script; testes listados são propostas ou presença na fonte, sem alegação de execução.'},
 'anchors':anchors,'gaps':gaps,'activity_wrapper_proposal':proposal,
 'test_plan':[{'id':i,'title':title,'expected':expect,'statute':'PROPOSED_NOT_RUN'} for i,title,expect in tests],
 'existing_test_sources':test_catalog,'deployment_surface_assessment':deployment,
 'limitations':[
   'Leitura estática não confirma versão carregada em MCP/worker/Bancada ou ativação de hooks.',
   'Nenhuma fila/banco de produção foi instanciado para listar jobs; estados remotos e resultados reais não foram consultados.',
   'Originais científicos, kernel, gate, cálculos, arquivos confidenciais e credenciais permaneceram intocados.',
   'ACOM é continuidade auditável; não demonstra memória nos pesos, ganho cognitivo ou eliminação de alucinação.',
   'Decisões de implantação e aceite de I exigem consolidar app/nativa/holografia e revisão cruzada futura.'
 ],
 'source_pins':[pin(p) for p in sorted(source_paths,key=lambda p:str(p).casefold())]
}
json_path=OUT/'QUEUE_SESSIONS_BANCADA_INVENTORY_R1.json'
save(json_path,(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8'))
lines=[
 'INVENTÁRIO FILA / SESSÕES / BANCADA — R1',
 f"[REAL] Autor: {ACTOR['id']}. Unidade F9.MEMORIA_ORGANISMO_20261016; requisito I, sem aceite.",
 f"[REAL] Referência exata: {WORK/'SESSION_REFERENCE.json'}",
 f"[REAL] project próprio: revisão {initial['revision']} → {projection['revision']}; identidade, original e todos critérios/dependências preservados.",
 f"[REAL] {len(source_paths)} arquivos pinados, {len(anchors)} âncoras. Zero testes executados/provedores/Bancada/reinícios/escritas de produção.",
 '', 'BASE REAPROVEITÁVEL',
 'ACOM/outbox/IDs de fila e candidatos DECLARADO já existem. MissionController usa o mesmo store, com CAS/posse/epoch/revisão independente; as quatro ferramentas MCP são uma entrada separada.',
 'Bancada já tem livro de tentativas, ociosidade local e revalidação do manifesto canônico antes/depois. Esses controles são preservados.',
 '', 'LACUNAS E PROPOSTAS']
for g in gaps:lines.extend([g['id']+' [DERIVED] '+g['title'],g['detail']])
lines.extend(['','CONTRATO PROPOSTO [DECLARADO]',proposal['architecture'],proposal['identity'],proposal['source_boundary'],proposal['criteria'],proposal['before_dispatch'],proposal['during_and_return'],proposal['bench'],proposal['progress_and_stop'], '', 'ESCRITAS / ATIVAÇÃO NECESSÁRIAS SE APROVADAS [DECLARADO]'])
lines.extend(deployment['writes_needed_if_proposal_approved']+deployment['activation'])
lines.extend(['','TESTES PROPOSTOS, NÃO EXECUTADOS'])
for i,title,expect in tests:lines.append(i+' '+title+': '+expect)
lines.extend(['','ÂNCORAS CONFERIDAS'])
for a in anchors:lines.append(f"{a['path']}:{a['line_start']}-{a['line_end']} — {a['observation']}")
lines.extend(['','PINS (bytes lidos por script)'])
for p in report['source_pins']:lines.append(f"{p['sha256']} {p['bytes']} bytes {p['path']}")
lines.extend(['','RECIBO FINAL',str(final_path),'JSON '+str(json_path),'SHA256 JSON '+pin(json_path)['sha256'],'','LIMITES']+report['limitations'])
txt_path=OUT/'QUEUE_SESSIONS_BANCADA_INVENTORY_R1.txt'
save(txt_path,('\n'.join(lines)+'\n').encode('utf-8'))
print(json.dumps({'report':pin(json_path),'text':pin(txt_path),
 'revision':projection['revision'],'source_file_count':len(source_paths),
 'anchor_count':len(anchors),'criteria_unchanged':True},ensure_ascii=False,indent=2))
