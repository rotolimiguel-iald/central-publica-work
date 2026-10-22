"""Custody measured components and append one synchronized progress record."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
from custody_fock_stress_r37 import verify
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT/'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'fecho_actual_cutoffs_and_calibration_20261016_r39'


def main():
    assert not (OUT/'PROGRESS_R39.json').exists()
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
            projection_sha256=current['projection_sha256']), 'R39_REGISTER_'+task_id)
    builds = [verify(ident, count) for ident, count in [
        ('20261016T140448_960256Z', 4), ('20261016T141848_714344Z', 7),
        ('20261016T142035_518658Z', 3), ('20261016T141540_391938Z', 7)]]
    custody_path = OUT/'gns_coefficient_tomita/ACTUAL_CUTOFFS_CUSTODY_R39.json'
    new(custody_path, dict(author=WHO, created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        builds=builds[:3], scope='Compiled cutoffs and their specialization to the actual polar. Full trace/PF remain open.',
        independent_rebuild=False, production_modified=False))
    evidence = [custody_path,
        OUT/'mission_review_20261016/R7_CFC_INSTANCE_SCOPE_DIAGNOSIS_R1.json',
        OUT/'mission_review_20261016/R7_MODULAR_BALANCE_HYPOTHESIS_MAP_R1.json',
        OUT/'mission_review_20261016/R8_CHARGE_ENERGY_NEXT_STEP_R1.json',
        OUT/'mission_review_20261016/R8_CALIBRATED_ROOT_REVIEW_R1.json',
        OUT/'maxwell_global/REGULAR_MAXWELL_CALIBRATED_DELIVERY_R1.json',
        OUT/'mission_resume_20261016/live_mission_r39.py',
        OUT/'mission_resume_20261016/R12_TERMINATION_R39.json',
        OUT/'orbital_rotation/attempts/20261016T140728_293277Z/RECEIPT.json',
        OUT/'orbital_rotation/attempts/20261016T141957_101316Z/RECEIPT.json',
        OUT/'orbital_rotation/attempts/20261016T142257_025756Z/RECEIPT.json']
    # Additional actual review artifacts may be supplied by exact path after return.
    evidence.extend(Path(p) for p in sys.argv[1:])
    provenance = json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    for key in ['program', 'seal']:
        assert pin(provenance[key+'_path'])['sha256'] == provenance[key+'_sha256']
    claims = {
        'takesaki': ('REAL', 'A igualdade CFC R5 compilou em 84,876s com quatro declarações impressas. R13 isolou os cortes espectrais e suas raízes: EXIT0 em 79,373s, sete declarações. ActualRightCutoffsR2 ligou-os ao scalarTomitaPolarFactor existente, consumindo scalarPolarRightAlgebra_regular_mem: EXIT0 em 81,745s, três declarações. Todos os axiomas impressos ficam no trio; sem nova hipótese de ação à direita.'),
        'maxwell': ('REAL', 'RegularFockMaxwellCalibratedR1 compila em 74,986s, sete declarações no trio. Transporta o MaxwellQuadraticForm por fator positivo (2π)^(-3), preservando domínio e leis. Revisão independente do coordenador, distinto do construtor, conferiu 960 pinos e o alcance; não houve segunda compilação independente.'),
        'calibration_scope': ('DERIVED', 'A escolha do fator é a calibração analítica proposta para a convenção de Fourier angular. O teorema compilado prova transporte por escala constante, não a identidade completa entre carga e energia. Positividade pontual do tensor não prova energia modular não nula.'),
        'reuse': ('REAL', 'O mapa focal encontrou a implementação modular Δ^it=L(t)R(-t) no mesmo GNS em CanonicalFockModularIdentificationR17 e CanonicalFockConjugationActionR3. Quatorze recibos existentes foram conferidos pelo revisor. O consumidor de balanço é candidato até sua própria compilação; não reconstruir a implementação existente.'),
        'scope': ('OPEN', 'R7 conserva as 21 obrigações de traço/PF; R8 conserva carga no domínio integral, energia modular não nula e ligação à fonte geométrica. R4/R5 ainda exigem identificação física do dispositivo e relógio; R3/R10 dependem da integração conjunta. R1/R2/R6/R9 e os dois requisitos de memória permanecem satisfeitos.'),
        'process': ('REAL', 'R12 foi encerrada após 647,126s na fase de comutação, com preflight fresco e PID/comando conferidos; recibo terminal preservado. A versão curta R2 de comutação falhou por imports/inferência; R3 falhou em 119,833s no transporte da representação/inferência de tipos. Um pedido indevido de registrar completed foi recusado pelo tracker antes da mutação; o estado correto failed foi registrado. Nenhuma dessas tentativas é prova. O balanço usa a comutação regular já compilada, independente dessas tentativas.'),
        'memory': ('REAL', 'live_mission_r39.py cria recibo único a cada leitura, nunca recuperando consulta antiga como estado vigente. As devoluções foram reconciliadas com a referência exata e a revisão atual. O código de memória/CLI/MCP/instruções já entregue permanece; processos antigos requerem adesão/recarga. Não há promessa de memória infalível ou execução de Lindblad nos pesos.'),
        'basis': ('REAL', 'Programa e selo v393 foram reconferidos por bytes. V351 é a linhagem de módulos reaproveitados; v394 segue candidata. Nenhum original científico, kernel do Nós, Bancada produtiva, dado observado ou gate foi alterado; nenhum provedor foi chamado.')
    }
    current, _ = live.project()
    progress = dict(unit='F1.FECHO_20261015', author=WHO,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(), status='EM_CURSO_FULL_SCOPE_PRESERVED',
        claim=claim, mission_reference=str(live.REFERENCE), revision=current['receipt']['revision'],
        claims={k: dict(statute=v[0], text=v[1]) for k, v in claims.items()},
        artifacts=[pin(p) for p in evidence],
        settled=[t['id'] for t in current['projection']['settled']],
        unresolved_handles=current['projection']['unresolved_handles'],
        production_modified=False, gate_moved=False, provider_calls=0)
    new(OUT/'PROGRESS_R39.json', progress)
    text = '\n\n## 16/10/2026 — Cortes polares concretos, calibração e memória sincronizada\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob a reivindicação vigente da F1.FECHO_20261015.\n'
    for label, (statute, body) in claims.items():
        text += f'\n[{statute} — {label}] {body}\n'
    text += f'\nEvidência: `{OUT/"PROGRESS_R39.json"}`; SHA256 `{pin(OUT/"PROGRESS_R39.json")["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R39.txt', text)
    memory = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R39.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memory, evidence=pin(OUT/'PROGRESS_R39.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R39.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Cortes ligados ao polar concreto e forma de Maxwell calibrada',
        resultado=' '.join(v[1] for v in claims.values()), estatuto='REAL — componentes; OPEN — conjunto',
        status='EM_CURSO', veredito='ACTUAL_POLAR_CUTOFFS_AND_SCALED_MAXWELL_COMPILED',
        defeito=claims['scope'][1], proximo_passo='Balanço do traço e identidade da carga, com reuso e revisão vigente.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R39.json'),str(OUT/'MEMORY_PROGRESS_R39.json')],
        olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar',
        OUT/'MAP_ENTRY_PROGRESS_R39.json', '--quem', WHO], 'MAP_RECEIPT_PROGRESS_R39.json')
    reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
        '--evidencia', OUT/'PROGRESS_R39.json', OUT/'MEMORY_PROGRESS_R39.json',
        '--nota', 'R39: cortes ligados ao polar real e Maxwell calibrado; memória sincronizada; critério integral preservado.'],
        'BOARD_PROGRESS_R39.json')
    current, _ = live.project()
    flow = dict(current['projection']['flow'])
    flow.update(phase='actual_polar_cutoffs_and_calibrated_maxwell',
        next_action='Reutilizar cortes concretos e implementação modular para o balanço; provar carga/energia calibrada; preservar R4/R5 e rito R3/R10. Não repetir handles pendentes.')
    result, receipt = live.call('session_memory.py', dict(operation='transition',
        reference=str(live.REFERENCE), actor=live.ACTOR, expected_revision=current['receipt']['revision'],
        event_id=MARKER, changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text='Componentes compilados e alcance aberto discriminados no PROGRESS_R39; a inscrição e todos os critérios permanecem.',
            sources=[dict(kind='artifact',ref=str(OUT/'PROGRESS_R39.json'),
                sha256=pin(OUT/'PROGRESS_R39.json')['sha256'])])], flow=flow)), 'R39_REGISTER_TRANSITION')
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R39.json'),
        memory=pin(OUT/'MEMORY_PROGRESS_R39.json'), revision=result.get('revision'), receipt=str(receipt)), ensure_ascii=False))


if __name__ == '__main__':
    main()
