import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager, _mathtext
for fn in ('ARIALN.TTF', 'ARIALNB.TTF', 'ARIALNI.TTF', 'ARIALNBI.TTF'):
    font_manager.fontManager.addfont('C:/Windows/Fonts/' + fn)
_mathtext.SHRINK_FACTOR = 1.0
plt.rcParams.update({'font.family': ['Arial Narrow', 'STIXGeneral', 'DejaVu Sans'], 'font.size': 14, 'mathtext.fontset': 'custom',
                     'mathtext.rm': 'Arial Narrow', 'mathtext.it': 'Arial Narrow:italic', 'mathtext.bf': 'Arial Narrow:bold',
                     'mathtext.cal': 'STIXGeneral', 'mathtext.fallback': 'stix', 'pdf.fonttype': 42})
fig = plt.figure(figsize=(9, 4))
fig.text(0.03, 0.85, 'plain: |Ψ⟩ ℋ ∮ T̂_M 𝒜_C 𝓐_C ψ₊ψ₋ ρ₀₁ ⁻¹ ×10⁻³ α² μ', fontsize=14)
fig.text(0.03, 0.65, 'math: $𝒜_C$ $\\mathcal{A}_C$ $\\hat{T}_M$ $\\oint$ $\\mathcal{H}_4$ $\\rangle$ ψ$_+$ ρ$_{01}$', fontsize=14)
fig.text(0.03, 0.45, 'math2: |Ψ$\\rangle$ $\\mathcal{H}_4$ T$_2$ = 50 μs', fontsize=14)
fig.savefig('C:/IALD/Central de Patentes/work/ro106_folhas_27out/_tmp/test_mpl.png', dpi=150)
print('ok')
