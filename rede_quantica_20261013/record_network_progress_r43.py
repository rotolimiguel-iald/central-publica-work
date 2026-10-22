"""Record R43 once, preserving full ACOM handles and immutable source evidence."""
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
MARKER = 'constructed_null_domain_live_mission_20261016_r43'


def main():
    target = OUT / 'PROGRESS_R43.json'
    if target.exists():
        raise RuntimeError('Immutable R43 already exists: recover its registration')
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, projected = live.project()
    for task_id in ['R7', 'R8']:
        task = next(t for t in current['projection']['active'] if t['id'] == task_id)
        live.call('mission_cli.py', dict(operation='check', reference=str(live.REFERENCE),
            actor=live.ACTOR, task_id=task_id, lease_id=task['lease']['id'],
            expected_revision=current['receipt']['revision'],
            projection_sha256=current['projection_sha256']), 'R43_RECORD_CHECK_'+task_id)
    definitions = [
        ('maxwell_global/NULL_SCHWARTZ_CORE_CUSTODY_R43.json',
         'R8_NULL_CORE_REVIEW_R43.json', '20261016T161839_194180Z', 14),
        ('maxwell_global/NULL_FREQUENCY_AE_CUSTODY_R43.json',
         'R8_NULL_DOMAIN_REVIEW_R43.json', '20261016T162928_136157Z', 4),
        ('maxwell_global/NULL_SCHWARTZ_DOMAIN_CUSTODY_R43.json',
         'R8_NULL_DOMAIN_REVIEW_R43.json', '20261016T163243_822675Z', 3),
        ('maxwell_global/CONSTRUCTED_NULL_CONSUMER_CUSTODY_R43.json',
         'R8_CONSTRUCTED_CONSUMER_REVIEW_R43.json', '20261016T163809_911747Z', 4),
        ('maxwell_global/NULL_SAMESIGN_CUSTODY_R43.json',
         'R8_SAMESIGN_REVIEW_R43.json', '20261016T164950_597875Z', 10)]
    components = []
    for custody, review, attempt, count in definitions:
        rp = OUT/'mission_review_20261016'/review
        reviewed = json.loads(rp.read_bytes())
        assert reviewed['verdict'] == 'PASS_COMPONENT_WITH_SCOPE'
        assert reviewed['r8_snapshot']['status'] == 'working'
        assert not reviewed.get('blocking_findings')
        assert reviewed.get('requirement_satisfied') is not True
        bp = OUT/'orbital_rotation/attempts'/attempt/'RECEIPT.json'
        r = json.loads(bp.read_bytes())
        assert type(r['exit_code']) is int and r['exit_code'] == 0
        assert r['readonly_dependencies_unchanged'] and r['dependency_cache_unchanged']
        source = r['source']
        original = OUT/'maxwell_global'/Path(source['path']).name
        assert pin(source['path'])['sha256'] == source['sha256'] == pin(original)['sha256']
        c = json.loads((OUT/custody).read_bytes())
        assert len(c['axioms']) == count
        components.append(dict(task_id='R8', requirement_satisfied=False, axiom_lists=count,
            source=pin(original), build=pin(bp), custody=pin(OUT/custody), review=pin(rp),
            verdict=reviewed['verdict']))
    # Later deployments supersede earlier hashes on the same target.
    expected = {}
    for manifest in [MEM/'DEPLOYMENT.json', MEM/'handoff_capacity_e1/DEPLOYMENT_E1.json',
                     MEM/'terminal_projection_e2/DEPLOYMENT_E2.json']:
        expected.update({x['target']:x['new_sha256'] for x in json.loads(manifest.read_bytes())['files']})
    installed = [pin(path) for path in expected]
    assert all(p['sha256'] == expected[p['path']] for p in installed)
    state, fetched = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R43_RECORD_GET')
    full_handles = state['p']['handles']
    attempt_ids = ['20261016T161251_564901Z', '20261016T161522_527783Z',
        '20261016T161839_194180Z', '20261016T162008_655693Z', '20261016T162928_136157Z',
        '20261016T163243_822675Z', '20261016T163357_662786Z', '20261016T163809_911747Z',
        '20261016T164448_563291Z', '20261016T164447_504879Z', '20261016T164950_597875Z']
    attempts = []
    for attempt in attempt_ids:
        bp = OUT/'orbital_rotation/attempts'/attempt/'RECEIPT.json'
        r = json.loads(bp.read_bytes())
        h = next(h for h in full_handles if h['id'] == 'build-'+attempt)
        assert h['status'] in ['completed', 'failed', 'terminated']
        assert (r['exit_code'] == 0) == (h['status'] == 'completed')
        attempts.append(dict(id=attempt, status=h['status'], exit_code=r['exit_code'],
                             seconds=r['seconds'], receipt=pin(bp)))
    claims = {
        'anchor': ('REAL', 'Referencia propria recuperada apos compactacao. M0/M1/M2 permanecem satisfeitos por revisao independente; oito destinos instalados conferidos pela cadeia M0+E1+E2. Devolucoes e compilações conciliadas no estado completo, com CAS; detalhes terminais fora do fluxo ativo e preservados no get. Nenhuma tarefa alheia adotada.'),
        'null_profile': ('REAL', 'S1-S3 constroem o perfil de Schwartz de frequencia nula a partir do nucleo suave compacto afastado do eixo no H1 real da rede. S4 transporta igualdades quase em toda parte entre as coordenadas orbitais e nulas. Fontes, builds e revisao independente estao pinados.'),
        'domain': ('REAL', 'S5-S6 constroem NullSchwartzData no mesmo H1 e provam densidade, pertencimento ao range de physicalSmearCLM e existencia de um vetor H1 nao nulo. O consumidor construtivo liga a onda existente, Parseval ponderado misto e B0, sem receber NullSchwartzData como premissa separada. Cinco componentes revisados,35 listas no trio,zero sorry.'),
        'real_wave': ('REAL', 'NullSchwartzSameSignR2 prova integrabilidade e anulacao do primeiro momento dos produtos de mesmo sinal para perfis de frequencia positiva. O produto das partes reais corresponde a metade da parte real do produto misto, preservando o fator -i(2pi)^3. Isso e uma identidade da onda de Schwartz, ainda nao a carga real em Fock.'),
        'scope': ('OPEN', 'Vetor H1 nao nulo nao e testemunha de energia modular nao nula. Ainda faltam a derivada forte em H1, a carga real em estados de Fock e a testemunha de energia do certificado Maxwell. Os resultados atuais nao satisfazem o criterio integral R8.'),
        'takesaki': ('REAL', 'R7 ProbeR3 foi interrompida deliberadamente depois de1234,019s, com diagnostico e identidade do processo preservados. R4 terminou EXIT1 em191,735s. R5 terminou EXIT1 em398,880s: sintaxe de docstring/set_option e limite1.800.000 nas fronteiras de norma/ordem; apenas conjugacao imprimiu o trio. Nao sao contraexemplos matematicos. R7 integral continua aberto; nao elevar novamente o limite sem isolar a conversao cara.'),
        'commentary_correction': ('REAL', 'ERRATA em nome de codex-gerente-tgl: a atualizacao ao operador que disse concluida a etapa de norma da R7 tomou o marcador norm returned como sucesso. O marcador so sinaliza passagem para a declaracao seguinte; o recibo final foi EXIT1 com timeout. Nenhuma prova de norma dessa tentativa foi aceita. A correcao foi comunicada imediatamente apos a leitura do resultado terminal.'),
        'remaining': ('OPEN', 'R3/R4/R5/R7/R8/R10: rito e integracao v394, relogio/espectro do objeto fisico, realizacao do dispositivo, traco/PF na representacao pretendida, Maxwell completo e revisao conjunta. Base v393; V351 e linhagem de lemas reutilizados. Nenhum provedor novo, original cientifico, Bancada, dado observado ou gate alterado.'),
        'memory_limit': ('REAL', 'A sincronizacao opera por revisao, lease, pinos e CAS nas fronteiras de trabalho e devolucao. Clientes que ignoram o protocolo nao ficam sincronizados automaticamente; nao se afirma Lindblad nos pesos ou infalibilidade. A PODA medida reduziu caracteres de contexto, sem alegacao de tokens faturados medidos.')}
    extra = [pin(Path(p)) for p in sys.argv[1:]]
    progress = dict(unit='F1.FECHO_20261015', author=WHO,
        at=dt.datetime.now(dt.timezone.utc).isoformat(), reference=pin(live.REFERENCE),
        revision=state['revision'], claim=claim, claims={k:dict(statute=s,text=t) for k,(s,t) in claims.items()},
        components=components, axiom_lists_reviewed=35, attempts=attempts, installed=installed,
        evidence=[pin(projected),pin(fetched)]+extra,
        settled=[t['id'] for t in current['projection']['settled']],
        active=[{k:t[k] for k in ['id','criterion','status']} for t in current['projection']['active']],
        full_requirement_accepted=False, providers_called=False)
    new(target, progress)
    text = '\n\n## 16/10/2026 — Dominio nulo construido e memoria da missao aplicada\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, pela reivindicacao F1.FECHO_20261015 vigente.\n'
    for key,(statute,body) in claims.items():
        text += f'\n[{statute} — {key}] {body}\n'
    text += f'\nEvidencia: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R43.txt', text)
    new(OUT/'MEMORY_PROGRESS_R43.json', dict(claim=claim,evidence=pin(target),
        surfaces=[append_bytes(p,text,MARKER) for p in surfaces]))
    entry = OUT/'MAP_ENTRY_PROGRESS_R43.json'
    new(entry, dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='Dominio nulo Schwartz construido no H1; 35 listas revisadas',
        resultado=' '.join(t for _,t in claims.values()),estatuto='REAL — componentes; OPEN — missao integral',
        status='EM_CURSO',veredito='FIVE_COMPONENTS_PASS_WITH_SCOPE_MISSION_NOT_COMPLETE',
        defeito=claims['remaining'][1],proximo_passo='Derivada forte, carga real e energia; traco/PF no sistema pretendido.',
        onde=str(OUT),artefatos=[str(target),str(OUT/'MEMORY_PROGRESS_R43.json')],olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO], 'MAP_RECEIPT_PROGRESS_R43.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO',
        '--evidencia',target,OUT/'MEMORY_PROGRESS_R43.json','--nota',
        'R43: dominio de Fourier construido;35 listas revisadas. Criterios integrais preservados.'], 'BOARD_PROGRESS_R43.json')
    # Re-read after external registrations: never reconstruct handles from the compact projection.
    state,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)),'R43_FINAL_GET')
    r,receipt=live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),
        actor=live.ACTOR,expected_revision=state['revision'],event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text='R43: cinco componentes revisados,35 listas no trio; dominio nulo construido no mesmo H1 e identidade de onda real. R7 ProbeR5 falhou; marcador de progresso nao certifica sucesso. Requisitos integrais continuam abertos. Ver PROGRESS_R43.',
            sources=[dict(kind='artifact',ref=str(target),sha256=pin(target)['sha256'])])],
            flow=dict(handles=state['p']['handles'],phase='constructed_null_domain_full_maxwell_and_trace_open',
                next_action=claims['remaining'][1]))),'R43_FINAL_TRANSITION')
    print(json.dumps(dict(progress=pin(target),revision=r['revision'],receipt=str(receipt)),ensure_ascii=False))


if __name__=='__main__': main()
