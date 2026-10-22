"""Independent decoder and source-byte comparison; no builder imports."""
from pathlib import Path
import hashlib
import json
import sys

def decode(value):
    if isinstance(value, list):
        return [decode(v) for v in value]
    if not isinstance(value, dict):
        return value
    result = {k:decode(v) for k,v in value.items() if k not in ('@SOURCE_FIELDS','@SOURCE_ITEMS')}
    for key in ('@SOURCE_FIELDS','@SOURCE_ITEMS'):
        if key not in value:
            continue
        group = value[key]
        assert isinstance(group, list if key == '@SOURCE_FIELDS' else dict)
        assert len(group) >= 2
        seen = set()
        for name in group:
            assert isinstance(name,str) and name and not name.startswith('@')
            assert '/' not in name and '~' not in name and name not in seen and name not in result
            seen.add(name)
            result[name] = {'@':'/'+name}
            if key == '@SOURCE_ITEMS':
                n = group[name]
                assert type(n) is int and n >= 0
                result[name]['items'] = n
    return result

def verify(path):
    path = Path(path)
    receipt = json.loads(path.with_suffix('.json').read_bytes())
    parent = Path(receipt['parent'])
    assert parent.resolve().parent == path.resolve().parent
    before, after = parent.read_bytes(), path.read_bytes()
    from verify_reviewed_draft import verify as verify_parent
    verify_parent(parent)
    assert hashlib.sha256(before).hexdigest() == receipt['parent_sha256']
    assert hashlib.sha256(after).hexdigest() == receipt['sha256']
    text = after.decode('utf-8')
    protocol = receipt['protocol']
    expected_protocol = '\nRemissões compactas: em cada objeto JSON, @SOURCE_FIELDS:[k,...] equivale a k:{"@":"/k"} para cada nome k; @SOURCE_ITEMS:{k:n,...} equivale a k:{"@":"/k","items":n}. As rotas mantêm o tópico Fonte correspondente. São referências ao acervo, não conteúdo integral carregado. items conta itens documentais, não provas. Campos, hipóteses e estatutos retidos permanecem explícitos.\n'
    assert protocol == expected_protocol
    assert text.count(protocol) == 1
    heading = '\n## Fundamento, Um, Meia-Nat e custo geométrico'
    ending = '\n## Exposição canônica integral: fórmulas e derivações'
    original = before.decode('utf-8')
    lower, upper = original.index(heading), original.index(ending)
    assert text.index(protocol) == lower
    text = text.replace(protocol, '', 1)
    oldlines, newlines = before.decode('utf-8').splitlines(keepends=True), text.splitlines(keepends=True)
    assert len(oldlines) == len(newlines)
    changed, position = [], 0
    for number, (old,new) in enumerate(zip(oldlines,newlines)):
        if old != new:
            assert lower <= position < upper
            assert decode(json.loads(new)) == json.loads(old)
            changed.append(number)
            newlines[number] = old
        position += len(old)
    assert changed == receipt['changed_line_numbers_zero_based']
    assert ''.join(newlines).encode('utf-8') == before
    return {'status':'LOSSLESS_METADATA_VERIFIED_NOT_DEPLOYED','changed_json_lines':len(changed),
            'parent_bytes_recovered':True,'draft_sha256':receipt['sha256']}

if __name__ == '__main__':
    print(json.dumps(verify(sys.argv[1]),ensure_ascii=False))
