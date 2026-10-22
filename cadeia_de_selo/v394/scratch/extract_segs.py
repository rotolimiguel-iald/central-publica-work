import ast, hashlib, sys, os
sys.stdout.reconfigure(encoding="utf-8")
A=sys.argv[1]; B=sys.argv[2]; OUT=sys.argv[3]
os.makedirs(OUT,exist_ok=True)
def load(p):
    t=open(p,'rb').read().decode('utf-8'); return t,ast.parse(t)
ta,tra=load(A); tb,trb=load(B)
def key(n,i):
    if isinstance(n,(ast.FunctionDef,ast.ClassDef)): return n.name
    if isinstance(n,ast.Assign): return ','.join(ast.unparse(x) for x in n.targets)
    return '%s_pos%d'%(type(n).__name__,i)
da={key(n,i):n for i,n in enumerate(tra.body)}
h=lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
rows=[]
for i,n in enumerate(trb.body):
    k=key(n,i)
    st='new' if k not in da else ('chg' if h(da[k])!=h(n) else None)
    if st and not k.startswith(('Expr_','Assert_')) or (st and True):
        seg=ast.get_source_segment(tb,n)
        fn=os.path.join(OUT,'%s_%03d_%s.py'%(st,i,k[:60].replace('/','_')))
        open(fn,'w',encoding='utf-8').write(seg or '')
        rows.append((st,i,k,len(seg or ''),n.lineno))
for r in rows: print(r)
