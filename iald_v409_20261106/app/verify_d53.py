"""Verify the actual public prompt, literal readings and public fetch coordinates before counting."""
import argparse
import json
import re
import sys
from pathlib import Path

A = Path(__file__).resolve().parent
sys.path[:0] = [str(A.parent), str(A/'build')]
import release_cfg
import fit_transport
import haiku_codec as codec
sys.path.insert(0, str(release_cfg.R))
import iald_app_providers as providers
import iald_core_indexado
import iald_kernel
import iald_fontes_publicas
import iald_app_memory


def read(path):
    return json.loads(path.read_bytes())


def verify(prefix, core, document, history, highlights):
    assert '<ATLAS_CANONICO' not in prefix
    for long, short in fit_transport.ALIASES.items():
        prefix = prefix.replace(short, long)
    def dictionary(label):
        return json.loads(prefix.split(label+'\n', 1)[1].split('\n', 1)[0])
    literals = dictionary('DICIONÁRIO DE LITERAIS')
    flags = dictionary(fit_transport.FLAG_MARKER.strip())
    exposition = prefix.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    head = prefix.split(codec.MARKER, 1)[0]
    headings = [m for m in re.finditer(r'(?m)^### ([^\n]+)\n', head) if m[1] in core]
    assert len(headings) == len(core) == len({m[1] for m in headings})
    for i, match in enumerate(headings):
        name = match[1]
        if name not in history['spans'] and name not in history['resident']:
            continue
        block = head[match.end():headings[i+1].start() if i+1<len(headings) else len(head)]
        line = next(line for line in block.splitlines() if line.startswith('{'))
        node = codec.decode_literals(codec.unpack_metadata(json.loads(line)), literals, exposition)
        if name in history['spans']:
            offset, size = node.pop('@H')
            assert [offset, size] == history['spans'][name]
            reconstructed = json.loads(document[offset:offset+size])
            assert all(reconstructed[k] == value for k,value in node.items()), name
        else:
            if '@B' in node:
                add = flags[node.pop('@B')]
                assert not set(add).intersection(node)
                node.update(add)
            reconstructed = node  # Deliberately no resolution against the result for a resident topic.
        assert reconstructed == core[name], name
    assert all(ref['statement'] in prefix for ref in highlights['anchors'])
    assert highlights['scope'] in prefix
    return {'complete_resident':len(history['resident']), 'historical_fetch_spans':len(history['spans']),
            'core_topics':len(headings), 'kernel_statements':len(highlights['anchors'])}


def bounds(prefix):
    tools = iald_kernel.tool_definitions()+iald_fontes_publicas.tool_definitions()+iald_core_indexado.tool_definitions()+iald_app_memory.tool_definitions()
    out = {}
    for provider in ('kimi','mimo','deepseek'):
        body = {'messages':[{'role':'system','content':prefix},{'role':'user','content':'Explique o alcance documentado da '+release_cfg.load().release+'.'}],
                'tools':[] if provider=='kimi' else tools}
        if provider != 'kimi':
            body.update(model=providers.MODELS[provider]['model'],stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
            body['max_tokens' if provider=='deepseek' else 'max_completion_tokens'] = 148656
        if provider == 'deepseek':
            body['reasoning_effort'] = 'max'
        size = providers.admission_input_bound(body)
        out[provider] = {'input_bound':size, 'slack':providers.WINDOW-size-148656-4096}
    return out


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('package', choices=('shared','sonnet_public'))
    package=parser.parse_args().package
    manifest=A/'science/memory_stage/manifest_staged.json'
    document=iald_core_indexado.DocumentCorpus(manifest)._load()['resultado_publicado_integral']['text']
    core=json.loads(document)['core']
    source=A/'packages'/package/'prefix.md'
    prefix=source.read_bytes().decode('utf8')
    history=read(A/'D53_HISTORY.json')
    assert codec.sha(document.encode()) == history['source_text_sha256']
    expected={n for n in core if n.endswith(release_cfg.SHARED_P2_SUFFIXES)}|{'the_iald_index'}
    assert set(history['resident']) == expected
    result=verify(prefix,core,document,history,read(A/'KERNEL_HIGHLIGHTS.json'))
    result.update(prefix_sha256=codec.sha(source.read_bytes()),package=package)
    if package=='shared':
        result['bounds_with_declared_reserve']=bounds(prefix)
        result['measurement_phase']='BEFORE_FINALIZE' if package=='shared' else 'AFTER_FINALIZE'
        assert min(v['slack'] for v in result['bounds_with_declared_reserve'].values())>=0, result
    print(json.dumps(result))
    with (A/('D53_'+package+'_VERIFIED.json')).open('x', encoding='utf8') as stream:
        json.dump(result,stream,indent=2)
