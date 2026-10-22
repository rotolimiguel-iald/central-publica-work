"""Exact-byte and Lean-output audit for spontaneous continuation 027.

Default mode is read-only. --write creates new output and refuses overwrites.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ["ProfileGNSPre","ProfileGNSUnitary","ProfileFactorTransport","UnitaryPartialTransport","ProfileTomitaTransport","ProfileModularTransport","ProfileFlowTransport","ProfileTransportControls"]
MANIFEST = ROOT / 'CONTINUACAO027_MANIFESTO.json'
DELIVERY = ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_027_ESPONTANEA_transporte_unitario_e_modular.md'
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
    if namespace != 'ChatgptAudit.Transport027':
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

    visit('ProfileTransportControls')
    if not set(MODULES) <= visited:
        raise RuntimeError('Final integration module does not reach all new modules')
    for namespace in ('TGL', 'TGLExt'):
        paths.update((ROOT / namespace).rglob('*.olean'))
    for name in [
        'audit_continuation027.py', 'revise_continuation027.py', 'verify_stage.ps1',
        'CONTINUACAO027_DERIVACAO_PREVIA.md', 'CONTINUACAO027_PARECER.md',
        'TUNEL/TUNEL_PROTOCOLO.md', 'CONTINUACAO026_MANIFESTO.json', 'audit_continuation026.py', 'CONTINUACAO025_MANIFESTO.json', 'audit_continuation025.py', 'CONTINUACAO024_MANIFESTO.json', 'audit_continuation024.py', 'CONTINUACAO023_MANIFESTO.json', 'audit_continuation023.py', 'TUNEL/PARA_CHATGPT/ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md', 'TUNEL/PARA_CHATGPT/ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md', 'CONTINUACAO022_MANIFESTO.json', 'audit_continuation022.py', 'CONTINUACAO021_MANIFESTO.json', 'audit_continuation021.py', 'CONTINUACAO020_MANIFESTO.json', 'audit_continuation020.py', 'CONTINUACAO019_MANIFESTO.json', 'audit_continuation019.py', 'CONTINUACAO018_MANIFESTO.json', 'audit_continuation018.py', 'CONTINUACAO017_MANIFESTO.json', 'audit_continuation017.py', 'CONTINUACAO016_MANIFESTO.json', 'audit_continuation016.py', 'CONTINUACAO015_MANIFESTO.json', 'audit_continuation015.py', 'CONTINUACAO012_MANIFESTO.json',
        'audit_continuation012.py', 'CONTINUACAO014_MANIFESTO.json', 'audit_continuation014.py',
        'CONTINUACAO013_MANIFESTO.json', 'audit_continuation013.py',
        'CONTINUACAO011_MANIFESTO.json',
        'CONTINUACAO010_MANIFESTO.json', 'CONTINUACAO009_MANIFESTO.json',
        'CONTINUACAO008_MANIFESTO.json', 'ORDEM007_MANIFESTO.json', 'audit_continuation011.py',
        'fontes/tgl_kernel/TGLExt/TowerDefinite.lean', 'fontes/tgl_kernel/TGLExt/RightMult.lean', 'fontes/tgl_kernel/TGLExt/SignatureInTheLimit.lean', 'fontes/tgl_kernel/TGLExt/ModularFirstLaw.lean',
        'fontes/tgl_kernel/TGLExt/Solder4D.lean', 'fontes/tgl_kernel/TGLExt/TheImportedEquilibrium.lean',
    ]:
        paths.add(ROOT / name)
    paths.update(ROOT.glob('CONTINUACAO027_*.md.bak_*'))
    paths.update(ROOT.glob('audit_continuation027.py.bak_*'))
    paths.update(ROOT.glob('revise_continuation027.py.bak_*'))
    files = []
    for path in sorted(paths):
        if not path.is_file():
            raise RuntimeError(f'Missing artifact: {path}')
        files.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': digest(path)})
    return {
        **{"status":"REAL: exact bytes and clean Lean compiler evidence; independent managerial audit pending","kind":"spontaneous continuation 027; no managerial order 027 issued at publication time","reuse":["product tower, canonical Tomita closure, positive self-adjoint half operator, Delta and modular group proved in earlier bench modules","positive infinite affinity criterion, global vector with all Q marginals, inverse-filter recovery and cyclicity/separation from continuation 026","Hilbert completion, continuous linear isometries, homeomorphisms and full LinearPMap adjoints in mathlib"],"paid":["well-defined linear inner-product-preserving map on the Q GNS quotient into the original H(P)","continuous isometric completion, exact intertwining on every local operator, surjectivity and a unitary U:H(Q)->H(P) sending Omega_Q to Phi","star-algebra conjugation sends the full factor M(Q) exactly onto M(P), proved through both centralizers","actual graph {(A Phi,A* Phi):A in M(P)} and its closure are transported by U x U, with exact domain and single-valued closed Tomita operator","generic transport of partial operator domains and graphs; density, closure, positivity and self-adjointness via the entire adjoint graph","antiunitary involution J_Phi, S_Phi=J_Phi A_Phi, A_Phi=J_Phi S_Phi positive and self-adjoint","Delta_Phi positive and self-adjoint; its domain equals {x in D(A_Phi):A_Phi x in D(A_Phi)}, and Delta_Phi equals A_Phi applied twice","local actions of A_Phi and Delta_Phi use the weights of Q on the cyclic vector Phi inside H(P)","unitary strongly continuous modular group, group law, fixed Phi, preservation of the original factor and vector state, and exact local action","transported eigenvectors, Delta eigenvalues, modular phases and uniqueness of the bounded flow from its spectral action on a total family","P=Q controls recover Phi=Omega, U=identity, factor conjugation, canonical J and canonical modular flow","infinite-site harmonic profile from 026 gives a different vector that is outside the old modular orbit of Omega","first off-diagonal modular eigenvalue changes from 1/2 to 5/7; transported Delta and flow realize the new value"],"inputs_and_unpaid":["P e Q sao perfis produto estritamente positivos fornecidos como INPUT; exige-se C(P,Q)>0. A 026 prova este antecedente para o exemplo harmonico.","A equivalencia unitaria foi construida para esta classe suficiente. Nao se prova necessidade de C>0 para toda equivalencia de representacoes, nem disjuncao geral quando C=0.","A nova S e identificada com o fecho do grafico real de Tomita em todo M(P). A auto-adjunticidade usa o adjunto inteiro; igualdade apenas numa torre densa nao foi usada como substituto.","A expressao raiz quadrada positiva refere-se a A positivo auto-adjunto com dominio e quadrado iguais aos de Delta demonstrados. Nao foi adicionada uma biblioteca geral de calculo funcional nao limitado ou um novo teorema abstrato de unicidade de raizes.","O fluxo construido transporta o grupo canonico de Q. A caracterizacao espectral e tipada na familia total transportada; nao se atribui a um grupo abstrato de hipoteses insuficientes.","O estado vetorial de 026 tem SeqWOTContinuous formalizado. Esta etapa nao formaliza um predual geral ou normalidade por todas as redes.","Nao se escolheu Q por uma dinamica fisica, nem se construiu estado correlacionado, gerador de translacao de energia positiva ou uma nova inclusao modular meio-lateral.","Nao se provou diferenciabilidade temporal do caminho P->Q, susceptibilidade global finita, lei de area, temperatura fisica ou fonte gravitacional microscopica.","Metrica lorentziana suave, dimensao, referencial, conservacao e relacao de Clausius/casamento microscopico permanecem hipoteses ou lacunas dos resultados geometricos condicionais. H3 e a reconstrucao gravitacional geral continuam abertas.","O objetivo amplo de gravidade quantica permanece nao alcancado. Nenhum gate, selo canonico, memoria ou conclusao observacional foi alterado."],"criteria":[["Derivacao anterior ao codigo","PAGO","CONTINUACAO027_DERIVACAO_PREVIA.md; auditoria 026 reconferida."],["Mapa no quociente GNS e isometria","PAGO","profile_gns_pre_tof, _add, _smul, _inner e _norm."],["Completamento, sobrejetividade e entrelacamento","PAGO","profile_gns_surjective, profileGNSUnitary, profile_gns_unitary_omega e _intertwines."],["Fator completo","PAGO","star_equiv_centralizer_transport e profile_factor_conjugation_iff."],["Tomita do estado Phi","PAGO","profile_tomita_graph_image, _closed_graph_eq, _domain_iff e _extends_star."],["Transporte do adjunto completo","PAGO","selfadjoint_weak_graph e unitary_partial_selfadjoint."],["JS positivo e auto-adjunto","PAGO","profile_js_equals_half, profile_half_positive e profile_half_selfadjoint."],["Quadrado e dominios","PAGO","profile_delta_domain_iff, profile_delta_is_square e profile_delta_selfadjoint."],["Grupo modular no Hilbert original","PAGO","profile_flow_group, _strongly_continuous, _preserves_factor, _preserves_state e _spectral_unique."],["Controle P=Q","PAGO","global_profile_vector_same, profile_unitary_self, profile_j_self e profile_flow_self."],["Instancia nao trivial","PAGO","gradual_profile_vector_ne_reference, old_modular_orbit_ne_gradual, gradual_first_eigenvalue e gradual_transported_delta_value."],["Selecao fisica e reconstrucao gravitacional geral","NAO PAGO","Nao decorrem automaticamente do transporte entre estados produtos; H3 e demais antecedentes persistem."]],"dependency_limit":"Local source closure and copied TGL/TGLExt oleans pinned. External Lean 4.31.0/mathlib is resolved by verify_stage.ps1; this is not a portable dependency bundle or independent recompilation."},
        'incoming_orders': [str(p) for p in sorted((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_*.md'))],
        'modules': records, 'theorems': sum(row['theorems'] for row in records),
        'integrated_root': 'ProfileTransportControls',
        'printed_definitions': sum(row['printed_definitions'] for row in records),
        'bench_source_build_order': order, 'files': files,
    }


def delivery_text(data):
    rows = ["[REAL / INPUT / OPEN] ENTREGA 027 ESPONTANEA — equivalencia unitaria e transporte modular com dominios.","","06/09/2026. Continuacao do objetivo associado a ordem 007. A entrega 026 foi reconferida e classificada como PROGRESSO. Nao e uma nova ordem gerencial.","","Dados perfis produto positivos P,Q com afinidade infinita C(P,Q)>0, a 026 fornece Phi em H(P). Esta entrega constroi U:H(Q)->H(P), unitaria sobrejetora, com U Omega_Q=Phi e U pi_Q(a)=pi_P(a) U. A conjugacao por U transporta exatamente M(Q) a M(P), inclusive os dois centralizadores.","","O grafico real {(A Phi,A* Phi):A em M(P)} e a imagem do grafico canonico de Q por U x U. O mesmo vale para seus fechos. Assim, S_Phi e o Tomita do estado em todo o fator original, com dominio explicitamente identificado.","","J_Phi=U J_Q U^-1 e antiunitario involutivo. A_Phi=J_Phi S_Phi e positivo e auto-adjunto. Delta_Phi=U Delta_Q U^-1 tambem e positivo e auto-adjunto, com D(Delta_Phi)={x em D(A_Phi):A_Phi x em D(A_Phi)} e Delta_Phi x=A_Phi(A_Phi x). O transporte generico de auto-adjunticidade prova a igualdade com o adjunto completo.","","O grupo V_Phi(t)=U V_Q(t) U^-1 e unitario, fortemente continuo, preserva M(P) e o estado e fixa Phi. Foram calculadas sua acao local, as razoes de pesos de Q para Delta e as fases correspondentes; a acao espectral determina o operador limitado em todo H(P).","","Para Q=P, Phi=Omega e U=identidade; J e fluxo voltam aos canonicos. Para P_n=1/3 e Q_n=1/3+1/(12(n+1)), a 026 paga C>0. O novo vetor difere de Omega e nao pode ser sua orbita pelo fluxo modular antigo, que fixa Omega. No primeiro sitio, a razao modular 1/2 passa a 5/7, com a acao transportada provada.","","[KNOWN] Estados produtos e equivalencias ligadas a afinidades pertencem a teoria classica; ver [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf). O resultado aqui e a formalizacao concreta na torre da casa, sem importar o teorema geral como axioma.","","[OPEN] A construcao nao seleciona o perfil por dinamica fisica, nao constroi correlacoes ou geometria e nao paga H3. A reconstrucao gravitacional geral permanece aberta.","","## Criterios","","| Criterio | Estado | Evidencia |","|---|---|---|"]
    rows.extend('| '+' | '.join(row)+' |' for row in data['criteria'])
    rows += ['', f"{len(data['modules'])} modulos; {data['theorems']} teoremas; {data['printed_definitions']} definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.",
        'Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiom aticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.',
        '', '## Reproducao', '', '\u0060\u0060\u0060powershell',
        f"& 'C:\\Python314\\python.exe' -B '{ROOT / 'audit_continuation027.py'}'",
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
    primary.update(str(ROOT / n) for n in ['CONTINUACAO027_DERIVACAO_PREVIA.md','CONTINUACAO027_PARECER.md','audit_continuation027.py'])
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
        '', 'Parecer: '+str(ROOT / 'CONTINUACAO027_PARECER.md')+'.',
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
        occupied = list((ROOT / 'TUNEL/PARA_CHATGPT').glob('ORDEM_027_*'))
        occupied += list((ROOT / 'TUNEL/DO_CHATGPT').glob('ENTREGA_027_*'))
        if MANIFEST.exists() or occupied:
            raise RuntimeError('Number 027 already occupied; refusing publication')
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
        raise SystemExit('Usage: audit_continuation027.py [--write]')
