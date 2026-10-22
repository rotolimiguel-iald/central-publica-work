"""Extend the isolated integration with the reviewed form cone and weight laws."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ('PositiveFormCone', 'DualFixedWeightLaws')


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def save(path, text):
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as f:
        f.write(before)
    assert backup.read_bytes() == before
    raw = text.encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + STAMP)
    with temporary.open('xb') as f:
        f.write(raw)
    assert temporary.read_bytes() == raw and len(raw) > 0
    temporary.replace(path)
    assert path.read_bytes() == raw


path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
assert "'PositiveFormCone'" not in text
text = replace_once(text, "'DualSupportTransport', 'DualFixedFormAffiliation']",
    "'DualSupportTransport', 'DualFixedFormAffiliation', 'PositiveFormCone', 'DualFixedWeightLaws']")
text = replace_once(text, "'import TGLExt.V350DualFixedFormAffiliation\\n')",
    "'import TGLExt.V350DualFixedFormAffiliation\\n'\n"
    "               'import TGLExt.V350PositiveFormCone\\nimport TGLExt.V350DualFixedWeightLaws\\n')")
targets = []
for module in MODULES:
    source = (ROOT / 'kernel/TGLV350' / (module + '.lean')).read_text(encoding='utf-8')
    targets.extend('TGLV350.Regular.' + name for name in
        re.findall(r'^#print axioms ([\w.]+)$', source, re.M))
text = replace_once(text, '#print axioms TGLV350.Regular.dualFixedAffiliatedPositiveForm_value\n',
    '#print axioms TGLV350.Regular.dualFixedAffiliatedPositiveForm_value\n\n'
    '-- Ordered affiliated forms and the faithful normal form-valued weight into F.\n'
    '-- Base identification, algebraic semifiniteness and the canonical trace remain open.\n'
    + ''.join('#print axioms ' + name + '\n' for name in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
text = replace_once(text, "'TGLExt/V350DualFixedFormAffiliation.lean',\n",
    "'TGLExt/V350DualFixedFormAffiliation.lean',\n"
    "                 'TGLExt/V350PositiveFormCone.lean', 'TGLExt/V350DualFixedWeightLaws.lean',\n")
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = '''check('normal_faithful_fixed_weight_does_not_supply_semifinitude_trace_or_physics',
      all('TGLV350.Regular.' + name in axioms for name in (
          'AffiliatedPositiveForm.scale_laws', 'AffiliatedPositiveForm.add_mono',
          'dualFixedWeight_add', 'dualFixedWeight_scale', 'dualFixedWeight_bimodule',
          'dualFixedWeight_faithful', 'dualFixedWeight_preserves_internal_isLUB'))
      and all(kf.get(flag) is False for flag in (
          'qgf_continuous_modular_realization_constructed',
          'qgf_unconditional_continuous_corner_proved', 'qgf_full_TGL_witness_constructed',
          'gpf_H1_internal_susy_relative_gap_discharged',
          'gpf_H2_smooth_modular_four_frame_discharged',
          'gpf_H3_local_horizon_equilibrium_discharged')))
'''
text = replace_once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)
print('Integration scripts extended; targets=' + str(len(targets)))
