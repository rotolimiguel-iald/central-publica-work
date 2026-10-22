from pathlib import Path
import datetime, hashlib, json, os
import numpy as np

ROOT = Path(__file__).resolve().parent
checks = []
def check(name, value, expected_zero=True):
    value = float(value)
    passed = value < 2e-12 if expected_zero else value > 1e-3
    checks.append(dict(name=name, value=value, expected_zero=expected_zero, passed=passed))
    assert passed, checks[-1]

def spectral_map(labels, x):
    return np.where(labels[:, None] == labels[None, :], x, 0)

def sigma(weights, t, x):
    logs = np.log(weights)
    return np.exp(1j * t * (logs[:, None] - logs[None, :])) * x

def conjugate_flow(generator, t, x):
    eig, v = np.linalg.eigh(generator)
    u = (v * np.exp(-1j * t * eig)) @ v.conj().T
    return u @ x @ u.conj().T

# Two actual binary product weights, then the next levels of a product tower.
# These are mathematical input profiles, not a measured physical diamond vacuum.
for sites in (2, 3, 4):
    weights = np.array([1/3, 2/3])
    for j in range(1, sites-1):
        p = 1 / (j+3)
        weights = np.kron(weights, [p, 1-p])
    tail = np.array([1/4, 3/4])
    d = np.kron(weights, tail)
    e = np.kron(weights, [1/2, 1/2])
    labels = np.tile(tail, len(weights))
    K, Q = np.diag(-np.log(d)), np.diag(-np.log(e))
    R = K-Q
    check(f'{sites}: density normalized', abs(d.sum()-1))
    check(f'{sites}: reference normalized', abs(e.sum()-1))
    check(f'{sites}: vacuum preserved', np.linalg.norm(spectral_map(labels, np.diag(d))-np.diag(d)))
    check(f'{sites}: remainder preserved', np.linalg.norm(spectral_map(labels, R)-R))
    check(f'{sites}: remainder nonscalar', np.linalg.norm(R-np.trace(R)/len(d)*np.eye(len(d))), False)
    largest_flow_error = largest_commutator = 0.0
    # Full basis of all matrix observables, not just one state or trace.
    for i in range(len(d)):
        for j in range(len(d)):
            x = np.zeros((len(d),len(d)), dtype=complex); x[i,j] = 1
            y = spectral_map(labels, x)
            largest_commutator = max(largest_commutator, np.linalg.norm(R@y-y@R))
            for t in (0.17, 0.61, 1.3):
                largest_flow_error = max(largest_flow_error,
                    np.linalg.norm(sigma(d,t,y)-sigma(e,t,y)))
    check(f'{sites}: full basis flow equality', largest_flow_error)
    check(f'{sites}: full basis remainder invisible', largest_commutator)
    x = np.zeros((len(d),len(d)),dtype=complex); x[0,2] = 1
    check(f'{sites}: nontrivial retained motion', np.linalg.norm(sigma(d,0.61,x)-x), False)
    # Full modular pinching freezes the output, unlike last-site pinching.
    x = np.ones((len(d),len(d)),dtype=complex)
    y = spectral_map(d,x)
    check(f'{sites}: full modular pinching stationary', np.linalg.norm(sigma(d,0.61,y)-y))

# Counterexample: removing R under the full modular reading is not enough.
K = np.diag([0.,2.]); R = np.array([[0.,1.],[1.,0.]])
Q = K-R; p = np.diag([1.,0.]); labels = np.array([0.,2.])
check('E_K(R)=0', np.linalg.norm(spectral_map(labels,R)))
check('E_K(R)=0 does not give original flow equality',
      np.linalg.norm(conjugate_flow(K,0.61,p)-conjugate_flow(Q,0.61,p)), False)
# Nor does it give equality of the final readings at finite time.
check('E_K(R)=0 does not give readout flow equality',
      np.linalg.norm(p-spectral_map(labels,conjugate_flow(Q,0.61,p))), False)

payload = dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    checks=checks, passed=len(checks), failed=0, independent_reviewer=False,
    physical_geometric_identification=False,
    scope='Finite product-tower profiles and a negative 2x2 control; not a QFT calculation.')
target = ROOT/'DEPHASING_NUMERICAL_CHECKS.json'
assert not target.exists()
data = json.dumps(payload, ensure_ascii=False, indent=2).encode('utf8')
temp=target.with_suffix('.tmp'); temp.write_bytes(data)
assert temp.read_bytes()==data
os.replace(temp,target)
print(json.dumps({'passed':len(checks), 'max_flow_errors':[c for c in checks if 'flow equality' in c['name']], 'output':str(target)}))
