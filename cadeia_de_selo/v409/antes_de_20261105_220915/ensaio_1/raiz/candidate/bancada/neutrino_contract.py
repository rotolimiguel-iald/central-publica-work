"""Author's distinct channels; conditional synthetic evolution, no data fit."""
from pathlib import Path
import json
import math
import numpy as np
from .canonical import require_current, verify_source_bytes, finite_number

HBAR_EV_S = 6.582119569e-16

def contract():
    receipt = require_current('neutrino_contract')
    path = Path(__file__).resolve().parents[1] / 'fontes_externas/NU3/CONTRACTS_API_R2.json'
    raw = path.read_bytes()
    pin = verify_source_bytes(path, raw)
    return dict(contract=json.loads(raw), pin=pin, canonical=receipt,
                data_opened=False, verdict='CONTRACT_RECOVERED_NO_NATURE_TEST')

def nonnegative(value, name):
    value = finite_number(value, name)
    if value < 0:
        raise ValueError(name + ': nonnegative required')
    return value

def density(value, n):
    # Complex values are JSON [real, imaginary], with no implicit coercion.
    if not isinstance(value, list) or len(value) != n:
        raise ValueError('density shape')
    a = np.zeros((n,n), dtype=complex)
    for i, row in enumerate(value):
        if not isinstance(row, list) or len(row) != n:
            raise ValueError('density shape')
        for j, cell in enumerate(row):
            if not isinstance(cell, list) or len(cell) != 2:
                raise ValueError('complex cell requires [real, imaginary]')
            a[i,j] = complex(finite_number(cell[0], 'rho.real'), finite_number(cell[1], 'rho.imag'))
    if not np.allclose(a, a.conj().T, rtol=0, atol=1e-12):
        raise ValueError('density must be Hermitian')
    if abs(np.trace(a) - 1) > 1e-12 or np.linalg.eigvalsh(a).min() < -1e-12:
        raise ValueError('density must be positive with unit trace')
    return a

def encode(a):
    return np.stack((a.real, a.imag), axis=-1).tolist()

def simulate(payload):
    if not isinstance(payload, dict):
        raise ValueError('payload must be object')
    before = require_current('neutrino_synthetic_start')
    beta = before['beta_tgl']
    kind = payload.get('channel')
    fields = {
        'boundary_parity_4state': {'channel', 's', 'rho'},
        'physical_mass_gap_dephasing': {'channel', 'mass_squared_eV2', 'energy_eV', 'tau_star_s', 'Kfac', 'time_s', 'rho'},
        'modular_root_dephasing': {'channel', 'modular_eigenvalues', 's', 'rho'},
        'beta_scale': {'channel', 'chi'},
    }
    if kind not in fields or set(payload) != fields[kind]:
        raise ValueError('EXACT_CHANNEL_FIELDS_REQUIRED: no ignored parameters')
    if kind == 'boundary_parity_4state':
        s = nonnegative(payload['s'], 'dimensionless time s')
        rho = density(payload['rho'], 4)
        x = np.kron(np.array([[0,1],[1,0]]), np.eye(2))
        flip = -0.5 * math.expm1(-2*s)
        result = (1-flip)*rho + flip*(x @ rho @ x)
        out = dict(rho=encode(result), flip_probability=flip,
            operator='X_A tensor I_B', basis='parity x charge',
            normalization='d rho / ds = X rho X - rho', physical_time_map='INPUT_NOT_ASSUMED')
    elif kind in ('physical_mass_gap_dephasing', 'modular_root_dephasing'):
        vals = payload['mass_squared_eV2'] if kind == 'physical_mass_gap_dephasing' else payload['modular_eigenvalues']
        if not isinstance(vals, list) or not 2 <= len(vals) <= 8:
            raise ValueError('2..8 eigenvalues required')
        vals = np.array([nonnegative(v, 'eigenvalue') for v in vals])
        rho = density(payload['rho'], len(vals))
        if kind == 'physical_mass_gap_dephasing':
            energy = finite_number(payload['energy_eV'], 'energy_eV', True)
            tau = nonnegative(payload['tau_star_s'], 'tau_star_s')
            kfac = nonnegative(payload['Kfac'], 'Kfac')
            time = nonnegative(payload['time_s'], 'time_s')
            h = vals / (2*energy)
            freq = (h[:,None]-h[None,:]) / HBAR_EV_S
            gamma = (beta*tau*kfac/2) * freq**2
            phase = -freq*time
            scope = 'vacuum relativistic H=M2/(2E); fixed tau_star and Kfac; n=-2'
        else:
            time = nonnegative(payload['s'], 's')
            h = np.sqrt(vals)
            gamma = (beta/2)*(h[:,None]-h[None,:])**2
            phase = np.zeros_like(gamma)
            scope = 'dimensionless modular channel; physical clock not identified'
        exponent = gamma*time
        if not all(np.isfinite(v).all() for v in (gamma, phase, exponent)):
            raise ValueError('NUMERICAL_OVERFLOW')
        result = rho * np.exp(-exponent + 1j*phase)
        out = dict(rho=encode(result), gamma=gamma.tolist(), damping=np.exp(-exponent).tolist(),
            coherence_loss=(-np.expm1(-exponent)).tolist(), scope=scope,
            gamma_units='s^-1' if kind == 'physical_mass_gap_dephasing' else 'per modular s',
            diagonal_population_max_change=float(np.max(np.abs(np.diag(result)-np.diag(rho)))),
            conserved_diagonal_generator_before=float(np.dot(h, np.diag(rho).real)),
            conserved_diagonal_generator_after=float(np.dot(h, np.diag(result).real)))
    elif kind == 'beta_scale':
        chi = nonnegative(payload['chi'], 'chi')
        e = math.exp(-chi/2)
        if e == 0:
            raise ValueError('BETA_SCALE_UNDERFLOW: finite chi requires positive beta; use a logarithmic formulation')
        out = dict(beta_bulk=math.sqrt(math.e)*2*e/(1+e*e), beta_frontier=beta,
            chi_frontier=2*math.acosh(1/before['alpha']),
            scope='bulk scale from v388; no automatic substitution into a neutrino channel')
    else:
        raise ValueError('unknown channel')
    if 'rho' in out:
        out.update(trace_real=float(np.trace(result).real), trace_imag=float(np.trace(result).imag),
                   min_eigenvalue=float(np.linalg.eigvalsh(result).min()))
    after = require_current('neutrino_synthetic_end')
    if before['canonical_manifest_sha256'] != after['canonical_manifest_sha256']:
        raise ValueError('CONTRACT_CHANGED_DURING_OPERATION')
    return dict(channel=kind, result=out, beta_tgl=beta, canonical=after,
        statute='DERIVED_CONDITIONAL_NUMERICAL_REALIZATION', synthetic=True,
        nature_sigma=None, data_opened=False, gate_effect='NONE')
