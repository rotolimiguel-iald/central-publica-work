"""Reviewer: v402 checks 15/17 re-applied to v404: (15) no statute/verdict leaf that the accepted v402 shared carried LITERAL (source unchanged v402->v404) became pointer-only in v404;
(17) topics whose JSON block omits source keys are IDENTICAL (decoded) to the accepted v402 block with unchanged source, or kernel_formalization; per package shared + sonnet_public + haiku55 + haiku_expanded."""
import json,re,sys,io,contextlib,importlib.util
from pathlib import Path
def load(wd):
    sys.argv=['x',str(wd)]
    spec=importlib.util.spec_from_file_location('r3x',str(Path(__file__).parent/'r3_topics_capsules.py'))
    with contextlib.redirect_stdout(io.StringIO()):
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
W4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');W2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027')
m4=load(W4);m2=load(W2)
STAT=re.compile(r'status|statute|estatuto|verdict|veredit',re.I)
def blocks(m,pkg):
    t=(m.W/'app/packages'/pkg/'prefix.md').read_text('utf-8');head=m.unalias(t.partition(m.MARK)[0])
    Dm=re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n',head);D=json.loads(Dm.group(1)) if Dm else {}
    F=re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n',head);FL=json.loads(F.group(1)) if F else {}
    E=t.partition(m.MARK)[2].split('<EXPOSICAO_CANONICA>\n',1)[1].split('\n</EXPOSICAO_CANONICA>',1)[0]
    hs=list(re.finditer(r'(?m)^### ([^\n]+)\n',head));out={}
    for i,h in enumerate(hs):
        seg=head[h.end():(hs[i+1].start() if i+1<len(hs) else len(head))]
        out[h[1]]=(seg,D,FL,E)
    return out
def decode(m,seg,D,FL,E):
    lines=[l for l in seg.split('\n') if l.strip() and not l.startswith('Fonte:')]
    try:v=json.loads(lines[0])
    except Exception:return ('TEXT',seg.strip())
    if isinstance(v,dict) and '@B' in v:v.update(FL[str(v.pop('@B'))])
    return ('JSON',m.dec_lit(m.unpack(v),D,E))
def lits(x,p=''):
    """literal leaf paths: leaves outside reference nodes, plus capsule 'fields' entries; value included"""
    out={}
    if type(x).__name__=='Summ':return {p:'SUMMARY_REF:'+x.ptr+':'+str(x.a)+':'+str(x.n)}
    if isinstance(x,dict):
        if '@' in x:
            for k,v in x.get('fields',{}).items():out.update(lits(v,p+k))
            for k,v in x.items():
                if k not in('@','fields','items','true_fields','false_fields'):out.update(lits(v,p+'/'+k))
            return out
        for k,v in x.items():out.update(lits(v,p+'/'+k.replace('~','~0').replace('/','~1')))
    elif isinstance(x,list):
        for i,v in enumerate(x):out.update(lits(v,p+'/'+str(i)))
    else:out[p]=json.dumps(x,ensure_ascii=False)
    return out
common=[n for n in m4.core if n in m2.core and m4.core[n]==m2.core[n]]
print('topics common to v402/v404 with UNCHANGED source:',len(common))
for pkg in('shared','sonnet_public','haiku_expanded'):
    b4=blocks(m4,pkg);b2=blocks(m2,pkg)
    regress=[];identical=0;differ=[];text_same=0;checked=0
    for n in common:
        k4,d4=decode(m4,*b4[n]);k2,d2=decode(m2,*b2[n])
        if k4=='TEXT' or k2=='TEXT':
            if k4==k2 and d4==d2:text_same+=1
            else:differ.append((n,'text-form differs'))
            continue
        checked+=1
        if json.dumps(d4,sort_keys=True,default=lambda o:'S:'+getattr(o,'ptr','')+str(getattr(o,'a',''))+str(getattr(o,'n',''))+str(getattr(o,'topic','')))==json.dumps(d2,sort_keys=True,default=lambda o:'S:'+getattr(o,'ptr','')+str(getattr(o,'a',''))+str(getattr(o,'n',''))+str(getattr(o,'topic',''))):identical+=1
        else:differ.append((n,'decoded block differs'))
        l4=lits(d4,'');l2=lits(d2,'')
        for p,val in l2.items():
            last=p.rsplit('/',1)[-1]
            if STAT.search(last) or STAT.search(p):
                if l4.get(p)!=val:regress.append((n,p))
    print(pkg,'| JSON topics',checked,'identical decoded to accepted v402',identical,'| text-form same',text_same,'| differ',len(differ),differ[:5],'| status-literal regressions',len(regress),regress[:5])
# new/changed topics: 62 source-changed topics. For those, status/verdict literal in v404 shared == source?
chg=[n for n in m4.core if n in m2.core and m4.core[n]!=m2.core[n]]
b4=blocks(m4,'shared');bad=[]
for n in chg:
    k,d=decode(m4,*b4[n])
    if k=='TEXT':continue
    rep=[]
    try:got=m4.restore(d,m4.res,'/core/'+n,rep,m4.E if hasattr(m4,'E') else '')
    except Exception as e:bad.append((n,str(e)[:80]))
print('source-changed topics',len(chg),'text-form',sum(1 for n in chg if decode(m4,*b4[n])[0]=='TEXT'))

# --- which top-level keys of the 6 former-window topics (v401/v402) are literal in accepted v402 but pointer-only in v404
print('--- former-window topics: top-level keys literal in v402 but pointer-only in v404')
def toplits(m,pkg,n):
    b=blocks(m,pkg);k,d=decode(m,*b[n])
    if k=='TEXT':return None
    L=lits(d,'');tops={}
    for p in L:
        t=p.split('/')[1] if p.count('/')>=1 else p
        tops.setdefault(t,0);tops[t]+=1
    return set(tops),len(L)
for pkg in('haiku_expanded','shared'):
    for n in('falsidade_da_inercia_v401','ponte_da_escala_dual_v402','queda_sem_geometria_v402','esperanca_condicional_v402','cunhagens_v401','cunhagens_v402','kh_n1_cobertura_v402','kh_n1_cobertura_v401'):
        if n not in m4.core or n not in m2.core:continue
        a=toplits(m2,pkg,n);b=toplits(m4,pkg,n)
        if a and b:print(pkg,n,'literal leaves v402',a[1],'-> v404',b[1],'| top keys lost literal:',sorted(a[0]-b[0]))
