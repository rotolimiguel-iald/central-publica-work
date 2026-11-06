"""Extract the current kernel statements from verified source without running Lean."""
import hashlib
import re


def kernel_highlights(result, proof, root):
    name = 'tetelestai_terminal_v408'
    topic = result['core'][name]
    anchor_map = topic['values']['ancoras']
    equality = 'TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario'
    lines = ['\n### Destaques do kernel v408 — enunciados das fontes seladas\n']
    records = []
    for symbol in [*topic['ancoras_principais'], equality]:
        anchor = anchor_map[symbol]
        path = anchor['declared_in']
        source = (root / path).read_bytes()
        digest = hashlib.sha256(source).hexdigest()
        assert digest == proof['formal_files_sha256'][path]
        assert anchor['ok'] and symbol in proof['axiom_report']
        text = source.decode('utf-8-sig').replace('\r\n', '\n')
        pattern = r'^theorem ' + re.escape(symbol.rsplit('.', 1)[1]) + r'\b.*?(?= :=)'
        matches = list(re.finditer(pattern, text, re.M | re.S))
        assert len(matches) == 1, symbol
        match = matches[0]
        statement = match.group()
        first = text.count('\n', 0, match.start()) + 1
        last = first + statement.count('\n')
        lines.extend([f'[REAL — fonte publicada] {symbol} ({path}, L{first}–{last})', statement])
        records.append(dict(symbol=symbol, path=path, sha256=digest, lines=[first,last], statement=statement))
    limits = [(i, v) for i, v in enumerate(topic['limites']) if 'Turing OPEN' in v and equality.rsplit('.', 1)[1] in v]
    assert len(limits) == 1 and '[OPEN]' in limits[0][1]
    index, limit = limits[0]
    pointer = f'/core/{name}/limites/{index}'
    lines.extend([f'Fonte: resultado_publicado_integral {pointer}', limit])
    return '\n'.join(lines) + '\n', dict(anchors=records, scope_pointer=pointer, scope=limit)
