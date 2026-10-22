"""Isolated byte-lossless reference/block transport; stdlib; no HTTP/auth/model adapter.

legacy_app_acom1_block layout reused from app patents/acom_codec.py, without NumPy,
tensor transforms or quantization. Decoder limits are enforced BEFORE expansion.
Context is trusted embedding-server data, NEVER authenticated by a wire header.
"""
from dataclasses import dataclass
from pathlib import Path
import hashlib,json,os,re,sqlite3,struct,tempfile,zlib

BLOCK=32768
MAX_OBJECT=8*1024*1024
MAX_HEADER=2048
MAX_FRAMES=(MAX_OBJECT//BLOCK)+2
MAX_WIRE=MAX_OBJECT+MAX_FRAMES*(MAX_HEADER+4)
MAGIC=b'ACOM1\x00'
SHA=re.compile(r'[0-9a-f]{64}\Z')
ID=re.compile(r'[A-Za-z0-9_-]{1,100}\Z')
PROTOCOL='iald-signal-blocks/1'
BLOCK_CODEC='legacy_app_acom1_block'

class Refusal(ValueError):pass
class MissingBase(Refusal):pass
class Conflict(Refusal):pass
def need(ok,reason):
    if not ok:raise Refusal(reason)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def exact(value,keys):need(type(value)is dict and set(value)==set(keys),'invalid_fields')
def integer(v,low,high):return type(v)is int and low<=v<=high

@dataclass(frozen=True)
class Context:
    principal:str
    generation:str
    conversation:str
    # Test adapter decisions. These booleans are NOT an authentication protocol.
    authenticated:bool=True
    csrf_valid:bool=True
    @property
    def key(self):return sha(canonical([self.principal,self.generation,self.conversation]))
    def authorize(self):
        need(self.authenticated is True and self.csrf_valid is True,'unauthorized_or_csrf')
        need(all(type(v)is str and 0<len(v)<=128 for v in (self.principal,self.generation,self.conversation)),'invalid_scope')

def acom1(raw):
    need(type(raw)is bytes and len(raw)<=BLOCK,'block_limit')
    return MAGIC+struct.pack('<QI',len(raw),zlib.crc32(raw)&0xffffffff)+hashlib.sha256(raw).digest()+zlib.compress(raw,6)

def unacom1(wire):
    need(type(wire)is bytes and 50<=len(wire)<=BLOCK+128 and wire[:6]==MAGIC,'bad_acom1')
    n,crc=struct.unpack('<QI',wire[6:18]);need(n<=BLOCK,'inflated_block_limit')
    decoder=zlib.decompressobj()
    try:raw=decoder.decompress(wire[50:],n+1)
    except zlib.error as exc:raise Refusal('corrupt_deflate') from exc
    need(len(raw)==n and decoder.eof and not decoder.unconsumed_tail and not decoder.unused_data,'incomplete_or_excess_deflate')
    need(zlib.crc32(raw)&0xffffffff==crc and hashlib.sha256(raw).digest()==wire[18:50],'acom1_integrity')
    return raw

def pack(header,payload=b''):
    encoded=canonical(header);need(len(encoded)<=MAX_HEADER,'header_limit')
    return struct.pack('!I',len(encoded))+encoded+payload

class Reader:
    """Bounded adapter for network chunks (caller must request <= BLOCK+4096)."""
    def __init__(self,chunks):self.chunks=iter(chunks);self.buf=bytearray();self.wire=0;self.peak=0
    def read(self,n):
        need(integer(n,0,BLOCK+4096),'read_limit')
        while len(self.buf)<n:
            try:part=next(self.chunks)
            except StopIteration:break
            need(type(part)is bytes and 0<len(part)<=BLOCK+4096,'source_chunk_limit')
            self.wire+=len(part);need(self.wire<=MAX_WIRE,'wire_limit')
            self.buf.extend(part);self.peak=max(self.peak,len(self.buf))
        raw=bytes(self.buf[:n]);del self.buf[:n];return raw
    def exact(self,n):
        raw=self.read(n);need(len(raw)==n,'truncated_frame');return raw
    def header(self):
        n=struct.unpack('!I',self.exact(4))[0];need(1<=n<=MAX_HEADER,'header_limit')
        raw=self.exact(n)
        def pairs(items):
            out={}
            for k,v in items:
                need(k not in out,'duplicate_json_key');out[k]=v
            return out
        try:value=json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(Refusal('nonfinite_json')))
        except (ValueError,UnicodeDecodeError) as e:raise Refusal('invalid_header_json') from e
        need(type(value)is dict,'header_object_required');return value

def encode(ctx,request_id,kind,chunks,*,known=None,declared_sha=None,declared_bytes=None):
    ctx.authorize();need(ID.fullmatch(request_id) and kind in ('query','attachment','result','event-stream'),'invalid_identity')
    need(declared_sha is None or type(declared_sha)is str and SHA.fullmatch(declared_sha),'invalid_declared_hash')
    need(declared_bytes is None or integer(declared_bytes,0,MAX_OBJECT),'invalid_declared_size')
    if known is not None:
        exact(known,('scope','root','blocks'));need(known['scope']==ctx.key,'known_scope_mismatch')
        need(type(known['root'])is str and SHA.fullmatch(known['root']) and type(known['blocks'])is list and len(known['blocks'])<=MAX_FRAMES,'invalid_known_state')
    hashes=set(known['blocks']) if known else set()
    yield pack(dict(t='begin',v=PROTOCOL,scope=ctx.key,id=request_id,kind=kind,
        base=known['root'] if known else None,sha=declared_sha,bytes=declared_bytes))
    total=0;hasher=hashlib.sha256();blocks=[]
    for i,raw in enumerate(chunks):
        need(type(raw)is bytes and 0<len(raw)<=BLOCK and i<MAX_FRAMES-2,'block_limit')
        total+=len(raw);need(total<=MAX_OBJECT,'object_limit');hasher.update(raw);digest=sha(raw)
        payload=b'';codec='ref'
        if digest not in hashes:
            compressed=acom1(raw)
            codec,payload=(BLOCK_CODEC,compressed) if len(compressed)<len(raw) else ('raw',raw)
        yield pack(dict(t='block',n=i,offset=total-len(raw),sha=digest,bytes=len(raw),codec=codec,wire=len(payload)),payload)
        blocks.append([digest,len(raw)])
    digest=hasher.hexdigest()
    need(declared_sha in (None,digest) and declared_bytes in (None,total),'source_differs_from_descriptor')
    manifest=dict(scope=ctx.key,sha=digest,bytes=total,blocks=blocks)
    yield pack(dict(t='end',n=len(blocks),bytes=total,sha=digest,root=sha(canonical(manifest))))

def slices(raw):
    for i in range(0,len(raw),BLOCK):yield raw[i:i+BLOCK]

class Store:
    """Scoped content store + durable transport ledger; no provider execution here.

    Single-process prototype. No encryption-at-rest, quotas/GC, multiworker locks
    or server authentication implementation: existing app must supply those.
    """
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(self.root/'transport.sqlite3')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS objects(scope TEXT,root TEXT,manifest BLOB,path TEXT,PRIMARY KEY(scope,root));
          CREATE TABLE IF NOT EXISTS requests(scope TEXT,id TEXT,kind TEXT,identity TEXT,sha TEXT,root TEXT,receipt BLOB,PRIMARY KEY(scope,id,kind));
        ''')
    def close(self):self.db.close()
    def _path(self,ctx,kind,digest):
        need(type(digest)is str and SHA.fullmatch(digest),'invalid_hash')
        return self.root/ctx.key/kind/digest
    def _put(self,ctx,path,raw):
        # Single-process local recovery only; never dispatch a provider.
        ctx.authorize()
        need(type(raw)is bytes and len(raw)<=BLOCK,'block_limit')
        expected=self.root.resolve()/ctx.key/'blocks'/sha(raw)
        path=Path(path)
        need(path.absolute()==expected and path.resolve()==expected,'block_scope_path')
        path.parent.mkdir(parents=True,exist_ok=True)
        tmp=path.with_name(path.name+'.tmp')
        need(not tmp.is_symlink() and tmp.resolve()==tmp.absolute(),'temp_scope_path')
        def valid(file):
            need(file.is_file() and file.stat().st_size==len(raw),'local_content_size')
            data=file.read_bytes()
            need(sha(data)==path.name and data==raw,'local_content_corrupt')
        if path.exists():
            valid(path)
            if tmp.exists():
                valid(tmp)
                tmp.unlink()
            return
        if tmp.exists():
            valid(tmp)  # Conflicting orphan remains intact for diagnosis.
        else:
            with tmp.open('xb') as out:
                out.write(raw);out.flush();os.fsync(out.fileno())
            valid(tmp)
        os.rename(tmp,path)
        valid(path)
    def offer(self,ctx,root):
        ctx.authorize();need(type(root)is str and SHA.fullmatch(root),'invalid_base')
        row=self.db.execute('SELECT manifest FROM objects WHERE scope=? AND root=?',(ctx.key,root)).fetchone()
        if row is None:raise MissingBase('base_missing_no_dispatch')
        raw=bytes(row[0]);need(sha(raw)==root,'manifest_corrupt')
        manifest=json.loads(raw);need(manifest['scope']==ctx.key,'manifest_scope')
        return dict(scope=ctx.key,root=root,blocks=[h for h,n in manifest['blocks']])
    def receive(self,ctx,chunks,*,on_block=None,require_eof=True):
        ctx.authorize() # BEFORE header, cache queries, path or body I/O.
        reader=Reader(chunks);begin=reader.header()
        exact(begin,('t','v','scope','id','kind','base','sha','bytes'))
        need(begin['t']=='begin' and begin['v']==PROTOCOL and begin['scope']==ctx.key,'scope_or_protocol')
        need(type(begin['id'])is str and ID.fullmatch(begin['id']) and begin['kind'] in ('query','attachment','result','event-stream'),'invalid_identity')
        need(begin['sha'] is None or type(begin['sha'])is str and SHA.fullmatch(begin['sha']),'invalid_declared_hash')
        need(begin['bytes'] is None or integer(begin['bytes'],0,MAX_OBJECT),'invalid_declared_size')
        # Cache choice is transport-only: same logical request can repair a missing
        # base cold ONLY while no completed request exists and before any dispatch.
        identity=sha(canonical({k:v for k,v in begin.items() if k!='base'}))
        old=self.db.execute('SELECT identity,sha,root,receipt FROM requests WHERE scope=? AND id=? AND kind=?',(ctx.key,begin['id'],begin['kind'])).fetchone()
        if old is not None and old[0]!=identity:raise Conflict('request_descriptor_conflict')
        allowed=set(self.offer(ctx,begin['base'])['blocks']) if begin['base'] is not None else set()
        pending=self.root/ctx.key/'pending';pending.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(dir=pending);temp=Path(name);total=0;hasher=hashlib.sha256();blocks=[]
        try:
            with os.fdopen(fd,'wb') as output:
                for index in range(MAX_FRAMES):
                    h=reader.header()
                    if h.get('t')=='end':
                        exact(h,('t','n','bytes','sha','root'))
                        need(type(h['n'])is int and h['n']==len(blocks) and type(h['bytes'])is int and h['bytes']==total,'end_count')
                        digest=hasher.hexdigest();need(h['sha']==digest,'object_hash')
                        need(begin['sha'] in (None,digest) and begin['bytes'] in (None,total),'declared_object_mismatch')
                        manifest=dict(scope=ctx.key,sha=digest,bytes=total,blocks=blocks);manifest_bytes=canonical(manifest);root=sha(manifest_bytes)
                        need(h['root']==root,'manifest_root')
                        if require_eof:need(reader.read(1)==b'','trailing_frames')
                        if old is not None:
                            if old[1]!=digest or old[2]!=root:raise Conflict('request_replay_payload_conflict')
                            result=json.loads(old[3]);result.update(replayed=True,dispatch_allowed=False,reader_peak=reader.peak)
                            return result
                        output.flush();os.fsync(output.fileno());break
                    exact(h,('t','n','offset','sha','bytes','codec','wire'))
                    need(h['t']=='block' and type(h['n'])is int and h['n']==len(blocks) and type(h['offset'])is int and h['offset']==total,'block_sequence')
                    need(integer(h['bytes'],1,BLOCK) and integer(h['wire'],0,BLOCK+128) and type(h['sha'])is str and SHA.fullmatch(h['sha']),'block_limits')
                    need(total+h['bytes']<=MAX_OBJECT,'object_limit')
                    if h['codec']=='ref':
                        need(h['wire']==0 and h['sha'] in allowed,'unnegotiated_reference')
                        path=self._path(ctx,'blocks',h['sha'])
                        if not path.exists():raise MissingBase('block_missing_no_dispatch')
                        need(path.stat().st_size<=BLOCK,'cached_block_limit');raw=path.read_bytes()
                    else:
                        need(h['codec'] in ('raw',BLOCK_CODEC),'unknown_codec');wire=reader.exact(h['wire'])
                        raw=wire if h['codec']=='raw' else unacom1(wire)
                    need(len(raw)==h['bytes'] and sha(raw)==h['sha'],'block_hash')
                    output.write(raw);hasher.update(raw);blocks.append([h['sha'],len(raw)]);total+=len(raw)
                    if on_block is not None and old is None:on_block(raw,len(blocks)-1) # Verified but PROVISIONAL until end.
                else:raise Refusal('frame_limit_or_missing_end')
            object_path=self._path(ctx,'objects',digest)
            object_path.parent.mkdir(parents=True,exist_ok=True)
            if object_path.exists():
                with object_path.open('rb') as existing:
                    same=hashlib.file_digest(existing,'sha256').hexdigest()==digest
                need(same and object_path.stat().st_size==total,'existing_object_corrupt')
            else:os.rename(temp,object_path)
            # Commit only verified blocks; bounded reads from the spooled object.
            with object_path.open('rb') as src:
                for block_hash,n in blocks:self._put(ctx,self._path(ctx,'blocks',block_hash),src.read(n))
            result=dict(protocol=PROTOCOL,scope=ctx.key,request_id=begin['id'],kind=begin['kind'],root=root,
                sha=digest,bytes=total,path=str(object_path),replayed=False,dispatch_allowed=True,
                reader_peak=reader.peak,status='TRANSPORT_RECONSTRUCTED_NOT_EXECUTED')
            # A transport receipt is not actual model admission; host still applies
            # current auth/memory/wallet/job guards and uncertain-call ledger.
            with self.db:
                self.db.execute('INSERT OR IGNORE INTO objects VALUES(?,?,?,?)',(ctx.key,root,manifest_bytes,str(object_path)))
                self.db.execute('INSERT INTO requests VALUES(?,?,?,?,?,?,?)',(ctx.key,begin['id'],begin['kind'],identity,digest,root,canonical(result)))
            return result
        finally:
            temp.unlink(missing_ok=True)
