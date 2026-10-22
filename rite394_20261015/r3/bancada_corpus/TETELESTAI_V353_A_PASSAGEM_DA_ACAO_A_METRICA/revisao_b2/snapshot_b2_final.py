from pathlib import Path
from datetime import datetime
import hashlib,json,os,re

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=R/'revisao_b2'
S=R/'s'
SRC=R/'kernel'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
A=OUT/('b2_final_'+STAMP)

def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def fresh(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp_'+STAMP)
    with t.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.replace(t,p)

def save(p,d):fresh(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))

def uncomment(text):
    depth=0;out=[];i=0
    while i<len(text):
        if text.startswith('/-',i):depth+=1;i+=2
        elif depth and text.startswith('-/',i):depth-=1;i+=2
        elif depth:
            if text[i]=='\n':out.append('\n')
            i+=1
        elif text.startswith('--',i):
            j=text.find('\n',i);i=len(text) if j<0 else j
        else:out.append(text[i]);i+=1
    return ''.join(out)

A.mkdir()
seen=set(); records=[]; statements=[]
def visit(mod):
    if mod in seen:return
    seen.add(mod)
    p=SRC/(mod.replace('.','/')+'.lean')
    b=p.read_bytes();code=uncomment(b.decode('utf-8-sig'))
    imports=[]
    for m in re.finditer(r'^\s*(?:public\s+)?import\s+([^\n]+)',code,re.M):imports.extend(m.group(1).split())
    for dep in imports:
        if dep.startswith(('TGL.','TGLExt.')) or dep in ['TGL','TGLExt']:visit(dep)
    q=S/p.relative_to(SRC)
    new=not q.exists()
    if new:fresh(q,b)
    assert q.read_bytes()==b,p
    if mod in ['TGLExt.FLRWGeometry','TGLExt.FLRWFieldEquations','TGLExt.AuditFLRW']:
        fresh(A/p.name,b)
    records.append(dict(module=mod,source=pin(p),copy=pin(q),new_source_copy=new,imports=imports))
    if mod in ['TGLExt.FLRWGeometry','TGLExt.FLRWFieldEquations']:
        forbidden=re.findall(r'\b(?:sorry|axiom|native_decide|trustCompiler|admit|unsafe)\b',code)
        assert not forbidden,(mod,forbidden)
        for match in re.finditer(r'^(def|theorem)\s+([A-Za-z0-9_]+)\b',code,re.M):
            start=match.start();end=code.find(':=',start)
            statements.append(dict(name='ChatgptAudit.FLRW.'+match.group(2),kind=match.group(1),module=mod,line=code[:start].count('\n')+1,statement=code[start:end].strip()))
visit('TGLExt.AuditFLRW')
code=(S/'TGLExt'/'AuditFLRW.lean').read_text(encoding='utf-8-sig')
targets=re.findall(r'^#print axioms\s+(\S+)',code,re.M)
assert len(targets)==len(set(targets))==32
assert set(targets)=={d['name'] for d in statements}
assert sum(d['kind']=='theorem' for d in statements)==26
review='import TGLExt.FLRWFieldEquations\n\nset_option pp.universes true\n\n'
for t in targets:review+=f'#check {t}\n#print axioms {t}\n\n'
own_audit=S/'TGLExt'/'ReviewFLRW.lean'
fresh(own_audit,review.encode('utf8'))
fiche=(OUT/'suppliers_20260914_153824_720287'/'REAPROVEITAMENTO_B2.json')
assert fiche.read_bytes()==(R/'REAPROVEITAMENTO_B2.json').read_bytes()
snapshot=dict(timestamp=datetime.now().astimezone().isoformat(),status='B2_SOURCE_FROZEN__BUILD_AND_REVIEW_PENDING',root=str(S),attempt=str(A),sources=records,targets=targets,statements=statements,author_auditor_targets_exact=True,new_target_count=32,theorems=26,definitions=6,own_auditor=pin(own_audit),fiche=pin(fiche),forbidden_tokens=[],author_project_objects_copied=False,needs_supplier_build_finished=True)
save(A/'snapshot.json',snapshot)
save(OUT/'B2_FINAL_SNAPSHOT_POINTER.json',dict(attempt=str(A),snapshot=pin(A/'snapshot.json')))
print(json.dumps(dict(attempt=str(A),source_count=len(records),new_copies=[r['module'] for r in records if r['new_source_copy']],targets=len(targets),pins=[r['source'] for r in records if r['module'] in ['TGLExt.FLRWGeometry','TGLExt.FLRWFieldEquations','TGLExt.AuditFLRW']]),ensure_ascii=False,indent=2))
