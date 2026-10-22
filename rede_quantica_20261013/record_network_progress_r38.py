"""Register measured Maxwell progress and failed Takesaki diagnostics additively."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(ROOT/'work/memoria_missao_20261016'))
import activate as a
a.ROOT = OUT/'mission_resume_20261016'
reg.DEST = OUT
MARKER = 'fecho_maxwell_quadratic_20261016_r38'


def main():
    assert not (OUT/'PROGRESS_R38.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%H%M%S_%f')
    v = a.call('mission_cli.py', dict(operation='project', reference=str(a.REF),
        max_chars=100000), 'R38_REGISTER_BEFORE_'+stamp)
    task = next(t for t in v['projection']['active'] if t['id']=='R8')
    a.call('mission_cli.py', dict(operation='check', reference=str(a.REF), actor=a.ACTOR,
        task_id='R8', lease_id=task['lease']['id'], expected_revision=v['receipt']['revision'],
        projection_sha256=v['projection_sha256']), 'R38_REGISTER_PREFLIGHT_'+stamp)
    delivery = OUT/'maxwell_global/REGULAR_MAXWELL_QUADRATIC_DELIVERY_R2.json'
    review = OUT/'mission_review_20261016/R8_REAL_QUADRATIC_REVIEW_R2.json'
    assert review.exists()
    checked = {}
    for build in json.loads(delivery.read_bytes())['builds']:
        for item in build['checked_files']:
            assert pin(item['path'])['sha256'] == item['sha256'], item['path']
            checked[item['path']] = item['sha256']
    attempts = OUT/'orbital_rotation/attempts'
    evidence = [delivery, review,
        OUT/'mission_review_20261016/R8_REAL_QUADRATIC_REVIEW_R1.json',
        OUT/'mission_review_20261016/R7_R11_COST_FOLLOWUP_R1.json',
        a.ROOT/'R38D_PROCESS_CORRECTION.json', a.ROOT/'R7_R11_TERMINATION_ACTION_R1.json',
        ROOT/'work/memoria_missao_20261016/FINAL_RECEIPT.json',
        ROOT/'work/memoria_missao_20261016/handoff_capacity_e1/FINAL_E1.json']
    for ident in ['20261016T125716_070120Z', '20261016T133508_005370Z',
                  '20261016T134128_460539Z', '20261016T134248_159556Z',
                  '20261016T134459_781070Z']:
        evidence.append(attempts/ident/'RECEIPT.json')
    provenance = json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    for key in ['program','seal']:
        assert pin(provenance[key+'_path'])['sha256'] == provenance[key+'_sha256']
    claims = {
        'maxwell': 'RegularFockRealCoordinateStressR2 e RegularFockMaxwellQuadraticR2 compilaram com EXIT0 em 74,644s e 75,639s; nove declarações impressas em cada pedra, somente no trio, zero sorry. Conservação fraca real no volume de Fin4→R, simetria, vácuo, translação e boost estão ligados ao MaxwellQuadraticForm existente no domínio regular de Fock.',
        'review': 'Revisão independente R2 PASS_DELTA_WITH_SCOPE: a correção foi somente a coerção explícita do domínio Submodule para Set; 956 pinos e 237 cópias de dependências conferidos. Nenhum aceite do requisito integral R8.',
        'scope': 'A construção é parametrizada por RemainingModularCoreInput A: as 21 obrigações de traço/PF permanecem. A carga no plano nulo, a energia modular não nula e a ligação à fonte geométrica ainda não foram fornecidas. O testemunho pontual não substitui o de energia modular. H3 universal permanece antecedente explícito.',
        'takesaki': 'R11 foi encerrada após 2378,245s com exit 4294967295. Sondas separadas mostraram que membership e a aplicação de scalarRightAction_cfc passam no trio. A conversão seguinte falha: R2 por inferência de predicado CFC e R3 por timeout de 600000 heartbeats em rw [regularSineWindow_val]. R3 terminou exit1 em 107,779s; nenhuma conclusão que depende dessa igualdade foi promovida.',
        'process': 'R38D_PROCESS_CORRECTION registra que um nome de recibo reutilizado recuperou snapshot antigo e a falha Python não interrompeu o PowerShell antes de Stop-Process. A parada conferiu PID/comando exatos, mas não teve novo preflight válido. A correção preserva esse fato: nomes únicos por leitura e verificação explícita de LASTEXITCODE antes de ação dependente.',
        'memory': 'M0_MEMORIA e M1_HANDOFF_CAPACITY seguem satisfeitos. Mesma inscrição, critérios R1–R10 e handles preservados. Código, CLI, MCP e instruções globais instalados; oito alvos atuais conferidos. Repasse admite capacidade explícita sem truncamento. Processos antigos não foram recarregados; sincronização depende de adesão ao protocolo.',
        'next': 'Continuar apenas os resíduos R7/R8 e a identificação física R4/R5; rito integral R3 e revisão conjunta R10 dependem deles. R1/R2/R6/R9 não são reconstruídos. Dois pedidos remotos mantêm identidades e não foram reenviados.',
        'basis': 'Programa e selo v393 reconferidos por bytes; V351 nomeia módulos históricos reaproveitados. v394 permanece candidata de sandbox. Nenhum programa canônico, kernel do Nós, Bancada produtiva, dado observado ou gate alterado.'
    }
    progress = dict(unit='F1.FECHO_20261015', author=WHO,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_SCOPE_PRESERVED', claim=claim,
        mission_reference=str(a.REF), mission_revision=v['receipt']['revision'],
        claims=claims, artifacts=[pin(p) for p in evidence], checked_file_count=len(checked),
        settled=[x['id'] for x in v['projection']['settled']],
        unresolved_handles=v['projection']['unresolved_handles'],
        prior_index_query='NOS_VIVO reported unit absent from its current graph; live board and pinned R37/R38 artifacts were used. This is stale indexing, not absence of prior work.',
        production_modified=False, new_provider_calls=0, gate_moved=False)
    new(OUT/'PROGRESS_R38.json', progress)
    text = '\n\n## 16/10/2026 — Contrato quadrático de Maxwell e sincronização aplicada\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob reivindicação vigente da F1.FECHO_20261015.\n'
    for key, body in claims.items():
        label = 'OPEN' if key in {'scope','next'} else 'REAL'
        text += f'\n[{label} — {key}] {body}\n'
    text += f'\nEvidência: `{OUT/"PROGRESS_R38.json"}`; SHA256 `{pin(OUT/"PROGRESS_R38.json")["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R38.txt', text)
    memory = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R38.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memory, evidence=pin(OUT/'PROGRESS_R38.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R38.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='MaxwellQuadraticForm concreto; traço e carga seguem abertos',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; OPEN — conjunto',
        status='EM_CURSO', veredito='MAXWELL_QUADRATIC_COMPILED_FULL_R8_OPEN',
        defeito='R7 igualdade CFC ainda falha; R8 sem carga modular e sem habitante do core A.',
        proximo_passo='Reutilizar componentes compilados e resolver resíduos tipados com memória vigente.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R38.json'),str(OUT/'MEMORY_PROGRESS_R38.json')],
        olhou_dados=False))
    mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar',
        OUT/'MAP_ENTRY_PROGRESS_R38.json','--quem', WHO], 'MAP_RECEIPT_PROGRESS_R38.json')
    board = reg.call([CLI, 'avancar', 'F1.FECHO_20261015', '--quem', WHO, '--status', 'EM_CURSO',
        '--evidencia', OUT/'PROGRESS_R38.json', OUT/'MEMORY_PROGRESS_R38.json',
        '--nota', 'R38: MaxwellQuadraticForm compilado/revisado; falhas Takesaki custodiadas; missão integral preservada.'],
        'BOARD_PROGRESS_R38.json')
    v = a.call('mission_cli.py', dict(operation='project', reference=str(a.REF),
        max_chars=100000), 'R38_REGISTER_CURRENT_'+stamp)
    flow = dict(v['projection']['flow'])
    flow.update(phase='maxwell_quadratic_integrated_remaining_contract',
        next_action='Resolver transporte CFC R7 sem repetir builds terminais; completar carga/energia R8 e identificação R4/R5; rito integral R3/R10 após isso.')
    transition = a.call('session_memory.py', dict(operation='transition', reference=str(a.REF),
        actor=a.ACTOR, expected_revision=v['receipt']['revision'], event_id=MARKER,
        changes=dict(records=[dict(id=MARKER, kind='fact', statute='REAL',
            text=' '.join(claims.values()), sources=[a.source(OUT/'PROGRESS_R38.json')])],
            flow=flow)), 'R38_REGISTER_TRANSITION_'+stamp)
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R38.json'),checked_files=len(checked),
        map_receipt=str(OUT/'MAP_RECEIPT_PROGRESS_R38.json'),
        board_receipt=str(OUT/'BOARD_PROGRESS_R38.json'),
        revision=transition.get('revision')), ensure_ascii=False))


if __name__=='__main__':
    main()
