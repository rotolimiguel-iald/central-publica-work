"""Custody the global net, independent source review, and current mission state."""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MEM = ROOT/'work/memoria_missao_20261016'
sys.path.insert(0, str(MEM))
import activate as a
a.ROOT = OUT/'mission_resume_20261016'
reg.DEST = OUT
MARKER = 'fecho_global_maxwell_net_20261016_r35'


def main():
    assert not (OUT/'PROGRESS_R35.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    v = a.call('mission_cli.py', {'operation':'project','reference':str(a.REF),'max_chars':48000}, 'R35_BEFORE')
    t = next(x for x in v['projection']['active'] if x['id']=='R5')
    a.call('mission_cli.py', {'operation':'check','reference':str(a.REF),'actor':a.ACTOR,
        'task_id':'R5','lease_id':t['lease']['id'],'expected_revision':v['receipt']['revision'],
        'projection_sha256':v['projection_sha256']}, 'R35_PREFLIGHT')
    attempt = OUT/'orbital_rotation/attempts/20261016T120556_913253Z'
    build = json.loads((attempt/'RECEIPT.json').read_bytes())
    assert build['exit_code'] == 0 and build['readonly_dependencies_unchanged']
    checked = {}
    for item in [build['source']] + build['dependencies'] + build['artifacts']:
        path = Path(item['path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], path
        checked[str(path)] = item['sha256']
    raw = (attempt/'AXIOMS.txt').read_text(encoding='utf-8')
    axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", raw)
    assert len(axioms) == 11
    for name, names in axioms:
        assert set(x.strip() for x in names.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'}, name
    source = Path(build['source']['path']).read_text(encoding='utf-8')
    assert not re.search(r'\bsorry\b|^axiom\b', source, re.M)
    review = OUT/'mission_review_20261016/PHYSICAL_GLOBAL_NET_REVIEW_R1.json'
    reviews = [review, OUT/'mission_review_20261016/R2_REQUIREMENT_REVIEW.json',
               OUT/'mission_review_20261016/R9_REQUIREMENT_REVIEW.json']
    assert {'M0_MEMORIA','R2','R9'} <= {x['id'] for x in v['projection']['settled']}
    provenance = json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    assert pin(Path(provenance['program_path']))['sha256'] == provenance['program_sha256']
    assert pin(Path(provenance['seal_path']))['sha256'] == provenance['seal_sha256']
    claims = {
        'global_net': 'Construída a rede global de Maxwell livre em Minkowski por testes reais de suporte compacto. Localidade causal é derivada pelas cunhas opostas e cobertura finita; a rede possui monotonia e covariâncias já construídas. A cunha física coincide por termo com KWR, e a rede nula é recusada por um vetor não nulo.',
        'build': f'PhysicalCanonicalNetCompleteR1: EXIT 0, onze impressões apenas no trio; {len(checked)} arquivos relidos por SHA256. Tempo {build["seconds"]:.3f}s, dos quais o perfil registra 764s de importação. Nenhum sorry na fonte candidata.',
        'review': 'Revisão independente de fonte PASS, anterior ao término da compilação, sem recompilação independente. O resultado terminal foi conferido pela raiz. Os dois alcances permanecem separados.',
        'poda': 'Na missão ACOM vigente, M0_MEMORIA, R2 e R9 estão satisfied. R2/R9 foram aceitos pelo revisor real distinto nas revisões 16/17. História e evidências preservadas; não equivale a fechamento do quadro.',
        'scope': 'R5 completo continua aberto quanto à realização/identificação do dispositivo. R6 compila em tentativa própria, sem resultado ainda. Traço escalado/PF, vínculo da carga de Maxwell, identificação física do relógio, rito final e revisão conjunta permanecem abertos. H3 universal continua antecedente explícito.',
        'basis': 'Base científica v393 conferida novamente; v394 é candidata em sandbox. V351 nomeia módulos históricos presentes nessa base. Produção, dados observados e gate intactos.'}
    progress = dict(unit='F1.FECHO_20261015', author=WHO,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_SCOPE_PRESERVED', claim=claim,
        mission_reference=str(a.REF), mission_revision=v['receipt']['revision'],
        claims=claims, build=pin(attempt/'RECEIPT.json'),
        source=pin(Path(build['source']['path'])), axioms=dict(axioms),
        checked_files=[{'path':p,'sha256':h} for p,h in checked.items()],
        reviews=[pin(p) for p in reviews],
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
        whole_certificate_inhabited=False, production_modified=False,
        new_provider_calls=0, gate_moved=False)
    new(OUT/'PROGRESS_R35.json', progress)
    text = '\n\n## 16/10/2026 — Rede global de Maxwell e PODA da missão\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, unidade F1.FECHO_20261015, reivindicação vigente conferida.\n'
    for label, body in claims.items():
        tag = 'OPEN' if label=='scope' else 'REAL'
        text += f'\n[{tag} — {label}] {body}\n'
    text += f'\nEvidência: `{OUT/"PROGRESS_R35.json"}`; SHA256 `{pin(OUT/"PROGRESS_R35.json")["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R35.txt', text)
    memories = [append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R35.json',dict(unit=progress['unit'],claim=claim,surfaces=memories,evidence=pin(OUT/'PROGRESS_R35.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R35.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='Rede global de Maxwell: localidade, cunha não trivial e PODA da missão',
        resultado=' '.join(claims.values()),estatuto='REAL — componente; EM_CURSO — conjunto',status='EM_CURSO',
        veredito='GLOBAL_NET_COMPILED_FULL_SCOPE_PRESERVED',defeito='Realização do dispositivo e certificado conjunto ainda abertos.',
        proximo_passo='Recolher ligação Fock, completar traço/carga e executar candidata final.',onde=str(OUT),
        artefatos=[str(OUT/'PROGRESS_R35.json'),str(OUT/'MEMORY_PROGRESS_R35.json')],olhou_dados=False))
    # Refresh after external review; preserve all unrelated handles and records.
    v = a.call('mission_cli.py',{'operation':'project','reference':str(a.REF),'max_chars':48000},'R35_CURRENT')
    handles = list(v['projection']['flow']['handles'])
    for h in handles:
        if h['id']=='build-20261016T120556_913253Z':
            h.update(status='completed',receipt=str(attempt/'RECEIPT.json'))
    pending = OUT/'orbital_rotation/attempts/20261016T121945_659941Z/START_RECEIPT.json'
    start = json.loads(pending.read_bytes())
    handles.append(dict(id='build-20261016T121945_659941Z',name='PhysicalFockNetRealizationR1',
        no_repeat=True,pid_at_start=start['pid'],receipt=str(pending),status='running',
        type='lean_build',unit='F1.FECHO_20261015'))
    a.call('session_memory.py',dict(operation='transition',reference=str(a.REF),expected_revision=v['receipt']['revision'],
        event_id=MARKER,actor=a.ACTOR,changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text=' '.join(claims.values()),sources=[a.source(OUT/'PROGRESS_R35.json'),a.source(pending)])],
        flow=dict(phase='physical_global_net_compiled',next_action='Recolher R6 existente; R5 dispositivo, R7 traço/PF, R8 carga e R3/R10 seguem. R2/R9 aceitos: não refazer.',handles=handles))), 'R35_TRANSITION')
    print(json.dumps({'progress':pin(OUT/'PROGRESS_R35.json'),'memory_surfaces':len(memories),'verified_files':len(checked)},ensure_ascii=False))


if __name__=='__main__':
    main()
