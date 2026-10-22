"""Independent, offline, read-only review of the prepared scientific release."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import unquote, urlparse
import ast
import hashlib
import json
import os
import re

WORK = Path(__file__).resolve().parents[1]
STAGE = WORK / 'memory_stage'
APP = Path('C:/IALD/projetos_pyhton/IALD')
VAULT = Path('C:/IALD/Central de Patentes/vault/originals_copy')
MARKER = '## Exposição canônica integral: fórmulas e derivações'
inputs, checks, findings = {}, [], []
stats = Counter()
BOOLEAN_DICTIONARY = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    path = Path(path)
    raw = path.read_bytes()
    key = str(path)
    pin = {'sha256': sha(raw), 'bytes': len(raw)}
    if key in inputs:
        assert inputs[key] == pin, 'Input changed while reading: ' + key
    inputs[key] = pin
    return raw

def pairs(rows):
    out = {}
    for key, value in rows:
        assert key not in out, 'Duplicate JSON key: ' + key
        out[key] = value
    return out

def loads(raw):
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))

def load(path):
    return loads(read(path))

def same(a, b):
    return json.dumps(a, sort_keys=True, ensure_ascii=False) == json.dumps(b, sort_keys=True, ensure_ascii=False)

def child(pointer, key):
    return pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')

def resolve(root, pointer):
    assert pointer == '' or pointer.startswith('/'), pointer
    for part in pointer.split('/')[1:]:
        assert not re.search('~(?![01])', part), pointer
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(root, list):
            assert re.fullmatch('0|[1-9][0-9]*', key), pointer
            root = root[int(key)]
        else:
            root = root[key]
    return root

def check(name, ok, evidence=None):
    checks.append({'name': name, 'passed': bool(ok), 'evidence': evidence})

def topics(text, names=None):
    body = text.split(MARKER, 1)[0]
    headers = list(re.finditer(r'(?m)^### ([^\n]+)\n', body))
    result = {}
    for i, h in enumerate(headers):
        name = h[1].split(' — ', 1)[0]
        if names is not None and name not in names:
            continue
        end = headers[i+1].start() if i+1 < len(headers) else len(body)
        block = body[h.end():end].split('\n## ', 1)[0].strip()
        assert name not in result, name
        result[name] = block
    return result

def reconstruct(node, source, topic, pointer, represented, partial=False):
    expected = resolve(source, pointer)
    if isinstance(node, dict):
        tags = [t for t in ('same_as', 'SOURCE_RELATIVE', 'DETAILS_IN_SOURCE', '@') if t in node]
        if tags:
            assert len(tags) == 1, pointer
            tag = tags[0]
            target = topic + node[tag] if tag in ('SOURCE_RELATIVE', '@') else node[tag]
            actual = resolve(source, target)
            assert same(actual, expected), 'Wrong reference target: ' + pointer
            if tag != 'same_as':
                assert target == pointer, 'Misplaced reference: ' + pointer
            stats['references_' + tag] += 1
            if 'items' in node:
                assert type(node['items']) is int and len(actual) == node['items'], pointer
            if 'true_fields' in node or 'false_fields' in node:
                assert all(type(x) is bool for x in actual.values()), pointer
                assert node['true_fields'] == sum(actual.values()), pointer
                assert node['false_fields'] == len(actual)-sum(actual.values()), pointer
            for suffix, value in node.get('fields', {}).items():
                assert same(resolve(actual, suffix), value), pointer + suffix
                represented[pointer + suffix] = value
            for key, value in node.get('semantic_fields', {}).items():
                reconstruct(value, source, topic, child(pointer, key), represented)
            for index, value in enumerate(node.get('first_records', [])):
                reconstruct(value, source, topic, child(pointer, index), represented)
            metadata = {tag, 'items', 'fields', 'semantic_fields', 'first_records', 'role', 'true_fields', 'false_fields'}
            for key, value in node.items():
                if key not in metadata:
                    reconstruct(value, source, topic, child(pointer, key), represented)
            return actual
        assert isinstance(expected, dict), pointer
        if partial:
            assert set(node) <= set(expected), pointer
        else:
            assert set(node) == set(expected), 'Field coverage: ' + pointer
        return {k: reconstruct(v, source, topic, child(pointer, k), represented, partial) for k, v in node.items()}
    if isinstance(node, list):
        assert isinstance(expected, list) and len(node) == len(expected), pointer
        return [reconstruct(v, source, topic, child(pointer, i), represented, partial) for i, v in enumerate(node)]
    assert same(node, expected), 'Literal changed: ' + pointer
    represented[pointer] = node
    return node

def decode(node, dictionary, exposition, source, topic=None):
    if isinstance(node, list):
        return [decode(x, dictionary, exposition, source, topic) for x in node]
    if not isinstance(node, dict):
        return node
    if set(node)=={'@upper'}:
        assert isinstance(node['@upper'],str)
        return node['@upper'].upper()
    if set(node)=={'@concat'}:
        assert isinstance(node['@concat'],list)
        parts=[decode(x,dictionary,exposition,source,topic) for x in node['@concat']]
        assert all(isinstance(x,str) for x in parts)
        return ''.join(parts)
    if set(node)=={'@enum'}:
        label=node['@enum']
        assert isinstance(label,str) and re.fullmatch('[a-z0-9 ]+',label)
        stats['lossless_enum_labels'] += 1
        return label.upper().replace(' ','_')
    aliases = {'@F':'@SOURCE_FIELDS','@I':'@SOURCE_ITEMS','@L':'@TGL_LITERAL','@Y':'@SUMMARY','@X':'@EXPOSITION'}
    expanded = {aliases.get(k,k):v for k,v in node.items()}
    assert len(expanded)==len(node), 'Conflicting metadata aliases'
    node = expanded
    if '@B' in node:
        flags = BOOLEAN_DICTIONARY[node.pop('@B')]
        assert all(type(v) is bool for v in flags.values()) and not set(flags)&set(node)
        node.update(flags)
        stats['literal_boolean_groups'] += 1
    if set(node) == {'@TGL_LITERAL'}:
        stats['haiku_literal_references'] += 1
        return decode(dictionary[node['@TGL_LITERAL']],dictionary,exposition,source,topic)
    if isinstance(node.get('@SUMMARY'),list):
        assert set(node)=={'@SUMMARY'}, 'Unexpected compact-summary metadata'
        parts=node['@SUMMARY']
        assert len(parts) in (3,4), 'Invalid compact summary'
        if len(parts)==3:
            assert topic in source['core'], 'Current topic required for compact summary'
            relative,start,size=parts;label=topic
        else:
            label,relative,start,size=parts
            assert topic is None or topic==label, 'Summary topic mismatch'
        assert isinstance(label,str) and label in source['core']
        assert isinstance(relative,str) and (relative=='' or relative.startswith('/'))
        assert type(start) is int and type(size) is int
        pointer='/core/'+label+relative
        resolve(source,pointer)
        node={'@SUMMARY':label,'source_pointer':pointer,'span':[start,size]}
        stats['compact_summary_expansions'] += 1
    if '@EXPOSITION' in node or '@SUMMARY' in node:
        start, size = node.get('span', node.get('@EXPOSITION'))
        assert type(start) is int and type(size) is int and 0 <= start < start+size <= len(exposition)
        text = exposition[start:start+size]
        if '@SUMMARY' in node:
            assert text.startswith('**Estatutos [' + node['@SUMMARY'] + ']**')
            stats['haiku_summary_references'] += 1
            # A documented summary is not equated to its literal source value.
            return resolve(source, node['source_pointer'])
        if 'starts_with' in node:
            assert text.startswith(decode(node['starts_with'],dictionary,exposition,source,topic))
        stats['haiku_exposition_references'] += 1
        return text
    out = {k: decode(v, dictionary, exposition, source, topic) for k, v in node.items()
           if k not in ('@SOURCE_FIELDS', '@SOURCE_ITEMS')}
    for tag in ('@SOURCE_FIELDS', '@SOURCE_ITEMS'):
        for key in node.get(tag, []):
            assert key not in out and '/' not in key and '~' not in key
            out[key] = {'@': '/' + key}
            if tag == '@SOURCE_ITEMS':
                out[key]['items'] = node[tag][key]
    return out

def important(value, pointer=''):
    out = {}
    if isinstance(value, dict):
        for key, item in value.items():
            if key == 'checks':
                continue
            p = child(pointer, key)
            if re.search('statut|status|scope|escopo|hypothes|hip[oó]tes|not_claimed|not_said|verdict|veredito', key, re.I):
                out[p] = item
            else:
                out.update(important(item, p))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            out.update(important(item, child(pointer, i)))
    return out

def covered(pointer, value, represented):
    if pointer in represented:
        return same(value, represented[pointer])
    for p, v in represented.items():
        if pointer.startswith(p + '/') and same(resolve(v, pointer[len(p):]), value):
            return True
    if isinstance(value, dict):
        return all(covered(child(pointer, k), v, represented) for k, v in value.items())
    if isinstance(value, list):
        return all(covered(child(pointer, k), v, represented) for k, v in enumerate(value))
    return False

# Independent reader derived from the finalized v389 reviewer, with compact
# summary validation added locally. No builder module is imported.
