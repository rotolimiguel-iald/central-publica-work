"""Exact-byte and Lean-output audit for spontaneous continuation 026.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['RelativeProfilePreparation', 'ProfileOverlapFactorization', 'AffinityProducts', 'AffinityVectorCriterion', 'GlobalProfileState', 'GlobalProfileFaithfulness', 'ProfileAffinityBound', 'GlobalProfileControls']
MANIFEST = ROOT / 'CONTINUACAO026_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_026_ESPONTANEA_afinidade_e_estado_global.md'
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

    visit('GlobalProfileControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation026.py', 'revise_continuation026.py', 'verify_stage.ps1',
        'CONTINUACAO026_DERIVACAO_PREVIA.md', 'CONTINUACAO026_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO025_MANIFESTO.json', 'audit_continuation025.py', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean', 'fontes/tgl_kernel/TGLExt/SignatureInTheLimit.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO026_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation026.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation026.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{'status': 'REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending', 'kind': 'spontaneous continuation 026; no managerial order 026 issued at publication time', 'reuse': ['canonical product tower, right multiplication and separating reference vector', 'finite Gibbs preparation from 024 and finite affinity identities from 025', 'Hilbert completeness, continuity and series convergence in mathlib'], 'paid': ['relative positive diagonal preparations for arbitrary strictly positive product profiles P and Q in the original H(P)', 'unit norm and exact Q marginals on every fixed local level', 'all-pair overlap C_N/C_L and squared distance 2(1-C_N/C_L), including inverse-filter overlap', 'positive antitone prefix affinities, infinite limit and sufficient summability criterion', 'canonical preparation is Cauchy, equivalently has a norm limit, if and only if the infinite affinity limit is positive', 'explicit unit vector in H(P), with normalized complex-linear positive state and all Q marginals', 'sequential WOT continuity of the constructed vector state', 'inverse finite filters recover Omega in norm; right action equals left action on the limit vector', 'constructed global vector is cyclic and separating, and its state is faithful on the original factor', 'quadratic binary affinity bound and square-summable sufficient condition', 'infinite-site harmonic perturbation with nonsummable first differences, square-summable differences, positive affinity limit and a faithful state different from the original reference', 'unchanged-profile control, stationary changed-profile zero limit and no canonical preparation limit', 'exact identification of the relative-profile preparation with the Gibbs preparation when Q=thermalProfile P s'], 'inputs_and_unpaid': ['P e Q sao perfis produto estritamente positivos, fornecidos como INPUT. Nao se construiu estado correlacionado nem foi selecionado um perfil por dinamica fisica.', 'A equivalencia de convergencia refere-se a sequencia canonica F_N Omega. O resultado nao classifica todos os estados normais, nao prova disjuncao ou quase-equivalencia de todas as representacoes.', "A continuidade formalizada e SeqWOTContinuous. O termo 'estado vetorial' descreve a construcao explicita; nao se declara uma formalizacao geral do predual ou de normalidade por todas as redes.", 'Fidelidade foi provada via recuperacao de Omega e comutante. Nao foi inferida da fidelidade de estados finitos sob passagem ao limite.', 'A somabilidade das perdas e criterio suficiente demonstrado; sua necessidade como serie nao e aqui afirmada, embora haja equivalencia exata com positividade do produto para a convergencia da preparacao.', 'A perturbacao harmonica e um exemplo matematico escolhido. Nao foram construidos aqui a unitaria H(Q) para H(P), o transporte de S/J/Delta, uma curva temporal duas vezes diferenciavel ou uma resposta gravitacional global finita.', 'H3, lei de area, dimensao, assinatura, solda, temperatura, unidades e a selecao fisica da fonte continuam antecedentes ou lacunas. Os resultados geometricos condicionais anteriores nao ganham nova hipotese paga por esta etapa.', 'O objetivo amplo de gravidade quantica e a reconstrucao global permanecem abertos. Nenhum gate, selo canonico ou conclusao observacional foi alterado.'], 'criteria': [['Derivacao antes do codigo', 'PAGO', 'CONTINUACAO026_DERIVACAO_PREVIA.md, com auditoria 025 novamente PASS.'], ['Preparacao relativa finita e marginais', 'PAGO', 'relative_filter_positive, profile_vector_norm e profile_state_marginal.'], ['Produto e sobreposicao entre quaisquer andares', 'PAGO', 'profile_affinity_product, profile_vectors_overlap e profile_vectors_distance.'], ['Criterio exato de limite no H original', 'PAGO NO ENUNCIADO', 'profile_vectors_cauchy_iff e profile_vectors_limit_iff; sequencia canonica especificada.'], ['Somabilidade suficiente', 'PAGO', 'affinity_loss_summable_positive_limit; sem importar o teorema geral de Kakutani.'], ['Estado global no H original', 'PAGO', 'globalProfileVector, global_profile_state_local, _one, _positive e _seqWOT.'], ['Fidelidade e ciclicidade no fator original', 'PAGO', 'global_profile_inverse_tendsto, global_profile_right_left, global_profile_vector_separating, global_profile_state_faithful e global_profile_vector_cyclic.'], ['Controle quadratico', 'PAGO', 'binary_affinity_quadratic_bound e profile_square_summable_positive.'], ['Mudanca em infinitos sitios', 'PAGO', 'gradualProfile, gradual_profile_changes_every_site, _square_summable, _diff_not_summable e _affinity_positive.'], ['Estado distinto e fiel', 'PAGO', 'gradual_state_not_reference, gradual_state_local e gradual_state_faithful.'], ['Controles e ligacao com Gibbs', 'PAGO', 'profile_affinity_limit_self, stationary_changed_no_preparation_limit e thermal_preparation_limit_iff.'], ['Classificacao de todos os estados normais e QG', 'NAO PAGO', 'O criterio nao e promovido a teorema geral de disjuncao; H3 e demais folhas continuam abertas.']], 'dependency_limit': 'Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation.'},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'GlobalProfileControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = ['[REAL / INPUT / OPEN] ENTREGA 026 ESPONTANEA — criterio de afinidade, estado global e fidelidade no Hilbert original.', '', '06/09/2026. A entrega 025 foi reconferida e classificada como PROGRESSO. Continuacao do objetivo amplo associado a ordem 007; nao e nova ordem gerencial.', '', 'Dados dois perfis produto positivos P,Q, F_N=diag sqrt(q_N/p_N) e Psi_N=pi_P(F_N)Omega vivem no mesmo H(P). Seus estados reproduzem exatamente as marginais Q de todo andar L menor ou igual a N.', '', 'Defina c_n=sum sqrt(p_n)sqrt(q_n), C_N=prod_{n<=N}c_n e C=lim C_N. Foram provados 0<c_n<=1, C_N positivo antitono, <Psi_L,Psi_N>=C_N/C_L e ||Psi_L-Psi_N||^2=2(1-C_N/C_L). A sequencia Psi_N e Cauchy, equivalentemente possui limite em norma, SE E SOMENTE SE C>0.', '', 'Se C>0, o vetor limite Phi tem norma um, e o estado <Phi,A Phi> e complexo-linear, positivo, normalizado, SeqWOTContinuous e reproduz todas as marginais Q no fator ORIGINAL de P. Para provar fidelidade, os filtros inversos locais aplicados a Phi convergem a Omega e coincidem com as acoes direitas correspondentes. O comutante e a separancia de Omega dao A Phi=0 => A=0. A mesma recuperacao de Omega e a densidade da torre provam que Phi tambem e ciclico.', '', 'A somabilidade de (1-c_n) e suficiente para C>0. Um limite quadratico de Hellinger da um exemplo inteiramente demonstrado: P_n=1/3 e Q_n=1/3+1/(12(n+1)). Todos os sitios mudam; as diferencas nao sao somaveis, mas seus quadrados sao. O estado global construido e fiel e diferente da referencia.', '', 'O controle estacionario P_n=1/3, Q_n=1/2 tem C=0 e nao admite limite em norma desta preparacao. Q=P tem C=1. A igualdade com a preparacao de Gibbs de 024 e tipada quando Q=thermalProfile(P,s).', '', '[KNOWN] Afinidades e estados produtos infinitos fazem parte da teoria classica de [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf). Esta entrega formaliza uma preparacao concreta na torre da casa. Nao importa o teorema geral como axioma nem reivindica sua descoberta.', '', 'O criterio exato concerne a sequencia especificada. Nao se provou aqui classificacao de todos os estados normais, disjuncao ou quase-equivalencia de representacoes; a continuidade formalizada e sequencial WOT. A existencia e fidelidade obtidas nao implicam H3, lei de area ou reconstrucao gravitacional geral.', '', '## Criterios', '', '| Criterio | Estado | Evidencia |', '|---|---|---|']
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.",
        'Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiom aticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.',
        '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation026.py'}'",
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO026_DERIVACAO_PREVIA.md','CONTINUACAO026_PARECER.md','audit_continuation026.py'])
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
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO026_PARECER.md')+'.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_026_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_026_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 026 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation026.py [--write]')




