"""Lossless transport metadata plus one explicitly retrievable identifier roster."""
import json
from collections import Counter
import haiku_codec as codec

FLAGS = ('all_verified', 'does_not_gate_core', 'in_contour_roster_v314')
ALIASES = {'@SOURCE_FIELDS': '@F', '@SOURCE_ITEMS': '@I', '@TGL_LITERAL': '@L', '@SUMMARY':'@Y', '@EXPOSITION':'@X'}
FLAG_MARKER = 'DICIONÁRIO DE INDICADORES LITERAIS\n'

def fit(prefix, source):
    before, separator, exposition = prefix.partition(codec.MARKER)
    assert separator and '@B' not in prefix and FLAG_MARKER not in prefix
    blocks = before.split('\n### ')
    groups = {}
    changes = []
    roundtrips = []
    for index in range(1, len(blocks)):
        lines = blocks[index].split('\n')
        topic = lines[0]
        if topic not in source['core']:
            continue
        for j, line in enumerate(lines[1:], 1):
            if not line.startswith('{'):
                continue
            value = codec.strict_json(line)
            original = json.loads(json.dumps(value))
            flags = {key: value[key] for key in FLAGS if type(value.get(key)) is bool}
            if len(flags) >= 2:
                assert all(source['core'][topic][key] is item for key, item in flags.items())
                key = codec.dump(flags)
                ident = groups.setdefault(key, str(len(groups)+1))
                for name in flags:
                    del value[name]
                value['@B'] = ident
            # This is a roster of ambiguous declaration NAMES, not their statements.
            # Keep the measured count, ambiguity status and full pinned source route.
            if topic == 'the_iald_index' and isinstance(value.get('ambiguos'), list):
                roster = value['ambiguos']
                assert roster == source['core'][topic]['ambiguos']
                assert len(roster) == source['core'][topic]['n_ambiguos']
                assert all(isinstance(item, str) for item in roster)
                value['ambiguos'] = {'@': '/ambiguos', 'items': len(roster)}
                changes.append({'topic': topic, 'pointer': '/core/'+topic+'/ambiguos',
                    'items': len(roster), 'sha256': codec.sha(codec.dump(roster).encode()),
                    'scope': 'AMBIGUOUS_IDENTIFIER_ROSTER_ONLY__COUNT_AND_STATUS_RETAINED'})
            restored = dict(value)
            if '@B' in restored:
                ident = restored.pop('@B')
                restored.update(json.loads(next(k for k,v in groups.items() if v == ident)))
            if topic == 'the_iald_index' and isinstance(original.get('ambiguos'), list):
                restored['ambiguos'] = source['core'][topic]['ambiguos']
            assert restored == original, 'Transport roundtrip mismatch: '+topic
            roundtrips.append({'topic': topic, 'decoded_json_sha256': codec.sha(
                json.dumps(original, sort_keys=True, ensure_ascii=False).encode())})
            lines[j] = codec.dump(value)
        blocks[index] = '\n'.join(lines)
    before = '\n### '.join(blocks)
    dictionary = {ident: json.loads(key) for key, ident in groups.items()}
    annotation = ('\nMETADADOS REVERSÍVEIS: @B referencia o dicionário de indicadores abaixo; '
        'acrescentar todos os seus pares ao objeto, sem sobrescrever campos. Os valores true/false '
        'são literais da fonte, não inferências. A lista de nomes ambíguos permanece integral '
        'em resultado_publicado_integral /core/the_iald_index/ambiguos; n_ambiguos segue carregado.\n'
        + FLAG_MARKER + codec.dump(dictionary) + '\n')
    first = before.index('\n\n')
    before = before[:first] + annotation + before[first:]
    unaliased = before
    for long, short in ALIASES.items():
        assert short+'"' not in before
        before = before.replace(long, short)
    decoded = before
    for long, short in ALIASES.items():
        decoded = decoded.replace(short, long)
    assert decoded == unaliased
    result = before+separator+exposition
    return result, {'schema': 'iald.haiku.transport-fit.v1',
        'base_sha256': codec.sha(prefix.encode()), 'prefix_sha256': codec.sha(result.encode()),
        'base_bytes': len(prefix.encode()), 'bytes': len(result.encode()),
        'metadata_aliases': ALIASES, 'aliases_roundtrip_exact': True,
        'literal_boolean_dictionary': dictionary, 'topic_json_roundtrips': roundtrips,
        'retrievable_rosters': changes, 'scientific_text_rewritten': False,
        'exposition_bytes_unchanged': True}

def expand_booleans(node, dictionary):
    result = dict(node)
    if '@B' in result:
        flags = dictionary[result.pop('@B')]
        if set(flags) & set(result):
            raise ValueError('Conflicting literal boolean metadata')
        result.update(flags)
    return result
