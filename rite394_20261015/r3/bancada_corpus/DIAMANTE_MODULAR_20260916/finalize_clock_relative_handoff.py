"""Issue once, or verify read-only, the recovered-clock and modular handoff."""
import argparse
import json
from pathlib import Path
import re
import hashlib
from finalize_weyl_bridge import ROOT, WORK, NOW, pin, atomic, backed_replace

MANIFEST = ROOT / 'CLOCK_RELATIVE_HANDOFF_MANIFEST.json'


def collect_pins(value):
    found = []
    if isinstance(value, dict):
        if {'path', 'bytes', 'sha256'} <= value.keys():
            found.append({k: value[k] for k in ('path', 'bytes', 'sha256')})
        else:
            for child in value.values():
                found.extend(collect_pins(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(collect_pins(child))
    return found


def verify():
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    failures = []
    records = data['sources'] + data['artifacts'] + data['v2_historical_pins_checked']
    for old in records:
        try:
            actual = pin(Path(old['path']))
            if actual != old:
                failures.append({'path': old['path'], 'error': 'BYTES_CHANGED'})
        except OSError as exc:
            failures.append({'path': old['path'], 'error': str(exc)})
    for old in data['v2_historical_memory_prefixes']:
        try:
            raw = Path(old['path']).read_bytes()
            if hashlib.sha256(raw[:old['bytes']]).hexdigest() != old['sha256']:
                failures.append({'path': old['path'], 'error': 'V2_MEMORY_PREFIX_CHANGED'})
        except OSError as exc:
            failures.append({'path': old['path'], 'error': str(exc)})
    for item in data['memory_appends']:
        try:
            backup = Path(item['backup']['path']).read_bytes()
            current = Path(item['after']['path']).read_bytes()
            if pin(Path(item['backup']['path'])) != item['backup']:
                failures.append({'path': item['backup']['path'], 'error': 'BACKUP_CHANGED'})
            if not current.startswith(backup):
                failures.append({'path': item['after']['path'], 'error': 'PREFIX_LOST'})
            size = item['after']['bytes']
            if hashlib.sha256(current[:size]).hexdigest() != item['after']['sha256']:
                failures.append({'path': item['after']['path'], 'error': 'APPEND_CHANGED'})
        except OSError as exc:
            failures.append({'path': item['after']['path'], 'error': str(exc)})
    print(json.dumps({'status': 'FAIL' if failures else 'PASS',
                     'frozen_records': len(records),
                     'v2_historical_records': len(data['v2_historical_pins_checked']),
                     'memory_prefixes': len(data['memory_appends']),
                     'failures': failures}, ensure_ascii=True))
    if failures:
        raise SystemExit(1)


def emit():
    if MANIFEST.exists():
        raise FileExistsError('One-shot emission already exists; use --verify')
    missing_output = WORK / 'HOMOTOPIA_BV_RELOGIOS_088_20260910'
    assert not missing_output.exists(), 'Historical-output status changed: inspect first'
    names = [
        'write_bv_clock088_new.py',
        'EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md',
        'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md',
        'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
        'RELOGIOS_RELACIONAIS_FUNDO_FISICO_088_20260910/RELOGIOS_X_SIGMA_E_RETRACAO_DE_JATOS.md',
        'DOMINIO_RELOGIOS_FISICOS_088_20260910/NOTE.payload.md',
        'DESCIDA_HORIZONTAL_WEYL_PAR_088_20260910/DESCIDA_POR_FORMAS_E_IMAGEM_HORIZONTAL_WEYL_PAR.md',
    ]
    sources = [pin(WORK / name) for name in names]
    for name in ('HANDOFF_MANIFEST.json', 'HANDOFF_TECNICO_V2.md',
                 'HANDOFF_DEFINICAO_CONJUNTA.md', 'JOINT_DEFINITION_MANIFEST.json'):
        sources.append(pin(ROOT / name))
    historical = json.loads((ROOT / 'HANDOFF_MANIFEST.json').read_text(encoding='utf-8'))
    v2_all = list({item['path']: item for item in collect_pins(historical)}.values())
    # The V2 memory proposal is append-only, unlike the frozen proof artifacts.
    v2_memory = [item for item in v2_all
                 if Path(item['path']) == ROOT / 'PROPOSTA_MEMORIA_ATLAS.md']
    v2 = [item for item in v2_all if item not in v2_memory]
    for old in v2_memory:
        raw = Path(old['path']).read_bytes()
        assert hashlib.sha256(raw[:old['bytes']]).hexdigest() == old['sha256'], old['path']
    for old in v2:
        assert pin(Path(old['path'])) == old, old['path']
    docs = ['PRIMITIVA_RELATIVA_RELOGIOS.md', 'REVISAO_PRIMITIVA_RELATIVA_RELOGIOS.md',
            'HANDOFF_VACUO_TORRE_E_INTERACAO.md']
    links = []
    for name in docs:
        body = (ROOT / name).read_text(encoding='utf-8')
        for raw in re.findall(r'\]\(([^)\n]+)\)', body):
            if raw.startswith(('http:', 'https:', '#')):
                continue
            target = (ROOT / raw.strip('<>')).resolve()
            if target == MANIFEST:
                continue
            assert target.is_file(), (name, raw)
            links.append({'document': name, 'target': str(target)})
    # Pin documentary inputs before and after finalization; do not execute them.
    appendix = f'''
## {NOW} — primitiva relativa localizada e handoff vácuo–torre

[REAL — recuperação documental] write_bv_clock088_new.py contém uma demonstração BV em sua string body, mas sua pasta HOMOTOPIA_BV_RELOGIOS_088_20260910 não foi encontrada. O helper não foi executado. Não confundir prova redigida com entrega emitida/revisada. NOTE.payload.md da auditoria de domínio é uma fonte existente, não uma aprovação de toda a cadeia.

[DERIVED — revisão independente Singer] PRIMITIVA_RELATIVA_RELOGIOS.md consome FK=Id de068 e BV069: na completação localizada do aberto dos relógios, sem coeficientes de ghost positivo, H^{{g,p}}(s|d_H)=0 para g>0, 0<=p<=4. Todas as variáveis BV contam na valência. A recorrência R=a-sB-dC, b_R=b-sC, DeltaB_E=h0R_E, DeltaC_E=h0(b_R)_E evita exigir uma descida completa. Antifields incluídos; não é teorema Lean nem QME. Fonte primária do mecanismo relativo: BBH hep-th/0002245, apêndice2.B.

[OPEN — ligação exata] Primitiva localizada não é família admissível de contratermos Q2: escala, contatos, aridades e categoria de fundos continuam requisitos. Estado livre067/P0 pagos não são reabertos; cargaP2/UV não são promovidos. A condição regional kT_tf=delta_D^(it)kf permanece distinta da ponte parcial da torre.

[HANDOFF] HANDOFF_VACUO_TORRE_E_INTERACAO.md é a porta atual. A V2 já fornece igualdade dos fluxos do estado produto e da referência parcial tracial em E_last, com R sobrevivente e ação invisível. Leitura completa é estacionária. Não criar canal/cociclo duplicado nem usar E(R)=0 como critério. Esta rodada confere bytes históricos, não recompila o kernel; zero alteração/execução/importação de um.py, zero movimento de gate medido. Proposta de memória canônica encaminhada pela gerência; apenas Chatgpt foi escrito.
'''
    memory = []
    for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md', 'PROPOSTA_MEMORIA_ATLAS.md'):
        path = ROOT / name
        before = path.read_bytes()
        backup = backed_replace(path, before + appendix.encode('utf-8'))
        assert Path(backup['path']).read_bytes() == before
        memory.append({'backup': backup, 'after': pin(path)})
    tunnel = WORK / 'TUNEL/DO_CHATGPT/ENTREGA_VACUO_TORRE_PRIMITIVA_RELATIVA_20260916.md'
    atomic(tunnel, f'''# Entrega — handoff consolidado vácuo, torre e interação

{NOW}. [DERIVED revisado — primitiva BRST relativa na categoria localizada] [KERNEL histórico — ponte V2, bytes conferidos].

- [Handoff para a sessão do um.py](../../DIAMANTE_MODULAR_20260916/HANDOFF_VACUO_TORRE_E_INTERACAO.md)
- [Prova relativa](../../DIAMANTE_MODULAR_20260916/PRIMITIVA_RELATIVA_RELOGIOS.md)
- [Revisão independente](../../DIAMANTE_MODULAR_20260916/REVISAO_PRIMITIVA_RELATIVA_RELOGIOS.md)
- [Manifesto](../../DIAMANTE_MODULAR_20260916/CLOCK_RELATIVE_HANDOFF_MANIFEST.json)

Não repetir FK=Id, P0, o canal ou a torre. O rascunho BV088 foi localizado em helper não executado; a prova consumida nesta rodada tem revisão própria. A primitiva relativa dispensa descida completa na localização física, mas não fornece automaticamente normalizações causais Q2/P2. A ponte de ações da torre parcial permanece distinta de sua identificação com a carga geométrica regional. Não houve escrita/execução/importação de originais ou mudança de gate.
''')
    assert all(pin(Path(item['path'])) == item for item in sources)
    data = {
        'timestamp': NOW,
        'status': 'WRITTEN_RELATIVE_PROOF_REVIEWED__LOCALIZED_CATEGORY_ONLY',
        'sources': sources,
        'artifacts': [pin(ROOT / name) for name in docs] + [pin(tunnel), pin(Path(__file__))],
        'v2_historical_pins_checked': v2,
        'v2_historical_memory_prefixes': v2_memory,
        'memory_appends': memory,
        'links_checked': links,
        'recovered_draft': {'path': str(WORK / names[0]), 'executed': False,
                            'announced_output': str(missing_output), 'found_at_emission': False},
        'reviewer': 'Singer / 01a0ac43-294f-7d21-9237-38c5de79dbb7',
        'source_reading_scope': 'See review; main used BRST068 sections1-3. No recursive audit of every source.',
        'primary_reference': 'https://arxiv.org/pdf/hep-th/0002245',
        'new_lean_compilations': 0, 'new_numerical_physics_tests': 0,
        'new_engine_functions': 0, 'canonical_executed': False, 'canonical_modified': False,
        'qme_proved': False, 'uv_proved': False, 'gate_movement_measured': False,
        'issuance_note': 'First preflight rejected a full-file hash of append-only memory before any memory mutation. Corrected to verify its historical byte prefix; all frozen proof hashes still exact.',
    }
    atomic(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2))
    verify()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--emit', action='store_true')
    group.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    emit() if args.emit else verify()
