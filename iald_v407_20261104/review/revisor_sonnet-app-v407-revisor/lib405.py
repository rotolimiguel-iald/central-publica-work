"""Reviewer (sonnet-app-v405-revisor) helper: generic, independent prefix parser/decoder parameterised by (prefix text, sealed result).
Same semantics as r3_topics_capsules.py but usable for the INSTALLED v404 prefixes too. Does not import haiku_codec / fit_*."""
import json, re, hashlib
from pathlib import Path

MARK = '## Exposição canônica integral: fórmulas e derivações'
AUD = 'AUDIT_BOOLEAN_FIELDS_IN_SOURCE'
ALIAS = {'"@F"': '"@SOURCE_FIELDS"', '"@I"': '"@SOURCE_ITEMS"', '"@L"': '"@TGL_LITERAL"', '"@Y"': '"@SUMMARY"', '"@X"': '"@EXPOSITION"'}
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def unalias(s):
    for sh_, lg in ALIAS.items():
        s = s.replace(sh_, lg)
    return s


def resolve(v, ptr):
    if ptr == '':
        return v
    assert ptr.startswith('/'), ptr
    for part in ptr.split('/')[1:]:
        k = part.replace('~1', '/').replace('~0', '~')
        v = v[int(k)] if isinstance(v, list) else v[k]
    return v


def child(p, k):
    return p + '/' + str(k).replace('~', '~0').replace('/', '~1')


def unpack(v):
    if isinstance(v, list):
        return [unpack(x) for x in v]
    if not isinstance(v, dict):
        return v
    out = {k: unpack(x) for k, x in v.items() if k not in ('@SOURCE_FIELDS', '@SOURCE_ITEMS')}
    if '@SOURCE_FIELDS' in v:
        for k in v['@SOURCE_FIELDS']:
            out[k] = {'@': '/' + k}
    if '@SOURCE_ITEMS' in v:
        for k, n in v['@SOURCE_ITEMS'].items():
            out[k] = {'@': '/' + k, 'items': n}
    return out


class Summ:
    def __init__(self, ptr, a, n, topic=None):
        self.ptr, self.a, self.n, self.topic = ptr, a, n, topic

    def key(self):
        return ('S', self.ptr, self.a, self.n, self.topic)


def dec_lit(v, D, E):
    if isinstance(v, list):
        return [dec_lit(x, D, E) for x in v]
    if not isinstance(v, dict):
        return v
    ks = set(v)
    if ks == {'@concat'}:
        return ''.join(dec_lit(x, D, E) for x in v['@concat'])
    if ks == {'@upper'}:
        return v['@upper'].upper()
    if ks == {'@enum'}:
        return v['@enum'].upper().replace(' ', '_')
    if ks == {'@TGL_LITERAL'}:
        return dec_lit(D[v['@TGL_LITERAL']], D, E)
    if ks == {'@EXPOSITION'}:
        s, l = v['@EXPOSITION']
        return E[s:s + l]
    if ks == {'@SUMMARY'} and isinstance(v['@SUMMARY'], list):
        return Summ(v['@SUMMARY'][0], v['@SUMMARY'][1], v['@SUMMARY'][2])
    if ks == {'@SUMMARY', 'source_pointer', 'span'}:
        return Summ(v['source_pointer'], v['span'][0], v['span'][1], v['@SUMMARY'])
    return {k: dec_lit(x, D, E) for k, x in v.items()}


def restore(v, src, cur, rep, E=''):
    if isinstance(v, Summ):
        topic = cur.split('/')[2]
        root = '/core/' + topic
        ptr = v.ptr if v.ptr.startswith('/core/') else root + v.ptr
        piece = E[v.a:v.a + v.n]
        assert piece.startswith('**Estatutos [' + topic + ']**'), ('stale summary', cur)
        return resolve(src, ptr)
    if isinstance(v, dict) and '@' in v:
        assert set(v) <= {'@', 'fields', 'items', 'true_fields', 'false_fields'}, ('unknown meta', sorted(v))
        actual = resolve(src, cur)
        assert v['@'] == cur[len(cur) - len(v['@']):] if v['@'] else True
        for suf, val in v.get('fields', {}).items():
            fv = restore(val, src, cur + suf, rep, E)
            assert resolve(actual, suf) == fv, ('field differs', cur, suf)
            rep.append((cur + suf, fv))
        if 'items' in v:
            assert len(actual) == v['items'], ('items', cur)
        if 'true_fields' in v:
            assert v['true_fields'] == sum(actual.values()) and v['false_fields'] == len(actual) - sum(actual.values())
        return actual
    if isinstance(v, dict):
        return {k: restore(x, src, child(cur, k), rep, E) for k, x in v.items()}
    if isinstance(v, list):
        return [restore(x, src, child(cur, i), rep, E) for i, x in enumerate(v)]
    return v


def parse_prefix(text):
    head, sep, expo_part = text.partition(MARK)
    head = unalias(head)
    D = {}
    E = ''
    m = re.search(r'(?:DICIONÁRIO DE LITERAIS|LITERAIS_COMPARTILHADOS)\n(\{.*\})\n', head)
    if m:
        D = json.loads(m.group(1))
    m2 = re.search(r'DICIONÁRIO DE INDICADORES LITERAIS\n(\{.*\})\n', head)
    FL = json.loads(m2.group(1)) if m2 else {}
    if '<EXPOSICAO_CANONICA>\n' in expo_part:
        E = expo_part.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    hs = list(re.finditer(r'(?m)^### ([^\n]+)\n', head))
    body = {}
    for i, h in enumerate(hs):
        stop = hs[i + 1].start() if i + 1 < len(hs) else len(head)
        body[h[1]] = head[h.end():stop]
    return {'head': head, 'D': D, 'FL': FL, 'E': E, 'body': body}


def first_json_line(seg):
    lines = [l for l in seg.split('\n') if l.strip() and not l.startswith('Fonte:')]
    return lines[0] if lines else None


def decode_block(P, n):
    """-> ('JSON', dv) | ('TEXT', text). dv still contains reference nodes ({'@':..}) and Summ objects."""
    seg = P['body'][n]
    line = first_json_line(seg)
    if line is None:
        return 'TEXT', ''
    try:
        v = json.loads(line)
    except Exception:
        return 'TEXT', seg.strip()
    if isinstance(v, dict) and '@B' in v:
        ident = str(v.pop('@B'))
        v.update(P['FL'][ident])
    return 'JSON', dec_lit(unpack(v), P['D'], P['E'])


def canon(x):
    """JSON-comparable canonical form of a decoded block (Summ -> tuple)."""
    if isinstance(x, Summ):
        return list(x.key())
    if isinstance(x, dict):
        return {k: canon(y) for k, y in x.items()}
    if isinstance(x, list):
        return [canon(y) for y in x]
    return x


def catalog_full(dv, src):
    """Merge the booleans that only the AUDIT capsule carries back from the SEALED source (independent recomputation)."""
    cap = dv.get(AUD)
    if cap is None:
        return dv
    lit = {k: x for k, x in dv.items() if k != AUD}
    lit_bool = {k for k, x in lit.items() if type(x) is bool}
    full = dict(lit)
    for k, x in src.items():
        if type(x) is bool and k not in lit_bool:
            full[k] = x
    return full


def leaves(v, p=''):
    if isinstance(v, dict):
        for k, x in v.items():
            yield from leaves(x, child(p, k))
    elif isinstance(v, list):
        for i, x in enumerate(v):
            yield from leaves(x, child(p, i))
    else:
        yield p, v


def is_ref(x):
    return isinstance(x, dict) and '@' in x


def literal_leaves(dv, p=''):
    """Leaves the model SEES literally: leaves outside reference nodes, plus the 'fields' entries of reference nodes (path = ref path + suffix).
    Returns {path: json-dumped value}. Summ objects are returned as pointer-only markers (not literal)."""
    out = {}
    if isinstance(dv, Summ):
        out[p] = 'SUMMARY_REF:' + dv.ptr
        return out
    if is_ref(dv):
        for suf, val in dv.get('fields', {}).items():
            out.update(literal_leaves(val, p + suf))
        for k, x in dv.items():
            if k not in ('@', 'fields', 'items', 'true_fields', 'false_fields'):
                out.update(literal_leaves(x, p + '/' + k.replace('~', '~0').replace('/', '~1')))
        return out
    if isinstance(dv, dict):
        for k, x in dv.items():
            out.update(literal_leaves(x, child(p, k)))
    elif isinstance(dv, list):
        for i, x in enumerate(dv):
            out.update(literal_leaves(x, child(p, i)))
    else:
        out[p] = json.dumps(dv, ensure_ascii=False)
    return out
