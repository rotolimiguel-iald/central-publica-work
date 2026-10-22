"""Integrate the finite-square ideal proofs in the isolated monolith."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ('RegularApproximation', 'FourierL1L2', 'RegularFiniteWeight', 'DualSemifiniteIdeal')


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def save(path, text):
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as f:
        f.write(before)
    assert backup.read_bytes() == before
    raw = text.encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.replace(path)
    assert path.read_bytes() == raw


path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'RegularApproximation'" not in text
text = once(text, "'PositiveFormCone', 'DualFixedWeightLaws']",
    "'PositiveFormCone', 'DualFixedWeightLaws', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350PositiveFormCone\\nimport TGLExt.V350DualFixedWeightLaws\\n')",
    "'import TGLExt.V350PositiveFormCone\\nimport TGLExt.V350DualFixedWeightLaws\\n'\n"
    + ''.join("               'import TGLExt.V350" + name + "\\n'\n" for name in MODULES).rstrip() + ')')
targets = []
for name in MODULES:
    source = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    namespace = 'TGLV350.Fourier.' if name == 'FourierL1L2' else 'TGLV350.Regular.'
    targets.extend(namespace + target for target in re.findall(r'^#print axioms ([\w.]+)$', source, re.M))
text = once(text, '#print axioms TGLV350.Regular.dualFixedWeight_preserves_internal_isLUB\n',
    '#print axioms TGLV350.Regular.dualFixedWeight_preserves_internal_isLUB\n\n'
    '-- Finite-square left ideal, exact Fourier weight and strong approximation.\n'
    '-- F=base, the scalar trace and full physical gate remain separate obligations.\n'
    + ''.join('#print axioms ' + name + '\n' for name in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
text = once(text, "'TGLExt/V350PositiveFormCone.lean', 'TGLExt/V350DualFixedWeightLaws.lean',\n",
    "'TGLExt/V350PositiveFormCone.lean', 'TGLExt/V350DualFixedWeightLaws.lean',\n"
    + ''.join("                 'TGLExt/V350" + name + ".lean',\n" for name in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = '''check('finite_square_ideal_is_dense_but_does_not_discharge_trace_or_physics',
      all(name in axioms for name in (
          'TGLV350.Fourier.fourier_integral_ae_eq_L2',
          'TGLV350.Fourier.fourier_integral_lintegral_norm_sq',
          'TGLV350.Regular.regularAverage_dualQuadraticIntegral',
          'TGLV350.Regular.finiteDualLeftIdeal_left_mul',
          'TGLV350.Regular.finiteDualLeftIdeal_strong_approximation'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)
print('Prepared isolated integration; new audit targets=' + str(len(targets)))
