"""Custody one compiled Maxwell component and the independent R1 acceptance."""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(ROOT/'work/memoria_missao_20261016'))
import activate as a
a.ROOT = OUT/'mission_resume_20261016'
reg.DEST = OUT
MARKER = 'fecho_null_frequency_and_reuse_20261016_r36'


def main():
    assert not (OUT/'PROGRESS_R36.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    v = a.call('mission_cli.py', {'operation':'project','reference':str(a.REF),'max_chars':48000}, 'R36_BEFORE')
    t = next(x for x in v['projection']['active'] if x['id']=='R8')
    a.call('mission_cli.py', {'operation':'check','reference':str(a.REF),'actor':a.ACTOR,
        'task_id':'R8','lease_id':t['lease']['id'],'expected_revision':v['receipt']['revision'],
        'projection_sha256':v['projection_sha256']}, 'R36_PREFLIGHT')
    attempt = OUT/'orbital_rotation/attempts/20261016T123047_944060Z'
    build = json.loads((attempt/'RECEIPT.json').read_bytes())
    assert build['exit_code'] == 0 and build['readonly_dependencies_unchanged']
    checked = {}
    for item in [build['source']] + build['dependencies'] + build['artifacts']:
        path = Path(item['path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], path
        checked[str(path)] = item['sha256']
    raw = (attempt/'AXIOMS.txt').read_text(encoding='utf-8')
    axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", raw)
    assert len(axioms) == 6
    for name, names in axioms:
        assert set(x.strip() for x in names.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'}, name
    source = Path(build['source']['path']).read_text(encoding='utf-8')
    assert not re.search(r'\bsorry\b|^axiom\b', source, re.M)
    assert {'M0_MEMORIA','R1','R2','R9'} <= {x['id'] for x in v['projection']['settled']}
    review = OUT/'mission_review_20261016/R1_REQUIREMENT_REVIEW.json'
    accept = OUT/'mission_review_20261016/R1_ACCEPT_RECEIPT.json'
    provenance = json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    assert pin(Path(provenance['program_path']))['sha256'] == provenance['program_sha256']
    assert pin(Path(provenance['seal_path']))['sha256'] == provenance['seal_sha256']
    claims = {
        'component': 'NullFrequencyCoordinatesR3 compilou: coordenada nula positiva, inversa longitudinal e identidade exata da medida du/u. Corrigida apenas a ambiguidade lexical de 0<inverseEnergy da fonte anterior; nenhuma hipótese de carga acrescentada.',
        'verification': f'EXIT 0; seis declarações impressas apenas no trio; {len(checked)} arquivos conferidos por SHA256; {build["seconds"]:.3f}s. Sem sorry. Verificação local do recibo, não recompilação independente.',
        'poda': 'R1 aceito pelo revisor independente codex-mission-memory-review, revisão 21, após 693 arquivos/38 âncoras. M0/R1/R2/R9 saem do trabalho ativo. Não equivale a fecho científico da unidade do quadro.',
        'scope': 'R8 permanece working: este componente não prova a identidade da carga nula com o gerador modular nem habita o MaxwellCertificate. R4/R5/R6/R7/R8/R3/R10 preservam seus critérios; H3 universal segue antecedente nomeado. Builds R6, R7 e stress-boost R8 conservam suas identidades e serão recolhidos sem repetir.',
        'basis': 'Base v393 conferida por bytes; V351 é módulo histórico reaproveitado; v394 candidata só em sandbox. Produção, dado observado e gate intactos.'}
    progress = dict(unit='F1.FECHO_20261015',author=WHO,created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_SCOPE_PRESERVED',claim=claim,mission_reference=str(a.REF),
        mission_revision=v['receipt']['revision'],claims=claims,build=pin(attempt/'RECEIPT.json'),
        source=pin(Path(build['source']['path'])),axioms=dict(axioms),
        checked_files=[{'path':p,'sha256':h} for p,h in checked.items()],
        review=[pin(review),pin(accept)],source_history=[pin(a.ROOT/'R8_SOURCE_REUSE_R1.json'),
        pin(a.ROOT/'R8_NULL_LEXICAL_CORRECTION_R1.json')],whole_certificate_inhabited=False,
        production_modified=False,new_provider_calls=0,gate_moved=False)
    new(OUT/'PROGRESS_R36.json',progress)
    text = '\n\n## 16/10/2026 — Coordenada nula e reaproveitamento aceito\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob reivindicação vigente da F1.FECHO_20261015.\n'
    for label, body in claims.items():
        text += f'\n[{"OPEN" if label=="scope" else "REAL"} — {label}] {body}\n'
    text += f'\nEvidência: `{OUT/"PROGRESS_R36.json"}`; SHA256 `{pin(OUT/"PROGRESS_R36.json")["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R36.txt',text)
    memories = [append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R36.json',dict(unit=progress['unit'],claim=claim,surfaces=memories,evidence=pin(OUT/'PROGRESS_R36.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R36.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='Coordenada nula compilada e R1 aceito por revisão independente',
        resultado=' '.join(claims.values()),estatuto='REAL — componente; EM_CURSO — conjunto',status='EM_CURSO',
        veredito='NULL_COORDINATE_COMPILED_REUSE_ACCEPTED_FULL_SCOPE_PRESERVED',
        defeito='Carga de Maxwell e certificado conjunto permanecem abertos.',
        proximo_passo='Recolher os builds já iniciados, avançar resíduos do mesmo contrato.',onde=str(OUT),
        artefatos=[str(OUT/'PROGRESS_R36.json'),str(OUT/'MEMORY_PROGRESS_R36.json')],olhou_dados=False))
    v = a.call('mission_cli.py',{'operation':'project','reference':str(a.REF),'max_chars':48000},'R36_CURRENT')
    handles = list(v['projection']['flow']['handles'])
    h = next(h for h in handles if h['id']=='build-20261016T123047_944060Z')
    h.update(status='completed',receipt=str(attempt/'RECEIPT.json'))
    a.call('session_memory.py',dict(operation='transition',reference=str(a.REF),expected_revision=v['receipt']['revision'],
        event_id=MARKER,actor=a.ACTOR,changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
        text=' '.join(claims.values()),sources=[a.source(OUT/'PROGRESS_R36.json')])],flow=dict(
        phase='maxwell_null_coordinate_compiled',next_action='Recolher builds R6/R7/R8 existentes; R1/R2/R9 aceitos: não refazer. Completar carga/traço/dispositivo e rito conjunto.',handles=handles))), 'R36_TRANSITION')
    mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_PROGRESS_R36.json','--quem',WHO], 'MAP_RECEIPT_PROGRESS_R36.json')
    board = reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',OUT/'PROGRESS_R36.json','--evidencia',OUT/'MEMORY_PROGRESS_R36.json','--evidencia',review,'--nota','R36: coordenada nula compilada e R1 aceito; contrato integral e processos existentes preservados.'], 'BOARD_PROGRESS_R36.json')
    print(json.dumps({'progress':pin(OUT/'PROGRESS_R36.json'),'verified_files':len(checked),'map':mapped,'board':board},ensure_ascii=False))


if __name__=='__main__':
    main()
