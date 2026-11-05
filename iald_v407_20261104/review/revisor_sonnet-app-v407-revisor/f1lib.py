"""Revisor sonnet-app-v407-revisor -- minha propria implementacao da regra F1 (registro de estatuto plano) e da classificacao de diferencas de bloco.
Independente de haiku_codec: a regra e' a do briefing (dict plano, so escalares, nao vazio, chave /status|estatuto|verdict|veredito/i, <= 500 B de JSON compacto)."""
import json, re
import lib405 as L

STATUS_KEY = re.compile(r'status|estatuto|verdict|veredito', re.I)
MAXB = 500
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
# chaves de qualificador (as do molde) -- usadas para dizer se uma perda de literal e' epistemica ou so' auxiliar
QK = re.compile(r'status|statute|estatuto|verdict|veredit|scope|escopo|limites|^diz$|^nao_diz$|theorem|hypothes|hip[oó]tes|formula|equation|equacao|claim|statement|enunciad|not_claimed|not_said|declar|conditional|condicional|caveat|unconditional', re.I)


def is_status_record(key, item):
    return (isinstance(item, dict) and bool(item) and STATUS_KEY.search(str(key)) is not None
            and all(not isinstance(v, (dict, list)) for v in item.values()) and len(dump(item)) <= MAXB)


def is_flat_status_dict_any_size(key, item):
    return (isinstance(item, dict) and bool(item) and STATUS_KEY.search(str(key)) is not None and all(not isinstance(v, (dict, list)) for v in item.values()))


def esc(k):
    return str(k).replace('~', '~0').replace('/', '~1')


def walk(node, ptr, pred, depth=1):
    """Yield (pointer, key, value) for every node at depth>=1 satisfying pred(key, value); does not descend into a match."""
    if isinstance(node, dict):
        for k, v in node.items():
            p = ptr + '/' + esc(k)
            if pred(k, v):
                yield (p, k, v)
            else:
                yield from walk(v, p, pred, depth + 1)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, ptr + '/' + str(i), pred, depth + 1)


def status_records(core_topic, topic):
    return list(walk(core_topic, '/core/' + topic, is_status_record))


def classify(topic, core_topic, dn_new, dn_old):
    """Compare what the model SEES literally (leaves outside pointers) in the new block against the old block, for a topic whose sealed source is unchanged.
    -> dict(kind=IDENTICAL | F1_GAIN_ONLY | F1_GAIN_AND_REPRESENTATION | UNEXPLAINED, gained, lost, ...)"""
    if L.canon(dn_new) == L.canon(dn_old):
        return {'kind': 'IDENTICAL'}
    ln = L.literal_leaves(dn_new, '/core/' + topic)
    lo = L.literal_leaves(dn_old, '/core/' + topic)
    gained = sorted(p for p, v in ln.items() if lo.get(p) != v)
    lost = sorted(p for p, v in lo.items() if ln.get(p) != v)
    recs = [r[0] for r in status_records(core_topic, topic)]
    unexpl_gain = [p for p in gained if not any(p == r or p.startswith(r + '/') for r in recs)]
    row = {'gained': len(gained), 'lost': len(lost), 'gained_not_in_status_records': unexpl_gain[:6], 'lost_sample': lost[:6]}
    new_cap = L.is_ref(dn_new) and dn_new.get('@') == ''
    old_cap = L.is_ref(dn_old) and dn_old.get('@') == ''
    row.update(new_capsule=bool(new_cap), old_capsule=bool(old_cap))
    if unexpl_gain:
        row['kind'] = 'UNEXPLAINED'
        return row
    if not lost:
        row['kind'] = 'F1_GAIN_ONLY' if gained else 'REPRESENTATION_ONLY'
        return row
    # perdas de literal: epistemicas (qualificador) ou so' auxiliares/hashes?
    lost_q = [p for p in lost if QK.search(p.split('/')[3] if p.count('/') >= 3 else '')]
    row.update(lost_epistemic=lost_q[:6], n_lost_epistemic=len(lost_q))
    row['kind'] = 'F1_GAIN_AND_REPRESENTATION' if (new_cap and not old_cap and not lost_q) else 'UNEXPLAINED'
    return row
