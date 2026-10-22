"""Scoped stateless chat/page envelope, stdlib only. No HTTP/auth/provider execution.

Versioned engineering control, NOT a luminidic atom or a canonical ACOM format.
Embedding server must authenticate/CSRF-check first and revalidate generation.
"""
import base64,binascii,hashlib,json,math,re,zlib

PROTOCOL='iald-byte-envelope/1'
CODEC='deflate-base64'
QUERY='iald-byte-envelope-v1'
REQUEST_LIMIT=20*1024*1024
PAGE_LIMIT=2*(16*1024*1024)+262144
WIRE_LIMIT=20*1024*1024
MAX_DEPTH=128
MAX_NODES=500000
SHA=re.compile(r'[a-f0-9]{64}\Z')
ID=re.compile(r'[A-Za-z0-9_-]{1,100}\Z')
ENVELOPE_KEYS={'protocol','codec','scope','binding','raw_bytes','sha256','data'}

class WireError(ValueError):
    def __init__(self,code,status=400):
        self.code,self.status=code,status
        self.no_dispatch_this_submission=True
        super().__init__(code)

def need(ok,code,status=400):
    if not ok:raise WireError(code,status)
def dump(value):return json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
def digest(raw):return hashlib.sha256(raw).hexdigest()
def _pairs(items):
    result={}
    for k,v in items:
        need(k not in result,'duplicate_json_key');result[k]=v
    return result
def _float(value):
    n=float(value);need(math.isfinite(n),'nonfinite_json');return n
def strict_json(raw,limit):
    need(type(raw)is bytes and len(raw)<=limit,'decoded_limit',413)
    try:
        value=json.loads(raw.decode('utf-8'),object_pairs_hook=_pairs,parse_float=_float,
            parse_constant=lambda x:(_ for _ in ()).throw(WireError('nonfinite_json')))
    except (UnicodeError,ValueError,RecursionError) as e:
        if isinstance(e,WireError):raise
        raise WireError('invalid_utf8_json') from e
    stack=[(value,0)];count=0
    while stack:
        obj,depth=stack.pop();count+=1
        need(depth<=MAX_DEPTH and count<=MAX_NODES,'json_structure_limit',413)
        if isinstance(obj,dict):stack.extend((v,depth+1) for v in obj.values())
        elif isinstance(obj,list):stack.extend((v,depth+1) for v in obj)
    return value
def valid_scope(scope):return type(scope)is str and 0<len(scope)<=256 and all(ord(c)>=32 for c in scope)
def binding_check(binding):
    need(type(binding)is dict,'invalid_binding')
    if binding.get('kind')=='request':
        need(set(binding)=={'kind','request_id','conversation'},'invalid_binding')
        need(type(binding['request_id'])is str and ID.fullmatch(binding['request_id']) and type(binding['conversation'])is str and 0<len(binding['conversation'])<=64 and ID.fullmatch(binding['conversation']),'invalid_binding')
    else:
        need(set(binding)=={'kind','job_id','after'} and binding.get('kind')=='page','invalid_binding')
        need(type(binding['job_id'])is str and ID.fullmatch(binding['job_id']) and type(binding['after'])is int and 0<=binding['after']<=2**53-1,'invalid_binding')
def capabilities():
    return dict(protocol=PROTOCOL,codec=CODEC,query=QUERY,request_decoded_bytes=REQUEST_LIMIT,
        page_decoded_bytes=PAGE_LIMIT,wire_bytes=WIRE_LIMIT,bases=False,min_savings_bytes=1024,min_savings_ratio=.05,
        max_json_depth=MAX_DEPTH,max_json_nodes=MAX_NODES)
def encode_envelope(raw,scope,binding,limit):
    need(valid_scope(scope),'invalid_scope');binding_check(binding);strict_json(raw,limit)
    return dict(protocol=PROTOCOL,codec=CODEC,scope=scope,binding=binding,raw_bytes=len(raw),
        sha256=digest(raw),data=base64.b64encode(zlib.compress(raw,6)).decode('ascii'))
def decode_envelope(envelope,scope,binding,limit):
    need(valid_scope(scope),'invalid_scope');binding_check(binding)
    need(type(envelope)is dict and set(envelope)==ENVELOPE_KEYS,'invalid_envelope')
    need(envelope['protocol']==PROTOCOL and envelope['codec']==CODEC,'unsupported_codec',415)
    binding_check(envelope['binding'])
    need(envelope['scope']==scope and envelope['binding']==binding,'scope_or_binding_mismatch',409)
    n=envelope['raw_bytes'];need(type(n)is int and 0<=n<=limit,'decoded_limit',413)
    need(type(envelope['sha256'])is str and SHA.fullmatch(envelope['sha256']),'invalid_hash')
    text=envelope['data'];need(type(text)is str and len(text)<=4*((WIRE_LIMIT+2)//3),'wire_limit',413)
    try:wire=base64.b64decode(text,validate=True)
    except (ValueError,binascii.Error) as e:raise WireError('invalid_base64') from e
    need(len(wire)<=WIRE_LIMIT and base64.b64encode(wire).decode('ascii')==text,'invalid_base64_or_wire_limit',413)
    decoder=zlib.decompressobj()
    try:raw=decoder.decompress(wire,n+1)
    except zlib.error as e:raise WireError('invalid_deflate') from e
    need(len(raw)==n and decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,'deflate_length_or_trailing')
    need(digest(raw)==envelope['sha256'],'hash_mismatch')
    strict_json(raw,limit)
    return raw
def worth(raw,packet):return len(packet)<=WIRE_LIMIT and len(raw)-len(packet)>=max(1024,math.ceil(len(raw)*.05))
def request_binding(value):
    need(type(value)is dict,'request_object_required')
    binding=dict(kind='request',request_id=value.get('request_id'),conversation=value.get('iald_conv'))
    binding_check(binding);return binding
def request_candidate(raw,scope):
    obj=strict_json(raw,REQUEST_LIMIT);need(type(obj)is dict,'request_object_required');need(obj.get('account')==scope,'account_changed',409)
    binding=request_binding(obj)
    packet=dump(dict(account=scope,request_id=obj['request_id'],iald_conv=obj['iald_conv'],
        iald_transport=encode_envelope(raw,scope,binding,REQUEST_LIMIT)))
    return packet if worth(raw,packet) else raw
def decode_request(wire,scope):
    # Only use for opted-in enveloped requests. Legacy path must remain untouched.
    outer=strict_json(wire,WIRE_LIMIT)
    need(type(outer)is dict and set(outer)=={'account','request_id','iald_conv','iald_transport'},'invalid_request_wrapper')
    need(outer['account']==scope,'account_changed',409)
    binding=request_binding(outer);raw=decode_envelope(outer['iald_transport'],scope,binding,REQUEST_LIMIT)
    obj=strict_json(raw,REQUEST_LIMIT)
    need(type(obj)is dict and obj.get('account')==scope and request_binding(obj)==binding,'inner_outer_mismatch',409)
    need('iald_transport' not in obj,'nested_envelope')
    return raw,obj
def page_candidate(raw,scope,binding):
    packet=dump({'iald_transport':encode_envelope(raw,scope,binding,PAGE_LIMIT)})
    return packet if worth(raw,packet) else raw
def decode_page(wire,scope,binding):
    obj=strict_json(wire,PAGE_LIMIT)
    if type(obj)is dict and 'iald_transport' in obj:
        need(set(obj)=={'iald_transport'} and len(wire)<=WIRE_LIMIT,'invalid_page_wrapper')
        return decode_envelope(obj['iald_transport'],scope,binding,PAGE_LIMIT)
    return wire
