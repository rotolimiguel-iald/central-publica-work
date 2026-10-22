from pathlib import Path
import ast, hashlib, json, re

ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent
STAGE=WORK/'stage'
STAGE.mkdir(exist_ok=True)
def sha(x):return hashlib.sha256(x).hexdigest()
def save(p,raw):
    if p.exists():assert p.read_bytes()==raw,p
    else:
        with p.open('xb') as f:f.write(raw)

pins={}
for name in ['iald_app_providers.py','iald_web_server.py']:
    raw=(ROOT/name).read_bytes();s=raw.decode('utf-8');pins[name]=sha(raw)
    if name=='iald_app_providers.py':
        s=s.replace('Operator-only app evaluation transports.', 'Account-scoped app transports.')
        start=s.index('def allowed(');end=s.index('\n\ndef adapter',start)
        s=s[:start]+'''FAMILY_ACCOUNTS = frozenset(('alanacaroline', 'liana'))


def allowed(record, username, provider=None):
    # Server-authenticated approved account only. Pending requests live elsewhere.
    if (not isinstance(username, str) or not username or not isinstance(record, dict)
            or not record or record.get('bloqueado') or record.get('acesso_bloqueado')):
        return False
    if provider is None:  # Legacy callers must never broaden a provider grant.
        return username == 'luiz' and record.get('plano') != 'gratuito'
    if provider not in MODELS:
        return False
    return provider == 'mimo' or username in FAMILY_ACCOUNTS or username == 'luiz'
'''+s[end:]
        s=s.replace("    if not allowed(record, username):\n        return []\n",'')
        s=s.replace('    for key, spec in MODELS.items():\n        reason', '    for key, spec in MODELS.items():\n        if not allowed(record, username, key):\n            continue\n        reason')
        s=s.replace("' · avaliação pessoal'", "' · memória TGL'")
        s=s.replace('Neste modo de avaliação pessoal, a IALD envia à ', 'Neste modo, a IALD envia à ')
        s=s.replace('A avaliação destes modelos aceita somente texto;', 'Este modelo aceita somente texto;')
        s=s.replace('        self.lock = threading.Lock()', '        self.lock = threading.Lock()\n        self.active_accounts = set()')
        s=s.replace('memory_sha256, http_post=None):', "memory_sha256, http_post=None, account_key='operator'):")
        s=s.replace('''        """One active evaluation. No fallback/retry after any provider dispatch."""
        if not self.lock.acquire(blocking=False):''','''        """One active request per account. No fallback/retry after dispatch."""
        with self.lock:
            busy = account_key in self.active_accounts
            if not busy:
                self.active_accounts.add(account_key)
        if busy:''')
        s=s.replace('Uma avaliação já está em andamento.', 'Uma resposta desta conta já está em andamento.')
        s=s.replace("                record['error_type'] = type(exc).__name__", "                record['error_type'] = type(exc).__name__\n                record['error_code'] = getattr(exc, 'code', 'transport_or_unclassified')\n                if isinstance(exc, json.JSONDecodeError): record['error_code'] = 'invalid_provider_json'")
        s=s.replace('A avaliação não concluiu.', 'A resposta não concluiu.')
        s=s.replace("                    self.lock.release()", "                    with self.lock:\n                        self.active_accounts.discard(account_key)")
        s=s.replace('''            content, reasoning, calls, usage, finish, done = '', '', {}, None, None, False''','''            content, reasoning, calls, usage, finish, done = '', '', {}, None, None, False
            record['protocol'] = dict(round=round_no, chunks=0, tool_calls=0,
                finish_reason=None, http_status=response.status_code)''')
        s=s.replace("                    chunk = json.loads(text)", "                    chunk = json.loads(text)\n                    record['protocol']['chunks'] += 1")
        s=s.replace("                            item = calls.setdefault", "                            record['protocol']['tool_calls'] = max(record['protocol']['tool_calls'], idx+1)\n                            item = calls.setdefault")
        s=s.replace("                        if choice.get('finish_reason') is not None: finish = choice['finish_reason']", "                        if choice.get('finish_reason') is not None:\n                            finish = choice['finish_reason']\n                            record['protocol']['finish_reason'] = finish if finish in ('stop','tool_calls','length','content_filter','insufficient_system_resource') else 'unknown'")
        codes={'Resposta ou modelo inesperado.':'unexpected_provider_model','Múltiplas respostas inesperadas.':'unexpected_choices','Ferramentas excessivas.':'tool_batch_limit','Argumentos excessivos.':'tool_arguments_limit','Fluxo incompleto.':'incomplete_stream','Conclusão inválida.':'invalid_completion','Ciclo de ferramentas não concluído.':'tool_round_limit','Ferramenta não permitida.':'tool_not_allowed'}
        for msg,code in codes.items():
            s=s.replace('raise ValueError('+repr(msg)+')', 'raise ProtocolError('+repr(code)+')')
        # Codes are fixed program constants; never raw exception/provider text.
        s=s.replace('\ndef wire_messages(', '''\nclass ProtocolError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def wire_messages(''')
    else:
        changes={
          'app_providers.allowed(registro, user)':'app_providers.allowed(registro, user, motor)',
          'app_providers.allowed(registro, username)':'app_providers.allowed(registro, username, motor)',
          'app_providers.allowed(conta, username)':None,
          'app_providers.allowed(registro, conta)':'app_providers.allowed(registro, conta, motor)'}
        for old,new in changes.items():
            if new:s=s.replace(old,new)
        s=s.replace('alvo in app_providers.MODELS and not app_providers.allowed(conta, username)', 'alvo in app_providers.MODELS and not app_providers.allowed(conta, username, alvo)')
        s=s.replace('option in app_providers.MODELS and not app_providers.allowed(conta, username)', 'option in app_providers.MODELS and not app_providers.allowed(conta, username, option)')
        s=s.replace('Avaliação liberada somente para a conta de Luiz.', 'Modelo não liberado para esta conta.')
        s=s.replace('Avaliação liberada somente para Luiz.', 'Modelo não liberado para esta conta.')
        s=s.replace("memory_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest())", "memory_sha256=hashlib.sha256(prefix.encode('utf-8')).hexdigest(),\n        account_key=hashlib.sha256(user.encode('utf-8')).hexdigest())")
        assert not re.search(r'app_providers.allowed\([^\n]+username\)',s)
    ast.parse(s)
    save(STAGE/name,s.encode('utf-8'))
save(WORK/'pins.json',json.dumps(pins,indent=2).encode())
print(json.dumps({'staged':list(pins),'production_changed':False}))
