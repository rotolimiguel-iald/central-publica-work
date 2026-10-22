"""Read-only local adversarial review. No project imports, network or API calls."""
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import socket

BASE = Path(__file__).resolve().parent
WORK = BASE.parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
def blocked(*args, **kwargs):
    raise RuntimeError('Network forbidden in local audit')
socket.socket = blocked
import tiktoken
ENC = tiktoken.get_encoding('o200k_base')
def tokens(text):
    return len(ENC.encode(text, disallowed_special=()))
def digest(raw):
    return hashlib.sha256(raw).hexdigest()
def dump(node):
    return json.dumps(node, ensure_ascii=False, separators=(',', ':'))
def output(name, node):
    raw = (json.dumps(node, ensure_ascii=False, indent=2) + '\n').encode()
    path = BASE / name
    if path.exists():
        raise RuntimeError('Refuse overwrite: ' + str(path))
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.replace(path)

files = ['haiku_candidate.md', 'haiku_candidate.json', 'build_haiku_candidate.py',
         'verify_haiku_candidate.py', 'audit_haiku_essential_fields.py']
before = {name: digest((WORK / name).read_bytes()) for name in files}
raw = (WORK / files[0]).read_bytes()
text = raw.decode('utf-8')
receipt = json.loads((WORK / files[1]).read_bytes())
assert digest(raw) == receipt['sha256']
count = json.loads((WORK / 'haiku_count.json').read_bytes())
assert count['candidate_sha256'] == digest(raw)
manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
protected = []
source_checks = {}
for name in ('mother_instruction', 'operational_core'):
    cfg = manifest[name]
    source_raw = Path(cfg['path']).read_bytes()
    assert digest(source_raw) == cfg['sha256']
    value = source_raw.decode('utf-8-sig')
    assert value in text
    protected.append(value)
    source_checks[name] = {'bytes': len(source_raw), 'sha256': digest(source_raw),
                           'literal_in_candidate': True, 'config': cfg}
entry = next(e for e in manifest['entries'] if e['id'] == 'resultado_publicado_integral')
source_raw = Path(entry['path']).read_bytes()
assert digest(source_raw) == entry['public_sha256']
source = json.loads(source_raw)
pattern = re.compile(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)')
matches = list(pattern.finditer(text))
assert len(matches) == len(receipt['topics']) == 325
nodes = [json.loads(m[3]) for m in matches]
key_counts = collections.Counter()
str_counts = collections.Counter()
key_costs = collections.Counter()
def walk(node):
    if isinstance(node, dict):
        for key, value in node.items():
            key_counts[key] += 1
            key_costs[key] += tokens(dump(key) + ':')
            walk(value)
    elif isinstance(node, list):
        for item in node: walk(item)
    elif isinstance(node, str): str_counts[node] += 1
for node in nodes: walk(node)

# Fully reversible key aliases: only keys repeated enough to repay the dictionary.
aliases = {}
for key, frequency in key_counts.most_common():
    alias = '~' + str(len(aliases))
    saving = frequency * (tokens(dump(key)) - tokens(dump(alias))) - tokens(dump({alias: key}))
    if saving > 5 and len(key) > 8:
        aliases[key] = alias
assert not (set(aliases.values()) & set(key_counts))
def alias_keys(node, reverse=False):
    mapping = {v:k for k,v in aliases.items()} if reverse else aliases
    if isinstance(node, dict): return {mapping.get(k,k):alias_keys(v,reverse) for k,v in node.items()}
    if isinstance(node, list): return [alias_keys(v,reverse) for v in node]
    return node
changed = [alias_keys(node) for node in nodes]
assert [alias_keys(node, True) for node in changed] == nodes
def replace_nodes(values, prefix=''):
    result = text
    for match, node in reversed(list(zip(matches, values))):
        result = result[:match.start(3)] + dump(node) + result[match.end(3):]
    return prefix + result
legend = 'ALIASES DE CHAVES JSON (expansão literal; estatutos e valores inalterados):\n' + dump({v:k for k,v in aliases.items()}) + '\n'
variant_a = replace_nodes(changed, legend)

# Dictionary for repeated identifier components in topic JSON keys/values only.
# Exact restoration is checked against each original JSON body; no prose is dropped.
bodies = [dump(n) for n in nodes]
ident_counts = collections.Counter(re.findall(r'[A-Za-z_][A-Za-z_0-9]{9,}', '\n'.join(bodies)))
ids = {}
for ident, freq in ident_counts.most_common():
    alias = '§' + str(len(ids)) + '§'
    saving = freq * (tokens(ident) - tokens(alias)) - tokens(dump({alias: ident}))
    if saving > 5:
        ids[ident] = alias
assert not re.search(r'§\d+§', ''.join(bodies))
ident_re = re.compile(r'[A-Za-z_][A-Za-z_0-9]{9,}')
new_bodies = [ident_re.sub(lambda m:ids.get(m[0],m[0]), b) for b in bodies]
reverse_ids = {v:k for k,v in ids.items()}
for old, new in zip(bodies,new_bodies):
    restored = re.sub(r'§\d+§',lambda m:reverse_ids[m[0]],new)
    assert old == restored
variant_b = text
for match, body in reversed(list(zip(matches,new_bodies))):
    variant_b = variant_b[:match.start(3)] + body + variant_b[match.end(3):]
variant_b = ('DICIONÁRIO LOCAL: expandir cada §n§ literalmente, inclusive dentro de chaves e valores JSON. Não muda estatuto.\n' + dump(reverse_ids) + '\n' + variant_b)

# Deduplicate arbitrary exact repeated string values with explicit local references.
values = {}
for value, freq in str_counts.most_common():
    alias = 'R' + str(len(values))
    saving = freq*(tokens(dump(value))-tokens(dump({'@R':alias})))-tokens(dump({alias:value}))
    if freq > 1 and saving > 5: values[value] = alias
def intern(node):
    if isinstance(node,str) and node in values: return {'@R':values[node]}
    if isinstance(node,dict): return {k:intern(v) for k,v in node.items()}
    if isinstance(node,list): return [intern(v) for v in node]
    return node
value_legend = 'LITERAIS compartilhados: @R remete ao valor integral abaixo, com o mesmo estatuto.\n' + dump({v:k for k,v in values.items()}) + '\n'
variant_c = replace_nodes([alias_keys(intern(n)) for n in nodes],legend + value_legend)

variants = {}
for name, variant in [('key_aliases',variant_a),('identifier_dictionary',variant_b),('keys_and_repeated_values',variant_c)]:
    assert all(p in variant for p in protected)
    original_exposition = text.split('## Exposição canônica integral: fórmulas e derivações',1)[1]
    assert variant.endswith(original_exposition)
    variants[name] = {'o200k_tokens':tokens(variant),'saved_o200k':tokens(text)-tokens(variant),
                      'haiku_tokens':'NOT_MEASURED', 'protected_blocks_literal':True,
                      'exposition_suffix_literal':True}

# Independently identify source strings missed by the builder's name-based selector.
essential = re.compile(r'formula|equation|equacao|equaç|hypothes|hip[oó]tes|assumption|premiss|scope|escopo|status|estatuto|verdict|veredito|claim|theorem|teorema|lagrang|hamilton|lindblad|dephas|comuta|commut',re.I)
missing = []
def scan(node,pointer):
    if isinstance(node,dict):
        for k,v in node.items():
            p=pointer+'/'+k.replace('~','~0').replace('/','~1')
            if isinstance(v,str) and len(v)>=40 and v not in text and dump(v)[1:-1] not in text:
                missing.append({'pointer':p,'value':v,'selected_by_regex':bool(essential.search(k))})
            scan(v,p)
    elif isinstance(node,list):
        for i,v in enumerate(node):
            p=pointer+'/'+str(i)
            if isinstance(v,str) and len(v)>=40 and v not in text and dump(v)[1:-1] not in text:
                missing.append({'pointer':p,'value':v,'selected_by_regex':False})
            scan(v,p)
for row in receipt['topics']: scan(source['core'][row['id']],row['pointer'])
after = {name: digest((WORK / name).read_bytes()) for name in files}
assert before == after, 'Concurrent candidate/source changes: discard measurement'
results = {'status':'LOCAL_MEASUREMENT_NOT_SEMANTIC_APPROVAL','input_hashes':before,
 'o200k_tokens':tokens(text),'anthropic_receipt':count,'source_checks':source_checks,
 'source_result_sha256':digest(source_raw),'topics':len(nodes),
 'topic_body_o200k_sum':sum(tokens(b) for b in bodies),
 'key_alias_count':len(aliases),'identifier_alias_count':len(ids),'value_alias_count':len(values),
 'variants':variants,'top_key_costs':key_costs.most_common(45),
 'top_identifiers':[(k,v,tokens(k)) for k,v in ident_counts.most_common(35)],
 'missing_source_strings':len(missing),'missing_regex_strings':sum(r['selected_by_regex'] for r in missing),
 'input_files_unchanged':True}
output('measurements.json',results)
output('missing_source_strings.json',missing)
output('reversible_dictionaries.json',{'keys':aliases,'identifiers':ids,'values':values})
print(json.dumps(results,ensure_ascii=False,indent=2))
