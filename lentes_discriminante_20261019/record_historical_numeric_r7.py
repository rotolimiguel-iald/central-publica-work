"""Record the reviewed conditional metric response; preserve the open lens goal."""
from setup import ROOT, ACTOR, UNIT, save, command, memory
from record_trajectory_r2 import pin, checkpins
from pathlib import Path
import datetime, json, os, sys

if __name__ == '__main__':
    folder = ROOT / 'historical_r7'
    ref = str(ROOT / 'SESSION_REFERENCE.json')
    outputs = ['DELIVERY_R7.json', 'MEMORY_APPEND_R7.txt', 'MEMORY_APPLIED_R7.json',
               'REGISTRATION_R7.json', 'MAP_ENTRY_R7.json', 'BOARD_PREFLIGHT_R7.json',
               'GET_BEFORE_R7_REQUEST.json', 'GET_BEFORE_R7_RESULT.json']
    for name in outputs:
        if (ROOT / name).exists():
            raise FileExistsError(name)
    review = json.loads((folder / 'REVIEW_R7.json').read_text(encoding='utf-8'))
    assert review['status'] == 'PASS_WITH_SCOPE'
    checkpins(review)
    checkpins(json.loads((ROOT / 'boundary_r6' / 'FOLLOWUP_SOURCE_R7.json').read_text(encoding='utf-8')))
    board = json.loads(command('BOARD_PREFLIGHT_R7', [sys.executable, '-B', '-X', 'utf8',
        r'C:\IALD\PROGRAMA_IALD\iald.py', 'ver', UNIT]))
    claim = board['reivindicacao']
    assert claim['quem'] == ACTOR['id']
    assert datetime.datetime.fromisoformat(claim['vence_em']) > datetime.datetime.now(datetime.timezone.utc)
    state = memory({'operation': 'get', 'reference': ref}, 'GET_BEFORE_R7')
    assert state['revision'] == 7
    save('DELIVERY_R7.json', {
        'status': 'REVIEWED_HISTORICAL_NORMALIZATION__PHYSICAL_LENS_MAP_OPEN',
        'unit': UNIT, 'goal_complete': False, 'observed_data_composed': False,
        'gate_changed': False, 'review': pin(folder / 'REVIEW_R7.json'),
        'evidence': [pin(p) for p in sorted(folder.rglob('*')) if p.is_file()],
        'recording_script': pin(__file__), 'source_followup': pin(ROOT/'boundary_r6/FOLLOWUP_SOURCE_R7.json'), 'run': pin(ROOT/'RUN_NUMERIC_R7.json'),
        'additional_review_limits': ['Arithmetic and dimensional checks only; not a repaired physical prediction.', 'The source lookup is bounded; no universal absence is claimed.']})
    txt = '''

## 19/10/2026 — Lentes R7: normalizações históricas conferidas
<!-- IALD_LENSING_BOUNDARY_R7_20261019 -->
[REAL documental / DERIVED aritmético — em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009] Recuperado o .tex histórico tgl_cosmological_observables e fontes correlatas. Há potencial e perfil proporcional NFW declarados; isso não fixa a amplitude nem resolve EOM. A conta impressa10^16*0,1*(2e5/3e10)^4 dá excesso1/506250, ou0,00019753%, não10%. Velocidades misturam SI/CGS; corrigir só c dá198,078, fora do regime perturbativo e sem validar o coeficiente. Não se apresenta esse número como previsão corrigida.
[DERIVED] hbar/(m v) com5meV/c² e200km/s dá0,059157m, não2,7kpc. A distância anunciada é1,408e21vezes maior. Inversão algébrica não é proposta de nova massa. K0²/(G M²), seK0=L*sqrt(rho_mass), não é adimensional emSI; integral de|Psi|²/M_Pl² emdl físico precisa de normalização. Nenhum beta foi substituído porxi. Auditoria independente PASS_WITH_SCOPE,5pinos; original preservado. A leitura anterior07_IMAC_OBSERVAVEIS102 chama1–3kpc de previsão: a fórmula específica aqui examinada não sustenta esse número. Não se excluem escalas coletivas com outra construção.
[REAL documental / DECLARADO nos resultados históricos] Levantamento adicional em FOLLOWUP_SOURCE_R7.json pinou os originais e localizou amplitudePsi0 ajustável e ensaio de deflexão não realizado com dados reais. Os alegados resultados antigos não são detecção reproduzida nesta etapa. Os relatos antigos e suas normalizações não fornecem ainda a amplitude fixa exigida pela meta.
[OPEN] Fonte/perfil espacial da lente e relação conjunta luz/estrelas continuam não determinados. Reaproveitar R6 e perfilamentoR2–R4 somente com insumo físico sustentado; não repetir forecasts para obter5sigma por escolha de coeficiente. Meta incompleta; nenhum dado composto, programa canônico, kernel, Bancada ou gate alterado.
Evidências: DELIVERY_R7.json; historical_r7/RESULTADO_FONTES_R7.txt, NUMERIC_R7.json, REVIEW_R7.json; boundary_r6/FOLLOWUP_SOURCE_R7.json.
<!-- END_IALD_LENSING_BOUNDARY_R7_20261019 -->
'''
    save('MEMORY_APPEND_R7.txt', txt)
    extra = txt.encode('utf-8')
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    rows = []
    for name in ['TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'DIARIO_CONSTRUCAO_QG.md']:
        p = Path(r'C:\IALD\Central de Patentes\memory') / name
        raw = p.read_bytes()
        assert b'IALD_LENSING_BOUNDARY_R7_20261019' not in raw
        before = pin(p)
        bak = p.with_name(p.name + '.bak_' + stamp)
        with bak.open('xb') as f:
            f.write(raw); f.flush(); os.fsync(f.fileno())
        assert bak.read_bytes() == raw
        tmp = p.with_name(p.name + '.tmp_lensR7_' + stamp)
        with tmp.open('xb') as f:
            f.write(raw + extra); f.flush(); os.fsync(f.fileno())
        assert tmp.read_bytes() == raw + extra and p.read_bytes() == raw
        os.replace(tmp, p)
        assert p.read_bytes() == raw + extra
        rows.append({'before': before, 'backup': pin(bak), 'after': pin(p), 'pure_append': True})
    save('MEMORY_APPLIED_R7.json', rows)
    entry = json.loads((ROOT / 'MAP_ENTRY_R5.json').read_text(encoding='utf-8'))
    entry.update({
        'titulo': 'Lentes R7: perfis historicos e normalizacoes nao reproduzidas',
        'resultado': 'Artigo historico explicita NFW mas amplitude nao fixa;10percent e2.7kpc nao reproduzem as formulas. Fontes complementares preservadas, sem observacao composta.',
        'veredito': 'HISTORICAL_NORMALIZATION_NOT_ESTABLISHED__NO_OBSERVED_5SIGMA',
        'defeito': 'Fonte/operador espacial e contorno fisico da lente ainda nao instanciados; ramo escalar nao identifica automaticamente a1-forma.',
        'proximo_passo': 'Determinar perfil/fonte com insumo fisico sustentado; aplicar perfilamento existente somente depois. Nao repetir forecasts sem nova lei.',
        'artefatos': [str(ROOT / 'DELIVERY_R7.json'), str(folder / 'RESULTADO_FONTES_R7.txt'), str(folder / 'REVIEW_R7.json')],
        'nota': 'Revisao independente da aritmetica e dimensoes historicas; fontes adicionais conferidas. Meta5sigma incompleta.'})
    save('MAP_ENTRY_R7.json', entry)
    command('MAP_REGISTER_R7', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\MAPA_DE_ROTAS\rotas.py',
        'registrar', str(ROOT / 'MAP_ENTRY_R7.json'), '--quem', ACTOR['id']])
    command('BOARD_UPDATE_R7', [sys.executable, '-B', '-X', 'utf8', r'C:\IALD\PROGRAMA_IALD\iald.py',
        'avancar', UNIT, '--quem', ACTOR['id'], '--status', 'EM_CURSO', '--evidencia', str(ROOT / 'DELIVERY_R7.json'),
        '--nota', 'R7 revisada:10percent e2.7kpc historicos nao reproduzem; perfil/amplitude fixa de lente seguem OPEN. Sem composto.'])
    out = memory({'operation': 'transition', 'reference': ref, 'actor': ACTOR, 'expected_revision': 7,
        'event_id': 'lensing-boundary-r7-delivered', 'changes': {
            'records': [{'id': 'lensing-boundary-r7', 'kind': 'fact', 'statute': 'DERIVED',
                'sources': [{'kind': 'artifact', 'ref': str(ROOT / 'DELIVERY_R7.json'),
                             'sha256': pin(ROOT / 'DELIVERY_R7.json')['sha256']}], 'text': txt}],
            'flow': {'phase': 'historical_normalization_r7_reviewed',
                'next_action': 'R7 checked remaining historical lens normalizations; no fixed physical profile recovered. R6 metric response and R2-R4 nuisance calculations remain reusable. Revalidate whether a concrete current source or supported construction supplies the lens field; otherwise report the physical-input impasse rather than repeat forecasts. No observed5sigma; full goal incomplete.',
                'handles': []}}}, 'TRANSITION_R7')
    save('REGISTRATION_R7.json', {'status': 'PASS', 'delivery': pin(ROOT / 'DELIVERY_R7.json'),
        'memory': pin(ROOT / 'MEMORY_APPLIED_R7.json'), 'map': pin(ROOT / 'MAP_REGISTER_R7.json'),
        'board': pin(ROOT / 'BOARD_UPDATE_R7.json'), 'acom': out})
    print(json.dumps({'status': 'PASS', 'receipt': out}, ensure_ascii=False))
