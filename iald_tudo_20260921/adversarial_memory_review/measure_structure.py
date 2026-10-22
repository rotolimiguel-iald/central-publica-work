"""Measure structural alternatives only in memory; never writes a candidate."""
from pathlib import Path
import collections, hashlib, json, os, re, socket
BASE=Path(__file__).resolve().parent
WORK=BASE.parent
os.environ['TIKTOKEN_CACHE_DIR']=r'C:\IALD\projetos_pyhton\IALD\.iald_runtime\tokenizer_cache'
def blocked(*a,**k): raise RuntimeError('Network forbidden')
socket.socket=blocked
import tiktoken
enc=tiktoken.get_encoding('o200k_base')
def tok(s): return len(enc.encode(s,disallowed_special=()))
def js(n): return json.dumps(n,ensure_ascii=False,separators=(',',':'))
raw=(WORK/'haiku_candidate.md').read_bytes(); text=raw.decode()
assert hashlib.sha256(raw).hexdigest()==json.loads((BASE/'measurements.json').read_bytes())['input_hashes']['haiku_candidate.md']
matches=list(re.finditer(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)',text))
nodes=[json.loads(m[3]) for m in matches]
marker='## Exposição canônica integral: fórmulas e derivações'
exp=text.split(marker,1)[1]
glossary=json.loads(text.split('a referência preserva o valor, não acrescenta estatuto.\n',1)[1].split('\n',1)[0])
keycost=collections.Counter()
for n in nodes:
    if isinstance(n,dict):
        for k,v in n.items(): keycost[k]+=tok(js({k:v}))
refs=[]
def xref(n):
    if isinstance(n,dict) and set(n)=={'@EXPOSITION','starts_with'}:
        # Preserve current reference; no inventing its length.
        return n
    if isinstance(n,str) and len(n)>=35 and n in exp:
        pos=exp.index(n)
        replacement={'@E':[pos,len(n)]}
        if tok(js(n))>tok(js(replacement))+1:
            assert exp[pos:pos+len(n)]==n
            refs.append({'offset':pos,'chars':len(n)})
            return replacement
    if isinstance(n,dict): return {k:xref(v) for k,v in n.items()}
    if isinstance(n,list): return [xref(v) for v in n]
    return n
def render(ns,prefix=''):
    out=text
    for m,n in reversed(list(zip(matches,ns))): out=out[:m.start(3)]+js(n)+out[m.end(3):]
    return prefix+out
v1=render([xref(n) for n in nodes], 'METADADOS @E=[offset,chars]: texto literal na exposição após seu cabeçalho fixo; índices Unicode.\n')
stub_count=0
def stubs(n):
    global stub_count
    if isinstance(n,dict):
        if set(n)=={'@'}:
            stub_count+=1
            return {'@':True}
        return {k:stubs(v) for k,v in n.items()}
    if isinstance(n,list):return [stubs(v) for v in n]
    return n
v2=render([stubs(n) for n in nodes], 'METADADOS: @:true indica detalhes não carregados no caminho JSON atual, relativo à Fonte do tópico.\n')
audit_removed=[]
def audit(n,path=''):
    if isinstance(n,dict):
        out={}
        for k,v in n.items():
            p=path+'/'+k
            if k in ('runtime_s','protocol_hash','frozen_hash','result_sha16','catalog_sha16','result_path'):
                audit_removed.append({'path':p,'o200k':tok(js({k:v}))})
            elif p=='/external_ladder/per_theorem':
                fields=v.get('fields',{})
                assert all(isinstance(b,bool) for b in fields.values())
                out[k]={'@':v['@'],'true_fields':sum(b is True for b in fields.values()),'false_fields':sum(b is False for b in fields.values())}
                audit_removed.append({'path':p,'o200k':tok(js({k:v}))-tok(js({k:out[k]}))})
            else:out[k]=audit(v,p)
        return out
    if isinstance(n,list):return [audit(v,path+'/'+str(i)) for i,v in enumerate(n)]
    return n
trim=[audit(n,'/'+m[1]) for m,n in zip(matches,nodes)]
v3=render(trim,'Metadados de tempo, hashes auxiliares e caminho de resultado permanecem recuperáveis na Fonte por chave original. per_theorem: contagens de booleanos, nunca provas; consultar indicador antes de atribuir prova.\n')
v4=render([stubs(xref(n)) for n in trim], 'Metadados: @:true usa o caminho JSON atual relativo à Fonte; @E=[offset,chars] recupera literal da exposição carregada após cabeçalho. Tempos, hashes auxiliares e result_path ficam na Fonte por chave original. Contagens per_theorem são booleanos, nunca provas.\n')
result={'candidate_sha256':hashlib.sha256(raw).hexdigest(),'original':tok(text),
 'section_o200k':{'before_topics':tok(text[:matches[0].start()]),'topics_area':tok(text[matches[0].start():text.index(marker)]),'exposition_and_tail':tok(marker+exp)},
 'top_field_costs':keycost.most_common(30),
 'variants':{name:{'o200k':tok(v),'saved_o200k':tok(text)-tok(v),'anthropic':'NOT_MEASURED'} for name,v in [('exact_exposition_offsets',v1),('implicit_stub_paths',v2),('audit_metadata_retrievable',v3),('combined_structural',v4)]},
 'new_literal_refs':len(refs),'audit_removed':audit_removed,
 'caveat':'Implicit paths require resolver tests; audit fields externalized need retrieval, not loaded. No semantic approval.'}
assert raw==(WORK/'haiku_candidate.md').read_bytes()
path=BASE/'structural_measurements.json'; payload=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode()
tmp=path.with_suffix('.tmp')
with tmp.open('xb') as f:f.write(payload)
assert tmp.read_bytes()==payload and not path.exists();tmp.replace(path)
print(json.dumps({k:v for k,v in result.items() if k!='audit_removed'},ensure_ascii=False,indent=2))
