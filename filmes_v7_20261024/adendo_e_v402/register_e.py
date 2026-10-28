"""Register the human-authorized v402 update without mutating film sources."""
from pathlib import Path
import hashlib, json, sys

E = Path(__file__).resolve().parent
W = E.parent
sys.path.insert(0, str(W))
import mission

ORDER = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_E_render_v402_autorizado.md')
CORRECTIONS = ORDER.with_name('ORDEM_022_ADENDO_D_legendas_proximo_render.md')
N = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
ACTOR = 'codex-video-v7'

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def save(name, value):
    p = E / name
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    if p.exists():
        assert p.read_bytes() == raw, 'Existing receipt differs: ' + str(p)
        return
    tmp = p.with_suffix(p.suffix + '.tmp')
    tmp.write_bytes(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)

def main():
    assert not (E / 'REGISTRATION_COMPLETE.json').exists(), 'Recover, do not register again'
    seal = json.loads((N / 'um_absoluto_selo.json').read_bytes())
    assert seal['um_version'] == 'v402', 'STOP: authorized source changed'
    assert pin(N / 'um.py')['sha256'] == seal['sha256']['um.py']
    assert pin(ORDER)['sha256'] == '3217e11e52af6ab88d7611329eee18daff9307f5ce745665452945d0b5e20ba1'
    save('SOURCE_INTAKE.json', {'order': pin(ORDER), 'corrections': pin(CORRECTIONS),
         'sources': [pin(N / name) for name in ('um.py', 'um_absoluto_selo.json', 'um_absoluto.json')],
         'version': seal['um_version'], 'timestamp': seal['timestamp']})
    save('HUMAN_AUTHORIZATION.json', {'origin_thread': '01a0ce2b-8c2f-71b0-a9a8-91b17715a569',
         'verified_using': 'mcp__codex_app__read_thread', 'role': 'user',
         'verbatim': 'Autorizo diretamente o encaminhamento do Adendo E à sessão do vídeo para iniciar o render V7 da v402, com as correções do Adendo D e sem publicação pela sessão.'})
    requirements = [
        {'id': 'ADENDO_E_V402', 'criterion': 'Integrar e renderizar V7 da v402 sob Adendo E e correções D; comparar exatamente números contra v401, parar em outra divergência ou avanço do selo; entregar manifestos e recibos sem publicação ou voz pessoal não aprovada.', 'depends_on': []},
        {'id': 'V402_DATA', 'criterion': 'Copiar fontes v402 em isolamento, importar somente cópia, exportar e comparar todos os números; aceitar somente mudanças autorizadas E; replay offline e controles negativos; fontes originais intactas.', 'depends_on': []},
        {'id': 'V402_AUDIO', 'criterion': 'Atualizar narração EN/PT e quatro legendas para contagens v402 e duas correções D; duração/timing/loudness conferidos; Edge público autorizado, recibos idempotentes; sem voz pessoal.', 'depends_on': []},
        {'id': 'V402_MEDIA', 'criterion': 'Preparar e concluir uma captura por filme/loop e exportações V7, frames/decodificação/dimensões/áudio e pinos conferidos; backups da v401, sem publicação; coordenador inicia browser apenas após freeze.', 'depends_on': []},
    ]
    sources = [{k: pin(p)[k] for k in ('path', 'sha256')} for p in (ORDER, CORRECTIONS, E/'HUMAN_AUTHORIZATION.json')]
    result = mission.call({'operation': 'extend', **mission.current(ACTOR),
        'event_id': 'ordem022-adendo-e-v402-extend', 'requirements': requirements,
        'reason': 'Adendo E de versão autorizado diretamente pelo operador, preservados os recibos e requisitos históricos.', 'sources': sources})
    save('MISSION_EXTEND.json', result)
    result = mission.call({'operation': 'claim', **mission.current(ACTOR),
        'task_id': 'ADENDO_E_V402', 'lease_seconds': 43200, 'event_id': 'ordem022-adendo-e-v402-parent-claim'})
    save('MISSION_PARENT_CLAIM.json', result)
    p = mission.project()
    t = next(t for t in p['projection']['active'] if t['id'] == 'ADENDO_E_V402')
    result = mission.call({'operation': 'check', **mission.current(ACTOR), 'task_id': t['id'], 'lease_id': t['lease']['id'], 'max_chars': 100000})
    assert result['ready']
    save('MISSION_PARENT_PREFLIGHT.json', result)
    save('REGISTRATION_COMPLETE.json', {'status': 'READY', 'tasks': [r['id'] for r in requirements], 'preflight_revision': result.get('receipt', {}).get('revision'), 'source': pin(E/'SOURCE_INTAKE.json')})
    print(json.dumps({'status': 'READY', 'tasks': [r['id'] for r in requirements]}))

if __name__ == '__main__':
    main()
