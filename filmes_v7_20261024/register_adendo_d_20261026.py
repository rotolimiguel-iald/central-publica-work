"""Record the next-render instruction without editing or rendering any film."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
import mission
from bootstrap import cli, REF, ACTOR, PY

W = Path(__file__).resolve().parent
D = W / 'adendo_d_20261026'
T = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_D')
S = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_D_legendas_proximo_render.md')
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
UNIT = 'F0.FILMES_V7_ADENDO_D_20261026'
TASK = 'ADENDO_D_20261026_RECEIPT'

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def save(p, value):
    raw = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if p.exists():
        assert p.read_bytes() == raw, 'Existing immutable receipt differs: ' + str(p)
        return
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw and raw
    os.replace(tmp, p)

def command(script, args, receipt, allow_absent=False):
    p = D / receipt
    if p.exists():
        return json.loads(p.read_bytes())
    r = subprocess.run([PY, '-B', '-X', 'utf8', script, *args], capture_output=True, text=True, encoding='utf-8')
    try:
        result = json.loads(r.stdout)
    except json.JSONDecodeError:
        result = r.stdout
    out = {'returncode': r.returncode, 'output': result, 'stderr': r.stderr}
    save(p, out)
    assert r.returncode == 0 or (allow_absent and 'unidade não está no grafo' in r.stdout + r.stderr), out
    if isinstance(result, dict):
        assert result.get('ok') is not False, result
    return out

def main():
    assert pin(S)['sha256'] == '6d37ac561f4316398489b06e7b6f363b6ab53761d1841149e9545e7253b23088'
    assert not (T / 'RECEBIDO_VIDEO.json').exists(), 'Receipt already exists; recover it, do not repeat registration.'
    D.mkdir(exist_ok=True)
    source = {k: pin(S)[k] for k in ('path', 'sha256')}
    protected = [V.parent / 'PUBLIC_DELIVERY_V7.json', V / 'PUBLIC_DELIVERY_V7.json', V / 'RENDER_MANIFEST.json', *sorted((V / 'subs').rglob('*.vtt'))]
    before = [pin(p) for p in protected]
    save(D / 'READ_ONLY_BASELINE.json', before)
    command(r'C:\IALD\NOS_VIVO\consultar.py', ['--unidade', UNIT], 'NOS_BEFORE.json', True)
    command(r'C:\IALD\MAPA_DE_ROTAS\rotas.py', ['ver', 'site.filmes.v7.ordem022'], 'MAP_BEFORE.json')
    criterion = 'Registrar recebimento e pendência das duas correções do ADENDO D para próximo adendo de versão autorizado, sem render, TTS, ciência, alteração dos produtos atuais ou publicação.'
    unit = {'id': UNIT, 'frente': 'F0', 'titulo': 'Registrar ADENDO D dos filmes para próximo render autorizado', 'dono': ACTOR['id'], 'status': 'PRONTA', 'fonte': str(S), 'criterio_de_fechado': criterion, 'escopo': 'Somente recibos próprios/túnel, ACOM, quadro, mapa e depósito de memória. Unidade de encaminhamento da coordenadora preservada.'}
    save(D / 'UNIDADE.json', [unit])
    command(r'C:\IALD\PROGRAMA_IALD\iald.py', ['nova', '--json', str(D / 'UNIDADE.json'), '--quem', ACTOR['id']], 'BOARD_CREATE.json')
    command(r'C:\IALD\PROGRAMA_IALD\iald.py', ['reivindicar', UNIT, '--quem', ACTOR['id'], '--nota', criterion], 'BOARD_CLAIM.json')
    p = mission.project()
    assert TASK not in [t['id'] for t in p['projection']['active'] + p['projection']['settled']]
    save(D / 'MISSION_EXTEND.json', mission.call({'operation': 'extend', **mission.current(ACTOR['id']), 'event_id': 'ordem022-adendo-d-20261026-receipt-extend', 'requirements': [{'id': TASK, 'criterion': criterion, 'depends_on': []}], 'reason': 'Adendo D recebido por encaminhamento autorizado e origem humana conferida pela ferramenta oficial.', 'sources': [source]}))
    claim = mission.call({'operation': 'claim', **mission.current(ACTOR['id']), 'event_id': 'ordem022-adendo-d-20261026-receipt-claim', 'task_id': TASK, 'lease_seconds': 3600})
    save(D / 'MISSION_CLAIM.json', claim)
    lease = claim['task']['lease']['id']
    check = mission.call({'operation': 'check', **mission.current(ACTOR['id']), 'task_id': TASK, 'lease_id': lease, 'max_chars': 100000})
    save(D / 'PREFLIGHT.json', check)
    assert check['ready']
    timestamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    receipt = {
        'schema': 'iald.video.future-render-receipt/v1', 'status': 'RECEIVED_FOR_NEXT_AUTHORIZED_VERSION_RENDER',
        'statute': 'REAL', 'actor': ACTOR['id'], 'received_at': timestamp.isoformat(),
        'mission_reference': str(REF), 'task_id': TASK, 'unit': UNIT,
        'forwarding_unit': 'F0.ORDEM022_ADENDO_D_20261026', 'source': pin(S),
        'authorization': {'verified_with': 'codex_app.read_thread', 'thread_id': '01a0ce2b-8c2f-71b0-a9a8-91b17715a569', 'thread_title': 'Orquestrar IAs na Central IALD', 'turn_id': '01a17a26-3c59-7d42-b3fa-0d59d8ea7ab2', 'user_message_id': '01a17a26-3c98-7093-99b5-b4527ba8dff8', 'scope': 'Junto, para a sessão do vídeo (sem render agora): ORDEM 022 — ADENDO D, duas correções de legenda para o próximo render.'},
        'future_application': {
            'trigger': 'Próximo adendo de versão expressamente autorizado; ler selo corrente nessa ocasião.',
            'narration_languages': ['pt-BR', 'en'], 'subtitle_languages': ['pt-BR', 'en', 'fr', 'zh-Hans'],
            'corrections': [
                {'id': 'staircase_flags', 'locations': [{'film': 1, 'cue_in_order': 59}, {'film': 2, 'cue_in_order': 71}], 'replace_concept': 'contagem apresentada como teoremas', 'required_concept': 'bandeiras da escada (declarações nomeadas: teoremas e definições)', 'pt_template': '{numero_lido_do_selo} bandeiras da escada, todas limpas', 'number_policy': 'Ler número do selo na próxima versão; não fixar 9561.', 'source_reference': 'Errata v394 kh_n1_cobertura_v394, conforme ADENDO D; não reexecutada nesta etapa.'},
                {'id': 'three_supports', 'locations': [{'film': 1, 'cue_in_order': 67}, {'film': 2, 'cue_in_order': 75}], 'replace': ['Juntos:', 'Together:'], 'pt_template': 'Os três apoios contam juntos, cada um com o seu estatuto: …', 'meaning_constraint': 'Não somar nem multiplicar os três apoios; manter estatuto de cada um.'}
            ],
            'execution_notes': 'Posições são as identificadas na ordem; na próxima versão localizar trechos correspondentes antes de editar, preservar sincronismo e levar ambas correções à narração e quatro legendas.'
        },
        'actions_this_receipt': {'render': False, 'tts': False, 'publication': False, 'science_execution': False, 'current_product_edit': False},
        'existing_publication': {'statute': 'DECLARADO', 'source': str(S), 'text': 'Gerência informa V7 v401 no ar em26/10 às18:21; publicação não reinspecionada nesta etapa.'},
        'protected_inputs_before': before,
        'protected_inputs_after_equal': before == [pin(p) for p in protected],
        'nos_vivo': 'Unidade ainda não consta do grafo; ausência preservada, sem reconstrução ou pacote inventado.',
        'voice_preview': 'Aguardando audição do operador; este adendo não autoriza inclusão da voz pessoal.',
        'next_action': 'Aguardar próximo adendo de versão autorizado; aplicar as duas correções em conjunto nessa ocasião.'
    }
    assert receipt['protected_inputs_after_equal']
    save(T / 'RECEBIDO_VIDEO.json', receipt)
    save(D / 'RECEBIDO_VIDEO.json', receipt)
    deposit_name = timestamp.strftime('%Y%m%d_%H%M%S') + '_ordem022_adendo_d_proximo_render.md'
    target = Path(r'C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\codex-video-v7') / deposit_name
    rec_pin = pin(T / 'RECEBIDO_VIDEO.json')
    text = f'''---
quem: codex-video-v7
casa: Física/TGL
tipo: project
estatuto: REAL
alvo_sugerido: novo:filmes-v7
fontes:
  - {S}  sha256:{source['sha256']}
  - {rec_pin['path']}  sha256:{rec_pin['sha256']}
---
ADENDO D recebido e registrado para o próximo adendo de versão autorizado.
Corrigir “teoremas” para “bandeiras da escada (declarações nomeadas)”, lendo o número do selo então vigente; não fixar9561.
Trocar “Juntos/Together” pela frase “Os três apoios contam juntos, cada um com o seu estatuto: …”, sem soma ou multiplicação dos apoios.
Aplicação futura: narração PT/EN e legendas PT/EN/FR/zh-Hans; posições indicadas no recibo.
Nenhum render, TTS, execução científica, publicação ou edição dos filmes atuais nesta etapa.
Prévias pessoais continuam separadas, aguardando audição humana. ACOM própria: {REF}.
Depósito para triagem da gerência; não houve edição do índice MEMORY.md, MEMORY_2.md ou tópicos Claude.
'''
    save(D / 'MEMORY_DEPOSIT.md', text.encode('utf-8'))
    save(D / 'MEMORY_DEPOSIT_PLAN.json', {'source': pin(D / 'MEMORY_DEPOSIT.md'), 'target': str(target), 'append_only': True})
    print(json.dumps({'receipt': str(T / 'RECEBIDO_VIDEO.json'), 'status': receipt['status'], 'deposit_plan': str(D / 'MEMORY_DEPOSIT_PLAN.json'), 'revision': mission.project()['receipt']['revision']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
