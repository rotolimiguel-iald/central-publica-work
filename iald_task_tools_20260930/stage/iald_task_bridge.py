"""Bridge the app's verified providers to task tools without sharing host files."""
from pathlib import Path
import hashlib,json,math,time,uuid,threading
import iald_task_policy as policy
from iald_task_session import TaskSession

TASK_RESULT_MAX_CHARS = 24000


def encode_task_result(result):
    """Keep tool JSON intact; oversized results fail visibly, never mid-field."""
    if isinstance(result,str):result=json.loads(result)
    if not isinstance(result,dict):raise ValueError('Invalid task result')
    # References and pagination precede prose, without dropping any fields.
    ordered={key:value for key,value in result.items() if key!='text'}
    if 'text' in result:ordered['text']=result['text']
    raw=json.dumps(ordered,ensure_ascii=False,allow_nan=False,separators=(',',':'))
    if len(raw)>TASK_RESULT_MAX_CHARS:
        raise ValueError('Task result exceeds the context limit; fields were not truncated')
    return raw


class TaskControl:
    """Shared cancellation; release the account only after workers/journals end."""
    def __init__(self):
        self.cancel=threading.Event();self.lock=threading.Lock()
        self.active=0;self.release=None;self.released=False

    def check(self):
        if self.cancel.is_set():raise InterruptedError('Task cancelled')

    def start(self):
        with self.lock:
            self.check();self.active+=1

    def _ready(self):
        if self.release is not None and not self.active and not self.released:
            self.released=True
            return self.release

    def finish(self):
        with self.lock:
            self.active-=1
            callback=self._ready()
        if callback:callback()

    def close(self,release):
        with self.lock:
            self.cancel.set()
            if self.release is None:self.release=release
            callback=self._ready()
        if callback:callback()


class SandboxAccount:
    def __init__(self,guard,cfg,user,ledger):
        self.guard,self.cfg,self.user,self.ledger=guard,cfg,user,ledger
        self.key=None;self.closed=False;self.rates=cfg.precos(cfg.modelo)
    def before(self,input_tokens,max_tokens):
        if self.key or self.closed:raise ValueError('Account already used')
        if type(input_tokens)is not int or type(max_tokens)is not int or min(input_tokens,max_tokens)<1:raise ValueError('Invalid count')
        rates=self.rates
        if len(rates)<3 or any(not math.isfinite(v) or v<0 for v in rates):raise ValueError('Invalid rates')
        # Count the actual wire input and reserve uncached tokens. Container time
        # is a separate conservative hold, never called a measured invoice.
        cap=(input_tokens*max(rates)+max_tokens*rates[2])/1e6+0.025
        limit=self.cfg.cota_global_usd if getattr(self.cfg,'somente_limite_global',False) else self.cfg.cota_operador_usd
        self.key=self.guard.reserve(self.user,self.cfg.modelo,cap,limit,self.cfg.cota_global_usd)
    def settle(self,usage):
        if not self.key or not isinstance(usage,dict):raise ValueError('Missing usage')
        pin,out,cached,created=[usage.get(k,0) for k in ('input_tokens','output_tokens','cache_read_input_tokens','cache_creation_input_tokens')]
        if any(type(v)is not int or v<0 for v in (pin,out,cached,created)):raise ValueError('Invalid usage')
        if 'input_tokens' not in usage or 'output_tokens' not in usage:raise ValueError('Missing usage')
        r=self.rates;cost=(pin*r[0]+cached*r[1]+out*r[2]+created*(r[3] if len(r)>3 else r[0]*1.25))/1e6
        # API reports calls, not billable duration. Keep the container reserve
        # as an explicit estimate until the provider's billing is reconciled.
        self.guard.settle(self.key,amount=cost+0.025);self.key=None
        self.ledger.registrar(self.user,self.cfg.modelo,pin+cached+created,cached,out,cost+0.025,estimado=True)
    def close(self):
        if self.key:self.guard.settle(self.key);self.key=None
        self.closed=True

def make_scope(*,root,user,authorize,options,package,evaluation,providers,router,sandbox_config,client_factory,guard_factory,ledger):
    from iald_task_artifacts import ArtifactStore,TOOL_DEFINITION
    import iald_task_sandbox
    control=TaskControl()
    store=ArtifactStore(root)
    prefix=package().prefix
    if not prefix or 'MEMORIA CANONICA INTEGRAL' in prefix:raise ValueError('Unverified memory')
    memory_sha=hashlib.sha256(prefix.encode()).hexdigest()

    def checked_authorize(provider='task'):
        control.check()
        current=authorize(provider)
        if current is False:raise PermissionError('Task authorization denied')
        control.check()
        return current

    def delegate(args,task_id,auth):
        auth('task')
        candidates=[p for p in options() if p in ('mimo','kimi')]
        # The router chooses only among already authorized text workers.
        if not candidates:raise ValueError('No eligible delegate')
        chosen,receipt=router.choose('Etapa '+args['role']+': '+args['objective'],candidates,worker=True)
        auth(chosen)
        request_text=json.dumps({'objective':args['objective'],'context':args.get('context','')},ensure_ascii=False)
        messages=[{'role':'system','content':prefix+'\nEtapa delegada: produza somente o rascunho solicitado. Não há ferramentas, execução local nem delegação recursiva. Preserve estatutos; não declare código executado.'},
            {'role':'user','content':request_text}]
        flow=evaluation.stream(chosen,messages,[],lambda *a: {'status':'UNAVAILABLE'},memory_sha256=memory_sha,
            account_key=hashlib.sha256((user+':task:'+task_id).encode()).hexdigest(),task_control=control)
        text=[];size=0;done=False;failure=False
        try:
            for frame in flow:
                auth(chosen)
                for line in frame.splitlines():
                    if not line.startswith('data: '):continue
                    body=line[6:]
                    if body=='[DONE]':done=True;continue
                    event=json.loads(body)
                    if event.get('iald_aviso'):failure=True
                    for c in event.get('choices',[]):
                        delta=(c.get('delta') or {}).get('content') or ''
                        if not isinstance(delta,str):raise ValueError('Invalid delegate output')
                        size+=len(delta)
                        if size>300000:raise ValueError('Delegate output exceeds transfer limit')
                        text.append(delta)
        finally:flow.close()
        if not done or failure or not text:raise ValueError('Delegate did not complete')
        whole=''.join(text)
        artifact=store.ingest(user,'rascunho-'+chosen+'.md',whole.encode())
        return {'status':'DRAFT_COMPLETED','provider':chosen,'routing_id':receipt['id'],
            'artifacts':[artifact],'partial':len(whole)>3500,'total_chars':len(whole),'next_offset':min(3500,len(whole)),
            'notice':'Texto gerado, não executado; a IA gestora deve revisar.','text':whole[:3500]}

    def python(args,task_id,auth):
        auth('claude');cfg=sandbox_config()
        account=SandboxAccount(guard_factory(),cfg,user,ledger)
        def sandbox_authorize():
            auth('claude')
            return True
        receipt=iald_task_sandbox.execute(client=client_factory(cfg),model=cfg.modelo,prefix=prefix,
            code=args['code'],data=args.get('data',{}),store=store,owner=user,
            authorize=sandbox_authorize,cancel=control.cancel.is_set,window=200000,accounting=account)
        # Full evidence stays in the immutable receipt; the manager gets references
        # and an explicitly partial excerpt, never a sliced JSON document.
        evidence=json.dumps({key:receipt.get(key,[]) for key in ('commands','results')},
                            ensure_ascii=False,separators=(',',':'))
        result={key:receipt.get(key) for key in ('execution_id','state','success',
            'exact_code_execution_verified','artifacts','receipt_artifact','error',
            'requires_continuation','dispatch_attempted')}
        result.update(evidence_status=receipt.get('evidence_status'),
            execution_excerpt_partial=len(evidence)>2000,execution_excerpt=evidence[:2000])
        return result

    scope=TaskSession(root,user,store,checked_authorize,delegate,python,TOOL_DEFINITION)
    execute=scope.execute
    def execute_tracked(name,args):
        try:control.start()
        except InterruptedError:return {'status':'CANCELLED','notice':'Nenhuma nova etapa iniciada.'}
        try:return execute(name,args)
        finally:control.finish()  # TaskSession persisted its terminal/uncertain state.
    scope.execute=execute_tracked
    scope.control=control
    return scope
