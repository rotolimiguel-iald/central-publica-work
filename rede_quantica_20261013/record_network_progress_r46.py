"""Custody material progress and reconcile the exact mission after memory recovery."""
import datetime as dt
import json
import re
import sys
from pathlib import Path
from diary_r1 import ROOT, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg
from custody_fock_stress_r37 import verify

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MEM = ROOT / 'work/memoria_missao_20261016/terminal_records_e3'
sys.path.insert(0, str(OUT / 'mission_resume_20261016'))
import live_mission_r39 as live
reg.DEST = OUT
MARKER = 'mission_recovery_material_progress_r46_20261016'


def main():
    target = OUT / 'PROGRESS_R46.json'
    if target.exists():
        raise RuntimeError('Recover existing immutable registration; never overwrite')
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
            projection_sha256=current['projection_sha256']), 'R46_RECORD_CHECK_'+task_id)
    definitions = [
        ('20261016T173910_273248Z',4,'maxwell_global','R8_NORMALIZATION_REVIEW_R45.json'),
        ('20261016T175125_726518Z',10,'maxwell_global','R46_COMPONENT_INDEPENDENT_REVIEW_R1.json'),
        ('20261016T175543_590282Z',8,'maxwell_global','R46_COMPONENT_INDEPENDENT_REVIEW_R1.json'),
        ('20261016T175315_888014Z',8,'maxwell_global','R46_COMPONENT_INDEPENDENT_REVIEW_R1.json'),
        ('20261016T175448_002037Z',5,'gns_coefficient_tomita','R46_COMPONENT_INDEPENDENT_REVIEW_R1.json'),
        ('20261016T180002_744440Z',14,'maxwell_global','R46_FOCK_STRESS_REVIEW_R1.json')]
    components = []
    for attempt,count,folder,review in definitions:
        d = OUT/'orbital_rotation/attempts'/attempt
        r = json.loads((d/'RECEIPT.json').read_bytes())
        assert r['exit_code'] == 0
        assert r['readonly_dependencies_unchanged'] and r['dependency_cache_unchanged']
        source = OUT/folder/Path(r['source']['path']).name
        assert pin(source)['sha256'] == pin(r['source']['path'])['sha256'] == r['source']['sha256']
        axioms = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", (d/'AXIOMS.txt').read_text(encoding='utf-8'))
        assert len(axioms) == count
        assert all(set(x.strip() for x in a.split(',') if x.strip()) <= {'propext','Classical.choice','Quot.sound'} for _,a in axioms)
        rp = OUT/'mission_review_20261016'/review
        reviewed = json.loads(rp.read_bytes())
        assert reviewed['verdict'].startswith('PASS_')
        assert reviewed.get('requirement_satisfied') is not True
        components.append(dict(source=pin(source),build=pin(d/'RECEIPT.json'),
            review=pin(rp),axiom_lists=count,seconds=r['seconds'],full_requirement_accepted=False))
    custody = OUT/'maxwell_global/UNITARY_FOURIER_FOCK_STRESS_CUSTODY_R46.json'
    new(custody, dict(statute='REAL',build=verify('20261016T180002_744440Z',14),
        scope='Compiled normalized regular Fock stress component; full R8 remains open.'))
    deployment = json.loads((MEM/'DELIVERY_E3.json').read_bytes())
    installed = []
    for expected in deployment['installed_current']:
        actual = pin(expected['path'])
        assert actual['sha256'] == expected['sha256']
        installed.append(actual)
    state, fetched = live.call('session_memory.py', dict(operation='get',reference=str(live.REFERENCE)), 'R46_RECORD_GET')
    attempts = []
    early = list((OUT/'orbital_rotation/attempts').glob('20261016T175109*/RECEIPT.json'))
    assert len(early) == 1
    for stamp in [early[0].parent.name,'20261016T180256_952949Z','20261016T180449_754475Z','20261016T180632_565196Z']:
        path = OUT/'orbital_rotation/attempts'/stamp/'RECEIPT.json'
        r = json.loads(path.read_bytes())
        assert r['exit_code'] != 0
        h = next(h for h in state['p']['handles'] if h['id'] == 'build-'+stamp)
        assert h['status'] == 'failed'
        attempts.append(dict(id=stamp,status='failed',receipt=pin(path),exit_code=r['exit_code']))
    claims = [
        ('REAL','Memoria recuperada pela referencia exata. M0/M1/M2/M3 satisfeitos; oito destinos instalados conferidos por hash. Dois builds terminados que ainda constavam running foram conciliados como failed nas revisoes217/218, sem repeticao; agentes anteriores estao encerrados.'),
        ('REAL','A projecao bruta de sessao recusou o limite130000; recuperacao com capacidade1000000 foi bem-sucedida. A projecao operacional da missao segue legivel com100000. Nenhum contexto foi truncado silenciosamente; a recusa e limite explicito, nao perda do banco.'),
        ('REAL','Seis componentes compilados e revisados,49 listas de axiomas somente no trio: normalizacao escalar4, reducao da derivada10, derivada forte construida8, tensor normalizado8, norma/ordem GNS concreto5, forma momento-energia Fock normalizada14. Estes componentes nao constituem aceite integral de R7/R8.'),
        ('REAL','A derivada forte do boost foi construida no mesmo H1 a partir de suporte compacto, majorante integravel e convergencia dominada. A especializacao nativa de norma/ordem no GNS concreto compila sem nova hipotese de traco ou troca de representacao.'),
        ('OPEN','Aditividade inversa concreta R1 e ligacao do momento nulo R2 terminaram EXIT1; os recibos falhos ficam preservados. Restam traco/PF concreto, carga no mesmo Fock e testemunha de energia modular nao nula, relogio e realizacao do dispositivo, integracao/rito v394 e revisao conjunta.'),
        ('REAL','PODA operacional separa fatos materiais q do fluxo p e indexa apenas registros mecanicos terminais verificaveis. E3 mediu99761 para78058 caracteres no mesmo snapshot, com historia preservada;46 testes de controlador e10 de tracker. Nao e medida de tokens faturados, Lindblad nos pesos ou garantia de infalibilidade. Clientes precisam aderir ao protocolo; MCP antigo nao foi reiniciado.')]
    progress = dict(unit='F1.FECHO_20261015',author=WHO,at=dt.datetime.now(dt.timezone.utc).isoformat(),
        claim=claim,reference=pin(live.REFERENCE),revision=state['revision'],components=components,
        reviewed_axiom_lists=49,failed_attempts=attempts,installed_memory=installed,
        claims=[dict(statute=s,text=t) for s,t in claims],
        evidence=[pin(projected),pin(fetched),pin(custody),pin(MEM/'FINAL_E3.json')],
        full_mission_complete=False,providers_called=False,production_science_modified=False,gate_moved=False)
    new(target,progress)
    text='\n\n## 16/10/2026 — Memoria sincronizada e componentes R46 preservados\n'
    text+=f'<!-- {MARKER} -->\nEm nome de {WHO}, sob a reivindicacao vigente F1.FECHO_20261015.\n'
    text+=''.join(f'\n[{s}] {t}\n' for s,t in claims)
    text+=f'\nEvidencia: `{target}`; SHA256 `{pin(target)["sha256"]}`.\n'
    new(OUT/'MEMORY_ADDITION_R46.txt',text)
    memory = OUT/'MEMORY_PROGRESS_R46.json'
    new(memory,dict(claim=claim,evidence=pin(target),surfaces=[append_bytes(p,text,MARKER) for p in surfaces]))
    entry=OUT/'MAP_ENTRY_PROGRESS_R46.json'
    new(entry,dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',dominio='FORMAL',
        titulo='R46: memoria conciliada; derivada forte e norma/ordem GNS construidas',
        resultado=' '.join(t for _,t in claims),estatuto='REAL — componentes; OPEN — missao integral',
        status='EM_CURSO',veredito='COMPONENTS_PASS_WITH_SCOPE_MISSION_NOT_COMPLETE',
        defeito=claims[4][1],proximo_passo='Retomar somente residuos de R7/R8 apos sincronizar, sem repetir componentes aceitos.',
        onde=str(OUT),artefatos=[str(target),str(memory)],olhou_dados=False))
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO],'MAP_RECEIPT_PROGRESS_R46.json')
    reg.call([CLI,'avancar','F1.FECHO_20261015','--quem',WHO,'--status','EM_CURSO','--evidencia',target,memory,
        '--nota','R46: seis componentes revisados;49 listas no trio. Memoria reconciliada; criterios integrais preservados.'],'BOARD_PROGRESS_R46.json')
    state,_=live.call('session_memory.py',dict(operation='get',reference=str(live.REFERENCE)),'R46_FINAL_GET')
    r,receipt=live.call('session_memory.py',dict(operation='transition',reference=str(live.REFERENCE),
        actor=live.ACTOR,expected_revision=state['revision'],event_id=MARKER,
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text='R46: seis componentes revisados,49 listas no trio. Derivada forte H1 e norma/ordem GNS construidas; forma Fock normalizada. Duas candidatas finais falharam; recibos conciliados, sem repeticao. Memoria M0-M3 verificada; R7/R8 integrais e missao continuam abertos.',
            sources=[dict(kind='artifact',ref=str(target),sha256=pin(target)['sha256'])])],
            flow=dict(handles=state['p']['handles'],phase='memory_reconciled_concrete_trace_and_fock_charge_open',
                next_action='Sincronizar antes de retomar: corrigir corte positivo R7 e elaboracao do momento nulo R8 em arquivos novos; nao reconstruir componentes aceitos.'))),'R46_FINAL_TRANSITION')
    verified,vr=live.call('session_memory.py',dict(operation='verify',reference=str(live.REFERENCE)),'R46_FINAL_VERIFY')
    print(json.dumps(dict(progress=pin(target),revision=r['revision'],receipt=str(receipt),verify_receipt=str(vr),verify_ok=verified.get('ok')),ensure_ascii=False))


if __name__=='__main__':
    main()
