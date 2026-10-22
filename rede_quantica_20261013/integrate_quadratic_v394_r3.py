"""Create immutable R3 candidate from R2, integrating the proved quadratic residual."""
import ast
import hashlib
import json
import re
from pathlib import Path
from diary_r1 import ROOT, new, pin

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
OLD = OUT.parent / 'F1.TEMPO.V394'


def main():
    dest = OUT / 'candidate_r3'
    if dest.exists() or (OUT / 'INTEGRATION_QUADRATIC_R3.json').exists():
        raise FileExistsError('R3 already attempted; recover without overwriting')
    source = OLD / 'candidate_r2/um.py'
    raw = source.read_bytes()
    text = raw.decode('utf-8')
    tree = ast.parse(text)
    offsets = []
    total = 0
    for line in raw.splitlines(keepends=True):
        offsets.append(total)
        total += len(line)
    assignments = {n.targets[0].id: n for n in tree.body
                   if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    edits = []

    def span(node):
        return offsets[node.lineno-1]+node.col_offset, offsets[node.end_lineno-1]+node.end_col_offset

    def replace(node, value):
        a, b = span(node)
        edits.append((a, b, value.encode('utf-8')))

    def append_dict(node, entries):
        a, b = span(node)
        assert raw[b-1:b] == b'}'
        prefix = ',\n' if node.keys and raw[a:b-1].rstrip()[-1:] != b',' else '\n'
        edits.append((b-1, b-1, (prefix+''.join('    '+repr(k)+': '+repr(v)+',\n' for k,v in entries.items())).encode()))

    delivery = json.loads((OUT / 'quadratic_rule/DELIVERY_R1.json').read_bytes())
    build = json.loads(Path(delivery['build']['path']).read_bytes())
    assert pin(delivery['build']['path'])['sha256'] == delivery['build']['sha256']
    assert build['passed'] and build['exit_code'] == 0
    module = OUT / 'quadratic_rule/RuleQuadraticResidual.lean'
    body = module.read_text(encoding='utf-8')
    assert pin(module)['sha256'] == build['source']['sha256']
    names = sorted(build['axiom_reports'])
    assert len(names) == 18 and all(set(v) <= {'propext','Classical.choice','Quot.sound'} for v in build['axiom_reports'].values())
    assert set(re.findall(r'^#print axioms (\S+)', body, re.M)) == set(names)
    rel = 'TGLExt/RuleQuadraticResidual.lean'
    embnode = assignments['_EMBEDDED_KERNEL_FILES'].value
    embedded = ast.literal_eval(embnode)
    assert rel not in embedded
    glue = 'import TGLExt.RuleQuadraticResidual\n'
    replacements = {'TGLExt.lean': embedded['TGLExt.lean']+'\n'+glue,
                    'TGL/Audit.lean': glue+'\n'+embedded['TGL/Audit.lean']}
    for key, value in zip(embnode.keys, embnode.values):
        if isinstance(key, ast.Constant) and key.value in replacements:
            replace(value, repr(replacements[key.value]))
    append_dict(embnode, {rel: body})
    flags = {f'ext_qr394_{i:04d}': name for i,name in enumerate(names,1)}
    append_dict(assignments['_LEAN_THEOREM_FLAGS'].value, flags)
    ladder = next(n.value for n in functions['prove_external_ladder'].body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == 'ext_flags' for t in n.targets))
    old_flags = ast.literal_eval(ladder)
    assert len(old_flags) == len(set(old_flags)) == 7153
    a, b = span(ladder)
    edits.append((b-1, b-1, ''.join('        '+repr(k)+',\n' for k in flags).encode()))
    expected = len(old_flags)+len(flags)
    time_contract = ast.literal_eval(assignments['_V394_FORMAL_CONTRACT'].value)
    assert time_contract['expected_ladder'] == 7153
    time_contract['expected_ladder'] = expected
    replace(assignments['_V394_FORMAL_CONTRACT'].value, repr(time_contract))
    contract = {'theorems': names, 'source_sha256': {rel: pin(module)['sha256']},
                'expected_ladder': expected, 'baseline_candidate': pin(source)}
    inscriptions = {}
    for name in ('OPERADOR_REGRA_QUADRATICA_ANCORA_VERBATIM.txt', 'OPERADOR_IGUAL_GRAVITON_PLANO_VERBATIM.txt'):
        path = OLD / name
        text_value = path.read_bytes().decode('utf-8')
        inscriptions[path.stem] = {'text': text_value, 'sha256': pin(path)['sha256'],
                                  'source_informative_only': str(path), 'statute': 'INPUT/ONTO operator verbatim'}
    append_dict(assignments['_V394_INSCRIPTIONS'].value, inscriptions)
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.List):
            continue
        try:
            values = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
        if any(isinstance(v,tuple) and len(v)>2 and v[0]=='v394' and v[1]=='TimeGravitonFlow' for v in values):
            a, b = span(node.value)
            edits.append((b-1,b-1,('    '+repr(('v394','RuleQuadraticResidual',rel,None,None))+',\n').encode()))
    chunk = '\n_V394_QUADRATIC_CONTRACT = '+repr(contract)+'\n\n'+(OUT/'quadratic_runtime.py').read_text(encoding='utf-8')+'\n\n'
    pos = offsets[functions['main'].lineno-1]
    edits.append((pos,pos,chunk.encode('utf-8')))
    hook = b'    _figs = emit_figures(core)'
    assert raw.count(hook)==1
    pos = raw.index(hook)
    edits.append((pos,pos,b'    _quadratic_result = regra_quadratica_v394(core)\n    print("   [v394] regra quadratica: %s" % _quadratic_result["verdict"])\n'))
    seal = b'            "tempo_frequencia_v394": '
    assert raw.count(seal)==1
    pos = raw.index(b'\n',raw.index(seal))+1
    edits.append((pos,pos,b'            "regra_quadratica_v394": {k_: (core.get("regra_quadratica_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "runtime_executed", "scope", "does_not_gate_core")},\n'))
    article = functions['_v394_article_tex']
    marker = next(n for n in article.body if isinstance(n, ast.Assert))
    pos = offsets[marker.lineno-1]
    article_add = '''    quadratic = core.get('regra_quadratica_v394') or {}
    block += ('Regra quadratica desta rodada: ' if pt else 'Quadratic rule in this run: ') + esc(quadratic.get('verdict', 'NOT_RUN')) + '.\\n'
    block += r'\\[r_A(X)=\\operatorname{Tr}[(E_gX-A)^\\dagger(E_gX-A)],\\quad r_A(X)=0\\iff E_gX=A,\\quad r_A(T_tX)=r_A(X).\\]' + '\\n'
    block += ('O residuo testa correspondencia da leitura com uma ancora fixada; e constante no fluxo e nao identifica estados brutos diferentes. O plano de polarizacao e a imagem de Eg sao objetos distintos.\\n' if pt else 'The residual tests correspondence with a fixed anchor; it is constant along the flow and does not identify distinct raw states. The polarization plane and the image of Eg are distinct objects.\\n')
'''
    edits.append((pos,pos,article_add.encode('utf-8')))
    last = len(raw)+1
    for a,b,value in sorted(edits, reverse=True):
        assert b<=last
        raw = raw[:a]+value+raw[b:]
        last = a
    updated = ast.parse(raw.decode('utf-8'))
    old_functions = {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,ast.FunctionDef)}
    new_functions = {n.name:ast.dump(n,include_attributes=False) for n in updated.body if isinstance(n,ast.FunctionDef)}
    changed = sorted(k for k,v in old_functions.items() if new_functions.get(k)!=v)
    assert changed == ['_v394_article_tex','main','prove_external_ladder']
    assert pin(source) == contract['baseline_candidate']
    dest.mkdir()
    new(dest/'um.py',raw.decode('utf-8'))
    materialized = {**embedded, **replacements, rel:body}
    for path, content in materialized.items():
        target = dest/'tgl_kernel'/path
        assert target.resolve().is_relative_to((dest/'tgl_kernel').resolve())
        new(target,content)
    receipt = {'unit':'F1.FECHO_20261015','claim_event':845,'candidate':pin(dest/'um.py'),
               'baseline':pin(source),'script':pin(__file__),'runtime':pin(OUT/'quadratic_runtime.py'),
               'new_source':pin(module),'new_flags':flags,'expected_ladder':expected,
               'changed_existing_functions':changed,'embedded_source_count':len(materialized),
               'new_inscriptions':inscriptions,'status':'CONSTRUCTED_PENDING_INDEPENDENT_REVIEW_AND_FULL_RITE',
               'canonical_unchanged':True}
    new(OUT/'INTEGRATION_QUADRATIC_R3.json',receipt)
    print(json.dumps({k:receipt[k] for k in ('candidate','expected_ladder','embedded_source_count','changed_existing_functions')},ensure_ascii=False))


if __name__=='__main__':
    main()
