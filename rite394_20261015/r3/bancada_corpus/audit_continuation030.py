"""Exact-byte and Lean-output audit for spontaneous continuation 030.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['SiteLogLikelihood', 'SummableLikelihoodGenerator', 'LikelihoodCocycle', 'LikelihoodPreparedState', 'LikelihoodStateCovariance', 'LikelihoodCocycleControls']
MANIFEST = ROOT / 'CONTINUACAO030_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_030_ESPONTANEA_cociclo_global_e_leitura_angular.md'
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
    if namespace != 'ChatgptAudit.Cocycle030':
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

    visit('LikelihoodCocycleControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation030.py', 'revise_continuation030.py', 'verify_stage.ps1',
        'CONTINUACAO030_DERIVACAO_PREVIA.md', 'CONTINUACAO030_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO029_MANIFESTO.json', 'audit_continuation029.py', 'CONTINUACAO028_MANIFESTO.json', 'audit_continuation028.py', 'CONTINUACAO027_MANIFESTO.json', 'audit_continuation027.py', 'CONTINUACAO026_MANIFESTO.json', 'audit_continuation026.py', 'CONTINUACAO025_MANIFESTO.json', 'audit_continuation025.py', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/Cocycle.lean', 'fontes/tgl_kernel/TGLExt/Ergodicity.lean', 'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean', 'fontes/tgl_kernel/TGLExt/SignatureInTheLimit.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO030_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation030.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation030.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'Spontaneous continuation 030 of order 007; global cocycle for a summable commuting product family, with quadratic phase test', 'reuse': ['Faithful global product states and modular transport of 026-027', 'Summable profile family and relative entropy limits of 028', 'Finite modular cocycle and diagonal logarithms already in TGLExt'], 'paid': ['Norm-summable bounded self-adjoint log-likelihood generator in the factor, fixed by the reference modular flow', 'Norm-continuous unitary cocycle, twisted law, and norm limit of actual finite cocycles', 'Positive invertible exponential filter preparing exactly the previously built global vector/state; normalization omega(exp L)=1', 'Exact intertwining of the two modular automorphism groups on every element of the factor via its double commutant', 'Expectation of the global generator equals the previously established finite-prefix relative entropy limit', 'Zero-amplitude and nontrivial infinite-profile controls', 'Positive quadratic phase observable, vector norm interpretation, operator-norm modular small-time limit to L squared, and quantitative fourth-order bound in the state parameter'], 'inputs_and_unpaid': ['The family is specified: reference (1/3,2/3), 0<=b_n<=1/12, summable b, h(t)=t^2/(1+t^2). It is a commuting perturbation, not a theorem about every pair of faithful states.', 'The relative unbounded Tomita operator, its closure and spectral calculus have not been formalized for this pair. Automorphism covariance alone does not fix central phase ambiguity. No full formal identification with the Connes Radon-Nikodym derivative or Araki entropy is claimed.', "The operator called L is a log-likelihood generator. Its identification with the user's cauda/poco, with a geometric tail algebra, or with light stabilization is not established.", "The operator clarified that the candidate area is a quadratic angular reading, not L. The tested F=(u-I)* (u-I) uses an adjoint on the first factor. It is a concrete candidate selected for testing, not an asserted unique interpretation of the user's term.", 'A projective-state metric removes global phase and uses variance rather than the raw second moment. This projective identification is an analytic observation. The fourth-order bound for the tested nonprojective F is formally proved.', 'No identification of the tested phase observable with geometric screen area, no choice of length units, region-algebra map, general H3, or graviton dynamics is supplied.', 'The previously constructed geometric family in 029 still has input ansatz and residual curvature freedom. The cocycle theorem does not remove those geometric obligations.', 'Final counts include auxiliary lemmas and controls; they do not measure completion of quantum gravity.', 'Canonical originals, um.py, Atlas, memories, gates, seals and previous deliveries remain untouched. Independent managerial audit and incorporation remain pending.'], 'criteria': [['Derivacao anterior ao codigo', 'PAGO', 'CONTINUACAO030_DERIVACAO_PREVIA.md, com adendo anterior ao teste angular.'], ['Gerador global convergente', 'PAGO', 'likelihood_terms_summable, likelihood_generator_selfadjoint, likelihood_generator_mem_factor.'], ['Cociclo e cortes efetivos', 'PAGO', 'likelihood_cocycle_twisted, likelihood_prefix_is_finite_cocycle, likelihood_prefix_cocycle_limit.'], ['Estado anterior reproduzido', 'PAGO', 'likelihood_filter_vector, likelihood_filter_state, likelihood_exponential_normalized.'], ['Positividade e inversao do filtro', 'PAGO', 'likelihood_filter_positive, likelihood_filter_invertible.'], ['Covariancia no fator inteiro', 'PAGO', 'likelihood_global_covariance; extensao pelo duplo comutante, sem postular WOT.'], ['Leitura entropica', 'PAGO NO LIMITE DE PREFIXOS', 'likelihood_generator_entropy; identificacao Araki geral NAO PAGA.'], ['Controles', 'PAGO', 'zero_amplitude_cocycle e geometric_generator_nonzero, com perfil infinito da 028.'], ['Leitura angular quadratica', 'PAGO COMO OBJETO POSITIVO', 'phase_quadratic_positive, phase_quadratic_read, phase_quadratic_modular_limit.'], ['Ordem da leitura angular testada', 'PAGO', 'phase_quadratic_norm_bound e phase_quadratic_fourth_order_bound; coeficiente de ordem t² dessa F e zero por limite.'], ['Identificacao modular relativa completa', 'NAO PAGO', 'Operador relativo nao limitado e dominios ainda por construir.'], ['Area geometrica e reconstrucao geral', 'NAO PAGO', 'Fase quadratica positiva nao seleciona tela, escala ou dinamica. H3 geral continua aberta.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved read-only by verify_stage.ps1. This is not a portable full bundle or independent recompilation.'},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'LikelihoodCocycleControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


INTRO = ['[REAL / INPUT / OPEN] ENTREGA 030 ESPONTANEA — cociclo global, estado efetivo e leitura angular quadratica.', '', '06/09/2026. Continuacao da ordem 007, sob a pergunta do operador sobre cociclo e area. A prova ampla permanece aberta; auditoria da gerencia pendente.', '', 'Para a familia somavel da 028, foi construido L(t)=sum L_n(t), limitado e autoadjunto em norma, e u_t(s)=exp(i s L(t)). O parametro t varia o estado; s e tempo modular. Os u_t(s) sao limites em norma dos cociclos finitos dos pesos efetivos, satisfazem a lei torcida e pertencem ao fator.', '', 'O filtro R=exp(L/2) e positivo, invertivel e reproduz exatamente o vetor e o estado globais ja construidos: R Omega=Psi, psi(A)=omega(R A R), omega(exp L)=1. A identidade u sigma_omega(A) u*=sigma_psi(A) foi provada para TODO A do fator, estendendo a igualdade local pelo duplo comutante.', '', 'A leitura psi(L) coincide com o limite somavel das entropias relativas dos prefixos. Isso nao e uma formalizacao completa do operador modular relativo nao limitado nem uma identificacao geral de entropia de Araki.', '', 'O operador esclareceu durante a etapa: a candidata a area e a leitura quadratica da fase, nao L. Foi testado F=(u-I)^*(u-I), positivo, igual a 2I-u-u*, com leitura ||(u-I)xi||^2 e limite F/s^2 -> L^2 em norma quando s -> 0. Essa construcao e uma interpretacao matematica a testar, nao a identificacao ja demonstrada com area de tela.', '', '[REAL / DERIVED] Lean prova ||F_t(s)||<=s^2||L(t)||^2<=36s^2B^2t^4. Para s fixo, segue F_t(s)/t^2 -> 0. A resposta entropica anterior com B>0 tem coeficiente -log(2)B em ordem t^2. Conversao constante finita dessa F nao resolve o casamento nessa parametrizacao. Isso nao exclui o modulo raiz de F ou outra leitura angular; a operacao pretendida precisa ser especificada.', '', '[KNOWN / DERIVED] Ao retirar a fase global, a metrica projetiva usa a variancia de L, em lugar do segundo momento. A formula do tensor geometrico dos estados e apresentada em [Ran Cheng, secao II, eqs. 4-6](https://arxiv.org/html/1012.1337v1). A aplicacao a u=exp(i s L) e uma substituicao analitica; nao implica area gravitacional.', '', 'Um controle de sinal de L, isoladamente, nao refuta a candidata angular esclarecida pelo operador. O teste relevante e a compatibilidade entre leitura, parametros, escala dimensional e area efetiva.']


def delivery_text(data):
    rows = INTRO[:]
    rows += ['', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes impressas. Contagens incluem auxiliares.",
             'Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.',
             '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
             f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation030.py'}'", '\u0060\u0060\u0060',
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO030_DERIVACAO_PREVIA.md','CONTINUACAO030_PARECER.md','audit_continuation030.py'])
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
    rows += ['', 'Parecer: '+str(ROOT / 'CONTINUACAO030_PARECER.md'),
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_030_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_030_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 030 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation030.py [--write]')

