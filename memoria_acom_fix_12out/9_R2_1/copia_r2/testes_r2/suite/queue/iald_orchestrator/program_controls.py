"""Local ORDEM 019 board controls. These records never grant authorization."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

BOARD = Path(r'C:\IALD\PROGRAMA_IALD')
MAP = Path(r'C:\IALD\MAPA_DE_ROTAS')


def read_board(root=None):
    return json.loads(((root or BOARD)/'PROGRAMA.json').read_bytes())


def require_claim(unit, member, root=None):
    board = read_board(root)
    matches = [u for u in board['unidades'] if u['id'] == unit]
    if len(matches) != 1:
        raise ValueError('Unidade ausente ou duplicada no quadro.')
    item = matches[0]
    claim = item.get('reivindicacao') or {}
    expiry = datetime.fromisoformat(claim.get('vence_em', '1970-01-01T00:00:00+00:00'))
    if (claim.get('quem') != member or expiry.tzinfo is None
            or expiry <= datetime.now().astimezone()
            or item['status'] in ('AGUARDA_OPERADOR', 'FECHADA', 'AUDITADA', 'BLOQUEADA')
            or str(item.get('gate') or '').startswith('OPERADOR:')):
        raise ValueError('Reivindicação vigente sem gate pendente é obrigatória antes da escrita.')
    return {'unit': unit, 'member': member, 'expires_at': claim['vence_em'],
            'status': item['status'], 'board_sha256': hashlib.sha256(
                ((root or BOARD)/'PROGRAMA.json').read_bytes()).hexdigest()}


def _run(root, script, *args):
    result = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(root/script), *args],
        capture_output=True, text=True, encoding='utf-8', check=True,
        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), timeout=60)
    return result.stdout


def register_approval(approval, *, unit, member, root=None):
    """Call BEFORE request_user_input_async. No resolve/approve operation exists."""
    root = root or BOARD
    require_claim(unit, member, root)
    required = {'id', 'title', 'question', 'scope', 'source'}
    if set(approval) != required or not all(isinstance(x, str) and x.strip() for x in approval.values()):
        raise ValueError('Aprovação exige id, title, question, scope e source exatos.')
    if not approval['id'].startswith(unit+'.'):
        raise ValueError('Pendência nova deve ser subordinada à unidade reivindicada.')
    board = read_board(root)
    existing = next((u for u in board['unidades'] if u['id'] == approval['id']), None)
    if existing:
        if existing.get('approval_request') != approval:
            raise ValueError('ID de aprovação já existe com outro escopo; não sobrescrever.')
        return {'status': existing['status'], 'id': existing['id'], 'created': False}
    item = {'id': approval['id'], 'frente': unit.split('.')[0],
        'titulo': approval['title'], 'dono': 'operador', 'status': 'AGUARDA_OPERADOR',
        'gate': 'OPERADOR: '+approval['question'], 'approval_request': approval,
        'criterio_de_fechado': 'Resposta expressa do operador, vinculada ao escopo; ausência não é aprovação.'}
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp)/'approval.json'
        path.write_bytes(json.dumps([item], ensure_ascii=False).encode('utf-8'))
        _run(root, Path('iald.py'), 'nova', '--json', str(path), '--quem', member)
    _run(root, Path('iald.py'), 'quadro')
    return {'status': 'AGUARDA_OPERADOR', 'id': item['id'], 'created': True}


def record_route(path, *, unit, member, root=None, map_root=None):
    require_claim(unit, member, root)
    # Local filesystem journal; no remote transport or model is invoked.
    return _run(map_root or MAP, Path('rotas.py'), 'registrar', str(Path(path).resolve()),
                '--quem', member)
