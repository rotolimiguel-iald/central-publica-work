"""Check an analytic first-order modular response against ordered preparation.

This is a regulated matrix verification of the Euclidean cylinder formula.
It neither constructs a physical QFT nor supplies a TGL stress tensor.
No imported engine or canonical program is executed.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import numpy as np

ROOT = Path(__file__).resolve().parent
PERIOD = 2 * np.pi

def hermitian_exp(a):
    values, vectors = np.linalg.eigh(a)
    return (vectors * np.exp(values)) @ vectors.conj().T

def negative_log(rho):
    values, vectors = np.linalg.eigh(rho)
    assert values.min() > 0
    return (vectors * (-np.log(values))) @ vectors.conj().T

def prepared_state(energies, zero, modes, coupling, steps):
    """Reflection-symmetric midpoint product: positive ordered preparation."""
    dt = PERIOD / steps
    transfer = np.eye(len(energies), dtype=complex)
    for j in range(steps):
        tau = (j + .5) * dt
        perturbation = zero.copy()
        for frequency, operator in modes:
            perturbation += np.cos(frequency * tau) * operator
        transfer = hermitian_exp(-dt * (np.diag(energies) + coupling * perturbation)) @ transfer
    hermiticity_error = float(np.linalg.norm(transfer - transfer.conj().T))
    assert hermiticity_error < 1e-11
    transfer = (transfer + transfer.conj().T) / 2
    state = transfer / np.trace(transfer)
    assert np.linalg.eigvalsh(state).min() > 0
    return state

def predicted_derivative(energies, zero, modes):
    gap = energies[:, None] - energies[None, :]
    result = PERIOD * zero.copy()
    for frequency, operator in modes:
        result += PERIOD * gap**2 / (gap**2 + frequency**2) * operator
    weights = np.exp(-PERIOD * energies)
    weights /= weights.sum()
    normalization = PERIOD * np.dot(weights, np.diag(zero)).real
    return result - normalization * np.eye(len(energies))

rng = np.random.default_rng(162026)
def sample_hermitian():
    raw = rng.normal(size=(3, 3)) + 1j*rng.normal(size=(3, 3))
    return (raw + raw.conj().T) / 12

zero, first, second = sample_hermitian(), sample_hermitian(), sample_hermitian()
cases = [
    ('distinct_gaps_first_harmonic', np.array([0., .35, .9]), zero, [(1, first)]),
    ('degenerate_gaps_two_harmonics', np.array([0., .45, .45]), zero, [(1, first), (2, second)]),
    ('static_source', np.array([0., .35, .9]), zero, []),
]
epsilon = 1e-4
results = []
for label, energies, constant, modes in cases:
    analytic = predicted_derivative(energies, constant, modes)
    errors = []
    for steps in [128, 256, 512, 1024]:
        plus = prepared_state(energies, constant, modes, epsilon, steps)
        minus = prepared_state(energies, constant, modes, -epsilon, steps)
        measured = (negative_log(plus) - negative_log(minus)) / (2*epsilon)
        error = float(np.linalg.norm(measured - analytic))
        errors.append({'steps': steps, 'frobenius_error': error})
    assert errors[-1]['frobenius_error'] < 2e-5, (label, errors)
    if modes:
        assert errors[-1]['frobenius_error'] < errors[0]['frobenius_error'] / 30
    results.append({'case': label, 'errors': errors,
                    'analytic_hermiticity_error': float(np.linalg.norm(analytic - analytic.conj().T))})

# Nonzero cosine preparation that commutes at every time integrates to zero.
# Within a degenerate block, the instantaneous charge can still act nontrivially.
energies = np.array([0., .4, .4])
operator = np.zeros((3, 3), dtype=complex)
operator[1, 2] = operator[2, 1] = 1
constant = np.zeros((3, 3), dtype=complex)
coupling = .03
state = prepared_state(energies, constant, [(1, operator)], coupling, 256)
weights = np.exp(-PERIOD * energies); weights /= weights.sum()
stationarity_error = float(np.linalg.norm(state - np.diag(weights)))
assert stationarity_error < 1e-12
observable = np.diag([0., 1., -1.])
remainder_derivative = -PERIOD * operator
commutator_norm = float(np.linalg.norm(remainder_derivative @ observable - observable @ remainder_derivative))
assert commutator_norm > 1

data = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'status': 'PASSED', 'epsilon': epsilon, 'period': float(PERIOD),
    'cases': results,
    'commuting_preparation_control': {
        'state_unchanged_error': stationarity_error,
        'instantaneous_remainder_commutator_norm': commutator_norm},
    'scope': 'Finite regulated matrices; numerical consistency check of the derived '
             'Duhamel/Frechet formula. Not measured QFT or physical data.',
    'kernel_formally_verified': False,
    'physical_TGL_coefficient_computed': False,
}
path = ROOT / 'CYLINDER_RESPONSE_CHECKS.json'
assert not path.exists(), 'Preserve previous evidence; do not overwrite silently.'
raw = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
tmp = path.with_suffix('.json.tmp')
tmp.write_bytes(raw); assert tmp.read_bytes() == raw
os.replace(tmp, path)
print(json.dumps(data, ensure_ascii=False, indent=2))
