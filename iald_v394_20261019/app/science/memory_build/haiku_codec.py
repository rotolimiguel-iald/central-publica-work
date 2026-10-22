"""Constrói candidato Haiku a partir do manifesto científico, inteiramente offline.

Contrato: build(manifest_path, app_root=APP) -> (prefix: str, receipt: dict).
Não importa/executa um.py, não chama tokenizer remoto, não lê .env nem servidor.
Importa somente os leitores documentais puros da aplicação. Não altera seus arquivos.
CLI: --manifest manifest_staged.json --out haiku_candidate.md [--dry-run].
Saídas da CLI ficam estritamente nesta pasta; arquivos existentes são imutáveis.
--self-test executa regressões em memória. --dry-run não grava artefato algum.

180000 é a meta NATIVA, não uma contagem obtida por este builder. O responsável
pela integração precisa medir prefixo e pedido wire com as sete ferramentas,
vinculando ambos ao hash deste candidato. Nenhum manifesto ativável é emitido.
"""
from __future__ import annotations

import argparse
from collections import Counter
import difflib
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys
import uuid

APP = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
LEGACY_RECEIPTS = Path('C:/IALD/Central de Patentes/work/iald_tudo_20260921')
MARKER = '## Exposição canônica integral: fórmulas e derivações'
PUBLIC_URL = re.compile(r'https://raw\.githubusercontent\.com/rotolimiguel-iald/the_boundary/([0-9a-f]{40})/.+')
ESSENTIAL = re.compile(
    r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|'
    r'scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|'
    r'theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)
# Generic child names still belong to the hypothesis/formula that owns them.
WHOLE_FIELD = re.compile(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad|formula|equation|equacao|equaç', re.I)
AUXILIARY = frozenset(('runtime_s', 'protocol_hash', 'frozen_hash', 'result_sha16', 'catalog_sha16', 'result_path'))
ALWAYS_FULL = frozenset(('/core/interface_is_light/witness_layers', '/core/interface_is_light/light_chain'))
RESERVED = frozenset(('@', '@SOURCE_FIELDS', '@SOURCE_ITEMS', '@TGL_LITERAL', '@EXPOSITION'))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def strict_json(raw):
    def pairs(rows):
        result = {}
        for key, value in rows:
            need(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ValueError('Non-finite JSON number')
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)


def child(pointer, key):
    return pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')


def resolve(value, pointer):
    need(isinstance(pointer, str) and (pointer == '' or pointer.startswith('/')), 'Invalid JSON pointer')
    for part in pointer.split('/')[1:]:
        need(re.search(r'~(?![01])', part) is None, 'Invalid pointer escape')
        key = part.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            need(re.fullmatch(r'0|[1-9][0-9]*', key), 'Invalid array pointer')
            value = value[int(key)]
        else:
            value = value[key]
    return value


def check_reserved(value):
    if isinstance(value, dict):
        need(not RESERVED.intersection(value), 'Reserved codec key in source; review required')
        for item in value.values():
            check_reserved(item)
    elif isinstance(value, list):
        for item in value:
            check_reserved(item)


def protected_fields(value, pointer=''):
    """Coordinates and unchanged values; no generated scientific paraphrases."""
    result = {}
    if pointer in ('/core/kernel_formalization/axiom_report', '/core/kernel_formalization/formal_files_sha256', '/core/external_ladder/per_theorem'):
        return result
    if isinstance(value, dict):
        for key, item in value.items():
            location = child(pointer, key)
            if WHOLE_FIELD.search(key) or (ESSENTIAL.search(key) and not isinstance(item, (dict, list))):
                result[location] = item
            else:
                result.update(protected_fields(item, location))
    elif isinstance(value, list):
        for key, item in enumerate(value):
            result.update(protected_fields(item, child(pointer, key)))
    return result


def project(value, pointer, topic, omitted, depth=0):
    """Same extractive field policy as the previous builder, with explicit gaps."""
    def reference(reason, *, counts=False):
        record = {'@': pointer[len(topic):]}
        fields = {} if reason in ('individual_boolean_audit_indicators', 'complete_audit_report_retrievable') else protected_fields(value)
        if fields:
            record['fields'] = fields
        if isinstance(value, (dict, list)):
            record['items'] = len(value)
        if counts:
            need(isinstance(value, dict) and all(type(v) is bool for v in value.values()),
                 'Boolean audit changed type; review required')
            record.update(true_fields=sum(value.values()), false_fields=len(value)-sum(value.values()))
        omitted.append({'pointer': pointer, 'reason': reason, 'value_sha256': sha(dump(value).encode())})
        return record

    field_name = pointer.rsplit('/', 1)[-1].replace('~1', '/').replace('~0', '~')
    if pointer in ALWAYS_FULL or (depth >= 1 and WHOLE_FIELD.search(field_name)):
        return value
    if pointer == '/core/external_ladder/per_theorem':
        return reference('individual_boolean_audit_indicators', counts=True)
    if pointer in ('/core/kernel_formalization/axiom_report', '/core/kernel_formalization/formal_files_sha256'):
        return reference('complete_audit_report_retrievable')
    if isinstance(value, dict):
        if depth >= 1:
            return reference('structured_evidence')
        return {key: (reference_scalar(item, child(pointer, key), topic, omitted)
                      if key in AUXILIARY and not isinstance(item, (dict, list))
                      else project(item, child(pointer, key), topic, omitted, depth+1))
                for key, item in value.items()}
    if isinstance(value, list):
        if len(value) > 3 and not any(isinstance(item, str) for item in value):
            return reference('detailed_collection')
        return [project(item, child(pointer, key), topic, omitted, depth+1) for key, item in enumerate(value)]
    return value


def reference_scalar(value, pointer, topic, omitted):
    omitted.append({'pointer': pointer, 'reason': 'auxiliary_metadata', 'value_sha256': sha(dump(value).encode())})
    return {'@': pointer[len(topic):]}


def pack_metadata(value):
    """Reversible @SOURCE_FIELDS/items format used by the existing pilot."""
    if isinstance(value, list):
        return [pack_metadata(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {key: pack_metadata(item) for key, item in value.items()}
    for tag, counted in (('@SOURCE_FIELDS', False), ('@SOURCE_ITEMS', True)):
        candidates = {}
        for key, item in result.items():
            if not key or '/' in key or '~' in key or key.startswith('@') or not isinstance(item, dict):
                continue
            if item == {'@': '/' + key} and not counted:
                candidates[key] = None
            elif counted and set(item) == {'@', 'items'} and item['@'] == '/' + key and type(item['items']) is int:
                candidates[key] = item['items']
        if len(candidates) >= 2:
            result = {key: item for key, item in result.items() if key not in candidates}
            result[tag] = candidates if counted else list(candidates)
    return result


def unpack_metadata(value):
    if isinstance(value, list):
        return [unpack_metadata(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {key: unpack_metadata(item) for key, item in value.items() if key not in ('@SOURCE_FIELDS', '@SOURCE_ITEMS')}
    for tag in ('@SOURCE_FIELDS', '@SOURCE_ITEMS'):
        if tag not in value:
            continue
        fields = value[tag]
        need(type(fields) is (list if tag == '@SOURCE_FIELDS' else dict) and len(fields) >= 2,
             'Invalid grouped metadata')
        for key in fields:
            need(isinstance(key, str) and key and '/' not in key and '~' not in key and not key.startswith('@') and key not in result,
                 'Duplicate or invalid grouped metadata')
            result[key] = {'@': '/' + key}
            if tag == '@SOURCE_ITEMS':
                need(type(fields[key]) is int and fields[key] >= 0, 'Invalid item count')
                result[key]['items'] = fields[key]
    return result


def intern_topics(topics, exposition):
    counts = Counter()
    def scan(value):
        if isinstance(value, str) and len(value) >= 80:
            counts[value] += 1
        elif isinstance(value, dict):
            for item in value.values(): scan(item)
        elif isinstance(value, list):
            for item in value: scan(item)
    for value in topics.values(): scan(value)
    strings = sorted(value for value, count in counts.items() if count > 1 and value not in exposition)
    lookup = {value: 'L'+str(index+1) for index, value in enumerate(strings)}
    dictionary = {ident: value for value, ident in lookup.items()}
    def encode(value):
        if isinstance(value, str):
            if len(value) >= 100 and value in exposition:
                return {'@EXPOSITION': [exposition.index(value), len(value)]}
            if value in lookup:
                return {'@TGL_LITERAL': lookup[value]}
        if isinstance(value, dict):
            # Pointer coordinates are syntax, not internable scientific strings.
            return {key: item if key == '@' else encode(item) for key, item in value.items()}
        if isinstance(value, list): return [encode(item) for item in value]
        return value
    return {key: pack_metadata(encode(value)) for key, value in topics.items()}, dictionary


def decode_literals(value, dictionary, exposition):
    if isinstance(value, list): return [decode_literals(item, dictionary, exposition) for item in value]
    if not isinstance(value, dict): return value
    if set(value) == {'@concat'}:
        parts=[decode_literals(part,dictionary,exposition) for part in value['@concat']]
        need(all(isinstance(part,str) for part in parts), 'Invalid literal concatenation')
        return ''.join(parts)
    if set(value) == {'@upper'}:
        need(isinstance(value['@upper'],str), 'Invalid uppercase spelling')
        return value['@upper'].upper()
    if set(value) == {'@enum'}:
        need(isinstance(value['@enum'],str) and re.fullmatch('[a-z0-9 ]+',value['@enum']), 'Invalid enum spelling')
        return value['@enum'].upper().replace(' ','_')
    if set(value) == {'@TGL_LITERAL'}:
        need(value['@TGL_LITERAL'] in dictionary, 'Missing literal')
        return decode_literals(dictionary[value['@TGL_LITERAL']],dictionary,exposition)
    if set(value) == {'@EXPOSITION'}:
        span = value['@EXPOSITION']
        need(isinstance(span, list) and len(span) == 2 and all(type(n) is int for n in span), 'Invalid exposition span')
        start, length = span
        need(start >= 0 and length > 0 and start+length <= len(exposition), 'Exposition span out of range')
        return exposition[start:start+length]
    return {key: decode_literals(item, dictionary, exposition) for key, item in value.items()}


def restore(value, source, topic, current, represented):
    """Reconstruct from anchored source AND verify every retained field at its path."""
    if isinstance(value, dict) and '@' in value:
        target = topic + value['@']
        need(target == current, 'Source reference assigned to the wrong field')
        actual = resolve(source, target)
        need(set(value) <= {'@', 'fields', 'items', 'true_fields', 'false_fields'}, 'Unknown reference metadata')
        for suffix, item in value.get('fields', {}).items():
            need(suffix.startswith('/') and resolve(actual, suffix) == item, 'Retained semantic field differs from source')
            represented[target+suffix] = item
        if 'items' in value: need(type(value['items']) is int and len(actual) == value['items'], 'Wrong item count')
        if 'true_fields' in value or 'false_fields' in value:
            need(isinstance(actual, dict) and all(type(v) is bool for v in actual.values()), 'Invalid boolean audit')
            need(value['true_fields'] == sum(actual.values()) and value['false_fields'] == len(actual)-sum(actual.values()), 'Wrong audit count')
        return actual
    if isinstance(value, dict):
        return {key: restore(item, source, topic, child(current, key), represented) for key, item in value.items()}
    if isinstance(value, list):
        return [restore(item, source, topic, child(current, key), represented) for key, item in enumerate(value)]
    represented[current] = value
    return value


def is_represented(pointer, value, represented):
    if pointer in represented:
        return represented[pointer] == value
    for ancestor, item in represented.items():
        if pointer.startswith(ancestor+'/'):
            return resolve(item, pointer[len(ancestor):]) == value
    if isinstance(value, dict):
        return all(is_represented(child(pointer, key), item, represented) for key, item in value.items())
    if isinstance(value, list):
        return all(is_represented(child(pointer, key), item, represented) for key, item in enumerate(value))
    return False


def compact_exposition(canonical):
    """Remove only a contiguous, typed boolean audit list; preserve all other bytes."""
    rows = list(re.finditer(r'(?m)^- `[^`\r\n]+` = `(?:True|False)`\r?$', canonical))
    if not rows:
        return canonical, []
    # Only the explicitly named audit ladder is eligible, never arbitrary prose.
    starts = list(re.finditer(r'(?m)^\*\*Escada auditada \(', canonical))
    if not starts:
        return canonical, []
    need(len(starts) == 1, 'Ambiguous audit ladder')
    start = starts[0].start()
    end = canonical.find('\n**', start+2)
    need(end > start, 'Audit ladder boundary missing')
    selected = [row for row in rows if start <= row.start() < end]
    changes = []
    for row in selected:
        # Keep the newline; offsets always refer to the unmodified full source.
        changes.append({'offset': row.start(), 'chars': len(row.group()), 'sha256': sha(row.group().encode())})
    exposition = canonical
    for row in reversed(selected):
        exposition = exposition[:row.start()] + exposition[row.end():]
    if selected:
        notice = ('\nIndicadores individuais de auditoria disponíveis em um_forma_canonica_integral, '
                  'offset='+str(selected[0].start())+', via fetch_tgl/next_offset. '+str(len(selected))+
                  ' registros documentais, não contagem nova de provas.\n')
        exposition = exposition[:start] + notice + exposition[start:]
        # Retain the exact inserted notice for an independent reversal.
        changes[0]['inserted_notice'] = notice
        changes[0]['notice_offset'] = start
    return exposition, changes


class Inputs:
    def __init__(self): self.records = {}

    def read(self, path, expected=None):
        path = Path(path).resolve()
        need(not any(part.casefold() in {'.env', 'iald_stack_v7.py', 'iald_psion_state.json', 'tgl_atlas.md'} for part in path.parts),
             'Confidential source forbidden')
        raw = path.read_bytes()
        digest = sha(raw)
        need(raw and len(raw) <= 64000000, 'Empty or oversized source')
        need(expected is None or expected == digest, 'Source hash mismatch: '+path.name)
        if path in self.records: need(self.records[path]['sha256'] == digest, 'Source changed during build')
        self.records[path] = {'sha256': digest, 'bytes': len(raw)}
        return raw

    def stable(self):
        for path, record in self.records.items():
            need(sha(path.read_bytes()) == record['sha256'], 'Source changed during build: '+path.name)


def readers(app_root):
    """Only existing pure document loaders; no server, provider or um import."""
    sys.dont_write_bytecode = True
    root = Path(app_root).resolve()
    modules = {}
    sys.path.insert(0, str(root))
    try:
        for name in ('iald_instrucao_mae', 'iald_core_indexado', 'iald_estado_publicado', 'iald_kernel', 'iald_response_contract'):
            module = importlib.import_module(name)
            need(Path(module.__file__).resolve().parent in (root, Path(__file__).resolve().parent), 'Document loader from unexpected directory')
            modules[name] = module
    finally:
        sys.path.pop(0)
    return modules


def build(manifest_path, app_root=APP):
    inputs = Inputs()
    manifest_path = Path(manifest_path).resolve()
    manifest = strict_json(inputs.read(manifest_path))
    cfg = manifest['active_cluster']
    release = cfg['release']
    need(re.fullmatch(r'v[0-9]+', release), 'Invalid release')
    need((cfg['commit'] is None and manifest.get('staging_only') is True) or re.fullmatch(r'[0-9a-f]{40}', cfg['commit']), 'Unpinned release')
    source_sha = cfg['release_source_sha256']
    op = manifest['operational_core']
    need(op['current_release'] == release and op['release_source_sha256'] == source_sha, 'Mixed release/core')
    need(manifest['mother_instruction']['version'] == 'v5', 'Mother kernel changed; review required')
    cluster = inputs.read(cfg['path'], cfg['sha256']).decode('utf-8-sig')
    entries = {}
    for entry in manifest['entries']:
        ident = entry['id']
        need(ident not in entries and re.fullmatch(r'[a-z0-9_]+', ident), 'Invalid or duplicate source ID')
        match = PUBLIC_URL.fullmatch(entry['url'])
        need((manifest.get('staging_only') is True and (entry['url']=='' or match)) or (match and match.group(1) == cfg['commit']), 'Public source commit mismatch')
        entries[ident] = inputs.read(entry['path'], entry['public_sha256'])
    evidence = manifest['published_evidence']
    payloads = {key: inputs.read(evidence[key]['path']) for key in ('program', 'result', 'proof_manifest', 'seal')}
    need(sha(payloads['program']) == source_sha, 'Cluster/program mismatch')
    seal = strict_json(payloads['seal'])
    need(seal['um_version'] == release and seal['fail_closed_selftest'] == 'FAIL_CLOSED_SELFTEST_PASSED', 'Seal release/selftest mismatch')
    need(payloads['result'] == entries['resultado_publicado_integral'], 'Retrievable result differs from sealed result')
    result = strict_json(payloads['result'])
    canonical = entries['um_forma_canonica_integral'].decode('utf-8-sig')
    canonical_entry = next(entry for entry in manifest['entries'] if entry['id'] == 'um_forma_canonica_integral')
    need(seal['sha256'].get(Path(canonical_entry['path']).name) == sha(entries['um_forma_canonica_integral']),
         'Canonical exposition differs from release seal')
    # The full-cluster builder can independently deduplicate its exposition.
    # The Haiku exposition comes from the separately sealed original above.
    need(cluster.count(MARKER) == 1, 'Cluster exposition boundary mismatch')
    topic_area = cluster.split(MARKER)[0]
    names = re.findall(r'(?m)^### ([^\r\n]+)\r?$', topic_area)
    need(len(names) == len(set(names)) == cfg['core_sections'] == len(result['core']) and set(names) == set(result['core']),
         'Cluster/result topic coverage mismatch')
    inputs.read(manifest['mother_instruction']['path'], manifest['mother_instruction']['sha256'])
    inputs.read(op['path'], op['sha256'])
    modules = readers(app_root)
    for module in modules.values(): inputs.read(module.__file__)
    catalog = modules['iald_kernel'].KernelCatalog(cfg['kernel_bundle'], cfg['kernel_verification'])
    inputs.read(Path(cfg['kernel_bundle'])/'kernel_manifest.json')
    inputs.read(cfg['kernel_verification'])
    for name, record in catalog.records.items(): inputs.read(catalog.root/name, record['sha256'])
    need(catalog.source_sha == source_sha, 'Catalog belongs to another release')
    formal, formal_meta = modules['iald_estado_publicado'].published_evidence(evidence, catalog)
    mother, _ = modules['iald_instrucao_mae'].mother_instruction(manifest['mother_instruction'])
    core, _ = modules['iald_core_indexado'].operational_core(manifest_path)
    protocols = modules['iald_response_contract']
    # The release is a candidate; do not emit a claim that production already uses it.
    check_reserved(result['core'])
    exposition, audit_rows = compact_exposition(canonical)
    omitted, topics = [], {}
    for name in names:
        pointer = child('/core', name)
        topics[name] = project(result['core'][name], pointer, pointer, omitted)
    encoded, dictionary = intern_topics(topics, exposition)
    semantic_fields = 0
    for name in names:
        pointer = child('/core', name)
        node = decode_literals(unpack_metadata(encoded[name]), dictionary, exposition)
        need(node == topics[name], 'Metadata/literal round trip failed')
        represented = {}
        actual = restore(node, result, pointer, pointer, represented)
        need(actual == result['core'][name], 'Source projection is not reconstructible')
        protected = protected_fields(result['core'][name], pointer)
        for location, item in protected.items():
            need(is_represented(location, item, represented), 'Missing semantic field: '+location)
        for location in ALWAYS_FULL:
            if location.startswith(pointer+'/'):
                need(is_represented(location, resolve(result, location), represented), 'Missing witness/light chain')
        semantic_fields += len(protected)
    header = (
        'MEMÓRIA CIENTÍFICA VERSIONADA.\nVersão selecionada do pacote: '+release+
        '; programa SHA256: '+source_sha+'; commit: '+str(cfg['commit'])+'.\n'
        'Contexto documental conferido; nenhuma nova execução de um.py, Lean ou teste de natureza.\n'
        'Todas as seções do resultado estão representadas. Detalhes apontados por @ NÃO estão carregados. '
        'Concatenar @ ao ponteiro Fonte do tópico; fields preserva valores literais nos caminhos relativos a @. '
        'items conta registros, nunca provas. true_fields/false_fields contam indicadores booleanos, não teoremas.\n'
        '@SOURCE_FIELDS:[k,...] equivale a k:{"@":"/k"}; @SOURCE_ITEMS:{k:n,...} equivale a k:{"@":"/k","items":n}. '
        '@TGL_LITERAL referencia o dicionário abaixo. @EXPOSITION:[offset,comprimento] referencia caracteres Unicode '
        'do bloco EXPOSICAO_CANONICA, sem a quebra após a abertura. São valores idênticos carregados, não resumos.\n'
        'LITERAIS_COMPARTILHADOS\n'+dump(dictionary)+'\n')
    source_rows = [{key: entry[key] for key in ('id', 'url', 'public_sha256')} for entry in manifest['entries']]
    blocks = [header, protocols.IDENTITY_PROTOCOL, protocols.SOLUTION_PROTOCOL, mother, core, formal,
              'FONTES PÚBLICAS RECUPERÁVEIS (fetch_tgl/search_tgl; páginas não equivalem à leitura integral)\n'+dump(source_rows)]
    for name in names:
        blocks.append('### '+name+'\nFonte: resultado_publicado_integral '+child('/core', name)+'\n'+dump(encoded[name]))
    blocks.extend([MARKER+'\n<EXPOSICAO_CANONICA>\n'+exposition+'\n</EXPOSICAO_CANONICA>',
                   protocols.IDENTITY_PROTOCOL, protocols.SOLUTION_PROTOCOL])
    prefix = '\n\n'.join(blocks)+'\n'
    need('<ATLAS_CANONICO' not in prefix, 'Private Atlas block forbidden')
    inputs.stable()
    receipt = {
        'schema': 'iald.haiku.candidate.v1', 'status': 'NATIVE_COUNT_REQUIRED_NOT_DEPLOYED',
        'release': release, 'source_sha256': source_sha, 'commit': cfg['commit'],
        'manifest_sha256': inputs.records[manifest_path]['sha256'], 'source_cluster_sha256': cfg['sha256'],
        'prefix_sha256': sha(prefix.encode()), 'bytes': len(prefix.encode()), 'characters': len(prefix),
        'native_tokens': None, 'native_request_tokens': None, 'target_native_tokens': 180000,
        'native_fit_verified': False, 'semantic_review_required': True,
        'required_native_budget': {'window': 200000, 'output': 4096, 'margin': 1024, 'minimum_remaining': 10000},
        'topic_count': len(names), 'topics': names, 'protected_fields_verified': semantic_fields,
        'projection_roundtrip_verified': True, 'metadata_roundtrip_verified': True,
        'mother_v5_full': True, 'operational_core_full': True,
        'exposition_change': 'only_typed_boolean_audit_rows_retrievable', 'audit_rows': audit_rows,
        'exposition_sha256': sha(exposition.encode()), 'exposition_characters': len(exposition),
        'shared_literal_count': len(dictionary), 'details_in_source': omitted,
        'published_evidence_checked': formal_meta['published_evidence_checked'],
        'scope': 'DOCUMENTARY_FIDELITY_ONLY__COMPILER_NOT_RERUN__NOT_SEMANTIC_CERTIFICATION',
        'inputs': {str(path): record for path, record in inputs.records.items()},
    }
    return prefix, receipt


def source_topics(text, names):
    """Read whole topic capsules, including the two reviewed titled capsules."""
    end = text.index('\n'+MARKER)
    body = text[:end]
    headings = []
    for match in re.finditer(r'(?m)^### ([^\n]+)\n', body):
        name = match.group(1).split(' — ', 1)[0]
        if name in names:
            headings.append((name, match))
    result = {}
    for index, (name, match) in enumerate(headings):
        stop = headings[index+1][1].start() if index+1 < len(headings) else len(body)
        block = body[match.end():stop]
        category = re.search(r'(?m)^## ', block)
        if category: block = block[:category.start()]
        need(name not in result and '/core/'+name in block, 'Missing/duplicate baseline topic anchor')
        result[name] = block.strip()
    need(set(result) == set(names), 'Baseline capsule coverage mismatch')
    return result


def offline_tokens(text, cache_dir):
    """Load the already installed BPE bytes directly; no downloader/cache writes."""
    import tiktoken
    import tiktoken_ext.openai_public as public
    import base64
    original = public.load_tiktoken_bpe
    def cached(url, expected_hash=None):
        path = Path(cache_dir)/hashlib.sha1(url.encode()).hexdigest()
        need(path.is_file(), 'Offline tokenizer cache absent')
        raw = path.read_bytes()
        need(expected_hash and sha(raw) == expected_hash, 'Offline tokenizer cache hash mismatch')
        return {base64.b64decode(token): int(rank)
                for token, rank in (line.split() for line in raw.splitlines() if line)}
    public.load_tiktoken_bpe = cached
    try:
        configuration = public.o200k_base()
    finally:
        public.load_tiktoken_bpe = original
    encoding = tiktoken.Encoding(**configuration)
    return len(encoding.encode(text, disallowed_special=()))




def lean_mask(source):
    """Mask comments/strings without changing offsets; do not parse proof syntax."""
    out=list(source); i=0; depth=0
    while i<len(source):
        if depth:
            if source.startswith('/-',i):out[i:i+2]='  ';depth+=1;i+=2
            elif source.startswith('-/',i):out[i:i+2]='  ';depth-=1;i+=2
            else:
                if source[i]!='\n':out[i]=' '
                i+=1
        elif source.startswith('/-',i):out[i:i+2]='  ';depth=1;i+=2
        elif source.startswith('--',i):
            while i<len(source) and source[i]!='\n':out[i]=' ';i+=1
        elif source[i]=='"':
            out[i]=' ';i+=1
            while i<len(source):
                c=source[i]
                if c!='\n':out[i]=' '
                i+=1
                if c=='\\' and i<len(source):out[i]=' ';i+=1
                elif c=='"':break
        else:i+=1
    need(depth==0,'Unterminated Lean comment')
    return ''.join(out)


def lean_declaration_excerpt(source):
    """Exact declaration heads and ambient scopes; structures retain all fields."""
    masked=lean_mask(source)
    pattern=r'(?m)^(?:(?:noncomputable|private|protected)\s+)*(def|theorem|lemma|structure|class|namespace|section|end|open|variable|universe|import)\b'
    marks=list(re.finditer(pattern,masked));parts=[];decls=[]
    for index,mark in enumerate(marks):
        end=marks[index+1].start() if index+1<len(marks) else len(source)
        text=masked[mark.start():end].rstrip()
        kind=mark.group(1)
        if kind in ('def','theorem','lemma'):
            nesting=0;cut=None
            for offset,char in enumerate(text):
                if char in '([{':nesting+=1
                elif char in ')]}':nesting-=1
                if nesting==0 and (text.startswith(':=',offset) or re.match(r'where\b',text[offset:])):
                    cut=offset;break
            need(cut is not None,'Lean declaration delimiter not found')
            text=text[:cut].rstrip()
            name=re.search(r'\b(?:def|theorem|lemma)\s+([^\s(:]+)',text)
            need(name,'Lean name not found')
            decls.append({'name':name.group(1),'line':source.count('\n',0,mark.start())+1,
                          'kind':kind,'header_sha256':sha(text.encode())})
            text += '\n-- Corpo completo: consultar esta declaração no catálogo.'
        elif kind in ('structure','class'):
            name=re.search(r'\b(?:structure|class)\s+([^\s(:]+)',text)
            need(name,'Lean structure name not found')
            decls.append({'name':name.group(1),'line':source.count('\n',0,mark.start())+1,
                          'kind':kind,'header_sha256':sha(text.encode())})
        text=re.sub(r'(?m)^[ \t]+$','',text)
        text=re.sub(r'\n{3,}','\n\n',text).strip()
        if text:parts.append(text)
    return '\n\n'.join(parts),decls


def compact_proof_sources(nucleus):
    records=[];tick=chr(96)*3
    marker='ESTADO DA PUBLICAÇÃO CONFERIDO NESTA REQUISIÇÃO'
    begin=nucleus.index('\n{', nucleus.index(marker))+1
    state,length=json.JSONDecoder().raw_decode(nucleus[begin:])
    serialized=dump(state)
    need(strict_json(serialized)==state,'Formal state serialization changed values')
    nucleus=nucleus[:begin]+serialized+nucleus[begin+length:]
    pattern=r'<FONTE_LEAN_DAS_HIPOTESES>\n([^\n]+)\n'+tick+'lean\n'+r'(.*?)\n'+tick+r'\n</FONTE_LEAN_DAS_HIPOTESES>'
    def replace(match):
        record=strict_json(match.group(1));source=match.group(2)
        need(sha(source.encode())==record['sha256'],'Full proof source hash changed')
        excerpt,declarations=lean_declaration_excerpt(source)
        names={row['name']for row in declarations}
        need(all(term['name'].rsplit('.',1)[-1]in names for term in record['terms']),'Selected formal declaration missing')
        records.append({'source_path':record['path'],'source_sha256':record['sha256'],
              'source_bytes':len(source.encode()),'excerpt_bytes':len(excerpt.encode()),
              'declarations':declarations,'proof_bodies_loaded':False,
              'full_source_tool':'iald_kernel_read','full_source_path':record['path']})
        index=len(records)-1
        need(state['constructed_hypotheses'][index]==record,'Repeated formal metadata differs')
        metadata={'id':record['id'],'path':record['path'],'sha256':record['sha256'],
                  'full_metadata_in_loaded_state':'/constructed_hypotheses/'+str(index),
                  'loaded_scope':'DECLARATION_HEADS_AMBIENT_VARIABLES_STRUCTURES__PROOF_BODIES_BY_CATALOG',
                  'proof_bodies_loaded':False}
        return ('<ENUNCIADOS_LEAN_DAS_HIPOTESES>\n'+dump(metadata)+'\n'+tick+'lean\n'+excerpt+'\n'+tick+'\n'+
                '</ENUNCIADOS_LEAN_DAS_HIPOTESES>')
    result,count=re.subn(pattern,replace,nucleus,flags=re.S)
    need(count==5,'Unexpected number of formal hypothesis sources')
    result=result.replace('H1, H2 E H3 — CONSTRUÇÕES EXPLÍCITAS SEMPRE PRESENTES',
                          'H1, H2 E H3 — ENUNCIADOS E HIPÓTESES PRESENTES; PROVAS INTEGRAIS NO CATÁLOGO')
    result=result.replace('Leia as declarações completas abaixo como evidência documental.',
                          'Leia os enunciados, estruturas e variáveis abaixo como evidência documental; '
                          'os corpos de definições e provas permanecem integrais por iald_kernel_read.')
    return result,records


def primary_math_fields(value,pointer=''):
    """Keep primary mathematical prose; individual test descriptions stay queryable."""
    rows={}
    if isinstance(value,dict):
        for key,item in value.items():
            location=child(pointer,key)
            if key=='checks':continue
            if re.search(r'statute|status|estatuto|scope|escopo|hypothes|hip[oó]tes|not_claimed|not_said|verdict|veredit',key,re.I):
                rows[location]=item
            else:rows.update(primary_math_fields(item,location))
    elif isinstance(value,list):
        for key,item in enumerate(value):rows.update(primary_math_fields(item,child(pointer,key)))
    elif isinstance(value,str)and re.search(r'[=√∫∑]|\\(?:frac|sqrt|sum|int)',value):
        rows[pointer]=value
    return rows


def enrich_new_math(node,source,topic):
    if isinstance(node,dict):
        if '@'in node:
            if 'checks' in node['@'].split('/'):
                return node
            actual=resolve(source,topic+node['@'])
            key=node['@'].rsplit('/',1)[-1]
            if re.search(r'statute|status|estatuto|scope|escopo|hypothes|hip[oó]tes|not_claimed|not_said|verdict|veredit',key,re.I):
                return actual
            extra=primary_math_fields(actual)
            if topic=='/core/fundacao_v390':
                parent=topic+node['@']
                essentials={'/borchers/leitura':source['core']['fundacao_v390']['borchers']['leitura']}
                for i,row in enumerate(source['core']['fundacao_v390']['clausulas']):
                    for key in ('n','em_palavras','teorema'):essentials['/clausulas/'+str(i)+'/'+key]=row[key]
                for suffix,value in essentials.items():
                    full=topic+suffix
                    if full.startswith(parent+'/'):extra[full[len(parent):]]=value

            # Numeric findings audited against this sealed release; values read from source.
            for full in ('/core/hubble_ratio_opening_v388/numbers/z_disc', '/core/hubble_ratio_opening_v388/numbers/z_delta', '/core/hubble_ratio_opening_v388/numbers/lnB/TGL_vs_LCDM', '/core/hubble_ratio_opening_v388/numbers/lnB/TGL_vs_beta_livre', '/core/hubble_ratio_opening_v388/recalculo_ao_lado/lnB_TGL_vs_beta_livre_convergido', '/core/hubble_ratio_opening_v388/recalculo_ao_lado/erro_quadratura_n25_n35', '/core/three_stress_tests_v387/joint/V3_P_all', '/core/three_stress_tests_v387/joint/V3_boolean', '/core/three_stress_tests_v387/joint/gpu_in_joint', '/core/three_stress_tests_v387/joint/three_pillar_probability_in_core'):
                parent=topic+node['@']
                if full.startswith(parent+'/'):extra[full[len(parent):]]=resolve(source,full)
            if ''in extra:return actual
            result=dict(node)
            if extra:result['fields']={**result.get('fields',{}),**extra}
            return result
        return {key:enrich_new_math(value,source,topic)for key,value in node.items()}
    if isinstance(node,list):return [enrich_new_math(value,source,topic)for value in node]
    return node


def compact_accepted_history(exposition, topics, canonical, unchanged, max_savings=30000):
    """Replace historical exposition repeats with their accepted loaded capsules.
    Literal/summary ranges used by any capsule remain verbatim and are remapped.
    Full chapter details stay retrievable in the current sealed canonical source.
    """
    spans = []
    def collect(node):
        if isinstance(node, dict):
            if '@EXPOSITION' in node or '@SUMMARY' in node:
                spans.append(tuple(node['span']))
            else:
                for item in node.values(): collect(item)
        elif isinstance(node, list):
            for item in node: collect(item)
    for body in topics.values():
        for line in body.splitlines():
            try: collect(strict_json(line))
            except ValueError: pass
    mapping = {
        '## v8 ': 'tetelestai_pruning', '## v10 ': 'smatrix_closure',
        '## v11 ': 'ergodicity_door_mixing', '## v12 ': 'absolute_one_as_input',
        '## v13 ': 'light_reason_radicalization', '## v14 ': 'reason_consciousness_operator',
        '## v17 ': 'reading_direction', '## v16 ': 'cocycle_to_einstein',
        '## v18 ': 'p2d_descent', '## v19 ': 'iii1_net_image',
        '## v20 ': 'half_nat_continuous_corner_density', '## v21-A ': 'specific_free_scalar_aqft_net',
        '## v21-B ': 'area_scale_newton_equivalence', '## v25 ': 'verb_inhabitant',
        '## v26 ': 'selector_transport', '## v27 ': 'name_index',
        '## v28 ': 'half_nat_tower', '## v29 ': 'graviton_shadow',
        '## v30 ': 'name_relation', '## v32 ': 'tgl_closure',
    }
    headings = list(re.finditer(r'(?m)^## [^\n]+', exposition))
    changes, saved = [], 0
    for i, heading in enumerate(headings):
        topic = next((name for prefix, name in mapping.items() if heading.group().startswith(prefix)), None)
        if topic not in unchanged: continue
        a = heading.start(); b = headings[i+1].start() if i+1 < len(headings) else len(exposition)
        canonical_start = canonical.find(heading.group())
        if canonical_start < 0: continue
        crossing = [(x,n) for x,n in spans if x < b and x+n > a and not (a <= x and x+n <= b)]
        if crossing: continue
        keep = sorted(set((x,x+n) for x,n in spans if a <= x < b))
        merged = []
        for x,y in keep:
            if merged and x <= merged[-1][1]: merged[-1] = (merged[-1][0], max(y,merged[-1][1]))
            else: merged.append((x,y))
        replacement = (heading.group()+'\nHistórico condensado já carregado em '+topic+
            '. Detalhes: fetch_tgl id=um_forma_canonica_integral offset='+str(canonical_start)+
            '; seguir next_offset. Os excertos literais referenciados continuam abaixo.\n')
        positions = []
        for x,y in merged:
            replacement += '\n'
            positions.append((x,y,len(replacement)))
            replacement += exposition[x:y]
        replacement += '\n\n'
        gain = len(exposition[a:b].encode())-len(replacement.encode())
        if gain <= 0 or saved+gain > max_savings: continue
        saved += gain
        changes.append({'start':a,'end':b,'replacement':replacement,'retained_ranges':positions,
            'topic':topic,'canonical_offset':canonical_start,'old_sha256':sha(exposition[a:b].encode()),
            'saved_bytes':gain})
    # Only synthesized operational guidance is updated; scientific historical v368 remains.
    old = 'conferir o estado da publicação v368 carregado antes de descrevê-los como pendências atuais'
    new = 'conferir o estado da publicação selecionada deste pacote antes de descrevê-los como pendências atuais'
    need(exposition.count(old)==1, 'Operational orientation absent or ambiguous')
    at = exposition.index(old)
    need(not any(row['start'] <= at < row['end'] for row in changes), 'Orientation overlaps historical compaction')
    changes.append({'start':at,'end':at+len(old),'replacement':new,'orientation_only':True,
                    'old_text':old,'new_text':new,'old_sha256':sha(old.encode()),'saved_bytes':len(old.encode())-len(new.encode())})
    changes.sort(key=lambda row:row['start'])
    def relocate(start, size):
        stop=start+size; shift=0; growth=0
        for row in changes:
            a,b=row['start'],row['end'];delta=len(row['replacement'])-(b-a)
            if b <= start: shift+=delta
            elif a >= stop: continue
            elif row.get('orientation_only') and start <= a and b <= stop: growth+=delta
            else:
                for x,y,new_position in row.get('retained_ranges',[]):
                    if x <= start and stop <= y:
                        return [a+shift+new_position+start-x,size]
                raise ValueError('Historical compaction would remove a referenced span')
        return [start+shift,size+growth]
    remapped={}
    def change_refs(node):
        if isinstance(node,dict):
            if '@EXPOSITION'in node or '@SUMMARY'in node:
                result=dict(node);result['span']=relocate(*node['span']);return result
            return {key:change_refs(item) for key,item in node.items()}
        if isinstance(node,list):return [change_refs(item) for item in node]
        return node
    for topic,body in topics.items():
        lines=[]
        for line in body.splitlines():
            try:value=strict_json(line)
            except ValueError:lines.append(line);continue
            lines.append(dump(change_refs(value)))
        remapped[topic]='\n'.join(lines)
    result=exposition
    for row in reversed(changes):result=result[:row['start']]+row['replacement']+result[row['end']:]
    return result, remapped, changes


def externalize_historical_labels(body, topic, source, dictionary, records):
    """Only old all-capitals machine identifiers; no prose/formula rewrite."""
    lines=[]
    for line in body.splitlines():
        try:node=strict_json(line)
        except ValueError:lines.append(line);continue
        if not isinstance(node,dict):lines.append(line);continue
        for key,value in list(node.items()):
            literal=dictionary.get(value.get('@TGL_LITERAL')) if isinstance(value,dict) and set(value)=={'@TGL_LITERAL'} else value
            if (key in ('verdict','status','selo','seal') and isinstance(literal,str) and len(literal)>120
                    and re.fullmatch(r'[A-Z0-9_:./ —-]+',literal)):
                need(source.get(key)==literal,'Historical label source drift')
                node[key]={'@':'/'+key}
                records.append({'topic':topic,'pointer':child('/core/'+topic,key),
                                'value_sha256':sha(literal.encode()),'reason':'historical_machine_identifier_retrievable'})
        lines.append(dump(node))
    return '\n'.join(lines)


def build_fitted(manifest_path, app_root=APP, baseline_prefix=None, baseline_manifest=None):
    """Reuse accepted capsules only for identical source subtrees; regenerate deltas.

    The accepted canonical condensation remains explicitly historical. Exact new
    canonical passages follow it, with precedence. Its duplicate verdict roster
    stays available by source offset; every new topic verdict is loaded separately.
    No scientific summary is fabricated to attain a byte target.
    """
    root = Path(app_root).resolve()
    baseline_prefix = Path(baseline_prefix or root/'.iald_runtime/haiku/prefix.md')
    baseline_manifest = Path(baseline_manifest or root/'iald_nucleo_fixo.json')
    initial, original_receipt = build(manifest_path, root)
    inputs = Inputs()
    current = strict_json(inputs.read(manifest_path))
    previous = strict_json(inputs.read(baseline_manifest))
    previous_raw = inputs.read(baseline_prefix)
    previous_text = previous_raw.decode('utf-8')
    runtime = strict_json(inputs.read(baseline_prefix.with_name('manifest.json')))
    need(sha(previous_raw) == runtime['prefix_sha256'], 'Installed baseline hash mismatch')
    prior_work = LEGACY_RECEIPTS
    draft_name = runtime['source_draft']
    need(Path(draft_name).name == draft_name and draft_name.endswith('.md'), 'Invalid baseline receipt name')
    proposal = strict_json(inputs.read(prior_work/Path(draft_name).with_suffix('.json')))
    need(proposal['sha256'] == sha(previous_raw), 'Accepted metadata receipt differs')
    parent_path = Path(proposal['parent'])
    need(parent_path.resolve().parent == prior_work.resolve(), 'Unexpected baseline parent')
    parent_raw = inputs.read(parent_path, proposal['parent_sha256'])
    parent_receipt = strict_json(inputs.read(parent_path.with_suffix('.json')))
    need(sha(parent_raw) == parent_receipt['sha256'], 'Baseline assembly receipt drift')
    marker = '\n'+MARKER
    start = previous_text.index(marker)+len(marker)
    exposition = previous_text[start:start+parent_receipt['new_exposition_chars']]
    need(sha(exposition.encode()) == parent_receipt['new_exposition_sha256'], 'Baseline exposition drift')
    def document(config, name):
        entry = next(item for item in config['entries'] if item['id'] == name)
        return inputs.read(entry['path'], entry['public_sha256'])
    old_result = strict_json(document(previous, 'resultado_publicado_integral'))
    new_result = strict_json(document(current, 'resultado_publicado_integral'))
    old_canonical = document(previous, 'um_forma_canonica_integral').decode('utf-8-sig').replace('\r\n', '\n')
    new_canonical = document(current, 'um_forma_canonica_integral').decode('utf-8-sig').replace('\r\n', '\n')
    prior_topics = source_topics(previous_text, old_result['core'])
    dictionary_marker = 'a referência preserva o valor, não acrescenta estatuto.\n'
    dictionary = strict_json(previous_text.split(dictionary_marker, 1)[1].split('\n', 1)[0])
    identical = {name for name in old_result['core'] if old_result['core'][name] == new_result['core'].get(name)}
    scientific_same = set(identical)
    auxiliary_only = []
    for name, node in old_result['core'].items():
        fresh_node = new_result['core'].get(name)
        if (name not in identical and isinstance(node, dict) and isinstance(fresh_node, dict)
                and 'runtime_s' in node and 'runtime_s' in fresh_node
                and {k:v for k,v in node.items() if k!='runtime_s'} == {k:v for k,v in fresh_node.items() if k!='runtime_s'}
                and 'runtime_s' not in prior_topics[name]):
            scientific_same.add(name);auxiliary_only.append(name)
    exposition, prior_topics, history_changes = compact_accepted_history(
        exposition, prior_topics, new_canonical, identical)
    historical_labels = []
    for name in scientific_same:
        prior_topics[name] = externalize_historical_labels(prior_topics[name], name,
            new_result['core'][name], dictionary, historical_labels)
    # Remove the repetitive roster only after comparing every row to sealed JSON.
    roster_heading = '## TODOS OS MODULOS COM VEREDITO NESTA RODADA'
    roster_start = new_canonical.find(roster_heading)
    roster = None
    current_for_diff = new_canonical
    if roster_start >= 0:
        roster_text = new_canonical[roster_start:]
        found = set()
        for line in roster_text.splitlines()[1:]:
            if not line.strip(): continue
            if re.fullmatch(r'_[0-9]+ modulos com veredito ou status nesta rodada; versao v[0-9]+; rodada [^_]+_', line):
                continue
            match = re.fullmatch(r'- `([^`]+)`: `(.*)`(?: \[all_verified=(True|False)\])?', line)
            need(match and match.group(1) in new_result['core'], 'Unrecognized canonical roster row')
            name, verdict, boolean = match.groups()
            node = new_result['core'][name]
            need(name not in found and isinstance(node, dict) and str(node.get('verdict', node.get('status'))) == verdict,
                 'Canonical roster differs from result verdict')
            if boolean: need(node.get('all_verified') is (boolean == 'True'), 'Roster audit flag mismatch')
            found.add(name)
        expected = {name for name, node in new_result['core'].items() if isinstance(node, dict) and isinstance(node.get('verdict', node.get('status')), str)}
        need(found == expected, 'Incomplete canonical verdict roster')
        roster = {'source_id': 'um_forma_canonica_integral', 'offset': roster_start,
                  'characters': len(roster_text), 'sha256': sha(roster_text.encode()), 'verified_rows': len(found)}
        current_for_diff = new_canonical[:roster_start]
    old_lines, new_lines = old_canonical.splitlines(keepends=True), current_for_diff.splitlines(keepends=True)
    differences, amendments = [], []
    for operation, a, b, c, d in difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes():
        if operation == 'equal': continue
        old_piece, new_piece = ''.join(old_lines[a:b]), ''.join(new_lines[c:d])
        differences.append({'operation': operation, 'old_lines': [a, b], 'new_lines': [c, d],
                            'old_sha256': sha(old_piece.encode()), 'new_sha256': sha(new_piece.encode())})
        if new_piece.strip():
            amendments.append('Fonte atual: um_forma_canonica_integral linhas '+str(c+1)+'–'+str(d)+'\n'+new_piece)
    exposition += ('\n\n## Correções canônicas da release '+current['active_cluster']['release']+'\n'
                   'Os trechos literais atuais abaixo prevalecem sobre a exposição histórica precedente. '
                   'A forma integral atual está em um_forma_canonica_integral; nenhum número histórico é contador atual.\n'
                   +'\n'.join(amendments))
    if roster:
        exposition += ('\nRol completo de vereditos repetidos: fetch_tgl id=um_forma_canonica_integral, offset='
                       +str(roster['offset'])+'. '+str(roster['verified_rows'])+' linhas conferidas com o resultado. '
                       'Todos os tópicos estão representados abaixo; novos vereditos permanecem literais.\n')
    names = original_receipt['topics']
    fresh, reused, omitted = {}, [], []
    for name in names:
        node = new_result['core'][name]
        if name in scientific_same:
            reused.append(name)
            continue
        pointer = child('/core', name)
        fresh[name] = project(node, pointer, pointer, omitted)
        if name not in old_result['core']:
            fresh[name] = enrich_new_math(fresh[name], new_result, pointer)
        if name == 'kernel_formalization':
            # Thousands of individual Boolean audit identifiers are a catalog,
            # not the hypothesis/source declarations that the full nucleus loads.
            flags = {key: value for key, value in node.items() if type(value) is bool}
            fresh[name] = {key: value for key, value in fresh[name].items() if key not in flags}
            fresh[name]['AUDIT_BOOLEAN_FIELDS_IN_SOURCE'] = {
                'source_pointer': pointer, 'true_fields': sum(flags.values()),
                'false_fields': len(flags)-sum(flags.values()),
                'reading': 'Indicadores individuais disponíveis na fonte; não são contagem de teoremas.'}
    encoded, new_dictionary = intern_topics(fresh, exposition)
    def rename(value):
        if isinstance(value, dict):
            if set(value) == {'@TGL_LITERAL'}: return {'@TGL_LITERAL': 'N'+value['@TGL_LITERAL']}
            return {key: rename(item) for key, item in value.items()}
        if isinstance(value, list): return [rename(item) for item in value]
        return value
    encoded = {name: rename(value) for name, value in encoded.items()}
    dictionary.update({'N'+key: value for key, value in new_dictionary.items()})
    # Initial generation already checked source integrity and the pure loaders.
    # Keep the entire mother, operational core, current formal evidence and sources.
    begin = initial.index(modules_identity := readers(root)['iald_response_contract'].IDENTITY_PROTOCOL)
    first_topic = initial.index('\n\n### '+names[0]+'\nFonte:')
    nucleus, formal_excerpts = compact_proof_sources(initial[begin:first_topic])
    catalog_marker='FONTES PÚBLICAS RECUPERÁVEIS (fetch_tgl/search_tgl; páginas não equivalem à leitura integral)\n'
    location=nucleus.index(catalog_marker)+len(catalog_marker)
    catalog_rows,catalog_length=json.JSONDecoder().raw_decode(nucleus[location:])
    need(all(set(row)=={'id','url','public_sha256'} for row in catalog_rows),'Unexpected public catalog fields')
    nucleus=nucleus[:location]+dump([row['id'] for row in catalog_rows])+(
        '\nÍndice de IDs. fetch_tgl devolve os hashes e URLs verificados; o recibo deste candidato vincula '
        'os registros completos ao manifesto da release.\n')+nucleus[location+catalog_length:]
    header = ('MEMÓRIA CIENTÍFICA VERSIONADA '+current['active_cluster']['release']+'.\n'
              'Programa SHA256 '+current['active_cluster']['release_source_sha256']+'.\n'
              'v5/Core integrais; enunciados Lean, variáveis e estruturas carregados; corpos das provas por consulta no catálogo completo. Tópicos atuais extraídos do resultado selado. '
              'Cápsulas aceitas são reutilizadas para subárvores JSON idênticas ou com mudança exclusiva do runtime_s não carregado. '
              'A exposição v368 é histórica e agora parcial: detalhes repetidos usam as cápsulas aceitas carregadas e a fonte integral recuperável. Correções literais da release selecionada ao final prevalecem.\n'
              'FONTE IMPLÍCITA de cada cabeçalho ### nome: resultado_publicado_integral /core/nome. METADADOS: @ concatena a esse ponteiro e indica detalhes não carregados; fields guarda valores literais '
              'com caminhos relativos a @. @SOURCE_FIELDS:[k] expande k:{"@":"/k"}; @SOURCE_ITEMS:{k:n} '
              'expande k:{"@":"/k","items":n}. items/true_fields/false_fields contam registros, nunca provas. '
              '@TGL_LITERAL lê o dicionário. @EXPOSITION com [offset,comprimento], ou com span e starts_with, '
              'lê texto literal do bloco de exposição; @SUMMARY referencia a síntese documental nomeada nesse bloco, '
              'NÃO o valor literal da fonte. Seus source_pointer permanecem recuperáveis. Offsets são caracteres Unicode.\n'
              'DICIONÁRIO DE LITERAIS\n'+dump(dictionary)+'\n')
    blocks = [header, nucleus]
    for name in names:
        if name in reused:
            body = prior_topics[name]
        else:
            body = 'Fonte: resultado_publicado_integral '+child('/core', name)+'\n'+dump(encoded[name])
        body = re.sub(r'(?m)^Fonte: resultado_publicado_integral /core/'+re.escape(name)+r'\n', '', body)
        blocks.append('### '+name+'\n'+body)
    blocks.append(MARKER+'\n<EXPOSICAO_CANONICA>\n'+exposition+'\n</EXPOSICAO_CANONICA>')
    prefix = '\n\n'.join(blocks)+'\n'
    # Every carried literal/summary anchor is checked in its new coordinate system.
    references = Counter()
    used_literals = set()
    def verify_refs(value):
        if isinstance(value, list):
            for item in value: verify_refs(item)
        elif isinstance(value, dict):
            if '@TGL_LITERAL' in value:
                need(value['@TGL_LITERAL'] in dictionary, 'Stale dictionary reference')
                references['literal'] += 1
                used_literals.add(value['@TGL_LITERAL'])
            elif '@EXPOSITION' in value or '@SUMMARY' in value:
                span = value.get('span', value.get('@EXPOSITION'))
                need(isinstance(span, list) and len(span) == 2, 'Malformed baseline span')
                start, size = span
                need(type(start) is int and type(size) is int and 0 <= start < start+size <= len(exposition), 'Stale exposition span')
                piece = exposition[start:start+size]
                if '@SUMMARY' in value:
                    need(piece.startswith('**Estatutos ['+value['@SUMMARY']+']**'), 'Stale summary reference')
                    need(value['source_pointer'].startswith('/core/'), 'Missing source pointer')
                    resolve(new_result, value['source_pointer'])
                    references['summary'] += 1
                elif 'starts_with' in value:
                    need(piece.startswith(value['starts_with']), 'Stale literal reference')
                    references['exposition'] += 1
                else:
                    references['exposition'] += 1
            else:
                for item in value.values(): verify_refs(item)
    for block in blocks[2:-1]:
        for line in block.splitlines():
            if line.startswith(('{', '[')):
                try: value = strict_json(line)
                except ValueError: continue
                verify_refs(value)
    new_topics = [name for name in names if name not in old_result['core']]
    # New conclusions must be present as exact source values after codec decoding.
    for name in new_topics:
        decoded = decode_literals(unpack_metadata(encoded[name]), dictionary, exposition)
        need(decoded.get('verdict') == new_result['core'][name].get('verdict'), 'New verdict lost')
        represented = {}
        pointer = child('/core', name)
        need(restore(decoded, new_result, pointer, pointer, represented) == new_result['core'][name], 'New topic reconstruction failed')
        for location, value in protected_fields(new_result['core'][name], pointer).items():
            need(is_represented(location, value, represented), 'New semantic field lost: '+location)
        for location, value in primary_math_fields(new_result['core'][name], pointer).items():
            need(is_represented(location, value, represented), 'New primary mathematical field lost: '+location)
    pruned = {key:value for key,value in dictionary.items() if key in used_literals}
    prefix = prefix.replace('DICIONÁRIO DE LITERAIS\n'+dump(dictionary)+'\n', 'DICIONÁRIO DE LITERAIS\n'+dump(pruned)+'\n',1)
    tokens = offline_tokens(prefix, root/'.iald_runtime/tokenizer_cache')
    baseline_tokens = offline_tokens(previous_text, root/'.iald_runtime/tokenizer_cache')
    inputs.stable()
    receipt = {
        'schema': 'iald.haiku.fitted-candidate.v1', 'status': 'LOCAL_COUNTED_NATIVE_COUNT_REQUIRED',
        'builder_sha256': sha(Path(__file__).read_bytes()),
        'release': current['active_cluster']['release'], 'prefix_sha256': sha(prefix.encode()),
        'bytes': len(prefix.encode()), 'o200k_tokens': tokens, 'native_tokens': None,
        'native_fit_verified': False, 'target_native_tokens': 180000,
        'baseline_prefix_sha256': sha(previous_raw), 'baseline_bytes': len(previous_raw),
        'baseline_o200k_tokens': baseline_tokens, 'baseline_native_tokens_reported': runtime['budget']['permanent_tokens'],
        'target_bytes': [470000, 490000], 'target_o200k_tokens': [150000, 165000],
        'local_byte_target_met': 470000 <= len(prefix.encode()) <= 490000,
        'local_token_target_met': 150000 <= tokens <= 165000,
        'topic_count': len(names), 'reused_identical_topics': sorted(identical),
        'reused_auxiliary_only_changed_topics': auxiliary_only,
        'historical_machine_labels': historical_labels,
        'historical_exposition_changes': history_changes,
        'canonical_diff_line_endings': 'CRLF normalized to LF in derived comparison only',
        'regenerated_topics': list(fresh), 'new_topics': new_topics, 'new_verdicts_exact': True,
        'new_semantic_fields_verified': True, 'mother_v5_full': True, 'operational_core_full': True,
        'formal_sources_full': False, 'formal_sources_available_integrally': True,
        'formal_declaration_excerpts': formal_excerpts, 'references_verified': dict(references),
        'public_document_records': catalog_rows,
        'public_document_index_loaded_scope': 'IDS__HASHES_AND_URLS_AVAILABLE_BY_FETCH_AND_RECEIPT',
        'canonical_legacy_exposition_sha256': parent_receipt['new_exposition_sha256'],
        'canonical_current_amendments': differences, 'duplicate_verdict_roster': roster,
        'source_manifest_sha256': sha(Path(manifest_path).read_bytes()),
        'source_sha256': current['active_cluster']['release_source_sha256'],
        'exposition_sha256': sha(exposition.encode()), 'details_in_source': omitted,
        'scope': 'ACCEPTED_UNCHANGED_CAPSULES_PLUS_EXTRACTIVE_CURRENT_DELTAS__NATIVE_COUNT_PENDING',
        'inputs': {**original_receipt['inputs'], **{str(path): record for path, record in inputs.records.items()}},
    }
    return prefix, receipt


def save_immutable(path, raw):
    path = Path(path).resolve()
    need(path.parent == WORK and path.suffix in ('.md', '.json'), 'Output must be a direct child of this staging directory')
    if path.exists():
        need(path.read_bytes() == raw, 'Existing candidate differs; choose another filename')
        return
    temporary = path.with_name(path.name+'.tmp_'+uuid.uuid4().hex)
    with temporary.open('xb') as stream: stream.write(raw)
    need(raw and temporary.read_bytes() == raw, 'Temporary output verification failed')
    # Windows rename refuses an existing target; no concurrent candidate overwrite.
    temporary.rename(path)


def self_test():
    import unittest
    class BuilderTests(unittest.TestCase):
        def test_projection_semantics_and_lossless_retrieval(self):
            data = {'core': {'sample': {'status': 'OPEN', 'runtime_s': 1.5,
                'record': {'formula': {'a': 'x=1-x', 'b': ['S=1/2', 'J^2=I']},
                           'hypothesis': {'amplitude': 3, 'sign': -1}, 'scope': 'conditional',
                           'series': list(range(50))},
                'rows': [{'statement': 'same statement '*20, 'value': n} for n in range(5)]}}}
            topic = '/core/sample'; omitted = []
            projection = project(data['core']['sample'], topic, topic, omitted)
            encoded, dictionary = intern_topics({'sample': projection}, 'same statement '*20)
            decoded = decode_literals(unpack_metadata(encoded['sample']), dictionary, 'same statement '*20)
            seen = {}
            self.assertEqual(restore(decoded, data, topic, topic, seen), data['core']['sample'])
            for pointer, item in protected_fields(data['core']['sample'], topic).items():
                self.assertTrue(is_represented(pointer, item, seen), pointer)
            self.assertNotIn(topic+'/record/series/0', seen)
            decoded['record']['fields']['/scope'] = 'unconditional'
            with self.assertRaises(ValueError): restore(decoded, data, topic, topic, {})

        def test_group_codec_and_conflicts(self):
            data = {'a': {'@': '/a'}, 'b': {'@': '/b'}, 'c': {'@': '/c', 'items': 2}, 'd': {'@': '/d', 'items': 0}}
            self.assertEqual(unpack_metadata(pack_metadata(data)), data)
            with self.assertRaises(ValueError): unpack_metadata({'a': 1, '@SOURCE_FIELDS': ['a', 'b']})

        def test_pointers_and_duplicate_source(self):
            self.assertEqual(resolve({'a/b': {'~': [9]}}, '/a~1b/~0/0'), 9)
            with self.assertRaises(ValueError): strict_json('{"a":1,"a":2}')
            with self.assertRaises(ValueError): strict_json('{"a":NaN}')
            with self.assertRaises(ValueError): check_reserved({'@': 'ambiguous'})

        def test_wrong_coordinate_and_out_of_range_span(self):
            with self.assertRaises(ValueError): restore({'@': '/other'}, {'core': {'x': {}}}, '/core/x', '/core/x', {})
            with self.assertRaises(ValueError): decode_literals({'@EXPOSITION': [1, 9]}, {}, 'x')

        def test_canonical_only_audit_rows_change(self):
            original = 'formula A=B\n**Escada auditada (2)**\n- `a` = `True`\n- `b` = `False`\n**Next**\nscope\n'
            compacted, rows = compact_exposition(original)
            notice = rows[0]['inserted_notice']; offset = rows[0]['notice_offset']
            self.assertEqual(compacted[offset:offset+len(notice)], notice)
            restored = compacted[:offset]+compacted[offset+len(notice):]
            for row in rows:
                piece = original[row['offset']:row['offset']+row['chars']]
                self.assertEqual(sha(piece.encode()), row['sha256'])
                restored = restored[:row['offset']]+piece+restored[row['offset']:]
            self.assertEqual(restored, original)

        def test_audit_type_change_and_formula_container(self):
            with self.assertRaises(ValueError):
                project({'a': 'new theorem'}, '/core/external_ladder/per_theorem', '/core/external_ladder', [])
            fields = protected_fields({'formulas': {'generic': ['literal equation']}})
            self.assertEqual(fields, {'/formulas': {'generic': ['literal equation']}})


        def test_lean_statement_keeps_assumptions_and_hides_proof(self):
            source = ('/- theorem fake : False := by nope -/\nnamespace N\n'
                      'variable (a : Nat)\nstructure Data where\n  positive : a > 0\n'
                      'theorem test (h : a > 0) : a = a := by\n  rfl\nend N\n')
            excerpt, rows = lean_declaration_excerpt(source)
            self.assertIn('variable (a : Nat)', excerpt)
            self.assertIn('positive : a > 0', excerpt)
            self.assertIn('theorem test (h : a > 0) : a = a', excerpt)
            self.assertNotIn('rfl', excerpt)
            self.assertNotIn('fake', excerpt)
            self.assertEqual([row['name'] for row in rows], ['Data', 'test'])

        def test_primary_formulas_and_statuses_loaded_but_audit_rows_queryable(self):
            source={'core':{'new':{'statuses':{'supplier':'CONDITIONAL with x = y','mode':'KNOWN by citation'},
                'values':{'law':'Gamma = beta * x','scope':'finite'},
                'checks':[['name = repeated audit description',True]]*4}}}
            topic='/core/new'; node=project(source['core']['new'],topic,topic,[])
            node=enrich_new_math(node,source,topic)
            seen={}; self.assertEqual(restore(node,source,topic,topic,seen),source['core']['new'])
            for pointer,value in primary_math_fields(source['core']['new'],topic).items():
                self.assertTrue(is_represented(pointer,value,seen),pointer)
            self.assertNotIn(topic+'/checks/0/0',seen)

        def test_orientation_edit_remaps_the_referenced_summary(self):
            old='conferir o estado da publicação v368 carregado antes de descrevê-los como pendências atuais'
            block='**Estatutos [runtime_synthesis]**\n'+old
            expo='## Runtime\n'+block+'\n'
            start=expo.index('**Estatutos')
            body=dump({'value':{'@SUMMARY':'runtime_synthesis','source_pointer':'/core/t',
                                'span':[start,len(block)]}})
            after,topics,changes=compact_accepted_history(expo,{'t':body},expo,set())
            record=strict_json(topics['t'])['value'];a,n=record['span']
            self.assertTrue(after[a:a+n].startswith('**Estatutos [runtime_synthesis]**'))
            self.assertIn('publicação selecionada deste pacote',after[a:a+n])
            self.assertNotIn(old,after)
            self.assertEqual(len(changes),1)
            self.assertTrue(changes[0]['orientation_only'])

        def test_top_level_bridge_equations_remain_loaded(self):
            topic = '/core/vacuum_impedance_bridge'
            equations = {'impedance': ['Z=mu*c', 'mu=Z/c'], 'scope': 'given normalization'}
            source = {'core': {'vacuum_impedance_bridge': {'bridge_equations': equations}}}
            projected = project(source['core']['vacuum_impedance_bridge'], topic, topic, [])
            self.assertEqual(projected['bridge_equations'], equations)
            seen = {}
            restore(projected, source, topic, topic, seen)
            self.assertTrue(is_represented(topic+'/bridge_equations', equations, seen))
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BuilderTests))
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--app-root', type=Path, default=APP)
    parser.add_argument('--out', type=Path, default=WORK/'haiku_candidate.md')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--fitted', action='store_true')
    parser.add_argument('--baseline-prefix', type=Path)
    parser.add_argument('--baseline-manifest', type=Path)
    args = parser.parse_args()
    if args.self_test: return 0 if self_test() else 1
    need(args.manifest is not None, '--manifest is required')
    if args.fitted:
        prefix, receipt = build_fitted(args.manifest, args.app_root, args.baseline_prefix, args.baseline_manifest)
    else:
        prefix, receipt = build(args.manifest, args.app_root)
    if not args.dry_run:
        output = args.out.resolve()
        need(output.suffix == '.md' and output.parent == WORK, 'Candidate output must be a staging Markdown file')
        receipt_raw = (json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode()
        # Preflight both immutable destinations before the first write.
        for path, raw in ((output, prefix.encode()), (output.with_suffix('.json'), receipt_raw)):
            need(not path.exists() or path.read_bytes() == raw, 'Existing output differs; choose another filename')
        save_immutable(output, prefix.encode())
        save_immutable(output.with_suffix('.json'), receipt_raw)
    print(json.dumps({key: receipt[key] for key in ('status', 'release', 'prefix_sha256', 'bytes', 'topic_count',
        'protected_fields_verified', 'o200k_tokens', 'local_byte_target_met', 'local_token_target_met',
        'native_tokens', 'target_native_tokens', 'native_fit_verified') if key in receipt}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        # Do not dump source text, tokens or exception bodies in a shared log.
        print(json.dumps({'status': 'FAILED_CLOSED', 'exception_type': type(error).__name__}))
        raise SystemExit(1)
