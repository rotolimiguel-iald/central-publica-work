"""Issue or read-only verify the joint-definition handoff and its custody."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from finalize_weyl_bridge import ROOT, WORK, NOW, pin, atomic, backed_replace


def verify():
    manifest = json.loads((ROOT / 'JOINT_DEFINITION_MANIFEST.json').read_text(encoding='utf-8'))
    failures = []
    records = manifest['delivery_sources'] + manifest['artifacts'] + [manifest['operator_receipt']]
    for old in records:
        path = Path(old['path'])
        try:
            current = pin(path)
        except OSError as exc:
            failures.append({'path': str(path), 'error': str(exc)})
            continue
        if current['sha256'] != old['sha256'] or current['bytes'] != old['bytes']:
            failures.append({'path': str(path), 'error': 'BYTES_CHANGED'})
    # Memory entries are historical append-only snapshots, not frozen artifacts.
    for item in manifest['memory_appends']:
        before = Path(item['backup']['path']).read_bytes()
        current = Path(item['after']['path']).read_bytes()
        if not current.startswith(before):
            failures.append({'path': item['after']['path'], 'error': 'MEMORY_PREFIX_NOT_PRESERVED'})
        length = item['after']['bytes']
        if hashlib.sha256(current[:length]).hexdigest() != item['after']['sha256']:
            failures.append({'path': item['after']['path'], 'error': 'MEMORY_SNAPSHOT_NOT_PRESERVED'})
    print(json.dumps({'status': 'FAIL' if failures else 'PASS', 'frozen_records': len(records),
                      'memory_prefixes': len(manifest['memory_appends']), 'failures': failures}, ensure_ascii=True))
    if failures:
        raise SystemExit(1)


def emit():
    destination = ROOT / 'JOINT_DEFINITION_MANIFEST.json'
    if destination.exists():
        raise FileExistsError('One-shot emission already exists; use --verify')
    inventory = json.loads((ROOT / 'JOINT_DEFINITION_INVENTORY.json').read_text(encoding='utf-8'))
    approval = json.loads((ROOT / 'JOINT_READING_ACCEPTANCE.json').read_text(encoding='utf-8'))
    assert approval['all_three_reports_read_by_main'] is True
    assert approval['complete_delivery_coverage'] is True
    groups = {
        'CORE_AND_FRIEDMANN': ('AUDITORIA_CONJUNTA_CORE', 49),
        'GEOMETRY_AND_MODULAR_EARLY': ('AUDITORIA_CONJUNTA_GEOMETRIA', 60),
        'PHYSICAL_QUANTUM_AND_RECENT': ('AUDITORIA_CONJUNTA_FISICA', 47),
    }
    for group, (stem, count) in groups.items():
        assert sum(x['review_group'] == group for x in inventory['sources']) == count
        assert approval['groups'][group]['full_delivery_read_count'] == count
        assert (ROOT / (stem + '.json')).is_file()
        assert (ROOT / (stem + '.md')).is_file()
    sources = []
    for expected in inventory['sources']:
        current = pin(Path(expected['path']))
        assert current['sha256'] == expected['sha256'], current['path']
        assert current['bytes'] == expected['bytes'], current['path']
        sources.append(current)
    assert len(sources) == 156
    assert sum(x['bytes'] for x in sources) == 1962076
    links = []
    for name in ('DEFINICAO_CONJUNTA_E_COSTURAS.md', 'HANDOFF_DEFINICAO_CONJUNTA.md'):
        doc = ROOT / name
        for raw in re.findall(r'\]\(([^)\n]+)\)', doc.read_text(encoding='utf-8')):
            raw = raw.strip('<>')
            if raw.startswith(('http:', 'https:', '#')):
                continue
            target = (doc.parent / raw).resolve()
            assert target.exists(), (name, raw)
            links.append({'document': str(doc), 'target': str(target)})
    appendix = f'''
## {NOW} — definição conjunta do estudo inteiro

[INPUT — recibo do operador lido integralmente] “não é apenas um arquivo que define a ação quantica renormalizada, o vácuo e o tensor de energia regional, é todo o estudo da bancada do chatgpt, isso está respondido lá”. Fonte: TUNEL/PARA_CHATGPT/RESPOSTA_OPERADOR_16SET_DEFINICAO_CONJUNTA_NO_ESTUDO_INTEIRO.md. Esta resposta corrige o pedido anterior por um arquivo único. Não devolver essa localização ao operador.

[REAL — leitura documental distribuída] Inventário de todos os156 documentos markdown do túnel DO_CHATGPT no snapshot:1962076bytes. Três leituras disjuntas49/60/47, com relatórios e pins. Isso é leitura das entregas, não de todo arquivo recursivamente referido, nem execução de provas. JOINT_DEFINITION_MANIFEST.json registra a cobertura e seus limites.

[DERIVED — composição] DEFINICAO_CONJUNTA_E_COSTURAS.md reúne ação Einstein–sigma, equivalência variacional e bordo067, estado físico067, BRST068, produtos locais renormalizados069, contratermos/RG070, recorrência formal072 e domínio/polarização073. P0 e Wick compacto deP1 pagos; não reabrir. Rota de estado Araki061 e dinâmica extensiva063 reconhecidas nos seus domínios. T2/T4 já explícitos; não dizer ausência de tensor ou de renormalização.

[OPEN — costuras precisas] A quebra deQ2 precisa de primitiva/normalização admissível e cargaP2 implementada no mesmo espaço. Cofatores/cohomologia de categorias diferentes não são intercambiáveis. A série formal não é automaticamente estadoUV de vonNeumann. A carga regional precisa consumir o mesmo estado, prescrição e bordo; o teste permanece kT_t f=delta_D^(it)kf. Não confundir o númeroRG155/6 com coeficiente modular. A derivada deR recebe simultaneamente Drho e DKxi; a variação do centralizador inclui DA. Nenhuma resposta ao parâmetro de expansão foi presumida: descreveu-se uma direção conjunta de dados.

[INTEGRAÇÃO] HANDOFF_DEFINICAO_CONJUNTA.md aponta consumidores já existentes; zero novas funções ou teoremas. V2 da torre não reaberta. Originais, Atlas, índice e gate não alterados. Proposta de adendo para Atlas/índice/linhagem/desenho segue pela gerência; memórias locais têm backups imediatos de bytes. Objetivo amplo permanece ativo; esta etapa é composição documental e delimitação de contratos, não solução daQG.
'''
    memories = []
    for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'PROPOSTA_MEMORIA_ATLAS.md'):
        path = ROOT / name
        backup = backed_replace(path, path.read_bytes() + appendix.encode('utf-8'))
        memories.append({'backup': backup, 'after': pin(path)})
    tunnel = WORK / 'TUNEL/DO_CHATGPT/ENTREGA_DEFINICAO_CONJUNTA_20260916.md'
    atomic(tunnel, f'''[DERIVED — composição documental] [OPEN — carga regional interagente/UV e sua identificação modular]

# Entrega — definição conjunta do estudo inteiro

{NOW}. Responde à orientação do operador de compor a ação, o estado e a tensão a partir do estudo inteiro.156 documentos do snapshot lidos por três leitores; cobertura e limitações registradas. Não equivale a recompilação das fontes recursivamente ligadas.

- [Handoff](../../DIAMANTE_MODULAR_20260916/HANDOFF_DEFINICAO_CONJUNTA.md)
- [Definição e costuras exatas](../../DIAMANTE_MODULAR_20260916/DEFINICAO_CONJUNTA_E_COSTURAS.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/JOINT_DEFINITION_MANIFEST.json)

Ação/renormalização069, estado067, domínio073, recorrência072 e fontes/bordo estão reconhecidos. P0 não volta à lista de faltas. A cargaP2 e a composição regional mantêm seus contratos. Nenhuma nova função/Lean, execução deum.py, rito experimental ou alteração de gate. Incorporação de memória e documentação pela gerência, sem promover fonte escrita aKERNEL.
''')
    names = ['JOINT_DEFINITION_INVENTORY.json', 'JOINT_READING_ACCEPTANCE.json',
             'DEFINICAO_CONJUNTA_E_COSTURAS.md', 'HANDOFF_DEFINICAO_CONJUNTA.md',
             'record_physical_joint_audit.py', 'record_joint_acceptance.py', 'finalize_joint_definition.py']
    for stem, _ in groups.values():
        names.extend([stem + '.md', stem + '.json'])
    artifacts = [pin(ROOT / name) for name in names] + [pin(tunnel)]
    receipt = pin(Path(inventory['operator_receipt']['path']))
    assert receipt == inventory['operator_receipt']
    manifest = {
        'timestamp': NOW, 'scope': 'JOINT_DEFINITION_DOCUMENTARY_COMPOSITION',
        'operator_receipt': receipt, 'delivery_count': len(sources),
        'delivery_bytes': sum(x['bytes'] for x in sources), 'delivery_sources': sources,
        'artifacts': artifacts, 'memory_appends': memories,
        'local_links_checked': links, 'acceptance': approval,
        'recursive_primary_source_review': 'Selected sources only; not every linked proof.',
        'new_lean_theorems': 0, 'new_python_engine_functions': 0,
        'canonical_executed': False, 'canonical_modified': False,
        'gate_changed': False, 'quantum_gravity_solved': False,
    }
    atomic(destination, json.dumps(manifest, ensure_ascii=False, indent=2))
    verify()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--emit', action='store_true')
    mode.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    emit() if args.emit else verify()
