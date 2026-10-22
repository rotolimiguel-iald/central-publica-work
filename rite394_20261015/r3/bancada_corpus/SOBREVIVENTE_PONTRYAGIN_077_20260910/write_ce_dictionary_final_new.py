from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'SOBREVIVENTE_PONTRYAGIN_077_20260910'
DRAFT = OUT / 'write_ce_dictionary_new.py'
SOURCES = [
    OUT / 'PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md',
    OUT / 'MANIFESTO_SOBREVIVENTE_PONTRYAGIN_077.json',
    ROOT / 'ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/RESULTADO_CE_EXATO_077.json',
    ROOT / 'compute_finite_ce077_run2.py',
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md',
    DRAFT,
]
EXTRA = r'''

## Precisões de leitura e da convenção KT

A reescala por √|K| em (D2) é somente um dicionário para o controle finito da álgebra de Killing com K fixo e não nulo. Ela não é usada na fórmula natural original α3=K m_ab p^ap^b+⅓tr(m³), que não contém divisão por K e permanece regular quando K varia. Não se introduz por esse controle uma categoria universal que permita coeficientes singulares em K.

A vírgula de separação na equação (7) da nota principal é apenas tipográfica. O primeiro coeficiente possível deve ser lido como o PRODUTO

\[
(A_P)_{[6]}=\rho_{[2]}[h,h]\,C^0C^1C^2C^3.
\tag{D5}
\]

ρ[2][h,h] é o coeficiente quadrático da densidade tr(W[1]∧W[1]); não é um argumento adicional do ghost nem uma operação de vírgula. Nada é alterado na fonte congelada.

O [adendo do sinal Koszul–Tate077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>) já corrige o sinal para s0u*=+H0u e conserva s0c*=+R0†u*. Foi lido integralmente para esta ponte. A construção de Pontryagin usa expressões sem antifields e somente sg/sc; seus líderes e suas correções até C5 não mudam com a correção. Isso não autoriza usar a convenção antiga em outros cálculos com antifields.

O primeiro script de emissão do dicionário havia sido criado, mas não executado, quando a raiz solicitou estas precisões. Foi conservado intacto. Este novo script lê somente sua string literal NOTE por AST/literal_eval e emite o adendo completo por escrita exclusiva. Nenhum código daquele rascunho ou do controle CE é executado/importado.
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
nodes = ast.parse(DRAFT.read_bytes()).body
values = [ast.literal_eval(n.value) for n in nodes if isinstance(n, ast.Assign)
          and any(isinstance(t, ast.Name) and t.id == 'NOTE' for t in n.targets)]
if len(values) != 1 or not isinstance(values[0], str):
    raise RuntimeError('DRAFT_LITERAL_NOT_UNIQUE')
note = values[0] + EXTRA
receipt = json.loads(SOURCES[2].read_bytes())
if receipt['source'] != before[3]:
    raise RuntimeError('CE_SCRIPT_PIN_MISMATCH')
note_path = OUT / 'DICIONARIO_CARTAN_DO_RECIBO_077.md'
emit(note_path, note.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
links = re.findall(r'\]\(<(C:/[^>]+)>\)', note)
if not all(Path(p).is_file() for p in links):
    raise RuntimeError('MISSING_LOCAL_LINK')
manifest = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'written_CE_dictionary_and_KT_precision',
    'status': 'DERIVED_WRITTEN_AWAITING_INDEPENDENT_REVIEW',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': True,
    'receipt_source_pin_matches_actual': True,
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': [{'path': p, 'exists': True} for p in links],
    'receipt_status_read': receipt['status'],
    'new_CAS_executions': 0,
    'new_Lean_executions': 0,
    'um_executed_or_imported': False,
    'CE_script_executed_or_imported_by_this_adendum': False,
    'draft_writer_executed_or_imported': False,
    'draft_consumed_only_as_AST_literal': True,
}
manifest_path = OUT / 'MANIFESTO_DICIONARIO_CARTAN_077.json'
emit(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'manifest': pin(manifest_path),
                  'sources_unchanged': True, 'source_count': len(before),
                  'local_links_existing': len(links)}, ensure_ascii=False))
