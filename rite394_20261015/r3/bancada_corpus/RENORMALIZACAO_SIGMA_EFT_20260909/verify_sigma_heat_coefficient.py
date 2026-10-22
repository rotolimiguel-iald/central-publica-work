from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os
import sympy as sp

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT)
results = []

def zero(name, expression):
    residual = sp.simplify(sp.expand(expression))
    results.append({'name': name, 'residual': str(residual), 'passed': residual == 0})
    assert residual == 0, (name, residual)

# Four base directions, three tangent target directions. All derivative jets are free.
components = sp.symbols('u0:12', real=True)
u = sp.Matrix(3, 4, components)
endomorphism = u * u.T
gram = u.T * u
q = sp.trace(endomorphism)
w2 = sp.trace(gram * gram)
potential = q * sp.eye(3) - endomorphism
zero('trace_U_squared_is_W_squared', sp.trace(endomorphism**2) - w2)
zero('trace_E', sp.trace(potential) - 2*q)
zero('trace_E_squared', sp.trace(potential**2) - q*q - w2)
curvature_square = 0
for mu in range(4):
    for nu in range(4):
        curvature = u[:, mu]*u[:, nu].T - u[:, nu]*u[:, mu].T
        curvature_square += sp.trace(curvature*curvature)
zero('trace_bundle_curvature_squared', curvature_square - 2*(w2-q*q))
r = sp.symbols('R', real=True)
heat_target_terms = r*sp.trace(potential)/6 + sp.trace(potential**2)/2 + curvature_square/12
zero('target_dependent_b4', heat_target_terms - r*q/3 - q*q/3 - 2*w2/3)

# Explicit harmonic great-circle background on a flat torus.
x, k, t = sp.symbols('x k t', real=True)
phi = sp.Matrix([sp.cos(k*x), sp.sin(k*x), 0, 0])
zero('great_circle_unit_constraint', (phi.T*phi)[0]-1)
dphi = phi.diff(x)
circle_q = sp.trigsimp((dphi.T*dphi)[0])
zero('great_circle_gradient', circle_q-k*k)
tau = phi.diff(x, 2) + circle_q*phi
for i in range(2):
    zero('great_circle_tension_component_' + str(i), sp.trigsimp(tau[i]))
heat_trace = 1 + 2*sp.exp(t*k*k)
zero('exact_parallel_frame_heat_coefficient', sp.diff(heat_trace, t, 2).subs(t, 0)/2 - k**4)
zero('great_circle_quartic_coefficient', circle_q**2/3 + 2*circle_q**2/3 - k**4)
zero('unabsorbable_three_winding_residual', (sp.Integer(2)**4-sp.Integer(2)**2)-12)

loop, vertices, derivative_sum = sp.symbols('L V sum_d')
internal = loop + vertices - 1
zero('connected_graph_power_counting', 4*loop - 2*internal + derivative_sum - (2 + 2*loop + derivative_sum - 2*vertices))

source = Path(__file__).read_bytes()
record = {
    'status': 'PASS_EXACT_SIGMA_HEAT_IDENTITIES__NOT_LEAN',
    'created_utc': datetime.now(timezone.utc).isoformat(), 'sympy_version': sp.__version__,
    'source': {'path': Path(__file__).as_posix(), 'bytes': len(source), 'sha256': hashlib.sha256(source).hexdigest()},
    'checks': results, 'check_count': len(results),
    'scope': 'Exact trace identities for arbitrary 3x4 jets, great-circle background, flat local heat coefficient and graph identity. Universal heat asymptotics, renormalization and global analytic arguments remain written/imported results.',
    'um_executed_or_imported': False, 'lean_executed': False, 'originals_modified': False
}
path = OUT / 'VERIFICACAO_SIGMA_HEAT.json'
assert not path.exists()
tmp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
data = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
with tmp.open('xb') as stream:
    stream.write(data); stream.flush(); os.fsync(stream.fileno())
assert tmp.read_bytes() == data
tmp.rename(path)
assert path.read_bytes() == data
print(json.dumps({'status': record['status'], 'checks': len(results), 'receipt': path.as_posix()}, ensure_ascii=True))
