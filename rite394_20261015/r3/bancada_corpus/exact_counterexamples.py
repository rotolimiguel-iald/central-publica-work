"""Controles racionais exatos; nenhuma execução ou escrita no acervo original."""
from fractions import Fraction as Q
from pathlib import Path
import json

def matrix(rows):
    return [[Q(x) for x in row] for row in rows]

def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2))
             for j in range(2)] for i in range(2)]

def adj(a):
    return [list(row) for row in zip(*a)]  # Todas as entradas são reais.

identity = matrix([[1, 0], [0, 1]])
rho = matrix([[Q(2, 3), 0], [0, Q(1, 3)]])
rho_inv = matrix([[Q(3, 2), 0], [0, 3]])
swap = matrix([[0, 1], [1, 0]])
projector = matrix([[1, 0], [0, 0]])

def omega(a):
    ra = mul(rho, a)
    return ra[0][0] + ra[1][1]

def norm_squared(a):
    return omega(mul(adj(a), a))

delta_swap = mul(mul(rho, swap), rho_inv)
checks = {
    'state_normalized': omega(identity) == 1,
    'density_strictly_positive': rho[0][0] > 0 and rho[1][1] > 0,
    'swap_unitary': mul(swap, adj(swap)) == identity,
    'normalization_does_not_force_invariance':
        omega(mul(mul(swap, projector), adj(swap))) != omega(projector),
    'S_preserves_this_vector_norm': norm_squared(adj(swap)) == norm_squared(swap),
    'this_vector_not_fixed_by_delta': delta_swap != swap,
    'this_vector_not_in_centralizer': mul(rho, swap) != mul(swap, rho),
}
assert all(checks.values()), checks
result = {
    'status': 'REAL_EXACT_RATIONAL_COMPUTATION',
    'checks': checks,
    'omega_projector': str(omega(projector)),
    'omega_conjugated_projector': str(omega(mul(mul(swap, projector), adj(swap)))),
    'norm_squared_swap': str(norm_squared(swap)),
    'norm_squared_S_swap': str(norm_squared(adj(swap))),
    'delta_swap': [[str(x) for x in row] for row in delta_swap],
    'scope': 'Contraexemplos a inferências gerais, não refutação dos teoremas Lean condicionais.',
}
output = Path(__file__).resolve().parent / 'contraexemplos_resultados.json'
temporary = output.with_suffix('.json.tmp')
data = json.dumps(result, ensure_ascii=False, indent=2).encode('utf-8')
temporary.write_bytes(data)
assert temporary.stat().st_size == len(data) > 0
temporary.replace(output)
print(json.dumps(result, ensure_ascii=False, indent=2))
