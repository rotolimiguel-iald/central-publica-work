"""Per-request bounded delegation, durable no-repeat journal, no local code execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,threading,uuid
import iald_task_policy as policy

NAMES=frozenset(('create_artifact','delegate_task','execute_python','get_task_capabilities','read_task_artifact'))
ARTIFACT_PAGE_CHARS=3500


def normalize_arguments(name,args):
    """Validate tool arguments and fill effective defaults before identity hashing."""
    required,optional={
        'create_artifact':({'kind','name','payload'},set()),
        'delegate_task':({'objective','role'},{'context'}),
        'execute_python':({'code'},{'data'}),
        'get_task_capabilities':(set(),set()),
        'read_task_artifact':({'artifact_id'},{'offset'}),
    }[name]
    if not required<=args.keys() or args.keys()-required-optional:
        raise ValueError('Argumentos inválidos.')
    normalized=dict(args)
    if name=='delegate_task':
        if args['role'] not in ('implement','analyze'):
            raise ValueError('Etapa inválida.')
        if type(args['objective']) is not str or not 0<len(args['objective'])<=12000:
            raise ValueError('Objetivo inválido.')
        normalized.setdefault('context','')
        if type(normalized['context']) is not str:
            raise ValueError('Contexto inválido.')
    elif name=='execute_python':
        if type(args['code']) is not str or not args['code'].strip():
            raise ValueError('Código inválido.')
        normalized.setdefault('data',{})
        if type(normalized['data']) is not dict:
            raise ValueError('Dados devem ser um objeto JSON.')
    elif name=='create_artifact':
        if any(type(args[key]) is not str or not args[key].strip() for key in ('kind','name')) or type(args['payload']) is not dict:
            raise ValueError('Argumentos de artefato inválidos.')
    elif name=='read_task_artifact':
        if type(args['artifact_id']) is not str or not args['artifact_id']:
            raise ValueError('Identificador inválido.')
        normalized.setdefault('offset',0)
        if type(normalized['offset']) is not int or normalized['offset']<0:
            raise ValueError('Faixa inválida.')
    return normalized

def definition(name,description,props,required=()):
    return dict(type='function',function=dict(name=name,description=description,
        parameters=dict(type='object',properties=props,required=list(required),additionalProperties=False)))

def definitions(artifact_definition):
    return [artifact_definition,
        definition('delegate_task','Delegue uma etapa de implementação ou análise. O JEV escolhe um executor autorizado; sem recursão, sem execução local. Resultado é rascunho para revisão.',
            {'objective':{'type':'string'},'context':{'type':'string'},'role':{'type':'string','enum':['implement','analyze']}},['objective','role']),
        definition('execute_python','Execute Python somente no sandbox remoto Anthropic; entregue código, JSON e evidências reais. Sem acesso ao computador da IALD. Dados devem ser JSON.',
            {'code':{'type':'string'},'data':{'type':'object'}},['code']),
        definition('get_task_capabilities','Consulte capacidades efetivamente integradas e limitações deste piloto.',{}),
        definition('read_task_artifact','Leia até 3500 caracteres por página de um artefato desta conta. Siga next_offset para continuar. Retorna metadata e links antes do texto; renova mobile_url temporário com expires_at. Binários retornam somente metadados e links. Nunca lê caminhos do servidor.',
            {'artifact_id':{'type':'string'},'offset':{'type':'integer','minimum':0}},['artifact_id'])]

class TaskSession:
    def __init__(self,root,owner,store,authorize,delegate,python,artifact_definition):
        if owner!='luiz':raise PermissionError('Piloto de ferramentas restrito ao operador.')
        self.id=uuid.uuid4().hex;self.owner=owner;self.store=store;self.authorize=authorize
        self.delegate=delegate;self.python=python;self.tools=definitions(artifact_definition)
        self.folder=Path(root)/'.iald_runtime/task_runs';self.folder.mkdir(parents=True,exist_ok=True)
        self.path=self.folder/(self.id+'.json');self.steps={};self.results={};self.lock=threading.Lock()
        self.counts={};self.record={'id':self.id,'owner_hash':hashlib.sha256(owner.encode()).hexdigest(),
            'created':datetime.now(timezone.utc).isoformat(),'steps':self.steps,'policy_version':1}
        self._save()

    def _save(self):
        raw=json.dumps(self.record,ensure_ascii=False,indent=2).encode()
        tmp=self.path.with_suffix('.tmp');tmp.write_bytes(raw)
        if tmp.read_bytes()!=raw:raise OSError('Journal write failed')
        os.replace(tmp,self.path)

    def execute(self,name,args):
        if type(name) is not str or name not in NAMES:return {'status':'UNAVAILABLE'}
        if type(args) is not dict:return {'status':'INVALID_ARGUMENTS'}
        try:
            self.authorize('task')
            try:
                args=normalize_arguments(name,args)
                wire=json.dumps([name,args],sort_keys=True,ensure_ascii=False,allow_nan=False).encode()
                if len(wire)>250000:raise ValueError('Pedido de ferramenta excede o limite desta etapa.')
                # Dispatch the same JSON snapshot that defines the identity. Neither
                # caller mutation nor executor mutation changes the original input.
                args=json.loads(wire)[1]
            except (ValueError,TypeError,OverflowError,RecursionError):
                return {'status':'INVALID_ARGUMENTS','notice':'Confira os campos e limites da ferramenta; nenhuma etapa foi iniciada.'}
            ident=hashlib.sha256(wire).hexdigest()
            with self.lock:
                if ident in self.steps:
                    # Only completed reads may run again, to renew an expired ticket.
                    # Started/uncertain reads and all costly steps keep no-repeat semantics.
                    if self.steps[ident]['status']!='returned':
                        return {'status':'PREVIOUS_ATTEMPT_UNCERTAIN','notice':'Não foi repetido.'}
                    if name!='read_task_artifact':
                        return self.results.get(ident,{'status':'PREVIOUS_ATTEMPT_UNCERTAIN','notice':'Não foi repetido.'})
                limits={'delegate_task':3,'execute_python':2,'create_artifact':12,'get_task_capabilities':2,'read_task_artifact':16}
                if self.counts.get(name,0)>=limits[name]:raise ValueError('Número de etapas desta mensagem esgotado; solicite continuação.')
                self.counts[name]=self.counts.get(name,0)+1
                self.steps[ident]={'tool':name,'status':'started','utc':datetime.now(timezone.utc).isoformat()}
                self.results.pop(ident,None)
                self._save()
            if name=='create_artifact':
                result=self.store.create(self.owner,**args)
            elif name=='delegate_task':
                result=self.delegate(args,self.id,self.authorize)
            elif name=='execute_python':
                self.authorize('claude')
                result=self.python(args,self.id,self.authorize)
            elif name=='read_task_artifact':
                result=self._read_artifact(args)
            else:result=policy.capabilities()
            if not isinstance(result,dict):raise ValueError('Resultado de ferramenta inválido.')
            with self.lock:
                self.steps[ident].update(status='returned',result_status=result.get('status',result.get('state','returned')))
                self._save();self.results[ident]=result
            return result
        except Exception as exc:
            # Never expose exception text: SDK errors can contain request bodies.
            if 'ident' in locals() and ident in self.steps:
                with self.lock:
                    self.steps[ident].update(status='failed_or_uncertain',error_type=type(exc).__name__)
                    self._save()
            from iald_task_artifacts import ArtifactError
            notice=str(exc) if isinstance(exc,ArtifactError) else 'A etapa não concluiu. Não houve repetição automática; confira o registro da tarefa.'
            return {'status':'FAILED_OR_UNCERTAIN','notice':notice,'task_id':self.id}

    def _read_artifact(self,args):
        artifact_id,offset=args['artifact_id'],args['offset']
        path,meta=self.store.resolve(self.owner,artifact_id)
        mobile_url=self.store.issue_ticket(self.owner,artifact_id)
        # Read exact expiry from the issued capability; never infer it from a clock.
        _,ticket_meta=self.store.resolve_ticket(artifact_id,mobile_url.rsplit('/',1)[-1])
        metadata={key:meta[key] for key in ('id','filename','mime','sha256','bytes','url')}
        metadata.update(mobile_url=mobile_url,expires_at=ticket_meta['expires_at'])
        result={'status':'METADATA_ONLY','metadata':metadata,'offset':offset,
            'total_chars':None,'next_offset':None,'source_sha256':meta['sha256']}
        if Path(meta['filename']).suffix.lower() not in ('.py','.md','.json','.csv','.txt','.html','.htm'):
            return result
        body=path.read_text(encoding='utf-8')
        end=min(offset+ARTIFACT_PAGE_CHARS,len(body))
        result.update(status='PARTIAL' if end<len(body) else 'COMPLETE_RANGE',
            total_chars=len(body),next_offset=end)
        result['text']=body[offset:end]
        return result
