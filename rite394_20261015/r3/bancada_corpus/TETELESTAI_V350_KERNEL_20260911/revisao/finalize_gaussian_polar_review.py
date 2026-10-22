from pathlib import Path
import datetime
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
REVIEW = ROOT / 'revisao'
RUN = REVIEW / 'gaussian_polar_independent_20260912_210534_399150'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def link(path, label=None):
    path = Path(path)
    return f'[{label or path.name}](<{path.as_posix()}>)'

def create_atomic(path, data):
    path = Path(path)
    assert path.is_relative_to(REVIEW) and not path.exists()
    tmp = path.with_name(path.name + '.tmp_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(data)
    assert tmp.read_bytes() == data and len(data) > 0
    os.replace(tmp, path)
    assert path.read_bytes() == data

m = read_json(RUN / 'manifest.json')
c = read_json(RUN / 'compilation.json')
h = read_json(RUN / 'helper_static_inspection.json')
assert c['complete'] and all(v for k, v in c.items() if isinstance(v, bool))
assert len(c['records']) == 5 and len(m['declarations']) == 34
assert len(m['dependencies']) == 387 and len(m['memory_surfaces']) == 34
assert all(h['checks'].values()) and not h['findings_P0_P2']
assert all(sha(ROOT / n) == pin for n, pin in m['artifact_pins'].items())
assert sha(ROOT / 'um.py') == m['working_sha256']
assert sha(ROOT / 'gate_extension.py') == m['gate_sha256']
for rec in c['records']:
    assert rec['returncode'] == 0 and rec['axioms_allowed'] and rec['exact_targets']
    assert sha(rec['stdout']) == rec['stdout_sha256']
    assert sha(rec['stderr']) == rec['stderr_sha256']
    assert sha(rec['command'][-1]) == rec['source_sha256']
    assert sha(rec['command'][2]) == rec['output_sha256']
for rel, src in m['sources'].items():
    assert sha(src['path']) == src['sha256'] == sha(src['snapshot'])
    assert sha(src['author_binary']) == src['author_binary_sha256']
    assert sha(src['author_log']) == src['author_log_sha256']
audit = c['records'][-1]
assert set(audit['axioms']) == set(m['declarations'])
assert all(set(v) == {'propext', 'Classical.choice', 'Quot.sound'} for v in audit['axioms'].values())

now = datetime.datetime.now().astimezone().isoformat()
verification = {
    'timestamp': now,
    'scope': 'GAUSSIAN_POLAR_DEV_REVIEW',
    'review_complete': True,
    'findings_P0_P2': [],
    'own_recompiled_modules': 4,
    'own_auditors': 1,
    'exact_targets': 34,
    'all_exit_zero': True,
    'four_binaries_equal_author': True,
    'all_targets_exact_trio': True,
    'full_types_with_universes_read': True,
    'source_and_author_output_pins_rechecked_at_report': True,
    'compilation_sha256': sha(RUN / 'compilation.json'),
    'dependency_manifest_sha256': sha(RUN / 'manifest.json'),
    'audit_stdout_sha256': audit['stdout_sha256'],
    'author_manifest_sha256': sha(ROOT / 'gaussian_polar_draft_status.json'),
    'author_report_sha256': sha(ROOT / 'RELATORIO_POLAR_GAUSSIANO_CICLICO_DEV.md'),
    'dependency_origins': m['origins'],
    'inherited_project_dependencies': len(m['dependencies']),
    'author_project_build_in_lean_path': False,
    'libraries_rebuilt': False,
    'helper_static_inspection_sha256': sha(RUN / 'helper_static_inspection.json'),
    'helper_execution_by_reviewer': False,
    'integrated_review': False,
    'new_custody_or_memory_recording_certified': False,
    'preservation_checks': {k: v for k, v in c.items() if isinstance(v, bool)},
    'working_sha256': m['working_sha256'],
    'parent_custody_sha256': m['artifact_pins']['core_polar_custody.json'],
    'limitations': [
        'V is complex-linear and is not the original antilinear weight J.',
        'No identification of the cyclic-vector Tomita operator with the original weight S or J.',
        'No reverse commutant inclusion, KMS, trace, gate promotion or full runtime.',
        'Project dependencies and external libraries inherited; only four modules plus auditor rebuilt here.'
    ]
}
create_atomic(RUN / 'verification.json', (json.dumps(verification, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

origin, provenance = next(iter(m['origins'].items()))
rows = []
for rec in c['records'][:4]:
    src = m['sources'][rec['module']]
    rows.append(f"| {Path(rec['module']).stem} | {len(rec['axioms'])} | `{src['sha256']}` | `{rec['output_sha256']}` |")
author_logs = '\n'.join(
    f"- {link(src['author_log'])}: `{src['author_log_sha256']}`."
    for src in m['sources'].values()
)
helper_pins = '\n'.join(
    f"- `{name}`: `{pin['sha256']}`."
    for name, pin in h['pins'].items()
)

body = f'''# Parecer DEV — polar gaussiano e vetor cíclico separante

GAUSSIAN_POLAR_DEV_REVIEW

Data: {now}. Escopo encerrado: quatro módulos, 34 alvos (6+9+9+10), relatório, manifesto e cinco helpers. **Nenhum achado P0, P1 ou P2 identificado.** A conclusão resulta da leitura integral das fontes e tipos, recompilação independente e inspeção estática documental; não é parecer de integração.

[REAL] Foram executados somente os quatro módulos novos e um auditor próprio com `#check` (universos explícitos) e `#print axioms` de todos os 34 alvos. As cinco execuções terminaram rc0; cada alvo depende exatamente de `propext`, `Classical.choice`, `Quot.sound`. Os quatro `.olean` próprios coincidem byte a byte com os finais do autor. Os três rc1 históricos foram capturados e excluídos da evidência aceita, inclusive seus eventuais `sorryAx`.

| Fonte em `kernel/TGLV350` | Alvos | SHA256 da fonte | SHA256 do binário próprio = autor |
|---|---:|---|---|
{chr(10).join(rows)}

Conferências matemáticas e hipóteses:

- `DenseLinearPolarExtension.lean:16–45`: extensão complexa pela igualdade de normas sobre a imagem densa; essa igualdade também fornece a compatibilidade dos núcleos. A sobrejetividade utiliza a densidade de `f` e a imagem fechada da isometria com domínio completo. As hipóteses genéricas estão explícitas; não se pressupõe inversa limitada.
- `BoundedInjectivePolar.lean:15–83`: `D=√(C* C)` é positivo, `‖Dx‖=‖Cx‖`; injetividade de C fornece injetividade e imagem densa de D. A unitária linear V satisfaz `V D=C`. O transporte exige e usa ambos `C A=B C` e `C A*=B* C`; o segundo dá `A C*=C* B`, portanto a comutação do Gram e de sua raiz. Não foi presumida a conclusão de entrelaçamento, nem um gap espectral.
- `ScalarGaussianImage.lean:15–93`: K é o fecho da imagem do mapa gaussiano C no L² ambiente. A pertinência de Ωg a K usa médias com h>0, a cota uniforme e o limite forte já construído. A igualdade `K=closure(ρ(N)Ωg)` tem as duas inclusões provadas. `C_K:H_I→K` é injetivo e tem imagem densa nesse contradomínio; não se afirma sobrejetividade de C no ambiente inteiro. Não há inversão limitada da gaussiana nem hipótese de separabilidade ou interseção a.e. não enumerável.
- `ScalarGaussianUnitary.lean:12–84`: a restrição a K usa invariância por todos A∈N, inclusive A*. Os dois entrelaçamentos exigidos pelo auxiliar são descarregados pela mesma representação e suas leis de estrela. V é aplicada ao H_I original, e `ξ=V⁻¹Ωg` pertence a esse H_I. A órbita `π(N)ξ` é densa e `π(A)ξ=0⇒A=0`, usando a separação gaussiana anterior para ρ(N), não para todos os operadores do L² ambiente. Nenhuma hipótese adicional sobre P ficou residual nos tipos concretos.

A construção conserva o mapa C anterior, `dualHaarFactor`, `regularVacuum` e π. A densidade de Λ(I) é reutilizada com seu domínio efetivo, sem impor I=nν. O auditor confirma os tipos concretos para `P : SiteProfile`; os auxiliares Hilbert estão declarados em `Type`, sem alegação adicional de generalidade de universos.

[REAL] **Proveniência da recompilação.** A árvore própria é {link(RUN, RUN.name)}. Foram congeladas 387 dependências de projeto a partir de {link(Path(origin), Path(origin).name)}, com fontes e binários confrontados por hash. O manifesto dessa origem tem SHA `{provenance['manifest_sha256']}` e sua conclusão de compilação `{provenance['compilation_sha256']}`. A lista individual com caminhos de origem, fontes, binários e hashes está no {link(RUN / 'manifest.json')}; esses 387 módulos não foram recompilados nesta rodada.

O `LEAN_PATH` contém exclusivamente o build próprio e os oito pacotes externos readonly sob `Nós/tgl_kernel/.lake/packages` (Mathlib, aesop, batteries, importGraph, LeanSearchClient, plausible, proofwidgets e Qq). Não contém o build autoral de projeto. Lean 4.31.0, executável SHA `{m['compiler_sha256']}`. Os pacotes não foram reconstruídos; os pins externos diretamente conferidos estão no manifesto. Esta é reprodução dos quatro novos contra dependências herdadas, não reconstrução independente de toda a biblioteca.

Evidência própria: {link(RUN / 'compilation.json')} SHA `{sha(RUN / 'compilation.json')}`; {link(Path(audit['stdout']), 'auditor: tipos e axiomas')} SHA `{audit['stdout_sha256']}`; {link(RUN / 'verification.json')} SHA `{sha(RUN / 'verification.json')}`. A verificação final confirmou preservação das fontes/binários autorais, dependências, arquivos anteriores de revisão, 34 superfícies de memória e seus backups, monólito e gate.

Logs finais autorais conferidos separadamente, com fonte/binário/stdout/stderr pinados no manifesto próprio:

{author_logs}

O manifesto autoral `gaussian_polar_draft_status.json` tem SHA `{sha(ROOT / 'gaussian_polar_draft_status.json')}`; o relatório lido integralmente `RELATORIO_POLAR_GAUSSIANO_CICLICO_DEV.md`, `{sha(ROOT / 'RELATORIO_POLAR_GAUSSIANO_CICLICO_DEV.md')}`. A mãe matemática e documental é `core_polar_custody.json`, SHA `{m['artifact_pins']['core_polar_custody.json']}`. A cópia continua no estrato anterior, SHA `{m['working_sha256']}`. Nenhum número futuro de integração é certificado aqui.

Inspeção estática dos helpers, **sem executá-los**:

- Maker e recorder de draft preservam o estatuto DEV; os rc0 aceitos são escolhidos pelos pins finais. Preparador exige leitura do parecer e confere a mãe e os artefatos. A simulação textual em memória confirmou quatro entradas novas, batch 491→525, ordem de compilação antes das raízes e o controle `gaussian_unitary_and_same_GNS_cyclic_separating_vector_does_not_discharge_KMS_trace_or_physical_frontier`. Nenhuma transposição foi aplicada por esta revisão.
- Recorder e verifier futuros conferem evidência de integração, fontes e binários dos registros, Audit bruto atual e histórico, fronteira e marcadores dos pareceres. As 34 superfícies vêm da mesma mãe core_polar. O plano usa backup dos bytes imediatamente anteriores, preservação de prefixo/crescimento e troca por temporário verificado, por arquivo; não promete transação única das 34 escritas. A leitura estática não certifica uma futura execução nem uma custódia nova já gravada.
- O texto mantém V linear distinto do J antilinear do peso e mantém a inclusão inversa de comutantes, KMS e traço abertos. Não encontrei promoção indevida no controle novo ou nos templates. Os seis flags permanecem falsos no estrato lido; monólito e `gate_extension.py` permaneceram idênticos.

Pins dos helpers efetivamente lidos:

{helper_pins}

A captura {link(RUN / 'helper_static_inspection.json')} registra a inspeção e as transformações ainda não aplicadas, SHA `{sha(RUN / 'helper_static_inspection.json')}`.

[OPEN] O resultado útil é uma unitária linear entre H_I e o espaço cíclico gaussiano e um vetor cíclico separante na **mesma π**. Esse vetor não é afirmado normalizado nem representante do peso infinito original. Seu Tomita/J não foi identificado com S/J do peso: não se pode extrair essa identificação apenas de `V|C|=C` e do entrelaçamento da álgebra. Permanecem fora deste pacote a inclusão inversa com o mesmo J, a igualdade global de comutantes, identificação modular/KMS, traço e runtime integral. Nenhum gate/QG é aprovado.

**Revisão DEV delimitada concluída, sem análise necessária pendente nos quatro módulos/34 alvos e nos helpers estáticos. Integração futura exige conferência própria de seus artefatos.** Pareceres anteriores e memórias preservados; todas as saídas desta revisão estão em `revisao/`.
'''
destination = REVIEW / 'REVIEW_GAUSSIAN_POLAR_DEV.md'
create_atomic(destination, body.encode('utf-8'))
print(json.dumps({'report': str(destination), 'report_sha256': sha(destination), 'bytes': destination.stat().st_size, 'lines': len(body.splitlines()), 'verification_sha256': sha(RUN / 'verification.json'), 'findings_P0_P2': []}, ensure_ascii=False))
