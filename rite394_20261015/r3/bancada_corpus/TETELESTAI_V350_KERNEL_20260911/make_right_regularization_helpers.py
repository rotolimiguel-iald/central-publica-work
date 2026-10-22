"""Derive a reviewed right-regularization stage from pinned parent helpers."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['DenseLinearPolarExtension', 'BoundedInjectivePolar', 'ScalarGaussianImage', 'ScalarGaussianUnitary']
NAMES = ['ScalarRightRegularization', 'ScalarCommutantRegularization']
OLD_FLAGS = ['gaussian_polar_unitary_constructed', 'gaussian_closed_image_identified', 'same_scalar_GNS_cyclic_separating_vector_constructed', 'original_weight_J_not_replaced']
FLAGS = ['full_weight_right_averages_constructed', 'commutant_right_bounded_approximation_constructed', 'right_bounded_reconstruction_still_open', 'original_weight_J_not_replaced']
BODY = '''No mesmo H_I e com o ideal completo n_ν do peso original, foi construído
R_h Λν(a)=Λν(a e_h), onde e_h é a média regular existente.
O bound de peso prova ||R_h||≤1 e a convergência GNS das inscrições,
estendida por equicontinuidade, prova R_h→I fortemente quando h→0, h≠0.
Para h>0, η_h=Λν(e_h) existe e R_hΛν(a)=π(a)η_h.

[REAL] Para qualquer T∈π(N)', T R_h é um multiplicador direito limitado,
com vetor Tη_h, ||T R_h||≤||T|| e T R_h→T fortemente. Esses multiplicadores
comutam com π(N). Todo T pertence à álgebra de von Neumann gerada por eles.
Não se restringe T aos geradores conhecidos nem se pressupõe sua reconstrução.

[OPEN] ScalarRightBounded significa um vetor η e um operador limitado R
com RΛν(a)=π(a)η. Não inclui vetor adjunto, fechamento por star, plenitude
de álgebra de Hilbert ou R=Jπ(b)J. Essas conclusões não foram promovidas.
A reconstrução polar dos multiplicadores e o fechamento da imagem π(N)
ainda precisam de prova; a inclusão inversa com J original permanece aberta.
O novo critério scalarCommutant_mem_of_rightBounded assume explicitamente
Q von Neumann e a inclusão dos multiplicadores em Q; a hipótese não é descartada.

Nenhum peso foi substituído pelo funcional gaussiano. Permanecem abertos
Δ^it/KMS do mesmo peso, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados tipados/runtime.
Seis flags maiores falsas; o gate não muda por esta regularização.

'''

def create(name, text):
    ast.parse(text)
    p = ROOT / name
    assert not p.exists()
    raw = text.encode('utf-8')
    tmp = p.with_suffix('.py.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)
    assert p.read_bytes() == raw

def common(text):
    text = text.replace('gaussian_polar', 'right_regularization').replace('GAUSSIAN_POLAR', 'RIGHT_REGULARIZATION')
    text = text.replace('core_polar_custody.json', 'gaussian_polar_custody.json')
    text = text.replace('POLAR_GAUSSIANO_CICLICO', 'REGULARIZACAO_COMUTANTE')
    text = text.replace('quatro módulos/34 alvos', 'dois módulos/19 alvos').replace('Quatro módulos/34 alvos', 'Dois módulos/19 alvos')
    text = text.replace('Polar gaussiano e vetor cíclico separante', 'Regularização de todo o comutante')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old.replace('gaussian_polar', 'right_regularization'), new)
    text = text.replace('len(targets) == 34', 'len(targets) == 19').replace('len(modules) == 4', 'len(modules) == 2')
    text = text.replace(repr(OLD_NAMES), repr(NAMES))
    return text

def replace_body(text):
    text, count = re.subn(r'No mesmo H_I=ScalarGNSHilbert P.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = replace_body(common((ROOT / 'record_gaussian_polar_draft.py').read_text(encoding='utf-8')))
t = t.replace("parent['actual_polar_conjugates_core_into_commutant']", "parent['gaussian_polar_unitary_constructed']")
t = t.replace('Freeze the Gaussian polar unitary and cyclic separating vector construction.',
    'Freeze actual bounded right regularization of the entire commutant.')
create('record_right_regularization_draft.py', t)

t = common((ROOT / 'prepare_gaussian_polar_stage.py').read_text(encoding='utf-8'))
t = t.replace("len(draft['targets']) == 34", "len(draft['targets']) == 19")
t = t.replace('assert count == 491', 'assert count == 525')
t = t.replace("text = once(text, '== 491', '== 525')", "text = once(text, '== 525', '== 544')")
t = t.replace("'ScalarGNSGeneratorTransport', 'CorePolarInclusion'", "'ScalarGaussianImage', 'ScalarGaussianUnitary'")
t = t.replace('TGLExt/V350CorePolarInclusion.lean', 'TGLExt/V350ScalarGaussianUnitary.lean')
begin = t.index('anchor = "        \'scalarGNS_commutation_from_generators\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarGNSCyclicVector_cyclic'),\\n"
text = once(text, anchor, anchor + "    'full_weight_right_regularization_and_commutant_approximation': (\\n"
    "        'scalarRightRegularization_embedding', 'scalarRightRegularization_tendsto',\\n"
    "        'scalarCommutant_rightBounded_approximation',\\n"
    "        'scalarCommutant_mem_generated_rightBounded'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 34", "'new_targets': 19").replace('count + 34', 'count + 19')
t = t.replace('Prepare the independently reviewed Gaussian polar and cyclic vector.',
    'Prepare the independently reviewed full-weight right regularization.')
create('prepare_right_regularization_stage.py', t)

t = replace_body(common((ROOT / 'record_gaussian_polar_progress.py').read_text(encoding='utf-8')))
t = t.replace('RELATORIO_INCLUSAO_POLAR_CORE_INTEGRADA.md', 'RELATORIO_POLAR_GAUSSIANO_CICLICO_INTEGRADA.md')
t = t.replace('Record reviewed Gaussian cyclic preparation with the complete memory lineage.',
    'Record reviewed right regularization with the complete memory lineage.')
create('record_right_regularization_progress.py', t)

t = common((ROOT / 'verify_gaussian_polar_custody.py').read_text(encoding='utf-8'))
t = t.replace('Reread the integrated Gaussian polar preparation and exact-byte memory lineage.',
    'Reread integrated commutant regularization and exact-byte memory lineage.')
create('verify_right_regularization_custody.py', t)
print('Created two-module/19-target helpers. No integration or memory writes executed.')
