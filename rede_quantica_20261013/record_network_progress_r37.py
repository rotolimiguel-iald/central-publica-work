"""Register R6 review and R8 boost component without reopening settled work."""
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
MARKER = 'fecho_fock_and_stress_20261016_r37'


def main():
    assert not (OUT/'PROGRESS_R37.json').exists()
    claim = reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    v = a.call('mission_cli.py',dict(operation='project',reference=str(a.REF),max_chars=60000),'R37_REGISTER_BEFORE')
    t = next(x for x in v['projection']['active'] if x['id']=='R8')
    a.call('mission_cli.py',dict(operation='check',reference=str(a.REF),actor=a.ACTOR,
        task_id='R8',lease_id=t['lease']['id'],expected_revision=v['receipt']['revision'],
        projection_sha256=v['projection_sha256']),'R37_REGISTER_PREFLIGHT')
    r6 = next(x for x in v['projection']['settled']+v['projection']['active'] if x['id']=='R6')
    evidence = [OUT/'orbital_rotation/PHYSICAL_FOCK_NET_DELIVERY_R2.json',
                OUT/'maxwell_global/REGULAR_STRESS_BOOST_DELIVERY_R3.json']
    checks = {}
    for file in evidence:
        data = json.loads(file.read_bytes())
        for p in data['build']['checked_files']:
            assert pin(Path(p['path']))['sha256']==p['sha256'], p['path']
            checks[p['path']] = p['sha256']
    evidence += [a.ROOT/'R7_R10_TERMINATION_RECEIPT.json',
        OUT/'mission_review_20261016/R7_COMPILE_COST_REVIEW_R1.json',
        OUT/'orbital_rotation/attempts/20261016T125716_070120Z/START_RECEIPT.json']
    reviewed = r6['status']=='satisfied'
    if reviewed:
        for p in r6['review_evidence']:
            assert pin(Path(p['path']))['sha256']==p['sha256']
            evidence.append(Path(p['path']))
    provenance = json.loads((OUT/'PROVENIENCIA_V393_REUSO_V351_R1.json').read_bytes())
    assert pin(Path(provenance['program_path']))['sha256']==provenance['program_sha256']
    assert pin(Path(provenance['seal_path']))['sha256']==provenance['seal_sha256']
    claims = {
        'fock': 'PhysicalFockNetRealizationR2 compilou em 83,191s: 16 declarações no trio, zero sorry. Weyl/CCR/R(K), vácuo cíclico e separante, não comutatividade, Gamma(J), Tomita e KMS estão ligados à mesma rede compacta de Maxwell e ao mesmo Fock.',
        'review': ('R6 aceito após revisão independente por '+r6['reviewed_by']+'. O aceite é do requisito R6; não fecha a missão nem o quadro.' if reviewed else 'R6 submetido, revisão independente ainda pendente; compilação sozinha não encerra o requisito.'),
        'stress': 'RegularFockStressBoostR3 compilou em 77,030s; duas declarações impressas somente no trio, zero sorry. A covariância do tensor de Maxwell por boost vale no mesmo domínio regular de Fock.',
        'cost': 'Builder compacto preserva os hashes e copia os .olean em um cache isolado, sem junção e sem alterar dependências. Nesta comparação de tentativas, import de R6 caiu de cerca de 1200s para 67,6s e de R8 de 633s para 65,6s. São tempos observados de tentativas, não benchmark controlado.',
        'remaining': 'R8 ainda exige carga modular normalizada e certificado conjunto. Em R7, a tentativa R10 foi encerrada após diagnóstico independente e verificação do PID, com exit 4294967295 e 7383,038s preservados; uma tentativa R11 separada foi iniciada com tipos explícitos e marcadores, sem duplicar processo. A causa da lentidão segue hipótese até o resultado. R4/R5 conservam a identificação física/dispositivo; R3 e R10 aguardam a composição final. H3 universal permanece antecedente explícito.',
        'memory': 'M0, R1, R2 e R9 permanecem aceitos. A revisão vigente e os handles foram recuperados da mesma inscrição; resultados terminais integrados por CAS. A aplicação usa estado discreto e prova de custódia, sem alegar Lindblad nos pesos ou memória infalível.',
        'basis': 'Programa e selo v393 reconferidos; V351 é módulo histórico reutilizado. v394 candidata em sandbox. Produção, dado observado, Bancada e gate intactos.'}
    progress = dict(unit='F1.FECHO_20261015',author=WHO,created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_SCOPE_PRESERVED',claim=claim,mission_reference=str(a.REF),
        mission_revision=v['receipt']['revision'],R6_status=r6['status'],claims=claims,
        artifacts=[pin(p) for p in evidence],checked_file_count=len(checks),
        settled=[x['id'] for x in v['projection']['settled']],
        unresolved_handles=v['projection']['unresolved_handles'],
        production_modified=False,new_provider_calls=0,gate_moved=False)
    new(OUT/'PROGRESS_R37.json',progress)
    text='\n\n## 16/10/2026 — Rede de Fock, tensor covariante e sincronização aplicada\n'
    text+=f'<!-- {MARKER} -->\nEm nome de {WHO}, sob reivindicação vigente da F1.FECHO_20261015.\n'
    for key,body in claims.items():
        text+=f'\n[{"OPEN" if key=="remaining" else "REAL"} — {key}] {body}\n'
    text+=f'\nEvidência: `{OUT/"PROGRESS_R37.json"}`; SHA256 `{pin(OUT/"PROGRESS_R37.json")["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R37.txt',text)
    memories=[append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R37.json',dict(unit=progress['unit'],claim=claim,surfaces=memories,evidence=pin(OUT/'PROGRESS_R37.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R37.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='Rede Fock concreta e tensor Maxwell covariante; memória sincronizada',
        resultado=' '.join(claims.values()),estatuto='REAL — componentes; EM_CURSO — conjunto',status='EM_CURSO',
        veredito='FOCK_AND_STRESS_COMPILED_FULL_SCOPE_PRESERVED',
        defeito='Carga, traço e identificação física do dispositivo ainda têm resíduos próprios.',
        proximo_passo='Completar somente resíduos vigentes, com preflight e revisão independente.',onde=str(OUT),
        artefatos=[str(OUT/'PROGRESS_R37.json'),str(OUT/'MEMORY_PROGRESS_R37.json')],olhou_dados=False))
    mapped=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_PROGRESS_R37.json','--quem',WHO],'MAP_RECEIPT_PROGRESS_R37.json')
    board=reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO',
        '--evidencia',OUT/'PROGRESS_R37.json',OUT/'MEMORY_PROGRESS_R37.json',
        '--nota','R37: rede Fock e stress-boost compilados; sincronização aplicada; resíduos integrais preservados.'],'BOARD_PROGRESS_R37.json')
    v=a.call('mission_cli.py',dict(operation='project',reference=str(a.REF),max_chars=60000),'R37_REGISTER_CURRENT')
    flow=dict(v['projection']['flow'])
    flow.update(phase='components_integrated_remaining_contract',next_action='Resolver R7 em voo sem repetir; concluir carga R8 e identificação R4/R5; composição e rito final R3/R10 após isso.')
    transition=a.call('session_memory.py',dict(operation='transition',reference=str(a.REF),actor=a.ACTOR,
        expected_revision=v['receipt']['revision'],event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',text=' '.join(claims.values()),
            sources=[a.source(OUT/'PROGRESS_R37.json')])],flow=flow)),'R37_REGISTER_TRANSITION')
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R37.json'),R6_status=r6['status'],
        checked_files=len(checks),map=mapped,board=board,revision=transition.get('revision')),ensure_ascii=False))


if __name__=='__main__':
    main()
