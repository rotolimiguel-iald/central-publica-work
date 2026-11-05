"""numeros extras para o parecer: tamanho dos blocos por sufixo no shared (v407 e v406 instalada), capacidade de conversa pelas formulas do runtime, distribuicao dos blocos _v402."""
import json, re, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104'); R = Path(r'C:\IALD\projetos_pyhton\IALD')
V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']
m_inst = json.loads((R / 'iald_nucleo_fixo.json').read_bytes()); core6 = json.loads(Path(m_inst['published_evidence']['result']['path']).read_bytes())['core']
P7 = L.parse_prefix((W / 'app/packages/shared/prefix.md').read_text('utf-8'))
P6 = L.parse_prefix((R / '.iald_runtime/haiku/prefix.md').read_text('utf-8'))
H7 = L.parse_prefix((W / 'app/packages/haiku_expanded/prefix.md').read_text('utf-8'))
H6 = L.parse_prefix((R / '.iald_runtime/haiku55/prefix.md').read_text('utf-8'))
suf = lambda n: (re.search(r'_(v40\d)$', n) or [None, 'older'])[1]
def sizes(P, names):
    d = {}
    for n in names:
        if n in P['body']:
            d[suf(n)] = d.get(suf(n), 0) + len(P['body'][n].encode())
    return dict(sorted(d.items()))
out = {'shared_block_bytes_by_suffix_v407': sizes(P7, core), 'shared_block_bytes_by_suffix_v406_installed': sizes(P6, core6),
       'haiku_expanded_block_bytes_by_suffix_v407': sizes(H7, core), 'haiku55_block_bytes_by_suffix_v406_installed': sizes(H6, core6)}
pb7 = json.loads((W / 'app/PREPARED_BINDING.json').read_bytes()); pb6 = json.loads((Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103') / 'app/PREPARED_BINDING.json').read_bytes())
WIN = 1048576
cap = {}
for tag, pb in (('v407', pb7), ('v406', pb6)):
    for prov, b in pb['shared_connector_bounds'].items():
        used = b['input_utf8_byte_bound']
        if prov == 'deepseek':
            cap[tag + ':' + prov] = WIN - used - 4096 - 128 - 16384     # output_budget exige >= min(16384, maximo)
        else:
            cap[tag + ':' + prov] = WIN - used - b['output_tokens'] - 4096   # saida fixa
out['conversation_capacity_bytes_before_visible_refusal'] = cap
json.dump(out, open(HERE / 'q_extra_numbers_out.json', 'w', encoding='utf8'), indent=1)
print(json.dumps(out, indent=1))
