"""Exact-byte and Lean-output audit for spontaneous continuation 025.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['GibbsProductLaw', 'GibbsProductVariance', 'TowerThermalProfile', 'GibbsAffinity', 'TowerThermalOverlap', 'ThermalCutoffResponse', 'ThermalLimitControls']
MANIFEST = ROOT / 'CONTINUACAO025_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_025_ESPONTANEA_limite_termico_e_corte.md'
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

    visit('ThermalLimitControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation025.py', 'revise_continuation025.py', 'verify_stage.ps1',
        'CONTINUACAO025_DERIVACAO_PREVIA.md', 'CONTINUACAO025_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO025_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation025.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation025.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'spontaneous continuation 025; no managerial order 025 issued at publication time', 'reuse': ['normalized faithful Gibbs vector preparation from 024', 'canonical tower for each SiteProfile and faithful reference state', 'finite entropy additivity and stationary tower entropy from TowerEntropyScaling', 'covector stress conservation from 023 and actual heat, screen area and conditional reconstruction from 020-024'], 'paid': ['Gibbs weights, partition and local generator expectation factorize under products', 'modular variance is additive; tower variance is the sum of site variances', 'thermalProfile P s is a strictly positive SiteProfile whose tower weights equal every tilted prefix', 'equality of all finite local states with the canonical representation of thermalProfile P s', 'compatibility of the actual same-Hilbert-space vector-state marginals as the preparation level grows', 'finite affinity identity, product formula, and strict affinity below one for nontrivial nontracial Gibbs tilt', 'exact overlap with Omega and exact successive-vector squared distance in the original H(P)', 'stationary nontracial preparations at fixed nonzero parameter are not Cauchy and have no norm limit', 'chosen coupling V_N/pi grows without bound in the stationary nontracial case', 'explicit frequency rescaling by square root of site count makes the second-order response independent of level', 'for fixed temporal parameter, every fixed local observable returns to the original reference state as level grows under the chosen rescaling', 'heat matching for the rescaled family with site coupling; area matching still equivalent to null Ricci balance', 'tracial fixed-vector and nontracial non-Cauchy controls; flat conserved source matches heat and fails area at every cutoff'], 'inputs_and_unpaid': ['O estado de referencia e produto. A formula linear de variancia e o negativo uniforme usam perfil constante nao tracial; nao se estendem automaticamente a perfis gerais ou estados correlacionados.', 'A representacao global construida e H(P_s). Nao foi provada identificacao com H(P), nem o teorema geral de normalidade, quase-equivalencia ou disjuncao de produtos infinitos.', 'O negativo em H(P) refere-se a sequencia especifica de vetores preparados em 024. Afinidade com Omega tendendo a zero nao prova, isoladamente, convergencia fraca a zero ou inexistencia de outro vetor com dadas marginais.', 'A escala por sqrt(N+1) e escolha explicita. O limite temporal de segunda ordem e tomado para cada N; nao se prova troca de limites ou uniformidade em N.', 'A resposta reescalada e extensiva. Todo observavel em andar fixo retorna a referencia para parametro temporal fixo; nao se declara nova dinamica local sobrevivente.', 'A correspondencia entropia-area, covetor/onda, quatro dimensoes, assinatura, solda, unidades, temperatura e coeficiente de Newton continuam antecedentes ou lacunas.', 'O objetivo amplo de gravidade quantica e a reconstrucao global permanecem abertos. Nenhum gate ou conclusao fisica foi alterado.'], 'criteria': [['Derivacao anterior ao codigo', 'PAGO', 'CONTINUACAO025_DERIVACAO_PREVIA.md registra as distincoes e os limites pretendidos.'], ['Fatoracao de Gibbs', 'PAGO', 'gibbs_partition_product, gibbs_weights_product e gibbs_mean_product.'], ['Variancia e corte', 'PAGO', 'modular_variance_product, tower_variance_sum, tower_variance_uniform, tower_coupling_unbounded.'], ['Perfil global construido', 'PAGO NO TIPO DECLARADO', 'thermalProfile e thermal_profile_tower_weights; representacao H(P_s), nao identificacao com H(P).'], ['Compatibilidade dos andares', 'PAGO', 'thermal_global_local_state, thermal_tower_marginal e thermal_tower_marginal_weights.'], ['Afinidade exata', 'PAGO', 'hellinger_sum_identity, diagonal_affinity_eq_one_iff, gibbs_fixed_iff_tracial e gibbs_affinity_product.'], ['Limite em H original', 'NEGATIVO PAGO', 'thermal_vectors_no_norm_limit e thermal_vectors_not_cauchy, para perfil constante nao tracial e s diferente de zero.'], ['Resposta com escala escolhida', 'PAGO CONDICIONAL', 'cutoff_response_equals_site e cutoff_modular_limit/cutoff_entropy_limit/cutoff_relative_entropy_limit.'], ['Estado local no limite do corte', 'PAGO', 'cutoff_local_state_returns_reference, para todo observavel local fixo; nao se afirma troca dos limites.'], ['Calor e area', 'CALOR PAGO; AREA CONDICIONAL', 'cutoff_heat_matching e cutoff_area_matching_iff_ricci para o acoplamento por sitio.'], ['Controles', 'PAGO', 'half_thermal_vectors_fixed, half_thermal_variance_zero; third_thermal_vectors_not_cauchy; cutoff_flat_area_not_matching.'], ['Normalidade/disjuncao e objetivo amplo', 'NAO PAGO', 'O alcance novo e medido sem promover nao-Cauchy a teorema geral de disjuncao; H3 e demais antecedentes continuam abertos.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation.'},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'ThermalLimitControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = [
        '[REAL / INPUT / OPEN] ENTREGA 025 ESPONTANEA - perfil termico global, obstrucao ao limite em norma da preparacao e escala da resposta.',
        '', '06/09/2026. A etapa 024 foi reconferida e classificada como PROGRESSO. Continuacao do objetivo amplo associado a ordem 007; nao e uma nova ordem gerencial.',
        '', 'Gibbs respeita o produto: r_(p tensor q)(s)=r_p(s) tensor r_q(s). A variancia do gerador local soma. O perfil P_s com pesos de sitio inclinados e construido como SiteProfile e satisfaz towerW(P_s,N)=r_(towerW(P,N))(s) para todo N.',
        '', 'O estado canonico do perfil P_s realiza todas as marginais na sua propria representacao H(P_s). Os estados vetoriais de 024, todos em H(P), tambem sao exatamente compativeis nos observaveis de cada andar fixo quando o corte da preparacao cresce. Estas duas afirmacoes nao identificam as representacoes completas.',
        '', 'A afinidade c(p,r)=sum sqrt(p_i)sqrt(r_i) pertence a (0,1] para pesos positivos normalizados, e vale um exatamente quando p=r. Para Gibbs nao tracial e s diferente de zero, c<1. Em perfil constante, <Omega,Psi_N>=c^(N+1) e ||Psi_N-Psi_(N+1)||^2=2(1-c). Logo a sequencia de vetores da preparacao NAO e Cauchy e nao tem limite em norma em H(P).',
        '', 'Este negativo e sobre a sequencia especifica. Nao equivale, sozinho, a um teorema de disjuncao, inexistencia de outro vetor, ou nao normalidade de toda realizacao com essas marginais. Referencia primaria de contexto: [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf), que trata produtos infinitos e estados normais com hipoteses e metricas proprias. O teorema geral desse artigo nao foi importado como axioma nem formalizado aqui.',
        '', 'Para perfil constante nao tracial, V_N=(N+1)V_site e kappa_N=V_N/pi cresce sem limite. Escolhendo frequencia_N=frequencia/sqrt(N+1), o coeficiente de DeltaS/t^2 e DeltaK/t^2 passa a -frequencia^2 V_site para todo N; D/t^2 tende a zero. Esta normalizacao e INPUT.',
        '', 'Para t fixo, s_N=(frequencia*t)^2/(N+1) tende a zero. Em TODO andar observado fixo, o estado reescalado retorna ao estado original. A resposta extensiva nao e apresentada como uma variacao local nao trivial sobrevivente. Os limites temporais sao provados para cada N; nao foi provada permutacao dos limites.',
        '', 'O tensor usa kappa_site=V_site/pi. A correspondencia do calor temporal efetivo e provada com a familia reescalada, mas area continua equivalente a eta Ric(d,d)=2 pi T(d,d). No espaco plano, o tensor e conservado, o calor corresponde e a area falha para todo N e toda eta quando V_site>0. A nova escala nao produz H3.',
        '', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|',
    ]
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.",
        'Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiom aticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.',
        '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation025.py'}'",
        '\u0060\u0060\u0060', '', 'O comando so le os artefatos e verifica a custodia. Recompilacao independente deve ocorrer em copia. Ordem dos novos modulos:']
    rows.extend('- '+str(ROOT / (module+'.lean')) for module in MODULES)
    rows += ['', 'Dependencias locais e sua ordem estao fixadas no manifesto; Lean/mathlib externos sao resolvidos pelo wrapper. Nao e um pacote integral portatil.',
        '', '## Axiomas', '', '\u0060\u0060\u0060text']
    for module in data['modules']:
        for item in module['axioms']:
            rows.append(item['declaration']+': ['+', '.join(item['axioms'])+']')
    rows += ['\u0060\u0060\u0060', '', '## Artefatos e hashes', '',
        f"Manifesto: \u0060{MANIFEST}\u0060 - SHA256 \u0060{digest(MANIFEST)}\u0060.",
        f"Inventario: {len(data['files'])} caminhos absolutos, com tamanho e SHA256 dos bytes.",
        '', '| Artefato principal | SHA256 |', '|---|---|']
    primary = {str(ROOT / (m+'.lean')) for m in MODULES}
    primary.update(m['final_log'] for m in data['modules'])
    primary.update(str(ROOT / n) for n in ['CONTINUACAO025_DERIVACAO_PREVIA.md','CONTINUACAO025_PARECER.md','audit_continuation025.py'])
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
    rows += ['', f'{rejected} tentativas rejeitadas preservadas. Fontes compilados recuperaveis pelos arquivos finais e backups dos bytes. Somente as compilacoes finais limpas sustentam esta entrega.',
        '', '## Dividas', '']
    rows.extend('- '+item for item in data['inputs_and_unpaid'])
    rows += ['', 'Originais, um.py, kernel canonico, Atlas, memorias, diarios, gate e entregas anteriores intocados. Nenhuma confirmacao fisica e declarada. O objetivo amplo permanece ativo e nao alcancado. Gerencia audita antes de incorporar.',
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO025_PARECER.md')+'.',
        '', 'Ordens encontradas:']
    rows.extend('- '+p for p in data['incoming_orders'])
    return ('\n'.join(rows)+'\n').replace('axiom aticas','axiomaticas')


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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_025_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_025_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 025 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation025.py [--write]')




