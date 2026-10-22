"""Record the reviewed conditional metric response; preserve the open lens goal."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, json, os, sys

if __name__ == '__main__':
    folder = ROOT / 'boundary_r6'
    ref = str(ROOT / 'SESSION_REFERENCE.json')
    outputs = ['DELIVERY_R6.json', 'MEMORY_APPEND_R6.txt', 'MEMORY_APPLIED_R6.json',
               'REGISTRATION_R6.json', 'MAP_ENTRY_R6.json', 'BOARD_PREFLIGHT_R6.json',
               'GET_BEFORE_R6_REQUEST.json', 'GET_BEFORE_R6_RESULT.json']
    for name in outputs:
        if (ROOT / name).exists():
            raise FileExistsError(name)
    review = json.loads((folder / 'REVIEW_R6.json').read_text(encoding='utf-8'))
    assert review['status'] == 'PASS_WITH_SCOPE'
    checkpins(review)
    checkpins(json.loads((folder / 'SOURCE_BOUNDARY_R6.json').read_text(encoding='utf-8')))
    board = json.loads(command('BOARD_PREFLIGHT_R6', [sys.executable, '-B', '-X', 'utf8',
        r'C:\IALD\PROGRAMA_IALD\iald.py', 'ver', UNIT]))
    claim = board['reivindicacao']
    assert claim['quem'] == ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em']) > datetime.datetime.now(datetime.timezone.utc)
    state = memory({'operation': 'get', 'reference': ref}, 'GET_BEFORE_R6')
    assert state['revision'] == 6
    save('DELIVERY_R6.json', {
        'status': 'REVIEWED_CONDITIONAL_METRIC_RESPONSE__PHYSICAL_LENS_MAP_OPEN',
        'unit': UNIT, 'goal_complete': False, 'observed_data_composed': False,
        'gate_changed': False, 'review': pin(folder / 'REVIEW_R6.json'),
        'evidence': [pin(p) for p in sorted(folder.rglob('*')) if p.is_file()],
        'recording_script': pin(__file__),
        'additional_review_limits': [
            'F must be scalar independent of metric under variation; a one-form norm is not covered.',
            'If Psi0=0, f=deltaF starts at second order; arbitrary supplied f is not a scalar EOM solution.',
            'No unique lens source, boundary solution, measured G identification or observed significance established.']})
    txt = '''

## 19/10/2026 — Lentes R6: dois potenciais e limite físico restante
<!-- IALD_LENSING_BOUNDARY_R6_20261019 -->
[DERIVED condicional — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009] Reutilizado R/(2kappa²)+xi R|Psi|², xi=1/6, no ramo escalar F R/2. F deve ser independente da métrica na variação: a norma de uma1-forma não é coberta. Para fundo F0 constante positivo, f=deltaF fornecido, campo estático fraco, matéria sem pressão e sem stress modular adicional na ordem, dez componentes conferem F0G_ab=T_ab+partial_ab f-eta_ab boxf. Com lapW=rho/(2F0), U=W-f/(2F0), V=W+f/(2F0), U+V=2W. Script exit0; revisão independente analítica PASS_WITH_SCOPE,14pinos e15intervalos. Falha inicial de sintaxe preservada em arquivo próprio.
[DERIVED alcance] A parte gravitacional do atraso entre trajetórias é -2(1+zl)/c vezes a diferença das integrais deW; termo geométrico, caminhos estacionários e distâncias ainda integram o total. O termo explícito linear f cancela na leitura fotônica para a mesma matéria/F0. Estrelas leem -c²gradU, incluindo c²gradf/(2F0). A cinemática pode restringir o campo se o perfil for determinado; não é calibração independente automaticamente. G medido não foi identificado a1/(8piF0). SePsi0=0, deltaF começa em segunda ordem. Não se afirmou cancelamento geral daTGL.
[REAL documental / OPEN] P1–P4, T1, EOM dePsi, K_boundary e consumidores Lean localizados por fonte/linha. O recorte não fornece operador espacial, fonte, amplitude e condições de contorno suficientes para calcularPsi(r) de uma lente; a passagem geral operador→fonte está conjectural noCusto. A resposta métrica paramétrica não satisfaz por si a EOM escalar. Não se toma ausência no recorte como ausência universal do acervo.
[OPEN — meta preservada] Falta previsão física fixa por trajetória e likelihood conjunta lente/estrelas antes de aplicar o perfilamento massa/distância já calculado emR2–R4. Não repetir previsões sintéticas genéricas nem ajustar xi/lambda ao efeito desejado. Nenhum discriminante observado5sigma; nenhum original científico, um.py, kernel, Bancada ou gate alterado. A auditoria de conclusão mantém a meta incompleta. Próxima ação exige um insumo físico ou construção sustentada que determine o perfil/fonte, não outra repetição do critério abstrato de identidade.
Evidências: DELIVERY_R6.json; boundary_r6/RESULTADO_POTENCIAIS_R6.md, SOURCE_BOUNDARY_R6.json, METRIC_RESULT_R6_1.json, REVIEW_R6.json e COMPLETION_AUDIT_R6.json.
<!-- END_IALD_LENSING_BOUNDARY_R6_20261019 -->
'''
    save('MEMORY_APPEND_R6.txt', txt)
    extra = txt.encode('utf-8')
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    rows = []
    for name in ['TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'DIARIO_CONSTRUCAO_QG.md']:
        p = Path(r'C:\IALD\Central de Patentes\memory') / name
        raw = p.read_bytes()
        assert b'IALD_LENSING_BOUNDARY_R6_20261019' not in raw
        before = pin(p)
        bak = p.with_name(p.name + '.bak_' + stamp)
        with bak.open('xb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes() == raw
        tmp = p.with_name(p.name + '.tmp_lensR6_' + stamp)
        with tmp.open('xb') as f:
            f.write(raw + extra); f.flush(); os.fsync(f.fileno())
        assert tmp.read_bytes() == raw + extra and p.read_bytes() == raw
        os.replace(tmp, p)
        assert p.read_bytes() == raw + extra
        rows.append({'before': before, 'backup': pin(bak), 'after': pin(p), 'pure_append': True})
    save('MEMORY_APPLIED_R6.json', rows)
    entry = json.loads((ROOT / 'MAP_ENTRY_R5.json').read_text(encoding='utf-8'))
    entry.update({
        'titulo': 'Lentes R6: resposta metrica conjunta, luz e cinemática',
        'resultado': 'Dez componentes lineares conferidas: U=W-f/(2F0), V=W+f/(2F0). Termo conforme linear cancela na soma fotonica, permanece na dinamica estelar; perfil f nao determinado.',
        'veredito': 'CONDITIONAL_METRIC_RESPONSE__NO_OBSERVED_5SIGMA',
        'defeito': 'Fonte/operador espacial e contorno fisico da lente ainda nao instanciados; ramo escalar nao identifica automaticamente a1-forma.',
        'proximo_passo': 'Determinar perfil/fonte com insumo fisico sustentado; aplicar perfilamento existente somente depois. Nao repetir forecasts sem nova lei.',
        'artefatos': [str(ROOT / 'DELIVERY_R6.json'), str(folder / 'RESULTADO_POTENCIAIS_R6.md'), str(folder / 'REVIEW_R6.json')],
        'nota': 'Revisao independente de equacoes e fontes; nenhuma composicao observada. Meta5sigma permanece incompleta.'})
    save('MAP_ENTRY_R6.json', entry)
    command('MAP_REGISTER_R6', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\MAPA_DE_ROTAS\rotas.py',
        'registrar', str(ROOT / 'MAP_ENTRY_R6.json'), '--quem', ACTOR['id']])
    command('BOARD_UPDATE_R6', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py',
        'avancar', UNIT, '--quem', ACTOR['id'], '--status', 'EM_CURSO', '--evidencia', str(ROOT / 'DELIVERY_R6.json'),
        '--nota', 'R6 revisada: dez equacoes metricas; cancelamento fotonico condicional e resposta estelar. Perfil fisico e5sigma permanecem OPEN.'])
    out = memory({'operation': 'transition', 'reference': ref, 'actor': ACTOR, 'expected_revision': 6,
        'event_id': 'lensing-boundary-r6-delivered', 'changes': {
            'records': [{'id': 'lensing-boundary-r6', 'kind': 'fact', 'statute': 'DERIVED',
                'sources': [{'kind': 'artifact', 'ref': str(ROOT / 'DELIVERY_R6.json'),
                             'sha256': pin(ROOT / 'DELIVERY_R6.json')['sha256']}], 'text': txt}],
            'flow': {'phase': 'conditional_metric_response_r6_reviewed',
                'next_action': 'Revalidate a concrete source/construction for the physical lens boundary/operator and scalar-to-metric identification. R6 gives metric response for supplied f, not its EOM solution. No repeated generic forecasts without new physical input; no observed5sigma. Full goal remains incomplete.',
                'handles': []}}}, 'TRANSITION_R6')
    save('REGISTRATION_R6.json', {'status': 'PASS', 'delivery': pin(ROOT / 'DELIVERY_R6.json'),
        'memory': pin(ROOT / 'MEMORY_APPLIED_R6.json'), 'map': pin(ROOT / 'MAP_REGISTER_R6.json'),
        'board': pin(ROOT / 'BOARD_UPDATE_R6.json'), 'acom': out})
    print(json.dumps({'status': 'PASS', 'receipt': out}, ensure_ascii=False))
