# Bancada GNS genuina (Hilbert-Schmidt) para a 1a clausula de comutante -- sombra de runtime, NAO teorema.
# Mesmo perfil de pesos da v244 (s0=1/3, s1=1/4), estado fiel omega(a)=Tr(rho a) em M_4.
import numpy as np, hashlib, json
s0=[1/3,2/3]; s1=[1/4,3/4]
pw=np.array([x*y for x in s0 for y in s1]); n=4
rho=np.diag(pw).astype(complex)
rng=np.random.default_rng(244)
U,_=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
rho_nd=U@rho@U.conj().T   # controle: estado nao diagonal
def bench(rho):
    w,V=np.linalg.eigh(rho); r12=V@np.diag(np.sqrt(w))@V.conj().T
    # H = M_n (vetorizado, 16 dim), xi_Omega = rho^{1/2}; pi(x) xi = x xi ; J xi = xi^dagger (conjugacao modular HS)
    vec=lambda A:A.reshape(-1); mat=lambda v:v.reshape(n,n)
    L=lambda x: np.kron(x,np.eye(n))            # x xi  (row-major)
    R=lambda y: np.kron(np.eye(n),y.T)          # xi y
    Jv=lambda v: vec(mat(v).conj().T)
    x=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); y=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    # J pi(x) J como operador 16x16
    E=np.eye(n*n); JLJ=np.column_stack([Jv(L(x)@Jv(E[:,k])) for k in range(n*n)])
    r_right=np.linalg.norm(JLJ-R(x.conj().T))                    # J pi(x) J = multiplicacao a direita por x^dagger
    r_hip=np.linalg.norm(JLJ@L(y)-L(y)@JLJ)                        # a hipotese: comuta com toda esquerda
    poly=x@x+3*x+np.eye(n)
    JPJ=np.column_stack([Jv(L(poly)@Jv(E[:,k])) for k in range(n*n)])
    r_bic=np.linalg.norm(JPJ@L(y)-L(y)@JPJ)
    r_ctrl=np.linalg.norm(L(x)@L(y)-L(y)@L(x))                    # controle negativo: esquerdas nao comutam
    r_left_ne_right=np.linalg.norm(L(x)-R(x))                      # esquerda != direita (a bancada distingue)
    xi=vec(r12); r_vac=np.linalg.norm(Jv(xi)-xi)                  # J xi_Omega = xi_Omega
    # Delta xi = rho xi rho^{-1}; J Delta^{1/2} pi(a) xi_Omega = pi(a)^dagger xi_Omega (Tomita)
    a=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
    rinv12=V@np.diag(1/np.sqrt(w))@V.conj().T
    D12=lambda v: vec(r12@mat(v)@rinv12)
    r_tomita=np.linalg.norm(Jv(D12(L(a)@xi))-L(a.conj().T)@xi)
    return dict(right_mult=r_right,hypothesis=r_hip,bicommutant_poly=r_bic,neg_control=r_ctrl,left_ne_right=r_left_ne_right,vacuum_fixed=r_vac,tomita_S=r_tomita)
out={"diag_profile":bench(rho),"nondiag_control":bench(rho_nd)}
print(json.dumps(out,indent=1))
print("script_sha16",hashlib.sha256(open(__file__,'rb').read()).hexdigest()[:16])
