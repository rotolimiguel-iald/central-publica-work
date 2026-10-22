# Bancada GNS genuina (proposta de substituicao da sombra v244/v266 L4). Somente leitura; nao toca o um.py.
import numpy as np
s0=[1/3,2/3]; s1=[1/4,3/4]
pw=np.array([x*y for x in s0 for y in s1])
rho=np.diag(pw).astype(complex)
# estado nao-diagonal tambem (rotaciona) para evitar trivialidade diagonal
rng=np.random.default_rng(244)
U,_=np.linalg.qr(rng.normal(size=(4,4))+1j*rng.normal(size=(4,4)))
rho=U@rho@U.conj().T
w,v=np.linalg.eigh(rho); sq=(v*np.sqrt(w))@v.conj().T
n=4; N=n*n
E=[np.zeros((n,n),complex) for _ in range(N)]
for k in range(N): E[k][k//n,k%n]=1
vec=lambda X: X.reshape(-1); unvec=lambda x: x.reshape(n,n)
def L(x): return np.column_stack([vec(x@E[k]) for k in range(N)])   # pi(x) xi = x xi
def R(x): return np.column_stack([vec(E[k]@x) for k in range(N)])
Jv=lambda xi: vec(unvec(xi).conj().T)  # J xi = xi^dagger (forma padrao, Omega = rho^1/2)
def Phi(T): # J T J, linear
    return np.column_stack([Jv(T@Jv(vec(E[k]))) for k in range(N)])
x=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); y=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
Om=vec(sq)
Jfix=np.linalg.norm(Jv(Om)-Om)
r_id=np.linalg.norm(Phi(L(x))-L(x))
r_right=np.linalg.norm(Phi(L(x))-R(x.conj().T))
r_hip=np.linalg.norm(L(y)@Phi(L(x))-Phi(L(x))@L(y))
poly=x@x+3*x+np.eye(n)
r_bic=np.linalg.norm(L(y)@Phi(L(poly))-Phi(L(poly))@L(y))
r_ctrl=np.linalg.norm(L(y)@L(x)-L(x)@L(y))
# clausula reciproca na face finita: dim do comutante de L(M_4) = 16 = dim {R(x)}
A=np.vstack([np.kron(np.eye(N),L(E[k]))-np.kron(L(E[k]).T,np.eye(N)) for k in range(N)])
dim_comm=N*N-np.linalg.matrix_rank(A,tol=1e-9)
print(dict(J_fixa_Omega=Jfix, Phi_menos_id=r_id, Phi_igual_direita=r_right, hipotese=r_hip, bicomutante=r_bic, controle=r_ctrl, dim_comutante=dim_comm))
