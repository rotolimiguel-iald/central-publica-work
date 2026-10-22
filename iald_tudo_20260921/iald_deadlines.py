"""Read-only operational deadlines. Never read or expose credential values."""
from datetime import datetime, timezone
import json
import math
from pathlib import Path

LABELS = {'anthropic_key': 'Chave Claude', 'openai_key': 'Chave ChatGPT',
          'testflight_internal': 'TestFlight interno', 'testflight_external': 'TestFlight convidados'}

def snapshot(path, now=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        raise ValueError('A timezone-aware clock is required')
    error = None
    try:
        raw = json.loads(Path(path).read_bytes())
        if not isinstance(raw, dict) or not isinstance(raw.get('items'), dict):
            raise ValueError('Invalid deadline document')
    except (OSError, ValueError):
        raw = {'items': {}}
        error = 'Não foi possível ler os prazos; confira o cadastro no servidor.'
    items = []
    for ident, label in LABELS.items():
        entry = raw['items'].get(ident, {})
        entry = entry if isinstance(entry, dict) else {}
        expires = entry.get('expires_at')
        row = {'id': ident, 'label': label, 'expires_at': None, 'days_remaining': None,
               'level': 'unknown', 'message': 'Vencimento não informado — conferir no provedor.'}
        if expires:
            try:
                deadline = datetime.fromisoformat(expires.replace('Z', '+00:00'))
                if deadline.tzinfo is None:
                    raise ValueError('Timezone missing')
                seconds = (deadline-now).total_seconds()
                days = max(0, math.ceil(seconds/86400))
                level = ('expired' if seconds <= 0 else 'critical' if days <= 3
                         else 'warning' if days <= 14 else 'attention' if days <= 30 else 'ok')
                threshold = next((n for n in (1, 3, 7, 14, 30) if days <= n), None)
                row.update(expires_at=deadline.isoformat(), days_remaining=days, level=level,
                           alert_threshold_days=threshold,
                           message='Vencido — renovar para restabelecer o serviço.' if seconds <= 0 else
                           ('Vence em menos de 24 horas — renovar.' if seconds < 86400 else
                            f'Faltam {days} dias.' + (' Planeje a renovação.' if days <= 30 else '')))
            except (ValueError, TypeError, AttributeError, OverflowError):
                row['message'] = 'Data inválida — conferir no provedor.'
        items.append(row)
    return {'checked_at': now.isoformat(), 'items': items, 'error': error,
            'note': 'Datas registradas pelo operador. Revogação e saldo podem interromper o serviço antes do vencimento.'}
