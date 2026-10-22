"""Exact-byte and Lean-output audit for spontaneous continuation 024.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['CanonicalModularStationarity', 'GibbsTilt', 'GibbsVarianceResponse', 'QuadraticGibbsCurve', 'TowerGibbsPerturbation', 'GibbsMatterBridge', 'GibbsGravityControls']
MANIFEST = ROOT / 'CONTINUACAO024_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_024_ESPONTANEA_perturbacao_termica_da_torre.md'
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

    visit('GibbsGravityControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation024.py', 'revise_continuation024.py', 'verify_stage.ps1',
        'CONTINUACAO024_DERIVACAO_PREVIA.md', 'CONTINUACAO024_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO024_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation024.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation024.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'spontaneous continuation 024; no managerial order 024 issued at publication time', 'reuse': ['canonical modularFlow_fixes_omega and modularConjugation_preserves_state from ModularPower, already proved before 024', 'canonical tower Hilbert representation, faithful separating reference vector and factor', 'actual geometric screens and temporal heat of 019-020', 'relative entropy calculus of 021', 'covector stress conservation and geometric reconstruction of 023'], 'paid': ['stationarity of canonical modular local marginals and entropy', 'positive normalized finite Gibbs tilt driven by local modular generator, all real parameters', 'entropy and generator first derivatives equal minus modular variance', 'variance nonnegative, zero exactly for equal strictly positive weights', 'Fisher coefficient of the Gibbs curve equals modular variance', 'quadratic reparameterization gives entropy and modular response minus frequency squared times variance, relative entropy coefficient zero', 'actual normalized faithful positive complex-linear vector states on the original tower factor, for arbitrary finite level N', 'local weights and generator expectation read directly from these same-Hilbert-space states', 'inclusion coherence for representations of each observable and SeqWOT continuity', 'nontrivial quadratic Gibbs perturbation cannot be the canonical stationary modular orbit', 'chosen stress coefficient variance over pi produces the actual heat-modular matching', 'area matching equivalent to null Ricci balance and conditional Einstein reconstruction', 'tracial and nontracial controls, flat conserved stress with heat matching and failed area matching'], 'inputs_and_unpaid': ['Escolha da perturbacao de Gibbs, do andar finito e do campo de covetores. A referencia p e constante em x no teorema gravitacional; nao se prova o caso p(x).', 'O parametro quadratico s=(w(d)t)^2 e escolhido; nao e uma dinamica derivada.', 'O acoplamento variancia/pi e a normalizacao escolhida para o calor; nao e uma constante gravitacional medida. O tensor e do tipo escalar, nao materia quantica geral.', 'A equacao de onda e o fechamento do covetor permanecem antecedentes da conservacao.', 'A correspondencia entropia-area permanece uma hipotese independente, equivalente ao balanco nulo de Ricci.', 'Quatro dimensoes, assinatura lorentziana e solda suave inversivel sao dados de entrada.', 'A continuidade SeqWOT e provada; nao se afirma um novo teorema de normalidade predual completa.', 'Coerencia das inclusoes de observaveis nao estabelece independencia do andar, limite termico tipo III ou coerencia entre regioes do espaco-tempo.', 'Nao foram construidos entropia tipo III completa, temperatura fisica selecionada, unidades, coeficiente de Newton, reconstrucao global ou solucao da gravidade quantica.'], 'criteria': [['Derivacao anterior ao codigo', 'PAGO', 'CONTINUACAO024_DERIVACAO_PREVIA.md registra formulas, antecedentes e controles.'], ['Fluxo modular canonico', 'PAGO COMO REUTILIZACAO', 'ModularPower ja fixava omega. canonical_modular_entropy_constant e demais lemas apenas explicitam as restricoes locais.'], ['Gibbs fiel e normalizado', 'PAGO', 'gibbs_weights_positive, gibbs_weights_normalized, gibbs_weights_derivative e gibbs_log_weights, para todo parametro real.'], ['Resposta e degenerescencia', 'PAGO', 'gibbs_entropy_derivative_zero, gibbs_modular_increment_derivative_zero; modular_variance_zero_iff_tracial.'], ['Parametros e limites', 'PAGO SOB ESCOLHA', 'quadratic_reparameterization_limit usa derivada bilateral; nao compoe indevidamente o limite esquerdo em s com t ao quadrado.'], ['Mesmo H da torre, N arbitrario', 'PAGO', 'tower_gibbs_local_state, tower_gibbs_vector_norm, tower_gibbs_state_faithful, tower_gibbs_state_square_nonnegative e linearidade.'], ['Topologia e inclusoes', 'PAGO NO SENTIDO DECLARADO', 'tower_gibbs_state_seqWOT e tower_gibbs_inclusion_coherent; sem teorema novo de normalidade predual ou limite dos andares.'], ['Resposta lida do estado real', 'PAGO', 'tower_gibbs_entropy_quadratic e tower_gibbs_modular_quadratic usam o funcional construido e observaveis locais.'], ['Distincao da orbita modular', 'PAGO', 'tower_gibbs_not_modular_orbit, sob variancia positiva e frequencia nao nula.'], ['Calor e fonte', 'PAGO SOB NORMALIZACAO', 'gibbs_heat_matching para T=(V/pi)[w tensor w-g q/2].'], ['Area e equacao gravitacional', 'CONDICIONAL', 'gibbs_area_matching_iff_ricci e einstein_from_gibbs_area_matching; a origem da relacao de area permanece aberta.'], ['Controles', 'PAGO', 'gibbs_weights_tracial, binary_gibbs_variance_positive, tower_first_site_variance_positive; controle plano conservado paga calor e recusa area.'], ['Objetivo amplo', 'NAO PAGO', 'Selecao fisica, area, globalizacao, dimensao/assinatura e limite da torre permanecem INPUT/OPEN. Gate intocado.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation.'},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'GibbsGravityControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 024 ESPONTANEA - perturbacao de Gibbs realizada no mesmo espaco de Hilbert da torre; reconstrucao gravitacional condicional.',
        '', '06/09/2026. Continuacao da entrega 023, no objetivo amplo associado a ordem 007. A ordem 006 tem aprovacao registrada na ordem 007. Esta entrega nao e uma nova ordem gerencial.',
        '', 'Para p=towerW(P,N)>0, K_i=-log(p_i), construimos r_i(s)=p_i exp(-s K_i)/Z(s). O filtro positivo invertivel a_s=diag(sqrt(r_i(s)/p_i)) produz Psi_s=pi(a_s)Omega e omega_s(A)=<Psi_s,A Psi_s> no H original. N e arbitrario mas finito. O funcional e linear complexo, normalizado, positivo e fiel no fator. Em s=0 retorna a omega. Seus pesos locais sao exatamente r_i(s).',
        '', 'A variancia V_p(K) e nao negativa e se anula exatamente para pesos iguais. A derivada inicial da entropia e da expectativa do gerador vale -V. O Fisher da curva vale V e D(r_s||p)/s^2 tende a V/2 pelo lado esquerdo.',
        '', 'Escolhendo s=(w_x(d)t)^2, obtemos DeltaS/t^2 e DeltaK/t^2 tendendo a -w_x(d)^2 V, enquanto D/t^2 tende a zero. A composicao quadratica e provada a partir da derivada bilateral; nao se usa indevidamente um limite esquerdo em s para uma curva que chega por s>=0.',
        '', 'O fluxo modular canonico preserva omega; esse fato ja era provado em ModularPower. A curva perturbada nao e a sua orbita quando V>0 e w_x(d) nao e zero. A novidade verificada aqui e a realizacao da perturbacao e sua ligacao ao calculo local; nao e a descoberta da estacionariedade modular ou da familia de Gibbs.',
        '', 'K_N=-log(rho_N) e um observavel do andar finito. Nao se afirma que pi(K_N) seja o operador modular global -log(Delta). As entropias e variancias calculadas sao locais finitas, sem limite de Araki provado.',
        '', 'Normalidade/topologia: provamos SeqWOTContinuous, exatamente a continuidade sequencial WOT definida na casa. A coerencia de inclusoes diz que duas representacoes do mesmo observavel dao o mesmo valor. Nao significa independencia do andar escolhido para perturbar, nem limite termico tipo III.',
        '', 'Com kappa=V/pi e T=kappa[w tensor w-g gInv(w,w)/2], a correspondencia calor-modular e demonstrada para o calor temporal efetivo de 020. Conservacao usa fechamento e equacao de onda de 023. A correspondencia de area equivale a eta Ric(d,d)=2 pi T(d,d). Sob essas hipoteses, o teorema produz G+Lambda g=(2 pi/eta)T em dominio aberto preconexo.',
        '', 'Controle adversarial matematico: no espaco plano, covetor temporal constante e V>0 produzem tensor conservado e correspondencia de calor, mas a correspondencia de area falha para toda eta. Assim, a nova realizacao de estados e a conservacao nao bastam para provar a hipotese de area.',
        '', 'Contexto primario: [Jacobson, Entanglement Equilibrium and the Einstein Equation](https://arxiv.org/abs/1505.04753) trata variacoes do estado e da geometria sob equilibrio, com alcance de primeira ordem para campos conformes e uma conjectura adicional no caso nao conforme. Esse artigo orienta a distincao conceitual; nao e introduzido como axioma Lean.',
        '', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|',
    ]
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += [
        '', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes com axiomas impressos separadamente. Contagens incluem lemas auxiliares e controles.",
        'Fontes finais: compilacoes exit 0, fonte estavel, zero erros/avisos/sorryAx; apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.',
        '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation024.py'}'",
        '\u0060\u0060\u0060', '', 'O comando so le e verifica os bytes e as evidencias registradas. Recompilacao independente deve ocorrer em copia. Ordem dos novos modulos:',
    ]
    rows.extend('- '+str(ROOT / (module+'.lean')) for module in MODULES)
    rows += ['', 'Dependencias locais e sua ordem estao fixadas no manifesto. Lean/mathlib externos sao resolvidos pelo wrapper; nao e um pacote integral portatil.', '', '## Axiomas', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration']+': ['+', '.join(item['axioms'])+']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
        f"Manifesto: \u0060{MANIFEST}\u0060 - SHA256 \u0060{digest(MANIFEST)}\u0060.",
        f"Inventario: {len(data['files'])} caminhos absolutos, com tamanho e SHA256 dos bytes.",
        '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m+'.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO024_DERIVACAO_PREVIA.md', 'CONTINUACAO024_PARECER.md', 'audit_continuation024.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    rejected = 0
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rejected += 1
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit {run['exit_code']}; copia exata do log rejeitado.")
    rows += ['', f'{rejected} tentativas rejeitadas preservadas. Todas as versoes compiladas sao recuperaveis pelos fontes finais e backups de bytes. Somente os fontes finais limpos sustentam a entrega.',
        '', '## Dividas', '']
    rows.extend('- '+item for item in data['inputs_and_unpaid'])
    rows += ['', 'Originais, um.py, kernel canonico, Atlas, memorias, diarios, gate e entregas anteriores intocados. Nenhuma confirmacao fisica e declarada. O objetivo amplo permanece ativo e nao alcancado; a gerencia deve auditar antes de incorporar.',
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO024_PARECER.md')+'.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_024_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_024_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 024 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation024.py [--write]')




