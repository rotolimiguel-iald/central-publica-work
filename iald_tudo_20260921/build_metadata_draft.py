"""Prepare a reversible metadata-only derivative; never deploy or contact APIs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import sys
from compact_source_fields import pack
from compact_source_items import pack_items
from verify_reviewed_draft import verify

W = Path(__file__).resolve().parent
START = '\n## Fundamento, Um, Meia-Nat e custo geométrico'
END = '\n## Exposição canônica integral: fórmulas e derivações'
PROTOCOL = '\nRemissões compactas: em cada objeto JSON, @SOURCE_FIELDS:[k,...] equivale a k:{"@":"/k"} para cada nome k; @SOURCE_ITEMS:{k:n,...} equivale a k:{"@":"/k","items":n}. As rotas mantêm o tópico Fonte correspondente. São referências ao acervo, não conteúdo integral carregado. items conta itens documentais, não provas. Campos, hipóteses e estatutos retidos permanecem explícitos.\n'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def main():
    parent = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else W / 'haiku_reviewed_runtime_20260922_134847_707064.md'
    verified = verify(parent)
    raw = parent.read_bytes()
    text = raw.decode('utf-8')
    lo, hi = text.index(START), text.index(END)
    output, changes, pos = [], [], 0
    for number, line in enumerate(text.splitlines(keepends=True)):
        inside = lo <= pos < hi
        pos += len(line)
        replacement = line
        if inside:
            try:
                node = json.loads(line)
            except ValueError:
                node = None
            if node is not None:
                packed = pack_items(pack(node))
                if packed != node:
                    ending = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
                    replacement = json.dumps(packed, ensure_ascii=False, separators=(',', ':')) + ending
                    changes.append(number)
        output.append(replacement)
    body = ''.join(output)
    assert body[:lo] == text[:lo] and body[body.index(END):] == text[hi:]
    body = body[:lo] + PROTOCOL + body[lo:]
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    target = W / ('haiku_metadata_proposal_' + stamp + '.md')
    result = body.encode('utf-8')
    assert parent.read_bytes() == raw
    with target.open('xb') as stream:
        stream.write(result)
    receipt = {'status':'PROPOSAL_NOT_DEPLOYED', 'parent':str(parent),
               'parent_sha256':digest(raw), 'sha256':digest(result),
               'protocol':PROTOCOL, 'changed_line_numbers_zero_based':changes,
               'parent_verification':verified}
    with target.with_suffix('.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
    print(target)

if __name__ == '__main__':
    main()
