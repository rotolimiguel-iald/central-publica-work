"""Register accepted R7/R8 and exact residuals once, with immutable evidence."""
import copy
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'mission_material_progress_r52_20261016'

def main():
    target = OUT / 'PROGRESS_R52.json'
    if target.exists():
        raise RuntimeError('Recover existing immutable stage; never overwrite')
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', OUT.parent/'AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    current, project_receipt = live.project()
    settled = {t['id']: t for t in current['projection']['settled']}
    assert all(settled[x]['status'] == 'satisfied' for x in ['R7','R8','M0_MEMORIA',
        'M1_HANDOFF_CAPACITY','M2_TERMINAL_PROJECTION','M3_TERMINAL_RECORDS'])
    sources = [OUT/'R7_DELIVERY_R52.json', OUT/'R8_DELIVERY_R52.json',
        OUT/'mission_review_20261016/R52_R7_FULL_REVIEW_R1.json',
        OUT/'mission_review_20261016/R52_R7_ACCEPT_RECEIPT_R1.json']
    # Review evidence is read from the accepted controller task, not guessed by name.
    for requirement in ['R7','R8']:
        for item in settled[requirement]['evidence'] + settled[requirement]['review_evidence']:
            assert pin(item['path'])['sha256'] == item['sha256']
            p = Path(item['path'])
            if p not in sources:
                sources.append(p)
    memory_delivery = ROOT/'work/memoria_missao_20261016/terminal_records_e3/DELIVERY_E3.json'
    installed = json.loads(memory_delivery.read_bytes())['installed_current']
    assert all(pin(x['path'])['sha256'] == x['sha256'] for x in installed)
    state, _ = live.call('session_memory.py', dict(operation='get', reference=str(live.REFERENCE)), 'R52_FINAL_GET')
    handles = copy.deepcopy(state['p']['handles'])
    h = next(x for x in handles if x['id'] == 'r52-r8-final-review')
    assert h['status'] in ['running','returned','accepted']
    h.update(status='accepted', receipt=settled['R8']['review_evidence'][0], requirement_accepted=True)
    live.call('session_memory.py', dict(operation='transition', reference=str(live.REFERENCE),
        actor=live.ACTOR, expected_revision=state['revision'], event_id='r52-r8-review-returned-and-accepted',
        changes=dict(flow=dict(handles=handles))), 'R52_REVIEW_FLOW')
    current, project_receipt = live.project()
    assert not current['projection']['unresolved_handles']
    failures = []
    for stamp in ['20261016T205837_144649Z','20261016T210854_377096Z']:
        p = OUT/'orbital_rotation/attempts'/stamp/'RECEIPT.json'
        r = json.loads(p.read_bytes())
        assert r['exit_code'] != 0
        failures.append(dict(attempt=stamp, receipt=pin(p), exit_code=r['exit_code']))
    next_action = ('R4/R5: retomar apenas a identificacao fisica do relogio/espectro e do dispositivo completo, '
        'partindo do inventario e diagnosticos existentes. A rede compacta, covariancia Lorentz futura, '
        'Fock, core/trace/PF e Maxwell conjunto ja estao construidos no alcance dos recibos; nao refazer. '
        'R3: pacote candidato e rito integral depois das dependencias. R10: revisao final distinta. '
        'M0-M3 satisfeitos: usar sincronizacao/preflight/handoff e PODA; nenhuma nova arquitetura de memoria sem achado material.')
    claims = [
        ('REAL','R7 aceito por revisor distinto no criterio original. Os 21 campos de RemainingModularCoreInput foram preenchidos e especializados em physicalCanonicalNet/physicalFockCertificate. Split e fornecedor: 14 listas de axiomas somente no trio.'),
        ('REAL','R8 aceito por revisor distinto no criterio original. Transporte circular de Maxwell e consumidor conjunto: 26 listas de axiomas somente no trio, na mesma rede e no mesmo Fock. Ha testemunha regular normalizada, energia modular nao nula, identidade de carga e identificacao Wick simultaneas.'),
        ('REAL','O tensor Wick e simetrico e conservado distribucionalmente no dominio regular; o consumidor geometrico usa esse mesmo tensor. N e G positivo continuam entradas nomeadas; H3 aqui tem alcance fixo-nulo/linearizado. Nao se afirma Einstein nao linear universal nem realizacao do dispositivo.'),
        ('REAL','Errata de estado ao lado da R51: A e D deixaram de ser pendencias. D=physicalCanonicalNet ja existia desde R35; o A concreto foi concluido nesta R52. A leitura total ENNReal e ciclica; nao se afirma linearidade complexa em toda a algebra.'),
        ('REAL','Memoria M0-M3 instalada, aceita e oito alvos reconferidos por hash. 46 testes do controlador e 10 do tracker constam dos recibos; reducao historica de projecao 21,75% em caracteres, sem medida de tokens faturados. CLI em processo novo usado; MCPs antigos nao foram reiniciados.'),
        ('OPEN','R4/R5: identificacao fisica do relogio/espectro com o dispositivo completo; R3: candidato e rito integral; R10: revisao final. A missao nao terminou. Nenhum original cientifico, producao, dado observado ou gate foi alterado.'),
    ]
    progress = dict(unit='F1.FECHO_20261015', author=WHO, at=dt.datetime.now(dt.timezone.utc).isoformat(),
        claim=claim, reference=pin(live.REFERENCE), revision=current['receipt']['revision'],
        accepted_requirements={key:settled[key] for key in ['R7','R8']}, new_axiom_reports=40,
        evidence=[pin(p) for p in sources] + [pin(project_receipt),pin(memory_delivery),pin(Path(__file__))],
        failed_attempts=failures, installed_memory=installed,
        claims=[dict(statute=s,text=t) for s,t in claims], next_action=next_action,
        active_requirements=current['projection']['active'], unresolved_handles=[],
        full_mission_complete=False, providers_called=False, production_science_modified=False, gate_moved=False)
    new(target, progress)
    text = '\n\n## 16/10/2026 — R52: Takesaki e Maxwell conjuntos aceitos\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, sob reivindicacao F1.FECHO_20261015.\n'
    text += ''.join(f'\n[{s}] {t}\n' for s,t in claims)
    text += f'\nEvidencia: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R52.txt',text)
    mem=OUT/'MEMORY_PROGRESS_R52.json'
    new(mem,dict(claim=claim,evidence=pin(target),surfaces=[append_bytes(p,text,MARKER) for p in surfaces]))
    entry=OUT/'MAP_ENTRY_PROGRESS_R52.json'
    new(entry,dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',dominio='FORMAL',
        titulo='R52: R7 e R8 aceitos na mesma rede e no mesmo Fock',resultado=' '.join(t for _,t in claims),
        estatuto='REAL — requisitos R7/R8; OPEN — missao integral',status='EM_CURSO',
        veredito='R7_R8_ACCEPTED_WITH_EXPLICIT_SCOPE_MISSION_NOT_COMPLETE',
        defeito=claims[-1][1],proximo_passo=next_action,onde=str(OUT),artefatos=[str(target),str(mem)],olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO],'MAP_RECEIPT_PROGRESS_R52.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',target,mem,
        '--nota','R52: R7/R8 aceitos por revisor distinto; 40 listas novas no trio; R4/R5/R3/R10 preservados abertos.'],'BOARD_PROGRESS_R52.json')
    state,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)),'R52_MATERIAL_GET')
    result,receipt=live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),
        actor=live.ACTOR,expected_revision=state['revision'],event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text='R52: R7 Takesaki e R8 Maxwell conjunto aceitos por revisor distinto; 40 listas novas somente no trio. A concreto e D concreto nao sao mais residuos. Mantidos limites ENNReal/fixo-nulo. R4/R5/R3/R10 abertos; memoria M0-M3 instalada e reconferida. Recibo define alcances e proxima acao.',
            sources=[dict(kind='artifact',ref=str(target),sha256=pin(target)['sha256'])])],
            flow=dict(handles=state['p']['handles'],phase='concrete_takesaki_and_maxwell_accepted',next_action=next_action))), 'R52_MATERIAL_TRANSITION')
    verified,vr=live.call('session_memory.py',dict(operation='verify',reference=str(live.REFERENCE)),'R52_FINAL_VERIFY')
    print(json.dumps(dict(progress=pin(target),revision=result['revision'],receipt=str(receipt),verify_receipt=str(vr),verify_ok=verified.get('ok')),ensure_ascii=False))

if __name__ == '__main__':
    main()
