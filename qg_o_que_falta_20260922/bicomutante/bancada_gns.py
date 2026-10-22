# Bancada GNS correta (proposta) para a secao the_first_commutant_clause (errata v266 L4).
# H = M4(C) (16 dim), <a,b> = Tr(rho a^H b), Omega = 1, J(a) = rho^{1/2} a^H rho^{-1/2}.
# Superoperadores como matrizes 16x16 via vec (row-major). Phi(T) = J o T o J.
import numpy as np, itertools
s0=[1/3,2/3]; s1=[1/4,3/4]
pw=np.array([x*y for x in s0 for y in s1]); n=4
rt=np.diag(np.sqrt(pw)).astype(complex); rti=np.linalg.inv(rt); rho=rt@rt
basis=[]
for i,j in itertools.product(range(n),range(n)):
    E=np.zeros((n,n),complex); E[i,j]=1; basis.append(E)
vec=lambda a:a.reshape(-1); unvec=lambda v:v.reshape(n,n)
def supmat(f):  # complex-linear superoperator -> 16x16
    return np.column_stack([vec(f(E)) for E in basis])
J=lambda a: rt@a.conj().T@rti
def Phi(T):   # T 16x16 complex-linear; Phi(T)=J T J (complex-linear again)
    return supmat(lambda a: J(unvec(T@vec(J(a)))))
L=lambda x: supmat(lambda a: x@a)
G=lambda X: np.array([[np.trace(rho@A.conj().T@B) for B in basis] for A in basis])  # Gram
rng=np.random.default_rng(244)
rc=lambda: rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
x,y=rc(),rc(); c=complex(rng.normal(),rng.normal())
T1=rng.normal(size=(16,16))+1j*rng.normal(size=(16,16)); T2=rng.normal(size=(16,16))+1j*rng.normal(size=(16,16))
nrm=np.linalg.norm
out={}
out['J_involutive']=nrm(J(J(x))-x)
Gm=G(None)
ip=lambda a,b: np.trace(rho@a.conj().T@b)
out['J_antiunitary_<Ja,Jb>=conj<a,b>']=abs(ip(J(x),J(y))-np.conj(ip(x,y)))
out['J_fixes_Omega']=nrm(J(np.eye(n))-np.eye(n))
out['Phi_linear']=nrm(Phi(c*T1+T2)-(c*Phi(T1)+Phi(T2)))
out['Phi_mult']=nrm(Phi(T1@T2)-Phi(T1)@Phi(T2))
out['Phi_invol']=nrm(Phi(Phi(T1))-T1)
out['Phi_NOT_identity_on_L(x)']=nrm(Phi(L(x))-L(x))   # deve ser GRANDE (a errata L4 era =0)
out['HIPOTESE [Phi(L_x),L_y]']=nrm(Phi(L(x))@L(y)-L(y)@Phi(L(x)))  # deve ser ~0
poly=x@x+3*x+np.eye(n)
out['BICOMUTANTE [Phi(L_p(x)),L_y]']=nrm(Phi(L(poly))@L(y)-L(y)@Phi(L(poly)))
out['CONTROLE [L_x,L_y]']=nrm(L(x)@L(y)-L(y)@L(x))
# Phi(L_x) e multiplicacao a DIREITA por rho^{1/2} x^H... medir forma: a -> a * r
Rx=Phi(L(x)); r=unvec(Rx@vec(np.eye(n)))  # imagem do vacuo
out['Phi(L_x) = R_r (a->a r)']=nrm(Rx-supmat(lambda a:a@r))
# RECIPROCA na face finita: comutante de L(M4) em End(H) = span Phi(L(M4))
gens=[L(E) for E in basis]
A=np.vstack([np.kron(g,np.eye(16))-np.kron(np.eye(16),g.T) for g in gens])  # vec(gT - Tg)=0
sv=np.linalg.svd(A,compute_uv=False); dimcomm=int(np.sum(sv<1e-9))
PhiM=np.column_stack([Phi(g).reshape(-1) for g in gens]); rkPhiM=np.linalg.matrix_rank(PhiM,1e-9)
# span(comutante) contido em span Phi(M)? usar nullspace
_,_,Vh=np.linalg.svd(A); N=Vh.conj().T[:, -dimcomm:] if dimcomm>0 else np.zeros((256,0))
joint=np.linalg.matrix_rank(np.hstack([PhiM,N]),1e-8)
out['dim M-linha (comutante de L(M4))']=dimcomm
out['posto Phi(L(M4))']=rkPhiM
out['posto conjunto (=16 sse iguais)']=joint
# CONTROLE NEGATIVO da reciproca: M = M2 (x) 1, Omega NAO ciclico -> JMJ estritamente menor que M'
sub=[np.kron(e,np.eye(2)) for e in [np.array([[1,0],[0,0]]),np.array([[0,1],[0,0]]),np.array([[0,0],[1,0]]),np.array([[0,0],[0,1]])]]
gs=[L(e.astype(complex)) for e in sub]
As=np.vstack([np.kron(g,np.eye(16))-np.kron(np.eye(16),g.T) for g in gs])
dcs=int(np.sum(np.linalg.svd(As,compute_uv=False)<1e-9))
rks=np.linalg.matrix_rank(np.column_stack([Phi(g).reshape(-1) for g in gs]),1e-9)
out['CTRL nao-ciclico: dim (M2x1)-linha']=dcs
out['CTRL nao-ciclico: posto Phi(M2x1)']=rks
for k,v in out.items(): print(f'{k}: {v}')
print('--- tipagem da linearidade')
print('Phi ANTIlinear em T: ||Phi(cT1+T2)-(conj(c)Phi(T1)+Phi(T2))|| =', nrm(Phi(c*T1+T2)-(np.conj(c)*Phi(T1)+Phi(T2))))
a0=rc()
f=lambda a: J(unvec(T1@vec(J(a))))
print('JTJ LINEAR nos vetores: ||JTJ(c a)-c JTJ(a)|| =', nrm(f(c*a0)-c*f(a0)))
