from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'SOBREVIVENTE_PONTRYAGIN_077_20260910'
SOURCES = [
    OUT / 'PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md',
    OUT / 'MANIFESTO_SOBREVIVENTE_PONTRYAGIN_077.json',
    ROOT / 'ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/RESULTADO_CE_EXATO_077.json',
    ROOT / 'compute_finite_ce077_run2.py',
]
NOTE = r'''# Dicionário com o controle CE exato da raiz

10/09/2026. [DERIVED — comparação algébrica escrita]. Adendo novo à [construção de Pontryagin até C5](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>), preservada. O [recibo CE da raiz](<C:/IALD/Central de Patentes/Chatgpt/ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/RESULTADO_CE_EXATO_077.json>) foi lido, não reexecutado.

O recibo registra as três assinaturas, dimensões invariantes 0/4/3 nos graus 2/3/4, posto três e núcleo unidimensional do primeiro diferencial, com linha do Cartan. Esta é evidência aritmética finita produzida pela raiz; não equivale a uma auditoria aqui do código inteiro ou do BRST de jatos. A construção sem antifields da nota principal independe da precisão separada do sinal KT077.

Para comparar representantes e não só dimensões, use precisamente a convenção registrada: X_ab[a,b]=ε_a, X_ab[b,a]=−ε_b e dθ_k=−Σ_(i<j) f_ij^k θ_iθ_j. Ponha

\[
\Theta=\sum_{a<b}\theta_{ab}X_{ab},\qquad d\Theta=-\Theta^2.
\tag{D1}
\]

Separando os índices tangentes 0,…,3 e o normal 4, a matriz tem a forma

\[
\Theta=\begin{pmatrix}M&u\\-\varepsilon_4u^\flat&0\end{pmatrix},
\qquad u^a=\varepsilon_a\theta_{a4},
\quad g_{ab}=\varepsilon_a\delta_{ab}.
\tag{D2}
\]

Para a normalização |K|=1, escolha K=ε4 e p=u. Assim a componente tangente de (D1) é dM=−M²+Kpp♭ e dp=−Mp, na convenção da nota principal. Para |K| distinto de um, u=√|K| p e ε4=sign(K) dão o mesmo dicionário após a reescala do setor de translações. Essa mudança de geradores não exige nem introduz uma raiz de K negativo.

Expandir o cubo de (D2) e usar a ciclicidade graduada dá

\[
\operatorname{tr}(\Theta^3)
=\operatorname{tr}(M^3)-3\operatorname{tr}(M Kpp^\flat).
\tag{D3}
\]

Por outro lado, defina a forma de Cartan na convenção do recibo por

\[
\mathscr C=\sum_{i<j<k}
\operatorname{tr}(X_i[X_j,X_k])\theta_i\theta_j\theta_k.
\]

As seis permutações de cada produto no traço do cubo de Θ dão três vezes esse coeficiente. Logo

\[
\boxed{\alpha_3=\operatorname{tr}(M Kpp^\flat)
-\tfrac13\operatorname{tr}(M^3)
=-\tfrac13\operatorname{tr}(\Theta^3)=-\mathscr C.}
\tag{D4}
\]

Isso fixa o sinal global na convenção CE da raiz. No controle espacial θ12θ13θ23, correspondente aos índices 4/5/7 da lista basis_pairs do recibo, Cartan tem coeficiente +2 nas três assinaturas registradas. A expressão (D4) tem coeficiente −2. A mudança m_ab=∇_[a C_b] para M_ab=−m_ab já foi explicitada na nota principal; ela não pode ser omitida numa comparação de componentes.

[DERIVED] O líder de Pontryagin é a negativa da cúbica de Cartan registrada, portanto gera a mesma linha sobrevivente. Isso complementa o controle de não nulidade da nota principal e a construção até C5; não modifica seus limites em valência seis e nas ordens posteriores.

[REAL — documental] Pins do recibo, do seu script e das duas fontes próprias foram medidos antes/depois, sem importar ou executar o script CE. O manifesto deste adendo não substitui o manifesto anterior. Zero novos CAS, Lean ou um.py; nenhuma aprovação por outro revisor atribuída.
'''


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def emit(path, data):
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if tmp.read_bytes() != data:
        raise RuntimeError('TEMP_BYTE_MISMATCH')
    if path.exists():
        raise FileExistsError(path)
    tmp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('FINAL_BYTE_MISMATCH')


before = [pin(path) for path in SOURCES]
receipt = json.loads(SOURCES[2].read_bytes())
source_record = receipt['source']
if source_record != before[3]:
    raise RuntimeError('CE_SCRIPT_PIN_MISMATCH')
note_path = OUT / 'DICIONARIO_CARTAN_DO_RECIBO_077.md'
emit(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
manifest = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'written_CE_convention_dictionary',
    'status': 'DERIVED_WRITTEN_AWAITING_INDEPENDENT_REVIEW',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': True,
    'receipt_source_pin_matches_actual': source_record == before[3],
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'receipt_status_read': receipt['status'],
    'new_CAS_executions': 0,
    'new_Lean_executions': 0,
    'um_executed_or_imported': False,
    'CE_script_executed_or_imported_by_this_adendum': False,
}
manifest_path = OUT / 'MANIFESTO_DICIONARIO_CARTAN_077.json'
emit(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'manifest': pin(manifest_path), 'sources_unchanged': True}, ensure_ascii=False))
