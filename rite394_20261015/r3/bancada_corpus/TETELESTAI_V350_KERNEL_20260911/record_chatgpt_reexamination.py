"""Record a scoped archive reexamination, preserving memory bytes and originals."""
import ast
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent
CENTRAL = ARCHIVE.parent
OUT = ROOT / 'REEXAME_CHATGPT_20260912'
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER = 'REEXAME_CHATGPT_REAPROVEITAMENTO_20260912'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

def link(path, label):
    assert path.is_file(), path
    return f'[{label}](<{path.as_posix()}>)'

inventory_path = OUT / 'inventory.json'
inventory = json.loads(inventory_path.read_bytes())
parent_path = ROOT / 'tomita_square_custody.json'
parent = json.loads(parent_path.read_bytes())
evidence_path = ROOT / 'kernel_incremental_evidence.json'
evidence = json.loads(evidence_path.read_bytes())
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == inventory['base_sha256']
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert inventory['inventory_returncode'] == 0
tree = ast.parse((ROOT / 'fontes/um_v350_original.py').read_bytes())
embedded = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets)))
names = ['general_smooth_gauge_invariance', 'general_source_einstein_from_area',
    'record_einstein_from_area', 'selected_metric_lorentz', 'selected_metric_smooth',
    'antiunitary_pairing_flip', 'closedAntilinearStandardSubspace',
    'exchange_heat_matching_iff', 'exchange_first_law', 'exchange_generator_global_cost']
rows = []
for name in names:
    matches = [k for k, v in embedded.items() if re.search(
        r'^(?:noncomputable )?(?:def|theorem|lemma) ' + name + r'\b', v, re.M)]
    audit = {k: v for k, v in evidence['axiom_report'].items() if k.endswith('.' + name)}
    assert all(set(v) <= {'propext', 'Classical.choice', 'Quot.sound'} for v in audit.values())
    rows.append({'name': name, 'v350_embedded_files': matches, 'existing_audit_entries': audit})
assert sum(bool(r['existing_audit_entries']) for r in rows) == 6
matched_names = {Path(r['path']).name for r in inventory['rows']
                 if r['v350_normalized_imports_equal']}
unique_hashes = {r['sha256'] for r in inventory['rows']}
source_records = {
    'reexame_v338': ARCHIVE / 'REEXAME_V338_FECHAMENTO_20260909/REEXAME_V338.md',
    'generic_adjoint': ARCHIVE / 'GenericAntilinearAdjoint.lean',
    'bounded_graph': ARCHIVE / 'BoundedGraphStandardSubspace.lean',
    'continuous_domain': ARCHIVE / 'ContinuousModularDomain.lean',
    'continuous_review_049': ARCHIVE / 'CONTINUACAO049_REVISAO_INDEPENDENTE.md',
    'continuous_review_050': ARCHIVE / 'CONTINUACAO050_REVISAO_INDEPENDENTE.md',
    'actual_standard_subspace_reuse': ROOT / 'kernel/TGLV350/ScalarTomitaStandardSubspace.lean',
    'general_gauge': ROOT / 'kernel/TGLExt/GeneralLinearizedGauge.lean',
    'selected_fisher': ROOT / 'kernel/TGLExt/SelectedFisherLorentzMetric.lean',
    'general_einstein': ROOT / 'kernel/TGLExt/GeneralSourceEinsteinBridge.lean',
    'response_record': ROOT / 'kernel/TGLExt/GravitationalResponseRecord.lean',
    'exchange_cost': ARCHIVE / 'ExchangeModularCost.lean',
    'exchange_entropy': ARCHIVE / 'ExchangeEntropyResponse.lean',
    'brst_class': ARCHIVE / 'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
    'brst_root_review': ARCHIVE / 'REVISOES_RAIZ_087_20260910/PARECER_CE_LINEAR_QUADRATICO_E_ALCANCE_087.md',
    'brst_independent_review': ARCHIVE / 'REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md',
    'brst_review_addendum': ARCHIVE / 'REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md',
    'new_root_review': ROOT / 'revisao/REVIEW_SCALAR_TOMITA_ROOT.md',
}
pins = {k: {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}
        for k, p in source_records.items()}
record = {'timestamp': DATE, 'inventory_sha256': sha(inventory_path),
    'listed_paths': inventory['listed_paths'], 'selected_source_paths': len(inventory['rows']),
    'selected_distinct_byte_hashes': len(unique_hashes),
    'normalized_matching_paths': inventory['normalized_matches'],
    'normalized_matching_basenames': len(matched_names), 'theorems': rows,
    'source_pins': pins, 'existing_audit_sha256': sha(evidence_path),
    'scope': 'Path inventory; selected source comparison; targeted mathematical and review reading. Not exhaustive content reading.',
    'new_compilation_for_archive_reexamination': False,
    'audit_read_is_not_fresh_compilation': True, 'gate_changed': False}
create(OUT / 'source_evidence.json', json.dumps(record, ensure_ascii=False, indent=2).encode())
report_path = OUT / 'RELATORIO_REAPROVEITAMENTO.md'
report = f'''# Reexame de Chatgpt: resultados existentes e elos que faltam

{DATE}. [REAL — leitura de fontes e evidências existentes; sem nova compilação do acervo]

Parte importante do trabalho já estava em Chatgpt e já foi incorporada à v350.
O diagnóstico deve localizar as hipóteses ainda não fornecidas pelos MESMOS dados,
em vez de apresentar construções genéricas existentes como teoremas ausentes.

## Escopo medido

`rg` inventariou {inventory['listed_paths']:,} caminhos `.lean`/`.md`, excluindo
`.lake`, `packages`, `build` e esta pasta de trabalho. Isso não significa leitura
integral desses arquivos. Foram lidas por script {len(inventory['rows'])} fontes
Lean selecionadas por nome e profundidade até dois, com {len(unique_hashes)} hashes
distintos. Há {inventory['normalized_matches']} caminhos correspondentes a
{len(matched_names)} nomes de módulos presentes na v350 após normalizar importações,
cabeçalho anterior ao primeiro import e fins de linha. Não são 261 provas novas;
a comparação normalizada também não é igualdade byte a byte.

{link(inventory_path, 'Inventário completo e método')}.
{link(OUT / 'source_evidence.json', 'Correspondências, seis entradas do Audit existente e pins')}.
Fontes profundas foram inventariadas, mas não exaustivamente lidas. As notas foram
lidas de modo dirigido: o reexame338, a composição BRST e seus pareceres completos;
os contratos pertinentes de geometria, Tomita e troca; trechos finais dos pareceres049/050.
Ausência nesta seleção não demonstra inexistência em todo o acervo.

## O que reaproveitar

| Frente | Resultado já localizado | O que ainda falta para a obrigação atual |
|---|---|---|
| Einstein | `general_source_einstein_from_area` e `record_einstein_from_area` estão na v350 e no Audit existente. | Entregar suavidade, estrutura lorentziana, conservação de T e limite da resposta de área no mesmo modelo selecionado. A implicação matemática já existe. |
| Métrica | `selected_metric_lorentz` e `selected_metric_smooth` constroem a métrica refletida de Fisher. | Fornecer `SelectedProbabilityData`: probabilidades positivas suaves, diferencial injetivo de posto quatro e diferencial selecionado não nulo; ligar esses dados ao peso/estado e à dinâmica exigidos. |
| Gauge | `general_smooth_gauge_invariance` vale para campos suaves gerais na geometria linearizada de Minkowski. | Essa prova clássica não constitui QME, carga BRST interagente ou ausência de anomalias quânticas. Corrige-se a descrição do acervo como restrito a ondas planas; o certificado físico consumido mantém seu alcance próprio. |
| Tomita | Há adjunto genérico, grafo limitado e subespaço padrão de operador antilinear fechado. `ScalarTomitaStandardSubspace` já importa e aplica o resultado antigo ao S atual. | `GenericAntilinearAdjoint` recebe J antiunitário e T; não constrói esse J a partir do S do peso atual. Seus lemas de pareamento poderão ser reutilizados depois dessa construção. |
| Modelo contínuo antigo | Multiplicação exponencial em L² da reta, com domínio ponderado, fechamento e auto-adjunticidade. | O modelo espectral fornecido não identifica automaticamente o operador atual em H_I, seu peso, fluxo KMS ou traço canônico. Os pareceres049/050 delimitam essa falta de identificação. |
| Troca microscópica | `ExchangeEntropyResponse`/`ExchangeModularCost` contêm primeira lei, custo e condições exatas de normalização do calor. | Os três nomes consultados não aparecem nas fontes embutidas nem no Audit atual. São candidatos de reaproveitamento, com compilação/compatibilidade ainda por conferir nesta rodada. A fonte contém também `exchange_no_common_heat_rate`: duas marginais fiéis diferentes não aceitam a mesma normalização térmica nesse protocolo. Não usar custo positivo como H3 físico automático. |
| BRST087 | Composição escrita e revisada de uma linha livre em H⁴ do BV–BRST clássico completo por valência; Pontryagin é exato no complexo completo. | Referência espaço-forma 4D, K>0 e sigma constante. Ainda faltam transporte ao setor físico, admissibilidade causal/contratermos, QME e rota UV. Não é compilação Lean nem anomalia física de ghost um. |

{link(source_records['reexame_v338'], 'Reexame338, lido integralmente')} já descrevia
essas distinções. {link(source_records['general_einstein'], 'Ponte de Einstein')},
{link(source_records['selected_fisher'], 'Dados e métrica de Fisher')},
{link(source_records['general_gauge'], 'Gauge geral linearizado')} e
{link(source_records['actual_standard_subspace_reuse'], 'Reuso literal no S atual')}.

{link(source_records['brst_independent_review'], 'Parecer independente da composição BRST')}
e {link(source_records['brst_review_addendum'], 'adendo que consome a revisão quadrática')}
foram lidos. A evidência autoriza registrar que essa revisão existe e tem alcance
delimitado; esta leitura não é uma nova validação integral das importações matemáticas.

## Efeito sobre o caminho crítico e a memória

[OPEN] Permanecem a identificação modular/KMS e o traço canônico do mesmo peso,
o canto contínuo/Three Locks e H1, H2 e H3 físicos compatíveis, o setor quântico
interagente e sua ligação efetiva ao certificado do gate. Não reabrir fase/ramo,
H3 interno ou implicações já demonstradas por homonímia com essas obrigações.

[REAL — etapa DEV atual, separada do reexame histórico] O parecer
{link(source_records['new_root_review'], 'da raiz de S†S')} foi lido integralmente:
cinco módulos/30 alvos recompilados pelo revisor, sem achados P0–P2. R=(I+A)⁻¹ é
limitado e B²=A no domínio exato; energia S/B apenas em D(A). A integração desses
cinco módulos ainda está pendente. D(B)=D(S), polar/KMS e traço não foram provados.
O rascunho `RealGraphCore.lean` teve rc1 e não é evidência aceita. A busca dirigida
não localizou uma prova anterior que já forneça essa igualdade para o H_I atual;
não se reivindica ausência global de tal teorema.

Gate legado inalterado; seis flags maiores falsas. Nenhum monólito foi executado
ou importado neste reexame. Original SHA256 `{sha(original)}`; cópia integrada
SHA256 `{sha(ROOT / 'um.py')}`. A atualização de memória registra reaproveitamento
e corrige o diagnóstico; não transforma consulta documental em prova nova.
'''
create(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[INPUT — solicitação do operador] “considere examinar na pasta \\chatgpt que vc
mesmo criou recentemente para trabalhar no fechamento do um.py se parte do que
busque já não está desenvolvido ali e atualize a sua memória”.

[REAL — reexame dirigido] Inventário de {inventory['listed_paths']} caminhos;
{len(inventory['rows'])} fontes Lean selecionadas, {len(unique_hashes)} hashes distintos;
{len(matched_names)} nomes de módulos com correspondência normalizada à v350.
Isso não é leitura integral do acervo nem nova compilação. Seis declarações
pertinentes foram localizadas no Audit existente, com apenas o trio permitido.

CORREÇÃO ADITIVA: a v350 já tem gauge linearizado para campos suaves gerais,
métrica lorentziana selecionada de Fisher e a implicação geral de Einstein por
área/conservação. Não descrevê-las como ausentes. Falta fornecer e ligar suas
hipóteses aos MESMOS dados físicos. O subespaço padrão antilinear antigo já é
reutilizado literalmente por ScalarTomitaStandardSubspace. O adjunto genérico
antigo recebe J/T e não constrói o J do peso atual. O modelo L² exponencial
antigo também exige uma identificação adicional com H_I.

[DERIVED escrito, com revisão localizada] BRST087 já trata uma linha livre em
H⁴ do complexo BV–BRST CLÁSSICO completo por valência e Pontryagin exato,
sob referência/sigma fixados. Não é QME, anomalia quântica de ghost um ou prova
Lean. Os módulos de troca055 consultados não estão na v350/Audit pelos nomes
verificados; são candidatos com controle negativo de normalização térmica,
sem promoção automática de H3. Fase/ramo e H3 interno não foram reabertos.

[REAL — DEV separado] Parecer da raiz de S†S lido: cinco módulos/30 alvos
recompilados independentemente, sem achados P0–P2. B²=A exato e energia em D(A);
integração pendente. D(B)=D(S), polar/KMS, traço, compatibilidades contínuas,
H1/H2/H3 físicos e setor quântico seguem abertos. Gate e seis flags inalterados;
sem runtime integral; objetivo integral ativo. Nenhum original alterado.

{link(report_path, 'Relatório do reexame, fontes, alcance e pontos de reaproveitamento')}.
'''
surfaces = [Path(p) for p in parent['surface_sha256']]
surfaces += [ROOT / 'RELATORIO_ADJUNTO_QUADRADO_INTEGRADO.md', ROOT / 'ROTA_POLAR_MESMO_GNS.md']
assert len(set(surfaces)) == len(surfaces)
before = {p: p.read_bytes() for p in surfaces}
backups = {}
for path, raw in before.items():
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert raw and MARKER.encode() not in raw
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as stream:
        stream.write(raw)
    assert backup.read_bytes() == raw
    backups[str(path)] = str(backup)
for path, raw in before.items():
    assert path.read_bytes() == raw, f'Concurrent edit: {path}'
    newline = '\r\n' if b'\r\n' in raw else '\n'
    updated = raw + note.replace('\n', newline).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(updated)
    assert temp.read_bytes() == updated and len(updated) > len(raw)
    assert path.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == updated and path.read_bytes().startswith(raw)
assert sha(original) == inventory['base_sha256'] and sha(ROOT / 'um.py') == parent['working_sha256']
assert all(sha(Path(row['path'])) == row['sha256'] for row in pins.values())
assert all(evidence[k] is False for k in parent['remaining_flags'])
custody = {'timestamp': DATE, 'marker': MARKER, 'parent_path': str(parent_path),
    'parent_sha256': sha(parent_path), 'original_sha256': sha(original),
    'working_sha256': sha(ROOT / 'um.py'), 'surface_sha256': {str(p): sha(p) for p in surfaces},
    'backups': backups, 'surface_before_sha256': {str(p): sha(Path(backups[str(p)])) for p in surfaces},
    'report_sha256': sha(report_path), 'inventory_sha256': sha(inventory_path),
    'source_evidence_sha256': sha(OUT / 'source_evidence.json'),
    'remaining_flags': {k: evidence[k] for k in parent['remaining_flags']},
    'memory_note_only': True, 'gate_changed': False, 'original_changed': False,
    'compilation_run_for_reexamination': False, 'full_goal_complete': False,
    'previous_custody_is_historical_after_this_append': True}
create(OUT / 'custody.json', json.dumps(custody, ensure_ascii=False, indent=2).encode())
verified = all(Path(backups[str(p)]).read_bytes() == before[p]
    and p.read_bytes().startswith(before[p]) and sha(p) == custody['surface_sha256'][str(p)]
    for p in surfaces)
assert verified
create(OUT / 'verification.json', json.dumps({'timestamp': DATE, 'custody_sha256': sha(OUT / 'custody.json'),
    'immediate_byte_backups_and_prefixes': len(surfaces), 'passed': verified,
    'original_and_working_copy_unchanged': True}, indent=2).encode())
print(json.dumps({'report': str(report_path), 'surfaces': len(surfaces),
    'custody_sha256': sha(OUT / 'custody.json'), 'verified': verified,
    'gate_changed': False}, ensure_ascii=False))
