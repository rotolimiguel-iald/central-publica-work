from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations
from functools import lru_cache
import hashlib,json,os
import sympy as S

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02'
OUT.mkdir(exist_ok=False)
checks=[]
def check(name, condition, detail=None):
    row={'name':name,'passed':bool(condition)}
    if detail is not None: row['detail']=detail
    checks.append(row)
    assert condition,row
def new(p,obj):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
    q=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with q.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert q.read_bytes()==b
    q.rename(p)
    assert p.read_bytes()==b
    return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
pairs=list(combinations(range(5),2))
indices={p:i for i,p in enumerate(pairs)}
@lru_cache(None)
def basis(q): return list(combinations(range(10),q))
@lru_cache(None)
def basis_index(q): return {v:i for i,v in enumerate(basis(q))}
def add(*forms):
    out={}
    for form in forms:
        for m,c in form.items(): out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}
def scale(k,form): return {m:k*c for m,c in form.items() if k*c}
def wedge(a,b):
    out={}
    for x,c in a.items():
        for y,d in b.items():
            if set(x)&set(y): continue
            sgn=(-1)**sum(i>j for i in x for j in y)
            z=tuple(sorted(x+y));out[z]=out.get(z,0)+sgn*c*d
    return {m:c for m,c in out.items() if c}
def monomial(m): return {tuple(m):S.Integer(1)}
def vector(form,q): return S.Matrix([form.get(m,0) for m in basis(q)])
def serial_form(form): return [{'indices':list(m),'coefficient':str(c)} for m,c in sorted(form.items())]
def matrix_data(M): return [[str(M[i,j]) for j in range(M.cols)] for i in range(M.rows)]
results=[]
for label,epsilon in [
    ('compact_so5',[1,1,1,1,1]),
    ('lorentz_so14',[-1,1,1,1,1]),
    ('lorentz_so23',[-1,1,1,1,-1])
]:
    matrices=[]
    eta=S.diag(*epsilon)
    for a,b in pairs:
        M=S.zeros(5);M[a,b]=epsilon[a];M[b,a]=-epsilon[b]
        matrices.append(M)
        check(label+':metric_skew:'+str((a,b)),M.T*eta+eta*M==S.zeros(5))
    structure={}
    for i in range(10):
        for j in range(10):
            comm=matrices[i]*matrices[j]-matrices[j]*matrices[i]
            co={k:comm[a,b]/epsilon[a] for k,(a,b) in enumerate(pairs) if comm[a,b]}
            recon=sum((v*matrices[k] for k,v in co.items()),S.zeros(5))
            check(label+':bracket:'+str((i,j)),comm==recon)
            structure[i,j]=co
    dg=[{} for _ in range(10)]
    for i,j in combinations(range(10),2):
        for k,v in structure[i,j].items(): dg[k][(i,j)]=-v
    def differential(form):
        out={}
        for m,c in form.items():
            for pos,k in enumerate(m):
                term=wedge(wedge(monomial(m[:pos]),dg[k]),monomial(m[pos+1:]))
                out=add(out,scale(c*(-1)**pos,term))
        return out
    for k in range(10): check(label+':d_squared:'+str(k),not differential(dg[k]))
    def lie_generator(a,k):
        return {(i,):-structure[a,i].get(k,0) for i in range(10) if structure[a,i].get(k,0)}
    def lie(a,form):
        out={}
        for m,c in form.items():
            for pos,k in enumerate(m):
                term=wedge(wedge(monomial(m[:pos]),lie_generator(a,k)),monomial(m[pos+1:]))
                out=add(out,scale(c,term))
        return out
    h=[i for i,(a,b) in enumerate(pairs) if b<4]
    invariants={}
    for q in [2,3,4]:
        cas=S.zeros(len(basis(q)))
        actions=[]
        for a in h:
            L=S.Matrix.hstack(*(vector(lie(a,monomial(m)),q) for m in basis(q)))
            i,j=pairs[a]
            cas+=epsilon[i]*epsilon[j]*(L*L)
            actions.append(L)
        inv=cas.nullspace()
        for i,v in enumerate(inv):
            check(label+':joint_invariant:'+str((q,i)),all(L*v==S.zeros(v.rows,1) for L in actions))
        check(label+':invariant_dimension:'+str(q),len(inv)=={2:0,3:4,4:3}[q],len(inv))
        invariants[q]=S.Matrix.hstack(*inv) if inv else S.zeros(len(basis(q)),0)
    D3=S.Matrix.hstack(*(vector(differential(monomial(m)),4) for m in basis(3)))
    image=D3*invariants[3]
    check(label+':invariant_d3_rank',image.rank()==3)
    kernel=image.nullspace()
    check(label+':invariant_d3_kernel_dimension',len(kernel)==1)
    survivor=invariants[3]*kernel[0]
    check(label+':survivor_closed',D3*survivor==S.zeros(len(basis(4)),1))
    # Cartan cubic is computed independently from the ten-dimensional Lie bracket.
    killing=S.Matrix(10,10,lambda i,j:S.trace(matrices[i]*matrices[j]))
    cartan={}
    for i,j,k in basis(3):
        val=sum(killing[i,l]*v for l,v in structure[j,k].items())
        if val: cartan[(i,j,k)]=val
    cv=vector(cartan,3)
    check(label+':cartan_nonzero',any(cv))
    check(label+':cartan_closed',not differential(cartan))
    check(label+':cartan_natural',all(not lie(a,cartan) for a in h))
    check(label+':same_surviving_line',S.Matrix.hstack(cv,survivor).rank()==1)
    # The full (non-invariant) ranks are separate finite-dimensional controls.
    D2=S.Matrix.hstack(*(vector(differential(monomial(m)),3) for m in basis(2)))
    check(label+':full_d2_rank',D2.rank()==35)
    check(label+':full_d3_rank',D3.rank()==84)
    check(label+':d3_d2_zero',D3*D2==S.zeros(len(basis(4)),len(basis(2))))
    rows=[{'q':q,'dimension':invariants[q].cols,'basis':[serial_form({m:invariants[q][i,j] for i,m in enumerate(basis(q)) if invariants[q][i,j]}) for j in range(invariants[q].cols)]} for q in [2,3,4]]
    results.append({'model':label,'metric':epsilon,'invariants':rows,
                    'd3_invariant_rank':3,'d3_invariant_kernel_dimension':1,
                    'cartan_three_form':serial_form(cartan),
                    'full_d2_rank':35,'full_d3_rank':84,
                    'scope':'Finite CE and isotropy invariants only, not the full jet BRST complex or inverse limits.'})
    print(json.dumps({'model':label,'done':True,'checks':len(checks)}),flush=True)
source=Path(__file__).resolve()
source_raw=source.read_bytes()
record={'status':'PASS_EXACT_FINITE_CE_CONTROLS','created_utc':datetime.now(timezone.utc).isoformat(),
        'basis_pairs':[list(p) for p in pairs],'convention':'X_ab[a,b]=epsilon[a], X_ab[b,a]=-epsilon[b]; dtheta_k=-sum_i<j f_ij^k theta_i wedge theta_j.',
        'results':results,'checks':checks,'checks_total':len(checks),'checks_passed':sum(c['passed'] for c in checks),
        'sympy_version':S.__version__,'source':{'path':source.as_posix(),'bytes':len(source_raw),'sha256':hashlib.sha256(source_raw).hexdigest()},
        'originals_written':False,'um_executed_or_imported':False,'new_lean_compilations':0,
        'limits':'Exact finite-dimensional algebra controls. Not proof of full H3/H4, lim1, anomaly removal or quantum gravity. No physical data tests.'}
pin=new(OUT/'RESULTADO_CE_EXATO_077.json',record)
print(json.dumps({'result':pin,'checks':len(checks)}),flush=True)

