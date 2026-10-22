import ast, hashlib, sys, json
sys.stdout.reconfigure(encoding="utf-8")
A=sys.argv[1]; B=sys.argv[2]
def load(p):
    t=open(p,'rb').read().decode('utf-8'); tree=ast.parse(t); return t,tree
def key(n,i):
    if isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.AsyncFunctionDef)): return (type(n).__name__,n.name)
    if isinstance(n,ast.Assign):
        ts=[ast.unparse(x) for x in n.targets]; return ('Assign',','.join(ts))
    if isinstance(n,ast.AnnAssign): return ('AnnAssign',ast.unparse(n.target))
    return (type(n).__name__, 'pos%d'%i)
ta,tra=load(A); tb,trb=load(B)
def idx(tree):
    d={}; order=[]
    for i,n in enumerate(tree.body):
        k=key(n,i); 
        if k in d: k=(k[0],k[1]+'#%d'%i)
        d[k]=n; order.append(k)
    return d,order
da,oa=idx(tra); db,ob=idx(trb)
h=lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
only_a=[k for k in oa if k not in db]; only_b=[k for k in ob if k not in da]
chg=[k for k in oa if k in db and h(da[k])!=h(db[k])]
print("top-level A:",len(oa),"B:",len(ob)); print("only in A:",only_a); print("only in B:",only_b)
print("changed:",len(chg))
for k in chg:
    na,nb=da[k],db[k]
    print("  ",k, "A lines",na.end_lineno-na.lineno+1,"B lines",nb.end_lineno-nb.lineno+1)
