# Segundo cálculo INDEPENDENTE do auditor (sem usar o código do construtor). β lido dos bytes do um.py.
import re, math, json, hashlib, sys
from fractions import Fraction
from decimal import Decimal, getcontext
sys.stdout.reconfigure(encoding='utf-8')
UM=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
b=open(UM,'rb').read()
out={"um_py_sha256":hashlib.sha256(b).hexdigest(),"um_py_bytes":len(b)}
lines=b.split(b"\n")
hits=[(i+1,l) for i,l in enumerate(lines) if l.startswith(b"ALPHA_FINE_CODATA_2018")]
out["linhas_ALPHA_nao_indentadas"]=[(n,l.decode()) for n,l in hits]
assert len(hits)==1
m=re.match(rb"ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)",hits[0][1]); alpha=float(m.group(1))
# tambem a atribuicao de topo SEALED_CODATA_ALPHA
hs=[(i+1,l) for i,l in enumerate(lines) if l.startswith(b"SEALED_CODATA_ALPHA")]
out["SEALED_CODATA_ALPHA"]=[(n,l.decode()[:80]) for n,l in hs]
beta=alpha*math.sqrt(math.e)
out["beta_runtime"]=beta; out["beta_minus_conferencia"]=beta-0.012031300400803142
# (1) S = cos t 1 + sin t Grot, sin^2 t = beta; T = |S|^2 entrywise; lambda = 1-2beta ; det T
th=math.asin(math.sqrt(beta))
S=[[math.cos(th),math.sin(th)],[-math.sin(th),math.cos(th)]]
T=[[S[i][j]**2 for j in range(2)] for i in range(2)]
lam=1-2*beta
out["A1_T"]=T; out["A1_T_vs_[[1-b,b],[b,1-b]]_max"]=max(abs(T[0][0]-(1-beta)),abs(T[0][1]-beta)); out["A1_detT"]=T[0][0]*T[1][1]-T[0][1]*T[1][0]; out["A1_detT_minus_lambda"]=T[0][0]*T[1][1]-T[0][1]*T[1][0]-lam
out["A1_theta_M"]=th; out["A1_cos"]=math.cos(th); out["A1_sin"]=math.sin(th); out["A1_lambda"]=lam
out["A1_a=-ln(lam)/2"]=-math.log(lam)/2
# (2) KMS/modular clock of rho1=diag(1-b,b): omega1 = ln((1-b)/b) ; P1 = 2pi/omega1 ; Davies rate g01 = b*omega1
w1=math.log((1-beta)/beta); P1=2*math.pi/w1; g01=beta*w1
out["A2_omega1"]=w1; out["A2_P1"]=P1; out["A2_g01"]=g01
out["A2_omega1_minus_conf"]=w1-4.4081393960414665; out["A2_P1_minus_conf"]=P1-1.4253599404823543; out["A2_g01_minus_conf"]=g01-0.05303564928238982
# KMS check for 2x2 diag state: omega(a sigma_{i}(b)) = omega(b a) with sigma_t(b)=rho^{it} b rho^{-it}; at t = i : rho^{-1} b rho ... verify for a=E01, b=E10 numerically:
# omega(a sigma_i(b)) = tr(rho a rho^{-1} b rho) ; omega(b a) = tr(rho b a)
rho=[[1-beta,0],[0,beta]]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def tr(A): return A[0][0]+A[1][1]
E01=[[0,1],[0,0]]; E10=[[0,0],[1,0]]
rinv=[[1/(1-beta),0],[0,1/beta]]
lhs=tr(mm(mm(mm(mm(rho,E01),rinv),E10),rho)); rhs=tr(mm(mm(rho,E10),E01))
out["A2_KMS_E01_E10_lhs_rhs_diff"]=lhs-rhs
# wrong temperature Delta_2 (rho^2 . rho^-2): fails?
r2=[[(1-beta)**2,0],[0,beta**2]]; r2inv=[[1/(1-beta)**2,0],[0,1/beta**2]]
lhs2=tr(mm(mm(mm(mm(rho,E01),r2inv),E10),r2)); out["A2_KMS_wrong_temperature_gap"]=lhs2-rhs
# (3) purity under dephasing psi+ with Davies rate at t=1: (1+e^{-2 g01})/2 ; and negativity (1-e^{gamma t})/2
out["A3_pur_psi_t1"]=(1+math.exp(-2*g01))/2; out["A3_pur_minus_conf"]=(1+math.exp(-2*g01))/2-0.9496802613377202
out["A3_vol_davies_t1=e^{-2g01}"]=math.exp(-2*g01); out["A3_vol_minus_conf"]=math.exp(-2*g01)-0.8993605226754405
for gt,conf in ((beta,-0.006051983815068773),(1.0,-0.8591409142295225),(10.0,-11012.732897403359),(g01,-0.02723361772478261)):
    v=(1-math.exp(gt))/2; out[f"A3_neg_gt={gt:.6g}"]=(v,v-conf)
# eigenvalue check: T_{-t} psi+ = 1/2 [[1, e^{gt}],[e^{gt},1]] has eigenvalues (1±e^{gt})/2 -> min negative
# (4) k_eps: smallest k with lambda^k < eps ; omega_k = 2 artanh(lambda^k) ; k where float64 lambda^k < 1e-15; rank drop
def keps(eps):
    k=1
    while lam**k>=eps: k+=1
    return k
out["A4_k_eps"]={e:keps(float(e)) for e in ("0.1","0.001","1e-06")}
out["A4_omega_k"]={k:2*math.atanh(lam**k) for k in (1,10,100,1000)}
out["A4_omega1_eq_2artanh_lambda"]=2*math.atanh(lam)-w1
out["A4_lam4096"]=lam**4096
# (5) T1.o analytic: min_T ||TH-HT - i 1||_F = sqrt(n) since commutators are exactly the traceless matrices and i1 ⟂ traceless with norm sqrt(n)
out["A5_min_dist_i1_to_traceless_n"]={n:math.sqrt(n) for n in (2,3,4,5,8)}
# numerical check with numpy-free lstsq for n=2 random: solve min over T of ||[T,H]-i1||: project i1 onto traceless: residual = |tr(i1)|/sqrt(n) = sqrt(n)
# (6) T9.o(c) float drift: repeated multiplication in float64 (my own loop) vs exact Fraction, k up to 1e4
import copy
Tf=[[T[0][0],T[0][1]],[T[1][0],T[1][1]]]
rowsum=[Tf[0][0]+Tf[0][1]-1, Tf[1][0]+Tf[1][1]-1]; out["A6_rowsum_minus_1_float"]=rowsum
# powers by repeated multiply (left) 
Pk=[[1.0,0.0],[0.0,1.0]]; maxdev=0; kmax_dev=None; first_exceed=None
Rm=[[0.5,0.5],[0.5,0.5]]
for k in range(1,10001):
    Pk=mm(Pk,Tf)
    lk=lam**k
    ref=[[Rm[i][j]+lk*((1.0 if i==j else 0.0)-Rm[i][j]) for j in range(2)] for i in range(2)]
    dev=max(abs(Pk[i][j]-ref[i][j]) for i in range(2) for j in range(2))
    if dev>maxdev: maxdev=dev; kmax_dev=k
    if first_exceed is None and dev>1e-13: first_exceed=k
out["A6_float_repeated_mult_maxdev"]=(maxdev,kmax_dev); out["A6_first_k_dev>1e-13"]=first_exceed
# binary powering (like matrix_power) 
def mpow(M,k):
    Rr=[[1.0,0.0],[0.0,1.0]]; B=M
    while k:
        if k&1: Rr=mm(Rr,B)
        B=mm(B,B); k>>=1
    return Rr
P4=mpow(Tf,10000); lk=lam**10000
ref=[[Rm[i][j]+lk*((1.0 if i==j else 0.0)-Rm[i][j]) for j in range(2)] for i in range(2)]
out["A6_binary_pow_k1e4_dev"]=max(abs(P4[i][j]-ref[i][j]) for i in range(2) for j in range(2))
# exact arithmetic: Fraction from the float entries of Tf (the represented matrix) -> exact power; deviation from R + lam_rep^k (I-R) where lam_rep = Tf00 - Tf01 exactly
TF=[[Fraction(Tf[i][j]) for j in range(2)] for i in range(2)]
def mmF(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mpowF(M,k):
    Rr=[[Fraction(1),Fraction(0)],[Fraction(0),Fraction(1)]]; B=M
    while k:
        if k&1: Rr=mmF(Rr,B)
        B=mmF(B,B); k>>=1
    return Rr
PF=mpowF(TF,10000)
delta=TF[0][0]+TF[0][1]-1  # row sum defect of the represented matrix
out["A6_rowsum_defect_exact_delta"]=float(delta)
# exact power of represented T: rows sum to (1+delta)^k; deviation from stochastic reference ~ ((1+delta)^k - 1)/2
out["A6_exact_power_rowsum_minus_1_k1e4"]=float(PF[0][0]+PF[0][1]-1)
out["A6_k*delta/2"]=float(10000*delta/2)
# exact identity with exact T from exact beta is tautological; the point: deviation from float ref
lamF=TF[0][0]-TF[0][1]
refF=[[Fraction(1,2)+lamF**10000*((1 if i==j else 0)-Fraction(1,2)) for j in range(2)] for i in range(2)]
out["A6_exact_power_vs_exact_ref_same_represented_T"]=float(max(abs(PF[i][j]-refF[i][j]) for i in range(2) for j in range(2)))
# (7) boost: B(1)^100 (1,-1) norm = sqrt(2) e^{-100}
out["A7_sqrt2_e^-100"]=math.sqrt(2)*math.exp(-100); out["A7_minus_conf"]=math.sqrt(2)*math.exp(-100)-5.260981898346995e-44
getcontext().prec=80
out["A7_decimal"]=str(Decimal(2).sqrt()*(Decimal(1).exp()**-100))[:40]
# (8) half identity rank 2, R=J/2 rank 1
out["A8_rank_I_over_2"]=2; out["A8_rank_R"]= 1 if (Rm[0][0]*Rm[1][1]-Rm[0][1]*Rm[1][0])==0 else 2
# (9) k at which float lambda^k < 1e-15 (coherence floor)
k=1
while lam**k>=1e-15: k+=1
out["A9_first_k_lambda^k<1e-15"]=k
json.dump(out,open("AUD_INDEPENDENTE.json","w",encoding='utf-8'),indent=1,ensure_ascii=False,default=str)
print(json.dumps(out,indent=1,ensure_ascii=False,default=str))
