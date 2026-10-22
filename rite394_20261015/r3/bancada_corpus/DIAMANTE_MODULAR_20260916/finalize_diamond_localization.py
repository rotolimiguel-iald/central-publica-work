from pathlib import Path
import datetime
import hashlib
import json
import os
import re

ROOT = Path(__file__).resolve().parent
CHATGPT = ROOT.parent
now = datetime.datetime.now().astimezone().isoformat()
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(p):
    raw = p.read_bytes()
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def create(p, content):
    assert p.resolve().is_relative_to(CHATGPT.resolve())
    assert not p.exists(), p
    raw = content.encode('utf-8') if isinstance(content, str) else content
    tmp = p.with_name(p.name + '.tmp_' + stamp)
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw
    os.replace(tmp, p)
    assert p.read_bytes() == raw

def create_json(p, content):
    create(p, json.dumps(content, ensure_ascii=False, indent=2))

def append(p, content):
    assert p.resolve().is_relative_to(CHATGPT.resolve())
    old = p.read_bytes()
    backup = p.with_name(p.name + '.bak_' + stamp)
    create(backup, old)
    new = old + ('\r\n\r\n' + content + '\r\n').encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + stamp)
    tmp.write_bytes(new)
    assert tmp.read_bytes() == new and len(new) > len(old)
    os.replace(tmp, p)
    assert p.read_bytes() == new and backup.read_bytes() == old
    return backup

source = ROOT / 'WedgeNetFiniteDiamond.lean'
source_pin = pin(source)
runs = []
for rp in (ROOT / 'attempts').glob('*/run.json'):
    r = json.loads(rp.read_text(encoding='utf-8'))
    if r['source'] == str(source) and r['sha256'] == source_pin['sha256'] and r['returncode'] == 0:
        assert r['source_unchanged']
        runs.append(rp)
assert runs
run = sorted(runs)[-1]
stdout = run.parent / 'stdout.txt'
stderr = run.parent / 'stderr.txt'
out = stdout.read_text(encoding='utf-8')
assert not stderr.read_text(encoding='utf-8').strip()
assert not re.search(r'\b(error|warning):|sorryAx', out)
names = re.findall(r'^theorem\s+(\w+)', source.read_text(encoding='utf-8'), re.M)
rows = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", out, re.S)
assert len(names) == len(rows) == 7
proofs = []
for name, dependencies in rows:
    deps = sorted(x.strip() for x in dependencies.split(',') if x.strip())
    assert set(deps) <= {'propext', 'Classical.choice', 'Quot.sound'}
    assert name.rsplit('.', 1)[-1] in names
    proofs.append({'name': name, 'axioms': deps})
canonical_path = ROOT / 'CANONICAL_DIAMOND_SOURCE_AUDIT.json'
canonical = json.loads(canonical_path.read_text(encoding='utf-8'))
assert canonical['canonical_source_equal_to_imported_source']
assert canonical['declared_gate']
assert pin(Path(canonical['imported_wedge_source']['path'])) == canonical['imported_wedge_source']
atlas_receipt = json.loads((ROOT / 'ATLAS_READ_CENTRALIZADOR.json').read_text(encoding='utf-8'))
assert pin(Path(atlas_receipt['source']['path'])) == atlas_receipt['source']

audit = {
    'timestamp': now, 'status': 'LEAN_ACCEPTED_WITHOUT_WARNINGS',
    'source': source_pin, 'compile_record': pin(run),
    'stdout': pin(stdout), 'stderr': pin(stderr), 'proofs': proofs,
    'theorems': len(proofs), 'new_axioms': False,
    'canonical_source_audit': pin(canonical_path),
    'existing_imported_objects_reused': True,
    'fresh_full_canonical_build': False, 'independent_reviewer': False,
    'canonical_gate_changed': False,
    'scope': 'Existing wedgeNet on bounded Minkowski diamonds. Not a theorem about every QFT.',
    'physical_coefficient_computed': False,
    'all_atlas_bytes_still_match_completed_read_receipt': True,
}
create_json(ROOT / 'AUDIT_DIAMANTE_LOCALIZACAO.json', audit)
create_json(ROOT / 'REQUISITOS_DIAMANTE_LOCALIZACAO.json', {
    'timestamp': now, 'turn_classification': 'PROGRESS', 'goal_status': 'ACTIVE',
    'new_result': 'Existing finite-diamond algebra equals scalarAlg and differs from wedge algebra',
    'full_atlas_read': 'VERIFIED_UNCHANGED',
    'first_variation_and_centrality_criterion': 'PREVIOUS_DELIVERY_PRESERVED',
    'physical_diamond_coefficient': 'OPEN',
    'quantum_gravity_solution': 'NOT_ACHIEVED',
    'remaining': ['Construct or identify a nontrivial physical regional realization',
                  'Identify stress-energy charge and vacuum in that realization',
                  'Compute the remainder with a specified comparison of states and regions'],
    'no_progress_streak': 0, 'blocked_declared': False,
    'canonical_um_modified': False, 'canonical_gate_changed': False,
})

memory = f'''## {now} — localização efetiva do diamante na torre

[REAL] Acesso canônico de leitura obtido; supera a pendência de acesso anterior. Fonte WedgeNet canônica idêntica à usada pela dependência local, por SHA256. Busca delimitada a TGL/TGLExt e 16 fontes pinadas em CANONICAL_DIAMOND_SOURCE_AUDIT.json; o selo existente foi lido, não reexecutado. Atlas permanece byte a byte igual ao recibo de leitura integral anterior.
[REAL] Sete teoremas Lean em WedgeNetFiniteDiamond.lean: regiões limitadas em x1 não contêm cunhas transladadas; recebem scalarAlg; diamante redondo de Minkowski está nesse caso; todo resto limitado tem ação trivial; sua álgebra é diferente da cunha não abeliana. Compilação aceita, sem warning/sorry/novo axioma. Dependências compiladas reutilizadas; sem revisão independente. A identificação scalarAlg=C1 e o argumento geral U=1+localidade+covariância⇒abelianidade em diamantes estão provados no texto, sem reivindicar formalização extra.
[OPEN] Essa centralidade automática não determina o primeiro coeficiente físico. A quarta face recebe EOM como hipótese e não identifica K_boundary com T·xi. Redes PhysicalNetData de fibras não substituem essa identificação regional pelo nome. O contrato de dualidade da torre permanece fechado no seu escopo; nenhum gate foi alterado. Nenhum novo motor de dephasing foi criado.
Entrega: HANDOFF_DIAMANTE_LOCALIZACAO.md, AUDIT_DIAMANTE_LOCALIZACAO.json e DIAMANTE_LOCALIZACAO_MANIFEST.json. Originais preservados; memórias locais com backup de bytes. Objetivo amplo ativo, progresso real; solução física de gravidade quântica não alcançada. Próximo passo técnico é a realização regional física, não repetir a centralidade finita já provada.'''
backups = [append(ROOT / 'MEMORIA_CENTRAL.md', memory),
           append(ROOT / 'REGISTRO_DAS_CONVERSAS.md',
                  f'''## {now} — continuação autônoma do objetivo vigente

O objetivo permaneceu: centralidade de R no diamante interagente UV completo, coeficiente e solução física de QG. Nenhuma nova fala do operador foi inventada neste registro. A bancada conferiu fontes canônicas em leitura, elaborou sete teoremas sobre a rede existente, delimitou a diferença entre cunha e diamante e entregou adendo. A meta completa não foi marcada como concluída nem bloqueada. Detalhes e evidências no HANDOFF_DIAMANTE_LOCALIZACAO.md.'''),
           append(ROOT / 'PROPOSTA_MEMORIA_ATLAS.md', memory)]

door = CHATGPT / 'TUNEL/DO_CHATGPT/ENTREGA_DIAMANTE_LOCALIZACAO_20260916.md'
base = ROOT.as_posix()
create(door, f'''# Entrega — localização do diamante na rede existente

{now}

[REAL] Sete teoremas Lean aceitos: todo diamante finito redondo de Minkowski recebe scalarAlg na wedgeNet atual; sua álgebra é diferente da cunha. A trivialidade da ação de qualquer resto limitado nesse setor é automática e não calcula o coeficiente físico. Não altera o gate algébrico.

- [Handoff e prova]({base}/HANDOFF_DIAMANTE_LOCALIZACAO.md)
- [Fonte Lean]({base}/WedgeNetFiniteDiamond.lean)
- [Auditoria da elaboração]({base}/AUDIT_DIAMANTE_LOCALIZACAO.json)
- [Fontes canônicas e hashes]({base}/CANONICAL_DIAMOND_SOURCE_AUDIT.json)
- [Manifesto da entrega]({base}/DIAMANTE_LOCALIZACAO_MANIFEST.json)
- [Adendo anterior sobre coeficientes]({base}/HANDOFF_CENTRALIZADOR_ADENDO.md)
- [Memória local]({base}/MEMORIA_CENTRAL.md)

As provas anteriores permanecem; evitar duplicar funções. [OPEN] realização regional física e identificação com a carga de tensão-energia. Atualização das memórias canônicas pela gerência, com backup de bytes e append. Todos os arquivos desta bancada ficam em Chatgpt.
'''.replace('](', '](<').replace('.md)', '.md>)').replace('.lean)', '.lean>)').replace('.json)', '.json>)'))

paths = [source, ROOT / 'HANDOFF_DIAMANTE_LOCALIZACAO.md',
         ROOT / 'AUDIT_DIAMANTE_LOCALIZACAO.json', canonical_path,
         ROOT / 'REQUISITOS_DIAMANTE_LOCALIZACAO.json',
         ROOT / 'capture_diamond_sources.py', Path(__file__),
         ROOT / 'MEMORIA_CENTRAL.md', ROOT / 'REGISTRO_DAS_CONVERSAS.md',
         ROOT / 'PROPOSTA_MEMORIA_ATLAS.md', door, run, stdout, stderr,
         ROOT / 'ATLAS_READ_CENTRALIZADOR.json'] + backups
manifest = {'timestamp': now, 'status': 'DELIVERED_LOCAL_SCOPE_AUDIT',
            'artifacts': [pin(p) for p in paths],
            'gate_changed': False, 'complete_goal_achieved': False}
create_json(ROOT / 'DIAMANTE_LOCALIZACAO_MANIFEST.json', manifest)
for item in manifest['artifacts']:
    assert pin(Path(item['path'])) == item
print(json.dumps({'theorems': len(proofs), 'manifest_artifacts_verified': len(paths),
                  'memory_backups': [str(p) for p in backups],
                  'handoff': str(ROOT / 'HANDOFF_DIAMANTE_LOCALIZACAO.md'),
                  'goal': 'ACTIVE'}, ensure_ascii=False))
