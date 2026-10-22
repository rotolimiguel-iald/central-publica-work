"""Afericao (8)+(9): 'verbo = projetor |a><a|' E '[V_i,V_j] = i c eps_ijk V_k' com c != 0
sao compativeis? Em dimensao finita: Tr[V_i,V_j] = 0 => c*Tr(V_k) = 0 => Tr(V_k)=0;
projetor com traco 0 tem posto 0 => V_k = 0. Numerico: para projetores de posto 1 aleatorios,
o residuo da relacao su(2) com c = beta nunca se anula; e com V_i = (c/2) sigma_i (su(2) genuina)
V_i^2 != V_i (nao sao projetores)."""
import numpy as np, math
rng=np.random.default_rng(0)
ALPHA=1/137.035999084; BETA=ALPHA*math.sqrt(math.e)
def proj(d):
    v=rng.normal(size=d)+1j*rng.normal(size=d); v/=np.linalg.norm(v); return np.outer(v,v.conj())
eps=np.zeros((3,3,3)); eps[0,1,2]=eps[1,2,0]=eps[2,0,1]=1; eps[0,2,1]=eps[2,1,0]=eps[1,0,2]=-1
def residual(V,c):
    r=0.0
    for i in range(3):
        for j in range(3):
            comm=V[i]@V[j]-V[j]@V[i]
            rhs=sum(1j*c*eps[i,j,k]*V[k] for k in range(3))
            r=max(r,np.abs(comm-rhs).max())
    return r
print("beta =",repr(BETA))
for d in (2,3,8):
    res=[residual([proj(d) for _ in range(3)],BETA) for _ in range(200)]
    print(f"d={d}: projetores posto-1 aleatorios: residuo min={min(res):.3e} (nunca 0)")
# trace argument, symbolic check on random projectors: Tr(comm)=0 always
V=[proj(4) for _ in range(3)]
print("Tr([V0,V1]) =",np.trace(V[0]@V[1]-V[1]@V[0]).round(12), "; Tr(V2) =",np.trace(V[2]).round(12),
      "=> c*Tr(V2)=0 forca Tr(V2)=0 => posto 0 => V2=0")
# genuine su(2) with constant c: V_i = (c/2) sigma_i
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]],complex)
W=[(BETA/2)*s for s in (sx,sy,sz)]
print("su(2) escalada V_i=(beta/2)sigma_i: residuo =",f"{residual(W,BETA):.3e}", "; idempotente? max|V^2-V| =",f"{max(np.abs(w@w-w).max() for w in W):.3e}")
# compact: exp(i theta V) periodic
th=np.linspace(0,2*np.pi/BETA*2,5)
from scipy.linalg import expm
print("exp(i*theta*(2/beta)*Vz) em theta=2pi:",np.round(expm(1j*2*np.pi*(2/BETA)*W[2]),6).tolist())
