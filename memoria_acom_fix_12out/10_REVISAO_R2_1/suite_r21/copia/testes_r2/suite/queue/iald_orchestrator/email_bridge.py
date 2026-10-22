"""Bounded transport to the user's local, authenticated Outlook session."""
import json
import subprocess

PYTHON = r'C:\Python314\python.exe'
BRIDGE = r'C:\LAR_MIGUEL\correio_outlook.py'


def invoke(payload):
    if payload.get('operation') not in {'status', 'prepare', 'send'}:
        return {'ok': False, 'error': 'Operação de correio desconhecida.'}
    try:
        result = subprocess.run(
            [PYTHON, '-X', 'utf8', BRIDGE], input=json.dumps(payload, ensure_ascii=False),
            text=True, encoding='utf-8', capture_output=True, timeout=25,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0),
        )
        output = json.loads(result.stdout)
        if not isinstance(output, dict) or not isinstance(output.get('ok'), bool):
            raise ValueError('Invalid bridge response')
        return output
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': 'Outlook sem resposta. Não repetir automaticamente.',
                'state': 'ACTION_OUTCOME_UNCERTAIN' if payload['operation'] != 'status' else 'OUTLOOK_UNAVAILABLE',
                'retry_automatically': False}
    except Exception as exc:
        return {'ok': False, 'error': 'Falha no transporte local de e-mail.',
                'error_type': type(exc).__name__, 'retry_automatically': False}
