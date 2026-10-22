"""Exact finite witness: spectral-center channel and a relative-state selector."""
from pathlib import Path
from fractions import Fraction as Q
from datetime import datetime,timezone
import hashlib,json,os,sys
sys.stdout.reconfigure(encoding="utf-8")
folder=Path(__file__).resolve().parent
assert folder.parent==Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
assert folder.name.startswith("PONTE_SETOR_GEOMETRICO_")
def zero(n=4):return [[Q(0) for j in range(n)] for i in range(n)]
def diag(v):
    a=zero(len(v))
    for i,x in enumerate(v):a[i][i]=x
    return a
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(a))) for j in range(len(a))] for i in range(len(a))]
def transpose(a):return [list(r) for r in zip(*a)]
def center(a):return diag([a[0][0],(a[1][1]+a[2][2])/2,(a[1][1]+a[2][2])/2,a[3][3]])
weights=[Q(1,9),Q(2,9),Q(2,9),Q(4,9)]
rho=diag(weights)
seed=diag([Q(1),Q(1),Q(0),Q(0)])
v=diag([Q(1)]*4)
v[1][1]=v[2][2]=Q(3,5);v[1][2]=Q(-4,5);v[2][1]=Q(4,5)
def rotate(a):return mul(mul(v,a),transpose(v))
sigmaweights=[Q(1,20),Q(1,5),Q(3,20),Q(3,5)]
sigma=diag(sigmaweights)
ratio=[s/r for s,r in zip(sigmaweights,weights)]
choi=zero(16)
for i in range(4):
    for j in range(4):
        e=zero();e[i][j]=Q(1)
        f=center(e)
        for a in range(4):
            for b in range(4):choi[4*i+a][4*j+b]=f[a][b]
checks={
"rho_faithful_normalized":all(w>0 for w in weights) and sum(weights)==1,
"sigma_faithful_normalized":all(w>0 for w in sigmaweights) and sum(sigmaweights)==1,
"rho_sigma_commute":mul(rho,sigma)==mul(sigma,rho),
"relative_density_all_distinct":len(set(ratio))==4,
"relative_density_positive_normalized":all(r>0 for r in ratio) and sum(w*r for w,r in zip(weights,ratio))==1,
"rotation_preserves_rho":rotate(rho)==rho,
"rotation_changes_sigma":rotate(sigma)!=sigma,
"rotated_sigma_offdiagonal":rotate(sigma)[1][2]==Q(3,125),
"center_changes_seed":center(seed)!=seed,
"centered_seed_exact":center(seed)==diag([Q(1),Q(1,2),Q(1,2),Q(0)]),
"seed_and_rotated_seed_noncommute":mul(seed,rotate(seed))!=mul(rotate(seed),seed),
"choi_diagonal":choi==diag([choi[i][i] for i in range(16)]),
"choi_nonnegative_diagonal":all(choi[i][i]>=0 for i in range(16)),
"choi_rank_six":sum(choi[i][i]>0 for i in range(16))==6,
"center_unital":center(diag([Q(1)]*4))==diag([Q(1)]*4),
}
for i in range(4):
    for j in range(4):
        e=zero();e[i][j]=Q(1)
        checks["idempotence_basis_%d_%d"%(i,j)]=center(center(e))==center(e)
        checks["weighted_state_basis_%d_%d"%(i,j)]=sum(weights[k]*center(e)[k][k] for k in range(4))==sum(weights[k]*e[k][k] for k in range(4))
        checks["rotation_covariance_basis_%d_%d"%(i,j)]=center(rotate(e))==rotate(center(e))
if not all(checks.values()):raise RuntimeError("Exact witness failed")
result={"status":"PASS_EXACT_WITNESS","created_utc":datetime.now(timezone.utc).isoformat(),
"rho":rho,"sigma":sigma,"relative_density":ratio,"rotation":v,"seed":seed,
"centered_seed":center(seed),"choi_diagonal":[choi[i][i] for i in range(16)],
"checks":checks,"check_count":len(checks),
"scope":{"positive_finite_channel":"CP follows from the exact nonnegative diagonal Choi matrix and the standard finite Choi theorem; not claimed compiled in Lean here.",
"relative_state":"Constructed finite witness supplied as additional input, not selected by a physical law.",
"phase_family":"Distinct positive relative eigenvalues imply distinct logarithms; the full one-parameter phase family separates the four labels. This analytic conclusion is explained in the report, not computed as a finite-time phase test.",
"quantum_gravity_closed":False},
"script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
data=(json.dumps(result,ensure_ascii=False,indent=2,default=str)+"\n").encode("utf-8")
target=folder/"TESTEMUNHA_EXATA.json"
temp=folder/"TESTEMUNHA_EXATA.json.tmp"
assert not target.exists()
with temp.open("xb") as f:f.write(data);f.flush();os.fsync(f.fileno())
assert temp.read_bytes()==data
os.rename(temp,target)
assert target.read_bytes()==data
print(json.dumps({"status":result["status"],"checks":len(checks),"relative_density":[str(r) for r in ratio],"file":target.as_posix()},ensure_ascii=False))
