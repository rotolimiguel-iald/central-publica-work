"""Register verified Bochner progress and the recovered mission, additively."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
from custody_fock_stress_r37 import verify
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MEM = ROOT/'work/memoria_missao_20261016'
sys.path.insert(0, str(OUT/'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'fecho_bochner_and_mission_recovery_20261016_r40'


def main():
    assert not (OUT/'PROGRESS_R40.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, _ = live.project()
    for task_id in ['R7', 'R8']:
        task = next(t for t in current['projection']['active'] if t['id'] == task_id)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=task_id, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R40_REGISTER_'+task_id)
    build = verify('20261016T144537_890350Z', 10)
    review_path = OUT/'mission_review_20261016/R8_BOCHNER_REVIEW_R1.json'
    review = json.loads(review_path.read_bytes())
    assert 'PASS_COMPONENT_WITH_SCOPE' in json.dumps(review)
    custody = OUT/'maxwell_global/NULL_FREQUENCY_BOCHNER_CUSTODY_R40.json'
    new(custody, dict(author=WHO, at=dt.datetime.now(dt.timezone.utc).isoformat(),
        build=build, independent_review=pin(review_path), independent_rebuild=False,
        scope='Bochner change of variables and null-frequency cancellation. Charge identity and complete Maxwell certificate remain open.'))
    wave_build = verify('20261016T145804_511128Z', 11)
    wave_review = OUT/'mission_review_20261016/R8_NULL_WAVE_REVIEW_R1.json'
    assert 'PASS' in json.dumps(json.loads(wave_review.read_bytes()))
    wave_custody = OUT/'maxwell_global/MAXWELL_NULL_WAVE_CUSTODY_R40.json'
    new(wave_custody,dict(author=WHO,build=wave_build,independent_review=pin(wave_review),
        independent_rebuild=False,scope='Actual regular Maxwell wave on null plane and its integrability. Charge and modular energy remain open.'))
    expected = {x['target']:x['new_sha256'] for x in json.loads((MEM/'DEPLOYMENT.json').read_bytes())['files']}
    expected.update({x['target']:x['new_sha256'] for x in json.loads((MEM/'handoff_capacity_e1/DEPLOYMENT_E1.json').read_bytes())['files']})
    installed = []
    for path, sha in expected.items():
        actual = pin(path)
        assert actual['sha256'] == sha, path
        installed.append(actual)
    memory_check = OUT/'mission_resume_20261016/INSTALLED_MEMORY_RECHECK_R40.json'
    new(memory_check, dict(at=dt.datetime.now(dt.timezone.utc).isoformat(), files=installed,
        all_match=True, tests_repeated=False, processes_restarted=False,
        scope='Current bytes match the already reviewed deployment plus E1. Legacy clients still require protocol consumption or reload.'))
    evidence = [custody, review_path, wave_custody, wave_review, memory_check, MEM/'FINAL_RECEIPT.json',
        MEM/'handoff_capacity_e1/FINAL_E1.json',
        OUT/'mission_resume_20261016/R4_ORDER_TERMINATION_R40.json',
        OUT/'mission_resume_20261016/BALANCE_R2_TERMINATION_R40.json',
        OUT/'orbital_rotation/attempts/20261016T144323_265660Z/RECEIPT.json',
        OUT/'orbital_rotation/attempts/20261016T143815_445332Z/RECEIPT.json',
        OUT/'orbital_rotation/attempts/20261016T144438_506902Z/RECEIPT.json',
        OUT/'orbital_rotation/attempts/20261016T145653_217589Z/RECEIPT.json',
        OUT/'orbital_rotation/attempts/20261016T145606_040004Z/RECEIPT.json',
        OUT/'mission_review_20261016/R7_PERTURBED_WEIGHT_ORDER_R5_CANDIDATE.json',
        OUT/'mission_review_20261016/R7_BALANCE_R3_INSTRUMENTATION.json',
        OUT/'maxwell_global/MAXWELL_NULL_PLANE_WAVE_CANDIDATE_R1.json']
    evidence.extend(Path(p) for p in sys.argv[1:])
    claims = {
        'bochner': ('REAL', 'NullFrequencyBochnerR2 recompilou com EXIT0 em 45,909s; dez declarações impressas somente no trio. Prova a mudança de medida de Bochner dp/E para du/u e o cancelamento do fator nulo na medida orbital efetiva. Revisão independente PASS_COMPONENT_WITH_SCOPE; sem segunda compilação independente.'),
        'wave': ('REAL', 'MaxwellNullPlaneWaveR2 compilou EXIT0 em 84,497s, onze declarações somente no trio. A contração da onda Maxwell regular ganha a representação de Fourier angular em frequência nula positiva; a integrabilidade é derivada do RegularProfile existente, incluindo a projeção real. R1 falhou apenas pelo uso de lambda reservado como nome; R2 mudou o nome para ell. Revisão independente do componente por recibo, sem segunda compilação.'),
        'limits': ('OPEN', 'O transporte e a onda não são a identidade carga/energia. R8 conserva Parseval ponderado para o perfil, ligação ao gerador, energia modular não nula e fonte geométrica. O MaxwellCertificate completo não foi habitado por esses dois componentes.'),
        'r7': ('REAL', 'A tentativa de norma/ordem R4 foi encerrada em 632,679s; BalanceR2 em 665,504s, com PID/comando e recibos preservados. R5 instrumentada terminou EXIT1 em 133,698s: timeout de conversão na linha86 e na monotonicidade. Nenhuma é prova aceita. BalanceR3 é candidata instrumentada, ainda sem execução. R7 integral, traço e PF, permanece aberto.'),
        'memory': ('REAL', 'Recuperação pela referência exata em processo novo: revisão 79 na retomada, seis requisitos satisfeitos fora da fila ativa. Os oito arquivos de controlador/CLI/MCP/protocolo/instruções foram rechecados contra implantação mais E1, todos idênticos. Transições posteriores preservam os handles em andamento e terminais. Nenhum requisito original R1-R10 foi reduzido.'),
        'memory_scope': ('REAL', 'M0_MEMORIA e M1_HANDOFF_CAPACITY já têm aceite técnico independente e não foram reconstruídos. Código e testes existentes implementam revisão, pinos, CAS, devolução como candidato e PODA; não há alegação de memória infalível nem Lindblad nos pesos. Processos antigos precisam consumir o protocolo ou recarregar o MCP. Não se mediu economia global de tokens.'),
        'remaining': ('OPEN', 'R3/R4/R5/R7/R8/R10 preservados: rito integral, identificação física/relógio, realização conjunta, traço/PF, Maxwell completo e revisão conjunta. Dois jobs awaiting_dispatch não foram repetidos; sua disposição continua pendente.'),
        'scope': ('REAL', 'Base v393 preservada; V351 é linhagem de módulos reaproveitados, v394 candidata. Nenhum original científico, kernel do Nós, Bancada produtiva, dado observado ou gate foi alterado. Nenhum provedor foi chamado.')}
    current, project_receipt = live.project()
    progress = dict(unit='F1.FECHO_20261015', author=WHO,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), status='EM_CURSO_FULL_SCOPE_PRESERVED',
        claim=claim, reference=str(live.REFERENCE), revision=current['receipt']['revision'],
        claims={k:dict(statute=v[0],text=v[1]) for k,v in claims.items()},
        artifacts=[pin(p) for p in evidence], project_receipt=pin(project_receipt),
        settled=[t['id'] for t in current['projection']['settled']],
        unresolved_handles=current['projection']['unresolved_handles'])
    new(OUT/'PROGRESS_R40.json', progress)
    text = '\n\n## 16/10/2026 — Transporte Bochner e retomada da missão ancorada\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob a reivindicação vigente da F1.FECHO_20261015.\n'
    for label,(statute,body) in claims.items():
        text += f'\n[{statute} — {label}] {body}\n'
    text += f'\nEvidência: `{OUT/"PROGRESS_R40.json"}`; SHA256 `{pin(OUT/"PROGRESS_R40.json")["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R40.txt', text)
    memory = [append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R40.json',dict(claim=claim,surfaces=memory,evidence=pin(OUT/'PROGRESS_R40.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R40.json',dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics',dominio='FORMAL',
        titulo='Transporte Bochner e onda Maxwell compilados; missão recuperada com revisão',
        resultado=' '.join(v[1] for v in claims.values()),estatuto='REAL — componente; OPEN — conjunto',
        status='EM_CURSO',veredito='BOCHNER_AND_NULL_WAVE_COMPILED_MISSION_ANCHOR_RECOVERED',
        defeito=claims['remaining'][1],proximo_passo='Onda Maxwell e balanço do traço, preservando revisão e todos os requisitos.',
        onde=str(OUT),artefatos=[str(OUT/'PROGRESS_R40.json'),str(OUT/'MEMORY_PROGRESS_R40.json')],olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_PROGRESS_R40.json','--quem',WHO],'MAP_RECEIPT_PROGRESS_R40.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',
        OUT/'PROGRESS_R40.json',OUT/'MEMORY_PROGRESS_R40.json','--nota',
        'R40: Bochner compilado/revisado; memória recuperada e instalação conferida; critérios integrais preservados.'],'BOARD_PROGRESS_R40.json')
    current,_ = live.project()
    flow = dict(current['projection']['flow'])
    flow.update(phase='bochner_compiled_actual_wave_and_balance_pending',
        next_action='Recuperar os builds exatos antes de outra tentativa; concluir carga/energia e traço/PF; preservar R4/R5 e rito R3/R10. M0/M1 aceitos, não reconstruir.')
    result,receipt = live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),
        actor=live.ACTOR,expected_revision=current['receipt']['revision'],event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',text='Bochner R2 compilado/revisado; memória instalada e retomada conferidas. Critérios integrais e limites no PROGRESS_R40.',
            sources=[dict(kind='artifact',ref=str(OUT/'PROGRESS_R40.json'),sha256=pin(OUT/'PROGRESS_R40.json')['sha256'])])],flow=flow)), 'R40_TRANSITION')
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R40.json'),memory=pin(OUT/'MEMORY_PROGRESS_R40.json'),receipt=str(receipt)),ensure_ascii=False))


if __name__ == '__main__':
    main()
