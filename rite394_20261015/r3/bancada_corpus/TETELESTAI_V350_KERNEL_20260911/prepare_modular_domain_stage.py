"""Prepare the scalar dual weight stage without promoting it to a trace."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ['ScalarModularInvariance', 'RegularScalarWeightCertificate', 'ContractionAdjointLimit', 'StrongBoundedApplication', 'FiniteDualStarCore']


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def save(path, text, new=False):
    assert path.resolve().is_relative_to(ROOT)
    if new:
        assert not path.exists(), path
    if path.exists():
        before = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + STAMP)
        with backup.open('xb') as handle:
            handle.write(before)
        assert backup.read_bytes() == before
    raw = text.encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as handle:
        handle.write(raw)
    assert temporary.read_bytes() == raw and len(raw) > 0
    temporary.replace(path)
    assert path.read_bytes() == raw


targets = []
for name in MODULES:
    source = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    targets += ['TGLV350.Regular.' + t for t in re.findall(r'^#print axioms ([\w.]+)$', source, re.M)]
assert len(targets) == 17

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'FiniteDualStarCore'" not in text
text = once(text, "'ScalarDualWeight']", "'ScalarDualWeight', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350ScalarDualWeight\\n')",
            "'import TGLExt.V350ScalarDualWeight\\n'\n" +
            '\n'.join("               'import TGLExt.V350" + n + "\\n'" for n in MODULES) + ')')
anchor = '#print axioms TGLV350.Regular.scalarDualWeight_bounded_base_value\n'
text = once(text, anchor, anchor + '\n-- Candidate flow invariance and a bounded strongly dense star domain; KMS remains open.\n' +
            ''.join('#print axioms ' + n + '\n' for n in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarDualWeight.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + n + ".lean',\n" for n in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = """check('modular_domain_and_invariance_do_not_discharge_KMS_trace_or_physical_obligations',
      all('TGLV350.Regular.' + name in axioms for name in (
          'scalarDualWeight_regular_invariant', 'regularScalarWeightCertificate',
          'contraction_adjoint_tendsto_identity', 'bounded_application_tendsto',
          'finiteDualStarCore', 'regularSandwich_norm_le',
          'finiteDualStarCore_strongStar_approximation', 'finiteDualStarCore_scalar_squares_finite'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
"""
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)

print('Prepared five modular-domain modules; no KMS, trace or gate promotion.')
