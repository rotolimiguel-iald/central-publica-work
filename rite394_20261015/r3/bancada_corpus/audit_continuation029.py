"""Exact-byte and Lean-output audit for spontaneous continuation 029.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['PlaneWaveSolder', 'PlaneWaveConnection', 'PlaneWaveCurvature', 'PlaneWaveMatter', 'PlaneWaveEntropyMatching', 'PlaneWaveReconstructionControls']
MANIFEST = ROOT / 'CONTINUACAO029_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_029_ESPONTANEA_geometria_curva_e_liberdade_residual.md'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def read(path):
    raw = path.read_bytes()
    return raw.decode('utf-16' if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else 'utf-8-sig')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_bytes(path, raw):
    if not path.resolve().is_relative_to(ROOT) or path.exists():
        raise RuntimeError(f'Output refused: {path}')
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    if temp.stat().st_size != len(raw) or temp.read_bytes() != raw:
        raise RuntimeError(f'Incomplete output: {temp}')
    temp.rename(path)


def write_new(path, value):
    write_bytes(path, value.encode('utf-8'))


def runs(module):
    records = []
    for meta in sorted(ROOT.glob(module + '.*.json')):
        data = json.loads(read(meta))
        log = ROOT / data['log']
        output = read(log)
        rejected = data['exit_code'] != 0 or bool(re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', output))
        label = ('failed_compile' if data['exit_code'] else
                 'rejected_warning')
        archive = log.with_name(log.stem + '.' + label + '.log') if rejected else None
        records.append((meta, data, log, output, archive))
    return records


def preserve_attempts():
    for module in MODULES:
        for _, _, log, _, archive in runs(module):
            if archive is not None:
                if archive.exists():
                    if archive.read_bytes() != log.read_bytes():
                        raise RuntimeError(f'Archive mismatch: {archive}')
                else:
                    write_bytes(archive, log.read_bytes())


def axiom_rows(output):
    rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)
    result = [{'declaration': n, 'axioms': [a.strip() for a in v.split(',') if a.strip()]} for n, v in rows]
    if any(not set(row['axioms']) <= ALLOWED for row in result):
        raise RuntimeError('Unexpected axiom dependency')
    return result


def inspect_module(module):
    source = ROOT / (module + '.lean')
    code = read(source)
    namespaces = re.findall(r'^namespace ([\w.]+)', code, re.M)
    if len(namespaces) != 1:
        raise RuntimeError(f'Unexpected namespace structure: {module}')
    namespace = namespaces[0]
    if namespace != 'ChatgptAudit.Wave029':
        raise RuntimeError(f'Unexpected namespace: {module}')
    if re.search(r'\b(sorry|admit|axiom)\b', code):
        raise RuntimeError(f'Forbidden declaration: {source}')
    declarations = re.findall(r'^(theorem|def)\s+([\w.]+)', code, re.M)
    theorems = [name for kind, name in declarations if kind == 'theorem']
    prints = re.findall(r'^#print axioms ([\w.]+)', code, re.M)
    if not set(theorems) <= set(prints) or len(prints) != len(set(prints)):
        raise RuntimeError(f'Theorem print coverage mismatch: {module}')
    if not set(prints) <= {name for _, name in declarations}:
        raise RuntimeError(f'Unknown printed declaration: {module}')
    attempts = runs(module)
    candidates = [r for r in attempts if r[1]['exit_code'] == 0 and r[1]['source_stable']
                  and r[1]['proof_sha256'].lower() == digest(source) and r[4] is None]
    if not candidates:
        raise RuntimeError(f'No clean compilation for exact final source: {module}')
    meta, data, log, output, _ = candidates[-1]
    if 'sorryAx' in output:
        raise RuntimeError(f'Unproved final dependency: {module}')
    axioms = axiom_rows(output)
    if sorted(row['declaration'] for row in axioms) != sorted(namespace + '.' + name for name in prints):
        raise RuntimeError(f'Qualified axiom names mismatch: {module}')
    paths = {source, source.with_suffix('.olean')}
    paths.update(ROOT.glob(module + '.lean.bak_*'))
    history = []
    source_versions = {digest(source)} | {digest(p) for p in ROOT.glob(module + '.lean.bak_*')}
    for m, d, l, out, archive in attempts:
        if d['proof_sha256'].lower() not in source_versions or not d['source_stable']:
            raise RuntimeError(f'Historical source missing or unstable: {m}')
        paths.update([m, l])
        if archive is not None:
            if not archive.exists() or archive.read_bytes() != l.read_bytes():
                raise RuntimeError(f'Failed attempt not preserved: {l}')
            paths.add(archive)
        history.append({'metadata': str(m), 'log': str(l), 'exit_code': d['exit_code'],
                        'record_kind': 'bench_interruption_note' if out.startswith('BENCH INTERRUPTION RECORD') else 'lean_compiler_output',
                        'source_sha256': d['proof_sha256'].lower(),
                        'rejected_copy': str(archive) if archive else None,
                        'issues': [line for line in out.splitlines()
                                   if re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', line)]})
    return {'module': module, 'namespace': namespace, 'theorems': len(theorems), 'printed_definitions': len(prints)-len(theorems),
            'helper_definitions_not_separately_printed': [n for k, n in declarations if k == 'def' and n not in prints],
            'final_metadata': str(meta), 'final_log': str(log), 'axioms': axioms, 'attempts': history}, paths



def inventory():
    records, paths = [], set()
    for module in MODULES:
        record, items = inspect_module(module)
        records.append(record)
        paths.update(items)
    visited, order = set(), []

    def visit(module):
        path = ROOT / (module.replace('.', '/') + '.lean')
        if module in visited or not path.exists():
            return
        visited.add(module)
        for imported in re.findall(r'^import\s+(\S+)', read(path), re.M):
            visit(imported)
        order.append(module)
        paths.add(path)
        if path.with_suffix('.olean').exists():
            paths.add(path.with_suffix('.olean'))

    visit('PlaneWaveReconstructionControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation029.py', 'revise_continuation029.py', 'verify_stage.ps1',
        'CONTINUACAO029_DERIVACAO_PREVIA.md', 'CONTINUACAO029_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO028_MANIFESTO.json', 'audit_continuation028.py', 'CONTINUACAO027_MANIFESTO.json', 'audit_continuation027.py', 'CONTINUACAO026_MANIFESTO.json', 'audit_continuation026.py', 'CONTINUACAO025_MANIFESTO.json', 'audit_continuation025.py', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean', 'fontes/tgl_kernel/TGLExt/SignatureInTheLimit.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO029_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation029.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation029.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'Spontaneous continuation 029 of order 007; explicit curved family, not a microscopic derivation of H3', 'reuse': ['Actual global faithful product states and joint entropy response of 026-028', 'Previously constructed local equilibrium screens, heat, Raychaudhuri and conditional Einstein theorem', 'Actual frame Levi-Civita, coordinate Riemann/Ricci and conserved scalar covector stress'], 'paid': ['Smooth globally invertible null rank-one solder and explicit metric/inverse in the existing four-dimensional chart', 'First derivatives of the metric and equality of proposed connection with the actual Levi-Civita connection', 'Explicit coordinate curvature, Ricci, zero scalar curvature and Einstein tensor', 'Parallel exact null covector, wave equation and conserved nonzero scalar stress', 'All-screen area matching for an explicit curved family selected from the entropy coefficient; no harea hypothesis in the matched family theorem', 'Exact Einstein equation with Lambda=0, plus reuse of full local area-to-Einstein reconstruction', 'Actual state-read entropy and geometric area match in the arbitrary joint cutoff/time limit', 'Necessary trace coefficient, refusal of wrong trace, and residual curvature freedom at equal Ricci/matter', 'Vacuum nonflat control and a nonzero-source control from the geometric amplitude'], 'inputs_and_unpaid': ['The metric ansatz, four-dimensional Lorentzian reference, scalar covector and entropy family are specified inputs. This is an existence construction inside that class, not derivation of general geometry from omega(I)=1.', 'The sum of transverse coefficients is chosen to satisfy the area matching. Its successful construction is not an independent microscopic dynamics forcing that choice. H3 remains OPEN for the general objective.', 'The difference of those coefficients remains a free real parameter. Equal entropy, Ricci and matter do not select the tested curvature coordinate. No global non-isometry classification is inferred merely from components.', "The eta coefficient must be nonzero in the area theorem. The direct algebraic Einstein formula also holds at eta=0 under Lean's total division convention; that degenerate formula is not a physical area-matching assertion.", 'The matter source is a massless scalar with a parallel null gradient. No classification of general quantum matter, physical selection of eta or Newton units, region-algebra correspondence, correlations or positive-energy spacetime translations is supplied.', 'The state-read limits are those of specified diagonal prefix functionals. Araki identification, full path differentiability, and a general quantum gravitational theory are not established.', 'Only exact final clean compilations support the delivery. Counts include helper lemmas and controls; no count measures completion of the broad proof.', 'Canonical originals, um.py, Atlas, memories, gates, seals and earlier deliveries remain untouched. Managerial independent audit/incorporation remain pending.'], 'criteria': [['Derivacao anterior ao codigo', 'PAGO', 'CONTINUACAO029_DERIVACAO_PREVIA.md; auditor 028 reconferido.'], ['Metrica e inversa reais', 'PAGO', 'wave_solder_inverse, wave_inverse_solder, wave_metric_formula, wave_inverse_metric_formula.'], ['Conexao calculada', 'PAGO', 'wave_metric_jet e wave_levi_civita, com derivadas de fderiv.'], ['Curvatura calculada', 'PAGO', 'wave_ricci, wave_scalar_curvature, wave_einstein, wave_first_curvature e wave_second_curvature.'], ['Materia escalar conservada', 'PAGO', 'wave_covector_parallel, wave_covector_wave, wave_covector_potential e wave_matter_conserved.'], ['Habitante curvo de harea', 'PAGO NA FAMILIA ESCOLHIDA', 'matched_wave_area e matched_constructed_area, em todos os pontos e telas locais.'], ['Calor e Einstein', 'PAGO NA FAMILIA ESCOLHIDA', 'wave_heat_matching, matched_wave_einstein e matched_wave_einstein_from_area.'], ['Resposta lida dos estados', 'PAGO', 'wave_read_entropy_joint e matched_read_area_joint; marginais e fidelidade de 026-028.'], ['Controle da escolha e liberdade', 'PAGO', 'wave_origin_area_iff, wave_wrong_trace_refused, zero_eta_nonzero_source_refused, matched_curvature_distinguishes e state_alone_not_curvature_coordinate.'], ['Controles nao triviais', 'PAGO', 'zero_wave_vacuum, zero_wave_nonflat, geometric_wave_matter_nonzero e geometric_wave_curved.'], ['Dinamica microscopica geral e prova ampla', 'NAO PAGO', 'A geometria foi selecionada dentro de um ansatz. A lei de area geral e a selecao da liberdade radiativa permanecem abertas.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1. This is not a portable full bundle or an independent recompilation.'},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'PlaneWaveReconstructionControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


INTRO = ['[REAL / INPUT / OPEN] ENTREGA 029 ESPONTANEA - geometria curva, casamento entropico e liberdade residual.', '', '06/09/2026. Continuacao da ordem 007 e da entrega 028. O objetivo amplo permanece aberto; auditoria independente da gerencia pendente.', '', 'Foi construida uma familia classica de metricas de onda plana, em todo R4, ligada aos estados globais reais da 028. Com eta4=diag(1,-1,-1,-1), k=(1,0,0,1), l=(1,0,0,-1), H=a*x^2+c*y^2, o coframe E=I+(H/2)(l tensor k) tem inversa D=I-(H/2)(l tensor k). O kernel calcula g=eta4+H(k tensor k), a inversa, sua Levi-Civita, Ric=(a+c)(k tensor k), R=0 e G=Ric.', '', 'O covetor constante k foi provado paralelo, nulo na metrica inversa e igual ao gradiente da funcao t+z. Sua equacao de onda e a conservacao do tensor escalar T=kappa(k tensor k) sao demonstradas. Para os estados da 028, kappa=log(2)*sum(b)/pi.', '', 'Para eta nao zero, define-se r=2*pi*kappa/eta, a=r/2+s e c=r/2-s. A condicao harea foi demonstrada nessa FAMILIA ESCOLHIDA, para toda tela de equilibrio local em todo ponto e direcao nula nao zero. O calor corresponde e a equacao G=(2*pi/eta)T vale com Lambda=0. A cadeia geral anterior de area para Einstein tambem foi instanciada, sem harea como hipotese no teorema final da familia.', '', 'A resposta entropica e ligada as probabilidades efetivamente lidas dos estados: o defeito entre a entropia lida e a area tende a zero, dividido pelo tempo ao quadrado, no limite conjunto arbitrario de corte e tempo (matched_read_area_joint). Nao se define entropia a partir da area.', '', 'Controle adversarial: na origem, a correspondencia exige exatamente eta*(a+c)=2*pi*kappa. Coeficiente errado falha. O parametro s permanece livre: Ric e materia ficam iguais, as metricas coincidem na origem, mas as componentes de curvatura diferem e R^1_(0 1 0)-R^2_(0 2 0)=2*s. Isso prova subdeterminacao da coordenada de curvatura no ansatz; nao e uma classificacao de metricas modulo isometria.', '', 'Com b=0 e s nao zero, Ric=0 e a curvatura e nao nula. Com o perfil geometrico da 028 e eta nao zero, ha materia nao nula e geometria curva correspondente.', '', '[INPUT / OPEN] Selecionar o ansatz e ajustar a soma dos coeficientes a resposta fornece existencia. Nao demonstra uma dinamica microscopica que force esse ajuste. H3 geral, regiao-algebra, origem da assinatura/dimensao, correlacoes e materia quantica geral permanecem abertos.', '', '[KNOWN] A classe geometrica tem antecedentes classicos: [David Tong, General Relativity, secao 5.2.3](https://davidtong.org/teaching/general-relativity/grhtml/S5) apresenta ondas de Brinkmann e a liberdade de perfil sem traco no vacuo; [Harte e Drivas, Physical Review D 85, 124039](https://link.aps.org/accepted/10.1103/PhysRevD.85.124039) apresenta a curvatura e Ricci de pp-waves. As formulas e os sinais desta bancada foram verificados por Lean; nenhum resultado externo entrou como axioma.']


def delivery_text(data):
    rows = INTRO[:]
    rows += ['', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes impressas. Contagens incluem auxiliares.",
             'Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.',
             '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
             f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation029.py'}'", '\u0060\u0060\u0060',
             '', 'Comando somente leitura; recompilacao independente em copias, na ordem do manifesto:']
    rows.extend('- '+str(ROOT / (module+'.lean')) for module in MODULES)
    rows += ['', '## Axiomas', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration']+': ['+', '.join(item['axioms'])+']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos',
             '', f"Manifesto: {MANIFEST}; SHA256 dos bytes: {digest(MANIFEST)}.",
             f"Inventario: {len(data['files'])} caminhos, com tamanho e SHA256.",
             '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m+'.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO029_DERIVACAO_PREVIA.md','CONTINUACAO029_PARECER.md','audit_continuation029.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| {item['path']} | {item['sha256']} |")
    rows += ['', '## Tentativas rejeitadas preservadas', '']
    rejected = 0
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rejected += 1
                rows.append(f"- {run['rejected_copy']}: exit {run['exit_code']}; copia dos bytes do log.")
    rows += ['', f'{rejected} tentativas rejeitadas preservadas com logs e fontes em backups dos bytes.',
             '', '## Limites e dividas', '']
    rows.extend('- '+item for item in data['inputs_and_unpaid'])
    rows += ['', 'Parecer: '+str(ROOT / 'CONTINUACAO029_PARECER.md'),
             '', 'Ordens encontradas:']
    rows.extend('- '+p for p in data['incoming_orders'])
    return '\n'.join(rows)+'\n'

def verify_custody():
    data = json.loads(read(MANIFEST))
    for item in data['files']:
        path = Path(item['path'])
        if path.stat().st_size != item['bytes'] or digest(path) != item['sha256']:
            raise RuntimeError(f'Custody mismatch: {path}')
    for module in data['modules']:
        source = ROOT / (module['module'] + '.lean')
        metadata = json.loads(read(Path(module['final_metadata'])))
        output = read(Path(module['final_log']))
        if (metadata['exit_code'] != 0 or not metadata['source_stable'] or
                metadata['proof_sha256'].lower() != digest(source) or
                'sorryAx' in output or re.search(r'\b(error|warning)(?:\([^\n]*?\))?:', output)):
            raise RuntimeError(f'Invalid final compilation: {module["module"]}')
        if axiom_rows(output) != module['axioms']:
            raise RuntimeError('Axiom inventory changed')
        code = read(source)
        if re.findall(r'^namespace ([\w.]+)', code, re.M) != [module['namespace']]:
            raise RuntimeError('Namespace changed')
        if len(re.findall(r'^theorem\s+', code, re.M)) != module['theorems']:
            raise RuntimeError('Theorem count changed')
        prints = re.findall(r'^#print axioms ([\w.]+)', code, re.M)
        if sorted(module['namespace'] + '.' + n for n in prints) != sorted(r['declaration'] for r in module['axioms']):
            raise RuntimeError('Axiom coverage changed')
    if delivery_text(data) != read(DELIVERY):
        raise RuntimeError('Delivery does not match the pinned inventory')
    print(f"PASS: {len(data['files'])} byte hashes; {len(data['modules'])} clean Lean modules; "
          f"{data['theorems']} declared theorems; {data['printed_definitions']} printed definitions; delivery verified")


if __name__ == '__main__':
    if sys.argv[1:] == ['--write']:
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_029_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_029_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 029 already occupied; refusing publication')
        preserve_attempts()
        data = inventory()
        write_new(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        write_new(DELIVERY, delivery_text(data))
        verify_custody()
        print(json.dumps({'modules': len(data['modules']), 'theorems': data['theorems'],
                          'printed_definitions': data['printed_definitions'], 'files': len(data['files']),
                          'delivery': str(DELIVERY), 'delivery_sha256': digest(DELIVERY)}, ensure_ascii=False))
    elif not sys.argv[1:]:
        verify_custody()
    else:
        raise SystemExit('Usage: audit_continuation029.py [--write]')

