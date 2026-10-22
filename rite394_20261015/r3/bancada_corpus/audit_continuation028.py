"""Exact-byte and Lean-output audit for spontaneous continuation 028.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ["RelativeEntropyProductBounds","ProfileEntropyLimits","HarmonicEnergyObstruction","SummableProfileCurve","SummableStateThermodynamics","UniformQuadraticResponse","SummableGravityBridge","SummableGravityControls"]
MANIFEST = ROOT / 'CONTINUACAO028_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_028_ESPONTANEA_resposta_global_e_limite_do_corte.md'
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
    if namespace != 'ChatgptAudit.Response028':
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

    visit('SummableGravityControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation028.py', 'revise_continuation028.py', 'verify_stage.ps1',
        'CONTINUACAO028_DERIVACAO_PREVIA.md', 'CONTINUACAO028_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO027_MANIFESTO.json', 'audit_continuation027.py', 'CONTINUACAO026_MANIFESTO.json', 'audit_continuation026.py', 'CONTINUACAO025_MANIFESTO.json', 'audit_continuation025.py', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean', 'fontes/tgl_kernel/TGLExt/SignatureInTheLimit.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO028_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation028.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation028.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{"status":"REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending","kind":"spontaneous continuation 028; no managerial order 028 issued at publication time","reuse":["actual product tower and finite diagonal states","global profile vectors, affinity criterion and faithfulness from 026, unitary equivalence and modular transport from 027","geometric screen, heat, covector stress and conditional Einstein reconstruction from previous bench modules","real logarithm inequalities, summable series and filters from mathlib"],"paid":["nonnegative finite diagonal relative entropy with a chi-square upper bound and exact product additivity","all prefix relative entropies and modular increments equal their site sums; entropy difference equals modular increment minus relative entropy","harmonic profile has positive affinity and finite relative entropy limit but prefix modular and entropy increments diverge to positive infinity","counterexample to finite prefix thermodynamic increments inferred solely from affinity positivity and representation equivalence","summable nonnegative amplitudes produce positive product profiles for every real parameter and faithful vector states in the original Hilbert space","prefix weights and modular expectations are explicitly read from the constructed global states","modular, relative and entropy increments have finite limits as the prefix cutoff tends to infinity","relative entropy remainder is bounded uniformly in the cutoff by a fourth-order temporal term","global temporal quadratic response and joint cutoff/time response along every admissible filter trajectory have the same finite coefficient","infinite summable source coefficient is nonnegative and independent of a prefix cutoff","constructed heat matches the modular response; the area defect coefficient is computed, and zero area defect is equivalent to the null Ricci balance","conditional Einstein equation on a preconnected coordinate domain follows under the explicitly retained area matching, smooth frame and conservation hypotheses","geometric amplitudes change infinitely many sites, have mass 1/12 and square mass 1/432, and coupling log(2)/(12*pi)","zero-amplitude profile returns the original state and zero entropy response","flat conserved nonzero source matches heat but fails area for the actual global family"],"inputs_and_unpaid":["A referencia escolhida e o perfil produto binario constante (1/3,2/3). As amplitudes b_n sao INPUT: nao negativas, no maximo 1/12 e somaveis. A escolha fisica desse perfil ou dessas amplitudes nao foi derivada.","Q_t.w(n)=1/3-b_n*t^2/(1+t^2) e uma curva escolhida matematicamente. Os estados fieis e suas marginais foram construidos; nao se postulou a lei de area na definicao da curva.","A entropia relativa global desta entrega e o limite das entropias relativas diagonais nos prefixos especificados. Sua identificacao com a entropia relativa de Araki completa nao foi formalizada.","S(t) e o limite das DIFERENCAS de entropias finitas, nao a subtracao de duas entropias infinitas tratadas como reais. K_N=-log(rho_N) e um observavel local; nao foi identificado a -log(Delta) global.","A regularidade demonstrada para a resposta e o limite quadratico, inclusive conjunto em corte e tempo. Nao se afirma derivada segunda em norma do vetor global ou continuidade em norma de toda a familia U(t).","A fidelidade e o transporte modular de cada estado reutilizam 026-027. A continuidade de estado formalizada anteriormente e sequencial WOT; nao se declara aqui um predual geral.","A fonte e do tipo covetor escalar, com acoplamento escolhido para o casamento do calor. Nao classifica toda materia quantica nem deriva a equacao de onda ou o perfil de uma dinamica fisica.","A area geometrica e calculada independentemente; sua correspondencia com S(t) continua HIPOTESE, equivalentemente o balanco nulo de Ricci. O controle plano mostra que a finitude global e o casamento do calor nao a implicam.","Regiao-algebra, correlacoes fisicas, dimensao, assinatura, solda, temperatura, unidades e origem microscopica da lei de area permanecem antecedentes ou lacunas. H3 e a reconstrucao gravitacional geral continuam abertas.","O objetivo amplo de gravidade quantica nao foi alcancado. Nenhum original, gate, selo canonico, memoria ou conclusao observacional foi alterado."],"criteria":[["Derivacao anterior ao codigo","PAGO","CONTINUACAO028_DERIVACAO_PREVIA.md; auditoria 027 reconferida."],["Cotas e produtos de entropia relativa","PAGO","diagonal_relative_nonnegative, diagonal_relative_upper, relative_entropy_product e third_binary_relative_bound."],["Valores efetivos de prefixo","PAGO","prefix_relative_sum, prefix_modular_sum e prefix_entropy_identity."],["Contraexemplo harmonico","PAGO","harmonic_relative_limit, harmonic_modular_diverges, harmonic_entropy_diverges e finite_relative_not_finite_entropy."],["Familia global fiel","PAGO","amplitudeProfile, amplitude_profile_affinity_positive, amplitudeState, amplitude_state_faithful e amplitude_unitary_omega."],["Leitura dos estados","PAGO","amplitude_read_weights, amplitude_read_modular_increment e amplitude_read_entropy_tendsto."],["Resposta finita sem corte","PAGO","amplitude_modular_tendsto, amplitude_relative_tendsto e amplitude_entropy_tendsto."],["Cota uniforme e limite conjunto","PAGO","amplitude_prefix_relative_scaled_bound, amplitude_prefix_modular_joint e amplitude_prefix_entropy_joint."],["Calor e coeficiente de area","PAGO NO ENUNCIADO","amplitude_heat_matching e amplitude_area_matching_iff_ricci."],["Implicacao Einstein","PAGO CONDICIONAL","einstein_from_summable_area_matching conserva harea, solda suave invertivel, covetor fechado e equacao de onda."],["Controles exatos","PAGO","geometric_amplitude_mass, geometric_amplitude_square_mass, geometric_state_not_reference, zero_amplitude_state e geometric_flat_area_not_matching."],["Lei de area microscopica e QG geral","NAO PAGO","A lei de area nao foi derivada da torre; o controle plano impede inferi-la apenas dos resultados obtidos."]],"dependency_limit":"Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation."},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'SummableGravityControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = ["[REAL / INPUT / OPEN] ENTREGA 028 ESPONTANEA — resposta global finita, limite conjunto e obstrucao termodinamica.","","06/09/2026. Continuacao do objetivo associado a ordem 007. A entrega 027 foi reconferida e classificada como PROGRESSO. O objetivo amplo permanece aberto.","","O perfil harmonico da 026 fornece um contraexemplo exato: afinidade infinita positiva, estado fiel e equivalencia unitaria no Hilbert original coexistem com incrementos modular e de entropia que divergem a +infinito quando o corte cresce. Sua entropia relativa de prefixo, em contraste, converge a um real finito. Existencia e equivalencia da representacao nao bastam para uma resposta termodinamica finita.","","A construcao positiva usa P_n=1/3, amplitudes 0<=b_n<=1/12 com soma B finita e Q_t(n)=1/3-b_n*h(t), h(t)=t^2/(1+t^2). Para todo t ha um estado fiel no H(P) original, com essas marginais, e a unitaria da 027. Pesos, entropias de prefixo e expectativas do gerador local sao explicitamente lidos dos estados.","","Foram provados os limites de corte K(t)=-log(2)*B*h(t), D(t)=lim D_N(t) e S(t)=lim[S(Q_t,N)-S(P,N)]=K(t)-D(t), com 0<=D(t)<=9/2*h(t)^2*sum b_n^2. S e limite das diferencas, sem subtrair infinitos.","","Ao reparametrizar por frequency*t, K/t^2 e S/t^2 tendem a -frequency^2*log(2)*B; D/t^2 tende a zero. A mesma resposta vale no LIMITE CONJUNTO, para qualquer corte que tenda a infinito e tempo que tenda a zero fora de zero, sem relacao imposta entre as velocidades. A cota do resto e uniforme em todo corte.","","O coeficiente kappa=log(2)*B/pi liga essa resposta finita ao tensor covetor anterior. O casamento do calor e provado. O defeito de area tem coeficiente -frequency^2*log(2)*B+eta*Ric(d,d)/2. Sua anulacao continua equivalente ao balanco nulo de Ricci; sob essa hipotese e as demais condicoes geometricas explicitadas, segue a equacao de Einstein com Lambda constante no dominio preconexo.","","Controle em infinitos sitios: b_n=(1/24)*(1/2)^n, B=1/12, sum b_n^2=1/432 e kappa=log(2)/(12*pi)>0. Todos os sitios mudam para parametro nao nulo. Amplitudes zero devolvem o estado original. No plano, a fonte nao nula e conservada e satisfaz calor, mas o casamento de area falha para todo eta.","","[KNOWN] [Casini, Relative entropy and the Bekenstein bound](https://arxiv.org/abs/0804.2182) trata entropia relativa de estados reduzidos e uma formulacao do limite em espaco plano. [Jacobson, Entanglement Equilibrium and the Einstein Equation](https://arxiv.org/abs/1505.04753) relaciona Einstein a uma hipotese de equilibrio, com alcance e condicoes proprios. Nenhum desses resultados e importado como axioma desta formalizacao.","","[OPEN] O limite diagonal especificado nao foi identificado ao funcional de Araki completo. A curva e o acoplamento sao escolhas explicitas, e a origem microscopica da correspondencia de area permanece aberta. Finitude da resposta global nao prova H3.","","## Criterios","","| Criterio | Estado | Evidencia |","|---|---|---|"]
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.",
        'Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiom aticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.',
        '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation028.py'}'",
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO028_DERIVACAO_PREVIA.md','CONTINUACAO028_PARECER.md','audit_continuation028.py'])
    for item in data['files']:
        if item['path'] in primary:
            rows.append(f"| \u0060{item['path']}\u0060 | \u0060{item['sha256']}\u0060 |")
    rows += ['', '## Tentativas preservadas', '']
    rejected = 0
    for module in data['modules']:
        for run in module['attempts']:
            if run['rejected_copy']:
                rejected += 1
                kind = ('registro da bancada sobre interrupcao, sem saida do compilador' if run['record_kind'] == 'bench_interruption_note' else 'saida do compilador')
                rows.append(f"- \u0060{run['rejected_copy']}\u0060: exit {run['exit_code']}; copia exata do registro rejeitado ({kind}).")
    rows += ['', f'{rejected} tentativas rejeitadas preservadas, incluindo eventual interrupcao explicitamente rotulada como nota da bancada. Fontes compilados recuperaveis pelos arquivos finais e backups dos bytes. Somente as compilacoes finais limpas sustentam esta entrega.',
        '', '## Dividas', '']
    rows.extend('- '+item for item in data['inputs_and_unpaid'])
    rows += ['', 'Originais, um.py, kernel canonico, Atlas, memorias, diarios, gate e entregas anteriores intocados. Nenhuma confirmacao fisica e declarada. O objetivo amplo permanece ativo e nao alcancado. Gerencia audita antes de incorporar.',
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO028_PARECER.md')+'.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_028_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_028_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 028 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation028.py [--write]')

