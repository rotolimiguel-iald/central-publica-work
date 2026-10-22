"""Prepare the reviewed finite-ideal GNS integration without moving the gate."""
import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
MODULES = ['DualOrbitStrongLimits', 'ScalarGNSStarApproximation', 'ScalarGNSStarDensity', 'ScalarTomitaGraph']


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def save(path, text):
    assert path.resolve().is_relative_to(ROOT)
    if path.exists():
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


targets = []
for name in MODULES:
    source = (ROOT / 'kernel/TGLV350' / (name + '.lean')).read_text(encoding='utf-8')
    targets += ['TGLV350.Regular.' + t for t in re.findall(r'^#print axioms ([\w.]+)$', source, re.M)]
assert len(targets) == 14

path = ROOT / 'integrate_v350.py'
text = path.read_text(encoding='utf-8')
text = once(text, "'ScalarGNSRepresentation']", "'ScalarGNSRepresentation', " + ', '.join(map(repr, MODULES)) + ']')
text = once(text, "'import TGLExt.V350ScalarGNSRepresentation\\n')",
            "'import TGLExt.V350ScalarGNSRepresentation\\n'\n" +
            '\n'.join("               'import TGLExt.V350" + n + "\\n'" for n in MODULES) + ')')
anchor = '#print axioms TGLV350.Regular.scalarGNSRepresentation_injective\n'
text = once(text, anchor, anchor + '\n-- Norm-dense initial involutive graph on the finite-ideal GNS space.\n' +
            ''.join('#print axioms ' + n + '\n' for n in targets))
save(path, text)

path = ROOT / 'compile_integrated.py'
text = path.read_text(encoding='utf-8')
anchor = "'TGLExt/V350ScalarGNSRepresentation.lean',\n"
text = once(text, anchor, anchor + ''.join("                 'TGLExt/V350" + n + ".lean',\n" for n in MODULES))
save(path, text)

path = ROOT / 'test_gate_extension.py'
text = path.read_text(encoding='utf-8')
control = 'check("dense_initial_Tomita_graph_does_not_discharge_closed_Tomita_KMS_trace",\n      all("TGLV350.Regular." + name in axioms for name in (\n          "dualOrbit_tendsto_of_uniformly_bounded",\n          "scalarGNSOrbit_leftRegularization_tendsto",\n          "scalarGNSStarEmbedding_denseRange",\n          "scalarTomitaGraph_single_valued",\n          "scalarTomitaGraph_swap", "scalarTomitaGraph_domain_dense"))\n      and all(kf.get(flag) is False for flag in (\n          "qgf_continuous_modular_realization_constructed",\n          "qgf_unconditional_continuous_corner_proved", "qgf_full_TGL_witness_constructed",\n          "gpf_H1_internal_susy_relative_gap_discharged",\n          "gpf_H2_smooth_modular_four_frame_discharged",\n          "gpf_H3_local_horizon_equilibrium_discharged")))\n'
text = once(text, "report = {'checks': checks", control + "report = {'checks': checks")
save(path, text)
print('Prepared four modules / 14 targets; no gate promotion.')
