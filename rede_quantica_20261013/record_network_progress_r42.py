"""Record reviewed components against the unchanged mission, with byte custody."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MEM = ROOT / 'work/memoria_missao_20261016'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'reviewed_components_and_live_anchor_20261016_r42'


def main():
    target = OUT / 'PROGRESS_R42.json'
    if target.exists():
        raise RuntimeError('Immutable result exists; recover the existing registration')
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT / 'memory/DIARIO_CONSTRUCAO_QG.md', ROOT / 'memory/TGL_ATLAS.md',
                ROOT / 'memory/TGL_INDICE_VIVO.md', OUT.parent / 'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, project_receipt = live.project()
    for task_id in ['R5', 'R7', 'R8']:
        task = next(t for t in current['projection']['active'] if t['id'] == task_id)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=task_id, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R42_INTEGRATE_'+task_id)
    definitions = [
        ('R8', 'maxwell_global/MAXWELL_NULL_SCHWARTZ_CUSTODY_R42.json',
         'R8_NULL_SCHWARTZ_REVIEW_R1.json', '20261016T152225_637794Z', 11),
        ('R5', 'orbital_rotation/PHYSICAL_FOCK_COVARIANCE_CUSTODY_R42.json',
         'R5_FOCK_COVARIANCE_REVIEW_R1.json', '20261016T152639_956206Z', 9),
        ('R8', 'maxwell_global/NULL_SCHWARTZ_CORE_SEED_CUSTODY_R42.json',
         'R8_CORE_SEED_REVIEW_R1.json', '20261016T152905_920201Z', 3)]
    components = []
    for task_id, custody, review, attempt, count in definitions:
        rp = OUT/'mission_review_20261016'/review
        reviewed = json.loads(rp.read_bytes())
        assert reviewed['verdict'] == 'PASS_COMPONENT_WITH_SCOPE'
        assert reviewed['requirement_satisfied'] is False
        build = OUT/'orbital_rotation/attempts'/attempt/'RECEIPT.json'
        r = json.loads(build.read_bytes())
        assert type(r['exit_code']) is int and r['exit_code'] == 0
        assert r['readonly_dependencies_unchanged'] and r['dependency_cache_unchanged']
        source = r['source']
        assert pin(source['path'])['sha256'] == source['sha256']
        original = OUT / custody.split('/')[0] / Path(source['path']).name
        assert pin(original)['sha256'] == source['sha256']
        components.append(dict(task_id=task_id, requirement_satisfied=False, axiom_lists=count,
            source=source, original_source=pin(original), build=pin(build), custody=pin(OUT/custody), review=pin(rp),
            verdict=reviewed['verdict'], scope='Component only; unchanged full mission criterion'))
    expected = {x['target']: x['new_sha256'] for x in json.loads((MEM/'DEPLOYMENT.json').read_bytes())['files']}
    expected.update({x['target']:x['new_sha256'] for x in json.loads((MEM/'handoff_capacity_e1/DEPLOYMENT_E1.json').read_bytes())['files']})
    installed = [pin(p) for p in expected]
    assert all(p['sha256'] == expected[p['path']] for p in installed)
    attempt_ids = ['20261016T151949_128158Z','20261016T152433_858034Z',
                   '20261016T153113_490978Z','20261016T153924_574512Z','20261016T153954_162725Z']
    attempts = []
    for attempt in attempt_ids:
        receipt = OUT/'orbital_rotation/attempts'/attempt/'RECEIPT.json'
        if not receipt.exists():
            raise RuntimeError('A launched attempt is not terminal: '+attempt)
        r = json.loads(receipt.read_bytes())
        handle = next(h for h in current['projection']['flow']['handles'] if h['id']=='build-'+attempt)
        assert handle['status'] in ['completed','failed','terminated']
        assert (r['exit_code'] == 0) == (handle['status'] == 'completed')
        attempts.append(dict(id=attempt, status=handle['status'], exit_code=r['exit_code'],
            seconds=r['seconds'], receipt=pin(receipt)))
    evidence = [project_receipt,
        OUT/'maxwell_global/MAXWELL_NULL_SCHWARTZ_CORE_TRANSPORT_CANDIDATE_R1.json',
        OUT/'mission_review_20261016/R7_CONVERSION_BOUNDARY_PROBE_R2_CANDIDATE.json']
    evidence.extend(Path(p) for p in sys.argv[1:])
    claims = {
        'memory': ('REAL', 'Recuperada a referencia exata da missao apos compactacao: a projecao devolveu revisao104, seis requisitos satisfeitos, seis abertos e os mesmos dois jobs pendentes. Os oito alvos instalados, incluindo E1, conferem por SHA256. M0/M1 permanecem satisfeitos, sem reconstrucao.'),
        'r8_fourier': ('REAL', 'MaxwellNullSchwartzConsumerR2 compilou EXIT0 em80,358s: onze listas no trio. Sob NullSchwartzData explicita, identifica a onda existente com Fourier angular, prova Parseval ponderado misto complexo e a derivada pontual +u*d_u do representante sob B0. Revisao independente PASS_COMPONENT_WITH_SCOPE.'),
        'r5': ('REAL', 'PhysicalFockSpacetimeCovarianceR2 compilou EXIT0 em81,108s: nove listas no trio. A mesma rede Weyl/Fock tem covariancia por translacao, Lorentz e boosts, com identificacao da representacao de Poincare ja existente. Revisao independente PASS_COMPONENT_WITH_SCOPE. A realizacao do dispositivo continua aberta.'),
        'r8_seed': ('REAL', 'NullSchwartzCoreSeedR1 compilou EXIT0 em76,544s: tres listas no trio. A classe compacta afastada do eixo e densa, StrongRegular, pertence ao range de physicalSmearCLM e tem testemunha H1 nao nula. Isso ainda nao e habitante NullSchwartzData nem energia modular nao nula. Revisao independente PASS_COMPONENT_WITH_SCOPE.'),
        'r7_diagnostic': ('REAL', 'A sonda R1 terminou EXIT1 em106,403s: falhas concretas de inferencia do Hilbert/adjunto, sem teorema aceito. A frase historica que localizava BalanceR3 apenas na inferencia era forte demais: seu marcador tambem abrangia o rw seguinte. O novo diagnostico separa etapas; redundancia de instancia nao provou diamante inconsistente.'),
        'next_candidates': ('REAL', 'ConversionBoundaryProbeR2 terminou EXIT1 em117,536s: a tipagem de pi ainda nao sintetiza Star, causando erros dependentes de norma; nao ha prova aceita. MaxwellNullSchwartzCoreTransportR1 terminou EXIT1 em92,015s: faltam aplicacoes explicitas de Complex.ofReal/contDiff e PiLp.continuous_toLp/apply, e convert abriu igualdade de instancias. As conclusoes dessas duas candidatas permanecem DECLARADO; somente os tres componentes revisados sao integrados.'),
        'memory_limit': ('REAL', 'Revisao, lease, pinos, CAS, PODA e handles sao aplicados nas fronteiras de sincronizacao. Chamadas nativas de agentes nao sao interceptadas automaticamente: o coordenador precisa registrar o repasse e reconciliar a devolucao. Sessoes antigas usam CLI ou recarregam MCP. Nao se afirma Lindblad nos pesos, infalibilidade ou economia global de tokens medida.'),
        'remaining': ('OPEN', 'R3/R4/R5/R7/R8/R10 continuam integrais: rito v394, espectro/relogio do objeto fisico, realizacao do dispositivo, traco/PF da representacao pretendida, certificado Maxwell completo e revisao conjunta. Base v393; V351 e linhagem reutilizada. Nenhum provedor novo, original cientifico, Bancada, dado observado ou gate alterado.')}
    agents = [
        dict(id='/root/fock_r6_review',status='completed',task_id='R8',
             result=pin(OUT/'maxwell_global/MAXWELL_NULL_SCHWARTZ_CORE_TRANSPORT_CANDIDATE_R1.json')),
        dict(id='/root/mission_memory_review',status='completed',task_id='R7',
             result=pin(OUT/'mission_review_20261016/R7_CONVERSION_BOUNDARY_PROBE_R2_CANDIDATE.json')),
        dict(id='/root/maxwell_covariance_review',status='completed',task_id='R5/R8',
             results=[c['review'] for c in components])]
    progress = dict(unit='F1.FECHO_20261015', author=WHO, at=dt.datetime.now(dt.timezone.utc).isoformat(),
        reference=str(live.REFERENCE), revision=current['receipt']['revision'], claim=claim,
        claims={k:dict(statute=s,text=t) for k,(s,t) in claims.items()}, installed=installed,
        components=components, attempts=attempts, axiom_lists_reviewed=23,
        agents_completed_observed=agents, agent_status_source='collaboration.list_agents observed by root in this turn; no automatic hook claimed',
        settled=[t['id'] for t in current['projection']['settled']],
        active=[{k:t[k] for k in ['id','criterion','status']} for t in current['projection']['active']],
        evidence=[pin(p) for p in evidence], providers_called=False, full_requirement_accepted=False)
    new(target, progress)
    text = '\n\n## 16/10/2026 — Componentes revisados e ancoragem aplicada\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, pela reivindicacao vigente F1.FECHO_20261015.\n'
    for name,(statute,body) in claims.items():
        text += f'\n[{statute} — {name}] {body}\n'
    text += f'\nEvidencia: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R42.txt',text)
    new(OUT/'MEMORY_PROGRESS_R42.json',dict(claim=claim,surfaces=[append_bytes(p,text,MARKER) for p in surfaces],evidence=pin(target)))
    new(OUT/'MAP_ENTRY_PROGRESS_R42.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='23 listas de axiomas em componentes revisados; missao preservada',
        resultado=' '.join(t for _,t in claims.values()),estatuto='REAL — componentes; OPEN — requisitos integrais',
        status='EM_CURSO',veredito='THREE_COMPONENTS_PASS_WITH_SCOPE_MISSION_NOT_COMPLETE',
        defeito=claims['remaining'][1],proximo_passo='Integrar somente apos preflight atual; descarregar dominios e ligacoes fisicas restantes.',
        onde=str(OUT),artefatos=[str(target),str(OUT/'MEMORY_PROGRESS_R42.json')],olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_PROGRESS_R42.json','--quem',WHO],'MAP_RECEIPT_PROGRESS_R42.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',target,
        OUT/'MEMORY_PROGRESS_R42.json','--nota','R42: tres componentes revisados, 23 listas no trio; R1-R10 sem reducao de criterio.'],'BOARD_PROGRESS_R42.json')
    current,_=live.project()
    flow=dict(current['projection']['flow'])
    handles=list(flow.get('handles',[]))
    for agent in agents:
        handle=dict(agent,id='r42-agent-return-'+agent['id'].replace('/','_'),
                    agent_id=agent['id'],kind='agent_return',status='completed',
                    observed_only=True,source=pin(target))
        assert not any(h['id']==handle['id'] for h in handles)
        handles.append(handle)
    flow.update(phase='three_components_reviewed_r7_r8_construction_open',
        handles=handles,
        next_action='Nao reconstruir M0/M1 nem componentes revisados. R7 ProbeR2 falhou na instancia Star de pi; corrigir a partir dos fornecedores verdes sem repetir tentativas cegas. R8 S1-S3 falhou em APIs de suavidade/PiLp; depois vem transporte a.e./dominio forte/carga real/energia. Manter R4/R5 dispositivo e R3/R10 integrais.')
    result,receipt=live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),
        actor=live.ACTOR,expected_revision=current['receipt']['revision'],event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text='Tres componentes com build verde e revisao independente: 23 listas no trio. Memoria recuperada e oito arquivos instalados conferidos. Requisitos integrais continuam abertos; detalhes e tentativas em PROGRESS_R42.',
            sources=[dict(kind='artifact',ref=str(target),sha256=pin(target)['sha256'])])],flow=flow)),'R42_TRANSITION')
    print(json.dumps(dict(progress=pin(target),revision=result['revision'],receipt=str(receipt)),ensure_ascii=False))


if __name__=='__main__':
    main()
