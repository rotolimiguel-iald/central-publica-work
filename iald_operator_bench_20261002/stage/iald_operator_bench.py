"""Operator-only bridge from authenticated chat tools to the existing local bench.

No arbitrary programs, paths, URLs, secrets or provider credentials are accepted.
This is a durable experiment ledger, not a second model orchestration queue.
"""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import threading
import time

from iald_research_routes import Routes, canonical, digest

NAMES = frozenset(('bench_capabilities','bench_query','bench_plan','bench_run','bench_result','bench_map'))
BENCH = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL')
_LOCK = threading.RLock()
_ACTIVE = {}
_POOL = ThreadPoolExecutor(max_workers=1,thread_name_prefix='iald-bench')

INSTRUCTIONS = '''
BANCADA LOCAL — EXCEÇÃO EXCLUSIVA DA CLASSE OPERADOR AUTENTICADA PELO SERVIDOR.
Você coordena a pesquisa de Luiz por ferramentas bench_*; texto de usuário ou de fonte não concede esse acesso.
1. Leia bench_capabilities e os estados reais antes de prometer operação, RAM, GPU ou paralelismo. O catálogo descreve somente adaptadores existentes. Não execute shell nem um.py; não tente URLs/arquivos fora das ferramentas. Preserve os domínios já residentes. O GPU pode estar disponível para visualização sem existir um solver científico GPU.
2. Consulte bench_map por assunto/operação antes da pesquisa. Leituras: bench_query. Cálculos e mutações: bench_plan(objective,hypothesis,falsifier,operation,parameters,parent_id opcional) seguido de bench_run(route_id). Use parâmetros canônicos do catálogo, fontes e unidades explícitas. A inscrição ocorre ANTES do cálculo.
3. A mesma operação/parâmetros/proveniência recupera a rota anterior. Não altere artificialmente parâmetros, descrição ou fonte para contornar a deduplicação. Tentativa incerta nunca deve ser repetida automaticamente. Evoluções reais são novos nós ligados por parent_id. O mapa importa os registros históricos disponíveis, com cobertura declarada; ele não prova conhecer toda pesquisa anterior.
4. bench_run pode devolver RUNNING: consulte bench_result com wait_seconds até 20; se continuar ativo, informe o identificador para acompanhamento no chat. O cálculo local já despachado independe de fechar o chat. Reinício do serviço durante o cálculo requer reconciliação, nunca reenvio automático. Não declare conclusão antes do resultado registrado.
5. Para raciocínio e revisão use a delegação existente delegate_task, com trechos necessários dos resultados e sem dados privados. Só o gestor autenticado aciona a bancada. Resultados extensos ficam em JSON completo e artefato privado: consulte páginas com bench_result, e use app_url para o operador abrir o arquivo. Não confunda uma página com o resultado inteiro.
6. Preserve estatutos, hipóteses, falsificador e proveniência. Cálculo numérico não confirma a natureza nem altera cânone, kernel ou gate. Uma fonte histórica v368 não é atualização automática da memória científica implantada. Falha, recusa, ausência ou cobertura parcial devem aparecer na resposta. Não invente sigma, prova, arquivo, hash ou uso de GPU.
'''

def is_operator(record,user):
    return (user == 'luiz' and type(record) is dict and record.get('admin') is True
            and record.get('classe_usuario') == 'operador' and not record.get('bloqueado',False)
            and not record.get('acesso_bloqueado',False))

def routing_context(record,user):
    if not is_operator(record,user):return None
    return {'role':'operador','capabilities':['local_scientific_bench','resident_RAM','durable_research_map'],
            'bench_families':{'gravitational_waves':['resident strain inspection','conditional ringdown model','registered C6 event view'],
                'cosmology':['DESI BAO background evaluation','conditional V3 model','saved scenarios and comparison exports'],
                'algebra':['identity chain','dephasing'],
                'research_map':['read historical inquiries/corrections','freeze parameters and provenance','reuse recorded routes']},
            'execution':'Select a tool-capable manager. Its bench_capabilities catalog describes 34 current adapters. Delegate reasoning through existing workers; do not grant them host execution.',
            'protocol':'Use bench_capabilities, bench_map, plan then run; actual supported operations are in the catalog.',
            'restrictions':'Fixed local adapters only; no arbitrary execution. No canon ratification or automatic uncertain retry.'}

def _tool(name,description,properties,required=()):
    return {'type':'function','function':{'name':name,'description':description,
        'parameters':{'type':'object','additionalProperties':False,'properties':properties,'required':list(required)}}}

TEXT={'type':'string'}
TOOLS=[
    _tool('bench_capabilities','Read supported bench operations and schemas. Begin here, then query the catalogued status operations.',
          {'section':{'type':'string','default':'overview'}}),
    _tool('bench_query','Read-only bench inspection. Computation or RAM changes require a research plan.',
          {'operation':TEXT,'parameters':{'type':'object'}},('operation','parameters')),
    _tool('bench_plan','Freeze a research route before computing. Identical data/code/operation/parameters reuse its previous route.',
          {'operation':TEXT,'parameters':{'type':'object'},'objective':TEXT,'hypothesis':TEXT,'falsifier':TEXT,
           'parent_id':TEXT},('operation','parameters','objective','hypothesis','falsifier')),
    _tool('bench_run','Dispatch an already inscribed research route once. Returns its state; never automatically resubmits an uncertain attempt.',
          {'route_id':TEXT},('route_id',)),
    _tool('bench_result','Read a route and a page of its complete JSON result. Can wait briefly for active research.',
          {'route_id':TEXT,'offset':{'type':'integer','minimum':0,'default':0},
           'wait_seconds':{'type':'integer','minimum':0,'maximum':20,'default':0}},('route_id',)),
    _tool('bench_map','Search the append-only research map, including available historical bench inscriptions.',
          {'query':TEXT,'offset':{'type':'integer','minimum':0,'default':0},'limit':{'type':'integer','minimum':1,'maximum':30,'default':20}})
]

def _validate(name,args):
    schema=next(x['function']['parameters'] for x in TOOLS if x['function']['name']==name)
    if type(args) is not dict or not set(schema['required']) <= args.keys() or args.keys()-schema['properties'].keys():
        raise ValueError('Invalid tool fields')
    if len(canonical(args).encode())>16000:raise ValueError('Tool arguments too large')
    for key,value in args.items():
        expected=schema['properties'][key]['type']
        if type(value) is not {'string':str,'integer':int,'object':dict}[expected]:raise ValueError('Invalid field type')
        if expected=='string' and (not value.strip() and key!='query' or len(value)>4000):raise ValueError('Invalid text')
        if key=='offset' and not 0<=value<=40*1024**2:raise ValueError('Invalid offset')
        if key=='wait_seconds' and not 0<=value<=20:raise ValueError('Invalid wait')
        if key=='limit' and not 1<=value<=30:raise ValueError('Invalid page size')
    return json.loads(canonical(args))

def _small(value,depth=0):
    """Explicitly partial summary; full scientific JSON is retained separately."""
    if depth>4:return {'summary':'DEPTH_LIMIT','type':type(value).__name__}
    if type(value)is dict:
        items=list(value.items())
        result={k:_small(v,depth+1) for k,v in items[:24]}
        if len(items)>24:result['_omitted_keys']=len(items)-24
        return result
    if type(value)is list:
        return {'count':len(value),'first':[_small(v,depth+1) for v in value[:3]],'partial':len(value)>3}
    if type(value)is str and len(value)>1200:return value[:1200]+' [PARTIAL]'
    return value

class OperatorBench:
    def __init__(self,root,user,authorize,store,catalog=None,bench=BENCH):
        if catalog is None:import iald_bench_catalog as catalog
        self.root=Path(root);self.user=user;self.authorize=authorize;self.store=store;self.catalog=catalog;self.bench=Path(bench)
        self.key=str((self.root/'.iald_runtime/research/map.sqlite3').resolve())

    def guard(self):
        if not is_operator(self.authorize('task'),self.user):raise PermissionError('Operator role required')

    def ledger(self):
        self.guard()
        return Routes(self.key)

    def _artifact(self,name,value):
        raw=canonical(value).encode()
        artifact=self.store.ingest(self.user,name,raw)
        # Do not send short-lived bearer download tokens through model context.
        return {k:v for k,v in artifact.items() if k in ('id','filename','bytes','sha256','url','app_url','mime')}

    def _bounded(self,value,label):
        raw=canonical(value)
        if len(raw)<=14000:return value
        artifact=self._artifact(label+'.json',value)
        envelope={**({k:value[k] for k in ('status','route_id','next_offset') if k in value} if type(value)is dict else {}),
                'coverage':'PARTIAL_SUMMARY_FULL_ARTIFACT','summary':_small(value),'artifact':artifact,
                'notice':'Read the JSON artifact in pages for the full result.'}
        if len(canonical(envelope))>14000:
            envelope['summary']={'omitted':True,'reason':'Full summary exceeds chat transport; read the complete artifact.'}
        if len(canonical(envelope))>20000:raise ValueError('Artifact envelope exceeds transport')
        return envelope

    def execute(self,name,args):
        try:
            self.guard();args=_validate(name,args)
            if name=='bench_capabilities':result=self.catalog.catalog(args.get('section','overview'))
            elif name=='bench_query':
                op=args['operation'];params=self.catalog.normalize(op,args['parameters'])
                if self.catalog.writes(op):raise ValueError('This operation requires plan then run')
                result=self.catalog.request(op,params)
            elif name=='bench_plan':
                op=args['operation'];params=self.catalog.normalize(op,args['parameters'])
                if not self.catalog.writes(op):raise ValueError('Use bench_query for inspection')
                provenance=self.catalog.provenance(op,params)
                ledger=self.ledger();history=ledger.import_history(self.bench)
                matches=ledger.historical_matches(op,params,self.catalog.normalize,provenance)
                exact=next((m for m in matches if m['same_recorded_sources']),None)
                if exact:
                    result={'status':'REUSED_HISTORICAL','route_id':exact['route_id'],'match':exact,
                            'notice':'Existing bench result with the same parameters and recorded source hashes. No computation dispatched; read bench_result.'}
                else:
                    route,reused=ledger.plan(op,params,provenance,args['objective'],args['hypothesis'],args['falsifier'],args.get('parent_id'))
                    result={'status':'REUSED' if reused else 'PLANNED','route_id':route['record']['id'],
                            'route':route,'historical_coverage':history,'historical_candidates':matches,
                            'notice':'Review candidates with matching parameters before running; missing/changed source pins are not proof of an identical experiment.'}
            elif name=='bench_run':result=self.run(args['route_id'])
            elif name=='bench_result':result=self.result(args['route_id'],args.get('offset',0),args.get('wait_seconds',0))
            else:
                ledger=self.ledger();history=ledger.import_history(self.bench)
                result=ledger.search(args.get('query',''),args.get('offset',0),args.get('limit',20));result['history']=history
            self.guard()
            return self._bounded(result,name)
        except PermissionError:
            return {'status':'FORBIDDEN','notice':'A bancada é exclusiva da conta luiz com classe operador ativa.'}
        except Exception as exc:
            # Local errors may contain paths or provider state; do not expose exception text.
            return {'status':'BENCH_REFUSED','error_type':type(exc).__name__,
                    'notice':'A etapa não foi concluída. Confira catálogo, parâmetros e estado da rota; não houve repetição automática.'}

    def run(self,identifier):
        ledger=self.ledger();route=ledger.get(identifier)
        if route['state']!='PLANNED':return self.result(identifier)
        r=route['record'];self.guard()
        current=self.catalog.provenance(r['operation'],r['parameters'])
        if digest(current)!=digest(r['provenance']):
            ledger.stale_unclaimed(identifier)
            return self.result(identifier)
        with _LOCK:
            active=_ACTIVE.get(self.key)
            if active and not active[1].done():
                return {'status':'BENCH_BUSY','route_id':identifier,'active_route_id':active[0],
                        'notice':'A resident research operation is active; this plan has not been dispatched.'}
            self.guard()
            if not ledger.claim(identifier):return self.result(identifier)
            # The durable claim precedes any network request. A process crash leaves uncertainty, not a retry.
            try:future=_POOL.submit(self._work,identifier)
            except Exception:
                ledger.event(identifier,'UNCERTAIN',{'notice':'Worker dispatch did not return a usable handle. No automatic resend.'})
                return self.result(identifier)
            _ACTIVE[self.key]=(identifier,future)
        return {'status':'RUNNING','route_id':identifier,'notice':'Use bench_result to read the durable result.'}

    def _work(self,identifier):
        ledger=Routes(self.key);sent=False;result_recorded=False
        try:
            self.guard();r=ledger.get(identifier)['record']
            if digest(self.catalog.provenance(r['operation'],r['parameters']))!=digest(r['provenance']):
                ledger.event(identifier,'STALE_PLAN',{'notice':'Source generation changed before dispatch.'});return
            self.guard();sent=True
            value=self.catalog.request(r['operation'],r['parameters'])
            # Record all returned evidence before artifact generation or authorization recheck.
            ledger.event(identifier,'RESULT_RECEIVED',{'result':value,'sha256':digest(value)})
            result_recorded=True
            if r['operation']=='universe_load' and type(value)is dict and value.get('status')=='LOADING':
                ledger.event(identifier,'PENDING_BACKEND',{'load_id':value.get('load_id'),'domain':value.get('domain'),'generation':value.get('generation'),
                    'notice':'Loading was accepted, not completed. Follow with bench_result; never repeat POST.'})
                return
            if r['operation']=='universe_load' and (type(value)is not dict or value.get('status') not in ('READY','ALREADY_RESIDENT')):
                ledger.event(identifier,'PARTIAL_OR_FAILED_LOAD',{'notice':'Resident load did not complete. Existing arrays preserved; no reload.'});return
            if type(value)is dict and (value.get('error') or value.get('status') in ('error','ERROR','FAILED','UNAVAILABLE','REFUSED')):
                ledger.event(identifier,'FAILED',{'notice':'The bench returned a failure. The full receipt is preserved.'});return
            self.guard()
            after=self.catalog.provenance(r['operation'],r['parameters'])
            source_changed=digest(after)!=digest(r['provenance'])
            # Loading a previously empty domain is expected to change its generation.
            expected_change=r['operation'] in ('universe_load','cosmos_status')
            ledger.event(identifier,'SOURCE_CHECK',{'after_sha256':digest(after),'changed':source_changed,
                         'expected_load_transition':source_changed and expected_change})
            if source_changed and not expected_change:
                ledger.event(identifier,'RESULT_SOURCE_CHANGED',{'notice':'Sources/generation changed during execution. Evidence retained; not a result under the frozen plan.'})
                return
            artifact=self._artifact('TGL_research_'+identifier+'.json',{'plan':r,'result':value})
            ledger.event(identifier,'COMPLETED',{'artifact':artifact,'result_sha256':digest(value),
                'scope':'Bench calculation/operation only; no canon ratification or empirical confirmation.'})
        except PermissionError:
            ledger.event(identifier,'RESULT_RESTRICTED' if result_recorded else ('UNCERTAIN' if sent else 'REVOKED'),
                         {'notice':'Operator authorization changed. No automatic repeat.'})
        except Exception as exc:
            ledger.event(identifier,'RESULT_STORED_ARTIFACT_FAILED' if result_recorded else ('UNCERTAIN' if sent else 'FAILED_BEFORE_DISPATCH'),
                         {'error_type':type(exc).__name__,'notice':'No automatic repeat. Check the recorded evidence.'})

    def _reconcile_load(self,ledger,route,wait_seconds=0):
        """Poll only the accepted load. Never start, replace or release a domain."""
        identifier=route['record']['id'];body=route['events'][-1]['body']
        load_id=body.get('load_id')
        if type(load_id)is not str or not load_id:return route
        deadline=time.monotonic()+wait_seconds
        while True:
            self.guard();current=self.catalog.request('universe_status',{})
            if any(current.get(key)!=body.get(key) for key in ('load_id','domain','generation')):
                ledger.event(identifier,'UNCERTAIN',{'notice':'Resident load identity changed; no automatic retry.'});break
            status=current.get('status')
            if status=='LOADING':
                if time.monotonic()>=deadline:break
                time.sleep(min(1,max(0,deadline-time.monotonic())));continue
            self.guard()
            ledger.event(identifier,'RESULT_RECEIVED',{'result':current,'sha256':digest(current)})
            if status=='READY' and current.get('loaded_files',0)>0 and current.get('loaded_files')==current.get('total_files') and not current.get('errors'):
                artifact=self._artifact('TGL_research_'+identifier+'.json',{'plan':route['record'],'result':current})
                ledger.event(identifier,'COMPLETED',{'artifact':artifact,'result_sha256':digest(current),
                    'scope':'Resident loading complete; not scientific confirmation.'})
            else:ledger.event(identifier,'PARTIAL_OR_FAILED_LOAD',{'notice':'Load did not complete. Existing arrays preserved; no reload.'})
            break
        return ledger.get(identifier)

    def result(self,identifier,offset=0,wait_seconds=0):
        self.guard()
        with _LOCK:active=_ACTIVE.get(self.key)
        if active and active[0]==identifier and wait_seconds:
            deadline=time.monotonic()+wait_seconds
            while not active[1].done() and time.monotonic()<deadline:
                self.guard();time.sleep(min(.2,max(0,deadline-time.monotonic())))
        ledger=self.ledger();route=ledger.get(identifier)
        if route['state']=='PENDING_BACKEND':
            with _LOCK:
                route=ledger.get(identifier)
                if route['state']=='PENDING_BACKEND':route=self._reconcile_load(ledger,route,wait_seconds)
        state=route['state']
        result={'status':state,'route_id':identifier,'plan':route['record'],
                'events':[{'created':e['created'],'state':e['state']} for e in route['events']]}
        if state=='DISPATCHING':
            result['status']='RUNNING' if active and active[0]==identifier and not active[1].done() else 'UNCERTAIN'
            result['notice']='Never resubmit this route automatically; a process restart may have interrupted receipt collection.'
        received=next((e['body'] for e in reversed(route['events']) if e['state']=='RESULT_RECEIVED'),None)
        if state=='IMPORTED_HISTORICAL':
            original=route['record']['original']
            if 'result_json' in original:
                value=json.loads(original['result_json']);received={'result':value,'sha256':digest(value)}
                # Avoid duplicating the full original in the plan and paginated result.
                result['plan']={k:v for k,v in route['record'].items() if k!='original'}
        if received:
            raw=canonical(received['result'])
            result.update(result_sha256=received['sha256'],total_chars=len(raw),offset=offset,
                          text=raw[offset:offset+6000],next_offset=offset+6000 if offset+6000<len(raw) else None,
                          coverage='PAGE' if offset or len(raw)>6000 else 'FULL_RESULT')
        last=route['events'][-1]['body'] if route['events'] else {}
        if 'artifact' in last:result['artifact']=last['artifact']
        self.guard();return result

def attach(scope,root,user,authorize):
    record=authorize('task')
    if not is_operator(record,user):return scope
    if getattr(scope,'operator_bench',None):return scope
    bridge=OperatorBench(root,user,authorize,scope.store)
    previous=scope.execute
    def execute(name,args):
        if name not in NAMES:return previous(name,args)
        control=getattr(scope,'control',None)
        if control:
            try:control.start()
            except Exception:return {'status':'CANCELLED','notice':'A conversa já foi encerrada; nenhuma nova pesquisa foi iniciada.'}
        try:return bridge.execute(name,args)
        finally:
            if control:control.finish()
    scope.execute=execute
    scope.tools=list(scope.tools)+TOOLS
    scope.instructions=INSTRUCTIONS
    scope.operator_bench=bridge
    return scope
