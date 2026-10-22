"""Build an extractive candidate; preserve originals, exact JSON pointers and equations.

This is a draft, not a ratified canon or a deployment. No network calls.
"""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from collections import Counter

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('TIKTOKEN_CACHE_DIR', str(ROOT / '.iald_runtime/tokenizer_cache'))
import tiktoken
from iald_instrucao_mae import mother_instruction
from iald_core_indexado import operational_core
from iald_response_contract import IDENTITY_PROTOCOL, SOLUTION_PROTOCOL
from iald_kernel import KernelCatalog
from iald_estado_publicado import published_evidence

ENC = tiktoken.get_encoding('o200k_base')
OMITTED = []
AUXILIARY_TOPIC_KEYS = frozenset(('runtime_s', 'protocol_hash', 'frozen_hash',
                                  'result_sha16', 'catalog_sha16', 'result_path'))
ESSENTIAL_FIELD = re.compile(
    r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|'
    r'scope|escopo|status|estatuto|verdict|veredito|claim|statement|enunciad|theorem|teorema|'
    r'lagrang|hamilton|lindblad|dephas|comuta|commut', re.I)


def pointer_child(pointer, key):
    return pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')


def protected_fields(node, location):
    fields = []
    if isinstance(node, dict):
        for key, item in node.items():
            child = pointer_child(location, key)
            if re.search(r'hypothes|hip[oó]tes|assumption|premiss|statement|enunciad', key, re.I):
                # A hypothesis owns its contents even when children have generic
                # names such as amplitude/sign/value. Preserve its entire value.
                fields.append({'pointer': child, 'value': item})
            elif ESSENTIAL_FIELD.search(key) and not isinstance(item, (dict, list)):
                fields.append({'pointer': child, 'value': item})
            else:
                fields.extend(protected_fields(item, child))
    elif isinstance(node, list):
        for index, item in enumerate(node):
            fields.extend(protected_fields(item, pointer_child(location, index)))
    return fields


def compact_references(node, topic_pointer):
    """Shorten only generated metadata; scalar source content remains literal."""
    if isinstance(node, list):
        return [compact_references(v, topic_pointer) for v in node]
    if not isinstance(node, dict):
        return node
    if 'DETAILS_IN_SOURCE' in node:
        full = node['DETAILS_IN_SOURCE']
        if not full.startswith(topic_pointer):
            raise ValueError('Reference escaped topic')
        result = {'@': full[len(topic_pointer):]}
        if 'protected_fields' in node:
            fields = {}
            for field in node['protected_fields']:
                if not field['pointer'].startswith(full + '/'):
                    raise ValueError('Protected field escaped source')
                fields[field['pointer'][len(full):]] = field['value']
            if fields:
                result['fields'] = fields
        for key, value in node.items():
            if key not in ('DETAILS_IN_SOURCE', 'protected_fields', 'reading'):
                result[key] = value
        return result
    return {k: compact_references(v, topic_pointer) for k, v in node.items()}


def capsule(value, pointer, depth=0):
    # These records distinguish constructed regular witnesses from the specific
    # canonical target. Dropping them leaves historical negatives unbalanced.
    if pointer in ('/core/interface_is_light/witness_layers',
                   '/core/interface_is_light/light_chain'):
        return value
    # Top-level assertions, formulas, hypotheses and status strings remain literal.
    # Long collections become explicit source references; never claim they were read.
    if pointer == '/core/external_ladder/per_theorem':
        if not isinstance(value, dict) or not all(type(v) is bool for v in value.values()):
            raise ValueError('Per-theorem audit now contains non-boolean content; review required')
        OMITTED.append({'pointer': pointer, 'reason': 'individual_boolean_audit_indicators'})
        return {'DETAILS_IN_SOURCE': pointer,
                'true_fields': sum(value.values()), 'false_fields': len(value) - sum(value.values()),
                'reading': 'Indicadores individuais de auditoria recuperáveis; não são enunciados nem nova contagem de teoremas.'}
    if pointer in ('/core/kernel_formalization/axiom_report',
                   '/core/kernel_formalization/formal_files_sha256'):
        OMITTED.append({'pointer': pointer, 'reason': 'complete_audit_report_retrievable'})
        return {'DETAILS_IN_SOURCE': pointer,
                'reading': 'Relatório completo de auditoria disponível para consulta; não constitui conteúdo matemático da instrução-mãe.'}
    if isinstance(value, dict):
        if pointer == '/core/kernel_formalization':
            flags = {k: v for k, v in value.items() if isinstance(v, bool)}
            retained = {k: capsule(v, pointer_child(pointer, k), depth + 1)
                        for k, v in value.items() if not isinstance(v, bool)}
            retained['individual_audit_flags'] = {
                'DETAILS_IN_SOURCE': pointer,
                'true_fields': sum(v is True for v in flags.values()),
                'false_fields': sum(v is False for v in flags.values()),
                'reading': 'Contagem de campos booleanos do relatório, não contagem de teoremas. Consultar o campo exato antes de atribuir prova.'}
            OMITTED.extend({'pointer': pointer_child(pointer, k), 'reason': 'individual_audit_flag'} for k in flags)
            return retained
        if depth >= 1:
            # Detailed evidence stays recoverable. Preserve scope/formula fields
            # wherever they occur, with their full source coordinates.
            protected = protected_fields(value, pointer)
            OMITTED.append({'pointer': pointer, 'items': len(value), 'reason': 'structured_evidence'})
            return {'DETAILS_IN_SOURCE': pointer, 'protected_fields': protected}
        retained = {}
        for key, item in value.items():
            if depth == 0 and key in AUXILIARY_TOPIC_KEYS and not isinstance(item, (dict, list)):
                OMITTED.append({'pointer': pointer_child(pointer, key),
                                'reason': 'auxiliary_topic_metadata_retrievable'})
            else:
                retained[key] = capsule(item, pointer_child(pointer, key), depth + 1)
        return retained
    if isinstance(value, list) and len(value) > 3:
        # Preserve all records containing equations, statements or scope information.
        if any(isinstance(item, str) for item in value):
            return [capsule(item, pointer_child(pointer, i), depth + 1)
                    for i, item in enumerate(value)]
        OMITTED.append({'pointer': pointer, 'items': len(value), 'reason': 'detailed_collection'})
        return {'DETAILS_IN_SOURCE': pointer, 'items': len(value),
                'protected_fields': protected_fields(value, pointer),
                'reading': 'Coleção detalhada disponível na fonte; conteúdo não carregado neste recorte.'}
    if isinstance(value, list):
        return [capsule(item, pointer_child(pointer, i), depth + 1) for i, item in enumerate(value)]
    return value


def store(path, raw):
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if path.exists():
        old = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + stamp)
        with backup.open('xb') as f:
            f.write(old)
        if backup.read_bytes() != old:
            raise RuntimeError('Backup mismatch')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as f:
        f.write(raw)
    if temp.read_bytes() != raw:
        raise RuntimeError('Temporary file mismatch')
    temp.replace(path)


def main():
    path = ROOT / 'iald_nucleo_fixo.json'
    manifest = json.loads(path.read_bytes())
    cfg = manifest['active_cluster']
    raw = Path(cfg['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != cfg['sha256']:
        raise ValueError('Cluster integrity mismatch')
    text = raw.decode('utf-8')
    marker = '## Exposição canônica integral: fórmulas e derivações'
    if text.count(marker) != 1:
        raise ValueError('Canonical exposition boundary missing or ambiguous')
    topic_text, exposition = text.split(marker, 1)
    mother, _ = mother_instruction(manifest['mother_instruction'])
    core, _ = operational_core(path)
    result_entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
    result_raw = Path(result_entry['path']).read_bytes()
    if hashlib.sha256(result_raw).hexdigest() != result_entry['public_sha256']:
        raise ValueError('Published result integrity mismatch')
    result = json.loads(result_raw)
    catalog = KernelCatalog(cfg['kernel_bundle'], cfg['kernel_verification'])
    formal_evidence, formal_metadata = published_evidence(manifest['published_evidence'], catalog)
    # The long ladder repeats audit identifiers. Keep its heading/overall status,
    # all mathematical prose and formulas; retrieve the itemized audit on demand.
    audit_start = exposition.index('**Escada auditada (')
    next_heading = exposition.find('\n**', audit_start + 2)
    if next_heading < 0:
        raise ValueError('Audit ladder boundary not found')
    audit_area = exposition[audit_start:next_heading]
    audit_rows = list(re.finditer(r'(?m)^- `[^`\n]+` = `[^`\n]+`\r?$', audit_area))
    if not audit_rows:
        raise ValueError('No audit rows found')
    form_entry = next(e for e in manifest['entries'] if e['id'] == 'um_forma_canonica_integral')
    form_raw = Path(form_entry['path']).read_bytes()
    if hashlib.sha256(form_raw).hexdigest() != form_entry['public_sha256']:
        raise ValueError('Canonical exposition source changed')
    form_text = form_raw.decode('utf-8-sig')
    audit_offsets = []
    for row in audit_rows:
        line = row.group(0).rstrip('\r')
        offset = form_text.find(line)
        if offset < 0:
            raise ValueError('Audit row absent from recoverable canonical document')
        audit_offsets.append({'offset': offset, 'chars': len(line)})
    trimmed_area = re.sub(r'(?m)^- `[^`\n]+` = `[^`\n]+`\r?\n?', '', audit_area)
    trimmed_area += ('\nLista individual de indicadores: disponível por fetch_tgl, id=um_forma_canonica_integral, '
                     'offset=' + str(min(r['offset'] for r in audit_offsets)) +
                     '. Seguir next_offset para continuar. São ' + str(len(audit_rows)) +
                     ' registros desta lista, não nova contagem de provas. Os conceitos e vereditos '
                     'dos tópicos permanecem nas cápsulas acima.\n')
    exposition = exposition[:audit_start] + trimmed_area + exposition[next_heading:]
    verdict_topics = {}
    for name, node in result['core'].items():
        if isinstance(node, dict) and isinstance(node.get('verdict'), str):
            verdict_topics.setdefault(node['verdict'], []).append(name)
    deduplicated_verdicts = []
    def deduplicate_verdict(match):
        names = verdict_topics.get(match.group(2), [])
        # Only refer to topics actually included in this candidate.
        names = [name for name in names if '\n### ' + name + '\n' in topic_text]
        if not names:
            return match.group(0)
        deduplicated_verdicts.append({'heading': match.group(1), 'topic': names[0], 'value': match.group(2)})
        return '**Estatutos [' + match.group(1) + ']** (veredito literal no tópico `' + names[0] + '` acima):'
    exposition = re.sub(r'\*\*Estatutos \[([^\]]+)\]\*\* \(veredito: `([^`]+)`\):', deduplicate_verdict, exposition)
    rows = []
    parts = []
    topic_nodes = []
    count = 0
    for line in topic_text.splitlines():
        if line.startswith('## '):
            parts.append('\n' + line)
        elif line.startswith('### '):
            topic = line[4:]
            if topic not in result['core']:
                raise ValueError('Topic absent from published JSON: ' + topic)
            pointer = pointer_child('/core', topic)
            # Use the published result, rather than treating an old capsule as proof.
            node = result['core'][topic]
            projected = capsule(node, pointer)
            compact = compact_references(projected, pointer)
            topic_nodes.append((topic, pointer, compact))
            body = json.dumps(compact, ensure_ascii=False, separators=(',', ':'))
            parts.append('\n### ' + topic + '\nFonte: resultado_publicado_integral ' + pointer + '\n' + body)
            rows.append({'id': topic, 'pointer': pointer,
                         'o200k_tokens': len(ENC.encode(body, disallowed_special=()))})
            count += 1
    if count != cfg['core_sections']:
        raise ValueError('Missing topic coverage')
    frequency = Counter()
    def count_literals(node):
        if isinstance(node, dict):
            if '@TGL_LITERAL' in node:
                raise ValueError('Reserved metadata key present in source')
            for value in node.values():
                count_literals(value)
        elif isinstance(node, list):
            for value in node:
                count_literals(value)
        elif isinstance(node, str) and len(node) >= 80:
            frequency[node] += 1
    for _, _, node in topic_nodes:
        count_literals(node)
    repeated = sorted((value for value, n in frequency.items() if n > 1),
                      key=lambda value: (-frequency[value] * len(value), value))
    dictionary = {value: 'L' + str(i + 1) for i, value in enumerate(repeated)}
    cross_references = []
    referenced_literals = set()
    def intern(node):
        if isinstance(node, str) and len(node) >= 100 and node in exposition:
            start = exposition.index(node)
            cross_references.append({'start': start, 'chars': len(node)})
            headings = re.findall(r'(?m)^#{1,6} .+$', exposition[:start])
            return {'@EXPOSITION': headings[-1] if headings else marker,
                    'starts_with': node[:60], 'span': [start, len(node)]}
        if isinstance(node, str) and node in dictionary:
            referenced_literals.add(dictionary[node])
            return {'@TGL_LITERAL': dictionary[node]}
        if isinstance(node, dict):
            return {k: intern(v) for k, v in node.items()}
        if isinstance(node, list):
            return [intern(v) for v in node]
        return node
    for _, pointer, node in topic_nodes:
        old = json.dumps(node, ensure_ascii=False, separators=(',', ':'))
        new = json.dumps(intern(node), ensure_ascii=False, separators=(',', ':'))
        for i, part in enumerate(parts):
            if part.endswith('\n' + old) and (' ' + pointer + '\n') in part:
                parts[i] = part[:-len(old)] + new
                break
        else:
            raise ValueError('Topic replacement failed')
    # Exposition references take precedence over dictionary references. Their
    # unused dictionary copies must not occupy the permanent context twice.
    unused_literals = {value: ident for value, ident in dictionary.items()
                       if ident not in referenced_literals}
    if any(value not in exposition for value in unused_literals):
        raise ValueError('Unused literal lacks an exact copy in loaded exposition')
    dictionary = {value: ident for value, ident in dictionary.items()
                  if ident in referenced_literals}
    glossary = json.dumps({ident: value for value, ident in dictionary.items()}, ensure_ascii=False, separators=(',', ':'))
    header = ('RASCUNHO EXTRATIVO — NÃO IMPLANTADO.\n'
              'IALD é regime operacional; TGL é teoria física. Fontes preservam estatutos e história.\n'
              'Versão do pacote: ' + cfg['release'] + '; programa SHA256: ' + cfg['release_source_sha256'] + '.\n'
              'As seções abaixo citam resultados publicados, não nova execução ou auditoria de provas.\n')
    header += ('METADADOS: @ indica detalhes NÃO carregados: concatenar seu valor ao ponteiro Fonte do tópico. '
               'fields contém valores literais preservados; suas chaves são caminhos relativos ao @. '
               'items conta registros, nunca provas; true_fields/false_fields contam indicadores de auditoria, nunca teoremas. '
               'Consultar a fonte antes de atribuir demonstração a um indicador.\n')
    header += ('DICIONÁRIO DE LITERAIS: @TGL_LITERAL referencia o texto integral abaixo, compartilhado entre fontes; '
               'a referência preserva o valor, não acrescenta estatuto.\n' + glossary + '\n')
    header += ('Metadados auxiliares de cada tópico (runtime_s, protocol_hash, frozen_hash, result_sha16, '
               'catalog_sha16, result_path) permanecem na Fonte por sua chave original; não estão carregados. '
               'O hash de ancoragem do pacote e as fontes nucleares continuam explícitos.\n')
    header += ('@EXPOSITION indica texto idêntico já presente na seção nomeada da exposição integral abaixo; '
               'starts_with identifica o começo literal da passagem. '
               'span=[offset,comprimento] usa caracteres Unicode, começando imediatamente após o título principal da exposição (inclui a quebra de linha). '
               'É referência interna a conteúdo carregado, não consulta externa nem omissão.\n')
    prefix = (header + IDENTITY_PROTOCOL + '\n' + SOLUTION_PROTOCOL + '\n' + mother + '\n' + core +
              '\n' + formal_evidence + '\n' +
              '\n'.join(parts) + '\n' + marker + exposition + '\n' + IDENTITY_PROTOCOL + '\n' + SOLUTION_PROTOCOL)
    data = prefix.encode('utf-8')
    tokens = len(ENC.encode(prefix, disallowed_special=()))
    receipt = {'status': 'DRAFT_NOT_DEPLOYED', 'release': cfg['release'],
               'source_cluster_sha256': cfg['sha256'], 'sha256': hashlib.sha256(data).hexdigest(),
               'o200k_tokens': tokens, 'haiku_tokens': None, 'target_haiku_tokens': 180000,
               'topic_count': count, 'kernel_full': True, 'memory_core_full': True,
               'exposition_full': False, 'exposition_change': 'itemized_audit_ladder_retrievable',
               'audit_ladder_source_id': form_entry['id'], 'audit_ladder_source_sha256': form_entry['public_sha256'],
               'audit_ladder_offsets': audit_offsets, 'omitted_numeric_series': OMITTED, 'topics': rows}
    receipt['shared_literal_count'] = len(dictionary)
    receipt['fixed_hypothesis_sources'] = formal_metadata['fixed_hypothesis_sources']
    receipt['published_evidence_checked'] = formal_metadata['published_evidence_checked']
    receipt['deduplicated_verdicts'] = deduplicated_verdicts
    receipt['exposition_cross_references'] = cross_references
    receipt['exposition_chars'] = len(exposition)
    receipt['exposition_sha256'] = hashlib.sha256(exposition.encode('utf-8')).hexdigest()
    store(WORK / 'haiku_candidate.md', data)
    store(WORK / 'haiku_candidate.json', (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode())
    print(json.dumps({k: v for k, v in receipt.items() if k not in ('topics', 'omitted_numeric_series', 'exposition_cross_references', 'audit_ladder_offsets', 'deduplicated_verdicts', 'fixed_hypothesis_sources')}))


if __name__ == '__main__':
    main()
